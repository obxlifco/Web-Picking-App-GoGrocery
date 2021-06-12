from django.shortcuts import render
from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

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

from webservices.views.common import common
from frontapp.views.sitecommon import common_functions


class PaymentMethodList_old(APIView):
    permission_classes = []
    def get(self, request, format=None):
        user                = request.user
        user_id             = user.id
        device_id           = request.META.get('HTTP_DEVICEID')
        website_id = common_functions.get_company_website_id_by_url()
        final_data = []
        paymenttypes = EngageboostPaymentgatewayTypes.objects.all().filter(isdeleted='n',isblocked='n').order_by('order_by')
        menulist = PaymentMethodListSerializer(paymenttypes, many=True)
        ind = 0
        for menu in menulist.data:
            parentdata={}
            child={}
            childdata=[]
            value=[]
            # parentdata=menu
            Paymentmethods = EngageboostPaymentgatewayMethods.objects.all().filter(paymentgateway_type_id=menu['id'], isdeleted='n',isblocked='n')
            childmenulist = PaymentgatewayMethodsSerializer(Paymentmethods, many=True)
            for menu1 in childmenulist.data:
                # child=menu1
                Paymentmethods_website = EngageboostWebsitePaymentmethods.objects.filter(engageboost_company_website_id=website_id,engageboost_paymentgateway_method_id=menu1['id'], isdeleted='n',isblocked='n').order_by('setting_order_by').count()
                Paymentmethods_fields = EngageboostPaymentgatewaySettings.objects.all().filter(paymentgateway_method_id=menu1['id'], isdeleted='n',isblocked='n').order_by('setting_order_by')
                payment_field = PaymentgatewaySettingsSerializer(Paymentmethods_fields, many=True)
                if Paymentmethods_website==0:
                    child['is_checked']=0
                else:
                    menulist.data.pop(ind)
                    parentdata=menu
                    child=menu1
                    child['is_checked']=1
                    child['payment_field']=payment_field.data

                    index = 0
                    for payment_field in payment_field.data:
                            
                        payment_field_values = EngageboostPaymentgatewaySettingInformation.objects.filter(paymentgateway_setting_id=payment_field['id'], isdeleted='n',isblocked='n').first()
                        if payment_field_values:
                            child['payment_field'][index]['values'] = payment_field_values.setting_val
                        index = index +1
                    childdata.append(child)
                    parentdata['payment_method']=childdata
                    final_data.append(parentdata)
            ind = ind+1
        data ={
		
		    'api_status':final_data,
        }
        return Response(data)


class PaymentMethodList(APIView):
    def get(self, request, format=None):
        user = request.user
        user_id = user.id
        device_id = request.META.get('HTTP_DEVICEID')
        warehouse_id = request.META.get('HTTP_WAREHOUSE')
        website_id = common_functions.get_company_website_id_by_url()
        final_data = []
        # paymenttypes = EngageboostPaymentgatewayTypes.objects.all().filter(isdeleted='n',isblocked='n').order_by('order_by')
        # menulist = PaymentMethodListSerializer(paymenttypes, many=True)
        ind = 0
        # rs_web_pay_method = EngageboostWebsitePaymentmethods.objects.filter(isblocked = 'n', isdeleted='n').distinct('engageboost_paymentgateway_method_id').all()
        # rs_data = WebsitePaymentmethodsViewSerializer(rs_web_pay_method, many=True).data

        payment_option = EngageboostPaymentWarehouse.objects.filter(warehouse_id=warehouse_id, isblocked='n',
                                                                    isdeleted='n').values_list('payment_method_id',
                                                                                               flat=True)

        # print('warehouse id====>',request.META)
        print('warehouse id====>', warehouse_id)
        print('method count====>', payment_option)
        if len(payment_option) <= 0:
            rs_web_pay_method = EngageboostWebsitePaymentmethods.objects.filter(isblocked='n', isdeleted='n').distinct(
                'engageboost_paymentgateway_method_id').all()
            pay_type = WebsitePaymentmethodsViewSerializer(rs_web_pay_method, many=True).data
        else:
            rs_web_pay_method = EngageboostWebsitePaymentmethods.objects.filter(isblocked='n', isdeleted='n',
                                                                                engageboost_paymentgateway_method_id__in=payment_option).distinct(
                'engageboost_paymentgateway_method_id').all()
            pay_type = WebsitePaymentmethodsViewSerializer(rs_web_pay_method, many=True).data
        data = {

            'api_status': pay_type,
        }
        return Response(data)
