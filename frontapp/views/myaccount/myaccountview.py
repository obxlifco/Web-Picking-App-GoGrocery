from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.db.models import F, Func, FloatField
from django.db.models.functions import Cast
from webservices.models import *
from frontapp.frontapp_serializers import *
import json
import base64
import sys,os
import traceback
import datetime
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password
from webservices.views.common import common
from datetime import timedelta
# from opencage.geocoder import OpenCageGeocode
class MyProfile(APIView):
    
    def get(self, request, format=None):
        user                   =  request.user
        user_id                =  user.id
        str_status = ""
        try:
            rs_user = EngageboostUsers.objects.filter(id=user_id).first()
            return_arr = {}
            if rs_user:
                rs_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
                address = ""
                gender = ""
                if rs_customer:
                    if rs_customer.address:
                        address = rs_customer.address
                    if rs_customer.gender:
                        gender = rs_customer.gender
                return_arr = {
                    "first_name":rs_user.first_name,
                    "last_name":rs_user.last_name,
                    "email":rs_user.email,
                    "phone":rs_user.phone,
                    "location":address,
                    "gender":gender
                }
                str_status = status.HTTP_200_OK
                data = {
                    "status":status.HTTP_200_OK,
                    "msg":"success",
                    "data":return_arr
                }
            else:
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                    "status":status.HTTP_204_NO_CONTENT,
                    "data":return_arr
                }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}

        return Response(data, str_status)

    def put(self, request, format=None):
        requestdata     = JSONParser().parse(request)
        user            = request.user
        user_id         = user.id
        first_name = None
        if "first_name" in requestdata:
            first_name      = requestdata['first_name']

        last_name = None
        if "last_name" in requestdata:
            last_name      = requestdata['last_name']
        
        email = None
        if "email" in requestdata:
            email      = requestdata['email'].strip()

        phone = None
        if "phone" in requestdata:
            phone      = requestdata['phone']
        
        gender = None
        if "gender" in requestdata:
            gender      = requestdata['gender'] 
        
        location = None
        if "location" in requestdata:
            location      = requestdata['location']
    
        str_status = ""
        try:
            #if first_name is None:
            if first_name =='':
                raise Exception("first name is required")
            #if last_name is None: 
            if last_name=='':
                raise Exception("last name is required") 
            #if email is None: 
            if email=='':
                raise Exception("email is required")  
            #if phone is None: 
            if phone =='':
                raise Exception("phone no is required")

            # ckeckingcnt = EngageboostUsers.objects.filter(id=user_id,email=email,phone=phone).count()
            check_email = EngageboostUsers.objects.filter(Q(email__iexact=email) | Q(phone=phone)).exclude(id=user_id).count()
            if check_email>0:
               raise Exception("Email / Mobile already exist")
            else:
                user = EngageboostUsers.objects.filter(isblocked='n',isdeleted='n',id=user_id).update(first_name=first_name,last_name=last_name,email=email,phone=phone)            
                customer = EngageboostCustomers.objects.filter(isblocked='n',isdeleted='n',auth_user_id=user_id).update(first_name=first_name,last_name=last_name,email=email,phone=phone,address=location,gender=gender)             
                if customer:
                    str_status = status.HTTP_200_OK
                    data = {
                        'status':str_status,
                        'message': 'Profile update successfully.'
                    }

        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status":str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response (data)

#----Test----#
class MyProfileTest(APIView):

    def get(self, request, format=None):
        user = request.user
        user_id = user.id
        str_status = ""
        try:
            rs_user = EngageboostUsers.objects.filter(id=user_id).first()
            return_arr = {}
            if rs_user:
                rs_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
                address = ""
                gender = ""
                if rs_customer:
                    if rs_customer.address:
                        address = rs_customer.address
                    if rs_customer.gender:
                        gender = rs_customer.gender
                return_arr = {
                    "first_name": rs_user.first_name,
                    "last_name": rs_user.last_name,
                    "email": rs_user.email,
                    "phone": rs_user.phone,
                    "location": address,
                    "gender": gender
                }
                str_status = status.HTTP_200_OK
                data = {
                    "status": status.HTTP_200_OK,
                    "msg": "success",
                    "data": return_arr
                }
            else:
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                    "status": status.HTTP_204_NO_CONTENT,
                    "data": return_arr
                }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line,
                    "error_message": str(error), "message": str(error)}

        return Response(data, str_status)

    def put(self, request, format=None):
        requestdata = JSONParser().parse(request)
        user = request.user
        user_id = user.id
        first_name = None
        if "first_name" in requestdata:
            first_name = requestdata['first_name']

        last_name = None
        if "last_name" in requestdata:
            last_name = requestdata['last_name']

        email = None
        if "email" in requestdata:
            email = requestdata['email'].strip()

        phone = None
        if "phone" in requestdata:
            phone = requestdata['phone']

        gender = None
        if "gender" in requestdata:
            gender = requestdata['gender']

        location = None
        if "location" in requestdata:
            location = requestdata['location']

        str_status = ""
        try:
            # if first_name is None:
            if first_name == '':
                raise Exception("first name is required")
            # if last_name is None:
            if last_name == '':
                raise Exception("last name is required")
            # if email is None:
            if email == '':
                raise Exception("email is required")
            # if phone is None:
            if phone == '':
                raise Exception("phone no is required")

            # ckeckingcnt = EngageboostUsers.objects.filter(id=user_id,email=email,phone=phone).count()
            check_email = EngageboostUsers.objects.filter(Q(email__iexact=email) | Q(phone=phone)).exclude(
                id=user_id).count()
            if check_email > 0:
                raise Exception("Email / Mobile already exist")
            else:
                user = EngageboostUsers.objects.filter(isblocked='n', isdeleted='n', id=user_id).update(
                    first_name=first_name, last_name=last_name, email=email, phone=phone)

                # -------Binayak Start 24-12-2020--------#
                if gender:
                    customer = EngageboostCustomers.objects.filter(isblocked='n', isdeleted='n',
                                                                   auth_user_id=user_id).update(first_name=first_name,
                                                                                                last_name=last_name,
                                                                                                email=email,
                                                                                                phone=phone,
                                                                                                address=location,
                                                                                                gender=gender)
                else:
                    customer = EngageboostCustomers.objects.filter(isblocked='n', isdeleted='n',
                                                                   auth_user_id=user_id).update(first_name=first_name,
                                                                                                last_name=last_name,
                                                                                                email=email,
                                                                                                phone=phone,
                                                                                                address=location
                                                                                                )
                # -------Binayak End 24-12-2020--------#

                if customer:
                    str_status = status.HTTP_200_OK
                    data = {
                        'status': str_status,
                        'message': 'Profile update successfully.'
                    }

        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line,
                    "error_message": str(error), "message": str(error)}
        return Response(data)
#----Test----#


class ChangePassword(APIView):
    def put(self, request, format=None):
        requestdata=JSONParser().parse(request)
        user                = request.user
        user_id             = user.id
        current_password    = requestdata['current_password']
        str_status = ""
        try:
            if current_password=='':
                raise Exception("current password is required ") 
            
            user = EngageboostUsers.objects.filter(isdeleted='n',isblocked='n',id=user_id).first()
            password_check = user.check_password(current_password)

            if password_check==False: 
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                    'status':str_status,
                    'message': 'This current password  doesn\'t exist'
                }
                #return JsonResponse(data)
            else:
                new_password = requestdata['new_password']
                if new_password=='':
                    raise Exception("New password is required ")
                confirm_password = requestdata['confirm_password'] 
                if confirm_password=='': 
                    raise Exception("Confirm password is required ") 
                if new_password !=confirm_password:
                    str_status = status.HTTP_406_NOT_ACCEPTABLE
                    data = {
                        'status':str_status,
                        'message': 'Password and confirm password does not match.'
                    }
                else:
                    hash_password = make_password(confirm_password, None, 'md5')
                    EngageboostUsers.objects.filter(id=user_id,isdeleted='n',isblocked='n').update(password=hash_password)
                    EngageboostCustomers.objects.filter(auth_user_id=user_id,isdeleted='n',isblocked='n').update(password=hash_password)
                    str_status = status.HTTP_200_OK
                    data = {
                        'status':str_status,
                        'message': 'Password has been successfully updated. Please login to continue.'
                    }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status":str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response(data)

