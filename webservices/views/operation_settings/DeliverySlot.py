from webservices.models import *
from django.http import Http404
from webservices.serializers import  DeliverySlotSerializer, OrderMasterSerializer, ZoneMastersSubAreaSerializer
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
from datetime import timedelta
from django.db.models import TimeField
from django.db.models.functions import Cast
import json





class DeliverySlotManager(generics.ListAPIView):

	def post(self, request):
		company_db = loginview.db_active_connection(request)
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		postdata=request.data

		#======================= Validation Part =====================================

		if not 'zone_id' in postdata.keys():
			return Response({"status":0, "Message":"Please send zone id"})

		if not EngageboostZoneMasters.objects.using(company_db).filter(id=postdata['zone_id'], location_type='Z').exists():
			return Response({"status":0, "Message":"Please send a valid zone id"})

		
		zone_id = postdata['zone_id']
		get_zone = EngageboostZoneMasters.objects.get(id=zone_id)

		zone_name = get_zone.name

		slot_records = postdata['slot_records']

		if not 'day_1' in slot_records.keys():
			return Response({'status':0, 'Message':'Please send record for Monday'})

		elif not 'day_2' in slot_records.keys():
			return Response({'status':0, 'Message':'Please send record for Tuesday'})

		elif not 'day_3' in slot_records.keys():
			return Response({'status':0, 'Message':'Please send record for Wednesday'})

		elif not 'day_4' in slot_records.keys():
			return Response({'status':0, 'Message':'Please send record for Thursday'})

		elif not 'day_5' in slot_records.keys():
			return Response({'status':0, 'Message':'Please send record for Friday'})

		elif not 'day_6' in slot_records.keys():
			return Response({'status':0, 'Message':'Please send record for Saturday'})

		elif not 'day_7' in slot_records.keys():
			return Response({'status':0, 'Message':'Please send record for Sunday'})


		query_set = EngageboostDeliverySlot.objects.filter(zone_id=zone_id).exclude(start_time__isnull=True,end_time__isnull=True,start_time="",end_time="").annotate(as_start_time=Cast('start_time', TimeField()), as_end_time=Cast('end_time', TimeField()))
		
		if query_set:
			for query in query_set:
				if query.as_start_time!=None and query.as_start_time!="" and query.as_end_time!=None and query.as_end_time!="": 
					if datetime.datetime.strptime(postdata['slot_start_time'], "%H:%M").time() > query.as_start_time and \
						datetime.datetime.strptime(postdata['slot_start_time'], "%H:%M").time() < query.as_end_time:
						
						return Response({'status':0, 'Message':'Your time slot is between another time slot'})

	

		if not 'all_slot_ids' in postdata.keys():

			if EngageboostDeliverySlot.objects.filter(zone_id=zone_id,  start_time=postdata['slot_start_time'], end_time=postdata['slot_end_time'], isdeleted='n').exists():
				return Response({'status':0, 'Message':zone_name+" already has same time slot"})
		else:
			for key, value in postdata['all_slot_ids'].items():
				if not EngageboostDeliverySlot.objects.filter(zone_id=zone_id, id=value).exists():
					return Response({'status':0, 'Message':'Please send valid slot record ids'})

		if datetime.datetime.strptime(postdata['slot_start_time'], "%H:%M") > datetime.datetime.strptime(postdata['slot_end_time'], "%H:%M"):
			return Response({'status':0, 'Message':"Slot start time can not be greater than slot end time"})
		for key in slot_records.keys():
			if slot_records[key] != 0 and slot_records[key] != "0":
				if "cutoff_time" in slot_records[key]:
					if (datetime.datetime.strptime(slot_records[key]['cutoff_time'], "%H:%M") >= datetime.datetime.strptime(postdata['slot_start_time'], "%H:%M")):
						return Response({'status':0, 'Message':"Cutt Off Time should not greater than slot start time."})
					

		#======================= Validation Part Ends =====================================

			#=================== Adding Records ====================

		if not 'all_slot_ids' in postdata.keys():

			for key in slot_records.keys():
				day_id = int(key[len(key)-1])
				# if EngageboostDeliverySlot.objects.filter(zone_id=zone_id).filter(Q())

				if slot_records[key] != 0 and slot_records[key] != "0": 
					if 'is_checked' in slot_records[key]:
						if slot_records[key]['is_checked']!=None and slot_records[key]['is_checked']!="" and slot_records[key]['is_checked']!=True:
							status = 'y'
						else:
							status = 'n'
					else:
						status = 'n'
					if 'based_on' in slot_records[key]:
						if slot_records[key]['based_on']!=None and slot_records[key]['based_on']!="":
							based_on = slot_records[key]['based_on']
						else:
							based_on = 'SameDay'
					else:
						based_on = 'SameDay'	 	
					create_record = EngageboostDeliverySlot.objects.create(location_id=0,
														zone_id=zone_id,
														day_id=day_id,
														start_time=postdata['slot_start_time'],
														end_time=postdata['slot_end_time'],
														cutoff_start=slot_records[key]['cutoff_time'],
														order_qty_per_slot=slot_records[key]['no_of_order'],
														based_on=based_on,
														isdeleted='n',
														isblocked=status,
														created=now_utc,
														modified=now_utc)

				else:
					create_record = EngageboostDeliverySlot.objects.create(location_id=0,
														zone_id=zone_id,
														day_id=day_id,
														order_qty_per_slot=0,
														isdeleted='n',
														isblocked='n',
														created=now_utc,
														modified=now_utc)

				send_data = {"status":1, "Message":'Records created successfully'}


			#=================== Editing Records ====================			

		else:

			for key in slot_records.keys():

				day_id = int(key[len(key)-1])

				record_id = postdata['all_slot_ids'][str(day_id-1)]

				#print(record_id)

				get_record = EngageboostDeliverySlot.objects.get(id=record_id)

				get_record.start_time = postdata['slot_start_time']
				get_record.end_time = postdata['slot_end_time']
				get_record.cutoff_start = slot_records[key]['cutoff_time']
				get_record.order_qty_per_slot=slot_records[key]['no_of_order']
				get_record.modified = now_utc

				get_record.save()


			send_data = {"status":1, "Message":'Records edited successfully'}
	

		return Response(send_data)

