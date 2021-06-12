from webservices.models import *
from webservices.serializers import *
# from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
import datetime
from rest_framework import generics
from rest_framework.response import Response
from django.http import JsonResponse
import socket
from webservices.views import loginview
import sys
import traceback
import json
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail, get_connection
import random
import urllib.request
from urllib.parse import urlencode, quote_plus, urlparse
from django.core.files.storage import FileSystemStorage
import os
import shutil
from django.apps import apps
import requests
import tinys3
import time
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from django.db import connection
from django.template.defaultfilters import slugify

import base64
from webservices.views.emailcomponent import emailcomponent
from decimal import Decimal
# from webservices.views.inventory.threading import *
from webservices.views.common.threading import *
from pyfcm import FCMNotification
# from rest_framework.decorators import authentication_classes, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.parsers import JSONParser

def connect_elastic():
    es = Elasticsearch([{'host': settings.ELASTIC_HOST, 'port': settings.ELASTIC_PORT,'timeout':3600}])
    es.cluster.health(wait_for_status='yellow', request_timeout=30)

    return es

es = connect_elastic()

def format_date(datestr):
    try:
        datestr = datetime.datetime.fromtimestamp(datestr)
    except:
        pass
    try:
        datestr = datetime.datetime.strptime(datestr, "%Y-%m-%d")
    except:
        pass
    try:
        datestr = datetime.datetime.strptime(datestr, "%d-%m-%Y")
    except:
        pass
    try:
        datestr = datetime.datetime.strptime(datestr, "%m-%d-%Y")
    except:
        pass

    try:
        datestr = datetime.datetime.strptime(datestr, "%Y/%m/%d")
    except:
        pass
    try:
        datestr = datetime.datetime.strptime(datestr, "%d/%m/%Y")
    except:
        pass
    try:
        datestr = datetime.datetime.strptime(datestr, "%m-%d-%Y")
    except:
        pass

    try:
        datestr = datetime.datetime.strptime(datestr, "%y-%m-%d")
    except:
        pass
    try:
        datestr = datetime.datetime.strptime(datestr, "%d-%m-%y")
    except:
        pass
    try:
        datestr = datetime.datetime.strptime(datestr, "%m-%d-%y")
    except:
        pass

    try:
        datestr = datetime.datetime.strptime(datestr, "%y/%m/%d")
    except:
        pass
    try:
        datestr = datetime.datetime.strptime(datestr, "%d/%m/%y")
    except:
        pass
    try:
        datestr = datetime.datetime.strptime(datestr, "%m/%d/%y")
    except:
        pass

    try:
        datestr = datestr.strftime('%Y-%m-%dT%H:%M:%SZ')
    except:
        pass

    return datestr

def getProductBarcode(product_id):
    barcodes = []
    multi_barcode = ""
    product_barcodes=EngageboostMultipleBarcodes.objects.all().filter(product_id=product_id,isdeleted='n',isblocked='n').order_by('id').values("barcode")
    for item in product_barcodes:
        barcodes.append(item["barcode"])
    if len(barcodes)>0:
        multi_barcode = ",".join(barcodes)
    return multi_barcode

def getAllCountries(company_db):
    settings1 = EngageboostCountries.objects.using(company_db).all()
    if settings1:
        serializer1 = GlobalsettingscountriesSerializer(settings1, many=True)
        data={"status":1,"countrylist":serializer1.data}
        return data
    else:
        data={"status":0,"countrylist":[]}
        return data

class CommonCountries(generics.ListAPIView):
    def get(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        settings1 = EngageboostCountries.objects.using(company_db).all().order_by('country_name')
        if settings1:
            serializer1 = GlobalsettingscountriesSerializer(settings1, many=True)
            data={"status":1,"countrylist":serializer1.data}
            return Response(data)
        else:
            data={"status":0,"countrylist":[]}
            return Response(data)

class CountryDetails(generics.ListAPIView):
    def get(self, request, pk, format=None):
        company_db = loginview.db_active_connection(request)
        try:
            settings1 = EngageboostCountries.objects.using(company_db).filter(id=pk)
            if settings1.count()>0:
                serializer1 = settings1.values().first()
                # serializer1 = GlobalsettingscountriesSerializer(settings1, partial=True)
                data={"status":1,"api_status":{"id":serializer1['id'],"country_name":serializer1['country_name']}}
                return Response(data)
            else:
                data={"status":0,"api_status":[]}
                return Response(data)
        except:
            data={"status":0,"api_status":[]}
            return Response(data)

class StateList(generics.ListAPIView):
    def get(self, request, country_id, format=None):
        company_db = loginview.db_active_connection(request)
        settings_ser = EngageboostStates.objects.using(company_db).all().filter(country_id=country_id).order_by('state_name')
        serializer_ser = StatesSerializer(settings_ser,many=True)
        if(serializer_ser):
            data ={
                'status':1,
                'states':serializer_ser.data,
                'message':'Data Found',
            }
        else:
            data ={
                'status':0,
                'api_status':serializer.errors,
                'message':'Data Not Found',
                }
        return Response(data)

class CustomerById(generics.ListAPIView):
    def get(self, request, customer_id, email, format=None):
        company_db = loginview.db_active_connection(request)
        if int(customer_id)!=0:
            cond = EngageboostCustomers.objects.using(company_db).filter(id=customer_id).first()
        else:
            cond = EngageboostCustomers.objects.using(company_db).filter(email=email,isdeleted="n").first()

        if cond:
            serializer = CustomerSerializer(cond)
            if serializer:
                data ={"status":1,"api_status":serializer.data,"message":'Customer exists'}
            else:
                data ={"status":0,"api_status":serializer.errors,"message":'Data Not Found'}
        else:
            data ={"status":0,"api_status":'Customer does not exists',"message":'Customer does not exists'}
        return Response(data)

class CustomerGroupList(generics.ListAPIView):
    def get(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        cond = EngageboostCustomerGroup.objects.using(company_db).filter(isdeleted='n',isblocked='n').all()
        if cond:
            serializer = CustomerGroupSerializer(cond,many=True)
            if serializer:
                data ={"status":1,"api_status":serializer.data,"message":'Customer Group List'}
            else:
                data ={"status":0,"api_status":serializer.errors,"message":'Data Not Found'}
        else:
            data ={"status":0,"api_status":'No Customer Group Found',"message":'No Customer Group Found'}
        return Response(data)

class MarketPlaceList(generics.ListAPIView):
    def get(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        cond = EngageboostChannels.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
        if cond:
            serializer = ChannelsSerializer(cond,many=True)
            if serializer:
                data ={"status":1,"api_status":serializer.data,"message":'Marketplace List'}
            else:
                data ={"status":0,"api_status":serializer.errors,"message":'Data Not Found'}
        else:
            data ={"status":0,"api_status":'No Marketplace Found',"message":'No Marketplace Found'}
        return Response(data)

class MarketPlaceListById(generics.ListAPIView):
    def get(self, request, id, format=None):
        company_db = loginview.db_active_connection(request)
        cond = EngageboostChannels.objects.using(company_db).filter(id=id).first()
        if cond:
            serializer = ChannelsSerializer(cond)
            if serializer:
                data ={"status":1,"api_status":serializer.data,"message":'Marketplace List'}
            else:
                data ={"status":0,"api_status":serializer.errors,"message":'Data Not Found'}
        else:
            data ={"status":0,"api_status":'No Marketplace Found',"message":'No Marketplace Found'}
        return Response(data)

class TagList(generics.ListAPIView):
    def get(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        cond = EngageboostTags.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
        if cond:
            serializer = TagsSerializer(cond,many=True)
            if serializer:
                data ={"status":1,"api_status":serializer.data,"message":'Tag List'}
            else:
                data ={"status":0,"api_status":serializer.errors,"message":'Data Not Found'}
        else:
            data ={"status":0,"api_status":'No tag found',"message":'No Tag Found'}
        return Response(data)

class WarehouseList(generics.ListAPIView):
    def get(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        cond = EngageboostWarehouseMasters.objects.using(company_db).all().filter(isdeleted='n', isblocked='n').values("id", "website_id", "name", "code", "country_id").order_by('name')
        if cond:
            serializer = WarehousemastersSerializer(cond,many=True)
            if serializer:
                for warehouse in serializer.data:
                    warehouse_manager_cond = EngageboostWarehouseManager.objects.using(company_db).filter(warehouse_id=warehouse["id"]).all()
                    if warehouse_manager_cond:
                        warehouse_manager_list=[]
                        warehouse_manager = WarehousemanagerSerializer(warehouse_manager_cond,many=True)
                        if warehouse_manager:
                            for warehousemanager in warehouse_manager.data:
                                if warehousemanager["manager"]:
                                    warehouse_manager_dict = {"id":warehousemanager["id"],"warehouse_id":warehousemanager["warehouse_id"],"manager_id":warehousemanager["manager"]["id"],"first_name":warehousemanager["manager"]["first_name"],"last_name":warehousemanager["manager"]["last_name"],"email":warehousemanager["manager"]["email"],"username":warehousemanager["manager"]["username"]}
                                    warehouse_manager_list.append(warehouse_manager_dict)

                        warehouse["warehouse_manager"] = warehouse_manager_list
                    else:
                        warehouse["warehouse_manager"] = []
                data ={"status":1,"api_status":serializer.data,"message":'Warehouse List'}
            else:
                data ={"status":0,"api_status":serializer.errors,"message":'Data Not Found'}
        else:
            data ={"status":0,"api_status":'No warehouse found',"message":'No warehouse Found'}
        return Response(data)


def save_order_activity(company_db,order_id=None,activity_time=None,status=None,msg=None,userId=None,activityType=1):
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    if userId is None or userId=='':
        userId = 1

    if activity_time is None:
        activity_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
    try:
        activity_arr = {
            "order_id":order_id,
            "activity_comments":msg,
            "status":status,
            "activity_date":activity_time,
            "user_ip_address":IPAddr,
            "user_id":userId,
            "activity_type":activityType
        }
        try:
            if product_id!=None and product_id!="":
                activity_arr['product_id'] = product_id
        except:
            pass

        try:
            if purchase_order_id!=None and purchase_order_id!="":
                activity_arr['purchase_order_id'] = purchase_order_id
        except:
            pass

        order_activities = EngageboostOrderActivity.objects.create(**activity_arr)
        data={'status':1,'api_status':order_activities.id, 'message': 'Order activity saved.'}
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error), 'message': str(error)}
    return data

def save_all_order_item_activity(company_db,order_id=None,activity_time=None,status=None,msg=None,userId=None,activityType=3,product_id=None):
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    if userId is None or userId=='':
        userId = 1

    if activity_time is None:
        activity_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
    try:
        all_products = EngageboostOrderProducts.objects.filter(order_id=order_id)
        if all_products.count()>0:
            all_products = all_products.all()
        activity_arr = {
            "order_id":order_id,
            "activity_comments":msg,
            "status":status,
            "activity_date":activity_time,
            "user_ip_address":IPAddr,
            "user_id":userId,
            "activity_type":activityType
        }
        try:
            if product_id!=None and product_id!="":
                activity_arr['product_id'] = product_id
        except:
            pass
        order_activities = EngageboostOrderActivity.objects.create(**activity_arr)
        data={'status':1,'api_status':order_activities.id, 'message': 'Order activity saved.'}
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error), 'message': str(error)}
    return data

def save_item_activity(company_db,order_id=None,activity_time=None,status=None,msg_type=1,userId=None,activityType=3,product_id=None,value=0,custom_order_id=None):
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    if userId is None or userId=='':
        userId = 1

    if activity_time is None:
        activity_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
    try:
        msg = ""
        if msg_type==1:
            msg = str(value)+" item sold on order number "+str(custom_order_id)
        elif msg_type==2:
            msg = "Item quantity increased to "+str(value)+" in order number "+str(custom_order_id)
        elif msg_type==3:
            msg = "Item quantity decreased to "+str(value)+" in order number "+str(custom_order_id)
        elif msg_type==4:
            msg = "Item price increased to "+str(value)+" in order number "+str(custom_order_id)
        elif msg_type==5:
            msg = "Item price decreased to "+str(value)+" in order number "+str(custom_order_id)

        activity_arr = {
            "order_id":order_id,
            "activity_comments":msg,
            "status":status,
            "activity_date":activity_time,
            "user_ip_address":IPAddr,
            "user_id":userId,
            "activity_type":activityType
        }
        try:
            if product_id!=None and product_id!="":
                activity_arr['product_id'] = product_id
        except:
            pass

        order_activities = EngageboostOrderActivity.objects.create(**activity_arr)
        data={'status':1,'api_status':order_activities.id, 'message': 'Order activity saved.'}
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error), 'message': str(error)}
    return data

def save_po_activity(company_db,purchase_order_id=None,activity_time=None,status=None,msg_type=1,userId=None,activityType=4,product_id=None,custom_order_id=None):
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    if userId is None or userId=='':
        userId = 1

    if activity_time is None:
        activity_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
    try:
        msg = ""
        if msg_type==1:
            msg = "Purchase order number "+str(custom_order_id)+" is created for this item"
        activity_arr = {
            "purchase_order_id":purchase_order_id,
            "activity_comments":msg,
            "status":status,
            "activity_date":activity_time,
            "user_ip_address":IPAddr,
            "user_id":userId,
            "activity_type":activityType
        }
        try:
            if product_id!=None and product_id!="":
                activity_arr['product_id'] = product_id
        except:
            pass

        order_activities = EngageboostOrderActivity.objects.create(**activity_arr)
        data={'status':1,'api_status':order_activities.id, 'message': 'Order activity saved.'}
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error), 'message': str(error)}
    return data

class GetGlobalSettings(generics.ListAPIView):
    def get(self,request,website_id):
        company_db = loginview.db_active_connection(request)
        GlobalSettings = getGlobalSettings(company_db,website_id)
        return Response(GlobalSettings)

def getGlobalSettings(company_db,website_id):
    condition = EngageboostGlobalSettings.objects.using(company_db).order_by("-id").filter(website_id=website_id,isdeleted='n',isblocked='n').first()
    if condition:
        globalSettings = GlobalsettingsSerializer(condition,partial=True)
        data = globalSettings.data
    else:
        data = {}
    return data

def GlobalSettings(website_id):
    condition = EngageboostGlobalSettings.objects.order_by("-id").filter(website_id=website_id,isdeleted='n',isblocked='n').first()
    if condition:
        globalSettings = GlobalsettingsSerializer(condition,partial=True)
        data = globalSettings.data
    else:
        data = {}
    return data

class CourierList(generics.ListAPIView):
    def get(self,request):
        company_db = loginview.db_active_connection(request)
        courier_info = get_courier_list(company_db)
        return Response(courier_info)

def get_courier_list(company_db):
    check_list=["courier","Courier"]
    courier_info_cond = EngageboostShippingMasters.objects.using(company_db).filter(shipping_type__in=check_list).all()
    if courier_info_cond:
        courier_info = ShippingSerializer(courier_info_cond,many=True)
        if courier_info:
            data ={"status":1, "api_status":courier_info.data, "message":'Courier List'}
        else:
            data ={"status":0, "api_status":courier_info.errors, "message":'No courier found'}
    else:
        data ={"status":0, "api_status":[],"message": 'No courier found'}
    return data

def getChannelInfo(company_db,channel_id):
    channelInfo = EngageboostChannels.objects.using(company_db).filter(id=channel_id).first()
    if channelInfo:
        channelInfo = ChannelsSerializer(channelInfo)
        if channelInfo:
            data ={"status":1, "api_status":channelInfo.data, "message":'Channel details'}
        else:
            data ={"status":0, "api_status":channelInfo.errors, "message":'No Channel found'}
    else:
        data ={"status":0, "api_status":[],"message": 'No Channel found'}
    return data

def getAutoResponder(company_db,shipment_status,webshop_id,warehouse_id,shipping_method_id,website_id, autoResponderId):
    # print(shipment_status, webshop_id ,warehouse_id , shipping_method_id ,website_id, autoResponderId)
    autoResponderId = int(autoResponderId)
    if shipment_status and webshop_id and warehouse_id and website_id:
        applicableResponder = EngageboostApplicableAutoresponders.objects.using(company_db).filter(website_id=website_id).order_by("-id")
        if shipment_status:
            applicableResponder = applicableResponder.filter(shipment_status=shipment_status)
        if warehouse_id:
            applicableResponder = applicableResponder.filter(applicable_for='Warehouse',applicable_chanel_id=warehouse_id)
        elif shipping_method_id:
            email_contain_data_arr = email_contain_data_arr.filter(applicable_for='ShippingProvider', applicable_chanel_id=shipping_method_id)
        else:
            applicableResponder = applicableResponder.filter(applicable_for='Channel',applicable_chanel_id=webshop_id)
        if applicableResponder.count()>0:
            applicableResponder = applicableResponder.first()
            autoResponderId = applicableResponder.auto_responder_id
    # print(autoResponderId)
    applicableResponder = EngageboostEmailTypeContents.objects.using(company_db).order_by("-id").filter(id=autoResponderId).first()
    if applicableResponder:
        applicableResponderSerializer = EmailTypeContentsSerializer(applicableResponder)
        data ={"status":1, "content":applicableResponderSerializer.data,"message": 'Auto Responder Data'}
    else:
        data ={"status":0, "content":{},"message": 'No Auto Responder Found'}
    return data

def loadCompanyDetails(company_db,website_id):
    websiteDetails = EngageboostCompanyWebsites.objects.using(company_db).order_by("-id").filter(id= website_id).first()
    data ={"status":1, "content":websiteDetails,"message": 'Auto Responder data'}
    return data

def getCountryDetails(company_db,country_id):
    countryDetails = EngageboostCountries.objects.using(company_db).order_by("-id").filter(id= country_id).first()
    if countryDetails:
        countryDetailsSerializer = GlobalsettingscountriesSerializer(countryDetails)
        data ={"status":1, "Country":countryDetailsSerializer.data,"message": 'Getting Country Information'}
    else:
        data ={"status":0, "Country":{},"message": "No information found"}
    return data

def getStateDetails(company_db,state_id):
    stateDetails = EngageboostStates.objects.using(company_db).order_by("-id").filter(id= state_id).first()
    data ={"status":1, "State":stateDetails,"message": 'Getting State information'}
    return data

def get_company_website(base_url):
    current_url = base_url
    if current_url is None:
        current_url='http://localhost:3000/'
    url_check = EngageboostCompanies.objects.filter(website_url=current_url).count()
    if url_check>0:
        db_fetch = EngageboostCompanies.objects.get(website_url=current_url)
        company_id = db_fetch.id
        company_website = EngageboostCompanyWebsites.objects.filter(engageboost_company_id=company_id).first()
        if company_website:
            company_website_serializer = CompanyWebsiteSerializer(company_website)
            company_website_serializer = company_website_serializer.data
            data = company_website_serializer
        else:
            company_website_serializer = {}
            data = {}
        return data
    else:
        data={}
        return data

def convert_datetime(date,time_zone=None,date_format="d-m-Y",offset=0.0):
    converted_date = date+ datetime.timedelta(hours=float(offset))
    converted_date = converted_date.strftime(str(date_format))
    return converted_date

def get_zonename(zone_id):
    if EngageboostZoneMasters.objects.filter(id=zone_id, location_type='Z').exists():
        get_record = EngageboostZoneMasters.objects.get(id=zone_id, location_type='Z')
        return get_record.name
    else:
        return None

def get_warehousename(warehouse_id):
    if warehouse_id:
        if EngageboostWarehouseMasters.objects.filter(id=warehouse_id).exists():
            get_record = EngageboostWarehouseMasters.objects.get(id=warehouse_id)
            return get_record.name
        else:
            return None
    else:
        return None
def get_areaname(area_id):
    if EngageboostZoneMasters.objects.filter(id=area_id, location_type='A').exists():
        get_record = EngageboostZoneMasters.objects.get(id=area_id, location_type='A')
        return get_record.name
    else:
        return None


def get_countryname(country_id):
    if EngageboostCountries.objects.filter(id=country_id).exists():
        get_record = EngageboostCountries.objects.get(id=country_id)
        return get_record.country_name

    else:
        return None


def get_statename(state_id):
    if EngageboostStates.objects.filter(id=state_id).exists():
        get_record = EngageboostStates.objects.get(id=state_id)

        return get_record.state_name

    else:
        return None


def get_managername(manager_id):
    if EngageboostDeliveryManagers.objects.filter(id=manager_id).exists():
        get_record = EngageboostDeliveryManagers.objects.get(id=manager_id)

        return get_record.name

    else:
        return None

