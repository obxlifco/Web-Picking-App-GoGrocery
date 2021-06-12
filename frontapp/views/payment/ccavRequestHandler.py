#!/usr/bin/python
from flask import request, redirect, Flask, render_template
from frontapp.views.payment.ccavutil import encrypt,decrypt
from frontapp.views.payment.ccavResponseHandler import res
from string import Template
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions, status, views, mixins

from webservices.models import *
from frontapp.frontapp_serializers import *
from frontapp.views.payment import paymentgateway as pg
import sys,math
import traceback
from django.utils import timezone
import requests
from webservices.views.common import common

app = Flask('ccavRequestHandler')
base_url = "https://www.gogrocery.ae/"
class CcavenueRequestHandler(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        accessCode = 'AVZO03HA32BC46OZCB'                   # Live
        workingKey = '1D5E76DE84FD6BD8B7708CF1A3A411C0'     # Live
        merchant_id = "46319"                               # Live

        # accessCode = 'AVUP03GL28CI81PUIC'                   # Demo
        # workingKey = '2C469A8EAB648B3516CAFB272D661668'     # Demo
        # merchant_id = "45990"                               # Demo


        requestdata     = request.data
        order_id        = requestdata['order_id']
        order_amount    = requestdata['order_amount']
        str_status = ""
        try:
            if int(order_id)>0:
                rs_order  = EngageboostOrdermaster.objects.filter(id=order_id).first()
            if rs_order:
                order_data = EngageboostOrdermasterSerializers(rs_order)
                order_data = order_data.data
                # Create Transaction
                customer_name = ""
                customer_email = ""
                customer_mobile = ""
                rs_trans_data = pg.CcAvenueCreateTransaction(order_id)
                if order_data["customer_details"] and order_data["customer_details"]["first_name"] is not None:
                    if order_data["customer_details"]["first_name"]!="":
                        customer_name = order_data["customer_details"]["first_name"].strip()

                    customer_name = customer_name + " " + order_data["customer_details"]["last_name"]
                    
                    if order_data["customer_details"]["email"] is not None and order_data["customer_details"]["email"]!="":
                        customer_email = order_data["customer_details"]["email"]
                    else:
                        customer_email = order_data["billing_email_address"]

                    if order_data["customer_details"]["phone"] is not None and order_data["customer_details"]["phone"]!="":
                        customer_mobile = order_data["customer_details"]["phone"]
                    else:
                        customer_mobile = order_data["billing_phone"]

                else:
                    customer_name = order_data["billing_name"]



                # Data for PG
                p_merchant_id       = str(merchant_id)
                p_order_id          = str(order_data["custom_order_id"])
                p_currency          = order_data['currency_code']
                # p_amount            = str(float(order_data['net_amount'])+float(order_data['shipping_cost']))
                p_amount            = str(float(order_data['gross_amount']))
                p_redirect_url      = 'http://157.175.131.51:8062/api/front/v1/payment-response/'
                p_cancel_url        = 'http://157.175.131.51:8062/api/front/v1/payment-response/'
                p_language          = 'EN'
                p_billing_name      = customer_name # order_data["billing_name"]
                p_billing_address   = order_data["billing_street_address"]
                p_billing_city      = order_data["billing_state_name"]
                p_billing_state     = order_data["billing_state_name"]
                p_billing_zip       = ""
                p_billing_country   = order_data["billing_country_name"]
                p_billing_tel       = str(customer_mobile) #str(order_data["billing_phone"])
                p_billing_email     = customer_email # order_data["billing_email_address"]
                p_delivery_name     = order_data["delivery_name"]
                p_delivery_address  = order_data["delivery_street_address"]
                p_delivery_city     = order_data["delivery_state_name"]
                p_delivery_state    = order_data["delivery_state_name"]
                p_delivery_zip      = ""
                p_delivery_country  = order_data["delivery_country_name"]
                p_delivery_tel      = str(order_data["delivery_phone"])
                p_merchant_param1   = str(order_id)
                p_merchant_param2   = str(rs_trans_data["transaction_id"])
                p_merchant_param3   = ""
                p_merchant_param4   = ""
                p_merchant_param5   = ""
                p_promo_code        = ""
                p_customer_identifier = str(order_data["customer"])

                merchant_data='merchant_id='+p_merchant_id+'&'+'order_id='+p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + p_amount+'&'+'redirect_url='+p_redirect_url+'&'+'cancel_url='+p_cancel_url+'&'+'language='+p_language+'&'+'billing_name='+p_billing_name+'&'+'billing_address='+p_billing_address+'&'+'billing_city='+p_billing_city+'&'+'billing_state='+p_billing_state+'&'+'billing_zip='+p_billing_zip+'&'+'billing_country='+p_billing_country+'&'+'billing_tel='+p_billing_tel+'&'+'billing_email='+p_billing_email+'&'+'delivery_name='+p_delivery_name+'&'+'delivery_address='+p_delivery_address+'&'+'delivery_city='+p_delivery_city+'&'+'delivery_state='+p_delivery_state+'&'+'delivery_zip='+p_delivery_zip+'&'+'delivery_country='+p_delivery_country+'&'+'delivery_tel='+p_delivery_tel+'&'+'merchant_param1='+p_merchant_param1+'&'+'merchant_param2='+p_merchant_param2+'&'+'merchant_param3='+p_merchant_param3+'&'+'merchant_param4='+p_merchant_param4+'&'+'merchant_param5='+p_merchant_param5+'&'+'promo_code='+p_promo_code+'&'+'customer_identifier='+p_customer_identifier+'&response_type=JSON&'
                # print("merchant_data==========++++", merchant_data)
                encryption = encrypt(merchant_data,workingKey)

                # return encryption
                # print(encryption)
                # exit(1)
                str_status = status.HTTP_200_OK
                data = {
                    "status":str_status,
                    "enc_value":encryption,
                    "access_code":accessCode
                }

            else:
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                    "status":str_status,
                    "message":"Order Id Not found.",
                    "enc_value":""
                }
        except Exception as error:
            str_status = status.HTTP_417_EXPECTATION_FAILED
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Order Not Found."}
        # print("data=========", data)
        return Response(data)

