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
from webservices.views import loginview

class Emailnotification(generics.ListAPIView):
# """ Add New Auto Responder(Email Notification) d1 and d2 is variable to store custom values and request values and dict is use to combine them"""
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        d1={'created':datetime.now().date(),'modified':datetime.now().date()}
        d2=request.data
        channels=request.data['channels']
        warehouse=request.data['warehouse']
        shipping=request.data['shipping']
        serializer_data=dict(d2,**d1)
        serializer = EmailTypeContentsSerializer(data=serializer_data,partial=True)
        
        if serializer.is_valid():
            serializer.save()
            # serializer_data_copy = serializer_data
            # serializer_data_copy.pop("emailId");serializer_data_copy.pop("channels")
            # serializer_data_copy.pop("applicable_email_channel")
            # serializer_data_copy.pop("warehouse");serializer_data_copy.pop("shipping")
            # EngageboostEmailTypeContents.objects.using(company_db).create(**serializer_data_copy)
            obj = EngageboostEmailTypeContents.objects.using(company_db).latest('id')
            last_id = obj.id
            channels_array=channels.split(",")
            warehouse_array=warehouse.split(",")
            shipping_array=shipping.split(",")
            if channels !="":
                for data in channels_array:
                    data1=str(data)
                    EngageboostApplicableAutoresponders.objects.using(company_db).create(website_id=request.data['website_id'],auto_responder_id=last_id,applicable_chanel_id=data1,applicable_for='Channel',shipment_status=request.data['shipment_status'],created=datetime.now().date(),modified=datetime.now().date(),createdby=request.data['createdby'],ip_address=request.data['ip_address'],updatedby=request.data['updatedby'])
            if warehouse!="":
                for data2 in warehouse_array:
                    EngageboostApplicableAutoresponders.objects.using(company_db).create(website_id=request.data['website_id'],auto_responder_id=last_id,applicable_chanel_id=data2,applicable_for='Warehouse',shipment_status=request.data['shipment_status'],created=datetime.now().date(),modified=datetime.now().date(),createdby=request.data['createdby'],ip_address=request.data['ip_address'],updatedby=request.data['updatedby'])
            if shipping !="":       
                for data3 in shipping_array:
                    data4=str(data3)
                    EngageboostApplicableAutoresponders.objects.using(company_db).create(website_id=request.data['website_id'],auto_responder_id=last_id,applicable_chanel_id=data4,applicable_for='ShippingProvider',shipment_status=request.data['shipment_status'],created=datetime.now().date(),modified=datetime.now().date(),createdby=request.data['createdby'],ip_address=request.data['ip_address'],updatedby=request.data['updatedby'])
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
                       
