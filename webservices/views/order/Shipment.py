from webservices.models import *
from django.http import Http404
from webservices.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
# from rest_framework import status
# from django.views.decorators.csrf import csrf_exempt
import datetime,time
from rest_framework import generics
from django.core import serializers
from webservices.views import loginview
from webservices.views.common import common
from webservices.views.emailcomponent import emailcomponent
from webservices.views.order import Order
from django.db.models import Count, Sum, Avg

import sys
import traceback
import json
from num2words import num2words
import os
import requests
import math
from django.core.files.storage import FileSystemStorage
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db.models.aggregates import Aggregate
from django.contrib.postgres.aggregates import *
from django.db.models import Q
from webservices.views.product import Discount
import base64
import urllib
from urllib.parse import urlencode, quote_plus, urlparse
from frontapp.views.payment.ccavRequestHandler import *

# import socket
class Shipment(generics.ListAPIView):
  # """ Add New Shipment """
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        shipmentType        = request.data["shipmentType"]
        website_id          = request.data["website_id"]
        company_id          = request.data["company_id"]
        userId = request.data["userId"]
        order_ids = request.data["selectedIds"]
        ItemIdsArr = order_ids.split(',')
        zone_id,assign_wh,assign_to = 0,0,0
        try:
            if shipmentType == "ItemWise":
                orders_data = EngageboostOrderProducts.objects.filter(id__in=ItemIdsArr, order_status='100').exclude(shipment_id__gt=0).all()
                if orders_data:
                    order_idsArr = []
                    order_prod_data_serializer = OrderProductsSerializer(orders_data,many=True)
                    if order_prod_data_serializer.data:
                        for OrderProductsData in order_prod_data_serializer.data:
                            order_idsArr.append(OrderProductsData["order_id"])
                        ItemIdsArr = list(set(order_idsArr)) # return unique array and assigned order id from order product table

                        assign_wh = order_prod_data_serializer.data[0][0]["assign_wh"]
                        assign_to = order_prod_data_serializer.data[0][0]["assign_to"]
                        zone_id   = order_prod_data_serializer.data[0][0]["zone_id"]
            else:
                orders_data = EngageboostOrdermaster.objects.filter(id__in=ItemIdsArr,order_status='100').exclude(shipment_id__gt=0).all()
                order_data_serializer = OrderMasterSerializer(orders_data,many=True)
                if order_data_serializer.data:
                    assign_wh = order_data_serializer.data[0]["assign_wh"]
                    assign_to = order_data_serializer.data[0]["assign_to"]
                    zone_id   = order_data_serializer.data[0]["zone_id"]

            warehouse_id = assign_wh;
            shipment_Prefix = "SHM#"
            lastShipment = EngageboostShipments.objects.last()
            if lastShipment:
                lastShipmentId = int(lastShipment.id)+int(1)
            else:
                lastShipmentId = 1
            shipment_id_new = shipment_Prefix+""+str(lastShipmentId)
            now_utc = datetime.now(timezone.utc).astimezone()
            if warehouse_id > 0: # and zone_id > 0
                Shipment = EngageboostShipments.objects.using(company_db).create(custom_shipment_id=shipment_id_new,warehouse_id=warehouse_id,created_by=assign_to,shipment_status='Shipment Processing',created=now_utc,modified=now_utc,website_id=website_id) #,zone_id=zone_id
                shipment_id = Shipment.id
                if shipment_id > 0:
                    for order_id in ItemIdsArr:
                        EngageboostOrdermaster.objects.filter(id=order_id).update(shipment_id=shipment_id)
                        EngageboostInvoicemaster.objects.filter(order_id=order_id).update(shipment_id=shipment_id)
                        EngageboostShipmentOrders.objects.filter(order_id=order_id,shipment_status='Create Shipment').update(shipment_status='Shipment Processing',shipment=shipment_id)
                        EngageboostShipmentOrderProducts.objects.filter(order_id=order_id,shipment_status='Create Shipment').update(shipment_status='Shipment Processing',shipment=shipment_id)
                        elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'shipping_status':'Shipment Processing'})
                        activityType = 1
                        activity_details = common.save_order_activity(company_db,order_id,now_utc,7,"Shipment process is started.",userId,activityType)
                    # create_automatic_delivery_plan call here, delivery planner start here by cds...
                    totalVechicle = create_automatic_delivery_plan(ItemIdsArr, shipment_id, warehouse_id)
                    #print('CDS checking vehicle nnumber...')
                    #print(totalVechicle)
                    #print('CDS checking vehicle nnumber...')
                    EngageboostShipments.objects.filter(id=shipment_id).update(no_of_vehicles=totalVechicle)
                    data = {
                        'status':1,
                        'api_status':'',
                        'shipment_id': shipment_id,
                        'message':'Successfully Inserted',
                    }
                else:
                    data ={
                        'status':0,
                        'api_status':'',
                        'shipment_id': 0,
                        'message':'Order Data Not Found'
                    }
            else:
                data ={
                    'status':0,
                    'api_status':'',
                    'shipment_id': 0,
                    'message':'Order Data Not Found'
                }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

class RemoveOrderShipment(generics.ListAPIView):
    def post(self,request):
        company_db = loginview.db_active_connection(request)
        requestdata = request.data
        now_utc = datetime.now(timezone.utc).astimezone()
        shipment_id = requestdata['shipment_id']
        order_ids = request.data["selectedIds"]
        ItemIdsArr = order_ids.split(',')
        userId = request.data["userId"]
        try:
            shipment_orders = EngageboostShipmentOrders.objects.using(company_db).filter(order__in=ItemIdsArr,shipment=shipment_id).all()
            shipment_orders_serializer = ShipmentsOrdersSerializer(shipment_orders,many=True)
            if shipment_orders_serializer :
                for shipmentOrder in shipment_orders_serializer.data:
                    shipment_status = shipmentOrder["shipment_status"]
                    order_id = shipmentOrder["order"]['id']
                    if shipment_status == 'Shipment Processing':
                        EngageboostOrdermaster.objects.filter(id=order_id,shipment_id=shipment_id).update(shipment_id=0,sort_by_distance=0)
                        EngageboostShipmentOrders.objects.filter(order=order_id,shipment=shipment_id).update(shipment_status='Create Shipment',shipment=0)
                        EngageboostShipmentOrderProducts.objects.filter(order_id=order_id,shipment=shipment_id).update(shipment_status='Create Shipment',shipment=0)
                        EngageboostInvoicemaster.objects.filter(order=order_id, shipment_id=shipment_id).update(shipment_id=0)
                        EngageboostDeliveryPlanOrder.objects.filter(order_id=order_id, shipment_id=shipment_id).delete()
                        elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'_status':'Create Shipment'})
                        activityType = 1
                        activity_details = common.save_order_activity(company_db,order_id,now_utc,7,"Order is removed from shipment.",userId,activityType)

                        shipment_order = EngageboostShipmentOrders.objects.using(company_db).filter(shipment=shipment_id).count()
                        if shipment_order == 0:
                            EngageboostShipments.objects.filter(id=shipment_id).update(isdeleted='y',isblocked='y')
                        data = {
                            'status':1,
                            'api_status':'',
                            'shipment_id': shipment_id,
                            'message':'Order is successfully remove from shipment',
                        }
                    else:
                        data = {
                            'status':0,
                            'api_status':'',
                            'shipment_id': shipment_id,
                            'message':"Delivery planner is already completed, you can't removed from shipment."
                        }
            else:
                data ={
                    'status':0,
                    'api_status':serializer.errors,
                    'shipment_id': shipment_id,
                    'message':'Data Not Found',
                }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

@csrf_exempt
def make_planner(request):
    print('Chkardhar testing planner start')
    #shipment_id = 94
    shipment_id = 117
    #orderArr = ['93', '94', '95', '96']
    orderArr = ['126', '127']
    create_automatic_delivery_plan(orderArr, shipment_id, 0)
    print('Chkardhar testing planner end')
    return 1;

# Making delivery planner...
def create_automatic_delivery_plan(orderArr, shipment_id, warehouse_id):
    origins = "25.2048,55.2708"
    if warehouse_id > 0:
        warehouseDetails = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).first()
        if warehouseDetails and warehouseDetails.latitude and warehouseDetails.longitude:
            origins = warehouseDetails.latitude+','+warehouseDetails.longitude;

    now_utc = datetime.now(timezone.utc).astimezone()
    #print("Planner is calling here...by cds...")
    #print("====================================")
    all_order = EngageboostOrdermaster.objects.filter(id__in=orderArr).order_by('slot_start_time').all()
    order_data_serializer = OrderMasterSerializer(all_order, many=True)
    #print(json.dumps(order_data_serializer.data))
    zoneId = order_data_serializer.data[0]["zone_id"]
    countOrder = len(orderArr);
    VehicleData = EngageboostVehicleMasters.objects.filter(no_of_orders__gt=0).first()
    if VehicleData and VehicleData.no_of_orders:
        vehicle_threshold = VehicleData.no_of_orders
    else:
        vehicle_threshold = 15

    # manual checking
    #vehicle_threshold = 2
    if countOrder > vehicle_threshold:
        no_of_vehicle = countOrder/vehicle_threshold
        no_of_vehicle = math.ceil(countOrder/vehicle_threshold)
    else:
        no_of_vehicle = 1

    time_slot_array = []
    time_slot_wise_array = []
    order_vs_timeslot = []
    timeslotWiseArr =[]
    #print(orderArr)
    #print(json.dumps(order_data_serializer.data))
    for allOrder in order_data_serializer.data:
        time_slot_array_Obj = {
            'slot_start_time':allOrder['slot_start_time'],
            'time_slot_id': allOrder['time_slot_id']
        }
        if time_slot_array_Obj not in time_slot_array :
            time_slot_array.append(time_slot_array_Obj)

    order_lat_long_relation = []
    for time_slot_wise_val in time_slot_array:
        order_lat_long_relation_allOrder = [] # Making slot wise order planner first
        destinations_arr = []  # Making slot wise order planner first
        for allOrder in order_data_serializer.data :
            if time_slot_wise_val['time_slot_id'] == allOrder['time_slot_id']:
                order_lat_long_relation_obj ={}
                # allOrder['CustomersAddressBook']['long_val'] = '88.3849'
                # allOrder['CustomersAddressBook']['lat_val'] = '22.8671'
                if allOrder['CustomersAddressBook']['lat_val'] is None:
                    allOrder['CustomersAddressBook']['lat_val'] = '22.8671'
                if allOrder['CustomersAddressBook']['long_val'] is None:
                    allOrder['CustomersAddressBook']['long_val'] = '88.3849'
                if allOrder['CustomersAddressBook']:
                    order_lat_long_relation_obj = {
                        'order_id': allOrder['id'],
                        'area_id': allOrder['area_id'],
                        'slot_start_time': allOrder['slot_start_time'],
                        'address_book_id': allOrder['CustomersAddressBook']['id'],
                        'longitude': allOrder['CustomersAddressBook']['long_val'],
                        'latitude': allOrder['CustomersAddressBook']['lat_val'],
                        'lat_long_val': allOrder['CustomersAddressBook']['lat_val']+","+allOrder['CustomersAddressBook']['long_val']
                    }
                    destinations_arr.append(allOrder['CustomersAddressBook']['lat_val']+","+allOrder['CustomersAddressBook']['long_val']);
                else:
                    order_lat_long_relation_obj = {
                        'order_id': allOrder['id'],
                        'area_id': allOrder['area_id'],
                        'slot_start_time': allOrder['slot_start_time'],
                        'address_book_id': 0,
                        'lat_long_val': origins,
                        'longitude':'88.4119',
                        'latitude':'22.5135'
                    }
                    destinations_arr.append(origins);
                order_lat_long_relation_allOrder.append(order_lat_long_relation_obj)
                order_lat_long_relation.append(order_lat_long_relation_obj)
        time_slot_wise_val['allOrder'] = order_lat_long_relation_allOrder
        time_slot_wise_val['destinations'] = '|'.join(destinations_arr)
    #print(json.dumps(time_slot_wise_val))
    #print(json.dumps(time_slot_array))
    # print('==================')
    if(no_of_vehicle == 1):
        total_orderd_array = []
        total_orderd_array = calculate_distance(origins,time_slot_array, order_lat_long_relation)
        # Manual checking if no planner exist
        # for order_id in orderArr:
        # 	total_orderd_array_obj = {
        # 		'order_id':order_id,
        # 		'distance':10,
        # 		'duration':2
        # 	}
        # 	total_orderd_array.append(total_orderd_array_obj)
        orders = 1
        for total_orderd_arrayvalue in total_orderd_array :
            EngageboostDeliveryPlanOrder.objects.filter(order_id=total_orderd_arrayvalue['order_id']).delete()
            EngageboostDeliveryPlanOrder.objects.create(
                order_id = total_orderd_arrayvalue['order_id'],
                orders = orders,
                distance = total_orderd_arrayvalue['distance'],
                time = total_orderd_arrayvalue['duration'],
                shipment_id = shipment_id,
                created = now_utc,
                virtual_vechile_id = 1
            )
            #update sort_by_distance
            EngageboostOrdermaster.objects.filter(id=total_orderd_arrayvalue['order_id']).update(sort_by_distance=orders)
            orders = orders+1
    else:
        totalCount = 0
        timeslotWiseCount = []
        total_time_slot = []
        no_of_slot = len(time_slot_array)
        average_order_per_vehicle = math.ceil(countOrder/no_of_vehicle)
        finalVehicleArr = []
        timeslotwise_max_order_per_vehicle = []
        for timeslotWiseCountvalue in time_slot_array:
            timeslotwise_max_order_per_vehicleObj = {
                'slot_start_time':timeslotWiseCountvalue['slot_start_time'],
                'max_order_per_slot': math.ceil(len(timeslotWiseCountvalue['allOrder'])/no_of_vehicle)
            }
            timeslotWiseCountvalue['max_order_per_slot'] = math.ceil(len(timeslotWiseCountvalue['allOrder'])/no_of_vehicle)

        # print(timeslotWiseCountvalue)
        finalVehicleArr = []
        AllAreaArr = EngageboostZoneMasters.objects.filter(location_type='A',isdeleted='n',isblocked='n').all().order_by('distance')
        for time_slot_wise_val in time_slot_array:
            order_lat_long_relation_new = []
            for all_area in AllAreaArr:
                for areawiseOrder in time_slot_wise_val['allOrder']:
                    if all_area.id == areawiseOrder['area_id']:
                        order_lat_long_relation_new.append(areawiseOrder)

            time_slot_wise_val['allOrder'] = order_lat_long_relation_new
            #print(time_slot_wise_val['allOrder'])
            #lista_rr = list(divide_chunks(time_slot_wise_val['allOrder'], 2))
            #print(lista_rr)
            if len(time_slot_wise_val['allOrder']) > 0:
                time_slot_wise_val['vehicleArr'] = list(divide_chunks(time_slot_wise_val['allOrder'], time_slot_wise_val['max_order_per_slot']))
            #print(time_slot_wise_val['vehicleArr'])
            for finalVehicleArrObj in time_slot_wise_val['vehicleArr']:
                finalVehicleArr.append(finalVehicleArrObj)

        #print(finalVehicleArr)
        vehicleCount = 1;
        for finalVehicleArrvalue in finalVehicleArr:
            timeslotWiseArrmulti = []
            order_lat_long_relationmulti = []
            destinations_arr = []
            for time_slot_wise_val in time_slot_array:
                for all_order in time_slot_wise_val['allOrder']:
                    #print(all_order)
                    if all_order in finalVehicleArrvalue:
                        time_slot_array_Obj = {
                            'slot_start_time':allOrder['slot_start_time'],
                            'time_slot_id': allOrder['time_slot_id']
                        }
                        # checking unique....
                        if time_slot_array_Obj not in timeslotWiseArrmulti :
                            timeslotWiseArrmulti.append(time_slot_array_Obj)
            #print(timeslotWiseArrmulti)

            for timeslotWiseArrmulti_val in timeslotWiseArrmulti:
                for all_order_new in finalVehicleArrvalue:
                    if all_order_new['slot_start_time'] == timeslotWiseArrmulti_val['slot_start_time']:
                        order_lat_long_relation_mul_obj = {}
                        order_lat_long_relation_mul_obj = all_order_new
                        order_lat_long_relationmulti.append(order_lat_long_relation_mul_obj)
                        destinations_arr.append(all_order_new['lat_long_val'])

            timeslotWiseArrmulti_val['allOrder'] = order_lat_long_relationmulti
            timeslotWiseArrmulti_val['destinations'] = '|'.join(destinations_arr)
            # print(json.dumps(timeslotWiseArrmulti))
            total_orderd_array = calculate_distance(origins, timeslotWiseArrmulti, order_lat_long_relationmulti)
            orders = 1
            # print(vehicleCount)
            # print(total_orderd_array)
            for total_orderd_arrayvalue in total_orderd_array:
                #EngageboostDeliveryPlanOrder.objects.filter(order_id=total_orderd_arrayvalue['order_id']).delete()
                order_exist = EngageboostDeliveryPlanOrder.objects.filter(order_id=total_orderd_arrayvalue['order_id']).count()
                # print(order_exist)
                if order_exist:
                    EngageboostDeliveryPlanOrder.objects.filter(order_id=total_orderd_arrayvalue['order_id']).update(
                        order_id = total_orderd_arrayvalue['order_id'],
                        orders = orders,
                        distance = total_orderd_arrayvalue['distance'],
                        time = total_orderd_arrayvalue['duration'],
                        shipment_id = shipment_id,
                        modified = now_utc,
                        virtual_vechile_id = vehicleCount
                    )
                else:
                    EngageboostDeliveryPlanOrder.objects.create(
                        order_id = total_orderd_arrayvalue['order_id'],
                        orders = orders,
                        distance = total_orderd_arrayvalue['distance'],
                        time = total_orderd_arrayvalue['duration'],
                        shipment_id = shipment_id,
                        created = now_utc,
                        virtual_vechile_id = vehicleCount
                    )
                #update sort_by_distance
                EngageboostOrdermaster.objects.filter(id=total_orderd_arrayvalue['order_id']).update(fulfillment_id = vehicleCount, sort_by_distance=orders)
                orders = orders+1
            vehicleCount = vehicleCount+1
        # else loop end
        # print(no_of_vehicle)
    return no_of_vehicle

def divide_chunks(l, n): 
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

def calculate_distance(origins,timeslotWiseArr,order_lat_long_relation):
    destinationArr = []
    #print('calculate_distance')
    #print(order_lat_long_relation)
    #print(json.dumps(timeslotWiseArr))
    firstcount = 0;
    secondCount = 0;
    final_ordered_array=[];
    final_ordered_array_first_slot = []
    final_ordered_array_second_slot = []
    first_slot = 0
    for destinationArrkey in timeslotWiseArr:
        destinations = destinationArrkey['destinations']
        #print(timeslotWiseArr)
        allDestination = destinations.split("|")
        allDestinationArr = destinations.split("|")
        # ENTER INTO FIRST SLOT
        if first_slot == 0:
            for allDestinationvalue in allDestination:
                #print('Yes data coming => ' + allDestinationvalue + ' >> ' + str(firstcount))
                #print(firstcount)
                if firstcount == 0:
                    origins = origins
                    # CALL FIRST TIME WITH WAREHOUSE AS ORIGIN AND ALL FIRST TIMESLOT ORDERS AS DESTINATION
                    return_element = call_google_distance_matrix(origins, destinations, timeslotWiseArr)
                    #print(return_element)
                    for order_lat_long_relation_val in order_lat_long_relation:
                        if order_lat_long_relation_val['order_id'] == return_element[0]['order_id']:
                            origins = order_lat_long_relation_val['lat_long_val']
                            value_index = allDestinationArr.index(order_lat_long_relation_val['lat_long_val'])
                            del allDestinationArr[value_index]
                            for destinationArrkeyValue in destinationArrkey['allOrder']:
                                #print(destinationArrkeyValue)
                                if destinationArrkeyValue['order_id'] == return_element[0]['order_id']:
                                    value_index = destinationArrkey['allOrder'].index(destinationArrkeyValue)
                                    del destinationArrkey['allOrder'][value_index]
                    final_ordered_array_first_slot.append(return_element[0])
                    #print(allDestinationArr)
                    #print(timeslotWiseArr)
                else:
                    allDestStr = '|'.join(allDestinationArr)
                    return_element = call_google_distance_matrix(origins, allDestStr, timeslotWiseArr)
                    for order_lat_long_relation_val in order_lat_long_relation:
                        if order_lat_long_relation_val['order_id'] == return_element[0]['order_id']:
                            origins = order_lat_long_relation_val['lat_long_val']
                            value_index = allDestinationArr.index(order_lat_long_relation_val['lat_long_val'])
                            del allDestinationArr[value_index]
                            for destinationArrkeyValue in destinationArrkey['allOrder']:
                                #print(destinationArrkeyValue)
                                if destinationArrkeyValue['order_id'] == return_element[0]['order_id']:
                                    value_index = destinationArrkey['allOrder'].index(destinationArrkeyValue)
                                    del destinationArrkey['allOrder'][value_index]
                    final_ordered_array_first_slot.append(return_element[0])
                    #print(allDestinationArr)
                    #print(allDestination)
                firstcount+=1
            #print(final_ordered_array_first_slot)
        else:
            # ENTER INTO SECOND SLOT
            allDestStr = '|'.join(allDestinationArr)
            for allDestinationvalue in allDestination:
                if secondCount == 0:
                    #origins is always coming from first slot
                    return_element_second = call_google_distance_matrix(origins, destinations, timeslotWiseArr)
                    #print(return_element_second)
                    for order_lat_long_relation_val in order_lat_long_relation:
                        if order_lat_long_relation_val['order_id'] == return_element_second[0]['order_id']:
                            origins = order_lat_long_relation_val['lat_long_val']
                            value_index = allDestinationArr.index(order_lat_long_relation_val['lat_long_val'])
                            del allDestinationArr[value_index]
                            for destinationArrkeyValue in destinationArrkey['allOrder']:
                                #print(destinationArrkeyValue)
                                if destinationArrkeyValue['order_id'] == return_element_second[0]['order_id']:
                                    value_index = destinationArrkey['allOrder'].index(destinationArrkeyValue)
                                    del destinationArrkey['allOrder'][value_index]
                    final_ordered_array_second_slot.append(return_element_second[0])
                else:
                    allDestStr = '|'.join(allDestinationArr)
                    return_element_second = call_google_distance_matrix(origins, allDestStr, timeslotWiseArr)
                    for order_lat_long_relation_val in order_lat_long_relation:
                        if order_lat_long_relation_val['order_id'] == return_element_second[0]['order_id']:
                            origins = order_lat_long_relation_val['lat_long_val']
                            value_index = allDestinationArr.index(order_lat_long_relation_val['lat_long_val'])
                            del allDestinationArr[value_index]
                            for destinationArrkeyValue in destinationArrkey['allOrder']:
                                #print(destinationArrkeyValue)
                                if destinationArrkeyValue['order_id'] == return_element_second[0]['order_id']:
                                    value_index = destinationArrkey['allOrder'].index(destinationArrkeyValue)
                                    del destinationArrkey['allOrder'][value_index]
                    final_ordered_array_second_slot.append(return_element_second[0])
                secondCount+=1
        first_slot+=1
    total_return_arr = []
    if len(final_ordered_array_second_slot)> 0:
        total_return_arr = final_ordered_array_first_slot+final_ordered_array_second_slot
    else:
        total_return_arr = final_ordered_array_first_slot
    #print(total_return_arr)
    return total_return_arr

def call_google_distance_matrix(source, dest, timeslotWiseArr):
    APY_KEY = 'AIzaSyBaTj-wuRYF1YuAHvj8UV5JhDMc_y5f9-g'
    #APY_KEY = 'AIzaSyCE0i_GPkfk5g2VINiZTYCobWU-qpk7psc'
    GOOGLE_MAPS_API_URL = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="+source+"&destinations="+dest+"&key="+APY_KEY+"&travelMode=DRIVING&waypoints=optimize:true&sensor=false"
    result = requests.get(GOOGLE_MAPS_API_URL)
    result = result.json()
    #print('Google response data...')
    print(result)
    timeDistance =  [];
    if(result['status'] == 'OK'):
        for value in result['rows'][0]['elements']:
            if value['status'] == 'ZERO_RESULTS':
                timeDistanceObj = {
                    'distance': 0,
                    'duration': 1,
                }
            else:
                timeDistanceObj = {
                    'distance': value['distance']['value'],
                    'duration': value['duration']['value'],
                }
            timeDistance.append(timeDistanceObj)
    #print(timeDistance)
    # Python shorting....
    timeDistance = sorted(timeDistance, key=lambda dct: dct['distance'])
    #print(timeDistance);
    shortestOrder = []
    count = 0
    #print("----------------------")
    #print(source)
    #print(dest)
    #print("----------------------")
    for timeDistancevalue in timeDistance:
        if count == 0:
            dest_new = dest.split("|")
            shoretes_one = dest_new[0]
            shoretes_one = shoretes_one.split(",")
            latitude = shoretes_one[0]
            seekreturn = seekValue(timeslotWiseArr,latitude)
            shortestOrderObj = {
                'order':0,
                'order_id': seekreturn,
                'distance':timeDistancevalue['distance'],
                'duration':timeDistancevalue['duration']
            }
            shortestOrder.append(shortestOrderObj)
            count += 1
    #print(shortestOrder)
    return shortestOrder

def seekValue(haystack, needle):
    #print(json.dumps(haystack))
    for haystack in haystack:
        for ordvalue in haystack['allOrder']:
            if ordvalue['latitude'] == needle:
                return ordvalue['order_id']

class ShipmentList(generics.ListAPIView):
    # """ List all Edit,Uodate Shipment """
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostShipments.objects.using(company_db).get(pk=pk)
        except EngageboostShipments.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        user = self.get_object(pk,request)
        serializer = ShipmentsSerializer(user)
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
        d1={'modified':datetime.now().date()}
        d2=request.data
        serializer_data=dict(d2,**d1)
        serializer = ShipmentsSerializer(Category,data=serializer_data,partial=True)
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

