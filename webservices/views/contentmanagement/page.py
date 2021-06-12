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
from webservices.views import loginview
from django.db.models import Q
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import time
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser
# from webservices.functions import *
import sys
import traceback
import json
import urllib
from urllib.request import urlopen
from django.views.generic import View
import os
import tinys3
import random
from webservices.views.common import common

class AddPage(generics.ListAPIView):
# """ Add New Page """
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        d1={'created':datetime.now(),'modified':datetime.now()}
        d2=request.data
        url=d2['url']
        page_url_count=EngageboostPages.objects.using(company_db).filter(url=url,isdeleted='n').count()
        if page_url_count ==0:
            serializer_data=dict(d2,**d1)
            serializer = PagesSerializer(data=serializer_data,partial=True)
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
        else:
            data ={
            'status':0,
            'message':'Page url is already exists',
            }
            return Response(data)

# Page Update and Get 
class EditPage(APIView):
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostPages.objects.using(company_db).get(pk=pk)
        except EngageboostPages.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        company_db = loginview.db_active_connection(request)
        settings = self.get_object(pk,request)
        serializer = PagesSerializer(settings)
        if(serializer): 
            data ={
                'status':1,
                'api_status':serializer.data,
                
            }
        else:
            data ={
                'status':0,
                'api_status':serializer.errors,
                'message':'Data Not Found',
            }
        return Response(data)

    def put(self, request, pk, format=None):
        company_db = loginview.db_active_connection(request)
        d1={'modified':datetime.now()}
        d2=request.data
        serializer_data=dict(d2,**d1)
        page = self.get_object(pk,request)
        url=d2['url']
        page_url_count=EngageboostPages.objects.using(company_db).filter(url=url,isdeleted='n',company_website_id=d2['company_website_id']).filter(~Q(id=pk)).count()
        if page_url_count ==0:
            
            serializer = PagesSerializer(page, data=serializer_data,partial=True)
            if serializer.is_valid():
                serializer.save()
                data ={
                'status':1,
                'api_status':'',
                'Message':'Successfully Updated',
                }
                return Response(data)
            else:
                data ={
                'status':0,
                'api_status':serializer.errors,
                'Message':'Data Not Found',
                }
                return Response(data)
        else:
            data ={
            'status':0,
            'message':'Page url is already exists',
            }
            return Response(data)
    
class LoadPage(APIView):
    #Load all page
    @csrf_exempt
    def get(self, request,pk, format=None):
        company_db = loginview.db_active_connection(request)
        if int(pk) == int(1):
            allpage = EngageboostPages.objects.using(company_db).filter(isdeleted='n',isblocked='n',company_website_id=pk,istype=0).filter(~Q(id__in=[1,2,11,15]))
            print(allpage.count())
        else:
            allpage = EngageboostPages.objects.using(company_db).filter(isdeleted='n',isblocked='n',company_website_id=pk,istype=0)
        serializer = PagesSerializer(allpage, many=True)
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


class LoadPageByPage(APIView):
    #Load all page
    def post(self, request,pk, format=None):
        company_db = loginview.db_active_connection(request)
        key=request.data['key']
        allpage = EngageboostPages.objects.using(company_db).all().filter(isdeleted='n',company_website_id=pk).filter(Q(meta_key__icontains=key))
        serializer = PagesSerializer(allpage, many=True)

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

class PageContent(generics.ListAPIView):
# """ Add New Page Content"""
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        d1={'created':datetime.now().date(),'modified':datetime.now().date()}
        d2=request.data
        page_id=d2['page_id']
        company_website_id=d2['company_website_id']
        temp_id=d2['temp_id']
        
        page_url_count=EngageboostCmsPageSettings.objects.using(company_db).filter(temp_id=temp_id,page_id=page_id,company_website_id=company_website_id).count()
        if page_url_count ==0:
            serializer_data=dict(d2,**d1)
            serializer = CmsPageSettingsSerializer(data=serializer_data,partial=True)
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
        else:
            data ={
            'status':0,
            'message':'Page is already exists',
            }
            return Response(data)
