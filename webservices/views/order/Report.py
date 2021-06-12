from django.db.models import Value
from django.db.models.functions import Concat
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import status
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from rest_framework.parsers import JSONParser
import datetime
from rest_framework import generics
# from itertools import chain
from django.core import serializers
# from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from webservices.views import loginview
from webservices.views.common import common
from webservices.views.emailcomponent import emailcomponent
from django.db.models import Q
import sys,math
import traceback
import json
from django.contrib.auth.hashers import make_password

import datetime
from datetime import timedelta
from django.db.models import TimeField
from django.db.models import Avg, Max, Min, Sum, Count

from webservices.models import *
from webservices.serializers import *


# $Reports = new ReportsController();
# $Reports->insert_report_date($website_id);
# $Reports->insert_report_customer($order_data['OrderList']['customer_id'],$website_id);
# $Reports->insert_report_order($order_id,$website_id);
# $Reports->insert_report_product($all_product_ids,$website_id);



def insert_report_date(websiteId=1,deleted_date = None):
    # $this->layout = '';
    # //$websiteId = $this->Session->read('Company.defaultwebsite.id');
    IorderByStr 		= " InvoiceMaster__created_date "
    OorderByStr 		= " OrderList__created_date"
    ShiporderByStr 	    = " OrderList__created_date"
    CorderByStr 		= " OrderList__reated_date"
    IgroupByStr 		= " InvoiceMaster__created_date"
    OgroupByStr 		= " OrderList__created_date"
    CgroupByStr 		= " OrderList.created_date"
    now 	= datetime.now()
    to_day = datetime.now().strftime('%Y-%m-%d')
    to_day = '2019-03-29'

    # $Ifields = "concat(DATE_FORMAT(InvoiceMaster.created_date,'%Y-%m-%d')) as created_date,sum(InvoiceMaster.gross_amount) as invoiced_amount ";
    # $Ofields = "count(distinct(OrderList.id)) as no_of_order, concat(DATE_FORMAT(OrderList.created_date,'%Y-%m-%d'))  as created_date,concat(YEAR(OrderList.created_date)) as cfield, sum(OrderList.gross_amount_base) as gross_amount ,sum(OrderList.net_amount_base) as net_amount, sum(OrderList.shipping_cost_base) as shipping_cost, sum( OrderList.gross_discount_amount_base) as gross_discount_amount";
    # $cfields = "concat(DATE_FORMAT(OrderList.created_date,'%Y-%m-%d'))   as created_date,sum(OrderProduct.deleted_quantity) as cancelled_quantity, (sum(OrderProduct.quantity) -  sum(OrderProduct.deleted_quantity) )as total_sold, SUM(OrderProduct.product_price_base*OrderProduct.deleted_quantity) as cancelled_amount";

    # $IsearchCondition	= " InvoiceMaster.website_id=".$websiteId." AND date(InvoiceMaster.created_date) = '".date('Y-m-d')."'";
    # $OsearchCondition	= " OrderList.buy_status='1' AND OrderList.order_status != '2' AND OrderList.website_id=".$websiteId." AND date(OrderList.created_date) = '".date('Y-m-d')."'";//exit;
    # $cancelledCon 		= " OrderList.buy_status='1' AND OrderList.website_id=".$websiteId." AND date(OrderList.created_date) = '".date('Y-m-d')."'";
    # $Invoicedata 		= $this->InvoiceMaster->find('all',array('conditions'=>"1 AND ".$IsearchCondition." ",'fields'=> $Ifields, 'order' => $IorderByStr, 'group' => $IgroupByStr ));
    # $Orderdata 		= $this->OrderList->find('all',array('conditions'=>"1 AND ".$OsearchCondition." ",'fields'=> $Ofields, 'order' => $OorderByStr, 'group' => $OgroupByStr ));
    # //$this->pr_exit($Orderdata);

   
    Invoicedata = EngageboostInvoicemaster.objects.filter(website_id=1, created_date__date = to_day).all().annotate(invoiced_amount=Sum('gross_amount')).values('gross_amount')
    Orderdata = EngageboostOrdermaster.objects.filter(website_id=1, buy_status=1, created__date = to_day ).exclude(order_status=2).values('company_id').annotate(no_of_order=Count('id'), total_gross_amount=Sum('gross_amount_base'), total_net_amount=Sum('net_amount_base'),total_shipping_cost = Sum('shipping_cost_base'), total_gross_discount_amount= Sum('gross_discount_amount_base'))
    

    # $deleteddata 	= $this->OrderProduct->find('all',array('conditions'=>"1 AND ".$cancelledCon." ",'fields'=> $cfields, 'order' => $CorderByStr, 'group' => $CgroupByStr ));
    # cfields = "concat(DATE_FORMAT(OrderList.created_date,'%Y-%m-%d'))   as created_date, (sum(OrderProduct.quantity) -  sum(OrderProduct.deleted_quantity) )as total_sold, SUM(OrderProduct.product_price_base*OrderProduct.deleted_quantity) as cancelled_amount";

    deleteddata = EngageboostOrderProducts.objects.filter(order__buy_status=1, order__website_id=1, order__created__date = to_day).annotate(cancelled_quantity=Sum('deleted_quantity')).values('warehouse_id')

    newInvoicedata =  {}
    newOrderdata =  []
    newdeleteddata =  {}

    if Invoicedata:
        for invoice_data in Invoicedata:
            newInvoicedata.update({'created_date':to_day})

    if Orderdata:
        for order_data in Orderdata:
            newOrderdata.append(order_data)

    if deleteddata:
        for delete_data in deleteddata:
            newdeleteddata.update({to_day:delete_data})

    dateReportArr = {}

