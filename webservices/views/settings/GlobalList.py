from webservices.models import *
from webservices.views.common.common import get_zonename,get_areaname,get_countryname, get_managername, get_statename, get_warehousename
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
import datetime
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
from django.db.models import Q,F
import ast
from django.db.models.functions import Cast
from django.db.models.functions import Concat
from webservices.views.common import common
from decimal import Decimal

class GlobalList(generics.ListAPIView):
    def get(self, request, pk, format=None):
        import urllib.parse
        company_db = loginview.db_active_connection(request)
        selection_fields = ["fix_select","select","multi_select"]
        try:
            labelResult = EngageboostAdvancedSearchLayouts.objects.filter(id=pk,isdeleted="n",isblocked="n")
            label = "name"
            value_field = "id"
            module = ""
            field = ""
            input_type = "text"
            key = request.GET.get('q')
            screen_name = request.data.get('screen_name')
            now 	= datetime.datetime.now()
            today 	= now.date()
            try:
                key = urllib.parse.unquote_plus(key)
            except:
                pass
            # print(key)
            if labelResult.count()>0:
                lables = labelResult.first()
                if lables.title_field_name!=None and lables.title_field_name!="":
                    label = lables.title_field_name
                module = lables.search_module
                module_id = lables.module_id
                field = lables.field
                input_type = lables.input_type
                if lables.value_field_name!=None and lables.value_field_name!="":
                    value_field = lables.value_field_name

            # print("Field==============",field,input_type,input_type in selection_fields)
            if field =="order_status" and input_type in selection_fields:
                result_set = [
                    {
                        "name": "Waiting Approval",
                        "id": 99
                    },
                    {
                        "name": "Pending",
                        "id": 0
                    },
                    {
                        "name": "Processing",
                        "id": 100
                    },
                    {
                        "name": "Shipped",
                        "id": 1
                    },
                    {
                        "name": "Cancelled",
                        "id": 2
                    },
                    {
                        "name": "Completed",
                        "id": 4
                    },
                    {
                        "name": "Full Refund",
                        "id": 5
                    },
                    {
                        "name": "Partial Refund",
                        "id": 6
                    },
                    {
                        "name": "Return Initiate",
                        "id": 7
                    },
                    {
                        "name": "Assigned to Showroom",
                        "id": 12
                    },
                    {
                        "name": "Delivered",
                        "id": 13
                    },
                    {
                        "name": "Closed",
                        "id": 16
                    },
                    {
                        "name": "Pending Service",
                        "id": 18
                    },
                    {
                        "name": "Hold",
                        "id": 9999
                    },
                    {
                        "name": "Abandoned",
                        "id": 3
                    },
                    {
                        "name": "Failed",
                        "id": 999
                    }
                ]
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="status" and input_type in selection_fields:
                if module_id == 14:
                    result_set = [
                        {
                            "name": "Draft",
                            "id": "Draft"
                        },
                        {
                            "name": "PO Sent",
                            "id": "PO Sent"
                        },
                        {
                            "name": "Shipped",
                            "id": "Shipped"
                        },
                        {
                            "name": "Cancel",
                            "id": "Cancel"
                        },
                        {
                            "name": "Received Partial",
                            "id": "Received Partial"
                        },
                        {
                            "name": "Grn Pending",
                            "id": "Grn Pending"
                        },
                        {
                            "name": "Received Full",
                            "id": "Received Full"
                        }
                    ]
                else:
                    result_set = [
                        {
                            "name": "Active",
                            "id": "n"
                        },
                        {
                            "name": "Inactive",
                            "id": "y"
                        }
                    ]
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="isblocked" and input_type in selection_fields:
                result_set = [
                    {
                        "name": "Active",
                        "id": "n"
                    },
                    {
                        "name": "Inactive",
                        "id": "y"
                    }
                ]
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="picklist_status" and input_type in selection_fields:
                result_set = [
                    {
                        "name": "Created",
                        "id": "Created"
                    },
                    {
                        "name": "Picking",
                        "id": "Picking"
                    },
                    {
                        "name": "Invoicing",
                        "id": "Invoicing"
                    },
                    {
                        "name": "Create Shipment",
                        "id": "Create Shipment"
                    }
                ]
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="return_status" and input_type in selection_fields:
                result_set = [
                    {
                        "name": "Pending",
                        "id": "Pending"
                    },
                    {
                        "name": "Authorized",
                        "id": "Authorized"
                    },
                    {
                        "name": "Processing",
                        "id": "Processing"
                    },
                    {
                        "name": "Declined",
                        "id": "Declined"
                    }
                ]
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="coupon_type" and input_type in selection_fields:
                result_set = [
                    {
                        "name": "Single Use",
                        "id": 1
                    },
                    {
                        "name": "Multiple Use",
                        "id": 2
                    }
                ]
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="email_type" and input_type in selection_fields:
                result_set = [
                    {
                        "name": "HTML",
                        "id": "H"
                    },
                    {
                        "name": "TEXT",
                        "id": "T"
                    },
                    {
                        "name": "HTML&TEXT",
                        "id": "HT"
                    }
                ]
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="has_multiplecoupons" and input_type in selection_fields:
                result_set = [
                    {
                        "name": "Yes",
                        "id": "y"
                    },
                    {
                        "name": "No",
                        "id": "n"
                    }
                ]
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="loyal_type" and input_type in selection_fields:
                result_set = [
                    {
                        "name": "Earn",
                        "id": "earn"
                    },
                    {
                        "name": "Burn",
                        "id": "burn"
                    }
                ]
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="redeem_type" and input_type in selection_fields:
                result_set = [
                    {
                        "name": "Loyalty",
                        "id": "loyalty"
                    },
                    {
                        "name": "Order",
                        "id": "order"
                    }
                ]
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="redeem_amount_type" and input_type in selection_fields:
                result_set = [
                    {
                        "name": "Fixed",
                        "id": "fixed"
                    },
                    {
                        "name": "Percentage",
                        "id": "percentage"
                    }
                ]
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="visibility_id" and input_type in selection_fields:
                result_set = [
                    {
                        "name": "Catalog Search",
                        "id": "Catalog Search"
                    },
                    {
                        "name": "Not Visible..",
                        "id": "Not Visible.."
                    }
                ]
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="veg_nonveg_type" and input_type in selection_fields:
                result_set = [
                    {
                        "name": "Veg",
                        "id": "veg"
                    },
                    {
                        "name": "Non Veg",
                        "id": "nonveg"
                    }
                ]
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="time_slot" and input_type in selection_fields:
                result_set = []
                result = EngageboostOrdermaster.objects.using(company_db).exclude(slot_start_time__isnull=True).values('time_slot_id', 'slot_start_time', 'slot_end_time').distinct('time_slot_id', 'slot_start_time', 'slot_end_time').all()
                try:
                    if key!="" and key!=None:
                        result = result.filter(Q(time_slot_id__icontains=key)|Q(slot_start_time__icontains=key)|Q(slot_end_time__icontains=key))
                except:
                    pass
                # resultdata = OrderMasterSerializer(result,many=True)    # delivery_date_from =
                # print(result)
                timesslot = {}
                for times in result:
                    # timesslot = {}
                    # print(times['slot_start_time'])

                    try:
                        if ":" in times['slot_start_time']:
                            try:
                                start = datetime.datetime.strptime(times['slot_start_time'], "%H:%M")
                                start = datetime.datetime.strftime(start, "%I:%M %p")
                            except:
                                start = datetime.datetime.strptime(times['slot_start_time'], "%H:%M:%S")
                                start = datetime.datetime.strftime(start, "%I:%M %p")
                        else:
                            start = datetime.datetime.strptime(times['slot_start_time'], "%H")
                            start = datetime.datetime.strftime(start, "%I:%M %p")
                        if ":" in times['slot_end_time']:
                            try:
                                end = datetime.datetime.strptime(times['slot_end_time'], "%H:%M")
                                end = datetime.datetime.strftime(end, "%I:%M %p")
                            except:
                                end = datetime.datetime.strptime(times['slot_end_time'], "%H:%M:%S")
                                end = datetime.datetime.strftime(end, "%I:%M %p")
                        else:
                            end = datetime.datetime.strptime(times['slot_end_time'], "%H")
                            end = datetime.datetime.strftime(end, "%I:%M %p")
                        time_slot_id = str(start)+"-"+str(end)
                        time_slot_id = time_slot_id.lower()

                        time_slot_id1 = time_slot_id.lower()
                        time_slot_id1 = time_slot_id1.replace("-","")
                        time_slot_id1 = time_slot_id1.replace(":","")
                        time_slot_id1 = time_slot_id1.replace(" ","")

                        timesslot[time_slot_id1] = time_slot_id

                    except:
                        print("nothing")
                for tim in timesslot.keys():
                    result_set.append({"name":timesslot[tim],"id":tim})
                # print(result_set)
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="time_slot_id" and input_type in selection_fields:
                result_set = []
                result = EngageboostOrdermaster.objects.exclude(slot_start_time__isnull=True).values('time_slot_id', 'slot_start_time', 'slot_end_time').distinct('time_slot_id', 'slot_start_time', 'slot_end_time').all()
                try:
                    if key!="" and key!=None:
                        result = result.filter(Q(time_slot_id__icontains=key)|Q(slot_start_time__icontains=key)|Q(slot_end_time__icontains=key))
                except:
                    pass
                timesslot = {}
                for times in result:
                    result_set.append({"name":times['time_slot_id'],"id":times['time_slot_id']})
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="shipment_status" and input_type in selection_fields:
                result_set = []
                result = EngageboostShipments.objects.exclude(shipment_status__isnull=True).values('shipment_status').distinct('shipment_status').all()

                if len(result)>0:
                    for times in result:
                        result_set.append({"name":times['shipment_status'],"id":times['shipment_status']})
                    data = {"status":1,"results":[{"result":[result_set]}],"message": ""}
                else:
                    data = {"status":0,"results":"","message": "Data not Found"}

            elif field =="created__week_day" and input_type in selection_fields:
                result_set = [
                    {
                        "name": "Sunday",
                        "id": 1
                    },
                    {
                        "name": "Monday",
                        "id": 2
                    },
                    {
                        "name": "Tuesday",
                        "id": 3
                    },
                    {
                        "name": "Wednesday",
                        "id": 4
                    },
                    {
                        "name": "Thursday",
                        "id": 5
                    },
                    {
                        "name": "Friday",
                        "id": 6
                    },
                    {
                        "name": "Saturday",
                        "id": 7
                    }
                ]
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="view_type" and input_type in selection_fields:
                result_set = [
                    {
                        "name": "With Login",
                        "id": 1
                    },
                    {
                        "name": "Without Login",
                        "id": 0
                    }
                ]
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="apply" and input_type in selection_fields:
                result_set = [
                    {
                        "name": "Billing Address",
                        "id": "b"
                    },
                    {
                        "name": "Shipping Addres",
                        "id": "s"
                    }
                ]
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="shipping_type" and input_type in selection_fields:
                result_set = [
                    {
                        "name": "Shipping",
                        "id": "Shipping"
                    },
                    {
                        "name": "Courier",
                        "id": "Courier"
                    },
                    {
                        "name": "Marketplace",
                        "id": "Marketplace"
                    }
                ]
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="tax_type" and input_type in selection_fields:
                result_set = [
                    {
                        "name": "VAT",
                        "id": "VAT"
                    },
                    {
                        "name": "CST",
                        "id": "CST"
                    },
                    {
                        "name": "Excise Duty",
                        "id": "Excise Duty"
                    }
                ]
                data = {"status":1,"results":[{"result":[result_set]}],"message": ""}

            elif field =="customer.id" and input_type in selection_fields:
                customers_obj = EngageboostCustomers.objects.filter(isdeleted="n",isblocked="n")
                customers_obj = customers_obj.annotate(name=Concat('first_name', Value(' '), 'last_name')).order_by("name")
                try:
                    if key!="" and key!=None:
                        customers_obj = customers_obj.filter(name__icontains=key)
                except:
                    pass
                customers_list = []
                if customers_obj.count()>0:
                    customers = customers_obj.all().values()

                    for item in customers:
                        name = item["name"]
                        customers_dict = {"id":item["id"],"name":name}
                        customers_list.append(customers_dict)
                    data = {"status":1,"results":[{"result":[customers_list]}],"message": ""}
                else:
                    data = {"status":0,"results":"","message": "Data not Found"}

            elif field =="assign_to" and input_type in selection_fields:
                warehouse_manager_list=[]
                warehouse_manager_cond = EngageboostWarehouseManager.objects.using(company_db).filter(isdeleted="n",isblocked="n").all().distinct("manager_id")
                try:
                    if key!="" and key!=None:
                        warehouse_manager_cond = warehouse_manager_cond.filter(get_search_filter(self,'EngageboostWarehouseManager',key))
                except:
                    pass
                if warehouse_manager_cond:
                    warehouse_manager = WarehousemanagerSerializer(warehouse_manager_cond,many=True)
                    if warehouse_manager:
                        for warehousemanager in warehouse_manager.data:
                            if warehousemanager["manager"]:
                                name = warehousemanager["manager"]["username"]
                                warehouse_manager_dict = {"id":warehousemanager["manager"]["id"],"name":name}
                                warehouse_manager_list.append(warehouse_manager_dict)

                    data = {"status":1,"results":[{"result":[warehouse_manager_list]}],"message": ""}
                else:
                    data = {"status":0,"results":"","message": "Data not Found"}
            else:
                table_name = "Engageboost" + module
                model = apps.get_model('webservices',table_name)
                try:
                    result_obj = model.objects.using(company_db).filter(isdeleted='n',isblocked="n")
                except Exception as error:
                    result_obj = model.objects.using(company_db)

                if field == "zone_id":
                    result_obj = result_obj.filter(location_type='Z')
                elif field == "parent_id":
                    result_obj = result_obj.filter(parent_id=0)
                try:
                    if key!="" and key!=None:
                        result_obj = result_obj.filter(get_search_filter(self,table_name,key))
                except:
                    pass
                result_count = result_obj.count()
                if result_count>0:
                    try:
                        results = result_obj.values().distinct(label)
                    except Exception as error:
                        results = result_obj.values()
                    result_set = []
                    for item in results:
                        item_set = {}
                        name = ""
                        name = item[label]
                        item_id = item[value_field]
                        item_set = {
                            "name":name,
                            "id":item_id
                        }
                        result_set.append(item_set)
                    data = {"status":1,"results":[{"result":[result_set]}],"message": ""}
                else:
                    data = {"status":0,"results":"","message": "Data not Found"}
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status":0,"results":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        table_name=request.data.get('model')
        userid = request.data.get('userid')
        model = apps.get_model('webservices',table_name)
        module = table_name.replace("Engageboost", "")
        screen_name = request.data.get('screen_name')
        # print(table_name+' '+screen_name)
        website_id = request.data.get('website_id')

        try:
            if request.data.get('show_all'):
                show_all = request.data.get('show_all')
            else:
                show_all = 0
        except Exception as error:
            show_all = 0

        global_setting_date = EngageboostGlobalSettings.objects.using(company_db).get(website_id=1,isdeleted='n',isblocked='n')
        global_setting_zone = EngageboostTimezones.objects.using(company_db).get(id = global_setting_date.timezone_id)

        if screen_name in ('list_zone', 'list_area', 'list_subarea'):
            serializer_class = get_zoneserializers(screen_name)
        else:
            serializer_class = get_serializer_class(self,table_name)
        #####################Query Generation#################################
        if request.data.get('search') and request.data.get('order_by'):
            key=request.data.get('search')
            key = key.strip()
            order_by=request.data.get('order_by')
            order_type=request.data.get('order_type')
            if(order_type=='+'):
                order = order_by
            else:
                order = '-'+order_by
            result = model.objects.using(company_db).all().order_by(order).filter(get_search_filter(self,table_name,key))
        elif request.data.get('search'):
            key = request.data.get('search')
            result = model.objects.using(company_db).all().order_by('-id').filter(get_search_filter(self,table_name,key))
        elif request.data.get('order_by'):
            order_by=request.data.get('order_by')
            order_type=request.data.get('order_type')
            if(order_type=='+'):
                order = order_by
            else:
                order='-'+order_by
            result = model.objects.using(company_db).order_by(order)
        elif request.data.get('location_type'):
            location_type = request.data.get('location_type')
            result = model.objects.using(company_db).filter(location_type=location_type).order_by('-id')
        else:
            result = model.objects.using(company_db).all().order_by('-id')

        if request.data.get('advanced_search'):
            filter_arr = request.data.get('advanced_search')
            result = common.get_advanced_search_filter(table_name,filter_arr,result)
        # print(result.query)
        # Filter based on website id... website_id
        exclude_website_id = [
            'EngageboostPurchaseOrdersPaymentMethods','EngageboostCompanyWebsites','EngageboostCurrencyMasters',
            'EngageboostPurchaseOrdersShippingMethods','EngageboostLanguages','EngageboostPages','EngageboostTrentPicklists'
        ]
        if table_name not in exclude_website_id:
            result = result.filter(website_id=website_id)
        # print(result.query)
        # Print data after sort and search,,,
        if table_name == "EngageboostDeliverySlot":
            query_set = EngageboostDeliverySlot.objects.distinct('zone_id').values('zone_id').all()
            zone_datas = DeliverySlotSerializer(query_set,many=True)
            zone = []
            if zone_datas:
                for zone_data in zone_datas.data:
                    query_set = EngageboostDeliverySlot.objects.filter(zone_id=zone_data['zone_id']).distinct('zone_id','start_time','end_time').values('zone_id','start_time','end_time').all()
                    time_datas = DeliverySlotSerializer(query_set,many=True)
                    times = []
                    if time_datas:
                        for time_data in time_datas.data:
                            query_set = EngageboostDeliverySlot.objects.filter(zone_id=zone_data['zone_id'],start_time=time_data['start_time'],end_time=time_data['end_time']).order_by("day_id").all()
                            slot_datas = DeliverySlotSerializer(query_set,many=True)
                            slots = []
                            if slot_datas:
                                for slot_data in slot_datas.data:
                                    slots.append(
                                        {
                                            "id": slot_data['id'],
                                            "day_id": slot_data['day_id'],
                                            "cutoff_start": slot_data['cutoff_start'],
                                            "cutoff_end": slot_data['cutoff_end'],
                                            "order_qty_per_slot": slot_data['order_qty_per_slot'],
                                            "based_on": slot_data['based_on'],
                                            "isblocked": slot_data['isblocked'],
                                            "created": slot_data['created'],
                                            "modified": slot_data['modified'],
                                            "action": "<div class=\"action\"></div>"
                                        }
                                    )
                            times.append(
                                {
                                    "start_time": time_data['start_time'],
                                    "end_time": time_data['end_time'],
                                    "slots":slots
                                }
                            )
                    zone.append({"zone_id":zone_data['zone_id'],"times":times})
                # print(zone)
                context_data={
                    'status':1,
                    'api_status':zone,
                    'message':'',
                }
            else:
                context_data={
                    'status':0,
                    'message':'No record found',
                }
            # print(delivery_slot_data)
            return Response(context_data)
            result = result.filter(isdeleted='n')

        elif table_name=='EngageboostDiscountMasters' and screen_name=='list1':
            result=result.filter(discount_master_type='1')

        elif table_name=='EngageboostDiscountMasters' and screen_name=='list2':
            result=result.filter(discount_master_type='0')

        elif table_name=='EngageboostShippingMastersSettings':
            result=result.filter(shipping_method_id=request.data.get('shipping_method_id'))

        elif table_name == 'EngageboostZoneMasters' and screen_name == 'list':
            result = model.objects.using(company_db).filter(location_type='Z', isdeleted='n', website_id=website_id).order_by('-id')

        elif table_name == 'EngageboostZoneMasters' and screen_name == 'list_zone':
            result = model.objects.using(company_db).filter(location_type='Z', isdeleted='n', website_id=website_id).order_by('-id')

        elif table_name == 'EngageboostZoneMasters' and screen_name == 'list_area':
            result = model.objects.using(company_db).filter(location_type='A', isdeleted='n',  website_id=website_id).order_by('-id')

        elif table_name == 'EngageboostZoneMasters' and screen_name == 'list_subarea':
            result = model.objects.using(company_db).filter(location_type='S', isdeleted='n',  website_id=website_id).order_by('-id')

        elif table_name == 'EngageboostVehicleMasters':
            result = result.filter(isdeleted='n', website_id=website_id)
            if request.data.get('warehouse_id'):
                warehouse_id = int(request.data.get('warehouse_id'))
                if warehouse_id > 0:
                    result = result.filter(warehouse_ids__iregex=r"\y{0}\y".format(warehouse_id))

        elif table_name == 'EngageboostCreditPoint' and screen_name=='list_earn':
            result = result.filter(isdeleted='n', website_id=website_id,loyal_type='earn')

        elif table_name=='EngageboostCreditPoint' and screen_name=='list_burn':
            result = result.filter(isdeleted='n', website_id=website_id,loyal_type='burn')

        elif table_name == 'EngageboostDeliveryManagers':
            result = result.filter(isdeleted='n', website_id=website_id)
            if request.data.get('warehouse_id'):
                warehouse_id = int(request.data.get('warehouse_id'))
                if warehouse_id > 0:
                    result = result.filter(warehouse_ids__iregex=r"\y{0}\y".format(warehouse_id))

        elif table_name == 'EngageboostPriceFormula':
            result = result.filter(isdeleted='n', website_id=website_id)

        elif table_name=='EngageboostPages':
            if website_id == 1:
                result=result.filter(company_website_id=website_id,isdeleted='n')
            else:
                result=result.filter(company_website_id=website_id,isdeleted='n')

        elif table_name=='EngageboostCategoryMasters':
            if request.data.get('warehouse_id'):
                warehouse_id = request.data.get('warehouse_id')
                categories = EngageboostCategoryWarehouse.objects.filter(warehouse_id=warehouse_id)
                categories = categories.values('category_id')
                result = result.filter(id__in=categories)

        elif table_name=='EngageboostWarehouseMasters':
            if request.data.get('warehouse_id'):
                warehouse_id = int(request.data.get('warehouse_id'))
                if warehouse_id > 0:
                    result = result.filter(id=warehouse_id)

        elif table_name =='EngageboostTrentPicklists' and screen_name=='list':
            if request.data.get('picklist_status'):
                list_of_order_status = request.data.get('picklist_status').split(",")
                order_status_field_value=[]
                for values in list_of_order_status:
                    order_status_field_value.append(values)
                result=result.filter(picklist_status__in=order_status_field_value)

            if request.data.get('warehouse_id'):
                list_of_warehouse_id = request.data.get('warehouse_id').split(",")
                warehouse_id_field_value=[]
                for values in list_of_warehouse_id:
                    warehouse_id_field_value.append(values)
                result=result.filter(warehouse_id__in=warehouse_id_field_value)

            if request.data.get('manager_warehouse_id'):
                manager_warehouse_id = request.data.get('manager_warehouse_id');
                if manager_warehouse_id != '':
                    result=result.filter(warehouse_id=manager_warehouse_id)

            if request.data.get('date'):
                date = request.data.get('date').split("##")
                start_date = date[0]
                end_date = date[1]
                if start_date == 'null' and end_date == 'null':
                    pass
                else:
                    result=result.filter(created__range=[start_date,end_date])

        elif table_name =='EngageboostShipments' and screen_name=='list':
            if request.data.get('shipment_status'):
                list_of_order_status = request.data.get('shipment_status').split(",")
                order_status_field_value=[]
                for values in list_of_order_status:
                    order_status_field_value.append(values)
                result=result.filter(shipment_status__in=order_status_field_value)

            if request.data.get('manager_warehouse_id'):
                manager_warehouse_id = request.data.get('manager_warehouse_id');
                if manager_warehouse_id != '':
                    result=result.filter(warehouse_id=manager_warehouse_id)

            if request.data.get('date'):
                date = request.data.get('date').split("##")
                start_date = date[0]
                end_date = date[1]
                if start_date == 'null' and end_date == 'null':
                    pass
                else:
                    result=result.filter(created__range=[start_date,end_date])

            if request.data.get('warehouse_status'):
                warehouse_status = request.data.get('warehouse_status')
                if warehouse_status is not None and warehouse_status!="":
                    if warehouse_status.lower() == "payment_complete":
                        result=result.exclude(shipment_status__in=["Invoicing","Picking"])

                    if warehouse_status.lower() == "payment_pending":
                        result=result.filter(shipment_status__in=["Invoicing"])

                    if warehouse_status.lower() == "delivered":
                        result=result.filter(order__order_status=4, order__buy_status=1)

                    if warehouse_status.lower() == "orders_in_picking":
                        result=result.filter(shipment_status__in=["Picking"] )

            print("result================", result.query)
        elif table_name == 'EngageboostUsers' and screen_name=='list':
            warehouse_id = request.data.get('warehouse_id')
            result=result.filter(user_type = "backend")
            if warehouse_id is not None and warehouse_id!="":
                if warehouse_id>0:
                    result=result.filter(warehouse_id=warehouse_id)

        elif table_name =='EngageboostGroups' and screen_name=='list':
            if request.data.get('warehouse_id'):
                warehouse_id = str(request.data.get('warehouse_id'))
                result = result.filter(warehouse_id = warehouse_id)

        elif table_name =='EngageboostRolemasters' and screen_name=='list':
            if request.data.get('warehouse_id'):
                warehouse_id = str(request.data.get('warehouse_id'))
                result = result.filter(warehouse_id = warehouse_id)

        if table_name=='EngageboostOrdermaster':
            # return order data filter
            if screen_name=='return_list':
                return_status_in = ['Pending','Authorized','Processing','Full Returned','Partial Returned','Credit Issued','Declined','Completed','Driver Assigned']
                result = result.filter(website_id=website_id,buy_status=1,return_status__in=return_status_in)

            # return order data filter
            if request.data.get('order_status'):
                list_of_order_status = request.data.get('order_status').split(",")
                order_status_field_value=[]
                for values in list_of_order_status:
                    order_status_field_value.append(values)
                result=result.filter(order_status__in=order_status_field_value)

            if request.data.get('webshop_id'):
                list_of_webshop_id = request.data.get('webshop_id').split(",")
                webshop_id_field_value=[]
                for values in list_of_webshop_id:
                    webshop_id_field_value.append(values)
                result=result.filter(webshop_id__in=webshop_id_field_value)

            if request.data.get('warehouse_id'):
                warehouse_id = str(request.data.get('warehouse_id'))
                list_of_warehouse_id = warehouse_id.split(",")
                warehouse_id_field_value=[]
                for values in list_of_warehouse_id:
                    warehouse_id_field_value.append(values)
                result=result.filter(assign_wh__in=warehouse_id_field_value)

            if request.data.get('date'):
                date = request.data.get('date').split("##")
                start_date = date[0]
                end_date = date[1]
                if start_date == 'null' and end_date == 'null':
                    pass
                else:
                    # result=result.filter(created__range=[,end_date])
                    start_date = start_date[:10]
                    end_date = end_date[:10]
                    result=result.filter(created__date__gte=start_date,created__date__lte=end_date)

            if request.data.get('zones'):
                list_of_zones = request.data.get('zones').split(",")
                zone_field_value=[]
                for values in list_of_zones:
                    zone_field_value.append(values)
                result=result.filter(zone_id__in=zone_field_value)

            if request.data.get('tags'):
                list_of_tags = request.data.get('tags').split(",")
                tags_field_value=[]
                for values in list_of_tags:
                    tags_field_value.append(values)
                result=result.filter(tags__in=tags_field_value)

            if request.data.get('delivery_date'):
                date = request.data.get('delivery_date').split("##")
                delivery_date_from = date[0]
                delivery_date_to = date[1]
                if delivery_date_from == 'null' and delivery_date_to == 'null':
                    pass
                else:
                    result=result.filter(delivery_date__range=[delivery_date_from,delivery_date_to])

            if request.data.get('delivery_slot'):
                list_of_delivery_slot = request.data.get('delivery_slot').split(",")
                delivery_slot_field_value=[]
                for values in list_of_delivery_slot:
                    delivery_slot_field_value.append(values)
                # result=result.filter(slot_start_time__in=delivery_slot_field_value)
                # print(delivery_slot_field_value)
                result=result.filter(time_slot_id__in=delivery_slot_field_value)

            if request.data.get('shipping_status'):
                list_of_shipping_status = request.data.get('shipping_status').split(",")
                shipping_status_field_value=[]
                for values in list_of_shipping_status:
                    shipping_status_field_value.append(values)
                result=result.filter(channel_shipping_status__in=shipping_status_field_value)

            if request.data.get('warehouse_status'):
                warehouse_status = request.data.get('warehouse_status')
                if warehouse_status is not None and warehouse_status!="":
                    if warehouse_status.lower() == "pending":
                        result=result.filter(order_status=0, buy_status=1)

                    if warehouse_status.lower() == "payment_complete":
                        # result=result.exclude(order_status__in = [0,2,4], shipment_order__shipment_status__in=["Invoicing","Picking"])
                        result=result.filter(order_status__in=[100,1], buy_status=1).exclude(shipment_order__shipment_status__in=["Invoicing","Picking"])

                    if warehouse_status.lower() == "payment_pending":
                        result=result.filter(shipment_order__shipment_status__in=["Invoicing"],order_status=100, buy_status=1 )

                    if warehouse_status.lower() == "delivered":
                        result=result.filter(order_status=4, buy_status=1)

                    if warehouse_status.lower() == "orders_in_picking":
                        result=result.filter(shipment_order__shipment_status__in=["Picking"],order_status=100, buy_status=1 )


            # [{"field":"custom_order_id","value":"#ABC001,#ABC006","find_type":""},{"field":"webshop_id","value":"","find_type":""}]

            if request.data.get('advance_filter'):
                field_value=[]
                advance_filters = ast.literal_eval(request.data.get('advance_filter'))
                for advance_filter in advance_filters:
                    list_of_values = advance_filter["value"].split(",")
                    field_value=[]
                    for values in list_of_values:
                        field_value.append(values)
                    # print(field_value)
                    if advance_filter["find_type"]=="equal":
                        field = {advance_filter["field"]+'__in':field_value}
                        result=result.filter(**field)
                    elif advance_filter["find_type"]=="notequal":
                        field = {advance_filter["field"]+'__in':field_value}
                        result=result.filter(~Q(**field))
                    else:
                        field = {advance_filter["field"]+'__icontains':field_value}
                        result=result.filter(**field)
                    # Model.objects.extra(where=['FIND_IN_SET(15, field)'])
            # print("result++++++++", result.query)
            result_all = result.count()
            result1 = result.count()
            result2 = result.count()
            result=result

        elif table_name=='EngageboostOrderProducts':
            if request.data.get('order_status'):
                list_of_order_status = request.data.get('order_status').split(",")
                order_status_field_value=[]
                for values in list_of_order_status:
                    order_status_field_value.append(values)
                result=result.filter(status__in=order_status_field_value)

            if request.data.get('webshop_id'):
                list_of_webshop_id = request.data.get('webshop_id').split(",")
                webshop_id_field_value=[]
                order_ids=[]
                for values in list_of_webshop_id:
                    webshop_id_field_value.append(values)

                webshop_cond = EngageboostOrdermaster.objects.all().filter(webshop_id__in=webshop_id_field_value)
                if webshop_cond:
                    orderMasterDetails = OrderMasterSerializer(webshop_cond,many=True)

                    for orderMaster in orderMasterDetails.data:
                        order_ids.append(orderMaster["id"])

                result=result.filter(order_id__in=order_ids)

            if request.data.get('warehouse_id'):
                list_of_warehouse_id = request.data.get('warehouse_id').split(",")
                warehouse_id_field_value=[]
                for values in list_of_warehouse_id:
                    warehouse_id_field_value.append(values)
                result=result.filter(assign_to__in=warehouse_id_field_value)

            if request.data.get('destination'):
                list_of_destination = request.data.get('destination').split(",")
                destination_field_value=[]
                order_ids=[]
                for values in list_of_destination:
                    destination_field_value.append(values)

                webshop_cond = EngageboostOrdermaster.objects.all().filter(delivery_country__in=destination_field_value)
                if webshop_cond:
                    orderMasterDetails = OrderMasterSerializer(webshop_cond,many=True)
                    for orderMaster in orderMasterDetails.data:
                        order_ids.append(orderMaster["id"])
                result=result.filter(order_id__in=order_ids)

            if request.data.get('tags'):
                list_of_tags = request.data.get('tags').split(",")
                tags_field_value=[]
                for values in list_of_tags:
                    tags_field_value.append(values)
                result=result.filter(tags__in=tags_field_value)

            if request.data.get('date'):
                date = request.data.get('date').split("##")
                start_date = date[0]
                end_date = date[1]
                if start_date == 'null' and end_date == 'null':
                    pass
                else:
                    result=result.filter(created__range=[start_date,end_date])

            result = result.order_by('order__created')
                # result=result.filter(created__range=[start_date,end_date])

            # [{"field":"custom_order_id","value":"#ABC001,#ABC006","find_type":""},{"field":"webshop_id","value":"","find_type":""}]

            if request.data.get('advance_filter'):
                field_value=[]
                advance_filters = ast.literal_eval(request.data.get('advance_filter'))
                for advance_filter in advance_filters:
                    list_of_values = advance_filter["value"].split(",")
                    field_value=[]
                    for values in list_of_values:
                        field_value.append(values)
                    # print(field_value)
                    if advance_filter["find_type"]=="equal":
                        field = {advance_filter["field"]+'__in':field_value}
                        result=result.filter(**field)
                    elif advance_filter["find_type"]=="notequal":
                        field = {advance_filter["field"]+'__in':field_value}
                        result=result.filter(~Q(**field))
                    else:
                        field = {advance_filter["field"]+'__icontains':field_value}
                        result=result.filter(**field)
                    # Model.objects.extra(where=['FIND_IN_SET(15, field)'])

            result_all = result.count()
            result1 = result.count()
            result2 = result.count()
            result=result

        elif table_name=='EngageboostBrandMasters':
            if request.data.get('warehouse_id'):
                warehouse_id = request.data.get('warehouse_id')
                brands = EngageboostBrandWarehouse.objects.filter(warehouse_id=warehouse_id)
                brands = brands.values('brand_id')
                result=result.filter(id__in=brands)

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

        elif table_name=='EngageboostFedexZipcodes':
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
        # /////////Create Pagination
        if show_all == 0:
            page = self.paginate_queryset(result)
        else:
            page = result.all()

        if page is not None:
            serializer = serializer_class(page, many=True)
            # print(result.query)
            #####################Layout#################################
            module = table_name.replace("Engageboost", "")
            layouts = common.fetch_grid_layout(request,module,screen_name)
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
            elif table_name=='EngageboostShippingMastersSettings' and screen_name=='list':
                menu_fetch=''
            elif table_name=='EngageboostShippingMastersSettings' and screen_name=='list1':
                menu_fetch=''
            elif table_name=='EngageboostOrdermaster' and screen_name=='product-list-order':
                menu_fetch=''
            elif table_name=='EngageboostOrderProducts' and screen_name=='list':
                menu_fetch=''
            elif table_name=='EngageboostShippingMastersSettings' and screen_name=='list-flat-shipping' or screen_name=='list-free-shipping':
                menu_fetch=''
            elif table_name=='EngageboostFedexZipcodes' and screen_name=='list':
                menu_fetch=''
            elif table_name=='EngageboostTags' and screen_name=='list':
                menu_fetch=''
            elif table_name=='EngageboostAwbMasters' and screen_name=='list-in-courier':
                menu_fetch=''
            #========================================
            elif table_name=='EngageboostZoneMasters' and screen_name=='list':
                menu_fetch=''

            elif table_name=='EngageboostZoneMasters' and screen_name=='list_zone':
                menu_fetch=''

            elif table_name=='EngageboostZoneMasters' and screen_name=='list_area':
                menu_fetch=''

            elif table_name=='EngageboostZoneMasters' and screen_name=='list_subarea':
                menu_fetch=''

            elif table_name=='EngageboostDeliverySlot' and screen_name=='list':
                menu_fetch=''

            elif table_name=='EngageboostPriceFormula' and screen_name=='list':
                menu_fetch=''

            elif table_name=='EngageboostCreditPoint' and screen_name=='list_earn':
                menu_fetch=''

            elif table_name=='EngageboostCreditPoint' and screen_name=='list_burn':
                menu_fetch=''
            #========================================
            else:
                menu_fetch=EngageboostMenuMasters.objects.using(company_db).get(module=module)

            menu_id = 0
            if menu_fetch:
                menu_id = menu_fetch.id
                menu_link=menu_fetch.link

            if issuperadmin=='Y':
                add='Y'
                edit='Y'
                delete='Y'
                status='Y'
                role_permission={"add":"Y","edit":"Y","delete":"Y","view":"Y","block":"Y","import_field":'Y',"export":'Y',"shipping_processes":'Y',"print":'1'}
            else:
                role_per = EngageboostRoleMenuPermissions.objects.using(company_db).get(role_id=role_id,master_id=menu_id,isblocked=0,isdeleted=0)
                role_permission={"add":role_per.add,"edit":role_per.edit,"delete":role_per.delete,"view":role_per.view,"block":role_per.block,"import_field":role_per.import_field,"export":role_per.export,"shipping_processes":role_per.shipping_processes,"print":role_per.print}
                add=role_per.add
                edit=role_per.edit
                delete=role_per.delete
                status=role_per.block
            ######################Role Permission###############

            #####################Action Links#################################
            link=module.replace("masters", "")
            link=link.replace("Masters", "")
            row=[]
            row_dict={}
            layout_fetch = EngageboostGridLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
            is_popup=layout_fetch.add_edit_url_popup
            folder=layout_fetch.folder_name
            layout_module=layout_fetch.module_name
            # print("serializer.data==========", serializer.data)
            for serializer_row in serializer.data :
                row_dict=serializer_row
                if table_name =='EngageboostCurrencyMasters':
                    edit_link='<a href="javascript:void(0)" ng-click="setBaseCurrency('+str(serializer_row['id'])+')"><span class="icon-edit-box"></span></a>'
                    delete_link=''
                    status_link=''
                #============================================
                elif table_name == 'EngageboostZoneMasters':
                    edit_link = ''
                    delete_link = ''
                    status_link = ''

                elif table_name == 'EngageboostVehicleMasters':
                    edit_link = ''
                    delete_link = ''
                    status_link = ''

                elif table_name == 'EngageboostDeliveryManagers':
                    edit_link = ''
                    delete_link = ''
                    status_link = ''

                elif table_name == 'EngageboostDeliverySlot':
                    edit_link = ''
                    delete_link = ''
                    status_link = ''

                elif table_name == 'EngageboostPriceFormula':
                    edit_link = ''
                    delete_link = ''
                    status_link = ''

                elif table_name == 'EngageboostCreditPoint':
                    edit_link = ''
                    delete_link = ''
                    status_link = ''
                #============================================
                else:
                    if table_name =='EngageboostOrderProducts' or table_name =='EngageboostFedexZipcodes': #******Action link not applicable for this module
                        edit_link=delete_link=status_link=''
                    else:
                        #Edit button start here....
                        if edit=='Y':
                            #Popup/page setup start here....
                            if is_popup=='y':
                                edit_link='<a href="javascript:void(0)" popup-box box-id="'+str(serializer_row['id'])+'" init-fn="add_edit_load(arg1)" box-template="static/pages/'+str(folder)+'/add_'+str.lower(module)+'.html" elem-id="#add_'+str.lower(module)+'_pop" mdTooltip="Edit Record"><span class="icon-edit-box"></span></a>'
                            else:
                                if table_name=='EngageboostDiscountMasters':
                                    edit_link='<a href="#/'+str.lower(link)+'/edit/'+str(serializer_row['id'])+'" ng-click="addTab(\''+str.lower(link)+''+str(menu_link)+'edit''\',\''+str.lower(link)+'/edit/'+str(serializer_row['id'])+'\',\'Edit '+str(layout_module)+'\',tabs[selectedTab].id)" mdTooltip="Edit Record"><span class="icon-edit-box"></span></a>'
                                else:
                                    edit_link='<a href="#/'+str.lower(link)+'/edit/'+str(serializer_row['id'])+'" ng-click="addTab(\''+str.lower(link)+'edit''\',\''+str.lower(link)+'/edit/'+str(serializer_row['id'])+'\',\'Edit '+str(layout_module)+'\',tabs[selectedTab].id)" mdTooltip="Edit Record"><span class="icon-edit-box"></span></a>'
                            #Popup/page setup end here....
                        else:
                            edit_link='<a href="javascript:void(0)" ng-click="$root.showAlertBox(\'Permission Error\',\'You have no permission to edit\')" mdTooltip="Edit Record"><span class="icon-edit-box"></span></a>'
                        #Delete button start here....
                        if table_name == 'EngageboostGlobalSettings':
                            delete_link = ''
                        else:
                            delete_link='<a href="javascript:void(0)" global-update tbl-name="'+table_name+'" tbl-action="delete" rec-id="'+str(serializer_row['id'])+'" (click)="updateStatusAll(2,\''+str(serializer_row['id'])+'\')" mdTooltip="Delete Record"><span class="icon-delete-box"></span></a>'
                        #Status button start here....
                        if serializer_row['isblocked']=='y':
                            status_link='<a href="javascript:void(0)" global-update tbl-name="'+table_name+'" tbl-action="status" rec-id="'+str(serializer_row['id'])+'" rec-status="'+str(serializer_row['isblocked'])+'" (click)="updateStatusAll(0,\''+str(serializer_row['id'])+'\')" mdTooltip="Unblock Record"><span class="icon-check-box"></span></a>'
                        else:
                            status_link='<a href="javascript:void(0)" global-update tbl-name="'+table_name+'" tbl-action="status" rec-id="'+str(serializer_row['id'])+'" rec-status="'+str(serializer_row['isblocked'])+'" (click)="updateStatusAll(1,\''+str(serializer_row['id'])+'\')" mdTooltip="Block Record"><span class="icon-check-box"></span></a>'

                action='<div class="action">'+edit_link+delete_link+status_link+'</div>'
                #####################Table Based Nesting#################################

                if table_name =='EngageboostProducts':
                    product_id=serializer_row['id']
                    brand_id=serializer_row['brand']
                    supplier_id=serializer_row['supplier_id']
                    fetchGlobalSettings=EngageboostGlobalSettings.objects.using(company_db).get(website_id=1)

                    prefixs = ""
                    suffixs = ""
                    if fetchGlobalSettings.sku_prefix!="" and fetchGlobalSettings.sku_prefix!=None:
                        prefixs = fetchGlobalSettings.sku_prefix
                    if fetchGlobalSettings.sku_suffix!="" and fetchGlobalSettings.sku_suffix!=None:
                        suffixs = fetchGlobalSettings.sku_suffix

                    row_dict['sku']=prefixs+serializer_row['sku']+suffixs
                    # /////Category////////
                    fetch_category=EngageboostProductCategories.objects.using(company_db).all().filter(product=product_id)
                    categoryarr=[]
                    catdict={}
                    for cat in fetch_category:
                        catdict=cat.category.name
                        categoryarr.append(catdict)
                    category=','.join([str(i) for i in categoryarr])
                    row_dict['category']=category
                    # ////////brand/////////
                    brandarr=[]
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
                    supplierarr=[]
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

                #==================================================================
                if table_name =='EngageboostCategoryMasters':
                    if len(serializer_row['lang_data'])>0:
                        for landdata in serializer_row['lang_data']:
                            serializer_row[landdata['field_name']]=landdata['field_name']
                    serializer_row.pop('lang_data')

                if table_name == 'EngageboostZoneMasters' and screen_name == 'list_zone':
                    country_id = row_dict['country_id']
                    row_dict['country'] = get_countryname(country_id)
                    if request.data.get('search'):
                        if row_dict['name'].find(key) < 0 and row_dict['state_name'].find(key) < 0 and row_dict['city'].find(key) < 0 and row_dict['country'].find(key) < 0:
                            continue

                elif table_name == 'EngageboostZoneMasters' and screen_name == 'list_area':
                    zone_id = row_dict['zone_id']
                    row_dict['zone_name'] = get_zonename(zone_id)
                    if request.data.get('search'):
                        if row_dict['name'].find(key) < 0 and row_dict['zone_name'].find(key) < 0 and row_dict['zipcode'].find(key) < 0:
                            continue

                elif table_name == 'EngageboostZoneMasters' and screen_name == 'list_subarea':
                    zone_id = row_dict['zone_id']
                    row_dict['zone_name'] = get_zonename(zone_id)
                    area_id = row_dict['area_id']
                    row_dict['area_name'] = get_areaname(area_id)
                    if request.data.get('search'):
                        if row_dict['name'].find(key) < 0 and row_dict['zone_name'].find(key) < 0 and row_dict['zipcode'].find(key) < 0 and row_dict['area_name'].find(key) <0:
                            continue


                elif table_name == 'EngageboostVehicleMasters' and screen_name == 'list':
                    manager_id = row_dict['manager_id']
                    row_dict['manager_name'] = get_managername(manager_id)
                    warehouse_ids = row_dict['warehouse_ids']
                    warehouse_name = ''
                    if warehouse_ids.find(',') > -1:
                        for warehouse_id in warehouse_ids.split(','):
                            warehouse_name = warehouse_name + ',' + str(get_warehousename(warehouse_id))
                        warehouse_name = warehouse_name[1:]
                    else:
                        # zone_name = get_zonename(warehouse_ids)
                        whDetails = EngageboostWarehouseMasters.objects.using(company_db).filter(id=warehouse_ids).first()
                        if whDetails:
                            warehouse_name = whDetails.name
                    row_dict['warehouse_name'] = warehouse_name

                    if request.data.get('search'):
                        if row_dict['phone_number'].find(key) < 0 and row_dict['vehicle_number'].find(key) < 0 and \
                            row_dict['model_no'].find(key) < 0 and row_dict['zip_code'].find(key) < 0 and\
                            row_dict['manager_name'].find(key) < 0 and row_dict['zone_name'].find(key) < 0:
                            continue
                elif table_name == 'EngageboostDeliveryManagers' and screen_name == 'list':
                    warehouse_ids = row_dict['warehouse_ids']
                    warehouse_name = ''
                    if warehouse_ids.find(',') > -1:
                        for warehouse_id in warehouse_ids.split(','):
                            warehouse_name = warehouse_name + ',' + str(get_warehousename(warehouse_id))
                        warehouse_name = warehouse_name[1:]
                    else:
                        # zone_name = get_zonename(warehouse_ids)
                        whDetails = EngageboostWarehouseMasters.objects.using(company_db).filter(id=warehouse_ids).first()
                        if whDetails:
                            warehouse_name = whDetails.name
                    row_dict['warehouse_name'] = warehouse_name

                #==================================================================
                elif table_name =='EngageboostPresets':
                    # /////size////////
                    size=str(serializer_row['sizel'])+"*"+str(serializer_row['sizew'])+"*"+str(serializer_row['sizeh'])
                    row_dict['size']=size
                elif table_name =='EngageboostEmktContactlists':
                    # /////contact////////
                    contlist_id=serializer_row['id']
                    contact=EngageboostEmktContacts.objects.using(company_db).filter(contact_list_id=contlist_id).count()
                    time_zone=get_date(serializer_row['created'],global_setting_zone,global_setting_date)
                    row_dict['created']=time_zone
                    row_dict['contact']=contact

                elif table_name =='EngageboostEmktSegments':
                    # /////contact////////
                    seg_id=serializer_row['id']
                    contact=EngageboostEmktSegmentContactlists.objects.using(company_db).filter(segment_id=seg_id).count()
                    row_dict['contact']=contact
                elif table_name =='EngageboostEmktSegments':
                    # /////contact////////
                    seg_id=serializer_row['id']
                    contact=EngageboostEmktSegmentContactlists.objects.using(company_db).filter(segment_id=seg_id).count()
                    row_dict['contact']=contact

                elif table_name =='EngageboostEmailTypeContents':
                    # /////contact////////
                    email_type=serializer_row['email_type']
                    if email_type == 'T':
                        contact ='TEXT'
                    elif email_type == 'HT':
                        contact ='HTML & TEXT'
                    elif email_type == 'H':
                        contact ='HTML'
                    row_dict['email_type']=contact

                elif table_name=='EngageboostCustomers' and screen_name=='list':
                    count=EngageboostOrdermaster.objects.using(company_db).filter(customer_id=serializer_row['id'],isdeleted='n').count()
                    row_dict['totalorder'] = count
                    net_amount = EngageboostOrdermaster.objects.using(company_db).filter(customer_id=serializer_row['id'],isdeleted='n').aggregate(Sum('gross_amount'))
                    row_dict['avgorder'] = net_amount['gross_amount__sum']

                elif table_name =='EngageboostUsers':
                    created_date=None
                    if serializer_row['last_login']:
                        created_date = str(serializer_row['last_login']).split('+')
                        created_date = created_date[0]
                        time_zone=get_time(created_date,global_setting_zone,global_setting_date)
                        row_dict['last_login']=time_zone
                    else:
                        row_dict['last_login']=created_date

                    if serializer_row['role']:
                        row_dict['role_name']=serializer_row['role']['name']
                elif table_name =='EngageboostGroups':
                    # /////Modified////////
                    row_dict['modified']=get_date(serializer_row['modified'],global_setting_zone,global_setting_date)
                elif table_name =='EngageboostRolemasters':
                    # /////Modified////////
                    Groupcond = EngageboostGroups.objects.using(company_db).filter(id=serializer_row['group_id']).first()
                    if Groupcond:
                        GroupDetails = GroupSerializer(Groupcond, partial=True)
                    row_dict['group_id']=GroupDetails.data['name']
                    row_dict['modified']=get_date(serializer_row['modified'],global_setting_zone,global_setting_date)
                elif table_name =='EngageboostGlobalSettings':
                    # /////timezone////////
                    timezone_id=serializer_row['timezone_id']
                    timezone_fetch=EngageboostTimezones.objects.using(company_db).get(id=timezone_id)
                    row_dict['timezone_location']=timezone_fetch.timezone_location+' '+timezone_fetch.gmt
                    row_dict['date_format']=serializer_row['date_format'].replace("%","")

                elif table_name =='EngageboostEmktContacts':
                    # /////timezone////////
                    time_zone=get_date(serializer_row['created'],global_setting_zone,global_setting_date)
                    row_dict['created']=time_zone
                elif table_name =='EngageboostCurrencyMasters':
                    # /////Currency////////
                    currency_id=serializer_row['id']
                    timezone_fetch=EngageboostCurrencyRates.objects.using(company_db).get(engageboost_currency_master_id=currency_id,engageboost_company_website_id=1)
                    row_dict['exchange_rate']=timezone_fetch.exchange_rate
                    row_dict['isbasecurrency']=timezone_fetch.isbasecurrency
                    row_dict['modified']=get_date(timezone_fetch.modified,global_setting_zone,global_setting_date)
                    row_dict['created']=get_date(timezone_fetch.created,global_setting_zone,global_setting_date)
                elif table_name =='EngageboostCompanyWebsites':
                    time_zone=get_time(serializer_row['created'],global_setting_zone,global_setting_date)
                    row_dict['created']=time_zone
                elif table_name =='EngageboostPages':
                    created = get_time(serializer_row['created'],global_setting_zone,global_setting_date)
                    row_dict['created'] = created
                elif table_name =='EngageboostDiscountMasters':
                    time_zone = get_time(serializer_row['disc_start_date'],global_setting_zone,global_setting_date)
                    row_dict['disc_start_date'] = time_zone
                    time_zone1=get_time(serializer_row['disc_end_date'],global_setting_zone,global_setting_date)
                    row_dict['disc_end_date'] = time_zone1
                    # print(serializer_row['coupon_type'])
                    if serializer_row['coupon_type']==1:
                        row_dict['coupon_type']="Single Use"
                    if serializer_row['coupon_type']==2:
                        row_dict['coupon_type']="Multiple Use"

                elif table_name =='EngageboostCategoryMasters':
                    row_dict['created'] = get_date(serializer_row['created'],global_setting_zone,global_setting_date)
                    # /////Parent Category////////
                    if serializer_row['parent_id']>0:
                        fetch_parent=EngageboostCategoryMasters.objects.using(company_db).get(id=serializer_row['parent_id'])
                        parent_category=fetch_parent.name
                    else:
                        parent_category = ''
                    row_dict['parent_category'] = parent_category
                    row_dict['modified']=get_date(serializer_row['modified'],global_setting_zone,global_setting_date)
                elif table_name =='EngageboostProductReviews':
                    row_dict['created']=get_time(serializer_row['created'],global_setting_zone,global_setting_date)
                    row_dict['product_name']=row_dict['product']['name']
                    row_dict['product_sku']=row_dict['product']['sku']

                elif table_name =='EngageboostShippingMasters':
                    # /////contact////////
                    shipping_id=serializer_row['id']
                    total=EngageboostAwbMasters.objects.using(company_db).filter(shipping_method_id=shipping_id).count()
                    awb_used=EngageboostAwbMasters.objects.using(company_db).filter(shipping_method_id=shipping_id,isused='y').count()
                    awb_unused=EngageboostAwbMasters.objects.using(company_db).filter(shipping_method_id=shipping_id,isused='n').count()
                    row_dict['total']=total
                    row_dict['awb_used']=awb_used
                    row_dict['awb_unused']=awb_unused
                elif table_name=='EngageboostDiscountMasters' and screen_name=='list1':
                    if serializer_row['coupon_type']==2:
                        row_dict['coupon_type']='Multiple Use'
                    else:
                        row_dict['coupon_type']='Single Use'
                elif table_name=='EngageboostDiscountMasters' and screen_name=='list2':
                    if serializer_row['disc_type']==1:
                        row_dict['disc_type']='Percentage of the original price'
                    else:
                        row_dict['disc_type']='Fixed Amount'
                elif table_name =='EngageboostWarehouseMasters':
                    # /////Applicable Channels////////
                    count_channel_applicable=EngageboostWarehouseMasterApplicableChannels.objects.using(company_db).filter(warehouse_master_id=serializer_row['id']).count()
                    channelarr=[]
                    channeldict={}
                    if count_channel_applicable>0:
                        fetch_channel_applicable=EngageboostWarehouseMasterApplicableChannels.objects.using(company_db).all().filter(warehouse_master_id=serializer_row['id'])
                        for channel in fetch_channel_applicable:
                            fetch_channel=EngageboostChannels.objects.using(company_db).get(id=channel.applicable_channel_id)
                            channeldict=fetch_channel.name
                            channelarr.append(channeldict)
                        channel=','.join([str(i) for i in channelarr])
                    else:
                        channel=''
                    row_dict['channel']=channel
                elif table_name =='EngageboostHsnCodeMaster':
                    # /////List Of HSN CODE////////
                    created_date = str(serializer_row['created']).split('+')
                    created_date = created_date[0]
                    row_dict['created']=get_time(created_date,global_setting_zone,global_setting_date)
                elif table_name =='EngageboostCategoryMasters':
                    # /////Parent Category////////
                    if serializer_row['parent_id']>0:
                        fetch_parent=EngageboostCategoryMasters.objects.using(company_db).get(id=serializer_row['parent_id'])
                        parent_category=fetch_parent.name
                    else:
                        parent_category=''
                    row_dict['parent_category']=parent_category

                elif table_name =='EngageboostOrderProducts':
                    # status@@tags@@created@@created_day@@order_id@@sku@@product_name@@quantity@@delivery_name@@delivery_email_address@@billing_email_address@@delivery_state@@delivery_city@@delivery_postcode@@assign_to@@product_price@@shipping_price@@product_discount_price@@product_excise_duty@@product_tax_price
                    # /////Fetch From Order Master Table///////
                    quantity=0
                    if serializer_row['quantity']:
                        quantity=quantity+serializer_row["quantity"]
                        if serializer_row["deleted_quantity"]:
                            quantity=quantity-serializer_row["deleted_quantity"]
                        if serializer_row["shortage"]:
                            quantity=quantity-serializer_row["shortage"]
                        if serializer_row["returns"]:
                            quantity=quantity-serializer_row["returns"]
                        row_dict["quantity"]=quantity
                    else:
                        row_dict["quantity"]=quantity

                    row_dict["order_status"] = serializer_row['status']
                    if serializer_row['product']['id']:
                        productDetails=EngageboostProducts.objects.using(company_db).filter(id=serializer_row['product']['id']).first()
                        if productDetails:
                            row_dict["product_name"] = productDetails.name
                            row_dict["sku"]=productDetails.sku

                    if serializer_row['order'] and serializer_row['order']>0:
                        orderMasterInfo=EngageboostOrdermaster.objects.using(company_db).filter(id=serializer_row['order']).first()
                        if orderMasterInfo:
                            row_dict["buy_status"] = orderMasterInfo.buy_status
                            row_dict["order_id"]=orderMasterInfo.custom_order_id
                            row_dict["delivery_name"]=orderMasterInfo.delivery_name
                            row_dict["delivery_email_address"]=orderMasterInfo.delivery_email_address
                            row_dict["billing_email_address"]=orderMasterInfo.billing_email_address
                            row_dict["delivery_country"]=''
                            row_dict["delivery_state"]=''
                            # row_dict["tags"]=''
                            # row_dict["assign_to"]=''
                            if orderMasterInfo.delivery_country:
                                countryDetails = EngageboostCountries.objects.using(company_db).filter(id=orderMasterInfo.delivery_country).first()
                                if countryDetails:
                                    row_dict["delivery_country"]=countryDetails.country_name

                            if orderMasterInfo.delivery_state:
                                stateDetails = EngageboostStates.objects.using(company_db).filter(id=orderMasterInfo.delivery_state).first()
                                if stateDetails:
                                    row_dict["delivery_state"]=stateDetails.state_name

                            row_dict["delivery_city"]=orderMasterInfo.delivery_city
                            row_dict["delivery_postcode"]=orderMasterInfo.delivery_postcode
                        else:
                            row_dict["delivery_name"]=row_dict["delivery_email_address"]=row_dict["billing_email_address"]=row_dict["delivery_country"]=row_dict["delivery_state"]=row_dict["delivery_city"]=row_dict["delivery_postcode"]=''
                            row_dict["buy_status"] = 0
                    else:
                        row_dict["delivery_name"]=row_dict["delivery_email_address"]=row_dict["billing_email_address"]=row_dict["delivery_country"]=row_dict["delivery_state"]=row_dict["delivery_city"]=row_dict["delivery_postcode"]=''
                        row_dict["buy_status"] = 0

                    if serializer_row['tags']:
                        tagDetails = EngageboostTags.objects.using(company_db).filter(id=serializer_row['tags']).first()
                        if tagDetails:
                            row_dict["tags"] = tagDetails.tag_name
                            row_dict["tags_color_code"] = tagDetails.color_code
                        else:
                            row_dict["tags"]=''
                            row_dict["tags_color_code"] = ''

                    if serializer_row['assign_to']:
                        userDetails = EngageboostUsers.objects.using(company_db).filter(id=serializer_row['assign_to']).first()
                        if userDetails:
                            row_dict["assign_to"]=userDetails.first_name+' '+userDetails.last_name
                        else:
                            row_dict["assign_to"]=''
                elif table_name =='EngageboostOrdermaster':
                    # if screen_name=='return_list':
                    if serializer_row['id']:
                        quantity=0
                        orderProductDetailscond = EngageboostOrderProducts.objects.using(company_db).filter(order_id=serializer_row['id']).all()
                        if orderProductDetailscond:
                            for orderProduct in orderProductDetailscond:
                                quantity=quantity+orderProduct.quantity
                                quantity=quantity-orderProduct.deleted_quantity
                                if orderProduct.shortage:
                                    quantity=quantity-orderProduct.shortage
                                if orderProduct.returns:
                                    quantity=quantity-orderProduct.returns
                            row_dict["quantity"]=quantity
                        else:
                            row_dict["quantity"]=quantity
                    # if screen_name=='list':


                    if serializer_row['tags']:
                        tagDetails = EngageboostTags.objects.using(company_db).filter(id=serializer_row['tags']).first()
                        if tagDetails:
                            row_dict["tags"]=tagDetails.tag_name
                            row_dict["tags_color_code"]=tagDetails.color_code
                        else:
                            row_dict["tags"]=''
                            row_dict["tags_color_code"] = ''

                    if serializer_row['assign_to']:
                        userDetails = EngageboostUsers.objects.using(company_db).filter(id=serializer_row['assign_to']).first()
                        if userDetails:
                            row_dict["assign_to"]=userDetails.first_name+' '+userDetails.last_name
                        else:
                            row_dict["assign_to"]=''

                    if serializer_row['assign_wh']:
                        whDetails = EngageboostWarehouseMasters.objects.using(company_db).filter(id=serializer_row['assign_wh']).first()
                        if whDetails:
                            row_dict["assign_wh"]=serializer_row['assign_wh']
                            row_dict["assign_wh_name"]=whDetails.name
                        else:
                            row_dict["assign_wh"]=''
                            row_dict["assign_wh_name"]=""
                    try:
                        if serializer_row['webshop_id']:
                            webshopDetails = EngageboostChannels.objects.using(company_db).filter(id=serializer_row['webshop_id']).first()
                            if webshopDetails:
                                row_dict["webshop_id"]=webshopDetails.name
                            else:
                                row_dict["webshop_id"]=''
                    except KeyError:
                        row_dict["webshop_id"]=''

                    if serializer_row['delivery_country']:
                        countryDetails = EngageboostCountries.objects.using(company_db).filter(id=serializer_row['delivery_country']).first()
                        if countryDetails:
                            row_dict["delivery_country"]=countryDetails.country_name

                    if serializer_row['delivery_state']:
                        stateDetails = EngageboostStates.objects.using(company_db).filter(id=serializer_row['delivery_state']).first()
                        if stateDetails:
                            row_dict["delivery_state"]=stateDetails.state_name
                            row_dict["delivery_state_name"]=stateDetails.state_name

                    if serializer_row['trent_picklist_id'] and serializer_row['trent_picklist_id']:
                        crate_arr = EngageboostCrates.objects.filter(trent_picklist_id=serializer_row['trent_picklist_id'], order_id=serializer_row['id'], isdeleted='n', isblocked='n').all()
                        crates_name_arr = []
                        for crate_arr_data in crate_arr:
                            crates_name_arr.append(crate_arr_data.crate_barcode)
                        # sprint(crates_name_arr)
                        if len(crates_name_arr) > 0:
                            row_dict["crate_no"] = ", ".join(crates_name_arr)
                        else:
                            row_dict["crate_no"] = ''

                elif table_name =='EngageboostShippingMastersSettings' and screen_name=='list-free-shipping':
                    list_of_country=[]
                    country_ids = serializer_row["country_ids"].split(',')
                    for i in country_ids:
                        countryDetails = EngageboostCountries.objects.using(company_db).filter(id=i).first()
                        if countryDetails:
                            list_of_country.append(countryDetails.country_name)
                    if list_of_country:
                        coutry_list = ",".join(list_of_country)
                    else:
                        coutry_list = ""

                    row_dict["country_ids"] = coutry_list

                elif table_name =='EngageboostFedexZipcodes':
                    if serializer_row['country_id']:
                        countryDetails = EngageboostCountries.objects.using(company_db).filter(id=serializer_row['country_id']).first()
                        if countryDetails:
                            row_dict["country_id"]=countryDetails.country_name
                        else:
                            row_dict["country_id"]=""
                elif table_name =='EngageboostCategoryBanners':
                    if serializer_row['warehouse_id']:
                        # warehouse_name = serializer_row['warehouse_id']['name']
                        # if warehouse_name:
                        # 	row_dict["warehouse_name"]=warehouse_name
                        # else:
                        # 	row_dict["warehouse_name"]=""

                        warehouse_name = ""
                        for warehouse_id in serializer_row['warehouse_id']:
                            if warehouse_name == "":
                                warehouse_name = warehouse_id['name']
                            else:
                                warehouse_name = warehouse_name + ","+warehouse_id['name']
                            row_dict["warehouse_name"]=warehouse_name
                    else:
                        row_dict["warehouse_name"]=""

                elif table_name =='EngageboostShipments' and screen_name=='list':
                    custom_order_id_arr = []
                    shipment_id = serializer_row["id"]
                    custom_order_ids = []
                    currency_code = ""
                    shipmentOrders = EngageboostShipmentOrders.objects.filter(shipment=serializer_row["id"]).all()
                    if request.data.get('warehouse_status'):
                        warehouse_status = request.data.get('warehouse_status')
                        if warehouse_status is not None and warehouse_status!="":
                            if warehouse_status.lower() == "payment_complete":
                                shipmentOrders=shipmentOrders.filter(order__order_status__in=[100,1], order__buy_status=1)

                            if warehouse_status.lower() == "payment_pending":
                                shipmentOrders=shipmentOrders.filter(order__order_status=100, order__buy_status=1 )

                            if warehouse_status.lower() == "delivered":
                                shipmentOrders=shipmentOrders.filter(order__order_status=4, order__buy_status=1)

                            if warehouse_status.lower() == "orders_in_picking":
                                shipmentOrders=shipmentOrders.filter(order__order_status=100, order__buy_status=1 )

                    for shipmentOrdersObj in shipmentOrders:
                        orderMasterCurrency = EngageboostOrdermaster.objects.filter(id=shipmentOrdersObj.order_id).values(
                            'currency_code').first()
                        currency_code = orderMasterCurrency['currency_code']
                        order_dict = {'id':shipmentOrdersObj.order_id, 'custom_order_id':shipmentOrdersObj.custom_order_id, 'shipping_cost':shipmentOrdersObj.order.shipping_cost,'gross_amount':shipmentOrdersObj.order.gross_amount,'cart_discount':shipmentOrdersObj.order.cart_discount, 'currency_code':currency_code}
                        custom_order_id_arr.append(order_dict)
                        custom_order_ids.append(shipmentOrdersObj.custom_order_id)
                    row_dict["custom_order_id"] = custom_order_id_arr
                    row_dict["currency_code"] = currency_code

                    custom_order_id_all = ''
                    if custom_order_ids:
                        custom_order_id_all = ",".join(custom_order_ids)
                    row_dict["custom_order_ids"] = custom_order_id_all

                    row_dict['quantity'] = 0
                    row_dict['net_amount'] = 0
                    row_dict['gross_amount'] = 0
                    row_dict['shipping_amount'] = 0
                    row_dict['discount_amount'] = 0
                    row_dict['tax_amount'] = 0
                    order_data = []
                    tax_type = ''
                    zone_id = 0
                    if serializer_row["zone_id"] and serializer_row["zone_id"] > 0 :
                        row_dict['zone_id'] = get_zonename(serializer_row["zone_id"])

                    whDetails = EngageboostWarehouseMasters.objects.filter(id=serializer_row['warehouse_id']).first()
                    if whDetails:
                        row_dict["warehouse_id"] = whDetails.name
                    else:
                        row_dict["warehouse_id"] = ''

                    find_all_shipments_product = EngageboostShipmentOrderProducts.objects.filter(shipment=shipment_id)
                    time_slot_id = ""
                    # print("Discount amount====", row_dict['discount_amount'])
                    # print("order id====", json.dumps(row_dict))
                    if find_all_shipments_product.count() > 0:
                        for single_product_row in find_all_shipments_product:
                            # print("single_product_row===========", single_product_row)
                            product_qty = 0
                            shortage = 0
                            deleted_quantity = 0
                            return_qty = 0
                            if single_product_row.order_product.quantity is not None and float(single_product_row.order_product.quantity)>0:
                                product_qty = float(single_product_row.quantity)
                            if single_product_row.order_product.shortage is not None and float(single_product_row.order_product.shortage)>0:
                                shortage = float(single_product_row.order_product.shortage)
                            if single_product_row.order_product.deleted_quantity is not None and float(single_product_row.order_product.deleted_quantity)>0:
                                deleted_quantity = float(single_product_row.order_product.deleted_quantity)

                            if single_product_row.order_product.returns is not None and float(single_product_row.order_product.returns)>0:
                                return_qty = float(single_product_row.order_product.returns)

                            product_qty = float(product_qty) - float(shortage) -float(deleted_quantity) - float(return_qty)
                            if float(product_qty)<=0:
                                product_qty = 0
                            # print("product_qty===", single_product_row.order_product.order_id, single_product_row.order_product.product_id, product_qty, single_product_row.order_product.quantity, single_product_row.order_product.shortage,single_product_row.order_product.deleted_quantity,single_product_row.order_product.returns)
                            row_dict["time_slot_date"] = single_product_row.order.time_slot_date
                            row_dict["time_slot_id"] = single_product_row.order.time_slot_id
                            tax_type = single_product_row.order.excise_duty
                            row_dict['net_amount'] += Decimal(single_product_row.order_product.product_price*product_qty).quantize(Decimal('.00'))
                            row_dict['shipping_amount'] += (0 if single_product_row.order_product.shipping_price is None else Decimal(single_product_row.order_product.shipping_price).quantize(Decimal('.00')))
                            # row_dict['discount_amount'] += (0 if single_product_row.order_product.product_discount_price is None else Decimal(single_product_row.order_product.product_discount_price).quantize(Decimal('.00')))
                            # product_qty = single_product_row.order_product.quantity
                            row_dict['tax_amount'] += (0 if single_product_row.order_product.product_tax_price is None else float(single_product_row.order_product.product_tax_price)*product_qty)
                            # row_dict['quantity'] += (0 if single_product_row.order_product.quantity is None else single_product_row.order_product.quantity)
                            row_dict['quantity'] += product_qty



                        row_dict['tax_amount'] = Decimal(row_dict['tax_amount']).quantize(Decimal('.00'))
                        for orderdata in row_dict['custom_order_id']:
                            row_dict['shipping_amount'] = float(row_dict['shipping_amount']) + float(orderdata['shipping_cost'])
                            row_dict['discount_amount'] = float(row_dict['discount_amount']) + float(orderdata['cart_discount'])
                        # print("net_amount=============", row_dict['custom_order_id'][0]['custom_order_id'],row_dict['net_amount'])
                        if tax_type == 'Inclusive Tax':
                            row_dict['gross_amount'] = (float(row_dict['net_amount'])+float(row_dict['shipping_amount']))-float(row_dict['discount_amount'])
                        else:
                            row_dict['gross_amount'] = (float(row_dict['net_amount'])+float(row_dict['shipping_amount'])+float(row_dict['tax_amount']))-float(row_dict['discount_amount'])

                        row_dict['gross_amount'] = Decimal(row_dict['gross_amount']).quantize(Decimal('.00'))
                    else:
                        order_data = EngageboostOrdermaster.objects.filter(shipment_id=shipment_id).first()
                        if order_data:
                            row_dict["time_slot_date"] = order_data.time_slot_date
                            row_dict["time_slot_id"] = order_data.time_slot_id
                        else:
                            row_dict["time_slot_date"] = ""
                            row_dict["time_slot_id"] = ""

                    # row_dict['created'] = get_date_from_datetime(serializer_row['created'],global_setting_zone,global_setting_date)
                    # row_dict['created_day'] = get_dayname_from_datetime(row_dict['created'],global_setting_zone,global_setting_date)

                    if "time_slot_date" in  row_dict and row_dict['time_slot_date'] is not None and row_dict['time_slot_date']!="":
                        row_dict['time_slot_date'] = common.get_date_from_datetime(row_dict['time_slot_date'],global_setting_zone, global_setting_date,'%Y-%m-%d') + " "+ row_dict["time_slot_id"]
                    else:
                        row_dict['time_slot_date'] = ""
                    #print(row_dict)
                elif table_name =='EngageboostTrentPicklists' and screen_name=='list':
                    custom_order_id=[]
                    shipmentOrders = EngageboostOrdermaster.objects.using(company_db).filter(trent_picklist_id=serializer_row["id"]).all()
                    if shipmentOrders:
                        shipmentOrders_Serializer = OrderMasterSerializer(shipmentOrders,many=True)
                        for shipment_Orders in shipmentOrders_Serializer.data:
                            custom_order_id.append(shipment_Orders["custom_order_id"])
                        if custom_order_id:
                            custom_order_ids = ",".join(custom_order_id)
                        else:
                            custom_order_ids = ""
                    else:
                        custom_order_ids = ""
                    row_dict["custom_order_id"] = custom_order_ids

                    whDetails = EngageboostWarehouseMasters.objects.using(company_db).filter(id=serializer_row['warehouse_id']).first()
                    if whDetails:
                        row_dict["warehouse_id"] = whDetails.name
                    else:
                        row_dict["warehouse_id"] = ''
                    row_dict['created'] = get_date_from_datetime(serializer_row['created'],global_setting_zone,global_setting_date)
                elif table_name =='EngageboostLanguages' and screen_name=='list':
                    if serializer_row['isblocked']=='y':
                        status_link='<a href="javascript:void(0)" global-update tbl-name="'+table_name+'" tbl-action="status" rec-id="'+str(serializer_row['id'])+'" rec-status="'+str(serializer_row['isblocked'])+'" (click)="updateStatusAll(0,\''+str(serializer_row['id'])+'\')" mdTooltip="Unblock Record"><span class="icon-check-box"></span></a>'
                    else:
                        status_link='<a href="javascript:void(0)" global-update tbl-name="'+table_name+'" tbl-action="status" rec-id="'+str(serializer_row['id'])+'" rec-status="'+str(serializer_row['isblocked'])+'" (click)="updateStatusAll(1,\''+str(serializer_row['id'])+'\')" mdTooltip="Block Record"><span class="icon-check-box"></span></a>'
                #####################Table Based Nesting#################################
                try:
                    if table_name !='EngageboostOrdermaster':
                        row_dict['created'] = get_date_from_datetime(serializer_row['created'],global_setting_zone,global_setting_date)
                except:
                    pass
                if len(row_dict)>0:
                    row_dict['action']=action
                    row.append(row_dict)
            #####################Action Links#################################
            if add=='Y':
                #Popup/page setup start here....
                if is_popup=='y':
                    if table_name=='EngageboostCurrencyMasters':
                        add_link='<a class="md-button btn-main mat-button" href="javascript:void(0)" popup-box init-fn="add_edit_load(arg1)" box-template="static/pages/'+str(folder)+'/add_'+str.lower(module)+'.html" elem-id="#add_'+str.lower(module)+'_pop"> Manage Excahnge Rate ''</a>'
                    else:
                        add_link='<a class="md-button btn-main mat-button" href="javascript:void(0)" popup-box init-fn="add_edit_load(arg1)" box-template="static/pages/'+str(folder)+'/add_'+str.lower(module)+'.html" elem-id="#add_'+str.lower(module)+'_pop">+ Add '+str(layout_module)+'</a>'
                else:
                    if table_name=='EngageboostDiscountMasters':
                        add_link='<button md-button ng-reflect class="md-button btn-main mat-button" href="#/'+str.lower(link)+'/add/'+str(menu_link)+'" (click)="globalService.addTab(\''+str.lower(link)+''+str(menu_link)+'add''\',\''+str.lower(link)+'/add/'+str(menu_link)+'\',\'Add '+str(layout_module)+'\',tabs[selectedTab].id)">+ Add '+str(layout_module)+'</button>'
                    else:
                        add_link='<button md-button ng-reflect class="md-button btn-main mat-button" href="#/'+str.lower(link)+'/add" (click)="globalService.addTab(\''+str.lower(link)+'add''\',\''+str.lower(link)+'/add\',\'Add '+str(layout_module)+'\',tabs[selectedTab].id)">+ Add '+str(layout_module)+'</button>'
                #Popup/page setup end here....
            else:
                add_link='<a class="md-button btn-main compile" href="javascript:void(0)" ng-click="$root.showAlertBox(\'Permission Error\',\'You have no permission to add\')">+ Add '+str(layout_module)+'</a>'
            add_btn=add_link
            pre_data={}
            final_data=[]
            tag_list=[]
            pre_data['result']=row
            pre_data['all']=result_all
            pre_data['inactive']=result1
            pre_data['active']=result2
            pre_data['layout']=layouts['layout']
            pre_data['applied_layout']=layouts['applied_layout']
            pre_data['role_permission']=role_permission
            pre_data['add_btn']=add_link
            #####################Active/Inacative#################################
            #####################Final Result#################################
            final_data.append(pre_data)
            delivery_slot_data = []
            api_status = []
            if show_all == 0:
                return self.get_paginated_response(final_data)
            else:
                serializer = serializer_class(result, many=True)
                # serializer.data["tag_list"]=tag_list
                return Response(final_data)

