from webservices.models import *
from django.http import Http404
from webservices.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
import datetime,time
from rest_framework import generics
from itertools import chain
from django.core import serializers
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from webservices.views import loginview
from webservices.views.common import common
from django.db.models import Q
from django.http import HttpResponse

import sys
import traceback
import json

from django.utils import timezone
import xlsxwriter
from django.db.models.functions import Concat
from django.db.models import Value
from django.db import connection
from django.db.models import Sum
import decimal
from decimal import Decimal
# from webservices.views.order import Order
from frontapp.views.product import discount
def get_time(gettime,zone,date):
	datetime = gettime.replace('T',' ')
	data_time=datetime.replace('Z',' ')
	a=data_time.split(".")
	b=a[0].replace(':',' ')
	c=b.replace('-',' ')
	date_format=c.split(" ")
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
	gettime=str(gettime)
	format1 =date.date_format
	datetime_object=datetime.datetime.strptime(gettime, '%Y-%m-%d').strftime(format1)
	return datetime_object
# """ User return popup code """

class OrderReturnRequest(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		product_id = request.data['product_id']
		website_id =  request.data['website_id']
		order_id = request.data['order_id']
		reason = request.data['reason']
		user_id = request.data['user_id']
		quantity = request.data['quantity']
		check_product_already_shipped_or_not = EngageboostOrderProducts.objects.using(company_db).filter(order_id=order_id, product_id=product_id, merchant_website_id=website_id).filter(Q(status=4))
		if check_product_already_shipped_or_not.count()>0:
			check_previous_return_request = EngageboostOrderReturnDetails.objects.using(company_db).filter(order_id=order_id, product_id=product_id, website_id=website_id, isdeleted='n',isblocked='n',return_status='Pending')
			if check_previous_return_request.count()==0:
				product_merchant_website = EngageboostOrderProducts.objects.using(company_db).get(order_id=order_id, product_id=product_id)
				EngageboostOrderReturnDetails.objects.using(company_db).create(
					order_id=order_id,
					website_id=product_merchant_website.merchant_website_id,
					product_id=product_id,
					return_by_id=user_id,
					quantity=quantity,
					reason=reason,
					created=timezone.now(),
					modified=timezone.now(),
					return_status='Pending'
				)
				data ={
				'status':1,
				'api_status':'',
				'message':'Successfully inserted.',
				}
			else:
				data ={
				'status':0,
				'api_status':'',
				'message':'You have already requested a return request for this product.',
				}
		else:
			data ={
			'status':0,
			'api_status':'',
			'message':'Product return only available after shipped the product',
			}
		return Response(data)

# Approve and Reject for return approval Processing and Declined...
class OrderReturnApprove(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		website_id = request.data['website_id']
		order_id = request.data['order_id']
		type_of_return_status = request.data['type_of_return_status'] #Processing/Decline
		find_return_request_data = EngageboostOrderReturnDetails.objects.using(company_db).filter(website_id=website_id,order_id=order_id)
		# OrderData['special_instruction'] =this->data['OrderList']['special_instruction'];
		if find_return_request_data.count()>0:
			EngageboostOrderReturnDetails.objects.using(company_db).filter(website_id=website_id,order_id=order_id).update(return_status=type_of_return_status)
			if type_of_return_status=='Processing':
				EngageboostOrdermaster.objects.using(company_db).filter(id=order_id,return_status='Pending').update(return_status='Processing')
				elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'return_status':'Processing'})
				EngageboostCustomerReturnStatus.objects.using(company_db).filter(id=order_id,customer_return_status='Return Initiated').update(customer_return_status='Return Confirmed')
			if type_of_return_status =='Declined':
				EngageboostOrdermaster.objects.using(company_db).filter(id=order_id,return_status='Pending').update(return_status='Declined')
				elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'return_status':'Declined'})
				EngageboostCustomerReturnStatus.objects.using(company_db).filter(id=order_id,customer_return_status='Return Initiated').update(customer_return_status='Return Rejected')
			data ={
				'status':1,
				'api_status':'',
				'message':'Successfully updated the return status.',
			}
		else:
			data ={
				'status':0,
				'api_status':'',
				'message':'Not allowed to update the return status.',
			}
		return Response(data)

