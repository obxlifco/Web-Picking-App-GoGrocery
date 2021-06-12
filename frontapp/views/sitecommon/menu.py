from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
# Import Model And Serializer
from webservices.models import *
from frontapp.frontapp_serializers import *

from django.db.models import F, Func, FloatField
from django.db.models.functions import Cast

import json
import base64
import sys,os
import traceback
import datetime
import pytz

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

class GetMenuList(APIView):
    permission_classes = []

    def post(self, request, format=None):
        # latitude 	= request.POST.get("latitude") 
        # longitude 	= request.POST.get("longitude") 
        website_id 	= request.POST.get("website_id")
        lang_code 	= request.POST.get("lang_code")
        warehouse_id = request.POST.get("warehouse_id")

        try:
            # if latitude is None:
            #     raise Exception("latitude is required") 
            # if longitude is None :
            #     raise Exception("longitude is required") 
            if website_id is None:
                raise Exception("website_id is required")
            if lang_code is None:
                raise Exception("lang_code is required")
            if warehouse_id is None:
                raise Exception("warehouse id is required")

            # radlat      = Radians(float(latitude))
            # radlong     = Radians(float(longitude))
            # radflat     = Radians(Cast(F('latitude'), FloatField()))
            # radflong    = Radians(Cast(F('longitude'), FloatField()))

            # Expression = 111.045 * Degrees(Acos(Cos(radlat) * Cos(radflat) * Cos(radflong - radlong) + Sin(radlat) * Sin(radflat)))
            # objWarehouse = EngageboostWarehouseMasters.objects.annotate(distance=Expression).filter(website_id=website_id).exclude(latitude__isnull=True,longitude__isnull=True, max_distance_sales__isnull=True, max_distance_sales__gt=0).order_by('distance')
            Category_data = []
            # if len(objWarehouse)>0:
            #     objWarehouse = objWarehouse.first()
            #     if objWarehouse.max_distance_sales:
            #         if objWarehouse.distance <= objWarehouse.max_distance_sales:
            objWarehouse_Categorylst = EngageboostCategoryWarehouse.objects.filter(warehouse_id=warehouse_id,product_count__gt=0, isblocked='n', isdeleted='n').values_list("category_id",flat=True)
            objCategorymaster = EngageboostCategoryMasters.objects.filter(id__in=objWarehouse_Categorylst, parent_id=0, isblocked='n', isdeleted='n').all().order_by('display_order').iterator()
            Category_data = CategoriesNewSerializer(objCategorymaster,many=True).data
            
            categoryData = []
            if Category_data:
                for categorydata in Category_data:
                    child = {}
                    child = GetChildByParent(categorydata['id'], website_id, categorydata['parent_id'],warehouse_id)
                    if child:
                        categorydata['child']= child
                    else:
                        categorydata['child']= []
                    if child:
                        categoryData.append(categorydata)

            ######cms header#############
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
            data = {
                "status":1,
                "menu_bar":categoryData, 
                "cms_menu":menu_data
            }
            return Response(data, status.HTTP_200_OK)
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
            # return JSONResponse(errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(data, status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)



# class GetMenuList(APIView):
#     permission_classes = []
#     def post(self, request, format=None):
#         # latitude  = request.POST.get("latitude") 
#         # longitude     = request.POST.get("longitude") 
#         # website_id    = request.POST.get("website_id")
#         # lang_code     = request.POST.get("lang_code")
#         warehouse_id = request.POST.get("warehouse_id")

#         try:
#             # if latitude is None:
#             #     raise Exception("latitude is required") 
#             # if longitude is None :
#             #     raise Exception("longitude is required") 
#             # if website_id is None:
#             #     raise Exception("website_id is required")
#             # if lang_code is None:
#             #     raise Exception("lang_code is required")
#             if warehouse_id is None:
#                 raise Exception("warehouse id is required")

#             # radlat      = Radians(float(latitude))
#             # radlong     = Radians(float(longitude))
#             # radflat     = Radians(Cast(F('latitude'), FloatField()))
#             # radflong    = Radians(Cast(F('longitude'), FloatField()))

