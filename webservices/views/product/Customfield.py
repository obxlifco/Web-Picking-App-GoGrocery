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
from itertools import chain
from django.core import serializers
from django.http import HttpResponse
import json
import requests
import random
from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import MultiPartParser, FormParser
import os
import socket
from django.conf import settings
from django.db.models import Q
import urllib.request
import csv
import codecs
from rest_framework import pagination
from rest_framework.response import Response
import math
from webservices.serializers import GlobalsettingsSerializer
from webservices.views import loginview
from webservices.views.common import common

# Custon field for category insert here
class customfields(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		d2 = request.data
		d3 = request.data['name']
		d4 = request.data['input_type']
		name 	= d3.lower()
		name1 	= name.replace(" ","-")
		name1 	= name1.replace('"','')
		name1 	= name1.replace("'",'')
		marketplacename_arr = []
		field_name 			= name.replace("'","")
		field_name 			= name.replace('"',"")
		field_name 			= name1.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./\'\"<>?\|`~=+"})
		custom_values 		= request.data['custom_values'].strip()
		cnt = EngageboostDefaultsFields.objects.using(company_db).filter(field_name=field_name,input_type=d4).count()
		if cnt == 0:
			d1={'name':d3,'field_name':field_name,'err_msg':'Please enter '+d3,'value':d3,'created':datetime.now().date(),'modified':datetime.now().date(),'input_type':d4,'data_type':'CharField','data_length':'255','custom_values':custom_values}
			serializer_data=dict(d2,**d1)
			serializer = DefaultsFieldsSerializer(data=serializer_data,partial=True)
			if serializer.is_valid():
				serializer.save()
				obj = EngageboostDefaultsFields.objects.using(company_db).latest('id')
				last_id = obj.id
				
				values=EngageboostDefaultModuleLayoutFields.objects.using(company_db).filter(category_id=request.data['category_id']).count()
				if values == 0:
					cal_val=1
					row_val=1
					if ',' in str(request.data['channel_id']):

						marketplace_ids=request.data['channel_id'].split(',')
						for marketplace_id in marketplace_ids:
							marketplacename=EngageboostChannels.objects.using(company_db).get(id=marketplace_id)

							EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=last_id,field_label=d3,channel_id=marketplace_id)
						marketplacename_arr.append(marketplacename.name)
						# print(marketplacename_arr)	
						marketplace_name=','.join(marketplacename_arr)
						# print(marketplace_name)
							
					else:
						marketplacename=EngageboostChannels.objects.using(company_db).get(id=request.data['channel_id'])
						marketplace_name=marketplacename.name
						EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=last_id,field_label=d3,channel_id=request.data['channel_id'])
					User = EngageboostDefaultModuleLayoutFields.objects.using(company_db).create(field_id=last_id,field_label=d3,input_type=d4,default_values=request.data['default_values'].strip(),is_optional=request.data['is_optional'],data_type='CharField',err_msg='Please enter '+d3,category_id=request.data['category_id'],section_col=cal_val,section_row=row_val,custom_values=custom_values,show_market_places_name=marketplace_name,show_market_places=request.data['channel_id'])

					all_language_data = common.get_all_languages()
					multi_lang_data = []
					for lang_code in all_language_data:
						langcode = lang_code['lang_code']
						lang_id = lang_code['id']
						listcount = len(d2)
						check_str = "_"+langcode
						for key, value in d2.items():
							lang_data = {}
							if check_str in key:
								lang_data = {
									"language_id":lang_id,
									"language_code":langcode,
									"category_id":request.data['category_id'],
									"field_id":last_id,
									"field_name":key,
									"field_lable_value":value,
									'created':datetime.now().date(),
									'modified':datetime.now().date()
								}
								multi_lang_data.append(lang_data)
					save_customfield_lang(multi_lang_data)

					data ={
					'status':1,
					'api_status':serializer.errors,
					'message':'Successfully Inserted',
					}
					return Response(data)
				else:
					
					row_col = EngageboostDefaultModuleLayoutFields.objects.using(company_db).all().filter(category_id=request.data['category_id']).order_by('id')
					for col in row_col:
						cal=col.section_col
						row=col.section_row
					
					if cal == 1:
						cal_val=2
						row_val=row
						if ',' in str(request.data['channel_id']):

							marketplace_ids=request.data['channel_id'].split(',')
							for marketplace_id in marketplace_ids:
								marketplacename=EngageboostChannels.objects.using(company_db).get(id=marketplace_id)
								EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=last_id,field_label=d3,channel_id=marketplace_id)
							marketplacename_arr.append(marketplacename.name)	
							marketplace_name=','.join(marketplacename_arr)
						else:
							marketplacename=EngageboostChannels.objects.using(company_db).get(id=request.data['channel_id'])
							marketplace_name=marketplacename.name
							EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=last_id,field_label=d3,channel_id=request.data['channel_id'])
						User = EngageboostDefaultModuleLayoutFields.objects.using(company_db).create(field_id=last_id,field_label=d3,input_type=d4,default_values=request.data['default_values'].strip(),is_optional=request.data['is_optional'],data_type='CharField',err_msg='Please enter '+d3,category_id=request.data['category_id'],section_col=cal_val,section_row=row_val,custom_values=custom_values,show_market_places_name=marketplace_name,show_market_places=request.data['channel_id'])

						all_language_data = common.get_all_languages()
						multi_lang_data = []
						for lang_code in all_language_data:
							langcode = lang_code['lang_code']
							lang_id = lang_code['id']
							listcount = len(d2)
							check_str = "_"+langcode
							for key, value in d2.items():
								lang_data = {}
								if check_str in key:
									lang_data = {
										"language_id":lang_id,
										"language_code":langcode,
										"category_id":request.data['category_id'],
										"field_id":last_id,
										"field_name":key,
										"field_lable_value":value,
										'created':datetime.now().date(),
										'modified':datetime.now().date()
									}
									multi_lang_data.append(lang_data)
						save_customfield_lang(multi_lang_data)

					else:
						cal_val=1
						row_val=row+1
						if ',' in str(request.data['channel_id']):

							marketplace_ids=request.data['channel_id'].split(',')
							for marketplace_id in marketplace_ids:
								marketplacename=EngageboostChannels.objects.using(company_db).all().filter(id=marketplace_id)
								EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=last_id,field_label=d3,channel_id=marketplace_id)
							marketplacename_arr.append(marketplacename.name)	
							marketplace_name=','.join(marketplacename_arr)
						else:
							marketplacename=EngageboostChannels.objects.using(company_db).get(id=request.data['channel_id'])
							marketplace_name=marketplacename.name
							EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=last_id,field_label=d3,channel_id=request.data['channel_id'])
						User = EngageboostDefaultModuleLayoutFields.objects.using(company_db).create(field_id=last_id,field_label=d3,input_type=d4,default_values=request.data['default_values'].strip(),is_optional=request.data['is_optional'],data_type='CharField',err_msg='Please enter '+d3,category_id=request.data['category_id'],section_col=cal_val,section_row=row_val,custom_values=custom_values,show_market_places_name=marketplace_name,show_market_places=request.data['channel_id'])

						all_language_data = common.get_all_languages()
						multi_lang_data = []
						for lang_code in all_language_data:
							langcode = lang_code['lang_code']
							lang_id = lang_code['id']
							listcount = len(d2)
							check_str = "_"+langcode
							for key, value in d2.items():
								lang_data = {}
								if check_str in key:
									lang_data = {
										"language_id":lang_id,
										"language_code":langcode,
										"category_id":request.data['category_id'],
										"field_id":last_id,
										"field_name":key,
										"field_lable_value":value,
										'created':datetime.now().date(),
										'modified':datetime.now().date()
									}
									multi_lang_data.append(lang_data)
						save_customfield_lang(multi_lang_data)

					data ={
					'status':1,
					'api_status':serializer.errors,
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
		else:
			obj = EngageboostDefaultsFields.objects.using(company_db).latest('id')
			last_id = obj.id
			EngageboostMarketplaceFieldLabels.objects.using(company_db).filter(field_id=last_id).delete()
			field_check=EngageboostDefaultModuleLayoutFields.objects.using(company_db).filter(category_id=request.data['category_id'],field_label=d3,input_type=d4).count()
			if 	field_check==0:
				values=EngageboostDefaultModuleLayoutFields.objects.using(company_db).filter(category_id=request.data['category_id']).count()
				fielsid=EngageboostDefaultsFields.objects.using(company_db).filter(field_name=field_name,input_type=d4).first()
				if values == 0:
					cal_val=1
					row_val=1
					if ',' in str(request.data['channel_id']):

							marketplace_ids=request.data['channel_id'].split(',')
							for marketplace_id in marketplace_ids:
								marketplacename=EngageboostChannels.objects.using(company_db).get(id=marketplace_id)
								EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=last_id,field_label=d3,channel_id=marketplace_id)
							
							marketplacename_arr.append(marketplacename.name)
							print(marketplacename_arr)	
							marketplace_name=','.join(marketplacename_arr)
							print(marketplace_name)
					else:
						marketplacename=EngageboostChannels.objects.using(company_db).get(id=request.data['channel_id'])
						marketplace_name=marketplacename.name
						EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=last_id,field_label=d3,channel_id=request.data['channel_id'])
					User = EngageboostDefaultModuleLayoutFields.objects.using(company_db).create(show_type=0,field_id=fielsid.id,field_label=d3,input_type=d4,default_values=request.data['default_values'].strip(),is_optional=request.data['is_optional'],data_type='CharField',err_msg='Please enter '+d3,category_id=request.data['category_id'],section_col=cal_val,section_row=row_val,custom_values=custom_values,show_market_places_name=marketplace_name,show_market_places=request.data['channel_id'])
					data ={
					'status':1,
					'message':'Successfully Inserted',
					}
					return Response(data)
				else:
					obj = EngageboostDefaultsFields.objects.using(company_db).latest('id')
					last_id = obj.id
					row_col = EngageboostDefaultModuleLayoutFields.objects.using(company_db).all().filter(category_id=request.data['category_id']).order_by('id')
					for col in row_col:
						cal=col.section_col
						row=col.section_row
					
					if cal == 1:
						cal_val=2
						row_val=row
						if ',' in str(request.data['channel_id']):

							marketplace_ids=request.data['channel_id'].split(',')
							for marketplace_id in marketplace_ids:
								marketplacename=EngageboostChannels.objects.using(company_db).get(id=marketplace_id)
								EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=last_id,field_label=d3,channel_id=marketplace_id)
							marketplacename_arr.append(marketplacename.name)	
							marketplace_name=','.join(marketplacename_arr)
						else:
							marketplacename=EngageboostChannels.objects.using(company_db).get(id=request.data['channel_id'])
							marketplace_name=marketplacename.name
							EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=last_id,field_label=d3,channel_id=request.data['channel_id'])
						User = EngageboostDefaultModuleLayoutFields.objects.using(company_db).create(show_type=request.data['show_type'],field_id=fielsid.id,field_label=d3,input_type=d4,default_values=request.data['default_values'].strip(),is_optional=request.data['is_optional'],data_type='CharField',err_msg='Please enter '+d3,category_id=request.data['category_id'],section_col=cal_val,section_row=row_val,custom_values=custom_values,show_market_places_name=marketplace_name,show_market_places=request.data['channel_id'])
						all_language_data = common.get_all_languages()
						multi_lang_data = []
						for lang_code in all_language_data:
							langcode = lang_code['lang_code']
							lang_id = lang_code['id']
							listcount = len(d2)
							check_str = "_"+langcode
							for key, value in d2.items():
								lang_data = {}
								if check_str in key:
									lang_data = {
										"language_id":lang_id,
										"language_code":langcode,
										"category_id":request.data['category_id'],
										"field_id":fielsid.id,
										"field_name":key,
										"field_lable_value":value,
										'created':datetime.now().date(),
										'modified':datetime.now().date()
									}
									multi_lang_data.append(lang_data)
						save_customfield_lang(multi_lang_data)
					else:
						obj = EngageboostDefaultsFields.objects.using(company_db).latest('id')
						last_id = obj.id
						cal_val=1
						row_val=row+1

						if ',' in str(request.data['channel_id']):

							marketplace_ids=request.data['channel_id'].split(',')
							for marketplace_id in marketplace_ids:
								marketplacename=EngageboostChannels.objects.using(company_db).get(id=marketplace_id)
								EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=last_id,field_label=d3,channel_id=marketplace_id)
							marketplacename_arr.append(marketplacename.name)
							marketplace_name=','.join(marketplacename_arr)
						else:
							marketplacename=EngageboostChannels.objects.using(company_db).get(id=request.data['channel_id'])
							marketplace_name=marketplacename.name
							EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=last_id,field_label=d3,channel_id=request.data['channel_id'])
						User = EngageboostDefaultModuleLayoutFields.objects.using(company_db).create(show_type=request.data['show_type'],field_id=fielsid.id,field_label=d3,input_type=d4,default_values=request.data['default_values'].strip(),custom_values=custom_values,is_optional=request.data['is_optional'],data_type='CharField',err_msg='Please enter '+d3,category_id=request.data['category_id'],section_col=cal_val,section_row=row_val,show_market_places_name=marketplace_name,show_market_places=request.data['channel_id'])

					data ={
					'status':1,
					'message':'Successfully Inserted',
					}
					return Response(data)
			else:
				data ={
					'status':0,
					'message':'already exists',
					}
				return Response(data)

				
