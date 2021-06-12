from webservices.models import EngageboostRolemasters,EngageboostGroups,EngageboostUsers,EngageboostMenuMasters,EngageboostRoleMenuPermissions, EngageboostWarehouseManager
from django.http import Http404
import json
from webservices.serializers import RoleSerializer,GroupSerializer,UserSerializer,MenuSerializer,MenuPermitionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime
from rest_framework import generics
from django.http import HttpResponse
from django.db.models import Q
from webservices.views import loginview

# from rest_framework.pagination import PageNumberPagination
class RoleList(generics.ListAPIView):
# """ List all Roles with pagination,sorting and searching """
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        # /////////Create Query
        if request.data.get('search') and request.data.get('order_by'):
            key=request.data.get('search')
            order_by=request.data.get('order_by')
            order_type=request.data.get('order_type')
            if(order_type=='+'):
                order=order_by
            else:
                order='-'+order_by
            groups = EngageboostRolemasters.objects.using(company_db).all().filter(isdeleted='n').filter(name__icontains=key).order_by(order)  
        elif request.data.get('search'):
            key=request.data.get('search')
            groups = EngageboostRolemasters.objects.using(company_db).all().filter(isdeleted='n').filter(name__icontains=key).order_by('-id')
        elif request.data.get('order_by'):
            order_by=request.data.get('order_by')
            order_type=request.data.get('order_type')
            if(order_type=='+'):
                order=order_by
            else:
                order='-'+order_by
            groups = EngageboostRolemasters.objects.using(company_db).all().filter(isdeleted='n').order_by(order)    
        else:
            groups = EngageboostRolemasters.objects.using(company_db).all().filter(isdeleted='n').order_by('-id')
        # /////////Create Pagination    
        page = self.paginate_queryset(groups)
        if page is not None:
            serializer = RoleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data) 
        serializer = self.RoleSerializer(groups, many=True)
        return Response(serializer.data)


class RoleMasterViewSet(generics.ListAPIView):
# """ Create a new Role """
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        d2=request.data
        d1={'created':datetime.now().date(),'modified':datetime.now().date(),"website_id":d2['website_id']}
        ourResult = d2['addrule']

        warehouse_id = 0
        if "warehouse_id" in request.data:
            if request.data['warehouse_id']!="":
                warehouse_id = request.data['warehouse_id']
                # d1={'created':datetime.now().date(),'modified':datetime.now().date(),"website_id":d2['website_id']}
                d1.update({'warehouse_id':warehouse_id})

        cnt = EngageboostRolemasters.objects.using(company_db).filter(name=ourResult['name'],isdeleted='n').count()
        if warehouse_id is not None:
            cnt = EngageboostRolemasters.objects.using(company_db).filter(name=ourResult['name'],isdeleted='n', warehouse_id = warehouse_id).count()

        if cnt == 0:
            serializer_data=dict(ourResult,**d1)
            serializer = RoleSerializer(data=serializer_data,partial=True)
            if serializer.is_valid():
                serializer.save()
                obj = EngageboostRolemasters.objects.using(company_db).latest('id')
                last_id = obj.id
                d1={'created':datetime.now().date(),'modified':datetime.now().date(),'role_id':last_id}
                ourResultset='' 
                # ourResultset.append(d2['ruleset'])
                # print(ourResultset)
                serializer_data=dict(ourResultset,**d1)
                for data in request.data['ruleset']:
                    final=dict(data,**d1)
                    querysetParent = EngageboostMenuMasters.objects.using(company_db).get(id=data['master_id'])
                    countParent=EngageboostRoleMenuPermissions.objects.using(company_db).filter(role_id=last_id).filter(master_id=querysetParent.parent_id).count()
                    if countParent==0:
                        EngageboostRoleMenuPermissions.objects.using(company_db).create(role_id=last_id,master_id=querysetParent.parent_id,add='N',edit='N',delete='N',view='N',block='N',import_field=0,export=0,shipping_processes=0,print=0,created=datetime.now().date(),modified=datetime.now().date(),isdeleted=0,isblocked=0)
                        serializer1 = MenuPermitionSerializer(data=final,partial=True)
                    serializer1 = MenuPermitionSerializer(data=final,partial=True)
                    if serializer1.is_valid():
                        serializer1.save()
                        data ={
                        'status':1,
                        
                        'message':'Successfully Inserted',
                        }
                    else:
                        data ={
                        'status':0,
                        'api_status':serializer1.errors,
                        'message':'Data Not Found',
                        }
                return Response(data)
            else:
                data ={
                'status':0,
                'api_status':serializer.errors,
                'message':'Data Not Found',
                }
            return Response(data)
        else:
            data ={
            'status':0,
            'message':'Role name is already exists',
            }
            return Response(data)