def num_to_words(num):
    d = { 0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five',
          6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine', 10 : 'ten',
          11 : 'eleven', 12 : 'twelve', 13 : 'thirteen', 14 : 'fourteen',
          15 : 'fifteen', 16 : 'sixteen', 17 : 'seventeen', 18 : 'eighteen',
          19 : 'nineteen', 20 : 'twenty',
          30 : 'thirty', 40 : 'forty', 50 : 'fifty', 60 : 'sixty',
          70 : 'seventy', 80 : 'eighty', 90 : 'ninety' }
    k = 1000
    m = k * 1000
    b = m * 1000
    t = b * 1000

    # assert(0 <= num)

    if(num<=0):
        return 'zero'

    if (num < 20):
        return d[num]

    if (num < 100):
        if num % 10 == 0: return d[num]
        else: return d[num // 10 * 10] +' ' + d[num % 10]

    if (num < k):
        if num % 100 == 0: return d[num // 100] + ' hundred'
        else: return d[num // 100] + ' hundred ' + num_to_words(num % 100)

    if (num < m):
        if num % k == 0: return num_to_words(num // k) + ' thousand'
        else: return num_to_words(num // k) + ' thousand, ' + num_to_words(num % k)

    if (num < b):
        if (num % m) == 0: return num_to_words(num // m) + ' million'
        else: return num_to_words(num // m) + ' million, ' + num_to_words(num % m)

    if (num < t):
        if (num % b) == 0: return num_to_words(num // b) + ' billion'
        else: return num_to_words(num // b) + ' billion, ' + num_to_words(num % b)

    if (num % t == 0): return num_to_words(num // t) + ' trillion'
    else: return num_to_words(num // t) + ' trillion, ' + num_to_words(num % t)

    raise AssertionError('num is too large: %s' % str(num))

def getAutoResponderDetails(field_dict):
    # field_dict = json.loads(request.body)
    if 'auto_responder_id' in field_dict.keys():
        if EngageboostEmailTypeContents.objects.filter(id=field_dict['auto_responder_id']).exists():
            get_template = EngageboostEmailTypeContents.objects.get(id=field_dict['auto_responder_id'])
            data = {'mail_subject':get_template.subject, 'mail_content':get_template.email_content, 'sms_subject': get_template.sms_subject, 'sms_content': get_template.email_content}

        else:
            data = {}

    else:
        if EngageboostApplicableAutoresponders.objects.filter(**field_dict).exists():
            get_record = EngageboostApplicableAutoresponders.objects.filter(**field_dict).last()
            get_template = get_record.auto_responder
            data = {'mail_subject':get_template.subject, 'mail_content':get_template.email_content, 'sms_subject': get_template.sms_subject, 'sms_content': get_template.email_content}

        else:
            data = {}
    return data

    # return JsonResponse({'status':1, 'messaage':'success', 'data':data})



def sendEmail(website_id, html_content, subject, to_email):
    get_setting = EngageboostGlobalSettings.objects.filter(website_id=website_id).last()

    host = get_setting.smtp_server
    port = get_setting.smtp_port
    username = get_setting.smtp_username
    password = get_setting.smtp_password
    use_tls = True

    connection = get_connection(host=host,
                port=port,
                username=username,
                password=password,
                use_tls=use_tls)

    from_email = get_setting.mail_sent_from

    try:
        msg = EmailMultiAlternatives(subject, html_content , from_email, to_email, connection=connection)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    except Exception as e:
        return str(e)

    return 'success'

class CommonCurrencyList(generics.ListAPIView):
    def get(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        rs_currency = EngageboostCurrencyMasters.objects.using(company_db).filter(isblocked='n',isdeleted='n').all()
        if rs_currency:
            currency_data = CurrencyViewSerializer(rs_currency, many=True)
            data={"status":1,"data":currency_data.data}
            return Response(data)
        else:
            data={"status":0,"data":[],'msg':"No data found."}
            return Response(data)

def getBaseCurrency():
    rs_base_currency = EngageboostCurrencyRates.objects.filter(isbasecurrency='y', isdeleted='n', isblocked='n').first()
    if rs_base_currency:
        base_currency 	= BaseCurrencyratesetSerializer(rs_base_currency)
        base_currency = base_currency.data
        currency_id 	= base_currency['engageboost_currency_master']
        currency_code 	= base_currency['currency_code']
    else:
        currency_id = '25'
        currency_code =  'INR'

    data = {
        "currency_id":currency_id,
        "currency_code":currency_code
    }
    return data

def get_exchange_rate(currency_id):
    rs_currency = EngageboostCurrencyRates.objects.filter(engageboost_currency_master_id=currency_id, isdeleted='n', isblocked='n', engageboost_company_website_id=1).first()
    currency_data = {}
    if rs_currency:
        currency_data = BaseCurrencyratesetSerializer(rs_currency)
        currency_data = currency_data.data
    return currency_data

def get_currency_details(currency_id):
    rs_currency = EngageboostCurrencyMasters.objects.filter(id=currency_id).first()
    currency_data = {}
    if rs_currency:
        currency_data = CurrencyViewSerializer(rs_currency)
        currency_data = currency_data.data
    return currency_data


class get_currency_details_by_code(generics.ListAPIView):
    def post(self, request, *args, **kwargs):
        requestdata 	= request.data
        currency_code = requestdata['currency_code']
        # company_db = loginview.db_active_connection(request)
        currency_data = {}
        if currency_code:
            rs_currency = EngageboostCurrencyMasters.objects.filter(currency=currency_code).first()

            if rs_currency:
                currency_data = CurrencyViewSerializer(rs_currency)
                currency_data = currency_data.data
                data = {
                    "status":1,
                    "data":currency_data
                }
            else:
                data = {
                    "status":0,
                    "data":currency_data,
                    "message":"No data found."
                }
        else:
            data = {
                    "status":0,
                    "data":currency_data,
                    "message":"Provide currency code."
                }
        return Response(data)


def updateDefaultPriceWithSelectedCurrency(default_price, product_chanel_price=None, update_with_product_chanel_or_exchange_rate=1,discount_applied='N'):
        exchange_rate_details = get_exchange_rate(currency_id)
        exchange_rate = exchange_rate_details['exchange_rate']
        if exchange_rate:
            pass
        else:
            exchange_rate = 1

        #### IF Currency not BASE Currency ####
        if update_with_product_chanel_or_exchange_rate == 1:
            if product_chanel_price is not None: # ----If channel currency have value
                if discount_applied == 'N':
                    default_price = product_chanel_price
                else: 		#-----this is product amount after discount
                    default_price = default_price
            else: #----If channel currency have no value
                default_price = default_price*exchange_rate

            default_price = default_price
            return default_price;
        else: #### IF Currency is BASE Currency ####
            if discount_applied == 'N':
                if product_chanel_price:
                    default_price = product_chanel_price
                else:
                    default_price = default_price
            else: 		#-----this is product amount after discount
                default_price = default_price

            default_price = default_price
            return default_price

# def change_product_price_by_currency(product_id, channel_id, currency_id):
# 	if product_id and product_id>0:
# 		rs_channel_currency = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=product_id, channel_id=channel_id, currency_id=currency_id).first()
# 		if rs_channel_currency:
# 			channel_currency_data = ChannelCurrencyProductPriceSerializer(rs_channel_currency)
# 			print(json.dumps(channel_currency_data.data))

# 			data = {
# 				'status':1,
# 				'price_details':"",
# 			}
# 		else:
# 			data = {
# 				'status':0,
# 				'msg':"Channel currency not found.",
# 			}
# 	else:
# 		data = {
# 			'status':0,
# 			'msg':"Provide product id."
# 		}

def get_product_channel_price(product_id, channel_id, currency_id):
    if product_id and product_id>0:
        rs_channel_currency = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=product_id, channel_id=channel_id, currency_id=currency_id).first()
        if rs_channel_currency:
            channel_currency_data = ChannelCurrencyProductPriceSerializer(rs_channel_currency)
            data = {
                'status':1,
                'price_details':channel_currency_data.data,
            }
        else:
            data = {
                'status':0,
                'msg':"Channel currency not found.",
            }
    else:
        data = {
            'status':0,
            'msg':"Provide product id."
        }


def download_img_from_temp(file_url=None,file_name=None):
    from PIL import Image
    if file_name==None:
        rand 		= str(random.randint(1,99999))
        time_stamp  = str(int(datetime.datetime.now().timestamp()))
        name1 		=rand+time_stamp
    else:
        name1 = file_name

    # print("url=================",file_url)
    file1 = file_url

    try:
        file1 = file1.split("?")
        file1 = file1[0]
    except:
        pass

    extrev=file1[::-1]
    extrevore = extrev.split(".")
    ext=extrevore[0][::-1]

    try:
        ext = ext.lower()
    except:
        pass
    # print("Ext==================",ext)
    if ext=="jpg" or ext=="jpeg" or ext=="png" or ext=="gif" or ext=="webp":
        print("File Url=====",file1)
        img=urllib.request.urlretrieve(file1, 'media/product/temp/'+name1+'.'+ext)
        cover_image=name1+'.'+ext
        fs=FileSystemStorage()
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uploaded_file_url = fs.url(img)
        # print("Path root=========",'/media/product/temp/'+name1+'.'+ext)
        data={
            "path":'/media/product/temp/'+name1+'.'+ext,
            "image_name":cover_image
        }
    else:
        data={
            "path":'',
            "image_name":''
        }

    return data

def amazons3_global_fileupload(file_name,resolution=None,module=None,company_name=None,s3folder_name=None):
    import tinys3

    if resolution and company_name and s3folder_name and module:
        conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)
        test_link = company_name+'/'+s3folder_name+'/'+module+'/'+resolution+'x'+resolution+'/'+file_name
        try:
            f = open(settings.MEDIA_ROOT+'/'+module+'/'+resolution+'x'+resolution+'/'+file_name,'rb')
            val = conn.upload(company_name+'/'+s3folder_name+'/'+module+'/'+resolution+'x'+resolution+'/'+file_name,f,settings.AMAZON_S3_BUCKET)
            print("AWS image upload success ==========","http://lifcogrocery.s3.amazonaws.com/"+test_link)
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
            print("AWS image upload Error ==========","http://lifcogrocery.s3.amazonaws.com/"+test_link)
    return 0

def amazons3_global_fileupload_new(file_name,resolution=None,module=None,company_name=None,s3folder_name=None):
    import tinys3

    if resolution and company_name and s3folder_name and module:
        conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)
        test_link = company_name+'/'+s3folder_name+'/'+module+'/'+resolution+'x'+resolution+'/'+file_name
        try:
            f = open(settings.MEDIA_ROOT+'/'+module+'/'+resolution+'x'+resolution+'/'+file_name,'rb')
            val = conn.upload(company_name+'/'+s3folder_name+'/'+module+'/'+resolution+'x'+resolution+'/'+file_name,f,settings.AMAZON_S3_BUCKET)
            data = {"status":1,"url":test_link}
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
            print("AWS image upload Error ==========","http://lifcogrocery.s3.amazonaws.com/"+test_link)
    print(data)
    return data

def delete_create_image_from_local_folder(resolutions=None,module=None):

    if resolutions and module:
        if os.path.exists(settings.BASE_DIR+'/media/'+module+'/'):
            shutil.rmtree(settings.BASE_DIR+'/media/'+module+'/')
        for resolution in resolutions:
            resolution = str(resolution)
            directory_prduct=settings.BASE_DIR+'/media/'+module+'/'+resolution+'x'+resolution+'/'
            if not os.path.exists(directory_prduct):
                os.makedirs(directory_prduct)

        directory_prduct7=settings.BASE_DIR+'/media/'+module+'/temp/'
        if not os.path.exists(directory_prduct7):
            os.makedirs(directory_prduct7)

def get_db_fields(model_name, primary_cat_id=0, import_type='Import'):
    website_id = 1
    module_list_id = ''
    new_db_fields = []
    new_db_field_filter = []
    new_custom_field = {}
    new_db_field = {}
    if model_name == 'Product' or model_name == 'product':
        module_id = 1
        module_details = EngageboostModuleLayouts.objects.filter(website_id=website_id,module_id=module_id).first()
        if module_details:
            module_list_id = module_details.id

        basic_field_map = {"Product Name":"name","SKU":"sku","PO Tax Class":"po_taxclass_id","Gross Weight":"weight","Sales Tax Class":"taxclass_id","ASIN":"asin","EAN/UPC":"ean","ISBN":"isbn","SUPC":"supc","Expected Delivery Days(sla)":"sla","Cost Per Unit":"cost_per_unit","Features":"features","Large Description":"description","Shipping Class":"shippingclass_id","Small Description":"mp_system_requirements","Status":"status","Parent SKU":"parent_product_id","Supplier":"supplier_id","Brand":"brand","Features":"features","META Page URL":"meta_url","META Page Title":"meta_title","META Keyword":"meta_key_word","META Description":"meta_description","Price":"defaultprice","Supc":"supc","Expected Delivery Days":"sla","AmazonIN Price":"AmazonIN_price","AmazonUK Price":"AmazonUK_price","AmazonUs Price":"AmazonUs_price","Ebayau Price":"ebayau_price","Ebayin Price":"ebayin_price","Ebayuk Price":"ebayuk_price","Ebayusa Price":"ebayusa_price","FlipKart Price":"FlipKart_price","Paytm Price":"Paytm_price","SnapDeal Price":"SnapDeal_price","Customer Group":"customer_group_id","Unit Of Measurement":"uom","AmazonIN SKU":"AmazonIN_sku","AmazonUK SKU":"AmazonUK_sku","AmazonUs SKU":"AmazonUs_sku","Ebayau SKU":"ebayau_sku","Ebayin SKU":"ebayin_sku","Ebayuk SKU":"ebayuk_sku","Ebayusa SKU":"ebayusa_sku","FlipKart SKU":"FlipKart_sku","Paytm SKU":"Paytm_sku","SnapDeal SKU":"SnapDeal_sku","NPN":"npn","Max Order Unit":"max_order_unit","HSN Code":"hsn_id","Visible In Listing":"visible_in_listing","Related Product SKU":"related_product_skus","Barcode":"barcodes"}

        for key,val in iter(basic_field_map.items()):
            extra_values =  {"field_label":key,"model_field_value":val}
            new_db_fields.append(extra_values)

        if primary_cat_id != 0:
            category_custom_field_cond = EngageboostDefaultModuleLayoutFields.objects.all().filter(category_id=primary_cat_id).filter(~Q(field_label="Status")).values('field_label','model_field_value','field_id','id','module_layout_section_id')
            if category_custom_field_cond:
                new_custom_db_fields = DefaultModuleLayoutFieldsSerializer(category_custom_field_cond,many=True)
                for category_custom_field in new_custom_db_fields.data:
                    if category_custom_field["field_label"]:
                        d11 ={"field_label":category_custom_field["field_label"]}; new_custom_field=dict(new_custom_field,**d11)
                    else:
                        d11 ={"field_label":""}; new_custom_field=dict(new_custom_field,**d11)

                    if category_custom_field["model_field_value"]:
                        d11 ={"model_field_value":category_custom_field["model_field_value"]}; new_custom_field=dict(new_custom_field,**d11)
                    elif category_custom_field["field_label"]:
                        d11 ={"model_field_value":category_custom_field["field_label"]}; new_custom_field=dict(new_custom_field,**d11)
                    else:
                        d11 ={"model_field_value":""}; new_custom_field=dict(new_custom_field,**d11)

                    try:
                        if category_custom_field["id"]: ids = category_custom_field["id"]
                        else: ids = None
                    except KeyError: ids = None
                    d11 ={"id":ids}; new_custom_field=dict(new_custom_field,**d11)

                    new_db_fields.append(new_custom_field)

        for db_fields in new_db_fields:
            if db_fields["field_label"]:
                d1 ={"field_label":db_fields['field_label']}; new_db_field=dict(new_db_field,**d1)
            else:
                d1 ={"field_label":""}; new_db_field=dict(new_db_field,**d1)

            if db_fields["model_field_value"]:
                d1 ={"model_field_value":db_fields['model_field_value']}; new_db_field=dict(new_db_field,**d1)
            else:
                d1 ={"model_field_value":""}; new_db_field=dict(new_db_field,**d1)

            try:
                if db_fields['id']: ids = db_fields['id']
                else: ids = None
            except KeyError: ids = None

            d1 ={"id":ids}; new_db_field=dict(new_db_field,**d1)

            new_db_field_filter.append(new_db_field)

        return new_db_field_filter

    if model_name == 'RelatedProduct' or model_name == 'related_product':
        module_id = 1
        module_details = EngageboostModuleLayouts.objects.filter(website_id=website_id,module_id=module_id).first()
        if module_details:
            module_list_id = module_details.id

        basic_field_map = {
                            "SKU":"sku",
                            "Related Products":"related_product_skus",
                            "Up-sells":"upsell_product_skus",
                            "Cross-sells":"cross_product_skus",
                            "Associated Products":"associated_product_skus",
                            "Substitute Products":"substitude_product_skus"
                            }

        for key,val in iter(basic_field_map.items()):
            extra_values =  {"field_label":key,"model_field_value":val}
            new_db_fields.append(extra_values)

        for db_fields in new_db_fields:
            if db_fields["field_label"]:
                d1 ={"field_label":db_fields['field_label']}; new_db_field=dict(new_db_field,**d1)
            else:
                d1 ={"field_label":""}; new_db_field=dict(new_db_field,**d1)

            if db_fields["model_field_value"]:
                d1 ={"model_field_value":db_fields['model_field_value']}; new_db_field=dict(new_db_field,**d1)
            else:
                d1 ={"model_field_value":""}; new_db_field=dict(new_db_field,**d1)

            try:
                if db_fields['id']: ids = db_fields['id']
                else: ids = None
            except KeyError: ids = None

            d1 ={"id":ids}; new_db_field=dict(new_db_field,**d1)
            new_db_field_filter.append(new_db_field)
        return new_db_field_filter


def getWebsiteDetails(websiteId=None):
    if websiteId is not None:
        company_cond = EngageboostCompanyWebsites.objects.filter(id = websiteId).first()
        companywebsitedetails = CompanyWebsiteSerializer(company_cond)
        return companywebsitedetails
    else :
        return {}

def amazons3GlobalUpload(file_name, dimenstion,moduleName,websiteId):
    rs_company = EngageboostCompanyWebsites.objects.filter(id=websiteId).first()
    company_name = "Lifco"
    s3folder_name = "lifco"
    if rs_company:
        company_name = rs_company.company_name
        s3folder_name = rs_company.s3folder_name
    # print(settings.MEDIA_ROOT+'/'+moduleName + '/'+dimenstion+'/'+file_name)
    conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)
    f400 = open(settings.MEDIA_ROOT+'/'+moduleName +'/'+dimenstion+'/'+file_name, 'rb')
    val = conn.upload(company_name+'/'+s3folder_name+'/product/'+dimenstion+'/'+file_name,f400,settings.AMAZON_S3_BUCKET)

    return 0

def get_all_languages():
    rs_all_lang = EngageboostLanguages.objects.filter(isblocked='n', isdeleted='n').exclude(lang_code='en').all()
    all_language_data = LanguageSerializer(rs_all_lang, many=True)
    all_language_data = all_language_data.data
    return all_language_data

class AllLanguages(generics.ListAPIView):
    def get(self, request, format=None):
        all_language = get_all_languages()
        if len(all_language)>0:
            data = {
                "status":1,
                "all_languages":all_language
            }
        else:
            data = {
                "status":0,
                "all_languages":[]
            }
        return Response(data)


def get_advanced_search_filter(table_name,filter_arr,filter_obj=None):
    # Condition Rules:
    # 1: Equals to
    # 2: Not Equals to
    # 3: Starts with
    # 4: Ends with
    # 5: Contains
    # 6: Does not contains
    # 7: Greater than equals to
    # 8: Less than equals to
    try:
        if filter_obj != None:
            model = apps.get_model('webservices',table_name)
            filter_obj = filter_obj.filter(isdeleted="n")
    except:
            model = apps.get_model('webservices',table_name)
            filter_obj = model.objects.filter(isdeleted="n")
    for item in filter_arr:
        # print(item)
        try:
            field = item["field"]
            try:
                input_type = item["input_type"]
            except:
                input_type = ""
            key = item["key"]
            try:
                key = key.strip()
            except:
                pass
            comparer = item["comparer"]
            if table_name=="EngageboostWarehouseMasters" and field=="channel_id":
                warehouseApplicable = EngageboostWarehouseMasterApplicableChannels.objects.filter(applicable_channel_id=key)
                if warehouseApplicable.count()>0:
                    warehouse_app = warehouseApplicable.all().values()
                    arr = []
                    for item in warehouse_app:
                        arr.append(item["warehouse_master_id"])
                    filter_obj = filter_obj.filter(id__in=arr)

            elif table_name=="EngageboostShipments" and field=="time_slot_id":
                orders = EngageboostOrdermaster.objects.filter(time_slot_id__in=key).values("trent_picklist_id")
                filter_obj = filter_obj.filter(id__in=orders)

            elif table_name=="EngageboostShipments" and field=="custom_order_id":
                orders = EngageboostShipmentOrders.objects.filter(order_id__custom_order_id__iexact=key).values("shipment")
                filter_obj = filter_obj.filter(id__in=orders)

            elif table_name=="EngageboostProductStocks" and field=="product__id":
                orders = EngageboostOrderProducts.objects.filter(product_id=key).values("order_id")
                filter_obj = filter_obj.filter(id__in=orders).order_by('-id')

            elif table_name == "EngageboostTrentPicklists" and field=="product__id":
                orders = EngageboostOrderProducts.objects.filter(product_id=pk).values("order_id")
                custom_order_id=[]
                shipmentOrders = EngageboostOrdermaster.objects.using(company_db).filter(id__in=orders)
                if shipmentOrders.count()>0:
                    shipmentOrders = shipmentOrders.values("trent_picklist_id")
                    filter_obj = filter_obj.filter(id__in=shipmentOrders)
            elif table_name=="EngageboostShipments" and field=="created_day":
                filter_obj = filter_obj.filter(created__week_day__in=key)

            elif table_name == "EngageboostTrentPicklists" and field=="custom_order_id":
                shipmentOrders = EngageboostOrdermaster.objects
                if comparer==1:
                    kwargs = {field+"__iexact":key}
                    shipmentOrders = shipmentOrders.filter(**kwargs)
                if comparer==2:
                    kwargs = {field+"__iexact":key}
                    shipmentOrders = shipmentOrders.exclude(**kwargs)
                if comparer==3:
                    kwargs = {field+"__istartswith":key}
                    shipmentOrders = shipmentOrders.filter(**kwargs)
                if comparer==4:
                    kwargs = {field+"__iendswith":key}
                    shipmentOrders = shipmentOrders.filter(**kwargs)
                if comparer==5:
                    kwargs = {field+"__icontains":key}
                    shipmentOrders = shipmentOrders.filter(**kwargs)
                if comparer==6:
                    kwargs = {field+"__icontains":key}
                    shipmentOrders = shipmentOrders.exclude(**kwargs)
                if comparer==7:
                    kwargs = {field+"__gte":key}
                    shipmentOrders = shipmentOrders.filter(**kwargs)
                if comparer==8:
                    kwargs = {field+"__lte":key}
                    shipmentOrders = shipmentOrders.filter(**kwargs)
                orders = shipmentOrders.all().values("trent_picklist_id")
                filter_obj = filter_obj.filter(id__in=orders)
            else:
                if comparer==1:
                    if input_type=="date":
                        if table_name == "EngageboostProductStocks":
                            kwargs = {field+"__istartswith":key}
                        else:
                            kwargs = {field+"__date":key}
                    elif input_type=="multi_select":
                        kwargs = {field+"__in":key}
                    else:
                        # if isinstance(key, list):
                        # 	kwargs = {field+"__in":key}
                        # elif isinstance(key, str):
                        # 	key = key.strip()
                        # else:
                        # 	key = key
                        key = str(key)
                        key = key.strip()
                        kwargs = {field+"__iexact":key}

                    filter_obj = filter_obj.filter(**kwargs)
                if comparer==2:
                    if input_type=="date":
                        if table_name == "EngageboostProductStocks":
                            kwargs = {field+"__istartswith":key}
                        else:
                            kwargs = {field+"__date":key}
                    elif input_type=="multi_select":
                        kwargs = {field+"__in":key}
                    else:
                        kwargs = {field+"__iexact":key}
                    filter_obj = filter_obj.exclude(**kwargs)
                if comparer==3:
                    key = key.strip()
                    kwargs = {field+"__istartswith":key}
                    filter_obj = filter_obj.filter(**kwargs)
                if comparer==4:
                    key = key.strip()
                    kwargs = {field+"__iendswith":key}
                    filter_obj = filter_obj.filter(**kwargs)
                if comparer==5:
                    key = key.strip()
                    kwargs = {field+"__icontains":key}
                    filter_obj = filter_obj.filter(**kwargs)
                if comparer==6:
                    key = key.strip()
                    kwargs = {field+"__icontains":key}
                    filter_obj = filter_obj.exclude(**kwargs)
                if comparer==7:
                    kwargs = {field+"__gte":key}
                    filter_obj = filter_obj.filter(**kwargs)
                if comparer==8:
                    kwargs = {field+"__lte":key}
                    filter_obj = filter_obj.filter(**kwargs)
        except Exception as error:
            try:
                if input_type=="date":
                    if table_name == "EngageboostProductStocks":
                        kwargs = {field+"__istartswith":key}
                    else:
                        kwargs = {field+"__date":key}
                elif input_type=="multi_select":
                    kwargs = {field+"__in":key}
                else:
                    kwargs = {field+"__iexact":key}
                filter_obj = filter_obj.filter(**kwargs)
            except:
                filter_obj = filter_obj

            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
            print("Error ==========",data)
    return filter_obj


def fetch_grid_layout(request,module,screen_name):
    company_db = loginview.db_active_connection(request)

    layout_fetch = EngageboostGridLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)

    layout_header=layout_fetch.header_name.split("@@")
    layout_field=layout_fetch.field_name.split("@@")

    existing = {}
    for j in range(0,len(layout_header)):
        ex_field = layout_field[j]
        field_name = ex_field
        existing[field_name] = layout_header[j]

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
        layout={"title":header,"field":field_name,"child":child_name,"show":status, "field_type":field_type}
        layout_arr.append(layout)

    ##################Applied Layout#####################
    if(layout_check):
        layout_column_check=EngageboostGridColumnLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
        layout_header2=layout_column_check.header_name.split("@@")
        layout_field2=layout_column_check.field_name.split("@@")
        # print(existing)
        # print(layout_header2)
        applied = {}
        child = {}
        f_type = {}
        for k in range(0,len(layout_header2)):
            ap_field = layout_field2[k]
            field_name = ap_field
            # print("=================",ap_field)

            ex_layout_field=field_name.split(".")
            is_numeric_field=field_name.split("#")
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

            applied[field_name] = layout_header2[k]
            f_type[field_name] = field_type
            child[field_name] = child_name
        try:
            all(map( existing.pop, applied))
        except:
            existing = applied
        applied = dict(applied,**existing)


    layout2={}
    layout2_arr=[]
    #print(applied)
    for field2 in applied:

        header2 = applied[field2]
        field_name2 = field2

        # ex_layout_field=field2.split(".")
        # is_numeric_field=field2.split("#")
        # field_name2=ex_layout_field[0]

        # if len(is_numeric_field)>1:
        # 	field_type2=is_numeric_field[1]
        # 	field_name2=is_numeric_field[0]
        # else:
        # 	field_type2=''

        # if len(ex_layout_field)>1:
        # 	child_name2=ex_layout_field[1]
        # 	field_name2=ex_layout_field[0]
        # else:
        # 	child_name2=''
        try:
            field_type2 = f_type[field_name2]
        except:
            field_type2=''
        try:
            child_name2 = child[field_name2]
        except:
            child_name2=''

        if header2 in layout_header2:
            status=1
        else:
            status=0
        layout2={"title":header2,"field":field_name2,"child":child_name2,"show":status, "field_type":field_type2}
        layout2_arr.append(layout2)
        ##################Applied Layout#####################
    data = {"layout":layout_arr,"applied_layout":layout2_arr}
    return data


def get_product_cost(product_id,warehouse_id):
    # print("=======================",product_id,warehouse_id)
    from django.db.models import F,Count,Sum,Avg,FloatField,Case,When,IntegerField
    poObj = EngageboostPurchaseOrders.objects.filter(warehouse_id=warehouse_id)
    avg_cost = 0
    total_price = 0
    total_quantity = 0
    if poObj.count()>0:
        poObj = poObj.values("id").all()

        poProObj = EngageboostPurchaseOrderProducts.objects.values().filter(product_id=product_id,purchase_order_id__in=poObj)
        # poProObj = poProObj.annotate(total_price=Sum(F('price'),output_field = FloatField()),
        # 							total_quantity=Sum(F('quantity'),output_field = IntegerField()))

        if poProObj.count()>0:
            poProObj = poProObj.last()

            # total_price = poProObj[0]['total_price']
            # total_quantity = poProObj[0]['total_quantity']

            # if total_quantity>0:
            # 	avg_cost = float(total_price/total_quantity)
            # 	avg_cost = round(avg_cost,2)
            avg_cost = round(poProObj['price'],2)

    return avg_cost
#========================Amazon s3 file upload==============#
def amazons3_fileupload(file_name,image_name):
    conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)
    f400 = open(settings.MEDIA_ROOT+'/'+file_name,'rb')
    conn.delete(settings.AMAZON_S3_FOLDER+'/product/200x200/'+file_name,settings.AMAZON_S3_BUCKET)
    conn.upload(settings.AMAZON_S3_FOLDER+'/cmsimages/'+image_name,f400,settings.AMAZON_S3_BUCKET)
    return 0

def amazons3_template800(file_name):
    conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)
    f400 = open(settings.MEDIA_ROOT+'/template/800x800/'+file_name,'rb')
    conn.upload(settings.AMAZON_S3_FOLDER+'/cmsimages/template/800x800/'+file_name,f400,settings.AMAZON_S3_BUCKET)
    os.remove(settings.MEDIA_ROOT+'/template/800x800/'+file_name)
    return 0

def amazons3_fileupload_temp(file_name,image_name):
    conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)
    conn.copy(settings.AMAZON_S3_FOLDER+'/temp_image/'+file_name,settings.AMAZON_S3_BUCKET,settings.AMAZON_S3_FOLDER+'/cmsimages/'+image_name)
    return 0

def amazons3_fileupload_template_template800(file_name,image_name,delete_image):
    conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)
    conn.copy(settings.AMAZON_S3_FOLDER+'/cmsimages/template/'+file_name,settings.AMAZON_S3_BUCKET, settings.AMAZON_S3_FOLDER+'/cmsimages/template/800x800/'+image_name)
    amazons3_template800_delete(delete_image)
    return 0

def amazons3_template800_delete(file_name):
    if file_name:
        conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)
    conn.delete(settings.AMAZON_S3_FOLDER+'/cmsimages/template/800x800/'+file_name,settings.AMAZON_S3_BUCKET)

# def get_geo_location(address,city,post_code,state,country):
def get_geo_location(address,state,country):
    import requests
    try:
        address = str(address)+","+str(city)+","+str(post_code)

        stateObj = EngageboostStates.objects.get(id=state)
        if stateObj:
            address = address+","+str(stateObj.state_name)

        countryObj = EngageboostCountries.objects.get(id=country)
        if countryObj:
            address = address+","+str(countryObj.country_name)

        api_key = 'AIzaSyD6X_gUYX5VI8wD7P7uiBeQu47XVgbfR1Q'
        #print("Address======",address)
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&sensor=false&key='+api_key)

        resp_json_payload = response.json()
        # print("Location======",resp_json_payload)

        geometry = resp_json_payload[0]['location']
        location = {"lat":round(float(geometry["lat"]),4),"lng":round(float(geometry["lng"]),4)}
        # print("Location======",location)
    except:
        latitude="22.5427604"
        longitude="88.3859595"

        location = {"lat":round(float(latitude),4),"lng":round(float(longitude),4)}
    return location

def update_stock_all(product_id=None,warehouse_id=None,quantity=None,status=None,stock_minus_type=None,order_id=None,website_id=None,updatedby=0):
    try:
        stockObj = EngageboostProductStocks.objects.filter(product_id=product_id,warehouse_id=warehouse_id)
        stock_result = stockObj.first()
        # Real stock increase
        stockData = StockViewSerializer(stock_result,partial=True)
        stock_data = stockData.data

        stoack_data_update = {}
        now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
        stoack_data_update['modified'] = now_utc
        stoack_data_update['updatedby'] = updatedby
        if stock_data:
            if((status == "Increase" or status == "Refund") and stock_minus_type=="real"):
                if stock_data:
                    stoack_data_update['stock'] = int(stock_data['stock']) + int(quantity)
                    stoack_data_update['real_stock'] = (int(stock_data['stock']) + int(quantity))-int(stock_data['safety_stock'])-int(stock_data['virtual_stock'])
                    EngageboostProductStocks.objects.filter(id = stock_data['id']).update(**stoack_data_update)

            # END
            # Virtual stock decrease
            if status == "Decrease" and stock_minus_type=="virtual":
                if stock_data:
                    stoack_data_update['virtual_stock'] = int(stock_data['virtual_stock']) + int(quantity)
                    stoack_data_update['real_stock'] = int(stock_data['stock'])-(int(stock_data['virtual_stock']) + int(quantity))-int(stock_data['safety_stock'])
                    EngageboostProductStocks.objects.filter(id = stock_data['id']).update(**stoack_data_update)
            # END
            # Real stock decrease
            if status == "Decrease" and stock_minus_type=="real":
                if stock_data:
                    stoack_data_update['stock'] = int(stock_data['stock']) - int(quantity)
                    stoack_data_update['real_stock'] = (int(stock_data['stock']) - int(quantity))-int(stock_data['safety_stock'])-int(stock_data['virtual_stock'])
                    EngageboostProductStocks.objects.filter(id = stock_data['id']).update(**stoack_data_update)

            product_stock = get_product_stock(product_id)
            elastic = change_field_value_elastic(product_id,'EngageboostProducts',{'inventory':product_stock})

        # END
        # Insert into
        data_cron_stock_save = {}
        if stock_data:
            condition_cron_stock = EngageboostProductStockCrons.objects.filter(warehouse_id=warehouse_id,product_id=product_id)
            condition_cron_stock_data = condition_cron_stock.first()

            if condition_cron_stock_data:
                condition_cron_stockData = ProductStockCronsSerializer(condition_cron_stock_data,partial=True)
                data_cron_stock = condition_cron_stockData.data
                # print("==============================",data_cron_stock)

                data_cron_stock_save['stock'] = int(stoack_data_update['real_stock'])
                data_cron_stock_save['created'] = datetime.datetime.now()
                EngageboostProductStockCrons.objects.filter(id = data_cron_stock['id']).update(**data_cron_stock_save)
            else:
                data_cron_stock_save['product_id'] = product_id
                data_cron_stock_save['warehouse_id'] = warehouse_id
                data_cron_stock_save['stock'] = int(stoack_data_update['real_stock'])
                data_cron_stock_save['created'] = datetime.datetime.now()
                EngageboostProductStockCrons.objects.create(**data_cron_stock_save)

             # this->inset_purchase_order_received(warehouse_id,product_id,status,quantity,order_id,rac_no,lot_No,website_id)
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        print("Stock Update Error ==========",data)
    return 0

def update_db_sequences(data):
    cursor = connection.cursor()
    if data=="productimages":
        cursor.execute('''SELECT setval('engageboost_productimages_id_seq', (SELECT MAX(id) FROM engageboost_productimages))''')
    elif data=="product_categories":
        cursor.execute('''SELECT setval('engageboost_product_categories_id_seq', (SELECT MAX(id) FROM engageboost_product_categories))''')
    elif data=="category_banners_images":
        cursor.execute('''SELECT setval('engageboost_category_banners_images_id_seq', (SELECT MAX(id) FROM engageboost_category_banners_images))''')
    elif data=="temp_product_price":
        cursor.execute('''SELECT setval('engageboost_temp_product_price_id_seq', (SELECT MAX(id) FROM engageboost_temp_product_price))''')
    elif data=="imported_temp_product_stocks":
        cursor.execute('''SELECT setval('engageboost_imported_temp_product_stocks_id_seq', (SELECT MAX(id) FROM engageboost_imported_temp_product_stocks))''')
    elif data=="channel_currency_product_price":
        cursor.execute('''SELECT setval('engageboost_channel_currency_product_price_id_seq', (SELECT MAX(id) FROM engageboost_channel_currency_product_price))''')
    else:
        try:
            cursor.execute("SELECT setval('engageboost_"+data+"_id_seq', (SELECT MAX(id) FROM engageboost_"+data+"))")
        except:
            pass
    return 1

def get_date_from_datetime(gettime, zone, date,db_format=None):
    getdate = str(gettime)
    date_format = date.date_format
    try:
        if db_format==None:
            try:
                db_format = "%Y-%m-%dT%H:%M:%S.%fZ"
                getdate = datetime.datetime.strptime(getdate, db_format)
            except:
                db_format = "%Y-%m-%d %H:%M:%S.%f"
                getdate = datetime.datetime.strptime(getdate, db_format)
        else:   #  Kalyan
            try:
                db_format = "%Y-%m-%dT%H:%M:%S.%fZ"
                getdate = datetime.datetime.strptime(getdate, db_format)
            except:
                db_format = "%Y-%m-%d"
                getdate = datetime.datetime.strptime(getdate, db_format)
    except:
        try:
            db_format = "%Y-%m-%dT%H:%M:%S.%fZ"
            getdate = datetime.datetime.strptime(getdate, db_format)
        except:
            db_format = "%Y-%m-%d %H:%M:%S.%f"
            getdate = datetime.datetime.strptime(getdate, db_format)
    # print("===========",db_format)

    datetime_object = getdate.strftime(date_format)

    return datetime_object

def get_time(gettime, zone, date):
    datetime = gettime.replace('T',' ')
    data_time=datetime.replace('Z',' ')
    a=data_time.split(".")
    b=a[0].replace(':',' ')
    c=b.replace('-',' ')
    date_format=c.split(" ")
    import datetime
    import time
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

#####################Elastic Functions###########################

def save_data_to_elastic(pk, table_name, fields=[]):
    e_id = pk
    elastic_URL = settings.ELASTIC_URL
    model = apps.get_model('webservices',table_name)
    count = model.objects.filter(id = e_id).count()
    try:
        if count>0:
            elastic_data = model.objects.get(id=e_id)
            serializer_class = get_serializer_class_elastic(table_name)
            serializer = serializer_class(elastic_data,partial=True)
            serializer_data = serializer.data

            #################Set Up Language Data#####################
            # data = setUpLangDataToSerializer(serializer_data)
            ###########################End############################

            #################Set Up Related Data#####################
            data = format_serialized_data(table_name,serializer_data)
            ###########################End############################
            index_name = get_index_name_elastic(pk,table_name)
            check_mapping_elastic(table_name,index_name)
            exists = es.exists(index=index_name, id=pk, doc_type="data")
            if exists:
                resp = es.index(index=index_name, id=pk, doc_type="data", body=data, refresh=True)
                # resp = requests.put(elastic_URL+index_name+"/data/"+str(pk), data=json.dumps(data),
                # 	headers={
                # 			"Content-Type":"application/json",
                # 			"Accept": "application/json"
                # 	})
            else:
                resp = es.create(index=index_name, id=pk, doc_type="data", body=data, refresh=True)
                # resp = requests.post(elastic_URL+index_name+"/data/"+str(pk), data=json.dumps(data),
                # 	headers={
                # 			"Content-Type":"application/json",
                # 			"Accept": "application/json"
                # 	})
                exists = es.exists(index=index_name, id=pk, doc_type="data")
            print("Resp=====",resp)
            if exists:
                return 1
            else:
                return 0
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        print("Elastic Error ==========",data)
    return 0

def save_data_to_elastic_single_data_generate_for_bulk(pk,table_name,fields=[]):
    e_id = pk
    # elastic_URL = settings.ELASTIC_URL
    model = apps.get_model('webservices', table_name)
    count = model.objects.filter(id=e_id).count()
    # try:
    if count > 0:
        elastic_data = model.objects.get(id=e_id)

        serializer_class = get_serializer_class_elastic(table_name)
        serializer = serializer_class(elastic_data, partial=True)
        serializer_data = serializer.data

        #################Set Up Language Data#####################
        # data = setUpLangDataToSerializer(serializer_data)
        ###########################End############################

        #################Set Up Related Data#####################
        data = format_serialized_data(table_name, serializer_data)
        ###########################End############################
        # index_name = get_index_name_elastic(pk, table_name)
        # print("index_name======>", index_name)
        # print("data======>", data)

        # check_mapping_elastic(table_name, index_name)
        # exists = es.exists(index=index_name, id=pk, doc_type="data")
        # if exists:
        #     resp = es.index(index=index_name, id=pk, doc_type="data", body=data, refresh=True)
        #     # resp = requests.put(elastic_URL+index_name+"/data/"+str(pk), data=json.dumps(data),
        #     # 	headers={
        #     # 			"Content-Type":"application/json",
        #     # 			"Accept": "application/json"
        #     # 	})
        # else:
        #     resp = es.create(index=index_name, id=pk, doc_type="data", body=data, refresh=True)
        #     # resp = requests.post(elastic_URL+index_name+"/data/"+str(pk), data=json.dumps(data),
        #     # 	headers={
        #     # 			"Content-Type":"application/json",
        #     # 			"Accept": "application/json"
        #     # 	})
        #     exists = es.exists(index=index_name, id=pk, doc_type="data")
        # print("Resp=====", resp)
        # if exists:
        #     return 1
        # else:
        #     return 0
        return data
    # except Exception as error:
    #     trace_back = sys.exc_info()[2]
    #     line = trace_back.tb_lineno
    #     data = {"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),
    #             "message": str(error)}
    #     print("Elastic Error ==========", data)
    # return 0

def change_field_value_elastic(pk,table_name,field_value):
    try:
        index_name = get_index_name_elastic(pk,table_name)
        exists = es.exists(index=index_name, id=pk, doc_type="data")
        elastic_URL = settings.ELASTIC_URL
        if exists:
            # print(pk)
            #print(field_value)
            print(elastic_URL+index_name+"/data/_update/"+str(pk))
            # print(json.dumps({"doc": field_value}))
            # status = es.update(index=index_name,doc_type='data',id=pk,body={"doc": field_value})
            status = requests.post(elastic_URL+index_name+"/data/"+str(pk)+"/_update/", data=json.dumps({"doc": field_value}),
                    headers={
                            "Content-Type":"application/json",
                            "Accept": "application/json"
                    })
            print(status,field_value)
        else:
            status = save_data_to_elastic(pk,table_name)
        #print(status)
        return status
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        print("Field value Error ==========",data)
        return 0

@postpone
def change_product_price_elastic(product_id):
    price_data = get_channel_currency_product_price(product_id)
    change_field_value_elastic(product_id,'EngageboostProducts',{"channel_currency_product_price":price_data})
    return 1

@postpone
def change_product_stock_elastic(product_id):
    product_stock = get_product_stock(product_id)
    change_field_value_elastic(product_id,'EngageboostProducts',{'inventory':product_stock})
    return 1

def get_index_name_elastic(pk,table_name,website_id=None):
    model = apps.get_model('webservices',table_name)

    index = ""
    if table_name=='EngageboostProducts':
        index="product"
    elif table_name=='EngageboostCategoryMasters':
        index="category"
    elif table_name=='EngageboostCustomers':
        index="customer"
    elif table_name=='EngageboostOrdermaster':
        index="order"

    store_name = settings.STORE_NAME

    if website_id==None:
        website_id = 1
        print("Pk=====================",pk)
        e_id = pk
        elastic_data = model.objects.get(id=e_id)
        if elastic_data.website_id!=None and elastic_data.website_id!="":
            website_id = elastic_data.website_id

    index = index+"_"+str(website_id)
    if store_name!="":
        index = store_name+"_"+index

    return index


def add_index_settings(index=None):
    try:
        elastic_URL = settings.ELASTIC_URL

        cluster_status = add_cluster_settings()

        if index==None or index=="":
            index = '_all'

        status = 0
        setting = 	{
                        "index.blocks.read_only_allow_delete": None
                    }
        status = requests.put(elastic_URL+index+"/_settings/", data=json.dumps(setting),
                headers= {
                        "Content-Type":"application/json",
                        "Accept": "application/json"
                })
        return status
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        print("Index Settings Error ==========",data)
        return 0

def add_cluster_settings():
    try:
        elastic_URL = settings.ELASTIC_URL

        status = 0

        setting = 	{
                      "transient": {
                        "cluster.routing.allocation.disk.watermark.low": "100gb",
                        "cluster.routing.allocation.disk.watermark.high": "50gb",
                        "cluster.routing.allocation.disk.watermark.flood_stage": "10gb",
                        "cluster.info.update.interval": "1m",
                        "cluster.routing.allocation.disk.threshold_enabled": False
                      }
                    }
        status = requests.put(elastic_URL+"_cluster/_settings/", data=json.dumps(setting),
                headers= {
                        "Content-Type":"application/json",
                        "Accept": "application/json"
                })
        return status
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        print("Cluster Settings Error ==========",data)
        return 0


def check_mapping_elastic(table_name,index=None):
    try:
        add_index_settings()
        if index!=None:
            exists = es.indices.exists(index=index)

            if not exists:
                es.indices.create(index=index, ignore=400)

                module = table_name.replace("Engageboost", "")
                layout_fetch = EngageboostGridLayouts.objects.get(module=module,screen_name="list")
                layout_field=layout_fetch.field_name.split("@@")
                arr = {}

                for field in layout_field:
                    excluded_fields = ['id','created','modified','variations']
                    if field not in excluded_fields:
                        typ = {
                                "type": "keyword",
                                # "analyzer": "my_analyzer",
                                "fields": {
                                  "keyword": {
                                    "type": "keyword"
                                  }
                                }
                            }
                        arr[field]=typ
                if table_name=='EngageboostOrdermaster':
                    arr["order_products"]={
                                            "type": "nested"
                                        }
                if table_name=='EngageboostProducts':
                    arr["inventory"]={
                                        "type": "nested"
                                    }
                    arr["channel_currency_product_price"]={
                                        "type": "nested"
                                    }
                    arr["product_images"]={
                                        "type": "nested"
                                    }


                data = {
                            "properties": arr
                        }

                resp = es.indices.put_mapping(index=index,doc_type="data", ignore=400,body=data)
                print("Add Mapping to Elastic====",resp,data)
        else:
            indexes = get_all_indexes(table_name)

            for index in indexes:
                exists = es.indices.exists(index=index)

                if not exists:
                    es.indices.create(index=index, ignore=400)

                es.indices.close(index=index)
                module = table_name.replace("Engageboost", "")
                layout_fetch = EngageboostGridLayouts.objects.get(module=module,screen_name="list")
                layout_field=layout_fetch.field_name.split("@@")
                arr = {}

                for field in layout_field:
                    excluded_fields = ['id','created','modified']
                    if field not in excluded_fields:
                        typ = {
                                "type": "keyword",
                                    "fields": {
                                      "keyword": {
                                        "type": "keyword"
                                      }
                                    }
                                }
                        arr[field]=typ

                if table_name=='EngageboostOrdermaster':
                    arr["order_products"]={
                                            "type": "nested"
                                        }
                if table_name=='EngageboostProducts':
                    arr["inventory"]={
                                        "type": "nested"
                                    }
                    arr["channel_currency_product_price"]={
                                        "type": "nested"
                                    }
                    arr["product_images"]={
                                        "type": "nested"
                                    }

                data = {
                            "properties": arr
                        }
                print(data)
                resp = es.indices.put_mapping(index=index,doc_type="data", ignore=400,body=data)
                es.indices.open(index=index)
                print("Add Mapping to Elastic====",resp)
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        print("Mapping Error ==========",data)
    return 1

def get_all_indexes(table_name):
    model = apps.get_model('webservices',table_name)
    obj = model.objects.values('website_id').distinct('website_id')

    index = ""
    if table_name=='EngageboostProducts':
        index="product"
    elif table_name=='EngageboostCategoryMasters':
        index="category"
    elif table_name=='EngageboostCustomers':
        index="customer"
    elif table_name=='EngageboostOrdermaster':
        index="order"

    store_name = settings.STORE_NAME
    indexes = []
    if obj.count()>0:
        data = obj.all()
        for item in data:
            indexes.append(index+"_"+str(item["website_id"]))
            if store_name!="":
                index = store_name+"_"+index

    return indexes

def setUpLangDataToSerializer(serializer=None):
    if serializer:
        if len(serializer)>0:
            if 'lang_data' in serializer.keys():
                for item in serializer['lang_data']:
                    # print(item['field_name'],":",item['field_value'])
                    # serializer[item['field_name']]=item['field_value']
                    serializer.update({item['field_name']:item['field_value']})
                serializer.pop('lang_data')
                # print("Previuos===================",serializer)
                # print("Next===================",serializer)
    return serializer

def update_order_tag_elastic(order_id,tag_ids):
    tags_arr = []
    if tag_ids!=None and tag_ids!="":
        tags = str(tag_ids)
        tags = tags.split(",")
        print("Tags====",tags)
        tagDetails = EngageboostTags.objects.filter(id__in=tags)
        if tagDetails.count()>0:
            tagDetails = tagDetails.all()
            for item in tagDetails:
                tags_arr.append({"tag_name":item.tag_name,"color_code":item.color_code})
    elastic = change_field_value_elastic(int(order_id),'EngageboostOrdermaster',{'tag_names':tags_arr})
    return 1

def get_serializer_class_elastic(table_name):
    if table_name=='EngageboostUsers':
        return UserSerializer
    elif table_name=='EngageboostGroups':
        return GroupSerializer
    elif table_name=='EngageboostRolemasters':
        return RoleSerializer
    elif table_name=='EngageboostCategoryMasters':
        return CategoriesSerializer_elastic
    elif table_name=='EngageboostHsnCodeMaster':
        return HsnCodeMasterSerializer
    elif table_name=='EngageboostBrandMasters':
        return BrandSerializer
    elif table_name=='EngageboostProductReviews':
        return ReviewSerializer
    elif table_name=='EngageboostProductCategories':
        return BasicinfometaSerializer
    elif table_name=='EngageboostDiscountMasters':
        return DiscountMasterSerializer
    elif table_name=='EngageboostEmktContactlists':
        return EmktContactlistsSerializer
    elif table_name=='EngageboostEmktContacts':
        return ContactsSerializer
    elif table_name=='EngageboostEmktSegments':
        return SegmentsSerializer
    elif table_name=='EngageboostProducts':
        return BasicinfoSerializer_elastic
    elif table_name=='EngageboostCustomers':
        return CustomerSerializer_elastic
    elif table_name=='EngageboostProductStocks':
        return StockSerializer
    elif table_name=='EngageboostPurchaseOrders':
        return PurchaseordersSerializer
    elif table_name=='EngageboostSuppliers':
        return SuppliersSerializer
    elif table_name=='EngageboostWarehouseMasters':
        return WarehousemastersSerializer
    elif table_name=='EngageboostPurchaseOrdersPaymentMethods':
        return PurchaseOrdersPaymentMethodsSerializer
    elif table_name=='EngageboostPurchaseOrdersShippingMethods':
        return PurchaseOrdersShippingMethodSerializer
    elif table_name=='EngageboostPresets':
        return PresetsSerializer
    elif table_name=='EngageboostOrdermaster':
        return OrderMasterSerializer
    elif table_name=='EngageboostOrderProducts':
        return OrderProductsSerializer
    elif table_name=='EngageboostTrentPicklists':
        return TrentPicklistsSerializer
    elif table_name=='EngageboostShipments':
        return ShipmentsSerializer
    elif table_name=='EngageboostGlobalSettings':
        return GlobalsettingsSerializer
    elif table_name=='EngageboostUnitMasters':
        return UnitmasterSerializer
    elif table_name=='EngageboostCurrencyMasters':
        return CurrencyMastersSerializer
    elif table_name=='EngageboostApplicableAutoresponders':
        return ApplicableAutorespondersSerializer
    elif table_name=='EngageboostShippingMasters':
        return ShippingSerializer
    elif table_name=='EngageboostEmailTypeContents':
        return EmailTypeContentsSerializer
    elif table_name=='EngageboostCompanyWebsites':
        return CompanyWebsiteSerializer
    elif table_name=='EngageboostCurrencyRates':
        return BaseCurrencyratesetSerializer
    elif table_name=='EngageboostCustomerGroup':
        return CustomerGroupSerializer
    elif table_name=='EngageboostShippingMastersSettings':
        return ShippingMastersSettingsSerializer
    elif table_name=='EngageboostFedexZipcodes':
        return FedexZipcodesSerializer
    elif table_name=='EngageboostTags':
        return TagsSerializer
    elif table_name=='EngageboostAwbMasters':
        return AwbMastersSerializer
    elif table_name=='EngageboostShipments':
        return ShipmentsSerializer
    elif table_name =='EngageboostZoneMasters':
        return ZoneMastersSerializer
    elif table_name == 'EngageboostVehicleMasters':
        return VehicleMasterSerializer
    elif table_name == 'EngageboostDeliveryManagers':
        return DeliveryManagerSerializer
    elif table_name == 'EngageboostDeliverySlot':
        return DeliverySlotSerializer
    elif table_name == 'EngageboostPriceFormula':
        return PriceFormulaSerializer
    elif table_name == 'EngageboostCreditPoint':
        return EngageboostCreditPointSerializer
    elif table_name == 'EngageboostCreditPointConditions':
        return EngageboostCreditPointConditionsSerializer
    elif table_name == 'EngageboostProductTaxClasses':
        return ProducttaxclassesSerializer
    elif table_name == 'EngageboostCustomerTaxClasses':
        return CustomerTaxClassesSerializer
    elif table_name == 'EngageboostTaxRates':
        return TaxratesSerializer
    elif table_name == 'EngageboostTaxRuleTables':
        return TaxRuleTablesSerializer
    elif table_name == 'EngageboostMultipleBarcodes':
        return MultipleBarcodeSerializer


def format_serialized_data(table_name,data):
    item_id = data['id']
    if table_name=='EngageboostProducts':
        variations = get_variations(item_id,data['website_id'])
        print("Variation Complete=====",datetime.datetime.now())

        inventory = get_inventory(data['product_stock'])
        print("Inventory Complete=====",datetime.datetime.now())

        taxclass = get_taxclass(data['taxclass'])
        print("Taxclass Complete=====",datetime.datetime.now())

        po_taxclass = get_taxclass(data['po_taxclass'])
        print("POTaxclass Complete=====",datetime.datetime.now())

        barcode = get_barcode(data['barcode_product_id'])
        print("Barcode Complete=====",datetime.datetime.now())

        category = get_category_list(data['product_list'],"name")
        print("Category Complete=====",datetime.datetime.now())

        category_id = get_category_list(data['product_list'],"id")
        print("Category ID Complete=====",datetime.datetime.now())

        category_slug = get_category_list(data['product_list'],"slug")
        print("Category slug Complete=====",datetime.datetime.now())

        product_price = get_channel_currency_product_price(item_id,data['website_id'])
        print("Product Price Complete=====",datetime.datetime.now())

        supplier_id = get_supplier(data['supplier_id'])
        print("Supplier ID Complete=====",datetime.datetime.now())

        custom_fields = get_custom_fields(data['id'])
        print("Custom Field Complete=====",datetime.datetime.now())

        product_cat_warehouse = get_category_warehouse(item_id)
        print("Product Category Complete=====",datetime.datetime.now())

        d1 = {
                "variations":variations,
                "inventory":inventory,
                "taxclass":taxclass,
                "po_taxclass":po_taxclass,
                "barcode":barcode,
                "category":category,
                "category_id":category_id,
                "category_slug":category_slug,
                "channel_currency_product_price":product_price,
                "supplier":supplier_id,
                "custom_fields":custom_fields,
                "category_warehouse":product_cat_warehouse
            }
        data.pop('product_stock')
        data.pop('barcode_product_id')
        data.pop('product_list')

        data = dict(data,**d1)

        link ='products/edit/'+str(item_id)
        tab_name ='Product'
        tab_id ='editproducts'
        parent_id = "77"

    elif table_name=='EngageboostCategoryMasters':
        link ='category/edit/'+str(item_id)
        tab_name ='Category'
        tab_id ='editcategory'
        parent_id = "80"

    elif table_name=='EngageboostCustomers':
        link ='customers/edit/'+str(item_id)
        tab_name ='Customer'
        tab_id ='editcustomers'
        parent_id = "110"

    elif table_name=='EngageboostOrdermaster':
        data = modify_order_details(data)
        link ='orders/edit/'+str(item_id)
        tab_name ='Order'
        tab_id ='editorders'
        parent_id = "83"

    d2 ={
            "link":link,
            "tab_name":tab_name,
            "tab_id":tab_id,
            "tab_parent_id":parent_id
        }
    data = dict(data,**d2)

    data = setUpLangDataToSerializer(data)
    return data

def get_variations(product_id,website_id=1):
    print("=========",product_id)
    collectionsObj = EngageboostCossSellProducts.objects.filter(product_id=product_id).exclude(cross_product_id=None).distinct('cross_product_id')
    # print(collectionsObj.query)
    custom_fields = []
    if collectionsObj.count()>0:
        collectionsData = CossSellProductsSerializer(collectionsObj,many=True)
        for collections in collectionsData.data:
            stock = get_variation_stock(collections['cross_product']['id'])
            childprice = get_channel_currency_product_price(collections['cross_product']['id'],website_id)
            collections['cross_product']['inventory'] = stock
            collections['cross_product']['channel_currency_product_price'] = childprice
            # print("Collections=========",collections['cross_product']['id'])
            fieldvalueObj = EngageboostMarketplaceFieldValue.objects.filter(product_id=collections['cross_product']['id'])
            # print(fieldvalueObj.query)
            if fieldvalueObj.count()>0:
                fieldvalue = fieldvalueObj.all()
                field_data = MarketplaceFieldValueSerializer(fieldvalue,many=True)
                # print(field_data.data)
                for item in field_data.data:
                    fValue = ""
                    if item["value"]!="" and item["value"]!=None:
                        fValue = item["value"]
                        fValue = fValue.split("##")
                        fValue = list(filter(None, fValue))
                    custom_fields.append(
                        {
                            "field_name":item["field_name"],
                            "field_value":fValue,
                            "field_id":item["field_id"],
                            "field_label":item["field_label"],
                            "is_parent":"n",
                            "product_details":collections['cross_product']
                        })

    parentProductObj = EngageboostProducts.objects.filter(id=product_id).first()
    parentProduct_data = EngageboostProductsSerializer(parentProductObj,partial=True)
    parentdata = parentProduct_data.data
    parentstock = get_variation_stock(product_id)
    parentprice = get_channel_currency_product_price(product_id,website_id)
    parentdata['inventory'] = parentstock
    parentdata['channel_currency_product_price'] = parentprice

    fieldvalueObj = EngageboostMarketplaceFieldValue.objects.filter(product_id=product_id)
    if fieldvalueObj.count()>0:
        fieldvalue = fieldvalueObj.all()
        field_data = MarketplaceFieldValueSerializer(fieldvalue,many=True)
        for item in field_data.data:
            fValue = ""
            if item["value"]!="" and item["value"]!=None:
                fValue = item["value"]
                fValue = fValue.split("##")
                fValue = list(filter(None, fValue))
            custom_fields.append(
                {
                    "field_name":item["field_name"],
                    "field_value":fValue,
                    "field_id":item["field_id"],
                    "field_label":item["field_label"],
                    "is_parent":"y",
                    "product_details":parentdata
                })

    return custom_fields

def get_custom_fields(product_id):
    pk = product_id
    try:
        obj 	= EngageboostProductCategories.objects.filter(product_id=pk,is_parent='y')
        if obj.count()>0:
            # product_category 	= EngageboostProductCategories.objects.get(product_id=pk,is_parent='y')
            product_category 	= EngageboostProductCategories.objects.filter(product_id=pk,is_parent='y').first()
            # custom_filter 	= EngageboostDefaultModuleLayoutFields.objects.all().filter(category_id=product_category.category_id,is_system='y').filter( Q(show_market_places__startswith=channel_id+',') | Q(show_market_places__endswith=','+channel_id) | Q(show_market_places__contains=',{0},'.format(channel_id)) | Q(show_market_places__exact=channel_id) ).order_by('section_row','section_col')
            custom 				= EngageboostDefaultModuleLayoutFields.objects.all().filter(category_id=product_category.category_id)
            channel 			= []
            for customs_category_in in custom:
                name=customs_category_in.show_market_places
                channel.append(name)
            str_to_array_channel = ','.join(channel)
            sta_value=str_to_array_channel.split(',')

            # serializer_custom 	= DefaultModuleLayoutFieldsSerializer(custom_filter,many=True)
            # serializer_custom = DefaultModuleLayoutFieldsProductSerializer(custom_filter,many=True)
            product_custom 		= EngageboostMarketplaceFieldValue.objects.all().filter(product_id=pk)
            # print(product_custom.query)
            serializer_productcustom = MarketplaceFieldValueSerializer(product_custom,many=True)
            # print(json.dumps(serializer_productcustom.data))
            for productcustom in serializer_productcustom.data:
                productcustom["field_label_l"]=productcustom['field_label'].lower()
                # print(json.dumps(productcustom))
                if productcustom['lang_data'] and len(productcustom['lang_data'])>0:
                    for productcustom_lang in productcustom['lang_data']:
                        productcustom[productcustom_lang['field_name']]=productcustom_lang['field_value']
            # productcustom.pop('lang_data')

            if(str_to_array_channel):
                settings4 = EngageboostChannels.objects.all().filter(isdeleted='n',isblocked='n').filter(id__in=sta_value)
                serializer4 = ChannelsSerializer(settings4, many=True)
                channel=serializer4.data
            else:
                channel=[]
            if(serializer_productcustom):
                data = []
                for custom_fields_arr in serializer_productcustom.data:
                    data_arr = {
                            "field_id":custom_fields_arr["field_id"],
                            "field_label":custom_fields_arr["field_label"],
                            "field_label_l":custom_fields_arr["field_label_l"],
                            "field_name":custom_fields_arr["field_name"],
                            "value":custom_fields_arr["value"]
                            }
                    data.append(data_arr)

            else:
                data = []
        else:
            data = []
        return data
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data1={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error), 'message':'Data Not Found',}
        print(data1)
        data = []
        return data

def get_inventory(product_arr):
    inventoryarr=[]
    for inventory in product_arr:
        warehouse_code=""
        warehouse_name=""
        stock=0
        warehouse_id = 0
        if inventory['warehouse']:
            if inventory['warehouse']['code']:
                warehouse_code=inventory['warehouse']['code']
            if inventory['warehouse']['name']:
                warehouse_name=inventory['warehouse']['name']
            if inventory['warehouse']['id']:
                warehouse_id=inventory['warehouse']['id']
        if inventory['real_stock']:
            stock=inventory['real_stock']
        inventoryarr.append({"id":int(warehouse_id),"name":warehouse_name,"code":warehouse_code,"stock":stock})

    return inventoryarr

# def get_taxclass(product_arr):
# 	if product_arr!=None:
# 		return product_arr["name"]

def get_taxclass(product_arr,field_name = None):
    try:
        if product_arr!=None:
            return product_arr["name"]
    except:
        name = ""
        try:
            product_obj = EngageboostProducts.objects.filter(id=product_arr)
            if product_obj.count()>0:
                product_obj = product_obj.values().first()
                taxObj = EngageboostTaxclasses.objects.filter(id = product_obj[field_name])
                if taxObj.count()>0:
                    taxObj = taxObj.values().first()
                    name = taxObj["name"]
        except:
            pass
        return name

def get_barcode(product_arr):
    barcodearr=[]
    if len(product_arr)>0:
        for barcode in product_arr:
            barcodearr.append(barcode['barcode'])
    return barcodearr

def get_category(product_arr,field):
    categoryarr=[];
    catdict={}
    if field=="name":
        for cat in product_arr:
            catdict=cat["category"][field]
            categoryarr.append(catdict)
        category=','.join([str(i) for i in categoryarr])
        return category
    elif field=="id":
        for cat in product_arr:
            catdict=cat["category"][field]
            categoryarr.append({"id":catdict})
        # category=','.join([str(i) for i in categoryarr])
        return categoryarr
    else:
        return ""

def get_category_warehouse(product_id):
    warehousearr=[];
    catmap = EngageboostProductCategories.objects.filter(isdeleted="n",isblocked="n",product_id=product_id)
    if catmap.count()>0:
        catmap = catmap.distinct("category_id").values("category_id").all()
        catwar = EngageboostCategoryWarehouse.objects.filter(category_id__in=catmap)
        if catwar.count()>0:
            catwar = catwar.distinct("warehouse_id").values("warehouse_id").all()
            wareObj = EngageboostWarehouseMasters.objects.filter(isdeleted="n",isblocked="n",id__in=catwar)
            if wareObj.count()>0:
                wareObj = wareObj.values().all()
                warehousedict={}
                for war_details in wareObj:
                    warehouse_code=""
                    warehouse_name=""
                    warehouse_id = 0

                    if war_details['code']:
                        warehouse_code=war_details['code']
                    if war_details['name']:
                        warehouse_name=war_details['name']
                    if war_details['id']:
                        warehouse_id=war_details['id']
                    warehousearr.append({"id":int(warehouse_id),"name":warehouse_name,"code":warehouse_code})
                # category=','.join([str(i) for i in categoryarr])
    return warehousearr

def get_product_images(product_id):
    rs = EngageboostProductimages.objects.filter(product_id = product_id)
    data = []
    if rs.count()>0:
        rsData = rs.all()
        imagedata = ProductImagesSerializer(rsData, many=True)
        data = imagedata.data
    return data

def get_channel_currency_product_price(product_id,website_id=1,warehouses=None, first=0):
    all_valid_price_type_ids = []
    mainObj = EngageboostPriceTypeMaster.objects.filter(isdeleted="n",isblocked="n")
    if mainObj.count()>0:
        mainObj = mainObj.values().all()
        for price_type_item in mainObj:
            subObj = EngageboostProductPriceTypeMaster.objects.filter(isdeleted="n",isblocked="n",price_type_id=price_type_item['id'],product_id=product_id).order_by("id")
            # print("subObj=======", subObj.query)
            if subObj.count()>0:
                # subObj = subObj.values().first()
                subObj = subObj.values().all()
                for price in subObj:
                    all_valid_price_type_ids.append(price['id'])

    if warehouses == None:
        warehouses = EngageboostWarehouseMasters.objects.filter(isdeleted='n').values_list("id",flat=True)
        warehouses = list(warehouses)

    data = []
    discount_product_id = product_id
    discount_product_cat_id = EngageboostProductCategories.objects.filter(product_id=discount_product_id).values(
        'category_id').first()
    if len(all_valid_price_type_ids)>0:

        rs = EngageboostChannelCurrencyProductPrice.objects.filter(product_id = product_id,warehouse_id__in=warehouses,product_price_type_id__in=all_valid_price_type_ids).distinct("product_id","product_price_type_id","warehouse_id")

        if rs.count()>0:
            rsData = rs.all()
            serializar_data = ChannelCurrencyProductPriceSerializer(rsData, many=True)
            data = serializar_data.data
            for i in range(len(data)):
                product_seri = getproduct_data(product_id)
                # ------Binayak Start 30-03-2021------#
                if first == 0:
                    if(product_seri):
                        if(data[i]["price"]):
                            product_seri["new_default_price"] = 0
                            product_seri["default_price"] = data[i]["price"]
                        else:
                            product_seri["new_default_price"] = 0
                            product_seri["default_price"] = 0
                        product_seri['qty'] = 1
                        discount_array = generate_discount_conditions(website_id,None,None, data[i]["warehouse_id"],product_id,discount_product_cat_id['category_id'])
                        product_new_price = genrate_new_prodcut_with_discount(None,product_seri,discount_array)
                        if product_new_price:
                            data[i]["new_default_price"]= product_new_price['new_default_price']
                            data[i]["new_default_price_unit"]=product_new_price['new_default_price_unit']
                            data[i]["discount_price_unit"]= product_new_price['discount_price_unit']
                            data[i]["discount_price"]= product_new_price['discount_price']
                            data[i]["discount_amount"]=product_new_price['discount_amount']
                            data[i]["disc_type"]= product_new_price['disc_type']
                            data[i]["coupon"]= product_new_price['coupon']
                        else:
                            data[i]["new_default_price"]= 0
                            data[i]["new_default_price_unit"]=0
                            data[i]["discount_price_unit"]= 0
                            data[i]["discount_price"]= 0
                            data[i]["discount_amount"]=0
                            data[i]["disc_type"]= ""
                            data[i]["coupon"]= ""
                    else:
                        if(data[i]["price"]):
                            data[i]["new_default_price"]= data[i]["price"]
                            data[i]["new_default_price_unit"]=data[i]["price"]
                        else:
                            data[i]["new_default_price"]= 0
                            data[i]["new_default_price_unit"]=0
                        data[i]["discount_price_unit"]= 0
                        data[i]["discount_price"]= 0
                        data[i]["discount_amount"]=0
                        data[i]["disc_type"]= ""
                        data[i]["coupon"]= ""
                elif first == 1:
                    data[i]["new_default_price"] = 0
                    data[i]["new_default_price_unit"] = 0
                    data[i]["discount_price_unit"] = 0
                    data[i]["discount_price"] = 0
                    data[i]["discount_amount"] = 0
                    data[i]["disc_type"] = ""
                    data[i]["coupon"] = ""
                # ------Binayak Start 30-03-2021------#
    # print("Price==============",json.dumps(data))
    return data

def get_category_list(product_arr,field):
    catdict=[];
    for cat in product_arr:
        if(cat["category"]['parent_id']!=0):
            objCategorychild1 = EngageboostCategoryMasters.objects.filter(id=cat["category"]['parent_id'],isdeleted='n',isblocked='n')

            if objCategorychild1.count()>0:
                objCategorychild1 = objCategorychild1.first()
                if(objCategorychild1.parent_id!=0):
                    objCategorychild2 = EngageboostCategoryMasters.objects.filter(id=objCategorychild1.parent_id,isdeleted='n',isblocked='n')

                    if objCategorychild2.count()>0:
                        objCategorychild2=objCategorychild2.first()
                        if(objCategorychild2.parent_id!=0):
                            objCategorychild3 = EngageboostCategoryMasters.objects.filter(id=objCategorychild2.parent_id,isdeleted='n',isblocked='n')

                            if objCategorychild3.count()>0:
                                objCategorychild3 = objCategorychild3.first()
                                if(objCategorychild3.parent_id!=0):
                                    if(field == "name"):
                                        catdict.append(objCategorychild3.name)
                                        catdict.append(objCategorychild2.name)
                                        catdict.append(objCategorychild1.name)
                                    elif(field == "id"):
                                        catdict.append(objCategorychild3.id)
                                        catdict.append(objCategorychild2.id)
                                        catdict.append(objCategorychild1.id)
                                    elif(field == "slug"):
                                        catdict.append(objCategorychild3.slug)
                                        catdict.append(objCategorychild2.slug)
                                        catdict.append(objCategorychild1.slug)
                                    catdict.append(cat["category"][field])
                                else:
                                    if(field == "name"):
                                        catdict.append(objCategorychild2.name)
                                        catdict.append(objCategorychild1.name)
                                    elif(field == "id"):
                                        catdict.append(objCategorychild2.id)
                                        catdict.append(objCategorychild1.id)
                                    elif(field == "slug"):
                                        catdict.append(objCategorychild2.slug)
                                        catdict.append(objCategorychild1.slug)
                                    catdict.append(cat["category"][field])
                        else:
                            if(field == "name"):
                                catdict.append(objCategorychild2.name)
                                catdict.append(objCategorychild1.name)
                            elif(field == "id"):
                                catdict.append(objCategorychild2.id)
                                catdict.append(objCategorychild1.id)
                            elif(field == "slug"):
                                catdict.append(objCategorychild2.slug)
                                catdict.append(objCategorychild1.slug)
                            catdict.append(cat["category"][field])
                else:
                    if(field == "name"):
                        catdict.append(objCategorychild1.name)
                    elif(field == "id"):
                        catdict.append(objCategorychild1.id)
                    elif(field == "slug"):
                        catdict.append(objCategorychild1.slug)
                    catdict.append(cat["category"][field])
        else:
            catdict.append(cat["category"][field])
    catdict = list(set(catdict))
    return catdict

def getproduct_data(product_id):
    try:
        cnt =EngageboostProducts.objects.filter(isdeleted='n',isblocked='n', id=product_id).count()
        if(cnt>0):
            condition = EngageboostProducts.objects.get(isdeleted='n',isblocked='n',id=product_id)
            # print(condition.query)
            product_details = BasicinfoSerializer(condition)
            # print(product_details.data)
            conditions = EngageboostProductCategories.objects.filter(product_id=product_id).first()
            if conditions and product_details.data:
                product_details.data["category_id"]=conditions.category_id

            return product_details.data
        else:
            return False
    except Exception as ex:
        import sys,os
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

def generate_discount_conditions_old(website_id,user_group_id,discountIds=None, warehouse_id = None):
    now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
    if user_group_id:
        if warehouse_id is not None:
            DiscountMasterCond = EngageboostDiscountMasters.objects.order_by("-id").filter(website_id=website_id,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc,customer_group__iregex=r"\y{0}\y".format(user_group_id),isdeleted='n',isblocked='n',discount_master_type=0, warehouse_id__iregex=r"\y{0}\y".format(warehouse_id)).all()[:1]
        else:
            DiscountMasterCond = EngageboostDiscountMasters.objects.order_by("-id").filter(website_id=website_id,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc,customer_group__iregex=r"\y{0}\y".format(user_group_id),isdeleted='n',isblocked='n',discount_master_type=0).all()[:1]
    else:
        if warehouse_id is not None:
            DiscountMasterCond = EngageboostDiscountMasters.objects.order_by("-id").filter(website_id=website_id,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc,isdeleted='n',isblocked='n',discount_master_type=0, warehouse_id__iregex=r"\y{0}\y".format(warehouse_id)).all()[:1]
        else:
            DiscountMasterCond = EngageboostDiscountMasters.objects.order_by("-id").filter(website_id=website_id,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc,isdeleted='n',isblocked='n',discount_master_type=0).all()[:1]
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


def generate_discount_conditions(website_id, user_group_id, discountIds=None, warehouse_id=None, product_id=None,
                                 category_id=None):
    # now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    # now_utc = datetime.datetime.now(timezone('UTC'))
    global_setting_date = EngageboostGlobalSettings.objects.filter(website_id=1, isdeleted='n', isblocked='n').first()
    global_setting_zone = EngageboostTimezones.objects.filter(id=global_setting_date.timezone_id).first()
    time_offset = global_setting_zone.offset

    date_time_obj = now_utc
    today = date_time_obj
    user_group_id = None
    if user_group_id:
        if warehouse_id is not None:
            DiscountMasterCond = EngageboostDiscountMasters.objects.order_by("discount_priority").filter(
                website_id=website_id, disc_start_date__lte=today, disc_end_date__gte=today,
                customer_group__iregex=r"\y{0}\y".format(user_group_id), isdeleted='n', isblocked='n',
                discount_master_type=0, warehouse_id__iregex=r"\y{0}\y".format(warehouse_id)).exclude(
                disc_type__in=[8, 9, 10]).all()
        else:
            DiscountMasterCond = EngageboostDiscountMasters.objects.order_by("discount_priority").filter(
                website_id=website_id, disc_start_date__lte=today, disc_end_date__gte=today,
                customer_group__iregex=r"\y{0}\y".format(user_group_id), isdeleted='n', isblocked='n',
                discount_master_type=0).exclude(disc_type__in=[8, 9, 10]).all()
    else:
        if warehouse_id is not None:
            DiscountMasterCond = EngageboostDiscountMasters.objects.order_by("discount_priority").filter(
                website_id=website_id, disc_start_date__lte=today, disc_end_date__gte=today, isdeleted='n',
                isblocked='n', discount_master_type=0, warehouse_id__iregex=r"\y{0}\y".format(warehouse_id)).exclude(
                disc_type__in=[8, 9, 10]).all()

        else:
            DiscountMasterCond = EngageboostDiscountMasters.objects.order_by("discount_priority").filter(
                website_id=website_id, disc_start_date__lte=today, disc_end_date__gte=today, isdeleted='n',
                isblocked='n', discount_master_type=0).exclude(disc_type__in=[8, 9, 10]).all()
        if product_id is not None and category_id is not None:
            DiscountMasterCond = DiscountMasterCond.filter(
                Q(DiscountMastersConditions__all_product_id__iregex=r"\y{0}\y".format(product_id)) | Q(
                    DiscountMastersConditions__all_category_id__iregex=r"\y{0}\y".format(category_id)))
        else:
            if int(product_id) is not None and int(product_id) > 0 and product_id != "":
                DiscountMasterCond = DiscountMasterCond.filter(
                    Q(DiscountMastersConditions__all_product_id__iregex=r"\y{0}\y".format(product_id)))
            if category_id is not None and category_id > 0 and category_id != "":
                DiscountMasterCond = DiscountMasterCond.filter(
                    Q(DiscountMastersConditions__all_category_id__iregex=r"\y{0}\y".format(category_id)))

    if discountIds:
        DiscountMasterCond = DiscountMasterCond.filter(id__in=discountIds)

    # print("DiscountMasterCond++++++", DiscountMasterCond.query)
    DiscountMasterSerializerData = DiscountMasterSerializer(DiscountMasterCond, many=True)

    if DiscountMasterSerializerData:
        for DiscountMaster in DiscountMasterSerializerData.data:
            DiscountMastersConditionsCond = EngageboostDiscountMastersConditions.objects.filter(
                discount_master_id=DiscountMaster["id"]).all()
            if DiscountMastersConditionsCond:
                DiscountMastersConditionsSerializerData = DiscountConditionsSerializer(DiscountMastersConditionsCond,
                                                                                       many=True)
                DiscountMastersConditionsSerializerData = DiscountMastersConditionsSerializerData.data
            else:
                DiscountMastersConditionsSerializerData = []

            DiscountMaster["discount_conditions"] = DiscountMastersConditionsSerializerData
    return DiscountMasterSerializerData.data


def genrate_new_prodcut_with_discount(user_id=None,product=None,discount_array_new=None,category_id=None,sub_category_id=None,cart_subtotal=None):
    try:
        if discount_array_new:
            exclude_ids = []
            for discount_array in discount_array_new:
                if(product["id"] not in exclude_ids):
                    return_price = check_conditions(user_id,product,discount_array,category_id,sub_category_id,cart_subtotal)
                    price_array = return_price.split('^')
                    if(price_array[2] == 'true'):
                        if price_array[1] != "product" and price_array[1] > "0" and float(product["default_price"]) != float(price_array[0]):
                            product["discount_price"] = float(price_array[1])*float(product["qty"])
                            product["new_default_price_unit"]   = float(price_array[0])
                            product["new_default_price"]        = float(price_array[0])*float(product["qty"])
                            product["discount_price_unit"]      = float(price_array[1])

                            product["discount_amount"]          = float(discount_array["amount"])
                            product["disc_type"]                = discount_array["disc_type"]
                            product["coupon"]                   = discount_array["name"]
                            exclude_ids.append(product["id"])
                        else:
                            product["new_default_price_unit"] = float(product["default_price"])
                            product["new_default_price"] = float(product["default_price"])*float(product["qty"])
                            if(price_array[1]!="product"):
                                product["discount_price_unit"] = float(price_array[1])
                                product["discount_price"] = float(price_array[1])*float(product["qty"])
                            else:
                                product["discount_price_unit"] = float(0)
                                product["discount_price"] = float(0)
                            product["discount_amount"] = float(0)
                            product["disc_type"] = ""
                            product["coupon"] = ""
                    else:
                        continue
        else:
            product["new_default_price_unit"] = float(product["default_price"])
            product["new_default_price"] = float(product["default_price"])*float(product["qty"])
            product["discount_price_unit"] = float(0)
            product["discount_price"] = float(0)*float(product["qty"])
            product["discount_amount"] = float(0)
            product["disc_type"] = ""
            product["coupon"] = ""
        if(float(product["new_default_price"])==0.0):
            product["new_default_price_unit"] = float(product["default_price"])
            product["new_default_price"] = float(product["default_price"])*float(product["qty"])
            product["discount_price_unit"] = float(0)
            product["discount_price"] = float(0)*float(product["qty"])
            product["discount_amount"] = float(0)
            product["disc_type"] = ""
            product["coupon"] = ""
        return product
    except Exception as ex:
        import sys,os
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #print(exc_type, fname, exc_tb.tb_lineno)


def get_supplier(supplier_id):
    supplierarr=[];
    if supplier_id:
        supplier=supplier_id.split(",")
        for sid in supplier:
            if sid:
                fetch_supplier=EngageboostSuppliers.objects.get(id=sid)
                supplierarr.append(fetch_supplier.name)
        supplier=','.join(supplierarr)
        supplier_name=supplier
        # print(supplier_name)
    else:
        supplier_name=''
    return supplier_name

def get_variation_stock(product_id):
    obj = EngageboostProductStocks.objects.filter(product_id=product_id)
    if obj.count()>0:
        product_arr = obj.all()
        product_arr = StockViewSerializer(product_arr,many=True)
        # print(product_arr.data)
        inventoryarr=[]
        for inventory in product_arr.data:
            warehouse_code=""
            warehouse_name=""
            stock=0
            warehouse_id = 0
            if inventory['warehouse']:
                warehouse_id=inventory['warehouse']
            if inventory['real_stock']:
                stock=inventory['real_stock']
            inventoryarr.append({"warehouse_id":int(warehouse_id),"name":warehouse_name,"code":warehouse_code,"stock":stock})

        return inventoryarr

def modify_order_details(order_arr):
    username = ""
    userObj = EngageboostUsers.objects.filter(id=order_arr['assign_to']).first()
    if userObj:
        username = userObj.username
    order_arr['assign_to_name']=username

    warehousename =""
    wareHouseObj = EngageboostWarehouseMasters.objects.filter(id=order_arr['assign_wh']).first()
    if wareHouseObj:
        warehousename = wareHouseObj.name
    order_arr['assign_wh_name']=warehousename

    products_id = []
    quantity = 0
    products = EngageboostOrderProducts.objects.filter(order_id=order_arr["id"])
    if products.count()>0:
        products = products.all()
        for orderProduct in products:
            products_id.append(orderProduct.product_id)
            deleted_quantity = orderProduct.deleted_quantity
            if orderProduct.shortage:
                shortage = orderProduct.shortage
            else:
                shortage = 0
            if orderProduct.returns:
                returns = orderProduct.returns
            else:
                returns = 0
            quantity = quantity+(int(orderProduct.quantity)-int(deleted_quantity)-int(shortage)-int(returns))
        if quantity < 0:
            quantity = 0
    order_arr['products_id']=products_id
    order_arr["quantity"] = quantity

    tags_arr = []
    if order_arr['tags']:
        tags = order_arr['tags']
        tags = tags.split(",")
        tagDetails = EngageboostTags.objects.filter(id__in=tags)
        if tagDetails.count()>0:
            tagDetails = tagDetails.all()
            for item in tagDetails:
                tags_arr.append({"tag_name":item.tag_name,"color_code":item.color_code})
    order_arr['tag_names'] = tags_arr

    return order_arr

def get_product_stock(product_id):
    inventory_result = EngageboostProductStocks.objects.filter(isdeleted='n', isblocked='n', product_id=product_id).all()
    inventories = WarehouseStockSerializer(inventory_result,many=True)
    inventoryarr=[]
    for inventory in inventories.data:
        # print("inventory============", json.dumps(inventory))
        warehouse_code=""
        warehouse_name=""
        stock=0
        warehouse_id = 0
        if inventory['warehouse']:
            if inventory['warehouse']['code']:
                warehouse_code=inventory['warehouse']['code']
            if inventory['warehouse']['name']:
                warehouse_name=inventory['warehouse']['name']
            if inventory['warehouse']['id']:
                warehouse_id=inventory['warehouse']['id']
        if inventory['real_stock']:
            stock=inventory['real_stock']
        inventoryarr.append({"id":int(warehouse_id),"name":warehouse_name,"code":warehouse_code,"stock":stock})

    return inventoryarr


def check_conditions(user_id=None,ind_product=None,discount_array=None,category_id=None,sub_category_id=None,cart_subtotal=None):
    default_price  = float(0)
    discount_price = float(0)
    if("discount_conditions" in discount_array.keys()):
        discount_array_condition = discount_array["discount_conditions"]
    elif("DiscountMasterCondition" in discount_array.keys()):
        discount_array_condition = discount_array["DiscountMasterCondition"]
    product_array_disc_applied = []
    flag="false"
    previous_flag = "false"
    i=0
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
                    # sub_category_id_array.append(str(pro["category_id"]))
            if sub_category_id_array:
                for index in range(len(sub_category_id_array)):
                    if ind_cond["condition"] == "==":
                        if str(sub_category_id_array[index]) in category_id_array:
                            flag = "true"
                            break
                        else:
                            flag = "false"
                    else:
                        if str(sub_category_id_array[index]) in category_id_array:
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
                if flag=="true" and previous_flag=="true":
                    previous_flag="true"
                else:
                    previous_flag="false"

            if previos_condition=="OR":
                if flag=="false" and previous_flag=="false":
                    previous_flag="false"
                else:
                    previous_flag="true"
        else:
            previous_flag = flag

        if(previous_flag == "false"):
            break
        previos_condition=ind_cond["condition_type"]
        i=i+1
    if previous_flag == "true":
        if discount_array["disc_type"]==1 or discount_array["disc_type"]==5:
            discount_array["discountPrice"]=float(ind_product["default_price"])*float(discount_array["amount"])/float(100)
        else:
            discount_array["discountPrice"]=float(discount_array["amount"])
        if discount_array["disc_type"]!=4:
            if ind_product["new_default_price"]:
                if ind_product["new_default_price"]== 0:
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
        else:
            default_price  = float(ind_product["default_price"])
            discount_price = float(0)
    return str(default_price)+"^"+str(discount_price)+"^"+str(previous_flag)

def get_geo_location_uae(address,city,country,state=None, post_code=None):
    import requests
    try:
        #address = str(address)+","+str(city)
        if post_code is not None:
            address = str(address)+","+str(post_code)
        if state is not None:
            stateObj = EngageboostStates.objects.get(id=state)
            if stateObj:
                address = address+","+str(stateObj.state_name)

        countryObj = EngageboostCountries.objects.get(id=country)
        if countryObj:
            address = address+","+str(countryObj.country_name)

        api_key = 'AIzaSyDwJfFz9Hyur4RkbEa_Hlt6Fkibr6rYhJo'
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&sensor=false&key='+api_key)
        resp_json_payload = response.json()
        geometry = resp_json_payload["results"][0]['geometry']['location']
        location = {"lat":geometry["lat"],"lng":geometry["lng"]}
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        str_status = 0
        location = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
    # except:
    #     latitude="22.5427604"
    #     longitude="88.3859595"
    return location

# @postpone
def update_category_warehouse_stock_price(category_id,old_warehouses,new_warehouses):
    try:
        deleted_warehouse_arr = list(set(old_warehouses) - set(new_warehouses))
        products = EngageboostProductCategories.objects.filter(category_id=category_id, product_id__isblocked='n', product_id__isdeleted='n').values_list("product_id",flat=True).all()

        for warehouse in deleted_warehouse_arr:
            for product in products:
                prices = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=product,warehouse_id=warehouse)
                if prices.count()>0:
                    # print("Price===============",product,warehouse,prices.count())
                    prices.update(price=0,cost=0,mrp=0,min_quantity=0,max_quantity=0)
                    product_price = get_channel_currency_product_price(product)
                    elastic = change_field_value_elastic(product,'EngageboostProducts',{'channel_currency_product_price':product_price})

                stocks = EngageboostProductStocks.objects.filter(product_id=product,warehouse_id=warehouse)
                if stocks.count()>0:
                    # print("Stock===============",product,warehouse,stocks.count())
                    stocks.update(stock=0,real_stock=0)
                    product_stock = get_product_stock(product)
                    elastic = change_field_value_elastic(product,'EngageboostProducts',{'inventory':product_stock})
    except:
        pass

    try:
        added_warehouse = list(set(new_warehouses) - set(old_warehouses))
        products = EngageboostProductCategories.objects.filter(category_id=category_id, product_id__isblocked='n', product_id__isdeleted='n').values_list("product_id",flat=True).all()

        for warehouse in added_warehouse:
            for product in products:
                prices = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=product,warehouse_id=warehouse)
                if prices.count()>0:
                    # print("Price===============",product,warehouse,prices.count())
                    prices.update(price=0,cost=0,mrp=0,min_quantity=0,max_quantity=0)
                else:
                    EngageboostChannelCurrencyProductPrice.objects.create(price=0,cost=0,mrp=0,min_quantity=0,max_quantity=0,product_id=product,warehouse_id=warehouse)
                product_price = get_channel_currency_product_price(product)
                elastic = change_field_value_elastic(product,'EngageboostProducts',{'channel_currency_product_price':product_price})

                stocks = EngageboostProductStocks.objects.filter(product_id=product,warehouse_id=warehouse)
                if stocks.count()>0:
                    # print("Stock===============",product,warehouse,stocks.count())
                    stocks.update(stock=0,real_stock=0)
                else:
                    EngageboostProductStocks.objects.create(product_id=product,warehouse_id=warehouse,stock=0,real_stock=0)
                product_stock = get_product_stock(product)
                elastic = change_field_value_elastic(product,'EngageboostProducts',{'inventory':product_stock})
    except:
        pass
    return 1

