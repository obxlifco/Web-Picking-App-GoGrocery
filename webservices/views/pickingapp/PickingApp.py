from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics,viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime, timedelta
from django.db.models import Q, F
from django.views.decorators.csrf import csrf_exempt
from webservices.views import loginview
from webservices.models import *
from webservices.serializers import *
import datetime,time
from rest_framework.authtoken.models import Token
import base64
import sys,math
import traceback
from django.conf import settings
from webservices.views.common import common
from webservices.views.emailcomponent import emailcomponent
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from frontapp.views.payment.ccavRequestHandler import payment_request_si_charge_si
import random
from django.db.models import Count, Sum, Avg
import requests, csv, os

# Picker Login 
@csrf_exempt
def PickerLogin(request):
	requestdata = JSONParser().parse(request)
	username = requestdata['username']
	password = requestdata['password']
	device_id = requestdata['device_id']
	ip_address = ''
	if "ip_address" in requestdata:
		ip_address = requestdata['ip_address']

	User = EngageboostUsers.objects.filter( Q(username__iexact=username) | Q(email__iexact=username)).filter(user_type='backend',isdeleted='n', isblocked='n').first()
	cnt = 0
	if User:
		cnt = 1
	if cnt<=0:
		data = {
			'status':0,
			'message': 'Invalid Username or password.'
		}
		return JsonResponse(data)
	else:
		password_check  = User.check_password(password)
		token, created  = Token.objects.get_or_create(user=User)
		token_data      = token.key
		if password_check==True:
			now = datetime.datetime.now()
			today = now.date()
			now_utc     = datetime.datetime.now(datetime.timezone.utc).astimezone()
			EngageboostUsers.objects.filter(email__iexact=username,user_type='backend').update(last_login=now_utc,device_token_android=device_id)
			employee_name = User.first_name
			# Company Details
			defaultWebsite = EngageboostCompanyWebsites.objects.filter(id=User.website_id).first()

			#WAREHOUSE CHECKING
			warehouse_id = ""
			if User.issuperadmin !='Y':
				listOfWarehouseIds = EngageboostWarehouseMasters.objects.filter(website_id=User.website_id, isdeleted='n',isblocked='n').values_list('id')
				warehouseManager = EngageboostWarehouseManager.objects.filter(manager_id = User.id,isdeleted='n',isblocked='n',warehouse_id__in=listOfWarehouseIds).order_by('-id').first()
				if warehouseManager:
					warehouse_id = warehouseManager.warehouse_id

			curencyObj = EngageboostCurrencyRates.objects.filter(isbasecurrency = 'y',isdeleted = 'n',isblocked = 'n').first()
			currencySerialise = BaseCurrencyRateSerializer(curencyObj,partial=True)
			currencyDetails = currencySerialise.data
			userdata = {
				'first_name':User.first_name,
				'last_name':User.last_name,
				'token' : token_data,
				'user_id': User.id,
				"id":User.id,
				"email":User.email,
				"username":User.username,
				"company_id":User.company_id,
                "image_name":"",
				"website_id":User.website_id,
				"defaultwebsite":defaultWebsite.websitename,
				"defaultcurrency": currencyDetails['currency_code'],
				'currencysymbol' : currencyDetails['engageboost_currency_master']['currencysymbol'],
				'isSuperAdmin':User.issuperadmin,
				'warehouse_id' : warehouse_id
			}
			common.saveloginhistory(User.id,ip_address,'login')
			if warehouse_id is None or warehouse_id =="":
				data = {
					'status':0,
					'message': 'User has not been assigned to any store.'
				}
			else:
				data = {
					'status':1,
					'msg':'success',
					'user_data':userdata ,
				}
		else:
			data = {
					'status':0,
					'message': 'Invalid Username or password.'
				}
		return JsonResponse(data)

# Picker Logout 
class picker_logout(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = JSONParser().parse(request)
		# requestdata = request.data
		user_id 	= request.user.id
		device_id = requestdata['device_id']
		ip_address = ''
		if "ip_address" in requestdata:
			ip_address = requestdata['ip_address']
		try:
			if user_id:
				now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
				User = EngageboostUsers.objects.filter(id=user_id).filter(isdeleted='n', isblocked='n').first()

				#----Binayak Start----#
				device_details = EngageboostAllUserDeviceToken.objects.filter(user_id=user_id,
															 device_id=device_id).first()


				#-----Removing customer device token----#
				if device_details:
					if device_details.device_type == 'a':
						EngageboostCustomers.objects.filter(auth_user_id=user_id).update(device_token_android=None)
					else:
						EngageboostCustomers.objects.filter(auth_user_id=user_id).update(device_token_ios=None)

					device_details.delete()

				# ----Binayak End----#

				if User:
					common.saveloginhistory(User.id, ip_address,'logout')
					status = 1
					msg = 'Success'
				else:
					status = 0
					msg = 'User id can not be blank'
			else:
				status = 0
				msg = 'User id can not be blank'
			
			data = {"status":status,"msg":msg,"message":msg}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"message":"Something went wrong"}
		return Response(data)

