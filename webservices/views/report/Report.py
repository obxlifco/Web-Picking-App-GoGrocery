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
import os
import sys
import xlrd
import xlsxwriter
from webservices.views.order import Order
from django.utils.crypto import get_random_string
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractWeek,ExtractWeekDay, ExtractYear
from elasticsearch import Elasticsearch
from elasticsearch import helpers
es = Elasticsearch([{'host': settings.ELASTIC_HOST, 'port': settings.ELASTIC_PORT}])

class OrderReport(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = request.data
		website_id = int(request.META.get('HTTP_WID'))
		# warehouse_id = request.META.get('HTTP_WAREHOUSEID')
		warehouse_id = 1
		if "warehouse_id" in requestdata:
			warehouse_id = requestdata['warehouse_id']

		company_id = requestdata['company_id']
		start_date = requestdata['start_date']
		end_date   = requestdata['end_date']

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

		elastic_index = 'order_'+str(website_id)
		exists = es.indices.exists(index=elastic_index)
		try:
			if not exists:
				data = {
					"status":0,
					"msg":"Index not found."
				}
			else:
				# ************  Check file dir exist or not. If dir not exist then create
				file_dir = settings.MEDIA_ROOT + '/exportfile/'
				export_dir = settings.MEDIA_URL + 'exportfile/'
				if not os.path.exists(file_dir):
					os.makedirs(file_dir)
				# ************  Create file name
				file_name = "order_export_" + get_random_string(length=5)

				# Create file full path
				file_path = file_dir + file_name + '.xlsx'
				export_file_path = export_dir + file_name + '.xlsx'
				export_file_path = export_file_path[1:]

				workbook = xlsxwriter.Workbook(file_path)
				worksheet = workbook.add_worksheet()

				q = {
					"query": {
						"range": {
							"created": {
								"gte": start_date,
								"lt": end_date
							}
						}
					}			
				}
				order_data = es.search(
					index=elastic_index, 
					doc_type="data",
					body=q,
					_source=True,
					_source_exclude="webshop"
				)

				bold = workbook.add_format({'bold': True})
				row = 1

				worksheet.write(0, 0, 'Order No', bold)
				worksheet.write(0, 1, 'Order Date', bold)
				worksheet.write(0, 2, 'Delivery Date', bold)
				worksheet.write(0, 3, 'Time Slot', bold)
				worksheet.write(0, 4, 'Coupon Code', bold)
				worksheet.write(0, 5, 'Payment Type', bold)
				worksheet.write(0, 6, 'Zone', bold)
				worksheet.write(0, 7, 'Customer Name', bold)
				worksheet.write(0, 8, 'Customer Email', bold)
				worksheet.write(0, 9, 'Customer Mob No', bold)
				worksheet.write(0, 10, 'Total No of Item', bold)
				worksheet.write(0, 11, 'Gross Amount', bold)
				worksheet.write(0, 12, 'Shipping Cost', bold)
				worksheet.write(0, 13, 'Coupon Discount', bold)
				worksheet.write(0, 14, 'Total Discount', bold)
				worksheet.write(0, 15, 'Net Amount', bold)

				if order_data['hits']['hits']:
					data = []			
					for orderdata in order_data['hits']['hits']:
						obj_data = {}
						created_date = ""
						# print(orderdata)
						dt = orderdata['_source']['created']
						f = "%Y-%m-%dT%H:%M:%S.%fZ"
						created_date = datetime.datetime.strptime(dt, f)
						created_date = created_date.strftime('%Y-%m-%d %H:%M:%S')
						worksheet.write(row, 0, orderdata['_source']['custom_order_id'], 0)
						worksheet.write(row, 1, created_date, 0)
						worksheet.write(row, 2, orderdata['_source']['time_slot_date'], 0)
						worksheet.write(row, 3, str(orderdata['_source']['time_slot_date'])+" "+str(orderdata['_source']['time_slot_id']), 0)
						worksheet.write(row, 4, orderdata['_source']['applied_coupon'], 0)
						worksheet.write(row, 5, orderdata['_source']['payment_method_name'], 0)
						worksheet.write(row, 6, orderdata['_source']['zone_name'], 0)
						worksheet.write(row, 7, orderdata['_source']['customer']['first_name'], 0)
						worksheet.write(row, 8, orderdata['_source']['customer']['email'], 0)
						worksheet.write(row, 9, orderdata['_source']['customer']['phone'], 0)
						worksheet.write(row, 10, len(orderdata['_source']['order_products']), 0)
						worksheet.write(row, 11, orderdata['_source']['gross_amount'], 0)
						worksheet.write(row, 12, orderdata['_source']['shipping_cost'], 0)
						worksheet.write(row, 13, orderdata['_source']['cart_discount'], 0)
						worksheet.write(row, 14, orderdata['_source']['gross_discount_amount'], 0)
						worksheet.write(row, 15, orderdata['_source']['net_amount'], 0)
						row = row + 1
					workbook.close()
					data = {
						"status":1,
						"message":"Report Created.",
						"file":file_name
					}
				else:
					data = {
						"status":0,
						"message":"No data found.",
						"file":""
					}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}

		# return Response(order_data)
		return Response(data)

