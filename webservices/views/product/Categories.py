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
import sys
import tinys3
import xlrd
import xlsxwriter
import sys
import traceback
from webservices.views import loginview
from django.utils.crypto import get_random_string
from webservices.views.common import common
from webservices.views.inventory.threading import *
import calendar, time


class CategoriesInfoViewSet(generics.ListAPIView):
    # """ create new category and image upload method variable d8 is declared for change request data string to json d(variable) is json form d9 use to get url string and di is the json form"""
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        method = request.scheme
        #current_url = request.META['HTTP_HOST']
        current_url = request.META['HTTP_ORIGIN']
        url = current_url + '/category/'
        d8 = request.data['data']
        imageresizeon = EngageboostGlobalSettings.objects.using(
            company_db).get(website_id=1)
        datajson = json.loads(d8)
        # print(datajson)
        d3 = datajson['name']

        marketplace_categories = datajson['marketplace_categories']
        url_suffix = datajson['url_suffix']
        name = d3.lower()
        name1 = name.replace(" ", "-")
        name1 = name1.translate(
            {ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~=+"})
        url1 = url + name1
        # ///////////////////////Name Checking for Parent'
        check_parent = EngageboostCategoryMasters.objects.using(company_db).filter(
            name=datajson['name'], parent_id=datajson['parent_id'], isdeleted='n', isblocked='n').count()
        if check_parent > 0:
            if datajson['parent_id'] == 0:
                msg = 'Parent Category Name already exists'
            else:
                msg = 'Some category have same name assigned to this parent category'
            data = {
                'status': 0,
                'message': msg,
            }
        # ///////////////////////category insert'
        else:
            cnt = EngageboostCategoryMasters.objects.using(
                company_db).filter(name=d3).count()
            if cnt == 0:
                cnt = cnt
                url2 = url1
                name1 = name1
            elif cnt == 1:
                cnt = cnt
                url2 = url1 + '1'
                name1 = name1 + '1'
            else:
                name1 = name1 + str(cnt)
                url2 = url1 + str(cnt)

            if url_suffix == "":
                main_url = url2
            else:

                cnt_url_suffix = EngageboostCategoryMasters.objects.using(
                    company_db).filter(category_url=url + url_suffix).count()

                if cnt_url_suffix == 0:
                    main_url = url + url_suffix

                else:

                    cnt_url_suffix = EngageboostCategoryMasters.objects.using(
                        company_db).filter(category_url=url + url_suffix).count()
                    if cnt_url_suffix != 0:
                        count_value = increment_value_post(
                            url_suffix, request, count_value=cnt_url_suffix)
                        main_url = url + url_suffix + str(count_value)
            from PIL import Image
            import os
            import urllib.request
            rand = str(random.randint(1111, 9999))
            if 'banner_image' in request.FILES:
                file1 = request.FILES['banner_image']
                image_name = file1.name
                ext = image_name.split('.')[-1]
                new_image_name = 'bannerImage_' + name1
                banner_image = new_image_name + '.' + ext
                fs = FileSystemStorage()
                filename = fs.save('category/200x200/' +
                                   new_image_name + '.' + ext, file1)
                uploaded_file_url = fs.url(filename)
                BASE_DIR = os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__)))
                image = Image.open(settings.BASE_DIR + uploaded_file_url)
                try:
                    image = Image.open(settings.BASE_DIR + uploaded_file_url).convert('RGB')
                except:
                    pass
                width_origenal, height_origenal = image.size
                if imageresizeon.image_resize == 'Width':
                    if width_origenal > 200:
                        ratio = width_origenal / height_origenal
                        width = 200
                        height = int(200 * height_origenal / width_origenal)
                    else:
                        width = width_origenal
                        height = height_origenal

                if imageresizeon.image_resize == 'Height':
                    if height_origenal > 200:
                        ratio = height_origenal / width_origenal
                        width = int(200 * width_origenal / height_origenal)
                        height = 200
                    else:
                        width = width_origenal
                        height = height_origenal

                # Banner 200x200
                img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/category/200x200/' + banner_image
                img_anti.save(new_image_file)
                amazons3_fileupload200(banner_image)
                if imageresizeon.image_resize == 'Width':
                    if width_origenal > 800:
                        ratio = width_origenal / height_origenal
                        width = 800
                        height = int(800 * height_origenal / width_origenal)
                    else:
                        width = width_origenal
                        height = height_origenal

                if imageresizeon.image_resize == 'Height':
                    if height_origenal > 800:
                        ratio = height_origenal / width_origenal
                        width = int(800 * width_origenal / height_origenal)
                        height = 800
                    else:
                        width = width_origenal
                        height = height_origenal

                # Banner 800x800  End

                img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/category/800x800/' + banner_image
                img_anti.save(new_image_file)
                amazons3_fileupload800(banner_image)

            elif(request.data['banner_image_url']):
                # Test Link
                file1 = request.data['banner_image_url']
                extrev = file1[::-1]
                extrevore = extrev.split(".")
                ext = extrevore[0][::-1]
                img = urllib.request.urlretrieve(
                    file1, 'media/category/200x200/' + 'bannerImage_' + name1 + '.' + ext)
                banner_image = 'bannerImage_' + name1 + '.' + ext
                BASE_DIR = os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__)))
                # Banner 200x200

                image = Image.open(settings.BASE_DIR +
                                   '/media/category/200x200/' + banner_image)
                try:
                    image = Image.open(settings.BASE_DIR +'/media/category/200x200/' + banner_image).convert('RGB')
                except:
                    pass
                width_origenal, height_origenal = image.size
                if imageresizeon.image_resize == 'Width':
                    if width_origenal > 200:
                        ratio = width_origenal / height_origenal
                        width = 200
                        height = int(200 * height_origenal / width_origenal)
                    else:
                        width = width_origenal
                        height = height_origenal

                if imageresizeon.image_resize == 'Height':
                    if height_origenal > 200:
                        ratio = height_origenal / width_origenal
                        width = int(200 * width_origenal / height_origenal)
                        height = 200
                    else:
                        width = width_origenal
                        height = height_origenal

                # Banner 200x200

                img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/category/200x200/' + banner_image
                img_anti.save(new_image_file)
                amazons3_fileupload200(banner_image)
                if imageresizeon.image_resize == 'Width':
                    if width_origenal > 800:
                        ratio = width_origenal / height_origenal
                        width = 800
                        height = int(800 * height_origenal / width_origenal)
                    else:
                        width = width_origenal
                        height = height_origenal

                if imageresizeon.image_resize == 'Height':
                    if height_origenal > 800:
                        ratio = height_origenal / width_origenal
                        width = int(800 * width_origenal / height_origenal)
                        height = 800
                    else:
                        width = width_origenal
                        height = height_origenal

                # Banner 800x800
                img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/category/800x800/' + banner_image
                img_anti.save(new_image_file)
                amazons3_fileupload800(banner_image)

                # test Link End
            else:

                banner_image = datajson['banner_image']
            if 'image' in request.FILES:
                file1 = request.FILES['image']
                image_name = file1.name
                ext = image_name.split('.')[-1]
                new_image_name = 'HeaderImage_' + name1
                header_image = new_image_name + '.' + ext
                fs = FileSystemStorage()
                filename = fs.save('category/200x200/' +
                                   new_image_name + '.' + ext, file1)
                uploaded_file_url = fs.url(filename)

                # Banner 200x200
                image = Image.open(settings.BASE_DIR + uploaded_file_url)
                try:
                    image = Image.open(settings.BASE_DIR + uploaded_file_url).convert('RGB')
                except:
                    pass
                width_origenal, height_origenal = image.size
                if imageresizeon.image_resize == 'Width':
                    if width_origenal > 200:
                        ratio = width_origenal / height_origenal
                        width = 200
                        height = int(200 * height_origenal / width_origenal)
                    else:
                        width = width_origenal
                        height = height_origenal

                if imageresizeon.image_resize == 'Height':
                    if height_origenal > 200:
                        ratio = height_origenal / width_origenal
                        width = int(200 * width_origenal / height_origenal)
                        height = 200
                    else:
                        width = width_origenal
                        height = height_origenal

                # Banner 200x200
                img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/category/200x200/' + header_image
                img_anti.save(new_image_file)
                amazons3_fileupload200(header_image)
                if imageresizeon.image_resize == 'Width':
                    if width_origenal > 800:
                        ratio = width_origenal / height_origenal
                        width = 800
                        height = int(800 * height_origenal / width_origenal)
                    else:
                        width = width_origenal
                        height = height_origenal

                if imageresizeon.image_resize == 'Height':
                    if height_origenal > 800:
                        ratio = height_origenal / width_origenal
                        width = int(800 * width_origenal / height_origenal)
                        height = 800
                    else:
                        width = width_origenal
                        height = height_origenal
                # Banner 800x800

                img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/category/800x800/' + header_image
                img_anti.save(new_image_file)
                amazons3_fileupload800(header_image)
            elif(request.data['image_url']):
                # Test Link
                file1 = request.data['image_url']
                extrev = file1[::-1]
                extrevore = extrev.split(".")
                ext = extrevore[0][::-1]
                img = urllib.request.urlretrieve(
                    file1, 'media/category/200x200/' + 'HeaderImage_' + name1 + '.' + ext)
                header_image = 'HeaderImage_' + name1 + '.' + ext
                BASE_DIR = os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__)))
                # Banner 200x200

                image = Image.open(settings.BASE_DIR +
                                   '/media/category/200x200/' + header_image)

                try:
                    image = Image.open(settings.BASE_DIR +'/media/category/200x200/' + header_image).convert('RGB')
                except:
                    pass
                width_origenal, height_origenal = image.size
                if imageresizeon.image_resize == 'Width':
                    if width_origenal > 200:
                        ratio = width_origenal / height_origenal
                        width = 200
                        height = int(200 * height_origenal / width_origenal)
                    else:
                        width = width_origenal
                        height = height_origenal

                if imageresizeon.image_resize == 'Height':
                    if height_origenal > 200:
                        ratio = height_origenal / width_origenal
                        width = int(200 * width_origenal / height_origenal)
                        height = 200
                    else:
                        width = width_origenal
                        height = height_origenal

                # Banner 200x200
                img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/category/200x200/' + header_image
                img_anti.save(new_image_file)
                amazons3_fileupload200(header_image)
                if imageresizeon.image_resize == 'Width':
                    if width_origenal > 800:
                        ratio = width_origenal / height_origenal
                        width = 800
                        height = int(800 * height_origenal / width_origenal)
                    else:
                        width = width_origenal
                        height = height_origenal

                if imageresizeon.image_resize == 'Height':
                    if height_origenal > 800:
                        ratio = height_origenal / width_origenal
                        width = int(800 * width_origenal / height_origenal)
                        height = 800
                    else:
                        width = width_origenal
                        height = height_origenal

                # Banner 800x800
                img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/category/800x800/' + header_image
                img_anti.save(new_image_file)
                amazons3_fileupload800(header_image)

            else:

                header_image = datajson['image']
            if 'thumb_image' in request.FILES:
                file1 = request.FILES['thumb_image']
                image_name = file1.name
                ext = image_name.split('.')[-1]
                new_image_name = 'IconImage_' + name1
                icon_image = new_image_name + '.' + ext
                fs = FileSystemStorage()
                filename = fs.save('category/100x100/' +
                                   new_image_name + '.' + ext, file1)
                uploaded_file_url = fs.url(filename)
                image = Image.open(settings.BASE_DIR +
                                   '/media/category/100x100/' + icon_image)
                try:
                    image = Image.open(settings.BASE_DIR + '/media/category/100x100/' + icon_image).convert('RGB')
                except:
                    pass
                width_origenal, height_origenal = image.size
                if imageresizeon.image_resize == 'Width':
                    if width_origenal > 100:
                        ratio = width_origenal / height_origenal
                        width = 100
                        height = int(100 * height_origenal / width_origenal)
                    else:

                        width = width_origenal
                        height = height_origenal

                if imageresizeon.image_resize == 'Height':
                    if height_origenal > 100:
                        ratio = height_origenal / width_origenal
                        width = int(100 * width_origenal / height_origenal)
                        height = 100
                    else:
                        width = width_origenal
                        height = height_origenal

                # Banner 200x200
                img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/category/100x100/' + icon_image
                img_anti.save(new_image_file)
                amazons3_fileupload100(icon_image)
            elif(request.data['thumb_image_url']):
                # Test Link
                file1 = request.data['thumb_image_url']
                extrev = file1[::-1]
                extrevore = extrev.split(".")
                ext = extrevore[0][::-1]

                img = urllib.request.urlretrieve(
                    file1, 'media/category/100x100/' + 'IconImage_' + name1 + '.' + ext)
                icon_image = 'IconImage_' + name1 + '.' + ext
                BASE_DIR = os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__)))
                # Banner 200x200

                image = Image.open(settings.BASE_DIR +
                                   '/media/category/100x100/' + icon_image)
                try:
                    image = Image.open(settings.BASE_DIR +'/media/category/100x100/' + icon_image).convert('RGB')
                except:
                    pass
                width_origenal, height_origenal = image.size
                if imageresizeon.image_resize == 'Width':
                    if width_origenal > 100:
                        ratio = width_origenal / height_origenal
                        width = 100
                        height = int(100 * height_origenal / width_origenal)
                    else:

                        width = width_origenal
                        height = height_origenal

                if imageresizeon.image_resize == 'Height':
                    if height_origenal > 100:
                        ratio = height_origenal / width_origenal
                        width = int(100 * width_origenal / height_origenal)
                        height = 100
                    else:
                        width = width_origenal
                        height = height_origenal

                # Banner 200x200
                img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/category/100x100/' + icon_image
                img_anti.save(new_image_file)
                amazons3_fileupload100(icon_image)

            else:
                icon_image = datajson['thumb_image']

            d1 = {'created': datetime.now().date(), 'modified': datetime.now().date(), 'category_url': main_url,
                  'slug': name1, 'image': header_image, 'banner_image': banner_image, 'thumb_image': icon_image}
            serializer_data = dict(datajson, **d1)

            serializer = CategoriesSerializer(
                data=serializer_data, partial=True)
            count = 0
            if serializer.is_valid():
                serializer.save()
                obj = EngageboostCategoryMasters.objects.using(
                    company_db).latest('id')
                last_id = obj.id
                cat_id = serializer.data['id']
                name = serializer.data['name']
                description = serializer.data['description']
                slug = serializer.data['slug']
                link = 'category/edit/' + str(cat_id)
                tab_name = 'Edit Category'
                tab_id = 'categoryedit'
                data = {"name": name, "description": description, "slug": slug,
                        "link": link, "tab_name": tab_name, "tab_id": tab_id}

                rs_all_lang = EngageboostLanguages.objects.filter(
                    isblocked='n', isdeleted='n').exclude(lang_code='en').all()
                all_language_data = LanguageSerializer(rs_all_lang, many=True)
                all_language_data = all_language_data.data
                multi_lang_data = []
                for lang_code in all_language_data:
                    langcode = lang_code['lang_code']
                    lang_id = lang_code['id']
                    listcount = len(datajson)
                    check_str = "_" + langcode

                    for key, value in datajson.items():
                        lang_data = {}
                        if check_str in key:
                            lang_data = {
                                "language_id": lang_id,
                                "language_code": langcode,
                                "category_id": cat_id,
                                "field_name": key,
                                "field_value": value,
                                'created': datetime.now().date(),
                                'modified': datetime.now().date()
                            }
                            multi_lang_data.append(lang_data)

                if serializer.data['show_navigation'] == 'Y':
                    for ware_h in datajson['warehouse']:
                        checkParent = EngageboostCategoryMasters.objects.filter(isdeleted='n',parent_id=serializer.data['id'])
                        if checkParent.count()==0:
                            catprod = EngageboostProductCategories.objects.filter(category_id = serializer.data['id'],product_id__isdeleted='n')
                            if catprod.count()>0:
                                catprod = catprod.distinct("product_id").values_list("product_id",flat=True)
                                product_id_list = list(catprod)
                                # print(product_id_list)
                                prostock = EngageboostProductStocks.objects.filter(warehouse_id = ware_h,product_id__in=product_id_list,real_stock__gt=0).count()
                            else:
                                prostock = 0
                            
                        else:
                            prostock = 1


                        EngageboostCategoryWarehouse.objects.create(
                            category_id=serializer.data['id'],
                            warehouse_id=ware_h,
                            created= datetime.now().date(),
                            modified=datetime.now().date(),
                            isdeleted='n',
                            isblocked='n',
                            product_count = prostock)
                        
                save_category_lang(multi_lang_data)

                elastic = common.save_data_to_elastic(last_id, 'EngageboostCategoryMasters')

                if marketplace_categories:
                    EngageboostChannelCategoryMappings.objects.filter(
                        boost_category_id=last_id).delete()
                    for marketplace_categorie in marketplace_categories:
                        parent_id = EngageboostCategoryMasters.objects.get(
                            id=last_id)
                        try:
                            channel_parent_id = EngageboostChannelsCategoriesMaster.objects.get(
                                id=marketplace_categorie['category_channel'])
                            EngageboostChannelCategoryMappings.objects.create(
                                channel_category_id=marketplace_categorie['category_channel'], channel_parent_category_id=channel_parent_id.parent_id, boost_parent_category_id=parent_id.parent_id, boost_category_id=last_id, channel_id=marketplace_categorie['channel'])
                        except KeyError:
                            EngageboostChannelCategoryMappings.objects.create(
                                channel_category_id=0, channel_parent_category_id=0, boost_parent_category_id=parent_id.parent_id, boost_category_id=last_id, channel_id=marketplace_categorie['channel'])

                data = {
                    'status': 1,
                    'api_status': serializer.data,
                    'message': 'Successfully Inserted',
                }
            else:
                data = {
                    'status': 0,
                    'api_status': serializer.errors,
                    'message': 'Data Not Found',
                }
        return Response(data)

