#!/usr/bin/python
from rest_framework import generics, permissions, status, views, mixins
from frontapp.views.payment.ccavutil import encrypt,decrypt
from string import Template
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework.response import Response
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from frontapp.views.payment import paymentgateway as pg
import base64
import json
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from webservices.models import *
from frontapp.frontapp_serializers import *

def PgSettingsDetails(method_id, payment_type_id):
    settings_data =[]
    rs_settings = EngageboostPaymentgatewaySettingInformation.objects.filter(paymentgateway_method_id=method_id, paymentgateway_type_id=payment_type_id, isblocked='n', isdeleted = 'n').all()
    if rs_settings:
        settings_data = PaymentgatewaySettingInformationSerializer(rs_settings, many=True)
        settings_data = settings_data.data


    if settings_data:
        for api_data in settings_data:
            print("api_data==", json.dumps(api_data))
            # if "api_url" in settings_data and settings_data[0]["api_url"]!="" and settings_data[0]["api_url"] is not None:
            #     base_URL = settings_data[0]["api_url"]

            if "CCAVENUE_UPGRADE_MERCHANT_ID" in api_data and api_data["CCAVENUE_UPGRADE_MERCHANT_ID"]!="" and api_data["CCAVENUE_UPGRADE_MERCHANT_ID"] is not None:
                print("kkk")
                merchant_id = api_data["CCAVENUE_UPGRADE_MERCHANT_ID"]

            # if "merchant_id" in settings_data and settings_data[0]["merchant_id"]!="" and settings_data[0]["merchant_id"] is not None:
            #     merchant_id = settings_data[0]["merchant_id"]
    # print("merchant_id++", merchant_id)
    return settings_data

# PgSettingsDetails(51,2)

@csrf_exempt
def res(request):
    if(request.method == "GET"):
        '''
        Please put in the 32 bit alphanumeric key in quotes provided by CCAvenues.
        '''
        encResp = request.GET['encResp']
        workingKey = '2C469A8EAB648B3516CAFB272D661668'
        decResp = decrypt(encResp,workingKey)

        data = '<table border=1 cellspacing=2 cellpadding=2><tr><td>'
        data = data + decResp.replace('=','</td><td>')
        data = data.replace('&','</td></tr><tr><td>')
        data = data + '</td></tr></table>'

        html = '''\
        <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                <title>Response Handler</title>
            </head>
            <body>
                <center>
                    <font size="4" color="blue"><b>Response Page</b></font>
                    <br>
                    $response
                </center>
                <br>
            </body>
        </html>
        '''
        fin = Template(html).safe_substitute(response=data)
        data = {
            "data":fin
        }
        return HttpResponse(fin)
    elif (request.method == "POST"):
        req_data = request.POST
        encResp = req_data.get('encResp')
        # workingKey = '2C469A8EAB648B3516CAFB272D661668'    # Demo
        workingKey = '1D5E76DE84FD6BD8B7708CF1A3A411C0'		 # Live
        decResp = decrypt(encResp,workingKey)
        obj_resp = str(decResp)
        obj_resp = obj_resp[2:]
        str_obj = obj_resp.split('}')
        str_data = str_obj[0]+"}"
        str_json = json.loads(str_data)
        order_id ="5000"+str_json["order_id"][-4:]
        merchant_param1 = str_json["order_id"][-4:]
        str_json['order_id'] = order_id
        str_json['merchant_param1'] = merchant_param1
        return_transaction = pg.UpdateCcAvenuePaymentTransaction(str_json)
        return HttpResponse(decResp)

