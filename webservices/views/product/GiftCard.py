from webservices.models import *
from django.http import Http404
from webservices.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import date,datetime
from rest_framework import generics
from itertools import chain
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Q 
from django.core.files.storage import FileSystemStorage
from webservices.views import loginview
from django.utils import timezone
import datetime
import json
import random
import os


# class GiftCard is used to insert GiftCard
class GiftCard(generics.ListAPIView):
	def get(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		obj = EngageboostGiftCardMasters.objects.using(company_db)
		objcount = obj.filter(id=pk).count()
		if objcount>0:
			creditObj = obj.get(id=pk)
			serializer = GiftCardMastersSerializer(creditObj,partial=True)
			if(serializer): 
				data ={
						'status':1,
						'api_status':serializer.data,
					}
			else:
				data ={
						'status':0,
						'api_status':serializer.errors,
						'message':'Data Not Found',
					}
		else:
			data ={
					'status':0,
					'api_status':"",
					'message':'Data Not Found',
				}			
		return Response(data)

	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		has_multy=request.data
		serializer_data = has_multy
		
		if not 'card_name' in serializer_data.keys() or serializer_data['card_name']=="" or serializer_data['card_name']==None:
			data ={
			'status':0,
			'api_status':"",
			'message':'Enter Card Name',
			}
			return Response(data)
		if not 'amount' in serializer_data.keys() or serializer_data['amount']=="" or serializer_data['amount']==None:
			data ={
			'status':0,
			'api_status':"",
			'message':'Enter Amount',
			}
			return Response(data)
		if not 'start_date' in serializer_data.keys() or serializer_data['start_date']=="" or serializer_data['start_date']==None:
			data ={
			'status':0,
			'api_status':"",
			'message':'Enter Start Date',
			}
			return Response(data)
		if not 'end_date' in serializer_data.keys() or serializer_data['end_date']=="" or serializer_data['end_date']==None:
			data ={
			'status':0,
			'api_status':"",
			'message':'Enter End Date',
			}
			return Response(data)		


		if len(serializer_data['coupon_code']) > 0:
			for couponcode in serializer_data['coupon_code']:
				insert_data = {}
				insert_data = {
					"card_number":couponcode['coupon_code'],
					"card_name": serializer_data['card_name'],
					"amount" : serializer_data['amount'],
					"start_date":serializer_data['start_date'],
					"end_date":serializer_data['end_date'],
					"modifiedby":1,					
					"website_id":serializer_data['website_id'],
					"isblocked":'n',
					"isdeleted":'n',
					"created":timezone.now(),
					"modified":timezone.now()
				}
				EngageboostGiftCardMasters.objects.create(**insert_data)	
		
			
			data ={
			'status':1,			
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

	def put(self, request, pk=None, format=None):
		company_db = loginview.db_active_connection(request)
		has_multy=request.data
		serializer_data = has_multy
		
		if not 'card_number' in serializer_data.keys() or serializer_data['card_number']=="" or serializer_data['card_number']==None:
			data ={
			'status':0,
			'api_status':"",
			'message':'Enter Card Number',
			}
			return Response(data)
		if not 'card_name' in serializer_data.keys() or serializer_data['card_name']=="" or serializer_data['card_name']==None:
			data ={
			'status':0,
			'api_status':"",
			'message':'Enter Card Name',
			}
			return Response(data)
		if not 'amount' in serializer_data.keys() or serializer_data['amount']=="" or serializer_data['amount']==None:
			data ={
			'status':0,
			'api_status':"",
			'message':'Enter Amount',
			}
			return Response(data)
		if not 'start_date' in serializer_data.keys() or serializer_data['start_date']=="" or serializer_data['start_date']==None:
			data ={
			'status':0,
			'api_status':"",
			'message':'Enter Start Date',
			}
			return Response(data)
		if not 'end_date' in serializer_data.keys() or serializer_data['end_date']=="" or serializer_data['end_date']==None:
			data ={
			'status':0,
			'api_status':"",
			'message':'Enter End Date',
			}
			return Response(data)

		if pk:
			tax_id = pk		
			
			d1={'modified':datetime.datetime.now()}
			serializer_data=dict(has_multy,**d1)

			creditObj = EngageboostGiftCardMasters.objects.using(company_db).get(id=tax_id)
			serializer = GiftCardMastersSerializer(creditObj,data=serializer_data,partial=True)
			if serializer.is_valid():
				serializer.save()
				data ={
				'status':1,
				'api_status':{"id":tax_id},
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
			data ={
				'status':0,
				'api_status':"",
				'message':'Send Gift Card ID',
			}
			return Response(data)