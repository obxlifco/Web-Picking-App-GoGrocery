from webservices.models import *
from django.apps import apps
from django.http import Http404
from django.http import JsonResponse
import sys
import traceback
import json
from django.db.models import * 
from webservices.serializers import *
from rest_framework.views import APIView
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpRequest
from rest_framework.parsers import JSONParser
from datetime import datetime
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django import views
from rest_framework import pagination
import math
import requests
from django.template import RequestContext
from django.utils import timezone
from webservices.views import loginview
from django.views.generic import View

class AutoComplete(generics.ListAPIView):
	def post(self, request, format=None):

		company_db = loginview.db_active_connection(request)
		try:
			table_name=request.data['table_name']
			company_id=request.data['company_id']
			website_id=request.data['website_id']
			model=apps.get_model('webservices',table_name)
			serializer_class = get_serializer_class(self,table_name)
			
			key=request.data['search']
				
			result = model.objects.using(company_db).all().filter(get_search_filter(self,table_name,key))
			if table_name=='EngageboostGroups':	
				result=result.filter(isdeleted='n',isblocked='n',company_id=company_id)
			if table_name=='EngageboostRolemasters':	
				result=result.filter(isdeleted='n',isblocked='n',company_id=company_id)
			if table_name=='EngageboostCountries':	
				result=result
			else:	
				result=result.filter(isdeleted='n',isblocked='n',website_id=website_id)
			

			result = result[:20]	
			serializer = serializer_class(result, many=True)	
			data = {
			'filter_data':serializer.data,
			
			}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data1={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error), 'message': str(error)}   	
			print(data1)
			data = {
			'filter_data':[],
			
			}
		return JsonResponse(data)

class AutoCompleteFrontend(View):
	def post(self, request, format=None):

		company_db = loginview.db_active_connection(request)
		data = JSONParser().parse(request)
		table_name=data['table_name']
		model=apps.get_model('webservices',table_name)
		serializer_class = get_serializer_class(self,table_name)
		
		key=data['search']
				
		result = model.objects.using(company_db).all().filter(get_search_filter(self,table_name,key))[:20]
		serializer = serializer_class(result, many=True)	
		data = {
		'filter_data':serializer.data,
		
		}
		return JsonResponse(data)

def get_serializer_class(self,table_name):
	if table_name=='EngageboostUsers':
		return UserSerializer
	elif table_name=='EngageboostGroups':
		return GroupSerializer
	elif table_name=='EngageboostRolemasters':
		return RoleSerializer
	elif table_name=='EngageboostCategoryMasters':
		return CategoriesSerializer 
	elif table_name=='EngageboostBrandMasters':
		return BrandSerializer 
	elif table_name=='EngageboostProductReviews':
		return ReviewSerializer 
	elif table_name=='EngageboostProductCategories':
		return BasicinfometaSerializer 
	elif table_name=='EngageboostDiscountMasters':
		return DiscountMasterSerializer
	elif table_name=='EngageboostEmktContactlists':
		return EmktContactlistsSerializer   
	elif table_name=='EngageboostEmktContacts':
		return ContactsSerializer 
	elif table_name=='EngageboostEmktSegments':
		return SegmentsSerializer 
	elif table_name=='EngageboostProducts':       
		return BasicinfoSerializer
	elif table_name=='EngageboostCustomers':
		return CustomerSerializer
	elif table_name=='EngageboostProductStocks':
		return StockSerializer
	elif table_name=='EngageboostPurchaseOrders':
		return PurchaseordersSerializer
	elif table_name=='EngageboostSuppliers':
		return SuppliersSerializer
	elif table_name=='EngageboostWarehouseMasters':
		return WarehousemastersSerializer
	elif table_name=='EngageboostPurchaseOrdersPaymentMethods':
		return PurchaseOrdersPaymentMethodsSerializer
	elif table_name=='EngageboostPurchaseOrdersShippingMethods':
		return PurchaseOrdersShippingMethodSerializer
	elif table_name=='EngageboostPresets':
		return PresetsSerializer
	elif table_name=='EngageboostOrdermaster':
		return OrderMasterSerializer
	elif table_name=='EngageboostShipments':
		return ShipmentsSerializer
	elif table_name=='EngageboostGlobalSettings':
		return GlobalsettingsSerializer
	elif table_name=='EngageboostUnitMasters':
		return UnitmasterSerializer
	elif table_name=='EngageboostCurrencyMasters':
		return CurrencyMastersSerializer
	elif table_name=='EngageboostApplicableAutoresponders':
		return ApplicableAutorespondersSerializer
	elif table_name=='EngageboostShippingMasters':
		return ShippingSerializer
	elif table_name=='EngageboostEmailTypeContents':
		return EmailTypeContentsSerializer
	elif table_name=='EngageboostCompanyWebsites':
		return CompanyWebsiteSerializer
	elif table_name=='EngageboostCurrencyRates':
		return BaseCurrencyratesetSerializer  
	elif table_name=='EngageboostCustomerGroup':
		return CustomerGroupSerializer
	elif table_name=='EngageboostCountries':
		return GlobalsettingscountriesSerializer      


