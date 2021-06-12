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

from frontapp.views.product import discount
from django.db.models import Avg, Max, Min, Sum, Count

import json
import base64
import sys,os
import traceback
import datetime
from frontapp.views.sitecommon import common_functions
from webservices.views.emailcomponent import emailcomponent
import re
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

class HomeCms(APIView):
    permission_classes = []
    def post(self, request, format=None):
        requestdata         = request.data
        company_website_id  = requestdata['company_website_id']
        lang                = requestdata['lang']
        template_id         = requestdata['template_id']
        page_id             = requestdata['page_id']
        start_limit         = requestdata['start_limit']
        end_limit           = requestdata['end_limit']
        warehouse_id        = requestdata['warehouse_id']       

        try:
            
            if company_website_id=='':
                raise Exception("company website id is required") 
            if lang=='':
                raise Exception("lang is required") 
            if template_id=='':
                raise Exception("template id is required")  
            if page_id=='':
                raise Exception("page id is required")
            if start_limit=='':
                raise Exception("start limit is required")
            if end_limit=='':
                raise Exception("end limit is required")
            if warehouse_id=='':
                raise Exception("warehouse id is required")  

            return_data ={}
            pages=EngageboostCmsPageSettings.objects.filter(company_website_id=company_website_id,lang=lang,temp_id=template_id,page_id=page_id).all()
            if end_limit == 0 and start_limit == 0:
                requestdata['no_of_page'] = 1
                requestdata['next_start_index'] = 0 
                requestdata['prev_start_index'] = 0  
            else:
                requestdata['no_of_page'] = int(len(pages) / end_limit) if(int(len(pages) % end_limit) == 0) else int(len(pages) / end_limit) + 1
                requestdata['next_start_index'] = start_limit if int(start_limit + end_limit) >= len(pages) else int(start_limit + end_limit)
                requestdata['prev_start_index'] = start_limit if int(start_limit - end_limit) < 0 else int(start_limit - end_limit)
                requestdata['total_number_row'] = len(pages)

            if end_limit != 0:
                pages = pages.order_by('id')[int(start_limit):int(start_limit) + int(end_limit)]
            
            pagecount = pages.count()
            #print(pagecount)
            serializer_cms = CmsPageSettingsSerializer(pages,many=True)
            serializer_cms = serializer_cms.data
            if serializer_cms:
                widgets_data            = []
                carousel                = []
                parent_category_list    = [] 
                best_sell_product       = []
                deals_product           = []
                product_by_category     = []
                product_by_categoryid   = []
                data                    = []
                banner_id               = []
                brand_ids               = []
                promotion_bannerid      = []
                category_ids            = []
                categorylist            = []
                selling_product         = []
                banner=[]
                deals_ofthe_day =[]
                category_banner =[]
                shop_by_brand =[]
                #str_status = ""
                for serializercms in serializer_cms:
                    widgets_id = serializercms['widgets']
                    applicable_for='mobile'
                    banner = Banner_List_For_App(company_website_id,applicable_for)
                    return_data.update({"carousel":banner})
                    # if(serializercms['widgets']== 24): 
                    #   propertyvalue = serializercms['property_value']
                    #   json_data = json.loads(propertyvalue)
                    #   carousel.append(json_data['insertables'][0]['properties'])
                    #   return_data.update({"carousel":carousel})
                    
                    if(serializercms['widgets']== 19):
                        propertyvalue = serializercms['property_value']
                        json_data = json.loads(propertyvalue)
                        data =json_data['insertables'][0]['properties']
                        # if data:
                        #   data.pop(0)
                        #   for datavalue in data:
                        #       value_id = datavalue['value']
                        #       category_ids.append(value_id)
                        #category_ids=[78,175,181,179,180,191,170,174]
                        # categorylist = Shop_By_Category_ByCatId(company_website_id)
                        categorylist = Shop_By_Category_ByCatId_new(company_website_id, warehouse_id)
                    # serializercms['categorylist']= categorylist
                        return_data.update({"Shop_By_Category":categorylist})
                    if(serializercms['widgets']== 26):
                        propertyvalue = serializercms['property_value']
                        selling_product = Best_Selling_Product(company_website_id,warehouse_id)
                        serializercms['selling_product']= selling_product
                        return_data.update({"best_sell_product":selling_product})
                    if(serializercms['widgets']== 25):
                        propertyvalue = serializercms['property_value']
                        deals_ofthe_day = Deals_Of_The_Day(company_website_id,warehouse_id)
                        return_data.update({"deals_of_the_day":deals_ofthe_day})
                    if(serializercms['widgets']== 18):
                        propertyvalue = serializercms['property_value']
                        json_data = json.loads(propertyvalue)
                        data =json_data['insertables'][0]['properties']
                        # if data:
                        #   data.pop(0)
                        #   for datavalue in data:
                        #       value_id = datavalue['value']
                        #       brand_ids.append(value_id)
                        shop_by_brand = Brand_List_By_BrandId(company_website_id)
                        return_data.update({"shop_by_brand":shop_by_brand})

                    if(serializercms['widgets']== 29):
                        propertyvalue = serializercms['property_value']
                        json_data = json.loads(propertyvalue)
                        data =json_data['insertables'][0]['properties']
                        # if data:
                        #   data.pop(0)
                        #   for datavalue in data:
                        #       value_id = datavalue['value']
                        #       banner_id.append(value_id)
                        applicable_for ='category'
                        banner_type = 'C'
                        category_banner = Banner_List(company_website_id,applicable_for,banner_type, warehouse_id)
                        return_data.update({"category_banner":category_banner})
                        
                    if(serializercms['widgets']== 20):
                        propertyvalue = serializercms['property_value']
                        json_data = json.loads(propertyvalue)
                        product_by_category=json_data['insertables'][0]['properties'][0]['value']
                        category_value=json_data['insertables'][0]['properties'][1]['value']
                        product_by_categoryid = Category_Product_ListView(category_value,warehouse_id,company_website_id)
                        product_by_categoryid[0].update({"label_value":product_by_category})
                        # for cat_details in product_by_categoryid:
                        #   cat_details.update({"label_value":product_by_category})
                        return_data.update({"product_by_categoryid":product_by_categoryid})
                    if(serializercms['widgets']== 30):
                        propertyvalue = serializercms['property_value']
                        json_data = json.loads(propertyvalue)
                        data =json_data['insertables'][0]['properties']
                        if data:
                            data.pop(0)
                            for datavalue in data:
                                value_id = datavalue['value']
                                promotion_bannerid.append(value_id)
                        promotional_banner = Promotional_Banner_ById(company_website_id,promotion_bannerid)
                        return_data.update({"promotional_banner":promotional_banner})

                return_data.update({"carousel":banner, "Shop_By_Category":categorylist, "deals_of_the_day":deals_ofthe_day,"category_banner":category_banner, "best_sell_product":selling_product, "product_by_categoryid":product_by_categoryid, "shop_by_brand":shop_by_brand})
                return_data.update({"total_widgets":pagecount})
                str_status = status.HTTP_200_OK
                data ={
                    "status":str_status,
                    "data":return_data
                }
            else:
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                    "status":str_status,
                    "msg":"No data found.",
                    "data":[]
                }
        except Exception as error:
            
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data, str_status)

