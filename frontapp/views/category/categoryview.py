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
from rest_framework import status

from django.http import JsonResponse
from django.db.models import F, Func, FloatField
from django.db.models.functions import Cast

from webservices.models import *
from frontapp.frontapp_serializers import *

import json
import base64
import sys,os
import traceback
import datetime


class ParentCategoryListView(APIView):
    
    permission_classes = []
    # def get(self, request, format=None):
    def post(self, request, format=None):
        website_id = request.META.get('HTTP_WID')
        if website_id:
            pass
        else:
            website_id = 1
           
        rs_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, parent_id=0).all(). order_by('display_order')
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
        return Response (data)


class ShopByCategory(APIView):
    permission_classes = []
    def get(self, request, format=None):
        website_id  = request.META.get('HTTP_WID')
        data        = {"status" : 0,"msg" : "something went wrong"}
        try:
            if website_id is None:
                raise Exception("Website id is required") 

            parent_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id,parent_id=0).values_list('id', flat=True).order_by('display_order')
            sub_category    = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id,parent_id__in=parent_category).all().order_by('-display_order')
            # print(sub_category.query)
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

        return Response(data)

class ShopByCategoryByCatId_old(APIView):
    permission_classes = []
    def post(self, request, format=None):
        website_id = request.POST.get('website_id')
        warehouse_id = request.POST.get('warehouse_id')
        #category_ids = request.POST.getlist('category_ids[]')
        try:
            if website_id is None:
                raise Exception("Website id is required")
            parent_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id).all().order_by('display_order')
            if warehouse_id:
                category_warehouse_ids = EngageboostCategoryWarehouse.objects.filter(warehouse_id=warehouse_id, product_count__gt=0).values_list('category_id', flat=True)
                parent_category = parent_category.filter(parent_id__in=category_warehouse_ids)

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

        return Response (data)

class ShopByCategoryByCatId_xx(APIView):
    permission_classes = []
    def post(self, request, format=None):
        website_id = request.POST.get('website_id')
        warehouse_id = request.POST.get('warehouse_id')
        #category_ids = request.POST.getlist('category_ids[]')
        try:
            if website_id is None:
                raise Exception("Website id is required")
            new_list = []
            parent_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id).all().order_by('display_order')
            new_list = parent_category
            #-----Binayak Start----#
            child_ids = []
            cate_wh_ids = []
            if warehouse_id:
                category_warehouse_ids = EngageboostCategoryWarehouse.objects.filter(warehouse_id=warehouse_id, product_count__gt=0).values_list('category_id', flat=True)
                parent_category = parent_category.filter(parent_id__in=category_warehouse_ids)
                child_ids = parent_category.values_list('id', flat = True)

                if child_ids:
                    cate_wh_ids = EngageboostCategoryWarehouse.objects.filter(warehouse_id=warehouse_id, product_count__gt=0, category_id__in = child_ids ).values_list('category_id', flat=True)
                    
            #-----Binayak End------#

            # cat_list = list(parent_category)
            # print('cat_list=======', cat_list)
            if cate_wh_ids:
                new_list = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id).all().order_by('display_order')
                new_list = new_list.filter(id__in = cate_wh_ids).values_list('parent_id', flat=True)
            
            new_parent_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id).all().order_by('display_order')
            new_parent_category = new_parent_category.filter(parent_id__in=new_list)

            # print("parent_category=========", parent_category.query)
            #print(parent_category.query)
            category_data = CategoryMastersSerializer(new_parent_category, many=True)
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

        return Response (data)

class ShopByCategoryByCatId(APIView):
    permission_classes = []
    def post(self, request, format=None):
        website_id 	= request.POST.get("website_id")
        warehouse_id = request.POST.get("warehouse_id")

        try:
            if website_id is None:
                raise Exception("website_id is required")
            if warehouse_id is None:
                raise Exception("warehouse id is required")
            Category_data = []
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

          
            parent_ids = []
            for catdata in categoryData:
                parent_ids.append(catdata['id'])
            
            new_parent_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, id__in =parent_ids).all().order_by('display_order')

            category_data = CategoryMastersSerializer(new_parent_category, many=True)
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

            return Response(data, status.HTTP_200_OK)
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
            # return JSONResponse(errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(data, status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)


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