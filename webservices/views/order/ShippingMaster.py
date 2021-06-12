from webservices.models import EngageboostShippingMasters,EngageboostAwbMasters,EngageboostShippingZipcodes
from django.http import Http404
from webservices.serializers import ShippingSerializer,AwbMastersSerializer
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

class ShippingMaster(generics.ListAPIView):
# """ Add New ShippingMaster """
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        d1={'created':datetime.now().date(),'modified':datetime.now().date()}
        d2=request.data
        serializer_data=dict(d2,**d1)
        serializer = ShippingSerializer(data=serializer_data,partial=True)
        if serializer.is_valid():
            serializer.save()
            tracking_type=request.data['tracking_type']
            if tracking_type == 'Awb':
                awb=request.data['awb']
                zipcode=request.data['zipcode']
                if zipcode!='':
                    method_name=request.data['method_name']
                    obj = EngageboostShippingMasters.objects.using(company_db).latest('id')
                    last_id = obj.id
                    Zipcode=zipcode.split(",")
                    for Zip in Zipcode: 
                        User = EngageboostShippingZipcodes.objects.using(company_db).create(zipcode=Zip,shipping_method_id=last_id)   
                AWB=awb.split(",")
                if awb != "":
                    for AWB_data in AWB:
                        
                        User = EngageboostAwbMasters.objects.using(company_db).create(awb_number=AWB_data,tracking_company_name=method_name,shipping_method_id=last_id,created=datetime.now(),isdeleted='n')
                        data ={
                        'status':1,
                        'api_status':'',
                        'message':'Successfully Inserted',
                        }
                    return Response(data)
                else:

                        
                        data ={
                        'status':1,
                        'api_status':'',
                        'message':'Successfully Inserted',
                        }
                        return Response(data)


            elif tracking_type == 'Range':
                method_name=request.data['method_name']
                obj = EngageboostShippingMasters.objects.using(company_db).latest('id')
                last_id = obj.id
                zipcode=request.data['zipcode']
                if zipcode!='':
                    Zipcode=zipcode.split(",")
                    for Zip in Zipcode: 
                        User = EngageboostShippingZipcodes.objects.using(company_db).create(zipcode=Zip,shipping_method_id=last_id)   
                range_start=int(request.data['tracking_id_start'])
                range_end=int(request.data['tracking_id_end'])
                prifix = request.data['awb_prefix']
                sufix = request.data['awb_suffix']
                if range_start >0 and range_end >0:
                    if range_end > range_start or range_end == range_start:
                        for b in range(range_start,range_end):
                            abw = prifix + str(b) + sufix
                            User = EngageboostAwbMasters.objects.using(company_db).create(awb_number=abw,tracking_company_name=method_name,shipping_method_id=last_id,created=datetime.now(),isdeleted='n')
                            data ={
                            'status':1,
                            'api_status':'',
                            'message':'Successfully Inserted',
                            }
                        return Response(data)
                    else:
                        data ={
                            'status':0,
                            'api_status':'',
                            'message':'Tracking Start value should be less then Tracking End value',
                            }
                        return Response(data)
                else:
                    
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
                       
