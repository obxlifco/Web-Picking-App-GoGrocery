from django.http import Http404
from django.db.models import Q
from webservices.models import *
from webservices.serializers import *
from rest_framework.views import APIView
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime
from rest_framework import generics
from rest_framework.response import Response
from webservices.views import loginview
import sys,math
import traceback


class LanguageData(generics.ListAPIView):
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostUnitMasters.objects.using(company_db).get(pk=pk)
        except EngageboostUnitMasters.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        try:
            rs_language = EngageboostLanguages.objects.filter(id=pk).first()
            serializer = LanguageSerializer(rs_language)
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
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}
        
        return Response(data)

    def post(self, request, format=None):
        d1={'modified':datetime.now().date()}
        d2=request.data
        serializer_data=dict(d2,**d1)
        rs_language = EngageboostLanguages.objects.filter(lang_code=d2['lang_code']).first()
       
        if rs_language:
            data ={
            'status':0,
            'api_status':"",
            'message':'Already exist.',
            }
            return Response(data)
        else:
            serializer = LanguageSerializer(rs_language, data=serializer_data,partial=True)
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

    def put(self, request, pk, format=None):
        d1={'modified':datetime.now().date()}
        d2=request.data
        serializer_data=dict(d2,**d1)

        rs_language = EngageboostLanguages.objects.filter(id=pk).first()
        if rs_language:
            serializer = LanguageSerializer(rs_language, data=serializer_data,partial=True)
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
            'api_status':"",
            'message':'No data Found',
            }
            return Response(data)