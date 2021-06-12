from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics,viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime, timedelta
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from webservices.views import loginview
from webservices.models import *
from webservices.serializers import *
import datetime,time
from rest_framework.authtoken.models import Token
import base64
import sys,math
import traceback

@csrf_exempt
def DriverLogin(request):
	requestdata = JSONParser().parse(request)
	user_mail  = requestdata['username']
	user_passw  = requestdata['password']
	# ip          = requestdata['ip_address']
	role_id = 1
	if "role_id" in requestdata:
		role_id = requestdata["role_id"]

	User = EngageboostUsers.objects.filter( Q(username=user_mail) | Q(email=user_mail)).filter(isdeleted='n', isblocked='n',role_id=role_id).first()
	cnt = 0
	if User:
		cnt = 1

	if cnt<=0:
		data = {
			'status':0,
			'message': 'Username / password mismatch.'
		}
		return JsonResponse(data)
	else:
		password_check  = User.check_password(user_passw)
		token, created  = Token.objects.get_or_create(user=User)
		token_data      = token.key

		if password_check==True:
			now = datetime.datetime.now()
			today = now.date()
			now_utc     = datetime.datetime.now(datetime.timezone.utc).astimezone()
			EngageboostUsers.objects.filter(email=user_mail).update(last_login=now_utc)

			rs_vehicledetails = EngageboostDriverVeichleMap.objects.filter(user_id=User.id, delivery_date=today).first()
			vehicledetails = VehicleDtailsSerializer(rs_vehicledetails)
			vehicledetails = vehicledetails.data
			if len(vehicledetails['veichele_details'])>0:
				vehicle_id 		= vehicledetails['veichele_details']['id']
				vehicle_number 	= vehicledetails['veichele_details']['vehicle_number']
			else:
				vehicle_id = 0
				vehicle_number = ''
			employee_name = User.first_name
			message="Hello "+employee_name+" ,"+vehicle_number+" has been assign to you."

			# Company Details
			defaultWebsite = EngageboostCompanyWebsites.objects.filter(id=User.website_id).first()

			userdata={
				'first_name':User.first_name,                    
				'last_name':User.last_name,
				'token' : token_data,
				'user_id': User.id,
				'email':User.email,
				"id":User.id,   
				"vehicle_id":vehicle_id,
				"vehicle_number":vehicle_number,
				"email":User.email,
				"username":User.username,
				"employee_name":User.first_name + " " + User.last_name,
				"company_id":User.company_id,
				"website_id":User.website_id,
				"defaultwebsite":defaultWebsite.websitename,
				"defaultcompany":defaultWebsite.company_name,
				"defaultcurrency":"INR"
			}

			data = {
				'status':1,
				'msg':'success',
				'user_data':userdata ,
			}
		else:
			data = {
					'status':0,
					'message': 'Username / password mismatch.'
				}
		return JsonResponse(data)

