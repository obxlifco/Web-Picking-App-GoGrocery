from webservices.models import *
from django.http import Http404
from webservices.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
import datetime
from datetime import datetime, timedelta
from rest_framework import generics
from itertools import chain
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Q
from django.utils import timezone
from webservices.views import loginview
from django.core.files.storage import FileSystemStorage
import random
import xlrd
import os
import time
import pytz
import xlsxwriter
from webservices.views.common import common
from webservices.views.common.threading import *
from django.db.models import * 
from django.db.models.functions import Cast
class WarehouseStockManagement(generics.ListAPIView):
	def get(self, request,pk,user_id=None, format=None):
		# warehouse_id = request.META.get('HTTP_WAREHOUSEID')
		# website_id = int(request.META.get('HTTP_WID'))
		# is_superadmin = request.META.get('HTTP_ISSUPER')
		# is_subadmin = request.META.get('HTTP_ISSUB')
		website_id = int(pk)
		company_db = loginview.db_active_connection(request) 
		data={}

		user                = request.user
		user_id             = user.id

		# warehouse = EngageboostWarehouseMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		warehouse = EngageboostWarehouseMasters.objects.using(company_db).all().filter(isdeleted='n', isblocked='n',
																					   website_id=website_id).order_by('name')
		
		if user_id!=None and user_id!="":
			userdetails = EngageboostUsers.objects.filter(id=user_id)
			if userdetails.count()>0:
				userdetails = userdetails.first()
				if userdetails.issuperadmin!="Y":
					userObj = EngageboostWarehouseManager.objects.filter(manager_id=user_id)
					if userObj.count()>0:
						userObj = userObj.values("warehouse_id")
						warehouse = warehouse.filter(id__in=userObj)

		warehousedata = WarehousemastersSerializer(warehouse, many=True)
		data['warehouse']=warehousedata.data
		return Response(data)	

class StockList(generics.ListAPIView):
	# """ Stock List """
	def post(self, request, format=None,many=True):
		company_db = loginview.db_active_connection(request)
		#####################Query Generation#################################
		today = datetime.today()
		page_size = 0
		if "item_per_page" in request.data:
			page_size = request.data.get('item_per_page')
		try:
			end_date = request.data['end_date']
			try:
				end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
			except:
				end_date = datetime.strptime(end_date, "%Y-%m-%d")
			end_date = end_date.strftime("%Y-%m-%d")
		except:
			end_date = ""
		try:
			start_date = request.data['start_date']
			try:
				start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
			except:
				start_date = datetime.strptime(start_date, "%Y-%m-%d")	
			start_date = start_date.strftime("%Y-%m-%d")
		except:
			start_date = ""

		try:
			if request.data.get('website_id'):
				website_id = request.data.get('website_id')
			else:
				website_id = 1
		except Exception as error:
			website_id = 1
		
		try:
			if request.data.get('category_id'):
				category_id = request.data.get('category_id')
			else:
				category_id = None
		except Exception as error:
			category_id = None
			
		order_type=request.data['order_type']
		order_by=request.data['order_by']
		warehouse_id=request.data['warehouse_id']
		hide_out_of_stock=request.data['hide_out_of_stock']
		try:
			if request.data.get('show_all'):
				show_all = request.data.get('show_all')
			else:
				show_all = 0
		except Exception as error:
			show_all = 0

		if order_by == 'name' or order_by == 'sku':
			order_by = 'product__'+order_by
		
		if(order_type == '+'):
			order = order_by
		elif(order_type == '-'):
			order = '-'+order_by
		# print(order)
		result = EngageboostProductStocks.objects.using(company_db).all().order_by(order).filter(isblocked='n',product__isdeleted='n').filter(warehouse_id__isdeleted='n',warehouse_id__isblocked='n')
		if category_id is not None:
			rs_child_ids = rs_category = EngageboostCategoryMasters.objects.filter(parent_id__in=category_id).values_list('id', flat = True)
			rs_child_ids = list(rs_child_ids)
			all_cat_ids = category_id + rs_child_ids
			# print('all_cat_ids1222===', all_cat_ids)
			rs_child_ids2 = rs_category = EngageboostCategoryMasters.objects.filter(parent_id__in=rs_child_ids).values_list('id', flat = True)
			rs_child_ids2 = list(rs_child_ids2)
			all_cat_ids = all_cat_ids + rs_child_ids2
			# print('all_cat_ids===', all_cat_ids)
			result = result.filter(product_id__product_list__category_id__in=all_cat_ids)
			
		if request.data['search']:
			key = request.data['search']
			key = key.strip()
			result = result.filter(
				Q(product__id__icontains=key)|Q(product__name__icontains=key)|Q(product__sku__icontains=key)|Q(warehouse__code__icontains=key)
			)
		if warehouse_id!="" and warehouse_id!=None:
			result=result.filter(warehouse_id=warehouse_id)

		if hide_out_of_stock!=0:
			result = result.filter(~Q(real_stock=0))
		result_count = result.count()
		userid=request.data['userid']
		users = EngageboostUsers.objects.using(company_db).get(id=userid)
		issuperadmin = users.issuperadmin
		role_id = users.role_id
		role_permission={}
		menu_fetch = EngageboostMenuMasters.objects.using(company_db).get(module='StockManagement')
		menu_id = menu_fetch.id

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
		if 	result_count !=0:
			if hide_out_of_stock==0:
				result = result
			else:
				result = result.filter(~Q(real_stock=0))
			
			if request.data.get('advanced_search'):
				filter_arr = request.data.get('advanced_search')
				result = common.get_advanced_search_filter("EngageboostProducts",filter_arr,result)

			if start_date!="" and end_date!="":
				# result = result.filter(modified__range=[start_date, end_date])
				result = result.filter(modified__date_gte=start_date, modified__date_lte=end_date)
				
			if warehouse_id!="" and warehouse_id!=None:
				result=result.filter(warehouse_id=warehouse_id)
			# print("result====", result.query)
			if show_all == 0:
				page = self.paginate_queryset(result)
			else:
				page = result.all()
			serializer = StockSerializer(page,context={'warehouse_id': warehouse_id}, many=True)
			arr=[]

			if len(serializer.data)>0:
				for product in serializer.data:
					# print('product=====', json.dumps(product["product"]))
					# for procuctinfos in procuctinfo:
					date=EngageboostGlobalSettings.objects.using(company_db).get(website_id=1)
					zone=EngageboostTimezones.objects.using(company_db).get(id=date.timezone_id)
					product_price = 0
					qs_price_data = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=product['product']['id'], warehouse_id=warehouse_id, product_price_type_id__price_type_id=1).first()
					if qs_price_data:
						product_price = qs_price_data.price
					time_zone = get_time(product['modified'],zone,date)
					str_weight = 0
					if product['product']['weight'] is not None and float(product['product']['weight'])>0:
						print("kjdsks",product['product']['id'] )
						str_weight = product['product']['weight']
					data ={
							'id':product['product']['id'],
							'warehouse_name':product['warehouse']['name'],
							'sku':product['product']['sku'],
							'product_name':product['product']['name'],
							'uom':product['product']['uom'],
							'weight':str_weight,
							'product_image':product['product']['product_images'],
							'safety_stock':product['safety_stock'],
							'last_modified':time_zone,
							'real_stock':product['real_stock'],
							'qty':product['stock'],
							'safety_stock':product['safety_stock'],
							'product_price': product_price
						}
					arr.append(data)
					data2 ={
						'product':arr
					}
			else:
				data2 = {
					'product':[]
				}
			pre_data={}
			final_data=[]
			pre_data['result']=data2
			pre_data['role_permission']=role_permission
			pre_data['page_size']=page_size
			final_data.append(pre_data)
			return self.get_paginated_response(final_data)
		else:
			data2 = {
				'product':[]
			}
			pre_data={}
			final_data=[]
			pre_data['result'] = data2
			pre_data['role_permission']=role_permission
			pre_data['page_size']=page_size
			final_data.append(pre_data)
			return Response({'status':0, 'Message':'No Data Found'})

