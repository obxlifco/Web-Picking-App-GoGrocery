from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics,viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime, timedelta
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from webservices.views import loginview
from webservices.models import *
from webservices.serializers import *
import datetime,time
from rest_framework.authtoken.models import Token
import base64
import sys,math
import traceback
from django.db.models import Count, Sum, Avg
from django.db.models.aggregates import Aggregate
from django.contrib.postgres.aggregates import *
from django.db.models import F,Count,Sum,Avg,FloatField,Case,When,IntegerField
from django.db.models.functions import TruncMonth, TruncYear
# from django.db.models.functions import ExtractWeekD
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractWeek,ExtractWeekDay, ExtractYear


class ShowDashboard(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = request.data
		website_id = int(request.META.get('HTTP_WID'))
		warehouse_id = request.META.get('HTTP_WAREHOUSEID')
		# print(request.META)
		# print(warehouse_id)
		company_id = requestdata['company_id']
		start_date = requestdata['start_date']
		end_date   = requestdata['end_date']

		if warehouse_id is not None and warehouse_id!="" and  int(warehouse_id) >0:
			pass
		else:
			if "warehouse_id" in requestdata:
				warehouse_id = requestdata['warehouse_id']

		# start_date = "2019-07-01"
		# end_date = "2019-07-15"

		start_month = 0
		end_month = 0
		pre_month = 0
		if start_date is not None:
			start_date =  start_date
			start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()		
		else:
			start_date =  yesterday

		if end_date is not None:
			end_date = end_date
			end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
		else:
			end_date = today

		# Combile All methods
		# new_customers 			= NewCustomers(website_id)
		# new_sales 				= NewSales(website_id, warehouse_id, start_date, end_date)
		# new_invoice 			= NewInvoice(website_id, warehouse_id, start_date, end_date)
		# top_customers 			= TopCustomers(website_id,start_date, end_date)
		# top_sold_products 		= TopSoldProduct(website_id, warehouse_id, start_date, end_date)
		# most_viewed_pages 		= MostViewedPage(website_id)
		# traffic_report 	  		= TrafficReport(website_id, start_date, end_date)
		# marketplace_report 	  	= MarketplaceReport(website_id, warehouse_id, start_date, end_date)
		# new_sales_monthly 		= NewSales_Monthly(website_id,warehouse_id, start_date, end_date)
		
		pending_order 			= PendingOrder(website_id,warehouse_id, start_date, end_date)
		payment_complete 		= PaymentComplete(website_id,warehouse_id, start_date, end_date)
		waiting_for_payment		= WaitingForPaymentOrder(website_id,warehouse_id, start_date, end_date)
		delivered_order 		= DeliveredOrder(website_id,warehouse_id, start_date, end_date)
		orders_in_picking 		= OrdersInPicking(website_id,warehouse_id, start_date, end_date)
			
		data = {
			# "new_customers":new_customers,
			# "new_sales":new_sales,
			# "new_sales_monthly":new_sales_monthly,
			# "new_invoice":new_invoice,
			# "top_customers":top_customers['top_customers_list'],
			# "top_sold_products":top_sold_products['top_sold_product'],
			# "most_viewed_pages":most_viewed_pages['top_page_view'],
			# "traffic_report":traffic_report,
			# "marketplace_report":marketplace_report,
			"pending_order":pending_order,
			"payment_complete":payment_complete,
			"waiting_for_payment":waiting_for_payment,
			"delivered_order":delivered_order,
			"orders_in_picking":orders_in_picking
		}
		return Response(data)


# Dasgboard related methodes
def NewCustomers(website_id):
	now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
	today = now_utc.date()
	yesterday = today - timedelta(days=1)
	rs_customers = EngageboostCustomers.objects.filter(isdeleted = 'n', isblocked='n', created__date__gte=yesterday, website_id=website_id).extra(select={'created':'DATE(created)'}).values('created').annotate(total_customer=Count('id')).order_by('created')

	status = 1
	today_count = 0
	if rs_customers:
		previous_count = 0
		
		for customerdata in rs_customers:
			if yesterday==customerdata['created']:
				previous_count = customerdata['total_customer']
			
			if today==customerdata['created']:
				today_count = customerdata['total_customer']
		diff = 0
		diff_in_percent = 0
		up_dn_status = 0
		if int(today_count)>int(previous_count):
			diff = int(today_count)-int(previous_count)
			if previous_count>0:
				diff_in_percent = (int(diff)*100)/previous_count
			else:
				previous_count= 1
				diff_in_percent = (int(diff)*100)/previous_count
			up_dn_status = 1
		elif int(previous_count)>int(today_count):
			diff = int(previous_count)-int(today_count)
			# diff_in_percent = (int(diff)*100)/previous_count
			if previous_count>0:
				diff_in_percent = (int(diff)*100)/previous_count
			else:
				previous_count= 1
				diff_in_percent = (int(diff)*100)/previous_count

			up_dn_status = 2
		else:
			pass
	else:
		status = 0
		diff = 0
		diff_in_percent = 0
		up_dn_status = 0

	data = {
		"status":status,
		"new_customer":today_count,
		"diff_in_percent":diff_in_percent,
		"up_dn_status":up_dn_status
	}
	return data 

def NewSales(website_id,warehouse_id, start_date, end_date):
	now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
	today = now_utc.date()
	yesterday = today - timedelta(days=1)
	sale_today = 0
	status = 1
	if warehouse_id and warehouse_id>0:
		rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=start_date, website_id=website_id, assign_wh = warehouse_id).exclude(order_status=2, assign_wh__isnull=True).extra(select={'created':'DATE(created)'}).values('created').annotate(total_order = Sum('net_amount')).order_by('created')
	else:
		rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=start_date, website_id=website_id).exclude(order_status=2, assign_wh__isnull=True).extra(select={'created':'DATE(created)'}).values('created').annotate(total_order = Sum('net_amount')).order_by('created')

	if end_date is not None:
		if warehouse_id and warehouse_id>0:
			rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=start_date, created__date__lte=end_date, website_id=website_id, assign_wh=warehouse_id).exclude(order_status=2, assign_wh__isnull=True).extra(select={'created':'DATE(created)'}).values('created').annotate(total_order = Sum('net_amount')).order_by('created')
		else:
			rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=start_date, created__date__lte=end_date, website_id=website_id).exclude(order_status=2, assign_wh__isnull=True).extra(select={'created':'DATE(created)'}).values('created').annotate(total_order = Sum('net_amount')).order_by('created')

	# print(rs_order.query)
	if rs_order:
		sale_today = rs_order[0]['total_order']

	data = {
		"status":status,
		"total_order_today":sale_today,
		"diff_in_percent":10,
		"up_dn_status":1
	}
	return data