#@csrf_exempt
class EditPageContent(generics.ListAPIView): 
  
    @csrf_exempt
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        d1={'modified':datetime.now().date()}
        d2=json.loads(request.data['data'])
        
        
        page_id=d2['page_id']
        lang=d2['lang']

        company_website_id=d2['company_website_id']
        temp_id=d2['template_id']
        image_data_cnt=EngageboostPages.objects.using(company_db).filter(id=page_id).count()   
        if image_data_cnt >0:
            image_data=EngageboostPages.objects.using(company_db).get(id=page_id)  
            #amazons3_template800_delete(image_data.template_image)
        widgets_array=[]
            
        widgets=d2['widgets']
        imageresizeon= EngageboostGlobalSettings.objects.using(company_db).get(website_id=company_website_id)
        from PIL import Image
        import os
        import urllib.request
        rand = str(random.randint(1111,9999))
        if 'file' in request.FILES:
            file1 = request.FILES['file']
            
            new_image_name='template_'+rand
            screenshot_image=new_image_name+'.png'
            fs=FileSystemStorage()
            filename = fs.save('template/800x800/'+screenshot_image, file1)
            uploaded_file_url = fs.url(filename)
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            image = Image.open(settings.BASE_DIR+uploaded_file_url)
            width_origenal, height_origenal=image.size
            if imageresizeon.image_resize =='Width':
                if width_origenal >800:
                    ratio = width_origenal/height_origenal
                    width=800
                    height=int(800*height_origenal/width_origenal)
                else:
                    width=width_origenal
                    height=height_origenal

            

            if imageresizeon.image_resize =='Height':
                if height_origenal >800:
                    ratio = height_origenal/width_origenal
                    width=int(800*width_origenal/height_origenal)
                    height=800
                else:
                    width=width_origenal
                    height=height_origenal

            
            # Banner 800x800
            img_anti = image.resize((width, height), Image.ANTIALIAS)
            new_image_file = settings.MEDIA_ROOT+'/template/800x800/'+screenshot_image
            img_anti.save(new_image_file)
            #amazons3_template800(screenshot_image)
            
        for widget in widgets:
            widgets_id=widget['id']
            if widget['type']!=3:
                for insertables in widget['insertables']:
                    for properties in insertables['properties']:
                        is_file=properties['is_file']
                        if is_file:
                            type_of_image=properties['type']
                            print("************** Image properties type **************")
                            print(type_of_image)
                            if type_of_image==2:
                                image_path=properties['value'].split('/temp_image/')
                                image_name=properties['value'].rsplit('/', 1)
                                print("*********** Image name ***********")
                                print(image_path)
                                print(image_name)
                                #amazon_path='https://s3-ap-southeast-1.amazonaws.com/barawkat/cmsimages/'
                                amazon_path = settings.AMAZON_BASE_URL+settings.AMAZON_S3_FOLDER+'/cmsimages/'
                                
                                full_image_path=amazon_path+image_name[1]
                                common.amazons3_fileupload_temp(image_path[1],image_name[1])
                                properties['value']=str(full_image_path) 
                                properties['type']=0  
                            elif type_of_image==1:
                                from PIL import Image
                                import os
                                import urllib.request
                                type_of_image=properties['type']
                                file1 = properties['value']
                                
                                extrev=file1[::-1]
                                extrevore = extrev.split(".")
                                ext=extrevore[0][::-1]
                                directory_name = str(int(time.time())*10000)

                                img=urllib.request.urlretrieve(file1,'media/temp_image/'+directory_name+'.'+ext)
                                image_name=directory_name+'.'+ext
                                fs=FileSystemStorage()
                                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                                image_path='temp_image/'+image_name
                                common.amazons3_fileupload(image_path,image_name)  
                                amazon_path=settings.AMAZON_BASE_URL+settings.AMAZON_S3_FOLDER+'/cmsimages/'
                                full_image_path=amazon_path+image_name
                                properties['value']=full_image_path
                                properties['type']=0
                    
        error_flag = 0
        for widget in widgets:
            serializer = CmsPageSettingsSerializer(data=widget,partial=True)
            if serializer.is_valid():
                error_flag = 0
            else: 
                error_flag = 1

        
        if error_flag==0:
            #EngageboostPages.objects.using(company_db).filter(id=page_id).update(template_image=screenshot_image)    
            page_row_count=EngageboostCmsPageSettings.objects.using(company_db).filter(lang=lang,page_id=page_id,company_website_id=company_website_id,temp_id=temp_id).count()
            if page_row_count >0:
                EngageboostCmsPageSettings.objects.using(company_db).filter(lang=lang,page_id=page_id,company_website_id=company_website_id,temp_id=temp_id).delete()
            
            for widget in widgets:
                EngageboostCmsPageSettings.objects.using(company_db).create(lang=lang,company_website_id=company_website_id,temp_id=temp_id,page_id=page_id,widgets=widget['id'],property_value=json.dumps(widget),modified=datetime.now().date(),created=datetime.now().date(),ip_address=d2['ip_address'],updatedby=d2['updatedby'],createdby=d2['createdby'])
            data ={
                'status':1,
                'api_status':'',
                'Message':'Successfully Updated',
            }

        else:    
            data ={
                'status':0,
                'api_status':'',
                'Message':'Database error',
            }
        return Response(data)    