class BestSellingProduct(APIView):
    permission_classes = []
    def post(self, request, format=None):
        warehouse_id = request.POST.get('warehouse_id') 
        website_id = request.POST.get('website_id')
        res_data = Best_Selling_Product(website_id, warehouse_id)

        if len(res_data)>0:
            data = {
                "status":1,
                "data":res_data
            }
        else:
            data = {
                "status":0,
                "data":[]
            }

        return Response(data)

def Best_Selling_Product(website_id,warehouse_id):
    product_list = []
    rs_order_product    = EngageboostOrderProducts.objects.filter(assign_wh = warehouse_id).values('product_id').annotate(tot_sale = Sum('quantity')).order_by('-tot_sale')[:20]
    if rs_order_product:
        for order_product in rs_order_product:
            product_list.append(order_product['product_id'])

    if product_list:
        selling_product     = EngageboostProducts.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, channel_price__warehouse_id=warehouse_id,channel_price__price__gt=0, id__in = product_list, product_stock__real_stock__gt=0, product_stock__warehouse=warehouse_id).distinct('channel_price__product_id').all()[:20]
    else:
        selling_product     = EngageboostProducts.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, channel_price__warehouse_id=warehouse_id,channel_price__price__gt=0, product_stock__real_stock__gt=0, product_stock__warehouse=warehouse_id).distinct('channel_price__product_id').all().order_by('channel_price__product_id','-numberof_sale')[:20]
    sellingproduct_data = ProductSerializer(selling_product, context={'warehouse_id': warehouse_id},many=True)
    sellingproduct_data = sellingproduct_data.data
    if sellingproduct_data:
        for crossproduct in sellingproduct_data:
            variant_product     = []
            crossrroductresult  = []
            cross_productArr    = []            
            #if crossproduct["channel_price"] and crossproduct["channel_price"]>0:
            if crossproduct["channel_price"]>0:
                crossproduct['default_price'] = crossproduct["channel_price"]

                request_data = {
                    'website_id': website_id,
                    'company_id': website_id,
                    'product_ids': crossproduct['id'],
                    'qtys': '1',
                    'prod_price': crossproduct['channel_price'],
                    'default_price': crossproduct['channel_price'],
                    'warehouse_id': warehouse_id
                }
                products_discount = discount.get_discount_detalils(request_data)    
                for productsdiscount in products_discount:
                    products_discount_data = {
                        "new_default_price": productsdiscount['new_default_price'],
                        "new_default_price_unit": productsdiscount['new_default_price_unit'],
                        "discount_price_unit": productsdiscount['discount_price_unit'],
                        "discount_price": productsdiscount['discount_price'],
                        "discount_amount": productsdiscount['discount_amount'],
                        "disc_type": productsdiscount['disc_type'],
                        "coupon": productsdiscount['coupon']
                    }
                crossproduct.update(products_discount_data)
            else:
                products_discount_data = {
                    "new_default_price": 0,
                    "new_default_price_unit": 0,
                    "discount_price_unit": 0,
                    "discount_price": 0,
                    "discount_amount": 0,
                    "disc_type": "",
                    "coupon": ""
                }
                crossproduct.update(products_discount_data)

            qs = EngageboostCossSellProducts.objects.filter(product_id=crossproduct['id']).all()            
            qs = EngageboostCossSellProducts.objects.filter(product_id=crossproduct['id']).all().iterator()

            if qs:
                for qsprod in qs:
                    cross_productArr.append(qsprod.cross_product_id)
            if len(cross_productArr)>0:
                qscrossprod = EngageboostProducts.objects.filter(id__in=cross_productArr,isdeleted='n', isblocked='n',website_id=website_id).all()
                if qscrossprod:
                    crossrroductresult = ProductSerializer(qscrossprod,context={'warehouse_id': warehouse_id},many=True).data
                    variant_product.append(crossrroductresult)
                    for crossbrand in crossrroductresult:
                        if crossbrand["channel_price"]>0:
                            crossbrand['default_price'] = crossbrand["channel_price"]
                        qs_brand = EngageboostBrandMasters.objects.filter(id=crossbrand['brand'], isblocked='n', isdeleted='n').first()
                        brand_data = BrandMastersSerializer(qs_brand)
                        crossbrand.update({'brand':brand_data.data})
            
            crossproduct.update({'variant_product':crossrroductresult})
            if crossproduct['brand'] is not None:
                brand_id_arr = str(crossproduct['brand']).split(",")
                brand_id_arr = list(filter(None, brand_id_arr))
                qs_brand = EngageboostBrandMasters.objects.filter(id__in=brand_id_arr, isblocked='n', isdeleted='n').first()
                brand_data = BrandMastersSerializer(qs_brand)
                crossproduct.update({'brand':brand_data.data})
    return sellingproduct_data

def Shop_By_Category(website_id):
    parent_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id,parent_id=0).values_list('id', flat=True)
    sub_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id,parent_id__in=parent_category).all().order_by('display_order')
    category_data = CategoryMastersSerializer(sub_category, many=True)
    category_data = category_data.data
    return category_data

def Shop_By_Category_ByCatId(website_id):
    parent_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id).all().order_by('display_order')
    category_data = CategoryMastersSerializer(parent_category, many=True)
    category_data = category_data.data
    return category_data

class DealsOfTheDay(APIView):
    permission_classes = []
    def post(self, request, format=None):
        warehouse_id = request.POST.get('warehouse_id') 
        website_id = request.POST.get('website_id')
        res_data = Deals_Of_The_Day(website_id, warehouse_id)
        if len(res_data)>0:
            data = {
                "status":1,
                "data":res_data
            }
        else:
            data = {
                "status":0,
                "data":[]
            }
        return Response(data)