class OrderHistory(APIView):
    def get(self, request, format=None):
        user       = request.user
        user_id    = user.id
        req_type = request.GET['req_type']
        #warehouse_id        = request.META.get('HTTP_WAREHOUSE')
        str_status = ""
        global_setting_date = EngageboostGlobalSettings.objects.filter(website_id=1,isdeleted='n',isblocked='n').first()
        if global_setting_date.timezone_id:
        	global_setting_zone = EngageboostTimezones.objects.filter(id = global_setting_date.timezone_id).first()
        	time_offset = global_setting_zone.offset
        else:
        	time_offset = 0
        try:
            rs_customer = EngageboostCustomers.objects.filter(auth_user_id = user_id).first()
            if rs_customer:
                customer_id = rs_customer.id
            else:
                raise Exception("Customer Not Found.") 
            # req_order_status =  req_type
            # order_request_tuple = (2,4,13,16,999) if req_order_status=='past':
            order_request_tuple = (2,4,13,16,999)
            if req_type == "past":
                order = EngageboostOrdermaster.objects.filter(isblocked='n',isdeleted='n',customer_id=customer_id,order_status__in=order_request_tuple).all().order_by('-id')
            # else:
            #     order = EngageboostOrdermaster.objects.filter(isblocked='n',isdeleted='n',customer_id=customer_id).exclude(order_status__in=order_request_tuple).all().order_by('-id')
            elif req_type == "present":
                order = EngageboostOrdermaster.objects.filter(isblocked='n', isdeleted='n',
                                                              customer_id=customer_id).exclude(
                    order_status__in=order_request_tuple).all().order_by('-id')
            elif req_type == "substitute":
                order_ids = []
                substitute_time_data = EngageboostAdditionalGlobalsettings.objects.filter(
                    settings_key='substitute_approval_time')
                if substitute_time_data.count():
                    substitute_time = substitute_time_data.first().settings_value
                else:
                    substitute_time = 10

                pending_order = EngageboostOrdermaster.objects.filter(isblocked='n', isdeleted='n',
                                                                      customer_id=customer_id,
                                                                      order_substitute_products__order_id=F('id'),
                                                                      order_substitute_products__send_approval='pending').all().order_by(
                    '-id').distinct('id')
                for p_order in pending_order:

                    substitute_detail = EngageboostOrderSubstituteProducts.objects.filter(order_id=p_order.id).first()

                    # print('created====>',substitute_detail.created)
                    substitute_valid_time = substitute_detail.created + datetime.timedelta(minutes=int(substitute_time))
                    # now_utc = datetime.datetime.utcnow()
                    time_now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()

                    # print(now_utc)
                    # print('now=====>',time_now_utc)

                    if substitute_valid_time >= time_now_utc:
                        # print('in')
                        # print('created====>', substitute_detail.created)
                        # print('now=====>', time_now_utc)
                        order_ids.append(p_order.id)

                # print('order_ids====>',order_ids)

                order = pending_order.filter(id__in=order_ids)
            #if warehouse_id is not None:
               #order = order.filter(assign_wh = warehouse_id)
            order_data = EngageboostOrdermasterSerializers(order,many=True)
            order_data = order_data.data
            if order_data:
                for orderdata in order_data:
                    if int(orderdata["order_status"]) == 99 and int(orderdata["buy_status"]) == 1:
                        orderdata["str_order_status"] = "Waiting Approval"
                    elif int(orderdata["order_status"]) == 20 and int(orderdata["buy_status"]) == 1:
                        orderdata["str_order_status"] = "Approved"
                    elif int(orderdata["order_status"]) == 0 and int(orderdata["buy_status"]) == 1:
                        orderdata["str_order_status"] = "Pending"
                    elif int(orderdata["order_status"]) == 100 and int(orderdata["buy_status"]) == 1:
                        orderdata["str_order_status"] = "Processing"
                    elif int(orderdata["order_status"]) == 1 and int(orderdata["buy_status"]) == 1:
                        orderdata["str_order_status"] = "Shipped"
                    elif int(orderdata["order_status"]) == 2 and int(orderdata["buy_status"]) == 1:
                        orderdata["str_order_status"] = "Cancelled"
                    elif int(orderdata["order_status"]) == 4 and int(orderdata["buy_status"]) == 1:
                        orderdata["str_order_status"] = "Completed"
                    elif int(orderdata["order_status"]) == 5 and int(orderdata["buy_status"]) == 1:
                        orderdata["str_order_status"] = "Full Refund"
                    elif int(orderdata["order_status"]) == 6 and int(orderdata["buy_status"]) == 1:
                        orderdata["str_order_status"] = "Partial Refund"
                    elif int(orderdata["order_status"]) == 13 and int(orderdata["buy_status"]) == 1:
                        orderdata["str_order_status"] = "Delivered"
                    elif int(orderdata["order_status"]) == 16 and int(orderdata["buy_status"]) == 1:
                        orderdata["str_order_status"] = "Closed"
                    elif int(orderdata["order_status"]) == 18 and int(orderdata["buy_status"]) == 1:
                        orderdata["str_order_status"] = "Pending Service"
                    elif int(orderdata["order_status"]) == 3 and int(orderdata["buy_status"]) == 0:
                        orderdata["str_order_status"] = "Abandoned"
                    elif int(orderdata["order_status"]) == 999 and int(orderdata["buy_status"]) == 0:
                        orderdata["str_order_status"] = "Failed"
                    elif int(orderdata["order_status"]) == 9999 and int(orderdata["buy_status"]) == 1:
                        orderdata["str_order_status"] = 'Hold'
                    elif int(orderdata["order_status"]) == 21 and int(orderdata["buy_status"]) == 1:
                        orderdata["str_order_status"] = 'Payment Initiated'
                    elif int(orderdata["order_status"]) == 21 and int(orderdata["buy_status"]) == 1:
                        orderdata["str_order_status"] = 'Payment Initiated'
                    else:
                        orderdata["str_order_status"] = 'Invoiced'
                    

                    paid_status = [4,5,6,16]
                    if orderdata['paid_amount']>0:
                        str_payment_status = "Paid"
                    else:
                        str_payment_status = "Unpaid"
                    orderdata["str_payment_status"] = str_payment_status
                    orderdata['created_gmt'] = orderdata['created']
                    created = datetime.datetime.strptime(str(orderdata['created']), "%Y-%m-%dT%H:%M:%S.%fZ")
                    modified = datetime.datetime.strptime(str(orderdata['modified']), "%Y-%m-%dT%H:%M:%S.%fZ")
                    if time_offset < 0:
                    	time_offset = str(time_offset).split('-')
                    	time_offset = time_offset[1]
                    	orderdata['created'] = created - timedelta(hours=float(time_offset))
                    	orderdata['modified'] = modified - timedelta(hours=float(time_offset))
                    else:
                    	orderdata['created'] = created + timedelta(hours=float(time_offset))
                    	orderdata['modified'] = modified + timedelta(hours=float(time_offset))
                    shipment_status = ""
                    if orderdata['shipment_id'] is not None and orderdata['shipment_id']>0:
                        rs_shipment = EngageboostShipmentOrders.objects.filter(order_id=orderdata["id"], shipment=orderdata['shipment_id']).first()
                        if rs_shipment:
                            shipment_status = rs_shipment.shipment_status
                    orderdata["shipment_status"] = shipment_status
                str_status = status.HTTP_200_OK
                data = {
                    'status':str_status,
                    'data':order_data,
                }
            else:
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                    'status':str_status,
                    'message': 'Order list not found',
                    'data':{}
                }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response (data)
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


class Float(Func):
    function = 'FLOAT'