#             # Expression = 111.045 * Degrees(Acos(Cos(radlat) * Cos(radflat) * Cos(radflong - radlong) + Sin(radlat) * Sin(radflat)))
#             # objWarehouse = EngageboostWarehouseMasters.objects.annotate(distance=Expression).filter(website_id=website_id).exclude(latitude__isnull=True,longitude__isnull=True, max_distance_sales__isnull=True, max_distance_sales__gt=0).order_by('distance')
#             Category_data = []
#             # if len(objWarehouse)>0:
#             #     objWarehouse = objWarehouse.first()
#             #     if objWarehouse.max_distance_sales:
#             #         if objWarehouse.distance <= objWarehouse.max_distance_sales:
#                         objWarehouse_Categorylst = EngageboostCategoryWarehouse.objects.filter(warehouse_id=warehouse_id).values_list("category_id",flat=True).iterator()
                        
#                         objCategorymaster = EngageboostCategoryMasters.objects.filter(id__in=objWarehouse_Categorylst, parent_id=0, isblocked='n', isdeleted='n').all().order_by('display_order').iterator()
                        
#                         Category_data = CategoriesNewSerializer(objCategorymaster,many=True).data
                        
#                         if Category_data:
#                             for categorydata in Category_data:
#                                 child = {}
#                                 child = GetChildByParent(categorydata['id'], website_id, categorydata['parent_id'])
#                                 if child:
#                                     categorydata['child']= child
#                                 else:
#                                     categorydata['child']= []


#             cmsmenu_qs = EngageboostCmsMenus.objects.filter(isblocked='n',isdeleted='n',parent_id=0,flag=0,company_website_id=website_id).all().exclude(page_id=None) #flag=0 for header
#             menu_data  = CmsMenusNewSerializer(cmsmenu_qs,context={'website_id':website_id},many=True)
#             menu_data  = menu_data.data
#             if menu_data:
#                 for data in menu_data:
#                     child = {}
#                     child = get_child_by_parent_id(data['id'], website_id, data['parent_id'])
#                     if child:
#                         data['child']= child
#                     else:
#                         data['child']= []
#             data = {
#                 "status":1,
#                 "menu_bar":Category_data, 
#                 "cms_menu":menu_data
#             }
#             return Response(data, status.HTTP_200_OK)
#         except Exception as error:
#             trace_back = sys.exc_info()[2]
#             line = trace_back.tb_lineno
#             data = {"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
#             # return JSONResponse(errors, status=status.HTTP_400_BAD_REQUEST)
#             return Response(data, status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)

class FooterMenu(APIView):
	# footer menu
    permission_classes = []
    def post(self, request, format=None):
        company_website_id = request.POST.get('company_website_id') 
        try:
            if company_website_id is None:
                raise Exception("company website id is required") 
			
            cmsmenu_qs = EngageboostCmsMenus.objects.filter(isblocked='n',isdeleted='n',flag=1,parent_id=0,company_website_id=company_website_id).all().exclude(page_id=None)
            menu_data  = CmsMenusNewSerializer(cmsmenu_qs,context={'company_website_id':company_website_id},many=True)
            menu_data  = menu_data.data
            res_status = ""
            if menu_data:
                for data in menu_data:
                    child = {}
                    child = get_child_by_parent_id(data['id'], company_website_id,data['parent_id'])
                    if child:
                        data['child']= child
                    else:
                        data['child']= []
                res_status = status.HTTP_200_OK
                data = {
                    "status":status.HTTP_200_OK,
                    "footer_menu":menu_data
                }
                
            else:
                data = {
                    "status":status.HTTP_204_NO_CONTENT,
                    "msg":"No data found.",
                    "footer_menu":[]
                }
                res_status=status.HTTP_204_NO_CONTENT
            return Response(data,res_status)
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
            return Response(data)



def GetChildByParent(parent_id, website_id, grand_parent,warehouse_id=None): 
    objWarehouse_Categorylst = EngageboostCategoryWarehouse.objects.filter(warehouse_id=warehouse_id,product_count__gt=0).values_list("category_id",flat=True) 

    rs_child = EngageboostCategoryMasters.objects.filter(id__in=objWarehouse_Categorylst,isdeleted='n', isblocked='n', website_id=website_id, parent_id = parent_id).all().order_by('display_order')
    child_data = CategoriesNewSerializer(rs_child, many=True)
    child_data = child_data.data
    if child_data:
        for childdata in child_data:
            childdata['grand_parent_id'] = grand_parent
            child = {}
            child = GetChildByParent(childdata['id'], website_id, childdata['parent_id'],warehouse_id)
            if child:
                childdata['child'] = child
            else:
                childdata['child'] = []
        
    return child_data  