class CustomerReport(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = request.data
		website_id = int(request.META.get('HTTP_WID'))
		# warehouse_id = request.META.get('HTTP_WAREHOUSEID')
		warehouse_id = 1
		if "warehouse_id" in requestdata:
			warehouse_id = requestdata['warehouse_id']

		company_id = requestdata['company_id']
		start_date = requestdata['start_date']
		end_date   = requestdata['end_date']

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

		# start_date = "2019-06-01"
		# end_date = "2019-07-25"
		elastic_index = 'order_'+str(website_id)
		exists = es.indices.exists(index=elastic_index)
		try:
			if not exists:
				data = {
					"status":0,
					"msg":"Index not found."
				}
			else:				
				q = {
					"query": {
						"bool": {
							"filter": {
								"range": {
									"created": {
										"gte": start_date,
										"lte": end_date
									}
								}
							}
						}
					},
					"aggs": {
						"user_likes": {
							"terms": {
								"field": "customer.id"
							},
							"aggs": {
								"toal_order_amount": {
									"sum": {
										"field": "net_amount"
									}
								},
								"total_discount": {
									"sum": {
										"field": "gross_discount_amount"
									}
								}
							}
						}
					}
				}
				order_data = es.search(
					index=elastic_index, 
					doc_type="data",
					body=q,
					_source=True,
					_source_exclude="webshop"
				)
				# print(order_data['aggregations']['user_likes']['buckets'])
				# print(order_data['hits']['hits'])				
				customer_arr = []
				if order_data['aggregations']['user_likes']['buckets']:
					for groupdata in order_data['aggregations']['user_likes']['buckets']:

						customer = {}
						customer = {
							"customer_id":groupdata['key'],
							"total_order":groupdata['doc_count'],
							"total_discount":groupdata['total_discount']['value'],
							"toal_order_amount":groupdata['toal_order_amount']['value'],
						}
						for customers in order_data['hits']['hits']:
							customer_name = ""
							if customers['_source']['customer']['id']==groupdata['key']:
								customer.update({"customer_name":customers['_source']['customer']['first_name'], "customer_email":customers['_source']['customer']['email'], "customer_phone":customers['_source']['customer']['phone'],"address":customers['_source']['customer']['address']})
								pass
								customer_arr.append(customer)
				
				# ************  Check file dir exist or not. If dir not exist then create
				file_dir = settings.MEDIA_ROOT + '/exportfile/'
				export_dir = settings.MEDIA_URL + 'exportfile/'
				if not os.path.exists(file_dir):
					os.makedirs(file_dir)
				# ************  Create file name
				file_name = "order_customer_export_" + get_random_string(length=5)

				# Create file full path
				file_path = file_dir + file_name + '.xlsx'
				export_file_path = export_dir + file_name + '.xlsx'
				export_file_path = export_file_path[1:]
				workbook = xlsxwriter.Workbook(file_path)
				worksheet = workbook.add_worksheet()

				bold = workbook.add_format({'bold': True})
				row = 1
				worksheet.write(0, 0, 'Customer name', bold)
				worksheet.write(0, 1, 'Eamil', bold)
				worksheet.write(0, 2, 'Mobile', bold)
				worksheet.write(0, 3, 'City', bold)
				worksheet.write(0, 4, 'No. Of Order', bold)
				worksheet.write(0, 5, 'Order Total', bold)
				worksheet.write(0, 6, 'Invoiced', bold)
				worksheet.write(0, 7, 'Discount', bold)

				for customer_data in customer_arr:
					worksheet.write(row, 0, customer_data['customer_name'], 0)
					worksheet.write(row, 1, customer_data['customer_email'], 0)
					worksheet.write(row, 2, customer_data['customer_phone'], 0)
					worksheet.write(row, 3, customer_data['address'], 0)
					worksheet.write(row, 4, customer_data['total_order'], 0)
					worksheet.write(row, 5, customer_data['toal_order_amount'], 0)
					worksheet.write(row, 6, "", 0)
					worksheet.write(row, 7, customer_data['total_discount'], 0)
					row = row + 1
				workbook.close()

				data = {
					"status":1,
					"message":"Report Created.",
					"file":file_name,
					"data":customer_arr
				}

		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}
		# data = {
		# 	"status":1,
		# 	"data":order_data['hits']['hits']
		# }
		# return Response(order_data)
		return Response(data)