@csrf_exempt
def res_demo(request):
    if(request.method == "GET"):
        '''
        Please put in the 32 bit alphanumeric key in quotes provided by CCAvenues.
        '''
        encResp = request.GET['encResp']
        workingKey = '2C469A8EAB648B3516CAFB272D661668'
        decResp = decrypt(encResp,workingKey)

        data = '<table border=1 cellspacing=2 cellpadding=2><tr><td>'
        data = data + decResp.replace('=','</td><td>')
        data = data.replace('&','</td></tr><tr><td>')
        data = data + '</td></tr></table>'

        html = '''\
        <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                <title>Response Handler</title>
            </head>
            <body>
                <center>
                    <font size="4" color="blue"><b>Response Page</b></font>
                    <br>
                    $response
                </center>
                <br>
            </body>
        </html>
        '''
        fin = Template(html).safe_substitute(response=data)
        data = {
            "data":fin
        }
        return HttpResponse(fin)
    elif (request.method == "POST"):
        req_data = request.POST
        encResp = req_data.get('encResp')
        workingKey = '2C469A8EAB648B3516CAFB272D661668'    # Demo
        # workingKey = '1D5E76DE84FD6BD8B7708CF1A3A411C0'		 # Live
        decResp = decrypt(encResp,workingKey)
        obj_resp = str(decResp)
        obj_resp = obj_resp[2:]
        str_obj = obj_resp.split('}')
        str_data = str_obj[0]+"}"
        str_json = json.loads(str_data)
        return_transaction = pg.UpdateCcAvenuePaymentTransaction(str_json)
        return HttpResponse(decResp)

@csrf_exempt
def res_si(request):
    if(request.method == "GET"):
        '''
        Please put in the 32 bit alphanumeric key in quotes provided by CCAvenues.
        '''
        encResp = request.GET['encResp']
        workingKey = '1D5E76DE84FD6BD8B7708CF1A3A411C0'
        # workingKey = '2C469A8EAB648B3516CAFB272D661668'
        decResp = decrypt(encResp,workingKey)

        data = '<table border=1 cellspacing=2 cellpadding=2><tr><td>'
        data = data + decResp.replace('=','</td><td>')
        data = data.replace('&','</td></tr><tr><td>')
        data = data + '</td></tr></table>'

        html = '''\
        <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                <title>Response Handler</title>
            </head>
            <body>
                <center>
                    <font size="4" color="blue"><b>Response Page</b></font>
                    <br>
                    $response
                </center>
                <br>
            </body>
        </html>
        '''
        fin = Template(html).safe_substitute(response=data)
        data = {
            "data":fin
        }
        return HttpResponse(fin)
    elif (request.method == "POST"):
        req_data = request.POST
        print("req_data===================", req_data)
        encResp = req_data.get('encResp')
        settings_data = PgSettingsDetails(51, 2)
        # workingKey = '2C469A8EAB648B3516CAFB272D661668'    # Demo
        # workingKey = 'A9B10EF32C4CBF97465203EF20468F0A'  # SI Demo
        workingKey = '1D5E76DE84FD6BD8B7708CF1A3A411C0'		 # Live
        decResp = decrypt(encResp,workingKey)
        obj_resp = str(decResp)
        obj_resp = obj_resp[2:]
        str_obj = obj_resp.split('}')
        str_data = str_obj[0]+"}"
        str_json = json.loads(str_data)
        print("str_json===================", str_json)
    pg.CcAvenueCreateTransactionByCustomOrderId(str_json['order_id'])
    return_transaction = pg.UpdateCcAvenuePaymentTransaction_si(str_json)
    return HttpResponse(decResp)

