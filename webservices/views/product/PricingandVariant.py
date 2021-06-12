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
from django.db.models import Q
import tinys3
from django.core.files.storage import FileSystemStorage
import json
from webservices.views import loginview
import requests
import random
import string
# add dufalt Product price 
class Productpricingadd(generics.ListAPIView):
	def post(self, request,format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		website_id=request.data['website_id']
		currencymain_slug=[]
		channelmain_slug=[]
		queryset=EngageboostGlobalSettings.objects.using(company_db).get(website_id=website_id)
		currency=EngageboostGlobalsettingCurrencies.objects.using(company_db).filter(global_setting_id=queryset.id)
		channel=EngageboostWebsiteChannels.objects.using(company_db).all().filter(engageboost_company_website_id=website_id)
		for channel1 in channel:
			chennelname=EngageboostChannels.objects.using(company_db).filter()
		for chennel_name in chennelname:
			d3={"channel_id":chennel_name.id,"channel_name":chennel_name.name}
			channelmain_slug.append(d3)
		for currency_id in currency:
			currency_name=EngageboostCurrencyMasters.objects.using(company_db).filter(id=currency_id.currency_id)
			for currencyname in currency_name:
				d2={"currency_id":currencyname.id,"currency_name":currencyname.currencyname}
				currencymain_slug.append(d2)	
			
		data2 ={
				'currency':currencymain_slug,
				'channel':channelmain_slug
				}
		return Response(data2)
# set dufalt Product price	
class ProductpriceSet(generics.ListAPIView):	
	def post(self, request,format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		js=request.data
		ourResult1 = js['data']
		for data in ourResult1:
			queryset=EngageboostChannelCurrencyProductPrice.objects.using(company_db).create(channel_id=data['channel_id'],currency_id=data['currency_id'],product_id=data['product_id'],price=data['price'])
			data ={
					'status':1,
					'message':'Successfully Inserted'
					
					}
		return Response(data)
# Class  ProductpriceSetView is used to show channels with price and variants
class ProductpriceSetView(generics.ListAPIView):
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostChannelCurrencyProductPrice.objects.using(company_db).get(pk=pk)
		except EngageboostChannelCurrencyProductPrice.DoesNotExist:
			raise Http404	
	def get(self, request, pk,website_id, format=None):
		company_db = loginview.db_active_connection(request)
		currencymain_slug=[]
		channelmain_slug=[]
		values=[]
		fields=[]
		channel_values=[]
		cross_sale_products=[]
		
		parentdata={}
		final_data=[]
			
		varientproduct={}
		
		cross_sale_product=EngageboostCossSellProducts.objects.using(company_db).all().filter(product_id=pk)
		for cross_sale in cross_sale_product:	
			cross_sale_products.append(cross_sale.cross_product_id)
		products_cross_sale=EngageboostProducts.objects.using(company_db).all().filter(id__in=cross_sale_products).filter(isdeleted='n',isblocked='n')
		products_varient=BasicinfoSerializer(products_cross_sale,many=True)
		products_details=EngageboostProducts.objects.using(company_db).all().filter(id=pk)
		queryset=EngageboostGlobalSettings.objects.using(company_db).get(website_id=website_id)
		products_details=EngageboostProducts.objects.using(company_db).all().filter(id=pk)
		products_detail=BasicinfoSerializer(products_details,many=True)
		currency=EngageboostGlobalsettingCurrencies.objects.using(company_db).filter(global_setting_id=queryset.id)
		

				
		basecurrency=EngageboostCurrencyRates.objects.get(isbasecurrency='y')	
		chennelname=EngageboostChannels.objects.using(company_db).filter(isdeleted='n')
		for chennel_name in chennelname:

			fetchCurrency=EngageboostWebsiteChannels.objects.using(company_db).filter(engageboost_channel_id=chennel_name.id).first()
			if fetchCurrency:			
				if chennel_name.id==fetchCurrency.engageboost_channel_id:
					productswebstoreCount=EngageboostChannelCurrencyProductPrice.objects.using(company_db).filter(product_id=pk,currency_id=fetchCurrency.currency_id,channel_id=chennel_name.id).count()
					if productswebstoreCount>0:
						productswebstore=EngageboostChannelCurrencyProductPrice.objects.using(company_db).filter(product_id=pk,currency_id=fetchCurrency.currency_id,channel_id=chennel_name.id).order_by('-id').first()
						d3={"basecurrency":'y',"channel_name":chennel_name.name,"channel_id":chennel_name.id,"currency_id":fetchCurrency.currency_id,"product_id":pk,"price":productswebstore.price}
					else:

						d3={"basecurrency":'y',"channel_name":chennel_name.name,"channel_id":chennel_name.id,"currency_id":fetchCurrency.currency_id,"product_id":pk,"price":''}
				else:
					d3={"basecurrency":'y',"channel_name":chennel_name.name,"channel_id":chennel_name.id,"currency_id":fetchCurrency.currency_id,"product_id":pk,"price":''}
				channelmain_slug.append(d3)
			
		product_category = EngageboostProductCategories.objects.using(company_db).get(product_id=pk,is_parent='y')
		channel_id='6'
		custom=EngageboostDefaultModuleLayoutFields.objects.using(company_db).all().filter(category_id=product_category.category_id,is_system='y').filter( Q(show_market_places__startswith=channel_id+',') | Q(show_market_places__endswith=','+channel_id) | Q(show_market_places__contains=',{0},'.format(channel_id)) | Q(show_market_places__exact=channel_id) )
		for field in custom:

			custom_fields=EngageboostDefaultsFields.objects.using(company_db).all().filter(id=field.field_id,is_variant='Yes')
			for custom_field in custom_fields:
				fields.append(custom_field.id)	
		custom_isvariant=EngageboostDefaultModuleLayoutFields.objects.using(company_db).all().filter(category_id=product_category.category_id,field_id__in=fields)
		serializer_custom = DefaultModuleLayoutFieldsSerializer(custom_isvariant,many=True)
		product_custom = EngageboostMarketplaceFieldValue.objects.using(company_db).all().filter(product_id=pk)
		serializer_productcustom = MarketplaceFieldValueSerializer(product_custom,many=True)
		for currency_id in currency:
			currency_name=EngageboostCurrencyRates.objects.using(company_db).filter(engageboost_currency_master_id=currency_id.currency_id,engageboost_company_website_id=1)
			currency_Symbol=EngageboostCurrencyMasters.objects.using(company_db).filter(id=currency_id.currency_id)
			for currency_Symbols in currency_Symbol:
				for currencyname in currency_name:
					d2={"currency_id":currencyname.engageboost_currency_master_id,"currency_name":currencyname.currency_code,"currency_exchange_rate":currencyname.exchange_rate,"isbasecurrency":currencyname.isbasecurrency,"currency_symbol":currency_Symbols.currencysymbol}
					currencymain_slug.append(d2)
		cnt=EngageboostChannelCurrencyProductPrice.objects.using(company_db).filter(product_id=pk).count()		
		if cnt>0:
			products=EngageboostChannelCurrencyProductPrice.objects.using(company_db).all().filter(product_id=pk).filter(channel_id=6)	
			basecurrency=EngageboostCurrencyRates.objects.get(isbasecurrency='y')
			for product in products:
				
				basecurrencyid=basecurrency.engageboost_currency_master_id
				if basecurrencyid==product.currency_id:
					d4={"basecurrency":'y',"channel_id":product.channel_id,"currency_id":product.currency_id,"product_id":product.product_id,"price":product.price}
				else:
					d4={"basecurrency":'n',"channel_id":product.channel_id,"currency_id":product.currency_id,"product_id":product.product_id,"price":product.price}
				values.append(d4)
			productsid=EngageboostChannelCurrencyProductPrice.objects.using(company_db).all().filter(product_id__in=cross_sale_products).filter(channel_id=6)	
			for productids in productsid:
				basecurrencyid=basecurrency.engageboost_currency_master_id
				if basecurrencyid==product.currency_id:
					d5={"basecurrency":'y',"channel_id":productids.channel_id,"currency_id":productids.currency_id,"product_id":productids.product_id,"price":productids.price}
				else:
					d5={"basecurrency":'n',"channel_id":productids.channel_id,"currency_id":productids.currency_id,"product_id":productids.product_id,"price":productids.price}
				channel_values.append(d5)
		# varientproduct['variant_product']=products_varient.data
		
		final_data=[]
		for vProduct in products_varient.data:
			channel_varient=[]
			custom_varient=[]
			customs={}
			varientproduct={}
			
			# print(vProduct['id'])
			product_img_count=EngageboostProductimages.objects.using(company_db).filter(product_id=vProduct['id'],is_cover=1).count()
			if product_img_count>0: 
				product_img=EngageboostProductimages.objects.using(company_db).filter(product_id=vProduct['id'],is_cover=1).order_by('-id').first()
				vProduct['img']=product_img.img	
				vProduct['imgid']=product_img.id
				vProduct['img_alt']=product_img.img_alt
				vProduct['img_title']=product_img.img_title
			else:
				vProduct['img']=''
			#varient Product id
			basecurrency=EngageboostCurrencyRates.objects.get(isbasecurrency='y')	
			chennelname=EngageboostChannels.objects.using(company_db).filter(isdeleted='n')
			for chennel_name in chennelname:

				fetchCurrency=EngageboostWebsiteChannels.objects.using(company_db).filter(engageboost_channel_id=chennel_name.id).first()
				if fetchCurrency:
					if chennel_name.id==fetchCurrency.engageboost_channel_id:
						# print(vProduct['id'])
						productswebstoreCount=EngageboostChannelCurrencyProductPrice.objects.using(company_db).filter(product_id=vProduct['id'],currency_id=fetchCurrency.currency_id,channel_id=chennel_name.id).count()
						if productswebstoreCount>0:
							productswebstore=EngageboostChannelCurrencyProductPrice.objects.using(company_db).get(product_id=vProduct['id'],currency_id=fetchCurrency.currency_id,channel_id=chennel_name.id)
							d3={"basecurrency":'y',"channel_name":chennel_name.name,"channel_id":chennel_name.id,"currency_id":fetchCurrency.currency_id,"product_id":vProduct['id'],"price":productswebstore.price}
						else:

							d3={"basecurrency":'y',"channel_name":chennel_name.name,"channel_id":chennel_name.id,"currency_id":fetchCurrency.currency_id,"product_id":vProduct['id'],"price":''}
					else:
						d3={"basecurrency":'y',"channel_name":chennel_name.name,"channel_id":chennel_name.id,"currency_id":fetchCurrency.currency_id,"product_id":vProduct['id'],"price":''}
				
					channel_varient.append(d3)	
			for serializer_customs in serializer_custom.data:

				# serializer_customs['value']=''

				marketplaceCount=EngageboostMarketplaceFieldValue.objects.using(company_db).filter(field_id=serializer_customs['field_id'],product_id=vProduct['id']).count()
				if marketplaceCount>0:
					marketplace=EngageboostMarketplaceFieldValue.objects.using(company_db).get(field_id=serializer_customs['field_id'],product_id=vProduct['id'])
					customs['value']=marketplace.value
					d2={"value":customs['value'],"CustomData":serializer_customs}						
					
					
				else:
					d2={"value":'',"CustomData":serializer_customs}	
				
				custom_varient.append(d2)

				
			varientproduct['products_varient']=vProduct
			varientproduct['channel_varient']=channel_varient
			varientproduct['custom_data_varient']=custom_varient
			final_data.append(varientproduct)
			# print(final_data)			
		data2 ={
		'currency':currencymain_slug,
		'custom_data':serializer_custom.data,
		'channel':channelmain_slug,
		'CurrencyProductPrice':values,
		'products':products_detail.data,
		'variant_product':final_data,
		'CurrencyProductPriceVariant':channel_values,
		# 'marketplace_values':marketplace_values.data,
		# 'channel_varient':channel_varient			
		}
		return Response(data2)
		# return HttpResponse(json.dumps({'variant_product':final_data}), content_type='application/json')

	# Update Variant products with price slug marketplace
	def put(self, request, pk,website_id, format=None):
		import random
		import string
		company_db = loginview.db_active_connection(request)
		EngageboostChannelCurrencyProductPrice.objects.using(company_db).filter(product_id=pk).delete()
		EngageboostMarketplaceFieldValue.objects.using(company_db).filter(product_id=pk).delete()
		# EngageboostCossSellProducts.objects.using(company_db).filter(product_id=pk).delete()
		imageresizeon= EngageboostGlobalSettings.objects.using(company_db).get(website_id=1)
		dataRequest=request.data['data']
		dataJson = dataRequest
		default_price=dataJson['default_price']
		product_id=dataJson['product']['id']
		varient=dataJson['varient']
		url=dataJson['product']['url']
		cnt_url_suffix = EngageboostProducts.objects.using(company_db).filter(url=url).count()
		if cnt_url_suffix !=0:
			
			count_value=url_post(company_db,url,count_value=cnt_url_suffix)
			main_url=url+str(count_value)
		else:
			main_url=url
		slug=dataJson['product']['slug']
		cnt_slug_suffix = EngageboostProducts.objects.using(company_db).filter(slug=slug).count()
		if cnt_slug_suffix !=0:
			count_value=slug_post(company_db,slug,count_value=cnt_slug_suffix)
			main_slug=slug+str(count_value)
			
		else:
			main_slug=slug
		EngageboostProducts.objects.using(company_db).all().filter(id=product_id).update(default_price=default_price)
		channel=dataJson['channel']
		arr_sku=[]
		
		for channels in channel:
			if(channels['price']):
				EngageboostChannelCurrencyProductPrice.objects.using(company_db).create(channel_id=channels['channel_id'],currency_id=channels['currency_id'],product_id=pk,price=channels['price'],website_id=channels['website_id'],warehouse_id=channels['warehouse_id'],price_type_id=channels['price_type_id'])
		
		if len(varient)>0:
			index=0	
			for varients in varient:
				index=index+1
				sku=varients['sku']
				default_price=varients['default_price']
				visibility=varients['visibility']
				
				varient_id=varients['variation_id']
				# keylist = [random.choice(string.ascii_letters + string.digits) for n in range(32)]
				# random = "".join(keylist)
				rand = str(random.randint(1,9999999))
				if varient_id==0:
					
					cnt = EngageboostProducts.objects.using(company_db).filter(sku=sku).filter(isdeleted='n').count()
					if cnt ==0:
						d1={'url':main_url,'slug':main_slug,'sku':sku,'default_price':default_price,'visibility_id':visibility,'order_id':0,"numberof_sale":0,"numberof_view":0,"ebay":0,"amazon":0,"webshop":1,"order_price":1, "isblocked":'n'}
						
						d2=dataJson['product']
						serializer_data=dict(d2,**d1)
						serializer = BasicinfoSerializer(data=serializer_data,partial=True)
						if serializer.is_valid():
							serializer.save()
							obj = EngageboostProducts.objects.using(company_db).latest('id')
							last_id = obj.id
							from PIL import Image
							import os
							import urllib.request
							
							if 'cover_image'+str(index) in request.FILES:
								file1 = request.FILES['cover_image'+str(index)]
								image_name=file1.name
								ext = image_name.split('.')[-1]
								# new_image_name='CoverImage_'+main_slug
								new_image_name='CoverImage_'+rand
								cover_image=new_image_name+'.'+ext
								fs=FileSystemStorage()
								filename = fs.save('product/200x200/'+new_image_name+'.'+ext, file1)
								uploaded_file_url = fs.url(filename)
								image = Image.open(settings.BASE_DIR+uploaded_file_url)
								width_origenal, height_origenal=image.size
								ImageResize(width_origenal,height_origenal,imageresizeon,cover_image)
								for channel in varients['channels']:
									EngageboostChannelCurrencyProductPrice.objects.using(company_db).create(channel_id=channel['channel_id'],currency_id=channel['currency_id'],product_id=varient_id,price=channel['price'],website_id=channel['website_id'],warehouse_id=channel['warehouse_id'],price_type_id=channel['price_type_id'])
								has_record = EngageboostProductimages.objects.using(company_db).filter(product_id=last_id).count()
								if has_record>0:
									EngageboostProductimages.objects.using(company_db).filter(product_id=last_id).update(is_cover=0)
									EngageboostProductimages.objects.using(company_db).create(product_id=last_id,created=datetime.now().date(),modified=datetime.now().date(),img=cover_image,is_cover=1,img_alt=varients['img_alt'],img_title=varients['img_title'],img_order=1)
								else:
									EngageboostProductimages.objects.using(company_db).create(product_id=last_id,created=datetime.now().date(),modified=datetime.now().date(),img=cover_image,is_cover=1,img_alt=varients['img_alt'],img_title=varients['img_title'],img_order=1)

							elif (request.data['cover_url'+str(index)]):
								file1 = request.data['cover_url'+str(index)]
								extrev=file1[::-1]
								extrevore = extrev.split(".")
								ext=extrevore[0][::-1]
								img=urllib.request.urlretrieve(file1, 'media/product/200x200/'+'CoverImage_'+rand+'.'+ext)
								cover_image='CoverImage_'+rand+'.'+ext
								fs=FileSystemStorage()
								BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
								uploaded_file_url = fs.url(img)
								
								# Banner 200x200
								image = Image.open(settings.BASE_DIR+'/media/product/200x200/'+cover_image)
								width_origenal, height_origenal=image.size
								ImageResize(width_origenal,height_origenal,imageresizeon,cover_image)
								for channel in varients['channels']:
									EngageboostChannelCurrencyProductPrice.objects.using(company_db).create(channel_id=channel['channel_id'],currency_id=channel['currency_id'],product_id=varient_id,price=channel['price'],website_id=channel['website_id'],warehouse_id=channel['warehouse_id'],price_type_id=channel['price_type_id'])
								has_record = EngageboostProductimages.objects.using(company_db).filter(product_id=last_id).count()
								if has_record>0:
									EngageboostProductimages.objects.using(company_db).filter(product_id=last_id).update(is_cover=0)
									EngageboostProductimages.objects.using(company_db).create(product_id=last_id,created=datetime.now().date(),modified=datetime.now().date(),img=cover_image,is_cover=1,img_alt=varients['img_alt'],img_title=varients['img_title'],img_order=1)
								else:
									EngageboostProductimages.objects.using(company_db).create(product_id=last_id,created=datetime.now().date(),modified=datetime.now().date(),img=cover_image,is_cover=1,img_alt=varients['img_alt'],img_title=varients['img_title'],img_order=1)								
								
							else:
								cover_image=''
								pass
								# EngageboostCossSellProducts.objects.using(company_db).create(product_id=pk,cross_product_id=last_id)
								# products_category=EngageboostProductCategories.objects.using(company_db).all().filter(product_id=pk)	
								# for cat in products_category:
								# 	obj = EngageboostProducts.objects.using(company_db).latest('id')
								# 	lastcat_id = obj.id
								# 	category_id=cat.category_id
								# 	is_parent=cat.is_parent
								# 	objcat=EngageboostProductCategories.objects.using(company_db).create(product_id=last_id,category_id=category_id,is_parent=is_parent)
								# 	serializer2 = ProductCategoriesSerializer(objcat,data=serializer_data,partial=True)
								# 	if serializer2.is_valid():
								# 		serializer2.save()
								# if len(varients['custom'])>0:
								# 	for custom_field in varients['custom']:
								# 		field_id=custom_field['field_id']
								# 		field_label_symbol_change=custom_field['field_label']
								# 		field_label_name=field_label_symbol_change.replace(" ","_")
								# 		field_label=field_label_name.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~=+"})
								# 		field_name=custom_field['field_name']
								# 		value=custom_field['value']
								# 		MarketplaceFieldLabels=EngageboostMarketplaceFieldValue.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=field_id,field_label=field_label,field_name=field_name,value=value,website_id=website_id,channel_id=6,product_id=last_id)
								# if len(varients['channels'])>0:	
								# 	for channel in varients['channels']:
								# 		EngageboostChannelCurrencyProductPrice.objects.using(company_db).create(channel_id=channel['channel_id'],currency_id=channel['currency_id'],product_id=lastcat_id,price=channel['price'])

								# has_record = EngageboostProductimages.objects.using(company_db).filter(product_id=lastcat_id).count()
								# if has_record>0:
								# 	EngageboostProductimages.objects.using(company_db).filter(product_id=lastcat_id).update(is_cover=0)
								# 	EngageboostProductimages.objects.using(company_db).create(product_id=lastcat_id,created=datetime.now().date(),modified=datetime.now().date(),img=varients['img'],is_cover=1,img_alt=varients['img_alt'],img_title=varients['img_title'],img_order=1)
								# else:
								# 	EngageboostProductimages.objects.using(company_db).create(product_id=lastcat_id,created=datetime.now().date(),modified=datetime.now().date(),img=varients['img'],is_cover=1,img_alt=varients['img_alt'],img_title=varients['img_title'],img_order=1)

							EngageboostCossSellProducts.objects.using(company_db).create(product_id=pk,cross_product_id=last_id)
							products_category=EngageboostProductCategories.objects.using(company_db).all().filter(product_id=pk)	
							for cat in products_category:
								obj = EngageboostProducts.objects.using(company_db).latest('id')
								lastcat_id = obj.id
								category_id=cat.category_id
								is_parent=cat.is_parent
								print(category_id)
								print(serializer_data)
								objcat=EngageboostProductCategories.objects.using(company_db).create(product_id=last_id,category_id=category_id,is_parent=is_parent)
								serializer2 = ProductCategoriesSerializer(objcat,data=serializer_data,partial=True)
								print(serializer2)
								if serializer2.is_valid():
									serializer2.save()
							if len(varients['custom'])>0:
								for custom_field in varients['custom']:
									field_id=custom_field['field_id']
									field_label_symbol_change=custom_field['field_label']
									field_label_name=field_label_symbol_change.replace(" ","_")
									field_label=field_label_name.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~=+"})
									field_name=custom_field['field_name']
									value=custom_field['value']
									MarketplaceFieldLabels=EngageboostMarketplaceFieldValue.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=field_id,field_label=field_label,field_name=field_name,value=value,website_id=website_id,channel_id=6,product_id=last_id)
							if len(varients['channels'])>0:	
								for channel in varients['channels']:
									EngageboostChannelCurrencyProductPrice.objects.using(company_db).create(channel_id=channel['channel_id'],currency_id=channel['currency_id'],product_id=lastcat_id,price=channel['price'],website_id=channel['website_id'],warehouse_id=channel['warehouse_id'],price_type_id=channel['price_type_id'])

							has_record = EngageboostProductimages.objects.using(company_db).filter(product_id=lastcat_id).count()
							if has_record>0:
								EngageboostProductimages.objects.using(company_db).filter(product_id=lastcat_id).update(is_cover=0)
								EngageboostProductimages.objects.using(company_db).create(product_id=lastcat_id,created=datetime.now().date(),modified=datetime.now().date(),img=varients['img'],is_cover=1,img_alt=varients['img_alt'],img_title=varients['img_title'],img_order=1)
							else:
								EngageboostProductimages.objects.using(company_db).create(product_id=lastcat_id,created=datetime.now().date(),modified=datetime.now().date(),img=varients['img'],is_cover=1,img_alt=varients['img_alt'],img_title=varients['img_title'],img_order=1)	
						data2 ={
						'status':1,
						'message':'Inserted Successfully'
						
						}
					else:
						arr_sku.append(sku)
						data2 ={
						'status':0,
						'message':'Those sku are already exists'+'('+ ''.join(arr_sku)+')'
						
						}

				else:
					cnt = EngageboostProducts.objects.using(company_db).filter(sku=sku).filter(isdeleted='n').filter(~Q(id=varient_id)).count()
					if cnt ==0:
						EngageboostProducts.objects.using(company_db).filter(id=varient_id).update(sku=sku,default_price=default_price,visibility_id=visibility)
						EngageboostChannelCurrencyProductPrice.objects.using(company_db).filter(product_id=varient_id).delete()
						EngageboostMarketplaceFieldValue.objects.using(company_db).filter(product_id=varient_id).delete()
						
						from PIL import Image
						import os
						import urllib.request
						print(index)
						if 'cover_image'+str(index) in request.FILES:
							file1 = request.FILES['cover_image'+str(index)]
							image_name=file1.name
							ext = image_name.split('.')[-1]
							new_image_name='CoverImage_'+rand
							cover_image=new_image_name+'.'+ext
							print(cover_image)
							fs=FileSystemStorage()
							# filename = fs.save('product/80x80/'+new_image_name+'.'+ext, file1)
							# filename2 = fs.save('product/100x100/'+new_image_name+'.'+ext, file1)
							filename = fs.save('product/200x200/'+new_image_name+'.'+ext, file1)
							# filename4 = fs.save('product/400x400/'+new_image_name+'.'+ext, file1)
							# filename5 = fs.save('product/800x800/'+new_image_name+'.'+ext, file1)
							# uploaded_file_url = fs.url(filename)
							# uploaded_file_url2 = fs.url(filename2)
							uploaded_file_url = fs.url(filename)
							# uploaded_file_url4 = fs.url(filename4)
							# uploaded_file_url5 = fs.url(filename5)
							image = Image.open(settings.BASE_DIR+uploaded_file_url)
							width_origenal, height_origenal=image.size
							ImageResize(width_origenal,height_origenal,imageresizeon,cover_image)
							for channel in varients['channels']:
								EngageboostChannelCurrencyProductPrice.objects.using(company_db).create(channel_id=channel['channel_id'],currency_id=channel['currency_id'],product_id=varient_id,price=channel['price'],website_id=channel['website_id'],warehouse_id=channel['warehouse_id'],price_type_id=channel['price_type_id'])

							has_record = EngageboostProductimages.objects.using(company_db).filter(product_id=varient_id).count()
							if has_record>0:
								EngageboostProductimages.objects.using(company_db).filter(product_id=varient_id).update(is_cover=0)
								EngageboostProductimages.objects.using(company_db).create(product_id=varient_id,created=datetime.now().date(),modified=datetime.now().date(),img=cover_image,is_cover=1,img_alt=varients['img_alt'],img_title=varients['img_title'],img_order=1)
							else:
								EngageboostProductimages.objects.using(company_db).create(product_id=varient_id,created=datetime.now().date(),modified=datetime.now().date(),img=cover_image,is_cover=1,img_alt=varients['img_alt'],img_title=varients['img_title'],img_order=1)
							
						elif (request.data['cover_url'+str(index)]):
							file1 = request.data['cover_url'+str(index)]
							extrev=file1[::-1]
							extrevore = extrev.split(".")
							ext=extrevore[0][::-1]
							img=urllib.request.urlretrieve(file1, 'media/product/200x200/'+'CoverImage_'+rand+'.'+ext)
							cover_image='CoverImage_'+rand+'.'+ext
							fs=FileSystemStorage()
							BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
							uploaded_file_url = fs.url(img)
							
							# Banner 200x200
							image = Image.open(settings.BASE_DIR+'/media/product/200x200/'+cover_image)
							width_origenal, height_origenal=image.size
							ImageResize(width_origenal,height_origenal,imageresizeon,cover_image)
							for channel in varients['channels']:
								EngageboostChannelCurrencyProductPrice.objects.using(company_db).create(channel_id=channel['channel_id'],currency_id=channel['currency_id'],product_id=varient_id,price=channel['price'],website_id=channel['website_id'],warehouse_id=channel['warehouse_id'],price_type_id=channel['price_type_id'])

							has_record = EngageboostProductimages.objects.using(company_db).filter(product_id=varient_id).count()
							if has_record>0:
								EngageboostProductimages.objects.using(company_db).filter(product_id=varient_id).update(is_cover=0)
								EngageboostProductimages.objects.using(company_db).create(product_id=varient_id,created=datetime.now().date(),modified=datetime.now().date(),img=cover_image,is_cover=1,img_alt=varients['img_alt'],img_title=varients['img_title'],img_order=1)
							else:
								EngageboostProductimages.objects.using(company_db).create(product_id=varient_id,created=datetime.now().date(),modified=datetime.now().date(),img=cover_image,is_cover=1,img_alt=varients['img_alt'],img_title=varients['img_title'],img_order=1)
						
						else:
							cover_image=''		
							for custom_field in varients['custom']:
								field_id=custom_field['field_id']
								field_label_symbol_change=custom_field['field_label']
								field_label_name=field_label_symbol_change.replace(" ","_")
								field_label=field_label_name.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~=+"})
								field_name=custom_field['field_name']

								value=custom_field['value']

								has_record = EngageboostMarketplaceFieldValue.objects.last()
								if has_record:
									last_entry_of_table = EngageboostMarketplaceFieldValue.objects.order_by('-id').latest('id')
									row_id = int(last_entry_of_table.id)+int(1)
								else:
									row_id = 1

								MarketplaceFieldLabels=EngageboostMarketplaceFieldValue.objects.using(company_db).create(id=row_id,created=datetime.now().date(),modified=datetime.now().date(),field_id=field_id,field_label=field_label,field_name=field_name,value=value,website_id=website_id,channel_id=6,product_id=varient_id)	
							for channel in varients['channels']:
								if (channel['price']):
									EngageboostChannelCurrencyProductPrice.objects.using(company_db).create(channel_id=channel['channel_id'],currency_id=channel['currency_id'],product_id=varient_id,price=float(channel['price']),website_id=channel['website_id'],warehouse_id=channel['warehouse_id'],price_type_id=channel['price_type_id'])
							count_img=EngageboostProductimages.objects.using(company_db).filter(product_id=varient_id).count()
							if count_img==0:
								EngageboostProductimages.objects.using(company_db).create(product_id=varient_id,created=datetime.now().date(),modified=datetime.now().date(),img=varients['img'],is_cover=1,img_alt=varients['img_alt'],img_title=varients['img_title'],img_order=1)
							else:
								EngageboostProductimages.objects.using(company_db).filter(product_id=varient_id).update(created=datetime.now().date(),modified=datetime.now().date(),img=varients['img'],is_cover=1,img_alt=varients['img_alt'],img_title=varients['img_title'],img_order=1)
						data2 ={
							'status':1,
							'message':'Inserted Successfully'
							
							}

					else:
						arr_sku.append(sku)
						data2 ={
						'status':0,
						'message':'Those sku are already exists'+'('+ ''.join(arr_sku)+')'
						
						}
						
				
					
			
			
		else:
			data2 ={
					'status':1,
					'message':'Inserted Successfully'
					
					}	
		return Response(data2)	
	#Delete Varient Products 		
	def delete(self, request,pk,website_id, format=None):
		company_db = loginview.db_active_connection(request)
		EngageboostCossSellProducts.objects.using(company_db).filter(cross_product_id=pk).delete()
		EngageboostProducts.objects.using(company_db).all().filter(id=pk).update(isdeleted='y')
		data ={
		'status':1,
		'message':'Successfully Deleted',
		}
		return Response(data)
#Url check
def url_post(company_db,url,count_value):

	cnt_url_suffix = EngageboostProducts.objects.using(company_db).filter(url=url+str(count_value)).count()
	if cnt_url_suffix ==0:
		return count_value
	else:
		count_value=count_value+1
		return url_post(company_db,url,count_value)
#Slug check
def slug_post(company_db,slug,count_value):
	
	cnt_url_suffix = EngageboostProducts.objects.using(company_db).filter(slug=slug+str(count_value)).count()
	if cnt_url_suffix ==0:
		return count_value
	else:
		count_value=count_value+1
		return slug_post(company_db,slug,count_value)

class AllProductImages(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		arr_image=[]
		categoryimage=[]
		categorybannerimage=[]
		categorythumbimage=[]
		type_img=request.data['type']
		if type_img =='category':
			product_image1=EngageboostCategoryMasters.objects.using(company_db).all().filter(isblocked='n',isdeleted='n').distinct('image')
			product_image2=EngageboostCategoryMasters.objects.using(company_db).all().filter(isblocked='n',isdeleted='n').distinct('banner_image')
			product_image3=EngageboostCategoryMasters.objects.using(company_db).all().filter(isblocked='n',isdeleted='n').distinct('thumb_image')
			for product_images in product_image1:
				if product_images.image !='':
					categoryimage.append(product_images.image)
			for product_images in product_image2:		
				if product_images.banner_image !='':
					categorybannerimage.append(product_images.banner_image)
			for product_images in product_image3:		
				if product_images.thumb_image !='':
					categorythumbimage.append(product_images.thumb_image)
			data ={
			'status':1,
			'category_images':categoryimage,
			'category_banner_image':categorybannerimage,
			'category_thumb_image':categorythumbimage

			}
		elif type_img =='product':		
			product_image=EngageboostProductimages.objects.using(company_db).all().distinct('img')
			for product_images in product_image:
				arr_image.append(product_images.img)

				data ={
				'status':1,
				'images':arr_image
				}

		return Response(data)


def ImageResize(width_origenal,height_origenal,imageresizeon,cover_image):
	from PIL import Image
	import os
	import urllib.request
	if imageresizeon.image_resize =='Width':
		if width_origenal >200:
			ratio = width_origenal/height_origenal
			width=200
			height=int(200*height_origenal/width_origenal)
		else:
			width=width_origenal
			height=height_origenal

	

	if imageresizeon.image_resize =='Height':
		if height_origenal >200:
			ratio = height_origenal/width_origenal
			width=int(200*width_origenal/height_origenal)
			height=200
		else:
			width=width_origenal
			height=height_origenal

	image = Image.open(settings.MEDIA_ROOT+'/product/200x200/'+cover_image)
	# Banner 800x800
	img_anti = image.resize((width, height), Image.ANTIALIAS)
	new_image_file = settings.MEDIA_ROOT+'/product/200x200/'+cover_image
	img_anti.save(new_image_file)
	amazons3_fileupload200(cover_image)
	if imageresizeon.image_resize =='Width':
		if width_origenal >100:
			ratio = width_origenal/height_origenal
			width=100
			height=int(100*height_origenal/width_origenal)
		else:
			width=width_origenal
			height=height_origenal

	

	if imageresizeon.image_resize =='Height':
		if height_origenal >100:
			ratio = height_origenal/width_origenal
			width=int(100*width_origenal/height_origenal)
			height=100
		else:
			width=width_origenal
			height=height_origenal
	img_anti = image.resize((width, height), Image.ANTIALIAS)
	new_image_file = settings.MEDIA_ROOT+'/product/100x100/'+cover_image
	img_anti.save(new_image_file)
	amazons3_fileupload100(cover_image)
	# ICON 80X80
	if imageresizeon.image_resize =='Width':
		if width_origenal >80:
			ratio = width_origenal/height_origenal
			width=80
			height=int(80*height_origenal/width_origenal)
		else:
			width=width_origenal
			height=height_origenal

	

	if imageresizeon.image_resize =='Height':
		if height_origenal >80:
			ratio = height_origenal/width_origenal
			width=int(80*width_origenal/height_origenal)
			height=80
		else:
			width=width_origenal
			height=height_origenal
	img_anti = image.resize((width, height), Image.ANTIALIAS)
	new_image_file = settings.MEDIA_ROOT+'/product/80x80/'+cover_image
	img_anti.save(new_image_file)
	amazons3_fileupload80(cover_image)
	# ICON 400X400
	if imageresizeon.image_resize =='Width':
		if width_origenal >400:
			ratio = width_origenal/height_origenal
			width=400
			height=int(400*height_origenal/width_origenal)
		else:
			width=width_origenal
			height=height_origenal

	

	if imageresizeon.image_resize =='Height':
		if height_origenal >400:
			ratio = height_origenal/width_origenal
			width=int(400*width_origenal/height_origenal)
			height=400
		else:
			width=width_origenal
			height=height_origenal
	img_anti = image.resize((width, height), Image.ANTIALIAS)
	new_image_file = settings.MEDIA_ROOT+'/product/400x400/'+cover_image
	img_anti.save(new_image_file)
	amazons3_fileupload400(cover_image)
	# ICON 200X200
	image = Image.open(settings.MEDIA_ROOT+'/product/100x100/'+cover_image)
	width_origenal, height_origenal=image.size
	
	if imageresizeon.image_resize =='Width':
		if width_origenal >800:
			ratio = width_origenal/height_origenal
			width=800
			height=int(800*height_origenal/width_origenal)
		else:
			width=width_origenal
			height=height_origenal

	

	if imageresizeon.image_resize =='Height':
		if height_origenal >800:
			ratio = height_origenal/width_origenal
			width=int(800*width_origenal/height_origenal)
			height=800
		else:
			width=width_origenal
			height=height_origenal
	img_anti = image.resize((width, height), Image.ANTIALIAS)
	new_image_file = settings.MEDIA_ROOT+'/product/800x800/'+cover_image
	img_anti.save(new_image_file)
	amazons3_fileupload800(cover_image)
	return 0

def amazons3_fileupload200(file_name):
	conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)

	f200 = open(settings.MEDIA_ROOT+'/product/200x200/'+file_name,'rb')
	conn.upload('Sample/sample/product/200x200/'+file_name,f200,settings.AMAZON_S3_BUCKET)
	
	return 0
def amazons3_fileupload800(file_name):
	conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)	
	f800 = open(settings.MEDIA_ROOT+'/product/800x800/'+file_name,'rb')
	conn.upload('Sample/sample/product/800x800/'+file_name,f800,settings.AMAZON_S3_BUCKET)
	
	return 0