class CcavenueRequestHandlerSi(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        # accessCode = 'AVZO03HA32BC46OZCB'                   # Live
        # workingKey = '1D5E76DE84FD6BD8B7708CF1A3A411C0'     # Live
        # merchant_id = "46319"                               # Live

        # accessCode = 'AVUP03GL28CI81PUIC'                   # Demo
        # workingKey = '2C469A8EAB648B3516CAFB272D661668'     # Demo
        # merchant_id = "45990"                               # Demo

        accessCode = 'AVCG03HF47CJ43GCJC'  # Demo
        workingKey = 'A9B10EF32C4CBF97465203EF20468F0A'  # Demo
        merchant_id = "43366"  # Demo

        requestdata     = request.data
        order_id        = requestdata['order_id']
        # order_amount    = requestdata['order_amount']
        str_status = ""
        try:
            if int(order_id)>0:
                rs_order  = EngageboostOrdermaster.objects.filter(custom_order_id=order_id).first()
            if rs_order:
                order_data = EngageboostOrdermasterSerializers(rs_order)
                order_data = order_data.data
                # Create Transaction
                customer_name = ""
                customer_email = ""
                customer_mobile = ""
                rs_trans_data = pg.CcAvenueCreateTransaction(order_data["id"])
                if order_data["customer_details"] and order_data["customer_details"]["first_name"] is not None:
                    if order_data["customer_details"]["first_name"]!="":
                        customer_name = order_data["customer_details"]["first_name"].strip()

                    customer_name = customer_name + " " + order_data["customer_details"]["last_name"]

                    if order_data["customer_details"]["email"] is not None and order_data["customer_details"]["email"]!="":
                        customer_email = order_data["customer_details"]["email"]
                    else:
                        customer_email = order_data["billing_email_address"]

                    if order_data["customer_details"]["phone"] is not None and order_data["customer_details"]["phone"]!="":
                        customer_mobile = order_data["customer_details"]["phone"]
                    else:
                        customer_mobile = order_data["billing_phone"]

                else:
                    customer_name = order_data["billing_name"]



                # Data for PG
                p_merchant_id       = str(merchant_id)
                p_order_id          = str(order_data["custom_order_id"])
                p_currency          = order_data['currency_code']
                # p_amount            = str(float(order_data['net_amount'])+float(order_data['shipping_cost']))
                # p_amount            = str(float(order_data['gross_amount']))
                p_amount            = '1.00'
                # p_redirect_url      = 'http://127.0.0.1:8000/api/front/v1/payment-response/'
                p_redirect_url      = 'http://15.185.126.44:8062/api/front/v1/payment-response/'
                # p_cancel_url        = 'http://127.0.0.1:8000/api/front/v1/payment-response/'
                p_cancel_url        = 'http://15.185.126.44:8062/api/front/v1/payment-response/'
                p_language          = 'EN'
                p_show_address      = 'N'
                p_show_addr         = 'N'
                p_billing_name      = customer_name # order_data["billing_name"]
                p_billing_address   = order_data["billing_street_address"]
                p_billing_city      = order_data["billing_state_name"]
                p_billing_state     = order_data["billing_state_name"]
                p_billing_zip       = ""
                p_billing_country   = order_data["billing_country_name"]
                p_billing_tel       = str(customer_mobile) #str(order_data["billing_phone"])
                p_billing_email     = customer_email # order_data["billing_email_address"]


                p_si_type           = "ONDEMAND"
                # p_si_mer_ref_no     = "1234"
                p_si_is_setup_amt   = "N"
                p_si_start_date     = requestdata['si_start_date']
                # p_delivery_name     = order_data["delivery_name"]
                # p_delivery_address  = order_data["delivery_street_address"]
                # p_delivery_city     = order_data["delivery_state_name"]
                # p_delivery_state    = order_data["delivery_state_name"]
                # p_delivery_zip      = ""
                # p_delivery_country  = order_data["delivery_country_name"]
                # p_delivery_tel      = str(order_data["delivery_phone"])
                # p_merchant_param1   = str(order_id)
                # p_merchant_param2   = str(rs_trans_data["transaction_id"])

                p_merchant_param1   = ""
                p_merchant_param2   = ""
                p_merchant_param3   = ""
                p_merchant_param4   = ""
                p_merchant_param5   = ""
                p_promo_code        = ""
                p_customer_identifier = ""


                # p_customer_identifier = str(order_data["customer"])

                merchant_data='merchant_id='+p_merchant_id+'&'+'order_id='+p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + p_amount+'&'+'redirect_url='+p_redirect_url+'&'+'cancel_url='+p_cancel_url+'&'+'language='+p_language+'&'+'show_address='+p_show_address+'&'+'show_addr='+p_show_addr+'&'+'billing_name='+p_billing_name+'&'+'billing_address='+p_billing_address+'&'+'billing_city='+p_billing_city+'&'+'billing_state='+p_billing_state+'&'+'billing_zip='+p_billing_zip+'&'+'billing_country='+p_billing_country+'&'+'billing_tel='+p_billing_tel+'&'+'billing_email='+p_billing_email+'&'+'si_type='+p_si_type+'&'+'si_is_setup_amt='+p_si_is_setup_amt+'&'+'si_start_date='+p_si_start_date+'&'+'merchant_param1='+p_merchant_param1+'&'+'merchant_param2='+p_merchant_param2+'&'+'merchant_param3='+p_merchant_param3+'&'+'merchant_param4='+p_merchant_param4+'&'+'merchant_param5='+p_merchant_param5+'&'+'promo_code='+p_promo_code+'&'+'customer_identifier='+p_customer_identifier
                # print("merchant_data==========++++", merchant_data)
                encryption = encrypt(merchant_data,workingKey)

                # url = "https://secure.ccavenue.ae/transaction/transaction.do?command=initiateTransaction"
                #
                # data = {'access_code': accessCode, 'encRequest': encryption}
                # cc_response = requests.post(url=url, data=data)
                # cc_response = cc_response.text
                # cc_response = str(cc_response)


                str_status = status.HTTP_200_OK
                data = {
                    "status":str_status,
                    "enc_value":encryption,
                    "access_code":accessCode
                }

            else:
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                    "status":str_status,
                    "message":"Order Id Not found.",
                    "enc_value":""
                }
        except Exception as error:
            str_status = status.HTTP_417_EXPECTATION_FAILED
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Order Not Found."}
        # print("data=========", data)
        return Response(data)

