from webservices.models import EngageboostProducts
from django.http import Http404
from webservices.serializers import BasicinfoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime, timedelta, date
from datetime import datetime
from rest_framework import generics
from itertools import chain
from django.core import serializers
from django.http import HttpResponse
from webservices.views import loginview
from webservices.models import *
from webservices.serializers import *
from django.db.models import Q
from django.db.models.aggregates import Aggregate
from django.contrib.postgres.aggregates import *
from django.db.models import F,Count,Sum,Avg,FloatField,Case,When,IntegerField
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractWeek,ExtractWeekDay, ExtractYear, TruncDate, TruncDay, TruncHour, TruncMinute, TruncSecond, TruncMonth
from dateutil.relativedelta import relativedelta
import sys
import traceback
import json

class productDetailsSummary(generics.ListAPIView):
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostProducts.objects.using(company_db).get(pk=pk)
        except EngageboostProducts.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        postdata = request.data
        try:
            pk = postdata['product_id']
            today = datetime.today()
            # Total Sale
            rs_sale = EngageboostOrderProducts.objects.filter(product_id = pk)
            try:
                warehouse_id = postdata['warehouse_id']
                if warehouse_id != "" and warehouse_id != None:
                    rs_sale = rs_sale.filter(order_id__assign_wh=warehouse_id)
            except:
                pass

            try:
                end_date = postdata['end_date']
                try:
                    end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                except:
                    end_date = datetime.strptime(end_date, "%Y-%m-%d")
                end_date = end_date.strftime("%Y-%m-%d")
            except:
                end_date = today
                end_date = end_date.strftime("%Y-%m-%d")

            try:
                start_date = postdata['start_date']
                try:
                    start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                except:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d")
                start_date = start_date.strftime("%Y-%m-%d")
            except:
                start_date = today+relativedelta(days=-30)
                start_date = start_date.strftime("%Y-%m-%d")    

            rs_sale     = rs_sale.filter(created__range=[start_date, end_date])    
            rs_sale     = rs_sale.values('product_id').annotate(
                    total_sale=Sum(F('product_price_base')*F('quantity'),output_field = FloatField()), 
                    total_discount=Sum(F('product_discount_price_base')*F('quantity'),output_field = FloatField()), 
                    total_cancel_amount=Sum(F('product_price_base')*F('deleted_quantity'),output_field = FloatField()), 
                    total_cancel_discount_amount=Sum(F('product_discount_price_base')*F('deleted_quantity'),output_field = FloatField()))
            total_sale = 0
            if rs_sale:
                total_sale = rs_sale[0]['total_sale']
            
            # Customer count
            rs_customer = EngageboostOrderProducts.objects.filter(product_id = pk).values('order_id__customer_id')
            try:
                warehouse_id = postdata['warehouse_id']
                if warehouse_id!="" and warehouse_id!=None:
                    rs_customer = rs_customer.filter(order_id__assign_wh=warehouse_id)
            except:
                pass
            rs_customer = rs_customer.filter(created__range=[start_date, end_date]) 
            rs_customer = rs_customer.distinct().count()   
            
            # Stock Details
            rs_stock    = EngageboostProductStocks.objects.filter(product_id=pk).values('product_id').annotate(tot_stock=Sum('stock'),tot_real_stock=Sum('real_stock'),tot_virtual_stock=Sum('virtual_stock'), tot_safety_stock=Sum('safety_stock'))
            try:
                warehouse_id = postdata['warehouse_id']
                if warehouse_id != "" and warehouse_id!=None:
                    rs_stock = rs_stock.filter(warehouse_id=warehouse_id)
            except:
                pass
            # rs_stock = rs_stock.filter(created__range=[start_date, end_date])

            tot_stock           = 0
            tot_real_stock      = 0
            tot_virtual_stock   = 0
            tot_safety_stock    = 0
            if rs_stock:
                tot_stock           = rs_stock[0]['tot_stock']
                tot_real_stock      = rs_stock[0]['tot_real_stock']
                tot_virtual_stock   = rs_stock[0]['tot_virtual_stock']
                tot_safety_stock    = rs_stock[0]['tot_safety_stock']
            
            # Visitors Count
            rs_product  = EngageboostProducts.objects.filter(id=pk).values('name', 'slug').first()
            slug = rs_product['slug']
            rs_visitors     = EngageboostTrafficReportsPages.objects.filter(pagepath__icontains=slug).count()

            data = {
                "total_sale":total_sale,
                "total_customer":rs_customer,
                "tot_stock": tot_stock,
                "tot_real_stock": tot_real_stock,
                "tot_virtual_stock": tot_virtual_stock,
                "tot_safety_stock": tot_safety_stock,
                "tot_visitors":rs_visitors,
                "start_date":start_date,
                "end_date":end_date
            }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