def NewSales_Monthly(website_id,warehouse_id, start_date=None, end_date=None):
	# def NewInvoice(website_id):
	now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
	today 	= now_utc.date()
	yesterday 	= today - timedelta(days=1)

	start_month = 0
	end_month = 0
	pre_month = 0

	start_month = start_date.month
	end_month = end_date.month

	sale_today 	= 0
	status 		= 1
	data 		= []
	last_month 	= []
	if warehouse_id and warehouse_id>0:
		doDtl = EngageboostOrdermaster.objects.filter(created__date__gte=start_date, created__date__lte=end_date,website_id = website_id,  assign_wh = warehouse_id).annotate(month=ExtractMonth('created'), year=ExtractYear('created')).values('month','year')
	else:
		doDtl = EngageboostOrdermaster.objects.filter(created__date__gte=start_date, created__date__lte=end_date,website_id = website_id).annotate(month=ExtractMonth('created'), year=ExtractYear('created')).values('month','year')

	doDtl = doDtl.annotate(total_order = Sum('net_amount'))
	doDtl = doDtl.order_by('month')
	# print(doDtl.query)
	if start_month==end_month:
		pre_month  = int(start_month)-1
		last_month = EngageboostOrdermaster.objects.annotate(month=ExtractMonth('created'), year=ExtractYear('created')).values('month','year')
		if warehouse_id and warehouse_id>0:
			last_month = last_month.filter( created__month= pre_month, assign_wh = warehouse_id, website_id = website_id)
		else:
			last_month = last_month.filter( created__month= pre_month, website_id = website_id)

		last_month = last_month.annotate(total_order = Sum('net_amount'))
		last_month = last_month.order_by('month')
		

	for order_data in doDtl:
		obj_order  	= {}
		obj_order.update({'month': order_data['month'], 'year': order_data['year'], 'total_order': order_data['total_order']})
		data.append(obj_order)
	
	if len(last_month) >0:
		for order_data_last in last_month:
			last_order  = {}
			last_order.update({'month': order_data_last['month'], 'year': order_data_last['year'], 'total_order': order_data_last['total_order']})
			data.append(last_order)


	diff 			= 0
	diff_in_percent = 0
	up_dn_status 	= 0
	
	today_count 	= 0
	previous_count 	= 0

	if data:
		if len(data)>1:
			today_count 	= data[1]['total_order']
		previous_count 	= data[0]['total_order']

	if today_count>0 and previous_count>0:
		if int(today_count)>int(previous_count):
			diff = int(today_count)-int(previous_count)
			diff_in_percent = (int(diff)*100)/previous_count
			up_dn_status = 1
		elif int(previous_count)>int(today_count):
			diff = int(previous_count)-int(today_count)
			diff_in_percent = (int(diff)*100)/previous_count
			up_dn_status = 2
		else:
			pass

	data = {
		"data":data,
		"new_order":diff,
		"total_order_today":diff,
		"diff_in_percent":diff_in_percent,
		"up_dn_status":up_dn_status,
		"up_dn_status_code":{'0':'No Change', '1':'Increase', '2':'Decrease'}
	}
	return data

