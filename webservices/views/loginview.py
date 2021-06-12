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
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
import hashlib
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password,check_password
import re
from django.conf import settings
from webservices.views import loginview
import socket
#from Crypto.Cipher import AES
#from pkcs7 import PKCS7Encoder
import base64
from webservices.serializers import BaseCurrencyRateSerializer,UserSerializer
from webservices.views.common import common
# from cryptography.fernet import Fernet
# from django.conf import settings
# from django.core import signals
# from django.db.utils import (DEFAULT_DB_ALIAS,DataError,ConnectionHandler,ConnectionRouter, OperationalError, IntegrityError, InternalError)
#  connections = ConnectionHandler()
 
# -router = ConnectionRouter(settings.DATABASE_ROUTERS)
# +router = ConnectionRouter()

@csrf_exempt
# login in method for Boost admin with email/username and password
def db_active_connection(request):
    current_url = request.META.get('HTTP_REFERER', '')
    if(current_url):
        current_url=re.sub('^https?:\/\/', '', current_url).split('/')
        current_url=current_url[0]
    else:
        current_url= 'http://localhost:3000/'
    url_check = EngageboostCompanies.objects.filter(website_url=current_url).count()

    if url_check>0:
        db_fetch = EngageboostCompanies.objects.get(website_url=current_url)
        company =db_fetch.company_name
        return company
    else:
        return 0

@csrf_exempt
# login in method for Boost admin with email/username and password
def login(request): 
    requestdata = JSONParser().parse(request)
    user_mail  = requestdata['username']
    user_passw = requestdata['password']
    ip = requestdata['ip_address']
    if ip == "":
        ip = request.META['REMOTE_ADDR']

    pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"   
    valid_email=re.match(pattern,user_mail)

    current_url = request.META['HTTP_ORIGIN'] + '/'
    #current_url = request.META['HTTP_REFERER']
    url_check = EngageboostCompanies.objects.filter(website_url=current_url).count()
    url_check=1
    if url_check>0:
        db_fetch = EngageboostCompanies.objects.get(website_url=current_url)
        company =db_fetch.company_name
        cnt=EngageboostUsers.objects.using(company).filter(email=user_mail)
        cnt1=EngageboostUsers.objects.using(company).filter(username=user_mail)
        if cnt.count() > 0:
            User = cnt.first()
        elif cnt1.count() > 0:
            User = cnt1.first()
        else:
            data = {
            'status':0,
            'message': 'Username / password mismatch.'
            }
            return JsonResponse(data)

        user_type = User.user_type
        password_check=User.check_password(user_passw)
        token=Token.objects.using(company).get_or_create(user=User)
        auth = Token.objects.using(company).get(user_id=User.id)
        EngageboostUsers.objects.using(company).filter(email=user_mail).using(db_fetch.company_name).update(last_login=datetime.now(),ip_address=ip)
        if password_check==True and user_type == 'backend':
            if(User.isblocked=='n'):
                if(User.isdeleted=='n'):
                    managerType = ''
                    if EngageboostSuppliers.objects.using(company).filter(user_id = User.id,isdeleted='n').exists(): 
                        managerType = 'Suppliers'
                    if managerType == '':
                        if EngageboostWarehouseManager.objects.using(company).filter(manager_id = User.id,isdeleted='n').exists():
                            managerType = 'WarehouseManager'
                    
                    #WAREHOUSE CHECKING
                    warehouse_id = ""
                    if User.issuperadmin !='Y':
                        listOfWarehouseIds = EngageboostWarehouseMasters.objects.using(company).filter(website_id=User.website_id).values_list('id')
                        warehouseManager = EngageboostWarehouseManager.objects.using(company).filter(manager_id = User.id,isdeleted='n',isblocked='n',warehouse_id__in=listOfWarehouseIds).order_by('-id').first()
                        if warehouseManager:
                            warehouse_id = warehouseManager.warehouse_id
                    
                    UserDetails = UserSerializer(User)
                    isSubAdmin="N"
                    if UserDetails:
                        if UserDetails.data["role"]["id"] == 4:
                            isSubAdmin="Y"
                    
                    curencyObj = EngageboostCurrencyRates.objects.filter(isbasecurrency = 'y',isdeleted = 'n',isblocked = 'n').first()
                    #print(curencyObj.engageboost_currency_master_id)
                    currencySerialise = BaseCurrencyRateSerializer(curencyObj,partial=True)
                    #print(currencySerialise.data)
                    currencyDetails = currencySerialise.data
                    # print(currencyDetails)

                    find_global_settings = EngageboostGlobalSettings.objects.using(company).filter(website_id=User.website_id,isdeleted = 'n',isblocked = 'n')
                    if find_global_settings.count()>0:
                        GlobalSettings = find_global_settings.first()
                    common.saveloginhistory(User.id,ip,'login')
                    data = {
                            'status':1,
                            'first_name':User.first_name,
                            'designation':User.designation,
                            'last_name':User.last_name,
                            'user_type':User.user_type,
                            'token'  : auth.key,
                            'user_id': User.id,
                            'role_id': User.role_id,
                            'email':User.email,
                            'username': User.username,
                            'reset_password': User.reset_password,
                            'company_id':User.company_id,
                            'managerType':managerType,
                            'isSuperAdmin':User.issuperadmin,
                            'isSubAdmin':isSubAdmin,
                            'website_id':User.website_id,
                            'currencyId' : currencyDetails['engageboost_currency_master']['id'],
                            'currencyCode' : currencyDetails['currency_code'],
                            'currencysymbol' : currencyDetails['engageboost_currency_master']['currencysymbol'],
                            'elastic_store_name':settings.STORE_NAME,
                            'elastic_host':settings.ELASTIC_HOST,
                            'elastic_port':settings.ELASTIC_PORT,
                            'elastic_url':settings.ELASTIC_URL,
                            'gl_date_format': GlobalSettings.date_format,
                            'gl_timezone_id': GlobalSettings.timezone_id,
                            'applicable_tax': GlobalSettings.applicable_tax,
                            'warehouse_id' : warehouse_id
                            # 'gl_image_resize': GlobalSettings.image_resize,
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
                    'status':0,
                    'message': 'Username / password mismatch.'
                    }
                return JsonResponse(data)
            else:
                data = {
                    'status':0,
                    'message': 'Your account is blocked. If you want to activate it please contact administrator.'
                }
        else:
            data = {
                'status':0,
                'message': 'Username / password mismatch.'
            }
    else:
        data = {
            'status':0,
            'message': 'Invalid Domain name '+current_url
        }    
    return JsonResponse(data)

