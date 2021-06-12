from webservices.models import EngageboostEmktContactlists,EngageboostCountries
from django.http import Http404
from webservices.serializers import EmktContactlistsSerializer,GlobalsettingscountriesSerializer
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

class ContactViewSet(generics.ListAPIView):
# """ Create New Contact Group """
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        d1={'created':datetime.now().date(),'modified':datetime.now().date()}
        d2=request.data
        cnt = EngageboostEmktContactlists.objects.using(company_db).filter(company_website_id=request.data['company_website_id'],name=request.data['name'],isdeleted='n').count()
        if cnt == 0:
            serializer_data=dict(d2,**d1)
            serializer = EmktContactlistsSerializer(data=serializer_data,partial=True)
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
            'message':'Contact Group name is already exists',
            }
            return Response(data)
#                     
class ContactList(generics.ListAPIView):
# """ List all Contract Groups"""
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostEmktContactlists.objects.using(company_db).get(pk=pk)
        except EngageboostEmktContactlists.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        user = self.get_object(pk,request)
        serializer_get = EmktContactlistsSerializer(user)
        settings1 = EngageboostCountries.objects.using(company_db).all().filter(country_name='India')
        serializer1 = GlobalsettingscountriesSerializer(settings1, many=True)
        settings = EngageboostCountries.objects.using(company_db).all().filter(~Q(country_name='India')).order_by('country_name')
        serializer = GlobalsettingscountriesSerializer(settings, many=True)
        d1=serializer1.data
        d2 = serializer.data
        data=d1+d2
        if(serializer): 
            data ={
                'status':1,
                'api_status':serializer_get.data,
                'countries':data,
                'message':'',
                }
        else:
            data ={
                'status':0,
                'api_status':serializer.errors,
                'message':'Data Not Found',
                }
        return Response(data)


 # """ Update all Contract Groups"""   
    def put(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        Category = self.get_object(pk,request)
        d1={'modified':datetime.now().date()}
        d2=request.data
        cnt = EngageboostEmktContactlists.objects.using(company_db).filter(company_website_id=request.data['company_website_id'],name=request.data['name'],isdeleted='n').filter(~Q(id=pk)).count()
        if cnt == 0:
            serializer_data=dict(d2,**d1)
            serializer = EmktContactlistsSerializer(Category,data=serializer_data,partial=True)
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
            'message':'Contact Group name is already exists',
            }
            return Response(data)