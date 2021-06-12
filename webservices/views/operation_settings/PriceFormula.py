from webservices.models import *
from django.http import Http404
from webservices.serializers import  PriceFormulaSerializer
from django.core.paginator import Paginator
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
from django.db.models import Q
from webservices.views import loginview
import datetime





class PriceFormulaManager(generics.ListAPIView):


	def post(self, request):

		company_db = loginview.db_active_connection(request)
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		postdata=request.data


		#===================== validation part ================================

		price_name = ('cost', 'selling')
		condition_type = ('+', '-')
		formula_type = ('customer', 'vendor')
		field_names = ('formula_name', 'price_name', 'condition_type', 'margin', 'formula_type')

		for field in field_names:
			if not field in postdata.keys():
				return Response({'status':0, 'field':field, 'Message':'Invalid Request Sent'})

		if not postdata['price_name'] in price_name:
			return Response({'status':0, 'field':'price_name', 'Message':'Invalid Request Sent'})

		if not postdata['condition_type'] in condition_type:
			return Response({'status':0, 'field':'condition_type', 'Message':'Invalid Request Sent'})

		if not postdata['formula_type'] in formula_type:
			return Response({'status':0, 'field':'formula_type', 'Message':'Invalid Request Sent'})

		website_id = postdata['website_id'] if postdata.get("website_id") else None


		#===================== validation part ================================

		record_id = postdata['id']if postdata.get("id") else None

		if record_id:

			if not EngageboostPriceFormula.objects.using(company_db).filter(id=record_id).exists():
				return Response({'status':0, 'Message':'Please send a valid record id'})
			
			get_record = EngageboostPriceFormula.objects.get(id=record_id)

			get_record.formulla_name = postdata['formula_name']
			get_record.price_name = postdata['price_name']
			get_record.condition = postdata['condition_type']
			get_record.margin = postdata['margin']
			get_record.formulla_type = postdata['formula_type']

			get_record.save()

			data = {'status':1, 'Message':'Record Updated Successfully'}

		else:
			EngageboostPriceFormula.objects.create(website_id=website_id,
													formulla_name=postdata['formula_name'],
													price_name=postdata['price_name'],
													condition=postdata['condition_type'],
													margin=postdata['margin'],
													formulla_type=postdata['formula_type'],
													created=now_utc,
													modified=now_utc,
													isblocked='n',
													isdeleted='n')

			data = {'status':1, 'Message':'Record Saved Successfully'}

		return Response(data)


class PriceFormulaManagerDetails(generics.ListAPIView):
	 #///////////////////Fetch Single Row
	def get(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		managers=EngageboostPriceFormula.objects.using(company_db).all().filter(id=pk)
		
		if managers:
			managers_data = PriceFormulaSerializer(managers, many=True)
			data = {
				"status":1,
				"data":managers_data.data
			}
		else:
			data = {
				"status":0,
				"data":[]
			}
		return Response(data)




