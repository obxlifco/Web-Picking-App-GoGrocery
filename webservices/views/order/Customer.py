from webservices.models import *
from webservices.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
import datetime
import pytz
from rest_framework import generics
from itertools import chain
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from webservices.views import loginview
import sys,os,math
from django.db.models import Q
import traceback
from webservices.views.common import common
class CustomerList(generics.ListAPIView):
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostCustomers.objects.using(company_db).get(pk=pk)
        except EngageboostCustomers.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        company_db = loginview.db_active_connection(request)
        user = self.get_object(pk,request)
        serializer = CustomerSerializer(user)
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

    def put(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        Category = self.get_object(pk,request)
        d1={'modified':datetime.datetime.now(datetime.timezone.utc).astimezone()}
        d2=request.data
        serializer_data=dict(d2,**d1)
        serializer = CustomerSerializer(Category,data=serializer_data,partial=True)
        if serializer.is_valid():
            serializer.save()
            data ={
            'status':1,
            'api_status':pk,
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

class CustomerEdit(generics.ListAPIView):
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostCustomers.objects.using(company_db).get(pk=pk)
        except EngageboostCustomers.DoesNotExist:
            raise Http404

    def get(self, request, customer_id, format=None):
        company_db = loginview.db_active_connection(request)
        user = self.get_object(customer_id,request)
        serializer = CustomerSerializer(user)
        if(serializer): 
            data ={'status':1,'api_status':serializer.data,'message':''}
        else:
            data ={'status':0,'api_status':serializer.errors,'message':'Data Not Found'}
        return Response(data)

class CustomerAdd(generics.ListAPIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        if request.method == 'POST':
            try:
                requestdata = request.data
                first_name = requestdata['first_name']
                last_name = requestdata['last_name']
                fullname = first_name+' '+last_name
                email = requestdata['email']
                hash_password = make_password(requestdata['password'], None, 'md5')
                vat = requestdata['vat']
                customer_group_id = requestdata['customer_group_id']
                company_id = requestdata['company_id']
                created_by = requestdata['createdby']
                modified_by = requestdata['updatedby']
                website_id = requestdata['website_id']
                status = requestdata['status']
                phone = requestdata['phone']
                tin = requestdata['tin']
                vat = requestdata['vat']
                now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
                if requestdata['insert_type'] == "add":                    
                    cnt = EngageboostCustomers.objects.using(company_db).filter(email__iexact=email,isblocked='n',isdeleted='n').count()
                    # cnt = EngageboostUsers.objects.using(company_db).filter(username=fullname,first_name=firstname,email=email,isblocked='n',isdeleted='n').count()
                    if cnt == 0:
                        try:
                            has_user = EngageboostUsers.objects.using(company_db).filter(username=fullname,first_name=first_name,email__iexact=email,isblocked='n',isdeleted='n').first()
                            if has_user:
                                auth_user_id = has_user.id
                            else:
                                # has_user_record = EngageboostUsers.objects.last()
                                # if has_user_record:
                                #     last_entry_of_user = EngageboostUsers.objects.order_by('-id').latest('id')
                                #     row_id = int(last_entry_of_user.id)+int(1)
                                # else:
                                #     row_id = 1
                                User = EngageboostUsers.objects.using(company_db).create(email=email,first_name=first_name,last_name=last_name,company_id=company_id,country_id='1',createdby_id=created_by,created_date=datetime.datetime.now(datetime.timezone.utc).astimezone(),modifiedby_id=modified_by,modified_date=datetime.datetime.now(datetime.timezone.utc).astimezone(),username=fullname,role_id=1,user_type='frontend')
                                    # obj = EngageboostUsers.objects.using(company_db).latest('id')
                                    # last_id = obj.id
                                auth_user_id = User.id

                            # has_Customer_record = EngageboostCustomers.objects.last()
                            # if has_Customer_record:
                            #     last_entry_of_cust = EngageboostCustomers.objects.order_by('-id').latest('id')
                            #     c_id = int(last_entry_of_cust.id)+int(1)
                            # else:
                            #     c_id = 1
                            Customer = EngageboostCustomers.objects.using(company_db).create(email=email,first_name=first_name,last_name=last_name,createdby=created_by,updatedby=modified_by,created=datetime.datetime.now(datetime.timezone.utc).astimezone(),modified=datetime.datetime.now(datetime.timezone.utc).astimezone(),auth_user_id=auth_user_id,vat=vat,phone=phone,ebayusername=fullname,website_id=website_id,group_id=customer_group_id,orders=0,avgorder=0,totalorder=0,lastlogin=datetime.datetime.now(datetime.timezone.utc).astimezone(),is_guest_user=0,is_ledger_created='n',isblocked=status,isdeleted='n')
                            last_inserted_id = Customer.id
                            elastic = common.save_data_to_elastic(last_inserted_id,'EngageboostCustomers')
                            data={'status':1,'last_inserted_id':last_inserted_id,'message':'Customer Created Successfully'}
                        except Exception as error:
                            trace_back = sys.exc_info()[2]
                            line = trace_back.tb_lineno
                            data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error), 'message': str(error)}
                    else:
                        data={'status':0,'api_status':0,'message':'User Already Exists'}
                else:
                    try:
                        has_user = EngageboostCustomers.objects.using(company_db).filter(email__iexact=email,isdeleted='n').first()
                        if has_user:
                            if has_user.id==requestdata['c_id']:
                                Customer = EngageboostCustomers.objects.using(company_db).filter(id=requestdata['c_id']).update(email=email,first_name=first_name,last_name=last_name,updatedby=modified_by,modified=datetime.datetime.now(datetime.timezone.utc).astimezone(),password=hash_password,vat=vat,phone=phone,ebayusername=fullname,website_id=website_id,group_id=customer_group_id,orders=0,avgorder=0,totalorder=0,lastlogin=datetime.datetime.now(datetime.timezone.utc).astimezone(),is_guest_user=0,is_ledger_created='n',isblocked=status,isdeleted='n')
                                last_inserted_id = Customer
                                data={'status':1,'last_inserted_id':last_inserted_id,'message':'Customer Updated Successfully'}
                            else:
                                data={'status':0,'api_status':0,'message':'User Already Exists'}
                        else:
                            Customer = EngageboostCustomers.objects.using(company_db).filter(id=requestdata['c_id']).update(email=email,first_name=first_name,last_name=last_name,updatedby=modified_by,modified=datetime.datetime.now(datetime.timezone.utc).astimezone(),password=hash_password,vat=vat,tin=tin,phone=phone,ebayusername=fullname,website_id=website_id,group_id=customer_group_id,orders=0,avgorder=0,totalorder=0,lastlogin=datetime.datetime.now(datetime.timezone.utc).astimezone(),is_guest_user=0,is_ledger_created='n',isblocked=status,isdeleted='n')
                            last_inserted_id = Customer
                            elastic = common.save_data_to_elastic(last_inserted_id,'EngageboostCustomers')
                            data={'status':1,'last_inserted_id':last_inserted_id,'message':'Customer Updated Successfully'} 
                    except Exception as error:
                        trace_back = sys.exc_info()[2]
                        line = trace_back.tb_lineno
                        data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'message': str(error)}
            except Exception as error:
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                data={'status':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'message': str(error)}

            return Response(data)

