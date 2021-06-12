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
from django.db import connection
import sys
import traceback
import json
from django.db.models import Q
import requests
from django.conf import settings
import random
import os
import tinys3
import datetime
from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import MultiPartParser, FormParser
import shutil
from django.utils import timezone
from webservices.views import loginview
from datetime import date,datetime
import xlsxwriter
import xlrd
import re
import unidecode
from django.template.defaultfilters import slugify
from webservices.views.common import common

class BasicInformationViewSet(generics.ListAPIView):
	# """ create new product and image upload method variable d8 is declared for change request data string to json d(variable) is json form d9 use to get url string and di is the json form"""
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		d8=request.data['data']
		d = json.loads(d8)
		image_meta_data = d['image_meta_data']
		image_library = d['image_library']
		url_suffix=d['url_suffix']
		image_meta_cover_data = d['image_meta_data'][0]
		website_id = d['website_id']
		createdby = d['createdby']
		d9=request.data['url']
		di = json.loads(d9)
		sku = d['sku']
		temp_sku = sku
		fetchGlobalSettings = EngageboostGlobalSettings.objects.get(website_id=1)
		prefixs = ""
		suffixs = ""
		if fetchGlobalSettings.sku_prefix != "" and fetchGlobalSettings.sku_prefix != None:
			prefixs = fetchGlobalSettings.sku_prefix
		if fetchGlobalSettings.sku_suffix != "" and fetchGlobalSettings.sku_suffix != None:
			suffixs = fetchGlobalSettings.sku_suffix
		temp_sku = prefixs+temp_sku+suffixs
		cnt = EngageboostProducts.objects.using(company_db).filter(sku=temp_sku,isdeleted='n').count()
		imageresizeon= EngageboostGlobalSettings.objects.using(company_db).get(website_id=1)
		try:
			if cnt == 0:
				method  = request.scheme 
				current_url = request.META['HTTP_HOST']
				url=method+'://'+current_url+'/product/'
				d2=d
				d3=d['name']
				name=d3.lower()
				name1 = common.create_product_slug(d3)

				url1 = url+name1
				cnt = EngageboostProducts.objects.using(company_db).filter(name=d3).count()
				if cnt == 0:
					cnt = cnt
					url2=url1
					name1=name1
				elif cnt ==1:
					cnt = cnt
					url2=url1+'1'
					name1=name1+'1'
				else:
					name1 = name1+str(cnt)
					url2=url1+str(cnt)
				count_url=0
				if count_url==0:
					if url_suffix =="":
						main_url=url2
					else:
						cnt_url_suffix = EngageboostProducts.objects.using(company_db).filter(url=url+url_suffix,isdeleted='n',isblocked='n').count()
						if cnt_url_suffix == 0:
							main_url=url+url_suffix
						else:
							cnt_url_suffix = EngageboostProducts.objects.using(company_db).filter(url=url+url_suffix,isdeleted='n',isblocked='n').count()
							if cnt_url_suffix !=0:
								count_value=increment_value_post(url_suffix,request,count_value=cnt_url_suffix)
								main_url=url+url_suffix+str(count_value)
					d1={'created':datetime.now().date(),'modified':datetime.now().date(),'url':main_url,'slug':name1}
					d2=request.data
					serializer_data=dict(d,**d1)
					req_data = d2['data']
					datajson = json.loads(req_data)
					############## MODIFY SKU ###############
					sku_data = {"sku":temp_sku}
					serializer_data=dict(serializer_data,**sku_data)
					############## MODIFY SKU ###############
					serializer = BasicinfoSerializer(data=serializer_data,partial=True)
					if serializer.is_valid():
						serializer.save()
						obj = EngageboostProducts.objects.using(company_db).latest('id')
						last_id = obj.id
						all_language_data = common.get_all_languages()
						multi_lang_data = []
						for lang_code in all_language_data:
							langcode = lang_code['lang_code']
							lang_id = lang_code['id']
							listcount = len(datajson)
							check_str = "_"+langcode
							for key, value in datajson.items():
								lang_data = {}
								if check_str in key:
									lang_data = {
										"language_id":lang_id,
										"language_code":langcode,
										"product_id":last_id,
										"field_name":key,
										"field_value":value,
										'created':datetime.now().date(),
										'modified':datetime.now().date()
									}
									multi_lang_data.append(lang_data)
						# print(multi_lang_data)
						save_product_lang(multi_lang_data)
						EngageboostProducts.objects.using(company_db).filter(id=last_id).update(customer_group_id=d['customer_group_id'],max_price_rule_id=d['max_price_rule_id'],min_price_rule_id=d['min_price_rule_id'],warehouse_id=d['warehouse_id'],po_taxclass_id=d['po_taxclass_id'],taxclass_id=d['taxclass_id'])
						warehouse_stock=EngageboostWarehouseMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
						for warehouse_stocks in warehouse_stock:
							procuctinfo=EngageboostProductStocks.objects.using(company_db).create(stock=0,safety_stock=0,avg_sales_week=0,avg_sales_month=0,stock_unit=0,product_id=last_id,warehouse_id=warehouse_stocks.id,created=timezone.now(),modified=timezone.now(),isdeleted='n',isblocked='n',real_stock=0)

						for cat in d['parent_categories']:
							check_count = EngageboostProductCategories.objects.using(company_db).filter(product_id=last_id,category_id=cat['category_id'],is_parent=cat['is_parent']).count()
							if check_count>0:
								pass
							else:
								common.update_db_sequences("product_categories")
								objcat = EngageboostProductCategories.objects.using(company_db).create(
									product_id=last_id,
									category_id=cat['category_id'],
									is_parent=cat['is_parent'],
									created=datetime.now().date(),
									modified=datetime.now().date(),
									createdby=createdby
								)
								lastcat_id = objcat.id
								# serializer2 = ProductCategoriesSerializer(objcat,data=serializer_data,partial=True)
								# if serializer2.is_valid():
									# serializer2.save()
						###### multiple barcode start here ###################	
						barcodes=d['barcode_list']
						barcodes = barcodes.split(",")
						error = []
						ids = []
						valid_barcodes = []
						for dt in barcodes:
							if dt!="" and dt!=None:
								psku_count = EngageboostProducts.objects.filter(ean=dt).count()
								msku_count = EngageboostMultipleBarcodes.objects.filter(barcode=dt).exclude(product_id=last_id).count()
								if psku_count==0 and msku_count==0:
									# error.append({'ean':dt,'msg':"Barcode already exists"})
									valid_barcodes.append(dt)
						if len(valid_barcodes)>0:
							for dt in valid_barcodes:
								d1={'created':date.today(),'modified':date.today(),'product_id':last_id,'barcode':dt}
								if website_id:
									d2 = {"website_id":website_id}
									serializer_data=dict(d1,**d2)
								EngageboostMultipleBarcodes.objects.using(company_db).create(**serializer_data)
								# obj = EngageboostMultipleBarcodes.objects.using(company_db).latest('id')
								# last_id = obj.id
								# ids.append(last_id)
						########## end barcode #################################

						from PIL import Image
						import os
						import urllib.request
						rand = str(random.randint(1111,9999))
						common.update_db_sequences("productimages")
						if 'cover_image' in request.FILES:
							common.update_db_sequences("productimages")
							file1 = request.FILES['cover_image']
							image_name=file1.name
							ext = image_name.split('.')[-1]
							new_image_name='CoverImage_'+name1
							cover_image=new_image_name+'.'+ext
							fs=FileSystemStorage()
							filename = fs.save('product/100x100/'+new_image_name+'.'+ext, file1)
							uploaded_file_url = fs.url(filename)
							image = Image.open(settings.BASE_DIR+uploaded_file_url)
							try:
								image = Image.open(settings.BASE_DIR+uploaded_file_url).convert('RGB')
							except:
								pass
							# ICON 100x100
							width_origenal, height_origenal=image.size
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
							
							# Banner 800x800
							img_anti = image.resize((width, height), Image.ANTIALIAS)
							new_image_file = settings.MEDIA_ROOT+'/product/200x200/'+new_image_name+'.'+ext
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
							new_image_file = settings.MEDIA_ROOT+'/product/100x100/'+new_image_name+'.'+ext
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
							new_image_file = settings.MEDIA_ROOT+'/product/80x80/'+new_image_name+'.'+ext
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
							new_image_file = settings.MEDIA_ROOT+'/product/400x400/'+new_image_name+'.'+ext
							img_anti.save(new_image_file)
							amazons3_fileupload400(cover_image)
							# ICON 200X200
							image = Image.open(settings.BASE_DIR+uploaded_file_url)
							try:
								image = Image.open(settings.BASE_DIR+uploaded_file_url).convert('RGB')
							except:
								pass
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
							new_image_file = settings.MEDIA_ROOT+'/product/800x800/'+new_image_name+'.'+ext
							img_anti.save(new_image_file)
							amazons3_fileupload800(cover_image)
							EngageboostProductimages.objects.using(company_db).create(product_id=last_id,created=datetime.now().date(),modified=datetime.now().date(),img=cover_image,is_cover=1,img_alt=image_meta_cover_data['img_alt'],img_title=image_meta_cover_data['img_title'],img_order=image_meta_cover_data['img_order'])
							
						elif (request.data['cover_url']):
							file1 = request.data['cover_url']
							extrev=file1[::-1]
							extrevore = extrev.split(".")
							ext=extrevore[0][::-1]
							img=urllib.request.urlretrieve(file1, 'media/product/200x200/'+'CoverImage_'+name1+'.'+ext)
							cover_image='CoverImage_'+name1+'.'+ext
							fs=FileSystemStorage()
							BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
							uploaded_file_url = fs.url(img)
							
							# Banner 200x200
							image = Image.open(settings.BASE_DIR+'/media/product/200x200/'+cover_image)
							try:
								image = Image.open(settings.BASE_DIR+'/media/product/200x200/'+cover_image).convert('RGB')
							except:
								pass
							width_origenal, height_origenal=image.size
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
						
							# Banner 800x800
							img_anti = image.resize((width, height), Image.ANTIALIAS)
							new_image_file = settings.MEDIA_ROOT+'/product/100x100/'+cover_image
							img_anti.save(new_image_file)
							amazons3_fileupload100(cover_image)
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
							EngageboostProductimages.objects.using(company_db).create(product_id=last_id,created=datetime.now().date(),modified=datetime.now().date(),img=cover_image,is_cover=1,img_alt=image_meta_cover_data['img_alt'],img_title=image_meta_cover_data['img_title'],img_order=image_meta_cover_data['img_order'])    
						else:
							cover_image = ''    
						image_meta_data_url=[]
						image_meta_data_length=len(image_meta_data)	
						for x in range(image_meta_data_length):

							if image_meta_data[x]['type']==1 and image_meta_data[x]['is_cover']==0:
								
								image_meta_data_url.append(image_meta_data[x])
						
						if (di['other_image']):
							index=0
							for images in di['other_image']:
								
								extrev=images[::-1]
								extrevore = extrev.split(".")
								ext=extrevore[0][::-1]
								file_name = images.split('.')
								img=urllib.request.urlretrieve(images, 'media/product/200x200/'+'OtherImage_'+str(index)+name1+'.'+ext)
								other_image='OtherImage_'+str(index)+name1+'.'+ext
								fs=FileSystemStorage()
								uploaded_file_url = fs.url(img)
								BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
								# Banner 200x200
								image = Image.open(settings.BASE_DIR+'/media/product/200x200/'+other_image)
								try:
									image = Image.open(settings.BASE_DIR+'/media/product/200x200/'+other_image).convert('RGB')
								except:
									pass
								width_origenal, height_origenal=image.size
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
								img_anti = image.resize((width, height), Image.ANTIALIAS)
								new_image_file = settings.MEDIA_ROOT+'/product/200x200/'+other_image
								img_anti.save(new_image_file)
								amazons3_fileupload200(other_image)
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
								new_image_file = settings.MEDIA_ROOT+'/product/80x80/'+other_image
								img_anti.save(new_image_file)
								amazons3_fileupload80(other_image)
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
								new_image_file = settings.MEDIA_ROOT+'/product/400x400/'+other_image
								img_anti.save(new_image_file)
								amazons3_fileupload400(other_image)
									# ICON 200X200
								image = Image.open(settings.BASE_DIR+'/media/product/200x200/'+other_image)
								try:
									image = Image.open(settings.BASE_DIR+'/media/product/200x200/'+other_image).convert('RGB')
								except:
									pass
								width_origenal, height_origenal=image.size
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
								
								# Banner 800x800
								img_anti = image.resize((width, height), Image.ANTIALIAS)
								new_image_file = settings.MEDIA_ROOT+'/product/100x100/'+other_image
								img_anti.save(new_image_file)
								amazons3_fileupload100(other_image)
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
								new_image_file = settings.MEDIA_ROOT+'/product/800x800/'+other_image
								img_anti.save(new_image_file)
								amazons3_fileupload800(other_image)                                
								EngageboostProductimages.objects.using(company_db).create(product_id=last_id,created=datetime.now().date(),modified=datetime.now().date(),img=other_image,is_cover=0,img_alt=image_meta_data_url[index]['img_alt'],img_title=image_meta_data_url[index]['img_title'],img_order=image_meta_data_url[index]['img_order'])
								index=index+1
						image_meta_data_browse=[]
						image_meta_data_length=len(image_meta_data)
						for x in range(image_meta_data_length):
							if image_meta_data[x]['type']==2 and image_meta_data[x]['is_cover']==0:
								
								image_meta_data_browse.append(image_meta_data[x])

						if 'other_image' in request.FILES:
							index=0
							for images in request.FILES.getlist('other_image'):
								file1 = images
								image_name=file1.name
								file_name = image_name.split('.')
								ext = image_name.split('.')[-1]
								other_image='OtherImage_'+file_name[0]+'_'+name1+'.'+ext
								fs=FileSystemStorage()
								filename = fs.save('product/200x200/'+other_image, file1)
								uploaded_file_url = fs.url(filename)
								# Banner 200x200
								image = Image.open(settings.BASE_DIR+'/media/product/200x200/'+other_image)
								try:
									image = Image.open(settings.BASE_DIR+'/media/product/200x200/'+other_image).convert('RGB')
								except:
									pass
								width_origenal, height_origenal=image.size
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
								img_anti = image.resize((width, height), Image.ANTIALIAS)
								new_image_file = settings.MEDIA_ROOT+'/product/200x200/'+other_image
								img_anti.save(new_image_file)
								amazons3_fileupload200(other_image)
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
								new_image_file = settings.MEDIA_ROOT+'/product/80x80/'+other_image
								img_anti.save(new_image_file)
								amazons3_fileupload80(other_image)
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
								new_image_file = settings.MEDIA_ROOT+'/product/400x400/'+other_image
								img_anti.save(new_image_file)
									# ICON 200X200
								amazons3_fileupload400(other_image)	
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
								
								# Banner 800x800
								img_anti = image.resize((width, height), Image.ANTIALIAS)
								new_image_file = settings.MEDIA_ROOT+'/product/100x100/'+other_image
								img_anti.save(new_image_file)
								amazons3_fileupload100(other_image)
								if imageresizeon.image_resize =='Width':
									ratio = width_origenal/height_origenal
									width=800
									height=int(800*height_origenal/width_origenal)
								
								if imageresizeon.image_resize =='Height' :
									ratio = height_origenal/width_origenal
									width=int(800*width_origenal/height_origenal)
									height=800
									img_anti = image.resize((width, height), Image.ANTIALIAS)
									new_image_file = settings.MEDIA_ROOT+'/product/800x800/'+other_image
									img_anti.save(new_image_file)
									amazons3_fileupload800(other_image)
									
								EngageboostProductimages.objects.using(company_db).create(product_id=last_id,created=datetime.now().date(),modified=datetime.now().date(),img=other_image,is_cover=0,img_alt=image_meta_data_browse[index]['img_alt'],img_title=image_meta_data_browse[index]['img_title'],img_order=image_meta_data_browse[index]['img_order'])
								index=index+1
							else:
								other_image = ''

						image_meta_data_library=[]
						image_meta_data_length=len(image_meta_data)	
						for x in range(image_meta_data_length):

							if image_meta_data[x]['type']==3:
								
								image_meta_data_library.append(image_meta_data[x])
						index=0		
						for image_librarys in image_library:
							if len(image_librarys['img'])>0:
								EngageboostProductimages.objects.using(company_db).create(product_id=last_id,created=datetime.now().date(),modified=datetime.now().date(),img=image_librarys['img'],is_cover=image_meta_data_library[index]['is_cover'],img_alt=image_meta_data_library[index]['img_alt'],img_title=image_meta_data_library[index]['img_title'],img_order=image_meta_data_library[index]['img_order'])
								index=index+1
						delete_create_image_from_local_folder()
						elastic = common.save_data_to_elastic(last_id,'EngageboostProducts')
						data ={
							'status':1,
							'api_status':last_id,
							'message':'Successfully Updated',
						}
					else:
						data ={
							'status':0,
							'api_status':serializer.errors,
							'message':'Invalid Data',
							}
			else:
				data ={
					'status':0,
					'message':'SKU number is already exists',
				}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
		# return all response data
		return Response(data)