class PickList(generics.ListAPIView):
    # """ Generate picklist """
    def post(self, request, format=None):
        company_db          = loginview.db_active_connection(request)
        picklist_arr_dict   = {}
        product_ids_qty     = {}
        picklist_details_dict = {}
        picklist_arr        = []
        picklist_order_ids_arr  = []
        existingprdlist     = []
        order_product_id_arr= []
        shipmentType        = request.data["shipmentType"]
        website_id          = request.data["website_id"]
        company_id          = request.data["company_id"]
        order_ids           = request.data["selectedIds"]
        shipment_id         = request.data["shipment_id"]
        userId              = request.data["userId"]
        picklist_Prefix		= 'PCK#'
        orderId_ProductsId	= []
        exist_ship_ment		= 0
        now_utc 			= datetime.now(timezone.utc).astimezone()
        hasPicklistRecord   = EngageboostTrentPicklists.objects.last()
        if hasPicklistRecord:
            lastEntryPickList   = EngageboostTrentPicklists.objects.order_by('-id').latest('id')
            PickListId          = int(lastEntryPickList.id)+int(1)
        else:
            PickListId = 1
        trents_picklist_no = picklist_Prefix+str(PickListId)

        if shipment_id > 0:
            exist_ship_ment = EngageboostShipments.objects.using(company_db).filter(id=shipment_id).count()
            exist_shipment_data  = EngageboostShipments.objects.using(company_db).filter(id=shipment_id).first()
        else:
            exist_picklist = None

        is_picklist_created = 'n'
        if exist_ship_ment > 0 and exist_shipment_data is not None:
            picklist_created_date   = exist_shipment_data.created
            picklist_id             =  exist_shipment_data.picklist_id
            warehouse_id            =  exist_shipment_data.warehouse_id
        else:
            picklist_created_date = now_utc
            picklist_id = 0
            ItemIdsArr = order_ids.split(',')
            # Check picklist created
            # print(ItemIdsArr)
            order_list = EngageboostOrdermaster.objects.filter(id__in=ItemIdsArr, order_status=0).all()
            # print(order_list.query)
            order_data_serializer = OrderMasterSerializer(order_list, many=True)
            warehouse_id = order_data_serializer.data[0]["assign_wh"]
            assign_to = order_data_serializer.data[0]["assign_to"]
            zone_id = order_data_serializer.data[0]["zone_id"]
        if is_picklist_created == 'n' and exist_ship_ment == 0 and shipment_id == 0: # generate Pick list
            shipment_Prefix = "SHM#"
            lastShipment = EngageboostShipments.objects.last()
            if lastShipment:
                lastShipmentId = int(lastShipment.id)+int(1)
            else:
                lastShipmentId = 1

            shipment_id_new = shipment_Prefix+""+str(lastShipmentId)
            try:
                common.update_db_sequences('shipments')
                Shipment = EngageboostShipments.objects.using(company_db).create(custom_shipment_id=shipment_id_new,warehouse_id=warehouse_id,created_by=assign_to,shipment_status='Picking',created=now_utc,modified=now_utc,website_id=website_id) #,zone_id=zone_id
                shipment_id = Shipment.id
                Picklist = EngageboostTrentPicklists.objects.using(company_db).create(
                    trents_picklist_no = trents_picklist_no ,
                    isconfirmed ='Y',
                    is_sub_picklist = 'No' ,
                    picklist_status = 'Picking',
                    modified=now_utc,
                    created=now_utc,
                    warehouse_id=warehouse_id,
                    zone_id=zone_id
                )
                order_ids_arr = order_ids.split(",")
                insert_picklist_id = Picklist.id
                if insert_picklist_id and shipment_id > 0:
                    EngageboostShipments.objects.filter(id=shipment_id).update(picklist_id=insert_picklist_id)
                    EngageboostOrdermaster.objects.filter(id__in=order_ids_arr).update(trent_picklist_id=insert_picklist_id,shipment_id=shipment_id, order_status=100)
                    EngageboostOrderProducts.objects.filter(order_id__in=order_ids_arr).update(trents_picklist_id=insert_picklist_id)
                    rs_order_product = EngageboostOrderProducts.objects.filter(order_id__in=order_ids_arr).values('product_id').annotate(total_quantity=Sum('quantity'))
                    i=0
                    for order_product in rs_order_product:
                        i=i+1
                        rs_orderproduct = EngageboostOrderProducts.objects.filter(product_id=order_product['product_id']).first()
                        pick_mrp            = 0
                        product_tax_price   = 0
                        tax_percentage      = 0
                        tax_name            = ''
                        if rs_orderproduct:
                            pick_mrp = float(rs_orderproduct.product_price)+float(rs_orderproduct.product_discount_price)
                            product_tax_price = rs_orderproduct.product_tax_price
                            tax_percentage = rs_orderproduct.tax_percentage
                            tax_name = rs_orderproduct.tax_name
                            insert_arr = {
                                'sr_no': i,
                                'trent_picklist_id':insert_picklist_id,
                                'product_id':order_product['product_id'],
                                'qty':order_product['total_quantity'],
                                'confirm_quantity':order_product['total_quantity'],
                                'stock_available':'y',
                                'pick_mrp':pick_mrp,
                                'product_tax_price':product_tax_price,
                                'tax_percentage':tax_percentage,
                                'tax_name':tax_name
                            }
                            common.update_db_sequences('trents_picklist_products')
                            EngageboostTrentsPicklistProducts.objects.create(**insert_arr)
                    # Get Order details
                    rs_order = EngageboostOrdermaster.objects.filter(id__in=order_ids_arr).all()
                    if rs_order:
                        for orderdata in order_data_serializer.data:
                            # Insert into shipment order
                            shipment_order_id   = EngageboostShipmentOrders.objects.using(company_db).create(
                                shipment_status = 'Picking',
                                custom_order_id = orderdata['custom_order_id'],
                                webshop_id      = orderdata['webshop']['id'],
                                warehouse_id    = orderdata['assign_wh'],
                                shipping_method_id = orderdata['shipping_method_id'],
                                zone_id = orderdata['zone_id'],
                                order_id = orderdata['id'],
                                shipment = shipment_id,
                                trent_picklist_id=insert_picklist_id
                            )
                            # insert into Shipment order product
                            if len(orderdata['order_products'])>0:
                                for order_products in orderdata['order_products']:
                                    EngageboostShipmentOrderProducts.objects.using(company_db).create(
                                        shipment_status = 'Picking',
                                        quantity        = order_products['quantity'],
                                        warehouse_id    = order_products['assign_wh'],
                                        order_id        = order_products['order'],
                                        order_product_id = order_products['id'],
                                        product_id      = order_products['product']['id'],
                                        shipment     = shipment_id,
                                        shipment_order_id = shipment_order_id.id,
                                        trent_picklist_id=insert_picklist_id,
                                    )
                        if shipment_order_id.id > 0 and shipment_id>0:
                            # Create added by default...by cds on 22Jan2020
                            crate_barcode = 'CRT#123'
                            order_data_save = {
                                "crate_barcode":crate_barcode,
                                "trent_picklist_id":insert_picklist_id,
                                "order_id":orderdata['id'],
                                "created":now_utc
                            }
                            EngageboostCrates.objects.create(**order_data_save)
                            EngageboostShipmentOrders.objects.filter(trent_picklist_id=insert_picklist_id, order_id=orderdata['id']).update(no_of_crates=1)
                            # Create added by default...by cds on 22Jan2020
                            elastic = common.change_field_value_elastic(orderdata['id'],'EngageboostOrdermaster',{'order_status':'100','shipping_status':'Picking'})
                            activityType = 1
                            activity_details = common.save_order_activity(company_db,orderdata['id'],now_utc,7,"Order is Picking",userId,activityType)

                picklist_details_dict = {"shipment_id":shipment_id, "picklist_id":insert_picklist_id}
                data={"status":1,"api_status":'1', "picklist_details": picklist_details_dict, "message": "Picklist has been created successfully" }
            except Exception as error:
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
            return Response(data)
        else:
            try:
                picklist_id = exist_picklist.id
                custom_picklist_id  = exist_picklist.trents_picklist_no
                picklist_data_serializer = TrentPicklistsSerializer(exist_picklist)
                # print(picklist_data_serializer.data)
                warehouseDetails = EngageboostWarehouseMasters.objects.using(company_db).filter(id=exist_picklist.warehouse_id).first()
                warehouse_name = warehouseDetails.name
                shipmentOrders = EngageboostOrdermaster.objects.using(company_db).filter(trent_picklist_id=picklist_id).all()
                if shipmentOrders:
                    shipmentOrders_Serializer = OrderMasterSerializer(shipmentOrders,many=True)
                    for shipment_Orders in shipmentOrders_Serializer.data:
                        picklist_order_ids_arr.append(shipment_Orders["custom_order_id"])
                        zone_id = shipment_Orders["zone_id"]
                    if picklist_order_ids_arr:
                        picklist_order_ids = ",".join(picklist_order_ids_arr)
                    else:
                        picklist_order_ids = ""
                else:
                    picklist_order_ids = ""
                # print(picklist_data_serializer.data)
                for shipmentOrderItem in picklist_data_serializer.data["trents_picklist_products"]:
                    quantity = shipmentOrderItem["qty"]
                    product_id = shipmentOrderItem["product_id"]
                    productDetails = EngageboostProducts.objects.using(company_db).filter(id=product_id).first()
                    productDetails_serializer = EngageboostProductsUomSerializer(productDetails)
                    productDetails_serializer = productDetails_serializer.data
                    productImage = EngageboostProductimages.objects.using(company_db).filter(product_id=product_id,is_cover = 1).first()
                    if productImage and productImage.img:
                        product_image = productImage.img
                    else:
                        product_image = ''

                    if product_id in existingprdlist:
                        for index,item in enumerate(existingprdlist):
                            if item == product_id:
                                order_product_id_arr[index]={"id":product_id,"qty":int(order_product_id_arr[index]["qty"])+int(quantity),"product_name" :productDetails.name,"sku" :productDetails.sku,"ean" :productDetails.ean,"uom" :productDetails_serializer['unit_name'],"picklist_id":picklist_id,"product_image":product_image,"variant":"", "unit_name":productDetails_serializer['unit_name']}
                    else:
                        existingprdlist.append(product_id)
                        product_ids_qty = {"id":product_id,"qty":quantity ,"product_name" :productDetails.name,"sku" :productDetails.sku,"ean" :productDetails.ean,"uom" :productDetails_serializer['unit_name'],"picklist_id":picklist_id,"product_image":product_image,"variant":"", "unit_name":productDetails_serializer['unit_name']}
                        order_product_id_arr.append(product_ids_qty)

                if len(existingprdlist)>0:
                    picklist_product_id = ','.join([str(i) for i in existingprdlist])
                else:
                    picklist_product_id = ''

                if custom_picklist_id is not None:
                    is_picklist_created = 'y'
                else:
                    is_picklist_created = 'n'

                picklist_details_dict = {
                    "picklist_id":picklist_id,
                    "shipment_id":shipment_id,
                    "trents_picklist_no":trents_picklist_no,
                    "picklist_created_date":picklist_created_date,
                    'picklist_order_ids':picklist_order_ids,
                    "warehouse_name":warehouse_name,
                    "is_picklist_created":is_picklist_created,
                    "warehouse_id":warehouse_id,
                    "picklist_product_id":picklist_product_id,
                    "picklist_status":exist_picklist.picklist_status
                }
                data = {"status":1,"api_status": order_product_id_arr, "picklist_details": picklist_details_dict, "message": "Getting the picklist information"}
            except Exception as error:
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
            return Response(data)

class Invoice(generics.ListAPIView):
    # """ Generate picklist """
    def post(self, request, format=None):
        company_db  = loginview.db_active_connection(request)
        now_utc     = datetime.now(timezone.utc).astimezone()
        website_id  = request.data["website_id"]
        company_id  = request.data["company_id"]
        shipment_id = request.data["shipment_id"]
        userId      = request.data["userId"]
        getGlobalSettings = common.getGlobalSettings(company_db, website_id)
        global_setting_date = EngageboostGlobalSettings.objects.using(company_db).get(website_id=website_id,isdeleted='n',isblocked='n')
        global_setting_zone = EngageboostTimezones.objects.using(company_db).get(id = getGlobalSettings['timezone_id'])
        order_id = ''
        final_payment_response = {}
        try:
            if request.data['invoice_create_request'] == 'y':

                order_ids = request.data["selectedIds"]
                order_idsArr = order_ids.split(",")
                shipment_orders = EngageboostShipmentOrders.objects.using(company_db).filter(shipment=shipment_id, order__in=order_idsArr).all()
                shipment_orders_serializer = ShipmentsOrdersSerializer(shipment_orders, many=True)

                if shipment_orders.count() > 0:
                    # shipment_orders_first = shipment_orders.first()
                    # order_id = shipment_orders_first.order_id
                    for shipmentOrder in shipment_orders_serializer.data:
                        order_id = shipmentOrder["order"]["id"]
                        order_id = int(order_id)
                        rs_order_master = EngageboostOrdermaster.objects.filter(id=order_id).first()
                        # if rs_order_master and rs_order_master.payment_type_id == 2 and rs_order_master.payment_method_id == 53:
                        if rs_order_master and rs_order_master.payment_type_id == 2 and rs_order_master.payment_method_id == 51:
                            # if rs_order_master.pay_txntranid is None or rs_order_master.pay_txntranid == '':
                            if rs_order_master.paid_amount <= 0:
                                payment_response = payment_request_si_charge_si(order_id)
                                print('payment_response============', payment_response)
                                if payment_response['status'] == 'failed':
                                    final_payment_response = {'status': payment_response['status'],
                                    'msg': "Please try after sometime",
                                    'msg_1': payment_response['msg'],
                                    'si_ref_no': payment_response['si_ref_no'],
                                    'pay_txntranid': payment_response['pay_txntranid']}
                                else:
                                    final_payment_response = {'status': payment_response['status'],
                                    'msg': payment_response['msg'],
                                    'msg_1': payment_response['msg']}
                            else:
                                final_payment_response = {'status': 'error', 'msg': "Payment Already Done"}

                            if final_payment_response['status'] == 'success':

                                # order wise invoice generate start here......
                            # for shipmentOrder in shipment_orders_serializer.data:
                            #     order_id = shipmentOrder["order"]["id"]
                            #     order_id = int(order_id)
                                warehouse_id = shipmentOrder["warehouse_id"]
                                # if shipmentOrder["shipment_status"] == 'Picking' or shipmentOrder["shipment_status"] == 'Invoicing':
                                if shipmentOrder["shipment_status"] == 'Picking':
                                    error = "Payment is not done by customer."
                                    data = {"status":0,"api_status":0,"error_line":'',"error_message":str(error),"message": str(error)}
                                    return Response(data)
                                # Invoice Creation start here
                                # print(shipment_orders_serializer.data['order'])
                                # print('******************')
                                custom_order_id = shipmentOrder["custom_order_id"]
                                trent_picklist_id = shipmentOrder["trent_picklist_id"]
                                customer_id =  shipmentOrder['order']['customer']['id']
                                shipping_cost = shipmentOrder['order']['shipping_cost']
                                pay_wallet_amount = shipmentOrder['order']['pay_wallet_amount']
                                webshop_id = shipmentOrder['order']['webshop_id']
                                paid_amount = shipmentOrder['order']['paid_amount']
                                shipping_method_id = shipmentOrder['order']['shipping_method_id']
                                cart_discount = shipmentOrder['order']["cart_discount"]
                                net_amount  = 0
                                excise_duty = 0
                                total_tax = 0
                                gross_amount = 0
                                invoice_id = 0
                                isInvoiceCreated = EngageboostInvoicemaster.objects.using(company_db).filter(shipment_id=shipment_id,order_id=order_id).first()
                                if isInvoiceCreated is None:
                                    invoice_id_format = getGlobalSettings["invoice_id_format"]
                                    hasInvoice = EngageboostInvoicemaster.objects.last()
                                    if hasInvoice:
                                        lastInvoiceDetails = EngageboostInvoicemaster.objects.order_by('-id').latest('id')
                                        if lastInvoiceDetails.id:
                                            last_invoice_id = int(lastInvoiceDetails.id)+1
                                            custom_invoice_id = invoice_id_format+""+str(last_invoice_id)
                                        else:
                                            custom_invoice_id = invoice_id_format+""+str(1)
                                    else:
                                        custom_invoice_id = invoice_id_format+""+str(1)

                                    invoiceMaster = EngageboostInvoicemaster.objects.using(company_db).create(website_id=website_id,order_id=order_id,shipment_id=shipment_id,custom_order_id=custom_order_id,customer_id=customer_id,webshop_id=webshop_id,shipping_method_id=shipping_method_id,excise_duty=excise_duty,gross_amount=gross_amount,net_amount=net_amount,paid_amount=paid_amount,trent_picklist_id=trent_picklist_id,created=now_utc,custom_invoice_id=custom_invoice_id,warehouse_id=warehouse_id)
                                    invoice_id = invoiceMaster.id

                                invoice_id = int(invoice_id)
                                if invoice_id>0:
                                    for shipmentOrderProduct in  shipmentOrder["shipment_order_products"]:
                                        #print(shipmentOrderProduct)
                                        product_id = shipmentOrderProduct["product"]["id"]
                                        quantity = shipmentOrderProduct["quantity"]

                                        price = shipmentOrderProduct["order_product"]["product_price"]
                                        product_tax_price = shipmentOrderProduct["order_product"]["product_tax_price"]
                                        product_excise_duty = shipmentOrderProduct["order_product"]["product_excise_duty"]

                                        quantity = shipmentOrderProduct["grn_quantity"]
                                        amount = price*quantity
                                        net_amount = float(net_amount) + float(amount)
                                        if product_tax_price:
                                            total_tax = float(total_tax) + float(quantity)*float(product_tax_price)
                                        if product_excise_duty:
                                            excise_duty = float(excise_duty) + float(quantity)*float(product_excise_duty)

                                        gross_amount = net_amount+excise_duty+total_tax+shipping_cost-float(cart_discount)
                                        # Wallet balance update start...
                                        if gross_amount>pay_wallet_amount:
                                            gross_amount = float(gross_amount-pay_wallet_amount)
                                        else:
                                            refund_wallet= float(pay_wallet_amount-gross_amount)
                                            # common.addCustomerLoyaltypoints()
                                            pay_wallet_amount = gross_amount
                                        # Wallet balance update end..
                                        exist_inv = EngageboostInvoiceProducts.objects.using(company_db).filter(order_id=order_id,invoice_id=invoice_id,product_id=product_id).count()
                                        if exist_inv==0:
                                            invoiceProduct = EngageboostInvoiceProducts.objects.using(company_db).create(order_id=order_id,invoice_id=invoice_id,product_id=product_id,quantity=quantity,price=price)
                                        EngageboostShipmentOrderProducts.objects.using(company_db).filter(order_id=order_id,product_id=product_id,shipment=shipment_id,shipment_status__in=['Invoicing','Packed']).update(shipment_status='Shipment Processing')

                                    EngageboostInvoicemaster.objects.filter(id=invoice_id).update(net_amount=net_amount,excise_duty=excise_duty,gross_amount=gross_amount)
                                    EngageboostShipmentOrders.objects.using(company_db).filter(order_id=order_id,shipment=shipment_id,shipment_status__in=['Invoicing','Packed']).update(shipment_status='Shipment Processing')

                                    AllshipmentOrder = EngageboostShipmentOrders.objects.filter(shipment=shipment_id, shipment_status__in=['Picking','Packed','Invoicing']).all()
                                    if len(AllshipmentOrder)>0:
                                        pass
                                    else:
                                        EngageboostShipments.objects.filter(id=shipment_id,shipment_status__in=['Invoicing','Packed']).update(shipment_status='Shipment Processing')
                                        EngageboostTrentPicklists.objects.filter(id=trent_picklist_id,picklist_status__in=['Invoicing','Packed']).update(picklist_status='Shipment Processing')

                                    if request.data["invoice_email"] == 'y':
                                        pass ### send email functiolity goes here.
                                    # order activity set
                                    activityType = 1
                                    activity_details = common.save_order_activity(company_db,order_id,now_utc,7,"Order is Shipment Processing",userId,activityType)
                                    elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'shipping_status':'Shipment Processing'})
                                    # Invoice Creation end here
                                # order wise invoice generate end here......
                                # Making delivery planner start here...
                                if order_idsArr and len(order_idsArr) > 0:
                                    totalVechicle = create_automatic_delivery_plan(order_idsArr, shipment_id, warehouse_id)
                                    EngageboostShipments.objects.filter(id=shipment_id).update(no_of_vehicles=totalVechicle)
                                # Making delivery planner end here...

                                # common.email_send_by_AutoResponder(order_id, 29)
                                common.sms_send_by_AutoResponder(order_id, '', 29, '')
                        else:
                            # order wise invoice generate start here......
                        # for shipmentOrder in shipment_orders_serializer.data:
                        #     order_id = shipmentOrder["order"]["id"]
                        #     order_id = int(order_id)
                            warehouse_id = shipmentOrder["warehouse_id"]
                            # if shipmentOrder["shipment_status"] == 'Picking' or shipmentOrder["shipment_status"] == 'Invoicing':
                            if shipmentOrder["shipment_status"] == 'Picking':
                                error = "Payment is not done by customer."
                                data = {"status": 0, "api_status": 0, "error_line": '', "error_message": str(error),
                                        "message": str(error)}
                                return Response(data)
                            # Invoice Creation start here
                            # print(shipment_orders_serializer.data['order'])
                            # print('******************')
                            custom_order_id = shipmentOrder["custom_order_id"]
                            trent_picklist_id = shipmentOrder["trent_picklist_id"]
                            customer_id = shipmentOrder['order']['customer']['id']
                            shipping_cost = shipmentOrder['order']['shipping_cost']
                            pay_wallet_amount = shipmentOrder['order']['pay_wallet_amount']
                            webshop_id = shipmentOrder['order']['webshop_id']
                            paid_amount = shipmentOrder['order']['paid_amount']
                            shipping_method_id = shipmentOrder['order']['shipping_method_id']
                            cart_discount = shipmentOrder['order']["cart_discount"]
                            net_amount = 0
                            excise_duty = 0
                            total_tax = 0
                            gross_amount = 0
                            invoice_id = 0
                            isInvoiceCreated = EngageboostInvoicemaster.objects.using(company_db).filter(
                                shipment_id=shipment_id, order_id=order_id).first()
                            if isInvoiceCreated is None:
                                invoice_id_format = getGlobalSettings["invoice_id_format"]
                                hasInvoice = EngageboostInvoicemaster.objects.last()
                                if hasInvoice:
                                    lastInvoiceDetails = EngageboostInvoicemaster.objects.order_by('-id').latest('id')
                                    if lastInvoiceDetails.id:
                                        last_invoice_id = int(lastInvoiceDetails.id) + 1
                                        custom_invoice_id = invoice_id_format + "" + str(last_invoice_id)
                                    else:
                                        custom_invoice_id = invoice_id_format + "" + str(1)
                                else:
                                    custom_invoice_id = invoice_id_format + "" + str(1)

                                invoiceMaster = EngageboostInvoicemaster.objects.using(company_db).create(
                                    website_id=website_id, order_id=order_id, shipment_id=shipment_id,
                                    custom_order_id=custom_order_id, customer_id=customer_id, webshop_id=webshop_id,
                                    shipping_method_id=shipping_method_id, excise_duty=excise_duty,
                                    gross_amount=gross_amount, net_amount=net_amount, paid_amount=paid_amount,
                                    trent_picklist_id=trent_picklist_id, created=now_utc,
                                    custom_invoice_id=custom_invoice_id, warehouse_id=warehouse_id)
                                invoice_id = invoiceMaster.id

                            invoice_id = int(invoice_id)
                            if invoice_id > 0:
                                for shipmentOrderProduct in shipmentOrder["shipment_order_products"]:
                                    # print(shipmentOrderProduct)
                                    product_id = shipmentOrderProduct["product"]["id"]
                                    quantity = shipmentOrderProduct["quantity"]

                                    price = shipmentOrderProduct["order_product"]["product_price"]
                                    product_tax_price = shipmentOrderProduct["order_product"]["product_tax_price"]
                                    product_excise_duty = shipmentOrderProduct["order_product"]["product_excise_duty"]

                                    quantity = shipmentOrderProduct["grn_quantity"]
                                    amount = price * quantity
                                    net_amount = float(net_amount) + float(amount)
                                    if product_tax_price:
                                        total_tax = float(total_tax) + float(quantity) * float(product_tax_price)
                                    if product_excise_duty:
                                        excise_duty = float(excise_duty) + float(quantity) * float(product_excise_duty)

                                    gross_amount = net_amount + excise_duty + total_tax + shipping_cost - float(
                                        cart_discount)
                                    # Wallet balance update start...
                                    if gross_amount > pay_wallet_amount:
                                        gross_amount = float(gross_amount - pay_wallet_amount)
                                    else:
                                        refund_wallet = float(pay_wallet_amount - gross_amount)
                                        # common.addCustomerLoyaltypoints()
                                        pay_wallet_amount = gross_amount
                                    # Wallet balance update end..
                                    exist_inv = EngageboostInvoiceProducts.objects.using(company_db).filter(
                                        order_id=order_id, invoice_id=invoice_id, product_id=product_id).count()
                                    if exist_inv == 0:
                                        invoiceProduct = EngageboostInvoiceProducts.objects.using(company_db).create(
                                            order_id=order_id, invoice_id=invoice_id, product_id=product_id,
                                            quantity=quantity, price=price)
                                    EngageboostShipmentOrderProducts.objects.using(company_db).filter(order_id=order_id,
                                                                                                      product_id=product_id,
                                                                                                      shipment=shipment_id,
                                                                                                      shipment_status__in=[
                                                                                                          'Invoicing',
                                                                                                          'Packed']).update(
                                        shipment_status='Shipment Processing')

                                EngageboostInvoicemaster.objects.filter(id=invoice_id).update(net_amount=net_amount,
                                                                                              excise_duty=excise_duty,
                                                                                              gross_amount=gross_amount)
                                EngageboostShipmentOrders.objects.using(company_db).filter(order_id=order_id,
                                                                                           shipment=shipment_id,
                                                                                           shipment_status__in=[
                                                                                               'Invoicing',
                                                                                               'Packed']).update(
                                    shipment_status='Shipment Processing')

                                AllshipmentOrder = EngageboostShipmentOrders.objects.filter(shipment=shipment_id,
                                                                                            shipment_status__in=[
                                                                                                'Picking', 'Packed',
                                                                                                'Invoicing']).all()
                                if len(AllshipmentOrder) > 0:
                                    pass
                                else:
                                    EngageboostShipments.objects.filter(id=shipment_id,
                                                                        shipment_status__in=['Invoicing',
                                                                                             'Packed']).update(
                                        shipment_status='Shipment Processing')
                                    EngageboostTrentPicklists.objects.filter(id=trent_picklist_id,
                                                                             picklist_status__in=['Invoicing',
                                                                                                  'Packed']).update(
                                        picklist_status='Shipment Processing')

                                if request.data["invoice_email"] == 'y':
                                    pass  ### send email functiolity goes here.
                                # order activity set
                                activityType = 1
                                activity_details = common.save_order_activity(company_db, order_id, now_utc, 7,
                                                                              "Order is Shipment Processing", userId,
                                                                              activityType)
                                elastic = common.change_field_value_elastic(order_id, 'EngageboostOrdermaster',
                                                                            {'shipping_status': 'Shipment Processing'})
                                # Invoice Creation end here
                            # order wise invoice generate end here......
                            # Making delivery planner start here...
                            if order_idsArr and len(order_idsArr) > 0:
                                totalVechicle = create_automatic_delivery_plan(order_idsArr, shipment_id, warehouse_id)
                                EngageboostShipments.objects.filter(id=shipment_id).update(no_of_vehicles=totalVechicle)
                            # Making delivery planner end here...

                            final_payment_response = {'status': 'success', 'msg': "Offline payment"}
            # display invoice order listing....
            shipment_status = ['Picking']
            shipment_order = EngageboostShipmentOrders.objects.using(company_db).filter(shipment=shipment_id).exclude(shipment_status__in=shipment_status).all()
            # shipment_orders_serializer = ShipmentsOrdersSerializer(shipment_order,many=True)
            shipment_orders_serializer = ShipmentsOrdersViewSerializer(shipment_order,many=True)
            count_invoice = 0
            picklist_id = 0
            # print('ShipmentsOrdersSerializer===========', json.dumps(shipment_orders_serializer.data))
            for shipmentOrder in shipment_orders_serializer.data:
                order_id = shipmentOrder["order"]["id"]
                picklist_id = shipmentOrder["trent_picklist_id"]
                shipmentOrder["order_details"] = shipmentOrder["order"]
                # start Date time format setting...
                shipmentOrder['order_details']['created'] = common.get_time(shipmentOrder["order"]["created"],global_setting_zone, global_setting_date)
                shipmentOrder['order_details']['time_slot_date'] = common.get_date_from_datetime(shipmentOrder["order"]["time_slot_date"],global_setting_zone, global_setting_date,'%Y-%m-%d')
                # end Date time format setting...
                # if shipmentOrder['shipment_order_products']:
                # 	for shipmentOrderProduct in shipmentOrder['shipment_order_products']:
                # 		# orderProductDetails = EngageboostOrderProducts.objects.using(company_db).filter(order_id=shipmentOrderProduct['order']['id'],product_id=shipmentOrderProduct['product']['id']).first()
                # 		# orderProductDetails_serializer = OrderProductsSerializer(orderProductDetails)
                # 		# shipmentOrderProduct['order_product_details']=orderProductDetails_serializer.data
                # 		# warehouseDetails = EngageboostWarehouseMasters.objects.using(company_db).filter(id=shipmentOrderProduct['warehouse_id']).all()
                # 		warehouseDetails = EngageboostWarehouseMasters.objects.using(company_db).filter(id=shipmentOrder['warehouse_id']).first()
                # 		shipmentOrderProduct['warehouse_name'] = warehouseDetails.name

                invoiceDetails = EngageboostInvoicemaster.objects.using(company_db).filter(shipment_id=shipment_id,order_id=order_id).first()
                if invoiceDetails is not None:
                    shipmentOrder['created_date'] = common.get_date_from_datetime(invoiceDetails.created,global_setting_zone, global_setting_date,'%Y-%m-%d')
                    shipmentOrder["custom_invoice_id"] = invoiceDetails.custom_invoice_id
                    count_invoice = int(count_invoice)+1
                shipmentOrder["count_invoice"] = count_invoice
                driverName = ''
                vehicle_no = ''
                if shipmentOrder["order"]["shipment_id"]:
                    shipment_id = shipmentOrder["order"]["shipment_id"]
                    driverVehicleMap = EngageboostDriverVeichleMap.objects.filter(shipment_id=shipment_id).first()
                    if driverVehicleMap:
                        driver_id = driverVehicleMap.user_id
                        vehicle_id = driverVehicleMap.vehicle_id
                        if driver_id > 0:
                            driverManagerdata = EngageboostDeliveryManagers.objects.filter(user_id=driver_id).first()
                            driverName = driverManagerdata.name
                        if vehicle_id > 0 :
                            vehicleData = EngageboostVehicleMasters.objects.filter(id=vehicle_id).first()
                            vehicle_no = vehicleData.vehicle_number

                    deliveryPlanOrder = EngageboostDeliveryPlanOrder.objects.filter(order_id=order_id,shipment_id=shipment_id).first()
                    if deliveryPlanOrder:
                        distance = deliveryPlanOrder.distance;
                        virtual_vehicle_id = deliveryPlanOrder.virtual_vechile_id;
                        if distance>1000:
                            distance = str( float("{0:.2f}".format(distance/1000))) + ' Km'
                        else:
                            distance = str( float("{0:.2f}".format(distance))) + ' mtr'

                        time = deliveryPlanOrder.time;
                        if time>3600:
                            time = str( float("{0:.2f}".format(time/3600))) + ' Hr'
                        else:
                            time = str( float("{0:.2f}".format(time/60))) + ' Min'
                shipmentOrder['order_details']['DriverName'] = driverName
                shipmentOrder['order_details']['vehicle_no'] = vehicle_no
            # final_payment_response = {}
            if count_invoice > 0:
                is_invoice_created = 'Y'
                # rs_order_master = EngageboostOrdermaster.objects.filter(id=order_id).first()
                # # if rs_order_master and rs_order_master.payment_type_id == 2 and rs_order_master.payment_method_id == 53:
                # if rs_order_master and rs_order_master.payment_type_id == 2 and rs_order_master.payment_method_id == 51:
                # 	if rs_order_master.pay_txntranid is None or rs_order_master.pay_txntranid == '':
                # 		final_payment_response = payment_request_si_charge(order_id)
                # 	else:
                # 		final_payment_response = {'status': 'error', 'msg': "duplicate_invoice_created"}
            else:
                is_invoice_created = 'N'
                # final_payment_response = {'status': 'error', 'msg': "no_invoice_created"}
            data={"status":1,"api_status":'1', "InvoiceDetails":shipment_orders_serializer.data,'picklist_id':picklist_id,'shipment_id':shipment_id,"message": "Getting the Invoice Informations","is_invoice_created":is_invoice_created, "payment_response": final_payment_response}
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