class NewCustomerReport(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = request.data
		website_id = int(request.META.get('HTTP_WID'))
		# warehouse_id = request.META.get('HTTP_WAREHOUSEID')
		warehouse_id = 1
		if "warehouse_id" in requestdata:
			warehouse_id = requestdata['warehouse_id']

		company_id = requestdata['company_id']
		start_date = requestdata['start_date']
		end_date   = requestdata['end_date']

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

		# start_date = "2019-06-01"
		# end_date = "2019-07-25"
		elastic_index = 'order_'+str(website_id)
		exists = es.indices.exists(index=elastic_index)
		try:
			if not exists:
				data = {
					"status":0,
					"msg":"Index not found."
				}
			else:				
				q = {
					"query": {
						"bool": {
							"filter": {
								"range": {
									"created": {
										"gte": start_date,
										"lte": end_date
									}
								}
							}
						}
					},
					"aggs": {
						"user_likes": {
							"terms": {
								"field": "customer.id"
							},
							"aggs": {
								"toal_order_amount": {
									"sum": {
										"field": "net_amount"
									}
								},
								"total_discount": {
									"sum": {
										"field": "gross_discount_amount"
									}
								}
							}
						}
					}
				}
				order_data = es.search(
					index=elastic_index, 
					doc_type="data",
					body=q,
					_source=True,
					_source_exclude="webshop"
				)
				# print(order_data['aggregations']['user_likes']['buckets'])
				# print(order_data['hits']['hits'])				
				customer_arr = []
				if order_data['aggregations']['user_likes']['buckets']:
					for groupdata in order_data['aggregations']['user_likes']['buckets']:

						customer = {}
						customer = {
							"customer_id":groupdata['key'],
							"total_order":groupdata['doc_count'],
							"total_discount":groupdata['total_discount']['value'],
							"toal_order_amount":groupdata['toal_order_amount']['value'],
						}
						for customers in order_data['hits']['hits']:
							customer_name = ""
							if customers['_source']['customer']['id']==groupdata['key']:
								customer.update({"customer_name":customers['_source']['customer']['first_name'], "customer_email":customers['_source']['customer']['email'], "customer_phone":customers['_source']['customer']['phone'],"address":customers['_source']['customer']['address']})
								pass
								customer_arr.append(customer)
				
				# ************  Check file dir exist or not. If dir not exist then create
				file_dir = settings.MEDIA_ROOT + '/exportfile/'
				export_dir = settings.MEDIA_URL + 'exportfile/'
				if not os.path.exists(file_dir):
					os.makedirs(file_dir)
				# ************  Create file name
				file_name = "order_customer_export_" + get_random_string(length=5)

				# Create file full path
				file_path = file_dir + file_name + '.xlsx'
				export_file_path = export_dir + file_name + '.xlsx'
				export_file_path = export_file_path[1:]
				workbook = xlsxwriter.Workbook(file_path)
				worksheet = workbook.add_worksheet()

				bold = workbook.add_format({'bold': True})
				row = 1
				worksheet.write(0, 0, 'Customer name', bold)
				worksheet.write(0, 1, 'Eamil', bold)
				worksheet.write(0, 2, 'Mobile', bold)
				worksheet.write(0, 3, 'City', bold)
				worksheet.write(0, 4, 'No. Of Order', bold)
				worksheet.write(0, 5, 'Order Total', bold)
				worksheet.write(0, 6, 'Invoiced', bold)
				worksheet.write(0, 7, 'Discount', bold)

				for customer_data in customer_arr:
					worksheet.write(row, 0, customer_data['customer_name'], 0)
					worksheet.write(row, 1, customer_data['customer_email'], 0)
					worksheet.write(row, 2, customer_data['customer_phone'], 0)
					worksheet.write(row, 3, customer_data['address'], 0)
					worksheet.write(row, 4, customer_data['total_order'], 0)
					worksheet.write(row, 5, customer_data['toal_order_amount'], 0)
					worksheet.write(row, 6, "", 0)
					worksheet.write(row, 7, customer_data['total_discount'], 0)
					row = row + 1
				workbook.close()

				data = {
					"status":1,
					"message":"Report Created.",
					"file":file_name,
					"data":customer_arr
				}

		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}
		# data = {
		# 	"status":1,
		# 	"data":order_data['hits']['hits']
		# }
		# return Response(order_data)
		return Response(data)