class list_order_for_delivery(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = request.data
		website_id = requestdata['website_id']
		company_id = requestdata['company_id']
		driver_id = requestdata['driver_id']
		now = datetime.datetime.now()
		today = now.date()
		now_utc     = datetime.datetime.now(datetime.timezone.utc).astimezone()
		warehouse_lat_long 		= get_latitude_longitude()
		warehouse_lat_long_str 	= warehouse_lat_long.split(',')
		warehouse_latitude 		= warehouse_lat_long_str[0]
		warehouse_longitude 	= warehouse_lat_long_str[1]

		returndata={}		
		data = {}
		try:
			if driver_id:		
				rs_orderdetails = EngageboostDriverVeichleMap.objects.filter(user_id=driver_id, delivery_date=today).all()
				# delivery_order_derails = DeliveryOrderSerializer(rs_orderdetails, many=True)
				delivery_order_derails = DeliveryOrderListSerializer(rs_orderdetails, many=True)
				delivery_order_derails = delivery_order_derails.data
				list_order_ids = []
				rs_delivery_order_ids = DeliveryOrdersSerializer(rs_orderdetails, many=True)
				if len(rs_delivery_order_ids.data)>0:
					for delivery_order in rs_delivery_order_ids.data:						
						if delivery_order['DeliveryPlanOrder'] and len(delivery_order['DeliveryPlanOrder'])>0:
							for order_id_data in delivery_order['DeliveryPlanOrder']:
								list_order_ids.append(order_id_data['order_id'])

				    # print(list_order_ids)
				rs_time_slot = EngageboostOrdermaster.objects.filter(id__in=list_order_ids).values_list('time_slot_id', flat=True).distinct()
				try:
					if len(rs_orderdetails)>0:
						dd = {}
						for x in range(len(rs_time_slot)):							
							timeslotdata=[]
							for delivery_orderdetails in delivery_order_derails:
								for DeliveryPlanOrder in delivery_orderdetails['DeliveryPlanOrder']:
									for orderdetails in DeliveryPlanOrder["OrderList"]:
										# $currencyformat = $orderdetails[$i]['OrderList']['currency_code'];
										currencyformat = "INR"
										paid_amount = orderdetails['paid_amount']
										gross_amount = orderdetails['gross_amount']
										net_amount = orderdetails['net_amount']
										order_status = orderdetails['order_status']
										distance = DeliveryPlanOrder['distance']
										time = DeliveryPlanOrder['time']
										listings = {}
										if str(rs_time_slot[x]) in orderdetails['time_slot_id']:
											listings={
												"id":orderdetails['id'],
												"custom_order_id":orderdetails['custom_order_id'],
												"time_slot_date":orderdetails['time_slot_date'],
												"time_slot_id":orderdetails['time_slot_id'],
												"billing_name":orderdetails['billing_name'],
												"billing_email_address":orderdetails['billing_email_address'],
												"billing_phone":orderdetails['billing_phone'],
												"billing_street_address":orderdetails['billing_street_address'],
												"billing_street_address1":orderdetails['billing_street_address1'],
												"billing_city":orderdetails['billing_city'],
												"billing_postcode":orderdetails['billing_postcode'],
												"billing_state":orderdetails['billing_state'],
												"billing_country_name":orderdetails['billing_country_name'],
												"delivery_name":orderdetails['delivery_name'],
												"delivery_email_address":orderdetails['delivery_email_address'],
												"delivery_phone":orderdetails['delivery_phone'],
												"delivery_street_address":orderdetails['delivery_street_address'],
												"delivery_street_address1":orderdetails['delivery_street_address1'],
												"delivery_city":orderdetails['delivery_city'],
												"delivery_postcode":orderdetails['delivery_postcode'],
												"delivery_state":orderdetails['delivery_state'],
												"delivery_country":orderdetails['delivery_country'],
												"driver_id":delivery_orderdetails['user_id'],
												"driver_name":"",
												"warehouse_id":orderdetails['assign_wh'],
												"warehouse_name":"",
												"payment_method_name":orderdetails['payment_method_name'],
												"currency":currencyformat,
												"gross_amount":gross_amount,
												"paid_amount":paid_amount,
												"net_amount":net_amount,
												"order_status":order_status,
												"sort_by_distanc":"",
												"latitude":"22.5427604", # orderdetails["CustomerBillingAddress"]['lat_val'],
												"longitude":"88.3859595", # orderdetails["CustomerBillingAddress"]['long_val'],
												"distance":distance,
												"time":time,
												"virtual_vechile_id":DeliveryPlanOrder['virtual_vechile_id'],
												"delivery_date":delivery_orderdetails['delivery_date'],
											}
											timeslotdata.append(listings)
							dd.update({rs_time_slot[x]:timeslotdata})
						# returndata.append(dd)
						returndata = dd
						
						data = {
							"ack":1,
							"msg":"success",
							"latitude":warehouse_latitude,
							"longitude":warehouse_longitude,
							"response":returndata
						}
					else:
						data = {
							"ack":0,
							"latitude":warehouse_latitude,
							"longitude":warehouse_longitude,
							"msg":"No data found.",
							"response":returndata
						}
				except Exception as error:
					trace_back = sys.exc_info()[2]
					line = trace_back.tb_lineno
					data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}

		return Response(data)

def get_latitude_longitude():
	# origin = '18.5101116,73.8777968'
	origin = '22.5135,88.4119'
	return origin

class driver_checkin_time(generics.ListAPIView):
	def post(self, request, format=None):
		website_id = 1
		company_id = 1
		requestdata = request.data
	
		driver_id 			= requestdata['driver_id']
		device_id 			= requestdata['device_id']
		checkin_kilometer 	= requestdata['checkin_kilometer']

		driverArr = {}
		try:
			if driver_id:
				now = datetime.datetime.now()
				today = now.date()
				now_utc     = datetime.datetime.now(datetime.timezone.utc).astimezone()
				rs_vehicledetails = EngageboostDriverVeichleMap.objects.filter(user_id=driver_id, delivery_date=today).first()
				vehicledetails = VehicleDtailsSerializer(rs_vehicledetails)
				vehicledetails = vehicledetails.data
				if vehicledetails:
					vehicle_id 		= vehicledetails['veichele_details']['id']
					vehicle_number 	= vehicledetails['veichele_details']['vehicle_number']
				else:
					vehicle_id = 0
					vehicle_number = ''
				
				checkin_date = today
				checkin_time = now_utc
				driverArr = {
					# "company_id":company_id,
					"website_id":website_id,
					"vehicle_id":vehicle_id,
					"driver_id":driver_id,
					"device_id":device_id,
					"checkin_date":checkin_date,
					"checkin_time":checkin_time,
					"checkin_kilometer":checkin_kilometer
				}
				EngageboostDriverLoginDetails.objects.create(**driverArr)
				status = 1
				msg = "Success"
			else:
				ack = 0
				msg = 'Please provide all details.'
			data = {
				"ack":status,
				"msg":msg
			}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}
		return Response(data)