@postpone
def update_category_warehouse_stock_price_test(category_id,old_warehouses,new_warehouses):
    print("======in here we go 123====")
    es = connect_elastic()
    # print("======in here old_warehouses====", list(old_warehouses))
    # print("======in here new_warehouses====", new_warehouses)
    table_name = 'EngageboostProducts'
    docs = []
    try:
        deleted_warehouse_arr = list(set(old_warehouses) - set(new_warehouses))
        products = EngageboostProductCategories.objects.filter(category_id=category_id, product_id__isblocked='n', product_id__isdeleted='n').values_list("product_id",flat=True).all()

        # print("====products=======", list(products))
        # print("====products count=======", products.count())

        #-----Binayak Start 16-03-2021------#

        if products:
            module_name = get_index_name_elastic(products[0], table_name)

            data_string = []
            for product_id in list(products):
                id_string = {
                    "_id": product_id,
                    "_source": {
                        "include": ["channel_currency_product_price", "inventory"]
                    }
                }
                data_string.append(id_string)
            # print("data_string=======>", data_string)

            prod_exists = es.mget(body=json.dumps({"docs": data_string}), index=module_name, doc_type="data")
            # -----Binayak End 16-03-2021------#
            # for warehouse in deleted_warehouse_arr:
            for product in prod_exists['docs']:
                cm_id = product['_id']
                # prices = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=product,warehouse_id=warehouse)
                prices = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=cm_id,warehouse_id__in=deleted_warehouse_arr)
                if prices.count()>0:
                    # print("Price===============",product,warehouse,prices.count())
                    prices.update(price=0,cost=0,mrp=0,min_quantity=0,max_quantity=0)
                    if product['found'] == True:
                        # print("======item======", item)
                        if len(deleted_warehouse_arr)>0:
                            price_data = product['_source']['channel_currency_product_price']
                            warehouse_list = deleted_warehouse_arr.copy()
                            modified_price_data = multiple_warehouse_channel_currency_price_update_string(cm_id, price_data, warehouse_list)
                            data = {"channel_currency_product_price": modified_price_data}

                            header = {
                                "_op_type": 'update',
                                "_index": module_name,
                                "_type": "data",
                                "_id": cm_id,
                                "doc": data
                            }
                            docs.append(header)
                    # else:
                    #     now_item = products.filter(id=cm_id)
                    #     serializer_class = get_serializer_class_elastic(table_name)
                    #     # serializer = serializer_class(item,partial=True)
                    #     serializer = serializer_class(now_item, partial=True)
                    #     data = serializer.data
                    #     # print("Data Formatting Start=====",datetime.now())
                    #     # data = common.setUpLangDataToSerializer(data)
                    #     data = format_serialized_data(table_name, data)
                    #
                    #     header = {
                    #         "_index": module_name,
                    #         "_type": "data",
                    #         "_id": cm_id,
                    #         "_source": data
                    #     }
                    #     # print("======add header=======", header)
                    #     docs.append(header)
                        # return
                    # product_price = get_channel_currency_product_price(product)
                    # elastic = change_field_value_elastic(product,'EngageboostProducts',{'channel_currency_product_price':product_price})

                # stocks = EngageboostProductStocks.objects.filter(product_id=product,warehouse_id=warehouse)
                stocks = EngageboostProductStocks.objects.filter(product_id=cm_id,warehouse_id__in=deleted_warehouse_arr)
                if stocks.count()>0:
                    # print("Stock===============",product,warehouse,stocks.count())
                    stocks.update(stock=0,real_stock=0)
                    product_stock = get_product_stock(cm_id)
                    data = {"inventory": product_stock}
                    # elastic = change_field_value_elastic(product,'EngageboostProducts',{'inventory':product_stock})
                    header = {
                        "_op_type": 'update',
                        "_index": module_name,
                        "_type": "data",
                        "_id": cm_id,
                        "doc": data
                    }
                    docs.append(header)

            # print("=====docs======", docs)
    except:
        pass
    print("=====done======")
    try:

        added_warehouse = list(set(new_warehouses) - set(old_warehouses))
        print('====added_warehouse=====', added_warehouse)
        products = EngageboostProductCategories.objects.filter(category_id=category_id, product_id__isblocked='n', product_id__isdeleted='n').values_list("product_id",flat=True).all()

        if products and len(added_warehouse)>0:
            print("====should not be here=====")
            module_name = get_index_name_elastic(products[0], table_name)

            data_string = []
            for product_id in list(products):
                id_string = {
                    "_id": product_id,
                    "_source": {
                        "include": ["channel_currency_product_price", "inventory"]
                    }
                }
                data_string.append(id_string)
            # print("data_string=======>", data_string)

            prod_exists = es.mget(body=json.dumps({"docs": data_string}), index=module_name, doc_type="data")
            # for warehouse in added_warehouse:
            for product in prod_exists['docs']:
                cm_id = product['_id']
                prices = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=cm_id,warehouse_id__in=added_warehouse)
                if prices.count()>0:
                    # print("Price===============",product,warehouse,prices.count())
                    prices.update(price=0,cost=0,mrp=0,min_quantity=0,max_quantity=0)
                else:
                    EngageboostChannelCurrencyProductPrice.objects.create(price=0,cost=0,mrp=0,min_quantity=0,max_quantity=0,product_id=cm_id,warehouse_id__in=added_warehouse)
                if product['found'] == True:
                # # print("======item======", item)
                    if len(added_warehouse)>0:
                        price_data = product['_source']['channel_currency_product_price']
                        warehouse_list = added_warehouse.copy()
                        modified_price_data = multiple_warehouse_channel_currency_price_update_string(cm_id, price_data, warehouse_list)
                        data = {"channel_currency_product_price": modified_price_data}

                        header = {
                            "_op_type": 'update',
                            "_index": module_name,
                            "_type": "data",
                            "_id": cm_id,
                            "doc": data
                        }
                        docs.append(header)
                    # else:
                    #     now_item = products.filter(id=cm_id)
                    #     serializer_class = get_serializer_class_elastic(table_name)
                    #     # serializer = serializer_class(item,partial=True)
                    #     serializer = serializer_class(now_item, partial=True)
                    #     data = serializer.data
                    #     # print("Data Formatting Start=====",datetime.now())
                    #     # data = common.setUpLangDataToSerializer(data)
                    #     data = format_serialized_data(table_name, data)
                    #
                    #     header = {
                    #         "_index": module_name,
                    #         "_type": "data",
                    #         "_id": cm_id,
                    #         "_source": data
                    #     }
                        # print("======add header=======", header)
                    #     docs.append(header)
                # product_price = get_channel_currency_product_price(product)
                # elastic = change_field_value_elastic(product,'EngageboostProducts',{'channel_currency_product_price':product_price})

                stocks = EngageboostProductStocks.objects.filter(product_id=cm_id,warehouse_id__in=added_warehouse)
                if stocks.count()>0:
                    # print("Stock===============",product,warehouse,stocks.count())
                    stocks.update(stock=0,real_stock=0)
                else:
                    EngageboostProductStocks.objects.create(product_id=cm_id,warehouse_id__in=added_warehouse,stock=0,real_stock=0)
                product_stock = get_product_stock(cm_id)
                data = {"inventory": product_stock}
                # elastic = change_field_value_elastic(product,'EngageboostProducts',{'inventory':product_stock})
                header = {
                    "_op_type": 'update',
                    "_index": module_name,
                    "_type": "data",
                    "_id": cm_id,
                    "doc": data
                }
                docs.append(header)
                # elastic = change_field_value_elastic(product,'EngageboostProducts',{'inventory':product_stock})
    except:
        pass
    # print("=======docs=======", docs)
    obj = helpers.bulk(es, docs)
    # print("=======obj update_category_warehouse_stock_price_test=======", obj)
    # response = emailcomponent.testmail('binayak.santra@navsoft.in', "Data updated to Elastic update_category_warehouse_stock_price_test",
    #                                    'Data preparation and pushed to elastic update_category_warehouse_stock_price_test' + str(datetime.datetime.now()) + ' datas==123===>' + str(obj) + ' elastic update data ' + str(docs))
    return 1