class DeliveryAddress(APIView):
    def get(self, request, format=None):
        user                   =  request.user
        user_id                =  user.id
        str_status = ""
        try:
            rs_customer = EngageboostCustomers.objects.filter(auth_user_id = user_id, isblocked = 'n', isdeleted = 'n').first()
            # print('rs_customer++++', rs_customer.query)
            if rs_customer:
                customer_id = rs_customer.id
            else:
                raise Exception("Customer Not Found.") 
            user_address = EngageboostCustomersAddressBook.objects.filter(isblocked='n',isdeleted='n',customers_id=customer_id).all().order_by('-set_primary')
            address_data = CustomersAddressBookSerializer(user_address,many=True).data
            if address_data:
                str_status = status.HTTP_200_OK  
                data = {
                    'status':str_status,
                    'data' : address_data 
                    }
            else:
                str_status = status.HTTP_200_OK
                data = {
                'status':str_status,
                'message': 'No data found.',
                'data':[]
                }
               
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response (data,str_status)

        
    def post(self, request, format=None):
        requestdata            =  JSONParser().parse(request)
        user                   =  request.user
        user_id                =  user.id
        name                   =  requestdata['name']
        address                =  requestdata['address']
        area =None
        if "area" in requestdata and requestdata['area'] !='':
            area               =  requestdata['area']
        country                =  requestdata['country']
        city =None
        if "city" in requestdata and requestdata['city'] !='':
            city               =  requestdata['city']
        state = None
        if "state" in requestdata and requestdata['state'] !='':
            state              =  requestdata['state']
        pincode = None
        if "pincode" in requestdata and requestdata['pincode']!='':
            pincode            =  requestdata['pincode']

        mobile_no              =  requestdata['mobile_no']
        alternative_mobile_no = None
        if "alternative_mobile_no" in requestdata and requestdata['alternative_mobile_no']!='':
            alternative_mobile_no  =  requestdata['alternative_mobile_no']
        website_id = request.META.get('HTTP_WID')
        warehouse_id     = request.META.get('HTTP_WAREHOUSE')
        str_status = ""
        now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()

        rs_user = EngageboostUsers.objects.filter(id=user_id).first()
        user_email = None
        if rs_user:
            user_email = rs_user.email
        if website_id is None:
            website_id = 1
        if website_id<=0:
            website_id = 1
        try:
            rs_customer = EngageboostCustomers.objects.filter(auth_user_id = user_id, isblocked = 'n', isdeleted = 'n').first()
            if rs_customer:
                customer_id = rs_customer.id
            else:
                raise Exception("Customer Not Found.") 
            if name=='':
                raise Exception("name is required") 
            # if last_name=='':
            #     raise Exception("last name is required")
            if address=='':
                raise Exception("address is required")
            if country=='':
                raise Exception("country is required")
            if state=='':
                raise Exception("state is required")
            if mobile_no=='':
                raise Exception("mobile no is required") 
            #name = first_name + " " + last_name
            geo_location = get_geo_location(address,city,area,country,state, pincode)
            warehouse_list = []
            latitude  = geo_location["lat"]
            longitude = geo_location["lng"]
            # print('latitude',latitude)
            # print('longitude',longitude)
            radlat      = Radians(float(latitude))
            radlong     = Radians(float(longitude))
            radflat     = Radians(Cast(F('latitude'), FloatField()))
            radflong    = Radians(Cast(F('longitude'), FloatField()))
            Expression = 111.045 * Degrees(Acos(Cos(radlat) * Cos(radflat) * Cos(radflong - radlong) + Sin(radlat) * Sin(radflat)))
            rs_objWarehouse = EngageboostWarehouseMasters.objects.annotate(distance=Expression).filter(website_id=website_id, isblocked='n', isdeleted='n').exclude(latitude__isnull=True,longitude__isnull=True).order_by('distance')
            #print(rs_objWarehouse.query)
            cntprimary=EngageboostCustomersAddressBook.objects.filter(set_primary=1,customers_id=customer_id, isblocked = 'n', isdeleted = 'n').count()
            if cntprimary>0:
                setprimary_update=EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,set_primary=1, isblocked = 'n', isdeleted = 'n').update(set_primary=0)
                customer_address = EngageboostCustomersAddressBook.objects.create(
                    customers_id=customer_id,
                    set_primary = 1,
                    billing_email_address = user_email,
                    delivery_name = name,
                    delivery_street_address = address, 
                    delivery_landmark = area,
                    delivery_country = country,
                    delivery_city = city,
                    delivery_state = state,
                    delivery_postcode = pincode,
                    delivery_phone = mobile_no,
                    delivery_fax = alternative_mobile_no,
                    delivery_email_address = user_email,
                    billing_name = name,
                    billing_street_address = address,
                    billing_landmark = area, 
                    billing_country = country,
                    billing_city = city,
                    billing_state = state,
                    billing_postcode = pincode,
                    billing_phone = mobile_no,
                    billing_fax = alternative_mobile_no,
                    created =  now_utc,
                    modified = now_utc,
                    lat_val=geo_location["lat"],
                    long_val=geo_location["lng"]
                )
                customer_address.save()

            else:
                customer_address=EngageboostCustomersAddressBook.objects.create(
                    customers_id=customer_id,
                    set_primary = 1,
                    delivery_name = name,
                    delivery_email_address = user_email,
                    delivery_street_address = address, 
                    delivery_landmark = area,
                    delivery_country = country,
                    delivery_city = city,
                    delivery_state = state,
                    delivery_postcode = pincode,
                    delivery_phone = mobile_no,
                    delivery_fax = alternative_mobile_no,
                    billing_name = name,
                    billing_email_address = user_email,
                    billing_street_address = address,
                    billing_landmark = area, 
                    billing_country = country,
                    billing_city = city,
                    billing_state = state,
                    billing_postcode = pincode,
                    billing_phone = mobile_no,
                    billing_fax = alternative_mobile_no,
                    created =  now_utc,
                    modified = now_utc,
                    lat_val = geo_location["lat"],
                    long_val = geo_location["lng"]
                )
                customer_address.save()  
            address_data = CustomersAddressBookSerializer(customer_address).data
            if len(rs_objWarehouse)>0:
                # objWarehouse = objWarehouse.first()
                for objWarehouse in rs_objWarehouse:
                    warehouse_obj = {}
                    if objWarehouse.max_distance_sales:
                        max_distance_salesKM = objWarehouse.max_distance_sales*1.60934
                        if objWarehouse.distance <= max_distance_salesKM:
                            warehouse_obj.update({
                                "id":objWarehouse.id,
                                "website_id":objWarehouse.website_id,
                                "name":objWarehouse.name,
                                "code":objWarehouse.code,
                                "address":objWarehouse.address,
                                "country_id":objWarehouse.country_id,
                                "state_id":objWarehouse.state_id,
                                "state_name":objWarehouse.state_name,
                                "city":objWarehouse.city,
                                "zipcode":objWarehouse.zipcode,
                                "phone":objWarehouse.phone,
                                "email":objWarehouse.email,
                                "channel_id":objWarehouse.channel_id,
                                "latitude":objWarehouse.latitude,
                                "longitude":objWarehouse.longitude,
                                "max_distance_sales":objWarehouse.max_distance_sales,
                                "distance":objWarehouse.distance,
                                "warehouse_logo":objWarehouse.warehouse_logo,
                            })
                            warehouse_list.append(warehouse_obj)
                # print("*******************warehouse_id**************")
                # print(warehouse_list)
                isMatch = 'n'
                wMsh = 'Sorry!!! Your delivery address does not belongs to our serviceable area.'
                if warehouse_list and len(warehouse_list)>0:
                    for wl in warehouse_list:
                        #print('+++++++++++++',int(wl['id']))
                        if int(wl['id']) == int(warehouse_id):
                            isMatch = "y"
                            wMsh = "Warehouse match"

                if warehouse_list:
                    str_status = status.HTTP_200_OK
                    data = {
                        'status':str_status,
                        'warehouseMatch':isMatch,
                        'message': 'Address create successfully',
                        'message2': wMsh,
                        'warehouse_list':warehouse_list,
                        'data' : address_data 

                    }
                else:
                    #print("*********************elsessssss******")
                    str_status = status.HTTP_200_OK  
                    data = {
                        'status':str_status,
                        'warehouseMatch':'n',
                        'message':'Address create successfully',
                        'message2': 'Sorry!!! Your delivery address does not belongs to our serviceable area.',
                        'warehouse_list' : warehouse_list,
                        'data' : address_data 
                    }
            else:
                #print("*********************else******")
                str_status = status.HTTP_200_OK
                data = {
                    "status":str_status,
                    'warehouseMatch':'n',
                    'message': 'Address create successfully',
                    'message2': 'Sorry!!! Your delivery address does not belongs to our serviceable area.',
                    'warehouse_list' : warehouse_list,
                    'data' : address_data 
                }
            
            # if address_data:
            #     str_status = status.HTTP_200_OK  
            #     data = {
            #         'status':str_status,
            #         'message': 'Address create successfully',
            #         'data' : address_data 
            #         }
               
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response (data,str_status)

    def put(self, request, format=None):
        requestdata            =  JSONParser().parse(request)
        user                   =  request.user
        user_id                =  user.id
        customers_addressId    =  requestdata['customers_addressId']
        name                   =  requestdata['name']
        address                =  requestdata['address']
        area =None
        if "area" in requestdata and requestdata['area'] !='':
            area               =  requestdata['area']
        # landmark               =  requestdata['landmark']
        country                =  requestdata['country']
        city =None
        if "city" in requestdata and requestdata['city'] !='':
            city               =  requestdata['city']
        #city                   =  requestdata['city']
        mobile_no              =  requestdata['mobile_no']
        
        state = None
        if "state" in requestdata and requestdata['state'] !='':
            state                  =  requestdata['state']
        pincode = None
        
        if "pincode" in requestdata and requestdata['pincode'] !='':
            pincode                =  requestdata['pincode']

        alternative_mobile_no = None
        if "alternative_mobile_no" in requestdata:
            alternative_mobile_no  =  requestdata['alternative_mobile_no']
        
        check                  =  requestdata['check']
        website_id = request.META.get('HTTP_WID')
        warehouse_id     = request.META.get('HTTP_WAREHOUSE')
        str_status = ""
        
        now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
        if website_id is None:
            website_id = 1
        if website_id<=0:
            website_id = 1
        try:
            rs_customer = EngageboostCustomers.objects.filter(auth_user_id = user_id,isblocked='n',isdeleted='n').first()
            if rs_customer:
                customer_id = rs_customer.id
            else:
                raise Exception("Customer Not Found.")
            if customers_addressId=='':
                raise Exception("customers address id is required")
            if name=='':
                raise Exception("name is required") 
            if address=='':
                raise Exception("address is required")
            if country=='':
                raise Exception("country is required")
            if state=='':
                raise Exception("state is required")
            if mobile_no=='':
                raise Exception("mobile no is required")
            # if check=='':
            #     raise Exception("check is required")
            rs_user = EngageboostUsers.objects.filter(id=user_id,isblocked='n',isdeleted='n').first()
            user_email = None
            if rs_user:
                user_email = rs_user.email

            #name = first_name + " " + last_name
            geo_location = get_geo_location(address,city,area,country,state, pincode)
            warehouse_list = []
            latitude  = geo_location["lat"]
            longitude = geo_location["lng"]
            # print('latitude',latitude)
            # print('longitude',longitude)
            radlat      = Radians(float(latitude))
            radlong     = Radians(float(longitude))
            radflat     = Radians(Cast(F('latitude'), FloatField()))
            radflong    = Radians(Cast(F('longitude'), FloatField()))
            Expression = 111.045 * Degrees(Acos(Cos(radlat) * Cos(radflat) * Cos(radflong - radlong) + Sin(radlat) * Sin(radflat)))
            rs_objWarehouse = EngageboostWarehouseMasters.objects.annotate(distance=Expression).filter(website_id=website_id, isblocked='n', isdeleted='n').exclude(latitude__isnull=True,longitude__isnull=True).order_by('distance')
            #print(rs_objWarehouse.query)
            #if check==1:
            cntprimary=EngageboostCustomersAddressBook.objects.filter(set_primary=1,customers_id=customer_id,isblocked='n',isdeleted='n').count()
            if cntprimary>0:
                setprimary_update=EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,set_primary=check,isblocked='n',isdeleted='n').update(set_primary=0)
                address_update=EngageboostCustomersAddressBook.objects.filter(isblocked='n',isdeleted='n',id=customers_addressId).update(
                    set_primary = check,
                    delivery_name = name,
                    delivery_email_address = user_email,
                    delivery_street_address = address, 
                    delivery_landmark = area,
                    delivery_country = country,
                    delivery_city = city,
                    delivery_state = state,
                    delivery_postcode = pincode,
                    delivery_phone = mobile_no,
                    delivery_fax = alternative_mobile_no,
                    billing_name = name,
                    billing_email_address = user_email,
                    billing_street_address = address,
                    billing_landmark = area, 
                    billing_country = country,
                    billing_city = city,
                    billing_state = state,
                    billing_postcode = pincode,
                    billing_phone = mobile_no,
                    billing_fax = alternative_mobile_no,
                    modified = now_utc,
                    lat_val = geo_location["lat"],
                    long_val = geo_location["lng"]
                    )  
                count_primary = EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,set_primary=1,isblocked='n',isdeleted='n').count()
                if count_primary==0:
                    next_id = EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,isdeleted='n',isblocked='n').exclude(id =customers_addressId).first()
                    addressid= next_id.id
                    EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,id=addressid,isblocked='n',isdeleted='n').update(set_primary=1)  

            else:
                address_update=EngageboostCustomersAddressBook.objects.filter(isblocked='n',isdeleted='n',id=customers_addressId).update(
                    set_primary = check,
                    delivery_name = name,
                    delivery_email_address = user_email,
                    delivery_street_address = address, 
                    delivery_landmark = area,
                    delivery_country = country,
                    delivery_city = city,
                    delivery_state = state,
                    delivery_postcode = pincode,
                    delivery_phone = mobile_no,
                    delivery_fax = alternative_mobile_no,
                    billing_name = name,
                    billing_email_address = user_email,
                    billing_street_address = address,
                    billing_landmark = area, 
                    billing_country = country,
                    billing_city = city,
                    billing_state = state,
                    billing_postcode = pincode,
                    billing_phone = mobile_no,
                    billing_fax = alternative_mobile_no,
                    modified = now_utc,
                    lat_val = geo_location["lat"],
                    long_val = geo_location["lng"]
                    )
                count_primary = EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,set_primary=1,isblocked='n',isdeleted='n').count()
                if count_primary==0:
                    next_id = EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,isdeleted='n',isblocked='n').exclude(id=customers_addressId).first()
                    addressid= next_id.id
                    EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,id=addressid,isblocked='n',isdeleted='n').update(set_primary=1)  

            if address_update:
                if len(rs_objWarehouse)>0:
                # objWarehouse = objWarehouse.first()
                    for objWarehouse in rs_objWarehouse:
                        warehouse_obj = {}
                        if objWarehouse.max_distance_sales:
                            max_distance_salesKM = objWarehouse.max_distance_sales*1.60934
                            if objWarehouse.distance <= max_distance_salesKM:
                                warehouse_obj.update({
                                    "id":objWarehouse.id,
                                    "website_id":objWarehouse.website_id,
                                    "name":objWarehouse.name,
                                    "code":objWarehouse.code,
                                    "address":objWarehouse.address,
                                    "country_id":objWarehouse.country_id,
                                    "state_id":objWarehouse.state_id,
                                    "state_name":objWarehouse.state_name,
                                    "city":objWarehouse.city,
                                    "zipcode":objWarehouse.zipcode,
                                    "phone":objWarehouse.phone,
                                    "email":objWarehouse.email,
                                    "channel_id":objWarehouse.channel_id,
                                    "latitude":objWarehouse.latitude,
                                    "longitude":objWarehouse.longitude,
                                    "max_distance_sales":objWarehouse.max_distance_sales,
                                    "distance":objWarehouse.distance,
                                    "warehouse_logo":objWarehouse.warehouse_logo,
                                })
                                warehouse_list.append(warehouse_obj)
                    # print("*******************warehouse_id**************")
                    # print(warehouse_list)
                    isMatch = 'n'
                    wMsh = 'Sorry!!! Your delivery address does not belongs to our serviceable area.'
                    if warehouse_list and len(warehouse_list)>0:
                        for wl in warehouse_list:
                            #print('+++++++++++++',int(wl['id']))
                            if int(wl['id']) == int(warehouse_id):
                                isMatch = "y"
                                wMsh = "Warehouse match"

                    if warehouse_list:
                        str_status = status.HTTP_200_OK
                        data = {
                            'status':str_status,
                            'warehouseMatch':isMatch,
                            'message': 'Address update successfully',
                            'message2': wMsh,
                            'warehouse_list':warehouse_list,
                            #'data' : address_data 

                        }
                    else:
                        #print("*********************elsessssss******")
                        str_status = status.HTTP_200_OK  
                        data = {
                            'status':str_status,
                            'warehouseMatch':'n',
                            'message':'Address update successfully',
                            'message2': 'Sorry!!! Your delivery address does not belongs to our serviceable area.',
                            'warehouse_list' : warehouse_list,
                            #'data' : address_data 
                        }
                else:
                    #print("*********************else******")
                    str_status = status.HTTP_200_OK
                    data = {
                        "status":str_status,
                        'warehouseMatch':'n',
                        'message': 'Address update successfully',
                        'message2': 'Sorry!!! Your delivery address does not belongs to our serviceable area.',
                        'warehouse_list' : warehouse_list,
                        #'data' : address_data 
                    }
                # str_status = status.HTTP_200_OK
                # data = {
                #     'status':str_status,
                #     'message': 'Address update successfully.',
                #     }
            else:
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                'status':str_status,
                'message': 'update failed',
                }
        
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status":str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response (data,str_status)

