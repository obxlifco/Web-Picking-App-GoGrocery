from django.shortcuts import render
from rest_framework import generics, permissions, status, views, mixins
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.http import HttpResponseRedirect

# import datetime
import datetime
import time

import django.db.models
from django.db.models import Avg, Max, Min, Sum, Count
from django import template
from django.template import loader
from django.template import Template
from django.core.mail import send_mail
from django.db.models import TimeField
from django.utils import timezone
from datetime import timedelta

# Import Model And Serializer
from webservices.models import *
from frontapp.frontapp_serializers import *
from frontapp.views.product import discount

import json
import base64
import sys,math
import traceback
import requests
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from webservices.views.common import common
from frontapp.views.sitecommon import common_functions
from frontapp.views.cart import loyalty

# from . import CurlClient
REDIRECT_URL = "http://192.168.0.228:8062/api/front/v1/payment-req/"

def PgSettingsDetails(method_id, payment_type_id):
    setings_data =[]
    rs_settings = EngageboostPaymentgatewaySettingInformation.objects.filter(paymentgateway_method_id=method_id, paymentgateway_type_id=payment_type_id, isblocked='n', isdeleted = 'n').all()
    if rs_settings:
        setings_data = PaymentgatewaySettingInformationSerializer(rs_settings, many=True)
        setings_data = setings_data.data

    return setings_data

    # engageboost_paymentgateway_setting_information


# Payment gateway action
def CreatePayment_OldVersion(payment_data):
    settings_data = PgSettingsDetails(51,2)
    base_URL = "https://ap-gateway.mastercard.com/api/rest/version/53"
    merchant_id = "000008047730"
    # if settings_data:
    #     for api_data in settings_data:
    #         if "api_url" in settings_data and settings_data[0]["api_url"]!="" and settings_data[0]["api_url"] is not None:
    #             base_URL = settings_data[0]["api_url"]
            
    #         if "merchant_id" in settings_data and settings_data[0]["merchant_id"]!="" and settings_data[0]["merchant_id"] is not None:
    #             merchant_id = settings_data[0]["merchant_id"]

    #         if "merchant_id" in settings_data and settings_data[0]["merchant_id"]!="" and settings_data[0]["merchant_id"] is not None:
    #             merchant_id = settings_data[0]["merchant_id"]
    
    session_id = "SESSION0002975960201G49568458K4"
    session_data = CreateSession(payment_data['order_id'])
    
    if int(session_data['status'])==1:
        session_id = session_data["response_data"]["session"]["id"]
    data ={
        "apiOperation":"PAY",
        "order":{
            "currency":"AED",
            "amount":payment_data['order_amount']
        },
        "sourceOfFunds":{
            "type":"CARD",
            "provided":{
                "card":{
                    "number":payment_data['card_number'],
                    "expiry":{
                        "month":payment_data['exp_month'],
                        "year":payment_data['exp_year']
                    },
                    "securityCode":payment_data['sec_code']
                }
            }
        },
        "transaction":{
            "frequency":"SINGLE"
        },
        "session":{
            "id":session_id
        }
    }
    try:
        str_link = base_URL+"/merchant/"+str(merchant_id)+"/order/"+str(payment_data['order_id'])+"/transaction/"+str(payment_data['transaction_id'])+"/"
        # print("str_link",str_link)
        headers = {
            "Content-Type":"application/json",
            "Accept": "application/json",
            "Authorization": "Basic bWVyY2hhbnQuMDAwMDA4MDQ3NzMwOjQ3NTk4NzMwMjI3YjhjM2YyYTg1MDYxNmU2NzMzMmI2"
        }
        resp = requests.request("PUT",str_link, data=json.dumps(data),headers=headers)
        # print("pg response",resp.text)
        resp_data = json.loads(resp.text)
       
        data = {
            "status":1,
            "response_data":resp_data,
            "req_data":data
        }
        up_arr = {
            "card_name":session_id
        }
        EngageboostMastercardPgReturnDetails.objects.filter(order_id=payment_data['order_id']).update(**up_arr)
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error),"req_data":data}
        print("Error ==========",data)
    return data


def SuccessPayment(payment_data):
    print("payment_data", payment_data)
    rs_trans = EngageboostMastercardPgReturnDetails.objects.filter(bank_ref_no =payment_data["3DSecureId"] ).first()
    settings_data = PgSettingsDetails(51,2)
    base_URL = "https://ap-gateway.mastercard.com/api/rest/version/53"
    merchant_id = "000008047730"   
    
    data ={
        "apiOperation":"PAY",
        "3DSecureId" : payment_data["3DSecureId"],
        "order":{
            "currency":"AED",
            "amount":rs_trans.amount
        },       
        "transaction":{
            "frequency":"SINGLE"
        },
        "session":{
            "id":rs_trans.card_name
        }
        # "authentication":{
        #     "3ds":{
        #         "acsEci":payment_data["3DSecure"]["acsEci"],
        #         "authenticationToken":payment_data["3DSecure"]["authenticationToken"],
        #         "transactionId":payment_data["3DSecure"]["xid"]

        #     }
        # }

    }
    dataxx=json.dumps(data)
    print("HGFHGHFHHGHFH", dataxx)
    try:
        str_link = base_URL+"/merchant/"+str(merchant_id)+"/order/"+str(rs_trans.order_id)+"/transaction/"+str(rs_trans.id)+"/"
        headers = {
            "Content-Type":"application/json",
            "Accept": "application/json",
            "Authorization": "Basic bWVyY2hhbnQuMDAwMDA4MDQ3NzMwOjQ3NTk4NzMwMjI3YjhjM2YyYTg1MDYxNmU2NzMzMmI2"
        }
        resp = requests.request("PUT",str_link, data=json.dumps(data),headers=headers)
        # print("pg response",resp.text)
        resp_data = json.loads(resp.text)
        print("success payment", resp_data)
        data = {
            "status":1,
            "response_data":resp_data,
            "req_data":data,
            "order_id":rs_trans.order_id,
            "order_amount":rs_trans.amount
        }
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error),"req_data":data, "order_id":rs_trans.order_id}
        print("Error ==========",data)
    return data