def get_child_by_parent_id(parent_id, company_website_id, grand_parent): 
    cm_child = EngageboostCmsMenus.objects.filter(isdeleted='n', isblocked='n', company_website_id=company_website_id, parent_id= parent_id).all().exclude(page_id=None)
    child_data = CmsMenusNewSerializer(cm_child, context={'company_website_id':company_website_id},many=True)
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

    
class HomeCategoryBanner(APIView):
    permission_classes = []
    # def get(self, request, format=None):
    def post(self, request, format=None):
        website_id = request.POST.get('website_id')
        #applicable_for = request.POST.get('applicable_for')
        banner_type = request.POST.get('banner_type') 
        
        try:
            if website_id is None:
                raise Exception("Website id is required")
            # if applicable_for is None:
            # 	raise Exception("applicable for is required")
            if banner_type is None:
                raise Exception("banner type is required")
				
			
            banner_qs = EngageboostCategoryBanners.objects.filter(website_id=website_id,banner_type=banner_type,isdeleted='n', isblocked='n').all().order_by('order_no')
            bannerimage_data = CategoryBannersNewSerializer(banner_qs,many=True)
            bannerimage_data = bannerimage_data.data
            if bannerimage_data:
								
                data = {
                    "status":1,
                    "data":bannerimage_data
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
        return Response (data)


class GetWarehouseListByLatLong(APIView):
    permission_classes = []
    def post(self, request, format=None):
        requestdata = request.data

        latitude 	= requestdata["latitude"] 
        longitude 	= requestdata["longitude"] 
        website_id 	= requestdata["website_id"]
        store_type_id = None
        if 'storetype_id' not in requestdata or requestdata['storetype_id'] is None or requestdata['storetype_id'] == "":
            store_type_id = None
        else:
            store_type_id = requestdata['storetype_id']
        # lang_code 	= request.POST.get("lang_code")

        try:
            if latitude is None:
                raise Exception("latitude is required") 
            if longitude is None :
                raise Exception("longitude is required") 
            if website_id is None:
                raise Exception("website_id is required")
            if store_type_id is None:
                raise Exception("storetype_id is required")
            # if lang_code is None:
            #     raise Exception("lang_code is required")

            radlat      = Radians(float(latitude))
            radlong     = Radians(float(longitude))
            radflat     = Radians(Cast(F('latitude'), FloatField()))
            radflong    = Radians(Cast(F('longitude'), FloatField()))
            warehouse_list = []
            Expression = 111.045 * Degrees(Acos(Cos(radlat) * Cos(radflat) * Cos(radflong - radlong) + Sin(radlat) * Sin(radflat)))

            if store_type_id is None:
                rs_objWarehouse = EngageboostWarehouseMasters.objects.annotate(distance=Expression).filter(website_id=website_id, isblocked='n', isdeleted='n').exclude(latitude__isnull=True,longitude__isnull=True).order_by('distance')
            else:
                get_warehouse_ids = []


                #-----Binayak Start 25-11-2020-----#
                if type(store_type_id) == list:
                    get_warehouse_ids = EngageboostStoreType.objects.filter(type_id__in=store_type_id,isdeleted='n',isblocked='n').values_list("warehouse_id",flat=True)
                else:
                    get_warehouse_ids = EngageboostStoreType.objects.filter(type_id=store_type_id, isdeleted='n',
                                                                            isblocked='n').values_list("warehouse_id",
                                                                                                       flat=True)

                # get_warehouse_ids = EngageboostStoreType.objects.filter(type_id=store_type_id,isdeleted='n',isblocked='n').values_list("warehouse_id",flat=True)
                if get_warehouse_ids:
                    rs_objWarehouse = EngageboostWarehouseMasters.objects.annotate(distance=Expression).filter(website_id=website_id, isblocked='n', isdeleted='n', id__in=get_warehouse_ids).exclude(latitude__isnull=True,longitude__isnull=True).order_by('distance')
                else:
                    rs_objWarehouse = []

            # if store_type_id == 0:
            #     rs_objWarehouse = EngageboostWarehouseMasters.objects.annotate(distance=Expression).filter(
            #         website_id=website_id, isblocked='n', isdeleted='n').exclude(latitude__isnull=True,
            #                                                                      longitude__isnull=True).order_by(
            #         'distance')
            # else:
            #     rs_objWarehouse = EngageboostWarehouseMasters.objects.annotate(distance=Expression).filter(website_id=website_id, isblocked='n', isdeleted='n', engagebooststoretype__type_id=store_type_id, engagebooststoretype__type__isdeleted='n', engagebooststoretype__type__isblocked='n').exclude(latitude__isnull=True,longitude__isnull=True).order_by('distance')
            qs_currency = EngageboostGlobalsettingCurrencies.objects.filter(isblocked='n',isdeleted='n').first()
            currencyvalue = GlobalsettingCurrenciesSerializer(qs_currency).data
            if qs_currency:
                currency1 =currencyvalue['currency_data']
                currency_id=currency1['id']
                currency_name = currency1['currency']
                currency={"currency_id":currency_id,"currency_name":currency_name}
            else:
                currency={"currency_id":'',"currency_name":''}

            Category_data = []
            str_status = ""
            if len(rs_objWarehouse)>0:
                # objWarehouse = objWarehouse.first()
                for objWarehouse in rs_objWarehouse:
                    warehouse_obj = {}
                    if objWarehouse.max_distance_sales:
                        if objWarehouse.distance <= objWarehouse.max_distance_sales:
                            # objWarehouse_Categorylst = EngageboostCategoryWarehouse.objects.filter(warehouse_id=objWarehouse.id).values_list("category_id",flat=True).iterator()
                            warehouse_obj.update({"currency":currency})
                            warehouse_obj.update({
                                "id":objWarehouse.id,
                                "website_id":objWarehouse.website_id,
                                "name":objWarehouse.name,
                                "code":objWarehouse.code,
                                "address":objWarehouse.address,
                                "country_id":objWarehouse.country_id,
                                "state_id":objWarehouse.state_id,
                                "state_name":objWarehouse.state_name,
                                "city":objWarehouse.city,
                                "zipcode":objWarehouse.zipcode,
                                "phone":objWarehouse.phone,
                                "email":objWarehouse.email,
                                "channel_id":objWarehouse.channel_id,
                                "latitude":objWarehouse.latitude,
                                "longitude":objWarehouse.longitude,
                                "max_distance_sales":objWarehouse.max_distance_sales,
                                "distance":objWarehouse.distance,
                                "warehouse_logo":objWarehouse.warehouse_logo,
                            })
                            warehouse_list.append(warehouse_obj)
                if warehouse_list:
                    str_status = status.HTTP_200_OK
                    data = {
                        "status":str_status,
                        "data":warehouse_list
                    }
                else:
                    str_status = status.HTTP_204_NO_CONTENT
                    data = {
                        "status":str_status,
                        "data":warehouse_list
                    }  
            else:
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                    "status":str_status,
                    "data":[]
                }            
        except Exception as error:
            str_status = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
            
        return Response (data, str_status)