def NewInvoice(website_id,warehouse_id, start_date=None, end_date=None):
	# def NewInvoice(website_id):
	now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
	today 	= now_utc.date()
	yesterday 	= today - timedelta(days=1)


	start_month = 0
	end_month = 0
	pre_month = 0

	start_month = start_date.month
	end_month = end_date.month

	sale_today 	= 0
	status 		= 1
	data 		= []
	
	last_month 	= []
	if warehouse_id and warehouse_id>0:
		doDtl = EngageboostInvoicemaster.objects.filter(created__gte=start_date, created__lte=end_date, warehouse_id = warehouse_id, website_id=website_id).annotate(month=ExtractMonth('created'), year=ExtractYear('created')).values('month','year')
	else:
		doDtl = EngageboostInvoicemaster.objects.filter(created__gte=start_date, created__lte=end_date, website_id=website_id).annotate(month=ExtractMonth('created'), year=ExtractYear('created')).values('month','year')

	doDtl = doDtl.annotate(total_order = Sum('net_amount'))
	doDtl = doDtl.order_by('month')

	if start_month==end_month:
		pre_month  = int(start_month)-1
		last_month = EngageboostInvoicemaster.objects.annotate(month=ExtractMonth('created'), year=ExtractYear('created')).values('month','year')
		if warehouse_id and warehouse_id>0:
			last_month = last_month.filter( created__month= pre_month, warehouse_id = warehouse_id, website_id=website_id)
		else:
			last_month = last_month.filter( created__month= pre_month, website_id=website_id)

		last_month = last_month.annotate(total_order = Sum('net_amount'))
		last_month = last_month.order_by('month')
		

	for invoice_data in doDtl:
		invoice  	= {}
		invoice.update({'month': invoice_data['month'], 'year': invoice_data['year'], 'total_order': invoice_data['total_order']})
		data.append(invoice)
	
	if len(last_month) >0:
		for invoice_data_last in last_month:
			last_invoice  = {}
			last_invoice.update({'month': invoice_data_last['month'], 'year': invoice_data_last['year'], 'total_order': invoice_data_last['total_order']})
			data.append(last_invoice)


	diff 			= 0
	diff_in_percent = 0
	up_dn_status 	= 0

	today_count = 0
	previous_count = 0
	if data:
		if len(data)>1:
			previous_count 	= data[1]['total_order']

		today_count 	= data[0]['total_order']
		

	if today_count>0 and previous_count>0:
		if int(today_count)>int(previous_count):
			diff = int(today_count)-int(previous_count)
			diff_in_percent = (int(diff)*100)/previous_count
			up_dn_status = 1
		elif int(previous_count)>int(today_count):
			diff = int(previous_count)-int(today_count)
			diff_in_percent = (int(diff)*100)/previous_count
			up_dn_status = 2
		else:
			pass

	data = {
		"data":data,
		"new_invoice":diff,
		"diff_in_percent":diff_in_percent,
		"up_dn_status":up_dn_status,
		"up_dn_status_code":{'0':'No Change', '1':'Increase', '2':'Decrease'}
	}

	return data

