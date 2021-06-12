from django.shortcuts import render
from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

import datetime
import time

import django.db.models
from django.db.models import Avg, Max, Min, Sum, Count
from django import template
from django.template import loader
from django.template import Template
from django.core.mail import send_mail
from django.db.models import TimeField
from django.utils import timezone
from datetime import timedelta

# Import Model And Serializer
from webservices.models import *
from frontapp.frontapp_serializers import *
from frontapp.views.product import discount

import json
import base64
import sys,math
import traceback

from webservices.views.common import common
from webservices.views.emailcomponent import emailcomponent
from frontapp.views.sitecommon import common_functions

from pytz import timezone

from django.core.mail import send_mail
from decimal import Decimal

# START LOYALTY POINTS
def common_data(a, b, condition): 
    a_set = set(a) 
    b_set = set(b) 
    if (a_set and b_set):
        if condition == '==':
            return True 
        if condition == '!=':
           return False 
    else:
        if condition == '==':
            return False 
        if condition == '!=':
           return True 


def EarnCreditPoints(order_id, user_id, website_id = None):
    customer_id = user_id    
    rs_order = EngageboostOrdermaster.objects.filter(id = order_id).first()
    price = rs_order.net_amount
    category_flag           = True
    product_flag            = True
    coustomer_flag          = True
    customer_group_flag     = True
    order_amount_flag       = True
    loyelty_serializer_arr  = {}
    today = django.utils.timezone.now()

    # category_ids
    rs_order_products   = EngageboostOrderProducts.objects.filter(order_id = order_id).values_list('product_id', flat = True)
    rs_prod_cat         = EngageboostProductCategories.objects.filter(product_id__in = rs_order_products).values_list('category_id', flat = True)
    category_ids = list(rs_prod_cat)
    credit_rs = EngageboostCreditPoint.objects.filter(isdeleted='n', isblocked='n', loyal_end_date__gte=today, loyal_type="earn").first()
    if credit_rs and credit_rs is not None:
        credit_data = EngageboostCreditPointSerializer(credit_rs).data
        if credit_data:
            if len(credit_data["CreditPointConditions"]) > 0 :
                for creadit_point in credit_data["CreditPointConditions"]:
                    if creadit_point["fields"] == 0:  ### For Category Checking
                        category_flag = False
                        all_category_ids = creadit_point["all_category_id"].split(',')
                        result = common_data(all_category_ids, category_ids, creadit_point["condition"])
                        category_flag = result 

                    if creadit_point["fields"] == 13633:  ### For SKU Checking
                        product_flag = False
                        all_product_ids = creadit_point["all_product_id"].split(',')
                        result = common_data(all_product_ids, product_ids, creadit_point["condition"])
                        product_flag = result

                    if creadit_point["fields"] == -1:  ### For Order Amount Checking
                        order_amount_flag = False
                        order_amount = creadit_point["value"]
                        condition = str(creadit_point["condition"])
                        if condition == '<=':
                            if int(price) <= int(order_amount):
                                order_amount_flag = True
                        if condition == '>=':
                            if int(price) >= int(order_amount):
                                order_amount_flag = True
                        if condition == '==':
                            if int(order_amount) == int(price):
                                order_amount_flag = True
                        if condition == '!=':
                            if int(order_amount) != int(price):
                                order_amount_flag = True
                    if creadit_point["fields"] == -2:  ### For Customer Checking
                        coustomer_flag = False
                        all_customer_ids = creadit_point["all_customer_id"].split(',')
                        result = common_data(all_customer_ids, customer_ids, creadit_point["condition"])
                        coustomer_flag = result
                    if creadit_point["fields"] == -3:  ### For Customer Group Checking
                        customer_group_flag = False
                        all_customer_group_ids = creadit_point["all_customer_id"].split(',')
                        result = common_data(all_customer_group_ids, customer_ids, creadit_point["condition"])
                        customer_group_flag = result
            if order_amount_flag == True and product_flag == True and category_flag == True:
                if credit_data["applied_as"] == 'percentage':
                    earn_points = 0
                    earn_points = ((float(price) / float(100)) * float(credit_data["points"]))
                if credit_data["applied_as"] == 'fixed':
                    earn_points_in_price = (float(price) / float(credit_data["per_rupees"]))
                    earn_points = float(credit_data["points"]) * float(earn_points_in_price)
                    # ((float(price) / float(credit_data["per_rupees"])) * float(credit_data["points"]))
                valid_to = django.utils.timezone.now() + timedelta(days=credit_data["loyalty_expire_days"])
                loyalty_in_amount = common_functions.pointToAmount_converter(earn_points, website_id)
                # print('(((((((((((((((((()))))))))))))))))))))))))', loyalty_in_amount)

                balance = GetUserLoyaltyBalance(user_id, order_id)

                loyaltypoints_obj = {}
                loyaltypoints_obj = {
                    "website_id": website_id,
                    "rule_id": credit_data["id"],
                    "customer_id": customer_id,
                    "order_id": order_id,
                    "custom_order_id": rs_order.custom_order_id,
                    # "customer_contact_no": customer_contact_no,
                    "description": 'This is test loyelty points',
                    "received_points": earn_points,
                    "burnt_points": 0.00,
                    "amount": loyalty_in_amount,
                    "received_burnt": 0.00,
                    "status": "earn",
                    "created": django.utils.timezone.now(),
                    "valid_form": django.utils.timezone.now(),
                    "expiry_date": valid_to,
                    "remaining_balance":float(balance)+int(Decimal(earn_points)),
                    # "processing_status": 'complete'
                }
                loyelty_serializer_arr = dict(loyelty_serializer_arr,**loyaltypoints_obj)
                rs_loyalty = EngageboostCustomerLoyaltypoints.objects.filter(order_id=order_id).count()
                if rs_loyalty>0:
                    EngageboostCustomerLoyaltypoints.objects.filter(order_id=order_id).update(**loyelty_serializer_arr)
                else:
                    save_loyalty_points = EngageboostCustomerLoyaltypoints.objects.create(**loyelty_serializer_arr)
                        
        data = {"status":1,"data":credit_data}
    else:
        data = {"status":0,"data":[]}
    # print('Earn Data', data)
    return Response(data)

