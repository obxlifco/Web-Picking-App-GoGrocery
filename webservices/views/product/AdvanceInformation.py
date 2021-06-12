from webservices.models import *
from django.http import Http404
from webservices.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
import datetime
from rest_framework import generics
from itertools import chain
from django.core import serializers
from django.http import HttpResponse
import json
from django.db.models import Q  
import requests
from django.conf import settings
import random
from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import MultiPartParser, FormParser
from webservices.views import loginview
import sys
import traceback
from webservices.views.common import common
class AdvanceInformationViewSet(generics.ListAPIView):
# """ List all users, or create a new user """
	def post(self, request, format=None):
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		company_db = loginview.db_active_connection(request)
		for data in request.data:
			cnt_product_id=EngageboostMarketplaceFieldValue.objects.using(company_db).filter(product_id=data['product_id']).count()
			if cnt_product_id >0:
				EngageboostMarketplaceFieldValue.objects.using(company_db).filter(product_id=data['product_id']).delete()
		if len(request.data)>0:
			elastic_product_id = ""
			prod_custom_lang = []
			for data in request.data:
				if 'product_id' in data.keys() and data['product_id']!=None and data['product_id']!="":
					elastic_product_id = data['product_id']
				
				if data['value'] !='':
					has_record = EngageboostMarketplaceFieldValue.objects.last()
					if has_record:
						last_entry_of_table = EngageboostMarketplaceFieldValue.objects.order_by('-id').latest('id')
						row_id = int(last_entry_of_table.id)+int(1)
					else:
						row_id = 1
					d1={'id':row_id,'created':now_utc,'modified':now_utc}
					d2=data
					serializer_data=dict(d2,**d1)
					insert_lang_obj = {}
					
					insert_lang_obj.update({"product_id":serializer_data['product_id'], "channel_id":serializer_data['channel_id'], "field_id":serializer_data['field_id'], "lang_data":serializer_data['lang_data']})
					serializer_data.pop('lang_data')

					serializer = MarketplaceFieldValueSerializer(data=serializer_data,partial=True)
					if serializer.is_valid():
						try:
							saved_Data = EngageboostMarketplaceFieldValue.objects.using(company_db).create(**serializer_data)
							# serializer.save()
							last_inserted_id = saved_Data.id
							save_product_customfield_lang(d2)

							data ={'status':1,'last_inserted_id':last_inserted_id,'message':'Successfully Inserted'}
						except Exception as error:
							trace_back = sys.exc_info()[2]
							line = trace_back.tb_lineno
							data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'message':str(error)}
					else:
						data ={
						'status':1,
						'message':'Data Not Inserted',
						'api_status':serializer.errors
						}
				else:
					data ={
						'status':1,
						'message':'Successfully Inserted',
						}
			if elastic_product_id !="":
				elastic = common.save_data_to_elastic(int(elastic_product_id),'EngageboostProducts')			
		else:
			data ={
					'status':1,
					'message':'Successfully Inserted',
					}		   
		return Response(data)