class driver_checkout_time(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = request.data
		driver_id 			= requestdata['driver_id']
		checkout_kilometer 	= requestdata['checkout_kilometer']

		driverArr = {}
		driverArrCondition = {}
		try:
			if driver_id:
				now = datetime.datetime.now()
				today = now.date()
				now_utc     = datetime.datetime.now(datetime.timezone.utc).astimezone()
				
				checkin_date 	= today
				checkout_time 	= now_utc

				rs_driver_login = EngageboostDriverLoginDetails.objects.filter(driver_id=driver_id).last()
				DriverLoginDetail = DriverLoginDetailsSerializer(rs_driver_login)
				DriverLoginDetail = DriverLoginDetail.data
				# print(DriverLoginDetail)
				device_id=''
				if DriverLoginDetail:
					driverArr = {
						"checkout_time":checkout_time,
						# "device_id":int(device_id),
						"checkout_kilometer":checkout_kilometer
					}
					EngageboostDriverLoginDetails.objects.filter(id=DriverLoginDetail['id']).update(**driverArr)
					status = 1
					msg = 'Success.'
			else:
				status = 0
				msg = 'Please provide all details.'
			
			data = {
				"ack":status,
				"msg":msg
			}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}

		return Response(data)

class delivery_attempt(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = request.data
		userdata = request.user
		logged_user_id = userdata.id
		website_id = 1
		company_id = 1
		now = datetime.datetime.now()
		today = now.date()
		now_utc     = datetime.datetime.now(datetime.timezone.utc).astimezone()

		today_time 	= now_utc
		shipment_id = "12345"
		if "shipment_id" in requestdata:
			shipment_id 				= requestdata["shipment_id"]

		order_id 					= requestdata["order_id"]
		# delivery_attempted_date 	= requestdata["delivery_attempted_date "]
		additional_note 			= requestdata["additional_note"]
		# images 						= requestdata["images"]
		attempted_type = ""
		if "attempted_type" in requestdata:
			attempted_type 				= requestdata["attempted_type"]
		reason = ""
		if "reason" in requestdata:
			reason 						= requestdata["reason"]

		# logged_user_name 				= requestdata["logged_user_name"]

		delivery_attempted_date = now_utc
		show_delivery_date = delivery_attempted_date
		try:
			if order_id:
				if "delivery_attempted_date" in requestdata:
					delivery_attempted_date 	= requestdata["delivery_attempted_date "]

				additional_note 			= additional_note
				save_arr = {
					"shipment_id":shipment_id,
					"order_id":order_id,
					"delivery_attempted_date":delivery_attempted_date,
					"additional_note":additional_note,
					"attempted_type":attempted_type,
					"reason":reason
				}
				rs_attempt = EnagageboostAttemptedDeliveryDetails.objects.create(**save_arr)
				insert_id = rs_attempt.id
				logged_user_name = "Admin"

				if attempted_type == 'attempt':
					msg = "Deivery attempt on " + str(show_delivery_date) +" By " +logged_user_name +"<br><strong>Reason:: "+additional_note+"</strong>"
				else:
					msg = "Order delivered and completed on "+str(show_delivery_date)+" By "+logged_user_name +"<br><strong>Reason:: "+additional_note+"</strong>"
				
				# last_id = common.save_order_activity(order_id,now_utc,7,msg,1)

				shipment_note = {
					"notes":msg,
					"order_id":order_id,
					"note_type":1,
					"isdeleted":'n',
					"isblocked":'n'
				}
				print(shipment_note)
				# EngageboostOrderNotes.objects.create(**shipment_note)
		# 		//End Order Activity And Note

		# 		if($last_id>0){
		# 			$this->upload_delivery_image($last_id,$images,$order_id,$attempted_type);
		# 		}
				status = 1
				msg = 'success'
			else:
				status = 1
				msg = 'No orders available.'

			data = {
				"ack":status,
				"msg":msg
			}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}

		return Response(data)