class BasicProductSet(generics.ListAPIView):
	# """ List all products for single row update """
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostProducts.objects.using(company_db).get(id=pk)
		except EngageboostProducts.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		product_info = EngageboostProducts.objects.using(company_db).filter(id=pk)
		if product_info.count()>0:
			product_info = product_info.first()
			serializer = BasicinfoSerializer(product_info,partial=True)
			# print(json.dumps(serializer.data))
			serializer_data = serializer.data
			if len(serializer_data['lang_data'])>0:
				for lang_data in serializer_data['lang_data']:
					serializer_data[lang_data['field_name']]=lang_data['field_value']
			serializer_data.pop('lang_data')
			product_category = EngageboostProductCategories.objects.using(company_db).all().filter(product_id=pk).order_by('id')
			serializer_cate = ProductCategoriesSerializer(product_category,many=True)
			product_cover_img = EngageboostProductimages.objects.using(company_db).all().filter(product_id=pk).filter(is_cover=1)
			product_cover_image = ProductImagesSerializer(product_cover_img,many=True)
			product_img=EngageboostProductimages.objects.using(company_db).all().filter(product_id=pk).filter(~Q(is_cover=1)).order_by('img_order')  
			serializer_img = ProductImagesSerializer(product_img,many=True)
			product_image=product_cover_image.data+serializer_img.data
			product_barcodes = common.getProductBarcode(pk)
			# print(product_barcodes)
			serializer_data['barcode_list'] = product_barcodes
			arr_parent=[]
			data_parent={}
			child_fetch = EngageboostProductCategories.objects.using(company_db).all().filter(product_id=pk, isdeleted='n', isblocked='n').order_by('-is_parent')
			if child_fetch:
				child_fetch_serializer=ProductCategoriesSerializer(child_fetch,many=True)
				for child in child_fetch_serializer.data:
					child_id1=EngageboostCategoryMasters.objects.using(company_db).filter(id=child["category"]["id"],isdeleted='n').first()
					if child_id1:
						if child_id1.parent_id!=0:
							child_id2=EngageboostCategoryMasters.objects.using(company_db).get(id=child_id1.parent_id,isdeleted='n')
							if child_id2:
								if child_id2.parent_id!=0:
									child_id3=EngageboostCategoryMasters.objects.using(company_db).get(id=child_id2.parent_id,isdeleted='n')
									if child_id3:
										if child_id3.parent_id!=0:
											child_id4=EngageboostCategoryMasters.objects.using(company_db).get(id=child_id3.parent_id,isdeleted='n')
											category_1=child_id4.id
											category_2=child_id3.id
											category_3=child_id2.id
											category_4=child_id1.id

										else:
											category_1=child_id3.id
											category_2=child_id2.id
											category_3=child_id1.id
											category_4=0
									else:
										category_1=0
										category_2=child_id2.id
										category_3=child_id1.id
										category_4=0
								else:
									category_1=child_id2.id
									category_2=child_id1.id
									category_3=0
									category_4=0
							else:
								category_1=0
								category_2=child_id1.id
								category_3=0
								category_4=0	
						else:
							category_1=child_id1.id
							category_2=0
							category_3=0
							category_4=0
					else:
						category_1=0
						category_2=0
						category_3=0
						category_4=0
					data_parent={"parent_id":category_1,"child_id":category_2,"sub_child_id":category_3,"sub_sub_child_id":category_4}	
					arr_parent.append(data_parent)
			if(serializer):
				data ={
					'status':1,
					'api_status':serializer_data,
					'product_category':serializer_cate.data,
					'product_img':product_image,
					'parent_child':arr_parent
				}
			else:
				data ={
					'status':0,
					'api_status':serializer.errors,
					'message':'Data Not Found',
				}
		else:
			data ={
				'status':0,
				'api_status':"",
				'message':'Data Not Found',
			}
		return Response(data)
	# """ single product update variable d8 is diclare for change request data string to json d(variable) is json form d9 use to get url string and di is the json form"""
	def put(self, request,pk, format=None):
		company_db = loginview.db_active_connection(request)
		product = self.get_object(pk,request)
		d8=request.data['data']
		d = json.loads(d8)
		url_suffix=d['url_suffix']
		image_meta_data = d['image_meta_data']
		website_id=d['website_id']
		updatedby =  d['updatedby']
		image_library = d['image_library']
		image_meta_cover_data = {}
		if len(d['image_meta_data']) > 0 and d['image_meta_data'][0]['is_cover']==1:
			image_meta_cover_data = d['image_meta_data'][0]
		if len(d['image_meta_data_edit']) > 0 and d['image_meta_data_edit'][0]['is_cover']==1:
			image_meta_data_cover_edit = d['image_meta_data_edit'][0]
		d9=request.data['url']
		di = json.loads(d9)
		sku=d['sku']
		cnt = EngageboostProducts.objects.using(company_db).filter(sku=sku,isdeleted='n').filter(~Q(id=pk)).count()
		imageresizeon= EngageboostGlobalSettings.objects.using(company_db).get(website_id=website_id)
		try:
			if  cnt == 0:
				method  = request.scheme 
				current_url = request.META['HTTP_HOST'] 
				url=method+'://'+current_url+'/product/'
				d2=d
				d3=d['name']
				name=d3.lower()
				name1 = common.create_product_slug(d3,pk)

				url1=url+name1
				same_name=EngageboostProducts.objects.using(company_db).filter(name=d3,id=pk).count()
				if same_name ==1:
					url2=url1
					name1=name1
				else:
					cnt = EngageboostProducts.objects.using(company_db).filter(name=d3).count()
					if cnt == 0:
						cnt = cnt
						url2=url1
						name1=name1
					elif cnt ==1:
						cnt = cnt
						url2=url1+'1'
						name1=name1+'1'
					else:
						name1 = name1+str(cnt)
						url2=url1+str(cnt)
				count_url=0
				if count_url==0:
					if url_suffix =="":
						main_url=url2
					else:
						cnt_url_suffix = EngageboostProducts.objects.using(company_db).filter(url=url+url_suffix,isdeleted='n',isblocked='n').count()
						if cnt_url_suffix == 0:
							main_url=url+url_suffix
						else:
							cnt_url_suffix = EngageboostProducts.objects.using(company_db).filter(url=url+url_suffix,isdeleted='n',isblocked='n').count()
							if cnt_url_suffix !=0:
								count_value=increment_value_post(url_suffix,request,count_value=cnt_url_suffix)
								main_url=url+url_suffix+str(count_value)

					# d1={'modified':datetime.now().date(),'url':main_url,'slug':name1}
					d1 = {'modified': datetime.now().date(), 'url': main_url}
					d2=request.data
					serializer_data=dict(d,**d1)

					serializer = BasicinfoSerializer(product,data=serializer_data,partial=True)
					if serializer.is_valid():
						serializer.save()

						all_language_data = all_language_data = common.get_all_languages()
						multi_lang_data = []
						for lang_code in all_language_data:
							langcode = lang_code['lang_code']
							lang_id = lang_code['id']
							listcount = len(d)
							check_str = "_"+langcode
							for key, value in d.items():
								lang_data = {}
								if check_str in key:
									lang_data = {
										"language_id":lang_id,
										"language_code":langcode,
										"product_id":pk,
										"field_name":key,
										"field_value":value,
										'created':datetime.now().date(),
										'modified':datetime.now().date()
									}
									multi_lang_data.append(lang_data)
						# print(multi_lang_data)
						save_product_lang(multi_lang_data)
						
						last_id = pk
						EngageboostProducts.objects.using(company_db).filter(id=last_id).update(customer_group_id=d['customer_group_id'],max_price_rule_id=d['max_price_rule_id'],min_price_rule_id=d['min_price_rule_id'],warehouse_id=d['warehouse_id'],po_taxclass_id=d['po_taxclass_id'],taxclass_id=d['taxclass_id'])
						EngageboostProductCategories.objects.using(company_db).filter(product_id=pk).delete()
						# EngageboostProductimages.objects.using(company_db).filter(product_id=pk).delete()
					else:
						data = {
							"status":0,
							"msg":serializer.errors
						}
						return Response(data)
					
					###### multiple barcode start here ###################	
					barcodes=d['barcode_list']
					barcodes = barcodes.split(",")
					error = []
					ids = []
					valid_barcodes = []
					for dt in barcodes:
						if dt!="" and dt!=None:
							psku_count = EngageboostProducts.objects.filter(ean=dt).count()
							msku_count = EngageboostMultipleBarcodes.objects.filter(barcode=dt).exclude(product_id=pk).count()
							if psku_count==0 and msku_count==0:
								# error.append({'ean':dt,'msg':"Barcode already exists"})
								valid_barcodes.append(dt)
					if len(valid_barcodes)>0:
						EngageboostMultipleBarcodes.objects.using(company_db).filter(product_id=pk).exclude(default_ean='y').delete()
						for dt in valid_barcodes:
							d1={'created':date.today(),'modified':date.today(),'product_id':pk,'barcode':dt}
							if website_id:
								d2 = {"website_id":website_id}
								serializer_data=dict(d1,**d2)
							EngageboostMultipleBarcodes.objects.using(company_db).create(**serializer_data)
							# obj = EngageboostMultipleBarcodes.objects.using(company_db).latest('id')
							# last_id = obj.id
							# ids.append(last_id)
					########## end barcode #################################

					for cat in d['parent_categories']:
						common.update_db_sequences("product_categories")
						objcat = EngageboostProductCategories.objects.using(company_db).create(
							product_id=last_id,
							category_id=cat['category_id'],
							is_parent=cat['is_parent'],
							created=datetime.now().date(),
							modified=datetime.now().date(),
							updatedby=updatedby
						)
						lastcat_id = objcat.id
						#serializer2 = ProductCategoriesSerializer(objcat,data=serializer_data,partial=True)
						if lastcat_id > 0:
							# serializer2.save()
							product_id = pk
							name = serializer.data['name']
							description = serializer.data['description']
							large_description = serializer.data['mp_description']
							sku= serializer.data['sku']
							link ='products/edit/'+str(product_id)
							tab_name ='Edit Product'
							tab_id ='productsedit'
							# elastic = common.save_data_to_elastic(product_id,'EngageboostProducts')
						for x in range(len(d['image_meta_data_edit'])):
							EngageboostProductimages.objects.using(company_db).filter(id=d['image_meta_data_edit'][x]['id']).update(modified=datetime.now().date(),img_alt=d['image_meta_data_edit'][x]['img_alt'],img_title=d['image_meta_data_edit'][x]['img_title'],img_order=d['image_meta_data_edit'][x]['img_order'])
						# ////////////////Image Resize//////////////
					from PIL import Image
					import os
					import urllib.request
					rand = str(random.randint(1111,9999))
					common.update_db_sequences("productimages")
					if 'cover_image' in request.FILES:
						file1 = request.FILES['cover_image']
						image_name=file1.name
						ext = image_name.split('.')[-1]
						new_image_name='CoverImage_'+name1
						cover_image=new_image_name+'.'+ext
						fs=FileSystemStorage()
						filename = fs.save('product/100x100/'+new_image_name+'.'+ext, file1)
						uploaded_file_url = fs.url(filename)
						image = Image.open(settings.BASE_DIR+uploaded_file_url)
						try:
							image = Image.open(settings.BASE_DIR+uploaded_file_url).convert('RGB')
						except:
							pass	
						# ICON 100x100
						width_origenal, height_origenal=image.size
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
						new_image_file = settings.MEDIA_ROOT+'/product/100x100/'+new_image_name+'.'+ext
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
						new_image_file = settings.MEDIA_ROOT+'/product/80x80/'+new_image_name+'.'+ext
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
						new_image_file = settings.MEDIA_ROOT+'/product/400x400/'+new_image_name+'.'+ext
						img_anti.save(new_image_file)
						
						# ICON 200X200
						amazons3_fileupload400(cover_image)
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
						img_anti = image.resize((width, height), Image.ANTIALIAS)
						new_image_file = settings.MEDIA_ROOT+'/product/200x200/'+new_image_name+'.'+ext
						img_anti.save(new_image_file)
						
						# Banner 800x800
						amazons3_fileupload200(cover_image)
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
						new_image_file = settings.MEDIA_ROOT+'/product/800x800/'+new_image_name+'.'+ext
						img_anti.save(new_image_file)
						amazons3_fileupload800(cover_image)
						# img_alt 	= ""
						# img_title 	= ""
						# img_order 	= 0
						create_arr = {
							"product_id":last_id,
							"created":datetime.now().date(),
							"modified":datetime.now().date(),
							"img":cover_image,
							"is_cover":1,
						}
						if image_meta_cover_data:
							create_arr.update({"img_alt":image_meta_cover_data['img_alt'], "img_title":image_meta_cover_data['img_title'], "img_order":image_meta_cover_data['img_order']})

						check_cover_img_count = EngageboostProductimages.objects.using(company_db).filter(product_id=last_id, is_cover=1).count()
						if check_cover_img_count>0:
							EngageboostProductimages.objects.using(company_db).filter(product_id=last_id, is_cover=1).update(**create_arr)
						else:
							EngageboostProductimages.objects.using(company_db).create(**create_arr)

					elif(request.data['cover_url']):
						file1 = request.data['cover_url']

						extrev=file1[::-1]
						extrevore = extrev.split(".")
						ext=extrevore[0][::-1]
						img=urllib.request.urlretrieve(file1, 'media/product/200x200/'+'CoverImage_'+name1+'.'+ext)
						cover_image='CoverImage_'+name1+'.'+ext
						fs=FileSystemStorage()
						BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
						uploaded_file_url = fs.url(img)
						# Banner 200x200
						image = Image.open(settings.BASE_DIR+'/media/product/200x200/'+cover_image)

						try:
							image = Image.open(settings.BASE_DIR+'/media/product/200x200/'+cover_image).convert('RGB')
						except:
							pass

						width_origenal, height_origenal=image.size
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
						img_anti = image.resize((width, height), Image.ANTIALIAS)
						new_image_file = settings.MEDIA_ROOT+'/product/200x200/'+cover_image
						img_anti.save(new_image_file)
						amazons3_fileupload200(cover_image)
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
						# ICON 200X200
						amazons3_fileupload400(cover_image)	
						
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
						
						# Banner 800x800
						img_anti = image.resize((width, height), Image.ANTIALIAS)
						new_image_file = settings.MEDIA_ROOT+'/product/100x100/'+cover_image
						img_anti.save(new_image_file)
						amazons3_fileupload100(cover_image)
						
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
						
						EngageboostProductimages.objects.using(company_db).create(product_id=last_id,created=datetime.now().date(),modified=datetime.now().date(),img=cover_image,is_cover=1,img_alt=image_meta_cover_data['img_alt'],img_title=image_meta_cover_data['img_title'],img_order=image_meta_cover_data['img_order'])    
					else:
						cover_image = d['cover_image'] 

					##### other image from url ########	   
					image_meta_data_url=[]
					image_meta_data_length=len(image_meta_data)	
					for x in range(image_meta_data_length):
						if image_meta_data[x]['type']==1 and image_meta_data[x]['is_cover']==0:
							image_meta_data_url.append(image_meta_data[x])
					
					if (di['other_image']):
						index=0
						for images in di['other_image']:
							
							extrev=images[::-1]
							extrevore = extrev.split(".")
							ext=extrevore[0][::-1]
							file_name = images.split('.')
							img=urllib.request.urlretrieve(images, 'media/product/200x200/'+'OtherImage_'+str(index)+name1+'.'+ext)
							other_image='OtherImage_'+str(index)+name1+'.'+ext
							fs=FileSystemStorage()
							uploaded_file_url = fs.url(img)
							BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
							# Banner 200x200
							image = Image.open(settings.BASE_DIR+'/media/product/200x200/'+other_image)

							try:
								image = Image.open(settings.BASE_DIR+'/media/product/200x200/'+other_image).convert('RGB')
							except:
								pass

							width_origenal, height_origenal=image.size
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
							img_anti = image.resize((width, height), Image.ANTIALIAS)
							new_image_file = settings.MEDIA_ROOT+'/product/200x200/'+other_image
							img_anti.save(new_image_file)
							amazons3_fileupload200(other_image)
							
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
							new_image_file = settings.MEDIA_ROOT+'/product/80x80/'+other_image
							img_anti.save(new_image_file)
							amazons3_fileupload80(other_image)
							
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
							new_image_file = settings.MEDIA_ROOT+'/product/400x400/'+other_image
							img_anti.save(new_image_file)
							amazons3_fileupload400(other_image)
							
								# ICON 200X200
							image = Image.open(settings.BASE_DIR+'/media/product/200x200/'+other_image)
							try:
								image = Image.open(settings.BASE_DIR+'/media/product/200x200/'+other_image).convert('RGB')
							except:
								pass
							width_origenal, height_origenal=image.size
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
							# Banner 800x800
							img_anti = image.resize((width, height), Image.ANTIALIAS)
							new_image_file = settings.MEDIA_ROOT+'/product/100x100/'+other_image
							img_anti.save(new_image_file)
							amazons3_fileupload100(other_image)
							
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
							new_image_file = settings.MEDIA_ROOT+'/product/800x800/'+other_image
							img_anti.save(new_image_file)
							amazons3_fileupload800(other_image) 
														   
							EngageboostProductimages.objects.using(company_db).create(product_id=last_id,created=datetime.now().date(),modified=datetime.now().date(),img=other_image,is_cover=0,img_alt=image_meta_data_url[index]['img_alt'],img_title=image_meta_data_url[index]['img_title'],img_order=image_meta_data_url[index]['img_order'])
							index=index+1

					#### other image from file browse ###########

					image_meta_data_browse=[]
					image_meta_data_length=len(image_meta_data)
					for x in range(image_meta_data_length):
						if image_meta_data[x]['type']==2 and image_meta_data[x]['is_cover']==0:
							image_meta_data_browse.append(image_meta_data[x])
							
					if 'other_image' in request.FILES:
						index=0
						for images in request.FILES.getlist('other_image'):
							file1 = images
							image_name=file1.name
							file_name = image_name.split('.')
							ext = image_name.split('.')[-1]
							other_image='OtherImage_'+file_name[0]+'_'+name1+'.'+ext
							fs=FileSystemStorage()
							filename = fs.save('product/200x200/'+other_image, file1)
							uploaded_file_url = fs.url(filename)
							# Banner 200x200
							image = Image.open(settings.BASE_DIR+'/media/product/200x200/'+other_image)
							try:
								image = Image.open(settings.BASE_DIR+'/media/product/200x200/'+other_image).convert('RGB')
							except:
								pass
							width_origenal, height_origenal=image.size
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
							img_anti = image.resize((width, height), Image.ANTIALIAS)
							new_image_file = settings.MEDIA_ROOT+'/product/200x200/'+other_image
							img_anti.save(new_image_file)
							amazons3_fileupload200(other_image)
							
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
							new_image_file = settings.MEDIA_ROOT+'/product/80x80/'+other_image
							img_anti.save(new_image_file)
							amazons3_fileupload80(other_image)
							
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
							new_image_file = settings.MEDIA_ROOT+'/product/400x400/'+other_image
							img_anti.save(new_image_file)
							amazons3_fileupload400(other_image)
								# ICON 200X200
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
							
							# Banner 100x100
							img_anti = image.resize((width, height), Image.ANTIALIAS)
							new_image_file = settings.MEDIA_ROOT+'/product/100x100/'+other_image
							img_anti.save(new_image_file)
							amazons3_fileupload100(other_image)

							# Banner 100x100
							if imageresizeon.image_resize =='Width':
								ratio = width_origenal/height_origenal
								width=800
								height=int(800*height_origenal/width_origenal)
							
							if imageresizeon.image_resize =='Height' :
								ratio = height_origenal/width_origenal
								width=int(800*width_origenal/height_origenal)
								height=800
								img_anti = image.resize((width, height), Image.ANTIALIAS)
								new_image_file = settings.MEDIA_ROOT+'/product/800x800/'+other_image
								img_anti.save(new_image_file)
								amazons3_fileupload800(other_image)
								
							EngageboostProductimages.objects.using(company_db).create(product_id=last_id,created=datetime.now().date(),modified=datetime.now().date(),img=other_image,is_cover=0,img_alt=image_meta_data_browse[index]['img_alt'],img_title=image_meta_data_browse[index]['img_title'],img_order=image_meta_data_browse[index]['img_order'])
							index=index+1
						else:
							other_image = ''
					delete_create_image_from_local_folder()
					image_meta_data_library=[]
					image_meta_data_length=len(image_meta_data)
					for x in range(image_meta_data_length):
						if image_meta_data[x]['type']==3:
							image_meta_data_library.append(image_meta_data[x])
					index=0
					for image_librarys in image_library:
						if len(image_librarys['img'])>0:
							EngageboostProductimages.objects.using(company_db).create(product_id=last_id,created=datetime.now().date(),modified=datetime.now().date(),img=image_librarys['img'],is_cover=image_meta_data_library[index]['is_cover'],img_alt=image_meta_data_library[index]['img_alt'],img_title=image_meta_data_library[index]['img_title'],img_order=image_meta_data_library[index]['img_order'])
							index=index+1
					
					elastic = common.save_data_to_elastic(pk,'EngageboostProducts')		

					data = {
						'status':1,
						'api_status':last_id,
						'message':'Successfully Updated',
					}
			else:
				data ={
					'status':0,
					'message':'SKU number is already exists',
				}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
		# return all response data
		return Response(data)