class AdvanceInformationLoadViewSet(generics.ListAPIView):
# """ List all users, or create a new user """
	
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostProducts.objects.using(company_db).get(id=pk)
		except EngageboostProducts.DoesNotExist:
			raise Http404

	def get(self, request, pk,channel_id, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		try:
			obj 	= EngageboostProductCategories.objects.using(company_db).filter(product_id=pk,is_parent='y')
			if obj.count()>0:
				product_category 	= EngageboostProductCategories.objects.using(company_db).get(product_id=pk,is_parent='y')
				custom_filter 		= EngageboostDefaultModuleLayoutFields.objects.using(company_db).all().filter(category_id=product_category.category_id,is_system='y').filter( Q(show_market_places__startswith=channel_id+',') | Q(show_market_places__endswith=','+channel_id) | Q(show_market_places__contains=',{0},'.format(channel_id)) | Q(show_market_places__exact=channel_id) ).order_by('section_row','section_col')
				custom 				= EngageboostDefaultModuleLayoutFields.objects.using(company_db).all().filter(category_id=product_category.category_id)
				channel 			= []
				for customs_category_in in custom:
					name=customs_category_in.show_market_places
					channel.append(name)
				str_to_array_channel = ','.join(channel)
				sta_value=str_to_array_channel.split(',')
					
				# serializer_custom 	= DefaultModuleLayoutFieldsSerializer(custom_filter,many=True)
				serializer_custom = DefaultModuleLayoutFieldsProductSerializer(custom_filter,many=True)
				product_custom 		= EngageboostMarketplaceFieldValue.objects.using(company_db).all().filter(product_id=pk)
				# print(product_custom.query)
				serializer_productcustom = MarketplaceFieldValueSerializer(product_custom,many=True)
				# print(json.dumps(serializer_productcustom.data))
				for productcustom in serializer_productcustom.data:
					productcustom["field_label_l"]=productcustom['field_label'].lower()
					# print(json.dumps(productcustom))
					if productcustom['lang_data'] and len(productcustom['lang_data'])>0:
						for productcustom_lang in productcustom['lang_data']:
							productcustom[productcustom_lang['field_name']]=productcustom_lang['field_value']
				# productcustom.pop('lang_data')

				if(str_to_array_channel):
					settings4 = EngageboostChannels.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').filter(id__in=sta_value)
					serializer4 = ChannelsSerializer(settings4, many=True)
					channel=serializer4.data
				else:
					channel=[]
				if(serializer_custom): 
					data ={
						'status':1,
						'custom_data':serializer_custom.data,
						'api_status':serializer_productcustom.data,
						'channel':channel
						}
				else:
					data ={
						'status':0,
						'api_status':serializer.errors,
						'message':'Data Not Found',
						}
			else:
				data ={
					'status':0,
					'api_status':"",
					'message':'Data Not Found',
					}			
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error), 'message':'Data Not Found',}
			return Response(data)

	def put(self, request,pk, format=None):
		company_db = loginview.db_active_connection(request)
		if len(request.data)>0:
			for data in request.data:				
				EngageboostDefaultModuleLayoutFields.objects.using(company_db).filter(field_id=int(data['field_id'])).update(default_values=data['default_value'])
				all_language_data = common.get_all_languages()
                # multi_lang_data = []
                # for lang_code in all_language_data:
                #     langcode = lang_code['lang_code']
                #     lang_id = lang_code['id']
                #     listcount = len(data)
                #     check_str = "_"+langcode
                #     for key, value in data.items():
                #         lang_data = {}
                #         if check_str in key:
                #             lang_data = {
                #                 "language_id":lang_id,
                #                 "language_code":langcode,
                #                 "brand_id":last_id,
                #                 "field_name":key,
                #                 "field_value":value,
                #                 'created':datetime.now().date(),
                #                 'modified':datetime.now().date()
                #             }
                #             multi_lang_data.append(lang_data)

			data ={
					'status':1,
					'message':'Successfully Updated',
					}

		else:
			data ={
				'status':1,
				'message':'Data Not Found',
				'api_status':''
				} 
		return Response(data)


def save_product_customfield_lang(requestdata):
	# {'product_id': 234, 'channel_id': 6, 'field_id': 5, 'value': 'Red', 'website_id': 1, 'field_name': 'Color', 'field_label': 'Color', 'lang_data': [{'lang_field_value': 'red h', 'lang_field_name': 'color_hi'}, {'lang_field_value': 'red th', 'lang_field_name': 'color_th'}]}

	if requestdata:
		print(requestdata)
		for langdata in requestdata['lang_data']:
			add_edit_arr = {
				"language_id":2,
				"language_code":"th",
				"field_id":requestdata['field_id'], 
				"product_id":requestdata['product_id'], 
				"field_name": langdata['lang_field_name'],
				# "field_value": langdata['lang_field_value'], 
				"isblocked":'n', 
				"isdeleted":'n'
			}
			if "lang_field_value" in langdata:
				add_edit_arr.update({"field_value":langdata['lang_field_value']})
				
			rs_check_exist = EngageboostProductCustomFieldMastersLang.objects.filter(field_id=requestdata['field_id'], product_id=requestdata['product_id'], field_name = langdata['lang_field_name'], isblocked='n', isdeleted='n').first()
			if rs_check_exist:
				EngageboostProductCustomFieldMastersLang.objects.filter(field_id=requestdata['field_id'], product_id=requestdata['product_id'], field_name = langdata['lang_field_name'], isblocked='n', isdeleted='n').update(**add_edit_arr)
			else:
				# print(add_edit_arr)
				lastObj = EngageboostProductCustomFieldMastersLang.objects.create(**add_edit_arr)
				# print("=============",lastObj)
	else:
		data = {}