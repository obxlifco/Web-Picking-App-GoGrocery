from webservices.models import EngageboostGroups,EngageboostMenuMasters,EngageboostRolemasters,EngageboostRoleMenuPermissions, EngageboostUsers
from django.http import Http404
from webservices.serializers import GroupSerializer,MenuSerializer
from rest_framework.views import APIView
from rest_framework import generics,viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from webservices.views import loginview

class GroupsList(generics.ListAPIView):
# """ List all Groups with pagination,sorting and searching """
	
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
			groups = EngageboostGroups.objects.using(company_db).all().filter(isdeleted='n').filter(name__icontains=key).order_by(order)
		elif request.data.get('search'):
			key=request.data.get('search')
			groups = EngageboostGroups.objects.using(company_db).all().filter(isdeleted='n').filter(name__icontains=key).order_by('-id')
		elif request.data.get('order_by'):
			order_by=request.data.get('order_by')
			order_type=request.data.get('order_type')
			if(order_type=='+'):
				order=order_by
			else:
				order='-'+order_by
			groups = EngageboostGroups.objects.using(company_db).all().filter(isdeleted='n').order_by(order)    
		else:
			groups = EngageboostGroups.objects.using(company_db).all().filter(isdeleted='n').order_by('-id')
		# /////////Create Pagination    
		page = self.paginate_queryset(groups)
		if page is not None:
			serializer = GroupSerializer(page, many=True)
			return self.get_paginated_response(serializer.data) 
		serializer = self.GroupSerializer(groups, many=True)
		return Response(serializer.data)

class GroupsAction(generics.ListAPIView):
# """ Create a new Group ,Bulk Delete , Bulk Status Change """
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		d1={'created':datetime.now().date(),'modified':datetime.now().date()}
		d2=request.data
		#print(request.data['website_id'])
		#print(request.data['name'])
		warehouse_id = None
		if "warehouse_id" in request.data:
			if request.data['warehouse_id']!="":
				warehouse_id = request.data['warehouse_id']

		cnt = EngageboostGroups.objects.using(company_db).filter(website_id=request.data['website_id'],name=request.data['name'],isdeleted='n').count()
		if warehouse_id is not None:
			cnt = EngageboostGroups.objects.using(company_db).filter(website_id=request.data['website_id'],name=request.data['name'],isdeleted='n', warehouse_id = warehouse_id).count()
			
		if cnt == 0:
			serializer_data=dict(d2,**d1)
			serializer = GroupSerializer(data=serializer_data)
			if serializer.is_valid():
				serializer.save()
				data ={
				'status':1,
				'api_status':'',
				'message':'Successfully Inserted',
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
			'message':'Group name is already exists',
			}
			return Response(data)