class Invoice_new(generics.ListAPIView):
    # """ Generate picklist """
    def post(self, request, format=None):
        company_db  = loginview.db_active_connection(request)
        now_utc     = datetime.now(timezone.utc).astimezone()
        website_id  = request.data["website_id"]
        company_id  = request.data["company_id"]
        shipment_id = request.data["shipment_id"]
        userId      = request.data["userId"]
        getGlobalSettings = common.getGlobalSettings(company_db, website_id)
        global_setting_date = EngageboostGlobalSettings.objects.using(company_db).get(website_id=website_id,isdeleted='n',isblocked='n')
        global_setting_zone = EngageboostTimezones.objects.using(company_db).get(id = getGlobalSettings['timezone_id'])
        order_id = ''
        final_payment_response = {}
        try:
            if request.data['invoice_create_request'] == 'y':

                order_ids = request.data["selectedIds"]
                order_idsArr = order_ids.split(",")
                shipment_orders = EngageboostShipmentOrders.objects.using(company_db).filter(shipment=shipment_id, order__in=order_idsArr).all()
                shipment_orders_serializer = ShipmentsOrdersSerializer(shipment_orders, many=True)

                if shipment_orders.count() > 0:
                    shipment_orders_first = shipment_orders.first()
                    order_id = shipment_orders_first.order_id

                    rs_order_master = EngageboostOrdermaster.objects.filter(id=order_id).first()
                    # if rs_order_master and rs_order_master.payment_type_id == 2 and rs_order_master.payment_method_id == 53:
                    if rs_order_master and rs_order_master.payment_type_id == 2 and rs_order_master.payment_method_id == 51:
                        # if rs_order_master.pay_txntranid is None or rs_order_master.pay_txntranid == '':
                        if rs_order_master.paid_amount <= 0:
                            payment_response = payment_request_si_charge(order_id)
                            if payment_response['status'] == 'failed':
                                final_payment_response = {'status': payment_response['status'],
                                                          'msg': "Please try after sometime",
                                                          'msg_1': payment_response['msg'],
                                                          'si_ref_no': payment_response['si_ref_no'],
                                                          'pay_txntranid': payment_response['pay_txntranid']}
                            else:
                                final_payment_response = {'status': payment_response['status'],
                                                          'msg': payment_response['msg'],
                                                          'msg_1': payment_response['msg']}
                        else:
                            final_payment_response = {'status': 'error', 'msg': "Payment Already Done"}

                        if final_payment_response['status'] == 'success':

                            # order wise invoice generate start here......
                            for shipmentOrder in shipment_orders_serializer.data:
                                order_id = shipmentOrder["order"]["id"]
                                order_id = int(order_id)
                                warehouse_id = shipmentOrder["warehouse_id"]
                                # if shipmentOrder["shipment_status"] == 'Picking' or shipmentOrder["shipment_status"] == 'Invoicing':
                                if shipmentOrder["shipment_status"] == 'Picking':
                                    error = "Payment is not done by customer."
                                    data = {"status":0,"api_status":0,"error_line":'',"error_message":str(error),"message": str(error)}
                                    return Response(data)
                                # Invoice Creation start here
                                # print(shipment_orders_serializer.data['order'])
                                # print('******************')
                                custom_order_id = shipmentOrder["custom_order_id"]
                                trent_picklist_id = shipmentOrder["trent_picklist_id"]
                                customer_id =  shipmentOrder['order']['customer']['id']
                                shipping_cost = shipmentOrder['order']['shipping_cost']
                                pay_wallet_amount = shipmentOrder['order']['pay_wallet_amount']
                                webshop_id = shipmentOrder['order']['webshop_id']
                                paid_amount = shipmentOrder['order']['paid_amount']
                                shipping_method_id = shipmentOrder['order']['shipping_method_id']
                                cart_discount = shipmentOrder['order']["cart_discount"]
                                net_amount  = 0
                                excise_duty = 0
                                total_tax = 0
                                gross_amount = 0
                                invoice_id = 0
                                isInvoiceCreated = EngageboostInvoicemaster.objects.using(company_db).filter(shipment_id=shipment_id,order_id=order_id).first()
                                if isInvoiceCreated is None:
                                    invoice_id_format = getGlobalSettings["invoice_id_format"]
                                    hasInvoice = EngageboostInvoicemaster.objects.last()
                                    if hasInvoice:
                                        lastInvoiceDetails = EngageboostInvoicemaster.objects.order_by('-id').latest('id')
                                        if lastInvoiceDetails.id:
                                            last_invoice_id = int(lastInvoiceDetails.id)+1
                                            custom_invoice_id = invoice_id_format+""+str(last_invoice_id)
                                        else:
                                            custom_invoice_id = invoice_id_format+""+str(1)
                                    else:
                                        custom_invoice_id = invoice_id_format+""+str(1)

                                    invoiceMaster = EngageboostInvoicemaster.objects.using(company_db).create(website_id=website_id,order_id=order_id,shipment_id=shipment_id,custom_order_id=custom_order_id,customer_id=customer_id,webshop_id=webshop_id,shipping_method_id=shipping_method_id,excise_duty=excise_duty,gross_amount=gross_amount,net_amount=net_amount,paid_amount=paid_amount,trent_picklist_id=trent_picklist_id,created=now_utc,custom_invoice_id=custom_invoice_id,warehouse_id=warehouse_id)
                                    invoice_id = invoiceMaster.id

                                invoice_id = int(invoice_id)
                                if invoice_id>0:
                                    for shipmentOrderProduct in  shipmentOrder["shipment_order_products"]:
                                        #print(shipmentOrderProduct)
                                        product_id = shipmentOrderProduct["product"]["id"]
                                        quantity = shipmentOrderProduct["quantity"]

                                        price = shipmentOrderProduct["order_product"]["product_price"]
                                        product_tax_price = shipmentOrderProduct["order_product"]["product_tax_price"]
                                        product_excise_duty = shipmentOrderProduct["order_product"]["product_excise_duty"]

                                        quantity = shipmentOrderProduct["grn_quantity"]
                                        amount = price*quantity
                                        net_amount = float(net_amount) + float(amount)
                                        if product_tax_price:
                                            total_tax = float(total_tax) + float(quantity)*float(product_tax_price)
                                        if product_excise_duty:
                                            excise_duty = float(excise_duty) + float(quantity)*float(product_excise_duty)

                                        gross_amount = net_amount+excise_duty+total_tax+shipping_cost-float(cart_discount)
                                        # Wallet balance update start...
                                        if gross_amount>pay_wallet_amount:
                                            gross_amount = float(gross_amount-pay_wallet_amount)
                                        else:
                                            refund_wallet= float(pay_wallet_amount-gross_amount)
                                            # common.addCustomerLoyaltypoints()
                                            pay_wallet_amount = gross_amount
                                        # Wallet balance update end..
                                        exist_inv = EngageboostInvoiceProducts.objects.using(company_db).filter(order_id=order_id,invoice_id=invoice_id,product_id=product_id).count()
                                        if exist_inv==0:
                                            invoiceProduct = EngageboostInvoiceProducts.objects.using(company_db).create(order_id=order_id,invoice_id=invoice_id,product_id=product_id,quantity=quantity,price=price)
                                        EngageboostShipmentOrderProducts.objects.using(company_db).filter(order_id=order_id,product_id=product_id,shipment=shipment_id,shipment_status__in=['Invoicing','Packed']).update(shipment_status='Shipment Processing')

                                    EngageboostInvoicemaster.objects.filter(id=invoice_id).update(net_amount=net_amount,excise_duty=excise_duty,gross_amount=gross_amount)
                                    EngageboostShipmentOrders.objects.using(company_db).filter(order_id=order_id,shipment=shipment_id,shipment_status__in=['Invoicing','Packed']).update(shipment_status='Shipment Processing')

                                    AllshipmentOrder = EngageboostShipmentOrders.objects.filter(shipment=shipment_id, shipment_status__in=['Picking','Packed','Invoicing']).all()
                                    if len(AllshipmentOrder)>0:
                                        pass
                                    else:
                                        EngageboostShipments.objects.filter(id=shipment_id,shipment_status__in=['Invoicing','Packed']).update(shipment_status='Shipment Processing')
                                        EngageboostTrentPicklists.objects.filter(id=trent_picklist_id,picklist_status__in=['Invoicing','Packed']).update(picklist_status='Shipment Processing')

                                    if request.data["invoice_email"] == 'y':
                                        pass ### send email functiolity goes here.
                                    # order activity set
                                    activityType = 1
                                    activity_details = common.save_order_activity(company_db,order_id,now_utc,7,"Order is Shipment Processing",userId,activityType)
                                    elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'shipping_status':'Shipment Processing'})
                                    # Invoice Creation end here
                                # order wise invoice generate end here......
                                # Making delivery planner start here...
                                if order_idsArr and len(order_idsArr) > 0:
                                    totalVechicle = create_automatic_delivery_plan(order_idsArr, shipment_id, warehouse_id)
                                    EngageboostShipments.objects.filter(id=shipment_id).update(no_of_vehicles=totalVechicle)
                                # Making delivery planner end here...
                    else:
                        # order wise invoice generate start here......
                        for shipmentOrder in shipment_orders_serializer.data:
                            order_id = shipmentOrder["order"]["id"]
                            order_id = int(order_id)
                            warehouse_id = shipmentOrder["warehouse_id"]
                            # if shipmentOrder["shipment_status"] == 'Picking' or shipmentOrder["shipment_status"] == 'Invoicing':
                            if shipmentOrder["shipment_status"] == 'Picking':
                                error = "Payment is not done by customer."
                                data = {"status": 0, "api_status": 0, "error_line": '', "error_message": str(error),
                                        "message": str(error)}
                                return Response(data)
                            # Invoice Creation start here
                            # print(shipment_orders_serializer.data['order'])
                            # print('******************')
                            custom_order_id = shipmentOrder["custom_order_id"]
                            trent_picklist_id = shipmentOrder["trent_picklist_id"]
                            customer_id = shipmentOrder['order']['customer']['id']
                            shipping_cost = shipmentOrder['order']['shipping_cost']
                            pay_wallet_amount = shipmentOrder['order']['pay_wallet_amount']
                            webshop_id = shipmentOrder['order']['webshop_id']
                            paid_amount = shipmentOrder['order']['paid_amount']
                            shipping_method_id = shipmentOrder['order']['shipping_method_id']
                            cart_discount = shipmentOrder['order']["cart_discount"]
                            net_amount = 0
                            excise_duty = 0
                            total_tax = 0
                            gross_amount = 0
                            invoice_id = 0
                            isInvoiceCreated = EngageboostInvoicemaster.objects.using(company_db).filter(
                                shipment_id=shipment_id, order_id=order_id).first()
                            if isInvoiceCreated is None:
                                invoice_id_format = getGlobalSettings["invoice_id_format"]
                                hasInvoice = EngageboostInvoicemaster.objects.last()
                                if hasInvoice:
                                    lastInvoiceDetails = EngageboostInvoicemaster.objects.order_by('-id').latest('id')
                                    if lastInvoiceDetails.id:
                                        last_invoice_id = int(lastInvoiceDetails.id) + 1
                                        custom_invoice_id = invoice_id_format + "" + str(last_invoice_id)
                                    else:
                                        custom_invoice_id = invoice_id_format + "" + str(1)
                                else:
                                    custom_invoice_id = invoice_id_format + "" + str(1)

                                invoiceMaster = EngageboostInvoicemaster.objects.using(company_db).create(
                                    website_id=website_id, order_id=order_id, shipment_id=shipment_id,
                                    custom_order_id=custom_order_id, customer_id=customer_id, webshop_id=webshop_id,
                                    shipping_method_id=shipping_method_id, excise_duty=excise_duty,
                                    gross_amount=gross_amount, net_amount=net_amount, paid_amount=paid_amount,
                                    trent_picklist_id=trent_picklist_id, created=now_utc,
                                    custom_invoice_id=custom_invoice_id, warehouse_id=warehouse_id)
                                invoice_id = invoiceMaster.id

                            invoice_id = int(invoice_id)
                            if invoice_id > 0:
                                for shipmentOrderProduct in shipmentOrder["shipment_order_products"]:
                                    # print(shipmentOrderProduct)
                                    product_id = shipmentOrderProduct["product"]["id"]
                                    quantity = shipmentOrderProduct["quantity"]

                                    price = shipmentOrderProduct["order_product"]["product_price"]
                                    product_tax_price = shipmentOrderProduct["order_product"]["product_tax_price"]
                                    product_excise_duty = shipmentOrderProduct["order_product"]["product_excise_duty"]

                                    quantity = shipmentOrderProduct["grn_quantity"]
                                    amount = price * quantity
                                    net_amount = float(net_amount) + float(amount)
                                    if product_tax_price:
                                        total_tax = float(total_tax) + float(quantity) * float(product_tax_price)
                                    if product_excise_duty:
                                        excise_duty = float(excise_duty) + float(quantity) * float(product_excise_duty)

                                    gross_amount = net_amount + excise_duty + total_tax + shipping_cost - float(
                                        cart_discount)
                                    # Wallet balance update start...
                                    if gross_amount > pay_wallet_amount:
                                        gross_amount = float(gross_amount - pay_wallet_amount)
                                    else:
                                        refund_wallet = float(pay_wallet_amount - gross_amount)
                                        # common.addCustomerLoyaltypoints()
                                        pay_wallet_amount = gross_amount
                                    # Wallet balance update end..
                                    exist_inv = EngageboostInvoiceProducts.objects.using(company_db).filter(
                                        order_id=order_id, invoice_id=invoice_id, product_id=product_id).count()
                                    if exist_inv == 0:
                                        invoiceProduct = EngageboostInvoiceProducts.objects.using(company_db).create(
                                            order_id=order_id, invoice_id=invoice_id, product_id=product_id,
                                            quantity=quantity, price=price)
                                    EngageboostShipmentOrderProducts.objects.using(company_db).filter(order_id=order_id,
                                                                                                      product_id=product_id,
                                                                                                      shipment=shipment_id,
                                                                                                      shipment_status__in=[
                                                                                                          'Invoicing',
                                                                                                          'Packed']).update(
                                        shipment_status='Shipment Processing')

                                EngageboostInvoicemaster.objects.filter(id=invoice_id).update(net_amount=net_amount,
                                                                                              excise_duty=excise_duty,
                                                                                              gross_amount=gross_amount)
                                EngageboostShipmentOrders.objects.using(company_db).filter(order_id=order_id,
                                                                                           shipment=shipment_id,
                                                                                           shipment_status__in=[
                                                                                               'Invoicing',
                                                                                               'Packed']).update(
                                    shipment_status='Shipment Processing')

                                AllshipmentOrder = EngageboostShipmentOrders.objects.filter(shipment=shipment_id,
                                                                                            shipment_status__in=[
                                                                                                'Picking', 'Packed',
                                                                                                'Invoicing']).all()
                                if len(AllshipmentOrder) > 0:
                                    pass
                                else:
                                    EngageboostShipments.objects.filter(id=shipment_id,
                                                                        shipment_status__in=['Invoicing',
                                                                                             'Packed']).update(
                                        shipment_status='Shipment Processing')
                                    EngageboostTrentPicklists.objects.filter(id=trent_picklist_id,
                                                                             picklist_status__in=['Invoicing',
                                                                                                  'Packed']).update(
                                        picklist_status='Shipment Processing')

                                if request.data["invoice_email"] == 'y':
                                    pass  ### send email functiolity goes here.
                                # order activity set
                                activityType = 1
                                activity_details = common.save_order_activity(company_db, order_id, now_utc, 7,
                                                                              "Order is Shipment Processing", userId,
                                                                              activityType)
                                elastic = common.change_field_value_elastic(order_id, 'EngageboostOrdermaster',
                                                                            {'shipping_status': 'Shipment Processing'})
                                # Invoice Creation end here
                            # order wise invoice generate end here......
                            # Making delivery planner start here...
                            if order_idsArr and len(order_idsArr) > 0:
                                totalVechicle = create_automatic_delivery_plan(order_idsArr, shipment_id, warehouse_id)
                                EngageboostShipments.objects.filter(id=shipment_id).update(no_of_vehicles=totalVechicle)
                            # Making delivery planner end here...

                        final_payment_response = {'status': 'success', 'msg': "Offline payment"}
            # display invoice order listing....
            shipment_status = ['Picking']
            shipment_order = EngageboostShipmentOrders.objects.using(company_db).filter(shipment=shipment_id).exclude(shipment_status__in=shipment_status).all()
            # shipment_orders_serializer = ShipmentsOrdersSerializer(shipment_order,many=True)
            shipment_orders_serializer = ShipmentsOrdersViewSerializer(shipment_order,many=True)
            count_invoice = 0
            picklist_id = 0
            # print('ShipmentsOrdersSerializer===========', json.dumps(shipment_orders_serializer.data))
            for shipmentOrder in shipment_orders_serializer.data:
                order_id = shipmentOrder["order"]["id"]
                picklist_id = shipmentOrder["trent_picklist_id"]
                shipmentOrder["order_details"] = shipmentOrder["order"]
                # start Date time format setting...
                shipmentOrder['order_details']['created'] = common.get_time(shipmentOrder["order"]["created"],global_setting_zone, global_setting_date)
                shipmentOrder['order_details']['time_slot_date'] = common.get_date_from_datetime(shipmentOrder["order"]["time_slot_date"],global_setting_zone, global_setting_date,'%Y-%m-%d')
                # end Date time format setting...
                # if shipmentOrder['shipment_order_products']:
                # 	for shipmentOrderProduct in shipmentOrder['shipment_order_products']:
                # 		# orderProductDetails = EngageboostOrderProducts.objects.using(company_db).filter(order_id=shipmentOrderProduct['order']['id'],product_id=shipmentOrderProduct['product']['id']).first()
                # 		# orderProductDetails_serializer = OrderProductsSerializer(orderProductDetails)
                # 		# shipmentOrderProduct['order_product_details']=orderProductDetails_serializer.data
                # 		# warehouseDetails = EngageboostWarehouseMasters.objects.using(company_db).filter(id=shipmentOrderProduct['warehouse_id']).all()
                # 		warehouseDetails = EngageboostWarehouseMasters.objects.using(company_db).filter(id=shipmentOrder['warehouse_id']).first()
                # 		shipmentOrderProduct['warehouse_name'] = warehouseDetails.name

                invoiceDetails = EngageboostInvoicemaster.objects.using(company_db).filter(shipment_id=shipment_id,order_id=order_id).first()
                if invoiceDetails is not None:
                    shipmentOrder['created_date'] = common.get_date_from_datetime(invoiceDetails.created,global_setting_zone, global_setting_date,'%Y-%m-%d')
                    shipmentOrder["custom_invoice_id"] = invoiceDetails.custom_invoice_id
                    count_invoice = int(count_invoice)+1
                shipmentOrder["count_invoice"] = count_invoice
                driverName = ''
                vehicle_no = ''
                if shipmentOrder["order"]["shipment_id"]:
                    shipment_id = shipmentOrder["order"]["shipment_id"]
                    driverVehicleMap = EngageboostDriverVeichleMap.objects.filter(shipment_id=shipment_id).first()
                    if driverVehicleMap:
                        driver_id = driverVehicleMap.user_id
                        vehicle_id = driverVehicleMap.vehicle_id
                        if driver_id > 0:
                            driverManagerdata = EngageboostDeliveryManagers.objects.filter(user_id=driver_id).first()
                            driverName = driverManagerdata.name
                        if vehicle_id > 0 :
                            vehicleData = EngageboostVehicleMasters.objects.filter(id=vehicle_id).first()
                            vehicle_no = vehicleData.vehicle_number

                    deliveryPlanOrder = EngageboostDeliveryPlanOrder.objects.filter(order_id=order_id,shipment_id=shipment_id).first()
                    if deliveryPlanOrder:
                        distance = deliveryPlanOrder.distance;
                        virtual_vehicle_id = deliveryPlanOrder.virtual_vechile_id;
                        if distance>1000:
                            distance = str( float("{0:.2f}".format(distance/1000))) + ' Km'
                        else:
                            distance = str( float("{0:.2f}".format(distance))) + ' mtr'

                        time = deliveryPlanOrder.time;
                        if time>3600:
                            time = str( float("{0:.2f}".format(time/3600))) + ' Hr'
                        else:
                            time = str( float("{0:.2f}".format(time/60))) + ' Min'
                shipmentOrder['order_details']['DriverName'] = driverName
                shipmentOrder['order_details']['vehicle_no'] = vehicle_no
            # final_payment_response = {}
            if count_invoice > 0:
                is_invoice_created = 'Y'
                # rs_order_master = EngageboostOrdermaster.objects.filter(id=order_id).first()
                # # if rs_order_master and rs_order_master.payment_type_id == 2 and rs_order_master.payment_method_id == 53:
                # if rs_order_master and rs_order_master.payment_type_id == 2 and rs_order_master.payment_method_id == 51:
                # 	if rs_order_master.pay_txntranid is None or rs_order_master.pay_txntranid == '':
                # 		final_payment_response = payment_request_si_charge(order_id)
                # 	else:
                # 		final_payment_response = {'status': 'error', 'msg': "duplicate_invoice_created"}
            else:
                is_invoice_created = 'N'
                # final_payment_response = {'status': 'error', 'msg': "no_invoice_created"}
            data={"status":1,"api_status":'1', "InvoiceDetails":shipment_orders_serializer.data,'picklist_id':picklist_id,'shipment_id':shipment_id,"message": "Getting the Invoice Informations","is_invoice_created":is_invoice_created, "payment_response": final_payment_response}
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

