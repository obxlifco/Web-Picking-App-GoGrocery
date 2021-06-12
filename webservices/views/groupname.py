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
from webservices.views import loginview
 




    # """ Listing Function to Fetch Role """
@csrf_exempt
def list_role(request):
	company_db = loginview.db_active_connection(request)
    if request.method == 'POST':
        queryset = EngageboostGropus.objects.using(company_db).all().filter(isdeleted=0).order_by('-id')
        name=queryset.name
        data = {
        'status':name,
        'message':'Something Went Wrong!'
        }
        return JsonResponse(data)