def TopCustomers(website_id, start_date, end_date):
	now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
	today = now_utc.date()
	today = now_utc.date()
	yesterday = today - timedelta(days=1)
	sale_today = 0
	status = 1
	rs_order = EngageboostOrdermaster.objects.filter(website_id=website_id, created__gte=start_date, created__lte=end_date).exclude(order_status=2).values('customer_id', 'customer__first_name', 'customer__last_name').annotate(total_amount=Sum('net_amount')).order_by('-total_amount')[:7]

	# rs_order = EngageboostOrdermaster.objects.exclude(order_status=2).annotate(total_amount=Sum('net_amount')).values('customer_id', 'customer__first_name', 'total_amount')
	data = {
		"status":status,
		"top_customers_list":rs_order
	}
	return data

def TopSoldProduct(website_id, warehouse_id, start_date, end_date):
	now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
	today = now_utc.date()
	yesterday = today - timedelta(days=1)
	sale_today = 0
	status = 1
	rs_order = EngageboostOrdermaster.objects.exclude(order_status=2, website_id=website_id, assign_wh=warehouse_id).values_list('id')
	if warehouse_id and warehouse_id>0:
		rs_order_product = EngageboostOrderProducts.objects.filter(order_id__in=rs_order, warehouse_id = warehouse_id, order__created__date__gte=start_date, order__created__date__lte=end_date).values('product_id','product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:7]
	else:
		rs_order_product = EngageboostOrderProducts.objects.filter(order_id__in=rs_order, order__created__date__gte=start_date, order__created__date__lte=end_date).values('product_id','product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:7]
	# print(rs_order_product.query)
	data = {
		"status":status,
		"top_sold_product":rs_order_product
	}
	return data

def MostViewedPage(website_id):
	now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
	today = now_utc.date()
	status = 1

	rs_page_view = EngageboostTrafficReportsPages.objects.filter(website_id=website_id).values('pagepath').annotate(total_page_view=Sum('pageviews')).order_by('-total_page_view')[:7]
	
	data = {
		"status":status,
		"top_page_view":rs_page_view
	}
	return data

def TrafficReport(website_id, start_date, end_date):
	now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
	today = now_utc.date()
	status = 1
	# start_date = "2015-07-01"
	# end_date = "2019-07-15"
	# print(website_id)
	site_visit   = 0
	new_visitors = 0
	total_visit  = 0
	total_avg_time_on_site = 0
	avg_time_on_site = 0
	percent_of_new_visit = 0
	rs_site_visit = EngageboostTrafficReports.objects.filter(date__gte=start_date, date__lte=end_date, website_id=website_id).values('user_type').annotate(total_visit=Sum('totalvisit'), avg_time_on_site=Avg('average_duration'))
	# print(rs_site_visit.query)
	if rs_site_visit and len(rs_site_visit)>0:
		for sitevisit in rs_site_visit:
			if sitevisit['user_type'] == 'New Visitor':
				new_visitors = sitevisit['total_visit']
			total_visit = int(total_visit)+ int(sitevisit['total_visit'])
			total_avg_time_on_site = float(total_avg_time_on_site)+float(sitevisit['avg_time_on_site'])

	site_visit = total_visit
	unique_visitor = site_visit
	new_visitors = new_visitors
	if int(total_visit)>0 and int(new_visitors)>0:
		percent_of_new_visit = (int(new_visitors)*100)/int(total_visit)

	if total_visit>0 and int(total_avg_time_on_site)>0:
		avg_time_on_site = total_avg_time_on_site/total_visit

	rs_page_view = EngageboostTrafficReportsPages.objects.filter(date__gte=start_date, date__lte=end_date,website_id=website_id).aggregate(total=Sum('pageviews'))
	total = 0
	if rs_page_view["total"]:
		total = rs_page_view["total"]
	# page_viewes
	
	data = {
		"site_visit":site_visit,
		'unique_visitor':new_visitors,
		"new_visitors":new_visitors,
		"avg_time_on_site":avg_time_on_site,
		"percent_of_new_visit":percent_of_new_visit,
		"page_view":total
	}
	return data

def MarketplaceReport(website_id,warehouse_id, start_date, end_date):
	now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
	# today = now_utc.date()
	if warehouse_id and warehouse_id>0:
		rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=start_date, created__date__lte=end_date, website_id=website_id, assign_wh=warehouse_id).exclude(order_status=2).values('webshop_id', 'webshop__name').annotate(total_order=Sum('net_amount'))
	else:
		rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=start_date, created__date__lte=end_date, website_id=website_id).exclude(order_status=2).values('webshop_id', 'webshop__name').annotate(total_order=Sum('net_amount'))
	# print(rs_order.query)
	# EngageboostChannels
	total_order = 0
	data = []
	if rs_order:
		for channel_data in rs_order:
			total_order = float(total_order)+float(channel_data['total_order'])
		if int(total_order) >0:
			for channel_data in rs_order:
				data_obj = {}
				percent_calc = 0
				percent_calc = (float(channel_data['total_order'])*100)/total_order

				data_obj = {"channel_name":channel_data['webshop__name'], "channel_id":channel_data['webshop_id'], "sales_percent":percent_calc, "total_order":channel_data['total_order']}
				data.append(data_obj)
	response_data = {
		"total_order_amount":total_order,
		"channel_wisw_data":data
	}
	# print(response_data)
	return response_data