def Deals_Of_The_Day(website_id,warehouse_id):
    warehouse_id = str(warehouse_id)
    now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
    deal_disc_master = EngageboostDiscountMasters.objects.filter(isdeleted='n', isblocked='n',website_id=website_id,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc,offer_type='Todays Offers').all().filter( Q(warehouse_id__startswith=warehouse_id+',') | Q(warehouse_id__endswith=','+warehouse_id) | Q(warehouse_id__contains=',{0},'.format(warehouse_id)) | Q(warehouse_id__exact=warehouse_id) ).values_list('id', flat=True)
    dis_master_condition = EngageboostDiscountMastersConditions.objects.filter(discount_master_id=deal_disc_master,isdeleted='n', isblocked='n')
    if dis_master_condition:
        for discnt in dis_master_condition:
            products_array=[]
            products = discnt.all_product_id
            if products:
                products_arr = products.split(',')
                if products_arr:
                    for provalue in products_arr:
                        products_array.append(int(provalue))
            productlist=[]
            cat_list = discnt.all_category_id
            if cat_list:
                category_arr = cat_list.split(',')
                product_data = EngageboostProductCategories.objects.filter(category_id__in=category_arr,isdeleted='n', isblocked='n').values_list('product_id', flat=True)
                if product_data:
                    for prodata in product_data:
                        productlist.append(prodata)
                
        joinedproduct = products_array + productlist
        totalproduct=list(set(joinedproduct))
        productresult = EngageboostProducts.objects.filter(isdeleted='n', isblocked='n', website_id=website_id,id__in=totalproduct,channel_price__warehouse_id=warehouse_id,channel_price__price__gt=0, product_stock__real_stock__gt=0, product_stock__warehouse=warehouse_id).distinct('channel_price__product_id').all()[:15]
        rs_product = ProductSerializer(productresult, context={'warehouse_id': warehouse_id},many=True)
        productresult_data = rs_product.data
        for crossproduct in productresult_data:
            variant_product =[]
            crossrroductresult =[]
            cross_productArr = []
            brand ={}
            if crossproduct["channel_price"]>0:
                crossproduct['default_price'] = crossproduct["channel_price"]

                request_data = {
                    'website_id': website_id,
                    'company_id': website_id,
                    'product_ids': crossproduct['id'],
                    'qtys': '1',
                    'prod_price': crossproduct['channel_price'],
                    'default_price': crossproduct['channel_price'],
                    'warehouse_id': warehouse_id
                }
                products_discount = discount.get_discount_detalils(request_data)    
                for productsdiscount in products_discount:
                    products_discount_data = {
                        "new_default_price": productsdiscount['new_default_price'],
                        "new_default_price_unit": productsdiscount['new_default_price_unit'],
                        "discount_price_unit": productsdiscount['discount_price_unit'],
                        "discount_price": productsdiscount['discount_price'],
                        "discount_amount": productsdiscount['discount_amount'],
                        "disc_type": productsdiscount['disc_type'],
                        "coupon": productsdiscount['coupon']
                    }
                crossproduct.update(products_discount_data)
            else:
                products_discount_data = {
                    "new_default_price": 0,
                    "new_default_price_unit": 0,
                    "discount_price_unit": 0,
                    "discount_price": 0,
                    "discount_amount": 0,
                    "disc_type": "",
                    "coupon": ""
                }
                crossproduct.update(products_discount_data)
            qs = EngageboostCossSellProducts.objects.filter(product_id=crossproduct['id']).all()
            
            if qs:
                for qsprod in qs:
                    cross_productArr.append(qsprod.cross_product_id)
                
            if len(cross_productArr)>0:
                qscrossprod = EngageboostProducts.objects.filter(id__in=cross_productArr,isdeleted='n', isblocked='n',website_id=website_id).all()
            
                if qscrossprod:
                    crossrroductresult = ProductSerializer(qscrossprod,context={'warehouse_id': warehouse_id}, many=True).data
                    variant_product.append(crossrroductresult)
                    for crossbrand in crossrroductresult:
                        if crossbrand["channel_price"]>0:
                            crossbrand['default_price'] = crossbrand["channel_price"]
                        qs_brand = EngageboostBrandMasters.objects.filter(id=crossbrand['brand'], isblocked='n', isdeleted='n').first()
                        brand_data = BrandMastersSerializer(qs_brand)
                        crossbrand.update({'brand':brand_data.data})

            crossproduct.update({'variant_product':crossrroductresult})
            qs_brand = EngageboostBrandMasters.objects.filter(id=crossproduct['brand'], isblocked='n', isdeleted='n').first()
            brand_data = BrandMastersSerializer(qs_brand)
            crossproduct.update({'brand':brand_data.data})  
    else:
        productresult_data = []
    
    return productresult_data

class CategoryProductListView(APIView):
    permission_classes = []
    def post(self, request, format=None):
        category_id = request.POST.get('category_id')
        warehouse_id = request.POST.get('warehouse_id') 
        website_id = request.POST.get('website_id')
        return_data = Category_Product_ListView(category_id,warehouse_id,website_id)
        if len(return_data)>0:  
            data = {
                "status":1,
                "data":return_data 
            }
        else: 
            data = {
                "status":0,
                "data":[]
            }
        return Response(data)


