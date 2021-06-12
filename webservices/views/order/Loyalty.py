from webservices.models import *
from django.db.models import Value
from django.db.models.functions import Concat
from django.http import Http404
from webservices.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import status
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from rest_framework.parsers import JSONParser
from datetime import datetime
from rest_framework import generics
# from itertools import chain
from django.core import serializers
# from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from webservices.views import loginview
from webservices.views.common import common
from webservices.views.emailcomponent import emailcomponent
from django.db.models import Q
import sys,math
import traceback
import json

# class LoyaltySet is used to insert Loyalty
class LoyaltySet(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		has_multy=request.data['value']
		error=[]
		
		if len(error)==0:	
			try:
				if has_multy['id']:
					loyalty_id = has_multy['id']
			except KeyError: 
					loyalty_id = ""		
			#is_mul = has_multy['has_multiplecoupons']
			d1={'created':datetime.now(),'modified':datetime.now()}
			serializer_data=dict(has_multy,**d1)
			
			if loyalty_id:
				serializer_data.pop("id")
				creditObj = EngageboostCreditPoint.objects.using(company_db).get(id=loyalty_id)
				serializer = CreditPointSerializer(creditObj,data=serializer_data,partial=True)
				if serializer.is_valid():
					serializer.save()
					data ={
					'status':1,
					'api_status':{"id":loyalty_id},
					'message':'Successfully Updated',
					}
					return Response(data)
				else:
					data ={
					'status':0,
					'api_status':serializer.errors,
					'message':'Data Not Found',
					}
					return Response(data)
			else:
				serializer = CreditPointSerializer(data=serializer_data,partial=True)
				if serializer.is_valid():
					serializer.save()
					obj = EngageboostCreditPoint.objects.using(company_db).latest('id')
					last_id = obj.id
					
					data ={
					'status':1,
					'api_status':{"id":last_id},
					'message':'Successfully Inserted',
					}
					return Response(data)
				else:
					data ={
					'status':0,
					'api_status':serializer.errors,
					'message':'Data Not Found',
					}
					return Response(data)		
		else:
			data ={
			'status':0,
			'api_status':error,
			'message':'Something went wrong',
			}
			return Response(data)			

# class LoyaltyConditions is used to insert Loyalty Conditions
class LoyaltyConditions(generics.ListAPIView):
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostCreditPointConditions.objects.using(company_db).get(loyalty_master_id=pk)
		except EngageboostCreditPointConditions.DoesNotExist:
			raise Http404

	def post(self, request, format=None):
		datas=[]
		company_db = loginview.db_active_connection(request)
		loyalty_master_id=request.data['loyalty_master_id']
		cnt=EngageboostCreditPointConditions.objects.using(company_db).filter(loyalty_master_id=loyalty_master_id).count()
		
		if cnt >0:
			EngageboostCreditPointConditions.objects.using(company_db).filter(loyalty_master_id=loyalty_master_id).delete()
		has_multy=request.data['value']
		for data in has_multy:
			# serializer_data = dict()
			has_record = EngageboostCreditPointConditions.objects.using(company_db).last()
			if has_record:
				last_entry_of_table = EngageboostCreditPointConditions.objects.order_by('-id').latest('id')
				row_id = int(last_entry_of_table.id)+int(1)
			else:
				row_id = 1
			d1={"id":row_id};
			data=dict(data,**d1)
			
			serializer = EngageboostCreditPointConditions.objects.using(company_db).create(**data)
			if serializer:
				# serializer.save()
				data ={
					'status':1,
					'api_status':'',
					'message':'Successfully Inserted',
				}
			else:
				data ={
					'status':0,
					'api_status':serializer.errors,
					'message':'Data Not Found',
				}
		return Response(data)

	def get(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		condition_array=[]
		# dis = self.get_object(pk,request)
		# serializer = CreditPointConditionsSerializer(dis)
		loyalties_count=EngageboostCreditPoint.objects.using(company_db).filter(id=pk,isdeleted='n',isblocked='n').count()
		if loyalties_count>0:
			conditions_count=EngageboostCreditPointConditions.objects.using(company_db).filter(loyalty_master_id=pk).count()
			if conditions_count>0:
				conditions_arr = EngageboostCreditPointConditions.objects.using(company_db).filter(loyalty_master_id=pk)
				conditions = CreditPointConditionsSerializer(conditions_arr, many=True)
				
				for condition in conditions.data:
					condition_array.append(condition)
		
				data ={
					'status':1,
					'api_status':condition_array,
					'message':'',
				}
			else:
				data ={
					'status':0,
					'api_status':"",
					'message':'Loyalty condition Not Found',
					}	
		else:
			data ={
				'status':0,
				'api_status':"",
				'message':'Loyalty Not Found',
				}
		return Response(data)	
	
# class DiscountList is used to fetch list of all  Discount
class LoyaltyList(generics.ListAPIView):
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostCreditPoint.objects.using(company_db).get(pk=pk)
		except EngageboostCreditPoint.DoesNotExist:
			raise Http404
	 #///////////////////Fetch Single Row
	
	def get(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		all_loyalty=[]
		dis = self.get_object(pk,request)
		serializer = CreditPointSerializer(dis)
		loyalties=EngageboostCreditPoint.objects.using(company_db).all().filter(id=pk)
		customergrp = EngageboostCustomerGroup.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
		customer = CustomerGroupSerializer(customergrp, many=True)
		for loyalty in loyalties:
			loyalty_array={'name':loyalty.name,
							'loyalty_desc':loyalty.loyalty_desc,
							'loyal_start_date':loyalty.loyal_start_date,
							'loyal_end_date':loyalty.loyal_end_date,
							'per_rupees':loyalty.per_rupees,
							'points':loyalty.points,
							'loyalty_expire_days':loyalty.loyalty_expire_days,
							'loyal_type':loyalty.loyal_type,
							'isblocked':loyalty.isblocked,
							'created':loyalty.created,
							'modified':loyalty.modified
							}
			all_loyalty.append(loyalty_array)
		if(serializer): 
			data ={
				'status':1,
				'api_status':serializer.data,
				'loyalties':all_loyalty,
				'customer_group':customer.data,
				'message':'',
				}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
		return Response(data)	
