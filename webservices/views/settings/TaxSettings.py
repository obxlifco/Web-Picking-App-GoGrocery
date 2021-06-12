from webservices.models import EngageboostTaxSettings
from django.http import Http404
from django.db.models import Q
from webservices.serializers import Taxsettings
from rest_framework.views import APIView
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime
from rest_framework import generics
from rest_framework.response import Response
from webservices.views import loginview

class Taxsettingsview(APIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        d1={'created':datetime.now().date(),'modified':datetime.now().date()}
        d2=request.data
        serializer_data=dict(d2,**d1)
        serializer = Taxsettings(data=serializer_data,partial=True)
        if serializer.is_valid():
            serializer.save()
            data ={
            'status':1,
            'api_status':'',
            'Message':'Successfully Inserted',
            }
            return Response(data)
        else:
            data ={
            'status':0,
            'api_status':serializer.errors,
            'Message':'Data Not Found',
            }
            return Response(data)
class Taxsettingsup(APIView):
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostTaxSettings.objects.using(company_db).get(pk=pk)
        except EngageboostTaxSettings.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        company_db = loginview.db_active_connection(request)
        settings = self.get_object(pk,request)
        serializer = Taxsettings(settings)
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

    def put(self, request, pk, format=None):
        company_db = loginview.db_active_connection(request)
        d1={'modified':datetime.now().date()}
        d2=request.data
        serializer_data=dict(d2,**d1)
        settings = self.get_object(pk,request)
        serializer = Taxsettings(settings, data=serializer_data,partial=True)
        if serializer.is_valid():
            serializer.save()
            data ={
            'status':1,
            'Message':'Successfully Updated',
            }
            return JsonResponse(data)
        else:
            data ={
            'status':0,
            'Message':'Data Not Found',
            }
            return Response(data)
class check(APIView):
    def get(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        return ('Hello')