# Custom Field Edit Web Services					
class customfieldsedit(generics.ListAPIView):
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostDefaultsFields.objects.using(company_db).get(pk=pk)
		except EngageboostDefaultsFields.DoesNotExist:
			raise Http404

	def get(self, request, pk,cat ,format=None):
		company_db = loginview.db_active_connection(request)
		user = self.get_object(pk,request)
		# serializer = DefaultsFieldsSerializer(user)
		serializer = DefaultsFieldsWithLangSerializer(user, context={'category_id': cat})
		# value = EngageboostDefaultModuleLayoutFields.objects.using(company_db).get(field_id=pk, category_id=cat)
		value = EngageboostDefaultModuleLayoutFields.objects.using(company_db).filter(field_id=pk, category_id=cat).first()
		
		settings4 = EngageboostChannels.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
		serializer4 = ChannelsSerializer(settings4, many=True)
		all_language_data = common.get_all_languages()

		# Get Custom field Lable Value
		serializer_data = serializer.data
		# print(json.dumps(serializer_data))

		if len(serializer_data['lang_data'])>0:
			for land_data in serializer_data['lang_data']:
				serializer_data[land_data['field_name']]=land_data['field_value']
		# serializer_data.pop('lang_data')

		if(serializer): 
			data ={
				'status':1,
				'api_status':serializer_data,
				'custom_values':value.custom_values,
				'default_values':value.default_values,
				'show_type':value.show_type,
				'label':value.field_label,
				'category_id':cat,
				'show_market_places_id':value.show_market_places,
				'channelid':value.channel_categories_id,
				'is_optional':value.is_optional,
				"channel":serializer4.data,
				"all_languages":all_language_data
				}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
		return Response(data)
	def put(self, request,pk,cat, format=None):
		company_db = loginview.db_active_connection(request)
		custedit = self.get_object(pk,request)
		d2=request.data
		d3=request.data['name']
		d4=request.data['input_type']
		name=d3.lower()
		name1=name.replace(" ","-")
		name1 = name1.replace('"','')
		name1 = name1.replace("'",'')
		field_name=name1.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~=+"})
		EngageboostMarketplaceFieldLabels.objects.using(company_db).filter(field_id=pk).delete()
		custom_values=request.data['custom_values']
		channel_id=request.data['channel_id']
		marketplacename_arr=[]
		cnt = EngageboostDefaultsFields.objects.using(company_db).filter(field_name=field_name,input_type=d4,id=pk).count()
		cnt2 = EngageboostDefaultsFields.objects.using(company_db).filter(id=pk).filter(~Q(field_name=field_name)|~Q(input_type=d4)).count()
		# print(cnt)
		# print('&&&')
		# print(cnt2)

		all_language_data = common.get_all_languages()
		multi_lang_data = []
		for lang_code in all_language_data:
			langcode = lang_code['lang_code']
			lang_id = lang_code['id']
			listcount = len(d2)
			check_str = "_"+langcode
			# print(json.dumps(d2))
			for key, value in d2.items():
				lang_data = {}
				if check_str in key:
					lang_data = {
						"language_id":lang_id,
						"language_code":langcode,
						"category_id":cat,
						"field_id":pk,
						"field_name":d2['field_name']+"_"+langcode,
						"field_lable_value":value.lower(),
						'created':datetime.now().date(),
						'modified':datetime.now().date()
					}
					multi_lang_data.append(lang_data)
		print("k1")
		print(multi_lang_data)
		save_customfield_lang(multi_lang_data)

		if cnt > 0:
		
			d1={'name':d3,'field_name':field_name,'err_msg':'Please enter '+d3,'value':d3,'modified':datetime.now().date(),'input_type':d4,'data_type':'CharField','data_length':'255','custom_values':custom_values}
			serializer_data=dict(d2,**d1)
			serializer = DefaultsFieldsSerializer(custedit,data=serializer_data,partial=True)
			if serializer.is_valid():
				serializer.save()
				obj = EngageboostDefaultsFields.objects.using(company_db).latest('id')
				last_id = obj.id
				if ',' in str(request.data['channel_id']):

					marketplace_ids=request.data['channel_id'].split(',')
					for marketplace_id in marketplace_ids:
						
						marketplacename=EngageboostChannels.objects.using(company_db).get(id=marketplace_id)
						
						EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=pk,field_label=d3,channel_id=marketplace_id)
						marketplacename_arr.append(marketplacename.name)	
					marketplace_name=','.join(marketplacename_arr)
					
				else:
					marketplacename=EngageboostChannels.objects.using(company_db).get(id=request.data['channel_id'])
					
					marketplace_name=marketplacename.name
					EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=pk,field_label=d3,channel_id=request.data['channel_id'])
				EngageboostDefaultModuleLayoutFields.objects.using(company_db).filter(field_id=pk).update(show_type=request.data['show_type'],field_label=d3,input_type=d4,default_values=request.data['default_values'],is_optional=request.data['is_optional'],data_type='CharField',err_msg='Please enter '+d3,custom_values=custom_values,show_market_places=channel_id,show_market_places_name=marketplace_name)
				
				data ={
				'status':1,
				'api_status':serializer.errors,
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
		if cnt2 > 0:
			cnt1 = EngageboostDefaultsFields.objects.using(company_db).filter(field_name=field_name,input_type=d4).filter(~Q(id=pk)).count()
			if cnt1 >0:
				field=EngageboostDefaultsFields.objects.using(company_db).get(field_name=field_name,input_type=d4)
				if ',' in str(request.data['channel_id']):

					marketplace_ids=request.data['channel_id'].split(',')
					for marketplace_id in marketplace_ids:
						marketplacename=EngageboostChannels.objects.using(company_db).get(id=marketplace_id)
						
						EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=pk,field_label=d3,channel_id=marketplace_id)
					marketplacename_arr.append(marketplacename.name)	
					marketplace_name=','.join(marketplacename_arr)
					
				else:
					marketplacename=EngageboostChannels.objects.using(company_db).get(id=request.data['channel_id'])
					
					marketplace_name=marketplacename.name
					EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=pk,field_label=d3,channel_id=request.data['channel_id'])
				EngageboostDefaultModuleLayoutFields.objects.using(company_db).filter(field_id=pk).update(show_type=request.data['show_type'],field_id=field.id,field_label=d3,input_type=d4,default_values=request.data['default_values'],is_optional=request.data['is_optional'],data_type='CharField',err_msg='Please enter '+d3,custom_values=custom_values,show_market_places=channel_id,show_market_places_name=marketplace_name)
				EngageboostDefaultsFields.objects.using(company_db).filter(id=pk).delete()
				data ={
				'status':1,
				'message':'Successfully Updated',
				}
				return Response(data)
			else:
				field_check=EngageboostDefaultModuleLayoutFields.objects.using(company_db).filter(category_id=request.data['category_id'],field_label=d3,input_type=d4).filter(~Q(field_id=pk)).count()
				if 	field_check==0:
					d1={'name':d3,'field_name':field_name,'err_msg':'Please enter '+d3,'value':d3,'modified':datetime.now().date(),'input_type':d4,'data_type':'CharField','data_length':'255','custom_values':custom_values}
					serializer_data=dict(d2,**d1)
					serializer = DefaultsFieldsSerializer(custedit,data=serializer_data,partial=True)
					if serializer.is_valid():
						serializer.save()
						obj = EngageboostDefaultsFields.objects.using(company_db).latest('id')
						last_id = obj.id
						if ',' in str(request.data['channel_id']):

							marketplace_ids=request.data['channel_id'].split(',')
							for marketplace_id in marketplace_ids:
								marketplacename=EngageboostChannels.objects.using(company_db).get(id=marketplace_id)
								
								EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=pk,field_label=d3,channel_id=marketplace_id)
							marketplacename_arr.append(marketplacename.name)	
							marketplace_name=','.join(marketplacename_arr)
							
						else:
							marketplacename=EngageboostChannels.objects.using(company_db).get(id=request.data['channel_id'])
							
							marketplace_name=marketplacename.name
							EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=pk,field_label=d3,channel_id=request.data['channel_id'])
						EngageboostDefaultModuleLayoutFields.objects.using(company_db).filter(field_id=pk).update(show_type=request.data['show_type'],field_label=d3,input_type=d4,default_values=request.data['default_values'],is_optional=request.data['is_optional'],data_type='CharField',err_msg='Please enter '+d3,custom_values=custom_values,show_market_places=channel_id,show_market_places_name=marketplace_name)
						
						data ={
						'status':1,
						
						'message':'Successfully Updated',
						}
						return Response(data)
				else:
					data ={
					'status':0,
					'message':'already exists',
					}
					return Response(data)
	# Delete single Custom Field
	def delete(self, request,pk,cat, format=None):
		company_db = loginview.db_active_connection(request)
		custedit = self.get_object(pk,request)
		# EngageboostDefaultsFields.objects.using(company_db).filter(id=pk).delete()
		EngageboostDefaultModuleLayoutFields.objects.using(company_db).filter(field_id=pk,category_id=cat).delete()
		data ={
		'status':1,
		'message':'Successfully Deleted',
		}
		return Response(data)