class StockListView(generics.ListAPIView):
	# """ Stock List Update"""
	def put(self, request, format=None,many=True):
		company_db = loginview.db_active_connection(request)
		qty=request.data['qty']
		safety_stock=request.data['safety_stock']
		warehouse_id=request.data['warehouse_id']
		product_id=request.data['product_id']

		prv_stock=EngageboostProductStocks.objects.using(company_db).get(warehouse_id=warehouse_id,product_id=product_id)

		if request.data['action'] == 'increase':
			curr_stock=int(prv_stock.stock)+int(qty)
			# real_stock=float(prv_stock.real_stock)-float(safety_stock) + float(qty)
			real_stock = int(prv_stock.stock)+int(qty)-prv_stock.virtual_stock-int(safety_stock)			
			# $stockTable['StockData']['real_stock'] = ($StockData['StockData']['stock']+$qty)-$StockData['StockData']['virtual_stock']-$StockData['StockData']['safety_stock'];
		else:	
			curr_stock=int(prv_stock.stock)-int(qty)
			# real_stock=float(prv_stock.real_stock)-float(safety_stock) - float(qty)
			real_stock = int(prv_stock.stock)-int(qty)-prv_stock.virtual_stock-int(safety_stock)
			# $stockTable['StockData']['real_stock'] = ($StockData['StockData']['stock']-$qty)-$StockData['StockData']['virtual_stock']-$this->data['PopIncrease']['safety_stock'];//['StockData']['safety_stock'];

		# real_stock=int(curr_stock)-int(safety_stock)
		EngageboostProductStocks.objects.using(company_db).filter(warehouse_id=warehouse_id,product_id=product_id).update(safety_stock=safety_stock,stock=curr_stock,real_stock=real_stock)
		EngageboostProductStockCrons.objects.using(company_db).create(warehouse_id=warehouse_id,product_id=product_id,stock=qty,created=datetime.now().date())
		EngageboostPurchaseOrderReceivedProducts.objects.using(company_db).create(quantity=qty,product_id=product_id)
		d2=request.data
		received_date_time=request.data['received_date']
		if 'T' in str(received_date_time):
			received_date_time_array=str(received_date_time).split("T")
			received_date=received_date_time_array[0]

		d1={'created':datetime.now().date(),'modified':datetime.now().date(),'received_date':received_date,'quantity':qty,'status':'r'}
		
		
		serializer_data=dict(d2,**d1)
		
		serializer = PurchaseOrdersReceivedSerializer(data=serializer_data,partial=True)
		if serializer.is_valid():
			serializer.save()

			product_stock = common.get_product_stock(product_id)
			elastic = common.change_field_value_elastic(product_id,'EngageboostProducts',{'inventory':product_stock})

			data ={
			'status':1,
			'api_status':'',
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

class StockSuppliers(generics.ListAPIView):
	# """ Warehouse for Stock Management """
	def get(self, request, format=None): 
		company_db = loginview.db_active_connection(request)
		data={}
		received_ids=EngageboostPurchaseOrderReceivedProducts.objects.using(company_db).latest('id')
		
		received_id =int(received_ids.id)+int(1)
		
		imageresizeon= EngageboostGlobalSettings.objects.using(company_db).get(website_id=1)
		data['received_code']=str(imageresizeon.receiptid_format)+str(received_id)
		StockSuppliers = EngageboostSuppliers.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		Suppliers = SuppliersSerializer(StockSuppliers, many=True)
		data['Suppliers']=Suppliers.data
		warehouse = EngageboostWarehouseMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		warehousedata = WarehousemastersSerializer(warehouse, many=True)
		data['warehouse']=warehousedata.data
		return Response(data)

class StockMove(generics.ListAPIView):
	# """ Warehouse for Stock Management """
	def put(self, request, format=None):
		company_db = loginview.db_active_connection(request) 
		qty=request.data['qty']
		to_location=request.data['to_location']
		from_location=request.data['from_location']
		product_id=request.data['product_id']
		received_code=request.data['received_code']
		received_date_time=request.data['received_date']
		if 'T' in str(received_date_time):
			received_date_time_array=str(received_date_time).split("T")
			received_date=received_date_time_array[0]
		
		
		createdby=request.data['createdby']

		from_location_stock=EngageboostProductStocks.objects.using(company_db).get(warehouse_id=from_location,product_id=product_id)
		if (EngageboostProductStocks.objects.using(company_db).filter(warehouse_id=to_location,product_id=product_id).exists()):
			to_location_stock=EngageboostProductStocks.objects.using(company_db).get(warehouse_id=to_location,product_id=product_id)
		else:
			#to_location_stock=EngageboostProductStocks.objects.using(company_db).get(warehouse_id=to_location,product_id=product_id,)
			to_location_stock=EngageboostProductStocks.objects.using(company_db).get(warehouse_id=to_location,product_id=product_id)
		form_move=int(from_location_stock.stock)-int(qty)
		to_move=int(to_location_stock.stock)+int(qty)
		
		EngageboostProductStocks.objects.using(company_db).filter(warehouse_id=from_location,product_id=product_id).update(stock=form_move,real_stock=form_move-int(from_location_stock.safety_stock))
		EngageboostProductStocks.objects.using(company_db).filter(warehouse_id=to_location,product_id=product_id).update(stock=to_move,real_stock=to_move-int(to_location_stock.safety_stock))
		EngageboostPurchaseOrdersReceived.objects.using(company_db).create(status='r',received_purchaseorder_id=received_code,received_date=received_date,warehouse_id=to_location,product_id=product_id,action='move',quantity=int(qty))
		latest=EngageboostPurchaseOrdersReceived.objects.using(company_db).latest('id')
		last_id = latest.id
		EngageboostProductMoveTrack.objects.using(company_db).create(website_id=1,createdby=createdby,purchase_order_received_id=last_id,product_id=product_id,warehouse_id_from=from_location,warehouse_id_to=to_location)		

		data ={
			'status':1,
			'api_status':'',
			'message':'Successfully Moved',
			}
		return Response(data)

def get_time(gettime,zone,date):
	datetime = gettime.replace('T',' ')
	data_time=datetime.replace('Z',' ')
	a=data_time.split(".")
	b=a[0].replace(':',' ')
	c=b.replace('-',' ')
	date_format=c.split(" ")
	import datetime
	import time
	a1 = datetime.datetime(int(date_format[0]), int(date_format[1]), int(date_format[2]), int(date_format[3]), int(date_format[4]), int(date_format[5]))
	if zone.offset == 5.5:
		b1 = a1 + datetime.timedelta(hours=5,minutes=29) # days, seconds, then other fields.
		added_time=b1.time()
		ad_time=str(added_time).split(":")
	else:
		b1 = a1 + datetime.timedelta(hours=zone.offset) # days, seconds, then other fields.
		added_time=b1.time()
		ad_time=str(added_time).split(":")
		
	t = (int(date_format[0]), int(date_format[1]), int(date_format[2]), int(ad_time[0]), int(ad_time[1]), int(ad_time[2]),0,0,0)
	t = time.mktime(t)
	format1 =date.date_format
	datetime_object=time.strftime(format1+" %I:%M %p", time.gmtime(t))
	return datetime_object
	
def get_date(gettime,zone,date):
	import datetime
	gettime=str(gettime)
	format1 =date.date_format
	datetime_object=datetime.datetime.strptime(gettime, '%Y-%m-%d').strftime(format1)
	return datetime_object

def get_day(gettime,zone,date):
	import datetime
	gettime=str(gettime)
	format1 =date.date_format
	datetime_object=datetime.datetime.strptime(gettime, '%Y-%m-%d').strftime('%A')
	return datetime_object				

class StockAdjustmentList(generics.ListAPIView):
	# """ List all Edit,Uodate Brand """
	def post(self, request, format=None,many=True):
		company_db = loginview.db_active_connection(request)
		stock_type=request.data['stock_type']
		user = EngageboostPurchaseOrdersReceived.objects.using(company_db).all()
		serializer = PurchaseOrdersReceivedSerializer(user,many=True)
		#####################Query Generation#################################
		if request.data.get('search') and request.data.get('order_by'):
			key=request.data.get('search')
			order_by=request.data.get('order_by')
			order_type=request.data.get('order_type')
			if(order_type=='+'):
				order=order_by
			else:
				order='-'+order_by
			result = EngageboostPurchaseOrdersReceived.objects.using(company_db).all().order_by(order).filter(Q(purchase_order_master_id__icontains=key)|Q(shipping_cost__icontains=key)|Q(purchase_order_tax__icontains=key)|Q(gross_amount__icontains=key)|Q(net_amount__icontains=key)|Q(discount_amount__icontains=key))
		elif request.data.get('search'):
			key=request.data.get('search')
			result = EngageboostPurchaseOrdersReceived.objects.using(company_db).all().order_by('-id').filter(Q(purchase_order_master_id__icontains=key)|Q(shipping_cost__icontains=key)|Q(purchase_order_tax__icontains=key)|Q(gross_amount__icontains=key)|Q(net_amount__icontains=key)|Q(discount_amount__icontains=key))
		elif request.data.get('order_by'):
			order_by=request.data.get('order_by')
			order_type=request.data.get('order_type')
			if(order_type=='+'):
				order=order_by
			else:
				order='-'+order_by
			result = EngageboostPurchaseOrdersReceived.objects.using(company_db).all().order_by(order)
		else:
			result = EngageboostPurchaseOrdersReceived.objects.using(company_db).all().order_by('-id')
		if stock_type!='':
			result=result.filter(action=stock_type).filter(status='r')
		
		result=result.filter(isblocked='n',isdeleted='n')
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
			serializer_product = PurchaseOrdersReceivedSerializer(page, many=True)
			row_dict={}
			row=[]
			product=[]
			layout_arr=[]
			for serializer_row in serializer_product.data :
				row_dict=serializer_row

				purchase_order_received_id=serializer_row['id']

				if serializer_row['purchase_order_master_id']:
					# print(purchase_order_received_id)
					received_products=EngageboostPurchaseOrderReceivedProducts.objects.using(company_db).all().filter(purchase_order_received_id=purchase_order_received_id)
					
					product_received = PurchaseOrderReceivedProductsSerializer(received_products, many=True)
					
					row_dict['products']=product_received.data
				else:
					row_dict['products']=[]
				supplier_id=serializer_row['supplier_id']
				if supplier_id:
					fetch_supplier=EngageboostSuppliers.objects.using(company_db).get(id=supplier_id)
					row_dict['vendor']=fetch_supplier.name
				else:
					row_dict['vendor']=''

				warehouse_id=serializer_row['warehouse_id']
				if warehouse_id:
					fetch_warehouse=EngageboostWarehouseMasters.objects.using(company_db).get(id=warehouse_id)
					row_dict['warehouse']=fetch_warehouse.name
				else:
					row_dict['warehouse']=''

				

				purchase_order_master_id=serializer_row['purchase_order_master_id']
				if purchase_order_master_id:
					fetch_po=EngageboostPurchaseOrders.objects.using(company_db).get(id=purchase_order_master_id)
					row_dict['po_no']=fetch_po.purchase_order_id
				else:
					row_dict['po_no']=''

				date=EngageboostGlobalSettings.objects.using(company_db).get(website_id=1)
				zone=EngageboostTimezones.objects.using(company_db).get(id=date.timezone_id)

				date_fetch=get_date(serializer_row['received_date'],zone,date)	
				
				day_fetch= get_day(serializer_row['received_date'],zone,date)

				row_dict['received_date']=date_fetch
				row_dict['received_day']=day_fetch


				count_track=EngageboostProductMoveTrack.objects.using(company_db).filter(purchase_order_received_id=purchase_order_received_id).count()

				if count_track!=0:

					fetch_track=EngageboostProductMoveTrack.objects.using(company_db).get(purchase_order_received_id=purchase_order_received_id)

					fetch_warehouse_from=EngageboostWarehouseMasters.objects.using(company_db).get(id=fetch_track.warehouse_id_from)
					fetch_warehouse_to=EngageboostWarehouseMasters.objects.using(company_db).get(id=fetch_track.warehouse_id_to)
					row_dict['warehouse_from']=fetch_warehouse_from.name
					row_dict['warehouse_to']=fetch_warehouse_to.name

				else:
					row_dict['warehouse_from']=''
					row_dict['warehouse_to']=''

				row_dict['lot_no']=''
				row_dict['rack_no']=''
				# product.append(product_received.data)
				# row_dict['products'] = product

				row.append(row_dict)

			module='PurchaseOrdersReceived'
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

class ImportStockSheet(generics.ListAPIView):
	def post(self, request, format=None):
		import datetime
		company_db = loginview.db_active_connection(request)
		
		post_data = request.data
		website_id = post_data['website_id']
		company_id = post_data['company_id']
		# d1={"website_id":website_id,"company_id":company_id}
		# serializer_data=dict(post_data,**d1)

		if 'import_file' in request.FILES:
			rand = str(random.randint(1111,9999))
			file1 = request.FILES['import_file']
			file_name=file1.name

			if file_name:
				ext = file_name.split('.')[-1]
				new_file_name='ProductStockFile_'+rand
				fs=FileSystemStorage()
				filename = fs.save('importfile/product_stock_file/'+new_file_name+'.'+ext, file1)


				importstockfile_cond = EngageboostImportStockFiles.objects.using(company_db).filter(company_id=company_id,website_id=website_id).order_by('-id').first()
				
				if importstockfile_cond:
					importstockfile = ImportStockFilesSerializer(importstockfile_cond,partial=True)
					if importstockfile.data['live_stock_updated'] == 'Y':
						queue_no = importstockfile.data['queue_no']+1
					else:
						queue_no = importstockfile.data['queue_no']
						if queue_no>0:
							queue_no=queue_no
						else:
							queue_no=1
				else:
					queue_no = 1

				# current_time = pytz.timezone('Asia/Kolkata').localize(datetime.datetime.now())
				current_time = datetime.datetime.now(pytz.timezone('utc')).astimezone()
				d1={"website_id":website_id,"company_id":company_id,"file_name":new_file_name+'.'+ext,"original_file_name":file_name,"file_type":"xls","stock_import_type":"Append","imported_on":current_time,"imported_status":"N","queue_no":queue_no,"total_success_sku":"0","total_error_sku":"0"}
				serializer_data=dict(post_data,**d1)


				# has_record = EngageboostImportStockFiles.objects.last()
				# if has_record:
				# 	last_entry_of_table = EngageboostImportStockFiles.objects.order_by('-id').latest('id')
				# 	row_id = last_entry_of_table.id+1
				# else:
				# 	row_id = 1

				# d1={"id":row_id};serializer_data=dict(post_data,**d1)
				
				serializer_data.pop("import_file")

				serializer = ImportStockFilesSerializer(data=serializer_data,partial=True)
				if serializer.is_valid():
					serializer.save()
					
					upload_temp_stock(request,serializer.data['id'])

					data ={
					'status':1,
					'api_status':serializer.data['id'],
					'message':'Stock will Upload Successfully',
					}
					return Response(data)
				else:
					data ={
					'status':0,
					'api_status':serializer.errors,
					'message':'Error Occured',
					}
					return Response(data)

					# stock_file_data = EngageboostImportStockFiles.objects.using(company_db).create(**serializer_data)
					# last_inserted_id = stock_file_data.id

				# if stock_file_data:
				# 	data ={
				# 	'status':1,
				# 	'api_status':last_inserted_id,
				# 	'message':'File Upload Successfully',
				# 	}
				# 	return Response(data)
				# else:
				# 	data ={
				# 	'status':0,
				# 	'api_status':serializer.errors,
				# 	'message':'Error Occured',
				# 	}
				# 	return Response(data)
			else:
				data ={
				'status':1,
				'api_status':'File Not Selected',
				'message':'File Not Selected',
				}
				return Response(data)

class UpdateTempStock(generics.ListAPIView):
	def get(self, request, website_id, company_id, format=None):
		company_db = loginview.db_active_connection(request)

		stock_files_cond = EngageboostImportStockFiles.objects.using(company_db).filter(website_id=website_id,company_id=company_id,imported_status='N',is_deleted='N',queue_no__gt=0).first()

		if stock_files_cond:
			stock_files = ImportStockFilesSerializer(stock_files_cond,partial=True)

			if stock_files.data['file_type'] == 'xls':
				FileName = stock_files.data['file_name']
				fs=FileSystemStorage()
				filename = 'importfile/product_stock_file/'+FileName
				uploaded_file_url = fs.url(filename)
				BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

				csvReader = xlrd.open_workbook(settings.BASE_DIR+uploaded_file_url)

				sheet = csvReader.sheet_by_index(0)
				length=len(sheet.col_values(0))
				arr_message=[]
				for x in range(length):
					if(sheet.col_values(0)[x]=='Warehouse Code'):
						pass
					else:						
						warehouse_code=sheet.col_values(0)[x]
						sku=sheet.col_values(1)[x]
						quantity=sheet.col_values(2)[x]
						action_qty=sheet.col_values(3)[x]
						safety_stock=sheet.col_values(4)[x]
						real_stock=sheet.col_values(5)[x]
						lot_number=sheet.col_values(6)[x]
						rack_number=sheet.col_values(7)[x]

						has_record = EngageboostImportedTempProductStocks.objects.last()
						if has_record:
							last_entry_of_table = EngageboostImportedTempProductStocks.objects.order_by('-id').latest('id')
							row_id = int(last_entry_of_table.id)+int(1)
						else:
							row_id = 1

						current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()

						stock_temp_data = EngageboostImportedTempProductStocks.objects.using(company_db).create(id=row_id,warehouse_name=warehouse_code,sku=sku,quantity=quantity,lot_number=lot_number,rack_number=rack_number,safety_stock=safety_stock,error_log='',company_id=company_id,website_id=website_id,is_imported=0,imported_on=current_time,stock_file_imorted_id=stock_files.data['id'])

						if stock_temp_data:
							last_stock_temp_data_id = stock_temp_data.id
							EngageboostImportStockFiles.objects.filter(id=stock_files.data['id']).update(imported_status="Y")
							data = {"status":1,"api_response":last_stock_temp_data_id,"message":"Success"}
						else:
							data = {"status":1,"api_response":"Failed","message":"Failed"}			
		else:
			data={"status":0,"api_status":"No File Exists","message":"No File Exists"}

		# stock_updated_status = EngageboostImportStockFiles.objects.using(company_db).get(id=shipping_id)
		# stock_file_update_status = ImportStockFilesSerializer(stock_updated_status, data=serializer_data,partial=True)

		# obj = EngageboostImportStockFiles.objects.using(company_db).get(id=shipping_id)
		# obj.imported_status = "Y"
		# obj.save()

		return Response(data)

class UpdateTempStockViaCron(generics.ListAPIView):
	def get(self, request, website_id, company_id, format=None):
		import datetime
		company_db = loginview.db_active_connection(request)
		datas=[]
		stock_files_cond = EngageboostImportStockFiles.objects.using(company_db).filter(website_id=website_id,company_id=company_id,live_stock_updated='N',is_deleted='N').all()

		if stock_files_cond:
			for item in stock_files_cond:
				stock_files = ImportStockFilesSerializer(item,partial=True)
				print('=========',stock_files.data['id'])
				website_id = stock_files.data['website_id']
				company_id = stock_files.data['company_id']
				EngageboostImportStockFiles.objects.filter(id=stock_files.data['id']).update(live_stock_updated="Y")
				# return Response(stock_files.data)

				if stock_files.data['stock_import_type'] == 'Append':
					# temp_stock_file_condition = EngageboostImportedTempProductStocks.objects.using(company_db).all().filter(stock_file_imorted_id=stock_files.data['id'],is_imported='N')
					temp_stock_file_condition = EngageboostImportedTempProductStocks.objects.using(company_db).all().filter(stock_file_imorted_id=stock_files.data['id'],is_imported='N')
					print(temp_stock_file_condition.query)
					if temp_stock_file_condition:				
						stock_temp_files_datas = ImportedTempProductStocksSerializer(temp_stock_file_condition,many=True)

						for stock_temp_files_data in stock_temp_files_datas.data:
							# return Response(stock_temp_files_data['sku'])
							try:
								stock_temp_files_data['sku'] = stock_temp_files_data['sku'].split('.')
								stock_temp_files_data['sku'] = stock_temp_files_data['sku'][0]
							except:
								pass
							product_condition =  EngageboostProducts.objects.using(company_db).filter(sku=stock_temp_files_data['sku'],website_id=website_id,isdeleted='n',status='n').first()  
							
							if product_condition:
								product_details = BasicinfoSerializer(product_condition,partial=True)
								product_id = product_details.data['id']
							else:
								product_id = 0

							warehouse_condition = EngageboostWarehouseMasters.objects.using(company_db).filter(code=stock_temp_files_data['warehouse_name'],website_id=website_id,isdeleted='n').first()
							if warehouse_condition:
								warehouse_data = WarehousemastersSerializer(warehouse_condition,partial=True)
								warehouse_id = warehouse_data.data['id']	
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
								prd_stock_condition = EngageboostProductStocks.objects.using(company_db).filter(product_id=product_id,warehouse_id=warehouse_id).first()
								if prd_stock_condition:
									check_stock_data = StockSerializer(prd_stock_condition,partial=True)
									if check_stock_data.data['virtual_stock'] != '':
										virtual_stock = check_stock_data.data['virtual_stock']
									else:
										virtual_stock =  0

									total_valid_qty = virtual_stock+safety_stock;
									real_stock = ((quantity+check_stock_data.data['stock'])-(virtual_stock+check_stock_data.data['safety_stock']+safety_stock))
									safety_stock = safety_stock+check_stock_data.data['safety_stock']
									quantity = quantity+check_stock_data.data['stock']

									serializer_data = dict()
									current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
									d1={"product_id":product_id,"warehouse_id":warehouse_id,"stock":quantity,"safety_stock":safety_stock,"real_stock":real_stock,"islot":lot_number,"islabel":rac_number,"modified":str(current_time)}
									serializer_data=dict(serializer_data,**d1)

									product_stock_table_id = EngageboostProductStocks.objects.using(company_db).get(id=check_stock_data.data['id'])
									serializer = StockSerializer(product_stock_table_id, data=serializer_data,partial=True)
									if serializer.is_valid():
										serializer.save()
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
									d1={"product_id":product_id,"warehouse_id":warehouse_id,"stock":quantity,"safety_stock":safety_stock,"real_stock":real_stock,"islot":lot_number,"islabel":rac_number,"created":current_time,"modified":current_time}
									serializer_data=dict(serializer_data,**d1)

									serializer = StockSerializer(data=serializer_data,partial=True)
									if serializer.is_valid():
										serializer.save()
										data ={'status':1,'api_status':serializer.data['id'],'message':'Stock Inserted'}
									else:
										data ={'status':0,'api_status':serializer.errors,'message':'Error Occured In Insert'}

									datas.append(data)
									# return Response(data)
								EngageboostImportedTempProductStocks.objects.filter(id=stock_temp_files_data['id']).update(is_imported="Y")
							else:
								data ={'status':0,'api_status':'Error Occured','message':'Either product is not exists or warehouse is not exists or error in quantity'}
								datas.append(data)
								# return Response(data)

			if datas:
				data ={'status':1,'api_status':datas}
			else:
				data ={'status':0,'api_status':datas}
			return Response(data)

		else:
			data ={'status':1,'api_status':'No Temporary Stock','message':'No Temporary Stock'}
			return Response(data)
		# else:
		# 	data ={'status':0,'api_status':'All Stock Files Imported','message':'All Stock Files Imported'}
		# 	return Response(data)




class AddReceivedPeoductDetails(generics.ListAPIView):

	def post(self, request):

		postdata = request.data
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()

		condition =  ('received', 'damaged', 'expired', 'shortage', 'mrp_issue')
		#================================= Validation Part ===========================================	
		for data in postdata['product']:

			damaged_quantity = 0
			shortage_quantity = 0
			received_quantity = 0
			total_quantity = int(data['total_quantity'])
			
			if not 'website_id' in postdata:
				return Response({'status':0, 'Message': 'Please provide Website Id'})

			if not EngageboostPurchaseOrders.objects.filter(id=postdata['purchase_order_id']).exists():
				return Response({'status':0, 'Message':'Invalid Purchase Order id Provided'})

			if not EngageboostPurchaseOrderProducts.objects.filter(purchase_order_id=postdata['purchase_order_id']).exists():
				return Response({'status':0, 'Message':'Invalid Purchase Order Product Entry Does Not Exists'})


			po_quantity = EngageboostPurchaseOrderProducts.objects.filter(purchase_order_id=postdata['purchase_order_id'],product_id=data['product_id']).first()

			if not EngageboostProducts.objects.filter(id=data['product_id']).exists():
				return Response({'status':0, "Message":"Such Product does not exists"})


			if not EngageboostPurchaseOrdersReceived.objects.filter(id=postdata['purchase_order_received_id']).exists():
				return Response({'status':0, 'Message':'Invalid Purchase Order Received id Provided'})

			get_sku = EngageboostProducts.objects.get(id=data['product_id']).sku

			for damaged in data['damaged']:
				if damaged['goods_condition'] != '' and damaged['goods_condition'] != None:
					if not damaged['goods_condition'] in condition:
						return Response({'status':0, 'Message':"Please Provide a valid goods condition for Damaged Product"})

				if int(damaged['quantity']) > int(total_quantity):
					return Response({'status':0, "Message":'Damaged Quantity can not be greater than Total quantity of SKU: '+get_sku})
				damaged_quantity = damaged_quantity + int(damaged['quantity'])

			if damaged_quantity > total_quantity:
				return Response({'status':0, "Message":'Damaged Quantity can not be greater than Total quantity of SKU: '+get_sku})

			for shortage in data['shortage']:
				if shortage['goods_condition'] != '' and shortage['goods_condition'] != None:
					if not shortage['goods_condition'] in condition:
						return Response({'status':0, 'Message':"Please Provide a valid goods condition for Shortage Product"})

				if int(shortage['quantity']) > total_quantity:
					return Response({'status':0, "Message":'Shortage Quantity can not be greater than Total quantity of SKU: '+get_sku})
				shortage_quantity = shortage_quantity + int(shortage['quantity'])

			if shortage_quantity > total_quantity:
				return Response({'status':0, "Message":'Shortage Quantity can not be greater than Total quantity  SKU: '+get_sku})

			for received in data['received']:
				if received['goods_condition'] != '' and received['goods_condition'] != None:
					if not received['goods_condition'] in condition:
						return Response({'status':0, 'Message':"Please Provide a valid goods condition for Received Product"})
				print(received['quantity'])
				print(data['total_quantity'])
				if received['quantity'] > data['total_quantity']:
					return Response({'status':0, "Message":'Damaged Quantity can not be greater than Total quantity of SKU: '+get_sku})
				received_quantity = received_quantity + int(received['quantity'])

			if received_quantity > total_quantity:
				return Response({'status':0, "Message":'Received Quantity can not be greater than Total quantity of SKU: '+get_sku})

			if (received_quantity + damaged_quantity + shortage_quantity) > total_quantity:
				return Response({'status':0, "Message":'PO Quantity can not be greater than Total quantity of SKU: '+get_sku})
			if po_quantity:
				po_quantity = po_quantity.quantity
				if total_quantity > po_quantity:
					return Response({'status':0, "Message":'Total quantity can not be greater than PO Quantity of SKU: '+get_sku})

			existed_total_quantity = 0
			existed_remaining_quantity = 0
			used_quantity = 0
			if EngageboostPurchaseOrderReceivedProductDetails.objects.filter(purchase_order_product_id=EngageboostPurchaseOrderProducts.objects.get(purchase_order_id=postdata['purchase_order_id'],product_id=data['product_id']).id).exists():
				get_details_record = EngageboostPurchaseOrderReceivedProductDetails.objects.filter(purchase_order_product_id=EngageboostPurchaseOrderProducts.objects.get(purchase_order_id=postdata['purchase_order_id'],product_id=data['product_id']).id)
				existed_quantity = get_details_record.last().total_quantity

				for record in get_details_record:
					if record.damaged_quantity != 0 and record.damaged_quantity != None:
						used_quantity = used_quantity + record.damaged_quantity

					if record.shortage_quantity != 0 and record.shortage_quantity != None:
						used_quantity = used_quantity + record.shortage_quantity

					if record.received_quantity != 0 and record.received_quantity != None:
						used_quantity = used_quantity + record.received_quantity


				existed_remaining_quantity = po_quantity - used_quantity

			else:
				existed_remaining_quantity = po_quantity

		if total_quantity >  existed_remaining_quantity:
			return Response({'status':0, 'Message':"Can not add quantity more than PO Quantity of SKU: "+get_sku})

		if total_quantity == existed_remaining_quantity:
			status = "Received Full"

		if total_quantity < existed_remaining_quantity:
			status = "Received Partial"

		#================================= Validation Part ===========================================	

		for data in postdata['product']:
			damaged_quantity = 0
			shortage_quantity = 0
			received_quantity = 0
			lot_no = ""
			rack_no = ""
			lot_count = 0
			rack_count = 0

			for damaged in data['damaged']:
				if int(damaged['quantity']) > 0:
					damaged_quantity = int(damaged['quantity'])
					create_record = EngageboostPurchaseOrderReceivedProductDetails.objects.create(website_id=postdata['website_id'], 
																							total_quantity=data['total_quantity'],
																							purchase_order_id=postdata['purchase_order_id'],
																							purchase_order_product_id=EngageboostPurchaseOrderProducts.objects.get(purchase_order_id=postdata['purchase_order_id'],product_id=data['product_id']).id,
																							purchase_order_received_id=postdata['purchase_order_received_id'],
																							created=now_utc, modified=now_utc,
																							isblocked='n', isdeleted='n')

					create_record.damaged_quantity = damaged['quantity']
					# if damaged['received_date'] != "" and damaged['received_date'] != None:
					create_record.received_date = data['received_date']
					if damaged['expiry_date'] != "" and damaged['expiry_date'] != None:
						create_record.expiry_date = damaged['expiry_date']
					if damaged['expiry_issue_comment'] != "" and damaged['expiry_issue_comment'] != None:
						create_record.expiry_issue_comment = damaged['expiry_issue_comment']
					if damaged['expiry_issue'] != "" and damaged['expiry_issue'] != None:
						create_record.expiry_issue = damaged['expiry_issue']

					if damaged['lot_no'] != "" and damaged['lot_no'] != None:
						create_record.lot_no = damaged['lot_no']

					if damaged['rack_no'] != "" and damaged['rack_no'] != None:
						create_record.rack_no = damaged['rack_no']

					if damaged['manufactured_date'] != "" and damaged['manufactured_date'] != None:
						create_record.manufactured_date = damaged['manufactured_date']

					if damaged['remarks'] != "" and damaged['remarks'] != None:
						create_record.remarks = damaged['remarks']

					if damaged['price'] != "" and damaged['price'] != None:
						create_record.price = damaged['price']

					if damaged['discount'] != "" and damaged['discount'] != None:
						create_record.discount = damaged['discount']

					if damaged['goods_condition'] != "" and damaged['goods_condition'] != None:
						create_record.goods_condition = damaged['goods_condition']

					create_record.save()


			for shortage in data['shortage']:

				if int(shortage['quantity']) > 0:
					shortage_quantity = int(shortage['quantity'])

					create_record = EngageboostPurchaseOrderReceivedProductDetails.objects.create(website_id=postdata['website_id'], 
																							total_quantity=data['total_quantity'],
																							purchase_order_id=postdata['purchase_order_id'],
																							purchase_order_product_id=EngageboostPurchaseOrderProducts.objects.get(purchase_order_id=postdata['purchase_order_id'],product_id=data['product_id']).id,
																							purchase_order_received_id=postdata['purchase_order_received_id'],
																							created=now_utc, modified=now_utc,
																							isblocked='n', isdeleted='n')

					create_record.shortage_quantity = shortage['quantity']

					# if shortage['received_date'] != "" and shortage['received_date'] != None:
					create_record.received_date = data['received_date']

					if shortage['expiry_date'] != "" and shortage['expiry_date'] != None:
						create_record.expiry_date = shortage['expiry_date']

					if shortage['expiry_issue_comment'] != "" and shortage['expiry_issue_comment'] != None:
						create_record.expiry_issue_comment = shortage['expiry_issue_comment']

					if shortage['expiry_issue'] != "" and shortage['expiry_issue'] != None:
						create_record.expiry_issue = shortage['expiry_issue']

					if shortage['lot_no'] != "" and shortage['lot_no'] != None:
						create_record.lot_no = shortage['lot_no']

					if shortage['rack_no'] != "" and shortage['rack_no'] != None:
						create_record.rack_no = shortage['rack_no']

					if shortage['manufactured_date'] != "" and shortage['manufactured_date'] != None:
						create_record.manufactured_date = shortage['manufactured_date']

					if shortage['remarks'] != "" and shortage['remarks'] != None:
						create_record.remarks = shortage['remarks']

					if shortage['price'] != "" and shortage['price'] != None:
						create_record.price = shortage['price']

					if shortage['discount'] != "" and shortage['discount'] != None:
						create_record.discount = shortage['discount']

					if shortage['goods_condition'] != "" and shortage['goods_condition'] != None:
						create_record.goods_condition = shortage['goods_condition']

					create_record.save()

			for received in data['received']:
				if int(received['quantity']) > 0:
					create_record = EngageboostPurchaseOrderReceivedProductDetails.objects.create(website_id=postdata['website_id'], 
																							total_quantity=data['total_quantity'],
																							purchase_order_id=postdata['purchase_order_id'],
																							purchase_order_product_id=EngageboostPurchaseOrderProducts.objects.get(purchase_order_id=postdata['purchase_order_id'],product_id=data['product_id']).id,
																							purchase_order_received_id=postdata['purchase_order_received_id'],
																							created=now_utc, modified=now_utc,
																							isblocked='n', isdeleted='n')

					create_record.received_quantity = received['quantity']
					# if received['received_date'] != "" and received['received_date'] != None:
					create_record.received_date = data['received_date']
					if received['expiry_date'] != "" and received['expiry_date'] != None:
						create_record.expiry_date = received['expiry_date']
					if received['expiry_issue_comment'] != "" and received['expiry_issue_comment'] != None:
						create_record.expiry_issue_comment = received['expiry_issue_comment']
					if received['expiry_issue'] != "" and received['expiry_issue'] != None:
						create_record.expiry_issue = received['expiry_issue']
					if received['lot_no'] != "" and received['lot_no'] != None:
						create_record.lot_no = received['lot_no']
						if lot_count == 0:
							lot_no = received['lot_no']
							lot_count = lot_count + 1
					if received['rack_no'] != "" and received['rack_no'] != None:
						create_record.rack_no = received['rack_no']
						if rack_count == 0:
							rack_no = received['rack_no']
							rack_count = rack_count + 1

					if received['manufactured_date'] != "" and received['manufactured_date'] != None:
						create_record.manufactured_date = received['manufactured_date']

					if received['remarks'] != "" and received['remarks'] != None:
						create_record.remarks = received['remarks']

					if received['price'] != "" and received['price'] != None:
						create_record.price = received['price']

					if received['discount'] != "" and received['discount'] != None:
						create_record.discount = received['discount']

					if received['goods_condition'] != "" and received['goods_condition'] != None:
						create_record.goods_condition = received['goods_condition']

					create_record.save()
				received_quantity = received_quantity + int(received['quantity'])

			#========================================== Grn Send ========================================
			company_db = loginview.db_active_connection(request)
			payment_due_date_time=''
			purchase_order_id=request.data['purchase_order_id']

			warehouse_id=EngageboostPurchaseOrders.objects.filter(id=postdata['purchase_order_id']).last().warehouse_id
			
			pur_id=EngageboostPurchaseOrdersReceived.objects.using(company_db).get(purchase_order_master_id=purchase_order_id)
			order_count=EngageboostPurchaseOrderReceivedProducts.objects.using(company_db).filter(purchase_order_received_id=pur_id.id).count()
			if order_count >0:
				EngageboostPurchaseOrderReceivedProducts.objects.using(company_db).filter(purchase_order_received_id=pur_id.id).delete()
			EngageboostPurchaseOrdersReceived.objects.filter(purchase_order_master_id=purchase_order_id).update(status='r')
			EngageboostPurchaseOrders.objects.using(company_db).filter(id=purchase_order_id).update(status=status)


			create_po_received_product = EngageboostPurchaseOrderReceivedProducts.objects.using(company_db).create(purchase_order_received_id=postdata['purchase_order_received_id'],received_date=data['received_date'],	\
				product_id=data['product_id'],quantity=received_quantity,damage=damaged_quantity,total_qty=data['total_quantity'],shortage=shortage_quantity, lot_no=lot_no, rec_no=rack_no)

			prv_stock=EngageboostProductStocks.objects.using(company_db).get(warehouse_id=warehouse_id,product_id=data['product_id'])
			curr_stock=int(prv_stock.stock)+received_quantity
			real_stock=int(curr_stock)-int(prv_stock.safety_stock)
			EngageboostProductStocks.objects.using(company_db).filter(warehouse_id=warehouse_id,product_id=data['product_id']).update(safety_stock=prv_stock.safety_stock,\
				stock=curr_stock,real_stock=real_stock)

			#========================================== Grn Send ========================================
		return Response({'status':1, "Message":"Records Added Successfully"})

@postpone
def upload_temp_stock(request,id):
	import datetime
	post_data = request.data
	website_id = post_data['website_id']
	company_id = post_data['company_id']
	company_db = loginview.db_active_connection(request)
	stock_files_cond = EngageboostImportStockFiles.objects.using(company_db).filter(id=id ,website_id=website_id,company_id=company_id,imported_status='N',is_deleted='N',queue_no__gt=0).first()
	if stock_files_cond:
		stock_files = ImportStockFilesSerializer(stock_files_cond,partial=True)

		if stock_files.data['file_type'] == 'xls':
			FileName = stock_files.data['file_name']
			fs=FileSystemStorage()
			filename = 'importfile/product_stock_file/'+FileName
			uploaded_file_url = fs.url(filename)
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

			csvReader = xlrd.open_workbook(settings.BASE_DIR+uploaded_file_url)

			sheet = csvReader.sheet_by_index(0)
			length=len(sheet.col_values(0))
			arr_message=[]
			for x in range(length):
				try:
					if(sheet.col_values(0)[x]=='Warehouse Code'):
						pass
					else:						
						warehouse_code=sheet.col_values(0)[x]

						sku=sheet.col_values(1)[x]
						quantity=sheet.col_values(2)[x]
						# action_qty=sheet.col_values(3)[x]
						safety_stock=sheet.col_values(3)[x]
						# real_stock=sheet.col_values(5)[x]
						lot_number=sheet.col_values(4)[x]
						rack_number=sheet.col_values(5)[x]

						if lot_number=="" or lot_number==None:
							lot_number = 0
						if rack_number=="" or rack_number==None:
							rack_number = 0	
						if safety_stock=="" or safety_stock==None:
							safety_stock = 0	
						if quantity=="" or quantity==None:
							quantity = 0

						has_record = EngageboostImportedTempProductStocks.objects.last()
						if has_record:
							last_entry_of_table = EngageboostImportedTempProductStocks.objects.order_by('-id').latest('id')
							row_id = int(last_entry_of_table.id)+int(1)
						else:
							row_id = 1

						current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()

						try:
							sku = str(sku).split('.')
							sku = sku[0]
						except:
							pass

						try:
							warehouse_code = str(warehouse_code).split('.')
							warehouse_code = warehouse_code[0]
						except:
							pass		
						print("======================",company_db,warehouse_code,sku,quantity,safety_stock,lot_number,rack_number,company_id,website_id,current_time,stock_files.data['id'])
						common.update_db_sequences("imported_temp_product_stocks")
						
						stock_temp_data = EngageboostImportedTempProductStocks.objects.using(company_db).create(warehouse_name=warehouse_code,sku=sku,quantity=quantity,lot_number=lot_number,rack_number=rack_number,safety_stock=safety_stock,error_log='',company_id=company_id,website_id=website_id,is_imported=0,imported_on=current_time,stock_file_imorted_id=stock_files.data['id'])

						if stock_temp_data:
							last_stock_temp_data_id = stock_temp_data.id
							# EngageboostImportStockFiles.objects.filter(id=stock_files.data['id']).update(imported_status="Y")
							EngageboostImportStockFiles.objects.filter(id=stock_files.data['id']).delete()
							data = {"status":1,"api_response":last_stock_temp_data_id,"message":"Success"}
						else:
							data = {"status":1,"api_response":"Failed","message":"Failed"}
				except:
					pass			
	return 1	

@csrf_exempt
def product_stock_cron():
	import datetime
	datas=[]
	stock_files_cond = EngageboostImportStockFiles.objects.filter(live_stock_updated='N',is_deleted='N').all()

	if stock_files_cond:
		for item in stock_files_cond:
			stock_files = ImportStockFilesSerializer(item,partial=True)
			print('=========',stock_files.data['id'])
			website_id = stock_files.data['website_id']
			company_id = stock_files.data['company_id']
			EngageboostImportStockFiles.objects.filter(id=stock_files.data['id']).update(live_stock_updated="Y")
			# return Response(stock_files.data)

			if stock_files.data['stock_import_type'] == 'Append':
				# temp_stock_file_condition = EngageboostImportedTempProductStocks.objects.using(company_db).all().filter(stock_file_imorted_id=stock_files.data['id'],is_imported='N')
				temp_stock_file_condition = EngageboostImportedTempProductStocks.objects.all().filter(stock_file_imorted_id=stock_files.data['id'],is_imported='N')
				print(temp_stock_file_condition.query)
				if temp_stock_file_condition:				
					stock_temp_files_datas = ImportedTempProductStocksSerializer(temp_stock_file_condition,many=True)

					for stock_temp_files_data in stock_temp_files_datas.data:
						# return Response(stock_temp_files_data['sku'])
						try:
							stock_temp_files_data['sku'] = stock_temp_files_data['sku'].split('.')
							stock_temp_files_data['sku'] = stock_temp_files_data['sku'][0]
						except:
							pass
						product_condition =  EngageboostProducts.objects.filter(sku=stock_temp_files_data['sku'],website_id=website_id,isdeleted='n',status='n').first()  
						
						if product_condition:
							product_details = BasicinfoSerializer(product_condition,partial=True)
							product_id = product_details.data['id']
						else:
							product_id = 0

						warehouse_condition = EngageboostWarehouseMasters.objects.filter(code=stock_temp_files_data['warehouse_name'],website_id=website_id,isdeleted='n').first()
						if warehouse_condition:
							warehouse_data = WarehousemastersSerializer(warehouse_condition,partial=True)
							warehouse_id = warehouse_data.data['id']	
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
								check_stock_data = StockSerializer(prd_stock_condition,partial=True)
								if check_stock_data.data['virtual_stock'] != '':
									virtual_stock = check_stock_data.data['virtual_stock']
								else:
									virtual_stock =  0

								total_valid_qty = virtual_stock+safety_stock;
								real_stock = ((quantity+check_stock_data.data['stock'])-(virtual_stock+check_stock_data.data['safety_stock']+safety_stock))
								safety_stock = safety_stock+check_stock_data.data['safety_stock']
								quantity = quantity+check_stock_data.data['stock']

								serializer_data = dict()
								current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
								d1={"product_id":product_id,"warehouse_id":warehouse_id,"stock":quantity,"safety_stock":safety_stock,"real_stock":real_stock,"islot":lot_number,"islabel":rac_number,"modified":str(current_time)}
								serializer_data=dict(serializer_data,**d1)

								product_stock_table_id = EngageboostProductStocks.objects.get(id=check_stock_data.data['id'])
								serializer = StockSerializer(product_stock_table_id, data=serializer_data,partial=True)
								if serializer.is_valid():
									serializer.save()
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
								d1={"product_id":product_id,"warehouse_id":warehouse_id,"stock":quantity,"safety_stock":safety_stock,"real_stock":real_stock,"islot":lot_number,"islabel":rac_number,"created":current_time,"modified":current_time}
								serializer_data=dict(serializer_data,**d1)

								serializer = StockSerializer(data=serializer_data,partial=True)
								if serializer.is_valid():
									serializer.save()
									data ={'status':1,'api_status':serializer.data['id'],'message':'Stock Inserted'}
								else:
									data ={'status':0,'api_status':serializer.errors,'message':'Error Occured In Insert'}

								datas.append(data)
								# return Response(data)
							EngageboostImportedTempProductStocks.objects.filter(id=stock_temp_files_data['id']).update(is_imported="Y")
						else:
							data ={'status':0,'api_status':'Error Occured','message':'Either product is not exists or warehouse is not exists or error in quantity'}
							datas.append(data)
							# return Response(data)

		if datas:
			data ={'status':1,'api_status':datas}
		else:
			data ={'status':0,'api_status':datas}
		return JsonResponse(data)

	else:
		data ={'status':1,'api_status':'No Temporary Stock','message':'No Temporary Stock'}
		return JsonResponse(data)
	# else:
	# 	data ={'status':0,'api_status':'All Stock Files Imported','message':'All Stock Files Imported'}
	# 	return Response(data)

# class ProductPriceUpdate(generics.ListAPIView):
# 	def post(self, request, format=None,many=True):

class ProductStockUpdate(generics.ListAPIView):
	def post(self, request, *args, **kwargs):
		print("request============", request.data)
		user                = request.user
		user_id             = user.id
		warehouse_id 	= request.data['warehouse_id']
		product_id 		= request.data['product_id']
		quantity = 0
		lot_number = 0
		rac_number = 0
		datas = []
		try:
			if request.data.get('stock'):
				quantity = request.data.get('stock')
			else:
				quantity = 0
		except Exception as error:
			quantity = 0
		safety_stock = 0
		# stock 			= request.data['stock']
		if int(product_id) > 0 and int(warehouse_id) > 0 and int(quantity) > 0:
			prd_stock_condition = EngageboostProductStocks.objects.filter(product_id=product_id,warehouse_id=warehouse_id).first()
			if prd_stock_condition:
				check_stock_data = StockSerializer(prd_stock_condition,partial=True)
				if check_stock_data.data['virtual_stock'] != '':
					virtual_stock = check_stock_data.data['virtual_stock']
					safety_stock = check_stock_data.data['safety_stock']
				else:
					virtual_stock =  0
					safety_stock = 0

				total_valid_qty = virtual_stock+safety_stock;
				real_stock = ((quantity+check_stock_data.data['stock'])-(virtual_stock+check_stock_data.data['safety_stock']+safety_stock))
				safety_stock = safety_stock+check_stock_data.data['safety_stock']
				quantity = quantity+check_stock_data.data['stock']

				serializer_data = dict()
				current_time = datetime.now(timezone.utc).astimezone()
				d1={"product_id":product_id,"warehouse_id":warehouse_id,"stock":quantity,"safety_stock":safety_stock,"real_stock":real_stock,"islot":lot_number,"islabel":rac_number,"modified":str(current_time)}
				serializer_data=dict(serializer_data,**d1)

				product_stock_table_id = EngageboostProductStocks.objects.get(id=check_stock_data.data['id'])
				serializer = StockSerializer(product_stock_table_id, data=serializer_data,partial=True)
				if serializer.is_valid():
					serializer.save()
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

				serializer_data = dict()
				current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
				d1={"product_id":product_id,"warehouse_id":warehouse_id,"stock":quantity,"safety_stock":safety_stock,"real_stock":real_stock,"islot":lot_number,"islabel":rac_number,"created":current_time,"modified":current_time}
				serializer_data=dict(serializer_data,**d1)

				serializer = StockSerializer(data=serializer_data,partial=True)
				if serializer.is_valid():
					serializer.save()
					data ={'status':1,'api_status':serializer.data['id'],'message':'Stock Inserted'}
				else:
					data ={'status':0,'api_status':serializer.errors,'message':'Error Occured In Insert'}

				datas.append(data)
				# return Response(data)
		else:
			if int(quantity)<=0:
				serializer_data = dict()
				current_time = datetime.now()
				d1={"stock":quantity,"safety_stock":0,"real_stock":0,"islot":lot_number,"islabel":rac_number,"created":current_time,"modified":current_time}
				EngageboostProductStocks.objects.filter(product_id=product_id, warehouse_id=warehouse_id).update(**d1)
				data ={'status':1,'api_status':'Stock Updated','message':'Stock Updated'}
			else:
				data ={'status':0,'api_status':'Error Occured','message':'Either product is not exists or warehouse is not exists or error in quantity'}
			datas.append(data)
		
		if product_id>0:
			common.save_data_to_elastic(product_id,"EngageboostProducts")

		if datas:
			data ={'status':1,'api_status':datas}
		else:
			data ={'status':0,'api_status':datas}
		return Response(data)

class ProductPriceUpdate(generics.ListAPIView):
	def post(self, request, *args, **kwargs):
		user                = request.user
		user_id             = user.id
		warehouse_id 	= request.data['warehouse_id']
		product_id 		= request.data['product_id']
		price_tye_id 	= request.data['price_tye_id']
		price           = request.data['price']
		
		if price is None or price =='':
			price = 0
		
		if price_tye_id is None or price_tye_id =='':
			price_tye_id = 1
		start_date = datetime.now(timezone.utc).astimezone()
		end_date = datetime.now(timezone.utc).astimezone()
		if int(product_id) > 0 and int(warehouse_id) > 0 and int(price_tye_id) >= 0:
			rs_price = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=product_id, warehouse_id = warehouse_id, product_price_type_id__price_type_id=price_tye_id).all()
			if rs_price:
				for pricedata in rs_price:
					# -----Binayak Start-----#
					EngageboostChannelCurrencyProductPrice.objects.filter(id=pricedata.id).update(price=price, cost=price, mrp=price)
					# -----Binayak End-----#
				data ={'status':1,'api_status':'Price Updated','message':'Price Updated'}
			else:
				#-----Binayak Start-----#
				price_type_id = 1
				minqty=0
				maxqty=0
				prcObj = EngageboostProductPriceTypeMaster.objects.filter(product_id=product_id,website_id=1,price_type_id=price_type_id)
				if prcObj.count()==0:
					price_data = {
						"name" : "Regular Price",
						"product_id" : product_id,
						"website_id" : 1,
						"warehouse_id": warehouse_id,
						"price_type_id": price_type_id,
						"min_quantity": minqty,
						"max_quantity": maxqty,
						"created": datetime.now(timezone.utc).astimezone(),
						"modified": datetime.now(timezone.utc).astimezone()
					}
					priceLatest = EngageboostProductPriceTypeMaster.objects.create(**price_data)
				else:
					priceLatest = prcObj.order_by("id").first()
					latestWarehouse_id = priceLatest.warehouse_id
					if latestWarehouse_id!="" and latestWarehouse_id!=None:
						latestWarehouse_id = latestWarehouse_id.split(',')
						if str(warehouse_id) not in latestWarehouse_id:
							latestWarehouse_id.append(str(warehouse_id))
						# print("Here============",latestWarehouse_id)
						latestWarehouse_id = ",".join(latestWarehouse_id)
					else:
						latestWarehouse_id = warehouse_id
					EngageboostProductPriceTypeMaster.objects.filter(id=priceLatest.id).update(warehouse_id=latestWarehouse_id)	
				price_d = {"channel_id":6, "product_id":product_id, "price":price, "max_quantity":maxqty,"warehouse_id":warehouse_id, "website_id":1, "product_price_type_id":priceLatest.id,
				"cost":price, "min_quantity":minqty, "end_date":end_date, "mrp":price,
				"start_date":start_date
				}
				try:
					objcurr = EngageboostChannelCurrencyProductPrice.objects.create(**price_d)
				except Exception as ex:
					print(ex)

				data = {'status': 1, 'api_status': 'Price Updated', 'message': 'Price Updated'}
				# -----Binayak End-----#
		else:
			data ={'status':0,'api_status':'Error Occured','message':'Either product is not exists or warehouse is not exists or error in price'}
		if product_id>0:
			common.change_product_price_elastic(product_id)
			# price_data = common.get_channel_currency_product_price(product_id)
			# common.change_field_value_elastic(product_id,'EngageboostProducts',{"channel_currency_product_price":price_data})
			# common.save_data_to_elastic(product_id,"EngageboostProducts")	
		return Response(data)