@permission_classes((AllowAny, ))
class PickerForgotPassword(generics.ListAPIView):
	def post(self,request,format=None):
		requestdata = request.data
		email = requestdata['email'].strip()
		# device_id = requestdata['device_id']
		ip_address = ''
		if "ip_address" in requestdata:
			ip_address = requestdata['ip_address']
		check_user = EngageboostUsers.objects.filter(email__iexact=email,user_type='backend',isblocked='n',isdeleted='n')
		# name = EngageboostUsers.objects.filter(email__iexact=email,isblocked='n',isdeleted='n').first()
		if  check_user.count() == 0:			
			data = {"status":0,"api_status":"error","message":"User does not exist"}
			return Response(data)
		else:
			try:
				check_user = check_user.first()
				if check_user.first_name is None or check_user.first_name == "":
					first_name = email
				else:
					first_name = check_user.first_name

				#### Encode email and generate link ####
				# message_bytes = email.encode('ascii')
				# base64_bytes = base64.b64encode(message_bytes)
				# base64_email = base64_bytes.decode('ascii')
				# link = "https://gogrocery.ae/reset-password/"+base64_email
				# link = "http://15.185.126.44:81/resetpassword/"+base64_email

				OTP = str(random.randint(000000,999999))
				now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
				new_date = now_utc + datetime.timedelta(minutes=10)
				OTP_pin = str(OTP)+'_'+str(new_date)
				message_bytes = OTP_pin.encode('ascii')
				base64_bytes = base64.b64encode(message_bytes)
				OTP_pin = base64_bytes.decode('ascii')				
				
				subject = "Forgot Password"
				# message = 'Hi'+' '+ first_name +','+'<br><br>We received a request to reset your password<br>'+'<br><a href="'+link+'">Click </a> here to change your password'
				message = 'Hi'+' '+ first_name +','+'<br>We have received a request to reset your password.<br>Your OTP code is '+OTP+'. Please enter this OTP to proceed.<br>Code is valid for 10 minutes only. Please DO NOT share this OTP with anyone.'
				
				emailcomponent.SendOtherMail(email,'support@gogrocery.ae',subject,message)
				# msg = 'Reset password link has been sent to your email id %s, please check your mail.' %(email)
				msg = 'An OTP has been sent to your email id %s, please check your mail.' %(email)
				data = {"status":1,"api_status":"success","message":msg,"name":first_name}
				EngageboostUsers.objects.filter(id=check_user.id,isblocked='n',isdeleted='n').update(reset_password='n',refferal_code=OTP_pin)
				return Response(data)
			# except (TypeError, ValueError, OverflowError):
			except Exception as error:
				trace_back = sys.exc_info()[2]
				line = trace_back.tb_lineno
				data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"message":"Something went wrong"}
				return Response(data, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((AllowAny, ))
class PickerResetPassword(generics.ListAPIView):
	def post(self,request,format=None):
		requestdata = request.data
		email = requestdata['email'].strip()
		userotp = requestdata['otp']
		new_password = requestdata['new_password']
		confirm_password = requestdata['confirm_password']
		gen_password = make_password(new_password, None, 'md5')
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		nowdate = str(now_utc)
		
		check_user = EngageboostUsers.objects.filter(email__iexact=email,user_type='backend',isblocked='n',isdeleted='n').first()
		if check_user:
			if check_user.reset_password == 'y':
				data = {'status':0,'api_status':'error','message':'Password has been reset already.'}
				return Response(data)

			if str(new_password) == str(confirm_password):
				if check_user:
					if check_user.refferal_code is None or check_user.refferal_code == "":
						data = {'status':0,'api_status':'error','message':'OTP has been expired'}
					else:
						refferal_code = check_user.refferal_code
						base64_bytes = refferal_code.encode('ascii')
						message_bytes = base64.b64decode(base64_bytes)
						refferal_code = message_bytes.decode('ascii')
						OTP= refferal_code.split("_")

						if str(userotp)==str(OTP[0]):
							if OTP[1] >= nowdate:
								updata={"password":gen_password,"reset_password":'y',"refferal_code":None}
								EngageboostUsers.objects.filter(id=check_user.id,isblocked='n',isdeleted='n').update(**updata)
								data = {'status':1,	'api_status':'success','message':'Password successfully updated.'}
							else:
								data = {'status':0,'api_status':'error','message':'OTP has been expired'}
						else:
							data = {'status':0,'api_status':'error','message':'Invalid OTP.'}
				else:
					data = {'status':0,'api_status':'error','message':'User not found.'}
			else:
				data = {'status':0,'api_status':'error','message':'Password and Confirm password are not same.'}
		else:
			data = {'status':0,'api_status':'error','message':'User not found.'}
		return Response(data)

class PickerDashboard(generics.ListAPIView):
	def post(self,request,format=None):
		requestdata = request.data
		now = datetime.datetime.now()
		warehouse_id = requestdata['warehouse_id']
		if requestdata['website_id']:
			website_id = requestdata['website_id']
		else:
			website_id = 1

		if 'startdate' in requestdata and requestdata['startdate']:
			startdate = requestdata['startdate']
		else:			
			# startdate = now.date()
			startdate = None

		if 'enddate' in requestdata and requestdata['enddate']:
			enddate = requestdata['enddate'] +" "+ "23:59:59"
		else:			
			# enddate = str(now.date()) +" "+ "23:59:59"
			enddate = None

		if startdate and enddate:
			check_order = EngageboostOrdermaster.objects.filter(isdeleted='n',isblocked='n',buy_status=1,website_id=website_id,assign_wh=warehouse_id,created__gte=startdate,created__lte=enddate)
		else:
			check_order = EngageboostOrdermaster.objects.filter(isdeleted='n',isblocked='n',buy_status=1,website_id=website_id,assign_wh=warehouse_id)

		# elif order_status == "substitution_sent":
		# 	orderlistcond = EngageboostOrdermaster.objects.filter(isblocked='n',isdeleted='n',buy_status=1,website_id=website_id,assign_wh=warehouse_id, order_substitute_products__order_id=F('id'), order_substitute_products__send_approval='pending', order_status__in=[100]).all().order_by('-id').distinct('id')
		# elif order_status == "substitution_received":
		# 	orderlistcond = EngageboostOrdermaster.objects.filter(isblocked='n',isdeleted='n',buy_status=1,website_id=website_id,assign_wh=warehouse_id, order_substitute_products__order_id=F('id'), order_substitute_products__send_approval__in=('approve', 'declined'), order_status__in=[100]).all().order_by('-id').distinct('id')

		total_order = shipped_order = pending_processing_order = pending_order = processing_order = cancel_order = substitution_sent_order = substitution_received_order = 0
		if check_order:
			total_order = check_order.count()
			pending_processing_order = check_order.filter(order_status__in=[0,100]).count()
			pending_order = check_order.filter(order_status__in=[0]).count()
			processing_order = check_order.filter(order_status__in=[100]).count()
			cancel_order = check_order.filter(order_status__in=[2]).count()
			shipped_order = check_order.filter(order_status='1').count()
			substitution_sent_order = check_order.filter(order_substitute_products__order_id=F('id'), order_substitute_products__send_approval='pending', order_status__in=[100]).exclude(order_substitute_products__send_approval__in=('approve', 'declined')).all().order_by('-id').distinct('id').count()
			# for sent in substitution_sent_order:
			# 	print('sent====>', sent.id)
			substitution_received_order = check_order.filter(order_substitute_products__order_id=F('id'), order_substitute_products__send_approval__in=('approve', 'declined'), order_status__in=[100]).all().order_by('-id').distinct('id').count()
			# for received in substitution_received_order:
			# 	print('received====>', received.id)

		data = {"status":1,"api_status":"success","total_order":total_order,"pending_processing_order":pending_processing_order,"pending_order":pending_order,"processing_order":processing_order,"cancel_order":cancel_order,"shipped_order":shipped_order,
				"substitution_sent_order":substitution_sent_order, "substitution_received_order":substitution_received_order}
		return Response(data)

class PickerOrderList(generics.ListAPIView):
	def post(self, request, format=None):
		try:
			requestdata = request.data
			# user_id = requestdata['user_id']
			warehouse_id = requestdata['warehouse_id']
			if requestdata['website_id'] is None or requestdata['website_id'] =="":
				website_id = 1
			else:
				website_id = requestdata['website_id']

			if 'page' not in requestdata or requestdata['page'] is None or requestdata['page'] =="":
				page = 1
			else:
				page = requestdata['page']

			if 'per_page' not in requestdata or requestdata['per_page'] is None or requestdata['per_page'] =="":
				per_page = get_page_size()
			else:
				per_page = requestdata['per_page']

			if 'order_status' not in requestdata or requestdata['order_status'] is None or requestdata['order_status'] =="":
				order_status = None
			else:
				order_status = requestdata['order_status']

			global_setting_date = EngageboostGlobalSettings.objects.filter(website_id=website_id,isdeleted='n',isblocked='n').first()
			if global_setting_date.timezone_id:
				global_setting_zone = EngageboostTimezones.objects.filter(id = global_setting_date.timezone_id).first()
				time_offset = global_setting_zone.offset
			else:
				time_offset = 0

			# orderlistcond = EngageboostOrdermaster.objects.filter(isdeleted='n',isblocked='n',buy_status=1,website_id=website_id).exclude(order_status__in=[3,2,5,6,11,12,16])
			if order_status:
				if order_status == "shipped":
					orderlistcond = EngageboostOrdermaster.objects.filter(isdeleted='n',isblocked='n',buy_status=1,website_id=website_id,assign_wh=warehouse_id).filter(order_status__in=[1])
				elif order_status == "pending":
					orderlistcond = EngageboostOrdermaster.objects.filter(isdeleted='n',isblocked='n',buy_status=1,website_id=website_id,assign_wh=warehouse_id).filter(order_status__in=[0])
				elif order_status == "processing":
					orderlistcond = EngageboostOrdermaster.objects.filter(isdeleted='n',isblocked='n',buy_status=1,website_id=website_id,assign_wh=warehouse_id).filter(order_status__in=[100])
		
				elif order_status == "cancelled":
					orderlistcond = EngageboostOrdermaster.objects.filter(isdeleted='n',isblocked='n',buy_status=1,website_id=website_id,assign_wh=warehouse_id).filter(order_status__in=[2])
				# elif order_status == "substitution_sent":
				# 	orderlistcond = EngageboostOrdermaster.objects.filter(isblocked='n',isdeleted='n',buy_status=1,website_id=website_id,assign_wh=warehouse_id, order_substitute_products__order_id=F('id'), order_substitute_products__send_approval='pending', order_status__in=[100]).all().order_by('-id').distinct('id')
				# elif order_status == "substitution_received":
				# 	orderlistcond = EngageboostOrdermaster.objects.filter(isblocked='n',isdeleted='n',buy_status=1,website_id=website_id,assign_wh=warehouse_id, order_substitute_products__order_id=F('id'), order_substitute_products__send_approval__in=('approve', 'declined'), order_status__in=[100]).all().order_by('-id').distinct('id')
					
				else:
					orderlistcond = EngageboostOrdermaster.objects.filter(isdeleted='n',isblocked='n',buy_status=1,website_id=website_id,assign_wh=warehouse_id).filter(order_status__in=[0,100])
			else:
				orderlistcond = EngageboostOrdermaster.objects.filter(isdeleted='n',isblocked='n',buy_status=1,website_id=website_id,assign_wh=warehouse_id).filter(order_status__in=[0,100])

			if orderlistcond.count()>0:
				total_order = orderlistcond.count()
				total_page = math.ceil(orderlistcond.count()/per_page)
				next_page = page+1
				current_page = page
				page = page-1
				if page > 0:					
					offset = page*per_page
				else:
					offset = 0
				limit = offset+per_page
				orderlistcond = orderlistcond.order_by('-id').all()[offset:limit]
				orderlist = OrderListSerializerPickingApp(orderlistcond,many=True)
				if orderlist:
					print('orderlist======>', orderlistcond.count())
					username = created_by_name = None
					for orderlists in orderlist.data:
						print('orderlists.id======>', orderlists['id'])
						created = datetime.datetime.strptime(str(orderlists['created']), "%Y-%m-%dT%H:%M:%S.%fZ")
						modified = datetime.datetime.strptime(str(orderlists['modified']), "%Y-%m-%dT%H:%M:%S.%fZ")
						
						if time_offset < 0:
							time_offset = str(time_offset).split('-')
							time_offset = time_offset[1]
							created  = created - timedelta(hours=float(time_offset))
							modified  = modified - timedelta(hours=float(time_offset))
						else:
							created  = created + timedelta(hours=float(time_offset))
							modified  = modified + timedelta(hours=float(time_offset))

						#*** Custom Gross Total Amount Calculation ****#
						if orderlists["order_amount"]:
							if orderlists["flag_order"] == 1 or orderlists["flag_order"] == '1':
								grand_total = (float(orderlists["net_amount"])+float(orderlists["cod_charge"])+float(orderlists["shipping_cost"])+float(orderlists["tax_amount"]))-float(orderlists["cart_discount"])-float(orderlists["pay_wallet_amount"])
							else:
								grand_total = (float(orderlists["order_net_amount"])+float(orderlists["cod_charge"])+float(orderlists["shipping_cost"])+float(orderlists["tax_amount"]))-float(orderlists["cart_discount"])-float(orderlists["pay_wallet_amount"])

							orderlists["gross_amount"] = grand_total
							orderlists["gross_amount_base"] = grand_total

						orderlists['created'] = format_date(str(created),'%Y-%m-%d %H:%M:%S')
						orderlists['modified'] = format_date(str(modified),'%Y-%m-%d %H:%M:%S')

						#------Binayak Start 10-10-2020------#
						is_substitution = EngageboostOrdermaster.objects.filter(id=orderlists['id'],
															  order_substitute_products__order_id=F('id'),
															  # order_substitute_products__send_approval='pending'
															  order_status__in=[100]).all().order_by('-id')

						# print('is_substitution.count()', is_substitution.count())

						if is_substitution.count():
							is_substitution_pending = is_substitution.filter(order_substitute_products__send_approval='pending').exclude(
								order_substitute_products__send_approval__in=('approve', 'declined')).distinct('id')

							if is_substitution_pending.count():
								orderlists['substitute_status'] = 'pending'

							is_substitution_done = is_substitution.filter(
								order_substitute_products__send_approval__in=('approve', 'declined')).distinct('id')

							if is_substitution_done.count():
								orderlists['substitute_status'] = 'done'

							is_substitution_picker_only = is_substitution.filter(
								order_substitute_products__send_approval__isnull=True).distinct('id')

							if is_substitution_picker_only.count():
								orderlists['substitute_status'] = 'none'

						else:
							orderlists['substitute_status'] = 'none'

						#------Binayak End 10-10-2020------#

						if orderlists['order_activity']:
							orderlists['order_activity']['activity_date'] = format_date(orderlists['order_activity']['activity_date'],'%Y-%m-%d %H:%M:%S')
						
						if orderlists['assign_to']:
							checkuser = EngageboostUsers.objects.filter(id=orderlists['assign_to']).first()			
							if checkuser:								
								if checkuser.first_name is None or checkuser.first_name == "":
									username = ""
								else:
									username = checkuser.first_name
								if checkuser.last_name is None or checkuser.last_name == "":
									username = username
								else:
									username = username+' '+checkuser.last_name
						orderlists['assign_to_name'] = username

						if 'order_shipment' in orderlists and orderlists['order_shipment']:
							if orderlists['picker_name']:
								orderlists['order_shipment']['created_by_name'] = orderlists['picker_name']
							else:
								checkuser = EngageboostUsers.objects.filter(id=orderlists['order_shipment']['created_by']).first()
								if checkuser:								
									if checkuser.first_name is None or checkuser.first_name == "":
										created_by_name = ""
									else:
										created_by_name = checkuser.first_name
									if checkuser.last_name is None or checkuser.last_name == "":
										created_by_name = created_by_name
									else:
										created_by_name = created_by_name+' '+checkuser.last_name
								orderlists['order_shipment']['created_by_name'] = created_by_name
				data = {
					"status":1,
					"api_status":"success",
					"total_order":total_order,
					"total_page":total_page,
					"current_page":current_page,
					"next_page":next_page,
					"per_page":per_page,
					"response":orderlist.data,
					"message": "Orderlist has been found"
				}
			else:
				data = {"status":0,"api_status":"error","response":[],"message": "No orderlist found"}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"response":[],"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

class PickerOrderDetails(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = request.data
		try:
			if requestdata['website_id'] is None or requestdata['website_id'] =="":
				website_id = 1
			else:
				website_id = requestdata['website_id']
			order_id = requestdata['order_id']

			global_setting_date = EngageboostGlobalSettings.objects.filter(website_id=website_id,isdeleted='n',isblocked='n').first()
			if global_setting_date.timezone_id:
				global_setting_zone = EngageboostTimezones.objects.filter(id = global_setting_date.timezone_id).first()
				time_offset = global_setting_zone.offset
			else:
				time_offset = 0

			orderlistcond = EngageboostOrdermaster.objects.filter(id=order_id,isdeleted='n',isblocked='n',buy_status=1,website_id=website_id)
			if orderlistcond:
				username = created_by_name = None
				orderlist = OrderAndOrderProductAndOrderSubstituteProductSerializer(orderlistcond,many=True)
				if orderlist:
					additional_globalsettings = EngageboostAdditionalGlobalsettings.objects.filter(settings_key__in=["minimum_substitute_limit","maximum_substitute_limit","substitute_approval_time"],isblocked='n',isdeleted='n').order_by('-id').all()
					for orderlists in orderlist.data:
						#*** Custom Gross Total Amount Calculation ****#
						if orderlists["order_amount"]:
							if orderlists["flag_order"] == 1 or orderlists["flag_order"] == '1':
								grand_total = (float(orderlists["net_amount"])+float(orderlists["cod_charge"])+float(orderlists["shipping_cost"])+float(orderlists["tax_amount"]))-float(orderlists["cart_discount"])-float(orderlists["pay_wallet_amount"])
							else:
								grand_total = (float(orderlists["order_net_amount"])+float(orderlists["cod_charge"])+float(orderlists["shipping_cost"])+float(orderlists["tax_amount"]))-float(orderlists["cart_discount"])-float(orderlists["pay_wallet_amount"])

							orderlists["gross_amount"] = grand_total
							orderlists["gross_amount_base"] = grand_total

						created = datetime.datetime.strptime(str(orderlists['created']), "%Y-%m-%dT%H:%M:%S.%fZ")
						modified = datetime.datetime.strptime(str(orderlists['modified']), "%Y-%m-%dT%H:%M:%S.%fZ")
						
						if time_offset < 0:
							time_offset = str(time_offset).split('-')
							time_offset = time_offset[1]
							created  = created - timedelta(hours=float(time_offset))
							modified  = modified - timedelta(hours=float(time_offset))
						else:
							created  = created + timedelta(hours=float(time_offset))
							modified  = modified + timedelta(hours=float(time_offset))

						orderlists['created'] = format_date(str(created),'%Y-%m-%d %H:%M:%S')
						orderlists['modified'] = format_date(str(modified),'%Y-%m-%d %H:%M:%S')

						minimum_substitute_limit = maximum_substitute_limit = substitute_approval_time = None
						if additional_globalsettings:
							for add_globalset in additional_globalsettings:
								if add_globalset.settings_key == "minimum_substitute_limit":
									if add_globalset.settings_value is None or add_globalset.settings_value == "":
										pass
									else:
										minimum_substitute_limit = int(add_globalset.settings_value)
								if add_globalset.settings_key == "maximum_substitute_limit":
									if add_globalset.settings_value is None or add_globalset.settings_value == "":
										pass
									else:
										maximum_substitute_limit = int(add_globalset.settings_value)
								if add_globalset.settings_key == "substitute_approval_time":
									if add_globalset.settings_value is None or add_globalset.settings_value == "":
										pass
									else:
										substitute_approval_time = int(add_globalset.settings_value)

						orderlists['minimum_substitute_limit'] = minimum_substitute_limit
						orderlists['maximum_substitute_limit'] = maximum_substitute_limit
						orderlists['substitute_approval_time'] = substitute_approval_time

						any_substtitute_exists = EngageboostOrderSubstituteProducts.objects.filter(order_id=order_id,pick_as_substitute='y',quantity__gt=0,send_approval__in=['approve','declined']).count()
						unavailable_products = []
						if 'order_products' in orderlists and orderlists['order_products']:
							for i in range(len(orderlists['order_products'])):
							# for order_products in orderlists['order_products']:
								#**** LIST UNAVAILABLE PRODUCT ****#
								order_quantity = orderlists['order_products'][i]['quantity']
								order_shortage = orderlists['order_products'][i]['shortage']
								# print(str(any_substtitute_exists)+"**"+str(order_quantity)+"**"+str(order_shortage))
								if order_shortage > 0 and order_quantity == order_shortage and any_substtitute_exists>0:
									unavailable_products.append(orderlists['order_products'][i]['id'])
									continue

								# *** GET PRODUCT CATEGORIES *** #
								product_main_category = product_child_category1 = product_child_category2 = ""
								product_all_category = []
								get_parent_category = common.get_category_hierarchy(orderlists['order_products'][i]['product']['id'],'name')
								if get_parent_category is not None:
									product_main_category = get_parent_category[0]
									total_category_level = len(get_parent_category)
									if total_category_level > 1 and total_category_level <3:
										product_child_category1 = get_parent_category[1]
									if total_category_level > 2 and total_category_level <4:
										product_child_category1 = get_parent_category[1]
										product_child_category2 = get_parent_category[2]
									product_all_category = get_parent_category

								orderlists['order_products'][i]['product_parent_category'] = product_main_category
								orderlists['order_products'][i]['product_child_category1'] = product_child_category1
								orderlists['order_products'][i]['product_child_category2'] = product_child_category2
								orderlists['order_products'][i]['product_categories'] = product_all_category
								# *** GET PRODUCT CATEGORIES *** #

								orderlists['order_products'][i]['created_time'] = format_date(str(orderlists['order_products'][i]['created']),'%Y-%m-%d %H:%M:%S')
								orderlists['order_products'][i]['minimum_substitute_limit'] = minimum_substitute_limit
								orderlists['order_products'][i]['maximum_substitute_limit'] = maximum_substitute_limit
								if float(orderlists['order_products'][i]['weight']) > 0:
									orderlists['order_products'][i]['weight'] = orderlists['order_products'][i]['weight']
								else:
									if orderlists['order_products'][i]['product']:
										if orderlists['order_products'][i]['product']['weight'] is None or orderlists['order_products'][i]['product']['weight'] == "":
											orderlists['order_products'][i]['weight'] = float(0)
										else:
											orderlists['order_products'][i]['weight'] = float(orderlists['order_products'][i]['product']['weight'])
									else:
										orderlists['order_products'][i]['weight'] = float(0)
									
							#**** REMOVE UNAVAILABLE PRODUCT ****#
							if unavailable_products:
								orderlists['order_products'] = [x for x in orderlists['order_products'] if x['id'] not in unavailable_products]

						if 'order_substitute_products' in orderlists and orderlists['order_substitute_products']:
							for order_substitute_products in orderlists['order_substitute_products']:
								# *** GET PRODUCT CATEGORIES *** #
								product_main_category = product_child_category1 = product_child_category2 = ""
								product_all_category = []
								get_parent_category = common.get_category_hierarchy(order_substitute_products['product']['id'],'name')
								if get_parent_category is not None:
									product_main_category = get_parent_category[0]
									total_category_level = len(get_parent_category)
									if total_category_level > 1 and total_category_level <3:
										product_child_category1 = get_parent_category[1]
									if total_category_level > 2 and total_category_level <4:
										product_child_category1 = get_parent_category[1]
										product_child_category2 = get_parent_category[2]
									product_all_category = get_parent_category

								order_substitute_products['product_parent_category'] = product_main_category
								order_substitute_products['product_child_category1'] = product_child_category1
								order_substitute_products['product_child_category2'] = product_child_category2
								order_substitute_products['product_categories'] = product_all_category
								# *** GET PRODUCT CATEGORIES *** #

								order_substitute_products['created_time'] = format_date(str(order_substitute_products['created']),'%Y-%m-%d %H:%M:%S')
								if float(order_substitute_products['weight']) > 0:
									order_substitute_products['weight'] = order_substitute_products['weight']
								else:
									if order_substitute_products['product']:
										if order_substitute_products['product']['weight'] is None or order_substitute_products['product']['weight'] == "":
											order_substitute_products['weight'] = float(0)
										else:
											order_substitute_products['weight'] = float(order_substitute_products['product']['weight'])
									else:
										order_substitute_products['weight'] = float(0)

						order_substitute_products_list = order_products_list = []
						orderlists['lat_val'] = orderlists['long_val'] = None
						if 'customer_addressbook' in orderlists and orderlists['customer_addressbook']:
							if orderlists['customer_addressbook']['lat_val'] is not None and orderlists['customer_addressbook']['lat_val'] != "":
								orderlists['lat_val'] = orderlists['customer_addressbook']['lat_val']
							if orderlists['customer_addressbook']['long_val'] is not None and orderlists['customer_addressbook']['long_val'] != "":
								orderlists['long_val'] = orderlists['customer_addressbook']['long_val']

						if 'order_activity' in orderlists and orderlists['order_activity']:
							for order_activity in orderlists['order_activity']:
								order_activity['activity_date'] = format_date(order_activity['activity_date'],'%Y-%m-%d %H:%M:%S')
						
						if orderlists['assign_to']:
							checkuser = EngageboostUsers.objects.filter(id=orderlists['assign_to']).first()			
							if checkuser:								
								if checkuser.first_name is None or checkuser.first_name == "":
									username = ""
								else:
									username = checkuser.first_name
								if checkuser.last_name is None or checkuser.last_name == "":
									username = username
								else:
									username = username+' '+checkuser.last_name
						orderlists['assign_to_name'] = username

						if 'order_shipment' in orderlists and orderlists['order_shipment']:
							if orderlists['picker_name']:
								orderlists['order_shipment']['created_by_name'] = orderlists['picker_name']
							else:
								checkuser = EngageboostUsers.objects.filter(id=orderlists['order_shipment']['created_by']).first()
								if checkuser:								
									if checkuser.first_name is None or checkuser.first_name == "":
										created_by_name = ""
									else:
										created_by_name = checkuser.first_name
									if checkuser.last_name is None or checkuser.last_name == "":
										created_by_name = created_by_name
									else:
										created_by_name = created_by_name+' '+checkuser.last_name
								orderlists['order_shipment']['created_by_name'] = created_by_name

				warehouse = EngageboostWarehouseMasters.objects.filter(id=orderlistcond[0].assign_wh).first()
				if warehouse:
					orderlists['warehouse_name'] = warehouse.name

				data = {"status":1,"api_status":"success","response":orderlist.data,"message": "Order details has been found"}
			else:
				data = {"status":0,"api_status":"error","response":[],"message": "No order details has been found"}
			return Response(data)	
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)	

@permission_classes((AllowAny, ))
class PickerOrderListDetails(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = request.data
		try:
			if requestdata['website_id'] is None or requestdata['website_id'] =="":
				website_id = 1
			else:
				website_id = requestdata['website_id']
			order_id = requestdata['order_id']

			global_setting_date = EngageboostGlobalSettings.objects.filter(website_id=website_id,isdeleted='n',isblocked='n').first()
			if global_setting_date.timezone_id:
				global_setting_zone = EngageboostTimezones.objects.filter(id = global_setting_date.timezone_id).first()
				time_offset = global_setting_zone.offset
			else:
				time_offset = 0

			orderlistcond = EngageboostOrdermaster.objects.filter(id=order_id,isdeleted='n',isblocked='n',buy_status=1,website_id=website_id)

			if orderlistcond:
				username = created_by_name = None
				orderlist = OrderAndOrderProductAndOrderSubstituteProductSerializerCustomerapp(orderlistcond,many=True)
				if orderlist:
					additional_globalsettings = EngageboostAdditionalGlobalsettings.objects.filter(settings_key__in=["minimum_substitute_limit","maximum_substitute_limit","substitute_approval_time"],isblocked='n',isdeleted='n').order_by('-id').all()
					for orderlists in orderlist.data:
						created = datetime.datetime.strptime(str(orderlists['created']), "%Y-%m-%dT%H:%M:%S.%fZ")
						modified = datetime.datetime.strptime(str(orderlists['modified']), "%Y-%m-%dT%H:%M:%S.%fZ")
						
						if time_offset < 0:
							time_offset = str(time_offset).split('-')
							time_offset = time_offset[1]
							created  = created - timedelta(hours=float(time_offset))
							modified  = modified - timedelta(hours=float(time_offset))
						else:
							created  = created + timedelta(hours=float(time_offset))
							modified  = modified + timedelta(hours=float(time_offset))

						orderlists['created'] = format_date(str(created),'%Y-%m-%d %H:%M:%S')
						orderlists['modified'] = format_date(str(modified),'%Y-%m-%d %H:%M:%S')

						minimum_substitute_limit = maximum_substitute_limit = substitute_approval_time = None
						if additional_globalsettings:
							for add_globalset in additional_globalsettings:
								if add_globalset.settings_key == "minimum_substitute_limit":
									if add_globalset.settings_value is None or add_globalset.settings_value == "":
										pass
									else:
										minimum_substitute_limit = int(add_globalset.settings_value)
								if add_globalset.settings_key == "maximum_substitute_limit":
									if add_globalset.settings_value is None or add_globalset.settings_value == "":
										pass
									else:
										maximum_substitute_limit = int(add_globalset.settings_value)
								if add_globalset.settings_key == "substitute_approval_time":
									if add_globalset.settings_value is None or add_globalset.settings_value == "":
										pass
									else:
										substitute_approval_time = int(add_globalset.settings_value)

						orderlists['minimum_substitute_limit'] = minimum_substitute_limit
						orderlists['maximum_substitute_limit'] = maximum_substitute_limit
						orderlists['substitute_approval_time'] = substitute_approval_time

						if 'order_products' in orderlists and orderlists['order_products']:
							for order_products in orderlists['order_products']:
								order_products['minimum_substitute_limit'] = minimum_substitute_limit
								order_products['maximum_substitute_limit'] = maximum_substitute_limit
								order_products['created_time'] = format_date(str(order_products['created']),'%Y-%m-%d %H:%M:%S')
								if float(order_products['weight']) > 0:
									order_products['weight'] = order_products['weight']
								else:
									if order_products['product']:
										if order_products['product']['weight'] is None or order_products['product']['weight'] == "":
											order_products['weight'] = float(0)
										else:
											order_products['weight'] = float(order_products['product']['weight'])
									else:
										order_products['weight'] = float(0)

								is_accepted_count = EngageboostOrderSubstituteProducts.objects.filter(order_id=order_id,substitute_product_id=order_products['product']['id'],pick_as_substitute='y',quantity__gt=0,send_approval__in=['approve','declined']).count()

								osp_cond = EngageboostOrderSubstituteProducts.objects.filter(order_id=order_id,substitute_product_id=order_products['product']['id'],pick_as_substitute='y',quantity__gt=0).all().order_by('-id')
								if osp_cond:
									ospserializer = OrderSubstituteProductsSerializer(osp_cond, many=True)
									ospserializer = ospserializer.data
								else:
									ospserializer = []
								if ospserializer:
									for order_substitute_products in ospserializer:
										order_substitute_products['created_time'] = format_date(str(order_substitute_products['created']),'%Y-%m-%d %H:%M:%S')
										# if float(order_substitute_products['weight']) > 0:
										# 	order_substitute_products['weight'] = order_substitute_products['weight']
										# else:
										# 	if order_substitute_products['product']:
										# 		if order_substitute_products['product']['weight'] is None or order_substitute_products['product']['weight'] == "":
										# 			order_substitute_products['weight'] = float(0)
										# 		else:
										# 			order_substitute_products['weight'] = float(order_substitute_products['product']['weight'])
										# 	else:
										# 		order_substitute_products['weight'] = float(0)

								order_products['substitute_products'] = ospserializer
								if is_accepted_count > 0:
									order_products['send_approval'] = "action_taken"
								else:
									order_products['send_approval'] = "action_pending"

						# if 'order_substitute_products' in orderlists and orderlists['order_substitute_products']:
						# 	for order_substitute_products in orderlists['order_substitute_products']:
						# 		if float(order_substitute_products['weight']) > 0:
						# 			order_substitute_products['weight'] = order_substitute_products['weight']
						# 		else:
						# 			if order_substitute_products['product']:
						# 				if order_substitute_products['product']['weight'] is None or order_substitute_products['product']['weight'] == "":
						# 					order_substitute_products['weight'] = float(0)
						# 				else:
						# 					order_substitute_products['weight'] = float(order_substitute_products['product']['weight'])
						# 			else:
						# 				order_substitute_products['weight'] = float(0)

						order_substitute_products_list = order_products_list = []
						orderlists['lat_val'] = orderlists['long_val'] = None
						if 'customer_addressbook' in orderlists and orderlists['customer_addressbook']:
							if orderlists['customer_addressbook']['lat_val'] is not None and orderlists['customer_addressbook']['lat_val'] != "":
								orderlists['lat_val'] = orderlists['customer_addressbook']['lat_val']
							if orderlists['customer_addressbook']['long_val'] is not None and orderlists['customer_addressbook']['long_val'] != "":
								orderlists['long_val'] = orderlists['customer_addressbook']['long_val']

						if 'order_activity' in orderlists and orderlists['order_activity']:
							for order_activity in orderlists['order_activity']:
								order_activity['activity_date'] = format_date(order_activity['activity_date'],'%Y-%m-%d %H:%M:%S')
						
						if orderlists['assign_to']:
							checkuser = EngageboostUsers.objects.filter(id=orderlists['assign_to']).first()			
							if checkuser:								
								if checkuser.first_name is None or checkuser.first_name == "":
									username = ""
								else:
									username = checkuser.first_name
								if checkuser.last_name is None or checkuser.last_name == "":
									username = username
								else:
									username = username+' '+checkuser.last_name
						orderlists['assign_to_name'] = username

						if 'order_shipment' in orderlists and orderlists['order_shipment']:
							if orderlists['picker_name']:
								orderlists['order_shipment']['created_by_name'] = orderlists['picker_name']
							else:
								checkuser = EngageboostUsers.objects.filter(id=orderlists['order_shipment']['created_by']).first()
								if checkuser:								
									if checkuser.first_name is None or checkuser.first_name == "":
										created_by_name = ""
									else:
										created_by_name = checkuser.first_name
									if checkuser.last_name is None or checkuser.last_name == "":
										created_by_name = created_by_name
									else:
										created_by_name = created_by_name+' '+checkuser.last_name
								orderlists['order_shipment']['created_by_name'] = created_by_name

				data = {"status":1,"api_status":"success","response":orderlist.data,"message": "Order details has been found"}
			else:
				data = {"status":0,"api_status":"error","response":[],"message": "No order details has been found"}
			return Response(data)	
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)	

class PickerGeneratePicklist(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = request.data
		try:
			company_db = loginview.db_active_connection(request)
			now_utc = datetime.datetime.utcnow()
			if requestdata['website_id'] is None or requestdata['website_id'] =="":
				website_id = 1
			else:
				website_id = requestdata['website_id']
			user_id = requestdata['user_id']
			picker_name = requestdata['picker_name']
			order_id = requestdata['order_id']
			shipment_id = requestdata['shipment_id']
			order_status = requestdata['order_status']			
			picklist_prefix = 'PCK#'
			shipment_prefix = "SHM#"

			checkuser = EngageboostUsers.objects.filter(id=user_id).first()
			if checkuser:
				# username = None
				# if checkuser.first_name is None or checkuser.first_name == "":
				# 	username = ""
				# else:
				# 	username = checkuser.first_name
				# if checkuser.last_name is None or checkuser.last_name == "":
				# 	username = username
				# else:
				# 	username = username+' '+checkuser.last_name
				
				# if username is not None and picker_name is not None and username.lower() == picker_name.lower():
				if picker_name is not None:
					#**** GENERATE PICKLIST ID ****#
					# lastPicklistRecord = EngageboostTrentPicklists.objects.last()
					# if lastPicklistRecord:
					# 	lastPickList = EngageboostTrentPicklists.objects.order_by('-id').latest('id')
					# 	picklist_id = int(lastPickList.id)+int(1)
					# else:
					# 	picklist_id = 1
					# trents_picklist_no = picklist_prefix+str(picklist_id)
					#**** GENERATE PICKLIST ID ****#

					#**** FETCH SHIPMENT DETAILS ****#
					if shipment_id > 0:
						shipment_details  = EngageboostShipments.objects.filter(id=shipment_id).first()
					else:
						shipment_details = None
					#**** FETCH SHIPMENT DETAILS ****#

					if shipment_details is not None and shipment_id > 0:
						picklist_created_date = shipment_details.created
						picklist_id = shipment_details.picklist_id
						warehouse_id = shipment_details.warehouse_id
					else:
						#**** GENERATE SHIPMENT ID ****#
						# lastShipmentRecord = EngageboostShipments.objects.last()
						# if lastShipmentRecord:
						# 	shipment_id = int(lastShipmentRecord.id)+int(1)
						# else:
						# 	shipment_id = 1						
						# shipment_id_no = shipment_prefix+str(shipment_id)
						#**** GENERATE SHIPMENT ID ****#

						picklist_created_date = now_utc

						orderlistdetails = EngageboostOrdermaster.objects.filter(id=order_id,website_id=website_id).all()
						orderlistdetails_serializer = OrderMasterSerializer(orderlistdetails, many=True)
						warehouse_id = orderlistdetails_serializer.data[0]["assign_wh"]
						assign_to = orderlistdetails_serializer.data[0]["assign_to"]
						zone_id = orderlistdetails_serializer.data[0]["zone_id"]
						# warehouse_id = orderlistdetails.assign_wh
						# assign_to = orderlistdetails.assign_to
						# zone_id = orderlistdetails.zone_id

						#**** CREATE SHIPMENT & GENERATE SHIPMENT ID****#
						Picklist = EngageboostTrentPicklists.objects.create(isconfirmed ='Y',is_sub_picklist = 'No',picklist_status = 'Picking',modified=now_utc,created=now_utc,warehouse_id=warehouse_id,zone_id=zone_id)
						picklist_id = Picklist.id
						trents_picklist_no = picklist_prefix+str(picklist_id)
						EngageboostTrentPicklists.objects.filter(id = picklist_id).update(trents_picklist_no = trents_picklist_no)

						Shipment = EngageboostShipments.objects.create(warehouse_id=warehouse_id,created_by=user_id,shipment_status='Picking',created=now_utc,modified=now_utc,website_id=website_id,zone_id=zone_id,picklist_id=picklist_id)
						shipment_id = Shipment.id
						shipment_id_no = shipment_prefix+str(shipment_id)
						EngageboostShipments.objects.filter(id = shipment_id).update(custom_shipment_id=shipment_id_no)
						#**** CREATE SHIPMENT & GENERATE SHIPMENT ID****#

						if picklist_id > 0 and shipment_id > 0:
							update_dict = {"order_status":100,"buy_status":1,"shipment_id":shipment_id,"trent_picklist_id":picklist_id,"picker_name":picker_name}
							EngageboostOrdermaster.objects.filter(id=order_id,website_id=website_id).update(**update_dict)
							EngageboostOrderProducts.objects.filter(order_id=order_id).update(trents_picklist_id=picklist_id)

							rs_order_product = EngageboostOrderProducts.objects.filter(order_id=order_id).values('product_id').annotate(total_quantity=Sum('quantity'))
							i=0
							for order_product in rs_order_product:
								i=i+1
								rs_orderproduct = EngageboostOrderProducts.objects.filter(product_id=order_product['product_id']).first()
								pick_mrp            = 0
								product_tax_price   = 0
								tax_percentage      = 0
								tax_name            = ''
								if rs_orderproduct:
									pick_mrp = float(rs_orderproduct.product_price)+float(rs_orderproduct.product_discount_price)
									product_tax_price = rs_orderproduct.product_tax_price
									tax_percentage = rs_orderproduct.tax_percentage
									tax_name = rs_orderproduct.tax_name
									insert_arr = {"sr_no": i,"trent_picklist_id":picklist_id,"product_id":order_product['product_id'],"qty":order_product['total_quantity'],"confirm_quantity":order_product['total_quantity'],"stock_available":'y',
										"pick_mrp":pick_mrp,"product_tax_price":product_tax_price,"tax_percentage":tax_percentage,"tax_name":tax_name}
									EngageboostTrentsPicklistProducts.objects.create(**insert_arr)

							# rs_order = EngageboostOrdermaster.objects.filter(id__in=order_id).all()
							if orderlistdetails:
								for orderdata in orderlistdetails_serializer.data:
									#**** INSERT IN SHIPMENT ORDER ****#
									shipment_order_id = EngageboostShipmentOrders.objects.create(shipment_status = 'Picking',custom_order_id = orderdata['custom_order_id'],webshop_id = orderdata['webshop']['id'],warehouse_id = orderdata['assign_wh'],shipping_method_id = orderdata['shipping_method_id'],zone_id = orderdata['zone_id'],order_id = orderdata['id'],shipment = shipment_id,trent_picklist_id=picklist_id)

									#**** INSERT IN SHIPMENT ORDER PRODUCT ****#
									if len(orderdata['order_products']) > 0:
										for order_products in orderdata['order_products']:
											EngageboostShipmentOrderProducts.objects.create(shipment_status = 'Picking',quantity = order_products['quantity'],warehouse_id = order_products['assign_wh'],order_id = order_products['order'],order_product_id = order_products['id'],product_id = order_products['product']['id'],shipment = shipment_id,shipment_order_id = shipment_order_id.id,trent_picklist_id=picklist_id)

											#**** INSERT IN SCANNED ORDER PRODUCT ****#
											# if order_products['quantity'] > 0:
											# 	for scaned_quantity in range(order_products['quantity']):
											# 		EngageboostScannedOrderProducts.objects.create(order_product_id=order_products['id'],order_id=orderdata['id'],product_id=order_products['product']['id'],barcode=None,quantity=1,product_old_price=order_products['product_price'],product_new_price=order_products['product_price'],weight=order_products['weight'],product_discount_price=order_products['product_discount_price'],product_tax_price=order_products['product_tax_price'],created=now_utc,modified=now_utc,is_deleted='n',is_blocked='n',pick_as_substitute='n')

									if shipment_order_id.id > 0 and shipment_id > 0:
										elastic = common.change_field_value_elastic(orderdata['id'],'EngageboostOrdermaster',{'order_status':'100','shipping_status':'Picking'})
										activityType = 1
										activityMsg = "Order is Picking by "+picker_name
										activity_details = common.save_order_activity(company_db,orderdata['id'],now_utc,7,activityMsg,user_id,activityType)

							data = {'status':1,'api_status':'success','shipment_id':shipment_id,'picklist_id':picklist_id,'message':'Picklist has been created successfully'}
						else:
							data = {'status':0,'api_status':'error','message':'Picklist or Shipment is not generated'}
				else:
					data = {'status':0,'api_status':'error','message':'Invalid user'}
			else:
				data = {'status':0,'api_status':'error','message':'Invalid user'}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

class PickerProductList(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = request.data
		try:
			now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
			if requestdata['website_id'] is None or requestdata['website_id'] =="":
				website_id = 1
			else:
				website_id = requestdata['website_id']
			user_id = requestdata['user_id']
			order_id = requestdata['order_id']
			warehouse_id = requestdata['warehouse_id']
			if 'page' not in requestdata or requestdata['page'] is None or requestdata['page'] =="":
				page = 1
			else:
				page = requestdata['page']

			if 'per_page' not in requestdata or requestdata['per_page'] is None or requestdata['per_page'] =="":
				per_page = get_page_size()
			else:
				per_page = requestdata['per_page']

			if 'search' not in requestdata or requestdata['search'] is None or requestdata['search'] =="":
				search = None
			else:
				search = requestdata['search']

			if 'ean' not in requestdata or requestdata['ean'] is None or requestdata['ean'] =="":
				ean = None
			else:
				ean = requestdata['ean']

			if 'category_id' not in requestdata or requestdata['category_id'] is None or requestdata['category_id'] =="":
				category_id = None
			else:
				category_id = requestdata['category_id']

			product_with_no_price = EngageboostChannelCurrencyProductPrice.objects.filter(price__gt=0,product_price_type_id__price_type_id=1,warehouse_id=warehouse_id).values_list("product_id",flat=True)
			# print(product_with_no_price)

			if search is None:
				if product_with_no_price:
					ProductCond = EngageboostProducts.objects.filter(website_id=website_id,isdeleted='n',isblocked='n').filter(id__in=product_with_no_price)
				else:
					ProductCond = EngageboostProducts.objects.filter(website_id=website_id,isdeleted='n',isblocked='n')
			else:
				if product_with_no_price:
					ProductCond = EngageboostProducts.objects.filter(website_id=website_id,isdeleted='n',isblocked='n').filter(Q(name__icontains=search)|Q(sku__icontains=search)|Q(description__icontains=search)|Q(brand__icontains=search)).filter(id__in=product_with_no_price)
				else:
					ProductCond = EngageboostProducts.objects.filter(website_id=website_id,isdeleted='n',isblocked='n').filter(Q(name__icontains=search)|Q(sku__icontains=search)|Q(description__icontains=search)|Q(brand__icontains=search))

			product_ids = []
			if category_id:
				isparentCategory = EngageboostCategoryMasters.objects.filter(id=category_id).first()

				if isparentCategory.parent_id == 0:
					all_cat_ids = []
					all_cat_ids.append(category_id)
					secondchild = EngageboostCategoryMasters.objects.filter(parent_id=category_id,website_id=website_id,isdeleted='n',isblocked='n').values_list('id',flat=True)
					if secondchild:
						all_cat_ids.extend(secondchild)
						thirdchild = EngageboostCategoryMasters.objects.filter(parent_id__in=secondchild,website_id=website_id,isdeleted='n',isblocked='n').values_list('id',flat=True)
						if thirdchild:
							all_cat_ids.extend(thirdchild)

					# print(all_cat_ids)
					product_ids = EngageboostProductCategories.objects.filter(category_id__in=all_cat_ids,isdeleted='n',isblocked='n').values_list('product_id',flat=True)
				else:
					product_ids = EngageboostProductCategories.objects.filter(category_id=category_id,isdeleted='n',isblocked='n').values_list('product_id',flat=True)

				if product_ids:
					ProductCond = ProductCond.filter(id__in=product_ids,website_id=website_id,isdeleted='n',isblocked='n')
				else:
					ProductCond = ProductCond
			else:
				ProductCond = ProductCond

			if ean:
				barcode_product = EngageboostMultipleBarcodes.objects.filter(barcode=ean, isdeleted = 'n', isblocked = 'n').first()
				if barcode_product:
					barcode_product_id = barcode_product.product_id
					ProductCond = ProductCond.filter(id=barcode_product_id)
				else:
					# ProductCond = ProductCond
					ProductCond = EngageboostProducts.objects.none()

			if ProductCond.count()>0:
				#**** Pagination Logic ****
				total_order = ProductCond.count()
				total_page = math.ceil(total_order/per_page)
				next_page = page+1
				current_page = page
				page = page-1
				if page > 0:					
					offset = page*per_page
				else:
					offset = 0
				limit = offset+per_page
				#**** Pagination Logic ****

				ProductCond = ProductCond.order_by('name').all()[offset:limit]

				if warehouse_id is not None:
					context = {"warehouse_id": warehouse_id}
					ProductDetails = PickerBasicinfoSerializer(ProductCond, context=context, many=True)
				else:
					ProductDetails = PickerBasicinfoSerializer(ProductCond,many=True)

				# for Products in ProductDetails.data:
				# 	product_id = Products['id']
				# 	product_stock = EngageboostProductStocks.objects.filter(product_id = product_id,warehouse_id=warehouse_id,isblocked='n',isdeleted='n').order_by('-id').first()
				# 	if product_stock:
				# 		product_stock_serializer = StockViewSerializer(product_stock, partial=True)
				# 		product_stock_serializer = product_stock_serializer.data
				# 	else:
				# 		product_stock_serializer = {"stock": 0,"safety_stock": 0,"virtual_stock": 0,"real_stock": 0}
				# 	Products['product_stock'] = product_stock_serializer

				data = {"status":1,"api_status":"success","response":ProductDetails.data,"total_order":total_order,"total_page":total_page,"current_page":current_page,"next_page":next_page,"per_page":per_page,"message":"Product has been found"}
			else:
				data = {"status":0,"api_status":"error","response":[],"message":"No product has been found"}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

class PickerSubstituteProductList(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = request.data
		try:
			now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
			if requestdata['website_id'] is None or requestdata['website_id'] =="":
				website_id = 1
			else:
				website_id = requestdata['website_id']
			user_id = requestdata['user_id']
			order_id = requestdata['order_id']
			product_id = requestdata['product_id']
			warehouse_id = requestdata['warehouse_id']
			if 'page' not in requestdata or requestdata['page'] is None or requestdata['page'] =="":
				page = 1
			else:
				page = requestdata['page']

			if 'per_page' not in requestdata or requestdata['per_page'] is None or requestdata['per_page'] =="":
				per_page = get_page_size()
			else:
				per_page = requestdata['per_page']

			if 'search' not in requestdata or requestdata['search'] is None or requestdata['search'] =="":
				search = None
			else:
				search = requestdata['search']

			if 'ean' not in requestdata or requestdata['ean'] is None or requestdata['ean'] =="":
				ean = None
			else:
				ean = requestdata['ean']

			if 'category_id' not in requestdata or requestdata['category_id'] is None or requestdata['category_id'] =="":
				category_id = None
			else:
				category_id = requestdata['category_id']

			# already_subs_product = EngageboostRelatedProducts.objects.filter(product_id=product_id,related_product_type=5).exclude(related_product_id=product_id).values_list('related_product_id',flat=True).all()

			product_ids = []
			if category_id:
				isparentCategory = EngageboostCategoryMasters.objects.filter(id=category_id).first()

				if isparentCategory.parent_id == 0:
					all_cat_ids = []
					all_cat_ids.append(category_id)
					secondchild = EngageboostCategoryMasters.objects.filter(parent_id=category_id,website_id=website_id,isdeleted='n',isblocked='n').values_list('id',flat=True)
					if secondchild:
						all_cat_ids.extend(secondchild)
						thirdchild = EngageboostCategoryMasters.objects.filter(parent_id__in=secondchild,website_id=website_id,isdeleted='n',isblocked='n').values_list('id',flat=True)
						if thirdchild:
							all_cat_ids.extend(thirdchild)

					# print(all_cat_ids)
					product_ids = EngageboostProductCategories.objects.filter(category_id__in=all_cat_ids,isdeleted='n',isblocked='n').values_list('product_id',flat=True)
				else:
					product_ids = EngageboostProductCategories.objects.filter(category_id=category_id,isdeleted='n',isblocked='n').values_list('product_id',flat=True)
			
			if ean:
				barcode_product = EngageboostMultipleBarcodes.objects.filter(barcode=ean, isdeleted = 'n', isblocked = 'n').first()
				if barcode_product:
					barcode_product_id = barcode_product.product_id
					# listof_subs_product = EngageboostRelatedProducts.objects.filter(product_id=product_id,related_product_type=5,related_product_id=barcode_product_id).exclude(related_product_id=product_id).values_list('related_product_id',flat=True).all()
					
					if product_ids:
						listof_subs_product = EngageboostProducts.objects.filter(website_id=website_id,isdeleted='n',isblocked='n',id=barcode_product_id).filter(id__in=product_ids).exclude(id=product_id).values_list('id',flat=True).all()
					else:
						listof_subs_product = EngageboostProducts.objects.filter(website_id=website_id,isdeleted='n',isblocked='n',id=barcode_product_id).exclude(id=product_id).values_list('id',flat=True).all()
				else:
					listof_subs_product = []
			else:
				if search is None:
					listof_subs_product = EngageboostRelatedProducts.objects.filter(product_id=product_id,related_product_type=5).exclude(related_product_id=product_id).values_list('related_product_id',flat=True).all()
					listof_subs_product_ids = list(listof_subs_product)
					if product_ids:
						product_ids = list(product_ids)
						listof_subs_product_ids.extend(product_ids)

					listof_subs_product = EngageboostProducts.objects.filter(website_id=website_id,isdeleted='n',isblocked='n',id__in=listof_subs_product_ids).exclude(id=product_id).values_list('id',flat=True).all()
				else:
					if product_ids:
						listof_subs_product = EngageboostProducts.objects.filter(website_id=website_id,isdeleted='n',isblocked='n',id__in=product_ids).filter(Q(name__icontains=search)|Q(sku__icontains=search)|Q(brand__icontains=search)|Q(description__icontains=search)).exclude(id=product_id).values_list('id',flat=True).all()
					else:
						listof_subs_product = EngageboostProducts.objects.filter(website_id=website_id,isdeleted='n',isblocked='n').filter(Q(name__icontains=search)|Q(sku__icontains=search)|Q(brand__icontains=search)|Q(description__icontains=search)).exclude(id=product_id).values_list('id',flat=True).all()
		
			if listof_subs_product:
				ProductCond = EngageboostProducts.objects.filter(id__in=listof_subs_product,website_id=website_id,isdeleted='n',isblocked='n')

				product_with_price = EngageboostChannelCurrencyProductPrice.objects.filter(price__gt=0,product_price_type_id__price_type_id=1,warehouse_id=warehouse_id).values_list("product_id",flat=True)
				product_stock_ids = EngageboostProductStocks.objects.filter(real_stock__gt=0,warehouse_id=warehouse_id,isblocked='n',isdeleted='n').values_list('product_id',flat=True)

				if product_with_price:
					ProductCond = ProductCond.filter(id__in=product_with_price)
				if product_stock_ids:
					ProductCond = ProductCond.filter(id__in=product_stock_ids)
				
				# if search is None:
				# 	ProductCond = EngageboostProducts.objects.filter(id__in=listof_subs_product,website_id=website_id,isdeleted='n',isblocked='n')
				# else:
				# 	ProductCond = EngageboostProducts.objects.filter(id__in=listof_subs_product,website_id=website_id,isdeleted='n',isblocked='n').filter(Q(name__icontains=search)|Q(sku__icontains=search)|Q(description__icontains=search)|Q(brand__icontains=search))

				if ProductCond.count()>0:
					#**** Pagination Logic ****
					total_order = ProductCond.count()
					total_page = math.ceil(total_order/per_page)
					next_page = page+1
					current_page = page
					page = page-1
					if page > 0:					
						offset = page*per_page
					else:
						offset = 0
					limit = offset+per_page
					#**** Pagination Logic ****

					ProductCond = ProductCond.order_by('name').all()[offset:limit]

					if warehouse_id is not None:
						context = {"warehouse_id": warehouse_id}
						ProductDetails = PickerBasicinfoSerializer(ProductCond, context=context, many=True)
					else:
						ProductDetails = PickerBasicinfoSerializer(ProductCond,many=True)

					if ProductDetails:
						for product in ProductDetails.data:
							if product["weight"] is None or product["weight"] =="":
								product["weight"] = float(0)
							#**** IS SUBSTITUTE PRODUCT CHECKING ****#
							check_if_substitute = EngageboostRelatedProducts.objects.filter(product_id=product_id,related_product_id=product['id'],related_product_type=5)
							if check_if_substitute:
								product["substitute_status"] = 1
								product["substitute_message"] = "This is substitute product."
							else:
								product["substitute_status"] = 0
								product["substitute_message"] = "This is not substitute product. Do you want to add this item as substitute product?"

					data = {"status":1,"api_status":"success","response":ProductDetails.data,"total_order":total_order,"total_page":total_page,"current_page":current_page,"next_page":next_page,"per_page":per_page,"message":"Substitute has been found for this product"}
				else:
					data = {"status":0,"api_status":"error","response":[],"message":"There is no substitute for this product"}
			else:
				data = {"status":0,"api_status":"error","response":[],"message":"There is no substitute for this product"}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

class AddProductAsSubstitute(generics.ListAPIView):
	def post(self, request, format=None,many=True):
		try:
			requestdata = request.data
			checkProduct = EngageboostRelatedProducts.objects.filter(product_id=requestdata['product_id'],related_product_id=requestdata['related_product_id'],related_product_type=requestdata['related_product_type']).count()
			if checkProduct>0:
				data ={'status':1,'api_status':'success','message':'Successfully Added'}       
			else:
				serializer = RelatedProductsSerializer(data=requestdata)
				if serializer.is_valid():
					serializer.save()
					data ={'status':1,'api_status':'success','message':'Successfully Added'}
				else:
					data ={'status':0,'api_status':'error','message':serializer.errors}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

class PickerAddMoreProduct(generics.ListAPIView):
	def post(self, request, format=None):
		try:
			requestdata = request.data
			now_utc = datetime.datetime.now()
			if requestdata['website_id'] is None or requestdata['website_id'] =="":
				website_id = 1
			else:
				website_id = requestdata['website_id']
			user_id = requestdata['user_id']
			order_id = requestdata['order_id']
			warehouse_id = requestdata['warehouse_id']
			shipment_id = requestdata['shipment_id']
			trent_picklist_id 	= requestdata['trent_picklist_id']
			product_ids = requestdata['product_ids']
			product_qtys = requestdata['product_qtys']
			# if 'quantity' not in requestdata or requestdata['quantity'] is None or requestdata['quantity'] =="":
			# 	quantity = 1
			# else:
			# 	quantity = requestdata['quantity']

			if 'action' not in requestdata or requestdata['action'] is None or requestdata['action'] =="":
				action = None
			else:
				action = requestdata['action']
			
			get_order_info = EngageboostOrdermaster.objects.filter(id=order_id,website_id=website_id).first()
			get_shipment_order_info = EngageboostShipmentOrders.objects.filter(order_id=order_id,shipment=shipment_id).first()

			# print(product_ids)
			loop_count = 0
			for product_id in product_ids:
				quantity = product_qtys[loop_count]
				sub_cart_data = get_substitude_product_cart(website_id,product_id,quantity,warehouse_id)

				if sub_cart_data['weight'] is None or sub_cart_data['weight'] == "":
					weight = float(0)
				else:
					weight = float(sub_cart_data['weight'])

				new_default_price = 0
				if "new_default_price_unit" in sub_cart_data and sub_cart_data['new_default_price_unit'] > 0:
					new_default_price = sub_cart_data['new_default_price_unit']
				else :
					new_default_price = sub_cart_data['default_price']
				
				discount_price = 0
				if "discount_price_unit" in sub_cart_data and sub_cart_data['discount_price_unit'] > 0:
					discount_price = sub_cart_data['discount_price_unit']
				
				coupon = ''
				disc_type = 0
				product_discount_rate = 0
				if 'coupon' in sub_cart_data and sub_cart_data['coupon'] != '':
					coupon = sub_cart_data['coupon']
					disc_type = sub_cart_data['disc_type']
					product_discount_rate = sub_cart_data['discount_amount']

				existing_substitute_OP  = EngageboostOrderProducts.objects.filter(order_id=order_id, product_id=product_id,pick_as_substitute='n').first()

				if existing_substitute_OP:
					if action is None or action == "" or action == "increase":
						scan_quantity = int(existing_substitute_OP.quantity)+int(quantity)
					else:
						if int(existing_substitute_OP.quantity) > 0:
							scan_quantity = int(existing_substitute_OP.quantity)-int(quantity)
				else:
					scan_quantity = int(quantity)

				order_product_params = {
					"order_id":order_id,
					"product_id":product_id,
					"quantity":scan_quantity,
					# "deleted_quantity":0,
					# "substitute_product_id":0,
					"product_price":new_default_price,
					"product_price_base":new_default_price,
					"product_discount_price":discount_price,
					"product_discount_price_base":discount_price,
					"product_discount_name": coupon,
					"product_disc_type": disc_type,
					"product_discount_rate": product_discount_rate,
					"status": 0,
					"trents_picklist_id": get_order_info.trent_picklist_id,
					"cost_price": new_default_price,
					"mrp": new_default_price,
					"assign_to": get_order_info.assign_to,
					"assign_wh": get_order_info.assign_wh,
					"warehouse_id": get_order_info.assign_wh,
					# "weight":sub_cart_data['weight'],
					"weight":weight,
					"pick_as_substitute":"n",
					# "substitute_product_id":old_product_id,
					"created":now_utc
				}
				if existing_substitute_OP:					
					EngageboostOrderProducts.objects.filter(order_id=order_id, product_id=product_id,pick_as_substitute='n').update(**order_product_params)
					order_product_id = existing_substitute_OP.id
				else:
					order_product = EngageboostOrderProducts.objects.create(**order_product_params)
					order_product_id = order_product.id

				if order_product_id > 0:
					#**** SAVE IN SCANNED ORDER PRODUCT TABLE AFTER EACH SCAN ****#
					# EngageboostScannedOrderProducts.objects.create(order_product_id=order_product_id,order_id=order_id,product_id=product_id,barcode=None,quantity=int(quantity),product_old_price=new_default_price,product_new_price=new_default_price,weight=weight,product_discount_price=discount_price,product_tax_price=0,created=now_utc,modified=now_utc,is_deleted='n',is_blocked='n',pick_as_substitute='n')

					existing_substitute_SOP  = EngageboostShipmentOrderProducts.objects.filter(order_id=order_id, product_id=product_id, order_product_id=order_product_id,pick_as_substitute='n').first()
					if existing_substitute_SOP:
						if action is None or action == "" or action == "increase":
							scan_quantity = int(existing_substitute_SOP.quantity)+int(quantity)
						else:
							if int(existing_substitute_SOP.quantity) > 0:
								scan_quantity = int(existing_substitute_SOP.quantity)-int(quantity)

						shipment_order_product = {
							"shipment_order_id" : get_shipment_order_info.id,
							"shipment"			: shipment_id,
							"order_id"			: order_id,
							"product_id"		: product_id,
							"trent_picklist_id"	: trent_picklist_id,
							"order_product_id"	: order_product_id,
							"quantity"			: scan_quantity,
							# "shortage"			: 0,
							# "returns"			: 0,
							# "grn_quantity"		: 0,
							"pick_as_substitute": 'n',
							"shipment_status"	: 'Picking',
							"warehouse_id"		: get_order_info.assign_wh
						}
						EngageboostShipmentOrderProducts.objects.filter(order=order_id, product=product_id,order_product_id=order_product_id,trent_picklist_id=trent_picklist_id,pick_as_substitute='n').update(**shipment_order_product)
					else:
						scan_quantity = int(quantity)
						shipment_order_product = {
							"shipment_order_id" : get_shipment_order_info.id,
							"shipment"			: shipment_id,
							"order_id"			: order_id,
							"product_id"		: product_id,
							"trent_picklist_id"	: trent_picklist_id,
							"order_product_id"	: order_product_id,
							"quantity"			: scan_quantity,
							"shortage"			: 0,
							"returns"			: 0,
							"grn_quantity"		: 0,
							"pick_as_substitute": 'n',
							"shipment_status"	: 'Picking',
							"warehouse_id"		: get_order_info.assign_wh
						}
						EngageboostShipmentOrderProducts.objects.create(**shipment_order_product)

					if sub_cart_data['product_stock']:
						# if sub_cart_data['product_stock']['real_stock']
						# if uom is not None and uom.lower()=='kg':
						# 	if weight > 0:
						# 		shortage = float(weight)*float(scan_qty)
						if action is None or action == "" or action == "increase":
							virtual_stock = int(sub_cart_data['product_stock']['virtual_stock'])+int(quantity)
							real_stock = int(sub_cart_data['product_stock']['real_stock'])-int(quantity)
						else:
							virtual_stock = int(sub_cart_data['product_stock']['virtual_stock'])-int(quantity)
							real_stock = int(sub_cart_data['product_stock']['real_stock'])+int(quantity)

						update_stock = {
							"modified": now_utc,
							"virtual_stock":virtual_stock,
							"real_stock":real_stock
						}
						EngageboostProductStocks.objects.filter(warehouse_id=get_order_info.assign_wh,product_id=product_id).update(**update_stock)
						product_stock = common.get_product_stock(product_id)
						elastic = common.change_field_value_elastic(product_id,'EngageboostProducts',{'inventory':product_stock})

				loop_count += 1
					# Update order master data and elastic data...
			update_order_and_order_products_for_picking(order_id)

			if action is None or action == "" or action == "increase":
				data = {"status":1,"api_status":"success","message":"New product has been added"}
			else:
				data = {"status":1,"api_status":"success","message":"Product has been removed"}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

class PickerAddSubstituteProduct(generics.ListAPIView):
	def post(self, request, format=None):
		try:
			requestdata = request.data
			now_utc = datetime.datetime.utcnow()
			if requestdata['website_id'] is None or requestdata['website_id'] =="":
				website_id = 1
			else:
				website_id = requestdata['website_id']
			user_id = requestdata['user_id']
			order_id = requestdata['order_id']
			warehouse_id = requestdata['warehouse_id']
			shipment_id = requestdata['shipment_id']
			trent_picklist_id 	= requestdata['trent_picklist_id']
			product_id = requestdata['product_id']
			sub_product_ids = requestdata['sub_product_ids']
			sub_product_qtys = requestdata['sub_product_qtys']
			# if 'quantity' not in requestdata or requestdata['quantity'] is None or requestdata['quantity'] =="":
			# 	quantity = 1
			# else:
			# 	quantity = requestdata['quantity']

			if 'action' not in requestdata or requestdata['action'] is None or requestdata['action'] =="":
				action = None
			else:
				action = requestdata['action']
			
			get_order_info = EngageboostOrdermaster.objects.filter(id=order_id,website_id=website_id).first()
			get_shipment_order_info = EngageboostShipmentOrders.objects.filter(order_id=order_id,shipment=shipment_id).first()

			# print(product_ids)
			loop_count = 0
			for sub_product_id in sub_product_ids:
				quantity = sub_product_qtys[loop_count]
				sub_cart_data = get_substitude_product_cart(website_id,sub_product_id,quantity,warehouse_id)

				if sub_cart_data['weight'] is None or sub_cart_data['weight'] == "":
					weight = float(0)
				else:
					weight = float(sub_cart_data['weight'])

				new_default_price = 0
				if "new_default_price_unit" in sub_cart_data and sub_cart_data['new_default_price_unit'] > 0:
					new_default_price = sub_cart_data['new_default_price_unit']
				else :
					new_default_price = sub_cart_data['default_price']
				
				discount_price = 0
				if "discount_price_unit" in sub_cart_data and sub_cart_data['discount_price_unit'] > 0:
					discount_price = sub_cart_data['discount_price_unit']
				
				coupon = ''
				disc_type = 0
				product_discount_rate = 0
				if 'coupon' in sub_cart_data and sub_cart_data['coupon'] != '':
					coupon = sub_cart_data['coupon']
					disc_type = sub_cart_data['disc_type']
					product_discount_rate = sub_cart_data['discount_amount']

				#**** CHECK EXISTING SUBSTITUTE PRODUCT IN ORDERPRODUCT ****#
				# existing_substitute_OP  = EngageboostOrderProducts.objects.filter(order_id=order_id, product_id=sub_product_id,pick_as_substitute='y').first()
				# existing_substitute_OP  = EngageboostOrderProducts.objects.filter(order_id=order_id, product_id=sub_product_id,substitute_product_id=product_id,pick_as_substitute='y').first()
				existing_substitute_OP = EngageboostOrderSubstituteProducts.objects.filter(order_id=order_id, product_id=sub_product_id,substitute_product_id=product_id,pick_as_substitute='y').first()

				if existing_substitute_OP:
					if action is None or action == "" or action == "increase":
						# scan_quantity = int(existing_substitute_OP.quantity)+int(quantity)
						scan_quantity = int(quantity)
					else:
						if int(existing_substitute_OP.quantity) > 0:
							scan_quantity = int(existing_substitute_OP.quantity)-int(quantity)
						else:
							scan_quantity = 0
				else:
					scan_quantity = int(quantity)

				order_product_params = {
					"order_id":order_id,
					"product_id":sub_product_id,
					"quantity":scan_quantity,
					# "grn_quantity":scan_quantity,
					# "deleted_quantity":0,
					# "substitute_product_id":0,
					"product_price":new_default_price,
					# "product_price_base":new_default_price,
					"product_discount_price":discount_price,
					# "product_discount_price_base":discount_price,
					"product_discount_name": coupon,
					"product_disc_type": disc_type,
					"product_discount_rate": product_discount_rate,
					# "status": 0,
					# "trents_picklist_id": get_order_info.trent_picklist_id,
					# "cost_price": new_default_price,
					# "mrp": new_default_price,
					# "assign_to": get_order_info.assign_to,
					# "assign_wh": get_order_info.assign_wh,
					"warehouse_id": get_order_info.assign_wh,
					# "weight":sub_cart_data['weight'],
					"weight":weight,
					"pick_as_substitute":"y",
					"substitute_product_id":product_id,
					"created":now_utc
				}
				if existing_substitute_OP:					
					# EngageboostOrderProducts.objects.filter(order_id=order_id, product_id=sub_product_id,pick_as_substitute='y').update(**order_product_params)
					order_product_id = existing_substitute_OP.id
					# EngageboostOrderProducts.objects.filter(id=order_product_id).update(**order_product_params)
					EngageboostOrderSubstituteProducts.objects.filter(id=order_product_id).update(**order_product_params)
				else:
					# order_product = EngageboostOrderProducts.objects.create(**order_product_params)
					order_product = EngageboostOrderSubstituteProducts.objects.create(**order_product_params)
					order_product_id = order_product.id

				#**** CHECK EXISTING MAIN PRODUCT IN ORDERPRODUCT ****#
				# existing_main_OP  = EngageboostOrderProducts.objects.filter(order_id=order_id, product_id=product_id,pick_as_substitute='n').first()
				# if existing_main_OP:
				# 	if action is None or action == "" or action == "increase":
				# 		main_product_shortage = int(existing_main_OP.shortage)+int(quantity)
				# 	else:
				# 		if int(existing_main_OP.shortage) > 0:
				# 			main_product_shortage = int(existing_main_OP.shortage)-int(quantity)
				# else:
				# 	main_product_shortage = int(quantity)
				# main_order_product_params = {"shortage":main_product_shortage}
				# EngageboostOrderProducts.objects.filter(order_id=order_id, product_id=product_id,pick_as_substitute='n').update(**main_order_product_params)

				if order_product_id > 0:
					#**** SAVE IN SCANNED ORDER PRODUCT TABLE AFTER EACH SCAN ****#
					# EngageboostScannedOrderProducts.objects.create(order_product_id=order_product_id,order_id=order_id,product_id=sub_product_id,barcode=None,quantity=int(quantity),product_old_price=new_default_price,product_new_price=new_default_price,weight=weight,product_discount_price=discount_price,product_tax_price=0,created=now_utc,modified=now_utc,is_deleted='n',is_blocked='n',pick_as_substitute='y')

					#**** CHECK EXISTING SUBSTITUTE PRODUCT IN SHIPMENTORDERPRODUCT ****#
					# existing_substitute_SOP  = EngageboostShipmentOrderProducts.objects.filter(order_id=order_id, product_id=sub_product_id, order_product_id=order_product_id, pick_as_substitute='y').first()
					# if existing_substitute_SOP:
					# 	if action is None or action == "" or action == "increase":
					# 		scan_quantity = int(existing_substitute_SOP.quantity)+int(quantity)
					# 	else:
					# 		if int(existing_substitute_SOP.quantity) > 0:
					# 			scan_quantity = int(existing_substitute_SOP.quantity)-int(quantity)

					# 	shipment_order_product = {
					# 		"shipment_order_id" : get_shipment_order_info.id,
					# 		"shipment"			: shipment_id,
					# 		"order_id"			: order_id,
					# 		"product_id"		: sub_product_id,
					# 		"trent_picklist_id"	: trent_picklist_id,
					# 		"order_product_id"	: order_product_id,
					# 		"quantity"			: scan_quantity,
					# 		# "shortage"			: 0,
					# 		# "returns"			: 0,
					# 		# "grn_quantity"		: 0,
					# 		"pick_as_substitute": 'y',
					# 		"shipment_status"	: 'Picking',
					# 		"warehouse_id"		: get_order_info.assign_wh
					# 	}
					# 	EngageboostShipmentOrderProducts.objects.filter(order=order_id, product=sub_product_id,order_product_id=order_product_id,trent_picklist_id=trent_picklist_id,pick_as_substitute='y').update(**shipment_order_product)
					# else:
					# 	scan_quantity = int(quantity)
					# 	shipment_order_product = {
					# 		"shipment_order_id" : get_shipment_order_info.id,
					# 		"shipment"			: shipment_id,
					# 		"order_id"			: order_id,
					# 		"product_id"		: sub_product_id,
					# 		"trent_picklist_id"	: trent_picklist_id,
					# 		"order_product_id"	: order_product_id,
					# 		"quantity"			: scan_quantity,
					# 		"shortage"			: 0,
					# 		"returns"			: 0,
					# 		"grn_quantity"		: 0,
					# 		"pick_as_substitute": 'y',
					# 		"shipment_status"	: 'Picking',
					# 		"warehouse_id"		: get_order_info.assign_wh
					# 	}
					# 	EngageboostShipmentOrderProducts.objects.create(**shipment_order_product)

					#**** CHECK EXISTING MAIN PRODUCT IN SHIPMENTORDERPRODUCT ****#
					# existing_main_SOP  = EngageboostShipmentOrderProducts.objects.filter(order_id=order_id, product_id=product_id, pick_as_substitute='n').first()
					# if existing_main_SOP:
					# 	if action is None or action == "" or action == "increase":
					# 		main_product_shortage = int(existing_main_SOP.shortage)+int(quantity)
					# 	else:
					# 		if int(existing_main_SOP.shortage) > 0:
					# 			main_product_shortage = int(existing_main_SOP.shortage)-int(quantity)
					# else:
					# 	main_product_shortage = int(quantity)
					# main_shipment_order_product_params = {"shortage":main_product_shortage}
					# EngageboostShipmentOrderProducts.objects.filter(order_id=order_id, product_id=product_id,pick_as_substitute='n').update(**main_shipment_order_product_params)

					#**** PRODUCT STOCK ADJUSTMENT ****#
					if sub_cart_data['product_stock']:
						# if sub_cart_data['product_stock']['real_stock']
						# if uom is not None and uom.lower()=='kg':
						# 	if weight > 0:
						# 		shortage = float(weight)*float(scan_qty)
						if action is None or action == "" or action == "increase":
							virtual_stock = int(sub_cart_data['product_stock']['virtual_stock'])+int(quantity)
							real_stock = int(sub_cart_data['product_stock']['real_stock'])-int(quantity)
						else:
							virtual_stock = int(sub_cart_data['product_stock']['virtual_stock'])-int(quantity)
							real_stock = int(sub_cart_data['product_stock']['real_stock'])+int(quantity)

						update_stock = {
							"modified": now_utc,
							"virtual_stock":virtual_stock,
							"real_stock":real_stock
						}
						EngageboostProductStocks.objects.filter(warehouse_id=get_order_info.assign_wh,product_id=sub_product_id).update(**update_stock)
						product_stock = common.get_product_stock(sub_product_id)
						elastic = common.change_field_value_elastic(sub_product_id,'EngageboostProducts',{'inventory':product_stock})

				loop_count += 1
			#**** Update order master data and elastic data ****#
			update_order_and_order_products_for_picking(order_id)

			if action is None or action == "" or action == "increase":
				data = {"status":1,"api_status":"success","message":"Substitute product has been added"}
			else:
				data = {"status":1,"api_status":"success","message":"Substitute product has been removed"}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

class PickerSendApproval(generics.ListAPIView):
	def post(self,request):
		try:
			requestdata = request.data
			now_utc = datetime.datetime.utcnow()
			if requestdata['website_id'] is None or requestdata['website_id'] =="":
				website_id = 1
			else:
				website_id = requestdata['website_id']
			user_id = requestdata['user_id']
			order_id = requestdata['order_id']
			warehouse_id = requestdata['warehouse_id']
			# shipment_id = requestdata['shipment_id']
			# trent_picklist_id 	= requestdata['trent_picklist_id']
			approval_details = requestdata['approval_details']
			if 'approval_details' in requestdata and requestdata['approval_details']:
				for approval_details in requestdata['approval_details']:
					sub_product_id = approval_details['product_id']
					order_product_id = approval_details['order_product_id']
					order_product_params = {
						"send_approval":"pending",
						"created":now_utc
					}
					# EngageboostOrderProducts.objects.filter(order_id=order_id, product_id=sub_product_id,id=order_product_id,pick_as_substitute='y').update(**order_product_params)
					EngageboostOrderSubstituteProducts.objects.filter(order_id=order_id, product_id=sub_product_id,id=order_product_id,pick_as_substitute='y').update(**order_product_params)

				#----Binayak Start----#
				common.notification_send_by_AutoResponder(order_id, 30)
				common.email_send_by_AutoResponder(order_id, 30)
				# ----Binayak End----#
				
				data = {"status":1,"api_status":"success","response":"Approval sent to the customer.","message":"Approval sent to the customer."}
			else:
				data = {"status":0,"api_status":"error","response":[],"message":"Invalid return request."}
			# update_order_and_order_products_for_picking(order_id)
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((AllowAny, ))
class PickerAcceptApproval(generics.ListAPIView):
	def post(self,request):
		try:
			requestdata = request.data
			# now_utc = datetime.datetime.utcnow()
			# now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
			# nowdate = str(now_utc)
			now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
			then_utc = now_utc - datetime.timedelta(minutes=10)
			thendate = str(then_utc)

			if requestdata['website_id'] is None or requestdata['website_id'] =="":
				website_id = 1
			else:
				website_id = requestdata['website_id']
			
			order_id = requestdata['order_id']

			if 'user_id' not in requestdata or requestdata['user_id'] is None or requestdata['user_id'] =="":
				user_id = None
			else:
				user_id = requestdata['user_id']
			
			# if 'product_id' not in requestdata and requestdata['product_id'] is None or requestdata['product_id'] =="":
			# 	product_id = None
			# else:
			# 	product_id = requestdata['product_id']
			
			# warehouse_id = requestdata['warehouse_id']
			# shipment_id = requestdata['shipment_id']
			# trent_picklist_id 	= requestdata['trent_picklist_id']
			api_respon = []

			# main_order_product_params = {"created":now_utc,"send_approval":"declined"}
			# EngageboostOrderProducts.objects.filter(order_id=order_id,pick_as_substitute='y').update(**main_order_product_params)
			get_order_info = EngageboostOrdermaster.objects.filter(id=order_id,website_id=website_id).first()

			if 'approval_details' in requestdata and requestdata['approval_details']:
				accepted_substitiutes = []
				for approval_details in requestdata['approval_details']:
					accepted_substitiutes.append(approval_details['order_product_id'])
					product_id = approval_details['product_id']
					substitute_product_id = approval_details['substitute_product_id']
					order_product_id = approval_details['order_product_id']
					# ord_prd_details = EngageboostOrderProducts.objects.filter(order_id=order_id, product_id=substitute_product_id,id=order_product_id,pick_as_substitute='y').first()
					ord_prd_details = EngageboostOrderSubstituteProducts.objects.filter(order_id=order_id, product_id=substitute_product_id,id=order_product_id,pick_as_substitute='y').first()

					if thendate <= str(ord_prd_details.created):						
						quantity = approval_details['quantity']
						grn_quantity = approval_details['grn_quantity']
						# subs_shortage = quantity-grn_quantity
						if grn_quantity == 0 or grn_quantity == "":
							grn_quantity = 0
							send_approval_status = "declined"
						else:
							send_approval_status = "approve"
						if quantity >= grn_quantity:
							pass
						else:
							quantity = grn_quantity

						order_product_params = {
							"quantity":quantity,
							"grn_quantity": grn_quantity,
							"send_approval": send_approval_status,
							"created":now_utc
						}
						# EngageboostOrderProducts.objects.filter(order_id=order_id, product_id=substitute_product_id,id=order_product_id,pick_as_substitute='y').update(**order_product_params)
						EngageboostOrderSubstituteProducts.objects.filter(order_id=order_id, product_id=substitute_product_id,id=order_product_id,pick_as_substitute='y').update(**order_product_params)

						if send_approval_status == "approve":
							#**** INSERT IN ORDER PRODUCT TABLE ****#
							existing_substitute_OP = EngageboostOrderSubstituteProducts.objects.filter(order_id=order_id, product_id=substitute_product_id,id=order_product_id,pick_as_substitute='y').first()

							custom_field_name = custom_field_value = None
							if 'custom_field_name' in approval_details:
								custom_field_name = approval_details['custom_field_name']
							if 'custom_field_value' in approval_details:
								custom_field_value = approval_details['custom_field_value']
							insert_order_product_params = {
								"order_id": order_id,
								"product_id": substitute_product_id,
								"quantity": quantity,
								"grn_quantity": grn_quantity,
								# "deleted_quantity":0,
								"product_price": existing_substitute_OP.product_price,
								"product_price_base": existing_substitute_OP.product_price,
								"product_discount_price": existing_substitute_OP.product_discount_price,
								"product_discount_price_base": existing_substitute_OP.product_discount_price,
								"product_discount_name": existing_substitute_OP.product_discount_name,
								"product_disc_type": existing_substitute_OP.product_disc_type,
								"product_discount_rate": existing_substitute_OP.product_discount_rate,
								# "status": 0,
								"trents_picklist_id": get_order_info.trent_picklist_id,
								"cost_price": existing_substitute_OP.product_price,
								"mrp": existing_substitute_OP.product_price,
								"assign_to": get_order_info.assign_to,
								"assign_wh": get_order_info.assign_wh,
								"warehouse_id": existing_substitute_OP.warehouse_id,
								"weight": existing_substitute_OP.weight,
								"pick_as_substitute": "y",
								"substitute_product_id": existing_substitute_OP.substitute_product_id,
								"send_approval": send_approval_status,
								"custom_field_name": custom_field_name,
								"custom_field_value": custom_field_value,
								"created": now_utc
							}
							EngageboostOrderProducts.objects.create(**insert_order_product_params)
							#**** INSERT IN ORDER PRODUCT TABLE ****#
						api_respon.append('success')
					else:
						api_respon.append('error')
				
				#**** DECLINED ALL PENDING PRODUCTS ****#
				reset_params = {"send_approval":"declined","created":now_utc}
				EngageboostOrderSubstituteProducts.objects.filter(Q(order_id=order_id,substitute_product_id=product_id,pick_as_substitute='y')).filter(~Q(id__in=accepted_substitiutes)).update(**reset_params)
				#**** DECLINED ALL PENDING PRODUCTS ****#
				
				if 'error' in api_respon:
					data = {"status":0,"api_status":"error","response":[],"message":"Your request time has been expired."}
				else:
					data = {"status":1,"api_status":"success","response":{"order_id":order_id},"message":"Your order has been updated"}

				update_order_and_order_products_for_picking(order_id)
			else:
				data = {"status":0,"api_status":"error","response":[],"message":"Invalid return request."}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((AllowAny, ))
class PickerResetSendApproval(generics.ListAPIView):
	def post(self,request):
		try:
			requestdata = request.data
			now_utc = datetime.datetime.utcnow()
			if 'website_id' in requestdata and requestdata['website_id'] is None or requestdata['website_id'] =="":
				website_id = 1
			else:
				website_id = requestdata['website_id']
			# user_id = requestdata['user_id']
			order_id = requestdata['order_id']
			# warehouse_id = requestdata['warehouse_id']

			reset_params = {"created":now_utc,"send_approval":"declined"}
			# EngageboostOrderProducts.objects.filter(Q(order_id=order_id,pick_as_substitute='y')).filter(~Q(send_approval="approve")).update(**reset_params)
			EngageboostOrderSubstituteProducts.objects.filter(Q(order_id=order_id,pick_as_substitute='y')).filter(~Q(send_approval="approve")).update(**reset_params)
			data = {"status":1,"api_status":"success","response":"All the substitute product has been declined","message":"All the substitute product has been declined"}
			#----Binayak Start----#
			# common.notification_send_by_AutoResponder(order_id, 30)
			# ----Binayak End----#
			# update_order_and_order_products_for_picking(order_id)
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

class PickerPicklistProductInfo(generics.ListAPIView):
	def post(self,request):
		requestdata = request.data
		try:
			now_utc = datetime.datetime.now()
			if requestdata['website_id'] is None or requestdata['website_id'] =="":
				website_id = 1
			else:
				website_id = requestdata['website_id']
			user_id = requestdata['user_id']
			order_id = requestdata['order_id']
			# warehouse_id = requestdata['warehouse_id']
			# shipment_id = requestdata['shipment_id']
			# trent_picklist_id 	= requestdata['trent_picklist_id']
			product_id = requestdata['product_id']
			order_product_id = requestdata['order_product_id']

			order_product_cond  = EngageboostOrderProducts.objects.filter(id=order_product_id,order_id=order_id, product_id=product_id).first()
			if order_product_cond and product_id > 0:
				order_product = OrderProductsSerializer(order_product_cond, partial=True)
				order_product = order_product.data
				# warehouse_id = order_product.data["warehouse_id"]
				if order_product:
					if order_product['assign_wh']:
						warehouse_id = order_product['assign_wh']
					if 'cost_price' in order_product:		
						order_product['cost_price'] = float("{:.2f}".format(order_product['cost_price']))
					if 'mrp' in order_product:
						order_product['mrp'] = float("{:.2f}".format(order_product['mrp']))
					if 'product_price' in order_product:
						order_product['product_price'] = float("{:.2f}".format(order_product['product_price']))
					if 'product_price_base' in order_product:
						order_product['product_price_base'] = float("{:.2f}".format(order_product['product_price_base']))				
				
				data = {"status":1,"api_status":"success","response": order_product,"message":"Product details has been found."}
			else:
				data = {"status":0,"api_status":"error","response":[],"message":"Data not found."}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

class PickerUpdatePicklistProductInfo(generics.ListAPIView):
	def post(self,request):
		try:
			requestdata = request.data
			now_utc = datetime.datetime.now()
			website_id 			= requestdata['website_id']
			order_id            = requestdata['order_id']
			user_id 			= requestdata['user_id']
			user_name 		   	= requestdata['user_name']
			product_id          = requestdata['product_id']
			product_sku         = requestdata['sku']
			order_product_id 	= requestdata['order_product_id']
			product_old_price   = requestdata['product_old_price']
			product_new_price   = requestdata['product_new_price']
			product_new_price   = requestdata['product_new_price']
			# pick_as_substitute 	= requestdata['pick_as_substitute']
			
			if 'weight' not in requestdata or requestdata['weight'] is None or requestdata['weight'] == "":
				weight = None
			else:
				weight = requestdata['weight']

			if 'notes' in requestdata:
				notes = requestdata['notes']
			else:
				notes = ""

			product_old_price = float(product_old_price)
			product_new_price = float(product_new_price)
			if product_old_price > 0 and product_new_price > 0:
				#**** Update Order Products ****#
				if weight:
					EngageboostOrderProducts.objects.filter(id=order_product_id,order_id=order_id,product_id=product_id).update(product_price=product_new_price,product_price_base=product_new_price,weight=weight,substitute_notes=notes)
				else:
					EngageboostOrderProducts.objects.filter(id=order_product_id,order_id=order_id,product_id=product_id).update(product_price=product_new_price,product_price_base=product_new_price,substitute_notes=notes)

				#**** order activity ****#
				order_activities_str = user_name+'</b> has changed the price for product '+product_sku+' from '+str(product_old_price)+' to '+str(product_new_price)
				order_activities_str+= '<br/>'+ notes
				common.save_order_activity("",order_id,None,7,order_activities_str,user_id,1)

				#**** SAVE IN SCANNED ORDER PRODUCT TABLE AFTER EACH SCAN ****#
				# EngageboostScannedOrderProducts.objects.filter(order_product_id=order_product_id,order_id=order_id,product_id=product_id,is_deleted='n',is_blocked='n').update(product_old_price=product_old_price,product_new_price=product_new_price,weight=weight,modified=now_utc)
				if weight:
					return_data	= {"product_old_price":product_old_price,"product_new_price":product_new_price,"weight":weight}
				else:
					return_data	= {"product_old_price":product_old_price,"product_new_price":product_new_price}
				update_order_and_order_products_for_picking(order_id)
				data = {
					"status":1,
					"api_status" : "success",
					"response" : return_data,
					"message":"Product price and weight changes successfully."
				}
			else:
				data = {
					"status":1,
					"api_status" : "success",
					"response" : {},
					"message":"No changes have been made."
				}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"response":{},"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)
				
class PickerGrnComplete(generics.ListAPIView):
	def post(self,request):
		try:
			requestdata = request.data			
			now_utc = datetime.datetime.utcnow()
			total_quantity = total_scan_quantity = 0
			if requestdata['website_id'] is None or requestdata['website_id'] =="":
				website_id = 1
			else:
				website_id = requestdata['website_id']
			user_id 			= requestdata['user_id']
			order_id 			= requestdata['order_id']
			warehouse_id 		= requestdata['warehouse_id']
			shipment_id 		= requestdata['shipment_id']
			trent_picklist_id 	= requestdata['trent_picklist_id']
			invoice_prefix 		= 'INV'
			manifest_prefix 	= 'MNF#'
			# order_arr   = requestdata['response']['shipmentProducts']
			globalsettings = EngageboostGlobalSettings.objects.filter(website_id=website_id,isblocked='n',isdeleted='n').first()
			if globalsettings:
				if globalsettings.invoice_id_format is None or globalsettings.invoice_id_format == "": 
					invoice_prefix = 'INV'
				else:
					invoice_prefix = globalsettings.invoice_id_format

			reset_params = {"send_approval":"declined"}
			EngageboostOrderSubstituteProducts.objects.filter(Q(order_id=order_id,pick_as_substitute='y')).filter(~Q(send_approval="approve")).update(**reset_params)

			update_order_and_order_products_for_picking(order_id)
			
			ordermasterdetails = EngageboostOrdermaster.objects.filter(id=order_id,website_id=website_id).first()
			order_product_cond  = EngageboostOrderProducts.objects.filter(order_id=order_id,quantity__gt=0).all()
			if order_product_cond:
				get_shipment_order_info = EngageboostShipmentOrders.objects.filter(order_id=order_id,shipment=shipment_id).first()
				excise_duty = ordermasterdetails.excise_duty
				gross_amount = ordermasterdetails.gross_amount
				net_amount = ordermasterdetails.net_amount
				paid_amount = ordermasterdetails.paid_amount

				#**** Generate Invoice *****#
				hasInvoice = EngageboostInvoicemaster.objects.filter(shipment_id=shipment_id,order_id=order_id).first()
				if hasInvoice:
					invoice_id = hasInvoice.id
				else:

					# ------Binayak Start-----#
					final_payment_response = {}
					rs_order_master = EngageboostOrdermaster.objects.filter(id=order_id).first()
					if rs_order_master and rs_order_master.payment_type_id == 2 and rs_order_master.payment_method_id == 51:
						if rs_order_master.paid_amount <= 0:
							payment_response = payment_request_si_charge_si(order_id)
							if payment_response['status'] == 'failed':
								final_payment_response = {'status': payment_response['status'],
														  'msg': "Please wait for 30 minutes from order creation",
														  'msg_1': payment_response['msg'],
														  'si_ref_no': payment_response['si_ref_no'],
														  'pay_txntranid': payment_response['pay_txntranid']}
							else:
								final_payment_response = {'status': payment_response['status'],
														  'msg': payment_response['msg'],
														  'msg_1': payment_response['msg']}
						else:
							final_payment_response = {'status': 'error', 'msg': "Payment Already Done"}
					else:
						final_payment_response = {'status': 'success', 'msg': "Offline payment"}

					if final_payment_response['status'] == 'success':
					# ----Binayak End----#
						Invoicemaster = EngageboostInvoicemaster.objects.create(website_id = website_id,custom_order_id = ordermasterdetails.custom_order_id,customer_id = ordermasterdetails.customer_id,webshop_id = ordermasterdetails.webshop_id,warehouse_id = warehouse_id,isblocked = 'n',isdeleted = 'n',order_id = order_id,trent_picklist_id = trent_picklist_id,created = now_utc.date(),modified = now_utc.date(),gross_amount = gross_amount,net_amount = net_amount,paid_amount = paid_amount,excise_duty = excise_duty,shipment_id = shipment_id)
						invoice_id = Invoicemaster.id
						invoice_id_no = invoice_prefix+str(invoice_id)
						EngageboostInvoicemaster.objects.filter(id=invoice_id).update(custom_invoice_id=invoice_id_no)
				#**** Generate Invoice *****#

						order_product = OrderProductsSerializer(order_product_cond, many=True)
						for shipmentProducts in order_product.data:
							if shipmentProducts['pick_as_substitute'] == 'n' or (shipmentProducts['pick_as_substitute'] == 'y' and shipmentProducts['send_approval'] == 'approve'):
								# shipment_order_product_id   = shipmentProducts['id']
								pick_as_substitute =  shipmentProducts['pick_as_substitute']
								order_product_id = shipmentProducts['id']
								product_price = shipmentProducts['product_price']
								warehouse_id = warehouse_id if shipmentProducts['warehouse_id'] is None or shipmentProducts['warehouse_id'] =="" else shipmentProducts['warehouse_id']
								product_id = shipmentProducts['product']['id']
								quantity = shipmentProducts['quantity']
								shortage = 0 if shipmentProducts['shortage'] is None or shipmentProducts['shortage'] =="" else shipmentProducts['shortage']
								deleted_quantity = 0 if shipmentProducts['deleted_quantity'] is None or shipmentProducts['deleted_quantity'] =="" else shipmentProducts['deleted_quantity']
								grn_quantity = quantity-(shortage+deleted_quantity)
								total_quantity = total_quantity+quantity
								total_scan_quantity = total_scan_quantity+grn_quantity
								product_weight = float(0) if shipmentProducts['weight'] is None or shipmentProducts['weight'] =="" else shipmentProducts['weight']

								update_shipment_order_product = {
									"shortage":shortage,
									"grn_quantity":grn_quantity,
									# "shipment_status":"Invoicing"
									"shipment_status":"Shipped"
								}
								# EngageboostShipmentOrderProducts.objects.filter(shipment=shipment_id,order_id=order_id, product_id=product_id,order_product_id=order_product_id).update(**update_shipment_order_product)

								#**** INSERT IN SHIPMENT ORDER PRODUCT ****#
								existing_substitute_SOP  = EngageboostShipmentOrderProducts.objects.filter(shipment=shipment_id,order_id=order_id, product_id=product_id, order_product_id=order_product_id).first()
								
								if existing_substitute_SOP:
									EngageboostShipmentOrderProducts.objects.filter(shipment=shipment_id,order_id=order_id, product_id=product_id,order_product_id=order_product_id).update(**update_shipment_order_product)
								else:
									shipment_order_product = {
										"shipment_order_id" : get_shipment_order_info.id,
										"shipment"			: shipment_id,
										"order_id"			: order_id,
										"product_id"		: product_id,
										"order_product_id"	: order_product_id,
										"trent_picklist_id"	: trent_picklist_id,									
										"quantity"			: quantity,
										"shortage"			: shortage,
										"returns"			: 0,
										"grn_quantity"		: grn_quantity,
										"pick_as_substitute": pick_as_substitute,
										"shipment_status"	: 'Shipped',
										"warehouse_id"		: warehouse_id
									}
									EngageboostShipmentOrderProducts.objects.create(**shipment_order_product)
								#**** INSERT IN SHIPMENT ORDER PRODUCT ****#

								EngageboostOrderProducts.objects.filter(order_id=order_id,product_id=product_id,id=order_product_id).update(shortage=shortage,grn_quantity=grn_quantity)

								#**** Insert in Invoice Product ****#
								hasInvoiceProduct = EngageboostInvoiceProducts.objects.filter(order_id=order_id, product_id=product_id,invoice_id=invoice_id).first()
								if hasInvoiceProduct:
									# updated_grn_quantity = int(hasInvoiceProduct.quantity)+int(grn_quantity)
									EngageboostInvoiceProducts.objects.filter(order_id=order_id, product_id=product_id,invoice_id=invoice_id).update(quantity=grn_quantity,price=product_price)
								else:
									EngageboostInvoiceProducts.objects.create(order_id=order_id, product_id=product_id,invoice_id=invoice_id,quantity=grn_quantity,price=product_price)
								#**** Insert in Invoice Product ****#
							else:
								pass
						order_ids = str(order_id)
						order_idsArr = order_ids.split(",")
						totalVechicle = create_automatic_delivery_plan(order_idsArr, shipment_id, warehouse_id)
						EngageboostShipments.objects.filter(id=shipment_id).update(no_of_vehicles=totalVechicle)

						#**** Insert in Delivery Planner ****#
						hasDeliveryPlanner = EngageboostDeliveryPlanOrder.objects.filter(order_id=order_id,shipment_id=shipment_id).first()
						if hasDeliveryPlanner:
							EngageboostDeliveryPlanOrder.objects.filter(order_id=order_id,shipment_id=shipment_id).update(orders=1,modified=now_utc)
						else:
							EngageboostDeliveryPlanOrder.objects.create(order_id=order_id, orders=1,shipment_id=shipment_id,created=now_utc,modified=now_utc)
							# EngageboostDeliveryPlanOrder.objects.create(order_id=order_id, orders=1,shipment_id=shipment_id,created=now_utc,modified=now_utc,distance="",time="",virtual_vechile_id="")
						#**** Insert in Delivery Planner ****#

						#**** Insert in Maniest ****#
						hasManifests = EngageboostManifests.objects.filter(order_id=order_id,shipment_id=shipment_id).first()
						if hasManifests:
							manifest_id = hasManifests.id
							manifest_id_no = hasManifests.manifest_no
							EngageboostManifests.objects.filter(id=manifest_id).update(modified=now_utc)
						else:
							has_mnf_record = EngageboostManifests.objects.last()
							if has_mnf_record:
								last_mnf_entry = EngageboostManifests.objects.order_by("-id").latest("id")
								manifest_no = last_mnf_entry.manifest_no
								manifest_no_arr = manifest_no.split("#")
								row_id = int(manifest_no_arr[1])+int(1)
								manifest_id_no = manifest_prefix+str(row_id)
							else:
								row_id = 1
								manifest_id_no = manifest_prefix+str(row_id)

							Manifests = EngageboostManifests.objects.create(manifest_no=manifest_id_no,order_id=order_id,shipment_id=shipment_id,comment="Manifest created successfully",created=now_utc,modified=now_utc,isblocked='n',isdeleted='n')
							manifest_id = Manifests.id
							# manifest_id_no = manifest_prefix+str(manifest_id)
							# EngageboostManifests.objects.filter(id=manifest_id).update(manifest_no=manifest_id_no)
						#**** Insert in Maniest ****#

						#**** Update Status in Shipment Order ****#
						# update_shipment_order = {"no_of_crates":1,"shipment_status":"Invoicing","total_quantity":total_scan_quantity}
						update_shipment_order = {"no_of_crates":1,"shipment_status":"Shipped","total_quantity":total_scan_quantity}
						EngageboostShipmentOrders.objects.filter(order_id=order_id,shipment=shipment_id).update(**update_shipment_order)
						#**** Update Status in Shipment Order ****#

						if user_id > 0:
							common.save_order_activity('',order_id,None,7,"Order is Invoicing",user_id,1)
							common.save_order_activity('',order_id,None,7,"Shipment Processing",user_id,1)
							common.save_order_activity('',order_id,None,7,"Ready to Ship",user_id,1)
							common.save_order_activity('',order_id,None,7,"Order is Shipped",user_id,1)
						EngageboostOrdermaster.objects.filter(id=order_id,shipment_id=shipment_id).update(grn_created_date=now_utc,flag_order=1,order_status=1)

						#**** Update Shipment Status ****#
						allshipmentOrder = EngageboostShipmentOrders.objects.filter(shipment=shipment_id).exclude(shipment_status='Shipped').count()
						if allshipmentOrder == 0:
							EngageboostShipments.objects.filter(id=shipment_id).update(shipment_status='Shipped',modified=now_utc)
							EngageboostTrentPicklists.objects.filter(id=trent_picklist_id).update(picklist_status='Shipped')
						#**** Update Shipment Status ****#

						# allshipmentOrder = EngageboostShipmentOrders.objects.filter(shipment=shipment_id, shipment_status__in=['Picking']).all()
						# if len(allshipmentOrder)>0:
						# 	pass
						# else:
						# 	EngageboostShipments.objects.filter(id=shipment_id).update(shipment_status='Invoicing')
						# 	EngageboostTrentPicklists.objects.filter(id=trent_picklist_id).update(picklist_status='Invoicing')

						elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'order_status':'1','shipping_status':'Shipped'})
						update_order_and_order_products(order_id)

						#**** Update Order Gross Amount Changed by picker****#
						rs_oder = EngageboostOrdermaster.objects.filter(id=order_id).values('id','gross_amount','gross_amount_base','net_amount','net_amount_base','order_amount','order_net_amount').first()
						old_gross_amount = rs_oder["gross_amount"]
						old_net_amount = rs_oder["net_amount"]
						old_order_amount = rs_oder["order_amount"]
						old_order_net_amount = rs_oder["order_net_amount"]
						if old_order_amount:
							gross_amount = rs_oder["order_amount"]
							net_amount = rs_oder["order_net_amount"]
							order_amount = rs_oder["gross_amount"]
							order_net_amount = rs_oder["net_amount"]
							shipped_save_order = {
								"gross_amount":gross_amount,
								"gross_amount_base":gross_amount,
								"net_amount":net_amount,
								"net_amount_base":net_amount,
								"order_amount":order_amount,
								"order_net_amount":order_net_amount
							}
							EngageboostOrdermaster.objects.filter(id=order_id).update(**shipped_save_order)
						#**** Update Order Gross Amount Changed by picker****#

						# **** Shortage product marked as Out of Stock ****#
						shortage_products = EngageboostOrderProducts.objects.filter(order_id=order_id,
																					shortage__gt=0).values_list(
							'product_id', flat=True)
						for shortage_product_id in shortage_products:
							EngageboostProductStocks.objects.filter(product_id=shortage_product_id,
																	warehouse_id=warehouse_id).update(stock=0,
																									  real_stock=0)
							EngageboostUpdateQueue.objects.create(product_id=shortage_product_id,
																  process_type='single',
																  operation_for='inventory',
																  warehouse_id=warehouse_id)
						# **** Shortage product marked as Out of Stock ****#

					# -----Binayak Start----#
						data = {"status": 1, "api_status": "success",
								"message": "The order has been processed successfully."}

						if rs_order_master and rs_order_master.payment_type_id == 2 and rs_order_master.payment_method_id == 51:
							# common.email_send_by_AutoResponder(order_id, 29)
							common.sms_send_by_AutoResponder(order_id, '', 29, '')

						common.notification_send_by_AutoResponder(order_id, 29)

					elif final_payment_response['status'] in ('failed', 'error'):
						data = {"status": 0, "api_status": "error", "message": final_payment_response['msg']}
						# -----Binayak End----#
			else:
				data = {"status":0,"api_status":"error","message":"Order Products not found."}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"response":[],"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

class PickerUpdateGrnQuantity(generics.ListAPIView):
	def post(self,request):
		try:
			requestdata = request.data
			now_utc = datetime.datetime.now()
			website_id 			= requestdata['website_id']
			user_id 			= requestdata['user_id']
			order_id            = requestdata['order_id']			
			product_id          = requestdata['product_id']
			order_product_id 	= requestdata['order_product_id']
			grn_quantity 		= requestdata['grn_quantity']
			shortage   			= requestdata['shortage']
			
			#**** Update Order Products ****#
			EngageboostOrderProducts.objects.filter(id=order_product_id,order_id=order_id,product_id=product_id).update(grn_quantity=grn_quantity,shortage=shortage)
			EngageboostShipmentOrderProducts.objects.filter(order_product_id=order_product_id,order_id=order_id,product_id=product_id).update(grn_quantity=grn_quantity,shortage=shortage)
			update_order_and_order_products_for_picking(order_id)
			
			orderlistcond = EngageboostOrdermaster.objects.filter(id=order_id).values("gross_amount","net_amount","tax_amount","shipping_cost","gross_discount_amount","cart_discount","pay_wallet_amount","refund_wallet_amount","paid_amount").first()
			if orderlistcond:
				order_details = orderlistcond
			else:
				order_details = []
				
			data = {"status":1,"api_status" : "success","response" : {"grn_quantity":grn_quantity,"shortage":shortage,"order_details":order_details},"message":"GRN Quantity and Shortage has been updated."}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"response":{},"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

def get_substitude_product_cart(website_id,product_id,quantity,warehouse_id=None):
	getproductforcart_net= {};
	if product_id > 0 and quantity > 0:
		checkout_info = {"product_id":product_id,"quantity":quantity}
		discount_array = common.generate_discount_conditions(website_id, None, None, warehouse_id)
		getproductforcart_net = getproductforcartNew(product_id, warehouse_id)
		if getproductforcart_net:
			getproductforcart_net["qty"] = quantity
			getproductforcart_net["new_default_price"] = float(getproductforcart_net["default_price"])*quantity
			getproductforcart_net["new_default_price_unit"] = float(getproductforcart_net["default_price"]) if getproductforcart_net["default_price"] else float(0)
			getproductforcart_net["discount_price_unit"] = float(0)
			getproductforcart_net["discount_price"] = float(0)
			getproductforcart_net["discount_amount"] = float(0)
			getproductforcart_net["disc_type"] =""
			getproductforcart_net["coupon"] = ""
			#print("Data after calculation substitude product...")
			#print(getproductforcart_net)
			if discount_array:
				getproductforcart_net = common.genrate_new_prodcut_with_discount(None, getproductforcart_net, discount_array)
	#print(getproductforcart_net)
	#print("Data after calculation substitude product...")
	return getproductforcart_net

def getproductforcartNew(product_id, warehouse_id=None):
	condition = EngageboostProducts.objects.filter(id=product_id).first()
	if warehouse_id is not None:
		context = {"warehouse_id": warehouse_id}
		product_details = PickerBasicinfoSerializer(condition, context=context, partial=True)
	else:
		product_details = PickerBasicinfoSerializer(condition,partial=True)
		# product_details = BasicinfoSerializer(condition)
	product_details = product_details.data
	if product_details:
		product_details['default_price'] = product_details['channel_currency_product_price']['price']
	return product_details

class PickerStockCategory(generics.ListAPIView):
	def post(self, request, format=None):
		try:
			requestdata = request.data
			now_utc = datetime.datetime.utcnow()
			warehouse_id = requestdata['warehouse_id']
			if "website_id" in requestdata and requestdata['website_id'] is not None and requestdata['website_id'] !="":
				website_id = requestdata['website_id']
			else:
				website_id = 1

			if 'isparent' in requestdata and requestdata['isparent'] is not None and requestdata['isparent'] !="":
				isparent = requestdata['isparent']
			else:
				isparent = None

			if "parent_id" in requestdata and requestdata['parent_id'] is not None and requestdata['parent_id'] !="":
				parent_id = requestdata['parent_id']
			else:
				parent_id = None

			get_category_ids = EngageboostCategoryWarehouse.objects.filter(warehouse_id=warehouse_id,isdeleted='n',isblocked='n').values_list('category_id',flat=True)
			if get_category_ids:
				categorycond = EngageboostCategoryMasters.objects.filter(id__in=get_category_ids,website_id=website_id,isdeleted='n',isblocked='n').values("id","name","description","parent_id","slug","category_url").order_by("name")
				if isparent:
					categorycond = categorycond.filter(parent_id=0)
				if parent_id:
					categorycond = categorycond.filter(parent_id=parent_id)

				if categorycond:
					categorycond = CategoriesViewSerializer(categorycond,many=True)
					data = {"status":1,"api_status":"success","response":categorycond.data,"message":"Category List"}
				else:
					data = {"status":0,"api_status":"error","response":[],"message":"No category found"}
			else:
				data = {"status":0,"api_status":"error","response":[],"message":"No category found"}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"response":[],"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)		

class PickerSearchStock(generics.ListAPIView):
	def post(self, request, format=None):
		try:
			requestdata = request.data
			now_utc = datetime.datetime.utcnow()
			if requestdata['website_id'] is None or requestdata['website_id'] =="":
				website_id = 1
			else:
				website_id = requestdata['website_id']
			# user_id = requestdata['user_id']
			# order_id = requestdata['order_id']
			warehouse_id = requestdata['warehouse_id']
			if 'page' not in requestdata or requestdata['page'] is None or requestdata['page'] =="":
				page = 1
			else:
				page = requestdata['page']

			if 'per_page' not in requestdata or requestdata['per_page'] is None or requestdata['per_page'] =="":
				per_page = get_page_size()
			else:
				per_page = requestdata['per_page']

			if 'search' not in requestdata or requestdata['search'] is None or requestdata['search'] =="":
				search = None
			else:
				search = requestdata['search']

			if 'category_id' not in requestdata or requestdata['category_id'] is None or requestdata['category_id'] =="":
				category_id = None
			else:
				category_id = requestdata['category_id']

			product_ids = []
			if category_id:
				isparentCategory = EngageboostCategoryMasters.objects.filter(id=category_id).first()

				if isparentCategory.parent_id == 0:
					all_cat_ids = []
					all_cat_ids.append(category_id)
					secondchild = EngageboostCategoryMasters.objects.filter(parent_id=category_id,website_id=website_id,isdeleted='n',isblocked='n').values_list('id',flat=True)
					if secondchild:
						all_cat_ids.extend(secondchild)
						thirdchild = EngageboostCategoryMasters.objects.filter(parent_id__in=secondchild,website_id=website_id,isdeleted='n',isblocked='n').values_list('id',flat=True)
						if thirdchild:
							all_cat_ids.extend(thirdchild)

					# print(all_cat_ids)
					product_ids = EngageboostProductCategories.objects.filter(category_id__in=all_cat_ids,isdeleted='n',isblocked='n').values_list('product_id',flat=True)
				else:
					product_ids = EngageboostProductCategories.objects.filter(category_id=category_id,isdeleted='n',isblocked='n').values_list('product_id',flat=True)

				if product_ids:
					ProductCond = EngageboostProducts.objects.filter(id__in=product_ids,website_id=website_id,isdeleted='n',isblocked='n')
				else:
					data = {"status":0,"api_status":"error","response":[],"message":"No product has been found"}
					return Response(data)
			else:

				#------Binayak Start 30-10-2020------#
				warehouse_category_ids = list(EngageboostCategoryWarehouse.objects.filter(isdeleted='n',isblocked='n',warehouse_id=warehouse_id).values_list('category_id',flat=True))
				product_ids = list(EngageboostProductCategories.objects.filter(category_id__in=warehouse_category_ids, isdeleted='n',isblocked='n').values_list('product_id',flat=True))
				ProductCond = EngageboostProducts.objects.filter(id__in=product_ids,website_id=website_id,isdeleted='n',isblocked='n')
				# ProductCond = EngageboostProducts.objects.filter(website_id=website_id,isdeleted='n',isblocked='n')
				#------Binayak End  30-10-2020------#
				
			if 'in_stock' not in requestdata or requestdata['in_stock'] is None or requestdata['in_stock'] =="":
				in_stock = None
			else:
				in_stock = requestdata['in_stock']
				if in_stock == "y":
					product_stock_ids = EngageboostProductStocks.objects.filter(real_stock__gt=0,warehouse_id=warehouse_id,isblocked='n',isdeleted='n').values_list('product_id',flat=True)
				if in_stock == "n":
					product_stock_ids = EngageboostProductStocks.objects.filter(real_stock__lte=0,warehouse_id=warehouse_id,isblocked='n',isdeleted='n').values_list('product_id',flat=True)
				ProductCond = ProductCond.filter(id__in=product_stock_ids)

			if 'has_price' not in requestdata or requestdata['has_price'] is None or requestdata['has_price'] =="":
				has_price = None
			else:
				has_price = requestdata['has_price']
				if has_price == "y":
					has_price_ids = EngageboostChannelCurrencyProductPrice.objects.filter(price__gt=0,product_price_type_id__price_type_id=1,warehouse_id=warehouse_id).values_list('product_id',flat=True)
					ProductCond = ProductCond.filter(id__in=has_price_ids)
					# product_stock_ids = EngageboostProductStocks.objects.filter(real_stock__gt=0,warehouse_id=warehouse_id,isblocked='n',isdeleted='n').values_list('product_id',flat=True)
				if has_price == "n":
					has_price_ids = EngageboostChannelCurrencyProductPrice.objects.filter(price__gt=0,product_price_type_id__price_type_id=1,warehouse_id=warehouse_id).values_list('product_id',flat=True)
					ProductCond = ProductCond.filter(~Q(id__in=has_price_ids))
					# product_stock_ids = EngageboostProductStocks.objects.filter(real_stock__lte=0,warehouse_id=warehouse_id,isblocked='n',isdeleted='n').values_list('product_id',flat=True)
				

			if search is None:
				ProductCond = ProductCond
			else:
				barcode_products = EngageboostMultipleBarcodes.objects.filter(barcode=search, isdeleted = 'n', isblocked = 'n').values_list('product_id',flat=True).all()
				if barcode_products:
					ProductCond = ProductCond.filter(Q(name__icontains=search)|Q(sku__icontains=search)|Q(description__icontains=search)|Q(brand__icontains=search)|Q(id__in=barcode_products))
				else:
					ProductCond = ProductCond.filter(Q(name__icontains=search)|Q(sku__icontains=search)|Q(description__icontains=search)|Q(brand__icontains=search))

			if ProductCond.count()>0:
				#**** Pagination Logic ****
				total_order = ProductCond.count()
				total_page = math.ceil(total_order/per_page)
				next_page = page+1
				current_page = page
				page = page-1
				if page > 0:					
					offset = page*per_page
				else:
					offset = 0
				limit = offset+per_page
				#**** Pagination Logic ****

				ProductCond = ProductCond.order_by('name').all()[offset:limit]				

				if warehouse_id is not None:
					context = {"warehouse_id": warehouse_id,"in_stock":in_stock}
					ProductDetails = PickerBasicinfoSerializer(ProductCond, context=context, many=True)
				else:
					ProductDetails = PickerBasicinfoSerializer(ProductCond,many=True)

				# for Products in ProductDetails.data:
				# 	product_id = Products['id']
				# 	product_stock = EngageboostProductStocks.objects.filter(product_id = product_id,warehouse_id=warehouse_id,isblocked='n',isdeleted='n').order_by('-id').first()
				# 	if product_stock:
				# 		product_stock_serializer = StockViewSerializer(product_stock, partial=True)
				# 		product_stock_serializer = product_stock_serializer.data
				# 	else:
				# 		product_stock_serializer = {"stock": 0,"safety_stock": 0,"virtual_stock": 0,"real_stock": 0}
				# 	Products['product_stock'] = product_stock_serializer

				data = {"status":1,"api_status":"success","response":ProductDetails.data,"total_order":total_order,"total_page":total_page,"current_page":current_page,"next_page":next_page,"per_page":per_page,"message":"Product has been found"}
			else:
				data = {"status":0,"api_status":"error","response":[],"message":"No product has been found"}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"response":[],"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

class PickerManageStock(generics.ListAPIView):
	def post(self,request):
		try:
			company_db = loginview.db_active_connection(request)
			requestdata  = request.data
			now_utc 	 = datetime.datetime.utcnow()
			website_id 	 = requestdata['website_id']
			user_id 	 = requestdata['user_id']
			warehouse_id = requestdata['warehouse_id']
			product_id   = requestdata['product_id']
			price 		 = requestdata['price']
			# action 		 = requestdata['increase']
			# stock   	 = requestdata['stock']

			if 'stock' not in requestdata or requestdata['stock'] is None or requestdata['stock'] =="":
				stock = None
			else:
				stock = requestdata['stock']
			
			#**** Update Product Price ****#
			# has_price = EngageboostChannelCurrencyProductPrice.objects.filter(product_id = product_id,warehouse_id=warehouse_id,product_price_type_id__price_type_id=1).order_by('-id').first()
			has_price = EngageboostChannelCurrencyProductPrice.objects.filter(product_id = product_id,warehouse_id=warehouse_id,product_price_type_id__price_type_id=1).first()
	        # else:
			#     price_obj = EngageboostChannelCurrencyProductPrice.objects.filter(product_id = EngageboostProducts.id,price__gte=0,product_price_type_id__price_type_id=1).order_by('-id').first()
			if has_price:
				price_obj={"price": float(price),"cost": float(price),"mrp": float(price),"channel_id": 6,"min_quantity": 0,"max_quantity": 0,"warehouse_id": warehouse_id,"product_id": product_id}
				EngageboostChannelCurrencyProductPrice.objects.filter(product_id = product_id,warehouse_id=warehouse_id,product_price_type_id__price_type_id=1).update(**price_obj)
				# channelprice = ChannelCurrencyProductPriceSerializer(price_obj, partial=True)
				# channelprice = channelprice.data
			else:
				# check_price_type_master = EngageboostProductPriceTypeMaster.objects.filter(product_id = product_id,price_type_id=1,website_id=website_id,isdeleted='n',isblocked='n').order_by('-id').first()
				check_price_type_master = EngageboostProductPriceTypeMaster.objects.filter(product_id = product_id,price_type_id=1,website_id=website_id,isdeleted='n',isblocked='n').first()
				if check_price_type_master:
					product_price_type_id = check_price_type_master.id
					list_of_warehouse = check_price_type_master.warehouse_id
					if list_of_warehouse == "" or list_of_warehouse is None:
						price_type_obj = {"name":"Regular Price","website_id":website_id,"warehouse_id":warehouse_id,"modified":now_utc}
						EngageboostProductPriceTypeMaster.objects.filter(id=product_price_type_id).update(**price_type_obj)
					else:
						list_of_warehouse = list_of_warehouse.split(',')
						if warehouse_id in list_of_warehouse:
							pass
						else:
							list_of_warehouse.append(warehouse_id)
							list_of_warehouse = ','.join(str(x) for x in list_of_warehouse)

							price_type_obj = {"name":"Regular Price","website_id":website_id,"warehouse_id":list_of_warehouse,"modified":now_utc}
							EngageboostProductPriceTypeMaster.objects.filter(id=product_price_type_id).update(**price_type_obj)

					price_obj={"price": float(price),"cost": float(price),"mrp": float(price),"channel_id": 6,"min_quantity": 0,"max_quantity": 0,"warehouse_id": warehouse_id,"product_id": product_id,"product_price_type_id":product_price_type_id,"start_date":now_utc}
				else:
					price_type_obj = {"name":"Regular Price","website_id":website_id,"created":now_utc,"modified":now_utc,"warehouse_id":warehouse_id,"price_type_id":1,"min_quantity": 0,"max_quantity": 0,"isdeleted":"n","isblocked":"n","product_id":product_id}
					ProductPriceTypeMaster = EngageboostProductPriceTypeMaster.objects.create(**price_type_obj)
					product_price_type_id = ProductPriceTypeMaster.id
					price_obj={"price": float(price),"cost": float(price),"mrp": float(price),"channel_id": 6,"min_quantity": 0,"max_quantity": 0,"warehouse_id": warehouse_id,"product_id": product_id,"product_price_type_id":product_price_type_id,"start_date":now_utc}
				EngageboostChannelCurrencyProductPrice.objects.create(**price_obj)

			# product_price = common.get_channel_currency_product_price(product_id,website_id)
			# elastic = common.change_field_value_elastic(product_id,'EngageboostProducts',{'channel_currency_product_price':product_price})
			# common.save_data_to_elastic(product_id,"EngageboostProducts")

			if stock is not None:
				update_stock = {"modified": now_utc,"stock":stock,"virtual_stock":0,"real_stock":stock}
				EngageboostProductStocks.objects.filter(warehouse_id = warehouse_id, product_id = product_id).update(**update_stock)
				
				# has_stock_already = EngageboostProductStocks.objects.filter(warehouse_id = warehouse_id, product_id = product_id).first()
				# if has_stock_already:
				# 	update_stock = {"modified": now_utc,"stock":stock,"virtual_stock":0,"real_stock":stock}
				# 	EngageboostProductStocks.objects.filter(warehouse_id = warehouse_id, product_id = product_id).update(**update_stock)
				# else:
				# 	update_stock = {"created": now_utc,"modified": now_utc,"stock":stock,"safety_stock":0,"virtual_stock":0,"real_stock":stock,"warehouse_id":warehouse_id,"product_id":product_id,"isblocked":"n","isdeleted":"n","stock_unit":0}
				# 	EngageboostProductStocks.objects.create(**update_stock)
				# product_stock = common.get_product_stock(product_id)
				# elastic = common.change_field_value_elastic(product_id,'EngageboostProducts',{'inventory':product_stock})
			
			# common.change_product_stock_elastic(product_id)
			EngageboostUpdateQueue.objects.create(product_id=product_id,
												  process_type='single',
												  operation_for='inventory',
												  warehouse_id=warehouse_id)

			# common.change_product_price_elastic(product_id)
			EngageboostUpdateQueue.objects.create(product_id=product_id,
												  process_type='single',
												  operation_for='price',
												  warehouse_id=warehouse_id)

			# product_price = common.get_channel_currency_product_price(product_id,website_id)
			# elastic = common.change_field_value_elastic(product_id,'EngageboostProducts',{'channel_currency_product_price':product_price})
			# common.save_data_to_elastic(product_id,"EngageboostProducts")
			data = {"status":1,"api_status":"success","response" : {"product_id":product_id,"warehouse_id":warehouse_id,"price": float(price)},"message":"Product price has been updated"}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"response":[],"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

class PickerSearchReturn(generics.ListAPIView):
	def post(self, request, format=None):
		try:
			requestdata = request.data
			now = datetime.datetime.now()
			if requestdata['website_id'] is None or requestdata['website_id'] =="":
				website_id = 1
			else:
				website_id = requestdata['website_id']

			order_no = requestdata['order_no']
			warehouse_id = requestdata['warehouse_id']

			if 'order_date' in requestdata and requestdata['order_date']: 
				start_date = str(requestdata['order_date']) +" "+ "00:00:00"
				end_date = str(requestdata['order_date']) +" "+ "23:59:59"
			else:
				start_date = end_date = None

			if 'invoice_no' in requestdata and requestdata['invoice_no']:
				invoice_no = requestdata['invoice_no']
			else:
				invoice_no = None

			if 'search' not in requestdata or requestdata['search'] is None or requestdata['search'] =="":
				search = None
			else:
				search = requestdata['search']

			listof_product = []
			if search is not None:
				barcode_products = EngageboostMultipleBarcodes.objects.filter(barcode__icontains=search, isdeleted = 'n', isblocked = 'n').values_list('product_id',flat=True).all()
				if barcode_products:
					listof_product = EngageboostProducts.objects.filter(website_id=website_id,isdeleted='n',isblocked='n').filter(Q(name__istartswith=search)|Q(sku__istartswith=search)|Q(description__istartswith=search)|Q(brand__istartswith=search)|Q(id__in=barcode_products)).values_list('id',flat=True)
				else:
					listof_product = EngageboostProducts.objects.filter(website_id=website_id,isdeleted='n',isblocked='n').filter(Q(name__istartswith=search)|Q(sku__istartswith=search)|Q(description__istartswith=search)|Q(brand__istartswith=search)).values_list('id',flat=True)

			global_setting_date = EngageboostGlobalSettings.objects.filter(website_id=website_id,isdeleted='n',isblocked='n').first()
			if global_setting_date.timezone_id:
				global_setting_zone = EngageboostTimezones.objects.filter(id = global_setting_date.timezone_id).first()
				time_offset = global_setting_zone.offset
			else:
				time_offset = 0

			# if time_offset < 0:
			# 	time_offset = str(time_offset).split('-')
			# 	time_offset = time_offset[1]
			# 	created  = created - timedelta(hours=float(time_offset))
			# 	modified  = modified - timedelta(hours=float(time_offset))
			# else:
			# 	created  = created + timedelta(hours=float(time_offset))
			# 	modified  = modified + timedelta(hours=float(time_offset))

			# order_id=order_id,shipment_id=shipment_id
			warehouseorderlistcond = EngageboostOrdermaster.objects.filter(custom_order_id=order_no,website_id=website_id).values('assign_wh').first()
			if warehouseorderlistcond:
				if warehouseorderlistcond['assign_wh'] is None or warehouseorderlistcond['assign_wh'] == "":
					pass
				else:
					if warehouseorderlistcond['assign_wh'] != warehouse_id:
						data = {"status":0,"api_status":"error","response":[],"message": "You have searched an order from different warehouse."}
						return Response(data)

			orderlistcond = EngageboostOrdermaster.objects.filter(custom_order_id=order_no,assign_wh=warehouse_id,website_id=website_id,order_status=4)

			if orderlistcond:
				if start_date:
					orderlistcond = orderlistcond.filter(created__gte=start_date,created__lte=end_date)
			
				order_ids = None
				if invoice_no:
					order_ids_arr = EngageboostInvoicemaster.objects.filter(website_id=website_id,custom_invoice_id=invoice_no).values_list('order_id',flat=True).all()
					if order_ids_arr:
						order_ids = order_ids_arr
				# print(order_ids)
				if invoice_no and order_ids and orderlistcond:
					orderlistcond = orderlistcond.filter(id__in=order_ids)
				elif invoice_no and order_ids is None and orderlistcond:
					orderlistcond = []
				else:
					orderlistcond = orderlistcond
			else:
				data = {"status":0,"api_status":"error","response":[],"message": "No order details has been found or the order has not been delivered yet"}
				return Response(data)

			if orderlistcond:
				username = created_by_name = None
				if search is not None:
					if listof_product.exists():
						pass						
					else:
						listof_product = [0]
					context = {"product_ids": listof_product}

					orderlist = OrderAndOrderProductAndOrderSubstituteProductSerializer(orderlistcond,context=context,many=True)
				else:
					orderlist = OrderAndOrderProductAndOrderSubstituteProductSerializer(orderlistcond,many=True)
				
				if orderlist:
					total_return_amount = 0
					for orderlists in orderlist.data:
						#*** Custom Gross Total Amount Calculation ****#
						if orderlists["order_amount"]:
							if orderlists["flag_order"] == 1 or orderlists["flag_order"] == '1':
								grand_total = (float(orderlists["net_amount"])+float(orderlists["cod_charge"])+float(orderlists["shipping_cost"])+float(orderlists["tax_amount"]))-float(orderlists["cart_discount"])-float(orderlists["pay_wallet_amount"])
							else:
								grand_total = (float(orderlists["order_net_amount"])+float(orderlists["cod_charge"])+float(orderlists["shipping_cost"])+float(orderlists["tax_amount"]))-float(orderlists["cart_discount"])-float(orderlists["pay_wallet_amount"])

							orderlists["gross_amount"] = grand_total
							orderlists["gross_amount_base"] = grand_total
							
						created = datetime.datetime.strptime(str(orderlists['created']), "%Y-%m-%dT%H:%M:%S.%fZ")
						modified = datetime.datetime.strptime(str(orderlists['modified']), "%Y-%m-%dT%H:%M:%S.%fZ")
						
						if time_offset < 0:
							time_offset = str(time_offset).split('-')
							time_offset = time_offset[1]
							created  = created - timedelta(hours=float(time_offset))
							modified  = modified - timedelta(hours=float(time_offset))
						else:
							created  = created + timedelta(hours=float(time_offset))
							modified  = modified + timedelta(hours=float(time_offset))

						orderlists['created'] = format_date(str(created),'%Y-%m-%d %H:%M:%S')
						orderlists['modified'] = format_date(str(modified),'%Y-%m-%d %H:%M:%S')

						if 'order_products' in orderlists and orderlists['order_products']:
							for order_products in orderlists['order_products']:
								if float(order_products['weight']) > 0:
									order_products['weight'] = order_products['weight']
								else:
									if order_products['product']:
										if order_products['product']['weight'] is None or order_products['product']['weight'] == "":
											order_products['weight'] = float(0)
										else:
											order_products['weight'] = float(order_products['product']['weight'])
									else:
										order_products['weight'] = float(0)

								#**** Return calculation for main products ****#
								if order_products['returns'] > 0:
									if order_products['product_tax_price'] is None or order_products['product_tax_price'] =="":
										order_products['product_tax_price'] = float(0)
									
									total_return_amount = total_return_amount + ((order_products['product_price'] + order_products['product_tax_price'])*order_products['returns'])

						if 'order_substitute_products' in orderlists and orderlists['order_substitute_products']:
							for order_substitute_products in orderlists['order_substitute_products']:
								if float(order_substitute_products['weight']) > 0:
									order_substitute_products['weight'] = order_substitute_products['weight']
								else:
									if order_substitute_products['product']:
										if order_substitute_products['product']['weight'] is None or order_substitute_products['product']['weight'] == "":
											order_substitute_products['weight'] = float(0)
										else:
											order_substitute_products['weight'] = float(order_substitute_products['product']['weight'])
									else:
										order_substitute_products['weight'] = float(0)

								#**** Return calculation for substitute products ****#
								if order_substitute_products['returns'] > 0:
									if order_substitute_products['product_tax_price'] is None or order_substitute_products['product_tax_price'] =="":
										order_substitute_products['product_tax_price'] = float(0)
									
									total_return_amount = total_return_amount + ((order_substitute_products['product_price'] + order_substitute_products['product_tax_price'])*order_substitute_products['returns'])

						orderlists['return_amount'] = total_return_amount
						order_substitute_products_list = order_products_list = []
						orderlists['lat_val'] = orderlists['long_val'] = None
						if 'customer_addressbook' in orderlists and orderlists['customer_addressbook']:
							if orderlists['customer_addressbook']['lat_val'] is not None and orderlists['customer_addressbook']['lat_val'] != "":
								orderlists['lat_val'] = orderlists['customer_addressbook']['lat_val']
							if orderlists['customer_addressbook']['long_val'] is not None and orderlists['customer_addressbook']['long_val'] != "":
								orderlists['long_val'] = orderlists['customer_addressbook']['long_val']

						if 'order_activity' in orderlists and orderlists['order_activity']:
							for order_activity in orderlists['order_activity']:
								order_activity['activity_date'] = format_date(order_activity['activity_date'],'%Y-%m-%d %H:%M:%S')
						if orderlists['assign_to']:
							checkuser = EngageboostUsers.objects.filter(id=orderlists['assign_to']).first()			
							if checkuser:								
								if checkuser.first_name is None or checkuser.first_name == "":
									username = ""
								else:
									username = checkuser.first_name
								if checkuser.last_name is None or checkuser.last_name == "":
									username = username
								else:
									username = username+' '+checkuser.last_name
						orderlists['assign_to_name'] = username
						
						if 'order_shipment' in orderlists and orderlists['order_shipment']:
							checkuser = EngageboostUsers.objects.filter(id=orderlists['order_shipment']['created_by']).first()
							if checkuser:								
								if checkuser.first_name is None or checkuser.first_name == "":
									created_by_name = ""
								else:
									created_by_name = checkuser.first_name
								if checkuser.last_name is None or checkuser.last_name == "":
									created_by_name = created_by_name
								else:
									created_by_name = created_by_name+' '+checkuser.last_name
							orderlists['order_shipment']['created_by_name'] = created_by_name

				data = {"status":1,"api_status":"success","response":orderlist.data,"message": "Order details has been found"}
			else:
				data = {"status":0,"api_status":"error","response":[],"message": "No order details has been found or the order has not been delivered yet"}
			return Response(data)	
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)	

class PickerConfirmReturn(generics.ListAPIView):
	def post(self,request):
		try:
			requestdata = request.data
			now_utc = datetime.datetime.now()
			website_id 		 	= requestdata['website_id']
			user_id 		 	= requestdata['user_id']
			order_id         	= requestdata['order_id']
			shipment_id 		= requestdata['shipment_id']
			trent_picklist_id 	= requestdata['trent_picklist_id']
			current_return_amount = 0
			if 'return_details' in requestdata and requestdata['return_details']:
				for product_arr in requestdata['return_details']:
					order_product_id = product_arr['order_product_id']
					product_id = product_arr['product_id']
					return_qty = product_arr['return_qty']

					#**** Return calculation ****#
					order_products = EngageboostOrderProducts.objects.filter(id=order_product_id,order_id=order_id,product_id=product_id).first()
					if return_qty > 0:
						if order_products.product_tax_price is None or order_products.product_tax_price =="":
							order_products.product_tax_price = float(0)
						
						current_return_amount = current_return_amount + ((order_products.product_price + order_products.product_tax_price)*return_qty)

					#**** Update Order Products ****#
					EngageboostOrderProducts.objects.filter(id=order_product_id,order_id=order_id,product_id=product_id).update(returns=return_qty)
					EngageboostShipmentOrderProducts.objects.filter(order_product_id=order_product_id,order_id=order_id,product_id=product_id).update(returns=return_qty)

				total_grn_quantity = EngageboostOrderProducts.objects.filter(order_id=order_id, quantity__gt=0).all().aggregate(Sum('grn_quantity'))
				total_returns = EngageboostOrderProducts.objects.filter(order_id=order_id, quantity__gt=0).all().aggregate(Sum('returns'))

				totalgrnquantity = totalreturns = 0
				if total_grn_quantity:
					if total_grn_quantity["grn_quantity__sum"] is not None:
						totalgrnquantity = total_grn_quantity["grn_quantity__sum"]
				if total_returns:
					if total_returns["returns__sum"] is not None:
						totalreturns = total_returns["returns__sum"]

				if int(totalgrnquantity) > int(0) and int(totalreturns) > int(0) and int(totalgrnquantity) == int(totalreturns):
					print('Full Return')
					EngageboostOrdermaster.objects.filter(id=order_id).update(return_status='Full Returned')
					common.save_order_activity('',order_id,None,7,"Full Return Received",user_id,1)
					# elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'order_status':'5','shipping_status':'Full Return'})

				if int(totalgrnquantity) > int(0) and int(totalreturns) > int(0) and int(totalgrnquantity) > int(totalreturns):
					print('Partial Return')
					EngageboostOrdermaster.objects.filter(id=order_id).update(return_status='Partial Returned')
					common.save_order_activity('',order_id,None,7,"Partial Return Received",user_id,1)
					# elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'order_status':'6','shipping_status':'Partial Return'})

				data = {"status":1,"api_status":"success","response":{"order_id":order_id,"current_return_amount":current_return_amount},"message":"Your return request has been confirmed."}
			else:
				data = {"status":0,"api_status":"error","response":[],"message":"Invalid return request."}
			update_order_and_order_products(order_id)
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"response":[],"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

class PickerLatestOrders(generics.ListAPIView):
	def post(self,request):
		try:
			requestdata = request.data
			now_utc 	= datetime.datetime.now()
			website_id 	= requestdata['website_id']
			warehouse_id = requestdata['warehouse_id']
			order_id    = requestdata['order_id']
			check_order = EngageboostOrdermaster.objects.filter(isdeleted='n',isblocked='n',order_status__in=[0,100],buy_status=1,website_id=website_id,assign_wh=warehouse_id).filter(id__gt=order_id)

			order_count = 0
			if check_order:
				order_count = check_order.count()

			data = {"status":1,"api_status":"success","response":{"no_of_latest_order":order_count,"last_order":order_id}}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"response":[],"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

#------Binayak Start-----#
class PickerSendPushNotification(generics.ListAPIView):
	def post(self,request):
		try:
			requestdata = request.data
			order_id    = requestdata['order_id']
			check_order = EngageboostOrdermaster.objects.filter(id=order_id)

			if check_order.count()>0:
				common.notification_send_by_AutoResponder(order_id, 31)

			data = {"status":1,"api_status":"success"}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"response":[],"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)
#------Binayak End-----#

# common.notification_send_by_AutoResponder(3061, 31)

def get_page_size():
	settings = EngageboostGlobalSettings.objects.filter(isdeleted='n',isblocked='n',website_id=1).order_by('-id').first()
	if settings:
		size=settings.itemlisting_backend
	else:
		size=20
	return size

def format_date(datestr,format='%Y-%m-%d'):
	# try:
	# 	datestr = datetime.datetime.fromtimestamp(datestr)
	# except:
	# 	pass
	try:
		datestr = datetime.datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%S.%fZ")
		datestr = datestr.strftime(format)
		# print(1)
		return datestr
	except:
		try:
			datestr = datetime.datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%SZ")
			datestr = datestr.strftime(format)
			# print(2)
			return datestr
		except:
			try:
				datestr = datetime.datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S")
				datestr = datestr.strftime(format)
				# print(3)
				return datestr
			except:
				try:
					datestr = datetime.datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S.%f")
					datestr = datestr.strftime(format)
					# print(4)
					return datestr
				except:
					try:
						datestr = datetime.datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%S.%f")
						datestr = datestr.strftime(format)
						# print(5)
						return datestr
					except:
						try:
							datestr = datetime.datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%S")
							datestr = datestr.strftime(format)
							# print(6)
							return datestr
						except:
							# print(7)
							return datestr
							pass


def update_order_and_order_products_for_picking(order_id, return_order_type='GRN Cancellation'):
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
		for products in all_OrderProduct['order_products']:
			if products['pick_as_substitute'] == 'n' or (products['pick_as_substitute'] == 'y' and products['send_approval'] == 'approve'):
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
			"gross_discount_amount_base":gross_discount_amount
		}
		EngageboostOrdermaster.objects.filter(id=order_id).update(**shipped_save_order)
		common.save_data_to_elastic(order_id,'EngageboostOrdermaster')

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
		pay_wallet_amount 	= rs_oder.pay_wallet_amount
		for products in all_OrderProduct['order_products']:
			if products['pick_as_substitute'] == 'n' or (products['pick_as_substitute'] == 'y' and products['send_approval'] == 'approve'):
				quantity = products['quantity']
				if int(products['grn_quantity']) > 0:
					quantity = int(products['grn_quantity'])-int(products['returns'])
				else:
					quantity = int(products['quantity'])-(int(products['deleted_quantity'])+int(products['returns'])+int(products['shortage']))
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
		if rs_oder.payment_type_id == 2:
			paid_amount = gross_amount
		else:
			paid_amount = rs_oder.paid_amount

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
			"pay_wallet_amount":pay_wallet_amount,
			"paid_amount": paid_amount
		}
		EngageboostOrdermaster.objects.filter(id=order_id).update(**shipped_save_order)
		common.save_data_to_elastic(order_id,'EngageboostOrdermaster')