class field_list(generics.ListAPIView):
	def get(self, request, category_id,channel_id, format=None):
		company_db = loginview.db_active_connection(request)
		str_to_array_channel=''
		user = EngageboostDefaultModuleLayoutFields.objects.using(company_db).all().filter(category_id=category_id).filter( Q(show_market_places__startswith=channel_id+',') | Q(show_market_places__endswith=','+channel_id) | Q(show_market_places__contains=',{0},'.format(channel_id)) | Q(show_market_places__exact=channel_id) ).order_by('section_row','section_col')
		# print(user.query)
		channel_ids=EngageboostDefaultModuleLayoutFields.objects.using(company_db).all().filter(category_id=category_id)
		channel=[]
		arr=[]
		for channels in channel_ids:
			name=channels.show_market_places
			
			channel.append(name)
		if len(channel)>0:	
			str_to_array_channel=','.join(channel)
			sta_value=str_to_array_channel.split(',')
		else:
			sta_value=''
		if(str_to_array_channel):
			settings4 = EngageboostChannels.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').filter(Q(id__in=sta_value) | Q(id=6))
			serializer4 = ChannelsSerializer(settings4, many=True)
			channel=serializer4.data
		else:
			channel=[]
		for Category in user:
			rs_lang = EngageboostCustomFieldMastersLang.objects.filter(field_id=Category.field_id,category_id=category_id).all()
			lang_data = CustomFieldMastersLangSerializer(rs_lang, many=True)
			data ={
				'id':Category.id,
				'field_id':Category.field_id,
				'section_row':Category.section_row,
				'section_col':Category.section_col,
				'field_label':Category.field_label,
				'input_type':Category.input_type,
				'default_values':Category.default_values,
				'value_required':Category.value_required,
				'is_optional':Category.is_optional,
				'is_system':Category.is_system,
				'data_type':Category.data_type,
				'custom_values':Category.custom_values,
				'channelid':Category.show_market_places,
				'lang_data':lang_data.data
				}

			# print('*******************')
			# print(Category.field_label)
			# print(Category.field_id)
			# print('*******************')
			arr.append(data)
		all_language_data = common.get_all_languages()
		return HttpResponse(json.dumps({"value": arr,"channel":channel, "all_languages":all_language_data}), content_type='application/json')