class CheckDeliveryAddress(APIView):
    def post(self, request, format=None):
        requestdata = JSONParser().parse(request)
        user = request.user
        user_id = user.id
        # address                =  requestdata['address']

        website_id = request.META.get('HTTP_WID')
        warehouse_id = request.META.get('HTTP_WAREHOUSE')

        # country = requestdata['country']
        city = None
        if "city" in requestdata and requestdata['city'] != '':
            city = requestdata['city']
        if "lat" in requestdata and requestdata['lat'] != '':
            lat = requestdata['lat']
        if "lng" in requestdata and requestdata['lng'] != '':
            lng = requestdata['lng']
        state = None
        if "state" in requestdata and requestdata['state'] != '':
            state = requestdata['state']
        str_status = ""
        # now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()

        # rs_user = EngageboostUsers.objects.filter(id=user_id).first()
        # user_email = None

        try:
            rs_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id, isblocked='n',
                                                              isdeleted='n').first()
            customer_id = None
            if rs_customer:
                customer_id = rs_customer.id

            if state == '':
                raise Exception("state is required")
            if city == '':
                raise Exception("city is required")

            KM_PER_DEGREE = 111.045
            METER_PER_DEGREE = KM_PER_DEGREE * 1000
            radlat = Radians(float(lat))
            radlong = Radians(float(lng))
            radflat = Radians(Cast(F('lat_val'), FloatField()))
            radflong = Radians(Cast(F('long_val'), FloatField()))
            Expression = METER_PER_DEGREE * Degrees(
                Acos(Cos(radlat) * Cos(radflat) * Cos(radflong - radlong) + Sin(radlat) * Sin(radflat)))
            # print('Expression=======>', Expression)
            # rs_objWarehouse = EngageboostCustomersAddressBook.objects.annotate(distance=Expression).filter(customers_id=customer_id,isblocked='n', isdeleted='n').exclude(lat_val__isnull=True,long_val__isnull=True).filter(distance__lte=1)
            # rs_objWarehouse = EngageboostCustomersAddressBook.objects.annotate(distance=Expression).filter(isblocked='n', isdeleted='n').exclude(lat_val__isnull=True,long_val__isnull=True).order_by('distance')
            distance = 999999999999
            address_data = {}
            addressMatch = False
            if customer_id != None:
                print('customer_id======>', customer_id)
                cntprimary = EngageboostCustomersAddressBook.objects.annotate(distance=Expression).filter(
                    customers_id=customer_id, isblocked='n', isdeleted='n').exclude(lat_val__isnull=True,
                                                                                    long_val__isnull=True).filter(
                    distance__lte=100)

                # cntprimary=EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id, isblocked = 'n', isdeleted = 'n', delivery_state=state_id, delivery_country=int(country_id))
                if int(cntprimary.count()) > 0:
                    address_data = CustomersAddressBookSerializer(cntprimary, many=True).data
                    addressMatch = True
                    distance = cntprimary.first().distance

            # print("*********************else******")
            str_status = status.HTTP_200_OK
            data = {
                "status": str_status,
                'addressMatch': addressMatch,
                'data': address_data,
                'distance': distance
            }

        # if address_data:
        #     str_status = status.HTTP_200_OK
        #     data = {
        #         'status':str_status,
        #         'message': 'Address create successfully',
        #         'data' : address_data
        #         }

        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line,
                    "error_message": str(error), "message": str(error)}
        return Response(data, str_status)