# """ List all category for single row update d8 variable is used to take request data d3 is used to get name of the categories"""


class CategoriesList(generics.ListAPIView):

    def get_object(self, pk, request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostCategoryMasters.objects.using(company_db).get(pk=pk)
        except EngageboostCategoryMasters.DoesNotExist:
            raise Http404

    #///////////////////Fetch Single Row
    def get(self, request, pk, format=None):
        company_db = loginview.db_active_connection(request)
        user = self.get_object(pk, request)
        serializer = CategoriesSerializer(user)
        serializer_data = serializer.data

        if len(serializer_data['lang_data']) > 0:
            for land_data in serializer_data['lang_data']:
                serializer_data[land_data['field_name']
                                ] = land_data['field_value']
        serializer_data.pop('lang_data')

        Channels = EngageboostChannels.objects.using(company_db).all().filter(
            isdeleted='n', isblocked='n').order_by('-id')
        Channel = ChannelsSerializer(Channels, many=True)
        Categories = EngageboostCategoryMasters.objects.using(company_db).all().filter(
            isdeleted='n', isblocked='n', parent_id=0).filter(~Q(id=pk)).order_by('-id')
        Category = CategoriesSerializer(Categories, many=True)
        for serializer_row in Category.data:
            if len(serializer_row['lang_data']) > 0:
                for landdata in serializer_row['lang_data']:
                    serializer_row[landdata['field_name']
                                   ] = landdata['field_value']
            serializer_row.pop('lang_data')
        marketplace = []
        if serializer.data['parent_id'] != 0:
            child_id1 = EngageboostCategoryMasters.objects.using(
                company_db).get(id=serializer.data['parent_id'], isdeleted='n')
            if child_id1.parent_id != 0:
                child_id2 = EngageboostCategoryMasters.objects.using(
                    company_db).get(id=child_id1.parent_id, isdeleted='n')
                if child_id2.parent_id != 0:
                    child_id3 = EngageboostCategoryMasters.objects.using(
                        company_db).get(id=child_id2.parent_id, isdeleted='n')
                    category_1 = child_id3.id
                    category_2 = child_id2.id
                    category_3 = child_id1.id
                else:
                    category_1 = child_id2.id
                    category_2 = child_id1.id
                    category_3 = 0
            else:
                category_1 = child_id1.id
                category_2 = 0
                category_3 = 0
            data_parent = {"category_1": category_1,
                           "category_2": category_2, "category_3": category_3}

        else:
            data_parent = {}

        rs_all_lang = EngageboostLanguages.objects.filter(
            isblocked='n', isdeleted='n').exclude(lang_code='en').all()
        all_language_data = LanguageSerializer(rs_all_lang, many=True)

        warehouse_lst = EngageboostCategoryWarehouse.objects.filter(isblocked='n', isdeleted='n',category_id=pk).values_list("warehouse_id",flat=True)
        cat_warehouse_seri = EngageboostWarehouseMasters.objects.filter(id__in=warehouse_lst).values("id","name")
        cat_warehouse = WarehousemastersSerializer(cat_warehouse_seri,many=True)

        serializer_data['warehouse']= cat_warehouse.data
        cnt = EngageboostChannelCategoryMappings.objects.filter(
            boost_category_id=pk).count()
        if cnt > 0:
            CategoryMappings = EngageboostChannelCategoryMappings.objects.all().filter(
                boost_category_id=pk)
            for CategoryMapping in CategoryMappings:
                categoryname = EngageboostChannelsCategoriesMaster.objects.all().filter(
                    id=CategoryMapping.channel_category_id)
                category = ChannelsCategoriesMasterSerializer(
                    categoryname, many=True)
                channel_data = {'channel_id': CategoryMapping.channel_id,
                                'channel_category_id': CategoryMapping.channel_category_id, 'category': category.data}
                marketplace.append(channel_data)
            return HttpResponse(json.dumps({"image_path": settings.BASE_DIR + '/media/category/', "parent_child": data_parent, "status": 1, "api_status": serializer_data, "category": Category.data, "marketplace": marketplace, "channel": Channel.data, "all_languages": all_language_data.data}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"image_path": settings.BASE_DIR + '/media/category/', "parent_child": data_parent, "status": 1, "api_status": serializer_data, "category": Category.data, "marketplace": [], "channel": Channel.data, "all_languages": all_language_data.data}), content_type='application/json')
        # return Response('ok')

    def put(self, request, pk, format=None, partial=True):
        company_db = loginview.db_active_connection(request)
        Category = self.get_object(pk, request)
        
        method = request.scheme
        #current_url = request.META['HTTP_HOST']
        current_url = request.META['HTTP_ORIGIN']
        url = current_url + '/category/'
        d2 = request.data

        # rs_all_lang = EngageboostLanguages.objects.filter(isblocked='n', isdeleted='n').all()
        rs_all_lang = EngageboostLanguages.objects.filter(
            isblocked='n', isdeleted='n').exclude(lang_code='en').all()
        all_language_data = LanguageSerializer(rs_all_lang, many=True)
        all_language_data = all_language_data.data
        # print(all_language_data)
        imageresizeon = EngageboostGlobalSettings.objects.using(
            company_db).get(website_id=1)
        d8 = request.data['data']

        datajson = json.loads(d8)
        d3 = datajson['name']
        multi_lang_data = []
        for lang_code in all_language_data:
            langcode = lang_code['lang_code']
            lang_id = lang_code['id']
            listcount = len(datajson)
            check_str = "_" + langcode

            for key, value in datajson.items():
                lang_data = {}
                if check_str in key:
                    lang_data = {
                        "language_id": lang_id,
                        "language_code": langcode,
                        "category_id": pk,
                        "field_name": key,
                        "field_value": value,
                        'created': datetime.now().date(),
                        'modified': datetime.now().date()
                    }
                    multi_lang_data.append(lang_data)

        marketplace_categories = datajson['marketplace_categories']
        url_suffix = datajson['url_suffix']
        name = d3.lower()
        name1 = name.replace(" ", "-")
        name1 = name1.translate(
            {ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~=+\"\'"})
        url1 = url + name1
        # ///////////////////////Name Checking for Parent'
        check_parent = EngageboostCategoryMasters.objects.using(company_db).filter(name=datajson['name'], parent_id=datajson['parent_id'], isdeleted='n', isblocked='n').filter(~Q(id=pk)).count()
        if check_parent > 0:
            if datajson['parent_id'] == 0:
                msg = 'Parent Category Name already exists'
            else:
                msg = 'Current category name exist in same chosen parent category! Choose some other parent category'
            data = {
                'status': 0,
                'message': msg,
            }
        # ///////////////////////category update'
        else:
                 # /////////////Reshuffle Parent/////////////////

            fetch_parent = EngageboostCategoryMasters.objects.using(company_db).get(id=pk)
            if fetch_parent.parent_id != datajson['parent_id']:
                EngageboostCategoryMasters.objects.using(company_db).filter(parent_id=pk).update(parent_id=fetch_parent.parent_id)

                # /////////////Reshuffle Parent/////////////////

            cnt = EngageboostCategoryMasters.objects.using(
                company_db).filter(name=d3).filter(~Q(id=pk)).count()

            gmt = time.gmtime()
            ts = calendar.timegm(gmt)
            if cnt == 0:
                # gmt = time.gmtime()
                # ts = calendar.timegm(gmt)

                cnt = cnt
                url2 = url1
                name1 = name1 + '_' + str(ts)
            elif cnt == 1:
                cnt = cnt
                url2 = url1 + '1'
                name1 = name1 + '1'
            else:
                name1 = name1 + str(cnt)
                url2 = url1 + str(cnt)

            from PIL import Image
            import os
            import urllib.request
            rand = str(random.randint(1111, 9999))
            if 'banner_image' in request.FILES:
                file1 = request.FILES['banner_image']
                image_name = file1.name
                ext = image_name.split('.')[-1]
                new_image_name = 'bannerImage_' + name1
                banner_image = new_image_name + '.' + ext
                fs = FileSystemStorage()
                filename = fs.save('category/200x200/' +
                                   new_image_name + '.' + ext, file1)
                uploaded_file_url = fs.url(filename)
                BASE_DIR = os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__)))
                image = Image.open(settings.BASE_DIR + uploaded_file_url)
                try:
                    image = Image.open(settings.BASE_DIR + uploaded_file_url).convert('RGB')
                except:
                    pass
                width_origenal, height_origenal = image.size
                if imageresizeon.image_resize == 'Width':
                    if width_origenal > 200:
                        ratio = width_origenal / height_origenal
                        width = 200
                        height = int(200 * height_origenal / width_origenal)
                    else:
                        width = width_origenal
                        height = height_origenal

                if imageresizeon.image_resize == 'Height':
                    if height_origenal > 200:
                        ratio = height_origenal / width_origenal
                        width = int(200 * width_origenal / height_origenal)
                        height = 200
                    else:
                        width = width_origenal
                        height = height_origenal

                # Banner 200x200
                img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + \
                    '/category/200x200/' + new_image_name + '.' + ext
                img_anti.save(new_image_file)
                amazons3_fileupload200(banner_image)
                if imageresizeon.image_resize == 'Width':
                    if width_origenal > 800:
                        ratio = width_origenal / height_origenal
                        width = 800
                        height = int(800 * height_origenal / width_origenal)
                    else:
                        width = width_origenal
                        height = height_origenal

                if imageresizeon.image_resize == 'Height':
                    if height_origenal > 800:
                        ratio = height_origenal / width_origenal
                        width = int(800 * width_origenal / height_origenal)
                        height = 800
                    else:
                        width = width_origenal
                        height = height_origenal

                # Banner 800x800
                img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + \
                    '/category/800x800/' + new_image_name + '.' + ext
                img_anti.save(new_image_file)
                amazons3_fileupload800(banner_image)

            elif(request.data['banner_image_url']):
                # Test Link
                file1 = request.data['banner_image_url']
                extrev = file1[::-1]
                extrevore = extrev.split(".")
                ext = extrevore[0][::-1]

                img = urllib.request.urlretrieve(
                    file1, 'media/category/200x200/' + 'bannerImage_' + name1 + '.' + ext)
                banner_image = 'bannerImage_' + name1 + '.' + ext
                BASE_DIR = os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__)))
                # Banner 200x200

                image = Image.open(settings.BASE_DIR +
                                   '/media/category/200x200/' + banner_image)
                try:
                    image = Image.open(settings.BASE_DIR +'/media/category/200x200/' + banner_image).convert('RGB')
                except:
                    pass
                width_origenal, height_origenal = image.size
                if imageresizeon.image_resize == 'Width':
                    if width_origenal > 200:
                        ratio = width_origenal / height_origenal
                        width = 200
                        height = int(200 * height_origenal / width_origenal)
                    else:
                        width = width_origenal
                        height = height_origenal

                if imageresizeon.image_resize == 'Height':
                    if height_origenal > 200:
                        ratio = height_origenal / width_origenal
                        width = int(200 * width_origenal / height_origenal)
                        height = 200
                    else:
                        width = width_origenal
                        height = height_origenal

                # Banner 200x200
                img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/category/200x200/' + banner_image
                img_anti.save(new_image_file)
                amazons3_fileupload200(banner_image)
                if imageresizeon.image_resize == 'Width':
                    if width_origenal > 800:
                        ratio = width_origenal / height_origenal
                        width = 800
                        height = int(800 * height_origenal / width_origenal)
                    else:
                        width = width_origenal
                        height = height_origenal

                if imageresizeon.image_resize == 'Height':
                    if height_origenal > 800:
                        ratio = height_origenal / width_origenal
                        width = int(800 * width_origenal / height_origenal)
                        height = 800
                    else:
                        width = width_origenal
                        height = height_origenal

                # Banner 800x800
                img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/category/800x800/' + banner_image
                img_anti.save(new_image_file)
                amazons3_fileupload800(banner_image)

                # test Link End
            else:
                banner_image = datajson['banner_image']
            if 'image' in request.FILES:
                file1 = request.FILES['image']
                image_name = file1.name
                ext = image_name.split('.')[-1]
                new_image_name = 'HeaderImage_' + name1
                header_image = new_image_name + '.' + ext
                fs = FileSystemStorage()
                filename = fs.save('category/200x200/' +
                                   new_image_name + '.' + ext, file1)
                filename2 = fs.save('category/800x800/' +
                                    new_image_name + '.' + ext, file1)
                uploaded_file_url = fs.url(filename)

                # Banner 200x200
                # image = Image.open(settings.BASE_DIR + uploaded_file_url)
                # try:
                #     image = Image.open(settings.BASE_DIR + uploaded_file_url).convert('RGB')
                # except:
                #     pass
                # width_origenal, height_origenal = image.size
                # if imageresizeon.image_resize == 'Width':
                #     if width_origenal > 200:
                #         ratio = width_origenal / height_origenal
                #         width = 200
                #         height = int(200 * height_origenal / width_origenal)
                #     else:
                #         width = width_origenal
                #         height = height_origenal
                #
                # if imageresizeon.image_resize == 'Height':
                #     if height_origenal > 200:
                #         ratio = height_origenal / width_origenal
                #         width = int(200 * width_origenal / height_origenal)
                #         height = 200
                #     else:
                #         width = width_origenal
                #         height = height_origenal
                #
                # # Banner 200x200
                # img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/category/200x200/' + header_image
                amazons3_fileupload200(header_image)
                # img_anti.save(new_image_file)
                # if imageresizeon.image_resize == 'Width':
                #     if width_origenal > 800:
                #         ratio = width_origenal / height_origenal
                #         width = 800
                #         height = int(800 * height_origenal / width_origenal)
                #     else:
                #         width = width_origenal
                #         height = height_origenal
                #
                # if imageresizeon.image_resize == 'Height':
                #     if height_origenal > 800:
                #         ratio = height_origenal / width_origenal
                #         width = int(800 * width_origenal / height_origenal)
                #         height = 800
                #     else:
                #         width = width_origenal
                #         height = height_origenal
                #
                # # Banner 800x800
                # img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/category/800x800/' + header_image
                # img_anti.save(new_image_file)
                amazons3_fileupload800(header_image)
            elif(request.data['image_url']):
                # Test Link
                file1 = request.data['image_url']
                extrev = file1[::-1]
                extrevore = extrev.split(".")
                ext = extrevore[0][::-1]
                img = urllib.request.urlretrieve(
                    file1, 'media/category/200x200/' + 'HeaderImage_' + name1 + '.' + ext)
                img2 = urllib.request.urlretrieve(
                    file1, 'media/category/800x800/' + 'HeaderImage_' + name1 + '.' + ext)
                header_image = 'HeaderImage_' + name1 + '.' + ext
                BASE_DIR = os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__)))
                # Banner 200x200

                # image = Image.open(settings.BASE_DIR +
                #                    '/media/category/200x200/' + header_image)
                # try:
                #     image = Image.open(settings.BASE_DIR +'/media/category/200x200/' + header_image).convert('RGB')
                # except:
                #     pass
                # width_origenal, height_origenal = image.size
                #
                # if imageresizeon.image_resize == 'Width':
                #     if width_origenal > 200:
                #         ratio = width_origenal / height_origenal
                #         width = 200
                #         height = int(200 * height_origenal / width_origenal)
                #     else:
                #         width = width_origenal
                #         height = height_origenal
                #
                # if imageresizeon.image_resize == 'Height':
                #     if height_origenal > 200:
                #         ratio = height_origenal / width_origenal
                #         width = int(200 * width_origenal / height_origenal)
                #         height = 200
                #     else:
                #         width = width_origenal
                #         height = height_origenal
                #
                # # Banner 200x200
                # img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/category/200x200/' + header_image
                # img_anti.save(new_image_file)
                amazons3_fileupload200(header_image)
                # if imageresizeon.image_resize == 'Width':
                #     if width_origenal > 800:
                #         ratio = width_origenal / height_origenal
                #         width = 800
                #         height = int(800 * height_origenal / width_origenal)
                #     else:
                #         width = width_origenal
                #         height = height_origenal
                #
                # if imageresizeon.image_resize == 'Height':
                #     if height_origenal > 800:
                #         ratio = height_origenal / width_origenal
                #         width = int(800 * width_origenal / height_origenal)
                #         height = 800
                #     else:
                #         width = width_origenal
                #         height = height_origenal
                #
                # # Banner 800x800
                # img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/category/800x800/' + header_image
                # img_anti.save(new_image_file)
                amazons3_fileupload800(header_image)
            else:
                header_image = datajson['image']
            if 'thumb_image' in request.FILES:
                file1 = request.FILES['thumb_image']
                image_name = file1.name
                ext = image_name.split('.')[-1]
                new_image_name = 'IconImage_' + name1
                icon_image = new_image_name + '.' + ext
                fs = FileSystemStorage()
                filename = fs.save('category/100x100/' +
                                   new_image_name + '.' + ext, file1)
                uploaded_file_url = fs.url(filename)
                image = Image.open(settings.BASE_DIR +
                                   '/media/category/100x100/' + icon_image)
                try:
                    image = Image.open(settings.BASE_DIR +'/media/category/100x100/' + icon_image).convert('RGB')
                except:
                    pass
                width_origenal, height_origenal = image.size
                if imageresizeon.image_resize == 'Width':
                    if width_origenal > 100:
                        ratio = width_origenal / height_origenal
                        width = 100
                        height = int(100 * height_origenal / width_origenal)
                    else:

                        width = width_origenal
                        height = height_origenal

                if imageresizeon.image_resize == 'Height':
                    if height_origenal > 100:
                        ratio = height_origenal / width_origenal
                        width = int(100 * width_origenal / height_origenal)
                        height = 100
                    else:
                        width = width_origenal
                        height = height_origenal

                # Banner 200x200
                img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/category/100x100/' + icon_image
                img_anti.save(new_image_file)
                amazons3_fileupload100(icon_image)
            elif(request.data['thumb_image_url']):
                # Test Link
                file1 = request.data['thumb_image_url']
                extrev = file1[::-1]
                extrevore = extrev.split(".")
                ext = extrevore[0][::-1]

                img = urllib.request.urlretrieve(
                    file1, 'media/category/100x100/' + 'IconImage_' + name1 + '.' + ext)
                icon_image = 'IconImage_' + name1 + '.' + ext
                BASE_DIR = os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__)))
                # Banner 200x200

                image = Image.open(settings.BASE_DIR +
                                   '/media/category/100x100/' + icon_image)
                try:
                    image = Image.open(settings.BASE_DIR +'/media/category/100x100/' + icon_image).convert('RGB')
                except:
                    pass
                width_origenal, height_origenal = image.size
                if imageresizeon.image_resize == 'Width':
                    if width_origenal > 100:
                        ratio = width_origenal / height_origenal
                        width = 100
                        height = int(100 * height_origenal / width_origenal)
                    else:

                        width = width_origenal
                        height = height_origenal

                if imageresizeon.image_resize == 'Height':
                    if height_origenal > 100:
                        ratio = height_origenal / width_origenal
                        width = int(100 * width_origenal / height_origenal)
                        height = 100
                    else:
                        width = width_origenal
                        height = height_origenal

                # Banner 200x200
                img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/category/100x100/' + icon_image
                img_anti.save(new_image_file)
                amazons3_fileupload100(icon_image)

            else:
                icon_image = datajson['thumb_image']
            if url_suffix == "":
                main_url = url2
                name1 = name1
            else:

                cnt_url_suffix = EngageboostCategoryMasters.objects.using(company_db).filter(
                    category_url=url + url_suffix).filter(~Q(id=pk)).count()

                if cnt_url_suffix == 0:
                    main_url = url + url_suffix

                else:

                    cnt_url_suffix = EngageboostCategoryMasters.objects.using(company_db).filter(
                        category_url=url + url_suffix).filter(~Q(id=pk)).count()
                    if cnt_url_suffix != 0:
                        count_value = increment_value(
                            url_suffix, pk, request, count_value=cnt_url_suffix)
                        main_url = url + url_suffix + str(count_value)

            # d1 = {'modified': datetime.now().date(), 'category_url': main_url, 'slug': name1.replace('_' + str(ts), ''),
            #       'image': header_image, 'banner_image': banner_image, 'thumb_image': icon_image}

            d1 = {'modified': datetime.now().date(), 'category_url': main_url,
                   'image': header_image, 'banner_image': banner_image, 'thumb_image': icon_image}
                 
            d2 = request.data
            serializer_data = dict(datajson, **d1)
            serializer = CategoriesSerializer(Category, data=serializer_data, partial=True)
            count = 0
            if serializer.is_valid():
                serializer.save()

                obj = EngageboostCategoryMasters.objects.using(company_db).latest('id')
                last_id = obj.id
                cat_id = pk

                # Insert to language table
                save_category_lang(multi_lang_data)

                EngageboostChannelCategoryMappings.objects.filter(boost_category_id=pk).delete()
                for marketplace_categorie in marketplace_categories:
                    parent_id = EngageboostCategoryMasters.objects.get(id=pk)
                    try:
                        channel_parent_id = EngageboostChannelsCategoriesMaster.objects.get(id=marketplace_categorie['category_channel'])
                        EngageboostChannelCategoryMappings.objects.create(channel_category_id=marketplace_categorie['category_channel'], channel_parent_category_id=channel_parent_id.parent_id, boost_parent_category_id=parent_id.parent_id, boost_category_id=pk, channel_id=marketplace_categorie['channel'])
                    except Exception as e:
                        EngageboostChannelCategoryMappings.objects.create(
                            channel_category_id=0, channel_parent_category_id=0, boost_parent_category_id=parent_id.parent_id, boost_category_id=pk, channel_id=marketplace_categorie['channel'])

                warehouse_arr = EngageboostCategoryWarehouse.objects.filter(category_id=pk).values_list("warehouse_id",flat=True).all()
                
                # common.update_category_warehouse_stock_price(pk,warehouse_arr,datajson['warehouse'])

                # EngageboostCategoryWarehouse.objects.filter(category_id=pk).delete()
                # if(serializer.data['show_navigation'] == 'Y'):
                if len(datajson['warehouse'])>0:
                    EngageboostCategoryWarehouse.objects.filter(category_id=pk).delete()
                    for ware_h in datajson['warehouse']:

                        checkParent = EngageboostCategoryMasters.objects.filter(isdeleted='n',parent_id=serializer.data['id'])
                        if checkParent.count()==0:
                            catprod = EngageboostProductCategories.objects.filter(category_id = serializer.data['id'],product_id__isdeleted='n')
                            if catprod.count()>0:
                                catprod = catprod.distinct("product_id").values_list("product_id",flat=True)
                                product_id_list = list(catprod)
                                # print(product_id_list)
                                prostock = EngageboostProductStocks.objects.filter(warehouse_id = ware_h,product_id__in=product_id_list,real_stock__gt=0).count()
                            else:
                                prostock = 0
                            
                        else:
                            prostock = 1

                        EngageboostCategoryWarehouse.objects.create(
                            category_id=serializer.data['id'],
                            warehouse_id=ware_h,
                            created= datetime.now().date(),
                            modified=datetime.now().date(),
                            isdeleted='n',
                            isblocked='n',
                            product_count = prostock)

                elastic = common.save_data_to_elastic(cat_id, 'EngageboostCategoryMasters')
                common.related_products_to_elastic('EngageboostCategoryMasters',pk)
                #  Update Product
                # update_product(cat_id)

                data = {
                    'status': 1,
                    'api_status': serializer.data,
                    'message': 'Successfully Updated',
                }
            else:
                data = {
                    'status': 0,
                    'api_status': serializer.errors,
                    'message': 'Data Not Found',
                }
        return Response(data)