class get_all_sub_areas(generics.ListAPIView):
	
	def get(self, request,format=None):
		# $all_applicable_warehouse_id  = $this->get_applicable_warehouses_for_zones();
		keyword = self.request.GET.get("keyword")
		rs_all_area_subarea = EngageboostZoneMasters.objects.filter(isblocked='n', isdeleted='n', location_type='S').order_by('-id').all()
		if keyword:
			rs_all_area_subarea = rs_all_area_subarea.filter(Q(name__icontains=keyword)|Q(zipcode__icontains=keyword)).values('id', 'area_id', 'name', 'zipcode', 'zone_id')
		else:
			rs_all_area_subarea = rs_all_area_subarea[0:10]
			# data = {
			# 	"status":0,
			# 	"Message":"Provide some keyword."
			# }

		all_area_subarea = ZoneMastersSubAreaSerializer(rs_all_area_subarea, many=True)
		for suareadata in all_area_subarea.data:
			suareadata.update({'abbrev':suareadata['name']+"-"+suareadata["zipcode"]})

		data = {
			"status":1,
			"data":all_area_subarea.data
		}	
		return Response(data)

class DeliverySlotUpdate(generics.ListAPIView):

	def post(self, request):
		company_db = loginview.db_active_connection(request)
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		serializer_data=request.data

		days = ["sunday","monday","tuesday","wednesday","thursday","friday","saturday"]
		#======================= Validation Part =====================================
		for day_id,day in enumerate(days):
			post_datas = []
			day_id = int(day_id)+1
			if not day in serializer_data.keys():
				return Response({"status":0, "Message":"Please send data of "+day})
			
			EngageboostDeliverySlot.objects.filter(day_id=day_id).delete()
			post_datas = serializer_data[day]
			
			for postdata in post_datas:

				# if not 'zones' in postdata.keys():
				# 	return Response({"status":0, "Message":"Please send zone id","data":postdata})

				# for zone in postdata['zones']:
				# 	if not EngageboostZoneMasters.objects.using(company_db).filter(id=zone, location_type='Z').exists():
				# 		return Response({"status":0, "Message":"Please send a valid zone id","data":{day:[postdata]},"zone_id":zone})		
					
				# 	zone_id = zone

				# 	get_zone = EngageboostZoneMasters.objects.get(id=zone_id)

				# 	zone_name = get_zone.name	

				if not 'warehouse_ids' in  postdata.keys():	
					return Response({"status":0, "Message":"Please send warehouse id","data":postdata})

				for warehouse in postdata['warehouse_ids']:
					# if not EngageboostWarehouseMasters.objects.using(company_db).filter(id=warehouse, isblocked='n', isdeleted='n').exists():
					# 	return Response({"status":0, "Message":"Please send a valid warehouse id","data":{day:[postdata]},"warehouse_id":warehouse})

					warehouse_id = warehouse

					get_warehouse = EngageboostWarehouseMasters.objects.get(id=warehouse_id)

					warehouse_name = get_warehouse.name

					#======================= Validation Part Ends =====================================

					#=================== Adding Records ====================
					slot_records = postdata
					
					start_time=slot_records['start_time']
					end_time=slot_records['end_time']

					if datetime.datetime.strptime(start_time, "%H:%M") > datetime.datetime.strptime(end_time, "%H:%M"):
						return Response({
										'status':0,
										'Message':'Slot start time can not be greater than slot end time',
										'data':{day:[postdata]}
									})

					query_set = EngageboostDeliverySlot.objects.filter(warehouse_id=warehouse_id,day_id=day_id, based_on=postdata['based_on']).exclude(start_time__isnull=True,end_time__isnull=True,start_time="",end_time="").annotate(as_start_time=Cast('start_time', TimeField()), as_end_time=Cast('end_time', TimeField()))
					
					if query_set:
						for query in query_set:
							if query.as_start_time!=None and query.as_start_time!="" and query.as_end_time!=None and query.as_end_time!="": 
								if datetime.datetime.strptime(start_time, "%H:%M").time() >= query.as_start_time and \
									datetime.datetime.strptime(end_time, "%H:%M").time() <= query.as_end_time:
									
									return Response({
										'status':0,
										'Message':'Your time slot is between another time slot',
										'data':{day:[postdata]}
									})
					slots = slot_records
					if not 0 in slots and not "0" in slots:
									
						if 'is_checked' in slots.keys():
							if slots['is_checked']==None or slots['is_checked']=="" or (slots['is_checked']!=True and slots['is_checked']!=1):
								status = 'y'
							else:
								status = 'n'
						else:
							status = 'y'
						if 'based_on' in slots.keys():
							if slots['based_on']!=None and slots['based_on']!="":
								based_on = slots['based_on']
							else:
								based_on = 'SameDay'
						else:
							based_on = 'SameDay'	 	
						create_record = EngageboostDeliverySlot.objects.create(location_id=0,
															#zone_id=zone_id,
															warehouse_id=warehouse_id,
															day_id=day_id,
															start_time=start_time,
															end_time=end_time,
															cutoff_time=slots['cutoff_time'],
															order_qty_per_slot=slots['no_of_order'],
															based_on=based_on,
															isdeleted='n',
															isblocked=status,
															created=now_utc,
															modified=now_utc)
					else:
						create_record = EngageboostDeliverySlot.objects.create(location_id=0,
															#zone_id=zone_id,
															warehouse_id=warehouse_id,
															day_id=day_id,
															start_time=start_time,
															end_time=end_time,
															order_qty_per_slot=0,
															isdeleted='n',
															isblocked='n',
															created=now_utc,
															modified=now_utc)	
		send_data = {"status":1, "Message":'Records updated successfully'}
		return Response(send_data)