class ItemwiseOrderReport(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = request.data
		website_id = int(request.META.get('HTTP_WID'))
		# warehouse_id = request.META.get('HTTP_WAREHOUSEID')
		warehouse_id = 1
		if "warehouse_id" in requestdata:
			warehouse_id = requestdata['warehouse_id']

		company_id = requestdata['company_id']
		start_date = requestdata['start_date']
		end_date   = requestdata['end_date']

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

		elastic_index = 'order_'+str(website_id)
		exists = es.indices.exists(index=elastic_index)
		try:
			if not exists:
				data = {
					"status":0,
					"msg":"Index not found."
				}
			else:
				# ************  Check file dir exist or not. If dir not exist then create
				file_dir = settings.MEDIA_ROOT + '/exportfile/'
				export_dir = settings.MEDIA_URL + 'exportfile/'
				if not os.path.exists(file_dir):
					os.makedirs(file_dir)
				# ************  Create file name
				file_name = "itemwise_order_export_" + get_random_string(length=5)

				# Create file full path
				file_path = file_dir + file_name + '.xlsx'
				export_file_path = export_dir + file_name + '.xlsx'
				export_file_path = export_file_path[1:]

				workbook = xlsxwriter.Workbook(file_path)
				worksheet = workbook.add_worksheet()

				q = {					
					"query": {
						"range": {
							"created": {
								"gte": start_date,
								"lt": end_date
							}
						}
					}			
				}
				order_data = es.search(
					index=elastic_index, 
					doc_type="data",
					body=q,
					_source=True,
					# _source_inclue="time_slot_date, time_slot_id, order_status, created, custom_order_id, shipping_status, cart_discount",
					_source_exclude="webshop,customer"
				)
				# print(json.dumps(order_data))

				bold = workbook.add_format({'bold': True})
				row = 1
				worksheet.write(0, 0, 'Delivery Date', bold)
				worksheet.write(0, 1, 'Order Date', bold)
				worksheet.write(0, 2, 'Order No', bold)
				worksheet.write(0, 3, 'Status', bold)
				worksheet.write(0, 4, 'Shipping Status', bold)
				worksheet.write(0, 5, 'Product SKU', bold)
				worksheet.write(0, 6, 'Product Name', bold)
				worksheet.write(0, 7, 'Category Name', bold)
				worksheet.write(0, 8, 'Original Qty', bold)
				worksheet.write(0, 9, 'Quantity', bold)
				worksheet.write(0, 10, 'Product Price', bold)
				worksheet.write(0, 11, 'Shipping Cost', bold)
				worksheet.write(0, 12, 'Coupon Discount', bold)				
				worksheet.write(0, 13, 'Gross Amount', bold)
				worksheet.write(0, 14, 'Product Discount', bold)
				worksheet.write(0, 15, 'Total Discount', bold)
				worksheet.write(0, 16, 'Tax Amount', bold)
				worksheet.write(0, 17, 'Net Amount', bold)
				worksheet.write(0, 18, 'Average Order Price', bold)

				if order_data['hits']['hits']:
					data = []			
					for orderdata in order_data['hits']['hits']:
						obj_data = {}
						custom_order_id = orderdata['_source']['custom_order_id']
						order_date = ""
						# print(orderdata)
						dt = orderdata['_source']['created']
						f = "%Y-%m-%dT%H:%M:%S.%fZ"
						order_date = datetime.datetime.strptime(dt, f)
						order_date = order_date.strftime('%Y-%m-%d %H:%M:%S')

						# time_slot_date, time_slot_id, order_status, created, custom_order_id, shipping_status, cart_discount

						worksheet.write(row, 0, orderdata['_source']['time_slot_date'], 0)
						worksheet.write(row, 1, order_date, 0)
						worksheet.write(row, 2, orderdata['_source']['custom_order_id'], 0)
						# ***********
						order_status = Order.CheckOrderStatusByOrderStatus(orderdata['_source']['order_status'], orderdata['_source']['buy_status'])

						worksheet.write(row, 3, str(order_status), 0)
						worksheet.write(row, 4, orderdata['_source']['shipping_status'], 0)
						worksheet.write(row, 11, orderdata['_source']['shipping_cost'], 0)
						worksheet.write(row, 12, orderdata['_source']['cart_discount'], 0)
						worksheet.write(row, 13, orderdata['_source']['gross_amount'], 0)
						worksheet.write(row, 15, orderdata['_source']['gross_discount_amount'], 0)						
						worksheet.write(row, 17, orderdata['_source']['net_amount'], 0)

						if len(orderdata['_source']['order_products'])>0:
							for products in orderdata['_source']['order_products']:
								worksheet.write(row, 5, products['product']['sku'], 0)
								worksheet.write(row, 6, products['product']['name'], 0)
								worksheet.write(row, 8, products['quantity'], 0)
								worksheet.write(row, 9, int(products['quantity'])-int(products['deleted_quantity'])-int(products['shortage'])-int(products['returns']), 0)
								worksheet.write(row, 10, products['product_price'], 0)
								worksheet.write(row, 16, products['product_tax_price'], 0)
								worksheet.write(row, 14, products['product_discount_price'], 0)
								# worksheet.write(row, 17, float(products['gross_amount'])/(int(products['quantity'])-int(products['deleted_quantity'])-int(products['shortage'])-int(products['returns'])), 0)
								row = row + 1
						# row = row + 1
					workbook.close()
					data = {
						"status":1,
						"message":"Report Created.",
						"file":file_name
					}
				else:
					data = {
						"status":0,
						"message":"No data found.",
						"file":""
					}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}

		# return Response(order_data)
		return Response(data)