class CustomerAddressSetup(generics.ListAPIView):
    # """ List all customers, or create a new customers """
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)                       
        current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
        # cnt = EngageboostCustomers.objects.using(company_db).filter(email=email,isblocked='n',isdeleted='n').count()
        postdata = request.data
        serializer_data={}
        # serializer_data={x:request.POST.get(x) for x in request.POST.keys()}
        serializer_data=request.data
        error = []
        
        if 'customers_id' in serializer_data.keys():
            customers_id = serializer_data['customers_id']
            if 'delivery_name' in serializer_data.keys():
                serializer_data['billing_name']=serializer_data['delivery_name']
            
            if 'delivery_company' in serializer_data.keys():
                serializer_data['billing_company']=serializer_data['delivery_company']
            
            if 'delivery_email_address' in serializer_data.keys():
                serializer_data['billing_email_address']=serializer_data['delivery_email_address']
            else:
                error.append("Add Delivery Name")
            
            if 'delivery_street_address' in serializer_data.keys():
                serializer_data['billing_street_address']=serializer_data['delivery_street_address']    
            # else:
            #     error.append("Add Delivery Street Address")
            
            if 'delivery_street_address1' in serializer_data.keys():
                serializer_data['billing_street_address1']=serializer_data['delivery_street_address1']
            
            if 'delivery_landmark' in serializer_data.keys():
                serializer_data['billing_landmark']=serializer_data['delivery_landmark']
            else:
                error.append("Add Delivery Land Mark")
            
            if 'delivery_city' in serializer_data.keys():
                serializer_data['billing_city']=serializer_data['delivery_city']
            else:
                error.append("Add Delivery City")
            
            if 'delivery_postcode' in serializer_data.keys():
                serializer_data['billing_postcode']=serializer_data['delivery_postcode']
            else:
                error.append("Add Delivery Postcode")
            
            if 'delivery_state' in serializer_data.keys():
                serializer_data['billing_state']=serializer_data['delivery_state']   
            else:
                error.append("Add Delivery State")
            
            if 'delivery_country' in serializer_data.keys():
                serializer_data['billing_country']=serializer_data['delivery_country']
            else:
                error.append("Add Delivery Country")
            
            if 'delivery_phone' in serializer_data.keys():
                serializer_data['billing_phone']=serializer_data['delivery_phone']
            else:
                error.append("Add Delivery Phone No")
            
            if 'delivery_fax' in serializer_data.keys():
                serializer_data['billing_fax']=serializer_data['delivery_fax']    
        else:
           error.append("Select Customer")

        if len(error)==0:   
            if 'id' in serializer_data.keys():
                customersObj = EngageboostCustomersAddressBook.objects.using(company_db).get(id=serializer_data['id'])
                d1={"modified":current_time}
                serializer_data=dict(serializer_data,**d1)
                # return Response(serializer_data)
                serializer = CustomersAddressBookSerializer(customersObj,data=serializer_data,partial=True)
                if serializer.is_valid():
                    serializer.save()

                    if 'set_primary' in serializer_data.keys():
                        if int(serializer_data['set_primary'])==1:
                            EngageboostCustomersAddressBook.objects.using(company_db).filter(customers_id=customers_id).exclude(id=serializer_data['id']).update(set_primary=0)

                    data ={"status":1,"api_status":'Successfully Updated',"message":'Successfully Updated'}
                else:
                    data ={"status":0,"api_status":serializer.errors,"message":'Data Not Found'}
            else:    
                # customers_id = EngageboostCustomersAddressBook.objects.using(company_db).get(id=postdata['id'])
                d1={"created":current_time,"modified":current_time}
                serializer_data=dict(serializer_data,**d1)
                # return Response(serializer_data)
                serializer = CustomersAddressBookSerializer(data=serializer_data,partial=True)
                if serializer.is_valid():
                    serializer.save()

                    if 'set_primary' in serializer_data.keys():
                        if int(serializer_data['set_primary'])==1:
                            obj = EngageboostCustomersAddressBook.objects.using(company_db).latest('id')
                            last_id = obj.id
                            EngageboostCustomersAddressBook.objects.using(company_db).filter(customers_id=customers_id).exclude(id=last_id).update(set_primary=0)

                    data ={"status":1,"api_status":'Successfully Added',"message":'Successfully Added'}
                else:
                    data ={"status":0,"api_status":serializer.errors,"message":'Data Not Found'}
        else:
            data ={"status":0,"api_status":"","message":error}

        return Response(data)

