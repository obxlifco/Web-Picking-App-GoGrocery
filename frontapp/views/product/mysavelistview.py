from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.db.models import F, Func, FloatField
from django.db.models.functions import Cast
from webservices.models import *
from frontapp.frontapp_serializers import *
import json
import base64
import sys,os
import traceback
import datetime
from django.db.models import Q
import random
class MySaveList(APIView):
	def get(self, request, format=None):
		user       = request.user
		user_id    = user.id
		try:
			qs_savelist = EngageboostMysavelist.objects.filter(isdeleted='n', user_id=user_id).all().order_by('-id')
			savelist_data =  EngageboostMysavelistSerializer(qs_savelist,many=True).data
			if savelist_data:
				for savelistdata in savelist_data:
					count = savelistdata['product_ids']
					countlent = 0
					if count:
						product_count = count.split(',')
						product_count = list(filter(None, product_count))
						up_data = []
						for i in range(len(product_count)):
							# if product_count[i] !='None':
							# 	up_data.append(product_count[i])
							if product_count[i] !='null':
								up_data.append(product_count[i])

						product_count = list(up_data)
						countlent = len(up_data)
					else:
						countlent =0
					
					savelistid = savelistdata['id']

					savelistidstr = str(savelistid)
					randomnum = '{:03d}'.format(random.randrange(1, 999))
					encoderandom = (randomnum + savelistidstr + randomnum)
					encodedBytes = base64.b64encode(encoderandom.encode("utf-8"))
					encodedStr = str(encodedBytes, "utf-8")
					savelistdata.update({'count':countlent, 'slug':encodedStr})
			if qs_savelist:
				#str_status = status.HTTP_200_OK
				data = {
						'status':1,
						'message': 'Success',
						'data' : savelist_data
					}
			else:
				#str_status = status.HTTP_204_NO_CONTENT
				data = {
					'status':0,
					'message': 'No data found',
					'data': []
				}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data = {"status":0, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
		return Response (data)

	def post(self, request, format=None): 
		requestdata     = request.data
		user            = request.user
		user_id         = user.id
		website_id      = requestdata['website_id']
		name            = requestdata['name']
		product_id      = None
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		if "product_id" in requestdata:
			product_id  = requestdata['product_id']
		name            = name.strip()
		str_status = ""
		try:
			if website_id == '':
				raise Exception("website id is required")
			if name == '':
				raise Exception("name is required")
			rs_savelist = EngageboostMysavelist.objects.filter(savelist_name__iexact=name,user_id=user_id).first()
			if rs_savelist:
				if product_id is not None:
					product_id = str(product_id)
					rs_save_product = EngageboostMysavelist.objects.all().filter(user_id=user_id).filter( Q(product_ids__startswith=product_id+',') | Q(product_ids__endswith=','+product_id) | Q(product_ids__contains=',{0},'.format(product_id)) | Q(product_ids__exact=product_id) )
					if rs_save_product:
						str_status = status.HTTP_200_OK
						data = {
							"status":str_status,
							"msg":"Exist"
						}
					else:
						product_ids = str(rs_savelist.product_ids)+","+str(product_id)
						save_ids_arr = product_ids.split(",")

						# save_ids_arr  = ' '.join(save_ids_arr).split() 
						save_ids_arr = list(filter(None, save_ids_arr))
						save_ids_str = ",".join(save_ids_arr)
						save_arr = {
							"product_ids":save_ids_str
						}
						EngageboostMysavelist.objects.filter(id=rs_savelist.id).update(**save_arr)
						str_status = status.HTTP_200_OK
						data = {
							"status":str_status,
							"msg":"success"
						}
			else:
				# if product_id is None or product_id=="":
				# 	product_id = 0
				str_status = status.HTTP_200_OK
				save_arr = {
					"website_id":website_id,
					"company_id":1,
					"user_id":user_id,
					"savelist_name":name,
					"product_ids":product_id,
					"isdeleted":"n",
					"created":now_utc,
					"modified":now_utc
				}
				EngageboostMysavelist.objects.create(**save_arr)
				data = {
					"status":str_status,
					"msg":"success"
				}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			str_status = status.HTTP_417_EXPECTATION_FAILED
			data = {"status":str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
		return Response(data, str_status)

class AddRemoveFromSavelist(APIView):
	def put(self, request, format=None):
		requestdata     = request.data
		user            = request.user
		user_id         = user.id
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		website_id      = requestdata['website_id']
		action = ""
		if "action" in requestdata:
			action      = requestdata['action']
		product_id      = ""
		if "product_id" in requestdata:
			product_id = str(requestdata['product_id'])
		list_id = 0
		if "list_id" in requestdata:
			list_id = int(requestdata['list_id'])
		try:
			if website_id == '':
				raise Exception("website id is required")
			if product_id == "":
				raise Exception("Product Id is required")
			if list_id == "":
				raise Exception("List Id is required")
			rs_save_product = EngageboostMysavelist.objects.all().filter(id=list_id, user_id=user_id).filter( Q(product_ids__startswith=product_id+',') | Q(product_ids__endswith=','+product_id) | Q(product_ids__contains=',{0},'.format(product_id)) | Q(product_ids__exact=product_id) )
			if rs_save_product:
				if action and action == 'del':
					rs_savelist = EngageboostMysavelist.objects.filter(id=list_id, user_id=user_id).first()
					product_ids = rs_savelist.product_ids
					save_ids_arr = product_ids.split(",")
					save_ids_arr = list(filter(None, save_ids_arr))
					save_str = ""
					new_arr = []
					for x in range(len(save_ids_arr)):
						if int(save_ids_arr[x]) == int(product_id):
							pass
						else:
							new_arr.append(save_ids_arr[x])
					save_str = ",".join(new_arr)
					save_arr = {
						"product_ids":save_str
					}
					EngageboostMysavelist.objects.filter(id=rs_savelist.id).update(**save_arr)
					str_status = status.HTTP_200_OK
					data = {
						"status":str_status,
						"msg":"success"
					}
				else:
					str_status = status.HTTP_200_OK
					data = {
						"status":str_status,
						"msg":"Exist"
					}
			else:
				str_status = status.HTTP_200_OK
				if action and action == 'del':
					data = {
						"status":str_status,
						"msg":"success"
					}
				else:
					rs_savelist = EngageboostMysavelist.objects.filter(id=list_id, user_id=user_id).first()
					if rs_savelist is not None:
						product_ids = str(rs_savelist.product_ids)+","+str(product_id)
					else:
						product_ids = str(product_id)

					save_ids_arr = product_ids.split(",")
					# save_ids_arr  = ' '.join(save_ids_arr).split() 
					save_ids_arr = list(save_ids_arr)
					save_ids_arr = list(filter(None, save_ids_arr))
					up_data = []
					for i in range(len(save_ids_arr)):
						if save_ids_arr[i] !='None':
							up_data.append(save_ids_arr[i])

					save_ids_str = ",".join(up_data)					

					save_arr = {
						"product_ids":save_ids_str
					}

					EngageboostMysavelist.objects.filter(id=rs_savelist.id).update(**save_arr)
					str_status = status.HTTP_200_OK
					data = {
						"status":str_status,
						"msg":"success"
					}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			str_status = status.HTTP_417_EXPECTATION_FAILED
			data = {"status":str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
		return Response(data)

class ViewSavelistDetails(generics.ListAPIView):
	def get(self, request, savelist_id, format=None):
		user                = request.user
		user_id             = user.id
		warehouse_id      = request.META.get('HTTP_WAREHOUSE')
		str_status = ""
		decode = base64.b64decode(savelist_id)
		d2 = decode.decode("UTF-8")
		fstrip = d2[3:]
		lstrip = fstrip[:-3]

		try:
			rs_savelist = EngageboostMysavelist.objects.filter(user_id=user_id,id=lstrip,isdeleted='n').first()
			if rs_savelist:
				productid=rs_savelist.product_ids
				savelist_name = rs_savelist.savelist_name
				savelistid = rs_savelist.id
				if productid:
					productidlist = []
					for pid in productid.split(','):
						productidlist.append(int(pid))

					product_qs = EngageboostProducts.objects.filter(isblocked='n',isdeleted='n',id__in=productidlist).all()
					# print(product_qs.query)
					product_data = SavelistDetailsSerializer(product_qs,context={'warehouse_id': warehouse_id},many=True).data
					if product_data:
						for data in product_data:

							if "id" in data['product']:
								data['product']['id']= data["id"]
							else:
								data["product"]['id'] =  data["id"]

							if float(data['channel_price'])>0:
								data['product']['product_price'] = data['channel_price']
							else:
								data['product']['product_price'] = 0
					
					if product_data:
						for productdata in product_data:
							productdata.update({'savelist_name':savelist_name,'savelist_id':savelistid})
						str_status = status.HTTP_200_OK
						data = {
						'status':str_status,
						'message': 'success',
						'data' : product_data
						}
					else:
						str_status = status.HTTP_204_NO_CONTENT
						data = {
						'status':str_status,
						'message': 'No data found',
						'data': []
						}
				else:
						str_status = status.HTTP_204_NO_CONTENT
						data = {
						'status':str_status,
						'message': 'No data found',
						'data': []
						}

			else:
				str_status = status.HTTP_401_UNAUTHORIZED
				data = {
				"status":str_status,
				"api_status": "You are not authorise to view this savelist.",
				"data":[]
				}
		except Exception as error:
			str_status = status.HTTP_417_EXPECTATION_FAILED
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in order update."}

		return Response(data,str_status)

class SavelistAddEditDelete(APIView):
	def post(self, request, format=None):
		requestdata     = request.data
		user       		= request.user
		user_id    		= user.id
		name       		= requestdata['name']
		website_id      = requestdata['website_id']
		name            = name.strip()
		
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		try:
			if name =='':
				raise Exception("name is required")
			if website_id =='':
				raise Exception("website id is required")	

			savelistcount=EngageboostMysavelist.objects.filter(isdeleted='n',user_id=user_id,savelist_name=name).count()
			if savelistcount>0:
				raise Exception("list already exist")
			else:
				qs_savelist=EngageboostMysavelist.objects.create(
					website_id = website_id,
					savelist_name = name, 
					user_id = user_id,
					company_id=1,
					created = now_utc,
					modified = now_utc
				)
				qs_savelist.save()
				savelist_data = EngageboostMysavelistSerializer(qs_savelist).data
				if savelist_data:
					str_status = status.HTTP_200_OK
					data = {
					'status':str_status,
					'message': 'Success',
					'data' : savelist_data
					}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			str_status = status.HTTP_417_EXPECTATION_FAILED
			data = {"status":str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
		return Response (data,str_status)

	def put(self, request, format=None):
		requestdata     = request.data
		user       		= request.user
		user_id    		= user.id
		name       		= requestdata['name']
		savelist_id     = requestdata['savelist_id']
		name            = name.strip()

		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		
		try:
			if name =='':
				raise Exception("name is required")
			if savelist_id =='':
				raise Exception("name is savelist id is required")
			qs_savelist = EngageboostMysavelist.objects.filter(id=savelist_id,user_id=user_id).first()
			if qs_savelist:
				savelistcount=EngageboostMysavelist.objects.filter(isdeleted='n',user_id=user_id,savelist_name=name).count()
				if savelistcount>0:
					raise Exception("list already exist")
				else:
					qs_savelist=EngageboostMysavelist.objects.filter(user_id=user_id,isdeleted='n',id=savelist_id).update(savelist_name = name, modified = now_utc)
					
					str_status = status.HTTP_200_OK
					data = {
					'status':str_status,
					'message': 'Success',
					}
			else:
				str_status = status.HTTP_401_UNAUTHORIZED
				data = {
				'status':str_status,
				'message': 'You are not authorise to edit this list.',
				}

		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			str_status = status.HTTP_417_EXPECTATION_FAILED
			data = {"status":str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
		return Response (data,str_status)

	def delete(self, request, pk, format=None):
		user                   =  request.user
		user_id                =  user.id
		str_status = ""
		rs_address = EngageboostMysavelist.objects.filter(id=pk,user_id=user_id).first()
		if rs_address:
			EngageboostMysavelist.objects.filter(id=pk,user_id=user_id).delete()
			qs_savelist = EngageboostMysavelist.objects.filter(isdeleted='n', user_id=user_id).all().order_by('-id')
			savelist_data =  EngageboostMysavelistSerializer(qs_savelist,many=True).data
			if savelist_data:
				for savelistdata in savelist_data:
					count = savelistdata['product_ids']
					if count:
						product_count = count.split(',')
						countlent = len(product_count)
					else:
						countlent =0
					savelistdata.update({'count':countlent})
			str_status = status.HTTP_200_OK
			data = {
			'status':str_status,
			'message': 'Success.',
			'data':savelist_data
			}
		else:
			str_status = status.HTTP_401_UNAUTHORIZED
			data = {
			'status':str_status,
			'message': 'You are not authorise to delete this list.',
			}
		return Response(data,str_status)