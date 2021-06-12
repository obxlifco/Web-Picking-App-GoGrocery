from webservices.models import *
from django.http import Http404
from webservices.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import date,datetime
from rest_framework import generics
from itertools import chain
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Q, Count
from django.core.files.storage import FileSystemStorage
from webservices.views import loginview
# import the necessary packages
import webservices.views.product.BasicInformation as basicinformation
import datetime
import requests
from webservices.views.common import common
from webservices.views.common.threading import *
from rest_framework.decorators import api_view, permission_classes
import tinys3
import sys
import traceback
import json
import csv
from webservices.views.emailcomponent import emailcomponent
from elasticsearch import helpers

@csrf_exempt
def save_temp_img_to_product():
	print('Image cron Running=========')
	process_temp_image()												
					
	data = {
		"status":1
	}
	return JsonResponse(data)

# @postpone
def process_temp_image():
	# return 1
	import urllib.request
	from PIL import Image
	offset = 0
	limit = 100000
	company_name = ""
	s3folder_name = ""
	product_ids = []
	temp_Img_ids = []

	img_resolutions = [80,100,200,400,800] #Resolutions List

	companyObj = EngageboostCompanies.objects

	companyCount = companyObj.count()
	# companyCount = 0
	if companyCount>0:
		companies = companyObj.all().iterator()
		for company in companies:
						
			websteObj = EngageboostCompanyWebsites.objects.filter(engageboost_company_id=company.id)

			if websteObj.count()>0:
				websites = websteObj.all().iterator()

				for website in websites:

					company_name = website.company_name
					s3folder_name = website.s3folder_name

					website_id = website.id

					obj = EngageboostTempProductimages.objects.filter(website_id=website_id).filter(error_msg=None).exclude(img='0').order_by("-id")[0:100]
					objcount = obj.count()
					# objcount = 0
					if objcount>0:
						tempImgsObj = obj.all().iterator()
						tempImgs = TempProductimagesSerializer(tempImgsObj,many=True)
						for tempImg in tempImgs.data:
							try:
								print("Image Link:-    ",tempImg['img'])
								upload = common.download_img_from_temp(tempImg['img'])
								# print("Path===============",settings.BASE_DIR+upload['path'])
								image = Image.open(settings.BASE_DIR+upload['path'])

								try:
									image = Image.open(settings.BASE_DIR+upload['path']).convert('RGB')
								except:
									pass
									
								new_image_name = upload['image_name']
								cover_image = upload['image_name']
								
								######### Resize Image ##############
								imageresizeon= EngageboostGlobalSettings.objects.get(website_id=1)
								width_origenal, height_origenal=image.size
								
								for imgresolution in img_resolutions:
									imgresolutionstr = str(imgresolution)

									# ICON 100X100
									if imageresizeon.image_resize =='Width':
										if width_origenal >imgresolution:
											ratio = width_origenal/height_origenal
											width=imgresolution
											height=int(imgresolution*height_origenal/width_origenal)
										else:
											width=width_origenal
											height=height_origenal	

									if imageresizeon.image_resize =='Height':
										if height_origenal >imgresolution:
											ratio = height_origenal/width_origenal
											width=int(imgresolution*width_origenal/height_origenal)
											height=imgresolution
										else:
											width=width_origenal
											height=height_origenal
									
									img_anti = image.resize((width, height), Image.ANTIALIAS)
									new_image_file = settings.MEDIA_ROOT+'/product/'+imgresolutionstr+'x'+imgresolutionstr+'/'+new_image_name
									img_anti.save(new_image_file)
									common.amazons3_global_fileupload(cover_image,imgresolutionstr,'product',company_name,s3folder_name)

								######### Resize Image ##############
								
								serializer_data = {}
								serializer_data = dict(serializer_data,**tempImg)
								d1 = {'img':cover_image}
								serializer_data = dict(serializer_data,**d1)
								
								if serializer_data['is_cover']==1:
									
									EngageboostProductimages.objects.filter(website_id=website_id,product_id=serializer_data['product']).update(is_cover=0)

								serializer = ProductImagesSerializer(data=serializer_data,partial=True)

								if serializer.is_valid():
									serializer.save()

									product_ids.append(serializer_data['product'])
									temp_Img_ids.append(tempImg['id'])
									#
									# product_images = common.get_product_images(serializer_data['product'])
									# elastic = common.change_field_value_elastic(serializer_data['product'],'EngageboostProducts',{'product_images':product_images})
									#
									# EngageboostTempProductimages.objects.filter(id=tempImg['id']).delete()

							except Exception as error :
								trace_back = sys.exc_info()[2]
								line = trace_back.tb_lineno
								data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
								EngageboostTempProductimages.objects.filter(id=tempImg['id']).update(error_msg=str(error))
								print("Local temp image not found ==========",data)
								print(".")
								print(".")
								print(".")

	image_to_elastic(temp_Img_ids, product_ids)

	print("Deleting temp Image...................")
	common.delete_create_image_from_local_folder(img_resolutions,'product')
	print("==============Temp Image Deleted==============")
	return 1

def image_to_elastic(temp_Img_ids, product_ids):
	es = common.connect_elastic()
	delete_temp_ids = []
	docs = []
	datas = []
	data_string = []

	try:
		if len(temp_Img_ids) > 0 and len(product_ids) > 0:
			for prod_id in product_ids:
		# if len(temp_Img_ids) > 0 and len(product_ids) > 0:
		# 	for product_id in rs_stock_product[start_pos:end_pos]:
				id_string = {
					"_id": prod_id,
					"_source": False
				}
				data_string.append(id_string)

			table_name = 'EngageboostProducts'
			module_name = common.get_index_name_elastic(product_ids[0], table_name)
			prod_exists = es.mget(body=json.dumps({"docs": data_string}), index=module_name, doc_type="data")

			for item in prod_exists['docs']:
				cm_id = item['_id']

				product_images_temp = EngageboostTempProductimages.objects.filter(id__in=temp_Img_ids, product=cm_id)
				if product_images_temp.count() > 0:
					for prod_img in product_images_temp:
						delete_temp_ids.append(prod_img.id)
				# elastic = common.change_field_value_elastic(ids, 'EngageboostProducts',
				# 											{'product_images': product_images})

				if item['found'] == True:

					product_images = common.get_product_images(cm_id)
					data = {"product_images": product_images}

					# data = get_product_field_value_for_elastic(cm_id, field_name)

					header = {
						"_op_type": 'update',
						"_index": module_name,
						"_type": "data",
						"_id": cm_id,
						"doc": data
					}

					docs.append(header)

				else:
					now_item = EngageboostProducts.objects.filter(id=cm_id)
					serializer_class = common.get_serializer_class_elastic(table_name)
					# serializer = serializer_class(item,partial=True)
					serializer = serializer_class(now_item, partial=True)
					data = serializer.data
					# print("Data Formatting Start=====",datetime.now())
					# data = common.setUpLangDataToSerializer(data)
					data = common.format_serialized_data(table_name, data)

					header = {
						"_index": module_name,
						"_type": "data",
						"_id": cm_id,
						"_source": data
					}

					docs.append(header)
	except Exception as error:
		trace_back = sys.exc_info()[2]
		line = trace_back.tb_lineno
		datas.append(
			{"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),
			 "message": str(error)})
	finally:
		# if len(delete_temp_ids)>0:
		EngageboostTempProductimages.objects.filter(id__in=delete_temp_ids).delete()

		obj = helpers.bulk(es, docs)
		datas.append({"obj": obj})
		response = emailcomponent.testmail('binayak.santra@navsoft.in',
										   "Warehouse product image sync @@@process_temp_imageLive@@@",
										   'Data preparation Completed and Pushed to Elastic,' + ' @ ' + str(
											   datetime.datetime.now()) + ' datas=====>' + str(datas))

		response = emailcomponent.testmail('lifco.onboard@gmail.com',
												   "Warehouse product image sync",
												   'Data preparation Completed and Pushed to Elastic,' + ' @ ' + str(
													   datetime.datetime.now()) + ' datas=====>' + str(obj))

	return 0

