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
from frontapp.views.product import discount

from django.db.models import F, Func, FloatField
from django.db.models.functions import Cast

import json
import base64
import sys,os
import traceback
import datetime
from django.db.models import Max,Min,Q, Count
from decimal import Decimal

def get_product_price(product_id,warehouse_id):
    currency_id = 13
    return_price = 0
    if product_id and warehouse_id:
        rs_price = EngageboostChannelCurrencyProductPrice.objects.filter(warehouse_id=warehouse_id, product_id=product_id, currency_id=currency_id).first()
        if rs_price:
            return_price =  rs_price.price
    return return_price

class ProductDetails(APIView):
    permission_classes = []
    def get(self, request, slug, format=None):
        # product_id = pk
        slug = slug
        # warehouse_id = request.GET('warehouse_id')
        website_id = request.META.get('HTTP_WID')
        warehouse_id = request.META.get('HTTP_WAREHOUSE')
        user                   =  request.user
        user_id                =  user.id

        if warehouse_id is None or warehouse_id == 0:
            warehouse_id = 2
        if website_id:
            pass
        else:
            website_id = 1
        warehouse_id = warehouse_id
        # rs_product = EngageboostProducts.objects.filter(slug=slug, isdeleted = 'n', isblocked='n').first()
        rs_product = EngageboostProducts.objects.filter(slug=slug, isdeleted='n', isblocked='n',
                                                        channel_price__price__gt=0,
                                                        channel_price__warehouse_id=warehouse_id).first()
        str_status = ""
        if rs_product:
            productid = rs_product.id
            if user_id:
                qs_wishlist=EngageboostWishlists.objects.filter(user_id=user_id,product_id=productid,isblocked='n',isdeleted='n').exists()
                if qs_wishlist==True:
                    is_wishlist=1
                else:
                    is_wishlist=0
            else:
                is_wishlist=0
            
            product_data = ProductsSerializer(rs_product, context={'warehouse_id': warehouse_id})
            product_data = product_data.data
            product_data.update({'is_wishlist': is_wishlist})
            
            if "channel_price" in product_data:
                if product_data["channel_price"] and product_data["channel_price"]>0:
                    product_data['default_price'] = product_data["channel_price"]

            # Get Product Stock
            rs_stock = EngageboostProductStocks.objects.filter(product_id=product_data['id'], isblocked='n', isdeleted='n', warehouse_id=warehouse_id).first()
            stock_data = ProductStocksSerializer(rs_stock)
            product_data.update({'stock_data': stock_data.data})

            # Get Variant Product
            # coss_product = get_cross_products(product_id)
            product_data.pop('supplier_id')
            product_data.pop('new_date')
            product_data.pop('isbn')
            product_data.pop('ebay_item_id')
            product_data.pop('amazon_itemid')
            product_data.pop('ebay_addstatus')
            product_data.pop('twitter_addstatus')
            product_data.pop('ebay_listing_starttime')
            product_data.pop('ebay_listing_endtime')
            product_data.pop('ebay_listing_build')
            product_data.pop('ebay_listing_version')
            product_data.pop('ebay_listing_time')
            product_data.pop('total_listingfee')
            # product_data["variant_products"] = coss_product
            # if product_data["channel_price"] and product_data["channel_price"]>0:
            #     product_data['default_price'] = product_data["channel_price"]
            request_data = {
                'website_id': website_id,
                'company_id': website_id,
                'product_ids': product_data['id'],
                'qtys': '1',
                'prod_price': product_data['default_price'],
                'warehouse_id':warehouse_id
            }
            productsdiscount = discount.get_discount_detalils(request_data)
            products_discount_data = {
                "new_default_price": Decimal(productsdiscount[0]['new_default_price']).quantize(Decimal('.00')) ,
                "new_default_price_unit": Decimal(productsdiscount[0]['new_default_price_unit']).quantize(Decimal('.00')),
                "discount_price_unit": Decimal(productsdiscount[0]['discount_price_unit']).quantize(Decimal('.00')),
                "discount_price": Decimal(productsdiscount[0]['discount_price']).quantize(Decimal('.00')),
                "discount_amount": Decimal(productsdiscount[0]['discount_amount']).quantize(Decimal('.00')),
                "disc_type": productsdiscount[0]['disc_type'],
                "coupon": productsdiscount[0]['coupon']
            }
            product_data.update(products_discount_data)
            str_status = status.HTTP_200_OK
            data = {
                "status": str_status,
                "data": product_data
            }
        else:
            str_status = status.HTTP_204_NO_CONTENT
            data = {
                "status": str_status,
                "msg": "Product not found."
            }
        # ***************************************************************************************
        result = {'data': data}
        return Response(data, str_status)

def get_cross_products(product_id):
    # Let Product id is a parent Product
    coss_data = []
    parent_product_id = []
    cross_product_list = EngageboostCossSellProducts.objects.filter( product_id=product_id).all().values_list('cross_product_id', flat=True)
    if cross_product_list:
        coss_data = CossSellProductsViewSerializer(
            cross_product_list, many=True)
        # coss_data = coss_data.data
    else:
        # Let given product is a coss product, Find the parent and then find coss for that parent
        rs_parent = EngageboostCossSellProducts.objects.filter(
            cross_product_id=product_id).first()
        if rs_parent:
            cross_product_list = EngageboostCossSellProducts.objects.filter(
                product_id=rs_parent.product_id).values_list('cross_product_id', flat=True)

    rs_variant = EngageboostMarketplaceFieldValue.objects.filter(product_id__in=cross_product_list).all()
    variant_data = EngageboostMarketplaceFieldValueSerializer(rs_variant, many=True)
    # print(json.dumps(variant_data.data))
    return variant_data.data

def get_related_product_ids(product_id=None):
    website_id      = 1 # get_company_website_id_by_url()
    pro_id          = 0
    prod_id_list    = ''
    new_product_id  = product_id
    related_product_type = "1"
    try:
        related_pro_ids = EngageboostRelatedProducts.objects.filter(product_id = new_product_id, related_product_type=related_product_type).values('related_product_id')  # Multiple id
        if related_pro_ids:
            pass
        else:
            rs_id = EngageboostRelatedProducts.objects.filter(related_product_id=new_product_id, related_product_type=1).values('product_id').first()
            if rs_id and len(rs_id)>0:
                pro_id = rs_id['product_id']
                related_pro_ids = EngageboostRelatedProducts.objects.filter(product_id = pro_id, related_product_type="1").values('related_product_id')

        product_with_images = EngageboostProductimages.objects.filter(product_id__in=related_pro_ids).values_list(
            'product_id', flat=True).distinct('product_id')

        related_pro_ids = product_with_images

        if related_pro_ids or pro_id:
            related = True
            prod_id_list =  ','.join(map(str, related_pro_ids))  #             related_pro_ids.join(',') + ","+pro_id
            prod_id_list = prod_id_list + ','+pro_id
        else:
            category_ids_list = category_ids_from_product_ids(product_id)
            prod_id_list = 	product_ids_from_categories_ids(category_ids_list)          
            prod_id_list = list(prod_id_list)
            prod_id_list = ','.join(map(str, prod_id_list))

        # print(prod_id_list)
        # str_list = "292,302"
        str_list = prod_id_list
        return str_list
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}

