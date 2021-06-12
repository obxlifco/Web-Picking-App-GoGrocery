from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from datetime import datetime
import datetime
import pytz
from datetime import timezone

from webservices.models import *
from coremodule.coremodule_serializers import *
import json
import random
import string

import pytz

from django.utils import timezone

class CustomerListView(generics.ListAPIView):

	def get(self, request, format=None):
		website_id = request.META.get('HTTP_WID')
		if website_id:
			pass 
		else: 
			website_id = 1
		search_data =   request.GET.get('search_data')
		customerObj = EngageboostCustomers.objects.filter(isdeleted='n', isblocked='n', website_id=website_id)
		if search_data!=None:
			customerObj = customerObj.filter( Q(first_name__contains=search_data) | Q(last_name__contains=search_data)| Q(email__contains=search_data)| Q(phone__contains=search_data))

		rs_customer 	= customerObj.all().order_by('-id')
		customer_data 	= CustomerListSerializer(rs_customer, many=True)
		customer_data 	= customer_data.data	
		cus_data =[]
		if customer_data:			
			for customerdata in customer_data:				
				customer_datas = {
							"first_name" : customerdata['first_name'],
							"last_name" : customerdata['last_name'],
							"email" : customerdata['email'], 
							"phone" : customerdata['phone'],  
							"auth_user_id" :  customerdata['auth_user_id'],       
							"address_one" : customerdata['address'],
							"address_two" : customerdata['street'],
							"website_id" :customerdata['website_id'],
							"created" : customerdata['created'],
							"modified" : customerdata['modified']
				}
				cus_data.append(customer_datas)
			data = {
				"status":1,
				"msg":"success",				
				"customers" :cus_data				
			}
		else:
			 data ={
				"status":0,
				"msg" :"No Data Found.",
				"customers" :[]			
			}
		
		return Response (data)

	def post(self, request, format=None):
		website_id = request.META.get('HTTP_WID')	
		if website_id:
			pass 
		else: 
			website_id 	= 1				
			requestdata = JSONParser().parse(request)			
			user_name	  = randomString()
			first_name  = requestdata['first_name']
			last_name 	= requestdata['last_name']
			email 		  = requestdata['email']
			address_one = requestdata['address_one']
			address_two = requestdata['address_two']
			phone = requestdata['mob_no']
			if address_one =="":
				address_one = ""
			if address_two == "":
					address_two = ""		
			if email !="":
				email = requestdata['email']
			else:					
				email = requestdata['mob_no']+'@pos.com'		
			if first_name == "":
				first_name = ""
			if last_name == "":
				last_name = ""

			# created_date = datetime.now().astimezone()			
			email = requestdata['mob_no']+'@pos.com'					
			# created_date = datetime.now()
			# created_date = pytz.timezone('UTC')
			# utc = timezone.utc
			created_date = datetime.now().astimezone()							
			data={
				'first_name':first_name,
				'last_name':last_name,			
				'username': user_name,	
				'email':email,
				'phone':phone,
				'created_date':created_date,
				'modified_date':created_date
			}
			customerObj = EngageboostUsers.objects.filter(isdeleted='n', isblocked='n',phone=phone).count()				
			if customerObj !=0:
				data1 ={
					"status":0,
					"msg" :"Phone nos allready exists.",
					"data":data	
				}	
			else:	
				insertAuth 	= EngageboostUsers.objects.create(**data)			
				latestID 	= EngageboostUsers.objects.latest('id')
				customerData={'auth_user_id':latestID.id,
								'created':created_date,
								'modified':created_date,
								'address':address_one,
								'street' :address_two,
								'website_id':website_id							
							}
				data=dict(data,**customerData)					
				data.pop('username')
				data.pop('created_date')
				data.pop('modified_date')				
				insertCustomer = EngageboostCustomers.objects.create(**data)
				data1 ={
					"status":1,
					"msg" :"success",
					"data":data				
				}		

			return Response (data1)

def randomString(stringLength=6):
	"""Generate a random string of fixed length """
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(stringLength))

	