class SalesReport(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = request.data
		website_id = int(request.META.get('HTTP_WID'))
		warehouse_id = 1
		if "warehouse_id" in requestdata:
			warehouse_id = requestdata['warehouse_id']

		company_id = requestdata['company_id']
		start_date = requestdata['start_date']
		end_date   = requestdata['end_date']

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

		elastic_index = 'order_'+str(website_id)
		exists = es.indices.exists(index=elastic_index)
		try:
			if not exists:
				data = {
					"status":0,
					"msg":"Index not found."
				}
			else:
				# ************  Check file dir exist or not. If dir not exist then create
				file_dir = settings.MEDIA_ROOT + '/exportfile/'
				export_dir = settings.MEDIA_URL + 'exportfile/'
				if not os.path.exists(file_dir):
					os.makedirs(file_dir)
				# ************  Create file name
				file_name = "sales_report_" + get_random_string(length=5)

				# Create file full path
				file_path = file_dir + file_name + '.xlsx'
				export_file_path = export_dir + file_name + '.xlsx'
				export_file_path = export_file_path[1:]

				workbook = xlsxwriter.Workbook(file_path)
				worksheet = workbook.add_worksheet()

				q = {
					"size": 200,
					"aggs": {
						"ArticlesAfterTime": {
							"filter": {
								"range": {
									"created": {
										"gte": "2019-07-01",
										"lt": "2019-07-30"
									}
								}
							},
							"aggs": {
								"GroupByDate": {
									"date_histogram": {
										"field": "created",
										"interval": "day",
										"format": "yyyy-MM-dd"
									},
									"aggs": {
										"total_netAmount": {
											"sum": {
												"field": "net_amount"
											}
										},
										"total_grossAmount": {
											"sum": {
												"field": "gross_amount"
											}
										},
										"total_shippingCost": {
											"sum": {
												"field": "shipping_cost"
											}
										},
										"total_taxAmount": {
											"sum": {
												"field": "tax_amount"
											}
										},
										"total_couponDiscount": {
											"sum": {
												"field": "cart_discount"
											}
										},
										"total_totalDiscount": {
											"sum": {
												"field": "gross_discount_amount"
											}
										},
										"total_productDiscount": {
											"sum": {
												"field": "order_products.product_discount_price"
											}
										}
										
									}
								}
							}
						}
					}
				}
				order_data = es.search(
					index=elastic_index, 
					doc_type="data",
					body=q,
					_source=True,
					_source_exclude="webshop,customer"
				)
				print(json.dumps(order_data))
				data = {
					"data":order_data
				}
				bold = workbook.add_format({'bold': True})
				row = 1
				worksheet.write(0, 0, 'Date', bold)
				worksheet.write(0, 1, 'No. Of Orders', bold)
				worksheet.write(0, 2, 'Gross Amount', bold)
				worksheet.write(0, 3, 'Total No. of Items', bold)
				worksheet.write(0, 4, 'Shipping Cost Amt', bold)
				worksheet.write(0, 5, 'Tax Amount', bold)
				worksheet.write(0, 6, 'Coupon Discount', bold)
				worksheet.write(0, 7, 'Product Discount', bold)
				worksheet.write(0, 8, 'Total Discount', bold)
				worksheet.write(0, 9, 'Net Amount', bold)
				worksheet.write(0, 10, 'Average Order Price', bold)

				if order_data['aggregations']['ArticlesAfterTime']['GroupByDate']['buckets'] and len(order_data['aggregations']['ArticlesAfterTime']['GroupByDate']['buckets'])>0:
					data = []
					for orderdata in order_data['aggregations']['ArticlesAfterTime']['GroupByDate']['buckets']:
						obj_data = {}
						# custom_order_id = orderdata['_source']['custom_order_id']
						# order_date = ""
						# # print(orderdata)
						# dt = orderdata['_source']['created']
						# f = "%Y-%m-%dT%H:%M:%S.%fZ"
						# order_date = datetime.datetime.strptime(dt, f)
						# order_date = order_date.strftime('%Y-%m-%d %H:%M:%S')

						worksheet.write(row, 0, orderdata['key_as_string'], 0)
						worksheet.write(row, 1, orderdata['doc_count'], 0)
						worksheet.write(row, 2, orderdata['total_grossAmount']['value'], 0)
						# worksheet.write(row, 3, str(order_status), 0)
						worksheet.write(row, 4, orderdata['total_shippingCost']['value'], 0)
						worksheet.write(row, 5, orderdata['total_taxAmount']['value'], 0)
						worksheet.write(row, 6, orderdata['total_couponDiscount']['value'], 0)
						worksheet.write(row, 7, orderdata['total_productDiscount']['value'], 0)
						worksheet.write(row, 8, orderdata['total_totalDiscount']['value'], 0)						
						worksheet.write(row, 9, orderdata['total_netAmount']['value'], 0)

					# 	if len(orderdata['_source']['order_products'])>0:
					# 		for products in orderdata['_source']['order_products']:
					# 			worksheet.write(row, 5, products['product']['sku'], 0)
					# 			worksheet.write(row, 6, products['product']['name'], 0)
					# 			worksheet.write(row, 8, products['quantity'], 0)
					# 			worksheet.write(row, 9, int(products['quantity'])-int(products['deleted_quantity'])-int(products['shortage'])-int(products['returns']), 0)
					# 			worksheet.write(row, 10, products['product_price'], 0)
					# 			worksheet.write(row, 16, products['product_tax_price'], 0)
					# 			worksheet.write(row, 14, products['product_discount_price'], 0)
					# 			# worksheet.write(row, 17, float(products['gross_amount'])/(int(products['quantity'])-int(products['deleted_quantity'])-int(products['shortage'])-int(products['returns'])), 0)
					# 			row = row + 1
						row = row + 1
					workbook.close()
					data = {
						"status":1,
						"message":"Report Created.",
						"file":file_name
					}
				else:
					data = {
						"status":0,
						"message":"No data found.",
						"file":""
					}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}

		# return Response(order_data)
		return Response(data)