class CheckDeliveryAddressTest(APIView):
	def post(self, request, format=None):
		requestdata            =  JSONParser().parse(request)
		user                   =  request.user
		user_id                =  user.id
		# address                =  requestdata['address']

		website_id = request.META.get('HTTP_WID')
		warehouse_id     = request.META.get('HTTP_WAREHOUSE')

		# country = requestdata['country']
		city = None
		# if "city" in requestdata and requestdata['city'] != '':
		# 	city = requestdata['city']
		if "lat" in requestdata and requestdata['lat'] != '':
			lat = requestdata['lat']
		if "lng" in requestdata and requestdata['lng'] != '':
			lng = requestdata['lng']
		state = None
		# if "state" in requestdata and requestdata['state'] != '':
		# 	state = requestdata['state']
		str_status = ""
		# now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()

		# rs_user = EngageboostUsers.objects.filter(id=user_id).first()
		# user_email = None

		try:
			rs_customer = EngageboostCustomers.objects.filter(auth_user_id = user_id, isblocked = 'n', isdeleted = 'n').first()
			customer_id = None
			if rs_customer:
				customer_id = rs_customer.id

			# if state=='':
			# 	raise Exception("state is required")
			# if city=='':
			# 	raise Exception("city is required")

			KM_PER_DEGREE = 111.045
			METER_PER_DEGREE = KM_PER_DEGREE * 1000
			radlat      = Radians(float(lat))
			radlong     = Radians(float(lng))
			radflat     = Radians(Cast(F('lat_val'), FloatField()))
			radflong    = Radians(Cast(F('long_val'), FloatField()))
			Expression = METER_PER_DEGREE * Degrees(Acos(Cos(radlat) * Cos(radflat) * Cos(radflong - radlong) + Sin(radlat) * Sin(radflat)))
			# print('Expression=======>', Expression)
			# rs_objWarehouse = EngageboostCustomersAddressBook.objects.annotate(distance=Expression).filter(customers_id=customer_id,isblocked='n', isdeleted='n').exclude(lat_val__isnull=True,long_val__isnull=True).filter(distance__lte=1)
			# rs_objWarehouse = EngageboostCustomersAddressBook.objects.annotate(distance=Expression).filter(isblocked='n', isdeleted='n').exclude(lat_val__isnull=True,long_val__isnull=True).order_by('distance')
			geo_location_reverse = get_geo_location_reverse(lat, lng)
			state = geo_location_reverse["state"]

			distance = 999999999999
			address_data = []
			addressMatch = False
			if customer_id!=None:
				# print('customer_id======>', customer_id)
				cntprimary = EngageboostCustomersAddressBook.objects.annotate(distance=Expression).filter(customers_id=customer_id,
																										delivery_state=state,
																										isblocked='n',
																										isdeleted='n'
																										  ).exclude(lat_val__isnull=True,
																					long_val__isnull=True).filter(distance__lte=500).order_by('distance')


				# cntprimary=EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id, isblocked = 'n', isdeleted = 'n', delivery_state=state_id, delivery_country=int(country_id))
				if int(cntprimary.count())>0:
					for dist in cntprimary:
						print("id======> ", dist.id)
						print("Distance======> ", dist.distance)
						print("=====================================================> ")
					address_data = CustomersAddressBookSerializer(cntprimary, many=True).data
					addressMatch = True
					distance = cntprimary.first().distance

			#print("*********************else******")
			str_status = status.HTTP_200_OK
			data = {
				"status":str_status,
				'addressMatch':addressMatch,
				'data' : address_data,
				'distance': distance
			}

			# if address_data:
			#     str_status = status.HTTP_200_OK
			#     data = {
			#         'status':str_status,
			#         'message': 'Address create successfully',
			#         'data' : address_data
			#         }

		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			str_status = status.HTTP_417_EXPECTATION_FAILED
			data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
		return Response (data,str_status)

class DeleteAddress(APIView): 
    def get(self, request, pk, format=None):
        user                   =  request.user
        user_id                =  user.id
        str_status = ""
        rs_customer = EngageboostCustomers.objects.filter(auth_user_id = user_id ,isblocked = 'n', isdeleted = 'n').first()
        if rs_customer:
            customer_id = rs_customer.id
        else:
            str_status = status.HTTP_401_UNAUTHORIZED
            data = {
                'status':str_status,
                'message': 'Customer not found.',
            }
        rs_address = EngageboostCustomersAddressBook.objects.filter(id=pk,customers_id=customer_id, isblocked = 'n', isdeleted = 'n').first()
        if rs_address:
            EngageboostCustomersAddressBook.objects.filter(id=pk,customers_id=customer_id, isblocked = 'n', isdeleted = 'n').update(isblocked='y',isdeleted='y')
            str_status = status.HTTP_200_OK
            data = {
                'status':str_status,
                'message': 'Success.',
            }
        else:
            str_status = status.HTTP_401_UNAUTHORIZED
            data = {
                'status':str_status,
                'message': 'You are not allowed to delete this address.',
            }
        return Response(data,str_status)