# process_temp_image()

@csrf_exempt
def product_stock_cron_old():
	import datetime
	print('Stock cron Running=========')
	datas=[]
	temp_stock_file_condition = EngageboostImportedTempProductStocks.objects.filter(is_imported=0).order_by("-id").all().iterator()
	# print(temp_stock_file_condition.query)
	if temp_stock_file_condition:				
		stock_temp_files_datas = ImportedTempProductStocksSerializer(temp_stock_file_condition,many=True)

		for stock_temp_files_data in stock_temp_files_datas.data:
			# return Response(stock_temp_files_data['sku'])
			website_id = stock_temp_files_data['website_id']
			try:
				stock_temp_files_data['sku'] = stock_temp_files_data['sku'].split('.')
				stock_temp_files_data['sku'] = stock_temp_files_data['sku'][0]
			except:
				pass
			
			try:
				stock_temp_files_data['sku'] = stock_temp_files_data['sku'].strip()
			except:
				pass	

			product_condition =  EngageboostProducts.objects.filter(sku=stock_temp_files_data['sku'],website_id=website_id,isdeleted='n').first()  
			
			if product_condition:
				# product_details = BasicinfoSerializer(product_condition,partial=True)
				# product_id = product_details.data['id']
				product_id = product_condition.id
			else:
				product_id = 0

			
			try:
				stock_temp_files_data['warehouse_name'] = str(stock_temp_files_data['warehouse_name'])
			except:
				pass
				
			try:
				stock_temp_files_data['warehouse_name'] = stock_temp_files_data['warehouse_name'].split('.')
				stock_temp_files_data['warehouse_name'] = stock_temp_files_data['warehouse_name'][0]
			except:
				pass
			try:
				stock_temp_files_data['warehouse_name'] = stock_temp_files_data['warehouse_name'].strip()
			except:
				pass	

			warehouse_condition = EngageboostWarehouseMasters.objects.filter(code=stock_temp_files_data['warehouse_name'],website_id=website_id,isdeleted='n').first()
			if warehouse_condition:
				# warehouse_data = WarehousemastersSerializer(warehouse_condition,partial=True)
				# warehouse_id = warehouse_data.data['id']
				warehouse_id = warehouse_condition.id	
			else:
				warehouse_id = 0	

			if stock_temp_files_data['quantity'] > 0:
				quantity = stock_temp_files_data['quantity']
			else:
				quantity = 0	

			if stock_temp_files_data['lot_number'] != '':
				lot_number = 1
			else:
				lot_number = 0

			if stock_temp_files_data['rack_number'] != '':
				rac_number = 1
			else:
				rac_number = 0	

			if stock_temp_files_data['safety_stock'] > 0:
				safety_stock = stock_temp_files_data['safety_stock']
			else:
				safety_stock = 0			
			
			print(product_id,warehouse_id,quantity)						
			if int(product_id) > 0 and int(warehouse_id) > 0 and int(quantity) >= 0:
				prd_stock_condition = EngageboostProductStocks.objects.filter(product_id=product_id,warehouse_id=warehouse_id).first()
				if prd_stock_condition:
					check_stock_data = StockViewSerializer(prd_stock_condition,partial=True)
					if check_stock_data.data['virtual_stock'] != '':
						virtual_stock = check_stock_data.data['virtual_stock']
					else:
						virtual_stock =  0

					total_valid_qty = virtual_stock+safety_stock;
					
					# real_stock = ((quantity+check_stock_data.data['stock'])-(virtual_stock+check_stock_data.data['safety_stock']+safety_stock))
					# safety_stock = safety_stock+check_stock_data.data['safety_stock']
					# quantity = quantity+check_stock_data.data['stock']

					real_stock = ((quantity)-(virtual_stock+safety_stock))

					safety_stock = safety_stock
					quantity = quantity

					if int(real_stock)<0:
						real_stock = 0
						quantity = check_stock_data.data['stock']

					serializer_data = dict()
					current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
					d1={"product_id":product_id,"warehouse_id":warehouse_id,"stock":quantity,"safety_stock":safety_stock,"real_stock":real_stock,"islot":lot_number,"islabel":rac_number,"modified":str(current_time)}
					serializer_data=dict(serializer_data,**d1)

					product_stock_table_id = EngageboostProductStocks.objects.get(id=check_stock_data.data['id'])
					serializer = StockViewSerializer(product_stock_table_id, data=serializer_data,partial=True)
					if serializer.is_valid():
						serializer.save()
						product_stock = common.get_product_stock(product_id)
						print("===================",product_stock)
						elastic = common.change_field_value_elastic(product_id,'EngageboostProducts',{'inventory':product_stock})

						data ={'status':1,'api_status':'Stock Updated','message':'Stock Updated'}
					else:
						data ={'status':0,'api_status':serializer.errors,'message':'Error Occured In Update'}

					datas.append(data)
					# return Response(data)
				else:
					virtual_stock =  0
					real_stock = quantity
					safety_stock = 0
					quantity = quantity

					# has_record = EngageboostProductStocks.objects.last()
					# if has_record:
					# 	last_entry_of_table = EngageboostProductStocks.objects.order_by('-id').latest('id')
					# 	row_id = int(last_entry_of_table.id)+int(1)
					# else:
					# 	row_id = 1

					serializer_data = dict()
					current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
					d1={"product_id":product_id,"warehouse_id":warehouse_id,"stock":quantity,"safety_stock":safety_stock,"real_stock":real_stock,"islot":lot_number,"islabel":rac_number,"created":str(current_time),"modified":str(current_time)}
					serializer_data=dict(serializer_data,**d1)

					print("serializer_data==============",serializer_data)
					serializer = StockViewSerializer(data=serializer_data,partial=True)
					if serializer.is_valid():
						# serializer.save()
						stockObj = EngageboostProductStocks.objects.create(**serializer_data)

						product_stock = common.get_product_stock(product_id)
						print("product_stock===================",product_stock)
						elastic = common.change_field_value_elastic(product_id,'EngageboostProducts',{'inventory':product_stock})

						data ={'status':1,'api_status':stockObj.id,'message':'Stock Inserted'}
					else:
						data ={'status':0,'api_status':serializer.errors,'message':'Error Occured In Insert'}

					datas.append(data)
					# return Response(data)
				# EngageboostImportedTempProductStocks.objects.filter(id=stock_temp_files_data['id']).update(is_imported="Y")
				EngageboostImportedTempProductStocks.objects.filter(id=stock_temp_files_data['id']).delete()
			else:
				EngageboostImportedTempProductStocks.objects.filter(id=stock_temp_files_data['id']).update(is_imported=1)
				data ={'status':0,'api_status':'Error Occured','message':'Either product is not exists or warehouse is not exists or error in quantity'}
				datas.append(data)
				# return Response(data)

		if datas:
			data ={'status':1,'api_status':datas}

		else:
			data ={'status':0,'api_status':datas}
		print("************** Cron data ************")
		print(data);
		return JsonResponse(data)
	else:
		data ={'status':0,'api_status':'All Stock Files Imported','message':'All Stock Files Imported'}
		return JsonResponse(data)