#-----------------duplicate----------------------#
class CcavenueRequestHandlerSi_SI(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        accessCode = 'AVZO03HA32BC46OZCB'                   # Live
        workingKey = '1D5E76DE84FD6BD8B7708CF1A3A411C0'     # Live
        merchant_id = "46319"                               # Live

        # accessCode = 'AVUP03GL28CI81PUIC'                   # Demo
        # workingKey = '2C469A8EAB648B3516CAFB272D661668'     # Demo
        # merchant_id = "45990"                               # Demo

        # accessCode = 'AVCG03HF47CJ43GCJC'  # Demo
        # workingKey = 'A9B10EF32C4CBF97465203EF20468F0A'  # Demo
        # merchant_id = "43366"  # Demo

        requestdata     = request.data
        order_id        = requestdata['order_id']
        # order_amount    = requestdata['order_amount']
        str_status = ""
        try:
            if int(order_id)>0:
                rs_order  = EngageboostOrdermaster.objects.filter(custom_order_id=order_id).first()
            if rs_order:
                order_data = EngageboostOrdermasterSerializers(rs_order)
                order_data = order_data.data
                # Create Transaction
                customer_name = ""
                customer_email = ""
                customer_mobile = ""
                rs_trans_data = pg.CcAvenueCreateTransaction(order_data["id"])
                if order_data["customer_details"] and order_data["customer_details"]["first_name"] is not None:
                    if order_data["customer_details"]["first_name"]!="":
                        customer_name = order_data["customer_details"]["first_name"].strip()

                    customer_name = customer_name + " " + order_data["customer_details"]["last_name"]

                    if order_data["customer_details"]["email"] is not None and order_data["customer_details"]["email"]!="":
                        customer_email = order_data["customer_details"]["email"]
                    else:
                        customer_email = order_data["billing_email_address"]

                    if order_data["customer_details"]["phone"] is not None and order_data["customer_details"]["phone"]!="":
                        customer_mobile = order_data["customer_details"]["phone"]
                    else:
                        customer_mobile = order_data["billing_phone"]

                else:
                    customer_name = order_data["billing_name"]



                # Data for PG
                p_merchant_id       = str(merchant_id)
                p_order_id          = str(order_data["custom_order_id"])
                p_currency          = order_data['currency_code']
                # p_amount            = str(float(order_data['net_amount'])+float(order_data['shipping_cost']))
                # p_amount            = str(float(order_data['gross_amount']))
                p_amount            = '1.00'
                # p_redirect_url      = 'http://127.0.0.1:8000/api/front/v1/payment-response/'
                # p_redirect_url      = 'https://www.gogrocery.ae/api/front/v1/payment-response-si/'
                # p_cancel_url        = 'http://127.0.0.1:8000/api/front/v1/payment-response/'
                # p_cancel_url        = 'https://www.gogrocery.ae/api/front/v1/payment-response-si/'
                p_redirect_url      = 'http://157.175.131.51:8062/api/front/v1/payment-response-si/'
                p_cancel_url        = 'http://157.175.131.51:8062/api/front/v1/payment-response-si/'
                p_language          = 'EN'
                p_show_address      = 'N'
                p_show_addr         = 'N'
                p_billing_name      = customer_name # order_data["billing_name"]
                p_billing_address   = order_data["billing_street_address"]
                p_billing_city      = order_data["billing_state_name"]
                p_billing_state     = order_data["billing_state_name"]
                p_billing_zip       = ""
                p_billing_country   = order_data["billing_country_name"]
                p_billing_tel       = str(customer_mobile) #str(order_data["billing_phone"])
                p_billing_email     = customer_email # order_data["billing_email_address"]


                p_si_type           = "ONDEMAND"
                # p_si_mer_ref_no     = "1234"
                p_si_is_setup_amt   = "N"
                p_si_start_date     = requestdata['si_start_date']
                p_delivery_name     = order_data["delivery_name"]
                p_delivery_address  = order_data["delivery_street_address"]
                p_delivery_city     = order_data["delivery_state_name"]
                p_delivery_state    = order_data["delivery_state_name"]
                p_delivery_zip      = ""
                p_delivery_country  = order_data["delivery_country_name"]
                p_delivery_tel      = str(order_data["delivery_phone"])
                p_merchant_param1   = str(order_id)
                p_merchant_param2   = str(rs_trans_data["transaction_id"])
                p_merchant_param1   = ""
                p_merchant_param2   = ""
                p_merchant_param3   = ""
                p_merchant_param4   = ""
                p_merchant_param5   = ""
                p_promo_code        = ""
                p_customer_identifier = ""


                # p_customer_identifier = str(order_data["customer"])

                # merchant_data='merchant_id='+p_merchant_id+'&'+'order_id='+p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + p_amount+'&'+'redirect_url='+p_redirect_url+'&'+'cancel_url='+p_cancel_url+'&'+'language='+p_language+'&'+'show_address='+p_show_address+'&'+'show_addr='+p_show_addr+'&'+'billing_name='+p_billing_name+'&'+'billing_address='+p_billing_address+'&'+'billing_city='+p_billing_city+'&'+'billing_state='+p_billing_state+'&'+'billing_zip='+p_billing_zip+'&'+'billing_country='+p_billing_country+'&'+'billing_tel='+p_billing_tel+'&'+'billing_email='+p_billing_email+'&'+'si_type='+p_si_type+'&'+'si_is_setup_amt='+p_si_is_setup_amt+'&'+'si_start_date='+p_si_start_date+'&'+'merchant_param1='+p_merchant_param1+'&'+'merchant_param2='+p_merchant_param2+'&'+'merchant_param3='+p_merchant_param3+'&'+'merchant_param4='+p_merchant_param4+'&'+'merchant_param5='+p_merchant_param5+'&'+'promo_code='+p_promo_code+'&'+'customer_identifier='+p_customer_identifier

                merchant_data='merchant_id='+p_merchant_id+'&'+'order_id='+p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + p_amount+'&'+'redirect_url='+p_redirect_url+'&'+'cancel_url='+p_cancel_url+'&'+'language='+p_language+'&'+'show_address='+p_show_address+'&'+'show_addr='+p_show_addr+'&'+'billing_name='+p_billing_name+'&'+'billing_address='+p_billing_address+'&'+'billing_city='+p_billing_city+'&'+'billing_state='+p_billing_state+'&'+'billing_zip='+p_billing_zip+'&'+'billing_country='+p_billing_country+'&'+'billing_tel='+p_billing_tel+'&'+'billing_email='+p_billing_email+'&'+'si_type='+p_si_type+'&'+'si_is_setup_amt='+p_si_is_setup_amt+'&'+'si_start_date='+p_si_start_date+'&'+'merchant_param1='+p_merchant_param1+'&'+'merchant_param2='+p_merchant_param2+'&'+'merchant_param3='+p_merchant_param3+'&'+'merchant_param4='+p_merchant_param4+'&'+'merchant_param5='+p_merchant_param5+'&'+'promo_code='+p_promo_code+'&'+'customer_identifier='+p_customer_identifier+'&delivery_name='+p_delivery_name+'&delivery_address='+p_delivery_address+'&delivery_city='+p_delivery_city+'&delivery_country='+p_delivery_country+'&delivery_tel='+p_delivery_tel

                # print("merchant_data==========++++", merchant_data)
                encryption = encrypt(merchant_data,workingKey)

                # url = "https://secure.ccavenue.ae/transaction/transaction.do?command=initiateTransaction"
                #
                # data = {'access_code': accessCode, 'encRequest': encryption}
                # cc_response = requests.post(url=url, data=data)
                # cc_response = cc_response.text
                # cc_response = str(cc_response)


                str_status = status.HTTP_200_OK
                data = {
                    "status":str_status,
                    "enc_value":encryption,
                    "access_code":accessCode
                }

            else:
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                    "status":str_status,
                    "message":"Order Id Not found.",
                    "enc_value":""
                }
        except Exception as error:
            str_status = status.HTTP_417_EXPECTATION_FAILED
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Order Not Found."}
        # print("data=========", data)
        return Response(data)