class sales_report(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = request.data
		website_id = int(request.META.get('HTTP_WID'))		
		company_id = requestdata['company_id']

		warehouse_id = 0
		if "warehouse_id" in requestdata:
			warehouse_id = requestdata['warehouse_id']

		start_date = requestdata['start_date']
		end_date   = requestdata['end_date']
		report_type   = requestdata['report_type']
		# start_date = "2019-07-01"
		# end_date = "2019-07-15"

		start_month = 0
		end_month = 0
		pre_month = 0
		if start_date is not None:
			start_date =  start_date
			start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()		
		else:
			start_date =  yesterday

		if end_date is not None:
			end_date = end_date
			end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
		else:
			end_date = today

		report_type = None
		if "report_type" in requestdata:
			report_type = requestdata['report_type']
		
		order_graph = OrderGraph(website_id,warehouse_id, start_date, end_date, report_type)

		# order_graph_data = {
		# 	"order_graph":order_graph['data']
		# }

		order_graph_data = {
			"order_graph":order_graph
		}

		return Response(order_graph_data)

def OrderGraph(website_id, warehouse_id,start_date, end_date, report_type=None):
	now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
	# today 	= now_utc.date()
	# date_from = today - timedelta(days=30)
	today 		= end_date
	date_from 	= start_date

	data = {}
	if report_type is not None:
		if report_type.lower() == "day":
			if warehouse_id and warehouse_id>0:
				rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=date_from, created__date__lte=today, website_id=website_id, assign_wh=warehouse_id).exclude(order_status=2, assign_wh__isnull=True).extra(select={'created':'DATE(created)'}).values('created').annotate(total_order=Sum('net_amount')).order_by('created') # Working fine for date
			else:
				rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=date_from, created__date__lte=today, website_id=website_id).exclude(order_status=2, assign_wh__isnull=True).extra(select={'created':'DATE(created)'}).values('created').annotate(total_order=Sum('net_amount')).order_by('created') # Working fine for date

			# rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=date_from, created__date__lte=today).exclude(order_status=2).annotate(total_order=Sum('net_amount'), year=ExtractYear('created'), month=ExtractMonth('created')).values('month','year'). order_by('year','month')
			# rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=date_from, created__date__lte=today).exclude(order_status=2).annotate(total_order=Sum('net_amount'), year=ExtractYear('created'), month=ExtractMonth('created')).values('month','year'). order_by('year','month')

			created = []
			data_val = []
			for orderdata in rs_order:
				created.append(orderdata['created'])
				data_val.append(orderdata['total_order'])		
			data = {
				"data":created,
				"value":data_val
			}

		elif report_type.lower() == "month":
			if warehouse_id and warehouse_id>0:
				doDtl = EngageboostOrdermaster.objects.filter(created__date__gte=date_from, created__date__lte=today, assign_wh=warehouse_id, website_id=website_id).exclude(order_status=2, assign_wh__isnull=True).annotate(month=ExtractMonth('created'), year=ExtractYear('created')).values('month','year')
			else:
				doDtl = EngageboostOrdermaster.objects.filter(created__date__gte=date_from, created__date__lte=today, website_id=website_id).exclude(order_status=2, assign_wh__isnull=True).annotate(month=ExtractMonth('created'), year=ExtractYear('created')).values('month','year')

			doDtl = doDtl.annotate(total_order = Sum('net_amount'))
			doDtl = doDtl.order_by('month')
			created = []
			data_val = []
			month_arr = ['january', 'February', 'March', 'April', 'May','June', 'July','August','September','October', 'November', 'December']
			for orderdata in doDtl:
				# created.append(orderdata['month'])
				created.append(month_arr[orderdata['month']-1])
				data_val.append(orderdata['total_order'])		
			data = {
				"data":created,
				"value":data_val
			}

		elif report_type.lower() == "week":
			if warehouse_id and warehouse_id>0:
				doDtl = EngageboostOrdermaster.objects.filter(created__date__gte=date_from, created__date__lte=today, assign_wh=warehouse_id, website_id=website_id).exclude(order_status=2, assign_wh__isnull=True).annotate(week=ExtractWeek('created'), year=ExtractYear('created')).values('week','year')
			else:
				doDtl = EngageboostOrdermaster.objects.filter(created__date__gte=date_from, created__date__lte=today, website_id=website_id).exclude(order_status=2, assign_wh__isnull=True).annotate(week=ExtractWeek('created'), year=ExtractYear('created')).values('week','year')

			doDtl = doDtl.annotate(total_order = Sum('net_amount'))
			doDtl = doDtl.order_by('week')
			week_data = []
			if len(doDtl)>0:
				for week_val in doDtl:
					data_obj = {}
					week_str = str(week_val['year'])+'-W'+str(week_val['week'])		# '2019-W25'
					date_of_week = datetime.datetime.strptime(week_str + '-1', '%G-W%V-%u')
					data_obj.update({"week": week_val['week'],"year": week_val['year'],"total_order": week_val['total_order'], "date_of_week":date_of_week})
					week_data.append(data_obj)

			created = []
			data_val = []
			for orderdata in week_data:
				created.append(orderdata['date_of_week'])
				data_val.append(orderdata['total_order'])		
			data = {
				"data":created,
				"value":data_val
			}

			# data = {
			# 	"data":week_data
			# }
		elif report_type.lower() == "year":
			thisyear = today.year
		
			doDtl = EngageboostOrdermaster.objects.exclude(order_status=2, assign_wh__isnull=True).annotate(year=ExtractYear('created')).values('year')
			# doDtl = doDtl.filter( created__date__year= thisyear)
			if warehouse_id and warehouse_id>0:
				doDtl = doDtl.filter( assign_wh=warehouse_id, website_id=website_id)
			
			doDtl = doDtl.annotate(total_order = Sum('net_amount'))
			doDtl = doDtl.order_by('year')
			# print(doDtl.query)
			created = []
			data_val = []
			for orderdata in doDtl:
				created.append(orderdata['year'])
				data_val.append(orderdata['total_order'])		
			data = {
				"data":created,
				"value":data_val
			}
			# data = {
			# 	"data":doDtl
			# }
		else:
			if warehouse_id and warehouse_id>0:
				rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=date_from, created__date__lte=today, website_id=website_id, assign_wh=warehouse_id).exclude(order_status=2).extra(select={'created':'DATE(created)'}).values('created').annotate(total_order=Sum('net_amount')).order_by('created') # Working fine for date
			else:
				rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=date_from, created__date__lte=today, website_id=website_id).exclude(order_status=2).extra(select={'created':'DATE(created)'}).values('created').annotate(total_order=Sum('net_amount')).order_by('created') # Working fine for date

			created = []
			data_val = []
			for orderdata in rs_order:
				created.append(orderdata['created'])
				data_val.append(orderdata['total_order'])		
			data = {
				"data":created,
				"value":data_val
			}

			
			# data = {
			# 	"data":rs_order
			# }
		
	else:
		if warehouse_id and warehouse_id>0:
			rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=date_from, created__date__lte=today, website_id=website_id, assign_wh=warehouse_id).exclude(order_status=2).extra(select={'created':'DATE(created)'}).values('created').annotate(total_order=Sum('net_amount')).order_by('created') # Working fine for date
		else:
			rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=date_from, created__date__lte=today, website_id=website_id).exclude(order_status=2).extra(select={'created':'DATE(created)'}).values('created').annotate(total_order=Sum('net_amount')).order_by('created') # Working fine for date
		data = {
			"data":rs_order
		}
	return data