def Category_Product_ListView(category_id,warehouse_id,website_id):
    return_data=[]
    product_data = []
    # product_ids = EngageboostProductCategories.objects.filter(category_id=category_id, isblocked='n', isdeleted='n',).all().values_list('product_id', flat=True)
    rs_cat = EngageboostCategoryMasters.objects.filter(parent_id=category_id).values_list('id', flat=True)
    if rs_cat:
        product_ids = EngageboostProductCategories.objects.filter(category_id__in=rs_cat, isblocked='n', isdeleted='n',).all().values_list('product_id', flat=True)[:20]
    else:
        product_ids = EngageboostProductCategories.objects.filter(category_id=category_id, isblocked='n', isdeleted='n',).all().values_list('product_id', flat=True)[:20]
    
    if len(product_ids) > 0:
            product_dtl = EngageboostProducts.objects.filter(id__in=product_ids,isblocked='n', isdeleted='n',website_id=website_id,channel_price__warehouse_id=warehouse_id,channel_price__price__gt=0, product_stock__real_stock__gt=0, product_stock__warehouse=warehouse_id).distinct('channel_price__product_id').all()[:15]
            if product_dtl:
                product_data = ProductSerializer(product_dtl, context={'warehouse_id': warehouse_id}, many=True).data
                
                if product_data:
                    for productvalue in product_data:
                        variant_product =[]
                        cross_productArr=[]
                        qscrossprod =[]
                        if productvalue["channel_price"]>0:
                            productvalue['default_price'] = productvalue["channel_price"]

                            request_data = {
                                'website_id': website_id,
                                'company_id': website_id,
                                'product_ids': productvalue['id'],
                                'qtys': '1',
                                'prod_price': productvalue['channel_price'],
                                'default_price': productvalue['channel_price'],
                                'warehouse_id': warehouse_id
                            }
                            products_discount = discount.get_discount_detalils(request_data)    
                            for productsdiscount in products_discount:
                                products_discount_data = {
                                    "new_default_price": productsdiscount['new_default_price'],
                                    "new_default_price_unit": productsdiscount['new_default_price_unit'],
                                    "discount_price_unit": productsdiscount['discount_price_unit'],
                                    "discount_price": productsdiscount['discount_price'],
                                    "discount_amount": productsdiscount['discount_amount'],
                                    "disc_type": productsdiscount['disc_type'],
                                    "coupon": productsdiscount['coupon']
                                }
                            productvalue.update(products_discount_data)
                        else:
                            products_discount_data = {
                                "new_default_price": 0,
                                "new_default_price_unit": 0,
                                "discount_price_unit": 0,
                                "discount_price": 0,
                                "discount_amount": 0,
                                "disc_type": "",
                                "coupon": ""
                            }
                            productvalue.update(products_discount_data)

                        productvalue.update({'brand_name':''})
                        variant_data = EngageboostCossSellProducts.objects.filter(product_id=productvalue['id']).all()

                        if variant_data:
                            for qsprod in variant_data:
                                cross_productArr.append(qsprod.cross_product_id)
                                
                                
                        if len(cross_productArr)>0:

                            qscrossprod = EngageboostProducts.objects.filter(id__in=cross_productArr,isdeleted='n', isblocked='n',website_id=website_id).all()
                            if qscrossprod:
                                crossrroductresult = ProductSerializer(qscrossprod,context={'warehouse_id': warehouse_id},many=True).data
                                if crossrroductresult:
                                    for crossbrand in crossrroductresult:
                                        if crossbrand["channel_price"]>0:
                                            crossbrand['default_price'] = crossbrand["channel_price"]
                                        crossbrand.update({'brand_name':''})
                                        qs_brand = EngageboostBrandMasters.objects.filter(id=crossbrand['brand'], isblocked='n', isdeleted='n').first()
                                        if qs_brand:
                                            crossbrand.update({'brand_name':qs_brand.name})
                        if variant_data:
                            productvalue.update({'variant_product':crossrroductresult})
                        else:
                            productvalue.update({'variant_product':[]})
                                    
                        qs_brand = EngageboostBrandMasters.objects.filter(id=productvalue['brand'], isblocked='n', isdeleted='n').first()
                        if qs_brand:
                            productvalue.update({'brand_name':qs_brand.name})
                else:
                    product_data=[]
                
    return_data.append({'category_id':category_id, 'product':product_data})
    return return_data

class BrandListByBrandId(APIView):
    permission_classes = []
    def post(self, request, format=None):
        website_id = request.POST.get('website_id')
        #brand_ids = request.POST.getlist('brand_ids[]')
        brands_data = Brand_List_By_BrandId(website_id)
        if len(brands_data)>0:
            data ={
                'status':1,
                'brands':brands_data
            }
        else:
            data={
                "status":0,
                "data":[]
            }
        return Response(data)


def Brand_List_By_BrandId(website_id):
    serializer_data=EngageboostBrandMasters.objects.filter(isdeleted='n',isblocked='n',website_id=website_id).all()
    brands_data = BrandSerializer(serializer_data,many=True).data
    return brands_data    

class BannerList(APIView):
    permission_classes = []
    def post(self, request, format=None):
        website_id = request.POST.get('website_id')
        #category_banner_id = request.POST.getlist('category_banner_id[]')
        applicable_for = request.POST.get('applicable_for')
        banner_type = request.POST.get('banner_type') 
        warehouse_id = request.POST.get('warehouse_id') 
        
        rs_update = EngageboostCategoryBanners.objects.filter(isdeleted='n', isblocked='n').all()
        rs_warehouse = EngageboostWarehouseMasters.objects.filter(isdeleted = 'n').values_list("id", flat = True)
        rs_warehouse_data = list(rs_warehouse)
        rs_warehouse_data = ','.join(map(str, rs_warehouse_data))
        updata = {
            'warehouse_id':rs_warehouse_data
        }
        # if rs_update:
        #     for up_data in rs_update:
        #         if up_data.warehouse_id is not None:
        #             pass
        #         else:
        #             EngageboostCategoryBanners.objects.filter(id = up_data.id).update(**updata)
                
        #         if up_data.warehouse_id == "":
        #             pass
        #         else:
        #             EngageboostCategoryBanners.objects.filter(id = up_data.id).update(**updata)

        bannerimage_data = Banner_List(website_id,applicable_for,banner_type, warehouse_id)
        if len(bannerimage_data)>0:
                data = {
                    "status":1,
                    "data":bannerimage_data
                }
        else:
            data = {
                "status":0,
                "data":[]
            }
        return Response (data)