def get_item_mail(orderid=None):
    if orderid is not None:
        rs_order_products = EngageboostOrderProducts.objects.filter(order_id = orderid)
        if rs_order_products:
            cart_data = OrderProductsSerializer(rs_order_products, many=True)
            cart_data = cart_data.data
            html = ""
            if cart_data:
                for cartdata in cart_data:
                    new_product_price = Decimal(cartdata["product_price"]).quantize(Decimal('.00'))
                    product_img = ""
                    if len(cartdata['product']['product_images'])>0:
                        product_img = cartdata['product']['product_images'][0]['img']
                    html = html+'<tr>'
                    html = html+'<td colspan="2">'
                    html = html+'<table cellpadding="10" width="600" style="width:94.5%;padding-left:3.5%">'
                    html = html+'<tbody><tr>'
                    html = html+'<td style="width:50px;padding-top:0;padding-bottom:0">'
                    html = html+'<img src="http://lifcogrocery.s3.amazonaws.com/Lifco/lifco/product/200x200/'+product_img+'" class="CToWUd" style="height:50px"></td>'
                    #html = html+'<img src="http://boostmysale.s3.amazonaws.com/Lifco/lifco/product/200x200/'+product_img+'" class="CToWUd" style="height:50px"></td>'
                    html = html+'<td align="left" style="width:300px" valign="top">'
                    html = html+'<p style="padding:0px;color:#333;line-height:20px;margin:0">'+cartdata['product']["name"]+'<br></p><p style="color:#999999">Quantity: <span style="color:#333">'+str(int(cartdata['quantity'])-int(cartdata['deleted_quantity'])-int(cartdata['returns'])-int(cartdata['shortage']))+'</span>'
                    # if int(cartdata['grn_quantity'])<=0:
                    if (int(cartdata['quantity'])-int(cartdata['deleted_quantity'])-int(cartdata['returns'])-int(cartdata['shortage'])) <= 0:
                        html = html+ '<span style="color:#FF0000"> Out of Stock</span>'
                    html = html+'</p></td>'
                    html = html+'<td align="right">'
                    #html = html+'<p style="font-size:12px;color:#999;margin:0">AED&nbsp;'+str(cartdata["new_default_price_unit"])+'</p>'
                    html = html+'<p style="font-size:16px;color:#333">AED '+str(new_product_price)+'</p>'
                    html = html+'</td></tr></tbody> </table> </td> </tr>'
            #print(html)
            return html