def create_automatic_delivery_plan(orderArr, shipment_id, warehouse_id):
	origins = "25.2048,55.2708"
	if warehouse_id > 0:
		warehouseDetails = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).first()
		if warehouseDetails and warehouseDetails.latitude and warehouseDetails.longitude:
			origins = warehouseDetails.latitude+','+warehouseDetails.longitude;

	now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
	#print("Planner is calling here...by cds...")
	#print("====================================")
	all_order = EngageboostOrdermaster.objects.filter(id__in=orderArr).order_by('slot_start_time').all()
	order_data_serializer = OrderMasterSerializer(all_order, many=True)
	#print(json.dumps(order_data_serializer.data))
	zoneId = order_data_serializer.data[0]["zone_id"]
	countOrder = len(orderArr);
	VehicleData = EngageboostVehicleMasters.objects.filter(no_of_orders__gt=0).first()
	if VehicleData and VehicleData.no_of_orders:
		vehicle_threshold = VehicleData.no_of_orders
	else:
		vehicle_threshold = 15

	# manual checking
	#vehicle_threshold = 2
	if countOrder > vehicle_threshold:
		no_of_vehicle = countOrder/vehicle_threshold
		no_of_vehicle = math.ceil(countOrder/vehicle_threshold)
	else:
		no_of_vehicle = 1

	time_slot_array = []
	time_slot_wise_array = []
	order_vs_timeslot = []
	timeslotWiseArr =[]
	#print(orderArr)
	#print(json.dumps(order_data_serializer.data))
	for allOrder in order_data_serializer.data:
		time_slot_array_Obj = {
			'slot_start_time':allOrder['slot_start_time'],
			'time_slot_id': allOrder['time_slot_id']
		}
		if time_slot_array_Obj not in time_slot_array :
			time_slot_array.append(time_slot_array_Obj)

	order_lat_long_relation = []
	for time_slot_wise_val in time_slot_array:
		order_lat_long_relation_allOrder = [] # Making slot wise order planner first
		destinations_arr = []  # Making slot wise order planner first
		for allOrder in order_data_serializer.data :
			if time_slot_wise_val['time_slot_id'] == allOrder['time_slot_id']:
				order_lat_long_relation_obj ={}
				# allOrder['CustomersAddressBook']['long_val'] = '88.3849'
				# allOrder['CustomersAddressBook']['lat_val'] = '22.8671'
				if allOrder['CustomersAddressBook']['lat_val'] is None:
					allOrder['CustomersAddressBook']['lat_val'] = '22.8671'
				if allOrder['CustomersAddressBook']['long_val'] is None:
					allOrder['CustomersAddressBook']['long_val'] = '88.3849'
				if allOrder['CustomersAddressBook']:
					order_lat_long_relation_obj = {
						'order_id': allOrder['id'],
						'area_id': allOrder['area_id'],
						'slot_start_time': allOrder['slot_start_time'],
						'address_book_id': allOrder['CustomersAddressBook']['id'],
						'longitude': allOrder['CustomersAddressBook']['long_val'],
						'latitude': allOrder['CustomersAddressBook']['lat_val'],
						'lat_long_val': allOrder['CustomersAddressBook']['lat_val']+","+allOrder['CustomersAddressBook']['long_val']
					}
					destinations_arr.append(allOrder['CustomersAddressBook']['lat_val']+","+allOrder['CustomersAddressBook']['long_val']);
				else:
					order_lat_long_relation_obj = {
						'order_id': allOrder['id'],
						'area_id': allOrder['area_id'],
						'slot_start_time': allOrder['slot_start_time'],
						'address_book_id': 0,
						'lat_long_val': origins,
						'longitude':'88.4119',
						'latitude':'22.5135'
					}
					destinations_arr.append(origins);
				order_lat_long_relation_allOrder.append(order_lat_long_relation_obj)
				order_lat_long_relation.append(order_lat_long_relation_obj)
		time_slot_wise_val['allOrder'] = order_lat_long_relation_allOrder
		time_slot_wise_val['destinations'] = '|'.join(destinations_arr)
	#print(json.dumps(time_slot_wise_val))
	#print(json.dumps(time_slot_array))
	# print('==================')
	if(no_of_vehicle == 1):
		total_orderd_array = []
		total_orderd_array = calculate_distance(origins,time_slot_array, order_lat_long_relation)
		# Manual checking if no planner exist
		# for order_id in orderArr:
		# 	total_orderd_array_obj = {
		# 		'order_id':order_id,
		# 		'distance':10,
		# 		'duration':2
		# 	}
		# 	total_orderd_array.append(total_orderd_array_obj)
		orders = 1
		for total_orderd_arrayvalue in total_orderd_array :
			EngageboostDeliveryPlanOrder.objects.filter(order_id=total_orderd_arrayvalue['order_id']).delete()
			EngageboostDeliveryPlanOrder.objects.create(
				order_id = total_orderd_arrayvalue['order_id'],
				orders = orders,
				distance = total_orderd_arrayvalue['distance'],
				time = total_orderd_arrayvalue['duration'],
				shipment_id = shipment_id,
				created = now_utc,
				virtual_vechile_id = 1
			)
			#update sort_by_distance
			EngageboostOrdermaster.objects.filter(id=total_orderd_arrayvalue['order_id']).update(sort_by_distance=orders)
			orders = orders+1
	else:
		totalCount = 0
		timeslotWiseCount = []
		total_time_slot = []
		no_of_slot = len(time_slot_array)
		average_order_per_vehicle = math.ceil(countOrder/no_of_vehicle)
		finalVehicleArr = []
		timeslotwise_max_order_per_vehicle = []
		for timeslotWiseCountvalue in time_slot_array:
			timeslotwise_max_order_per_vehicleObj = {
				'slot_start_time':timeslotWiseCountvalue['slot_start_time'],
				'max_order_per_slot': math.ceil(len(timeslotWiseCountvalue['allOrder'])/no_of_vehicle)
			}
			timeslotWiseCountvalue['max_order_per_slot'] = math.ceil(len(timeslotWiseCountvalue['allOrder'])/no_of_vehicle)

		# print(timeslotWiseCountvalue)
		finalVehicleArr = []
		AllAreaArr = EngageboostZoneMasters.objects.filter(location_type='A',isdeleted='n',isblocked='n').all().order_by('distance')
		for time_slot_wise_val in time_slot_array:
			order_lat_long_relation_new = []
			for all_area in AllAreaArr:
				for areawiseOrder in time_slot_wise_val['allOrder']:
					if all_area.id == areawiseOrder['area_id']:
						order_lat_long_relation_new.append(areawiseOrder)

			time_slot_wise_val['allOrder'] = order_lat_long_relation_new
			#print(time_slot_wise_val['allOrder'])
			#lista_rr = list(divide_chunks(time_slot_wise_val['allOrder'], 2))
			#print(lista_rr)
			if len(time_slot_wise_val['allOrder']) > 0:
				time_slot_wise_val['vehicleArr'] = list(divide_chunks(time_slot_wise_val['allOrder'], time_slot_wise_val['max_order_per_slot']))
			#print(time_slot_wise_val['vehicleArr'])
			for finalVehicleArrObj in time_slot_wise_val['vehicleArr']:
				finalVehicleArr.append(finalVehicleArrObj)

		#print(finalVehicleArr)
		vehicleCount = 1;
		for finalVehicleArrvalue in finalVehicleArr:
			timeslotWiseArrmulti = []
			order_lat_long_relationmulti = []
			destinations_arr = []
			for time_slot_wise_val in time_slot_array:
				for all_order in time_slot_wise_val['allOrder']:
					#print(all_order)
					if all_order in finalVehicleArrvalue:
						time_slot_array_Obj = {
							'slot_start_time':allOrder['slot_start_time'],
							'time_slot_id': allOrder['time_slot_id']
						}
						# checking unique....
						if time_slot_array_Obj not in timeslotWiseArrmulti :
							timeslotWiseArrmulti.append(time_slot_array_Obj)
			#print(timeslotWiseArrmulti)

			for timeslotWiseArrmulti_val in timeslotWiseArrmulti:
				for all_order_new in finalVehicleArrvalue:
					if all_order_new['slot_start_time'] == timeslotWiseArrmulti_val['slot_start_time']:
						order_lat_long_relation_mul_obj = {}
						order_lat_long_relation_mul_obj = all_order_new
						order_lat_long_relationmulti.append(order_lat_long_relation_mul_obj)
						destinations_arr.append(all_order_new['lat_long_val'])

			timeslotWiseArrmulti_val['allOrder'] = order_lat_long_relationmulti
			timeslotWiseArrmulti_val['destinations'] = '|'.join(destinations_arr)
			# print(json.dumps(timeslotWiseArrmulti))
			total_orderd_array = calculate_distance(origins, timeslotWiseArrmulti, order_lat_long_relationmulti)
			orders = 1
			# print(vehicleCount)
			# print(total_orderd_array)
			for total_orderd_arrayvalue in total_orderd_array:
				#EngageboostDeliveryPlanOrder.objects.filter(order_id=total_orderd_arrayvalue['order_id']).delete()
				order_exist = EngageboostDeliveryPlanOrder.objects.filter(order_id=total_orderd_arrayvalue['order_id']).count()
				# print(order_exist)
				if order_exist:
					EngageboostDeliveryPlanOrder.objects.filter(order_id=total_orderd_arrayvalue['order_id']).update(order_id = total_orderd_arrayvalue['order_id'],orders = orders,distance = total_orderd_arrayvalue['distance'],time = total_orderd_arrayvalue['duration'],shipment_id = shipment_id,modified = now_utc,virtual_vechile_id = vehicleCount)
				else:
					EngageboostDeliveryPlanOrder.objects.create(order_id = total_orderd_arrayvalue['order_id'],orders = orders,distance = total_orderd_arrayvalue['distance'],time = total_orderd_arrayvalue['duration'],shipment_id = shipment_id,created = now_utc,virtual_vechile_id = vehicleCount)
				#update sort_by_distance
				EngageboostOrdermaster.objects.filter(id=total_orderd_arrayvalue['order_id']).update(fulfillment_id = vehicleCount, sort_by_distance=orders)
				orders = orders+1
			vehicleCount = vehicleCount+1
		# else loop end
		# print(no_of_vehicle)
	return no_of_vehicle