def get_popular_product_ids(product_id=None,warehouse_id = 2):
    website_id      = 1 # get_company_website_id_by_url()
    pro_id          = 0
    prod_id_list    = ''
    new_product_id  = product_id
    related_product_type = "1"
    try:
        popular_pro_ids = EngageboostProducts.objects.filter(isblocked='n', isdeleted='n',product_stock__real_stock__gt=0,
                                                             product_stock__warehouse=warehouse_id).annotate(product_images_count=Count('product_images')).filter(product_images_count__gt=0).values_list('id',flat=True).order_by('-numberof_view')[:20]
                                                             # product_stock__warehouse=warehouse_id).values_list('id', flat=True).order_by('-numberof_view')[:20]

        # popular_pro_ids = EngageboostProducts.objects.filter(isblocked='n', isdeleted='n',product_stock__real_stock__gt=0,product_stock__warehouse=warehouse_id).values_list('id', flat=True).order_by('-numberof_view')[:20]
        if popular_pro_ids:
            product_ids = ','.join(map(str, popular_pro_ids))
            return product_ids
        else:
            return ""
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}

def category_ids_from_product_ids(product_ids=None, is_primary=None):
    categoris = []
    if product_ids:
        product_ids_arr = product_ids.split(',')
        if product_ids_arr:
            rs_category = EngageboostProductCategories.objects.filter(product_id__in=product_ids_arr).values_list("category_id",flat=True)
            if is_primary is not None:
                rs_category = rs_category.filter(is_parent="Y")
            if rs_category:
                categoris = rs_category
    return categoris

def product_ids_from_categories_ids(category_ids=None):
    products = []
    if category_ids:
        rs_product = EngageboostProductCategories.objects.filter(category_id__in=category_ids).values_list('product_id',flat=True)[:20]
        if rs_product:
            product_ids = rs_product
            products = product_ids
    return products

# get_related_product_ids('370')