class RoleMasterDetail(APIView):
    # """Retrieve, update or delete a role instance."""
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostRolemasters.objects.using(company_db).get(pk=pk)
        except EngageboostRolemasters.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        company_db = loginview.db_active_connection(request)
        roles = self.get_object(pk,request)
        serializer = RoleSerializer(roles)
        grouplist = EngageboostGroups.objects.using(company_db).get(id=roles.group_id)
        users = request.user
        user_id = users.id
        issuperadmin = users.issuperadmin
        
        if issuperadmin.lower() == 'y':
            groups = EngageboostGroups.objects.using(company_db).all().filter(isdeleted='n', isblocked='n').order_by('name')
        else:
            rs_wh_manager = EngageboostWarehouseManager.objects.filter(manager_id = user_id).first()
            if rs_wh_manager:
                warehouse_id = rs_wh_manager.warehouse_id
                groups = EngageboostGroups.objects.using(company_db).all().filter(isdeleted='n', isblocked='n',
                                                                                  warehouse_id=warehouse_id).order_by('name')
        if groups:
            serializer_grp = GroupSerializer(groups, many=True).data
        else:
            serializer_grp = []

        menu_group=grouplist.masters.split(",")
        final_data=[]
        child=[]
        parentdata={}
        parentdata['addrule']=serializer.data
        for menu_id in menu_group:
            menu1 =EngageboostMenuMasters.objects.using(company_db).filter(id=menu_id).filter(~Q(parent_id=0)).count()
            if menu1>0:
                menu = EngageboostMenuMasters.objects.using(company_db).get(id=menu_id)
                menu_pem = EngageboostRoleMenuPermissions.objects.using(company_db).get(master_id=menu_id,role_id=pk)
                childdata={
                'role_id':menu_pem.role_id,
                'name':menu.name,
                'id':menu_id,
                'add':menu_pem.add,
                'edit':menu_pem.edit,
                'view':menu_pem.view,
                'delete':menu_pem.delete,
                'block':menu_pem.block,
                'import_field':menu_pem.import_field,
                'export':menu_pem.export,
                'shipping_processes':menu_pem.shipping_processes,
                'print':menu_pem.print,
                }

                # parentdata['menu']=serializer_menu.data
                child.append(childdata)
        parentdata['ruleset']=child 
        parentdata['grp']=serializer_grp     
        final_data.append(parentdata)

        if(serializer): 
            data ={
                'status':1,
                'api_status':final_data,
                'message':'',
                }
        else:
            data ={
                'status':0,
                'api_status':serializer.errors,
                'message':'Data Not Found',
                }
        return Response(data)

