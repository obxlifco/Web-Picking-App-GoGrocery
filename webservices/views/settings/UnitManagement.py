from webservices.models import EngageboostUnitMasters
from django.http import Http404
from django.db.models import Q
from webservices.serializers import UnitmasterSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime
from rest_framework import generics
from rest_framework.response import Response
from webservices.views import loginview
from webservices.views.common import common

# Unit Settings Insert 
class Unitsettings(APIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        # unit_name_count = EngageboostUnitMasters.objects.using(company_db).filter(unit_name__icontains=request.data['unit_name'],isdeleted='n').count()
        # unit_full_name = EngageboostUnitMasters.objects.using(company_db).filter(unit_full_name__icontains=request.data['unit_full_name'],isdeleted='n').count()
        unit_name_count = EngageboostUnitMasters.objects.using(company_db).filter(unit_name=request.data['unit_name'],isdeleted='n').count()
        unit_full_name = EngageboostUnitMasters.objects.using(company_db).filter(unit_full_name=request.data['unit_full_name'],isdeleted='n').count()
        if unit_name_count == 0:
            if unit_full_name == 0:
                d1={'created':datetime.now().date(),'modified':datetime.now().date()}
                d2=request.data
                serializer_data=dict(d2,**d1)
                serializer = UnitmasterSerializer(data=serializer_data,partial=True)
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
            else:
                data ={
                'status':0,
                'api_status':serializer.errors,
                'message':'Unit Full name is already exists',
                }
                return Response(data)
        else:
                data ={
                'status':0,
                'message':'Unit name is already exists',
                }
                return Response(data)
# Unit Settings Update and Get 
class Unitsettingsup(APIView):
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostUnitMasters.objects.using(company_db).get(pk=pk)
        except EngageboostUnitMasters.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        company_db = loginview.db_active_connection(request)
        settings = self.get_object(pk,request)
        serializer = UnitmasterSerializer(settings)
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
        # unit_name_count = EngageboostUnitMasters.objects.filter(unit_name__iexact=request.data['unit_name'],isdeleted='n').filter(~Q(id=pk)).count()
        # unit_full_name = EngageboostUnitMasters.objects.filter(unit_full_name__iexact=request.data['unit_full_name'],isdeleted='n').filter(~Q(id=pk)).count()
        unit_name_count = EngageboostUnitMasters.objects.filter(unit_name__iexact=request.data['unit_name'],isdeleted='n').exclude(id=pk).count()
        unit_full_name = EngageboostUnitMasters.objects.filter(unit_full_name__iexact=request.data['unit_full_name'],isdeleted='n').exclude(id=pk).count()
        if unit_name_count == 0:
            if unit_full_name == 0:
                serializer = UnitmasterSerializer(settings, data=serializer_data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    common.related_products_to_elastic('EngageboostUnitMasters',pk)
                    data ={
                    'status':1,
                    'api_status':'',
                    'Message':'Successfully Updated',
                    }
                    return Response(data)
                else:
                    data ={
                    'status':0,
                    'api_status':serializer.errors,
                    'Message':'Data Not Found',
                    }
                    return Response(data)
            else:
                data ={
                'status':0,
                'api_status':serializer.errors,
                'message':'Unit Full name is already exists',
                }
                return Response(data)
        else:
                data ={
                'status':0,
                'message':'Unit name is already exists',
                }
                return Response(data)