class Tempimage(generics.ListAPIView):
    def post(self, request,  format=None):
        # get image data for cropping from request params
        image_data = json.loads(request.POST['image_data'])
        # dir_name variable store directory name value it's may be empty or directory already created
        dir_name=image_data['dir_name']
        # Check directory exists or not / if not create directory using timestamp
        if dir_name:            
            media_directory = os.path.join(settings.BASE_DIR+'/media/', 'temp_image', dir_name)
            directory_name = dir_name
        else:
            directory_name = str(int(time.time())*10000)
            media_directory = os.path.join(settings.BASE_DIR+'/media/', 'temp_image', directory_name)        
        if not os.path.exists(media_directory):
            os.makedirs(media_directory)
        # upload original image to media folder
        f = request.FILES['file']
        image_name = f.name
        image_name=image_name.replace(" ","-")
        file_name = str(int(time.time())) + '_' + image_name
        path = os.path.join(media_directory, file_name)
        print("************* Media path **********")
        print(path)
        destination = open(path, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        # image crop and resizing
        # image_resize(path, path, image_data['modal_image_width'], image_data['modal_image_height'])
        #crop_image(path, path, image_data['image_x'], image_data['image_y'], image_data['image_width'], int(image_data['image_height']))
        crop_image(path,(int(image_data['image_x1']),int(image_data['image_y1']),int(image_data['image_x2']),int(image_data['image_y2'])),file_name)
        amazons3_temp_image(directory_name,file_name)
        # make http response 
        response = {
            'status': 1,
            'media_dir': 'temp_image/' + directory_name + '/' + file_name,
            'dir_name': directory_name
        }
        return HttpResponse(JsonResponse(response, safe=False))
def crop_image(image_path, coords, saved_location):
    from PIL import Image
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)
    cropped_image.show()

def amazons3_temp_image(directory_name,file_name):
   #print(settings)
   conn = tinys3.Connection(settings.AMAZON_S3_ACCESS_KEY,settings.AMAZON_S3_SECRET_KEY,tls=True)
   f400 = open(settings.MEDIA_ROOT+'/temp_image/'+directory_name+'/'+file_name,'rb')
   conn.upload('Lifco/lifco/temp_image/'+directory_name+'/'+file_name,f400,settings.AMAZON_S3_BUCKET)
   return 0
class PageFormData(View):
    """save form data of a cms page"""
    def post(self, request,  format=None):
        company_db = loginview.db_active_connection(request)
        d1={'created':datetime.now(),'modified':datetime.now()}
        d2=JSONParser().parse(request)
        serializer_data=dict(d2,**d1)
        serializer = PageDataSerializer(data=serializer_data,partial=True)
        if serializer.is_valid():
            serializer.save()            
            data ={
            'status':1,
            'api_status':'',
            'message':'Successfully Inserted',
            }
            return JsonResponse(data)
        else:
            data ={
            'status':0,
            'api_status':serializer.errors,
            'message':'Data Not Found',
            }
            return JsonResponse(data)

