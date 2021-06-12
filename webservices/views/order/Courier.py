from webservices.models import EngageboostPresets,EngageboostShippingMasters,EngageboostShippingServiceNames,EngageboostShippingPackagingtype,EngageboostShippingZipcodes,EngageboostAwbMasters,EngageboostGridLayouts,EngageboostGridColumnLayouts,EngageboostOrdermaster,EngageboostGlobalSettings
from django.http import Http404
from webservices.serializers import PresetsSerializer,ShippingSerializer,ShippingServiceNamesSerializer,PackagSerializer,ShippingMastersSettingsSerializer,AwbMastersSerializer,ShippingZipcodesSerializer
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

# {"edit_type":"add","method_name":"test","short_name":"","shipping_type":"courier","tracking_type":"awb","method_type":"Manual","zip_code":"700046,700045","zip_routing_codes":"700046@@CCW/AB###700045@@CCW/CD","tracking_url":,"awb_number":"125,4554"}
# {"id":21,"edit_type":"edit",method_name":"test","short_name":"","shipping_type":"courier","tracking_type":"awb","method_type":"Manual","zip_code":"700046,700045","zip_routing_codes":"700046@@CCW/AB###700045@@CCW/CD","tracking_url":"","tracking_id_start":2,"tracking_id_end":3,"awb_prefix":"prefix","awb_suffix":"suffix"}
class CourierAdd(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		postdata = request.data
		method_name=postdata["method_name"]
		short_name=postdata["short_name"] if postdata.get("short_name") else None
		shipping_type=postdata["shipping_type"]
		tracking_type=postdata["tracking_type"]
		website_id=postdata["website_id"]
		method_type="Manual"
		zip_codes=postdata["zip_code"] if postdata.get("zip_code") else None
		zip_routing_codes=postdata["zip_routing_codes"] if postdata.get("zip_routing_codes") else None
		tracking_url=postdata["tracking_url"] if postdata.get("tracking_url") else None
		awb_numbers=postdata["awb_number"] if postdata.get("awb_number") else None
		tracking_id_start=postdata["tracking_id_start"] if postdata.get("tracking_id_start") else None
		tracking_id_end=postdata["tracking_id_end"] if postdata.get("tracking_id_end") else None
		awb_prefix=postdata["awb_prefix"] if postdata.get("awb_prefix") else None
		awb_suffix=postdata["awb_suffix"] if postdata.get("awb_suffix") else None
		if postdata['edit_type']=="add":
			try:
				has_shipping = EngageboostShippingMasters.objects.using(company_db).filter(method_name=method_name).first()
				if has_shipping:
					SaveShippingMasterId=0
					data={"status":0,"api_status":"Method already exists", "message":"Method already exists"}
				else:
					has_record = EngageboostShippingMasters.objects.last()
					if has_record:
					    last_entry_of_table = EngageboostShippingMasters.objects.order_by('-id').latest('id')
					    row_id = int(last_entry_of_table.id)+int(1)
					else:
					    row_id = 1
					if postdata["tracking_type"]=="awb" or postdata["tracking_type"]=="Awb":
						SaveShippingMaster = EngageboostShippingMasters.objects.using(company_db).create(id=row_id,website_id=website_id,method_name=method_name,short_name=short_name,shipping_type=shipping_type,tracking_type=tracking_type,method_type=method_type,tracking_url=tracking_url,created=now_utc,modified=now_utc)
					else:
						SaveShippingMaster = EngageboostShippingMasters.objects.using(company_db).create(id=row_id,website_id=website_id,method_name=method_name,short_name=short_name,shipping_type=shipping_type,tracking_type=tracking_type,method_type=method_type,tracking_url=tracking_url,tracking_id_start=tracking_id_start,tracking_id_end=tracking_id_end,awb_prefix=awb_prefix,awb_suffix=awb_suffix,created=now_utc,modified=now_utc)

					if SaveShippingMaster:
						data={"status":1,"api_status":SaveShippingMaster.id, "message":"Courier created successfully"}
						SaveShippingMasterId=SaveShippingMaster.id
					else:
						data={"status":0,"api_status":"Error occured in courier creation", "message":"Error occured in courier creation"}
						SaveShippingMasterId=0
			except Exception as error:
				SaveShippingMasterId=0
				trace_back = sys.exc_info()[2]
				line = trace_back.tb_lineno
				data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error), "message": str(error)}
		else:
			try:
				has_shipping = EngageboostShippingMasters.objects.using(company_db).filter(method_name=method_name).filter(~Q(id=postdata["id"])).first()
				if has_shipping:
					SaveShippingMasterId=0
					data={"status":0,"api_status":"Method already exists", "message":"Method already exists"}
				else:
					if postdata["tracking_type"]=="awb" or postdata["tracking_type"]=="Awb":
						SaveShippingMaster = EngageboostShippingMasters.objects.using(company_db).filter(id=postdata["id"]).update(method_name=method_name,short_name=short_name,shipping_type=shipping_type,tracking_type=tracking_type,method_type=method_type,tracking_url=tracking_url,modified=now_utc)
					else:
						SaveShippingMaster = EngageboostShippingMasters.objects.using(company_db).filter(id=postdata["id"]).update(method_name=method_name,short_name=short_name,shipping_type=shipping_type,tracking_type=tracking_type,method_type=method_type,tracking_url=tracking_url,tracking_id_start=tracking_id_start,tracking_id_end=tracking_id_end,awb_prefix=awb_prefix,awb_suffix=awb_suffix,modified=now_utc)

					if SaveShippingMaster:
						data={"status":1,"api_status":SaveShippingMaster, "message":"Courier updated successfully"}
						SaveShippingMasterId=postdata["id"]
					else:
						data={"status":0,"api_status":"Error occured in courier creation", "message":"Error occured in courier modification"}
						SaveShippingMasterId=0
			except Exception as error:
				SaveShippingMasterId=0
				trace_back = sys.exc_info()[2]
				line = trace_back.tb_lineno
				data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error), "message": str(error)}


		#******SAVE ZIPCODE AND ROUTING CODE******#
		if SaveShippingMasterId==0:
			return Response(data)
		else:
			if zip_routing_codes:
				EngageboostShippingZipcodes.objects.using(company_db).filter(shipping_method_id=SaveShippingMasterId).delete()
				# EngageboostAwbMasters.objects.using(company_db).filter(shipping_method_id=SaveShippingMasterId).delete()
				try:
					zip_routing_codes=zip_routing_codes.split("###")
					for zip_routing_code in zip_routing_codes:
						zip_routing_code = zip_routing_code.split("@@")
						zip_code=zip_routing_code[0]
						routing_code=zip_routing_code[1]

						has_record = EngageboostShippingZipcodes.objects.last()
						if has_record:
						    last_entry_of_table = EngageboostShippingZipcodes.objects.order_by('-id').latest('id')
						    row_id = int(last_entry_of_table.id)+int(1)
						else:
						    row_id = 1
						EngageboostShippingZipcodes.objects.using(company_db).create(id=row_id,zipcode=zip_code,shipping_method_id=SaveShippingMasterId,routing_code=routing_code)

					if tracking_type=="awb" or tracking_type=="Awb":
						list_of_awb_numbers = []
						if awb_numbers:
							awb_numbers=awb_numbers.split(",")
							for awb_number in awb_numbers:
								list_of_awb_numbers.append(awb_number)
								has_awb_number = EngageboostAwbMasters.objects.using(company_db).filter(shipping_method_id=SaveShippingMasterId,isdeleted='n',awb_number=awb_number).first()

								if has_awb_number:
									EngageboostAwbMasters.objects.using(company_db).filter(id=has_awb_number.id).update(awb_number=awb_number,shipping_method_id=SaveShippingMasterId,tracking_company_name=method_name,modified=now_utc)
								else:
									has_record = EngageboostAwbMasters.objects.last()
									if has_record:
									    last_entry_of_table = EngageboostAwbMasters.objects.order_by('-id').latest('id')
									    row_id = int(last_entry_of_table.id)+int(1)
									else:
									    row_id = 1
									EngageboostAwbMasters.objects.using(company_db).create(id=row_id,awb_number=awb_number,shipping_method_id=SaveShippingMasterId,tracking_company_name=method_name,isused='n',order_id=None,created=now_utc,modified=now_utc)

						if list_of_awb_numbers:
							EngageboostAwbMasters.objects.using(company_db).filter(~Q(awb_number__in=list_of_awb_numbers)).filter(isused='n',shipping_method_id=SaveShippingMasterId).delete()
						else:
							EngageboostAwbMasters.objects.using(company_db).filter(isused='n',shipping_method_id=SaveShippingMasterId).delete()
					else:
						if tracking_id_start and tracking_id_end:
							awb_number_list=getTrackingCodeRange(tracking_id_start,tracking_id_end,awb_prefix,awb_suffix)
							if awb_number_list:
								for awb_number in range(len(awb_number_list)):
									has_awb_number = EngageboostAwbMasters.objects.using(company_db).filter(shipping_method_id=SaveShippingMasterId,isdeleted='n',awb_number=awb_number_list[awb_number]).first()

									if has_awb_number:
										EngageboostAwbMasters.objects.using(company_db).filter(id=has_awb_number.id).update(awb_number=awb_number_list[awb_number],shipping_method_id=SaveShippingMasterId,tracking_company_name=method_name,modified=now_utc)
									else:
										has_record = EngageboostAwbMasters.objects.last()
										if has_record:
										    last_entry_of_table = EngageboostAwbMasters.objects.order_by('-id').latest('id')
										    row_id = int(last_entry_of_table.id)+int(1)
										else:
										    row_id = 1
										EngageboostAwbMasters.objects.using(company_db).create(id=row_id,awb_number=awb_number_list[awb_number],shipping_method_id=SaveShippingMasterId,tracking_company_name=method_name,isused='n',order_id=None,created=now_utc,modified=now_utc)

						if awb_number_list:
							EngageboostAwbMasters.objects.using(company_db).filter(~Q(awb_number__in=awb_number_list)).filter(isused='n',shipping_method_id=SaveShippingMasterId).delete()
						else:
							EngageboostAwbMasters.objects.using(company_db).filter(isused='n',shipping_method_id=SaveShippingMasterId).delete()

					data={"status":1,"api_status":SaveShippingMasterId, "message":"Courier created successfully"}
				except Exception as error:
					trace_back = sys.exc_info()[2]
					line = trace_back.tb_lineno
					data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error), "message": "Error occured during shipping zipcode creation"}
			else:
				data={"status":1,"api_status":SaveShippingMasterId, "message":"Courier created successfully"}

			return Response(data)