class ShippingMasterList(generics.ListAPIView):
# """ List all Edit,Uodate ShippingMaster """
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostShippingMasters.objects.using(company_db).get(pk=pk)
        except EngageboostShippingMasters.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        user = self.get_object(pk,request)
        serializer = ShippingSerializer(user)
        awb_no=EngageboostAwbMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n',shipping_method_id=pk)
        awb_total=EngageboostAwbMasters.objects.using(company_db).filter(isdeleted='n',isblocked='n',shipping_method_id=pk).count()
        awb_unused=EngageboostAwbMasters.objects.using(company_db).filter(isdeleted='n',isblocked='n',shipping_method_id=pk,isused='n').count()
        awb_used=EngageboostAwbMasters.objects.using(company_db).filter(isdeleted='n',isblocked='n',shipping_method_id=pk,isused='y').count()
        
        arr=[]
        for awb_num in awb_no:
            arr.append(awb_num.awb_number)
        arr2=','.join([str(i) for i in arr])
     
        
        arr1=[]
        zipcode=EngageboostShippingZipcodes.objects.using(company_db).all().filter(shipping_method_id=pk)    
        for zipcode_num in zipcode:
            arr1.append(zipcode_num.zipcode)
        arr3=','.join([str(i) for i in arr1])    
        
        d1={'total':awb_total,'awb_used':awb_used,'awb_unused':awb_unused}
        d2=serializer.data
        serializer_data=dict(d2,**d1)
        if(serializer): 
            data ={
                'status':1,
                'api_status':serializer_data,
                'awb_number':arr2,
                'zipcode':arr3
                
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
        Shipping = self.get_object(pk,request)
        d1={'modified':datetime.now().date()}
        d2=request.data
        serializer_data=dict(d2,**d1)
        serializer = ShippingSerializer(Shipping,data=serializer_data,partial=True)
        if serializer.is_valid():
            serializer.save()
            EngageboostAwbMasters.objects.using(company_db).filter(shipping_method_id=pk).delete()
            tracking_type=request.data['tracking_type']
            if tracking_type == 'Awb':
                awb=request.data['awb']
                method_name=request.data['method_name']
                zipcode=request.data['zipcode']
                # zipcode=",".join([str(zipcode) for zipcode in zipcode])
                EngageboostShippingZipcodes.objects.using(company_db).filter(shipping_method_id=pk).delete()
                obj = EngageboostShippingMasters.objects.using(company_db).latest('id')
                last_id = pk
                if zipcode!='':
                    Zipcode=zipcode.split(",")
                    for Zip in Zipcode: 
                        User = EngageboostShippingZipcodes.objects.using(company_db).create(zipcode=Zip,shipping_method_id=last_id)   
                AWB=awb.split(",")
                if awb != "":
                    for AWB_data in AWB:
                        
                        User = EngageboostAwbMasters.objects.using(company_db).create(awb_number=AWB_data,tracking_company_name=method_name,shipping_method_id=last_id,created=datetime.now(),isdeleted='n')
                        data ={
                        'status':1,
                        'api_status':'',
                        'message':'Successfully Updated',
                        }
                    return Response(data)
                else:

                        
                        data ={
                        'status':1,
                        'api_status':'',
                        'message':'Successfully Updated',
                        }
                        return Response(data)


            elif tracking_type == 'Range':
                method_name=request.data['method_name']
                obj = EngageboostShippingMasters.objects.using(company_db).latest('id')
                last_id = pk
                EngageboostShippingZipcodes.objects.using(company_db).filter(shipping_method_id=pk).delete()
                zipcode=request.data['zipcode']
                if zipcode!='':
                    Zipcode=zipcode.split(",")
                    for Zip in Zipcode: 
                        User = EngageboostShippingZipcodes.objects.using(company_db).create(zipcode=Zip,shipping_method_id=last_id)   
                range_start=int(request.data['tracking_id_start'])
                range_end=int(request.data['tracking_id_end'])
                prifix = request.data['awb_prefix']
                sufix = request.data['awb_suffix']
                if range_start >0 and range_end >0:
                    if range_end > range_start or range_end == range_start:
                        for b in range(range_start,range_end):
                            abw = prifix + str(b) + sufix
                            User = EngageboostAwbMasters.objects.using(company_db).create(awb_number=abw,tracking_company_name=method_name,shipping_method_id=last_id,created=datetime.now(),isdeleted='n')
                            data ={
                            'status':1,
                            'api_status':'',
                            'message':'Successfully Updated',
                            }
                        return Response(data)
                    else:
                        data ={
                            'status':0,
                            'api_status':'',
                            'message':'Tracking Start value should be less then Tracking End value',
                            }
                        return Response(data)
                else:
                    
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
