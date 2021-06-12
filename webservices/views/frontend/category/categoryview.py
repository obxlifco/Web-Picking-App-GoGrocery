
from django.shortcuts import render

from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.http import JsonResponse

# Import Model And Serializer
from webservices.models import *
from webservices.serializers import *
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
import sys,os
import traceback

from django.db.models import F, Func, FloatField
from django.db.models.functions import Cast
# from webservices.views.frontend.common.common import CommonFunctionality

@csrf_exempt
def ParentCategoryListView(request):
	website_id = request.META.get('HTTP_WID')
	data = {"status" : 0,"msg" : "something went wrong"}
	try:
		if website_id is None:
			raise Exception("Website id is required") 
		rs_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, parent_id=0).all().order_by('display_order')[:15]
		category_data = CategoryMastersSerializer(rs_category, many=True)
		category_data = category_data.data
		if category_data:
			
			data = {
				"status":1,
				"data":category_data
			}
		else:
			data = {
				"status":0,
				"msg":"No data found.",
				"data":[]
			}
	except Exception as error:
		data["msg"] = str(error)

	return JsonResponse(data)

# def Parent_Category_ListView(website_id):
# 	rs_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, parent_id=0).all().order_by('display_order')[:15]
# 	category_data = CategoryMastersSerializer(rs_category, many=True)
# 	category_data = category_data.data
# 	return category_data


def GetChildByParent(parent_id, website_id, grand_parent): 
    rs_child = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, parent_id = parent_id).all().order_by('display_order')
    child_data = CategoriesNewSerializer(rs_child, many=True)
    child_data = child_data.data
    if child_data:
        for childdata in child_data:
            childdata['grand_parent_id'] = grand_parent
            child = {}
            child = GetChildByParent(childdata['id'], website_id, childdata['parent_id'])
            if child:
                childdata['child'] = child
            else:
                childdata['child'] = []
        
    return child_data  




class Sin(Func):
	function = 'SIN'


class Cos(Func):
	function = 'COS'


class Acos(Func):
	function = 'ACOS'


class Radians(Func):
	function = 'RADIANS'


class Degrees(Func):
	function = 'DEGREES'


class Float(Func):
	function = 'FLOAT'


def get_child_by_parent_id(parent_id, company_website_id, grand_parent): 
    cm_child = EngageboostCmsMenus.objects.filter(isdeleted='n', isblocked='n', company_website_id=company_website_id, parent_id= parent_id).all().exclude(page_id=None)
    child_data = CmsMenusNewSerializer(cm_child, context={'company_website_id':company_website_id},many=True)
    #print(cm_child.query)
    child_data = child_data.data
    if child_data:
        for childdata in child_data:
            childdata['grand_parent_id'] = grand_parent
            child = {}
            child = get_child_by_parent_id(childdata['id'], company_website_id, childdata['parent_id'])
            if child:
                childdata['child'] = child
            else:
                childdata['child'] = []
        
    return child_data   

