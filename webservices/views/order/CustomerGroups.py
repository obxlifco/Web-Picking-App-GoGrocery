from webservices.models import *
from django.http import Http404
from webservices.serializers import *
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

class Customers(generics.ListAPIView):
    def get(self, request, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        settings = EngageboostCustomers.objects.using(company_db).all()
        serializer = CustomerSerializer(settings,many=True)
        if(serializer): 
            data ={
                'customer':serializer.data,
                }
            return Response(data)
    def post(self, request, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        order_type=request.data['order_type']
        order_by=request.data['order_by']
        key=request.data['search']
        website_id = int(request.data['website_id'])
        company_id = int(request.data['company_id'])
        id_array=[0]
        if(order_type=='+'):
            order=order_by
        elif(order_type=='-'):
            order='-'+order_by

        if(key):
            result = EngageboostCustomers.objects.using(company_db).filter(isblocked='n',isdeleted='n').filter(Q(first_name__icontains=key)|Q(last_name__icontains=key)|Q(email__icontains=key)).order_by(order)
        else: 
            result = EngageboostCustomers.objects.using(company_db).filter(isblocked='n',isdeleted='n').order_by(order)

        page = self.paginate_queryset(result)
        if page is not None:            
            serializer = CustomerSerializer(page,many=True)           
            final_data=[]           
            final_data.append({'result':serializer.data})
            return self.get_paginated_response(final_data) 
        else:
            return self.get_paginated_response({})

class CustomerGroup(generics.ListAPIView):
# """ Add New PaymentMethod """
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        d1={'created':datetime.now(),'modified':datetime.now()}
        d2=request.data
        
        if 'name' in d2.keys() and d2['name']!="" and d2['name']!=None:
            serializer_data=dict(d2,**d1)
            serializer = CustomerGroupSerializer(data=serializer_data,partial=True)
            if serializer.is_valid():
                serializer.save()
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
            'api_status':'',
            'message':'Enter name',
            }
            return Response(data)        
        
class CustomerGroupList(generics.ListAPIView):
# """ List all Edit,Uodate PaymentMethod """
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostCustomerGroup.objects.using(company_db).get(pk=pk)
        except EngageboostCustomerGroup.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        user = self.get_object(pk,request)
        serializer = CustomerGroupSerializer(user)
        # settings1 = EngageboostCustomers.objects.using(company_db).all()
        # serializer1 = CustomerSerializer(settings1,many=True)
        if(serializer): 
            data ={
                'status':1,
                'api_status':serializer.data,
                # 'customer':serializer1.data,
                'message':'',
                }
        else:
            data ={
                'status':0,
                'api_status':serializer.errors,
                'message':'Data Not Found',
                }
        return Response(data)
    
    def put(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        Category = self.get_object(pk,request)
        d1={'modified':datetime.now()}
        d2=request.data
        if 'name' in d2.keys() and d2['name']!="" and d2['name']!=None:
            serializer_data=dict(d2,**d1)
            serializer = CustomerGroupSerializer(Category,data=serializer_data,partial=True)
            if serializer.is_valid():
                serializer.save()
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
            'api_status':'',
            'message':'Enter name',
            }
            return Response(data)        
                        
            