class productDetailsSummarySalesReportGraph(generics.ListAPIView):
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostProducts.objects.using(company_db).get(pk=pk)
        except EngageboostProducts.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        postdata = request.data
        try:
            #  Sale Graph
            pk = postdata['product_id']
            today       = datetime.today()
            # Total Sale
            rs_sale     = EngageboostOrderProducts.objects.filter(product_id = pk)

            try:
                warehouse_id = postdata['warehouse_id']
                if warehouse_id!="" and warehouse_id!=None:
                    rs_sale = rs_sale.filter(order_id__assign_wh=warehouse_id)
            except:
                pass

            try:
                end_date = postdata['end_date']
                try:
                    end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                except:
                    end_date = datetime.strptime(end_date, "%Y-%m-%d")
                end_date = end_date.strftime("%Y-%m-%d")
            except:
                end_date = today
                end_date = end_date.strftime("%Y-%m-%d")

            try:
                start_date = postdata['start_date']
                try:
                    start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                except:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d")
                start_date = start_date.strftime("%Y-%m-%d")
            except:
                start_date = today+relativedelta(days=-30)
                start_date = start_date.strftime("%Y-%m-%d")    

            rs_sale     = rs_sale.filter(created__range=[start_date, end_date])
            # print("==============",start_date, end_date,rs_sale.query)
            rs_sales    = rs_sale.annotate(weekly_day=TruncDay('created')).values('weekly_day').annotate(total_sale=Sum(F('product_price')*F('quantity'),output_field = FloatField())).order_by("weekly_day")

            if rs_sales:
                for rc_date in rs_sales:
                    rc_date['day']=rc_date['weekly_day'].strftime("%A")

                data = {
                    "api_status":1,
                    "dated":str(start_date)+' - '+str(today),
                    "data":rs_sales
                }
            else:
                data = {
                    "api_status":0,
                    "dated":str(start_date)+' - '+str(today),
                    "data":[]
                }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}        
        return Response(data)

class productDetailsMarketplaceReportGraph(generics.ListAPIView):
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostProducts.objects.using(company_db).get(pk=pk)
        except EngageboostProducts.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        postdata = request.data
        try:
            #  Sale Graph
            pk = postdata['product_id']
            today       = datetime.today()
            # Total Sale
            rs_sale     = EngageboostOrderProducts.objects.filter(product_id = pk)

            try:
                warehouse_id = postdata['warehouse_id']
                if warehouse_id!="" and warehouse_id!=None:
                    rs_sale = rs_sale.filter(order_id__assign_wh=warehouse_id)
            except:
                pass

            try:
                end_date = postdata['end_date']
                try:
                    end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                except:
                    end_date = datetime.strptime(end_date, "%Y-%m-%d")
                end_date = end_date.strftime("%Y-%m-%d")
            except:
                end_date = today
                end_date = end_date.strftime("%Y-%m-%d")

            try:
                start_date = postdata['start_date']
                try:
                    start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                except:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d")
                start_date = start_date.strftime("%Y-%m-%d")
            except:
                start_date = today+relativedelta(days=-30)
                start_date = start_date.strftime("%Y-%m-%d")    

            rs_sale     = rs_sale.filter(created__range=[start_date, end_date])

            rs_sales    = rs_sale.filter(product_id = pk, created__range=[start_date, end_date]).values('order__webshop_id', 'order__webshop_id__name').annotate(total_sale=Sum(F('product_price')*F('quantity'),output_field = FloatField()))
            if rs_sales:
                data = {
                    "api_status":1,
                    "dated":str(start_date)+' - '+str(today),
                    "data":rs_sales
                }
            else:
                data = {
                    "api_status":0,
                    "dated":str(start_date)+' - '+str(today),
                    "data":[]
                }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}        
        return Response(data)

