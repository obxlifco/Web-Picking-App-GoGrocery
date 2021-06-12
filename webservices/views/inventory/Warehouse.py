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
from django.http import HttpResponse
import json
from django.db.models import Q
from webservices.views import loginview
from webservices.views.common import common
from webservices.views.inventory.threading import *
import sys
from elasticsearch import Elasticsearch
from webservices.views.emailcomponent import emailcomponent
from elasticsearch import helpers
import traceback

class Warehouse(generics.ListAPIView):
# """ Create  Warehouse"""
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        d1={'created':datetime.now().date(),'modified':datetime.now().date()}
        d2=request.data

        address = d2['address']
        city = d2['city']
        country = d2['country_id']
        state = d2['state_id']
        lat_val = d2['latitude']
        long_val = d2['longitude']

        store_category_type = d2['store_category_type']
        store_category = d2['store_category']
        payment_option = d2['payment_option']
        expected_delivery_time = d2['expected_delivery_time']
        # Requir validation
        # geo_location = common.get_geo_location_uae(address,city,country,state, None)
        # d1={'modified':datetime.now().date(), 'latitude':geo_location['lat'], 'longitude':geo_location['lng']}
        d1={'modified':datetime.now().date(), 'latitude':lat_val, 'longitude':long_val}

        serializer_data=dict(d2,**d1)
        cnt_name = EngageboostWarehouseMasters.objects.using(company_db).filter(name=request.data['name']).filter(isdeleted='n',isblocked='n').count()
        if  cnt_name == 0:
            serializer = WarehousemastersSerializer(data=serializer_data,partial=True)
            if serializer.is_valid():
                serializer.save()
                obj = EngageboostWarehouseMasters.objects.using(company_db).latest('id')
                last_id = obj.id
                # Update stock for all product for this warehouse
                # UpadateStock(last_id)
                UpadateStockTest(last_id)
                # UpadateCategoryWarehouse(last_id)
                d4=request.data
                applicable_channel_id=d4['applicable_channel_id']
                menu_group=applicable_channel_id.split(",")
                applicable_country_id=d4['applicable_country_id']
                country=applicable_country_id.split(",")
                manager_id=d4['manager_id']
                manager_id1=manager_id.split(",")
                cashier_id = ''
                if 'cashier_id' in request.data:
                    cashier_id=d4['cashier_id']
                    cashier_id1=cashier_id.split(",")

                if applicable_channel_id !="":
                    for data in menu_group:
                        data1=str(data)
                        EngageboostWarehouseMasterApplicableChannels.objects.using(company_db).create(warehouse_master_id=last_id,applicable_channel_id=data1)
                if manager_id!="":
                    for data2 in manager_id1:
                        EngageboostWarehouseManager.objects.using(company_db).create(warehouse_id=last_id,manager_id=data2,role="Warehouse Manager",created_date=datetime.now().date())

                if 'cashier_id' in request.data and cashier_id != "":
                    for data3 in cashier_id1:
                        EngageboostWarehouseManager.objects.using(company_db).create(warehouse_id=last_id,manager_id=data3,role="Cashier",created_date=datetime.now().date())

                if applicable_country_id !="":       
                    for data3 in country:
                        data4=str(data3)
                        EngageboostWarehouseMasterApplicableRegions.objects.using(company_db).create(ware_house_master_id=last_id,applicable_country_id=data4,applicable_state_id=1)
                

                if len(store_category)>0:
                    print('count is more')
                    for cat in store_category:
                        
                        checkParent = EngageboostCategoryMasters.objects.filter(isdeleted='n',parent_id=cat)
                        if checkParent.count()==0:
                            catprod = EngageboostProductCategories.objects.filter(category_id = cat,product_id__isdeleted='n')
                            if catprod.count()>0:
                                catprod = catprod.distinct("product_id").values_list("product_id",flat=True)
                                product_id_list = list(catprod)
                                # print(product_id_list)
                                prostock = EngageboostProductStocks.objects.filter(warehouse_id = last_id,product_id__in=product_id_list,real_stock__gt=0).count()
                            else:
                                prostock = 0
                            
                        else:
                            prostock = 1

                        EngageboostCategoryWarehouse.objects.create(category_id=cat,
                                                                    warehouse_id=last_id,
                                                                    created=datetime.now(),
                                                                    modified=datetime.now(),
                                                                    product_count=prostock)

                if len(store_category_type)>0:
                    for store_type in store_category_type:
                        EngageboostStoreType.objects.create(type_id=store_type,
                                                            warehouse_id=last_id,
                                                            created=datetime.now(),
                                                            modified=datetime.now())


                if len(payment_option)>0:
                    for pay_option in payment_option:
                        EngageboostPaymentWarehouse.objects.create(payment_method_id=pay_option,
                                                                    warehouse_id=last_id,
                                                                    created=datetime.now(),
                                                                    modified=datetime.now())

                #all_p=EngageboostProducts.objects.using(company_db).all().filter(isdeleted='n')
                # for all_pr in all_p:
                #     procuctinfo=EngageboostProductStocks.objects.using(company_db).create(stock=0,safety_stock=0,avg_sales_week=0,avg_sales_month=0,stock_unit=0,product_id=all_pr.id,warehouse_id=last_id,created=datetime.now(),modified=datetime.now(),isdeleted='n',isblocked='n',real_stock=0) 

                data ={
                'status':1,
                'api_status':'',
                'message':'Successfully Inserted',
                }
            return Response(data)
        else:
            data ={
            'status':0,
            'message':'Warehouse Master Name is already exists',
            }
            return Response(data)

