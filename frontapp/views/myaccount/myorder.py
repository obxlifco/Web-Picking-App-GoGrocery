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

class CancelOrder(APIView):
	def get(self, request, order_id, format=None):
		requestdata     = request.data
		user            = request.user
		user_id         = user.id
		warehouse_id    = request.META.get('HTTP_WAREHOUSE')
		website_id = 1
		if warehouse_id is None:
			warehouse_id = 2

		customer_id = None
		str_status = ""
		try:
			rs_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
			if rs_customer:
				customer_id = rs_customer.id
			else:
				raise Exception("Customer Not Found.")  
			rs_order = EngageboostOrdermaster.objects.filter(id=order_id,customer_id=customer_id,order_status__in=[0,20,99]).first()
			if rs_order:
				str_status = status.HTTP_200_OK
				EngageboostOrdermaster.objects.filter(id=order_id).update(order_status=2)
				elastic = common.save_data_to_elastic(order_id,'EngageboostOrdermaster')
				warehouse_id = rs_order.assign_wh
				rs_orderproduct = EngageboostOrderProducts.objects.filter(order_id=order_id)
				if rs_orderproduct:
					for products in rs_orderproduct:
						common.update_stock_all(products.product_id,warehouse_id,int(products.quantity),"Increase","real",order_id,website_id)

				data = {
					"status":str_status,
					"message":"success"
				}
				pass
			else:
				raise Exception("You can't cancel this order.")
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			str_status = status.HTTP_417_EXPECTATION_FAILED
			data = {"status":str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
		return Response (data,str_status)
	def post(self, request, order_id, format=None):
		requestdata     = JSONParser().parse(request)
		user            = request.user
		user_id         = user.id
		order_id		= requestdata['order_id']
		return_note		= requestdata['return_note']
		return_others_reason = ''
		if "return_others_reason" in requestdata:
			return_others_reason = requestdata['return_others_reason']
			if return_note == 'Others' and return_others_reason != '':
				return_note = return_others_reason

		website_id = 1
		customer_id = None
		str_status = ""
		try:
			rs_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
			if rs_customer:
				customer_id = rs_customer.id
			else:
				raise Exception("Customer Not Found.")
			rs_order = EngageboostOrdermaster.objects.filter(id=order_id,customer_id=customer_id,order_status__in=[0,20,99]).first()
			if rs_order:
				str_status = status.HTTP_200_OK
				EngageboostOrdermaster.objects.filter(id=order_id).update(order_status=2, return_note=return_note)
				elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'order_status':2,'return_note':return_note})
				# Cancel Mail
				common.email_send_by_AutoResponder(order_id, 16)
								
				# Cancel SMS
				common.sms_send_by_AutoResponder(order_id, None, 16)
				warehouse_id = rs_order.assign_wh
				rs_orderproduct = EngageboostOrderProducts.objects.filter(order_id=order_id)
				if rs_orderproduct:
					for products in rs_orderproduct:
						common.update_stock_all(products.product_id,warehouse_id,int(products.quantity),"Increase","real",order_id,website_id)
				data = {
					"status":str_status,
					"message":"success"
				}
				pass
			else:
				raise Exception("You can't cancel this order.")
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			str_status = status.HTTP_417_EXPECTATION_FAILED
			data = {"status":str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
		return Response (data,str_status)