class positionchange(generics.ListAPIView):
		def post(self, request, format=None):
			company_db = loginview.db_active_connection(request)
			rows=request.data['id']
			rows1=request.data['id1']
			row_first = EngageboostDefaultModuleLayoutFields.objects.using(company_db).get(field_id=rows)
			row_second = EngageboostDefaultModuleLayoutFields.objects.using(company_db).get(field_id=rows1)
			cal1=row_first.section_col
			row1=row_first.section_row
			cal2=row_second.section_col
			row2=row_second.section_row
			EngageboostDefaultModuleLayoutFields.objects.using(company_db).filter(field_id=rows).update(section_col=cal2,section_row=row2)
			EngageboostDefaultModuleLayoutFields.objects.using(company_db).filter(field_id=rows1).update(section_col=cal1,section_row=row1)
			data ={
					'status':1,
					'api_status':'',
					'message':'Successfully Updated',
					}
			return Response(data)
class customfieldsimport(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		import xlrd
		# ifile  = open('custom_fields_import.csv', "rt",encoding='latin1')

		import os
		if 'import_file' in request.FILES:
			rand = str(random.randint(1111,9999))
			file1 = request.FILES['import_file']
			file_name=file1.name
			
			ext = file_name.split('.')[-1]
			new_file_name='ImportFile_'+rand
			fs=FileSystemStorage()
			filename = fs.save('importfile/'+new_file_name+'.'+ext, file1)
			uploaded_file_url = fs.url(filename)
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			
			if(ext=='csv'):
			
				csvReader = csv.reader(codecs.open(settings.BASE_DIR+uploaded_file_url, 'r', encoding='utf-8'))
				if(csvReader==""):
					data ={
								'status':0,
								
								'message':'Please Import Utf-8 File',
								}

					return Response(data)
				else:

					reader = list(csvReader)
				arr_message=[]
				for row in reader:
					
					if(row[0]=='Field Name'):
						pass
					else:

						msg=""
						d2=request.data
						category_id= request.data['category_id']
						d3=row[0]
						field_label_symbol_change=row[1]
						# field_label_name=field_label_symbol_change.replace(" ","_")
						field_label=field_label_symbol_change.translate ({ord(c): "" for c in "!@#$%^&*()[]{};\'\":,./<>?\|`~=+"})
						name1=d3.replace(" ","_")
						name1 = name1.replace('"','')
						name1 = name1.replace("'",'')
						field_name=name1.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~=+"})

						d4=row[2]
						input_type=['Textbox','Dropdown','Textarea','Checkbox','Radio']
						isvariant=['Yes','No']
						if d4 not in input_type:
							msg =msg+"Invalid Type Field data"

						values=row[4]
						
						custom_values=values
						default_values=values
						
						isrequerd=row[3]
						isrequerd_view=row[3]
						if isrequerd=='Required':
							isrequerd=1
							
						elif isrequerd=='Optional':
							isrequerd=0

						else:
							msg =msg+",Invalid isRequired Field data"


						channelname=row[5]
						Channels_count = EngageboostChannels.objects.using(company_db).filter(name=channelname).count()
						if Channels_count==0:
							msg =msg+",Invalid Channel Name Field data"
						else:
							Channels = EngageboostChannels.objects.using(company_db).get(name=channelname)
							channelid=Channels.id
						isvariant=row[6]
						if isvariant not in isvariant:
							msg =msg+",Invalid Variant Field data"
						variantname=row[7]

						
							
						if msg=="":


							d2={"FieldName":field_name,'label':field_label,"Type":d4,"IsRequired":isrequerd_view,"ChannelName":channelname,"isvariant":isvariant,"VariantName":variantname,"custom_value":custom_values,"status":1,"msg":""}


						else:
							d2={"FieldName":field_name,'label':field_label,"Type":row[2],"IsRequired":isrequerd_view,"ChannelName":str(row[5]),"isvariant":row[6],"VariantName":row[7],"custom_value":custom_values,"status":0,"msg":msg}
						arr_message.append(d2)
						
									
				return HttpResponse(json.dumps({'msg':arr_message}), content_type='application/json')
			else:
				csvReader = xlrd.open_workbook(settings.BASE_DIR+uploaded_file_url)
				sheet = csvReader.sheet_by_index(0)
				length=len(sheet.col_values(0))
				arr_message=[]
				for x in range(length):
					
					if(sheet.col_values(0)[x]=='Field Name'):
						pass
					else:
						msg=""
						d2=request.data
						category_id= request.data['category_id']

						d3=sheet.col_values(0)[x]
						name1=d3.replace(" ","_")
						name1 = name1.replace('"','')
						name1 = name1.replace("'",'')
						field_name=name1.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~=+"})

						field_label_symbol_change=sheet.col_values(1)[x]
						# field_label_name=field_label_symbol_change.replace(" ","_")
						field_label=field_label_symbol_change.translate ({ord(c): "" for c in "!@#$%^&*\'\"()[]{};:,./<>?\|`~=+"})
						d4=sheet.col_values(2)[x]
						input_type=['Textbox','Dropdown','Textarea','Checkbox','Radio']
						isvariant=['Yes','No']
						if d4 not in input_type:
							msg =msg+"Invalid Type Field data"
						custom_values=sheet.col_values(4)[x]
						default_values=sheet.col_values(4)[x]
						
						isrequerd=sheet.col_values(3)[x]
						isrequerd_view=sheet.col_values(3)[x]
						if isrequerd=='Required':
							isrequerd=1
							
						elif isrequerd=='Optional':
							
							isrequerd=0

						else:
							msg =msg+",Invalid isRequired Field data"
						channelname=sheet.col_values(5)[x]
						Channels_count = EngageboostChannels.objects.using(company_db).filter(name=channelname).count()
						if Channels_count==0:
							msg =msg+",Invalid Channel Name Field data"
						else:
							Channels = EngageboostChannels.objects.using(company_db).get(name=channelname)
							channelid=Channels.id
						isvariant=sheet.col_values(6)[x]
						if isvariant =='Yes':
							isvariant='Yes'
						elif isvariant =='No':
							isvariant='No'
						else:
							msg =msg+",Invalid Variant Field data"
						
						variantname=sheet.col_values(7)[x]
						
						
						if msg=="":
							d2={"FieldName":field_name,"label":field_label,"Type":d4,"IsRequired":isrequerd_view,"ChannelName":channelname,"isvariant":isvariant,"VariantName":variantname,"custom_value":custom_values,"status":1,"msg":""}
						else:
							d2={"FieldName":field_name,"label":field_label,"Type":d4,"IsRequired":isrequerd_view,"ChannelName":channelname,"isvariant":isvariant,"VariantName":variantname,"custom_value":custom_values,"status":0,"msg":msg}
						arr_message.append(d2)
						
				return HttpResponse(json.dumps({'msg':arr_message}), content_type='application/json')
# Default Value For custom Field Update
class customvalueupdate(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		for data in request.data:
			
			EngageboostDefaultModuleLayoutFields.objects.using(company_db).filter(field_id=int(data['field_id'])).update(default_values=data['default_value'])
		
		data ={
			'status':1,
			'message':'Successfully Updated',
		}

		return Response(data)
# customfieldsystemFor custom Field Update
class customfieldsystem(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		for data in request.data:
			
			EngageboostDefaultModuleLayoutFields.objects.using(company_db).filter(field_id=int(data['field_id'])).update(is_system=data['is_system'])
		data ={
				'status':1,
				'message':'Successfully Updated',
				}

		return Response(data)

class customsuccessfieldimport(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		d2=request.data
		category_id= request.data['category_id']
		rows=d2['rows']
		for row in rows:
			d3=row['FieldName']
			field_name=d3.lower()
			field_label=row['label']
			d4=row['Type']
			name=d3.lower()

			
			variantname=row['VariantName']
			values=row['custom_value']
			values_hash=values.replace(',','##')
			custom_values=values_hash
			# default_values=values_hash
			default_values=variantname
			
			isrequerd=row['IsRequired']
			if isrequerd=='Required':
				isrequerd=1
				
			elif isrequerd=='Optional':
				
				isrequerd=0


			channelname=row['ChannelName']
			
			
			
			isvariant=row['isvariant']
			
			
			status=row['status']
			cnt = EngageboostDefaultsFields.objects.using(company_db).filter(field_name=field_name,input_type=d4).count()
			if status == 1:

				Channels = EngageboostChannels.objects.using(company_db).get(name=channelname)
				channelid=Channels.id

				if cnt == 0:

					d1={'name':field_label,'field_name':field_name,'err_msg':'Please enter '+field_label,'value':field_label,'created':datetime.now().date(),'modified':datetime.now().date(),'input_type':d4,'data_type':'CharField','data_length':'255','custom_values':custom_values,'is_optional':isrequerd,"is_variant":isvariant}
					dcat={'category_id':category_id}
					serializer_data=dict(dcat,**d1)
					serializer = DefaultsFieldsSerializer(data=serializer_data,partial=True)
					if serializer.is_valid():
						serializer.save()
						obj = EngageboostDefaultsFields.objects.using(company_db).latest('id')
						last_id = obj.id
						EngageboostMarketplaceFieldLabels.objects.using(company_db).create(created=datetime.now().date(),modified=datetime.now().date(),field_id=last_id,field_label=field_label,channel_id=channelid)
						values=EngageboostDefaultModuleLayoutFields.objects.using(company_db).filter(category_id=category_id).count()
						if values == 0:
							cal_val=1
							row_val=1
							User = EngageboostDefaultModuleLayoutFields.objects.using(company_db).create(channel_categories_id=Channels.id,field_id=last_id,field_label=field_label,input_type=d4,default_values=default_values,is_optional=isrequerd,data_type='CharField',err_msg='Please enter '+field_name,category_id=category_id,section_col=cal_val,section_row=row_val,custom_values=custom_values,show_market_places=channelid,show_market_places_name=channelname)
							data ={
							'status':1,
							'api_status':serializer.errors,
							'message':'Successfully Inserted',
							
							}
							
						else:
							
							row_col = EngageboostDefaultModuleLayoutFields.objects.using(company_db).all().filter(category_id=category_id).order_by('id')
							for col in row_col:
								cal=col.section_col
								row=col.section_row
							
							if cal == 1:
								cal_val=2
								row_val=row
								User = EngageboostDefaultModuleLayoutFields.objects.using(company_db).create(channel_categories_id=Channels.id,field_id=last_id,field_label=field_label,input_type=d4,default_values=default_values,is_optional=isrequerd,data_type='CharField',err_msg='Please enter '+field_name,category_id=category_id,section_col=cal_val,section_row=row_val,custom_values=custom_values,show_market_places=channelid,show_market_places_name=channelname)
							else:
								cal_val=1
								row_val=row+1
								User = EngageboostDefaultModuleLayoutFields.objects.using(company_db).create(channel_categories_id=Channels.id,field_id=last_id,field_label=field_label,input_type=d4,default_values=default_values,is_optional=isrequerd,data_type='CharField',err_msg='Please enter '+field_name,category_id=category_id,section_col=cal_val,section_row=row_val,custom_values=custom_values,show_market_places=channelid,show_market_places_name=channelname)


							data ={
							'status':1,
							'api_status':serializer.errors,
							'message':'Successfully Inserted',
							
							}
							
							
					else:
						data ={
						'status':0,
						'api_status':serializer.errors,
						'message':'Data Not Found',
						}
						
				else:
					field_check=EngageboostDefaultModuleLayoutFields.objects.using(company_db).filter(category_id=request.data['category_id'],field_label=field_label,input_type=d4).count()
					if 	field_check==0:
						values=EngageboostDefaultModuleLayoutFields.objects.using(company_db).filter(category_id=category_id).count()
						fielsid=EngageboostDefaultsFields.objects.using(company_db).filter(field_name=field_name,input_type=d4,is_variant=isvariant,is_optional=isrequerd).first()
						if fielsid:
							pass
						else:
							has_record = EngageboostDefaultsFields.objects.last()
							if has_record:
								last_entry_of_table = EngageboostDefaultsFields.objects.order_by('-id').latest('id')
								row_id = int(last_entry_of_table.id)+int(1)
							else:
								row_id = 1
							fielsid = EngageboostDefaultsFields.objects.using(company_db).create(id=row_id,name=field_label,value=field_label,field_name=field_name,input_type=d4,is_variant=isvariant,is_optional=isrequerd,err_msg='Please enter '+field_name,data_type='CharField',data_length=255)

						if values == 0:
							cal_val=1
							row_val=1
							User = EngageboostDefaultModuleLayoutFields.objects.using(company_db).create(channel_categories_id=Channels.id,field_id=fielsid.id,field_label=field_label,input_type=d4,default_values=default_values,is_optional=isrequerd,data_type='CharField',err_msg='Please enter '+field_name,category_id=category_id,section_col=cal_val,section_row=row_val,custom_values=custom_values,show_market_places=channelid,show_market_places_name=channelname)
							data ={
							'status':1,
							'message':'Successfully Inserted',
							
							}
							
						else:
							
							cat_id=category_id
							row_col = EngageboostDefaultModuleLayoutFields.objects.using(company_db).all().filter(category_id=category_id).order_by('id')
							for col in row_col:
								cal=col.section_col
								row=col.section_row
								
							if cal == 1:
								cal_val=2
								row_val=row
								# print(cat_id)
								
								User = EngageboostDefaultModuleLayoutFields.objects.using(company_db).create(channel_categories_id=Channels.id,field_id=fielsid.id,field_label=field_label,input_type=d4,default_values=default_values,is_optional=isrequerd,data_type='CharField',err_msg='Please enter '+field_name,category_id=cat_id,section_col=cal_val,section_row=row_val,custom_values=custom_values,show_market_places=channelid,show_market_places_name=channelname)
							else:
								cal_val=1
								row_val=row+1
								
								# User = EngageboostDefaultModuleLayoutFields.objects.using(company_db).create(field_id=fielsid.id,field_label=d3,input_type=d4,default_values=default_values,custom_values=custom_values,is_optional=isrequerd,data_type='CharField',err_msg='Please enter '+d3,category_id=cat_id,section_col=cal_val,section_row=row_val)
								User = EngageboostDefaultModuleLayoutFields.objects.using(company_db).create(field_id=fielsid.id,field_label=field_label,input_type=d4,default_values=default_values,custom_values=custom_values,is_optional=isrequerd,data_type='CharField',err_msg='Please enter '+field_name,category_id=cat_id,section_col=cal_val,section_row=row_val,show_market_places=channelid,show_market_places_name=channelname)
								
							data ={
							'status':1,
							'message':'Successfully Inserted',
							
							}
					else:
						data ={
						'status':0,
						'message':'already exists',
						}
			else:
				data ={
				
				'message':'Invalid data',
				}	
		return Response(data)

	

class Channelscustomfield(generics.ListAPIView):
	def get(self, request, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		settings4 = EngageboostChannels.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
		serializer4 = ChannelsSerializer(settings4, many=True)
		all_language_data = common.get_all_languages()
		if(serializer4): 
			data ={
				
				'channel':serializer4.data,
				"all_languages":all_language_data
				}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
		return Response(data)

def GetCustomeFieldLang(field_id):
	if field_id and field_id>0:
		rs_custon_field_lang = EngageboostCustomFieldMastersLang.objects.filter(field_id=field_id).all()
		

def save_customfield_lang(requestdata):
	if requestdata:
		for langdata in requestdata:
			rs_check_exist = EngageboostCustomFieldMastersLang.objects.filter(field_id=langdata['field_id'], category_id=langdata['category_id'], language_code = langdata['language_code'], field_name = langdata['field_name'], isblocked='n', isdeleted='n').all()
			print(rs_check_exist.query)
			if rs_check_exist:
				EngageboostCustomFieldMastersLang.objects.filter(field_id=langdata['field_id'], category_id=langdata['category_id'], language_code = langdata['language_code'], field_name = langdata['field_name'], isblocked='n', isdeleted='n').update(**langdata)
			else:
				EngageboostCustomFieldMastersLang.objects.create(**langdata)
	else:
		data = {}