class WarehouseList(generics.ListAPIView):
# """ List all Warehouse """
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostWarehouseMasters.objects.using(company_db).get(pk=pk)
        except EngageboostWarehouseMasters.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        user = self.get_object(pk,request)
        serializer = WarehousemastersSerializer(user)
        arr=[]
        Conditions_list1 = EngageboostWarehouseMasterApplicableRegions.objects.using(company_db).all().filter(ware_house_master_id=pk)   
        for c1 in Conditions_list1:
            # print(c1.name)
            arr.append(c1.applicable_country_id)
            Conditions_list = EngageboostCountries.objects.using(company_db).all().filter(isdeleted='n',
                                                                                          isblocked='n').order_by('country_name')
        arr2=[]
        for c2 in Conditions_list:
            if c2.id in arr:
                d2={"id":c2.id,"country_name":c2.country_name,"status":1}
            else:
                d2={"id":c2.id,"country_name":c2.country_name,"status":0}
            arr2.append(d2)
        arr_selected_other=[]
        Conditions_list15 = EngageboostWarehouseMasterApplicableChannels.objects.using(company_db).all().filter(~Q(warehouse_master_id=pk)).filter(isdeleted='n',isblocked='n')   
        for c15 in Conditions_list15:
            arr_selected_other.append(c15.applicable_channel_id)
            
        arr3=[]
        Conditions_list5 = EngageboostWarehouseMasterApplicableChannels.objects.using(company_db).all().filter(warehouse_master_id=pk).filter(isdeleted='n',isblocked='n')   
        for c5 in Conditions_list5:
            arr3.append(c5.applicable_channel_id)

        Conditions_list7 = EngageboostChannels.objects.using(company_db).all().filter(~Q(id__in=arr_selected_other),
                                                                                      isdeleted='n',
                                                                                      isblocked='n').order_by('name')


        warehouse_category = EngageboostCategoryWarehouse.objects.filter(warehouse_id=pk, isblocked='n', isdeleted='n')
        ware_cat = EngageboostCategoryWarehouseSerializer(warehouse_category, many=True)

        store_type = EngageboostStoreType.objects.filter(warehouse_id=pk, isblocked='n', isdeleted='n')
        stor_type = EngageboostStoreTypeSerializer(store_type, many=True)

        payment_option = EngageboostPaymentWarehouse.objects.filter(warehouse_id=pk, isblocked='n', isdeleted='n')
        pay_type = EngageboostPaymentWarehouseSerializer(payment_option, many=True)


        arr4=[]
        for c7 in Conditions_list7:
            if c7.id in arr3:
                d3={"id":c7.id,"name":c7.name,"status":1}
            else:
                d3={"id":c7.id,"name":c7.name,"status":0}
            arr4.append(d3)
        arr6=[]
        Conditions_list5 = EngageboostWarehouseManager.objects.using(company_db).all().filter(warehouse_id=pk)
        # Conditions_list9 = {}
        if Conditions_list5:
            for c5 in Conditions_list5:
                arr6.append(c5.manager_id)
                # print(arr3)
        
        Conditions_list9 = EngageboostUsers.objects.using(company_db).all().filter(isdeleted='n', isblocked='n',
                                                                                       user_type='backend').order_by('username')
        arr8=[]
        if Conditions_list9:
            for c9 in Conditions_list9:
                if c9.id in arr6:
                    d4={"id":c9.id,"username":c9.username,"first_name":c9.first_name,"last_name":c9.last_name,"status":1}
                else:
                    d4={"id":c9.id,"username":c9.username,"first_name":c9.first_name,"last_name":c9.last_name,"status":0}
                
                arr8.append(d4)
        # return HttpResponse(json.dumps({"warehouse": serializer.data,"countries":arr2,"channel":arr4,"users":arr8}), content_type='application/json')
        return HttpResponse(json.dumps(
            {"warehouse": serializer.data, "countries": arr2, "channel": arr4, "users": arr8,
             "warehouse_category": ware_cat.data, "store_type": stor_type.data, 'payment_option': pay_type.data}),
                            content_type='application/json')
   # """ Update single Warehouse """
    def put(self, request,pk,format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        warehouse = self.get_object(pk,request)
        # d1={'modified':datetime.now().date()}
        d2=request.data
        address = d2['address']
        city = d2['city']
        country = d2['country_id']
        state = d2['state_id']
        lat_val = d2['latitude']
        long_val = d2['longitude']

        store_category_type = d2['store_category_type']
        store_category = d2['store_category']
        payment_option = d2['payment_option']
        expected_delivery_time = d2['expected_delivery_time']
        min_order_amount =0
        if "min_order_amount" in d2:
            min_order_amount = d2['min_order_amount']
        else:
            d2['min_order_amount'] = 0
        # Requir validation
        # geo_location = common.get_geo_location_uae(address,city,country,state, None)
        # lat_val = None
        # long_val = None
        # if geo_location:
        #     lat_val = geo_location['lat']
        #     long_val = geo_location['lng']
        if lat_val is not None and long_val is not None:
            d1={'modified':datetime.now().date(), 'latitude':lat_val, 'longitude':long_val}
        else:
            d1={'modified':datetime.now().date()}

        serializer_data=dict(d2,**d1)
        cnt_name = EngageboostWarehouseMasters.objects.using(company_db).filter(name=request.data['name']).filter(~Q(id=pk)).count()
        if  cnt_name == 0:
            serializer = WarehousemastersSerializer(warehouse,data=serializer_data,partial=True)
            if serializer.is_valid():
                serializer.save()
                # UpadateStock(pk)
                d4=request.data
                applicable_channel_id=d4['applicable_channel_id']
                menu_group=applicable_channel_id.split(",")
                applicable_country_id=d4['applicable_country_id']
                country=applicable_country_id.split(",")
                manager_id=d4['manager_id']
                manager_id1=manager_id.split(",")
                cashier_id = ''
                if 'cashier_id' in request.data:
                    cashier_id = d4['cashier_id']
                    cashier_id1=cashier_id.split(",")

                EngageboostWarehouseMasterApplicableChannels.objects.using(company_db).filter(warehouse_master_id=pk).delete()
                EngageboostWarehouseManager.objects.using(company_db).filter(warehouse_id=pk).delete()
                EngageboostWarehouseMasterApplicableRegions.objects.using(company_db).filter(ware_house_master_id=pk).delete()
                if applicable_channel_id !="":
                    for data in menu_group:
                        data1=str(data)
                        EngageboostWarehouseMasterApplicableChannels.objects.using(company_db).create(warehouse_master_id=pk,applicable_channel_id=data1)
                if manager_id !="":
                    for data2 in manager_id1:
                        EngageboostWarehouseManager.objects.using(company_db).create(warehouse_id=pk,manager_id=data2,role="Warehouse Manager",created_date=datetime.now().date())
                
                if 'cashier_id' in request.data and cashier_id != "":
                    for data3 in cashier_id1:
                        EngageboostWarehouseManager.objects.using(company_db).create(warehouse_id=pk,manager_id=data3,role="Cashier",created_date=datetime.now().date())
                
                if applicable_country_id !="":       
                    for data3 in country:
                        data4=str(data3)
                        EngageboostWarehouseMasterApplicableRegions.objects.using(company_db).create(ware_house_master_id=pk,applicable_country_id=data4,applicable_state_id=1)


                if len(store_category)>0:
                    for cat in store_category:
                        
                        checkParent = EngageboostCategoryMasters.objects.filter(isdeleted='n',parent_id=cat)
                        if checkParent.count()==0:
                            catprod = EngageboostProductCategories.objects.filter(category_id = cat,product_id__isdeleted='n')
                            if catprod.count()>0:
                                catprod = catprod.distinct("product_id").values_list("product_id",flat=True)
                                product_id_list = list(catprod)
                                # print(product_id_list)
                                prostock = EngageboostProductStocks.objects.filter(warehouse_id = pk,product_id__in=product_id_list,real_stock__gt=0).count()
                            else:
                                prostock = 0
                            
                        else:
                            prostock = 1

                        cat_warObj = EngageboostCategoryWarehouse.objects.filter(warehouse_id=pk, category_id=cat)    
                        if cat_warObj.count()==0:
                            EngageboostCategoryWarehouse.objects.create(category_id=cat,warehouse_id=pk,created=datetime.now(), modified=datetime.now(),product_count=prostock)
                        else:
                            cat_warObj.update(modified=datetime.now(),product_count=prostock,isdeleted='n')
                        # EngageboostCategoryWarehouse.objects.get_or_create(category_id=cat,
                        #                                             warehouse_id=pk,
                        #                                             defaults = {'created':datetime.now(), 'modified':datetime.now(),'product_count':prostock})

                    EngageboostCategoryWarehouse.objects.filter(warehouse_id=pk).exclude(category_id__in=store_category).update(isdeleted='y',product_count=0)
                    # EngageboostCategoryWarehouse.objects.filter(warehouse_id=pk, category_id__in=store_category).update(isdeleted='n',product_count=prostock)
                else:
                    EngageboostCategoryWarehouse.objects.filter(warehouse_id=pk).update(isdeleted='y', product_count=0)


                if len(store_category_type)>0:
                    for store_type in store_category_type:
                        EngageboostStoreType.objects.get_or_create(type_id=store_type,
                                                            warehouse_id=pk,
                                                            defaults={'created': datetime.now(),
                                                                             'modified': datetime.now()})

                    EngageboostStoreType.objects.filter(warehouse_id=pk).exclude(type_id__in=store_category_type).update(isdeleted='y')
                    EngageboostStoreType.objects.filter(warehouse_id=pk, type_id__in=store_category_type).update(isdeleted='n')
                else:
                    EngageboostStoreType.objects.filter(warehouse_id=pk).update(isdeleted='y')



                    # for pay_option in payment_option:
                    #     EngageboostPaymentWarehouse.objects.create(payment_method_id=pay_option,
                    #                                                 warehouse_id=last_id,
                    #                                                 created=datetime.now(),
                    #                                                 modified=datetime.now())
                if len(payment_option)>0:
                    for pay_option in payment_option:
                        EngageboostPaymentWarehouse.objects.get_or_create(payment_method_id=pay_option,
                                                                        warehouse_id=pk,
                                                                        defaults={'created': datetime.now(),
                                                                                 'modified': datetime.now()})

                    EngageboostPaymentWarehouse.objects.filter(warehouse_id=pk).exclude(payment_method_id__in=payment_option).update(isdeleted='y')
                    EngageboostPaymentWarehouse.objects.filter(warehouse_id=pk, payment_method_id__in=payment_option).update(isdeleted='n')
                else:
                    EngageboostPaymentWarehouse.objects.filter(warehouse_id=pk).update(isdeleted='y')


                data ={
                    'status':1,
                    'api_status':'',
                    'message':'Successfully Updated',
                }
            else:
                 data ={
                    'status':1,
                    'api_status':serializer.errors,
                }    
            return Response(data)
        else:
            data ={
            'status':0,
            'message':'Warehouse Master Name is already exists',
            }
            return Response(data)
      # """ Load of all web services for  Warehouse """            
class WarehouseAllList(generics.ListAPIView):
    def get(self, request, format=None,partial=True):
        company_db = loginview.db_active_connection(request)

        warehouse = EngageboostWarehouseMasters.objects.using(company_db).all().filter(isdeleted='n',isblocked='n').order_by('-id')
        serializer_warehouse = WarehousemastersSerializer(warehouse, many=True)

        settings1 = EngageboostCountries.objects.using(company_db).all().filter(country_name='India')
        serializer1 = GlobalsettingscountriesSerializer(settings1, many=True)
        settings = EngageboostCountries.objects.using(company_db).all().filter(~Q(country_name='India')).order_by('country_name')
        serializer = GlobalsettingscountriesSerializer(settings, many=True)
        d1=serializer1.data
        d2 = serializer.data
        
        data=d1+d2
        
        settings3 = EngageboostUsers.objects.using(company_db).all().filter(isdeleted='n',isblocked='n',user_type='backend')
        serializer3 = UserSerializer(settings3, many=True)
       
        settings5 = EngageboostStates.objects.using(company_db).order_by('state_name')
        serializer5 = StatesSerializer(settings5, many=True)
        channel_ids  = EngageboostWarehouseMasterApplicableChannels.objects.using(company_db).all().filter(isdeleted='n',isblocked='n')
        arr=[]
        for channel_id in channel_ids:
            arr.append(channel_id.applicable_channel_id)
            
        settings4 = EngageboostChannels.objects.using(company_db).all().filter(~Q(id__in=arr)).filter(isdeleted='n',isblocked='n')
        serializer4 = ChannelsSerializer(settings4, many=True)
        if(serializer_warehouse): 
            data ={
                'status':1,
                'countries':data,
                'users':serializer3.data,
                'channel':serializer4.data,
                'State':serializer5.data,
                'warehouse':serializer_warehouse.data,
            }
        else:
            data ={
            'status':0,
            'api_status':serializer.errors,
            'message':'Data Not Found',
        }
        return Response(data)

@postpone
def UpadateStock(warehouse_id=None):
    if warehouse_id is not None:
        rs_stock_product = EngageboostProducts.objects.filter(isblocked = 'n', isdeleted='n').order_by('id').values_list('id', flat=True).iterator()
        rs_stock_product = list(set(rs_stock_product))
        for product_id in rs_stock_product:
            rs_check = EngageboostProductStocks.objects.filter(isblocked = 'n', isdeleted='n', product_id = product_id, warehouse_id=warehouse_id).count()
            if rs_check>0:
                # product_stock = common.get_product_stock(product_id)
                # elastic = common.change_field_value_elastic(product_id,'EngageboostProducts',{'inventory':product_stock})
                pass
            else:
                procuctinfo=EngageboostProductStocks.objects.create(
                    stock=0,
                    safety_stock=0,
                    avg_sales_week=0,
                    avg_sales_month=0,
                    stock_unit=0,
                    product_id=product_id,
                    warehouse_id=warehouse_id,
                    created=datetime.now(),
                    modified=datetime.now(),
                    isdeleted='n',
                    isblocked='n',
                    real_stock=0
                )
        
            product_stock = common.get_product_stock(product_id)
            elastic = common.change_field_value_elastic(product_id,'EngageboostProducts',{'inventory':product_stock})

        # rs_product = EngageboostProducts.objects.filter(isblocked = 'n', isdeleted='n').values_list('id', flat=True).iterator()
        # rs_product_list = list(set(rs_product))
        rs_product_list = rs_stock_product
        rs_currency = EngageboostGlobalsettingCurrencies.objects.filter(isblocked='n', isdeleted = 'n').values('currency_id').first()
        currency_id = 16
        if rs_currency:
            currency_id = rs_currency['currency_id']

        rs_price_master = EngageboostPriceTypeMaster.objects.filter(isdeleted='n', isblocked = 'n').all().values('id','name')
        price_master = PriceTypeMasterSerializer(rs_price_master, many=True)
        # rs_price_master = list(set(rs_price_master))
        if price_master and len(rs_product_list)>0:
            for price_type in rs_price_master:
                for product_id in rs_product_list:
                    # print("product_id===========",product_id)
                    check_price_type = EngageboostProductPriceTypeMaster.objects.filter(isdeleted = 'n', isblocked='n', price_type_id=price_type['id'], product_id=product_id)
                    if check_price_type.count()>0:
                        check_price_type = check_price_type.order_by("id").first()
                        try:
                            latestWarehouse_id = check_price_type.warehouse_id
                            if latestWarehouse_id!="" and latestWarehouse_id!=None:
                                latestWarehouse_id = latestWarehouse_id.split(',')
                                if str(warehouse_id) not in latestWarehouse_id:
                                    latestWarehouse_id.append(str(warehouse_id))
                                # print("Here============",latestWarehouse_id)
                                latestWarehouse_id = ",".join(latestWarehouse_id)
                            else:
                                latestWarehouse_id = str(warehouse_id)

                            EngageboostProductPriceTypeMaster.objects.filter(id=check_price_type.id).update(warehouse_id=latestWarehouse_id)
                        except:
                            pass    
                        
                        check_channel_price = EngageboostChannelCurrencyProductPrice.objects.filter(product_id = product_id, warehouse_id=warehouse_id, currency_id=currency_id, product_price_type_id=check_price_type.id).count()
                        if check_channel_price>0:
                            pass
                        else:
                            rs_insert_channel_price = EngageboostChannelCurrencyProductPrice.objects.create(
                                product_id = product_id, 
                                warehouse_id=warehouse_id, 
                                currency_id=currency_id, 
                                product_price_type_id=check_price_type.id,
                                channel_id=6,
                                price=0,
                                max_quantity=0,
                                website_id=1,
                                cost=0,
                                min_quantity=0,
                                start_date=datetime.now(),
                                mrp=0
                            )
                            price_data = common.get_channel_currency_product_price(product_id)
                            common.change_field_value_elastic(product_id,'EngageboostProducts',{"channel_currency_product_price":price_data})
                    else:
                        rs_insert_price_type = EngageboostProductPriceTypeMaster.objects.create(
                            name = price_type['name'],
                            website_id = 1,
                            # created = datetime.now(),
                            # modified = datetime.now(),
                            isdeleted = 'n',
                            isblocked = 'n',
                            price_type_id = price_type['id'],
                            product_id = product_id,
                            max_quantity = 0,
                            min_quantity = 0,
                            warehouse_id = warehouse_id
                        )
                        rs_insert_channel_price = EngageboostChannelCurrencyProductPrice.objects.create(
                            product_id = product_id, 
                            warehouse_id=warehouse_id, 
                            currency_id=currency_id, 
                            product_price_type_id=rs_insert_price_type.id,
                            channel_id=6,
                            price=0,
                            max_quantity=0,
                            website_id=1,
                            cost=0,
                            min_quantity=0,
                            start_date=datetime.now(),
                            mrp=0
                        )
                        price_data = common.get_channel_currency_product_price(product_id)
                        common.change_field_value_elastic(product_id,'EngageboostProducts',{"channel_currency_product_price":price_data})

@postpone
def UpadateStockTest(warehouse_id=None):
    # print("Initiated for warehouse ===>", warehouse_id)
    response = emailcomponent.testmail('binayak.santra@navsoft.in',
                                       "Warehouse product sync started @@@SavePriceFromTempToTableLive123@@@",
                                       'Data preparation Started,' + ' @ ' + str(
                                           datetime.now()) + ' datas==' + str(warehouse_id) + '===>')

    response = emailcomponent.testmail('lifco.onboard@gmail.com',
                                       "Warehouse product sync started",
                                       'Data preparation Started,' + ' @ ' + str(
                                           datetime.now()) + ' datas==' + str(warehouse_id) + '===>')

    es = Elasticsearch([{'host': settings.ELASTIC_HOST, 'port': settings.ELASTIC_PORT, 'timeout': 3600}])
    es.cluster.health(wait_for_status='yellow', request_timeout=30)

    datas = []
    docs = []
    defunct_product_ids = []

    # es = common.connect_elastic()

    if warehouse_id is not None:
        rs_stock_product = EngageboostProducts.objects.filter(isblocked='n', isdeleted='n').order_by('id').values_list(
            'id', flat=True).iterator()
        rs_stock_product = list(set(rs_stock_product))

        #-----Binayak Start 16-03-2021-----#
        table_name = 'EngageboostProducts'
        total_len_count = len(rs_stock_product)
        if total_len_count>0:
            module_name = common.get_index_name_elastic(rs_stock_product[0], table_name)

            #===================Processing by fragment of 1000==================#
            chunk_size = 1000
            fragment_size, remainder = divmod(total_len_count, chunk_size)
            # print("fragment_size====", fragment_size, remainder)
            if int(remainder)>0:
                fragment_size+=1
            # print("product_id", rs_stock_product[0])
            # print("product_ids", len(rs_stock_product))
            for i in range(fragment_size):
                try:
                    docs = []
                    datas = []
                    data_string = []
                    start_pos = i * chunk_size
                    # start_pos = 51365
                    end_pos = (i + 1) * chunk_size
                    # end_pos = 51701
                    if i == fragment_size - 1:
                        end_pos = start_pos + remainder
                    for product_id in rs_stock_product[start_pos:end_pos]:
                        id_string = {
                            "_id": product_id,
                            "_source": {
                                "include": ["channel_currency_product_price"]
                            }
                        }
                        data_string.append(id_string)
                    # print("data_string", data_string)
                    # print("======i=======", i)
                    # print("start_pos", start_pos)
                    # print("end_pos", end_pos)
                # return
                    prod_exists = es.mget(body=json.dumps({"docs": data_string}), index=module_name, doc_type="data")


                    # for product_id in rs_stock_product:
                    for item in prod_exists['docs']:
                        # print("_id", item['_id'])
                        cm_id = item['_id']
                        # print("======cm_id=======", cm_id)

                        EngageboostProductStocks.objects.get_or_create(isblocked='n',
                                                                       isdeleted='n',
                                                                       product_id=cm_id,
                                                                       warehouse_id=warehouse_id,
                                                                       defaults={'created': datetime.now(),
                                                                                 'modified': datetime.now(),
                                                                                 'stock': 0,
                                                                                 'safety_stock': 0,
                                                                                 'avg_sales_week': 0,
                                                                                 'avg_sales_month': 0,
                                                                                 'stock_unit': 0,
                                                                                 'real_stock': 0})
                        # rs_check = EngageboostProductStocks.objects.filter(isblocked='n', isdeleted='n', product_id=cm_id,
                        #                                                    warehouse_id=warehouse_id).count()
                        # if rs_check > 0:
                        #     # product_stock = common.get_product_stock(product_id)
                        #     # elastic = common.change_field_value_elastic(product_id,'EngageboostProducts',{'inventory':product_stock})
                        #     pass
                        # else:
                        #     procuctinfo = EngageboostProductStocks.objects.create(
                        #         stock=0,
                        #         safety_stock=0,
                        #         avg_sales_week=0,
                        #         avg_sales_month=0,
                        #         stock_unit=0,
                        #         product_id=cm_id,
                        #         warehouse_id=warehouse_id,
                        #         created=datetime.now(),
                        #         modified=datetime.now(),
                        #         isdeleted='n',
                        #         isblocked='n',
                        #         real_stock=0
                        #     )

                        if item['found'] == True:

                            product_stock = common.get_product_stock(cm_id)
                            data = {"inventory": product_stock}

                            # data = get_product_field_value_for_elastic(cm_id, field_name)

                            header = {
                                "_op_type": 'update',
                                "_index": module_name,
                                "_type": "data",
                                "_id": cm_id,
                                "doc": data
                            }

                            docs.append(header)

                        else:
                            now_item = EngageboostProducts.objects.filter(id=cm_id).first()
                            try:
                                serializer_class = common.get_serializer_class_elastic(table_name)
                                # serializer = serializer_class(item,partial=True)
                                serializer = serializer_class(now_item, partial=True)
                                data = serializer.data
                                # print("Data Formatting Start=====",datetime.now())
                                # data = common.setUpLangDataToSerializer(data)
                                data = common.format_serialized_data(table_name, data)

                                header = {
                                    "_index": module_name,
                                    "_type": "data",
                                    "_id": cm_id,
                                    "_source": data
                                }

                                docs.append(header)
                            except:
                                defunct_product_ids.append(cm_id)
                                pass
                        # print('========header===========', header)
                        # -----Binayak Start 16-03-2021-----#
                        # elastic = common.change_field_value_elastic(product_id, 'EngageboostProducts', {'inventory': product_stock})
                        # -----Binayak Start 16-03-2021-----#
                    # print('========inventory data prepared end===========')

                    # response = emailcomponent.testmail('binayak.santra@navsoft.in',
                    #                                    "Warehouse product sync started @@@SavePriceFromTempToTableLive123@@@",
                    #                                    'Data preparation for inventory,' + ' @ ' + str(
                    #                                        datetime.now()) + ' datas==' + str(warehouse_id) + '===>')
                    # return
                    # rs_product = EngageboostProducts.objects.filter(isblocked = 'n', isdeleted='n').values_list('id', flat=True).iterator()
                    # rs_product_list = list(set(rs_product))
                    rs_product_list = rs_stock_product[start_pos:end_pos]
                    rs_currency = EngageboostGlobalsettingCurrencies.objects.filter(isblocked='n', isdeleted='n').values(
                        'currency_id').first()
                    currency_id = 16
                    if rs_currency:
                        currency_id = rs_currency['currency_id']

                    rs_price_master = EngageboostPriceTypeMaster.objects.filter(isdeleted='n', isblocked='n').all().values('id',
                                                                                                                           'name')
                    # price_master = PriceTypeMasterSerializer(rs_price_master, many=True)
                    # rs_price_master = list(set(rs_price_master))
                    # if price_master and len(rs_product_list) > 0:
                    if rs_price_master.count()>0 and len(rs_product_list) > 0:
                        # print("i am here")
                        for price_type in rs_price_master:
                            # for product_id in rs_product_list:
                            for item in prod_exists['docs']:
                                cm_id = item['_id']
                                # print("=======cm_id=========", cm_id)
                                # print("product_id===========",product_id)
                                check_price_type = EngageboostProductPriceTypeMaster.objects.filter(isdeleted='n', isblocked='n',
                                                                                                    price_type_id=price_type['id'],
                                                                                                    product_id=cm_id)
                                if check_price_type.count() > 0:
                                    # print("i am here 2")
                                    check_price_type = check_price_type.order_by("id").first()
                                    try:
                                        latestWarehouse_id = check_price_type.warehouse_id
                                        if latestWarehouse_id != "" and latestWarehouse_id != None:
                                            latestWarehouse_id = latestWarehouse_id.split(',')
                                            if str(warehouse_id) not in latestWarehouse_id:
                                                latestWarehouse_id.append(str(warehouse_id))
                                            # print("Here============",latestWarehouse_id)
                                            latestWarehouse_id = ",".join(latestWarehouse_id)
                                        else:
                                            latestWarehouse_id = str(warehouse_id)

                                        EngageboostProductPriceTypeMaster.objects.filter(id=check_price_type.id).update(
                                            warehouse_id=latestWarehouse_id)
                                    except:
                                        pass

                                    EngageboostChannelCurrencyProductPrice.objects.get_or_create(
                                        product_id=cm_id,
                                        warehouse_id=warehouse_id,
                                        currency_id=currency_id,
                                        product_price_type_id=check_price_type.id,
                                        defaults={'channel_id': 6,
                                                  'price': 0,
                                                  'max_quantity': 0,
                                                  'website_id': 1,
                                                  'cost': 0,
                                                  'min_quantity': 0,
                                                  'start_date': datetime.now(),
                                                  'mrp': 0})

                                    # check_channel_price = EngageboostChannelCurrencyProductPrice.objects.filter(
                                    #     product_id=cm_id, warehouse_id=warehouse_id, currency_id=currency_id,
                                    #     product_price_type_id=check_price_type.id).count()
                                    # if check_channel_price > 0:
                                    #     pass
                                    # else:
                                    #     try:
                                    #         rs_insert_channel_price = EngageboostChannelCurrencyProductPrice.objects.create(
                                    #             product_id=cm_id,
                                    #             warehouse_id=warehouse_id,
                                    #             currency_id=currency_id,
                                    #             product_price_type_id=check_price_type.id,
                                    #             channel_id=6,
                                    #             price=0,
                                    #             max_quantity=0,
                                    #             website_id=1,
                                    #             cost=0,
                                    #             min_quantity=0,
                                    #             start_date=datetime.now(),
                                    #             mrp=0
                                    #         )
                                    #     except:
                                    #         pass

                                    # ------Binayak Start 16-03-2021------#
                                    # price_data = common.get_channel_currency_product_price(product_id)
                                    if item['found'] == True:
                                        price_data = item['_source']['channel_currency_product_price']
                                        price_data = common.single_channel_currency_price_update_string(cm_id, price_data, warehouse_id, 1)
                                        data = {"channel_currency_product_price": price_data}

                                        header = {
                                            "_op_type": 'update',
                                            "_index": module_name,
                                            "_type": "data",
                                            "_id": cm_id,
                                            "doc": data
                                        }
                                    else:
                                        now_item = EngageboostProducts.objects.filter(id=cm_id).first()
                                        serializer_class = common.get_serializer_class_elastic(table_name)
                                        # serializer = serializer_class(item,partial=True)
                                        serializer = serializer_class(now_item, partial=True)
                                        data = serializer.data
                                        # print("Data Formatting Start=====",datetime.now())
                                        # data = common.setUpLangDataToSerializer(data)
                                        data = format_serialized_data(table_name, data)

                                        header = {
                                            "_index": module_name,
                                            "_type": "data",
                                            "_id": cm_id,
                                            "_source": data
                                        }
                                    # print("======add header=======", header)
                                    docs.append(header)
                                        # price_data = common.get_channel_currency_product_price(cm_id, 1, [warehouse_id])
                                    # ------Binayak Start 16-03-2021------#

                                    # common.change_field_value_elastic(cm_id, 'EngageboostProducts',
                                    #                                   {"channel_currency_product_price": price_data})

                                else:
                                    rs_insert_price_type = EngageboostProductPriceTypeMaster.objects.create(
                                        name=price_type['name'],
                                        website_id=1,
                                        created=datetime.now(),
                                        modified=datetime.now(),
                                        isdeleted='n',
                                        isblocked='n',
                                        price_type_id=price_type['id'],
                                        product_id=cm_id,
                                        max_quantity=0,
                                        min_quantity=0,
                                        warehouse_id=warehouse_id
                                    )
                                    rs_insert_channel_price = EngageboostChannelCurrencyProductPrice.objects.create(
                                        product_id=cm_id,
                                        warehouse_id=warehouse_id,
                                        currency_id=currency_id,
                                        product_price_type_id=rs_insert_price_type.id,
                                        channel_id=6,
                                        price=0,
                                        max_quantity=0,
                                        website_id=1,
                                        cost=0,
                                        min_quantity=0,
                                        start_date=datetime.now(),
                                        mrp=0
                                    )

                                    # ------Binayak Start 16-03-2021------#
                                    # price_data = common.get_channel_currency_product_price(product_id)
                                    if item['found'] == True:
                                        price_data = item['_source']['channel_currency_product_price']
                                        price_data = common.single_channel_currency_price_update_string(cm_id, price_data,
                                                                                                        warehouse_id, 1)
                                        data = {"channel_currency_product_price": price_data}

                                        header = {
                                            "_op_type": 'update',
                                            "_index": module_name,
                                            "_type": "data",
                                            "_id": cm_id,
                                            "doc": data
                                        }
                                    else:
                                        now_item = EngageboostProducts.objects.filter(id=cm_id).first()
                                        serializer_class = common.get_serializer_class_elastic(table_name)
                                        # serializer = serializer_class(item,partial=True)
                                        serializer = serializer_class(now_item, partial=True)
                                        data = serializer.data
                                        # print("Data Formatting Start=====",datetime.now())
                                        # data = common.setUpLangDataToSerializer(data)
                                        data = format_serialized_data(table_name, data)

                                        header = {
                                            "_index": module_name,
                                            "_type": "data",
                                            "_id": cm_id,
                                            "_source": data
                                        }
                                        # print("======add header=======", header)
                                    docs.append(header)
                                    # price_data = common.get_channel_currency_product_price(cm_id, 1, [warehouse_id])
                                    # ------Binayak End 16-03-2021------#

                                    # common.change_field_value_elastic(cm_id, 'EngageboostProducts',
                                    #                                   {"channel_currency_product_price": price_data})

                    # response = emailcomponent.testmail('binayak.santra@navsoft.in',
                    #                                    "Warehouse product sync started @@@SavePriceFromTempToTableLive123@@@",
                    #                                    'Data preparation for price,' + ' @ ' + str(
                    #                                        datetime.now()) + ' datas==' + str(warehouse_id) + '===>')
                    print("======channel price data ended=======")
                except Exception as error:
                    trace_back = sys.exc_info()[2]
                    line = trace_back.tb_lineno
                    datas.append({"status": 0, "api_status": traceback.format_exc(), "error_line": line,
                             "error_message": str(error),
                             "message": str(error)})
                finally:
                    # print("==========docs===========", docs)
                    obj = helpers.bulk(es, docs)
                    datas.append({"obj": obj})
                    response = emailcomponent.testmail('binayak.santra@navsoft.in',
                                                       "Warehouse product sync @@@SavePriceFromTempToTableLive123@@@",
                                                       'Data preparation Completed and Pushed to Elastic,' +  ' @ ' + str(
                                                           datetime.now()) + ' datas for warehouse ==' + str(warehouse_id) + '===>' + str(datas) + "=======defunct_product_ids=======" + str(defunct_product_ids))

                    response = emailcomponent.testmail('lifco.onboard@gmail.com',
                                                       "Warehouse product sync @@@SavePriceFromTempToTableLive123@@@",
                                                       'Data preparation Completed and Pushed to Elastic,' +  ' @ ' + str(
                                                           datetime.now()) + ' datas for warehouse ==' + str(warehouse_id) + '===>' + str(obj))


# def UpadateStockTestCron():
#     UpadateStockTest(154)

class UpadateStockTestCron(generics.ListAPIView):
    def get(self, request, pk, format=None, partial=True):
        UpadateStockTest(pk)
        return Response('done')


def ProductElasticUpdate():
    rs_product = EngageboostProducts.objects.filter(isblocked = 'n', isdeleted='n').values_list('id', flat=True).iterator()
    rs_product_list = list(set(rs_product))
    for product_id in rs_product_list:
        price_data = common.get_channel_currency_product_price(product_id)
        common.change_field_value_elastic(product_id,'EngageboostProducts',{"channel_currency_product_price":price_data})

        product_stock = common.get_product_stock(product_id)
        elastic = common.change_field_value_elastic(product_id,'EngageboostProducts',{'inventory':product_stock})


def CopyAutoresponder(warehouse_id=None):
    if warehouse_id is not None:
        # EngageboostEmailTypeContents.objects.filter(warehouse_id=1).all()
        rs_copy_from = EngageboostEmailTypeContents.objects.filter(website_id=1).all()[:1]
        copy_from_data = EmailTypeContentsSerializer(rs_copy_from, many=True)
        copy_from_data = copy_from_data.data
        if copy_from_data:
            for from_data in copy_from_data:
                from_data.pop('id')
                # from_data['warehouse_id'] = warehouse_id
                
                EngageboostEmailTypeContents.objects.create(**from_data)


@postpone
def UpadateCategoryWarehouse(warehouse_id=None):
    category_qs = EngageboostCategoryMasters.objects.filter(isdeleted='n',isblocked='n').all()
    #print('category',category_qs.query)
    if category_qs:
        for category_data in category_qs:
            #print('++++++++',category_data.id)
            catWarehouse_qs = EngageboostCategoryWarehouse.objects.create(warehouse_id=warehouse_id,created = datetime.now(),modified=datetime.now(),category_id=category_data.id)
    ###########update category banner start here ############################   

    rs_update = EngageboostCategoryBanners.objects.filter(isdeleted='n')    
    #print(rs_update.query) 
    if rs_update and warehouse_id:
        for up_data in rs_update:
            newWarehouseId = str(warehouse_id)
            if up_data.warehouse_id and up_data.warehouse_id is not None:
                newWarehouseId = str(up_data.warehouse_id)+","+str(warehouse_id)
            #print(up_data.id)
            if newWarehouseId is not None and newWarehouseId!="":
                EngageboostCategoryBanners.objects.filter(id = up_data.id,isdeleted='n').update(warehouse_id=newWarehouseId)

class DuplicatePriceRemove(generics.ListAPIView):
    def post(self, request, format=None):
        RemoveDuplicatePrice()
        data ={
            'status':1,
            'api_status':[],
            'message':'Success',
        }
        return Response(data)

@postpone       
def RemoveDuplicatePrice():
    rs_products = EngageboostProducts.objects.filter(isdeleted  ='n').all()
    if rs_products:
        for products in rs_products:
            rs_price_type =   EngageboostProductPriceTypeMaster.objects.filter(product_id = products.id, price_type_id = 1).order_by("id")
            price_type_data = ProductPriceTypeMasterSerializer(rs_price_type, many= True).data
            if len(price_type_data)>0:
                deletable_id = []
                for i in range(len(price_type_data)):            
                    if i>0:
                        deletable_id.append(price_type_data[i]['id'])

            EngageboostChannelCurrencyProductPrice.objects.filter(product_id = products.id, product_price_type_id__in = deletable_id).delete()
            EngageboostProductPriceTypeMaster.objects.filter(id__in = deletable_id).delete()

# RemoveDuplicatePrice()
