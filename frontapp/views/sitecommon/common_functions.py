from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
# Import Model And Serializer
from webservices.models import *
from frontapp.frontapp_serializers import *
from webservices.serializers import TemplateIndustryMastersSerializer

from django.db.models import F, Func, FloatField
from django.db.models.functions import Cast
from django.template.defaultfilters import slugify

import json
import base64
import sys,os
import traceback
import datetime
import socket
import requests

# ------Binayak Start 29-10-2020-----#
class Sin(Func):
	function = 'SIN'


class Cos(Func):
	function = 'COS'


class Acos(Func):
	function = 'ACOS'


class Radians(Func):
	function = 'RADIANS'


class Degrees(Func):
	function = 'DEGREES'
# ------Binayak End 29-10-2020-----#

def GetGlobalSettings():
	data = {}
	rs_global_settings = EngageboostGlobalSettings.objects.filter(isblocked='n', isdeleted='n').first()
	if rs_global_settings:
		data = GlobalSettingserializer(rs_global_settings).data
	return data

def getStateDetails(state_id):
	stateDetails = EngageboostStates.objects.filter(id=state_id).all().order_by("-id")
	data ={"status":1, "State":stateDetails,"message": 'Getting State information'}
	return data

def save_order_activity(order_id=None,activity_time=None,status=None,msg=None,userId=None,activityType=1):
	hostname = socket.gethostname()
	IPAddr = socket.gethostbyname(hostname)
	if userId is None or userId=='':
		userId = 1
	
	if activity_time is None:
		activity_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
	try:
		order_activities = EngageboostOrderActivity.objects.create(order_id=order_id,activity_comments=msg,status=status,activity_date=activity_time,user_ip_address=IPAddr,user_id=userId,activity_type=activityType)
		data={'status':1,'api_status':order_activities.id, 'message': 'Order activity saved.'}  
	except Exception as error:
		trace_back = sys.exc_info()[2]
		line = trace_back.tb_lineno
		data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error), 'message': str(error)}   
	return data

def getAutoResponder(shipment_status,webshop_id,warehouse_id,shipping_method_id,website_id,autoResponderId):
	if shipment_status and webshop_id and warehouse_id and shipping_method_id and website_id:
		if shipping_method_id:
			applicableResponder = EngageboostApplicableAutoresponders.objects.order_by("-id").filter(shipment_status=shipment_status,website_id=website_id,applicable_for='ShippingProvider',applicable_chanel_id = shipping_method_id).first()
		elif warehouse_id:
			applicableResponder = EngageboostApplicableAutoresponders.objects.order_by("-id").filter(shipment_status=shipment_status,website_id=website_id,applicable_for='Warehouse',applicable_chanel_id=warehouse_id).first()
		else:
			applicableResponder = EngageboostApplicableAutoresponders.objects.order_by("-id").filter(shipment_status=shipment_status,website_id=website_id,applicable_for='Channel',applicable_chanel_id=webshop_id).first()

		if applicableResponder:
			autoResponderId = applicableResponder.auto_responder_id
		else:
			autoResponderId = autoResponderId
	else:
		autoResponderId = autoResponderId
	
	applicableResponder = EngageboostEmailTypeContents.objects.order_by("-id").filter(id= autoResponderId).first()
	if applicableResponder:
		applicableResponderSerializer=EmailTypeContentsSerializer(applicableResponder)
		data ={"status":1, "content":applicableResponderSerializer.data,"message": 'Auto Responder Data'}
	else:
		data ={"status":0, "content":{},"message": 'No Auto Responder Found'}
	return data

def get_company_website_id_by_url():
    website_id = 1
    return website_id

def pointToAmount_converter(points, website_id):
    globalsettings_rs = EngageboostGlobalSettings.objects.filter(website_id=website_id).first()
    point_in_amount = 0
    if globalsettings_rs:
        point_in_amount = 1 # globalsettings_rs.loyalty_amount
    total_points_in_amunt = round(float(points) / float(point_in_amount), 2)
    return total_points_in_amunt

