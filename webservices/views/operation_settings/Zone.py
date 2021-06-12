from webservices.models import *
from django.http import Http404
from webservices.serializers import ZoneMastersSerializer, UserSerializer
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
from settings.settings import directory
from django.db.models import CharField
from django.db.models.functions import Cast
import random, string
from webservices.views.common import get_statename


class ZoneAdd(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		postdata=request.data
		location_types = ["A","S","Z"]
		
		zipcodes = postdata['zipcode'] if postdata.get("zipcode") else None

		location_type = postdata['location_type'] if postdata.get("location_type") else None

		if not location_type in location_types:
			return JsonResponse({"status":0, "Message":"Please send a valid Location Type"})


		if location_type == "A":
			if not 'zone_id' in postdata or postdata['zone_id'] == None:
				return Response({"status":0, "Message":"Please Provide Area ID"})

		elif location_type == "S":
			if not 'zone_id' in postdata or postdata['zone_id'] == None:
				return Response({"status":0, "Message": "Please Provide Area ID"})

			if not 'area_id' in postdata or postdata['area_id'] == None:
				return Response({"status":0, "Message": "Please Provide Area ID"})


		name = postdata['name'] if postdata.get("name") else None
		zone_id = postdata['zone_id'] if postdata.get("zone_id") else 0
		area_id = postdata['area_id'] if postdata.get("area_id") else 0
		website_id = postdata['website_id'] if postdata.get("website_id") else None
		country_id = postdata['country_id'] if postdata.get("country_id") else 0
		state_id = postdata['state_id'] if postdata.get("state_id") else 0
		# state_name = postdata['state_name'] if postdata.get("state_name") else None
		city = postdata['city'] if postdata.get("city") else None
		manager_id = postdata['manager_id'] if postdata.get("manager_id") else None
		warehouse_id = postdata['warehouse_id'] if postdata.get("warehouse_id") else None
		office_address1 = postdata['address1'] if postdata.get("address1") else None
		office_address2 = postdata['address2'] if postdata.get("address2") else None
		phone_number = postdata['phone_number'] if postdata.get("phone_number") else None
		distance = postdata['distance']if postdata.get("distance") else None
		record_id = postdata['id']if postdata.get("id") else None
		min_order_amount = postdata['min_order_amount']if postdata.get("min_order_amount") else None


		if location_type == "Z":
			state_name = get_statename(state_id)
			if not state_name:
				return Response({"status":0, "Message": "Invalid State Id."})


		created = now_utc
		if record_id:		

			if EngageboostZoneMasters.objects.filter(id=record_id, location_type=location_type).exists():
				get_record = EngageboostZoneMasters.objects.get(id=record_id, location_type=location_type)

				if location_type == 'Z':

					if zipcodes:
						zipcode_records = EngageboostZoneZipcodeMasters.objects.filter(zone_id=record_id)
						zipcode_records.delete()

						if zipcodes.find(","):
							for zipcode in zipcodes.split(','):
								if not EngageboostZoneZipcodeMasters.objects.filter(zip_code=zipcode).exists():
									EngageboostZoneZipcodeMasters.objects.create(zone_id=get_record.id,
																	zip_code=zipcode,
																	created=created,
																	modified=created)
						else:
							if not EngageboostZoneZipcodeMasters.objects.filter(zip_code=zipcodes).exists():
								EngageboostZoneZipcodeMasters.objects.create(zone_id=get_record.id,
																	zip_code=zipcodes,
																	created=created,
																	modified=created)
					
					get_record.state_id = state_id
					get_record.country_id = country_id
					get_record.city = city

				elif location_type == 'A' or location_type == 'S':
					get_record.zone_id = zone_id


					if location_type == 'S':
						get_record.area_id = area_id
						get_record.min_order_amount = min_order_amount


				get_record.name=name
				get_record.location_type=location_type

				if website_id:
					get_record.website_id=website_id

				if manager_id:
					get_record.manager_id=manager_id

				if warehouse_id:
					get_record.warehouse_id=warehouse_id

				if office_address1:
					get_record.office_address1=office_address1

				if office_address2:
					get_record.office_address2=office_address2

				if phone_number:
					get_record.phone_number=phone_number
				
				get_record.modified=created

				get_record.save()

				if location_type == 'Z':
					data={"status":1,"Message":"Zone Record Updated Successfully"}
				elif location_type == 'A':
					data={"status":1,"Message":"Area Record Updated Successfully"}
				elif location_type == 'S':
					data={"status":1,"Message":"Subarea Record Updated Successfully"}


			else:
				data={"status":0,"Message":"Please send a valid record id"}

		else:

			if EngageboostZoneMasters.objects.using(company_db).filter(name=name, location_type=location_type).exists():
				return Response({"status":0, "Message":"Record already Exists"})


			create_record = EngageboostZoneMasters.objects.create(name=name,
																	location_type=location_type,
																	website_id=website_id,
																	manager_id=manager_id,
																	warehouse_id=warehouse_id,
																	office_address1=office_address1,
																	office_address2=office_address2,
																	phone_number=phone_number,
																	created=created,
																	modified=created)

			if location_type == "Z":

				create_record.state_id = state_id

				create_record.country_id = country_id
				create_record.city = city
				create_record.save()

				if zipcodes:
					if zipcodes.find(","):
						for zipcode in zipcodes.split(','):
							if not EngageboostZoneZipcodeMasters.objects.filter(zip_code=zipcode).exists():
								EngageboostZoneZipcodeMasters.objects.create(zone_id=create_record.id,
																zip_code=zipcode,
																created=created,modified=created)
							
					else:
						if EngageboostZoneZipcodeMasters.objects.filter(zip_code=zipcodes).exists():
							EngageboostZoneZipcodeMasters.objects.create(zone_id=create_record.id,
																zip_code=zipcodes,
																created=created,modified=created)

			elif location_type == 'A' or location_type == 'S':

				create_record.zone_id = zone_id

				if location_type == 'S':
					create_record.area_id = area_id

					#EngageboostZoneMasters.objects.filter(id=create_record.id).update(min_order_amount=min_order_amount)

					create_record.min_order_amount = min_order_amount
					if zipcodes:
						create_record.zipcode = zipcodes

				create_record.save()

			if location_type == 'Z':
				data={"status":1,"Message":"Zone Record Saved Sucessfully"}

			elif location_type == 'A':
				data={"status":1,"Message":"Area Record Saved Sucessfully"}

			elif location_type == 'S':
				data={"status":1,"Message":"Subarea Record Saved Sucessfully"}



		return Response(data)

		

	def get(self, request):
		company_db = loginview.db_active_connection(request)
		all_zones = EngageboostZoneMasters.objects.using(company_db).filter(location_type='Z', isdeleted='n',
																			isblocked='n').values('id','name').order_by('name')

		print(all_zones)

		return Response({'status':1, "Message":'success', 'data':all_zones})



class Get_Zone_Idbased(generics.ListAPIView):
	def get(self, request, pk):
		try:
			if not EngageboostZoneMasters.objects.filter(id=pk, isdeleted='n', isblocked='n').exists():
				return Response({'status':0, 'Message':'Please Provide a valid record id'})
		except Exception as e:
			print(str(e))

		try:
			get_record = EngageboostZoneMasters.objects.get(id=pk, isdeleted='n', isblocked='n')
		except Exception as e:
			print(str(e))

		if get_record.location_type == 'Z':
			try:
				get_zipcodes = EngageboostZoneZipcodeMasters.objects.filter(zone=get_record).values_list('zip_code',flat=True)

				zipcode = ','.join(get_zipcodes)

			except:
				zipcode = None
		else:
			zipcode = get_record.zipcode

		data_dict = {"id": get_record.id,
					"name": get_record.name,
					"zipcode": zipcode,
					"location_type": get_record.location_type,
					"zone_id": get_record.zone_id,
					"area_id": get_record.area_id,
					"website_id": get_record.website_id,
					"country_id": get_record.country_id,
					"state_id": get_record.state_id,
					"state_name": get_record.state_name,
					"city": get_record.city,
					"manager_id": get_record.manager_id,
					"min_order_amount": get_record.min_order_amount,
					"warehouse_id": get_record.warehouse_id,
					"office_address1": get_record.office_address1,
					"office_address2" : get_record.office_address2,
					"phone_number": get_record.phone_number,
					"distance": get_record.distance,
					"created": get_record.created,
					"modified": get_record.modified,
					"isblocked": get_record.isblocked,
					"isdeleted": get_record.isdeleted}

		data = {"status":1, "Message": "Success", "data": data_dict}

		return Response(data)
	



class ManagerList(generics.ListAPIView):
	def get(self, request):
		user_records = EngageboostUsers.objects.all().filter(isdeleted='n', isblocked='n',user_type='backend').order_by('employee_name')
		
		user_serializer =  UserSerializer(user_records, many=True)

		return Response({"status":1, "users":user_serializer.data})



class ManagerListWareHouse(generics.ListAPIView):
	def get(self, request, pk):
		record_id = pk
		warehouse_records = EngageboostWarehouseManager.objects.filter(warehouse_id=record_id)
		manager_id_list = []
		for item in warehouse_records:
			manager_id_list.append(item.manager_id)
		data_array = []
		user_records = EngageboostUsers.objects.filter(isdeleted='n',isblocked='n')

		for user in user_records:
			if user.id in manager_id_list:
				data ={"id":user.id,"username":user.username,"first_name":user.first_name,"last_name":user.last_name}
				data_array.append(data)
		return Response({"status":1, "users":data_array})




class ZipCodeManager(generics.ListAPIView):
	def post(self, request):
		uploaded_file = request.FILES['import_file']
		fs = FileSystemStorage()
		filename = fs.save(uploaded_file.name, uploaded_file)
		uploaded_file_url = directory + uploaded_file.name
		zip_codes = ''

		if uploaded_file.name.split(".")[1].lower() == 'xls' or uploaded_file.name.split(".")[1].lower() == 'xlsx':
			try:
				wb = xl.open_workbook(uploaded_file_url)
				sheet = wb.sheet_by_index(0)
			except Exception as e:
				print("Error : ",str(e))
				return JsonResponse({"status":0, "Message":str(e)})
			try:
				for row in range(sheet.nrows):
					zip_codes = zip_codes + str(int(sheet.cell(row,0).value)) + ','
			except Exception as e:
				return JsonResponse({"status":0, "Message":str(e)})

		elif uploaded_file.name.split(".")[1].lower() == 'csv':
			with open(uploaded_file_url) as file:
				lines = file.readlines()
			for line in lines:
				if line.find(",") > -1:
					for ln in line.split(','):
						if ln.find('\n'):
							ln = ln.replace('\n', '')
						zip_codes = zip_codes+ln+','
				else:
					if line.find('\n') > -1:
						line = line.replace('\n', '')
					zip_codes = zip_codes + line + ','


		zip_codes = zip_codes[:-1]
		os.remove(uploaded_file_url)

		return JsonResponse({"status":1, "Message":"Done", "zipcodes":zip_codes})





class ImportArea(generics.ListAPIView):
	def post(self, request):
		uploaded_file = request.FILES['import_file']
		postdata = request.data
		website_id = postdata['website_id'] if postdata.get("website_id") else None
		
		fs = FileSystemStorage()
		filename = fs.save(uploaded_file.name, uploaded_file)
		uploaded_file_url = directory + uploaded_file.name

		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()

		data_list = []

		if uploaded_file.name.split(".")[1].lower() == 'xls' or uploaded_file.name.split(".")[1].lower() == 'xlsx':
			try:
				wb = xl.open_workbook(uploaded_file_url)
				sheet = wb.sheet_by_index(0)
			except Exception as e:
				print("Error : ",str(e))
				return JsonResponse({"status":0, "Message":str(e)})
			
			for row in range(sheet.nrows):
				if row == 0:
					continue
				try:
					data_list.append({
						"zone": str(sheet.cell(row,0).value),
						"area": str(sheet.cell(row,1).value),
						"sub_area": str(sheet.cell(row,2).value),
						"zipcode": str(int(sheet.cell(row,3).value)),
						"min_order_amount": str(sheet.cell(row,4).value)
						})

				except Exception as e:
					return Response({'status':0, 'Message':str(e)})


		elif uploaded_file.name.split(".")[1].lower() == 'csv':

			with open(uploaded_file_url) as file:
				lines = file.readlines()
			count =0
			for line in lines:
				if count == 0:
					count = count +1
					continue

				if line.find('\n'):
					temp_line = line.replace('\n', '')

				if temp_line.find(','):
					temp_line = temp_line.split(',')

				data_list.append({"zone": temp_line[0],
									"area": temp_line[1],
									"sub_area": temp_line[2],
									"zipcode": temp_line[3],
									"min_order_amount": temp_line[4]
									})

		else:
			return Response({"status":0, 'Message':'Please upload a valid file.'})

		os.remove(uploaded_file_url)

		for data in data_list:
			### check from zone name . if exist then fetch zone_id else create new zone and get zone id 

			if EngageboostZoneMasters.objects.filter(name=data['zone'], location_type='Z').exists():
				get_zone_record = EngageboostZoneMasters.objects.get(name=data['zone'])
				get_zone_id = get_zone_record.id

				if not EngageboostZoneZipcodeMasters.objects.filter(zip_code=data['zipcode'], zone_id=get_zone_id).exists():
					create_zip_record = EngageboostZoneZipcodeMasters.objects.create(zone_id=get_zone_id ,zip_code=data['zipcode'],created=now_utc)

				

				if EngageboostZoneMasters.objects.filter(zone_id=get_zone_id, name=data['area'], location_type='A').exists():
					
					get_area_record = EngageboostZoneMasters.objects.get(zone_id=get_zone_id, name=data['area'], location_type='A')

					get_area_id = get_area_record.id

					if not EngageboostZoneMasters.objects.filter(zone_id=get_zone_id, name=data['sub_area'], area_id=get_area_id, location_type='S').exists():
						create_subare_record = EngageboostZoneMasters.objects.create(zone_id=get_zone_id, name=data['sub_area'], area_id=get_area_id, location_type='S', 
																					created=now_utc, isblocked='n', isdeleted='n',zipcode=data['zipcode'], website_id=website_id)

						EngageboostZoneMasters.objects.filter(id=create_subare_record.id).update(min_order_amount=data['min_order_amount'])

				else:
					create_area_record = EngageboostZoneMasters.objects.create(zone_id=get_zone_id, 
																				name=data['area'], 
																				location_type='A', 
																				area_id=0, 
																				created=now_utc, 
																				isblocked='n', 
																				isdeleted='n',
																				zipcode=data['zipcode'],
																				website_id=website_id)

					create_subarea_record = EngageboostZoneMasters.objects.create(zone_id=get_zone_id, name=data['sub_area'], area_id=create_area_record.id, 
																					location_type='S', created=now_utc, isblocked='n', isdeleted='n', zipcode=data['zipcode'],
																					website_id=website_id)
					EngageboostZoneMasters.objects.filter(id=create_subarea_record.id).update(min_order_amount=data['min_order_amount'])

			else:
				create_zone = EngageboostZoneMasters.objects.create(name=data['zone'], location_type='Z', zone_id=0, area_id=0, created=now_utc, isblocked='n', isdeleted='n', 
																	website_id=website_id)

				get_zone_id = create_zone.id

				if not EngageboostZoneZipcodeMasters.objects.filter(zip_code=data['zipcode']).exists():
					create_zip_record = EngageboostZoneZipcodeMasters.objects.create(zone_id=get_zone_id ,zip_code=data['zipcode'],created=now_utc)

				create_area_record = EngageboostZoneMasters.objects.create(zone_id=get_zone_id, 
																			name=data['area'], 
																			location_type='A', 
																			area_id=0, 
																			created=now_utc, 
																			isblocked='n', 
																			isdeleted='n',
																			zipcode=data['zipcode'],
																			website_id=website_id)

				create_subarea_record = EngageboostZoneMasters.objects.create(zone_id=get_zone_id, 
																				name=data['sub_area'], 
																				area_id=create_area_record.id, 
																				location_type='S', 
																				created=now_utc, 
																				isblocked='n', 
																				isdeleted='n',
																				zipcode=data['zipcode'],
																				website_id=website_id)

				EngageboostZoneMasters.objects.filter(id=create_subarea_record.id).update(min_order_amount=data['min_order_amount'])

		return Response({'status':1, 'Message':'All records added successfully'})





class ExportArea(generics.ListAPIView):

	def post(self, request):
		company_db = loginview.db_active_connection(request)

		response = HttpResponse(content_type='application/ms-excel')
		response['Content-Disposition'] = 'attachment; filename="export.xls"'

		postdata = request.data

		location_type = postdata['location_type']
		search_filter = postdata['search_filter']

		if search_filter != "":

			if EngageboostZoneZipcodeMasters.objects.filter(zip_code=search_filter).exists():
				zone_idlist = list(EngageboostZoneZipcodeMasters.objects.filter(zip_code=search_filter).distinct().values_list('zone_id', flat=True))

				zone_records = EngageboostZoneMasters.objects.using(company_db).filter(id__in=zone_idlist, website_id=postdata['website_id'])

			else:
				zone_records = EngageboostZoneMasters.objects.using(company_db).filter(location_type=location_type, name=search_filter, website_id=postdata['website_id'])

		elif location_type != "":
			zone_records = EngageboostZoneMasters.objects.using(company_db).filter(location_type=location_type, website_id=postdata['website_id'])

		else:
			zone_records = EngageboostZoneMasters.objects.using(company_db).filter(website_id=postdata['website_id'])

		area_count = zone_records.count()

		data_array = []
		temp_dict = {}

		if area_count > 0:

			if location_type == 'Z':

				zone_idlist = zone_records.values_list('id', flat=True)

				for ids in zone_idlist:

					if EngageboostZoneZipcodeMasters.objects.filter(zone_id=ids).exists():
						zip_code = EngageboostZoneZipcodeMasters.objects.filter(zone_id=ids).last()

					if EngageboostZoneMasters.objects.using(company_db).filter(location_type='A', zone_id=ids).exists():
						areas = EngageboostZoneMasters.objects.using(company_db).filter(location_type='A', zone_id=ids).values('id', 'name', 'isdeleted', 'isblocked')

						for area in areas:
							if EngageboostZoneMasters.objects.using(company_db).filter(location_type='S',area_id=area['id'], zone_id=ids).exists():
								sub_areas = EngageboostZoneMasters.objects.using(company_db).filter(location_type='S',area_id=area['id'], zone_id=ids).values('name', 'isdeleted', 'isblocked')

								for sub_area in sub_areas:
									temp_dict['subarea'] = sub_area['name']
									temp_dict['area'] = area['name']
									get_zone = EngageboostZoneMasters.objects.get(id=ids)

									temp_dict['zone'] = get_zone.name								

									temp_dict['zipcode'] = zip_code.zip_code

									if sub_area['isdeleted'] == 'n' and sub_area['isblocked'] == 'n':
										temp_dict['status'] = 'Active'
									else:
										temp_dict['status'] = 'Inactive'

									data_array.append(temp_dict)
									temp_dict = {}

							else:
								temp_dict['area'] = area['name']
								get_zone = EngageboostZoneMasters.objects.get(id=ids)

								temp_dict['zone'] = get_zone.name

								temp_dict['zipcode'] = zip_code.zip_code

								if area['isdeleted'] == 'n' and area['isblocked'] == 'n':
									temp_dict['status'] = 'Active'
								else:
									temp_dict['status'] = 'Inactive'
								

								data_array.append(temp_dict)
								temp_dict = {}

					else:

						get_zone = EngageboostZoneMasters.objects.get(id=ids).values('name', 'isdeleted', 'isblocked')

						temp_dict['zone'] = get_zone['name']

						if EngageboostZoneZipcodeMasters.objects.filter(zone_id=ids).exists():
							zip_code = EngageboostZoneZipcodeMasters.objects.filter(zone_id=ids).last().values('zip_code')

							temp_dict['zipcode'] = zip_code['zip_code']

						if get_zone['isdeleted'] == 'n' and get_zone['isblocked'] == 'n':
							temp_dict['status'] = 'Active'
						else:
							temp_dict['status'] = 'Inactive'


						data_array.append(temp_dict)
						temp_dict = {}


			elif location_type == 'A':
				
				for area in zone_records:
					if EngageboostZoneMasters.objects.using(company_db).filter(area_id=area.id, location_type='S').exists():
						get_subarea = EngageboostZoneMasters.objects.using(company_db).filter(area_id=area.id, location_type='S').values('name', 'isdeleted', 'isblocked')

						for sub_area in get_subarea:
							temp_dict['subarea'] = sub_area['name']
							temp_dict['area'] = area.name

							get_zone = EngageboostZoneMasters.objects.get(id=area.zone_id)				

							temp_dict['zone'] = get_zone.name

							if EngageboostZoneZipcodeMasters.objects.filter(zone_id=area.zone_id).exists():
								zip_code = EngageboostZoneZipcodeMasters.objects.filter(zone_id=area.zone_id).last()

								temp_dict['zipcode'] = zip_code.zip_code

							if sub_area['isdeleted'] == 'n' and sub_area['isblocked'] == 'n':
								temp_dict['status'] = 'Active'
							else:
								temp_dict['status'] = 'Inactive'

						data_array.append(temp_dict)
						temp_dict = {}

					else:
						temp_dict['area'] = area.name

						get_zone = EngageboostZoneMasters.objects.get(id=area.zone_id)

						temp_dict['zone'] = get_zone.name

						if EngageboostZoneZipcodeMasters.objects.filter(zone_id=area.zone_id).exists():
							zip_code = EngageboostZoneZipcodeMasters.objects.filter(zone_id=area.zone_id).last()

							temp_dict['zipcode'] = zip_code.zip_code

						if area['isdeleted'] == 'n' and area['isblocked'] == 'n':
							temp_dict['status'] = 'Active'
						else:
							temp_dict['status'] = 'Inactive'

						data_array.append(temp_dict)
						temp_dict = {}

			elif location_type == 'S':
				for subarea in zone_records:

					temp_dict['subarea'] = subarea.name

					if EngageboostZoneMasters.objects.using(company_db).filter(id=subarea.area_id).exists():
						get_area = EngageboostZoneMasters.objects.filter(id=subarea.area_id).last()
						temp_dict['area'] = get_area.name

					else:
						temp_dict['area'] = ""


					get_zone = EngageboostZoneMasters.objects.get(id=subarea.zone_id)

					temp_dict['zone'] = get_zone.name

					if EngageboostZoneZipcodeMasters.objects.using(company_db).filter(zone_id=subarea.zone_id).exists():
						zip_code = EngageboostZoneZipcodeMasters.objects.filter(zone_id=subarea.zone_id).last()

						temp_dict['zipcode'] = zip_code.zip_code

					if subarea.isdeleted == 'n' and subarea.isblocked == 'n':
						temp_dict['status'] = 'Active'
					else:
						temp_dict['status'] = 'Inactive'

					data_array.append(temp_dict)
					temp_dict = {}

			else:
				for zone in zone_records:

					if EngageboostZoneMasters.objects.using(company_db).filter(location_type='A', zone_id=zone.id).exists():
						areas = EngageboostZoneMasters.objects.using(company_db).filter(location_type='A', zone_id=zone.id).values('id', 'name', 'isdeleted', 'isblocked')

						for area in areas:
							if EngageboostZoneMasters.objects.using(company_db).filter(location_type='S',area_id=area['id'], zone_id=zone.id).exists():
								sub_areas = EngageboostZoneMasters.objects.using(company_db).filter(location_type='S',area_id=area['id'], zone_id=zone.id).values('name', 'isdeleted', 'isblocked')

								for sub_area in sub_areas:
									temp_dict['subarea'] = sub_area['name']
									temp_dict['area'] = area['name']
									temp_dict['zone'] = zone.name								
									temp_dict['zipcode'] = search_filter

									if sub_area['isdeleted'] == 'n' and sub_area['isblocked'] == 'n':
										temp_dict['status'] = 'Active'
									else:
										temp_dict['status'] = 'Inactive'

									data_array.append(temp_dict)
									temp_dict = {}

							else:
								temp_dict['subarea'] = ""
								temp_dict['area'] = area['name']
								temp_dict['zone'] = zone.name
								temp_dict['zipcode'] = search_filter

								if area['isdeleted'] == 'n' and area['isblocked'] == 'n':
									temp_dict['status'] = 'Active'
								else:
									temp_dict['status'] = 'Inactive'

								data_array.append(temp_dict)
								temp_dict = {}
					else:
						temp_dict['subarea'] = ""
						temp_dict['area'] = ""
						temp_dict['zone'] = zone.name								
						temp_dict['zipcode'] = search_filter

						if zone.isdeleted == 'n' and zone.isblocked == 'n':
							temp_dict['status'] = 'Active'
						else:
							temp_dict['status'] = 'Inactive'

						data_array.append(temp_dict)
						temp_dict = {}


		else:
			data = {"status":0, "Message": "Sorry did not get any record"}
			return Response(data)

		# file_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

		file_name = "zone-area-subarea.xls"

		uploaded_file_url = directory + 'exportfile/'+ file_name

		wb = xlw.Workbook(encoding='utf-8')
		ws = wb.add_sheet('Sheet1')

		columns = ['Zone', 'Area', 'Sub-Area', 'Pincode', 'Status']

		for col_num in range(len(columns)):
			ws.write(0, col_num, columns[col_num])

		for index, row in enumerate(data_array):

			if 'zone' in row.keys():
				ws.write(index+1, 0, row['zone'])
			else:
				ws.write(index+1, 0, "")

			if 'area' in row.keys():
				ws.write(index+1, 1, row['area'])
			else:
				ws.write(index+1, 1, "")

			if 'subarea' in row.keys():
				ws.write(index+1, 2, row['subarea'])
			else:
				ws.write(index+1, 2, "")

			ws.write(index+1, 3, row['zipcode'])
			
			ws.write(index+1, 4, row['status'])

		try:

			wb.save(uploaded_file_url)

		except Exception as e:
			data = {"status":0,
					"Message": "error happened",
					"api_error": str(e)}
		# wb.save(response)

		data = {"status":1,
				"Message": "Success",
				"file_link": "/media/exportfile/"+file_name}
		
		return Response(data)


	

class Get_Zipcodes(generics.ListAPIView):
	def post(self, request):
		company_db = loginview.db_active_connection(request)
		# now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		postdata=request.data
		zone_id = postdata['zone_id'] if postdata.get("zone_id") else 0

		if zone_id:
			if not EngageboostZoneZipcodeMasters.objects.filter(zone_id=zone_id, isblocked='n', isdeleted='n').exists():
				return Response({'status':0, "Message":" Invalid Zone ID Provided"})

			zipcode_dict = EngageboostZoneZipcodeMasters.objects.filter(zone_id=zone_id, isblocked='n',
																		isdeleted='n').values('id','zip_code').order_by('zip_code')

			zipcode_list = [zipcode for zipcode in zipcode_dict]
		
			data = {"status":1, "Message": "Success", "data": zipcode_list}

			return Response(data)
			
		else:
			return Response({'status':0, "Message":" Invalid Request Provided"})



class Get_Areanames(generics.ListAPIView):
	def post(self, request):
		company_db = loginview.db_active_connection(request)
		# now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		postdata=request.data
		zone_id = postdata['zone_id'] if postdata.get("zone_id") else 0

		if zone_id:
			if not EngageboostZoneMasters.objects.filter(zone_id=zone_id, isblocked='n', 
														isdeleted='n', location_type='A').exists():
				return Response({'status':0, "Message":" Invalid Zone ID Provided"})

			area_list = EngageboostZoneMasters.objects.filter(zone_id=zone_id, isblocked='n',
															  isdeleted='n', location_type='A').values('id','name').order_by('name')

			area_list = [area for area in area_list]

			data = {"status":1, "Message": "Success", "data": area_list}

			return Response(data)

		else:
			return Response({'status':0, "Message":" Invalid Request Provided"})