@csrf_exempt
def AcavenueWebResponse(request):
    if (request.method == "POST"):
        req_data = request.POST
        encResp = req_data.get('encResp')
        settings_data = PgSettingsDetails(51,2)
        # workingKey = '2C469A8EAB648B3516CAFB272D661668'    # Demo
        workingKey = '1D5E76DE84FD6BD8B7708CF1A3A411C0'		 # Live
        # workingKey =
        decResp = decrypt(encResp,workingKey)
        obj_resp = str(decResp)
        obj_resp = obj_resp[2:]
        str_obj = obj_resp.split('}')
        str_data = str_obj[0]+"}"
        str_json = json.loads(str_data)
        return_transaction = pg.UpdateCcAvenuePaymentTransaction(str_json)

        print("return_transaction===", return_transaction)


        if str_json['order_status'].lower()=='success':
            redirect_to = "https://www.gogrocery.ae/success-payment/"
        else:
            redirect_to = "https://www.gogrocery.ae/failed-payment/"

        pay_status = status.HTTP_200_OK
        response_data = {
            "status":pay_status,
            "transaction_id":str_json['tracking_id']
        }
        response_data = str(urlsafe_base64_encode(force_bytes(response_data)))
        response_data = response_data.replace("b","")
        response_data = response_data.replace("'","")
        vv = redirect_to+'?res='+response_data
        print("redirect url+++++++", vv)
        # return HttpResponse(redirect_to)
        # return HttpResponseRedirect(redirect_to=redirect_to+'?res='+response_data)
        return HttpResponseRedirect(redirect_to=redirect_to)


@csrf_exempt
def AcavenueWebResponse_new(request):
    if (request.method == "POST"):
        req_data = request.POST
        encResp = req_data.get('encResp')
        # settings_data = PgSettingsDetails(51,2)
        # workingKey = '2C469A8EAB648B3516CAFB272D661668'    # Demo
        # workingKey = '1D5E76DE84FD6BD8B7708CF1A3A411C0'		 # Live
        workingKey = 'A9B10EF32C4CBF97465203EF20468F0A'
        # workingKey =
        decResp = decrypt(encResp,workingKey)
        print(decResp)
        obj_resp = str(decResp)
        obj_resp = obj_resp[2:-1]
        # str_obj = obj_resp.split('}')
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
        str_obj = str_obj.replace("=&", "\":\"\", \"")
        str_obj = str_obj.replace("=", "\":\"")
        str_obj = str_obj.replace("&", "\", \"")
        # str_obj = "{\""+str_obj+"\"}"
        # print(str_obj)
        # return HttpResponse(str_obj)
        str_json = json.loads(str_obj)
        return_transaction = pg.UpdateCcAvenuePaymentTransaction_new(str_json)

        print("return_transaction===", return_transaction)


        if str_json['order_status'].lower()=='success':
            # redirect_to = "http://15.185.126.44:82/success-payment/"+str_json['order_id']
            redirect_to = "http://15.185.126.44:82/checkout/success/"+str_json['order_id']
        else:
            redirect_to = "http://15.185.126.44:82/failed-payment/"+str_json['order_id']+"/"+str_json['order_status']+"/"+str_json['status_message']+"/"+str_json['failure_message']

        pay_status = status.HTTP_200_OK
        response_data = {
            "status":pay_status,
            "transaction_id":str_json['tracking_id']
        }
        response_data = str(urlsafe_base64_encode(force_bytes(response_data)))
        response_data = response_data.replace("b","")
        response_data = response_data.replace("'","")
        vv = redirect_to+'?res='+response_data
        print("redirect url+++++++", vv)
        # return HttpResponse(str_obj)
        # return HttpResponse(redirect_to)
        # return HttpResponseRedirect(redirect_to=redirect_to+'?res='+response_data)
        return HttpResponseRedirect(redirect_to=redirect_to)