def Banner_List(website_id,applicable_for,banner_type,warehouse_id = None): 
    now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
    website_id = 1
    if warehouse_id is not None:
        rs_cat = EngageboostCategoryWarehouse.objects.filter(warehouse_id=warehouse_id, isdeleted='n', isblocked='n').values_list('category_id', flat=True)
        if rs_cat and banner_type=='C':
            banner_qs = EngageboostCategoryBanners.objects.filter(banner_type=banner_type,website_id=website_id,isdeleted='n', isblocked='n', warehouse_id__iregex=r"\y{0}\y".format(warehouse_id), category_id__in = rs_cat)
        else:
            banner_qs = EngageboostCategoryBanners.objects.filter(banner_type=banner_type,website_id=website_id,isdeleted='n', isblocked='n', warehouse_id__iregex=r"\y{0}\y".format(warehouse_id))
    else:
        banner_qs = EngageboostCategoryBanners.objects.filter(banner_type=banner_type,website_id=website_id,isdeleted='n', isblocked='n')

    bannerimage_qs = EngageboostCategoryBannersImages.objects.filter(category_banner_id__in=banner_qs,isdeleted='n', isblocked='n',applicable_for=applicable_for)
    if (banner_type=='H' and (applicable_for=='mobile' or applicable_for=='web')):

        bannerimage_qs = bannerimage_qs.filter(start_date__lte=now_utc,end_date__gte=now_utc,applicable_for=applicable_for)
    bannerimage_qs = bannerimage_qs.all()

    bannerimage_data = CategoryBannersImagesNewSerializer(bannerimage_qs,many=True).data
    #bannerimage_data = bannerimage_data.data
    if bannerimage_data:
        for bannerimage in bannerimage_data:
            if bannerimage["category_id"]:
                # qs_category = EngageboostCategoryMasters.objects.filter(id=bannerimage["category_id"],isdeleted='n', isblocked='n')
                qs_category = EngageboostCategoryMasters.objects.filter(id=bannerimage["category_id"])
                if qs_category.count()>0:
                    qs_category=qs_category.first()
                    category_name = qs_category.name
                    bannerimage['link']="listing/"+qs_category.slug
                else:
                    category_name=''    
            else:
                category_name=''
            bannerimage.update({'category_name':category_name})
    return bannerimage_data

class BannerListForHome(APIView):
    permission_classes = []
    def post(self, request, format=None):
        website_id = request.POST.get('website_id')
        applicable_for = request.POST.get('applicable_for')
        #warehouse_id = request.POST.get('warehouse_id') 
        
        bannerimage_data = Banner_List_For_App(website_id,applicable_for)
        if len(bannerimage_data)>0:
                data = {
                    "status":1,
                    "data":bannerimage_data
                }
        else:
            data = {
                "status":0,
                "data":[]
            }
        return Response (data)

def Banner_List_For_App(website_id,applicable_for):
    now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
    banner_qs = EngageboostCategoryBanners.objects.filter(banner_type='H',website_id=website_id,isdeleted='n', isblocked='n').all().values_list('id',flat=True)
    if (applicable_for=='mobile' or applicable_for=='web'):
        bannerimage_qs = EngageboostCategoryBannersImages.objects.filter(category_banner_id__in=banner_qs,start_date__lte=now_utc,end_date__gte=now_utc,isdeleted='n', isblocked='n',applicable_for=applicable_for)
        bannerimage_data = CategoryBannersImagesNewSerializer(bannerimage_qs,many=True).data
    return bannerimage_data


# @csrf_exempt
# class CategoryBannerForPromotion(APIView):
#   permission_classes = []
#   def post(self, request, format=None):
#       warehouse_id = request.POST.get('warehouse_id') 
#       website_id = request.POST.get('website_id')
#       res_data = Deals_Of_The_Day(website_id, warehouse_id)
#       if len(res_data)>0:
#           data = {
#               "status":1,
#               "data":res_data
#           }
#       else:
#           data = {
#               "status":0,
#               "data":[]
#           }
#       return Response(data)


@csrf_exempt
def PromotionalCategoryBannerList(request):
    website_id = request.META.get('HTTP_WID')
    try:
        if website_id is None:
            raise Exception("Website id is required") 
        company_website_id = 1
        template_id = 1
        lang ="en"
                
        banner_promotion = EngageboostCategoryBanners.objects.filter(isdeleted='n', isblocked='n', website_id=website_id,banner_type='C', category_banners_images__promotion_id__gt=0).all().order_by('order_no')
        banner_promotion_data = CategoryBannersForPromotionSerializer(banner_promotion, many=True)
        banner_promotion_data = banner_promotion_data.data
        str_status = ""
        if banner_promotion_data:
            str_status = status.HTTP_200_OK
            data = {
                "status":str_status,
                "data":banner_promotion_data
            }
        else:
            str_status = status.HTTP_204_NO_CONTENT
            data = {
                "status":str_status,
                "msg":"No data found.",
                "data":[]
            }
    except Exception as error:
            str_status = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
    return JsonResponse(data)

# class CategoryPromotionalBanner(APIView):
#   permission_classes = []
#   def get(self, request, format=None):
#       pages=EngageboostCmsPageSettings.objects.filter(company_website_id=company_website_id,lang=lang,temp_id=template_id,page_id=page_id).all()

class PromotionalBannerById(APIView):
    permission_classes = []
    def post(self, request, format=None):
        website_id = request.POST.get('website_id')
        banner_ids = request.POST.getlist('banner_ids[]')
        
        banner_promotion = Promotional_Banner_ById(website_id,banner_ids)
        if len(banner_promotion)>0:
                data = {
                    "status":1,
                    "data":banner_promotion
                }
        else:
            data = {
                "status":0,
                "data":[]
            }
        return Response (data)


def Promotional_Banner_ById(website_id,banner_ids):
    company_website_id = 1
    template_id = 1
    lang ="en"
            
    banner_promotion = EngageboostCategoryBanners.objects.filter(isdeleted='n', isblocked='n', website_id=website_id,id__in=banner_ids).all().order_by('order_no')      
    banner_promotion_data = CategoryBannersForPromotionSerializer(banner_promotion, many=True)
    banner_promotion_data = banner_promotion_data.data
    
    if banner_promotion_data:
        for discountdata in banner_promotion_data:
            product_count = 0
            if discountdata["banner_image"]["promotion_id"] is not None:
                rs_discount = EngageboostDiscountMastersConditions.objects.filter(discount_master_id=discountdata["banner_image"]["promotion_id"])
                if rs_discount:
                    for discnt in rs_discount:
                        products_array=[]
                        products = discnt.all_product_id
                        products_arr = products.split(',')
                        if products_arr:
                            for provalue in products_arr:
                                products_array.append(int(provalue))
                        
                        productlist=[]
                        cat_list = discnt.all_category_id
                        if cat_list:
                            category_arr = cat_list.split(',')
                            product_data = EngageboostProductCategories.objects.filter(category_id__in=category_arr,isdeleted='n', isblocked='n').values_list('product_id', flat=True)
                            product_data = product_data.distinct()
                            if product_data:
                                for prodata in product_data:
                                    productlist.append(prodata) 
                            #product_count = product_count + len(product_data)
                        joinedproduct = products_array + productlist
                        totalproduct=list(set(joinedproduct))
                        product_count = product_count + len(totalproduct)

            discountdata["product_count"] = product_count

    return banner_promotion_data


