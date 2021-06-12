from webservices.models import EngageboostProducts
from django.http import Http404
from webservices.serializers import BasicinfoSerializer
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
from webservices.views import loginview

                    
       
class DefaultPriceList(generics.ListAPIView):
# """ List all Edit,Uodate Brand """
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostProducts.objects.using(company_db).get(pk=pk)
        except EngageboostProducts.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        user = self.get_object(pk,request)
        serializer = BasicinfoSerializer(user)
        
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
        serializer = BasicinfoSerializer(Category,data=serializer_data,partial=True)
        if serializer.is_valid():
            serializer.save()
            data ={
            'status':1,
            'api_status':pk,
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
                    
            