class DeliverySlotDelete(generics.ListAPIView):
	
	def post(self, request):
		# $all_applicable_warehouse_id  = $this->get_applicable_warehouses_for_zones();
		postdata=request.data

		zone_id = postdata['zone_id']
		start_time = postdata['start_time']
		end_time = postdata['end_time']
		
		count = EngageboostDeliverySlot.objects.filter(zone_id=zone_id,start_time=start_time,end_time=end_time).count()

		if count>0:
			EngageboostDeliverySlot.objects.filter(zone_id=zone_id,start_time=start_time,end_time=end_time).delete()

			data = {
				"status":1,
				"Message":"Deleted Successfully"
			}
		else:
			data = {
				"status":0,
				"Message":"No slots can be found"
			}
		return Response(data)

class DeliverySlotList(generics.ListAPIView):

	def get(self, request):
		company_db = loginview.db_active_connection(request)		
		days = ["sunday","monday","tuesday","wednesday","thursday","friday","saturday"]
		datas = []
		for day_id,day in enumerate(days):
			data = []
			day_id = int(day_id)+1
			# print(day_id)
			delveryObj = EngageboostDeliverySlot.objects.using(company_db).filter(isdeleted='n', day_id=day_id).distinct('start_time', 'end_time', 'based_on')

			if delveryObj.count()>0:
				delveryObj = delveryObj.all()
				deliverydata = DeliverySlotSerializer(delveryObj,many=True)

				for v in deliverydata.data:
					zone = []
					
					temp = EngageboostDeliverySlot.objects.using(company_db).filter(isdeleted='n', day_id=day_id,start_time=v['start_time'],end_time=v['end_time'], based_on=v['based_on'])
					if temp.count()>0:
						temp = temp.all()
						for j in temp:
							zone.append(j.warehouse_id)

						blocked=0
						if v["isblocked"]=="n":
							blocked=1
						d1 = {"warehouse_ids":zone,"no_of_order":v["order_qty_per_slot"],"is_checked":blocked}
						v = dict(v,**d1)
						v.pop("zone_id")
						v.pop("warehouse")
						v.pop("order_qty_per_slot")
						v.pop("isblocked")
					data.append(v)
			else:
				dy = {
						"based_on": "",
						"start_time": "",
						"no_of_order": "",
						"is_checked": 0,
						"cutoff_time": "",
						"warehouse_ids": [],
						"end_time": ""
					}
				data.append(dy)    
			datas.append({day:data}) 	
		send_data = {"status":1, "api_status":datas}
		return Response(send_data)		