def amazons3_fileupload100(file_name):
	conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)
	f100 = open(settings.MEDIA_ROOT+'/product/100x100/'+file_name,'rb')
	conn.upload('Sample/sample/product/100x100/'+file_name,f100,settings.AMAZON_S3_BUCKET)	
	
	return 0

def amazons3_fileupload80(file_name):
	conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)
	f80 = open(settings.MEDIA_ROOT+'/product/80x80/'+file_name,'rb')
	conn.upload('Sample/sample/product/80x80/'+file_name,f80,settings.AMAZON_S3_BUCKET)	
	
	return 0
def amazons3_fileupload400(file_name):
	conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)
	f400 = open(settings.MEDIA_ROOT+'/product/400x400/'+file_name,'rb')
	conn.upload('Sample/sample/product/400x400/'+file_name,f400,settings.AMAZON_S3_BUCKET)	
			
	return 0

def delete_create_image_from_local_folder():

	if os.path.exists(settings.BASE_DIR+'/media/product/'):
		shutil.rmtree(settings.BASE_DIR+'/media/product/')

	directory_prduct1=settings.BASE_DIR+'/media/'+'product/100x100/'
	directory_prduct2=settings.BASE_DIR+'/media/'+'product/200x200/'
	directory_prduct3=settings.BASE_DIR+'/media/'+'product/800x800/'
	directory_prduct5=settings.BASE_DIR+'/media/'+'product/80x80/'
	directory_prduct6=settings.BASE_DIR+'/media/'+'product/400x400/'

	
	if not os.path.exists(directory_prduct1):
		os.makedirs(directory_prduct1)

	if not os.path.exists(directory_prduct2):
		os.makedirs(directory_prduct2)

	if not os.path.exists(directory_prduct3):
		os.makedirs(directory_prduct3)

	if not os.path.exists(directory_prduct5):
		os.makedirs(directory_prduct5)

	if not os.path.exists(directory_prduct6):
		os.makedirs(directory_prduct6) 
	 


