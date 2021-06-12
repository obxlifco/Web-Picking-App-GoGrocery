from webservices.models import *
from django.http import Http404
from django.db.models import Q
from webservices.serializers import *
from rest_framework.views import APIView
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
import datetime
from rest_framework import generics
from rest_framework.response import Response
import random
from django.http import HttpResponse
from django.http import HttpResponse
import json
import requests
import random
from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import MultiPartParser, FormParser
import os
import socket
from django.conf import settings
from django.db.models import Q
from webservices.views import loginview
import tinys3
import urllib
import base64
import pytz
import xlsxwriter
class HsncodeSetup(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		datas=[]
		import xlrd
		import os
		import time
		post_data = request.data
		d2 = request.data
		website_id = post_data['website_id']
		d1={"website_id":website_id}
		serializer_data=dict(d2,**d1)
		if 'import_file' in request.FILES:
			rand = str(random.randint(1111,9999))
			file1 = request.FILES['import_file']
			file_name=file1.name
			# print(file_name)			
			ext = file_name.split('.')[-1]
			new_file_name='HsnCode_'+rand
			fs=FileSystemStorage()
			filename = fs.save('importfile/hsncode/'+new_file_name+'.'+ext, file1)
			uploaded_file_url = fs.url(filename)
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			csvReader = xlrd.open_workbook(settings.BASE_DIR+uploaded_file_url)
			sheet = csvReader.sheet_by_index(0)
			length=len(sheet.col_values(0))
			arr_message=[]
			for x in range(length):
				if(sheet.col_values(0)[x]=='HSN'):
					pass
				else:
					hsn_id=0
					if type(sheet.col_values(0)[x]) == float:
						hsn_code=int(round(sheet.col_values(0)[x]))
					else:
						hsn_code=sheet.col_values(0)[x]
					sgst=sheet.col_values(1)[x]
					cgst=sheet.col_values(2)[x]
					igst=sheet.col_values(3)[x]
					cess=sheet.col_values(4)[x]
					has_record = EngageboostHsnCodeMaster.objects.last()
					if has_record:
						last_entry_of_table = EngageboostHsnCodeMaster.objects.order_by('-id').latest('id')
						row_id = int(last_entry_of_table.id)+int(1)
					else:
						row_id = 1
					# d1={"id":row_id,"hsn_code":hsn_code,"sgst":sgst,"cgst":cgst,"igst":igst,"cess":cess,"created":datetime.datetime.now(),"modified":datetime.datetime.now()};serializer_data=dict(d2,**d1)
					# serializer_data.pop("import_file")
					current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
					# current_time = pytz.timezone('Asia/Kolkata').localize(datetime.datetime.now())
					# current_time = str(current_time).split('+')
					# plus_time = current_time[1].replace(':','.')
					# current_time = datetime.datetime.strptime(current_time[0], "%Y-%m-%d %H:%M:%S.%f")
					# current_time = current_time+ datetime.timedelta(hours=float(plus_time))

					hsncodelist = EngageboostHsnCodeMaster.objects.using(company_db).create(id=row_id,hsn_code=hsn_code,sgst=sgst,cgst=cgst,igst=igst,cess=cess,created=current_time,modified=current_time)
					if hsncodelist:
						last_hsncodelist_id = hsncodelist.id
						datas.append(last_hsncodelist_id)
					else:
						datas.append('failed')

			data = {"status":1,"api_response":datas,"message":"Success"}
			return Response(data)
		else:
			try:
				if post_data['id']: hsn_id = post_data['id'] # this is primary key(id) of the table/ only require when update
				else: hsn_id = "0"
			except KeyError: hsn_id = "0"
			d1={"hsn_id":hsn_id};serializer_data=dict(d2,**d1)

			try:
				if post_data['hsn_code']: hsn_code = post_data['hsn_code']
				else: hsn_code = ""
			except KeyError: hsn_code = ""
			d1={"hsn_code":hsn_code};serializer_data=dict(d2,**d1)

			try:
				if post_data['sgst']: sgst = post_data['sgst']
				else: sgst = 0
			except KeyError: sgst = 0
			d1={"sgst":sgst};serializer_data=dict(d2,**d1)

			try:
				if post_data['cgst']: cgst = post_data['cgst']
				else: cgst = 0
			except KeyError: cgst = 0
			d1={"cgst":cgst};serializer_data=dict(d2,**d1)

			try:
				if post_data['igst']: igst = post_data['igst']
				else: igst = 0
			except KeyError: igst = 0
			d1={"igst":igst};serializer_data=dict(d2,**d1)

			try:
				if post_data['cess']: cess = post_data['cess']
				else: cess = 0
			except KeyError: cess = 0
			d1={"cess":cess};serializer_data=dict(d2,**d1)


			if hsn_id == 0 or hsn_id == "0":
				hsncodeIsexists = EngageboostHsnCodeMaster.objects.using(company_db).filter(hsn_code=hsn_code).first()
				if hsncodeIsexists:
					data ={
						'status':0,
						'api_status':'HSN Code already exists',
						'message':'HSN Code already exists',
						}
				else:
					has_record = EngageboostHsnCodeMaster.objects.last()
					if has_record:
						last_entry_of_table = EngageboostHsnCodeMaster.objects.order_by('-id').latest('id')
						row_id = int(last_entry_of_table.id)+int(1)
					else:
						row_id = 1

					current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
					d1={"id":row_id,"created":current_time,"modified":current_time};serializer_data=dict(d2,**d1)
					
					# serializer_data.pop("hsn_id")

					hsncode = EngageboostHsnCodeMaster.objects.using(company_db).create(**serializer_data)
					last_inserted_id = hsncode.id

					if hsncode:
						data ={
						'status':1,
						'api_status':last_inserted_id,
						'message':'Data Saved Successfully',
						}
					else:
						data ={
						'status':0,
						'api_status':serializer.errors,
						'message':'Error Occured',
						}
				return Response(data)
			else:
				serializer_data.pop('id')
				
				current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
				d1={"modified":current_time};serializer_data=dict(d2,**d1)

				hsncodeIsexists = EngageboostHsnCodeMaster.objects.using(company_db).filter(hsn_code=hsn_code,isdeleted='n', isblocked='n').first()
				if hsncodeIsexists:
					if hsncodeIsexists.id == hsn_id:
						hsncode = EngageboostHsnCodeMaster.objects.using(company_db).get(id=hsn_id)
						serializer = HsnCodeMasterSerializer(hsncode, data=serializer_data,partial=True)
						if serializer.is_valid():
							serializer.save()
							data ={
							'status':1,
							'api_status':'Data Updated Successfully',
							'message':'Data Updated Successfully',
							}
							return Response(data)
						else:
							data ={
							'status':0,
							'api_status':serializer.errors,
							'message':'Error Occured',
							}
							return Response(data)
					else:
						data ={
						'status':0,
						'api_status':'HSN Code already exists',
						'message':'HSN Code already exists',
						}
						return Response(data)
				else:
					hsncode = EngageboostHsnCodeMaster.objects.using(company_db).get(id=hsn_id)
					serializer = HsnCodeMasterSerializer(hsncode, data=serializer_data,partial=True)
					if serializer.is_valid():
						serializer.save()
						data ={
						'status':1,
						'api_status':'Data Updated Successfully',
						'message':'Data Updated Successfully',
						}
						return Response(data)
					else:
						data ={
						'status':0,
						'api_status':serializer.errors,
						'message':'Error Occured',
						}
						return Response(data)

	def get(self, request, id, format=None):
		company_db = loginview.db_active_connection(request)
		HsnCodeListCond = EngageboostHsnCodeMaster.objects.using(company_db).filter(id=id).first()
		if HsnCodeListCond:
			HsnCodeLists = HsnCodeMasterSerializer(HsnCodeListCond, partial=True)
			data={"status":1,"api_status":HsnCodeLists.data,"message":"Data Found"}
		else:
			data={"status":0,"api_status":"No Data Found","message":"No Data Found"}
		
		return Response(data)


class HsnCodeList(generics.ListAPIView):
	def get(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		HsnCodeListCond = EngageboostHsnCodeMaster.objects.using(company_db).filter(isdeleted='n', isblocked='n').all()
		if HsnCodeListCond:
			HsnCodeLists = HsnCodeMasterSerializer(HsnCodeListCond, many=True)
			data={"status":1,"api_status":HsnCodeLists.data,"message":"Data Found"}
		else:
			data={"status":0,"api_status":"No Data Found","message":"No Data Found"}
		
		return Response(data)

class HsncodeExport(generics.ListAPIView):
	def get(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT+'/exportfile/hsncode_export.xls')
		worksheet = workbook.add_worksheet()
		HsnCodeListCond = EngageboostHsnCodeMaster.objects.using(company_db).all().filter(isdeleted='n').order_by('-id')
		HsnCodeLists = HsnCodeMasterSerializer(HsnCodeListCond, many=True)
		bold = workbook.add_format({'bold': True})
		row = 1
		worksheet.write(0,0,'HSN CODE',bold)
		worksheet.write(0,1,'SGST',bold)
		worksheet.write(0,2,'CGST',bold)
		worksheet.write(0,3,'IGST',bold)
		worksheet.write(0,4,'CESS',bold)
		for HsnCodeList in HsnCodeLists.data:
			# worksheet.write(0,i,item['title'],0)
			worksheet.write(row,0,HsnCodeList['hsn_code'],0)
			worksheet.write(row,1,HsnCodeList['sgst'],0)
			worksheet.write(row,2,HsnCodeList['cgst'],0)
			worksheet.write(row,3,HsnCodeList['igst'],0)
			worksheet.write(row,4,HsnCodeList['cess'],0)
			row = row+1
		workbook.close()
		data ={'status':1}
		return Response(data)