def CreatePayment(payment_data):
    settings_data = PgSettingsDetails(51,2)
    base_URL = "https://ap-gateway.mastercard.com/api/rest/version/53"
    merchant_id = "000008047730"
    # ***********     CREATE SESSION ************
    # session_id = "SESSION0002975960201G49568458K4"
    # session_data = CreateSession(payment_data['order_id'])
    
    # if int(session_data['status'])==1:
    #     session_id = session_data["response_data"]["session"]["id"]
    data ={
        "apiOperation":"PAY",
        "order":{
            "currency":"AED",
            "amount":payment_data['order_amount']
        },
        "sourceOfFunds":{
            "type":"CARD",
            "provided":{
                "card":{
                    "number":payment_data['card_number'],
                    "expiry":{
                        "month":payment_data['exp_month'],
                        "year":payment_data['exp_year']
                    },
                    "securityCode":payment_data['sec_code']
                }
            }
        },
        "transaction":{
            "frequency":"SINGLE"
        },
        "session":{
            "id":session_id
        }
    }
    try:
        str_link = base_URL+"/merchant/"+str(merchant_id)+"/order/"+str(payment_data['order_id'])+"/transaction/"+str(payment_data['transaction_id'])+"/"
        # print("str_link",str_link)
        headers = {
            "Content-Type":"application/json",
            "Accept": "application/json",
            "Authorization": "Basic bWVyY2hhbnQuMDAwMDA4MDQ3NzMwOjQ3NTk4NzMwMjI3YjhjM2YyYTg1MDYxNmU2NzMzMmI2"
        }
        resp = requests.request("PUT",str_link, data=json.dumps(data),headers=headers)
        # print("pg response",resp.text)
        resp_data = json.loads(resp.text)
       
        data = {
            "status":1,
            "response_data":resp_data,
            "req_data":data
        }
        up_arr = {
            "card_name":session_id
        }
        EngageboostMastercardPgReturnDetails.objects.filter(order_id=payment_data['order_id']).update(**up_arr)
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error),"req_data":data}
        print("Error ==========",data)
    return data

def CreateTransaction(order_id):
    # Testing
    order_id = order_id
    rs_order    = EngageboostOrdermaster.objects.filter(id=order_id).first() 
    order_data  = ViewOrderSerializer(rs_order)
    order_data  = order_data.data
    transaction_arr = {
        "website_id":1,
        "order_id":order_id,
        "currency":"AED",
        "amount":order_data['net_amount'],
        "billing_name":order_data['billing_name'],
        "billing_address":order_data['billing_street_address'],
        "billing_city":order_data['billing_city'],
        "billing_state":order_data['billing_state_name'],
        "billing_zip":order_data['billing_postcode'],
        "billing_country":order_data['billing_country_name'],
        "billing_tel":order_data['billing_phone'],
        "billing_email":order_data['billing_email_address'],
        "delivery_name":order_data['delivery_name'],
        "delivery_address":order_data['delivery_street_address'],
        "delivery_city":order_data['delivery_city'],
        "delivery_state":order_data['delivery_state_name'],
        "delivery_zip":order_data['delivery_postcode'],
        "delivery_country":order_data['delivery_country_name'],
        "delivery_tel":order_data['delivery_phone']
    }

    rs_trans = EngageboostMastercardPgReturnDetails.objects.filter(order_id=order_id).first()
    insert_id = 0
    if rs_trans:
        rs_record = EngageboostMastercardPgReturnDetails.objects.filter(order_id=order_id).update(**transaction_arr)
        insert_id = rs_record
    else:
        transaction_arr.update({"order_status":"pending"})
        rs_record = EngageboostMastercardPgReturnDetails.objects.filter(order_id=order_id).create(**transaction_arr)
        insert_id = rs_record.id
    data = {
        "customer_id":order_data['customer']['id'],
        "custom_order_id":order_data['custom_order_id'],
        "transaction_id":insert_id,
        "order_amount":order_data['net_amount']
    }
    return data