@csrf_exempt
def menu_bar(request):
	# header menu
	# http_origin = request.user_agent.device

	# print("************** Http origin  ****************")
	# print(parse(http_origin))
	if request.method == 'POST':
		latitude 	= request.POST.get("latitude") 
		longitude 	= request.POST.get("longitude") 
		website_id 	= request.POST.get("website_id")
		lang_code 	= request.POST.get("lang_code")
		# if request.META.get('HTTP_X_FORWARDED_FOR') :
		# 	ip = request.META.get('HTTP_X_FORWARDED_FOR')
		# else :
		# 	ip = request.META.get('REMOTE_ADDR')
		
		#request_ip = CommonFunctionality.get_client_ip(request)
		#print("************** Request ip address **************")
		#current_lat_lng = CommonFunctionality.get_lat_lng_by_ip(ip)
		# print(current_lat_lng)
		# print("************** Current lat lng **************")
		# latitude = request.POST.get('latitude') 
		# longitude = request.POST.get('longitude') 
		# website_id = request.POST.get("website_id")
		# lang_code = request.POST.get("lang_code")
		# print(website_id)
		# print(lang_code)

		try:
			if latitude is None:
				raise Exception("latitude is required") 
			if longitude is None :
				raise Exception("longitude is required") 
			if website_id is None:
				raise Exception("website_id is required")
			if lang_code is None:
				raise Exception("lang_code is required")

			# request.user_agent.device
			# print("****** Request user agent  ***************")
			# print(request.user_agent)

			radlat = Radians(float(latitude))
			radlong = Radians(float(longitude))
			radflat = Radians(Cast(F('latitude'), FloatField()))
			radflong = Radians(Cast(F('longitude'), FloatField()))

			Expression = 111.045 * Degrees(Acos(Cos(radlat) * Cos(radflat) * Cos(radflong - radlong) + Sin(radlat) * Sin(radflat)))


			objWarehouse = EngageboostWarehouseMasters.objects.annotate(distance=Expression).filter(website_id=website_id).exclude(latitude__isnull=True,longitude__isnull=True).order_by('distance')
			Category_data = []
			if len(objWarehouse)>0:
				objWarehouse = objWarehouse.first()
				if objWarehouse.max_distance_sales:
					if objWarehouse.distance <= objWarehouse.max_distance_sales:
						objWarehouse_Categorylst = EngageboostCategoryWarehouse.objects.filter(warehouse_id=objWarehouse.id).values_list("category_id",flat=True)
						
						objCategorymaster = EngageboostCategoryMasters.objects.filter(id__in=objWarehouse_Categorylst, parent_id=0, show_navigation='Y',isblocked='n', isdeleted='n').all().order_by('display_order')
						
						Category_data = CategoriesNewSerializer(objCategorymaster,many=True).data
						
						if Category_data:
							for categorydata in Category_data:
								child = {}
								child = GetChildByParent(categorydata['id'], website_id, categorydata['parent_id'])
								if child:
									categorydata['child']= child
								else:
									categorydata['child']= []


			cmsmenu_qs = EngageboostCmsMenus.objects.filter(isblocked='n',isdeleted='n',parent_id=0,flag=0,company_website_id=website_id).all().exclude(page_id=None) #flag=0 for header
			menu_data  = CmsMenusNewSerializer(cmsmenu_qs,context={'website_id':website_id},many=True)
			menu_data  = menu_data.data
			if menu_data:
				for data in menu_data:
					child = {}
					child = get_child_by_parent_id(data['id'], website_id, data['parent_id'])
					if child:
						data['child']= child
					else:
						data['child']= []

			
			# page_data =PagesSerializerNew(page_qs,many=True)
			# page_data = page_data.data
			#menu_data = menu_data.data
			# print("************* Cms smenu data ************")
			# print(menu_data)
		
			data = {
				"status":1,
				"menu_bar":Category_data, 
				"cms_menu":menu_data
				}

			
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data = {"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
	return JsonResponse(data)


@csrf_exempt 
def footermenu(request):
	# footer menu
	if request.method == 'POST':
		company_website_id = request.POST.get('company_website_id') 
		try:
			if company_website_id is None:
			 	raise Exception("company website id is required") 

				# "cms_menu":menu_data,
				# "lat_lng" : current_lat_lng,
			
			
			cmsmenu_qs = EngageboostCmsMenus.objects.filter(isblocked='n',isdeleted='n',flag=1,parent_id=0,company_website_id=company_website_id).all().exclude(page_id=None)
			menu_data  = CmsMenusNewSerializer(cmsmenu_qs,context={'company_website_id':company_website_id},many=True)
			menu_data  = menu_data.data
			if menu_data:
				for data in menu_data:
					child = {}
					child = get_child_by_parent_id(data['id'], company_website_id,data['parent_id'])
					if child:
						data['child']= child
					else:
						data['child']= []

				data = {
					"status":1,
					"footer_menu":menu_data
				}
			else:
				data = {
					"status":0,
					"msg":"No data found.",
					"footer_menu":[]
				}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data = {"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}

	return JsonResponse(data)


@csrf_exempt
def ShopByCategory(request):
	website_id = request.META.get('HTTP_WID')
	data = {"status" : 0,"msg" : "something went wrong"}
	try:
		if website_id is None:
			raise Exception("Website id is required") 
		parent_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id,parent_id=0).values_list('id', flat=True)
		sub_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id,parent_id__in=parent_category).all().order_by('display_order')
		#print(sub_category.query)
		category_data = CategoryMastersSerializer(sub_category, many=True)
		category_data = category_data.data
		if category_data:
			
			data = {
				"status":1,
				"data":category_data
			}
		else:
			data = {
				"status":0,
				"msg":"No data found.",
				"data":[]
			}
	except Exception as error:
		trace_back = sys.exc_info()[2]
		line = trace_back.tb_lineno
		data = {"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}

	return JsonResponse(data)


def Shop_By_Category(website_id):
	parent_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id,parent_id=0).values_list('id', flat=True)
	sub_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id,parent_id__in=parent_category).all().order_by('display_order')
	#print(sub_category.query)
	category_data = CategoryMastersSerializer(sub_category, many=True)
	category_data = category_data.data
	return category_data


@csrf_exempt
def ShopByCategoryByCatId(request):
	if request.method == 'POST':
		website_id = request.POST.get('website_id')
		category_ids = request.POST.getlist('category_ids[]')
		try:
			if website_id is None:
				raise Exception("Website id is required")
			# if len(id)==0:
			# 	raise Exception("id is required")

			parent_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id,id__in=category_ids).all()
			#print(parent_category.query)
			category_data = CategoryMastersSerializer(parent_category, many=True)
			category_data = category_data.data
			if category_data:
				data = {
					"status":1,
					"data":category_data
				}
			else:
				data = {
					"status":0,
					"msg":"No data found.",
					"data":[]
				}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
	return JsonResponse (data)