def divide_chunks(l, n): 
	# looping till length l
	for i in range(0, len(l), n):
		yield l[i:i + n]

def calculate_distance(origins,timeslotWiseArr,order_lat_long_relation):
	destinationArr = []
	#print('calculate_distance')
	#print(order_lat_long_relation)
	#print(json.dumps(timeslotWiseArr))
	firstcount = 0;
	secondCount = 0;
	final_ordered_array=[];
	final_ordered_array_first_slot = []
	final_ordered_array_second_slot = []
	first_slot = 0
	for destinationArrkey in timeslotWiseArr:
		destinations = destinationArrkey['destinations']
		#print(timeslotWiseArr)
		allDestination = destinations.split("|")
		allDestinationArr = destinations.split("|")
		# ENTER INTO FIRST SLOT
		if first_slot == 0:
			for allDestinationvalue in allDestination:
				#print('Yes data coming => ' + allDestinationvalue + ' >> ' + str(firstcount))
				#print(firstcount)
				if firstcount == 0:
					origins = origins
					# CALL FIRST TIME WITH WAREHOUSE AS ORIGIN AND ALL FIRST TIMESLOT ORDERS AS DESTINATION
					return_element = call_google_distance_matrix(origins, destinations, timeslotWiseArr)
					#print(return_element)
					for order_lat_long_relation_val in order_lat_long_relation:
						if order_lat_long_relation_val['order_id'] == return_element[0]['order_id']:
							origins = order_lat_long_relation_val['lat_long_val']
							value_index = allDestinationArr.index(order_lat_long_relation_val['lat_long_val'])
							del allDestinationArr[value_index]
							for destinationArrkeyValue in destinationArrkey['allOrder']:
								#print(destinationArrkeyValue)
								if destinationArrkeyValue['order_id'] == return_element[0]['order_id']:
									value_index = destinationArrkey['allOrder'].index(destinationArrkeyValue)
									del destinationArrkey['allOrder'][value_index]
					final_ordered_array_first_slot.append(return_element[0])
					#print(allDestinationArr)
					#print(timeslotWiseArr)
				else:
					allDestStr = '|'.join(allDestinationArr)
					return_element = call_google_distance_matrix(origins, allDestStr, timeslotWiseArr)
					for order_lat_long_relation_val in order_lat_long_relation:
						if order_lat_long_relation_val['order_id'] == return_element[0]['order_id']:
							origins = order_lat_long_relation_val['lat_long_val']
							value_index = allDestinationArr.index(order_lat_long_relation_val['lat_long_val'])
							del allDestinationArr[value_index]
							for destinationArrkeyValue in destinationArrkey['allOrder']:
								#print(destinationArrkeyValue)
								if destinationArrkeyValue['order_id'] == return_element[0]['order_id']:
									value_index = destinationArrkey['allOrder'].index(destinationArrkeyValue)
									del destinationArrkey['allOrder'][value_index]
					final_ordered_array_first_slot.append(return_element[0])
					#print(allDestinationArr)
					#print(allDestination)
				firstcount+=1
			#print(final_ordered_array_first_slot)
		else:
			# ENTER INTO SECOND SLOT
			allDestStr = '|'.join(allDestinationArr)
			for allDestinationvalue in allDestination:
				if secondCount == 0:
					#origins is always coming from first slot
					return_element_second = call_google_distance_matrix(origins, destinations, timeslotWiseArr)
					#print(return_element_second)
					for order_lat_long_relation_val in order_lat_long_relation:
						if order_lat_long_relation_val['order_id'] == return_element_second[0]['order_id']:
							origins = order_lat_long_relation_val['lat_long_val']
							value_index = allDestinationArr.index(order_lat_long_relation_val['lat_long_val'])
							del allDestinationArr[value_index]
							for destinationArrkeyValue in destinationArrkey['allOrder']:
								#print(destinationArrkeyValue)
								if destinationArrkeyValue['order_id'] == return_element_second[0]['order_id']:
									value_index = destinationArrkey['allOrder'].index(destinationArrkeyValue)
									del destinationArrkey['allOrder'][value_index]
					final_ordered_array_second_slot.append(return_element_second[0])
				else:
					allDestStr = '|'.join(allDestinationArr)
					return_element_second = call_google_distance_matrix(origins, allDestStr, timeslotWiseArr)
					for order_lat_long_relation_val in order_lat_long_relation:
						if order_lat_long_relation_val['order_id'] == return_element_second[0]['order_id']:
							origins = order_lat_long_relation_val['lat_long_val']
							value_index = allDestinationArr.index(order_lat_long_relation_val['lat_long_val'])
							del allDestinationArr[value_index]
							for destinationArrkeyValue in destinationArrkey['allOrder']:
								#print(destinationArrkeyValue)
								if destinationArrkeyValue['order_id'] == return_element_second[0]['order_id']:
									value_index = destinationArrkey['allOrder'].index(destinationArrkeyValue)
									del destinationArrkey['allOrder'][value_index]
					final_ordered_array_second_slot.append(return_element_second[0])
				secondCount+=1
		first_slot+=1
	total_return_arr = []
	if len(final_ordered_array_second_slot)> 0:
		total_return_arr = final_ordered_array_first_slot+final_ordered_array_second_slot
	else:
		total_return_arr = final_ordered_array_first_slot
	#print(total_return_arr)
	return total_return_arr

