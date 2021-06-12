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
from django.http import JsonResponse
from rest_framework import status
# Import Model And Serializer
from webservices.models import *
from frontapp.frontapp_serializers import *
from frontapp.views.product import discount

from django.db.models import F, Func, FloatField
from django.db.models.functions import Cast

import json
import base64
import sys,os
import traceback
import datetime

from django.db.models import Max,Min,Q
from django.db.models import Count, Sum, Avg
from django.db.models.aggregates import Aggregate
from django.contrib.postgres.aggregates import *
from django.db.models import F,Count,Sum,Avg,FloatField,Case,When,IntegerField

class write_review(APIView):

    def post(self, request, format=None):
        # $this->loadModel('ProductReviewRating');
        # $website_id = $this->get_company_website_id_by_url();
        # $channel_id = 6;
        requestdata = request.data
        user = request.user
        user_id = user.id

        # device_id = requestdata
        # device_type = requestdata
        product_id      = requestdata['product_id']
        review_title    = requestdata['review_title']
        review_message  = requestdata['review_message']
        review_star     = requestdata['review_star']
        # user_id         = request.POST.get('user_id')
        # user_name       = request.POST.get('user_name')
        # review_id       = request.POST.get('review_id')
        # limit           = request.POST.get('limit')
        
        rating_star = []
        review = {}
        data = []
        rs_rating = []
        review_data = []
        review_avg = 0
        now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
        if user_id is not None:
            if product_id is not None:
                rs_product_review = EngageboostProductReviews.objects.filter(isdeleted='n', isblocked='n', isflagged='n', product_id=product_id, user_id=user_id)
                rs_review_cnt = rs_product_review.count()
                if rs_review_cnt<=0:
                    if review_title is not None and review_message is not None and review_star is not None:
                        product_id = product_id;
                        review.update({'website_id':1, 'product_id':product_id, 'channel_id':6, 'user_id':user_id})
                        rs_user = EngageboostUsers.objects.filter(id=user_id).first()
                        user_name = rs_user.first_name + " " + rs_user.last_name

                        ispurchased = HasPurchased(product_id,user_id)
                        review.update({'isblocked':'n', 'title':review_title, 'review':review_message, 'rating':review_star, 'reply':"", 'ispurchased':ispurchased, 'user_name':user_name, 'created':now_utc, 'modified':now_utc})
                        rs_insert = EngageboostProductReviews.objects.create(**review)

                        rs_rating = EngageboostProductReviews.objects.filter(isdeleted='n', isblocked = 'n', isflagged='n', product_id = product_id).values('rating').annotate(rating_count = Count('rating')).order_by('-rating')
                        total_review_count = EngageboostProductReviews.objects.filter(isdeleted='n', isblocked = 'n', isflagged='n', product_id = product_id).count()

                        review_max = 5 
                        user_count = 0 
                        rating_count = 0

                        if rs_rating:
                            for reviews in rs_rating:
                                reviews['percent'] = (reviews['rating_count']/total_review_count)*100
                                rating_count = rating_count + (reviews['rating_count']*reviews['rating'])
                                user_count = user_count + reviews['rating_count']
                        
                        review_avg= 0
                        if rating_count>0 and user_count >0:
                            review_avg = (rating_count/user_count)
                        
                        # $rating_star[0]['count'] = total_review_count; $rating_star[0]['max'] = review_max; $rating_star[0]['avg'] = review_avg;

                        # // get review details
                        rs_review = EngageboostProductReviews.objects.filter(isdeleted='n', isblocked = 'n', isflagged='n', product_id = product_id).order_by("-id")
                        review_data = EngageboostProductReviewsSerializer(rs_review, many=True)
                        review_data = review_data.data
                        ack = "success"
                        msg = "Reviewed successfully done."
                    else :
                        ack = "fail";
                        msg = "All fields are mandatory." ;
                else:
                    rs_rating = EngageboostProductReviews.objects.filter(isdeleted='n', isblocked = 'n', isflagged='n', product_id = product_id).values('rating').annotate(rating_count = Count('rating')).order_by('-rating')
                    total_review_count = EngageboostProductReviews.objects.filter(isdeleted='n', isblocked = 'n', isflagged='n', product_id = product_id).count()

                    review_max = 5 
                    user_count = 0 
                    rating_count = 0

                    if rs_rating:
                        for reviews in rs_rating:
                            reviews['percent'] = (reviews['rating_count']/total_review_count)*100
                            rating_count = rating_count + (reviews['rating_count']*reviews['rating'])
                            user_count = user_count + reviews['rating_count']
                    
                    review_avg= 0
                    if rating_count>0 and user_count >0:
                        review_avg = (rating_count/user_count)
                    
                    # $rating_star[0]['count'] = total_review_count; $rating_star[0]['max'] = review_max; $rating_star[0]['avg'] = review_avg;

                    # // get review details
                    rs_review = EngageboostProductReviews.objects.filter(isdeleted='n', isblocked = 'n', isflagged='n', product_id = product_id).order_by("-id")
                    review_data = EngageboostProductReviewsSerializer(rs_review, many=True)
                    review_data = review_data.data
                    ack = "fail";
                    msg = "You have already reviewed this product." 
            else:
                ack = "fail";
                msg = "Provide product id." 
        else:
            ack = "fail";
            msg = "Please login first." 

        data = {
            "status":1,
            "msg":msg,
            "rating_data":rs_rating,
            "review_data":review_data,
            "review_avg":review_avg
        }   

        return Response(data)