#Cancellation = 1, Partial Cancellation=2, GRN Cancellation=3, Delete Cancellation=4
class ViewOrderReturn(generics.ListAPIView):
	def get(self, request, pk, format=None):
		rs_order = EngageboostOrdermaster.objects.filter(id=pk).first()
		order_data = ViewOrderSerializer(rs_order)
		order_data = order_data.data

		total_return_amount = 0.00
		for order_products in order_data['order_products']:
			if order_products['returns'] > 0:
				total_return_amount += float(order_products['returns']) * float(order_products['cost_price'])

		order_data['return_price'] = total_return_amount

		try:
			data = {
				"status":1,
				"api_status": 1,
				"data":order_data,
			}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in order update."}
		return Response(data)
	def put(self, request, pk, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		# ip_address=request.data['data']['ip_address']
		website_id = request.data['website_id']
		order_id = request.data['order_id']
		return_order_type = request.data['return_order_type']
		userId = request.data['userId']
		trent_picklist_id = request.data['trent_picklist_id']
		OrderProductArr = request.data['shipmentOrderProduct']
		returnType = request.data['returnType']
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		activityType = 1
		try:
			orderData = EngageboostOrdermaster.objects.using(company_db).filter(id=order_id).first()
			total_refund_quantity_check = 0
			total_quantity = 0
			count_more_return = 0; 
			for OrderProduct in OrderProductArr:
				total_quantity = total_quantity+int(OrderProduct['quantity'])
				shortage = OrderProduct['shortage'] if OrderProduct['shortage'] else 0
				returns = OrderProduct['returns'] if OrderProduct['returns'] else 0
				total_refund_quantity_check = total_refund_quantity_check+int(shortage)+int(returns)
				total_damaged = int(OrderProduct['damaged'])
				if(total_damaged > 0 and (total_damaged > int(OrderProduct['returns']))):
					count_more_return = 1

			if total_refund_quantity_check == 0:
				data = {
					'status':0,
					'api_status':'',
					'message':'All refund quantity is zero.'
				}
				return Response(data)
			elif count_more_return == 1:
				data = {
					'status':0,
					'api_status':'',
					'message':"You can't enter more damaged than return quantity."
				}
				return Response(data)
			else:
				for OrderProduct in OrderProductArr:
					quantity = int(OrderProduct['quantity'])
					damaged = int(OrderProduct['damaged'])
					if OrderProduct['returns']:
						returns = int(OrderProduct['returns'])
					else:
						returns = 0
					if OrderProduct['shortage']:
						shortage = int(OrderProduct['shortage'])
					else:
						shortage = 0
					return_warehouse_id = int(OrderProduct['return_warehouse_id'])
					warehouse_id = OrderProduct['warehouse_id']
					stock_return = quantity-shortage-damaged
					if damaged > 0 :
						order_return_details = {
							'order_id':order_id,
							'product_id':OrderProduct['product_id'],
							'return_type':'Damage',
							'quantity':damaged,
							# 'warehouse_id':return_warehouse_id,
							"created":now_utc
						}
						# print(order_return_details)
						EngageboostReturnDetails.objects.create(**order_return_details)
					elif damaged == 0 and returns > 0:
						order_return_details = {
							'order_id':order_id,
							'product_id':OrderProduct['product_id'],
							'return_type':'InStock',
							'quantity':returns,
							# 'warehouse_id':return_warehouse_id,
							"created":now_utc
						}
						# print(order_return_details)
						EngageboostReturnDetails.objects.create(**order_return_details)
						common.update_stock_all(OrderProduct['product_id'],return_warehouse_id,returns,"Refund","real",0,0,userId)

				if returnType == 'FR': 
					order_update = {
						'order_status': 5,
						'return_status':'Completed',
						'flag_order':1
					}
					elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'order_status':5, 'return_status':'Completed', 'flag_order':1})
				elif returnType == 'PR':
					order_update = {
						'order_status': 6,
						'return_status':"Completed"
					}
					elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'order_status':6, 'return_status':'Completed', 'flag_order':0})
				EngageboostOrdermaster.objects.filter(id=order_id).update(**order_update)
				succ_message = "You have successfully done return."
			data = {
				'status':1,
				'api_status':'',
				'message':succ_message
			}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in order update."}
		return Response(data)

