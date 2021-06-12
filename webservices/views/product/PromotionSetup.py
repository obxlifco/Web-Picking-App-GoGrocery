from webservices.models import *
from django.http import Http404
from django.db.models import Q
from webservices.serializers import *
from rest_framework.views import APIView
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.db.models import Q
from webservices.views import loginview
import os
import socket
import json
import requests
import datetime
import random
import tinys3
import urllib
import base64
import pytz
import xlsxwriter
import xlrd
import time
import string

class ProductPromotionImport(generics.ListAPIView):
	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)

		post_data = request.data
		website_id = post_data['website_id']
		# company_id = post_data['company_id']

		if 'import_file' in request.FILES:
			keylist = [random.choice(string.ascii_letters + string.digits) for n in range(32)]
			rand = "".join(keylist)
			# rand = str(random.randint(1111,9999))
			file1 = request.FILES['import_file']
			file_name=file1.name

			if file_name:
				ext = file_name.split('.')[-1]
				new_file_name='ProductPromotionImportFile_'+rand
				fs=FileSystemStorage()
				filename = fs.save('importfile/promotion_import_file/'+new_file_name+'.'+ext, file1)
				
				uploaded_file_url = fs.url(filename)
				BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
				csvReader = xlrd.open_workbook(settings.BASE_DIR+uploaded_file_url)
				sheet = csvReader.sheet_by_index(0)
				length=len(sheet.col_values(0))
				datas=[]
				product_eq_ids='';product_neq_ids=''
				product_eq_names='';product_neq_names=''
				category_eq_ids='';category_neq_ids=''
				category_eq_names='';category_neq_names=''
				amount_eq_value='';amount_gt_value='';amount_lt_value=''
				customer_eq_ids='';customer_neq_ids=''
				customer_eq_names='';customer_neq_names=''
				for x in range(length):
					if(sheet.col_values(0)[x]=='Discount Name'):
						pass
					else:
						name=sheet.col_values(0)[x]
						desc=sheet.col_values(1)[x]
						amount=sheet.col_values(3)[x]
						disc_type=sheet.col_values(2)[x]
						if disc_type == "P":
							disc_type=1
						else:
							disc_type=2
						disc_start_date=sheet.col_values(4)[x]
						disc_start_date = covert_time_to_utc(disc_start_date,"Asia/Kolkata","UTC")
						disc_end_date=sheet.col_values(5)[x]
						disc_end_date =covert_time_to_utc(disc_end_date,"Asia/Kolkata","UTC")
						customer_group=sheet.col_values(6)[x]
						if customer_group == "Registerd":
							customer_group="1"
						elif customer_group == "Guest":
							customer_group="2"
						else:
							customer_group="1,2"

						status=sheet.col_values(7)[x]
						if status == "Active":
							status='y'
						else:
							status='n'

						discount_type='p'
						isdeleted='n'
						discount_master_type=0

						sku_equal_to = sheet.col_values(8)[x]
						sku_not_equal_to = sheet.col_values(9)[x]

						category_equal_to = sheet.col_values(10)[x]
						category_not_equal_to = sheet.col_values(11)[x]

						amount_equal_to = sheet.col_values(12)[x]
						amount_greater_than = sheet.col_values(13)[x]
						amount_less_than = sheet.col_values(14)[x]

						customer_equal_to = sheet.col_values(15)[x]
						customer_not_equal_to = sheet.col_values(16)[x]

						if sku_equal_to:
							is_sku_eq = 1
							sku_equal_to_list = sku_equal_to.split(',')
							sku_eq_index=0
							for sku_eq in sku_equal_to_list:
								sku_eq_index +=1
								ProductDetails = EngageboostProducts.objects.using(company_db).filter(sku=sku_eq).first()
								if ProductDetails:
									if product_eq_ids == '':
										product_eq_ids = str(ProductDetails.id)
										product_eq_names = ProductDetails.sku
									else: 
										product_eq_ids = product_eq_ids+','+str(ProductDetails.id)
										product_eq_names = product_eq_names+','+ProductDetails.sku
								else:
									product_eq_ids = product_eq_ids
									product_eq_names = product_eq_names
						else:
							is_sku_eq = 0

						if sku_not_equal_to:
							is_sku_neq = 1
							sku_not_equal_to_list = sku_not_equal_to.split(',')
							for sku_neq in sku_not_equal_to_list:
								ProductDetails = EngageboostProducts.objects.using(company_db).filter(sku=sku_neq).first()
								if ProductDetails:
									if product_neq_ids == '':
										product_neq_ids = str(ProductDetails.id)
										product_neq_names = ProductDetails.sku
									else: 
										product_neq_ids = product_neq_ids+','+str(ProductDetails.id)
										product_neq_names = product_neq_names+','+ProductDetails.sku
								else:
									product_neq_ids = product_neq_ids
									product_neq_names = product_neq_names
						else:
							is_sku_neq = 0

						if category_equal_to:
							is_cat_eq = 1
							category_equal_to_list = category_equal_to.split(',')
							for cat_eq in category_equal_to_list:
								CategoryDetails = EngageboostCategoryMasters.objects.using(company_db).filter(name__iexact=cat_eq,isdeleted='n',isblocked='n').first()
								if CategoryDetails:
									if category_eq_ids == '':
										category_eq_ids = str(CategoryDetails.id)
										category_eq_names = CategoryDetails.name
									else: 
										category_eq_ids = category_eq_ids+','+str(CategoryDetails.id)
										category_eq_names = category_eq_names+','+CategoryDetails.name
								else:
									category_eq_ids = category_eq_ids
									category_eq_names = category_eq_names
						else:
							is_cat_eq = 0

						if category_not_equal_to:
							is_cat_neq = 1
							category_not_equal_to_list = category_not_equal_to.split(',')
							for cat_neq in category_not_equal_to_list:
								CategoryDetails = EngageboostCategoryMasters.objects.using(company_db).filter(name__iexact=cat_neq,isdeleted='n',isblocked='n').first()
								if CategoryDetails:
									if category_neq_ids == '':
										category_neq_ids = str(CategoryDetails.id)
										category_neq_names = CategoryDetails.name
									else: 
										category_neq_ids = category_neq_ids+','+str(CategoryDetails.id)
										category_neq_names = category_neq_names+','+CategoryDetails.name
								else:
									category_neq_ids = category_neq_ids
									category_neq_names = category_neq_names
						else:
							is_cat_neq = 0

						if amount_equal_to:
							is_amount_eq = 1
							amount_eq_value = amount_equal_to
						else:
							is_amount_eq = 0

						if amount_greater_than:
							is_amount_gt = 1
							amount_gt_value = amount_greater_than
						else:
							is_amount_gt = 0

						if amount_less_than:
							is_amount_lt = 1
							amount_lt_value = amount_less_than
						else:
							is_amount_lt = 0
						
						if customer_equal_to:
							is_customer_eq = 1
							customer_equal_to_list = customer_equal_to.split(',')
							for cust_eq in customer_equal_to_list:
								CustomerDetails = EngageboostCustomers.objects.using(company_db).filter(email=cust_eq,isblocked='n',isdeleted='n').first()
								if CustomerDetails:
									if customer_eq_ids == '':
										customer_eq_ids = str(CustomerDetails.id)
										customer_eq_names = CustomerDetails.email
									else: 
										customer_eq_ids = customer_eq_ids+','+str(CustomerDetails.id)
										customer_eq_names = customer_eq_names+','+CustomerDetails.email
								else:
									customer_eq_ids = customer_eq_ids
									customer_eq_names = customer_eq_names
						else:
							is_customer_eq = 0

						if customer_not_equal_to:
							is_customer_neq = 1
							customer_not_equal_to_list = customer_not_equal_to.split(',')
							for cust_neq in customer_not_equal_to_list:
								CustomerDetails = EngageboostCustomers.objects.using(company_db).filter(email=cust_neq,isblocked='n',isdeleted='n').first()
								if CustomerDetails:
									if customer_neq_ids == '':
										customer_neq_ids = str(CustomerDetails.id)
										customer_neq_names = CustomerDetails.email
									else: 
										customer_neq_ids = customer_neq_ids+','+str(CustomerDetails.id)
										customer_neq_names = customer_neq_names+','+CustomerDetails.email
								else:
									customer_neq_ids = customer_neq_ids
									customer_neq_names = customer_neq_names
						else:
							is_customer_neq = 0

						# datas.append(product_names)
							
						# has_record = EngageboostDiscountMasters.objects.using(company_db).last()
						# if has_record:
						# 	last_entry_of_table = EngageboostDiscountMasters.objects.order_by('-id').latest('id')
						# 	row_id = int(last_entry_of_table.id)+int(1)
						# else:
						# 	row_id = 1

						
						# discount_master = EngageboostDiscountMasters.objects.using(company_db).create(website_id=website_id,name=name,description=desc,amount=amount,disc_type=disc_type,disc_start_date=disc_start_date,disc_end_date=disc_end_date,customer_group=customer_group,discount_type=discount_type,isdeleted=isdeleted,discount_master_type=discount_master_type,coupon_type=0,used_coupon=0)	

						# if discount_master:
						# 	last_inserted_id = discount_master.id
						# 	datas.append(last_inserted_id)
						# else:
						# 	datas.append(0)

						# **************** Insert in discount master table ***************
						serializer_data = dict()
						current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
						d1={"website_id":website_id,"name":name,"description":desc,"amount":amount,"disc_type":disc_type,"disc_start_date":disc_start_date,"disc_end_date":disc_end_date,"customer_group":customer_group,"discount_type":discount_type,"isblocked":status,"isdeleted":isdeleted,"discount_master_type":discount_master_type,"coupon_type":0,"used_coupon":0,"created":current_time,"modified":current_time}
						serializer_data=dict(serializer_data,**d1)	
						serializer = DiscountMasterSerializer(data=serializer_data,partial=True)

						if serializer.is_valid():
							serializer.save()
							last_inserted_id = serializer.data['id']
							datas.append(last_inserted_id)

							# **** IF SKU EQUALS TO ****
							if is_sku_eq==1:
								has_record = EngageboostDiscountMastersConditions.objects.using(company_db).last()
								if has_record:
									last_entry_of_table = EngageboostDiscountMastersConditions.objects.order_by('-id').latest('id')
									row_id = int(last_entry_of_table.id)+int(1)
								else:
									row_id = 1

								disc_master_cond_sku_eq = EngageboostDiscountMastersConditions.objects.using(company_db).create(id=row_id,discount_master_id=last_inserted_id,fields=13633,condition="==",value=product_eq_names,all_product_id=product_eq_ids,condition_type="AND")
								if disc_master_cond_sku_eq:
									last_inserted_cond_id = disc_master_cond_sku_eq.id

							# **** IF SKU NOT EQUALS TO ****
							if is_sku_neq==1:
								has_record = EngageboostDiscountMastersConditions.objects.using(company_db).last()
								if has_record:
									last_entry_of_table = EngageboostDiscountMastersConditions.objects.order_by('-id').latest('id')
									row_id = int(last_entry_of_table.id)+int(1)
								else:
									row_id = 1

								disc_master_cond_sku_neq = EngageboostDiscountMastersConditions.objects.using(company_db).create(id=row_id,discount_master_id=last_inserted_id,fields=13633,condition="!=",value=product_neq_names,all_product_id=product_neq_ids,condition_type="AND")
								if disc_master_cond_sku_neq:
									last_inserted_cond_id = disc_master_cond_sku_neq.id

							# **** IF CATEGORY EQUALS TO ****
							if is_cat_eq==1:
								has_record = EngageboostDiscountMastersConditions.objects.using(company_db).last()
								if has_record:
									last_entry_of_table = EngageboostDiscountMastersConditions.objects.order_by('-id').latest('id')
									row_id = int(last_entry_of_table.id)+int(1)
								else:
									row_id = 1

								disc_master_cond_cat_eq = EngageboostDiscountMastersConditions.objects.using(company_db).create(id=row_id,discount_master_id=last_inserted_id,fields=0,condition="==",value=category_eq_names,all_category_id=category_eq_ids,condition_type="AND")
								if disc_master_cond_cat_eq:
									last_inserted_cond_id = disc_master_cond_cat_eq.id

							# **** IF CATEGORY NOT EQUALS TO ****
							if is_cat_neq==1:
								has_record = EngageboostDiscountMastersConditions.objects.using(company_db).last()
								if has_record:
									last_entry_of_table = EngageboostDiscountMastersConditions.objects.order_by('-id').latest('id')
									row_id = int(last_entry_of_table.id)+int(1)
								else:
									row_id = 1

								disc_master_cond_cat_neq = EngageboostDiscountMastersConditions.objects.using(company_db).create(id=row_id,discount_master_id=last_inserted_id,fields=0,condition="!=",value=category_neq_names,all_category_id=category_neq_ids,condition_type="AND")
								if disc_master_cond_cat_neq:
									last_inserted_cond_id = disc_master_cond_cat_neq.id

							# **** IF AMOUNT EQUALS TO ****
							if is_amount_eq==1:
								has_record = EngageboostDiscountMastersConditions.objects.using(company_db).last()
								if has_record:
									last_entry_of_table = EngageboostDiscountMastersConditions.objects.order_by('-id').latest('id')
									row_id = int(last_entry_of_table.id)+int(1)
								else:
									row_id = 1

								disc_master_cond_amount_eq = EngageboostDiscountMastersConditions.objects.using(company_db).create(id=row_id,discount_master_id=last_inserted_id,fields=-1,condition="==",value=amount_eq_value,condition_type="AND")
								if disc_master_cond_amount_eq:
									last_inserted_cond_id = disc_master_cond_amount_eq.id

							# **** IF AMOUNT GREATER THAN ****
							if is_amount_gt==1:
								has_record = EngageboostDiscountMastersConditions.objects.using(company_db).last()
								if has_record:
									last_entry_of_table = EngageboostDiscountMastersConditions.objects.order_by('-id').latest('id')
									row_id = int(last_entry_of_table.id)+int(1)
								else:
									row_id = 1

								disc_master_cond_amount_gt = EngageboostDiscountMastersConditions.objects.using(company_db).create(id=row_id,discount_master_id=last_inserted_id,fields=-1,condition=">=",value=amount_gt_value,condition_type="AND")
								if disc_master_cond_amount_gt:
									last_inserted_cond_id = disc_master_cond_amount_gt.id

							# **** IF AMOUNT LESS THAN ****
							if is_amount_lt==1:
								has_record = EngageboostDiscountMastersConditions.objects.using(company_db).last()
								if has_record:
									last_entry_of_table = EngageboostDiscountMastersConditions.objects.order_by('-id').latest('id')
									row_id = int(last_entry_of_table.id)+int(1)
								else:
									row_id = 1

								disc_master_cond_amount_lt = EngageboostDiscountMastersConditions.objects.using(company_db).create(id=row_id,discount_master_id=last_inserted_id,fields=-1,condition="<=",value=amount_lt_value,condition_type="AND")
								if disc_master_cond_amount_lt:
									last_inserted_cond_id = disc_master_cond_amount_lt.id

							# **** IF CATEGORY EQUALS TO ****
							if is_customer_eq==1:
								has_record = EngageboostDiscountMastersConditions.objects.using(company_db).last()
								if has_record:
									last_entry_of_table = EngageboostDiscountMastersConditions.objects.order_by('-id').latest('id')
									row_id = int(last_entry_of_table.id)+int(1)
								else:
									row_id = 1

								disc_master_cond_cust_eq = EngageboostDiscountMastersConditions.objects.using(company_db).create(id=row_id,discount_master_id=last_inserted_id,fields=-2,condition="==",value=customer_eq_names,all_customer_id=customer_eq_ids,condition_type="AND")
								if disc_master_cond_cust_eq:
									last_inserted_cond_id = disc_master_cond_cust_eq.id

							# **** IF CATEGORY NOT EQUALS TO ****
							if is_customer_neq==1:
								has_record = EngageboostDiscountMastersConditions.objects.using(company_db).last()
								if has_record:
									last_entry_of_table = EngageboostDiscountMastersConditions.objects.order_by('-id').latest('id')
									row_id = int(last_entry_of_table.id)+int(1)
								else:
									row_id = 1

								disc_master_cond_cust_neq = EngageboostDiscountMastersConditions.objects.using(company_db).create(id=row_id,discount_master_id=last_inserted_id,fields=-2,condition="!=",value=customer_neq_names,all_customer_id=customer_neq_ids,condition_type="AND")
								if disc_master_cond_cust_neq:
									last_inserted_cond_id = disc_master_cond_cust_neq.id
								
						else:
							error_response = serializer.errors
							datas.append(error_response)

				data ={
				'status':1,
				'api_status':datas,
				'message':'Successfully Inserted',
				}
			else:
				data ={
				'status':0,
				'api_status':'Error in uploaded file',
				'message':'Error in uploaded file',
				}
		else:
			data ={
			'status':0,
			'api_status':'No file has been uploaded',
			'message':'No file has been uploaded',
			}

		return Response(data)


def covert_time_to_utc(date,from_zone,target_zone):
	tz1 = pytz.timezone(from_zone)
	tz2 = pytz.timezone(target_zone)

	dt = datetime.datetime.strptime(str(date)+" 00:00:00.0","%Y-%m-%d %H:%M:%S.%f")
	dt = tz1.localize(dt)
	dt = dt.astimezone(tz2)
	dt = dt.strftime("%Y-%m-%d %H:%M:%S")
	return dt