class earn_creadit_points(APIView):
    def post(self, request, *args, **kwargs):
        requestdata         = request.data
        website_id          = requestdata['website_id']
        order_id            = requestdata['order_id']       
        user = request.user
        user_id = user.id
        customer_id = user_id
        
        rs_order = EngageboostOrdermaster.objects.filter(id = order_id).first()
        price = rs_order.net_amount
        category_flag           = True
        product_flag            = True
        coustomer_flag          = True
        customer_group_flag     = True
        order_amount_flag       = True
        loyelty_serializer_arr  = {}
        today = django.utils.timezone.now()
        credit_rs = EngageboostCreditPoint.objects.filter(isdeleted='n', isblocked='n', loyal_end_date__gte=today, loyal_type="earn").first()
        if credit_rs and credit_rs is not None:
            credit_data = EngageboostCreditPointSerializer(credit_rs).data
            if credit_data:
                if len(credit_data["CreditPointConditions"]) > 0 :
                    for creadit_point in credit_data["CreditPointConditions"]:
                        if creadit_point["fields"] == 0:  ### For Category Checking
                            category_flag = False
                            all_category_ids = creadit_point["all_category_id"].split(',')
                            result = common_data(all_category_ids, category_ids, creadit_point["condition"])
                            category_flag = result 

                        if creadit_point["fields"] == 13633:  ### For SKU Checking
                            product_flag = False
                            all_product_ids = creadit_point["all_product_id"].split(',')
                            result = common_data(all_product_ids, product_ids, creadit_point["condition"])
                            product_flag = result

                        if creadit_point["fields"] == -1:  ### For Order Amount Checking
                            order_amount_flag = False
                            order_amount = creadit_point["value"]
                            condition = str(creadit_point["condition"])
                            if condition == '<=':
                                if int(price) <= int(order_amount):
                                    order_amount_flag = True
                            if condition == '>=':
                                if int(price) >= int(order_amount):
                                    order_amount_flag = True
                            if condition == '==':
                                if int(order_amount) == int(price):
                                    order_amount_flag = True
                            if condition == '!=':
                                if int(order_amount) != int(price):
                                    order_amount_flag = True
                        if creadit_point["fields"] == -2:  ### For Customer Checking
                            coustomer_flag = False
                            all_customer_ids = creadit_point["all_customer_id"].split(',')
                            result = common_data(all_customer_ids, customer_ids, creadit_point["condition"])
                            coustomer_flag = result
                        if creadit_point["fields"] == -3:  ### For Customer Group Checking
                            customer_group_flag = False
                            all_customer_group_ids = creadit_point["all_customer_id"].split(',')
                            result = common_data(all_customer_group_ids, customer_ids, creadit_point["condition"])
                            customer_group_flag = result

                if order_amount_flag == True and product_flag == True and category_flag == True:
                    if credit_data["applied_as"] == 'percentage':
                        earn_points = 0
                        earn_points = ((float(price) / float(100)) * float(credit_data["points"]))
                    if credit_data["applied_as"] == 'fixed':
                        earn_points_in_price = (float(price) / float(credit_data["per_rupees"]))
                        earn_points = float(credit_data["points"]) * float(earn_points_in_price)
                        # ((float(price) / float(credit_data["per_rupees"])) * float(credit_data["points"]))
                    valid_to = django.utils.timezone.now() + timedelta(days=credit_data["loyalty_expire_days"])
                    loyalty_in_amount = common_functions.pointToAmount_converter(earn_points, website_id)
                    # print('(((((((((((((((((()))))))))))))))))))))))))', loyalty_in_amount)
                    loyaltypoints_obj = {}
                    loyaltypoints_obj = {
                        "website_id": website_id,
                        "rule_id": credit_data["id"],
                        "customer_id": customer_id,
                        "order_id": order_id,
                        "custom_order_id": rs_order.custom_order_id,
                        # "customer_contact_no": customer_contact_no,
                        "description": 'This is test loyelty points',
                        "received_points": earn_points,
                        "burnt_points": 0.00,
                        "amount": loyalty_in_amount,
                        "received_burnt": 0.00,
                        "status": "earn",
                        "created": django.utils.timezone.now(),
                        "valid_form": django.utils.timezone.now(),
                        "expiry_date": valid_to,
                        # "processing_status": 'complete'
                    }
                    loyelty_serializer_arr = dict(loyelty_serializer_arr,**loyaltypoints_obj)
                    rs_loyalty = EngageboostCustomerLoyaltypoints.objects.filter(order_id=order_id).count()
                    if rs_loyalty>0:
                        EngageboostCustomerLoyaltypoints.objects.filter(order_id=order_id).update(**loyelty_serializer_arr)
                    else:
                        save_loyalty_points = EngageboostCustomerLoyaltypoints.objects.create(**loyelty_serializer_arr)
                            
            data = {"status":0,"data":credit_data}
        else:
            data = {"status":0,"data":[]}
        # print('Earn Data', data)
        return Response(data)