def parse_payment_data(str_obj):

    search_string = "\"order_id\":\""
    print(search_string)
    index_of_order = str_obj.index(search_string)
    index_of_order += 12

    index_of_next_col = str_obj.index('"', index_of_order, len(str_obj))
    extracted_order_id = str_obj[index_of_order:index_of_next_col]

    rs_order = EngageboostOrdermaster.objects.filter(custom_order_id=extracted_order_id).first()
    order_id = rs_order.id

    # rs_record = EngageboostCcavenueUpgradedReturnDetails.objects.filter(order_id=order_id).update(
    #     payment_response_full=str_obj)
    print(order_id)

    # ----Getting tracking id-----#
    search_string = "\"tracking_id\":\""
    print(search_string)
    index_of_order = str_obj.index(search_string)
    index_of_order += 15

    index_of_next_col = str_obj.index('"', index_of_order, len(str_obj))
    extracted_tracking_id = str_obj[index_of_order:index_of_next_col]
    print(extracted_tracking_id)

    # ----Getting bank ref no-----#
    search_string = "\"bank_ref_no\":\""
    print(search_string)
    index_of_order = str_obj.index(search_string)
    index_of_order += 15

    index_of_next_col = str_obj.index('"', index_of_order, len(str_obj))
    extracted_bank_ref_no = str_obj[index_of_order:index_of_next_col]
    print(extracted_bank_ref_no)

    # ----Getting failure message-----#
    search_string = "\"failure_message\":\""
    print(search_string)
    index_of_order = str_obj.index(search_string)
    index_of_order += 19

    index_of_next_col = str_obj.index('"', index_of_order, len(str_obj))
    extracted_failure_message = str_obj[index_of_order:index_of_next_col]
    print(extracted_failure_message)

    # ----Getting payment mode-----#
    search_string = "\"payment_mode\":\""
    print(search_string)
    index_of_order = str_obj.index(search_string)
    index_of_order += 16

    index_of_next_col = str_obj.index('"', index_of_order, len(str_obj))
    extracted_payment_mode = str_obj[index_of_order:index_of_next_col]
    print(extracted_payment_mode)

    # ----Getting card name-----#
    search_string = "\"card_name\":\""
    print(search_string)
    index_of_order = str_obj.index(search_string)
    index_of_order += 13

    index_of_next_col = str_obj.index('"', index_of_order, len(str_obj))
    extracted_card_name = str_obj[index_of_order:index_of_next_col]
    print(extracted_card_name)

    # ----Getting status code-----#
    search_string = "\"status_code\":\""
    print(search_string)
    index_of_order = str_obj.index(search_string)
    index_of_order += 15

    index_of_next_col = str_obj.index('"', index_of_order, len(str_obj))
    extracted_status_code = str_obj[index_of_order:index_of_next_col]
    print(extracted_status_code)

    # ----Getting status message-----#
    search_string = "\"status_message\":\""
    print(search_string)
    index_of_order = str_obj.index(search_string)
    index_of_order += 18

    index_of_next_col = str_obj.index('"', index_of_order, len(str_obj))
    extracted_status_message = str_obj[index_of_order:index_of_next_col]
    print(extracted_status_message)

    # ----Getting currency-----#
    search_string = "\"currency\":\""
    print(search_string)
    index_of_order = str_obj.index(search_string)
    index_of_order += 12

    index_of_next_col = str_obj.index('"', index_of_order, len(str_obj))
    extracted_currency = str_obj[index_of_order:index_of_next_col]
    print(extracted_currency)

    # ----Getting si_created-----#
    search_string = "\"si_created\":\""
    print(search_string)
    index_of_order = str_obj.index(search_string)
    index_of_order += 14

    index_of_next_col = str_obj.index('"', index_of_order, len(str_obj))
    extracted_si_created = str_obj[index_of_order:index_of_next_col]
    print(extracted_si_created)

    if extracted_si_created.lower() == 'n':
        extracted_si_ref_no = ""
    else:
        # ----Getting si_ref_no-----#
        search_string = "\"si_ref_no\":\""
        print(search_string)
        index_of_order = str_obj.index(search_string)
        index_of_order += 13

        index_of_next_col = str_obj.index('"', index_of_order, len(str_obj))
        extracted_si_ref_no = str_obj[index_of_order:index_of_next_col]
    print(extracted_si_ref_no)

    # ----Getting order_status-----#
    search_string = "\"order_status\":\""
    print(search_string)
    index_of_order = str_obj.index(search_string)
    index_of_order += 16

    index_of_next_col = str_obj.index('"', index_of_order, len(str_obj))
    extracted_order_status = str_obj[index_of_order:index_of_next_col]
    print(extracted_order_status)

    data = {
        "order_id": extracted_order_id,
        "tracking_id": extracted_tracking_id,
        "bank_ref_no": extracted_bank_ref_no,
        "failure_message": extracted_failure_message,
        "payment_mode": extracted_payment_mode,
        "card_name": extracted_card_name,
        "status_code": extracted_status_code,
        "status_message": extracted_status_message,
        "currency": extracted_currency,
        "si_ref_no": extracted_si_ref_no,
        "order_status": extracted_order_status
    }

    data = str(data)
    data = data.replace("'", '"')
    data_json = json.loads(str(data))

    return data_json