class GridLayout(generics.ListAPIView):
    def post(self, request, format=None):
        #####################Layout#################################
        company_db = loginview.db_active_connection(request)
        table_name = request.data.get('model')
        model = apps.get_model('webservices',table_name)
        screen_name = request.data.get('screen_name')
        visibility_id = ""
        if "visibility_id" in request.data.keys():
            visibility_id = request.data.get('visibility_id')
        userid = request.data.get('userid')
        result = model.objects.using(company_db).all().order_by('-id').filter(isdeleted='n')
        if visibility_id!="" and visibility_id!=None:
            result = result.filter(visibility_id=visibility_id)

        result_all = result.count()
        result_inactive = result.filter(isblocked='y').count()
        result_active = result.filter(isblocked='n').count()

        users = EngageboostUsers.objects.using(company_db).get(id=userid)
        role_id = users.role_id
        issuperadmin = users.issuperadmin

        menu_id = 0;
        module = table_name.replace("Engageboost", "")
        menu_fetch = EngageboostMenuMasters.objects.using(company_db).get(module=module)
        if menu_fetch:
            menu_id=menu_fetch.id

        if issuperadmin=='Y':
            add='Y'
            edit='Y'
            delete='Y'
            status='Y'
            role_permission={"add":"Y","edit":"Y","delete":"Y","view":"Y","block":"Y","import_field":0,"export":0,"shipping_processes":0,"print":0}
        else:
            role_per = EngageboostRoleMenuPermissions.objects.using(company_db).get(role_id=role_id,master_id=menu_id,isblocked=0,isdeleted=0)
            role_permission={"add":role_per.add,"edit":role_per.edit,"delete":role_per.delete,"view":role_per.view,"block":role_per.block,"import_field":role_per.import_field,"export":role_per.export,"shipping_processes":role_per.shipping_processes,"print":role_per.print}

        settings = EngageboostGlobalSettings.objects.get(isdeleted='n',isblocked='n',website_id=1)
        page_size=settings.itemlisting_backend

        layouts = common.fetch_grid_layout(request,module,screen_name)
        data = {
            "results":[{
                "all":result_all,
                "inactive":result_inactive,
                "active":result_active,
                "role_permission":role_permission,
                "layout":layouts['layout'],
                "applied_layout":layouts['applied_layout']
            }],
            "page_size":page_size
        }
        return Response(data)
        #####################Layout#################################

