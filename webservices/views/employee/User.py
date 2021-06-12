from webservices.models import EngageboostUsers,EngageboostRolemasters, EngageboostCustomers, EngageboostWarehouseManager
from django.http import Http404
from webservices.serializers import UserSerializer,RoleSerializer,CustomerSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpRequest
import json
import random
from django.db.models import Q
from rest_framework.renderers import JSONRenderer
from django.utils.six import BytesIO
from django.contrib.auth.hashers import make_password,check_password
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from rest_framework import filters
from datetime import datetime
from django.utils import timezone
from webservices.views import loginview
import smtplib

class UserList(generics.ListAPIView):
# """ List all users with pagination,sorting and searching """
	# queryset = EngageboostUsers.objects.using(company_db).select_related('role')
	# serializer_class = UserSerializer
	# # print(HttpRequest.get('table_name'))
	# # users = EngageboostUsers.objects.using(company_db).select_related('role').filter(isdeleted='n').order_by('-id')
	# filter_backends = (filters.SearchFilter,)
	# search_fields = ('first_name','last_name')
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		# /////////Create Query
		if request.data.get('search') and request.data.get('order_by'):
			key=request.data.get('search')
			order_by=request.data.get('order_by')
			order_type=request.data.get('order_type')
			if(order_type=='+'):
				order=order_by
			else:
				order='-'+order_by
			users = EngageboostUsers.objects.using(company_db).select_related('role').filter(isdeleted='n').filter(Q(first_name__contains=key)|Q(last_name__contains=key)|Q(email__contains=key)|Q(business_name__contains=key)|Q(employee_name__contains=key)|Q(designation__contains=key)|Q(city__contains=key)|Q(state__contains=key)|Q(postcode__contains=key)|Q(phone__contains=key)).order_by(order)
		elif request.data.get('search'):
			key=request.data.get('search')
			users = EngageboostUsers.objects.using(company_db).select_related('role').filter(isdeleted='n').filter(Q(first_name__contains=key)|Q(last_name__contains=key)|Q(email__contains=key)|Q(business_name__contains=key)|Q(employee_name__contains=key)|Q(designation__contains=key)|Q(city__contains=key)|Q(state__contains=key)|Q(postcode__contains=key)|Q(phone__contains=key)).order_by('-id')
		elif request.data.get('order_by'):
			order_by=request.data.get('order_by')
			order_type=request.data.get('order_type')
			if(order_type=='+'):
				order=order_by
			else:
				order='-'+order_by
			users = EngageboostUsers.objects.using(company_db).select_related('role').filter(isdeleted='n').order_by(order)    
		else:
			users = EngageboostUsers.objects.using(company_db).select_related('role').filter(isdeleted='n').order_by('-id')
		# /////////Create Pagination    
		page = self.paginate_queryset(users)

		if page is not None:
			serializer = UserSerializer(page, many=True)
			return self.get_paginated_response(serializer.data) 
		serializer = self.UserSerializer(users, many=True)
		return Response(serializer.data)

class UserAction(generics.ListAPIView):
# """ Create a new user"""

	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		if request.method == 'POST':
			requestdata = JSONParser().parse(request)
			first_name = requestdata['first_name']
			last_name = requestdata['last_name']
			employee_name = requestdata['employee_name']
			fullname = first_name+' '+last_name
			email = requestdata['email']
			password = requestdata['password']
			hash_password =make_password(password, None, 'md5')
			designation = requestdata['designation']
			role_id = requestdata['role_id']
			ip = requestdata['ip_address']
			isblocked = requestdata['isblocked']
			reset_password = requestdata['reset_password']
			send_password = requestdata['send_password']

			created = requestdata['createdby_id']
			modified = requestdata['modifiedby_id']
			username = requestdata['username']
			phone = requestdata['phone']
			website_id = requestdata['website_id']
			warehouse_id = 0
			if "warehouse_id" in requestdata:
				warehouse_id = requestdata['warehouse_id']


			email_user = email.split('@')
			cnt_email = EngageboostUsers.objects.using(company_db).filter(email=email,isdeleted='n',isblocked='n').count()
			if  cnt_email == 0:
				cnt1 = EngageboostUsers.objects.using(company_db).filter(username=username).count()
				if  cnt1 == 0:
					cnt = EngageboostUsers.objects.using(company_db).filter(phone=phone,isdeleted='n',isblocked='n').count()
					if  cnt == 0:
						if role_id == 1:
							User = EngageboostUsers.objects.using(company_db).create(phone=phone,
																					 last_login=timezone.now(),
																					 email=email,
																					 first_name=first_name,
																					 last_name=last_name,
																					 company_id='1', country_id='1',
																					 createdby_id=created,
																					 modifiedby_id=modified,
																					 isblocked=isblocked, isdeleted='n',
																					 username=username,
																					 employee_name=employee_name,
																					 designation=designation,
																					 password=hash_password,
																					 role_id=role_id,
																					 reset_password=reset_password,
																					 user_type='backend', ip_address=ip,
																					 created_date=timezone.now(),
																					 modified_date=timezone.now(),
																					 issuperadmin='Y',
																					 is_superuser=True,
																					 website_id=website_id,
																					 warehouse_id=warehouse_id)
						else:
							User = EngageboostUsers.objects.using(company_db).create(phone=phone,last_login=timezone.now(),email=email,
								first_name=first_name,last_name=last_name,company_id='1',country_id='1',createdby_id=created,
								modifiedby_id=modified,isblocked=isblocked,isdeleted='n',username=username,employee_name=employee_name,
								designation=designation,password=hash_password,role_id=role_id,reset_password=reset_password,
								user_type='backend',ip_address=ip,created_date=timezone.now(),modified_date=timezone.now(), issuperadmin='N', is_superuser=False, website_id=website_id, warehouse_id=warehouse_id)

						if send_password == 1:							
							from_email = 'admin@boostmysale.com'
							to_addr_list = email
							subject = 'Thank you for being a part of us'
							html_content = 'Your Password is :'+password							
							msg = EmailMultiAlternatives(subject, html_content, from_email, [to_addr_list])
							msg.attach_alternative(html_content, "text/html")
							msg.send()
							
						data = {
						'status':1,
						'message':"Successfully Inserted"
						}
						return JsonResponse(data)
					else:
						data ={
						'status':0,
						'message':'Phone Number is already exists',
						}
						return Response(data)   
				else:
					data ={
					'status':0,
					'message':'User name is already exists',
					}
					return Response(data)
			else:
				data ={
				'status':0,
				'message':'Email Id is already exists',
				}
				return Response(data)  
		