class productDetailsVisitorsReportGraph(generics.ListAPIView):
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostProducts.objects.using(company_db).get(pk=pk)
        except EngageboostProducts.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        postdata = request.data
        try:
            pk = postdata['product_id']
            today = datetime.today()
            
            try:
                end_date = postdata['end_date']
                try:
                    end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                except:
                    end_date = datetime.strptime(end_date, "%Y-%m-%d")
                end_date = end_date.strftime("%Y-%m-%d")
            except:
                end_date = today
                end_date = end_date.strftime("%Y-%m-%d")

            try:
                start_date = postdata['start_date']
                try:
                    start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                except:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d")
                start_date = start_date.strftime("%Y-%m-%d")
            except:
                start_date = today+relativedelta(days=-30)
                start_date = start_date.strftime("%Y-%m-%d")    

            rs_product  = EngageboostProducts.objects.filter(id=pk).values('name', 'slug').first()
            slug = rs_product['slug']
            
            rs_sales    = EngageboostTrafficReportsPages.objects.filter(pagepath__icontains=slug, date__range=[start_date, end_date]).values('date').annotate(total=Count('id'))
            if rs_sales:
                data = {
                    "api_status":1,
                    "dated":str(start_date)+' - '+str(end_date),
                    "data":rs_sales
                }
            else:
                data = {
                    "api_status":0,
                    "dated":str(start_date)+' - '+str(end_date),
                    "data":[]
                }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
        return Response(data)

class productDetailsStockReportGraph(generics.ListAPIView):
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostProducts.objects.using(company_db).get(pk=pk)
        except EngageboostProducts.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        postdata = request.data
        try:
            pk = postdata['product_id']
            today = datetime.today()
            
            try:
                end_date = postdata['end_date']
                try:
                    end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                except:
                    end_date = datetime.strptime(end_date, "%Y-%m-%d")
                end_date = end_date.strftime("%Y-%m-%d")
            except:
                end_date = today
                end_date = end_date.strftime("%Y-%m-%d")

            try:
                start_date = postdata['start_date']
                try:
                    start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                except:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d")
                start_date = start_date.strftime("%Y-%m-%d")
            except:
                start_date = today+relativedelta(days=-30)
                start_date = start_date.strftime("%Y-%m-%d")

            rs_product  = EngageboostProducts.objects.filter(id=pk).values('id').first()
            p_id = rs_product['id']
            rs_sales     = EngageboostProductStocks.objects.filter(product_id=p_id, created__range=[start_date, end_date]).values('created').annotate(total=Sum('real_stock'))
            
            try:
                warehouse_id = postdata['warehouse_id']
                if warehouse_id!="" and warehouse_id!=None:
                    rs_sale = rs_sale.filter(warehouse_id=warehouse_id)
            except:
                pass

            # print(rs_sales.query)
            if rs_sales:
                data = {
                    "api_status":1,
                    "dated":str(start_date)+' - '+str(end_date),
                    "data":rs_sales
                }
            else:
                data = {
                    "api_status":0,
                    "dated":str(start_date)+' - '+str(end_date),
                    "data":[]
                }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}        
        return Response(data)


