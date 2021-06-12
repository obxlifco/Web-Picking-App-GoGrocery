from webservices.models import EngageboostEmktContacts,EngageboostEmktContactlists,EngageboostCountries
from django.http import Http404
from webservices.serializers import ContactsSerializer,EmktContactlistsSerializer,GlobalsettingscountriesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime
from rest_framework import generics
from itertools import chain
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse
from webservices.views import loginview

class ContactsSetView(generics.ListAPIView):
# """ Create New Contact List """

	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		d1={'created':datetime.now().date(),'modified':datetime.now().date()}
		d2=request.data
		serializer_data=dict(d2,**d1)
		cnt = EngageboostEmktContacts.objects.using(company_db).filter(company_website_id=request.data['company_website_id'],email=request.data['email'],isdeleted='n').count()
		if cnt == 0:
			serializer = ContactsSerializer(data=serializer_data,partial=True)
			if serializer.is_valid():
				serializer.save()
				obj = EngageboostEmktContacts.objects.using(company_db).latest('id')
				last_id = obj.id
				EngageboostEmktContacts.objects.using(company_db).filter(id=last_id).update(contact_list_id=request.data['contact_list_id'],country_id=request.data['country_id'])
				data ={
				'status':1,
				'api_status':'',
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
			'message':'Email Id is already exists',
			}
			return Response(data)			
	   
class ContactsList(generics.ListAPIView):
# """ List all Contract List"""
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostEmktContacts.objects.using(company_db).get(pk=pk)
		except EngageboostEmktContacts.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		user = self.get_object(pk,request)
		serializer = ContactsSerializer(user)
		settings1 = EngageboostEmktContactlists.objects.using(company_db).all()
		serializer2 = EmktContactlistsSerializer(settings1,many=True)
		settings12 = EngageboostCountries.objects.using(company_db).all().filter(country_name='India')
		serializer12 = GlobalsettingscountriesSerializer(settings12, many=True)
		settings13 = EngageboostCountries.objects.using(company_db).all().filter(~Q(country_name='India')).order_by('country_name')
		serializer13 = GlobalsettingscountriesSerializer(settings13, many=True)
		d1=serializer12.data
		d2 = serializer13.data
		data=d1+d2
		
		if(serializer): 
			data ={
				'status':1,
				'api_status':serializer.data,
				'ContactsList':serializer2.data,
				'Countries':data,
				}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
		return Response(data)


	# """ Update all Contract List"""  
	def put(self, request, pk, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		Category = self.get_object(pk,request)

	
		d1={'modified':datetime.now().date()}
		d2=request.data
		serializer_data=dict(d2,**d1)
		cnt = EngageboostEmktContacts.objects.using(company_db).filter(company_website_id=request.data['company_website_id'],email=request.data['email'],isdeleted='n').filter(~Q(id=pk)).count()
		if cnt == 0:
			serializer = ContactsSerializer(Category,data=serializer_data,partial=True)
			if serializer.is_valid():
				serializer.save()
				EngageboostEmktContacts.objects.using(company_db).filter(id=pk).update(contact_list_id=request.data['contact_list_id'],country_id=request.data['country_id'])
				data ={
				'status':1,
				'api_status':'',
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
			'message':'Email Id is already exists',
			}
			return Response(data)				
# """ Api of all Contacts"""  		 
class Contacts(generics.ListAPIView):

	def get(self, request, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		settings1 = EngageboostEmktContactlists.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
		serializer2 = EmktContactlistsSerializer(settings1,many=True)
		settings12 = EngageboostCountries.objects.using(company_db).all().filter(country_name='India')
		serializer12 = GlobalsettingscountriesSerializer(settings12, many=True)
		settings13 = EngageboostCountries.objects.using(company_db).all().filter(~Q(country_name='India')).order_by('country_name')
		serializer13 = GlobalsettingscountriesSerializer(settings13, many=True)
		d1=serializer12.data
		d2 = serializer13.data
		data=d1+d2
		if(serializer2): 
			data ={
				'ContactsList':serializer2.data,
				'Countries':data,
				}
			return Response(data)