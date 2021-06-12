from webservices.models import EngageboostCurrencyRates
from django.http import Http404
from django.db.models import Q
from webservices.serializers import BaseCurrencyratesetSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime
from rest_framework import generics
from rest_framework.response import Response
import requests
from urllib.request import urlopen
from django.http import HttpResponse
import json
from bs4 import BeautifulSoup
from webservices.views import loginview

class currencysettingsup(APIView):
	def get_object(self):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostCurrencyRates.objects.using(company_db).get()
		except EngageboostCurrencyRates.DoesNotExist:
			raise Http404
# all BaseCurrency for website id
	def get(self, request,format=None):
		company_db = loginview.db_active_connection(request)
		settings = EngageboostCurrencyRates.objects.using(company_db).all().filter(engageboost_company_website_id=1)
		serializer = BaseCurrencyratesetSerializer(settings,many=True)
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
# Insert of BaseCurrency
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		d1={'created':datetime.now().date(),'modified':datetime.now().date()}
		d2=request.data
		results=d2['data']
		
		for data in results:
			cnt=EngageboostCurrencyRates.objects.using(company_db).filter(engageboost_currency_master_id=data['engageboost_currency_master_id']).count()
			if cnt==0:
				
				User = EngageboostCurrencyRates.objects.using(company_db).create(created=datetime.now(),modified=datetime.now(),country_id=data['country_id'],engageboost_company_website_id=data['engageboost_company_website_id'],engageboost_currency_master_id=data['engageboost_currency_master_id'],currency_code=data['currency_code'],exchange_rate=data['exchange_rate'],isbasecurrency=data['isbasecurrency'],updatedby=data['updatedby'],createdby=data['createdby'])
			else:
				
				EngageboostCurrencyRates.objects.using(company_db).filter(engageboost_currency_master_id=data['engageboost_currency_master_id']).update(created=datetime.now(),modified=datetime.now(),country_id=data['country_id'],engageboost_company_website_id=data['engageboost_company_website_id'],currency_code=data['currency_code'],exchange_rate=data['exchange_rate'],isbasecurrency=data['isbasecurrency'],updatedby=data['updatedby'],createdby=data['createdby'])
		data ={
		'status':1,
		'api_status':'',
		'Message':'Successfully Updated',
		}
		return Response(data)
# BaseCurrencyset for website ids 
class BaseCurrencyset(APIView):
	def put(self, request,pk, format=None):
		company_db = loginview.db_active_connection(request)
		arr_currency=[]
		EngageboostCurrencyRates.objects.using(company_db).update(isbasecurrency='n')
		EngageboostCurrencyRates.objects.using(company_db).filter(engageboost_currency_master_id=pk).update(isbasecurrency='y',exchange_rate='1')
		settings = EngageboostCurrencyRates.objects.using(company_db).all()
		for setting in settings:
			d3={"engageboost_currency_master_id":setting.engageboost_currency_master_id,"currency_code":setting.currency_code,"exchange_rate":setting.exchange_rate,"isbasecurrency":setting.isbasecurrency}
			arr_currency.append(d3)
		data ={
			'status':1,
			'curreny':arr_currency,
			'message':'Successfully Updated'
		}
		return Response(data)

class BaseCurrencyChange(APIView):
	def put(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		d2=request.data
		results=d2['data']
		
		for data in results:
			User = EngageboostCurrencyRates.objects.using(company_db).filter(currency_code=data['currency_code']).update(exchange_rate=data['exchange_rate'],updatedby=data['updatedby'])
		data ={
			'status':1,
			
			'message':'Successfully Updated',
		}
		return Response(data)

class CurrencyExchangerate(APIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		Isbasecurrency=EngageboostCurrencyRates.objects.using(company_db).get(isbasecurrency='y')
		othercurrency=EngageboostCurrencyRates.objects.using(company_db).all().filter(isbasecurrency='n')
		settings = EngageboostCurrencyRates.objects.using(company_db).all().filter(engageboost_company_website_id=1)
		serializer = BaseCurrencyratesetSerializer(settings,many=True)
		for othercurrencys in othercurrency:
			yql_base_url = "https://finance.google.com/finance/converter?a=1&from="+Isbasecurrency.currency_code+"&to="+othercurrencys.currency_code
			
			yql_response = urlopen(yql_base_url)
			# print (yql_response)
			# row=str(yql_response)
			# print(yql_response)	
			soup = BeautifulSoup(yql_response)
			string1=soup.find('span', class_='bld')
			numbers=get_num(str(string1))
			EngageboostCurrencyRates.objects.using(company_db).filter(currency_code=othercurrencys.currency_code).update(exchange_rate=numbers,updatedby=request.data['updatedby'])
			data ={
			'status':1,
			'AllCurrencyRates':serializer.data,
			'message':'Successfully Updated',
			}
		return Response(data)
		


def get_num(x):
    return float(''.join(ele for ele in x if ele.isdigit() or ele == '.'))

	
	
	