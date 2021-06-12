from webservices.models import EngageboostPresets,EngageboostShippingMasters,EngageboostShippingServiceNames,EngageboostShippingPackagingtype
from django.http import Http404
from webservices.serializers import PresetsSerializer,ShippingSerializer,ShippingServiceNamesSerializer,PackagSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import generics
from itertools import chain
from django.core import serializers
from django.http import HttpResponse
from webservices.views import loginview
from django.db.models import Q
import sys,os,math
import traceback
import datetime

class PresetSetup(generics.ListAPIView):
    # """ Add New Preset """
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
        d2=request.data
        d1={}
        # d2={x:request.POST.get(x) for x in request.POST.keys()}
        serializer_data=dict(d2,**d1)
        serializer = PresetsSerializer(data=serializer_data,partial=True)
        if serializer.is_valid():
            # serializer.save()
            try:
                has_preset = EngageboostPresets.objects.filter(name=d2["name"]).first()
                if has_preset:
                    data ={"status":0,"api_status":'Preset already exists',"message":'Preset already exists'}
                else:
                    has_record = EngageboostPresets.objects.last()
                    if has_record:
                        last_entry_of_table = EngageboostPresets.objects.order_by('-id').latest('id')
                        row_id = int(last_entry_of_table.id)+int(1)
                    else:
                        row_id = 1

                    d1={"id":row_id,"created_date":now_utc,"modified_date":now_utc}
                    serializer_data=dict(serializer_data,**d1)
                    # return Response(serializer_data)
                    
                    preset_data = EngageboostPresets.objects.using(company_db).create(**serializer_data)

                    last_inserted_id = preset_data.id
                    data={"status":1,"last_inserted_id":last_inserted_id,"message":'Preset Created Successfully'}
            except Exception as error:
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error), "message": str(error)}
        else:
            data ={"status":0,"api_status":serializer.errors,"message":'Error Occured'}

        return Response(data)

class PresetListView(generics.ListAPIView):
    # """ List all Edit,Uodate Preset """
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostPresets.objects.using(company_db).get(pk=pk)
        except EngageboostPresets.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        preset = self.get_object(pk,request)
        service_id=preset.service_id
        shipping_method_id=preset.shipping_method_id
        package_id=preset.package_id
        serializer = PresetsSerializer(preset)
        settings1 = EngageboostShippingMasters.objects.using(company_db).all()
        serializer2 = ShippingSerializer(settings1,many=True)
        settings_ser = EngageboostShippingServiceNames.objects.using(company_db).all().filter(shipping_method_type=shipping_method_id)
        serializer_ser = ShippingServiceNamesSerializer(settings_ser,many=True)
        settings_pack = EngageboostShippingPackagingtype.objects.using(company_db).all().filter(shipping_method_id=shipping_method_id)
        serializer_pack = PackagSerializer(settings_pack,many=True)
        if(serializer): 
            data ={'status':1,'api_status':serializer.data,'message':'','courier_arr':serializer2.data,'services_arr':serializer_ser.data,'package_arr':serializer_pack.data}
        else:
            data ={'status':0,'api_status':serializer.errors,'message':'Data Not Found'}
        return Response(data)
    
    def put(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
        preset = self.get_object(pk,request)
        d1={"modified_date":now_utc}
        d2=request.data
        #d2={x:request.POST.get(x) for x in request.POST.keys()}
        serializer_data=dict(d2,**d1)
        serializer = PresetsSerializer(preset,data=serializer_data,partial=True)
        if serializer.is_valid():
            has_preset = EngageboostPresets.objects.filter(name=d2["name"]).first()
            if has_preset:
                if has_preset.id == int(pk):
                    serializer.save()
                    EngageboostPresets.objects.filter(id=pk).update(shipping_method_id=d2["shipping_method_id"],service_id=d2["service_id"],package_id=d2["package_id"])
                    data ={'status':1,'api_status':'','message':'Successfully Updated'}
                else:
                    data ={"status":0,"api_status":'Preset already exists',"message":'Preset already exists'}
            else:
                serializer.save()
                data ={'status':1,'api_status':'','message':'Successfully Updated'}
        else:
            data ={'status':0,'api_status':serializer.errors,'message':'Error Occured'}
        
        return Response(data)

class Presetdata(generics.ListAPIView):

    def get(self, request, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        settings1 = EngageboostShippingMasters.objects.using(company_db).all()
        serializer2 = ShippingSerializer(settings1,many=True)
        
        if(serializer2): 
            data ={
                'courier_arr':serializer2.data,
                }
            return Response(data)

class ServicesList(generics.ListAPIView):
    # """ List all Edit,Uodate Preset """
    def get_object(self, shipping_service_id):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostShippingServiceNames.objects.using(company_db).get(shipping_service_id=shipping_service_id)
        except EngageboostShippingServiceNames.DoesNotExist:
            raise Http404
    def get(self, request, shipping_service_id, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        settings_ser = EngageboostShippingServiceNames.objects.using(company_db).all().filter(shipping_method_type=shipping_service_id)
        serializer_ser = ShippingServiceNamesSerializer(settings_ser,many=True)
        settings_ser2 = EngageboostShippingPackagingtype.objects.using(company_db).all().filter(shipping_method_id=shipping_service_id)
        serializer_ser2 = PackagSerializer(settings_ser2,many=True)
        if(serializer_ser): 
            data ={
                'services_arr':serializer_ser.data,
                'packages_arr':serializer_ser2.data,
            }
        else:
            data ={
                'status':0,
                'api_status':serializer.errors,
                'message':'Data Not Found',
                }
        return Response(data)

class PackegeList(generics.ListAPIView):
    # """ List all Edit,Uodate Preset """
    def get_object(self):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostShippingPackagingtype.objects.using(company_db).get()
        except EngageboostShippingPackagingtype.DoesNotExist:
            raise Http404
    def get(self, request, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        settings_ser = EngageboostShippingPackagingtype.objects.using(company_db).all()
        serializer_ser = PackagSerializer(settings_ser,many=True)
        if(serializer_ser): 
            data ={
                'services_arr':serializer_ser.data,
            }
        else:
            data ={
                'status':0,
                'api_status':serializer.errors,
                'message':'Data Not Found',
                }
        return Response(data)