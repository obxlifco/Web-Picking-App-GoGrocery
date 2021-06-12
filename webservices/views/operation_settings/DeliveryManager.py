from webservices.models import *
from django.http import Http404
from webservices.serializers import DeliveryManagerSerializer, DeliverySlotSerializer, DeliveryManagersSerializer
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import generics
from itertools import chain
from django.core import serializers
from django.http import HttpResponse
from webservices.views import loginview
from django.db.models import Q
import datetime
class DManagerMaster(generics.ListAPIView):
	def post(self, request):
		company_db = loginview.db_active_connection(request)
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		postdata=request.data
		seralizer_data = {}
		website_id = postdata['website_id'] if postdata.get("website_id") else None
		name = postdata['name'] if postdata.get("name") else None
		user_id = postdata['user_id'] if postdata.get("user_id") else None
		phone = postdata['phone'] if postdata.get("phone") else None
		email = postdata['email'] if postdata.get("email") else None
		zone = postdata['zone'] if postdata.get("zone") else None
		warehouse_ids = postdata['warehouse_ids'] if postdata.get("warehouse_ids") else None
		address1 = postdata['address1'] if postdata.get("address1") else None
		address2 = postdata['address2'] if postdata.get("address2") else None
		created = now_utc
		modified = now_utc
		isdeleted = 'n'
		isblocked = 'n'
		record_id = postdata['id']if postdata.get("id") else None
		serializer_data = {
			"website_id":website_id,
			"name":name,
			"user_id":user_id,
			"phone":phone,
			"email":email,
			"zone":zone,
			"warehouse_ids":warehouse_ids,
			"address1":address1,
			"address2":address2,
			"created":created,
			"modified":modified,
			"isdeleted":isdeleted,
			"isblocked":isblocked
		}
		if record_id:
			if EngageboostDeliveryManagers.objects.using(company_db).filter(id=record_id).exists():
				get_record = EngageboostDeliveryManagers.objects.get(id=record_id)
				serializer = DeliveryManagerSerializer(get_record, data=serializer_data,partial=True)
				if serializer.is_valid():
					serializer.save()
					data = {
						'status':1,
						'Message':'Data Updated Successfully',
					}
				else:
					data = {
						'status':0,
						'api_status':serializer.errors,
						'Message':'Error Occured',
					}
			else:
				data={"status":0,"message":"Please send a valid record id"}

		else:
			create_record = EngageboostDeliveryManagers.objects.using(company_db).create(**serializer_data)
			if create_record:
				data ={
				'status':1,
				'Message':'Data Saved Successfully',
				}
				
			else:
				data ={
				'status':0,
				'api_status':serializer.errors,
				'Message':'Error Occured',
				}
		return Response(data)

class DeliveryManagerLists(generics.ListAPIView):
	def post(self, request):
		postdata = request.data
		website_id = postdata['website_id']
		# warehouse_id = postdata['warehouse_id'] if postdata.get("warehouse_id") else None
		if website_id:
			pass
		else:
			website_id = 1
		rs = EngageboostDeliveryManagers.objects.filter(website_id = website_id, isdeleted='n', isblocked='n')
		# if warehouse_id is not None:
			# rs = rs.filter(warehouse_ids__iregex=r"\y{0}\y".format(warehouse_id))
		rs = rs.all().values('id', 'website_id', 'name', 'user_id', 'phone', 'email', 'zone', 'warehouse_ids',
							 'address1', 'address2').order_by('name')
		if rs:
			rs_data = DeliveryManagersSerializer(rs, many=True)
			data = {
				"status":1,
				"data":rs_data.data
			}
		else:
			data = {
				"status":0,
				"data":[]
			}
		return Response(data)

class DeliveryManagerDetails(generics.ListAPIView):
	 #///////////////////Fetch Single Row
	def get(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		managers=EngageboostDeliveryManagers.objects.using(company_db).all().filter(id=pk)
		if managers:
			managers_data = DeliveryManagersSerializer(managers, many=True)
			data_dict = managers_data.data
			#print()
			warehouse_ids = data_dict[0]['warehouse_ids']
			warehouse_names = []
			if warehouse_ids!=None:
				warehouseIdsArr = warehouse_ids.split(',')
				if len(warehouseIdsArr) > 0:
					warehouse_names = EngageboostWarehouseMasters.objects.filter(id__in=warehouseIdsArr).values_list('name', flat=True)
					data_dict[0].update({'warehouse_ids' : warehouseIdsArr})
				data_dict[0].update({'zone_warehouse': warehouse_names})
			data = {
				"status":1,
				"data":data_dict
			}
		else:
			data = {
				"status":0,
				"data":[]
			}
		return Response(data)
