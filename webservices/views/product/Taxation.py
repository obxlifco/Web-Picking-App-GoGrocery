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

import datetime
import json
import random
import os
import xlrd
import sys
import traceback
from webservices.views.common import common
from webservices.views.common.threading import *
from webservices.views.emailcomponent import emailcomponent
from elasticsearch import helpers
from django.apps import apps

# class ProductTaxClass is used to insert ProductTaxClass
class ProductTaxClass(generics.ListAPIView):
	def get(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		obj = EngageboostProductTaxClasses.objects.using(company_db)
		objcount = obj.filter(id=pk).count()
		if objcount>0:
			creditObj = obj.get(id=pk)
			serializer = ProducttaxclassesSerializer(creditObj,partial=True)
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

	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		has_multy=request.data['value']
		
		try:
			if has_multy['id']:
				tax_id = has_multy['id']
		except KeyError: 
				tax_id = ""		
		#is_mul = has_multy['has_multiplecoupons']
		d1={'created':date.today(),'modified':date.today()}
		serializer_data=dict(has_multy,**d1)

		if tax_id:
			serializer_data.pop("id")
			creditObj = EngageboostProductTaxClasses.objects.using(company_db).get(id=tax_id)
			serializer = ProducttaxclassesSerializer(creditObj,data=serializer_data,partial=True)
			if serializer.is_valid():
				serializer.save()
				data ={
				'status':1,
				'api_status':{"id":tax_id},
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
			serializer = ProducttaxclassesSerializer(data=serializer_data,partial=True)
			if serializer.is_valid():
				serializer.save()
				obj = EngageboostProductTaxClasses.objects.using(company_db).latest('id')
				last_id = obj.id
				
				data ={
				'status':1,
				'api_status':{"id":last_id},
				'message':'Successfully Inserted',
				}
				return Response(data)
			else:
				data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
				return Response(data)					

# class CustomerTaxClass is used to insert CustomerTaxClass
class CustomerTaxClass(generics.ListAPIView):
	def get(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		obj = EngageboostCustomerTaxClasses.objects.using(company_db)
		objcount = obj.filter(id=pk).count()
		if objcount>0:
			creditObj = obj.get(id=pk)
			serializer = CustomerTaxClassesSerializer(creditObj,partial=True)
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

	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		has_multy=request.data['value']
		
		try:
			if has_multy['id']:
				tax_id = has_multy['id']
		except KeyError: 
				tax_id = ""		
		#is_mul = has_multy['has_multiplecoupons']
		d1={'created':date.today(),'modified':date.today()}
		serializer_data=dict(has_multy,**d1)

		if tax_id:
			serializer_data.pop("id")
			creditObj = EngageboostCustomerTaxClasses.objects.using(company_db).get(id=tax_id)
			serializer = CustomerTaxClassesSerializer(creditObj,data=serializer_data,partial=True)
			if serializer.is_valid():
				serializer.save()
				data ={
				'status':1,
				'api_status':{"id":tax_id},
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
			serializer = CustomerTaxClassesSerializer(data=serializer_data,partial=True)
			if serializer.is_valid():
				serializer.save()
				obj = EngageboostCustomerTaxClasses.objects.using(company_db).latest('id')
				last_id = obj.id
				
				data ={
				'status':1,
				'api_status':{"id":last_id},
				'message':'Successfully Inserted',
				}
				return Response(data)
			else:
				data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
				return Response(data)					

# class TaxRate is used to insert TaxRate
class TaxRate(generics.ListAPIView):
	def get(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		obj = EngageboostTaxRates.objects.using(company_db)
		objcount = obj.filter(id=pk).count()
		if objcount>0:
			creditObj = obj.get(id=pk)
			serializer = TaxratesSerializer(creditObj,partial=True)
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

	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		serializer_data=request.data['value']
		
		try:
			if serializer_data['id']:
				tax_id = serializer_data['id']
		except KeyError: 
				tax_id = ""		
		#is_mul = has_multy['has_multiplecoupons']
		# d1={'created':date.today(),'modified':date.today()}
		# serializer_data=dict(serializer_data,**d1)

		if tax_id:
			serializer_data.pop("id")
			creditObj = EngageboostTaxRates.objects.using(company_db).get(id=tax_id)
			serializer = TaxratesSerializer(creditObj,data=serializer_data,partial=True)
			if serializer.is_valid():
				obj = EngageboostTaxRates.objects.filter(id=tax_id).update(**serializer_data)
				
				data ={
				'status':1,
				'api_status':{"id":tax_id},
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
			serializer = TaxratesSerializer(data=serializer_data,partial=True)
			if serializer.is_valid():
				EngageboostTaxRates.objects.create(**serializer_data)
				# serializer.save()
				obj = EngageboostTaxRates.objects.using(company_db).latest('id')
				last_id = obj.id
				
				data ={
				'status':1,
				'api_status':{"id":last_id},
				'message':'Successfully Inserted',
				}
				return Response(data)
			else:
				data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
				return Response(data)


# class TaxRule is used to insert TaxRule
class TaxRule(generics.ListAPIView):
	def get(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		obj = EngageboostTaxRuleTables.objects.using(company_db)
		objcount = obj.filter(id=pk).count()
		if objcount>0:
			creditObj = obj.get(id=pk)
			serializer = TaxRuleTablesSerializer(creditObj,partial=True)
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

	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		serializer_data=request.data['value']
		
		try:
			if serializer_data['id']:
				tax_id = serializer_data['id']
		except KeyError: 
				tax_id = ""		
		#is_mul = has_multy['has_multiplecoupons']
		# d1={'created':date.today(),'modified':date.today()}
		# serializer_data=dict(serializer_data,**d1)
		error = []
		if not 'rule_name' in serializer_data.keys() or serializer_data['rule_name']=="" or serializer_data['rule_name']==None:
			error.append("Enter Rule Name")
		if not 'tax_rate_id' in serializer_data.keys() or serializer_data['tax_rate_id']=="" or serializer_data['tax_rate_id']==None:
			error.append("Select Tax Rules")
		if not 'priority' in serializer_data.keys() or serializer_data['priority']=="" or serializer_data['priority']==None:
			error.append("Enter Priority")		
		
		if len(error)==0:
			if tax_id:
				serializer_data.pop("id")
				creditObj = EngageboostTaxRuleTables.objects.using(company_db).get(id=tax_id)
				serializer = TaxRuleTablesSerializer(creditObj,data=serializer_data,partial=True)
				if serializer.is_valid():
					EngageboostTaxRuleTables.objects.filter(id=tax_id).update(**serializer_data)
					data ={
					'status':1,
					'api_status':{"id":tax_id},
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
				serializer = TaxRuleTablesSerializer(data=serializer_data,partial=True)
				if serializer.is_valid():
					EngageboostTaxRuleTables.objects.create(**serializer_data)
					# serializer.save()
					obj = EngageboostTaxRuleTables.objects.using(company_db).latest('id')
					last_id = obj.id
					
					data ={
					'status':1,
					'api_status':{"id":last_id},
					'message':'Successfully Inserted',
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
				'api_status':error,
				'message':'Something went wrong',
			}
			return Response(data)							

# class TaxSettings is used to insert TaxSettings
class TaxSettings(generics.ListAPIView):
	def get(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		#website_id = self.request.GET.get("website_id")
		obj = EngageboostTaxSettings.objects.using(company_db).filter(website_id=pk)
		objcount = obj.count()
		if objcount>0:
			creditObj = obj.first()
			serializer = Taxsettings(creditObj,partial=True)
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

	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		serializer_data=request.data['value']
		# print(serializer_data)
		error = []
		
		if not "apply_customer_tax" in serializer_data.keys() or serializer_data['apply_customer_tax']=="" or serializer_data['apply_customer_tax']==None:
				error.append("Select Apply Customer Tax")
		if not "catalog_prices" in serializer_data.keys() or serializer_data['catalog_prices']=="" or serializer_data['catalog_prices']==None:
				error.append("Select Catalog Prices")
		if not "apply_discount_on_prices" in serializer_data.keys() or serializer_data['apply_discount_on_prices']=="" or serializer_data['apply_discount_on_prices']==None:
				error.append("Select Apply discount on Prices")
		if not "website_id" in serializer_data.keys() or serializer_data['website_id']=="" or serializer_data['website_id']==None:
				error.append("Select Apply discount on Prices")						
		if len(error)==0:
			d1={'created':date.today(),'modified':date.today()}
			serializer_data=dict(serializer_data,**d1)
			serializer = Taxsettings(data=serializer_data,partial=True)
			if serializer.is_valid():
				EngageboostTaxSettings.objects.using(company_db).filter(website_id=serializer_data['website_id']).delete()
				serializer.save()
				obj = EngageboostTaxSettings.objects.using(company_db).filter(website_id=serializer_data['website_id']).first()
				last_id = Taxsettings(obj,partial=True)
				
				data ={
				'status':1,
				'api_status':serializer.data,
				'message':'Successfully Saved',
				}
				return Response(data)
			else:
				data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Please enter valid adata',
				}
				return Response(data)
		else:	
			data ={
				'status':0,
				'api_status':error,
				'message':'Something went wrong',
				}
			return Response(data)	
			
# class ProductPriceType is used to insert ProductPriceType
class ProductPriceType(generics.ListAPIView):
	def get(self, request, format=None):
		pk = request.GET.get("id")
		product = request.GET.get("product")
		price_type = request.GET.get("price_type")

		company_db = loginview.db_active_connection(request)
		obj = EngageboostProductPriceTypeMaster.objects.using(company_db)

		if pk!=None and pk!="":
			obj = obj.filter(id=pk)
		if product!=None and product!="":
			obj = obj.filter(product_id=product)
		if price_type!=None and price_type!="":
			obj = obj.filter(price_type_id=price_type)

		
		objcount = obj.count()
		if objcount>0:
			creditObj = obj.last()
			serializer = ProductPriceTypeMasterSerializer(creditObj,partial=True)
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
				

	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		has_multy=request.data
		
		try:
			if has_multy['id']:
				tax_id = has_multy['id']
		except KeyError: 
				tax_id = ""	

		try:
			if has_multy['price_type_id']:
				price_type = has_multy['price_type_id']
		except KeyError: 
				price_type = ""

		try:
			if has_multy['product_id']:
				product = has_multy['product_id']
		except KeyError: 
				product = ""		

		#is_mul = has_multy['has_multiplecoupons']
		current_data = datetime.datetime.now(datetime.timezone.utc).astimezone()
		d1={'created':current_data,'modified':current_data}
		serializer_data=dict(has_multy,**d1)

		if tax_id:
			EngageboostProductPriceTypeMaster.objects.using(company_db).filter(id=tax_id).update(**serializer_data)
			data ={
				'status':1,
				'api_status':{"id":tax_id},
				'message':'Successfully Updated',
				}	

			return Response(data)
		else:
			if price_type!="" and price_type!=None and product!="" and product!=None:
				Price_Obj = EngageboostProductPriceTypeMaster.objects.using(company_db).filter(price_type_id=price_type,product_id=product)
				if Price_Obj.count()>0:
					Price_data = Price_Obj.last()
					# serializer = ProductPriceTypeMasterSerializer(Price_data,data=serializer_data,partial=True)
					EngageboostProductPriceTypeMaster.objects.using(company_db).filter(price_type_id=price_type,product_id=product).update(**serializer_data)
					data ={
							'status':1,
							'api_status':{"id":Price_data.id},
							'message':'Successfully Saved',
							}
				else:
					# serializer = ProductPriceTypeMasterSerializer(data=serializer_data,partial=True)
					EngageboostProductPriceTypeMaster.objects.using(company_db).create(**serializer_data)
					obj = EngageboostProductPriceTypeMaster.objects.using(company_db).latest('id')
					last_id = obj.id
					
					data ={
						'status':1,
						'api_status':{"id":last_id},
						'message':'Successfully Saved',
						}
				return Response(data)					

class ProductWareHouse(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		has_multy=request.data

		if 'product' in has_multy.keys() and has_multy['product']!=None and has_multy['product']!="":
			product_id = has_multy['product']
		else:
			data ={
					'status':0,
					'api_status':"",
					'message':'Invalid Product',
				}						
			return Response(data)

		user                = request.user
		user_id             = user.id
		warehouseObj = 0
		if user_id!=None and user_id!="":
			userdetails = EngageboostUsers.objects.filter(id=user_id)
			if userdetails.count()>0:
				userdetails = userdetails.first()
				if userdetails.issuperadmin!="Y":
					userObj = EngageboostWarehouseManager.objects.filter(manager_id=user_id).first()
					if userObj:
						warehouseObj = userObj.warehouse_id

		# print('warehouse_obj===', warehouse_obj.query)

		all_valid_price_type_ids = []
		mainObj = EngageboostPriceTypeMaster.objects.filter(isdeleted="n",isblocked="n")

		if mainObj.count()>0:
			mainObj = mainObj.values().all()
			for price_type_item in mainObj:
				if int(warehouseObj)>0:
					print("k2")
					subObj = EngageboostProductPriceTypeMaster.objects.filter(isdeleted="n",isblocked="n",price_type_id=price_type_item['id'],product_id=product_id,warehouse_id__iregex=r"\y{0}\y".format(warehouseObj)).order_by("id")
				else:
					print("k1")
					subObj = EngageboostProductPriceTypeMaster.objects.filter(isdeleted="n",isblocked="n",price_type_id=price_type_item['id'],product_id=product_id).order_by("id")

				print("==============================",subObj.query)
				if subObj.count()>0:
					# subObj = subObj.values().first()
					subObj = subObj.values().all()
					for price in subObj:
						all_valid_price_type_ids.append(price['id'])

		if len(all_valid_price_type_ids)>0:
			if int(warehouseObj)>0:
				obj = EngageboostProductPriceTypeMaster.objects.using(company_db).filter(isblocked='n',isdeleted='n',id__in=all_valid_price_type_ids,  warehouse_id__iregex=r"\y{0}\y".format(warehouseObj)).order_by("price_type")
			else:
				obj = EngageboostProductPriceTypeMaster.objects.using(company_db).filter(isblocked='n',isdeleted='n',id__in=all_valid_price_type_ids).order_by("price_type")

			if 'product' in has_multy.keys() and has_multy['product']!=None and has_multy['product']!="":
				product = has_multy['product']
				obj = obj.filter(product_id=product)
			if 'website_id' in has_multy.keys() and has_multy['website_id']!=None and has_multy['website_id']!="":
				website_id = has_multy['website_id']
				obj = obj.filter(website_id=website_id)
			if 'price_type_id' in has_multy.keys() and has_multy['price_type_id']!=None and has_multy['price_type_id']!="":
				product_price_type = has_multy['price_type_id']
				product_price_type = product_price_type.split(",")
				obj = obj.filter(price_type_id__in=product_price_type)	
			
			warehouse_arr = []
			objcount = obj.count()
			if objcount>0:
				pro_price_type_obj=obj.all()
				
				pro_price_types = ProductPriceTypeMasterSerializer(pro_price_type_obj,many=True)

				for pro_price_type in pro_price_types.data:
					# print("==============",pro_price_type['id'])
					pricedata = []
					if warehouseObj:
						warhouse_obj = EngageboostWarehouseMasters.objects.using(company_db).filter(isblocked='n',isdeleted='n',  id = warehouseObj)
					else:
						warhouse_obj = EngageboostWarehouseMasters.objects.using(company_db).filter(isblocked='n',isdeleted='n')
						
					warehouse_ids = []
					warehouses = []
					if pro_price_type['warehouse_id']:
						warehouse_ids = pro_price_type['warehouse_id'].split(",")			
						if 'warehouse_id' in has_multy.keys() and has_multy['warehouse_id']!=None and has_multy['warehouse_id']!="":
							warehouses = has_multy['warehouse_id']
							warehouses = warehouses.split(",")
							warehouse_ids2 = warehouses
							
							warehouse_ids = list(set(warehouse_ids).intersection(warehouse_ids2))
					val = []
					for i in range(len(warehouse_ids)):
						if warehouse_ids[i] !='None':
							val.append(warehouse_ids[i])
					
					warehouse_ids = val

					warhouse_obj = warhouse_obj.filter(id__in=warehouse_ids)
					
					if has_multy['website_id'] and has_multy['website_id']!=None and has_multy['website_id']!="":
						warhouse_obj = warhouse_obj.filter(website_id=website_id)

					if warhouse_obj.count()>0:
						warhouse_data = warhouse_obj.all()
						warhousedata = WarehousemastersSerializer(warhouse_data,many=True)
						price_type_id = pro_price_type['id']
						price_type_name = pro_price_type['name']
						price_type_master_name = pro_price_type['price_type']['name']
						price_type_master_id = pro_price_type['price_type']['id']

						for k in warhousedata.data:
							obj = EngageboostChannelCurrencyProductPrice.objects.using(company_db).filter(product_price_type_id=pro_price_type['id'],warehouse_id=k['id'],product_id=product)
							cost_price = common.get_product_cost(product,k['id'])
							
							# print("=================",cost_price)
							if obj.count()>0:
								rs = obj.all()
								# for v in rs:
								rs_data = ChannelCurrencyProductPriceSerializer(rs,many=True)
								d1={"warehouse_name":k['name'],"warehouse_id":k['id'],"cost":cost_price}
								temp = []
								
								for price_data in rs_data.data:
									temp.append(price_data)
								
								# price_data = dict(price_data,**d1)

								pricedata.append({"warehousedata":temp,"warehouse_name":k['name'],"warehouse_id":k['id']})
							else:
								prices = EngageboostChannelCurrencyProductPrice._meta.get_fields(include_hidden=True)
								arr = {}
								for price in prices:
									if price.name=="cost" or price.name=="price" or price.name=="mrp":
										j={price.name:cost_price}
									else:
										j={price.name:""}	
									arr = dict(arr,**j)
								d1={"product":product,"product_price_type":pro_price_type['id']}
								arr = dict(arr,**d1)		
								# pricedata.append(arr)

								pricedata.append({"warehousedata":[arr],"warehouse_name":k['name'],"warehouse_id":k['id']})
								
						warehouse_arr.append({"name":price_type_name,"warehouse_id":k['id'],"master_name":price_type_master_name,"master_id":price_type_master_id,"product_price_type_id":price_type_id,"data":pricedata})		
				# data = pricedata
				return Response({"status":1,'api_status':warehouse_arr})
			else:		
				data ={
						'status':0,
						'api_status':"",
						'message':'Data Not Found',
					}						
				return Response(data)
		else:		
			data ={
					'status':0,
					'api_status':"",
					'message':'Data Not Found',
				}						
			return Response(data)

class PriceType(generics.ListAPIView):
	def get(self, request, pk=None, format=None):
		company_db = loginview.db_active_connection(request)
		obj = EngageboostPriceTypeMaster.objects.using(company_db)
		
		if pk:
			objcount = obj.filter(id=pk)

		objcount = obj.count()
		if objcount>0:
			if pk:
				creditObj = obj.last()
				serializer = PriceTypeMasterSerializer(creditObj,partial=True)
			else:
				creditObj = obj.all()
				serializer = PriceTypeMasterSerializer(creditObj,many=True)	
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

	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		serializer_data=request.data
		website_id=serializer_data["website_id"]
		obj = EngageboostPriceTypeMaster.objects.using(company_db)
		objcount = obj.filter(website_id=website_id).count()
		if objcount>0:
			creditObj = obj.filter(website_id=website_id)
			serializer = PriceTypeMasterSerializer(creditObj,many=True)
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

class ProductPriceTypeList(generics.ListAPIView):
	def post(self, request, format=None):
		has_multy=request.data
		company_db = loginview.db_active_connection(request)
		obj = EngageboostProductPriceTypeMaster.objects.using(company_db)

		try:
			if has_multy['price_type_id']:
				price_type_id = has_multy['price_type_id']
				obj = obj.filter(price_type_id=price_type_id)
		except KeyError: 
				price_type_id = ""

		try:
			if has_multy['product_id']:
				product_id = has_multy['product_id']
				obj = obj.filter(product_id=product_id)
		except KeyError: 
				product_id = ""

		objcount = obj.count()
		if objcount>0:
			creditObj = obj.last()
			serializer = ProductPriceTypeMasterSerializer(creditObj,partial=True)
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

class ChannelCurrencyProductPrice(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		seialized_data = request.data['values']
		# print(seialized_data)
		datas = []
		errors = []
		elastic_product_id = ""
		productId = ""

		if 'product_id' in request.data.keys() and request.data['product_id']!=None and request.data['product_id']!="":
			productId = request.data['product_id']
			EngageboostChannelCurrencyProductPrice.objects.filter(product_id=productId).delete()

		for has_multy in seialized_data:
			tax_id=""
			product_id =""
			warehouse_id=""
			max_quantity =""
			min_quantity=""
			product_price_type = ""
			
			if 'id' in has_multy.keys() and has_multy['id']!=None and has_multy['id']!="":
				tax_id = has_multy['id']

			if 'product_id' in has_multy.keys() and has_multy['product_id']!=None and has_multy['product_id']!="":
				product_id = has_multy['product_id']
				has_multy['product'] = has_multy['product_id']
				elastic_product_id = has_multy['product_id']
				
			if 'warehouse_id' in has_multy.keys() and has_multy['warehouse_id']!=None and has_multy['warehouse_id']!="":
				warehouse_id = has_multy['warehouse_id']
				
			if 'max_quantity' in has_multy.keys() and has_multy['max_quantity']!=None and has_multy['max_quantity']!="":
				max_quantity = has_multy['max_quantity']

			if 'min_quantity' in has_multy.keys() and has_multy['min_quantity']!=None and has_multy['min_quantity']!="":
				min_quantity = has_multy['min_quantity']
				
			if 'product_price_type' in has_multy.keys() and has_multy['product_price_type']!=None and has_multy['product_price_type']!="":
				product_price_type = has_multy['product_price_type']

			if 'start_date' in has_multy.keys() and (has_multy['start_date']==None or has_multy['start_date']==""):
				has_multy.pop('start_date')
				
			if 'end_date' in has_multy.keys() and (has_multy['end_date']==None or has_multy['end_date']==""):
				has_multy.pop('end_date')	

			#is_mul = has_multy['has_multiplecoupons']
			# lastObj = EngageboostChannelCurrencyProductPrice.objects.latest('id')
			lastObj = EngageboostChannelCurrencyProductPrice.objects.order_by("-id").first()
			last_id = 0
			if lastObj:
				last_id = int(lastObj.id)
			last_id = last_id+1
			current_data = datetime.datetime.now(datetime.timezone.utc).astimezone()
			d1={'created':current_data,'modified':current_data,"id":last_id}
			serializer_data=dict(has_multy,**d1)

			if tax_id!="":
				serializer_data.pop("id")
				creditObj = EngageboostChannelCurrencyProductPrice.objects.using(company_db).get(id=tax_id)
				serializer = ChannelCurrencyProductPriceSerializer(creditObj,data=serializer_data,partial=True)
				if serializer.is_valid():
					serializer.save()
					# data ={
					# 'status':1,
					# 'api_status':{"id":tax_id},
					# 'message':'Successfully Updated',
					# }
					# return Response(data)
				else:
					data ={
						'msg':serializer.errors
					}
					errors.append(data)
			else:
				if product_price_type!="" and product_id!="" and warehouse_id!="":
					temp_obj = EngageboostProductPriceTypeMaster.objects.using(company_db).filter(id=product_price_type)
					if temp_obj.count()>0:
						type_obj = temp_obj.last()
						type_master = type_obj.price_type_id

						Price_Obj = EngageboostChannelCurrencyProductPrice.objects.using(company_db).filter(product_price_type_id=product_price_type,product_id=product_id,warehouse_id=warehouse_id)
						
						if type_master==2:
							Price_Obj = Price_Obj.filter(max_quantity=max_quantity,min_quantity=min_quantity)
							
							if Price_Obj.count()==0:
								serializer = ChannelCurrencyProductPriceSerializer(data=serializer_data,partial=True)
						
								if serializer.is_valid():
									serializer.save()
									obj = EngageboostChannelCurrencyProductPrice.objects.using(company_db).latest('id')
									last_id = obj.id
								else:
									data ={
										'msg':serializer.errors
									}
									# errors.append(data)
							else:
								creditObj = Price_Obj.last()
								serializer = ChannelCurrencyProductPriceSerializer(creditObj,data=serializer_data,partial=True)
									
								if serializer.is_valid():
									serializer.save()
									last_id = creditObj.id
									
								else:
									data ={
										'msg':serializer.errors
									}
									# errors.append(data)		
						else:
							if Price_Obj.count()==0:
								serializer = ChannelCurrencyProductPriceSerializer(data=serializer_data,partial=True)
							
								if serializer.is_valid():
									serializer.save()
								else:
									data ={
										'msg':serializer.errors
									}
									# errors.append(data)		
							else:
								creditObj = Price_Obj.last()
								serializer = ChannelCurrencyProductPriceSerializer(creditObj,data=serializer_data,partial=True)
								
								if serializer.is_valid():
									serializer.save()
								else:
									data ={
										'msg':serializer.errors
									}
									# errors.append(data)

					else:
						data ={
							'msg':'Invalid Product Price Type',
							'product_id':has_multy["product_price_type"],
						}
						errors.append(data)
				else:
					data ={
						'msg':'Enter required fields',
						'data':has_multy,
					}
					errors.append(data)
		
		if elastic_product_id !="":
			elastic = common.save_data_to_elastic(int(elastic_product_id),'EngageboostProducts')

		# print("Here")
		priceData = EngageboostProductPriceTypeMaster.objects.using(company_db).filter(product_id=productId)
		# print(priceData.query)
		if priceData.count()>0:
			priceResult = priceData.all()
			for pr in priceResult:
				currencyData = EngageboostChannelCurrencyProductPrice.objects.using(company_db).filter(product_price_type_id=pr.id,product_id=productId).values('warehouse_id')		
				# print(currencyData.query)
				warehouse_ids = []
				if currencyData.count()>0:
					currencyResult = currencyData.all()
					for item in currencyResult:
						warehouse_ids.append(str(item['warehouse_id']))
				# print(warehouse_ids)

				warehouseId = ",".join(warehouse_ids)
				# print(product_price_type,"==========",warehouseId)	
				EngageboostProductPriceTypeMaster.objects.using(company_db).filter(id=pr.id).update(warehouse_id=warehouseId)		
		# print(errors)
		if len(errors)>0:
			data ={
				'status':0,
				'api_status':errors,
				'message':'Something went wrong',
			}
			return Response(data)	
		else:
			data ={
				'status':1,
				'api_status':"",
				'message':'Successfully Saved',
			}
			return Response(data)

class ChannelCurrencyPriceDelete(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		has_multy = request.data
		Price_Obj = EngageboostChannelCurrencyProductPrice.objects.using(company_db)
		if 'id' in has_multy.keys() and has_multy['id']!=None and has_multy['id']!="":
			id = has_multy['id']
			Price_Obj = Price_Obj.filter(id=id)
		else:	
			if 'product_id' in has_multy.keys() and has_multy['product_id']!=None and has_multy['product_id']!="":
				product_id = has_multy['product_id']
				Price_Obj = Price_Obj.filter(product_id=product_id)

			if 'warehouse_id' in has_multy.keys() and has_multy['warehouse_id']!=None and has_multy['warehouse_id']!="":
				warehouse_id = has_multy['warehouse_id']
				Price_Obj = Price_Obj.filter(warehouse_id=warehouse_id)
				
			if 'product_price_type' in has_multy.keys() and has_multy['product_price_type']!=None and has_multy['product_price_type']!="":
				product_price_type = has_multy['product_price_type']
				Price_Obj = Price_Obj.filter(product_price_type_id=product_price_type)
		if Price_Obj.count()>0:
			Price_Obj.delete()
			data ={
				'status':1,
				'api_status':"",
				'data':has_multy,
				'message':'Data Deleted',
			}
		else:
			data ={
				'status':0,
				'api_status':"",
				'message':'No Record Found',
			}
		return Response(data)


class ImportFilePriceProducts(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		datas = []
		db_fields = []
		product_path = 'products'
		module_id = 1
		temp_model = 'TempProductsPrice'
		model = 'ProductsPrice'
		filepath = 'importfile'
		try:
			post_data = request.data
			if 'import_file' in request.FILES:
				rand = str(random.randint(1,99999))
				file1 = request.FILES['import_file']
				file_name=file1.name
				ext = file_name.split('.')[-1]
				time_stamp = str(int(datetime.datetime.now().timestamp()))
				new_file_name='ProductsPrice_'+rand+time_stamp
				fs=FileSystemStorage()
				filename = fs.save(filepath+'/'+product_path+'/'+new_file_name+'.'+ext, file1)
				uploaded_file_url = fs.url(filename)
				BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

				csvReader = xlrd.open_workbook(settings.BASE_DIR+uploaded_file_url)
				sheet = csvReader.sheet_by_index(0)
				headers = [str(cell.value) for cell in sheet.row(0)]
				headers = {k: k for k in headers}
			datas = {"filename":new_file_name+'.'+ext,"xls_header":headers,"website_id":post_data["website_id"]}
			save_price_to_table(request,datas)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			datas = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}	
		return Response(datas) 

class SaveFilePriceData(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		product_path = 'products'
		module_id = 1
		temp_model = 'TempProductsPrice'
		model = 'ProductsPrice'
		filepath = 'importfile'
		datas = []
		custom_field_datas=[]
		post_data = request.data
		# map_fields = post_data["map_fields"]
		current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
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
				error_text = []
				if x==0:
					pass
				else:
					has_record = EngageboostTempProductPrice.objects.last()
					if has_record:
						last_entry_of_table = EngageboostTempProductPrice.objects.order_by('-id').latest('id')
						row_id = int(last_entry_of_table.id)+int(1)
					else:
						row_id = 1

					serializer_data={}
					CF_serializer_data={}
					custom_field_list=[]
					d2 = {}
					d1 = {"id":row_id,"website_id":post_data['website_id'],"file_name":post_data['filename']};
					serializer_data=dict(serializer_data,**d1)
					
					for xls_column_header in xls_column_header_info:
							
						coupon_type = ""
						disc_type = ""
						column_name = str(xls_column_header["column_name"])
						column_name = column_name.strip()
						column_number = xls_column_header["column_number"]
						field_value = sheet.col_values(column_number)[x] if sheet.col_values(column_number)[x] else None

						# print(column_name,"==========",field_value)

						if column_name=="SKU":
							keyword = "sku"
						if column_name=="Warehouse Code":
							keyword = "warehouse_code"
						if column_name=="Price Type":
							keyword = "price_type"
						if column_name=="Price":
							keyword = "price"
						if column_name=="Cost":
							keyword = "cost"
						if column_name=="MRP":
							keyword = "mrp"
						if column_name=="Minimum Quantity":
							keyword = "min_quantity"
						if column_name=="Maximum Quantity":
							keyword = "max_quantity"
						if column_name=="Start Date":
							keyword = "start_date"
						if column_name=="End Date":
							keyword = "end_date"
						
						d2.update({keyword:field_value})
					
					if d2['sku']!="" and d2['sku']!=None:
						try:
							d2['sku'] = str(d2['sku'])
						except:
							pass

						try:
							d2['sku'] = d2['sku'].split('.')
							d2['sku'] = d2['sku'][0]
						except:
							pass
						try:
							d2['sku'] = d2['sku'].strip()
						except:
							pass	
								
						skuObj = EngageboostProducts.objects.using(company_db).filter(sku=d2['sku'],isdeleted='n')
						if skuObj.count()>0:
							skuData = skuObj.first()
							d2.update({"product_id":skuData.id})
						else:
							d2.update({"product_id":None})
							error_text.append("Invalid SKU")
					else:
						d2.update({"product_id":None})
						error_text.append("Enter SKU")

					if d2['warehouse_code']!="" and d2['warehouse_code']!=None:
						try:
							d2['warehouse_code'] = str(d2['warehouse_code'])
						except:
							pass
							
						try:
							d2['warehouse_code'] = d2['warehouse_code'].split('.')
							d2['warehouse_code'] = d2['warehouse_code'][0]
						except:
							pass
						try:
							d2['warehouse_code'] = d2['warehouse_code'].strip()
						except:
							pass

						skuObj = EngageboostWarehouseMasters.objects.using(company_db).filter(code=d2['warehouse_code'],isdeleted='n')
						print(skuObj.query)
						if skuObj.count()>0:
							skuData = skuObj.first()
							d2.update({"warehouse_id":skuData.id})
						else:
							d2.update({"warehouse_id":None})
							error_text.append("Invalid Warehouse Code")
					else:
						d2.update({"warehouse_id":None})
						error_text.append("Enter Warehouse Code")

					if d2['price_type']!="" and d2['price_type']!=None:
						# print("d2['price_type']============",d2['price_type'])
						if d2['price_type']=="Regular" or d2['price_type']=="Quantity":
							prc_type_id = 1 if d2['price_type']=="Regular" else 2

							prcObj = EngageboostProductPriceTypeMaster.objects.using(company_db).filter(product_id=d2["product_id"],website_id=post_data["website_id"],price_type_id=prc_type_id)
							# prcObj = prcObj.filter(Q(warehouse_id=d2["warehouse_id"])|
							# 						Q(warehouse_id__istartswith=str(d2["warehouse_id"])+",")|
							# 						Q(warehouse_id__iendswith=","+str(d2["warehouse_id"]))|
							# 						Q(warehouse_id__icontains=","+str(d2["warehouse_id"])+",")
							# 						)
							
							if prcObj.count()==0:
								price_data = {
									"name" : d2['price_type'],
									"product_id" : d2["product_id"],
									"website_id" : post_data["website_id"],
									"warehouse_id": d2["warehouse_id"],
									"price_type_id": 1 if d2['price_type']=="Regular" else 2,
									"min_quantity": d2["min_quantity"] if d2['price_type']=="Quantity" else 0,
									"max_quantity": d2["max_quantity"] if d2['price_type']=="Quantity" else 0,
									"created": current_time,
									"modified": current_time
								}
								priceLatest = EngageboostProductPriceTypeMaster.objects.using(company_db).create(**price_data)

								d2['product_price_type_id'] = priceLatest.id
							else:
								priceLatest = prcObj.order_by("id").first()
								latestWarehouse_id = priceLatest.warehouse_id
								if latestWarehouse_id!="" and latestWarehouse_id!=None:
									latestWarehouse_id = latestWarehouse_id.split(',')
									if str(d2["warehouse_id"]) not in latestWarehouse_id:
										latestWarehouse_id.append(str(d2["warehouse_id"]))
									# print("Here============",latestWarehouse_id)
									latestWarehouse_id = ",".join(latestWarehouse_id)
								else:
									latestWarehouse_id = d2["warehouse_id"]

								d2['product_price_type_id'] = priceLatest.id
								EngageboostProductPriceTypeMaster.objects.using(company_db).filter(id=priceLatest.id).update(warehouse_id=latestWarehouse_id)	
						else:
							error_text.append("Invalid Price Type")
					else:
						error_text.append("Enter Price Type")

					if d2['price']=="" or d2['price']==None:
						error_text.append("Enter Price")
					else:
						if d2['mrp']=="" or d2['mrp']==None:
							d2['mrp'] = d2['price']	
					
					if d2['price_type']!="" and d2['price_type']!=None:
						if d2['price_type']=="Quantity" and (d2['min_quantity']=="" or d2['min_quantity']==None):		
							error_text.append("Enter minimum quantity")
						if d2['price_type']=="Quantity" and (d2['max_quantity']=="" or d2['max_quantity']==None):		
							error_text.append("Enter maximum quantity")	
					

					if d2['start_date']!="" and d2['start_date']!=None:
						try:
							workbook_datemode = csvReader.datemode
							y, M, d, h, m, s = xlrd.xldate_as_tuple(d2['start_date'], workbook_datemode)
							d2['start_date'] = ("{0}-{1}-{2}".format(y, M, d, h, m, s))
						except:
							pass

						start_date = common.format_date(d2['start_date'])
						d2['start_date'] = start_date
					
					else:
						d2['start_date'] = datetime.datetime.now()
						# try:
						# 	workbook_datemode = csvReader.datemode
						# 	y, M, d, h, m, s = xlrd.xldate_as_tuple(d2['start_date'], workbook_datemode)
						# 	d2['start_date'] = ("{0}-{1}-{2}".format(y, M, d, h, m, s))
						# except:
						# 	pass

						# start_date = common.format_date(d2['start_date'])
						# d2['start_date'] = start_date

					if d2['end_date']!="" and d2['end_date']!=None:
						try:
							workbook_datemode = csvReader.datemode
							y, M, d, h, m, s = xlrd.xldate_as_tuple(d2['end_date'], workbook_datemode)
							d2['end_date'] = ("{0}-{1}-{2}".format(y, M, d, h, m, s))
						except:
							pass	 

						end_date = common.format_date(d2['end_date'])
						d2['end_date'] = end_date
					
					d2['channel_id'] = 6

					gbl_settings = EngageboostGlobalSettings.objects.get(website_id=post_data["website_id"])
					if gbl_settings:
						gblCurrency = EngageboostGlobalsettingCurrencies.objects.filter(global_setting_id = gbl_settings.id)
						if gblCurrency.count()>0:
							gblCurrency = gblCurrency.first()
							d2['currency_id'] = gblCurrency.currency_id
					if len(error_text)>0:
						d2['err_flag'] = 1
						d2["error_text"] = ",".join(error_text)	
					else:
						d2['err_flag'] = 0	
						d2["error_text"] = "SUCCESS"	
					serializer_data=dict(serializer_data,**d2)

					d1={"created":current_time,"modified":current_time};
				
					serializer_data=dict(serializer_data,**d1)
					print("Data=======",serializer_data)
					common.update_db_sequences("temp_product_price")
					save_temp_product = EngageboostTempProductPrice.objects.using(company_db).create(**serializer_data)
					data_status = {"status":1,"filename":post_data["filename"]}			
			
			os.remove(settings.BASE_DIR+uploaded_file_url)
		else:
			data_status = {"status":0,"filename":post_data["filename"],'errors':"File Not Exists" }
		return Response(data_status)	

class PreviewSaveFilePrice(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		post_data = request.data
		fetch_all_data = []
		data = {}
		try:
			fetch_all_data_cond = EngageboostTempProductPrice.objects.using(company_db).all().filter(website_id=post_data['website_id'],file_name=post_data['filename']) #fetch from temp product table
			if fetch_all_data_cond:
				fetch_all_datas = TempProductPriceSerializer(fetch_all_data_cond,many=True)
				# fetch_all_data = fetch_all_datas.data
				fetch_all_data = fetch_all_datas.data
			data = {"preview_data":fetch_all_data,"filename":post_data['filename']}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}	
		return Response(data)

class SaveAllImportedPrice(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		datas = []
		db_fields = []
		product_path = 'products'
		module_id = 1
		temp_model = 'TempProductsPrice'
		model = 'ProductsPrice'
		filepath = 'importfile'
		fetch_temp_datas = []
		try:
			post_data = request.data
			selectedIds = post_data["selected_ids"].split(',')

			# for i in selectedIds:
			# 	fetch_temp_data_cond = EngageboostTempProductPrice.objects.using(company_db).filter(id=int(i),err_flag=0).first()
			# 	if fetch_temp_data_cond:
			# 		fetch_temp_data = TempProductPriceSerializer(fetch_temp_data_cond,partial=True)
			# 		fetch_temp_datas.append(fetch_temp_data.data)

			fetch_temp_data_cond = EngageboostTempProductPrice.objects.using(company_db).filter(id__in=selectedIds,err_flag=0)		
			if fetch_temp_data_cond.count():
				fetch_temp_data_cond = fetch_temp_data_cond.all().iterator()
				fetch_temp_datas = TempProductPriceSerializer(fetch_temp_data_cond,many=True)
				fetch_temp_datas = fetch_temp_datas.data
			
				if len(fetch_temp_datas)>0:
					for fetchtempdatas in fetch_temp_datas:
						fetchtempdatas['product']=fetchtempdatas['product_id']
						serializer_data = {}
						serializer_data = dict(serializer_data,**fetchtempdatas)
						# print("Price_data===================",serializer_data)
						Price_Obj = EngageboostChannelCurrencyProductPrice.objects.using(company_db).filter(product_price_type_id=serializer_data['product_price_type'],product_id=serializer_data['product_id'],warehouse_id=serializer_data['warehouse_id'])
						current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
						
						# print(Price_Obj.query,Price_Obj.count())

						if Price_Obj.count()==0:
							d1 = {"created":current_time,"modified":current_time}
							serializer_data = dict(serializer_data,**d1)
							datas.append(serializer_data)
							serializer = ChannelCurrencyProductPriceImportSerializer(data=serializer_data,partial=True)
						else:
							d1 = {"modified":current_time}
							serializer_data = dict(serializer_data,**d1)
							datas.append(serializer_data)

							creditObj = Price_Obj.last()
							serializer = ChannelCurrencyProductPriceImportSerializer(creditObj,data=serializer_data,partial=True)
						
						print(serializer_data)
						
						if serializer.is_valid():
							serializer.save()
							# print("Price_data===================",serializer.data)
							#####################Update Product price in Elastic#########################
							try:
								product_id = serializer.data['product_id']
							except:
								product_id = serializer.data['product']	
							price_data = common.get_channel_currency_product_price(product_id)

							common.change_field_value_elastic(product_id,'EngageboostProducts',{"channel_currency_product_price":price_data})
							#####################Update Product price in Elastic#########################
							EngageboostTempProductPrice.objects.using(company_db).filter(id=fetchtempdatas['id']).delete()
							responseDatas = {"status":1,"api_response":datas,"message":'Price Saved'}
						else:
							data ={'status':0,'api_status':serializer.errors,'message':'Error Occured'}
							datas.append(data)

							responseDatas = {"status":0,"api_response":datas,"message":'Error Occured in Price'}

				else:
					responseDatas = {"status":0,"api_response":"","message":'Price Not Saved'}
			else:
				responseDatas = {"status":0,"api_response":"","message":'Price Not Saved'}	
			# EngageboostTempProductPrice.objects.using(company_db).filter(file_name=post_data['filename']).delete()
			return Response(responseDatas)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			datas = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
			return Response(datas)		

@postpone
def save_price_to_table(request,req_data):
	company_db = loginview.db_active_connection(request)
	product_path = 'products'
	module_id = 1
	temp_model = 'TempProductsPrice'
	model = 'ProductsPrice'
	filepath = 'importfile'
	datas = []
	custom_field_datas=[]
	post_data = req_data
	# map_fields = post_data["map_fields"]
	current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
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
		cnt = 0
		for x in range(length):
			error_text = []
			if x==0:
				pass
			else:
				has_record = EngageboostTempProductPrice.objects.last()
				if has_record:
					last_entry_of_table = EngageboostTempProductPrice.objects.order_by('-id').latest('id')
					row_id = int(last_entry_of_table.id)+int(1)
				else:
					row_id = 1

				serializer_data={}
				CF_serializer_data={}
				custom_field_list=[]
				d2 = {}
				d1 = {"id":row_id,"website_id":post_data['website_id'],"file_name":post_data['filename']};
				serializer_data=dict(serializer_data,**d1)
				
				for xls_column_header in xls_column_header_info:
						
					coupon_type = ""
					disc_type = ""
					column_name = str(xls_column_header["column_name"])
					column_name = column_name.strip()
					column_number = xls_column_header["column_number"]
					field_value = sheet.col_values(column_number)[x] if sheet.col_values(column_number)[x] else None

					# print(column_name,"==========",field_value)

					if column_name=="SKU":
						keyword = "sku"
					if column_name=="Warehouse Code":
						keyword = "warehouse_code"
					if column_name=="Price Type":
						keyword = "price_type"
					if column_name=="Price":
						keyword = "price"
					if column_name=="Cost":
						keyword = "cost"
					if column_name=="MRP":
						keyword = "mrp"
					if column_name=="Minimum Quantity":
						keyword = "min_quantity"
					if column_name=="Maximum Quantity":
						keyword = "max_quantity"
					if column_name=="Start Date":
						keyword = "start_date"
					if column_name=="End Date":
						keyword = "end_date"
					
					d2.update({keyword:field_value})
				
				if d2['sku']!="" and d2['sku']!=None:
					try:
						# d2['sku'] = str(int(d2['sku']))
						d2['sku'] = str(d2['sku'])
					except:
						d2['sku'] = str(d2['sku'])

					try:
						d2['sku'] = d2['sku'].split('.')
						d2['sku'] = d2['sku'][0]
					except:
						pass
					try:
						d2['sku'] = d2['sku'].strip()
					except:
						pass
						
					print(d2['sku'])		
					skuObj = EngageboostProducts.objects.using(company_db).filter(sku=d2['sku'],isdeleted='n')
					if skuObj.count()>0:
						skuData = skuObj.first()
						d2.update({"product_id":skuData.id})
					else:
						d2.update({"product_id":None})
						error_text.append("Invalid SKU")
				else:
					d2.update({"product_id":None})
					error_text.append("Enter SKU")

				if d2['warehouse_code']!="" and d2['warehouse_code']!=None:
					try:
						d2['warehouse_code'] = str(d2['warehouse_code'])
					except:
						pass
						
					try:
						d2['warehouse_code'] = d2['warehouse_code'].split('.')
						d2['warehouse_code'] = d2['warehouse_code'][0]
					except:
						pass
					try:
						d2['warehouse_code'] = d2['warehouse_code'].strip()
					except:
						pass
					skuObj = EngageboostWarehouseMasters.objects.using(company_db).filter(code=d2['warehouse_code'],isdeleted='n')
					# print(skuObj.query)
					if skuObj.count()>0:
						skuData = skuObj.first()
						d2.update({"warehouse_id":skuData.id})
					else:
						d2.update({"warehouse_id":None})
						error_text.append("Invalid Warehouse Code")
				else:
					d2.update({"warehouse_id":None})
					error_text.append("Enter Warehouse Code")

				if d2['price_type']!="" and d2['price_type']!=None:
					# print("d2['price_type']============",d2['price_type'])
					if d2['price_type']=="Regular" or d2['price_type']=="Quantity":
						prc_type_id = 1 if d2['price_type']=="Regular" else 2
						price_type_masterObj = EngageboostPriceTypeMaster.objects.filter(id=prc_type_id).first()
												
						prcObj = EngageboostProductPriceTypeMaster.objects.using(company_db).filter(product_id=d2["product_id"],website_id=post_data["website_id"],price_type_id=prc_type_id)
						# prcObj = prcObj.filter(Q(warehouse_id=d2["warehouse_id"])|
						# 						Q(warehouse_id__istartswith=str(d2["warehouse_id"])+",")|
						# 						Q(warehouse_id__iendswith=","+str(d2["warehouse_id"]))|
						# 						Q(warehouse_id__icontains=","+str(d2["warehouse_id"])+",")
						# 						)
						
						if prcObj.count()==0:
							price_data = {
								"name" : price_type_masterObj.name,
								"product_id" : d2["product_id"],
								"website_id" : post_data["website_id"],
								"warehouse_id": d2["warehouse_id"],
								"price_type_id": 1 if d2['price_type']=="Regular" else 2,
								"min_quantity": d2["min_quantity"] if d2['price_type']=="Quantity" else 0,
								"max_quantity": d2["max_quantity"] if d2['price_type']=="Quantity" else 0,
								"created": current_time,
								"modified": current_time
							}
							priceLatest = EngageboostProductPriceTypeMaster.objects.using(company_db).create(**price_data)

							d2['product_price_type_id'] = priceLatest.id
						else:
							priceLatest = prcObj.order_by("id").first()
							latestWarehouse_id = priceLatest.warehouse_id
							if latestWarehouse_id!="" and latestWarehouse_id!=None:
								latestWarehouse_id = latestWarehouse_id.split(',')
								if str(d2["warehouse_id"]) not in latestWarehouse_id:
									latestWarehouse_id.append(str(d2["warehouse_id"]))
								# print("Here============",latestWarehouse_id)
								latestWarehouse_id = ",".join(latestWarehouse_id)
							else:
								latestWarehouse_id = d2["warehouse_id"]

							d2['product_price_type_id'] = priceLatest.id
							EngageboostProductPriceTypeMaster.objects.using(company_db).filter(id=priceLatest.id).update(warehouse_id=latestWarehouse_id)	
					else:
						error_text.append("Invalid Price Type")
				else:
					error_text.append("Enter Price Type")

				if d2['price']=="" or d2['price']==None:
					error_text.append("Enter Price")
				else:
					if d2['mrp']=="" or d2['mrp']==None:
						d2['mrp'] = d2['price']	
				
				# if d2['cost']=="" or d2['cost']==None:
				# 	d2['cost'] = 0		

				if d2['price_type']!="" and d2['price_type']!=None:
					if d2['price_type']=="Quantity" and (d2['min_quantity']=="" or d2['min_quantity']==None):		
						error_text.append("Enter minimum quantity")
					if d2['price_type']=="Quantity" and (d2['max_quantity']=="" or d2['max_quantity']==None):		
						error_text.append("Enter maximum quantity")	
				

				if d2['start_date']!="" and d2['start_date']!=None:
					try:
						workbook_datemode = csvReader.datemode
						y, M, d, h, m, s = xlrd.xldate_as_tuple(d2['start_date'], workbook_datemode)
						d2['start_date'] = ("{0}-{1}-{2}".format(y, M, d, h, m, s))
					except:
						pass

					start_date = common.format_date(d2['start_date'])
					d2['start_date'] = start_date
				
				else:
					d2['start_date'] = current_time
					# try:
					# 	workbook_datemode = csvReader.datemode
					# 	y, M, d, h, m, s = xlrd.xldate_as_tuple(d2['start_date'], workbook_datemode)
					# 	d2['start_date'] = ("{0}-{1}-{2}".format(y, M, d, h, m, s))
					# except:
					# 	pass

					# start_date = common.format_date(d2['start_date'])
					# d2['start_date'] = start_date

				if d2['end_date']!="" and d2['end_date']!=None:
					try:
						workbook_datemode = csvReader.datemode
						y, M, d, h, m, s = xlrd.xldate_as_tuple(d2['end_date'], workbook_datemode)
						d2['end_date'] = ("{0}-{1}-{2}".format(y, M, d, h, m, s))
					except:
						pass	 

					end_date = common.format_date(d2['end_date'])
					d2['end_date'] = end_date
				else:	
					d2['end_date'] = None	
				
				d2['channel_id'] = 6

				try:
					gbl_settings = EngageboostGlobalSettings.objects.filter(website_id=post_data["website_id"])
					if gbl_settings.count()>0:
						gbl_settings = gbl_settings.first()
						gblCurrency = EngageboostGlobalsettingCurrencies.objects.filter(global_setting_id = gbl_settings.id)
						if gblCurrency.count()>0:
							gblCurrency = gblCurrency.first()
							d2['currency_id'] = gblCurrency.currency_id
						else:
							d2['currency_id'] = None
					else:
						d2['currency_id'] = None
				except:
					d2['currency_id'] = None			
				print(cnt,"======Data=======",",".join(error_text))
				if len(error_text)>0:
					d2['err_flag'] = 1
					d2["error_text"] = ",".join(error_text)

					serializer_data=dict(serializer_data,**d2)

					d1={"created":current_time,"modified":current_time};
				
					serializer_data=dict(serializer_data,**d1)
					# print("Data=======",serializer_data)
					common.update_db_sequences("temp_product_price")
					save_temp_product = EngageboostTempProductPrice.objects.using(company_db).create(**serializer_data)
				else:
					cnt = cnt+1
					d2['err_flag'] = 0	
					d2["error_text"] = None	
					serializer_data=dict(serializer_data,**d2)

					d1={"created":current_time,"modified":current_time};
				
					serializer_data=dict(serializer_data,**d1)

					common.update_db_sequences("temp_product_price")
					save_temp_product = EngageboostTempProductPrice.objects.using(company_db).create(**serializer_data)
					# updated_price = {
					# 	"channel_id" : serializer_data["channel_id"],
					# 	"currency_id" : serializer_data["currency_id"],
					# 	"product_id" : serializer_data["product_id"],
					# 	"price" : serializer_data["price"], 
					# 	"mrp" : serializer_data["mrp"],
					# 	"min_quantity" : serializer_data["min_quantity"],
					# 	"max_quantity" : serializer_data["max_quantity"],
					# 	"warehouse_id" : serializer_data["warehouse_id"],
					# 	"website_id" : serializer_data["website_id"],
					# 	"start_date" : serializer_data["start_date"],
					# 	"end_date" : serializer_data["end_date"],
					# 	"product_price_type_id" : serializer_data["product_price_type_id"]
					# }

					# print(cnt,"======Data=======",updated_price)
					# common.update_db_sequences("channel_currency_product_price")

					# Price_Obj = EngageboostChannelCurrencyProductPrice.objects.filter(product_price_type_id=serializer_data["product_price_type_id"],product_id=serializer_data["product_id"],warehouse_id=serializer_data["warehouse_id"])
					# if Price_Obj.count()>0:
					# 	Price_Obj.update(**updated_price)
					# else:	
					# 	save_product_price = EngageboostChannelCurrencyProductPrice.objects.create(**updated_price)

					# price_data = common.get_channel_currency_product_price(serializer_data["product_id"])
					# common.change_field_value_elastic(serializer_data["product_id"],'EngageboostProducts',{"channel_currency_product_price":price_data})	
				
				data_status = {"status":1,"filename":post_data["filename"]}			
		
		os.remove(settings.BASE_DIR+uploaded_file_url)
	else:
		data_status = {"status":0,"filename":post_data["filename"],'errors':"File Not Exists" }
	return Response(data_status)	

# @postpone
def save_price_from_temp_to_table_old():
	obj = EngageboostTempProductPrice.objects.filter(website_id=1).filter(err_flag=0,error_text=None)
	objcount = obj.count()
	# objcount = 0
	if objcount>0:
		product_ids = obj.values_list('product_id',flat=True).order_by("id")[0:500]
		product_ids = list(set(product_ids))
		for item_id in product_ids:
			try:
				tempDataId = []
				TempProductPriceObj = EngageboostTempProductPrice.objects.filter(website_id=1,product_id=item_id).filter(err_flag=0,error_text=None)
				
				TempProductPrice = TempProductPriceSerializer(TempProductPriceObj,many=True)
				for serializer_data in TempProductPrice.data:
					try:
						print(serializer_data)
					
						updated_price = {
							"channel_id" : serializer_data["channel_id"],
							"currency_id" : serializer_data["currency_id"],
							"product_id" : serializer_data["product_id"],
							"price" : serializer_data["price"], 
							# "cost" : serializer_data["cost"],
							"mrp" : serializer_data["mrp"],
							"min_quantity" : serializer_data["min_quantity"],
							"max_quantity" : serializer_data["max_quantity"],
							"warehouse_id" : serializer_data["warehouse_id"],
							"website_id" : serializer_data["website_id"],
							"start_date" : serializer_data["start_date"],
							"end_date" : serializer_data["end_date"],
							"product_price_type_id" : serializer_data["product_price_type"]
						}

						print("======Data=======",updated_price)
						common.update_db_sequences("channel_currency_product_price")

						Price_Obj = EngageboostChannelCurrencyProductPrice.objects.filter(product_price_type_id=serializer_data["product_price_type"],product_id=serializer_data["product_id"],warehouse_id=serializer_data["warehouse_id"])
						if Price_Obj.count()>0:
							Price_Obj.update(**updated_price)
						else:	
							save_product_price = EngageboostChannelCurrencyProductPrice.objects.create(**updated_price)

						tempDataId.append(serializer_data["id"])
					except:
						pass
				price_data = common.get_channel_currency_product_price(item_id)
				common.change_field_value_elastic(item_id,'EngageboostProducts',{"channel_currency_product_price":price_data})
				EngageboostTempProductPrice.objects.filter(id__in=tempDataId).update(error_text="SUCCESS")
			except Exception as error :
				trace_back = sys.exc_info()[2]
				line = trace_back.tb_lineno
				data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
				EngageboostTempProductPrice.objects.filter(id__in=tempDataId).update(error_text=str(error),err_flag=1)
				print("Local temp Price issue found ==========",data)
	print("Deleting temp price...................")

def save_price_from_temp_to_table_old_2():
	print('=============in  save_price_from_temp_to_table  =============')
	response = emailcomponent.testmail('binayak.santra@navsoft.in',
									   "Data Preparation Start @@@SavePriceFromTempToTableLive@@@",
									   'Data preparation Initiated ' + str(
										   datetime.datetime.now()))
	es = common.connect_elastic()
	obj = EngageboostTempProductPrice.objects.filter(website_id=1).filter(err_flag=0, error_text=None)
	objcount = obj.count()
	# objcount = 0
	datas = []
	docs = []
	tempDataId = []
	table_name = 'EngageboostProducts'

	model = apps.get_model('webservices', table_name)
	prod_obj = model.objects.filter(isdeleted='n')

	try:
		if objcount > 0:
			# ------Binayak Start 29-01-2021----#
			product_ids = obj.values_list('product_id', flat=True).order_by("id")[0:500]

			if len(product_ids) > 0:
				prod_obj = prod_obj.filter(id__in=product_ids)

			if prod_obj.count() > 0:
				products = prod_obj.order_by("-id").all().iterator()

			module_name = common.get_index_name_elastic(product_ids[0], table_name)
			serializer_class = common.get_serializer_class_elastic(table_name)
			# data_string = {
			# 	"ids": list(product_ids)
			# }
			data_string = []
			for id in product_ids:
				id_string = {
					"_id": id,
					"_source": False
				}
				data_string.append(id_string)
			# print(data_string)
			# prod_exists = es.mget(body=data_string, index=module_name, doc_type="data")
			prod_exists = es.mget(body=json.dumps({"docs": data_string}), index=module_name, doc_type="data")

			# ------Binayak End 29-01-2021----#
			for item in prod_exists['docs']:
				cm_id = item['_id']
				if item['found'] == True:
					TempProductPriceObj = EngageboostTempProductPrice.objects.filter(website_id=1,
																					 product_id=cm_id).filter(
						err_flag=0, error_text=None)

					TempProductPrice = TempProductPriceSerializer(TempProductPriceObj, many=True)
					for serializer_data in TempProductPrice.data:
						# print(serializer_data)

						updated_price = {
							"channel_id": serializer_data["channel_id"],
							"currency_id": serializer_data["currency_id"],
							"product_id": serializer_data["product_id"],
							"price": serializer_data["price"],
							# "cost" : serializer_data["cost"],
							"mrp": serializer_data["mrp"],
							"min_quantity": serializer_data["min_quantity"],
							"max_quantity": serializer_data["max_quantity"],
							"warehouse_id": serializer_data["warehouse_id"],
							"website_id": serializer_data["website_id"],
							"start_date": serializer_data["start_date"],
							"end_date": serializer_data["end_date"],
							"product_price_type_id": serializer_data["product_price_type"]
						}

						# -----Binayak Start 29-01-2021-----#
						# updated_commission = {
						# 	"product_id": serializer_data["product_id"],
						# 	"warehouse_id": serializer_data["warehouse_id"],
						# 	"commission_percentage": serializer_data["commission"]
						# }
						# -----Binayak End 29-01-2021-----#

						# print("======Data=======", updated_price)
						common.update_db_sequences("channel_currency_product_price")

						Price_Obj = EngageboostChannelCurrencyProductPrice.objects.filter(
							product_price_type_id=serializer_data["product_price_type"],
							product_id=serializer_data["product_id"],
							warehouse_id=serializer_data["warehouse_id"])

						# -----Binayak Start 29-01-2021-----#
						# Stock_Obj = EngageboostProductStocks.objects.filter(product_id=serializer_data["product_id"],
						# 													warehouse_id=serializer_data[
						# 														"warehouse_id"])
						# -----Binayak End 29-01-2021-----#

						if Price_Obj.count() > 0:
							Price_Obj.update(**updated_price)
						else:
							save_product_price = EngageboostChannelCurrencyProductPrice.objects.create(**updated_price)

						# -----Binayak Start 29-01-2021-----#
						# if Stock_Obj.count() > 0:
						# 	Stock_Obj.update(**updated_commission)
						# else:
						# 	save_product_stock = EngageboostProductStocks.objects.create(**updated_price)
						# -----Binayak End 29-01-2021-----#

						tempDataId.append(serializer_data["id"])
					# ==========================================
					price_data = common.get_channel_currency_product_price(cm_id)
					data = {"channel_currency_product_price": price_data}

					# data = get_product_field_value_for_elastic(cm_id, field_name)

					header = {
						"_op_type": 'update',
						"_index": module_name,
						"_type": "data",
						"_id": cm_id,
						"doc": data
					}
				# print("======update header=======", header)
				else:
					now_item = prod_obj.filter(id=cm_id).first()
					# serializer_class = get_serializer_class_elastic(table_name)
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
				# print("======add header=======", header)
				docs.append(header)

			response = emailcomponent.testmail('binayak.santra@navsoft.in',
											   "Data Preparation Completed @@@SavePriceFromTempToTableLive@@@",
											   'Data preparation Completed ' + str(
												   datetime.datetime.now()))

			datas.append({"msg": "Success"})
	except Exception as error:
		trace_back = sys.exc_info()[2]
		line = trace_back.tb_lineno
		datas.append({"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),
				 "message": str(error)})
		EngageboostTempProductPrice.objects.filter(id=serializer_data['id']).update(error_text=str(error), err_flag=1)

	finally:
		print('=======in finally save_price_from_temp_to_table ========')
		obj = helpers.bulk(es, docs)
		EngageboostTempProductPrice.objects.filter(id__in=tempDataId).update(error_text="SUCCESS")
		datas.append({"obj": obj})
		response = emailcomponent.testmail('binayak.santra@navsoft.in',
										   "Data Pushed to Elastic @@@SavePriceFromTempToTableLive@@@",
										   'Data preparation Completed and Pushed to Elastic, PRODUCT_COUNT =====>' + str(
											   len(tempDataId)) + ' @ ' + str(
											   datetime.datetime.now()) + ' datas=====>' + str(datas))

	print("Deleting temp price...................")

def save_price_from_temp_to_table():
	print('=============in  save_price_from_temp_to_table  =============')
	response = emailcomponent.testmail('binayak.santra@navsoft.in',
									   "Data Preparation Start @@@SavePriceFromTempToTableLive@@@",
									   'Data preparation Initiated ' + str(
										   datetime.datetime.now()))

	response = emailcomponent.testmail('lifco.onboard@gmail.com',
									   "Data Preparation Start @@@SavePriceFromTempToTableLive@@@",
									   'Data preparation Initiated ' + str(
										   datetime.datetime.now()))
	es = common.connect_elastic()
	obj = EngageboostTempProductPrice.objects.filter(website_id=1).filter(err_flag=0, error_text=None)
	objcount = obj.count()
	# objcount = 0
	datas = []
	docs = []
	tempDataId = []
	table_name = 'EngageboostProducts'

	model = apps.get_model('webservices', table_name)
	prod_obj = model.objects.filter(isdeleted='n')

	try:
		if objcount > 0:
			# ------Binayak Start 29-01-2021----#
			product_ids = obj.values_list('product_id', flat=True).order_by("id")[0:500]

			if len(product_ids) > 0:
				prod_obj = prod_obj.filter(id__in=product_ids)

			if prod_obj.count() > 0:
				products = prod_obj.order_by("-id").all().iterator()

			module_name = common.get_index_name_elastic(product_ids[0], table_name)
			serializer_class = common.get_serializer_class_elastic(table_name)
			# data_string = {
			# 	"ids": list(product_ids)
			# }
			data_string = []
			for id in product_ids:
				id_string = {
					"_id": id,
					"_source": {
				       "include": [ "channel_currency_product_price" ]
				    }
				}
				data_string.append(id_string)
			# print(data_string)
			# prod_exists = es.mget(body=data_string, index=module_name, doc_type="data")
			prod_exists = es.mget(body=json.dumps({"docs": data_string}), index=module_name, doc_type="data")

			# ------Binayak End 29-01-2021----#
			for item in prod_exists['docs']:
				cm_id = item['_id']
				if item['found'] == True:
					TempProductPriceObj = EngageboostTempProductPrice.objects.filter(website_id=1,
																					 product_id=cm_id).filter(
						err_flag=0, error_text=None)

					# warehouse_id = None
					warehouse_id = []
					flag = 0

					TempProductPrice = TempProductPriceSerializer(TempProductPriceObj, many=True)
					for serializer_data in TempProductPrice.data:
						# print(serializer_data)

						# warehouse_id = serializer_data["warehouse_id"]
						warehouse_id.append(serializer_data["warehouse_id"])

						updated_price = {
							"channel_id": serializer_data["channel_id"],
							"currency_id": serializer_data["currency_id"],
							"product_id": serializer_data["product_id"],
							"price": serializer_data["price"],
							# "cost" : serializer_data["cost"],
							"mrp": serializer_data["mrp"],
							"min_quantity": serializer_data["min_quantity"],
							"max_quantity": serializer_data["max_quantity"],
							"warehouse_id": serializer_data["warehouse_id"],
							"website_id": serializer_data["website_id"],
							"start_date": serializer_data["start_date"],
							"end_date": serializer_data["end_date"],
							"product_price_type_id": serializer_data["product_price_type"]
						}

						# -----Binayak Start 29-01-2021-----#
						# updated_commission = {
						# 	"product_id": serializer_data["product_id"],
						# 	"warehouse_id": serializer_data["warehouse_id"],
						# 	"commission_percentage": serializer_data["commission"]
						# }
						# -----Binayak End 29-01-2021-----#

						# print("======Data=======", updated_price)
						common.update_db_sequences("channel_currency_product_price")

						Price_Obj = EngageboostChannelCurrencyProductPrice.objects.filter(
							product_price_type_id=serializer_data["product_price_type"],
							product_id=serializer_data["product_id"],
							warehouse_id=serializer_data["warehouse_id"])

						# -----Binayak Start 29-01-2021-----#
						# Stock_Obj = EngageboostProductStocks.objects.filter(product_id=serializer_data["product_id"],
						# 													warehouse_id=serializer_data[
						# 														"warehouse_id"])
						# -----Binayak End 29-01-2021-----#

						if Price_Obj.count() > 0:
							Price_Obj.update(**updated_price)
						else:
							save_product_price = EngageboostChannelCurrencyProductPrice.objects.create(**updated_price)

						# -----Binayak Start 29-01-2021-----#
						# if Stock_Obj.count() > 0:
						# 	Stock_Obj.update(**updated_commission)
						# else:
						# 	save_product_stock = EngageboostProductStocks.objects.create(**updated_price)
						# -----Binayak End 29-01-2021-----#

						tempDataId.append(serializer_data["id"])
					# ==========================================
					if len(warehouse_id) > 0:
						price_data = item['_source']['channel_currency_product_price']
						warehouse_list = warehouse_id.copy()
						modified_price_data = common.multiple_warehouse_channel_currency_price_update_string(cm_id,
																											 price_data,
																											 warehouse_list)
						data = {"channel_currency_product_price": modified_price_data}
						# print("=====price_Data=====", price_data)
						# ========process elastic price========#
						# for channel_currency_product_price in price_data:
						# 	# print("======channel_currency_product_price======warehouse_id======",
						# 	# 	  channel_currency_product_price['warehouse_id'])
						# 	if channel_currency_product_price['warehouse_id'] == warehouse_id:
						# 		price_data_single = common.get_channel_currency_product_price(cm_id, 1, [warehouse_id])
						#
						# 		for data in price_data_single:
						# 			channel_currency_product_price['id'] = data['id']
						# 			channel_currency_product_price['promotions'] = data['promotions']
						# 			channel_currency_product_price['price_type'] = data['price_type']
						# 			channel_currency_product_price['channel_id'] = data['channel_id']
						# 			channel_currency_product_price['currency_id'] = data['currency_id']
						# 			channel_currency_product_price['price'] = data['price']
						# 			channel_currency_product_price['cost'] = data['cost']
						# 			channel_currency_product_price['mrp'] = data['mrp']
						# 			channel_currency_product_price['min_quantity'] = data['min_quantity']
						# 			channel_currency_product_price['max_quantity'] = data['max_quantity']
						# 			channel_currency_product_price['warehouse_id'] = data['warehouse_id']
						# 			channel_currency_product_price['website_id'] = data['website_id']
						# 			channel_currency_product_price['start_date'] = data['start_date']
						# 			channel_currency_product_price['end_date'] = data['end_date']
						# 			channel_currency_product_price['product'] = data['product']
						# 			channel_currency_product_price['product_price_type'] = data['product_price_type']
						# 			channel_currency_product_price['new_default_price'] = data['new_default_price']
						# 			channel_currency_product_price['new_default_price_unit'] = data[
						# 				'new_default_price_unit']
						# 			channel_currency_product_price['discount_price_unit'] = data['discount_price_unit']
						# 			channel_currency_product_price['discount_price'] = data['discount_price']
						# 			channel_currency_product_price['discount_amount'] = data['discount_amount']
						# 			channel_currency_product_price['disc_type'] = data['disc_type']
						# 			channel_currency_product_price['coupon'] = data['coupon']
						#
						# 		flag = 1
						#
						# if flag == 0:
						# 	# print("I am here")
						# 	price_data_single = common.get_channel_currency_product_price(cm_id, 1, [warehouse_id])
						# 	# price_data_single = json.dumps(price_data_single)
						# 	# price_data_single = json.loads(price_data_single)
						# 	# print("======price_data_single======", price_data_single[0])
						# 	# price_data = common.get_channel_currency_product_price(cm_id)
						# 	price_data.append(price_data_single[0])
						# else:
						# 	price_data = item['_source']['channel_currency_product_price']

						# print("======price_data=======", price_data)
						# price_data = common.get_channel_currency_product_price(cm_id)
						# data = {"channel_currency_product_price": price_data}

						# data = get_product_field_value_for_elastic(cm_id, field_name)

						header = {
							"_op_type": 'update',
							"_index": module_name,
							"_type": "data",
							"_id": cm_id,
							"doc": data
						}
						docs.append(header)
				# print("======update header=======", header)
				else:
					now_item = prod_obj.filter(id=cm_id).first()
					# serializer_class = get_serializer_class_elastic(table_name)
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
				# print("======add header=======", header)
				docs.append(header)

			# response = emailcomponent.testmail('binayak.santra@navsoft.in',
			# 								   "Data Preparation Completed @@@SavePriceFromTempToTableLive@@@",
			# 								   'Data preparation Completed ' + str(
			# 									   datetime.datetime.now()))

			datas.append({"msg": "Success"})
	except Exception as error:
		trace_back = sys.exc_info()[2]
		line = trace_back.tb_lineno
		datas.append({"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),
				 "message": str(error)})
		EngageboostTempProductPrice.objects.filter(id=serializer_data['id']).update(error_text=str(error), err_flag=1)

	finally:
		print('=======in finally save_price_from_temp_to_table ========')
		obj = helpers.bulk(es, docs)
		EngageboostTempProductPrice.objects.filter(id__in=tempDataId).update(error_text="SUCCESS")
		datas.append({"obj": obj})
		response = emailcomponent.testmail('binayak.santra@navsoft.in',
										   "Data Pushed to Elastic @@@SavePriceFromTempToTableLive@@@",
										   'Data preparation Completed and Pushed to Elastic, PRODUCT_COUNT =====>' + str(
											   len(tempDataId)) + ' @ ' + str(
											   datetime.datetime.now()) + ' datas=====>' + str(datas))

		response = emailcomponent.testmail('lifco.onboard@gmail.com',
										   "Data Pushed to Elastic @@@SavePriceFromTempToTableLive@@@",
										   'Data preparation Completed and Pushed to Elastic, PRODUCT_COUNT =====>' + str(
											   len(tempDataId)) + ' @ ' + str(
											   datetime.datetime.now()) + ' datas=====>' + str(obj))

	print("Deleting temp price...................")

# save_price_from_temp_to_table()

@csrf_exempt
def saveprice_temp_to_table(request):
	print('Price cron Running=========')
	save_price_from_temp_to_table()												
					
	data = {
		"status":1
	}
	return JsonResponse(data)

# save_price_from_temp_to_table()