def UpdateOrdermasterElastic(update_data):
    customer_id = update_data['customer_id']
    order_id    = update_data['custom_order_id']
    rs_check    = EngageboostOrdermaster.objects.filter(customer_id=update_data['customer_id'], custom_order_id=update_data['custom_order_id']).first()
    now_utc     = datetime.now(timezone.utc).astimezone()
    
    has_customer = EngageboostCustomers.objects.filter(id=customer_id).first()
    user_id = has_customer.auth_user_id

    if rs_check:
        # update shipment and picklist status
        shipment_order_id   = rs_check.id
        shipment_id         = rs_check.shipment_id
        trent_picklist_id   = rs_check.trent_picklist_id
        
        if shipment_id > 0 and shipment_order_id > 0:
            # check already paid
            rs_ship = EngageboostShipments.objects.filter(id=shipment_id).first()
            # if rs_ship and rs_ship.shipment_status != 'Invoicing':Packed
            if rs_ship and rs_ship.shipment_status != 'Invoicing':
                str_status = status.HTTP_200_OK
                msg= "Payment Already done."
            else:
                if update_data and update_data['payment_status']>0:
                    EngageboostTrentPicklists.objects.filter(id=trent_picklist_id,picklist_status='Invoicing').update(picklist_status='Packed')
                    EngageboostShipmentOrders.objects.filter(order_id=shipment_order_id,shipment=shipment_id,shipment_status='Invoicing').update(shipment_status='Packed')
                    EngageboostShipments.objects.filter(id=shipment_id).update(shipment_status='Packed')

                    # update shipment and picklist status
                    str_status = status.HTTP_200_OK
                    update_arr = {
                        "payment_method_id":51,
                        "payment_type_id":2,
                        "payment_method_name":"Credit / Debit Card",
                        "pay_txntranid":update_data['pay_txntranid'],
                        "pay_txndate":now_utc,
                        "received_status":update_data['received_status'],
                        "paid_amount":update_data['paid_amount'],
                    }
                    rs_order_count = EngageboostOrdermaster.objects.filter(custom_order_id=order_id, order_status = 999, buy_status=0).count()
                    if rs_order_count>0:
                        update_arr.update({"order_status":100,"buy_status":1})

                    EngageboostOrdermaster.objects.filter(customer_id=customer_id, custom_order_id=order_id).update(**update_arr)
                    msg= "Payment create successfully."
                    loyalty.EarnCreditPoints(rs_check.id, user_id, 1)   
                    # elastic = common.save_data_to_elastic(rs_check.id,'EngageboostOrdermaster')
                    elastic_update_arr = {
                        "payment_method_id":51,
                        "payment_type_id":2,
                        "payment_method_name":"Credit / Debit Card",
                        "pay_txntranid":update_data['pay_txntranid'],
                        # "pay_txndate":now_utc,
                        "received_status":update_data['received_status'],
                        "paid_amount":update_data['paid_amount'],
                        "shipping_status":"Packed"
                    }
                    if rs_order_count>0:
                        elastic_update_arr.update({"order_status":100,"buy_status":1})
                   
                    elastic = common.change_field_value_elastic(rs_check.id,'EngageboostOrdermaster',elastic_update_arr)
                    # email to customer after order approval...
                    common.email_send_by_AutoResponder(rs_check.id, 12)
                    # email to customer after order approval...
                else:    # Fail
                    str_status = status.HTTP_200_OK
                    update_arr = {
                        "payment_method_id":51,
                        "payment_type_id":2,
                        "payment_method_name":"Credit / Debit Card",
                        "pay_txndate":now_utc,
                        "received_status":update_data['received_status'],
                        "order_status":999,
                        "buy_status":0
                    }
                    EngageboostOrdermaster.objects.filter(customer_id=customer_id, custom_order_id=order_id).update(**update_arr)
                    msg= "Payment Unsuccessful."

                    # elastic = common.save_data_to_elastic(rs_check.id,'EngageboostOrdermaster')
                    elastic_update_arr = {
                        "payment_method_id":51,
                        "payment_type_id":2,
                        "payment_method_name":"Credit / Debit Card",
                        "shipping_status":"Packed",
                        "order_status":999,
                        "buy_status":0
                    }
                    elastic = common.change_field_value_elastic(rs_check.id,'EngageboostOrdermaster',elastic_update_arr)

                    # email to customer after order fail...
                    common.email_send_by_AutoResponder(rs_check.id, 25)
                    # email to customer after order fail...
        else:
            str_status = status.HTTP_200_OK
            msg= "Your Order Is not approved yet."
    else:
        str_status = status.HTTP_401_UNAUTHORIZED
        msg= "You are not allowed to make this payment."
    data = {
        "order_id":order_id,
        "status":str_status,
        "msg":msg
    }