def update_brand_slug():
    rs_brand = EngageboostBrandMasters.objects.filter(slug__isnull=True, isblocked='n', isdeleted='n')
    if rs_brand:
        for brand in rs_brand:
            name = brand.name.lower()
            name1 = name.replace(" ", "-")
            nametrns = name1.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~=+"})
            nametrns = slugify(nametrns)
            EngageboostBrandMasters.objects.filter(id=brand.id).update(slug=nametrns)
      
def SendSms(message,mobile_no):
	settings_data = GetGlobalSettings()
	# url = "https://apiw.me.synapselive.com/push.aspx"
	url = "http://apiw.me.synapselive.com/push.aspx"
	# https://apiw.me.synapselive.com/push.aspx?user=ONBOARDEXP&pass=onboa@12&message=Test from gogrocery&lang=0&senderid=GoGrocery&mobile=971506983429
	username 	= "ONBOARDEXP"
	password 	= "onboa@12"
	senderid 	= "GoGrocery"
	if settings_data:
		username 	= settings_data["sms_auth_key"]
		password 	= "onboa@12" # settings_data["sms_route"]
		senderid 	= settings_data["sms_sender_id"]
	# mobile_no = "506983429"
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
				print("data==========", data)
				r = requests.get(url = url, params = data) 
				# print("r++++++++++", r)
				url_response = r.text
				# print("url_response=======", url_response)
				# r++++++++++ <Response [200]>
				# url_response======= 1HAT43U7YQ
				# ====================================================
				# r++++++++++ <Response [200]>
				# url_response======= Invalid Credentials
				data = {
					"status":1,
					"response":url_response
				}
			except Exception as error:
				trace_back = sys.exc_info()[2]
				line = trace_back.tb_lineno
				data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}

			sms_insert_arr = {
				"mobile_number":mobile_no,
				"sms_content_text":message,
				"response_text":url_response,
				"created":datetime.datetime.now(datetime.timezone.utc)
			}
			EngageboostSmsLog.objects.create(**sms_insert_arr)
		
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
	print("sms data+++++++++++", data)
	return data

# SendSms("Hello Mahesh this test SMS from GoGrocery. Please inform if received.", "+971506983429")
# SendSms("Hello Kalyan this test SMS from GoGrocery. Please inform if received.", "919804977639")

class UpdateDeviceDetails(APIView):
    def post(self, request, format=None):
        now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
        user = request.user
        user_id = user.id
        requestdata = JSONParser().parse(request)
        device_id = request.META.get('HTTP_DEVICEID')
        device_token = requestdata['device_token']
        version = requestdata['version']
        os_version = requestdata['os_version']
        device_type = requestdata['device_type']
        created = now_utc
        modified = now_utc

        create_arr = {
            "user_id": user_id,
            "device_id": device_id,
            "device_token": device_token,
            "version": version,
            "os_version": os_version,
            "device_type": device_type,
            "created": created,
            "modified": modified
        }
        if user_id:
            if device_token is not None and device_type is not None:
                if device_type.lower() == 'a':
                    EngageboostCustomers.objects.filter(auth_user_id=user_id).update(device_token_android=device_token)
                else:
                    EngageboostCustomers.objects.filter(auth_user_id=user_id).update(device_token_ios=device_token)

                if device_id is not None:
                    rs_device = EngageboostAllUserDeviceToken.objects.filter(user_id=user_id,
                                                                             device_id=device_id).first()
                    if rs_device:
                        EngageboostAllUserDeviceToken.objects.filter(user_id=user_id, device_id=device_id).update(
                            device_token=device_token, version=version, os_version=os_version, device_type=device_type,
                            modified=modified)
                    else:
                        EngageboostAllUserDeviceToken.objects.create(**create_arr)
                else:
                    rs_device = EngageboostAllUserDeviceToken.objects.filter(user_id=user_id).first()
                    if rs_device:
                        EngageboostAllUserDeviceToken.objects.filter(user_id=user_id).update(device_token=device_token,
                                                                                             version=version,
                                                                                             os_version=os_version,
                                                                                             device_type=device_type,
                                                                                             modified=modified)
                    else:
                        EngageboostAllUserDeviceToken.objects.create(**create_arr)
                status = 200
                res_type = "Success"
                msg = "Update Successfully."
            else:
                status = 0
                res_type = "fail"
                msg = "Provide Device_token and Device_type."
        else:
            status = 0
            res_type = "fail"
            msg = "User not Found."

        data = {
            "status": status,
            "res_type": res_type,
            "msg": msg
        }
        return Response(data)


