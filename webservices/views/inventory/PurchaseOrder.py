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
from datetime import datetime
from rest_framework import generics
from itertools import chain
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Sum, Count
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail, get_connection
from django.core.mail.message import EmailMessage
from webservices.views import loginview
from django.shortcuts import render
# from webservices.views.common.common import num_to_words, getAutoResponderDetails, sendEmail
from webservices.views.common import common
import os
import json
from webservices.views.common import common


class PurchaseOrder(generics.ListAPIView):
# """ Add new Purchase Order Web Services """
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		now_utc = datetime.now().astimezone()
		payment_due_date_time=''
		d2=request.data['order']
		payment_time=request.data['order']['payment_due_date']
		if 'T' in str(payment_time):
			payment_due_date=str(payment_time).split("T")
			payment_due_date_time=payment_due_date[0]
			d1={'created':datetime.now().date(),'modified':datetime.now().date(),'payment_due_date':payment_due_date_time}
		else:
			d1={'created':datetime.now().date(),'modified':datetime.now().date(),'payment_due_date':payment_time}
		serializer_data=dict(d2,**d1)
		serializer = PurchaseOrderSerializer(data=serializer_data,partial=True)

		if serializer.is_valid():
			serializer.save()
			purchase_order = EngageboostPurchaseOrders.objects.using(company_db).latest('id')
			puchase_order_latest_id=purchase_order.id
			

			for product in request.data['products']:
				
				d1={'purchase_order_id':puchase_order_latest_id}
				d2=product
				EngageboostPurchaseOrderProducts.objects.create(purchase_order_id=puchase_order_latest_id,price=product['price'],discount=product['discount'],quantity=product['quantity'],discount_amount=product['discount_amount'],product_id=product['product_id'])
				common.save_po_activity(company_db,puchase_order_latest_id,now_utc,0,1,"",4,product['product_id'],serializer_data["purchase_order_id"])
				
				mappObj = EngageboostWarehouseSupplierMappings.objects.filter(warehouse_id=request.data['order']['warehouse_id'],supplier_id=request.data['order']['supplier_id'],product_id=product['product_id'])
				
				if mappObj.count()>0:	
					d3 = {
						"website_id":request.data['order']['website_id'],
						"supplier_sku":product['sku'],
						"base_cost":product['price'],
						"sale_per_pack_unit":product['price'],
						'modified':datetime.now().date()
					}
					EngageboostWarehouseSupplierMappings.objects.filter(warehouse_id=request.data['order']['warehouse_id'],supplier_id=request.data['order']['supplier_id'],product_id=product['product_id']).update(**d3)
				else:	
					d3 = {
						"warehouse_id":request.data['order']['warehouse_id'],
						"supplier_id":request.data['order']['supplier_id'],
						"website_id":request.data['order']['website_id'],
						"product_id":product['product_id'],
						"supplier_sku":product['sku'],
						"base_cost":product['price'],
						"sale_per_pack_unit":product['price'],
						'created':datetime.now().date(),
						'modified':datetime.now().date()
					}
					EngageboostWarehouseSupplierMappings.objects.create(**d3)	
				data ={
					'status':1,
					'message':'Successfully Inserted',
					}
			return Response(data)
		else:
			data ={
			'status':0,
			'error':serializer.errors,
			'message':'Data Not Found',
			}
				
			return Response(data)

