from webservices.models import *
from django.http import Http404
from django.db.models import Q
from webservices.serializers import *
from frontapp.frontapp_serializers import WebsitePaymentmethodsViewSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
import datetime
from rest_framework import generics
from rest_framework.response import Response
import random
from django.http import HttpResponse
from django.http import HttpResponse
import json
import requests
import random
from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import permission_classes
import os
import socket
from django.conf import settings
from django.db.models import Q
from webservices.views import loginview
import tinys3
import urllib
import base64
import pytz
import sys,math
import traceback
from PIL import Image
import xlrd
import urllib.request

# Basicsettings Insert 
class BasicsettingsList(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		imageresizeon= EngageboostGlobalSettings.objects.using(company_db).get(website_id=1)
		data_string=request.data
		# website_id=datajson['website_id']
		# website_id=data_string['website_id']
		requestdatajson = request.data['data']
		website_id = requestdatajson['website_id']
		try:
			
			if 'website_logo' in request.FILES:
				file1 = request.FILES['website_logo']
				image_name=file1.name
				ext = image_name.split('.')[-1]
				new_image_name='logo_'+image_name+str(website_id)
				website_logo=new_image_name+'.'+ext
				fs=FileSystemStorage()
				filename = fs.save('companylogo/250x185/'+website_logo, file1)
				uploaded_file_url = fs.url(filename)
				BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
				image = Image.open(settings.BASE_DIR+uploaded_file_url)
				width_origenal, height_origenal=image.size
				ImageResize(image,width_origenal,height_origenal,imageresizeon,website_logo)
				has_image = 1
			elif (request.data['website_logo']):
				file1 = request.data['website_logo']
				extrev=file1[::-1]
				extrevore = extrev.split(".")
				ext=extrevore[0][::-1]
				img=urllib.request.urlretrieve(file1, 'companylogo/250x185/'+'logo'+website_id+'.'+ext)
				website_logo='logo'+website_id+'.'+ext
				fs=FileSystemStorage()
				BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
				uploaded_file_url = fs.url(img)
				image = Image.open(settings.BASE_DIR+'/companylogo/250x185/'+website_logo)
				width_origenal, height_origenal=image.size
				ImageResize(image,width_origenal,height_origenal,imageresizeon,website_logo)
				has_image = 1
			else:
				website_logo=''
				has_image = 1

			company_name=requestdatajson['business_name'].upper()
			d1={'created':datetime.datetime.now(),'modified':datetime.datetime.now(),'website_logo':website_logo, 'id_proof':'', 'address_proof':'', 'other_document':'','plan_id':1,'engageboost_template_master_id':0,'engageboost_template_color_master_id':0,'company_name':company_name,'websitename':company_name}
			serializer_data=dict(requestdatajson,**d1)
			# print(serializer_data)
			# serializer_data['country'] = serializer_data['country_id']
			d1={'created':datetime.datetime.now(datetime.timezone.utc).astimezone(),
				'modified':datetime.datetime.now(datetime.timezone.utc).astimezone()
				}
			serializer_data=dict(serializer_data,**d1)
			serializer_data.pop('settingsId')
			serializer_data.pop('website_id')
			serializer_data.pop('banner_image')
			serializer_data.pop('company_id')
			serializer_data.pop('updatedby')

			serializer = CompanyWebsiteSerializer(data=serializer_data,partial=True)
			if serializer.is_valid():
				# serializer.save()
				# latest = EngageboostCompanyWebsites.objects.using(company_db).create(**serializer_data)
				# last_inserted_id = latest.id
				last_inserted_id = 1
				company_cond = EngageboostCompanyWebsites.objects.using(company_db).get(id=last_inserted_id) 
				companywebsitedetails = CompanyWebsiteSerializer(company_cond, partial=True)
				if has_image == 0:
					amazons3_fileupload250(website_logo,companywebsitedetails.data)
				data ={
					'status':1,
					'api_status':last_inserted_id,
					'Message':'Successfully Inserted',
				}
			else:
				data ={
					'status':0,
					'api_status':serializer.errors,
					'Message':'Data Not Found',
				}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}	
		return Response(data)