def HasPurchased(product_id=None,user_id=None):
    is_purchased = 'n'
    if user_id is not None:
        has_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
        if has_customer:
            customer_id = has_customer.id

        if product_id is not None:
            rs_order_pro = EngageboostOrderProducts.objects.filter(product_id = product_id, order_id__customer_id = customer_id)
            rs_count = rs_order_pro.count()
            if rs_count>0:
                is_purchased = 'y'
    return is_purchased         


class product_review_stats(APIView):
    permission_classes = []
    def post(self, request, format=None):
        # $device_id 		= isset($this->request->data['device_id'])?$this->request->data['device_id']:'';
        # $device_type 	= isset($this->request->data['device_type'])?$this->request->data['device_type']:'';

        requestdata = request.data
        user = request.user
        user_id = user.id

        product_id 	    = requestdata['product_id']
        limit = 15
        if "limit" in requestdata:
            limit = requestdata['limit']
        page = 0
        if "page" in requestdata:
            page = requestdata['page']

		# offset = '';
		# if(!empty($limit)) {
		# 	$offset = $page*$limit;
		# }

        if product_id:           
            rs_rating = EngageboostProductReviews.objects.filter(isdeleted='n', isblocked = 'n', isflagged='n', product_id = product_id).values('rating').annotate(rating_count = Count('rating')).order_by('-rating')
            total_review_count = EngageboostProductReviews.objects.filter(isdeleted='n', isblocked = 'n', isflagged='n', product_id = product_id).count()

            review_max = 5 
            user_count = 0 
            rating_count = 0

            if rs_rating:
                for reviews in rs_rating:
                    reviews['percent'] = (reviews['rating_count']/total_review_count)*100
                    rating_count = rating_count + (reviews['rating_count']*reviews['rating'])
                    user_count = user_count + reviews['rating_count']
            
            review_avg= 0
            if rating_count>0 and user_count >0:
                review_avg = (rating_count/user_count)
            
			# $rating_star[0]['count'] = total_review_count; $rating_star[0]['max'] = review_max; $rating_star[0]['avg'] = review_avg;

			# // get review details
            rs_review = EngageboostProductReviews.objects.filter(isdeleted='n', isblocked = 'n', isflagged='n', product_id = product_id).order_by("-id")
            review_data = EngageboostProductReviewsSerializer(rs_review, many=True)
            review_data = review_data.data
            ack = "success"
            msg = "success"
        else:
            ack = "fail"
            msg = "Product id is blank."

        data = {
            "status":ack,
            "rating_data":rs_rating,
            "review_data":review_data,
            "review_avg":review_avg
        }   

        return Response(data)