class AdvancedFilter(generics.ListAPIView):
    def post(self, request, format=None):
        #####################Layout#################################
        try:
            table_name = request.data.get('model')
            model = apps.get_model('webservices',table_name)
            module = table_name.replace("Engageboost", "")
            try:
                screen_name = request.data.get('screen_name')
                if screen_name=="" or screen_name==None:
                    screen_name ="list"
            except:
                screen_name = "list"

            try:
                exclude_list = request.data.get('exclude')
                if exclude_list=="" or exclude_list==None:
                    exclude_list =[]
            except:
                exclude_list = []
            # print(table_name+' '+screen_name)
            website_id = request.data.get('website_id')

            modulename = EngageboostAdvancedSearchModules.objects.filter(screen_name=screen_name,module=module,isdeleted="n",isblocked="n")
            # modulename = modulename.filter(website_id=website_id)
            filters = []
            if modulename.count()>0:
                modulename_result = modulename.first()
                layouts = EngageboostAdvancedSearchLayouts.objects.filter(module_id=modulename_result.id,isdeleted="n",isblocked="n")
                try:
                    key = request.data.get('search')
                    layouts = layouts.filter(columns__icontains=key)
                except:
                    pass
                try:
                    layouts = layouts.exclude(id__in=exclude_list)
                except:
                    pass

                layouts = layouts.order_by("columns")

                if layouts.count()>0:
                    result = layouts.values("id","columns","field","input_type","field_type","url","search_module","title_field_name").all()
                    filters.append(result)

                    data = {
                        "status":1,
                        "api_status":filters,
                        "msg":""
                    }
                else:
                    data = {
                        "status":0,
                        "api_status":[],
                        "msg":"No filters found"
                    }
            else:
                data = {
                    "status":0,
                    "api_status":[],
                    "msg":"No filters found"
                }

        except Exception as error:
            data = {
                "status":0,
                "api_status":[],
                "msg":"No filters found"
            }
        return Response(data)
        #####################Layout#################################