#     foreach($newInvoicedata as $newInvoicedataKey=>$newInvoicedataVal)
#     {
#         $dateReportArr[$newInvoicedataKey]['invoiced_amount'] = $newInvoicedataVal['invoiced_amount'];
#         $dateReportArr[$newInvoicedataKey]['created_date'] = $newInvoicedataVal['created_date'];
#     }

    if newInvoicedata:
        for newinv_data in newInvoicedata:
            dateReportArr.update({'invoiced_amount':newInvoicedata['invoiced_amount'], 'created_date':to_day})


#     foreach($newOrderdata as $newOrderdataKey=>$newOrderdataVal)
#     {
#         $dateReportArr[$newOrderdataKey]['gross_amount'] = $newOrderdataVal['gross_amount'];
#         $dateReportArr[$newOrderdataKey]['net_amount'] = $newOrderdataVal['net_amount'];
#         $dateReportArr[$newOrderdataKey]['shipping_cost'] = $newOrderdataVal['shipping_cost'];
#         $dateReportArr[$newOrderdataKey]['gross_discount_amount'] = $newOrderdataVal['gross_discount_amount'];
#         $dateReportArr[$newOrderdataKey]['created_date'] = $newOrderdataVal['created_date'];
#         $dateReportArr[$newOrderdataKey]['no_of_order'] = $newOrderdataVal['no_of_order'];
#     }
    if newOrderdata:
        for newOrder_data in newOrderdata:
            pass
            # printj(newOrder_data)

#     foreach($newdeleteddata as $newdeleteddataKey=>$newdeleteddataVal)
#     {
#         $dateReportArr[$newdeleteddataKey]['cancelled_quantity'] = $newdeleteddataVal['cancelled_quantity'];
#         $dateReportArr[$newdeleteddataKey]['total_sold'] = $newdeleteddataVal['total_sold'];
#         $dateReportArr[$newdeleteddataKey]['cancelled_amount'] = $newdeleteddataVal['cancelled_amount'];
#         $dateReportArr[$newdeleteddataKey]['created_date'] = $newdeleteddataVal['created_date'];
#     }
    finaldateArray = {}
#     # // First delete All data for that date
    if newOrderdata:
        print("k1")
        print(to_day)
        for datareport_arr in newOrderdata:
            finaldateArray.update({"invoiced_amount":0})
            finaldateArray.update({"gross_amount":datareport_arr['total_gross_amount']})
            finaldateArray.update({"net_amount":0})
            finaldateArray.update({"shipping_amount":0})
            finaldateArray.update({"discount":0})
            finaldateArray.update({"cancelled_quantity":0})
            finaldateArray.update({"total_sold":0})
            finaldateArray.update({"no_of_order":datareport_arr['no_of_order']})
            finaldateArray.update({"cancelled_amount":0})
            finaldateArray.update({"avg_order_price":0})
            finaldateArray.update({"website_id":0})
            finaldateArray.update({"date":to_day})
            
            # EngageboostReportDate.objects.filter(date = to_day).delete()
            # EngageboostReportDate.objects.create(**finaldateArray)


class testreport(generics.ListAPIView):

    def post(self, request, *args, **kwargs):
        company_db = loginview.db_active_connection(request)
        insert_report_date()
        # print(activity_details)
        data = {
            "status":1,
            # "data":activity_details
        }

        return Response(data)




def printj(jsn):
	print(json.dumps(jsn, indent=4, sort_keys=True))