class BasicInformationLoadViewSet(generics.ListAPIView):
	# """ Dropdown for Brand, category, supplier, customer group, min price rule, max price rule"""
	def get(self, request, format=None): 
		company_db = loginview.db_active_connection(request)
		data={}
		data1 = EngageboostProductTaxClasses.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer1 = TaxclassesSerializer(data1, many=True)  
		data2 = EngageboostCustomerGroup.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer2 = CustomerGroupSerializer(data2, many=True) 
		data3 = EngageboostRepricingMaximumMinRules.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer3 = ProductpriceroulSerializer(data3, many=True)
		data4 = EngageboostRepricingMaximumMinRules.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer4 = ProductpriceroulSerializer(data3, many=True)
		data5 = EngageboostBrandMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer5 = BrandSerializer(data5, many=True)
		data6 = EngageboostSuppliers.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer6 = SuppliersSerializer(data6, many=True)
		data7 = EngageboostCategoryMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n',parent_id=0).order_by('-id')
		serializer7 = CategoriesSerializer(data7, many=True)
		data8 = EngageboostUnitMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer8 = UnitmasterSerializer(data8, many=True)
		data9 = EngageboostWarehouseMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer9 = WarehousemastersSerializer(data9, many=True)
		data10 = EngageboostProductTaxClasses.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer10 = TaxclassesSerializer(data10, many=True)
		all_language_data = common.get_all_languages()

		data['category']=serializer7.data
		data['supplier']=serializer6.data
		data['brand']=serializer5.data
		data['ptaxclass']=serializer1.data
		data['customergrp']=serializer2.data
		data['minprice']=serializer3.data
		data['maxprice']=serializer4.data
		data['unit']=serializer8.data
		data['warehouse']=serializer9.data
		data['taxclass']=serializer10.data
		data['all_languages']=all_language_data

		return Response(data)