#  It is for calculation of burn points based on condition fra an perticular order
def get_creadit_points(cart_data, user_id):
    # order_id = order_id
    # rs_order_details    = EngageboostOrdermaster.objects.filter(id = order_id ).first() 
    # rs_order_products   = EngageboostOrderProducts.objects.filter(order_id = order_id).values_list('product_id', flat = True)
    # rs_prod_cat         = EngageboostProductCategories.objects.filter(product_id__in = rs_order_products).values_list('category_id', flat = True)
    product_ids = []
    product_id_price = []
    category_ids = []
    if cart_data and len(cart_data['cartdetails'])>0:
        for prod_details in cart_data['cartdetails']:
            product_price_obj = {}
            product_ids.append(prod_details['id'])
            product_price_obj.update({"product_id":prod_details['id'], "price":prod_details['new_default_price']})
            product_id_price.append(product_price_obj)
            category_ids.append(prod_details['category_id'])

    product_ids     = list(set(product_ids))
    category_ids    = list(set(category_ids))

    customer_id     = user_id
    price           = cart_data['orderamountdetails'][0]['sub_total']
    # custom_order_id = rs_order_details.custom_order_id

    earn_points         = 0
    category_flag           = True
    product_flag            = True
    coustomer_flag          = True
    customer_group_flag     = True
    order_amount            = True
    flag = False
    rule_id = 0
    redeem_limit = 0
    # print(request)
    today = django.utils.timezone.now()
    # credit_rs = EngageboostCreditPoint.objects.filter(isdeleted='n', isblocked='n', loyal_end_date__gte=today, loyal_type="burn").all()
    # credit_data = EngageboostCreditPointSerializer(credit_rs)
    credit_rs = EngageboostCreditPoint.objects.filter(isdeleted='n', isblocked='n',loyal_type="burn").last()
    # if credit_data and credit_data is not None:
    if credit_rs and credit_rs is not None:
        credit_data = EngageboostCreditPointSerializer(credit_rs)
        credit_data = credit_data.data
        rule_id = credit_data['id']
        redeem_limit = credit_data['redeem_limit']

        if credit_data["CreditPointConditions"]:
            if len(credit_data["CreditPointConditions"]) > 0 :
                for creadit_point in credit_data["CreditPointConditions"]:
                    if creadit_point["fields"] == 0:  ### For Category Checking
                        all_category_ids = creadit_point["all_category_id"].split(',')
                        result = common_data(all_category_ids, category_ids, creadit_point["condition"])
                        category_flag = result
                        flag = result
                    if creadit_point["fields"] == 13633:  ### For SKU Checking
                        all_product_ids = creadit_point["all_product_id"].split(',')
                        result = common_data(all_product_ids, product_ids, creadit_point["condition"])
                        product_flag = result
                    if creadit_point["fields"] == -1:  ### For Order Amount Checking
                        order_amount_value = creadit_point["value"]
                        condition = str(creadit_point["condition"])
                        # print('Order Amount', condition)
                        if condition == '<=':
                            if int(order_amount_value) <= int(price):
                                order_amount = True
                        if condition == '>=':
                            if int(order_amount_value) >= int(price):
                                order_amount = True
                        if condition == '==':
                            if int(order_amount_value) == int(price):
                                order_amount = True
                        if condition == '!=':
                            if int(order_amount_value) != int(price):
                                order_amount = True

                    if creadit_point["fields"] == -2:  ### For Customer Checking
                        all_customer_ids = creadit_point["all_customer_id"].split(',')
                        result = common_data(all_customer_ids, customer_ids, creadit_point["condition"])
                        coustomer_flag = result

                    if creadit_point["fields"] == -3:  ### For Customer Group Checking
                        all_customer_group_ids = creadit_point["all_customer_id"].split(',')
                        result = common_data(all_customer_group_ids, customer_ids, creadit_point["condition"])
                        customer_group_flag = result
            else:
                category_flag           = True
                product_flag            = True
                coustomer_flag          = True
                customer_group_flag     = True
                order_amount            = True
            if customer_group_flag == True and coustomer_flag == True and order_amount == True and product_flag == True and category_flag == True:
                if credit_data["applied_as"].lower() == 'percentage':
                    earn_points = ((float(price) / float(100)) * float(credit_data["points"]))
                if credit_data["applied_as"] == 'fixed':
                    earn_points_in_price = (float(price) / float(credit_data["per_rupees"]))
                    earn_points = float(credit_data["points"]) * float(earn_points_in_price)
                    # ((float(price) / float(credit_data["per_rupees"])) * float(credit_data["points"]))
                # valid_to = django.utils.timezone.now() + timedelta(days=credit_data["loyalty_expire_days"])
           
        data = {"status":1,"burn_point":earn_points, "rule_id":rule_id, "redeem_limit":redeem_limit}
    else:
        data = {"status":0,"burn_point":0, "rule_id":rule_id, "redeem_limit":redeem_limit}
    
    return data