@csrf_exempt
def category_banner(request):
    if(request.method == "GET"):
        try:
            data={}
            slug = request.GET['slug']
            website_id = request.GET['website_id']
            #warehouse_id = request.GET['warehouse_id']
            strtype = request.GET['type']
            breadcrumb = []

            if(strtype=="category"):
                objCategory_cnt = EngageboostCategoryMasters.objects.filter(slug=slug,website_id=website_id,isdeleted='n',isblocked='n').count()
                if(objCategory_cnt!=0):
                    objCategory = EngageboostCategoryMasters.objects.filter(slug=slug,website_id=website_id,isdeleted='n',isblocked='n').first()
                    #objcat_warehouse_cnt = EngageboostCategoryWarehouse.objects.filter(category_id=objCategory.id, warehouse_id=warehouse_id).count()
                    #if(objcat_warehouse_cnt !=0):
                    objCategory_banner = EngageboostCategoryBanners.objects.filter(Q(banner_type='c')|Q(banner_type='C')).filter(category_id=objCategory.id,website_id=website_id,isdeleted='n',isblocked='n')
                    objCategory_data = CategoryBannersSerializer(objCategory_banner,many=True).data

                    objGlobalsettings = EngageboostGlobalSettings.objects.get(website_id=website_id)
                    data['status'] = 1
                    data['category_banner'] = objCategory_data
                    data['sort_by'] = []
                    data['category_id'] = objCategory.id
                    sortby_lst = ['New Arrivals','Price : High to Low','Price : Low to High']
                    for i in range(len(sortby_lst)):
                        sort_data = {}
                        sort_data['id'] = i+1
                        sort_data['name'] = sortby_lst[i]
                        data['sort_by'].append(sort_data)

                    data['breadcrumb'] = get_hierarchy(objCategory,website_id)
                    data['itemlisting_front'] = objGlobalsettings.itemlisting_front
                    # else:
                    #     data['status'] = 0
                    #     data['message'] = 'Category banner not found.'
                else:
                    data = {
                            "status": 0,
                            "message": "Category not found."
                        }
            elif strtype=="brand":
                rs_brand = EngageboostBrandMasters.objects.filter(slug=slug, isblocked='n', isdeleted='n').first()
                rs_product_list = EngageboostProducts.objects.filter(isblocked='n', isdeleted='n').filter( Q(brand__startswith=str(rs_brand.id)+',') | Q(brand__endswith=','+str(rs_brand.id)) | Q(brand__contains=',{0},'.format(str(rs_brand.id))) | Q(brand__exact=str(rs_brand.id)) ).count()
                sort_by = []
                sortby_lst = ['Popularity','New Arrivals','Price : High to Low','Price : Low to High']
                for i in range(len(sortby_lst)):
                    sort_data = {}
                    sort_data['id'] = i+1
                    sort_data['name'] = sortby_lst[i]
                    sort_by.append(sort_data)
                data = {
                    "status":1,
                    "category_banner":[],
                    "sort_by":sort_by,
                    "breadcrumb": [
                            {
                            "id": 0,
                            "name": "Home",
                            "url": "/"
                            },
                            {
                            "id": 164,
                            "name": rs_brand.name,
                            "url": "/listing/",
                            "slug": rs_brand.slug
                            }
                    ],
                        "itemlisting_front": rs_product_list
                }

            else:
                cnt_prod = EngageboostProducts.objects.filter(slug=slug,website_id=website_id,isdeleted='n',isblocked='n').count()
                if(cnt_prod!=0):
                    objproduct = EngageboostProducts.objects.get(slug=slug,website_id=website_id,isdeleted='n',isblocked='n')
                    objproduct_category = EngageboostProductCategories.objects.all().filter(product_id=objproduct.id)
                    if objproduct_category:
                        child_fetch_serializer = ProductCategoriesSerializer(
                            objproduct_category, many=True)
                        for child in child_fetch_serializer.data:
                            objCategory = EngageboostCategoryMasters.objects.get(id=child['category']['id'],website_id=website_id,isdeleted='n',isblocked='n')
                            breadcrumb = get_hierarchy(objCategory,website_id)
                        breadcrumb.append({'name':objproduct.name ,"url":"/product/" ,"slug":objproduct.slug})
                        data['status'] = 1
                        data['breadcrumb'] = breadcrumb
                    else:
                        data = {
                            "status": 0,
                            "message": "Product category not found"
                        }
                else:
                    data = {
                        "status": 0,
                        "message": "Product not found"
                    }
        except Exception as error:
            import sys, traceback
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status": 0, "api_status": traceback.format_exc(
            ), "error_line": line, "error_message": str(error), "message": str(error)}
        return JsonResponse(data)
    else:
        data = {
            "status": 0,
            "message": "invalid request"
        }
    return JsonResponse(data)

@csrf_exempt
def get_hierarchy(data,website_id):
    breadcrumb = []
    breadcrumb.append({'id':0,'name':"Home" ,"url":"/"})
    if(data.parent_id!=0):
        objCategorychild1 = EngageboostCategoryMasters.objects.get(id=data.parent_id,website_id=website_id,isdeleted='n',isblocked='n')
        if(objCategorychild1.parent_id!=0):
            objCategorychild2 = EngageboostCategoryMasters.objects.get(id=objCategorychild1.parent_id,website_id=website_id,isdeleted='n',isblocked='n')
            if(objCategorychild2.parent_id!=0):
                objCategorychild3 = EngageboostCategoryMasters.objects.get(id=objCategorychild2.parent_id,website_id=website_id,isdeleted='n',isblocked='n')
                if(objCategorychild3.parent_id!=0):
                    breadcrumb.append({'id':objCategorychild3.id,'name':objCategorychild3.name ,"url":"/listing/","slug":objCategorychild3.slug})
                    breadcrumb.append({'id':objCategorychild2.id,'name':objCategorychild2.name ,"url":"/listing/","slug":objCategorychild2.slug})
                    breadcrumb.append({'id':objCategorychild1.id,'name':objCategorychild1.name ,"url":"/listing/","slug":objCategorychild1.slug})
                    breadcrumb.append({'id':data.id,'name':data.name ,"url":"/listing/","slug":data.slug})
                else:
                    breadcrumb.append({'id':objCategorychild2.id,'name':objCategorychild2.name ,"url":"/listing/","slug":objCategorychild2.slug})
                    breadcrumb.append({'id':objCategorychild1.id,'name':objCategorychild1.name ,"url":"/listing/","slug":objCategorychild1.slug})
                    breadcrumb.append({'id':data.id,'name':data.name ,"url":"/listing/","slug":data.slug})
            else:
                breadcrumb.append({'id':objCategorychild2.id,'name':objCategorychild2.name ,"url":"/listing/","slug":objCategorychild2.slug})
                breadcrumb.append({'id':objCategorychild1.id,'name':objCategorychild1.name ,"url":"/listing/","slug":objCategorychild1.slug})
                breadcrumb.append({'id':data.id,'name':data.name ,"url":"/listing/","slug":data.slug})
        else:
            breadcrumb.append({'id':objCategorychild1.id,'name':objCategorychild1.name ,"url":"/listing/","slug":objCategorychild1.slug})
            breadcrumb.append({'id':data.id,'name':data.name ,"url":"/listing/","slug":data.slug})
    else:
        breadcrumb.append({'id':data.id,'name':data.name ,"url":"/listing/","slug":data.slug})

    return breadcrumb