class delivery_order_details(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = request.data
		website_id = 1
		order_id = requestdata['order_id']
		data = {}
		returnArray = {}
		try:
			if order_id:
				rs_order = EngageboostOrdermaster.objects.filter(id=order_id).first()
				order_data = DeliveryOrderDetailsSerializer(rs_order)
				order_data = order_data.data
				# print(json.dumps(order_data))
				showcurrency = " <span class='WebRupee rupees'>&#x20B9;</span>"
				if order_data:
					currencyformat = order_data['currency_code']
					if currencyformat == 'INR':
						showcurrency = " <span class='WebRupee rupees'>&#x20B9;</span>"

					order_status_label = ''
					order_status = order_data['order_status']
					buy_status = order_data['buy_status']
					# order_status_label = get_order_status($order_status,$buy_status)
					order_status_label = "Shipped"

					total_items = len(order_data['order_products'])
					time_slot= order_data['time_slot_id']

					latitude="22.5427604"
					longitude="88.3859595"
					if order_data['address_book_id']:
						rs = EngageboostCustomersAddressBook.objects.filter(id = order_data['address_book_id']).first()
						if rs and float(rs.lat_val)>0:
							latitude = rs.lat_val
						if rs and float(rs.long_val)>0:
							longitude = rs.long_val
					data = {
						"master":{
							"order_status_label":order_status_label,
							"time_slot":time_slot,
							"time_slot_id":order_data['time_slot_id'],
							"custom_order_id":order_data['custom_order_id'],
							"created_date":order_data['created'],
							"id":order_data['id'],
							"website_id":order_data['website_id'],
							"company_id":order_data['company_id'],
							"zone_id":order_data['zone_id'],
							"sort_by_distance":order_data['sort_by_distance'],
							"latitude":latitude,
							"longitude":longitude,
							"special_instruction":order_data['custom_msg'],
							"total_items":total_items,
							"payment_method_name":order_data['payment_method_name'],
							"shipping_method_id":order_data['shipping_method_id'],
							"sort_by_distance":order_data['sort_by_distance'],
							"currency":showcurrency,
							"order_status":order_data['order_status'],

						},
						"Customer":{
							"order_status":order_data['order_status'],
							"customer_id":order_data['customer'],
							"billing_name":order_data['billing_name'],
							"billing_company":order_data['billing_company'],
							"billing_email_address":order_data['billing_email_address'],
							"billing_street_address":order_data['billing_street_address'],
							"billing_street_address1":order_data['billing_street_address1'],
							"billing_city":order_data['billing_city'],
							"billing_postcode":order_data['billing_postcode'],
							"billing_state":order_data['billing_state'],
							"billing_country":order_data['billing_country'],
							"billing_phone":order_data['billing_phone'],
							"delivery_name":order_data['delivery_name'],
							"delivery_company":order_data['delivery_company'],
							"delivery_email_address":order_data['delivery_email_address'],
							"delivery_street_address":order_data['delivery_street_address'],
							"delivery_street_address1":order_data['delivery_street_address1'],
							"delivery_city":order_data['delivery_city'],
							"delivery_postcode":order_data['delivery_postcode'],
							"delivery_state":order_data['delivery_state'],
							"delivery_country":order_data['delivery_country'],
							"delivery_phone":order_data['delivery_phone'],
						}
					}
					arrayProduct = {}
					counter = 0
					total_saved = 0
					product_list_arr = []
					for orderDataList in order_data['order_products']:
						is_shortage = 'No'
						if int(orderDataList['shortage'])>0 or int(orderDataList['returns'])>0 or int(orderDataList['deleted_quantity'])>0:
							is_shortage='yes'
						product_list = {}
						product_image = ""
						image_path = ""
						if len(orderDataList['product']['product_images'])>0:
							
							for productimage in orderDataList['product']['product_images']:
								if productimage['is_cover']==1:
									product_image = productimage['img']
									image_path = productimage['link']
								else:
									product_image = productimage['img']
									image_path = productimage['link']
							
							orderDataList['product'].pop("product_images")
						total_quantity=int(orderDataList['quantity'])-int(orderDataList['deleted_quantity'])-int(orderDataList['shortage'])-int(orderDataList['returns'])
						total_saved=float(total_saved) + (float(orderDataList['product_discount_price'])*int(total_quantity))
						product_list = {
							"id":orderDataList['id'],
							"order_id":order_id,
							"product_id":orderDataList["product"]['id'],
							"product_image":product_image,
							"product_image_path":image_path,
							"product_name":orderDataList['product']['name'],
							"product_description":orderDataList['product']['description'],
							"product_default_price":orderDataList['product']['default_price'],
							"product_price":orderDataList['product_price'],
							"product_discount_price":orderDataList['product_discount_price'],
							"product_excise_duty":orderDataList['product_excise_duty'],
							"product_tax_price":orderDataList['product_tax_price'],
							"product_tax_name":orderDataList['tax_name'],
							"warehouse_id":orderDataList['warehouse_id'],
							"quantity":total_quantity,
							"is_shortage":is_shortage,
						}
						product_list_arr.append(product_list)
					data.update({"ProductList":product_list_arr})
					total_saved= float(total_saved)+float(order_data['cart_discount'])
					OrderSummary = {
						"sub_total":order_data['gross_amount'],
						"delivery_charges":order_data['shipping_cost'],
						"promo_code":order_data['applied_coupon'],
						# "referal_code":order_data['referal_code'],
						# "loyality_point":order_data['loyality_point'],
						"total_saved":total_saved,
						"total_paid":order_data['gross_amount'],
						"net_amount":order_data['net_amount']
					}
					data.update({"OrderSummary":OrderSummary})
					status = 1
					msg='Success'
				else:
					status=0
					msg='No such details'
			else:
				status=0
				msg='Provide both website id and order id'
			data = {
				"details":data,
				"ack":status,
				"msg":msg
			}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}

		return Response(data)