def PendingOrder(website_id, warehouse_id,start_date, end_date):
	# website_id, warehouse_id,start_date, end_date
	if int(warehouse_id) >0:
		rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=start_date,created__date__lte=end_date, website_id=website_id, assign_wh = warehouse_id, order_status=0, buy_status=1).exclude(assign_wh__isnull=True).extra(select={'created':'DATE(created)'}).values('created').annotate(total_order_amount = Sum('net_amount'), total_order = Count('id')).order_by('created').iterator()
	else:
		rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=start_date,created__date__lte=end_date, website_id=website_id, order_status=0, buy_status=1).exclude(assign_wh__isnull=True).extra(select={'created':'DATE(created)'}).values('created').annotate(total_order_amount = Sum('net_amount'), total_order = Count('id')).order_by('created').iterator()

	data = {}
	date_wise_data = []
	total_order_amount = 0
	total_order_count = 0
	if rs_order:
		for orderdata in rs_order:
			date_wise_data.append(orderdata)
			total_order_amount = float(total_order_amount) + float(orderdata["total_order_amount"])
			total_order_count = int(total_order_count) + int(orderdata["total_order"])
	data = {"date_wise_data":date_wise_data, "total_order_amount":total_order_amount, "total_order_count":total_order_count}
	return data

def PaymentComplete(website_id, warehouse_id,start_date, end_date):
	if int(warehouse_id)>0:
		rs_order = EngageboostShipmentOrders.objects.filter(order_id__created__date__gte=start_date, order_id__created__date__lte=end_date, order_id__order_status__in=[100,1], order_id__buy_status=1, order_id__assign_wh = warehouse_id).exclude(order_id__assign_wh__isnull=True).exclude(shipment_status__in=["Invoicing","Picking"]).extra(select={'created':'DATE(created)'}).values('order_id__created').annotate(total_order_amount = Sum('order_id__net_amount'), total_order = Count('order_id__id')).order_by('order_id__created').iterator()
	else:
		rs_order = EngageboostShipmentOrders.objects.filter(order_id__created__date__gte=start_date, order_id__created__date__lte=end_date, order_id__order_status__in=[100,1], order_id__buy_status=1).exclude(order_id__assign_wh__isnull=True).exclude(shipment_status__in=["Invoicing","Picking"]).extra(select={'created':'DATE(created)'}).values('order_id__created').annotate(total_order_amount = Sum('order_id__net_amount'), total_order = Count('order_id__id')).order_by('order_id__created').iterator()
	
	data 				= {}
	date_wise_data 		= []
	total_order_amount 	= 0
	total_order_count 	= 0
	if rs_order:
		for orderdata in rs_order:
			date_wise_data.append(orderdata)
			total_order_amount = float(total_order_amount) + float(orderdata["total_order_amount"])
			total_order_count = int(total_order_count) + int(orderdata["total_order"])
	data = {"date_wise_data":date_wise_data, "total_order_amount":total_order_amount, "total_order_count":total_order_count}
	return data