class SubscribeNewsletter(APIView):
    permission_classes = []
    def post(self, request, format=None):
        requestdata =  JSONParser().parse(request)
        email       =  requestdata['email']
        website_id  =  requestdata['website_id']
        str_status = ""
        try:
            if email=='':
                raise Exception("email is required") 
            pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"   
            valid_email=re.match(pattern,email) 
            if valid_email==None:
                raise Exception("invalid email")           
                
            customer_qs = EngageboostCustomers.objects.filter(email=email,isdeleted = 'n',isblocked = 'n').exists()
            if customer_qs:
                customerdata_qs = EngageboostCustomers.objects.filter(email=email,isdeleted = 'n',isblocked = 'n').first()
                customer_id = customerdata_qs.auth_user_id
                #first_name = customerdata_qs.first_name
            else:
                customer_id=0
            contact_qs = EngageboostEmktContacts.objects.filter(email=email,isdeleted = 'n',isblocked = 'n').count()
            now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
            today = now_utc.strftime('%Y-%m-%d')
            contactslist_qs = EngageboostEmktContactlists.objects.filter(name='Default Customer',isdeleted = 'n',isblocked = 'n').first()
            if contactslist_qs:
                contact_list_id = contactslist_qs.id
            if contact_qs>0:
                contacts_update=EngageboostEmktContacts.objects.filter(email=email,customer_id = customer_id,isdeleted = 'n',isblocked = 'n').update(modified=today,email_format='HTML',activity_status='subscribed',confirmation_status = 'confirm',customer_id = customer_id,
                company_website_id = website_id,)
                str_status = status.HTTP_200_OK
                data = {
                    'status':str_status,
                    'message': 'you have already subscribed to our newsletter. ',
                }
            else:
                EmktContacts = EngageboostEmktContacts.objects.create(
                    
                  customer_id = customer_id,
                  company_website_id = website_id,
                  email = email,
                  email_format='HTML',
                  activity_status = 'subscribed',
                  confirmation_status = 'confirm',
                  contact_list_id = contact_list_id,
                  created = today,
                  modified = today,
                    
                )
                EmktContacts.save()
                contacts = EmktContactserializer(EmktContacts)
                contact_data = contacts.data
                website_qs=EngageboostCompanyWebsites.objects.filter(id=website_id,isblocked='n',isdeleted='n').first()
                website_name=website_qs.company_name
                #EMAIL TO User Subscribe to our newsletter STARTS HERE######################################################3
                buffer_data = common_functions.getAutoResponder("","","","","",26)
                if buffer_data and buffer_data["content"]:
                    autoResponderData  = buffer_data["content"]
                    if autoResponderData["email_type"] == 'H':
                        emailContent = autoResponderData["email_content"]
                    else:
                        emailContent = autoResponderData["email_content_text"]
                    emailContent = str(emailContent)

                    #emailContent = emailContent.replace('{@first_name}',first_name)
                    emailContent = emailContent.replace('{@website_name}',website_name)
                if email:
                    emailcomponent.OrderMail(email,autoResponderData["email_from"],autoResponderData["subject"],emailContent)
                #EMAIL EMAIL TO User end here########################################################################################
                #Notification to admin start here################################################################################################ 
                buffer_data = common_functions.getAutoResponder("","","","","",13)
                if buffer_data and buffer_data["content"]:
                    autoResponderData  = buffer_data["content"]
                    if autoResponderData["email_type"] == 'H':
                        emailContent = autoResponderData["email_content"]
                    else:
                        emailContent = autoResponderData["email_content_text"]
                    subject = autoResponderData["subject"]
                    subject = subject.replace('{@website_name}',website_name)
                    emailContent = str(emailContent)

                    #emailContent = emailContent.replace('{@first_name}',first_name)
                    emailContent = emailContent.replace('{@website_name}',website_name)
                    tomail=autoResponderData["email_from"]
                    emailcomponent.OrderMail(tomail,autoResponderData["email_from"],subject,emailContent)
                #Notification to admin end here################################################################################################
                str_status = status.HTTP_200_OK
                data = {
                    'status':str_status,
                    'message': 'you have successfully subscribed to our newsletter',
                    'data':contact_data
                }

        except Exception as error:
          trace_back = sys.exc_info()[2]
          line = trace_back.tb_lineno
          str_status = status.HTTP_417_EXPECTATION_FAILED
          data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response (data)

class UnsubscribeNewsletter(APIView):
    permission_classes = []
    def post(self, request, format=None):
        requestdata          =  JSONParser().parse(request)
        #contactId           =  requestdata['contactId']
        email                =  requestdata['email']
        notes                =  requestdata['notes']
        website_id           =  requestdata['website_id']
        #unsubscribed_option =  requestdata['unsubscribed_option']
        str_status = ""

        try:
            if email=='':
                raise Exception("email is required") 
            pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"   
            valid_email=re.match(pattern,email) 
            if valid_email==None:
                raise Exception("invalid email")        

            now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
            today = now_utc.strftime('%Y-%m-%d')
            contacts_update=EngageboostEmktContacts.objects.filter(email=email,isdeleted = 'n',isblocked = 'n').update(activity_status='unsubscribed',notes=notes,unsub_date=now_utc,company_website_id = website_id,modified=today)
            website_qs=EngageboostCompanyWebsites.objects.filter(id=website_id,isblocked='n',isdeleted='n').first()
            website_name=website_qs.company_name
            
            if contacts_update:
                #Notification mail to admin start here################################################################################################ 
                buffer_data = common_functions.getAutoResponder("","","","","",14)
                if buffer_data and buffer_data["content"]:
                    autoResponderData  = buffer_data["content"]
                    if autoResponderData["email_type"] == 'H':
                        emailContent = autoResponderData["email_content"]
                    else:
                        emailContent = autoResponderData["email_content_text"]
                    subject = autoResponderData["subject"]
                    subject = subject.replace('{@website_name}',website_name)
                    emailContent = str(emailContent)
                    #emailContent = emailContent.replace('{@first_name}',first_name)
                    emailContent = emailContent.replace('{@website_name}',website_name)
                    tomail=autoResponderData["email_from"]
                    emailcomponent.OrderMail(tomail,autoResponderData["email_from"],subject,emailContent)
                #Notification to admin end here################################################################################################ 
                str_status = status.HTTP_200_OK
                data = {
                    'status':str_status,
                    'message': 'You have successfully unsubscribed to our newsletter.',
                }
            else:
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                    'status':str_status,
                    'message': 'email does not exist ',
                }
                   
        except Exception as error:
          trace_back = sys.exc_info()[2]
          line = trace_back.tb_lineno
          str_status = status.HTTP_417_EXPECTATION_FAILED
          data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response (data)

