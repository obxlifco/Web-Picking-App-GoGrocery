
from django.shortcuts import render

from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.http import JsonResponse

# Import Model And Serializer
from webservices.models import *
from webservices.serializers import *
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
import sys,os
import traceback


@csrf_exempt
def BrandListByBrandId(request):
	if request.method == 'POST':
		website_id = request.POST.get('website_id')
		brand_ids = request.POST.getlist('brand_ids[]')
    
		try:
			if website_id is None:
				raise Exception("Website id is required")
			if len(brand_ids)==0: 
				raise Exception("brand ids is required")

			serializer_data=EngageboostBrandMasters.objects.filter(isdeleted='n',isblocked='n',website_id=website_id,id__in=brand_ids).all()
			brands_data = BrandSerializer(serializer_data,many=True).data
			if brands_data:
				data ={
				    'status':1,
				    'brands':brands_data
				}
			else:
				data={
					"status":0,
					"msg":"No data found.",
					"data":[]
				}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
	return JsonResponse(data)    