class ProductReport(generics.ListAPIView):
	def post(self, request, format=None):
		requestdata = request.data
		website_id = int(request.META.get('HTTP_WID'))
		warehouse_id = 1
		if "warehouse_id" in requestdata:
			warehouse_id = requestdata['warehouse_id']

		company_id = requestdata['company_id']
		start_date = requestdata['start_date']
		end_date   = requestdata['end_date']

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

		elastic_index = 'order_'+str(website_id)
		exists = es.indices.exists(index=elastic_index)
		order_data = {
			"status":1
		}
		
		try:
			rs_order = EngageboostOrderProducts.objects.filter(order__isdeleted='n', order__isblocked='n', order__created__date__gte=start_date, order__created__date__lte=end_date).values('product_id__name','product_id__sku', 'cost_price', 'product_price').select_related('').annotate(total_pro_price=Sum('product_price'), no_of_qty_sold=Count('product_id'), total_discount=Sum('product_discount_price'), no_of_orders=Count('product_id__id'))

			print(rs_order.query)
			# ************  Check file dir exist or not. If dir not exist then create
			file_dir = settings.MEDIA_ROOT + '/exportfile/'
			export_dir = settings.MEDIA_URL + 'exportfile/'
			if not os.path.exists(file_dir):
				os.makedirs(file_dir)
			# ************  Create file name
			file_name = "product_report_" + get_random_string(length=5)

			# Create file full path
			file_path = file_dir + file_name + '.xlsx'
			export_file_path = export_dir + file_name + '.xlsx'
			export_file_path = export_file_path[1:]

			workbook = xlsxwriter.Workbook(file_path)
			worksheet = workbook.add_worksheet()

			bold = workbook.add_format({'bold': True})
			row = 1
			worksheet.write(0, 0, 'No. Of Order', bold)
			worksheet.write(0, 1, 'Product Name', bold)
			worksheet.write(0, 2, 'Category Name', bold)
			worksheet.write(0, 3, 'Sold Item', bold)
			worksheet.write(0, 4, 'Order Total', bold)
			worksheet.write(0, 5, 'Invoiced', bold)
			worksheet.write(0, 6, 'Discount', bold)
			worksheet.write(0, 7, 'Default Price', bold)
			worksheet.write(0, 8, 'Total Discount', bold)
			worksheet.write(0, 9, 'Cost Per Unit', bold)
			# No. Of Order	Product Name	Category Name	Sold Item	Order Total	Invoiced	Discount	Default Price	Cost Per Unit
	
			if rs_order:
				data = []
				for orderdata in rs_order:
					obj_data = {}
					worksheet.write(row, 0, orderdata['no_of_orders'], 0)
					worksheet.write(row, 1, orderdata['product_id__name'], 0)
					# worksheet.write(row, 2, orderdata['Category Name'], 0)
					worksheet.write(row, 3, orderdata['no_of_qty_sold'], 0)
					worksheet.write(row, 4, orderdata['total_pro_price'], 0)
					# worksheet.write(row, 5, orderdata['Invoiced'], 0)
					worksheet.write(row, 6, orderdata['total_discount'], 0)
					worksheet.write(row, 7, orderdata['product_price'], 0)
					worksheet.write(row, 8, orderdata['total_discount'], 0)						
					worksheet.write(row, 9, orderdata['cost_price'], 0)
					row = row + 1
				workbook.close()
				data = {
					"status":1,
					"message":"Report Created.",
					"file":file_name
				}
			else:
				data = {
					"status":0,
					"message":"No data found.",
					"file":""
				}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}
		# data = {
		# 	"status":order_data
		# }
		return Response(data)
		
def get_str_order_status(order_status, buy_status):
	str_order_status = ""
	if int(order_status) == 99 and int(buy_status) == 1:
		str_order_status = "Waiting Approval"
	elif int(order_status) == 20 and int(buy_status) == 1:
		str_order_status = "Approved"
	elif int(order_status) == 0 and int(buy_status) == 1:
		str_order_status = "Pending"
	elif int(order_status) == 100 and int(buy_status) == 1:
		str_order_status = "Processing"
	elif int(order_status) == 1 and int(buy_status) == 1:
		str_order_status = "Shipped"
	elif int(order_status) == 2 and int(buy_status) == 1:
		str_order_status = "Cancelled"
	elif int(order_status) == 4 and int(buy_status) == 1:
		str_order_status = "Completed"
	elif int(order_status) == 5 and int(buy_status) == 1:
		str_order_status = "Full Refund"
	elif int(order_status) == 6 and int(buy_status) == 1:
		str_order_status = "Partial Refund"
	elif int(order_status) == 13 and int(buy_status) == 1:
		str_order_status = "Delivered"
	elif int(order_status) == 16 and int(buy_status) == 1:
		str_order_status = "Closed"
	elif int(order_status) == 18 and int(buy_status) == 1:
		str_order_status = "Pending Service"
	elif int(order_status) == 3 and int(buy_status) == 0:
		str_order_status = "Abandoned"
	elif int(order_status) == 999 and int(buy_status) == 0:
		str_order_status = "Failed"
	elif int(order_status) == 9999 and int(buy_status) == 1:
		str_order_status = 'Hold'
	else:
		str_order_status = 'Invoiced'

	return str_order_status