class UserDetail(APIView):
# """Retrieve, update  a user instance."""
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostUsers.objects.using(company_db).get(pk=pk)
		except EngageboostUsers.DoesNotExist:
			raise Http404
	#///////////////////Fetch Single Row
	def get(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		user = self.get_object(pk,request)
		serializer = UserSerializer(user)
		settings = EngageboostRolemasters.objects.using(company_db).all().filter(isdeleted='n', isblocked='n').order_by('name')
		serializer1 = RoleSerializer(settings, many=True)
		if(serializer): 
			data ={
				'status':1,
				'api_status':serializer.data,
				'role':serializer1.data,
				'message':'',
				}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
		return Response(data)

	#///////////////////Update All Fields  
	
	def put(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		user = self.get_object(pk,request)
		role = request.data['role_id']
		phone = request.data['phone']
		email = request.data['email']
		send_password = request.data['send_password']
		website_id = request.data['website_id']
		# print(rr)
		cnt_email = EngageboostUsers.objects.using(company_db).filter(email=email).filter(~Q(id=pk)).count()
		if  cnt_email == 0:
			cnt = EngageboostUsers.objects.using(company_db).filter(phone=phone).filter(~Q(id=pk)).count()
			if  cnt == 0:
				if request.data['password'] == '':
					password=EngageboostUsers.objects.using(company_db).get(id=pk)
					d1={'modified_date':datetime.now(),'password':password.password}
					d2=request.data
					serializer_data=dict(d2,**d1)
					serializer = UserSerializer(user,data=serializer_data,partial=True)
					if serializer.is_valid():

						serializer.save()
						
						userudates = EngageboostUsers.objects.using(company_db).filter(id=pk).update(role=role)
					   
						data ={
						'status':1,
						'api_status':serializer.data,
						'message':'Successfully Updated',
						}
					else:
						data ={
						'status':0,
						'api_status':serializer.errors,
						'message':'Data Not Found',
						}
					return Response(data) 
				else:
					
					d1={'modified_date':datetime.now()}
					d2=request.data
					email=request.data['email']
					# print(email)
					send_password = request.data['send_password']
					# print(send_password)
					if send_password == 1:
						send_password = request.data['send_password']
						
						server = smtplib.SMTP('smtp.gmail.com', 587)
						server.starttls()
						server.login("subhasis.debnath@navsoft.in", "sdchelsea")
						
						from_addr = 'subhasis.debnath@navsoft.in'
						to_addr_list = email
						cc_addr_list = 'subhasis.debnath@navsoft.in'
						subject = 'Thank you for being a part of us'
						msg = 'Your Password is :'+request.data['password']
						message = 'Subject: {}\n\n{}'.format(subject, msg)
						
						server.sendmail(from_addr,to_addr_list,message)
						server.quit()
						
						# subject, from_email, to = 'Password', 'subhasis.debnath@navsoft.in', email
						# text_content = 'Boostmysale Password'
						# html_content = 'Your Password is :'+password
						# msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
						# msg.attach_alternative(html_content, "text/html")
						# msg.send()
							
					serializer_data=dict(d2,**d1)
					serializer = UserSerializer(user,data=serializer_data,partial=True)
					if serializer.is_valid():
						serializer.save()
						EngageboostUsers.objects.using(company_db).filter(id=pk).update(password=make_password(request.data['password'], None, 'md5'))            
						rr = EngageboostUsers.objects.using(company_db).filter(id=pk).update(role_id=role)
						
						
						data ={
						'status':1,
						'api_status':serializer.data,
						'message':'Successfully Updated',
						}
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
				'message':'Phone Number is already exists',
				}
				return Response(data)   
		else:
			data ={
			'status':0,
			'message':'Email Id is already exists',
			}
			return Response(data)     

class UserChangePassword(APIView):
	#############Change Password
	def put(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		user = EngageboostUsers.objects.using(company_db).get(pk=pk)
		old_password = request.data['old_password']
		reset_password = request.data['reset_password']
		print(reset_password)
		password_check=user.check_password(old_password)
		new_password = make_password(request.data['new_password'], None, 'md5')
		if password_check ==True:
			serializer_data={'modified_date':datetime.now(),'password':new_password,'reset_password':reset_password}
			serializer = UserSerializer(user,data=serializer_data,partial=True)
			if serializer.is_valid():
				serializer.save()
				data ={
				'status':1,
				'api_status':serializer.data,
				'message':'Successfully Updated',
				}
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
				'api_status':'Sorry! Old Password does not match',
				'message':'Sorry! Old Password does not match',
				}
			return Response(data)
class FileUploadView(APIView):
	# parser_classes = (FileUploadParser)
	def put(self, request, filename, format=None):
		company_db = loginview.db_active_connection(request)
		file_obj = request.data['file']
		# ...
		# do some stuff with uploaded file
		# ...
		return Response(status=204)
# This method is used to assign role
class RoleAssign(APIView):
	def get(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		warehouse_id =0
		user    = request.user
		user_id = user.id
		rs_wh_manager = EngageboostWarehouseManager.objects.filter(manager_id = user_id).first()
		if rs_wh_manager:
			warehouse_id = rs_wh_manager.warehouse_id
		if warehouse_id is not None and int(warehouse_id) >0:
			settings = EngageboostRolemasters.objects.using(company_db).all().filter(isdeleted='n', isblocked='n',
																					 warehouse_id=warehouse_id).order_by('name')
		else:
			settings = EngageboostRolemasters.objects.using(company_db).all().filter(isdeleted='n',
																					 isblocked='n').order_by('name')

		serializer = RoleSerializer(settings, many=True)
		return Response(serializer.data)
# This method is used to get custer name from customer id

class CustomerDataFetch(generics.ListAPIView):
	def post(self, request, format=None):		
		company_db = loginview.db_active_connection(request)
		required_chk = blank_field_check('customer_id',request.data)
		if required_chk == 1:
			customer_id_arr = str(request.data['customer_id']).split(",")
			if len(customer_id_arr) > 0:
				find_all_customer = EngageboostCustomers.objects.using(company_db).filter(Q(id__in=customer_id_arr))
				if find_all_customer.count() > 0:
					customers = CustomerSerializer(find_all_customer,many=True,partial=True)
					data ={
					'status':1,
					'api_status':customers.data,
					'message':'Customer found',
					}
				else:
					data ={
					'status':0,
					'api_status':'',
					'message':'No customer found',
					}
			else:
				data ={
					'status':0,
					'api_status':'',
					'message':'No customer found',
					}
		else:
			data ={
				'status':0,
				'api_status':'',
				'message':'Invalid response',
				}
		return Response(data)

def blank_field_check(required_field,received_data):
	# required_field is "," seperated required fields
	# received_data is array based data received from frontend
	try:
		if required_field !='' and required_field is not None:
			splited_fields = required_field.split(",")
			if len(splited_fields)>0:
				no_of_required_fields = len(splited_fields)
				counter_success = 0
				for single_field_name in splited_fields:
					if single_field_name in received_data and received_data[single_field_name] !='' and received_data[single_field_name] is not None:			
						counter_success = counter_success + 1
				if counter_success == no_of_required_fields:
					return 1
		return 0
	except:
		return 0

def blank_field_check_or_condition(required_field,received_data):
	# required_field is "," seperated required fields
	# received_data is array based data received from frontend
	try:
		if required_field !='' and required_field is not None:
			splited_fields = required_field.split(",")
			if len(splited_fields)>0:
				no_of_required_fields = len(splited_fields)
				counter_success = 0
				for single_field_name in splited_fields:
					if single_field_name in received_data and received_data[single_field_name] !='' and received_data[single_field_name] is not None:			
						counter_success = counter_success + 1
				if counter_success >0:
					return 1
		return 0
	except:
		return 0