def get_serializer_class(self,table_name):
    if table_name=='EngageboostUsers':
        return UserSerializer
    elif table_name=='EngageboostGroups':
        return GroupSerializer
    elif table_name=='EngageboostRolemasters':
        return RoleSerializer
    elif table_name=='EngageboostCategoryMasters':
        return CategoriesSerializer
    elif table_name=='EngageboostHsnCodeMaster':
        return HsnCodeMasterSerializer
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
        # return OrderMasterSerializer
        return OrderMasterSerializerList
    elif table_name=='EngageboostOrderProducts':
        return OrderProductsSerializer
    elif table_name=='EngageboostTrentPicklists':
        return TrentPicklistsSerializer
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
    elif table_name=='EngageboostShippingMastersSettings':
        return ShippingMastersSettingsSerializer
    elif table_name=='EngageboostFedexZipcodes':
        return FedexZipcodesSerializer
    elif table_name=='EngageboostTags':
        return TagsSerializer
    elif table_name=='EngageboostAwbMasters':
        return AwbMastersSerializer
    elif table_name=='EngageboostShipments':
        return ShipmentsSerializer
    elif table_name =='EngageboostZoneMasters':
        return ZoneMastersSerializer
    elif table_name == 'EngageboostVehicleMasters':
        return VehicleMasterSerializer
    elif table_name == 'EngageboostDeliveryManagers':
        return DeliveryManagerSerializer
    elif table_name == 'EngageboostDeliverySlot':
        return DeliverySlotSerializer
    elif table_name == 'EngageboostPriceFormula':
        return PriceFormulaSerializer
    elif table_name == 'EngageboostCreditPoint':
        return EngageboostCreditPointSerializer
    elif table_name == 'EngageboostCreditPointConditions':
        return EngageboostCreditPointConditionsSerializer
    elif table_name == 'EngageboostProductTaxClasses':
        return ProducttaxclassesSerializer
    elif table_name == 'EngageboostCustomerTaxClasses':
        return CustomerTaxClassesSerializer
    elif table_name == 'EngageboostTaxRates':
        return TaxratesSerializer
    elif table_name == 'EngageboostTaxRuleTables':
        return TaxRuleTablesSerializer
    elif table_name == 'EngageboostMultipleBarcodes':
        return MultipleBarcodeSerializer
    elif table_name == 'EngageboostGiftCardMasters':
        return GiftCardMastersSerializer
    elif table_name=='EngageboostPages':
        return PagesSerializer
    elif table_name=='EngageboostCategoryBanners':
        return CategoryBannersSerializer
    elif table_name=='EngageboostLanguages':
        return LanguageSerializer
    elif table_name=='EngageboostTemplateIndustryMasters':
        return TemplateIndustryMastersSerializer

