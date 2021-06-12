from webservices.models import *
from django.apps import apps
from django.http import Http404
from django.http import JsonResponse
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
import csv
import collections
from webservices.views import loginview

#///////////////////Global Listing Filter
class GlobalListFilter(generics.ListAPIView):
# """ Global List Filter all Models with pagination,sorting and searching """
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        # /////////Create Query
        table_name=request.data.get('model')
        model=apps.get_model('webservices',table_name)
        screen_name=request.data.get('screen_name')
        serializer_class = get_serializer_class(self,table_name)
        module=table_name.replace("Engageboost", "")

        #####################Layout#################################
        layout_fetch=EngageboostGridLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
        layout_header=layout_fetch.header_name
        layout_field=layout_fetch.field_name
        
        layout_check=EngageboostGridColumnLayouts.objects.using(company_db).filter(module=module,screen_name=screen_name).count()
        if(layout_check):
            layout = EngageboostGridColumnLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
            if request.data.get('is_default'):
                serializer_data={'header_name':layout_header,'field_name':layout_field,'modified':datetime.now()}
            else:
                d1={'modified':datetime.now()}
                d2=request.data
                serializer_data=dict(d2,**d1)
            serializer = GridColumnLayoutsSerializer(layout,data=serializer_data,partial=True)
        else:
            if request.data.get('is_default'):
                serializer_data={'website_id':1,'company_id':1,'module':module,'screen_name':screen_name,'isdeleted':'n','header_name':layout_header,'field_name':layout_field,'created':datetime.now(),'modified':datetime.now()}
            else:
                d1={'website_id':1,'company_id':1,'module':module,'screen_name':screen_name,'isdeleted':'n','created':datetime.now(),'modified':datetime.now()}
                d2=request.data
                serializer_data=dict(d2,**d1)
            serializer = GridColumnLayoutsSerializer(data=serializer_data,partial=True)    
        #####################Layout#################################
        #####################Final Result#################################
        if serializer.is_valid():
            serializer.save()
            data ={
            'status':1,
            'api_status':serializer.data,
            'message':'Successfully Updated',
            }
        else:
            data ={
            'status':0,
            'api_status':serializer.errors,
            'message':'Data Not Found',
            }
        return Response(data)  
