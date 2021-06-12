from webservices.models import *
from django.db.models import Value
from django.db.models.functions import Concat
from django.http import Http404
from webservices.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import status
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from rest_framework.parsers import JSONParser
# import datetime
from rest_framework import generics
# from itertools import chain
from django.core import serializers
# from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from webservices.views import loginview
from webservices.views.common import common
from webservices.views.emailcomponent import emailcomponent
from django.db.models import Q
import sys,math
import traceback
import json
from django.contrib.auth.hashers import make_password
import datetime
from datetime import timedelta
from django.db.models import TimeField
from django.db.models import Avg, Max, Min, Sum, Count
from slugify import slugify
import os
from os import path
import time
import base64
import xlrd
import xlsxwriter
from django.utils.crypto import get_random_string
import random
from decimal import Decimal
from frontapp.views.cart import loyalty

# Web Services for all Order View  List - add_order load data... add order data load by cds...on 4th July 2019
class OrdersLoadView(generics.ListAPIView):
	def get(self, request,website_id, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		webstore = EngageboostChannels.objects.using(company_db).all().filter(isblocked='n',isdeleted='n')
		serializer = ChannelsSerializer(webstore,many=True)
		zone_list = EngageboostZoneMasters.objects.filter(isblocked='n', isdeleted='n', location_type='Z').all()
		zone_list = ZoneMastersSerializer(zone_list,many=True)
		payment_methods=[]
		PaymentgatewaySettingInformationCond = EngageboostPaymentgatewaySettingInformation.objects.using(company_db).filter(website_id=website_id,isblocked='n',isdeleted='n').distinct('paymentgateway_method_id')
		if PaymentgatewaySettingInformationCond:
			PaymentgatewaySettingInformation = PaymentgatewaySettingInformationSerializer(PaymentgatewaySettingInformationCond,many=True)
			for PaymentgatewaySetting in PaymentgatewaySettingInformation.data:
				payment_method_id = PaymentgatewaySetting["paymentgateway_method_id"]
				payment_method_details = EngageboostPaymentgatewayMethods.objects.using(company_db).filter(id=payment_method_id).first()
				if payment_method_details:
					PaymentgatewayMethodDict={}
					PaymentgatewayMethodDict={"id":payment_method_details.id,"name":payment_method_details.name}
					payment_methods.append(PaymentgatewayMethodDict)
		country_list = EngageboostCountries.objects.using(company_db).all().filter(country_name='India')
		serializer1 = GlobalsettingscountriesSerializer(country_list, many=True)
		settings = EngageboostCountries.objects.using(company_db).all().filter(~Q(country_name='India')).order_by('country_name')
		serializer_countrys = GlobalsettingscountriesSerializer(settings, many=True)
		d1 = serializer1.data
		d2 = serializer_countrys.data
		country_data = d1+d2
		
		Order = common.GenerateOrderId(1)
		# get_customers = EngageboostCustomers.objects.using(company_db).all().filter(isblocked='n',isdeleted='n')
		# serializer_get_customers = CustomerSerializer(get_customers,many=True)
		
		

		if(serializer): 
			data = {
				'status':1,
				'channel':serializer.data,
				'zone_list':zone_list.data,
				'payment_method':payment_methods,
				'country_list':country_data,
				'Order_id':Order,
				'message':'',
			}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
			}
		return Response(data)

#################Order Delivery######################
class OrderDelivery(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		post_data = request.data
		try:
			status = request.data['status']
			if status=='attempt':
				order_id = request.data['order_id']
				new_delivery_date = request.data['new_delivery_date']
				attempt_delivery_date = request.data['attempt_delivery_date']
				reason = request.data['reason']
				note = request.data['note']
				msg = "Delivery attempted on "+str(attempt_delivery_date)+" failed due to "+str(reason)+" <br>New Delivery Date is "+str(new_delivery_date)+" <br>Note:"+str(note)
				EngageboostOrdermaster.objects.using(company_db).filter(id=order_id).update(delivery_date=new_delivery_date)
				common.save_order_activity(company_db,order_id,None,7,msg,None,1)
				elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'delivery_date':new_delivery_date})
				data = {
						'status':1,
						'api_status':'',
						'message':'Order delivery attempt',
					}
			elif status=='delivery':
				order_id = request.data['order_id']
				EngageboostOrdermaster.objects.using(company_db).filter(id=order_id).update(order_status=4)
				elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'order_status':4})
				data ={
						'status':1,
						'api_status':'',
						'message':'Order delivered',
					}        
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Something went wrong"}
		return Response(data)

# addEditOrderSave save new/create order- add_order.html OrderAddEditComponent save add order by cds on 4th July 2019
class OrderInfoViewSet(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		website_id=request.data['data']['website_id']
		ip_address=request.data['data']['ip_address']
		user_id=request.data['data']['user_id']
		email=request.data['data']['email']
		prefix=EngageboostGlobalSettings.objects.using(company_db).get(website_id=website_id)
		order_prefix=prefix.order_prefix_type
		count =EngageboostOrdermaster.objects.using(company_db).count()
		if count >0:
			obj = EngageboostOrdermaster.objects.using(company_db).latest('id')
			last_id = obj.id
			order_no=order_prefix+str(last_id)
		else:
			order_no=order_prefix+0
		d1={'created_date':datetime.datetime.now(),'modified':datetime.datetime.now(),'custom_order_id':order_no}
		send_email=request.data['data']['send_email']
		try:
			if send_email==1:
				subject, from_email, to = 'Order details', 'aritra.chowdhury@navsoft.in', email
				text_content = 'Order details'
				html_content = 'Order details'
				msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
				msg.attach_alternative(html_content, "text/html")
				msg.send()
			d2=request.data['data']
			serializer_data=dict(d2,**d1)
			serializer = OrderMasterSerializer(data=serializer_data,partial=True)
			if serializer.is_valid():
				serializer.save()
				orderlast = EngageboostOrdermaster.objects.using(company_db).latest('id')
				orderlastid = orderlast.id
				products=request.data['product']
				for productorder in products:
					EngageboostOrderProducts.objects.using(company_db).create(order_id=int(orderlastid),product_id=int(productorder['product_id']),quantity=int(productorder['quantity']),product_price=productorder['product_price'],product_discount_price=productorder['product_discount_price'],warehouse_id=0)
				data ={
					'status':1,
					'api_status':'',
					'message':'Successfully Inserted',
				}
			else:
				data = {
					'status':0,
					'api_status':serializer.errors,
					'message':'Data Not Found',
				}

		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Something went wrong"}
		return Response(data)
# addEditOrderSave save order- add_order.html OrderAddEditComponent edit ORDER by cds on 4th July 2019 """
class OrderList(generics.ListAPIView):
	# """ List all users, or create a new user """
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostOrdermaster.objects.using(company_db).get(pk=pk)
		except EngageboostOrdermaster.DoesNotExist:
			raise Http404
	#Fetch Single Row  # get edit order data - get edit order by cds on 4th July 2019 """
	def get(self, request, pk, website_id, format=None):
		company_db = loginview.db_active_connection(request)
		# Common dropdown data start 
		try:
			webstore = EngageboostChannels.objects.using(company_db).all().filter(isblocked='n',isdeleted='n')
			webstore_data = ChannelsSerializer(webstore,many=True)
			zone_list = EngageboostZoneMasters.objects.filter(isblocked='n', isdeleted='n', location_type='Z').all()
			zone_list = ZoneMastersSerializer(zone_list,many=True)
			payment_methods=[]
			PaymentgatewaySettingInformationCond = EngageboostPaymentgatewaySettingInformation.objects.using(company_db).filter(website_id=website_id,isblocked='n',isdeleted='n').distinct('paymentgateway_method_id')
			if PaymentgatewaySettingInformationCond:
				PaymentgatewaySettingInformation = PaymentgatewaySettingInformationSerializer(PaymentgatewaySettingInformationCond,many=True)
				for PaymentgatewaySetting in PaymentgatewaySettingInformation.data:
					payment_method_id = PaymentgatewaySetting["paymentgateway_method_id"]
					payment_method_details = EngageboostPaymentgatewayMethods.objects.using(company_db).filter(id=payment_method_id).first()
					if payment_method_details:
						PaymentgatewayMethodDict={}
						PaymentgatewayMethodDict={"id":payment_method_details.id,"name":payment_method_details.name}
						payment_methods.append(PaymentgatewayMethodDict)
			country_list = EngageboostCountries.objects.using(company_db).all().filter(country_name='India')
			serializer1 = GlobalsettingscountriesSerializer(country_list, many=True)
			settings = EngageboostCountries.objects.using(company_db).all().filter(~Q(country_name='India')).order_by('country_name')
			serializer_countrys = GlobalsettingscountriesSerializer(settings, many=True)
			d1 = serializer1.data
			d2 = serializer_countrys.data
			country_data = d1+d2
			# Common dropdown data end
			order = self.get_object(pk,request)
			serializer = OrderMasterSerializer(order)
			product_arr = []
			OrderProductsquery = EngageboostOrderProducts.objects.using(company_db).all().filter(order_id=pk)
			# product select for single row update
			for products in OrderProductsquery:
				product_name = EngageboostProducts.objects.using(company_db).all().filter(id=products.product_id)
				for productsset in product_name:
					product_arr.append({
						'product_id': productsset.id,
						'sku': productsset.sku,
						'product_name':productsset.name,
						'description':productsset.description,
						'cost':products.product_price,
						'quantity':products.quantity,
						'product_discount_price':products.product_discount_price,
					})

			if(serializer): 
				data = {
					'status':1,
					'api_status':serializer.data,
					'channel':webstore_data.data,
					'zone_list':zone_list.data,
					'payment_method':payment_methods,
					'country_list':country_data,
					'products':product_arr,
					'message':''
				}
			else:
				data ={
					'status':0,
					'api_status':serializer.errors,
					'message':'Data Not Found',
				}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error), 'message': str(error)}              
		return Response(data)
	# save edit order data - save edit order by cds on 4th July 2019 """
	def put(self, request, pk, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		order = self.get_object(pk,request)
		d1={'auth_user_id':pk,'modified':datetime.datetime.now()}
		d2=request.data['data']
		send_email=request.data['data']['send_email']
		serializer_data=dict(d2,**d1)
		serializer = OrderMasterSerializer(order,data=serializer_data,partial=True)
		if serializer.is_valid():
			serializer.save()
			EngageboostOrderProducts.objects.using(company_db).filter(order_id=pk).delete()
			products=request.data['product']
			for productorder in products:
				EngageboostOrderProducts.objects.using(company_db).create(order_id=pk,product_id=int(productorder['product_id']),quantity=int(productorder['quantity']),product_price=productorder['product_price'],product_discount_price=productorder['product_discount_price'],warehouse_id=0)
			data ={
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
# payment method list for order insert
class Paymentmethodtype(generics.ListAPIView):
	def get(self, request, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		settings = EngageboostPaymentgatewayMethods.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
		serializer = PaymentgatewayMethodsSerializer(settings, many=True)
		if(serializer): 
			data ={
				'status':1,
				'payment_method':serializer.data,

				}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
		return Response(data)
# Promotions Coupon list for order insert       
class Promotionscoupon(generics.ListAPIView):
	def post(self, request, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		coupon=request.data['coupon']
		coupon_id = EngageboostDiscountMastersCoupons.objects.using(company_db).all().filter(isdeleted='n',coupon_code=coupon)
		serializer = DiscountMasterCouponSerializer(coupon_id, many=True)
		if(serializer): 
			data ={
				'status':1,
				'payment_method':serializer.data,

				}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
		return Response(data)

class AssignToWarehouse(generics.ListAPIView):
	def post(self, request, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		pending_orders=[]
		try:
			if request.data.get('order_ids'): #*********OrderWise Warehouse assign************
				orderIds=request.data['order_ids'].split(',')
				for i in orderIds:
					orderDetails=EngageboostOrdermaster.objects.using(company_db).filter(id=i).first()
					if orderDetails:
						order_status = orderDetails.order_status
						if order_status!=0:
							pending_data={"order_id":orderDetails.id,"order_custom_id":orderDetails.custom_order_id}
							pending_orders.append(pending_data)
							data={"status":0,"message":"You cann't assign warehouse other than a pending order","pending_orders":pending_orders}
						else:
							try:
								if request.data['assign_wh']:
									EngageboostOrdermaster.objects.filter(id=i).update(assign_to=request.data['assign_to'],assign_wh=request.data['assign_wh'])
									
									username = ""
									userObj = EngageboostUsers.objects.filter(id=request.data['assign_to']).first()
									if userObj:
										username = userObj.username

									warehousename =""
									wareHouseObj = EngageboostWarehouseMasters.objects.filter(id=request.data['assign_wh']).first()
									if wareHouseObj:
										warehousename = wareHouseObj.name

									elastic = common.change_field_value_elastic(i,'EngageboostOrdermaster',{'assign_to':request.data['assign_to'],'assign_to_name':username,'assign_wh':request.data['assign_wh'],'assign_wh_name':warehousename})
									EngageboostOrderProducts.objects.filter(order_id=i).update(assign_to=request.data['assign_to'],assign_wh=request.data['assign_wh'])
									data={"status":1,"message":"Warehouse assigned to orders","warehouse_manager":request.data['manager_name'],"pending_orders":pending_orders}
								else:
									EngageboostOrdermaster.objects.filter(id=i).update(assign_to=None,assign_wh=None)
									EngageboostOrderProducts.objects.filter(order_id=i).update(assign_to=None,assign_wh=None)
									data={"status":1,"message":"Warehouse removed from orders","warehouse_manager":"","pending_orders":pending_orders}
							except Exception as error:
								trace_back = sys.exc_info()[2]
								line = trace_back.tb_lineno
								data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'message':str(error)}
					else:
						data={"status":0,"message":"No order found"}

				# warehouseManagerCond = EngageboostWarehouseManager.objects.using(company_db).filter(warehouse_id=request.data['assign_wh']).first()
				# if warehouseManagerCond:
				#     userDetails = EngageboostUsers.objects.using(company_db).filter(id=warehouseManagerCond.manager_id,isblocked='n',isdeleted='n').first()
				#     if userDetails:
				#         for i in orderIds:
				#             orderDetails=EngageboostOrdermaster.objects.using(company_db).filter(id=i).first()
				#             if orderDetails:
				#                 order_status = orderDetails.order_status
				#                 if order_status!=0:
				#                     pending_data={"order_id":orderDetails.id,"order_custom_id":orderDetails.custom_order_id}
				#                     pending_orders.append(pending_data)
				#                     data={"status":0,"message":"You cann't assign warehouse other than a pending order","pending_orders":pending_orders}
				#                 else:
				#                     try:
				#                         EngageboostOrdermaster.objects.filter(id=i).update(assign_to=warehouseManagerCond.manager_id,assign_wh=request.data['assign_wh'])
				#                         EngageboostOrderProducts.objects.filter(order_id=i).update(assign_to=warehouseManagerCond.manager_id,assign_wh=request.data['assign_wh'])
				#                         data={"status":1,"message":"Warehouse assigned to orders","warehouse_manager":userDetails.first_name+' '+userDetails.last_name,"pending_orders":pending_orders}
				#                     except Exception as error:
				#                         trace_back = sys.exc_info()[2]
				#                         line = trace_back.tb_lineno
				#                         data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error)}
				#             else:
				#                 data={"status":0,"message":"No order found"}
				#     else:
				#         data={"status":0,"message":"Either warehouse manager deleted or blocked."}
				# else:
				#     data={"status":0,"message":"No warehouse manager"}

			else: #*********ItemWise Warehouse assign************
				itemIds = request.data["item_ids"].split(',')

				for i in itemIds:
					orderProductDetails=EngageboostOrderProducts.objects.using(company_db).filter(id=i).first()
					if orderProductDetails:
						order_status = orderProductDetails.status
						if order_status!=0:
							pending_data={"product_id":orderProductDetails.id}
							pending_orders.append(pending_data)
							data={"status":0,"message":"You cann't assign warehouse other than a pending order","pending_orders":pending_orders}
						else:                            
							try:
								# EngageboostOrdermaster.objects.filter(id=orderProductDetails.order_id).update(assign_to=request.data['assign_to'],assign_wh=request.data['assign_wh'])
								if request.data['assign_wh']:
									EngageboostOrderProducts.objects.filter(id=i).update(assign_to=request.data['assign_to'],assign_wh=request.data['assign_wh'],warehouse_id=request.data['assign_wh'])
									data={"status":1,"message":"Warehouse assigned to products","warehouse_manager":request.data['manager_name']}
								else:
									EngageboostOrderProducts.objects.filter(id=i).update(assign_to=None,assign_wh=None,warehouse_id=None)
									data={"status":1,"message":"Warehouse removed from products","warehouse_manager":request.data['manager_name']}
							except Exception as error:
								trace_back = sys.exc_info()[2]
								line = trace_back.tb_lineno
								data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'message':str(error)}
					else:
						data={"status":0,"message":"No order item found"}


				# warehouseManagerCond = EngageboostWarehouseManager.objects.using(company_db).filter(warehouse_id=request.data['assign_wh']).first()
				# if warehouseManagerCond:
				#     userDetails = EngageboostUsers.objects.using(company_db).filter(id=warehouseManagerCond.manager_id,isblocked='n',isdeleted='n').first()
				#     if userDetails:
				#         for i in itemIds:
				#             try:
				#                 # EngageboostOrdermaster.objects.filter(id=order_id).update(assign_to=warehouseManagerCond.manager_id,assign_wh=request.data['assign_wh'])
				#                 EngageboostOrderProducts.objects.filter(id=i).update(assign_to=warehouseManagerCond.manager_id,assign_wh=request.data['assign_wh'],warehouse_id=request.data['assign_wh'])
				#                 data={"status":1,"message":"Warehouse assigned to products","warehouse_manager":userDetails.first_name+' '+userDetails.last_name}
				#             except Exception as error:
				#                 trace_back = sys.exc_info()[2]
				#                 line = trace_back.tb_lineno
				#                 data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'message':str(error)}
				#     else:
				#         data={"status":0,"message":"Either warehouse manager deleted or blocked."}
				# else:
				#     data={"status":0,"message":"No warehouse manager"}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'message':str(error)}

		return Response(data)

class UpdateOrderStatus(generics.ListAPIView):
	def post(self, request, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		status_not_change=[]
		# return Response(request.data)
		try:
			if request.data.get('order_ids'):
				orderIds=request.data['order_ids'].split(',')
				for i in orderIds:
					orderDetails=EngageboostOrdermaster.objects.using(company_db).filter(id=i).first()
					if orderDetails:
						order_status = orderDetails.order_status
						buy_status = orderDetails.buy_status
						new_order_status = ""
						if request.data.get('order_status') == "completed": 
							# if order_status == 1 and buy_status == 1: # If order is waiting for approval
							if buy_status == 1:
								if order_status == 1:
									now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
									delivery_date = now_utc
									save_arr = {}
									save_arr = {
										"order_status":4,
										"delivery_date":delivery_date,
										"paid_amount":float(orderDetails.gross_amount)
									}
								else : 
									save_arr = {
										"order_status":4,
									}
								EngageboostOrdermaster.objects.filter(id=i).update(**save_arr)
								new_order_status = 4
							else:
								pending_data={"order_id":orderDetails.id,"order_custom_id":orderDetails.custom_order_id}
								status_not_change.append(pending_data)

							if status_not_change:
								data={"status":1,"message":"Only Shipped orders can be updated to completed status","unchanged_orders":status_not_change}
							else:
								data={"status":1,"message":"Order Status Updated","unchanged_orders":status_not_change}

						elif request.data.get('order_status') == "pending": 
							if buy_status == 0: # If order is Falied or Abandoned
								EngageboostOrdermaster.objects.filter(id=i).update(order_status=0,buy_status=1)
								new_order_status = 0
							else:
								pending_data={"order_id":orderDetails.id,"order_custom_id":orderDetails.custom_order_id}
								status_not_change.append(pending_data)

							if status_not_change:
								data={"status":1,"message":"Only Falied or Abandoned are allowed to move success order","unchanged_orders":status_not_change}
							else:
								data={"status":1,"message":"Order Status Updated","unchanged_orders":status_not_change}

						elif request.data.get('order_status') == "closed": 
							if (order_status == 0 or order_status == 99 or order_status == 999 or order_status == 3 or order_status == 1 or order_status == 16) and buy_status == 1:
								pending_data={"order_id":orderDetails.id,"order_custom_id":orderDetails.custom_order_id}
								status_not_change.append(pending_data)
							else:
								EngageboostOrdermaster.objects.filter(id=i).update(order_status=16,buy_status=1)
								new_order_status = 16

							if status_not_change:
								data={"status":1,"message":"Pending, Cancelled, Failed, Abondoned, Closed orders are not allowed change to closed","unchanged_orders":status_not_change}
							else:
								data={"status":1,"message":"Order Status Updated","unchanged_orders":status_not_change}
						else:
							# 1=Shipped 13=Delivered 2=Deleted/Cancelled 16=Closed 
							if order_status == 2 or order_status == 1 or order_status == 16 or order_status == 13 and buy_status == 1:
								pending_data={"order_id":orderDetails.id,"order_custom_id":orderDetails.custom_order_id}
								status_not_change.append(pending_data)
							else:
								EngageboostOrdermaster.objects.filter(id=i).update(order_status=2,buy_status=1)
								new_order_status = 2
								orderProductDetailsCond=EngageboostOrderProducts.objects.using(company_db).filter(order_id=i).all()
								if orderProductDetailsCond:
									orderProductDetails = OrderProductsSerializer(orderProductDetailsCond,many=True)
									for orderProducts in orderProductDetails.data:
										EngageboostOrderProducts.objects.filter(id=orderProducts["id"]).update(status=2,deleted_quantity=orderProducts["quantity"])

							if status_not_change:
								data={"status":1,"message":"Shipped, Delivered, Cancelled and Closed orders are not allowed to change","unchanged_orders":status_not_change}
							else:
								data={"status":1,"message":"Order Status Updated","unchanged_orders":status_not_change}
						
						if new_order_status!="":
							elastic = common.change_field_value_elastic(int(i),'EngageboostOrdermaster',{'order_status':new_order_status})
					else:
						data={"status":0,"message":"No order found"}
			else:
				itemIds=request.data['item_ids'].split(',')
				for i in itemIds:
					itemDetails=EngageboostOrderProducts.objects.using(company_db).filter(id=i).first()
					if itemDetails:
						order_status = itemDetails.status
						if request.data.get('order_status') == "approve": 
							if order_status == 99: # If order is waiting for approval
								EngageboostOrderProducts.objects.filter(id=i).update(status=0)
							else:
								pending_data={"product_id":itemDetails.id}
								status_not_change.append(pending_data)

							if status_not_change:
								data={"status":1,"message":"Only Waiting for Approval products can be updated to pending status","unchanged_products":status_not_change}
							else:
								data={"status":1,"message":"Order Product Status Updated","unchanged_products":status_not_change}

						elif request.data.get('order_status') == "pending": 
							orderDetails=EngageboostOrdermaster.objects.using(company_db).filter(id=itemDetails.order_id).first()
							buy_status = orderDetails.buy_status

							if buy_status == 0: # If order is Falied or Abandoned
								# EngageboostOrdermaster.objects.filter(id=i).update(order_status=0,buy_status=1)
								pending_data={"order_id":orderDetails.id,"order_custom_id":orderDetails.custom_order_id}
								status_not_change.append(pending_data)
							else:
								pass

							if status_not_change:
								data={"status":1,"message":"These are failed orders. Please change the order status to pending.","unchanged_orders":status_not_change}
							else:
								data={"status":1,"message":"Order Product staus updated","unchanged_orders":status_not_change}

						elif request.data.get('order_status') == "closed": 
							orderProductDetailsCond=EngageboostOrderProducts.objects.using(company_db).all().filter(order_id=itemDetails.order_id).filter(~Q(status=1)|~Q(status=16))
							if orderProductDetailsCond:
								orderDetails=EngageboostOrdermaster.objects.using(company_db).filter(id=itemDetails.order_id).first()
								pending_data={"order_id":orderDetails.id,"order_custom_id":orderDetails.custom_order_id}
								status_not_change.append(pending_data)
							else:
								EngageboostOrderProducts.objects.filter(id=i).update(status=16)
								orderProductDetailsCond=EngageboostOrderProducts.objects.using(company_db).all().filter(order_id=itemDetails.order_id).filter(~Q(status=1)|~Q(status=16))
								if orderProductDetailsCond:
									pass
								else:
									EngageboostOrdermaster.objects.filter(id=itemDetails.order_id).update(order_status=16,buy_status=1)


							if status_not_change:
								data={"status":1,"message":"You can not close an single item, until all the products associated with the same order has been shipped.","unchanged_orders":status_not_change}
							else:
								data={"status":1,"message":"Order Product Status Updated","unchanged_orders":status_not_change}

						else:
							# 1=Shipped 13=Delivered 2=Deleted/Cancelled 16=Closed 
							if order_status == 2 or order_status == 1 or order_status == 16 or order_status == 13: # If order is pending
								pending_data={"order_id":orderDetails.id,"order_custom_id":orderDetails.custom_order_id}
								status_not_change.append(pending_data)
							else:
								EngageboostOrderProducts.objects.filter(id=i).update(status=2,deleted_quantity=itemDetails.quantity)

							if status_not_change:
								data={"status":1,"message":"Shipped, Delivered, Cancelled and Closed orders are not allowed to change","unchanged_orders":status_not_change}
							else:
								data={"status":1,"message":"Order Product Status Updated","unchanged_orders":status_not_change}

		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error)}

		return Response(data)   

class GetTags(generics.ListAPIView):
	def get(self, request, id, format=None):
		company_db = loginview.db_active_connection(request)
		cond = EngageboostTags.objects.using(company_db).all().filter(id=id)
		if cond:
			serializer = TagsSerializer(cond,many=True)
			if serializer: 
				data ={"status":1,"api_status":serializer.data,"message":'Tag Information'}
			else:
				data ={"status":0,"api_status":serializer.errors,"message":'Data Not Found'}
		else:
			data ={"status":0,"api_status":'No tag found',"message":'No Tag Found'}
		return Response(data)

class ManageTags(generics.ListAPIView):
	def post(self, request, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		serializer_data={}
		# serializer_data={x:request.POST.get(x) for x in request.POST.keys()}
		serializer_data=request.data

		try:
			if request.data.get('id'): 
				ids = request.data.get('id')
			else: ids = None
		except KeyError: ids = None

		if ids: #For Edit Tag
			if request.data.get('isdeleted') == "y" or request.data.get('isblocked') == "y":
				tag_id = EngageboostTags.objects.using(company_db).get(id=serializer_data['id'])
				serializer_data=dict(serializer_data)
				serializer = TagsSerializer(tag_id,data=serializer_data,partial=True)
				if serializer.is_valid():
					serializer.save()
					data={"status":1,"api_status":serializer.data["id"],"message":'Tag Updated successfully'}
				else:
					data={"status":0,"api_status":serializer.errors,"message":'Error occured'}
			else:
				has_tag = EngageboostTags.objects.using(company_db).filter(tag_name=serializer_data["tag_name"]).first()
				if has_tag:
					existing_tag_id = has_tag.id
					if existing_tag_id==int(ids):
						# print("1111111111111")
						tag_id = EngageboostTags.objects.using(company_db).get(id=serializer_data['id'])
						serializer_data=dict(serializer_data)
						serializer = TagsSerializer(tag_id,data=serializer_data,partial=True)
						if serializer.is_valid():
							serializer.save()
							data={"status":1,"api_status":serializer.data["id"],"message":'Tag Updated successfully'}
						else:
							data={"status":0,"api_status":serializer.errors,"message":'Error occured'}
					else:
						# print("222222222222")
						data={"status":0,"api_status":"Tag already exists","message":"Tag already exists"}
				else:
					tag_id = EngageboostTags.objects.using(company_db).get(id=serializer_data['id'])
					serializer_data=dict(serializer_data)
					serializer = TagsSerializer(tag_id,data=serializer_data,partial=True)
					if serializer.is_valid():
						serializer.save()
						data={"status":1,"api_status":serializer.data["id"],"message":'Tag Updated successfully'}
					else:
						data={"status":0,"api_status":serializer.errors,"message":'Error occured'}
		
		else: #For Add Tag
			has_tag = EngageboostTags.objects.using(company_db).filter(tag_name=serializer_data["tag_name"]).first()
			if has_tag:
				data={"status":0,"api_status":"Tag already exists","message":"Tag already exists"}
			else:
				serializer_data=dict(serializer_data)
				serializer = TagsSerializer(data=serializer_data,partial=True)
				if serializer.is_valid():
					serializer.save()
					data={"status":1,"api_status":serializer.data["id"],"message":'Tag added successfully'}
				else:
					data={"status":0,"api_status":serializer.errors,"message":'Error occured'}
		return Response(data)

class AssignTag(generics.ListAPIView):
	def post(self, request, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		errors=[]
		try:
			if request.data.get('order_ids'): #*********OrderWise Tag assign************
				orderIds=request.data['order_ids'].split(',')
				for i in orderIds:
					try:
						if request.data['tag_id']:
							EngageboostOrdermaster.objects.filter(id=i).update(tags=request.data['tag_id'])
							EngageboostOrderProducts.objects.filter(order_id=i).update(tags=request.data['tag_id'])

							elastic = common.update_order_tag_elastic(i,request.data['tag_id'])
							data={"status":1,"api_status":"Tag assigned to order","message":"Tag assigned to order"}
						else:
							EngageboostOrdermaster.objects.filter(id=i).update(tags=None)
							EngageboostOrderProducts.objects.filter(order_id=i).update(tags=None)

							elastic = common.update_order_tag_elastic(i,None)
							data={"status":1,"api_status":"Tag removed from order","message":"Tag removed from order"}        

					except Exception as error:
						trace_back = sys.exc_info()[2]
						line = trace_back.tb_lineno
						data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error)}
						errors.append(data)
			else: #*********ItemWise Tag assign************   
				itemIds = request.data["item_ids"].split(',')
				for i in itemIds:
					try:
						orderProductDetails = EngageboostOrderProducts.objects.filter(id=i).first()
						if orderProductDetails:
							order_id = orderProductDetails.order_id
							if request.data['tag_id']:
								EngageboostOrdermaster.objects.filter(id=order_id).update(tags=request.data['tag_id'])
								elastic = common.update_order_tag_elastic(order_id,request.data['tag_id'])
							else:
								EngageboostOrdermaster.objects.filter(id=order_id).update(tags=None)
								elastic = common.update_order_tag_elastic(order_id,None)

						if request.data['tag_id']:
							EngageboostOrderProducts.objects.filter(id=i).update(tags=request.data['tag_id'])
							data={"status":1,"api_status":"Tag assigned to products","message":"Tag assigned to products"}
						else:
							EngageboostOrderProducts.objects.filter(id=i).update(tags=None)
							data={"status":1,"api_status":"Tag removed from products","message":"Tag removed from products"}
					except Exception as error:
						trace_back = sys.exc_info()[2]
						line = trace_back.tb_lineno
						data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error)}
						errors.append(data)
						
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error)}

		data["error"]=errors
		return Response(data)