def get_zoneserializers(screen_name):
    if screen_name == 'list_zone':
        return ZoneMastersZoneSerializer
    elif screen_name == 'list_area':
        return ZoneMastersAreaSerializer
    elif screen_name == 'list_subarea':
        return ZoneMastersSubAreaSerializer

def get_search_filter(self,table_name,key):
    if table_name=='EngageboostUsers':
        return (Q(role__name__icontains=key)|Q(first_name__icontains=key)|Q(last_name__icontains=key)|Q(email__icontains=key)|Q(business_name__icontains=key)|Q(employee_name__icontains=key)|Q(designation__icontains=key)|Q(city__icontains=key)|Q(state__icontains=key)|Q(postcode__icontains=key)|Q(phone__icontains=key)|Q(username__icontains=key))
    elif table_name=='EngageboostMultipleBarcodes':
        return (Q(barcode__icontains=key))
    elif table_name=='EngageboostGroups':
        return (Q(name__icontains=key))
    elif table_name=='EngageboostRolemasters':
        return (Q(name__icontains=key))
    elif table_name=='EngageboostCategoryMasters':
        return (Q(name__icontains=key)|Q(description__icontains=key)|Q(meta_keywords__icontains=key)|Q(page_title__icontains=key)|Q(meta_description__icontains=key)|Q(category_url__icontains=key)|Q(display_order__icontains=key))
    elif table_name=='EngageboostHsnCodeMaster':
        return (Q(hsn_code__icontains=key)|Q(sgst__icontains=key)|Q(cgst__icontains=key)|Q(igst__icontains=key)|Q(cess__icontains=key))
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
    elif table_name=='EngageboostTrentPicklists':
        return (Q(trents_picklist_no__icontains=key)|Q(picklist_status__icontains=key))
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
        return (Q(currencyname__icontains=key)|Q(currency__icontains=key)|Q(currencysymbol__icontains=key))
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
    elif table_name=='EngageboostTags':
        return (Q(tag_name__icontains=key))
    elif table_name=='EngageboostAwbMasters':
        return (Q(awb_number__icontains=key))
    elif table_name =='EngageboostZoneMasters':
        return (Q(name__icontains=key)| Q(zipcode__icontains=key))
    elif table_name =='EngageboostGiftCardMasters':
        return (Q(card_name__icontains=key)| Q(card_number__icontains=key))
    elif table_name=='EngageboostVehicleMasters':
        return (Q(vehicle_name__icontains=key)|Q(vehicle_number__icontains=key)|Q(model_no__icontains=key)|Q(zip_code__icontains=key)|Q(phone_number__icontains=key)|Q(city__icontains=key))
    elif table_name == 'EngageboostDeliveryManagers':
        return (Q(name__icontains=key)|Q(phone__icontains=key)|Q(email__icontains=key)|Q(zone__icontains=key)|Q(created__icontains=key))
    elif table_name == 'EngageboostCreditPoint':
        return (Q(name__icontains=key)|Q(loyalty_desc__icontains=key)|Q(points__icontains=key)|Q(per_rupees__icontains=key))
    elif table_name == "EngageboostPriceFormula":
        return (Q(formulla_name__icontains=key)|Q(price_name__icontains=key)|Q(condition__icontains=key)|Q(margin__icontains=key)|Q(formulla_type__icontains=key))
    elif table_name=='EngageboostPages':
        return (Q(page_name__icontains=key)|Q(page_title__icontains=key)|Q(url__icontains=key))
    elif table_name=='EngageboostLanguages':
        return (Q(name__icontains=key)|Q(lang_code__icontains=key))
    elif table_name=='EngageboostProductTaxClasses':
        return (Q(name__icontains=key))
    elif table_name=='EngageboostCustomerTaxClasses':
        return (Q(tax_class_name__icontains=key))
    elif table_name=='EngageboostTaxRates':
        return (Q(name__icontains=key)|Q(percentage__icontains=key)|Q(tax_type__icontains=key)|Q(apply__icontains=key))
    elif table_name=='EngageboostTaxRuleTables':
        return (Q(rule_name__icontains=key)|Q(priority__icontains=key))
    elif table_name=='EngageboostCategoryBanners':
        return (Q(banner_name__icontains=key)|Q(banner_description__icontains=key)|Q(applicable_for__icontains=key))
    elif table_name=='EngageboostWarehouseManager':
        return (Q(manager__username__icontains=key))

def get_time(gettime, zone, date):
    try:
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
    except:
        return ""

def get_date(gettime,zone,date):
    import datetime
    gettime = str(gettime)
    format1 = date.date_format
    datetime_object=datetime.datetime.strptime(gettime, '%Y-%m-%d').strftime(format1)
    return datetime_object

def get_date_from_datetime(gettime, zone, date):
    gettime = str(gettime)
    date_format = date.date_format
    db_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    gettime = datetime.datetime.strptime(gettime, db_format)
    datetime_object = gettime.strftime(date_format)
    return datetime_object

def get_dayname_from_datetime(gettime, zone, date):
    gettime = str(gettime)
    db_format = date.date_format
    gettime = datetime.datetime.strptime(gettime, db_format)
    datetime_object = gettime.strftime("%A")
    return datetime_object