def get_search_filter(self,table_name,key):
	if table_name=='EngageboostUsers':
		return (Q(role__name__icontains=key)|Q(first_name__icontains=key)|Q(last_name__icontains=key)|Q(email__icontains=key)|Q(business_name__icontains=key)|Q(employee_name__icontains=key)|Q(designation__icontains=key)|Q(city__icontains=key)|Q(state__icontains=key)|Q(postcode__icontains=key)|Q(phone__icontains=key))
	elif table_name=='EngageboostGroups':
		return (Q(name__icontains=key))
	elif table_name=='EngageboostRolemasters':
		return (Q(name__icontains=key))
	elif table_name=='EngageboostCategoryMasters':
		return (Q(name__icontains=key))    
	elif table_name=='EngageboostBrandMasters':
		return (Q(name__icontains=key)) 
	elif table_name=='EngageboostProducts':       
		return (Q(name__icontains=key)|Q(sku__icontains=key)|Q(description__icontains=key)|Q(brand__icontains=key)) 
	elif table_name=='EngageboostProductReviews':
		return (Q(name__icontains=key))
	elif table_name=='EngageboostProductCategories':
		return (Q(name__icontains=key)) 
	elif table_name=='EngageboostDiscountMasters':
		return (Q(name__icontains=key)|Q(description__icontains=key)|Q(amount__icontains=key))     
	elif table_name=='EngageboostEmktContactlists':
		return (Q(name__icontains=key))
	elif table_name=='EngageboostEmktContacts':
		return (Q(title__icontains=key)|Q(user_name__icontains=key)|Q(list_name__icontains=key))  
	elif table_name=='EngageboostEmktSegmentContactlists':
		return (Q(title__icontains=key)|Q(user_name__icontains=key)|Q(list_name__icontains=key))       
	elif table_name=='EngageboostDiscountMasters':
		return (Q(name__icontains=key)|Q(description__icontains=key)|Q(amount__icontains=key))        
	elif table_name=='EngageboostCustomers':
		return (Q(first_name__icontains=key)|Q(last_name__icontains=key)|Q(email__icontains=key)|Q(city__icontains=key)|Q(state__icontains=key)|Q(post_code__icontains=key)|Q(phone__icontains=key))
	elif table_name=='EngageboostOrdermaster':
		return (Q(custom_order_id__icontains=key)|Q(payment_method_name__icontains=key)|Q(delivery_email_address__icontains=key))
	elif table_name=='EngageboostShipments':
		return (Q(custom_shipment_id__icontains=key)|Q(shipment_status__icontains=key))
	elif table_name=='EngageboostPresets':
		return (Q(name__icontains=key))
	elif table_name=='EngageboostGlobalSettings':
		return (Q(name__icontains=key)|Q(date_format__icontains=key)|Q(itemlisting_backend__icontains=key)|Q(itemlisting_front__icontains=key))
	elif table_name=='EngageboostPurchaseOrdersPaymentMethods':
		return (Q(name__icontains=key)) 
	elif table_name=='EngageboostPurchaseOrdersShippingMethods':
		return (Q(name__icontains=key))
	elif table_name=='EngageboostUnitMasters':
		return (Q(unit_name__icontains=key)|Q(unit_full_name__icontains=key))
	elif table_name=='EngageboostCurrencyMasters':
		return (Q(currencyname__icontains=key)|Q(currency__icontains=key))
	elif table_name=='EngageboostSuppliers':
		return (Q(name__icontains=key)|Q(code__icontains=key)|Q(company_name__icontains=key)|Q(email__icontains=key)|Q(contact_person__icontains=key))
	elif table_name=='EngageboostShippingMasters':
		return (Q(method_name__icontains=key)|Q(short_name__icontains=key)|Q(shipping_type__icontains=key)|Q(method_type__icontains=key))
	elif table_name=='EngageboostEmailTypeContents':
		return (Q(name__icontains=key)|Q(subject__icontains=key)|Q(email_type__icontains=key))
	elif table_name=='EngageboostCompanyWebsites':
		return (Q(business_name__icontains=key)|Q(company_name__icontains=key)|Q(email__icontains=key)|Q(website_url__icontains=key))
	elif table_name=='EngageboostCustomerGroup':
		return (Q(name__icontains=key)|Q(view_type__icontains=key))
	elif table_name=='EngageboostWarehouseMasters':
		return (Q(name__icontains=key)|Q(code__icontains=key)|Q(city__icontains=key)|Q(contact_person__icontains=key)|Q(phone__icontains=key)|Q(email__icontains=key))	
	elif table_name=='EngageboostCountries':
		return (Q(country_name__icontains=key)|Q(country_code__icontains=key))		