def call_google_distance_matrix(source, dest, timeslotWiseArr):
	APY_KEY = 'AIzaSyBaTj-wuRYF1YuAHvj8UV5JhDMc_y5f9-g'
	#APY_KEY = 'AIzaSyCE0i_GPkfk5g2VINiZTYCobWU-qpk7psc'
	GOOGLE_MAPS_API_URL = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="+source+"&destinations="+dest+"&key="+APY_KEY+"&travelMode=DRIVING&waypoints=optimize:true&sensor=false"
	result = requests.get(GOOGLE_MAPS_API_URL)
	result = result.json()
	#print('Google response data...')
	print(result)
	timeDistance =  [];
	if(result['status'] == 'OK'):
		for value in result['rows'][0]['elements']:
			if value['status'] == 'ZERO_RESULTS':
				timeDistanceObj = {
					'distance': 0,
					'duration': 1,
				}
			else:
				timeDistanceObj = {
					'distance': value['distance']['value'],
					'duration': value['duration']['value'],
				}
			timeDistance.append(timeDistanceObj)
	#print(timeDistance)
	# Python shorting....
	timeDistance = sorted(timeDistance, key=lambda dct: dct['distance'])
	#print(timeDistance);
	shortestOrder = []
	count = 0
	#print("----------------------")
	#print(source)
	#print(dest)
	#print("----------------------")
	for timeDistancevalue in timeDistance:
		if count == 0:
			dest_new = dest.split("|")
			shoretes_one = dest_new[0]
			shoretes_one = shoretes_one.split(",")
			latitude = shoretes_one[0]
			seekreturn = seekValue(timeslotWiseArr,latitude)
			shortestOrderObj = {
				'order':0,
				'order_id': seekreturn,
				'distance':timeDistancevalue['distance'],
				'duration':timeDistancevalue['duration']
			}
			shortestOrder.append(shortestOrderObj)
			count += 1
	#print(shortestOrder)
	return shortestOrder

