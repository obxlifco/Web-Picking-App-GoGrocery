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
from frontapp.views.product import discount

class MyWishlist(APIView):
    def get(self, request, format=None): 
        user            = request.user
        user_id         = user.id 
        warehouse_id    = request.META.get('HTTP_WID')
        str_status = ""
        try:
            now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
            # print(user_id)
            create_wishlist=EngageboostWishlists.objects.filter(user_id=user_id,isblocked='n',isdeleted='n').all()
            user_data = WishlistsSerializer(create_wishlist,context={'warehouse_id': warehouse_id},many=True).data               
            if user_data:
                for userdata in user_data:
                    products_discount_data = {
                            "new_default_price": 0,
                            "new_default_price_unit": 0,
                            "discount_price_unit": 0,
                            "discount_price": 0,
                            "discount_amount": 0,
                            "disc_type": "",
                            "coupon": ""
                        }
                    #print(userdata['product']['channel_price'])
                    if  userdata['product']['channel_price'] is not None:
                        for channelprice in userdata['product']['channel_price']:
                            #print(userdata['product']['channel_price']['channel_price'])
                
                            userdata['product']['default_price'] = userdata['product']['channel_price']['channel_price']

                            request_data = {
                                'website_id': userdata['product']['website_id'],
                                'company_id': userdata['product']['website_id'],
                                'product_ids': userdata['product']['id'],
                                'qtys': '1',
                                'prod_price': userdata['product']['channel_price']['channel_price'],
                                'default_price': userdata['product']['channel_price']['channel_price'],
                                'warehouse_id': warehouse_id
                            }
                    
                            products_discount = discount.get_discount_detalils(request_data)    
                            for productsdiscount in products_discount:
                                products_discount_data.update({
                                    "new_default_price": productsdiscount['new_default_price'],
                                    "new_default_price_unit": productsdiscount['new_default_price_unit'],
                                    "discount_price_unit": productsdiscount['discount_price_unit'],
                                    "discount_price": productsdiscount['discount_price'],
                                    "discount_amount": productsdiscount['discount_amount'],
                                    "disc_type": productsdiscount['disc_type'],
                                    "coupon": productsdiscount['coupon']
                                    })
                               
                        userdata.update(products_discount_data)
                    
                str_status = status.HTTP_200_OK
                data = {
                    'status':str_status,
                    'data':user_data
                    }
            else:
                str_status = status.HTTP_200_OK
                data = {
                    'status':str_status,
                    'message': 'No data found',
                    'data':[]
                }      
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status":str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response (data)  

    def post(self, request, format=None): 
        requestdata     = JSONParser().parse(request)     
        user            = request.user
        user_id         = user.id
        website_id      = requestdata['website_id']
        product_id      = requestdata['product_id']
        str_status = ""
        
        try:
            if website_id=='':
                raise Exception("website id is required") 
            if product_id=='':
                raise Exception("product id is required") 
            now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
            qs_product = EngageboostProducts.objects.filter(id=product_id,isblocked='n',isdeleted='n').exists()  
            if qs_product:
                qs_wishlist=EngageboostWishlists.objects.filter(user_id=user_id,product_id=product_id,isblocked='n',isdeleted='n').count()
                
                if qs_wishlist>=1:
                    str_status = status.HTTP_200_OK
                    data = {
                    'status':str_status,
                    'message': 'This product is already in your wishlist',
                    } 
                else:
                    create_wishlist=EngageboostWishlists.objects.create(
                        user_id =   user_id,
                        website_id = website_id,
                        product_id = product_id,
                        created  =  now_utc,
                        modified = now_utc
                    ) 
                    create_wishlist.save()
                    user_data = WishlistsSerializer(create_wishlist).data  
                    product_count=EngageboostWishlists.objects.filter(user_id=user_id,isblocked='n',isdeleted='n').values_list('product_id', flat=True).count()
                    user_data.update({"total_count":product_count})              
                    if user_data:
                        str_status = status.HTTP_200_OK
                        data = {
                        'status':str_status,
                        'message': 'Item added to wishlist.',
                        'data':user_data
                        } 
            else: 
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                'status':str_status,
                'message': 'product is not present',
                }
            
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status":str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response (data,str_status)  


class DeleteWishlist(APIView): 
    def post(self, request,format=None):
        requestdata             = JSONParser().parse(request)    
        user                    =  request.user
        user_id                 =  user.id
        product_id              =  requestdata['product_id']
        # print(user_id)
        str_status = ""
        try: 
            if product_id=='':
                raise Exception("Product id is required") 
            qs_wishlists = EngageboostWishlists.objects.filter(product_id=product_id,user_id=user_id).exists()
            
            if qs_wishlists:
                EngageboostWishlists.objects.filter(product_id=product_id,user_id=user_id).delete()
                str_status = status.HTTP_200_OK
                data = {
                    'status':str_status,
                    'message': 'Item deleted from wishlist.',
                }
            else:
                str_status = status.HTTP_401_UNAUTHORIZED
                data = {
                    'status':str_status,
                    'message': 'You are not allowed to delete this product.',
                }
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status":str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response(data,str_status)

