from webservices.models import *
from django.http import Http404
from webservices.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime
from rest_framework import generics
from itertools import chain
from django.core import serializers
from django.http import HttpResponse
from webservices.views import loginview
from django.db.models import Q
import json
from django.db.models import F,Count,Sum,Avg,FloatField,Case,When,IntegerField,Max
# from django.views.generic import TemplateView
from django.views.generic import View
class MenuAdd(APIView):
# """ Add New Page Menu """
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		flag=request.data['flag']
		d2=request.data
		if d2['parent_id']==0:
			menu_count=EngageboostCmsMenus.objects.using(company_db).filter(isdeleted='n',flag=flag).count()
			if menu_count>0:
				menu=EngageboostCmsMenus.objects.using(company_db).filter(isdeleted='n',flag=flag)	
				menu=menu.aggregate(ulorder = Max('ulorder'))
				ulorder=menu['ulorder']+1
			else:	
				ulorder=1
			d1={'created':datetime.now(),'modified':datetime.now(),'ulorder':ulorder,'liorder':0}
		else:
			parent_id=d2['parent_id']
			parent_ul=EngageboostCmsMenus.objects.using(company_db).all().filter(isdeleted='n',id=parent_id)
			for parent_uls in parent_ul:
				ulorder=parent_uls.ulorder
			menu=EngageboostCmsMenus.objects.using(company_db).filter(isdeleted='n',ulorder=ulorder)	
			menu=menu.aggregate(liorder = Max('liorder'))
			liorder=menu['liorder']+1
			d1={'created':datetime.now(),'modified':datetime.now(),'ulorder':ulorder,'liorder':liorder}
		serializer_data=dict(d2,**d1)
		serializer = CmsMenusSerializer(data=serializer_data,partial=True)
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
class EditMenu(APIView):
# """ Edit New Page Menu """	
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostCmsMenus.objects.using(company_db).get(pk=pk)
		except EngageboostCmsMenus.DoesNotExist:
			raise Http404		
	def get(self, request, pk,flag, format=None):
		company_db = loginview.db_active_connection(request)
		flag=flag
		settings = EngageboostCmsMenus.objects.using(company_db).all().filter(isdeleted='n',flag=flag,id=pk)
		serializer = CmsMenusSerializer(settings,many=True)
		row_dict={}
		row=[]
		for serializers_row in serializer.data :
			row_dict=serializers_row
			category=serializers_row['category_id']
			page_id=serializers_row['page_id']
			if category is not None:
				cat_name=EngageboostCategoryMasters.objects.using(company_db).get(id=category)
				category=cat_name.name
				row_dict['name']=category
			elif page_id is not None:
				page_id=serializers_row['page_id']				
				cat_name=EngageboostPages.objects.using(company_db).get(id=page_id)
				page=cat_name.page_name
				row_dict['name']=page
			row.append(row_dict)
		menu=EngageboostCmsMenus.objects.using(company_db).all().filter(isdeleted='n',parent_id=0,flag=flag)	
		menus_master=[]
		for menus in menu:
			if menus.flag == 1:
				d1={'name':menus.label,'id':menus.id}
				menus_master.append(d1)
			else:
				if menus.page_id is not None:
					header_menu=EngageboostPages.objects.using(company_db).get(id=menus.page_id)
					d1={'name':header_menu.page_name,'id':menus.id}
					menus_master.append(d1)
				elif menus.category_id is not None:
					header_menu=EngageboostCategoryMasters.objects.using(company_db).get(id=menus.category_id)
					d1={'name':header_menu.name,'id':menus.id}
					menus_master.append(d1)
		if(serializer): 
			data ={
				'status':1,
				'api_status':row,
				'header_menu':menus_master
			}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
			}
		return Response(data)

	def put(self, request, pk,flag, format=None):
		company_db = loginview.db_active_connection(request)
		d1={'modified':datetime.now()}
		d2=request.data
		serializer_data=dict(d2,**d1)
		page = self.get_object(pk,request)
		serializer = CmsMenusSerializer(page, data=serializer_data,partial=True)
		if serializer.is_valid():
			serializer.save()
			data ={
			'status':1,
			'api_status':'',
			'message':'Successfully Updated',
			}
			return Response(data)
		else:
			data ={
			'status':0,
			'api_status':serializer.errors,
			'message':'Data Not Found',
			}
			return Response(data)
		