@csrf_exempt
def listing_filters(request):
    """ Listing filter for listin module """
    if(request.method == "GET"):
        data = []
        try:
            warehouse_id = request.GET.get('warehouse_id', 4)
            slug = request.GET['slug']
            website_id = request.GET.get('website_id', 1)
            str_type = request.GET.get('type')
            category_ids = request.GET.get('category_ids')
            
            if str_type == 'category':
                cnt = EngageboostCategoryMasters.objects.filter(slug=slug,isdeleted='n',isblocked='n').count()
            else:
                brand_id = 0
                rs_brand = EngageboostBrandMasters.objects.filter(slug=slug, isblocked='n', isdeleted='n').first()
                if rs_brand:
                    brand_id = rs_brand.id
                    brand_id = str(brand_id)
                    rs_product_list = EngageboostProducts.objects.filter(isblocked='n', isdeleted='n').filter( Q(brand__startswith=brand_id+',') | Q(brand__endswith=','+brand_id) | Q(brand__contains=',{0},'.format(brand_id)) | Q(brand__exact=brand_id) ).values_list("id", flat=True)
                    # print(rs_product_list.query)
                    if rs_product_list:
                        rs_cat = EngageboostProductCategories.objects.filter(product_id__in=rs_product_list).values_list("category", flat=True).distinct()
                        cnt = rs_cat.count()
                    else:
                        cnt = 0
                        
            if(cnt > 0):
                if str_type == 'category':
                    objcat = EngageboostCategoryMasters.objects.filter(slug=slug,isdeleted='n',isblocked='n').first()
                    category_id = objcat.id
                    # serializer_data = EngageboostCategoryMasters.objects.filter(parent_id=category_id,isdeleted='n',isblocked='n').order_by('id')
                    if objcat.parent_id >0:
                        serializer_data = EngageboostCategoryMasters.objects.filter(id=category_id,isdeleted='n',isblocked='n').order_by('id')
                    else:
                        serializer_data = EngageboostCategoryMasters.objects.filter(parent_id=category_id,isdeleted='n',isblocked='n').order_by('id')
                else:
                    # rs_cat_parent = EngageboostCategoryMasters.objects.filter(id__in=rs_cat,isdeleted='n',isblocked='n').values_list("parent_id",flat=True).distinct()
                    # if rs_cat_parent.count()>0:
                    #     serializer_data = EngageboostCategoryMasters.objects.filter(parent_id__in=rs_cat_parent,isdeleted='n',isblocked='n').order_by('id')
                    # else:
                    #     serializer_data = EngageboostCategoryMasters.objects.filter(parent_id__in=rs_cat,isdeleted='n',isblocked='n').order_by('id')
                    serializer_data = EngageboostCategoryMasters.objects.filter(id__in=rs_cat,isdeleted='n',isblocked='n').order_by('id')
                lst_cat = serializer_data.values_list("id",flat=True)

                # print(lst_cat.query)
                if str_type == 'category': 
                    if(lst_cat):
                        lst_cat = list(lst_cat)
                        lst_cat.append(category_id)
                    else:
                        lst_cat = [category_id]

                context = {"warehouse_id": warehouse_id}
                categories_data = EngageboostCategoriesSerializer(serializer_data, many=True,context=context).data
                data.append({'field_name': 'categories','field_id':'category_slug','is_variant':'false','is_static':'true','child':categories_data})
                if str_type == "category":
                    # product_lst = EngageboostProductCategories.objects.filter(category_id__in=lst_cat, isblocked='n', isdeleted='n', product_id__isblocked='n', product_id__isdeleted='n').values_list('product_id',flat=True)
                    product_lst = EngageboostProductCategories.objects.filter(category_id__in=lst_cat, isblocked='n', isdeleted='n', product_id__isblocked='n', product_id__isdeleted='n',product__channel_price__warehouse_id=warehouse_id,product__channel_price__price__gt=0, product__product_stock__real_stock__gt=0, product__product_stock__warehouse=warehouse_id).values_list('product_id',flat=True)
                    
                    if category_ids is not None and category_ids!="":
                        cat_ids = category_ids.split(",")
                        cat_ids = set(list(cat_ids))
                        product_lst = EngageboostProductCategories.objects.filter(category_id__in=cat_ids, isblocked='n', isdeleted='n', product_id__isblocked='n', product_id__isdeleted='n', product__channel_price__warehouse_id=warehouse_id,product__channel_price__price__gt=0, product__product_stock__real_stock__gt=0, product__product_stock__warehouse=warehouse_id).values_list('product_id',flat=True)
                        # print("product_lst==", product_lst.query)
                if str_type=="brand":
                    product_lst = rs_product_list
                    # product_lst = product_lst
                if(product_lst):
                    objProducts = EngageboostChannelCurrencyProductPrice.objects.filter(product_id__in = product_lst,warehouse_id=warehouse_id)#,product_price_type_id__in = objproductpricetype
                    range_price = []
                    if(objProducts.count()>0):
                        min_price = objProducts.aggregate(Min('price'))['price__min']
                        max_price = objProducts.aggregate(Max('price'))['price__max']
                        currency = ""
                        queryset=EngageboostGlobalSettings.objects.get(website_id=website_id)
                        currency=EngageboostGlobalsettingCurrencies.objects.filter(global_setting_id=queryset.id).first()
                        if(currency):
                            currencyobj=EngageboostCurrencyMasters.objects.filter(id=currency.currency_id).first()
                            if(currencyobj):
                                currency = currencyobj.currencysymbol
                        # divide_by = 4
                        # max_price= 1000
                        # diff_price = int(max_price)/divide_by
                        divide_by = 6
                        max_price= max_price
                        diff_price = 10
                        rng={}
                        new_price = min_price
                        i=1
                        for i in range(divide_by):
                            rng = {}
                            if i ==0:
                                pass
                            else:
                                if i == 1:
                                    if max_price < diff_price:
                                        rng['min'] = 0
                                        rng['max'] = diff_price
                                        rng['name'] = "Less than " +str(currency)+str(diff_price)
                                        range_price.append(rng)
                                    else:
                                        rng['min'] = 0
                                        rng['max'] = diff_price
                                        rng['name'] = str(currency)+str(0) +" to " +str(currency)+ str(10)
                                        range_price.append(rng)
                                else:
                                    x1 = i-1
                                    new_range = diff_price*x1
                                    x = x1+1
                                    rng1 = ""
                                    if new_range < max_price:
                                        if i<5:
                                            rng['min'] = new_range
                                            rng['max'] = diff_price*x
                                            rng['name'] = str(currency)+str(new_range) +" to " +str(currency)+ str(diff_price*x)
                                            range_price.append(rng)
                                        else:
                                            rng['min'] = new_range
                                            rng['max'] = ""
                                            rng['name'] = rng['name'] = "Above " +str(currency)+ str(new_range)
                                            range_price.append(rng)
                                    else:
                                        rng['min'] = max_price
                                        rng['max'] = ""
                                        rng['name'] = rng['name'] = "Above " +str(currency)+ str(max_price)
                                        range_price.append(rng)

                    data.append({'field_name':'price','field_id':'channel_currency_product_price.price','is_variant':'false','is_static':'true','child': range_price, "max_price":max_price})
                    curr_product_lst = EngageboostChannelCurrencyProductPrice.objects.filter(product_id__in = product_lst,warehouse_id=warehouse_id).distinct().values_list('product_id',flat=True)
                
                    # brand_list = EngageboostProducts.objects.filter(isblocked='n', isdeleted='n',id__in = product_lst).values_list('brand',flat=True).distinct()
                    brand_list = EngageboostProducts.objects.filter(isblocked='n', isdeleted='n',id__in = product_lst, channel_price__warehouse_id=warehouse_id,channel_price__price__gt=0, product_stock__real_stock__gt=0, product_stock__warehouse=warehouse_id).values_list('brand',flat=True).distinct()
                    brand_list = EngageboostProducts.objects.filter(isblocked='n', isdeleted='n',id__in = product_lst).values_list('brand',flat=True).distinct()
                    print(brand_list.query)
                    if(brand_list):
                        lst_brand= []
                        for brnd in brand_list:
                            if ("," in str(brnd)):
                                lst_brand.extend(brnd.split(","))
                            else:
                                lst_brand.append(brnd)
                        brand_list=lst_brand
                    else:
                        brand_list = []
                    brand_data = EngageboostBrandMasters.objects \
                        .filter(id__in=brand_list,
                            isdeleted='n',
                            isblocked='n').order_by('id')
                    brand_data = BrandMastersSerializer(brand_data, many=True).data
                    data.append({'field_name':'brand','field_id':'brand_slug','is_variant':'false','is_static':'false','child': brand_data})

                    layoutFieldsobj = EngageboostDefaultModuleLayoutFields.objects.filter(category_id__in = lst_cat).values_list('field_id',flat=True)
                    # print(layoutFieldsobj.query)
                    field_ids_list = EngageboostDefaultsFields.objects.filter(id__in = layoutFieldsobj,visible_in_filter=1, isblocked='n', isdeleted='n').values_list('id',flat=True)
                    # print(field_ids_list.query)
                    if(field_ids_list):
                        field_ids_list = list(field_ids_list)
                        fields_names = EngageboostMarketplaceFieldValue.objects.filter(product_id__in = product_lst,field_id__in = field_ids_list).distinct('field_id','field_name').values_list('field_name',flat=True)
                        # print(fields_names.query)
                        if(fields_names):
                            fields_lst = list(fields_names)
                            #print(product_lst)
                            for field_d in fields_lst:
                                objMarketplace_size = EngageboostMarketplaceFieldValue.objects.filter(field_name__icontains =field_d, product_id__in = product_lst).distinct('field_id','product_id')
                                # print(objMarketplace_size.query)  ##  Actual value from list
                                objsize_data = MarketplaceFieldValueSerializerListing(objMarketplace_size,many=True).data
                                field_name=[]
                                field_v = {}
                                for s_data in objsize_data:
                                    if("#" in str(s_data['value'])):
                                        s_val = s_data['value'].split("##")
                                        for sp in s_val:
                                            if(sp!=""):
                                                if(sp in field_v.keys()):
                                                    field_v[sp].append(s_data['product_id'])
                                                else:
                                                    field_v[sp]= [s_data['product_id']]
                                    else:
                                        if(s_data['value'] in field_v.keys()):
                                            field_v[s_data['value']].append(s_data['product_id'])
                                        else:
                                            field_v[s_data['value']]=[s_data['product_id']]
                                for key,val in field_v.items():
                                    out = {}
                                    out['id']=val
                                    out['name']=key
                                    field_name.append(out)
                                data.append({'field_name':field_d,'field_id':field_d,'is_variant':'true','is_static':'false','child': field_name})
                    discount_data=[]
					
                    data.append({'field_name':'discount','field_id':'id','is_variant':'false','is_static':'false','child': discount_data})
                    
                else:
                    data = [{
                        "status": 0,
                        "message": "Product not found."
                    }]
                # else:
                # 	data = [{
                # 			"status": 0,
                # 			"message": "Product not found."
                # 		}]
            else:
                data = [{
                    "status": 0,
                    "message": "Category not found."
                }]
                    
        except Exception as error:
            str_status = status.HTTP_417_EXPECTATION_FAILED
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in saving customer information"}
            # data = []
    else:
        data = [{
            "status": 0,
            "message": "invalid request"
        }]
		
    return JsonResponse(data, safe=False)   

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
                rs_product_list = EngageboostProducts.objects.filter(isblocked='n', isdeleted='n').filter( Q(brand__startswith=rs_brand.id+',') | Q(brand__endswith=','+rs_brand.id) | Q(brand__contains=',{0},'.format(rs_brand.id)) | Q(brand__exact=rs_brand.id) ).count()
                sort_by = []
                sortby_lst = ['Popularity','New Arrivals','Price : High to Low','Price : Low to High']
                for i in range(len(sortby_lst)):
                    sort_data = {}
                    sort_data['id'] = i+1
                    sort_data['name'] = sortby_lst[i]
                    print("sort_data", sort_data)
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
def CategoryProductListView(request):
	"""product list by category id"""
	if request.method == 'POST':
		category_id = request.POST.get('category_id')
		warehouse_id = request.POST.get('warehouse_id') 
		#data = {"status" : 0,"msg" : "something went wrong"}
		website_id = request.POST.get('website_id')
		try:
			if category_id is None:
				raise Exception("category_id is required") 
			if warehouse_id is None :
				raise Exception("warehouse_id is required") 
			if website_id is None:
				raise Exception("website_id is required")
			return_data=[]
			
			product_data = []
			
			product_ids = EngageboostProductCategories.objects.filter(category_id=category_id, isblocked='n', isdeleted='n',).all().values_list('product_id', flat=True)
			if len(product_ids) > 0:
				
				product_dtl = EngageboostProducts.objects.filter(id__in=product_ids,isblocked='n', isdeleted='n',website_id=website_id).all()

				if product_dtl:

					product_data = ProductSerializer(product_dtl, context={'warehouse_id': warehouse_id}, many=True).data
					
					if product_data:
						for productvalue in product_data:
							variant_product =[]
							cross_productArr=[]
							qscrossprod =[]
							productvalue.update({'brand_name':''})
							variant_data = EngageboostCossSellProducts.objects.filter(product_id=productvalue['id']).all()

							if variant_data:
								for qsprod in variant_data:
									cross_productArr.append(qsprod.cross_product_id)
									#cross_productArr.append(qsprod.cross_product_id)
							if len(cross_productArr)>0:
								qscrossprod = EngageboostProducts.objects.filter(id__in=cross_productArr,isdeleted='n', isblocked='n',website_id=website_id).all()
								if qscrossprod:
									crossrroductresult = ProductSerializer(qscrossprod,context={'warehouse_id': warehouse_id},many=True).data
									if crossrroductresult:
										for crossbrand in crossrroductresult:
											crossbrand.update({'brand_name':''})
											qs_brand = EngageboostBrandMasters.objects.filter(id=crossbrand['brand'], isblocked='n', isdeleted='n').first()
											if qs_brand:
												crossbrand.update({'brand_name':qs_brand.name})
									#variant_product.append(crossrroductresult)
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
			
			
			
			if return_data:

				data = {
				"status":1,
				"data":return_data 

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
	return JsonResponse(data)

class CategoryProductListView(APIView):
    def options(self,request,format=None):
        print("**************** Category prodyuct request ************")
    def get(self, request, format=None):
        website_id = request.META.get('HTTP_WID')
        category_id = request.META.get('HTTP_CAT')
        #print("************category id *************")
        #print(category_id)
        warehouse_id = 1
        # category_id = 2

        if website_id:
            pass
        else:
            website_id = 1
        product = []

        # Get sorting data
        filter_var = self.request.GET.get("filter")

        list_order_by = '-product__numberof_sale'
        if filter_var is not None and filter_var == "popular":
            list_order_by = "-product__numberof_sale"
        elif filter_var is not None and filter_var == "price-low-high":
            list_order_by = "product__default_price"
        elif filter_var is not None and filter_var == "price-high-low":
            list_order_by = "-product__default_price"
        else:
            list_order_by = "-product__numberof_sale"

        # View Only Parent Products
        product_ids = EngageboostProductCategories.objects.filter(category_id=category_id, isblocked='n', isdeleted='n', product__isdeleted='n', product__isblocked='n', product__visibility_id=1).all()

        # Product Filter

        #  Price Range
        price_range = self.request.GET.get("price_range")

        lower_price = 0
        upper_price = 0
        if price_range:
            price_range_arr = price_range.split("-")
            if len(price_range_arr) > 0:
                if price_range_arr[0] is not None:
                    lower_price = price_range_arr[0]
                if price_range_arr[1] is not None:
                    upper_price = price_range_arr[1]

            product_ids = product_ids.filter(product__default_price__gte=lower_price, product__default_price__lte=upper_price)

        # Brand
        brand = self.request.GET.get("brand")
        if brand:
            brand_arr = brand.split(",")
            product_ids = product_ids.filter(product__brand__in=brand_arr)

        # Order By (Sorting)
        product_ids = product_ids.order_by(list_order_by)
        # product_data = ProductCategoriesSerializer(product_ids, many=True)

        page = self.paginate_queryset(product_ids)
        if page is not None:
            serializer = ProductCategoriesSerializer(page, many=True)
            for products in serializer.data:
                # print(json.dumps(products, indent=4, sort_keys=True))
                # Get Product Stock
                qs_stock = EngageboostProductStocks.objects.filter(product_id=products['id'], warehouse_id=warehouse_id).all()
                stock_data = ProductStocksSerializer(qs_stock, many=True)
                # Get variant Products
                cross_prod_arr = get_cross_products(products['id'])
                products.update(
                    {'varient_product': cross_prod_arr, 'stock_details': stock_data.data})
                # for cross_product in cross_prod_arr
                request_data = {
                    'website_id': website_id,
                    'company_id': website_id,
                    'product_ids': products['product']['id'],
                    'qtys': '1',
                    'prod_price': products['product']['default_price']
                }
                products_discount = discount.get_discount_detalils(request_data)

                for productsdiscount in products_discount:
                    products_discount_data = {
                        "new_default_price": Decimal(productsdiscount[0]['new_default_price']).quantize(Decimal('.00')) ,
                        "new_default_price_unit": Decimal(productsdiscount['new_default_price_unit']).quantize(Decimal('.00')),
                        "discount_price_unit": Decimal(productsdiscount['discount_price_unit']).quantize(Decimal('.00')),
                        "discount_price": Decimal(productsdiscount['discount_price']).quantize(Decimal('.00')),
                        "discount_amount": Decimal(productsdiscount['discount_amount']).quantize(Decimal('.00')),
                        "disc_type": productsdiscount['disc_type'],
                        "coupon": productsdiscount['coupon']
                    }
                    products['product'].update(products_discount_data)
                product.append(products)
        return self.get_paginated_response(serializer.data)
  

class SimilarProduct(APIView):
    permission_classes = []
    def get(self, request, product_id, format=None):
        product_id = product_id
        warehouse_id           = request.META.get('HTTP_WAREHOUSE')
        if warehouse_id is None:
            warehouse_id = 2
        # similar product
        ret_data = ProductList(product_id, warehouse_id)
        str_status = ""
        if ret_data:
            str_status = status.HTTP_200_OK
        else:
            # str_status = status.HTTP_204_NO_CONTENT
            str_status = status.HTTP_200_OK

        data = {
            "status":str_status,
            "data":ret_data
        }
        return Response(data, str_status)


class PopularProduct(APIView):
    permission_classes = []
    def get(self, request, product_id, format=None):
        product_id = product_id
        warehouse_id           = request.META.get('HTTP_WAREHOUSE')
        ret_data = PopularProductList(product_id, warehouse_id)
        str_status = ""
        if ret_data:
            str_status = status.HTTP_200_OK
        else:
            str_status = status.HTTP_204_NO_CONTENT

        data = {
            "status":str_status,
            "data":ret_data
        }
        return Response(data, str_status)
        # return Response(ret_data)

def PopularProductList(product_id, warehouse_id=None):
    website_id = 1
    if warehouse_id is None:
        warehouse_id = 2
    
    product_id = get_popular_product_ids(product_id,warehouse_id)
    
    product_ids_arr = product_id.split(',')
    # product_ids = EngageboostProductCategories.objects.filter(product_id__in=product_ids_arr, isblocked='n', isdeleted='n', product_id__visibility_id = 1, product_id__channel_price__warehouse_id=warehouse_id,product_id__channel_price__price__gt=0).all()[:15].iterator()

    product_ids = EngageboostProductCategories.objects.filter(product_id__in=product_ids_arr, isblocked='n', isdeleted='n',
                                                              product_id__visibility_id = 1, product_id__channel_price__warehouse_id=warehouse_id,
                                                              # product_id__channel_price__price__gt=0).annotate(product_images_count=Count('product_id__product_images')).filter(product_images_count__gt=0).all()[:15].iterator()
                                                              product_id__channel_price__price__gt=0).all()[:15].iterator()
    if product_ids is not None:
        serializer = ProductCategoriesSerializer(product_ids, context={'warehouse_id': warehouse_id}, many=True)
        product = []
        for products in serializer.data:
            # Get Product Stock
            qs_stock = EngageboostProductStocks.objects.filter(product_id=products['product']['id'],warehouse_id=warehouse_id).all()
            # print('qs_stock', qs_stock.query)
            stock_data = ProductStocksSerializer(qs_stock, many=True)
            stock_data = stock_data.data
            # Get variant Products
            # cross_prod_arr = get_cross_products(products['product']['id'])
            # products.update({'varient_product': cross_prod_arr, 'stock_details': stock_data.data})
            if len(stock_data)<=0:
                stock_data_obj = {
                    "product_id":products['id'],
                    "real_stock":0,
                    "warehouse_id":warehouse_id
                }
                stock_data.append(stock_data_obj)
            products.update({'stock_details': stock_data})
            # for cross_product in cross_prod_arr
            if products['product']['channel_price']>0:
                products['product']['default_price'] = products['product']['channel_price']
                request_data = {
                    'website_id': website_id,
                    'company_id': website_id,
                    'product_ids': products['product']['id'],
                    'qtys': '1',
                    'prod_price': products['product']['channel_price'],
                    'default_price': products['product']['channel_price'],
                    'warehouse_id': warehouse_id
                }
                products_discount = discount.get_discount_detalils(request_data)

                for productsdiscount in products_discount:
                    products['product']['default_price'] = products['product']['channel_price']
                    products_discount_data = {
                        "new_default_price": Decimal(productsdiscount['new_default_price']).quantize(Decimal('.00')),
                        "new_default_price_unit": Decimal(productsdiscount['new_default_price_unit']).quantize(Decimal('.00')),
                        "discount_price_unit": Decimal(productsdiscount['discount_price_unit']).quantize(Decimal('.00')),
                        "discount_price": Decimal(productsdiscount['discount_price']).quantize(Decimal('.00')),
                        "discount_amount": Decimal(productsdiscount['discount_amount']).quantize(Decimal('.00')),
                        "disc_type": productsdiscount['disc_type'],
                        "coupon": productsdiscount['coupon']
                    }
                products['product'].update(products_discount_data)
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
                products['product'].update(products_discount_data)
    return serializer.data

# PopularProductList(1941,4)

def ProductList(product_id, warehouse_id):
    website_id = 1
    old_product_id = product_id
    product_id = get_related_product_ids(product_id)
    if product_id:
        product_ids_arr = product_id.split(',')
        product_ids_arr = product_ids_arr
        product_ids_arr = [x for x in product_ids_arr if x != old_product_id]
        
        # product_ids = EngageboostProductCategories.objects.filter(product_id__in=product_ids_arr, isblocked='n', isdeleted='n', product__isdeleted='n', product__isblocked='n', product__visibility_id=1).all()
        # product_ids = EngageboostProductCategories.objects.filter(product_id__in=product_ids_arr, isblocked='n', isdeleted='n', product_id__visibility_id=1, product_id__channel_price__warehouse_id=warehouse_id,product_stock__real_stock__gt=0, product_stock__warehouse=warehouse_id).exclude(product_id__channel_price__price__gt=0).all()[:15].iterator()

        product_ids = EngageboostProductCategories.objects.filter(product_id__in=product_ids_arr, isblocked='n', isdeleted='n',
                                                                  product_id__visibility_id=1, product_id__channel_price__warehouse_id=warehouse_id,
                                                                  product_id__channel_price__price__gt=0, product_id__product_stock__real_stock__gt=0,
                                                                  # product_id__product_stock__warehouse=warehouse_id).annotate(product_images_count=Count('product_id__product_images')).filter(product_images_count__gt=0).all()[:15].iterator()
                                                                  product_id__product_stock__warehouse=warehouse_id).all()[:15].iterator()
        if product_ids is not None:
            serializer = ProductCategoriesSerializer(product_ids, context={'warehouse_id': warehouse_id}, many=True)
            product = []
            stock_data = []
            for products in serializer.data:
                # Get Product Stock
                qs_stock = EngageboostProductStocks.objects.filter(product_id=products['product']['id'], warehouse_id=warehouse_id).all()
                stock_data = ProductStocksSerializer(qs_stock, many=True)
                stock_data = stock_data.data
                products['product']['default_price'] = products['product']['channel_price']
                # Get variant Products
                # cross_prod_arr = get_cross_products(products['product']['id'])
                # products.update({'varient_product': cross_prod_arr, 'stock_details': stock_data.data})
                if len(stock_data)<=0:
                    stock_data_obj = {
                        "product_id":products['id'],
                        "real_stock":0,
                        "warehouse_id":warehouse_id
                    }
                    stock_data.append(stock_data_obj)

                products.update({'stock_details': stock_data})
                # for cross_product in cross_prod_arr
                if products['product']['channel_price']>0:
                    products['product']['default_price'] = products['product']['channel_price']
                    request_data = {
                        'website_id': website_id,
                        'company_id': website_id,
                        'product_ids': products['product']['id'],
                        'qtys': '1',
                        'prod_price': products['product']['channel_price'],
                        'default_price': products['product']['channel_price'],
                        'warehouse_id': warehouse_id
                    }
                    products_discount = discount.get_discount_detalils(request_data)    
                    for productsdiscount in products_discount:
                        products_discount_data = {
                            "new_default_price": Decimal(productsdiscount['new_default_price']).quantize(Decimal('.00')),
                            "new_default_price_unit": Decimal(productsdiscount['new_default_price_unit']).quantize(Decimal('.00')),
                            "discount_price_unit": Decimal(productsdiscount['discount_price_unit']).quantize(Decimal('.00')),
                            "discount_price": Decimal(productsdiscount['discount_price']).quantize(Decimal('.00')),
                            "discount_amount": Decimal(productsdiscount['discount_amount']).quantize(Decimal('.00')),
                            "disc_type": productsdiscount['disc_type'],
                            "coupon": productsdiscount['coupon']
                        }
                        products['product'].update(products_discount_data)
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
                    products['product'].update(products_discount_data)
                # Static
                # products_discount_data = {
                #     "new_default_price": 0,
                #     "new_default_price_unit": 0,
                #     "discount_price_unit": 0,
                #     "discount_price": 0,
                #     "discount_amount": 0,
                #     "disc_type": 1,
                #     "coupon": ""
                # }
                # products['product'].update(products_discount_data)
        return serializer.data
    else:
        return []

def get_related_product_ids_for_like(product_ids=None):
    website_id      = 1 # get_company_website_id_by_url()
    pro_id          = 0
    prod_id_list    = ''
    new_product_id  = product_ids
    related_product_type = "1"
    try:
        if product_ids is not None:
            new_product_id = product_ids.split(",")
            related_pro_ids = EngageboostRelatedProducts.objects.filter(product_id__in = new_product_id, related_product_type=related_product_type).values('related_product_id')  # Multiple id
            if related_pro_ids:
                pass
            else:
                rs_id = EngageboostRelatedProducts.objects.filter(related_product_id__in=new_product_id, related_product_type=1).values('product_id').first()

                if rs_id and len(rs_id)>0:
                    pro_id = rs_id['product_id']
                    related_pro_ids = EngageboostRelatedProducts.objects.filter(product_id = pro_id, related_product_type="1").values('related_product_id')

            if related_pro_ids or pro_id:
                related = True
                prod_id_list =  ','.join(map(str, related_pro_ids))  #             related_pro_ids.join(',') + ","+pro_id
                prod_id_list = prod_id_list + ','+pro_id
            else:
                category_ids_list = category_ids_from_product_ids(product_ids)
                prod_id_list = 	product_ids_from_categories_ids(category_ids_list)          
                prod_id_list = list(prod_id_list)
                prod_id_list = ','.join(map(str, prod_id_list))

            str_list = prod_id_list
            return str_list
        else:
            return ""
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}