def save_burn_points(request):
    if request and int(request['order_id'])>0:
        balance = GetUserLoyaltyBalance(request['customer_id'], request['order_id'])
        check_exist = EngageboostCustomerLoyaltypoints.objects.filter(order_id=request['order_id'], status='burn').count()
        if check_exist>0:
            request['remaining_balance'] = float(balance) - float(request['burnt_points'])
            save_loyalty_points = EngageboostCustomerLoyaltypoints.objects.filter(order_id=request['order_id'], status='burn').update(**request)
            data={"status":1,"message": "loyelty points save successfully."}
        else:
            request['remaining_balance'] = float(balance) - float(request['burnt_points'])
            save_loyalty_points = EngageboostCustomerLoyaltypoints.objects.create(**request)
            data={"status":1,"message": "loyelty points save successfully."}
        return data

def GetUserLoyaltyBalance(user_id, order_id=None):
    now_utc = datetime.now(timezone('UTC')).astimezone(timezone('Asia/Dubai'))
    to_day      = now_utc.strftime('%Y-%m-%d')
    # rs_loyalty = EngageboostCustomerLoyaltypoints.objects.filter(customer_id =user_id, valid_form__date__lte=to_day, expiry_date__date__gte=to_day).annotate(total_amount = Sum('amount')).values('status', 'total_amount')
    rs_loyalty = EngageboostCustomerLoyaltypoints.objects.filter(customer_id =user_id).annotate(total_amount = Sum('amount')).values('status', 'total_amount')
    if order_id is not None and order_id>0:
        rs_loyalty = rs_loyalty.exclude(order_id = order_id)

    balance_amount = 0
    earn_amount = 0
    burn_amount = 0
    if rs_loyalty:
        for loyalty_amount in rs_loyalty:
            if loyalty_amount['status'].lower() == 'earn':
                earn_amount = float(earn_amount) + float(loyalty_amount['total_amount'])
            if loyalty_amount['status'].lower() == 'burn':
                burn_amount = float(burn_amount) + loyalty_amount['total_amount']
        if float(earn_amount) > float(burn_amount):
            balance_amount = float(earn_amount) - float(burn_amount)
    return balance_amount

class LoyaltyPointsLog(APIView):
    def get(self, request, format=None):
        user = request.user
        user_id = user.id
        str_status = ""
        rs_loyalty = EngageboostCustomerLoyaltypoints.objects.filter(customer_id = user_id)
        # rs_loyalty1 = EngageboostCustomerLoyaltypoints.objects.filter(customer_id =user_id).annotate(total_received_points = Sum('received_points'), total_burnt_points=Sum('burnt_points'), total_received_burnt=Sum('received_burnt')).values('status', 'total_received_points', 'valid_form', 'burnt_points', 'total_burnt_points','total_received_burnt')
        loyalty_points_data = []
        if rs_loyalty:
            loyalty_points_data = EngageboostCustomerLoyaltypointsSerializer(rs_loyalty, many=True)
            loyalty_points_data = loyalty_points_data.data
            str_status = status.HTTP_200_OK
        else:
            str_status = status.HTTP_204_NO_CONTENT
        
        data = {
            "status":str_status,
            "data":loyalty_points_data
        }
        return Response(data,str_status)