def payment_request_si_charge(order_id):

    accessCode = 'AVCG03HF47CJ43GCJC'                   # Demo
    workingKey = 'A9B10EF32C4CBF97465203EF20468F0A'     # Demo
    merchant_id = "43366"                               # Demo

    url = "https://login.ccavenue.ae/apis/servlet/DoWebTrans"

    # requestdata     = request.data
    # order_id        = requestdata['order_id']
    # print('order_id')
    # print(order_id)
    now_utc = datetime.now(timezone.utc).astimezone()
    decryption = {}
    try:

        rs_record = EngageboostCcavenueUpgradedReturnDetails.objects.filter(order_id=order_id).first()
        rs_order = EngageboostOrdermaster.objects.filter(id=order_id).first()

        si_sub_ref_no = rs_record.si_ref_no
        si_mer_charge_ref_no = str(order_id)
        si_currency = "AED"
        si_amount = str(rs_order.gross_amount)

        command = "chargeSI"
        request_type = "STRING"
        version = "1.1"

        charge_data = si_sub_ref_no+"|"+si_mer_charge_ref_no+"|"+si_currency+"|"+si_amount+"|"
        # print("merchant_data==========++++", merchant_data)
        encryption = encrypt(charge_data, workingKey)

        data = {'access_code': accessCode, 'request_type': request_type, 'command': command,
                'response_type': "JSON", 'enc_request': encryption, 'version': version}
        cc_response = requests.post(url=url, data=data)
        cc_response = cc_response.text
        cc_response = str(cc_response)
        # print('cc_response')
        # print(cc_response)

        res = []
        for sub in cc_response.split('&'):
            if '=' in sub:
                res.append(map(str.strip, sub.split('=', 1)))
        res = dict(res)
        # print(res)
        # print('res')
        decryption=''
        # print(type(res['status']))
        # print(res['status'])
        if res['status'] == '0':
            str_status = status.HTTP_200_OK
            decResp = decrypt(res['enc_response'], workingKey)

            obj_resp = str(decResp)
            obj_resp = obj_resp[2:-1]
            str_obj = obj_resp.replace("\\x00", '')
            str_obj = str_obj.replace("\\x01", '')
            str_obj = str_obj.replace("\\x02", '')
            str_obj = str_obj.replace("\\x03", '')
            str_obj = str_obj.replace("\\x04", '')
            str_obj = str_obj.replace("\\x05", '')
            str_obj = str_obj.replace("\\x06", '')
            str_obj = str_obj.replace("\\x07", '')
            str_obj = str_obj.replace("\\x08", '')
            str_obj = str_obj.replace("\\x09", '')
            str_obj = str_obj.replace("\\x10", '')
            str_obj = str_obj.replace("\\x0a", '')
            str_obj = str_obj.replace("\\x0b", '')
            str_obj = str_obj.replace("\\x0c", '')
            str_obj = str_obj.replace("\\x0d", '')
            str_obj = str_obj.replace("\\x0e", '')
            str_obj = str_obj.replace("\\x0f", '')
            str_obj = str_obj.replace("\\t", '')
            str_obj = str_obj.replace("\\n", '')
            str_obj = str_obj.replace("\\r", '')

            decryption = json.loads(str_obj)

            if decryption['si_charge_status'] == "0" and decryption['si_charge_txn_status'] == "0":
                update_arr = {
                    # "received_status": "Payment Ok",
                    "pay_txntranid": decryption['reference_no'],
                    "pay_txndate": now_utc,
                    "paid_amount": round(rs_order.gross_amount, 2)
                }

                data = {'status': 'success',
                        'msg': decryption['si_error_desc'],
                        'si_ref_no': rs_record.si_ref_no,
                        'pay_txntranid': decryption['reference_no']
                        }

                common.email_send_by_AutoResponder(rs_order.id, 3)
            else:
                update_arr = {
                    # "order_status": 999,
                    # "buy_status": 0,
                    "pay_txntranid": decryption['reference_no'],
                    "pay_txndate": now_utc,
                    # "received_status": "Payment Failed."
                }

                data = {'status': 'failed',
                        'msg': decryption['si_error_desc'],
                        'si_ref_no': rs_record.si_ref_no,
                        'pay_txntranid': decryption['reference_no']}

                common.email_send_by_AutoResponder(rs_order.id, 25)

            EngageboostOrdermaster.objects.filter(id=rs_order.id).update(**update_arr)


        elif res['status'] == '1':
            decryption = res['enc_response']

            # Update Stock
            # rs_trans = EngageboostCcavenueUpgradedReturnDetails.objects.filter(order_id=rs_order.id).first()
            # if rs_trans:
                # update_arr = {
                    # "order_status": 999,
                    # "buy_status": 0,
                    # "received_status": "Payment Failed."
                # }

                # CANCEL ORDER IF CUSMER CANCEL PAYMENT
                # order_id = rs_trans.order_id
                # rs_order = EngageboostOrdermaster.objects.filter(id=order_id).first()
                # if rs_order:
                    # EngageboostCcavenueUpgradedReturnDetails.objects.filter(order_id=order_id).update(order_status="cancel")
                    # EngageboostOrdermaster.objects.filter(id=order_id).update(**update_arr)
                    # common.email_send_by_AutoResponder(rs_order.id, 28)

            data = {'status': 'error', 'msg': decryption}


    except Exception as error:
        str_status = status.HTTP_417_EXPECTATION_FAILED
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Order Not Found.", "decryption":decryption}
    # print("data=========", data)
    return data