class MakePayment_OldVersion(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        requestdata         = request.data
        device_id           = request.META.get('HTTP_DEVICEID')
        warehouse_id        = request.META.get('HTTP_WAREHOUSE')
        order_id            = requestdata['order_id']
        payment_method_id   = requestdata["payment_method_id"]      # 51 = Credit / Debit Card / Net Banking
        payment_type_id     = requestdata["payment_type_id"]        # 2 = Credit Card Payment Gateways
        payment_method_name = requestdata["payment_method_name"]    # Credit / Debit Card / Net Banking

        card_number = requestdata["card_number"]
        exp_month   = requestdata["exp_month"]
        exp_year    = requestdata["exp_year"]
        sec_code    = requestdata["sec_code"]
        pay_status  = ""
        currency_code = "AED"
        now_utc = datetime.now(timezone.utc).astimezone()
        # Create Transaction
        traction_data = CreateTransaction(order_id)
        # print("traction_data", traction_data)
        payment_data    = {}
        trans_resp      = {}
        if traction_data['transaction_id'] >0 and float(traction_data['order_amount'])>0:
            payment_data = {
                "card_number":card_number,
                "exp_month":exp_month,
                "exp_year":exp_year,
                "sec_code":sec_code,
                "order_id":order_id,
                "currency_code":currency_code,
                "order_amount":traction_data['order_amount'],
                "transaction_id":traction_data['transaction_id']            
            }
            
            # Move to Payment gateway
            trans_resp = CreatePayment(payment_data)

            if trans_resp['status']==1 and "response_data" in trans_resp:
                response_data = trans_resp["response_data"]
                if response_data["result"].lower() == "success":   # Payment Success
                    pay_status = status.HTTP_200_OK
                    update_arr = {
                        "tracking_id":response_data['transaction']['receipt'],
                        "order_status":response_data['response']['gatewayCode'],
                        "payment_mode":response_data['sourceOfFunds']['type'],
                        "status_code":response_data['response']['acquirerCode'],
                        "status_message":response_data['response']['acquirerMessage']
                    }

                    update_ordermaster = {
                        "order_id":order_id,
                        "custom_order_id":traction_data['custom_order_id'],
                        "customer_id":traction_data['customer_id'],
                        "pay_txntranid":response_data['transaction']['receipt'],
                        "received_status":"Payment Ok",
                        "paid_amount":traction_data['order_amount'],
                        "pay_txndate":now_utc,
                        "payment_status":1
                    }
                else:    # Payment fail
                    pay_status = status.HTTP_417_EXPECTATION_FAILED
                    error = {}
                    if "risk" in response_data:
                        error = {
                            "cause":response_data['risk']['response']['gatewayCode'],
                            "explanation":response_data['risk']['response']['gatewayCode'] + " (Payment Failed.)"
                        }
                    if "error" in response_data:
                        update_arr = {
                            "order_status":"failed",
                            "status_code":response_data['error']['validationType'],
                            "status_message":response_data['error']['explanation'],
                        }
                    else:
                        response_data.update({"error":error})
                        response_data.pop("result")
                        response_data.update({"result":"ERROR"})
                        update_arr = {
                            "order_status":"failed",
                            "status_code":response_data["order"]['status'],
                            "status_message":response_data['response']['gatewayCode'],
                        }
                    update_ordermaster = {
                        "order_id":order_id,
                        "custom_order_id":traction_data['custom_order_id'],
                        "customer_id":traction_data['customer_id'],
                        "received_status":"Payment Failed",
                        "pay_txndate":now_utc,
                        "payment_status":0
                    }
                UpdateOrdermasterElastic(update_ordermaster)
                check_exist = EngageboostMastercardPgReturnDetails.objects.filter(order_id=order_id).last()
                if check_exist:
                    if str(check_exist.order_status).lower() == 'approved':
                        pass
                    else:
                        rs_record = EngageboostMastercardPgReturnDetails.objects.filter(order_id=order_id).update(**update_arr)
                else:
                    rs_record = EngageboostMastercardPgReturnDetails.objects.filter(order_id=order_id).update(**update_arr)
            else:
                pay_status = status.HTTP_417_EXPECTATION_FAILED
                trans_resp = {}
        else:
            pay_status = status.HTTP_204_NO_CONTENT
        
        data = {
            "status":pay_status,
            "response":trans_resp['response_data']
        }
        return Response(data,pay_status)

class MakePayment(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        requestdata         = request.data
        device_id           = request.META.get('HTTP_DEVICEID')
        warehouse_id        = request.META.get('HTTP_WAREHOUSE')
        order_id            = requestdata['order_id']
        payment_method_id   = requestdata["payment_method_id"]      # 51 = Credit / Debit Card / Net Banking
        payment_type_id     = requestdata["payment_type_id"]        # 2 = Credit Card Payment Gateways
        payment_method_name = requestdata["payment_method_name"]    # Credit / Debit Card / Net Banking
        device_type = None
        if "device_type" in requestdata:
            device_type = requestdata["device_type"]

        card_number = requestdata["card_number"]
        exp_month   = requestdata["exp_month"]
        exp_year    = requestdata["exp_year"]
        sec_code    = requestdata["sec_code"]
        pay_status  = ""
        currency_code = "AED"
        now_utc = datetime.now(timezone.utc).astimezone()
        # Create Transaction
        traction_data = CreateTransaction(order_id)
        # print("traction_data", traction_data)
        payment_data    = {}
        trans_resp      = {}
        res_3d = {}
        if traction_data['transaction_id'] >0 and float(traction_data['order_amount'])>0:
            payment_data = {
                "card_number":card_number,
                "exp_month":exp_month,
                "exp_year":exp_year,
                "sec_code":sec_code,
                "order_id":order_id,
                "currency_code":currency_code,
                "order_amount":traction_data['order_amount'],
                "transaction_id":traction_data['transaction_id']            
            }
            
            # **********  Create and upadate Session **************
            session_id          = "SESSION0002975960201G49568458K4"
            session_data        = CreateSession(payment_data['order_id'])
            
            if int(session_data['status'])==1:
                session_id          = session_data["response_data"]["session"]["id"]
                payment_data.update({"session_id":session_id})
                update_session_data = UpdateSession(payment_data)

                data_3d = {
                    "order_id":order_id,
                    "order_amount":traction_data['order_amount'],
                    "currency_code":currency_code,
                    "session_id":session_id
                }
                res_3d = Enroll3Ds(data_3d)

                print("Response 3d====", res_3d)

               
                if res_3d['status']==0:
                    message = "Card Not Accepted"
                    pay_status = status.HTTP_406_NOT_ACCEPTABLE
                    if device_type is not None and device_type.lower() == "mob":
                        data = {
                            "status":pay_status,
                            "response":res_3d,
                            "session_id":session_id,
                            "message":message
                        }
                        return Response(data)
                    else:
                        return HttpResponseRedirect(redirect_to="https://www.gogrocery.ae/cancell-payment")
                else:
                    pay_status = status.HTTP_200_OK
                    message = "3D Check Successfull."
                    
            else:
                message = "Card Not Accepted"
                pay_status = status.HTTP_406_NOT_ACCEPTABLE
                if device_type is not None and device_type.lower() == "mob":
                    data = {
                        "status":pay_status,
                        "response":res_3d,
                        "session_id":session_id,
                        "message":message
                    }
                    return Response(data)
                else:
                    return HttpResponseRedirect(redirect_to="https://www.gogrocery.ae/cancell-payment")
            # Move to Payment gateway
            # trans_resp = CreatePayment(payment_data)
        else:
            message = "Card Not Accepted"
            pay_status = pay_status = status.HTTP_406_NOT_ACCEPTABLE
            if device_type is not None and device_type.lower() == "mob":
                data = {
                    "status":pay_status,
                    "response":res_3d,
                    "session_id":session_id,
                    "message":message
                }
                return Response(data)
            else:
                return HttpResponseRedirect(redirect_to="https://www.gogrocery.ae/cancell-payment")
        
        data = {
            "status":pay_status,
            "response":res_3d,
            "session_id":session_id,
            "message":message
        }
        # pay_status = status.HTTP_200_OK
        return Response(data,pay_status)

def GetOrderDetails(order_id):
    rs_order    = EngageboostOrdermaster.objects.filter(id=order_id).first() 
    order_data = []
    status = 0
    if rs_order:
        order_data  = ViewOrderSerializer(rs_order)
        order_data  = order_data.data
        status = 1
    data = {
        "status":1,
        "order_data":order_data
    }
    return data

def CreateSession(order_id):
    # settings_data = PgSettingsDetails(51,2)
    base_URL = "https://ap-gateway.mastercard.com/api/rest/version/53"
    merchant_id = "000008047730"   
    data ={
        "apiOperation":"CREATE_CHECKOUT_SESSION",
        "interaction":{
		    "operation":"VERIFY"
	    },
        "order":{
            "currency":"AED",
            "id":order_id
        }
    }
    try:
        str_link = base_URL+"/merchant/000008047730/session/"
        # print("str_link",str_link)
        headers = {
            "Content-Type":"application/json",
            "Accept": "application/json",
            "Authorization": "Basic bWVyY2hhbnQuMDAwMDA4MDQ3NzMwOjQ3NTk4NzMwMjI3YjhjM2YyYTg1MDYxNmU2NzMzMmI2"
        }
        resp = requests.request("POST",str_link, data=json.dumps(data),headers=headers)
        print("pg response",resp.text)
        resp_data = json.loads(resp.text)
       
        data = {
            "status":1,
            "response_data":resp_data
        }
        session_id = resp_data["session"]["id"]
        up_arr = {
            "card_name":session_id
        }
        EngageboostMastercardPgReturnDetails.objects.filter(order_id=order_id).update(**up_arr)
        print("SESSION Created")
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        print("Error ==========",data)
    print("data", data)
    return data

def UpdateSession(request_data):
    print("Update session req data", request_data)
    base_URL = "https://ap-gateway.mastercard.com/api/rest/version/53"
    merchant_id = "000008047730"   
    data ={
        "sourceOfFunds":{
            "type":"CARD",
            "provided":{
                "card":{
                    "number":request_data["card_number"],
                    "expiry":{
                        "month":request_data["exp_month"],
                        "year":request_data["exp_year"]
                    },
                    "securityCode":request_data["sec_code"]
                }
            }
        }
    }
    try:
        str_link = base_URL+"/merchant/000008047730/session/"+request_data["session_id"]
        headers = {
            "Content-Type":"application/json",
            "Accept": "application/json",
            "Authorization": "Basic bWVyY2hhbnQuMDAwMDA4MDQ3NzMwOjQ3NTk4NzMwMjI3YjhjM2YyYTg1MDYxNmU2NzMzMmI2"
        }
        resp = requests.request("PUT",str_link, data=json.dumps(data),headers=headers)
        print("pg response1",resp.text)
        resp_data = json.loads(resp.text)
       
        data = {
            "status":1,
            "response_data":resp_data
        }
        print("SESSION Updates")     
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        print("Error ==========",data)
    print("data", data)

    return data

def Enroll3Ds(requestdata):
    now_utc     = datetime.now(timezone.utc).astimezone()
    now_date = now_utc.strftime("%d%m%Y%H%M%S")
    base_URL = "https://ap-gateway.mastercard.com/api/rest/version/53"
    merchant_id = "000008047730"
    print("requestdata", requestdata)
    data ={	
        "apiOperation":"CHECK_3DS_ENROLLMENT",
        "3DSecure":{
            "authenticationRedirect":{
                "responseUrl":REDIRECT_URL,
                "pageGenerationMode" : "CUSTOMIZED"
            }
        },
        "order":{
            "amount":requestdata["order_amount"],
            "currency":requestdata["currency_code"]
        },
        "session":{
            "id":requestdata["session_id"]
        }
    }
    try:
        str_3d_id = str(now_date)+"_"+str(requestdata['order_id'])
        str_3d_id = str(str_3d_id)
        str_link = base_URL+"/merchant/000008047730/3DSecureId/"+str_3d_id
        # print("str_link",str_link)
        headers = {
            "Content-Type":"application/json",
            "Accept": "application/json",
            "Authorization": "Basic bWVyY2hhbnQuMDAwMDA4MDQ3NzMwOjQ3NTk4NzMwMjI3YjhjM2YyYTg1MDYxNmU2NzMzMmI2"
        }
        up_arr = {
            "bank_ref_no":str_3d_id
        }
        EngageboostMastercardPgReturnDetails.objects.filter(order_id=requestdata['order_id']).update(**up_arr)

        resp = requests.request("PUT",str_link, data=json.dumps(data),headers=headers)
        print("pg response2",resp.text)
        resp_data = json.loads(resp.text)
        if resp_data['3DSecure']['veResEnrolled'] == 'Y' :
            data = {
                "status":1,
                "enroll_data":resp_data
            }
        else:
            data = {
                "status":0,
                "enroll_data":resp_data
            }
       
        #  Need checking if response PROCEED
        # authenticate_data =  {
        #     "paRes":resp_data["3DSecure"]["authenticationRedirect"]["customized"]["paReq"],
        #     "3ds_id":resp_data["3DSecureId"],
        #     "session_id":requestdata["session_id"]
        # }
        # res_acs_result = ProcessAcsResult(authenticate_data)


        # data = {
        #     "status":1,
        #     "enroll_data":resp_data,
        #     "acs_result":res_acs_result
        # }
        

    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        print("Error ==========",data)
    print("data", data)
    return data


def ProcessAcsResult(requestdata):
    now_utc     = datetime.now(timezone.utc).astimezone()
    base_URL = "https://ap-gateway.mastercard.com/api/rest/version/53"
    merchant_id = "000008047730"
    print("requestdata", requestdata)
    data ={	
        "apiOperation":"PROCESS_ACS_RESULT",
        "3DSecure":{
            "paRes":requestdata["paRes"]
        }
    }
    try:
        # rs_trans = EngageboostMastercardPgReturnDetails.objects.filter()
        str_link = base_URL+"/merchant/000008047730/3DSecureId/"+requestdata["3ds_id"]
        headers = {
            "Content-Type":"application/json",
            "Accept": "application/json",
            "Authorization": "Basic bWVyY2hhbnQuMDAwMDA4MDQ3NzMwOjQ3NTk4NzMwMjI3YjhjM2YyYTg1MDYxNmU2NzMzMmI2"
        }
        resp = requests.request("POST",str_link, data=json.dumps(data),headers=headers)
        print("pg response3",resp.text)
        resp_data = json.loads(resp.text)
       
        data = {
            "status":1,
            "response_data":resp_data
        }       
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        print("Error ==========",data)
    print("data", data)
    return data

class getResponseData(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        redirect_to = "https://www.gogrocery.ae"
        requestdata = request.data
        processAcsData = {
            "paRes" : requestdata["PaRes"],
            "3ds_id":requestdata["MD"]
        }
        print("processAcsData", processAcsData)
        data = ProcessAcsResult(processAcsData)

        print('process result response from webhook', data)
        trans_resp = SuccessPayment(data["response_data"])
        response_data = {}
        print("final response", trans_resp)
        now_utc = datetime.now(timezone.utc).astimezone()
        if trans_resp['status']==1 and "response_data" in trans_resp:
            rs_order = EngageboostOrdermaster.objects.filter(id=trans_resp['order_id']).first() 
            response_data = trans_resp["response_data"]
            if response_data["result"].lower() == "success":   # Payment Success
                pay_status = status.HTTP_200_OK
                update_arr = {
                    "tracking_id":response_data['transaction']["acquirer"]["transactionId"],
                    "order_status":response_data['response']['gatewayCode'],
                    "payment_mode":response_data['sourceOfFunds']['type'],
                    "status_code":response_data['response']['acquirerCode'],
                    "status_message":response_data['response']['acquirerMessage']
                }

                update_ordermaster = {
                    "order_id":trans_resp["order_id"],
                    "custom_order_id":rs_order.custom_order_id,
                    "customer_id":rs_order.customer_id,
                    "pay_txntranid":response_data['transaction']["acquirer"]["transactionId"],
                    "received_status":"Payment Ok",
                    "paid_amount":trans_resp['order_amount'],
                    "pay_txndate":now_utc,
                    "payment_status":1
                }
                response_data = {
                    "status":pay_status,
                    "message":response_data['response']['acquirerMessage'],
                    "transaction_id":response_data['transaction']["acquirer"]["transactionId"]
                }
                redirect_to = "https://www.gogrocery.ae/success-payment/"
            else:    # Payment fail
                pay_status = status.HTTP_417_EXPECTATION_FAILED
                error = {}
                if "risk" in response_data:
                    error = {
                        "cause":response_data['risk']['response']['gatewayCode'],
                        "explanation":response_data['risk']['response']['gatewayCode'] + " (Payment Failed.)"
                    }
                if "error" in response_data:
                    update_arr = {
                        "order_status":"failed",
                        "status_code":response_data['error']['validationType'],
                        "status_message":response_data['error']['explanation'],
                    }
                else:
                    response_data.update({"error":error})
                    response_data.pop("result")
                    response_data.update({"result":"ERROR"})
                    update_arr = {
                        "order_status":"failed",
                        "status_code":response_data["order"]['status'],
                        "status_message":response_data['response']['gatewayCode'],
                    }
                update_ordermaster = {
                    "order_id":trans_resp["order_id"],
                    "custom_order_id":rs_order.custom_order_id,
                    "customer_id":rs_order.customer_id,
                    "received_status":"Payment Failed",
                    "pay_txndate":now_utc,
                    "payment_status":0
                }
                response_data = {
                    "status":pay_status,
                    "message":response_data['response']['gatewayCode'] + " (Payment Failed.)",
                    "transaction_id":response_data['transaction']["acquirer"]["transactionId"]
                }
                redirect_to = "https://www.gogrocery.ae/failed-payment/"
            UpdateOrdermasterElastic(update_ordermaster)
            check_exist = EngageboostMastercardPgReturnDetails.objects.filter(order_id=trans_resp["order_id"]).last()
            if check_exist:
                if str(check_exist.order_status).lower() == 'approved':
                    pass
                else:
                    rs_record = EngageboostMastercardPgReturnDetails.objects.filter(order_id=trans_resp["order_id"]).update(**update_arr)
            else:
                rs_record = EngageboostMastercardPgReturnDetails.objects.filter(order_id=trans_resp["order_id"]).update(**update_arr)
        else:
            pay_status = status.HTTP_417_EXPECTATION_FAILED
            trans_resp = {}
        
        data = {
            "status":pay_status,
            "response":trans_resp
        }
        # response_data = str(urlsafe_base64_encode(force_bytes(data)))
        response_data = str(urlsafe_base64_encode(force_bytes(response_data)))
        response_data = response_data.replace("b","")
        response_data = response_data.replace("'","")
        redirect_url = redirect_to+'?res='+response_data
        print("redirect_url================", redirect_url)
        return HttpResponseRedirect(redirect_to=redirect_to+'?res='+response_data)


def checkbase64():
    pay_status = status.HTTP_200_OK
    now_utc = datetime.now(timezone.utc).astimezone()
    
    trans_resp = {
        "status":1,
        "order_id":878,
        "order_amount":0.50,
        "response_data":{
        "amount": 0.5,
        "chargeback": {
            "amount": 0,
            "currency": "AED"
        },
        "creationTime": "2019-12-18T15:45:34.404Z",
        "currency": "AED",
        "id": "878",
        "merchant": "000008047730",
        "merchantCategoryCode": "5411",
        "result": "SUCCESS",
        "sourceOfFunds": {
            "provided": {
            "card": {
                "brand": "VISA",
                "expiry": {
                "month": "10",
                "year": "23"
                },
                "fundingMethod": "CREDIT",
                "issuer": "ICICI BANK, LTD.",
                "number": "437551xxxxxx7007",
                "scheme": "VISA",
                "storedOnFile": "NOT_STORED"
            }
            },
            "type": "CARD"
        },
        "status": "CAPTURED",
        "totalAuthorizedAmount": 0.5,
        "totalCapturedAmount": 0.5,
        "totalRefundedAmount": 0,
        "transaction": [
            {
            "3DSecure": {
                "acsEci": "05",
                "authenticationToken": "AAABAHcAAAUxY5Z0dwAAAAAAAAA=",
                "paResStatus": "Y",
                "veResEnrolled": "Y",
                "xid": "zY3OMnGTuV50QLuHf/WNcu1MyjY="
            },
            "3DSecureId": "18122019154433_878",
            "authorizationResponse": {
                "cardLevelIndicator": "N ",
                "cardSecurityCodeError": "M",
                "commercialCard": "!01",
                "commercialCardIndicator": "0",
                "date": "1218",
                "posData": "1025100006600",
                "posEntryMode": "812",
                "processingCode": "000000",
                "responseCode": "00",
                "returnAci": "M",
                "stan": "26626",
                "time": "154534",
                "transactionIdentifier": "589352567342656",
                "validationCode": "QQ5G",
                "vpasResponse": "2"
            },
            "gatewayEntryPoint": "WEB_SERVICES_API",
            "merchant": "000008047730",
            "order": {
                "amount": 0.5,
                "chargeback": {
                "amount": 0,
                "currency": "AED"
                },
                "creationTime": "2019-12-18T15:45:34.404Z",
                "currency": "AED",
                "id": "878",
                "merchantCategoryCode": "5411",
                "status": "CAPTURED",
                "totalAuthorizedAmount": 0.5,
                "totalCapturedAmount": 0.5,
                "totalRefundedAmount": 0
            },
            "response": {
                "acquirerCode": "00",
                "acquirerMessage": "Approved",
                "cardSecurityCode": {
                "acquirerCode": "M",
                "gatewayCode": "MATCH"
                },
                "gatewayCode": "APPROVED"
            },
            "result": "SUCCESS",
            "sourceOfFunds": {
                "provided": {
                "card": {
                    "brand": "VISA",
                    "expiry": {
                    "month": "10",
                    "year": "23"
                    },
                    "fundingMethod": "CREDIT",
                    "issuer": "ICICI BANK, LTD.",
                    "number": "437551xxxxxx7007",
                    "scheme": "VISA",
                    "storedOnFile": "NOT_STORED"
                }
                },
                "type": "CARD"
            },
            "timeOfRecord": "2019-12-18T15:45:34.404Z",
            "transaction": {
                "acquirer": {
                "batch": 20191218,
                "date": "1218",
                "id": "MASHREQ_S2I",
                "merchantId": "000008047730",
                "settlementDate": "2019-12-18",
                "timeZone": "+0400",
                "transactionId": "589352567342656"
                },
                "amount": 0.5,
                "authorizationCode": "471014",
                "currency": "AED",
                "frequency": "SINGLE",
                "id": "138",
                "receipt": "935215026626",
                "source": "INTERNET",
                "terminal": "MASS2I03",
                "type": "PAYMENT"
            },
            "version": "53"
            }
        ]
        }
    }
    data = {
        "status":pay_status,
        "response":trans_resp
    }
    rs_order = EngageboostOrdermaster.objects.filter(id=trans_resp['order_id']).first() 

    if trans_resp['status']==1 and "response_data" in trans_resp:
        response_data = trans_resp["response_data"]
        if response_data["result"].lower() == "success":   # Payment Success
            pay_status = status.HTTP_200_OK
            update_arr = {
                "tracking_id":response_data['transaction'][0]['transaction']["acquirer"]["transactionId"],
                "order_status":response_data['transaction'][0]['response']['gatewayCode'],
                "payment_mode":response_data['sourceOfFunds']['type'],
                "status_code":response_data['transaction'][0]['response']['acquirerCode'],
                "status_message":response_data['transaction'][0]['response']['acquirerMessage']
            }

            update_ordermaster = {
                "order_id":trans_resp["order_id"],
                "custom_order_id":rs_order.custom_order_id,
                "customer_id":rs_order.customer_id,
                "pay_txntranid":response_data['transaction'][0]['transaction']["acquirer"]["transactionId"],
                "received_status":"Payment Ok",
                "paid_amount":trans_resp['order_amount'],
                "pay_txndate":now_utc,
                "payment_status":1
            }
            redirect_to = "https://www.gogrocery.ae/"
        else:    # Payment fail
            pay_status = status.HTTP_417_EXPECTATION_FAILED
            error = {}
            if "risk" in response_data:
                error = {
                    "cause":response_data['risk']['response']['gatewayCode'],
                    "explanation":response_data['risk']['response']['gatewayCode'] + " (Payment Failed.)"
                }
            if "error" in response_data:
                update_arr = {
                    "order_status":"failed",
                    "status_code":response_data['error']['validationType'],
                    "status_message":response_data['error']['explanation'],
                }
            else:
                response_data.update({"error":error})
                response_data.pop("result")
                response_data.update({"result":"ERROR"})
                update_arr = {
                    "order_status":"failed",
                    "status_code":response_data["order"]['status'],
                    "status_message":response_data['transaction'][0]['response']['gatewayCode'],
                }
            update_ordermaster = {
                "order_id":trans_resp["order_id"],
                "custom_order_id":rs_order.custom_order_id,
                "customer_id":rs_order.customer_id,
                "received_status":"Payment Failed",
                "pay_txndate":now_utc,
                "payment_status":0
            }
            redirect_to = "https://www.gogrocery.ae/"
        UpdateOrdermasterElastic(update_ordermaster)
        check_exist = EngageboostMastercardPgReturnDetails.objects.filter(order_id=trans_resp["order_id"]).last()
        if check_exist:
            if str(check_exist.order_status).lower() == 'approved':
                pass
            else:
                rs_record = EngageboostMastercardPgReturnDetails.objects.filter(order_id=trans_resp["order_id"]).update(**update_arr)
        else:
            rs_record = EngageboostMastercardPgReturnDetails.objects.filter(order_id=trans_resp["order_id"]).update(**update_arr)
    else:
        pay_status = status.HTTP_417_EXPECTATION_FAILED
        trans_resp = {}
    
    data = {
        "status":pay_status,
        "response":trans_resp
    }
    response_data = str(urlsafe_base64_encode(force_bytes(data)))
    response_data = response_data.replace("b","")
    response_data = response_data.replace("'","")
    return HttpResponseRedirect(redirect_to=redirect_to+'?res='+response_data)

# checkbase64()

# GetOrderDetails(451)

def PgTest():
    base_URL = "https://test-gateway.mastercard.com/api/rest/version/53"
    merchant_id = "000008047730"
    data ={
        "apiOperation":"PAY",
        "order":{
            "currency":"AED",
            "amount":150
        },
        "sourceOfFunds":{
            "type":"CARD",
            "provided":{
                "card":{
                    "number":4111111111111111,
                    "expiry":{
                        "month":6,
                        "year":25
                    },
                    "securityCode":123
                }
            }
        }
    }
    try:
        # str_link = base_URL+"/merchant/"+str(merchant_id)+"/balanceInquiry"
        str_link = base_URL+"/merchant/"+str(merchant_id)+"/order/115/transaction/11578/"

        # https://test-gateway.mastercard.com/api/rest/version/53/merchant/000008047730/order/1234/transaction/1234
        # https://test-gateway.mastercard.com/api/rest/version/53/merchant/000008047730/balanceInquiry

        headers = {
            "Content-Type":"application/json",
            "Accept": "application/json",
            "Authorization": "Basic bWVyY2hhbnQuMDAwMDA4MDQ3NzMwOmUxMDYzOGE3YjFjMjJjODdiNTZiODdkMjA4NzE1Mzg5"
        }
        resp = requests.request("PUT",base_URL+"/merchant/"+str(merchant_id)+"/order/4528/transaction/4528/", data=json.dumps(data),headers=headers)
        # print(resp.text)
        data = json.loads(resp.text)
        print(data)
        print("error data",data["error"])

    # except HTTPError as http_err:
    #     pass
    #     # print(f'HTTP error occurred: {http_err}')  # Python 3.6	
        
    except Exception as error:
        print(error)
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        print("Error ==========",data)
    return 0

# PgTest()