def seekValue(haystack, needle):
	#print(json.dumps(haystack))
	for haystack in haystack:
		for ordvalue in haystack['allOrder']:
			if ordvalue['latitude'] == needle:
				return ordvalue['order_id']

class PickerUpdateOrderDetails(generics.ListAPIView):
	def post(self,request):
		try:
			requestdata = request.data
			# now_utc = datetime.datetime.now()
			website_id 				= requestdata['website_id']
			order_id 				= requestdata['order_id']
			user_id 				= requestdata['user_id']
			if 'order_amount' not in requestdata or requestdata['order_amount'] is None or requestdata['order_amount'] =="":
				order_amount = None
				updated_order_amount = None
			else:
				order_amount = requestdata['order_amount']
				updated_order_amount = requestdata['updated_order_amount']
			
			if order_amount:
				#**** Update Order Amount ****#
				EngageboostOrdermaster.objects.filter(id=order_id).update(order_net_amount=float(updated_order_amount))
				#**** order activity ****#
				order_activities_str = 'Value of products has been updated from '+str(order_amount)+' to '+str(updated_order_amount)
				common.save_order_activity("",order_id,None,7,order_activities_str,user_id,1)
				
				orderlists = EngageboostOrdermaster.objects.filter(id=order_id).values("gross_amount","net_amount","cod_charge","shipping_cost","tax_amount","cart_discount","pay_wallet_amount","flag_order","order_amount","order_net_amount").first()
				#*** Custom Gross Total Amount Calculation ****#
				if orderlists["order_net_amount"]:
					if orderlists["flag_order"] == 1 or orderlists["flag_order"] == '1':
						grand_total = (float(orderlists["net_amount"])+float(orderlists["cod_charge"])+float(orderlists["shipping_cost"])+float(orderlists["tax_amount"]))-float(orderlists["cart_discount"])-float(orderlists["pay_wallet_amount"])
						orderlists["net_amount"] = float(orderlists["net_amount"])
						orderlists["net_amount_base"] = float(orderlists["net_amount"])
					else:
						grand_total = (float(orderlists["order_net_amount"])+float(orderlists["cod_charge"])+float(orderlists["shipping_cost"])+float(orderlists["tax_amount"]))-float(orderlists["cart_discount"])-float(orderlists["pay_wallet_amount"])
						orderlists["net_amount"] = float(orderlists["order_net_amount"])
						orderlists["net_amount_base"] = float(orderlists["order_net_amount"])

					orderlists["gross_amount"] = grand_total
					orderlists["gross_amount_base"] = grand_total

					EngageboostOrdermaster.objects.filter(id=order_id).update(order_amount=float(grand_total))
				else:
					orderlists["gross_amount"] = orderlists["gross_amount"]
					orderlists["net_amount"] = orderlists["net_amount"]

				data = {
					"status":1,
					"api_status" : "success",
					"response" : {"order_amount":float(orderlists["gross_amount"]),"order_net_amount":float(orderlists["net_amount"]),"old_order_amount":float(order_amount)},
					"message":"Order amount has been updated."
				}
			else:
				slot_start_time = requestdata['slot_start_time']
				slot_end_time = requestdata['slot_end_time']

				#**** Update Order Time Slot ****#
				slot_start_time_12 = datetime.datetime.strptime(slot_start_time, "%H:%M")
				slot_start_time_12 = slot_start_time_12.strftime("%I:%M %p")

				slot_end_time_12 = datetime.datetime.strptime(slot_end_time, "%H:%M")
				slot_end_time_12 = slot_end_time_12.strftime("%I:%M %p")

				time_slot_id = str(slot_start_time_12)+' - '+str(slot_end_time_12)
				EngageboostOrdermaster.objects.filter(id=order_id).update(slot_start_time=slot_start_time,slot_end_time=slot_end_time,time_slot_id=time_slot_id)

				#**** order activity ****#
				order_activities_str = 'Order delivery time has been changed to '+str(slot_end_time)
				common.save_order_activity("",order_id,None,7,order_activities_str,user_id,1)
				# common.notification_send_by_AutoResponder(order_id, 32)
				# common.email_send_by_AutoResponder(order_id, 32)
				data = {
					"status":1,
					"api_status" : "success",
					"response" : {"slot_start_time":slot_start_time,"slot_end_time":slot_end_time},
					"message":"Order delivery time has been changed."
				}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"response":{},"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