class HeaderMenu(APIView):
	def get(self, request,pk, website_id,format=None):
		company_db = loginview.db_active_connection(request)
		flag=pk
		menu=EngageboostCmsMenus.objects.using(company_db).all().filter(isdeleted='n',parent_id=0,flag=flag,company_website_id=website_id)	
		menus_master=[]
		for menus in menu:
			if menus.flag == 1:
				d1={'name':menus.label,'id':menus.id}
				menus_master.append(d1)
			else:
				if menus.category_id is  None:
					header_menu=EngageboostPages.objects.using(company_db).get(id=menus.page_id)
					d1={'name':header_menu.page_name,'id':menus.id}
					menus_master.append(d1)
				else:
					header_menu=EngageboostCategoryMasters.objects.using(company_db).get(id=menus.category_id)
					d1={'name':header_menu.name,'id':menus.id}
					menus_master.append(d1)
		return HttpResponse(json.dumps({"header_menu":menus_master}), content_type='application/json')        


class AllMenu(View):
	def get(self, request,pk, website_id,format=None):
		#company_db = loginview.db_active_connection(request)
		flag=pk
		menu=EngageboostCmsMenus.objects.all().filter(isdeleted='n',parent_id=0,flag=flag,company_website_id=website_id)
		menus_master=[]
		for menus in menu:
			if menus.flag == 1:
				d1={'name':menus.label,'id':menus.id}
				menus_master.append(d1)
			else:

				if menus.category_id is  None:
					header_menu=EngageboostPages.objects.get(id=menus.page_id)
					d1={'name':header_menu.page_name,'id':menus.id,'url':header_menu.url,'type': 'page'}
					menus_master.append(d1)
				else:
					header_menu=EngageboostCategoryMasters.get(id=menus.category_id)
					d1={'name':header_menu.name,'id':menus.id,'url':header_menu.slug,'type': 'category'}
					menus_master.append(d1)
		sub_menu=EngageboostCmsMenus.objects.all().filter(isdeleted='n',flag=flag,company_website_id=website_id).filter(~Q(parent_id=0))	
		child_menus_master=[]
		for sub_menus in sub_menu:
			if sub_menus.category_id is  None:
				header_menu=EngageboostPages.objects.get(id=sub_menus.page_id)
				d1={'name':header_menu.page_name,'id':sub_menus.id,'parent_id':sub_menus.parent_id,'url':header_menu.url,'type': 'page'}
				child_menus_master.append(d1)
			else:
				header_menu=EngageboostCategoryMasters.objects.get(id=sub_menus.category_id)
				d1={'name':header_menu.name,'id':sub_menus.id,'parent_id':sub_menus.parent_id,'url':header_menu.slug,'type': 'category'}
				child_menus_master.append(d1)
		return HttpResponse(json.dumps({"header_menu":menus_master,'child':child_menus_master}), content_type='application/json')        


class CategoriesListMenu(APIView):
# """ Categories Selected  """
	#///////////////////Fetch Single Row
	def get(self, request, website_id,format=None):
		company_db = loginview.db_active_connection(request)
		user = EngageboostCategoryMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n',parent_id=0,website_id=1).order_by('name')
		serializer = CategoriesSerializer(user,many=True)
		data_parent={}
		arr1=[]
		menudata=[]
		for menu in serializer.data:
			parentdata={}
			parentdata=menu
			if menu['parent_id']==0:
				childmenudata={}
				querychild = EngageboostCategoryMasters.objects.all().filter(isblocked='n',isdeleted='n',parent_id=menu['id'])
				childmenulist = CategoriesSerializer(querychild, many=True)
				if len(childmenulist.data)>0:     
					childmenudata=childmenulist.data
					parentdata['child']=childmenudata
					index = 0
					for childmenudata1 in childmenudata:
						querychild1 = EngageboostCategoryMasters.objects.all().filter(isblocked='n',isdeleted='n',parent_id=childmenudata1['id'])
						childmenulist1 = CategoriesSerializer(querychild1, many=True)
						childmenudata1=childmenulist1.data
						parentdata['child'][index]['child']=childmenudata1
						index = index +1
				else:
					parentdata['child']=[]
			menudata.append(parentdata)
		return HttpResponse(json.dumps({"parent_child":menudata}), content_type='application/json')