@csrf_exempt                
def insertdata(request):
    company_db = loginview.db_active_connection(request)
    error='Error generated'
    if request.method=='POST':
        requestdata=JSONParser().parse(request)
        user_email  = requestdata['email']
        user_passw = requestdata['password']
        hash_password =make_password(user_passw, None, 'md5')
        #print(hash_password)
        country_id='121'
        role_id='1'
        lead_manager_id='277'
        createdby_id='277'
        company_db = loginview.db_active_connection(request)
        User=EngageboostUsers.objects.using(company_db).create(
                email=user_email, 
                password=hash_password,
                username='Shamol',
                first_name='Shamol',
                is_superuser='f',
                last_name='Singha',
                is_staff='t',
                is_active='t', 
                # date_joined=datetime.now(), 
                company_id='15', 
                business_name='bms', 
                boost_url='www.bms.com/1125', 
                website_url='www.bms.com/1125', 
                company_logo='abc.png', 
                employee_name='abc', 
                designation='abc', 
                image_name='abc.png', 
                reset_password='12', 
                city='kolkata', 
                state='wb', 
                postcode='7000091',
                phone='9674419914', 
                country_id=country_id, 
                role_id=role_id, 
                lead_manager_id=lead_manager_id, 
                createdby_id=createdby_id, 
                # created_date=datetime.now(), 
                modifiedby_id='121', 
                # modified_date=datetime.now(),
                isblocked='n', 
                isdeleted='n', 
                is_verified='1', 
                verified_code='002', 
                refferal_code='123', 
                google_login_id='null', 
                device_token_ios='123654', 
                device_token_android='123654', 
        )
        User.save()
        token=Token.objects.using(company_db).get_or_create(user=User)
        response_data={'user_email':user_email, 'user_passw':user_passw}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse({"error":error})
