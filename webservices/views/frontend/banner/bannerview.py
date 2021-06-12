
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
import json
import sys,os
import traceback
from django.views.decorators.csrf import csrf_exempt
import datetime
from webservices.views.frontend.category.categoryview import * 
from webservices.views.frontend.product.productview import * 
from django.db.models import Count
from django.db.models import Q


@csrf_exempt
def BannerList(request):
	if request.method == 'POST':
		website_id = request.POST.get('website_id')
		category_banner_id = request.POST.getlist('category_banner_id[]')
		applicable_for = request.POST.get('applicable_for')
		banner_type = request.POST.get('banner_type') 
		
		try:
			if website_id is None:
				raise Exception("Website id is required")
			if len(category_banner_id)==0:
				raise Exception("category banner id is required")
			if applicable_for is None:
				raise Exception("applicable for is required")
			if banner_type is None:
				raise Exception("banner type is required")
					
			now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
			banner_qs = EngageboostCategoryBanners.objects.filter(id__in=category_banner_id,banner_type=banner_type,website_id=website_id,isdeleted='n', isblocked='n')
			
			bannerimage_qs = EngageboostCategoryBannersImages.objects.filter(category_banner_id__in=banner_qs,isdeleted='n', isblocked='n',applicable_for=applicable_for)
			if (banner_type=='H' and (applicable_for=='mobile' or applicable_for=='web')):
				#print('########################################')
				bannerimage_qs = bannerimage_qs.filter(start_date__lte=now_utc,end_date__gte=now_utc,applicable_for=applicable_for)
			bannerimage_qs = bannerimage_qs.all()
			
			bannerimage_data = CategoryBannersImagesNewSerializer(bannerimage_qs,many=True)
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
	return JsonResponse (data)


#######################################################for app###################################################
@csrf_exempt
def CmsContent(request):

	data 				= 	JSONParser().parse(request)
	company_website_id	=	data['company_website_id']
	lang				=	data['lang']
	template_id			=	data['template_id']
	page_id				=   data['page_id']
	start_limit     	=   data['start_limit']
	end_limit      		=   data['end_limit']
	warehouse_id 		=   data['warehouse_id']
	#category_id 		=   data['category_id']
	
	try:
		return_data =[]
		pages=EngageboostCmsPageSettings.objects.filter(company_website_id=company_website_id,lang=lang,temp_id=template_id,page_id=page_id).all()
		
		if end_limit == 0 and start_limit == 0:
			data['no_of_page'] = 1
			data['next_start_index'] = 0
			data['prev_start_index'] = 0  
		else:
			data['no_of_page'] = int(len(pages) / end_limit) if(int(len(pages) % end_limit) == 0) else int(len(pages) / end_limit) + 1
			data['next_start_index'] = start_limit if int(start_limit + end_limit) >= len(pages) else int(start_limit + end_limit)
			data['prev_start_index'] = start_limit if int(start_limit - end_limit) < 0 else int(start_limit - end_limit)
			data['total_number_row'] = len(pages)

		if end_limit != 0:
			pages = pages.order_by('-id')[int(start_limit):int(start_limit) + int(end_limit)]
		pagecount=pages.count()
		#print(pagecount)
		serializer_cms = CmsPageSettingsSerializer(pages,many=True)
		serializer_cms = serializer_cms.data
		if serializer_cms:
			widgets_data=[]
			properties =[]
			parent_category_list=[] 
			best_sell_product=[]
			deals_product = []
			product_by_category = []
			for serializercms in serializer_cms:
				widgets_id = serializercms['widgets']
				
				if(serializercms['widgets']== 24): 
					propertyvalue = serializercms['property_value']
					json_data = json.loads(propertyvalue)
					properties.append(json_data)
					
					widgets_data.append({"widgets_id":widgets_id,"properties":properties})

				if(serializercms['widgets']== 20):
					categorylist = Shop_By_Category(company_website_id)
					serializercms['categorylist']= categorylist
					widgets_data.append({"widgets_id":widgets_id,"parent_category_list":categorylist}) 

				# if(serializercms['widgets']== 25):
				# 	dealsproduct = Deals_Of_The_Day(company_website_id,warehouse_id)
				# 	serializercms['dealsproduct']= dealsproduct
				# 	print(str(dealsproduct.pop(2)) + " has been removed")
				# 	# print('++++++++++++++++++++++++++++++++++++++++++++++')
				# 	# print('+++++++++++=',dealsproduct)
				# 	widgets_data.append({"widgets_id":widgets_id,"deals_product":dealsproduct})

				if(serializercms['widgets']== 26):
					propertyvalue = serializercms['property_value']
					selling_product = Best_Selling_Product(company_website_id,warehouse_id)
					serializercms['selling_product']= selling_product
					widgets_data.append({"widgets_id":widgets_id,"best_sell_product":selling_product})

				

				# if(serializercms['widgets']== 19):
				# 	cat_product = Category_Product_ListView(category_id,warehouse_id,company_website_id)
				# 	serializercms['cat_product']= cat_product
				# 	widgets_data.append({"widgets_id":widgets_id,"product_by_category":cat_product})


			return_data.append({"total_widgets":pagecount, "widgets_data":widgets_data})
			data ={
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
                    sortby_lst = ['Popularity','New Arrivals','Price : High to Low','Price : Low to High']
                    for i in range(len(sortby_lst)):
                        sort_data = {}
                        sort_data['id'] = i+1
                        sort_data['name'] = sortby_lst[i]
                        data['sort_by'].append(sort_data)

                    data['breadcrumb'] = get_hierarchy(objCategory,website_id)
                    data['itemlisting_front'] = objGlobalsettings.itemlisting_front
                    data['category_id'] = objCategory.id
                    # else:
                    #     data['status'] = 0
                    #     data['message'] = 'Category banner not found.'
                else:
                    data = {
                            "status": 0,
                            "message": "Category not found."
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



@csrf_exempt
def CategoryBannerForHome(request):
	if request.method == 'POST':
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
	return JsonResponse (data)

@csrf_exempt
def CategoryBannerForPromotion(request):
	website_id = request.META.get('HTTP_WID')
	try:
		if website_id is None:
			raise Exception("Website id is required") 
		company_website_id = 1
		template_id = 1
		lang ="en"
		# pages=EngageboostCmsPageSettings.objects.filter(company_website_id=company_website_id,lang=lang,temp_id=template_id,page_id=9, widgets = 29).first()
		# serializer_cms = CmsPageSettingsSerializer(pages)
		# serializercms = serializer_cms.data
		# propertyvalue = serializercms['property_value']
		# json_data = json.loads(propertyvalue)
		# print(json_data['insertables'][0]['properties'])
		
		
		banner_promotion = EngageboostCategoryBanners.objects.filter(isdeleted='n', isblocked='n', website_id=website_id,banner_type='C').all().order_by('order_no')		
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
							#product_count = product_count + len(products_array)
							productlist=[]
							cat_list = discnt.all_category_id
							if cat_list:
								category_arr = cat_list.split(',')
								product_data = EngageboostProductCategories.objects.filter(category_id__in=category_arr,isdeleted='n', isblocked='n').values_list('product_id', flat=True)
								product_data = product_data.distinct()
								print(product_data)
								if product_data:
									for prodata in product_data:
										productlist.append(prodata)	
								product_count = product_count + len(product_data)
				discountdata["product_count"] = product_count
				# joinedproduct = products_array + productlist
				# totalproduct=list(set(joinedproduct))
				# print(totalproduct)
								

				#discountdata['product_count'] = product_count
		if banner_promotion_data:
			
			data = {
				"status":1,
				"data":banner_promotion_data
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