@csrf_exempt
def product_stock_cron():
	import datetime
	print('Stock cron Running=========')
	datas = []
	docs = []
	tempDataId = []
	es = common.connect_elastic()

	table_name = 'EngageboostProducts'

	module_name = ""
	response = emailcomponent.testmail('binayak.santra@navsoft.in',
									   "Data Preparation Initiated @@@product_stock_cron_live123@@@",
									   'Data preparation Initiated ' + str(
										   datetime.datetime.now()))
	response = emailcomponent.testmail('lifco.onboard@gmail.com',
									   "Data Preparation Initiated @@@product_stock_cron_live123@@@",
									   'Data preparation Initiated ' + str(
										   datetime.datetime.now()))

	try:
		# temp_stock_file_condition = EngageboostImportedTempProductStocks.objects.filter(is_imported=0).all().iterator()
		temp_stock_file_condition = EngageboostImportedTempProductStocks.objects.filter(is_imported=0).order_by('id')[:3000]
		# temp_stock_file_condition = EngageboostImportedTempProductStocks.objects.filter(is_imported=0).all()
		# print(temp_stock_file_condition.query)
		if temp_stock_file_condition:
			# print("=======temp_stock_file_condition======")
			stock_temp_files_datas = ImportedTempProductStocksSerializer(temp_stock_file_condition, many=True)

			# module_name = common.get_index_name_elastic(product_ids[0], table_name)
			for stock_temp_files_data in stock_temp_files_datas.data:
				# return Response(stock_temp_files_data['sku'])
				website_id = stock_temp_files_data['website_id']
				try:
					stock_temp_files_data['sku'] = stock_temp_files_data['sku'].split('.')
					stock_temp_files_data['sku'] = stock_temp_files_data['sku'][0]
				except:
					pass

				try:
					stock_temp_files_data['sku'] = stock_temp_files_data['sku'].strip()
				except:
					pass

				product_condition = EngageboostProducts.objects.filter(sku=stock_temp_files_data['sku'],
																	   website_id=website_id, isdeleted='n').first()

				# # -----Binayak Start 16-02-2021-----#
				# if module_name == "":
				# 	module_name = common.get_index_name_elastic(product_condition.id, table_name)
				# # -----Binayak End 16-02-2021-----#


				if product_condition:
					# product_details = BasicinfoSerializer(product_condition,partial=True)
					# product_id = product_details.data['id']
					product_id = product_condition.id
					module_name = common.get_index_name_elastic(product_condition.id, table_name)
				else:
					product_id = 0

				try:
					stock_temp_files_data['warehouse_name'] = str(stock_temp_files_data['warehouse_name'])
				except:
					pass

				try:
					stock_temp_files_data['warehouse_name'] = stock_temp_files_data['warehouse_name'].split('.')
					stock_temp_files_data['warehouse_name'] = stock_temp_files_data['warehouse_name'][0]
				except:
					pass
				try:
					stock_temp_files_data['warehouse_name'] = stock_temp_files_data['warehouse_name'].strip()
				except:
					pass

				warehouse_condition = EngageboostWarehouseMasters.objects.filter(
					code=stock_temp_files_data['warehouse_name'], website_id=website_id, isdeleted='n').first()
				if warehouse_condition:
					# warehouse_data = WarehousemastersSerializer(warehouse_condition,partial=True)
					# warehouse_id = warehouse_data.data['id']
					warehouse_id = warehouse_condition.id
				else:
					warehouse_id = 0

				if stock_temp_files_data['quantity'] > 0:
					quantity = stock_temp_files_data['quantity']
				else:
					quantity = 0

				if stock_temp_files_data['lot_number'] != '':
					lot_number = 1
				else:
					lot_number = 0

				if stock_temp_files_data['rack_number'] != '':
					rac_number = 1
				else:
					rac_number = 0

				if stock_temp_files_data['safety_stock'] > 0:
					safety_stock = stock_temp_files_data['safety_stock']
				else:
					safety_stock = 0

				print(product_id,warehouse_id,quantity)
				if int(product_id) > 0 and int(warehouse_id) > 0 and int(quantity) >= 0:
					prd_stock_condition = EngageboostProductStocks.objects.filter(product_id=product_id,
																				  warehouse_id=warehouse_id).first()
					if prd_stock_condition:
						# print("====inside prd_stock_condition====")
						check_stock_data = StockViewSerializer(prd_stock_condition, partial=True)
						if check_stock_data.data['virtual_stock'] != '':
							virtual_stock = check_stock_data.data['virtual_stock']
						else:
							virtual_stock = 0

						total_valid_qty = virtual_stock + safety_stock;

						# real_stock = ((quantity+check_stock_data.data['stock'])-(virtual_stock+check_stock_data.data['safety_stock']+safety_stock))
						# safety_stock = safety_stock+check_stock_data.data['safety_stock']
						# quantity = quantity+check_stock_data.data['stock']

						real_stock = ((quantity) - (virtual_stock + safety_stock))

						safety_stock = safety_stock
						quantity = quantity

						if int(real_stock) < 0:
							real_stock = 0
							quantity = check_stock_data.data['stock']

						serializer_data = dict()
						current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
						d1 = {"product_id": product_id, "warehouse_id": warehouse_id, "stock": quantity,
							  "safety_stock": safety_stock, "real_stock": real_stock, "islot": lot_number,
							  "islabel": rac_number, "modified": str(current_time)}
						serializer_data = dict(serializer_data, **d1)

						product_stock_table_id = EngageboostProductStocks.objects.get(id=check_stock_data.data['id'])
						serializer = StockViewSerializer(product_stock_table_id, data=serializer_data, partial=True)
						if serializer.is_valid():
							serializer.save()
							product_stock = common.get_product_stock(product_id)
							# print("===================",product_stock)
							# elastic = common.change_field_value_elastic(product_id, 'EngageboostProducts',
							# 											{'inventory': product_stock})

							data = {'inventory': product_stock}

							# print("======elastic======", data)
							# return
							header = {
								"_op_type": 'update',
								"_index": module_name,
								"_type": "data",
								"_id": product_id,
								"doc": data
							}
							docs.append(header)
							tempDataId.append(stock_temp_files_data["id"])
							# print("serializer=========>", stock_temp_files_data)
							# print("header=========>", header)
							# return

							# data = {'status': 1, 'api_status': 'Stock Updated', 'message': 'Stock Updated'}
						else:
							print('====not valid====')
							# data = {'status': 0, 'api_status': serializer.errors, 'message': 'Error Occured In Update'}

						# datas.append(data)
					# return Response(data)
					else:
						virtual_stock = 0
						real_stock = quantity
						safety_stock = 0
						quantity = quantity

						# has_record = EngageboostProductStocks.objects.last()
						# if has_record:
						# 	last_entry_of_table = EngageboostProductStocks.objects.order_by('-id').latest('id')
						# 	row_id = int(last_entry_of_table.id)+int(1)
						# else:
						# 	row_id = 1

						serializer_data = dict()
						current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
						d1 = {"product_id": product_id, "warehouse_id": warehouse_id, "stock": quantity,
							  "safety_stock": safety_stock, "real_stock": real_stock, "islot": lot_number,
							  "islabel": rac_number, "created": str(current_time), "modified": str(current_time)}
						serializer_data = dict(serializer_data, **d1)

						serializer = StockViewSerializer(data=serializer_data, partial=True)
						if serializer.is_valid():
							serializer.save()

							product_stock = common.get_product_stock(product_id)
							# print("===================",product_stock)
							# elastic = common.change_field_value_elastic(product_id, 'EngageboostProducts',
							# 											{'inventory': product_stock})

							data = {'inventory': product_stock}

							header = {
								"_op_type": 'update',
								"_index": module_name,
								"_type": "data",
								"_id": product_id,
								"doc": data
							}

							docs.append(header)
							tempDataId.append(stock_temp_files_data["id"])

							# data = {'status': 1, 'api_status': serializer.data['id'], 'message': 'Stock Inserted'}
						else:
							data = {'status': 0, 'api_status': serializer.errors, 'message': 'Error Occured In Insert'}
							EngageboostImportedTempProductStocks.objects.filter(id=stock_temp_files_data['id']).delete()

							datas.append(data)
					# return Response(data)
					# EngageboostImportedTempProductStocks.objects.filter(id=stock_temp_files_data['id']).update(is_imported="Y")
					# EngageboostImportedTempProductStocks.objects.filter(id=stock_temp_files_data['id']).delete()
				else:
					# EngageboostImportedTempProductStocks.objects.filter(id=stock_temp_files_data['id']).update(
					# 	is_imported=1)
					# data = {'status': 0, 'api_status': 'Error Occured',
					# 		'message': 'Either product is not exists or warehouse is not exists or error in quantity'}

					EngageboostImportedTempProductStocks.objects.filter(id=stock_temp_files_data['id']).update(
						is_imported=1)
					data = {'status': 0, 'api_status': 'Error Occured for ' + str(stock_temp_files_data['id']),
							'message': 'Either product is not exists or warehouse is not exists or error in quantity'}

					datas.append(data)
			# return Response(data)

			#-----Binayak Start 16-02-2021-----#
			# response = emailcomponent.testmail('binayak.santra@navsoft.in',
			# 								   "Data Preparation Completed @@@product_stock_cron_live123@@@",
			# 								   'Data preparation Completed ' + str(
			# 									   datetime.datetime.now()))

			datas.append({"msg": "Success"})
			#-----Binayak End 16-02-2021-----#
			if datas:
				data = {'status': 1, 'api_status': datas}

			else:
				data = {'status': 0, 'api_status': datas}
			print("************** Cron data ************")
			# print(data);
			# return JsonResponse(data)
		else:
			data = {'status': 0, 'api_status': 'All Stock Files Imported', 'message': 'All Stock Files Imported'}
			# return JsonResponse(data)
	except Exception as error:
		trace_back = sys.exc_info()[2]
		line = trace_back.tb_lineno
		datas.append({"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),
				 "message": str(error)})
		# EngageboostTempProductPrice.objects.filter(id=serializer_data['id']).update(error_text=str(error), err_flag=1)

	finally:
		print('=======in finally product_stock_cron ========')
		# print("=======docs========", docs)
		obj = helpers.bulk(es, docs)
		EngageboostImportedTempProductStocks.objects.filter(id__in=tempDataId).update(
			is_imported=1)
		datas.append({"obj": obj})
		# EngageboostTempProductPrice.objects.filter(id__in=tempDataId).update(error_text="SUCCESS")
		response = emailcomponent.testmail('binayak.santra@navsoft.in',
										   "Data Pushed to Elastic @@@product_stock_cron_live123@@@",
										   'Data preparation Completed and Pushed to Elastic, PRODUCT_COUNT =====>' + str(
											   len(tempDataId)) + ' @ ' + str(datetime.datetime.now()) + ' DATA=====> ' + str(datas))
		response = emailcomponent.testmail('lifco.onboard@gmail.com',
										   "Data Pushed to Elastic @@@product_stock_cron_live123@@@",
										   'Data preparation Completed and Pushed to Elastic, PRODUCT_COUNT =====>' + str(
											   len(tempDataId)) + ' @ ' + str(datetime.datetime.now()) + ' DATA=====> ' + str(obj))

		print("Deleting temp price...................")
		return Response(datas)