def getTrackingCodeRange(tracking_id_start,tracking_id_end,awb_prefix,awb_suffix):
	x = tracking_id_start
	awb_number_list=[]
	while x <= tracking_id_end:
		awb_number = ''
		if awb_prefix:
			awb_number = str(awb_prefix)
		awb_number = str(awb_number)+str(x)
		if awb_suffix:
			awb_number = str(awb_number)+str(awb_suffix)

		awb_number_list.append(awb_number)
		x+=1
	return awb_number_list

class GetCourierInfo(generics.ListAPIView):
	def get(self, request, id, format=None):
		company_db = loginview.db_active_connection(request)
		courier_info_cond = EngageboostShippingMasters.objects.using(company_db).filter(id=id).all()
		if courier_info_cond:
			courier_info = ShippingSerializer(courier_info_cond,many=True)
			if courier_info:
				for courierinfo in courier_info.data:
					if courierinfo["tracking_type"]=="awb" or courierinfo["tracking_type"]=="Awb":
						awb_info_cond = EngageboostAwbMasters.objects.using(company_db).filter(shipping_method_id=id,isblocked='n',isdeleted='n').all().values("id","awb_number","tracking_company_name","shipping_method_id","isused")
						if awb_info_cond:
							awb_info = AwbMastersSerializer(awb_info_cond,many=True)
							courierinfo["awb_numbers"] = awb_info.data
						else:
							courierinfo["awb_numbers"] = []
					else:
						courierinfo["awb_numbers"] = []

					shipping_zip_cond = EngageboostShippingZipcodes.objects.using(company_db).filter(shipping_method_id=id).all()
					if shipping_zip_cond:
						shipping_zip = ShippingZipcodesSerializer(shipping_zip_cond,many=True)
						courierinfo["zipcodes"] = shipping_zip.data
					else:
						courierinfo["zipcodes"] = []
				data ={"status":1, "api_status":courier_info.data, "message":'Courier List'}
			else:
				data ={"status":0, "api_status":courier_info.errors, "message":'No courier found'}
		else:
			data ={"status":0, "api_status":[],"message": 'No courier found'}

		return Response(data)