# Order approval email to customer...
def email_send_by_AutoResponder(orderid=None, autoResponderId=None):
    link = ""
    buffer_data = getAutoResponder("","","","","","",autoResponderId)
    if buffer_data and buffer_data["content"]:
        autoResponderData  = buffer_data["content"]
        if autoResponderData["email_type"] == 'H':
            emailContent = autoResponderData["email_content"]
        else:
            emailContent = autoResponderData["email_content_text"]

        if orderid is not None:
            if autoResponderId == 30:
                order_id_str = str(orderid)
                order_id_str = order_id_str.encode("ascii")
                order_id_str = base64.b64encode(bytes(order_id_str))
                order_id_str = order_id_str.decode("ascii")

                link = "https://gogrocery.ae/substitute-product/" + order_id_str
            rs_order_products = EngageboostOrdermaster.objects.filter(id=orderid).first()
            if rs_order_products:
                orderid = rs_order_products.id
                cust_orderid = str(orderid)
                custom_order_id = rs_order_products.custom_order_id
                billing_name = rs_order_products.billing_name
                delivery_name = rs_order_products.delivery_name
                delivery_email = rs_order_products.delivery_email_address
                ordercustomer_id = rs_order_products.customer_id
                delivery_street_address = rs_order_products.delivery_street_address
                delivery_city = rs_order_products.delivery_city
                delivery_country = rs_order_products.delivery_country
                delivery_country_name = rs_order_products.delivery_country_name
                delivery_phone = rs_order_products.delivery_phone
                slot_start_time = rs_order_products.slot_start_time
                gross_amount = rs_order_products.gross_amount
                net_amount = rs_order_products.net_amount
                shipping_cost = rs_order_products.shipping_cost
                tax_amount = rs_order_products.tax_amount
                cart_discount = rs_order_products.cart_discount
                randomnum = '{:03d}'.format(random.randrange(1, 999))
                encoderandom = (randomnum + cust_orderid + randomnum)
                encodedBytes = base64.b64encode(encoderandom.encode("utf-8"))
                encodedStr = str(encodedBytes, "utf-8")
                # encodedStr = urlencode(encodedStr, quote_via=quote_plus)
                encodedStr = urllib.parse.quote(encodedStr)
                # dddd = urllib.parse.unquote(encodedStr)
                redeem_amount = rs_order_products.pay_wallet_amount
                payment_method_id = rs_order_products.payment_method_id
                payment_type_id = rs_order_products.payment_type_id
                # if (payment_method_id==16 and payment_type_id==4):
                if (payment_type_id==4):
                    email_subject = 'Pending'
                else:
                    email_subject = 'Successfull'
        email_subjectlower = email_subject.lower()
        subject = autoResponderData["subject"]
        subject = subject.replace('{@email_subject}',email_subject)

        emailContent = str(emailContent)
        emailContent = emailContent.replace('{@cust_orderid}',cust_orderid)
        emailContent = emailContent.replace('{@cust_orderidencode}',encodedStr)
        emailContent = emailContent.replace('{@name}',billing_name)
        emailContent = emailContent.replace('{@first_name}', billing_name)
        emailContent = emailContent.replace('{@custom_order_id}',custom_order_id)
        emailContent = emailContent.replace('{@link}', link)

        emailContent = emailContent.replace('{@delivery_name}',delivery_name)
        emailContent = emailContent.replace('{@delivery_street_address}',delivery_street_address)
        # emailContent = emailContent.replace('{@delivery_city}',delivery_city)
        emailContent = emailContent.replace('{@delivery_country}',delivery_country_name)
        emailContent = emailContent.replace('{@delivery_phone}',delivery_phone)
        emailContent = emailContent.replace('{@gross_amount}',str(gross_amount))
        # emailContent = emailContent.replace('{@gross_amount}',str(net_amount))
        emailContent = emailContent.replace('{@shipping_cost}',str(shipping_cost))
        emailContent = emailContent.replace('{@tax_amount}',str(tax_amount))
        emailContent = emailContent.replace('{@pay_wallet_amount}',str(redeem_amount))
        emailContent = emailContent.replace('{@discount_amount}',str(cart_discount))
        emailContent = emailContent.replace('{@net_amount}',str(net_amount))
        emailContent = emailContent.replace('{@slot_start_time}',str(slot_start_time))
        order_items = get_item_mail(orderid)
        emailContent = emailContent.replace('{@order_items}',str(order_items))
        emailContent = emailContent.replace('{@header_subject}',subject)
        emailContent = emailContent.replace('{@email_subjectlower}',email_subjectlower)
    if delivery_email:
        emailcomponent.OrderMail(delivery_email,autoResponderData["email_from"],subject,emailContent)
    if autoResponderId == 10:
        return encodedStr