# product_stock_cron()

def delete_images():
	all_products = EngageboostProductimages.objects.filter(~Q(product_id=3513)).distinct('product_id').all().order_by("-product_id").values_list('product_id',flat=True)

	for product_id in all_products:
		print("Product_id=====",product_id)
		image_count = EngageboostProductimages.objects.filter(product_id=product_id,is_cover=1)

		if image_count.count()>=1:
			first_image = image_count.first()
			first_image_id = first_image.id
			exist_image = EngageboostProductimages.objects.filter(product_id=product_id)
			delete_image = exist_image.filter(~Q(id=first_image_id))
			if delete_image.count()>0:
				print("Total Records=====",exist_image.count(),"records")
				print("Have to delete=====",delete_image.count(),"records")
				delete_image = delete_image.delete()
				# delete_image = delete_image.all().values_list('id',flat=True)
				# EngageboostProductimages.objects.filter(id__in=delete_image).delete()
		elif image_count.count()==0:
			image_count = EngageboostProductimages.objects.filter(product_id=product_id,is_cover=0)
			delete_image = image_count
			if delete_image.count()>0:
				print("Total Records=====",delete_image.count(),"records")
				print("Have to delete=====",delete_image.count(),"records")
				delete_image = delete_image.delete()
				# delete_image = delete_image.all().values_list('id',flat=True)
				# EngageboostProductimages.objects.filter(id__in=delete_image).delete()
		# print("Have to delete=====",delete_image)	
	print("Complete=====")	
	return 1
# delete_images()
#.filter(Q(product_id=3475))
def delete_price():
	all_products = EngageboostChannelCurrencyProductPrice.objects.filter(warehouse_id=33).distinct('product_id','warehouse_id','product_price_type_id').all().values('id','product_id','warehouse_id','product_price_type_id')
	total_pending = 0
	for product_id in all_products:
		warehouse_id = product_id['warehouse_id']
		productID = product_id['product_id']
		product_price_type_id = product_id['product_price_type_id']
		image_count = EngageboostChannelCurrencyProductPrice.objects.filter(warehouse_id=warehouse_id,product_price_type_id=product_price_type_id,product_id=productID).order_by('-id')
		if image_count.count()>1:
			# print("ChannelCurrencyProductPrice id=====",product_id['id'])
			# print("warehouse_id=====",product_id['warehouse_id'])
			# print("Product_id=====",product_id['product_id'])
			# print("product_price_type_id=====",product_id['product_price_type_id'])
			first_image = image_count.first()
			first_image_id = first_image.id
			exist_image = EngageboostChannelCurrencyProductPrice.objects.filter(warehouse_id=warehouse_id,product_price_type_id=product_price_type_id,product_id=productID)
			delete_image = exist_image.filter(~Q(id=first_image_id))
			if delete_image.count()>0:
				# print("Total Records=====",exist_image.count(),"records")
				# print("Have to delete=====",delete_image.count(),"records")
				delete_image = delete_image.delete()
				print("ChannelCurrencyProductPrice id=====",first_image_id)
	print("Complete=====")	
	return 1
# delete_price()		


@csrf_exempt
def category_product_stock(request):
	print('check_category_product_stock Running=========')
	check_category_product_stock(2)

	data = {
		"status": 1
	}
	return JsonResponse(data)