class OrderReturnView(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		website_id = request.data['website_id']
		return_id = request.data['return_id']
		find_return_request_data = EngageboostOrderReturnDetails.objects.using(company_db).filter(website_id=website_id, id=return_id)
		if find_return_request_data.count()>0:
			find_return_request_data_get = EngageboostOrderReturnDetails.objects.using(company_db).get(website_id=website_id,id=return_id)	
			serializer_return_details = OrderReturnDetailsWithoutDepthSerializer(find_return_request_data_get)
			date=EngageboostGlobalSettings.objects.using(company_db).get(website_id=website_id)
			zone=EngageboostTimezones.objects.using(company_db).get(id=date.timezone_id)
			datetime = serializer_return_details.data['created'].replace('T',' ')
			data_time=datetime.replace('Z',' ')
			new_date = get_time(data_time,zone,date)
			
			
			order = EngageboostOrdermaster.objects.using(company_db).get(id=find_return_request_data_get.order.id)
			serializer = OrderMasterSerializer(order)
			merchant_order_status = serializer.data['order_status']
			check_from_merchant_order = EngageboostOrderMerchantOrderStatus.objects.using(company_db).filter(merchant_website_id=website_id,order_id=find_return_request_data_get.order.id)

			if check_from_merchant_order.count()>0:
				check_from_merchant_order_get = EngageboostOrderMerchantOrderStatus.objects.using(company_db).get(merchant_website_id=website_id,order_id=find_return_request_data_get.order.id)
				merchant_order_status = check_from_merchant_order_get.order_status
			product_arr=[]
			OrderProductsquery = EngageboostOrderProducts.objects.using(company_db).filter(order_id=find_return_request_data_get.order.id,merchant_website_id=website_id,merchant_product_id=find_return_request_data_get.product.id)
		
			serializer_product = OrderProductsSerializer(OrderProductsquery, many=True)
			timeline=EngageboostOrderActivity.objects.using(company_db).order_by('-id').filter(order_id=find_return_request_data_get.order.id)
			serializer_time=OrderActivitySerializer(timeline, many=True)
			
			activity=[]
			data ={
				'status':0,
				'api_status':[],
				'message':'Data Not Found',
				}
			for timelines in serializer_time.data:
				
				date=EngageboostGlobalSettings.objects.using(company_db).get(website_id=serializer.data['website_id'])
				zone=EngageboostTimezones.objects.using(company_db).get(id=date.timezone_id)
				time=timelines['activity_date']
				date_fetch=get_time(time,zone,date)

				d1={'activity_date':date_fetch,'activity_comments':timelines['activity_comments']}
				activity.append(d1)
			# product select for single row update
			for products in serializer_product.data:

				product_name = EngageboostProducts.objects.using(company_db).all().filter(id=products['merchant_product_id'])
				
				for productsset in product_name:
					
					d1={
						'product_id': productsset.id,
						'sku': productsset.sku,
						'product_name':productsset.name	
					}
					d2=products
					dict_data=dict(d2,**d1)
					product_arr.append(dict_data)

			if(serializer): 
				data ={
					'status':1,
					'api_status':serializer.data,
					'products':product_arr,
					'return_details':serializer_return_details.data,
					'activity':activity,
					'return_created_date':new_date,
					'merchant_order_status':merchant_order_status,
					'message':'Data found',
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
				'api_status':'',
				'message':'Data Not Found',
				}
			
		return Response(data)


class OrderReturnComplete(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		website_id = request.data['website_id']
		return_id = request.data['return_id']
		stock = request.data['stock']
		damaged = request.data['damaged']
		find_return_request_data = EngageboostOrderReturnDetails.objects.using(company_db).filter(website_id=website_id,id=return_id)		
		if find_return_request_data.count()>0:	
			find_return_request_data_get = EngageboostOrderReturnDetails.objects.using(company_db).get(website_id=website_id,id=return_id)
			product_details_from_order_products = EngageboostOrderProducts.objects.using(company_db).filter(order_id=find_return_request_data_get.order_id,merchant_product_id=find_return_request_data_get.product_id)
			if product_details_from_order_products.count()>0 and find_return_request_data_get.quantity<=(stock+damaged):
				product_details_from_order_products_get = EngageboostOrderProducts.objects.using(company_db).get(order_id=find_return_request_data_get.order_id,merchant_product_id=find_return_request_data_get.product_id)
				EngageboostOrderProducts.objects.using(company_db).filter(order_id=find_return_request_data_get.order_id,merchant_product_id=find_return_request_data_get.product_id).update(damaged=damaged,stock=stock)
			
				EngageboostOrderReturnDetails.objects.using(company_db).filter(website_id=website_id,id=return_id).update(return_status='Completed')
				if stock>0:
					value=EngageboostProductStocks.objects.using(company_db).get(warehouse_id=product_details_from_order_products_get.warehouse_id,product_id=find_return_request_data_get.product_id)
					real_stock=int(value.real_stock)+int(find_return_request_data_get.quantity)
					stock=int(value.stock)+int(find_return_request_data_get.quantity)
					#virtual_stock=int(value.virtual_stock)+int(productorder['quantity'])
					value=EngageboostProductStocks.objects.using(company_db).filter(warehouse_id=product_details_from_order_products_get.warehouse_id,product_id=find_return_request_data_get.product_id).update(real_stock=stock,stock=stock)
			data ={
				'status':1,
				'api_status':'',
				'message':'Data Updated Successfully',
				}
		else:
			data ={
				'status':0,
				'api_status':'',
				'message':'Data Not Found',
				}
			
		return Response(data)


# need to optimize the code..
class CancelOrderRefund(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		website_id = request.data['website_id']
		order_id = request.data['order_id']
		quantity = request.data['quantity']
		product_id = request.data['product_id']
		return_type = request.data['return_type']
		userId = request.data['userId']
		customer_id = request.data['customer_id']
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		activityType = 1
		OrderProductArr = EngageboostOrderProducts.objects.using(company_db).filter(order_id=order_id, grn_quantity__gte=0).all()
		try:
			if product_id > 0:
				OrderProductArr = OrderProductArr.filter(product_id=product_id)
			total_refund_quantity = 0;
			for OrderProduct in OrderProductArr:
				refund_quantity = OrderProduct.grn_quantity-OrderProduct.returns
				grn_quantity = OrderProduct.quantity-refund_quantity
				if(refund_quantity > 0):
					EngageboostOrderProducts.objects.filter(order_id=order_id).update(returns=refund_quantity,grn_quantity=grn_quantity)
					order_return_details = {
						'website_id': website_id,
						'order_id':order_id,
						'product_id':OrderProduct.product_id,
						'return_by_id':userId,
						'quantity':refund_quantity,
						'reason':"Edit Order after shipped",
						'return_status':'Authorized',
						"created":now_utc
					}
					EngageboostOrderReturnDetails.objects.create(**order_return_details)
					customer_return_details = {
						'customer_id': customer_id,
						'order_id':order_id,
						'product_id':OrderProduct.product_id,
						'customer_return_status':'Return Initiated',
						"created":now_utc
					}
					EngageboostCustomerReturnStatus.objects.create(**customer_return_details)
					total_refund_quantity = total_refund_quantity+1
			
			if total_refund_quantity > 0:
				if return_type=='FULL':
					order_update = {
						'order_status': 7,
						'return_note':"Order is Rescheduled",
						'flag_order':1
					}
				order_update.update({return_status:'Processing'})
				EngageboostOrdermaster.objects.filter(order_id=order_id).update(**order_update)
				activity_msg = "Order return process has been started";
				activity_details = common.save_order_activity(company_db,order_id,now_utc,7,activity_msg,userId,activityType)
			else:
				EngageboostOrdermaster.objects.filter(id=order_id).update(order_status=2, flag_order=1)
				activity_msg = "Order is Rescheduled and cancelled after edit";
				activity_details = common.save_order_activity(company_db,order_id,now_utc,order_status,activity_msg,userId,activityType)
		
			activity_details = common.save_order_activity(company_db,order_id,now_utc,2,"Order is Cancelled",userId,activityType)
			data={"status":1,"api_status":'1', "message": activity_msg}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
		return Response(data)

#Cancellation = 1, Partial Cancellation=2, GRN Cancellation=3, Delete Cancellation=4
def update_invoice_refund(order_id,product_id, refund_quantity=0, shortage_quantity=0):
	if order_id > 0 and product_id > 0 and refund_quantity>0:
		rs_invoice_data 	= EngageboostInvoiceProducts.objects.filter(order_id = order_id, product_id = product_id, quantity__gte = 0).first()
		all_invoice_data 	= InvoiceproductSerializer(rs_invoice_data)
		all_invoice_data 	= all_invoice_data.data
		rest_quantity  		= int(refund_quantity) + float(shortage_quantity)
		if all_invoice_data and all_invoice_data['id']> 0:
			rs_order_list = EngageboostOrdermaster.objects.filter(id = all_invoice_data['order_id']).first()

			shipping_cost 	= rs_order_list.shipping_cost
			tax_amount 		= rs_order_list.tax_amount
			cart_discount 	= rs_order_list.cart_discount

			if all_invoice_data['quantity'] > 0:
				if int(rest_quantity)  >= int(all_invoice_data['quantity']):
					updatequantity = all_invoice_data['quantity']
				else:
					updatequantity = rest_quantity
				
				shipped_save = {}
				shipped_save.update({
					"quantity":int(all_invoice_data["quantity"])-int(updatequantity)
				})
				EngageboostInvoiceProducts.objects.filter(id = all_invoice_data["id"]).update(**shipped_save)

				total_price = int(updatequantity)*float(all_invoice_data['price'])
				total_price = Decimal(total_price).quantize(Decimal('.00'))
				net_amount_shipped_order 	= float(rs_order_list.net_amount) - float(total_price)
				gross_amount_shipped_order 	= float(net_amount_shipped_order)+float(tax_amount)+float(shipping_cost)-float(cart_discount)

				shipped_save_order = {}
				shipped_save_order.update({"gross_amount":Decimal(gross_amount_shipped_order).quantize(Decimal('.00')),"net_amount":Decimal(net_amount_shipped_order).quantize(Decimal('.00'))})
				EngageboostInvoicemaster.objects.filter(id=all_invoice_data["invoice"]).update(**shipped_save_order)

# worked 25th jan 2020
class RefundOrders(generics.ListAPIView):
	def get(self, request, pk, format=None):
		rs_order = EngageboostOrdermaster.objects.filter(id=pk).first()
		order_data = ViewOrderSerializer(rs_order)
		order_data = order_data.data
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
	def put(self, request, pk, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		# ip_address=request.data['data']['ip_address']
		website_id = request.data['website_id']
		order_id = request.data['order_id']
		return_order_type = request.data['return_order_type']
		userId = request.data['userId']
		trent_picklist_id = int(request.data['trent_picklist_id'])
		OrderProductArr = request.data['shipmentOrderProduct']
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		activityType = 1
		try:
			# OrderProductArr = EngageboostOrderProducts.objects.using(company_db).filter(order_id=order_id).all()
			orderData = EngageboostOrdermaster.objects.using(company_db).filter(id=order_id).first()
			total_refund_quantity_check  = 0;
			count_more_return = 0; 
			for OrderProduct in OrderProductArr:
				shortage = OrderProduct['shortage']
				if shortage:
					shortage = int(shortage)
				else :
					shortage = 0
				
				total_refund_quantity_check = total_refund_quantity_check+shortage+int(OrderProduct['quantityrefund'])
				total_return_qty = int(OrderProduct['returns'])+int(OrderProduct['quantityrefund'])
				if(OrderProduct['quantityrefund'] > 0 and (OrderProduct['quantity'] < total_return_qty)):
					count_more_return = 1

			if total_refund_quantity_check == 0:
				data = {
					'status':0,
					'api_status':'',
					'message':'All refund quantity is zero.'
				}
				return Response(data)
			elif count_more_return == 1:
				data = {
					'status':0,
					'api_status':'',
					'message':"You can't return more than order quantity."
				}
				return Response(data)
			else:
				total_quantity = 0;
				return_message = "";
				if return_order_type == 1:
					return_message = request.data['return_note']
					if return_message == 'Others':
						return_message = request.data['return_others_reason']
				for OrderProduct in OrderProductArr:
					total_quantity = total_quantity + int(OrderProduct['quantity'])
					quantity = int(OrderProduct['quantity'])
					grn_quantity = int(OrderProduct['grn_quantity']) if OrderProduct['grn_quantity'] else 0
					shortage_quantity = int(OrderProduct['shortage']) if OrderProduct['shortage'] else 0
					returns = int(OrderProduct['returns'])
					refund_quantity = int(OrderProduct['quantityrefund'])
					warehouse_id 	= OrderProduct['warehouse_id']
					rest_quantity   = refund_quantity+shortage_quantity+returns+int(OrderProduct['deleted_quantity'])
					if rest_quantity > quantity:
						data = {
							'status':1,
							'api_status':'',
							'message':"You can't return more than order quantity."
						}
						return Response(data)

					if (grn_quantity > 0 and refund_quantity <= grn_quantity):
						refund_quantity = refund_quantity
						grn_quantity = int(grn_quantity-refund_quantity)
					elif (grn_quantity > 0 and refund_quantity >= grn_quantity):
						refund_quantity = grn_quantity
						grn_quantity = int(grn_quantity-refund_quantity)
					elif (refund_quantity > 0 and refund_quantity <= quantity):
						refund_quantity = refund_quantity
						grn_quantity = 0
				
					shipped_save = {
						'returns': refund_quantity,
						'grn_quantity':grn_quantity
					}
					# print("product_id", OrderProduct['product_id'])
					if(return_order_type == 2):
						if refund_quantity >0:
							EngageboostOrderProducts.objects.filter(product_id=OrderProduct['product_id'], order_id=order_id).update(**shipped_save)
					else:
						EngageboostOrderProducts.objects.filter(product_id=OrderProduct['product_id'], order_id=order_id).update(**shipped_save)
						
					if(return_order_type == 2):
						return_message = ""
						if "return_request_message" in OrderProduct:
							return_message = OrderProduct["return_request_message"]
						update_invoice_refund(order_id,OrderProduct['product_id'],refund_quantity,shortage_quantity);
						# update_shipment_quantity(shipment_id, order_id, OrderProduct['product_id'],OrderProduct['quantity'],refund_quantity);
					
					if refund_quantity > 0 :
						order_return_details = {
							'website_id': website_id,
							'order_id':order_id,
							'product_id':OrderProduct['product_id'],
							'return_by_id':userId,
							'quantity':refund_quantity,
							'reason':return_message,
							'return_status':'Authorized',
							"created":now_utc
						}
						# print(order_return_details)
						EngageboostOrderReturnDetails.objects.create(**order_return_details)
						customer_return_details = {
							'customer_id': request.data['customer_id'],
							'order_id':order_id,
							'product_id':OrderProduct['product_id'],
							'customer_return_status':'Return Initiated',
							"created":now_utc
						}
						EngageboostCustomerReturnStatus.objects.create(**customer_return_details)
						if return_order_type != 1:
							activity_msg = "Return Reason : "+return_message+" for product sku-"+OrderProduct["product"]['sku'];
							activity_details = common.save_order_activity(company_db,order_id,now_utc,7,activity_msg,userId,activityType)

				if (return_order_type == 1 or return_order_type == 4):
					order_update = {
						'order_status': 7,
						'return_status':'Authorized',
						'return_note': return_message,
						'flag_order':1
					}
					elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'order_status':7, 'return_status':'Authorized','return_note': return_message, 'flag_order':1})
					activity_msg = "Return Reason : "+return_message+" for order-"+request.data['custom_order_id']
					activity_details = common.save_order_activity(company_db,order_id,now_utc,7,activity_msg,userId,activityType)
					EngageboostOrdermaster.objects.filter(id=order_id).update(**order_update)
					# flag_full_refund = 1;
					# this->sendmail_order(order_id, 'No', 6);
					# this->sendmail_invoice(order_id);
					# this->send_sms(orderData, 6, orderData['OrderList']['delivery_phone'],1, orderData['OrderList']['customer_id']);   
					# this->send_sms_invoice(order_id,5);// sms for invoice
				else:
					order_update = {
						'order_status': 7,
						'return_status':"Authorized",
						'return_note':'',
						'flag_order':1
					}
					EngageboostOrdermaster.objects.filter(id=order_id).update(**order_update)
					#elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'order_status':7,'return_status':'Authorized','return_note': '', 'flag_order':1})
					update_order_and_order_products(order_id, return_order_type) # elastic update also takes place here...
					# flag_full_refund = 0;
					# this->sendmail_order(order_id, 'No', 115);
					# this->sendmail_invoice(order_id);
					# this->send_sms(orderData, 115, orderData['OrderList']['delivery_phone'],1,orderData['OrderList']['customer_id']);  // sms for invoice 
					# this->send_sms_invoice(order_id,5);
				succ_message = ''
				if(return_order_type == 1):
					succ_message = "Success : You have successfully initiate return the Order."
				else:
					succ_message = "Success : You have successfully initiate partial return the Order."
				data = {
					'status':1,
					'api_status':'',
					'message':succ_message
				}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in order update."}
		return Response(data)

#Cancellation = 1, Partial Cancellation=2, GRN Cancellation=3, Delete Cancellation=4

# =============================================

# def update_invoice_refund(order_id,product_id, refund_quantity=0, shortage_quantity=0):
	# this->InvoiceProduct->bindModel(array('belongsTo'=>array(
	# 	'OrderList' =>
	# 		array('className'    => 'OrderList',
	# 		'conditions'   => '',
	# 		'order'        => '',
	# 		'dependent'    =>  false,
	# 		'foreignKey'   => 'order_id',
	# 		'fields'	   => 'OrderList.id,OrderList.shipping_cost,OrderList.tax_amount,cart_discount'
	# 	),
	# 	'InvoiceMaster' =>
	# 		array('className'    => 'InvoiceMaster',
	# 		'conditions'   => '',
	# 		'order'        => '',
	# 		'dependent'    =>  false,
	# 		'foreignKey'   => 'invoice_id',
	# 		'fields'	   => 'InvoiceMaster.id,InvoiceMaster.net_amount'
	# 		)
	# 	)
	# ));
	# if(order_id > 0 && product_id > 0 ) {
	# 	all_invoiced_con    = "InvoiceProduct.order_id='".order_id."' AND InvoiceProduct.product_id='".product_id."' AND InvoiceProduct.quantity > 0";
	# 	all_invoice_data    = this->InvoiceProduct->find("first",array("conditions"=>all_invoiced_con));
	# 	//this->pr_exit(all_invoice_data);
	# 	rest_quantity  = refund_quantity + shortage_quantity;
	# 	if(!empty(all_invoice_data) && (all_invoice_data['InvoiceMaster']['id'] > 0)) {
	# 		shipping_cost = all_invoice_data['OrderList']['shipping_cost'];
	# 		tax_amount = all_invoice_data['OrderList']['tax_amount'];
	# 		cart_discount = all_invoice_data['OrderList']['cart_discount'];
	# 		if(all_invoice_data['InvoiceProduct']['quantity'] > 0) {
	# 			if(rest_quantity  >= all_invoice_data['InvoiceProduct']['quantity']) {
	# 				updatequantity = all_invoice_data['InvoiceProduct']['quantity'];
	# 			} else {
	# 				updatequantity = rest_quantity;
	# 			}
	# 			shipped_save = array();
	# 			shipped_save['InvoiceProduct']['id'] = all_invoice_data['InvoiceProduct']['id'];
	# 			shipped_save['InvoiceProduct']['quantity'] = all_invoice_data['InvoiceProduct']['quantity'] - updatequantity ;
	# 			//this->pr_exit(shipped_save);
	# 			this->InvoiceProduct->id = all_invoice_data['InvoiceProduct']['id'];
	# 			this->InvoiceProduct->save(shipped_save['InvoiceProduct']);
	# 			total_price = updatequantity*all_invoice_data['InvoiceProduct']['price'];
	# 			net_amount_shipped_order 	= all_invoice_data['InvoiceMaster']['net_amount'] - total_price;
	# 			gross_amount_shipped_order = (net_amount_shipped_order+tax_amount+shipping_cost)-cart_discount;
	# 			shipped_save_order = array();
	# 			shipped_save_order['InvoiceMaster']['id'] = all_invoice_data['InvoiceMaster']['id'];
	# 			shipped_save_order['InvoiceMaster']['gross_amount'] = gross_amount_shipped_order;
	# 			shipped_save_order['InvoiceMaster']['net_amount']   = net_amount_shipped_order;
	# 			this->InvoiceMaster->id = all_invoice_data['InvoiceMaster']['id'];
	# 			//this->pr_exit(shipped_save_order);
	# 			this->InvoiceMaster->save(shipped_save_order['InvoiceMaster']);
	# 		}
	# 	}
	# }

#Cancellation = 1, Partial Cancellation=2, GRN Cancellation=3, Delete Cancellation=4
def update_shipment_quantity(shipment_id, order_id, product_id, quantity=0, returns=0):
	if shipment_id > 0 and order_id > 0 and product_id > 0:
		order_list = EngageboostShipmentOrders.objects.filter(order_id=order_id, shipment_id=shipment_id).first()
		# if((order_list.shipment_status == 'Picking') && returns > 0) :
		# 	this->ShipmentOrderProduct->query("UPDATE engageboost_shipment_order_products SET quantity=quantity-returns WHERE shipment_id=shipment_id AND order_id=order_id AND product_id=product_id AND quantity >= returns AND quantity > 0");
		# 	//this->OrderProduct->query("UPDATE engageboost_order_products SET grn_quantity=grn_quantity-returns WHERE order_id=order_id and product_id=product_id and grn_quantity>0");
		# elif(in_array(shipment_status,array('Ready to Ship','Dispatched','Shipped','Completed'))  && returns > 0):
		# 	this->ShipmentOrderProduct->query("UPDATE engageboost_shipment_order_products SET grn_quantity=grn_quantity-returns, returns=returns+returns WHERE shipment_id=shipment_id AND order_id=order_id AND product_id=product_id AND grn_quantity >= returns AND grn_quantity > 0");
		# 	//this->OrderProduct->query("UPDATE engageboost_order_products SET returns=returns+returns WHERE order_id=order_id and product_id=product_id");

# update Order list and order product after return....
def update_order_and_order_products(order_id, return_order_type='GRN Cancellation'):
	if order_id > 0:
		rs_oder = EngageboostOrdermaster.objects.filter(id=order_id).first()
		order_data = OrderAndOrderProductSerializer(rs_oder)
		all_OrderProduct = order_data.data
		net_amount      = 0
		gross_amount    = 0
		tax_amount      = 0
		gross_discount_amount = 0
		cart_discount  	= rs_oder.cart_discount
		shipping_cost 	= rs_oder.shipping_cost
		pay_wallet_amount = rs_oder.pay_wallet_amount
		for products in all_OrderProduct['order_products']:
			quantity = products['quantity']
			if int(products['grn_quantity']) > 0:
				quantity = int(products['grn_quantity'])
			else:
				quantity = int(products['quantity'])-(int(products['deleted_quantity'])+int(products['returns'])+int(products['shortage']))
			net_amount = float(net_amount) + (float(products['product_price'])*float(quantity))
			tax_amount = float(tax_amount) + (float(products['product_tax_price'])*int(quantity))
			gross_discount_amount = float(gross_discount_amount) + (float(products['product_discount_price'])*int(quantity))
		if rs_oder.applied_coupon and cart_discount > 0:
			# cart_discount = grn_cart_discount(OrderData['applied_coupon'], all_OrderProduct, return_order_type, website_id,OrderData['customer_id'])
			cart_discount = rs_oder.cart_discount
		else:
			cart_discount = rs_oder.cart_discount
		gross_amount = float(net_amount)+float(tax_amount)+float(shipping_cost)-float(cart_discount)
		# Wallet balance update start...
		if gross_amount>pay_wallet_amount:
			gross_amount = float(gross_amount-pay_wallet_amount)
		else:
			refund_wallet= float(pay_wallet_amount-gross_amount)
			# common.addCustomerLoyaltypoints()
			pay_wallet_amount = gross_amount
		# Wallet balance update end..

		# # end Shipping cost calculation for return product...
		shipped_save_order = {}
		shipped_save_order = {
			"net_amount":net_amount,
			"net_amount_base":net_amount,
			"tax_amount":tax_amount,
			"gross_amount":gross_amount,
			"gross_amount_base":gross_amount,
			"cart_discount":cart_discount,
			"gross_discount_amount":gross_discount_amount,
			"gross_discount_amount_base":gross_discount_amount,
			"pay_wallet_amount":pay_wallet_amount
		}
		EngageboostOrdermaster.objects.filter(id=order_id).update(**shipped_save_order)
		common.save_data_to_elastic(order_id,'EngageboostOrdermaster')

def get_information_shipping_admin(country_id='99',state_id=0, order_amt=0, website_id=0):
	free_shipping_min_amount = 0
	# conditions = "ShippingSetting.website_id='".website_id."' AND ShippingSetting.status='Yes' AND FIND_IN_SET('".country_id."', ShippingSetting.country_ids) AND ShippingSetting.isblocked='n'";
	# this->ShippingSetting->bindModel(array('belongsTo'=>array(
	# 	'ShippingMethod' => array('className' => 'ShippingMethod', 'conditions' => '', 'order' => '', 'dependent' =>  false, 'foreignKey'   => 'shipping_method_id', 'fields' => '')
	# )));
	# shipping_methods_website = this->ShippingSetting->find("all",array('conditions'=>conditions,'order'=>'ShippingMethod.id asc'));
	# //this->pr_exit(shipping_methods_website);
	# if(!empty(website_id)){
	# 	weightUnitCon = array('GlobalSetting.website_id' => website_id,'GlobalSetting.isblocked'=>'n','GlobalSetting.isdeleted'=>'n');
	# 	findWeightUnit = this->GlobalSetting->find('first', array('fields' => array('GlobalSetting.weight_unit', 'GlobalSetting.is_global_shipping_app', 'GlobalSetting.shipping_charge' , 'GlobalSetting.min_order_amount'), 'conditions' => weightUnitCon));
	# 	weightUnit    = findWeightUnit['GlobalSetting']['weight_unit'];
	# 	global_shipping   = findWeightUnit['GlobalSetting']['is_global_shipping_app'];
	# 	global_shipping_amount = findWeightUnit['GlobalSetting']['shipping_charge'];
	# 	min_order_amount   = findWeightUnit['GlobalSetting']['min_order_amount'];
	# }
	# foreach(shipping_methods_website as k=>v){
	# if(v['ShippingSetting']['shipping_method_id'] == 6){
	# 	free_shipping_min_amount = v['ShippingSetting']['minimum_order_amount'];
	# }
	# if(v['ShippingSetting']['shipping_method_id'] == 4){
	# 	flat_rate = v['ShippingSetting']['flat_price'];
	# }
	# }
	# if(order_amt > min_order_amount){
	# 	if(order_amt >= free_shipping_min_amount){
	# 		shipping_price = 0;
	# 		shipping_method = "Free Shipping";
	# 		shipping_message = "As your order is above Rs. ".number_format(free_shipping_min_amount,2)." you will not be charged any shipping fees.";
	# 	}else{
	# 		shipping_price = flat_rate;
	# 		shipping_method = "Flat Rate";
	# 		shipping_message="As your order is under Rs. ".number_format(free_shipping_min_amount,2).", a nominal shipping fee has been charged.
	# 		To save Rs. ".number_format(flat_rate,2)." of Delivery charges, please add items worth Rs. ".number_format((free_shipping_min_amount-order_amt),2). " or more and qualify for free home delivery.";
	# 	}
	# }else{
	# 	shipping_message  = "min order should be " .min_order_amount;
	# 	shipping_price = flat_rate;
	# 	shipping_method = "Flat Rate";
	# }

	# return_data = {
	# 	'shipping_cost'		: shipping_price,
	# 	'shipping_method_id': shipping_method,
	# 	'min_order_amount'	: min_order_amount,
	# 	'free_shipping_min_amount': free_shipping_min_amount,
	# 	'shipping_message'	: shipping_message,
	# 	'order_amount'		: order_amt
	# }

	# return return_data;

# def grn_cart_discount(coupon_code, order_products, strfrom='GRN Cancellation', website_id=None,customer_id=None, custom_order_id=None,points_disc=None):
def grn_cart_discount(cartdetails,total_product_refund, website_id=None):
	if website_id is None:
		website_id = 1
	order_id 		= cartdetails["id"]
	user_group_id 	= None
	warehouse_id 	= cartdetails['assign_wh']
	user_id 		= cartdetails['customer']
	order_total 	= cartdetails['gross_amount']
	# order_total = float(order_amount) - float(total_product_refund)
	#********APPLY COUPON CODE********#
	coupon_details = {}
	if cartdetails and cartdetails['applied_coupon'] is not None:
	# if cartdetails and cartdetails['applied_coupon'] !="":
		coupon_code = cartdetails['applied_coupon']
		discount_array_coupon=discount.generate_discount_conditions_coupon(website_id,user_group_id,coupon_code)
		if discount_array_coupon and discount_array_coupon[0]["name"]!="invalid":
			if discount_array_coupon[0]["disc_type"]!=3:
				if discount_array_coupon[0]["coupon_type"]==2:
					cartdetails = discount.genrate_new_prodcut_with_discount_coupon(user_id,cartdetails,discount_array_coupon,order_total)
				else:
					if discount_array_coupon[0]["used_coupon"]==0:
						cartdetails = discount.genrate_new_prodcut_with_discount_coupon(user_id,cartdetails,discount_array_coupon,order_total)
			else:
				order_total = float(order_total) - float(total_product_refund)
				if discount_array_coupon[0]["coupon_type"]==2:
					coupon_details = discount.genrate_new_prodcut_with_discount_coupon_order_total(user_id,cartdetails,discount_array_coupon,order_total)
				else:
					if discount_array_coupon[0]["used_coupon"]==0:
						coupon_details = discount.genrate_new_prodcut_with_discount_coupon_order_total(user_id,cartdetails,discount_array_coupon,order_total)
	else:
		coupon_details = ({'coupon_discount_amount':0})
	return coupon_details