class Invoice_si(generics.ListAPIView):
    # """ Generate picklist """
    def post(self, request, format=None):
        company_db  = loginview.db_active_connection(request)
        now_utc     = datetime.now(timezone.utc).astimezone()
        website_id  = request.data["website_id"]
        company_id  = request.data["company_id"]
        shipment_id = request.data["shipment_id"]
        userId      = request.data["userId"]
        getGlobalSettings = common.getGlobalSettings(company_db, website_id)
        global_setting_date = EngageboostGlobalSettings.objects.using(company_db).get(website_id=website_id,isdeleted='n',isblocked='n')
        global_setting_zone = EngageboostTimezones.objects.using(company_db).get(id = getGlobalSettings['timezone_id'])
        order_id = ''
        final_payment_response = {}
        try:
            if request.data['invoice_create_request'] == 'y':

                order_ids = request.data["selectedIds"]
                order_idsArr = order_ids.split(",")
                shipment_orders = EngageboostShipmentOrders.objects.using(company_db).filter(shipment=shipment_id, order__in=order_idsArr).all()
                shipment_orders_serializer = ShipmentsOrdersSerializer(shipment_orders, many=True)

                if shipment_orders.count() > 0:
                    shipment_orders_first = shipment_orders.first()
                    order_id = shipment_orders_first.order_id

                    rs_order_master = EngageboostOrdermaster.objects.filter(id=order_id).first()
                    # if rs_order_master and rs_order_master.payment_type_id == 2 and rs_order_master.payment_method_id == 53:
                    if rs_order_master and rs_order_master.payment_type_id == 2 and rs_order_master.payment_method_id == 51:
                        # if rs_order_master.pay_txntranid is None or rs_order_master.pay_txntranid == '':
                        if rs_order_master.paid_amount <= 0:
                            payment_response = payment_request_si_charge_si(order_id)
                            print('payment_response============', payment_response)
                            if payment_response['status'] == 'failed':
                                final_payment_response = {'status': payment_response['status'],
                                'msg': "Please try after sometime",
                                'msg_1': payment_response['msg'],
                                'si_ref_no': payment_response['si_ref_no'],
                                'pay_txntranid': payment_response['pay_txntranid']}
                            else:
                                final_payment_response = {'status': payment_response['status'],
                                'msg': payment_response['msg'],
                                'msg_1': payment_response['msg']}
                        else:
                            final_payment_response = {'status': 'error', 'msg': "Payment Already Done"}

                        if final_payment_response['status'] == 'success':

                            # order wise invoice generate start here......
                            for shipmentOrder in shipment_orders_serializer.data:
                                order_id = shipmentOrder["order"]["id"]
                                order_id = int(order_id)
                                warehouse_id = shipmentOrder["warehouse_id"]
                                # if shipmentOrder["shipment_status"] == 'Picking' or shipmentOrder["shipment_status"] == 'Invoicing':
                                if shipmentOrder["shipment_status"] == 'Picking':
                                    error = "Payment is not done by customer."
                                    data = {"status":0,"api_status":0,"error_line":'',"error_message":str(error),"message": str(error)}
                                    return Response(data)
                                # Invoice Creation start here
                                # print(shipment_orders_serializer.data['order'])
                                # print('******************')
                                custom_order_id = shipmentOrder["custom_order_id"]
                                trent_picklist_id = shipmentOrder["trent_picklist_id"]
                                customer_id =  shipmentOrder['order']['customer']['id']
                                shipping_cost = shipmentOrder['order']['shipping_cost']
                                pay_wallet_amount = shipmentOrder['order']['pay_wallet_amount']
                                webshop_id = shipmentOrder['order']['webshop_id']
                                paid_amount = shipmentOrder['order']['paid_amount']
                                shipping_method_id = shipmentOrder['order']['shipping_method_id']
                                cart_discount = shipmentOrder['order']["cart_discount"]
                                net_amount  = 0
                                excise_duty = 0
                                total_tax = 0
                                gross_amount = 0
                                invoice_id = 0
                                isInvoiceCreated = EngageboostInvoicemaster.objects.using(company_db).filter(shipment_id=shipment_id,order_id=order_id).first()
                                if isInvoiceCreated is None:
                                    invoice_id_format = getGlobalSettings["invoice_id_format"]
                                    hasInvoice = EngageboostInvoicemaster.objects.last()
                                    if hasInvoice:
                                        lastInvoiceDetails = EngageboostInvoicemaster.objects.order_by('-id').latest('id')
                                        if lastInvoiceDetails.id:
                                            last_invoice_id = int(lastInvoiceDetails.id)+1
                                            custom_invoice_id = invoice_id_format+""+str(last_invoice_id)
                                        else:
                                            custom_invoice_id = invoice_id_format+""+str(1)
                                    else:
                                        custom_invoice_id = invoice_id_format+""+str(1)

                                    invoiceMaster = EngageboostInvoicemaster.objects.using(company_db).create(website_id=website_id,order_id=order_id,shipment_id=shipment_id,custom_order_id=custom_order_id,customer_id=customer_id,webshop_id=webshop_id,shipping_method_id=shipping_method_id,excise_duty=excise_duty,gross_amount=gross_amount,net_amount=net_amount,paid_amount=paid_amount,trent_picklist_id=trent_picklist_id,created=now_utc,custom_invoice_id=custom_invoice_id,warehouse_id=warehouse_id)
                                    invoice_id = invoiceMaster.id

                                invoice_id = int(invoice_id)
                                if invoice_id>0:
                                    for shipmentOrderProduct in  shipmentOrder["shipment_order_products"]:
                                        #print(shipmentOrderProduct)
                                        product_id = shipmentOrderProduct["product"]["id"]
                                        quantity = shipmentOrderProduct["quantity"]

                                        price = shipmentOrderProduct["order_product"]["product_price"]
                                        product_tax_price = shipmentOrderProduct["order_product"]["product_tax_price"]
                                        product_excise_duty = shipmentOrderProduct["order_product"]["product_excise_duty"]

                                        quantity = shipmentOrderProduct["grn_quantity"]
                                        amount = price*quantity
                                        net_amount = float(net_amount) + float(amount)
                                        if product_tax_price:
                                            total_tax = float(total_tax) + float(quantity)*float(product_tax_price)
                                        if product_excise_duty:
                                            excise_duty = float(excise_duty) + float(quantity)*float(product_excise_duty)

                                        gross_amount = net_amount+excise_duty+total_tax+shipping_cost-float(cart_discount)
                                        # Wallet balance update start...
                                        if gross_amount>pay_wallet_amount:
                                            gross_amount = float(gross_amount-pay_wallet_amount)
                                        else:
                                            refund_wallet= float(pay_wallet_amount-gross_amount)
                                            # common.addCustomerLoyaltypoints()
                                            pay_wallet_amount = gross_amount
                                        # Wallet balance update end..
                                        exist_inv = EngageboostInvoiceProducts.objects.using(company_db).filter(order_id=order_id,invoice_id=invoice_id,product_id=product_id).count()
                                        if exist_inv==0:
                                            invoiceProduct = EngageboostInvoiceProducts.objects.using(company_db).create(order_id=order_id,invoice_id=invoice_id,product_id=product_id,quantity=quantity,price=price)
                                        EngageboostShipmentOrderProducts.objects.using(company_db).filter(order_id=order_id,product_id=product_id,shipment=shipment_id,shipment_status__in=['Invoicing','Packed']).update(shipment_status='Shipment Processing')

                                    EngageboostInvoicemaster.objects.filter(id=invoice_id).update(net_amount=net_amount,excise_duty=excise_duty,gross_amount=gross_amount)
                                    EngageboostShipmentOrders.objects.using(company_db).filter(order_id=order_id,shipment=shipment_id,shipment_status__in=['Invoicing','Packed']).update(shipment_status='Shipment Processing')

                                    AllshipmentOrder = EngageboostShipmentOrders.objects.filter(shipment=shipment_id, shipment_status__in=['Picking','Packed','Invoicing']).all()
                                    if len(AllshipmentOrder)>0:
                                        pass
                                    else:
                                        EngageboostShipments.objects.filter(id=shipment_id,shipment_status__in=['Invoicing','Packed']).update(shipment_status='Shipment Processing')
                                        EngageboostTrentPicklists.objects.filter(id=trent_picklist_id,picklist_status__in=['Invoicing','Packed']).update(picklist_status='Shipment Processing')

                                    if request.data["invoice_email"] == 'y':
                                        pass ### send email functiolity goes here.
                                    # order activity set
                                    activityType = 1
                                    activity_details = common.save_order_activity(company_db,order_id,now_utc,7,"Order is Shipment Processing",userId,activityType)
                                    elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'shipping_status':'Shipment Processing'})
                                    # Invoice Creation end here
                                # order wise invoice generate end here......
                                # Making delivery planner start here...
                                if order_idsArr and len(order_idsArr) > 0:
                                    totalVechicle = create_automatic_delivery_plan(order_idsArr, shipment_id, warehouse_id)
                                    EngageboostShipments.objects.filter(id=shipment_id).update(no_of_vehicles=totalVechicle)
                                # Making delivery planner end here...

                            # common.email_send_by_AutoResponder(order_id, 29)
                            common.sms_send_by_AutoResponder(order_id, '', 29, '')
                    else:
                        # order wise invoice generate start here......
                        for shipmentOrder in shipment_orders_serializer.data:
                            order_id = shipmentOrder["order"]["id"]
                            order_id = int(order_id)
                            warehouse_id = shipmentOrder["warehouse_id"]
                            # if shipmentOrder["shipment_status"] == 'Picking' or shipmentOrder["shipment_status"] == 'Invoicing':
                            if shipmentOrder["shipment_status"] == 'Picking':
                                error = "Payment is not done by customer."
                                data = {"status": 0, "api_status": 0, "error_line": '', "error_message": str(error),
                                        "message": str(error)}
                                return Response(data)
                            # Invoice Creation start here
                            # print(shipment_orders_serializer.data['order'])
                            # print('******************')
                            custom_order_id = shipmentOrder["custom_order_id"]
                            trent_picklist_id = shipmentOrder["trent_picklist_id"]
                            customer_id = shipmentOrder['order']['customer']['id']
                            shipping_cost = shipmentOrder['order']['shipping_cost']
                            pay_wallet_amount = shipmentOrder['order']['pay_wallet_amount']
                            webshop_id = shipmentOrder['order']['webshop_id']
                            paid_amount = shipmentOrder['order']['paid_amount']
                            shipping_method_id = shipmentOrder['order']['shipping_method_id']
                            cart_discount = shipmentOrder['order']["cart_discount"]
                            net_amount = 0
                            excise_duty = 0
                            total_tax = 0
                            gross_amount = 0
                            invoice_id = 0
                            isInvoiceCreated = EngageboostInvoicemaster.objects.using(company_db).filter(
                                shipment_id=shipment_id, order_id=order_id).first()
                            if isInvoiceCreated is None:
                                invoice_id_format = getGlobalSettings["invoice_id_format"]
                                hasInvoice = EngageboostInvoicemaster.objects.last()
                                if hasInvoice:
                                    lastInvoiceDetails = EngageboostInvoicemaster.objects.order_by('-id').latest('id')
                                    if lastInvoiceDetails.id:
                                        last_invoice_id = int(lastInvoiceDetails.id) + 1
                                        custom_invoice_id = invoice_id_format + "" + str(last_invoice_id)
                                    else:
                                        custom_invoice_id = invoice_id_format + "" + str(1)
                                else:
                                    custom_invoice_id = invoice_id_format + "" + str(1)

                                invoiceMaster = EngageboostInvoicemaster.objects.using(company_db).create(
                                    website_id=website_id, order_id=order_id, shipment_id=shipment_id,
                                    custom_order_id=custom_order_id, customer_id=customer_id, webshop_id=webshop_id,
                                    shipping_method_id=shipping_method_id, excise_duty=excise_duty,
                                    gross_amount=gross_amount, net_amount=net_amount, paid_amount=paid_amount,
                                    trent_picklist_id=trent_picklist_id, created=now_utc,
                                    custom_invoice_id=custom_invoice_id, warehouse_id=warehouse_id)
                                invoice_id = invoiceMaster.id

                            invoice_id = int(invoice_id)
                            if invoice_id > 0:
                                for shipmentOrderProduct in shipmentOrder["shipment_order_products"]:
                                    # print(shipmentOrderProduct)
                                    product_id = shipmentOrderProduct["product"]["id"]
                                    quantity = shipmentOrderProduct["quantity"]

                                    price = shipmentOrderProduct["order_product"]["product_price"]
                                    product_tax_price = shipmentOrderProduct["order_product"]["product_tax_price"]
                                    product_excise_duty = shipmentOrderProduct["order_product"]["product_excise_duty"]

                                    quantity = shipmentOrderProduct["grn_quantity"]
                                    amount = price * quantity
                                    net_amount = float(net_amount) + float(amount)
                                    if product_tax_price:
                                        total_tax = float(total_tax) + float(quantity) * float(product_tax_price)
                                    if product_excise_duty:
                                        excise_duty = float(excise_duty) + float(quantity) * float(product_excise_duty)

                                    gross_amount = net_amount + excise_duty + total_tax + shipping_cost - float(
                                        cart_discount)
                                    # Wallet balance update start...
                                    if gross_amount > pay_wallet_amount:
                                        gross_amount = float(gross_amount - pay_wallet_amount)
                                    else:
                                        refund_wallet = float(pay_wallet_amount - gross_amount)
                                        # common.addCustomerLoyaltypoints()
                                        pay_wallet_amount = gross_amount
                                    # Wallet balance update end..
                                    exist_inv = EngageboostInvoiceProducts.objects.using(company_db).filter(
                                        order_id=order_id, invoice_id=invoice_id, product_id=product_id).count()
                                    if exist_inv == 0:
                                        invoiceProduct = EngageboostInvoiceProducts.objects.using(company_db).create(
                                            order_id=order_id, invoice_id=invoice_id, product_id=product_id,
                                            quantity=quantity, price=price)
                                    EngageboostShipmentOrderProducts.objects.using(company_db).filter(order_id=order_id,
                                                                                                      product_id=product_id,
                                                                                                      shipment=shipment_id,
                                                                                                      shipment_status__in=[
                                                                                                          'Invoicing',
                                                                                                          'Packed']).update(
                                        shipment_status='Shipment Processing')

                                EngageboostInvoicemaster.objects.filter(id=invoice_id).update(net_amount=net_amount,
                                                                                              excise_duty=excise_duty,
                                                                                              gross_amount=gross_amount)
                                EngageboostShipmentOrders.objects.using(company_db).filter(order_id=order_id,
                                                                                           shipment=shipment_id,
                                                                                           shipment_status__in=[
                                                                                               'Invoicing',
                                                                                               'Packed']).update(
                                    shipment_status='Shipment Processing')

                                AllshipmentOrder = EngageboostShipmentOrders.objects.filter(shipment=shipment_id,
                                                                                            shipment_status__in=[
                                                                                                'Picking', 'Packed',
                                                                                                'Invoicing']).all()
                                if len(AllshipmentOrder) > 0:
                                    pass
                                else:
                                    EngageboostShipments.objects.filter(id=shipment_id,
                                                                        shipment_status__in=['Invoicing',
                                                                                             'Packed']).update(
                                        shipment_status='Shipment Processing')
                                    EngageboostTrentPicklists.objects.filter(id=trent_picklist_id,
                                                                             picklist_status__in=['Invoicing',
                                                                                                  'Packed']).update(
                                        picklist_status='Shipment Processing')

                                if request.data["invoice_email"] == 'y':
                                    pass  ### send email functiolity goes here.
                                # order activity set
                                activityType = 1
                                activity_details = common.save_order_activity(company_db, order_id, now_utc, 7,
                                                                              "Order is Shipment Processing", userId,
                                                                              activityType)
                                elastic = common.change_field_value_elastic(order_id, 'EngageboostOrdermaster',
                                                                            {'shipping_status': 'Shipment Processing'})
                                # Invoice Creation end here
                            # order wise invoice generate end here......
                            # Making delivery planner start here...
                            if order_idsArr and len(order_idsArr) > 0:
                                totalVechicle = create_automatic_delivery_plan(order_idsArr, shipment_id, warehouse_id)
                                EngageboostShipments.objects.filter(id=shipment_id).update(no_of_vehicles=totalVechicle)
                            # Making delivery planner end here...

                        # common.email_send_by_AutoResponder(order_id, 29)
                        # common.sms_send_by_AutoResponder(order_id, '', 29, '')

                        final_payment_response = {'status': 'success', 'msg': "Offline payment"}
            # display invoice order listing....
            shipment_status = ['Picking']
            shipment_order = EngageboostShipmentOrders.objects.using(company_db).filter(shipment=shipment_id).exclude(shipment_status__in=shipment_status).all()
            # shipment_orders_serializer = ShipmentsOrdersSerializer(shipment_order,many=True)
            shipment_orders_serializer = ShipmentsOrdersViewSerializer(shipment_order,many=True)
            count_invoice = 0
            picklist_id = 0
            # print('ShipmentsOrdersSerializer===========', json.dumps(shipment_orders_serializer.data))
            for shipmentOrder in shipment_orders_serializer.data:
                order_id = shipmentOrder["order"]["id"]
                picklist_id = shipmentOrder["trent_picklist_id"]
                shipmentOrder["order_details"] = shipmentOrder["order"]
                # start Date time format setting...
                shipmentOrder['order_details']['created'] = common.get_time(shipmentOrder["order"]["created"],global_setting_zone, global_setting_date)
                shipmentOrder['order_details']['time_slot_date'] = common.get_date_from_datetime(shipmentOrder["order"]["time_slot_date"],global_setting_zone, global_setting_date,'%Y-%m-%d')
                # end Date time format setting...
                # if shipmentOrder['shipment_order_products']:
                # 	for shipmentOrderProduct in shipmentOrder['shipment_order_products']:
                # 		# orderProductDetails = EngageboostOrderProducts.objects.using(company_db).filter(order_id=shipmentOrderProduct['order']['id'],product_id=shipmentOrderProduct['product']['id']).first()
                # 		# orderProductDetails_serializer = OrderProductsSerializer(orderProductDetails)
                # 		# shipmentOrderProduct['order_product_details']=orderProductDetails_serializer.data
                # 		# warehouseDetails = EngageboostWarehouseMasters.objects.using(company_db).filter(id=shipmentOrderProduct['warehouse_id']).all()
                # 		warehouseDetails = EngageboostWarehouseMasters.objects.using(company_db).filter(id=shipmentOrder['warehouse_id']).first()
                # 		shipmentOrderProduct['warehouse_name'] = warehouseDetails.name

                invoiceDetails = EngageboostInvoicemaster.objects.using(company_db).filter(shipment_id=shipment_id,order_id=order_id).first()
                if invoiceDetails is not None:
                    shipmentOrder['created_date'] = common.get_date_from_datetime(invoiceDetails.created,global_setting_zone, global_setting_date,'%Y-%m-%d')
                    shipmentOrder["custom_invoice_id"] = invoiceDetails.custom_invoice_id
                    count_invoice = int(count_invoice)+1
                shipmentOrder["count_invoice"] = count_invoice
                driverName = ''
                vehicle_no = ''
                if shipmentOrder["order"]["shipment_id"]:
                    shipment_id = shipmentOrder["order"]["shipment_id"]
                    driverVehicleMap = EngageboostDriverVeichleMap.objects.filter(shipment_id=shipment_id).first()
                    if driverVehicleMap:
                        driver_id = driverVehicleMap.user_id
                        vehicle_id = driverVehicleMap.vehicle_id
                        if driver_id > 0:
                            driverManagerdata = EngageboostDeliveryManagers.objects.filter(user_id=driver_id).first()
                            driverName = driverManagerdata.name
                        if vehicle_id > 0 :
                            vehicleData = EngageboostVehicleMasters.objects.filter(id=vehicle_id).first()
                            vehicle_no = vehicleData.vehicle_number

                    deliveryPlanOrder = EngageboostDeliveryPlanOrder.objects.filter(order_id=order_id,shipment_id=shipment_id).first()
                    if deliveryPlanOrder:
                        distance = deliveryPlanOrder.distance;
                        virtual_vehicle_id = deliveryPlanOrder.virtual_vechile_id;
                        if distance>1000:
                            distance = str( float("{0:.2f}".format(distance/1000))) + ' Km'
                        else:
                            distance = str( float("{0:.2f}".format(distance))) + ' mtr'

                        time = deliveryPlanOrder.time;
                        if time>3600:
                            time = str( float("{0:.2f}".format(time/3600))) + ' Hr'
                        else:
                            time = str( float("{0:.2f}".format(time/60))) + ' Min'
                shipmentOrder['order_details']['DriverName'] = driverName
                shipmentOrder['order_details']['vehicle_no'] = vehicle_no
            # final_payment_response = {}
            if count_invoice > 0:
                is_invoice_created = 'Y'
                # rs_order_master = EngageboostOrdermaster.objects.filter(id=order_id).first()
                # # if rs_order_master and rs_order_master.payment_type_id == 2 and rs_order_master.payment_method_id == 53:
                # if rs_order_master and rs_order_master.payment_type_id == 2 and rs_order_master.payment_method_id == 51:
                # 	if rs_order_master.pay_txntranid is None or rs_order_master.pay_txntranid == '':
                # 		final_payment_response = payment_request_si_charge(order_id)
                # 	else:
                # 		final_payment_response = {'status': 'error', 'msg': "duplicate_invoice_created"}
            else:
                is_invoice_created = 'N'
                # final_payment_response = {'status': 'error', 'msg': "no_invoice_created"}
            data={"status":1,"api_status":'1', "InvoiceDetails":shipment_orders_serializer.data,'picklist_id':picklist_id,'shipment_id':shipment_id,"message": "Getting the Invoice Informations","is_invoice_created":is_invoice_created, "payment_response": final_payment_response}
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

class CreatePicklist(generics.ListAPIView):
    # """ Generate picklist """
    def post(self, request, format=None):
        company_db  = loginview.db_active_connection(request)
        now_utc     = datetime.now(timezone.utc).astimezone()
        website_id  = request.data["website_id"]
        company_id  = request.data["company_id"]
        picklist_id = request.data["picklist_id"]
        userId      = request.data["userId"]
        try:
            is_existing_picklist = EngageboostTrentPicklists.objects.using(company_db).filter(id=picklist_id,isdeleted='n',isblocked='n').first()
            if is_existing_picklist and is_existing_picklist.picklist_status == 'Created':
                EngageboostTrentPicklists.objects.using(company_db).filter(id=is_existing_picklist.id).update(modified=now_utc, picklist_status='Picking')
                EngageboostShipmentOrders.objects.using(company_db).filter(trent_picklist_id=is_existing_picklist.id).update(shipment_status='Picking')

                EngageboostShipmentOrderProducts.objects.using(company_db).filter(trent_picklist_id=is_existing_picklist.id).update(shipment_status='Picking')

                ext_order = EngageboostOrdermaster.objects.filter(trent_picklist_id=is_existing_picklist.id).first()
                elastic = common.change_field_value_elastic(ext_order.id,'EngageboostOrdermaster',{'shipping_status':'Picking'})

                shipment_orders = EngageboostShipmentOrders.objects.using(company_db).filter(trent_picklist_id=picklist_id,shipment_status='Picking').all()
                shipment_orders_serializer = ShipmentsOrdersSerializer(shipment_orders,many=True)
                for shipmentOrder in shipment_orders_serializer.data:
                    activityType = 1
                    activity_details = common.save_order_activity(company_db,shipmentOrder['order_id'],now_utc,7,"Order is Picking",userId,activityType)
            elif is_existing_picklist :
                picklist_id = is_existing_picklist.id
            data={"status":1,"api_status":'1', "picklist_id" : picklist_id, "message": "Picklist has been created successfully"}
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