# This is checked and verified by cds on 13-06-2019
@csrf_exempt
def Pageslurtoidload(request):
    company_db = loginview.db_active_connection(request)
    data=JSONParser().parse(request)
    url=data['url']
    lang=data['lang']
    template_id=data['template_id']
    company_website_id=data['company_website_id']
    try:
        page_slug=EngageboostPages.objects.using(company_db).get(company_website_id=company_website_id,url=url,isdeleted='n')
        pages=EngageboostCmsPageSettings.objects.using(company_db).filter(lang=lang,company_website_id=company_website_id,temp_id=template_id,page_id=page_slug.id)
        serializer_cms=CmsPageSettingsSerializer(pages,many=True)
        get_funnel_pages = EngageboostEmktFunnelPages.objects.using(company_db).filter(company_website_id=company_website_id,isdeleted='n',isblocked='n').filter(Q(landing_page_id=page_slug.id) | Q(thankyou_page_id=page_slug.id))
        funnel_data = []
        for page_value in get_funnel_pages:
            funnel_id = page_value.funnel_id
            temp = {}
            get_funnel = EngageboostEmktFunnel.objects.using(company_db).get(id=funnel_id)
            temp['funnel_id'] = funnel_id
            temp['funnel_target'] = get_funnel.funnel_target
            temp['funnel_type'] = get_funnel.funnel_type
            temp['products'] = page_value.product_ids
            temp['thankyou_slug'] = ''
            if page_slug.id == page_value.landing_page_id:
                temp['landing_or_thankyou'] = 1 ## landing page
                if temp['funnel_target']==1 or temp['funnel_type']==5:
                    thankyou_slug=EngageboostPages.objects.using(company_db).get(company_website_id=company_website_id,id=page_value.thankyou_page_id,isdeleted='n')
                    temp['thankyou_slug'] = thankyou_slug.url
                
            else:
                temp['landing_or_thankyou'] = 2 ## thankyou page
                temp['thankyou_slug'] = url  
            funnel_data.append(temp)
        data ={
            'status':1,
            'page_id':page_slug.id,
            'page_title':page_slug.page_title,
            # 'page_title_th':page_slug.page_title_th,
            'page_meta_keywords':page_slug.meta_key,
            'page_meta_description':page_slug.meta_desc,
            'page_meta_data':page_slug.meta_data,
            'cms_widgets':serializer_cms.data,
            # 'page_type': page_slug.istype,
            # 'page_data': page_slug.page_data,
            'funnel_data': funnel_data
        }
        # print(data)
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
    return JsonResponse(data)


@csrf_exempt
def CategoryList(request):
    company_db = loginview.db_active_connection(request)
    try:
        serializer_data=EngageboostCategoryMasters.objects.using(company_db).filter(isdeleted='n',isblocked='n').order_by('id')
        categories = CategoriesSerializer(serializer_data,many=True).data
        data ={
            'status':1,
            'categories':categories
        }
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
    return JsonResponse(data)    


@csrf_exempt
def ParentCategoryList(request):
    company_db = loginview.db_active_connection(request)
    data=JSONParser().parse(request)
    #print(request)
    category_id=data['category_id']
    try:
        serializer_data=EngageboostCategoryMasters.objects.using(company_db).filter(parent_id=category_id,isdeleted='n',isblocked='n').order_by('id')
        categories = CategoriesSerializer(serializer_data,many=True).data
        data ={
            'status':1,
            'categories':categories
        }
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
    return JsonResponse(data)  

@csrf_exempt
def BrandList(request):
    company_db = loginview.db_active_connection(request)
    try:
        serializer_data=EngageboostBrandMasters.objects.using(company_db).filter(isdeleted='n',isblocked='n').order_by('id')
        brands = BrandSerializer(serializer_data,many=True).data
        data ={
            'status':1,
            'brands':brands
        }
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
    return JsonResponse(data)    