class Basicsettingsup(APIView):
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostCompanyWebsites.objects.using(company_db).get(pk=pk)
		except EngageboostCompanyWebsites.DoesNotExist:
			raise Http404
	def get(self, request, pk, format=None):
		# company_db = loginview.db_active_connection(request)
		# settings = self.get_object(pk,request)
		# settings_gl = CompanyWebsiteSerializer(settings)
		
		# settings = EngageboostCountries.objects.using(company_db).all().filter(id=settings_gl.data['country_id'])
		# serializer = GlobalsettingscountriesSerializer(settings, many=True)
		
		# serializer_IM = TemplateIndustryMastersSerializer(settings_IM, many=True)

		# country_list_settings = EngageboostCountries.objects.using(company_db).all()
		# country_list = GlobalsettingscountriesSerializer(country_list_settings, many=True)
		# data = {
		# 'status':1,
		# 'company_details':settings_gl.data,
		# 'company_country':serializer.data,
		# 'country_list':country_list.data,
		# 'industrylist':serializer_IM.data
		# }
		# return Response(data)
		try:
			company_db = loginview.db_active_connection(request)
			settings = self.get_object(pk,request)
			settings_gl = CompanyWebsiteSerializer(settings)
			# print(settings_gl.data)
			countryData = ""
			if settings_gl.data['country']:
				settings = EngageboostCountries.objects.using(company_db).all().filter(id=settings_gl.data['country']['id']).order_by('country_name')
				serializer = GlobalsettingscountriesSerializer(settings, many=True)
				countryData = serializer.data

			settings_IM = EngageboostTemplateIndustryMasters.objects.using(company_db).all().order_by('name')
			serializer_IM = TemplateIndustryMastersSerializer(settings_IM, many=True)
			data = {
			'api_status':settings_gl.data,
			'country':countryData,
			'industrylist':serializer_IM.data
			}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}
		return Response(data)

	def put(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		imageresizeon= EngageboostGlobalSettings.objects.using(company_db).get(website_id=1)
		rand = str(random.randint(1111,9999))
		name1 = ''
		website_id='1'
		requestdatajson = json.loads(request.data['data'])
		# return Response(requestdatajson["website_logo"])
		
		if 'website_logo' in request.FILES:
			file1 = request.FILES['website_logo']
			image_name=file1.name
			image_name=image_name.replace(" ","-")
			# image_name=image_name.translate ({ord(c): "-" for c in "!@#$%^&*()[]{};:,./<>?\|`~=+"})
			ext = image_name.split('.')[-1]
			rand=str(random.randint(1,999999999))
			new_image_name='logo_'+rand+'.'+ext
			website_logo=new_image_name
			fs=FileSystemStorage()
			filename = fs.save('companylogo/250x185/'+website_logo, file1)
			uploaded_file_url = fs.url(filename)
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			image = Image.open(settings.BASE_DIR+uploaded_file_url)
			width_origenal, height_origenal=image.size
			
			ImageResize(image,width_origenal,height_origenal,imageresizeon,website_logo)
			has_image = 0
		elif (requestdatajson["website_logo"]):
			file1 = request.data['website_logo']
			website_logo = requestdatajson["website_logo"]
			# extrev=file1[::-1]
			# extrevore = extrev.split(".")
			# ext=extrevore[0][::-1]

			# img=urllib.request.urlretrieve(file1, 'media/companylogo/250x185/'+'logo'+website_id+'.'+ext)

			# website_logo='logo'+website_id+'.'+ext
			# fs=FileSystemStorage()
			# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			# uploaded_file_url = fs.url(img)
			# image = Image.open(settings.BASE_DIR+'/media/companylogo/250x185/'+website_logo)
			# width_origenal, height_origenal=image.size
			# ImageResize(image,width_origenal,height_origenal,imageresizeon,website_logo)
			has_image = 1
		else:
			website_logo=''
			has_image = 1

		d1={'modified':datetime.datetime.now(),'website_logo':website_logo}
		data_string=request.data['data']
		datajson = json.loads(data_string)
		serializer_data=dict(datajson,**d1)
		settings1 = self.get_object(pk,request)
		serializer_data['country'] = serializer_data['country_id']
		print(serializer_data)
		serializer = CompanyWebsiteSerializer1(settings1, data=serializer_data,partial=True)
		if serializer.is_valid():
			serializer.save()
			company_cond = EngageboostCompanyWebsites.objects.using(company_db).get(id=pk) 
			companywebsitedetails = CompanyWebsiteSerializer(company_cond, partial=True)
			print('companywebsitedetails.data')
			print(companywebsitedetails.data['company_name'])
			print(companywebsitedetails.data['s3folder_name'])
			print(companywebsitedetails.data['company_name'])
			if has_image == 0:
				amazons3_fileupload250(website_logo,companywebsitedetails.data)
			
			data ={
			'status':1,
			'api_status':pk,
			'Message':'Successfully Updated',
			}
			return Response(data)
		else:
			data ={
			'status':0,
			'api_status':serializer.errors,
			}
			return Response(data)


class IndustryList(APIView):

	def get(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		settings12 = EngageboostTemplateIndustryMasters.objects.using(company_db).all().order_by('name')
		serializer12 = TemplateIndustryMastersSerializer(settings12, many=True)
		settings1 = EngageboostCountries.objects.using(company_db).all().filter(country_name='India')
		serializer1 = GlobalsettingscountriesSerializer(settings1, many=True)
		settings = EngageboostCountries.objects.using(company_db).all().filter(~Q(country_name='India')).order_by('country_name')
		serializer = GlobalsettingscountriesSerializer(settings, many=True)
		d1=serializer1.data
		d2 = serializer.data
		data=d1+d2
		data ={
		'country':data,
		'Industry':serializer12.data,
		}
		return Response(data)

class TemplatesList(APIView):

	def get(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		settings = EngageboostEmktWebsiteTemplates.objects.using(company_db).all()
		serializer = EmktWebsiteTemplatesSerializer(settings, many=True)
		data ={
		
		'api_status':serializer.data,
		}
		return Response(data)

# Add Template for BasicSetup
class TemplatesEdit(APIView):
	# Get BasicSetup row to update Template
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostCompanyWebsites.objects.using(company_db).get(pk=pk)
		except EngageboostCompanyWebsites.DoesNotExist:
			raise Http404
# Update Template
	def get(self, request,pk, format=None):
		company_db = loginview.db_active_connection(request)
		web_store=EngageboostCompanyWebsites.objects.using(company_db).all().filter(id=pk)
		webstore_serializer=CompanyWebsiteSerializer(web_store,many=True)
		
		settings = EngageboostTemplateMasters.objects.using(company_db).all().filter(isblocked='n',isdeleted='n')
		serializer = BasicTemplateMastersSerializer(settings, many=True)
		data ={
		'webstore_data':webstore_serializer.data,
		'api_status':serializer.data,
		}
		return Response(data)
# Update Template 
	def put(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		d1={'modified':datetime.datetime.now()}
		d2=request.data
		serializer_data=dict(d2,**d1)
		settings = self.get_object(pk,request)
		serializer = CompanyWebsiteSerializer(settings, data=serializer_data,partial=True)
		if serializer.is_valid():
			serializer.save()
			data ={
			'status':1,
			'api_status':pk,
			'Message':'Successfully Updated',
			}
			return JsonResponse(data)
		else:
			data ={
			'status':0,
			'api_status':serializer.errors,
			}
			return Response(data)
#Payment Methods List 
# class PaymentMethodList(APIView):
# 	def get(self, request, format=None):
# 		company_db = loginview.db_active_connection(request)
# 		final_data=[]
# 		paymenttypes = EngageboostPaymentgatewayTypes.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('order_by')
# 		menulist = PaymentMethodListSerializer(paymenttypes, many=True)
# 		for menu in menulist.data:
# 			parentdata={}
# 			child={}
# 			childdata=[]
# 			parentdata=menu
# 			Paymentmethods = EngageboostPaymentgatewayMethods.objects.using(company_db).all().filter(paymentgateway_type_id=menu['id'], isdeleted='n',isblocked='n')
# 			childmenulist = PaymentgatewayMethodsSerializer(Paymentmethods, many=True)
# 			for menu1 in childmenulist.data:
# 				child=menu1
# 				Paymentmethods_fields = EngageboostPaymentgatewaySettings.objects.using(company_db).all().filter(paymentgateway_method_id=menu1['id'], isdeleted='n',isblocked='n').order_by('setting_order_by')
# 				payment_field = PaymentgatewaySettingsSerializer(Paymentmethods_fields, many=True)
# 				child['payment_field']=payment_field.data
# 				childdata.append(child)
# 				parentdata['payment_method']=childdata
# 			final_data.append(parentdata)
# 		return HttpResponse(json.dumps({"paymenttypes":final_data}), content_type='application/json')
# Basicsettings Pay Insert 

class PaymentSetup(generics.ListAPIView):

	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		d2=request.data
		results=d2['data']
		for payment_methods in results:
			 EngageboostPaymentgatewaySettingInformation.objects.using(company_db).create(isblocked=payment_methods['isblocked'],isdeleted=payment_methods['isdeleted'],paymentgateway_type_id=payment_methods['paymentgateway_type_id'],paymentgateway_method_id=payment_methods['paymentgateway_method_id'],setting_key=payment_methods['setting_key'],setting_val=payment_methods['setting_val'])
			 obj = EngageboostPaymentgatewaySettingInformation.objects.using(company_db).latest('id')
			 last_id = obj.id
			 EngageboostWebsitePaymentmethods.objects.using(company_db).create(isblocked=payment_methods['isblocked'],isdeleted=payment_methods['isdeleted'],engageboost_company_website_id=payment_methods['engageboost_company_website_id'],engageboost_paymentgateway_method_id=last_id)
		data ={
		'status':1,
		'api_status':'',
		'Message':'Successfully Inserted',
		}
		return Response(data)

class PaymentSetupView(APIView):
# Get BasicSetup row to update Template
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostPaymentgatewaySettingInformation.objects.using(company_db).get(pk=pk)
		except EngageboostPaymentgatewaySettingInformation.DoesNotExist:
			raise Http404

	def get(self, request,pk, format=None):
		company_db = loginview.db_active_connection(request)
		final_data=[]
		paymenttypes = EngageboostPaymentgatewayTypes.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('order_by')
		menulist = PaymentMethodListSerializer(paymenttypes, many=True)
		for menu in menulist.data:
			parentdata={}
			child={}
			childdata=[]
			value=[]
			parentdata=menu
			Paymentmethods = EngageboostPaymentgatewayMethods.objects.using(company_db).all().filter(paymentgateway_type_id=menu['id'], isdeleted='n',isblocked='n')
			childmenulist = PaymentgatewayMethodsSerializer(Paymentmethods, many=True)
			for menu1 in childmenulist.data:
				child=menu1
				Paymentmethods_website = EngageboostWebsitePaymentmethods.objects.using(company_db).filter(engageboost_company_website_id=pk,engageboost_paymentgateway_method_id=menu1['id'], isdeleted='n',isblocked='n').order_by('setting_order_by').count()
				Paymentmethods_fields = EngageboostPaymentgatewaySettings.objects.using(company_db).all().filter(paymentgateway_method_id=menu1['id'], isdeleted='n',isblocked='n').order_by('setting_order_by')
				payment_field = PaymentgatewaySettingsSerializer(Paymentmethods_fields, many=True)
				# print("Count======",Paymentmethods_website)
				if Paymentmethods_website==0:
					child['is_checked']=0
				else:		
					child['is_checked']=1
				child['payment_field']=payment_field.data

				index = 0
				for payment_field in payment_field.data:
						
					payment_field_values = EngageboostPaymentgatewaySettingInformation.objects.using(company_db).filter(paymentgateway_setting_id=payment_field['id'], isdeleted='n',isblocked='n').first()
					if payment_field_values:
						child['payment_field'][index]['values'] = payment_field_values.setting_val
					index = index +1
				childdata.append(child)
				parentdata['payment_method']=childdata
			final_data.append(parentdata)
		data ={
		
		'api_status':final_data,
		}
		return Response(data)
	
	def put(self, request,pk, format=None):
		company_db = loginview.db_active_connection(request)
		settings = EngageboostWebsitePaymentmethods.objects.using(company_db).all().filter(engageboost_company_website_id=pk)
		serializer = WebsitePaymentmethodsSerializer(settings, many=True)
		final_data=[]
		for menu in serializer.data:
			EngageboostPaymentgatewaySettingInformation.objects.using(company_db).filter(paymentgateway_method_id=menu['engageboost_paymentgateway_method_id']).delete()
		EngageboostWebsitePaymentmethods.objects.using(company_db).filter(engageboost_company_website_id=pk).delete()
		
		d2=request.data
		results=d2['data']
		enabled_methods=d2['enabled_methods']
		enabled_methods = enabled_methods.split(',')
		methods = []
		for payment_methods in results:
			EngageboostPaymentgatewaySettingInformation.objects.using(company_db).create(website_id=payment_methods['website_id'],paymentgateway_type_id=payment_methods['paymentgateway_type_id'],paymentgateway_method_id=payment_methods['paymentgateway_method_id'],setting_key=payment_methods['setting_key'],setting_val=payment_methods['setting_val'],paymentgateway_setting_id=payment_methods['paymentgateway_setting_id'])
			obj = EngageboostPaymentgatewaySettingInformation.objects.using(company_db).latest('id')
			last_id = obj.paymentgateway_method_id
			entry = EngageboostWebsitePaymentmethods.objects.using(company_db).create(engageboost_company_website_id=pk,engageboost_paymentgateway_method_id=last_id)
			# print(entry.id)
			methods.append(str(last_id))
		methods=list(set(methods))
		excluded_payaments = list(set(enabled_methods) - set(methods))
		# print("Entered Methods =====",methods)
		# print("Enable Methods =====",enabled_methods)
		# print("Difference =====",list(set(enabled_methods) - set(methods)))
		for payment_methods in excluded_payaments:
			entry = EngageboostWebsitePaymentmethods.objects.using(company_db).create(engageboost_company_website_id=pk,engageboost_paymentgateway_method_id=int(payment_methods))	
		data ={
		'status':1,
		'api_status':'',
		'Message':'Successfully Updated',
		}
		return Response(data)

#Shipping Methods List
class ShippingList(APIView):
	def get(self, request, shipping_method_id, shipping_type,table_rate_type,shipping_id, format=None):
		company_db = loginview.db_active_connection(request)
		shipping_ids = int(shipping_id)
		shipping_master_settings = EngageboostShippingMasters.objects.using(company_db).get(isblocked='n',isdeleted='n',shipping_type=shipping_type,id=shipping_method_id)
		flat_shipping_details = ShippingSerializer(shipping_master_settings, partial=True)
		shipping_method_id = flat_shipping_details.data['id']

		if shipping_method_id == 5:
			# ship_settings = EngageboostShippingMastersSettings.objects.using(company_db).get(isblocked='n',website_id=1,shipping_method_id=shipping_method_id,table_rate_matrix_type=table_rate_type)
			# shipping_settings_details = ShippingMastersSettingsSerializer(ship_settings, partial=True)

			ship_settings = EngageboostShippingMastersSettings.objects.using(company_db).filter(website_id=1,shipping_method_id=shipping_method_id,table_rate_matrix_type=table_rate_type)
			shipping_settings_details = ShippingMastersSettingsSerializer(ship_settings, many=True)
		elif shipping_method_id == 1 or shipping_method_id == 2 or shipping_method_id == 3 or shipping_method_id == 7:
			ship_settings = EngageboostShippingMastersSettings.objects.using(company_db).all().filter(website_id=1,shipping_method_id=shipping_method_id)
			shipping_settings_details = ShippingMastersSettingsSerializer(ship_settings, many=True)
		else:
			if shipping_ids == 0:
				# print(1)
				ship_settings = EngageboostShippingMastersSettings.objects.using(company_db).all().filter(website_id=1,shipping_method_id=shipping_method_id)
				shipping_settings_details = ShippingMastersSettingsSerializer(ship_settings, many=True)
			else:
				# print(2)
				ship_settings = EngageboostShippingMastersSettings.objects.using(company_db).all().filter(website_id=1,shipping_method_id=shipping_method_id,id=shipping_id)
				shipping_settings_details = ShippingMastersSettingsSerializer(ship_settings, many=True)

		if shipping_method_id == 5:
			datas=[]
			for shipping_settings_table_rate in shipping_settings_details.data:
				ship_order_amount_cond = EngageboostShippingTableRateOrderAmount.objects.using(company_db).all().filter(shipping_masters_setting_id=shipping_settings_table_rate['id'])
				ship_order_amount_details = ShippingTableRateOrderAmountSerializer(ship_order_amount_cond, many=True)

				for shipping_settings in ship_order_amount_details.data:
					currency_settings = EngageboostCurrencyMasters.objects.using(company_db).get(engageboost_country_id=shipping_settings['country_id'])
					currency_master = CurrencyMastersSerializer(currency_settings,partial=True)
					shipping_settings['currency_code'] = currency_master.data['currency']

					country_settings = EngageboostCountries.objects.using(company_db).all().filter(id=shipping_settings['country_id']).first()
					if country_settings:
						country_details = GlobalsettingscountriesSerializer(country_settings)
						shipping_settings['country_name'] = country_details.data['country_name']
					else:
						shipping_settings['country_name'] = {}
					
					state_cond = EngageboostStates.objects.using(company_db).all().filter(id=shipping_settings['state_id'],country_id=shipping_settings['country_id']).exists()				
					#shipping_settings['state'] = state_details.data

					if not state_cond:
						shipping_settings['state'] = {}
					else:
						state_conds = EngageboostStates.objects.using(company_db).get(id=shipping_settings['state_id'])
						state_details = StatesSerializer(state_conds, partial=True)
						shipping_settings['state'] = state_details.data
					datas.append(shipping_settings)
				
			if datas:
				data ={'status':1,'shipping_info':datas}
			else:
				data ={'status':0,'shipping_info':datas}
			return Response(data)
		elif shipping_method_id == 1 or shipping_method_id == 2 or shipping_method_id == 3 or shipping_method_id == 7:
			if shipping_settings_details.data:
				for shipping_settings in shipping_settings_details.data:			
					country_settings = EngageboostCountries.objects.using(company_db).all()
					country_details = GlobalsettingscountriesSerializer(country_settings, many=True)
					shipping_settings['countries'] = country_details.data
					data ={'status':1,'shipping_info':shipping_settings_details.data}
			else:
				shipping_settings_arr = [];shipping_settings = {}
				country_settings = EngageboostCountries.objects.using(company_db).all()
				country_details = GlobalsettingscountriesSerializer(country_settings, many=True)
				shipping_settings['countries'] = country_details.data
				shipping_settings_arr.append(shipping_settings)

				data ={'status':0,'shipping_info':shipping_settings_arr}
			return Response(data)
		else:
			for shipping_settings in shipping_settings_details.data:
				currency_settings = EngageboostCurrencyMasters.objects.using(company_db).filter(engageboost_country_id=shipping_settings['country_ids'],isblocked="n",isdeleted="n").first()
				currency_master = CurrencyMastersSerializer(currency_settings,partial=True)
				if currency_master:					
					shipping_settings['currency_code'] = currency_master.data['currency']
				
				country_settings = EngageboostCountries.objects.using(company_db).get(id=shipping_settings['country_ids'])
				country_details = GlobalsettingscountriesSerializer(country_settings,partial=True)
				shipping_settings['country_name'] = country_details.data['country_name']

				data ={
				'status':1,
				'shipping_info':shipping_settings_details.data,
				}
			return Response(data)

class StateList(APIView):
	def get(self, request,pk, format=None):
		company_db = loginview.db_active_connection(request)
		settings = EngageboostStates.objects.using(company_db).all().filter(country_id=pk)
		serializer = StatesSerializer(settings, many=True)
		data ={
		'api_status':serializer.data,
		}
		return Response(data)

class ShippingSetup(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		post_data = request.data
		d2 = request.data
		# website_id = post_data['website_id']
		website_id = 1
		shipping_method_id = post_data['shipping_method_id']
		
		shipping_master_cond = EngageboostShippingMasters.objects.using(company_db).filter(isblocked='n',isdeleted='n',id=shipping_method_id).first()
		shipping_master_details = ShippingSerializer(shipping_master_cond, partial=True)
		

		d1={"website_id":website_id,"shipping_method_id":shipping_method_id}
		serializer_data=dict(d2,**d1)

		try:
			if post_data['shipping_id']: shipping_id = post_data['shipping_id'] # this is primary key(id) of the table/ only require when update
			else: shipping_id = 0
		except KeyError: shipping_id = 0

		try:
			if post_data['title']: title = post_data['title']
			else: title = ""
		except KeyError: title = ""
		d1={"title":title};serializer_data=dict(d2,**d1)

		try:
			if post_data['country_ids']: country_ids = post_data['country_ids']
			else: country_ids = ""
		except KeyError:
			country_ids = ""
		d1={"country_ids":country_ids};serializer_data=dict(d2,**d1)

		try:
			if post_data['mthod_type']: mthod_type = post_data['mthod_type']
			else: mthod_type = ""
		except KeyError:
			mthod_type = ""
		d1={"mthod_type":mthod_type};serializer_data=dict(d2,**d1)

		try:
			if post_data['flat_price']: flat_price = post_data['flat_price']
			else: flat_price = ""
		except KeyError:
			flat_price = ""
		d1={"flat_price":flat_price};serializer_data=dict(d2,**d1)

		try:
			if post_data['method_name']: method_name = post_data['method_name']
			else: method_name = ""
		except KeyError:
			method_name = ""
		d1={"method_name":method_name};serializer_data=dict(d2,**d1)

		try:
			if post_data['description']: description = post_data['description']
			else: description = ""
		except KeyError:
			description = ""
		d1={"description":description};serializer_data=dict(d2,**d1)

		try:
			if post_data['handling_fees_type']: handling_fees_type = post_data['handling_fees_type']
			else: handling_fees_type = "0"
		except KeyError:
			handling_fees_type = "0"
		d1={"handling_fees_type":handling_fees_type};serializer_data=dict(d2,**d1)

		try:
			if post_data['handling_price']: handling_price = post_data['handling_price']
			else: handling_price = ""
		except KeyError:
			handling_price = ""
		d1={"handling_price":handling_price};serializer_data=dict(d2,**d1)

		try:
			if post_data['dispatch_time_max']: dispatch_time_max = post_data['dispatch_time_max']
			else: dispatch_time_max = ""
		except KeyError:
			dispatch_time_max = ""
		d1={"dispatch_time_max":dispatch_time_max};serializer_data=dict(d2,**d1)

		try:
			if post_data['customer_code']: customer_code = post_data['customer_code']
			else: customer_code = ""
		except KeyError:
			customer_code = ""
		d1={"customer_code":customer_code};serializer_data=dict(d2,**d1)

		try:
			if post_data['customer_code_cod']: customer_code_cod = post_data['customer_code_cod']
			else: customer_code_cod = ""
		except KeyError:
			customer_code_cod = ""
		d1={"customer_code_cod":customer_code_cod};serializer_data=dict(d2,**d1)

		try:
			if post_data['origin_area']: origin_area = post_data['origin_area']
			else: origin_area = ""
		except KeyError:
			origin_area = ""
		d1={"origin_area":origin_area};serializer_data=dict(d2,**d1)

		try:
			if post_data['state_id']: state_id = post_data['state_id']
			else: state_id = ""
		except KeyError:
			state_id = ""
		d1={"state_id":state_id};serializer_data=dict(d2,**d1)

		try:
			if post_data['is_ebay']: 
				if post_data['is_ebay'] == "y":
					is_ebay = "y"
					state_id = ""
					applicable_for = 'E'
				else:
					is_ebay = "n"
					applicable_for = 'W'
			else:
				is_ebay = "n"
				applicable_for = 'W'
		except KeyError:
			is_ebay = "n"
			applicable_for = 'W'
		d1={"is_ebay":is_ebay,"applicable_for":applicable_for,"state_id":state_id};serializer_data=dict(d2,**d1)

		try:
			if post_data['service_methods']: service_methods = post_data['service_methods']
			else: service_methods = ""
		except KeyError:
			service_methods = ""
		d1={"service_methods":service_methods};serializer_data=dict(d2,**d1)

		try:
			if post_data['table_rate_matrix_type']: table_rate_matrix_type = post_data['table_rate_matrix_type']
			else: table_rate_matrix_type = ""
		except KeyError:
			table_rate_matrix_type = ""
		d1={"table_rate_matrix_type":table_rate_matrix_type};serializer_data=dict(d2,**d1)

		try:
			if post_data['minimum_order_amount']: minimum_order_amount = post_data['minimum_order_amount']
			else: minimum_order_amount = 0
		except KeyError:
			minimum_order_amount = 0
		d1={"minimum_order_amount":minimum_order_amount};serializer_data=dict(d2,**d1)

		try:
			if post_data['ups_account_number']: ups_account_number = post_data['ups_account_number']
			else: ups_account_number = ""
		except KeyError:
			ups_account_number = ""
		d1={"ups_account_number":ups_account_number};serializer_data=dict(d2,**d1)

		try:
			if post_data['ups_user_id']: ups_user_id = post_data['ups_user_id']
			else: ups_user_id = ""
		except KeyError:
			ups_user_id = ""
		d1={"ups_user_id":ups_user_id};serializer_data=dict(d2,**d1)

		try:
			if post_data['ups_password']: ups_password = post_data['ups_password']
			else: ups_password = ""
		except KeyError:
			ups_password = ""
		d1={"ups_password":ups_password};serializer_data=dict(d2,**d1)

		try:
			if post_data['ups_weight_unit']: ups_weight_unit = post_data['ups_weight_unit']
			else: ups_weight_unit = ""
		except KeyError:
			ups_weight_unit = ""
		d1={"ups_weight_unit":ups_weight_unit};serializer_data=dict(d2,**d1)

		try:
			if post_data['ups_min_weight']: ups_min_weight = post_data['ups_min_weight']
			else: ups_min_weight = ""
		except KeyError:
			ups_min_weight = ""
		d1={"ups_min_weight":ups_min_weight};serializer_data=dict(d2,**d1)

		try:
			if post_data['ups_max_weight']: ups_max_weight = post_data['ups_max_weight']
			else: ups_max_weight = ""
		except KeyError:
			ups_max_weight = ""
		d1={"ups_max_weight":ups_max_weight};serializer_data=dict(d2,**d1)

		try:
			if post_data['package_code']: package_code = post_data['package_code']
			else: package_code = "0"
		except KeyError:
			package_code = "0"
		d1={"package_code":package_code};serializer_data=dict(d2,**d1)

		try:
			if post_data['usps_user_id']: usps_user_id = post_data['usps_user_id']
			else: usps_user_id = ""
		except KeyError:
			usps_user_id = ""
		d1={"usps_user_id":usps_user_id};serializer_data=dict(d2,**d1)

		try:
			if post_data['usps_password']: usps_password = post_data['usps_password']
			else: usps_password = ""
		except KeyError:
			usps_password = ""
		d1={"usps_password":usps_password};serializer_data=dict(d2,**d1)

		try:
			if post_data['usps_devolopment_mode']: usps_devolopment_mode = post_data['usps_devolopment_mode']
			else: usps_devolopment_mode = "0"
		except KeyError:
			usps_devolopment_mode = "0"
		d1={"usps_devolopment_mode":usps_devolopment_mode};serializer_data=dict(d2,**d1)

		try:
			if post_data['usps_size']: usps_size = post_data['usps_size']
			else: usps_size = ""
		except KeyError:
			usps_size = ""
		d1={"usps_size":usps_size};serializer_data=dict(d2,**d1)

		try:
			if post_data['usps_machinable']: usps_machinable = post_data['usps_machinable']
			else: usps_machinable = ""
		except KeyError:
			usps_machinable = ""
		d1={"usps_machinable":usps_machinable};serializer_data=dict(d2,**d1)

		try:
			if post_data['status']: status = post_data['status']
			else: status = "no"
		except KeyError:
			status = "no"
		d1={"status":status};serializer_data=dict(d2,**d1)

		try:
			if post_data['fedex_user_id']: fedex_user_id = post_data['fedex_user_id']
			else: fedex_user_id = ""
		except KeyError:
			fedex_user_id = ""
		d1={"fedex_user_id":fedex_user_id};serializer_data=dict(d2,**d1)

		try:
			if post_data['fedex_meter_no']: fedex_meter_no = post_data['fedex_meter_no']
			else: fedex_meter_no = ""
		except KeyError:
			fedex_meter_no = ""
		d1={"fedex_meter_no":fedex_meter_no};serializer_data=dict(d2,**d1)

		try:
			if post_data['fedex_key']: fedex_key = post_data['fedex_key']
			else: fedex_key = ""
		except KeyError:
			fedex_key = ""
		d1={"fedex_key":fedex_key};serializer_data=dict(d2,**d1)

		try:
			if post_data['fedex_password']: fedex_password = post_data['fedex_password']
			else: fedex_password = ""
		except KeyError:
			fedex_password = ""
		d1={"fedex_password":fedex_password};serializer_data=dict(d2,**d1)

		try:
			if post_data['usps_intr_package']: usps_intr_package = post_data['usps_intr_package']
			else: usps_intr_package = ""
		except KeyError:
			usps_intr_package = ""
		d1={"usps_intr_package":usps_intr_package};serializer_data=dict(d2,**d1)

		try:
			if post_data['usps_intr_package']: usps_intr_package = post_data['usps_intr_package']
			else: usps_intr_package = "0"
		except KeyError:
			usps_intr_package = "0"
		d1={"usps_intr_package":usps_intr_package};serializer_data=dict(d2,**d1)

		try:
			if post_data['self_pickup_price']: self_pickup_price = post_data['self_pickup_price']
			else: self_pickup_price = ""
		except KeyError:
			self_pickup_price = ""
		d1={"self_pickup_price":self_pickup_price};serializer_data=dict(d2,**d1)

		try:
			if post_data['zone_id']: zone_id = post_data['zone_id']
			else: zone_id = ""
		except KeyError:
			zone_id = ""
		d1={"zone_id":zone_id};serializer_data=dict(d2,**d1)

		# return Response(serializer_data)

		#{"website_id":1,"title":"Flat Shipping Test","country_ids":"99","mthod_type":2,"flat_price":"50.00","method_name":"","description":"Flat Shipping Method","handling_fees_type":0,"handling_price":"10","dispatch_time_max":"5","customer_code":"","customer_code_cod":"","origin_area":"","state_id":"1,2","is_ebay":"N","minimum_order_amount":"","ups_account_number":"","ups_user_id":"","ups_password":"","ups_weight_unit":"","ups_min_weight":"","ups_max_weight":"","package_code":"","usps_user_id":"","usps_password":"","usps_devolopment_mode":"","usps_size":"","usps_machinable":"","status":"","fedex_user_id":"","fedex_meter_no":"","fedex_key":"","fedex_password":"","usps_intr_package":""}

		if shipping_id == 0 or shipping_id == "0":
			has_record = EngageboostShippingMastersSettings.objects.last()
			if has_record:
				last_entry_of_table = EngageboostShippingMastersSettings.objects.order_by('-id').latest('id')
				row_id = int(last_entry_of_table.id)+int(1)
			else:
				row_id = 1

			d1={"id":row_id};serializer_data=dict(d2,**d1)

			serializer_data.pop('shipping_id')

			shipping_method = EngageboostShippingMastersSettings.objects.using(company_db).create(**serializer_data)
			last_inserted_id = shipping_method.id

			if shipping_method:
				data ={
				'status':1,
				'api_status':last_inserted_id,
				'message':'Data Saved Successfully',
				}
				return Response(data)
			else:
				data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Error Occured',
				}
				return Response(data)
		else:
			serializer_data.pop('shipping_id')
			shipping_method = EngageboostShippingMastersSettings.objects.using(company_db).get(id=shipping_id)
			serializer = ShippingMastersSettingsSerializer(shipping_method, data=serializer_data,partial=True)
			if serializer.is_valid():
				serializer.save()
				data ={
				'status':1,
				'api_status':'Data Updated Successfully',
				'message':'Data Updated Successfully',
				}
				return Response(data)
			else:
				data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Error Occured',
				}
				return Response(data)

class SaveTableRate(generics.ListAPIView):
	def post(self,request,format=None):
		company_db = loginview.db_active_connection(request)
		datas=[]
		# ifile  = open('custom_fields_import.csv', "rt",encoding='latin1')
		post_data = json.loads(request.data['data'])
		website_id = post_data['website_id']
		shipping_method_id = post_data['shipping_method_id']

		try:
			if post_data['title']: title = post_data['title']
			else: title = ""
		except KeyError: title = ""

		try:
			if post_data['description']: description = post_data['description']
			else: description = ""
		except KeyError:
			description = ""

		try:
			if post_data['handling_fees_type']: handling_fees_type = post_data['handling_fees_type']
			else: handling_fees_type = "0"
		except KeyError:
			handling_fees_type = "0"

		try:
			if post_data['handling_price']: handling_price = post_data['handling_price']
			else: handling_price = ""
		except KeyError:
			handling_price = ""

		try:
			if post_data['table_rate_matrix_type']: table_rate_matrix_type = post_data['table_rate_matrix_type']
			else: table_rate_matrix_type = "0"
		except KeyError:
			table_rate_matrix_type = "0"

		last_entry_of_table = EngageboostShippingMastersSettings.objects.order_by('-id').latest('id')
		if last_entry_of_table:
			row_id = int(last_entry_of_table.id)+int(1)
		else:
			row_id = 1

		shipping_method = EngageboostShippingMastersSettings.objects.using(company_db).create(id=row_id,website_id=website_id,shipping_method_id=shipping_method_id,title=title,description=description,handling_price=handling_price,handling_fees_type=handling_fees_type,table_rate_matrix_type=table_rate_matrix_type)
		last_inserted_id = shipping_method.id

		if 'import_file' in request.FILES:
			rand = str(random.randint(1111,9999))
			file1 = request.FILES['import_file']
			file_name=file1.name
			# print(file_name)
			
			ext = file_name.split('.')[-1]
			new_file_name='ImportFile_'+rand
			fs=FileSystemStorage()
			filename = fs.save('importfile/shipping/'+new_file_name+'.'+ext, file1)
			uploaded_file_url = fs.url(filename)
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

			csvReader = xlrd.open_workbook(settings.BASE_DIR+uploaded_file_url)
			sheet = csvReader.sheet_by_index(0)
			length=len(sheet.col_values(0))
			arr_message=[]
			for x in range(length):
				if(sheet.col_values(0)[x]=='Country'):
					pass
				else:
					country_name=sheet.col_values(0)[x]
					country_cond = EngageboostCountries.objects.using(company_db).all().filter(country_name=country_name).first()
					if country_cond:
						country_serializer = GlobalsettingscountriesSerializer(country_cond)
						country_id = country_serializer.data['id']
					else:
						country_id = 0

					state_name=sheet.col_values(1)[x]
					state_cond = EngageboostStates.objects.using(company_db).all().filter(country_id=country_id,state_name=state_name).first()					
					if state_cond:
						state_serializer = StatesSerializer(state_cond)
						state_id = state_serializer.data['id']
					else:
						state_id = 0
					zipcode = str(sheet.col_values(2)[x])
					weight = sheet.col_values(3)[x]
					shipping_price = sheet.col_values(4)[x]

					# data={"country_id":country_id,"state_id":state_id,"zipcode":zipcode,"weight":weight,"shipping_price":shipping_price}

					shipping_table_rate_order_amount = EngageboostShippingTableRateOrderAmount.objects.using(company_db).create(shipping_masters_setting_id=last_inserted_id,country_id=country_id,state_id=state_id,zip_code=zipcode,weight=weight,shipping_price=shipping_price)
					if shipping_table_rate_order_amount:
						last_table_rate_order_amount_id = shipping_table_rate_order_amount.id
						datas.append(last_table_rate_order_amount_id)
					else:
						datas.append('failed')

			data = {"status":1,"api_response":datas,"message":"Success"}
			return Response(data)
		else:
			data = {"status":1,"api_response":"Error in file import","message":"Error in file import"}
			return Response(data)

class FedexZipcodeSetup(generics.ListAPIView):
	def post(self,request,format=None):
		company_db = loginview.db_active_connection(request)
		datas=[]
		post_data = request.data
		website_id = post_data['website_id']
		# shipping_method_id = post_data['shipping_method_id']

		try:
			if post_data['title']: title = post_data['title']
			else: title = ""
		except KeyError: title = ""

		try:
			if post_data['description']: description = post_data['description']
			else: description = ""
		except KeyError:
			description = ""


		if 'import_file' in request.FILES:
			rand = str(random.randint(1111,9999))
			file1 = request.FILES['import_file']
			file_name=file1.name
			# print(file_name)
			
			ext = file_name.split('.')[-1]
			new_file_name='ImportFile_'+rand
			fs=FileSystemStorage()
			filename = fs.save('importfile/fedexzipcode/'+new_file_name+'.'+ext, file1)
			uploaded_file_url = fs.url(filename)
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

			csvReader = xlrd.open_workbook(settings.BASE_DIR+uploaded_file_url)
			sheet = csvReader.sheet_by_index(0)
			length=len(sheet.col_values(0))
			arr_message=[]
			for x in range(length):
				if(sheet.col_values(0)[x]=='PINCODE'):
					pass
				else:
					pincode=int(round(sheet.col_values(0)[x]))
					prepaid=sheet.col_values(1)[x]
					cod=sheet.col_values(2)[x]
					country_name=sheet.col_values(3)[x]
					cityname=sheet.col_values(4)[x]
					state_name=sheet.col_values(5)[x]

					if prepaid=="Yes":
						prepaid = 'y'
					else:
						prepaid = 'n'

					if cod=="Yes":
						cod = 'y'
					else:
						cod = 'n'	

					country_cond = EngageboostCountries.objects.using(company_db).all().filter(country_name=country_name).first()
					if country_cond:
						country_serializer = GlobalsettingscountriesSerializer(country_cond)
						country_id = country_serializer.data['id']
					else:
						country_id = 0

					state_cond = EngageboostStates.objects.using(company_db).all().filter(country_id=country_id,state_name=state_name).first()
					if state_cond:
						state_serializer = StatesSerializer(state_cond)
						state_id = state_serializer.data['id']
					else:
						state_id = 0

					has_record = EngageboostFedexZipcodes.objects.last()
					if has_record:
						last_entry_of_table = EngageboostFedexZipcodes.objects.order_by('-id').latest('id')
						row_id = int(last_entry_of_table.id)+int(1)
					else:
						row_id = 1

					fedexzipcodelist = EngageboostFedexZipcodes.objects.using(company_db).create(website_id=1,id=row_id,country_id=country_id,state_id=state_id,state_name=state_name,pincode=pincode,prepaid=prepaid,cod=cod,city_name=cityname,name=title,description=description)
					if fedexzipcodelist:
						last_fedexzipcode_id = fedexzipcodelist.id
						datas.append(last_fedexzipcode_id)
					else:
						datas.append('failed')

			data = {"status":1,"api_response":datas,"message":"Success"}
			return Response(data)
		else:
			data = {"status":1,"api_response":"Error in file import","message":"Error in file import"}
			return Response(data)

class FedexZipcodeDelete(generics.ListAPIView):
	def post(self,request,format=None):
		company_db = loginview.db_active_connection(request)
		post_data = request.data
		ids=post_data['id']
		del_ids=EngageboostFedexZipcodes.objects.using(company_db).filter(id__in=ids)
		if del_ids.count()>0:
			del_ids.delete()
			data = {"status":1,"api_response":"","message":"Deleted Successfully"}
		else :
			data = {"status":0,"api_response":"","message":"Data not found"}											
		return Response(data)
		
class FedexZipcodeList(generics.ListAPIView):
	def get(self,request,format=None):
		company_db = loginview.db_active_connection(request)
		fedexzipcodelist = EngageboostFedexZipcodes.objects.using(company_db).all().order_by('-id')

		if fedexzipcodelist:
			fedexzipcodelistSerializer = FedexZipcodesSerializer(fedexzipcodelist,many=True)
			for fedexzipcode in fedexzipcodelistSerializer.data:
				country_settings = EngageboostCountries.objects.using(company_db).all().filter(id=fedexzipcode['country_id']).first()
				country_details = GlobalsettingscountriesSerializer(country_settings)							
				fedexzipcode['country_name'] = country_details.data['country_name']
				# return Response(country_details.data)		
				# if country_settings:
				# 	country_details = GlobalsettingscountriesSerializer(country_settings)							
				# 	fedexzipcode['country_name'] = country_details.data['country_name']
				# else:
				# 	fedexzipcode['country_name'] = ""

				data = {"status":1,"api_response":fedexzipcodelistSerializer.data,"message":"Success"}
				return Response(data)
		else:
			data = {"status":0,"api_response":[],"message":"No Data Found"}
			return Response(data)

class ShippingMethodUpdate(generics.ListAPIView):
# """ List all Edit,Uodate Shipping Method """
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostShippingMastersSettings.objects.using(company_db).get(pk=pk)
		except EngageboostShippingMastersSettings.DoesNotExist:
			raise Http404

	def post(self, request, pk, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		user = self.get_object(pk,request)
		country_ids=request.data['country_id']
		serializer = ShippingMastersSettingsSerializer(user)
		settings1 = EngageboostCountries.objects.using(company_db).all().filter(country_name='India')
		serializer1 = GlobalsettingscountriesSerializer(settings1, many=True)
		settings = EngageboostCountries.objects.using(company_db).all().filter(~Q(country_name='India')).order_by('country_name')
		serializer = GlobalsettingscountriesSerializer(settings, many=True)
		d1=serializer1.data
		d2 = serializer.data
		data=d1+d2
		settings_state = EngageboostStates.objects.using(company_db).all().filter(country_id=country_ids)
		states = StatesSerializer(settings_state, many=True)
		if(serializer): 
			data ={
				'status':1,
				'api_status':serializer.data,
				'country':data,
				'state':states.data,
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
		Category = self.get_object(pk,request)
		d1={'modified':datetime.date.today()}
		d2=request.data
		serializer_data=dict(d2,**d1)
		serializer = ShippingMastersSettingsSerializer(Category,data=serializer_data,partial=True)
		if serializer.is_valid():
			serializer.save()
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
# class ChannelList(APIView):
# 	def get(self, request, format=None):
# 		company_db = loginview.db_active_connection(request)
# 		settings = EngageboostChannels.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
# 		serializer = ChannelsSerializer(settings, many=True)
# 		data ={
# 		'api_status':serializer.data,
# 		}
# 		return Response(data)

# class ChannelSetup(APIView):
# 	def post(self, request, format=None):
# 		company_db = loginview.db_active_connection(request)
# 		js=request.data
# 		ourResult = js['table']
# 		engageboost_company_website_id=ourResult['website_id']
# 		ourResult1 = js['data']
# 		for data in ourResult1:
# 			queryset=EngageboostWebsiteChannels.objects.using(company_db).create(engageboost_channel_id=data['channel_id'],engageboost_company_website_id=engageboost_company_website_id)
# 			data ={
# 			'status':1,
# 			'Message':'Successfully Inserted',
# 			}
# 		return Response(data)

class ChannelViewList(APIView):
	def get(self, request,pk, format=None):
		company_db = loginview.db_active_connection(request)
		channel_id_arr=[]
		listingArr=[]
		d2=[]
		website_channel  =	EngageboostWebsiteChannels.objects.using(company_db).all().filter(engageboost_company_website_id=pk)
		for channel_list in website_channel:
			channel_id_arr.append(channel_list.engageboost_channel_id)

		#print(channel_id_arr)

		all_channel = EngageboostChannels.objects.using(company_db).all().filter(~Q(id='6'),~Q(parent_id='0'),isdeleted='n',isblocked='n').distinct('parent_id')
		for channel in all_channel:
			#print(str(channel.parent_id)+' '+str(channel.id))
			parent_id = (channel.parent_id)

			if channel.id in channel_id_arr:
				d2.append({"name":channel.parent_name,"parent_id":channel.parent_id,"channel_id":channel.id,"parent_logo":channel.parent_logo,"description":channel.description,"status":1})
			else:
				d2.append({"name":channel.parent_name,"parent_id":channel.parent_id,"channel_id":channel.id,"parent_logo":channel.parent_logo,"description":channel.description,"status":0})
			# d2.append({parent_id:d1})
			
			# d2[parent_id]= {"name":channel.parent_name,"parent_id":channel.parent_id,"channel_id":channel.id,"parent_logo":channel.parent_logo,"description":channel.description}
			# if channel.id in channel_id_arr:
			# 	#d2={"channel":channel.id,"name":channel.name,"image":channel.image,"description":channel.description,"site":channel.site,"website_name":channel.website_name,"status":1}
			# 	d2[parent_id]['status'] = 1
			# else:
			# 	#d2={"channel":channel.id,"name":channel.name,"image":channel.image,"description":channel.description,"site":channel.site,"website_name":channel.website_name,"status":0}
			# 	d2[parent_id]['status'] = 0

		# listingArr= d2
		data ={
			'status':1,
			'channels':d2,
			}
		return Response(data)
		#return HttpResponse(json.dumps({"channels": listingArr}), content_type='application/json')
	
	def put(self, request,pk, format=None):
		company_db = loginview.db_active_connection(request)
		js=request.data
		ourResult1 = js['data']
		EngageboostWebsiteChannels.objects.using(company_db).filter(engageboost_company_website_id=pk).delete()
		for data in ourResult1:
			queryset=EngageboostWebsiteChannels.objects.using(company_db).create(engageboost_channel_id=data['channel_id'],engageboost_company_website_id=pk)
			data ={
			'status':1,
			'Message':'Successfully Updated',
			}
		return Response(data)

class AmazonCredential(generics.ListAPIView):
	def get(self,request,website_id,channel_id,format=None):
		company_db = loginview.db_active_connection(request)
		channel_credential_arr=[]
		#response={}

		if channel_id == '2':
			#print("---1")
			all_channel = EngageboostChannels.objects.using(company_db).all().filter(parent_id=channel_id,isdeleted='n',isblocked='n')			
			for channel in all_channel:
				invidual_channel_credential = EngageboostAmazonCredentials.objects.using(company_db).all().filter(channel_parrent_id=channel.parent_id,channel_id=channel.id,company_website_id=website_id)
				serializer = AmazonCredentialsSerializer(invidual_channel_credential, many=True)
				#print(serializer.data[0])
				if invidual_channel_credential.exists():
					# channel_credential_arr[channel.id] = {"merchant_id":serializer.data[0]['merchant_id'],"access_key":serializer.data[0]['access_key'],"secret_key":serializer.data[0]['secret_key'],"name":channel.name,"website_name":channel.website_name,"id":channel.id}
					amazon_credential = {"merchant_id":serializer.data[0]['merchant_id'],"access_key":serializer.data[0]['access_key'],"secret_key":serializer.data[0]['secret_key'],"name":channel.name,"website_name":channel.website_name,"id":channel.id}
					channel_credential_arr.append(amazon_credential)

			response = {"status":1,"credentials":channel_credential_arr,"message":"Data Found"}

		elif channel_id == '1':
			#print("---1")
			all_channel = EngageboostChannels.objects.using(company_db).all().filter(parent_id=channel_id,isdeleted='n',isblocked='n')
			for channel in all_channel:
				empty_data={}
				ebay_credential = EngageboostChannelUsers.objects.using(company_db).all().filter(channel_id=channel.id,parent_id=channel_id,company_website_id=website_id,isdeleted='n',isblocked='n')
				ebay_ch_serializer = ChannelUsersSerializer(ebay_credential, many=True)
				if ebay_credential.exists():
					ebay_ch_serializer.data[0]['id'] = channel.id		
					ebay_ch_serializer.data[0]['website_name'] = channel.website_name
					ebay_ch_serializer.data[0]['name'] = channel.name			
					channel_credential_arr.append(ebay_ch_serializer.data[0])
				else:
					empty_data['id'] = channel.id
					empty_data['website_name'] = channel.website_name
					empty_data['name'] = channel.name	
					empty_data['parent_id'] = channel_id		
					channel_credential_arr.append(empty_data)
			
			if channel_credential_arr:
				response = {"status":1,"credentials":channel_credential_arr,"message":"Data Found"}
			else:
				response = {"status":0,"credentials":[],"message":"No Data Found"}

		else: # 20 this is for Flipkart # 23 this is for Paytm # 21 this is for Snapdeal 
			#print("---2")
			empty_data={}
			flipkart_credential = EngageboostChannelUsers.objects.using(company_db).filter(parent_id=channel_id,company_website_id=website_id,isdeleted='n',isblocked='n').first()
			serializer = ChannelUsersSerializer(flipkart_credential, partial=True)
			#if flipkart_credential.exists():
			if serializer.data['parent_id'] is None:
				empty_data['id'] = channel_id
				empty_data['parent_id'] = channel_id
				channel_credential_arr.append(empty_data)
				# response = {"status":0,"credentials":[],"message":"No Data Found"}
			else:
				empty_data = serializer.data
				empty_data['id'] = channel_id
				channel_credential_arr.append(empty_data)			
				# response = {"status":1,"credentials":channel_credential_arr,"message":"Data Found"}	

			if channel_credential_arr:
				response = {"status":1,"credentials":channel_credential_arr,"message":"Data Found"}
			else:
				response = {"status":0,"credentials":[],"message":"No Data Found"}

		return Response(response)

class AmazonCredentialSave(generics.ListAPIView):
	def post(self,request,format=None):
		company_db = loginview.db_active_connection(request)
		data_string = request.data
		# datajson = json.loads(data_string)
		d1={"created_on":datetime.date.today(),"isdeleted":'n',"default_category":0,"channel_site_ids":"0","merchant_identifier":"0"}
		serializer_data=dict(data_string,**d1)	
		serializer = AmazonCredentialsSerializer(data=serializer_data,partial=True)

		count = EngageboostAmazonCredentials.objects.using(company_db).filter(channel_id=serializer_data['channel_id'],channel_parrent_id=serializer_data['channel_parrent_id'],company_website_id=serializer_data['company_website_id'],company_id=serializer_data['company_id'],isdeleted='n').count()
		if count == 0:
			if serializer.is_valid():
				serializer.save()
				data={'status':1,'message':'Successfully Inserted'}
			else:
				data={'status':0,'api_status':serializer.errors,'message':'Error Occured'}
			return Response(data)
		else:
			credential_details = EngageboostAmazonCredentials.objects.using(company_db).filter(channel_id=serializer_data['channel_id'],channel_parrent_id=serializer_data['channel_parrent_id'],company_website_id=serializer_data['company_website_id'],company_id=serializer_data['company_id'],isdeleted='n').first()
			credential_details_serializer = AmazonCredentialsSerializer(credential_details)
			pk = credential_details_serializer.data['id']
			#print(pk)
			row_id = EngageboostAmazonCredentials.objects.using(company_db).get(pk=pk)
			serializer = AmazonCredentialsSerializer(row_id,data=serializer_data,partial=True)
			if serializer.is_valid():
				serializer.save()
				data={'status':1,'message':'Successfully Updated'}
			else:
				data={'status':0,'api_status':serializer.errors,'message':'Error Occured'}
			
			return Response(data)

class FlipkartCredentialSave(generics.ListAPIView):
	def post(self,request,format=None):
		company_db = loginview.db_active_connection(request)
		data_string = request.data
		username = data_string['username']
		password = data_string['password']
		user_auth = str(base64.b64encode(str(username+':'+password).encode('utf-8')).decode("utf-8"))
		# response = requests.get("curl -u bb2133755068ba156857561151a069557059:1a31c4a90e2e415b2eee9460f4c60b85e https://api.flipkart.net/oauth-service/oauth/token\?grant_type\=client_credentials\&scope=Seller_Api")
		
		count = EngageboostChannelUsers.objects.using(company_db).filter(parent_id=data_string['parent_id'],company_website_id=data_string['company_website_id'],company_id=data_string['company_id'],isdeleted='n',isblocked='n').count()
		
		if count == 0:
			# url = "https://api.flipkart.net/oauth-service/oauth/token"
			# querystring = {"grant_type":"client_credentials","scope":"Seller_Api"}
			# headers = {
			#     'Authorization': "Basic "+user_auth,
			#     'Cache-Control': "no-cache",
			#     'Postman-Token': "627d7688-db65-4375-a42c-3ff241f383f9"
			#     }
			# response = requests.request("GET", url, headers=headers, params=querystring)
			# access_token = response.json()['access_token']
			# expires_in = response.json()['expires_in']
			# token_type = response.json()['token_type']
			access_token = '81150be0-9d95-4d23-9fd6-a07ecea816b6'
			expires_in = '4121907'
			token_type = 'bearer'

			last_entry_of_table = EngageboostChannelUsers.objects.using(company_db).last()
			row_id = int(last_entry_of_table.id)+int(1)
			current_date = datetime.date.today()
			filpkart_credential = EngageboostChannelUsers.objects.using(company_db).create(id=row_id,channel_id=data_string['channel_id'],parent_id=data_string['parent_id'],channel_site_ids=data_string['channel_id'],username=username,password=password,token=access_token,token_expired=current_date,tokentype=token_type,fullfilment_by=data_string['fullfilment_by'],refreshtoken='',company_website_id=data_string['company_website_id'],company_id=data_string['company_id'],default_ebay_category=0,created=current_date,modified=current_date)
			last_inserted_id = filpkart_credential.id
			data ={'status':1,'api_status':last_inserted_id,'message':'Successfully Inserted'}
			
			return Response(data)
		else:
			# url = "https://api.flipkart.net/oauth-service/oauth/token"
			# querystring = {"grant_type":"client_credentials","scope":"Seller_Api"}
			# headers = {
			#     'Authorization': "Basic "+user_auth,
			#     'Cache-Control': "no-cache",
			#     'Postman-Token': "627d7688-db65-4375-a42c-3ff241f383f9"
			#     }
			# response = requests.request("GET", url, headers=headers, params=querystring)
			# access_token = response.json()['access_token']
			# expires_in = response.json()['expires_in']
			# token_type = response.json()['token_type']
			access_token = '81150be0-9d95-4d23-9fd6-a07ecea816b6'
			expires_in = '4121907'
			token_type = 'bearer'

			credential_details = EngageboostChannelUsers.objects.using(company_db).filter(parent_id=data_string['parent_id'],company_website_id=data_string['company_website_id'],company_id=data_string['company_id'],isdeleted='n',isblocked='n').first()
			credential_details_serializer = ChannelUsersSerializer(credential_details)
			pk = credential_details_serializer.data['id']

			row_id = EngageboostChannelUsers.objects.using(company_db).get(pk=pk)
			serializer_data = {"channel_id":data_string['channel_id'],"parent_id":data_string['parent_id'],"channel_site_ids":data_string['channel_id'],"username":username,"password":password,"token":access_token,"token_expired":datetime.datetime.now(),"tokentype":token_type,"fullfilment_by":data_string['fullfilment_by'],"refreshtoken":'',"company_website_id":data_string['company_website_id'],"company_id":data_string['company_id'],"default_ebay_category":0,"modified":datetime.date.today()}
			serializer = ChannelUsersSerializer(row_id,data=serializer_data,partial=True)
			if serializer.is_valid():
				serializer.save()
				data={'status':1,'message':'Successfully Updated'}
			else:
				data={'status':0,'api_status':serializer.errors,'message':'Error Occured'}
			
			return Response(data)
		
class EbayCredentialSave(generics.ListAPIView):
	def post(self,request,format=None):
		company_db = loginview.db_active_connection(request)
		data_string = request.data
		username = data_string['username']
		
		count = EngageboostChannelUsers.objects.using(company_db).filter(channel_id=data_string['channel_id'],parent_id=data_string['parent_id'],company_website_id=data_string['company_website_id'],company_id=data_string['company_id'],isdeleted='n',isblocked='n').count()
		
		if count == 0:
			# url = "https://api.flipkart.net/oauth-service/oauth/token"
			# querystring = {"grant_type":"client_credentials","scope":"Seller_Api"}
			# headers = {
			#     'Authorization': "Basic "+user_auth,
			#     'Cache-Control': "no-cache",
			#     'Postman-Token': "627d7688-db65-4375-a42c-3ff241f383f9"
			#     }
			# response = requests.request("GET", url, headers=headers, params=querystring)
			# access_token = response.json()['access_token']
			# expires_in = response.json()['expires_in']
			# token_type = response.json()['token_type']
			access_token = 'ebay-H78yi-81150be0'
			expires_in = '4121907'
			token_type = 'bearer'

			last_entry_of_table = EngageboostChannelUsers.objects.order_by('-id').latest('id')
			row_id = int(last_entry_of_table.id)+int(1)
			current_date = datetime.date.today()
			filpkart_credential = EngageboostChannelUsers.objects.using(company_db).create(id=row_id,channel_id=data_string['channel_id'],parent_id=data_string['parent_id'],channel_site_ids=data_string['channel_id'],username=username,password="xxx",token=access_token,token_expired=current_date,tokentype=token_type,fullfilment_by='standard',refreshtoken='',company_website_id=data_string['company_website_id'],company_id=data_string['company_id'],default_ebay_category=0,created=current_date,modified=current_date)
			last_inserted_id = filpkart_credential.id
			data ={'status':1,'api_status':last_inserted_id,'message':'Successfully Inserted'}
			
			return Response(data)
		else:
			# url = "https://api.flipkart.net/oauth-service/oauth/token"
			# querystring = {"grant_type":"client_credentials","scope":"Seller_Api"}
			# headers = {
			#     'Authorization': "Basic "+user_auth,
			#     'Cache-Control': "no-cache",
			#     'Postman-Token': "627d7688-db65-4375-a42c-3ff241f383f9"
			#     }
			# response = requests.request("GET", url, headers=headers, params=querystring)
			# access_token = response.json()['access_token']
			# expires_in = response.json()['expires_in']
			# token_type = response.json()['token_type']
			access_token = 'ebay-H78yi-81150be0'
			expires_in = '4121907'
			token_type = 'bearer'

			credential_details = EngageboostChannelUsers.objects.using(company_db).filter(channel_id=data_string['channel_id'],parent_id=data_string['parent_id'],company_website_id=data_string['company_website_id'],company_id=data_string['company_id'],isdeleted='n',isblocked='n').first()
			credential_details_serializer = ChannelUsersSerializer(credential_details)
			pk = credential_details_serializer.data['id']

			row_id = EngageboostChannelUsers.objects.using(company_db).get(pk=pk)
			serializer_data = {"channel_id":data_string['channel_id'],"parent_id":data_string['parent_id'],"channel_site_ids":data_string['channel_id'],"username":username,"password":"xxx","token":access_token,"token_expired":datetime.datetime.now(),"tokentype":token_type,"fullfilment_by":'standard',"refreshtoken":'',"company_website_id":data_string['company_website_id'],"company_id":data_string['company_id'],"default_ebay_category":0,"modified":datetime.date.today()}
			serializer = ChannelUsersSerializer(row_id,data=serializer_data,partial=True)
			if serializer.is_valid():
				serializer.save()
				data={'status':1,'message':'Successfully Updated'}
			else:
				data={'status':0,'api_status':serializer.errors,'message':'Error Occured'}
			
			return Response(data)

class SnapdealCredentialSave(generics.ListAPIView):
	def post(self,request,format=None):
		company_db = loginview.db_active_connection(request)
		data_string = request.data	
		current_date = datetime.date.today()			

		count = EngageboostChannelUsers.objects.using(company_db).filter(channel_id=data_string['channel_id'],parent_id=data_string['parent_id'],company_website_id=data_string['company_website_id'],company_id=data_string['company_id'],isdeleted='n',isblocked='n').count()
		
		if count == 0:
			token_type = 'bearer'

			last_entry_of_table = EngageboostChannelUsers.objects.order_by('-id').latest('id')
			row_id = int(last_entry_of_table.id)+int(1)
			
			# d1={"channel_site_ids":data_string['channel_id'],"password":"n/a","token":"n/a","token_expired":datetime.datetime.now(),"tokentype":token_type,"fullfilment_by":'standard',"default_ebay_category":0,"created":current_date,"modified":current_date}
			# serializer_data=dict(data_string,**d1)	
			# serializer = ChannelUsersSerializer(data=serializer_data,partial=True)

			snapdeal_credential = EngageboostChannelUsers.objects.using(company_db).create(id=row_id,name=data_string['name'],username=data_string['username'],refreshtoken=data_string['refreshtoken'],channel_id=data_string['channel_id'],parent_id=data_string['parent_id'],company_website_id=data_string['company_website_id'],company_id=data_string['company_id'],channel_site_ids=data_string['channel_id'],password="n/a",token="n/a",token_expired=current_date,tokentype=token_type,fullfilment_by="standard",default_ebay_category=0,created=current_date,modified=current_date)

			last_inserted_id = snapdeal_credential.id
			data ={'status':1,'api_status':last_inserted_id,'message':'Successfully Inserted'}
			# data={'status':1,'message':row_id}
			return Response(data)
		else:
			token_type = 'bearer'

			credential_details = EngageboostChannelUsers.objects.using(company_db).filter(channel_id=data_string['channel_id'],parent_id=data_string['parent_id'],company_website_id=data_string['company_website_id'],company_id=data_string['company_id'],isdeleted='n',isblocked='n').first()
			credential_details_serializer = ChannelUsersSerializer(credential_details)
			pk = credential_details_serializer.data['id']
			row_id = EngageboostChannelUsers.objects.using(company_db).get(pk=pk)

			d1={"channel_site_ids":data_string['channel_id'],"password":"n/a","token":"n/a","token_expired":datetime.datetime.now(),"tokentype":token_type,"fullfilment_by":'standard',"default_ebay_category":0,"modified":current_date}
			serializer_data=dict(data_string,**d1)	

			serializer = ChannelUsersSerializer(row_id,data=serializer_data,partial=True)
			if serializer.is_valid():
				serializer.save()
				data={'status':1,'message':'Successfully Updated'}
			else:
				data={'status':0,'api_status':serializer.errors,'message':'Error Occured'}
			
			return Response(data) 

class ActiveDeactiveChannel(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		data_string = request.data
		parent_id = data_string['parent_id']
		website_id = data_string['website_id']
		is_active = data_string['is_active']
		datas=[]

		if is_active == 0: ### For deactivate
			website_channels = EngageboostChannels.objects.using(company_db).all().filter(isdeleted='n',isblocked='n',parent_id=parent_id).order_by('order_id')

			for website_channel in website_channels:
				channel_id = website_channel.id
				if channel_id == 7:
					data={"status":0}
				else:
					EngageboostWebsiteChannels.objects.using(company_db).filter(engageboost_channel_id=channel_id).delete()
					EngageboostChannelSettings.objects.using(company_db).filter(channel_site_id=channel_id,company_website_id=website_id).delete()
					data={"status":1}

			EngageboostChannelUsers.objects.using(company_db).filter(company_website_id=website_id,parent_id=parent_id).delete()
			return Response(data)
		else:
			website_channels = EngageboostChannels.objects.using(company_db).all().filter(isdeleted='n',isblocked='n',parent_id=parent_id).order_by('order_id')
			for website_channel in website_channels:
				channel_id = website_channel.id
				country_id = website_channel.country_id
				currency_id = 0
				currency_cond = EngageboostCurrencyMasters.objects.using(company_db).all().filter(engageboost_country_id=country_id,isblocked='n',isdeleted='n')
				#currency_idarr = CurrencyMastersSerializer(currency_cond,partial=True)
				# print(currency_cond.id)
				if currency_cond.exists():
					currency_id = currency_cond[0].id
				else:
					currency_id = 0	

				# if channel_id is not None:
				channel_data={}
				
				
				website_chnlcount = EngageboostWebsiteChannels.objects.using(company_db).filter(engageboost_channel_id=channel_id,engageboost_company_website_id=website_id).count()
				if website_chnlcount>0:
					website_chnl_cond = EngageboostWebsiteChannels.objects.using(company_db).filter(engageboost_channel_id=channel_id,engageboost_company_website_id=website_id).first()
					website_chnl = WebsiteChannelsSerializer(website_chnl_cond)

					if website_chnl.data['id'] is not None:
						channel_data={"engageboost_channel_id":channel_id,"engageboost_company_website_id":website_id,"currency_id":currency_id,"isblocked":"n","isdeleted":"n"}
						serializer = WebsiteChannelsSerializer(website_chnl.data['id'],data=channel_data,partial=True)
						if serializer.is_valid():
							serializer.save()
							website_chnl_data={'status':1,'message':'Successfully Updated'}
						else:
							website_chnl_data={'status':0,'api_status':serializer.errors,'message':'Error Occured'}
				else:
					last_entry_of_table = EngageboostWebsiteChannels.objects.order_by('-id').latest('id')
					row_id = int(last_entry_of_table.id)+int(1)

					activate_action = EngageboostWebsiteChannels.objects.using(company_db).create(id=row_id,engageboost_channel_id=channel_id,engageboost_company_website_id=website_id,currency_id=currency_id,isblocked="n",isdeleted="n")

					last_inserted_id = activate_action.id
					website_chnl_data ={'status':1,'api_status':last_inserted_id,'message':'Successfully Inserted'}

					# if serializer.is_valid():
					# 	serializer.save()
					# 	website_chnl_data={'status':1,'message':'Successfully Inserted'}
					# else:
					# 	website_chnl_data={'status':0,'api_status':serializer.errors,'message':'Error Occured'}
				
				# data={"channel_id":channel_id,"country_id":country_id,"currency_id":currency_id}
				# datas.append(website_chnl_data)


			channel_id_arr=[]
			d2=[]
			website_channel = EngageboostWebsiteChannels.objects.using(company_db).all().filter(engageboost_company_website_id=website_id,isdeleted="n",isblocked="n").order_by('id')
			for channel_list in website_channel:
				channel_id_arr.append(channel_list.engageboost_channel_id)

			all_channel = EngageboostChannels.objects.using(company_db).all().filter(~Q(id='6'),~Q(parent_id='0'),isdeleted='n',isblocked='n').distinct('parent_id')
			for channel in all_channel:
				#print(str(channel.parent_id)+' '+str(channel.id))
				parent_id = (channel.parent_id)

				if channel.id in channel_id_arr:
					d2.append({"name":channel.parent_name,"parent_id":channel.parent_id,"channel_id":channel.id,"parent_logo":channel.parent_logo,"description":channel.description,"status":1})
				else:
					d2.append({"name":channel.parent_name,"parent_id":channel.parent_id,"channel_id":channel.id,"parent_logo":channel.parent_logo,"description":channel.description,"status":0})
			data ={
				'status':1,
				'channels':d2,
				}
			
			return Response(data)

class Channelusers(generics.ListAPIView):
# """ Add New Brand """
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		d1={'created':datetime.date.today(),'modified':datetime.date.today()}
		d2=request.data
		serializer_data=dict(d2,**d1)
		serializer = ChannelUsersSerializer(data=serializer_data,partial=True)
		if serializer.is_valid():
			serializer.save()
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
class ChannelusersList(generics.ListAPIView):
# """ List all Edit,Uodate Brand """
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostChannelUsers.objects.using(company_db).get(pk=pk)
		except EngageboostChannelUsers.DoesNotExist:
			raise Http404

	def get(self, request, pk,company_website_id, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		user = self.get_object(pk,request)
		serializer = ChannelUsersSerializer(user)
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
	
	def put(self, request, pk,company_website_id, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		Category = self.get_object(pk,request)
		d1={'modified':datetime.date.today()}
		d2=request.data
		serializer_data=dict(d2,**d1)
		serializer = ChannelUsersSerializer(Category,data=serializer_data,partial=True)
		if serializer.is_valid():
			serializer.save()
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

def ImageResize(image,width_origenal,height_origenal,imageresizeon,cover_image):	
	if imageresizeon.image_resize =='Width':
		if width_origenal >250:
			ratio = width_origenal/height_origenal
			width=250
			height=int(250*height_origenal/width_origenal)
		else:
			width=width_origenal
			height=height_origenal



	if imageresizeon.image_resize =='Height':
		if height_origenal >185:
			ratio = height_origenal/width_origenal
			width=int(185*width_origenal/height_origenal)
			height=185
		else:
			width=width_origenal
			height=height_origenal
	img_anti = image.resize((width, height), Image.ANTIALIAS)
	new_image_file = settings.MEDIA_ROOT+'/companylogo/250x185/'+cover_image
	img_anti.save(cover_image)

def amazons3_fileupload250(file_name,companywebsitedetails):
	conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)
	#print(file_name)
	f200 = open(settings.MEDIA_ROOT+'/companylogo/250x185/'+file_name,'rb')
	#conn.upload(companywebsitedetails['company_name']+'/'+companywebsitedetails['s3folder_name']+'/companylogo/250x185/'+file_name,f200,'boostmysale')
	conn.upload(settings.AMAZON_S3_FOLDER+'/companylogo/250x185/'+file_name,f200,settings.AMAZON_S3_BUCKET)
	if os.path.exists(settings.BASE_DIR+'/companylogo/250x185/'+file_name):
			os.unlink(settings.BASE_DIR+'/companylogo/250x185/'+file_name)
	return 0

class WebstoreImageDelete(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		
		field=request.data['field']
		file_name=request.data['file_name']
		website_id=request.data['id']

		# company_cond = EngageboostCompanyWebsites.objects.using(company_db).get(id=website_id) 
		# companywebsitedetails = CompanyWebsiteSerializer(company_cond, partial=True)
		# AMAZON_S3_FOLDER = str(companywebsitedetails['company_name'])+'/'+str(companywebsitedetails['s3folder_name'])


		value=''
		query = {field : value}
		# conn = tinys3.Connection('AKIAJV3766IH6NOYUKRA','qBkJW2ZhnD8gR0Lq99YKoEn6yEvq+W8y4W2Zhjvm',tls=True)
		# if(field=='website_logo'):
		# 	conn.delete('companylogo/250x185/'+file_name,AMAZON_S3_FOLDER)
		# elif(field=='id_proof'):
		# 	conn.delete('id_proof/'+file_name,AMAZON_S3_FOLDER)
		# elif(field=='address_proof'):	
		# 	conn.delete('address_proof/'+file_name,AMAZON_S3_FOLDER)
		# else:
		# 	conn.delete('other_document/'+file_name,AMAZON_S3_FOLDER)

		EngageboostCompanyWebsites.objects.using(company_db).filter(id=website_id).update(**query)
		data ={
				'status':1,
				'message':'Successfully Deleted',
				}

		return Response(data)

class ShippingMethodStatus(generics.ListAPIView):
	def get(self, request,website_id, shipping_method_id, format=None):
		try:
			# post_data = request.data

			# website_id = post_data['website_id']
			# shipping_method_id = post_data['shipping_method_id']

			# settingsObj = EngageboostShippingMastersSettings.objects.filter(website_id=website_id,shipping_method_id=shipping_method_id,status='yes',isblocked='n',isdeleted='n')

			settingsObj = EngageboostShippingMastersSettings.objects.filter(website_id=website_id,shipping_method_id=shipping_method_id,status='yes')

			if settingsObj.count()>0:
				# settingsObj = settingsObj
				data ={
					'status':1,
					'api_status':'',
					'Message':'Shipping method enabled',
				}
			else:
				data ={
					'status':0,
					'api_status':'',
					'Message':'Shipping method disabled',
				}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}			
		return Response(data)
	def post(self, request, format=None):
		try:
			post_data = request.data

			website_id = post_data['website_id']
			shipping_method_id = post_data['shipping_method_id']
			status = post_data['status']

			shipping_status = 'yes'
			if status==1:
				shipping_status = 'yes'
			else:
				shipping_status = 'no'	

			settingsObj = EngageboostShippingMastersSettings.objects.filter(website_id=website_id,shipping_method_id=shipping_method_id).update(status=shipping_status)
			data ={
				'status':1,
				'api_status':'',
				'Message':'success',
			}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}			
		return Response(data)


class StoreTypeAdd(generics.ListAPIView):
	def get(self, request, pk, format=None):
		try:
			store_type_obj = EngageboostTemplateIndustryMasters.objects.get(id=pk)
			serializer = TemplateIndustryMastersSerializer(store_type_obj)
			if serializer:
				data = {
					'data': serializer.data,
					'status': 1,
					'api_status': '',
					'Message': 'success',
				}
			else:
				data = {
					'status': 0,
					'api_status': '',
					'Message': 'data not found',
				}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data = {"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),
					"message": str(error)}
		return Response(data)

	def post(self, request, format=None):
		try:
			requestdata = request.data

			# print(requestdata['fileUrl'])
			name = requestdata['store_name']
			image = requestdata['storecategory_logo']
			order = requestdata['sequence_number']
			storeCategoryId = requestdata['storeCategoryId']

			store_type_categories_selected = map(str, requestdata['store_type_categories_selected'])

			website_id = requestdata['website_id']
			created = datetime.datetime.now(datetime.timezone.utc).astimezone()
			modified = datetime.datetime.now(datetime.timezone.utc).astimezone()
			createdby = request.user.id
			modifiedby = request.user.id

			# if int(storeCategoryId) <= 0:
			# 	store_type_obj = EngageboostTemplateIndustryMasters.objects.create(name=name, image=image, website_id=website_id, created=created, modified=modified, createdby=createdby, order=order)
			# else:
			# 	store_type_obj = EngageboostTemplateIndustryMasters.objects.filter(id=storeCategoryId).update(name=name, image=image, website_id=website_id, created=created, modified=modified, modifiedby=modifiedby, order=order)

			str1 = ","
			store_type_categories_selected = str1.join(store_type_categories_selected)
			# print('parent_category_ids=====>', store_type_categories_selected)
			# print('store_type_categories_selected=====>', store_type_categories_selected)

			if int(storeCategoryId) <= 0:
				store_type_obj = EngageboostTemplateIndustryMasters.objects.create(name=name, image=image,
																				   website_id=website_id,
																				   created=created, modified=modified,
																				   createdby=createdby, order=order,
																				   store_type_categories_selected=store_type_categories_selected)
			else:
				store_type_obj = EngageboostTemplateIndustryMasters.objects.filter(id=storeCategoryId).update(name=name,
																											  image=image,
																											  website_id=website_id,
																											  created=created,
																											  modified=modified,
																											  modifiedby=modifiedby,
																											  order=order,
																											  store_type_categories_selected=store_type_categories_selected)

			data = {
				'status': 1,
				'api_status': '',
				'Message': 'success',
			}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
		return Response(data)


@permission_classes([])
class StoreTypeAll(generics.ListAPIView):
	def get(self, request, format=None):
		try:
			store_type_obj = EngageboostTemplateIndustryMasters.objects.filter(isblocked='n', isdeleted='n', website_id=1)
			serializer = TemplateIndustryMastersSerializer(store_type_obj, many=True)
			if serializer:
				data = {
					'data': serializer.data,
					'status': 1,
					'api_status': '',
					'Message': 'success',
				}
			else:
				data = {
					'status': 0,
					'api_status': '',
					'Message': 'data not found',
				}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data = {"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),
					"message": str(error)}
		return Response(data)


class CategoryAll(generics.ListAPIView):
	def get(self, request, format=None):
		try:
			cat_obj = EngageboostCategoryMasters.objects.filter(isblocked='n', isdeleted='n', website_id=1)
			serializer = CategoryMastersSerializer(cat_obj, many=True)
			if serializer:
				data = {
					'data': serializer.data,
					'status': 1,
					'api_status': '',
					'Message': 'success',
				}
			else:
				data = {
					'status': 0,
					'api_status': '',
					'Message': 'data not found',
				}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data = {"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),
					"message": str(error)}
		return Response(data)

class PaymentMethodList(APIView):
	def get(self, request, format=None):
		user = request.user
		user_id = user.id
		device_id = request.META.get('HTTP_DEVICEID')
		# website_id = common_functions.get_company_website_id_by_url()
		final_data = []
		# paymenttypes = EngageboostPaymentgatewayTypes.objects.all().filter(isdeleted='n',isblocked='n').order_by('order_by')
		# menulist = PaymentMethodListSerializer(paymenttypes, many=True)
		ind = 0
		rs_web_pay_method = EngageboostWebsitePaymentmethods.objects.filter(isblocked='n', isdeleted='n').distinct(
			'engageboost_paymentgateway_method_id').all()
		rs_data = WebsitePaymentmethodsViewSerializer(rs_web_pay_method, many=True).data
		data = {

			'api_status': rs_data,
		}
		return Response(data)


class GetStoreTypeCategories(generics.ListAPIView):
    def post(self, request, format=None):
        try:
            requestdata = request.data
            store_type_ids = requestdata['store_type_ids']
            category_list = []
            categories_list_level_0 = []
            stores_category_list = EngageboostTemplateIndustryMasters.objects.filter(id__in=store_type_ids).values_list('store_type_categories_selected', flat=True)
            for store_category in stores_category_list:
                # print('store_category===>', store_category)
                if store_category:
                    arr_1 = store_category.replace(' ','')
                    arr_1 = arr_1.split(',')
                    categories_list_level_0.extend(arr_1)
                    # print('arr_1====>',arr_1)
            categories_list_level_1 = EngageboostCategoryMasters.objects.filter(parent_id__in=set(categories_list_level_0)).values_list('id', flat=True)
            categories_list_level_2 = EngageboostCategoryMasters.objects.filter(parent_id__in=set(categories_list_level_1)).values_list('id', flat=True)

            category_list.extend(categories_list_level_0)
            category_list.extend(categories_list_level_1)
            category_list.extend(categories_list_level_2)
            category_list = list(set(category_list))

            cat_obj = EngageboostCategoryMasters.objects.filter(id__in=category_list, isblocked='n', isdeleted='n', website_id=1)
            serializer = CategoryMastersSerializer(cat_obj, many=True)

            # category_data = EngageboostCategoryMasters.objects.filter(id__in=category_list)
            # serializer = CategoryMastersSerializer(category_data, partial=True)
            # print("store_type_ids======>", store_type_ids)

            if serializer:
                data = {
                    'data': serializer.data,
                    'status': 1,
                    'api_status': 1,
                    'Message': 'success',
                }
            else:
                data = {
                    'status': 0,
                    'api_status': 0,
                    'Message': 'data not found',
                }

            # data = {
            # 	'data': {
            # 		"category_list": serializer.data
            # 	},
            # 	'status': 1,
            # 	'api_status': '',
            # 	'Message': 'success',
            # }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status": 0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),
                    "message": str(error)}
        return Response(data)