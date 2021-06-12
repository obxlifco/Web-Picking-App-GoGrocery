
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
import datetime
import json
import sys,os
import traceback
from django.db.models import Max,Min,Q
# from webservices.views.order import Order as discount_details



@csrf_exempt
def BestSellingProduct(request):

	if request.method == 'POST':
		warehouse_id = request.POST.get('warehouse_id') 
		data = {"status" : 0,"msg" : "something went wrong"}
		website_id = request.POST.get('website_id')
		try:
			if warehouse_id is None:  
				raise Exception("warehouse id is required") 
			if website_id is None:
				raise Exception("website id is required") 
			selling_product = EngageboostProducts.objects.filter(isdeleted='n', isblocked='n', website_id=website_id,numberof_sale__gt=0).all().order_by('-numberof_sale')
			
			sellingproduct_data = ProductSerializer(selling_product, context={'warehouse_id': warehouse_id},many=True)
			sellingproduct_data = sellingproduct_data.data
			
			for crossproduct in sellingproduct_data:
				variant_product =[]
				crossrroductresult =[] 
				cross_productArr = []
				
				qs = EngageboostCossSellProducts.objects.filter(product_id=crossproduct['id']).all()
				
				if qs:
					for qsprod in qs:
						cross_productArr.append(qsprod.cross_product_id)
					
				if len(cross_productArr)>0:
					qscrossprod = EngageboostProducts.objects.filter(id__in=cross_productArr,isdeleted='n', isblocked='n',website_id=website_id).all()

					if qscrossprod:
						crossrroductresult = ProductSerializer(qscrossprod, context={'warehouse_id': warehouse_id},many=True).data
						variant_product.append(crossrroductresult)
						for crossbrand in crossrroductresult:
							qs_brand = EngageboostBrandMasters.objects.filter(id=crossbrand['brand'], isblocked='n', isdeleted='n').first()
							brand_data = BrandMastersSerializer(qs_brand)
							crossbrand.update({'brand':brand_data.data})
				crossproduct.update({'variant_product':crossrroductresult})
				qs_brand = EngageboostBrandMasters.objects.filter(id=crossproduct['brand'], isblocked='n', isdeleted='n').first()
				brand_data = BrandMastersSerializer(qs_brand)
				crossproduct.update({'brand':brand_data.data})

			
			if sellingproduct_data:

				data = {
				"status":1,
				"data":sellingproduct_data 
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


def Best_Selling_Product(website_id,warehouse_id):
	
	selling_product = EngageboostProducts.objects.filter(isdeleted='n', isblocked='n', website_id=website_id,numberof_sale__gt=0).all().order_by('-numberof_sale')
	sellingproduct_data = ProductSerializer(selling_product, context={'warehouse_id': warehouse_id},many=True)
	sellingproduct_data = sellingproduct_data.data
	if sellingproduct_data:

		for crossproduct in sellingproduct_data:
			variant_product =[]
			crossrroductresult =[]
			cross_productArr = []
			qs = EngageboostCossSellProducts.objects.filter(product_id=crossproduct['id']).all()
			
			if qs:
				for qsprod in qs:
					cross_productArr.append(qsprod.cross_product_id)
				
			if len(cross_productArr)>0:
				qscrossprod = EngageboostProducts.objects.filter(id__in=cross_productArr,isdeleted='n', isblocked='n',website_id=website_id).all()

				if qscrossprod:
					crossrroductresult = ProductSerializer(qscrossprod,context={'warehouse_id': warehouse_id},many=True).data
					variant_product.append(crossrroductresult)
					for crossbrand in crossrroductresult:
						qs_brand = EngageboostBrandMasters.objects.filter(id=crossbrand['brand'], isblocked='n', isdeleted='n').first()
						brand_data = BrandMastersSerializer(qs_brand)
						crossbrand.update({'brand':brand_data.data})
			crossproduct.update({'variant_product':crossrroductresult})
			qs_brand = EngageboostBrandMasters.objects.filter(id=crossproduct['brand'], isblocked='n', isdeleted='n').first()
			brand_data = BrandMastersSerializer(qs_brand)
			crossproduct.update({'brand':brand_data.data})
	return sellingproduct_data


@csrf_exempt
def DealsOfTheDay(request):

	if request.method == 'POST':
		warehouse_id = request.POST.get('warehouse_id') 
		#data = {"status" : 0,"msg" : "something went wrong"}
		website_id = request.POST.get('website_id')
		try:
			if warehouse_id is None:  
				raise Exception("warehouse id is required") 
			if website_id is None:
				raise Exception("website id is required") 

			now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
			
			deal_disc_master = EngageboostDiscountMasters.objects.filter(isdeleted='n', isblocked='n',website_id=website_id,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc,offer_type='Todays Offers').all().filter( Q(warehouse_id__startswith=warehouse_id+',') | Q(warehouse_id__endswith=','+warehouse_id) | Q(warehouse_id__contains=',{0},'.format(warehouse_id)) | Q(warehouse_id__exact=warehouse_id) ).values_list('id', flat=True)
			
			dis_master_condition = EngageboostDiscountMastersConditions.objects.filter(discount_master_id=deal_disc_master,isdeleted='n', isblocked='n')

			if dis_master_condition:
				for discnt in dis_master_condition:
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
						if product_data:
							for prodata in product_data:
								productlist.append(prodata)
						
				joinedproduct = products_array + productlist
				totalproduct=list(set(joinedproduct))
				productresult= EngageboostProducts.objects.filter(isdeleted='n', isblocked='n', website_id=website_id,id__in=totalproduct).all()
				productresult_data = ProductSerializer(productresult, context={'warehouse_id': warehouse_id},many=True)
				productresult_data = productresult_data.data
				for crossproduct in productresult_data:
					variant_product =[]
					crossrroductresult =[]
					cross_productArr = []
					brand ={}
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
								qs_brand = EngageboostBrandMasters.objects.filter(id=crossbrand['brand'], isblocked='n', isdeleted='n').first()
								brand_data = BrandMastersSerializer(qs_brand)
								crossbrand.update({'brand':brand_data.data})

					crossproduct.update({'variant_product':crossrroductresult})
					qs_brand = EngageboostBrandMasters.objects.filter(id=crossproduct['brand'], isblocked='n', isdeleted='n').first()
					brand_data = BrandMastersSerializer(qs_brand)
					crossproduct.update({'brand':brand_data.data})
			
				if productresult_data:
					data = {
					"status":1,
					"data":productresult_data
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
	
def Deals_Of_The_Day(website_id,warehouse_id):
	now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
			
	deal_disc_master = EngageboostDiscountMasters.objects.filter(isdeleted='n', isblocked='n',website_id=website_id,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc,offer_type='Todays Offers').all().filter( Q(warehouse_id__startswith=warehouse_id+',') | Q(warehouse_id__endswith=','+warehouse_id) | Q(warehouse_id__contains=',{0},'.format(warehouse_id)) | Q(warehouse_id__exact=warehouse_id) ).values_list('id', flat=True)

	dis_master_condition = EngageboostDiscountMastersConditions.objects.filter(discount_master_id=deal_disc_master,isdeleted='n', isblocked='n')

	if dis_master_condition:
		for discnt in dis_master_condition:
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
				if product_data:
					for prodata in product_data:
						productlist.append(prodata)
				
		joinedproduct = products_array + productlist
		totalproduct=list(set(joinedproduct))
		productresult= EngageboostProducts.objects.filter(isdeleted='n', isblocked='n', website_id=website_id,id__in=totalproduct).all()
		productresult_data = ProductSerializer(productresult, context={'warehouse_id': warehouse_id},many=True)
		productresult_data = productresult_data.data
		for crossproduct in productresult_data:
			variant_product =[]
			crossrroductresult =[]
			cross_productArr = []
			brand ={}
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
						qs_brand = EngageboostBrandMasters.objects.filter(id=crossbrand['brand'], isblocked='n', isdeleted='n').first()
						brand_data = BrandMastersSerializer(qs_brand)
						crossbrand.update({'brand':brand_data.data})

			crossproduct.update({'variant_product':crossrroductresult})
			qs_brand = EngageboostBrandMasters.objects.filter(id=crossproduct['brand'], isblocked='n', isdeleted='n').first()
			brand_data = BrandMastersSerializer(qs_brand)
			crossproduct.update({'brand':brand_data.data})	
	return productresult_data
	
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

def Category_Product_ListView(category_id,warehouse_id,website_id):
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

@csrf_exempt
def listing_filters(request):
	""" Listing filter for listin module """
	if(request.method == "GET"):
		data = []
		try:
			warehouse_id = request.GET.get('warehouse_id', 4)
			slug = request.GET['slug']
			website_id = request.GET.get('website_id', 1)
			cnt = EngageboostCategoryMasters.objects \
			.filter(
				slug=slug,
				isdeleted='n',
				isblocked='n').count()

			if(cnt > 0):
				objcat = EngageboostCategoryMasters.objects \
				.get(
					slug=slug,
					isdeleted='n',
					isblocked='n')
				category_id = objcat.id
				#objwarehouse_cnt = EngageboostCategoryWarehouse.objects.filter(category_id=category_id, warehouse_id=warehouse_id).count()
				#print(objwarehouse_cnt)
				#if(objwarehouse_cnt!=0):
				serializer_data = EngageboostCategoryMasters.objects \
						.filter(
							parent_id=category_id,
							isdeleted='n',
							isblocked='n').order_by('id')
				lst_cat = serializer_data.values_list("id",flat=True)

				#lst_cat = EngageboostCategoryWarehouse.objects.filter(category_id__in=lst_cat, warehouse_id=warehouse_id).values_list("category_id",flat=True)
				if(lst_cat):
					lst_cat = list(lst_cat)
					lst_cat.append(category_id)
				else:
					lst_cat = [category_id]
				context = {"warehouse_id": warehouse_id}
				categories_data = EngageboostCategoriesSerializer(serializer_data, many=True,context=context).data
				data.append({'field_name': 'categories','field_id':'category_id.id','is_variant':'false','is_static':'true','child':categories_data})
				product_lst = EngageboostProductCategories.objects.filter(category_id__in=lst_cat,product__isblocked='n',product__isdeleted='n', isblocked='n', isdeleted='n').values_list('product_id',flat=True)
				if(product_lst):
					#product_lst = EngageboostWarehouseSupplierMappings.objects.filter(product_id__in = list(product_lst)).distinct().values_list('product_id',flat=True)
					#objPricetype = EngageboostPriceTypeMaster.objects.get(name='Regular Price', isblocked='n', isdeleted='n')
					#objproductpricetype = EngageboostProductPriceTypeMaster.objects.filter(price_type_id = objPricetype.id,product_id__in = product_lst).values_list('id',flat=True)
					product_lst = EngageboostProductStocks.objects.filter(warehouse_id=warehouse_id,product_id__in = product_lst,product__isblocked='n',product__isdeleted='n', isblocked='n', isdeleted='n').values_list('product_id',flat=True)
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
							divide_by = 4
							#max_price= 1000
							diff_price = int(max_price)/divide_by
							if(diff_price <= 50):
								rng={}
								rng['min'] = min_price
								rng['max'] =max_price
								if(currency!=""):
									rng['name'] = str(currency)+str(min_price) +" to " +str(currency)+ str(max_price)
								else:
									rng['name'] = str(min_price) +" to " + str(max_price)
								range_price.append(rng)
							else:
								rng={}
								new_price = min_price
								for j in range(divide_by):
									rng={}
									if(j==0):
										rng['min'] = 0
										rng['max'] = diff_price
										if(currency!=""):
											rng['name'] = "Less than " +str(currency)+str(diff_price)
										else:
											rng['name'] = "Less than " + str(diff_price)
									elif(j+1==divide_by):
										rng['min'] =new_price
										rng['max'] = None
										if(currency!=""):
											rng['name'] = "Above " +str(currency)+ str(new_price)
										else:
											rng['name'] = "Above " + str(new_price)
									else:
										rng['min'] = new_price
										rng['max'] = new_price+diff_price
										if(currency!=""):
											rng['name'] = str(currency)+str(new_price) +" to " + str(currency)+str(new_price+diff_price)
										else:
											rng['name'] = str(new_price) +" to " + str(new_price+diff_price)
									new_price = new_price + diff_price
									range_price.append(rng)

						data.append({'field_name':'price','field_id':'channel_currency_product_price.price','is_variant':'false','is_static':'true','child': range_price})
						product_lst = EngageboostChannelCurrencyProductPrice.objects.filter(product_id__in = product_lst,warehouse_id=warehouse_id).distinct().values_list('product_id',flat=True)
					
						brand_list = EngageboostProducts.objects.filter(isblocked='n', isdeleted='n',id__in = product_lst,warehouse_id=warehouse_id).distinct('brand').values_list('brand',flat=True)
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
						data.append({'field_name':'brand','field_id':'brand_id','is_variant':'false','is_static':'false','child': brand_data})

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
						#discount_data=[]
						# if(product_lst):
						#     discount_array = discount_details.generate_discount_conditions(website_id,None)
						#     discnt_lst = []
						#     discount_data = []
						#     if(discount_array):
						#         exclude_ids = []
						#         for discount_n in discount_array:
						#             for product_id in product_lst:
						#                 if(product_id not in exclude_ids):
						#                     getproduct = discount_details.getproduct_data(product_id)
						#                     if(getproduct):
						#                         getproduct["qty"]=getproduct['quantity']
						#                         try:
						#                             if getproduct["new_default_price"]: getproduct["new_default_price"] = getproduct["new_default_price"]
						#                             else: getproduct["new_default_price"] = getproduct["default_price"]
						#                         except KeyError: getproduct["new_default_price"] = getproduct["default_price"]
											
						#                         out_flag = discount_details.check_in_prod_disc(None,getproduct,discount_n,None)
						#                         if(out_flag == 'true'):
						#                             discnt_lst.append(discount_n['id'])
						#                             exclude_ids.append(product_id)
						#         now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
						#         obj_discount_lst = EngageboostDiscountMasters.objects.filter(id__in =discnt_lst,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc, isblocked='n', isdeleted='n').all()

						#         discount_data = EngageboostDiscountMastersSerializer(obj_discount_lst, many=True).data
						#data.append({'field_name':'discount','field_id':'id','is_variant':'false','is_static':'false','child': discount_data})
					else:
						data = [{
						    "status": 0,
						    "message": "Product not found."
						}]
					
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
					
		except Exception as ex:
			import sys,os
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			data = []
	else:
		data = [{
			"status": 0,
			"message": "invalid request"
		}]
		
	return JsonResponse(data, safe=False)   