# Product Image delete
class ProductImageDelete(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		ids=request.data['id']
		field=request.data['field']
		file_name=request.data['file_name']
		value=''
		query = {field : value}
		image_name=EngageboostProductimages.objects.using(company_db).values(field).filter(id=ids)
		img_count=EngageboostProductimages.objects.using(company_db).filter(img=file_name).count()
		if img_count==1:
			conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)
			conn.delete('product/200x200/'+file_name,settings.AMAZON_S3_BUCKET)
			conn.delete('product/800x800/'+file_name,settings.AMAZON_S3_BUCKET)
			conn.delete('product/400x400/'+file_name,settings.AMAZON_S3_BUCKET)
			conn.delete('product/80x80/'+file_name,settings.AMAZON_S3_BUCKET)
			conn.delete('product/400x400/'+file_name,settings.AMAZON_S3_BUCKET)
		# if os.path.exists(settings.BASE_DIR+'/media/product/200x200/'+file_name):
		# 	os.unlink(settings.BASE_DIR+'/media/product/200x200/'+file_name)
		# if os.path.exists(settings.BASE_DIR+'/media/product/100x100/'+file_name):
		# 	os.unlink(settings.BASE_DIR+'/media/product/100x100/'+file_name)
		# if os.path.exists(settings.BASE_DIR+'/media/product/800x800/'+file_name):
		# 	os.unlink(settings.BASE_DIR+'/media/product/800x800/'+file_name)
		# if os.path.exists(settings.BASE_DIR+'/media/product/400x400/'+file_name):
		# 	os.unlink(settings.BASE_DIR+'/media/product/400x400/'+file_name)
		# if os.path.exists(settings.BASE_DIR+'/media/product/80x80/'+file_name):
		# 	os.unlink(settings.BASE_DIR+'/media/product/80x80/'+file_name)
		EngageboostProductimages.objects.using(company_db).filter(id=ids).delete()
		data ={
				'status':1,
				'message':'Successfully Deleted',
				}

		return Response(data)