#-----------------duplicate----------------------#
def payment_request_si_charge_si(order_id):

    # accessCode = 'AVCG03HF47CJ43GCJC'                   # Demo
    # workingKey = 'A9B10EF32C4CBF97465203EF20468F0A'     # Demo
    # merchant_id = "43366"                               # Demo

    accessCode = 'AVZO03HA32BC46OZCB'                   # Live
    workingKey = '1D5E76DE84FD6BD8B7708CF1A3A411C0'     # Live
    merchant_id = "46319"                               # Live

    url = "https://login.ccavenue.ae/apis/servlet/DoWebTrans"

    # requestdata     = request.data
    # order_id        = requestdata['order_id']
    # print('order_id')
    # print(order_id)
    now_utc = datetime.now(timezone.utc).astimezone()
    decryption = {}
    try:

        rs_record = EngageboostCcavenueUpgradedReturnDetails.objects.filter(order_id=order_id).first()
        rs_order = EngageboostOrdermaster.objects.filter(id=order_id).first()

        si_sub_ref_no = rs_record.si_ref_no
        si_mer_charge_ref_no = str(order_id)
        si_currency = "AED"
        si_amount = str(rs_order.gross_amount)
        # si_amount = "1.00"
        command = "chargeSI"
        request_type = "STRING"
        version = "1.1"

        charge_data = si_sub_ref_no+"|"+si_mer_charge_ref_no+"|"+si_currency+"|"+si_amount+"|"
        print("charge_data==========++++", charge_data)
        encryption = encrypt(charge_data, workingKey)

        data = {'access_code': accessCode, 'request_type': request_type, 'command': command,
                'response_type': "JSON", 'enc_request': encryption, 'version': version}
        cc_response = requests.post(url=url, data=data)
        cc_response = cc_response.text
        cc_response = str(cc_response)
        print('cc_response==============', cc_response)
        # print(cc_response)

        res = []
        for sub in cc_response.split('&'):
            if '=' in sub:
                res.append(map(str.strip, sub.split('=', 1)))
        res = dict(res)
        # print(res)
        # print('res')
        decryption=''
        # print(type(res['status']))
        # print(res['status'])
        if res['status'] == '0':
            str_status = status.HTTP_200_OK
            decResp = decrypt(res['enc_response'], workingKey)

            obj_resp = str(decResp)
            obj_resp = obj_resp[2:-1]
            str_obj = obj_resp.replace("\\x00", '')
            str_obj = str_obj.replace("\\x01", '')
            str_obj = str_obj.replace("\\x02", '')
            str_obj = str_obj.replace("\\x03", '')
            str_obj = str_obj.replace("\\x04", '')
            str_obj = str_obj.replace("\\x05", '')
            str_obj = str_obj.replace("\\x06", '')
            str_obj = str_obj.replace("\\x07", '')
            str_obj = str_obj.replace("\\x08", '')
            str_obj = str_obj.replace("\\x09", '')
            str_obj = str_obj.replace("\\x10", '')
            str_obj = str_obj.replace("\\x0a", '')
            str_obj = str_obj.replace("\\x0b", '')
            str_obj = str_obj.replace("\\x0c", '')
            str_obj = str_obj.replace("\\x0d", '')
            str_obj = str_obj.replace("\\x0e", '')
            str_obj = str_obj.replace("\\x0f", '')
            str_obj = str_obj.replace("\\t", '')
            str_obj = str_obj.replace("\\n", '')
            str_obj = str_obj.replace("\\r", '')
            print("str_obj============123==", str_obj)
            decryption = json.loads(str_obj)
            print("decryption============123==", decryption)

            if decryption['si_charge_status'] == "0" and decryption['si_charge_txn_status'] == "0":
                update_arr = {
                    # "received_status": "Payment Ok",
                    "pay_txntranid": decryption['reference_no'],
                    "pay_txndate": now_utc,
                    "paid_amount": round(rs_order.gross_amount, 2)
                }

                data = {'status': 'success',
                        'msg': decryption['si_error_desc'],
                        'si_ref_no': rs_record.si_ref_no,
                        'pay_txntranid': decryption['reference_no']
                        }

            else:
                update_arr = {
                    # "order_status": 999,
                    # "buy_status": 0,
                    "pay_txntranid": decryption['reference_no'],
                    "pay_txndate": now_utc,
                    # "received_status": "Payment Failed."
                }

                data = {'status': 'failed',
                        'msg': decryption['si_error_desc'],
                        'si_ref_no': rs_record.si_ref_no,
                        'pay_txntranid': decryption['reference_no']}

                

            EngageboostOrdermaster.objects.filter(id=rs_order.id).update(**update_arr)


        elif res['status'] == '1':
            decryption = res['enc_response']

            # Update Stock
            # rs_trans = EngageboostCcavenueUpgradedReturnDetails.objects.filter(order_id=rs_order.id).first()
            # if rs_trans:
                # update_arr = {
                    # "order_status": 999,
                    # "buy_status": 0,
                    # "received_status": "Payment Failed."
                # }

                # CANCEL ORDER IF CUSMER CANCEL PAYMENT
                # order_id = rs_trans.order_id
                # rs_order = EngageboostOrdermaster.objects.filter(id=order_id).first()
                # if rs_order:
                    # EngageboostCcavenueUpgradedReturnDetails.objects.filter(order_id=order_id).update(order_status="cancel")
                    # EngageboostOrdermaster.objects.filter(id=order_id).update(**update_arr)
                    # common.email_send_by_AutoResponder(rs_order.id, 28)

            data = {'status': 'error', 'msg': decryption}


    except Exception as error:
        str_status = status.HTTP_417_EXPECTATION_FAILED
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Order Not Found.", "decryption":decryption}
    # print("data=========", data)
    return data


