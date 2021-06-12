from django.http import HttpResponse
from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from webservices.models import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user_model, login
from django.db.models import Q
import json
from django.http import JsonResponse
from twilio.rest import Client
import urllib.request
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import random
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
import hashlib
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from webservices.views import loginview

@csrf_exempt
# user registration and login with google 
def usercreate(request) :
	company_db = loginview.db_active_connection(request)
	if request.method == 'POST':
		requestdata = JSONParser().parse(request)
		google_login_id = requestdata['google_login_id']
		first_name = requestdata['first_name']
		last_name = requestdata['last_name']
		fullname = first_name+' '+last_name
		email = requestdata['email']
		ip_address = requestdata['ip_address']
	   
		cnt = EngageboostUsers.objects.using(company_db).filter(google_login_id=google_login_id).count()
		if  cnt == 0:
			email_user = email.split('@')
			
			cnt1 = EngageboostUsers.objects.using(company_db).filter(username=email_user[0]).count()
			
			if  cnt1 == 0:
				username=email_user[0]
				
			else: 
				items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
				pin = str(random.randint(11,99))
				cnt2 = EngageboostUsers.objects.using(company_db).filter(username=email_user[0]+pin).count()
				if cnt2 ==0:
					username=email_user[0]+pin
				else:
					items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
					pin = str(random.randint(11111,99999))
					username=email_user[0]+pin

			User = EngageboostUsers.objects.using(company_db).create(email=email,google_login_id=google_login_id,first_name=first_name,last_name=last_name,company_id='1',country_id='65',role_id='1',lead_manager_id='1',createdby_id='1',modifiedby_id=1,isblocked='n',isdeleted='n',username=username,employee_name=fullname,designation='User',last_login=timezone.now(),created_date=timezone.now(),modified_date=timezone.now(),password='n',user_type='backend',ip_address=ip_address)
			user = EngageboostUsers.objects.using(company_db).get(google_login_id=google_login_id)
			user_id = user.id
			token=Token.objects.using(company_db).get_or_create(user=User)
			auth = Token.objects.using(company_db).get(user_id=user_id)
			# GlobalSettings = EngageboostGlobalSettings.objects.using(company_db).get(createdby=user_id)
			user_id = user.id
			first_name = user.first_name
			last_name = user.last_name
			data = {

			'status':1,
			'user_id': user_id,
			'token'  : auth.key,
			'first_name':first_name,
			'last_name' : last_name,
   #          'gl_website_id': GlobalSettings.website_id,
			# 'gl_date_format': GlobalSettings.date_format,
			# 'gl_image_resize': GlobalSettings.image_resize,
			# 'gl_timezone_id': GlobalSettings.timezone_id,
			# 'gl_orderid_format': GlobalSettings.orderid_format,
			# 'gl_sms_auth_key': GlobalSettings.sms_auth_key,
			# 'gl_sms_check': GlobalSettings.sms_check,
			# 'gl_sms_sender_id': GlobalSettings.sms_sender_id,
			# 'gl_itemlisting_backend': GlobalSettings.itemlisting_backend,
			# 'gl_fb_store_app_id': GlobalSettings.fb_store_app_id,
			# 'gl_fb_store_secret': GlobalSettings.fb_store_secret,
			# 'gl_fb_login_id': GlobalSettings.fb_login_id,
			# 'gl_fb_login_secret': GlobalSettings.fb_login_secret,
			# 'gl_google_application_name': GlobalSettings.google_application_name,
			# 'gl_google_login_client_id': GlobalSettings.google_login_client_id,
			# 'gl_google_login_client_secret': GlobalSettings.google_login_client_secret,
			# 'gl_google_login_redirect_url': GlobalSettings.google_login_redirect_url,
			# 'gl_is_ebay_store_on': GlobalSettings.is_ebay_store_on,
			# 'gl_sms_route': GlobalSettings.sms_route,
			# 'gl_sms_route': GlobalSettings.sms_route,
			# 'gl_smtp_server': GlobalSettings.smtp_server,
			# 'gl_smtp_port': GlobalSettings.smtp_port,
			# 'gl_smtp_username': GlobalSettings.smtp_username,
			# 'gl_smtp_password': GlobalSettings.smtp_password,
			# 'gl_no_of_item_picklist': GlobalSettings.no_of_item_picklist,

			}
			return JsonResponse(data)
		else:
			user = EngageboostUsers.objects.using(company_db).get(google_login_id=google_login_id)
			user_id = user.id
			first_name = user.first_name
			last_name = user.last_name
			token=Token.objects.using(company_db).get_or_create(user=user_id)
			auth = Token.objects.using(company_db).get(user_id=user_id)
			
			# GlobalSettings = EngageboostGlobalSettings.objects.using(company_db).get(createdby=user_id)
			EngageboostUsers.objects.using(company_db).filter(google_login_id=google_login_id).update(last_login=datetime.now(),isdeleted='n',isblocked='n',ip_address=ip_address)
			data = {

			'status':1,
			'user_id': user_id,
			'token'  : auth.key,
			'first_name':first_name,
			'last_name' : last_name,
   #          'gl_website_id': GlobalSettings.website_id,
			# 'gl_date_format': GlobalSettings.date_format,
			# 'gl_image_resize': GlobalSettings.image_resize,
			# 'gl_timezone_id': GlobalSettings.timezone_id,
			# 'gl_orderid_format': GlobalSettings.orderid_format,
			# 'gl_sms_auth_key': GlobalSettings.sms_auth_key,
			# 'gl_sms_check': GlobalSettings.sms_check,
			# 'gl_sms_sender_id': GlobalSettings.sms_sender_id,
			# 'gl_itemlisting_backend': GlobalSettings.itemlisting_backend,
			# 'gl_fb_store_app_id': GlobalSettings.fb_store_app_id,
			# 'gl_fb_store_secret': GlobalSettings.fb_store_secret,
			# 'gl_fb_login_id': GlobalSettings.fb_login_id,
			# 'gl_fb_login_secret': GlobalSettings.fb_login_secret,
			# 'gl_google_application_name': GlobalSettings.google_application_name,
			# 'gl_google_login_client_id': GlobalSettings.google_login_client_id,
			# 'gl_google_login_client_secret': GlobalSettings.google_login_client_secret,
			# 'gl_google_login_redirect_url': GlobalSettings.google_login_redirect_url,
			# 'gl_is_ebay_store_on': GlobalSettings.is_ebay_store_on,
			# 'gl_sms_route': GlobalSettings.sms_route,
			# 'gl_sms_route': GlobalSettings.sms_route,
			# 'gl_smtp_server': GlobalSettings.smtp_server,
			# 'gl_smtp_port': GlobalSettings.smtp_port,
			# 'gl_smtp_username': GlobalSettings.smtp_username,
			# 'gl_smtp_password': GlobalSettings.smtp_password,
			# 'gl_no_of_item_picklist': GlobalSettings.no_of_item_picklist,
			}
			return JsonResponse(data)