class InvoicePrint(generics.ListAPIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        now_utc = datetime.now(timezone.utc).astimezone()
        try:
            website_id=request.data["website_id"]
            global_setting_date = EngageboostGlobalSettings.objects.using(company_db).get(website_id=website_id,isdeleted='n',isblocked='n')
            global_setting_zone = EngageboostTimezones.objects.using(company_db).get(id = global_setting_date.timezone_id)
            order_ids = request.data["selectedIds"]
            trent_picklist_id = request.data["trent_picklist_id"]
            orderIdsArr = order_ids.split(",")
            # for order_id in orderIdsArr:
            invoice_cotent = ''
            invoice_master = EngageboostInvoicemaster.objects.using(company_db).filter(trent_picklist_id=trent_picklist_id,order_id__in=orderIdsArr).all()
            invoice_serializer = InvoicemasterSerializer(invoice_master,many=True)
            # print(invoice_master.data)
            if invoice_master:
                for invoiceDetails in invoice_serializer.data:
                    order_id = invoiceDetails["order"]["id"]
                    shipment_orders = EngageboostShipmentOrders.objects.using(company_db).filter(trent_picklist_id=trent_picklist_id,order_id=order_id).first()
                    buffer_data = common.getAutoResponder(company_db,"Shipment Processing",invoiceDetails["webshop_id"], shipment_orders.warehouse_id, shipment_orders.shipping_method_id,website_id,7)
                    autoResponderData  = buffer_data["content"]
                    #print(autoResponderData)
                    if autoResponderData["email_type"] == 'T':
                        emailContent = autoResponderData["email_content_text"]
                    else:
                        emailContent = autoResponderData["email_content"]
                    emailContent = str(emailContent)
                    invoice_buffer = generateInvoiceFormat(company_db,invoiceDetails["id"],"No",invoiceDetails,emailContent,website_id)
                    orderData = invoice_buffer["content"]
                    orderData["order"]["no_of_crates"] = shipment_orders.no_of_crates
                    # cds working
                    crate_arr = EngageboostCrates.objects.filter(trent_picklist_id=trent_picklist_id, order_id=order_id, isdeleted='n', isblocked='n').all()
                    crates_name_arr = []
                    for crate_arr_data in crate_arr:
                        crates_name_arr.append(crate_arr_data.crate_barcode)
                    # sprint(crates_name_arr)
                    orderData["order"]["crates_name"] = ", ".join(crates_name_arr)
                    # print(orderData["order"])

                    # start Date time format setting...
                    orderData['order']['order_date'] = common.get_time(orderData["order"]["order_date"],global_setting_zone, global_setting_date)
                    orderData['order']['time_slot_date'] = common.get_date_from_datetime(orderData["order"]["time_slot_date"],global_setting_zone, global_setting_date,'%Y-%m-%d')
                    orderData['order']['invoice_date'] = common.get_date_from_datetime(orderData["order"]["invoice_date"],global_setting_zone, global_setting_date,'%Y-%m-%d')
                    # end Date time format setting...

                    for orderKey in orderData["order"]:
                        replacingKey = '{@'+str(orderKey)+'}'
                        #print(orderData["order"][orderKey])
                        emailContent = emailContent.replace(str(replacingKey),str(orderData["order"][orderKey] if orderData["order"][orderKey]!= '' else ''))
                    invoice_cotent+=emailContent
                data={"status":1,"api_status":1, "message": "Printing invoice details","invoice_content":invoice_cotent}
            else:
                data={"status":0,"api_status":0, "message": "invoice is not created.","invoice_content":invoice_cotent}

        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

def generateInvoiceFormat(company_db,invoiceId,forMail,invoiceDetails,buffer,website_id):
    invoice_master = EngageboostInvoicemaster.objects.using(company_db).filter(id=invoiceId).first()
    invoice_serializer = InvoicemasterSerializer(invoice_master)
    invoice_serializer.data["order"]["custom_invoice_id"]=invoice_serializer.data["custom_invoice_id"]
    if invoice_serializer.data["order"]["customer"]["last_name"]:
        invoice_serializer.data["order"]["customer_name"]=invoice_serializer.data["order"]["customer"]["first_name"]+" "+invoice_serializer.data["order"]["customer"]["last_name"]
    else:
        invoice_serializer.data["order"]["customer_name"]=invoice_serializer.data["order"]["customer"]["first_name"]
    if invoice_serializer.data["order"]["customer"]["vat"]:
        invoice_serializer.data["order"]["vat"]=invoice_serializer.data["order"]["customer"]["vat"]
    if invoice_serializer.data['webshop_id'] == 6:
        invoice_serializer.data["order"]["channel_order_id"]=invoice_serializer.data["order"]["custom_order_id"]

    channelDetails = common.getChannelInfo(company_db,invoice_serializer.data["webshop_id"])
    invoice_serializer.data["order"]["channel_name"] = (channelDetails["api_status"]["name"])
    invoice_serializer.data["order"]["market_place_type"] = (channelDetails["api_status"]["name"])

    invoice_serializer.data["order"]["store_country"] = ''
    warehouseDetails = EngageboostWarehouseMasters.objects.using(company_db).filter(id=invoice_serializer.data["order"]["assign_wh"]).first()
    if warehouseDetails:
        invoice_serializer.data["order"]["store_name"] = warehouseDetails.name
        invoice_serializer.data["order"]["store_code"] = warehouseDetails.code
        invoice_serializer.data["order"]["store_address"] = warehouseDetails.address
        invoice_serializer.data["order"]["store_contact_person"] = warehouseDetails.contact_person
        invoice_serializer.data["order"]["store_email"] = warehouseDetails.email
        invoice_serializer.data["order"]["store_phone"] = warehouseDetails.phone
        invoice_serializer.data["order"]["store_city"] = warehouseDetails.city
        invoice_serializer.data["order"]["store_zipcode"] = warehouseDetails.zipcode
        invoice_serializer.data["order"]["store_state"] = warehouseDetails.state_name
        invoice_serializer.data["order"]["store_logo"] = warehouseDetails.warehouse_logo
        if warehouseDetails.country_id:
            countries = EngageboostCountries.objects.using(company_db).filter(id=warehouseDetails.country_id).first()
            invoice_serializer.data["order"]["store_country"] = countries.country_name

    tax_amount = 0
    grand_total = 0
    product_discount = 0
    for InvoiceProduct in invoice_serializer.data["invoice_order_products"]:
        order_id = InvoiceProduct["order_id"]
        product_id = InvoiceProduct["product_id"]
        order_product_info = EngageboostOrderProducts.objects.using(company_db).filter(product_id=product_id,order_id=order_id).first()
        InvoiceProduct["product_discount_price"] = order_product_info.product_discount_price
        InvoiceProduct["product_tax_price"] = order_product_info.product_tax_price
        InvoiceProduct["shipping_price"] = order_product_info.shipping_price
        InvoiceProduct["product_price"] = order_product_info.product_price
        tax_amount = tax_amount+float(order_product_info.product_tax_price)*float(InvoiceProduct["quantity"])
        product_discount = product_discount+float(order_product_info.product_discount_price)*float(InvoiceProduct["quantity"])

    order_amount = invoice_serializer.data["order"]["order_amount"]
    gross_amount = invoice_serializer.data["order"]["gross_amount"]
    odrernet_amount = invoice_serializer.data["order"]["net_amount"]
    net_amount = invoice_serializer.data["net_amount"]
    cod_charge = invoice_serializer.data["order"]["cod_charge"]
    paid_amount = invoice_serializer.data["order"]["paid_amount"]
    shipping_cost = invoice_serializer.data["order"]["shipping_cost"]
    cart_discount = invoice_serializer.data["order"]["cart_discount"]
    pay_wallet_amount = invoice_serializer.data["order"]["pay_wallet_amount"]

    total_saving = float(cart_discount)+product_discount
    invoice_serializer.data["order"]["total_saving"] = formatNumber(total_saving)
    grand_total = (float(net_amount)+float(cod_charge)+float(shipping_cost)+float(tax_amount))-float(cart_discount)-float(pay_wallet_amount)
    if order_amount:
        grand_total = gross_amount
        net_amount = odrernet_amount
    balance_due = grand_total-float(paid_amount)
    invoice_serializer.data["order"]["grand_total"] = formatNumber(grand_total)
    invoice_serializer.data["order"]["cart_discount"] = formatNumber(cart_discount) if cart_discount else '0.00'
    invoice_serializer.data["order"]["pay_wallet_amount"] = formatNumber(pay_wallet_amount) if pay_wallet_amount else '0.00'
    invoice_serializer.data["order"]["shipping_cost"] = formatNumber(shipping_cost) if shipping_cost else '0.00'
    invoice_serializer.data["order"]["balance_due"] = formatNumber(balance_due) if balance_due else '0.00'
    invoice_serializer.data["order"]["paid_amount"] = formatNumber(invoice_serializer.data["order"]["paid_amount"]) if invoice_serializer.data["order"]["paid_amount"] else '0.00'

    productBoxInfo = createProductBoxInvoice(company_db,invoice_serializer.data["order"],invoice_serializer.data["invoice_order_products"])
    invoice_serializer.data["order"]["PRODUCT_BOX"] = productBoxInfo["PRODUCT_BOX"]
    invoice_serializer.data["order"]["invoice_date"] = invoice_serializer.data["created"]
    invoice_serializer.data["order"]["order_date"] = invoice_serializer.data["order"]["created"]
    invoice_serializer.data["order"]["first_name"] = invoice_serializer.data["order"]["customer"]["first_name"]
    invoice_serializer.data["order"]["last_name"] = invoice_serializer.data["order"]["customer"]["last_name"]
    invoice_serializer.data["order"]["total_qty"] = productBoxInfo["total_qty"]
    invoice_serializer.data["order"]["total_weight"] = productBoxInfo["total_weight"]
    invoice_serializer.data["order"]["tax_amount"] = formatNumber(tax_amount) if tax_amount else '0.00'
    invoice_serializer.data["order"]["tax"] = formatNumber(tax_amount) if tax_amount else '0.00'
    invoice_serializer.data["order"]["sub_total"] = formatNumber(net_amount) if net_amount else '0.00'
    amount_in_word = num2words(float(grand_total))
    amount_in_word = amount_in_word.replace('-','').replace(',','')
    invoice_serializer.data["order"]["grand_total_words"] = amount_in_word.title()+" Only."
    data ={"status":1, "content":invoice_serializer.data,"message": 'Getting invoice information from auto responder'}
    return data

def createProductBoxInvoice(company_db,orderData,InvoiceProduct):
    total_str = ""
    table_str = '<table width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td align="left" style="background-color:#e1e1e1; padding:5px; padding-left:10px; border-top:1px solid #414141;font-size:10pt; border-right:1px solid #414141; border-bottom:1px solid #414141;" valign="top"><strong>S.No</strong></td><td align="left" style="background-color:#e1e1e1; padding:5px; padding-left:10px; border-top:1px solid #414141;font-size:10pt; border-right:1px solid #414141; border-bottom:1px solid #414141;" valign="top"><strong>ITEM DESCRIPTION</strong></td><td align="center" style="background-color:#e1e1e1; padding:5px; border-top:1px solid #414141;font-size:10pt; border-right:1px solid #414141; border-bottom:1px solid #414141;" valign="top"><strong>QTY</strong></td><td align="center" style="background-color:#e1e1e1; padding:5px; border-top:1px solid #414141;font-size:10pt; border-right:1px solid #414141; border-bottom:1px solid #414141;width:17%;" valign="top"><strong>UNIT PRICE</strong></td><td align="left" style="background-color:#e1e1e1; padding:5px; padding-left:10px; border-top:1px solid #414141;font-size:10pt; border-right:1px solid #414141; border-bottom:1px solid #414141;" valign="top"><strong>Tax Price</strong></td><td align="center" style="background-color:#e1e1e1; padding:5px; border-top:1px solid #414141;font-size:10pt; border-bottom:1px solid #414141;width:17%;" valign="top"><strong>AMOUNT</strong></td></tr>'
    total_str=total_str+""+table_str
    total_weight = 0
    count = 1
    total_qty = 0
    for InvoiceItem in InvoiceProduct:
        product_id = InvoiceItem["product_id"]
        productDetails = EngageboostProducts.objects.using(company_db).filter(id=product_id).first()
        rs_uom = EngageboostUnitMasters.objects.filter(id=productDetails.uom).first()
        uom_name = ""
        if rs_uom:
            uom_name = rs_uom.unit_name
        if productDetails.weight:
            product_weight = productDetails.weight*InvoiceItem["quantity"]
            total_weight = total_weight+float(productDetails.weight)
        else:
            productDetails.weight = ""
        total_qty=total_qty+int(InvoiceItem["quantity"])
        itemGrossPrice = float(InvoiceItem["product_price"]*InvoiceItem["quantity"])+float(InvoiceItem["product_tax_price"]*InvoiceItem["quantity"])
        total_str+= '<tr  style="text-transform:none;">'
        total_str+= '<td width="0" align="left" style="font-size:10pt; text-align:center; border-right:1px solid #414141; border-bottom:1px solid #414141; padding:5px; padding-left:10px;" valign="top">'+str(count)+'</td>'
        if productDetails.weight is None or productDetails.weight == "":
            total_str+= '<td width="0" align="left" style="font-size:10pt; text-align:center; border-right:1px solid #414141; border-bottom:1px solid #414141; padding:5px; padding-left:10px;" valign="top">'+productDetails.name+'</td>'
        else:
            total_str+= '<td width="0" align="left" style="font-size:10pt; text-align:center; border-right:1px solid #414141; border-bottom:1px solid #414141; padding:5px; padding-left:10px;" valign="top">'+productDetails.name+ ' ('+ productDetails.weight + ' '+ uom_name +')</td>'
        total_str+= '<td width="0" align="left" style="font-size:10pt; text-align:center; border-right:1px solid #414141; border-bottom:1px solid #414141; padding:5px; padding-left:10px;" valign="top">'+str(InvoiceItem["quantity"])+'</td>'
        total_str+= '<td width="0" align="left" style="font-size:10pt; text-align:center; border-right:1px solid #414141; border-bottom:1px solid #414141; padding:5px; padding-left:10px;" valign="top">'+str(formatNumber(InvoiceItem["product_price"]))+'</td>'
        total_str+= '<td width="0" align="left" style="font-size:10pt; text-align:center; border-right:1px solid #414141; border-bottom:1px solid #414141; padding:5px; padding-left:10px;" valign="top">'+str(formatNumber(InvoiceItem["product_tax_price"]))+'</td>'
        total_str+= '<td width="0" align="left" style="font-size:10pt; text-align:center; border-right:1px solid #414141; border-bottom:1px solid #414141; padding:5px; padding-left:10px;" valign="top">'+str(formatNumber(itemGrossPrice)) +'</td>'
        total_str+="</tr>"
        count=count+1
    total_str+="</table>"
    data ={"status":1, "PRODUCT_BOX":total_str,"total_qty":total_qty,"total_weight":total_weight}
    return data

def formatNumber(number):
    return ("{:,.2f}".format(number))

#_______________Delivery Planner_______________#
class DeliveryPlanner(generics.ListAPIView):
    def post(self,request):
        company_db = loginview.db_active_connection(request)
        postdata = request.data
        all_order_ids_arr = []
        ItemIdsArr = []
        orderDataList = []
        vehicle_no = ''
        driverName = ''
        virtual_vehicle_id = 1
        time = ''
        distance = ''
        try:
            website_id = postdata["website_id"] if postdata.get("website_id") else 1
            # start Date time format setting...
            global_setting_date = EngageboostGlobalSettings.objects.using(company_db).get(website_id=website_id,isdeleted='n',isblocked='n')
            global_setting_zone = EngageboostTimezones.objects.using(company_db).get(id = global_setting_date.timezone_id)
            # end Date time format setting...

            shipment_id = postdata["shipment_id"] if postdata.get("shipment_id") else None
            if shipment_id:
                shipment_order = EngageboostShipmentOrders.objects.using(company_db).filter(shipment=shipment_id).exclude(shipment_status__in=['Invoicing','Picking']).all().order_by('order__sort_by_distance')
                if shipment_order:
                    shipment_orders_serializer = ShipmentsOrdersSerializer(shipment_order,many=True)
                    for shipmentOrder in shipment_orders_serializer.data:
                        order_id = shipmentOrder["order"]["id"]
                        all_order_ids_arr.append(order_id)

                        shipmentOrder["OrderList"] = shipmentOrder["order"]
                        shipmentOrder["sort_by_distance"] = shipmentOrder["order"]["sort_by_distance"]

                        deliveryPlanOrder = EngageboostDeliveryPlanOrder.objects.filter(order_id=order_id,shipment_id=shipment_id).first()
                        if deliveryPlanOrder:
                            distance = deliveryPlanOrder.distance
                            virtual_vehicle_id = deliveryPlanOrder.virtual_vechile_id
                            if distance>1000:
                                distance = str( float("{0:.2f}".format(distance/1000))) + ' Km'
                            else:
                                distance = str( float("{0:.2f}".format(distance))) + ' mtr'

                            time = deliveryPlanOrder.time
                            if time>3600:
                                time = str( float("{0:.2f}".format(time/3600))) + ' Hr'
                            else:
                                time = str( float("{0:.2f}".format(time/60))) + ' Min'

                        driverVehicleMap = EngageboostDriverVeichleMap.objects.filter(shipment_id=shipment_id,virtual_vechile_id=virtual_vehicle_id).first()
                        if driverVehicleMap:
                            driver_id = driverVehicleMap.user_id
                            vehicle_id = driverVehicleMap.vehicle_id
                            if driver_id > 0:
                                driverManagerdata = EngageboostDeliveryManagers.objects.filter(user_id=driver_id,isdeleted='n', isblocked='n').first()
                                driverName = driverManagerdata.name
                            if vehicle_id > 0 :
                                vehicleData = EngageboostVehicleMasters.objects.filter(id=vehicle_id).first()
                                vehicle_no = vehicleData.vehicle_number

                        #DriverName, vehicle_no, time, distance, virtual_vehicle_id
                        shipmentOrder["OrderList"]['DriverName'] = driverName
                        shipmentOrder["OrderList"]['vehicle_no'] = vehicle_no
                        shipmentOrder["OrderList"]['time_required'] = time
                        shipmentOrder["OrderList"]['distance'] = distance
                        shipmentOrder["OrderList"]['virtual_vehicle_id'] = virtual_vehicle_id

                        # start Date time format setting...
                        shipmentOrder['OrderList']['created'] = common.get_time(shipmentOrder["order"]["created"],global_setting_zone, global_setting_date)
                        shipmentOrder['order']['time_slot_date'] = common.get_date_from_datetime(shipmentOrder["order"]["time_slot_date"],global_setting_zone, global_setting_date,'%Y-%m-%d')
                        # end Date time format setting...

                        if shipmentOrder['shipment_order_products']:
                            for shipmentOrderProduct in shipmentOrder['shipment_order_products']:
                                orderProductDetails = EngageboostOrderProducts.objects.using(company_db).filter(order_id=shipmentOrderProduct['order']['id'],product_id=shipmentOrderProduct['product']['id']).first()
                                orderProductDetails_serializer = OrderProductsSerializer(orderProductDetails)
                                shipmentOrderProduct['order_product_details']=orderProductDetails_serializer.data
                                warehouseDetails = EngageboostWarehouseMasters.objects.using(company_db).filter(id=shipmentOrderProduct['warehouse_id']).first()
                                shipmentOrderProduct['warehouse_name'] = warehouseDetails.name
                    data={"status":1,"api_status":shipment_orders_serializer.data,"message":"Order List"}
                else:
                    data={"status":0,"api_status":[],"message":"Payment not completed by customer."}
            else:
                data={"status":0,"api_status":[],"message":"Payment not completed by customer."}

            # For testing purpose...
            #totalVechicle = create_automatic_delivery_plan(all_order_ids_arr, shipment_id);
            #EngageboostShipments.objects.filter(id=shipment_id).update(no_of_vehicles=totalVechicle)

            # data={"status":1,"api_status":shipment_orders_serializer.data,"message":"Order List"}
            return Response(data)
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message":str(error)}
            return Response(data)

#_______________Delivery Planner save Sort By distance Manual_______________#
class saveSortBydistance(generics.ListAPIView):
    def post(self,request):
        company_db = loginview.db_active_connection(request)
        requestdata = request.data
        order_data  = requestdata['order_data']
        try:
            if len(order_data)>0:
                for order_data in order_data:
                    order_id = order_data['order_id']
                    shipment_id = order_data['shipment_id']
                    sort_by_distance = order_data['sort_by_distance']
                    website_id = order_data['website_id']
                    if order_id > 0 and shipment_id > 0:
                        EngageboostOrdermaster.objects.filter(id=order_id, shipment_id=shipment_id).update(sort_by_distance=sort_by_distance)
                        EngageboostDeliveryPlanOrder.objects.filter(id=order_id, shipment_id=shipment_id).update(orders=sort_by_distance)

            data={"status":1,"api_status":shipment_id,"message":"Order List"}
            return Response(data)
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message":str(error)}

        return Response(data)

#_______________Assign Vehicle_______________#
class AssignVehicle(generics.ListAPIView):
    def post(self,request):
        company_db = loginview.db_active_connection(request)
        postdata = request.data
        all_order_ids_arr = []
        orderDataList = {}
        extdriverObj = {}
        driverVehicleArr = []
        no_of_vehicles = 1
        available_driver = []
        available_vehicle = []
        try:
            website_id = postdata["website_id"] if postdata.get("website_id") else 1
            warehouse_id = postdata["warehouse_id"] if postdata.get("warehouse_id") else None
            shipment_id = postdata["shipment_id"] if postdata.get("shipment_id") else None
            if shipment_id:
                order_data = EngageboostShipmentOrders.objects.using(company_db).filter(shipment=shipment_id).first()
                if order_data:
                    orderData = ShipmentsOrdersSerializer(order_data)
                    orderData = orderData.data
                    # print(json.dumps(orderData))
                    time_slot_date = orderData["order"]["time_slot_date"]
                    zone_id = orderData["zone_id"]
                # Exist vehicle map checking

                # no_of_vehicles from shipment table
                shipment_data = EngageboostShipments.objects.using(company_db).filter(id=shipment_id, no_of_vehicles__gt=0).first()
                if shipment_data:
                    no_of_vehicles = int(shipment_data.no_of_vehicles)
                    exist_driver_map_all = EngageboostDriverVeichleMap.objects.filter(shipment_id=shipment_id).all()
                    if exist_driver_map_all.count() == no_of_vehicles:
                        for exist_driver_map in exist_driver_map_all:
                            extdriverObj = {
                                "user_id": exist_driver_map.user_id,
                                "vehicle_id" : exist_driver_map.vehicle_id
                            }
                            driverVehicleArr.append(extdriverObj)
                    elif exist_driver_map_all.count() < no_of_vehicles:
                        for exist_driver_map in exist_driver_map_all:
                            extdriverObj = {
                                "user_id": exist_driver_map.user_id,
                                "vehicle_id" : exist_driver_map.vehicle_id
                            }
                            driverVehicleArr.append(extdriverObj)
                        pending_assign = int(no_of_vehicles-exist_driver_map_all.count())
                        while pending_assign > 0:
                            extdriverObj = {
                                "user_id": '',
                                "vehicle_id" : ''
                            }
                            driverVehicleArr.append(extdriverObj)
                            pending_assign = pending_assign-1
                    else:
                        totalVechicle = no_of_vehicles
                        while totalVechicle > 0:
                            extdriverObj = {
                                "user_id": '',
                                "vehicle_id" : ''
                            }
                            driverVehicleArr.append(extdriverObj)
                            totalVechicle = totalVechicle-1

                # exist_driver_map = EngageboostDriverVeichleMap.objects.filter(shipment_id=shipment_id).first()
                # if exist_driver_map:
                # 	extdriverObj = {
                # 		"user_id": exist_driver_map.user_id,
                # 		"vehicle_id" : exist_driver_map.vehicle_id
                # 	}
                # 	driverVehicleArr.append(extdriverObj)

                alldeliveryManagerData = EngageboostDeliveryManagers.objects.using(company_db).filter(website_id=website_id,isblocked='n',isdeleted='n')
                if warehouse_id is not None:
                    alldeliveryManagerData = alldeliveryManagerData.filter(warehouse_ids__iregex=r"\y{0}\y".format(warehouse_id))
                alldeliveryManagerData = alldeliveryManagerData.all()

                if alldeliveryManagerData:
                    alldeliveryManager_Data = DeliveryManagersSerializer(alldeliveryManagerData,many=True)
                    for allDriver in alldeliveryManager_Data.data:
                        allDriverObj = {
                            "user_id": allDriver['user_id'],
                            "name" : allDriver['name']
                        }
                        available_driver.append(allDriverObj)
                # print(json.dumps(available_driver))
                alldeliveryVehicleData = EngageboostVehicleMasters.objects.using(company_db).filter(website_id=website_id,isblocked='n',isdeleted='n')
                if warehouse_id is not None:
                    alldeliveryVehicleData = alldeliveryVehicleData.filter(warehouse_ids__iregex=r"\y{0}\y".format(warehouse_id))
                alldeliveryVehicleData = alldeliveryVehicleData.all()

                # filter( Q(zone_ids__startswith=zone_id+',') | Q(zone_ids__endswith=','+zone_id) | Q(zone_ids__contains=',{0},'.format(zone_id)) | Q(zone_ids__exact=zone_id))
                if alldeliveryVehicleData:
                    alldeliveryVehicle_Data = VehicleMastersSerializer(alldeliveryVehicleData,many=True)
                    for allVehicle in alldeliveryVehicle_Data.data:
                        allVehicleObj = {
                            "id": allVehicle['id'],
                            "vehicle_number" : allVehicle['vehicle_number']
                        }
                        available_vehicle.append(allVehicleObj)
                # print(json.dumps(available_vehicle))
                orderDataList.update({
                    "available_driver":available_driver,
                    "available_vehicle":available_vehicle,
                    "totalVechicle":no_of_vehicles,
                    "driverVehicleArr":driverVehicleArr,
                    "delivery_date":time_slot_date
                })
            if orderDataList:
                data={"status":1,"api_status":orderDataList,"message":"Order List"}
            else:
                data={"status":0,"api_status":orderDataList,"message":"No order list found"}
            return Response(data)
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message":str(error)}
            return Response(data)

class CreateAssignVehicle(generics.ListAPIView):
    def post(self,request):
        company_db = loginview.db_active_connection(request)
        now_utc = datetime.now(timezone.utc).astimezone()
        postdata = request.data
        orderDataList = []
        try:
            website_id = postdata["website_id"]
            shipment_id = postdata["shipment_id"]
            driverVehicleArr = postdata["driverVehicleArr"]
            userId = postdata["userId"]
            delivery_date = postdata["delivery_date"] if postdata.get("delivery_date") else None
            totalVechicle = postdata["totalVechicle"] if postdata.get("totalVechicle") else None
            # driver_id = postdata["driver_id"] if postdata.get("driver_id") else None
            #vehicle_id = postdata["vehicle_id"] if postdata.get("vehicle_id") else None
            if shipment_id > 0:
                EngageboostDriverVeichleMap.objects.using(company_db).filter(shipment_id=shipment_id).delete()

            error_count = 1
            virtual_vechile_id = 1
            for driver in driverVehicleArr:
                vehicle_id = 0
                driver_id = int(driver['user_id'])
                if driver['vehicle_id']:
                    vehicle_id = int(driver['vehicle_id'])
                # print(driver_id)
                # print(vehicle_id)
                if driver_id > 0:
                    #  looping will go here...
                    EngageboostDriverVeichleMap.objects.using(company_db).create(vehicle_id=vehicle_id,driver_id=driver_id,user_id=driver_id,delivery_date=delivery_date,shipment_id=shipment_id,virtual_vechile_id=virtual_vechile_id, created=now_utc)
                    virtual_vechile_id = virtual_vechile_id+1
                    error_count = 0
            if error_count == 0:
                # EngageboostShipmentOrders and  EngageboostShipmentOrderProducts status update
                EngageboostShipmentOrders.objects.using(company_db).filter(shipment=shipment_id,shipment_status='Shipment Processing').update(shipment_status="Ready to Ship")
                EngageboostShipmentOrderProducts.objects.using(company_db).filter(shipment=shipment_id,shipment_status='Shipment Processing').update(shipment_status="Ready to Ship")
                #********ORDER ACTIVITY********#
                # activityType = 1
                # activity_details = common.save_order_activity(company_db,order_id,now_utc,7,"Order is Ready to Ship",user_id,activityType)
            has_planner = EngageboostShipmentOrders.objects.using(company_db).filter(shipment=shipment_id,shipment_status="Shipment Processing").count()
            if has_planner == 0:
                EngageboostShipments.objects.using(company_db).filter(id=shipment_id,shipment_status="Shipment Processing").update(shipment_status="Ready to Ship")

            data={"status":1, "api_status":orderDataList, "message":"Assign Vehicle Successfully Completed."}
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message":str(error)}
        return Response(data)

#_______________Delivery Note_______________#
class ShipingManifest(generics.ListAPIView):
    def post(self,request):
        company_db = loginview.db_active_connection(request)
        postdata = request.data
        manifest_details = {}
        driverName = ''
        vehicle_no = ''
        virtual_vehicle_id = 1
        time = ''
        distance = ''
        shipment_orders_serializer = []
        try:
            website_id = postdata["website_id"] if postdata.get("website_id") else 1
            # start Date time format setting...
            global_setting_date = EngageboostGlobalSettings.objects.using(company_db).get(website_id=website_id,isdeleted='n',isblocked='n')
            global_setting_zone = EngageboostTimezones.objects.using(company_db).get(id = global_setting_date.timezone_id)
            # end Date time format setting...
            shipment_id = postdata["shipment_id"] if postdata.get("shipment_id") else None
            if shipment_id:
                manifest_details_cond = EngageboostManifests.objects.using(company_db).filter(shipment_id=shipment_id).first()
                if manifest_details_cond:
                    manifest_details = ManifestsSerializer(manifest_details_cond)
                    manifest_details = manifest_details.data
                    # start Date time format setting...
                    manifest_details['created'] = common.get_time(manifest_details['created'],global_setting_zone, global_setting_date)
                    # start Date time format setting...
                shipment_order = EngageboostShipmentOrders.objects.using(company_db).filter(shipment=shipment_id).exclude(shipment_status__in=['Invoicing','Picking']).all().order_by('order__sort_by_distance')
                if shipment_order:
                    shipment_orders_serializer = ShipmentsOrdersSerializer(shipment_order,many=True).data
                    for shipmentOrder in shipment_orders_serializer:
                        if shipmentOrder["order"]:
                            order_id = shipmentOrder["order"]["id"]
                            shipmentOrder["OrderList"] = shipmentOrder["order"]

                            deliveryPlanOrder = EngageboostDeliveryPlanOrder.objects.filter(order_id=order_id,shipment_id=shipment_id).first()
                            if deliveryPlanOrder:
                                distance = deliveryPlanOrder.distance
                                virtual_vehicle_id = deliveryPlanOrder.virtual_vechile_id
                                if distance>1000:
                                    distance = str( float("{0:.2f}".format(distance/1000))) + ' Km'
                                else:
                                    distance = str( float("{0:.2f}".format(distance))) + ' mtr'

                                time = deliveryPlanOrder.time
                                if time>3600:
                                    time = str( float("{0:.2f}".format(time/3600))) + ' Hr'
                                else:
                                    time = str( float("{0:.2f}".format(time/60))) + ' Min'

                            driverVehicleMap = EngageboostDriverVeichleMap.objects.filter(shipment_id=shipment_id,virtual_vechile_id=virtual_vehicle_id).first()
                            if driverVehicleMap:
                                driver_id = driverVehicleMap.user_id
                                vehicle_id = driverVehicleMap.vehicle_id
                                if driver_id > 0:
                                    driverManagerdata = EngageboostDeliveryManagers.objects.filter(user_id=driver_id,isdeleted='n', isblocked='n').first()
                                    driverName = driverManagerdata.name
                                if vehicle_id > 0 :
                                    vehicleData = EngageboostVehicleMasters.objects.filter(id=vehicle_id).first()
                                    vehicle_no = vehicleData.vehicle_number

                        shipmentOrder["OrderList"]['DriverName'] = driverName
                        shipmentOrder["OrderList"]['vehicle_no'] = vehicle_no
                        shipmentOrder["OrderList"]['time_required'] = time
                        shipmentOrder["OrderList"]['distance'] = distance
                        shipmentOrder["OrderList"]['virtual_vehicle_id'] = virtual_vehicle_id

                        # start Date time format setting...
                        shipmentOrder['OrderList']['created'] = common.get_time(shipmentOrder["order"]["created"],global_setting_zone, global_setting_date)
                        shipmentOrder['order']['time_slot_date'] = common.get_date_from_datetime(shipmentOrder["order"]["time_slot_date"],global_setting_zone, global_setting_date,'%Y-%m-%d')
                        # end Date time format setting...
            if shipment_orders_serializer:
                data = {"status":1,"api_status":shipment_orders_serializer,"manifest_details":manifest_details,"message":"Order List"}
            else:
                data = {"status":0,"api_status":[],"manifest_details":manifest_details,"message":"Payment not completed by customer"}
            return Response(data)
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message":str(error)}
            return Response(data)

class CreateShipingManifest(generics.ListAPIView):
    def post(self,request):
        company_db = loginview.db_active_connection(request)
        now_utc = datetime.now(timezone.utc)
        # now_utc = pytz.timezone('UTC').localize(datetime.datetime.now())
        # requestdatajson=request.data["shipping_manifest"]
        postdata = request.data
        try:
            website_id = postdata["website_id"]
            shipment_id = postdata["shipment_id"] if postdata.get("shipment_id") else None
            order_ids = postdata["order_ids"] if postdata.get("order_ids") else None
            comment = postdata["comment"] if postdata.get("comment") else None
            user_id = postdata["user_id"] if postdata.get("user_id") else None
            order_ids_arr = order_ids.split(",")

            has_manifest = EngageboostManifests.objects.using(company_db).filter(shipment_id=shipment_id).first()
            if has_manifest:
                EngageboostManifests.objects.using(company_db).filter(id=has_manifest.id).update(shipment_id=shipment_id,order_id=order_ids,comment=comment,modified=now_utc)
                manifest_id = has_manifest.id
                manifest_no = has_manifest.manifest_no
            else:
                manifest_prefix = 'MNF#'
                has_record = EngageboostManifests.objects.last()
                if has_record:
                    last_entry_of_table = EngageboostManifests.objects.order_by("-id").latest("id")
                    manifest_no = last_entry_of_table.manifest_no
                    manifest_no_arr = manifest_no.split("#")
                    row_id = int(manifest_no_arr[1])+int(1)
                    manifest_no = manifest_prefix+str(row_id)
                else:
                    row_id = 1
                    manifest_no = manifest_prefix+str(row_id)

                save_manifest=EngageboostManifests.objects.using(company_db).create(manifest_no=manifest_no,shipment_id=shipment_id,order_id=order_ids,comment=comment,created=now_utc)
                manifest_id = save_manifest.id
            EngageboostShipmentOrders.objects.using(company_db).filter(shipment=shipment_id,order_id__in=order_ids_arr).update(shipment_status="Shipped")
            EngageboostShipmentOrderProducts.objects.using(company_db).filter(shipment=shipment_id,order_id__in=order_ids_arr).update(shipment_status="Shipped")

            has_manifest = EngageboostShipmentOrders.objects.using(company_db).filter(shipment=shipment_id).exclude(shipment_status="Shipped").count()
            if has_manifest == 0:
                EngageboostShipments.objects.using(company_db).filter(id=shipment_id).update(shipment_status="Shipped", modified=now_utc)

                for order_id in order_ids_arr:
                    activityType = 1
                    # EngageboostOrdermaster.objects.using(company_db).filter(id=order_id, shipment_id=shipment_id).update(order_status=1,flag_order=0)
                    rs_check = EngageboostOrdermaster.objects.using(company_db).filter(id=order_id, shipment_id=shipment_id, order_status=100).first()
                    if rs_check:
                        EngageboostOrdermaster.objects.using(company_db).filter(id=order_id, shipment_id=shipment_id, order_status=100).update(order_status=1,flag_order=0)
                        activity_details = common.save_order_activity(company_db,order_id,now_utc,7,"Order is Shipped",user_id,activityType)
                        elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'order_status':'1', 'shipping_status':'Shipped'})
                        # SMS to customer after order approval...
                        common.sms_send_by_AutoResponder(order_id,"Dispatched", 8)
                        # SMS to customer after order approval...

            data={"status":1,"api_status":manifest_id,"manifest_no":manifest_no,"message":"You have successfully created delivery note."}
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message":str(error)}
        return Response(data)

