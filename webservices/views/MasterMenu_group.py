from django.shortcuts import render
from rest_framework import viewsets,generics
from webservices.models import EngageboostMenuMasters, EngageboostUsers, EngageboostRoleMenuPermissions
from webservices.serializers import MenuSerializer
from django.http import HttpResponse
import json
from webservices.views import loginview
""" View to represent the Menu """
class MenuGroup(viewsets.ModelViewSet):

	""" Listing Function to Fetch Menu """
	def list(self, request):
		company_db = loginview.db_active_connection(request)
		company_db='BoostPrimemall'
		user    = request.user
		user_id = user.id
		users = EngageboostUsers.objects.get(id=user_id)
		issuperadmin = users.issuperadmin
		role_id = users.role_id


		role_per = EngageboostRoleMenuPermissions.objects.all().filter(role_id=role_id,isblocked=0,isdeleted=0)
		master_id_arr=[]
		for role_data in role_per:
			master_id_arr.append(role_data.master_id)

		menudata=[]
		
		# queryset = EngageboostMenuMasters.objects.all().filter(isblocked=0,isdeleted=0,parent_id=0).order_by('orders')
		if issuperadmin=='Y' or issuperadmin=='y':
			queryset = EngageboostMenuMasters.objects.all().filter(isblocked=0,isdeleted=0,parent_id=0).order_by('orders')
		else:
			queryset = EngageboostMenuMasters.objects.all().filter(isblocked=0,isdeleted=0,parent_id=0).filter(id__in=master_id_arr).order_by('orders')

		serializer_class = MenuSerializer
		menulist = MenuSerializer(queryset, many=True)

		""" Generate Submenu """
		for menu in menulist.data:
			parentdata={}			
			parentdata=menu
			if menu['parent_id']==0:
				childmenudata={}
				
				# querychild = EngageboostMenuMasters.objects.all().filter(isblocked=0,isdeleted=0,parent_id=menu['id']).order_by('orders')
				if issuperadmin=='Y':
					querychild = EngageboostMenuMasters.objects.all().filter(isblocked=0,isdeleted=0,parent_id=menu['id']).order_by('orders')
				else:
					querychild = EngageboostMenuMasters.objects.all().filter(isblocked=0,isdeleted=0,parent_id=menu['id']).filter(id__in=master_id_arr).order_by('orders')

				childmenulist = MenuSerializer(querychild, many=True)
				if len(childmenulist.data)>0:     
					childmenudata=childmenulist.data
					parentdata['child']=childmenudata
				else:
					
					parentdata['child']=[]
			menudata.append(parentdata)
		""" Send Response """      

		return HttpResponse(json.dumps({"data": menudata}), content_type='application/json')