def remaning_return_loyelty_points(user_id):
    #### 0= no remain_loyelty, 1 = remain_loyelty equal to payment_amount, 2 = payment_amount grater then remain_loyelty
    # user_id = request['user_id']
    user_id = 2
    remain_loyelty = 0
    payment_due = 0
    loyalty_rs = EngageboostCustomerLoyaltypoints.objects.filter(customer_id=user_id, status='return').all()
    if loyalty_rs:
        for loyalty in loyalty_rs:
            remain_loyelty += loyalty.amount
        loyelty_serializer_arr = {}
        total_points = commonfunction.amountToPoint_converter(request["payment_amount"], request["website_id"])
        if remain_loyelty >= request["payment_amount"]:
            request_obj = {
                    "website_id": request["website_id"],
                    "rule_id": request["rule_id"],
                    "customer_id": request["customer_id"],
                    "order_id": request["order_id"],
                    "custom_order_id": request["custom_order_id"],
                    "customer_contact_no": request["customer_contact_no"],
                    "description": 'This is burn for order no ' + request["custom_order_id"],
                    "received_points": 0.00,
                    "burnt_points": total_points,
                    "amount": request["payment_amount"],
                    "received_burnt": total_points,
                    "status": "returnburn",
                    "processing_status": "complete",
                    "created": django.utils.timezone.now(),
                    "valid_form": django.utils.timezone.now()
                    # "expiry_date": valid_to
                }
            loyelty_serializer_arr = dict(loyelty_serializer_arr,**request_obj)
            save_loyalty_points = EngageboostCustomerLoyaltypoints.objects.create(**loyelty_serializer_arr)
            data ={'status':1, 'payment_due':payment_due}
        if remain_loyelty < request["payment_amount"]:
            payment_due = float(request["payment_amount"]) - float(remain_loyelty)
            request_obj = {
                    "website_id": request["website_id"],
                    "rule_id": request["rule_id"],
                    "customer_id": request["customer_id"],
                    "order_id": request["order_id"],
                    "custom_order_id": request["custom_order_id"],
                    "customer_contact_no": request["customer_contact_no"],
                    "description": 'This is burn for order no ' + request["custom_order_id"],
                    "received_points": 0.00,
                    "burnt_points": total_points,
                    "amount": request["payment_amount"],
                    "received_burnt": total_points,
                    "status": "returnburn",
                    "processing_status": "complete",
                    "created": django.utils.timezone.now(),
                    "valid_form": django.utils.timezone.now()
                    # "expiry_date": valid_to
                }
            loyelty_serializer_arr = dict(loyelty_serializer_arr,**request_obj)
            save_loyalty_points = EngageboostCustomerLoyaltypoints.objects.create(**loyelty_serializer_arr)
            data ={'status':2, 'payment_due':payment_due}
    else:
        data ={'status':0, 'payment_due':payment_due}
    return data

