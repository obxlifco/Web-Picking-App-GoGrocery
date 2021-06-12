from webservices.models import EngageboostCustomers,EngageboostUsers
from django.http import Http404
from webservices.serializers import CustomerSerializer,UserSerializer
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
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from webservices.views import loginview

class CustomerInfoViewSet(generics.ListAPIView):
# """ List all customers, or create a new customers """
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        if request.method == 'POST':
            requestdata = JSONParser().parse(request)
            first_name = requestdata['first_name']
            last_name = requestdata['last_name']
            fullname = first_name+' '+last_name
            email = requestdata['email']
            password = requestdata['password']
            vat = requestdata['vat']
            customers_group = requestdata['customers_group']
            company_id = requestdata['company_id']
            hash_password =make_password(password, None, 'md5')
            cnt = EngageboostUsers.objects.using(company_db).filter(username=fullname,first_name=first_name).count()
            if  cnt == 0:
                    User = EngageboostUsers.objects.using(company_db).create(email=email,first_name=first_name,last_name=last_name,company_id='1',country_id='1',createdby_id='1',created_date=datetime.now(),modifiedby_id=1,modified_date=datetime.now(),last_login=datetime.now(),username=first_name,password='n',role_id=1,user_type='frontend')
                    obj = EngageboostUsers.objects.using(company_db).latest('id')
                    last_id = obj.id
                    created_by = requestdata['created_by']
                    modified_by = requestdata['modified_by']
                    website_id = requestdata['website_id']
                    isblocked = requestdata['isblocked']
                    Customer = EngageboostCustomers.objects.using(company_db).create(email=email,first_name=first_name,last_name=last_name,created=datetime.now(),modified=datetime.now(),password=hash_password,auth_user_id=last_id,vat=vat,website_id=website_id,orders=1,avgorder=1,totalorder=1,lastlogin=datetime.now(),is_guest_user=1,is_ledger_created='n',isblocked=isblocked)
                    data ={
                    'status':1,
                    'api_status':'',
                    'message':'Successfully Inserted',
                    }
                    return Response(data)
                 
            else:
                data ={
                'status':0,
                
                'message':'Username Alrady exists',
                }
               
class CustomerList(generics.ListAPIView):
# """ List all users, or create a new user """
#///////////////////Fetch Single Row
    def get(self, request, pk, format=None):
        company_db = loginview.db_active_connection(request)
        Customer = EngageboostCustomers.objects.using(company_db).get(id=pk)
            data ={
                'status':1,
                'email':Customer.email,
                'first_name':Customer.first_name,
                'message':'',
                }
        
        return Response(data)
    def put(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        Customer = EngageboostCustomers.objects.using(company_db).filter(id=pk).update(email=email,first_name=first_name,last_name=last_name,created=datetime.now(),modified=datetime.now(),password='n',auth_user_id=last_id,vat=vat,website_id=website_id,orders=1,avgorder=1,totalorder=1,lastlogin=datetime.now(),is_guest_user=1,is_ledger_created='n',isblocked=isblocked)
            data ={
            'status':1,
            'api_status':'',
            'message':'Successfully Updated',
            }
            return Response(data)
        else:
            data ={
            'status':0,
            'message':'Data Not Found',
            }
            return Response(data)
                    
            