class PrintManifest(generics.ListAPIView):
    def post(self,request):
        company_db = loginview.db_active_connection(request)
        now_utc = datetime.now(timezone.utc).astimezone()
        postdata = request.data
        shipping_label_content = ""
        count=1
        try:
            website_id = postdata["website_id"] if postdata.get("website_id") else 1
            # start Date time format setting...
            global_setting_date = EngageboostGlobalSettings.objects.using(company_db).get(website_id=website_id,isdeleted='n',isblocked='n')
            global_setting_zone = EngageboostTimezones.objects.using(company_db).get(id = global_setting_date.timezone_id)
            # end Date time format setting...
            manifest_id = postdata["manifest_id"] if postdata.get("manifest_id") else None
            shipment_id = postdata["shipment_id"] if postdata.get("shipment_id") else None
            order_ids = postdata["order_ids"] if postdata.get("order_ids") else None
            orderIdsArr = order_ids.split(",")
            condition = EngageboostShipmentOrders.objects.using(company_db).filter(shipment=shipment_id,order_id__in=orderIdsArr,shipment_status__in=['Shipped','Completed']).all()
            if condition:
                orderData = ShipmentsOrdersSerializer(condition,many=True)
                for val in orderData.data:
                    order_id = val["order"]["id"]
                    trent_picklist_id = val["trent_picklist_id"]
                    driverVehicleMap = EngageboostDriverVeichleMap.objects.filter(shipment_id=shipment_id).first()
                    if driverVehicleMap:
                        driver_id = driverVehicleMap.user_id
                        vehicle_id = driverVehicleMap.vehicle_id
                        if driver_id > 0:
                            driverManagerdata = EngageboostDeliveryManagers.objects.filter(user_id=driver_id).first()
                            driverName = driverManagerdata.name
                        if vehicle_id > 0 :
                            vehicleData = EngageboostVehicleMasters.objects.filter(id=vehicle_id).first()
                            vehicle_no = vehicleData.vehicle_number

                    deliveryPlanOrder = EngageboostDeliveryPlanOrder.objects.filter(order_id=order_id,shipment_id=shipment_id).first()
                    if deliveryPlanOrder:
                        distance = deliveryPlanOrder.distance
                        virtual_vehicle_id = deliveryPlanOrder.virtual_vechile_id
                        if distance>1000:
                            distance = str( float("{0:.2f}".format(distance/1000))) + ' Km'
                        else:
                            distance = str( float("{0:.2f}".format(distance))) + ' mtr'

                        time = deliveryPlanOrder.time
                        if time>3600:
                            time = str( float("{0:.2f}".format(time/3600))) + ' Hr'
                        else:
                            time = str( float("{0:.2f}".format(time/60))) + ' Min'

                    val["order"]['DriverName'] = driverName
                    val["order"]['vehicle_no'] = vehicle_no
                    val["order"]['time_required'] = time
                    val["order"]['distance'] = distance
                    val["order"]['virtual_vehicle_id'] = virtual_vehicle_id
                    # cds working for find crate name
                    crate_arr = EngageboostCrates.objects.filter(trent_picklist_id=trent_picklist_id,order_id=order_id,isdeleted='n', isblocked='n').all()
                    crates_name_arr = []
                    for crate_arr_data in crate_arr:
                        crates_name_arr.append(crate_arr_data.crate_barcode)
                    val["crates_name"] = ", ".join(crates_name_arr)
                    buffer_data = common.getAutoResponder(company_db,"Shipped",val["webshop_id"],val["warehouse_id"],val["shipping_method_id"],website_id,8)
                    autoResponderData  = buffer_data["content"]
                    if autoResponderData["email_type"] == 'T':
                        emailContent = autoResponderData["email_content_text"]
                    else:
                        emailContent = autoResponderData["email_content"]
                    emailContent = str(emailContent)
                    # cds working for print manifest
                    emailContent = emailContent.replace("{@zone_name}",str(val["order"]["zone_name"] if val["order"]["zone_name"] else ''))
                    # start Date time format setting...
                    val['order']['time_slot_date'] = common.get_date_from_datetime(val["order"]["time_slot_date"],global_setting_zone, global_setting_date,'%Y-%m-%d')
                    # end Date time format setting...
                    emailContent = emailContent.replace("{@time_slot_date}",str(val["order"]["time_slot_date"]))
                    emailContent = emailContent.replace("{@vehicle_no}",str(val["order"]["vehicle_no"]))
                    emailContent = emailContent.replace("{@DriverName}",str(val["order"]["DriverName"]))
                    emailContent = generateManifestFormat(company_db,website_id,count,manifest_id, val,emailContent)
                    shipping_label_content+=emailContent
                    count +=1

                data={"status":1,"message":"Printing manifest","email_content":shipping_label_content}
            else:
                data={"status":0,"message": "No manifest to print"}
            return Response(data)
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
            return Response(data)

def generateManifestFormat(company_db,website_id,count,manifest_id,manifest_data,emailContent):
    total_str = ''
    if manifest_id:
        manifest_details_cond = EngageboostManifests.objects.using(company_db).filter(id=manifest_id).first()
        if manifest_details_cond:
            manifest_details = ManifestsSerializer(manifest_details_cond)
            manifest_details = manifest_details.data
            emailContent = emailContent.replace("{@manifest_no}",str(manifest_details["manifest_no"] if manifest_details["manifest_no"] else ''))

        total_str+='<tr>'
        total_str+='<td>'+str(count)+'</td>'
        total_str+='<td>'+str(manifest_data['order']['custom_order_id'])+'</td>'
        total_str+='<td>'+str(manifest_data['order']['delivery_name'])+'</td>'
        total_str+='<td>'+str(manifest_data['order']['delivery_street_address'])+ ', '+str(manifest_data['order']['delivery_street_address1'])+'</td>'
        total_str+='<td>'+str(manifest_data['no_of_crates'])+'('+ str(manifest_data['crates_name']) + ')</td>'
        total_str+='<td>'+str(manifest_data['total_quantity'])+'</td>'
        total_str+='<td>'+str(manifest_data['order']['custom_msg'])+'</td>'
        total_str+='<td>'+str(manifest_data['order']['payment_method_name'])+'</td>'
        total_str+='<td>'+ str( float("{0:.2f}".format(manifest_data['order']['gross_amount'])))+'</td>'
        total_str+='<td class="cus_sign">&nbsp;</td>'
        total_str+='<td>'+str(manifest_data['order']['applied_coupon'])+'</td>'
        total_str+='</tr>'
        #print(total_str)
    emailContent = emailContent.replace('{@ORDER_BOX}',str(total_str if total_str else ''))
    return emailContent

class print_barcode(generics.ListAPIView):
    def post(self,request):
        postdata = request.data
        picklist_id  = postdata['picklist_id']
        rs_picklist = EngageboostPicklistProducts.objects.filter(picklist_id=picklist_id).values_list('product_id').distinct().all()

        rs = EngageboostProducts.objects.filter(id__in=rs_picklist).values('id', 'name', 'sku', 'title', 'ean' ).all()
        serializar_data = EngageboostProductsSerializer(rs, many=True)

        data = {
            'status':1,
            'api_status':serializar_data.data
        }
        return Response(data)

class OrderlistByPicklist(generics.ListAPIView):
    def get(self, request, pk, format=None):
        company_db = loginview.db_active_connection(request)
        rs_picklist = EngageboostTrentPicklists.objects.using(company_db).filter(id=pk).first()
        if rs_picklist:
            rs_data = TrentPicklistShipmentSerializer(rs_picklist)
            data = {
                "status":1,
                "message":"success",
                "api_status":rs_data.data
            }
        else:
            data = {
                "status":0,
                "message":"No data found.",
                "api_status":{}
            }
        return Response(rs_data.data)
# grn_mobile , getting order details in GRN page...picking page...
class OrderDetailsByPicklistid(generics.ListAPIView):
    def get(self, request, pk, website_id, format=None):
        rs_picklist_orders = EngageboostShipmentOrders.objects.filter(shipment=pk).all().order_by('order_id')
        if rs_picklist_orders:
            rs_data = PicklistProductDetailsSerializer(rs_picklist_orders, many=True)
            rs_data = rs_data.data
            #print(json.dumps(rs_data))
            # order_data = {}
            date_format = '%d-%m-%Y'
            find_global_settings = EngageboostGlobalSettings.objects.filter(website_id=website_id,isdeleted = 'n',isblocked = 'n')
            if find_global_settings.count()>0:
                GlobalSettings = find_global_settings.first()
                date_format = GlobalSettings.date_format

            total_grn_completed_order = 0
            order_ids = []
            for rsdata  in rs_data:
                order_ids.append(rsdata['order'])
                if rsdata['no_of_crates'] is None or rsdata['no_of_crates']=="":
                    rsdata['no_of_crates'] = 0
                picklist_id = rsdata['trent_picklist_id']
                display_time_slot_date = rsdata['order_data']['time_slot_date']
                f = "%Y-%m-%d"
                display_time_slot_date = datetime.strptime(display_time_slot_date, f)
                display_time_slot_date = display_time_slot_date.strftime(date_format)
                rsdata['order_data']['display_time_slot_date'] = display_time_slot_date
                for orderdata in rsdata['shipment_order_product']:
                    is_sub_prod_exist = 'N'
                    product_id = orderdata['order_product_details']['product']['id']
                    count_all_data_related = EngageboostRelatedProducts.objects.filter(product_id=product_id,related_product_type = '5').count()
                    if count_all_data_related > 0 and rsdata['shipment_status'] == 'Picking':
                        is_sub_prod_exist = 'Y'

                    sub_prod_sku = ''
                    if orderdata['order_product_details']['substitute_product_id'] > 0:
                        sub_prod = EngageboostProducts.objects.filter(id=orderdata['order_product_details']['substitute_product_id']).first()
                        sub_prod_sku = sub_prod.name

                    order_data = {}
                    selling_price = float(orderdata['order_product_details']['product_price'])+float(orderdata['order_product_details']['product_tax_price'])
                    product_image = ''
                    if orderdata['order_product_details']['product']['product_images']:
                        for image_data in orderdata['order_product_details']['product']['product_images']:
                            if image_data['is_cover'] == 1:
                                product_image = image_data['img']

                    uom_name = ''
                    if orderdata['order_product_details']['product']['weight'] and orderdata['order_product_details']['product']['uom']:
                        uom_name = orderdata['order_product_details']['product']['uom']['uom_name']
                        if orderdata['order_product_details']['weight'] and float(orderdata['order_product_details']['weight']) > 0:
                            weight = orderdata['order_product_details']['weight']
                        else:
                            weight = orderdata['order_product_details']['product']['weight']
                        uom_name = str(weight) + ' '+ uom_name

                    # order_data.update({
                    #     "product_id":product_id,
                    #     "product_name":orderdata['order_product_details']['product']['name'],
                    #     "product_sku":orderdata['order_product_details']['product']['sku'],
                    #     "sub_prod_sku":sub_prod_sku,
                    #     "product_default_price":orderdata['order_product_details']['product']['default_price'],
                    #     "product_ean":orderdata['order_product_details']['product']['ean'],
                    #     "uom_name": uom_name,
                    #     "product_image":product_image,
                    #     #sahooooo
                    #
                    #     "product_quantity":orderdata['order_product_details']['quantity'],
                    #     "deleted_quantity":orderdata['order_product_details']['deleted_quantity'],
                    #     "product_price":orderdata['order_product_details']['product_price'],
                    #
                    #     "selling_price":selling_price,
                    #     "mrp":orderdata['order_product_details']['mrp'],
                    #     "product_discount_price":orderdata['order_product_details']['product_discount_price'],
                    #     "product_discount_rate":orderdata['order_product_details']['product_discount_rate'],
                    #     "product_tax_price":orderdata['order_product_details']['product_tax_price'],
                    #     "tax_percentage":orderdata['order_product_details']['tax_percentage'],
                    #     "shipping_price":orderdata['order_product_details']['shipping_price'],
                    #     "assign_to":orderdata['order_product_details']['assign_to'],
                    #     "assign_wh":orderdata['order_product_details']['assign_wh'],
                    #     "substitute_product_id":orderdata['order_product_details']['substitute_product_id'],
                    #     "is_sub_prod_exist": is_sub_prod_exist
                    # })
                    order_data.update({
                        "product_id": product_id,
                        "product_name": orderdata['order_product_details']['product']['name'],
                        "product_sku": orderdata['order_product_details']['product']['sku'],
                        "sub_prod_sku": sub_prod_sku,
                        "product_default_price": orderdata['order_product_details']['product']['default_price'],
                        "product_ean": orderdata['order_product_details']['product']['ean'],
                        "uom_name": uom_name,
                        "product_image": product_image,
                        # sahooooo

                        "product_quantity": orderdata['order_product_details']['quantity'],
                        "deleted_quantity": orderdata['order_product_details']['deleted_quantity'],
                        "product_price": orderdata['order_product_details']['product_price'],

                        "selling_price": selling_price,
                        "mrp": orderdata['order_product_details']['mrp'],
                        "product_discount_price": orderdata['order_product_details']['product_discount_price'],
                        "product_discount_rate": orderdata['order_product_details']['product_discount_rate'],
                        "product_tax_price": orderdata['order_product_details']['product_tax_price'],
                        "tax_percentage": orderdata['order_product_details']['tax_percentage'],
                        "shipping_price": orderdata['order_product_details']['shipping_price'],
                        "assign_to": orderdata['order_product_details']['assign_to'],
                        "assign_wh": orderdata['order_product_details']['assign_wh'],
                        "substitute_product_id": orderdata['order_product_details']['substitute_product_id'],
                        "is_sub_prod_exist": is_sub_prod_exist,
                        "custom_field_name": orderdata['order_product_details']['custom_field_name'],
                        "custom_field_value": orderdata['order_product_details']['custom_field_value']
                    })
                    orderdata.pop('order_product_details')
                    orderdata['order_product_details'] = order_data
                rsdata['order_data']['shipment_order_product'] = rsdata['shipment_order_product']
                rsdata.pop('shipment_order_product')

            if len(order_ids)>0:
                # rs_time_slot = EngageboostOrdermaster.objects.filter(id__in=order_ids).exclude(slot_start_time__isnull=True).values('time_slot_id', 'slot_start_time', 'slot_end_time').all().distinct()
                rs_time_slot = EngageboostOrdermaster.objects.filter(id__in=order_ids).exclude(slot_start_time__isnull=True).values('time_slot_id', 'slot_start_time', 'slot_end_time',ids_arr=ArrayAgg('id')).all().annotate(total_order=Count('id'))
                if rs_time_slot:
                    for timeslot in rs_time_slot:
                        grn_completed_count = EngageboostShipmentOrders.objects.filter(order_id__in=timeslot['ids_arr'], isdeleted='n').exclude(shipment_status__in=['Picking','Created']).count()
                        if grn_completed_count:
                            timeslot['total_grn_completed_order'] = grn_completed_count
                            total_grn_completed_order = grn_completed_count
                        else:
                            timeslot['total_grn_completed_order'] = 0
                        sort_id = timeslot['ids_arr']
                        sort_id.sort()
                        timeslot['ids_arr'] = sort_id
            data = {
                "status":1,
                "message":"success",
                "api_status":rs_data,
                "time_slot":rs_time_slot,
                "shipment_id":pk,
                "picklist_id":picklist_id,
                "total_grn_completed_order":total_grn_completed_order
            }
        else:
            data = {
                "status":0,
                "message":"No data found.",
                "api_status":{}
            }

        return Response(data)

class get_grn_order_details(generics.ListAPIView):
    def post(self,request):
        requestdata         = request.data
        trent_picklist_id   = requestdata['trent_picklist_id']
        order_id            = requestdata['order_id']
        crate_count = 0
        rs_order = EngageboostOrdermaster.objects.filter(id=order_id).first()
        time_slot_date = rs_order.time_slot_date
        time_slot_time = rs_order.time_slot_id
        assign_wh      = rs_order.assign_wh
        if trent_picklist_id>0 and order_id>0:
            crate_count = EngageboostCrates.objects.filter(trent_picklist_id=trent_picklist_id, order_id=order_id, isdeleted='n', isblocked='n').count()
        if trent_picklist_id:
            rs_picklist = EngageboostShipmentOrderProducts.objects.filter(trent_picklist_id=trent_picklist_id, order_id=order_id).all()
            if rs_picklist:
                rs_data = EngageboostShipmentOrderProductsSerializer(rs_picklist, many=True)
                rs_data = rs_data.data
                for data in rs_data:
                    if len(data['product_details'])>0:
                        data['product_name']   = data['product_details']['product_name']
                        data['sku']            = data['product_details']['sku']
                        data['default_price']  = data['product_details']['default_price']
                    # Stock
                    if data['warehouse_id']:
                        rs_stock = EngageboostProductStocks.objects.filter(product_id=data['product'], warehouse_id=data['warehouse_id']).first()
                        if rs_stock:
                            data['real_stock'] = rs_stock.real_stock
                        else:
                            data['real_stock'] = 0
                    else:
                        data['real_stock'] = 0

                    data.pop('product_details')
                data = {
                    "status":1,
                    "message":"success",
                    "time_slot_date":time_slot_date,
                    "time_slot_time":time_slot_time,
                    "crate_count":crate_count,
                    "trent_picklist_id":trent_picklist_id,
                    "shipment_order_product":rs_data
                }
            else:
                data = {
                    "status":0,
                    "message":"No data found.",
                    "shipment_order_product":{}
                }
        else:
            data = {
                "status":0,
                "message":"Provide trent picklist id."
            }
        return Response(data)
## cds working
# Select order from dropdown in grn page
class get_grn_order_details_by_order_id(generics.ListAPIView):
    def post(self,request):
        requestdata         = request.data
        trent_picklist_id   = requestdata['trent_picklist_id']
        order_id            = requestdata['order_id']
        website_id          = requestdata['website_id']
        product_id = 0
        if request.data.get('product_id'):
            product_id = request.data['product_id']

        date_format = '%d-%m-%Y'
        find_global_settings = EngageboostGlobalSettings.objects.filter(website_id=website_id,isdeleted = 'n',isblocked = 'n')
        if find_global_settings.count()>0:
            GlobalSettings = find_global_settings.first()
            date_format = GlobalSettings.date_format

        rs_picklist_orders = EngageboostShipmentOrders.objects.filter(trent_picklist_id=trent_picklist_id, order_id=order_id).all().order_by('order_id')
        if product_id > 0:
            rs_picklist_orders = rs_picklist_orders.filter(product_id=trent_picklist_id)

        if rs_picklist_orders:
            rs_data = PicklistProductDetailsSerializer(rs_picklist_orders, many=True)
            rs_data = rs_data.data
            order_ids = []
            for rsdata  in rs_data:
                order_ids.append(rsdata['order'])
                if rsdata['no_of_crates'] is None or rsdata['no_of_crates']=="":
                    rsdata['no_of_crates'] = 0

                display_time_slot_date = rsdata['order_data']['time_slot_date']
                f = "%Y-%m-%d"
                display_time_slot_date = datetime.strptime(display_time_slot_date, f)
                display_time_slot_date = display_time_slot_date.strftime(date_format)
                rsdata['order_data']['display_time_slot_date'] = display_time_slot_date

                for orderdata in rsdata['shipment_order_product']:
                    is_sub_prod_exist = 'N'
                    product_id = orderdata['order_product_details']['product']['id']
                    count_all_data_related = EngageboostRelatedProducts.objects.filter(product_id=product_id,related_product_type = '5').count()
                    if count_all_data_related > 0 and rsdata['shipment_status'] == 'Picking':
                        is_sub_prod_exist = 'Y'

                    sub_prod_sku = ''
                    if orderdata['order_product_details']['substitute_product_id'] > 0:
                        sub_prod = EngageboostProducts.objects.filter(id=orderdata['order_product_details']['substitute_product_id']).first()
                        sub_prod_sku = sub_prod.name

                    order_data = {}
                    selling_price = float(orderdata['order_product_details']['product_price'])+float(orderdata['order_product_details']['product_tax_price'])
                    product_image = ''
                    if orderdata['order_product_details']['product']['product_images']:
                        for image_data in orderdata['order_product_details']['product']['product_images']:
                            if image_data['is_cover'] == 1:
                                product_image = image_data['img']

                    uom_name = ''
                    if orderdata['order_product_details']['product']['weight'] and orderdata['order_product_details']['product']['uom']:
                        uom_name = orderdata['order_product_details']['product']['uom']['uom_name']
                        if orderdata['order_product_details']['weight'] and float(orderdata['order_product_details']['weight']) > 0:
                            weight = orderdata['order_product_details']['weight']
                        else:
                            weight = orderdata['order_product_details']['product']['weight']
                        uom_name = str(weight) + ' '+ uom_name

                    order_data.update({
                        "product_id":product_id,
                        "product_name":orderdata['order_product_details']['product']['name'],
                        "product_sku":orderdata['order_product_details']['product']['sku'],
                        "sub_prod_sku":sub_prod_sku,
                        "product_default_price":orderdata['order_product_details']['product']['default_price'],
                        "product_ean":orderdata['order_product_details']['product']['ean'],
                        "uom_name": uom_name,
                        "product_image":product_image,
                        #sahooooo

                        "product_quantity":orderdata['order_product_details']['quantity'],
                        "deleted_quantity":orderdata['order_product_details']['deleted_quantity'],
                        "product_price":orderdata['order_product_details']['product_price'],

                        "selling_price":selling_price,
                        "mrp":orderdata['order_product_details']['mrp'],
                        "product_discount_price":orderdata['order_product_details']['product_discount_price'],
                        "product_discount_rate":orderdata['order_product_details']['product_discount_rate'],
                        "product_tax_price":orderdata['order_product_details']['product_tax_price'],
                        "tax_percentage":orderdata['order_product_details']['tax_percentage'],
                        "shipping_price":orderdata['order_product_details']['shipping_price'],
                        "assign_to":orderdata['order_product_details']['assign_to'],
                        "assign_wh":orderdata['order_product_details']['assign_wh'],
                        "substitute_product_id":orderdata['order_product_details']['substitute_product_id'],
                        "is_sub_prod_exist": is_sub_prod_exist
                    })
                    orderdata.pop('order_product_details')
                    orderdata['order_product_details'] = order_data

                rsdata['order_data']['shipment_order_product'] = rsdata['shipment_order_product']
                rsdata.pop('shipment_order_product')
            data = {
                "status":1,
                "message":"success",
                "api_status":rs_data
            }
        else:
            data = {
                "status":0,
                "message":"No data found.",
                "api_status":{}
            }
        return Response(data)

class get_order_products_info(generics.ListAPIView):
    def post(self,request):
        requestdata = request.data
        ean         = requestdata['ean']
        order_id    = requestdata['order_id']
        scan_qty    = requestdata['scan_qty']
        num_type    = requestdata['num_type']
        trent_picklist_id = requestdata['trent_picklist_id']
        return_arr = []
        if ean and order_id > 0:
            order_product_data = EngageboostShipmentOrderProducts.objects.filter(order_id=order_id,product_id__ean=ean,trent_picklist_id=trent_picklist_id).first()
            order_product = EngageboostShipmentOrderProductsPicklistSerializer(order_product_data, partial=True)
            if order_product and scan_qty <= order_product_data.quantity:
                #     return_arr['po_product_id'] = order_product_data['ShipmentOrderProduct']['id']
                #     return_arr['order_id'] = order_id;
                #     return_arr['product_id'] = order_product_data['ShipmentOrderProduct']['product_id']
                #     return_arr['item_scan'] = scan_qty
                #     return_arr['price'] = order_product_data['OrderProduct']['product_price']+order_product_data['OrderProduct']['product_tax_price']+order_product_data['OrderProduct']['product_excise_duty']+order_product_data['OrderProduct']['product_discount_price']
                #     return_arr['error'] = 0
                # } else if(!empty(order_product_data) && scan_qty > order_product_data['ShipmentOrderProduct']['quantity']) {
                #     return_arr['error'] = 1
                # } else {
                #     return_arr['error'] = 2
                # }
                data = {
                    "status":1,
                    "shipment_order_product_id":1,
                    "message":"success",
                    "api_status":order_product.data
                }
            else:
                data = {
                    "status":0,
                    "shipment_order_product_id":0,
                    "message":"No data found.",
                    "api_status":{}
                }
        else:
            data = {
                "status":0,
                "shipment_order_product_id":0,
                "message":"No data found.",
                "api_status":{}
            }
        return Response(data)

class search_picked_products(generics.ListAPIView):
    def post(self,request):
        requestdata         = request.data
        trent_picklist_id   = requestdata['trent_picklist_id']
        order_id            = requestdata['order_id']
        rs_picklist = EngageboostShipmentOrderProducts.objects.filter(trent_picklist_id=trent_picklist_id, order_id=order_id).all()
        if rs_picklist:
            rs_data = EngageboostShipmentOrderProductsSerializer(rs_picklist, many=True)
            rs_data = rs_data.data

            for data in rs_data:
                if len(data['product_details'])>0:
                    data['ean']            = data['product_details']['ean']
                    data['sku']            = data['product_details']['sku']
                    data['product_name']   = data['product_details']['product_name']
                    data['default_price']  = data['product_details']['default_price']
                data.pop('product_details')
            data = {
                "status":1,
                "message":"success",
                "api_status":rs_data
            }
        else:
            data = {
                "status":0,
                "message":"No data found.",
                "api_status":{}
            }
        return Response(data)

class add_crates(generics.ListAPIView):
    def post(self,request):
        crate_count        = 0
        requestdata        = request.data
        crate_barcode      = requestdata['crate_barcode']
        trent_picklist_id  = requestdata['trent_picklist_id']
        order_id           = requestdata['order_id']
        now_utc            = datetime.now(timezone.utc).astimezone()
        order_data_save = {}
        try:
            if trent_picklist_id > 0 and order_id > 0:
                order_data_save = {
                    "crate_barcode":crate_barcode,
                    "trent_picklist_id":trent_picklist_id,
                    "order_id":order_id,
                    "created":now_utc
                }
                count_crate = EngageboostCrates.objects.filter(trent_picklist_id=trent_picklist_id, order_id=order_id, crate_barcode=crate_barcode,isdeleted='n',isblocked='n').count()
                if count_crate <= 0:
                    EngageboostCrates.objects.create(**order_data_save)
                    crate_count = 1
                crate_count = EngageboostCrates.objects.filter(trent_picklist_id=trent_picklist_id, order_id=order_id,isdeleted='n',isblocked='n').count()
                EngageboostShipmentOrders.objects.filter(trent_picklist_id=trent_picklist_id, order_id=order_id).update(no_of_crates=crate_count)
            data = {
                "status":1,
                "message" : 'Crate added successfully.',
                "crate_count":crate_count
            }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

class delete_crates(generics.ListAPIView):
    def post(self,request):
        crate_count         = 0
        requestdata         = request.data
        action_id           = requestdata['action_id']
        trent_picklist_id   = requestdata['trent_picklist_id']
        order_id            = requestdata['order_id']
        now_utc             = datetime.now(timezone.utc).astimezone()
        try:
            if len(action_id)>0:
                EngageboostCrates.objects.filter(id__in=action_id).update(isdeleted='y')
            if int(trent_picklist_id)>0 and int(order_id)>0:
                crate_count = EngageboostCrates.objects.filter(trent_picklist_id=trent_picklist_id, order_id=order_id,isdeleted='n',isblocked='n').count()
                EngageboostShipmentOrders.objects.filter(trent_picklist_id=trent_picklist_id, order_id=order_id).update(no_of_crates=crate_count)
            data = {
                "status":1,
                "ack":1,
                "crate_count":crate_count
            }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

class get_all_crates(generics.ListAPIView):
    def post(self,request):
        requestdata         = request.data
        trent_picklist_id   = requestdata['trent_picklist_id']
        order_id            = requestdata['order_id']
        search = None
        if "search" in requestdata:
            search              = requestdata['search']
        if trent_picklist_id>0 and order_id>0:
            rs_crate = EngageboostCrates.objects.filter(trent_picklist_id=trent_picklist_id,order_id=order_id,isdeleted='n',isblocked='n').all()
            if search is not None:
                rs_crate = rs_crate.filter(Q(crate_barcode__icontains=search))
            if rs_crate:
                crate_data = CratesSerializer(rs_crate, many=True)
                crate_data = crate_data.data
                data = {
                    "status":1,
                    "message":"success",
                    "crate_list":crate_data
                }
            else:
                data = {
                    "status":0,
                    "message":"No data found",
                    "crate_list":[]
                }
        else:
            data = {
                "status":0,
                "message":"Trent picklist id and Order id should not be blank."
            }
        return Response(data)