#GET PRODUCT SUPPLIERS USING PRODUCT ID       
class ProductSuppliers(generics.ListAPIView):
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostProducts.objects.using(company_db).get(pk=pk)
        except EngageboostProducts.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        # try:
        dis = self.get_object(pk,request)
        suppliers_id = EngageboostWarehouseSupplierMappings.objects.filter(product_id=pk,isdeleted='n',isblocked='n').annotate(no_of_warehouse=Count('warehouse_id')).order_by("-no_of_warehouse").values("supplier_id")
        
        try:
            warehouse_id = postdata['warehouse_id']
            if warehouse_id!="" and warehouse_id!=None:
                suppliers_id = suppliers_id.filter(warehouse_id=warehouse_id)
        except:
            pass

        suppliers = EngageboostSuppliers.objects.using(company_db).filter(isdeleted='n',isblocked='n',id__in=suppliers_id)[:7]
        serializer = SuppliersSerializer(suppliers,many=True)
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
        # except:
        #     data ={
        #         'status':0,
        #         'api_status':"",
        #         'message':'Data Not Found',
        #     }        
        return Response(data)
#GET PRODUCT PROMOTION USING PRODUCT ID
class ProductPromotion(generics.ListAPIView):
    def get_object(self, pk, request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostProducts.objects.using(company_db).get(pk=pk)
        except EngageboostProducts.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None, partial=True):
        company_db = loginview.db_active_connection(request)
        dis = self.get_object(pk, request)
        conditions_list= EngageboostDiscountMastersConditions.objects.filter(Q(all_product_id__startswith=str(pk)+",")|Q(all_product_id__endswith=","+str(pk))|Q(all_product_id__contains=","+str(pk)+",")|Q(all_product_id=pk)).values("discount_master_id")
        promotion_list= EngageboostDiscountMasters.objects.using(company_db).filter(isblocked='n', isdeleted='n',id__in=conditions_list)[:7]
        
        serializer = DiscountMasterSerializer(promotion_list, many=True)
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
#GET TOP CUSTOMERS USING PRODUCT ID
class TopCustomers(generics.ListAPIView):
    def get_object(self, pk, request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostProducts.objects.using(company_db).get(pk=pk)
        except EngageboostProducts.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None, partial=True):
        company_db = loginview.db_active_connection(request)
        dis = self.get_object(pk, request)
        top_customers= EngageboostCustomers.objects.using(company_db).filter(isblocked='n', isdeleted='n')[:7]
        serializer = CustomerSerializer(top_customers, many=True)
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

#GET ACTIVITY USING PRODUCT ID
class ProductActivity(generics.ListAPIView):
    def get(self, request, pk, format=None, partial=True):
        website_id = 1
        
        orders = EngageboostOrderProducts.objects.filter(product_id=pk).values("order_id").order_by("id")

        try:
            warehouse_id = postdata['warehouse_id']
            if warehouse_id!="" and warehouse_id!=None:
                orders = orders.filter(order_id__assign_wh=warehouse_id)
        except:
            pass

        rs_order1 = EngageboostOrderActivity.objects.filter(order_id__in=orders).distinct("activity_comments","order_id").values("id")[:15]
        rs_order = EngageboostOrderActivity.objects.filter(id__in=rs_order1).order_by('-id')
        # print(rs_order.query)
        serializer = ProductActivitySerializer(rs_order,many=True)

        if serializer: 
            data ={
                'status':1,
                'api_status':serializer.data,
                'message':'',
            }
        else:
            data ={
                'status':0,
                'api_status':[],
                'message':'Data Not Found',
            }
        return Response(data)

#GET RAC NO USING PRODUCT ID
class ProductRACNO(generics.ListAPIView):
    def get(self, request, pk, format=None, partial=True):
        website_id = 1
        
        orders = EngageboostPurchaseOrderReceivedProducts.objects.filter(product_id=pk).values("purchase_order_received_id").order_by("id")

        rs_order = EngageboostPurchaseOrderReceivedProductDetails.objects.filter(purchase_order_received_id__in=orders).order_by('-id')
        # print(rs_order.query)
        serializer = EngageboostPurchaseOrderReceivedProductDetailsSerializer(rs_order,many=True)

        if serializer: 
            data ={
                'status':1,
                'api_status':serializer.data,
                'message':'',
            }
        else:
            data ={
                'status':0,
                'api_status':[],
                'message':'Data Not Found',
            }
        return Response(data)                