def WaitingForPaymentOrder(website_id, warehouse_id,start_date, end_date):
	if int(warehouse_id)>0:
		# rs_order = EngageboostShipmentOrders.objects.filter(order_id__created__date__gte=start_date, order_id__created__date__lte=end_date, order_id__order_status=100, order_id__buy_status=1, order_id__assign_wh = warehouse_id).exclude(order_id__assign_wh__isnull=True, shipment_status__in=["Invoicing","Picking"]).extra(select={'created':'DATE(created)'}).values('order_id__created').annotate(total_order_amount = Sum('order_id__net_amount'), total_order = Count('order_id__id')).order_by('order_id__created')
		rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=start_date,created__date__lte=end_date,order_status=100,buy_status=1,assign_wh = warehouse_id,shipment_order__shipment_status__in=["Invoicing"]).extra(select={'created':'DATE(created)'}).values('created').annotate(total_order_amount = Sum('net_amount'), total_order = Count('id')).order_by('created').iterator()
	else:
		# rs_order = EngageboostShipmentOrders.objects.filter(order_id__created__date__gte=start_date, order_id__created__date__lte=end_date, order_id__order_status=100, order_id__buy_status=1).exclude(order_id__assign_wh__isnull=True, shipment_status__in=["Invoicing","Picking"]).extra(select={'created':'DATE(created)'}).values('order_id__created').annotate(total_order_amount = Sum('order_id__net_amount'), total_order = Count('order_id__id')).order_by('order_id__created').iterator()
		rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=start_date,created__date__lte=end_date,order_status=100,buy_status=1,shipment_order__shipment_status__in=["Invoicing"]).extra(select={'created':'DATE(created)'}).values('created').annotate(total_order_amount = Sum('net_amount'), total_order = Count('id')).order_by('created').iterator()
	data 				= {}
	date_wise_data 		= []
	total_order_amount 	= 0
	total_order_count 	= 0
	if rs_order:
		for orderdata in rs_order:
			date_wise_data.append(orderdata)
			total_order_amount = float(total_order_amount) + float(orderdata["total_order_amount"])
			total_order_count = int(total_order_count) + int(orderdata["total_order"])
	data = {"date_wise_data":date_wise_data, "total_order_amount":total_order_amount, "total_order_count":total_order_count}
	return data

