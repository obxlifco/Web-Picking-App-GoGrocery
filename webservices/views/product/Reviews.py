from webservices.models import EngageboostProductReviews
from django.http import Http404
from webservices.serializers import ReviewSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime
from rest_framework import generics
from itertools import chain
from django.core import serializers
from django.http import HttpResponse
from webservices.views import loginview
import datetime

class ReviewsList(generics.ListAPIView):
# """ List all users, or create a new user """
	def get_object(self, pk,request):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostProductReviews.objects.using(company_db).get(pk=pk)
		except EngageboostProductReviews.DoesNotExist:
			raise Http404

	# def get_object(self, pk,request):
	#     try:
	#         return EngageboostChannelsCategoriesMaster.objects.using(company_db).get(pk=pk)
	#     except EngageboostChannelsCategoriesMaster.DoesNotExist:
	#         raise Http404



	#///////////////////Fetch Single Row
	def get(self, request, pk, format=None):
		company_db = loginview.db_active_connection(request)
		user = self.get_object(pk,request)
		serializer = ReviewSerializer(user)
		
		
		if(serializer): 
			data ={
				'status':1,
				'api_status':serializer.data,
				
				'message':'',
				}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
		return Response(data)


	def put(self, request, pk, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		Reviews = self.get_object(pk,request)

	
		d1={'created':datetime.now(),'modified':datetime.now(),'replied':datetime.now()}
		
		d2=request.data
		serializer_data=dict(d2,**d1)
		serializer = ReviewSerializer(Reviews,data=serializer_data,partial=True)
		
			  
		if serializer.is_valid():
			serializer.save()

			data ={
			'status':1,
			'api_status':'',
			'message':'Successfully Updated',
			}
			return Response(data)
		else:
			data ={
			'status':0,
			'api_status':serializer.errors,
			'message':'Data Not Found',
			}
			return Response(data)

class flag(generics.ListAPIView):

	def post(self, request,format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		js=request.data
		ourResult = js['table']
		value=ourResult['value']
		ourResult1 = js['data']
		for data in ourResult1:
			queryset=EngageboostProductReviews.objects.using(company_db).filter(id=int(data['id'])).update(isflagged=value)
			data2 ={
					'status':1
					}
		return Response(data2)

class ProductReviews(generics.ListAPIView):
	def post(self, request, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		requestdata     = request.data
		website_id      = requestdata['website_id']
		user_ip         = requestdata['user_ip']
		user_name       = requestdata['user_name']
		user_city       = requestdata['user_city']
		user_state		= requestdata['user_state']
		user_country    = requestdata['user_country']
		title           = requestdata['title']
		review          = requestdata['review']
		rating          = requestdata['rating']
		product_id      = requestdata['product_id']
		user_id        	= requestdata['user_id']
		# reviews = None
  #       if "reviews" in requestdata:
		# 	reviews         = requestdata['reviews']
		review_id = 0
		if "id" in requestdata:
			review_id = requestdata['id']

		now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()

		if review_id >0:
			s_reviews=EngageboostProductReviews.objects.filter(id=review_id).update(
				website_id = website_id,
				user_ip=user_ip,
				user_name=user_name,
				user_city = user_city,
				user_state = user_state,
				user_country = user_country,
				title = title,
				review = review,
				rating = rating,
				product_id = product_id,
				user_id = user_id,
				created = now_utc,
				modified = now_utc,
				replied = now_utc
			)
			data ={
				'status':1,
				'message':'Successfully Updated'
			}
		else:
			qs_reviews=EngageboostProductReviews.objects.create(
				website_id = website_id,
				user_ip=user_ip,
				user_name=user_name,
				user_city = user_city,
				user_state = user_state,
				user_country = user_country,
				title = title,
				review = review,
				rating = rating,
				product_id = product_id,
				user_id = user_id,
				created = now_utc,
				modified = now_utc,
				replied = now_utc
			)
			qs_reviews.save()
			serializer = ReviewSerializer(qs_reviews).data
			if serializer:
				data ={
				'status':1,
				'message':'Successfully Insert',
				'api_status':serializer,
				}	
			
			else:
				data ={
				'status':0,
				'api_status':'',
				'message':'Data Not Found',
				}
		return Response(data)




		
		   