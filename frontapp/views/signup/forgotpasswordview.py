from django.http import HttpResponse
from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from webservices.models import *
from django.core.mail import EmailMultiAlternatives
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user_model, login
from django.db.models import Q
import json
from django.http import JsonResponse
from twilio.rest import Client
import urllib.request
import random
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
import hashlib
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
import base64
import datetime
from django.utils import timezone 
from webservices.views import loginview
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.hashers import make_password,check_password
from webservices.views.emailcomponent import emailcomponent

# forgot password webservices receiveing email and send link to the email address with random number
@csrf_exempt
def forgotpassword(request) :
	if request.method == 'POST':
		requestdata = JSONParser().parse(request)

		email = requestdata['email'].strip()
		check_email = EngageboostUsers.objects.filter(email__iexact=email,isblocked='n',isdeleted='n').count()
		name = EngageboostUsers.objects.filter(email__iexact=email,isblocked='n',isdeleted='n').first()
		if  check_email == 0:			
			data = {
			'message': 'This email does not exist',
			'status' : '0',
			}
			return JsonResponse(data)
		else:
			first_name =name.first_name		
			items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
			pin = str(random.randint(11111,99999))
			pin = urlsafe_base64_encode(force_bytes(pin))
			pin = str(pin)
			pin = pin.replace("b","")
			pin = pin.replace("'","")

			now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
			now_date = now_utc
			newdate = now_date + datetime.timedelta(minutes=30)
			date = urlsafe_base64_encode(force_bytes(newdate))
			ex = str(date) 
			ex = ex.replace("b","")
			ex = ex.replace("'","")
			pincode = pin + '_' + ex
			status_code = EngageboostUsers.objects.filter(email__iexact=email,isblocked='n',isdeleted='n').update(verified_code=pin)
			
			c = {
				'email': email,
				'domain': "https://www.gogrocery.ae", #request.META['HTTP_HOST'],
				# 'domain': "http://192.168.0.187:55", #request.META['HTTP_HOST'],
				'site_name': 'gogrocery.ae',
				# 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				# 'user': user,
				# 'token': default_token_generator.make_token(user),
				'protocol': 'https',
				}
			#link = "https://www.gogrocery.ae/reset-password/"+pincode+"/?link="
			link = "https://gogrocery.ae/reset-password/"+pincode+"/?link="
			#print('++++++++++',link)
			# link = "http://192.168.0.187:55/reset-password/"+pin+"/"
			email_template_name='site_api/password_reset_email.html'
			subject = "Forgot Password"
			message = 'Hi'+' '+ first_name +','+'<br><br>We received a request to reset your password<br>'+'<br><a href="'+link+'">Click </a> here to change your password'
			try:
				# send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False, html_message=message)
				emailcomponent.SendOtherMail(email,'support@gogrocery.ae',subject,message)
				msg = {"reset_password":['Reset password link has been sent to your email id %s, please check your mail.' %(email),]}
				success_message = {'success_message':msg, "name":first_name,'status' : '1','message':'Reset password link has been sent to your email id %s, please check your mail.' %(email)}
				return JsonResponse(success_message)
			except (TypeError, ValueError, OverflowError):
				msg = {"authorization":['Error in sending reset password mail. Please try again later.',]}
				errors = {'errors':msg}
				return Response(errors, status=status.HTTP_400_BAD_REQUEST)

# verification of the user code webservices 
@csrf_exempt
def verification(request) :
	company_db = loginview.db_active_connection(request)
	if request.method == 'POST':
		requestdata = JSONParser().parse(request)
		code = requestdata['code']
		email = requestdata['email']
		code1 = EngageboostUsers.objects.filter(verified_code=code,email__iexact=email).count()
		if  code1 == 0:
			data = {
			'message': 'This is not a valid verification code',
			'status' : '0',
			}
			return JsonResponse(data)
		else:
			data = {
			'message': 'Success',
			'status' : '1',
			'code'   : code,
			'email'   : email
			}
			return JsonResponse(data)

@csrf_exempt
def PasswordResetConfirmView(request):
	if request.method == 'POST':
		requestdata = JSONParser().parse(request)
		new_password    = requestdata['new_password']
		confirm_password    = requestdata['confirm_password']
		pin_code    = requestdata['pin_code']
		gen_password = make_password(new_password, None, 'md5')
		decodetimestrip= pin_code.split("_")
		pin = decodetimestrip[0]
		validatetime = decodetimestrip[1]
		decodetime = urlsafe_base64_decode(force_bytes(validatetime)).decode()
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		nowdate = str(now_utc)
		if decodetime >= nowdate:
			if str(new_password) == str(confirm_password):
				user = EngageboostUsers.objects.filter(verified_code = pin,isblocked='n',isdeleted='n').first()
				if user:
					updata={
						"password":gen_password,
						"verified_code":''
					}
					EngageboostUsers.objects.filter(verified_code = pin,isblocked='n',isdeleted='n').update(**updata)
					data = {
						'status':1,
						'api_status':'',
						'message':'Successfully Updated',
					}
				else:
					data = {
						'status':0,
						'api_status':'',
						'message':'Verification code not match.',
					}
			else:
				data = {
					'status':0,
					'api_status':'',
					'message':'Password and confirm password not match.',
				}
		else:
			data = {
				'status':0,
				'api_status':'',
				'message':'Your time is expired',
				}
		
		return JsonResponse(data)