class GroupsDetail(generics.ListAPIView):
	# """Retrieve, update a Group instance."""

	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostGroups.objects.using(company_db).get(pk=pk)
		except EngageboostGroups.DoesNotExist:
			raise Http404

	#///////////////////Fetch Single Row
	def get(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)

		groups = self.get_object(pk,request)
		menu_group=groups.masters.split(",")
		menu_group=[int(x) for x in menu_group]
		
		serializer = GroupSerializer(groups)
		# users = EngageboostUsers.objects.get(id=groups.user_id)
		users = request.user
		issuperadmin = users.issuperadmin
		role_id = users.role_id

		# ///////////////////MENU

		role_per = EngageboostRoleMenuPermissions.objects.all().filter(role_id=role_id,isblocked=0,isdeleted=0)
		master_id_arr=[]
		for role_data in role_per:
			master_id_arr.append(role_data.master_id)

		menudata=[]
		# queryset = EngageboostMenuMasters.objects.using(company_db).all().filter(isblocked=0,isdeleted=0,parent_id=0).order_by('orders')
		if issuperadmin=='Y' or issuperadmin=='y':
			queryset = EngageboostMenuMasters.objects.all().filter(isblocked=0,isdeleted=0,parent_id=0).order_by('orders')
		else:
			queryset = EngageboostMenuMasters.objects.all().filter(isblocked=0,isdeleted=0,parent_id=0).filter(id__in=master_id_arr).order_by('orders')

		serializer_class = MenuSerializer
		menulist = MenuSerializer(queryset, many=True)
		""" Generate Submenu """
		for menu in menulist.data:
			# print(menus)
			if menu['id'] in menu_group:
				parent_s=1
			else:
				parent_s=0
			parentdata={}           
			parentdata=menu
			parentdata['status'] = parent_s
			if menu['parent_id']==0:
				childmenudata={}
				querychild = EngageboostMenuMasters.objects.using(company_db).all().filter(isblocked=0,isdeleted=0,parent_id=menu['id']).order_by('orders')
				childmenulist = MenuSerializer(querychild, many=True)
				if len(childmenulist.data)>0:
					for child in childmenulist.data:
						if child['id'] in menu_group:
							child_s=1
						else:
							child_s=0     
						childmenudata=child
						childmenudata['status'] = child_s
					parentdata['child']=childmenulist.data
				else:
					parentdata['child']=[]
			menudata.append(parentdata)
		# ///////////////////
		menu={}
		menu['menu']=menudata
		grp={}
		grp['grp']=serializer.data
		finaldata=dict(grp,**menu)
		if(serializer): 
			data ={
				'status':1,
				'api_status':finaldata,
				'message':'',
				}
		else:
			data ={
			'status':0,
			'api_status':serializer.errors,
			'message':'Data Not Found',
			}
		return Response(data)

	#///////////////////Update All Fields
	def put(self, request, pk, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		groups = self.get_object(pk,request)
		d1={'modified':datetime.now().date()}
		d2=request.data
		cnt = EngageboostGroups.objects.using(company_db).filter(website_id=request.data['website_id'],name=request.data['name'],isdeleted='n').filter(~Q(id=pk)).count()
		if cnt == 0:
			serializer_data=dict(d2,**d1)
			serializer = GroupSerializer(groups,data=serializer_data,partial=True)
			if serializer.is_valid():
				serializer.save()
				groups =EngageboostGroups.objects.using(company_db).get(id=pk)
				master_id=groups.masters
				master=[int(x) for x in master_id.split(",")]
				
				role_id=EngageboostRolemasters.objects.using(company_db).all().filter(group_id=pk)
				
				for role in role_id:
				
					EngageboostRoleMenuPermissions.objects.using(company_db).filter(role_id=role.id).filter(~Q(master_id__in=master)).delete()
					for masters in master:
						cnt = EngageboostRoleMenuPermissions.objects.using(company_db).filter(role_id=role.id).filter(master_id=masters).count()
						querysetParent = EngageboostMenuMasters.objects.using(company_db).get(id=masters)
						countParent=EngageboostRoleMenuPermissions.objects.using(company_db).filter(role_id=role.id).filter(master_id=querysetParent.parent_id).count()
						if countParent==0:
							EngageboostRoleMenuPermissions.objects.using(company_db).create(role_id=role.id,master_id=querysetParent.parent_id,add='N',edit='N',delete='N',view='N',block='N',import_field=0,export=0,shipping_processes=0,print=0,created=datetime.now().date(),modified=datetime.now().date(),isdeleted=0,isblocked=0)
						if cnt ==0:
							EngageboostRoleMenuPermissions.objects.using(company_db).create(role_id=role.id,master_id=masters,add='N',edit='N',delete='N',view='N',block='N',import_field=0,export=0,shipping_processes=0,print=0,created=datetime.now().date(),modified=datetime.now().date(),isdeleted=0,isblocked=0)
				
				data ={
				'status':1,
				'api_status':serializer.data,
				'message':'Successfully Updated',
				}
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
			'message':'Group name is already exists',
			}
			return Response(data)
# Avtive Inactive and all methon code here        
class Active(APIView):
	def get(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		
		active = EngageboostGroups.objects.using(company_db).filter(isdeleted='n').count()
		Inactive = EngageboostGroups.objects.using(company_db).filter(isdeleted='y').count()
		al = EngageboostGroups.objects.using(company_db).filter().count()
		data = {
		'Active':active,
		'Inactive':Inactive,
		'all':al 
		}
		return JsonResponse(data)
