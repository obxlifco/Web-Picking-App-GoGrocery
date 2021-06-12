# from django.shortcuts import render
from rest_framework import viewsets
from webservices.models import EngageboostMenuMasters,EngageboostUsers,EngageboostRoleMenuPermissions
from webservices.serializers import MenuSerializer
from django.http import HttpResponse
import json
# from webservices.views import loginview
# from django.conf import settings
# import requests
class MenuViewSet(viewsets.ModelViewSet):
	def list(self, request,pk):
		# company_db = loginview.db_active_connection(request)
		# company_db='default'
		menudata=[]
		users = EngageboostUsers.objects.get(id=pk)
		issuperadmin = users.issuperadmin
		role_id = users.role_id
		role_per = EngageboostRoleMenuPermissions.objects.all().filter(role_id=role_id,isblocked=0,isdeleted=0)
		master_id_arr=[]
		for role_data in role_per:
			master_id_arr.append(role_data.master_id)
		
		if issuperadmin=='Y' or issuperadmin=='y':
			queryset = EngageboostMenuMasters.objects.all().filter(isblocked=0,isdeleted=0,parent_id=0,menu_type='A').order_by('orders')
		else:
			queryset = EngageboostMenuMasters.objects.all().filter(isblocked=0,isdeleted=0,parent_id=0,menu_type='A').filter(id__in=master_id_arr).order_by('orders')
			
		
		serializer_class = MenuSerializer
		menulist = MenuSerializer(queryset, many=True)
		""" Generate Submenu """
		for menu in menulist.data:
			parentdata={}
			parentdata=menu
			if menu['parent_id']==0:
				childmenudata={}
				if issuperadmin=='Y':
					querychild = EngageboostMenuMasters.objects.all().filter(isblocked=0,isdeleted=0,menu_type='A',parent_id=menu['id']).order_by('orders')
				else:
					querychild = EngageboostMenuMasters.objects.all().filter(isblocked=0,isdeleted=0,menu_type='A',parent_id=menu['id']).filter(id__in=master_id_arr).order_by('orders')
			
				childmenulist = MenuSerializer(querychild, many=True)
				if len(childmenulist.data)>0:     
					childmenudata=childmenulist.data
					parentdata['child']=childmenudata
				else:
					parentdata['child']=[]
			menudata.append(parentdata)
		""" Send Response """      
		menudata1=[]
		if issuperadmin=='Y':
			queryset = EngageboostMenuMasters.objects.all().filter(isblocked=0,isdeleted=0,parent_id=0,menu_type='F').order_by('orders')
		else:
			queryset = EngageboostMenuMasters.objects.all().filter(isblocked=0,isdeleted=0,parent_id=0,menu_type='F').filter(id__in=master_id_arr).order_by('orders')
				
		serializer_class = MenuSerializer
		menulist = MenuSerializer(queryset, many=True)
		""" Generate Submenu """
		for menu in menulist.data:
			parentdata1={}
			parentdata1=menu
			if menu['parent_id']==0:
				childmenudata={}
				if issuperadmin=='Y':
					querychild = EngageboostMenuMasters.objects.all().filter(isblocked=0,isdeleted=0,menu_type='F',parent_id=menu['id']).order_by('orders')
				else:
					querychild = EngageboostMenuMasters.objects.all().filter(isblocked=0,isdeleted=0,menu_type='F',parent_id=menu['id']).filter(id__in=master_id_arr).order_by('orders')
				childmenulist = MenuSerializer(querychild, many=True)
				if len(childmenulist.data)>0:     
					childmenudata=childmenulist.data
					parentdata1['child']=childmenudata
				else:
					parentdata1['child']=[]
			menudata1.append(parentdata1)
		return HttpResponse(json.dumps({"Frontend": menudata1,"Admin":menudata}), content_type='application/json')