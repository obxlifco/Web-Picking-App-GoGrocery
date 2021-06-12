from webservices.models import *
from django.http import Http404
from webservices.serializers import ZoneMastersSerializer, UserSerializer, VehicleMasterSerializer
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
import sys,os,math
import traceback
import datetime
from django.core.files.storage import FileSystemStorage
import xlrd as xl
import xlwt as xlw
from webservices.views.common import get_statename
class VehicleMaster(generics.ListAPIView):
	def post(self, request):
		company_db = loginview.db_active_connection(request)
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		postdata=request.data
		
		vehicle_name = postdata['vehicle_name'] if postdata.get("vehicle_name") else None
		vehicle_description = postdata['vehicle_description'] if postdata.get("vehicle_description") else None
		
		vehicle_number = postdata['vehicle_number'] if postdata.get("vehicle_number") else None
		manager_id = postdata['manager_id'] if postdata.get("manager_id") else None
		warehouse_ids = postdata['warehouse_ids'] if postdata.get("warehouse_ids") else None
		model_no = postdata['model_no'] if postdata.get("model_no") else None
		website_id = postdata['website_id'] if postdata.get("website_id") else None
		country_id = postdata['country_id'] if postdata.get("country_id") else None
		zip_code = postdata['zip_code'] if postdata.get("zip_code") else None
		address2 = postdata['address2'] if postdata.get("address2") else None
		state_id = postdata['state_id'] if postdata.get("state_id") else None
		# state_name = postdata['state_name'] if postdata.get("state_name") else None
		city = postdata['city'] if postdata.get("city") else None
		address1 = postdata['address1'] if postdata.get("address1") else None
		phone_number = postdata['phone_number'] if postdata.get("phone_number") else None
		record_id = postdata['id']if postdata.get("id") else None
		if state_id:
			state_name = get_statename(state_id)
		else:
			state_name = ""
		if record_id:
			get_record = EngageboostVehicleMasters.objects.get(id=record_id)
			if get_record:
				get_record.vehicle_name = vehicle_name
				get_record.vehicle_description = vehicle_description
				get_record.vehicle_number = vehicle_number
				get_record.manager_id = manager_id
				get_record.warehouse_ids = warehouse_ids
				get_record.model_no = model_no
				get_record.website_id = website_id
				get_record.country_id = country_id
				get_record.zip_code = zip_code
				get_record.address2 = address2
				get_record.state_id = state_id
				get_recordstate_name = state_name
				get_record.city = city
				get_record.address1 = address1
				get_record.phone_number = phone_number
				get_record.modified=now_utc
				get_record.save()
				data={"status":1,"Message":"Vehicle Record Saved Successfully"}
			else:
				data={"status":0,"Message":"Please send a valid record id"}
		else:
			if EngageboostVehicleMasters.objects.using(company_db).filter(vehicle_number=vehicle_number).exists():
				return Response({"status":0, "Message":"Record already Exists"})

			EngageboostVehicleMasters.objects.create(vehicle_name = vehicle_name,
													vehicle_number = vehicle_number,
													vehicle_description = vehicle_description,
													manager_id = manager_id,
													warehouse_ids = warehouse_ids,
													model_no = model_no,
													website_id = website_id,
													country_id = country_id,
													zip_code = zip_code,
													address2 = address2,
													state_id = state_id,
													state_name = state_name,
													city = city,
													address1 = address1,
													phone_number = phone_number,
													created=now_utc,
													modified=now_utc)

			data={"status":1,"Message":"Vehicle created sucessfully"}
		return Response(data)

	def get(self, request, pk):
		get_vehicle_record = EngageboostVehicleMasters.objects.get(id=pk)
		serializer = VehicleMasterSerializer(get_vehicle_record)
		data_dict = serializer.data
		warehouse_ids = data_dict['warehouse_ids']
		warehouse_names = []
		warehouseidsArr = warehouse_ids.split(',')
		if len(warehouseidsArr) > 0:
			warehouse_names = EngageboostWarehouseMasters.objects.filter(id__in=warehouseidsArr).values_list('name', flat=True)
		#if zone_ids.find(',') >-1:
		else:
			warehouse_names = EngageboostWarehouseMasters.objects.get(id=warehouse_ids).values_list('name', flat=True)
		print(data_dict['manager_id'])
		if data_dict['manager_id'] and int(data_dict['manager_id']) > 0:
			get_manager = EngageboostDeliveryManagers.objects.get(id=data_dict['manager_id'])
			data_dict.update({'manager_name': get_manager.name})
		else :
			pass
		if len(warehouse_names) > 1:
			data_dict.update({'warehouse_names' : ','.join(warehouse_names)})
		else:
			data_dict.update({'warehouse_names': warehouse_names[0]})

		data = {"status":1, "Message":'success', 'data':data_dict}
		return Response(data)