def delivery_order_derails_return(order_id):
	try:
		if order_id:
			rs_order = EngageboostOrdermaster.objects.filter(id=order_id).first()
			order_data = DeliveryOrderDetailsSerializer(rs_order)
			order_data = order_data.data
			# print(order_data)
			try:
				if order_data:
					currencyformat = order_data['currency_code']
					showcurrency = " <span class='WebRupee rupees'>&#x20B9;</span>"
					if currencyformat == 'INR':
						showcurrency = " <span class='WebRupee rupees'>&#x20B9;</span>"

					order_status_label = ''
					order_status = order_data['order_status']
					buy_status = order_data['buy_status']
					# order_status_label = get_order_status($order_status,$buy_status)
					order_status_label = "Shipped"

					total_items = len(order_data['order_products'])
					time_slot= order_data['time_slot_id']

					latitude="22.5427604"
					longitude="88.3859595"
					if order_data['address_book_id']:
						rs = EngageboostCustomersAddressBook.objects.filter(id = order_data['address_book_id']).first()
						if rs and float(rs.lat_val)>0:
							latitude = rs.lat_val
						if rs and float(rs.long_val)>0:
							longitude = rs.long_val

					data = {
						"master":{
							"order_status_label":order_status_label,
							"time_slot":time_slot,
							"time_slot_id":order_data['time_slot_id'],
							"custom_order_id":order_data['custom_order_id'],
							"created_date":order_data['created'],
							"id":order_data['id'],
							"website_id":order_data['website_id'],
							"company_id":order_data['company_id'],
							"zone_id":order_data['zone_id'],
							"sort_by_distance":order_data['sort_by_distance'],
							"latitude":latitude,
							"longitude":longitude,
							"special_instruction":order_data['custom_msg'],
							"total_items":total_items,
							"payment_method_name":order_data['payment_method_name'],
							"shipping_method_id":order_data['shipping_method_id'],
							"sort_by_distance":order_data['sort_by_distance'],
							"currency":showcurrency,
							"order_status":order_data['order_status'],

						},
						"Customer":{
							"order_status":order_data['order_status'],
							"customer_id":order_data['customer'],
							"billing_name":order_data['billing_name'],
							"billing_company":order_data['billing_company'],
							"billing_email_address":order_data['billing_email_address'],
							"billing_street_address":order_data['billing_street_address'],
							"billing_street_address1":order_data['billing_street_address1'],
							"billing_city":order_data['billing_city'],
							"billing_postcode":order_data['billing_postcode'],
							"billing_state":order_data['billing_state'],
							"billing_country":order_data['billing_country'],
							"billing_phone":order_data['billing_phone'],
							"delivery_name":order_data['delivery_name'],
							"delivery_company":order_data['delivery_company'],
							"delivery_email_address":order_data['delivery_email_address'],
							"delivery_street_address":order_data['delivery_street_address'],
							"delivery_street_address1":order_data['delivery_street_address1'],
							"delivery_city":order_data['delivery_city'],
							"delivery_postcode":order_data['delivery_postcode'],
							"delivery_state":order_data['delivery_state'],
							"delivery_country":order_data['delivery_country'],
							"delivery_phone":order_data['delivery_phone'],
						}
					}
					arrayProduct = {}
					counter = 0
					total_saved = 0
					product_list_arr = []
					for orderDataList in order_data['order_products']:
						is_shortage = 'No'
						if int(orderDataList['shortage'])>0 or int(orderDataList['returns'])>0 or int(orderDataList['deleted_quantity'])>0:
							is_shortage='yes'
						product_list = {}
						product_image = ""
						image_path = ""
						if len(orderDataList['product']['product_images'])>0:
							
							for productimage in orderDataList['product']['product_images']:
								if productimage['is_cover']==1:
									product_image = productimage['img']
									image_path = productimage['link']
								else:
									product_image = productimage['img']
									image_path = productimage['link']
							
							orderDataList['product'].pop("product_images")
						total_quantity=int(orderDataList['quantity'])-int(orderDataList['deleted_quantity'])-int(orderDataList['shortage'])-int(orderDataList['returns'])
						total_saved=float(total_saved) + (float(orderDataList['product_discount_price'])*int(total_quantity))
						product_list = {
							"id":orderDataList['id'],
							"order_id":order_id,
							"product_id":orderDataList["product"]['id'],
							"product_image":product_image,
							"product_image_path":image_path,
							"product_name":orderDataList['product']['name'],
							"product_description":orderDataList['product']['description'],
							"product_default_price":orderDataList['product']['default_price'],
							"product_price":orderDataList['product_price'],
							"product_discount_price":orderDataList['product_discount_price'],
							"product_excise_duty":orderDataList['product_excise_duty'],
							"product_tax_price":orderDataList['product_tax_price'],
							"product_tax_name":orderDataList['tax_name'],
							"warehouse_id":orderDataList['warehouse_id'],
							"quantity":total_quantity,
							"is_shortage":is_shortage,						
						}
						product_list_arr.append(product_list)
					data.update({"ProductList":product_list_arr})
					total_saved= float(total_saved)+float(order_data['cart_discount'])
					OrderSummary = {
						"sub_total":order_data['gross_amount'],
						"delivery_charges":order_data['shipping_cost'],
						"promo_code":order_data['applied_coupon'],
						# "referal_code":order_data['referal_code'],
						# "loyality_point":order_data['loyality_point'],
						"total_saved":total_saved,
						"total_paid":order_data['gross_amount'],
						"net_amount":order_data['net_amount']
					}
					data.update({"OrderSummary":OrderSummary})
					status = 1
					msg='Success'
				else:
					status=0
					msg='No such details'
			except Exception as error:
				trace_back = sys.exc_info()[2]
				line = trace_back.tb_lineno
				data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}
		else:
			status=0
			msg='Provide both website id and order id'

		data = {
			"details":data,
			"ack":status,
			"msg":msg
		}
	except Exception as error:
		trace_back = sys.exc_info()[2]
		line = trace_back.tb_lineno
		data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}
	return data