class OrderReportAll(generics.ListAPIView):
	permission_classes = []
	def post(self, request, format=None):
		requestdata = request.data
		# website_id = int(request.META.get('HTTP_WID'))
		# warehouse_id = request.META.get('HTTP_WAREHOUSEID')

		# warehouse_id = 1
		# if "warehouse_id" in requestdata:
		# 	warehouse_id = requestdata['warehouse_id']

		start_date = requestdata['start_date']
		end_date   = requestdata['end_date']

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

		try:
			# ************  Check file dir exist or not. If dir not exist then create
			file_dir = settings.MEDIA_ROOT + '/exportfile/'
			export_dir = settings.MEDIA_URL + 'exportfile/'
			if not os.path.exists(file_dir):
				os.makedirs(file_dir)
			# ************  Create file name
			# file_name = "order_export_" + get_random_string(length=5)
			file_name = "category-wise-order-report-" + str(start_date)+"-to-"+str(end_date)
			# Create file full path
			file_path = file_dir + file_name + '.xlsx'
			export_file_path = export_dir + file_name + '.xlsx'
			export_file_path = export_file_path[1:]

			workbook = xlsxwriter.Workbook(file_path)
			worksheet = workbook.add_worksheet()
			
			rs_order = EngageboostOrdermaster.objects.filter(isdeleted='n', isblocked='n', created__date__gte=start_date, created__date__lte=end_date)
			# order_data = OrderMasterSerializerReportSerializer(rs_order, many=True)
			order_data = OrderMasterSerializerReportCustomerSerializer(rs_order, many=True)
			order_data = order_data.data
			# data = order_data

			bold = workbook.add_format({'bold': True})
			row = 1

			worksheet.write(0, 0, 'CUSTOMER NAME', bold)
			worksheet.write(0, 1, 'CUSTOMER EMAIL', bold)
			worksheet.write(0, 2, 'STORE CODE', bold)
			worksheet.write(0, 3, 'STORE NAME', bold)
			worksheet.write(0, 4, 'ORDER NO', bold)
			worksheet.write(0, 5, 'ORDER DATE', bold)
			worksheet.write(0, 6, 'PAYMENT METHOD', bold)
			worksheet.write(0, 7, 'ORDER STATUS', bold)
			worksheet.write(0, 8, 'PRODUCT NAME', bold)
			worksheet.write(0, 9, 'BARCODE', bold)
			worksheet.write(0, 10, 'CATEGORY ID', bold)
			worksheet.write(0, 11, 'CATEGORY', bold)
			worksheet.write(0, 12, 'QTY', bold)
			worksheet.write(0, 13, 'INVOICED AMOUNT (AFTER COMPLETE DISCOUNTS)', bold)
			worksheet.write(0, 14, 'TOTAL AMOUNT', bold)
			worksheet.write(0, 15, 'SHIPPING COST', bold)

			if order_data:
				data = []			
				for orderdata in order_data:
					obj_data = {}
					created_date = ""
					dt = orderdata['created']
					f = "%Y-%m-%dT%H:%M:%S.%fZ"
					created_date = datetime.datetime.strptime(dt, f)
					created_date = created_date.strftime('%Y-%m-%d %H:%M:%S')
					
					# Order Satus
					order_status = get_str_order_status(orderdata['order_status'],orderdata['buy_status'])
					

					# if len(orderdata['invoice_order']):
					# 	worksheet.write(row, 5, orderdata['invoice_order'][0]['gross_amount'], 0)
					# else:
					# 	worksheet.write(row, 5, orderdata['gross_amount'], 0)
					shipping_row = row
					for products in orderdata['order_products']:
						# worksheet.write(row, 0,orderdata['customer']['first_name'] + ' ' + orderdata['customer']['last_name'],0)
						worksheet.write(row, 0, orderdata['billing_name'],0)
						worksheet.write(row, 1, orderdata['delivery_email_address'],0)
						worksheet.write(row, 2, orderdata['store_details']['store_code'], 0)
						worksheet.write(row, 3, orderdata['store_details']['store_name'], 0)
						worksheet.write(row, 4, orderdata['custom_order_id'], 0)
						worksheet.write(row, 5, created_date, 0)
						worksheet.write(row, 6, orderdata['payment_method_name'], 0)
						worksheet.write(row, 7, order_status, 0)
						# shipping_row = row
						worksheet.write(row, 8, products["product"]["name"], 0)
						worksheet.write(row, 9, products["product"]["sku"], 0)
						worksheet.write(row, 10, products["product"]["product_category"]['ret_cat_id'], 0)
						worksheet.write(row, 11, products["product"]["product_category"]['ret_cat_name'], 0)
						# -----Binayak Start-----#
						qty = int(0 if products["quantity"] == None else products["quantity"]) - int(
							0 if products["deleted_quantity"] == None else products["deleted_quantity"]) - int(
							0 if products["shortage"] == None else products["shortage"]) - int(
							0 if products["returns"] == None else products["returns"])
						if qty <= 0:
							qty = 0
						# -----Binayak End-----#
						worksheet.write(row, 12, qty, 0)
						worksheet.write(row, 13, products["product_price"], 0)
						worksheet.write(row, 14, float(products["product_price"]) * int(qty), 0)
						worksheet.write(shipping_row, 15, orderdata["shipping_cost"], 0)
						row = row + 1
					
					# row = row + 1
				workbook.close()
				data = {
					"status":1,
					# "data":order_data,
					"message":"Report Created.",
					"file":file_name,
					"export_file_path":export_file_path
				}
			else:
				data = {
					"status":0,
					"message":"No data found.",
					"file":""
				}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={'ack':0,'api_status':traceback.format_exc(),'error_line':line,'error_message':str(error),'msg':str(error)}

		# return Response(order_data)
		return Response(data)