class CustomerAddressFetch(generics.ListAPIView):
    def get(self, request, customer_id, format=None):
        company_db = loginview.db_active_connection(request)
        obj = EngageboostCustomersAddressBook.objects.using(company_db).filter(customers_id = customer_id,isdeleted='n')
        countries = EngageboostCountries.objects.using(company_db).all()
        countries_list = []
        if countries:
            countries = GlobalsettingscountriesSerializer(countries, many=True)
            countries_list = countries.data
        if obj.count()>0:
            user = obj.all()
            if user: 
                serializer = CustomersAddressBookSerializer(user,many=True)
                data ={"status":1,"countrylist":countries_list,"response":serializer.data}
            else:
                data ={"status":0,"countrylist":countries_list,"response":'Address not found'}
        else:
            data ={"status":0,"countrylist":countries_list,"response":'Address not found'}
        return Response(data)

class CustomerAddressDelete(generics.ListAPIView):
    def post(self, request, format=None):
        postdata = request.data
        add_id = postdata['id']
        customer_id = postdata['customer_id']
        company_db = loginview.db_active_connection(request)
        obj = EngageboostCustomersAddressBook.objects.using(company_db).filter(id = add_id,isdeleted='n')
        
        if obj.count()>0:
            user = obj.delete()
            addObj = EngageboostCustomersAddressBook.objects.using(company_db).filter(customers_id = customer_id,isdeleted='n')
            
            if addObj.count()>0:
                primaryCount = addObj.filter(set_primary=1).count()

                if primaryCount==0:
                    firstObj = addObj.first()
                    EngageboostCustomersAddressBook.objects.using(company_db).filter(id=firstObj.id).update(set_primary=1)

            data ={"status":1,"response":'Address deleted'}
        else:
            data ={"status":0,"response":'Address not found'}
        return Response(data)        