# web services set cover image for product image upload
class SetCoverImage(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		ids=request.data['id']
		product_id=request.data['product_id']
		EngageboostProductimages.objects.using(company_db).filter(id=ids,product_id=product_id).update(is_cover=1,img_order=1)
		EngageboostProductimages.objects.using(company_db).filter(product_id=product_id).filter(~Q(id=ids)).update(is_cover=0)
		data ={
				'status':1,
				'message':'Selected image has been set as cover image',
				}

		return Response(data)
# Get Child data 
class GetProductChild(APIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		category_id=request.data['category_id']
		ids=request.data['id']
		lvl=request.data['lvl']
		if ids==0:
			parent_category_id=category_id
		else:
			parent_category_id=ids

		if lvl==2:
			Categories = EngageboostParentCategories.objects.using(company_db).all().filter(parent_category_id=category_id).filter(parent_two_category_id=0).filter(~Q(category_id=ids)).distinct('category_id')
		if lvl==3:
			Categories = EngageboostParentCategories.objects.using(company_db).all().filter(parent_two_category_id=category_id).filter(parent_three_category_id=0).filter(~Q(category_id=ids)).distinct('category_id')
		if lvl==4:
			Categories = EngageboostParentCategories.objects.using(company_db).all().filter(parent_three_category_id=category_id).filter(~Q(category_id=ids)).distinct('category_id')			
		arr2=[]
		for Categories1 in Categories:
			Categoriesid = EngageboostCategoryMasters.objects.using(company_db).all().filter(id=Categories1.category_id).order_by('-id')
			for Categoriesid1 in Categoriesid:
				d2={"id":Categoriesid1.id,"name":Categoriesid1.name,"parent_id":Categories1.id}
				arr2.append(d2)
		return HttpResponse(json.dumps({"category":arr2,"status":1}), content_type='application/json')		

def increment_value(url_suffix,pk,request,count_value):
	company_db = loginview.db_active_connection(request)
	method    = request.scheme 
	current_url = request.META['HTTP_HOST']
	url=method+'://'+current_url+'/product/'

	cnt_url_suffix = EngageboostProducts.objects.using(company_db).filter(url=url+url_suffix+str(count_value),isdeleted='n',isblocked='n').filter(~Q(id=pk)).count()
	if cnt_url_suffix ==0:
		return count_value
	else:
		count_value=count_value+1
		return increment_value(url_suffix,pk,request,count_value)


def increment_value_post(url_suffix,request,count_value):
	company_db = loginview.db_active_connection(request)
	method    = request.scheme 
	current_url = request.META['HTTP_HOST']
	url=method+'://'+current_url+'/product/'

	cnt_url_suffix = EngageboostProducts.objects.using(company_db).filter(url=url+url_suffix+str(count_value),isblocked='n',isdeleted='n').count()
	if cnt_url_suffix ==0:
		return count_value
	else:
		count_value=count_value+1
		return increment_value_post(url_suffix,request,count_value)

class ProductList(generics.ListAPIView):
	# """ List all Edit,Uodate Brand """
	def post(self, request, format=None,many=True):
		company_db = loginview.db_active_connection(request)
		visibility_id=request.data['visibility_id']
		user = EngageboostProducts.objects.using(company_db).all()
		serializer = BasicinfoSerializer(user,many=True)
		#####################Query Generation#################################
		if request.data.get('search') and request.data.get('order_by'):
			key=request.data.get('search')
			order_by=request.data.get('order_by')
			order_type=request.data.get('order_type')
			if(order_type=='+'):
				order=order_by
			else:
				order='-'+order_by
			result = EngageboostProducts.objects.using(company_db).all().order_by(order).filter(Q(name__icontains=key)|Q(sku__icontains=key)|Q(visibility_id__icontains=key)|Q(cost_per_unit__icontains=key)|Q(default_price__icontains=key))
		elif request.data.get('search'):
			key=request.data.get('search')
			result = EngageboostProducts.objects.using(company_db).all().order_by('-id').filter(Q(name__icontains=key)|Q(sku__icontains=key)|Q(visibility_id__icontains=key)|Q(cost_per_unit__icontains=key)|Q(default_price__icontains=key))
		elif request.data.get('order_by'):
			order_by=request.data.get('order_by')
			order_type=request.data.get('order_type')
			if(order_type=='+'):
				order=order_by
			else:
				order='-'+order_by
			result = EngageboostProducts.objects.using(company_db).all().order_by(order)    
		else:
			result = EngageboostProducts.objects.using(company_db).all().order_by('-id')
		if visibility_id==4:
			result=result.filter(visibility_id=1)

		# result=result.filter(isblocked='n',isdeleted='n')
		result=result.filter(isdeleted='n')
		result_all = result.count()
		result1 = result.filter(isblocked='y').count()
		result2 = result.filter(isblocked='n').count()
		if request.data['status']:
			if request.data['status']=="n":
				result=result.filter(isblocked='n')
			elif request.data['status']=="y":
				result=result.filter(isblocked='y')
		else:
			result=result
		page = self.paginate_queryset(result)
		#####################Query Generation#################################
		userid=request.data['userid']
		users = EngageboostUsers.objects.using(company_db).get(id=userid)
		issuperadmin = users.issuperadmin
		role_id = users.role_id
		role_permission={}
		if issuperadmin=='Y':
			add='Y'
			edit='Y'
			delete='Y'
			status='Y'
			role_permission={"add":"Y","edit":"Y","delete":"Y","view":"Y","block":"Y","import_field":0,"export":0,"shipping_processes":0,"print":0}
		else:
			role_per = EngageboostRoleMenuPermissions.objects.using(company_db).get(role_id=role_id,master_id=menu_id,isblocked=0,isdeleted=0)
			role_permission={"add":role_per.add,"edit":role_per.edit,"delete":role_per.delete,"view":role_per.view,"block":role_per.block,"import_field":role_per.import_field,"export":role_per.export,"shipping_processes":role_per.shipping_processes,"print":role_per.print}
			add=role_per.add
			edit=role_per.edit
			delete=role_per.delete
			status=role_per.block
		#####################Layout#################################
		if page is not None:
			serializer_product = BasicinfoSerializer(page, many=True)
			row_dict={}
			row=[]
			if serializer_product.data:
				for serializer_row in serializer_product.data :
					row_dict=serializer_row
					
					product_id=serializer_row['id']
					brand_id=serializer_row['brand']
					supplier_id=serializer_row['supplier_id']
					fetchGlobalSettings=EngageboostGlobalSettings.objects.using(company_db).filter(website_id=1).first()
					sku_prefix = fetchGlobalSettings.sku_prefix if fetchGlobalSettings.sku_prefix else ""
					sku_suffix = fetchGlobalSettings.sku_suffix if fetchGlobalSettings.sku_suffix else ""
					row_dict['sku']=sku_prefix+serializer_row['sku']+sku_suffix
					# /////Category////////
					fetch_category=EngageboostProductCategories.objects.using(company_db).all().filter(product=product_id)
					categoryarr=[];
					catdict={}
					for cat in fetch_category:
						catdict=cat.category.name
						categoryarr.append(catdict)
					category=','.join([str(i) for i in categoryarr])
					row_dict['category']=category
					# ////////brand/////////
					brandarr=[];
					if brand_id:
						brands=brand_id.split(",")  
						for bid in brands:
							if bid:       
								fetch_brand=EngageboostBrandMasters.objects.using(company_db).filter(id=bid).first()
								if fetch_brand:
									brandarr.append(fetch_brand.name)
						brand=','.join([str(i) for i in brandarr])
						row_dict['brand']=brand
					else:   
						row_dict['brand']=''
					# ////////supplier/////////
					supplierarr=[];
					if supplier_id:
						supplier=supplier_id.split(",")  
						for sid in supplier:
							if sid: 
								#print(sid)      
								fetch_supplier=EngageboostSuppliers.objects.using(company_db).filter(id=sid).first()
								if fetch_supplier:
									supplierarr.append(fetch_supplier.name)
						supplier=','.join([str(i) for i in supplierarr])
						row_dict['supplier']=supplier 
					else:   
						row_dict['supplier']=''

					if serializer_row['visibility_id']==1:
						row_dict['visibility_id']='Catalog Search'
					else:
						row_dict['visibility_id']='Not Visible..'

					module='Products'
					screen_name='list'
					layout_fetch=EngageboostGridLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
					layout_header=layout_fetch.header_name.split("@@")
					layout_field=layout_fetch.field_name.split("@@")
					layout_check=EngageboostGridColumnLayouts.objects.using(company_db).filter(module=module,screen_name=screen_name).count()
					layout={}
					layout_arr=[]

					for header,field in zip(layout_header,layout_field):
						ex_layout_field=field.split(".")
						is_numeric_field=field.split("#")
						field_name=ex_layout_field[0]
						
						if len(is_numeric_field)>1:
							field_type=is_numeric_field[1]
							field_name=is_numeric_field[0]
						else:
							field_type=''	

						if len(ex_layout_field)>1:
							child_name=ex_layout_field[1]
							field_name=ex_layout_field[0]
						else:
							child_name=''
							
						if(layout_check):
							layout_column_fetch=EngageboostGridColumnLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
							layout_column_header=layout_column_fetch.header_name
							layout_column_field=layout_column_fetch.field_name

							if header in layout_column_header:
								status=1
							else:
								status=0
						else:
							status=1        
						layout={"title":header,"field":field_name,"child":child_name,"show":status,"field_type":field_type}
						layout_arr.append(layout)
					row.append(row_dict)
			else:
				module='Products'
				screen_name='list'
				layout_fetch=EngageboostGridLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
				layout_header=layout_fetch.header_name.split("@@")
				layout_field=layout_fetch.field_name.split("@@")
				layout_check=EngageboostGridColumnLayouts.objects.using(company_db).filter(module=module,screen_name=screen_name).count()
				layout={}
				layout_arr=[]

				for header,field in zip(layout_header,layout_field):
					ex_layout_field=field.split(".")
					is_numeric_field=field.split("#")
					field_name=ex_layout_field[0]
					
					if len(is_numeric_field)>1:
						field_type=is_numeric_field[1]
						field_name=is_numeric_field[0]
					else:
						field_type=''	

					if len(ex_layout_field)>1:
						child_name=ex_layout_field[1]
						field_name=ex_layout_field[0]
					else:
						child_name=''
						
					if(layout_check):
						layout_column_fetch=EngageboostGridColumnLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
						layout_column_header=layout_column_fetch.header_name
						layout_column_field=layout_column_fetch.field_name

						if header in layout_column_header:
							status=1
						else:
							status=0
					else:
						status=1        
					layout={"title":header,"field":field_name,"child":child_name,"show":status,"field_type":field_type}
					layout_arr.append(layout)
		#####################Layout#################################  
		pre_data={}
		final_data=[]
		pre_data['all']=result_all
		pre_data['inactive']=result1
		pre_data['active']=result2 
		pre_data['result']=row
		pre_data['layout']=layout_arr
		pre_data['role_permission']=role_permission
		final_data.append(pre_data)
		return self.get_paginated_response(final_data)

# class CustomerTaxClass is used to insert CustomerTaxClass
class MultipleBarcodes(generics.ListAPIView):
	def get(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		obj = EngageboostMultipleBarcodes.objects.using(company_db)
		objcount = obj.filter(product_id=pk).count()
		if objcount>0:
			creditObj = obj.filter(product_id=pk).all()
			serializer = MultipleBarcodeSerializer(creditObj, many=True)

			if(serializer): 
				data ={
						'status':1,
						'api_status':serializer.data,
					}
			else:
				data ={
						'status':0,
						'api_status':serializer.errors,
						'message':'Data Not Found',
					}
		else:
			data ={
					'status':0,
					'api_status':"",
					'message':'Data Not Found',
				}			
		return Response(data)

	def put(self, request, pk, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		has_multy=request.data['value']
		website_id=request.data['website_id']
		error = []
		ids = []
					
		for dt in has_multy:
			if not "barcode" in dt.keys() or dt['barcode']=="" or dt['barcode']==None:
				error.append("Enter EAN no")	 
			psku_count = EngageboostProducts.objects.filter(ean=dt['barcode']).count()
			msku_count = EngageboostMultipleBarcodes.objects.filter(barcode=dt['barcode']).exclude(product_id=pk).count()
			if psku_count>0 or msku_count>0:
				error.append({'ean':dt['barcode'],'msg':"Barcode already exists"})
		if len(error)==0:
			EngageboostMultipleBarcodes.objects.using(company_db).filter(product_id=pk).exclude(default_ean='y').delete()
			for dt in has_multy:
				d1={'created':date.today(),'modified':date.today(),'product_id':pk}
				serializer_data=dict(dt,**d1)
				if website_id:
					d2 = {"website_id":website_id}
					serializer_data=dict(serializer_data,**d2)


				EngageboostMultipleBarcodes.objects.using(company_db).create(**serializer_data)
				obj = EngageboostMultipleBarcodes.objects.using(company_db).latest('id')
				last_id = obj.id
				ids.append(last_id)
			data ={
					'status':1,
					'api_status':{"id":ids},
					'message':'Successfully Saved',
				}
			return Response(data)		
		else:
			data ={
				'status':0,
				'api_status':error,
				'message':'Something went wrong',
			}
			return Response(data)							

class ImportBarcodes(generics.ListAPIView):
	def post(self, request, *args, **kwargs):
		website_id = request.POST.get('website_id')
		if 'import_file' in request.FILES:
			file 		= request.FILES['import_file']
			
			rand 		= str(random.randint(1,99999))
			time_stamp  = str(int(datetime.now().timestamp()))
			file1 		= request.FILES['import_file']
			file_name 	= file1.name
			datas 		= []
			
			error 		= ""
				
			ext 		= file_name.split('.')[-1]
			new_file_name = 'barcodes_'+rand+time_stamp
			fs 			= FileSystemStorage()
			filename 	= fs.save('importfile/userimport/'+new_file_name+'.'+ext, file1)
			uploaded_file_url 	= fs.url(filename)
			BASE_DIR 			= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

			csvReader 	= xlrd.open_workbook(settings.BASE_DIR+uploaded_file_url)
			sheet 		= csvReader.sheet_by_index(0)
			length 		= len(sheet.col_values(0))
			arr_message = []
			for x in range(length):

				if x==0:
					pass
				else:	
					data        = []
					sku 		= ""
					barcode		= ""
					default_ean	= ""
					created 	= date.today() 
					modified 	= date.today()

					sku 		= str(sheet.col_values(0)[x])
					barcode 	= str(sheet.col_values(1)[x])
					default_ean	= sheet.col_values(2)[x]
					
					barcode 	= barcode.split('.')[0]
					sku 		= sku.split('.')[0]

					if sku=="" or barcode=="" or sku==None or barcode==None:
						data.append("Incomplete data") 

					pcount = EngageboostProducts.objects.filter(sku=sku).count()
					if pcount==0:
						data.append("Invalid product")
						
					sku_value 	= EngageboostProducts.objects.filter(sku=sku).first()
					psku_count 	  = EngageboostProducts.objects.filter(ean=barcode).count()
					msku_count 	  = EngageboostMultipleBarcodes.objects.filter(barcode=barcode).count()
					if psku_count>0 or msku_count>0:
						data.append("Barcode already exists")
					
					if len(data)>0:
						err_flag=1
						error = ",".join(data)
					else:
						err_flag=0
						error = "SUCCESS"	
					user = EngageboostTempMultipleBarcodes.objects.create(
										sku=sku,
										barcode=barcode,
										default_ean=default_ean,
										file_name=new_file_name+'.'+ext,
										err_flag = err_flag,
										error_text = error,	
										created=created,
										website_id = website_id,
										modified=modified)	
						
			# print(settings.BASE_DIR+uploaded_file_url)
			if os.path.exists(settings.BASE_DIR+uploaded_file_url):
				os.remove(settings.BASE_DIR+uploaded_file_url)

			data = {"status":1,"message":"Success","website_id":website_id,"file_name":new_file_name+'.'+ext}
			return Response(data)

class PreviewImportedBarcodes(generics.ListAPIView):
	def post(self, request, *args, **kwargs):
		company_db = loginview.db_active_connection(request)
		post_data = request.data
		fetch_all_data = []
		save_temp_img_to_product(request)
		if 'file_name' in post_data:
			fetch_all_data_cond = EngageboostTempMultipleBarcodes.objects.using(company_db).all().filter(file_name=post_data['file_name'],website_id=post_data['website_id'])
			if fetch_all_data_cond:
				fetch_all_datas = EngageboostTempMultipleBarcodesSerializer(fetch_all_data_cond,many=True)
				fetch_all_data = fetch_all_datas.data

				for fetch_data in fetch_all_data:
					if fetch_data['error_text']!="" and fetch_data['error_text']!=None:
						fetch_data['error_text']=fetch_data['error_text'].split(',')
				
		data = {"preview_data":fetch_all_data,"file_name":post_data['file_name'],"website_id":post_data['website_id']}
		return Response(data)

class SaveAllImportedBarcodes(generics.ListAPIView):
	def post(self, request, *args, **kwargs):
		company_db = loginview.db_active_connection(request)
		post_data = request.data
		website_id = post_data['website_id']
		selectedIds = post_data["selected_ids"].split(',')
		fetch_temp_datas = []
		datas = []
		
		tempObj = EngageboostTempMultipleBarcodes.objects.using(company_db).filter(id__in=selectedIds,err_flag=0,website_id=website_id)
		
		if tempObj.count()>0:

			fetch_temp_data_cond = tempObj.all()
			fetch_temp_data = EngageboostTempMultipleBarcodesSerializer(fetch_temp_data_cond,many=True)

			# for i in selectedIds:
			# 	fetch_temp_data_cond = EngageboostTempMultipleBarcodes.objects.using(company_db).filter(id=int(i),err_flag=0).first()
			# 	if fetch_temp_data_cond:
			# 		fetch_temp_data = EngageboostTempMultipleBarcodesSerializer(fetch_temp_data_cond,partial=True)
			# 		fetch_temp_datas.append(fetch_temp_data.data)

			for fetchtempdatas in fetch_temp_data.data:
				serializer_data = {}
				serializer_data = dict(serializer_data,**fetchtempdatas)

				sku_value = EngageboostProducts.objects.filter(sku=fetchtempdatas['sku']).first()
				
				current_time = timezone.now()
				d1 = {"created":current_time,"modified":current_time,"product_id":sku_value.id}

				serializer_data = dict(serializer_data,**d1)
				
				datas.append(serializer_data)
				
				serializer_data.pop('sku')
				serializer_data.pop('error_text')
				serializer_data.pop('err_flag')
				serializer_data.pop('file_name')
				serializer_data.pop('id')
				
				serializer = MultipleBarcodeSerializer(data=serializer_data,partial=True)		
				
				if serializer.is_valid():
					
					EngageboostMultipleBarcodes.objects.using(company_db).create(**serializer_data)
					responseDatas = {"status":1,"api_response":datas,"message":'Barcodes Saved'}
				else:
					data ={'status':0,'api_status':serializer.errors,'message':'Error Occured'}
					datas.append(data)

					responseDatas = {"status":0,"api_response":datas,"message":'Error Occured in Barcodes'}
		else:
			responseDatas = {"status":0,"api_response":[],"message":'Data not exists'}
		EngageboostTempMultipleBarcodes.objects.using(company_db).filter(file_name=post_data['file_name']).delete()
		return Response(responseDatas)		

def amazons3_fileupload200(file_name):
	
	conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)

	f200 = open(settings.MEDIA_ROOT+'/product/200x200/'+file_name,'rb')
	print("================================",settings.AMAZON_S3_FOLDER+'/product/200x200/'+file_name)
	val = conn.upload(settings.AMAZON_S3_FOLDER+'/product/200x200/'+file_name,f200,settings.AMAZON_S3_BUCKET)
	
	return 0
def amazons3_fileupload800(file_name):
	conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)	
	f800 = open(settings.MEDIA_ROOT+'/product/800x800/'+file_name,'rb')
	val = conn.upload(settings.AMAZON_S3_FOLDER+'/product/800x800/'+file_name,f800,settings.AMAZON_S3_BUCKET)
	
	return 0
def amazons3_fileupload100(file_name):
	conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)
	f100 = open(settings.MEDIA_ROOT+'/product/100x100/'+file_name,'rb')
	val = conn.upload(settings.AMAZON_S3_FOLDER+'/product/100x100/'+file_name,f100,settings.AMAZON_S3_BUCKET)	
	
	return 0

def amazons3_fileupload80(file_name):
	conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)
	f80 = open(settings.MEDIA_ROOT+'/product/80x80/'+file_name,'rb')
	val = conn.upload(settings.AMAZON_S3_FOLDER+'/product/80x80/'+file_name,f80,settings.AMAZON_S3_BUCKET)	
	
	return 0
