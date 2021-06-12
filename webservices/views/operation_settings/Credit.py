from webservices.models import *
from django.http import Http404
from django.apps import apps
from webservices.serializers import  EngageboostCreditPointSerializer
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
from django.db.models import Q
from webservices.views import loginview
import datetime



class ShopOnGoCreditManager(generics.ListAPIView):

	def post(self, request):
		table_name = 'EngageboostCreditPoint'
		model=apps.get_model('webservices',table_name)
		company_db = loginview.db_active_connection(request)
		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
		postdata=request.data

		serializer_data = {}

		name = postdata['name'] if postdata.get("name") else None
		points = postdata['points'] if postdata.get("points") else None
		loyal_start_date = postdata['start_date'] if postdata.get("start_date") else None
		loyal_end_date = postdata['end_date'] if postdata.get("end_date") else None
		min_threshold_points = postdata['min_points'] if postdata.get("min_points") else None
		loyalty_desc = postdata['description'] if postdata.get("description") else None
		per_rupees = postdata['per_rupee'] if postdata.get("per_rupee") else None
		loyalty_expire_limit = postdata['expire_limit'] if postdata.get("expire_limit") else None
		website_id = postdata['website_id'] if postdata.get("website_id") else 0

		serializer_data = {"name": name,
							"points": points,
							"loyal_start_date" : loyal_start_date,
							"loyal_end_date": loyal_end_date,
							"min_threshold_points": min_threshold_points,
							"loyalty_desc": loyalty_desc,
							"per_rupees": per_rupees,
							"loyalty_expire_limit": loyalty_expire_limit,
							"created": now_utc,
							"modified": now_utc,
							"website_id": website_id}
		
		record_id = postdata['id'] if postdata.get("id") else None

		if record_id:

			get_record = model.objects.get(id=record_id)
			serializer_data.pop('created')
			serializer = EngageboostCreditPointSerializer(get_record, data=serializer_data, partial=True)

			if serializer.is_valid():
				serializer.save()
				data ={
				'status':1,
				'Message':'Data Updated Successfully',
				}

			else:
				data = {"status":0,
						'api_error':serializer.errors,
						"Message": "Error Occured"}

		else:
			create_record = model.objects.create(**serializer_data)
			data ={
					'status':1,
					'Message':'Data Saved Successfully',
					}

		return Response(data)



		
		



		