class CustomerAddressSetPrimary(generics.ListAPIView):
    def post(self, request, format=None):
        postdata = request.data
        add_id = postdata['id']
        customer_id = postdata['customer_id']
        company_db = loginview.db_active_connection(request)
        obj = EngageboostCustomersAddressBook.objects.using(company_db).filter(id = add_id,isdeleted='n')
        # print(obj.all().query)
        if obj.count()>0:
            user = obj.update(set_primary=1)
            EngageboostCustomersAddressBook.objects.using(company_db).filter(customers_id=customer_id,isdeleted='n').exclude(id = add_id).update(set_primary=0)
            data ={"status":1,"response":'Address set as primary'}
        else:
            data ={"status":0,"response":'Address not found'}
        return Response(data)

class CustomerOrderList(generics.ListAPIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        postdata = request.data
        pre_data={}
        #********* Start Grid Headings *********#
        row_dict={}
        row=[]
        module='CustomerOrderList'
        screen_name='list-custom'
        layout_fetch=EngageboostGridLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
        layout_header=layout_fetch.header_name.split("@@")
        layout_field=layout_fetch.field_name.split("@@")
        layout_check=EngageboostGridColumnLayouts.objects.using(company_db).filter(module=module,screen_name=screen_name).count()
        layout={}
        layout_arr=[]
        for header,field in zip(layout_header,layout_field):
            ex_layout_field=field.split(".")
            is_numeric_field=field.split("#")
            field_name=ex_layout_field[0]
            if len(is_numeric_field)>1:
                field_type=is_numeric_field[1]
                field_name=is_numeric_field[0]
            else:
                field_type=''
            if len(ex_layout_field)>1:
                child_name=ex_layout_field[1]
                field_name=ex_layout_field[0]
            else:
                child_name=''
            if(layout_check):
                layout_column_fetch=EngageboostGridColumnLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
                layout_column_header=layout_column_fetch.header_name
                layout_column_field=layout_column_fetch.field_name
                if header in layout_column_header:
                    status=1
                else:
                    status=0
            else:
                status=1
            layout={"title":header,"field":field_name,"child":child_name,"show":status,"field_type":field_type}
            layout_arr.append(layout)
        #********* End Grid Headings *********#
        order_data = EngageboostOrdermaster.objects.using(company_db).filter(isdeleted='n',customer_id=postdata["customer_id"])
        if request.data.get('search'):
            search_cond = request.data.get('search')
            order_data = order_data.filter(Q(custom_order_id__icontains = search_cond) | Q(billing_name__icontains = search_cond) | Q(billing_email_address__icontains = search_cond))
        if request.data.get('order_by'):
            order_by=request.data.get('order_by');
            order_type=request.data.get('order_type')
            order=order_by if order_type=='+' else '-'+order_by
            order_data = order_data.order_by(order)
        if order_data.count() > 0:
            page = order_data.all()
            OrderMasterDetails = OrderMasterSerializer(page, many=True)
            pre_data['all']=len(OrderMasterDetails.data)
            pre_data['result']=OrderMasterDetails.data
            pre_data['layout']=layout_arr
            # pre_data['role_permission']=role_permission
        else:
            pre_data['all']=0
            pre_data['result']=[]
            pre_data['layout']=layout_arr
            # data ={"status":0,"response":'No Order Found'}
        customer_orderlist_data = self_pagination(pre_data)
        return Response(customer_orderlist_data)

class CustomerInvoiceList(generics.ListAPIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        postdata = request.data
        pre_data={}

        #********* Start Grid Headings *********#
        row_dict={}
        row=[]
        module='CustomerInvoiceList'
        screen_name='list-custom'
        layout_fetch=EngageboostGridLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
        layout_header=layout_fetch.header_name.split("@@")
        layout_field=layout_fetch.field_name.split("@@")
        layout_check=EngageboostGridColumnLayouts.objects.using(company_db).filter(module=module,screen_name=screen_name).count()
        layout={}
        layout_arr=[]

        for header,field in zip(layout_header,layout_field):
            ex_layout_field=field.split(".")
            is_numeric_field=field.split("#")
            field_name=ex_layout_field[0]
            
            if len(is_numeric_field)>1:
                field_type=is_numeric_field[1]
                field_name=is_numeric_field[0]
            else:
                field_type=''   

            if len(ex_layout_field)>1:
                child_name=ex_layout_field[1]
                field_name=ex_layout_field[0]
            else:
                child_name=''            

            if(layout_check):
                layout_column_fetch=EngageboostGridColumnLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
                layout_column_header=layout_column_fetch.header_name
                layout_column_field=layout_column_fetch.field_name

                if header in layout_column_header:
                    status=1
                else:
                    status=0
            else:
                status=1        
            layout={"title":header,"field":field_name,"child":child_name,"show":status,"field_type":field_type}
            layout_arr.append(layout)
        #********* End Grid Headings *********#
        if request.data.get('order_by'):
            order_by=request.data.get('order_by');order_type=request.data.get('order_type')
            order=order_by if order_type=='+' else '-'+order_by

        if request.data.get('search'):
            search_cond = request.data.get('search')
            if request.data.get('order_by'):
                order_by=request.data.get('order_by');order_type=request.data.get('order_type')
                order=order_by if order_type=='+' else '-'+order_by
                cond = EngageboostInvoicemaster.objects.using(company_db).all().order_by(order).filter(customer_id=postdata["customer_id"]).filter(Q(custom_order_id__icontains = search_cond) | Q(custom_invoice_id__icontains = search_cond))
            else:
                cond = EngageboostInvoicemaster.objects.using(company_db).all().filter(customer_id=postdata["customer_id"]).filter(Q(custom_order_id__icontains = search_cond) | Q(custom_invoice_id__icontains = search_cond))
        else:
            if request.data.get('order_by'):
                order_by=request.data.get('order_by');order_type=request.data.get('order_type')
                order=order_by if order_type=='+' else '-'+order_by
                cond = EngageboostInvoicemaster.objects.using(company_db).all().order_by(order).filter(customer_id=postdata["customer_id"]) 
            else:
                cond = EngageboostInvoicemaster.objects.using(company_db).all().filter(customer_id=postdata["customer_id"])   


        if cond: 
            InvoiceMasterDetails = InvoicemasterSerializer(cond,many=True)
            # data ={"status":1,"response":OrderMasterDetails.data}
            pre_data['all']=len(InvoiceMasterDetails.data)
            pre_data['result']=InvoiceMasterDetails.data
            pre_data['layout']=layout_arr
            # pre_data['role_permission']=role_permission
        else:
            pre_data['all']=0
            pre_data['result']=[]
            pre_data['layout']=layout_arr
            # data ={"status":0,"response":'No Order Found'}

        customer_invoicelist_data = self_pagination(pre_data)
        return Response(customer_invoicelist_data)

def get_page_size():
    settings = EngageboostGlobalSettings.objects.get(isdeleted='n',isblocked='n',website_id=1)
    size=settings.itemlisting_backend
    return size 

def self_pagination(array_list):
    results_arr=[]
    page_size = get_page_size()
    length_of_list = len(array_list['result'])
    results_arr.append(array_list)
    result = {"count":length_of_list,"per_page_count": math.ceil(length_of_list/page_size),"page_size":page_size,"results":results_arr}
    return result