@csrf_exempt
def AcavenueWebResponse_SI(request):
    if (request.method == "POST"):
        req_data = request.POST
        encResp = req_data.get('encResp')
        # settings_data = PgSettingsDetails(51,2)
        # workingKey = '2C469A8EAB648B3516CAFB272D661668'    # Demo
        workingKey = '1D5E76DE84FD6BD8B7708CF1A3A411C0'		 # Live
        # workingKey = 'A9B10EF32C4CBF97465203EF20468F0A'
        # workingKey =
        decResp = decrypt(encResp,workingKey)
        # decResp = encResp
        print("decResp=======================", decResp)
        obj_resp = str(decResp)
        obj_resp = obj_resp[2:-1]
        # str_obj = obj_resp.split('}')
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
        str_obj = str_obj.replace("=&", "\":\"\", \"")
        str_obj = str_obj.replace("=", "\":\"")
        str_obj = str_obj.replace("&", "\", \"")
        # str_obj = str_obj[2:-1]
        # str_obj = "{\""+str_obj+"\"}"
        print("str_obj=================", str_obj)
        # return HttpResponse(str_obj)
        # str_json = json.loads(str_obj)


        #----Getting order id-----#
        search_string = "\"order_id\":\""
        print(search_string)
        index_of_order = str_obj.index(search_string)
        index_of_order += 12

        index_of_next_col = str_obj.index('"', index_of_order, len(str_obj))
        extracted_order_id = str_obj[index_of_order:index_of_next_col]

        # str_json = parse_payment_data(str_obj)


        rs_order = EngageboostOrdermaster.objects.filter(custom_order_id=extracted_order_id).first()
        order_id = rs_order.id

        rs_record = EngageboostCcavenueUpgradedReturnDetails.objects.filter(order_id=order_id).update(payment_response_full=str_obj)


        try:
            str_obj_1 = "{\"" + str_obj + "\"}"
            str_json = json.loads(str_obj_1)
        except Exception as error:

            try:
                # str_obj = "{\""+str_obj+"\"}"
                str_json = json.loads(str_obj)
            except Exception as error:
                str_json = parse_payment_data(str_obj)


        return_transaction = pg.UpdateCcAvenuePaymentTransaction_si(str_json)

        print("return_transaction===", return_transaction)

        if str_json['order_status'].lower()=='success':
            # redirect_to = "http://15.185.126.44:82/success-payment/"+str_json['order_id']
            # redirect_to = "https://www.gogrocery.ae/success-payment/"
            redirect_to = "https://www.gogrocery.ae/checkout/success/"+str_json['order_id']
        else:
            redirect_to = "https://www.gogrocery.ae/failed-payment/"+str_json['order_id']+"/"+str_json['order_status']+"/"+str_json['status_message']+"/"+str_json['failure_message']

        pay_status = status.HTTP_200_OK
        response_data = {
            "status":pay_status,
            "transaction_id":str_json['tracking_id']
        }
        response_data = str(urlsafe_base64_encode(force_bytes(response_data)))
        response_data = response_data.replace("b","")
        response_data = response_data.replace("'","")
        vv = redirect_to+'?res='+response_data
        print("redirect url+++++++", vv)
        # return HttpResponse(str_obj)
        # return HttpResponse(redirect_to)
        # return HttpResponseRedirect(redirect_to=redirect_to+'?res='+response_data)
        return HttpResponseRedirect(redirect_to=redirect_to)