# email_send_by_AutoResponder(1342,12)   

def saveloginhistory(user_id=None,ip_address=None,login_type='login'):
    now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
    if user_id:
        if login_type == 'login':
            login_data_save = {
                "user_id":user_id,
                "ip_address":ip_address,
                "in_time":now_utc
            }
            EngageboostUserLoginDetails.objects.create(**login_data_save)
        else:
            last_login_data = EngageboostUserLoginDetails.objects.filter(user_id=user_id).order_by('-id').first()
            if last_login_data:
                EngageboostUserLoginDetails.objects.filter(id=last_login_data.id).update(out_time=now_utc,ip_address=ip_address)
    return 1

def update_brand_slug():
    rs_brand = EngageboostBrandMasters.objects.filter(slug__isnull=True, isblocked='n', isdeleted='n')
    if rs_brand:
        for brand in rs_brand:
            name = brand.name.lower()
            name1 = name.replace(" ", "-")
            nametrns = name1.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~=+"})
            nametrns = slugify(nametrns)
            nametrns = CheckSlugExist(nametrns)
            EngageboostBrandMasters.objects.filter(id=brand.id).update(slug=nametrns)

def CheckSlugExist(str_slug=None):
    if str_slug is not None:
        rs_brand = EngageboostBrandMasters.objects.filter(slug__iexact=str_slug, isblocked='n', isdeleted='n')
        cnt = rs_brand.count()
        if cnt==0:
            # print("str_slug++++++++++", str_slug)
            return str_slug
        else:
            str_slug = str_slug+"1"
            # print("str_slug===", str_slug)

            str_slug = CheckSlugExist(str_slug)
            return str_slug

def addCustomerLoyaltypoints(order_id, customer_id, custom_order_id, pay_by_wallet ):
    now_utc     = datetime.datetime.now(datetime.timezone.utc).astimezone()
    valid_to = now_utc+ timedelta(days=60)
    rs_customer = EngageboostCustomers.objects.filter(id=customer_id).first()
    loyalty_balance = 0
    rs_loyalty = EngageboostCustomerLoyaltypoints.objects.filter(customer_id=customer_id).last()
    if rs_loyalty:
        rs_loyalty = rs_loyalty.remaining_balance
    loyaltypoints_obj = {
        "website_id": 1,
        "rule_id": 77,
        "customer_id": rs_customer.auth_user_id,
        "order_id": order_id,
        "custom_order_id": custom_order_id,
        "description": 'Received from Order return.',
        "received_points": int(pay_by_wallet),
        "burnt_points": 0.00,
        "amount": int(pay_by_wallet),
        "received_burnt": 0.00,
        "status": "earn",
        "created": now_utc,
        "valid_form": now_utc,
        "expiry_date": valid_to,
        "remaining_balance":int(loyalty_balance)+int(pay_by_wallet),
        # "processing_status": 'complete'
    }
    EngageboostCustomerLoyaltypoints.objects.create(**loyaltypoints_obj)
    return 1

# @postpone
# def update_bulk_elastic(table_name,item_ids=[]):
# 	try:
# 		model=apps.get_model('webservices',table_name)
# 		serializer_class = get_serializer_class_elastic(table_name)
# 		datas = []
# 		docs = []
# 		prod_obj = model.objects.filter(isdeleted='n')
# 		if len(item_ids)>0:
# 			prod_obj = prod_obj.filter(id__in=item_ids)
# 		if prod_obj.count()>0:
# 			products = prod_obj.order_by("-id").all().iterator()
# 			# common.check_mapping_elastic(table_name)
# 			for item in products:
# 				# save_data_to_elastic(item.id,table_name)
# 				serializer = serializer_class(item,partial=True)
# 				data = serializer.data
# 				# print("Data Formatting Start=====",datetime.now())
# 				data = format_serialized_data(table_name,data)
# 				# print("Data Formatting Complete=====",datetime.now())
# 				cm_id= data["id"]
# 				website_id = data["website_id"]
# 				module_name = get_index_name_elastic(cm_id,table_name)
# 				header = {
# 					"_index": module_name,
# 					"_type": "data",
# 					"_id": cm_id,
# 					"_source": data
# 				}
# 				docs.append(header)
# 			obj = helpers.bulk(es,docs)
# 			datas.append({"msg":"Success","item_ids":item_ids})
# 			# print("After All=====",datetime.now())
# 			print(datas)
# 	except Exception as error:
# 		trace_back = sys.exc_info()[2]
# 		line = trace_back.tb_lineno
# 		datas = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
# 		print("Elastic Error ==========",datas)	
# 	return datas	

def SendSms(message,mobile_no):
    settings_data = GlobalSettings(1)
    # url = "https://apiw.me.synapselive.com/push.aspx"
    url = "http://apiw.me.synapselive.com/push.aspx"
    username 	= "ONBOARDEXP"
    password 	= "onboa@12"
    senderid 	= "GoGrocery"
    if settings_data:
        username 	= settings_data["sms_auth_key"]
        password 	= "onboa@12" # settings_data["sms_route"]
        senderid 	= settings_data["sms_sender_id"]

    if message is not None and message!="":
        if mobile_no is not None and mobile_no!="":
            try:
                # check Mobile country code
                mobile_no  = str(mobile_no)
                mobile_no = mobile_no.replace("+", "")
                str_co = str(mobile_no)[:3]
                if str_co == '971':
                    pass
                else:
                    mobile_no = "971"+mobile_no

                data = {'user':username,
                        'pass':password,
                        'senderid':senderid,
                        'lang':'0',
                        'mobile':mobile_no,
                        'message':message
                    }
                print("data====", data)
                r = requests.get(url = url, params = data)
                url_response = r.text
                data = {
                    "status":1,
                    "response":url_response
                }
                sms_insert_arr = {
                    "mobile_number":mobile_no,
                    "sms_content_text":message,
                    "response_text":url_response,
                    "created":datetime.datetime.now(datetime.timezone.utc)
                }
                EngageboostSmsLog.objects.create(**sms_insert_arr)

            except Exception as error:
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        else:
            data = {
            "status":0,
            "msg":"Message should not be blank."
        }
    else:
        data = {
            "status":0,
            "msg":"Message should not be blank."
        }
    print("sms===", data)
    return data

# @postpone
def sms_send_by_AutoResponder(orderid, shipment_status=None, autoResponderId=None, str_link = None):
    order_data = EngageboostOrdermaster.objects.filter(id=orderid).first()
    if shipment_status:
        buffer_data = getAutoResponder(None,shipment_status,order_data.webshop_id,order_data.assign_wh,order_data.shipping_method_id,order_data.website_id,autoResponderId)
    else:
        buffer_data = getAutoResponder("","","","","","",autoResponderId)

    if buffer_data and buffer_data["content"]:
        autoResponderData  = buffer_data["content"]
        sms_content = str(autoResponderData["sms_content_text"])
        # str_sms = sms_content.replace('{@custom_order_id}',custom_order_id)
        # common_functions.SendSms(str_sms,customerdetails["billing_phone"])
        rs_order_data = OrderShipmentViewSerializer(order_data).data
        if rs_order_data:
            # print("jgjj", json.dumps(rs_order_data))
            for i in rs_order_data:
                key = i
                val = rs_order_data[i]
                sms_content = sms_content.replace('{@'+str(key)+'}', str(val))
            if str_link is not None:
                sms_content = sms_content.replace('{@cust_orderidencode}',str_link)

            print("sms_content===", sms_content)
            SendSms(sms_content,rs_order_data['billing_phone'])


def get_category_hierarchy(product_id,field):
    catdict=[];
    all_categories = EngageboostProductCategories.objects.filter(product_id=product_id,category_id__isdeleted='n',category_id__isblocked='n')
    if all_categories.count()>0:
        product_arr = all_categories.all()
        product_arr = ProductCategoriesSerializer_elastic(product_arr,many=True)
        for cat in product_arr.data:
            # print(cat)
            if(cat["category"]['parent_id']!=0):
                objCategorychild1 = EngageboostCategoryMasters.objects.filter(id=cat["category"]['parent_id'],isdeleted='n',isblocked='n')

                if objCategorychild1.count()>0:
                    objCategorychild1 = objCategorychild1.values().first()
                    if(objCategorychild1['parent_id']!=0):
                        objCategorychild2 = EngageboostCategoryMasters.objects.filter(id=objCategorychild1.parent_id,isdeleted='n',isblocked='n')

                        if objCategorychild2.count()>0:
                            objCategorychild2=objCategorychild2.values().first()
                            if(objCategorychild2['parent_id']!=0):
                                objCategorychild3 = EngageboostCategoryMasters.objects.filter(id=objCategorychild2.parent_id,isdeleted='n',isblocked='n')

                                if objCategorychild3.count()>0:
                                    objCategorychild3 = objCategorychild3.values().first()
                                    if(objCategorychild3['parent_id']!=0):
                                        catdict.append(objCategorychild3[field])
                                        catdict.append(objCategorychild2[field])
                                        catdict.append(objCategorychild1[field])
                                        catdict.append(cat["category"][field])
                                    else:
                                        catdict.append(objCategorychild2[field])
                                        catdict.append(objCategorychild1[field])
                                        catdict.append(cat["category"][field])
                            else:
                                catdict.append(objCategorychild2[field])
                                catdict.append(objCategorychild1[field])
                                catdict.append(cat["category"][field])
                    else:
                        catdict.append(objCategorychild1[field])
                        catdict.append(cat["category"][field])
            else:
                catdict.append(cat["category"][field])
    # catdict = list(set(catdict))
    return catdict

def get_brand(product_id,field_name=None):
    brandarr=[];
    product_obj = EngageboostProducts.objects.filter(id=product_id,isdeleted='n',isblocked='n')
    if product_obj.count()>0:
        product_obj = product_obj.first()
        brand_id = product_obj.brand
        if brand_id:
            brands=brand_id.split(",")
            if field_name=='name':
                for bid in brands:
                    if bid:
                        fetch_brand=EngageboostBrandMasters.objects.filter(id=bid,isdeleted='n',isblocked='n')
                        if fetch_brand.count()>0:
                            fetch_brand = fetch_brand.first()
                            brandarr.append(fetch_brand.name)
                brand=','.join([str(i) for i in brandarr])
                brands_name=brand
            elif field_name == 'id':
                for bid in brands:
                    if bid:
                        fetch_brand=EngageboostBrandMasters.objects.filter(id=bid,isdeleted='n',isblocked='n')
                        if fetch_brand.count()>0:
                            fetch_brand = fetch_brand.first()
                            brandarr.append(fetch_brand.id)
                brands_id=brandarr
            elif field_name == 'slug':
                for bid in brands:
                    if bid:
                        fetch_brand=EngageboostBrandMasters.objects.filter(id=bid,isdeleted='n',isblocked='n')
                        if fetch_brand.count()>0:
                            fetch_brand = fetch_brand.first()
                            brand_slug = fetch_brand.slug
        else:
            brands_name=''
            brands_id = []
            brand_slug = ''
    else:
        brands_name=''
        brands_id = []
        brand_slug = ''
    if field_name=='name':
        return brands_name
    elif field_name == 'id':
        return brands_id
    elif field_name == 'slug':
        return brand_slug

def get_unit(product_id):
    print("================",product_id)
    product_obj = EngageboostProducts.objects.filter(id=product_id)
    if product_obj.count()>0:
        product_obj = product_obj.first()
        UOM = product_obj.uom
        if UOM is not None:
            obj = EngageboostUnitMasters.objects.filter(isblocked='n', isdeleted='n')
            if UOM.isnumeric()==True:
                print("=====================",UOM)
                rs_uom = obj.filter(id=int(UOM)).first()
            else:
                rs_uom = obj.filter(unit_name=UOM).first()
            if rs_uom:
                return rs_uom.unit_name
            else:
                return ''
        else:
            return ''
    else:
        return ''

@postpone
def related_products_to_elastic(table_name,data_id,prev_products=[]):
    try:
        if table_name == 'EngageboostDiscountMasters':
            final = []
            objproduct_list = EngageboostDiscountMastersConditions.objects.filter(discount_master_id = data_id).values_list('all_product_id',flat=True)
            if(prev_products):
                objproduct_list = list(objproduct_list)

                # -------Binayak Start 17-03-2021-------#
                for single_obj in objproduct_list:
                    new = single_obj.split(',')
                    final.extend(new)

                final.extend(prev_products)
                final = list(set(final))

                # objproduct_list.extend(prev_products)
                # objproduct_list = list(set(objproduct_list))

            # if objproduct_list :
            if final:
                elastic = update_bulk_elastic('EngageboostProducts', final, 'channel_currency_product_price',
                                              'update')
                # for elastic_product_id in objproduct_list:
                # 	if(elastic_product_id is not None):
                # 		try:
                # 			if("," in elastic_product_id):
                # 				prod_lst = elastic_product_id.split(",")
                # 				elastic = update_bulk_elastic('EngageboostProducts',prod_lst,'channel_currency_product_price','update')
                # 			else:
                # 				elastic = update_bulk_elastic('EngageboostProducts',[int(elastic_product_id)],'channel_currency_product_price','update')
                # 		except:
                # 			elastic = update_bulk_elastic('EngageboostProducts',[int(elastic_product_id)],'channel_currency_product_price','update')

                # -------Binayak Start 17-03-2021-------#

        elif table_name == 'EngageboostCategoryMasters':
            objproduct_list = EngageboostProductCategories.objects.filter(category_id = data_id).values_list('product_id',flat=True)
            if objproduct_list :
                elastic = update_bulk_elastic('EngageboostProducts',objproduct_list,'category_id','update')
                elastic = update_bulk_elastic('EngageboostProducts',objproduct_list,'category','update')
                elastic = update_bulk_elastic('EngageboostProducts',objproduct_list,'category_slug','update')


        elif table_name == 'EngageboostBrandMasters':
            objproduct_list = EngageboostProducts.objects.filter(brand = data_id).values_list('id',flat=True)
            if objproduct_list :
                elastic = update_bulk_elastic('EngageboostProducts',objproduct_list,'brand','update')
                elastic = update_bulk_elastic('EngageboostProducts',objproduct_list,'brand_id','update')
                elastic = update_bulk_elastic('EngageboostProducts',objproduct_list,'brand_slug','update')

        elif table_name == 'EngageboostProductTaxClasses':
            objproduct_list = EngageboostProducts.objects.filter(Q(taxclass_id = data_id)|Q(po_taxclass_id = data_id)).values_list('id',flat=True)
            if objproduct_list :
                elastic = update_bulk_elastic('EngageboostProducts',objproduct_list,'taxclass','update')
                elastic = update_bulk_elastic('EngageboostProducts',objproduct_list,'po_taxclass','update')

        elif table_name == 'EngageboostSuppliers':
            objproduct_list = EngageboostProducts.objects.filter(supplier_id = data_id).values_list('id',flat=True)
            if objproduct_list :
                elastic = update_bulk_elastic('EngageboostProducts',objproduct_list,'supplier','update')

        elif table_name == 'EngageboostUnitMasters':
            objproduct_list = EngageboostProducts.objects.filter(uom = data_id).values_list('id',flat=True)
            if objproduct_list :
                elastic = update_bulk_elastic('EngageboostProducts',objproduct_list,'unit','update')

    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        datas = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        print("Elastic Error ==========",datas)
    return 1

# def update_bulk_elastic(table_name,item_ids=[],field_name=None,action='index'):
# 	try:
# 		es = Elasticsearch([{'host': settings.ELASTIC_HOST, 'port': settings.ELASTIC_PORT}])
# 		model=apps.get_model('webservices',table_name)
# 		# serializer_class = get_serializer_class_elastic(table_name)

# 		datas = []
# 		docs = []

# 		prod_obj = model.objects.filter(isdeleted='n')

# 		if len(item_ids)>0:
# 			prod_obj = prod_obj.filter(id__in=item_ids)		

# 		if prod_obj.count()>0:			
# 			products = prod_obj.order_by("-id").values().all().iterator()

# 			# common.check_mapping_elastic(table_name)

# 			for item in products:
# 				data = get_product_field_value_for_elastic(item['id'], field_name)

# 				cm_id= item["id"]
# 				website_id = item["website_id"]

# 				module_name = get_index_name_elastic(cm_id,table_name)

# 				header = {
# 					"_op_type": action,
# 					"_index": module_name,
# 					"_type": "data",
# 					"_id": cm_id,
# 					"doc": data
# 				}
# 				docs.append(header)
# 			print("Updated products==========",docs)
# 			obj = helpers.bulk(es,docs)
# 			datas.append({"msg":"Success","item_ids":item_ids})
# 			# print("After All=====",datetime.now())	
# 			print(datas)
# 	except Exception as error:
# 		trace_back = sys.exc_info()[2]
# 		line = trace_back.tb_lineno
# 		datas = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
# 		print("Elastic Error ==========",datas)	
# 	return datas

def update_bulk_elastic_old(table_name,item_ids=[],field_name=None,action='index', warehouse=None):
    try:
        es = Elasticsearch([{'host': settings.ELASTIC_HOST, 'port': settings.ELASTIC_PORT}])
        model=apps.get_model('webservices',table_name)


        datas = []
        docs = []

        prod_obj = model.objects.filter(isdeleted='n')

        if len(item_ids)>0:
            prod_obj = prod_obj.filter(id__in=item_ids)

        if prod_obj.count()>0:
            products = prod_obj.order_by("-id").all().iterator()

            # common.check_mapping_elastic(table_name)

            for item in products:

                cm_id= item.id
                website_id = item.website_id

                module_name = get_index_name_elastic(cm_id,table_name)

                exists = es.exists(index=module_name, id=cm_id, doc_type="data")

                if exists:
                    data = get_product_field_value_for_elastic(item.id, field_name)


                    header = {
                        "_op_type": 'update',
                        "_index": module_name,
                        "_type": "data",
                        "_id": cm_id,
                        "doc": data
                    }
                else:
                    serializer_class = get_serializer_class_elastic(table_name)
                    serializer = serializer_class(item,partial=True)
                    data = serializer.data
                    # print("Data Formatting Start=====",datetime.now())
                    # data = common.setUpLangDataToSerializer(data)
                    data = format_serialized_data(table_name,data)

                    header = {
                        "_index": module_name,
                        "_type": "data",
                        "_id": cm_id,
                        "_source": data
                    }
                docs.append(header)
            print("Updated products==========",docs)
            obj = helpers.bulk(es,docs)
            datas.append({"msg":"Success","item_ids":item_ids})
            # print("After All=====",datetime.now())
            print(datas)
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        datas = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        print("Elastic Error ==========",datas)
    return datas

