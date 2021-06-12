from django.http import HttpResponse
from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from webservices.models import *
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user_model, login, authenticate
from django.db.models import Q
import json
from django.http import JsonResponse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from validate_email import validate_email
from bcrypt import hashpw, gensalt
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
import hashlib
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password,check_password
import re
from webservices.views import loginview

@csrf_exempt
def changepassword(request):
	company_db = loginview.db_active_connection(request)

	if request.method=='POST':
		requestdata=JSONParser().parse(request)
		code  = requestdata['code']
		cnt = EngageboostUsers.objects.using(company_db).filter(verified_code=code).count()
		if cnt == 0:
			data = {
			'message': 'This Code  Does\'t Exsits',
			'status':'0',
				
			}
			return JsonResponse(data)
		else:
			user_passw = requestdata['password']
			hash_password =make_password(user_passw, None, 'md5')
			
			EngageboostUsers.objects.using(company_db).filter(verified_code=code,isdeleted='n',isblocked='n').update(password=hash_password)

			data = {
			'message': 'Password has been successfully updated. Please login to continue.',
			'status':'1',
				
			}
			return JsonResponse(data)

	else:
		data = {
		'message': 'Something went wrong. Try again.',
		'status':'0',	
		}
		return JsonResponse(data)
		
	