def LikeProductList(product_id):
    website_id = 1
    warehouse_id = 2
    product_id = get_related_product_ids_for_like(product_id)
    if product_id:
        product_ids_arr = product_id.split(',')
        product_ids_arr = product_ids_arr
        # product_ids = EngageboostProductCategories.objects.filter(product_id__in=product_ids_arr, isblocked='n', isdeleted='n', product__isdeleted='n', product__isblocked='n', product__visibility_id=1).all()
        product_ids = EngageboostProductCategories.objects.filter(product_id__in=product_ids_arr, isblocked='n', isdeleted='n', product_id__visibility_id=1).all()
    
        if product_ids is not None:
            serializer = ProductCategoriesSerializer(product_ids, many=True)
            product = []
            for products in serializer.data:
                # Get Product Stock
                qs_stock = EngageboostProductStocks.objects.filter(product_id=products['id'], warehouse_id=warehouse_id).all()
                stock_data = ProductStocksSerializer(qs_stock, many=True)
                new_price = get_product_price(products['product']['id'], warehouse_id)
                if new_price>0:
                    products['product']['default_price'] = new_price
                # Get variant Products
                # cross_prod_arr = get_cross_products(products['product']['id'])
                # products.update({'varient_product': cross_prod_arr, 'stock_details': stock_data.data})
                products.update({'stock_details': stock_data.data})
                # for cross_product in cross_prod_arr
                request_data = {
                    'website_id': website_id,
                    'company_id': website_id,
                    'product_ids': products['product']['id'],
                    'qtys': '1',
                    'prod_price': products['product']['default_price']
                }
                products_discount = discount.get_discount_detalils(request_data)

                for productsdiscount in products_discount:
                    products_discount_data = {
                        "new_default_price": round(productsdiscount['new_default_price'],2),
                        "new_default_price_unit": round(productsdiscount['new_default_price_unit'],2),
                        "discount_price_unit": round(productsdiscount['discount_price_unit'],2),
                        "discount_price": round(productsdiscount['discount_price'],2),
                        "discount_amount": round(productsdiscount['discount_amount'],2),
                        "disc_type": productsdiscount['disc_type'],
                        "coupon": productsdiscount['coupon']
                    }
                    products['product'].update(products_discount_data)

                # Static
                # products_discount_data = {
                #     "new_default_price": 0,
                #     "new_default_price_unit": 0,
                #     "discount_price_unit": 0,
                #     "discount_price": 0,
                #     "discount_amount": 0,
                #     "disc_type": 1,
                #     "coupon": ""
                # }
                # products['product'].update(products_discount_data)
        # print(serializer.data)
        return serializer.data
    else:
        return []