#  Save as Draft GRN start here....
class grn_save_as_draft(generics.ListAPIView):
    def post(self,request):
        requestdata = request.data
        order_id    = requestdata['order_id']
        shipment_id = requestdata['shipment_id']
        order_arr   = requestdata['shipmentOrderProduct']
        if len(order_arr)>0:
            for grn_data in order_arr:
                update_shipment_order_product = {
                    "quantity":grn_data['quantity'],
                    "shortage":grn_data['shortage'],
                    "returns":grn_data['returns'],
                    "grn_quantity":grn_data['grn_quantity']
                }
                EngageboostShipmentOrderProducts.objects.filter(order_id=order_id, product_id=grn_data['product_id'],shipment=shipment_id).update(**update_shipment_order_product)
            rs_shipment_order_product   = EngageboostShipmentOrderProducts.objects.filter(order_id=order_id, shipment=shipment_id).all()
            shipment_order_product_data = EngageboostShipmentOrderProductsSerializer(rs_shipment_order_product, many=True)
            data = {
                "status":1,
                "message:":"Picking product data save successfully.",
                "api_status":shipment_order_product_data.data
            }
        else:
            data = {
                "status":0,
                "message:":"Order Products not found.",
                "api_status":{}
            }
        return Response(data)

def update_stock_all_refund(product_id=None,warehouse_id=None,quantity=0,status=None,stock_minus_type=None) :
    rs_stock    = EngageboostProductStocks.objects.filter(product_id=product_id, warehouse_id=warehouse_id).first()
    stock_data  = StockSerializer(rs_stock)
    stock_data  = stock_data.data
    safety_stock    = 0
    virtual_stock   = 0
    stock           = 0
    if len(stock_data) >0:
        if stock_data['virtual_stock']=='null':
            virtual_stock = 0
        if stock_data['safety_stock']=='null':
            safety_stock = 0
        if stock_data['stock']=='null':
            stock = 0

    # /*Real stock increase*/
    if status == "Increase" or status == "Refund":
        if stock_minus_type=="real" and len(stock_data)>0:
            stoack_data_update = {
                "stock":int(stock_data['stock'])+int(quantity),
                "real_stock":(int(stock_data['stock'])+int(quantity))-(int(quantity)-int(safety_stock)-int(virtual_stock))
            }
            EngageboostProductStocks.objects.filter(id=stock_data['id']).update(**stoack_data_update)

    # /*Virtual stock decrease*/
    if status == "Decrease" and stock_minus_type == "virtual":
        if len(stock_data)>0:
            stoack_data_update = {
                "virtual_stock":int(stock_data['virtual_stock'])+int(quantity),
                "real_stock":int(stock_data['stock'])-int(virtual_stock)-int(quantity)-int(safety_stock)
            }
            EngageboostProductStocks.objects.filter(id=stock_data['id']).update(**stoack_data_update)

    # /*Real stock decrease*/
    if status == "Decrease" and stock_minus_type == "real":
        if len(stock_data)>0:
            stoack_data_update = {
                "virtual_stock":int(stock_data['stock'])-int(quantity),
                "real_stock":int(stock_data['stock'])-int(quantity)-int(safety_stock)-int(virtual_stock)
            }
            EngageboostProductStocks.objects.filter(id=stock_data['id']).update(**stoack_data_update)

class grn_complete(generics.ListAPIView):
    def post(self,request):
        requestdata = request.data
        order_id    = requestdata['order_id']
        order_arr           = requestdata['shipmentOrderProduct']
        company_db          = loginview.db_active_connection(request)
        # ** GRN data save start here here........
        grn_data = requestdata
        order_id               = requestdata['order_id']
        logged_user_id         = requestdata['userId']
        trent_picklist_id      = requestdata['trent_picklist_id']
        shipment_id      	   = requestdata['shipment_id']
        no_of_crates           = requestdata['no_of_crates']
        shipment_order_id      = requestdata['id']
        total_quantity         = 0
        total_scan_quantity    = 0
        try:
            for shipmentProducts in order_arr:
                shipment_order_product_id   = shipmentProducts['id']
                product_id                  = shipmentProducts['product_id']
                quantity                    = shipmentProducts['quantity']
                if shipmentProducts['grn_quantity']:
                    item_scan = shipmentProducts['grn_quantity']
                else:
                    item_scan = 0
                if shipmentProducts['shortage']:
                    shortage = shipmentProducts['shortage']
                else:
                    shortage = 0
                total_quantity              = total_quantity+quantity
                total_scan_quantity         = total_scan_quantity+item_scan
                update_shipment_order_product = {
                    "shortage":shortage,
                    "grn_quantity":item_scan,
                    "shipment_status":"Invoicing"
                }
                EngageboostShipmentOrderProducts.objects.filter(shipment=shipment_id, order_id=order_id, product_id=product_id).update(**update_shipment_order_product)
                EngageboostOrderProducts.objects.filter(order_id=order_id,product_id=product_id).update(shortage=shortage,grn_quantity=item_scan)
                elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'shipping_status':'Invoicing'})
                # ** update order product...
                update_order_and_order_products(order_id)
            # update orderlist , order product and shipment for flag order....
            if total_scan_quantity<=0:
                EngageboostOrdermaster.objects.filter(id=order_id).update(flag_order=1)

            update_shipment_order = {
                "no_of_crates":no_of_crates,
                "shipment_status":"Invoicing",
                "total_quantity":total_scan_quantity
            }
            EngageboostShipmentOrders.objects.filter(id=shipment_order_id,shipment=shipment_id).update(**update_shipment_order)
            # ** order activity....
            common.save_order_activity(company_db,order_id,None,7,"Order is Invoicing", 1, logged_user_id)
            # ** grn created date update...
            now_utc = datetime.now(timezone.utc).astimezone()
            EngageboostOrdermaster.objects.filter(id=order_id,shipment_id=shipment_id).update(grn_created_date=now_utc)
            AllshipmentOrder = EngageboostShipmentOrders.objects.filter(shipment=shipment_id, shipment_status__in=['Picking']).all()
            if len(AllshipmentOrder)>0:
                pass
            else:
                EngageboostShipments.objects.filter(id=shipment_id).update(shipment_status='Invoicing')
                EngageboostTrentPicklists.objects.filter(id=trent_picklist_id).update(picklist_status='Invoicing')

            # email to customer after order approval...
            str_link = common.email_send_by_AutoResponder(order_id, 10)
            # if str_link is not None:
            # 	str_link = urllib.parse.unquote(str_link)
            final_link = "https://www.gogrocery.ae/approved-order/place-order/"+str_link
            # email to customer after order approval...
            # Save Payment Link for Lifco
            EngageboostOrdermaster.objects.filter(id=order_id).update(delivery_sap_ecustomer_state_no=final_link)
            # SMS to customer after order approval...
            # common.sms_send_by_AutoResponder(order_id,None, 10, final_link)
            # SMS to customer after order approval...

            data={
                "status":1,
                "api_status" : 'success',
                "message":"You have successfully created Picking."
            }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

def update_order_refund(order_id,product_id,refund_quantity=0,shortage_quantity=0, return_order_type='Cancellation',grn_quantity=0):
    website_id      = 1
    logged_user_id  = 1
    now_utc             = datetime.now(timezone.utc).astimezone()
    rs_order_product = EngageboostOrderProducts.objects.filter(order_id=order_id, product_id=product_id).all()
    all_data_shipped = OrderProductsViewSerializer(rs_order_product, many=True)
    all_data_shipped = all_data_shipped.data
    # print(json.dumps(all_data_shipped.data))
    rest_quantity  = int(refund_quantity) + int(shortage_quantity)
    for shipped in all_data_shipped:
        if int(rest_quantity)>=shipped['quantity']:
            updatequantity = shipped['quantity']
        else:
            updatequantity = rest_quantity

        if shortage_quantity > 0 and shortage_quantity > shipped['quantity']:
            shortage_quantity = shipped['quantity']

        shipped_save = {}
        if return_order_type == 'Cancellation':
            return_qty = int(shipped['returns']) + int(updatequantity)
            EngageboostOrderProducts.objects.filter(id=shipped['id']).update(returns=return_qty)
        else:
            shortage_qty = 0
            if shortage_quantity > 0:
                shortage_qty = shortage_quantity
            else:
                shortage_qty = shipped['shortage']
            shipped_save.update({"shortage":shortage_qty})
            grn_qty = 0
            if int(refund_quantity) > 0:
                if return_order_type == 'GRN Cancellation':
                    shipped_save.update({"returns":refund_quantity})
                else:
                    if int(refund_quantity) > 0 and int(shipped['quantity']) >= (int(shipped['returns'])+int(refund_quantity)):
                        refund_qty = 0
                        refund_qty =  int(shipped['returns'])+int(refund_quantity)
                        shipped_save.update({"returns":refund_qty})

                if grn_quantity == 0 and ind(shipped['grn_quantity']) > 0:
                    grn_qty = int(shipped['grn_quantity'])-int(refund_quantity)
                    # shipped_save.update({"grn_quantity":grn_qty})

            if grn_quantity > 0:
                grn_qty = grn_quantity

            shipped_save.update({"grn_quantity":grn_qty})

#             # /*if(instock_qty > 0) {
#             #     shipped_save['OrderProduct']['instock_qty'] = instock_qty
#             # }*/
            EngageboostOrderProducts.objects.filter(id=shipped['id']).update(**shipped_save)

            total_price = int(updatequantity)*float(shipped['product_price'])
            tax_price   = int(updatequantity)*float(shipped['product_tax_price'])  # added by cds for tax...
            total_price_discount = int(updatequantity)*float(shipped['product_discount_price'])
#             # /*this is for main price minus*/
            net_amount = float(shipped['net_amount'])-float(total_price)
            total_tax_amount =  float(shipped['tax_amount']) - float(tax_price) # added by cds for tax...

#             # # Shipping cost calculation for return product...
            if return_order_type != 'GRN Cancellation':
                shortage_amount = 0
                if shipped_save['shortage'] > 0:
                    shortage_amount = int(shipped_save['shortage'])*float(shipped['product_price'])

                order_amt = float(net_amount) + float(total_tax_amount) + float(shortage_amount)

                # shipping_arr = this->get_information_shipping_admin(shipped['OrderList']['delivery_country'],shipped['OrderList']['delivery_state'], order_amt, website_id) # shipping adn cod
                # shipping_cost = floatval(shipping_arr['shipping_cost'])
                # this->OrderList->id = order_id
                # this->OrderList->saveField('shipping_cost', shipping_cost)
                shipping_cost = 0  # Static for testing....
                EngageboostOrdermaster.objects.filter(id=order_id).update(shipping_cost=shipping_cost)

#             # # end Shipping cost calculation for return product...
            if return_order_type != 'Delete Cancellation':
                # this->update_order_and_order_products(order_id, return_order_type,website_id)
                update_order_and_order_products(order_id, return_order_type, website_id)

            return_message = "Return from GRN"
            if refund_quantity > 0:
                if return_order_type == 'GRN Cancellation' or return_order_type == 'Delete Cancellation':
                    order_return_details = {
                        "website_id":website_id,
                        "order_id":order_id,
                        "product_id":shipped['product_id'],
                        "return_by_id":logged_user_id,
                        "quantity":refund_quantity,
                        "reason":return_message,
                        "return_status":"Authorized"
                    }
                    EngageboostOrderReturnDetails.objects.create(**order_return_details)

                    customer_return_details = {}
                    customer_return_details = {
                        "customer_id":shipped['customer_id'],
                        "order_id":order_id,
                        "product_id":shipped['product_id'],
                        "customer_return_status":"Return Initiated"
                    }
                    EngageboostCustomerReturnStatus.objects.create(**customer_return_details)

                    activity_time = now_utc
                    activity_msg = "Return Reason : "+return_message+" for product sku-"+shipped['product']['sku']
                    order_status = 7
                    common.save_order_activity(order_id,activity_time,order_status,activity_msg)
                    EngageboostOrdermaster.objects.filter(id=order_id).update(return_status="Processing")

def get_information_shipping_admin(country_id='99',state_id=None, order_amt=None, website_id=None):
    website_id = 1
    free_shipping_min_amount = 0
    shippingObj = EngageboostShippingMastersSettings.objects.filter(website_id=website_id,status='Yes',isblocked='n').filter(Q(country_ids__istartswith=country_id+",")|Q(country_ids__iendswith=","+country_id)|Q(country_id__contains=","+country_id+",")|Q(country_id=country_id))
    # conditions = "ShippingSetting.website_id='".website_id."' AND ShippingSetting.status='Yes' AND FIND_IN_SET('".country_id."', ShippingSetting.country_ids) AND ShippingSetting.isblocked='n'"
    # this->ShippingSetting->bindModel(array('belongsTo'=>array(
    #     'ShippingMethod' => array('className' => 'ShippingMethod', 'conditions' => '', 'order' => '', 'dependent' =>  false, 'foreignKey'   => 'shipping_method_id', 'fields' => '')
    # )));
    rs = EngageboostShippingMastersSettings.objects.filter(website_id=website_id)
    # shipping_methods_website = this->ShippingSetting->find("all",array('conditions'=>conditions,'order'=>'ShippingMethod.id asc'));
    shipping_methods_website = shippingObj.order_by("id").all().values()
    # this->pr_exit(shipping_methods_website);
    if website_id:
        globalsettingsObj = EngageboostGlobalSettings.objects.filter(website_id=website_id,isblocked='n',isdeleted='n')
        findWeightUnit = globalsettingsObj.values('weight_unit','is_global_shipping_app','shipping_charge','min_order_amount').first()

        weightUnit    = findWeightUnit['weight_unit']
        global_shipping   = findWeightUnit['is_global_shipping_app']
        global_shipping_amount = findWeightUnit['shipping_charge']
        min_order_amount   = findWeightUnit['min_order_amount']

    for k in shipping_methods_website.keys():
        v = shipping_methods_website[k]
        if v['shipping_method_id'] == 6:
            free_shipping_min_amount = v['minimum_order_amount']

        if v['shipping_method_id'] == 4:
            flat_rate = v['flat_price']

    if order_amt > min_order_amount:
        if order_amt >= free_shipping_min_amount:
            shipping_price = 0
            shipping_method = "Free Shipping"
            shipping_message = "As your order is above Rs. "+round(free_shipping_min_amount,2)+" you will not be charged any shipping fees."
        else:
            shipping_price = flat_rate
            shipping_method = "Flat Rate"
            shipping_message="As your order is under Rs. "+round(free_shipping_min_amount,2)+", a nominal shipping fee has been charged.To save Rs. "+number_format(flat_rate,2)+" of Delivery charges, please add items worth Rs. "+round((float(free_shipping_min_amount)-float(order_amt)),2)+ " or more and qualify for free home delivery."
    else:
        shipping_message  = "min order should be " +min_order_amount
        shipping_price = flat_rate
        shipping_method = "Flat Rate"

    data = {}
    data['shipping_cost']=shipping_price
    data['shipping_method_id']=shipping_method
    data['min_order_amount']=min_order_amount
    data['free_shipping_min_amount']=free_shipping_min_amount
    data['shipping_message']=shipping_message
    data['order_amount']=order_amt
    return data


def update_order_and_order_products(order_id, return_order_type='GRN Cancellation'):
    if order_id > 0:
        rs_oder = EngageboostOrdermaster.objects.filter(id=order_id).first()
        order_data = OrderAndOrderProductSerializer(rs_oder)
        all_OrderProduct = order_data.data
        net_amount      = 0
        gross_amount    = 0
        tax_amount      = 0
        gross_discount_amount = 0
        cart_discount  	= rs_oder.cart_discount
        shipping_cost 	= rs_oder.shipping_cost
        pay_wallet_amount = rs_oder.pay_wallet_amount
        for products in all_OrderProduct['order_products']:
            quantity = products['quantity']
            if products['grn_quantity'] and int(products['grn_quantity']) > 0:
                quantity = int(products['grn_quantity'])
            else:
                quantity = int(products['quantity'])-(int(products['deleted_quantity'])+int(products['returns'])+int(products['shortage']))
            net_amount = float(net_amount) + (float(products['product_price'])*float(quantity))
            tax_amount = float(tax_amount) + (float(products['product_tax_price'])*int(quantity))
            gross_discount_amount = float(gross_discount_amount) + (float(products['product_discount_price'])*int(quantity))
        if rs_oder.applied_coupon and cart_discount > 0:
            # cart_discount = grn_cart_discount(OrderData['applied_coupon'], all_OrderProduct, return_order_type, website_id,OrderData['customer_id'])
            cart_discount = rs_oder.cart_discount
        else:
            cart_discount = rs_oder.cart_discount
        gross_amount = float(net_amount)+float(tax_amount)+float(shipping_cost)-float(cart_discount)
        # Wallet balance update start...
        if gross_amount>pay_wallet_amount:
            gross_amount = float(gross_amount-pay_wallet_amount)
        else:
            refund_wallet= float(pay_wallet_amount-gross_amount)
            # common.addCustomerLoyaltypoints()
            pay_wallet_amount = gross_amount
        # Wallet balance update end..

        # # end Shipping cost calculation for return product...
        shipped_save_order = {}
        shipped_save_order = {
            "net_amount":net_amount,
            "net_amount_base":net_amount,
            "tax_amount":tax_amount,
            "gross_amount":gross_amount,
            "gross_amount_base":gross_amount,
            "cart_discount":cart_discount,
            "gross_discount_amount":gross_discount_amount,
            "gross_discount_amount_base":gross_discount_amount,
            "pay_wallet_amount":pay_wallet_amount
        }
        EngageboostOrdermaster.objects.filter(id=order_id).update(**shipped_save_order)
        common.save_data_to_elastic(order_id,'EngageboostOrdermaster')

def grn_cart_discount(coupon_code, order_products, fromdata='GRN Cancellation', website_id=None,customer_id=None, custom_order_id=None,points_disc=None):
    website_id = 1
    cartSubTotal = 0
    # #this->pr(order_products);
    cartdetails = {}
    # for(order_products as key => domain_cookie_product) {
    for key in domain_cookie_product.keys():
        order_products = domain_cookie_product[key]
        # #this->pr(domain_cookie_product)
        cartdetails[key] = {}
        cartdetails[key]['id'] = domain_cookie_product['OrderProduct']['product_id']
        cartdetails[key]['new_default_price'] = domain_cookie_product['OrderProduct']['product_price']
        cartdetails[key]['tax_price'] = domain_cookie_product['OrderProduct']['product_tax_price']

        if domain_cookie_product['OrderProduct']['grn_quantity'] > 0 or domain_cookie_product['OrderProduct']['instock_qty'] > 0:
            cartdetails[key]['qty'] = int(domain_cookie_product['OrderProduct']['grn_quantity']) + int(domain_cookie_product['OrderProduct']['instock_qty'])
        else:
            cartdetails[key]['qty'] = int(domain_cookie_product['OrderProduct']['quantity'])-int(domain_cookie_product['OrderProduct']['deleted_quantity'])-int(domain_cookie_product['OrderProduct']['shortage'])-int(domain_cookie_product['OrderProduct']['returns'])

    # this->Session->write('admin_cartdetails', cartdetails);
    discount_array = Discount.generate_discount_conditions_coupon(website_id, coupon_code)
    discount_amount_order_total = 0
    flag_return = "false"
    if discount_array :
        # cartSubTotal = order_total_exclude_kvi(discount_array[0]['DiscountMasterCondition'],  cartdetails)
        cartSubTotal = 10
        flag_return = Discount.genrate_new_prodcut_with_discount_coupon_order_total(cartdetails, discount_array, '', '', cartSubTotal, customer_id)
        # if(from == 'GRN Cancellation')
        # fromData === from
        fromData = ""
        if fromData == 'GRN Cancellation':

            if discount_array[0]['DiscountMaster']['disc_type']==6 :
                ## not need because flag true if  whole cart discount applicable and then  disc_type=3
                discount_amount_order_total = (cartSubTotal*(discount_array[0]['DiscountMaster']['amount']/100))
                if discount_array[0]['DiscountMaster']['up_to_discount'] and int(discount_amount_order_total) > int(discount_array[0]['DiscountMaster']['up_to_discount']):
                    discount_amount_order_total = discount_array[0]['DiscountMaster']['up_to_discount']
            else:
                discount_amount_order_total = discount_array[0]['DiscountMaster']['amount']

        else :
            if flag_return == False :
                discount_amount_order_total = 0
                  # #no statements ...
            else :
                if discount_array[0]['DiscountMaster']['disc_type']==6:
                    # # not need because flag true if  whole cart discount applicable and then  disc_type=3
                    discount_amount_order_total  = cartSubTotal*float(int(discount_array[0]['DiscountMaster']['amount'])/100)
                    if discount_array[0]['DiscountMaster']['up_to_discount'] and int(discount_amount_order_total) > int(discount_array[0]['DiscountMaster']['up_to_discount']):
                         discount_amount_order_total = discount_array[0]['DiscountMaster']['up_to_discount']
                else:
                    discount_amount_order_total = discount_array[0]['DiscountMaster']['amount']
    # this->Session->write('admin_cartdetails', '');
    return discount_amount_order_total
  
# update_order_and_order_products(20)
# update_order_refund(20,3, 1,1,'GRN Cancellation', 1)

class DeleteShipment(generics.ListAPIView):
    def post(self,request):
        company_db = loginview.db_active_connection(request)
        requestdata = request.data
        now_utc = datetime.now(timezone.utc).astimezone()
        shipment_id = requestdata['shipment_id']
        website_id = requestdata['website_id']
        userId = requestdata['userid']
        check_data_exist_or_not = EngageboostShipments.objects.using(company_db).filter(id=shipment_id)
        try:
            if check_data_exist_or_not.count()>0:
                shipment_orders = EngageboostShipmentOrders.objects.using(company_db).filter(shipment=shipment_id).all()
                shipment_orders_serializer = ShipmentsOrdersSerializer(shipment_orders,many=True)
                if shipment_orders_serializer and shipment_orders.count() > 0 :
                    for shipmentOrder in shipment_orders_serializer.data:
                        shipment_status = shipmentOrder["shipment_status"]
                        trent_picklist_id = shipmentOrder["trent_picklist_id"]
                        order_id = shipmentOrder["order"]['id']
                        if shipment_status == 'Picking' or shipment_status == 'Invoicing':
                            EngageboostOrdermaster.objects.filter(id=order_id, shipment_id=shipment_id).update(shipment_id=0, trent_picklist_id=0,sort_by_distance=0,order_status=0)
                            EngageboostShipmentOrders.objects.filter(order=order_id,shipment=shipment_id).update(isdeleted='y',isblocked='y')
                            EngageboostCrates.objects.filter(trent_picklist_id=trent_picklist_id, order_id=order_id).update(isdeleted='y',isblocked='y')
                            elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'shipping_status':'Pending','shipment_id':0,'trent_picklist_id':0,'sort_by_distance':0,'order_status':0})
                            activityType = 1
                            activity_details = common.save_order_activity(company_db,order_id,now_utc,7,"Order is removed from shipment.",userId,activityType)
                            # Delete Shipment and picklist
                            AllshipmentOrder = EngageboostShipmentOrders.objects.filter(shipment=shipment_id, isdeleted='n', isblocked='n').all()
                            if len(AllshipmentOrder)>0:
                                pass
                            else:
                                EngageboostTrentPicklists.objects.filter(id=trent_picklist_id).update(isdeleted='y',isblocked='y')
                                EngageboostShipments.objects.filter(id=shipment_id).update(isdeleted='y',isblocked='y')
                            # Delete Shipment and picklist
                            data = {
                                'status':1,
                                'api_status':'',
                                'shipment_id': shipment_id,
                                'message':'Shipment deleted Successfully',
                            }
                        else:
                            data = {
                                'status':0,
                                'api_status':'',
                                'shipment_id': shipment_id,
                                'message':"Shipment is is already packed, you can't removed from shipment."
                            }
                else:
                    data ={
                        'status':0,
                        'api_status':'',
                        'shipment_id': shipment_id,
                        'message':'Data Not Found',
                    }
            else:
                data ={
                    'status':0,
                    'api_status':'',
                    'shipment_id': shipment_id,
                    'message':'Data Not Found',
                }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

class DeletePicklist(generics.ListAPIView):
    def post(self,request):
        company_db = loginview.db_active_connection(request)
        requestdata = request.data
        now_utc = datetime.now(timezone.utc).astimezone()
        trent_picklist_id = requestdata['picklist_id']
        website_id = requestdata['website_id']
        userId = requestdata['userid']
        check_data_exist_or_not = EngageboostTrentPicklists.objects.using(company_db).filter(id=trent_picklist_id)
        try:
            if check_data_exist_or_not.count()>0 and trent_picklist_id > 0:
                shipment_orders = EngageboostShipmentOrders.objects.using(company_db).filter(trent_picklist_id=trent_picklist_id).all()
                shipment_orders_serializer = ShipmentsOrdersSerializer(shipment_orders,many=True)
                if shipment_orders_serializer and shipment_orders.count() > 0 :
                    for shipmentOrder in shipment_orders_serializer.data:
                        shipment_status = shipmentOrder["shipment_status"]
                        order_id = shipmentOrder["order"]['id']
                        if order_id > 0 and shipment_status == 'Created' or shipment_status == 'Picking':
                            EngageboostOrdermaster.objects.filter(id=order_id,trent_picklist_id=trent_picklist_id).update(trent_picklist_id=0,order_status=0)
                            EngageboostShipmentOrders.objects.filter(order=order_id,trent_picklist_id=trent_picklist_id).update(isdeleted='y',isblocked='y')
                            EngageboostCrates.objects.filter(trent_picklist_id=trent_picklist_id, order_id=order_id).update(isdeleted='y',isblocked='y')
                            elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'order_status':'0','shipping_status':'Pending'})
                            activityType = 1
                            activity_details = common.save_order_activity(company_db,order_id,now_utc,7,"Order is removed from picklist.",userId,activityType)
                            EngageboostTrentPicklists.objects.filter(id=trent_picklist_id).update(isdeleted='y',isblocked='y')
                            data = {
                                'status':1,
                                'api_status':'',
                                'shipment_id': trent_picklist_id,
                                'message':'Picklist deleted Successfully',
                            }
                        else:
                            data = {
                                'status':0,
                                'api_status':'',
                                'shipment_id': trent_picklist_id,
                                'message':"GRN is already completed, you can't delete this picklist."
                            }
                else:
                    data ={
                        'status':0,
                        'api_status':'',
                        'shipment_id': trent_picklist_id,
                        'message':'Data Not Found',
                    }
            else:
                data ={
                    'status':0,
                    'api_status':'',
                    'shipment_id': trent_picklist_id,
                    'message':'Data Not Found',
                }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