# """ Update a new Role """
    def put(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        roles = self.get_object(pk,request)
        d2=request.data
        d1={'modified':datetime.now().date(),"website_id":d2['website_id']}
        ourResult = d2['addrule']
        user_role_type = ourResult['user_role_type']
        cnt = EngageboostRolemasters.objects.using(company_db).filter(name=ourResult['name'],isdeleted='n').filter(~Q(id=pk)).count()
        if cnt == 0:
            if user_role_type=="Super Admin":
                group_id = EngageboostRolemasters.objects.using(company_db).get(id=pk)
                user_id = EngageboostGroups.objects.using(company_db).all().filter(id=group_id.id)
                for user in user_id:
                    
                    EngageboostUsers.objects.using(company_db).filter(id=user.user_id).update(issuperadmin='Y')

            serializer_data=dict(ourResult,**d1)
            serializer = RoleSerializer(roles,data=serializer_data,partial=True)
            if serializer.is_valid():
                serializer.save()
                d1={'created':datetime.now().date(),'modified':datetime.now().date(),'role_id':pk}
                ourResultset='' 
                serializer_data=dict(ourResultset,**d1)
                data_exist = EngageboostRoleMenuPermissions.objects.using(company_db).all().filter(role_id=pk)
                data_exist.delete()
                for data1 in request.data['ruleset']:
                    final=dict(data1,**d1)
                    
                    querysetParent = EngageboostMenuMasters.objects.using(company_db).get(id=data1['master_id'])
                    countParent=EngageboostRoleMenuPermissions.objects.using(company_db).filter(role_id=pk).filter(master_id=querysetParent.parent_id).count()
                    if countParent==0:
                        EngageboostRoleMenuPermissions.objects.using(company_db).create(role_id=pk,master_id=querysetParent.parent_id,add='N',edit='N',delete='N',view='N',block='N',import_field=0,export=0,shipping_processes=0,print=0,created=datetime.now().date(),modified=datetime.now().date(),isdeleted=0,isblocked=0)
                        serializer1 = MenuPermitionSerializer(data=final,partial=True)
                    
                    serializer1 = MenuPermitionSerializer(data=final,partial=True)
                    if serializer1.is_valid():
                        serializer1.save()

                        data ={
                        'status':1,
                        'api_status':serializer.data,
                        'message':'Successfully Updated',
                        }
                    else:
                        data ={
                        'status':0,
                        'api_status':serializer1.errors,
                        'message':'Data Not Found',
                        }
                return Response(data)               
            else:
                data ={
                'status':0,
                'api_status':serializer.errors,
                'message':'Data Not Found',
                }
            return Response(data)
        else:
            data ={
            'status':0,
            'message':'Role name is already exists',
            }
            return Response(data)


class Groupname(APIView):
    def get(self, request, format=None):
        company_db = loginview.db_active_connection(request)

        requestdata = request.data
        user    = request.user
        user_id = user.id
        rs_wh_manager = EngageboostWarehouseManager.objects.filter(manager_id = user_id).first()
        if rs_wh_manager:
            warehouse_id = rs_wh_manager.warehouse_id

        if warehouse_id is not None and int(warehouse_id) >0:
            settings = EngageboostGroups.objects.using(company_db).all().filter(isdeleted='n', isblocked='n',
                                                                                warehouse_id=warehouse_id).order_by('name')
        else:
            settings = EngageboostGroups.objects.using(company_db).all().filter(isdeleted='n', isblocked='n').order_by('name')

        serializer = GroupSerializer(settings, many=True)
        return Response(serializer.data)

class UsersName(APIView):
    def get(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        settings = EngageboostUsers.objects.using(company_db).all().filter(isblocked=0,isdeleted=0).order_by('-id')
        serializer = UserSerializer(settings, many=True)
        return Response(serializer.data)

class GetRoleMenu(APIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        # print(request.data['id'])
        roles = EngageboostGroups.objects.using(company_db).get(id=request.data['id'])
        groupid = roles.masters.split(",")
        menu_name = []
        for groupname in groupid:
            menu1 =EngageboostMenuMasters.objects.using(company_db).filter(~Q(parent_id=0)).filter(id=groupname).count()
            if menu1>0:
                menu = EngageboostMenuMasters.objects.using(company_db).get(id=groupname)
                # print(menu.name)
                menu_name.append({
                'name':menu.name,
                'id':menu.id,
        })
        return HttpResponse(json.dumps({"data": menu_name}), content_type='application/json')

# This function is not needed 
class EditRole(APIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        roles = EngageboostGroups.objects.using(company_db).get(id=request.data.id)
        groupid=roles.masters.split(",")
        menu_name = []
        for groupname in groupid:
            menu = EngageboostMenuMasters.objects.using(company_db).get(id=groupname)
            #print(menu.name)
            add = EngageboostRoleMenuPermissions.objects.using(company_db).all().filter(role_id=data['id'])
            for add in add:
                menu_name.append({
                'name':menu.name,
                'id':menu.id,
                'add':add.add,
                'delete':add.delete,
                'edit':add.edit,
                'view':add.view
                })

        return HttpResponse(json.dumps({"data": menu_name}), content_type='application/json')     