class EmailnotificationList(generics.ListAPIView):
# """ List single row for Auto Responder(Email Notification) """
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostEmailTypeContents.objects.using(company_db).get(pk=pk)
        except EngageboostEmailTypeContents.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        arr_channel=[]
        arr_warehouse=[]
        arr_shippingprovider=[]
        user = self.get_object(pk,request)
        serializer = EmailTypeContentsSerializer(user)
        data7 = EngageboostChannels.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
        serializer7 = ChannelsSerializer(data7, many=True)
        data8 = EngageboostShippingMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
        serializer8 = ShippingSerializer(data8, many=True)
        data9 = EngageboostWarehouseMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
        serializer9 = WarehousemastersSerializer(data9, many=True)
        channel_id = EngageboostApplicableAutoresponders.objects.using(company_db).all().filter(auto_responder_id=pk,applicable_for='Channel')
        warehouse_id = EngageboostApplicableAutoresponders.objects.using(company_db).all().filter(auto_responder_id=pk,applicable_for='Warehouse')
        shippingprovider_id = EngageboostApplicableAutoresponders.objects.using(company_db).all().filter(auto_responder_id=pk,applicable_for='ShippingProvider')
        for channel in channel_id:
            arr_channel.append(channel.applicable_chanel_id)
        for warehouse in warehouse_id:
            arr_warehouse.append(warehouse.applicable_chanel_id)
        for shippingprovider in shippingprovider_id:
            arr_shippingprovider.append(shippingprovider.applicable_chanel_id)    
        if(serializer): 
            data ={
                'status':1,
                'api_status':serializer.data,
                'channels':serializer7.data,
                'shipping':serializer8.data,
                'WarehouseMasters':serializer9.data,
                'selected_channel':arr_channel,
                'selected_warehouse':arr_warehouse,
                'selected_shippingprovider':arr_shippingprovider,
                
                'message':'',
                }
        else:
            data ={
                'status':0,
                'api_status':serializer.errors,
                'message':'Data Not Found',
                }
        return HttpResponse(json.dumps({"data":data,'product_label':product_label(),'customer_label':customer_label(),'order_label':order_label()}), content_type='application/json')
    # """Update  rows for Auto Responder(Email Notification) d1 and d2 is variable to store custom values and request values and dict is use to combine them"""
    def put(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        Category = self.get_object(pk,request)
        d1={'modified':datetime.now().date()}
        d2=request.data
        channels=request.data['channels']
        warehouse=request.data['warehouse']
        shipping=request.data['shipping']
        serializer_data=dict(d2,**d1)
        serializer = EmailTypeContentsSerializer(Category,data=serializer_data,partial=True)
        if serializer.is_valid():
            serializer.save()
            obj = EngageboostApplicableAutoresponders.objects.using(company_db).filter(auto_responder_id=pk).delete()
            
            channels_array=channels.split(",")
            warehouse_array=warehouse.split(",")
            shipping_array=shipping.split(",")
            if channels !="":
                for data in channels_array:
                    data1=str(data)
                    EngageboostApplicableAutoresponders.objects.using(company_db).create(website_id=request.data['website_id'],auto_responder_id=pk,applicable_chanel_id=data1,applicable_for='Channel',shipment_status=request.data['shipment_status'],created=datetime.now().date(),modified=datetime.now().date(),createdby=request.data['createdby'],ip_address=request.data['ip_address'],updatedby=request.data['updatedby'])
            if warehouse!="":
                for data2 in warehouse_array:
                    EngageboostApplicableAutoresponders.objects.using(company_db).create(website_id=request.data['website_id'],auto_responder_id=pk,applicable_chanel_id=data2,applicable_for='Warehouse',shipment_status=request.data['shipment_status'],created=datetime.now().date(),modified=datetime.now().date(),createdby=request.data['createdby'],ip_address=request.data['ip_address'],updatedby=request.data['updatedby'])
            if shipping !="":       
                for data3 in shipping_array:
                    data4=str(data3)
                    EngageboostApplicableAutoresponders.objects.using(company_db).create(website_id=request.data['website_id'],auto_responder_id=pk,applicable_chanel_id=data4,applicable_for='ShippingProvider',shipment_status=request.data['shipment_status'],created=datetime.now().date(),modified=datetime.now().date(),createdby=request.data['createdby'],ip_address=request.data['ip_address'],updatedby=request.data['updatedby'])
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

class AutoresponderViewSet(generics.ListAPIView):
    # """Channels,ShippingMasters,WarehouseMasters web services load for Email Notification  """
    def get(self, request, format=None): 
        company_db = loginview.db_active_connection(request)
        data={}
        
        data7 = EngageboostChannels.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
        serializer7 = ChannelsSerializer(data7, many=True)
        data8 = EngageboostShippingMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
        serializer8 = ShippingSerializer(data8, many=True)
        data9 = EngageboostWarehouseMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
        serializer9 = WarehousemastersSerializer(data9, many=True)

        data['channels']=serializer7.data
        data['Shipping']=serializer8.data
        data['warehouse']=serializer9.data
        
        return HttpResponse(json.dumps({"data":data,'product_label':product_label(),'customer_label':customer_label(),'order_label':order_label()}), content_type='application/json')
        

def product_label():
    product_array=[]
    product ={"product":[{'label':'Product Name','value':'{@name}'},{'label':'Gross Weight','value':'{@weight}'},{'label':'SKU','value':'{@sku}'},{'label':'Price','value':'{@default_price}'}]}
    return product['product']

def customer_label():
    customer_array=[]
    customer ={"customer":[{'label':'First Name','value':'{@first_name}'},{'label':'Email','value':'{@email}'},{'label':'VAT','value':'{@VAT}'},{'label':'Last Name','value':'{@last_name}'},{'label':'Status','value':'{@status}'},{'label':'Password','value':'{@password}'}]}
    return customer['customer']

def order_label():
    order_array=[]
    order ={"order":[{'label':'Order Number','value':'{@custom_order_id}'},{'label':'Invoice Number','value':'{@custom_invoice_id}'},{'label':'Customer Name','value':'{@customer_name}'},{'label':'Payment Method','value':'{@payment_method_name}'},{'label':'Status','value':'{@status}'},{'label':'Shipping Method','value':'{@shipping_method_name}'},{'label':'Billing Name','value':'{@billing_name}'},{'label':'Billing Company','value':'{@billing_company}'},{'label':'Billing Email Address','value':'{@billing_email_address}'},{'label':'Billing Address','value':'{@billing_street_address}'},{'label':'Billing City','value':'{@billing_city}'},{'label':'Billing Zip Code','value':'{@billing_postcode}'},{'label':'Billing Status','value':'{@billing_state}'},{'label':'Billing Country','value':'{@billing_country_name}'},{'label':'Billing Phone','value':'{@billing_phone}'},{'label':'Billing Mobile No','value':'{@billing_fax}'},{'label':'Shipping Name','value':'{@delivery_name}'},{'label':'Shipping Company','value':'{@delivery_company}'},{'label':'Shipping Email Address','value':'{@delivery_email_address}'},{'label':'Shipping Address','value':'{@delivery_street_address}'},{'label':'Shipping City','value':'{@delivery_city}'},{'label':'Shipping Zip Code','value':'{@delivery_postcode}'},{'label':'Shipping State','value':'{@delivery_state}'},{'label':'Shipping Country','value':'{@delivery_country_name}'},{'label':'Shipping Phone','value':'{@delivery_phone}'},{'label':'Order Net Amount','value':'{@net_amount}'},{'label':'Tax Amount','value':'{@tax_amount}'},{'label':'Excise Duty','value':'{@excise_duty}'},{'label':'Order Gross Amount','value':'{@gross_amount}'},{'label':'Shipping Amount','value':'{@shipping_cost}'},{'label':'COD Change','value':'{@cod_charge}'},{'label':'Discount Amount','value':'{@gross_discount_amount}'},{'label':'Order Currency','value':'{@currency_code}'},{'label':'Order Date','value':'{@created}'},{'label':'Tracking No','value':'{@tracking_no}'},{'label':'Tracking Company Name','value':'{@tracking_company_name}'},{'label':'Tracking Url','value':'{@tracking_url}'},{'label':'Tracking ID','value':'{@txnTranID}'},{'label':'Total','value':'{@total_amt}'},{'label':'Routing Codes','value':'{@routing_code}'},{'label':'Pieces','value':'{@total_quantity}'},{'label':'Actual Weight','value':'{@weight}'},{'label':'Package Dimension','value':'{@dimension}'}]}
    return order['order']