#-----Binayak Start----#
class ExportProductStock(generics.ListAPIView):
	permission_classes = []

	def post(self, request, format=None):
		requestdata = request.data

		warehouse_id = requestdata['warehouse_id']
		hide_out_of_stock = requestdata['hide_out_of_stock']

		try:
			# ************  Check file dir exist or not. If dir not exist then create
			file_dir = settings.MEDIA_ROOT + '/exportfile/'
			export_dir = settings.MEDIA_URL + 'exportfile/'
			if not os.path.exists(file_dir):
				os.makedirs(file_dir)
			# ************  Create file name

			rs_warehouse = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).values('code').first()
			if rs_warehouse and rs_warehouse['code'] is not None and rs_warehouse['code']!="":
				file_name = "stock_export_" + rs_warehouse['code'].strip()
			else:
				file_name = "stock_export_" + get_random_string(length=5)

			# Create file full path
			file_path = file_dir + file_name + '.xlsx'
			export_file_path = export_dir + file_name + '.xlsx'
			export_file_path = export_file_path[1:]

			workbook = xlsxwriter.Workbook(file_path)
			worksheet = workbook.add_worksheet()

			# p_stock = EngageboostProductStocks.objects.filter(warehouse_id=warehouse_id)
			stock_data = {}
			
			hide_out_of_stock = str(hide_out_of_stock)

			if hide_out_of_stock == "0":
				stock_data = EngageboostProductStocks.objects.filter(warehouse_id=warehouse_id,product__isdeleted='n').values('warehouse__name','warehouse__code', 'product__name', 'product__sku','stock', 'safety_stock', 'avg_sales_week', 'avg_sales_month', 'stock_unit', 'islot', 'islabel', 'virtual_stock', 'real_stock')

			else:
				stock_data = EngageboostProductStocks.objects.filter(warehouse_id=warehouse_id,product__isdeleted='n',real_stock__gt=0).values('warehouse__name','warehouse__code', 'product__name', 'product__sku','stock', 'safety_stock', 'avg_sales_week', 'avg_sales_month', 'stock_unit', 'islot', 'islabel', 'virtual_stock', 'real_stock')


			bold = workbook.add_format({'bold': True})
			row = 1

			worksheet.write(0, 0, 'WAREHOUSE CODE', bold)
			worksheet.write(0, 1, 'PRODUCT NAME', bold)
			worksheet.write(0, 2, 'PRODUCT SKU', bold)
			worksheet.write(0, 3, 'STOCK', bold)
			worksheet.write(0, 4, 'SAFETY STOCK', bold)
			# worksheet.write(0, 4, 'AVG. SALES WEEK', bold)
			# worksheet.write(0, 5, 'AVG. SALES MONTH', bold)
			# worksheet.write(0, 5, 'STOCK UNIT', bold)
			# worksheet.write(0, 7, 'IS LOT', bold)
			# worksheet.write(0, 8, 'IS LABEL', bold)
			# worksheet.write(0, 6, 'VIRTUAL STOCK', bold)
			worksheet.write(0, 5, 'REAL STOCK', bold)

			if stock_data:
				data = []
				for stockdata in stock_data:

					worksheet.write(row, 0, stockdata['warehouse__code'], 0)
					worksheet.write(row, 1, stockdata['product__name'], 0)
					worksheet.write(row, 2, stockdata['product__sku'], 0)
					worksheet.write(row, 3, stockdata['stock'], 0)
					worksheet.write(row, 4, stockdata['safety_stock'], 0)
					# worksheet.write(row, 4, stockdata['avg_sales_week'], 0)
					# worksheet.write(row, 5, stockdata['avg_sales_month'], 0)
					# shipping_row = row
					# worksheet.write(row, 5, stockdata['stock_unit'], 0)
					# worksheet.write(row, 7, stockdata['islot'], 0)
					# worksheet.write(row, 8, stockdata['islabel'], 0)
					# worksheet.write(row, 6, stockdata['virtual_stock'], 0)
					# qty = int(products["quantity"]) - int(products["deleted_quantity"]) - int(products["shortage"])
					worksheet.write(row, 5, stockdata['real_stock'], 0)
					row = row + 1

				# row = row + 1
				workbook.close()
				data = {
					"status": 1,
					# "data":order_data,
					"message": "Report Created.",
					"file": file_name,
					"export_file_path": export_file_path
				}
			else:
				data = {
					"status": 0,
					"message": "No data found.",
					"file": ""
				}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data = {'ack': 0, 'api_status': traceback.format_exc(), 'error_line': line, 'error_message': str(error),
					'msg': str(error)}

		# return Response(order_data)
		return Response(data)
#-----Binayak End-----#