class DeliveryAddressTest(APIView):
	def get(self, request, format=None):
		user                   =  request.user
		user_id                =  user.id
		str_status = ""
		try:
			rs_customer = EngageboostCustomers.objects.filter(auth_user_id = user_id, isblocked = 'n', isdeleted = 'n').first()
			# print('rs_customer++++', rs_customer.query)
			if rs_customer:
				customer_id = rs_customer.id
			else:
				raise Exception("Customer Not Found.")
			user_address = EngageboostCustomersAddressBook.objects.filter(isblocked='n',isdeleted='n',customers_id=customer_id).all().order_by('-set_primary')
			address_data = CustomersAddressBookSerializer(user_address,many=True).data
			if address_data:
				str_status = status.HTTP_200_OK
				data = {
					'status':str_status,
					'data' : address_data
					}
			else:
				str_status = status.HTTP_200_OK
				data = {
				'status':str_status,
				'message': 'No data found.',
				'data':[]
				}

		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			str_status = status.HTTP_417_EXPECTATION_FAILED
			data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
		return Response (data,str_status)

	#-----Binayak Start 15-02-2021-----#
	def post(self, request, format=None):
		requestdata            =  JSONParser().parse(request)
		user                   =  request.user
		user_id                =  user.id
		name                   =  requestdata['name']
		address                =  requestdata['address']


		area = latitude = longitude = country = city = state = pincode = None
		if "lat_val" in requestdata and requestdata['lat_val'] !='':
			latitude			   =  requestdata['lat_val']

		if "long_val" in requestdata and requestdata['long_val'] !='':
			longitude			   =  requestdata['long_val']

		if "area" in requestdata and requestdata['area'] !='':
			area               	   =  requestdata['area']

		if "country" in requestdata and requestdata['country'] !='':
			country                =  requestdata['country']

		if "city" in requestdata and requestdata['city'] !='':
			city               =  requestdata['city']

		if "state" in requestdata and requestdata['state'] !='':
			state              =  requestdata['state']

		if "pincode" in requestdata and requestdata['pincode']!='':
			pincode            =  requestdata['pincode']

		mobile_no              =  requestdata['mobile_no']
		alternative_mobile_no = None
		if "alternative_mobile_no" in requestdata and requestdata['alternative_mobile_no']!='':
			alternative_mobile_no  =  requestdata['alternative_mobile_no']
		website_id = request.META.get('HTTP_WID')
		warehouse_id     = request.META.get('HTTP_WAREHOUSE')
		str_status = ""
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()

		rs_user = EngageboostUsers.objects.filter(id=user_id).first()
		user_email = None
		if rs_user:
			user_email = rs_user.email
		if website_id is None:
			website_id = 1
		if website_id<=0:
			website_id = 1
		try:
			rs_customer = EngageboostCustomers.objects.filter(auth_user_id = user_id, isblocked = 'n', isdeleted = 'n').first()
			if rs_customer:
				customer_id = rs_customer.id
			else:
				raise Exception("Customer Not Found.")
			if name=='':
				raise Exception("name is required")
			# if last_name=='':
			#     raise Exception("last name is required")
			if address=='':
				raise Exception("address is required")
			# if country=='':
			# 	raise Exception("country is required")
			# if state=='':
			# 	raise Exception("state is required")
			if mobile_no=='':
				raise Exception("mobile no is required")
			#name = first_name + " " + last_name
			if state != None and country != None:
				geo_location = get_geo_location(address,city,area,country,state, pincode)
				latitude  = geo_location["lat"]
				longitude = geo_location["lng"]
				# print('latitude',latitude)
				# print('longitude',longitude)
			else:
				geo_location_reverse = get_geo_location_reverse(latitude, longitude)
				print("=======here adding========")
				# return Response(geo_location_reverse)
				city = geo_location_reverse["city"]
				state = geo_location_reverse["state"]
				country = geo_location_reverse["country"]


			warehouse_list = []


			radlat      = Radians(float(latitude))
			radlong     = Radians(float(longitude))
			radflat     = Radians(Cast(F('latitude'), FloatField()))
			radflong    = Radians(Cast(F('longitude'), FloatField()))
			Expression = 111.045 * Degrees(Acos(Cos(radlat) * Cos(radflat) * Cos(radflong - radlong) + Sin(radlat) * Sin(radflat)))
			rs_objWarehouse = EngageboostWarehouseMasters.objects.annotate(distance=Expression).filter(website_id=website_id, isblocked='n', isdeleted='n').exclude(latitude__isnull=True,longitude__isnull=True).order_by('distance')
			#print(rs_objWarehouse.query)
			cntprimary=EngageboostCustomersAddressBook.objects.filter(set_primary=1,customers_id=customer_id, isblocked = 'n', isdeleted = 'n').count()
			if cntprimary>0:
				setprimary_update=EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,set_primary=1, isblocked = 'n', isdeleted = 'n').update(set_primary=0)
				customer_address = EngageboostCustomersAddressBook.objects.create(
					customers_id=customer_id,
					set_primary = 1,
					billing_email_address = user_email,
					delivery_name = name,
					delivery_street_address = address,
					delivery_landmark = area,
					delivery_country = country,
					delivery_city = city,
					delivery_state = state,
					delivery_postcode = pincode,
					delivery_phone = mobile_no,
					delivery_fax = alternative_mobile_no,
					delivery_email_address = user_email,
					billing_name = name,
					billing_street_address = address,
					billing_landmark = area,
					billing_country = country,
					billing_city = city,
					billing_state = state,
					billing_postcode = pincode,
					billing_phone = mobile_no,
					billing_fax = alternative_mobile_no,
					created =  now_utc,
					modified = now_utc,
					lat_val = latitude,
					long_val = longitude
					# lat_val=geo_location["lat"],
					# long_val=geo_location["lng"]
				)
				customer_address.save()

			else:
				customer_address=EngageboostCustomersAddressBook.objects.create(
					customers_id=customer_id,
					set_primary = 1,
					delivery_name = name,
					delivery_email_address = user_email,
					delivery_street_address = address,
					delivery_landmark = area,
					delivery_country = country,
					delivery_city = city,
					delivery_state = state,
					delivery_postcode = pincode,
					delivery_phone = mobile_no,
					delivery_fax = alternative_mobile_no,
					billing_name = name,
					billing_email_address = user_email,
					billing_street_address = address,
					billing_landmark = area,
					billing_country = country,
					billing_city = city,
					billing_state = state,
					billing_postcode = pincode,
					billing_phone = mobile_no,
					billing_fax = alternative_mobile_no,
					created =  now_utc,
					modified = now_utc,
					lat_val = latitude,
					long_val = longitude
					# lat_val = geo_location["lat"],
					# long_val = geo_location["lng"]
				)
				customer_address.save()
			address_data = CustomersAddressBookSerializer(customer_address).data
			if len(rs_objWarehouse)>0:
				# objWarehouse = objWarehouse.first()
				for objWarehouse in rs_objWarehouse:
					warehouse_obj = {}
					if objWarehouse.max_distance_sales:
						max_distance_salesKM = objWarehouse.max_distance_sales*1.60934
						if objWarehouse.distance <= max_distance_salesKM:
							warehouse_obj.update({
								"id":objWarehouse.id,
								"website_id":objWarehouse.website_id,
								"name":objWarehouse.name,
								"code":objWarehouse.code,
								"address":objWarehouse.address,
								"country_id":objWarehouse.country_id,
								"state_id":objWarehouse.state_id,
								"state_name":objWarehouse.state_name,
								"city":objWarehouse.city,
								"zipcode":objWarehouse.zipcode,
								"phone":objWarehouse.phone,
								"email":objWarehouse.email,
								"channel_id":objWarehouse.channel_id,
								"latitude":objWarehouse.latitude,
								"longitude":objWarehouse.longitude,
								"max_distance_sales":objWarehouse.max_distance_sales,
								"distance":objWarehouse.distance,
								"warehouse_logo":objWarehouse.warehouse_logo,
							})
							warehouse_list.append(warehouse_obj)
				# print("*******************warehouse_id**************")
				# print(warehouse_list)
				isMatch = 'n'
				wMsh = 'Sorry!!! Your delivery address does not belongs to our serviceable area.'
				if warehouse_list and len(warehouse_list)>0:
					for wl in warehouse_list:
						#print('+++++++++++++',int(wl['id']))
						if int(wl['id']) == int(warehouse_id):
							isMatch = "y"
							wMsh = "Warehouse match"
				if int(warehouse_id)==0:
					isMatch = "y"
					wMsh = "Warehouse match"
				if warehouse_list:
					str_status = status.HTTP_200_OK
					data = {
						'status':str_status,
						'warehouseMatch':isMatch,
						'message': 'Address create successfully',
						'message2': wMsh,
						'warehouse_list':warehouse_list,
						'data' : address_data

					}
				else:
					#print("*********************elsessssss******")
					str_status = status.HTTP_200_OK
					data = {
						'status':str_status,
						'warehouseMatch':'n',
						'message':'Address create successfully',
						'message2': 'Sorry!!! Your delivery address does not belongs to our serviceable area.',
						'warehouse_list' : warehouse_list,
						'data' : address_data
					}

			else:
				#print("*********************else******")
				str_status = status.HTTP_200_OK
				data = {
					"status":str_status,
					'warehouseMatch':'n',
					'message': 'Address create successfully',
					'message2': 'Sorry!!! Your delivery address does not belongs to our serviceable area.',
					'warehouse_list' : warehouse_list,
					'data' : address_data
				}

			# if address_data:
			#     str_status = status.HTTP_200_OK
			#     data = {
			#         'status':str_status,
			#         'message': 'Address create successfully',
			#         'data' : address_data
			#         }

		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			str_status = status.HTTP_417_EXPECTATION_FAILED
			data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
		return Response (data,str_status)

	def put(self, request, format=None):
		requestdata            =  JSONParser().parse(request)
		user                   =  request.user
		user_id                =  user.id
		customers_addressId    =  requestdata['customers_addressId']
		name                   =  requestdata['name']
		address                =  requestdata['address']
		area =None
		if "area" in requestdata and requestdata['area'] !='':
			area               =  requestdata['area']
		# landmark               =  requestdata['landmark']
		country = None
		if "country" in requestdata and requestdata['country'] != '':
			country                =  requestdata['country']
		city =None
		if "city" in requestdata and requestdata['city'] !='':
			city               =  requestdata['city']
		#city                   =  requestdata['city']
		mobile_no              =  requestdata['mobile_no']

		state = None
		if "state" in requestdata and requestdata['state'] !='':
			state                  =  requestdata['state']

		pincode = None

		if "pincode" in requestdata and requestdata['pincode'] !='':
			pincode                =  requestdata['pincode']

		alternative_mobile_no = None
		if "alternative_mobile_no" in requestdata:
			alternative_mobile_no  =  requestdata['alternative_mobile_no']

		check                  =  requestdata['check']
		website_id = request.META.get('HTTP_WID')
		warehouse_id     = request.META.get('HTTP_WAREHOUSE')
		str_status = ""

		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		if website_id is None:
			website_id = 1
		if website_id<=0:
			website_id = 1
		try:
			rs_customer = EngageboostCustomers.objects.filter(auth_user_id = user_id,isblocked='n',isdeleted='n').first()
			if rs_customer:
				customer_id = rs_customer.id
			else:
				raise Exception("Customer Not Found.")
			if customers_addressId=='':
				raise Exception("customers address id is required")
			if name=='':
				raise Exception("name is required")
			if address=='':
				raise Exception("address is required")
			# if country=='':
			# 	raise Exception("country is required")
			# if state=='':
				raise Exception("state is required")
			if mobile_no=='':
				raise Exception("mobile no is required")
			# if check=='':
			#     raise Exception("check is required")
			rs_user = EngageboostUsers.objects.filter(id=user_id,isblocked='n',isdeleted='n').first()
			user_email = None
			if rs_user:
				user_email = rs_user.email

			#name = first_name + " " + last_name
			#------Binayak Start 12-02-2021------#
			rs_objWarehouse = {}


			# if state != None and country != None:
			# 	geo_location = get_geo_location(address,city,area,country,state, pincode)
			# 	latitude  = geo_location["lat"]
			# 	longitude = geo_location["lng"]
			# 	# print('latitude',latitude)
			# 	# print('longitude',longitude)
			# else:
			# 	geo_location_reverse = get_geo_location_reverse(latitude, longitude)
			# 	print("=======here adding========")
			# 	# return Response(geo_location_reverse)
			# 	city = geo_location_reverse["city"]
			# 	state = geo_location_reverse["state"]
			# 	country = geo_location_reverse["country"]


			if state != None and country != None:
				geo_location = get_geo_location(address,city,area,country,state, pincode)
				latitude = geo_location["lat"]
				longitude = geo_location["lng"]
			else:
				get_address = EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id, isblocked='n',
															   isdeleted='n').first()
				if get_address:
					latitude = get_address.lat_val
					longitude = get_address.long_val
			#------Binayak End 12-02-2021------#

			warehouse_list = []

			# print('latitude',latitude)
			# print('longitude',longitude)
			radlat      = Radians(float(latitude))
			radlong     = Radians(float(longitude))
			radflat     = Radians(Cast(F('latitude'), FloatField()))
			radflong    = Radians(Cast(F('longitude'), FloatField()))
			Expression = 111.045 * Degrees(Acos(Cos(radlat) * Cos(radflat) * Cos(radflong - radlong) + Sin(radlat) * Sin(radflat)))
			rs_objWarehouse = EngageboostWarehouseMasters.objects.annotate(distance=Expression).filter(website_id=website_id, isblocked='n', isdeleted='n').exclude(latitude__isnull=True,longitude__isnull=True).order_by('distance')
			#print(rs_objWarehouse.query)
			#if check==1:
			cntprimary=EngageboostCustomersAddressBook.objects.filter(set_primary=1,customers_id=customer_id,isblocked='n',isdeleted='n').count()
			if cntprimary>0:
				#-------Binayak Start 12-02-2021-------#
				if country != None and state != None:
					setprimary_update=EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,set_primary=check,isblocked='n',isdeleted='n').update(set_primary=0)
					address_update=EngageboostCustomersAddressBook.objects.filter(isblocked='n',isdeleted='n',id=customers_addressId).update(
						set_primary = check,
						delivery_name = name,
						delivery_email_address = user_email,
						delivery_street_address = address,
						delivery_landmark = area,
						delivery_country = country,
						delivery_city = city,
						delivery_state = state,
						delivery_postcode = pincode,
						delivery_phone = mobile_no,
						delivery_fax = alternative_mobile_no,
						billing_name = name,
						billing_email_address = user_email,
						billing_street_address = address,
						billing_landmark = area,
						billing_country = country,
						billing_city = city,
						billing_state = state,
						billing_postcode = pincode,
						billing_phone = mobile_no,
						billing_fax = alternative_mobile_no,
						modified = now_utc,
						# lat_val = geo_location["lat"],
						# long_val = geo_location["lng"]
						lat_val=latitude,
						long_val=longitude
						)
					count_primary = EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,set_primary=1,isblocked='n',isdeleted='n').count()
					if count_primary==0:
						next_id = EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,isdeleted='n',isblocked='n').exclude(id =customers_addressId).first()
						addressid= next_id.id
						EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,id=addressid,isblocked='n',isdeleted='n').update(set_primary=1)
				else:
					setprimary_update = EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,
																					   set_primary=check, isblocked='n',
																					   isdeleted='n').update(
						set_primary=0)
					address_update = EngageboostCustomersAddressBook.objects.filter(isblocked='n', isdeleted='n',
																					id=customers_addressId).update(
						set_primary=check,
						delivery_name=name,
						delivery_email_address=user_email,
						delivery_street_address=address,
						delivery_landmark=area,
						# delivery_country=country,
						delivery_city=city,
						# delivery_state=state,
						delivery_postcode=pincode,
						delivery_phone=mobile_no,
						delivery_fax=alternative_mobile_no,
						billing_name=name,
						billing_email_address=user_email,
						billing_street_address=address,
						billing_landmark=area,
						# billing_country=country,
						billing_city=city,
						# billing_state=state,
						billing_postcode=pincode,
						billing_phone=mobile_no,
						billing_fax=alternative_mobile_no,
						modified=now_utc,
						# lat_val=geo_location["lat"],
						# long_val=geo_location["lng"]
						lat_val=latitude,
						long_val=longitude
					)
					count_primary = EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,
																				   set_primary=1, isblocked='n',
																				   isdeleted='n').count()
					if count_primary == 0:
						next_id = EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,
																				 isdeleted='n', isblocked='n').exclude(
							id=customers_addressId).first()
						addressid = next_id.id
						EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id, id=addressid,
																	   isblocked='n', isdeleted='n').update(
							set_primary=1)
				# -------Binayak End 12-02-2021-------#
			else:
				# -------Binayak Start 12-02-2021-------#
				if country != None and state != None:
					address_update=EngageboostCustomersAddressBook.objects.filter(isblocked='n',isdeleted='n',id=customers_addressId).update(
						set_primary = check,
						delivery_name = name,
						delivery_email_address = user_email,
						delivery_street_address = address,
						delivery_landmark = area,
						delivery_country = country,
						delivery_city = city,
						delivery_state = state,
						delivery_postcode = pincode,
						delivery_phone = mobile_no,
						delivery_fax = alternative_mobile_no,
						billing_name = name,
						billing_email_address = user_email,
						billing_street_address = address,
						billing_landmark = area,
						billing_country = country,
						billing_city = city,
						billing_state = state,
						billing_postcode = pincode,
						billing_phone = mobile_no,
						billing_fax = alternative_mobile_no,
						modified = now_utc,
						# lat_val = geo_location["lat"],
						# long_val = geo_location["lng"]
						lat_val = latitude,
						long_val = longitude
						)
					count_primary = EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,set_primary=1,isblocked='n',isdeleted='n').count()
					if count_primary==0:
						next_id = EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,isdeleted='n',isblocked='n').exclude(id=customers_addressId).first()
						addressid= next_id.id
						EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,id=addressid,isblocked='n',isdeleted='n').update(set_primary=1)
				else:
					address_update = EngageboostCustomersAddressBook.objects.filter(isblocked='n', isdeleted='n',
																					id=customers_addressId).update(
						set_primary=check,
						delivery_name=name,
						delivery_email_address=user_email,
						delivery_street_address=address,
						delivery_landmark=area,
						# delivery_country=country,
						delivery_city=city,
						# delivery_state=state,
						delivery_postcode=pincode,
						delivery_phone=mobile_no,
						delivery_fax=alternative_mobile_no,
						billing_name=name,
						billing_email_address=user_email,
						billing_street_address=address,
						billing_landmark=area,
						# billing_country=country,
						billing_city=city,
						# billing_state=state,
						billing_postcode=pincode,
						billing_phone=mobile_no,
						billing_fax=alternative_mobile_no,
						modified=now_utc,
						# lat_val=geo_location["lat"],
						# long_val=geo_location["lng"]
						lat_val=latitude,
						long_val=longitude
					)
					count_primary = EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,
																				   set_primary=1, isblocked='n',
																				   isdeleted='n').count()
					if count_primary == 0:
						next_id = EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id,
																				 isdeleted='n', isblocked='n').exclude(
							id=customers_addressId).first()
						addressid = next_id.id
						EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id, id=addressid,
																	   isblocked='n', isdeleted='n').update(
							set_primary=1)

			if address_update:
				if len(rs_objWarehouse)>0:
				# objWarehouse = objWarehouse.first()
					for objWarehouse in rs_objWarehouse:
						warehouse_obj = {}
						if objWarehouse.max_distance_sales:
							max_distance_salesKM = objWarehouse.max_distance_sales*1.60934
							if objWarehouse.distance <= max_distance_salesKM:
								warehouse_obj.update({
									"id":objWarehouse.id,
									"website_id":objWarehouse.website_id,
									"name":objWarehouse.name,
									"code":objWarehouse.code,
									"address":objWarehouse.address,
									"country_id":objWarehouse.country_id,
									"state_id":objWarehouse.state_id,
									"state_name":objWarehouse.state_name,
									"city":objWarehouse.city,
									"zipcode":objWarehouse.zipcode,
									"phone":objWarehouse.phone,
									"email":objWarehouse.email,
									"channel_id":objWarehouse.channel_id,
									"latitude":objWarehouse.latitude,
									"longitude":objWarehouse.longitude,
									"max_distance_sales":objWarehouse.max_distance_sales,
									"distance":objWarehouse.distance,
									"warehouse_logo":objWarehouse.warehouse_logo,
								})
								warehouse_list.append(warehouse_obj)
					# print("*******************warehouse_id**************")
					# print(warehouse_list)
					isMatch = 'n'
					wMsh = 'Sorry!!! Your delivery address does not belongs to our serviceable area.'
					if warehouse_list and len(warehouse_list)>0:
						for wl in warehouse_list:
							#print('+++++++++++++',int(wl['id']))
							if int(wl['id']) == int(warehouse_id):
								isMatch = "y"
								wMsh = "Warehouse match"
					if int(warehouse_id) == 0:
						isMatch = "y"
						wMsh = "Warehouse match"
					if warehouse_list:
						str_status = status.HTTP_200_OK
						data = {
							'status':str_status,
							'warehouseMatch':isMatch,
							'message': 'Address update successfully',
							'message2': wMsh,
							'warehouse_list':warehouse_list,
							#'data' : address_data

						}
					else:
						#print("*********************elsessssss******")
						str_status = status.HTTP_200_OK
						data = {
							'status':str_status,
							'warehouseMatch':'n',
							'message':'Address update successfully',
							'message2': 'Sorry!!! Your delivery address does not belongs to our serviceable area.',
							'warehouse_list' : warehouse_list,
							#'data' : address_data
						}
				else:
					#print("*********************else******")
					str_status = status.HTTP_200_OK
					data = {
						"status":str_status,
						'warehouseMatch':'n',
						'message': 'Address update successfully',
						'message2': 'Sorry!!! Your delivery address does not belongs to our serviceable area.',
						'warehouse_list' : warehouse_list,
						#'data' : address_data
					}
				# str_status = status.HTTP_200_OK
				# data = {
				#     'status':str_status,
				#     'message': 'Address update successfully.',
				#     }
			else:
				str_status = status.HTTP_204_NO_CONTENT
				data = {
				'status':str_status,
				'message': 'update failed',
				}

		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			str_status = status.HTTP_417_EXPECTATION_FAILED
			data = {"status":str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
		return Response (data,str_status)

	def patch(self, request, format=None):
		user = request.user
		user_id = user.id
		requestdata =  JSONParser().parse(request)

		addressId = None
		if "addressId" in requestdata:
			addressId = requestdata['addressId']
		if addressId == '' or addressId == None:
			raise Exception("addressId is required")
		try:
			rs_customer = EngageboostCustomers.objects.filter(auth_user_id = user_id, isblocked = 'n', isdeleted = 'n').first()

			# print('rs_customer++++', rs_customer.query)
			if rs_customer:
				customer_id = rs_customer.id
			else:
				raise Exception("Customer Not Found.")
			EngageboostCustomersAddressBook.objects.filter(isblocked='n',isdeleted='n',customers_id=customer_id).update(set_primary=0, is_selected=0)

			customer_address = EngageboostCustomersAddressBook.objects.filter(isblocked='n',isdeleted='n',customers_id=customer_id, id=addressId)
			# cust_address = customer_address
			customer_address.update(set_primary=1, is_selected=1)
			customer_address = EngageboostCustomersAddressBook.objects.filter(isblocked='n', isdeleted='n',
																			  customers_id=customer_id, id=addressId)

			print('customer_address====>', customer_address.count())

			address_data = CustomersAddressBookSerializer(customer_address, many=True).data

			str_status = status.HTTP_200_OK
			data = {
				"status": str_status,
				"address_data": address_data,
				'message': 'Address set as default successfully',
				# 'warehouse_list': warehouse_list,
				# 'data' : address_data
			}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			str_status = status.HTTP_417_EXPECTATION_FAILED
			data = {"status":str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
		return Response (data,str_status)

class CountriesList(APIView):
    permission_classes = []
    def post(self, request, format=None):
        country_id    =  request.POST.get('country_id')
        country_name  =  request.POST.get('country_name')
        str_status = ""
        try:
            if country_id is not None or country_name is not None:
                qs_countries = EngageboostCountries.objects.filter(isblocked='n',isdeleted='n').filter(Q(id=country_id) | Q(country_name=country_name)).all()
            else:
                qs_countries = EngageboostCountries.objects.filter(isblocked='n',isdeleted='n').all()
            countries_data = EngageboostCountriesSerializer(qs_countries,many=True).data
            
            if countries_data:
                str_status = status.HTTP_200_OK  
                data = {
                    'status':str_status,
                    'data' : countries_data 
                    }
            else:
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                'status':str_status,
                'message': 'No data found.',
                'data':[]
                }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response (data,str_status)

class StatesList(APIView): 
    permission_classes = []
    def post(self, request, format=None):
        country_id    =  request.POST.get('country_id')
        str_status = ""
        try:
            if country_id is not None:
                qs_states = EngageboostStates.objects.filter(country_id=country_id).all()
            else:
                qs_states = EngageboostStates.objects.all()
            states_data = EngageboostStatesSerializer(qs_states,many=True).data
            if states_data:
                str_status = status.HTTP_200_OK  
                data = {
                    'status':str_status,
                    'data' : states_data 
                    }
            else:
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                'status':str_status,
                'message': 'No data found.',
                'data':[]
                }
               
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response (data,str_status)