# LikeProductList("25,580,711")

class LikeProduct(APIView):
    permission_classes = []
    def get(self, request, format=None):
        requestdata = request.data
        user                = request.user
        user_id             = user.id
        device_id           = request.META.get('HTTP_DEVICEID')
        customer_id         = user_id
        # website_id          = get_company_website_id_by_url()
        # company_id          = get_company_id_by_url()

        if user_id is not None:
            rs_cart_product = EngageboostTemporaryShoppingCarts.objects.filter(customer_id=user_id).values_list('product_id')
        elif device_id is not None:
            rs_cart_product = EngageboostTemporaryShoppingCarts.objects.filter(device_id=device_id).values_list('product_id')

        if rs_cart_product:
           str_list = "25,580,711"
           ret_data = LikeProductList(str_list)

        str_status = ""
        if ret_data:
            str_status = status.HTTP_200_OK
        else:
            str_status = status.HTTP_204_NO_CONTENT
        str_status = status.HTTP_200_OK
        data = {
            "status":str_status,
            "data":ret_data
        }
        return Response(data, str_status)

class SlugToId(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        requestdata = request.data
        slug = requestdata['slug']
        listingType = requestdata['listingType']
        if slug:
            if listingType.lower() == "category":
                # rs_cat = EngageboostCategoryMasters.objects.filter(slug__icontains=slug).first()
                rs_cat = EngageboostCategoryMasters.objects.filter(slug=slug).first()
            else:
                # rs_cat = EngageboostBrandMasters.objects.filter(slug__icontains=slug).first()
                rs_cat = EngageboostBrandMasters.objects.filter(slug=slug).first()
                
            if rs_cat:
                data = {
                    "status":1,
                    "id":rs_cat.id,
                    "name":rs_cat.name
                }
            else:
                data = {
                    "status":0,
                    "id":0
                }
        else:
            data = {
                    "status":0,
                    "id":0
                }
        return Response(data)

class SearchList(APIView):
    permission_classes = []
    def get(self, request, format=None):
        search_value = request.GET.get('v')
        warehouse_id = request.META.get('HTTP_WAREHOUSE')
        website_id = 1
        str_search_value = ""
        ret_data = []
        product_ids = ""
        if warehouse_id is None:
            warehouse_id = 2
        
        if search_value is not None:
            str_search_value = base64.b64decode(search_value)
            str_search_value = str(str_search_value)
            str_search_value = str_search_value.replace("b","")
            str_search_value = str_search_value.replace("'","")
            product_ids = str_search_value

        if product_ids:
            product_id_list = product_ids.split(",")
            selling_product     = EngageboostProducts.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, channel_price__warehouse_id=warehouse_id,channel_price__price__gt=0, id__in = product_id_list, product_stock__real_stock__gt=0, product_stock__warehouse=warehouse_id).distinct('channel_price__product_id').all()
            # print("selling_product++++++++++++", selling_product.query)
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
            ret_data = sellingproduct_data
        str_status = ""
        if ret_data:
            str_status = status.HTTP_200_OK
        else:
            str_status = status.HTTP_204_NO_CONTENT

        data = {
            "status":str_status,
            "data":ret_data
        }
        return Response(data, str_status)

