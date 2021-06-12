from webservices.models import EngageboostAdditionalGlobalsettings,EngageboostGlobalSettings,EngageboostCountries,EngageboostTimezones,EngageboostLanguages,EngageboostCurrencyMasters,EngageboostGlobalsettingCountries,EngageboostGlobalsettingCurrencies,EngageboostGlobalsettingLanguages,EngageboostCompanyWebsites
from django.http import Http404
from django.db.models import Q
from webservices.serializers import AdditionalGlobalsettingsSerializer,GlobalsettingsSerializer,GlobalsettingscountriesSerializer,GlobalsettingstimezoneSerializer,LanguageSerializer,CurrencyMastersSerializer,CompanyWebsiteSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime
from rest_framework import generics
from rest_framework.response import Response
from webservices.views import loginview

class GlobalsettingsList(generics.ListAPIView):
# """ List all Groups with pagination,sorting and searching """
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		# /////////Create Query
		if request.data.get('search'):
			key=request.data.get('search')
			groups = EngageboostGlobalSettings.objects.using(company_db).all().filter(name__icontains=key).order_by('-id')
		elif request.data.get('order_by'):
			order_by=request.data.get('order_by')
			order_type=request.data.get('order_type')
			if(order_type=='+'):
				order=order_by
			else:
				order='-'+order_by
			groups = EngageboostGlobalSettings.objects.using(company_db).all().order_by(order)    
		else:
			groups = EngageboostGlobalSettings.objects.using(company_db).all().order_by('-id')
		# /////////Create Pagination    
		page = self.paginate_queryset(groups)
		if page is not None:
			serializer = GlobalsettingsSerializer(page, many=True)
			return self.get_paginated_response(serializer.data) 
		serializer = self.GlobalsettingsSerializer(groups, many=True)
		return Response(serializer.data)
