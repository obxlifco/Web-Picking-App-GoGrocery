from webservices.models import EngageboostPurchaseOrdersShippingMethods
from django.http import Http404
from webservices.serializers import PurchaseOrdersShippingMethodSerializer
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
from django.db.models import Q  
from webservices.views import loginview

class ShippingMethod(generics.ListAPIView):
# """ Add New Brand """
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        d1={'created':datetime.now().date(),'modified':datetime.now().date()}
        d2=request.data
        serializer_data=dict(d2,**d1)
        cnt_name = EngageboostPurchaseOrdersShippingMethods.objects.using(company_db).filter(name=request.data['name']).count()
        if  cnt_name == 0:
            serializer = PurchaseOrdersShippingMethodSerializer(data=serializer_data,partial=True)
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
            'message':'Shipping Method Name is already exists',
            }
            return Response(data)
class ShippingMethodList(generics.ListAPIView):
# """ List all Edit,Uodate Brand """
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostPurchaseOrdersShippingMethods.objects.using(company_db).get(pk=pk)
        except EngageboostPurchaseOrdersShippingMethods.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        user = self.get_object(pk,request)
        serializer = PurchaseOrdersShippingMethodSerializer(user)
        if(serializer): 
            data ={
                'status':1,
                'api_status':serializer.data,
                
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
        d1={'modified':datetime.now().date()}
        d2=request.data
        serializer_data=dict(d2,**d1)
        cnt_name = EngageboostPurchaseOrdersShippingMethods.objects.using(company_db).filter(name=request.data['name'],isdeleted='n').filter(~Q(id=pk)).count()
        if  cnt_name == 0:
            serializer = PurchaseOrdersShippingMethodSerializer(Category,data=serializer_data,partial=True)
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
            'message':'Shipping Method Name is already exists',
            }
            return Response(data)