class Loyaltypoints(APIView):
    permission_classes = []
    def post(self, request, format=None):
        website_id = request.META.get('HTTP_WID')
        if website_id:
            website_id = website_id
        else:
            website_id = 1
        loyelty = []
        requestdata = request.data
        # user = request.user
        # user_id = user.id
        order_id = requestdata["order_id"]
        rs_order = EngageboostOrdermaster.objects.filter(id=order_id).first()
        order_price = rs_order.net_amount
        customer_id = rs_order.customer_id
        # Get User id and customer id from order id
        rs_customer = EngageboostCustomers.objects.filter(id = customer_id).first()
        user_id = rs_customer.auth_user_id

        customer_ids = []
        customer_ids.append(user_id)
        loyalty_data = []
        final_obj = {}
        return_data = {
            "minimum_order_amount": 0,
            "total_earn_amount": 0,
            "total_earn_points": 0,
            "total_burn_amount": 0,
            "total_burn_points": 0,
            "max_loyalty_amount_use_limit": 0,
            "loyalty_amount": 0,
            "loyalty_points":0,
            "remaning_earn_amount": 0,
            "remaning_earn_points": 0,
            "loyalty_end_date":"",
            "rule_id":0
        }
        return_loyalty = {
           'return_loyalty_valid_from': '25-05-2019',
           'return_loyalty_valid_to': '25-10-2019',
           'return_loyalty_amount': 0,
           'return_loyalty_points': 0
        }
        # customer_dtl = customer_detalils(customer_contact_no, website_id)
        # today = django.utils.timezone.now()
        now_utc = datetime.now(timezone('UTC')).astimezone(timezone('Asia/Dubai'))
        today      = now_utc.strftime('%Y-%m-%d')

        loyaltypoints_rs = EngageboostCustomerLoyaltypoints.objects.filter(customer_id=user_id, status="earn", expiry_date__date__gte=today).values('customer_id').all().annotate(total_earn_amount=Sum('amount'), total_earn_points=Sum('received_points'))
        
        burnloyaltypoints_rs = EngageboostCustomerLoyaltypoints.objects.filter(customer_id=user_id, status="burn").all()

        total_burnloyelty = 0
        total_burnloyelty_points = 0
        if burnloyaltypoints_rs:
            for burn in burnloyaltypoints_rs:
                total_burnloyelty += burn.amount
                total_burnloyelty_points += burn.burnt_points
            
        return_data.update({'total_burn_amount': total_burnloyelty})
        rule_id = 0
        total_earn_amount = 0
        total_earn_points = 0
        remaining_amount = 0
        remaining_burn_points = 0
        burn_rupee = 0
        if loyaltypoints_rs:
            # loyalty_data = EngageboostCustomerLoyaltypointsSerializer(loyaltypoints_rs, many=True).data
            for loyalty in loyaltypoints_rs:
                total_earn_amount += loyalty["total_earn_amount"]
                total_earn_points += loyalty["total_earn_points"]
            if total_earn_amount > total_burnloyelty:
                remaining_amount = int(total_earn_amount) - int(total_burnloyelty)
                remaining_burn_points = int(total_earn_points) - int(total_burnloyelty_points)
            return_data.update({'total_earn_amount': total_earn_amount})
            return_data.update({'total_earn_points': total_earn_points})
            return_data.update({'remaning_earn_amount': remaining_amount})
            return_data.update({'remaning_earn_points': remaining_burn_points})

            credit_rs = EngageboostCreditPoint.objects.filter(isdeleted='n', isblocked='n', loyal_type="burn", website_id=website_id).last()
            if credit_rs is not None:
                credit_data = EngageboostCreditPointSerializer(credit_rs).data 
                # print(json.dumps(credit_data))
                if credit_data:
                    burn_rupee = 0
                    if credit_data["per_rupees"] is not None:
                        if credit_data["per_rupees"] <= order_price:
                            point_rupees = int(order_price) / int(credit_data["per_rupees"])
                            burn_rupee = int(point_rupees) * int(credit_data["points"])
                            if total_burnloyelty < total_earn_amount:
                                burn_rupee = int(burn_rupee)
                            else:
                                burn_rupee = 0 

                            if burn_rupee >= credit_data["redeem_limit"]:
                                if remaining_amount < burn_rupee:
                                    if remaining_amount < credit_data["redeem_limit"]:
                                        burn_rupee = remaining_amount
                                    else:
                                        burn_rupee = credit_data["redeem_limit"]
                                else:
                                    burn_rupee = credit_data["redeem_limit"]
                            
                        return_data.update({'loyalty_amount': burn_rupee})
                        return_data.update({'loyalty_points': credit_data["points"]})
                    else:
                        return_data.update({'loyalty_amount': credit_data["points"]})
                        return_data.update({'loyalty_points': credit_data["points"]})

                    return_data.update({'max_loyalty_amount_use_limit': credit_data["redeem_limit"]})
                    return_data.update({'minimum_order_amount': credit_data["per_rupees"]})
                    return_data.update({'loyalty_end_date': credit_data["loyal_end_date"]})
                    return_data.update({'rule_id': credit_data["id"]})
        ###### Get All Return Loyalty Amount ######
        total_return_loyalty = 0
        total_return_loyalty_points = 0
        total_burnloyelty = 0
        total_burnloyelty_points = 0
        remaining_return_loyalty = 0
        remaining_return_loyalty_points = 0
        returnloyalty_rs = EngageboostCustomerLoyaltypoints.objects.filter(customer_id=user_id, status="return").values('customer_id').all().annotate(total_return_amount=Sum('amount'), total_earn_points=Sum('received_points'))
        ###### Get All Return Burn Loyalty Amount ######
        returnburnloyalty_rs = EngageboostCustomerLoyaltypoints.objects.filter(customer_id=user_id, status="returnburn").values('customer_id').all().annotate(total_return_burn_amount=Sum('amount'), total_burn_points=Sum('burnt_points'))
        if returnloyalty_rs:
            for returnloyalty in returnloyalty_rs:
                 total_return_loyalty += returnloyalty["total_return_amount"]
                 total_return_loyalty_points += returnloyalty["total_earn_points"]
        if returnburnloyalty_rs:
            for returnburnloyalty in returnburnloyalty_rs:
                 total_burnloyelty += returnburnloyalty["total_return_burn_amount"]
                 total_burnloyelty_points += returnburnloyalty["total_burn_points"]

        if total_return_loyalty > total_burnloyelty:       
            remaining_return_loyalty = float(total_return_loyalty) - float(total_burnloyelty)
        if total_return_loyalty_points > total_burnloyelty_points:
            remaining_return_loyalty_points = float(total_return_loyalty_points) - float(total_burnloyelty_points)
        return_loyalty.update({'return_loyalty_amount': remaining_return_loyalty})
        return_loyalty.update({'return_loyalty_points': remaining_return_loyalty_points})
        final_obj.update({'burn_loyalty':return_data, 'return_loyalty':return_loyalty})
        loyalty_data.append(final_obj)
        data ={
            'status':1,
            'message':'Success',
            'data':loyalty_data
            # 'data1':loyalty_points
        }
        return Response(data)