class PurchaseOrderViewList(generics.ListAPIView):
# """ Edit Purchase Order Web Services """
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostPurchaseOrders.objects.using(company_db).get(pk=pk)
		except EngageboostPurchaseOrders.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None, partial=True):
		company_db = loginview.db_active_connection(request)
		website_id = 1
		pur_id = ''
		purchase_order_products = []
		global_setting= EngageboostGlobalSettings.objects.using(company_db).get(website_id=1)
		order_id = EngageboostPurchaseOrders.objects.using(company_db).count()
		new_order_id = int(order_id)+int(1)
		Order = str(global_setting.purchase_order_id_format)+str(new_order_id)
		currency_data = EngageboostCurrencyMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
		serializer_currency = CurrencyMastersSerializer(currency_data,many=True)
		Suppliers = EngageboostSuppliers.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
		serializer = SuppliersSerializer(Suppliers,many=True)
		warehouse = EngageboostWarehouseMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer_warehouse = WarehousemastersSerializer(warehouse, many=True)
		PurchaseOrders = EngageboostPurchaseOrdersShippingMethods.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer_PurchaseOrdersShippingMethods = PurchaseOrdersShippingMethodSerializer(PurchaseOrders, many=True)
		PurchaseOrdersPaymentMethods = EngageboostPurchaseOrdersPaymentMethods.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer_paymentmethods = PurchaseOrdersPaymentMethodsSerializer(PurchaseOrdersPaymentMethods, many=True)
		PurchaseOrders = EngageboostPurchaseOrders.objects.using(company_db).all().filter(id=pk)
		serializer_PurchaseOrders = PurchaseOrderSerializer(PurchaseOrders, many=True)
		purchaseordersproducts = EngageboostPurchaseOrderProducts.objects.using(company_db).all().filter(purchase_order_id=pk)
		serializer_purchaseordersproducts = PurchaseOrderProductSerializer(purchaseordersproducts, many=True)
		purchase_order_products = serializer_purchaseordersproducts.data
		
		#product = EngageboostProducts.objects.using(company_db).all().filter(isblocked='n',isdeleted='n')
		#serializer_info = BasicinfoSerializer(product,many=True)

		for productData in serializer_purchaseordersproducts.data:
			#print(json.dumps(productData, indent=4, sort_keys=True))
			purchaseordersproducts = EngageboostPurchaseOrderReceivedProductDetails.objects.using(company_db).all().filter(purchase_order_id=pk,purchase_order_product_id =productData['product']['id']).order_by('-expiry_date').all()
			PoReceivedItemDetails = EngageboostPurchaseOrderReceivedProductDetailsSerializer(purchaseordersproducts, many=True)
			#print(PoReceivedItemDetails.data)

		pur_id_count=EngageboostPurchaseOrdersReceived.objects.using(company_db).filter(purchase_order_master_id=pk).count()
		received_purchaseorder_master_id = 0
		received_purchaseorder_id = 0
		received_date = ''
		if pur_id_count >0:
			pur_id = EngageboostPurchaseOrdersReceived.objects.using(company_db).get(purchase_order_master_id=pk)
			purchase_order_count=EngageboostPurchaseOrderReceivedProducts.objects.using(company_db).filter(purchase_order_received_id=pur_id.id).count()
			if purchase_order_count > 0:
				purchaseordersproductsrecieved = EngageboostPurchaseOrderReceivedProducts.objects.using(company_db).all().filter(purchase_order_received_id=pur_id.id)
				serializer_purchaseordersreceivedproducts = PurchaseOrderReceivedProductsSerializer(purchaseordersproductsrecieved, many=True)
				purchase_order_products = []
				purchase_order_products = serializer_purchaseordersreceivedproducts.data

			received_purchaseorder_master_id = pur_id.id
			received_date = pur_id.received_date
			received_purchaseorder_id = pur_id.received_purchaseorder_id
		data = {
			'status':1,
			'currency':serializer_currency.data,
			'Suppliers':serializer.data,
			'purchase_order_id':Order,
			'warehouse':serializer_warehouse.data,
			'PurchaseOrders_shipping_method':serializer_PurchaseOrdersShippingMethods.data,
			'PurchaseOrders_payment_method':serializer_paymentmethods.data,
			'purchase_order_list':serializer_PurchaseOrders.data,
			'purchase_order_products':purchase_order_products,
			'received_purchaseorder_master_id': received_purchaseorder_master_id,
			'received_date':received_date,
			'received_purchaseorder_id':received_purchaseorder_id,
			#'Product':serializer_info.data
			'Product':[]
		}
		return Response(data)

	def put(self, request,pk, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		PurchaseOrder = self.get_object(pk,request)
		payment_due_date_time=''
		d2=request.data['order']
		payment_time=request.data['order']['payment_due_date']
		if 'T' in str(payment_time):
			payment_due_date=str(payment_time).split("T")
			payment_due_date_time=payment_due_date[0]
			d1={'created':datetime.now().date(),'modified':datetime.now().date(),'payment_due_date':payment_due_date_time}
		else:
			d1={'created':datetime.now().date(),'modified':datetime.now().date(),'payment_due_date':payment_time}
		serializer_data=dict(d2,**d1)
		serializer = PurchaseOrderSerializer(PurchaseOrder,data=serializer_data,partial=True)

		if serializer.is_valid():
			serializer.save()
			EngageboostPurchaseOrderProducts.objects.using(company_db).filter(purchase_order_id=pk).delete()
			for product in request.data['products']:
				d1={'purchase_order_id':pk}
				d2=product
				serializer_data_products=dict(d1,**d2)
				serializer = PurchaseOrderProductSerializer(data=serializer_data_products,partial=True)
				if serializer.is_valid():
					serializer.save()
					data ={
					'status':1,
					'message':'Successfully Updated',
					}
				else:
					data ={
					'status':0,
					'error':serializer.errors,
					'message':'Data Not Found',
					}
		else:
			data ={
				'status':0,
				'error':serializer.errors,
				'message':'Data Not Found',
			}
		return Response(data)

class PurchaseOrderView(generics.ListAPIView):
# """ View Purchase Order Web Services """
	def get(self, request, pk, format=None, partial=True):
		company_db = loginview.db_active_connection(request)
		website_id = 1
		pur_id = ''
		purchase_order_products = []
		currency_data = EngageboostCurrencyMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
		serializer_currency = CurrencyMastersSerializer(currency_data,many=True)
		Suppliers = EngageboostSuppliers.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
		serializer = SuppliersSerializer(Suppliers,many=True)
		warehouse = EngageboostWarehouseMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer_warehouse = WarehousemastersSerializer(warehouse, many=True)
		PurchaseOrders = EngageboostPurchaseOrdersShippingMethods.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer_PurchaseOrdersShippingMethods = PurchaseOrdersShippingMethodSerializer(PurchaseOrders, many=True)
		PurchaseOrdersPaymentMethods = EngageboostPurchaseOrdersPaymentMethods.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer_paymentmethods = PurchaseOrdersPaymentMethodsSerializer(PurchaseOrdersPaymentMethods, many=True)
		PurchaseOrders = EngageboostPurchaseOrders.objects.using(company_db).all().filter(id=pk)
		serializer_PurchaseOrders = PurchaseOrderSerializer(PurchaseOrders, many=True)
		purchaseordersproducts = EngageboostPurchaseOrderProducts.objects.using(company_db).all().filter(purchase_order_id=pk)
		serializer_purchaseordersproducts = PurchaseOrderProductSerializer(purchaseordersproducts, many=True)
		purchase_order_products = serializer_purchaseordersproducts.data
		# for productData in serializer_purchaseordersproducts.data:
		# 	#print(json.dumps(productData, indent=4, sort_keys=True))
		# 	purchaseordersproducts = EngageboostPurchaseOrderReceivedProductDetails.objects.using(company_db).all().filter(purchase_order_id=pk,purchase_order_product_id =productData['product']['id']).order_by('-expiry_date').all()
		# 	PoReceivedItemDetails = EngageboostPurchaseOrderReceivedProductDetailsSerializer(purchaseordersproducts, many=True)
		# 	#print(PoReceivedItemDetails.data)
		pur_id_count=EngageboostPurchaseOrdersReceived.objects.using(company_db).filter(purchase_order_master_id=pk).count()
		received_purchaseorder_master_id = 0
		received_purchaseorder_id = 0
		received_date = ''
		if pur_id_count >0:
			pur_id = EngageboostPurchaseOrdersReceived.objects.using(company_db).get(purchase_order_master_id=pk)
			purchase_order_count=EngageboostPurchaseOrderReceivedProducts.objects.using(company_db).filter(purchase_order_received_id=pur_id.id).count()
			if purchase_order_count > 0:
				purchaseordersproductsrecieved = EngageboostPurchaseOrderReceivedProducts.objects.using(company_db).all().filter(purchase_order_received_id=pur_id.id)
				serializer_purchaseordersreceivedproducts = PurchaseOrderReceivedProductsSerializer(purchaseordersproductsrecieved, many=True)
				purchase_order_products = []
				purchase_order_products = serializer_purchaseordersreceivedproducts.data
			received_purchaseorder_master_id = pur_id.id
			received_date = pur_id.received_date
			received_purchaseorder_id = pur_id.received_purchaseorder_id

		data = {
			'status':1,
			'currency':serializer_currency.data,
			'Suppliers':serializer.data,
			'warehouse':serializer_warehouse.data,
			'PurchaseOrders_shipping_method':serializer_PurchaseOrdersShippingMethods.data,
			'PurchaseOrders_payment_method':serializer_paymentmethods.data,
			'purchase_order_list':serializer_PurchaseOrders.data,
			'purchase_order_products':purchase_order_products,
			'received_purchaseorder_master_id': received_purchaseorder_master_id,
			'received_date':received_date,
			'received_purchaseorder_id':received_purchaseorder_id,
		}
		return Response(data)
	
# Suppliers Dropdown web services
class SuppliersDropdown(generics.ListAPIView):    
	
	def get(self, request,format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		Suppliers = EngageboostSuppliers.objects.using(company_db).all().filter(id=ids).filter(isdeleted='n',isblocked='n')
		serializer = SuppliersSerializer(Suppliers,many=True)
	  
		
		if(serializer): 
			data ={
				'status':1,
				'Suppliers':serializer.data
				
				
				}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
		return Response(data)
# Select Suppliers Address web services
class SuppliersAddress(generics.ListAPIView):    
	
	def post(self, request,format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		ids=request.data['supplier_id']
		Suppliers = EngageboostSuppliers.objects.using(company_db).all().filter(id=ids).filter(isdeleted='n',isblocked='n')
		serializer = SuppliersSerializer(Suppliers,many=True)
	  
		
		if(serializer): 
			data ={
				'status':1,
				'Suppliers':serializer.data
				
				
				}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
		return Response(data)
# Select Suppliers Currency web services
class SuppliersCurrency(generics.ListAPIView):
	def get(self, request,format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		website_id=1
		imageresizeon= EngageboostGlobalSettings.objects.using(company_db).get(website_id=1)
		order_id=EngageboostPurchaseOrders.objects.using(company_db).count()          
		Order1 =int(order_id)+int(1)

		Order=str(imageresizeon.purchase_order_id_format)+str(Order1)
		queryset=EngageboostGlobalSettings.objects.using(company_db).get(website_id=website_id)
		
		currency_data = EngageboostCurrencyMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
		serializer_currency = CurrencyMastersSerializer(currency_data,many=True)
		Suppliers = EngageboostSuppliers.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
		serializer = SuppliersSerializer(Suppliers,many=True)
		warehouse = EngageboostWarehouseMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer_warehouse = WarehousemastersSerializer(warehouse, many=True)
		PurchaseOrders = EngageboostPurchaseOrdersShippingMethods.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer_PurchaseOrders = PurchaseOrdersShippingMethodSerializer(PurchaseOrders, many=True)
		PurchaseOrdersPaymentMethods = EngageboostPurchaseOrdersPaymentMethods.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer_paymentmethods = PurchaseOrdersPaymentMethodsSerializer(PurchaseOrdersPaymentMethods, many=True)
		# product = EngageboostProducts.objects.using(company_db).all().filter(isblocked='n',isdeleted='n')
		# serializer_info = BasicinfoSerializer(product,many=True)
		if(serializer): 
			data ={
				'status':1,
				'currency':serializer_currency.data,
				'Suppliers':serializer.data,
				'purchase_order_id':Order,
				'warehouse':serializer_warehouse.data,
				'PurchaseOrders_shipping_method':serializer_PurchaseOrders.data,
				'PurchaseOrders_payment_method':serializer_paymentmethods.data
				# 'Product':serializer_info.data
				
				
				}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
		return Response(data)
# Select Suppliers Product web services
class SuppliersProducts(generics.ListAPIView):    
	
	def post(self, request,format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		supplier_ids=request.data['supplier_id']
		supplier_arr=[]
		order_type=request.data['order_type']
		order_by=request.data['order_by']
		key=request.data['search']
		if(order_type=='+'):
			order=order_by
		elif(order_type=='-'):
			order='-'+order_by
		data={'status':1,'Suppliers_products':''}
		Suppliers = EngageboostProducts.objects.using(company_db).all().filter(isblocked='n',isdeleted='n')
		serializer = BasicinfoSerializer(Suppliers,many=True)
		for supplier_id in serializer.data:
			if ',' in str(supplier_id['supplier_id']):
				row=supplier_id['supplier_id'].split(",")
				for rows in row:
					if rows in str(supplier_ids):

						d1=supplier_id['id']
						
						supplier_arr.append(d1)
			else:
				if str(supplier_ids) == supplier_id['supplier_id']:
					d1=supplier_id['id']
					
					supplier_arr.append(d1)  
			if key:
				Suppliers_product = EngageboostProducts.objects.using(company_db).all().order_by(order).filter(isblocked='n',isdeleted='n').filter(id__in=supplier_arr).filter(Q(name__icontains=key)|Q(sku__icontains=key))  
			else:
				Suppliers_product = EngageboostProducts.objects.using(company_db).all().order_by(order).filter(isblocked='n',isdeleted='n').filter(id__in=supplier_arr)
			serializer_product = BasicinfoSerializer(Suppliers_product,many=True)      
			# supplier_arr=[]
			# supplier_arr.append(supplier_id['supplier_id'])
			# print(supplier_arr)

		products = EngageboostProducts.objects.using(company_db).all().order_by(order).filter(isblocked='n',isdeleted='n')
		serializer_product_all = BasicinfoSerializer(products,many=True)
		if(serializer): 
			data ={
				'status':1,
				'Suppliers_products':serializer_product.data,
				'All_products':serializer_product_all.data
				
				}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
		return Response(data)

class PurchaseOrderList(generics.ListAPIView):
# """ List all Purchase Order """
	
	def post(self, request, format=None,many=True):
		company_db = loginview.db_active_connection(request)
		arr=[]
		order_type=request.data['order_type']
		order_by=request.data['order_by']
		key=request.data['search']
		filter_status=request.data['filter']
		user_id = request.data['userid']
		supplier_id = request.data['supplier_id']
		final_data=""

		try:
			key = key.strip()
		except:
			pass	

		try:
			product_id=request.data['product_id']
		except:
			product_id=""
		
		today = datetime.today()   
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
			if request.data.get('show_all'):
				show_all = request.data.get('show_all')
			else:
				show_all = 0
		except Exception as error:
			show_all = 0
		
		if order_by=='name':
			if(order_type=='+'):
				order_product=order_by
				order='id'
			elif(order_type=='-'):
				order_product='-'+order_by
				order='id'
		elif order_by=='sku':
			if(order_type=='+'):
				order_product=order_by
				order='id'
			elif(order_type=='-'):
				order_product='-'+order_by
				order='id'
		else:
			order_product = 'name'
			if(order_type=='+'):
				order=order_by
			elif(order_type=='-'):
				order='-'+order_by
		arr_sup=[]
		arr_warehouse=[] 
		result = ''
		if supplier_id!="" and supplier_id!=None and supplier_id!=0:
			if not EngageboostSuppliers.objects.filter(id=supplier_id).exists():
				return Response({"status":0, "Message":"Please Provide a valid Supplier Id"})
			else:
				result_order = EngageboostPurchaseOrders.objects.using(company_db).all().order_by(order).filter(supplier_id=supplier_id, status__in=['PO Sent', 'Shipped'])	
		else:			
			if not EngageboostUsers.objects.filter(id=user_id).exists():
				return Response({"status":0, "Message":"Please Provide a valid User Id"})

			user_type = EngageboostUsers.objects.get(id=user_id).role.user_role_type
			
			if user_type == 'Supplier':
				if EngageboostSuppliers.objects.filter(user_id=user_id).exists():
					supplier_id = EngageboostSuppliers.objects.using(company_db).get(user_id=user_id).id
					result_order = EngageboostPurchaseOrders.objects.using(company_db).all().order_by(order).filter(supplier_id=supplier_id, status__in=['PO Sent', 'Shipped'])
				else:
					result_order = EngageboostPurchaseOrders.objects.using(company_db).all().order_by(order)

			elif user_type == 'Warehouse Manager':
				if EngageboostWarehouseManager.objects.using(company_db).filter(manager=EngageboostUsers.objects.get(id=user_id)).exists():
					warehouse_id_list = EngageboostWarehouseManager.objects.using(company_db).filter(manager=EngageboostUsers.objects.get(id=user_id)).values_list('warehouse_id', flat=True)
					result_order = EngageboostPurchaseOrders.objects.using(company_db).filter(warehouse_id__in=list(warehouse_id_list)).order_by(order)
				else:
					result_order = EngageboostPurchaseOrders.objects.using(company_db).all().order_by(order)

			else:
				result_order = EngageboostPurchaseOrders.objects.using(company_db).all().order_by(order)

		
				
		if start_date!="" and end_date!="":
			result_order = result_order.filter(created__range=[start_date, end_date])

		if key != "":
			result = result_order.filter(purchase_order_id__icontains=key)
			if EngageboostSuppliers.objects.using(company_db).all().order_by(order).filter(Q(name__icontains=key)).exists():
				arr_sup = EngageboostSuppliers.objects.using(company_db).all().order_by(order).filter(Q(name__icontains=key)).values_list('id', flat=True)
				result = result_order.filter(supplier_id__in=list(arr_sup))

			if EngageboostWarehouseMasters.objects.using(company_db).all().order_by(order).filter(Q(name__icontains=key)).exists():
				arr_warehouse = EngageboostWarehouseMasters.objects.using(company_db).all().order_by(order).filter(Q(name__icontains=key)).values_list('id', flat=True)
				result = result_order.filter(warehouse_id__in=list(arr_warehouse))
		else:
			if filter_status !="":
				result = result_order.filter(status=filter_status)
			else:
				result = result_order
		if request.data.get('advanced_search'):
			filter_arr = request.data.get('advanced_search')
			result = common.get_advanced_search_filter("EngageboostPurchaseOrders",filter_arr,result)
		if product_id != "" and product_id != None:
			productsObj = EngageboostPurchaseOrderProducts.objects.filter(product_id=product_id)
			if productsObj.count()>0:
				productsObj = productsObj.values("purchase_order_id")
				result = result.filter(id__in=productsObj)

		try:
			warehouse_id=request.data['warehouse_id']
			result = result.filter(warehouse_id=warehouse_id)
			
		except:
			pass		
		
					
		# print("=================",result.query)
		users = EngageboostUsers.objects.using(company_db).get(id=user_id)
		issuperadmin = users.issuperadmin
		role_id = users.role_id
		role_permission={}

		menu_fetch=EngageboostMenuMasters.objects.using(company_db).get(module='PurchaseOrders')
		menu_id=menu_fetch.id
		menu_link=menu_fetch.link
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

		# if result.count()>0:
		if show_all == 0:
			page = self.paginate_queryset(result)
		else:
			page = result.all()
		
	
		serializer = PurchaseOrderSerializer(page, many=True)
		
		data = {}
		module='PurchaseOrders'
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

		##################Applied Layout#####################	
		if(layout_check):
			layout_column_check=EngageboostGridColumnLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
			layout_header2=layout_column_check.header_name.split("@@")

			layout_header3 = list(set(layout_header) - set(layout_header2))
			layout_header = layout_header2+layout_header3

			layout_field2=layout_column_check.field_name.split("@@")

			layout_field3 = list(set(layout_field) - set(layout_field2))
			layout_field = layout_field2+layout_field3

		layout2={}
		layout2_arr=[]
		for header2,field2 in zip(layout_header,layout_field):
			ex_layout_field=field2.split(".")
			is_numeric_field=field2.split("#")
			field_name2=ex_layout_field[0]
			
			if len(is_numeric_field)>1:
				field_type2=is_numeric_field[1]
				field_name2=is_numeric_field[0]
			else:
				field_type2=''	

			if len(ex_layout_field)>1:
				child_name=ex_layout_field[1]
				field_name2=ex_layout_field[0]
			else:
				child_name=''			

			if(layout_check):
				layout_column_fetch=EngageboostGridColumnLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
				layout_column_header=layout_column_fetch.header_name
				layout_column_field=layout_column_fetch.field_name
				if header2 in layout_column_header:
					status=1
				else:
					status=0
			else:
				status=1        
			layout2={"title":header2,"field":field_name2,"child":child_name,"show":status, "field_type":field_type2}
			layout2_arr.append(layout2)
			##################Applied Layout#####################	

		final_data=[]
		pre_data={}   
		# print(serializer.data)
		if serializer.data:   
			for purchase_order in serializer.data:
				# print(serializer.data)
				supplier_name=EngageboostSuppliers.objects.using(company_db).get(id=int(purchase_order['supplier_id']))
				warehouse_name=EngageboostWarehouseMasters.objects.using(company_db).get(id=int(purchase_order['warehouse_id']))
				date=EngageboostGlobalSettings.objects.using(company_db).get(website_id=1)
				zone=EngageboostTimezones.objects.using(company_db).get(id=date.timezone_id)
				time_zone=common.get_date_from_datetime(purchase_order['order_date'],zone,date)

				data ={
					'id':purchase_order['id'],
					'purchase_order_id':purchase_order['purchase_order_id'],
					'order_date':time_zone,
					'created_date':purchase_order['order_date'],
					'supplier_name':supplier_name.name,
					'warehouse_name':warehouse_name.name,
					'gross_amount':purchase_order['gross_amount'],
					'net_amount':purchase_order['net_amount'],
					'shipping_cost':purchase_order['shipping_cost'],
					'cart_discount':purchase_order['discount_amount'],
					'purchase_order_tax':purchase_order['purchase_order_tax'],
					'status':purchase_order['status']		
					}

				arr.append(data)
				data2 ={
					'product':arr					
					}
				
				pre_data['result']=data2
		else:
			pre_data['result']=''

		pre_data['layout']=layout_arr
		pre_data['applied_layout']=layout2_arr
		pre_data['role_permission']=role_permission
		final_data.append(pre_data)    
		return self.get_paginated_response(final_data)

class PurchaseOrdersStatusChange(generics.ListAPIView):    
	
	def post(self, request,format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		status=request.data['status']
		ids=request.data['id']
		user_id = request.data['user_id']

		if not EngageboostUsers.objects.filter(id=user_id).exists():
			return Response({'status':0, 'Message':'Please Provide a valid User Id'})

		if status =='Shipped':
			tracking_url=request.data['tracking_url']
			tracking_company=request.data['tracking_company']
			tracking_id=request.data['tracking_id']
			isEmail = request.data['isEmail']
			get_record = EngageboostPurchaseOrders.objects.using(company_db).filter(id=ids)
			website_id = get_record.last().website_id
			get_record.update(status=status,tracking_company=tracking_company,tracking_id=tracking_id,tracking_url=tracking_url) 

			get_record = get_record[0]  
		
			if request.data['isEmail']==True:
				field_dict = {'auto_responder_id': 2}		

				data_dict = {}
				data_dict = getAutoResponderDetails(field_dict)

				to_email = EngageboostUsers.objects.get(id=get_record.createdby).email

				html_content = data_dict['mail_content']
				subject = data_dict['mail_subject']

				supplier_name = EngageboostSuppliers.objects.get(id=get_record.supplier_id).name
				get_warehouse = EngageboostWarehouseMasters.objects.get(id=get_record.warehouse_id)

				serializer =  PurchaseOrderSerializer(get_record)

				for key in serializer.data.keys():
					if html_content.find('{@'+key+'}') > -1:
						html_content = html_content.replace('{@'+key+'}', str(serializer.data[key]))
						

				html_content = html_content.replace('{@name}', get_warehouse.name)
				html_content = html_content.replace('{@supplier_name}', supplier_name)

				response = sendEmail(website_id, html_content, subject, [to_email])

				if response != 'success':
					return Response({'status':0, 'message':'Error', 'api_status': response})


		elif status =='Cancel':
			EngageboostPurchaseOrders.objects.using(company_db).filter(id=ids).update(status=status)
		elif status =='GRN Pending':
			
			received_id=request.data['received_id']
			received_date_time=request.data['received_date']
			warehouse_id=request.data['warehouse_id']
			EngageboostPurchaseOrders.objects.using(company_db).filter(id=ids).update(status=status)
			all_product=EngageboostPurchaseOrderProducts.objects.using(company_db).all().filter(purchase_order_id=ids)
			podata=EngageboostPurchaseOrders.objects.using(company_db).get(id=ids)
			received_date_time_array=str(received_date_time).split("T")
			received_date=received_date_time_array[0]

			d1={'supplier_id':podata.supplier_id,
				'purchase_order_shipping_id':podata.purchase_order_shipping_id,
				'gross_amount':podata.gross_amount,
				'net_amount':podata.net_amount,
				'discount_amount':podata.discount_amount,
				'shipping_cost_base':podata.shipping_cost_base,
				'gross_amount_base':podata.gross_amount_base,
				'net_amount_base':podata.net_amount_base,
				'shipping_cost':podata.shipping_cost,
				'purchase_order_master_id':ids,
				'created':datetime.now().date(),
				'warehouse_id':warehouse_id,
				'modified':datetime.now().date(),
				'received_date':received_date,
				'action':'increase',
				'received_purchaseorder_id':received_id,
				'order_date': datetime.combine(podata.created, datetime.min.time()),
				'website_id': podata.website_id,
				'createdby': podata.createdby,
				'currency_id': podata.currency_id,
				'purchase_order_payment_id': podata.purchase_order_payment_id,
				'payment_method_description':podata.payment_method_description,
				'payment_due_date': podata.payment_due_date,
				'shipping_method_description': podata.shipping_method_description,
				'purchase_order_tax': podata.purchase_order_tax,
				'paid_amount': podata.paid_amount}

			for product in all_product:
				d1['product_id'] = str(product.id)
				d1['quantity'] = product.quantity
											
				serializer = PurchaseOrdersReceivedSerializer(data=d1,partial=True)
				if serializer.is_valid():
					serializer.save()
					data ={
					'status':1,
					'api_status':'',
					'message':'PO Received Successfully.',
					}
					return Response(data)
				else:
					data ={
					'status':0,
					'api_status':serializer.errors,
					'message':'Data Not Found',
					}
					return Response(data)

			

		elif status =='PO Sent':
			if request.data['send_email']==1:
				supplier_email=request.data['supplier_email']

				get_po_record = EngageboostPurchaseOrders.objects.get(id=ids)
				website_id = get_po_record.website_id

				field_dict = {'auto_responder_id': 1}				
				data_dict = {}
				data_dict = getAutoResponderDetails(field_dict)

				html_content = data_dict['mail_content']

				
				currency_symbol = EngageboostCurrencyMasters.objects.get(id=get_po_record.currency_id).currencysymbol
				serializer = PurchaseOrderSerializer(get_po_record)

				for key in serializer.data.keys():
					if html_content.find('{@'+key+'}') > -1:

						if key == 'order_date':
							date = serializer.data[key]
							date = date.split('T')[0]
							date = date.split('-')
							date = date[2]+'/'+date[1]+'/'+date[0]
							html_content = html_content.replace('{@'+key+'}', date)

						if key in ('shipping_cost', 'purchase_order_tax', 'discount_amount'):
							html_content = html_content.replace('{@'+key+'}', currency_symbol+' '+str(serializer.data[key]))

						html_content = html_content.replace('{@'+key+'}', str(serializer.data[key]))
						
				get_supplier = EngageboostSuppliers.objects.get(id=get_po_record.supplier_id)
				warehouse = EngageboostWarehouseMasters.objects.get(id=get_po_record.warehouse_id)
				get_products = EngageboostPurchaseOrderProducts.objects.filter(purchase_order_id=get_po_record.id)


				html_content = html_content.replace('{@supplier_name}', get_supplier.name)
				html_content = html_content.replace('{@warehouse_name}', warehouse.name)
				html_content = html_content.replace('{@warehouse_email}', warehouse.email)
				html_content = html_content.replace('{@warehouse_address}', warehouse.address)
				html_content = html_content.replace('{@warehouse_phone}', warehouse.phone)
				html_content = html_content.replace('{@email}', supplier_email)


				product_table = '<table style="padding: 0px 0 ;border-top:2px dashed #c8c8c8;border-bottom:2px dashed #c8c8c8;" width="100%">\n<tbody>\n<tr>\n\
						<td align="center" ><b>SKU</b></td>\n\
						<td align="center" >Product Name</td>\n\
						<td align="center" >Quantity</td>\n\
						<td align="right" >Cost Per unit</td>\n\
						<td align="right" >Gross Amount</td>\n\
						<td align="right" >Discount Amount</td>\n\
						<td align="right" >Net Amount</td>\n\
					</tr>\n'

				fixed_td = '<tr>\n\
						<td align="center" >{@sku}</td>\n\
						<td align="center" >{@product_name}</td>\n\
						<td align="center" >{@quantity}</td>\n\
						<td align="right" >{@cost_per_unit}</td>\n\
						<td align="right" >{@gross_amount}</td>\n\
						<td align="right" >{@discount_amount}</td>\n\
						<td align="right" >{@net_amount}</td>\n\
						</tr>'

				temp_td = fixed_td

				sub_total = 0

				for product in get_products:
					
					temp_td = temp_td.replace('{@quantity}', str(product.quantity))
					# get_product = EngageboostProducts.objects.filter(id=product_id).last()
					temp_td = temp_td.replace('{@sku}', product.product.sku)
					temp_td = temp_td.replace('{@product_name}', product.product.name)
					gross_amount = int(float(product.price)*float(product.quantity))
					temp_td = temp_td.replace('{@gross_amount}', currency_symbol+' '+ str(gross_amount))
					temp_td = temp_td.replace('{@cost_per_unit}', currency_symbol+' '+str(product.price))
					temp_td = temp_td.replace('{@discount_amount}', currency_symbol+' '+str(product.discount_amount))
					net_amount = gross_amount - int(product.discount_amount)
					sub_total = sub_total + net_amount
					temp_td = temp_td.replace('{@net_amount}', currency_symbol+' '+ str(net_amount))

					product_table = product_table + temp_td
					temp_td = fixed_td

				product_table = product_table + "\n</tbody>\n</table>"

				grand_total = (sub_total + get_po_record.purchase_order_tax + get_po_record.shipping_cost) - get_po_record.discount_amount
				# grand_total_words = num_to_words(grand_total)
				# grand_total_words = grand_total_words.title()

				html_content = html_content.replace('{@product_table}', product_table)
				html_content = html_content.replace('{@sub_total}', currency_symbol+' '+str(sub_total))
				html_content = html_content.replace('{@grand_total}', currency_symbol+' '+str(grand_total))
				# html_content = html_content.replace('{@grand_total_words}', grand_total_words)				
				

				html_content = html_content.replace('{@shipping_method_name}', str(EngageboostPurchaseOrdersShippingMethods.objects.get(id=get_po_record.purchase_order_shipping_id).name))				
				html_content = html_content.replace('{@payment_method_name}', str(EngageboostPurchaseOrdersPaymentMethods.objects.get(id=get_po_record.purchase_order_payment_id).name))				

				subject = 'Purchase Order Confirmation #'+str(serializer.data['purchase_order_id'])
				to_email = supplier_email
		
				response = sendEmail(website_id, html_content, subject, [to_email])

				if response != 'success':
					return Response({'status':0, 'message':'Error', 'api_status': response})


			EngageboostPurchaseOrders.objects.using(company_db).filter(id=ids).update(status=status)
		data ={
				'status':1,
				'message':'Successfully Updated',
				}
		return Response(data)  




class SuppliersEmail(generics.ListAPIView):    
	
	def post(self, request,format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		ids=request.data['id']  
		po_id_count=EngageboostPurchaseOrders.objects.using(company_db).filter(id=ids).count()
		if po_id_count >0:
			po_id=EngageboostPurchaseOrders.objects.using(company_db).get(id=ids)
			sup_id_count=EngageboostSuppliers.objects.using(company_db).filter(id=po_id.supplier_id).count()
			if sup_id_count >0:
				sup_id=EngageboostSuppliers.objects.using(company_db).get(id=po_id.supplier_id)
				data ={
						'status':1,
						'email':sup_id.email,
						}
				
			else:
				data ={
					'status':1,
					'email':'not found',
					}
			return Response(data)
		else:
			data ={
				'status':1,
				'email':'not found',
				}
		return Response(data)
class PoReceived(generics.ListAPIView):
	def post(self, request,format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		purchase_order_id=request.data['data']['purchase_order_id']
		warehouse_id=request.data['data']['warehouse_id']
		total_qty=request.data['data']['total_qty']
		for product_order in request.data['data']['product']:
			EngageboostPurchaseOrderProducts.objects.using(company_db).filter(purchase_order_id=purchase_order_id,product_id=product_order['product_id']).update(updated_quantity=product_order['updated_quantity'])
			qty_stock=EngageboostProductStocks.objects.using(company_db).get(warehouse_id=warehouse_id,product_id=product_order['product_id'])
			
			stock_increased=int(qty_stock.stock)+int(product_order['updated_quantity'])
			real_stock=int(stock_increased)-int(qty_stock.safety_stock)
			EngageboostProductStocks.objects.using(company_db).filter(warehouse_id=warehouse_id,product_id=product_order['product_id']).update(stock=stock_increased,real_stock=real_stock)
			
		quantity=result = sum([i.quantity for i in EngageboostPurchaseOrderProducts.objects.using(company_db).filter(purchase_order_id=purchase_order_id)])
		if total_qty==quantity:
			EngageboostPurchaseOrders.objects.using(company_db).filter(id=purchase_order_id).update(status='Received Full')
		else:
			EngageboostPurchaseOrders.objects.using(company_db).filter(id=purchase_order_id).update(status='Received Partial')
		
		data ={
				'status':1,
				'message':'Successfully Updated'
				}
		return Response(data)

class poreceivedget(generics.ListAPIView):
	def post(self, request,format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		purchase_order_id=request.data['purchase_order_id']
		
		if(EngageboostPurchaseOrdersReceived.objects.using(company_db).count()>0):

			received_ids=EngageboostPurchaseOrdersReceived.objects.using(company_db).latest('id')
			received_id =int(received_ids.id)+int(1)
		else:    
			received_id = int(1)
			
		imageresizeon= EngageboostGlobalSettings.objects.using(company_db).get(website_id=1)
		received_code=str(imageresizeon.receiptid_format)+str(received_id)        
		warehouse=EngageboostPurchaseOrders.objects.using(company_db).get(id=purchase_order_id)            
		quantity=result = sum([i.quantity for i in EngageboostPurchaseOrderProducts.objects.using(company_db).filter(purchase_order_id=purchase_order_id)])
		
		data ={
				'status':1,
				'total_qty':quantity,
				'received_code':received_code,
				'warehouse_id':warehouse.warehouse_id
				}
		return Response(data)

class GrnSend(generics.ListAPIView):
# """ Add new Purchase Order Web Services """
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		payment_due_date_time = ''
		purchase_order_id 	= request.data['purchase_order_id']
		status 				= request.data['status']
		payment_time = request.data['received_date']
		warehouse_id = request.data['warehouse_id']
		
		if 'website_id' in request.data:
			website_id = request.data['website_id']
		else:
			website_id = 1

		pur_id 		= EngageboostPurchaseOrdersReceived.objects.using(company_db).get(purchase_order_master_id=purchase_order_id)
		order_count = EngageboostPurchaseOrderReceivedProducts.objects.using(company_db).filter(purchase_order_received_id=pur_id.id).count()
		if order_count >0:
			EngageboostPurchaseOrderReceivedProducts.objects.using(company_db).filter(purchase_order_received_id=pur_id.id).delete()
		EngageboostPurchaseOrdersReceived.objects.filter(purchase_order_master_id = purchase_order_id).update(status='r')
		# d1={'purchase_order_received_id':pur_id.id,'received_date':payment_time}
		EngageboostPurchaseOrders.objects.using(company_db).filter(id=purchase_order_id).update(status=status)
		for product in request.data['product']:
			EngageboostPurchaseOrderReceivedProducts.objects.using(company_db).create(
				purchase_order_received_id = pur_id.id,
				received_date 	= payment_time,
				product_id 		= product['product_id'],
				price 			= product['price'],
				discount 		= product['discount'],
				quantity 		= product['quantity'],
				discount_amount = product['discount_amount'],
				damage 			= product['damage'],
				total_qty 		= product['total_qty'],
				shortage 		= product['shortage'],
				lot_no 			= product['lot_no'],
				expiry_date 	= product['expiry_date'],
				issues 			= product['damageReason']
			)
			if product['quantityDetails'] and len(product['quantityDetails'])>0:
				for quantityDetails in product['quantityDetails']:
					EngageboostPurchaseOrderReceivedProductDetails.objects.filter(purchase_order_product_id=product['product_id'], purchase_order_received_id=pur_id.id, purchase_order_id=purchase_order_id).delete()
					batchNo = ""
					if "batchNo" in quantityDetails:
						batchNo = quantityDetails['batchNo'] 
					insert_arr = {
						"purchase_order_product_id":product['product_id'], 
						"purchase_order_received_id":pur_id.id, 
						"purchase_order_id":purchase_order_id,
						"lot_no": batchNo,
						"received_quantity":quantityDetails['receivedQuanity'],
						"damaged_quantity":product['damage'],
						# "shortage_quantity": ,
						# "total_quantity": ,
						# "manufactured_date": ,
						# "received_date": ,
						# "expiry_issue_comment": ,
						# "expiry_issue": ,
						# "remarks": ,
						# "price": ,
						# "discount": ,
						# "goods_condition": ,
						"created":datetime.now().date(),
						"modified":datetime.now().date(),
						"website_id":website_id,

					}
					if quantityDetails['expiry_date'] and quantityDetails['expiry_date'] != 'null':
						insert_arr.update({"expiry_date":quantityDetails['expiry_date']})
					EngageboostPurchaseOrderReceivedProductDetails.objects.create(**insert_arr)

			prv_stock 	= EngageboostProductStocks.objects.using(company_db).filter(warehouse_id=warehouse_id, product_id 	= product['product_id']).first()
			if prv_stock:
				# print(prv_stock.query)
				curr_stock 	= int(prv_stock.stock)+int(product['quantity'])
				real_stock 	= int(curr_stock)-int(prv_stock.safety_stock)
				EngageboostProductStocks.objects.using(company_db).filter(warehouse_id=warehouse_id,product_id=product['product_id']).update(
					safety_stock = prv_stock.safety_stock,
					stock 		= curr_stock,real_stock=real_stock
				)
			else:
				EngageboostProductStocks.objects.using(company_db).create(
					safety_stock = 0,
					stock 		= int(product['quantity']),
					real_stock=int(product['quantity']),
					warehouse_id = warehouse_id,
					product_id = product['product_id'],
					created = datetime.now().date(),
					modified = datetime.now().date(),
				)
		data ={
		'status':1,
		'message':'Successfully Inserted',
		}
			
		return Response(data)

class UpdateSafetyStock(generics.ListAPIView):    
	
	def post(self, request,format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		product_id=request.data['product_id']
		warehouse_id=request.data['warehouse_id']
		safety_stock=request.data['safety_stock']
		updatedby=request.data['updatedby']
		prv_stock=EngageboostProductStocks.objects.using(company_db).get(warehouse_id=warehouse_id,product_id=product_id)
		
		# real_stock=int(prv_stock.stock)-int(safety_stock)
		real_stock=float(prv_stock.real_stock)+float(prv_stock.safety_stock)-float(safety_stock)
		EngageboostProductStocks.objects.using(company_db).filter(warehouse_id=warehouse_id,product_id=product_id).update(safety_stock=safety_stock,real_stock=real_stock,updatedby=updatedby)
		
		data ={
			'status':1,
			'message':'Successfully Updated'			
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




class PurchaseOrderGrnDetails(generics.ListAPIView):
	def get(self,request, pk):
		company_db = loginview.db_active_connection(request)
		if not EngageboostPurchaseOrders.objects.filter(id=pk, isdeleted='n').exists():
			return Response({'status':0, "Message":"Such Purchase Order record does not exists"})
		if not EngageboostPurchaseOrderReceivedProductDetails.objects.filter(purchase_order_id=pk, isdeleted='n').exists():
			return Response({'status':0, "Message":"Such Purchase Order Received Product Details record does not exists"})
		if not EngageboostPurchaseOrdersReceived.objects.filter(purchase_order_master_id=pk).exists():
			return Response({'status':0, "Message":"Such Purchase Order Received record does not exists"})
		get_po_record = EngageboostPurchaseOrders.objects.get(id=pk)
		get_record = EngageboostPurchaseOrdersReceived.objects.get(purchase_order_master_id=pk)
		detail_serializer = GrnPurchaseOrderReceivedSerializer(get_record)
		currency_data = EngageboostCurrencyMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
		serializer_currency = CurrencyMastersSerializer(currency_data,many=True)
		Suppliers = EngageboostSuppliers.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
		serializer = SuppliersSerializer(Suppliers,many=True)
		warehouse = EngageboostWarehouseMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer_warehouse = WarehousemastersSerializer(warehouse, many=True)
		PurchaseOrders = EngageboostPurchaseOrdersShippingMethods.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer_PurchaseOrdersShippingMethods = PurchaseOrdersShippingMethodSerializer(PurchaseOrders, many=True)
		PurchaseOrdersPaymentMethods = EngageboostPurchaseOrdersPaymentMethods.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer_paymentmethods = PurchaseOrdersPaymentMethodsSerializer(PurchaseOrdersPaymentMethods, many=True)
		PurchaseOrders = EngageboostPurchaseOrders.objects.using(company_db).all().filter(id=pk)
		serializer_PurchaseOrders = PurchaseOrderSerializer(PurchaseOrders, many=True)
		pur_id=EngageboostPurchaseOrdersReceived.objects.using(company_db).get(purchase_order_master_id=pk)	
		purchaseordersproductsrecieved = EngageboostPurchaseOrderReceivedProducts.objects.using(company_db).all().filter(purchase_order_received_id=pur_id.id)
		serializer_purchaseordersreceivedproducts = PurchaseOrderReceivedProductsSerializer(purchaseordersproductsrecieved, many=True)
		data ={
				'status':1,
				'currency':serializer_currency.data,
				'Suppliers':serializer.data,
				'purchase_order_id':get_po_record.purchase_order_id,
				'warehouse':serializer_warehouse.data,
				'PurchaseOrders_shipping_method':serializer_PurchaseOrdersShippingMethods.data,
				'PurchaseOrders_payment_method':serializer_paymentmethods.data,
				'purchase_order_list':serializer_PurchaseOrders.data,
				'purchase_order_products':serializer_purchaseordersreceivedproducts.data,
				'received_purchaseorder_id':pur_id.received_purchaseorder_id,
				'received_date':pur_id.received_date,
				'Purchase_Order_Received':detail_serializer.data
				}

		return Response({'status':1, "Message":"Success", "data":data})