# To load Basic Info category page


class BasicInfoLoad(APIView):
    def get(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        Channels = EngageboostChannels.objects.using(company_db).all().filter(
            isdeleted='n', isblocked='n').order_by('-id')
        Channel = ChannelsSerializer(Channels, many=True)
        Categories = EngageboostCategoryMasters.objects.using(company_db).all().filter(
            isdeleted='n', isblocked='n', parent_id=0).order_by('-id')
        Category = CategoriesSerializer(Categories, many=True)

        rs_all_lang = EngageboostLanguages.objects.filter(
            isblocked='n', isdeleted='n').exclude(lang_code='en').all()
        all_language_data = LanguageSerializer(rs_all_lang, many=True)
        all_language_data = all_language_data.data

        if(Category):
            data = {
                'status': 1,
                'category': Category.data,
                'channel': Channel.data,
                "all_languages": all_language_data
            }

        else:
            data = {
                'status': 0,
                'api_status': serializer.errors,
                'message': 'Data Not Found',
            }
        return Response(data)

# Delete single Custom Field
    def delete(self, request, pk, cat, format=None):
        company_db = loginview.db_active_connection(request)
        custedit = self.get_object(pk, request)
        EngageboostDefaultsFields.objects.using(
            company_db).filter(id=pk).delete()
        EngageboostDefaultModuleLayoutFields.objects.using(
            company_db).filter(field_id=pk).delete()
        data = {
            'status': 1,
            'message': 'Successfully Deleted',
        }
        return Response(data)

# Class field_list used for Field List Web Services


class Image(generics.ListAPIView):
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        if 'image' in request.FILES:
            rand = str(random.randint(1111, 9999))
            file1 = request.FILES['image']
            image_name = file1.name
            ext = image_name.split('.')[-1]
            new_image_name = 'bannerImage_' + name1
            fs = FileSystemStorage()
            filename = fs.save('category/original/' +
                               new_image_name + '.' + ext, file1)
            uploaded_file_url = fs.url(filename)
            width = 100
            height = 100
            img_anti = img_org.resize((width, height), Image.ANTIALIAS)
            filename = fs.save('home-banners/100x100' +
                               img_anti + '.' + ext, file1)

# Get Child data


class Getchild(APIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        category_id = request.data['category_id']
        Categories = EngageboostCategoryMasters.objects.using(company_db).all().filter(
            parent_id=category_id, isdeleted='n', isblocked='n').filter(~Q(id=request.data['id']))
        Category = CategoriesSerializer(Categories, many=True)
        return HttpResponse(json.dumps({"category": Category.data, "status": 1}), content_type='application/json')
# Custom field for csv and xls file insert


# ImageDelete web services
class ImageDelete(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		ids = request.data['id']
		field = request.data['field']
		file_name = request.data['file_name']

		value = ''
		query = {field: value}
		image_name = EngageboostCategoryMasters.objects.using(
			company_db).values(field).filter(id=ids)
		conn = tinys3.Connection(
			'AKIAIOPCBUM7WOE63WDA', 'OAKgyYqjuDIa6lOsMbfbayB+X0bBRuRbWQr5aKH4', tls=True)
		image_count = EngageboostCategoryMasters.objects.using(company_db).values(field).filter(
			image=file_name).filter(Q(thumb_image=file_name)).filter(Q(banner_image=file_name))
		if image_count == 1:
			conn.delete(settings.MEDIA_ROOT+'/category/100x100/' +
						file_name, 'boostmysale')
			conn.delete(settings.MEDIA_ROOT+'/category/200x200/' +
						file_name, 'boostmysale')
			conn.delete(settings.MEDIA_ROOT+'/category/800x800/' +
						file_name, 'boostmysale')
		# if os.path.exists(settings.BASE_DIR+'/media/category/200x200/'+file_name):
		#   os.unlink(settings.BASE_DIR+'/media/category/200x200/'+file_name)
		# if os.path.exists(settings.BASE_DIR+'/media/category/100x100/'+file_name):
		#   os.unlink(settings.BASE_DIR+'/media/category/100x100/'+file_name)
		# if os.path.exists(settings.BASE_DIR+'/media/category/800x800/'+file_name):
		#   os.unlink(settings.BASE_DIR+'/media/category/800x800/'+file_name)
		EngageboostCategoryMasters.objects.using(
			company_db).filter(id=ids).update(**query)
		data = {
			'status': 1,
			'message': 'Successfully Deleted',
		}

		return Response(data)


class ChannelMapping(generics.ListAPIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        channel_id = request.data['channel_id']
        parents = EngageboostChannelsCategoriesMaster.objects.using(
            company_db).all().filter(channel_id=channel_id, parent_id=0)
        parentsdata = ChannelsCategoriesMasterSerializer(parents, many=True)
        if(parentsdata):
            data = {
                'status': 1,
                'parents': parentsdata.data,

            }

        else:
            data = {
                'status': 0,
                'api_status': serializer.errors,
                'message': 'Data Not Found',
            }
        return Response(data)


class child(generics.ListAPIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        channel_id = request.data['channel_id']
        parent_id = request.data['parent_id']
        parents = EngageboostChannelsCategoriesMaster.objects.using(
            company_db).all().filter(channel_id=channel_id, parent_id=parent_id)
        parentsdata = ChannelsCategoriesMasterSerializer(parents, many=True)
        if(parentsdata):
            parents_count = EngageboostChannelsCategoriesMaster.objects.using(
                company_db).filter(channel_id=channel_id, parent_id=parent_id).count()
            if parents_count > 0:
                data = {
                    'status': 1,
                    'child': parentsdata.data,

                }
            else:
                data = {
                    'status': 0,
                    'message': 'No child Found',

                }

        else:
            data = {
                'status': 0,
                'api_status': serializer.errors,
                'message': 'Data Not Found',
            }
        return Response(data)

class CategoryExport(generics.ListAPIView):

    def post(self, request, *args, **kwargs):
        company_db = loginview.db_active_connection(request)
        # ************  Check file dir exist or not. If dir not exist then create
        file_dir = settings.MEDIA_ROOT + '/exportfile/'
        export_dir = settings.MEDIA_URL + 'exportfile/'
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        # ************  Create file name
        today = datetime.today()
        today = today.strftime("%Y-%m-%d")
        file_name = "BMS_Categories_" + str(today)

        # Create file full path
        file_path = file_dir + file_name + '.xlsx'
        export_file_path = export_dir + file_name + '.xlsx'
        export_file_path = export_file_path[1:]

        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})
        row = 1

        worksheet.write(0, 0, 'Category1', bold)
        worksheet.write(0, 1, 'Category2', bold)
        worksheet.write(0, 2, 'Category3', bold)
        worksheet.write(0, 3, 'No of Active Product in Catalogue', bold)
        worksheet.write(0, 4, 'No of Inactive Product in Catalogue', bold)

        result = EngageboostCategoryMasters.objects.using(company_db).filter(isdeleted='n')
        
        result = result.filter(parent_id=0)
        result_count = result.count()
        
        result_data = CategoriesSerializer(result, many=True)
        result_data = result_data.data

        active_count = 0
        inactive_count = 0

        for resultdata in result_data:
            worksheet.write(row, 0, resultdata['name'], 0)

            result1 = EngageboostCategoryMasters.objects.using(company_db).filter(isdeleted='n', parent_id=resultdata['id'])
            result_count1 = result1.count()
            
            if result_count1 > 0:
                result_data1 = CategoriesSerializer(result1, many=True)
                result_data1 = result_data1.data

                for resultdata1 in result_data1:
                    worksheet.write(row, 0, resultdata['name'], 0)
                    worksheet.write(row, 1, resultdata1['name'], 0)

                    result2 = EngageboostCategoryMasters.objects.using(company_db).filter(isdeleted='n', parent_id=resultdata1['id'])
                    result_count2 = result2.count()

                    if result_count2 > 0:
                        result_data2 = CategoriesSerializer(result2, many=True)
                        result_data2 = result_data2.data

                        for resultdata2 in result_data2:
                            worksheet.write(row, 0, resultdata['name'], 0)
                            worksheet.write(row, 1, resultdata1['name'], 0)
                            worksheet.write(row, 2, resultdata2['name'], 0)

                            cat_count = get_product_count(resultdata2['id'])

                            active_count = cat_count['active_count']
                            inactive_count = cat_count['inactive_count']

                            worksheet.write(row, 3, active_count, 0)
                            worksheet.write(row, 4, inactive_count, 0)
                            row = row + 1
                    else:
                        cat_count = get_product_count(resultdata1['id'])

                        active_count = cat_count['active_count']
                        inactive_count = cat_count['inactive_count']
                    
                        worksheet.write(row, 3, active_count, 0)
                        worksheet.write(row, 4, inactive_count, 0)        
                        row = row + 1    
            else:
                cat_count = get_product_count(resultdata['id'])

                active_count = cat_count['active_count']
                inactive_count = cat_count['inactive_count']
                worksheet.write(row, 3, active_count, 0)
                worksheet.write(row, 4, inactive_count, 0)
                row = row + 1
        workbook.close()
        data = {'status': 1, "file_path": export_file_path}

        return Response(data)

class CategoryBanner(generics.ListAPIView):

    def get(self, request, pk, format=None):
        catObj = EngageboostCategoryBanners.objects.filter(id=pk)
        if catObj.count()>0:
            catResult = catObj.first()
            images = []
            serializer = CategoryBannersSerializer(catResult,partial=True)
            category_data = serializer.data
            # print(category_data)
            catObj1 = EngageboostCategoryBannersImages.objects.filter(category_banner_id=pk).distinct().order_by("id")
            imgdata_arr = []
            if catObj1.count()>0:
                catResult1 = catObj1.all().iterator()
                serializer1 = CategoryBannersImagesSerializer(catResult1,many=True)
                images = serializer1.data

                if category_data['banner_type'] == 'H':                       
                    imgdata = {}  
                    cnt = 0
                    for img in images:
                        cnt = cnt+1
                        if img['applicable_for']=="web" and cnt==1:
                            imgdata.update({"web":img})
                           
                        if img['applicable_for']=="mobile" and cnt==2:
                            imgdata.update({"mobile":img})

                        if cnt==2:
                            cnt = 0
                            imgdata_arr.append(imgdata)
                            imgdata = {}

            if category_data['banner_type'] == 'H':
                category_data["category_banners_images"] = imgdata_arr
            else:
                category_data["category_banners_images"] = images

            data = {"status":1,"api_status":category_data,"message": ""}
        else:
            data = {"status":0,"api_status":[],"message": "No data found"}    

        return Response(data)

    def post(self, request, *args, **kwargs):
        import base64
        data = request.data['data']
        data = json.loads(data)
        # print("files==================",request.FILES)
        try:
            name = data["banner_name"]
            name=name.lower()
            name1 = name.replace(" ","-")
            website_id = data["website_id"]
            warehouse_id = data["warehouse_id"]
            bannerdata = data['catgory_banner_image']
            module_name = 'category_banner'
            if data['banner_type']=="category":
                banner_type = "C"
            else:
                banner_type = "H"
                bannerdata = data['catgory_home_desktop_image']

            bannerdata_len = len(bannerdata)
            from PIL import Image
            import os
            import time
            import urllib.request
            rand = str(random.randint(1111,9999))
            img_resolutions = [200,800]
   
            banner_data = {
                "website_id":website_id,
                "banner_name":name,
                "warehouse_id":warehouse_id,
                "banner_type":banner_type,
                "created":datetime.now().date(),
                "modified":datetime.now().date()
            }

            if banner_type=="C":
                banner_data["category_id"] = data['category_id']

            banner = EngageboostCategoryBanners.objects.create(**banner_data)

            bannerId = banner.id
            # print(bannerdata)
            common.update_db_sequences("category_banners_images")
            for item_image in bannerdata:
                timestamp = time.strftime("%Y%m%d%H%M%s")
                if banner_type=="C":
                    if item_image['url']:
                        image_data = item_image['url']
                        img_arr = image_data.split(",")
                        img_rs = img_arr[0]
                        img_rs_arr = img_rs.split("/")
                        img_rs_arr = img_rs_arr[1].split(";")
                        imgdata = base64.b64decode(img_arr[1])
                        ext = img_rs_arr[0]
                        
                        new_image_name = name1+'_'+timestamp
                        other_image = new_image_name+'.'+ext

                    elif(item_image['image_url']):
                        file1 = item_image['image_url']
                        extrev=file1[::-1]
                        extrevore = extrev.split(".")
                        ext=extrevore[0][::-1]

                        new_image_name = name1+'_'+timestamp
                        other_image = new_image_name+'.'+ext    
                    
                    imageresizeon= EngageboostGlobalSettings.objects.get(website_id=website_id)
                    website = EngageboostCompanyWebsites.objects.get(id=website_id)

                    company_name = website.company_name
                    s3folder_name = website.s3folder_name
                    
                    for imgresolution in img_resolutions:
                        imgresolutionstr = str(imgresolution)

                        if item_image['url']:
                            filename = settings.BASE_DIR+'/media/'+module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+other_image 
                            # I assume you have a way of picking unique filenames
                            with open(filename, 'wb') as f:
                                    f.write(imgdata)

                        elif(item_image['image_url']):
                            img=urllib.request.urlretrieve(file1, '/media/'+module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+other_image)
                            fs=FileSystemStorage()
                            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                            uploaded_file_url = fs.url(img)

                        image = Image.open(settings.BASE_DIR+'/media/'+module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+other_image)
                        try:
                            image = Image.open(settings.BASE_DIR+'/media/'+module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+other_image).convert('RGB')
                        except:
                            pass
                        width_origenal, height_origenal=image.size

                        # ICON 100X100
                        if imageresizeon.image_resize =='Width' and imgresolution==200:
                            if width_origenal >imgresolution:
                                ratio = width_origenal/height_origenal
                                width=imgresolution
                                height=int(imgresolution*height_origenal/width_origenal)
                            else:
                                width=width_origenal
                                height=height_origenal
                        else:
                            width=width_origenal
                            height=height_origenal          

                        if imageresizeon.image_resize =='Height' and imgresolution==200:
                            if height_origenal >imgresolution:
                                ratio = height_origenal/width_origenal
                                width=int(imgresolution*width_origenal/height_origenal)
                                height=imgresolution
                            else:
                                width=width_origenal
                                height=height_origenal
                        else:
                            width=width_origenal
                            height=height_origenal        
                        
                        img_anti = image.resize((width, height), Image.ANTIALIAS)
                        new_image_file = settings.MEDIA_ROOT+'/'+module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+other_image
                        img_anti.save(new_image_file)
                        common.amazons3_global_fileupload(other_image,imgresolutionstr,module_name,company_name,s3folder_name)
                        
                    cat_data = {}

                    cat_data["primary_image_name"] = other_image
                    cat_data["category_banner_id"] = bannerId
                        
                    item = item_image         
                    cat_data1 = {}
                    try:
                        if item["caption1"]:
                            cat_data1["banner_caption1"] = item["caption1"]
                        if item["caption2"]:
                            cat_data1["banner_caption2"] = item["caption2"]
                        if data['category_id']:
                            cat_data1["category_id"] = data['category_id']
                        if item['banner_linkto']:
                            cat_data1["banner_link_to"] = item['banner_linkto']

                        if item['banner_linkto']=="external link":
                            banner_link = item['link']
                            cat_data['link'] = banner_link

                        elif item['banner_linkto']=="promotion":
                            banner_link = item['item_ids']
                            cat_data['promotion_id'] = banner_link

                        elif item['banner_linkto']=="category":
                            banner_link = item['item_ids']
                            cat_data['category_id'] = banner_link 

                        elif item['banner_linkto']=="product":
                            banner_link = item['item_ids']
                            cat_data['product_id'] = banner_link

                        # if item['send_notification']=="yes":
                        #     send = "Yes"
                        #     cat_data["is_notification_enabled_val"] = send
                        #     cat_data["notification_msg"] = item['message']
                        # else:
                        #     send = "No"
                        #     cat_data["is_notification_enabled_val"] = send    
                    except Exception as error:
                        print("error")         
                    cat_data1["created"] = datetime.now().date()
                    cat_data1["modified"] = datetime.now().date()
                    # cat_data1["start_date"] = item_image['start_date']
                    # cat_data1["end_date"] = item_image['end_date']
                    cat_data = dict(cat_data,**cat_data1)          
                    EngageboostCategoryBannersImages.objects.create(**cat_data)
                else:
                    type_arr = ['web', 'mobile']
                    # timestamp = time.strftime("%Y%m%d%H%M%s")
                    for x in type_arr:
                        # timestamp = time.strftime("%Y%m%d%H%M%s")
                        if item_image[x]['url']:
                            # print(item_image[x])
                            image_data = item_image[x]['url']
                            img_arr = image_data.split(",")
                            img_rs = img_arr[0]
                            img_rs_arr = img_rs.split("/")
                            img_rs_arr = img_rs_arr[1].split(";")
                            imgdata = base64.b64decode(img_arr[1])
                            ext = img_rs_arr[0]
                            
                            new_image_name = name1+'_'+timestamp
                            other_image = new_image_name+'.'+ext

                        elif(item_image[x]['image_url']):
                            file1 = item_image[x]['image_url']
                            extrev=file1[::-1]
                            extrevore = extrev.split(".")
                            ext=extrevore[0][::-1]

                            new_image_name = name1+'_'+timestamp
                            other_image = new_image_name+'.'+ext    
                        
                        imageresizeon= EngageboostGlobalSettings.objects.get(website_id=website_id)
                        website = EngageboostCompanyWebsites.objects.get(id=website_id)

                        company_name = website.company_name
                        s3folder_name = website.s3folder_name
                        
                        for imgresolution in img_resolutions:
                            imgresolutionstr = str(imgresolution)

                            if item_image[x]['url']:
                                filename = settings.BASE_DIR+'/media/'+module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+other_image 
                                # I assume you have a way of picking unique filenames
                                with open(filename, 'wb') as f:
                                        f.write(imgdata)

                            elif(item_image[x]['image_url']):
                                img=urllib.request.urlretrieve(file1, '/media/'+module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+other_image)
                                fs=FileSystemStorage()
                                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                                uploaded_file_url = fs.url(img)

                            image = Image.open(settings.BASE_DIR+'/media/'+module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+other_image)
                            try:
                                image = Image.open(settings.BASE_DIR+'/media/'+module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+other_image).convert('RGB')
                            except:
                                pass
                            width_origenal, height_origenal=image.size

                            # ICON 100X100
                            if imageresizeon.image_resize =='Width' and imgresolution==200:
                                if width_origenal >imgresolution:
                                    ratio = width_origenal/height_origenal
                                    width=imgresolution
                                    height=int(imgresolution*height_origenal/width_origenal)
                                else:
                                    width=width_origenal
                                    height=height_origenal
                            else:
                                width=width_origenal
                                height=height_origenal          

                            if imageresizeon.image_resize =='Height' and imgresolution==200:
                                if height_origenal >imgresolution:
                                    ratio = height_origenal/width_origenal
                                    width=int(imgresolution*width_origenal/height_origenal)
                                    height=imgresolution
                                else:
                                    width=width_origenal
                                    height=height_origenal
                            else:
                                width=width_origenal
                                height=height_origenal        
                            
                            img_anti = image.resize((width, height), Image.ANTIALIAS)
                            new_image_file = settings.MEDIA_ROOT+'/'+module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+other_image
                            img_anti.save(new_image_file)
                            common.amazons3_global_fileupload(other_image,imgresolutionstr,module_name,company_name,s3folder_name)

                        cat_data = {}
                        
                        cat_data["primary_image_name"] = other_image
                        cat_data["category_banner_id"] = bannerId
                            
                        item = item_image         
                        cat_data1 = {}       
                        cat_data1["created"] = datetime.now().date()
                        cat_data1["modified"] = datetime.now().date()
                        cat_data1["applicable_for"] = x
                        # cat_data1["start_date"] = item_image[x]['start_date']
                        # cat_data1["end_date"] = item_image[x]['end_date']
                        cat_data = dict(cat_data,**cat_data1)          
                        EngageboostCategoryBannersImages.objects.create(**cat_data)


            common.delete_create_image_from_local_folder(img_resolutions,module_name)                  
            data = {"status":1,"api_status":"","message": "Successfully Saved"}        
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
            print(data)
        data.update({"imgdata":bannerdata})
        return Response(data)

    def put(self, request, pk, *args, **kwargs):
        import base64
        data = request.data['data']
        data = json.loads(data)
        print("files==================",data)
        try:
            banner_count = EngageboostCategoryBanners.objects.filter(id=pk,isdeleted="n").count()
            if banner_count>0:
                name = data["banner_name"]
                name = name.lower()
                name1 = name.replace(" ","-")
                website_id = data["website_id"]
                warehouse_id = data["warehouse_id"]
                bannerdata = data['catgory_banner_image']
                module_name = 'category_banner'

                if data['banner_type']=="category":
                    banner_type = "C"
                else:
                    banner_type = "H"
                    bannerdata = data['catgory_home_desktop_image']

                bannerdata_len = len(bannerdata)
                from PIL import Image
                import os
                import time
                import base64
                import urllib.request
                rand = str(random.randint(1111,9999))
                img_resolutions = [200,800]
                
                banner_data = {
                    "website_id":website_id,
                    "banner_name":name,
                    "warehouse_id":warehouse_id,
                    "banner_type":banner_type,
                    "created":datetime.now().date(),
                    "modified":datetime.now().date()
                }

                if banner_type=="C":
                    banner_data["category_id"] = data['category_id']

                banner = EngageboostCategoryBanners.objects.filter(id=pk).update(**banner_data)
                bannerId = pk
                common.update_db_sequences("category_banners_images")
                for item_image in bannerdata:
                    item = item_image
                    cat_data1 = {}
                    cat_data = {}
                    if 'id' not in item_image.keys():
                        image_data = item_image['url']
                        img_arr = image_data.split(",")
                        img_rs = img_arr[0]
                        img_rs_arr = img_rs.split("/")
                        img_rs_arr = img_rs_arr[1].split(";")
                        imgdata = base64.b64decode(img_arr[1])
                        ext = img_rs_arr[0]
                        timestamp = time.strftime("%Y%m%d%H%M%s")
                        new_image_name = name1+'_'+timestamp
                        other_image = new_image_name+'.'+ext
                        
                        imageresizeon= EngageboostGlobalSettings.objects.get(website_id=website_id)
                        website = EngageboostCompanyWebsites.objects.get(id=website_id)

                        company_name = website.company_name
                        s3folder_name = website.s3folder_name
                        
                        for imgresolution in img_resolutions:
                            imgresolutionstr = str(imgresolution)

                            filename = settings.BASE_DIR+'/media/'+module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+other_image 

                            # I assume you have a way of picking unique filenames
                            with open(filename, 'wb') as f:
                                    f.write(imgdata)

                            # fs=FileSystemStorage()
                            # filename = fs.save(module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+other_image, file1)
                            # uploaded_file_url = fs.url(filename)
                            # Banner 200x200
                            image = Image.open(settings.BASE_DIR+'/media/'+module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+other_image)
                            try:
                                image = Image.open(settings.BASE_DIR+'/media/'+module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+other_image).convert('RGB')
                            except:
                                pass
                            width_origenal, height_origenal=image.size

                            # ICON 100X100
                            # print(imageresizeon.image_resize,imageresizeon.image_resize)
                            if imageresizeon.image_resize =='Width':
                                if width_origenal >imgresolution and imgresolution==200:
                                    ratio = width_origenal/height_origenal
                                    width=imgresolution
                                    height=int(imgresolution*height_origenal/width_origenal)
                                else:
                                    width=width_origenal
                                    height=height_origenal
                            # else:
                            #     print("Here4")
                            #     width=width_origenal
                            #     height=height_origenal          

                            if imageresizeon.image_resize =='Height':
                                if height_origenal >imgresolution and imgresolution==200:
                                    ratio = height_origenal/width_origenal
                                    width=int(imgresolution*width_origenal/height_origenal)
                                    height=imgresolution
                                else:
                                    width=width_origenal
                                    height=height_origenal
                            # else:
                            #     width=width_origenal
                            #     height=height_origenal
                            img_anti = image.resize((width, height), Image.ANTIALIAS)
                            new_image_file = settings.MEDIA_ROOT+'/'+module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+other_image
                            img_anti.save(new_image_file)
                            common.amazons3_global_fileupload(other_image,imgresolutionstr,module_name,company_name,s3folder_name)

                        cat_data["primary_image_name"] = other_image
                        cat_data["category_banner_id"] = bannerId
                        
                    try:
                        if item["caption1"]:
                            cat_data1["banner_caption1"] = item["caption1"]
                        if item["caption2"]:
                            cat_data1["banner_caption2"] = item["caption2"]
                        if data['category_id']:
                            cat_data1["category_id"] = data['category_id']
                        if item['banner_linkto']:
                            cat_data1["banner_link_to"] = item['banner_linkto']

                        if item['banner_linkto']=="external link":
                            banner_link = item['link']
                            cat_data['link'] = banner_link

                        elif item['banner_linkto']=="promotion":
                            banner_link = item['item_ids']
                            cat_data['promotion_id'] = banner_link

                        elif item['banner_linkto']=="category":
                            banner_link = item['item_ids']
                            cat_data['category_id'] = banner_link 

                        elif item['banner_linkto']=="product":
                            banner_link = item['item_ids']
                            cat_data['product_id'] = banner_link

                        # if item['send_notification']=="yes":
                        #     send = "Yes"
                        #     cat_data["is_notification_enabled_val"] = send
                        # else:
                        #     send = "No"
                        #     cat_data["is_notification_enabled_val"] = send    
                    except Exception as error:
                        print("error")         
                    cat_data1["created"] = datetime.now().date()
                    cat_data1["modified"] = datetime.now().date()

                    cat_data = dict(cat_data,**cat_data1)          

                    # print("Cat Data==========",cat_data)
                    try:
                        image_id = item_image['id']
                        EngageboostCategoryBannersImages.objects.filter(id=image_id).update(**cat_data)
                    except Exception as error:
                        EngageboostCategoryBannersImages.objects.create(**cat_data)

                common.delete_create_image_from_local_folder(img_resolutions,module_name)      
                data = {"status":1,"api_status":"","message": "Successfully Updated"}        
            else:
                data = {"status":0,"api_status":"","message": "Data not found"}
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
            print(data)
        return Response(data)

# CategoryBanner Image delete
class CategoryBannerImageDelete(generics.ListAPIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        ids=request.data['id']
        # field=request.data['field']
        # file_name=request.data['file_name']

        field = "primary_image_name"

        value=''
        query = {field : value}
        image_name=EngageboostCategoryBannersImages.objects.using(company_db).filter(id=ids).first()
        file_name = image_name.primary_image_name
        d1 = {field:file_name}
        img_count=EngageboostCategoryBannersImages.objects.using(company_db).filter(**d1).count()
        # print("img_count=====",img_count)
        catObj = EngageboostCategoryBanners.objects.filter(id=image_name.category_banner_id)
        if catObj.count()>0:
            link = ""
            catResult = catObj.first()
            website_id = catResult.website_id
            website = EngageboostCompanyWebsites.objects.get(id=website_id)
            company_name = website.company_name
            s3folder_name = website.s3folder_name
            module_name = 'category_banner'
            link = company_name+'/'+s3folder_name+'/'+module_name

            if img_count==1:
                conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)
                conn.delete(link+'/200x200/'+file_name,settings.AMAZON_S3_BUCKET)
                conn.delete(link+'/800x800/'+file_name,settings.AMAZON_S3_BUCKET)
                # conn.delete(link+'/400x400/'+file_name,settings.AMAZON_S3_BUCKET)
                # conn.delete(link+'/80x80/'+file_name,settings.AMAZON_S3_BUCKET)
                # conn.delete(link+'/400x400/'+file_name,settings.AMAZON_S3_BUCKET)
            # if os.path.exists(settings.BASE_DIR+'/media/product/200x200/'+file_name):
            #   os.unlink(settings.BASE_DIR+'/media/product/200x200/'+file_name)
            # if os.path.exists(settings.BASE_DIR+'/media/product/100x100/'+file_name):
            #   os.unlink(settings.BASE_DIR+'/media/product/100x100/'+file_name)
            # if os.path.exists(settings.BASE_DIR+'/media/product/800x800/'+file_name):
            #   os.unlink(settings.BASE_DIR+'/media/product/800x800/'+file_name)
            # if os.path.exists(settings.BASE_DIR+'/media/product/400x400/'+file_name):
            #   os.unlink(settings.BASE_DIR+'/media/product/400x400/'+file_name)
            # if os.path.exists(settings.BASE_DIR+'/media/product/80x80/'+file_name):
            #   os.unlink(settings.BASE_DIR+'/media/product/80x80/'+file_name)
            EngageboostCategoryBannersImages.objects.using(company_db).filter(id=ids).delete()
        data ={
                'status':1,
                'message':'Successfully Deleted',
                }

        return Response(data)

def get_product_count(cat_id):
    products = EngageboostProductCategories.objects.filter(
        category_id=cat_id).values_list('product_id', flat=True)
    count1 = 0
    count2 = 0
    if len(products) > 0:
        count1 = EngageboostProducts.objects.filter(
            isdeleted='n', id__in=products).count()
        count2 = EngageboostProducts.objects.filter(
            isdeleted='y', id__in=products).count()
    return {"active_count": count1, "inactive_count": count2}

def increment_value(url_suffix, pk, request, count_value):
    company_db = loginview.db_active_connection(request)
    method = request.scheme
    current_url = request.META['HTTP_HOST']
    url = method + '://' + current_url + '/category/'

    cnt_url_suffix = EngageboostCategoryMasters.objects.using(company_db).filter(
        category_url=url + url_suffix + str(count_value), isblocked='n', isdeleted='n').filter(~Q(id=pk)).count()
    if cnt_url_suffix == 0:
        return count_value
    else:
        count_value = count_value + 1
        return increment_value(url_suffix, pk, request, count_value)

def increment_value_post(url_suffix, request, count_value):
    company_db = loginview.db_active_connection(request)
    method = request.scheme
    current_url = request.META['HTTP_HOST']
    url = method + '://' + current_url + '/category/'

    cnt_url_suffix = EngageboostCategoryMasters.objects.using(company_db).filter(
        category_url=url + url_suffix + str(count_value), isblocked='n', isdeleted='n').count()
    if cnt_url_suffix == 0:
        return count_value
    else:
        count_value = count_value + 1
        return increment_value_post(url_suffix, request, count_value)

def amazons3_fileupload200(file_name):

	conn = tinys3.Connection(
		settings.AMAZON_S3_ACCESS_KEY, settings.AMAZON_S3_SECRET_KEY, tls=True)

	f200 = open(settings.MEDIA_ROOT + '/category/200x200/' + file_name, 'rb')
	conn.upload(settings.AMAZON_S3_FOLDER+'/category/200x200/' +
				file_name, f200, settings.AMAZON_S3_BUCKET)
	if os.path.exists(settings.BASE_DIR + '/media/category/200x200/' + file_name):
		os.unlink(settings.BASE_DIR + '/media/category/200x200/' + file_name)
	return 0

def amazons3_fileupload800(file_name):
	conn = tinys3.Connection(
		settings.AMAZON_S3_ACCESS_KEY, settings.AMAZON_S3_SECRET_KEY, tls=True)
	f800 = open(settings.MEDIA_ROOT + '/category/800x800/' + file_name, 'rb')
	conn.upload(settings.AMAZON_S3_FOLDER+'/category/800x800/' +
				file_name, f800, settings.AMAZON_S3_BUCKET)
	if os.path.exists(settings.BASE_DIR + '/media/category/800x800/' + file_name):
		os.unlink(settings.BASE_DIR + '/media/category/800x800/' + file_name)
	return 0

def amazons3_fileupload100(file_name):
	conn = tinys3.Connection(
		settings.AMAZON_S3_ACCESS_KEY, settings.AMAZON_S3_SECRET_KEY, tls=True)
	f100 = open(settings.MEDIA_ROOT + '/category/100x100/' + file_name, 'rb')
	conn.upload(settings.AMAZON_S3_FOLDER+'/category/100x100/' +
				file_name, f100, settings.AMAZON_S3_BUCKET)
	if os.path.exists(settings.BASE_DIR + '/media/category/100x100/' + file_name):
		os.unlink(settings.BASE_DIR + '/media/category/100x100/' + file_name)
	return 0

def save_category_lang(requestdata):
	if requestdata:
		for langdata in requestdata:
			rs_check_exist = EngageboostCategoryMastersLang.objects.filter(
				category_id=langdata['category_id'], language_code=langdata['language_code'], field_name=langdata['field_name'], isblocked='n', isdeleted='n').first()
			if rs_check_exist:
				EngageboostCategoryMastersLang.objects.filter(
					category_id=langdata['category_id'], language_code=langdata['language_code'], field_name=langdata['field_name'], isblocked='n', isdeleted='n').update(**langdata)
			else:
				EngageboostCategoryMastersLang.objects.create(**langdata)
	else:
		data = {}

class AllImageUpload(generics.ListAPIView):

    def get_queryset(self, pk, request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostCategoryMasters.objects.using(company_db).get(pk=pk)
        except EngageboostCategoryMasters.DoesNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):
        from PIL import Image
        import os
        import urllib.request
        import time

        rand                = str(random.randint(1111,9999))
        img_resolutions     = [200,800]
        rand                = str(random.randint(1111, 9999))
        return_data_list    = []
        module_name = None
        if "module_name" in request.data:
            module_name = request.data['module_name']

        if 'catgory_banner_image' in request.FILES:
            file_arr    = request.FILES.getlist('catgory_banner_image')            #  Image File
            # module_name = 'category_banner'
            for file1 in file_arr:
                return_data = {}
                timestamp       = time.strftime("%Y%m%d%H%M%s")
                website_id = request.data['website_id']
                location_type = None
                if "image_type" in request.data:
                    location_type 	= request.data['image_type']    #  category image/ Home Banner Image/ Category Banner Image etc/;
                
                if location_type is None:
                    location_type 	= request.data['imageType']
                image_name      = file1.name                        #  Get Image Name from uploading file
                ext             = image_name.split('.')[-1]         #  Get Image Ext. from uploading file
                if location_type is not None:
                    location_type = location_type.replace(" ","-")
                else:
                    location_type = module_name

                if module_name is None:
                    module_name = location_type

                new_image_name  = location_type + "_" + timestamp      # Generate New Image Name
                banner_image    = new_image_name + '.' + ext
                other_image = banner_image

                fs              = FileSystemStorage()
                filename        = fs.save(module_name+'/200x200/' + new_image_name + '.' + ext, file1)
                uploaded_file_url = fs.url(filename)
                BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                image           = Image.open(settings.BASE_DIR + uploaded_file_url)
                try:
                    image = Image.open(settings.BASE_DIR + uploaded_file_url).convert('RGB')
                except:
                    pass
                width_origenal, height_origenal = image.size               
                imageresizeon = "Width"
                if imageresizeon == 'Width':
                    if width_origenal > 200:
                        ratio = width_origenal / height_origenal
                        width = 200
                        height = int(200 * height_origenal / width_origenal)
                    else:
                        width = width_origenal
                        height = height_origenal
                if imageresizeon == 'Height':
                    if height_origenal > 200:
                        ratio = height_origenal / width_origenal
                        width = int(200 * width_origenal / height_origenal)
                        height = 200
                    else:
                        width = width_origenal
                        height = height_origenal

                # Banner 200x200
                img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/'+module_name+'/200x200/' + banner_image
                img_anti.save(new_image_file)
                imgresolution = 200
                imgresolutionstr = str(imgresolution)
                website         = EngageboostCompanyWebsites.objects.get(id=website_id)
                company_name    = website.company_name
                s3folder_name   = website.s3folder_name

                aws_return = common.amazons3_global_fileupload_new(other_image,imgresolutionstr,module_name,company_name,s3folder_name)
                # if int(aws_return['status'])>0:
                test_link200 = company_name+'/'+s3folder_name+'/'+module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+other_image

                return_data.update({"link200":test_link200})
    
                # Banner 800x800
                if imageresizeon == 'Width':
                    if width_origenal > 800:
                        ratio = width_origenal / height_origenal
                        width = 800
                        height = int(800 * height_origenal / width_origenal)
                    else:
                        width = width_origenal
                        height = height_origenal
                if imageresizeon == 'Height':
                    if height_origenal > 800:
                        ratio = height_origenal / width_origenal
                        width = int(800 * width_origenal / height_origenal)
                        height = 800
                    else:
                        width = width_origenal
                        height = height_origenal
                img_anti = image.resize((width, height), Image.ANTIALIAS)

                imgresolution_800 = 800
                imgresolutionstr = str(imgresolution_800)
                website         = EngageboostCompanyWebsites.objects.get(id=website_id)
                company_name    = website.company_name
                s3folder_name   = website.s3folder_name

                fs              = FileSystemStorage()
                filename        = fs.save(module_name+'/800x800/' + new_image_name + '.' + ext, file1)
                uploaded_file_url = fs.url(filename)
                BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                image           = Image.open(settings.BASE_DIR + uploaded_file_url)
                try:
                    image = Image.open(settings.BASE_DIR + uploaded_file_url).convert('RGB')
                except:
                    pass

                new_image_file = settings.MEDIA_ROOT + '/'+module_name+'/800x800/' + banner_image
                img_anti.save(new_image_file)
                aws_return = common.amazons3_global_fileupload_new(other_image,imgresolutionstr,module_name,company_name,s3folder_name)
                # if int(aws_return['status'])>0:
                test_link800 = company_name+'/'+s3folder_name+'/'+module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+banner_image
                return_data.update({"link800":test_link800})
                return_data.update({"file_name":banner_image})
                return_data_list.append(return_data)
                # Banner 800x800  End
            
            common.delete_create_image_from_local_folder(img_resolutions,module_name) 
        elif "banner_image_url" in request.data and (request.data['banner_image_url']):
            # Test Link
            file1 = request.data['banner_image_url']
            extrev = file1[::-1]
            extrevore = extrev.split(".")
            ext = extrevore[0][::-1]
            img = urllib.request.urlretrieve(
                file1, 'media/category/200x200/' + 'bannerImage_' + name1 + '.' + ext)
            banner_image = 'bannerImage_' + name1 + '.' + ext
            BASE_DIR = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))
            # Banner 200x200

            image = Image.open(settings.BASE_DIR +
                                '/media/category/200x200/' + banner_image)
            try:
                image = Image.open(settings.BASE_DIR +'/media/category/200x200/' + banner_image).convert('RGB')
            except:
                pass
            width_origenal, height_origenal = image.size
            if imageresizeon.image_resize == 'Width':
                if width_origenal > 200:
                    ratio = width_origenal / height_origenal
                    width = 200
                    height = int(200 * height_origenal / width_origenal)
                else:
                    width = width_origenal
                    height = height_origenal

            if imageresizeon.image_resize == 'Height':
                if height_origenal > 200:
                    ratio = height_origenal / width_origenal
                    width = int(200 * width_origenal / height_origenal)
                    height = 200
                else:
                    width = width_origenal
                    height = height_origenal

            # Banner 200x200

            img_anti = image.resize((width, height), Image.ANTIALIAS)
            new_image_file = settings.MEDIA_ROOT + '/category/200x200/' + banner_image
            img_anti.save(new_image_file)
            amazons3_fileupload200(banner_image)
            if imageresizeon.image_resize == 'Width':
                if width_origenal > 800:
                    ratio = width_origenal / height_origenal
                    width = 800
                    height = int(800 * height_origenal / width_origenal)
                else:
                    width = width_origenal
                    height = height_origenal

            if imageresizeon.image_resize == 'Height':
                if height_origenal > 800:
                    ratio = height_origenal / width_origenal
                    width = int(800 * width_origenal / height_origenal)
                    height = 800
                else:
                    width = width_origenal
                    height = height_origenal

            # Banner 800x800
            img_anti = image.resize((width, height), Image.ANTIALIAS)
            new_image_file = settings.MEDIA_ROOT + '/category/800x800/' + banner_image
            img_anti.save(new_image_file)
            amazons3_fileupload800(banner_image)

            # test Link End
        elif 'import_file' in request.FILES and module_name is not None:
            file_arr    = request.FILES.getlist('import_file')            #  Image File
            module_name = module_name
            for file1 in file_arr:
                return_data = {}
                timestamp       = time.strftime("%Y%m%d%H%M%s")
                website_id = request.data['website_id']
                location_type = None
                image_name      = file1.name                        #  Get Image Name from uploading file
                ext             = image_name.split('.')[-1]         #  Get Image Ext. from uploading file
                if module_name is not None:
                    location_type = module_name.replace(" ","-")
               
                new_image_name  = location_type + "_" + timestamp      # Generate New Image Name
                banner_image    = new_image_name + '.' + ext
                other_image = banner_image

                fs              = FileSystemStorage()
                filename        = fs.save(location_type+'/200x200/' + new_image_name + '.' + ext, file1)
                uploaded_file_url = fs.url(filename)
                BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                image           = Image.open(settings.BASE_DIR + uploaded_file_url)
                try:
                    image = Image.open(settings.BASE_DIR + uploaded_file_url).convert('RGB')
                except:
                    pass
                width_origenal, height_origenal = image.size               
                imageresizeon = "Width"
                if imageresizeon == 'Width':
                    if width_origenal > 200:
                        ratio = width_origenal / height_origenal
                        width = 200
                        height = int(200 * height_origenal / width_origenal)
                    else:
                        width = width_origenal
                        height = height_origenal
                if imageresizeon == 'Height':
                    if height_origenal > 200:
                        ratio = height_origenal / width_origenal
                        width = int(200 * width_origenal / height_origenal)
                        height = 200
                    else:
                        width = width_origenal
                        height = height_origenal

                # Banner 200x200
                img_anti = image.resize((width, height), Image.ANTIALIAS)
                new_image_file = settings.MEDIA_ROOT + '/'+location_type+'/200x200/' + banner_image
                img_anti.save(new_image_file)
                imgresolution = 200
                imgresolutionstr = str(imgresolution)
                website         = EngageboostCompanyWebsites.objects.get(id=website_id)
                company_name    = website.company_name
                s3folder_name   = website.s3folder_name

                aws_return = common.amazons3_global_fileupload_new(other_image,imgresolutionstr,module_name,company_name,s3folder_name)
                print(aws_return)
                # if int(aws_return['status'])>0:
                test_link200 = company_name+'/'+s3folder_name+'/'+module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+other_image

                return_data.update({"link200":test_link200})
    
                # Banner 800x800
                if imageresizeon == 'Width':
                    if width_origenal > 800:
                        ratio = width_origenal / height_origenal
                        width = 800
                        height = int(800 * height_origenal / width_origenal)
                    else:
                        width = width_origenal
                        height = height_origenal
                if imageresizeon == 'Height':
                    if height_origenal > 800:
                        ratio = height_origenal / width_origenal
                        width = int(800 * width_origenal / height_origenal)
                        height = 800
                    else:
                        width = width_origenal
                        height = height_origenal
                img_anti = image.resize((width, height), Image.ANTIALIAS)

                imgresolution_800 = 800
                imgresolutionstr = str(imgresolution_800)
                website         = EngageboostCompanyWebsites.objects.get(id=website_id)
                company_name    = website.company_name
                s3folder_name   = website.s3folder_name


                fs              = FileSystemStorage()
                filename        = fs.save(location_type+'/800x800/' + new_image_name + '.' + ext, file1)
                uploaded_file_url = fs.url(filename)
                BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                image           = Image.open(settings.BASE_DIR + uploaded_file_url)
                try:
                    image = Image.open(settings.BASE_DIR + uploaded_file_url).convert('RGB')
                except:
                    pass

                new_image_file = settings.MEDIA_ROOT + '/'+location_type+'/800x800/' + banner_image
                img_anti.save(new_image_file)
                aws_return = common.amazons3_global_fileupload_new(other_image,imgresolutionstr,module_name,company_name,s3folder_name)
                # if int(aws_return['status'])>0:
                test_link800 = company_name+'/'+s3folder_name+'/'+module_name+'/'+imgresolutionstr+'x'+imgresolutionstr+'/'+banner_image
                return_data.update({"link800":test_link800})
                return_data.update({"file_name":banner_image})
                return_data_list.append(return_data)
                # Banner 800x800  End
            
            common.delete_create_image_from_local_folder(img_resolutions,module_name) 
        else:
            banner_image = datajson['banner_image']
        
        data = {
            "status":1,
            "data":return_data_list,
            "AMAZON_IMAGE_URL":settings.AMAZON_BASE_URL
        }

        return Response(data)

def amazons3_fileupload(file_name,file_size,file_location):
	file_size = file_size+"x"+file_size
	conn = tinys3.Connection(
		settings.AMAZON_S3_ACCESS_KEY, settings.AMAZON_S3_SECRET_KEY, tls=True)
	f800 = open(settings.MEDIA_ROOT + "/"+file_location+"/"+file_size+"/" + file_name, 'rb')
	conn.upload(settings.AMAZON_S3_FOLDER+file_location+'/'+file_size+'/' +
				file_name, f800, settings.AMAZON_S3_BUCKET)
	if os.path.exists(settings.BASE_DIR + '/media/category/800x800/' + file_name):
		os.unlink(settings.BASE_DIR + '/media/category/800x800/' + file_name)
	return 0


class CategoryBannerNew(generics.ListAPIView):

    def get(self, request, pk, format=None):
        catObj = EngageboostCategoryBanners.objects.filter(id=pk)
        if catObj.count()>0:
            catResult = catObj.first()
            images = []
            serializer = CategoryBannersSerializer(catResult,partial=True)
            category_data = serializer.data
            catObj1 = EngageboostCategoryBannersImages.objects.filter(category_banner_id=pk).order_by("id")
            if catObj1.count()>0:
                catResult1 = catObj1.all().iterator()
                serializer1 = CategoryBannersImagesSerializer(catResult1,many=True)
                images = serializer1.data
                if category_data['banner_type'] == 'H':
                    rs_image = EngageboostCategoryBannersImages.objects.filter(category_banner_id=pk).values_list('primary_image_name').distinct()
                    imgdata_arr = []
                    for image_data in rs_image:                        
                        imgdata = {}                      
                        for img in images:                            
                            if img['applicable_for']=="web":
                                imgdata.update({"web":img})
                            else:
                                imgdata.update({"mobile":img})
                        imgdata_arr.append(imgdata)
                        # print(imgdata_arr)
            if category_data['banner_type'] == 'H':
                category_data["category_banners_images"] = imgdata_arr
            else:
                category_data["category_banners_images"] = images

            data = {"status":1,"api_status":category_data,"message": ""}
        else:
            data = {"status":0,"api_status":[],"message": "No data found"}    

        return Response(data)

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            name = data["banner_name"]
            name = name.lower()
            website_id  = data["website_id"]
            warehouse_id = data["warehouse_id"]
            module_name = 'category_banner'
            bannerdata  = data['catgory_banner_image']
            edit_banner_id = None
            if "banner_id" in data:
                edit_banner_id = data['banner_id']

            if data['banner_type']=="category":
                banner_type = "C"
            else:
                banner_type = "H"
                # bannerdata = data['catgory_home_desktop_image']

            bannerdata_len = len(bannerdata)
            rand = str(random.randint(1111,9999))
            img_resolutions = [200,800]
   
            banner_data = {
                "website_id":website_id,
                "banner_name":name,
                "warehouse_id":warehouse_id,
                "banner_type":banner_type,
                "created":datetime.now().date(),
                "modified":datetime.now().date()
            }

            if banner_type=="C":
                banner_data["category_id"] = data['category_id']
            if banner_type!="" and banner_type.lower()=="category":
                banner_data["category_id"] = data['category_id']
            
            if edit_banner_id is None:
                insert_id = EngageboostCategoryBanners.objects.create(**banner_data)
                banner_id = insert_id.id
            else:
                insert_id = EngageboostCategoryBanners.objects.filter(id=edit_banner_id).update(**banner_data)
                banner_id = edit_banner_id
            # dd = {"ss":1}
            # return Response(dd) 
            update_banner_list = []
            for item_image in data['catgory_banner_image']:
                if banner_type=="C" or banner_type=="category":
                    cat_data = {}
                    cat_data1 = {}
                    
                    cat_data["primary_image_name"]  = item_image['primary_image_name']
                    cat_data["category_banner_id"]  = banner_id
                    cat_data1["created"]            = datetime.now().date()
                    cat_data1["modified"]           = datetime.now().date()
                    #cat_data1["start_date"]         = item_image['start_date']
                    #cat_data1["end_date"]           = item_image['end_date']
                    try:
                        if item_image["banner_caption1"]:
                            cat_data1["banner_caption1"] = item_image["banner_caption1"]
                        if item_image["banner_caption2"]:
                            cat_data1["banner_caption2"] = item_image["banner_caption2"]
                        
                        if data['category_id']:
                            cat_data1["category_id"] = data['category_id']
                        
                        if "banner_linkto" in item_image:
                            cat_data1["banner_link_to"] = item_image['banner_linkto']

                            if item_image['banner_linkto']=="external link":
                                banner_link = item_image['link']
                                cat_data1['link'] = banner_link

                            if item_image['banner_linkto']=="promotion":
                                banner_link = item_image['item_ids']
                                cat_data1['promotion_id'] = banner_link

                            if item_image['banner_linkto']=="category":
                                banner_link = item_image['item_ids']
                                cat_data1['category_id'] = banner_link 

                            if item_image['banner_linkto']=="product":
                                banner_link = item_image['item_ids']
                                cat_data1['product_id'] = banner_link
                    except Exception as error:
                        trace_back = sys.exc_info()[2]
                        line = trace_back.tb_lineno
                        data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}        

                    cat_data = dict(cat_data,**cat_data1)

                    rs_chk_exist = EngageboostCategoryBannersImages.objects.filter(primary_image_name=item_image['primary_image_name'], category_banner_id=banner_id).first()
                    if rs_chk_exist:
                        EngageboostCategoryBannersImages.objects.filter(id=rs_chk_exist.id).update(**cat_data)
                    else:
                        EngageboostCategoryBannersImages.objects.create(**cat_data)
                else:
                    type_arr = ['web', 'mobile']
                    for x in type_arr:
                        cat_data    = {}
                        cat_data1   = {}
                        cat_data["primary_image_name"] = item_image[x]['primary_image_name']
                        cat_data["category_banner_id"] = banner_id                                                    
                        cat_data1["created"]        = datetime.now().date()
                        cat_data1["modified"]       = datetime.now().date()
                        cat_data1["applicable_for"] = x
                        cat_data1["start_date"]     = item_image[x]['start_date']
                        cat_data1["end_date"]       = item_image[x]['end_date']
                        if item_image[x]["banner_caption1"]:
                            cat_data1["banner_caption1"] = item_image[x]["banner_caption1"]
                        if item_image[x]["banner_caption2"]:
                            cat_data1["banner_caption2"] = item_image[x]["banner_caption2"]
                        
                        if "category_id" in data and data['category_id']:
                            cat_data1["category_id"] = data['category_id']
                        if "banner_linkto" in item_image[x]:
                                cat_data1["banner_link_to"] = item_image[x]['banner_linkto']

                                if item_image[x]['banner_linkto']=="external link":
                                    banner_link = item_image[x]['link']
                                    cat_data1['link'] = banner_link

                                if item_image[x]['banner_linkto']=="promotion":
                                    banner_link = item_image[x]['item_ids']
                                    cat_data1['promotion_id'] = banner_link

                                if item_image[x]['banner_linkto']=="category":
                                    banner_link = item_image[x]['item_ids']
                                    cat_data1['category_id'] = banner_link 

                                if item_image[x]['banner_linkto']=="product":
                                    banner_link = item_image[x]['item_ids']
                                    cat_data1['product_id'] = banner_link  

                        cat_data = dict(cat_data,**cat_data1)
                        rs_chk_exist = EngageboostCategoryBannersImages.objects.filter(primary_image_name=item_image[x]['primary_image_name'], category_banner_id=banner_id).first()
                        

                        if rs_chk_exist:
                            EngageboostCategoryBannersImages.objects.filter(id=rs_chk_exist.id).update(**cat_data)
                            update_banner_list.append(rs_chk_exist.id)
                        else:
                            insert_id = EngageboostCategoryBannersImages.objects.create(**cat_data)
                            update_banner_list.append(insert_id.id)

            if len(update_banner_list)>0:
                rs_delete = EngageboostCategoryBannersImages.objects.filter(category_banner_id=banner_id).exclude(id__in = update_banner_list).delete()                

            common.delete_create_image_from_local_folder(img_resolutions,module_name)                  
            data = {"status":1,"api_status":"","message": "Successfully Saved"}        
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
            # print(data)
        # data.update({"imgdata":bannerdata})
        return Response(data)

@postpone
def update_product(cat_id):
    try:
        if int(cat_id)>0:
            rs_pro_cat = EngageboostProductCategories.objects.filter(category_id=cat_id, product_id__isblocked='n', product_id__isdeleted='n')
            if rs_pro_cat.count()>0:
                prod_list = rs_pro_cat.values_list("product_id", flat=True)
                prod_list = list(set(prod_list))
                for products in prod_list:
                    if products is not None and products!="" and int(products)>0:
                        elastic = common.save_data_to_elastic(int(products), 'EngageboostProducts')
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        # print(data)