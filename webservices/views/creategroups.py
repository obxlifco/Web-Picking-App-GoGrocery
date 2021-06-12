from django.http import HttpResponse
from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from webservices.models import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user_model, login
from django.db.models import Q
import json
from django.http import JsonResponse
from rest_framework.exceptions import ParseError
from webservices.views import loginview

@csrf_exempt
# Add group class is to insert or update groups table data
def add_group(request) :
	company_db = loginview.db_active_connection(request)
	if request.method == 'POST':
		requestdata = JSONParser().parse(request)
		company_id = requestdata['company_id']
		group_id = requestdata['group_id']
		name = requestdata['name']
		details = requestdata['details']
		language_id = requestdata['language_id']
		ip = request.META.get('REMOTE_ADDR')
		user_id = requestdata['user_id']
		website_id = requestdata['website_id']
		changed_by = requestdata['changed_by']
		masters = requestdata['masters']
		if  group_id == '':
			EngageboostGroups.objects.using(company_db).create(company_id=company_id,masters=masters,name=name,user_id=user_id,website_id=website_id,language_id=language_id,ip_address=ip,createdby=changed_by,created=datetime.now(),modified=datetime.now(),isblocked='0',isdeleted='0')
			data = {
			'status':1,
			'message':'Successfuly Inserted'
			}
			return JsonResponse(data)
		else:
			EngageboostGroups.objects.using(company_db).filter(id=group_id).update(company_id=company_id,masters=masters,name=name,user_id=user_id,website_id=website_id,language_id=language_id,ip_address=ip,createdby=changed_by,created=datetime.now(),modified=datetime.now())
			data = {
			'status':1,
			'message':'Successfuly updateed'
			}
			return JsonResponse(data)