def amazons3_fileupload400(file_name):
	conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)
	f400 = open(settings.MEDIA_ROOT+'/product/400x400/'+file_name,'rb')
	val = conn.upload(settings.AMAZON_S3_FOLDER+'/product/400x400/'+file_name,f400,settings.AMAZON_S3_BUCKET)	
		
	return 0
def delete_create_image_from_local_folder():

	if os.path.exists(settings.BASE_DIR+'/media/product/'):
		shutil.rmtree(settings.BASE_DIR+'/media/product/')

	directory_prduct1=settings.BASE_DIR+'/media/'+'product/100x100/'
	directory_prduct2=settings.BASE_DIR+'/media/'+'product/200x200/'
	directory_prduct3=settings.BASE_DIR+'/media/'+'product/800x800/'
	directory_prduct5=settings.BASE_DIR+'/media/'+'product/80x80/'
	directory_prduct6=settings.BASE_DIR+'/media/'+'product/400x400/'
	directory_prduct7=settings.BASE_DIR+'/media/'+'product/temp/'

	
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

	if not os.path.exists(directory_prduct7):
		os.makedirs(directory_prduct7)	 
	 
def save_temp_img_to_product(request):
	import urllib.request
	from PIL import Image

	company_db = loginview.db_active_connection(request)
	obj = EngageboostTempProductimages.objects.using(company_db)
	objcount = obj.count()
	
	if objcount>0:
		tempImgsObj = obj.all()
		tempImgs = TempProductimagesSerializer(tempImgsObj,many=True)
		for tempImg in tempImgs.data:
			
			upload = common.download_img_from_temp(tempImg['img'])
			
			image = Image.open(settings.BASE_DIR+upload['path'])
			try:
				image = Image.open(settings.BASE_DIR+upload['path']).convert('RGB')
			except:
				pass
			new_image_name = upload['image_name']
			cover_image = upload['image_name']
			######### Resize Image ##############
			imageresizeon= EngageboostGlobalSettings.objects.using(company_db).get(website_id=1)
			width_origenal, height_origenal=image.size
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
			new_image_file = settings.MEDIA_ROOT+'/product/100x100/'+new_image_name
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
			new_image_file = settings.MEDIA_ROOT+'/product/80x80/'+new_image_name
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
			new_image_file = settings.MEDIA_ROOT+'/product/400x400/'+new_image_name
			img_anti.save(new_image_file)
			
			# ICON 200X200
			amazons3_fileupload400(cover_image)
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
			img_anti = image.resize((width, height), Image.ANTIALIAS)
			new_image_file = settings.MEDIA_ROOT+'/product/200x200/'+new_image_name
			img_anti.save(new_image_file)
			
			# Banner 800x800
			amazons3_fileupload200(cover_image)
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
			new_image_file = settings.MEDIA_ROOT+'/product/800x800/'+new_image_name
			img_anti.save(new_image_file)
			amazons3_fileupload800(cover_image)
			######### Resize Image ##############
			
			serializer_data = {}
			serializer_data = dict(serializer_data,**tempImg)
			d1 = {'img':cover_image}
			serializer_data = dict(serializer_data,**d1)
			
			serializer = ProductImagesSerializer(data=serializer_data,partial=True)

			if serializer.is_valid():
				serializer.save()
	
	delete_create_image_from_local_folder()
	return 0

class GetBarcodeDetails(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = JSONParser().parse(request)	
		bid = requestdata['id']
		condition = EngageboostMultipleBarcodes.objects.filter(id=bid).first()
		if condition:
			barcodeDetails = MultipleBarcodeSerializer(condition)
			data = {"status":1,"data":barcodeDetails.data}
		else:
			data = {"status":0,"data":"No data found"}
		return Response(data)

def save_product_lang(requestdata):
	if requestdata:
		for langdata in requestdata:
			rs_check_exist = EngageboostProductMastersLang.objects.filter(product_id=langdata['product_id'], language_code = langdata['language_code'], field_name = langdata['field_name'], isblocked='n', isdeleted='n').first()
			if rs_check_exist:
				EngageboostProductMastersLang.objects.filter(product_id=langdata['product_id'], language_code = langdata['language_code'], field_name = langdata['field_name'], isblocked='n', isdeleted='n').update(**langdata)
			else:
				EngageboostProductMastersLang.objects.create(**langdata)
	else:
		data = {}