@postpone
def check_category_product_stock(email_send=1):
	catwar = EngageboostCategoryWarehouse.objects.filter(isdeleted='n', warehouse_id__isdeleted='n',
														 category_id__isdeleted='n').order_by("warehouse_id") #[0:30]
	all_data = []
	if catwar.count() > 0:
		catwar = catwar.values("id", "category_id", "category_id__name", "warehouse_id",
							   "warehouse_id__name").all().iterator()

		for item in catwar:
			print(item)
			checkParent = EngageboostCategoryMasters.objects.filter(isdeleted='n', parent_id=item["category_id"])
			if checkParent.count() == 0:
				catprod = EngageboostProductCategories.objects.filter(category_id=item["category_id"],
																	  product_id__isdeleted='n')
				if catprod.count() > 0:
					catprod = catprod.distinct("product_id").values_list("product_id", flat=True)
					product_id_list = list(catprod)
					# print(product_id_list)
					prostock = EngageboostProductStocks.objects.filter(warehouse_id=item["warehouse_id"],
																	   product_id__in=product_id_list,
																	   real_stock__gt=0).count()
					if prostock > 0:
						all_data.append({"category": item["category_id__name"], "warehouse": item["warehouse_id__name"],
										 "count": prostock})
				else:
					prostock = 0

			else:
				prostock = 1
			EngageboostCategoryWarehouse.objects.filter(id=item["id"]).update(product_count=prostock)

		from webservices.views.emailcomponent import emailcomponent

		buffer_data = common.getAutoResponder("", "", "", "", "", "", 33)
		if buffer_data and buffer_data["content"]:
			autoResponderData = buffer_data["content"]
			if autoResponderData["email_type"] == 'H':
				emailContent = autoResponderData["email_content"]
			else:
				emailContent = autoResponderData["email_content_text"]

			if email_send == 1:

				to_emails = autoResponderData["bcc"]
				to_emails = to_emails.replace(' ', '')
				to_emails = to_emails.split(',')
				to_emails.append('anjan.saha@navsoft.in', 'mousumi.dhibar@navsoft.in')
				# to_emails = ["anjan.saha@navsoft.in", "mohammadabouchama@lifcoshop.net", "apurba@navsoft.in"]
			else:
				# to_emails = ["anjan.saha@navsoft.in"]
				to_emails = ["anjan.saha@navsoft.in", "mousumi.dhibar@navsoft.in"]
				to_emails.append('binayak.santra@navsoft.in')

			# subject = "Warehouse category cron completed"
			subject = autoResponderData['subject']

			table_content = '<table class="action" border="1" align="center" width="100%" cellpadding="0" cellspacing="0">\
								<tr>\
									<th align="center" width="45%">\
										Store\
									</th>\
									<th align="center" width="45%">\
										Category\
									</th>\
									<th align="center" width="10%">\
										Products\
									</th>\
								</tr>'


			today = datetime.datetime.today()
			today = today.strftime("%Y-%m-%d")

			file_name = "BMS_products_stock_" + str(today) + ".csv"

			# export_file_path = settings.MEDIA_ROOT + '/exportfile/' + file_name
			# download_path = settings.MEDIA_URL + 'exportfile/' + file_name




			if len(all_data) > 0:


				with open(file_name, 'w', newline='') as file:
					# print('in here')
					fieldnames = ['Warehouse', 'Category', 'Products']
					writer = csv.DictWriter(file, fieldnames=fieldnames)
					writer.writeheader()

					for newitem in all_data:
						table_content = table_content + '<tr>\
							<td align="center" width="45%">\
								' + str(newitem["warehouse"]) + '\
							</td>\
							<td align="center" width="45%">\
								' + str(newitem["category"]) + '\
							</td>\
							<td align="center" width="10%">\
								' + str(newitem["count"]) + '\
							</td>\
						</tr>'

						# writer.writeheader()
						writer.writerow(
							{'Warehouse': newitem["warehouse"], 'Category': newitem["category"], 'Products': newitem["count"]})


			else:
				table_content = table_content + '<tr>\
					<td align="center" width="100%" colspan="2">\
						No Order today\
					</td>\
				</tr>'
			table_content = table_content + '</table>'

			html_content = "Warehouse category cron completed \n" + table_content



			for to_email in to_emails:
				# print('to_email====>', to_email)
				response = emailcomponent.SendAllMail(to_email, subject, emailContent, file_name)
	print("end==")
	return 1



def UpdateDiscountCron():
	print("=======cron for update discount cron start=========")
	now_utc = datetime.datetime.now(datetime.timezone.utc)
	print('now_utc==', now_utc)
	cutoff_date_time = now_utc
	# cutoff_date_time = now_utc- timedelta(hours=2)
	# cutoff_date = cutoff_date_time.strftime('%Y-%m-%d')
	# cutoff_time = cutoff_date_time.strftime('%H:%M:%S')
	search_date_time = cutoff_date_time.strftime('%Y-%m-%d %H:%M')
	# companyObj = EngageboostCompanies.objects.filter(isdeleted='n', isblocked='n').distinct('database_name')
	# if companyObj.count() > 0:
	# 	companies = companyObj.all().iterator()
		# for company in companies:
		# 	# print("===================================================================================CS Start")
		# 	company_id = company.id
		# 	company_db = company.database_name
		# 	print('Database Name', company_db)
		# 	connections.databases[company_db] = {
		# 		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		# 		'NAME': company_db,
		# 		'USER': 'postgres',
		# 		'PASSWORD': 'postgre1234#',
		# 		'HOST': '50.16.162.98',
		# 		'PORT': '5432',
		# 	}
		# 	conn = connections[company_db]

	new_product_in_arr = []
	new_product_out_arr = []
	# rs_discount_master = EngageboostDiscountMasters.objects.filter(modified__date=cutoff_date, modified__time__gte=cutoff_time,discount_master_type=0, isdeleted='n', isblocked='n' ).all()
	# modified__gte=search_date_time,
	rs_discount_master = EngageboostDiscountMasters.objects.filter(disc_end_date__lt=search_date_time,
																   discount_master_type=0, isdeleted='n',
																   isblocked='n').all()
	# print('rs_discount_master======', rs_discount_master.query)
	# print('rs_discount_master======', rs_discount_master)
	if rs_discount_master:
		for dis_master_data in rs_discount_master:
			EngageboostDiscountMasters.objects.filter(id=dis_master_data.id).update(isblocked='y')

			new_conditions = EngageboostDiscountMastersConditions.objects.filter(
				discount_master_id=dis_master_data.id).all()
			new_conditions_serializar = DiscountConditionsSerializer(new_conditions, many=True)
			new_conditions_serializar = new_conditions_serializar.data
			for ind_pre_cond in new_conditions_serializar:
				if ind_pre_cond["all_product_id"]:
					product_id_array = ind_pre_cond["all_product_id"].split(",")
					if ind_pre_cond["condition"] == "==":
						new_product_in_arr = new_product_in_arr + product_id_array
					else:
						new_product_out_arr = new_product_out_arr + product_id_array
				elif ind_pre_cond["all_category_id"]:
					category_id_array = ind_pre_cond["all_category_id"].split(",")
					find_category_products = EngageboostProductCategories.objects.filter(
						category_id__in=category_id_array, category_id__isdeleted='n',
						product_id__isdeleted='n').values_list('product_id', flat=True).distinct()
					find_category_products = list(find_category_products)
					if ind_pre_cond["condition"] == "==":
						new_product_in_arr = new_product_in_arr + find_category_products
					else:
						new_product_out_arr = new_product_out_arr + find_category_products
	# hot_product_lst = GetHotOffersProducts()
	if new_product_in_arr:
		new_product_in_arr = set(new_product_in_arr)
		for elastic_product_id in new_product_in_arr:
			if (elastic_product_id != "" and elastic_product_id is not None):
				# if(elastic_product_id != "" and elastic_product_id is not None and elastic_product_id not in hot_product_lst):
				print('Hello', elastic_product_id)
				try:
					if ("," in elastic_product_id):
						prod_lst = elastic_product_id.split(",")
						elastic = common.update_bulk_elastic('EngageboostProducts', prod_lst,
															 'channel_currency_product_price', 'update')
						elastic = common.update_bulk_elastic('EngageboostProducts', prod_lst,
															 'free_installation', 'update')

					else:
						elastic = common.update_bulk_elastic('EngageboostProducts', [int(elastic_product_id)],
															 'channel_currency_product_price', 'update')
						elastic = common.update_bulk_elastic('EngageboostProducts', [int(elastic_product_id)],
															 'free_installation', 'update')
				except:
					elastic = common.update_bulk_elastic('EngageboostProducts', [int(elastic_product_id)],
														 'channel_currency_product_price', 'update')
					elastic = common.update_bulk_elastic('EngageboostProducts', [int(elastic_product_id)],
														 'free_installation', 'update')

	# conn.close()

	from webservices.views.emailcomponent import emailcomponent

	to_email = "binayak.santra@navsoft.in"
	subject = "Discount cron hit LIVE"
	html_content = "Discount cron hit successfully"
	response = emailcomponent.SendAllMail(to_email, subject, html_content)
	response = emailcomponent.SendAllMail('lifco.onboard@gmail.com', subject, html_content)
	print("=======cron for update discount cron end=========")
		# rs_price_master = EngageboostChannelCurrencyProductPrice.objects.filter(end_date__lt=search_date_time,product_price_type_id__price_type_id=2, product_id__isdeleted='n')
		# if rs_price_master.count()>0:
		# 	product_ids = rs_price_master.values_list('product_id',flat=True)