class GetAppVersion(APIView):
    permission_classes = []
    def get(self, request, format=None):
        try:
            app_type = request.GET.get('type')
            appversion_qs=EngageboostAppVersionControl.objects.first()
            appversion_data = AppVersionControlSerializer(appversion_qs).data
            str_status = ""
            if appversion_data:
                str_status = status.HTTP_200_OK
                if app_type is None:
                    appversion_data.pop("picking_android")
                else:
                    if app_type == "picking":
                        pass
                    else:
                        appversion_data.pop("picking_android")
                data = {
                    "status":str_status,
                    "data":appversion_data
                }
            else:
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                    'status':str_status,
                    'message': 'data not found.',
                }
        except Exception as error:
          trace_back = sys.exc_info()[2]
          line = trace_back.tb_lineno
          str_status = status.HTTP_417_EXPECTATION_FAILED
          data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response (data,str_status)

    def put(self, request, format=None):
        version = request.POST.get('version')
        device_type = request.POST.get('device_type')
        try:
            now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
            if device_type is not None and device_type=='i':
                appversion_updateqs = EngageboostAppVersionControl.objects.update(version_i=version,modified=now_utc)
            else:
                appversion_updateqs = EngageboostAppVersionControl.objects.update(version_a=version,upgrade_to=version,modified=now_utc)
            str_status = ""
            if appversion_updateqs:
                str_status = status.HTTP_200_OK
                data = {
                    'status':str_status,
                    'message': 'Version update successfully.'
                }
        except Exception as error:
          trace_back = sys.exc_info()[2]
          line = trace_back.tb_lineno
          str_status = status.HTTP_417_EXPECTATION_FAILED
          data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response (data,str_status)


class CustomerQuery(APIView):
    permission_classes = []
    def post(self, request, format=None):
        requestdata          =  JSONParser().parse(request)
        user                 =  request.user
        user_id              =  user.id
        name                 =  requestdata['name']
        try:
            name = name.strip()
        except:
            pass
        email                =  requestdata['email']
        try:
            email = email.strip()
        except:
            pass
        phone                =  requestdata['phone']
        try:
            phone = phone.strip()
        except:
            pass
        message              =  requestdata['message']
        try:
            message = message.strip()
        except:
            pass

        str_status = ""

        try:
            if email=='':
                raise Exception("email is required") 
            pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"   
            valid_email=re.match(pattern,email) 
            if valid_email==None:
                raise Exception("invalid email") 
            if name=='':
                raise Exception("name is required")  
            if phone=='':
                raise Exception("phone is required")
            if message=='':
                raise Exception("message is required")

            now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
            today = now_utc.strftime('%Y-%m-%d')
            if user_id:
                user_id = user_id
            else:
                user_id = 0 
            visitcontact_qs=EngageboostVisitContacts.objects.create(
                user_id = user_id,
                name  = name,
                email = email, 
                telph = phone,
                msg   = message,
                date  = today
            )
            visitcontact_qs.save()

            #visitcontact_data = VisitContactsSerializers(visitcontact_qs).data
            #EMAIL TO User STARTS HERE######################################################3
            buffer_data = common_functions.getAutoResponder("","","","","",19)
            if buffer_data and buffer_data["content"]:
                autoResponderData  = buffer_data["content"]
                if autoResponderData["email_type"] == 'H':
                    emailContent = autoResponderData["email_content"]
                else:
                    emailContent = autoResponderData["email_content_text"]
                emailContent = str(emailContent)

                emailContent = emailContent.replace('{@name}',name)
    
            if email:
                emailcomponent.OrderMail(email,autoResponderData["email_from"],autoResponderData["subject"],emailContent)
            #Notification to admin start here###########################################################
            buffer_data = common_functions.getAutoResponder("","","","","",20)
            if buffer_data and buffer_data["content"]:
                autoResponderData  = buffer_data["content"]
                if autoResponderData["email_type"] == 'H':
                    emailContent = autoResponderData["email_content"]
                else:
                    emailContent = autoResponderData["email_content_text"]
                emailContent = str(emailContent)

                emailContent = emailContent.replace('{@name}',name)
                emailContent = emailContent.replace('{@email}',email)
                emailContent = emailContent.replace('{@phone}',phone)
                emailContent = emailContent.replace('{@message}',message)
                tomail=autoResponderData["email_from"]
                emailcomponent.OrderMail(tomail,autoResponderData["email_from"],autoResponderData["subject"],emailContent)
            str_status = status.HTTP_200_OK
            data = {
                'status':str_status,
                'message': 'success.',
                #'data':visitcontact_data
            }

        except Exception as error:
          trace_back = sys.exc_info()[2]
          line = trace_back.tb_lineno
          str_status = status.HTTP_417_EXPECTATION_FAILED
          data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response (data,str_status)

def Shop_By_Category_ByCatId_new(website_id, warehouse_id):
    website_id 	= 1
    warehouse_id = warehouse_id

    try:
        if website_id is None:
            raise Exception("website_id is required")
        if warehouse_id is None:
            raise Exception("warehouse id is required")
        Category_data = []
        objWarehouse_Categorylst = EngageboostCategoryWarehouse.objects.filter(warehouse_id=warehouse_id,product_count__gt=0).values_list("category_id",flat=True)
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
            return category_data
        else:
            return []
        # return Response(data, status.HTTP_200_OK)
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data = {"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        # return JSONResponse(errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response(data, status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)
        return []


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