class update_delivery_status(generics.ListAPIView):
	
	def post(self, request, format=None):
		website_id = 1
		company_id = 1
		requestdata = request.data

		order_id = requestdata['order_id']
		latitude = requestdata['latitude']
		longitude = requestdata['longitude']
		signature = requestdata['signature']
		now = datetime.datetime.now()
		today = now.date()
		now_utc     = datetime.datetime.now(datetime.timezone.utc).astimezone()
		if order_id:
			# filename = "signature"+rand("10000","99999").time()+".png"
			filename = "signature"+".png"
			delivery_date = now_utc
			order_status = 4
			save_arr = {}
			save_arr = {
				"order_status":order_status,
				"delivery_date":delivery_date,
				"signature_image":filename
			}
			is_update = EngageboostOrdermaster.objects.filter(id=order_id).update(**save_arr)
			# $affectedRows = $this->OrderList->getAffectedRows();
			affectedRows = is_update
			if affectedRows:
				status=1
				msg='Success'
				orderData = EngageboostOrdermaster.objects.filter(id=order_id).first()

				address_book_id = orderData.address_book_id
				update_arr = {}

				update_arr = {
					"lat_val":latitude,
					"long_val":longitude
				}
				rs_data = EngageboostCustomersAddressBook.objects.filter(id=address_book_id).update(**update_arr)
				# $this->send_sms($orderData,3107, $orderData['OrderList']['delivery_phone'],1, $orderData['OrderList']['customer_id']);
			else:
				status = 0
				msg = 'Already updated.'
			img_data = b'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'
			fh = open("/var/www/html/imageToSave.png", "wb")
			# fh.write(img_data.decode('base64'))
			fh.write(base64.decodebytes(img_data))
			fh.close()
		else:
			status = 0
			msg = "Provide order id."
		
		data = {
			"ack":status,
			"msg":msg
		}
		return Response(data)