class PicklistPrint(generics.ListAPIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        now_utc = datetime.now(timezone.utc).astimezone()
        try:
            website_id=request.data["website_id"]
            company_id=request.data["company_id"]
            trent_picklist_id = request.data["trent_picklist_id"]
            picklist_id       = trent_picklist_id
            picklist_content = ''
            webshop_id = 0
            product_ids_qty     = {}
            picklist_details_dict = {}
            picklist_order_ids_arr  = []
            existingprdlist         = []
            order_product_id_arr    = []
            exist_picklist  = EngageboostTrentPicklists.objects.using(company_db).filter(id=trent_picklist_id).first()
            if int(trent_picklist_id) > 0 and exist_picklist is not None:
                picklist_created_date   = exist_picklist.created
                picklist_id             =  exist_picklist.id
                warehouse_id            =  exist_picklist.warehouse_id
                trents_picklist_no  	= exist_picklist.trents_picklist_no

                picklist_id = exist_picklist.id
                custom_picklist_id  = exist_picklist.trents_picklist_no
                picklist_data_serializer = TrentPicklistsSerializer(exist_picklist)
                # print(picklist_data_serializer.data)
                warehouseDetails = EngageboostWarehouseMasters.objects.using(company_db).filter(id=exist_picklist.warehouse_id).first()
                warehouse_name = warehouseDetails.name
                shipmentOrders = EngageboostOrdermaster.objects.using(company_db).filter(trent_picklist_id=picklist_id).all()
                if shipmentOrders:
                    shipmentOrders_Serializer = OrderMasterSerializer(shipmentOrders,many=True)
                    for shipment_Orders in shipmentOrders_Serializer.data:
                        picklist_order_ids_arr.append(shipment_Orders["custom_order_id"])
                        webshop_id = shipment_Orders["webshop_id"]
                    if picklist_order_ids_arr:
                        picklist_order_ids = ",".join(picklist_order_ids_arr)
                    else:
                        picklist_order_ids = ""
                else:
                    picklist_order_ids = ""
                # print(picklist_data_serializer.data)
                for shipmentOrderItem in picklist_data_serializer.data["trents_picklist_products"]:
                    quantity = shipmentOrderItem["qty"]
                    product_id = shipmentOrderItem["product_id"]
                    productDetails = EngageboostProducts.objects.using(company_db).filter(id=product_id).first()
                    productDetails_serializer = EngageboostProductsUomSerializer(productDetails)
                    productDetails_serializer = productDetails_serializer.data
                    if product_id in existingprdlist:
                        for index,item in enumerate(existingprdlist):
                            if item == product_id:
                                order_product_id_arr[index]={"id":product_id,"qty":int(order_product_id_arr[index]["qty"])+int(quantity),"product_name" :productDetails.name,"sku" :productDetails.sku,"ean" :productDetails.ean,"uom" :productDetails_serializer['unit_name'],"picklist_id":picklist_id,"product_image":product_image,"variant":"", "unit_name":productDetails_serializer['unit_name']}
                    else:
                        existingprdlist.append(product_id)
                        product_ids_qty = {"id":product_id,"qty":quantity ,"product_name" :productDetails.name,"sku" :productDetails.sku,"ean" :productDetails.ean,"uom" :productDetails_serializer['unit_name'],"picklist_id":picklist_id,"variant":"", "unit_name":productDetails_serializer['unit_name']}
                        order_product_id_arr.append(product_ids_qty)

                picklist_details_dict = {
                    "picklist_id":picklist_id,
                    "trents_picklist_no":trents_picklist_no,
                    "picklist_created_date":picklist_created_date,
                    'picklist_order_ids':picklist_order_ids,
                    "warehouse_name":warehouse_name,
                    "warehouse_id":warehouse_id,
                }

            # print(invoice_master.data)
            buffer_data = common.getAutoResponder(company_db,"Picking",webshop_id,warehouse_id,'',website_id,9)
            autoResponderData  = buffer_data["content"]
            # print(autoResponderData)
            if autoResponderData["email_type"] == 'T':
                emailContent = autoResponderData["email_content_text"]
            else:
                emailContent = autoResponderData["email_content"]
            emailContent = str(emailContent)

            productBoxInfo = createProductBoxPicklist(order_product_id_arr)
            picklist_details_dict["PRODUCT_BOX"] = productBoxInfo
            # print(picklist_details_dict)
            for orderKey, orderval in picklist_details_dict.items():
                replacingKey = '{@'+str(orderKey)+'}'
                emailContent = emailContent.replace(str(replacingKey),str(orderval if orderval else ''))
            picklist_content+=emailContent
            data = {"status":1,"api_status":1, "message": "Printing picklist details","picklist_content":picklist_content}
            # print(data);
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

def createProductBoxPicklist(pickListItems):
    total_str=""
    table_str='<table width="100%" border="0" cellspacing="0" cellpadding="0">'
    table_str+='<tr>'
    table_str+='<td align="left" style="background-color:#e1e1e1; padding:5px; padding-left:10px; border-top:1px solid #414141;font-size:10pt; border-right:1px solid #414141; border-bottom:1px solid #414141;" valign="top"><strong>S.No</strong></td>'
    table_str+='<td align="left" style="background-color:#e1e1e1; padding:5px; padding-left:10px; border-top:1px solid #414141;font-size:10pt; border-right:1px solid #414141; border-bottom:1px solid #414141;" valign="top"><strong>Title</strong></td>'
    table_str+='<td align="center" style="background-color:#e1e1e1; padding:5px; border-top:1px solid #414141;font-size:10pt; border-right:1px solid #414141; border-bottom:1px solid #414141;" valign="top"><strong>Product SKU</strong></td>'
    table_str+='<td align="center" style="background-color:#e1e1e1; padding:5px; border-top:1px solid #414141;font-size:10pt; border-right:1px solid #414141; border-bottom:1px solid #414141;width:17%;" valign="top"><strong>EAN</strong></td>'
    table_str+='<td align="left" style="background-color:#e1e1e1; padding:5px; padding-left:10px; border-top:1px solid #414141;font-size:10pt; border-right:1px solid #414141; border-bottom:1px solid #414141;" valign="top"><strong>UOM</strong></td>'
    table_str+='<td align="center" style="background-color:#e1e1e1; padding:5px; border-top:1px solid #414141;font-size:10pt; border-bottom:1px solid #414141;width:17%;" valign="top"><strong>Variant</strong></td>'
    table_str+='<td align="center" style="background-color:#e1e1e1; padding:5px; border-top:1px solid #414141;font-size:10pt; border-bottom:1px solid #414141;width:17%;" valign="top"><strong>Quantity</strong></td>'
    table_str+='</tr>'
    total_str=total_str+""+table_str
    total_weight = 0
    count = 1
    total_qty = 0
    # print(json.dumps(pickListItems))
    for pickListItem in pickListItems:
        total_str+= '<tr  style="text-transform:none;">'
        total_str+= '<td width="0" align="left" style="font-size:10pt; text-align:center; border-right:1px solid #414141; border-bottom:1px solid #414141; padding:5px; padding-left:10px;" valign="top">'+str(count)+'</td>'
        total_str+= '<td width="0" align="left" style="font-size:10pt; text-align:center; border-right:1px solid #414141; border-bottom:1px solid #414141; padding:5px; padding-left:10px;" valign="top">'+pickListItem['product_name']+'</td>'
        total_str+= '<td width="0" align="left" style="font-size:10pt; text-align:center; border-right:1px solid #414141; border-bottom:1px solid #414141; padding:5px; padding-left:10px;" valign="top">'+str(pickListItem['sku'])+'</td>'
        total_str+= '<td width="0" align="left" style="font-size:10pt; text-align:center; border-right:1px solid #414141; border-bottom:1px solid #414141; padding:5px; padding-left:10px;" valign="top">'+str(pickListItem['ean'])+'</td>'
        total_str+= '<td width="0" align="left" style="font-size:10pt; text-align:center; border-right:1px solid #414141; border-bottom:1px solid #414141; padding:5px; padding-left:10px;" valign="top">'+str(pickListItem['uom'])+'</td>'
        total_str+= '<td width="0" align="left" style="font-size:10pt; text-align:center; border-right:1px solid #414141; border-bottom:1px solid #414141; padding:5px; padding-left:10px;" valign="top">'+str(pickListItem['variant'])+'</td>'
        total_str+= '<td width="0" align="left" style="font-size:10pt; text-align:center; border-right:1px solid #414141; border-bottom:1px solid #414141; padding:5px; padding-left:10px;" valign="top">'+str(pickListItem['qty'])+'</td>'
        total_str+="</tr>"
        count=count+1
    total_str+="</table>"
    return total_str

def formatNumber(number):
    return ("{:,.2f}".format(number))

def test_dist(shipment_id):
    print(shipment_id)
    #result = file_get_contents("https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=22.5135,88.4019&destinations=22.5135,88.4019|22.5791,88.3943|22.5981,88.3708|22.603,88.404|22.603,88.404&key=AIzaSyBaTj-wuRYF1YuAHvj8UV5JhDMc_y5f9-g&travelMode=DRIVING&waypoints=optimize:true&sensor=true")
    #result = json_decode(result,true)

    # Working fine
    GOOGLE_MAPS_API_URL = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=22.5135,88.4019&destinations=22.5135,88.4019|22.5791,88.3943|22.5981,88.3708|22.603,88.404|22.603,88.404&key=AIzaSyBaTj-wuRYF1YuAHvj8UV5JhDMc_y5f9-g&travelMode=DRIVING&waypoints=optimize:true&sensor=true"

    #GOOGLE_MAPS_API_URL = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='22.5135,88.4019'&destinations='22.642626,88.438649|22.642626,88.438649|22.5981,88.3708|22.603,88.404'&key=AIzaSyBaTj-wuRYF1YuAHvj8UV5JhDMc_y5f9-g&travelMode=DRIVING&waypoints=optimize:true&sensor=false"
    result = requests.get(GOOGLE_MAPS_API_URL)
    result = result.json()
    print(result)

class getGrnProductsInfo(generics.ListAPIView):
    def post(self,request):
        requestdata         = request.data
        trent_picklist_id   = requestdata['trent_picklist_id']
        order_id            = requestdata['order_id']
        website_id          = requestdata['website_id']
        product_id 			= request.data['product_id']
        try:
            order_product_data = EngageboostShipmentOrderProducts.objects.filter(order_id=order_id,product_id=product_id,trent_picklist_id=trent_picklist_id).first()
            order_product = EngageboostShipmentOrderProductsPicklistSerializer(order_product_data, partial=True)
            if order_product and product_id > 0:
                # substitute product
                all_data_related_cond = EngageboostRelatedProducts.objects.filter(product_id=product_id,related_product_type = '5').all()
                all_data_related = RelatedProductsSerializer(all_data_related_cond,many=True)
                orderproducts = EngageboostOrderProducts.objects.filter(order_id=order_id)
                orderproducts_arr = []
                if orderproducts.count()>0:
                    orderproducts_arr = orderproducts.values_list("product_id",flat=True)

                # end substitute product
                data = {
                    "status":1,
                    "api_status": order_product.data,
                    "substitute_product": all_data_related.data,
                    "order_products":orderproducts_arr,
                    "message": ''
                }
            else:
                data = {
                    'status':0,
                    'api_status':'',
                    'message':'Data Not Found',
                }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

class saveEditGRN(generics.ListAPIView):
    def post(self,request):
        company_db             = loginview.db_active_connection(request)
        requestdata 		   = request.data
        order_id               = requestdata['order_id']
        logged_user_id         = requestdata['userId']
        trent_picklist_id      = requestdata['trent_picklist_id']
        product_id             = requestdata['product_id']
        old_grn_quantity       = requestdata['old_grn_quantity']
        grn_quantity           = requestdata['grn_quantity']
        shortage               = requestdata['shortage']
        try:
            total_quantity = 0
            if old_grn_quantity != grn_quantity:
                update_shipment_order_product = {}
                update_shipment_order_product = {
                    "shortage":shortage,
                    "grn_quantity":grn_quantity
                }
                EngageboostShipmentOrderProducts.objects.filter(trent_picklist_id=trent_picklist_id, order=order_id, product=product_id).update(**update_shipment_order_product)
                EngageboostOrderProducts.objects.filter(order=order_id, product=product_id).update(**update_shipment_order_product)
                # need to update order net_amount and gross amount, and total_quantity in EngageboostShipmentOrders.
                order_data = EngageboostOrdermaster.objects.filter(id=order_id, trent_picklist_id=trent_picklist_id).first()
                OrderProduct = EngageboostOrderProducts.objects.filter(order_id=order_id).all()
                if OrderProduct:
                    order_prod_data_serializer = OrderProductsSerializer(OrderProduct,many=True)
                    tax_amount = 0
                    net_amount = 0
                    shipping_cost = float(order_data.shipping_cost)
                    cod_charge = float(order_data.cod_charge)
                    cart_discount = float(order_data.cart_discount)
                    pay_wallet_amount = float(order_data.pay_wallet_amount)
                    if order_prod_data_serializer.data:
                        for OrderProducts in order_prod_data_serializer.data:
                            grn_quantity = int(OrderProducts['grn_quantity'])
                            tax_amount = tax_amount + (OrderProducts['product_tax_price']*grn_quantity)
                            net_amount = net_amount + ((OrderProducts['product_price']+OrderProducts['product_tax_price'])*grn_quantity)
                            total_quantity = total_quantity+grn_quantity
                    gross_amount = float(net_amount)+float(tax_amount)+shipping_cost+cod_charge-cart_discount
                    # Wallet balance update start...
                    if gross_amount>pay_wallet_amount:
                        gross_amount = float(gross_amount-pay_wallet_amount)
                    else:
                        refund_wallet= float(pay_wallet_amount-gross_amount)
                        # common.addCustomerLoyaltypoints()
                        pay_wallet_amount = gross_amount
                    # Wallet balance update end..
                    order_update_arr = {
                        'tax_amount':tax_amount,
                        'net_amount':net_amount,
                        'net_amount_base':net_amount,
                        'gross_amount':gross_amount,
                        'gross_amount_base':gross_amount,
                        'pay_wallet_amount':pay_wallet_amount
                    }
                    EngageboostOrdermaster.objects.filter(id=order_id,trent_picklist_id=trent_picklist_id).update(**order_update_arr)
                EngageboostShipmentOrders.objects.filter(id=order_id).update(total_quantity=total_quantity)
                # Elastic data update...
                common.save_data_to_elastic(order_id,'EngageboostOrdermaster')
                # Elastic data update...
                # ** order activity....
                common.save_order_activity(company_db,order_id,None,7,"Order edited in grn.", 1, logged_user_id)
            # ** grn created date update...
            data = {
                "status":1,
                "api_status" : 'success',
                "message":"GRN edited successfully.."
            }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

class saveEditPrice(generics.ListAPIView):
    def post(self,request):
        company_db             = loginview.db_active_connection(request)
        requestdata            = request.data
        website_id             = requestdata['website_id']
        order_id               = requestdata['order_id']
        logged_user_id         = requestdata['userId']
        employee_name 		   = requestdata['employee_name']
        trent_picklist_id      = requestdata['trent_picklist_id']
        product_id             = requestdata['product_id']
        old_product_price      = requestdata['old_product_price']
        product_price   	   = requestdata['product_price']
        weight   	   		   = requestdata['weight']
        notes                  = requestdata['notes']
        now_utc = datetime.now(timezone.utc).astimezone()
        try:
            product_price = float(product_price)
            old_product_price = float(old_product_price)
            if product_price > 0 and (product_price != old_product_price) :
                #$this->Update_Order_product_Discount_Shipping_grn($OrderProduct, $order_id, $order_product_id, $product_price, $website_id);
                order_activities_str = employee_name+'</b> has changed the price for product '+requestdata['sku']+' from '+str(old_product_price)+' to '+str(product_price)
                order_activities_str+= '<br/>'+ notes
                # for grn price change...
                # need to update order net_amount and gross amount in order master table...
                update_price = {
                    "product_price":product_price,
                    "weight":weight
                }
                EngageboostOrderProducts.objects.filter(order_id=order_id, product_id=product_id).update(**update_price)
                order_data = EngageboostOrdermaster.objects.filter(id=order_id, trent_picklist_id=trent_picklist_id).first()
                cart_discount = float(order_data.cart_discount)
                tax_amount = 0
                net_amount = 0
                shipping_cost = float(order_data.shipping_cost)
                pay_wallet_amount = float(order_data.pay_wallet_amount)
                if order_data.cod_charge:
                    cod_charge = float(order_data.cod_charge)
                else:
                    cod_charge = 0.00
                uom_name = ''
                OrderProduct = EngageboostOrderProducts.objects.filter(order_id=order_id).all()
                if OrderProduct:
                    order_prod_data_serializer = OrderProductsSerializer(OrderProduct,many=True)
                    for OrderProducts in order_prod_data_serializer.data:
                        if (product_id == OrderProducts['product']['id']) and weight and OrderProducts['product']['uom']:
                            uom_name = OrderProducts['product']['uom']['uom_name']
                            uom_name = str(OrderProducts['weight']) + ' '+ uom_name

                        deleted_quantity = OrderProducts['deleted_quantity']
                        if OrderProducts['shortage']:
                            shortage = OrderProducts['shortage']
                        else:
                            shortage = 0
                        if OrderProducts['returns']:
                            returns = OrderProducts['returns']
                        else:
                            returns = 0
                        grn_quantity = int(OrderProducts['quantity'])-int(deleted_quantity)-int(shortage)-int(returns)
                        tax_amount = tax_amount + (OrderProducts['product_tax_price']*grn_quantity)
                        net_amount = net_amount + ((OrderProducts['product_price']+OrderProducts['product_tax_price'])*grn_quantity)

                    gross_amount = float(net_amount)+float(tax_amount)+shipping_cost+cod_charge-cart_discount;
                    # Wallet balance update start...
                    if gross_amount>pay_wallet_amount:
                        gross_amount = float(gross_amount-pay_wallet_amount)
                    else:
                        refund_wallet= float(pay_wallet_amount-gross_amount)
                        # common.addCustomerLoyaltypoints()
                        pay_wallet_amount = gross_amount
                    # Wallet balance update end..
                    order_update_arr = {
                        'tax_amount':tax_amount,
                        'net_amount':net_amount,
                        'net_amount_base':net_amount,
                        'gross_amount':gross_amount,
                        'gross_amount_base':gross_amount,
                        'pay_wallet_amount':pay_wallet_amount
                    }
                    EngageboostOrdermaster.objects.filter(id=order_id,trent_picklist_id=trent_picklist_id).update(**order_update_arr)
                    # Elastic data update...
                    common.save_data_to_elastic(order_id,'EngageboostOrdermaster')
                    return_data	= {
                        "product_price":float(product_price),
                        "uom_name":uom_name
                    }
                    # Elastic data update...
                order_price_changes = {
                    "order_id":order_id,
                    "product_id":product_id,
                    "old_product_price":old_product_price,
                    "new_product_price":product_price,
                    "notes":notes,
                    "user_id":logged_user_id,
                    "website_id":website_id,
                    "created":now_utc,
                    "modified":now_utc
                }
                EngageboostOrderPriceChange.objects.create(**order_price_changes)
                #print(order_price_changes)
                # ** order activity....
                common.save_order_activity(company_db,order_id,None,7,order_activities_str , 1, logged_user_id)
                # ** grn created date update...
                data = {
                    "status":1,
                    "api_status" : return_data,
                    "message":"Price changes successfully."
                }
            else:
                data = {
                    "status":0,
                    "api_status" : {},
                    "message":"Please enter correct price."
                }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

class saveSubstituteProduct(generics.ListAPIView):
    def post(self,request):
        company_db        = loginview.db_active_connection(request)
        requestdata       = request.data
        website_id        = requestdata['website_id']
        order_id          = requestdata['order_id']
        logged_user_id    = requestdata['userId']
        employee_name     = requestdata['employee_name']
        trent_picklist_id = requestdata['trent_picklist_id']
        shipment_id 	  = requestdata['shipment_id']
        shipment_order_id = requestdata['shipment_order_id']
        old_product_id    = requestdata['product_id']
        sub_product_id    = requestdata['sub_product_id']
        shortage      	  = int(requestdata['shortage'])
        now_utc 		  = datetime.now(timezone.utc).astimezone()
        try:
            order_product_id = 0
            if sub_product_id > 0 and shortage > 0 and sub_product_id > 0:
                order_product_data = EngageboostOrderProducts.objects.filter(order_id=order_id,product_id=old_product_id,trents_picklist_id=trent_picklist_id).first()
                sub_cart_data = Order.get_substitude_product_cart(website_id, sub_product_id, shortage, order_product_data.assign_wh )
                #print(json.dumps(sub_cart_data))
                new_default_price = 0
                if new_default_price in sub_cart_data and sub_cart_data['new_default_price'] > 0:
                    new_default_price = sub_cart_data['new_default_price']
                else :
                    new_default_price = sub_cart_data['default_price']

                discount_price = 0
                if discount_price in sub_cart_data and sub_cart_data['discount_price'] > 0:
                    discount_price = sub_cart_data['discount_price']

                coupon = ''
                disc_type = 0
                product_discount_rate = 0
                if coupon in sub_cart_data and sub_cart_data['coupon'] != '':
                    coupon = sub_cart_data['coupon']
                    disc_type = sub_cart_data['disc_type']
                    product_discount_rate = sub_cart_data['discount_amount']

                order_product_params = {
                    "order_id":order_id,
                    "product_id":sub_product_id,
                    "quantity":shortage,
                    "deleted_quantity":0,
                    "product_price":new_default_price,
                    "substitute_product_id":0,
                    "product_price_base":new_default_price,
                    "product_discount_price":discount_price,
                    "product_discount_price_base":discount_price,
                    "product_discount_name": coupon,
                    "product_disc_type": disc_type,
                    "product_discount_rate": product_discount_rate,
                    "status": 0,
                    "trents_picklist_id": trent_picklist_id,
                    "cost_price": new_default_price,
                    "mrp": new_default_price,
                    "assign_to": order_product_data.assign_to,
                    "assign_wh": order_product_data.assign_wh,
                    "warehouse_id": order_product_data.warehouse_id,
                    "weight":sub_cart_data['weight'],
                    "created":now_utc
                }
                #print(order_product_params)
                order_product_exist = EngageboostOrderProducts.objects.filter(order_id=order_id,product_id=sub_product_id).first()
                if order_product_exist and order_product_exist.id > 0:
                    order_product_id = order_product_exist.id
                else :
                    order_product = EngageboostOrderProducts.objects.create(**order_product_params)
                    order_product_id = order_product.id

                if order_product_id > 0:
                    shipment_order_product = {
                        "shipment_order_id" : shipment_order_id,
                        "shipment"			: shipment_id,
                        "order_id"			: order_id,
                        "product_id"		: sub_product_id,
                        "trent_picklist_id"	: trent_picklist_id,
                        "order_product_id"	: order_product_id,
                        "quantity"			: shortage,
                        "shortage"			: 0,
                        "returns"			: 0,
                        "grn_quantity"		: 0,
                        "shipment_status"	: 'Picking',
                        "warehouse_id"		: order_product_data.assign_wh
                    }
                    #print(shipment_order_product)
                    shipment_order_product_count = EngageboostShipmentOrderProducts.objects.filter(order_id=order_id, product_id=sub_product_id,trent_picklist_id=trent_picklist_id).count()
                    if shipment_order_product_count == 0:
                        EngageboostShipmentOrderProducts.objects.using(company_db).create(**shipment_order_product)

                    EngageboostShipmentOrderProducts.objects.filter(order=order_id, product=old_product_id,trent_picklist_id=trent_picklist_id).update(shortage=shortage)
                    EngageboostOrderProducts.objects.filter(order=order_id, product=old_product_id).update(shortage=shortage,substitute_product_id=sub_product_id)

                    pick_mrp = float(new_default_price)+float(discount_price)
                    product_tax_price = 0
                    tax_percentage = 0
                    tax_name = ''
                    sr_no = 0
                    total_quantity = shortage
                    trent_picklist_product = EngageboostTrentsPicklistProducts.objects.filter(product_id=sub_product_id,trent_picklist_id=trent_picklist_id).first()
                    if trent_picklist_product and trent_picklist_product.id > 0:
                        pass
                    else:
                        insert_arr = {
                            'sr_no': sr_no,
                            'trent_picklist_id':trent_picklist_id,
                            'product_id':sub_product_id,
                            'qty':total_quantity,
                            'confirm_quantity':total_quantity,
                            'stock_available':'y',
                            'pick_mrp':pick_mrp,
                            'product_tax_price':product_tax_price,
                            'tax_percentage':tax_percentage,
                            'tax_name':tax_name
                        }
                        EngageboostTrentsPicklistProducts.objects.create(**insert_arr)
                    stock_data = EngageboostProductStocks.objects.filter(warehouse_id=order_product_data.assign_wh,product_id=sub_product_id).first()
                    if stock_data and stock_data.id > 0:
                        virtual_stock = int(stock_data.virtual_stock)+shortage
                        real_stock = int(stock_data.real_stock)-shortage
                        update_stock = {
                            'virtual_stock':virtual_stock,
                            'real_stock':real_stock,
                        }
                        EngageboostProductStocks.objects.filter(warehouse_id=order_product_data.assign_wh,product_id=sub_product_id).update(**update_stock)
                    # Update order master data and elastic data...
                    update_order_and_order_products(order_id)
                    data = {
                        "status":1,
                        "api_status" : 'success',
                        "message":"Substitute product added successfully."
                    }
                else:
                    data = {
                        "status":0,
                        "api_status" : 'success',
                        "message":"Data not found."
                    }
            else:
                data = {
                    "status":0,
                    "api_status" : 'success',
                    "message":"Data not found."
                }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

#_______________Assign Vehicle_ Return______________#
class AssignVehicleReturn(generics.ListAPIView):
    def post(self,request):
        company_db = loginview.db_active_connection(request)
        postdata = request.data
        assignVehicleData = {}
        available_driver = []
        return_driver_id = 0
        return_delivery_date = ''
        try:
            website_id = postdata["website_id"] if postdata.get("website_id") else 1
            warehouse_id = postdata["warehouse_id"] if postdata.get("warehouse_id") else None
            order_id = postdata["order_id"] if postdata.get("order_id") else None
            shipment_id = postdata["shipment_id"] if postdata.get("shipment_id") else None

            if shipment_id and order_id > 0:
                order_data = EngageboostShipmentOrders.objects.using(company_db).filter(shipment=shipment_id,order=order_id).first()
                if order_data:
                    return_driver_id = order_data.return_driver_id
                    return_delivery_date = order_data.return_delivery_date

                alldeliveryManagerData = EngageboostDeliveryManagers.objects.using(company_db).filter(website_id=website_id,isblocked='n',isdeleted='n')
                if warehouse_id is not None:
                    alldeliveryManagerData = alldeliveryManagerData.filter(warehouse_ids__iregex=r"\y{0}\y".format(warehouse_id))
                alldeliveryManagerData = alldeliveryManagerData.all()

                if alldeliveryManagerData:
                    alldeliveryManager_Data = DeliveryManagersSerializer(alldeliveryManagerData,many=True)
                    for allDriver in alldeliveryManager_Data.data:
                        allDriverObj = {
                            "id": allDriver['id'],
                            "user_id": allDriver['user_id'],
                            "name" : allDriver['name']
                        }
                        available_driver.append(allDriverObj)

                assignVehicleData.update({
                    "available_driver":available_driver,
                    "return_driver_id" : return_driver_id,
                    "return_delivery_date":return_delivery_date
                })
            if assignVehicleData:
                data={"status":1,"api_status":assignVehicleData,"message":"Driver List"}
            else:
                data={"status":0,"api_status":assignVehicleData,"message":"No Driver list found"}
            return Response(data)
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message":str(error)}
            return Response(data)

class CreateAssignVehicleReturn(generics.ListAPIView):
    def post(self,request):
        company_db = loginview.db_active_connection(request)
        now_utc = datetime.now(timezone.utc).astimezone()
        postdata = request.data
        orderDataList = []
        try:
            shipment_id = postdata["shipment_id"]
            order_id = postdata["order_id"]
            return_delivery_date = postdata["return_delivery_date"] if postdata.get("return_delivery_date") else None
            return_delivery_date = datetime.strptime(return_delivery_date,'%Y-%m-%dT%H:%M:%S.%fZ')
            return_delivery_date = return_delivery_date.strftime("%Y-%m-%d")
            return_driver_id = postdata["return_driver_id"] if postdata.get("return_driver_id") else 0
            if shipment_id > 0 and return_driver_id > 0 and order_id > 0:
                EngageboostShipmentOrders.objects.using(company_db).filter(shipment=shipment_id,order=order_id).update(return_driver_id=return_driver_id,return_delivery_date = return_delivery_date)
                EngageboostOrdermaster.objects.filter(shipment_id=shipment_id,id=order_id).update(return_status="Driver Assigned")
                elastic = common.change_field_value_elastic(order_id,'EngageboostOrdermaster',{'return_status':"Driver Assigned"})
                # SMS to customer after order approval...
                common.sms_send_by_AutoResponder(order_id,None, 15)
                # SMS to customer after order approval...
                #********ORDER ACTIVITY********#
                # activityType = 1
                # activity_details = common.save_order_activity(company_db,order_id,now_utc,7,"Order is Ready to Ship",user_id,activityType)
                data={"status":1, "api_status":orderDataList, "message":"Assign Vehicle Successfully Completed."}
            else:
                data={"status":0, "api_status":orderDataList, "message":"Vehicle data not found."}
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message":str(error)}
        return Response(data)