class SearchFilters(APIView):
    permission_classes = []
    def get(self, request, format=None):
        data = []
        try:
            warehouse_id = request.META.get('HTTP_WAREHOUSE')        
            website_id = request.GET.get('website_id', 1)
            search_value = request.GET.get('v')
            category_ids = request.GET.get('category_ids')
            # if str_type == 'category':
            #     cnt = EngageboostCategoryMasters.objects.filter(slug=slug,isdeleted='n',isblocked='n').count()
            # else:
            #     brand_id = 0
            #     rs_brand = EngageboostBrandMasters.objects.filter(slug=slug, isblocked='n', isdeleted='n').first()
            #     if rs_brand:
            #         brand_id = rs_brand.id
            #         brand_id = str(brand_id)
            #         rs_product_list = EngageboostProducts.objects.filter(isblocked='n', isdeleted='n').filter( Q(brand__startswith=brand_id+',') | Q(brand__endswith=','+brand_id) | Q(brand__contains=',{0},'.format(brand_id)) | Q(brand__exact=brand_id) ).values_list("id", flat=True)
            if search_value is not None:
                str_search_value = base64.b64decode(search_value)
                str_search_value = str(str_search_value)
                str_search_value = str_search_value.replace("b","")
                str_search_value = str_search_value.replace("'","")
                product_ids = str_search_value
                
            product_id_list = product_ids.split(",")
            product_lst = product_id_list
            if product_id_list:
                rs_cat = EngageboostProductCategories.objects.filter(product_id__in=product_id_list).values_list("category", flat=True).distinct()
                # print(rs_cat.query)
                cnt = rs_cat.count()
            else:
                cnt = 0
            if(cnt > 0):
                # if str_type == 'category':
                #     objcat = EngageboostCategoryMasters.objects.filter(slug=slug,isdeleted='n',isblocked='n').first()
                #     category_id = objcat.id
                #     if objcat.parent_id >0:
                #         serializer_data = EngageboostCategoryMasters.objects.filter(id=category_id,isdeleted='n',isblocked='n').order_by('id')
                #     else:
                #         serializer_data = EngageboostCategoryMasters.objects.filter(parent_id=category_id,isdeleted='n',isblocked='n').order_by('id')
                # else:
                #     serializer_data = EngageboostCategoryMasters.objects.filter(id__in=rs_cat,isdeleted='n',isblocked='n').order_by('id')
                # lst_cat = serializer_data.values_list("id",flat=True)
                serializer_data = EngageboostCategoryMasters.objects.filter(id__in=rs_cat,isdeleted='n',isblocked='n').order_by('id')
                lst_cat = serializer_data.values_list("id",flat=True)
                # if str_type == 'category': 
                #     if(lst_cat):
                #         lst_cat = list(lst_cat)
                #         lst_cat.append(category_id)
                #     else:
                #         lst_cat = [category_id]

                context = {"warehouse_id": warehouse_id}
                categories_data = EngageboostCategoriesSerializer(serializer_data, many=True,context=context).data
                # print("categories_data============", json.dumps(categories_data))
                data.append({'field_name': 'categories','field_id':'category_slug','is_variant':'false','is_static':'true','child':categories_data})
                # print("data+++++++++", data)
                # if str_type == "category":
                #     print("kkkk")
                #     product_lst = EngageboostProductCategories.objects.filter(category_id__in=lst_cat, isblocked='n', isdeleted='n', product_id__isblocked='n', product_id__isdeleted='n').values_list('product_id',flat=True)
                if category_ids is not None and category_ids!="":
                    cat_ids = category_ids.split(",")
                    cat_ids = set(list(cat_ids))
                    product_lst = EngageboostProductCategories.objects.filter(category_id__in=cat_ids, isblocked='n', isdeleted='n', product_id__isblocked='n', product_id__isdeleted='n', product_id__in=product_lst).values_list('product_id',flat=True)
                    
                # if str_type=="brand":
                #     product_lst = rs_product_list

                # product_lst = product_id_list
                if(product_lst):
                    objProducts = EngageboostChannelCurrencyProductPrice.objects.filter(product_id__in = product_lst,warehouse_id=warehouse_id)
                    range_price = []
                    if(objProducts.count()>0):
                        min_price = objProducts.aggregate(Min('price'))['price__min']
                        max_price = objProducts.aggregate(Max('price'))['price__max']
                        currency = ""
                        queryset=EngageboostGlobalSettings.objects.get(website_id=website_id)
                        currency=EngageboostGlobalsettingCurrencies.objects.filter(global_setting_id=queryset.id).first()
                        if(currency):
                            currencyobj=EngageboostCurrencyMasters.objects.filter(id=currency.currency_id).first()
                            if(currencyobj):
                                currency = currencyobj.currencysymbol
                        divide_by = 6
                        max_price= max_price
                        diff_price = 10
                        rng={}
                        new_price = min_price
                        i=1
                        for i in range(divide_by):
                            rng = {}
                            if i ==0:
                                pass
                            else:
                                if i == 1:
                                    if max_price < diff_price:
                                        rng['min'] = 0
                                        rng['max'] = diff_price
                                        rng['name'] = "Less than " +str(currency)+str(diff_price)
                                        range_price.append(rng)
                                    else:
                                        rng['min'] = 0
                                        rng['max'] = diff_price
                                        rng['name'] = str(currency)+str(0) +" to " +str(currency)+ str(10)
                                        range_price.append(rng)
                                else:
                                    x1 = i-1
                                    new_range = diff_price*x1
                                    x = x1+1
                                    rng1 = ""
                                    if new_range < max_price:
                                        if i<5:
                                            rng['min'] = new_range
                                            rng['max'] = diff_price*x
                                            rng['name'] = str(currency)+str(new_range) +" to " +str(currency)+ str(diff_price*x)
                                            range_price.append(rng)
                                        else:
                                            rng['min'] = new_range
                                            rng['max'] = ""
                                            rng['name'] = rng['name'] = "Above " +str(currency)+ str(new_range)
                                            range_price.append(rng)
                                    else:
                                        rng['min'] = max_price
                                        rng['max'] = ""
                                        rng['name'] = rng['name'] = "Above " +str(currency)+ str(max_price)
                                        range_price.append(rng)

                    data.append({'field_name':'price','field_id':'channel_currency_product_price.price','is_variant':'false','is_static':'true','child': range_price, "max_price":max_price})
                    curr_product_lst = EngageboostChannelCurrencyProductPrice.objects.filter(product_id__in = product_lst,warehouse_id=warehouse_id).distinct().values_list('product_id',flat=True)
                    brand_list = EngageboostProducts.objects.filter(isblocked='n', isdeleted='n',id__in = product_lst).values_list('brand',flat=True).distinct()
                    # print(brand_list.query)
                    if(brand_list):
                        lst_brand= []
                        for brnd in brand_list:
                            if ("," in str(brnd)):
                                lst_brand.extend(brnd.split(","))
                            else:
                                lst_brand.append(brnd)
                        brand_list=lst_brand
                    else:
                        brand_list = []
                    brand_data = EngageboostBrandMasters.objects \
                        .filter(id__in=brand_list,
                            isdeleted='n',
                            isblocked='n').order_by('id')
                    brand_data = BrandMastersSerializer(brand_data, many=True).data
                    data.append({'field_name':'brand','field_id':'brand_slug','is_variant':'false','is_static':'false','child': brand_data})

                    layoutFieldsobj = EngageboostDefaultModuleLayoutFields.objects.filter(category_id__in = lst_cat).values_list('field_id',flat=True)
                    field_ids_list = EngageboostDefaultsFields.objects.filter(id__in = layoutFieldsobj,visible_in_filter=1, isblocked='n', isdeleted='n').values_list('id',flat=True)
                    if(field_ids_list):
                        field_ids_list = list(field_ids_list)
                        fields_names = EngageboostMarketplaceFieldValue.objects.filter(product_id__in = product_lst,field_id__in = field_ids_list).distinct('field_id','field_name').values_list('field_name',flat=True)
                        if(fields_names):
                            fields_lst = list(fields_names)
                            for field_d in fields_lst:
                                objMarketplace_size = EngageboostMarketplaceFieldValue.objects.filter(field_name__icontains =field_d, product_id__in = product_lst).distinct('field_id','product_id')
                                objsize_data = MarketplaceFieldValueSerializerListing(objMarketplace_size,many=True).data
                                field_name=[]
                                field_v = {}
                                for s_data in objsize_data:
                                    if("#" in str(s_data['value'])):
                                        s_val = s_data['value'].split("##")
                                        for sp in s_val:
                                            if(sp!=""):
                                                if(sp in field_v.keys()):
                                                    field_v[sp].append(s_data['product_id'])
                                                else:
                                                    field_v[sp]= [s_data['product_id']]
                                    else:
                                        if(s_data['value'] in field_v.keys()):
                                            field_v[s_data['value']].append(s_data['product_id'])
                                        else:
                                            field_v[s_data['value']]=[s_data['product_id']]
                                for key,val in field_v.items():
                                    out = {}
                                    out['id']=val
                                    out['name']=key
                                    field_name.append(out)
                                data.append({'field_name':field_d,'field_id':field_d,'is_variant':'true','is_static':'false','child': field_name})
                    discount_data=[]
                    
                    data.append({'field_name':'discount','field_id':'id','is_variant':'false','is_static':'false','child': discount_data})                    
                else:
                    data = [{
                        "status": 0,
                        "message": "Product not found."
                    }]
            else:
                data = [{
                    "status": 0,
                    "message": "Category not found."
                }]
        except Exception as ex:
            str_status = status.HTTP_417_EXPECTATION_FAILED
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            # data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error)}
            data = []
		
        sort_by = []
        sortby_lst = ['New Arrivals','Price : High to Low','Price : Low to High']
        for i in range(len(sortby_lst)):
            sort_data = {}
            sort_data['id'] = i+1
            sort_data['name'] = sortby_lst[i]
            sort_by.append(sort_data)
        data.append({'field_name':"sort_by",'child': sort_by})

        return Response(data)   