def get_geo_location(address,city,area,country,state=None, post_code=None):
    import requests
    try:
        address = str(address)+","+str(city)+","+str(area)
        if post_code is not None:
            address = str(address)+","+str(city)+","+str(area)+","+str(post_code)
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
        str_status = status.HTTP_417_EXPECTATION_FAILED
        location = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
    # except:
    #     latitude="22.5427604"
    #     longitude="88.3859595"
    return location

def get_geo_location_reverse(latitude,longitude):
	import requests
	try:

		# api_key = 'AIzaSyDwJfFz9Hyur4RkbEa_Hlt6Fkibr6rYhJo'
		api_key = 'AIzaSyA9eZvR2TXFmzgWnYa1wpjHIOFjb1JG2mw'
		response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng=' + str(latitude) + ',' + str(longitude) + '&key='+api_key + '&language=en')

		country = state = city = area = None
		resp_json_payload = response.json()
		flag = 0

		if 'results' in resp_json_payload:
			if len(resp_json_payload['results'])>0:

				if 'address_components' in resp_json_payload['results'][0]:
					for address_details in resp_json_payload['results'][0]['address_components']:
						for component in address_details:
							if component == 'types':
								if 'country' in address_details[component]:
									# print('======in here========')
									country = address_details['long_name']
								if 'administrative_area_level_1' in address_details[component]:
									# print('======in here========')
									state = address_details['long_name']
								if 'locality' in address_details[component]:
									# print('======in here======== city')
									city = address_details['long_name']
									# print('city', city)
								if 'premise' in address_details[component] or 'establishment' in address_details[component] or 'point_of_interest' in address_details[component]:
									if flag == 0:
										# print('======in here========')
										area = address_details['long_name']
										flag = 1

								# print()
							# if component == '':
							# 		country = resp_json_payload['results'][0]['address_components']['long_name']


		# print('country=========>', country)
		# translator = Translator()
		# from translate import translator
		# print(translator('en', 'zh-TW', 'Hello World!'))
		# print('country=========>', translator.translate('country', dest='ja'))
		# state = translator('ar', 'en', state)[0][0][0]
		# city = translator('ar', 'en', city)[0][0][0]
		print('state=========>', state)
		print('city=========>', city)
		print('area=========>', area)
		if area != None:
			city = city + ', ' + area
		# print('new city=========>', city)
		# if countryObj:
		# 	address = address+","+str(countryObj.country_name)
		country_id = state_id = None
		if country is not None:
			countryObj = EngageboostCountries.objects.filter(country_name=country).first()
			if countryObj:
				country_id = countryObj.id
		if state is not None:
			stateObj = EngageboostStates.objects.filter(state_name=state).first()
			if stateObj:
				state_id = stateObj.id
			else:
				stateObj = EngageboostStates.objects.filter(state_name_ar=state).first()
				if stateObj:
					state_id = stateObj.id



		# resp_json_payload = response.json()
		# geometry = resp_json_payload["results"][0]['geometry']['location']
		location = {"country":country_id,"state":state_id, "city":city, "area":area}
	except Exception as error:
		trace_back = sys.exc_info()[2]
		line = trace_back.tb_lineno
		str_status = status.HTTP_417_EXPECTATION_FAILED
		location = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
	# except:
	#     latitude="22.5427604"
	#     longitude="88.3859595"
	return location

