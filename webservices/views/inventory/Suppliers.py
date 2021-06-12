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
from webservices.views import loginview
from django.contrib.auth.hashers import make_password,check_password
from django.utils import timezone
import random
import sys
import traceback
import json
from django.core.mail import EmailMultiAlternatives
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import date,datetime
from webservices.views.common import common
class Suppliers(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		d1={'createdon':datetime.now(),'modifiedon':datetime.now(),'owner_id':1}
		d2=request.data
		email=request.data['email']
		name=request.data['name']
		# fullname=request.data['name']
		country_id=request.data['country_id']
		created_by=request.data['created_by']
		modified_by=request.data['modified_by']
		ip_address=request.data['ip_address']
		code=request.data['code']
		user_id = request.data['user_id']
		website_id = request.data['website_id']

		if EngageboostSuppliers.objects.filter(email=request.data['email'],isdeleted='n').exists():
			data ={'status':0,'message':'Email Id is already exists'}
			return Response(data)

		if EngageboostSuppliers.objects.filter(code=code,isdeleted='n').exists():
			data ={'status':0,'message':'Company Code is already exists'}
			return Response(data)

		serializer_data=dict(d2,**d1)
		serializer = SuppliersSerializer(data=serializer_data,partial=True)

		if serializer.is_valid():
			serializer.save()
			obj = EngageboostSuppliers.objects.latest('id')
			last_id = obj.id
			data ={'status':1,'api_status':last_id,'message':'Successfully Inserted'}

		else:
			data ={'status':0,'api_status':serializer.errors,'message':'Record Insertion failed'}

		return Response(data)


		
class SuppliersList(generics.ListAPIView):
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostSuppliers.objects.using(company_db).get(pk=pk)
		except EngageboostSuppliers.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		user = self.get_object(pk,request)
		serializer = SuppliersSerializer(user)
		settings1 = EngageboostCountries.objects.using(company_db).all().filter(country_name='India')
		serializer1 = GlobalsettingscountriesSerializer(settings1, many=True)
		settings2 = EngageboostCountries.objects.using(company_db).all().filter(~Q(country_name='India')).order_by('country_name')
		serializer2 = GlobalsettingscountriesSerializer(settings2, many=True)
		d1=serializer1.data
		d2 = serializer2.data
		data=d1+d2
		settings3 = EngageboostWarehouseMasters.objects.using(company_db).all().filter(isdeleted='n',
																					   isblocked='n').order_by('name')
		serializer3 = WarehousemastersSerializer(settings3, many=True)
		settings4 = EngageboostUsers.objects.using(company_db).all()
		serializer4 = UserSerializer(settings4, many=True)
		value_id  = EngageboostSuppliers.objects.using(company_db).get(id=pk)
		settings5 = EngageboostStates.objects.using(company_db).all().filter(country_id=value_id.country_id).order_by('state_name')
		serializer5 = StatesSerializer(settings5, many=True)
		settings6 = EngageboostCurrencyMasters.objects.using(company_db).all().filter(isdeleted='n',
																					  isblocked='n').order_by('currencyname')
		serializer6 = CurrencyMastersSerializer(settings6, many=True)
		if(serializer): 
			data ={
				'status':1,
				'countries':data,
				'warehouse':serializer3.data,
				'vendor':serializer4.data,
				'State':serializer5.data,
				'currency':serializer6.data,
				'user':serializer4.data,
				'api_status':serializer.data,
				
				'message':'',
				}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
		return Response(data)
	
	def put(self, request, pk, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		Category = self.get_object(pk,request)
		d1={'modifiedon':datetime.now(),'owner_id':1}
		d2=request.data
		serializer_data=dict(d2,**d1)
		email=request.data['email']
		cnt = EngageboostSuppliers.objects.filter(email=request.data['email'],isdeleted='n').filter(~Q(id=pk)).count()
		
		
		cnt_code = EngageboostSuppliers.objects.filter(code=request.data['code'],isdeleted='n').filter(~Q(id=pk)).count()
		if cnt == 0:
			
				
			if cnt_code==0:    
				serializer = SuppliersSerializer(Category,data=serializer_data,partial=True)
				if serializer.is_valid():
					serializer.save()
					common.related_products_to_elastic('EngageboostSuppliers',pk)
					data ={
					'status':1,
					'api_status':pk,
					'message':'Successfully Updated',
					}
				else:
					data ={
					'status':0,
					'api_status':serializer.errors,
					
					}
					
			else:
				data ={
				'status':0,
				
				'message':'Company Code is already exists',
				}
							

			
				
		else:
			data ={
			'status':0,
			
			'message':'Email Id is already exists',
			}
		return Response(data)

class statelist(generics.ListAPIView):
# """ List all Edit,Uodate Preset """
	def get_object(self, country_id):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostStates.objects.using(company_db).get(country_id=country_id)
		except EngageboostStates.DoesNotExist:
			raise Http404

	def get(self, request, country_id, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		settings_ser = EngageboostStates.objects.using(company_db).all().filter(country_id=country_id).order_by('state_name')
		serializer_ser = StatesSerializer(settings_ser,many=True)
		if(serializer_ser): 
			data ={
				'state_arr':serializer_ser.data,
			}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
		return Response(data)

class Suppliersadd(generics.ListAPIView):
	def get(self, request, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		settings1 = EngageboostCountries.objects.using(company_db).all().filter(country_name='India')
		serializer1 = GlobalsettingscountriesSerializer(settings1, many=True)
		settings2 = EngageboostCountries.objects.using(company_db).all().filter(~Q(country_name='India')).order_by('country_name')
		serializer2 = GlobalsettingscountriesSerializer(settings2, many=True)
		d1=serializer1.data
		d2 = serializer2.data
		data=d1+d2
		settings3 = EngageboostWarehouseMasters.objects.using(company_db).all().filter(isdeleted='n',
																					   isblocked='n').order_by('name')
		serializer3 = WarehousemastersSerializer(settings3, many=True)
		settings4 = EngageboostUsers.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
		serializer4 = UserSerializer(settings4, many=True)
		settings5 = EngageboostStates.objects.using(company_db).all().order_by('state_name')
		serializer5 = StatesSerializer(settings5, many=True)
		settings6 = EngageboostCurrencyMasters.objects.using(company_db).all().filter(isdeleted='n',
																					  isblocked='n').order_by('currencyname')
		serializer6 = CurrencyMastersSerializer(settings6, many=True)
		if(serializer6): 
			data ={
				'status':1,
				'countries':data,
				'warehouse':serializer3.data,
				'vendor':serializer4.data,
				'State':serializer5.data,
				'currency':serializer6.data,
				'user':serializer4.data,
				'message':'',
				}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
		return Response(data)

class SupplierPoList(generics.ListAPIView):
# """ List of Supplier PO List """

	def post(self, request, format=None,many=True):
		company_db = loginview.db_active_connection(request)
		supplier_id=request.data.get('supplier_id')
		user = EngageboostPurchaseOrders.objects.using(company_db).all().filter(supplier_id=supplier_id)
		serializer = PurchaseordersSerializer(user,many=True)
		#####################Query Generation#################################
		if request.data.get('search') and request.data.get('order_by'):
			key=request.data.get('search')
			order_by=request.data.get('order_by')
			order_type=request.data.get('order_type')
			if(order_type=='+'):
				order=order_by
			else:
				order='-'+order_by
			result = EngageboostPurchaseOrders.objects.using(company_db).all().order_by(order).filter(Q(name__icontains=key)|Q(sku__icontains=key)|Q(visibility_id__icontains=key)|Q(cost_per_unit__icontains=key)|Q(default_price__icontains=key))
		elif request.data.get('search'):
			key=request.data.get('search')
			result = EngageboostPurchaseOrders.objects.using(company_db).all().order_by('-id').filter(Q(name__icontains=key)|Q(sku__icontains=key)|Q(visibility_id__icontains=key)|Q(cost_per_unit__icontains=key)|Q(default_price__icontains=key))
		elif request.data.get('order_by'):
			order_by=request.data.get('order_by')
			order_type=request.data.get('order_type')
			if(order_type=='+'):
				order=order_by
			else:
				order='-'+order_by
			result = EngageboostPurchaseOrders.objects.using(company_db).all().order_by(order)    
		else:
			result = EngageboostPurchaseOrders.objects.using(company_db).all().order_by('-id')
		result=result.filter(Q(supplier_id=supplier_id)).filter(isblocked='n',isdeleted='n')
		page = self.paginate_queryset(result)
		#####################Query Generation#################################
		#####################Layout#################################
		if page is not None:
			serializer_product = PurchaseordersSerializer(page, many=True)
			module='PurchaseOrders'
			screen_name='list_posupp'
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
		final_data.append(pre_data)
		return self.get_paginated_response(final_data)

# class WarehouseSupplierMap is used to insert WarehouseSupplierMap
class WarehouseSupplierMap(generics.ListAPIView):
	def get(self, request, format=None):
		pk = request.GET.get("id")
		product = request.GET.get("product")
		supplier = request.GET.get("supplier")
		warehouse = request.GET.get("warehouse")


		company_db = loginview.db_active_connection(request)
		obj = EngageboostWarehouseSupplierMappings.objects.using(company_db)

		if pk!=None and pk!="":
			obj = obj.filter(id=pk)
		if product!=None and product!="":
			obj = obj.filter(product_id=product)
		if supplier!=None and supplier!="":
			obj = obj.filter(supplier_id=supplier)
		if warehouse!=None and warehouse!="":
			obj = obj.filter(warehouse_id=warehouse)	

		objcount = obj.count()
		if objcount>0:
			creditObj = obj.last()
			serializer = WarehouseSupplierMappingsSerializer(creditObj,partial=True)
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
		post_data = request.data
		
		if not 'values' in post_data.keys() or post_data['values']=="" or post_data['values']==None:
			data ={
				'status':0,
				'api_status':"",
				'message':'Data not posted',
			}								
			return Response(data)
		else:
			serializer_datas=post_data['values']

		# if not 'warehouse_ids' in post_data.keys() or post_data['warehouse_ids']=="" or post_data['warehouse_ids']==None or len(post_data['warehouse_ids'])==0:
		# 	data ={
		# 		'status':0,
		# 		'api_status':"",
		# 		'message':'Select warehouse',
		# 	}								
		# 	return Response(data)
		# else:
		# 	warehouse_arr=post_data['warehouse_ids']


		try:
			warehouse_arr=post_data['warehouse_ids']
		except:
			warehouse_arr=[]	

		datas = []
		errors = []		
		
		d1={'created':datetime.now(),'modified':datetime.now()}
		
		for serializer_data in serializer_datas:
			try:
				if serializer_data['id']:
					tax_id = serializer_data['id']
			except KeyError: 
					tax_id = ""

			serializer_data=dict(serializer_data,**d1)
			
			error = []
			
			if not 'supplier_id' in serializer_data.keys() or serializer_data['supplier_id']=="" or serializer_data['supplier_id']==None:
				error.append("Select supplier")
			if not 'product' in serializer_data.keys() or serializer_data['product']=="" or serializer_data['product']==None:
				error.append("Select product")			
			
			if len(error)==0:
				serializer_data['product_id'] = serializer_data['product']
				serializer_data.pop("product")
				if len(warehouse_arr)>0:
					for warehouse in warehouse_arr:
						current_time = datetime.now().astimezone()
						temp_arr = {"warehouse_id":warehouse,"created":current_time,"modified":current_time}
						serializer_data=dict(serializer_data,**temp_arr)
						if tax_id:
							serializer_data.pop("id")
							creditObj = EngageboostWarehouseSupplierMappings.objects.using(company_db).filter(id=tax_id)
							if creditObj.count()>0:
								serializer = WarehouseSupplierMappingsSerializer(creditObj,data=serializer_data,partial=True)
								if serializer.is_valid():
									creditObj.update(**serializer_data)
								else:
									data ={
									'msg':serializer.errors
									}
									errors.append(data)
							else:
								data ={
								'msg':"Data not found"
								}
								errors.append(data)		
								
						else:
							tempObj = EngageboostWarehouseSupplierMappings.objects.filter(product_id=serializer_data['product_id'],warehouse_id=serializer_data['warehouse_id'],supplier_id=serializer_data['supplier_id'],isdeleted='n')

							if tempObj.count()>0:
								tempData = tempObj.last()
								serializer = WarehouseSupplierMappingsSerializer(tempData,data=serializer_data,partial=True)
								if serializer.is_valid():
									resultobj=tempObj.update(**serializer_data)
								else:
									data ={
									'msg':serializer.errors
									}
									errors.append(data)
							else:
								serializer = WarehouseSupplierMappingsSerializer(data=serializer_data,partial=True)
								if serializer.is_valid():
									obj = EngageboostWarehouseSupplierMappings.objects.create(**serializer_data)
									last_id = obj.id
									
								else:
									data ={
									'msg':serializer.errors
									}
									errors.append(data)					
				else:
					if not 'warehouse_id' in serializer_data.keys() or serializer_data['warehouse_id']=="" or serializer_data['warehouse_id']==None:
						data ={
								'status':0,
								'api_status':serializer_data,
								'message':'Select warehouse',
							}								
						return Response(data)
					else:	
						current_time = datetime.now().astimezone()
						temp_arr = {"created":current_time,"modified":current_time}
						serializer_data=dict(serializer_data,**temp_arr)
						if tax_id:
							serializer_data.pop("id")
							creditObj = EngageboostWarehouseSupplierMappings.objects.using(company_db).filter(id=tax_id)
							if creditObj.count()>0:
								serializer = WarehouseSupplierMappingsSerializer(creditObj,data=serializer_data,partial=True)
								if serializer.is_valid():
									creditObj.update(**serializer_data)
								else:
									data ={
									'msg':serializer.errors
									}
									errors.append(data)
							else:
								data ={
								'msg':"Data not found"
								}
								errors.append(data)		
								
						else:
							tempObj = EngageboostWarehouseSupplierMappings.objects.filter(product_id=serializer_data['product_id'],warehouse_id=serializer_data['warehouse_id'],supplier_id=serializer_data['supplier_id'],isdeleted='n')

							if tempObj.count()>0:
								tempData = tempObj.last()
								serializer = WarehouseSupplierMappingsSerializer(tempData,data=serializer_data,partial=True)
								if serializer.is_valid():
									resultobj=tempObj.update(**serializer_data)
								else:
									data ={
									'msg':serializer.errors
									}
									errors.append(data)
							else:
								serializer = WarehouseSupplierMappingsSerializer(data=serializer_data,partial=True)
								if serializer.is_valid():
									obj = EngageboostWarehouseSupplierMappings.objects.create(**serializer_data)
									last_id = obj.id
									
								else:
									data ={
									'msg':serializer.errors
									}
									errors.append(data)

			else:
				errors.append(error)
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

class WarehouseSupplierMapDelete(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		serializer_data=request.data
		
		if not 'warehouse' in serializer_data.keys() or serializer_data['warehouse']=="" or serializer_data['warehouse']==None:
			data ={
					'status':0,
					'api_status':"",
					'message':'Select Warehouse',
				}										
			return Response(data)
		if not 'supplier' in serializer_data.keys() or serializer_data['supplier']=="" or serializer_data['supplier']==None:
			data ={
					'status':0,
					'api_status':"",
					'message':'Select supplier',
				}										
			return Response(data)
		if not 'product' in serializer_data.keys() or serializer_data['product']=="" or serializer_data['product']==None:
			data ={
					'status':0,
					'api_status':"",
					'message':'Select product',
				}										
			return Response(data)

		creditObj = EngageboostWarehouseSupplierMappings.objects.using(company_db).filter(warehouse_id=serializer_data['warehouse'],supplier_id=serializer_data['supplier'],product_id=serializer_data['product'],isdeleted='n')
		
		if creditObj.count()>0:
			creditObj.delete()
			data ={
					'status':1,
					'api_status':"",
					'message':'Successfully Deleted',
				}
		else:
			data ={
					'status':0,
					'api_status':"",
					'message':'Data not found',
				}										
		return Response(data)		

class WarehouseSupplierMapList(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		has_multy=request.data

		warehouse_arr = []

		warhouse_obj = EngageboostWarehouseMasters.objects.using(company_db).filter(isblocked='n',
																					isdeleted='n').order_by('name')
				
		if 'website_id' in has_multy.keys() and has_multy['website_id']!=None and has_multy['website_id']!="":
			website_id = has_multy['website_id']
			warhouse_obj = warhouse_obj.filter(website_id=website_id)
		if 'warehouse' in has_multy.keys() and has_multy['warehouse']!=None and has_multy['warehouse']!="":
			warehouse = has_multy['warehouse']
			warhouse_obj = warhouse_obj.filter(id=warehouse)
					

		if warhouse_obj.count()>0:	
			warhouse_data = warhouse_obj.all()
			warhousedata = WarehousemastersSerializer(warhouse_data,many=True)
			
			for k in warhousedata.data:
				
				supplier_obj = EngageboostSuppliers.objects.using(company_db).filter(isblocked='n',isdeleted='n')
				if 'website_id' in has_multy.keys() and has_multy['website_id']!=None and has_multy['website_id']!="":
					supplier_obj = supplier_obj.filter(website_id=website_id)

				if supplier_obj.count()>0:
					supplier_data = supplier_obj.all()
					supplierdata = SuppliersSerializer(supplier_data,many=True)
					pricedata = []
					for suppliers in supplierdata.data:	
						
						obj = EngageboostWarehouseSupplierMappings.objects.using(company_db).filter(isblocked='n',isdeleted='n',warehouse_id=k['id'],supplier_id=suppliers['id'])
						
						if 'product' in has_multy.keys() and has_multy['product']!=None and has_multy['product']!="":
							product = has_multy['product']
							obj = obj.filter(product_id=product)
						if 'website_id' in has_multy.keys() and has_multy['website_id']!=None and has_multy['website_id']!="":
							obj = obj.filter(website_id=website_id)
						
						if obj.count()>0:

							rs = obj.all()
							
							rs_data = WarehouseSupplierMappingsSerializer(rs,many=True)
							
							for price_data in rs_data.data:
								# print(price_data)
								if 'product' in has_multy.keys() and has_multy['product']!=None and has_multy['product']!="":
									prodObj = EngageboostProducts.objects.filter(id=product).last()
									product_arr = {"product_name":prodObj.name,"product_sku":prodObj.sku}
									price_data = dict(price_data,**product_arr)

								d1={"supplier_name":suppliers['name']}
								price_data = dict(price_data,**d1)

								pricedata.append(price_data)
						
				warehouse_arr.append({"name":k['name'],"id":k['id'],"data":pricedata})		

			return Response(warehouse_arr)
				
		else:		
			data ={
					'status':0,
					'api_status':"",
					'message':'Data Not Found',
				}						
			return Response(data)