# create otp for login with phonenumber			
@csrf_exempt			
def createotp(request):
	company_db = loginview.db_active_connection(request)
	if request.method == 'POST':
		requestdata = JSONParser().parse(request)
		mobile_number = requestdata['username']
		cnt = EngageboostUsers.objects.using(company_db).filter(phone=mobile_number).count()
		if cnt == 0:
			data = {
			'status': 0,
			'message': 'Mobile Number does\'t exist',
			}
			return JsonResponse(data)
		else:
			items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
			pin = str(random.randint(1111,9999))
			message="Your KWAME OTP is "+pin+".The otp is valid for one minute from now."

			cnt_check = EngageboostOTP.objects.using(company_db).filter(mobile=mobile_number).count()
			if cnt_check ==0:
				EngageboostOTP.objects.using(company_db).create(mobile=mobile_number,otp=pin)
			else:
				EngageboostOTP.objects.using(company_db).filter(mobile=mobile_number).update(otp=pin)

			# data = {
			# 'mobile_number': mobile_number,
				
			# }
			# return JsonResponse(data)
			# account_sid ="ACd9f356f4a77f21314139221e9fb22060"
			# auth_token = "825da6ac35be54e5094e1fac6a6ee57d"
			# client = Client(account_sid, auth_token)
			# message = client.messages.create(
			# 	   body="%s" % message,
			# 	   to="+91"+mobile_number,
			# 	   from_="+17125609076",
			#    )
			account_sid ="AC8b7fa38f888b0b581031eb40c2bfb0ae"
			auth_token = "15553a55afb2a0addd21a97e9a7a865e"
			client = Client(account_sid, auth_token)
			message = client.messages.create(
				   body="%s" % message,
				   to="+91"+mobile_number,
				   from_="+12513339015",
			   )
			
			data = {
			'status': 1,
			'message': 'OTP has been sent to your mobile number',
			}
			return JsonResponse(data)
