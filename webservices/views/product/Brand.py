from webservices.models import EngageboostBrandMasters, EngageboostLanguages, EngageboostBrandMastersLang, EngageboostBrandWarehouse, EngageboostWarehouseMasters
from django.http import Http404
from webservices.serializers import BrandSerializer, LanguageSerializer, BrandEditSerializer, WarehousemastersSerializer
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
from django.db.models import Q
from webservices.views import loginview
from webservices.views.common import common
from django.template.defaultfilters import slugify

import json

def unique_slugify(instance,value,slug_field_name='slug',queryset=None,slug_separator='-',):
	slug_field = instance._meta.get_field(slug_field_name)
	slug = getattr(instance, slug_field.attname)
	slug_len = slug_field.max_length

	slug = slugify(value)
	if slug_len:
		slug = slug[:slug_len]
	slug = _slug_strip(slug, slug_separator)
	original_slug = slug

	if queryset is None:
		queryset = instance.__class__._default_manager.all()
	if instance.pk:
		queryset = queryset.exclude(pk=instance.pk)

	next = 2
	while not slug or queryset.filter(**{slug_field_name: slug}):
		slug = original_slug
		end = '%s%s' % (slug_separator, next)
		if slug_len and len(slug) + len(end) > slug_len:
			slug = slug[:slug_len - len(end)]
			slug = _slug_strip(slug, slug_separator)
		slug = '%s%s' % (slug, end)
		next += 1

	setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
	separator = separator or ''
	if separator == '-' or not separator:
		re_sep = '-'
	else:
		re_sep = '(?:-|%s)' % re.escape(separator)
	if separator != re_sep:
		value = re.sub('%s+' % re_sep, separator, value)
	if separator:
		if separator != '-':
			re_sep = re.escape(separator)
		value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
	return value

class Brand(generics.ListAPIView):
# """ Add New Brand """
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        name=request.data['name']
        cnt = EngageboostBrandMasters.objects.using(company_db).filter(name=name,isdeleted='n').count()
        if cnt == 0:  
            namelower = name.lower()
            name1 = namelower.replace(" ", "-")
            nametrns = name1.translate(
            {ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~=+\"\'"})
            nametrns = slugify(nametrns)
            d1={'created':datetime.now().date(),'modified':datetime.now().date(),'slug': nametrns}
            d2=request.data

            serializer_data=dict(d2,**d1)
            serializer = BrandSerializer(data=serializer_data,partial=True)

            if serializer.is_valid():
                serializer.save()
                obj = EngageboostBrandMasters.objects.using(company_db).latest('id')
                last_id = obj.id

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
                                "brand_id":last_id,
                                "field_name":key,
                                "field_value":value,
                                'created':datetime.now().date(),
                                'modified':datetime.now().date()
                            }
                            multi_lang_data.append(lang_data)

                save_brand_lang(multi_lang_data)
                
                EngageboostBrandWarehouse.objects.filter(brand_id=last_id).delete()
                if(d2['show_navigation'] == 'Y'):
                    for ware_h in d2['warehouse']:
                        EngageboostBrandWarehouse.objects.create(
                            brand_id=last_id,
                            warehouse_id=ware_h,
                            created= datetime.now().date(),
                            modified=datetime.now().date(),
                            isdeleted='n',
                            isblocked='n')

                data ={
                'status':1,
                'message':'Successfully Inserted',
                }
                return Response(data)
            else:
                data ={
                'status':0,
                'message':'Data Not Found',
                }
                return Response(data)
        else:
                data ={
                'status':0,
                
                'message':'Brand name is already exists',
                }
                return Response(data)
 #  list of Single row for brand update                   
class BrandList(generics.ListAPIView):
# """ List all Edit,Uodate Brand """
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostBrandMasters.objects.using(company_db).get(pk=pk)
        except EngageboostBrandMasters.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        user = self.get_object(pk,request)
        serializer = BrandEditSerializer(user)
        serializer_data = serializer.data
        
        if len(serializer_data['lang_data'])>0:
            for land_data in serializer_data['lang_data']:
                serializer_data[land_data['field_name']]=land_data['field_value']
        serializer_data.pop('lang_data')

        warehouse_lst = EngageboostBrandWarehouse.objects.filter(isblocked='n', isdeleted='n',brand_id=pk).values_list("warehouse_id",flat=True)
        brand_warehouse_seri = EngageboostWarehouseMasters.objects.filter(id__in=warehouse_lst).values("id","name")
        brand_warehouse = WarehousemastersSerializer(brand_warehouse_seri,many=True)

        serializer_data['warehouse']= brand_warehouse.data

        all_language_data = common.get_all_languages()

        if(serializer): 
            data ={
                'status':1,
                'api_status':serializer_data,
                "all_languages":all_language_data,
                'message':'',
                }
        else:
            data ={
                'status':0,
                'api_status':serializer.errors,
                'message':'Data Not Found',
        }
        return Response(data)
    #  Single row update of brand web services is doing here
    def put(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        Category = self.get_object(pk,request)
        #d1={'modified':datetime.now().date()}
        d2=request.data
        jsondata =json.dumps(d2)
        datajson = json.loads(jsondata)
        namejson = datajson['name']
        name = namejson.lower()
        name1 = name.replace(" ", "-")
        nametrns = name1.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~=+"})
        nametrns = slugify(nametrns)

        # d1={'modified':datetime.now().date(),'slug':nametrns}
        d1 = {'modified': datetime.now().date()}

        rs_all_lang = EngageboostLanguages.objects.filter(isblocked='n', isdeleted='n').exclude(lang_code='en').all()
        all_language_data = LanguageSerializer(rs_all_lang, many=True)
        all_language_data = all_language_data.data
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
                        "brand_id":pk,
                        "field_name":key,
                        "field_value":value,
                        'created':datetime.now().date(),
                        'modified':datetime.now().date()
                    }
                    multi_lang_data.append(lang_data)
        save_brand_lang(multi_lang_data)

        serializer_data=dict(d2,**d1)
        cnt = EngageboostBrandMasters.objects.using(company_db).filter(name=request.data['name'],isdeleted='n').filter(~Q(id=pk)).count()
        if cnt == 0:    
            serializer = BrandSerializer(Category,data=serializer_data,partial=True)
            if serializer.is_valid():
                serializer.save()
                common.related_products_to_elastic('EngageboostBrandMasters',pk)
                EngageboostBrandWarehouse.objects.filter(brand_id=pk).delete()
                if(d2['show_navigation'] == 'Y'):
                    for ware_h in d2['warehouse']:
                        EngageboostBrandWarehouse.objects.create(
                            brand_id=serializer.data['id'],
                            warehouse_id=ware_h,
                            created= datetime.now().date(),
                            modified=datetime.now().date(),
                            isdeleted='n',
                            isblocked='n')

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
        else:
            data ={
            'status':0,
            
            'message':'Brand name is already exists',
            }
            return Response(data)

def save_brand_lang(requestdata):

	if requestdata:
		for langdata in requestdata:
			rs_check_exist = EngageboostBrandMastersLang.objects.filter(brand_id=langdata['brand_id'], language_code = langdata['language_code'], field_name = langdata['field_name'], isblocked='n', isdeleted='n').first()
			if rs_check_exist:
				EngageboostBrandMastersLang.objects.filter(brand_id=langdata['brand_id'], language_code = langdata['language_code'], field_name = langdata['field_name'], isblocked='n', isdeleted='n').update(**langdata)
			else:
				EngageboostBrandMastersLang.objects.create(**langdata)
	else:
		data = {}