class CheckDuplicatePrice(generics.ListAPIView):
	def post(self, request, *args, **kwargs):
		products_arr = [
			9802,
			16284,
			11994,
			12149,
			7045,
			9874,
			5683,
			14686,
			5896,
			11796,
			13610,
			14610,
			10118,
			12188,
			5758,
			17479,
			3574,
			4915,
			9292,
			6912,
			7176,
			4010,
			17826,
			4667,
			17008,
			15158,
			7494,
			13745,
			10024,
			5770,
			14194,
			13728,
			14262,
			6612,
			17692,
			6672,
			5884,
			4372,
			7489,
			16835,
			10560,
			9832,
			4072,
			17431,
			8479,
			17877,
			5647,
			8576,
			17613,
			16807,
			8351,
			5876,
			9854,
			14013,
			9073,
			15802,
			9789,
			4900,
			4417,
			7356,
			9971,
			13609,
			10345,
			13961,
			13919,
			13622,
			14591,
			5613,
			14015,
			8510,
			8565,
			6696,
			6873,
			13813,
			9257,
			13687,
			4965,
			5793,
			14230,
			4537,
			13750,
			6634,
			9270,
			10168,
			14158,
			11517,
			5079,
			14731,
			10556,
			10055,
			10112,
			16872,
			7371,
			6797,
			4890,
			16169,
			7036,
			5636,
			11519,
			16864,
			8696,
			16518,
			17698,
			18035,
			7605,
			30590,
			14538,
			5874,
			15303,
			14263,
			5473,
			3822,
			4486,
			5651,
			17660,
			4694,
			7177,
			17088,
			12066,
			13821,
			12545,
			7010,
			11452,
			4909,
			5773,
			13577,
			7714,
			13494,
			11346,
			5577,
			6937,
			4547,
			14899,
			16709,
			3657,
			4701,
			5806,
			9139,
			13605,
			14678,
			11758,
			3821,
			6666,
			9023,
			4604,
			7407,
			7241,
			16223,
			11639,
			11744,
			3689,
			8713,
			7015,
			13574,
			11313,
			5314,
			4884,
			14222,
			10335,
			14272,
			9846,
			16005,
			3609,
			10537,
			8990,
			14605,
			14290,
			5628,
			15249,
			14243,
			4013,
			4096,
			16366,
			5622,
			7444,
			7331,
			10170,
			11023,
			5759,
			17550,
			7656,
			4052,
			11944,
			7086,
			7079,
			10109,
			11845,
			8595,
			9123,
			13971,
			13730,
			7002,
			15843,
			5013,
			5137,
			13682,
			14526,
			12073,
			5918,
			15734,
			4351,
			8460,
			16305,
			14164,
			5456,
			16599,
			15156,
			5076,
			17517,
			6840,
			6641,
			4374,
			4343,
			4614,
			12551,
			8932,
			5413,
			7581,
			7403,
			15897,
			12582,
			14898,
			13613,
			16828,
			13729,
			9203,
			11640,
			7262,
			9271,
			9452,
			14200,
			8320,
			15145,
			12103,
			16226,
			14999,
			10054,
			5312,
			9865,
			17815,
			9256,
			13678,
			5655,
			3809,
			7644,
			4022,
			17385,
			3996,
			8561,
			16469,
			5645,
			11448,
			5005,
			14016,
			13727,
			11372,
			4080,
			8948,
			10576,
			12576,
			9130,
			7034,
			5334,
			16025,
			13936,
			7168,
			7948,
			7790,
			7038,
			4985,
			16126,
			6661,
			9948,
			10349,
			18030,
			13485,
			11689,
			9622,
			14600,
			9999,
			6637,
			5578,
			5434,
			16810,
			12081,
			8163,
			6838,
			5159,
			9928,
			5385,
			7135,
			14276,
			17929,
			5188,
			5072,
			4631,
			6831,
			7418,
			13533,
			17862,
			8404,
			5618,
			5469,
			12270,
			3582,
			9800,
			5313,
			17083,
			5785,
			15919,
			11742,
			5457,
			10361,
			5026,
			13698,
			10392,
			15774,
			8852,
			11142,
			9133,
			10174,
			15704,
			4067,
			11353,
			10044,
			9155,
			14199,
			15250,
			11739,
			9261,
			7073,
			13527,
			11350,
			9782,
			7495,
			11399,
			17750,
			8694,
			16793,
			3763,
			10357,
			16854,
			15219,
			5040,
			13778,
			14244,
			17489,
			8255,
			4702,
			14513,
			12181,
			9126,
			12578,
			8781,
			11547,
			7231,
			16354,
			5278,
			5318,
			4476,
			8790,
			4490,
			30701,
			16287,
			8539,
			8905,
			17693,
			14282,
			17615,
			6850,
			15506,
			15888,
			13774,
			5689,
			10201,
			30679,
			16865,
			13693,
			8034,
			5266,
			15898,
			16794,
			15912,
			4980,
			10483,
			16240,
			11312,
			7468,
			7209,
			8478,
			11655,
			9064,
			5955,
			7013,
			17551,
			9611,
			13990,
			7258,
			16024,
			9859,
			4110,
			5154,
			8614,
			17102,
			3803,
			12546,
			8032,
			10065,
			14161,
			4978,
			8808,
			6633,
			8690,
			8318,
			8461,
			5617,
			5825,
			3559,
			5889,
			11915,
			13567,
			10213,
			4887,
			13697,
			7040,
			17636,
			17334,
			5753,
			6866,
			16812,
			14279,
			13499,
			4976,
			5762,
			8592,
			14902,
			14031,
			14218,
			10022,
			5420,
			7204,
			13763,
			13520,
			7540,
			9249,
			12564,
			5534,
			12828,
			8345,
			6675,
			4790,
			17496,
			9158,
			4092,
			13752,
			8866,
			5971,
			7425,
			10585,
			3768,
			11283,
			7322,
			8800,
			11846,
			7317,
			7978,
			14275,
			4894,
			5390,
			8616,
			7041,
			13616,
			5642,
			17696,
			11685,
			8925,
			11031,
			16588,
			8630,
			18085,
			14668,
			11721,
			5381,
			7125,
			17554,
			17015,
			11643,
			5206,
			15248,
			11660,
			7391,
			8356,
			6888,
			15328,
			13652,
			15801,
			5594,
			7311,
			10350,
			7124,
			12163,
			10545,
			7410,
			8273,
			10091,
			9160,
			16601,
			16249,
			5399,
			17444,
			5769,
			5481,
			9974,
			8674,
			9867,
			5053,
			14718,
			5135,
			4727,
			5794,
			14189,
			17475,
			12568,
			14165,
			12550,
			7184,
			9558,
			30099,
			7138,
			17251,
			11682,
			14219,
			7976,
			5946,
			7783,
			14187,
			18059,
			8918,
			11494,
			5415,
			14688,
			4016,
			3775,
			30413,
			3825,
			9534,
			8343,
			10593,
			9630,
			10557,
			14522,
			12635,
			14024,
			3986,
			14278,
			8330,
			17236,
			13775,
			17697,
			8919,
			13854,
			5996,
			9596,
			12162,
			5459,
			8862,
			13999,
			16814,
			16678,
			14240,
			10336,
			7344,
			16520,
			17713,
			11865,
			8487,
			11334,
			9852,
			5890,
			13962,
			16604,
			5560,
			7492,
			14110,
			9209,
			16792,
			6833,
			13935,
			13571,
			3559,
			5429,
			4599,
			4443,
			17110,
			10586,
			8243,
			10063,
			16908,
			9086,
			13475,
			6865,
			9125,
			14648,
			16874,
			8913,
			9560,
			8450,
			5756,
			5219,
			11459,
			11738,
			11932,
			13663,
			12059,
			9987,
			11679,
			5634,
			3992,
			5782,
			8920,
			16679,
			14203,
			11341,
			17640,
			10542,
			5981,
			13495,
			5620,
			7598,
			9843,
			4889,
			14890,
			16781,
			7012,
			11513,
			8861,
			11560,
			13740,
			8157,
			4910,
			5411,
			11460,
			7080,
			7397,
			8377,
			7219,
			6841,
			16037,
			4056,
			17432,
			10102,
			6758,
			7099,
			12072,
			16699,
			8583,
			11440,
			8547,
			8632,
			9842,
			7557,
			5632,
			4379,
			9032,
			10062,
			4070,
			10189,
			7571,
			5596,
			6984,
			8599,
			9164,
			13484,
			4483,
			14567,
			13909,
			17140,
			10216,
			8244,
			16315,
			15815,
			5023,
			6721,
			13751,
			14493,
			12567,
			9055,
			7239,
			14635,
			5589,
			12011,
			7047,
			5954,
			8586,
			16695,
			15159,
			11376,
			14231,
			6866,
			5297,
			30584,
			13882,
			12654,
			14676,
			12068,
			10493,
			5818,
			16606,
			10479,
			13948,
			12002,
			9282,
			4370,
			16430,
			10135,
			3797,
			8757,
			13490,
			13651,
			13767,
			14227,
			8838,
			7084,
			3558,
			12585,
			4984,
			5581,
			15191,
			9052,
			9278,
			7421,
			9739,
			13933,
			13766,
			10205,
			7404,
			9029,
			4122,
			7524,
			5784,
			13937,
			14213,
			11304,
			10578,
			4952,
			4905,
			14614,
			4461,
			6986,
			18099,
			9280,
			13950,
			14210,
			16861,
			5816,
			12638,
			17547,
			30677,
			10202,
			13685,
			4015,
			3607,
			7095,
			8658,
			17305,
			5887,
			11651,
			17485,
			14637,
			13518,
			11996,
			4097,
			3645,
			5386,
			16788,
			9530,
			4814,
			17384,
			5926,
			8158,
			15681,
			11646,
			4125,
			5598,
			9954,
			7820,
			3819,
			16744,
			7487,
			5267,
			7486,
			16286,
			6771,
			18107,
			13924,
			10489,
			4641,
			6612,
			9870,
			13617,
			9612,
			5855,
			15720,
			6761,
			16082,
			6995,
			10072,
			14217,
			6630,
			8904,
			5603,
			8347,
			7005,
			10113,
			7389,
			10333,
			7243,
			5034,
			16134,
			17235,
			13993,
			8931,
			5611,
			11351,
			18029,
			8846,
			8317,
			17374,
			14223,
			13708,
			6872,
			7954,
			10575,
			4071,
			13674,
			10555,
			9369,
			10030,
			12006,
			10088,
			9069,
			4556,
			9879,
			12007,
			5325,
			9022,
			5599,
			17084,
			4648,
			17335,
			7119,
			11641,
			9845,
			5038,
			8629,
			11366,
			7658,
			7676,
			8811,
			3731,
			12177,
			14510,
			5605,
			13712,
			7786,
			5409,
			10190,
			4718,
			7416,
			16308,
			4086,
			8624,
			17852,
			14888,
			13723,
			6693,
			7366,
			8443,
			15721,
			13925,
			7194,
			5593,
			9067,
			8319,
			17694,
			5022,
			9145,
			6875,
			4822,
			9765,
			9711,
			9245,
			9031,
			4898,
			17714,
			16957,
			8429,
			8687,
			7350,
			5322,
			3788,
			17653,
			11328,
			7565,
			9116,
			8956,
			5374,
			8579,
			17853,
			11667,
			5280,
			12150,
			14604,
			16012,
			10488,
			3581,
			8222,
			8522,
			7094,
			8688,
			13593,
			14657,
			18032,
			14541,
			12187,
			12553,
			7496,
			11571,
			6985,
			17658,
			14003,
			16252,
			6889,
			13529,
			5788,
			5372,
			5304,
			4712,
			14603,
			9197,
			15515,
			4966,
			9305,
			10481,
			5231,
			14241,
			14504,
			11670,
			4677,
			16018,
			17639,
			16036,
			6657,
			3778,
			13681,
			15799,
			7017,
			6715,
			5339,
			12886,
			12174,
			16720,
			5249,
			11397,
			8475,
			11028,
			8933,
			6670,
			5760,
			16851,
			11503,
			5860,
			8560,
			9044,
			7181,
			9829,
			13738,
			9250,
			10539,
			17796,
			14215,
			7555,
			7042,
			14691,
			5380,
			4864,
			16603,
			17681,
			11030,
			5321,
			9702,
			11255,
			5653,
			30696,
			8509,
			6730,
			17027,
			4046,
			4736,
			14618,
			13477,
			5425,
			11393,
			6896,
			4505,
			17915,
			16877,
			9398,
			5183,
			10566,
			13965,
			5355,
			9890,
			10181,
			4442,
			4527,
			13770,
			9943,
			9740,
			7424,
			7498,
			4640,
			6982,
			6880,
			9422,
			7792,
			5084,
			13916,
			14188,
			10079,
			17476,
			16894,
			4529,
			13679,
			11045,
			11463,
			7075,
			6702,
			14623,
			17791,
			6895,
			12554,
			6667,
			7154,
			10577,
			7188,
			5423,
			11914,
			14620,
			16804,
			10046,
			13519,
			16328,
			11017,
			9041,
			10478,
			10042,
			10613,
			7784,
			8577,
			16422,
			30593,
			13590,
			11037,
			14905,
			11677,
			15504,
			13602,
			9616,
			4440,
			8999,
			14631,
			3560,
			14486,
			10551,
			12648,
			7697,
			16508,
			17094,
			5540,
			6737,
			11332,
			11410,
			9678,
			10207,
			14896,
			17074,
			13704,
			13921,
			3557,
			5982,
			4066,
			12588,
			11038,
			5294,
			7216,
			17427,
			5893,
			8480,
			14207,
			13903,
			9381,
			11927,
			8315,
			9533,
			5377,
			4977,
			3820,
			14611,
			12173,
			5778,
			5863,
			9675,
			9276,
			16384,
			7584,
			4642,
			8564,
			30676,
			7558,
			4356,
			7060,
			14684,
			5281,
			7312,
			13718,
			11456,
			14636,
			9136,
			12067,
			5772,
			13691,
			5303,
			11937,
			5917,
			10610,
			13982,
			8477,
			16869,
			13758,
			8618,
			13680,
			11606,
			4993,
			13981,
			8376,
			11630,
			16836,
			5623,
			5606,
			5081,
			7386,
			8572,
			5615,
			13611,
			4555,
			4408,
			4436,
			14659,
			5602,
			14562,
			11928,
			4670,
			6704,
			17638,
			30656,
			5275,
			5277,
			11741,
			9606,
			6725,
			5846,
			16780,
			11636,
			10501,
			17495,
			8894,
			9272,
			10346,
			13757,
			9279,
			5862,
			30698,
			14448,
			7011,
			12572,
			14643,
			17011,
			4958,
			30187,
			12561,
			9161,
			8683,
			18039,
			14257,
			7530,
			11848,
			9595,
			14647,
			18031,
			4517,
			5776,
			5580,
			9504,
			14211,
			6663,
			8482,
			9955,
			17447,
			8211,
			14689,
			5143,
			16857,
			16071,
			13594,
			16020,
			4502,
			5344,
			5583,
			8168,
			12195,
			7586,
			8929,
			17641,
			17563,
			13902,
			13734,
			10049,
			5952,
			16579,
			7162,
			7179,
			9613,
			7343,
			10337,
			5065,
			10122,
			8336,
			18021,
			7398,
			10212,
			9283,
			11936,
			6769,
			7457,
			17543,
			7076,
			4961,
			5763,
			17058,
			13797,
			14598,
			4061,
			8457,
			18087,
			7711,
			7352,
			8602,
			6695,
			17446,
			9790,
			4732,
			11363,
			18062,
			7539,
			10424,
			4638,
			12175,
			4886,
			11642,
			6788,
			4908,
			8201,
			6987,
			12581,
			16791,
			6644,
			10180,
			17390,
			4650,
			5237,
			7245,
			14545,
			7947,
			4347,
			13595,
			10409,
			10360,
			9106,
			4435,
			9831,
			10032,
			16600,
			9025,
			14563,
			13798,
			5875,
			7149,
			4357,
			13597,
			17695,
			30678,
			8540,
			9942,
			11441,
			5925,
			4691,
			16011,
			5405,
			9152,
			5619,
			10482,
			16250,
			9538,
			3593,
			13686,
			11769,
			11781,
			17107,
			8562,
			7573,
			6690,
			6665,
			8224,
			14602,
			11331,
			17441,
			6674,
			13954,
			11358,
			10498,
			7052,
			12170,
			8859,
			9884,
			16276,
			12563,
			6685,
			7735,
			5967,
			16521,
			4834,
			17363,
			5246,
			12544,
			10191,
			10195,
			8803,
			10706,
			10019,
			15043,
			5966,
			7675,
			7192,
			5403,
			6595,
			14277,
			8968,
			14186,
			7347,
			17442,
			10476,
			6635,
			9708,
			6799,
			13932,
			16813,
			8030,
			6632,
			9771,
			4113,
			4706,
			14740,
			8755,
			13772,
			5798,
			16222,
			9253,
			8908,
			8695,
			16517,
			7166,
			9544,
			3559,
			3777,
			8986,
			7456,
			7393,
			12060,
			17604,
			17367,
			5720,
			8463,
			12176,
			8845,
			11487,
			11436,
			7617,
			5393,
			4644,
			10534,
			10584,
			11388,
			18013,
			9153,
			30703,
			12169,
			7127,
			8451,
			7112,
			9347,
			15736,
			15083,
			4735,
			14552,
			7688,
			5775,
			3658,
			5789,
			7476,
			17141,
			3753,
			6759,
			13539,
			5783,
			11829,
			17080,
			10544,
			4101,
			5398,
			4595,
			5452,
			9791,
			8459,
			15169,
			9821,
			13794,
			5308,
			7014,
			9797,
			3551,
			5454,
			7376,
			17690,
			8855,
			12589,
			13776,
			14685,
			9450,
			14502,
			9151,
			3991,
			3558,
			13673,
			4949,
			5110,
			12136,
			13632,
			4049,
			10597,
			5438,
			12160,
			4428,
			13714,
			10103,
			5331,
			8701,
			15203,
			9828,
			5276,
			15316,
			9150,
			15315,
			8441,
			15229,
			7720,
			11336,
			13804,
			7021,
			10004,
			8476,
			4963,
			7490,
			5049,
			4090,
			14661,
			5467,
			7123,
			11342,
			10332,
			4485,
			6772,
			5796,
			17644,
			13489,
			7956,
			4055,
			12580,
			16801,
			7564,
			5370,
			13760,
			8895,
			4526,
			14717,
			10574,
			30673,
			6625,
			16878,
			17821,
			5340,
			11780,
			4026,
			7077,
			5761,
			8594,
			16014,
			10485,
			11258,
			12579,
			13795,
			8812,
			10568,
			12565,
			9833,
			11697,
			16248,
			14612,
			15278,
			8900,
			8657,
			3742,
			4901,
			30586,
			5404,
			9827,
			30657,
			13918,
			6694,
			10583,
			11925,
			9220,
			7734,
			7355,
			12071,
			14214,
			30702,
			11481,
			14671,
			7576,
			13988,
			7488,
			15804,
			4078,
			7789,
			11301,
			10175,
			8375,
			6607,
			9274,
			10160,
			7332,
			11321,
			10614,
			17237,
			7193,
			8469,
			15634,
			4434,
			9738,
			9946,
			7395,
			11895,
			5317,
			6952,
			7307,
			4971,
			13552,
			11930,
			30699,
			7103,
			8563,
			17655,
			11438,
			4812,
			11027,
			8833,
			11647,
			4418,
			8625,
			10375,
			6920,
			14959,
			12108,
			17870,
			5289,
			9141,
			7043,
			3985,
			5287,
			7422,
			4342,
			15524,
			7172,
			5098,
			8015,
			8700,
			6971,
			16628,
			15202,
			12107,
			17766,
			5652,
			14225,
			8229,
			10351,
			4100,
			11039,
			4785,
			5097,
			3738,
			6955,
			30585,
			9760,
			6962,
			9246,
			8993,
			14128,
			10570,
			4600,
			14530,
			11896,
			10565,
			6643,
			14617,
			9913,
			7396,
			7365,
			4369,
			13587,
			13534,
			13487,
			13541,
			4974,
			16935,
			5221,
			4023,
			3667,
			17225,
			9615,
			8857,
			13476,
			15770,
			11847,
			11688,
			18061,
			17582,
			9889,
			4709,
			3559,
			5643,
			5801,
			13717,
			16013,
			6992,
			7575,
			7501,
			5039,
			13913,
			13688,
			12652,
			7373,
			11678,
			14594,
			9267,
			13992,
			14281,
			3557,
			7035,
			4525,
			9594,
			7500,
			14687,
			9066,
			7330,
			13647,
			17428,
			15196,
			13739,
			5790,
			6891,
			7944,
			8786,
			30658,
			13731,
			9607,
			14537,
			13922,
			8159,
			6966,
			8358,
			14675,
			7383,
			8458,
			13816,
			8174,
			5178,
			13634,
			5847,
			7677,
			9045,
			13675,
			8212,
			3659,
			5517,
			4882,
			4000,
			3546,
			10051,
			7089,
			30659,
			10045,
			9047,
			12235,
			13535,
			9872,
			11551,
			12056,
			16863,
			5646,
			3558,
			6684,
			8352,
			11329,
			10553,
			8177,
			9773,
			9043,
			14599,
			13513,
			14255,
			6875,
			8686,
			15803,
			11396,
			11713,
			15771,
			5994,
			13764,
			9143,
			17477,
			10358,
			16617,
			14887,
			9895,
			14588,
			16597,
			30674,
			5279,
			10176,
			10348,
			11704,
			12829,
			8544,
			10044,
			6940,
			8536,
			4017,
			5421,
			7781,
			9148,
			4548,
			17546,
			9099,
			8785,
			4528,
			3791,
			8541,
			4994,
			7787,
			10005,
			6640,
			5051,
			16667,
			9712,
			13952,
			7009,
			13777,
			3559,
			8527,
			15318,
			16006,
			5078,
			12151,
			12114,
			12042,
			9718,
			8449,
			6697,
			9131,
			11921,
			3981,
			12161,
			5341,
			4975,
			11029,
			4865,
			4339,
			4106,
			13586,
			7577,
			5600,
			8793,
			10089,
			8704,
			7372,
			9807,
			17645,
			7522,
			10502,
			7318,
			14273,
			16363,
			4637,
			7083,
			4448,
			4931,
			8247,
			17865,
			13549,
			12556,
			12047,
			3564,
			8985,
			7942,
			5142,
			13500,
			4057,
			7342,
			17691,
			10612,
			8213,
			9264,
			8570,
			7377,
			5883,
			11021,
			5120,
			13705,
			13526,
			30098,
			4796,
			16811,
			12560,
			7392,
			14646,
			9838,
			4671,
			9050,
			13684,
			11051,
			14001,
			11665,
			10595,
			9345,
			6909,
			13960,
			16091,
			17717,
			13732,
			15827,
			6845,
			16834,
			13491,
			14654,
			6664,
			5892,
			5891,
			8354,
			5484,
			11702,
			5410,
			4962,
			13974,
			16090,
			16825,
			17588,
			7497,
			4489,
			8762,
			17327,
			10028,
			8927,
			4658,
			9268,
			7185,
			3995,
			13588,
			3669,
			10507,
			7349,
			7795,
			10003,
			14613,
			14544,
			8368,
			8573,
			14509,
			7155,
			8750,
			8220,
			3994,
			11939,
			14690,
			18017,
			14229,
			6675,
			9567,
			6724,
			4470,
			3588,
			4102,
			9873,
			11635,
			9042,
			10547,
			7082,
			5837,
			8322,
			17685,
			14900,
			7152,
			14891,
			8520,
			8178,
			10564,
			4734,
			5935,
			7091,
			14266,
			11631,
			14177,
			3621,
			13538,
			17463,
			14236,
			9617,
			11050,
			14921,
			30101,
			5414,
			17392,
			9040,
			13820,
			13711,
			7459,
			6961,
			6633,
			13915,
			16094,
			10617,
			7019,
			5787,
			16921,
			5074,
			14245,
			16035,
			17252,
			4877,
			14212,
			14641,
			13589,
			9147,
			4550,
			13806,
			14032,
			11370,
			4904,
			3570,
			14529,
			16816,
			10064,
			10002,
			13537,
			5422,
			7351,
			5612,
			7316,
			5145,
			3734,
			8923,
			6877,
			7108,
			14556,
			17672,
			10011,
			7485,
			17028,
			4717,
			12012,
			11897,
			10148,
			7719,
			8353,
			4034,
			8782,
			4748,
			7587,
			4987,
			14216,
			16783,
			12651,
			13695,
			30672,
			9396,
			13599,
			9024,
			4020,
			4880,
			10009,
			13966,
			11403,
			7460,
			5923,
			4007,
			3741,
			14233,
			5144,
			9459,
			17627,
			17626,
			17646,
			4705,
			9028,
			8854,
			13604,
			4014,
			10432,
			4348,
			9137,
			3706,
			8537,
			9878,
			16527,
			6681,
			14679,
			9605,
			17501,
			13949,
			13951,
			14670,
			11338,
			4004,
			14649,
			8161,
			11457,
			5378,
			5460,
			7712,
			13815,
			5359,
			12182,
			12653,
			3602,
			17401,
			11916,
			30700,
			17382,
			15633,
			5109,
			4920,
			17377,
			9397,
			12074,
			6659,
			4414,
			14258,
			14619,
			15480,
			8410,
			7716,
			7985,
			8484,
			7169,
			12570,
			11035,
			8776,
			5610,
			10013,
			4665,
			6942,
			7505,
			11899,
			4907,
			5330,
			13826,
			7061,
			15907,
			8891,
			16598,
			17395,
			10146,
			12574,
			13989,
			9291,
			5264,
			13550,
			16674,
			5262,
			11360,
			14508,
			6735,
			5570,
			17533,
			6951,
			5871,
			7234,
			17565,
			15921,
			12598,
			7556,
			7503,
			10573,
			5795,
			30583,
			3611,
			14681,
			16722,
			7178,
			16268,
			12179,
			8452,
			11348,
			5375,
			8274,
			5458,
			17184,
			6911,
			15725,
			13779,
			14153,
			7583,
			30587,
			4743,
			8309,
			13701,
			5439,
			5616,
			7499,
			8784,
			5532,
			18046,
			16233,
			3790,
			9651,
			17538,
			17398,
			9074,
			13560,
			9293,
			14209,
			10535,
			4522,
			4535,
			4021,
			5105,
			18086,
			9563,
			12166,
			11310,
			8888,
			6950,
			11934,
			10125,
			7063,
			8626,
			11989,
			9443,
			16784,
			5607,
			4001,
			7235,
			4074,
			5845,
			10163,
			30655,
			12283,
			5604,
			13603,
			5757,
			7461,
			8584,
			7173,
			7023,
			6698,
			4069,
			16708,
			8902,
			4816,
			10563,
			11573,
			4731,
			13568,
			10211,
			5730,
			4358,
			3792,
			8839,
			16364,
			11976,
			14271,
			4511,
			4747,
			11747,
			7114,
			11756,
			5358,
			13658,
			14908,
			17013,
			13931,
			7694,
			7378,
			17383,
			17581,
			6958,
			3805,
			3795,
			7207,
			6868,
			5032,
			8528,
			14990,
			11386,
			8795,
			14269,
			4545,
			10182,
			11323,
			30653,
			13805,
			5424,
			7986,
			7156,
			17371,
			9645,
			6870,
			30326,
			17091,
			13761,
			13480,
			5536,
			14193,
			14650,
			16917,
			13814,
			7246,
			5953,
			7068,
			7186,
			6676,
			13581,
			5121,
			30233,
			10209,
			11558,
			8440,
			5856,
			7111,
			5873,
			13546,
			5802,
			6591,
			15968,
			11605,
			10085,
			4035,
			13953,
			11303,
			17462,
			17527,
			7003,
			8761,
			8601,
			13612,
			14108,
			9734,
			7030,
			17456,
			4381,
			5995,
			16771,
			10536,
			8817,
			16936,
			14267,
			8756,
			14496,
			8708,
			14204,
			17400,
			14265,
			4680,
			12037,
			9604,
			6655,
			9820,
			6629,
			6634,
			9633,
			4058,
			11913,
			13726,
			8628,
			10141,
			11359,
			15084,
			5791,
			7129,
			13746,
			10486,
			6834,
			14639,
			6645,
			7538,
			10200,
			14616,
			9565,
			9030,
			3601,
			16585,
			4082,
			7074,
			10066,
			8966,
			6617,
			14630,
			8465,
			17580,
			5433,
			5070,
			11032,
			5041,
			7788,
			5993,
			11398,
			12127,
			4099,
			9677,
			11343,
			5106,
			6832,
			4544,
			17336,
			13964,
			5315,
			16858,
			11929,
			16232,
			7256,
			8370,
			5592,
			4704,
			9834,
			3558,
			16010,
			11040,
			4091,
			3687,
			7604,
			5858,
			7791,
			5160,
			7004,
			9169,
			4911,
			9733,
			10598,
			8660,
			6873,
			7588,
			10508,
			14447,
			5538,
			17440,
			4609,
			17598,
			11808,
			7554,
			7941,
			14719,
			4350,
			11561,
			15263,
			17472,
			5356,
			15153,
			6848,
			5824,
			9178,
			14155,
			8930,
			15839,
			11920,
			10092,
			9818,
			5630,
			4707,
			5629,
			6996,
			3740,
			10377,
			13553,
			4024,
			11437,
			18034,
			6726,
			14228,
			12552,
			18095,
			13551,
			13677,
			30589,
			8566,
			13532,
			16829,
			9620,
			11843,
			13780,
			3575,
			13737,
			13742,
			4972,
			4450,
			11020,
			17795,
			16027,
			8548,
			13548,
			11993,
			12573,
			9623,
			17490,
			10219,
			14232,
			4885,
			4999,
			13706,
			8474,
			11917,
			17555,
			7523,
			5595,
			5861,
			16795,
			16860,
			10569,
			15146,
			11975,
			16815,
			10095,
			10505,
			10562,
			13765,
			8906,
			8969,
			5326,
			15147,
			10210,
			15230,
			8772,
			16798,
			5957,
			16424,
			6634,
			11779,
			8613,
			6629,
			5117,
			17925,
			15923,
			14197,
			7420,
			11288,
			3993,
			5332,
			16778,
			3783,
			17556,
			11757,
			11992,
			13744,
			11394,
			4050,
			16066,
			16358,
			9275,
			9098,
			11986,
			13709,
			4027,
			9772,
			16175,
			7367,
			14721,
			13598,
			30582,
			10587,
			11357,
			4895,
			5627,
			6732,
			5601,
			11495,
			3764,
			7618,
			5597,
			10331,
			7582,
			16237,
			10193,
			12128,
			16313,
			3566,
			7254,
			7151,
			13694,
			4366,
			14913,
			15741,
			12045,
			12003,
			7240,
			7544,
			4899,
			11373,
			14176,
			15881,
			4410,
			17949,
			14185,
			5397,
			6743,
			10007,
			9998,
			5626,
			5306,
			5035,
			8770,
			5797,
			13710,
			30592,
			7657,
			8893,
			8223,
			8615,
			3559,
			16346,
			8768,
			12057,
			8398,
			30591,
			11720,
			8507,
			5895,
			11933,
			17614,
			9689,
			4119,
			17445,
			16866,
			11374,
			17734,
			8896,
			10192,
			4373,
			13762,
			7504,
			5674,
			14261,
			13733,
			10203,
			5172,
			13676,
			5384,
			11324,
			5659,
			8886,
			10073,
			17224,
			11435,
			13713,
			7405,
			5300,
			17759,
			3567,
			17101,
			7174,
			10425,
			9554,
			9033,
			7394,
			10080,
			8659,
			5060,
			11585,
			3603,
			6842,
			17234,
			9840,
			8412,
			5419,
			5800,
			6946,
			5260,
			10082,
			14512,
			14910,
			11649,
			8436,
			16376,
			8423,
			11912,
			9048,
			9835,
			9555,
			8366,
			13817,
			30654,
			17103,
			17720,
			30588,
			9950,
			5924,
			8575,
			7018,
			9823,
			5333,
			3557,
			8344,
			8581,
			7802,
			4925,
			7475,
			7782,
			14192,
			8171,
			8582,
			8176,
			5754,
			11371,
			6921,
			3998,
			5859,
			7408,
			16942,
			5223,
			14226,
			12211,
			16403,
			16800,
			13547,
			15042,
			9142,
			14625,
			15155,
			14156,
			10541,
			7388,
			7362,
			5376,
			6878,
			7360,
			8889,
			16007,
			8364,
			13907,
			8980,
			14539,
			16016,
			4848,
			14205,
			9255,
			14224,
			6991,
			30697,
			3781,
			10071,
			7960,
			13891,
			6714,
			11349,
			11018,
			10546,
			10338,
			13743,
			17719,
			5311,
			3559,
			5635,
			16028,
			15724,
			9660,
			5395,
			17596,
			7525,
			16871,
			3786,
			18033,
			16171,
			8473,
			6679,
			11587,
			3550,
			4676,
			17183,
			11377,
			30572,
			4612,
			16246,
			10356,
			7025,
			4033,
			8864,
			14208,
			4386,
			13759,
			9929,
			3559,
			4806,
			9976,
			4591,
			4108,
			11365,
			11345,
			10099,
			16023,
			4842,
			9851,
			9458,
			13735,
			4818,
			30097,
			5470,
			7244,
			5222,
			10579,
			4460,
			4959,
			14246,
			5391,
			4951,
			5799,
			4711,
			7957,
			11043,
			5815,
			10086,
			5638,
			5296,
			12022,
			7020,
			9778,
			10512,
			9128,
			12167,
			7031,
			14220,
			7639,
			11447,
			16467,
			14674,
			4006,
			8937,
			14997,
			6898,
			10615,
			3787,
			5242,
			10446,
			5153,
			5633,
			5203,
			30234,
			17773,
			5389,
			7097,
			3800,
			6674,
			13715,
			14270,
			4005,
			8863,
			17430,
			16817,
			10641,
			10475,
			9766,
			3604,
			10050,
			5118,
			9194,
			14264,
			8468,
			4029,
			13626,
			16571,
			3808,
			8481,
			8415,
			15896,
			6639,
			7511,
			14606,
			5718,
			9289,
			13592,
			5155,
			5771,
			7674,
			9561,
			8684,
			11991,
			15705,
			5877,
			6837,
			16806,
			5428,
			16837,
			14596,
			30704,
			9853,
			14191,
			14634,
			7984,
			17014,
			13531,
			16015,
			13790,
			7645,
			13523,
			9819,
			5305,
			9850,
			7619,
			15780,
			3987,
			12178,
			15170,
			4639,
			12548,
			6644,
			10499,
			15262,
			10554,
			14488,
			11942,
			17394,
			8892,
			9336,
			7943,
			17497,
			7402,
			30580,
			7721,
			14280,
			10504,
			8911,
			4068,
			7070,
			8177,
			16850,
			17085,
			6684,
			6745,
			6965,
			14196,
			9213,
			11804,
			5369,
			6977,
			4703,
			13481,
			10014,
			4995,
			7354,
			7072,
			5396,
			16026,
			13488,
			18063,
			7180,
			11581,
			4645,
			5455,
			11919,
			17391,
			7249,
			17666,
			17647,
			13773,
			13756,
			15709,
			3666,
			17368,
			15798,
			5147,
			8585,
			5838,
			15044,
			13545,
			5719,
			4392,
			5779,
			5755,
			7502,
			7306,
			3728,
			13920,
			10370,
			13683,
			14154,
			8705,
			12104,
			12645,
			9638,
			14521,
			9758,
			5033,
			4463,
			11852,
			17194,
			5044,
			15151,
			16254,
			15792,
			5631,
			17774,
			4484,
			4344,
			5295,
			9725,
			13631,
			5557,
			5427,
			10500,
			7225,
			8578,
			5241,
			3608,
			6960,
			12586,
			7085,
			4725,
			6933,
			6929,
			10214,
			4753,
			5354,
			5383,
			17797,
			7964,
			16849,
			5412,
			17372,
			5786,
			4087,
			14557,
			30266,
			30579,
			14011,
			6677,
			8508,
			9173,
			8597,
			5817,
			8783,
			13994,
			15563,
			4441,
			17429,
			11699,
			11795,
			11406,
			5590,
			9909,
			4025,
			8780,
			3798,
			14624,
			11938,
			6644,
			4075,
			7170,
			10509,
			12087,
			5324,
			8662,
			7233,
			11609,
			7229,
			16873,
			11523,
			17876,
			14507,
			9065,
			7268,
			9891,
			7090,
			7955,
			13512,
			9263,
			7959,
			10058,
			11326,
			18065,
			4012,
			17082,
			14260,
			14242,
			8673,
			9120,
			8939,
			3824,
			17548,
			4883,
			4723,
			4783,
			4413,
			11891,
			4998,
			5885,
			14692,
			30705,
			13987,
			5657,
			13524,
			14540,
			11335,
			9562,
			17010,
			6628,
			7171,
			6613,
			17782,
			7384,
			13653,
			7785,
			4868,
			17469,
			11827,
			8559,
			17455,
			9262,
			16299,
			11302,
			11625,
			16605,
			6924,
			4953,
			14289,
			10374,
			30675,
			15165,
			14655,
			11515,
			14534,
			13741,
			8702,
			4914,
			17758,
			11803,
			7270,
			15938,
			6978,
			11450,
			8031,
			11369,
			17079,
			11555,
			11354,
			8912,
			5387,
			10167,
			13636,
			10000,
			13736,
			15008,
			13649,
			6723,
			7374,
			10096,
			5668,
			7359,
			6658,
			4710,
			16721,
			5058,
			16199,
			9417,
			6963,
			4059,
			17597,
			11867,
			16471,
			5729,
			10558,
			3823,
			12314,
			7353,
			7157,
			16696,
			11995,
			14221,
			6602,
			18057,
			11044,
			4047,
			13955,
			3610,
			6839,
			4060,
			8438,
			7616,
			7520,
			9234,
			9248,
			14615,
			17499,
			16862,
			4902,
			7572,
			7945,
			13929,
			7271,
			8275,
			5102,
			7348,
			10379,
			3562,
			4653,
			10611,
			8221,
			11671,
			6670,
			6835,
			9154,
			13912,
			13591,
			13606,
			8316,
			4437,
			10552,
			4464,
			11988,
			14259,
			5591,
			15166,
			7472,
			12137,
			13996,
			17228,
			11347,
			11926,
			10531,
			11311,
			8568,
			5765,
			6915,
			7310,
			7509,
			5431,
			5245,
			7406,
			17579,
			11616,
			6874,
			9049,
			14907,
			7543,
			8253,
			6747,
			14190,
			13967,
			16088,
			6875,
			9224,
			15742,
			8574,
			10097,
			6667,
			8791,
			13753,
			11691,
			4733,
			15307,
			10581,
			7574,
			10070,
			8865,
			13554,
			10532,
			16867,
			16056,
			30100,
			10601,
			14621,
			14286,
			5442,
			14107,
			9247,
			5894,
			11327,
			7237,
			12184,
			12640,
			5067,
			13544,
			11805,
			6998,
			17488,
			18016,
			17399,
			4488,
			9260,
			8014,
			7361,
			9822,
			14894,
			6881,
			14501,
			9806,
			7098,
			11361,
			17393,
			8991,
			3806,
			13483,
			7691,
			4742,
			8921,
			4549,
			7696,
			7345,
			17460,
			6872,
			5482,
			9076,
			14680,
			9290,
			13755,
			18064,
			10179,
			5774,
			4979,
			4917,
			7037,
			17434,
			17675,
			16570,
			9281,
			5319,
			16021,
			9869,
			11703,
			5685,
			15057,
			14677,
			7507,
			14184,
			16796,
			13596,
			7508,
			10467,
			9799,
			9046,
			15739,
			14274,
			16618,
			13725,
			30581,
			11314,
			11161,
			16677,
			7182,
			6619,
			3796,
			4589,
			5936,
			5608,
			6663,
			8569,
			12543,
			14633,
			4919,
			16689,
			5625,
			8685,
			5027,
			5268,
			11943,
			14511,
			18073,
			7541,
			13910,
			13707,
			5582,
			8767,
			5185,
			8389,
			10383,
			9699,
			16168,
			11042,
			10354,
			10477,
			11400,
			12575,
			14589,
			9273,
			15788,
			12540,
			8992,
			14607,
			5941,
			8606,
			10098,
			4530,
			15150,
			10353,
			14183,
			6621,
			17549,
			9277,
			12686,
			7071,
			13608,
			5587,
			13630,
			13624,
			9238,
			8230,
			8715,
			5240,
			7493,
			7150,
			9654,
			5298,
			11308,
			7346,
			5220,
			10533,
			5000,
			4346,
			4820,
			5707,
			9876,
			5882,
			8464,
			17386,
			7382,
			10334,
			6800,
			8538,
			10196,
			16697,
			13536,
			4929,
			4932,
			15152,
			8631,
			17100,
			13696,
			5056,
			5310,
			11586,
			17478,
			8448,
			6880,
			14515,
			5579,
			16824,
			8663,
			12186,
			4422,
			16805,
			14629,
			10352,
			16092,
			16833,
			7946,
			14168,
			6660,
			7058,
			10572,
			6699,
			5402,
			4032,
			14730,
			4891,
			3674,
			13522,
			14206,
			12005,
			11566,
			8472
		]
		allProd = EngageboostProducts.objects.filter(isdeleted='n',id__in=products_arr)
		if allProd.count()>0:
			allProd = allProd.values_list('id',flat=True)
			allProd = list(allProd)
			
			for item in allProd:
				priceTypeObj = EngageboostProductPriceTypeMaster.objects.filter(product_id = item)
				if priceTypeObj.count()>0:
					first_arr = {}
					last_arr = {}

					priceTypeObj = priceTypeObj.order_by('id')

					first_arr = priceTypeObj.values('id','name','warehouse_id').first()
					last_arr = priceTypeObj.values('id','name','warehouse_id').last()

					first_warehouse = first_arr['warehouse_id']
					first_warehouse_list = first_warehouse.split(',')

					last_warehouse = last_arr['warehouse_id']
					last_warehouse_list = last_warehouse.split(',')

					modified_warehouse_list = first_warehouse_list+last_warehouse_list

					modified_warehouse_list = list(set(modified_warehouse_list))

					modified_warehouse = ','.join(modified_warehouse_list)
					print(modified_warehouse)
					EngageboostProductPriceTypeMaster.objects.filter(id= first_arr['id']).update(warehouse_id=modified_warehouse)
					EngageboostChannelCurrencyProductPrice.objects.filter(product_price_type_id= last_arr['id'],product_id=item).delete()
					EngageboostProductPriceTypeMaster.objects.filter(id= last_arr['id']).delete()

		data = {'status': 1, 'api_status': 'Price Updated', 'message': 'Price Updated'}
		return Response(data)