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
from django.db.models import Q 
from django.core.files.storage import FileSystemStorage
from webservices.views import loginview
from django.utils.crypto import get_random_string

import datetime
import json
import random
import os
import ast
import xlsxwriter
import xlrd
import sys
import traceback
from webservices.views.common import common

# class DiscountSet is used to insert Discount
class DiscountSet(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		has_multy = request.data['value']
		name = has_multy['name']
		# namelower = name.lower()
		# name1 = namelower.replace(" ", "-")
		# nametrns = name1.translate(
		# {ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~=+\"\'"})
		# slugname = slugify(nametrns)
		# cnt = EngageboostDiscountMasters.objects.filter(name=name).count()
		# if cnt == 0:
		# 	cnt = cnt
		# 	slugname = slugname
		# elif cnt == 1:
		# 	cnt = cnt
		# 	slugname = slugname + '1'
		# else:
		# 	slugname = slugname + str(cnt)
		# slugname = common.create_discount_slug(name)

		if 'DiscountMastersConditions' in has_multy.keys():
			has_multy.pop('DiscountMastersConditions')
		if 'DiscountMastersCoupons' in has_multy.keys():
			has_multy.pop('DiscountMastersCoupons')

		discount_master_type = has_multy['discount_master_type']
		product_id_qty = ""
		if 'product_id_qty' in has_multy.keys():
			product_id_qty = has_multy['product_id_qty']

		is_mul = has_multy['has_multiplecoupons']
		d1 = {'created': datetime.datetime.now(), 'modified': datetime.datetime.now(), 'used_coupon': 0}
		serializer_data = dict(has_multy, **d1)
		if is_mul == 'n':
			if discount_master_type != 0:
				coupon_code = has_multy['coupon_code']

				if has_multy['coupon_prefix'] is None:
					has_multy['coupon_prefix'] = ""
				if has_multy['coupon_suffix'] is None:
					has_multy['coupon_suffix'] = ""
				if has_multy['coupon_prefix'] is not None and has_multy['coupon_prefix'] != "":
					has_multy['coupon_code'] = str(has_multy['coupon_code']).strip(str(has_multy['coupon_prefix']))
					coupon_code = str(has_multy['coupon_prefix']).strip() + str(coupon_code).strip()
				if has_multy['coupon_suffix'] is not None and has_multy['coupon_suffix'] != "":
					has_multy['coupon_code'] = str(has_multy['coupon_code']).strip() + str(
						has_multy['coupon_suffix']).strip()
					coupon_code = str(coupon_code).strip() + str(has_multy['coupon_suffix']).strip()
				serializer_data['coupon_code'] = coupon_code
				cnt = EngageboostDiscountMasters.objects.filter(coupon_code=coupon_code).count()
				if cnt == 0:
					if 'id' in has_multy.keys():
						discount_id = has_multy['id']
						creditObj = EngageboostDiscountMasters.objects.get(id=discount_id)
						serializer_data.pop("id")
						serializer = DiscountMasterSerializer(creditObj, data=serializer_data, partial=True)
					else:
						serializer = DiscountMasterSerializer(data=serializer_data, partial=True)
					if serializer.is_valid():
						serializer.save()

						obj = EngageboostDiscountMasters.objects.latest('id')
						last_id = obj.id

						if product_id_qty:
							product_id_qtys = product_id_qty.split(",")
							if len(product_id_qtys) > 0:
								EngageboostDiscountFreebieMappings.objects.filter(discount_master_id=last_id).delete()
								for item in product_id_qtys:
									pro_qty = item.split("@")
									current_date = datetime.datetime.now(datetime.timezone.utc).astimezone()
									EngageboostDiscountFreebieMappings.objects.create(discount_master_id=last_id,
																					  product_id=pro_qty[0],
																					  qty=pro_qty[1],
																					  created=current_date,
																					  modified=current_date)

						data = {
							'status': 1,
							'api_status': {"id": last_id},
							'message': 'Successfully Inserted',
						}
						return Response(data)
					else:
						data = {
							'status': 0,
							'api_status': serializer.errors,
							'message': 'Data Not Found',
						}
						return Response(data)
				else:
					data = {
						'status': 0,

						'message': 'Coupon code already exists',
					}
					return Response(data)
			else:
				if 'id' in has_multy.keys():
					discount_id = has_multy['id']
					creditObj = EngageboostDiscountMasters.objects.get(id=discount_id)
					serializer_data.pop("id")
					serializer = DiscountMasterSerializer(creditObj, data=serializer_data, partial=True)
				else:
					serializer = DiscountMasterSerializer(data=serializer_data, partial=True)

				if serializer.is_valid():
					serializer.save()
					obj = EngageboostDiscountMasters.objects.latest('id')
					last_id = obj.id

					if product_id_qty:
						product_id_qtys = product_id_qty.split(",")
						if len(product_id_qtys) > 0:
							EngageboostDiscountFreebieMappings.objects.filter(discount_master_id=last_id).delete()
							for item in product_id_qtys:
								pro_qty = item.split("@")
								current_date = datetime.datetime.now(datetime.timezone.utc).astimezone()
								EngageboostDiscountFreebieMappings.objects.create(discount_master_id=last_id,
																				  product_id=pro_qty[0], qty=pro_qty[1],
																				  created=current_date,
																				  modified=current_date)

					data = {
						'status': 1,
						'api_status': {"id": last_id},
						'message': 'Successfully Inserted',
					}
					return Response(data)
				else:
					data = {
						'status': 0,
						'api_status': serializer.errors,
						'message': 'Data Not Found',
					}
					return Response(data)

		else:
			d1 = request.data['value']
			d1 = {'created': datetime.datetime.now(), 'modified': datetime.datetime.now()}
			serializer_data = dict(has_multy, **d1)

			if 'id' in d1.keys():
				discount_id = d1['id']
				creditObj = EngageboostDiscountMasters.objects.get(id=discount_id)
				serializer_data.pop("id")
				serializer = DiscountMasterSerializer(creditObj, data=serializer_data, partial=True)
			else:
				serializer = DiscountMasterSerializer(data=serializer_data, partial=True)

			if serializer.is_valid():
				serializer.save()
				obj = EngageboostDiscountMasters.objects.latest('id')
				last_id = obj.id

				if product_id_qty:
					product_id_qtys = product_id_qty.split(",")
					if len(product_id_qtys) > 0:
						EngageboostDiscountFreebieMappings.objects.filter(discount_master_id=last_id).delete()
						for item in product_id_qtys:
							pro_qty = item.split("@")
							current_date = datetime.datetime.now(datetime.timezone.utc).astimezone()
							EngageboostDiscountFreebieMappings.objects.create(discount_master_id=last_id,
																			  product_id=pro_qty[0], qty=pro_qty[1],
																			  created=current_date,
																			  modified=datetime.datetime.now())

				if 'multiple_coupons' in has_multy.keys():
					if request.data['multiple_coupons']:
						list_of_multiple_coupons = request.data['multiple_coupons']
					else:
						list_of_multiple_coupons = None
				else:
					list_of_multiple_coupons = None

				if list_of_multiple_coupons:
					for coupon_code in list_of_multiple_coupons:
						cnt = EngageboostDiscountMastersCoupons.objects.filter(coupon_code=coupon_code).count()
						if cnt == 0:
							User = EngageboostDiscountMastersCoupons.objects.create(website_id=has_multy['website_id'],
																					discount_master_id=last_id,
																					coupon_code=coupon_code,
																					created=datetime.datetime.now())
							data = {
								'status': 1,
								'api_status': {"id": last_id},
								'message': 'Successfully Inserted',
							}
						else:
							data = {
								'status': 0,
								'message': 'Coupon code already exists',
							}
				else:
					no_of_coupon = has_multy["number_of_coupon"]
					flag = 0
					sresult = 1
					list_of_multiple_coupons = []
					prefix = suffix = ""
					if 'prefix' in has_multy.keys():
						prefix = has_multy['prefix']
					if 'suffix' in has_multy.keys():
						suffix = has_multy['suffix']

					while sresult != -1 and flag < no_of_coupon:
						res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

						res = str(prefix) + str(res).lower() + str(suffix)
						result = EngageboostDiscountMastersCoupons.objects.filter(isdeleted='n',
																				  coupon_code=res).count()
						if result > 0:
							pass
						else:
							list_of_multiple_coupons.append(res)
							sresult = int(flag)
							flag += 1

					for coupon_code in list_of_multiple_coupons:
						User = EngageboostDiscountMastersCoupons.objects.create(website_id=has_multy['website_id'],
																				discount_master_id=last_id,
																				coupon_code=coupon_code,
																				created=datetime.datetime.now())
						data = {
							'status': 1,
							'api_status': {"id": last_id},
							'message': 'Successfully Inserted',
						}
				return Response(data)

			else:
				data = {
					'status': 0,
					'api_status': serializer.errors,
					'message': 'Data Not Found',
				}
				return Response(data)
# class DiscountList is used to fetch list of all  Discount
class DiscountList(generics.ListAPIView):
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostDiscountMasters.objects.using(company_db).get(pk=pk)
		except EngageboostDiscountMasters.DoesNotExist:
			raise Http404
	 #///////////////////Fetch Single Row
	
	def get(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		coupon_code=[]
		dis = self.get_object(pk,request)
		serializer = DiscountMasterSerializer(dis)
		couponcode1=EngageboostDiscountMastersCoupons.objects.using(company_db).all().filter(discount_master_id=pk)
		customergrp = EngageboostCustomerGroup.objects.using(company_db).all().filter(isdeleted='n',
																					  isblocked='n').order_by('name')
		customer = CustomerGroupSerializer(customergrp, many=True)
		for coupon in couponcode1:
			coupon_array={'coupon_code':coupon.coupon_code,'is_used':coupon.is_used}
			coupon_code.append(coupon_array)
		if(serializer): 
			data ={
				'status':1,
				'api_status':serializer.data,
				'multiple_coupons':coupon_code,
				'customer_group':customer.data,
				'message':'',
				}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
		return Response(data)
	# Update Discount
	def put(self, request, pk, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		dis = self.get_object(pk,request)
		coupon_code = request.data['value']['coupon_code']

		#------Binayak Start 11-03-2021-----#
		warehouse = request.data['value']['warehouse']
		# print("======warehouse======", warehouse)
		# ------Binayak End 11-03-2021-----#

		has_multy = request.data['value']
		if 'DiscountMastersConditions' in has_multy.keys():
			has_multy.pop('DiscountMastersConditions')
		if 'DiscountMastersCoupons' in has_multy.keys():
			has_multy.pop('DiscountMastersCoupons')

		is_mul = has_multy['has_multiplecoupons']
		discount_master_type = has_multy['discount_master_type']
		# print('Chakradhar Working', is_mul, discount_master_type)
		product_id_qty = ""
		if 'product_id_qty' in has_multy.keys():
			product_id_qty = has_multy['product_id_qty']
		
		d1={'modified':datetime.datetime.now()}
		serializer_data=dict(has_multy,**d1)
		if is_mul == 'n':
			if discount_master_type != 0:
				cnt=EngageboostDiscountMasters.objects.using(company_db).filter(coupon_code=coupon_code).filter(~Q(id=pk)).count()
				if cnt ==0:
					serializer = DiscountMasterSerializer(dis,data=serializer_data,partial=True)
					if serializer.is_valid():
						latest = serializer.save()
						if product_id_qty:
							product_id_qtys = product_id_qty.split(",")
							if len(product_id_qtys)>0:
								EngageboostDiscountFreebieMappings.objects.filter(discount_master_id=latest.id).delete()
								for item in product_id_qtys:
									pro_qty = item.split("@")
									current_date = datetime.datetime.now(datetime.timezone.utc).astimezone()
									EngageboostDiscountFreebieMappings.objects.create(discount_master_id=latest.id,product_id=pro_qty[0],qty=pro_qty[1],created=current_date,modified=current_date)
						data = {
							'status':1,
							'api_status':'',
							'message':'Successfully Updated',
						}
						return Response(data)
					else:
						data ={
							'status':0,
							'api_status':serializer.errors,
							'message':'Data Not Found',
						}
						return Response(data)
				else:
					data ={
						'status':0,
						'message':'Coupon code is already exists',
					}
					return Response(data)
			else:
				serializer = DiscountMasterSerializer(dis,data=serializer_data,partial=True)
				if serializer.is_valid():
					prev_products = list(EngageboostDiscountMastersConditions.objects.filter(discount_master_id = pk).values_list('all_product_id',flat=True))
					prev_warehouses = EngageboostDiscountMasters.objects.filter(id=pk).first().warehouse_id
					latest = serializer.save()
					if product_id_qty:
						product_id_qtys = product_id_qty.split(",")
						if len(product_id_qtys)>0:
							EngageboostDiscountFreebieMappings.objects.filter(discount_master_id=latest.id).delete()
							for item in product_id_qtys:
								pro_qty = item.split("@")
								current_date = datetime.datetime.now(datetime.timezone.utc).astimezone()
								EngageboostDiscountFreebieMappings.objects.create(discount_master_id=latest.id,product_id=pro_qty[0],qty=pro_qty[1],created=current_date,modified=current_date)
					data ={
					'status':1,
					'api_status':'',
					'message':'Successfully Updated',
					}
					objproduct_list = EngageboostDiscountMastersConditions.objects.filter(discount_master_id = pk).values_list('all_product_id',flat=True)
					if(prev_products):
						objproduct_list = list(objproduct_list)
						objproduct_list.extend(prev_products)
						objproduct_list = list(set(objproduct_list))

					# if objproduct_list :
					# 	for elastic_product_id in objproduct_list:
					# 		if(elastic_product_id is not None):
					# 			print('Hello', elastic_product_id)
					# 			if("," in elastic_product_id):
					# 				prod_lst = elastic_product_id.split(",")
					# 				elastic = common.update_bulk_elastic('EngageboostProducts',prod_lst)
					# 			else:
					# 				elastic = common.update_bulk_elastic('EngageboostProducts',[int(elastic_product_id)])				

					if objproduct_list:
						# print("=====objproduct_list=====", objproduct_list)
						#-------Binayak start 12-03-2021------#\
						prooduct_id_list = []
						for prod in objproduct_list:
							if prod:
								prod = prod.split(',')
								# prev_products = list(prev_products.split(","))
								# print("=====prev_products=====", prev_products)
								# print("=====prev_products=====", type(prev_products))
								prooduct_id_list.extend(prod)
						# print("=====prooduct_id_list=====", prooduct_id_list)
						prooduct_id_list = list(map(int, prooduct_id_list))
						# if prooduct_id_list:
						# 	elastic = common.update_bulk_elastic('EngageboostProducts', prooduct_id_list,
						# 										 'channel_currency_product_price', 'update', warehouse)
						#-------Binayak end 12-03-2021------#
						# for elastic_product_id in objproduct_list:
						# 	if(elastic_product_id is not None):
						# 		try:
						# 			if("," in elastic_product_id):
						# 				prod_lst = elastic_product_id.split(",")
						# 				elastic = common.update_bulk_elastic('EngageboostProducts',prod_lst,'channel_currency_product_price','update', warehouse)
						# 			else:
						# 				print("=====in here 5=====")
						# 				elastic = common.update_bulk_elastic('EngageboostProducts',[int(elastic_product_id)],'channel_currency_product_price','update', warehouse)
						# 		except:
						# 			print("=====in here 6=====")
						# 			elastic = common.update_bulk_elastic('EngageboostProducts',[int(elastic_product_id)],'channel_currency_product_price','update', warehouse)

					EngageboostUpdateQueue.objects.create(discount_id=pk,
														  process_type='single',
														  operation_for='discount',
														  prev_warehouses=prev_warehouses)

					return Response(data)
				else:
					data ={
					'status':0,
					'api_status':serializer.errors,
					'message':'Data Not Found',
					}
					return Response(data)
		else:
			d1= request.data['value']
			d2 =  request.data['multiple_coupons']
			d1={'modified':datetime.datetime.now()}
			serializer_data=dict(has_multy,**d1)
			serializer = DiscountMasterSerializer(dis,data=serializer_data,partial=True)
			if serializer.is_valid():
				latest = serializer.save()
				if product_id_qty:
					product_id_qtys = product_id_qty.split(",")
					if len(product_id_qtys)>0:
						EngageboostDiscountFreebieMappings.objects.filter(discount_master_id=latest.id).delete()
						for item in product_id_qtys:
							pro_qty = item.split("@")
							current_date = datetime.datetime.now(datetime.timezone.utc).astimezone()
							EngageboostDiscountFreebieMappings.objects.create(discount_master_id=latest.id,product_id=pro_qty[0],qty=pro_qty[1],created=current_date,modified=current_date)
				for is_mul in d2:
					cnt= EngageboostDiscountMastersCoupons.objects.using(company_db).filter(coupon_code=is_mul['coupon_code']).filter(~Q(discount_master_id=pk)).count()
					if cnt ==0:
						User = EngageboostDiscountMastersCoupons.objects.using(company_db).create(website_id=has_multy['website_id'],discount_master_id=pk,coupon_code=is_mul['coupon_code'],modified=datetime.datetime.now().date())
						data ={
							'status':1,
							'api_status':'',
							'message':'Successfully Updated',
						}
					else:
						data ={
							'status':0,
							'api_status':'',
							'message':'Coupon code is already exists',
						}
				return Response(data)
			else:
				data ={
					'status':0,
					'api_status':serializer.errors,
					'message':'Data Not Found',
				}
				return Response(data)
# Set discount conditions(Insert new records)
# Save discount data after save condition by cds on 11th Oct 2019
class DiscountConditions(generics.ListAPIView):
	def post(self, request, format=None):
		datas=[]
		company_db = loginview.db_active_connection(request)
		discount_master_id=request.data['discount_master_id']
		warehouse = EngageboostDiscountMasters.objects.filter(id=discount_master_id).values_list('warehouse_id',
																								 flat=True)
		prev_products = list(EngageboostDiscountMastersConditions.objects.using(company_db).filter(discount_master_id = discount_master_id).values_list('all_product_id',flat=True))

		prev_conditions = EngageboostDiscountMastersConditions.objects.using(company_db).filter(discount_master_id=discount_master_id).all()
		prev_pro_ids = []
		new_pro_ids = []
		# if cnt >0:
		if prev_conditions:
			prev_conditions_serializar = DiscountConditionsSerializer(prev_conditions, many=True)
			prev_conditions_serializar = prev_conditions_serializar.data
			product_in_arr = []
			product_out_arr = []
			for ind_pre_cond in prev_conditions_serializar:
				if ind_pre_cond["all_product_id"]:
					product_id_array = ind_pre_cond["all_product_id"].split(",")
					if ind_pre_cond["condition"] == "==":
						product_in_arr = product_in_arr + product_id_array
					else:
						product_out_arr = product_out_arr + product_id_array
				elif ind_pre_cond["all_category_id"]:
					category_id_array = ind_pre_cond["all_category_id"].split(",")
					find_category_products = EngageboostProductCategories.objects.filter(category_id__in=category_id_array).values_list('product_id', flat= True).distinct()
					find_category_products = list(find_category_products)
					if ind_pre_cond["condition"] == "==":
						product_in_arr = product_in_arr + find_category_products
					else:
						product_out_arr = product_out_arr + find_category_products

				prev_pro_ids = list(set(product_in_arr) - set(product_out_arr)) #product_in_arr-product_out_arr
			EngageboostDiscountMastersConditions.objects.using(company_db).filter(discount_master_id=discount_master_id).delete()
		has_multy=request.data['value']
		for data in has_multy:
			has_record = EngageboostDiscountMastersConditions.objects.using(company_db).last()
			if has_record:
				last_entry_of_table = EngageboostDiscountMastersConditions.objects.order_by('-id').latest('id')
				row_id = int(last_entry_of_table.id)+int(1)
			else:
				row_id = 1
			d1={"id":row_id};
			data=dict(data,**d1)
			# datas.append(data)
			# serializer = DiscountConditionsSerializer(data=data,partial=True)
			serializer = EngageboostDiscountMastersConditions.objects.using(company_db).create(**data)
			# objproduct_list = EngageboostDiscountMastersConditions.objects.using(company_db).filter(discount_master_id = discount_master_id).values_list('all_product_id',flat=True)

			# New
			new_conditions = EngageboostDiscountMastersConditions.objects.using(company_db).filter(discount_master_id=discount_master_id).all()
			new_conditions_serializar = DiscountConditionsSerializer(new_conditions, many=True)
			new_conditions_serializar = new_conditions_serializar.data
			new_product_in_arr = []
			new_product_out_arr = []
			for ind_pre_cond in new_conditions_serializar:
				if ind_pre_cond["all_product_id"]:
					product_id_array = ind_pre_cond["all_product_id"].split(",")
					if ind_pre_cond["condition"] == "==":
						new_product_in_arr = new_product_in_arr + product_id_array
					else:
						new_product_out_arr = new_product_out_arr + product_id_array
				elif ind_pre_cond["all_category_id"]:
					category_id_array = ind_pre_cond["all_category_id"].split(",")
					find_category_products = EngageboostProductCategories.objects.filter(category_id__in=category_id_array).values_list('product_id', flat= True).distinct()
					find_category_products = list(find_category_products)
					if ind_pre_cond["condition"] == "==":
						new_product_in_arr = new_product_in_arr + find_category_products
					else:
						new_product_out_arr = new_product_out_arr + find_category_products
					
				new_pro_ids = list(set(new_product_in_arr) - set(new_product_out_arr)) #product_in_arr-product_out_arr

			# End New
			diff_ids = prev_pro_ids + new_pro_ids
			final_arr = list(set(diff_ids))
					
			objproduct_list = prev_pro_ids   #  It is static. Checking for testing purpose
			# if final_arr :
			# 	for elastic_product_id in final_arr:
			# 		if(elastic_product_id != "" and elastic_product_id is not None):
			# 			elastic_product_id = str(elastic_product_id)
			# 			if (elastic_product_id.find(',') != -1): 
			# 				prod_lst = elastic_product_id.split(",")
			# 				for prod_id in prod_lst:
			# 					if(prod_id!=""):
			# 						elastic = common.save_data_to_elastic(int(prod_id),'EngageboostProducts')
			# 			else:
			# 				elastic = common.save_data_to_elastic(int(elastic_product_id),'EngageboostProducts')
			
			if final_arr:
				# for elastic_product_id in final_arr:
				# 	if(elastic_product_id != "" and elastic_product_id is not None):
				# 		print('Hello', elastic_product_id)
				# 		try:
				# 			if("," in elastic_product_id):
				# 				prod_lst = elastic_product_id.split(",")
				# 				elastic = common.update_bulk_elastic('EngageboostProducts',prod_lst,'channel_currency_product_price','update')
				# 			else:
				# 				elastic = common.update_bulk_elastic('EngageboostProducts',[int(elastic_product_id)],'channel_currency_product_price','update')
				# 		except:
				# 			elastic = common.update_bulk_elastic('EngageboostProducts',[int(elastic_product_id)],'channel_currency_product_price','update')
				prooduct_id_list = []
				# print("======final_arr=======", final_arr)
				for prev_prov in final_arr:
					if type(prev_prov) == 'str':
						prev_prov = prev_prov.split(',')
						prooduct_id_list.extend(prev_prov)
					else:
						prooduct_id_list.append(prev_prov)

				prooduct_id_list = list(map(int, prooduct_id_list))

				warehouse_lists = []
				if prooduct_id_list:
					for warehouse_ids in warehouse:
						# print('======warehouse======', warehouse_ids)
						warehouse_lists.extend(list(map(int, list(warehouse_ids.split(',')))))
					# warehouse = list(map(int, list(warehouse)))

					prev_pro_ids = list(map(str, prev_pro_ids))

					EngageboostUpdateQueue.objects.create(discount_id=discount_master_id,
														  process_type='single',
														  operation_for='discount',
														  prev_products=", ".join(prev_pro_ids))
					#
					# elastic = common.update_bulk_elastic('EngageboostProducts', prooduct_id_list,
					# 									 'channel_currency_product_price',
					# 									 'update', warehouse_lists)

			if serializer:
				# serializer.save()
				data ={
					'status':1,
					'api_status':'',
					'message':'Successfully Inserted',
				}
			else:
				data ={
					'status':0,
					'api_status':serializer.errors,
					'message':'Data Not Found',
				}
		return Response(data)
		# return Response(datas)



# Set discount conditions Get single row and update
class DiscountConditionsSet(generics.ListAPIView):
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostDiscountMastersConditions.objects.using(company_db).get(pk=pk)
		except EngageboostDiscountMastersConditions.DoesNotExist:
			raise Http404
	
	def get(self, request, pk, format=None,many=True):
		company_db = loginview.db_active_connection(request)
		Conditions = EngageboostDiscountMastersConditions.objects.using(company_db).all().filter(discount_master_id=pk)
		serializer = DiscountConditionsSerializer(Conditions,many=True)
		# data1 = EngageboostCustomers.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		# serializer1 = CustomerSerializer(data1, many=True)
		# Channels = EngageboostChannels.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		# Channel = ChannelsSerializer(Channels, many=True)
		# Categories = EngageboostCategoryMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n',parent_id=0).order_by('-id')
		# Category = CategoriesSerializer(Categories, many=True)
		# product = EngageboostProducts.objects.using(company_db).all().filter(isblocked='n',isdeleted='n')
		# product = BasicinfoSerializer(product,many=True)
		if(serializer): 
			data ={
				'Rows':serializer.data,
				# 'customergrp':serializer1.data,
				# 'category':Category.data,
				# 'channel':Channel.data,
				# 'product':product.data
				}
		else:
			data ={
					'status':0,
					'api_status':serializer.errors,
					'message':'Data Not Found',
				}
		return Response(data)

	# def put(self, request, pk, format=None,many=True):
	# 	Reviews = self.get_object(pk,request)
	# 	has_multy=request.data['value']
	# 	for data1 in has_multy:
	# 		#print(data1)
	# 		serializer = DiscountConditionsSerializer(Reviews,data=data1)
	# 		if serializer.is_valid():
	# 			serializer.save() 
	# 			data ={
	# 				'status':1,
	# 				'message':'Successfully Updated',
	# 				}
	# 		else:
	# 			data ={
	# 					'status':0,
	# 					'message':'Data Not Found',
	# 					}
	# 	return Response(data)
# Fetch All CustomerGroup Record for page load web services 
class CustomerGroupDiscount(generics.ListAPIView):
		
	def get_object(request, discount_master_id, format=None):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostDiscountMastersConditions.objects.using(company_db).get(discount_master_id=discount_master_id)
		except EngageboostDiscountMastersConditions.DoesNotExist:
			raise Http404

	def get(self, request,discount_master_id, format=None,many=True):
		company_db = loginview.db_active_connection(request)
		# pk=request.data.get('pk')
		user = EngageboostDiscountMastersConditions.objects.using(company_db).all().filter(discount_master_id=discount_master_id)
		serializer = DiscountConditionsSerializer(user,many=True)

		#####################Query Generation#################################
		if request.data.get('search') and request.data.get('order_by'):
			key=request.data.get('search')
			order_by=request.data.get('order_by')
			order_type=request.data.get('order_type')
			if(order_type=='+'):
				order=order_by
			else:
				order='-'+order_by
			result = EngageboostCustomers.objects.using(company_db).all().order_by(order).filter(Q(first_name__icontains=key)|Q(last_sku__icontains=key)|Q(email__icontains=key))
		elif request.data.get('search'):
			key=request.data.get('search')
			result = EngageboostCustomers.objects.using(company_db).all().order_by('-id').filter(Q(first_name__icontains=key)|Q(last_sku__icontains=key)|Q(email__icontains=key))
		elif request.data.get('order_by'):
			order_by=request.data.get('order_by')
			order_type=request.data.get('order_type')
			if(order_type=='+'):
				order=order_by
			else:
				order='-'+order_by
			result = EngageboostCustomers.objects.using(company_db).all().order_by(order)    
		else:
			result = EngageboostCustomers.objects.using(company_db).all().order_by('-id')
		result=result.filter(~Q(pk=discount_master_id)).filter(isblocked='n',isdeleted='n')
		#print(request.data.get('search'))
		page = self.paginate_queryset(result)
		#####################Query Generation#################################
		#####################Layout#################################
		if page is not None:
			serializer_product = CustomerSerializer(page, many=True)
			module='Customers'
			screen_name='list'
			layout_fetch=EngageboostGridLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
			layout_header=layout_fetch.header_name.split("@@")
			layout_field=layout_fetch.field_name.split("@@")
			layout_check=EngageboostGridColumnLayouts.objects.using(company_db).filter(module=module,screen_name=screen_name).count()
			layout={}
			layout_arr=[]

			for header,field in zip(layout_header,layout_field):
				ex_layout_field=field.split(".")
				field_name=ex_layout_field[0]
				if len(ex_layout_field)>1:
					child_name=ex_layout_field[1]
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
				layout={"title":header,"field":field_name,"child":child_name,"show":status}
				layout_arr.append(layout)
			
		#####################Layout#################################  
		pre_data={}
		final_data=[] 
		pre_data['result']=serializer_product.data 
		pre_data['layout']=layout_arr
		pre_data['discount']=serializer.data
		final_data.append(pre_data)
		return self.get_paginated_response(final_data)
# Fetch All Category Record for page load web services
class CategoryLoed(APIView):
	def get(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		Categories = EngageboostCategoryMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n',parent_id=0).order_by('-id')
		Category = CategoriesSerializer(Categories, many=True)
		if(Category):
			data ={
				'status':1,
				'category':Category.data,
			}
		
		else:
			data ={
			'status':0,
			'api_status':serializer.errors,
			'message':'Data Not Found',
			}
		return Response(data)
# select chield category for parent category
class Getchild_category(APIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		category_id=request.data['category_id']
		Categories = EngageboostCategoryMasters.objects.using(company_db).all().filter(parent_id=category_id)
		arr2=[]
		for Categories1 in Categories:
			d2={"id":Categories1.id,"name":Categories1.name}
			arr2.append(d2)
		return HttpResponse(json.dumps({"category":arr2,"status":1}), content_type='application/json')

class ProductLoad(generics.ListAPIView):
# """ List all products from web services """
	

	def post(self, request, format=None,many=True):
		company_db = loginview.db_active_connection(request)
		#####################Query Generation#################################
		if request.data['search']:
			key=request.data['search']
			order_type=request.data['order_type']
			order_by=request.data['order_by']
			if(order_type=='+'):
				order=order_by
			elif(order_type=='-'):
				order='-'+order_by
			cnt = EngageboostProducts.objects.using(company_db).filter(Q(name__icontains=key)|Q(sku__icontains=key)|Q(default_price__icontains=key)).filter(isblocked='n',isdeleted='n').count()
			if cnt !=0:
				result = EngageboostProducts.objects.using(company_db).all().order_by(order).filter(Q(name__icontains=key)|Q(sku__icontains=key)|Q(default_price__icontains=key)).filter(isblocked='n',isdeleted='n')[:100]
				arr=[]
				for product in result:
					data ={
						'id':product.id,
						'name':product.name,
						'sku':product.sku,						
						'default_price':product.default_price						
						}
					arr.append(data)
					data2 ={
							'product':arr
						}
				return Response(data2)
			else:
				data2 ={
							'product':''
						}
				return Response(data2)
		else:
			order_type=request.data['order_type']
			order_by=request.data['order_by']
			if(order_type=='+'):
				order=order_by
			elif(order_type=='-'):
				order='-'+order_by
			result = EngageboostProducts.objects.using(company_db).all().order_by(order).filter(isblocked='n',isdeleted='n')[:100]
			arr=[]
			for product in result:
				data ={
					'id':product.id,
					'name':product.name,
					'sku':product.sku,
					'default_price':product.default_price
					}

				arr.append(data)
				data2 ={
						'product':arr
					}
			return Response(data2)

class ProductLoadPaging(generics.ListAPIView):
	# """ List all products from web services """
	def post(self, request, format=None,many=True):
		company_db = loginview.db_active_connection(request)
		#####################Query Generation#################################
		#print('Chkardahr Sahoo')
		key = ''
		if request.data['search']:
			key = request.data['search']

		order_type = request.data['order_type']
		order_by = request.data['order_by']
		product_id = request.data['product_id']

		if(order_type=='+'):
			order = order_by
		elif(order_type=='-'):
			order = '-'+order_by
	
		parentProduct = EngageboostCossSellProducts.objects.values('product_id').filter(~Q(product_id=product_id))
		
		# print("Parents",parentProduct)

		ownchildProduct = EngageboostCossSellProducts.objects.values('cross_product_id').filter(~Q(product_id=product_id))
		
		# print("Childs",ownchildProduct,ownchildProduct.query)

		proObj = EngageboostProducts.objects.using(company_db).filter(isblocked='n',isdeleted='n').filter(~Q(id=product_id)).values('id')
		product_ids = []
		if proObj.count()>0:
			result = proObj.all()
			for item in result:
				check = EngageboostCossSellProducts.objects.filter(Q(product_id=item['id'])|Q(cross_product_id=item['id'])).filter(~Q(product_id=product_id))
				if check.count()==0:
					product_ids.append(item['id'])
		proObj = EngageboostProducts.objects.using(company_db).filter(id__in=product_ids)
		
		catProduct = EngageboostProductCategories.objects.filter(isblocked='n',isdeleted='n',product_id=product_id).last()
		sameCatProduct = EngageboostProductCategories.objects.filter(isblocked='n',isdeleted='n',category_id=catProduct.category_id).values('product_id')
		
		proObj = proObj.filter(id__in=sameCatProduct)
		
		if key != '':
			proObj = proObj.filter(Q(name__icontains=key)|Q(sku__icontains=key)|Q(default_price__icontains=key))
		# print(proObj.query)
		cnt = proObj.count()
		if cnt !=0:
			result = proObj.all().order_by(order)[:100]
			page = self.paginate_queryset(result)
			arr=[]
			if page is not None:
				serializer_product = EngageboostProductsSerializer(page, many=True)
				serializer_product = serializer_product.data
				for product in serializer_product:
					data ={
						'id':product['id'],
						'name':product['name'],
						'sku':product['sku'],
						'default_price':product['default_price']
					}
					arr.append(data)
			return self.get_paginated_response(arr)
		else:
			data2 = {
				"result":[]
			}
			return Response(data2)

# Customer group web services for Discount Setup Load
class CustomerLoed(APIView):
	def get(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		customergrp = EngageboostCustomerGroup.objects.using(company_db).all().filter(isdeleted='n',
																					  isblocked='n').order_by('name')
		customer = CustomerGroupSerializer(customergrp, many=True)
		if(customer):
			data ={
				'status':1,
				'customer':customer.data,
				
				}
		else:
			data ={
			'status':0,
			'api_status':serializer.errors,
			'message':'Data Not Found',
			}
		return Response(data)

class CustomerType(generics.ListAPIView):
	# """ List all products from web services """
	def post(self, request, format=None,many=True):
		company_db = loginview.db_active_connection(request)
		#####################Query Generation#################################
		if request.data['search']:
			key=request.data['search']
			order_type=request.data['order_type']
			order_by=request.data['order_by']
			if(order_type=='+'):
				order=order_by
			elif(order_type=='-'):
				order='-'+order_by
			cnt = EngageboostCustomerGroup.objects.using(company_db).filter(Q(name__icontains=key)).filter(isblocked='n',isdeleted='n').count()
			if cnt !=0:
				result = EngageboostCustomerGroup.objects.using(company_db).all().order_by(order).filter(Q(name__icontains=key)).filter(isblocked='n',isdeleted='n')[:100]
				arr=[]
				for customergrp in result:
					data ={
						'id':customergrp.id,
						'name':customergrp.name
						}
					arr.append(data)
					data2 ={
						'customergrp':arr
						}
				return Response(data2)
			else:
				data2 ={
						'customergrp':''
						}
				return Response(data2)
		else:
			order_type=request.data['order_type']
			order_by=request.data['order_by']
			if(order_type=='+'):
				order=order_by
			elif(order_type=='-'):
				order='-'+order_by
			result = EngageboostCustomerGroup.objects.using(company_db).all().order_by(order).filter(isblocked='n',isdeleted='n')[:100]
			arr=[]
			for customergrp in result:
				data ={
					'id':customergrp.id,
					'name':customergrp.name
					}
				arr.append(data)
				data2 ={
					'customergrp':arr
					}
			return Response(data2)

class DiscountCustomer(generics.ListAPIView):
	# """ List all products from web services """
	def post(self, request, format=None,many=True):
		company_db = loginview.db_active_connection(request)
		#####################Query Generation#################################
		if request.data['search']:
			key=request.data['search']
			order_type=request.data['order_type']
			order_by=request.data['order_by']
			if(order_type=='+'):
				order=order_by
			elif(order_type=='-'):
				order='-'+order_by
			cnt = EngageboostCustomers.objects.using(company_db).filter(Q(first_name__icontains=key)|Q(email__icontains=key)).filter(isblocked='n',isdeleted='n').count()
			if cnt !=0:
				result = EngageboostCustomers.objects.using(company_db).all().order_by(order).filter(Q(first_name__icontains=key)|Q(email__icontains=key)).filter(isblocked='n',isdeleted='n')[:100]
				arr=[]
				for customer in result:
					data ={
						'id':customer.id,
						'first_name':customer.first_name,
						'last_name':customer.last_name,
						'email':customer.email
						}
					arr.append(data)
					data2 ={
						'customer':arr
						}
				return Response(data2)
			else:
				data2 ={
						'customer':''
						}
				return Response(data2)
		else:
			order_type=request.data['order_type']
			order_by=request.data['order_by']
			if(order_type=='+'):
				order=order_by
			elif(order_type=='-'):
				order='-'+order_by
			result = EngageboostCustomers.objects.using(company_db).all().order_by(order).filter(isblocked='n',isdeleted='n')[:100]
			arr=[]
			for customer in result:
				data ={
					'id':customer.id,
					'first_name':customer.first_name,
					'last_name':customer.last_name,
					'email':customer.email
					}
				arr.append(data)
				data2 ={
					'customer':arr
					}
			return Response(data2)
class CategoriesListDiscount(generics.ListAPIView):
	# """ Categories Selected  """
	#///////////////////Fetch Single Row
	def get(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		Categories = EngageboostCategoryMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n',parent_id=0).order_by('-id')
		Category = CategoriesSerializer(Categories, many=True)
		child_id=EngageboostDiscountMastersConditions.objects.using(company_db).get(id=pk)
		if str(child_id.all_category_id)!='None':
			all_categories=child_id.all_category_id.split(',')
			all_categories = [int(numeric_string) for numeric_string in all_categories]
			all_categories.sort()
			arr2=[]
			for child in all_categories:
				child_id1 = EngageboostCategoryMasters.objects.using(company_db).filter(id=child,isdeleted='n',isblocked='n')
				if child_id1.count() > 0:
					child_id1 = child_id1.first()
					if child_id1.parent_id != 0:
						child_count1=EngageboostCategoryMasters.objects.using(company_db).filter(id=child_id1.parent_id,isdeleted='n',isblocked='n').count()
						if child_count1 > 0:
							child_id2=EngageboostCategoryMasters.objects.using(company_db).get(id=child_id1.parent_id,isdeleted='n',isblocked='n')
							if child_id2.parent_id!=0:
								child_count2=EngageboostCategoryMasters.objects.using(company_db).filter(id=child_id2.parent_id,isdeleted='n',isblocked='n').count()
								if child_count2 >0:
									child_id3=EngageboostCategoryMasters.objects.using(company_db).get(id=child_id2.parent_id,isdeleted='n',isblocked='n')
								if child_id3.parent_id!=0:
									child_count2=EngageboostCategoryMasters.objects.using(company_db).filter(id=child_id3.parent_id,isdeleted='n',isblocked='n').count()
									if child_count2 >0:
										child_id4=EngageboostCategoryMasters.objects.using(company_db).get(id=child_id3.parent_id,isdeleted='n',isblocked='n')
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
								category_1=child_id2.id
								category_2=child_id1.id
								category_3=0
								category_4=0
					else:
						category_1=child_id1.id
						category_2=0
						category_3=0
						category_4=0
					data_parent={"category_1":category_1,"category_2":category_2,"category_3":category_3,"category_4":category_4}	
					arr2.append(data_parent)
			return HttpResponse(json.dumps({"parent_child":arr2,'category':Category.data}), content_type='application/json')		
		else:
			data_parent=[{"category_1":0,"category_2":0,"category_3":0,"category_4":0}]	
			return HttpResponse(json.dumps({"parent_child":data_parent,'category':Category.data}), content_type='application/json')			

class CatrgoryConditionsSet(generics.ListAPIView):
	# Category all for discount coupan
	def get(self, request, format=None,many=True):
		company_db = loginview.db_active_connection(request)
		Categories = EngageboostCategoryMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
		Category = CategoriesSerializer(Categories, many=True)
		if(Category): 
			data ={
				'category':Category.data,
			}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
			}
		return Response(data)

class ImportFileDiscounts(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		datas = []
		db_fields = []
		product_path = 'discounts'
		module_id = 1
		temp_model = 'TempDiscount'
		model = 'Discount'
		filepath = 'importfile'
		post_data = request.data
		if 'import_file' in request.FILES:
			rand = str(random.randint(1,99999))
			file1 = request.FILES['import_file']
			file_name=file1.name
			ext = file_name.split('.')[-1]
			time_stamp = str(int(datetime.datetime.now().timestamp()))
			new_file_name='DiscountImport_'+rand+time_stamp
			fs=FileSystemStorage()
			filename = fs.save(filepath+'/'+product_path+'/'+new_file_name+'.'+ext, file1)
			uploaded_file_url = fs.url(filename)
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

			csvReader = xlrd.open_workbook(settings.BASE_DIR+uploaded_file_url)
			sheet = csvReader.sheet_by_name('Sheet1')
			headers = [str(cell.value) for cell in sheet.row(0)]
			headers = {k: k for k in headers}

		#********* List Of Parent Category *********#
		category_lists = []
		category_cond = EngageboostCategoryMasters.objects.using(company_db).all().filter(website_id=post_data['website_id'],parent_id=0,isblocked="n",isdeleted="n").order_by('name')
		if category_cond:
			category_list = CategoriesSerializer(category_cond,many=True)
			category_lists = category_list.data
		else:
			category_lists = []

		datas = {"category_list":category_lists,"filename":new_file_name+'.'+ext,"xls_header":headers}
		return Response(datas)

class SaveFileDiscounts(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		product_path = 'discounts'
		module_id = 1
		temp_model = 'TempDiscount'
		model = 'Discount'
		filepath = 'importfile'
		datas = []
		custom_field_datas=[]
		post_data = request.data
		# map_fields = post_data["map_fields"]
		# Read xls Data
		fs=FileSystemStorage()
		filename = filepath+'/'+product_path+'/'+post_data["filename"]
		uploaded_file_url = fs.url(filename)
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		if os.path.exists(BASE_DIR):
			csvReader = xlrd.open_workbook(settings.BASE_DIR+uploaded_file_url)
			sheet = csvReader.sheet_by_index(0)
			length=len(sheet.col_values(0))
			xls_column_header_info = []
			xls_column_info={}
			row_no_in_xls= sheet.ncols
			# max_column = sheet.ncols
			for x in range(length):
				if x==0:
					for i in range(row_no_in_xls):
						d11 ={"column_name":sheet.col_values(i)[x],"column_number":i}; xls_column_info=dict(xls_column_info,**d11)
						xls_column_header_info.append(xls_column_info)
				else:
					pass
			for x in range(length):
				if x==0:
					pass
				else:
					has_record = EngageboostTempDiscountMasters.objects.last()
					if has_record:
						last_entry_of_table = EngageboostTempDiscountMasters.objects.order_by('-id').latest('id')
						row_id = int(last_entry_of_table.id)+int(1)
					else:
						row_id = 1

					serializer_data={}
					CF_serializer_data={}
					custom_field_list=[]
					d2 = {}
					d1 = {"id":row_id,"website_id":post_data['website_id'],"file_name":post_data['filename']};
					serializer_data=dict(serializer_data,**d1)
					
					try:
						for xls_column_header in xls_column_header_info:
							
							coupon_type = ""
							disc_type = ""
							column_name = str(xls_column_header["column_name"])
							column_name = column_name.strip()
							column_number = xls_column_header["column_number"]
							field_value = sheet.col_values(column_number)[x] if sheet.col_values(column_number)[x] else None

							if column_name=="Discount Name":
								keyword = "name"
							if column_name=="Discount Description":
								keyword = "description"
							if column_name=="Discount Type":
								keyword = "discount_type"
							if column_name=="Apply Per/Fixed":
								keyword = "disc_type"
								disc_type = field_value
							if column_name=="Coupon Code":
								keyword = "coupon_code"
							if column_name=="Coupon Type":
								keyword = "coupon_type"
							if column_name=="Generate Options":
								keyword = "has_multiplecoupons"
							if column_name=="Number of Coupons":
								keyword = "used_coupon"
							if column_name=="Coupon Prefix":
								keyword = "coupon_prefix"
							if column_name=="Coupon Suffix":
								keyword = "coupon_suffix"
							if column_name=="Discount Amount":
								keyword = "amount"
							if column_name=="Discount Starts":
								keyword = "disc_start_date"
							if column_name=="Discount End":
								keyword = "disc_end_date"
							if column_name=="Max. no of items":
								keyword = "no_of_quantity_per"
							if column_name=="Max Discount Amount":
								keyword = "up_to_discount"
							if column_name=="Offer Type":
								keyword = "offer_type"
							if column_name=="Customer Group":
								keyword = "customer_group"
							if column_name=="Status":
								keyword = "isblocked"
							if column_name=="SKU Equals To":
								keyword = "sku_equals"
							if column_name=="SKU Not Equals To":
								keyword = "sku_not_equals"
							if column_name=="Category Equals To":
								keyword = "category_equals"
							if column_name=="Category Not Equals To":
								keyword = "category_not_equals"
							if column_name=="Amount Equals To":
								keyword = "amount_equals"
							if column_name=="Amount Equals To&GT":
								keyword = "amount_equals_greater"
							if column_name=="Amount Equals To&LT":
								keyword = "amount_equals_less"
							if column_name=="Free Item sku":
								keyword = "free_item_sku"
							if column_name=="Free item Quantity":
								keyword = "free_item_quantity"
							if column_name=="Weekly Equals To":
								keyword = "weekly_equals"
							if column_name=="Weekly Not Equals To":
								keyword = "weekly_not_equals"
							if column_name=="Customer Equals To":
								keyword = "customer_equals"
							if column_name=="Customer Not Equals To":
								keyword = "customer_not_equals"
							if column_name=="Free Shipping":
								keyword = "free_shipping"
							d2.update({keyword:field_value})
						
						if d2['discount_type'].lower()=="product" and d2['disc_type'].lower()=="p":
							d2.update({"disc_type":1})
						elif d2['discount_type'].lower()=="product" and d2['disc_type'].lower()=="f":
							d2.update({"disc_type":2})
						elif d2['discount_type'].lower()=="product" and d2['disc_type'].lower()=="p":
							d2.update({"disc_type":4})
						elif d2['discount_type'].lower()=="coupon" and d2['disc_type'].lower()=="p":
							d2.update({"disc_type":6})
						elif d2['discount_type'].lower()=="coupon" and d2['disc_type'].lower()=="f":
							d2.update({"disc_type":3})
						elif d2['discount_type'].lower()=="coupon" and d2['disc_type'].lower()=="fh":
							d2.update({"disc_type":7})

						if d2['discount_type'].lower()=="product":
							d2.update({"discount_type":"p"})
						elif d2['discount_type'].lower()=="coupon":
							d2.update({"discount_type":"c"})

						if d2['discount_type'].lower()=="coupon" and d2['coupon_type'].lower()=='single use':
							d2.update({"coupon_type":1})
						elif d2['discount_type'].lower()=="coupon" and d2['coupon_type'].lower()=='multiple use':
							d2.update({"coupon_type":2})

						if d2['has_multiplecoupons'].lower()=="single code":
							d2.update({"has_multiplecoupons":'n'})
						elif d2['has_multiplecoupons'].lower()=="multiple code":
							d2.update({"has_multiplecoupons":'y'})

						if d2['coupon_type'].lower()=="single use":
							d2.update({"coupon_type":1})
						elif d2['coupon_type'].lower()=="multiple use":
							d2.update({"coupon_type":2})

						if d2['isblocked'].lower()=="active":
							d2.update({"isblocked":'n'})
						elif d2['isblocked'].lower()=="inactive":
							d2.update({"isblocked":'y'})    
						
						if d2['customer_group']!="" and d2['customer_group']!=None:
							obj = EngageboostCustomerGroup.objects.filter(name=d2['customer_group'])
							if obj.count()>0:
								custgrp=obj.last()
								d2.update({"customer_group":custgrp.id})
							else:
								d2.update({"customer_group":None})	
						

						workbook_datemode = csvReader.datemode
						y, M, d, h, m, s = xlrd.xldate_as_tuple(d2['disc_start_date'], workbook_datemode)
						d2['disc_start_date'] = ("{0}-{1}-{2}".format(y, M, d, h, m, s))

						y, M, d, h, m, s = xlrd.xldate_as_tuple(d2['disc_end_date'], workbook_datemode)
						d2['disc_end_date'] = ("{0}-{1}-{2}".format(y, M, d, h, m, s))    
						
						d2['disc_start_date'] = datetime.datetime.strptime(d2['disc_start_date'],'%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%SZ')
						d2['disc_end_date'] = datetime.datetime.strptime(d2['disc_end_date'],'%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%SZ')
						
						serializer_data=dict(serializer_data,**d2)
							
					except KeyError: no=""

					current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
					d1={"created":current_time,"modified":current_time};
					
					serializer_data=dict(serializer_data,**d1)
					
					try:
						save_temp_product = EngageboostTempDiscountMasters.objects.using(company_db).create(**serializer_data)
						data_status = {"status":1,"filename":post_data["filename"]} 
					except Exception as e :
						data_status = {"status":0,"filename":post_data["filename"],'errors':str(e) }
			
			os.remove(settings.BASE_DIR+uploaded_file_url)
		else:
			data_status = {"status":0,"filename":post_data["filename"],'errors':"File Not Exists" }
		return Response(data_status)

class PreviewSaveFileDiscounts(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		post_data = request.data
		fetch_all_data = []
		data = {}
		if post_data["model"] == "discount":
			fetch_all_data_cond = EngageboostTempDiscountMasters.objects.using(company_db).all().filter(website_id=post_data['website_id'],file_name=post_data['filename']) #fetch from temp product table
			if fetch_all_data_cond:
				fetch_all_datas = TempDiscountsSerializer(fetch_all_data_cond,many=True)
				# fetch_all_data = fetch_all_datas.data
				for fad in fetch_all_datas.data:
					#print(check_exported_data(fad,request))
					error=[]
					special_char='no'
					if error:
						fad["error"] = 1
						fad["error_message"] = error
					else:
						error.append("SUCCESS")
						fad["error"] = 0
						fad["error_message"] = error

				fetch_all_data = fetch_all_datas.data
				
			data = {"preview_data":fetch_all_data,"filename":post_data['filename']}
		return Response(data)

class SaveAllImportedDiscounts(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		product_path = 'discount'
		module_id = 1
		temp_model = 'TempDiscount'
		model = 'Discount'
		datas = []
		fetch_temp_datas = []
		# map_field_dict="";map_field_array=[]
		post_data = request.data

		selectedIds = post_data["selected_ids"].split(',')

		for i in selectedIds:
			fetch_temp_data_cond = EngageboostTempDiscountMasters.objects.using(company_db).filter(id=int(i)).first()
			if fetch_temp_data_cond:
				fetch_temp_data = TempDiscountsSerializer(fetch_temp_data_cond,partial=True)
				fetch_temp_datas.append(fetch_temp_data.data)

		for fetchtempdatas in fetch_temp_datas:
			serializer_data = {}
			serializer_data = dict(serializer_data,**fetchtempdatas)
			
			if fetchtempdatas['discount_type']=="c":
				discount_master_type = 1
			elif fetchtempdatas['discount_type']=="p":
				discount_master_type = 0

			current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
			d1 = {"discount_master_type":discount_master_type,"website_id":fetchtempdatas["website_id"],"created":current_time,"modified":current_time}

			serializer_data = dict(serializer_data,**d1)
			datas.append(serializer_data)
			serializer = DiscountMasterSerializer(data=serializer_data,partial=True)
			if serializer.is_valid():
				serializer.save()
				responseDatas = {"status":1,"api_response":datas,"message":'Discounts Saved'}
			else:
				data ={'status':0,'api_status':serializer.errors,'message':'Error Occured'}
				datas.append(data)

				responseDatas = {"status":0,"api_response":datas,"message":'Error Occured in Discounts'}
		
		EngageboostTempDiscountMasters.objects.using(company_db).filter(file_name=post_data['filename']).delete()
		return Response(responseDatas)

# Set discount condition(Insert new records)
class DiscountCouponCondition(generics.ListAPIView):
	def post(self, request, format=None):
		datas=[]
		company_db = loginview.db_active_connection(request)
		discount_master_id=request.data['discount_master_id']
		disc_cnt=EngageboostDiscountMasters.objects.using(company_db).filter(id=discount_master_id,discount_type="c").count()
		
		if disc_cnt>0:
			cnt=EngageboostDiscountMastersConditions.objects.using(company_db).filter(discount_master_id=discount_master_id).count()
			if cnt >0:
				EngageboostDiscountMastersConditions.objects.using(company_db).filter(discount_master_id=discount_master_id).delete()
			has_multy=request.data['value']
			error = []
			datas = []
			for data in has_multy:
				# serializer_data = dict()

				if data['fields']=="-1"or data['fields']=="-4" or data['fields']=="-2" or data['fields']=="-3" or data['fields']=="9175" or data['fields']=="0": 
					
					has_record = EngageboostDiscountMastersConditions.objects.using(company_db).last()
					if has_record:
						last_entry_of_table = EngageboostDiscountMastersConditions.objects.order_by('-id').latest('id')
						row_id = int(last_entry_of_table.id)+int(1)

					else:
						row_id = 1
					
					d1={"id":row_id};

					#Customer
					if data['fields']=="-2":
						if not 'all_customer_id' in data or data['all_customer_id']=="" or data['all_customer_id']==None:
							data.update({"error":"Select customers"})
							error.append(data)
					
					#Week Days
					elif data['fields']=="-3":
						if not 'all_day_id' in data or data['all_day_id']=="" or data['all_day_id']==None:
							data.update({"error":"Select Days"})
							error.append(data)
					
					#Free Shipping or Order Amount
					elif data['fields']=="-4" or data['fields']=="-1":
						if not 'value' in data or data['value']=="" or data['value']==None:
							data.update({"error":"Enter value"})
							error.append(data)

					#SKU
					elif data['fields']=="9175":
						if not 'all_product_id' in data or data['all_product_id']=="" or data['all_product_id']==None:
							data.update({"error":"Select Products"})
							error.append(data)
						
					#Category
					elif data['fields']=="0":
						if not 'all_category_id' in data or data['all_category_id']=="" or data['all_category_id']==None:
							data.update({"error":"Select Categories"})
							error.append(data)
							
					data=dict(data,**d1)
					now = datetime.datetime.now()
					current_time = now.strftime("%Y-%m-%d")
					d3 = {"created":current_time,"modified":current_time}
					data=dict(data,**d3)
					
					# datas.append(data)

					serializer = DiscountConditionsSerializer(data=data,partial=True)
					if serializer.is_valid():
						serializer.save()
					else:
						data.update({"error":serializer.errors})
						error.append(data)	
				else:
					data.update({"error":"Invalid discount type"})
					error.append(data)
		else:
			error.append("Invalid discount")
		if len(error)>0:
			context ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Something went wrong',
			}
		else:
			context ={
				'status':1,
				'api_status':'',
				'message':'Successfully Inserted',
			}
		return Response(context)
		# return Response(datas)

# Set discount condition(Insert new records)
class DiscountProductFree(generics.ListAPIView):
	def post(self, request, format=None):
		data=request.data
		company_db = loginview.db_active_connection(request)
		now = datetime.datetime.now()
		current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
		d3 = {"created":current_time,"modified":current_time}
		data = dict(data,**d3)
		#print(data)
		serializer = DiscountMasterSerializer(data=data,partial=True)
		if serializer.is_valid():
			prev_products = list(EngageboostDiscountMastersConditions.objects.filter(discount_master_id = serializer.id).values_list('all_product_id',flat=True))
			
			serializer.save()
			# if(serializer.id):
			# 	objproduct_list = EngageboostDiscountMastersConditions.objects.filter(discount_master_id = serializer.id).values_list('all_product_id',flat=True)
			# 	if(prev_products):
			# 		objproduct_list = list(objproduct_list)
			# 		objproduct_list.extend(prev_products)
			# 		objproduct_list = list(set(objproduct_list))
			# 	if objproduct_list :
			# 		for elastic_product_id in objproduct_list:
			# 			if(elastic_product_id!=""):
			# 				if("," in elastic_product_id):
			# 					prod_lst = elastic_product_id.split(",")
			# 					for prod_id in prod_lst:
			# 						if(prod_id!=""):
			# 							elastic = common.save_data_to_elastic(int(prod_id),'EngageboostProducts')
			# 				else:
			# 					elastic = common.save_data_to_elastic(int(elastic_product_id),'EngageboostProducts')

			if(serializer.id):
				objproduct_list = EngageboostDiscountMastersConditions.objects.filter(discount_master_id = serializer.id).values_list('all_product_id',flat=True)
				if(prev_products):
					objproduct_list = list(objproduct_list)
					objproduct_list.extend(prev_products)
					objproduct_list = list(set(objproduct_list))
				if objproduct_list :
					for elastic_product_id in objproduct_list:
						if(elastic_product_id != "" and elastic_product_id is not None):
							try:
								if("," in elastic_product_id):
									prod_lst = elastic_product_id.split(",")
									elastic = common.update_bulk_elastic('EngageboostProducts',prod_lst,'channel_currency_product_price','update')
								else:
									elastic = common.update_bulk_elastic('EngageboostProducts',[int(elastic_product_id)],'channel_currency_product_price','update')
							except:
								elastic = common.update_bulk_elastic('EngageboostProducts',[int(elastic_product_id)],'channel_currency_product_price','update')	
			
			context ={
					'status':1,
					'api_status':'',
					'message':'Successfully Inserted',
				}
		else:
			context ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Something went wrong',
			}


		return Response(context)
		# return Response(datas)


class CouponExport(generics.ListAPIView):

	def post(self, request, *args, **kwargs):
		company_db = loginview.db_active_connection(request)
		try:
			discount_master_id=request.data['discount_master_id']
			## ************  Check file dir exist or not. If dir not exist then create
			file_dir = settings.MEDIA_ROOT+'/exportfile/'
			export_dir = settings.MEDIA_URL+'exportfile/'
			if not os.path.exists(file_dir):
				os.makedirs(file_dir)
			## ************  Create file name
			file_name = "coupon_export_"+get_random_string(length=5)

			## Create file full path
			file_path = file_dir+file_name+'.xlsx'
			export_file_path = export_dir+file_name+'.xlsx'
			export_file_path = export_file_path[1:]

			workbook 	= xlsxwriter.Workbook(file_path)		
			worksheet 	= workbook.add_worksheet()

			bold = workbook.add_format({'bold': True})
			row = 1

			worksheet.write(0,0,'ID',bold)
			worksheet.write(0,1,'Coupon Code',bold)
			worksheet.write(0,2,'Is Used',bold)

			is_used = ""
			result = EngageboostDiscountMastersCoupons.objects.using(company_db).filter(isdeleted='n',discount_master_id=discount_master_id).order_by('id')
			result_count = result.count()
			
			if result_count>0:
				result_data = DiscountMasterCouponSerializer(result, many=True)
				result_data = result_data.data

				for resultdata in result_data:
					if resultdata['is_used']=="y":
						is_used = "Yes"
					else:
						is_used = "No"	
					worksheet.write(row,0,resultdata['id'],0)
					worksheet.write(row,1,resultdata['coupon_code'],0)
					worksheet.write(row,2,is_used,0)
					row = row + 1
				workbook.close()
				data ={'status':1,"file_path":export_file_path}
			else:
				data ={'status':0,"message":"No coupon found for this promotion"}

		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}		
					
		return Response(data)



# @csrf_exempt
# @permission_classes((AllowAny,))
def check_exported_data(serializer_data,request):
	company_db = loginview.db_active_connection(request)
	d2 = {'status':'','err_flag':'','error_text':[]}
	current_time = datetime.datetime.now()
	serializer_data['disc_start_date'] = datetime.datetime.strptime(serializer_data['disc_start_date'],'%Y-%m-%dT%H:%M:%SZ')
	serializer_data['disc_end_date'] = datetime.datetime.strptime(serializer_data['disc_end_date'],'%Y-%m-%dT%H:%M:%SZ')
	coupon=EngageboostDiscountMasters.objects.using(company_db).filter(coupon_code=serializer_data['coupon_code'],isblocked="n",isdeleted="n").count()

	if serializer_data['discount_type'] == 'coupon' and serializer_data['coupon_code'] == "" and serializer_data['has_multiplecoupons'] == "Single Code": 
		d2['error_text'].append("Coupon code is missing")

	if serializer_data['discount_type'] == 'coupon' and serializer_data['has_multiplecoupons'] == "Multiple Code" and serializer_data['used_coupon'] <= 0: 
		d2['error_text'].append("Number of coupons should not blank")

	if serializer_data['discount_type'] == 'product' and serializer_data['offer_type'] == "" : 
		d2['error_text'].append("Offer type should not blank")

	if serializer_data['coupon_type'] == "" and serializer_data['discount_type'] == 'coupon': 
		d2['error_text'].append("Coupon type does not exist")

	if serializer_data['name'] == "": 
		d2['error_text'].append("Discount name is missing")

	if serializer_data['amount'] == "": 
		d2['error_text'].append("Discount amount should not blank")

	if serializer_data['disc_start_date']=="": 
		d2['error_text'].append("Start date should not blank")

	if serializer_data['disc_start_date']<current_time:	
		d2['error_text'].append("Start date should not less than current date")

	if serializer_data['disc_end_date'] == "": 
		d2['error_text'].append("End date should not blank")

	if serializer_data['disc_end_date']<current_time:	
		d2['error_text'].append("End date should not less than current date")	

	if serializer_data['disc_end_date']<=serializer_data['disc_start_date']:
		d2['error_text'].append("End date should be greater than Start date")

	if serializer_data['offer_type'] == "": 
		d2['error_text'].append("Offer type is missing")

	if serializer_data['customer_group'] == "":
		d2['error_text'].append("Customer group is missing")

	if serializer_data['isblocked'] == "":
		d2['error_text'].append("Status is missing")

	if serializer_data['disc_type'] == "":
		d2['error_text'].append("Apply per should not blank")

	if coupon > 0:
		d2['error_text'].append("Coupon code exist")

	if len(d2['error_text'])>0:
		d2['err_flag']= 1
	else: 
		d2['err_flag']= 0

	serializer_data=dict(serializer_data,**d2)
	return serializer_data