class delivery_order_list_and_details(generics.ListAPIView):

	def post(self, request, format=None):
		website_id = 1
		company_id = 1
		now = datetime.datetime.now()
		today = now.date()
		now_utc     = datetime.datetime.now(datetime.timezone.utc).astimezone()
		requestdata = request.data
        # $date=date('Y-m-d');

		driver_id = requestdata['driver_id']

		warehouse_lat_long         = get_latitude_longitude()
		warehouse_lat_long_str     = warehouse_lat_long.split(",")
		warehouse_latitude         = warehouse_lat_long_str[0]
		warehouse_longitude        = warehouse_lat_long_str[1]
		# details = delivery_order_derails_return(orderdetails['id'])
		returndata = {}
		data       = {}
		try:
			if driver_id:		
				rs_orderdetails = EngageboostDriverVeichleMap.objects.filter(user_id=driver_id, delivery_date=today).all()
				# delivery_order_derails = DeliveryOrderSerializer(rs_orderdetails, many=True)
				delivery_order_derails = DeliveryOrderListSerializer(rs_orderdetails, many=True)
				delivery_order_derails = delivery_order_derails.data
				list_order_ids = []
				rs_delivery_order_ids = DeliveryOrdersSerializer(rs_orderdetails, many=True)
				if len(rs_delivery_order_ids.data)>0:
					for delivery_order in rs_delivery_order_ids.data:						
						if delivery_order['DeliveryPlanOrder'] and len(delivery_order['DeliveryPlanOrder'])>0:
							for order_id_data in delivery_order['DeliveryPlanOrder']:
								list_order_ids.append(order_id_data['order_id'])

				rs_time_slot = EngageboostOrdermaster.objects.filter(id__in=list_order_ids).values_list('time_slot_id', flat=True).distinct().order_by("time_slot_id")
				try:
					if len(rs_orderdetails)>0:
						dd = {}
						for x in range(len(rs_time_slot)):
							timeslotdata=[]
							for delivery_orderdetails in delivery_order_derails:
								for DeliveryPlanOrder in delivery_orderdetails['DeliveryPlanOrder']:
									for orderdetails in DeliveryPlanOrder["OrderList"]:
										# $currencyformat = $orderdetails[$i]['OrderList']['currency_code'];
										details = delivery_order_derails_return(orderdetails['id'])
										currencyformat = "INR"
										paid_amount = orderdetails['net_amount'] # orderdetails['paid_amount']
										gross_amount = orderdetails['gross_amount']
										net_amount = orderdetails['net_amount']
										order_status = orderdetails['order_status']
										distance = DeliveryPlanOrder['distance']
										time = DeliveryPlanOrder['time']

										latitude 	= "22.5427604"
										longitude 	= "88.3859595"
										if orderdetails['address_book_id']:
											rs = EngageboostCustomersAddressBook.objects.filter(id = orderdetails['address_book_id']).first()
											if rs and float(rs.lat_val)>0:
												latitude = rs.lat_val
											if rs and float(rs.long_val)>0:
												longitude = rs.long_val
												
										listings = {}
										if str(rs_time_slot[x]) in orderdetails['time_slot_id']:
											listings={
												"id":orderdetails['id'],
												"custom_order_id":orderdetails['custom_order_id'],
												"time_slot_date":orderdetails['time_slot_date'],
												"time_slot_id":orderdetails['time_slot_id'],
												"billing_name":orderdetails['billing_name'],
												"billing_email_address":orderdetails['billing_email_address'],
												"billing_phone":orderdetails['billing_phone'],
												"billing_street_address":orderdetails['billing_street_address'],
												"billing_street_address1":orderdetails['billing_street_address1'],
												"billing_city":orderdetails['billing_city'],
												"billing_postcode":orderdetails['billing_postcode'],
												"billing_state":orderdetails['billing_state'],
												"billing_country_name":orderdetails['billing_country_name'],
												"delivery_name":orderdetails['delivery_name'],
												"delivery_email_address":orderdetails['delivery_email_address'],
												"delivery_phone":orderdetails['delivery_phone'],
												"delivery_street_address":orderdetails['delivery_street_address'],
												"delivery_street_address1":orderdetails['delivery_street_address1'],
												"delivery_city":orderdetails['delivery_city'],
												"delivery_postcode":orderdetails['delivery_postcode'],
												"delivery_state":orderdetails['delivery_state'],
												"delivery_country":orderdetails['delivery_country'],
												"driver_id":delivery_orderdetails['user_id'],
												"driver_name":"",
												"warehouse_id":orderdetails['assign_wh'],
												"warehouse_name":"",
												"payment_method_name":orderdetails['payment_method_name'],
												"currency":currencyformat,
												"gross_amount":gross_amount,
												"paid_amount":paid_amount,
												"net_amount":net_amount,
												"order_status":order_status,
												"sort_by_distanc":"",
												"latitude":latitude, # orderdetails["CustomerBillingAddress"]['lat_val'],
												"longitude":longitude, # orderdetails["CustomerBillingAddress"]['long_val'],
												"distance":distance,
												"time":time,
												"virtual_vechile_id":DeliveryPlanOrder['virtual_vechile_id'],
												"delivery_date":delivery_orderdetails['delivery_date'],
												"details":details['details']
											}
											timeslotdata.append(listings)
							dd.update({rs_time_slot[x]:timeslotdata})
						returndata = dd
						
						data = {
							"ack":1,
							"msg":"success",
							"latitude":warehouse_latitude,
							"longitude":warehouse_longitude,
							"response":returndata
						}
					else:
						data = {
							"ack":0,
							"latitude":warehouse_latitude,
							"longitude":warehouse_longitude,
							"msg":"No data found.",
							"response":returndata
						}
				except Exception as error:
					trace_back = sys.exc_info()[2]
					line = trace_back.tb_lineno
					data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}
		return Response(data)

class notify_order_area(generics.ListAPIView):
	
	def post(self, request, format=None):
		status    = 0
		msg    = ''
		data   = {}
		now = datetime.datetime.now()
		today = now.date()
		now_utc     = datetime.datetime.now(datetime.timezone.utc).astimezone()
		requestdata = request.data
		
		lat_val    = requestdata['lat']
		long_val   = requestdata['lng']
		order_id   = requestdata['orderId']
		driver_id  = requestdata['driverId']
		try:
			if order_id and order_id is not None:
				insert_arr = {
					"order_id":order_id,
					"driver_id":driver_id,
					"lat_val":lat_val,
					"long_val":long_val,
					"created":now_utc,
					"modified":now_utc
				}
				insert_id = EngageboostNotifyOrderArea.objects.create(**insert_arr)
				status = 1
				msg = 'success'
			else:
				status = 0
				msg = 'Order id is blank.'

			data = {
				"ack":status,
				"msg":msg
			}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}

		return Response(data)