# All GlobalSettings rows fetch web services
class Glsettings(APIView):
	def get(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		settings = EngageboostGlobalSettings.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer = GlobalsettingsSerializer(settings, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		d1={'created':datetime.now().date(),'modified':datetime.now().date()}
		d2=request.data
		serializer_data=dict(d2,**d1)
		serializer = GlobalsettingsSerializer(data=serializer_data,partial=True)
		if serializer.is_valid():
			serializer.save()
			obj = EngageboostGlobalSettings.objects.using(company_db).latest('id')
			last_id = obj.id
			country=request.data['country_id']
			currency=request.data['currency_id']
			language=request.data['language_id']
			Language=language.split(",")
			Country=country.split(",")
			Currency=currency.split(",")
			for Country_data in Country:
				
				User = EngageboostGlobalsettingCountries.objects.using(company_db).create(global_setting_id=last_id,country_id=Country_data,created=datetime.now(),modified=datetime.now())
			
			for Currency_data in Currency:
				
				User = EngageboostGlobalsettingCurrencies.objects.using(company_db).create(global_setting_id=last_id,currency_id=Currency_data,created=datetime.now(),modified=datetime.now())
			
			for Language_data in Language:
				
				User = EngageboostGlobalsettingLanguages.objects.using(company_db).create(global_setting_id=last_id,language_id=Language_data,created=datetime.now(),modified=datetime.now())
			response = requests.post(serverurl+str('/api/custompagination/'), data= '',
			headers={
					   "Content-Type":"application/json",
					   "Accept": "application/json",
					   "Authorization":"token 09c3b932ba526c5038c54a6c4995a229b9606cb6"
					})
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
   
class Glsettingsup(APIView):
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostGlobalSettings.objects.using(company_db).get(pk=pk)
		except EngageboostGlobalSettings.DoesNotExist:
			raise Http404
# Single row for GlobalSettings fetch web services
	def get(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		settings = self.get_object(pk,request)
		settings_gl = GlobalsettingsSerializer(settings)
		settings1 = EngageboostCountries.objects.using(company_db).all().filter(country_name='India')
		serializer1 = GlobalsettingscountriesSerializer(settings1, many=True)
		settings = EngageboostCountries.objects.using(company_db).all().filter(~Q(country_name='India')).order_by('country_name')
		serializer = GlobalsettingscountriesSerializer(settings, many=True)
		d1=serializer1.data
		d2 = serializer.data
		data=d1+d2
		settings12 = EngageboostTimezones.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer12 = GlobalsettingstimezoneSerializer(settings12, many=True)
		settings13 = EngageboostLanguages.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer13 = LanguageSerializer(settings13, many=True)
		settings14 = EngageboostCurrencyMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
		serializer14 = CurrencyMastersSerializer(settings14, many=True)
		Countries_no=EngageboostGlobalsettingCountries.objects.using(company_db).all().filter(global_setting_id=pk)
		arr2=[]
		for Countries_num in Countries_no:
			arr2.append(Countries_num.country_id)
		
		
		Currency_no=EngageboostGlobalsettingCurrencies.objects.using(company_db).all().filter(global_setting_id=pk)
		arr3=[]
		for Currency_num in Currency_no:
			arr3.append(Currency_num.currency_id)
			
		Languages_no=EngageboostGlobalsettingLanguages.objects.using(company_db).all().filter(global_setting_id=pk)
		arr4=[]
		for Languages_num in Languages_no:
			arr4.append(Languages_num.language_id)
		add_arr={}
		additionalObj = EngageboostAdditionalGlobalsettings.objects.using(company_db).filter(isdeleted='n',isblocked='n').order_by('-id')    
		if additionalObj.count()>0:
			additional_data = additionalObj.all()

			additionaldata = AdditionalGlobalsettingsSerializer(additional_data,many=True)

			for addition in additionaldata.data:
				temp = {addition['settings_key']:addition['settings_value']}
				add_arr = dict(add_arr,**temp)

		data = {
			'country_list':arr2,
			'currency_list':arr3,
			'language_list':arr4,
			'globallist':settings_gl.data,
			'country':data,
			'timezone':serializer12.data,
			'language':serializer13.data,
			'currency':serializer14.data,
			'additional_settings':add_arr
		}
		return Response(data)
# update of GlobalSettings web services 
	def put(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		d1={'modified':datetime.now().date()}
		d2=request.data
		serializer_data=dict(d2,**d1)

		additional_settings=d2['additional_settings']
		
		settings = self.get_object(pk,request)
		serializer = GlobalsettingsSerializer(settings, data=serializer_data,partial=True)
		if serializer.is_valid():
			serializer.save()
			obj = EngageboostGlobalSettings.objects.using(company_db).latest('id')
			last_id = obj.id
			EngageboostGlobalsettingCountries.objects.using(company_db).filter(global_setting_id=pk).delete()
			EngageboostGlobalsettingCurrencies.objects.using(company_db).filter(global_setting_id=pk).delete()
			EngageboostGlobalsettingLanguages.objects.using(company_db).filter(global_setting_id=pk).delete()
			country=request.data['country_id']
			currency=request.data['currency_id']
			language=request.data['language_id']
			Language=language.split(",")
			Country=country.split(",")
			Currency=currency.split(",")
			for Country_data in Country:
				User = EngageboostGlobalsettingCountries.objects.using(company_db).create(global_setting_id=last_id,country_id=Country_data,created=datetime.now(),modified=datetime.now())
			for Currency_data in Currency:
				User = EngageboostGlobalsettingCurrencies.objects.using(company_db).create(global_setting_id=last_id,currency_id=Currency_data,created=datetime.now(),modified=datetime.now())
			for Language_data in Language:
				User = EngageboostGlobalsettingLanguages.objects.using(company_db).create(global_setting_id=last_id,language_id=Language_data,created=datetime.now(),modified=datetime.now())
			for additional in additional_settings:
				
				addition = EngageboostAdditionalGlobalsettings.objects.using(company_db).filter(settings_key=additional)
				if addition.count()>0:
					EngageboostAdditionalGlobalsettings.objects.using(company_db).filter(settings_key=additional).update(settings_value=additional_settings[additional],modified=datetime.now().date()) 
				else:
					EngageboostAdditionalGlobalsettings.objects.using(company_db).create(settings_key=additional,settings_value=additional_settings[additional],created=datetime.now().date(),modified=datetime.now().date())

			data ={
				'status':1,
				'Message':'Successfully Updated',
			}
			return JsonResponse(data)
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
			}
			return Response(data)

# selete Countries for  GlobalSettings web services 
class Glsettingscountries(APIView):
	def get(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		settings1 = EngageboostCountries.objects.using(company_db).all().filter(country_name='India')
		serializer1 = GlobalsettingscountriesSerializer(settings1, many=True)
		settings = EngageboostCountries.objects.using(company_db).all().filter(~Q(country_name='India')).order_by('country_name')
		serializer = GlobalsettingscountriesSerializer(settings, many=True)
		d1=serializer1.data
		d2 = serializer.data
		data=d1+d2
		# data1=jsonify(**data)
		return Response(data)
# selete zone for  GlobalSettings web services 
class Glsettingstimezone(APIView):
	def get(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		settings1 = EngageboostCountries.objects.using(company_db).all().filter(country_name='India')
		serializer1 = GlobalsettingscountriesSerializer(settings1, many=True)
		settings = EngageboostCountries.objects.using(company_db).all().filter(~Q(country_name='India')).order_by('country_name')
		serializer = GlobalsettingscountriesSerializer(settings, many=True)
		d1=serializer1.data
		d2 = serializer.data
		data=d1+d2
		settings12 = EngageboostTimezones.objects.using(company_db).all().filter(isdeleted='n', isblocked='n').order_by('timezone_location')
		serializer12 = GlobalsettingstimezoneSerializer(settings12, many=True)

		settings13 = EngageboostLanguages.objects.using(company_db).all().filter(isdeleted='n', isblocked='n').order_by('name')
		serializer13 = LanguageSerializer(settings13, many=True)

		settings14 = EngageboostCurrencyMasters.objects.using(company_db).all().filter(isdeleted='n',
																					   isblocked='n').order_by('currencyname')
		serializer14 = CurrencyMastersSerializer(settings14, many=True)
		data ={
			'country':data,
			'timezone':serializer12.data,
			'language':serializer13.data,
			'currency':serializer14.data
		}
		return Response(data)

class CompanyWebsites(APIView):
	def post(self, request, format=None):
		requestdata = JSONParser().parse(request)
		company_id = requestdata['company_id']
		condition = EngageboostCompanyWebsites.objects.all().filter(isdeleted='n',isblocked='n',engageboost_company_id=company_id).order_by('id').values('id','engageboost_company_id','business_name','company_name','websitename','isblocked','isdeleted','plan_id','website_category_id','engageboost_template_master_id','engageboost_template_color_master_id')
		WebsiteList = CompanyWebsiteSerializer(condition, many=True)
		if WebsiteList.data:
			data = {
				'status':1,
				'api_status':WebsiteList.data,
				'message':'Data found'
			}
		else:
			data ={
				'status':0,
				'api_status':'Data not found',
				'message':'Data not found'
			}
		return Response(data)