class CcavenueRequestHandlerSiChargeList(APIView):
    # permission_classes = []
    def get(self, request, format=None):

        # accessCode = 'AVCG03HF47CJ43GCJC'                   # Demo
        # workingKey = 'A9B10EF32C4CBF97465203EF20468F0A'     # Demo
        # merchant_id = "43366"                               # Demo

        accessCode = 'AVZO03HA32BC46OZCB'  # Live
        workingKey = '1D5E76DE84FD6BD8B7708CF1A3A411C0'  # Live
        merchant_id = "46319"  # Live

         # https://secure.ccavenue.ae/transaction/transaction.do?command=initiateTransaction
        # url = "https://test.ccavenue.ae/apis/servlet/DoWebTrans"

        url = "https://login.ccavenue.ae/apis/servlet/DoWebTrans"

        # print(request.POST['si_sub_ref_no'])
        try:
            requestdata = request.data
            # si_sub_ref_no_list = requestdata['si_sub_ref_no']
            customer_id = EngageboostCustomers.objects.filter(auth_user=request.user.id).first()
            # print("=====customer_id.id=======", customer_id.id)
            si_sub_ref_no_list = EngageboostUserSIList.objects.filter(customer_id=customer_id.id, isdeleted='n', isblocked='n').values('si_ref_no', 'id', 'is_default')

            # print("=====si_sub_ref_no_list=======", si_sub_ref_no_list)
            # print("customer_id", customer_id.id, customer_id.auth_user_id)
            # si_mer_charge_ref_no = "ABCD1234"
            # si_currency = "AED"
            # si_amount = request.POST['si_amount']

            command = "getSIChargeList"
            access_code = "AVZO03HA32BC46OZCB"
            request_type = "JSON"
            version = "1.1"

            card_list = []
            # charge_data = si_sub_ref_no
            for si_sub_ref_no in si_sub_ref_no_list:
                charge_data = {
                    'si_sub_ref_no': si_sub_ref_no['si_ref_no'],
                    'page_size': 1,
                    'page_number': 1
                    }
                # print("merchant_data==========++++", merchant_data)
                encryption = encrypt(str(charge_data), workingKey)

                data = {'access_code': access_code, 'request_type': request_type, 'command': command,
                        'response_type': "JSON", 'enc_request': encryption, 'version': version}
                cc_response = requests.post(url=url, data=data)
                cc_response = cc_response.text
                cc_response = str(cc_response)
                # print(type(cc_response))

                res = []
                for sub in cc_response.split('&'):
                    if '=' in sub:
                        res.append(map(str.strip, sub.split('=', 1)))
                res = dict(res)
                # print(res)
                # print('res')
                decryption=''
                # print(type(res['status']))
                # print(res['status'])
                if res['status'] == '0':
                    decryption = decrypt(res['enc_response'], workingKey)
                elif res['status'] == '1':
                    decryption = res['enc_response']
                # return encryption
                # print(json.dumps(decryption))

                obj_resp = str(decryption)
                obj_resp = obj_resp[2:-1]
                str_obj = obj_resp.replace("\\x00", '')
                str_obj = str_obj.replace("\\x01", '')
                str_obj = str_obj.replace("\\x02", '')
                str_obj = str_obj.replace("\\x03", '')
                str_obj = str_obj.replace("\\x04", '')
                str_obj = str_obj.replace("\\x05", '')
                str_obj = str_obj.replace("\\x06", '')
                str_obj = str_obj.replace("\\x07", '')
                str_obj = str_obj.replace("\\x08", '')
                str_obj = str_obj.replace("\\x09", '')
                str_obj = str_obj.replace("\\x10", '')
                str_obj = str_obj.replace("\\x0a", '')
                str_obj = str_obj.replace("\\x0b", '')
                str_obj = str_obj.replace("\\x0c", '')
                str_obj = str_obj.replace("\\x0d", '')
                str_obj = str_obj.replace("\\x0e", '')
                str_obj = str_obj.replace("\\x0f", '')
                str_obj = str_obj.replace("\\t", '')
                str_obj = str_obj.replace("\\n", '')
                str_obj = str_obj.replace("\\r", '')

                decryption = json.loads(str_obj)
                if int(decryption['total_records']) > 0:
                    card_data = {
                        "id": si_sub_ref_no['id'],
                        "si_sub_ref_no": si_sub_ref_no['si_ref_no'],
                        "card_type": decryption['si_Charge_List_Result'][0]['card_name'],
                        "card_suffix": decryption['si_Charge_List_Result'][0]['card_suffix'],
                        "is_default": si_sub_ref_no['is_default']
                    }

                    card_list.append(card_data)
            # print(decrypt(encryption, workingKey))
            # exit(1)
            str_status = status.HTTP_200_OK
            data = {
                "status": str_status,
                # "enc_value": encryption,
                "card_list": card_list,
                # "cc_response": cc_response,
                # "access_code": accessCode
            }
        except Exception as error:
            str_status = status.HTTP_417_EXPECTATION_FAILED
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Order Not Found."}
        # print("data=========", data)
        return Response(data)