#----Test----#
class GetWarehouseListByLatLongTest(APIView):
    permission_classes = []

    def post(self, request, format=None):
        requestdata = request.data

        latitude = requestdata["latitude"]
        longitude = requestdata["longitude"]
        website_id = requestdata["website_id"]
        store_type_id = None
        if 'storetype_id' not in requestdata or requestdata['storetype_id'] is None or requestdata[
            'storetype_id'] == "":
            store_type_id = None
        else:
            store_type_id = requestdata['storetype_id']
        # lang_code 	= request.POST.get("lang_code")

        try:
            if latitude is None:
                raise Exception("latitude is required")
            if longitude is None:
                raise Exception("longitude is required")
            if website_id is None:
                raise Exception("website_id is required")
            if store_type_id is None:
                raise Exception("storetype_id is required")
            #  if lang_code is None:
            #     raise Exception("lang_code is required")

            radlat = Radians(float(latitude))
            radlong = Radians(float(longitude))
            radflat = Radians(Cast(F('latitude'), FloatField()))
            radflong = Radians(Cast(F('longitude'), FloatField()))
            warehouse_list = []
            Expression = 111.045 * Degrees(
                Acos(Cos(radlat) * Cos(radflat) * Cos(radflong - radlong) + Sin(radlat) * Sin(radflat)))
            # -----Binayak Start------#
            # print(type(store_type_id) == list)
            if store_type_id is None:
                rs_objWarehouse = EngageboostWarehouseMasters.objects.annotate(distance=Expression).filter(
                    website_id=website_id, isblocked='n', isdeleted='n').exclude(latitude__isnull=True,
                                                                                 longitude__isnull=True).order_by(
                    'distance')
            else:
                get_warehouse_ids = []
                # -----Binayak Start 25-11-2020-----#
                if type(store_type_id) == list:
                    get_warehouse_ids = EngageboostStoreType.objects.filter(type_id__in=store_type_id, isdeleted='n',
                                                                            isblocked='n').values_list("warehouse_id",
                                                                                                       flat=True)
                else:
                    get_warehouse_ids = EngageboostStoreType.objects.filter(type_id=store_type_id, isdeleted='n',
                                                                            isblocked='n').values_list("warehouse_id",
                                                                                                       flat=True)
                # -----Binayak End 25-11-2020-----#
                if get_warehouse_ids:
                    rs_objWarehouse = EngageboostWarehouseMasters.objects.annotate(distance=Expression).filter(
                        website_id=website_id, isblocked='n', isdeleted='n', id__in=get_warehouse_ids).exclude(
                        latitude__isnull=True, longitude__isnull=True).order_by('distance')
                else:
                    # ------Binayak Start 10-10-2020-----#
                    rs_objWarehouse = []
                    # ------Binayak End 10-10-2020-----#

            # if store_type_id == 0:
            #     rs_objWarehouse = EngageboostWarehouseMasters.objects.annotate(distance=Expression).filter(website_id=website_id, isblocked='n', isdeleted='n').exclude(latitude__isnull=True,longitude__isnull=True).order_by('distance')
            # else:
            #     rs_objWarehouse = EngageboostWarehouseMasters.objects.annotate(distance=Expression).filter(website_id=website_id, isblocked='n', isdeleted='n', engagebooststoretype__type_id=store_type_id, engagebooststoretype__type__isdeleted='n', engagebooststoretype__type__isblocked='n').exclude(latitude__isnull=True,longitude__isnull=True).order_by('distance')
            # -----Binayak End------#
            qs_currency = EngageboostGlobalsettingCurrencies.objects.filter(isblocked='n', isdeleted='n').first()
            currencyvalue = GlobalsettingCurrenciesSerializer(qs_currency).data
            if qs_currency:
                currency1 = currencyvalue['currency_data']
                currency_id = currency1['id']
                currency_name = currency1['currency']
                currency = {"currency_id": currency_id, "currency_name": currency_name}
            else:
                currency = {"currency_id": '', "currency_name": ''}

            Category_data = []
            str_status = ""

            tz_NY = pytz.timezone('Asia/Dubai')
            datetime_NY = datetime.datetime.now(tz_NY).time()
            # print('datetime_NY======>', datetime_NY)
            # print('now======>', datetime.datetime.now())
            weekday = datetime.datetime.now().weekday() + 2
            if weekday == 8:
                weekday = 1

            if len(rs_objWarehouse) > 0:
                # objWarehouse = objWarehouse.first()
                for objWarehouse in rs_objWarehouse:
                    warehouse_obj = {}
                    if objWarehouse.max_distance_sales:
                        if objWarehouse.distance <= objWarehouse.max_distance_sales:
                            store_timing = EngageboostDeliverySlot.objects.filter(warehouse_id=objWarehouse.id,
                                                                                  isdeleted='n',
                                                                                  day_id=weekday,
                                                                                  based_on='SameDay').first()

                            store_open = False
                            nextday = False
                            store_time_display = False
                            open_time = close_time = datetime.datetime.strptime('00:00', "%H:%M").time()
                            if store_timing:
                                # print('store_timing====>', store_timing)
                                if store_timing.start_time != None and store_timing.start_time != '':
                                    # open_time = store_timing.start_time.strftime("%I:%M%p")
                                    open_time = store_timing.start_time
                                if store_timing.end_time != None and store_timing.end_time != '':
                                    # close_time = store_timing.end_time.strftime("%I:%M%p")
                                    close_time = store_timing.end_time

                                open_time = datetime.datetime.strptime(open_time, "%H:%M").time()
                                close_time = datetime.datetime.strptime(close_time, "%H:%M").time()

                                if open_time < datetime_NY and close_time > datetime_NY:
                                    store_open = True
                                elif store_timing.start_time == store_timing.end_time:
                                    store_open = True
                                else:
                                    store_open = False

                                # delveryObj = EngageboostDeliverySlot.objects.filter(warehouse_id=objWarehouse.id, isdeleted='n',day_id=weekday+1).first()

                                store_time_display = True

                            delveryObj = EngageboostDeliverySlot.objects.filter(warehouse_id=objWarehouse.id,
                                                                                isdeleted='n', day_id=weekday,
                                                                                based_on='NextDay').first()
                            if delveryObj:
                                # print(delveryObj.based_on)
                                # if delveryObj.based_on=='NextDay':
                                nextday = True

                            formatted_open_time = custom_time_formatting(open_time)
                            formatted_close_time = custom_time_formatting(close_time)

                            # objWarehouse_Categorylst = EngageboostCategoryWarehouse.objects.filter(warehouse_id=objWarehouse.id).values_list("category_id",flat=True).iterator()
                            warehouse_obj.update({"currency": currency})
                            warehouse_obj.update({
                                "id": objWarehouse.id,
                                "website_id": objWarehouse.website_id,
                                "name": objWarehouse.name,
                                "code": objWarehouse.code,
                                "address": objWarehouse.address,
                                "country_id": objWarehouse.country_id,
                                "state_id": objWarehouse.state_id,
                                "state_name": objWarehouse.state_name,
                                "city": objWarehouse.city,
                                "zipcode": objWarehouse.zipcode,
                                "phone": objWarehouse.phone,
                                "email": objWarehouse.email,
                                "channel_id": objWarehouse.channel_id,
                                "latitude": objWarehouse.latitude,
                                "longitude": objWarehouse.longitude,
                                "max_distance_sales": objWarehouse.max_distance_sales,
                                "distance": objWarehouse.distance,
                                "warehouse_logo": objWarehouse.warehouse_logo,
                                "store_open": store_open,
                                "open_time": formatted_open_time,
                                "close_time": formatted_close_time,
                                "store_time_display": store_time_display,
                                "nextday": nextday
                            })
                            warehouse_list.append(warehouse_obj)
                if warehouse_list:
                    str_status = status.HTTP_200_OK
                    data = {
                        "status": str_status,
                        "data": warehouse_list
                    }
                else:
                    str_status = status.HTTP_204_NO_CONTENT
                    data = {
                        "status": str_status,
                        "data": warehouse_list
                    }
            else:
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                    "status": str_status,
                    "data": []
                }
        except Exception as error:
            str_status = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line,
                    "error_message": str(error), "message": str(error)}

        return Response(data, str_status)