#///////////////////Global Listing Export
class GlobalListExport(generics.ListAPIView):
# """ Global List Export all Models with searching """
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        # /////////Create Query
        table_name=request.data.get('model')
        userid=request.data.get('userid')
        model=apps.get_model('webservices',table_name)
        export_type=request.data.get('type')
        module=table_name.replace("Engageboost", "")
        screen_name=request.data.get('screen_name')
        serializer_class = get_serializer_class(self,table_name)
        #####################Query Generation#################################
        if request.data.get('search') and request.data.get('order_by'):
            key=request.data.get('search')
            order_by=request.data.get('order_by')
            order_type=request.data.get('order_type')
            if(order_type=='+'):
                order=order_by
            else:
                order='-'+order_by
            result = model.objects.using(company_db).all().order_by(order).filter(get_search_filter(self,table_name,key))
        elif request.data.get('search'):
            key=request.data.get('search')
            result = model.objects.using(company_db).all().order_by('-id').filter(get_search_filter(self,table_name,key))
        elif request.data.get('order_by'):
            order_by=request.data.get('order_by')
            order_type=request.data.get('order_type')
            if(order_type=='+'):
                order=order_by
            else:
                order='-'+order_by
            result = model.objects.using(company_db).all().order_by(order)    
        else:
            result = model.objects.using(company_db).all().order_by('-id')
        ###############################Additional Filter Model Wise###########
        if table_name=='EngageboostDiscountMasters' and screen_name=='list1':
            result=result.filter(discount_master_type='1')
        elif table_name=='EngageboostDiscountMasters' and screen_name=='list2':
            result=result.filter(discount_master_type='0')

        if table_name=='EngageboostOrdermaster':
            result_all = result.count()
            result1 = result.count()
            result2 = result.count() 
            result=result
        else:
            result=result.filter(isdeleted='n')
            result_all = result.count()
            result1 = result.filter(isblocked='y').count()
            result2 = result.filter(isblocked='n').count()
            if request.data.get('status'):
                if request.data.get('status')=="n":
                    result=result.filter(isblocked='n')
                elif request.data.get('status')=="y":
                    result=result.filter(isblocked='y')
            else:
                result=result

        #####################Query Generation#################################
        # /////////Create Result    
        if result is not None:
            serializer = serializer_class(result, many=True)
            #####################Layout#################################
            module=table_name.replace("Engageboost", "")
            layout_fetch=EngageboostGridLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
            layout_header=layout_fetch.header_name.split("@@")
            layout_field=layout_fetch.field_name.split("@@")
            layout_check=EngageboostGridColumnLayouts.objects.using(company_db).filter(module=module,screen_name=screen_name).count()
            layout={}
            layout_arr=[]
            layout_head=[]
            layout_item=[]
            for header,field in zip(layout_header,layout_field):
                ex_layout_field=field.split(".")
                field_name=ex_layout_field[0]
                if len(ex_layout_field)>1:
                    child_name=ex_layout_field[1]
                else:
                    child_name=''

                if(layout_check):
                    layout_column_fetch=EngageboostGridColumnLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
                    layout_column_header=layout_column_fetch.header_name
                    layout_column_field=layout_column_fetch.field_name
                    if header in layout_column_header:
                        status=1
                        layout_head.append(header)
                        layout_item.append(field)
                    else:
                        status=0
                else:
                    status=1 
                    layout_head.append(header)
                    layout_item.append(field)       
                layout={"title":header,"field":field_name,"child":child_name,"show":status}
                layout_arr.append(layout)
            
            #####################Layout#################################

            ######################Role Permission###############
            users = EngageboostUsers.objects.using(company_db).get(id=userid)
            issuperadmin = users.issuperadmin
            role_id = users.role_id
            role_permission={}

            if table_name=='EngageboostDiscountMasters' and screen_name=='list1':
                menu_fetch=EngageboostMenuMasters.objects.using(company_db).get(module='DiscountMasters1')
            elif table_name=='EngageboostDiscountMasters' and screen_name=='list2':
                menu_fetch=EngageboostMenuMasters.objects.using(company_db).get(module='DiscountMasters2')
            else:
                menu_fetch=EngageboostMenuMasters.objects.using(company_db).get(module=module)
            menu_id=menu_fetch.id
            menu_link=menu_fetch.link

            if issuperadmin=='Y':
                export='1'
            else:
                role_per = EngageboostRoleMenuPermissions.objects.using(company_db).get(role_id=role_id,master_id=menu_id,isblocked=0,isdeleted=0)
                export=role_per.export
            ######################Role Permission###############

            #####################Action Links#################################
            link=module.replace("masters", "")
            link=link.replace("Masters", "")
            row=[]
            row_dict={}
            is_popup=layout_fetch.add_edit_url_popup
            folder=layout_fetch.folder_name
            layout_module=layout_fetch.module_name
            
            for serializer_row in serializer.data :
                
                row_dict=serializer_row

                #####################Table Based Nesting#################################
                if table_name =='EngageboostProducts':
                    product_id=serializer_row['id']
                    brand_id=serializer_row['brand']
                    supplier_id=serializer_row['supplier_id']
                    # /////Category////////
                    fetch_category=EngageboostProductCategories.objects.using(company_db).all().filter(product=product_id)
                    categoryarr=[];
                    catdict={}
                    for cat in fetch_category:
                        catdict=cat.category.name
                        categoryarr.append(catdict)
                    category=','.join([str(i) for i in categoryarr])
                    row_dict['category']=category
                    # ////////brand/////////
                    brandarr=[];
                    if brand_id:
                        brands=brand_id.split(",")  
                        for bid in brands:
                            if bid:       
                                fetch_brand=EngageboostBrandMasters.objects.using(company_db).get(id=bid)
                                brandarr.append(fetch_brand.name)
                        brand=','.join([str(i) for i in brandarr])
                        row_dict['brand']=brand
                    else:   
                        row_dict['brand']=''
                    # ////////supplier/////////
                    supplierarr=[];
                    if supplier_id:
                        supplier=supplier_id.split(",")  
                        for sid in supplier:
                            if sid:       
                                fetch_supplier=EngageboostSuppliers.objects.using(company_db).get(id=sid)
                                supplierarr.append(fetch_supplier.name)
                        supplier=','.join([str(i) for i in supplierarr])
                        row_dict['supplier']=supplier 
                    else:   
                        row_dict['supplier']=''

                if table_name =='EngageboostPresets':
                    # /////size////////
                    size=str(serializer_row['sizel'])+"*"+str(serializer_row['sizew'])+"*"+str(serializer_row['sizeh'])
                    row_dict['size']=size
                if table_name =='EngageboostEmktContactlists':
                    # /////contact////////
                    contlist_id=serializer_row['id']
                    contact=EngageboostEmktContacts.objects.using(company_db).filter(contact_list_id=contlist_id).count()
                    row_dict['contact']=contact
                if table_name =='EngageboostEmktSegments':
                    # /////contact////////
                    seg_id=serializer_row['id']
                    contact=EngageboostEmktSegmentContactlists.objects.using(company_db).filter(segment_id=seg_id).count()
                    row_dict['contact']=contact 
                if table_name =='EngageboostEmktSegments':
                    # /////contact////////
                    seg_id=serializer_row['id']
                    contact=EngageboostEmktSegmentContactlists.objects.using(company_db).filter(segment_id=seg_id).count()
                    row_dict['contact']=contact   
                     
                if table_name =='EngageboostEmailTypeContents':
                    # /////contact////////
                    email_type=serializer_row['email_type']
                    if email_type == 'T':
                        contact ='TEXT'
                    elif email_type == 'HT':
                        contact ='HTML & TEXT'
                    elif email_type == 'H':
                        contact ='HTML'
                    row_dict['email_type']=contact    

                if table_name =='EngageboostShippingMasters':
                    # /////contact////////
                    id=serializer_row['id']
                    awb_total=EngageboostAwbMasters.objects.using(company_db).filter(isdeleted='n',isblocked='n',shipping_method_id=id).count()
                    awb_unused=EngageboostAwbMasters.objects.using(company_db).filter(isdeleted='n',isblocked='n',shipping_method_id=id,isused='n').count()
                    awb_used=EngageboostAwbMasters.objects.using(company_db).filter(isdeleted='n',isblocked='n',shipping_method_id=id,isused='y').count()
                    row_dict['total']=awb_total
                    row_dict['awb_unused']=awb_unused
                    row_dict['awb_used']=awb_used  

                if table_name =='EngageboostUsers':
                    # /////last login////////
                    date=EngageboostGlobalSettings.objects.using(company_db).get(website_id=1)
                    zone=EngageboostTimezones.objects.using(company_db).get(id=date.timezone_id)
                    time_zone=get_time(serializer_row['last_login'],zone,date)
                    row_dict['last_login']=time_zone
                if table_name =='EngageboostGlobalSettings':
                    # /////timezone////////
                    timezone_id=serializer_row['timezone_id']
                    timezone_fetch=EngageboostTimezones.objects.using(company_db).get(id=timezone_id) 
                    row_dict['timezone_location']=timezone_fetch.timezone_location+' '+timezone_fetch.gmt 
                    row_dict['date_format']=serializer_row['date_format'].replace("%","")
                if table_name =='EngageboostCurrencyMasters':
                    # /////Currency////////
                    currency_id=serializer_row['id']
                    timezone_fetch=EngageboostCurrencyRates.objects.using(company_db).get(engageboost_currency_master_id=currency_id) 
                    row_dict['currency_code']=timezone_fetch.currency_code
                    row_dict['exchange_rate']=timezone_fetch.exchange_rate
                    row_dict['isbasecurrency']=timezone_fetch.isbasecurrency
                    row_dict['modified']=timezone_fetch.modified
                if table_name =='EngageboostCompanyWebsites':
                    date=EngageboostGlobalSettings.objects.using(company_db).get(website_id=1)
                    zone=EngageboostTimezones.objects.using(company_db).get(id=date.timezone_id)
                    time_zone=get_time(serializer_row['created'],zone,date)
                    row_dict['created']=time_zone
                #####################Table Based Nesting#################################
                row.append(row_dict) 
                  
            #####################Action Links#################################
            if export=='1':               
                #Popup/page setup start here....
                if export_type=='y':
                    export_link='<a class="md-button btn-main" href="javascript:void(0)" popup-box init-fn="add_edit_load(arg1)" box-template="static/pages/'+str(folder)+'/add_'+str.lower(module)+'.html" elem-id="#add_'+str.lower(module)+'_pop"> Manage Excahnge Rate ''</a>'
                else:
                    export_link='<md-button class="md-button btn-main" href="#/'+str.lower(link)+'/add/'+str(menu_link)+'" ng-click="addTab(\''+str.lower(link)+''+str(menu_link)+'add''\',\''+str.lower(link)+'/add/'+str(menu_link)+'\',\'Add '+str(layout_module)+'\',tabs[selectedTab].id)">+ Add '+str(layout_module)+'</md-button>'
               #Popup/page setup end here....
            else:
                export_link='<a class="md-button btn-main compile" href="javascript:void(0)" ng-click="$root.showAlertBox(\'Permission Error\',\'You have no permission to Export\')">+ Add '+str(layout_module)+'</a>'
            export_btn=export_link
            #####################Active/Inacative#################################
            pre_data={}
            final_data=[] 
            pre_data=row 
            # pre_data['all']=result_all
            # pre_data['add_btn']=add_link
            #####################Active/Inacative#################################
            #####################Final Result#################################
            final_data.append(pre_data)
            # return Response(final_data)   
        #####################Layout#################################
        #####################Final Result#################################
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        writer = csv.writer(response)
        res={}
        resarr=[]
        i=0
        resarr.append(layout_head)
        # writer.writerow(layout_head)
        for data in final_data[0]:

            i += 1
            j=i
            # print(data['name'])
            # for item in layout_item:
            #     res=(data[item])
            #     # if i==j:
            #         # resarr.append(res)
            # #         # a= ','.join(resarr)  
            # #         # print(a)
            # writer.writerow([data['name'],data['isblocked']])
            res={data['name'],data['isblocked']}

            resarr.append(res)
        # return response
        return Response(resarr) 
        # if serializer.is_valid():
        #     serializer.save()
        #     data ={
        #     'status':1,
        #     'api_status':serializer.data,
        #     'message':'Successfully Updated',
        #     }
        # else:
        #     data ={
        #     'status':0,
        #     'api_status':serializer.errors,
        #     'message':'Data Not Found',
        #     }
        # return Response(data)  
    def get(self,request):
        company_db = loginview.db_active_connection(request)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        # writer = csv.writer(response)
        # res={}
        # resarr=[]
        # i=0
        # with open('some.csv', 'wb') as f:    
        #     writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"]) 
        #     return response
        with open('persons.csv', 'wb') as csvfile:
            writer = csv.writer(response)
            writer.writerow(['Name', 'Profession'])
            writer.writerow(['Derek', 'Software Developer'])
            writer.writerow(['Steve', 'Software Developer'])
            writer.writerow(['Paul', 'Manager'])
        return response                