class ApplyLoyalty(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        # user                = request.user
        # user_id             = user.id
        device_id           = request.META.get('HTTP_DEVICEID')
        warehouse_id        = request.META.get('HTTP_WAREHOUSE')
        if warehouse_id is None or warehouse_id == 0:
            warehouse_id = 2

        website_id = get_company_website_id_by_url()
        company_id = get_company_id_by_url()

        requestdata = request.data
        coupon_code = None
        
        # Need when pay before create order
        # if "coupon_code" in requestdata:
        #     coupon_code = requestdata["coupon_code"]

        # if "warehouse_id" in requestdata:
        #     warehouse_id = requestdata["warehouse_id"]        
        
        if "loyalty_amount" in requestdata:
            loyalty_amount = requestdata["loyalty_amount"]
        
        if "order_id" in requestdata:
            order_id = requestdata["order_id"]

        str_status = ""
        cartData = []

        rs_order    = EngageboostOrdermaster.objects.filter(id=order_id).first()
        customer_id = rs_order.customer_id
        # Get User id and customer id from order id
        rs_customer = EngageboostCustomers.objects.filter(id = customer_id).first()
        user_id = rs_customer.auth_user_id

        if device_id is None and user_id is None:
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {
                "status":str_status,
                "msg":"User id or Device id is blank.",
                "data":[]
            }
        else:
            str_status = status.HTTP_200_OK
            
            # #  If Pay before create order

            # country_id = None
            # state_id = None
            # post_code = None
            # has_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
            # customer_id = has_customer.id
            # rs_address = EngageboostCustomersAddressBook.objects.filter(customers_id=user_id).first()
            # if rs_address:
            #     country_id = rs_address.delivery_country
            #     state_id = rs_address.delivery_state
            #     post_code = rs_address.delivery_postcode
            # cartData = discount.GetCartDetails(company_id,website_id,customer_id, device_id, None, country_id, state_id, post_code, user_id,None,coupon_code, warehouse_id)
            # cartData = cartData.data
            # if cartData and 'orderamountdetails' in cartData:
            #     if float(cartData['orderamountdetails'][0]['sub_total'])>0:
            #         cartData['orderamountdetails'][0]['sub_total'] = float(cartData['orderamountdetails'][0]['sub_total'])-float(loyalty_amount)
            #         cartData['orderamountdetails'][0]['balance_due'] = float(cartData['orderamountdetails'][0]['balance_due'])-float(loyalty_amount)
            #         cartData['orderamountdetails'][0]['applied_loyalty_amount'] = float(loyalty_amount)

            # Pay After create Order
            # rs_order    = EngageboostOrdermaster.objects.filter(id=order_id).first() 
            # customer_id = rs_order.customer_id
            # # Get User id and customer id from order id
            # rs_customer = EngageboostCustomers.objects.filter(id = customer_id).first()
            # user_id = rs_customer.auth_user_id

            if rs_order:
                order_data  = ViewOrderSerializer(rs_order)
                order_data  = order_data.data

                if order_data['shipment_id'] is not None and order_data['shipment_id']>0:
                    rs_shipment = EngageboostShipmentOrders.objects.filter(shipment=order_data['shipment_id']).first()
                    if rs_shipment:
                        shipment_status = rs_shipment.shipment_status  

                order_data['shipment_status'] = shipment_status
                credit_rs = EngageboostCreditPoint.objects.filter(isdeleted='n', isblocked='n', loyal_type="burn", website_id=website_id).last()
                order_data['rule_id'] = ''
                if credit_rs:
                    order_data['rule_id'] = credit_rs.id

                if float(order_data['net_amount'])>float(loyalty_amount):
                    order_data['net_amount'] = float(order_data['net_amount']) - float(loyalty_amount)
                    order_data['applied_loyalty_amount'] = float(loyalty_amount)
                else:
                    order_data['applied_loyalty_amount'] = 0

                data = {
                    "status":str_status,
                    "data":order_data
                }
            else:
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                    "status":str_status,
                    "msg":"No Order found.",
                    "data":[]
                }
        return Response(data)