@postpone
def update_bulk_elastic(table_name,item_ids=[],field_name=None,action='index', warehouse=None):
    es = Elasticsearch([{'host': settings.ELASTIC_HOST, 'port': settings.ELASTIC_PORT}])

    datas = []
    docs = []
    tempId = []

    response = emailcomponent.testmail('binayak.santra@navsoft.in', "Data Preparation Start update_bulk_elastic__LIVE",
                                       'Data preparation process start' + str(datetime.datetime.now()))
    # table_name = 'EngageboostProducts'
    # field_name = 'channel_currency_product_price'
    # item_ids = EngageboostProducts.objects.filter(isblocked='n', isdeleted='n').values_list('id', flat=True)[
    #            0:10000]

    # print('item_ids=======>', item_ids)
    # item_ids = item_ids_get.values_list('id', flat=True)
    action = 'update'

    model = apps.get_model('webservices', table_name)
    prod_obj = model.objects.filter(isdeleted='n')

    n = 500
    # using list comprehension
    chunked_products = [item_ids[i * n:(i + 1) * n] for i in range((len(item_ids) + n - 1) // n)]

    for chunk in chunked_products:
        datas = []
        docs = []
        tempId = []

        try:
            if len(chunk) > 0:
                prod_obj_1 = prod_obj.filter(id__in=chunk)

            if prod_obj_1.count() > 0:
                products = prod_obj_1.order_by("-id")
                # products = prod_obj_1.order_by("-id").all().iterator()

                new_cm_id = prod_obj_1.values_list('id', flat=True)
                module_name = get_index_name_elastic(new_cm_id[0], table_name)

                data_string = []
                if field_name:
                    for id in new_cm_id:
                        id_string = {
                            "_id": id,
                            "_source": {
                               "include": [ field_name ]
                            }
                        }
                        data_string.append(id_string)
                else:
                    for id in new_cm_id:
                        id_string = {
                            "_id": id,
                            "_source": False
                        }
                        data_string.append(id_string)
                print("=====data_string=====", data_string)
                prod_exists = es.mget(body=json.dumps({"docs": data_string}), index=module_name, doc_type="data")
                for item in prod_exists['docs']:
                    cm_id = item['_id']
                    warehouse_id = None

                    if item['found'] == True:
                        # print("======item======", item)
                        #-------Binayak Start 11-03-2021-------#
                        if field_name == 'channel_currency_product_price' and warehouse != None:
                            price_data = item['_source']['channel_currency_product_price']

                            # -------Binayak Start 17-03-2021------#
                            warehouse_list = warehouse.copy()
                            modified_price_data = multiple_warehouse_channel_currency_price_update_string(cm_id, price_data,warehouse_list)

                            data = {"channel_currency_product_price": modified_price_data}

                            # -------Binayak Start 17-03-2021------#

                            # for channel_currency_product_price in price_data:
                            #
                            #     # flag = 0
                            #     if channel_currency_product_price['warehouse_id'] in warehouse:
                            #         warehouse_id = channel_currency_product_price['warehouse_id']
                            #         # print("======warehouse_id=======", warehouse_id, cm_id)
                            #         price_data_single = get_channel_currency_product_price(cm_id, 1, [warehouse_id])
                            #         # print("=====price_data_single=====", price_data_single)
                            #
                            #         for data_single in price_data_single:
                            #             channel_currency_product_price['id'] = data_single['id']
                            #             channel_currency_product_price['promotions'] = data_single['promotions']
                            #             channel_currency_product_price['price_type'] = data_single['price_type']
                            #             channel_currency_product_price['channel_id'] = data_single['channel_id']
                            #             channel_currency_product_price['currency_id'] = data_single['currency_id']
                            #             channel_currency_product_price['price'] = data_single['price']
                            #             channel_currency_product_price['cost'] = data_single['cost']
                            #             channel_currency_product_price['mrp'] = data_single['mrp']
                            #             channel_currency_product_price['min_quantity'] = data_single['min_quantity']
                            #             channel_currency_product_price['max_quantity'] = data_single['max_quantity']
                            #             channel_currency_product_price['warehouse_id'] = data_single['warehouse_id']
                            #             channel_currency_product_price['website_id'] = data_single['website_id']
                            #             channel_currency_product_price['start_date'] = data_single['start_date']
                            #             channel_currency_product_price['end_date'] = data_single['end_date']
                            #             channel_currency_product_price['product'] = data_single['product']
                            #             channel_currency_product_price['product_price_type'] = data_single['product_price_type']
                            #             channel_currency_product_price['new_default_price'] = data_single['new_default_price']
                            #             channel_currency_product_price['new_default_price_unit'] = data_single['new_default_price_unit']
                            #             channel_currency_product_price['discount_price_unit'] = data_single['discount_price_unit']
                            #             channel_currency_product_price['discount_price'] = data_single['discount_price']
                            #             channel_currency_product_price['discount_amount'] = data_single['discount_amount']
                            #             channel_currency_product_price['disc_type'] = data_single['disc_type']
                            #             channel_currency_product_price['coupon'] = data_single['coupon']
                            #
                            #         # flag = 1

                            # if flag == 0:
                            #     # print("I am here")
                            #     price_data_single = get_channel_currency_product_price(cm_id, None, [warehouse_id])
                            #     # price_data_single = json.dumps(price_data_single)
                            #     # price_data_single = json.loads(price_data_single)
                            #     print("======price_data_single======", price_data_single)
                            #     # price_data = common.get_channel_currency_product_price(cm_id)
                            #     price_data.append(price_data_single[0])
                            # data = {field_name:price_data}
                        else:
                            data = get_product_field_value_for_elastic(cm_id, field_name)
                        #------Binayak End 11-03-2021------#
                        header = {
                            "_op_type": 'update',
                            "_index": module_name,
                            "_type": "data",
                            "_id": cm_id,
                            "doc": data
                        }
                        tempId.append(cm_id)
                    else:
                        now_item = products.filter(id=cm_id)
                        serializer_class = get_serializer_class_elastic(table_name)
                        serializer = serializer_class(now_item, partial=True)
                        data = serializer.data

                        data = format_serialized_data(table_name, data)

                        header = {
                            "_index": module_name,
                            "_type": "data",
                            "_id": cm_id,
                            "_source": data
                        }
                        tempId.append(cm_id)
                    docs.append(header)
                    # print("====docs====", docs)
                # response = emailcomponent.testmail('binayak.santra@navsoft.in', "Data Prepared",
                #                                    'Data preparation completed, initiating elastic push' + str(
                #                                        datetime.datetime.now()))
                # print("Updated products==========",docs)
                # obj = helpers.bulk(es, docs)
                # response = emailcomponent.testmail('binayak.santra@navsoft.in', "Data Pushed to Elastic",
                #                                    'Data updating to elastic completed' + str(datetime.datetime.now()))
                # datas.append({"msg": "Success", "item_ids": item_ids})
                # print("After All=====",datetime.now())
                # print(datas)
                # return Response(datas)
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            datas.append({"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),
                     "message": str(error)})
            print("Elastic Error ==========", datas)

        finally:
            obj = helpers.bulk(es, docs)

            datas.append({"msg": "Success", "item_ids": chunk})
            datas.append({"data": obj})
            response = emailcomponent.testmail('binayak.santra@navsoft.in', "Data Pushed to Elastic_update_bulk_elastic_LIVE",
                                               'Data updating to elastic completed' + str(datetime.datetime.now()) + ' <=====data=====> ' + str(datas) + ' <<======updated products list=======>> ' + str(tempId))
            print("Elastic Success ==========", datas)

#-------Binayak Start 27-04-2021-------#
def update_bulk_elastic_now_process(table_name,item_ids=[],field_name=None,action='index', warehouse=None):
    es = Elasticsearch([{'host': settings.ELASTIC_HOST, 'port': settings.ELASTIC_PORT}])

    tempDataId = []
    datas = []
    docs = []

    try:
        response = emailcomponent.testmail('binayak.santra@navsoft.in', "Data Prepared",
                                           'Data preparation process start' + str(datetime.datetime.now()))
        # table_name = 'EngageboostProducts'
        # field_name = 'channel_currency_product_price'
        # item_ids = EngageboostProducts.objects.filter(isblocked='n', isdeleted='n').values_list('id', flat=True)[
        #            0:10000]

        # print('item_ids=======>', item_ids)
        # item_ids = item_ids_get.values_list('id', flat=True)
        action = 'update'


        model = apps.get_model('webservices', table_name)

        prod_obj = model.objects.filter(isdeleted='n')

        if len(item_ids) > 0:
            prod_obj = prod_obj.filter(id__in=item_ids)

        if prod_obj.count() > 0:
            products = prod_obj.order_by("-id")
            # products = prod_obj.order_by("-id").all().iterator()

            new_cm_id = prod_obj.values_list('id', flat=True)
            module_name = get_index_name_elastic(new_cm_id[0], table_name)

            data_string = []
            if field_name:
                for id in new_cm_id:
                    id_string = {
                        "_id": id,
                        "_source": {
                           "include": [ field_name ]
                        }
                    }
                    data_string.append(id_string)
            else:
                for id in new_cm_id:
                    id_string = {
                        "_id": id,
                        "_source": False
                    }
                    data_string.append(id_string)
            # print("=====data_string=====", data_string)
            prod_exists = es.mget(body=json.dumps({"docs": data_string}), index=module_name, doc_type="data")
            for item in prod_exists['docs']:
                cm_id = item['_id']
                warehouse_id = None

                if item['found'] == True:
                    # print("======item======", item)
                    #-------Binayak Start 11-03-2021-------#
                    if field_name == 'channel_currency_product_price' and warehouse != None:
                        price_data = item['_source']['channel_currency_product_price']

                        #-------Binayak Start 17-03-2021------#
                        warehouse_list = warehouse.copy()
                        modified_price_data = multiple_warehouse_channel_currency_price_update_string(cm_id, price_data,
                                                                                                      warehouse_list)
                        data = {"channel_currency_product_price": modified_price_data}
                        print("=====data=====", data)
                        # -------Binayak Start 17-03-2021------#

                        # for channel_currency_product_price in price_data:
                        #
                        #     # flag = 0
                        #     if channel_currency_product_price['warehouse_id'] in warehouse:
                        #         warehouse_id = channel_currency_product_price['warehouse_id']
                        #         # print("======warehouse_id=======", warehouse_id, cm_id)
                        #         price_data_single = get_channel_currency_product_price(cm_id, 1, [warehouse_id])
                        #         # print("=====price_data_single=====", price_data_single)
                        #
                        #         for data_single in price_data_single:
                        #             channel_currency_product_price['id'] = data_single['id']
                        #             channel_currency_product_price['promotions'] = data_single['promotions']
                        #             channel_currency_product_price['price_type'] = data_single['price_type']
                        #             channel_currency_product_price['channel_id'] = data_single['channel_id']
                        #             channel_currency_product_price['currency_id'] = data_single['currency_id']
                        #             channel_currency_product_price['price'] = data_single['price']
                        #             channel_currency_product_price['cost'] = data_single['cost']
                        #             channel_currency_product_price['mrp'] = data_single['mrp']
                        #             channel_currency_product_price['min_quantity'] = data_single['min_quantity']
                        #             channel_currency_product_price['max_quantity'] = data_single['max_quantity']
                        #             channel_currency_product_price['warehouse_id'] = data_single['warehouse_id']
                        #             channel_currency_product_price['website_id'] = data_single['website_id']
                        #             channel_currency_product_price['start_date'] = data_single['start_date']
                        #             channel_currency_product_price['end_date'] = data_single['end_date']
                        #             channel_currency_product_price['product'] = data_single['product']
                        #             channel_currency_product_price['product_price_type'] = data_single['product_price_type']
                        #             channel_currency_product_price['new_default_price'] = data_single['new_default_price']
                        #             channel_currency_product_price['new_default_price_unit'] = data_single['new_default_price_unit']
                        #             channel_currency_product_price['discount_price_unit'] = data_single['discount_price_unit']
                        #             channel_currency_product_price['discount_price'] = data_single['discount_price']
                        #             channel_currency_product_price['discount_amount'] = data_single['discount_amount']
                        #             channel_currency_product_price['disc_type'] = data_single['disc_type']
                        #             channel_currency_product_price['coupon'] = data_single['coupon']
                        #
                        #         # flag = 1

                        # if flag == 0:
                        #     # print("I am here")
                        #     price_data_single = get_channel_currency_product_price(cm_id, None, [warehouse_id])
                        #     # price_data_single = json.dumps(price_data_single)
                        #     # price_data_single = json.loads(price_data_single)
                        #     print("======price_data_single======", price_data_single)
                        #     # price_data = common.get_channel_currency_product_price(cm_id)
                        #     price_data.append(price_data_single[0])
                        # data = {field_name:price_data}
                    else:
                        data = get_product_field_value_for_elastic(cm_id, field_name)
                    #------Binayak End 11-03-2021------#
                    header = {
                        "_op_type": 'update',
                        "_index": module_name,
                        "_type": "data",
                        "_id": cm_id,
                        "doc": data
                    }
                else:
                    now_item = products.filter(id=cm_id).first()
                    serializer_class = get_serializer_class_elastic(table_name)
                    serializer = serializer_class(now_item, partial=True)
                    data = serializer.data

                    data = format_serialized_data(table_name, data)

                    header = {
                        "_index": module_name,
                        "_type": "data",
                        "_id": cm_id,
                        "_source": data
                    }
                docs.append(header)
                tempDataId.append(cm_id)
                # print("====docs====", docs)
            response = emailcomponent.testmail('binayak.santra@navsoft.in', "Data Prepared",
                                               'Data preparation completed, initiating elastic push' + str(
                                                   datetime.datetime.now()))
            # print("Updated products==========",docs)
            # obj = helpers.bulk(es, docs)
            # response = emailcomponent.testmail('binayak.santra@navsoft.in', "Data Pushed to Elastic",
            #                                    'Data updating to elastic completed' + str(datetime.datetime.now()))
            # datas.append({"msg": "Success", "item_ids": item_ids})
            # print("After All=====",datetime.now())
            # print(datas)
            # return Response(datas)
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        datas.append({"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),
                 "message": str(error)})
        print("Elastic Error ==========", datas)

    finally:
        obj = helpers.bulk(es, docs)
        response = emailcomponent.testmail('binayak.santra@navsoft.in', "Data Pushed to Elastic",
                                           'Data updating to elastic completed' + str(datetime.datetime.now()))
        datas.append({"msg": "Success", "item_ids": item_ids})
        print("Elastic Success ==========", datas)
        return tempDataId
#-------Binayak End 27-04-2021-------#


@postpone
def products_to_elastic(product_ids):
    es = connect_elastic()
    table_name = 'EngageboostProducts'

    # print("======threading.active_count()=======", active_schedulers())

    datas = []
    docs = []
    current_product_chunk = []
    processed_product_chunk = []

    total_len_count = len(product_ids)

    if total_len_count > 0:

        index_name = get_index_name_elastic(product_ids[0], table_name)
        check_mapping_elastic(table_name, index_name)

        chunk_size = 500
        fragment_size, remainder = divmod(total_len_count, chunk_size)
        print("fragment_size====", fragment_size, remainder)
        if int(remainder) > 0:
            fragment_size += 1
        for i in range(fragment_size):
            docs = []
            datas = []
            data_string = []
            current_product_chunk = []
            processed_product_chunk = []
            try:

                # datas = []
                start_pos = i * chunk_size
                end_pos = (i + 1) * chunk_size

                if i == fragment_size - 1:
                    end_pos = start_pos + remainder

                print("======start_pos======", start_pos)
                print("======end_pos======", end_pos)
                current_product_chunk.extend(product_ids[start_pos:end_pos])

                for prod_id in current_product_chunk:
                    # for id in product_ids:
                    id_string = {
                        "_id": prod_id,
                        "_source": False
                    }
                    data_string.append(id_string)
                # print("======data_string======", data_string)
                prod_exists = es.mget(body=json.dumps({"docs": data_string}), index=index_name, doc_type="data")

                # docs = []
                for item in prod_exists['docs']:
                    cm_id = item['_id']
                    elastic_data_string = save_data_to_elastic_single_data_generate_for_bulk(cm_id, table_name)
                    if item['found'] == True:

                        header = {
                            "_op_type": 'update',
                            "_index": index_name,
                            "_type": "data",
                            "_id": cm_id,
                            "doc": elastic_data_string
                        }
                        docs.append(header)
                        processed_product_chunk.append(cm_id)
                    else:

                        header = {
                            "_index": index_name,
                            "_type": "data",
                            "_id": cm_id,
                            "_source": elastic_data_string
                        }
                        docs.append(header)
                        processed_product_chunk.append(cm_id)


                # datas.append({"obj": obj})
                # response = emailcomponent.testmail('binayak.santra@navsoft.in',
                #                                    "Product Pushed to Elastic @@@SaveAllImportedDataTest@@@",
                #                                    'Data preparation Completed and Pushed to Elastic, PRODUCT_COUNT =====>' + str(
                #                                        len(product_ids)) + ' @ ' + str(
                #                                        datetime.datetime.now()) + ' datas=====> ' + str(obj))
                print("======channel price data ended=======")
            except Exception as error:
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                datas.append({"status": 0, "api_status": traceback.format_exc(), "error_line": line,
                              "error_message": str(error),
                              "message": str(error)})
            finally:
                # print("==========docs===========", docs)

                obj = helpers.bulk(es, docs)
                sku_list = EngageboostProducts.objects.filter(id__in=product_ids).values_list('sku', flat=True)
                EngageboostTempProducts.objects.filter(sku__in=sku_list, is_import='y').delete()

                datas.append({"obj": obj})
                response = emailcomponent.testmail('binayak.santra@navsoft.in',
                                                   "Product sync @@@products_to_elasticLive@@@",
                                                   'Data preparation Completed and Pushed to Elastic,' + ' @ ' + str(
                                                       datetime.datetime.now()) + ' datas=====>' + str(datas) +
                                                   '=====processed_product_chunk======' + str(len(processed_product_chunk)) +
                                                   '=====current_product_chunk======' + str(len(current_product_chunk)))
                                                   # '=====current_product_chunk======' + str(len(current_product_chunk)) + '=======threads========' + str(threading.active_count()))

def products_to_elastic_cron(product_ids):
    es = connect_elastic()
    table_name = 'EngageboostProducts'

    # print("======threading.active_count()=======", active_schedulers())

    datas = []
    docs = []
    current_product_chunk = []
    processed_product_chunk = []

    total_len_count = len(product_ids)

    if total_len_count > 0:

        index_name = get_index_name_elastic(product_ids[0], table_name)
        check_mapping_elastic(table_name, index_name)

        chunk_size = 500
        fragment_size, remainder = divmod(total_len_count, chunk_size)
        print("fragment_size====", fragment_size, remainder)
        if int(remainder) > 0:
            fragment_size += 1
        for i in range(fragment_size):
            docs = []
            datas = []
            data_string = []
            current_product_chunk = []
            processed_product_chunk = []
            try:

                # datas = []
                start_pos = i * chunk_size
                end_pos = (i + 1) * chunk_size

                if i == fragment_size - 1:
                    end_pos = start_pos + remainder

                print("======start_pos======", start_pos)
                print("======end_pos======", end_pos)
                current_product_chunk.extend(product_ids[start_pos:end_pos])

                for prod_id in current_product_chunk:
                    # for id in product_ids:
                    id_string = {
                        "_id": prod_id,
                        "_source": False
                    }
                    data_string.append(id_string)
                # print("======data_string======", data_string)
                prod_exists = es.mget(body=json.dumps({"docs": data_string}), index=index_name, doc_type="data")

                # docs = []
                for item in prod_exists['docs']:
                    cm_id = item['_id']
                    elastic_data_string = save_data_to_elastic_single_data_generate_for_bulk(cm_id, table_name)
                    if item['found'] == True:

                        header = {
                            "_op_type": 'update',
                            "_index": index_name,
                            "_type": "data",
                            "_id": cm_id,
                            "doc": elastic_data_string
                        }
                        docs.append(header)
                        processed_product_chunk.append(cm_id)
                    else:

                        header = {
                            "_index": index_name,
                            "_type": "data",
                            "_id": cm_id,
                            "_source": elastic_data_string
                        }
                        docs.append(header)
                        processed_product_chunk.append(cm_id)


                # datas.append({"obj": obj})
                # response = emailcomponent.testmail('binayak.santra@navsoft.in',
                #                                    "Product Pushed to Elastic @@@SaveAllImportedDataTest@@@",
                #                                    'Data preparation Completed and Pushed to Elastic, PRODUCT_COUNT =====>' + str(
                #                                        len(product_ids)) + ' @ ' + str(
                #                                        datetime.datetime.now()) + ' datas=====> ' + str(obj))
                print("======channel price data ended=======")
            except Exception as error:
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                datas.append({"status": 0, "api_status": traceback.format_exc(), "error_line": line,
                              "error_message": str(error),
                              "message": str(error)})
            finally:
                # print("==========docs===========", docs)

                obj = helpers.bulk(es, docs)
                sku_list = EngageboostProducts.objects.filter(id__in=product_ids).values_list('sku', flat=True)
                EngageboostTempProducts.objects.filter(sku__in=sku_list, is_import='y').delete()

                datas.append({"obj": obj})
                response = emailcomponent.testmail('binayak.santra@navsoft.in',
                                                   "Product sync @@@products_to_elasticLive@@@",
                                                   'Data preparation Completed and Pushed to Elastic,' + ' @ ' + str(
                                                       datetime.datetime.now()) + ' datas=====>' + str(datas) +
                                                   '=====processed_product_chunk======' + str(len(processed_product_chunk)) +
                                                   '=====current_product_chunk======' + str(len(current_product_chunk)))
                response = emailcomponent.testmail('lifco.onboard@gmail.com',
                                                   "Product sync @@@products_to_elasticLive@@@",
                                                   'Data preparation Completed and Pushed to Elastic,' + ' @ ' + str(
                                                       datetime.datetime.now()) + ' datas=====>' + str(obj))
                                                   # '=====current_product_chunk======' + str(len(current_product_chunk)) + '=======threads========' + str(threading.active_count()))

def get_product_field_value_for_elastic(item_id, field_name):
    data = {}
    if field_name == 'category':
        data_arr = get_category_hierarchy(item_id,'name')

    elif field_name == 'category_slug':
        data_arr = get_category_hierarchy(item_id,'slug')

    elif field_name == 'category_id':
        data_arr = get_category_hierarchy(item_id,'id')

    elif field_name == 'channel_currency_product_price':
        data_arr = get_channel_currency_product_price(item_id)

    elif field_name == 'brand':
        data_arr = get_brand(item_id,"name")

    elif field_name == 'brand_id':
        data_arr = get_brand(item_id,"id")

    elif field_name == 'brand_slug':
        data_arr = get_brand(item_id,"slug")

    elif field_name == 'taxclass':
        data_arr = get_taxclass(item_id,'taxclass_id')

    elif field_name == 'po_taxclass':
        data_arr = get_taxclass(item_id,'po_taxclass_id')

    elif field_name == 'supplier':
        data_arr = get_product_supplier(item_id)

    elif field_name == 'unit':
        data_arr = get_unit(item_id)

    data = {field_name:data_arr}
    return data

class UpdateBulkElasticCheck(generics.ListAPIView):
    def get(self, request, field_name, start, end, format=None):
        try:
            response = emailcomponent.testmail('binayak.santra@navsoft.in', "Data Prepared--" + str(field_name),
                                               'Data preparation process start' + str(datetime.datetime.now()))
            table_name = 'EngageboostProducts'
            # field_name = 'channel_currency_product_price'
            item_ids = EngageboostProducts.objects.filter(isblocked='n', isdeleted='n').values_list('id', flat=True)[int(start):int(end)]

            print('item_ids=======>', item_ids)
            # item_ids = item_ids_get.values_list('id', flat=True)
            action = 'update'
            es = Elasticsearch([{'host': settings.ELASTIC_HOST, 'port': settings.ELASTIC_PORT}])

            model=apps.get_model('webservices',table_name)


            datas = []
            docs = []

            prod_obj = model.objects.filter(isdeleted='n')

            if len(item_ids)>0:
                prod_obj = prod_obj.filter(id__in=item_ids)

            if prod_obj.count()>0:
                products = prod_obj.order_by("-id").all().iterator()

                # common.check_mapping_elastic(table_name)

                new_cm_id = prod_obj.values_list('id', flat=True)
                # print('new_cm_id=======>', new_cm_id)
                module_name = get_index_name_elastic(new_cm_id[0], table_name)

                # prod_exists = es.mget(index=module_name, id=new_cm_id, doc_type="data")
                data_string = []
                for id in new_cm_id:
                    id_string = {
                        "_id": id,
                        "_source": False
                    }
                    data_string.append(id_string)
                # data_string={
                #       "ids" : list(new_cm_id)
                #         }
                print(data_string)
                prod_exists = es.mget(body=json.dumps({"docs":data_string}), index=module_name, doc_type="data")
                # print('prod_exists=======>', prod_exists)
                # return Response(prod_exists['docs'])
                for item in prod_exists['docs']:
                    # print('item=====>', item)
                    # return Response(item)
                    # cm_id= item.id
                    cm_id= item['_id']
                    # website_id = item.website_id

                    # module_name = get_index_name_elastic(cm_id,table_name)
                    # print('module_name=======>', module_name)
                    # print('cm_id=======>', cm_id)
                    # exists = es.exists(index=module_name, id=cm_id, doc_type="data")

                    # if exists:
                    if item['found']==True:
                        # data = get_product_field_value_for_elastic(item.id, field_name)
                        data = get_product_field_value_for_elastic(cm_id, field_name)

                        # print("=====data=====", data)

                        header = {
                            "_op_type": 'update',
                            "_index": module_name,
                            "_type": "data",
                            "_id": cm_id,
                            "doc": data
                        }
                    else:
                        now_item = products.filter(id=cm_id)
                        serializer_class = get_serializer_class_elastic(table_name)
                        # serializer = serializer_class(item,partial=True)
                        serializer = serializer_class(now_item,partial=True)
                        data = serializer.data
                        # print("Data Formatting Start=====",datetime.now())
                        # data = common.setUpLangDataToSerializer(data)
                        data = format_serialized_data(table_name,data)

                        header = {
                            "_index": module_name,
                            "_type": "data",
                            "_id": cm_id,
                            "_source": data
                        }
                    docs.append(header)

                response = emailcomponent.testmail('binayak.santra@navsoft.in', "Data Prepared", 'Data preparation completed, initiating elastic push'  + str(datetime.datetime.now()))
                # print("Updated products==========",docs)
                obj = helpers.bulk(es,docs)
                datas.append({"msg": "Success", "item_ids": item_ids})
                response = emailcomponent.testmail('binayak.santra@navsoft.in', "Data Pushed to Elastic",
                                                      'Data updating to elastic completed' + str(datetime.datetime.now()) + "DATAS======>" + str(datas))

                # print("After All=====",datetime.now())
                # print(datas)
                return Response(datas)
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            datas = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
            print("Elastic Error ==========",datas)
        return Response(datas)

def create_product_slug(name=None,pk=None,next=2):
    try:
        name = name.strip().lower().replace('"', "").replace(" ", "-").replace(".", "-").replace("/", "").replace("&", "and").translate({ord(c): "" for c in "'!@#$%^*()[]{};:,./<>?\|`~=+"})
    except:
        pass
    print("Product Name========================",name)
    slug = name
    original_slug = slug

    if pk!=None:
        instance = EngageboostProducts.objects.filter(isdeleted='n').exclude(id=pk)
    else:
        instance = EngageboostProducts.objects.filter(isdeleted='n')
    instance = instance.filter(**{'slug': slug})
    # print(instance.query,instance.count())
    if instance.count()>0:
        # print("Here==============")
        slug = original_slug
        end = '%s%s' % ('-', next)
        slug = '%s%s' % (slug, end)
        # print("slug==============",slug)
        next = int(next)+1
        slug = create_product_slug(slug,pk,next)
        return slug
    else:
        return slug

@csrf_exempt
def update_product_price(request):
    update_all_product()
    data={"status":1}
    return JsonResponse(data)

@postpone
def update_all_product():
    # for product_id in all_ids:
    product_obj = EngageboostProducts.objects.filter(isdeleted='n').order_by('-id')
    if product_obj.count()>0:
        product_obj = product_obj.values('id').all()
        for item in product_obj:
            product_id = item['id']
            print("product_id=================",product_id)
            # price_data = get_channel_currency_product_price(product_id)
            save_data_to_elastic(product_id, "EngageboostProducts")
            # change_field_value_elastic(product_id,'EngageboostProducts',{"channel_currency_product_price":price_data})
        print("End function")
    return 1

def unique_slugify(instance,value,slug_field_name='slug',queryset=None,slug_separator='-'):
    slug_field = instance._meta.get_field(slug_field_name)
    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len - len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1
    return slug
    # setattr(instance, slug_field.attname, slug)

def _slug_strip(value, separator='-'):
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)

    return value

def GenerateOrderId(website_id=None):
    if website_id is None:
        website_id = 1

    rs_settings = EngageboostGlobalSettings.objects.get(website_id=website_id)
    orders = EngageboostOrdermaster.objects.last()
    Order1 =int(orders.id)+int(1)
    Order1 = str(Order1)
    # cust_order_id = str(rs_settings.orderid_format)+str(Order1)
    cust_order_id = str(Order1)
    cust_order_id = "5"+Order1.zfill(7)
    return cust_order_id

def sync_db_seq():
    cursor = connection.cursor()
    from django.apps import apps

    models= ['auditlog','webservices']
    for item in models:
        alldata = apps.all_models[item]
        for model in alldata:
            model = apps.get_model(item,model)
            new_object = model() # Create an instance of that model
            # model.objects.filter(...) # Query the objects of that model
            model._meta.db_table # Get the name of the model in the database
            # model._meta.verbose_name # Get a verbose name of the model
            model_table = str(model._meta.db_table)
            # print(str(model_table))
            try:
                res = cursor.execute("SELECT setval('"+model_table+"_id_seq', (SELECT MAX(id) FROM "+model_table+"))")
                print(model_table,"squence synced")
            except:
                pass


class SaveElasticByUser(generics.ListAPIView):
    def put(self, request, format=None):
        product_id = request.data["product_id"]
        print("product_id=====", product_id)
        rs_product_ids = EngageboostProducts.objects.filter(id__in = product_id).values_list('id', flat=True)
        product_id_list = list(rs_product_ids)
        # product_id_list = set(product_id_list)
        if len(product_id_list)>0:
            for i in range(len(product_id_list)):
                save_data_to_elastic(product_id_list[i],"EngageboostProducts")

        data = {
            "status":1
        }
        return Response(data)

# sync_db_seq()


def firebaseNotification(user_id, message_title, message_body, noti_type, user_type, device_type, custom_order_id, order_id):

    global_settings_FCM_SERVER_KEY = EngageboostAdditionalGlobalsettings.objects.filter(
        settings_key__in=('FCM_SERVER_KEY_ANDROID', 'FCM_SERVER_KEY_IOS', 'FCM_SERVER_KEY_PICKING'))

    FCM_SERVER_KEY_ANDROID = global_settings_FCM_SERVER_KEY.filter(
        settings_key='FCM_SERVER_KEY_ANDROID')
    FCM_SERVER_KEY_IOS = global_settings_FCM_SERVER_KEY.filter(
        settings_key='FCM_SERVER_KEY_IOS')
    FCM_SERVER_KEY_PICKING = global_settings_FCM_SERVER_KEY.filter(
        settings_key='FCM_SERVER_KEY_PICKING')

    result = {}

    #-------------------FOR ANDROID USERS--------------------#
    if FCM_SERVER_KEY_ANDROID.count()>0 and user_type=='customer' and device_type=='android':
        FCM_SERVER_KEY_ANDROID = FCM_SERVER_KEY_ANDROID.first()
        push_service = FCMNotification(api_key=FCM_SERVER_KEY_ANDROID.settings_value)

        registration_ids = list(
            EngageboostAllUserDeviceToken.objects.filter(user_id=user_id, device_token__isnull=False,
                                                         device_type='a').values_list('device_token', flat=True))

        data_message = {
            "custom_order_id": custom_order_id,
            "order_id": int(order_id),
            "title": message_title,
            "message": message_body,
            "noti_type": noti_type,
            "priority": "high"
        }

        if len(registration_ids) > 0:
            # result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title,
            result = push_service.multiple_devices_data_message(registration_ids=registration_ids,
                                                                # message_title=message_title,
                                                                # message_body=message_body)
                                                                data_message=data_message)

    # -------------------FOR IOS USERS--------------------#
    elif FCM_SERVER_KEY_IOS.count()>0 and user_type=='customer' and device_type=='ios':
        FCM_SERVER_KEY_IOS = FCM_SERVER_KEY_IOS.first()
        push_service = FCMNotification(api_key=FCM_SERVER_KEY_IOS.settings_value)

        registration_ids = list(
            EngageboostAllUserDeviceToken.objects.filter(user_id=user_id, device_token__isnull=False,
                                                         device_type='i').values_list('device_token', flat=True))

        data_message = {
            # "data": {
                "custom_order_id": custom_order_id,
                "order_id": int(order_id),
                "title": message_title,
                "message": message_body,
                "noti_type": noti_type,
                # "sound": "default"
                # "priority": "high"
            # }
        }

        if len(registration_ids) > 0:
            result = push_service.notify_multiple_devices(registration_ids=registration_ids,
                                                                message_title=message_title,
                                                                message_body=message_body,
                                                                sound="default",
                                                                data_message=data_message)

    # -------------------FOR ANDROID PICKERS--------------------#
    elif FCM_SERVER_KEY_PICKING.count()>0 and user_type=='picker' and device_type=='android':
        FCM_SERVER_KEY_PICKING = FCM_SERVER_KEY_PICKING.first()
        push_service = FCMNotification(api_key=FCM_SERVER_KEY_PICKING.settings_value)

        registration_ids = list(
            EngageboostAllUserDeviceToken.objects.filter(user_id=user_id, device_token__isnull=False,
                                                         device_type='a').values_list('device_token', flat=True))

        # print('registration_ids')
        # print(registration_ids)
        data_message = {
                "order_id": custom_order_id,
                "title": message_title,
                "message": message_body,
                "noti_type": noti_type,
                "priority": "high"
        }


        if len(registration_ids) > 0:
            result = push_service.multiple_devices_data_message(registration_ids=registration_ids,
            # result = push_service.notify_multiple_devices(registration_ids=registration_ids,
            #                                               message_title=message_title,
            #                                               message_body=message_body,
                                                          data_message=data_message)


    # result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
    #                                            message_body=message_body, message_icon=message_icon)
                                               # message_body=message_body, message_icon='stock_ticker_update')
                                               # message_body=message_body, badge=message_icon)
                                               # message_body=message_body, badge=42)
                                               # message_body=message_body, message_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRL9uEpss7SRrafVH8X-lQsLdJ-uVJnpCbU1w&usqp=CAU")

    # result = {}
    # if len(registration_ids)>0:
        # result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)

    # print("result==", result)

    return Response(result)



def notification_send_by_AutoResponder(orderid=None, autoResponderId=None):
    buffer_data = getAutoResponder("", "", "", "", "", "", autoResponderId)
    if buffer_data and buffer_data["content"]:
        autoResponderData = buffer_data["content"]
        notification_body = autoResponderData["notification_body"]
        notification_title = autoResponderData["notification_title"]
        notification_body_store = autoResponderData["notification_body_store"]
        notification_title_store = autoResponderData["notification_title_store"]
        noti_type = autoResponderData["name"]

        if autoResponderId == 32 or autoResponderId == "32":
            notification_body = autoResponderData["sms_content_text"]
            notification_title = autoResponderData["sms_subject"]

        if orderid is not None:
            rs_order_products = EngageboostOrdermaster.objects.filter(id=orderid).first()
            if rs_order_products:
                custom_order_id = rs_order_products.custom_order_id
                customer = EngageboostCustomers.objects.filter(id=rs_order_products.customer_id).first()

            if noti_type in ('Place Order', 'Order Substitute Completed'):
                order_products = EngageboostOrderProducts.objects.filter(order_id=orderid).first()
                pickers = EngageboostUsers.objects.filter(warehouse_id=order_products.warehouse_id)

                print('pickers')
                print(pickers)





        if notification_body not in ('', None) and notification_title not in ('', None):
            notification_body = notification_body.replace('{@custom_order_id}', custom_order_id)
            print('======customercontent=======', notification_body)

            firebaseNotification(customer.auth_user_id, notification_title, notification_body, noti_type, 'customer', 'android', custom_order_id, orderid)
            firebaseNotification(customer.auth_user_id, notification_title, notification_body, noti_type, 'customer', 'ios', custom_order_id, orderid)

        # if noti_type == 'Place Order':
        if notification_body_store not in ('', None) and notification_title_store not in ('', None):
            notification_body_store = notification_body_store.replace('{@custom_order_id}', custom_order_id)
            print('======storecontent=======', notification_body_store)

            for picker in pickers:
                firebaseNotification(picker.id, notification_title_store, notification_body_store, noti_type, 'picker', 'android', custom_order_id, orderid)
    return


# notification_send_by_AutoResponder(3049, 30)

class SaveElasticByUser(generics.ListAPIView):
    def put(self, request, format=None):
        product_id = request.data["product_id"]
        print("product_id=====", product_id)
        rs_product_ids = EngageboostProducts.objects.filter(id__in = product_id).values_list('id', flat=True)
        product_id_list = list(rs_product_ids)
        # product_id_list = set(product_id_list)
        if len(product_id_list)>0:
            for i in range(len(product_id_list)):
                save_data_to_elastic(product_id_list[i],"EngageboostProducts")

        data = {
            "status":1
        }
        return Response(data)

class SaveElasticByUserNew(generics.ListAPIView):
    def put(self, request, format=None):
        parent_category_name = request.data["parent_category_name"]
        category = EngageboostCategoryMasters.objects.filter(name=parent_category_name).first()
        category_list = []
        if category:
            category_list.append(category.id)
            child_category = EngageboostCategoryMasters.objects.filter(parent_id=category.id).values_list('id',
                                                                                                          flat=True)
            category_list.extend(list(child_category))
            print("=====category_list=====", category_list)
            # return
            category_products = list(EngageboostProductCategories.objects.values_list('product_id', flat=True).order_by(
                'product_id').distinct('product_id').filter(category_id__in=category_list, is_parent='y'))
            # print("====category_products====", len(category_products))
            # print("====category_products====", category_products)
            # for prod in category_products:



            product_id = list(category_products)
            print("product_id=====", product_id)
            rs_product_ids = EngageboostProducts.objects.filter(id__in = product_id).values_list('id', flat=True)
            product_id_list = list(rs_product_ids)
            # product_id_list = set(product_id_list)
            if len(product_id_list)>0:
                for i in range(len(product_id_list)):
                    save_data_to_elastic(product_id_list[i],"EngageboostProducts")

        data = {
            "status":1
        }
        return Response(data)
# save_data_to_elastic(2436,"EngageboostOrdermaster")
# SendSms("Hello Kalyan this test SMS from GoGrocery. Please inform if received.", "919804977639")

#------Binayak Start 16-03-2021-----#
def single_channel_currency_price_update_string(cm_id, price_data, warehouse_id, first=0):
    flag = 0
    for channel_currency_product_price in price_data:
        # print("======channel_currency_product_price======warehouse_id======",
        # 	  channel_currency_product_price['warehouse_id'])
        if channel_currency_product_price['warehouse_id'] == warehouse_id:
            price_data_single = get_channel_currency_product_price(cm_id, 1, [warehouse_id])

            for data in price_data_single:
                channel_currency_product_price['id'] = data['id']
                channel_currency_product_price['promotions'] = data['promotions']
                channel_currency_product_price['price_type'] = data['price_type']
                channel_currency_product_price['channel_id'] = data['channel_id']
                channel_currency_product_price['currency_id'] = data['currency_id']
                channel_currency_product_price['price'] = data['price']
                channel_currency_product_price['cost'] = data['cost']
                channel_currency_product_price['mrp'] = data['mrp']
                channel_currency_product_price['min_quantity'] = data['min_quantity']
                channel_currency_product_price['max_quantity'] = data['max_quantity']
                channel_currency_product_price['warehouse_id'] = data['warehouse_id']
                channel_currency_product_price['website_id'] = data['website_id']
                channel_currency_product_price['start_date'] = data['start_date']
                channel_currency_product_price['end_date'] = data['end_date']
                channel_currency_product_price['product'] = data['product']
                channel_currency_product_price['product_price_type'] = data['product_price_type']
                channel_currency_product_price['new_default_price'] = data['new_default_price']
                channel_currency_product_price['new_default_price_unit'] = data['new_default_price_unit']
                channel_currency_product_price['discount_price_unit'] = data['discount_price_unit']
                channel_currency_product_price['discount_price'] = data['discount_price']
                channel_currency_product_price['discount_amount'] = data['discount_amount']
                channel_currency_product_price['disc_type'] = data['disc_type']
                channel_currency_product_price['coupon'] = data['coupon']

            flag = 1

    if flag == 0:
        # print("I am here")
        price_data_single = get_channel_currency_product_price(cm_id, 1, [warehouse_id], first)
        # price_data_single = json.dumps(price_data_single)
        # price_data_single = json.loads(price_data_single)
        # print("======price_data_single======", price_data_single[0])
        # price_data = common.get_channel_currency_product_price(cm_id)
        price_data.append(price_data_single[0])

    return price_data
#------Binayak End 16-03-2021-----#

#------Binayak Start 17-03-2021------#
def multiple_warehouse_channel_currency_price_update_string(cm_id, price_data, warehouse_list):
    # not_found_warehouse = []
    # print("=========multiple_warehouse_channel_currency_price_update_string========")
    # # print("=========price_data========", price_data)
    # print("=========cm_id========", cm_id)
    # print("=========warehouse_list========", warehouse_list)

    for channel_currency_product_price in price_data:
        # flag = 0
        warehouse_id = None
        # print("========loop warehouse_id=========", type(channel_currency_product_price['warehouse_id']))
        if channel_currency_product_price['warehouse_id'] in warehouse_list:
            warehouse_id = channel_currency_product_price['warehouse_id']
            # print("======warehouse_id=======", warehouse_id, cm_id)
            price_data_single = get_channel_currency_product_price(cm_id, 1, [warehouse_id])
            # print("=====price_data_single=====", price_data_single)

            for data_single in price_data_single:
                channel_currency_product_price['id'] = data_single['id']
                channel_currency_product_price['promotions'] = data_single['promotions']
                channel_currency_product_price['price_type'] = data_single['price_type']
                channel_currency_product_price['channel_id'] = data_single['channel_id']
                channel_currency_product_price['currency_id'] = data_single['currency_id']
                channel_currency_product_price['price'] = data_single['price']
                channel_currency_product_price['cost'] = data_single['cost']
                channel_currency_product_price['mrp'] = data_single['mrp']
                channel_currency_product_price['min_quantity'] = data_single['min_quantity']
                channel_currency_product_price['max_quantity'] = data_single['max_quantity']
                channel_currency_product_price['warehouse_id'] = data_single['warehouse_id']
                channel_currency_product_price['website_id'] = data_single['website_id']
                channel_currency_product_price['start_date'] = data_single['start_date']
                channel_currency_product_price['end_date'] = data_single['end_date']
                channel_currency_product_price['product'] = data_single['product']
                channel_currency_product_price['product_price_type'] = data_single['product_price_type']
                channel_currency_product_price['new_default_price'] = data_single['new_default_price']
                channel_currency_product_price['new_default_price_unit'] = data_single['new_default_price_unit']
                channel_currency_product_price['discount_price_unit'] = data_single['discount_price_unit']
                channel_currency_product_price['discount_price'] = data_single['discount_price']
                channel_currency_product_price['discount_amount'] = data_single['discount_amount']
                channel_currency_product_price['disc_type'] = data_single['disc_type']
                channel_currency_product_price['coupon'] = data_single['coupon']

            index_of = warehouse_list.index(warehouse_id)
            warehouse_list.pop(index_of)
            # print("======warehouse_list=======", warehouse_list)
        # else:
            # not_found_warehouse.append(warehouse_id)
            # flag = 1

        # if flag == 0:
    if len(warehouse_list)>0:
        # if warehouse_id not in found_warehouse:
        # print("I am here=====for warehouse ", warehouse_list)
        price_data_single = get_channel_currency_product_price(cm_id, 1, warehouse_list)
        # price_data_single = json.dumps(price_data_single)
        # price_data_single = json.loads(price_data_single)
        # print("======price_data_single======", price_data_single)
        # print("======price_data_single 123======", price_data_single[0])
        # price_data = common.get_channel_currency_product_price(cm_id)
        price_data.extend(price_data_single)
    # data = {field_name: price_data}
    return price_data
#------Binayak Start 17-03-2021------#

def remove_warehouse_channel_currency_price_update_string(cm_id, price_data, warehouse_list):
    # not_found_warehouse = []

    new_price_data = []
    for channel_currency_product_price in price_data:
        # print("============================channel_currency_product_price==========================")
        # print(channel_currency_product_price['warehouse_id'])
        # print(warehouse_list)
        # print(channel_currency_product_price)
        # flag = 0
        warehouse_id = None
        if channel_currency_product_price['warehouse_id'] in warehouse_list:
            pass
            # warehouse_id = channel_currency_product_price['warehouse_id']
            # # print("======warehouse_id=======", warehouse_id, cm_id)
            # price_data_single = get_channel_currency_product_price(cm_id, 1, [warehouse_id])
            # # print("=====price_data_single=====", price_data_single)
            #
            # for data_single in price_data_single:
            #     channel_currency_product_price['id'] = data_single['id']
            #     channel_currency_product_price['promotions'] = data_single['promotions']
            #     channel_currency_product_price['price_type'] = data_single['price_type']
            #     channel_currency_product_price['channel_id'] = data_single['channel_id']
            #     channel_currency_product_price['currency_id'] = data_single['currency_id']
            #     channel_currency_product_price['price'] = data_single['price']
            #     channel_currency_product_price['cost'] = data_single['cost']
            #     channel_currency_product_price['mrp'] = data_single['mrp']
            #     channel_currency_product_price['min_quantity'] = data_single['min_quantity']
            #     channel_currency_product_price['max_quantity'] = data_single['max_quantity']
            #     channel_currency_product_price['warehouse_id'] = data_single['warehouse_id']
            #     channel_currency_product_price['website_id'] = data_single['website_id']
            #     channel_currency_product_price['start_date'] = data_single['start_date']
            #     channel_currency_product_price['end_date'] = data_single['end_date']
            #     channel_currency_product_price['product'] = data_single['product']
            #     channel_currency_product_price['product_price_type'] = data_single['product_price_type']
            #     channel_currency_product_price['new_default_price'] = data_single['new_default_price']
            #     channel_currency_product_price['new_default_price_unit'] = data_single['new_default_price_unit']
            #     channel_currency_product_price['discount_price_unit'] = data_single['discount_price_unit']
            #     channel_currency_product_price['discount_price'] = data_single['discount_price']
            #     channel_currency_product_price['discount_amount'] = data_single['discount_amount']
            #     channel_currency_product_price['disc_type'] = data_single['disc_type']
            #     channel_currency_product_price['coupon'] = data_single['coupon']
            #
            # index_of = warehouse_list.index(warehouse_id)
            # warehouse_list.pop(index_of)
            # print("======warehouse_list=======", warehouse_list)
        else:
            new_price_data.append(channel_currency_product_price)
            # not_found_warehouse.append(warehouse_id)
            # flag = 1

        # if flag == 0:
    # if len(warehouse_list)>0:
    #     # if warehouse_id not in found_warehouse:
    #     # print("I am here=====for warehouse ", warehouse_list)
    #     price_data_single = get_channel_currency_product_price(cm_id, 1, warehouse_list)
    #     # price_data_single = json.dumps(price_data_single)
    #     # price_data_single = json.loads(price_data_single)
    #     # print("======price_data_single======", price_data_single)
    #     # print("======price_data_single 123======", price_data_single[0])
    #     # price_data = common.get_channel_currency_product_price(cm_id)
    #     price_data.extend(price_data_single)
    # data = {field_name: price_data}
    return new_price_data

def get_parent_cat(cat_id):
    parent_category_data = EngageboostCategoryMasters.objects.filter(id=cat_id).first()
    if parent_category_data:
        parent_cat_id = parent_category_data.parent_id
        # print("======parent_cat_id=======", parent_cat_id)
        parent_category = EngageboostCategoryMasters.objects.filter(id=parent_cat_id).first()
        if parent_category:
            parent_category_slug = parent_category.slug
            # parent_category_name = parent_category.name
            # print("====parent_category_name========", parent_category_name)
            data = {
                'status': 1,
                'name': parent_category.name
            }
            return data
            # return parent_category_name
        else:
            data = {
                'status': 0
            }
    else:
        data = {
            'status': 0
        }
        return data