#----Test-----#
class DeleteWishlistTest(APIView):
    def post(self, request,format=None):
        requestdata             = JSONParser().parse(request)
        user                    =  request.user
        user_id                 =  user.id
        product_id              =  requestdata['product_id']

        # -------Binayak Start 23-12-2020--------#
        if 'warehouse_id' in  requestdata:
            warehouse_id        =  requestdata['warehouse_id']
        else:
            warehouse_id        =  None
        # -------Binayak End 23-12-2020--------#

        # print(user_id)
        str_status = ""
        try:
            if product_id=='':
                raise Exception("Product id is required")
            qs_wishlists = EngageboostWishlists.objects.filter(product_id=product_id,user_id=user_id).exists()

            if qs_wishlists:
                EngageboostWishlists.objects.filter(product_id=product_id,user_id=user_id).delete()

                #-------Binayak Start 23-12-2020--------#
                if warehouse_id != None:
                    now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
                    # print(user_id)
                    create_wishlist = EngageboostWishlists.objects.filter(user_id=user_id, isblocked='n',
                                                                          isdeleted='n').all()
                    user_data = WishlistsSerializer(create_wishlist, context={'warehouse_id': warehouse_id}, many=True).data
                    if user_data:
                        for userdata in user_data:
                            products_discount_data = {
                                "new_default_price": 0,
                                "new_default_price_unit": 0,
                                "discount_price_unit": 0,
                                "discount_price": 0,
                                "discount_amount": 0,
                                "disc_type": "",
                                "coupon": ""
                            }
                            # print(userdata['product']['channel_price'])
                            if userdata['product']['channel_price'] is not None:
                                for channelprice in userdata['product']['channel_price']:
                                    # print(userdata['product']['channel_price']['channel_price'])

                                    userdata['product']['default_price'] = userdata['product']['channel_price'][
                                        'channel_price']

                                    request_data = {
                                        'website_id': userdata['product']['website_id'],
                                        'company_id': userdata['product']['website_id'],
                                        'product_ids': userdata['product']['id'],
                                        'qtys': '1',
                                        'prod_price': userdata['product']['channel_price']['channel_price'],
                                        'default_price': userdata['product']['channel_price']['channel_price'],
                                        'warehouse_id': warehouse_id
                                    }

                                    products_discount = discount.get_discount_detalils(request_data)
                                    for productsdiscount in products_discount:
                                        products_discount_data.update({
                                            "new_default_price": productsdiscount['new_default_price'],
                                            "new_default_price_unit": productsdiscount['new_default_price_unit'],
                                            "discount_price_unit": productsdiscount['discount_price_unit'],
                                            "discount_price": productsdiscount['discount_price'],
                                            "discount_amount": productsdiscount['discount_amount'],
                                            "disc_type": productsdiscount['disc_type'],
                                            "coupon": productsdiscount['coupon']
                                        })

                                userdata.update(products_discount_data)
                else:
                    user_data = []

                str_status = status.HTTP_200_OK
                data = {
                    'status':str_status,
                    'message': 'Item deleted from wishlist.',
                    'data': user_data
                }
            else:
                str_status = status.HTTP_401_UNAUTHORIZED
                data = {
                    'status':str_status,
                    'message': 'You are not allowed to delete this product.',
                    'data': []
                }

                # -------Binayak End 23-12-2020--------#

        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status":str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response(data,str_status)
#----Test-----#


class GetWishlistCount(APIView): 
    def get(self, request,format=None):
        user                    =  request.user
        user_id                 =  user.id
        str_status = ""
        try: 
            product_count=EngageboostWishlists.objects.filter(user_id=user_id,isblocked='n',isdeleted='n').exclude(product_id__isnull=True).count()
            if product_count>0:
                str_status = status.HTTP_200_OK
                data = {
                    'status':str_status,
                    'total_count': product_count,
                }
            else:
                str_status = status.HTTP_200_OK
                data = {
                    'status':str_status,
                    'total_count': 0
                }


        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status":str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response(data,str_status)


class EmptyWishlist(APIView):
    def get(self, request,format=None):
        # requestdata             = JSONParser().parse(request)
        user                    =  request.user
        user_id                 =  user.id
        # product_id              =  requestdata['product_id']


        try:
            EngageboostWishlists.objects.filter(user_id=user_id).delete()


            str_status = status.HTTP_200_OK
            data = {
                'status':str_status,
                'message': 'Empty from wishlist successfull.'
            }

        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status":str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response(data,str_status)