def check_and_update_expired_discounts():
	print('=============in  check_and_update_expired_discounts  =============')
	# response = emailcomponent.testmail('binayak.santra@navsoft.in',
	# 								   "Data Preparation Start @@@check_and_update_expired_discounts@@@TEST",
	# 								   'Data preparation Initiated ' + str(
	# 									   datetime.datetime.now()))
	website_id =1
	es = common.connect_elastic()
	query = {
    "query": {
      "bool": {
        "must": [
          {
            "match": {
              "isdeleted": "n"
            }
          },
          {
            "match": {
              "isblocked": "n"
            }
          }
        ],
        "filter": [
          {
            "nested": {
              "path": "channel_currency_product_price",
              "query": {
                "bool": {
                  "must": [
                    {
                      "range": {
                        "channel_currency_product_price.discount_amount": {
                          "gt": 0
                        }
                      }
                    }
                  ]
                }
              }
            }
          }
        ]
      }
    }
  }


	module_name = 'lifco1_product_1'
	prod_count = es.search(body=json.dumps(query), index=module_name, doc_type="", _source=False)
	# print("======prod_count======", prod_count)


	total_count = prod_count['hits']['total']
	print("======total_count======", total_count)

	for i in range(0, 100):
		print(i)
		start = i * 1000
		size = 1000

		if start < total_count:
			print("====range====="+str(start)+"======="+str(size))
			docs = []

			prod_exists = es.search(body=json.dumps(query), index=module_name, doc_type="",
									_source_include=['channel_currency_product_price'], from_=start, size=size)
			# print()
			for item in prod_exists['hits']['hits']:
				cm_id = item['_id']
				print("====cm_id======", cm_id)
				# if item['found'] == True:
				TempProductPriceObj = EngageboostTempProductPrice.objects.filter(website_id=1,
																				 product_id=cm_id).filter(
					err_flag=0, error_text=None)

				warehouse_id = None
				flag = 0


				price_data = item['_source']['channel_currency_product_price']
				# print("=====price_Data=====", price_data)
				# ========process elastic price========#
				for channel_currency_product_price in price_data:
					# print("======channel_currency_product_price======warehouse_id======",
					# 	  channel_currency_product_price['warehouse_id'])
					if int(channel_currency_product_price['discount_amount']) > 0:
						warehouse_id = channel_currency_product_price['warehouse_id']
						# print('======warehouse_type=======', type(warehouse_id))
						price_data_single = common.get_channel_currency_product_price(cm_id, website_id, [warehouse_id])

						for data in price_data_single:
							channel_currency_product_price['id'] = data['id']
							channel_currency_product_price['promotions'] = data['promotions']
							channel_currency_product_price['price_type'] = data['price_type']
							channel_currency_product_price['channel_id'] = data['channel_id']
							channel_currency_product_price['currency_id'] = data['currency_id']
							channel_currency_product_price['price'] = data['price']
							channel_currency_product_price['cost'] = data['cost']
							channel_currency_product_price['mrp'] = data['mrp']
							channel_currency_product_price['min_quantity'] = data['min_quantity']
							channel_currency_product_price['max_quantity'] = data['max_quantity']
							channel_currency_product_price['warehouse_id'] = data['warehouse_id']
							channel_currency_product_price['website_id'] = data['website_id']
							channel_currency_product_price['start_date'] = data['start_date']
							channel_currency_product_price['end_date'] = data['end_date']
							channel_currency_product_price['product'] = data['product']
							channel_currency_product_price['product_price_type'] = data['product_price_type']
							channel_currency_product_price['new_default_price'] = data['new_default_price']
							channel_currency_product_price['new_default_price_unit'] = data[
								'new_default_price_unit']
							channel_currency_product_price['discount_price_unit'] = data['discount_price_unit']
							channel_currency_product_price['discount_price'] = data['discount_price']
							channel_currency_product_price['discount_amount'] = data['discount_amount']
							channel_currency_product_price['disc_type'] = data['disc_type']
							channel_currency_product_price['coupon'] = data['coupon']

						flag = 1

				if flag == 0:
					# print("I am here")
					price_data_single = common.get_channel_currency_product_price(cm_id, website_id, [warehouse_id])
					# price_data_single = json.dumps(price_data_single)
					# price_data_single = json.loads(price_data_single)
					# print("======price_data_single======", price_data_single[0])
					# price_data = common.get_channel_currency_product_price(cm_id)
					price_data.append(price_data_single[0])
				# else:
				# 	price_data = item['_source']['channel_currency_product_price']

				# print("======price_data=======", price_data)
				# price_data = common.get_channel_currency_product_price(cm_id)
				data = {"channel_currency_product_price": price_data}

				# data = get_product_field_value_for_elastic(cm_id, field_name)

				header = {
					"_op_type": 'update',
					"_index": module_name,
					"_type": "data",
					"_id": cm_id,
					"doc": data
				}
				# print("======add header=======", header)
				docs.append(header)

			obj = helpers.bulk(es, docs)
	print('=======in finally save_price_from_temp_to_table ========')

	# EngageboostTempProductPrice.objects.filter(id__in=tempDataId).update(error_text="SUCCESS")
	# datas.append({"obj": obj})
	response = emailcomponent.testmail('binayak.santra@navsoft.in',
									   "check_and_update_expired_discountsLive@@@",
									   'Data preparation Completed and Pushed to Elastic @ ' + str(datetime.datetime.now()))
	response = emailcomponent.testmail('lifco.onboard@gmail.com',
									   "check_and_update_expired_discountsLive@@@",
									   'Data preparation Completed and Pushed to Elastic @ ' + str(datetime.datetime.now()))
	return