class RemoveSavedCard(APIView):
    # permission_classes = []
    def get(self, request, pk, format=None):
        # accessCode = 'AVCG03HF47CJ43GCJC'  # Demo
        # workingKey = 'A9B10EF32C4CBF97465203EF20468F0A'  # Demo
        # merchant_id = "43366"  # Demo

        accessCode = 'AVZO03HA32BC46OZCB'  # Live
        workingKey = '1D5E76DE84FD6BD8B7708CF1A3A411C0'  # Live
        merchant_id = "46319"  # Live

        command = "cancelSI"
        request_type = "JSON"
        version = 1.1
        # https://secure.ccavenue.ae/transaction/transaction.do?command=initiateTransaction
        url = "https://test.ccavenue.ae/apis/servlet/DoWebTrans"
        try:

            si_sub_ref_data = EngageboostUserSIList.objects.filter(id=pk).first()
            if si_sub_ref_data:
                # charge_data = {
                #     'si_sub_ref_no': si_sub_ref_data.si_ref_no
                # }
                # # print("merchant_data==========++++", merchant_data)
                # encryption = encrypt(str(charge_data), workingKey)
                #
                # data = {'access_code': accessCode, 'request_type': request_type, 'command': command,
                #         'response_type': "JSON", 'enc_request': encryption, 'version': version}
                # cc_response = requests.post(url=url, data=data)
                # cc_response = cc_response.text
                # cc_response = str(cc_response)
                # # print(type(cc_response))
                #
                # res = []
                # for sub in cc_response.split('&'):
                #     if '=' in sub:
                #         res.append(map(str.strip, sub.split('=', 1)))
                # res = dict(res)
                # # print(res)
                # # print('res')
                # decryption = ''
                # # print(type(res['status']))
                # # print(res['status'])
                # if res['status'] == '0':
                #     decryption = decrypt(res['enc_response'], workingKey)
                # elif res['status'] == '1':
                #     decryption = res['enc_response']
                # # return encryption
                # # print(json.dumps(decryption))
                #
                # obj_resp = str(decryption)
                # obj_resp = obj_resp[2:-1]
                # str_obj = obj_resp.replace("\\x00", '')
                # str_obj = str_obj.replace("\\x01", '')
                # str_obj = str_obj.replace("\\x02", '')
                # str_obj = str_obj.replace("\\x03", '')
                # str_obj = str_obj.replace("\\x04", '')
                # str_obj = str_obj.replace("\\x05", '')
                # str_obj = str_obj.replace("\\x06", '')
                # str_obj = str_obj.replace("\\x07", '')
                # str_obj = str_obj.replace("\\x08", '')
                # str_obj = str_obj.replace("\\x09", '')
                # str_obj = str_obj.replace("\\x10", '')
                # str_obj = str_obj.replace("\\x0a", '')
                # str_obj = str_obj.replace("\\x0b", '')
                # str_obj = str_obj.replace("\\x0c", '')
                # str_obj = str_obj.replace("\\x0d", '')
                # str_obj = str_obj.replace("\\x0e", '')
                # str_obj = str_obj.replace("\\x0f", '')
                # str_obj = str_obj.replace("\\t", '')
                # str_obj = str_obj.replace("\\n", '')
                # str_obj = str_obj.replace("\\r", '')
                #
                # decryption = json.loads(str_obj)
                #
                # # print("===decryption=====", decryption)
                # if decryption['si_cancel_status']==0:
                EngageboostUserSIList.objects.filter(id=pk).update(isdeleted='y')
                message = "Card removed successfully"
                # else:
                #     message = "Card removed failed"
                str_status = status.HTTP_200_OK
                data = {
                    "status": str_status,
                    "api_status": 1,
                    "message": message
                }
        except Exception as error:
            str_status = status.HTTP_417_EXPECTATION_FAILED
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Card Not Found."}
        # print("data=========", data)
        return Response(data)