# @permission_classes([])
# class StoreTypeAll(generics.ListAPIView):
# 	def get(self, request, format=None):
# 		try:
# 			store_type_obj = EngageboostTemplateIndustryMasters.objects.filter(isblocked='n', isdeleted='n', website_id=1).order_by('order')
# 			serializer = TemplateIndustryMastersSerializer(store_type_obj, many=True)
# 			if serializer:
# 				data = {
# 					'data': serializer.data,
# 					'status': 1,
# 					'api_status': '',
# 					'Message': 'success',
# 				}
# 			else:
# 				data = {
# 					'status': 0,
# 					'api_status': '',
# 					'Message': 'data not found',
# 				}
# 		except Exception as error:
# 			trace_back = sys.exc_info()[2]
# 			line = trace_back.tb_lineno
# 			data = {"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),
# 					"message": str(error)}
# 		return Response(data)

#-----Binayak Start-----#
@permission_classes([])
class StoreTypeAll(generics.ListAPIView):
	def post(self, request, format=None):

		# ------Binayak Start 29-10-2020   Change request type to post-----#
		request_data = JSONParser().parse(request)
		latitude = request_data.get('latitude')
		longitude = request_data.get('longitude')
		website_id = request_data.get('website_id')

		if latitude != None and longitude != None and website_id != None:

			radlat = Radians(float(latitude))
			radlong = Radians(float(longitude))
			radflat = Radians(Cast(F('latitude'), FloatField()))
			radflong = Radians(Cast(F('longitude'), FloatField()))
			warehouse_list = []
			Expression = 111.045 * Degrees(
				Acos(Cos(radlat) * Cos(radflat) * Cos(radflong - radlong) + Sin(radlat) * Sin(radflat)))
		# ------Binayak End 29-10-2020-----#
		try:
			store_type_obj = EngageboostTemplateIndustryMasters.objects.filter(isblocked='n', isdeleted='n', website_id=1).order_by('order')
			serializer = TemplateIndustryMastersSerializer(store_type_obj, many=True)
			if serializer:
				# ------Binayak Start 29-10-2020-----#

				if latitude != None and longitude != None and website_id != None:
					for ser_data in serializer.data:

						get_warehouse_ids = EngageboostStoreType.objects.filter(type_id=ser_data['id'], isdeleted='n',isblocked='n').values_list("warehouse_id",flat=True)

						if get_warehouse_ids:

							rs_objWarehouse = EngageboostWarehouseMasters.objects.annotate(distance=Expression).filter(
								website_id=website_id, isblocked='n', isdeleted='n', id__in=get_warehouse_ids).exclude(
								latitude__isnull=True, longitude__isnull=True).order_by('distance').filter(distance__lte=F('max_distance_sales')).count()

							if rs_objWarehouse > 0:
								rs_objWarehouse_count = 1
							else:
								rs_objWarehouse_count = 0
						else:
							rs_objWarehouse_count = 0
						ser_data['has_store'] = int(rs_objWarehouse_count)

				# ------Binayak End 29-10-2020-----#
				data = {
					'data': serializer.data,
					'status': 1,
					'api_status': '',
					'Message': 'success',
				}
			else:
				data = {
					'status': 0,
					'api_status': '',
					'Message': 'data not found',
				}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data = {"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),
					"message": str(error)}
		return Response(data)

#-----Binayak Start-----#