class PickerUpdateOrderBillNumber(generics.ListAPIView):
	def post(self,request):
		try:
			requestdata = request.data
			# now_utc = datetime.datetime.now()
			website_id = requestdata['website_id']
			order_id = requestdata['order_id']
			user_id = requestdata['user_id']
			if 'order_bill_number' not in requestdata or requestdata['order_bill_number'] is None or requestdata['order_bill_number'] =="":
				order_bill_number = None
			else:
				order_bill_number = requestdata['order_bill_number']
			
			if order_bill_number:
				#**** Update Order Bill Number ****#
				EngageboostOrdermaster.objects.filter(id=order_id).update(channel_order_id=order_bill_number)
				#**** order activity ****#
				order_activities_str = 'Order bill number has been updated '+str(order_bill_number)
				common.save_order_activity("",order_id,None,7,order_activities_str,user_id,1)

				data = {
					"status":1,
					"api_status" : "success",
					"response" : {"order_id":order_id,"order_bill_number":order_bill_number},
					"message":"Bill number has been updated."
				}
			else:
				data = {
					"status":0,
					"api_status" : "error",
					"response" : {},
					"message":"No bill number found."
				}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"msg":str(error),"response":{},"message":"Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)

class PickerOrderDetailsCsv(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = request.data
		try:
			if requestdata['website_id'] is None or requestdata['website_id'] == "":
				website_id = 1
			else:
				website_id = requestdata['website_id']
			order_id = requestdata['order_id']


			orderlistcond = EngageboostOrdermaster.objects.filter(id=order_id, isdeleted='n', isblocked='n',buy_status=1, website_id=website_id)
			if orderlistcond:
				# username = created_by_name = None

				file_dir = settings.MEDIA_ROOT + '/pickingorderdetails/'
				export_dir = settings.MEDIA_URL + 'pickingorderdetails/'
				if not os.path.exists(file_dir):
					os.makedirs(file_dir)
				# ************  Create file name
				# file_name = "stock_export_" + get_random_string(length=5)
				file_name = "Order_products_details" + str(order_id) + ".csv"

				# Create file full path
				file_path = file_dir + file_name
				export_file_path = export_dir + file_name
				export_file_path = export_file_path[1:]

				orderlist = OrderAndOrderProductAndOrderSubstituteProductCSVSerializer(orderlistcond, many=True)
				if orderlist:

					with open(file_path, 'w', newline='') as file:
						# print('in here')
						fieldnames = ['Product Name', 'SKU', 'Quantity Ordered', 'Unit Weight', 'Unit Price']
						writer = csv.DictWriter(file, fieldnames=fieldnames)
						writer.writeheader()

						for orderlists in orderlist.data:
							any_substtitute_exists = EngageboostOrderSubstituteProducts.objects.filter(order_id=order_id,pick_as_substitute='y',quantity__gt=0,send_approval__in=['approve','declined']).count()
							unavailable_products = []
							if 'order_products' in orderlists and orderlists['order_products']:
								for i in range(len(orderlists['order_products'])):

									if float(orderlists['order_products'][i]['weight']) > 0:
										orderlists['order_products'][i]['weight'] = orderlists['order_products'][i][
											'weight']
									else:
										if orderlists['order_products'][i]['product']:
											if orderlists['order_products'][i]['product']['weight'] is None or \
													orderlists['order_products'][i]['product']['weight'] == "":
												orderlists['order_products'][i]['weight'] = float(0)
											else:
												orderlists['order_products'][i]['weight'] = float(
													orderlists['order_products'][i]['product']['weight'])
										else:
											orderlists['order_products'][i]['weight'] = float(0)

									writer.writerow(
										{'Product Name': orderlists['order_products'][i]['product']['name'],
										 'SKU': orderlists['order_products'][i]['product']['sku'],
										 'Quantity Ordered': orderlists['order_products'][i]['quantity'],
										 'Unit Weight': orderlists['order_products'][i]['weight'],
										 'Unit Price': orderlists['order_products'][i]['product_price']})


							order_substitute_products_list = order_products_list = []
							orderlists['lat_val'] = orderlists['long_val'] = None

				data = {
					"status": 1,
					# "data":order_data,
					"api_status": "success", "file_name": file_name,
					"message": "Order details has been found",
					"export_file_path": export_file_path
				}
			else:

				data = {
					"status": 0,
					"api_status": "error",
					"file_name": "",
					"message": "No order details has been found",
					"export_file_path": ""
				}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data = {"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),
					"msg": str(error), "message": "Something went wrong"}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)