class FindCustomer(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		if request.data.get('search'):
			search=request.data['search']
			customer_email = EngageboostCustomers.objects.annotate(customer_name=Concat('first_name', Value(' '), 'last_name')).all()
			customer_email = customer_email.filter(Q(email__icontains=search)|Q(phone__icontains=search)|Q(customer_name__icontains=search)).filter(isdeleted='n',isblocked='n').values("id","website_id","first_name","last_name","email","phone","orders","avgorder","totalorder","lastlogin","is_guest_user","is_ledger_created")
			customer_email = customer_email.order_by('-id')
			if search.strip()=="":
				customer_email = customer_email[0:10]
			# queryset = Item.objects.annotate(search_name=Concat('series', Value(' '), 'number')) # then you can filter: 
			# queryset.filter(search_name__icontains='whatever text')
			if customer_email:
				serializer = CustomerListViewSerializer(customer_email,many=True)
				data ={"status":1,"api_status":serializer.data,"message":'Customer record found'}
			else:
				data ={"status":0,"api_status":'No customer record found',"message":'No customer record found'}
		else:
			data ={"status":0,"api_status":'No customer record found',"message":'No customer record found'}
		return Response(data)
# Customer details selected by email id 
class GetCustomerInfo(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		if request.data.get('id'):
			cust_id=request.data['id']
			customer_email = EngageboostCustomers.objects.using(company_db).all().filter(id=cust_id,isdeleted='n',isblocked='n').values("id","website_id","first_name","last_name","email","phone","orders","avgorder","totalorder","lastlogin","is_guest_user","is_ledger_created","group_id")

			if customer_email:    
				serializer = CustomerListViewSerializer(customer_email,many=True)
				if serializer: 
					for customer in serializer.data:
						address_book_cond = EngageboostCustomersAddressBook.objects.using(company_db).filter(customers_id=customer["id"],set_primary=1,isdeleted='n',isblocked='n').first()
						if address_book_cond:
							address_book = CustomersAddressBookSerializer(address_book_cond)
							customer["customer_address_book"] = address_book.data
						else:
							customer["customer_address_book"] = []

					data ={"status":1,"api_status":serializer.data,"message":'Customer record found'}
			else:
				data ={"status":0,"api_status":'No customer record found',"message":'No customer record found'}
		else:
			data ={"status":0,"api_status":'Wrong data post',"message":'Wrong data post'}
		return Response(data)

class GenerateOrderId(generics.ListAPIView):
	def get(self, request, channel_id, format=None):
		company_db = loginview.db_active_connection(request)
		website_id=1
		custom_order_id=''

		# Find custom order prefix from global settings
		prefixCon = EngageboostGlobalSettings.objects.using(company_db).filter(website_id=website_id,isblocked='n',isdeleted='n').first()
		if prefixCon:
			ordPrefix = prefixCon.orderid_format
			if prefixCon.order_prefix_type=='Warehouse' and channel_id>0:
				warehouse_data = EngageboostWarehouseMasterApplicableChannels.objects.using(company_db).filter(applicable_channel_id=channel_id).first()
				warehouse_id = warehouse_data.warehouse_master_id
				if warehouse_id>0:
					data=EngageboostWarehouseMasters.objects.using(company_db).filter().first(id=warehouse_id,website_id=website_id,isblocked='n',isdeleted='n')
					ordPrefix=data.order_id_format
			has_record = EngageboostOrdermaster.objects.filter(website_id=website_id,webshop_id=channel_id).order_by('-id').first()
			if has_record:
				lastCustomOrder = has_record.custom_order_id
				# return Response(ordPrefix)
				orderArr=lastCustomOrder.split(ordPrefix)
				# return Response(orderArr)
				if orderArr[0]:
					has_record = EngageboostOrdermaster.objects.filter(website_id=website_id,webshop_id=channel_id).order_by('-id').latest('id')
					if has_record:
						appendId = has_record.id
						nextappendId=appendId+1
					else:
						nextappendId = 1

					customorderid=ordPrefix+''+str(nextappendId)
				else:
					appendId=int(orderArr[1])
					nextappendId=appendId+1
					customorderid=ordPrefix+''+str(nextappendId)
			else:
				appendId = 1
				nextappendId=appendId+1
				customorderid=ordPrefix+''+str(nextappendId)

			data={"status":1,"api_status":customorderid,"message":"Custom Order ID"}
		else:
			data={"status":0,"message":"No record in global settings"}

		return Response(data)

class PaymentGatewayList(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		website_id = request.data["website_id"]
		PaymentgatewayMethodList=[]
		PaymentgatewaySettingInformationCond = EngageboostPaymentgatewaySettingInformation.objects.using(company_db).filter(website_id=website_id,isblocked='n',isdeleted='n').distinct('paymentgateway_method_id')
		if PaymentgatewaySettingInformationCond:
			PaymentgatewaySettingInformation = PaymentgatewaySettingInformationSerializer(PaymentgatewaySettingInformationCond,many=True)
			for PaymentgatewaySetting in PaymentgatewaySettingInformation.data:
				payment_method_id = PaymentgatewaySetting["paymentgateway_method_id"]
				payment_method_details = EngageboostPaymentgatewayMethods.objects.using(company_db).filter(id=payment_method_id).first()
				if payment_method_details:
					PaymentgatewayMethodDict={}
					PaymentgatewayMethodDict={"id":payment_method_details.id,"name":payment_method_details.name}
					PaymentgatewayMethodList.append(PaymentgatewayMethodDict)

			data={"status":1,"api_status":PaymentgatewayMethodList,"message":"Payment gateway List"}
		else:
			data={"status":0,"api_status":PaymentgatewayMethodList,"message":"No payment gateway available"}

		return Response(data)
# popup order edit listing
class WarehouseWiseProduct(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		postdata = request.data
		channel_id = postdata["channel_id"]
		website_id = postdata["website_id"]
		search_key = None
		if "search" in postdata:
			search_key = postdata["search"]
		currency_id = ""
		if "currency_id" in postdata:
			currency_id = postdata["currency_id"]
		pre_data={}
		#********* Start Grid Headings *********#
		row_dict={}
		row=[]
		module='Products'
		screen_name='list-order-grid'
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
		#********* End Grid Headings *********#
		warehouse_list = getting_warehouseId_from_channelId(channel_id)
		length_of_list = 0
		product_cond=EngageboostProducts.objects.using(company_db).all().filter(isdeleted='n',isblocked='n',website_id=website_id, product_stock__real_stock__gt=0).distinct().order_by("-id")
		if search_key is not None:
			product_cond = product_cond.filter(name__icontains=search_key)
		length_of_list = len(product_cond)
		# .values("name","sku","default_price")
		page = self.paginate_queryset(product_cond)
		page_size = get_page_size()
		re_data = {}
		if page:
			# product_list = BasicinfoSerializer(product_cond,many=True, context={'channel_id': channel_id, 'currency_id':currency_id})
			product_list = BasicinfoSerializer(page,many=True, context={'channel_id': channel_id, 'currency_id':currency_id})
			for product in product_list.data:
				real_stock = product_stock_count(product["id"],warehouse_list)
				product["real_stock"] = real_stock
			ProductListArr      = product_list.data
			pre_data['all']     = len(ProductListArr)
			pre_data['result']  = ProductListArr
			pre_data['layout']  = layout_arr
			# pre_data["results"]=results_arr
			# data={"status":1,"api_status":product_list.data,"message":"Product List"}
		else:
			ProductListArr = []
			pre_data['all'] = 0
			pre_data['result'] = []
			pre_data['layout'] = layout_arr
			# data={"status":0,"message":"No product found"}
		# product_list_data = self_pagination(ProductListArr)
		results_arr = []
		results_arr.append(pre_data)
		result = {"count":length_of_list,"per_page_count": math.ceil(length_of_list/page_size),"page_size":page_size,"results":results_arr}
		# return Response(result)
		return self.get_paginated_response(results_arr)

def getting_warehouseId_from_channelId(channel_id):
	Warehouse_list=[]
	WareHouseArrCond = EngageboostWarehouseMasterApplicableChannels.objects.filter(applicable_channel_id=channel_id,isblocked='n',isdeleted='n').all()
	if WareHouseArrCond:
		WareHouseArr = WarehousemasterapplicablechannelsSerializer(WareHouseArrCond,many=True)
		for WareHouse in WareHouseArr.data:
			if WareHouse["warehouse_master_id"]:
				Warehouse_list.append(WareHouse["warehouse_master_id"])

	return Warehouse_list

def product_stock_count(product_id, warehouse_list):
	prev_stock=0
	stock_cond = EngageboostProductStocks.objects.filter(warehouse_id__in=warehouse_list,product_id=product_id, real_stock__gt=0).all()
	# .values('product_id','warehouse_id','stock','real_stock')
	if stock_cond:
		productStocks = StockSerializer(stock_cond,many=True)
		for product_stocks in productStocks.data:
			if product_stocks["real_stock"]:
				if prev_stock <= product_stocks["real_stock"]:
					prev_stock=product_stocks["real_stock"]

	return prev_stock

def get_page_size():
	settings = EngageboostGlobalSettings.objects.get(isdeleted='n',isblocked='n',website_id=1)
	size=settings.itemlisting_backend
	return size 

def self_pagination(array_list):
	results_arr=[]
	page_size = get_page_size()
	# print(page_size)
	# print(json.dumps(array_list))
	length_of_list = len(array_list['result'])
	results_arr.append(array_list)
	result = {"count":length_of_list,"per_page_count": math.ceil(length_of_list/page_size),"page_size":page_size,"results":results_arr}
	return result

def payment_method_onepage_checkout(website_id):
	# EngageboostCompanyWebsites.objects.filter(id=website_id).all()
	website_methods=[]
	payment_setting_info_list=[]
	website_data_cond = EngageboostWebsitePaymentmethods.objects.filter(engageboost_company_website_id=website_id).all()
	website_data=WebsitePaymentmethodsSerializer(website_data_cond,many=True)
	for websitedata in website_data.data:
		website_methods.append(websitedata["engageboost_paymentgateway_method_id"])

	payment_setting_info_cond=EngageboostPaymentgatewaySettingInformation.objects.filter(website_id=website_id,isblocked='n',isdeleted='n').all()
	payment_setting_info=PaymentgatewaySettingInformationSerializer(payment_setting_info_cond,many=True)

	for payment_settinginfo in payment_setting_info.data:
		payment_setting_type=EngageboostPaymentgatewayTypes.objects.filter(id=payment_settinginfo["paymentgateway_type_id"]).first()
		payment_setting_method=EngageboostPaymentgatewayMethods.objects.filter(id=payment_settinginfo["paymentgateway_method_id"]).first()

		if payment_setting_type:
			payment_settinginfo["payment_type_name"]=payment_setting_type.name
			payment_settinginfo["payment_type_image"]=payment_setting_type.image
			payment_settinginfo["payment_type_id"]=payment_setting_type.id

		if payment_setting_method:
			payment_settinginfo["name"]=payment_setting_method.name
			payment_settinginfo["destination_url"]=payment_setting_method.destination_url
			payment_settinginfo["payment_method_id"]=payment_setting_method.id

	return payment_setting_info.data

class ProductDiscountCalculation(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		if "order_id" in request.data.keys():
			order_id = request.data["order_id"]
		else:
			order_id = ""
		company_id = request.data["company_id"]
		website_id = request.data["website_id"]
		webshop_id = request.data["webshop_id"] if request.data.get("webshop_id") else 6
		product_ids= request.data["product_ids"]
		qtys       = request.data["qtys"]
		prod_price = request.data["prod_price"]
		country_id = request.data["country_id"] if request.data.get("country_id") else ""
		state_id = request.data["state_id"] if request.data.get("state_id") else ""
		post_code = request.data["post_code"] if request.data.get("post_code") else ""
		payment_method_id = request.data["payment_method_id"] if request.data.get("payment_method_id") else None
		user_id = request.data["user_id"] if request.data.get("user_id") else None
		user_group_id = request.data["user_group_id"] if request.data.get("user_group_id") else None
		coupon_code = request.data["coupon_code"] if request.data.get("coupon_code") else None
		paid_amount = float(request.data["paid_amount"]) if request.data.get("paid_amount") else float(0)
		# warehouse_id = request.data["warehouse_id"]
		warehouse_id = request.data['warehouse_id']
		applicable_coupon_type = request.data['applicable_coupon_type']
		is_apply_wallet = request.data['is_apply_wallet']
		customer_id = request.data['customer_id']
		auth_user_id = ""
		if customer_id is not None and customer_id >0:
			rs_customer = EngageboostCustomers.objects.filter(id = customer_id).first()
			auth_user_id = rs_customer.auth_user_id

		order_id = None
		if "order_id" in request.data:
			order_id = request.data['order_id']

		redeem_amount = 0
		rule_id = 0
		# Loyalty Points
		if "redeem_amount" in request.data:
			redeem_amount = request.data["redeem_amount"]


		cartdetails=[];checkout_info=[];new_unit_netamount=[];new_total_netamount=[]
		shipper_address=EngageboostCompanyWebsites.objects.using(company_db).filter(id=website_id).first()
		cod_min_amount=cod_max_amount=None
		cod_charge=0
		if payment_method_id:
			if int(payment_method_id)==15 or int(payment_method_id)==16:
				payment_method_onepage=payment_method_onepage_checkout(website_id)
			else:
				payment_method_onepage=payment_method_onepage_checkout(website_id)
		else:
			payment_method_onepage=payment_method_onepage_checkout(website_id)

		#print(payment_method_onepage)
		# return Response(payment_method_onepage)
		for value in payment_method_onepage:
			if 'payment_type_id' in value.keys() and value['payment_type_id']==4:
				# flag=False
				if value["setting_key"]=="min_amount":
					cod_min_amount=float(value["setting_val"])
				if value["setting_key"]=="max_amount":
					cod_max_amount=float(value["setting_val"])
				if value["setting_key"]=="cod_charge":
					cod_charge=float(value["setting_val"])

		product_ids=product_ids.split(",")
		quantity=qtys.split(",")
		prod_price=prod_price.split(",")
		for index in range(len(product_ids)):
			product_id = product_ids[index]
			# checkout_info_dict = {"product_id":product_ids[index],"quantity":quantity[index],"product_price":prod_price[index]}
			# checkout_info.append(checkout_info_dict)
			new_unit_netamount.append(float(prod_price[index])/float(quantity[index]))
			new_total_netamount.append(float(prod_price[index])*float(quantity[index]))
			discount_array_net = generate_discount_conditions(website_id,user_group_id)
			# getproductforcart_net = getproductforcart(product_id)
			prod_list = []
			prod_list.append(getproductforcartNew(product_id, warehouse_id))
			getproductforcart_net = prod_list
			# print("KKKKKKKKKKKK====", json.dumps(getproductforcart_net))
			for getproductforcartnet in getproductforcart_net:
				# print("getproductforcartnet====", json.dumps(getproductforcartnet))
				getproductforcartnet["qty"]=int(quantity[index])
				itemPrice = prod_price[index]

				if int(itemPrice)<=0:
					price_obj = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=product_id,price__gte=0,product_price_type_id__price_type_id=1, warehouse_id=warehouse_id)
					if price_obj.count()>0:
						price_obj = price_obj.values().last()
						# print(price_obj)
						itemPrice = price_obj['price']

				#print(getproductforcartnet["new_default_price"])
				try:
					if getproductforcartnet["new_default_price"]: 
						if float(itemPrice) > float(0) :
							getproductforcartnet["new_default_price"] = itemPrice
						else :
							if float(itemPrice) > float(0) :
								getproductforcartnet["new_default_price"] = itemPrice
							else :
								getproductforcartnet["new_default_price"] = getproductforcartnet["default_price"]
					else:
						if float(itemPrice) > float(0) :
							getproductforcartnet["new_default_price"] = itemPrice
						else : 
							getproductforcartnet["new_default_price"] = getproductforcartnet["default_price"]
				except KeyError: 
					if float(itemPrice) > float(0) :
							getproductforcartnet["new_default_price"] = itemPrice
					else : 
						getproductforcartnet["new_default_price"] = getproductforcartnet["default_price"]
			#******************Check if it is an Existing order (Edit Order)**********************    
			if order_id and order_id!="" and order_id!=None:
				for getproductforcartnet in getproductforcart_net:
					exist_order_obj = EngageboostOrderProducts.objects.filter(order_id=order_id,product_id=product_id)
					# print("count==",exist_order_obj.query)
					if exist_order_obj.count()>0:
						itemPrice = prod_price[index]
						# print("itemPrice",itemPrice)
						exist_order = exist_order_obj.first()
						try:
							#print(exist_order.product_price)
							if float(itemPrice) > float(0) :
								if exist_order.product_price: 
									getproductforcartnet["new_default_price"] = itemPrice
									# print("itemPrice1",getproductforcartnet["new_default_price"])
								else: 
									getproductforcartnet["new_default_price"] = getproductforcartnet["default_price"]
									# print("itemPrice2",getproductforcartnet["new_default_price"])
							else :
								if exist_order.product_price:
									getproductforcartnet["new_default_price"] = exist_order.product_price
									# print("itemPrice3",getproductforcartnet["new_default_price"])
								else:
									getproductforcartnet["new_default_price"] = getproductforcartnet["default_price"]
									# print("itemPrice4",getproductforcartnet["new_default_price"])
						except KeyError: 
							getproductforcartnet["new_default_price"] = getproductforcartnet["default_price"]
							# print("itemPrice5",getproductforcartnet["new_default_price"])

						try:
							if exist_order.quantity and exist_order.deleted_quantity: 
								orderqty= int(exist_order.quantity)-int(exist_order.deleted_quantity)
								
								if orderqty<1:
									orderqty = 0

								getproductforcartnet["quantity"] = orderqty
							else: 
								getproductforcartnet["quantity"] = 1
						except KeyError: 
							getproductforcartnet["quantity"] = 1

						try:
							if exist_order.product_discount_price: 
								getproductforcartnet["discount_price"] = exist_order.product_discount_price
							else: 
								getproductforcartnet["discount_price"] = float(0)
						except KeyError: 
							getproductforcartnet["discount_price"] = float(0)
			#print(getproductforcartnet["new_default_price"])
			#********Apply Discount and Get New Product Amount********#
				# if getproductforcartnet['id']==3:
				#     print("old_default_price====",getproductforcartnet['new_default_price'])
			product_detail_net = genrate_new_prodcut_with_discount(user_id,getproductforcart_net,discount_array_net)
			product_detail_net = product_detail_net[0]
			# if product_detail_net['id']==3:
			#     print("new_default_price====",product_detail_net['new_default_price'])
			# print("*****************")
			# print(product_detail_net)
			# print("*****************")

			#********Tax Calculation********#
			# if country_id!="" or state_id!="" or post_code!="":
			tax_price_arr = get_price_including_tax(website_id,company_id,product_detail_net,country_id,state_id,post_code,'back')

			company_info = EngageboostCompanyWebsites.objects.filter(id=website_id).first()
			if company_info:
				company_state=company_info.state
			else:
				company_state=0

			if str(company_state)!=str(state_id):
				product_tax={"tax_price_unit":float(tax_price_arr["tax_igst"]),"tax_price":float(tax_price_arr["tax_igst"])*float(product_detail_net["qty"]),"tax_percentage":tax_price_arr["igst"],"tax_name":tax_price_arr["tax_name"],"cgst":tax_price_arr["cgst"],"sgst":tax_price_arr["sgst"],"igst":tax_price_arr["igst"],"cess":tax_price_arr["cess"],"is_igst":"yes","tax_type":tax_price_arr["tax_type"]}
			else:
				product_tax={"tax_price_unit":float(tax_price_arr["tax_igst"]),"tax_price":float(tax_price_arr["tax_igst"])*float(product_detail_net["qty"]),"tax_percentage":tax_price_arr["igst"],"tax_name":tax_price_arr["tax_name"],"cgst":tax_price_arr["cgst"],"sgst":tax_price_arr["sgst"],"igst":tax_price_arr["igst"],"cess":tax_price_arr["cess"],"is_igst":"no","tax_type":tax_price_arr["tax_type"]}
			
			product_detail_net=dict(product_detail_net,**product_tax)
			if product_detail_net["tax_type"]=="including":
				product_detail_net["new_default_price_unit"]=float(product_detail_net["new_default_price_unit"])-float(product_detail_net["tax_price_unit"])
				product_detail_net["new_default_price"]=float(product_detail_net["new_default_price"])-float(product_detail_net["tax_price"])
			#********Tax Calculation (END)********#

			cartdetails.append(product_detail_net)

		order_total=0
		order_weight=0
		if cartdetails:
			for products in cartdetails:
				if products["tax_type"]=="including":
					order_total = float(order_total)+float(products["new_default_price"])+float(products["tax_price"])
				else:
					order_total = float(order_total)+float(products["new_default_price"])
				if products["weight"]:
					order_weight = float(order_weight)+float(products["weight"])

		#********Shipping Calculation********#
		shipping_amount_arr={"shipping_amount":0,"mthod_type":0,"mthod_name":"orderwise","handling_fees_type":0,"handling_price":0}
		if cartdetails:
			shipping_flat = rate_flat(website_id,company_id,country_id,state_id,post_code,'back')
			shipping_table = rate_table(website_id,company_id,cartdetails,country_id,state_id,post_code,'back')
			shipping_free = rate_free(website_id,company_id,country_id,state_id)

			if shipping_flat:
				if float(shipping_flat["flat_price"])>float(0) and float(order_total)<float(shipping_free["minimum_order_amount"]):
					shipping_amount_arr={"shipping_amount":float(shipping_flat["flat_price"]),"mthod_type":shipping_flat["mthod_type"],"mthod_name":shipping_flat["mthod_name"],"handling_fees_type":shipping_flat["handling_fees_type"],"handling_price":shipping_flat["handling_price"]}

			if shipping_table:
				if float(shipping_table["flat_price"])>float(0) and float(order_total)<float(shipping_free["minimum_order_amount"]):
					shipping_amount_arr={"shipping_amount":float(shipping_table["flat_price"]),"mthod_type":shipping_table["mthod_type"],"mthod_name":shipping_table["mthod_name"],"handling_fees_type":shipping_table["handling_fees_type"],"handling_price":shipping_table["handling_price"]}
		#********Shipping Calculation (END)********#

		#********APPLY COUPON CODE********#
		if cartdetails and coupon_code is not None:
			discount_array_coupon=generate_discount_conditions_coupon(website_id,user_group_id,coupon_code)

			if discount_array_coupon and discount_array_coupon[0]["name"]!="invalid":
				if discount_array_coupon[0]["disc_type"]!=3:
					if discount_array_coupon[0]["coupon_type"]==2:
						cartdetails=genrate_new_prodcut_with_discount_coupon(user_id,cartdetails,discount_array_coupon,order_total)
					else:
						if discount_array_coupon[0]["used_coupon"]==0:
							cartdetails=genrate_new_prodcut_with_discount_coupon(user_id,cartdetails,discount_array_coupon,order_total)
				else:
					if discount_array_coupon[0]["coupon_type"]==2:
						coupon_details=genrate_new_prodcut_with_discount_coupon_order_total(user_id,cartdetails,discount_array_coupon,order_total)
					else:
						if discount_array_coupon[0]["used_coupon"]==0:
							coupon_details=genrate_new_prodcut_with_discount_coupon_order_total(user_id,cartdetails,discount_array_coupon,order_total)
		#********APPLY COUPON CODE (END)********#
		postdata=[]
		applied_coupon=[]
		order_total=0
		order_weight=0
		total_tax=0
		shipping_amount=0
		handling_charge=0
		order_total_with_handling_price=0
		gross_discount_amount = 0
		grandtotal=subtotal=nettotal=cart_discount=0
		if cartdetails:
			for products in cartdetails:
				order_total = float(order_total)+float(products["new_default_price"])+float(products["tax_price"])
				total_tax = float(total_tax)+float(products["tax_price"])
				#********PRODUCT TOTAL DISCOUNT (EXCLUDING WHOLE CART DISCOUNT)********#
				gross_discount_amount = float(gross_discount_amount)+float(products["discount_price"])

				if shipping_amount_arr["mthod_type"]!=0:
					shipping_price=float(shipping_amount_arr["shipping_amount"])*float(products["qty"])
					shipping_amount=float(shipping_amount)+float(shipping_price)
				else:
					shipping_amount=float(shipping_amount_arr["shipping_amount"])

			if shipping_amount_arr["handling_fees_type"]==0:
				handling_charge = shipping_amount_arr["handling_price"]
				order_total_with_handling_price = float(order_total)+float(handling_charge)
			else:
				handling_charge = float(order_total)*float(shipping_amount_arr["handling_price"])/float(100)
				order_total_with_handling_price = float(order_total)+float(handling_charge)

			#********TOTAL AMOUNT PRODUCT PRICE + SHIPPING CHARGE + HANDLING CHARGE ********#
			grandtotal = float(order_total_with_handling_price)+float(shipping_amount)

			#********APPLY COD CHAGE********#
			if cod_min_amount is not None and cod_max_amount is not None:
				if float(cod_min_amount)<=float(grandtotal) and float(grandtotal)<=float(cod_max_amount):
					grandtotal = float(grandtotal)+float(cod_charge)
					applied_cod_charge = float(cod_charge)
				else:
					grandtotal = grandtotal
					applied_cod_charge = float(0)
			else:
				grandtotal = grandtotal
				applied_cod_charge = float(0)

			#********APPLY COUPON DISCOUNT ON WHOLE CART********#
			if coupon_code is not None:
				if discount_array_coupon and discount_array_coupon[0]["name"]!="invalid":
					# print('discount_array_coupon===========', json.dumps(discount_array_coupon))
					# print("coupon_details==============", json.dumps(coupon_details))
					if discount_array_coupon[0]["disc_type"]==3:
						grandtotal = float(grandtotal)
						# subtotal = float(grandtotal)-float(coupon_details["coupon_discount_amount"])
						subtotal = float(order_total)
						cart_discount = float(grandtotal)-float(subtotal)
					else:
						grandtotal = float(grandtotal)
						subtotal = float(order_total)
						cart_discount = float(grandtotal)-float(subtotal)  # - shupping_charge

					applied_coupon_dict={"status": 1 ,"name":discount_array_coupon[0]["name"],"coupon_code":discount_array_coupon[0]["coupon_code"],"disc_type":discount_array_coupon[0]["disc_type"],"amount":discount_array_coupon[0]["amount"]}
					applied_coupon.append(applied_coupon_dict)
				else:
					grandtotal = float(grandtotal)
					subtotal = float(grandtotal)
					cart_discount = float(grandtotal)-float(subtotal) # - shipping_charge
					applied_coupon_dict={"status": 0,"name":discount_array_coupon[0]["name"],"coupon_code":discount_array_coupon[0]["coupon_code"],"message":discount_array_coupon[0]["message"]}
					applied_coupon.append(applied_coupon_dict)
			else:
				grandtotal = float(grandtotal)
				subtotal = float(grandtotal)
				cart_discount = float(grandtotal)-float(subtotal)   # -shipping_charge
			#********APPLY COUPON DISCOUNT ON WHOLE CART(END)********#
		if coupon_code is not None and applied_coupon_dict:
			cart_discount = applied_coupon_dict["amount"]
		nettotal = float(subtotal)-float(total_tax)-float(handling_charge)-float(applied_cod_charge) #-float(shipping_amount)
		balance_due = float(subtotal)-float(paid_amount)
		grandtotal = float(grandtotal) - float(cart_discount)
		subtotal = order_total
		postdata_dict={"company_id":company_id,"website_id":website_id,"webshop_id":webshop_id,"payment_method_id":payment_method_id,"tax_amount":total_tax,"shipping_charge":shipping_amount,"handling_charge":handling_charge,"cod_charge":applied_cod_charge,"gross_discount":gross_discount_amount,"min_amount":cod_min_amount,"max_amount":cod_max_amount,"grand_total":grandtotal,"sub_total":subtotal,"net_total":nettotal,"cart_discount":cart_discount,"paid_amount":paid_amount,"balance_due":balance_due}
		postdata.append(postdata_dict)
		
		# Change
		if applicable_coupon_type =='loaddata' and is_apply_wallet==0:
			redeem_amount = 0
		elif applicable_coupon_type =='applycode' and is_apply_wallet==0:
			redeem_amount = 0
		else:
			print("k")
			cartData = {
				"orderamountdetails":[
					{
						"website_id": 1,
						"webshop_id": 6,
						"sub_total": subtotal,
						"net_total": nettotal,
					}
				],
				"cartdetails":cartdetails,
				"user_id":auth_user_id
			}

			ret_loyalty = ApplyLoyalty(cartData)
			redeem_amount = ret_loyalty["usable_loyalty"]
		if float(redeem_amount) > 0:
			net_total = float(postdata[0]['net_total'])
			if (float(postdata[0]['grand_total'])-float(postdata[0]['shipping_charge']))>float(redeem_amount):
				postdata[0]['net_total'] = float(net_total)
				postdata[0]['balance_due'] = float(postdata[0]['balance_due']) - float(redeem_amount)
				postdata[0]['applied_loyalty_amount'] = redeem_amount
				postdata[0]['grand_total'] = float(postdata[0]['grand_total']) - float(redeem_amount)
			else:
				redeem_amount = float(postdata[0]['grand_total'])-float(postdata[0]['shipping_charge'])
				postdata[0]['net_total'] = float(net_total)
				postdata[0]['balance_due'] = float(postdata[0]['balance_due']) - float(redeem_amount)
				postdata[0]['applied_loyalty_amount'] = redeem_amount
				postdata[0]['grand_total'] = float(postdata[0]['grand_total'])- float(redeem_amount)
		else:
			postdata[0]['net_total'] = float(postdata[0]['net_total'])
			postdata[0]['grand_total'] = float(postdata[0]['grand_total'])
			postdata[0]['applied_loyalty_amount'] = redeem_amount
		
		if applicable_coupon_type =='loaddata':
			rs_order = EngageboostOrdermaster.objects.filter(id = order_id).first()
			if rs_order:
				postdata[0]['net_total'] = float(rs_order.net_amount)
				postdata[0]['applied_loyalty_amount'] = rs_order.pay_wallet_amount
				postdata[0]['grand_total'] = float(postdata[0]['grand_total'])-float(rs_order.cart_discount)-float(rs_order.pay_wallet_amount)
				# postdata[0]["shipping_charge"]=rs_order.shipping_cost
				# postdata[0]["cod_charge"]=rs_order.cod_charge
				# postdata[0]["gross_discount"]=rs_order.gross_discount_amount
				postdata[0]["cart_discount"]=rs_order.cart_discount
				# postdata[0]["paid_amount"]=rs_order.paid_amount
				postdata[0]["balance_due"]=float(postdata[0]["balance_due"])-float(rs_order.pay_wallet_amount)

		# data={"cartdetails":cartdetails,"postdata":postdata,"min_amount":cod_min_amount,"max_amount":cod_max_amount,"cod_charge":cod_charge,"shipping_flat":shipping_flat,"shipping_table":shipping_table,"shipping_free":shipping_free,"discount_array_coupon":discount_array_coupon}
		data={"cartdetails":cartdetails,"postdata":postdata,"applied_coupon":applied_coupon,"shipping_flat":shipping_flat,"shipping_table":shipping_table}

		return Response(data)

def generate_discount_conditions(website_id,user_group_id,discountIds=None, warehouse_id = None):
	now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
	if user_group_id:
		if warehouse_id is not None:
			DiscountMasterCond = EngageboostDiscountMasters.objects.order_by("discount_priority").filter(website_id=website_id,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc,customer_group__iregex=r"\y{0}\y".format(user_group_id),isdeleted='n',isblocked='n',discount_master_type=0, warehouse_id__iregex=r"\y{0}\y".format(warehouse_id)).all()
		else:
			DiscountMasterCond = EngageboostDiscountMasters.objects.order_by("discount_priority").filter(website_id=website_id,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc,customer_group__iregex=r"\y{0}\y".format(user_group_id),isdeleted='n',isblocked='n',discount_master_type=0).all()
	else:
		if warehouse_id is not None:
			DiscountMasterCond = EngageboostDiscountMasters.objects.order_by("discount_priority").filter(website_id=website_id,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc,isdeleted='n',isblocked='n',discount_master_type=0, warehouse_id__iregex=r"\y{0}\y".format(warehouse_id)).all()
		else:
			DiscountMasterCond = EngageboostDiscountMasters.objects.order_by("discount_priority").filter(website_id=website_id,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc,isdeleted='n',isblocked='n',discount_master_type=0).all()
	if discountIds:
		DiscountMasterCond = DiscountMasterCond.filter(id__in=discountIds)

	DiscountMasterSerializerData = DiscountMasterSerializer(DiscountMasterCond,many=True)
	if DiscountMasterSerializerData:
		for DiscountMaster in DiscountMasterSerializerData.data:
			DiscountMastersConditionsCond = EngageboostDiscountMastersConditions.objects.filter(discount_master_id=DiscountMaster["id"]).all()
			if DiscountMastersConditionsCond:
				DiscountMastersConditionsSerializerData = DiscountConditionsSerializer(DiscountMastersConditionsCond,many=True)
				DiscountMastersConditionsSerializerData = DiscountMastersConditionsSerializerData.data
			else:
				DiscountMastersConditionsSerializerData = []

			DiscountMaster["discount_conditions"] = DiscountMastersConditionsSerializerData

	return DiscountMasterSerializerData.data

# Chakradhar working substitute product...
def getproductforcartNew(product_id, warehouse_id=None):
	condition = EngageboostProducts.objects.filter(id=product_id).first()
	if warehouse_id is not None:
		context = {"warehouse_id": warehouse_id}
		product_details = BasicinfoSerializer(condition, context=context)
	else:
		product_details = BasicinfoSerializer(condition)
	product_details = product_details.data
	qs_price_data = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=product_id, warehouse_id=warehouse_id)
	if qs_price_data.count()>0:
		qs_price_data = qs_price_data.first()
		product_details.update({"channel_price":qs_price_data.price})
		product_details['default_price'] = qs_price_data.price
	else:
		product_details.update({"channel_price":0})
		product_details['default_price'] = 0
	return product_details
	
def getproductforcart(product_id):
	# condition = EngageboostProducts.objects.filter(isdeleted='n',isblocked='n',id=product_id).all().values("id","name","brand","hsn_id","sku","slug","description","default_price","weight","taxclass_id","amazon_itemid","twitter_addstatus","amazon_addstatus","status", "warehouse")
	condition = EngageboostProducts.objects.filter(isdeleted='n',isblocked='n',id=product_id).all()

	product_details = BasicinfoSerializer(condition,many=True)
	conditions = EngageboostProductCategories.objects.filter(product_id=product_id).first()

	if conditions:
		product_details.data[0]["category_id"]=conditions.category_id
	
	return product_details.data

def genrate_new_prodcut_with_discount(user_id=None,product_array=None,discount_array_new=None,category_id=None,sub_category_id=None,cart_subtotal=None):
	if "new_default_price" in product_array[0].keys():
		if product_array[0]["new_default_price"]!="" and product_array[0]["new_default_price"]!=None:
			old_price = product_array[0]["new_default_price"]
		else:
			old_price = 0
	if discount_array_new:
		print('genrate_new_prodcut_with_discount')
		for discount_array in discount_array_new:
			# print("==================",discount_array,"======================")
			for product in product_array:
				return_price = check_in_prod_disc(user_id,product,discount_array,category_id,sub_category_id,cart_subtotal)
				price_array = return_price.split('^')
				print("#########",return_price)
				if price_array[1] != "product" and float(price_array[1]) > 0 and float(product["new_default_price"]) != float(price_array[0]):
					product["new_default_price_unit"] = float(old_price)
					product["new_default_price"] = float(float(old_price)-float(price_array[1]))*float(product["qty"])
					product["discount_price_unit"] = float(price_array[1])
					product["discount_price"] = float(price_array[1])*float(product["qty"])
					product["discount_amount"] = float(discount_array["amount"])
					product["disc_type"] = discount_array["disc_type"]
					product["coupon"] = discount_array["name"]
				else:
					product["new_default_price_unit"] = float(old_price)
					product["new_default_price"] = float(product["new_default_price_unit"])*float(product["qty"])
					product["discount_price_unit"] = float(price_array[1])
					product["discount_price"] = float(price_array[1])*float(product["qty"])
					product["discount_amount"] = float(0)
					product["disc_type"] = ""
					product["coupon"] = ""
	else:
		for product in product_array:
			product["new_default_price_unit"] = float(old_price)
			product["new_default_price"] = float(product["new_default_price_unit"])*float(product["qty"])
			product["discount_price_unit"] = float(0)
			product["discount_price"] = float(0)*float(product["qty"])
			product["discount_amount"] = float(0)
			product["disc_type"] = ""
			product["coupon"] = ""
	return product_array

def check_in_prod_disc(user_id=None,ind_product=None,discount_array=None,category_id=None,sub_category_id=None,cart_subtotal=None):
	discount_array_condition = discount_array["discount_conditions"]
	product_array_disc_applied = []
	i=0
	previos_flag = ""
	# if ind_product["id"]==3:
	#     print("Here==============",ind_product["default_price"])
	for ind_cond in discount_array_condition:
		if ind_cond["fields"]==-1:
			if cart_subtotal:
				if ind_cond["condition"] == "==":
					flag = "true" if float(cart_subtotal) == float(ind_cond["value"]) else "false"
				elif ind_cond["condition"] == ">=":
					flag = "true" if float(cart_subtotal) >= float(ind_cond["value"]) else "false"
				else:
					flag = "false" if float(cart_subtotal) >= float(ind_cond["value"]) else "true"
			else:
				flag = "false"
		elif ind_cond["all_category_id"]:
			category_id_array = ind_cond["all_category_id"].split(",")
			find_category = EngageboostProductCategories.objects.filter(product_id=ind_product["id"]).all()
			
			sub_category_id_array = []
			
			if find_category:
				ptcArr = ProductCategoriesSerializer(find_category,many=True)
				for pro in ptcArr.data:
					sub_category_id_array.append(pro["category"]["id"])
			if sub_category_id_array:
				for index in range(len(sub_category_id_array)):
					if ind_cond["condition"] == "==":
						if str(sub_category_id_array[index]) in category_id_array:
							flag = "true"
							break
						else:
							flag = "false"
					else:
						if sub_category_id_array[index] in category_id_array:
							flag = "false"
							break
						else:
							flag = "true"
			else:
				if ind_cond["condition"] == "==": 
					if category_id in category_id_array:
						flag = "true"
					else:
						flag = "false"
				else:
					if category_id in category_id_array:
						flag = "false"
					else:
						flag = "true"
		elif ind_cond["all_product_id"]:
			product_id_array = ind_cond["all_product_id"].split(",")
			if ind_cond["condition"] == "==":
				if str(ind_product["id"]) in product_id_array:
					flag = "true"
				else:
					flag = "false"
			else:
				if ind_product["id"] in product_id_array:
					flag = "false"
				else:
					flag = "true"
		elif ind_cond["all_customer_id"]:
			customer_id_array = ind_cond["all_customer_id"].split(",")
			if user_id:
				if ind_cond["condition"] == "==":
					if user_id in customer_id_array:
						flag = "true"
					else:
						flag = "false"
				else:
					if user_id in customer_id_array:
						flag = "false"
					else:
						flag = "true"
			else:
				flag = "false"
		if i!=0:
			if previos_condition=="AND":
				if flag=="true" and previos_flag=="true":
					previos_flag="true"
				else:
					previos_flag="false"

			if previos_condition=="OR":
				if flag=="false" and previos_flag=="false":
					previos_flag="false"
				else:
					previos_flag="true"
		else:
			previos_flag = flag

		previos_condition=ind_cond["condition_type"]
		i=i+1
	if previos_flag == "true":
		if discount_array["disc_type"]==1:
			discount_array["discountPrice"]=float(ind_product["default_price"])*float(discount_array["amount"])/float(100)
		else:
			discount_array["discountPrice"]=float(discount_array["amount"])

		if discount_array["disc_type"]!=4:
			if ind_product["new_default_price"]:
				if ind_product["new_default_price"]=="0":
					if float(ind_product["default_price"])>float(discount_array["discountPrice"]):
						default_price=float(ind_product["default_price"])-float(discount_array["discountPrice"])
						discount_price=float(ind_product["discount_price"])+float(discount_array["discountPrice"])
					else:
						default_price=float(ind_product["default_price"])
						discount_price=float(ind_product["discount_price"])
					product_array_disc_applied.append(ind_product["id"])
				else:
					if float(ind_product["default_price"])>float(discount_array["discountPrice"]):
						default_price = float(ind_product["new_default_price"])-float(discount_array["discountPrice"])
						discount_price = float(discount_array["discountPrice"])
						
					else:
						default_price = float(ind_product["new_default_price"])
						discount_price = float(0)
					product_array_disc_applied.append(ind_product["id"])
			else:
				if float(ind_product["default_price"])>float(discount_array["discountPrice"]):
					default_price=float(ind_product["default_price"])-float(discount_array["discountPrice"])
					discount_price=float(discount_array["discountPrice"])
					product_array_disc_applied.append(ind_product["id"])
				else:
					default_price  = float(0)
					discount_price = float(0)
		else:
			default_price = discount_array["product_id"]
			discount_price = "product"
	else:
		if ind_product["new_default_price"]:
			default_price = float(ind_product["new_default_price"])
			discount_price = float(0)
			# print("default_price======",ind_product)
		else:
			default_price  = float(0)
			discount_price = float(0)
	return str(default_price)+"^"+str(discount_price)

def get_price_including_tax(website_id='1',company_id=None,product_arr=None,country_id=None,state_id=None,post_code=None,order_from='front'):
	state_id=state_id
	tax_price_arr = []
	tax_price = "0.00"
	excise_duty = "0.00"
	discount_price = "0.00"
	coupon_disc_amount_nw = "0.00"
	is_tax_find = 'No'
	tax_name = ""
	tax_rate = "0.00"
	rate_of_duty  = "0.00"
	tax_type = "excluding"

	globalsettings = EngageboostGlobalSettings.objects.get(website_id=website_id)
	if globalsettings.applicable_tax=="GST":
		if product_arr["hsn_id"]:
			hsnDetails = EngageboostHsnCodeMaster.objects.filter(id=product_arr["hsn_id"]).first()
			if hsnDetails:
				tax_rate = hsnDetails.igst
				if tax_type=="excluding":
					tax_price = float(product_arr["new_default_price_unit"])*float(tax_rate)/float(100)
					data={"tax_cgst":float(tax_price)/float(2),"tax_sgst":float(tax_price)/float(2),"tax_igst":float(tax_price),"tax_name":hsnDetails.hsn_code,"cgst":float(tax_rate)/float(2),"sgst":float(tax_rate)/float(2),"igst":float(tax_rate),"cess":float(hsnDetails.cess),"tax_type":"excluding"}
				else:
					tax_price = (float(product_arr["new_default_price_unit"])*float(tax_rate))/(float(100)+float(tax_rate))
					data={"tax_cgst":float(tax_price)/float(2),"tax_sgst":float(tax_price)/float(2),"tax_igst":float(tax_price),"tax_name":hsnDetails.hsn_code,"cgst":float(tax_rate)/float(2),"sgst":float(tax_rate)/float(2),"igst":float(tax_rate),"cess":float(hsnDetails.cess),"tax_type":"including"}
			else:
				data={"tax_cgst":float(0),"tax_sgst":float(0),"tax_igst":float(0),"tax_name":"","cgst":float(0),"sgst":float(0),"igst":float(0),"cess":float(0),"tax_type":""}
		else:
			data={"tax_cgst":float(0),"tax_sgst":float(0),"tax_igst":float(0),"tax_name":"","cgst":float(0),"sgst":float(0),"igst":float(0),"cess":float(0),"tax_type":""}
	elif globalsettings.applicable_tax=="VAT":
		# print("vat",product_arr)
		if product_arr['taxclass']:
			# print("Tax Class Id=====",product_arr['taxclass']['id'])
			taxclassId=str(product_arr['taxclass']['id'])
			taxRuleObj = EngageboostTaxRuleTables.objects.filter(isblocked='n',isdeleted='n')
			taxRuleObj = taxRuleObj.filter( Q(product_tax_class_id__startswith=taxclassId+',') | Q(product_tax_class_id__endswith=','+taxclassId) | Q(product_tax_class_id__contains=',{0},'.format(taxclassId)) | Q(product_tax_class_id__exact=taxclassId) )
			taxRuleObj = taxRuleObj.first()
			if taxRuleObj:   
				taxRateObj = EngageboostTaxRates.objects.filter(id=taxRuleObj.tax_rate_id,isblocked='n',isdeleted='n')
				if taxRateObj.count()>0:
					taxRates = taxRateObj.first()
					tax_rate = taxRates.percentage
					tax_price = float(product_arr["new_default_price_unit"])*float(tax_rate)/float(100)
					tax_settings = EngageboostTaxSettings.objects.first()
					data={"tax_cgst":float(tax_price)/float(2),"tax_sgst":float(tax_price)/float(2),"tax_igst":float(tax_price),"tax_name":taxRates.name,"cgst":float(tax_rate)/float(2),"sgst":float(tax_rate)/float(2),"igst":float(tax_rate),"cess":0.00,"tax_type":tax_settings.catalog_prices}
				else:
					data={"tax_cgst":float(0),"tax_sgst":float(0),"tax_igst":float(0),"tax_name":"","cgst":float(0),"sgst":float(0),"igst":float(0),"cess":float(0),"tax_type":""}
			else:
				data={"tax_cgst":float(0),"tax_sgst":float(0),"tax_igst":float(0),"tax_name":"","cgst":float(0),"sgst":float(0),"igst":float(0),"cess":float(0),"tax_type":""}
		else:
			data={"tax_cgst":float(0),"tax_sgst":float(0),"tax_igst":float(0),"tax_name":"","cgst":float(0),"sgst":float(0),"igst":float(0),"cess":float(0),"tax_type":""}
	return data

def rate_flat(website_id='1',company_id=None,country_id=None,state_id=None,post_code=None,order_from='front'):
	#******** FOR FLAT RATE CALCULATION ********#
	if state_id:
		conditions = EngageboostShippingMastersSettings.objects.filter(website_id=website_id,country_ids__iregex=r"\y{0}\y".format(country_id),state_id__iregex=r"\y{0}\y".format(state_id),shipping_method_id='4',isblocked='n',isdeleted='n').all()
	else:
		conditions = EngageboostShippingMastersSettings.objects.filter(website_id=website_id,country_ids__iregex=r"\y{0}\y".format(country_id),shipping_method_id='4',isblocked='n',isdeleted='n').all()

	data={"shipping_type":"Flat Shipping","mthod_type":0,"mthod_name":"orderwise","flat_price":float(0),"handling_fees_type":0,"handling_price":float(0)}

	if conditions:
		settings_info = ShippingMastersSettingsSerializer(conditions,many=True)
		for settingsinfo in settings_info.data:
			data={}
			if settingsinfo["mthod_type"]:
				if settingsinfo["mthod_type"]=="1": #****ITEMWISE
					if float(settingsinfo["flat_price"])>float(0):
						data={"shipping_type":"Flat Shipping","shipping_setting_id":settingsinfo["id"],"mthod_type":1,"mthod_name":"itemwise","flat_price":float(settingsinfo["flat_price"])}
					else:
						data={"shipping_type":"Flat Shipping","mthod_type":1,"mthod_name":"itemwise","flat_price":float(0)}
				else:
					if float(settingsinfo["flat_price"])>float(0):
						data={"shipping_type":"Flat Shipping","shipping_setting_id":settingsinfo["id"],"mthod_type":0,"mthod_name":"orderwise","flat_price":float(settingsinfo["flat_price"])}
					else:
						data={"shipping_type":"Flat Shipping","mthod_type":0,"mthod_name":"orderwise","flat_price":float(0)}
			else:
				data={"shipping_type":"Flat Shipping","mthod_type":0,"mthod_name":"orderwise","flat_price":float(0)}

			if settingsinfo["handling_fees_type"] is not None:
				if settingsinfo["handling_fees_type"]==0: #****FIXED PRICE
					if float(settingsinfo["handling_price"])>float(0):
						d1={"shipping_type":"Flat Shipping","handling_fees_type":0,"handling_price":float(settingsinfo["handling_price"])}
					else:
						d1={"shipping_type":"Flat Shipping","handling_fees_type":0,"handling_price":float(0)}
				else:
					if float(settingsinfo["handling_price"])>float(0):
						d1={"shipping_type":"Flat Shipping","handling_fees_type":1,"handling_price":float(settingsinfo["handling_price"])}
					else:
						d1={"shipping_type":"Flat Shipping","handling_fees_type":1,"handling_price":float(0)}
			else:
				d1={"shipping_type":"Flat Shipping","handling_fees_type":0,"handling_price":float(0)}

			data=dict(data,**d1)
	#******** FOR FLAT RATE CALCULATION (END) ********#
	return data

def rate_table(website_id='1',company_id=None,cartdetails=None,country_id=None,state_id=None,post_code=None,order_from='front'):
	data={"shipping_type":"Table Rate Shipping","mthod_type":0,"mthod_name":"orderwise","flat_price":float(0),"handling_fees_type":0,"handling_price":float(0)}
	order_total=0
	order_weight=0
	for products in cartdetails:
		if products["tax_type"]=="including":
			order_total = float(order_total)+float(products["new_default_price"])+float(products["tax_price"])
		else:
			order_total = float(order_total)+float(products["new_default_price"])
		if products["weight"]:
			order_weight = float(order_weight)+float(products["weight"])

	#******** FOR TABLE RATE CALCULATION ********#
	conditionss = EngageboostShippingMastersSettings.objects.order_by("id").filter(website_id=website_id,shipping_method_id='5',isblocked='n',isdeleted='n').all()
	if conditionss:
		settings_info2 = ShippingMastersSettingsSerializer(conditionss,many=True)
		for settingsinfos in settings_info2.data:
			if country_id:
				conditions2 = EngageboostShippingTableRateOrderAmount.objects.order_by("id").filter(shipping_masters_setting_id=settingsinfos["id"],country_id__iregex=r"\y{0}\y".format(country_id)).all()
			else:
				conditions2 = EngageboostShippingTableRateOrderAmount.objects.order_by("id").filter(shipping_masters_setting_id=settingsinfos["id"]).all()

			if state_id:
				conditions2 = conditions2.order_by("id").filter(shipping_masters_setting_id=settingsinfos["id"],state_id__iregex=r"\y{0}\y".format(state_id)).all()
			else:
				conditions2 = conditions2

			if post_code:
				conditions2 = conditions2.order_by("id").filter(shipping_masters_setting_id=settingsinfos["id"],zip_code__iregex=r"\y{0}\y".format(post_code)).all()
			else:
				conditions2 = conditions2

			if conditions2:
				settings_order_amount_info = ShippingTableRateOrderAmountSerializer(conditions2,many=True)

				for settings_orderamount_info in settings_order_amount_info.data:
					if settings_orderamount_info["order_subtotal"]:
						if float(order_total)>=float(settings_orderamount_info["order_subtotal"]):
							data={"shipping_type":"Table Rate Shipping","shipping_setting_id":settings_orderamount_info["id"],"mthod_type":1,"mthod_name":"orderwise","flat_price":float(settings_orderamount_info["shipping_price"])}

					if settings_orderamount_info["weight"]:
						if float(order_weight)>=float(settings_orderamount_info["weight"]):
							data={"shipping_type":"Table Rate Shipping","shipping_setting_id":settings_orderamount_info["id"],"mthod_type":0,"mthod_name":"orderwise","flat_price":float(settings_orderamount_info["shipping_price"])}
			 
			if settingsinfos["handling_fees_type"] is not None:
				if int(settingsinfos["handling_fees_type"])==0: #****FIXED PRICE
					if float(settingsinfos["handling_price"])>float(0):
						d1={"handling_fees_type":0,"handling_price":float(settingsinfos["handling_price"])}
					else:
						d1={"handling_fees_type":0,"handling_price":float(0)}
				else:
					if float(settingsinfos["handling_price"])>float(0):
						d1={"handling_fees_type":1,"handling_price":float(settingsinfos["handling_price"])}
					else:
						d1={"handling_fees_type":1,"handling_price":float(0)}
			else:
				d1={"handling_fees_type":0,"handling_price":float(0)}

			data=dict(data,**d1)
	Obj = EngageboostTaxSettings.objects.filter(website_id=website_id)
	if Obj.count()>0:
		taxData = Obj.first()
		# print(taxData.shipping_tax_rate)
		shipping_price = data['flat_price']
		tax_rate = float(taxData.shipping_tax_rate) if taxData.shipping_tax_rate else float(0)
		shipping_tax_type = taxData.shipping_price if taxData.shipping_price else "Excluding Tax"

		if shipping_tax_type=="1Excluding Tax":
			tax_price = float(shipping_price)*float(tax_rate)/float(100)
			d1={"shipping_igst":tax_price,"shipping_cgst":float(0),"shipping_sgst":float(0),"shipping_cess":float(0),"tax_type":"excluding"}
		else:
			tax_price = (float(shipping_price)*float(tax_rate))/(float(100)+float(tax_rate))
			d1={"shipping_igst":tax_price,"shipping_cgst":float(0),"shipping_sgst":float(0),"shipping_cess":float(0),"tax_type":"including"}

		data=dict(data,**d1)
	#******** FOR TABLE RATE CALCULATION (END) ********#
	return data

def rate_free(website_id='1',company_id=None,country_id=None,state_id=None):
	minimum_order_amount=0
	data={"minimum_order_amount":minimum_order_amount}

	conditions = EngageboostShippingMastersSettings.objects.order_by("id").filter(website_id=website_id,shipping_method_id='6',isblocked='n',isdeleted='n').all()
	if country_id:
		conditions = conditions.order_by("id").filter(country_ids__iregex=r"\y{0}\y".format(country_id)).all()
	else:
		conditions = conditions

	if state_id:
		conditions = conditions.order_by("id").filter(state_id__iregex=r"\y{0}\y".format(state_id)).all()
	else:
		conditions = conditions

	if conditions:
		settings_info = ShippingMastersSettingsSerializer(conditions,many=True)
		for settingsinfo in settings_info.data:
			if settingsinfo["minimum_order_amount"] is not None:
				data={"shipping_setting_id":settingsinfo["id"],"minimum_order_amount":float(settingsinfo["minimum_order_amount"])}
	return data

def generate_discount_conditions_coupon(website_id,user_group_id=None,coupon_code=None):
	now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
	all_discount_data=[]
	discount_multi_coupon=EngageboostDiscountMastersCoupons.objects.filter(isdeleted='n',coupon_code__iexact=coupon_code).first()
	#discount_multi_coupon=EngageboostDiscountMastersCoupons.objects.filter(isdeleted='n',coupon_code__iregex=r'(' + '|'.join(coupon_code.lower()) + ')').first()
	if discount_multi_coupon:
		discount_master_id=discount_multi_coupon.discount_master_id
		condition_discount_coupon_part=EngageboostDiscountMasters.objects.filter(id=discount_master_id).all()
	else:
		condition_discount_coupon_part=EngageboostDiscountMasters.objects.filter(coupon_code__iexact=coupon_code).all()
		#condition_discount_coupon_part=EngageboostDiscountMasters.objects.filter(coupon_code__iregex=r'(' + '|'.join(coupon_code.lower()) + ')').all()

	if condition_discount_coupon_part:
		condition_discount_coupon_part=condition_discount_coupon_part.filter(website_id=website_id,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc,isdeleted='n',isblocked='n',discount_master_type='1').all()
		if user_group_id:
			condition_discount_coupon_part=condition_discount_coupon_part.filter(customer_group__iregex=r"\y{0}\y".format(user_group_id)).all()

		if condition_discount_coupon_part:
			condition_discount_coupon_part_serialize=DiscountMasterSerializer(condition_discount_coupon_part,many=True)
			for condition_discount_coupon in condition_discount_coupon_part_serialize.data:
				discount_master_condition = EngageboostDiscountMastersConditions.objects.order_by("id").filter(discount_master_id=condition_discount_coupon["id"]).all()
				if discount_master_condition:
					discount_master_condition_serializer = DiscountConditionsSerializer(discount_master_condition,many=True)
					condition_discount_coupon["DiscountMasterCondition"]=discount_master_condition_serializer.data

				discount_master_coupon = EngageboostDiscountMastersCoupons.objects.order_by("id").filter(discount_master_id=condition_discount_coupon["id"],isdeleted='n').all()
				if discount_master_coupon:
					discount_master_coupon_serializer = DiscountMasterCouponSerializer(discount_master_coupon,many=True)
					condition_discount_coupon["DiscountMasterCoupon"]=discount_master_coupon_serializer.data

			all_discount_data=condition_discount_coupon_part_serialize.data
		else:
			data={"name":"invalid","coupon_code":coupon_code,"message":"Coupon code expired or condition not satisfied."}
			all_discount_data.append(data)
	else:
		data={"name":"invalid","coupon_code":coupon_code,"message":"Invalid Coupon Code"}
		all_discount_data.append(data)
	
	return all_discount_data

def genrate_new_prodcut_with_discount_coupon(user_id=None,cartdetails=None,discount_array_coupon=None,order_total=None):
	for discount_array in discount_array_coupon:
		for product in cartdetails:
			# product = getproductforcart(product_detail["id"])
			return_price = check_in_prod_disc_coupon(user_id,product,discount_array,order_total)
			# print("Return Price ======",return_price)
			price_array = return_price.split('^')
			if price_array[2] != "false":
				product["new_default_price_unit"] = float(price_array[0])
				product["new_default_price"] = float(price_array[0])*float(product["qty"])
				product["discount_price_unit"] = float(product["discount_price_unit"])+float(price_array[1])
				product["discount_price"] = float(product["discount_price"])+float(price_array[1])*float(product["qty"])
				product["coupon_discount_amount"] = float(discount_array["amount"])
				product["coupon_disc_type"] = discount_array["disc_type"]
				product["coupon_name"] = discount_array["name"]
				product["coupon_code"] = discount_array["coupon_code"]
			else:
				product["coupon_discount_amount"] = float(0)
				product["coupon_disc_type"] = ""
				product["coupon_name"] = ""
				product["coupon_code"] = ""

	return cartdetails

def check_in_prod_disc_coupon(user_id=None,ind_product=None,discount_array=None,cart_subtotal=None):
	discount_array_condition = discount_array["DiscountMasterCondition"]
	product_array_disc_applied = []
	i=0
	flag = "false"
	for ind_cond in discount_array_condition:
		if ind_cond["fields"]==-1:
			if cart_subtotal:
				if ind_cond["condition"] == "==":
					flag = "true" if float(cart_subtotal) == float(ind_cond["value"]) else "false"
				elif ind_cond["condition"] == ">=":
					flag = "true" if float(cart_subtotal) >= float(ind_cond["value"]) else "false"
				else:
					flag = "false" if float(cart_subtotal) >= float(ind_cond["value"]) else "true"
			else:
				flag = "false"
		elif ind_cond["all_category_id"]:
			category_id_array = ind_cond["all_category_id"].split(",")
			find_category = EngageboostProductCategories.objects.filter(product_id=ind_product["id"]).all()
			
			sub_category_id_array = []
			
			if find_category:
				ptcArr = ProductCategoriesSerializer(find_category,many=True)
				for pro in ptcArr.data:
					sub_category_id_array.append(pro["category"]["id"])

			if sub_category_id_array:
				for index in range(len(sub_category_id_array)):
					if ind_cond["condition"] == "==":
						if sub_category_id_array[index] in category_id_array:
							flag = "true"
							break
						else:
							flag = "false"
					else:
						if sub_category_id_array[index] in category_id_array:
							flag = "false"
							break
						else:
							flag = "true"
			else:
				if ind_cond["condition"] == "==": 
					if ind_product["category_id"] in category_id_array:
						flag = "true"
					else:
						flag = "false"
				else:
					if ind_product["category_id"] in category_id_array:
						flag = "false"
					else:
						flag = "true"
		elif ind_cond["all_product_id"]:
			product_id_array = ind_cond["all_product_id"].split(",")
			if ind_cond["condition"] == "==":
				if str(ind_product["id"]) in product_id_array:
					flag = "true"
				else:
					flag = "false"
			else:
				if ind_product["id"] in product_id_array:
					flag = "false"
				else:
					flag = "true"
		elif ind_cond["all_customer_id"]:
			customer_id_array = ind_cond["all_customer_id"].split(",")
			if user_id:
				if ind_cond["condition"] == "==":
					if user_id in customer_id_array:
						flag = "true"
					else:
						flag = "false"
				else:
					if user_id in customer_id_array:
						flag = "false"
					else:
						flag = "true"
			else:
				flag = "false"

		if i!=0:
			if previos_condition=="AND":
				if flag=="true" and previos_flag=="true":
					previos_flag="true"
				else:
					previos_flag="false"

			if previos_condition=="OR":
				if flag=="false" and previos_flag=="false":
					previos_flag="false"
				else:
					previos_flag="true"
		else:
			previos_flag = flag

		previos_condition=ind_cond["condition_type"]
		i=i+1

	if previos_flag == "true":
		if discount_array["disc_type"]==1:
			discount_array["discountPrice"]=float(ind_product["new_default_price_unit"])*float(discount_array["amount"])/float(100)
		else:
			discount_array["discountPrice"]=float(discount_array["amount"])

		if ind_product["new_default_price_unit"]:
			if float(ind_product["new_default_price_unit"])<=float(0):
				if float(ind_product["new_default_price_unit"])>=float(discount_array["discountPrice"]):
					default_price=float(ind_product["new_default_price_unit"])-float(discount_array["discountPrice"])
					discount_price=float(ind_product["discount_price_unit"])+float(discount_array["discountPrice"])
				else:
					default_price=float(ind_product["new_default_price_unit"])
					discount_price=float(ind_product["discount_price_unit"])

				product_array_disc_applied.append(ind_product["id"])
			else:
				if float(ind_product["default_price"])>=float(discount_array["discountPrice"]):
					default_price = float(ind_product["new_default_price_unit"])-float(discount_array["discountPrice"])
					discount_price = float(discount_array["discountPrice"])
				else:
					default_price = float(ind_product["new_default_price_unit"])
					discount_price = float(ind_product["discount_price_unit"])
				product_array_disc_applied.append(ind_product["id"])
		else:
			if float(ind_product["default_price"])>=float(discount_array["discountPrice"]):
				default_price=float(ind_product["default_price"])-float(discount_array["discountPrice"])
				discount_price=float(discount_array["discountPrice"])
				product_array_disc_applied.append(ind_product["id"])
			else:
				default_price  = float(0)
				discount_price = float(0)
	else:
		if ind_product["new_default_price_unit"]:
			default_price = float(ind_product["new_default_price_unit"])
			discount_price = float(ind_product["discount_price_unit"])
		else:
			default_price  = float(0)
			discount_price = float(0)

	return str(default_price)+"^"+str(discount_price)+"^"+str(previos_flag)

def genrate_new_prodcut_with_discount_coupon_order_total(user_id=None,cartdetails=None,discount_array_coupon=None,order_total=None):
	set_of_response=[]
	coupon_details_dict={}
	for discount_array in discount_array_coupon:
		print("discount_array======", json.dumps(discount_array))
		coupon_details={"coupon_discount_amount":float(discount_array["amount"]),"coupon_disc_type":discount_array["disc_type"],"coupon_name":discount_array["name"],"coupon_code":discount_array["coupon_code"]}
		for product in cartdetails:
			return_price = check_in_prod_disc_coupon_order_total(user_id,product,discount_array,order_total)
			print('price_array==========', return_price)
			price_array = return_price
			set_of_response.append(price_array)

	check_string="false"
	if check_string in set_of_response:
		# coupon_details_dict={"coupon_discount_amount":float(0),"coupon_disc_type":coupon_details["coupon_disc_type"],"coupon_name":coupon_details["coupon_name"],"coupon_code":coupon_details["coupon_code"]}
		coupon_details_dict={"coupon_discount_amount":float(discount_array["amount"]),"coupon_disc_type":coupon_details["coupon_disc_type"],"coupon_name":coupon_details["coupon_name"],"coupon_code":coupon_details["coupon_code"]}
		return coupon_details_dict
	else:
		return coupon_details

def check_in_prod_disc_coupon_order_total(user_id=None,ind_product=None,discount_array=None,cart_subtotal=None):
	discount_array_condition = discount_array["DiscountMasterCondition"]
	product_array_disc_applied = []
	i=0
	flag = "false"
	for ind_cond in discount_array_condition:
		if ind_cond["fields"]==-1:
			if cart_subtotal:
				if ind_cond["condition"] == "==":
					flag = "true" if float(cart_subtotal) == float(ind_cond["value"]) else "false"
				elif ind_cond["condition"] == ">=":
					flag = "true" if float(cart_subtotal) >= float(ind_cond["value"]) else "false"
				else:
					flag = "false" if float(cart_subtotal) >= float(ind_cond["value"]) else "true"
			else:
				flag = "false"
		elif ind_cond["all_category_id"]:
			category_id_array = ind_cond["all_category_id"].split(",")
			find_category = EngageboostProductCategories.objects.filter(product_id=ind_product["id"]).all()
			
			sub_category_id_array = []
			
			if find_category:
				ptcArr = ProductCategoriesSerializer(find_category,many=True)
				for pro in ptcArr.data:
					sub_category_id_array.append(pro["category"]["id"])

			if sub_category_id_array:
				for index in range(len(sub_category_id_array)):
					if ind_cond["condition"] == "==":
						if sub_category_id_array[index] in category_id_array:
							flag = "true"
							break
						else:
							flag = "false"
					else:
						if sub_category_id_array[index] in category_id_array:
							flag = "false"
							break
						else:
							flag = "true"
			else:
				if ind_cond["condition"] == "==": 
					if ind_product["category_id"] in category_id_array:
						flag = "true"
					else:
						flag = "false"
				else:
					if ind_product["category_id"] in category_id_array:
						flag = "false"
					else:
						flag = "true"
		elif ind_cond["all_product_id"]:
			product_id_array = ind_cond["all_product_id"].split(",")
			if ind_cond["condition"] == "==":
				if str(ind_product["id"]) in product_id_array:
					flag = "true"
				else:
					flag = "false"
			else:
				if ind_product["id"] in product_id_array:
					flag = "false"
				else:
					flag = "true"
		elif ind_cond["all_customer_id"]:
			customer_id_array = ind_cond["all_customer_id"].split(",")
			if user_id:
				if ind_cond["condition"] == "==":
					if user_id in customer_id_array:
						flag = "true"
					else:
						flag = "false"
				else:
					if user_id in customer_id_array:
						flag = "false"
					else:
						flag = "true"
			else:
				flag = "false"

		if i!=0:
			if previos_condition=="AND":
				if flag=="true" and previos_flag=="true":
					previos_flag="true"
				else:
					previos_flag="false"

			if previos_condition=="OR":
				if flag=="false" and previos_flag=="false":
					previos_flag="false"
				else:
					previos_flag="true"
		else:
			previos_flag = flag

		previos_condition=ind_cond["condition_type"]
		i=i+1

	return str(previos_flag)

class SaveOrder(generics.ListAPIView):
	def post(self, request, format=None):
		company_db  = loginview.db_active_connection(request)
		now_utc     = datetime.datetime.now(datetime.timezone.utc).astimezone()
		shipping_label_content = ""
		#  *************  Get Base currency
		base_currency = common.getBaseCurrency()
		
		try:
			postdata        = request.data["data"]
			order_serializer_arr    = {}
			website_id = request.data['data']['website_id']
			customerdetails = postdata["customerdetails"]
			payment_type_id = 0
			# warehouse_id = request.data['data']['warehouse_id']
			warehouse_id = 37
			#********FETCH PAYMENT TYPE********#
			payment_method_details = EngageboostPaymentgatewayMethods.objects.using(company_db).filter(id=postdata["payment_method_id"]).first()
			if payment_method_details:
				payment_type_id = payment_method_details.paymentgateway_type_id

			if postdata["applied_coupon"] and postdata["applied_coupon"][0]["name"]!="invalid":
				applied_coupon = postdata["applied_coupon"][0]["coupon_code"]
			else:
				applied_coupon = ""

			#******** SAVE CUSTOMER INFORMATION ********#
			customer_email = customerdetails["billing_email_address"]
			hash_password = make_password("123456", None, 'md5')
			address_book_id = ""
			try:
				has_customer = EngageboostCustomers.objects.using(company_db).filter(email=customer_email,isblocked='n',isdeleted='n').first()
				if has_customer:
					customer_id = has_customer.id
				else:
					user_name = generateNewUserName(customer_email)
					user_arr = {
						"first_name":customerdetails["billing_name"],
						"last_name":"",
						"email":customer_email,
						"country_id":1,
						"role_id":1,
						"username":user_name,
						"created_date":now_utc,
						"modified_date":now_utc
					}
					is_user =  EngageboostUsers.objects.using(company_db).filter(email=customer_email,isblocked='n',isdeleted='n').first()
					if is_user:
						auth_user_id = is_user.id
					else:
						insert_id = EngageboostUsers.objects.using(company_db).create(**user_arr)
						auth_user_id = insert_id.id

					customer_arr={"auth_user_id":auth_user_id, "is_guest_user":0,"website_id":website_id,"first_name":customerdetails["billing_name"],"email":customerdetails["billing_email_address"],"street":customerdetails["billing_street_address"],"city":customerdetails["billing_city"],"state":customerdetails["billing_state"],"country_id":customerdetails["billing_country"],"post_code":customerdetails["billing_postcode"],"phone":customerdetails["billing_phone"],"password":hash_password,"created":now_utc,"modified":now_utc}
					save_customer = EngageboostCustomers.objects.using(company_db).create(**customer_arr)
					customer_id = save_customer.id

				# geo_location = common.get_geo_location(customerdetails["billing_street_address"],customerdetails["billing_city"],customerdetails["billing_postcode"],customerdetails["billing_state"],customerdetails["billing_country"])
				geo_location = common.get_geo_location(customerdetails["billing_street_address"],customerdetails["billing_state"],customerdetails["billing_country"])   
				customer_address_book = {
					"customers_id":customer_id,
					"billing_name":customerdetails["billing_name"],
					"billing_email_address":customerdetails["billing_email_address"],
					"billing_street_address":customerdetails["billing_street_address"],
					"billing_street_address1":customerdetails["billing_street_address1"],
					"billing_city":customerdetails["billing_city"],
					"billing_postcode":customerdetails["billing_postcode"],
					"billing_state":customerdetails["billing_state"],
					"billing_country":customerdetails["billing_country"],
					"billing_phone":customerdetails["billing_phone"],
					"delivery_name":customerdetails["billing_name"],
					"delivery_email_address":customerdetails["billing_email_address"],
					"delivery_street_address":customerdetails["delivery_street_address"],
					"delivery_street_address1":customerdetails["delivery_street_address1"],
					"delivery_city":customerdetails["delivery_city"],
					"delivery_postcode":customerdetails["delivery_postcode"],
					"delivery_state":customerdetails["delivery_state"],
					"delivery_country":customerdetails["delivery_country"],
					"delivery_phone":customerdetails["billing_phone"],
					"lat_val":geo_location["lat"],
					"long_val":geo_location["lng"]
				}
				try:
					if customerdetails["area_id"]!="" and customerdetails["area_id"]!=None:
						customer_address_book.update({"area_id":customerdetails["area_id"]})
					else:
						pass
				except:
					pass
				try:
					if customerdetails["address_book_id"]!="" and customerdetails["address_book_id"]!=None:
						add_id = customerdetails["address_book_id"]
						customerdetails.pop("address_book_id")
						save_customer_addressbook = EngageboostCustomersAddressBook.objects.using(company_db).filter(id=add_id).update(**customer_address_book)
						address_book_id = add_id
					else:
						save_customer_addressbook = EngageboostCustomersAddressBook.objects.using(company_db).create(**customer_address_book)
						address_book_id = save_customer_addressbook.id
				except Exception as error:
					save_customer_addressbook = EngageboostCustomersAddressBook.objects.using(company_db).create(**customer_address_book)
					address_book_id = save_customer_addressbook.id 
			except Exception as error:
				trace_back = sys.exc_info()[2]
				line = trace_back.tb_lineno
				data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in saving customer information"}
				# print("2========",data)
				return Response(data)
			#******** SAVE CUSTOMER INFORMATION (END)********#

			#******** SAVE IN ORDER TABLE ********#
			try:
				if customerdetails["billing_state"]:
					get_billing_state = common.getStateDetails(company_db,customerdetails["billing_state"])
					billing_state_name = get_billing_state["State"].state_name

				if customerdetails["delivery_state"]:
					get_delivery_state = common.getStateDetails(company_db,customerdetails["delivery_state"])
					delivery_state_name = get_delivery_state["State"].state_name

				if customerdetails["billing_country"]:
					get_billing_country = common.getCountryDetails(company_db,customerdetails["billing_country"])
					billing_country_name = get_billing_country["Country"]["country_name"]

				if customerdetails["delivery_country"]:
					get_delivery_country = common.getCountryDetails(company_db,customerdetails["delivery_country"])
					delivery_country_name = get_delivery_country["Country"]["country_name"]

				if postdata["payment_method_id"]:
					payment_method_details = EngageboostPaymentgatewayMethods.objects.using(company_db).filter(id=postdata["payment_method_id"]).first()
					payment_method_name = payment_method_details.name

				rs_wh_manager = EngageboostWarehouseManager.objects.filter(warehouse_id=warehouse_id, isdeleted='n', isblocked = 'n' ).first()
				if rs_wh_manager:
					wh_manager = rs_wh_manager.manager_id

				order_info = {
					"website_id":postdata["website_id"],
					"company_id":postdata["company_id"],
					"webshop_id":postdata["webshop_id"],
					"payment_method_id":postdata["payment_method_id"],
					"payment_type_id":payment_type_id,
					"payment_method_name":payment_method_name,
					"gross_amount":postdata["sub_total"],
					"net_amount":postdata["net_total"],
					"shipping_cost":postdata["shipping_charge"],
					"paid_amount":postdata["paid_amount"],
					"gross_discount_amount":postdata["gross_discount"],
					"tax_amount":postdata["tax_amount"],
					"order_status":0,
					"buy_status":1,
					"created":now_utc,
					"modified":now_utc,
					"cart_discount":postdata["cart_discount"],
					"cod_charge":postdata["cod_charge"],
					"applied_coupon":applied_coupon,
					"custom_msg":postdata["custom_msg"],
					"custom_order_id":postdata["custom_order_id"],
					"pay_txntranid":postdata["pay_txntranid"],
					"customer_id":customer_id,
					"pay_txndate":postdata['pay_txndate'],
					"assign_wh":warehouse_id,						
					"assign_to":wh_manager,
				}
				if 'gross_total' in postdata:
					order_info.update({ "order_amount":postdata["gross_total"]})
				if 'zone_id' in postdata:
					order_info.update({"zone_id":postdata["zone_id"]})
				if 'area_id' in postdata:
					order_info.update({"area_id":postdata["area_id"]})
				if 'time_slot_date' in postdata:
					order_info.update({"time_slot_date":postdata["time_slot_date"]})
				if 'time_slot_id' in postdata:
					order_info.update({"time_slot_id":postdata["time_slot_id"]})
				if 'slot_start_time' in postdata:
					order_info.update({"slot_start_time":postdata["slot_start_time"]})
				if 'slot_end_time' in postdata:
					order_info.update({"slot_end_time":postdata["slot_end_time"]})
				if 'currency_id' in postdata:
					currency = common.get_currency_details(postdata["currency_id"])
					order_info.update({"currency_code":currency["currency"]})
				else:
					order_info.update({"currency_code":base_currency["currency_code"]})

				if address_book_id!="" and address_book_id!=None:
					order_info.update({"address_book_id":address_book_id})    

				order_serializer_arr = dict(order_serializer_arr,**order_info)
				customer_info={"billing_name":customerdetails["billing_name"],"billing_email_address":customerdetails["billing_email_address"],"billing_street_address":customerdetails["billing_street_address"],"billing_street_address1":customerdetails["billing_street_address1"],"billing_city":customerdetails["billing_city"],"billing_postcode":customerdetails["billing_postcode"],"billing_state":customerdetails["billing_state"],"billing_state_name":billing_state_name,"billing_country":customerdetails["billing_country"],"billing_country_name":billing_country_name,"billing_phone":customerdetails["billing_phone"],"delivery_name":customerdetails["billing_name"],"delivery_email_address":customerdetails["billing_email_address"],"delivery_street_address":customerdetails["delivery_street_address"],"delivery_street_address1":customerdetails["delivery_street_address1"],"delivery_city":customerdetails["delivery_city"],"delivery_postcode":customerdetails["delivery_postcode"],"delivery_state":customerdetails["delivery_state"],"delivery_state_name":delivery_state_name,"delivery_country":customerdetails["delivery_country"],"delivery_country_name":delivery_country_name,"delivery_phone":customerdetails["billing_phone"]}
				order_serializer_arr=dict(order_serializer_arr,**customer_info)
				hasOrder = EngageboostOrdermaster.objects.using(company_db).filter(custom_order_id=postdata["custom_order_id"]).first()
				if hasOrder:
					# order_id = 0
					imageresizeon = EngageboostGlobalSettings.objects.using(company_db).get(website_id=1)
					orders = EngageboostOrdermaster.objects.using(company_db).last()
					Order1 =int(orders.id)+int(1)
					cust_order_id = str(imageresizeon.orderid_format)+str(Order1)
					order_serializer_arr['custom_order_id']=cust_order_id

					save_order_master = EngageboostOrdermaster.objects.using(company_db).create(**order_serializer_arr)
					order_id = save_order_master.id if save_order_master else 0

				else:
					save_order_master = EngageboostOrdermaster.objects.using(company_db).create(**order_serializer_arr)
					order_id = save_order_master.id if save_order_master else 0
			except Exception as error:
				trace_back = sys.exc_info()[2]
				line = trace_back.tb_lineno
				data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in order creation"}
				return Response(data)
			#******** SAVE IN ORDER TABLE (END)********#

			#******** SAVE IN ORDER PRODUCT TABLE ********#
			try:
				if postdata["cartdetails"]:
					for cartdetails in postdata["cartdetails"]:
						if cartdetails["is_igst"]=="no":
							cgst=sgst=float(cartdetails["tax_price_unit"])/float(2)
							igst=float(0)
						else:
							cgst=sgst=float(0)
							igst=cartdetails["tax_price_unit"]
						order_product_arr={
							"order_id":order_id,
							"product_id":cartdetails["id"],
							"quantity":cartdetails["qty"],
							"deleted_quantity":0,
							"product_price":cartdetails["new_default_price_unit"],
							"product_discount_price":cartdetails["discount_price_unit"],
							"product_tax_price":cartdetails["tax_price_unit"],
							"tax_percentage":cartdetails["tax_percentage"],
							"product_price_base":cartdetails["new_default_price_unit"],
							"product_discount_price_base":cartdetails["discount_price_unit"],
							"hsn_id":cartdetails["hsn_id"],
							"hsn_id":cartdetails["hsn_id"],
							"sgst":sgst,
							"cgst":cgst,
							"igst":igst,
							"cess":cartdetails["cess"],
							"created":now_utc
						}

						price_obj = EngageboostProductPriceTypeMaster.objects.using(company_db).filter(isblocked='n',isdeleted='n',product_id=cartdetails["id"], price_type_id=1)
						
						if price_obj.count()>0:
							priceData = price_obj.first()
							obj = EngageboostChannelCurrencyProductPrice.objects.using(company_db).filter(product_price_type_id=priceData.id,warehouse_id=1,product_id=cartdetails["id"])
							if obj.count()>0:
								channelData = obj.first()
								order_product_arr["mrp"] = channelData.mrp
								order_product_arr["cost_price"] = channelData.cost


						save_order_product = EngageboostOrderProducts.objects.using(company_db).create(**order_product_arr)

						activityType=3
						common.save_item_activity(company_db,order_id,now_utc,0,1,'',activityType,cartdetails["id"],cartdetails["qty"],postdata["custom_order_id"])
						
						common.update_stock_all(cartdetails["id"],1,cartdetails["qty"],"Decrease","virtual",order_id,website_id)

			except Exception as error:
				trace_back = sys.exc_info()[2]
				line = trace_back.tb_lineno
				data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in saving order product information"}
				return Response(data)
			#******** SAVE IN ORDER PRODUCT TABLE (END)********#

			#******** SAVE ORDER ACTIVITY ********#
			activityType = 1
			activity_details = common.save_order_activity(company_db,order_id,now_utc,0,"Order has been placed",'',activityType)
			#******** SAVE ORDER ACTIVITY (END)********#

			#******** GENERATE AUTO RESPONDER ********#
			buffer_data = common.getAutoResponder(company_db,"","","","","",3)
			# print(json.dumps(buffer_data))
			if buffer_data and buffer_data["content"]:
				autoResponderData  = buffer_data["content"]
				if autoResponderData["email_type"] == 'T':
					emailContent = autoResponderData["email_content_text"]
				else:
					emailContent = autoResponderData["email_content"]
				emailContent = str(emailContent)
				try:
					emailContent = emailContent.replace('{@first_name}',customerdetails["billing_name"])
				except:
					pass
				try:
					emailContent = emailContent.replace('{@custom_order_id}',postdata["custom_order_id"])
				except:
					pass
				try:
					emailContent = emailContent.replace('{@delivery_name}',customerdetails["billing_name"])
				except:
					pass
				try:
					emailContent = emailContent.replace('{@delivery_street_address}',customerdetails["delivery_street_address"])
				except:
					pass
				try:
					emailContent = emailContent.replace('{@delivery_city}',customerdetails["delivery_city"])
				except:
					pass
				try:
					emailContent = emailContent.replace('{@delivery_postcode}',customerdetails["delivery_postcode"])
				except:
					pass
				try:
					emailContent = emailContent.replace('{@delivery_state}',billing_state_name)
				except:
					pass
				try:
					emailContent = emailContent.replace('{@delivery_country}',billing_country_name)
				except:
					pass
				try:
					emailContent = emailContent.replace('{@delivery_phone}',customerdetails["billing_phone"])
				except:
					pass
				try:
					emailContent = emailContent.replace('{@payment_method_name}',payment_method_name)
				except:
					pass
				try:
					emailContent = emailContent.replace('{@gross_amount}',str(postdata["sub_total"]))
				except:
					pass
				try:
					emailContent = emailContent.replace('{@shipping_cost}',str(postdata["shipping_charge"]))
				except:
					pass
				try:
					emailContent = emailContent.replace('{@tax_amount}',str(postdata["tax_amount"]))
				except:
					pass
				try:
					emailContent = emailContent.replace('{@discount_amount}',str(postdata["gross_discount"]))
				except:
					pass
				try:
					emailContent = emailContent.replace('{@net_amount}',str(postdata["net_total"]))
				except:
					pass
				
				#******** GENERATE AUTO RESPONDER (END)********#
			# emailcomponent.sendOrderMail(company_db,customerdetails["billing_email_address"],autoResponderData["email_from"],autoResponderData["subject"],emailContent)
			elastic = common.save_data_to_elastic(order_id,'EngageboostOrdermaster')
			
			data={"status":1,"api_status":"Order created successfully","message":"Order created successfully"}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Something went wrong"}
		return Response(data)

class test(generics.ListAPIView):
	def post(self, request, format=None):
		# from num2words import num2words
		# p = num2words(1589625.256)
		# p = p.replace('-','').replace(',','')
		# data={"Word":p}
		# return Response(data)
		company_db = loginview.db_active_connection(request)
		# details = EngageboostShipmentOrders.objects.filter(shipment_id=94).all()
		# details_list = ShipmentsOrdersSerializer(details,many=True)
		# country = common.getAllCountries(company_db)
		import smtplib

		from email.mime.multipart import MIMEMultipart
		from email.mime.text import MIMEText

		# me == my email address
		# you == recipient's email address
		me = "subhasis.debnath@navsoft.in"
		you = "subhasis.debnath@navsoft.in"

		# Create message container - the correct MIME type is multipart/alternative.
		msg = MIMEMultipart('alternative')
		msg['Subject'] = "Test Email In Python"
		msg['From'] = me
		msg['To'] = you

		# Create the body of the message (a plain-text and an HTML version).
		# text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
		template = """\
		<html>
		  <head></head>
		  <body>
			<p>Hi!<br>
			   How are you?<br>
			   Name-{@name}, Phone Number-{@phone}.
			</p>
		  </body>
		</html>
		"""
		template = template.replace("{@name}","Subhasis Debnath")
		template = template.replace("{@phone}","9046793412")

		# Record the MIME types of both parts - text/plain and text/html.
		# part1 = MIMEText(text, 'plain')
		part2 = MIMEText(template, 'html')

		# Attach parts into message container.
		# According to RFC 2046, the last part of a multipart message, in this case
		# the HTML message, is best and preferred.
		# msg.attach(part1)
		msg.attach(part2)
		# Send the message via local SMTP server.
		mail = smtplib.SMTP('smtp.gmail.com', 587)

		mail.ehlo()

		mail.starttls()

		mail.login('subhasis.debnath@navsoft.in', 'sdchelsea')
		mail.sendmail(me, you, msg.as_string())
		mail.quit()
		data={"status":1}
		return Response(data)

class get_delivery_slot(generics.ListAPIView):
	
	def get(self, request,format=None):
		zone_id = self.request.GET.get("zone_id")

		# returndata = GetDeliverySlot(zone_id)
		returndata = GetDeliverySlotByWarehouse(zone_id)
		return Response(returndata)          

def GetDeliverySlot(zone_id):
	now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
	data            = []
	DeliverySlot    = []
	dataTimeslot    = []
	newTimeSlot     = []
	
	if zone_id and int(zone_id)<=0:
		returndata = {
			"status":0,
			"ack":"fail",
			"msg":"Zone not available"
		}
	else:
		next_day_arr = []
		for x in range(7):
			now 	= datetime.datetime.now()
			today 	= now.date()                
			new_date = ''  
			new_date = now_utc + timedelta(days=x)
			next_day_arr.append(new_date)

		rs_data = EngageboostDeliverySlot.objects.filter(isdeleted='n', isblocked='n', zone_id=zone_id).order_by('day_id','start_time').all()
		slot_data 	= DeliverySlotSerializer(rs_data, many=True)
		DeliverySlot = []
		current_time = datetime.datetime.now().strftime('%H:%M:%S')
		to_day = datetime.datetime.now().strftime('%Y-%m-%d')            
		order_data = EngageboostOrdermaster.objects.filter(time_slot_date__gte=to_day,buy_status = 1, zone_id=zone_id).exclude(order_status=2).all().order_by('time_slot_date','slot_start_time').annotate(total=Count('slot_start_time')).values('time_slot_date','slot_start_time')
		for dayarr in next_day_arr:
			dtarr = dayarr.strftime('%Y-%m-%d')
			year, month, day = (int(x) for x in dtarr.split('-'))    
			dt = datetime.date(year, month, day)
			day_id = dt.weekday()
			temp_arr = {}
			templist = []
			temp_list2 = {}
			for slotdata in slot_data.data:
				if slotdata['day_id'] == day_id:
					templist.append(slotdata)            
			temp_list2.update({"delivery_date":dtarr})
			temp_arr.update({"delivery_date":dtarr, "available_slot":templist})
			DeliverySlot.append(temp_arr)
		returndata = {
			"status":1,
			# "date_data":next_day_arr,
			# "delivery_slot_data":slot_data.data,
			"delivery_slot":DeliverySlot
		}
	return returndata

def GetDeliverySlotByWarehouse(zone_id):
	from pytz import timezone
	# now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
	now_utc = datetime.datetime.now(timezone('UTC')).astimezone(timezone('Asia/Dubai'))
	# now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
	days_arr = ['NA','sun','mon', 'tue', 'wed', 'thu', 'fri','sat']
	# now_utc = now_utc+ timedelta(hours=4)
	data            = []
	DeliverySlot    = []
	dataTimeslot    = []
	newTimeSlot     = []
	warehouse_id    = zone_id
	if warehouse_id and int(warehouse_id)<=0:
		returndata = {
			"status":0,
			"ack":"fail",
			"msg":"Warehouse not available"
		}
	else:
		next_day_arr = []
		for x in range(1):
			# now 	= datetime.now()
			# now = now + timedelta(hours=4)
			today 	= now_utc.date()
			new_date = ''  
			new_date = now_utc + timedelta(days=x)
			next_day_arr.append(new_date)

		# today_id = today.weekday()
		today_name = today.strftime("%a")
		today_name = today_name.lower()
		today_id = days_arr.index(today_name)
		nextday_id = today_id+1
		if today_id>=7:
			nextday_id = 1

		rs_data     = EngageboostDeliverySlot.objects.filter(isdeleted='n', isblocked='n', warehouse_id=warehouse_id, day_id__in=[today_id, nextday_id]).order_by('day_id','start_time').all().order_by('day_id')
		slot_data 	= DeliverySlotSerializer(rs_data, many=True)
		DeliverySlot = []
		current_time = datetime.datetime.now().strftime('%H:%M:%S')
		to_day      = datetime.datetime.now().strftime('%Y-%m-%d')
		order_data  = EngageboostOrdermaster.objects.filter(time_slot_date__gte=to_day,buy_status = 1).exclude(order_status=2).all().values('time_slot_date','slot_start_time').order_by('time_slot_date','slot_start_time').annotate(total=Count('time_slot_date'))

		flag = 0
		for dayarr in next_day_arr:
			dtarr   = dayarr.strftime('%Y-%m-%d')
			dt      = dayarr
			# day_id  = dt.weekday()
			day_name = dayarr.strftime("%a")
			day_name = day_name.lower()
			day_id = days_arr.index(day_name)
			temp_arr = {}
			next_arr = {}
			next_list = []
			# templist = []
			temp_list2 = {}
			# day_id = day_id+2
			# print("day_id",day_id)
			for slotdata in slot_data.data:
				templist = []
				if slotdata['day_id'] == day_id:
					# +++++++++++++++++++++
					date_format = "%Y-%m-%d"
					current_time = now_utc.strftime('%H:%M')
					str_current_time_arr = str(current_time).split(":")
					str_current_time = str_current_time_arr[0]
					time_format = "%H:%M"
					# cutoff_time = time.strptime(str(slotdata['cutoff_time']), time_format)                 

					str_cutoff_time_arr = str(slotdata['cutoff_time']).split(":")
					str_cutoff_time = str_cutoff_time_arr[0]
					# print("str_cutoff_time", str_cutoff_time)
					# print("str_current_time", str_current_time)
					# print("day_id", day_id)

					if int(str_cutoff_time) > int(str_current_time):
						slotdata.update({"is_active":"Yes"})
						slotdata["based_on"]="SameDay"
						templist.append(slotdata)
						temp_list2.update({"delivery_date":dtarr})
						temp_arr.update({"delivery_date":dtarr, "available_slot":templist})
						DeliverySlot.append(temp_arr)
					else:
						if flag>0:
							pass
						else:
							flag = 1
							slotdata.update({"is_active":"Yes"})
							slotdata["based_on"]="Nextday"
							dt_arr = new_date = now_utc + timedelta(days=1)
							dt_arr = dt_arr.strftime('%Y-%m-%d')
							templist.append(slotdata)
							next_arr.update({"delivery_date":dt_arr, "available_slot":templist})
							DeliverySlot.append(next_arr)
					# +++++++++++++++++++++
				else:
					if flag > 0:
						pass
					else:
						flag = 1
						dt_arr = new_date = now_utc + timedelta(days=1)
						dt_arr = dt_arr.strftime('%Y-%m-%d')
						slotdata.update({"is_active":"Yes"})
						slotdata["based_on"]="Nextday"
						templist.append(slotdata)
						next_arr.update({"delivery_date":dt_arr, "available_slot":templist})
						DeliverySlot.append(next_arr)    
		DeliverySlot.sort(key=lambda x: x['delivery_date'].lower())
		returndata = {
			"status":1,
			"delivery_slot":DeliverySlot
		}
	return returndata

class GetAvailablePromo(generics.ListAPIView):
	def get(self, request,format=None):
		user_id = self.request.GET.get("user_id")
		listing 			= []
		discountdata 	    = {}
		
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		website_id = 1
		# now 	= datetime.datetime.now()
		# today 	= now.date()
		# if user_id:
		rs_discount = EngageboostDiscountMasters.objects.filter(website_id=website_id, disc_start_date__lte = now_utc, disc_end_date__gte =now_utc, isdeleted='n', discount_master_type=1).exclude(coupon_code='').all()
		if rs_discount:
			discount_data = DiscountMasterSerializer(rs_discount,many=True)
			for discount in discount_data.data:
				discountdata = {"name":discount['name'], "description":discount['description'], "coupon_code":discount['coupon_code']}
				listing.append(discountdata)
				data = {
					"status":1,
					"data":listing
				}
		else:
			data = {
				"status":0,
				"Message":"No promotion found."
			}
		
		return Response(data)

class ViewOrder(generics.ListAPIView):
	def get(self, request, pk, format=None):
		rs_order = EngageboostOrdermaster.objects.filter(id=pk).first()
		order_data = ViewOrderSerializer(rs_order)
		order_data = order_data.data
		date=EngageboostGlobalSettings.objects.get(website_id=1)
		zone=EngageboostTimezones.objects.get(id=date.timezone_id)
		order_data['created']=common.get_time(order_data['created'],zone,date)
		order_data['modified']=common.get_time(order_data['modified'],zone,date)
		if(order_data['pay_txndate']):
			order_data['pay_txndate']=common.get_time(order_data['pay_txndate'],zone,date)
		order_data['time_slot_date']=common.get_date_from_datetime(order_data['time_slot_date'],zone,date,"%Y-%m-%d")
		status_message = ""
		rs_transaction = EngageboostMastercardPgReturnDetails.objects.filter(order_id = pk).last()
		if rs_transaction:
			transaction_data = EngageboostMastercardPgReturnDetailsSerializer(rs_transaction)
			transaction_data = transaction_data.data
			status_message = transaction_data['status_message']
		order_data['status_message'] = status_message
		try:
			data = {
				"status":1,
				"api_status": 1,
				"data":order_data
			}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in order update."}
		return Response(data)

class EditOrder(generics.ListAPIView):
	def put(self, request):
		company_db = loginview.db_active_connection(request)
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		shipping_label_content = ""
		try:
			postdata  = request.data["data"]
			order_serializer_arr    = {}
			website_id = request.data['data']['website_id']
			ip_address = request.data['data']['ip_address']
			customerdetails = postdata["customerdetails"]
			warehouse_id = request.data['data']['warehouse_id']

			payment_type_id = 0
			#********FETCH PAYMENT TYPE********#
			payment_method_details = EngageboostPaymentgatewayMethods.objects.using(company_db).filter(id=postdata["payment_method_id"]).first()
			if payment_method_details:
				payment_type_id = payment_method_details.paymentgateway_type_id
			if postdata["applied_coupon"] and postdata["applied_coupon"][0]["name"]!="invalid":
				applied_coupon = postdata["applied_coupon"][0]["coupon_code"]
			else:
				applied_coupon = ""
			#******** SAVE CUSTOMER INFORMATION ********#
			customer_email = customerdetails["billing_email_address"]
			hash_password = make_password("123456", None, 'md5')
			address_book_id = ""
			try:
				has_customer = EngageboostCustomers.objects.using(company_db).filter(email=customer_email,isblocked='n',isdeleted='n').first()
				if has_customer:
					customer_id = has_customer.id
				else:
					user_name = generateNewUserName(customer_email)
					user_arr = {
						"first_name":customerdetails["billing_name"],
						"last_name":"",
						"email":customer_email,
						"username":user_name,
						"country_id":1,
						"role_id":1,
						"created_date":now_utc,
						"modified_date":now_utc
					}
					is_user =  EngageboostUsers.objects.using(company_db).filter(email=customer_email,isblocked='n',isdeleted='n').first()
					if is_user:
						auth_user_id = is_user.id
					else:
						insert_id = EngageboostUsers.objects.using(company_db).create(**user_arr)
						auth_user_id = insert_id.id  
						
					customer_arr = {
						"auth_user_id":auth_user_id,
						"is_guest_user":0,
						"website_id":website_id,
						"first_name":customerdetails["billing_name"],
						"email":customerdetails["billing_email_address"],
						"street":customerdetails["billing_street_address"],
						"city":customerdetails["billing_city"],
						"state":customerdetails["billing_state"],
						"country_id":customerdetails["billing_country"],
						"post_code":customerdetails["billing_postcode"],
						"phone":customerdetails["billing_phone"],
						"password":hash_password,
						"created":now_utc,
						"modified":now_utc
					}
					save_customer = EngageboostCustomers.objects.using(company_db).create(**customer_arr)
					customer_id = save_customer.id
					
				# geo_location = common.get_geo_location(customerdetails["billing_street_address"],customerdetails["billing_city"],customerdetails["billing_postcode"],customerdetails["billing_state"],customerdetails["billing_country"])
				geo_location = common.get_geo_location(customerdetails["billing_street_address"],customerdetails["billing_state"],customerdetails["billing_country"])
				customer_address_book = {
					"customers_id":customer_id,
					"billing_name":customerdetails["billing_name"],
					"billing_email_address":customerdetails["billing_email_address"],
					"billing_street_address":customerdetails["billing_street_address"],
					"billing_street_address1":customerdetails["billing_street_address1"],
					"billing_city":customerdetails["billing_city"],
					"billing_postcode":customerdetails["billing_postcode"],
					"billing_state":customerdetails["billing_state"],
					"billing_country":customerdetails["billing_country"],
					"billing_phone":customerdetails["billing_phone"],
					"delivery_name":customerdetails["billing_name"],
					"delivery_email_address":customerdetails["billing_email_address"],
					"delivery_street_address":customerdetails["delivery_street_address"],
					"delivery_street_address1":customerdetails["delivery_street_address1"],
					"delivery_city":customerdetails["delivery_city"],
					"delivery_postcode":customerdetails["delivery_postcode"],
					"delivery_state":customerdetails["delivery_state"],
					"delivery_country":customerdetails["delivery_country"],
					"delivery_phone":customerdetails["billing_phone"],
					"lat_val":geo_location["lat"],
					"long_val":geo_location["lng"]
				}
				try:
					if customerdetails["area_id"]!="" and customerdetails["area_id"]!=None:
						customer_address_book.update({"area_id":customerdetails["area_id"]})
					else:
						pass
				except:
					pass
				try:
					if customerdetails["address_book_id"]!="" and customerdetails["address_book_id"]!=None:
						add_id = customerdetails["address_book_id"]
						customerdetails.pop("address_book_id")
						save_customer_addressbook = EngageboostCustomersAddressBook.objects.using(company_db).filter(id=add_id).update(**customer_address_book)
						address_book_id = add_id
					else:
						save_customer_addressbook = EngageboostCustomersAddressBook.objects.using(company_db).create(**customer_address_book)
						address_book_id = save_customer_addressbook.id
				except Exception as error:
					save_customer_addressbook = EngageboostCustomersAddressBook.objects.using(company_db).create(**customer_address_book)
					address_book_id = save_customer_addressbook.id
			except Exception as error:
				trace_back = sys.exc_info()[2]
				line = trace_back.tb_lineno
				data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in saving customer information"}
				return Response(data)
			#******** SAVE CUSTOMER INFORMATION (END)********#
			#******** SAVE IN ORDER TABLE ********#
			try:
				if customerdetails["billing_state"]:
					get_billing_state = common.getStateDetails(company_db,customerdetails["billing_state"])
					billing_state_name = get_billing_state["State"].state_name

				if customerdetails["delivery_state"]:
					get_delivery_state = common.getStateDetails(company_db,customerdetails["delivery_state"])
					delivery_state_name = get_delivery_state["State"].state_name

				if customerdetails["billing_country"]:
					get_billing_country = common.getCountryDetails(company_db,customerdetails["billing_country"])
					billing_country_name = get_billing_country["Country"]["country_name"]

				if customerdetails["delivery_country"]:
					get_delivery_country = common.getCountryDetails(company_db,customerdetails["delivery_country"])
					delivery_country_name = get_delivery_country["Country"]["country_name"]
				payment_method_name = ""
				if postdata["payment_method_id"]:
					payment_method_details = EngageboostPaymentgatewayMethods.objects.using(company_db).filter(id=postdata["payment_method_id"]).first()
					payment_method_name = payment_method_details.name

				rs_wh_manager = EngageboostWarehouseManager.objects.filter(warehouse_id=warehouse_id, isdeleted='n', isblocked = 'n' ).first()
				if rs_wh_manager:
					wh_manager = rs_wh_manager.manager_id

				order_info = {
					"website_id":postdata["website_id"],
					"company_id":postdata["company_id"],
					"webshop_id":postdata["webshop_id"],
					"payment_method_id":postdata["payment_method_id"],
					"payment_type_id":payment_type_id,
					"payment_method_name":payment_method_name,
					"gross_amount":postdata["grand_total"],
					"net_amount":postdata["net_total"],
					"shipping_cost":postdata["shipping_charge"],
					"paid_amount":postdata["paid_amount"],
					"gross_discount_amount":postdata["gross_discount_amount"],
					"tax_amount":postdata["tax_amount"],
					# "order_status":0,
					# "buy_status":1,
					"created":now_utc,
					"modified":now_utc,
					"cart_discount":postdata["cart_discount"],
					"cod_charge":postdata["cod_charge"],
					"applied_coupon":applied_coupon,
					"custom_msg":postdata["custom_msg"],
					"custom_order_id":postdata["custom_order_id"],
					"pay_txntranid":postdata["pay_txntranid"],
					"customer_id":customer_id,
					"assign_wh":warehouse_id,						
					"assign_to":wh_manager,
					"zone_id":24,
					'pay_wallet_amount':postdata["pay_wallet_amount"],
				}
				print("order_info+++++++++++", order_info)
				if 'gross_total' in postdata:
					order_info.update({ "order_amount":postdata["gross_total"]})
				if 'zone_id' in postdata:
					order_info.update({"zone_id":postdata["zone_id"]})
				if 'area_id' in postdata:
					order_info.update({"billing_street_address1":postdata["area_id"]})
				if 'time_slot_date' in postdata:
					order_info.update({"time_slot_date":postdata["time_slot_date"]})
				if 'time_slot_id' in postdata:
					order_info.update({"time_slot_id":postdata["time_slot_id"]})
				if 'slot_start_time' in postdata:
					order_info.update({"slot_start_time":postdata["slot_start_time"]})
				if 'slot_end_time' in postdata:
					order_info.update({"slot_end_time":postdata["slot_end_time"]})

				order_info.update({"time_slot_id":"5:00 PM - 07:30 PM"})
				order_info.update({"slot_start_time":"17:00"})
				order_info.update({"slot_end_time":"19:30"})

				if address_book_id!="" and address_book_id!=None:
					order_info.update({"address_book_id":address_book_id})

				order_serializer_arr = dict(order_serializer_arr,**order_info)
				customer_info = {
					"billing_name":customerdetails["billing_name"],
					"billing_email_address":customerdetails["billing_email_address"],
					"billing_street_address":customerdetails["billing_street_address"],
					"billing_street_address1":customerdetails["billing_street_address1"],
					"billing_city":customerdetails["billing_city"],
					"billing_postcode":customerdetails["billing_postcode"],
					"billing_state":customerdetails["billing_state"],
					"billing_state_name":billing_state_name,
					"billing_country":customerdetails["billing_country"],
					"billing_country_name":billing_country_name,
					"billing_phone":customerdetails["billing_phone"],
					"delivery_name":customerdetails["billing_name"],
					"delivery_email_address":customerdetails["billing_email_address"],
					"delivery_street_address":customerdetails["delivery_street_address"],
					"delivery_street_address1":customerdetails["delivery_street_address1"],
					"delivery_city":customerdetails["delivery_city"],
					"delivery_postcode":customerdetails["delivery_postcode"],
					"delivery_state":customerdetails["delivery_state"],
					"delivery_state_name":delivery_state_name,
					"delivery_country":customerdetails["delivery_country"],
					"delivery_country_name":delivery_country_name,
					"delivery_phone":customerdetails["billing_phone"]
				}
				order_serializer_arr=dict(order_serializer_arr,**customer_info)
				# print("order_serializer_arr++++++++++++++", order_serializer_arr)

				hasOrder = EngageboostOrdermaster.objects.using(company_db).filter(custom_order_id=postdata["custom_order_id"]).first()
				if hasOrder:
					order_id = hasOrder.id
					order_status = hasOrder.order_status
					buy_status = hasOrder.buy_status
					try:
						save_order_master = EngageboostOrdermaster.objects.using(company_db).filter(id=order_id).update(**order_serializer_arr)
						custom_order_id = hasOrder.custom_order_id
						# Loyalty Transaction
						loyalty_trans_arr = {
							"website_id": 1,
							"rule_id": 77,
							"customer_id": 22,
							"order_id": order_id,
							"custom_order_id": postdata["custom_order_id"],
							"description": 'This is burn for order no ' + custom_order_id,
							"received_points": 0.00,
							"burnt_points": postdata["pay_wallet_amount"],
							"amount": postdata["pay_wallet_amount"],
							"received_burnt": postdata["pay_wallet_amount"],
							"status": "burn",
							"created": now_utc,
							"valid_form": now_utc
						}
						if order_id >0:
							loyalty.save_burn_points(loyalty_trans_arr)


					except Exception as error:
						trace_back = sys.exc_info()[2]
						line = trace_back.tb_lineno
						data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in order update."}
				else:
					data={"status":0,"api_status":"Error","message":"Order Not Found."}
					return Response(data)
			except Exception as error:
				trace_back = sys.exc_info()[2]
				line = trace_back.tb_lineno
				data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in order update."}
				return Response(data)
			#******** SAVE IN ORDER TABLE (END)********#

			#******** SAVE IN ORDER PRODUCT TABLE ********#
			try:
				if postdata["cartdetails"]:
					delete_order_ids = []
					if int(order_status)==0:
						if buy_status == 1:
							ex_arr = []
							for cartdetails in postdata["cartdetails"]:
								if cartdetails["is_igst"]=="no":
									cgst=sgst=float(cartdetails["tax_price_unit"])/float(2)
									igst=float(0)
								else:
									cgst=sgst=float(0)
									igst=cartdetails["tax_price_unit"]
								
								order_product_arr = {
									"order_id":order_id,
									"product_id":cartdetails["id"],
									"quantity":cartdetails["qty"],
									"deleted_quantity":0,
									"product_price":cartdetails["new_default_price_unit"],
									"product_discount_price":cartdetails["discount_price_unit"],
									"product_tax_price":cartdetails["tax_price_unit"],
									"tax_percentage":cartdetails["tax_percentage"],
									"product_price_base":cartdetails["new_default_price_unit"],
									"product_discount_price_base":cartdetails["discount_price_unit"],
									"hsn_id":cartdetails["hsn_id"],
									"hsn_id":cartdetails["hsn_id"],
									"sgst":sgst,
									"cgst":cgst,
									"igst":igst,
									"cess":cartdetails["cess"],
									"created":now_utc
								}
								try:
									obj_pro = EngageboostOrderProducts.objects.using(company_db).get(order_id=order_id, product_id=cartdetails["id"])
									ex_arr.append(cartdetails["id"])
									previous_quantity = int(obj_pro.quantity)
									previous_price = int(obj_pro.product_price)
									save_order_product = EngageboostOrderProducts.objects.using(company_db).filter(order_id=order_id, product_id=cartdetails["id"]).update(**order_product_arr)
									
									activityType=3
									msg_type = ""
									msg_value= ""
									if previous_quantity < int(cartdetails["qty"]):
										msg_type = 2
										msg_value = int(cartdetails["qty"])
										common.save_item_activity(company_db,order_id,now_utc,0,msg_type,'',activityType,cartdetails["id"],msg_value,postdata["custom_order_id"])
										common.update_stock_all(cartdetails["id"],1,cartdetails["qty"],"Decrease","real",order_id,website_id)
									
									elif previous_quantity > int(cartdetails["qty"]):    
										msg_type = 3
										msg_value = int(cartdetails["qty"])
										common.save_item_activity(company_db,order_id,now_utc,0,msg_type,'',activityType,cartdetails["id"],msg_value,postdata["custom_order_id"])
										common.update_stock_all(cartdetails["id"],1,cartdetails["qty"],"Increase","virtual",order_id,website_id)
									
									if previous_price < float(cartdetails["new_default_price_unit"]):
										msg_type = 4
										msg_value = float(cartdetails["new_default_price_unit"])
										common.save_item_activity(company_db,order_id,now_utc,0,msg_type,'',activityType,cartdetails["id"],msg_value,postdata["custom_order_id"])
									
									elif previous_price > float(cartdetails["new_default_price_unit"]):    
										msg_type = 5
										msg_value = float(cartdetails["new_default_price_unit"])
										common.save_item_activity(company_db,order_id,now_utc,0,msg_type,'',activityType,cartdetails["id"],msg_value,postdata["custom_order_id"])

								except EngageboostOrderProducts.DoesNotExist:
									ex_arr.append(cartdetails["id"])
									save_order_product = EngageboostOrderProducts.objects.using(company_db).create(**order_product_arr)
									
									common.update_stock_all(cartdetails["id"],1,cartdetails["qty"],"Decrease","virtual",order_id,website_id)
							
							EngageboostOrderProducts.objects.using(company_db).filter(order_id=order_id).exclude(product_id__in=ex_arr).delete()
						else:
							pass
			except Exception as error:
				trace_back = sys.exc_info()[2]
				line = trace_back.tb_lineno
				data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in saving order product information"}
				return Response(data)
			#******** SAVE IN ORDER PRODUCT TABLE (END)********#

			#******** SAVE ORDER ACTIVITY ********#
			# activityType = 1
			# activity_details = common.save_order_activity(company_db,order_id,now_utc,0,"Order has been placed",'',activityType)
			#******** SAVE ORDER ACTIVITY (END)********#

			#******** GENERATE AUTO RESPONDER ********#
			buffer_data = common.getAutoResponder(company_db,"","","","","",77)
			if buffer_data["status"]>0:
				autoResponderData  = buffer_data["content"]
				if autoResponderData["email_type"] == 'T':
					emailContent = autoResponderData["email_content_text"]
				else:
					emailContent = autoResponderData["email_content"]
				emailContent = str(emailContent)
				emailContent = emailContent.replace('{@first_name}',customerdetails["billing_name"])
				emailContent = emailContent.replace('{@custom_order_id}',postdata["custom_order_id"])
				emailContent = emailContent.replace('{@delivery_name}',customerdetails["billing_name"])
				emailContent = emailContent.replace('{@delivery_street_address}',customerdetails["delivery_street_address"])
				emailContent = emailContent.replace('{@delivery_city}',customerdetails["delivery_city"])
				emailContent = emailContent.replace('{@delivery_postcode}',customerdetails["delivery_postcode"])
				emailContent = emailContent.replace('{@delivery_state}',billing_state_name)
				emailContent = emailContent.replace('{@delivery_country}',billing_country_name)
				emailContent = emailContent.replace('{@delivery_phone}',customerdetails["billing_phone"])
				emailContent = emailContent.replace('{@payment_method_name}',payment_method_name)
				emailContent = emailContent.replace('{@gross_amount}',str(postdata["sub_total"]))
				emailContent = emailContent.replace('{@shipping_cost}',str(postdata["shipping_charge"]))
				emailContent = emailContent.replace('{@tax_amount}',str(postdata["tax_amount"]))
				emailContent = emailContent.replace('{@discount_amount}',str(postdata["gross_discount"]))
				emailContent = emailContent.replace('{@net_amount}',str(postdata["net_total"]))
				#******** GENERATE AUTO RESPONDER (END)********#
				emailcomponent.sendOrderMail(company_db,customerdetails["billing_email_address"],autoResponderData["email_from"],autoResponderData["subject"],emailContent)
			
			elastic = common.save_data_to_elastic(order_id,'EngageboostOrdermaster')
			data={"status":1,"api_status":"Order updated successfully","message":"Order updated successfully"}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Something went wrong"}
		return Response(data)

class DeleteOrder(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata=request.data
		ids         = None 
		company_id  = None
		website_id  = None
		receiptid_format = None
		company_db = loginview.db_active_connection(request)
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		if 'ids' in requestdata:
			ids = requestdata['ids']
		if 'company_id' in requestdata:
			company_id = requestdata['company_id']
		else:
			company_id = 1
		if 'website_id' in requestdata:
			website_id = requestdata['website_id']
		else:
			website_id = 1
		if 'receiptid_format' in requestdata:
			receiptid_format = requestdata['receiptid_format']
		# return_message = '';
		# return_message = $this->data['Orders']['return_note'];
		# if($return_note == 'Others'){
		# 	$return_message = $this->data['Orders']['return_others_reason'];
		# }
		if ids:
			idArray = ids.split("^")
			rs_order  = EngageboostOrdermaster.objects.using(company_db).filter(id__in =idArray).all()
			# .values('id,customer_id,delivery_phone,custom_order_id, order_status, applied_coupon,custom_order_id')
			orderData = ViewOrderSerializer(rs_order, many=True)
			orderData = orderData.data
			for order_data in orderData:
				# start for pending order...
				if order_data['order_status'] == 99 or order_data['order_status'] == 0: 
					# Pending and waiting approval order for cancellaton...
					EngageboostOrdermaster.objects.using(company_db).filter(id=order_data['id']).update(order_status=2)
					common.save_order_activity(company_db,order_data['id'],now_utc,0,"Order has been Cancled",'',2)
					# Send Mail and SMS
					# $this->sendmail_order($order_id, 'No', 6);
					# $this->send_sms($orderData, 6, $orderData['OrderList']['delivery_phone'],1, $orderData['OrderList']['customer_id']);
					common.sms_send_by_AutoResponder(order_data['id'],None, 16)
				else:
					total_refund_quantity_check  = 0
					for order_products in order_data['order_products']:
						refund_quantity = order_products['grn_quantity']
						if total_refund_quantity_check and refund_quantity:
							total_refund_quantity_check = int(total_refund_quantity_check) + int(refund_quantity)
					# echo $total_refund_quantity_check; exit;
					if total_refund_quantity_check == 0:
						EngageboostOrdermaster.objects.using(company_db).filter(id=order_data['id']).update(order_status=2)
						common.save_order_activity(company_db,order_data['id'],now_utc,0,"Order has been Cancled",'',2)
						common.sms_send_by_AutoResponder(order_data['id'],None, 16)
						# $this->save_order_activity($value,$activity_time,'2');
						# $this->sendmail_order($order_id, 'No', 6);
						# $this->send_sms($orderData, 6, $orderData['OrderList']['delivery_phone'],1, $orderData['OrderList']['customer_id']);
					else:
						i = 0
						order_data = {}
						refund_quantity = 0
						shortage_quantity = 0
						for order_products in order_data['order_products']:
							refund_quantity = order_products['grn_quantity']
							# update_order_refund($order_id,$Order['OrderProduct']['product_id'],$refund_quantity,$shortage_quantity,$return_order_type);
							if refund_quantity > 0:
								order_return_details = {}
								order_return_details = {
									'website_id':website_id,
									'order_id':order_id,
									'product_id':Order['OrderProduct']['product_id'],
									'return_by_id':logged_user_id,
									'quantity':refund_quantity,
									'reason':return_message,
									'return_status':Authorized
								}
								EngageboostOrderReturnDetails.objects.create(**order_return_details)
								customer_return_details = {}
								customer_return_details = {
								   'customer_id':order_data['customer_id'],
								   'order_id':order_id,
								   'product_id':order_products['product_id'],
								   'customer_return_status':'Return Initiated'
								}
								EngageboostCustomerReturnStatus.objects.create(**customer_return_details)
						EngageboostOrdermaster.objects.using(company_db).filter(id__in =idArray).update(
							order_status     = 7,
							return_status    = 'Authorized'
						)
						
						# activity_msg = "Return Reason : ".$return_message." for order-".$orderData['OrderList']['custom_order_id'];
						# $this->save_order_activity($value,$activity_time,'7',$activity_msg);
						# $this->sendmail_order($order_id, 'No', 6);
						# $this->send_sms($orderData, 6, $orderData['OrderList']['delivery_phone'],1,$orderData['OrderList']['customer_id']);   
						# $this->sendmail_invoice($order_id);
						# $this->send_sms_invoice($order_id,5); # sms for invoice				 

				# // coupon update...
				# if(is_array($orderData) && !empty($orderData['OrderList']['applied_coupon'])) {
				#     $applied_coupon = trim($orderData['OrderList']['applied_coupon']);
				#     if(!empty($applied_coupon)) {
				#         $discount_array = $this->generate_discount_conditions_coupon($website_id,$applied_coupon);
				#         if($discount_array[0]['DiscountMaster']['coupon_type'] ==1) {
				#             # before multiple discount coupon single user scenario ...
				#             if($discount_array[0]['DiscountMaster']['used_coupon']==1) {
				#                 $new_discount_array['DiscountMaster']['id'] = $discount_array[0]['DiscountMaster']['id'];
				#                 $new_discount_array['DiscountMaster']['used_coupon'] = 0;
				#                 $this->DiscountMaster->save($new_discount_array['DiscountMaster']);
				#             }
				#             if(!empty($discount_array[0]['DiscountMasterCoupon']) && $discount_array[0]['DiscountMasterCoupon'][0]['is_used']=='y') {
				#                 $discount_master_coupons_used = array();
				#                 $discount_master_coupons_used['is_used']='n';
				#                 $discount_master_coupons_used['id']=$discount_array[0]['DiscountMasterCoupon'][0]['id'];
				#                 $this->DiscountMasterCoupon->save($discount_master_coupons_used);          
				#             }
				#         }        
				#     }
				# }
				# // unset coupon...end....
				# if order_status == 99 or order_status == 0:
				#     order_product_cancel(value, website_id,receiptid_format)
		data = {
			"status":1
		}
		return Response(data)

class testorder(generics.ListAPIView):
	def post(self, request, *args, **kwargs):
		company_db = loginview.db_active_connection(request)
		# order_id = 1
		# now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		# activityType = 1
		# activity_details = common.save_order_activity(company_db,order_id,now_utc,0,"Order has been placed",'',activityType)
		# print(activity_details)

		update_order_refund(8, 16, 1,0, 'Cancellation', 1, 0, 1, 1)

		data = {
			"status":1        
		}

		return Response(data)

def update_order_refund(order_id, product_id, refund_quantity=0,shortage_quantity=0, return_order_type='Cancellation', grn_quantity=0, instock_qty=0, website_id=None, logged_user_id=None):

	if website_id is None:
		website_id = 1
			
	logged_user_id = 1

	rs_refund = EngageboostOrderProducts.objects.filter(order_id=order_id,product_id=product_id).values('order__gross_amount')
	all_data_shipped = OrderProductsViewSerializer(rs_refund, many=True)

	# print(json.dumps(all_data_shipped.data))
	rest_quantity  = int(refund_quantity) + int(shortage_quantity)

	data = {
		"status":1
	}
	return Response(data)


	# for shipped in all_data_shipped.data:
	#     if($rest_quantity >= $shipped['OrderProduct']['quantity']) {
	#         $updatequantity = $shipped['OrderProduct']['quantity'];	
	#     } else {
	#         $updatequantity = $rest_quantity;
	#     }
	#     if($shortage_quantity > 0 && $shortage_quantity > $shipped['OrderProduct']['quantity']) {
	#         $shortage_quantity = $shipped['OrderProduct']['quantity'];	
	#     }
	#     $shipped_save = array();
	#     if($return_order_type == 'Cancellation') {
	#         $shipped_save['OrderProduct']['id'] = $shipped['OrderProduct']['id'];
	#         $shipped_save['OrderProduct']['returns'] = $shipped['OrderProduct']['returns'] + $updatequantity ;
	#         $this->OrderProduct->save($shipped_save['OrderProduct']);
	#     } else {
	#         $shipped_save['OrderProduct']['id'] = $shipped['OrderProduct']['id'];
	#         if($shortage_quantity > 0) {
	#             $shipped_save['OrderProduct']['shortage'] = $shortage_quantity;
	#         } else {
	#             $shipped_save['OrderProduct']['shortage'] = $shipped['OrderProduct']['shortage'];
	#         }
	#         if($refund_quantity > 0) {
	#             if($return_order_type == 'GRN Cancellation') {
	#                 $shipped_save['OrderProduct']['returns'] = $refund_quantity;
	#             } else {
	#                 if($refund_quantity > 0 && ($shipped['OrderProduct']['quantity'] >= $shipped['OrderProduct']['returns']+$refund_quantity)) {
	#                     $shipped_save['OrderProduct']['returns'] = $shipped['OrderProduct']['returns']+$refund_quantity;
	#                 }
	#             }
	#             if($grn_quantity == 0 && $shipped['OrderProduct']['grn_quantity'] > 0) {
	#                 $shipped_save['OrderProduct']['grn_quantity'] = $shipped['OrderProduct']['grn_quantity']-$refund_quantity;
	#             }
	#         }
	#         if($grn_quantity > 0) {
	#             $shipped_save['OrderProduct']['grn_quantity'] = $grn_quantity;
	#         }
	#         # /*if($instock_qty > 0) {
	#         #     $shipped_save['OrderProduct']['instock_qty'] = $instock_qty;
	#         # }*/
	#         $this->OrderProduct->save($shipped_save['OrderProduct']);
	#         $total_price = $updatequantity*$shipped['OrderProduct']['product_price'];
	#         $tax_price 	= $updatequantity*$shipped['OrderProduct']['product_tax_price']; // added by cds for tax...
	#         $total_price_discount = $updatequantity*$shipped['OrderProduct']['product_discount_price'];
			
	#         # /*this is for main price minus*/
	#         $net_amount = $shipped['OrderList']['net_amount']-$total_price;
	#         $total_tax_amount =  $shipped['OrderList']['tax_amount'] - $tax_price; // added by cds for tax...
	#         # // Shipping cost calculation for return product...
	#         if($return_order_type != 'GRN Cancellation') {
	#             $shortage_amount = 0;
	#             if($shipped_save['OrderProduct']['shortage'] > 0) {
	#                 $shortage_amount = $shipped_save['OrderProduct']['shortage']*$shipped['OrderProduct']['product_price'];
	#             }
	#             $order_amt = $net_amount + $total_tax_amount + $shortage_amount;
	#             $shipping_arr = $this->get_information_shipping_admin($shipped['OrderList']['delivery_country'],$shipped['OrderList']['delivery_state'], $order_amt, $website_id); // shipping adn cod
	#             $shipping_cost = floatval($shipping_arr['shipping_cost']);
	#             $this->OrderList->id = $order_id;
	#             $this->OrderList->saveField('shipping_cost', $shipping_cost);
	#         }
	#         # // end Shipping cost calculation for return product...
	#         if($return_order_type != 'Delete Cancellation') {
	#             # //$this->Update_Order_product_Discount_Shipping_grn($shipped, $order_id, $shipped['OrderProduct']['id'], $shipped['OrderProduct']['product_price'], $website_id);
	#             $this->update_order_and_order_products($order_id, $return_order_type,$website_id);
	#         }
	#         $return_message = "Return from GRN";
	#         if($refund_quantity > 0 && ($return_order_type == 'GRN Cancellation' || $return_order_type == 'Delete Cancellation') ) {
	#             $order_return_details = array();
	#             $order_return_details['website_id'] = $website_id;
	#             $order_return_details['order_id'] = $order_id;
	#             $order_return_details['product_id'] = $shipped['OrderProduct']['product_id'];
	#             $order_return_details['return_by_id'] = $logged_user_id;
	#             $order_return_details['quantity'] = $refund_quantity;
	#             $order_return_details['reason'] = $return_message;
	#             $order_return_details['return_status'] = 'Authorized';
	#             $this->OrderReturnDetail->create();
	#             $this->OrderReturnDetail->save($order_return_details);

	#             $customer_return_details = array();
	#             $customer_return_details['customer_id'] = $shipped['OrderList']['customer_id'];
	#             $customer_return_details['order_id'] =  $order_id;
	#             $customer_return_details['product_id'] =  $shipped['OrderProduct']['product_id'];
	#             $customer_return_details['customer_return_status'] =  'Return Initiated';
	#             $this->CustomerReturn->create();
	#             $this->CustomerReturn->save($customer_return_details);
	#             $activity_time = date("Y-m-d H:i:s");
	#             $activity_msg = "Return Reason : ".$return_message." for product sku-".$shipped['Product']['sku'];
	#             $order_status = 7;
	#             $this->save_order_activity($order_id,$activity_time,$order_status,$activity_msg);
	#             $OrderList = array();
	#             $OrderList['OrderList']['id'] = $order_id;
	#             $OrderList['OrderList']['return_status'] = 'Processing';
	#             $this->OrderList->id = $order_id;
	#             $this->OrderList->save($OrderList);
	#         }
	#     }
	# }

class GetOrderDeliverySlot(generics.ListAPIView):

	def post(self, request, *args, **kwargs):
		company_db = loginview.db_active_connection(request)
		result = EngageboostOrdermaster.objects.using(company_db).exclude(slot_start_time__isnull=True).values('time_slot_id', 'slot_start_time', 'slot_end_time').all()
		if request.data.get('delivery_date'):
			delivery_date_arr = request.data.get('delivery_date').split("##")
			delivery_date_from = delivery_date_arr[0]; delivery_date_to = delivery_date_arr[1]
			if delivery_date_from == 'null' and delivery_date_to == 'null':
				pass
			else:
				result=result.filter(created__range=[delivery_date_from,delivery_date_to]).distinct()
				pass
		else:
			now 	= datetime.datetime.now()
			today 	= now.date() 
		
		# resultdata = OrderMasterSerializer(result,many=True)    # delivery_date_from = 
		for times in result:
			if ":" in times['slot_start_time']:
				start = datetime.datetime.strptime(times['slot_start_time'], "%H:%M")
				start = datetime.datetime.strftime(start, "%I:%M %p")
			else:
				start = datetime.datetime.strptime(times['slot_start_time'], "%H")
				start = datetime.datetime.strftime(start, "%I:%M %p")    
			if ":" in times['slot_end_time']:
				end = datetime.datetime.strptime(times['slot_end_time'], "%H:%M")
				end = datetime.datetime.strftime(end, "%I:%M %p")
			else:
				end = datetime.datetime.strptime(times['slot_end_time'], "%H")
				end = datetime.datetime.strftime(end, "%I:%M %p")
			time_slot_id = str(start)+"-"+str(end)
			time_slot_id = time_slot_id.lower()
			times['time_slot_id'] = time_slot_id
			# print(time_slot_id)    
		
		data = {
			"status":1,
			"time_slot":result
		}
		return Response(data)
				
class OrderExport(generics.ListAPIView):

	def post(self, request, *args, **kwargs):
		company_db = loginview.db_active_connection(request)
		date=EngageboostGlobalSettings.objects.get(website_id=1)
		zone = EngageboostTimezones.objects.get(id=date.timezone_id)

		fromDate = toDate = datetime.datetime.today()
		requestdata = request.data
		if 'fromDate' in requestdata:
			fromDate = requestdata['fromDate']

		if 'toDate' in requestdata:
			toDate = requestdata['toDate']

		order_ids = []


		## ************  Check file dir exist or not. If dir not exist then create
		file_dir = settings.MEDIA_ROOT+'/exportfile/'
		export_dir = settings.MEDIA_URL+'exportfile/'
		if not os.path.exists(file_dir):
			os.makedirs(file_dir)
		## ************  Create file name
		try:
			if request.data.get('show_item_wise_order')<=0:
				file_name = "order_export_"+get_random_string(length=5)
			else:
				file_name = "order_export_itemwise_"+get_random_string(length=5)
		except:
			file_name = "order_export_itemwise_"+get_random_string(length=5)        

		try:
			if request.data.get('order_ids')!="" and request.data.get('order_ids')!=None:
				order_ids = request.data.get('order_ids')
				order_ids = order_ids.split(",")
			else:
				order_ids = []
		except:
			order_ids = []

		## Create file full path
		file_path = file_dir+file_name+'.xlsx'
		export_file_path = export_dir+file_name+'.xlsx'
		export_file_path = export_file_path[1:]

		workbook 	= xlsxwriter.Workbook(file_path)		
		worksheet 	= workbook.add_worksheet()
		if int(request.data.get('show_item_wise_order'))<=0:
			result = EngageboostOrdermaster.objects.using(company_db).filter(isdeleted='n', buy_status='1')
			if request.data.get('order_status'):
				list_of_order_status = request.data.get('order_status').split(",")
				order_status_field_value=[]
				for values in list_of_order_status:
					order_status_field_value.append(values)
				result=result.filter(order_status__in=order_status_field_value)
				
			# if request.data.get('webshop_id'):
			#     list_of_webshop_id = request.data.get('webshop_id').split(",")
			#     webshop_id_field_value=[]
			#     for values in list_of_webshop_id:
			#         webshop_id_field_value.append(values)
			#     result=result.filter(webshop_id__in=webshop_id_field_value)

			if request.data.get('warehouse_id'):
				list_of_warehouse_id = request.data.get('warehouse_id').split(",")
				warehouse_id_field_value=[]
				for values in list_of_warehouse_id:
					warehouse_id_field_value.append(values)
				result=result.filter(assign_to__in=warehouse_id_field_value)

			if request.data.get('destination'):
				list_of_destination = request.data.get('destination').split(",")
				destination_field_value=[]
				for values in list_of_destination:
					destination_field_value.append(values)
				result=result.filter(delivery_country__in=destination_field_value)

			if request.data.get('tags'):
				list_of_tags = request.data.get('tags').split(",")
				tags_field_value=[]
				for values in list_of_tags:
					tags_field_value.append(values)
				result=result.filter(tags__in=tags_field_value)

			if request.data.get('date'):
				date = request.data.get('date').split("##")
				start_date = date[0]; end_date = date[1]
				if start_date == 'null' and end_date == 'null':
					pass
				else:
					result=result.filter(created__range=[start_date,end_date])

			if request.data.get('zones'):
				list_of_zones = request.data.get('zones').split(",")
				zone_field_value=[]
				for values in list_of_zones:
					zone_field_value.append(values)
				result=result.filter(zone_id__in=zone_field_value)

			if request.data.get('delivery_date'):
				date = request.data.get('delivery_date').split("##")
				delivery_date_from = date[0]; delivery_date_to = date[1]
				if delivery_date_from == 'null' and delivery_date_to == 'null':
					pass
				else:
					result=result.filter(delivery_date__range=[delivery_date_from,delivery_date_to])

			if request.data.get('delivery_slot'):
				list_of_delivery_slot = request.data.get('delivery_slot').split(",")
				delivery_slot_field_value=[]
				for values in list_of_shipping_status:
					delivery_slot_field_value.append(values)
				result=result.filter(slot_start_time__in=delivery_slot_field_value)				

			if request.data.get('shipping_status'):
				list_of_shipping_status = request.data.get('shipping_status').split(",")
				shipping_status_field_value=[]
				for values in list_of_shipping_status:
					shipping_status_field_value.append(values)
				result=result.filter(channel_shipping_status__in=shipping_status_field_value)        
			
			if request.data.get('advance_filter'):
				field_value=[]
				advance_filters = ast.literal_eval(request.data.get('advance_filter'))
				for advance_filter in advance_filters:
					list_of_values = advance_filter["value"].split(",")
					field_value=[]
					for values in list_of_values:
						field_value.append(values)
					
					if advance_filter["find_type"]=="equal":
						field = {advance_filter["field"]+'__in':field_value}
						result=result.filter(**field)
					elif advance_filter["find_type"]=="notequal":
						field = {advance_filter["field"]+'__in':field_value}
						result=result.filter(~Q(**field))
					else:
						field = {advance_filter["field"]+'__icontains':field_value}
						result=result.filter(**field)
			
			# if len(order_ids)>0:
			# 	result = result.filter(id__in=order_ids)

			if fromDate and toDate:
				result = result.filter(created__range=[fromDate, toDate])

			result = result.order_by('id') 
			result_all = result.count()
			result1 = result.count()
			result2 = result.count() 
			result=result
			result_data = ViewOrderSerializer(result, many=True)
			# result_data = OrderAndOrderProductSerializer(result, many=True)
			# DeliveryOrderDetailsSerializer
			result_data = result_data.data
			bold = workbook.add_format({'bold': True})
			row = 1

			worksheet.write(0,0,'Order Date',bold)
			worksheet.write(0,1,'Delivery Date',bold)
			worksheet.write(0,2,'Order Day',bold)
			worksheet.write(0,3,'Order Id',bold)
			worksheet.write(0,4,'Customer Name',bold)
			worksheet.write(0,5,'Shipping Address',bold)
			worksheet.write(0,6,'Shipping PIN Code',bold)
			worksheet.write(0,7,'Shipping State',bold)
			worksheet.write(0,8,'Shipping Email Address',bold)
			worksheet.write(0,9,'Phone',bold)
			worksheet.write(0,10,'Store',bold)

			worksheet.write(0,11,'Payment Type',bold)
			worksheet.write(0,12,'Net Amount',bold)
			worksheet.write(0,13,'Coupon Discount',bold)
			worksheet.write(0,14,'Tax Amount',bold)
			worksheet.write(0,15,'Delivery Charge',bold)
			worksheet.write(0,16,'Gross Amount',bold)
			worksheet.write(0,17,'Discount Amount',bold)
			worksheet.write(0,18,'Amount Paid',bold)
			worksheet.write(0,19,'Balance Due',bold)
			worksheet.write(0,20,'Transaction Id',bold)
			worksheet.write(0,21,'Referral code',bold)
			worksheet.write(0,22,'Payment Order Id',bold)
			worksheet.write(0,23,'Quantity',bold)
			# worksheet.write(0,24,'Order From',bold)
			worksheet.write(0,25,'Status',bold)
			worksheet.write(0,26,'Last Activities',bold)
			worksheet.write(0,27,'Applied Coupon',bold)
			worksheet.write(0,28,'Original Amount',bold)
			worksheet.write(0,29,'Special Instructions',bold)
			# worksheet.write(0,30,'Tags',bold)
			#worksheet.write(0,30,'Crate No.',bold)

			for resultdata in result_data:
				time_slot_date = resultdata['time_slot_date'] if (resultdata['time_slot_date']!=None and resultdata['time_slot_date']!="")  else ""
				time_slot_id = resultdata['time_slot_id'] if (resultdata['time_slot_id']!=None and resultdata['time_slot_id']!="")  else ""
				first_name = resultdata['customer']['first_name'] if (resultdata['customer'] and resultdata['customer']['first_name']!=None and resultdata['customer']['first_name']!="")  else ""
				delivery_street_address = resultdata['delivery_street_address'] if (resultdata['delivery_street_address']!=None and resultdata['delivery_street_address']!="")  else ""
				delivery_street_address1 = resultdata['delivery_street_address1'] if (resultdata['delivery_street_address1']!=None and resultdata['delivery_street_address1']!="")  else ""
				try:
					dt = datetime.datetime.strptime(resultdata['created'],'%Y-%m-%dT%H:%M:%S.%fZ')
				except:
					dt = datetime.datetime.strptime(resultdata['created'],'%Y-%m-%dT%H:%M:%S%fZ')
				
				order_date=common.get_time(resultdata['created'],zone,date)
				# order_date = dt.strftime("%d-%m-%Y %I:%M %p")
				# order_date_arr = resultdata['created'].split('-')
				# order_date = (order_date_arr[0]+"-"+order_date_arr[1]+"-"+order_date_arr[2])
				worksheet.write(row,0,order_date,0)
				worksheet.write(row,1, str(time_slot_date),0)
				worksheet.write(row,2,dt.strftime("%A"),0)
				worksheet.write(row,3,resultdata['custom_order_id'],0)
				worksheet.write(row,4,str(first_name),0)
				worksheet.write(row,5,str(delivery_street_address) + " " + str(delivery_street_address1) ,0)
				worksheet.write(row,6,resultdata['delivery_postcode'],0)
				worksheet.write(row,7,resultdata['delivery_state_name'],0)
				worksheet.write(row,8,resultdata['delivery_email_address'],0)
				worksheet.write(row,9,resultdata['delivery_phone'],0)
				worksheet.write(row,10,resultdata['warehouse_name'],0)

				worksheet.write(row,11,resultdata['payment_method_name'],0)
				worksheet.write(row,12,resultdata['net_amount'],0)
				worksheet.write(row,13,resultdata['cart_discount'],0)
				worksheet.write(row,14,resultdata['tax_amount'],0)
				worksheet.write(row,15,resultdata['shipping_cost'],0)
				worksheet.write(row,16,resultdata['gross_amount'],0)
				worksheet.write(row,17,resultdata['gross_discount_amount'],0)
				worksheet.write(row,18,resultdata['paid_amount'],0)
				worksheet.write(row,19,(resultdata['gross_amount'] - resultdata['paid_amount']),0)

				# worksheet.write(row,20,resultdata['Transaction Id'],0)
				# worksheet.write(row,21,resultdata['Referral code'],0)
				# worksheet.write(row,22,resultdata['Payment Order Id'],0)
				cnt_product = 0
				if resultdata['order_products'] and len(resultdata['order_products'])>0:
					for order_pro in resultdata['order_products']:
						cnt_product = cnt_product + int(order_pro['quantity'])

				worksheet.write(row,23,cnt_product,0)
				# worksheet.write(row,24,resultdata['Order From'],0)
				order_status = ""
				order_status = CheckOrderStatusByOrderStatus(resultdata['order_status'], resultdata['buy_status'])
				worksheet.write(row,25,order_status,0)
				# worksheet.write(row,26,resultdata['zone_name'],0)
				if resultdata["order_activity"] and len(resultdata["order_activity"])>0:
					worksheet.write(row,27,resultdata["order_activity"][0]['activity_comments'],0)
				else:
					worksheet.write(row,27," ",0)

				worksheet.write(row,27,resultdata['applied_coupon'],0)
				worksheet.write(row,28,resultdata['gross_amount'],0)
				worksheet.write(row,29,resultdata['custom_msg'],0)
				# worksheet.write(row,30,resultdata['Tags'],0)
				# worksheet.write(row,31,resultdata['Crate No.'],0)

				row = row + 1
			# list_data = []
			workbook.close()
			data ={'status':1,"file_path":export_file_path, 'data':result_data}
		else:
			result = EngageboostOrderProducts.objects.using(company_db).all()
			if request.data.get('order_status'):
				list_of_order_status = request.data.get('order_status').split(",")
				order_status_field_value=[]
				for values in list_of_order_status:
					order_status_field_value.append(values)
				result=result.filter(status__in=order_status_field_value)

			if request.data.get('webshop_id'):
				list_of_webshop_id = request.data.get('webshop_id').split(",")
				webshop_id_field_value=[]
				order_ids=[]
				for values in list_of_webshop_id:
					webshop_id_field_value.append(values)

				webshop_cond = EngageboostOrdermaster.objects.all().filter(webshop_id__in=webshop_id_field_value)
				if webshop_cond:
					orderMasterDetails = OrderMasterSerializer(webshop_cond,many=True)

					for orderMaster in orderMasterDetails.data:
						order_ids.append(orderMaster["id"])

				result=result.filter(order_id__in=order_ids)

			if request.data.get('warehouse_id'):
				list_of_warehouse_id = request.data.get('warehouse_id').split(",")
				warehouse_id_field_value=[]
				for values in list_of_warehouse_id:
					warehouse_id_field_value.append(values)
				result=result.filter(assign_to__in=warehouse_id_field_value)

			if request.data.get('destination'):
				list_of_destination = request.data.get('destination').split(",")
				destination_field_value=[]
				order_ids=[]
				for values in list_of_destination:
					destination_field_value.append(values)


				webshop_cond = EngageboostOrdermaster.objects.all().filter(delivery_country__in=destination_field_value)
				if webshop_cond:
					orderMasterDetails = OrderMasterSerializer(webshop_cond,many=True)

					for orderMaster in orderMasterDetails.data:
						order_ids.append(orderMaster["id"])

				result=result.filter(order_id__in=order_ids)

			if request.data.get('tags'):
				list_of_tags = request.data.get('tags').split(",")
				tags_field_value=[]
				for values in list_of_tags:
					tags_field_value.append(values)
				result=result.filter(tags__in=tags_field_value)

			if request.data.get('date'):
				date = request.data.get('date').split("##")
				start_date = date[0]; end_date = date[1]
				if start_date == 'null' and end_date == 'null':
					pass
				else:
					result=result.filter(created__range=[start_date,end_date])
			
			result = result.order_by('order__created')
				# result=result.filter(created__range=[start_date,end_date])

			# [{"field":"custom_order_id","value":"#ABC001,#ABC006","find_type":""},{"field":"webshop_id","value":"","find_type":""}]
			
			if request.data.get('advance_filter'):
				field_value=[]
				advance_filters = ast.literal_eval(request.data.get('advance_filter'))
				for advance_filter in advance_filters:
					list_of_values = advance_filter["value"].split(",")
					field_value=[]
					for values in list_of_values:
						field_value.append(values)
					# print(field_value)
					if advance_filter["find_type"]=="equal":
						field = {advance_filter["field"]+'__in':field_value}
						result=result.filter(**field)
					elif advance_filter["find_type"]=="notequal":
						field = {advance_filter["field"]+'__in':field_value}
						result=result.filter(~Q(**field))
					else:
						field = {advance_filter["field"]+'__icontains':field_value}
						result=result.filter(**field)
					# Model.objects.extra(where=['FIND_IN_SET(15, field)'])
			
			if len(order_ids)>0:
				result = result.filter(id__in=order_ids)		
			
			result_all = result.count()
			result1 = result.count()
			result2 = result.count() 
			result=result
			order_product = OrderProductsSerializer(result, many=True)
			data ={
				"status":1,
				"data":order_product.data
			}
		return Response(data)


# class order_activity():
#     def post(self, request, *args, **kwargs):
#         company_db = loginview.db_active_connection(request)
		
#         save_order_activity(company_db,order_id=None,activity_time=None,status=None,msg=None,userId=None,activityType=1)

def generateNewUserName(email):
	# username = slugify(email.split('@', 1)[0])
	# User = get_user_model()
	# while User.objects.filter(username=username).exists():
	#     username += get_random_string(length=5)
	username = get_random_string(length=5)
	return username

def printj(jsn):
	print(json.dumps(jsn, indent=4, sort_keys=True))

def CheckOrderStatusByOrderStatus(order_status, buy_status):
	# //////////// start the status settings //////////////////////
	buy_status = str(buy_status)
	order_status = str(order_status)
	if (order_status == '99' and buy_status == '1'):
		order_status = 'Waiting Approval'
	elif (order_status == '20' and buy_status == '1'):
		order_status = 'Approved';
	elif (order_status == '0' and buy_status == '1'):
		order_status = 'Pending'
	elif (order_status == '100' and buy_status == '1'):
		order_status = 'Processing'
	elif (order_status == '1' and buy_status == '1'):
		order_status = 'Shipped'
	elif (order_status == '2' and buy_status == '1'):
		order_status = 'Cancelled'
	elif (order_status == '4' and buy_status == '1'):
		order_status = 'Completed'
	elif (order_status == '5' and buy_status == '1'):
		order_status = 'Full Refund'
	elif (order_status == '6' and buy_status == '1'):
		order_status = 'Partial Refund'
	elif (order_status == '7' and buy_status == '1'):
		order_status = 'Return Initiate'
	elif (order_status == '12' and buy_status == '1'):
		order_status = 'Assigned to Showroom'
	elif (order_status == '13' and buy_status == '1'):
		order_status = 'Delivered'
	elif (order_status == '16' and buy_status == '1'):
		order_status = 'Closed'
	elif (order_status == '18' and buy_status == '1'):
		order_status = 'Pending Service'
	elif (order_status == '3' and buy_status == '0'):
		order_status = 'Abandoned'
	elif (order_status == '999' and buy_status == '0'):
		order_status = 'Failed'
	elif (order_status == '9999' and buy_status == '0'):
		order_status = 'Hold'
	else:
		order_status = 'Invoiced'
	return order_status

class OrderActivity(generics.ListAPIView):
	def get(self, request,order_id, website_id, format=None,partial=True):
		#data={"status":0,"api_status":serializer.errors,"message":'Error occured'}
		company_db = loginview.db_active_connection(request)
		order_activity = EngageboostOrderActivity.objects.using(company_db).all().filter(order_id=order_id).order_by('-id')
		serializer = OrderActivitySerializer(order_activity,many=True)
		if serializer.data:
			data = {
				'status':1,
				'api_status': serializer.data,
				'message':'Successfully getting data',
			}
		else:
			data = {
				'status':0,
				'api_status':[],
				'message':'Data Not Found',
			}
		return Response(data)

	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		order_id = request.data["order_id"]
		activity_time = datetime.datetime.now() 
		status = request.data["status"]
		msg = request.data["activity_comments"]
		activityType = request.data["activity_type"]
		userId = request.data["user_id"]
		result = common.save_order_activity(company_db,order_id,activity_time,status,msg,userId,activityType)
		data ={"status":1,"data":result}
		return Response(data)

# Web Services for all Order View  List popup order edit listing
class OrdersLoadViewProduct(generics.ListAPIView):  
	def post(self, request, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		postdata = request.data
		website_id = postdata['website_id']
		channel_id = postdata['channel_id']
		order_type = postdata['order_type']
		order_by = postdata['order_by']
		show_all = postdata['show_all']
		if 'product_ids' not in request.data:
			product_ids = []
		else:
			product_ids=request.data['product_ids']
		search_key = None
		if "search" in postdata:
			search_key = postdata["search"]
		currency_id = ""
		if "currency_id" in postdata:
			currency_id = postdata["currency_id"]

		if(order_type=='+'):
			order=order_by
		elif(order_type=='-'):
			order='-'+order_by
		company_db = loginview.db_active_connection(request)
		
		productObj = EngageboostProducts.objects.using(company_db).filter(website_id=website_id,isblocked='n',isdeleted='n')
		product = productObj.all()
		product_arr=[]
		for products in product:
			value_stock=EngageboostProductStocks.objects.using(company_db).filter(warehouse_id=products.warehouse_id,product_id=products.id)
			# if value_stock.count()>0:
			#     value = value_stock.first()
			#     if value.real_stock !=0:
			product_arr.append(products.id)

		productObj = productObj.order_by(order).filter(id__in=product_arr).filter(Q(default_price__gte=0))
		if len(product_ids)>0:
			productObj = productObj.filter(id__in=product_ids)
		if search_key is not None:
			productObj = productObj.filter(Q(name__icontains=search_key)|Q(sku__icontains=search_key))

		length_of_list = productObj.count()
		page = self.paginate_queryset(productObj.all())
		if show_all > 0:
			page_size = length_of_list
		else:
			page_size = get_page_size()

		if page_size <= 0:
			page_size = 1
		
		serializer_product = BasicinfoSerializer(page,many=True)
		if(serializer_product):
			currency_rate=EngageboostCurrencyRates.objects.using(company_db).get(isbasecurrency='y',engageboost_company_website_id=website_id) 
			counter=0
			for product_price_fetch in serializer_product.data:
				queryset=EngageboostChannelCurrencyProductPrice.objects.using(company_db).filter(currency_id=currency_rate.engageboost_currency_master_id,channel_id=6,product_id=product_price_fetch['id']).count()
				if queryset >0:
					product_price=EngageboostChannelCurrencyProductPrice.objects.using(company_db).get(currency_id=currency_rate.engageboost_currency_master_id,channel_id=6,product_id=product_price_fetch['id'])
					serializer_product.data[counter]['default_price'] = product_price.price
				counter=counter+1
			pre_data ={
				'status':1,
				'products':serializer_product.data
			}
		else:
			pre_data ={
				'status':0,
				'products':[],
				'api_status':serializer.errors,
				'message':'Data Not Found'
			}
		# return Response(data)

		results_arr = []
		results_arr.append(pre_data)
		result = {"count":length_of_list,"per_page_count": math.ceil(length_of_list/page_size),"page_size":page_size,"results":results_arr}
		# return Response(result)
		return self.get_paginated_response(results_arr)

# substitude product price and details calculation....by cds on 28th Jan 2020
def get_substitude_product_cart(website_id,product_id,quantity,warehouse_id=None):
		getproductforcart_net= {};
		if product_id > 0 and quantity > 0:
			checkout_info = {"product_id":product_id,"quantity":quantity}
			discount_array = common.generate_discount_conditions(website_id, None, None, warehouse_id)
			getproductforcart_net = getproductforcartNew(product_id, warehouse_id)
			if getproductforcart_net:
				getproductforcart_net["qty"] = quantity
				getproductforcart_net["new_default_price"] = float(getproductforcart_net["channel_price"])*quantity
				getproductforcart_net["new_default_price_unit"] = float(getproductforcart_net["channel_price"]) if getproductforcart_net["channel_price"] else 0.0
				getproductforcart_net["discount_price_unit"] = 0.00
				getproductforcart_net["discount_price"] = 0.00
				getproductforcart_net["discount_amount"] = 0.00
				getproductforcart_net["disc_type"] =""
				getproductforcart_net["coupon"] = ""
				#print("Data after calculation substitude product...")
				#print(getproductforcart_net)
				if discount_array:
					getproductforcart_net = common.genrate_new_prodcut_with_discount(None, getproductforcart_net, discount_array)
		#print(getproductforcart_net)
		#print("Data after calculation substitude product...")
		return getproductforcart_net


class TimeLine(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		activity_comments=request.data['activity_comments']
		order_id=request.data['order_id']
		ip_address=request.data['ip_address']
		user_id=request.data['user_id']
		user=EngageboostUsers.objects.using(company_db).get(id=user_id)
		EngageboostOrderActivity.objects.using(company_db).create(order_id=order_id,activity_date=datetime.now(),status=1,activity_comments=activity_comments,user_ip_address=ip_address,username=user.username,user_id=user_id)
		data ={
			'status':1,
			'api_status':'',
			'message':'Successfully Inserted',
			
		}
		return Response(data)

class ManageOrderDetails(generics.ListAPIView):
	def get(self, request, pk, format=None):
		rs_order = EngageboostOrdermaster.objects.filter(id=pk).first()
		order_data = ViewOrderSerializer(rs_order)
		order_data = order_data.data
		zone_id = ""
		data = {
			"status":1,
			"data":order_data
		}
		return Response(data)

class InvoiceList(generics.ListAPIView):
	# """ Stock List """
	def post(self, request, format=None,many=True):
		from datetime import datetime, timedelta, date
		from dateutil.relativedelta import relativedelta
		company_db = loginview.db_active_connection(request)
		#####################Query Generation#################################
		order_type=request.data['order_type']
		order_by=request.data['order_by']
		try:
			if request.data['search']:
				key = request.data['search']
				key = key.strip()
			else:
				key = ""
		except:
			key = ""
		try:
			product_id=request.data['product_id']
		except:
			product_id = ""
	   
		today = datetime.today()
		try:
			end_date = postdata['end_date']
			try:
				end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
			except:
				end_date = datetime.strptime(end_date, "%Y-%m-%d")
			end_date = end_date.strftime("%Y-%m-%d")
		except:
			end_date = today
			end_date = end_date.strftime("%Y-%m-%d")
		try:
			start_date = postdata['start_date']
			try:
				start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
			except:
				start_date = datetime.strptime(start_date, "%Y-%m-%d")
			start_date = start_date.strftime("%Y-%m-%d")
		except:
			start_date = today+relativedelta(days=-30)
			start_date = start_date.strftime("%Y-%m-%d")
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
			else:
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
				order_product='-'+order_by
				order='id'
		else:
			order_product = 'name'
			if(order_type=='+'):
				order=order_by
			elif(order_type=='-'):
				order='-'+order_by
			else:
				order='-'+order_by
		result_count = EngageboostInvoicemaster.objects.using(company_db).all().order_by(order).filter(isblocked='n',isdeleted='n')
		if key!="" and key!=None:
			customers_obj = EngageboostCustomers.objects.filter(isdeleted="n",isblocked="n")
			customers_obj = customers_obj.annotate(name=Concat('first_name', Value(' '), 'last_name')).order_by("name")
			customers_obj = customers_obj.filter(name__icontains=key) 
			customers_obj = customers_obj.values("id")
			result_count = result_count.filter(Q(custom_invoice_id__icontains=key)|Q(order_id__custom_order_id__icontains=key)|Q(customer_id__in=customers_obj)|Q(order_id__webshop_id__name__icontains=key))
		try:
			warehouse_id=request.data['warehouse_id']
			result_count = result_count.filter(order_id__assign_wh=warehouse_id)
		except:
			pass

		if product_id!="" and product_id!=None:
			product_count = EngageboostInvoiceProducts.objects.filter(product_id=product_id)
			if product_count.count()>0:
				product_count = product_count.all().values("invoice_id") 
				result_count = result_count.filter(id__in=product_count) 

		result_count = result_count.filter(created__range=[start_date, end_date])
		userid=request.data['userid']
		users = EngageboostUsers.objects.using(company_db).get(id=userid)
		issuperadmin = users.issuperadmin
		role_id = users.role_id
		role_permission= {}
		menu_fetch = EngageboostMenuMasters.objects.using(company_db).get(module='TrentPicklists')
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
			
		if result_count.count()>0:
			result = result_count
			if request.data.get('advanced_search'):
				filter_arr = request.data.get('advanced_search')
				result = common.get_advanced_search_filter("EngageboostInvoicemaster",filter_arr,result)    
			if show_all == 0:   
				page = self.paginate_queryset(result)
			else:
				page = result.all()
			serializer = InvoicemasterSerializer(page, many=True)
			arr=[]
			# print(serializer.data)
			if len(serializer.data)>0:
				for product in serializer.data:
					total_quantity = 0
					productinfo=EngageboostInvoiceProducts.objects.using(company_db).filter(invoice__isblocked='n',invoice__isdeleted='n',invoice_id=product['id'])
					if product_id!="" and product_id!=None:
						productinfo=productinfo.filter(product_id=product_id)
					if productinfo.count()>0:
						productinfo = productinfo.values('quantity').first()
						total_quantity = productinfo['quantity']

					date=EngageboostGlobalSettings.objects.using(company_db).get(website_id=1)
					zone=EngageboostTimezones.objects.using(company_db).get(id=date.timezone_id)
					data ={
						'invoice_id':product['custom_invoice_id'],
						'order_id':product['order']['custom_order_id'],
						'customer_name':product['customer_name'],
						'created':product['order']['created'],
						'webshop_name':product['order']['webshop']['name'],
						'quantity':total_quantity,
						'gross_amount':product['gross_amount'],
						'net_amount':product['net_amount'],
						'shipping_amount':product['order']['shipping_cost'],
						}
					arr.append(data)
					data2 ={
						'product':arr
					}
			else:
				data2 = {
					'product':[]
				}
			# page = self.paginate_queryset(result)
			pre_data={}
			final_data=[]
			pre_data['result']=data2
			pre_data['role_permission']=role_permission
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
			final_data.append(pre_data)
			return Response({'status':0, 'Message':'No Data Found'})
			# return self.get_paginated_response(final_data)

class LoyaltyPointsDetails(generics.ListAPIView):
	def post(self, request, format=None,many=True):
		user_id = 22
		request_data = request.data
		request_data = request_data['data']
		# print("request_data========", request_data)
		cartData = {
			"orderamountdetails":[
				{
					"website_id": 1,
					"webshop_id": 6,
					"shipping_charge": request_data["shipping_charge"],
					"handling_charge": request_data["handling_charge"],
					"cod_charge": request_data["cod_charge"],
					"gross_discount": request_data["gross_discount"],
					"grand_total": request_data["grand_total"],
					"sub_total": request_data["net_total"],
					"net_total": request_data["net_total"],
					"cart_discount": request_data["cart_discount"],
					"paid_amount": request_data["paid_amount"],
					"balance_due": request_data["balance_due"],
				}
			],
			"cartdetails":request_data["cartdetails"]
		}

		# print('cartData========', json.dumps(cartData))


		usable_loyalty = loyalty.get_creadit_points(cartData, user_id)
		remain_loyalty = loyalty.GetUserLoyaltyBalance(user_id)
		burn_amount = 0
		if float(remain_loyalty) >0 and float(usable_loyalty['burn_point'])>0:
			if float(remain_loyalty) >float(usable_loyalty['burn_point']):
				burn_amount = Decimal(usable_loyalty['burn_point']).quantize(Decimal('.00'))						
			else:
				if float(remain_loyalty) > float(usable_loyalty['redeem_limit']):
					burn_amount = Decimal(usable_loyalty['redeem_limit']).quantize(Decimal('.00'))
				else:
					burn_amount = Decimal(remain_loyalty).quantize(Decimal('.00'))
		else:
			burn_amount = 0
		loyalty_details = {}
		loyalty_details.update({"usable_loyalty":burn_amount,"remain_loyalty":remain_loyalty,"rule_id":usable_loyalty['rule_id'],"redeem_limit":usable_loyalty['redeem_limit']})
	
		print("loyalty_details============", loyalty_details)
		return Response(loyalty_details)

def ApplyLoyalty(request):
	# request_data = request_data['data']
	request_data = request
	# print("request_data========", request_data)
	# cartData = {
	# 	"orderamountdetails":[
	# 		{
	# 			"website_id": 1,
	# 			"webshop_id": 6,
	# 			"shipping_charge": request_data["shipping_charge"],
	# 			"handling_charge": request_data["handling_charge"],
	# 			"cod_charge": request_data["cod_charge"],
	# 			"gross_discount": request_data["gross_discount"],
	# 			"grand_total": request_data["grand_total"],
	# 			"sub_total": request_data["net_total"],
	# 			"net_total": request_data["net_total"],
	# 			"cart_discount": request_data["cart_discount"],
	# 			"paid_amount": request_data["paid_amount"],
	# 			"balance_due": request_data["balance_due"],
	# 		}
	# 	],
	# 	"cartdetails":request_data["cartdetails"]
	# }
	user_id = request_data["user_id"]
	if user_id!="":
		usable_loyalty = loyalty.get_creadit_points(request_data, user_id)
		remain_loyalty = loyalty.GetUserLoyaltyBalance(user_id)
		burn_amount = 0
		if float(remain_loyalty) >0 and float(usable_loyalty['burn_point'])>0:
			if float(remain_loyalty) >float(usable_loyalty['burn_point']):
				burn_amount = Decimal(usable_loyalty['burn_point']).quantize(Decimal('.00'))						
			else:
				if float(remain_loyalty) > float(usable_loyalty['redeem_limit']):
					burn_amount = Decimal(usable_loyalty['redeem_limit']).quantize(Decimal('.00'))
				else:
					burn_amount = Decimal(remain_loyalty).quantize(Decimal('.00'))
		else:
			burn_amount = 0
		loyalty_details = {}
		loyalty_details.update({"usable_loyalty":burn_amount,"remain_loyalty":remain_loyalty,"rule_id":usable_loyalty['rule_id'],"redeem_limit":usable_loyalty['redeem_limit']})
	else:
		loyalty_details.update({"usable_loyalty":0,"remain_loyalty":0,"rule_id":0,"redeem_limit":0})

	print("loyalty_details============", loyalty_details)
	return loyalty_details