class SelectAddress(APIView): 
    def post(self, request, format=None):
        requestdata            =  JSONParser().parse(request)
        user                   =  request.user
        user_id                =  user.id
        address_id             =  requestdata['address_id']
        website_id             =  request.META.get('HTTP_WID')
        warehouse_id           =  request.META.get('HTTP_WAREHOUSE')
        str_status = ""
        
        try:
            rs_customer = EngageboostCustomers.objects.filter(auth_user_id = user_id,isblocked='n',isdeleted='n').first()
            if rs_customer:
                customer_id = rs_customer.id
            else:
                raise Exception("Customer Not Found.")
            if address_id=='':
                raise Exception("address id is required")

            rs_address = EngageboostCustomersAddressBook.objects.filter(id=address_id,customers_id=customer_id, isblocked = 'n', isdeleted = 'n').first()

            #address_data = CustomersAddressBookSerializer(rs_address).data
            if rs_address:
                warehouse_list = []
                latitude = rs_address.lat_val
                longitude = rs_address.long_val
                # print('latitude',latitude)
                # print('longitude',longitude)
                radlat      = Radians(float(latitude))
                radlong     = Radians(float(longitude))
                radflat     = Radians(Cast(F('latitude'), FloatField()))
                radflong    = Radians(Cast(F('longitude'), FloatField()))
                Expression = 111.045 * Degrees(Acos(Cos(radlat) * Cos(radflat) * Cos(radflong - radlong) + Sin(radlat) * Sin(radflat)))
                rs_objWarehouse = EngageboostWarehouseMasters.objects.annotate(distance=Expression).filter(website_id=website_id, isblocked='n', isdeleted='n').exclude(latitude__isnull=True,longitude__isnull=True).order_by('distance')
                if len(rs_objWarehouse)>0:
                    for objWarehouse in rs_objWarehouse:
                        warehouse_obj = {}
                        if objWarehouse.max_distance_sales:
                            max_distance_salesKM = objWarehouse.max_distance_sales*1.60934
                            if objWarehouse.distance <= max_distance_salesKM:
                                warehouse_obj.update({
                                    "id":objWarehouse.id,
                                    "website_id":objWarehouse.website_id,
                                    "name":objWarehouse.name,
                                    "code":objWarehouse.code,
                                    "address":objWarehouse.address,
                                    "country_id":objWarehouse.country_id,
                                    "state_id":objWarehouse.state_id,
                                    "state_name":objWarehouse.state_name,
                                    "city":objWarehouse.city,
                                    "zipcode":objWarehouse.zipcode,
                                    "phone":objWarehouse.phone,
                                    "email":objWarehouse.email,
                                    "channel_id":objWarehouse.channel_id,
                                    "latitude":objWarehouse.latitude,
                                    "longitude":objWarehouse.longitude,
                                    "max_distance_sales":objWarehouse.max_distance_sales,
                                    "distance":objWarehouse.distance,
                                    "warehouse_logo":objWarehouse.warehouse_logo,
                                })
                                warehouse_list.append(warehouse_obj)
                    # print("*******************warehouse_id**************")
                    # print(warehouse_list)
                    isMatch = 'n'
                    wMsh = 'Sorry!!! Your delivery address does not belongs to our serviceable area.'
                    if warehouse_list and len(warehouse_list)>0:
                        for wl in warehouse_list:
                            #print('+++++++++++++',int(wl['id']))
                            if int(wl['id']) == int(warehouse_id):
                                isMatch = "y"
                                wMsh = "Warehouse match"

                    if warehouse_list:
                        str_status = status.HTTP_200_OK
                        data = {
                            'status':str_status,
                            'warehouseMatch':isMatch,
                            'message': wMsh,
                            # 'warehouse_list':warehouse_list,
                            # 'data' : address_data 

                        }
                    else:
                        #print("*********************elsessssss******")
                        str_status = status.HTTP_200_OK  
                        data = {
                            'status':str_status,
                            'warehouseMatch':'n',
                            'message': 'Sorry!!! Your delivery address does not belongs to our serviceable area.',
                            # 'warehouse_list' : warehouse_list,
                            # 'data' : address_data 
                        }
                
                else:
                    #print("*********************else******")
                    str_status = status.HTTP_200_OK
                    data = {
                        "status":str_status,
                        'warehouseMatch':'n',
                        'message': 'Sorry!!! Your delivery address does not belongs to our serviceable area.',
                    }
            else:
                str_status = status.HTTP_200_OK
                data = {
                'status':str_status,
                'message': 'No data found.',
                'data':[]
                }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response(data)