# check opt given by user side
@csrf_exempt			
def checkotp(request):
	company_db = loginview.db_active_connection(request)
	if request.method == 'POST':
		requestdata = JSONParser().parse(request)
		mobile_number = requestdata['username']
		pin = requestdata['pin']
		ip_address = requestdata['ip_address']
		cnt = EngageboostOTP.objects.using(company_db).filter(mobile=mobile_number).count()
		if cnt == 0:
			# return HttpResponse(fullPath+'verify/'+str(enc))
			data = {
				'status': 'Mobile Number or OTP does\'t match',
			}
			return JsonResponse(data)
		else:
			user = EngageboostOTP.objects.using(company_db).get(mobile=mobile_number)
			otp=user.otp
			user_table = EngageboostUsers.objects.using(company_db).get(phone=mobile_number)
			user_id=user_table.id
			first_name = user_table.first_name
			last_name = user_table.last_name
			auth = Token.objects.using(company_db).get(user_id=user_id)
			EngageboostUsers.objects.using(company_db).filter(phone=mobile_number).update(last_login=datetime.now(),ip_address=ip_address)
			if otp == pin:
				data = {
				'status': 'Success',
				'user': user_id,
				'token'  : auth.key,
				'first_name':first_name,
				'last_name' : last_name,
				# 'gl_website_id': GlobalSettings.website_id,
				# 'gl_date_format': GlobalSettings.date_format,
				# 'gl_image_resize': GlobalSettings.image_resize,
				# 'gl_timezone_id': GlobalSettings.timezone_id,
				# 'gl_orderid_format': GlobalSettings.orderid_format,
				# 'gl_sms_auth_key': GlobalSettings.sms_auth_key,
				# 'gl_sms_check': GlobalSettings.sms_check,
				# 'gl_sms_sender_id': GlobalSettings.sms_sender_id,
				# 'gl_itemlisting_backend': GlobalSettings.itemlisting_backend,
				# 'gl_fb_store_app_id': GlobalSettings.fb_store_app_id,
				# 'gl_fb_store_secret': GlobalSettings.fb_store_secret,
				# 'gl_fb_login_id': GlobalSettings.fb_login_id,
				# 'gl_fb_login_secret': GlobalSettings.fb_login_secret,
				# 'gl_google_application_name': GlobalSettings.google_application_name,
				# 'gl_google_login_client_id': GlobalSettings.google_login_client_id,
				# 'gl_google_login_client_secret': GlobalSettings.google_login_client_secret,
				# 'gl_google_login_redirect_url': GlobalSettings.google_login_redirect_url,
				# 'gl_is_ebay_store_on': GlobalSettings.is_ebay_store_on,
				# 'gl_sms_route': GlobalSettings.sms_route,
				# 'gl_sms_route': GlobalSettings.sms_route,
				# 'gl_smtp_server': GlobalSettings.smtp_server,
				# 'gl_smtp_port': GlobalSettings.smtp_port,
				# 'gl_smtp_username': GlobalSettings.smtp_username,
				# 'gl_smtp_password': GlobalSettings.smtp_password,
				# 'gl_no_of_item_picklist': GlobalSettings.no_of_item_picklist,	
				}
				return JsonResponse(data)
			else:
				data = {
				'status': 'Mobile Number or OTP does\'t match',
					
				}
				return JsonResponse(data)
#delete group web services
def delete_group(request):
	company_db = loginview.db_active_connection(request)
	if request.method == 'POST':
		requestdata = JSONParser().parse(request)
		group_id = requestdata['id']
		cnt = EngageboostGroups.objects.using(company_db).filter(id=group_id).count()
		if  cnt != 0:
			queryset=EngageboostGroups.objects.using(company_db).filter(id=group_id).update(isdeleted=y)
			data = {
			'status':1,
			'message': 'Deleted Successfully!',
			}
			return JsonResponse(data)		
			




		
		