def custom_time_formatting(time_string):
    time_string = time_string.strftime("%I:%M %p")
    time_array_pos_1 = time_string.split(':')

    time_array_pos_2 = time_array_pos_1[1].split(' ')

    hour = int(time_array_pos_1[0])
    minutes = ''
    format = time_array_pos_2[1]
    if int(time_array_pos_2[0]) > 0:
        minutes = time_array_pos_2[0]

        new_format = ":" + str(minutes) + " " + str(format)
    else:
        new_format = " " + str(format)

    formatted_time = str(hour) + str(new_format)
    return formatted_time
#----Test----#

class GetMenuListApp(APIView):
    permission_classes = []

    def post(self, request, format=None):
        # latitude 	= request.POST.get("latitude")
        # longitude 	= request.POST.get("longitude")
        website_id = request.POST.get("website_id")
        lang_code = request.POST.get("lang_code")
        warehouse_id = request.POST.get("warehouse_id")

        try:
            # if latitude is None:
            #     raise Exception("latitude is required")
            # if longitude is None :
            #     raise Exception("longitude is required")
            if website_id is None:
                raise Exception("website_id is required")
            if lang_code is None:
                raise Exception("lang_code is required")
            if warehouse_id is None:
                raise Exception("warehouse id is required")

            # radlat      = Radians(float(latitude))
            # radlong     = Radians(float(longitude))
            # radflat     = Radians(Cast(F('latitude'), FloatField()))
            # radflong    = Radians(Cast(F('longitude'), FloatField()))

            # Expression = 111.045 * Degrees(Acos(Cos(radlat) * Cos(radflat) * Cos(radflong - radlong) + Sin(radlat) * Sin(radflat)))
            # objWarehouse = EngageboostWarehouseMasters.objects.annotate(distance=Expression).filter(website_id=website_id).exclude(latitude__isnull=True,longitude__isnull=True, max_distance_sales__isnull=True, max_distance_sales__gt=0).order_by('distance')
            Category_data = []
            # if len(objWarehouse)>0:
            #     objWarehouse = objWarehouse.first()
            #     if objWarehouse.max_distance_sales:
            #         if objWarehouse.distance <= objWarehouse.max_distance_sales:
            objWarehouse_Categorylst = EngageboostCategoryWarehouse.objects.filter(warehouse_id=warehouse_id,
                                                                                   product_count__gt=0, isblocked='n',
                                                                                   isdeleted='n').values_list(
                "category_id", flat=True)
            objCategorymaster = EngageboostCategoryMasters.objects.filter(id__in=objWarehouse_Categorylst, parent_id=0,
                                                                          isblocked='n', isdeleted='n').all().order_by(
                'display_order').iterator()
            Category_data = CategoriesNewSerializer(objCategorymaster, many=True).data

            categoryData = []
            # categoryData2 = []
            if Category_data:
                i = 0
                for categorydata in Category_data:
                    child = {}
                    child = GetChildByParent(categorydata['id'], website_id, categorydata['parent_id'], warehouse_id)
                    if child:
                        categorydata['child'] = child
                    else:
                        categorydata['child'] = []
                    if child:
                        # categoryData.append(categorydata)
                        # categoryData2.append({"name": "All", "page_title": "All"})
                        categoryData.append(categorydata)
                        # print('child====>', categoryData2[0]['child'])
                        intermediate_child = categoryData[i]['child']
                        categoryData[i]['child'] = []
                        categoryData[i]['child'].append({"id": 0,
                                                          "parent_id": 0,
                                                          "display_order": "null",
                                                          "name": "All",
                                                          "description": "null",
                                                          "image": "",
                                                          "thumb_image": "",
                                                          "banner_image": "",
                                                          "page_title": "All",
                                                          "meta_description": "null",
                                                          "meta_keywords": "null",
                                                          "category_url": "",
                                                          "slug": "",
                                                          "type": "null",
                                                          "website_id": 1,
                                                          "is_ebay_store_category": "N",
                                                          "customer_group_id": "null",
                                                          "display_mobile_app": "Y",
                                                          "show_navigation": "Y",
                                                          "product_count": 0,
                                                          "lang_data": [],
                                                          "grand_parent_id": 0,
                                                          "child": []})
                        categoryData[i]['child'].extend(intermediate_child)
                        i += 1
                        # print('child====>', categoryData2[0]['child'])
                        # return
            ######cms header#############
            cmsmenu_qs = EngageboostCmsMenus.objects.filter(isblocked='n', isdeleted='n', parent_id=0, flag=0,
                                                            company_website_id=website_id).all().exclude(
                page_id=None)  # flag=0 for header
            menu_data = CmsMenusNewSerializer(cmsmenu_qs, context={'website_id': website_id}, many=True)
            menu_data = menu_data.data
            if menu_data:
                for data in menu_data:
                    child = {}
                    child = get_child_by_parent_id(data['id'], website_id, data['parent_id'])
                    if child:
                        data['child'] = child
                    else:
                        data['child'] = []
            data = {
                "status": 1,
                "menu_bar": categoryData,
                # "menu_bar_new": categoryData2,
                "cms_menu": menu_data
            }
            return Response(data, status.HTTP_200_OK)
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),
                    "message": str(error)}
            # return JSONResponse(errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(data, status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)