class list_reshedule_order(generics.ListAPIView):
	
	def post(self, request, format=None):
		website_id = 1
		company_id = 1
		requestdata = request.data
		now 		= datetime.datetime.now()
		today 		= now.date()
		now_utc     = datetime.datetime.now(datetime.timezone.utc).astimezone()

		driver_id = requestdata['driver_id']

		warehouse_lat_long         = get_latitude_longitude()
		warehouse_lat_long_str     = warehouse_lat_long.split(",")
		warehouse_latitude         = warehouse_lat_long_str[0]
		warehouse_longitude        = warehouse_lat_long_str[1]

		returndata={}
		
		data = {}
		try:
			if driver_id:		
				rs_orderdetails = EngageboostDriverVeichleMap.objects.filter(user_id=driver_id, delivery_date=today).all()
				# delivery_order_derails = DeliveryOrderSerializer(rs_orderdetails, many=True)
				delivery_order_derails = DeliveryOrderListSerializer(rs_orderdetails, many=True)
				delivery_order_derails = delivery_order_derails.data
				list_order_ids = []
				rs_delivery_order_ids = DeliveryOrdersSerializer(rs_orderdetails, many=True)
				if len(rs_delivery_order_ids.data)>0:
					for delivery_order in rs_delivery_order_ids.data:						
						if delivery_order['DeliveryPlanOrder'] and len(delivery_order['DeliveryPlanOrder'])>0:
							for order_id_data in delivery_order['DeliveryPlanOrder']:
								list_order_ids.append(order_id_data['order_id'])

				rs_time_slot = EngageboostOrdermaster.objects.filter(id__in=list_order_ids).values_list('time_slot_id', flat=True).distinct()
				try:
					if len(rs_orderdetails)>0:
						dd = {}
						for x in range(len(rs_time_slot)):
							timeslotdata=[]
							for delivery_orderdetails in delivery_order_derails:
								for DeliveryPlanOrder in delivery_orderdetails['DeliveryPlanOrder']:
									for orderdetails in DeliveryPlanOrder["OrderList"]:
										# $currencyformat = $orderdetails[$i]['OrderList']['currency_code'];
										currencyformat = "INR"
										paid_amount = orderdetails['paid_amount']
										gross_amount = orderdetails['gross_amount']
										net_amount = orderdetails['net_amount']
										order_status = orderdetails['order_status']
										distance = DeliveryPlanOrder['distance']
										time = DeliveryPlanOrder['time']
										listings = {}
										if str(rs_time_slot[x]) in orderdetails['time_slot_id']:
											listings={
												"id":orderdetails['id'],
												"custom_order_id":orderdetails['custom_order_id'],
												"time_slot_date":orderdetails['time_slot_date'],
												"time_slot_id":orderdetails['time_slot_id'],
												"billing_name":orderdetails['billing_name'],
												"billing_email_address":orderdetails['billing_email_address'],
												"billing_phone":orderdetails['billing_phone'],
												"billing_street_address":orderdetails['billing_street_address'],
												"billing_street_address1":orderdetails['billing_street_address1'],
												"billing_city":orderdetails['billing_city'],
												"billing_postcode":orderdetails['billing_postcode'],
												"billing_state":orderdetails['billing_state'],
												"billing_country_name":orderdetails['billing_country_name'],
												"delivery_name":orderdetails['delivery_name'],
												"delivery_email_address":orderdetails['delivery_email_address'],
												"delivery_phone":orderdetails['delivery_phone'],
												"delivery_street_address":orderdetails['delivery_street_address'],
												"delivery_street_address1":orderdetails['delivery_street_address1'],
												"delivery_city":orderdetails['delivery_city'],
												"delivery_postcode":orderdetails['delivery_postcode'],
												"delivery_state":orderdetails['delivery_state'],
												"delivery_country":orderdetails['delivery_country'],
												"driver_id":delivery_orderdetails['user_id'],
												"driver_name":"",
												"warehouse_id":orderdetails['assign_wh'],
												"warehouse_name":"",
												"payment_method_name":orderdetails['payment_method_name'],
												"currency":currencyformat,
												"gross_amount":gross_amount,
												"paid_amount":paid_amount,
												"net_amount":net_amount,
												"order_status":order_status,
												"sort_by_distanc":"",
												"latitude":"22.5427604", # orderdetails["CustomerBillingAddress"]['lat_val'],
												"longitude":"88.3859595", # orderdetails["CustomerBillingAddress"]['long_val'],
												"distance":distance,
												"time":time,
												"virtual_vechile_id":DeliveryPlanOrder['virtual_vechile_id'],
												"delivery_date":delivery_orderdetails['delivery_date'],
											}
											timeslotdata.append(listings)
							dd.update({rs_time_slot[x]:timeslotdata})
						returndata = dd
						
						data = {
							"ack":1,
							"msg":"success",
							"latitude":warehouse_latitude,
							"longitude":warehouse_longitude,
							"response":returndata
						}
					else:
						data = {
							"ack":0,
							"latitude":warehouse_latitude,
							"longitude":warehouse_longitude,
							"msg":"No data found.",
							"response":returndata
						}
				except Exception as error:
					trace_back = sys.exc_info()[2]
					line = trace_back.tb_lineno
					data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'message':str(error)}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}

		return Response(data)