# check_and_update_expired_discounts()


def duplicate_product_categories():
    from webservices.views.emailcomponent import emailcomponent
    # all_categories = EngageboostCategoryMasters.objects.values_list('id')
    category_products = EngageboostProductCategories.objects.values('product_id').order_by('product_id').annotate(category_count=Count('product_id')).filter(category_count__gt=1)

    matching_ids = []
    for cat in category_products:
        # print("====cat===", cat)
        category_list = EngageboostProductCategories.objects.values('id', 'product_id', 'category_id').filter(product_id=cat['product_id'])

        category_list_ids = category_list.values_list('category_id', flat=True)
        # print("=====category_list_ids======", category_list_ids)
        category_list_ids = set(list(category_list_ids))
        # print("=====category_list_ids======", category_list_ids)
        category_id = None


        for cat_id in category_list_ids:
            # category_check = EngageboostProductCategories.objects.values('id', 'product_id', 'category_id').filter(
            #     product_id=cat['product_id'], category_id=cat_id)
            category_check = category_list.values('id', 'product_id', 'category_id').filter(category_id=cat_id)

            if category_check.count()>1:
                ids = list(category_check.values_list('id', flat=True))

                EngageboostProductCategories.objects.filter(id__in=ids[1:]).delete()

                print("ids==@@@@====", ids)
                print("delete_ids==@@@@====", ids[1:])
                matching_ids.extend(ids)

        # for category_list_detail in category_list:
        #
        #     print("======category_list_detail=======", category_list_detail)


    print("=====count=====", category_products.count())
    product_list = list(category_products.values_list('product_id', flat=True))
    # print("=====values_list======", product_list)
    response = emailcomponent.testmail('binayak.santra@navsoft.in',
                                       "duplicate product categories",
                                       'duplicate product categories ' + str(product_list) + "ids========> " + str(matching_ids))

    print("======product_list======", product_list)


def remove_secondary_category_for_specific_primary_category(cat_name):
	category = EngageboostCategoryMasters.objects.filter(name=cat_name).first()
	category_list = []
	if category:
		category_list.append(category.id)
		child_category = EngageboostCategoryMasters.objects.filter(parent_id=category.id).values_list('id', flat=True)
		category_list.extend(list(child_category))
		# print("=====category_list=====", category_list)
		category_products = list(EngageboostProductCategories.objects.values_list('product_id', flat=True).order_by('product_id').distinct('product_id').filter(category_id__in=category_list, is_parent='y'))
		# print("====category_products====", len(category_products))
		# print("====category_products====", category_products)
		for prod in category_products:

			print("====prod id=====", prod)
			stay_id = EngageboostProductCategories.objects.filter(product_id=prod, is_parent='y').first()
			delete_id = EngageboostProductCategories.objects.exclude(id=stay_id.id).filter(product_id=prod).values_list('id', flat=True)
			# print("====delete_id=====", delete_id)
			# return
			EngageboostProductCategories.objects.filter(id__in=delete_id).delete()

		print("=======done========")


def remove_secondary_category_for_all_primary_category():
	parent_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', parent_id=0).values_list('name', flat=True)
	for cat_name in parent_category:
		print("=====cat_name======", cat_name)
		remove_secondary_category_for_specific_primary_category(cat_name)

# remove_secondary_category_for_all_primary_category()
# remove_secondary_category_for_specific_primary_category('Cans - Jars & Others')
# duplicate_product_categories()

def ProductsToElasticCron():
    get_temp_product_skus = list(EngageboostTempProducts.objects.values_list('sku', flat=True))
    if len(get_temp_product_skus)>0:
        get_product_ids = EngageboostProducts.objects.filter(sku__in=get_temp_product_skus).values_list('id', flat=True)
        if get_product_ids:
            common.products_to_elastic_cron(list(get_product_ids))
        else:
            return
    else:
        return

# def ProductsToElasticCronResync():
# 	product_ids = [1, 3]
# 	common.products_to_elastic(list(product_ids))


def ProcessCronQueue():
	response = emailcomponent.testmail('binayak.santra@navsoft.in',
									   "Data preparation started @@@ProcessCronQueue---Test@@@",
									   'Data preparation start for ProcessCronQueue =====>' + ' @ ' + str(
										   datetime.datetime.now()))
	inactive_processes = EngageboostProcessQueueMaster.objects.filter(is_running='n').values_list('process_type', flat=True)

	ProcessProductStockCron(list(inactive_processes))


def ProcessProductStockCron(inactive_processes_type_list):

	pending_process_list = []
	products_ids = []
	product_price_update_list = 0
	discount_update_list = 0
	#--------Stock update for single case START--------#
	if 'inventory' in inactive_processes_type_list:
		product_list = EngageboostUpdateQueue.objects.filter(operation_for='inventory',
															 process_type='single',
															 process_state='Pending').values_list('product_id', flat=True)
		products_ids = list(set(product_list))

		if len(products_ids) > 0:
			pending_process_list.append('inventory')

	# --------Stock update for single case END--------#
	###########################################################################

	# --------Price update for single case START--------#
	if 'price' in inactive_processes_type_list:
		product_price_update_list = EngageboostUpdateQueue.objects.filter(operation_for='price',
																		 process_type='single',
																		 process_state='Pending').count()

		if product_price_update_list > 0:
			pending_process_list.append('price')
	# --------Price update for single case END--------#

	# ---------Discount update queue---------#
	if 'discount' in inactive_processes_type_list:
		discount_update_list = EngageboostUpdateQueue.objects.filter(operation_for='discount',
																	 process_type='single',
																	 process_state='Pending').count()
		if discount_update_list > 0:
			pending_process_list.append('discount')
	# ---------Discount update queue---------#


	# -----If Pending stock update found-----#
	if len(products_ids) > 0:
		stock_update_single_queue_process(products_ids)

	#----If pending price update found------#
	if product_price_update_list>0:
		price_update_single_queue_process()

	# ----If Pending discount found------#
	if discount_update_list > 0:
		discount_update_queue_process()


def stock_update_single_queue_process(products_ids):
	docs = []
	datas = []
	tempDataId = []
	es = common.connect_elastic()

	table_name = 'EngageboostProducts'

	EngageboostUpdateQueue.objects.filter(product_id__in=products_ids, process_state='Pending', operation_for='inventory').update(
		process_state="Processing")
	EngageboostProcessQueueMaster.objects.filter(process_type='inventory').update(is_running='y')

	module_name = ""
	if len(products_ids)>0:
		module_name = common.get_index_name_elastic(products_ids[0], table_name)
	# response = emailcomponent.testmail('binayak.santra@navsoft.in',
	# 								   "Data Preparation Initiated @@@product_stock_cron_test123@@@",
	# 								   'Data preparation Initiated ' + str(
	# 									   datetime.datetime.now()))

	try:
		for product_id in products_ids:
			product_stock = common.get_product_stock(product_id)
			# print("===================",product_stock)
			# elastic = common.change_field_value_elastic(product_id, 'EngageboostProducts',
			# 											{'inventory': product_stock})

			data = {'inventory': product_stock}

			header = {
				"_op_type": 'update',
				"_index": module_name,
				"_type": "data",
				"_id": product_id,
				"doc": data
			}

			docs.append(header)
			tempDataId.append(product_id)

		# data = {'status': 1, 'api_status': serializer.data['id'], 'message': 'Stock Inserted'}
		# else:
		# 	data = {'status': 0, 'api_status': 0, 'message': 'No product to update'}
		# 	datas.append(data)

	except Exception as error:
		trace_back = sys.exc_info()[2]
		line = trace_back.tb_lineno
		datas.append(
			{"status": 0, "api_status": trace_back.format_exc(), "error_line": line, "error_message": str(error),
			 "message": str(error)})
	# EngageboostTempProductPrice.objects.filter(id=serializer_data['id']).update(error_text=str(error), err_flag=1)

	finally:
		print('=======in finally========')
		# print("=======docs========", docs)
		obj = helpers.bulk(es, docs)
		print("========tempDataId========", tempDataId)
		EngageboostUpdateQueue.objects.filter(product_id__in=tempDataId, process_state='Processing', operation_for='inventory').update(
			process_state="Completed")
		EngageboostProcessQueueMaster.objects.filter(process_type='inventory').update(is_running='n')
		datas.append({"obj": obj})

		response = emailcomponent.testmail('binayak.santra@navsoft.in',
										   "Data Pushed to Elastic @@@stock_update_single_queue_process---Live@@@",
										   'Data preparation Completed and Pushed to Elastic, PRODUCT_COUNT =====>' + str(
											   len(tempDataId)) + ' @ ' + str(datetime.datetime.now()) + ' DATA=====> ' + str(datas))

