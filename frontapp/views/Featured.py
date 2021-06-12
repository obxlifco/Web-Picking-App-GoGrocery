from webservices.models import *
from django.http import Http404
from webservices.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime
from rest_framework import generics
from django.core import serializers
from django.http import HttpResponse
import json
from django.db.models import Q  
import requests
from django.conf import settings
from django.utils import timezone
from webservices.views import loginview
from collections import Counter
from random import randint
from django.db.models import Count
from django.views.generic import View
import urllib.parse
from django.db.models import Sum
from django.http import HttpRequest 

class Pageloadsettings(View):
# """ basic setup info  web services"""
	def get(self, request, pk,format=None):
		company_db = loginview.db_active_connection(request)
		open_store_via_order_chk=1
		distributor_user_type=''
		pk = urllib.parse.unquote(pk)
		if(pk == '1'):
			cnt=EngageboostCompanyWebsites.objects.using(company_db).filter(id=1).count()
		else:
			cnt=EngageboostCompanyWebsites.objects.using(company_db).filter(business_name__iexact=pk,isdeleted='n',isblocked='n').count()
		if cnt>0:
			if(pk=='1'):
				basicsetup=EngageboostCompanyWebsites.objects.using(company_db).get(id=1)
				distributor_website_id = basicsetup.id
				dist_site_status = 1
			else:
				basicsetup=EngageboostCompanyWebsites.objects.using(company_db).get(business_name__iexact=pk,isdeleted='n',isblocked='n')
				distributor_user_type = basicsetup.distributor_user_type
				if basicsetup.is_purchase_item_first_time=='n':
					open_store_via_order_chk=0
				distributor_website_id = basicsetup.id
				dist_site_status = 1
		else:			
			basicsetup=EngageboostCompanyWebsites.objects.using(company_db).get(id=1)
			blocked_data = EngageboostCompanyWebsites.objects.using(company_db).filter(business_name__iexact=pk).filter(Q(isdeleted='y') | Q(isblocked='y'))
			if blocked_data.count() > 0:
				blocked_data_row = blocked_data.first()
				distributor_website_id = blocked_data_row.id
				dist_site_status = 0
			else:
				distributor_website_id = 0
				dist_site_status = 0

		globalsettings= EngageboostGlobalSettings.objects.using(company_db).get(website_id=basicsetup.id)
		currency_rate=EngageboostCurrencyRates.objects.using(company_db).get(isbasecurrency='y',engageboost_company_website_id=basicsetup.id)
		currency=EngageboostCurrencyMasters.objects.using(company_db).get(id=currency_rate.engageboost_currency_master_id)
		Currency_no=EngageboostGlobalsettingCurrencies.objects.using(company_db).all().filter(global_setting_id=globalsettings.id)
		default_warehouse_type = 'default';
		default_warehouse_id = 0
		latitude = ""
		longitude = ""
		if basicsetup.id:
			rs_channel = EngageboostWarehouseMasterApplicableChannels.objects.filter(applicable_channel_id=6, isblocked='n', isdeleted='n').first()
			if rs_channel:
				defult_warehouse = EngageboostWarehouseMasters.objects.using(company_db).filter(id=rs_channel.warehouse_master_id).all()
			else:
				defult_warehouse = EngageboostWarehouseMasters.objects.using(company_db).filter(website_id=basicsetup.id, isblocked='n', isdeleted='n').all()
			if defult_warehouse.count() > 0:
				warehouse_type = defult_warehouse.first()
				# default_warehouse_type = defult_warehouse[0].warehouse_type
				# default_warehouse_id = defult_warehouse[0].id
				# default_warehouse_type = warehouse_type.warehouse_type
				default_warehouse_id = warehouse_type.id
				latitude = warehouse_type.latitude
				longitude = warehouse_type.longitude

		arr3=[]
		for Currency_num in Currency_no:
			arr3.append(Currency_num.currency_id)
		currency_master=EngageboostCurrencyMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n',id__in=arr3)	
		currency_master_arr=[]
		for currencys in currency_master:
			if currencys.id==currency_rate.engageboost_currency_master_id:
				d1={'currency_id':currencys.id,'currency_code':currencys.currency,'currency_symbol':currencys.currencysymbol,'isbasecurrency':1}
			else:
				d1={'currency_id':currencys.id,'currency_code':currencys.currency,'currency_symbol':currencys.currencysymbol,'isbasecurrency':0}
			currency_master_arr.append(d1)
		
		language=EngageboostLanguages.objects.using(company_db).get(id=1)
		company_globalsettings= EngageboostGlobalSettings.objects.using(company_db).get(website_id=1)
		x_forwarded_for = ""
		if "HTTP_X_FORWARDED_FOR" in request.META:
			x_forwarded_for = request.META['HTTP_X_FORWARDED_FOR'] 
			if x_forwarded_for: 
				ip = x_forwarded_for.split(',')[0] 
		else: 
			ip = request.META['REMOTE_ADDR']

		data={
			'status':1,
			'website_id':basicsetup.id,
			'company_id':basicsetup.engageboost_company_id,
			'country_id':basicsetup.country_id,
			'language_name':language.name,
			'language_id':language.id,
			'currency_code':currency.currency,
			'currency_symbol':currency.currencysymbol,
			'currency_id':currency.id,
			'currency_exchange':1,
			'website_logo':basicsetup.website_logo,
			'currency_master':currency_master_arr,
			'fb_store_app_id':globalsettings.fb_store_app_id,
			'fb_store_secret':globalsettings.fb_store_secret,
			'fb_login_id':globalsettings.fb_login_id,
			'fb_login_secret':globalsettings.fb_login_secret,
			# 'fb_pixel_id':globalsettings.fb_pixel_id,
			'google_login_client_id':globalsettings.google_login_client_id,
			'google_login_client_secret':globalsettings.google_login_client_secret,
			'google_login_redirect_url':globalsettings.google_login_redirect_url,
			'google_application_name':globalsettings.google_application_name,
			'google_login_devoloper_key':globalsettings.google_login_devoloper_key,
			'template':basicsetup.engageboost_template_master_id,
			'business_name': basicsetup.business_name,
			'company_name': basicsetup.company_name,
			'websitename': basicsetup.websitename,
			'ga_view_id':globalsettings.google_analytics_profileid,
			# 'min_order_amount':d3,
			'open_store_via_order_chk':open_store_via_order_chk,
			'distributor_user_type':distributor_user_type,
			# 'warehouse_type': default_warehouse_type,
			'default_warehouse_id':default_warehouse_id,
			"latitude" :latitude,
			"longitude" :longitude,
			'tax_type' : company_globalsettings.algolia_app_key,
			'distributor_website_id':distributor_website_id,
			'dist_site_status':dist_site_status,
			'requested_ip':ip
		}	
		return JsonResponse(data)

class GetSlug(generics.ListAPIView):
	permission_classes = []
	def post(self, request, format=None):
		slug = request.data.get('slug')
		type = request.data.get('type')

		data = {}
		if type == 'category':
			slug_data = EngageboostCategoryMasters.objects.filter(slug=slug).first()
			if slug_data:
				data = {
					"name": slug_data.name,
					"meta_title": slug_data.page_title,
					"meta_keywords": slug_data.meta_keywords,
					"meta_description": slug_data.meta_description
				}
		elif type == 'product':
			slug_data = EngageboostProducts.objects.filter(slug=slug).first()
			if slug_data:
				data = {
					"name": slug_data.name,
					"meta_title": slug_data.meta_title,
					"meta_keywords": slug_data.meta_key_word,
					"meta_description": slug_data.meta_description
				}
			# meta_title, meta_key_word, meta_description
			# page_title, meta_keywords, meta_description

		resp_data = {
			'status': 1,
			'data': data,
		}

		return Response(resp_data)