def export_csv(request):
    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="users.csv"'

    # writer = csv.writer(response)
    # writer.writerow(['Username', 'First name', 'Last name', 'Email address'])
    # return response
    with open('persons.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Name', 'Profession'])
        writer.writerow(['Derek', 'Software Developer'])
        writer.writerow(['Steve', 'Software Developer'])
        writer.writerow(['Paul', 'Manager'])
    return response

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

def get_time(gettime,zone,date):
    datetime = gettime.replace('T',' ')
    data_time=datetime.replace('Z',' ')
    a=data_time.split(".")
    b=a[0].replace(':',' ')
    c=b.replace('-',' ')
    date_format=c.split(" ")
    import datetime
    import time
    a1 = datetime.datetime(int(date_format[0]), int(date_format[1]), int(date_format[2]), int(date_format[3]), int(date_format[4]), int(date_format[5]))
    if zone.offset == 5.5:
        b1 = a1 + datetime.timedelta(hours=5,minutes=29) # days, seconds, then other fields.
        added_time=b1.time()
        ad_time=str(added_time).split(":")
    else:
        b1 = a1 + datetime.timedelta(hours=zone.offset) # days, seconds, then other fields.
        added_time=b1.time()
        ad_time=str(added_time).split(":")
        
    t = (int(date_format[0]), int(date_format[1]), int(date_format[2]), int(ad_time[0]), int(ad_time[1]), int(ad_time[2]),0,0,0)
    t = time.mktime(t)
    format1 =date.date_format
    datetime_object=time.strftime(format1+" %I:%M %p", time.gmtime(t))
    return datetime_object