def price_update_single_queue_process():
	docs = []
	datas = []
	tempDataId = []

	# es = common.connect_elastic()

	table_name = 'EngageboostProducts'

	EngageboostUpdateQueue.objects.filter(process_state='Pending',
										  process_type='single',
										  operation_for='price').update(
		process_state="Processing")
	EngageboostProcessQueueMaster.objects.filter(process_type='price').update(is_running='y')

	processing_price_queue = EngageboostUpdateQueue.objects.filter(process_type='single', process_state='Processing', operation_for='price')

	for product in processing_price_queue:

		# print("=======product=======", product.product_id)
		# print("=======product=======", product.warehouse_id)

		if product.warehouse_id !=None:
			success_id = common.update_bulk_elastic_now_process('EngageboostProducts', [int(product.product_id)],
											 'channel_currency_product_price', 'update', [int(product.warehouse_id)])
		else:
			success_id = common.update_bulk_elastic_now_process('EngageboostProducts', [int(product.product_id)],
											 'channel_currency_product_price', 'update')

		tempDataId.extend(success_id)


	EngageboostUpdateQueue.objects.filter(process_state='Processing',
										  process_type='single',
										  operation_for='price').update(
		process_state="Completed")
	EngageboostProcessQueueMaster.objects.filter(process_type='price').update(is_running='n')

	response = emailcomponent.testmail('binayak.santra@navsoft.in',
									   "Data Pushed to Elastic @@@price_update_single_queue_process---Live@@@",
									   'Data preparation Completed and Pushed to Elastic, PRODUCT_COUNT =====>' + str(
										   len(tempDataId)) + ' @ ' + str(
										   datetime.datetime.now()) + ' DATA=====> ' + str(datas))


def discount_update_queue_process():
	docs = []
	datas = []
	tempDataId = []

	# es = common.connect_elastic()

	table_name = 'EngageboostProducts'



	processing_discount_queue = EngageboostUpdateQueue.objects.filter(process_type='single', process_state='Pending',
																   operation_for='discount').values_list('discount_id', flat=True)

	processing_discount_queue = set(processing_discount_queue)
	print("==============processing_discount_queue================", processing_discount_queue)

	for discount_id in processing_discount_queue:
		prev_product_ids_list = []
		prev_warehouse_ids_list = []
		product_ids_list = []
		category_ids_list = []
		warehouse_ids = []

		discount_data = EngageboostUpdateQueue.objects.filter(process_state='Pending',
															  process_type='single',
															  operation_for='discount',
															  discount_id=discount_id)

		# ---------Fetching the previous mapped product list---------#
		prev_discount_products = discount_data.values_list('prev_products', flat=True)
		prev_discount_warehouses = discount_data.values_list('prev_warehouses', flat=True)
		print("==============prev_discount_products=================", prev_discount_products)
		for prev_prod in prev_discount_products:
			if prev_prod != None:
				prev_product_ids_list.extend(list(map(int, prev_prod.split(","))))

		print("========prev_product_ids_list=========", prev_product_ids_list)

		for prev_ware in prev_discount_warehouses:
			if prev_ware != None:
				prev_warehouse_ids_list.extend(list(map(int, prev_ware.split(","))))

		# ---------Marking the discounts as processing---------#
		discount_data.update(process_state="Processing")

		EngageboostProcessQueueMaster.objects.filter(process_type='discount').update(is_running='y')


		discount_condition = EngageboostDiscountMastersConditions.objects.filter(discount_master_id=discount_id, isdeleted='n', isblocked='n')
		for condition in discount_condition:
			condition_warehouse = EngageboostDiscountMasters.objects.filter(id=discount_id, isdeleted='n', isblocked='n')

			if condition_warehouse.count()>0:
				print("in here", discount_id)
				warehouse_ids = condition_warehouse.first().warehouse_id
				warehouse_ids = list(map(int, warehouse_ids.split(",")))

				# print("=======product=======", condition.all_product_id)
				# print("=======category=======", condition.all_category_id)
				# print("=======@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=======")

				if condition.all_product_id != None:
					product_ids_list.extend(list(map(int,condition.all_product_id.split(","))))

				if condition.all_category_id != None:
					category_ids_list.extend(list(map(int, condition.all_category_id.split(","))))

					found_parent_cat_ids = EngageboostCategoryMasters.objects.filter(id__in=category_ids_list, parent_id=0, isdeleted='n', isblocked='n').values_list('id', flat=True)

					# print("======found_parent_cat_ids========", found_parent_cat_ids)
					# child_cats

					category_product_list = EngageboostProductCategories.objects.filter(category_id__in=category_ids_list, isdeleted='n', isblocked='n').values_list('product_id', flat=True)

					# print("======category_product_list========", category_product_list.count())

					product_ids_list.extend(list(category_product_list))


				# print("=======product=======", product_ids_list)
				# print("=======warehouse_ids=======", warehouse_ids)

		warehouse_ids.extend(prev_warehouse_ids_list)
		warehouse_ids = set(warehouse_ids)

		product_ids_list.extend(prev_product_ids_list)
		product_ids_list = set(product_ids_list)

		if warehouse_ids:
			success_id = common.update_bulk_elastic_now_process('EngageboostProducts', product_ids_list,
																'channel_currency_product_price', 'update',
																warehouse_ids)
		else:
			success_id = common.update_bulk_elastic_now_process('EngageboostProducts', product_ids_list,
																'channel_currency_product_price', 'update')

			# tempDataId.extend(success_id)
		#
		EngageboostUpdateQueue.objects.filter(process_state='Processing',
											  process_type='single',
											  operation_for='discount',
											  discount_id=discount_id).update(
			process_state="Completed")
		EngageboostProcessQueueMaster.objects.filter(process_type='discount').update(is_running='n')

		response = emailcomponent.testmail('binayak.santra@navsoft.in',
										   "Data Pushed to Elastic @@@discount_update_queue_process---Live@@@",
										   'Data preparation Completed and Pushed to Elastic, PRODUCT_COUNT =====>' + str(
											   len(product_ids_list)) + ' for DISCOUNT ' + str(discount_id) + ' @ ' + str(
											   datetime.datetime.now()) + ' DATA=====> ' + str(datas))