def DeliveredOrder(website_id, warehouse_id,start_date, end_date):
	if int(warehouse_id)>0:
		rs_order = EngageboostShipmentOrders.objects.filter(order_id__created__date__gte=start_date, order_id__created__date__lte=end_date, order_id__order_status=4, order_id__buy_status=1, order_id__assign_wh = warehouse_id).exclude(order_id__assign_wh__isnull=True).extra(select={'created':'DATE(created)'}).values('order_id__created').annotate(total_order_amount = Sum('order_id__net_amount'), total_order = Count('order_id__id')).order_by('order_id__created').iterator()
	else:
		rs_order = EngageboostShipmentOrders.objects.filter(order_id__created__date__gte=start_date, order_id__created__date__lte=end_date, order_id__order_status=4, order_id__buy_status=1).exclude(order_id__assign_wh__isnull=True).extra(select={'created':'DATE(created)'}).values('order_id__created').annotate(total_order_amount = Sum('order_id__net_amount'), total_order = Count('order_id__id')).order_by('order_id__created').iterator()
	
	data 					= {}
	date_wise_data 			= []
	total_order_amount 		= 0
	total_order_count 		= 0
	if rs_order:
		for orderdata in rs_order:
			date_wise_data.append(orderdata)
			total_order_amount = float(total_order_amount) + float(orderdata["total_order_amount"])
			total_order_count = int(total_order_count) + int(orderdata["total_order"])
	data = {"date_wise_data":date_wise_data, "total_order_amount":total_order_amount, "total_order_count":total_order_count}
	return data

def OrdersInPicking(website_id, warehouse_id,start_date, end_date):
	if int(warehouse_id)>0:
		rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=start_date,created__date__lte=end_date,order_status=100,buy_status=1,assign_wh = warehouse_id,shipment_order__shipment_status__in=["Picking"]).extra(select={'created':'DATE(created)'}).values('created').annotate(total_order_amount = Sum('net_amount'), total_order = Count('id')).order_by('created').iterator()
	else:
		rs_order = EngageboostOrdermaster.objects.filter(created__date__gte=start_date,created__date__lte=end_date,order_status=100,buy_status=1,shipment_order__shipment_status__in=["Picking"]).extra(select={'created':'DATE(created)'}).values('created').annotate(total_order_amount = Sum('net_amount'), total_order = Count('id')).order_by('created').iterator()
	# "Picking"
	data 				= {}
	date_wise_data 		= []
	total_order_amount 	= 0
	total_order_count 	= 0
	if rs_order:
		for orderdata in rs_order:
			date_wise_data.append(orderdata)
			total_order_amount = float(total_order_amount) + float(orderdata["total_order_amount"])
			total_order_count = int(total_order_count) + int(orderdata["total_order"])
	data = {"date_wise_data":date_wise_data, "total_order_amount":total_order_amount, "total_order_count":total_order_count}
	return data


class PendinOrderData(APIView):
	def post(self, request, format=None):
		website_id = 1 
		warehouse_id = 34
		start_date = "2020-03-01"
		end_date = "2020-04-01"
		data = DeliveredOrder(website_id, warehouse_id,start_date, end_date)
		return Response(data)


# PendingOrder()

# ****************************

# OrderGraph()
# MarketplaceReport(1,'2019-06-01','2019-07-01' )
# TrafficReport(1,'2015-07-01', '2019-07-15')
# NewSales_new(1, '2019-06-01', '2019-07-01')