def PriceFilter():
    warehouse_id = 4
    data = []
    website_id = 1
    product_lst = [1960,1971,1967,1945,1950,1963,1947,1962,1952,1964,1943,1946,1968,1954,1944,1956,1942,1966,1948,1949,1957,1941,1965,1969,1958]
    objProducts = EngageboostChannelCurrencyProductPrice.objects.filter(product_id__in = product_lst,warehouse_id=warehouse_id)
    range_price = []
    if(objProducts.count()>0):
        min_price = objProducts.aggregate(Min('price'))['price__min']
        max_price = objProducts.aggregate(Max('price'))['price__max']

        currency = ""
        queryset=EngageboostGlobalSettings.objects.get(website_id=website_id)
        currency=EngageboostGlobalsettingCurrencies.objects.filter(global_setting_id=queryset.id).first()
        if(currency):
            currencyobj=EngageboostCurrencyMasters.objects.filter(id=currency.currency_id).first()
            if(currencyobj):
                currency = currencyobj.currencysymbol
        divide_by = 6
        max_price= 1000
        # diff_price = int(max_price)/divide_by
        diff_price = 10
        
        i=1
        for i in range(divide_by):
            rng = {}
            if i ==0:
                pass
            else:
                if i == 1:
                    if max_price < diff_price:
                        rng['min'] = 0
                        rng['max'] = diff_price
                        rng['name'] = "Less than " +str(currency)+str(diff_price)
                        range_price.append(rng)
                    else:
                        rng['min'] = 0
                        rng['max'] = diff_price
                        rng['name'] = str(currency)+str(0) +" to " +str(currency)+ str(10)
                        range_price.append(rng)
                else:
                    x1 = i-1
                    new_range = diff_price*x1
                    x = x1+1
                    rng1 = ""
                    if new_range < max_price:
                        if i<5:
                            rng['min'] = new_range+1
                            rng['max'] = diff_price*x
                            rng['name'] = str(currency)+str(new_range+1) +" to " +str(currency)+ str(diff_price*x)
                            range_price.append(rng)
                        else:
                            rng['min'] = new_range+1
                            rng['max'] = ""
                            rng['name'] = rng['name'] = "Above " +str(currency)+ str(new_range+1)
                            range_price.append(rng)
                    else:
                        rng['min'] = new_range+1
                        rng['max'] = ""
                        rng['name'] = rng['name'] = "Above " +str(currency)+ str(new_range+1)
                        range_price.append(rng)

            data.append({'field_name':'price','field_id':'channel_currency_product_price.price','is_variant':'false','is_static':'true','child': range_price})


# PriceFilter()