class ViewAwbDetails(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		pre_data={}
		shipping_method_id = request.data["shipping_method_id"]
		# isused = request.data["isused"]

		#********* Start Grid Headings *********#
		row_dict={}
		row=[]
		module='AwbMasters'
		screen_name='list-in-courier'
		layout_fetch=EngageboostGridLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
		layout_header=layout_fetch.header_name.split("@@")
		layout_field=layout_fetch.field_name.split("@@")
		layout_check=EngageboostGridColumnLayouts.objects.using(company_db).filter(module=module,screen_name=screen_name).count()
		layout={}
		layout_arr=[]

		for header,field in zip(layout_header,layout_field):
		    ex_layout_field=field.split(".")
		    is_numeric_field=field.split("#")
		    field_name=ex_layout_field[0]
		    
		    if len(is_numeric_field)>1:
		        field_type=is_numeric_field[1]
		        field_name=is_numeric_field[0]
		    else:
		        field_type=''   

		    if len(ex_layout_field)>1:
		        child_name=ex_layout_field[1]
		        field_name=ex_layout_field[0]
		    else:
		        child_name=''            

		    if(layout_check):
		        layout_column_fetch=EngageboostGridColumnLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
		        layout_column_header=layout_column_fetch.header_name
		        layout_column_field=layout_column_fetch.field_name

		        if header in layout_column_header:
		            status=1
		        else:
		            status=0
		    else:
		        status=1        
		    layout={"title":header,"field":field_name,"child":child_name,"show":status,"field_type":field_type}
		    layout_arr.append(layout)
		#********* End Grid Headings *********#

		awb_info_cond = EngageboostAwbMasters.objects.using(company_db).filter(shipping_method_id=shipping_method_id, isdeleted='n').all().values("id","awb_number","tracking_company_name","shipping_method_id","isused","order_id")
		if awb_info_cond:
			awb_info_list = []			
			# if request.data.get('search'):
			#     search_cond = request.data.get('search')
			#     if request.data.get('order_by'):
			#         order_by=request.data.get('order_by');order_type=request.data.get('order_type')
			#         order=order_by if order_type=='+' else '-'+order_by
			#         awb_info_cond = awb_info_cond.order_by(order).filter(Q(awb_number__icontains = search_cond) | Q(order_id__icontains = search_cond))
			#     else:
			#         awb_info_cond = awb_info_cond.filter(Q(awb_number__icontains = search_cond) | Q(order_id__icontains = search_cond))
			# else:
			#     if request.data.get('order_by'):
			#         order_by=request.data.get('order_by');order_type=request.data.get('order_type')
			#         order=order_by if order_type=='+' else '-'+order_by
			#         awb_info_cond = awb_info_cond.order_by(order)
			#     else:
			#         awb_info_cond = awb_info_cond

			awb_info = AwbMastersSerializer(awb_info_cond,many=True)
			for awbinfo in awb_info.data:
				if awbinfo["order_id"]:
					order_master = EngageboostOrdermaster.objects.filter(id=awbinfo["order_id"]).first()
					if order_master:
						awbinfo["order_id"] = order_master.custom_order_id
					else:
						awbinfo["order_id"] = ""
				else:
					awbinfo["order_id"]=""

				if request.data.get('search'):
					search_cond = request.data.get('search')
					if search_cond.lower() in awbinfo["order_id"].lower() or search_cond.lower() in awbinfo["awb_number"].lower():
						awb_info_list.append(awbinfo)
				else:
					awb_info_list.append(awbinfo)

			pre_data['all']=len(awb_info_list)
			pre_data['result']=awb_info_list
			pre_data['layout']=layout_arr
		else:
			pre_data['all']=0
			pre_data['result']=[]
			pre_data['layout']=layout_arr

		awb_list_data = self_pagination(pre_data)
		return Response(awb_list_data)

def get_page_size():
    settings = EngageboostGlobalSettings.objects.get(isdeleted='n',isblocked='n',website_id=1)
    size=settings.itemlisting_backend
    return size 

def self_pagination(array_list):
    results_arr=[]
    page_size = get_page_size()
    length_of_list = len(array_list['result'])
    results_arr.append(array_list)
    result = {"count":length_of_list,"per_page_count": math.ceil(length_of_list/page_size),"page_size":page_size,"results":results_arr}
    return result

class AddAwbNumber(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		postdata=request.data
		shipping_method_id=postdata["shipping_method_id"]
		tracking_company_name=postdata["tracking_company_name"]
		awb_numbers=postdata["awb_number"]
		try:
			if awb_numbers:
				awb_numbers=awb_numbers.split(",")
				for awb_number in awb_numbers:
					has_awb_number = EngageboostAwbMasters.objects.using(company_db).filter(shipping_method_id=shipping_method_id,isdeleted='n',awb_number=awb_number).first()

					if has_awb_number:
						EngageboostAwbMasters.objects.using(company_db).filter(id=has_awb_number.id).update(awb_number=awb_number,shipping_method_id=shipping_method_id,modified=now_utc)
					else:
						has_record = EngageboostAwbMasters.objects.last()
						if has_record:
						    last_entry_of_table = EngageboostAwbMasters.objects.order_by('-id').latest('id')
						    row_id = int(last_entry_of_table.id)+int(1)
						else:
						    row_id = 1
						EngageboostAwbMasters.objects.using(company_db).create(id=row_id,awb_number=awb_number,shipping_method_id=shipping_method_id,tracking_company_name=tracking_company_name,isused='n',order_id=None,created=now_utc,modified=now_utc)

			data={"status":1, "message":"AWB created successfully"}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error), "message": "Error occured during AWB number save"}

		return Response(data)