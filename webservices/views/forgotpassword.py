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
# forgot password webservices receiveing email and send link to the email address with random number
@csrf_exempt
def forgotpassword(request) :
	company_db = loginview.db_active_connection(request)
	if request.method == 'POST':
		requestdata = JSONParser().parse(request)
	   
		email = requestdata['email']
		check_email = EngageboostUsers.objects.using(company_db).filter(email=email).count()
		name = EngageboostUsers.objects.using(company_db).get(email=email)
		first_name =name.first_name
		if  check_email == 0:
			
			data = {
			'message': 'This email does not exist',
			'status' : '0',
			}
			return JsonResponse(data)

		else:
			
			items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
			pin = str(random.randint(11111,99999))
			c = EngageboostUsers.objects.using(company_db).filter(email=email).update(verified_code=pin)


			subject, from_email, to = 'Update Password', 'aritra.chowdhury@navsoft.in', email
			text_content = 'Update Password'
			link =settings.SITE_URL+'/#/'+'verify_code/'
			html_content = 'Hi'+' '+ first_name +','+'<br><br>We received a request to reset your password<br>'+'<br><a href="'+link+'">Click here to change your password</a>'+'<br><br>Alternatively,You can enter the following password reset code  '+' : '+pin
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			# text = 'Hi'+ first_name <br>+'You can enter the following Password reset code  '+' : '+pin
			# text = 'Cleck Here to Reset Your Password'+' : '+fullPath+a
			# return HttpResponse(fullPath+'verify/'+str(enc))
			# send_mail('Update Password',text,'aritra.chowdhury@navsoft.in',[email],fail_silently=False,
			data = {
			'message': 'verification code has been send to this email id'+' '+email,
			'status' : '1',
			}
			return JsonResponse(data)
# verification of the user code webservices 
@csrf_exempt
def verification(request) :
	company_db = loginview.db_active_connection(request)
	if request.method == 'POST':
		requestdata = JSONParser().parse(request)
		code = requestdata['code']
		email = requestdata['email']
		code1 = EngageboostUsers.objects.using(company_db).filter(verified_code=code,email=email).count()
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