def GetLoyaltyBalance(user_id , web_id = None):
    website_id = 1
    if web_id is not None:
        website_id = web_id

    loyelty = []
    customer_ids = []
    customer_ids.append(user_id)
    loyalty_data = []
    final_obj = {}
    return_data = {
        "minimum_order_amount": 0,
        "total_earn_amount": 0,
        "total_earn_points": 0,
        "total_burn_amount": 0,
        "total_burn_points": 0,
        "max_loyalty_amount_use_limit": 0,
        "loyalty_amount": 0,
        "loyalty_points":0,
        "remaning_earn_amount": 0,
        "remaning_earn_points": 0,
        "loyalty_end_date":"",
        "rule_id":0
    }
    return_loyalty = {
        'return_loyalty_valid_from': '25-05-2019',
        'return_loyalty_valid_to': '25-10-2019',
        'return_loyalty_amount': 0,
        'return_loyalty_points': 0
    }
    # customer_dtl = customer_detalils(customer_contact_no, website_id)
    # today = django.utils.timezone.now()
    now_utc = datetime.now(timezone('UTC')).astimezone(timezone('Asia/Dubai'))
    today      = now_utc.strftime('%Y-%m-%d')

    loyaltypoints_rs = EngageboostCustomerLoyaltypoints.objects.filter(customer_id=user_id, status="earn", expiry_date__date__gte=today).values('customer_id').all().annotate(total_earn_amount=Sum('amount'), total_earn_points=Sum('received_points'))
    
    burnloyaltypoints_rs = EngageboostCustomerLoyaltypoints.objects.filter(customer_id=user_id, status="burn").all()

    total_burnloyelty = 0
    total_burnloyelty_points = 0
    if burnloyaltypoints_rs:
        for burn in burnloyaltypoints_rs:
            total_burnloyelty += burn.amount
            total_burnloyelty_points += burn.burnt_points
        
    return_data.update({'total_burn_amount': total_burnloyelty})
    rule_id = 0
    total_earn_amount = 0
    total_earn_points = 0
    remaining_amount = 0
    remaining_burn_points = 0
    burn_rupee = 0
    if loyaltypoints_rs:
        # loyalty_data = EngageboostCustomerLoyaltypointsSerializer(loyaltypoints_rs, many=True).data
        for loyalty in loyaltypoints_rs:
            total_earn_amount += loyalty["total_earn_amount"]
            total_earn_points += loyalty["total_earn_points"]
        if total_earn_amount > total_burnloyelty:
            remaining_amount = int(total_earn_amount) - int(total_burnloyelty)
            remaining_burn_points = int(total_earn_points) - int(total_burnloyelty_points)
        return_data.update({'total_earn_amount': total_earn_amount})
        return_data.update({'total_earn_points': total_earn_points})
        return_data.update({'remaning_earn_amount': remaining_amount})
        return_data.update({'remaning_earn_points': remaining_burn_points})

        credit_rs = EngageboostCreditPoint.objects.filter(isdeleted='n', isblocked='n', loyal_type="burn", website_id=website_id).last()
        if credit_rs is not None:
            credit_data = EngageboostCreditPointSerializer(credit_rs).data 
            # print(json.dumps(credit_data))
            if credit_data:
                burn_rupee = 0
                if credit_data["per_rupees"] is not None:
                    if credit_data["per_rupees"] <= order_price:
                        point_rupees = int(order_price) / int(credit_data["per_rupees"])
                        burn_rupee = int(point_rupees) * int(credit_data["points"])
                        if total_burnloyelty < total_earn_amount:
                            burn_rupee = int(burn_rupee)
                        else:
                            burn_rupee = 0 

                        if burn_rupee >= credit_data["redeem_limit"]:
                            if remaining_amount < burn_rupee:
                                if remaining_amount < credit_data["redeem_limit"]:
                                    burn_rupee = remaining_amount
                                else:
                                    burn_rupee = credit_data["redeem_limit"]
                            else:
                                burn_rupee = credit_data["redeem_limit"]
                        
                    return_data.update({'loyalty_amount': burn_rupee})
                    return_data.update({'loyalty_points': credit_data["points"]})
                else:
                    return_data.update({'loyalty_amount': credit_data["points"]})
                    return_data.update({'loyalty_points': credit_data["points"]})

                return_data.update({'max_loyalty_amount_use_limit': credit_data["redeem_limit"]})
                return_data.update({'minimum_order_amount': credit_data["per_rupees"]})
                return_data.update({'loyalty_end_date': credit_data["loyal_end_date"]})
                return_data.update({'rule_id': credit_data["id"]})
    ###### Get All Return Loyalty Amount ######
    total_return_loyalty = 0
    total_return_loyalty_points = 0
    total_burnloyelty = 0
    total_burnloyelty_points = 0
    remaining_return_loyalty = 0
    remaining_return_loyalty_points = 0
    returnloyalty_rs = EngageboostCustomerLoyaltypoints.objects.filter(customer_id=user_id, status="return").values('customer_id').all().annotate(total_return_amount=Sum('amount'), total_earn_points=Sum('received_points'))
    ###### Get All Return Burn Loyalty Amount ######
    returnburnloyalty_rs = EngageboostCustomerLoyaltypoints.objects.filter(customer_id=user_id, status="returnburn").values('customer_id').all().annotate(total_return_burn_amount=Sum('amount'), total_burn_points=Sum('burnt_points'))
    if returnloyalty_rs:
        for returnloyalty in returnloyalty_rs:
                total_return_loyalty += returnloyalty["total_return_amount"]
                total_return_loyalty_points += returnloyalty["total_earn_points"]
    if returnburnloyalty_rs:
        for returnburnloyalty in returnburnloyalty_rs:
                total_burnloyelty += returnburnloyalty["total_return_burn_amount"]
                total_burnloyelty_points += returnburnloyalty["total_burn_points"]

    if total_return_loyalty > total_burnloyelty:       
        remaining_return_loyalty = float(total_return_loyalty) - float(total_burnloyelty)
    if total_return_loyalty_points > total_burnloyelty_points:
        remaining_return_loyalty_points = float(total_return_loyalty_points) - float(total_burnloyelty_points)
    return_loyalty.update({'return_loyalty_amount': remaining_return_loyalty})
    return_loyalty.update({'return_loyalty_points': remaining_return_loyalty_points})
    final_obj.update({'burn_loyalty':return_data, 'return_loyalty':return_loyalty})
    loyalty_data.append(final_obj)
    data ={
        'status':1,
        'message':'Success',
        'data':loyalty_data
        # 'data1':loyalty_points
    }
    print(data)
    return data


# EarnCreditPoints(636,22,1)

# END LOYALTY POINTS