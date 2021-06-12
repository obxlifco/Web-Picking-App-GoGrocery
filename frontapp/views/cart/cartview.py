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
from frontapp.views.cart import loyalty

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
import urllib
from urllib.parse import urlencode, quote_plus, urlparse


def get_company_website_id_by_url():
    website_id = 1
    return website_id

def get_max_order_unit():
    return 10
def warehouse_id_by_user_id(user_id,device_id):
    warehouse_id = 1
    return warehouse_id

def get_company_id_by_url():
    company_id = 1313
    return  company_id

class add_to_cart_old(APIView):
    def get_queryset(self):
        # print('Debug: I am starting...\n\n\n\n')
        # do a lot of things filtering data from Django models by some information on neo4j and saving data in the queryset...
        return self.queryset

    permission_classes = []
    def post(self, request, *args, **kwargs):

        website_id = get_company_website_id_by_url()
        company_id = get_company_id_by_url()
        warehouse_id           = request.META.get('HTTP_WAREHOUSE')
        data        = []
        returnData  = []
        cartData    = []
        user_id     = 0
        saved_amount = 0
        total_amount = 0
        total_cart_count    = 0

        requestdata = request.data
        user                = request.user
        user_id             = user.id
        device_id   = None
        customer_id = None
        product_id  = 0
        quantity    = 0
        if warehouse_id is None:
            if "warehouse_id" in requestdata:
                warehouse_id = requestdata["warehouse_id"]
            else:
                warehouse_id = 34

        if "device_id" in requestdata: device_id = requestdata['device_id']
        # if "customer_id" in requestdata: customer_id = requestdata['customer_id']
        if "product_id" in requestdata: product_id = requestdata['product_id']
        if "quantity" in requestdata: quantity = requestdata['quantity']
        if user_id is not None:
            rs_customer = EngageboostCustomers.objects.filter(auth_user_id = user_id).first()
            if rs_customer:
                customer_id = rs_customer.id

        # if device_id  and customer_id:
        if device_id:
            # product_count = EngageboostProducts.objects.filter(isdeleted='n', isblocked='n', status='n', default_price__gt=0, id=product_id).count()
            product_count = EngageboostProducts.objects.filter(isdeleted='n', isblocked='n', id=product_id).count()
            # print("product_count+++++++++++", product_count.query)
            if product_count <=0:
                status = 0
                ack = "fail"
                msg = "Product not available."
            else:
                if quantity>0:
                    dataProductAvailability = check_instock_quantity(product_id,quantity,warehouse_id,customer_id,device_id)
                    if dataProductAvailability['ack']:
                        cartCount = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id ).all()
                        # if customer_id and  customer_id is not None and customer_id>0:
                        if user_id and  user_id is not None and user_id>0:
                            cartCount = cartCount.filter(customer_id=user_id)
                        elif device_id:
                            # cartCount = cartCount.filter(customer_id=0, device_id=device_id)
                            cartCount = cartCount.filter(device_id=device_id, customer_id__isnull=True)
                        cartCount = cartCount.count()
                        if cartCount<=0:
                            if quantity<=0:
                                status = 0
                                ack = 'fail'
                                msg = 'provide quantity to be added.'
                            else:
                                cartArr = {}
                                cartArr.update({"website_id":website_id, "device_id":device_id, "product_id":product_id, "quantity":quantity})
                                if user_id and user_id is not None:
                                    cartArr.update({"customer_id":user_id})
                                insert_id = EngageboostTemporaryShoppingCarts.objects.create(**cartArr)
                                if insert_id.id>0:
                                    status = 1
                                    ack = 'success'
                                    msg = 'Product added to cart.'
                                else:
                                    status = 0
                                    ack = 'fail'
                                    msg = 'Product not added to cart.'
                        else:
                            if quantity>0:
                                cartArr = {}
                                if customer_id and customer_id is not None:
                                    # EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, device_id=device_id, customer_id=user_id, product_id=product_id).delete()
                                    # cartArr.update({"website_id":website_id, "device_id":device_id, "product_id":product_id, "quantity":quantity, "customer_id":user_id})
                                    # insert_id = EngageboostTemporaryShoppingCarts.objects.create(**cartArr)
                                    update_id = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, device_id=device_id, customer_id=user_id, product_id=product_id).update(quantity=quantity)
                                elif device_id:
                                    # EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, device_id=device_id, customer_id=user_id, product_id=product_id).delete()
                                    # cartArr.update({"website_id":website_id, "device_id":device_id, "product_id":product_id, "quantity":quantity})
                                    # insert_id = EngageboostTemporaryShoppingCarts.objects.create(**cartArr)

                                    update_id = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, device_id=device_id, product_id=product_id, customer_id__isnull=True).update(quantity=quantity)
                                status = 1
                                ack = 'success'
                                msg = 'Cart quantity updated.'
                            else:
                                if customer_id and customer_id>0:
                                    EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, customer_id=user_id ).delete()
                                elif device_id:
                                    EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, device_id=device_id,customer_id__isnull=True).delete()
                                status = 1
                                ack = 'success'
                                msg = 'Product deleted from cart.'
                    else:
                        status = 0
                        ack = 'fail'
                        msg = dataProductAvailability['msg']
                else:
                    cartCount = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id ).all()
                    if customer_id and customer_id>0:
                        cartCount = cartCount.filter(customer_id=user_id)
                    elif device_id:
                        cartCount = cartCount.filter(device_id=device_id, customer_id__isnull=True)
                    cartCount = cartCount.count()

                    if cartCount>0:
                        if customer_id and customer_id>0:
                            EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, customer_id=user_id ).delete()
                        elif device_id:
                            EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, device_id=device_id,customer_id__isnull=True).delete()
                        status = 1
                        ack = 'success'
                        msg = 'Product deleted from cart.'
                    else:
                        status = 0
                        ack = 'fail'
                        msg = "Quantity should not be 0."

        cart_data = discount.GetCartDetails(1,1,customer_id, device_id, None, None,None,None,user_id,None,None,warehouse_id,'addtocart')
        cartdata = cart_data.data
        # print("******************* cart data ******************")
        # print(cartdata)
        return_details = []
        if cart_data:
            cnt = 0
            for i in range(len(cartdata['cartdetails'])):
              if int(cartdata['cartdetails'][i]['id']) == int(product_id):
                  return_details.append(cartdata['cartdetails'][i])
        cartdata['cartdetails'] = return_details
        data = {
            "status":status,
            "ack":ack,
            "msg":msg,
            # "cart_data":cart_data.data
            "cart_data":cartdata
        }
        return Response(data)

def check_instock_quantity(product_id, qty, warehouse_id, user_id=None, device_id=None):
    data = []
    qty  = abs(qty)

    warehouse_id = warehouse_id
    if product_id and qty:
        max_order_unit = get_max_order_unit()
        rs_prod_qty = EngageboostProducts.objects.filter(id=product_id).first()
        prod_qty_data = ProductsViewNewSerializer(rs_prod_qty)

        if prod_qty_data['max_order_unit']:
            max_order_unit= prod_qty_data['max_order_unit']
        default_price = 1
        max_order_unit = 100
        if default_price>0:
            if max_order_unit >= qty:
                product_quantity = product_stock_count(product_id,warehouse_id);
                # product_quantity = 10
                if int(product_quantity) > 0:
                    if int(qty) <= int(product_quantity):
                        ack=1
                        msg="available"
                    else:
                        ack = 0
                        msg = "Only "+ str(product_quantity) + " qty of this product is available."
                else:
                    ack=0
                    msg="out of stock"
                    # if user_id is not None:
                    # 	EngageboostTemporaryShoppingCarts.objects.filter(product_id=product_id, customer_id = user_id).delete()
                    # if user_id is not None:
                    # 	EngageboostTemporaryShoppingCarts.objects.filter(product_id=product_id, device_id = device_id).delete()
            else:
                ack=0
                msg="You can purchase only "+ str(max_order_unit) +" qty of this product."
        else:
            ack=0
            msg="Not Available."
    data = {
        "ack":ack,
        "status":ack,
        "msg":msg
    }
    return data

def get_max_order_unit():
    max_order_unit = 10
    return max_order_unit

def product_stock_count(product_id, warehouse_id=None):
    product_quantity    = 0
    website_id          = get_company_website_id_by_url()
    if warehouse_id:
        pass
    else:
        warehouse_id = get_default_warehouse_id()
    if product_id:
        stock_data = EngageboostProductStocks.objects.filter(warehouse_id=warehouse_id, product_id=product_id).values('real_stock').first()
        if stock_data:
            product_quantity = stock_data['real_stock']
        return product_quantity

def get_default_warehouse_id():
    warehouse_id = 5
    return warehouse_id

class remove_cart(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        requestdata = request.data
        user                = request.user
        user_id             = user.id
        # customer_id = user_id
        customer_id = None
        if user_id is not None:
            rs_customer = EngageboostCustomers.objects.filter(auth_user_id = user_id).first()
            if rs_customer:
                # customer_id = rs_customer.id
                customer_id = user_id

        company_id = 1

        str_status = ""
        try:
            if requestdata['product_id']:
                product_id = requestdata['product_id']
            else:
                product_id = ""
        except KeyError:
            product_id = ""

        try:
            if requestdata['website_id']:
                website_id = requestdata['website_id']
            else:
                website_id = None
        except KeyError:
            website_id = None

        try:
            if requestdata['device_id']:
                device_id = requestdata['device_id']
            else:
                device_id = None
        except KeyError:
            device_id = None


        try:
            if requestdata['warehouse_id']:
                warehouse_id = requestdata['warehouse_id']
            else:
                warehouse_id = None
        except KeyError:
            warehouse_id = None
        
        if warehouse_id is None:
            warehouse_id           = request.META.get('HTTP_WAREHOUSE')
            
        # customer_id = None
        # if user_id is not None:
        #     rs_customer = EngageboostCustomers.objects.filter(auth_user_id = user_id).first()
        #     if rs_customer:
        #         customer_id = rs_customer.id

        # if user_id is not None:
        #     customer_id = user_id
        # else:
        #     customer_id = None

        if product_id:
            cart_data = RemoveFromCart(product_id, website_id, customer_id, device_id)
            str_status = cart_data['str_status']
            data = {
                "status":str_status,
                "msg":cart_data['msg']
            }
        else:
            str_status = status.HTTP_400_BAD_REQUEST
            data = {
                "status":str_status,
                "msg":"Provide Product_id."
            }

        disc_pro = discount.GetCartDetails( company_id,website_id,customer_id, device_id, None, None,None,None,user_id,None,None,warehouse_id)

        data.update({"data":disc_pro.data})
        return Response(data, str_status)

def RemoveFromCart(product_id, website_id, customer_id=None, device_id=None):
    str_status = ""
    msg = ""
    if customer_id and customer_id>0:
        EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, customer_id=customer_id ).delete()
        str_status = status.HTTP_200_OK
        msg = "success"
    elif device_id:
        EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id,device_id=device_id,customer_id__isnull=True).delete()
        str_status = status.HTTP_200_OK
        msg = "success"
    else:
        str_status = status.HTTP_400_BAD_REQUEST
        msg = "Provide Customer Id or Device Id."
    data = {"str_status":str_status, "msg":msg}
    return data

class empty_cart(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        requestdata = request.data
        user = request.user
        user_id = user.id
        customer_id = user_id
        str_status = ""
        try:
            if requestdata['website_id']:
                website_id = requestdata['website_id']
            else:
                website_id = 1
        except KeyError:
            website_id = 1

        try:
            if requestdata['device_id']:
                device_id = requestdata['device_id']
            else:
                device_id = None
        except KeyError:
            device_id = None

        # try:
        #     if requestdata['customer_id']:
        #         customer_id = requestdata['customer_id']
        #     else:
        #         customer_id = None
        # except KeyError:
        #     customer_id = None

        str_status  = ""
        msg         = ""
        if customer_id and customer_id>0:
            EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, customer_id=customer_id ).delete()
            str_status = status.HTTP_200_OK
            msg = "success"
        elif device_id:
            EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, device_id=device_id,customer_id__isnull=True).delete()
            str_status = status.HTTP_200_OK
            msg = "success"
        else:
            str_status = status.HTTP_400_BAD_REQUEST
            msg = "Provide Customer Id or Device Id."
        data = {"status":str_status, "msg":msg}

        return Response(data, str_status)

class Viewcart(APIView):
    permission_classes = []
    def get(self, request, format=None):

        requestdata = request.data
        user                = request.user
        user_id             = user.id
        device_id           = request.META.get('HTTP_DEVICEID')
        warehouse_id           = request.META.get('HTTP_WAREHOUSE')
        customer_id         = user_id
        website_id          = get_company_website_id_by_url()
        company_id          = get_company_id_by_url()

        saved_amount        = 0
        total_amount        = 0
        total_cart_count    = 0
        returnArray         = []
        data                = []
        cartData            = []

        str_status  = ""
        # customer_id = None
        # device_id   = None

        # if "user_id" in requestdata:
        #     customer_id = requestdata['user_id']
        # if "device_id" in requestdata:
        #     device_id = requestdata['device_id']

        if customer_id is None and device_id is None:
            str_status = status.HTTP_400_BAD_REQUEST
            msg     = 'provide user id or device id.'
        else:
            cartData = get_cart_view(device_id,customer_id, warehouse_id)

            total_cart_count    = cartData['cart_count']
            saved_amount        = cartData['saved_amount']
            total_amount        = cartData['total_amount']
            returnArray         = cartData['cart_details']
            cart_count_itemwise = cartData['cart_count_itemwise']
            stock_message       = cartData['stock_message']
            if int(total_cart_count)>0:
                str_status = status.HTTP_200_OK
                msg = "Success"
            else:
                str_status = status.HTTP_204_NO_CONTENT
                msg = 'Cart is empty'

        # Check Minimum Order Amount
            minimum_order_amount = 0
            minimum_order_amount_check = 'yes'

            rs_min_order = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).first()
            if float(rs_min_order.min_order_amount)>0:
                minimum_order_amount = float(rs_min_order.min_order_amount)
            else:
                rs_global_settings = EngageboostGlobalSettings.objects.filter(isblocked='n', isdeleted='n', website_id= website_id).first()
                if rs_global_settings and float(rs_global_settings.min_order_amount)>0:
                    minimum_order_amount = float(rs_global_settings.min_order_amount)

            if float(total_amount)<float(minimum_order_amount):
                minimum_order_amount_check = 'no'

            # warehouse_zone = EngageboostZoneMasters.objects.filter(warehouse_id=warehouse_id, isdeleted='n',
            #                                                        isblocked='n').first()
            # if warehouse_zone:
            #     # ------Binayak Start 13-01-2021-----#
            #     country_id = warehouse_zone.country_id
            #     state_id = warehouse_zone.state_id
            #     post_code = warehouse_zone.zipcode
            #     # shipping_master = EngageboostShippingMastersSettings.objects.filter(zone_id=warehouse_zone.id, isdeleted='n', isblocked='n').first()
            #     # shipping_master = EngageboostShippingMastersSettings.objects.filter(zone_id__null=False, isdeleted='n', isblocked='n')
            #     shipping_rate_flat = discount.rate_flat('1', company_id, country_id, state_id, post_code, 'front',
            #                                             warehouse_id, warehouse_id)
            #     # ------Binayak End 13-01-2021-----#
            #     # print('shipping_rate_flat===>', shipping_rate_flat)
            #     # if shipping_master:
            #     #     shipping_amount = shipping_master.flat_price
            #     if shipping_rate_flat:
            #         shipping_amount = shipping_rate_flat['flat_price']
            #     else:
            #         GlobalSettings_qs = EngageboostGlobalSettings.objects.filter(isblocked='n',
            #                                                                      isdeleted='n').first()
            #         shipping_amount = GlobalSettings_qs.shipping_charge
            # else:
            #     GlobalSettings_qs = EngageboostGlobalSettings.objects.filter(isblocked='n',
            #                                                                  isdeleted='n').first()
            #     shipping_amount = GlobalSettings_qs.shipping_charge


        data = {
            "status":str_status,
            "msg":msg,
            "cart_count":total_cart_count,
            "cart_count_itemwise":cart_count_itemwise,
            "saved_amount":saved_amount,
            "total_amount":total_amount,
            "stock_message":stock_message,
            "data":returnArray,
            "minimum_order_amount":minimum_order_amount,
            "minimum_order_amount_check":minimum_order_amount_check
        }
        return Response(data, str_status)

#---Test---#
class ViewcartTest(APIView):
    permission_classes = []
    def get(self, request, format=None):

        requestdata = request.data
        user                = request.user
        user_id             = user.id
        device_id           = request.META.get('HTTP_DEVICEID')
        warehouse_id           = request.META.get('HTTP_WAREHOUSE')
        customer_id         = user_id
        website_id          = get_company_website_id_by_url()
        company_id          = get_company_id_by_url()

        saved_amount        = 0
        total_amount        = 0
        total_cart_count    = 0
        returnArray         = []
        data                = []
        cartData            = []

        str_status  = ""
        # customer_id = None
        # device_id   = None

        # if "user_id" in requestdata:
        #     customer_id = requestdata['user_id']
        # if "device_id" in requestdata:
        #     device_id = requestdata['device_id']

        if customer_id is None and device_id is None:
            str_status = status.HTTP_400_BAD_REQUEST
            msg     = 'provide user id or device id.'
        else:
            cartData = get_cart_view(device_id,customer_id, warehouse_id)

            total_cart_count    = cartData['cart_count']
            saved_amount        = cartData['saved_amount']
            total_amount        = cartData['total_amount']
            returnArray         = cartData['cart_details']
            cart_count_itemwise = cartData['cart_count_itemwise']
            stock_message       = cartData['stock_message']
            if int(total_cart_count)>0:
                str_status = status.HTTP_200_OK
                msg = "Success"
            else:
                # str_status = status.HTTP_204_NO_CONTENT
                str_status = status.HTTP_200_OK
                msg = 'Cart is empty'

        # Check Minimum Order Amount
            minimum_order_amount = 0
            minimum_order_amount_check = 'yes'

            rs_min_order = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).first()
            if rs_min_order:
                if float(rs_min_order.min_order_amount)>0:
                    minimum_order_amount = float(rs_min_order.min_order_amount)
                else:
                    rs_global_settings = EngageboostGlobalSettings.objects.filter(isblocked='n', isdeleted='n',
                                                                                  website_id=website_id).first()
                    if rs_global_settings and float(rs_global_settings.min_order_amount) > 0:
                        minimum_order_amount = float(rs_global_settings.min_order_amount)
            else:
                rs_global_settings = EngageboostGlobalSettings.objects.filter(isblocked='n', isdeleted='n', website_id= website_id).first()
                if rs_global_settings and float(rs_global_settings.min_order_amount)>0:
                    minimum_order_amount = float(rs_global_settings.min_order_amount)

            if float(total_amount)<float(minimum_order_amount):
                minimum_order_amount_check = 'no'

            #------Binayak Start 11-12-2020------#

            shipping_amount = 0

            # customer_details = EngageboostCustomers.objects.filter(auth_user=customer_id).first()
            # if customer_details and total_cart_count>0:
            #
            #     rs_address = EngageboostCustomersAddressBook.objects.filter(customers_id=customer_details.id,
            #                                                                     set_primary=1).first()
            #
            #
            #     if rs_address:
            #         country_id = rs_address.delivery_country
            #         state_id = rs_address.delivery_state
            #         post_code = rs_address.delivery_postcode
            #
            #         shipping_rate_flat = discount.rate_flat('1',company_id,country_id,state_id,post_code,'front',warehouse_id, None)
                    # print('shipping_rate_flat======>', shipping_rate_flat)


                    # shipping_amount = shipping_rate_flat['flat_price']

                # else:
            warehouse_zone = EngageboostZoneMasters.objects.filter(warehouse_id=warehouse_id, isdeleted='n', isblocked='n').first()
            if warehouse_zone:
                country_id = warehouse_zone.country_id
                state_id = warehouse_zone.state_id
                post_code = warehouse_zone.zipcode
                # shipping_master = EngageboostShippingMastersSettings.objects.filter(zone_id=warehouse_zone.id, isdeleted='n', isblocked='n').first()
                # shipping_master = EngageboostShippingMastersSettings.objects.filter(zone_id__null=False, isdeleted='n', isblocked='n')
                shipping_rate_flat = discount.rate_flat('1', company_id, country_id, state_id, post_code, 'front',
                                                        warehouse_id, warehouse_id)
                # shipping_master = EngageboostShippingMastersSettings.objects.filter(zone_id=warehouse_zone.id, isdeleted='n', isblocked='n').first()
                # shipping_master = EngageboostShippingMastersSettings.objects.filter(zone_id__null=False, isdeleted='n', isblocked='n')
                # shipping_rate_flat = discount.rate_flat('1', company_id, '', '', '', 'front',
                #                                         warehouse_id, warehouse_id)
                # print('shipping_rate_flat===>', shipping_rate_flat)
                # if shipping_master:
                #     shipping_amount = shipping_master.flat_price
                if shipping_rate_flat:
                    shipping_amount = shipping_rate_flat['flat_price']
                else:
                    GlobalSettings_qs = EngageboostGlobalSettings.objects.filter(isblocked='n',
                                                                                 isdeleted='n').first()
                    shipping_amount = GlobalSettings_qs.shipping_charge
            else:
                GlobalSettings_qs = EngageboostGlobalSettings.objects.filter(isblocked='n',
                                                                             isdeleted='n').first()
                shipping_amount = GlobalSettings_qs.shipping_charge

        data = {
            "status":str_status,
            "msg":msg,
            "cart_count":total_cart_count,
            "cart_count_itemwise":cart_count_itemwise,
            "saved_amount":saved_amount,
            "total_amount":total_amount,
            "stock_message":stock_message,
            "data":returnArray,
            "minimum_order_amount":minimum_order_amount,
            "minimum_order_amount_check":minimum_order_amount_check,
            "shipping_amount":shipping_amount,
            "final_amount":float(total_amount) + float(shipping_amount)
        }

        # ------Binayak End 11-12-2020------#
        return Response(data, str_status)
#---Test---#

def get_cart_view(device_id=None, user_id=None, warehouse_id=None):
    website_id = get_company_website_id_by_url()
    # company_id = get_company_id_by_url()
    returnArray     = []
    saved_amount    = 0
    total_amount    = 0
    cart_count      = 0
    counter         = 0
    cart_count_itemwise = 0
    warehouse_id = warehouse_id
    if warehouse_id is None:
        warehouse_id = 2
    rs_cart = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id).order_by("id")
    if user_id and user_id>0:
        rs_cart = rs_cart.filter(customer_id=user_id)
    elif device_id and device_id is not None:
        rs_cart = rs_cart.filter(device_id=device_id).exclude(customer_id__isnull=False)

    # Remove Duplicate
    for row in rs_cart.all():
        if rs_cart.filter(product_id=row.product_id).count() > 1:
            row.delete()
    # End Remove Duplicate
    cart_count = rs_cart.count()
    cart_data = []
    return_cart_data = []
    stock_message = ""
    if cart_count>0:
        rs_cart = rs_cart.all()
        cart_data = EngageboostTemporaryShoppingCartsSerializer(rs_cart, context={'warehouse_id': warehouse_id}, many=True)
        # ProductCategoriesSerializer(product_ids, context={'warehouse_id': warehouse_id}, many=True)
        cart_data = cart_data.data
        saved_amount = 0
        total_amount = 0
        if rs_cart:
            for cartvalue in  cart_data:
                if float(cartvalue['product_id']['stock']["stock_value"])>0:
                    pass
                else:
                    stock_message = "Some product(s) are out of stock. Please remove or change those product to continue checkout process."

                if cartvalue['product_id']['channel_price'] >0:
                    cart_count_itemwise = cart_count_itemwise + int(cartvalue['quantity'])
                    cartvalue['product_id']['default_price'] = cartvalue['product_id']['channel_price']
                    cartvalue['original_price'] = cartvalue['product_id']['channel_price']
                    cartvalue['product_price'] = cartvalue['product_id']['channel_price']
                    request_data = {
                        'website_id': website_id,
                        'company_id': website_id,
                        'product_ids': cartvalue['product_id']['id'],
                        'qtys': cartvalue['quantity'],
                        'prod_price': cartvalue['product_id']['channel_price'],
                        'warehouse_id': warehouse_id
                    }
                    productsdiscount = discount.get_discount_detalils(request_data)

                    # field_name="'size'";
                    # primary_category_id = $ContentManagements->category_ids_from_product_ids($product_id);
                    # customfield=$this->get_custom_fields_var($primary_category_id, $product_id,6,1,'','', $field_name);
                    # variant_name=$customfield[0]['MarketplaceFieldValue']['value'];
                    cartvalue['product_name']    = cartvalue['product_id']['name']
                    cartvalue['product_sku']    = cartvalue['product_id']['sku']
                    cartvalue['product_slug']    = cartvalue['product_id']['slug']
                    cartvalue['original_price']  = cartvalue['product_id']['channel_price']
                    cartvalue['product_price']  = cartvalue['product_id']['channel_price']
                    cartvalue['new_default_price']       = productsdiscount[0]['new_default_price']
                    cartvalue['new_default_price_unit']  = productsdiscount[0]['new_default_price_unit']
                    cartvalue['discount_price_unit']     = productsdiscount[0]['discount_price_unit']
                    cartvalue['discount_price']          = productsdiscount[0]['discount_price']
                    cartvalue['discount_amount']         = productsdiscount[0]['discount_amount']
                    cartvalue['disc_type']               = productsdiscount[0]['disc_type']
                    cartvalue['coupon']                  = productsdiscount[0]['coupon']

                    cartvalue['veg_nonveg_type'] = cartvalue['veg_nonveg_type']
                    cartvalue['default_price']   = cartvalue['product_id']['channel_price']

                    cartvalue['unit'] = common.get_unit(cartvalue['product_id']['id'])
                    cartvalue['weight'] = cartvalue['weight']

                    # discount_price=$original_price-$selling_price;
                    saved_amount = float(saved_amount) + float(productsdiscount[0]['discount_price'])
                    total_amount = float(total_amount) + float(productsdiscount[0]['new_default_price'])
                    return_cart_data.append(cartvalue)
                else:
                    EngageboostTemporaryShoppingCarts.objects.filter(id=cartvalue['id']).delete()
    data = {
        "cart_details":return_cart_data,
        "cart_count":cart_count,
        "cart_count_itemwise":cart_count_itemwise,
        "total_amount":total_amount,
        "saved_amount":saved_amount,
        "stock_message":stock_message
    }
    return data

class get_delivery_slot(APIView):
    permission_classes = []
    def get(self, request,zone_id, format=None):
        # zone_id = self.request.GET.get("zone_id")
        returndata = GetDeliverySlot(zone_id)
        str_status = ""
        if int(returndata['status'])==1:
            str_status = status.HTTP_200_OK
            data = {
                "status":status.HTTP_200_OK,
                "data":returndata['delivery_slot']
            }
        else:
            str_status = status.HTTP_204_NO_CONTENT
            data = {
                "status":status.HTTP_204_NO_CONTENT,
                "data":[]
            }
        return Response(returndata,str_status)

def GetDeliverySlot(zone_id):
    # now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
    now_utc = datetime.now(timezone('UTC')).astimezone(timezone('Asia/Dubai'))
    days_arr = ['NA','sun','mon', 'tue', 'wed', 'thu', 'fri','sat']
    # now_utc = now_utc+ timedelta(hours=4)
    data            = []
    DeliverySlot    = []
    dataTimeslot    = []
    newTimeSlot     = []
    warehouse_id    = zone_id
    if warehouse_id and int(warehouse_id)<=0:
        returndata = {
            "status":0,
            "ack":"fail",
            "msg":"Warehouse not available"
        }
    else:
        next_day_arr = []
        for x in range(1):
            # now 	= datetime.now()
            # now = now + timedelta(hours=4)
            today 	= now_utc.date()
            new_date = ''
            new_date = now_utc + timedelta(days=x)
            next_day_arr.append(new_date)

        # today_id = today.weekday()
        today_name = today.strftime("%a")
        today_name = today_name.lower()
        today_id = days_arr.index(today_name)
        nextday_id = today_id+1
        if today_id>=7:
            nextday_id = 1

        rs_data     = EngageboostDeliverySlot.objects.filter(isdeleted='n', isblocked='n', warehouse_id=warehouse_id, day_id__in=[today_id, nextday_id]).order_by('day_id','start_time').all().order_by('day_id')
        slot_data 	= DeliverySlotSerializer(rs_data, many=True)
        DeliverySlot = []
        current_time = datetime.now().strftime('%H:%M:%S')
        to_day      = datetime.now().strftime('%Y-%m-%d')
        order_data  = EngageboostOrdermaster.objects.filter(time_slot_date__gte=to_day,buy_status = 1).exclude(order_status=2).all().values('time_slot_date','slot_start_time').order_by('time_slot_date','slot_start_time').annotate(total=Count('time_slot_date'))

        flag = 0

        current_time = now_utc.strftime('%H:%M')
        # str_current_time_arr = str(current_time).split(":")
        # str_current_time = str_current_time_arr[0]

        for dayarr in next_day_arr:
            dtarr   = dayarr.strftime('%Y-%m-%d')
            dt      = dayarr
            # day_id  = dt.weekday()
            day_name = dayarr.strftime("%a")
            day_name = day_name.lower()
            day_id = days_arr.index(day_name)
            temp_arr = {}
            next_arr = {}
            next_list = []
            # templist = []
            temp_list2 = {}
            # day_id = day_id+2
            # print("day_id",day_id)


            # ========checking for same day delivery=========#
            is_today_deliverable = rs_data.filter(day_id=today_id, based_on='SameDay').first()
            if is_today_deliverable:
                # print("======in here 1===========")
                # str_cutoff_time_arr = str(is_today_deliverable.cutoff_time).split(":")
                # str_cutoff_time = str_cutoff_time_arr[0]
                str_cutoff_time = datetime.strptime(is_today_deliverable.cutoff_time, '%H:%M').strftime('%H:%M')
                # print("======str_cutoff_time========", str_cutoff_time)
                # print("======str_current_time========", str_current_time)
                if str_cutoff_time > current_time:
                    print("======in here 2===========")
                    for slotdata in slot_data.data:
                        templist = []
                        if slotdata['id'] == is_today_deliverable.id:
                            print("======in here 4===========", is_today_deliverable.id)
                            slotdata.update({"is_active": "Yes"})
                            # slotdata["based_on"] = "SameDay"
                            templist.append(slotdata)
                            temp_list2.update({"delivery_date": dtarr})
                            temp_arr.update({"delivery_date": dtarr, "available_slot": templist})
                            DeliverySlot.append(temp_arr)
                else:
                    # print("======in here 3===========")
                    pass
            # print("========DeliverySlot===1======", DeliverySlot)

            next_day_deliverable = rs_data.filter(day_id=today_id, based_on='NextDay').first()
            if next_day_deliverable:
                # ========checking for next day delivery=========#
                for slotdata in slot_data.data:
                    templist = []
                    temp_arr = {}
                    if slotdata['id'] == next_day_deliverable.id:
                        # print("======in here 5===========", next_day_deliverable.id)
                        delivery_date = dayarr + timedelta(days=1)
                        delivery_date = delivery_date.strftime('%Y-%m-%d')
                        slotdata.update({"is_active": "Yes"})
                        # slotdata["based_on"] = "SameDay"
                        templist.append(slotdata)
                        temp_list2.update({"delivery_date": delivery_date})
                        temp_arr.update({"delivery_date": delivery_date, "available_slot": templist})
                        DeliverySlot.append(temp_arr)

            # else:
            #     for slotdata in slot_data.data:
            #         templist = []
            #         if slotdata['day_id'] == day_id:
            #             # +++++++++++++++++++++
            #             date_format = "%Y-%m-%d"
            #             current_time = now_utc.strftime('%H:%M')
            #             str_current_time_arr = str(current_time).split(":")
            #             str_current_time = str_current_time_arr[0]
            #             time_format = "%H:%M"
            #             # cutoff_time = time.strptime(str(slotdata['cutoff_time']), time_format)
            #
            #             str_cutoff_time_arr = str(slotdata['cutoff_time']).split(":")
            #             str_cutoff_time = str_cutoff_time_arr[0]
            #             # print("str_cutoff_time", str_cutoff_time)
            #             # print("str_current_time", str_current_time)
            #             # print("day_id", day_id)
            #
            #             if int(str_cutoff_time) > int(str_current_time):
            #                 slotdata.update({"is_active":"Yes"})
            #                 slotdata["based_on"]="SameDay"
            #                 templist.append(slotdata)
            #                 temp_list2.update({"delivery_date":dtarr})
            #                 temp_arr.update({"delivery_date":dtarr, "available_slot":templist})
            #                 DeliverySlot.append(temp_arr)
            #             else:
            #                 if flag>0:
            #                     pass
            #                 else:
            #                     flag = 1
            #                     slotdata.update({"is_active":"Yes"})
            #                     slotdata["based_on"]="Nextday"
            #                     dt_arr = new_date = now_utc + timedelta(days=1)
            #                     dt_arr = dt_arr.strftime('%Y-%m-%d')
            #                     templist.append(slotdata)
            #                     next_arr.update({"delivery_date":dt_arr, "available_slot":templist})
            #                     DeliverySlot.append(next_arr)
            #             # +++++++++++++++++++++
            #         else:
            #             if flag > 0:
            #                 pass
            #             else:
            #                 flag = 1
            #                 dt_arr = new_date = now_utc + timedelta(days=1)
            #                 dt_arr = dt_arr.strftime('%Y-%m-%d')
            #                 slotdata.update({"is_active":"Yes"})
            #                 slotdata["based_on"]="Nextday"
            #                 templist.append(slotdata)
            #                 next_arr.update({"delivery_date":dt_arr, "available_slot":templist})
            #                 DeliverySlot.append(next_arr)
        DeliverySlot.sort(key=lambda x: x['delivery_date'].lower())
        returndata = {
            "status":1,
            "delivery_slot":DeliverySlot
        }
    return returndata

def GetDeliverySlot_XX(zone_id):
    # now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
    now_utc = datetime.now(timezone.utc).astimezone()
    data            = []
    DeliverySlot    = []
    dataTimeslot    = []
    newTimeSlot     = []
    warehouse_id    = zone_id
    if warehouse_id and int(warehouse_id)<=0:
        returndata = {
            "status":0,
            "ack":"fail",
            "msg":"Warehouse not available"
        }
    else:
        next_day_arr = []
        for x in range(2):
            now 	= datetime.now()
            today 	= now.date()
            new_date = ''
            new_date = now_utc + timedelta(days=x)
            next_day_arr.append(new_date)

        rs_data     = EngageboostDeliverySlot.objects.filter(isdeleted='n', isblocked='n', warehouse_id=warehouse_id).order_by('day_id','start_time').all()
        slot_data 	= DeliverySlotSerializer(rs_data, many=True)
        DeliverySlot = []
        current_time = datetime.now().strftime('%H:%M:%S')
        to_day      = datetime.now().strftime('%Y-%m-%d')
        order_data  = EngageboostOrdermaster.objects.filter(time_slot_date__gte=to_day,buy_status = 1).exclude(order_status=2).all().values('time_slot_date','slot_start_time').order_by('time_slot_date','slot_start_time').annotate(total=Count('slot_start_time'))
        for dayarr in next_day_arr:
            dtarr   = dayarr.strftime('%Y-%m-%d')
            dt      = dayarr
            day_id  = dt.weekday()
            temp_arr = {}
            templist = []
            temp_list2 = {}
            day_id = day_id+1
            for slotdata in slot_data.data:
                if slotdata['day_id'] == day_id:
                    # templist.append(slotdata)
                    # +++++++++++++++++++++
                    flag = 0
                    for date_dict in order_data:
                        if str(date_dict['time_slot_date']) == str(dtarr):
                            flag = 1
                            if str(date_dict['slot_start_time'])==str(slotdata['start_time']):
                                if int(date_dict['total'])>=slotdata['order_qty_per_slot']:  # Check Order Limit
                                    slotdata.update({"is_active":"No"})
                                    templist.append(slotdata)
                                else:
                                    day_diff = 0
                                    if slotdata['based_on']=="NextDay":
                                        day_diff = 1
                                    # cutoff_date = date_dict['time_slot_date'] - timedelta(days=day_diff)
                                    cutoff_date = date_dict['time_slot_date'] + timedelta(days=day_diff)
                                    date_format = "%Y-%m-%d"
                                    check_today = datetime.strptime(str(to_day), date_format)
                                    check_cutoff = datetime.strptime(str(cutoff_date), date_format)
                                    date_delta = check_cutoff - check_today
                                    date_delta_days = date_delta.days
                                    # if to_day > check_cutoff:
                                    if date_delta_days>0:
                                        slotdata.update({"is_active":"No"})
                                        templist.append(slotdata)
                                    # elif date_delta_days == 0:
                                    elif to_day == check_cutoff:
                                        current_time = datetime.now().strftime('%H:%M:%S')
                                        time_format = "%H:%M:%S"
                                        cutoff_time = datetime.strptime(str(slotdata['cutoff_time']), date_format)
                                        slotdata.update({"is_active":"Yes"})
                                        templist.append(slotdata)
                            else:
                                slotdata.update({"is_active":"Yes"})
                                templist.append(slotdata)
                        else:
                            pass
                    if flag == 0:
                        slotdata.update({"is_active":"Yes"})
                        templist.append(slotdata)
                    # +++++++++++++++++++++
            temp_list2.update({"delivery_date":dtarr})
            temp_arr.update({"delivery_date":dtarr, "available_slot":templist})
            DeliverySlot.append(temp_arr)
        returndata = {
            "status":1,
            "delivery_slot":DeliverySlot
        }
    return returndata

def GetDeliverySlot_old(zone_id):
    # now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
    now_utc = datetime.now(timezone.utc).astimezone()
    data            = []
    DeliverySlot    = []
    dataTimeslot    = []
    newTimeSlot     = []
    warehouse_id    = zone_id
    if warehouse_id and int(warehouse_id)<=0:
        returndata = {
            "status":0,
            "ack":"fail",
            "msg":"Warehouse not available"
        }
    else:
        next_day_arr = []
        for x in range(2):
            now 	= datetime.now()
            today 	= now.date()
            new_date = ''
            new_date = now_utc + timedelta(days=x)
            next_day_arr.append(new_date)

        rs_data     = EngageboostDeliverySlot.objects.filter(isdeleted='n', isblocked='n', warehouse_id=warehouse_id).order_by('day_id','start_time').all()
        slot_data 	= DeliverySlotSerializer(rs_data, many=True)
        DeliverySlot = []
        current_time = datetime.now().strftime('%H:%M:%S')
        to_day      = datetime.now().strftime('%Y-%m-%d')
        order_data  = EngageboostOrdermaster.objects.filter(time_slot_date__gte=to_day,buy_status = 1).exclude(order_status=2).all().values('time_slot_date','slot_start_time').order_by('time_slot_date','slot_start_time').annotate(total=Count('slot_start_time'))
        for dayarr in next_day_arr:
            dtarr   = dayarr.strftime('%Y-%m-%d')
            dt      = dayarr
            day_id  = dt.weekday()
            temp_arr = {}
            templist = []
            temp_list2 = {}
            day_id = day_id+1
            for slotdata in slot_data.data:
                if slotdata['day_id'] == day_id:
                    # templist.append(slotdata)
                    # +++++++++++++++++++++
                    flag = 0
                    for date_dict in order_data:
                        if str(date_dict['time_slot_date']) == str(dtarr):
                            flag = 1
                            if str(date_dict['slot_start_time'])==str(slotdata['start_time']):
                                if int(date_dict['total'])>=slotdata['order_qty_per_slot']:  # Check Order Limit
                                    slotdata.update({"is_active":"No"})
                                    templist.append(slotdata)
                                else:
                                    # slotdata.update({"is_active":"Yes"})
                                    # templist.append(slotdata)
                                    day_diff = 0
                                    if slotdata['based_on']=="NextDay":
                                        day_diff = 1
                                    # cutoff_date = date_dict['time_slot_date'] - timedelta(days=day_diff)
                                    cutoff_date = date_dict['time_slot_date'] + timedelta(days=day_diff)
                                    date_format = "%Y-%m-%d"
                                    check_today = datetime.strptime(str(to_day), date_format)
                                    check_cutoff = datetime.strptime(str(cutoff_date), date_format)
                                    date_delta = check_cutoff - check_today
                                    date_delta_days = date_delta.days
                                    # if to_day > check_cutoff:
                                    if date_delta_days>0:
                                        slotdata.update({"is_active":"No"})
                                        templist.append(slotdata)
                                    # elif date_delta_days == 0:
                                    elif to_day == check_cutoff:
                                        current_time = datetime.now().strftime('%H:%M:%S')
                                        time_format = "%H:%M:%S"
                                        cutoff_time = datetime.strptime(str(slotdata['cutoff_time']), date_format)
                                        slotdata.update({"is_active":"Yes"})
                                        templist.append(slotdata)
                            else:
                                slotdata.update({"is_active":"Yes"})
                                templist.append(slotdata)
                        else:
                            pass
                    if flag == 0:
                        slotdata.update({"is_active":"Yes"})
                        templist.append(slotdata)
                    # +++++++++++++++++++++
            temp_list2.update({"delivery_date":dtarr})
            temp_arr.update({"delivery_date":dtarr, "available_slot":templist})
            DeliverySlot.append(temp_arr)
        returndata = {
            "status":1,
            "delivery_slot":DeliverySlot
        }
    return returndata

# class SaveCart(APIView):
#     def post(self, request, format=None):
#         # now_utc = datetime.now(timezone.utc).astimezone()
#         now_utc = datetime.now(timezone('UTC')).astimezone(timezone('Asia/Dubai'))
#         shipping_label_content = ""
#         #  *************  Get Base currency
#         base_currency = "AED"
#         try:
#             postdata                = request.data
#             user                = request.user
#             user_id             = user.id
#             device_id 				= postdata['device_id']
#             # user_id 				= postdata['user_id']
#             address_book_id 		= postdata['address_book_id']
#             time_slot_date 		    = postdata['time_slot_date']
#             time_slot_time 		    = postdata['time_slot_time']
#             # special_instruction 	= postdata['special_instruction']
#             coupon_code 			= postdata['coupon_code']
#             webshop_id 				= 6
#             if "webshop_id" in postdata:
#                 webshop_id = postdata['webshop_id']
#             special_instruction = None
#             if "special_instruction" in postdata:
#                 special_instruction = postdata['special_instruction']
#
#             redeem_amount = 0
#             rule_id = 0
#
#             if "redeem_amount" in postdata:
#                 redeem_amount = postdata['redeem_amount']
#
#             if "rule_id" in postdata and postdata['rule_id']!="":
#                 rule_id = postdata['rule_id']
#
#             customer_id = None
#             loyalty_amount = 0
#             # if 'loyalty_amount' in postdata and float(postdata['loyalty_amount'])>0:
#             #     loyalty_amount        = postdata['loyalty_amount']
#
#             if 'time_slot_id' in postdata:
#                 time_slot_id        = postdata['time_slot_id']
#             # else:
#             #     d = datetime.strptime("22:30", "%H:%M")
#             #     d.strftime("%I:%M %p")
#             website_id 			    = postdata['website_id']
#             warehouse_id = 4
#             if warehouse_id:
#                 warehouse_id        = postdata['warehouse_id']
#
#             website_id              = website_id
#             minimum_order_amount = 0
#
#             rs_min_order = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).first()
#             if float(rs_min_order.min_order_amount)>0:
#                 minimum_order_amount = float(rs_min_order.min_order_amount)
#             # Get global settings
#             else:
#                 rs_global_settings = EngageboostGlobalSettings.objects.filter(isblocked='n', isdeleted='n', website_id= website_id).first()
#                 if rs_global_settings and float(rs_global_settings.min_order_amount)>0:
#                     minimum_order_amount = float(rs_global_settings.min_order_amount)
#
#             # customer_id = user_id
#             # has_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
#             # customer_id = has_customer.id
#
#             order_serializer_arr    = {}
#
#             # *** Get Customer details
#             # customerdetails         = postdata["customerdetails"]
#             payment_type_id         = 0
#             str_status = ""
#             #********FETCH PAYMENT TYPE********#
#             if coupon_code:
#                 applied_coupon = coupon_code
#             else:
#                 applied_coupon = None
#
#             #******** SAVE CUSTOMER INFORMATION ********#
#
#             address_book_id = address_book_id
#             try:
#                 has_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
#                 if has_customer:
#                     customer_id = has_customer.id
#                 else:
#                     raise Exception("Customer not Found.")
#                 rs_customerdetails = EngageboostCustomersAddressBook.objects.filter(id=address_book_id).first()
#                 customerdetails = CustomersAddressBookSerializer(rs_customerdetails)
#                 customerdetails = customerdetails.data
#             except Exception as error:
#                 str_status = status.HTTP_417_EXPECTATION_FAILED
#                 trace_back = sys.exc_info()[2]
#                 line = trace_back.tb_lineno
#                 data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in saving customer information"}
#                 return Response(data)
#             #******** SAVE CUSTOMER INFORMATION (END)********#
#
#             #******** SAVE IN ORDER TABLE ********#
#             try:
#                 cartData = discount.GetCartDetails(1,1,customer_id, device_id, 6, 221, None, None, user_id, None,applied_coupon, warehouse_id)
#                 cartData = cartData.data
#                 # print("cartData++++++++++++++", cartData)
#                 # return 1
#                 wh_manager = None
#                 rs_wh_manager = EngageboostWarehouseManager.objects.filter(warehouse_id=warehouse_id, isdeleted='n', isblocked = 'n' ).first()
#                 if rs_wh_manager:
#                     wh_manager = rs_wh_manager.manager_id
#
#                 rs_warehouse = EngageboostWarehouseMasters.objects.filter(id = warehouse_id).first()
#
#                 rs_warehouse = EngageboostWarehouseMasters.objects.filter(id = warehouse_id).first()
#                 lst_prepaid_cat = [370,371,372,385]
#                 new_list = []
#                 if cartData:
#                     product_categories = (list(set(cartData['orderamountdetails'][0]['product_categories'])))
#                     new_list = (list(set(product_categories) - set(lst_prepaid_cat)))
#
#                 if len(new_list)>0:
#                     if cartData:
#                         check_minimum = float(cartData['orderamountdetails'][0]['net_total']) + float(cartData['orderamountdetails'][0]['shipping_charge'])
#                         if float(check_minimum)>=float(minimum_order_amount):
#                             # if int(cartData['orderamountdetails'][0]['check_stock'])>0:
#                             if float(redeem_amount)>float(cartData['orderamountdetails'][0]['net_total']):
#                                 redeem_amount = Decimal(float(cartData['orderamountdetails'][0]['net_total']) + float(cartData['orderamountdetails'][0]['shipping_charge'])).quantize(Decimal('.00'))
#                             order_info = {
#                                 "website_id":website_id,
#                                 "company_id":1,
#                                 "webshop_id":int(webshop_id),
#                                 "payment_method_id":0,
#                                 "payment_type_id":0,
#                                 "payment_method_name":"", #Decimal(cartdata["new_default_price"]).quantize(Decimal('.00'))
#                                 "gross_amount": Decimal(float(cartData['orderamountdetails'][0]['grand_total']) + float(cartData['orderamountdetails'][0]["add_shipping_discount"]) - float(redeem_amount) - float(cartData['orderamountdetails'][0]["cart_discount"])).quantize(Decimal('.00')),
#                                 "net_amount": float(cartData['orderamountdetails'][0]['net_total']) - float(cartData['orderamountdetails'][0]["add_shipping_discount"]) + float(cartData['orderamountdetails'][0]['cart_discount']),# - float(redeem_amount)+float(cartData['orderamountdetails'][0]['shipping_charge'])
#                                 "shipping_cost":cartData['orderamountdetails'][0]['shipping_charge'],
#                                 "paid_amount":cartData['orderamountdetails'][0]['paid_amount'],
#                                 "gross_discount_amount":cartData['orderamountdetails'][0]['gross_discount'],
#                                 "tax_amount":cartData['orderamountdetails'][0]["tax_amount"],
#                                 "order_status":0,
#                                 "buy_status":1,
#                                 "created":now_utc,
#                                 "modified":now_utc,
#                                 "cart_discount":cartData['orderamountdetails'][0]["cart_discount"],
#                                 "cod_charge":cartData['orderamountdetails'][0]["cod_charge"],
#                                 # "applied_coupon":applied_coupon,
#                                 # "pay_wallet_amount":loyalty_amount,
#                                 "zone_id":24,
#                                 # "custom_msg":cartData['orderamountdetails'][0]["custom_msg"],
#                                 "custom_msg": special_instruction,
#                                 "customer_id":customer_id,
#                                 "assign_wh":warehouse_id,
#                                 "assign_to":wh_manager,
#                                 "pay_wallet_amount":redeem_amount
#                             }
#
#                             str_applied_coupon = ""
#                             if cartData['applied_coupon'] and cartData['applied_coupon'][0]['status']>0:
#                                 str_applied_coupon = cartData['applied_coupon'][0]['coupon_code']
#
#                             order_info.update({"applied_coupon":str_applied_coupon})
#
#                             if 'gross_total' in postdata:
#                                 order_info.update({ "order_amount":cartData['orderamountdetails'][0]['grand_total']})
#                             if 'time_slot_date' in postdata:
#                                 order_info.update({"time_slot_date":postdata["time_slot_date"]})
#                             if 'time_slot_id' in postdata:
#                                 order_info.update({"time_slot_id":postdata["time_slot_id"]})
#                             if 'slot_start_time' in postdata:
#                                 order_info.update({"slot_start_time":postdata["slot_start_time"]})
#                             if 'slot_end_time' in postdata:
#                                 order_info.update({"slot_end_time":postdata["slot_end_time"]})
#
#                             time_slot_id = "06:00 PM - 06:00 PM"
#                             slot_start_time = "18:00"
#                             slot_end_time = "18:00"
#                             if str(now_utc.date()) == str(time_slot_date):
#                                 hours = 0
#                                 if postdata['warehouse_id']:
#                                     get_warehouse = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).values('id','expected_delivery_time').first()
#                                     if get_warehouse:
#                                         hours = get_warehouse['expected_delivery_time']
#
#                                 extended_current_slot_start = now_utc + timedelta(hours=float(hours))
#                                 extended_current_slot_end = extended_current_slot_start + timedelta(hours=float(2))
#                                 # slot_start_time = str(extended_current_slot_start.hour)+':'+str(extended_current_slot_start.minute)
#                                 slot_start_time = str(extended_current_slot_start.strftime("%H"))+':'+str(extended_current_slot_start.strftime("%M"))
#                                 # slot_end_time = str(extended_current_slot_end.hour)+':'+str(extended_current_slot_end.minute)
#                                 slot_end_time = slot_start_time
#
#                                 slot_start_time_txt = datetime.strptime(slot_start_time, "%H:%M")
#                                 slot_start_time_txt = slot_start_time_txt.strftime("%I:%M %p")
#                                 slot_end_time_txt = datetime.strptime(slot_end_time, "%H:%M")
#                                 slot_end_time_txt = slot_end_time_txt.strftime("%I:%M %p")
#                                 time_slot_id = str(slot_start_time_txt)+' - '+str(slot_start_time_txt)
#                             else:
#                                 time_slot_id = "06:00 PM - 06:00 PM"
#                                 slot_start_time = "18:00"
#                                 slot_end_time = "18:00"
#
#                             order_info.update({"time_slot_id":time_slot_id})
#                             order_info.update({"slot_start_time":slot_start_time})
#                             order_info.update({"slot_end_time":slot_end_time})
#
#                             # if 'currency_id' in postdata:
#                             #     currency = common.get_currency_details(postdata["currency_id"])
#                             #     order_info.update({"currency_code":currency["currency"]})
#                             # else:
#                             #     order_info.update({"currency_code":base_currency["currency_code"]})
#                             order_info.update({"currency_code":"AED"})
#
#                             if address_book_id!="" and address_book_id!=None:
#                                 order_info.update({"address_book_id":address_book_id})
#
#                             order_serializer_arr = dict(order_serializer_arr,**order_info)
#                             customer_info={
#                                 "billing_name":str(customerdetails["billing_name"]),
#                                 "billing_email_address":customerdetails["billing_email_address"],
#                                 "billing_street_address":customerdetails["billing_street_address"],
#                                 "billing_street_address1":customerdetails["billing_street_address1"],
#                                 "billing_city":customerdetails["billing_city"],
#                                 "billing_postcode":customerdetails["billing_postcode"],
#                                 "billing_state":customerdetails["billing_state"],
#                                 "billing_state_name":customerdetails['billing_state_name'],
#                                 "billing_country":customerdetails["billing_country"],
#                                 "billing_country_name":customerdetails['billing_country_name'],
#                                 "billing_phone":customerdetails["billing_phone"],
#                                 "delivery_name":customerdetails["billing_name"],
#                                 "delivery_email_address":customerdetails["billing_email_address"],
#                                 "delivery_street_address":customerdetails["delivery_street_address"],
#                                 "delivery_street_address1":customerdetails["delivery_street_address1"],
#                                 "delivery_city":customerdetails["delivery_city"],
#                                 "delivery_postcode":customerdetails["delivery_postcode"],
#                                 "delivery_state":customerdetails["delivery_state"],
#                                 "delivery_state_name":customerdetails['delivery_state_name'],
#                                 "delivery_country":customerdetails["delivery_country"],
#                                 "delivery_country_name":customerdetails['delivery_country_name'],
#                                 "delivery_phone":customerdetails["billing_phone"]
#                             }
#                             order_serializer_arr=dict(order_serializer_arr,**customer_info)
#                             custom_order_id = GenerateOrderId(website_id)
#                             hasOrder = EngageboostOrdermaster.objects.filter(custom_order_id=custom_order_id).first()
#
#                             if hasOrder:
#                                 custom_order_id = GenerateOrderId(website_id)
#                                 order_serializer_arr['custom_order_id']=custom_order_id
#                                 save_order_master = EngageboostOrdermaster.objects.create(**order_serializer_arr)
#                                 order_id = save_order_master.id if save_order_master else 0
#
#                                 # Loyalty Transaction
#                                 loyalty_trans_arr = {
#                                     "website_id": 1,
#                                     "rule_id": rule_id,
#                                     "customer_id": user_id,
#                                     "order_id": order_id,
#                                     "custom_order_id": custom_order_id,
#                                     "description": 'This is burn for order no ' + custom_order_id,
#                                     "received_points": 0.00,
#                                     "burnt_points": redeem_amount,
#                                     "amount": redeem_amount,
#                                     "received_burnt": redeem_amount,
#                                     "status": "burn",
#                                     "created": django.utils.timezone.now(),
#                                     "valid_form": django.utils.timezone.now(),
#                                 }
#
#                                 if order_id >0:
#                                     loyalty.save_burn_points(loyalty_trans_arr)
#                             else:
#                                 order_serializer_arr['custom_order_id']=custom_order_id
#                                 save_order_master = EngageboostOrdermaster.objects.create(**order_serializer_arr)
#                                 order_id = save_order_master.id if save_order_master else 0
#
#                                 # Loyalty Transaction
#                                 loyalty_trans_arr = {
#                                     "website_id": 1,
#                                     "rule_id": rule_id,
#                                     "customer_id": user_id,
#                                     "order_id": order_id,
#                                     "custom_order_id": custom_order_id,
#                                     "description": 'This is burn for order no ' + custom_order_id,
#                                     "received_points": 0.00,
#                                     "burnt_points": redeem_amount,
#                                     "amount": redeem_amount,
#                                     "received_burnt": redeem_amount,
#                                     "status": "burn",
#                                     "created": django.utils.timezone.now(),
#                                     "valid_form": django.utils.timezone.now(),
#                                 }
#                                 if order_id >0 and float(redeem_amount)>0:
#                                     loyalty.save_burn_points(loyalty_trans_arr)
#
#                             # Change coupon code status
#                             if applied_coupon is not None:
#                                 ChangeCouponCodeStatus(applied_coupon,warehouse_id)
#                             # else:
#                             # 	raise Exception("Some product(s) are out of stock. Please remove or change those product to continue checkout process.")
#                         else:
#                             str_status = status.HTTP_406_NOT_ACCEPTABLE
#                             data = {
#                                 "status":str_status,
#                                 "message":"Minimum order amount should be "+ str(minimum_order_amount)
#                             }
#                             return Response(data, str_status)
#                             raise Exception("Minimum order amount should be "+ str(minimum_order_amount))
#                 else:
#                     # str_status = status.HTTP_406_NOT_ACCEPTABLE
#                     str_status = status.HTTP_417_EXPECTATION_FAILED
#                     data = {
#                         "status":str_status,
#                         "message":"You can not purchase only prepaid card."
#                     }
#                     return Response(data, str_status)
#                     raise Exception("You can not purchase only prepaid card")
#
#             except Exception as error:
#                 str_status = status.HTTP_417_EXPECTATION_FAILED
#                 trace_back = sys.exc_info()[2]
#                 line = trace_back.tb_lineno
#                 data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in order creation"}
#                 return Response(data)
#             #******** SAVE IN ORDER TABLE (END)********#
#
#             #******** SAVE IN ORDER PRODUCT TABLE ********#
#             try:
#                 if cartData:
#                     for cartdetails in cartData['cartdetails']:
#                         order_product_arr={
#                             "order_id":order_id,
#                             "product_id":int(cartdetails["id"]),
#                             "quantity":int(cartdetails["qty"]),
#                             "deleted_quantity":0,
#                             "product_price":cartdetails["new_default_price_unit"],
#                             "product_discount_price":cartdetails["discount_price_unit"],
#                             "product_tax_price":cartdetails["tax_price_unit"],
#                             "tax_percentage":cartdetails["tax_percentage"],
#                             "product_price_base":cartdetails["new_default_price_unit"],
#                             "product_discount_price_base":cartdetails["discount_price_unit"],
#                             "created":now_utc,
#                             "warehouse_id":warehouse_id,
#                             "assign_wh":warehouse_id,
#                             "assign_to":wh_manager
#                         }
#
#                         price_obj = EngageboostProductPriceTypeMaster.objects.filter(isblocked='n',isdeleted='n',product_id=cartdetails["id"], price_type_id=1)
#
#                         if price_obj.count()>0:
#                             priceData = price_obj.first()
#                             obj = EngageboostChannelCurrencyProductPrice.objects.filter(product_price_type_id=priceData.id,warehouse_id=warehouse_id,product_id=cartdetails["id"])
#                             if obj.count()>0:
#                                 channelData = obj.first()
#                                 order_product_arr["mrp"] = channelData.mrp
#                                 order_product_arr["cost_price"] = channelData.price
#                         save_order_product = EngageboostOrderProducts.objects.create(**order_product_arr)
#                         common.update_stock_all(cartdetails["id"],warehouse_id,int(cartdetails["qty"]),"Decrease","virtual",order_id,website_id)
#
#             except Exception as error:
#                 str_status = status.HTTP_417_EXPECTATION_FAILED
#                 trace_back = sys.exc_info()[2]
#                 line = trace_back.tb_lineno
#                 data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in saving order product information"}
#                 return Response(data)
#             #******** SAVE IN ORDER PRODUCT TABLE (END)********#
#
#             #******** SAVE ORDER ACTIVITY ********#
#             activityType = 1
#             activity_details = common_functions.save_order_activity(order_id,now_utc,0,"Order has been placed",'',activityType)
#             elastic = common.save_data_to_elastic(order_id,'EngageboostOrdermaster')
#             #******** SAVE ORDER ACTIVITY (END)********#
#
#             #******** GENERATE AUTO RESPONDER ********#
#             buffer_data = common_functions.getAutoResponder("","","","","",3)
#             if buffer_data and buffer_data["content"]:
#                 autoResponderData  = buffer_data["content"]
#                 if autoResponderData["email_type"] == 'T':
#                     emailContent = autoResponderData["email_content_text"]
#                 else:
#                     emailContent = autoResponderData["email_content"]
#                 emailContent = str(emailContent)
#                 bcc = buffer_data['bcc']
#                 # Send Order place SMS
#                 sms_content = str(autoResponderData["sms_content_text"])
#                 str_sms = sms_content.replace('{@custom_order_id}',custom_order_id)
#                 if customerdetails["billing_phone"]:
#                     common_functions.SendSms(str_sms,customerdetails["billing_phone"])
#
#                 # SMS to Warehouse Manager
#                 sms_data = common_functions.getAutoResponder("","","","","",28)
#                 if sms_data and sms_data["content"]:
#                     autoResponderData  = sms_data["content"]
#                     manager_sms_content = str(autoResponderData["sms_content_text"])
#                     manager_sms_content = manager_sms_content.replace('{@custom_order_id}',custom_order_id)
#                     manager_sms_content = manager_sms_content.replace('{@name}',customerdetails["billing_name"])
#                     manager_sms_content = manager_sms_content.replace('{@contact_no}',customerdetails["billing_phone"])
#                     rs_user = EngageboostUsers.objects.filter(id=rs_wh_manager.manager_id).first()
#                     warehouse_manager_phone = rs_user.phone
#                     if warehouse_manager_phone:
#                         common_functions.SendSms(manager_sms_content,warehouse_manager_phone)
#
#                     if str(rs_warehouse.phone)==str(warehouse_manager_phone):
#                         pass
#                     else:
#                         common_functions.SendSms(manager_sms_content,rs_warehouse.phone)
#
#                 emailContent = emailContent.replace('{@first_name}',customerdetails["billing_name"])
#                 emailContent = emailContent.replace('{@custom_order_id}',custom_order_id)
#                 emailContent = emailContent.replace('{@delivery_name}',customerdetails["billing_name"])
#                 emailContent = emailContent.replace('{@delivery_street_address}',customerdetails["delivery_street_address"])
#                 #emailContent = emailContent.replace('{@delivery_city}',customerdetails["delivery_city"])
#                 # emailContent = emailContent.replace('{@delivery_postcode}',customerdetails["delivery_postcode"])
#                 # emailContent = emailContent.replace('{@delivery_state}',customerdetails['billing_state_name'])
#                 emailContent = emailContent.replace('{@delivery_country}',customerdetails['billing_country_name'])
#                 emailContent = emailContent.replace('{@delivery_phone}',customerdetails["billing_phone"])
#                 # emailContent = emailContent.replace('{@payment_method_name}',payment_method_name)
#                 # gross_amt = float(cartData['orderamountdetails'][0]['net_total']) - float(redeem_amount)+float(cartData['orderamountdetails'][0]['shipping_charge'])
#                 gross_amt = float(cartData['orderamountdetails'][0]['grand_total'])
#                 net_amt = float(cartData['orderamountdetails'][0]['net_total'])+float(cartData['orderamountdetails'][0]['shipping_charge']) + float(cartData['orderamountdetails'][0]["cart_discount"])
#                 emailContent = emailContent.replace('{@gross_amount}',str(gross_amt))
#                 emailContent = emailContent.replace('{@shipping_cost}',str(cartData['orderamountdetails'][0]["shipping_charge"]))
#                 emailContent = emailContent.replace('{@tax_amount}',str(cartData['orderamountdetails'][0]["tax_amount"]))
#                 emailContent = emailContent.replace('{@pay_wallet_amount}',str(redeem_amount))
#                 emailContent = emailContent.replace('{@discount_amount}',str(cartData['orderamountdetails'][0]["cart_discount"]))
#                 net_amount = float(cartData['orderamountdetails'][0]["net_total"])-float(redeem_amount)
#                 emailContent = emailContent.replace('{@net_amount}',str(net_amt)) #grand_total
#                 order_items = get_item_mail(cartData)
#                 emailContent = emailContent.replace('{@order_items}',str(order_items))
#                 #******** GENERATE AUTO RESPONDER (END)********#
#             if customerdetails["delivery_email_address"]:
#                 emailcomponent.OrderMail(customerdetails["delivery_email_address"],autoResponderData["email_from"],autoResponderData["subject"],emailContent, bcc)
#             # delete Temp Cart
#             EngageboostTemporaryShoppingCarts.objects.filter(customer_id=user_id).delete()
#             res_orderdata = {
#                 "gross_amount":gross_amt,
#                 "net_amount":net_amt,
#                 "discount_amount":cartData['orderamountdetails'][0]["cart_discount"],
#                 "pay_wallet_amount":redeem_amount
#             }
#             str_status = status.HTTP_200_OK
#             data={"status":str_status,"api_status":"Order created successfully","message":"Order created successfully", "order_id":custom_order_id, "order_data":res_orderdata}
#         except Exception as error:
#             str_status = status.HTTP_417_EXPECTATION_FAILED
#             trace_back = sys.exc_info()[2]
#             line = trace_back.tb_lineno
#             data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Something went wrong", "order_data":{}}
#         return Response(data, str_status)
#-----quick fix 11-10-2020----#
class SaveCart(APIView):
    def post(self, request, format=None):
        # now_utc = datetime.now(timezone.utc).astimezone()
        now_utc = datetime.now(timezone('UTC')).astimezone(timezone('Asia/Dubai'))
        shipping_label_content = ""
        #  *************  Get Base currency
        base_currency = "AED"
        customer_info = {}
        order_id = ''
        order_status = 0
        try:
            postdata = request.data
            user = request.user
            user_id = user.id
            device_id = postdata['device_id']
            # user_id 				= postdata['user_id']
            address_book_id = postdata['address_book_id']
            time_slot_date = postdata['time_slot_date']
            time_slot_time = postdata['time_slot_time']
            # special_instruction 	= postdata['special_instruction']
            coupon_code = postdata['coupon_code']
            payment_method_id = postdata['payment_method_id']
            payment_type_id = postdata['payment_type_id']
            payment_method_name = postdata['payment_method_name']

            if payment_type_id == 2 and payment_method_id == 51:
                order_status = 21

            webshop_id = 6
            if "webshop_id" in postdata:
                webshop_id = postdata['webshop_id']
            special_instruction = None
            if "special_instruction" in postdata:
                special_instruction = postdata['special_instruction']

            redeem_amount = 0
            rule_id = 0

            if "redeem_amount" in postdata:
                redeem_amount = postdata['redeem_amount']

            if "rule_id" in postdata and postdata['rule_id'] != "":
                rule_id = postdata['rule_id']

            customer_id = None
            loyalty_amount = 0
            # if 'loyalty_amount' in postdata and float(postdata['loyalty_amount'])>0:
            #     loyalty_amount        = postdata['loyalty_amount']

            if 'time_slot_id' in postdata:
                time_slot_id = postdata['time_slot_id']
            # else:
            #     d = datetime.strptime("22:30", "%H:%M")
            #     d.strftime("%I:%M %p")
            website_id = postdata['website_id']
            warehouse_id = 4
            if warehouse_id:
                warehouse_id = postdata['warehouse_id']

            website_id = website_id
            minimum_order_amount = 0

            rs_min_order = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).first()
            if float(rs_min_order.min_order_amount) > 0:
                minimum_order_amount = float(rs_min_order.min_order_amount)
            # Get global settings
            else:
                rs_global_settings = EngageboostGlobalSettings.objects.filter(isblocked='n', isdeleted='n',
                                                                              website_id=website_id).first()
                if rs_global_settings and float(rs_global_settings.min_order_amount) > 0:
                    minimum_order_amount = float(rs_global_settings.min_order_amount)

            # customer_id = user_id
            # has_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
            # customer_id = has_customer.id

            order_serializer_arr = {}

            # *** Get Customer details
            # customerdetails         = postdata["customerdetails"]
            # payment_type_id         = 0
            str_status = ""
            # ********FETCH PAYMENT TYPE********#
            if coupon_code:
                applied_coupon = coupon_code
            else:
                applied_coupon = None

            # ******** SAVE CUSTOMER INFORMATION ********#

            address_book_id = address_book_id
            try:
                has_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
                if has_customer:
                    customer_id = has_customer.id
                else:
                    raise Exception("Customer not Found.")
                rs_customerdetails = EngageboostCustomersAddressBook.objects.filter(id=address_book_id).first()
                customerdetails = CustomersAddressBookSerializer(rs_customerdetails)
                customerdetails = customerdetails.data
            except Exception as error:
                str_status = status.HTTP_417_EXPECTATION_FAILED
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line,
                        "error_message": str(error), "message": "Error in saving customer information"}
                return Response(data)
            # ******** SAVE CUSTOMER INFORMATION (END)********#

            # ******** SAVE IN ORDER TABLE ********#
            try:
                cartData = discount.GetCartDetails(1, 1, customer_id, device_id, 6, 221, None, None, user_id, None,
                                                   applied_coupon, warehouse_id)
                cartData = cartData.data
                # print("cartData++++++++++++++", cartData)
                # return 1
                wh_manager = None
                rs_wh_manager = EngageboostWarehouseManager.objects.filter(warehouse_id=warehouse_id, isdeleted='n',
                                                                           isblocked='n').first()
                if rs_wh_manager:
                    wh_manager = rs_wh_manager.manager_id

                rs_warehouse = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).first()

                rs_warehouse = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).first()
                lst_prepaid_cat = [370, 371, 372, 385]
                new_list = []
                if cartData:
                    product_categories = (list(set(cartData['orderamountdetails'][0]['product_categories'])))
                    new_list = (list(set(product_categories) - set(lst_prepaid_cat)))

                if len(new_list) > 0:
                    if cartData:
                        check_minimum = float(cartData['orderamountdetails'][0]['net_total']) + float(
                            cartData['orderamountdetails'][0]['shipping_charge'])
                        if float(check_minimum) >= float(minimum_order_amount):
                            # if int(cartData['orderamountdetails'][0]['check_stock'])>0:
                            if float(redeem_amount) > float(cartData['orderamountdetails'][0]['net_total']):
                                redeem_amount = Decimal(float(cartData['orderamountdetails'][0]['net_total']) + float(
                                    cartData['orderamountdetails'][0]['shipping_charge'])).quantize(Decimal('.00'))
                            order_info = {
                                "website_id": website_id,
                                "company_id": 1,
                                "webshop_id": int(webshop_id),
                                "payment_method_id": payment_method_id,
                                "payment_type_id": payment_type_id,
                                "payment_method_name": payment_method_name,
                            # Decimal(cartdata["new_default_price"]).quantize(Decimal('.00'))
                                # "gross_amount":Decimal(float(cartData['orderamountdetails'][0]['grand_total']) - float(redeem_amount)-float(cartData['orderamountdetails'][0]["cart_discount"])).quantize(Decimal('.00')),
                                # "net_amount":float(cartData['orderamountdetails'][0]['net_total'])+float(cartData['orderamountdetails'][0]['shipping_charge']) + float(cartData['orderamountdetails'][0]['cart_discount']), # - float(redeem_amount)+float(cartData['orderamountdetails'][0]['shipping_charge'])
                                # "gross_amount": Decimal(float(cartData['orderamountdetails'][0]['grand_total']) + float(
                                #     cartData['orderamountdetails'][0]["add_shipping_discount"]) - float(
                                #     redeem_amount) - float(
                                #     cartData['orderamountdetails'][0]["cart_discount"])).quantize(Decimal('.00')),
                                #
                                "gross_amount": Decimal(float(cartData['orderamountdetails'][0]['grand_total']) + float(
                                    cartData['orderamountdetails'][0]["add_shipping_discount"]) - float(
                                    redeem_amount) - float(cartData['orderamountdetails'][0]["cart_discount"]) + float(
                                    cartData['orderamountdetails'][0]["product_cart_discount"])).quantize(
                                    Decimal('.00')),
                                "net_amount": float(cartData['orderamountdetails'][0]['net_total']) - float(
                                    cartData['orderamountdetails'][0]["add_shipping_discount"]) + float(
                                    cartData['orderamountdetails'][0]['cart_discount']),
                                # - float(redeem_amount)+float(cartData['orderamountdetails'][0]['shipping_charge'])
                                "shipping_cost": cartData['orderamountdetails'][0]['shipping_charge'],
                                "paid_amount": cartData['orderamountdetails'][0]['paid_amount'],
                                "gross_discount_amount": cartData['orderamountdetails'][0]['gross_discount'],
                                "tax_amount": cartData['orderamountdetails'][0]["tax_amount"],
                                "order_status": order_status,
                                "buy_status": 1,
                                "created": now_utc,
                                "modified": now_utc,
                                "cart_discount": cartData['orderamountdetails'][0]["cart_discount"],
                                "cod_charge": cartData['orderamountdetails'][0]["cod_charge"],
                                # "applied_coupon":applied_coupon,
                                # "pay_wallet_amount":loyalty_amount,
                                "zone_id": 24,
                                # "custom_msg":cartData['orderamountdetails'][0]["custom_msg"],
                                "custom_msg": special_instruction,
                                "customer_id": customer_id,
                                "assign_wh": warehouse_id,
                                "assign_to": wh_manager,
                                "pay_wallet_amount": redeem_amount
                            }

                            str_applied_coupon = ""
                            if cartData['applied_coupon'] and cartData['applied_coupon'][0]['status'] > 0:
                                str_applied_coupon = cartData['applied_coupon'][0]['coupon_code']

                            order_info.update({"applied_coupon": str_applied_coupon})

                            if 'gross_total' in postdata:
                                order_info.update({"order_amount": cartData['orderamountdetails'][0]['grand_total']})
                            if 'time_slot_date' in postdata:
                                order_info.update({"time_slot_date": postdata["time_slot_date"]})
                            if 'time_slot_id' in postdata:
                                order_info.update({"time_slot_id": postdata["time_slot_id"]})
                            if 'slot_start_time' in postdata:
                                order_info.update({"slot_start_time": postdata["slot_start_time"]})
                            if 'slot_end_time' in postdata:
                                order_info.update({"slot_end_time": postdata["slot_end_time"]})

                            time_slot_id = "06:00 PM - 06:00 PM"
                            slot_start_time = "18:00"
                            slot_end_time = "18:00"
                            if str(now_utc.date()) == str(time_slot_date):
                                hours = 0
                                if postdata['warehouse_id']:
                                    get_warehouse = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).values(
                                        'id', 'expected_delivery_time').first()
                                    if get_warehouse:
                                        hours = get_warehouse['expected_delivery_time']

                                extended_current_slot_start = now_utc + timedelta(hours=float(hours))
                                extended_current_slot_end = extended_current_slot_start + timedelta(hours=float(2))
                                # slot_start_time = str(extended_current_slot_start.hour)+':'+str(extended_current_slot_start.minute)
                                slot_start_time = str(extended_current_slot_start.strftime("%H")) + ':' + str(
                                    extended_current_slot_start.strftime("%M"))
                                # slot_end_time = str(extended_current_slot_end.hour)+':'+str(extended_current_slot_end.minute)
                                slot_end_time = slot_start_time

                                slot_start_time_txt = datetime.strptime(slot_start_time, "%H:%M")
                                slot_start_time_txt = slot_start_time_txt.strftime("%I:%M %p")
                                slot_end_time_txt = datetime.strptime(slot_end_time, "%H:%M")
                                slot_end_time_txt = slot_end_time_txt.strftime("%I:%M %p")
                                time_slot_id = str(slot_start_time_txt) + ' - ' + str(slot_start_time_txt)
                            else:
                                time_slot_id = "06:00 PM - 06:00 PM"
                                slot_start_time = "18:00"
                                slot_end_time = "18:00"

                            order_info.update({"time_slot_id": time_slot_id})
                            order_info.update({"slot_start_time": slot_start_time})
                            order_info.update({"slot_end_time": slot_end_time})

                            # if 'currency_id' in postdata:
                            #     currency = common.get_currency_details(postdata["currency_id"])
                            #     order_info.update({"currency_code":currency["currency"]})
                            # else:
                            #     order_info.update({"currency_code":base_currency["currency_code"]})
                            order_info.update({"currency_code": "AED"})

                            if address_book_id != "" and address_book_id != None:
                                order_info.update({"address_book_id": address_book_id})

                            order_serializer_arr = dict(order_serializer_arr, **order_info)
                            customer_info = {
                                "billing_name": str(customerdetails["billing_name"]),
                                "billing_email_address": customerdetails["billing_email_address"],
                                "billing_street_address": customerdetails["billing_street_address"],
                                "billing_street_address1": customerdetails["billing_street_address1"],
                                "billing_landmark": customerdetails["billing_landmark"],
                                "billing_city": customerdetails["billing_city"],
                                "billing_postcode": customerdetails["billing_postcode"],
                                "billing_state": customerdetails["billing_state"],
                                "billing_state_name": customerdetails['billing_state_name'],
                                "billing_country": customerdetails["billing_country"],
                                "billing_country_name": customerdetails['billing_country_name'],
                                "billing_phone": customerdetails["billing_phone"],
                                "delivery_name": customerdetails["billing_name"],
                                "delivery_email_address": customerdetails["billing_email_address"],
                                "delivery_street_address": customerdetails["delivery_street_address"],
                                "delivery_street_address1": customerdetails["delivery_street_address1"],
                                "delivery_landmark": customerdetails["delivery_landmark"],
                                "delivery_city": customerdetails["delivery_city"],
                                "delivery_postcode": customerdetails["delivery_postcode"],
                                "delivery_state": customerdetails["delivery_state"],
                                "delivery_state_name": customerdetails['delivery_state_name'],
                                "delivery_country": customerdetails["delivery_country"],
                                "delivery_country_name": customerdetails['delivery_country_name'],
                                "delivery_phone": customerdetails["billing_phone"]
                            }
                            order_serializer_arr = dict(order_serializer_arr, **customer_info)
                            custom_order_id = GenerateOrderId(website_id)
                            hasOrder = EngageboostOrdermaster.objects.filter(custom_order_id=custom_order_id).first()

                            if hasOrder:
                                custom_order_id = GenerateOrderId(website_id)
                                order_serializer_arr['custom_order_id'] = custom_order_id
                                save_order_master = EngageboostOrdermaster.objects.create(**order_serializer_arr)
                                order_id = save_order_master.id if save_order_master else 0

                                # Loyalty Transaction
                                loyalty_trans_arr = {
                                    "website_id": 1,
                                    "rule_id": rule_id,
                                    "customer_id": user_id,
                                    "order_id": order_id,
                                    "custom_order_id": custom_order_id,
                                    "description": 'This is burn for order no ' + custom_order_id,
                                    "received_points": 0.00,
                                    "burnt_points": redeem_amount,
                                    "amount": redeem_amount,
                                    "received_burnt": redeem_amount,
                                    "status": "burn",
                                    "created": django.utils.timezone.now(),
                                    "valid_form": django.utils.timezone.now(),
                                }

                                if order_id > 0:
                                    loyalty.save_burn_points(loyalty_trans_arr)
                            else:
                                order_serializer_arr['custom_order_id'] = custom_order_id
                                save_order_master = EngageboostOrdermaster.objects.create(**order_serializer_arr)
                                order_id = save_order_master.id if save_order_master else 0

                                # Loyalty Transaction
                                loyalty_trans_arr = {
                                    "website_id": 1,
                                    "rule_id": rule_id,
                                    "customer_id": user_id,
                                    "order_id": order_id,
                                    "custom_order_id": custom_order_id,
                                    "description": 'This is burn for order no ' + custom_order_id,
                                    "received_points": 0.00,
                                    "burnt_points": redeem_amount,
                                    "amount": redeem_amount,
                                    "received_burnt": redeem_amount,
                                    "status": "burn",
                                    "created": django.utils.timezone.now(),
                                    "valid_form": django.utils.timezone.now(),
                                }
                                if order_id > 0 and float(redeem_amount) > 0:
                                    loyalty.save_burn_points(loyalty_trans_arr)

                            # Change coupon code status
                            # Change coupon code status
                            if applied_coupon is not None:
                                ChangeCouponCodeStatus(applied_coupon, warehouse_id)
                            # else:
                            # 	raise Exception("Some product(s) are out of stock. Please remove or change those product to continue checkout process.")
                        else:
                            str_status = status.HTTP_406_NOT_ACCEPTABLE
                            data = {
                                "status": str_status,
                                "message": "Minimum order amount should be " + str(minimum_order_amount)
                            }
                            return Response(data, str_status)
                            raise Exception("Minimum order amount should be " + str(minimum_order_amount))
                else:
                    # str_status = status.HTTP_406_NOT_ACCEPTABLE
                    str_status = status.HTTP_417_EXPECTATION_FAILED
                    data = {
                        "status": str_status,
                        "message": "You can not purchase only prepaid card."
                    }
                    return Response(data, str_status)
                    raise Exception("You can not purchase only prepaid card")

            except Exception as error:
                str_status = status.HTTP_417_EXPECTATION_FAILED
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line,
                        "error_message": str(error), "message": "Error in order creation"}
                return Response(data)
            # ******** SAVE IN ORDER TABLE (END)********#

            # ******** SAVE IN ORDER PRODUCT TABLE ********#
            try:
                if cartData:
                    for cartdetails in cartData['cartdetails']:
                        # order_product_arr={
                        #     "order_id":order_id,
                        #     "product_id":int(cartdetails["id"]),
                        #     "quantity":int(cartdetails["qty"]),
                        #     "deleted_quantity":0,
                        #     "product_price":cartdetails["new_default_price_unit"],
                        #     "product_discount_price":cartdetails["discount_price_unit"],
                        #     "product_tax_price":cartdetails["tax_price_unit"],
                        #     "tax_percentage":cartdetails["tax_percentage"],
                        #     "product_price_base":cartdetails["new_default_price_unit"],
                        #     "product_discount_price_base":cartdetails["discount_price_unit"],
                        #     "created":now_utc,
                        #     "warehouse_id":warehouse_id,
                        #     "assign_wh":warehouse_id,
                        #     "assign_to":wh_manager
                        # }


                        order_product_arr = {
                            "order_id": order_id,
                            "product_id": int(cartdetails["id"]),
                            "quantity": int(cartdetails["qty"]),
                            "deleted_quantity": 0,
                            "product_price": cartdetails["new_default_price_unit"],
                            "product_discount_price": cartdetails["discount_price_unit"],
                            "product_tax_price": cartdetails["tax_price_unit"],
                            "tax_percentage": cartdetails["tax_percentage"],
                            "product_price_base": cartdetails["new_default_price_unit"],
                            "product_discount_price_base": cartdetails["discount_price_unit"],
                            "created": now_utc,
                            "warehouse_id": warehouse_id,
                            "assign_wh": warehouse_id,
                            "assign_to": wh_manager,
                            "custom_field_name": cartdetails["custom_field_name"],
                            "custom_field_value": cartdetails["custom_field_value"]
                        }

                        price_obj = EngageboostProductPriceTypeMaster.objects.filter(isblocked='n', isdeleted='n',
                                                                                     product_id=cartdetails["id"],
                                                                                     price_type_id=1)

                        if price_obj.count() > 0:
                            priceData = price_obj.first()
                            obj = EngageboostChannelCurrencyProductPrice.objects.filter(
                                product_price_type_id=priceData.id, warehouse_id=warehouse_id,
                                product_id=cartdetails["id"])
                            if obj.count() > 0:
                                channelData = obj.first()
                                order_product_arr["mrp"] = channelData.mrp
                                order_product_arr["cost_price"] = channelData.price
                        save_order_product = EngageboostOrderProducts.objects.create(**order_product_arr)
                        common.update_stock_all(cartdetails["id"], warehouse_id, int(cartdetails["qty"]), "Decrease",
                                                "virtual", order_id, website_id)

            except Exception as error:
                str_status = status.HTTP_417_EXPECTATION_FAILED
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line,
                        "error_message": str(error), "message": "Error in saving order product information"}
                return Response(data)
            # ******** SAVE IN ORDER PRODUCT TABLE (END)********#

            # ******** SAVE ORDER ACTIVITY ********#
            activityType = 1
            activity_details = common_functions.save_order_activity(order_id, now_utc, 0, "Order has been placed", '',
                                                                    activityType)
            elastic = common.save_data_to_elastic(order_id, 'EngageboostOrdermaster')
            # ******** SAVE ORDER ACTIVITY (END)********#

            # ******** GENERATE AUTO RESPONDER ********#
            buffer_data = common_functions.getAutoResponder("", "", "", "", "", 3)
            if buffer_data and buffer_data["content"]:
                autoResponderData = buffer_data["content"]
                if autoResponderData["email_type"] == 'T':
                    emailContent = autoResponderData["email_content_text"]
                else:
                    emailContent = autoResponderData["email_content"]
                emailContent = str(emailContent)

                # Send Order place SMS
                sms_content = str(autoResponderData["sms_content_text"])
                str_sms = sms_content.replace('{@custom_order_id}', custom_order_id)
                # if customerdetails["billing_phone"]:
                #     common_functions.SendSms(str_sms,customerdetails["billing_phone"])

                # SMS to Warehouse Manager
                sms_data = common_functions.getAutoResponder("", "", "", "", "", 28)
                if sms_data and sms_data["content"]:
                    autoResponderData = sms_data["content"]
                    manager_sms_content = str(autoResponderData["sms_content_text"])
                    manager_sms_content = manager_sms_content.replace('{@custom_order_id}', custom_order_id)
                    manager_sms_content = manager_sms_content.replace('{@name}', customerdetails["billing_name"])
                    manager_sms_content = manager_sms_content.replace('{@contact_no}', customerdetails["billing_phone"])
                    rs_user = EngageboostUsers.objects.filter(id=rs_wh_manager.manager_id).first()
                    warehouse_manager_phone = rs_user.phone
                    # if warehouse_manager_phone:
                    #     common_functions.SendSms(manager_sms_content,warehouse_manager_phone)
                    #
                    # if str(rs_warehouse.phone)==str(warehouse_manager_phone):
                    #     pass
                    # else:
                    #     common_functions.SendSms(manager_sms_content,rs_warehouse.phone)

                emailContent = emailContent.replace('{@first_name}', customerdetails["billing_name"])
                emailContent = emailContent.replace('{@custom_order_id}', custom_order_id)
                emailContent = emailContent.replace('{@delivery_name}', customerdetails["billing_name"])
                emailContent = emailContent.replace('{@delivery_street_address}',
                                                    customerdetails["delivery_street_address"])
                # emailContent = emailContent.replace('{@delivery_city}',customerdetails["delivery_city"])
                # emailContent = emailContent.replace('{@delivery_postcode}',customerdetails["delivery_postcode"])
                # emailContent = emailContent.replace('{@delivery_state}',customerdetails['billing_state_name'])
                emailContent = emailContent.replace('{@delivery_country}', customerdetails['billing_country_name'])
                emailContent = emailContent.replace('{@delivery_phone}', customerdetails["billing_phone"])
                # emailContent = emailContent.replace('{@payment_method_name}',payment_method_name)
                # gross_amt = float(cartData['orderamountdetails'][0]['net_total']) - float(redeem_amount)+float(cartData['orderamountdetails'][0]['shipping_charge'])
                gross_amt = float(cartData['orderamountdetails'][0]['grand_total'])
                # net_amt = float(cartData['orderamountdetails'][0]['net_total']) + float(
                #     cartData['orderamountdetails'][0]['shipping_charge']) + float(
                #     cartData['orderamountdetails'][0]["cart_discount"])
                net_amt = float(cartData['orderamountdetails'][0]['net_total']) + float(
                    cartData['orderamountdetails'][0]["cart_discount"])
                emailContent = emailContent.replace('{@gross_amount}', str(gross_amt))
                emailContent = emailContent.replace('{@shipping_cost}',
                                                    str(cartData['orderamountdetails'][0]["shipping_charge"]))
                emailContent = emailContent.replace('{@tax_amount}',
                                                    str(cartData['orderamountdetails'][0]["tax_amount"]))
                emailContent = emailContent.replace('{@pay_wallet_amount}', str(redeem_amount))
                emailContent = emailContent.replace('{@discount_amount}',
                                                    str(cartData['orderamountdetails'][0]["cart_discount"]))
                net_amount = float(cartData['orderamountdetails'][0]["net_total"]) - float(redeem_amount)
                emailContent = emailContent.replace('{@net_amount}', str(net_amt))  # grand_total
                order_items = get_item_mail(cartData)
                emailContent = emailContent.replace('{@order_items}', str(order_items))
                # ******** GENERATE AUTO RESPONDER (END)********#
            # if customerdetails["delivery_email_address"]:
            #     emailcomponent.OrderMail(customerdetails["delivery_email_address"],autoResponderData["email_from"],autoResponderData["subject"],emailContent)
            # # delete Temp Cart
            # EngageboostTemporaryShoppingCarts.objects.filter(customer_id=user_id).delete()

            # if payment_type_id == 4 and payment_method_id == 16:
            #     checkout_put(custom_order_id, payment_method_id, payment_type_id, payment_method_name)

            if payment_type_id == 4 and payment_method_id == 16:
                checkout_put(custom_order_id, payment_method_id, payment_type_id, payment_method_name)

                if customerdetails["delivery_email_address"]:
                    emailcomponent.OrderMail(customerdetails["delivery_email_address"], autoResponderData["email_from"],
                                             autoResponderData["subject"], emailContent)

                # Send Order place SMS
                if customerdetails["billing_phone"]:
                    common_functions.SendSms(str_sms, customerdetails["billing_phone"])

                # Send Order place NOTIFICATION
                common.notification_send_by_AutoResponder(order_id, 3)

                # SMS to Warehouse Manager
                sms_data = common_functions.getAutoResponder("", "", "", "", "", 28)
                if sms_data and sms_data["content"]:
                    autoResponderData = sms_data["content"]
                    manager_sms_content = str(autoResponderData["sms_content_text"])
                    manager_sms_content = manager_sms_content.replace('{@custom_order_id}', custom_order_id)
                    manager_sms_content = manager_sms_content.replace('{@name}',
                                                                      customerdetails["billing_name"])
                    manager_sms_content = manager_sms_content.replace('{@contact_no}',
                                                                      customerdetails["billing_phone"])
                    rs_user = EngageboostUsers.objects.filter(id=rs_wh_manager.manager_id).first()
                    warehouse_manager_phone = rs_user.phone
                    if warehouse_manager_phone:
                        common_functions.SendSms(manager_sms_content, warehouse_manager_phone)

                    if str(rs_warehouse.phone) == str(warehouse_manager_phone):
                        pass
                    else:
                        common_functions.SendSms(manager_sms_content, rs_warehouse.phone)

            elif payment_type_id == 4 and payment_method_id == 59:
                checkout_put(custom_order_id, payment_method_id, payment_type_id, payment_method_name)

                if customerdetails["delivery_email_address"]:
                    emailcomponent.OrderMail(customerdetails["delivery_email_address"], autoResponderData["email_from"],
                                             autoResponderData["subject"], emailContent)

                # Send Order place SMS
                if customerdetails["billing_phone"]:
                    common_functions.SendSms(str_sms, customerdetails["billing_phone"])

                # Send Order place NOTIFICATION
                common.notification_send_by_AutoResponder(order_id, 3)

                # SMS to Warehouse Manager
                sms_data = common_functions.getAutoResponder("", "", "", "", "", 28)
                if sms_data and sms_data["content"]:
                    autoResponderData = sms_data["content"]
                    manager_sms_content = str(autoResponderData["sms_content_text"])
                    manager_sms_content = manager_sms_content.replace('{@custom_order_id}', custom_order_id)
                    manager_sms_content = manager_sms_content.replace('{@name}',
                                                                      customerdetails["billing_name"])
                    manager_sms_content = manager_sms_content.replace('{@contact_no}',
                                                                      customerdetails["billing_phone"])
                    rs_user = EngageboostUsers.objects.filter(id=rs_wh_manager.manager_id).first()
                    warehouse_manager_phone = rs_user.phone
                    if warehouse_manager_phone:
                        common_functions.SendSms(manager_sms_content, warehouse_manager_phone)

                    if str(rs_warehouse.phone) == str(warehouse_manager_phone):
                        pass
                    else:
                        common_functions.SendSms(manager_sms_content, rs_warehouse.phone)

            res_orderdata = {
                "gross_amount": gross_amt,
                "net_amount": net_amt,
                "discount_amount": cartData['orderamountdetails'][0]["cart_discount"],
                "pay_wallet_amount": redeem_amount,
                "customer_info": customer_info
            }

            str_status = status.HTTP_200_OK
            data = {"status": str_status, "api_status": "Order created successfully",
                    "message": "Order created successfully", "order_id": custom_order_id, "order_data": res_orderdata}
        except Exception as error:
            str_status = status.HTTP_417_EXPECTATION_FAILED
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line,
                    "error_message": str(error), "message": "Something went wrong", "order_data": {}}
        return Response(data, str_status)
#-----quick fix end 11-10-2020----#

class SaveCartSi(APIView):
    def post(self, request, format=None):
        # now_utc = datetime.now(timezone.utc).astimezone()
        now_utc = datetime.now(timezone('UTC')).astimezone(timezone('Asia/Dubai'))
        shipping_label_content = ""
        #  *************  Get Base currency
        base_currency = "AED"
        customer_info = {}
        order_id = ''
        order_status = 0
        try:
            postdata                = request.data
            user                = request.user
            user_id             = user.id
            device_id 				= postdata['device_id']
            # user_id 				= postdata['user_id']
            address_book_id 		= postdata['address_book_id']
            time_slot_date 		    = postdata['time_slot_date']
            time_slot_time 		    = postdata['time_slot_time']
            # special_instruction 	= postdata['special_instruction']
            coupon_code 			= postdata['coupon_code']
            payment_method_id 		= postdata['payment_method_id']
            payment_type_id			= postdata['payment_type_id']
            payment_method_name 	= postdata['payment_method_name']
            si_ref_no = postdata.get('si_ref_no')

            if payment_type_id == 2 and payment_method_id == 51:
                if si_ref_no in (None, ''):
                    order_status = 21

            # if payment_type_id == 2 and payment_method_id == 51:
            #     order_status = 21

            webshop_id 				= 6
            if "webshop_id" in postdata:
                webshop_id = postdata['webshop_id']
            special_instruction = None
            if "special_instruction" in postdata:
                special_instruction = postdata['special_instruction']

            redeem_amount = 0
            rule_id = 0

            if "redeem_amount" in postdata:
                redeem_amount = postdata['redeem_amount']

            if "rule_id" in postdata and postdata['rule_id']!="":
                rule_id = postdata['rule_id']

            customer_id = None
            loyalty_amount = 0
            # if 'loyalty_amount' in postdata and float(postdata['loyalty_amount'])>0:
            #     loyalty_amount        = postdata['loyalty_amount']

            if 'time_slot_id' in postdata:
                time_slot_id        = postdata['time_slot_id']
            # else:
            #     d = datetime.strptime("22:30", "%H:%M")
            #     d.strftime("%I:%M %p")
            website_id 			    = postdata['website_id']
            warehouse_id = 4
            if warehouse_id:
                warehouse_id        = postdata['warehouse_id']

            website_id              = website_id
            minimum_order_amount = 0

            rs_min_order = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).first()
            if float(rs_min_order.min_order_amount)>0:
                minimum_order_amount = float(rs_min_order.min_order_amount)
            # Get global settings
            else:
                rs_global_settings = EngageboostGlobalSettings.objects.filter(isblocked='n', isdeleted='n', website_id= website_id).first()
                if rs_global_settings and float(rs_global_settings.min_order_amount)>0:
                    minimum_order_amount = float(rs_global_settings.min_order_amount)

            # customer_id = user_id
            # has_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
            # customer_id = has_customer.id

            order_serializer_arr    = {}

            # *** Get Customer details
            # customerdetails         = postdata["customerdetails"]
            # payment_type_id         = 0
            str_status = ""
            #********FETCH PAYMENT TYPE********#
            if coupon_code:
                applied_coupon = coupon_code
            else:
                applied_coupon = None

            #******** SAVE CUSTOMER INFORMATION ********#

            address_book_id = address_book_id
            try:
                has_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
                if has_customer:
                    customer_id = has_customer.id
                else:
                    raise Exception("Customer not Found.")
                rs_customerdetails = EngageboostCustomersAddressBook.objects.filter(id=address_book_id).first()
                customerdetails = CustomersAddressBookSerializer(rs_customerdetails)
                customerdetails = customerdetails.data
            except Exception as error:
                str_status = status.HTTP_417_EXPECTATION_FAILED
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in saving customer information"}
                return Response(data)
            #******** SAVE CUSTOMER INFORMATION (END)********#

            #******** SAVE IN ORDER TABLE ********#
            try:
                cartData = discount.GetCartDetails(1,1,customer_id, device_id, 6, 221, None, None, user_id, None,applied_coupon, warehouse_id)
                cartData = cartData.data
                # print("cartData++++++++++++++", cartData)
                # return 1
                wh_manager = None
                rs_wh_manager = EngageboostWarehouseManager.objects.filter(warehouse_id=warehouse_id, isdeleted='n', isblocked = 'n' ).first()
                if rs_wh_manager:
                    wh_manager = rs_wh_manager.manager_id

                rs_warehouse = EngageboostWarehouseMasters.objects.filter(id = warehouse_id).first()

                rs_warehouse = EngageboostWarehouseMasters.objects.filter(id = warehouse_id).first()
                lst_prepaid_cat = [370,371,372,385]
                new_list = []
                if cartData:
                    product_categories = (list(set(cartData['orderamountdetails'][0]['product_categories'])))
                    new_list = (list(set(product_categories) - set(lst_prepaid_cat)))

                if len(new_list)>0:
                    if cartData:
                        # check_minimum = float(cartData['orderamountdetails'][0]['net_total']) + float(cartData['orderamountdetails'][0]['shipping_charge'])
                        check_minimum = float(cartData['orderamountdetails'][0]['sub_total']) + float(cartData['orderamountdetails'][0]['cart_discount'])
                        if float(check_minimum)>=float(minimum_order_amount):
                            # if int(cartData['orderamountdetails'][0]['check_stock'])>0:
                            if float(redeem_amount)>float(cartData['orderamountdetails'][0]['net_total']):
                                redeem_amount = Decimal(float(cartData['orderamountdetails'][0]['net_total']) + float(cartData['orderamountdetails'][0]['shipping_charge'])).quantize(Decimal('.00'))
                            order_info = {
                                "website_id":website_id,
                                "company_id":1,
                                "webshop_id":int(webshop_id),
                                "payment_method_id": payment_method_id,
                                "payment_type_id": payment_type_id,
                                "payment_method_name": payment_method_name, #Decimal(cartdata["new_default_price"]).quantize(Decimal('.00'))
                                # "gross_amount":Decimal(float(cartData['orderamountdetails'][0]['grand_total']) - float(redeem_amount)-float(cartData['orderamountdetails'][0]["cart_discount"])).quantize(Decimal('.00')),
                                # "net_amount":float(cartData['orderamountdetails'][0]['net_total'])+float(cartData['orderamountdetails'][0]['shipping_charge']) + float(cartData['orderamountdetails'][0]['cart_discount']), # - float(redeem_amount)+float(cartData['orderamountdetails'][0]['shipping_charge'])
                                "gross_amount": Decimal(float(cartData['orderamountdetails'][0]['grand_total']) + float(
                                    cartData['orderamountdetails'][0]["add_shipping_discount"]) - float(
                                    redeem_amount) - float(
                                    cartData['orderamountdetails'][0]["cart_discount"])).quantize(Decimal('.00')),
                                "net_amount": float(cartData['orderamountdetails'][0]['net_total']) - float(
                                    cartData['orderamountdetails'][0]["add_shipping_discount"]) + float(
                                    cartData['orderamountdetails'][0]['cart_discount']),
                            # - float(redeem_amount)+float(cartData['orderamountdetails'][0]['shipping_charge'])
                                "shipping_cost":cartData['orderamountdetails'][0]['shipping_charge'],
                                "paid_amount":cartData['orderamountdetails'][0]['paid_amount'],
                                "gross_discount_amount":cartData['orderamountdetails'][0]['gross_discount'],
                                "tax_amount":cartData['orderamountdetails'][0]["tax_amount"],
                                "order_status":order_status,
                                "buy_status":1,
                                "created":now_utc,
                                "modified":now_utc,
                                "cart_discount":cartData['orderamountdetails'][0]["cart_discount"],
                                "cod_charge":cartData['orderamountdetails'][0]["cod_charge"],
                                # "applied_coupon":applied_coupon,
                                # "pay_wallet_amount":loyalty_amount,
                                "zone_id":24,
                                # "custom_msg":cartData['orderamountdetails'][0]["custom_msg"],
                                "custom_msg": special_instruction,
                                "customer_id":customer_id,
                                "assign_wh":warehouse_id,
                                "assign_to":wh_manager,
                                "pay_wallet_amount":redeem_amount
                            }

                            str_applied_coupon = ""
                            if cartData['applied_coupon'] and cartData['applied_coupon'][0]['status']>0:
                                str_applied_coupon = cartData['applied_coupon'][0]['coupon_code']

                            order_info.update({"applied_coupon":str_applied_coupon})

                            if 'gross_total' in postdata:
                                order_info.update({ "order_amount":cartData['orderamountdetails'][0]['grand_total']})
                            if 'time_slot_date' in postdata:
                                order_info.update({"time_slot_date":postdata["time_slot_date"]})
                            if 'time_slot_id' in postdata:
                                order_info.update({"time_slot_id":postdata["time_slot_id"]})
                            if 'slot_start_time' in postdata:
                                order_info.update({"slot_start_time":postdata["slot_start_time"]})
                            if 'slot_end_time' in postdata:
                                order_info.update({"slot_end_time":postdata["slot_end_time"]})

                            time_slot_id = "06:00 PM - 06:00 PM"
                            slot_start_time = "18:00"
                            slot_end_time = "18:00"
                            if str(now_utc.date()) == str(time_slot_date):
                                hours = 0
                                if postdata['warehouse_id']:
                                    get_warehouse = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).values('id','expected_delivery_time').first()
                                    if get_warehouse:
                                        hours = get_warehouse['expected_delivery_time']

                                extended_current_slot_start = now_utc + timedelta(hours=float(hours))
                                extended_current_slot_end = extended_current_slot_start + timedelta(hours=float(2))
                                # slot_start_time = str(extended_current_slot_start.hour)+':'+str(extended_current_slot_start.minute)
                                slot_start_time = str(extended_current_slot_start.strftime("%H"))+':'+str(extended_current_slot_start.strftime("%M"))
                                # slot_end_time = str(extended_current_slot_end.hour)+':'+str(extended_current_slot_end.minute)
                                slot_end_time = slot_start_time
                                
                                slot_start_time_txt = datetime.strptime(slot_start_time, "%H:%M")
                                slot_start_time_txt = slot_start_time_txt.strftime("%I:%M %p")
                                slot_end_time_txt = datetime.strptime(slot_end_time, "%H:%M")
                                slot_end_time_txt = slot_end_time_txt.strftime("%I:%M %p")
                                time_slot_id = str(slot_start_time_txt)+' - '+str(slot_start_time_txt)
                            else:
                                time_slot_id = "06:00 PM - 06:00 PM"
                                slot_start_time = "18:00"
                                slot_end_time = "18:00"

                            order_info.update({"time_slot_id":time_slot_id})
                            order_info.update({"slot_start_time":slot_start_time})
                            order_info.update({"slot_end_time":slot_end_time})

                            # if 'currency_id' in postdata:
                            #     currency = common.get_currency_details(postdata["currency_id"])
                            #     order_info.update({"currency_code":currency["currency"]})
                            # else:
                            #     order_info.update({"currency_code":base_currency["currency_code"]})
                            order_info.update({"currency_code":"AED"})

                            if address_book_id!="" and address_book_id!=None:
                                order_info.update({"address_book_id":address_book_id})

                            order_serializer_arr = dict(order_serializer_arr,**order_info)
                            customer_info={
                                "billing_name":str(customerdetails["billing_name"]),
                                "billing_email_address":customerdetails["billing_email_address"],
                                "billing_street_address":customerdetails["billing_street_address"],
                                "billing_street_address1":customerdetails["billing_street_address1"],
                                "billing_landmark": customerdetails["billing_landmark"],
                                "billing_city":customerdetails["billing_city"],
                                "billing_postcode":customerdetails["billing_postcode"],
                                "billing_state":customerdetails["billing_state"],
                                "billing_state_name":customerdetails['billing_state_name'],
                                "billing_country":customerdetails["billing_country"],
                                "billing_country_name":customerdetails['billing_country_name'],
                                "billing_phone":customerdetails["billing_phone"],
                                "delivery_name":customerdetails["billing_name"],
                                "delivery_email_address":customerdetails["billing_email_address"],
                                "delivery_street_address":customerdetails["delivery_street_address"],
                                "delivery_street_address1":customerdetails["delivery_street_address1"],
                                "delivery_landmark": customerdetails["delivery_landmark"],
                                "delivery_city":customerdetails["delivery_city"],
                                "delivery_postcode":customerdetails["delivery_postcode"],
                                "delivery_state":customerdetails["delivery_state"],
                                "delivery_state_name":customerdetails['delivery_state_name'],
                                "delivery_country":customerdetails["delivery_country"],
                                "delivery_country_name":customerdetails['delivery_country_name'],
                                "delivery_phone":customerdetails["billing_phone"]
                            }
                            order_serializer_arr=dict(order_serializer_arr,**customer_info)
                            custom_order_id = GenerateOrderId(website_id)
                            hasOrder = EngageboostOrdermaster.objects.filter(custom_order_id=custom_order_id).first()

                            if hasOrder:
                                custom_order_id = GenerateOrderId(website_id)
                                order_serializer_arr['custom_order_id']=custom_order_id
                                save_order_master = EngageboostOrdermaster.objects.create(**order_serializer_arr)
                                order_id = save_order_master.id if save_order_master else 0

                                # Loyalty Transaction
                                loyalty_trans_arr = {
                                    "website_id": 1,
                                    "rule_id": rule_id,
                                    "customer_id": user_id,
                                    "order_id": order_id,
                                    "custom_order_id": custom_order_id,
                                    "description": 'This is burn for order no ' + custom_order_id,
                                    "received_points": 0.00,
                                    "burnt_points": redeem_amount,
                                    "amount": redeem_amount,
                                    "received_burnt": redeem_amount,
                                    "status": "burn",
                                    "created": django.utils.timezone.now(),
                                    "valid_form": django.utils.timezone.now(),
                                }

                                if order_id >0:
                                    loyalty.save_burn_points(loyalty_trans_arr)
                            else:
                                order_serializer_arr['custom_order_id']=custom_order_id
                                save_order_master = EngageboostOrdermaster.objects.create(**order_serializer_arr)
                                order_id = save_order_master.id if save_order_master else 0

                                # Loyalty Transaction
                                loyalty_trans_arr = {
                                    "website_id": 1,
                                    "rule_id": rule_id,
                                    "customer_id": user_id,
                                    "order_id": order_id,
                                    "custom_order_id": custom_order_id,
                                    "description": 'This is burn for order no ' + custom_order_id,
                                    "received_points": 0.00,
                                    "burnt_points": redeem_amount,
                                    "amount": redeem_amount,
                                    "received_burnt": redeem_amount,
                                    "status": "burn",
                                    "created": django.utils.timezone.now(),
                                    "valid_form": django.utils.timezone.now(),
                                }
                                if order_id >0 and float(redeem_amount)>0:
                                    loyalty.save_burn_points(loyalty_trans_arr)

                            # Change coupon code status
                            # Change coupon code status
                            if applied_coupon is not None:
                                ChangeCouponCodeStatus(applied_coupon,warehouse_id)
                            # else:
                            # 	raise Exception("Some product(s) are out of stock. Please remove or change those product to continue checkout process.")
                        else:
                            str_status = status.HTTP_406_NOT_ACCEPTABLE
                            data = {
                                "status":str_status,
                                "message":"Minimum order amount should be "+ str(minimum_order_amount)
                            }
                            return Response(data, str_status)
                            raise Exception("Minimum order amount should be "+ str(minimum_order_amount))
                else:
                    # str_status = status.HTTP_406_NOT_ACCEPTABLE
                    str_status = status.HTTP_417_EXPECTATION_FAILED
                    data = {
                        "status":str_status,
                        "message":"You can not purchase only prepaid card."
                    }
                    return Response(data, str_status)
                    raise Exception("You can not purchase only prepaid card")

            except Exception as error:
                str_status = status.HTTP_417_EXPECTATION_FAILED
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in order creation"}
                return Response(data)
            #******** SAVE IN ORDER TABLE (END)********#

            #******** SAVE IN ORDER PRODUCT TABLE ********#
            try:
                if cartData:
                    for cartdetails in cartData['cartdetails']:
                        order_product_arr={
                            "order_id":order_id,
                            "product_id":int(cartdetails["id"]),
                            "quantity":int(cartdetails["qty"]),
                            "deleted_quantity":0,
                            "product_price":cartdetails["new_default_price_unit"],
                            "product_discount_price":cartdetails["discount_price_unit"],
                            "product_tax_price":cartdetails["tax_price_unit"],
                            "tax_percentage":cartdetails["tax_percentage"],
                            "product_price_base":cartdetails["new_default_price_unit"],
                            "product_discount_price_base":cartdetails["discount_price_unit"],
                            "created":now_utc,
                            "warehouse_id":warehouse_id,
                            "assign_wh":warehouse_id,
                            "assign_to":wh_manager,
                            "custom_field_name": cartdetails["custom_field_name"],
                            "custom_field_value": cartdetails["custom_field_value"]
                        }

                        price_obj = EngageboostProductPriceTypeMaster.objects.filter(isblocked='n',isdeleted='n',product_id=cartdetails["id"], price_type_id=1)

                        if price_obj.count()>0:
                            priceData = price_obj.first()
                            obj = EngageboostChannelCurrencyProductPrice.objects.filter(product_price_type_id=priceData.id,warehouse_id=warehouse_id,product_id=cartdetails["id"])
                            if obj.count()>0:
                                channelData = obj.first()
                                order_product_arr["mrp"] = channelData.mrp
                                order_product_arr["cost_price"] = channelData.price
                        save_order_product = EngageboostOrderProducts.objects.create(**order_product_arr)
                        common.update_stock_all(cartdetails["id"],warehouse_id,int(cartdetails["qty"]),"Decrease","virtual",order_id,website_id)

            except Exception as error:
                str_status = status.HTTP_417_EXPECTATION_FAILED
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in saving order product information"}
                return Response(data)
            #******** SAVE IN ORDER PRODUCT TABLE (END)********#

            #******** SAVE ORDER ACTIVITY ********#
            activityType = 1
            activity_details = common_functions.save_order_activity(order_id,now_utc,0,"Order has been placed",'',activityType)
            elastic = common.save_data_to_elastic(order_id,'EngageboostOrdermaster')
            #******** SAVE ORDER ACTIVITY (END)********#

            #******** GENERATE AUTO RESPONDER ********#
            buffer_data = common_functions.getAutoResponder("","","","","",3)
            if buffer_data and buffer_data["content"]:
                autoResponderData  = buffer_data["content"]
                if autoResponderData["email_type"] == 'T':
                    emailContent = autoResponderData["email_content_text"]
                else:
                    emailContent = autoResponderData["email_content"]
                emailContent = str(emailContent)

                # Send Order place SMS
                sms_content = str(autoResponderData["sms_content_text"])
                str_sms = sms_content.replace('{@custom_order_id}',custom_order_id)
                # if customerdetails["billing_phone"]:
                #     common_functions.SendSms(str_sms,customerdetails["billing_phone"])

                # SMS to Warehouse Manager
                sms_data = common_functions.getAutoResponder("","","","","",28)
                if sms_data and sms_data["content"]:
                    autoResponderData  = sms_data["content"]
                    manager_sms_content = str(autoResponderData["sms_content_text"])
                    manager_sms_content = manager_sms_content.replace('{@custom_order_id}',custom_order_id)
                    manager_sms_content = manager_sms_content.replace('{@name}',customerdetails["billing_name"])
                    manager_sms_content = manager_sms_content.replace('{@contact_no}',customerdetails["billing_phone"])
                    rs_user = EngageboostUsers.objects.filter(id=rs_wh_manager.manager_id).first()
                    warehouse_manager_phone = rs_user.phone
                    # if warehouse_manager_phone:
                    #     common_functions.SendSms(manager_sms_content,warehouse_manager_phone)
                    #
                    # if str(rs_warehouse.phone)==str(warehouse_manager_phone):
                    #     pass
                    # else:
                    #     common_functions.SendSms(manager_sms_content,rs_warehouse.phone)

                emailContent = emailContent.replace('{@first_name}',customerdetails["billing_name"])
                emailContent = emailContent.replace('{@custom_order_id}',custom_order_id)
                emailContent = emailContent.replace('{@delivery_name}',customerdetails["billing_name"])
                emailContent = emailContent.replace('{@delivery_street_address}',customerdetails["delivery_street_address"])
                #emailContent = emailContent.replace('{@delivery_city}',customerdetails["delivery_city"])
                # emailContent = emailContent.replace('{@delivery_postcode}',customerdetails["delivery_postcode"])
                # emailContent = emailContent.replace('{@delivery_state}',customerdetails['billing_state_name'])
                emailContent = emailContent.replace('{@delivery_country}',customerdetails['billing_country_name'])
                emailContent = emailContent.replace('{@delivery_phone}',customerdetails["billing_phone"])
                # emailContent = emailContent.replace('{@payment_method_name}',payment_method_name)
                # gross_amt = float(cartData['orderamountdetails'][0]['net_total']) - float(redeem_amount)+float(cartData['orderamountdetails'][0]['shipping_charge'])
                gross_amt = float(cartData['orderamountdetails'][0]['grand_total'])
                net_amt = float(cartData['orderamountdetails'][0]['net_total'])+float(cartData['orderamountdetails'][0]['shipping_charge']) + float(cartData['orderamountdetails'][0]["cart_discount"])
                emailContent = emailContent.replace('{@gross_amount}',str(gross_amt))
                emailContent = emailContent.replace('{@shipping_cost}',str(cartData['orderamountdetails'][0]["shipping_charge"]))
                emailContent = emailContent.replace('{@tax_amount}',str(cartData['orderamountdetails'][0]["tax_amount"]))
                emailContent = emailContent.replace('{@pay_wallet_amount}',str(redeem_amount))
                emailContent = emailContent.replace('{@discount_amount}',str(cartData['orderamountdetails'][0]["cart_discount"]))
                net_amount = float(cartData['orderamountdetails'][0]["net_total"])-float(redeem_amount)
                emailContent = emailContent.replace('{@net_amount}',str(net_amt)) #grand_total
                order_items = get_item_mail(cartData)
                emailContent = emailContent.replace('{@order_items}',str(order_items))
                #******** GENERATE AUTO RESPONDER (END)********#
            # if customerdetails["delivery_email_address"]:
            #     emailcomponent.OrderMail(customerdetails["delivery_email_address"],autoResponderData["email_from"],autoResponderData["subject"],emailContent)
            # # delete Temp Cart
            # EngageboostTemporaryShoppingCarts.objects.filter(customer_id=user_id).delete()

            # if payment_type_id == 4 and payment_method_id == 16:
            #     checkout_put(custom_order_id, payment_method_id, payment_type_id, payment_method_name)

            if payment_type_id == 4 and payment_method_id == 16:
                checkout_put(custom_order_id, payment_method_id, payment_type_id, payment_method_name)

                if customerdetails["delivery_email_address"]:
                    emailcomponent.OrderMail(customerdetails["delivery_email_address"], autoResponderData["email_from"],
                                             autoResponderData["subject"], emailContent)

                # Send Order place SMS
                if customerdetails["billing_phone"]:
                    common_functions.SendSms(str_sms,customerdetails["billing_phone"])

                # Send Order place NOTIFICATION
                common.notification_send_by_AutoResponder(order_id, 3)


                # SMS to Warehouse Manager
                sms_data = common_functions.getAutoResponder("", "", "", "", "", 28)
                if sms_data and sms_data["content"]:
                    autoResponderData = sms_data["content"]
                    manager_sms_content = str(autoResponderData["sms_content_text"])
                    manager_sms_content = manager_sms_content.replace('{@custom_order_id}', custom_order_id)
                    manager_sms_content = manager_sms_content.replace('{@name}',
                                                                      customerdetails["billing_name"])
                    manager_sms_content = manager_sms_content.replace('{@contact_no}',
                                                                      customerdetails["billing_phone"])
                    rs_user = EngageboostUsers.objects.filter(id=rs_wh_manager.manager_id).first()
                    warehouse_manager_phone = rs_user.phone
                    if warehouse_manager_phone:
                        common_functions.SendSms(manager_sms_content, warehouse_manager_phone)

                    if str(rs_warehouse.phone) == str(warehouse_manager_phone):
                        pass
                    else:
                        common_functions.SendSms(manager_sms_content, rs_warehouse.phone)

            elif payment_type_id == 4 and payment_method_id == 59:
                checkout_put(custom_order_id, payment_method_id, payment_type_id, payment_method_name)

                if customerdetails["delivery_email_address"]:
                    emailcomponent.OrderMail(customerdetails["delivery_email_address"], autoResponderData["email_from"],
                                             autoResponderData["subject"], emailContent)

                # Send Order place SMS
                if customerdetails["billing_phone"]:
                    common_functions.SendSms(str_sms, customerdetails["billing_phone"])

                # Send Order place NOTIFICATION
                common.notification_send_by_AutoResponder(order_id, 3)

                # SMS to Warehouse Manager
                sms_data = common_functions.getAutoResponder("", "", "", "", "", 28)
                if sms_data and sms_data["content"]:
                    autoResponderData = sms_data["content"]
                    manager_sms_content = str(autoResponderData["sms_content_text"])
                    manager_sms_content = manager_sms_content.replace('{@custom_order_id}', custom_order_id)
                    manager_sms_content = manager_sms_content.replace('{@name}',
                                                                      customerdetails["billing_name"])
                    manager_sms_content = manager_sms_content.replace('{@contact_no}',
                                                                      customerdetails["billing_phone"])
                    rs_user = EngageboostUsers.objects.filter(id=rs_wh_manager.manager_id).first()
                    warehouse_manager_phone = rs_user.phone
                    if warehouse_manager_phone:
                        common_functions.SendSms(manager_sms_content, warehouse_manager_phone)

                    if str(rs_warehouse.phone) == str(warehouse_manager_phone):
                        pass
                    else:
                        common_functions.SendSms(manager_sms_content, rs_warehouse.phone)

            res_orderdata = {
                "gross_amount":gross_amt,
                "net_amount":net_amt,
                "discount_amount":cartData['orderamountdetails'][0]["cart_discount"],
                "pay_wallet_amount":redeem_amount,
                "customer_info": customer_info
            }

            str_status = status.HTTP_200_OK
            data={"status":str_status,"api_status":"Order created successfully","message":"Order created successfully", "order_id":custom_order_id, "order_data":res_orderdata}
        except Exception as error:
            str_status = status.HTTP_417_EXPECTATION_FAILED
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Something went wrong", "order_data":{}}
        return Response(data, str_status)

class SaveCartSiNew(APIView):
    permission_classes = []

    def post(self, request, format=None):
        # now_utc = datetime.now(timezone.utc).astimezone()
        now_utc = datetime.now(timezone('UTC')).astimezone(timezone('Asia/Dubai'))
        shipping_label_content = ""
        #  *************  Get Base currency
        base_currency = "AED"
        customer_info = {}
        order_id = ''
        order_status = 0
        # print('now_utc')
        # print(now_utc)
        try:
            postdata                = request.data
            user                = request.user
            user_id             = user.id
            device_id 				= postdata['device_id']
            # user_id 				= postdata['user_id']
            address_book_id 		= postdata['address_book_id']
            time_slot_date 		    = postdata['time_slot_date']
            time_slot_time 		    = postdata['time_slot_time']
            # special_instruction 	= postdata['special_instruction']
            coupon_code 			= postdata['coupon_code']
            payment_method_id 		= postdata['payment_method_id']
            payment_type_id			= postdata['payment_type_id']
            payment_method_name 	= postdata['payment_method_name']

            if payment_type_id == 2 and payment_method_id == 51:
                order_status = 21

            webshop_id 				= 6
            if "webshop_id" in postdata:
                webshop_id = postdata['webshop_id']
            special_instruction = None
            if "special_instruction" in postdata:
                special_instruction = postdata['special_instruction']

            redeem_amount = 0
            rule_id = 0

            if "redeem_amount" in postdata:
                redeem_amount = postdata['redeem_amount']

            if "rule_id" in postdata and postdata['rule_id']!="":
                rule_id = postdata['rule_id']

            customer_id = None
            loyalty_amount = 0
            # if 'loyalty_amount' in postdata and float(postdata['loyalty_amount'])>0:
            #     loyalty_amount        = postdata['loyalty_amount']

            if 'time_slot_id' in postdata:
                time_slot_id        = postdata['time_slot_id']
            # else:
            #     d = datetime.strptime("22:30", "%H:%M")
            #     d.strftime("%I:%M %p")
            website_id 			    = postdata['website_id']
            warehouse_id = 4
            if warehouse_id:
                warehouse_id        = postdata['warehouse_id']

            website_id              = website_id
            minimum_order_amount = 0

            rs_min_order = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).first()
            if float(rs_min_order.min_order_amount)>0:
                minimum_order_amount = float(rs_min_order.min_order_amount)
            # Get global settings
            else:
                rs_global_settings = EngageboostGlobalSettings.objects.filter(isblocked='n', isdeleted='n', website_id= website_id).first()
                if rs_global_settings and float(rs_global_settings.min_order_amount)>0:
                    minimum_order_amount = float(rs_global_settings.min_order_amount)

            # customer_id = user_id
            # has_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
            # customer_id = has_customer.id

            order_serializer_arr    = {}

            # *** Get Customer details
            # customerdetails         = postdata["customerdetails"]
            # payment_type_id         = 0
            str_status = ""
            #********FETCH PAYMENT TYPE********#
            if coupon_code:
                applied_coupon = coupon_code
            else:
                applied_coupon = None

            #******** SAVE CUSTOMER INFORMATION ********#

            address_book_id = address_book_id
            try:
                has_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
                if has_customer:
                    customer_id = has_customer.id
                else:
                    raise Exception("Customer not Found.")
                rs_customerdetails = EngageboostCustomersAddressBook.objects.filter(id=address_book_id).first()
                customerdetails = CustomersAddressBookSerializer(rs_customerdetails)
                customerdetails = customerdetails.data
            except Exception as error:
                str_status = status.HTTP_417_EXPECTATION_FAILED
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in saving customer information"}
                return Response(data)
            #******** SAVE CUSTOMER INFORMATION (END)********#

            #******** SAVE IN ORDER TABLE ********#
            try:
                cartData = discount.GetCartDetails(1,1,customer_id, device_id, 6, 221, None, None, user_id, None,applied_coupon, warehouse_id)
                cartData = cartData.data
                # print("cartData++++++++++++++", cartData)
                # return 1
                wh_manager = None
                rs_wh_manager = EngageboostWarehouseManager.objects.filter(warehouse_id=warehouse_id, isdeleted='n', isblocked = 'n' ).first()
                if rs_wh_manager:
                    wh_manager = rs_wh_manager.manager_id

                rs_warehouse = EngageboostWarehouseMasters.objects.filter(id = warehouse_id).first()

                rs_warehouse = EngageboostWarehouseMasters.objects.filter(id = warehouse_id).first()
                lst_prepaid_cat = [370,371,372,385]
                new_list = []
                if cartData:
                    product_categories = (list(set(cartData['orderamountdetails'][0]['product_categories'])))
                    new_list = (list(set(product_categories) - set(lst_prepaid_cat)))

                if len(new_list)>0:
                    if cartData:
                        check_minimum = float(cartData['orderamountdetails'][0]['net_total']) + float(cartData['orderamountdetails'][0]['shipping_charge'])
                        if float(check_minimum)>=float(minimum_order_amount):
                            # if int(cartData['orderamountdetails'][0]['check_stock'])>0:
                            if float(redeem_amount)>float(cartData['orderamountdetails'][0]['net_total']):
                                redeem_amount = Decimal(float(cartData['orderamountdetails'][0]['net_total']) + float(cartData['orderamountdetails'][0]['shipping_charge'])).quantize(Decimal('.00'))
                            order_info = {
                                "website_id":website_id,
                                "company_id":1,
                                "webshop_id":int(webshop_id),
                                "payment_method_id": payment_method_id,
                                "payment_type_id": payment_type_id,
                                "payment_method_name": payment_method_name, #Decimal(cartdata["new_default_price"]).quantize(Decimal('.00'))
                                "gross_amount":Decimal(float(cartData['orderamountdetails'][0]['grand_total']) - float(redeem_amount)-float(cartData['orderamountdetails'][0]["cart_discount"])).quantize(Decimal('.00')),
                                "net_amount":float(cartData['orderamountdetails'][0]['net_total'])+float(cartData['orderamountdetails'][0]['shipping_charge']) + float(cartData['orderamountdetails'][0]['cart_discount']), # - float(redeem_amount)+float(cartData['orderamountdetails'][0]['shipping_charge'])
                                "shipping_cost":cartData['orderamountdetails'][0]['shipping_charge'],
                                "paid_amount":cartData['orderamountdetails'][0]['paid_amount'],
                                "gross_discount_amount":cartData['orderamountdetails'][0]['gross_discount'],
                                "tax_amount":cartData['orderamountdetails'][0]["tax_amount"],
                                "order_status":order_status,
                                "buy_status":1,
                                "created":now_utc,
                                "modified":now_utc,
                                "cart_discount":cartData['orderamountdetails'][0]["cart_discount"],
                                "cod_charge":cartData['orderamountdetails'][0]["cod_charge"],
                                # "applied_coupon":applied_coupon,
                                # "pay_wallet_amount":loyalty_amount,
                                "zone_id":24,
                                # "custom_msg":cartData['orderamountdetails'][0]["custom_msg"],
                                "custom_msg": special_instruction,
                                "customer_id":customer_id,
                                "assign_wh":warehouse_id,
                                "assign_to":wh_manager,
                                "pay_wallet_amount":redeem_amount
                            }

                            str_applied_coupon = ""
                            if cartData['applied_coupon'] and cartData['applied_coupon'][0]['status']>0:
                                str_applied_coupon = cartData['applied_coupon'][0]['coupon_code']

                            order_info.update({"applied_coupon":str_applied_coupon})

                            if 'gross_total' in postdata:
                                order_info.update({ "order_amount":cartData['orderamountdetails'][0]['grand_total']})
                            if 'time_slot_date' in postdata:
                                order_info.update({"time_slot_date":postdata["time_slot_date"]})
                            if 'time_slot_id' in postdata:
                                order_info.update({"time_slot_id":postdata["time_slot_id"]})
                            if 'slot_start_time' in postdata:
                                order_info.update({"slot_start_time":postdata["slot_start_time"]})
                            if 'slot_end_time' in postdata:
                                order_info.update({"slot_end_time":postdata["slot_end_time"]})

                            order_info.update({"time_slot_id":"5:00 PM - 07:30 PM"})
                            order_info.update({"slot_start_time":"17:00"})
                            order_info.update({"slot_end_time":"19:30"})

                            # if 'currency_id' in postdata:
                            #     currency = common.get_currency_details(postdata["currency_id"])
                            #     order_info.update({"currency_code":currency["currency"]})
                            # else:
                            #     order_info.update({"currency_code":base_currency["currency_code"]})
                            order_info.update({"currency_code":"AED"})

                            if address_book_id!="" and address_book_id!=None:
                                order_info.update({"address_book_id":address_book_id})

                            order_serializer_arr = dict(order_serializer_arr,**order_info)
                            customer_info={
                                "billing_name":str(customerdetails["billing_name"]),
                                "billing_email_address":customerdetails["billing_email_address"],
                                "billing_street_address":customerdetails["billing_street_address"],
                                "billing_street_address1":customerdetails["billing_street_address1"],
                                "billing_city":customerdetails["billing_city"],
                                "billing_postcode":customerdetails["billing_postcode"],
                                "billing_state":customerdetails["billing_state"],
                                "billing_state_name":customerdetails['billing_state_name'],
                                "billing_country":customerdetails["billing_country"],
                                "billing_country_name":customerdetails['billing_country_name'],
                                "billing_phone":customerdetails["billing_phone"],
                                "delivery_name":customerdetails["billing_name"],
                                "delivery_email_address":customerdetails["billing_email_address"],
                                "delivery_street_address":customerdetails["delivery_street_address"],
                                "delivery_street_address1":customerdetails["delivery_street_address1"],
                                "delivery_city":customerdetails["delivery_city"],
                                "delivery_postcode":customerdetails["delivery_postcode"],
                                "delivery_state":customerdetails["delivery_state"],
                                "delivery_state_name":customerdetails['delivery_state_name'],
                                "delivery_country":customerdetails["delivery_country"],
                                "delivery_country_name":customerdetails['delivery_country_name'],
                                "delivery_phone":customerdetails["billing_phone"]
                            }
                            order_serializer_arr=dict(order_serializer_arr,**customer_info)
                            custom_order_id = GenerateOrderId(website_id)
                            hasOrder = EngageboostOrdermaster.objects.filter(custom_order_id=custom_order_id).first()

                            if hasOrder:
                                custom_order_id = GenerateOrderId(website_id)
                                order_serializer_arr['custom_order_id']=custom_order_id
                                save_order_master = EngageboostOrdermaster.objects.create(**order_serializer_arr)
                                order_id = save_order_master.id if save_order_master else 0

                                # Loyalty Transaction
                                loyalty_trans_arr = {
                                    "website_id": 1,
                                    "rule_id": rule_id,
                                    "customer_id": user_id,
                                    "order_id": order_id,
                                    "custom_order_id": custom_order_id,
                                    "description": 'This is burn for order no ' + custom_order_id,
                                    "received_points": 0.00,
                                    "burnt_points": redeem_amount,
                                    "amount": redeem_amount,
                                    "received_burnt": redeem_amount,
                                    "status": "burn",
                                    "created": django.utils.timezone.now(),
                                    "valid_form": django.utils.timezone.now(),
                                }

                                if order_id >0:
                                    loyalty.save_burn_points(loyalty_trans_arr)
                            else:
                                order_serializer_arr['custom_order_id']=custom_order_id
                                save_order_master = EngageboostOrdermaster.objects.create(**order_serializer_arr)
                                order_id = save_order_master.id if save_order_master else 0

                                # Loyalty Transaction
                                loyalty_trans_arr = {
                                    "website_id": 1,
                                    "rule_id": rule_id,
                                    "customer_id": user_id,
                                    "order_id": order_id,
                                    "custom_order_id": custom_order_id,
                                    "description": 'This is burn for order no ' + custom_order_id,
                                    "received_points": 0.00,
                                    "burnt_points": redeem_amount,
                                    "amount": redeem_amount,
                                    "received_burnt": redeem_amount,
                                    "status": "burn",
                                    "created": django.utils.timezone.now(),
                                    "valid_form": django.utils.timezone.now(),
                                }
                                if order_id >0 and float(redeem_amount)>0:
                                    loyalty.save_burn_points(loyalty_trans_arr)

                            # Change coupon code status
                            # Change coupon code status
                            if applied_coupon is not None:
                                ChangeCouponCodeStatus(applied_coupon,warehouse_id)
                            # else:
                            # 	raise Exception("Some product(s) are out of stock. Please remove or change those product to continue checkout process.")
                        else:
                            str_status = status.HTTP_406_NOT_ACCEPTABLE
                            data = {
                                "status":str_status,
                                "message":"Minimum order amount should be "+ str(minimum_order_amount)
                            }
                            return Response(data, str_status)
                            raise Exception("Minimum order amount should be "+ str(minimum_order_amount))
                else:
                    # str_status = status.HTTP_406_NOT_ACCEPTABLE
                    str_status = status.HTTP_417_EXPECTATION_FAILED
                    data = {
                        "status":str_status,
                        "message":"You can not purchase only prepaid card."
                    }
                    return Response(data, str_status)
                    raise Exception("You can not purchase only prepaid card")

            except Exception as error:
                str_status = status.HTTP_417_EXPECTATION_FAILED
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in order creation"}
                return Response(data)
            #******** SAVE IN ORDER TABLE (END)********#

            #******** SAVE IN ORDER PRODUCT TABLE ********#
            try:
                if cartData:
                    for cartdetails in cartData['cartdetails']:
                        order_product_arr={
                            "order_id":order_id,
                            "product_id":int(cartdetails["id"]),
                            "quantity":int(cartdetails["qty"]),
                            "deleted_quantity":0,
                            "product_price":cartdetails["new_default_price_unit"],
                            "product_discount_price":cartdetails["discount_price_unit"],
                            "product_tax_price":cartdetails["tax_price_unit"],
                            "tax_percentage":cartdetails["tax_percentage"],
                            "product_price_base":cartdetails["new_default_price_unit"],
                            "product_discount_price_base":cartdetails["discount_price_unit"],
                            "created":now_utc,
                            "warehouse_id":warehouse_id,
                            "assign_wh":warehouse_id,
                            "assign_to":wh_manager
                        }

                        price_obj = EngageboostProductPriceTypeMaster.objects.filter(isblocked='n',isdeleted='n',product_id=cartdetails["id"], price_type_id=1)

                        if price_obj.count()>0:
                            priceData = price_obj.first()
                            obj = EngageboostChannelCurrencyProductPrice.objects.filter(product_price_type_id=priceData.id,warehouse_id=warehouse_id,product_id=cartdetails["id"])
                            if obj.count()>0:
                                channelData = obj.first()
                                order_product_arr["mrp"] = channelData.mrp
                                order_product_arr["cost_price"] = channelData.price
                        save_order_product = EngageboostOrderProducts.objects.create(**order_product_arr)
                        common.update_stock_all(cartdetails["id"],warehouse_id,int(cartdetails["qty"]),"Decrease","virtual",order_id,website_id)

            except Exception as error:
                str_status = status.HTTP_417_EXPECTATION_FAILED
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in saving order product information"}
                return Response(data)
            #******** SAVE IN ORDER PRODUCT TABLE (END)********#

            #******** SAVE ORDER ACTIVITY ********#
            activityType = 1
            activity_details = common_functions.save_order_activity(order_id,now_utc,0,"Order has been placed",'',activityType)
            elastic = common.save_data_to_elastic(order_id,'EngageboostOrdermaster')
            #******** SAVE ORDER ACTIVITY (END)********#

            #******** GENERATE AUTO RESPONDER ********#
            buffer_data = common_functions.getAutoResponder("","","","","",3)
            if buffer_data and buffer_data["content"]:
                autoResponderData  = buffer_data["content"]
                if autoResponderData["email_type"] == 'T':
                    emailContent = autoResponderData["email_content_text"]
                else:
                    emailContent = autoResponderData["email_content"]
                emailContent = str(emailContent)

                # Send Order place SMS
                sms_content = str(autoResponderData["sms_content_text"])
                str_sms = sms_content.replace('{@custom_order_id}',custom_order_id)
                if customerdetails["billing_phone"]:
                    common_functions.SendSms(str_sms,customerdetails["billing_phone"])

                # SMS to Warehouse Manager
                sms_data = common_functions.getAutoResponder("","","","","",28)
                if sms_data and sms_data["content"]:
                    autoResponderData  = sms_data["content"]
                    manager_sms_content = str(autoResponderData["sms_content_text"])
                    manager_sms_content = manager_sms_content.replace('{@custom_order_id}',custom_order_id)
                    manager_sms_content = manager_sms_content.replace('{@name}',customerdetails["billing_name"])
                    manager_sms_content = manager_sms_content.replace('{@contact_no}',customerdetails["billing_phone"])
                    rs_user = EngageboostUsers.objects.filter(id=rs_wh_manager.manager_id).first()
                    warehouse_manager_phone = rs_user.phone
                    if warehouse_manager_phone:
                        common_functions.SendSms(manager_sms_content,warehouse_manager_phone)

                    if str(rs_warehouse.phone)==str(warehouse_manager_phone):
                        pass
                    else:
                        common_functions.SendSms(manager_sms_content,rs_warehouse.phone)

                emailContent = emailContent.replace('{@first_name}',customerdetails["billing_name"])
                emailContent = emailContent.replace('{@custom_order_id}',custom_order_id)
                emailContent = emailContent.replace('{@delivery_name}',customerdetails["billing_name"])
                emailContent = emailContent.replace('{@delivery_street_address}',customerdetails["delivery_street_address"])
                #emailContent = emailContent.replace('{@delivery_city}',customerdetails["delivery_city"])
                # emailContent = emailContent.replace('{@delivery_postcode}',customerdetails["delivery_postcode"])
                # emailContent = emailContent.replace('{@delivery_state}',customerdetails['billing_state_name'])
                emailContent = emailContent.replace('{@delivery_country}',customerdetails['billing_country_name'])
                emailContent = emailContent.replace('{@delivery_phone}',customerdetails["billing_phone"])
                # emailContent = emailContent.replace('{@payment_method_name}',payment_method_name)
                # gross_amt = float(cartData['orderamountdetails'][0]['net_total']) - float(redeem_amount)+float(cartData['orderamountdetails'][0]['shipping_charge'])
                gross_amt = float(cartData['orderamountdetails'][0]['grand_total'])
                net_amt = float(cartData['orderamountdetails'][0]['net_total'])+float(cartData['orderamountdetails'][0]['shipping_charge']) + float(cartData['orderamountdetails'][0]["cart_discount"])
                emailContent = emailContent.replace('{@gross_amount}',str(gross_amt))
                emailContent = emailContent.replace('{@shipping_cost}',str(cartData['orderamountdetails'][0]["shipping_charge"]))
                emailContent = emailContent.replace('{@tax_amount}',str(cartData['orderamountdetails'][0]["tax_amount"]))
                emailContent = emailContent.replace('{@pay_wallet_amount}',str(redeem_amount))
                emailContent = emailContent.replace('{@discount_amount}',str(cartData['orderamountdetails'][0]["cart_discount"]))
                net_amount = float(cartData['orderamountdetails'][0]["net_total"])-float(redeem_amount)
                emailContent = emailContent.replace('{@net_amount}',str(net_amt)) #grand_total
                order_items = get_item_mail(cartData)
                emailContent = emailContent.replace('{@order_items}',str(order_items))
                #******** GENERATE AUTO RESPONDER (END)********#
            # if customerdetails["delivery_email_address"]:
            #     emailcomponent.OrderMail(customerdetails["delivery_email_address"],autoResponderData["email_from"],autoResponderData["subject"],emailContent)
            # # delete Temp Cart
            # EngageboostTemporaryShoppingCarts.objects.filter(customer_id=user_id).delete()

            if payment_type_id == 4 and payment_method_id == 16:
                checkout_put(custom_order_id, payment_method_id, payment_type_id, payment_method_name)

                if customerdetails["delivery_email_address"]:
                    emailcomponent.OrderMail(customerdetails["delivery_email_address"], autoResponderData["email_from"],
                                             autoResponderData["subject"], emailContent)

            elif payment_type_id == 4 and payment_method_id == 59:
                checkout_put(custom_order_id, payment_method_id, payment_type_id, payment_method_name)

                if customerdetails["delivery_email_address"]:
                    emailcomponent.OrderMail(customerdetails["delivery_email_address"], autoResponderData["email_from"],
                                             autoResponderData["subject"], emailContent)

            res_orderdata = {
                "gross_amount":gross_amt,
                "net_amount":net_amt,
                "discount_amount":cartData['orderamountdetails'][0]["cart_discount"],
                "pay_wallet_amount":redeem_amount,
                "customer_info": customer_info
            }

            str_status = status.HTTP_200_OK
            data={"status":str_status,"api_status":"Order created successfully","message":"Order created successfully", "order_id":custom_order_id, "order_data":res_orderdata}
        except Exception as error:
            str_status = status.HTTP_417_EXPECTATION_FAILED
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Something went wrong", "order_data":{}}
        return Response(data, str_status)


def get_item_mail(cart_data=None):

    html = ""
    if cart_data:
        for cartdata in cart_data['cartdetails']:
            new_product_price = Decimal(cartdata["new_default_price"]).quantize(Decimal('.00'))
            product_img = ""
            if len(cartdata['product_images'])>0:
                product_img = cartdata['product_images'][0]['img']
            html = html+'<tr>'
            html = html+'<td colspan="2">'
            html = html+'<table cellpadding="10" width="600" style="width:94.5%;padding-left:3.5%">'
            html = html+'<tbody><tr>'
            html = html+'<td style="width:50px;padding-top:0;padding-bottom:0">'
            html = html+'<img src="http://lifcogrocery.s3.amazonaws.com/Lifco/lifco/product/200x200/'+product_img+'" class="CToWUd" style="height:50px"></td>'
            html = html+'<td align="left" style="width:300px" valign="top">'
            html = html+'<p style="padding:0px;color:#333;line-height:20px;margin:0">'+cartdata["name"]+'<br></p><p style="color:#999999">Quantity: <span style="color:#333">'+str(cartdata["qty"])+'</span></p></td>'
            html = html+'<td align="right">'
            # html = html+'<p style="font-size:12px;color:#999;margin:0">AED&nbsp;'+str(cartdata["new_default_price_unit"])+'</p>'
            html = html+'<p style="font-size:16px;color:#333">AED '+str(new_product_price)+'</p>'
            html = html+'</td></tr></tbody> </table> </td> </tr>'
    return html


def checkout_put(order_id, payment_method_id, payment_type_id, payment_method_name):
    now_utc = datetime.now(timezone('UTC')).astimezone(timezone('Asia/Dubai'))
    # requestdata = request.data
    # order_id = requestdata['order_id']
    # payment_method_id = requestdata["payment_method_id"]
    # payment_type_id = requestdata["payment_type_id"]
    # payment_method_name = requestdata["payment_method_name"]
    rs_cart = EngageboostOrdermaster.objects.filter(custom_order_id=order_id).first()
    customer_id = rs_cart.customer_id
    # net_amount = rs_cart.net_amount
    # applied_net_amount = float(net_amount) - loyalty_amount
    str_status = ""
    msg = ""
    update_arr = {
        "payment_method_id": payment_method_id,
        "payment_type_id": payment_type_id,
        "payment_method_name": payment_method_name
        # "order_status":0,
        # "buy_status":1
    }
    if rs_cart and rs_cart.order_status == 999:
        update_arr.update({"order_status": 100, "buy_status": 1})

    rs_check = EngageboostOrdermaster.objects.filter(customer_id=customer_id, custom_order_id=order_id).first()
    if rs_check:
        # update shipment and picklist status
        shipment_id = rs_check.shipment_id
        trent_picklist_id = rs_check.trent_picklist_id
        if shipment_id > 0 and rs_check.id > 0:
            # check already paid
            rs_ship = EngageboostShipmentOrders.objects.filter(order_id=rs_check.id, shipment=shipment_id).first()
            if rs_ship and rs_ship.shipment_status != 'Invoicing':
                str_status = status.HTTP_200_OK
                msg = "Payment Already done."
            else:
                EngageboostShipmentOrders.objects.filter(order_id=rs_check.id, shipment=shipment_id,
                                                         shipment_status='Invoicing').update(
                    shipment_status='Packed')
                AllshipmentOrder = EngageboostShipmentOrders.objects.filter(shipment=shipment_id,
                                                                            shipment_status__in=['Created',
                                                                                                 'Picking',
                                                                                                 'Invoicing']).all()
                if len(AllshipmentOrder) > 0:
                    pass
                else:
                    EngageboostTrentPicklists.objects.filter(id=trent_picklist_id,
                                                             picklist_status='Invoicing').update(
                        picklist_status='Packed')
                    EngageboostShipments.objects.filter(id=shipment_id, shipment_status='Invoicing').update(
                        shipment_status='Packed')
                # update shipment and picklist status
                str_status = status.HTTP_200_OK
                EngageboostOrdermaster.objects.filter(id=rs_check.id, customer_id=customer_id).update(**update_arr)
                msg = "Payment create successfully."
                # save_burn_points(loyalty_trans_arr)
                # elastic = common.save_data_to_elastic(rs_check.id,'EngageboostOrdermaster')
                elastic_update_arr = {
                    "payment_method_id": payment_method_id,
                    "payment_type_id": payment_type_id,
                    "payment_method_name": payment_method_name,
                    "shipping_status": "Packed"
                }
                if rs_cart and rs_cart.order_status == 999:
                    elastic_update_arr.update({"order_status": 100, "buy_status": 1})
                if rs_cart and rs_cart.order_status == 100:
                    elastic_update_arr.update({"order_status": 100, "buy_status": 1})

                elastic = common.change_field_value_elastic(rs_check.id, 'EngageboostOrdermaster',
                                                            elastic_update_arr)
                # loyalty.EarnCreditPoints(rs_check.id, user_id, 1)
                # email to customer after order approval...
                ## common.email_send_by_AutoResponder(rs_check.id, 12)
                # email to customer after order approval...

                # email to customer after order approval...
                # common.sms_send_by_AutoResponder(rs_check.id,None, 12)
                common.sms_send_by_AutoResponder(rs_check.id, None, 27)
        # email to customer after order approval...

        else:
            str_status = status.HTTP_200_OK
            msg = "Your Order Is not approved yet."
    else:
        str_status = status.HTTP_401_UNAUTHORIZED
        msg = "You are not allowed to make this payment."
    data = {
        "order_id": order_id,
        "status": str_status,
        "msg": msg
    }
    return (data, str_status)
    
class checkout(APIView):
    permission_classes = []
    def put(self, request, format=None):
        now_utc             = datetime.now(timezone('UTC')).astimezone(timezone('Asia/Dubai'))
        requestdata         = request.data
        order_id            = requestdata['order_id']
        payment_method_id   = requestdata["payment_method_id"]
        payment_type_id     = requestdata["payment_type_id"]
        payment_method_name = requestdata["payment_method_name"]
        rs_cart = EngageboostOrdermaster.objects.filter(custom_order_id=order_id).first()
        customer_id = rs_cart.customer_id
        # net_amount = rs_cart.net_amount
        # applied_net_amount = float(net_amount) - loyalty_amount
        str_status = ""
        msg = ""
        update_arr = {
            "payment_method_id":payment_method_id,
            "payment_type_id":payment_type_id,
            "payment_method_name":payment_method_name
            # "order_status":0,
            # "buy_status":1
        }
        if rs_cart and rs_cart.order_status == 999:
            update_arr.update({"order_status":100,"buy_status":1})

        rs_check = EngageboostOrdermaster.objects.filter(customer_id=customer_id, custom_order_id=order_id).first()
        if rs_check:
            # update shipment and picklist status
            shipment_id = rs_check.shipment_id
            trent_picklist_id = rs_check.trent_picklist_id
            if shipment_id > 0 and rs_check.id > 0:
                # check already paid
                rs_ship = EngageboostShipmentOrders.objects.filter(order_id=rs_check.id, shipment=shipment_id).first()
                if rs_ship and rs_ship.shipment_status != 'Invoicing':
                    str_status = status.HTTP_200_OK
                    msg= "Payment Already done."
                else:
                    EngageboostShipmentOrders.objects.filter(order_id=rs_check.id,shipment=shipment_id,shipment_status='Invoicing').update(shipment_status='Packed')
                    AllshipmentOrder = EngageboostShipmentOrders.objects.filter(shipment=shipment_id, shipment_status__in=['Created', 'Picking','Invoicing']).all()
                    if len(AllshipmentOrder)>0:
                        pass
                    else:
                        EngageboostTrentPicklists.objects.filter(id=trent_picklist_id,picklist_status='Invoicing').update(picklist_status='Packed')
                        EngageboostShipments.objects.filter(id=shipment_id,shipment_status='Invoicing').update(shipment_status='Packed')
                    # update shipment and picklist status
                    str_status = status.HTTP_200_OK
                    EngageboostOrdermaster.objects.filter(id=rs_check.id, customer_id=customer_id).update(**update_arr)
                    msg= "Payment create successfully."
                    # save_burn_points(loyalty_trans_arr)
                    # elastic = common.save_data_to_elastic(rs_check.id,'EngageboostOrdermaster')
                    elastic_update_arr = {
                        "payment_method_id":payment_method_id,
                        "payment_type_id":payment_type_id,
                        "payment_method_name":payment_method_name,
                        "shipping_status":"Packed"
                    }
                    if rs_cart and rs_cart.order_status == 999:
                        elastic_update_arr.update({"order_status":100,"buy_status":1})
                    if rs_cart and rs_cart.order_status == 100:
                        elastic_update_arr.update({"order_status":100,"buy_status":1})

                    elastic = common.change_field_value_elastic(rs_check.id,'EngageboostOrdermaster',elastic_update_arr)
                    # loyalty.EarnCreditPoints(rs_check.id, user_id, 1)
                    # email to customer after order approval...
                    ## common.email_send_by_AutoResponder(rs_check.id, 12)
                    # email to customer after order approval...

                    # email to customer after order approval...
                    # common.sms_send_by_AutoResponder(rs_check.id,None, 12)
                    common.sms_send_by_AutoResponder(rs_check.id,None, 27)
                    # email to customer after order approval...

            else:
                str_status = status.HTTP_200_OK
                msg= "Your Order Is not approved yet."
        else:
            str_status = status.HTTP_401_UNAUTHORIZED
            msg= "You are not allowed to make this payment."
        data = {
            "order_id":order_id,
            "status":str_status,
            "msg":msg
        }
        return Response(data, str_status)

def GenerateOrderId(website_id=None):
    if website_id is None:
        website_id = 1

    rs_settings = EngageboostGlobalSettings.objects.get(website_id=website_id)
    orders = EngageboostOrdermaster.objects.last()
    Order1 =int(orders.id)+int(1)
    Order1 = str(Order1)
    # cust_order_id = str(rs_settings.orderid_format)+str(Order1)
    cust_order_id = str(Order1)
    cust_order_id = "5"+Order1.zfill(7)
    return cust_order_id

class ViewOrderDetails(APIView):
    def get(self, request, order_id, format=None):
        # now_utc = datetime.now(timezone.utc).astimezone()
        now_utc	= datetime.now(timezone('UTC')).astimezone(timezone('Asia/Dubai'))
        user    = request.user
        user_id = user.id
        str_status = ""
        rs_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
        customer_id = rs_customer.id
        global_setting_date = EngageboostGlobalSettings.objects.filter(website_id=1,isdeleted='n',isblocked='n').first()
        if global_setting_date.timezone_id:
            global_setting_zone = EngageboostTimezones.objects.filter(id = global_setting_date.timezone_id).first()
            time_offset = global_setting_zone.offset
        else:
            time_offset = 0
        try:
            rs_order = EngageboostOrdermaster.objects.filter(id=order_id, customer_id=customer_id).first()
            shipment_status = ""
            if rs_order:
                order_data  = ViewOrderSerializer(rs_order)
                order_data  = order_data.data
                if order_data:
                    order_data["custom_order_id"] = int(order_data["custom_order_id"])
                    # for orderdata in order_data:
                    if int(order_data["order_status"]) == 99 and int(order_data["buy_status"]) == 1:
                        order_data["str_order_status"] = "Waiting Approval"
                    elif int(order_data["order_status"]) == 20 and int(order_data["buy_status"]) == 1:
                        order_data["str_order_status"] = "Approved"
                    elif int(order_data["order_status"]) == 0 and int(order_data["buy_status"]) == 1:
                        order_data["str_order_status"] = "Pending"
                    elif int(order_data["order_status"]) == 100 and int(order_data["buy_status"]) == 1:
                        order_data["str_order_status"] = "Processing"
                    elif int(order_data["order_status"]) == 1 and int(order_data["buy_status"]) == 1:
                        order_data["str_order_status"] = "Shipped"
                    elif int(order_data["order_status"]) == 2 and int(order_data["buy_status"]) == 1:
                        order_data["str_order_status"] = "Cancelled"
                    elif int(order_data["order_status"]) == 4 and int(order_data["buy_status"]) == 1:
                        order_data["str_order_status"] = "Completed"
                    elif int(order_data["order_status"]) == 5 and int(order_data["buy_status"]) == 1:
                        order_data["str_order_status"] = "Full Refund"
                    elif int(order_data["order_status"]) == 6 and int(order_data["buy_status"]) == 1:
                        order_data["str_order_status"] = "Partial Refund"
                    elif int(order_data["order_status"]) == 13 and int(order_data["buy_status"]) == 1:
                        order_data["str_order_status"] = "Delivered"
                    elif int(order_data["order_status"]) == 16 and int(order_data["buy_status"]) == 1:
                        order_data["str_order_status"] = "Closed"
                    elif int(order_data["order_status"]) == 18 and int(order_data["buy_status"]) == 1:
                        order_data["str_order_status"] = "Pending Service"
                    elif int(order_data["order_status"]) == 3 and int(order_data["buy_status"]) == 0:
                        order_data["str_order_status"] = "Abandoned"
                    elif int(order_data["order_status"]) == 999 and int(order_data["buy_status"]) == 0:
                        order_data["str_order_status"] = "Failed"
                    elif int(order_data["order_status"]) == 9999 and int(order_data["buy_status"]) == 1:
                        order_data["str_order_status"] = 'Hold'
                    else:
                        order_data["str_order_status"] = 'Invoiced'

                    paid_status = [4,5,6,16]
                    if order_data['paid_amount']>0 or int(order_data["order_status"]) in paid_status:
                        str_payment_status = "Paid"
                    else:
                        str_payment_status = "Unpaid"
                    order_data["str_payment_status"] = str_payment_status

                    created = datetime.strptime(str(order_data['created']), "%Y-%m-%dT%H:%M:%S.%fZ")
                    modified = datetime.strptime(str(order_data['modified']), "%Y-%m-%dT%H:%M:%S.%fZ")
                    if time_offset < 0:
                        time_offset = str(time_offset).split('-')
                        time_offset = time_offset[1]
                        order_data['created'] = created - timedelta(hours=float(time_offset))
                        order_data['modified'] = modified - timedelta(hours=float(time_offset))
                    else:
                        order_data['created'] = created + timedelta(hours=float(time_offset))
                        order_data['modified'] = modified + timedelta(hours=float(time_offset))

                if rs_order.shipment_id is not None and rs_order.shipment_id>0:
                    rs_shipment = EngageboostShipmentOrders.objects.filter(order_id=order_data["id"], shipment=rs_order.shipment_id).first()
                    if rs_shipment:
                        shipment_status = rs_shipment.shipment_status
                order_data['shipment_status'] = shipment_status
                # Loyalty
                loyalty_details = GetLoyaltyBalance(order_id, None)
                # order_data['loyalty_details'] = loyalty_details['data']
                loyalty_details = loyalty_details['data']
                # loyalty_data = loyalty_details['data'][0]['burn_loyalty']
                cr_amount = get_creadit_points(order_id)
                loyalty_details[0]['burn_loyalty']['loyalty_points_amount'] = loyalty_details[0]['burn_loyalty']['loyalty_amount']
                for loyalty_data in loyalty_details:
                    if float(loyalty_data['burn_loyalty']['remaning_earn_amount']) >0 and float(cr_amount['burn_point'])>0:
                        if float(loyalty_data['burn_loyalty']['remaning_earn_amount']) >float(cr_amount['burn_point']):
                            if loyalty_data['burn_loyalty']['max_loyalty_amount_use_limit'] is None:
                                loyalty_data['burn_loyalty']['max_loyalty_amount_use_limit'] = 0

                            if float(loyalty_data['burn_loyalty']['remaning_earn_amount']) > float(loyalty_data['burn_loyalty']['max_loyalty_amount_use_limit']):
                                loyalty_data['burn_loyalty']['loyalty_amount'] = loyalty_data['burn_loyalty']['max_loyalty_amount_use_limit']
                            else:
                                loyalty_data['burn_loyalty']['loyalty_amount'] = loyalty_data['burn_loyalty']['remaning_earn_amount']
                        else:
                            loyalty_data['burn_loyalty']['loyalty_amount'] = cr_amount['burn_point']
                    else:
                        loyalty_data['burn_loyalty']['loyalty_amount'] = 0

                order_data['loyalty_details'] = loyalty_data
                order_data['custom_order_id'] = str(order_data['custom_order_id'])
                str_status = status.HTTP_200_OK
                data = {
                    "status":str_status,
                    "msg": "success",
                    "data":order_data
                }
            else:
                str_status = status.HTTP_401_UNAUTHORIZED
                data = {
                    "status":str_status,
                    "api_status": "You are not authorise to view this order.",
                    "data":[]
                }
        except Exception as error:
            str_status = status.HTTP_417_EXPECTATION_FAILED
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in order update."}
        return Response(data, str_status)

class CartSync(APIView):
    def get(self, request, format=None):
        user                = request.user
        user_id             = user.id
        device_id           = request.META.get('HTTP_DEVICEID')
        rs_up = EngageboostTemporaryShoppingCarts.objects.filter(device_id=device_id, customer_id__isnull=True).update(customer_id=user_id)
        data = {
            "status":status.HTTP_200_OK,
            "msg":"success"
        }
        return Response(data)

class ApplyCouponCode(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        user                = request.user
        user_id             = user.id
        device_id           = request.META.get('HTTP_DEVICEID')
        warehouse_id        = request.META.get('HTTP_WAREHOUSE')
        if warehouse_id is None or warehouse_id == 0:
            warehouse_id = 2

        website_id = get_company_website_id_by_url()
        company_id = get_company_id_by_url()

        requestdata = request.data
        coupon_code = None
        if "coupon_code" in requestdata:
            coupon_code = requestdata["coupon_code"]

        if "warehouse_id" in requestdata:
            warehouse_id = requestdata["warehouse_id"]

        redeem_amount = 0
        rule_id = 0
        # Loyalty Points
        if "redeem_amount" in requestdata:
            redeem_amount = requestdata["redeem_amount"]

        if "rule_id" in requestdata:
            rule_id = requestdata["rule_id"]

        country_id = 221
        if "address_id" in requestdata and requestdata["address_id"]!="":
            pass
        else:
            requestdata["address_id"] = ""

        str_status = ""
        cartData = []
        if device_id is None and user_id is None:
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {
                "status":str_status,
                "msg":"User id or Device id is blank.",
                "data":[]
            }
        else:
            str_status = status.HTTP_200_OK
            country_id = None
            state_id = None
            post_code = None

            has_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
            customer_id = has_customer.id
            # rs_address = EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id).first()
            # if rs_address:
            #     country_id = rs_address.delivery_country
            #     state_id = rs_address.delivery_state
            #     post_code = rs_address.delivery_postcode
            if "address_id" in requestdata:
                address_id = requestdata["address_id"]
                if address_id:
                    rs_address = EngageboostCustomersAddressBook.objects.filter(id=address_id).first()
                    if rs_address:
                        country_id = rs_address.delivery_country
                        state_id = rs_address.delivery_state
                        post_code = rs_address.delivery_postcode
            else:
                if user_id is not None:
                    # rs_address = EngageboostCustomersAddressBook.objects.filter(customers_id=user_id, set_primary=1).first()
                    rs_address = EngageboostCustomersAddressBook.objects.filter(customers_id=rs_customer.id, set_primary=1).first()
                    if rs_address:
                        country_id = rs_address.delivery_country
                        state_id = rs_address.delivery_state
                        post_code = rs_address.delivery_postcode

            cartData = discount.GetCartDetails(company_id,website_id,customer_id, device_id, None, country_id, state_id, post_code, user_id,None,coupon_code, warehouse_id)
            cartData = cartData.data

            minimum_order_amount = 0
            minimum_order_amount_check = 'yes'
            rs_min_order = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).first()
            if float(rs_min_order.min_order_amount)>0:
                minimum_order_amount = float(rs_min_order.min_order_amount)
            else:
                rs_global_settings = EngageboostGlobalSettings.objects.filter(isblocked='n', isdeleted='n', website_id= website_id).first()
                if rs_global_settings and float(rs_global_settings.min_order_amount)>0:
                    minimum_order_amount = float(rs_global_settings.min_order_amount)

            # if float(cartData['orderamountdetails'][0]['sub_total'])<float(minimum_order_amount):
            #     minimum_order_amount_check = 'no'


            if float(redeem_amount) > 0:
                net_total = float(cartData['orderamountdetails'][0]['sub_total']) + float(cartData['orderamountdetails'][0]['cart_discount'])
                if float(cartData['orderamountdetails'][0]['sub_total'])>float(redeem_amount):
                    cartData['orderamountdetails'][0]['sub_total'] = float(net_total)
                    cartData['orderamountdetails'][0]['balance_due'] = float(cartData['orderamountdetails'][0]['balance_due']) - float(redeem_amount)
                    cartData['orderamountdetails'][0]['applied_loyalty_amount'] = redeem_amount
                    cartData['orderamountdetails'][0]['grand_total'] = float(net_total) +float(cartData['orderamountdetails'][0]['shipping_charge'])- float(redeem_amount)-float(cartData['orderamountdetails'][0]['cart_discount'])
                else:
                    redeem_amount = float(cartData['orderamountdetails'][0]['sub_total'])
                    cartData['orderamountdetails'][0]['sub_total'] = float(net_total)
                    cartData['orderamountdetails'][0]['balance_due'] = float(cartData['orderamountdetails'][0]['balance_due']) - float(redeem_amount)
                    cartData['orderamountdetails'][0]['applied_loyalty_amount'] = redeem_amount
                    cartData['orderamountdetails'][0]['grand_total'] = float(net_total) + float(cartData['orderamountdetails'][0]['shipping_charge'])- float(redeem_amount)-float(cartData['orderamountdetails'][0]['cart_discount'])
            else:
                if cartData["applied_coupon"] and int(cartData["applied_coupon"][0]['disc_type']) == 7 and int(
                        cartData["applied_coupon"][0]['status']) == 1:
                    cartData['orderamountdetails'][0]['sub_total'] = float(
                        cartData['orderamountdetails'][0]['sub_total'])
                    cartData['orderamountdetails'][0]['grand_total'] = float(
                        cartData['orderamountdetails'][0]['sub_total']) - float(
                        cartData['orderamountdetails'][0]['cart_discount']) + float(
                        cartData['orderamountdetails'][0]['shipping_charge']) - float(redeem_amount)
                else:
                    cartData['orderamountdetails'][0]['sub_total'] = float(
                        cartData['orderamountdetails'][0]['sub_total']) + float(
                        cartData['orderamountdetails'][0]['cart_discount'])
                    cartData['orderamountdetails'][0]['grand_total'] = float(
                        cartData['orderamountdetails'][0]['sub_total']) - float(
                        cartData['orderamountdetails'][0]['cart_discount']) + float(
                        cartData['orderamountdetails'][0]['shipping_charge']) - float(redeem_amount)

            if float(cartData['orderamountdetails'][0]['sub_total']) < float(minimum_order_amount):
                minimum_order_amount_check = 'no'

            data = {
                "status":str_status,
                "data":cartData,
                "minimum_order_amount":minimum_order_amount,
                "minimum_order_amount_check":minimum_order_amount_check
            }
        return Response(data,str_status)

#----Test----#
class ApplyCouponCodeTest(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        user                = request.user
        user_id             = user.id
        device_id           = request.META.get('HTTP_DEVICEID')
        warehouse_id        = request.META.get('HTTP_WAREHOUSE')
        if warehouse_id is None or warehouse_id == 0:
            warehouse_id = 2

        website_id = get_company_website_id_by_url()
        company_id = get_company_id_by_url()

        requestdata = request.data
        coupon_code = None
        if "coupon_code" in requestdata:
            coupon_code = requestdata["coupon_code"]

        if "warehouse_id" in requestdata:
            warehouse_id = requestdata["warehouse_id"]

        redeem_amount = 0
        rule_id = 0
        # Loyalty Points
        if "redeem_amount" in requestdata:
            redeem_amount = requestdata["redeem_amount"]

        if "rule_id" in requestdata:
            rule_id = requestdata["rule_id"]


        str_status = ""
        cartData = []
        if device_id is None and user_id is None:
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {
                "status":str_status,
                "msg":"User id or Device id is blank.",
                "data":[]
            }
        else:
            str_status = status.HTTP_200_OK
            country_id = None
            state_id = None
            post_code = None

            has_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
            customer_id = has_customer.id
            # rs_address = EngageboostCustomersAddressBook.objects.filter(customers_id=user_id).first()
            rs_address = EngageboostCustomersAddressBook.objects.filter(customers_id=customer_id).first()

            #------Binayak Start 23-12-2020-----#
            # if rs_address:
            #     country_id = rs_address.delivery_country
            #     state_id = rs_address.delivery_state
            #     post_code = rs_address.delivery_postcode

            #------Binayak Start 11-12-2020-----#
            # else:
            warehouse_zone = EngageboostZoneMasters.objects.filter(warehouse_id=warehouse_id, isdeleted='n',
                                                                   isblocked='n').first()
            if warehouse_zone:
                country_id = warehouse_zone.country_id
                state_id = warehouse_zone.state_id
                post_code = warehouse_zone.zipcode

            # ------Binayak End 11-12-2020-----#

            cartData = discount.GetCartDetails(company_id,website_id,customer_id, device_id, None, country_id, state_id, post_code, user_id,None,coupon_code, warehouse_id)
            cartData = cartData.data

            minimum_order_amount = 0
            minimum_order_amount_check = 'yes'
            rs_min_order = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).first()
            if float(rs_min_order.min_order_amount)>0:
                minimum_order_amount = float(rs_min_order.min_order_amount)
            else:
                rs_global_settings = EngageboostGlobalSettings.objects.filter(isblocked='n', isdeleted='n', website_id= website_id).first()
                if rs_global_settings and float(rs_global_settings.min_order_amount)>0:
                    minimum_order_amount = float(rs_global_settings.min_order_amount)

            # -----Binayak Start-----#
            # if float(cartData['orderamountdetails'][0]['sub_total'])<float(minimum_order_amount):
            #     minimum_order_amount_check = 'no'
            # -----Binayak End-----#


            if float(redeem_amount) > 0:
                net_total = float(cartData['orderamountdetails'][0]['sub_total']) + float(cartData['orderamountdetails'][0]['cart_discount'])
                if float(cartData['orderamountdetails'][0]['sub_total'])>float(redeem_amount):
                    cartData['orderamountdetails'][0]['sub_total'] = float(net_total)
                    cartData['orderamountdetails'][0]['balance_due'] = float(cartData['orderamountdetails'][0]['balance_due']) - float(redeem_amount)
                    cartData['orderamountdetails'][0]['applied_loyalty_amount'] = redeem_amount
                    cartData['orderamountdetails'][0]['grand_total'] = float(net_total) +float(cartData['orderamountdetails'][0]['shipping_charge'])- float(redeem_amount)-float(cartData['orderamountdetails'][0]['cart_discount'])
                else:
                    redeem_amount = float(cartData['orderamountdetails'][0]['sub_total'])
                    cartData['orderamountdetails'][0]['sub_total'] = float(net_total)
                    cartData['orderamountdetails'][0]['balance_due'] = float(cartData['orderamountdetails'][0]['balance_due']) - float(redeem_amount)
                    cartData['orderamountdetails'][0]['applied_loyalty_amount'] = redeem_amount
                    cartData['orderamountdetails'][0]['grand_total'] = float(net_total) + float(cartData['orderamountdetails'][0]['shipping_charge'])- float(redeem_amount)-float(cartData['orderamountdetails'][0]['cart_discount'])
            else:
                # -----Binayak Start-----#
                if cartData["applied_coupon"] and int(cartData["applied_coupon"][0]['disc_type'])==7 and int(cartData["applied_coupon"][0]['status'])==1:
                    cartData['orderamountdetails'][0]['sub_total'] = float(cartData['orderamountdetails'][0]['sub_total'])
                    cartData['orderamountdetails'][0]['grand_total'] = float(cartData['orderamountdetails'][0]['sub_total']) - float(cartData['orderamountdetails'][0]['cart_discount']) + float(cartData['orderamountdetails'][0]['shipping_charge'])- float(redeem_amount)
                else:
                    cartData['orderamountdetails'][0]['sub_total'] = float(cartData['orderamountdetails'][0]['sub_total']) + float(cartData['orderamountdetails'][0]['cart_discount'])
                    cartData['orderamountdetails'][0]['grand_total'] = float(cartData['orderamountdetails'][0]['sub_total']) - float(cartData['orderamountdetails'][0]['cart_discount']) + float(cartData['orderamountdetails'][0]['shipping_charge'])- float(redeem_amount)


            if float(cartData['orderamountdetails'][0]['sub_total'])<float(minimum_order_amount):
                minimum_order_amount_check = 'no'
            # -----Binayak End-----#

            data = {
                "status":str_status,
                "data":cartData,
                "minimum_order_amount":minimum_order_amount,
                "minimum_order_amount_check":minimum_order_amount_check
            }
        return Response(data,str_status)
#----Test----#


class CartSummary(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        user                = request.user
        user_id             = user.id
        device_id           = request.META.get('HTTP_DEVICEID')
        warehouse_id        = request.META.get('HTTP_WAREHOUSE')
        website_id = get_company_website_id_by_url()
        company_id = get_company_id_by_url()
        requestdata = request.data
        country_id = None
        state_id = None
        post_code = None

        rs_customer = EngageboostCustomers.objects.filter(auth_user_id = user_id).first()

        if "warehouse_id" in requestdata:
            warehouse_id = requestdata["warehouse_id"]
        else:
            warehouse_id = warehouse_id

        coupon_code = None
        if "coupon_code" in requestdata:
            coupon_code = requestdata["coupon_code"]
        country_id = 221
        if "address_id" in requestdata and requestdata["address_id"]!="":
            pass
        else:
            requestdata["address_id"] = ""

        if "address_id" in requestdata:
            address_id = requestdata["address_id"]
            if address_id:
                rs_address = EngageboostCustomersAddressBook.objects.filter(id=address_id).first()
                if rs_address:
                    country_id = rs_address.delivery_country
                    state_id = rs_address.delivery_state
                    post_code = rs_address.delivery_postcode
        else:
            if user_id is not None:
                # rs_address = EngageboostCustomersAddressBook.objects.filter(customers_id=user_id, set_primary=1).first()
                rs_address = EngageboostCustomersAddressBook.objects.filter(customers_id=rs_customer.id, set_primary=1).first()
                if rs_address:
                    country_id = rs_address.delivery_country
                    state_id = rs_address.delivery_state
                    post_code = rs_address.delivery_postcode

        str_status = ""
        cartData = []
        if device_id is None and user_id is None:
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {
                "status":str_status,
                "msg":"User id or Device id is blank.",
                "data":[]
            }
        else:
            str_status = status.HTTP_200_OK
            has_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
            customer_id = has_customer.id
            cartData = discount.GetCartDetails(company_id,website_id,customer_id, device_id, 6, country_id, state_id, post_code, None, None,coupon_code, warehouse_id)
            cartData = cartData.data
            usable_loyalty = loyalty.get_creadit_points(cartData, user_id)
            remain_loyalty = loyalty.GetUserLoyaltyBalance(user_id)
            burn_amount = 0
            if float(remain_loyalty) >0 and float(usable_loyalty['burn_point'])>0:
                if float(remain_loyalty) >float(usable_loyalty['burn_point']):
                    burn_amount = round(usable_loyalty['burn_point'])
                else:
                    if float(remain_loyalty) > float(usable_loyalty['redeem_limit']):
                        burn_amount = round(usable_loyalty['redeem_limit'],2)
                    else:
                        burn_amount = round(remain_loyalty,2)
            else:
                burn_amount = 0
            loyalty_details = {}
            loyalty_details.update({"usable_loyalty":burn_amount,"remain_loyalty":remain_loyalty,"rule_id":usable_loyalty['rule_id'],"redeem_limit":usable_loyalty['redeem_limit']})
            cartData.update({"loyalty_details":loyalty_details})
            minimum_order_amount = 0
            minimum_order_amount_check = 'yes'

            rs_min_order = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).first()
            if float(rs_min_order.min_order_amount)>0:
                minimum_order_amount = float(rs_min_order.min_order_amount)
            else:
                rs_global_settings = EngageboostGlobalSettings.objects.filter(isblocked='n', isdeleted='n', website_id= website_id).first()
                if rs_global_settings and float(rs_global_settings.min_order_amount)>0:
                    minimum_order_amount = float(rs_global_settings.min_order_amount)

            if float(cartData['orderamountdetails'][0]['sub_total'])<float(minimum_order_amount):
                minimum_order_amount_check = 'no'

            data = {
                "status":str_status,
                "data":cartData,
                "usable_loyalty":burn_amount,
                "remain_loyalty":remain_loyalty,
                "rule_id":usable_loyalty['rule_id'],
                "redeem_limit":usable_loyalty['redeem_limit'],
                "minimum_order_amount":minimum_order_amount,
                "minimum_order_amount_check":minimum_order_amount_check
            }
        return Response(data,str_status)

#----Test----#
class CartSummaryTest(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        user                = request.user
        user_id             = user.id
        device_id           = request.META.get('HTTP_DEVICEID')
        warehouse_id        = request.META.get('HTTP_WAREHOUSE')
        website_id = get_company_website_id_by_url()
        company_id = get_company_id_by_url()
        requestdata = request.data
        country_id = None
        state_id = None
        post_code = None

        rs_customer = EngageboostCustomers.objects.filter(auth_user_id = user_id).first()


        if "warehouse_id" in requestdata:
            warehouse_id = requestdata["warehouse_id"]
        else:
            warehouse_id = warehouse_id

        coupon_code = None
        if "coupon_code" in requestdata:
            coupon_code = requestdata["coupon_code"]
        country_id = 221
        if "address_id" in requestdata:
            address_id = requestdata["address_id"]
            if address_id:
                rs_address = EngageboostCustomersAddressBook.objects.filter(id=address_id).first()
                if rs_address:
                    country_id = rs_address.delivery_country
                    state_id = rs_address.delivery_state
                    post_code = rs_address.delivery_postcode
        else:
            # if user_id is not None:
            #
            #     # rs_address = EngageboostCustomersAddressBook.objects.filter(customers_id=user_id, set_primary=1).first()
            #     rs_address = EngageboostCustomersAddressBook.objects.filter(customers_id=rs_customer.id, set_primary=1).first()
            #     if rs_address:
            #         country_id = rs_address.delivery_country
            #         state_id = rs_address.delivery_state
            #         post_code = rs_address.delivery_postcode

                #------Binayak Start 22-12-2020------#
                # else:
            warehouse_zone = EngageboostZoneMasters.objects.filter(warehouse_id=warehouse_id, isdeleted='n', isblocked='n').first()
            if warehouse_zone:
                country_id = warehouse_zone.country_id
                state_id = warehouse_zone.state_id
                post_code = warehouse_zone.zipcode
                        # shipping_master = EngageboostShippingMastersSettings.objects.filter(zone_id=warehouse_zone.id, isdeleted='n', isblocked='n').first()
                        # if shipping_master:
                        #     shipping_amount = shipping_master.flat_price
                        # else:
                        #     GlobalSettings_qs = EngageboostGlobalSettings.objects.filter(isblocked='n',
                        #                                                                  isdeleted='n').first()
                        #     shipping_amount = GlobalSettings_qs.shipping_charge
                # ------Binayak Start 22-12-2020------#

        str_status = ""
        cartData = []
        if device_id is None and user_id is None:
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {
                "status":str_status,
                "msg":"User id or Device id is blank.",
                "data":[]
            }
        else:
            str_status = status.HTTP_200_OK
            has_customer = EngageboostCustomers.objects.filter(auth_user_id=user_id).first()
            customer_id = has_customer.id
            cartData = discount.GetCartDetails(company_id,website_id,customer_id, device_id, 6, country_id, state_id, post_code, None, None,coupon_code, warehouse_id)
            cartData = cartData.data
            usable_loyalty = loyalty.get_creadit_points(cartData, user_id)
            remain_loyalty = loyalty.GetUserLoyaltyBalance(user_id)
            burn_amount = 0
            if float(remain_loyalty) >0 and float(usable_loyalty['burn_point'])>0:
                if float(remain_loyalty) >float(usable_loyalty['burn_point']):
                    burn_amount = round(usable_loyalty['burn_point'])
                else:
                    if float(remain_loyalty) > float(usable_loyalty['redeem_limit']):
                        burn_amount = round(usable_loyalty['redeem_limit'],2)
                    else:
                        burn_amount = round(remain_loyalty,2)
            else:
                burn_amount = 0
            loyalty_details = {}
            loyalty_details.update({"usable_loyalty":burn_amount,"remain_loyalty":remain_loyalty,"rule_id":usable_loyalty['rule_id'],"redeem_limit":usable_loyalty['redeem_limit']})
            cartData.update({"loyalty_details":loyalty_details})
            minimum_order_amount = 0
            minimum_order_amount_check = 'yes'

            rs_min_order = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).first()
            if float(rs_min_order.min_order_amount)>0:
                minimum_order_amount = float(rs_min_order.min_order_amount)
            else:
                rs_global_settings = EngageboostGlobalSettings.objects.filter(isblocked='n', isdeleted='n', website_id= website_id).first()
                if rs_global_settings and float(rs_global_settings.min_order_amount)>0:
                    minimum_order_amount = float(rs_global_settings.min_order_amount)

            if float(cartData['orderamountdetails'][0]['sub_total'])<float(minimum_order_amount):
                minimum_order_amount_check = 'no'

            data = {
                "status":str_status,
                "data":cartData,
                "usable_loyalty":burn_amount,
                "remain_loyalty":remain_loyalty,
                "rule_id":usable_loyalty['rule_id'],
                "redeem_limit":usable_loyalty['redeem_limit'],
                "minimum_order_amount":minimum_order_amount,
                "minimum_order_amount_check":minimum_order_amount_check
            }
        return Response(data,str_status)
#----Test----#

class ViewOrderDetailsPayment(APIView):
    permission_classes = []
    def get(self, request, order_id, format=None):
        order_id = urllib.parse.unquote(order_id)
        decode = base64.b64decode(order_id)
        d2 = decode.decode("UTF-8")
        fstrip = d2[3:]
        lstrip = fstrip[:-3]

        # now_utc = datetime.now(timezone.utc).astimezone()
        now_utc = datetime.now(timezone('UTC')).astimezone(timezone('Asia/Dubai'))
        str_status = ""
        try:
            rs_order    = EngageboostOrdermaster.objects.filter(id=lstrip).first()
            #print(rs_order.query)
            if rs_order:
                shipment_status = ""

            if rs_order:
                order_data  = ViewOrderSerializer(rs_order)
                order_data  = order_data.data
                if rs_order.shipment_id is not None and rs_order.shipment_id>0:
                    rs_shipment = EngageboostShipmentOrders.objects.filter(shipment=rs_order.shipment_id).first()
                    if rs_shipment:
                        shipment_status = rs_shipment.shipment_status

                order_data['shipment_status'] = shipment_status
                str_status = status.HTTP_200_OK
                data = {
                    "status":str_status,
                    "msg": "success",
                    "data":order_data
                }
            else:
                str_status = status.HTTP_401_UNAUTHORIZED
                data = {
                    "status":str_status,
                    "api_status": "You are not authorise to view this order.",
                    "data":[]
                }
        except Exception as error:
            str_status = status.HTTP_417_EXPECTATION_FAILED
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in order update."}

        return Response(data, str_status)

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
def get_creadit_points(order_id):   
    order_id = order_id
    rs_order_details    = EngageboostOrdermaster.objects.filter(id = order_id ).first()
    rs_order_products   = EngageboostOrderProducts.objects.filter(order_id = order_id).values_list('product_id', flat = True)
    rs_prod_cat         = EngageboostProductCategories.objects.filter(product_id__in = rs_order_products).values_list('category_id', flat = True)

    product_ids     = list(set(rs_order_products))
    category_ids    = list(set(rs_prod_cat))
    customer_id     = rs_order_details.customer_id
    price           = rs_order_details.net_amount
    custom_order_id = rs_order_details.custom_order_id

    earn_points         = 0
    category_flag           = False
    product_flag            = False
    coustomer_flag          = False
    customer_group_flag     = False
    order_amount            = False
    flag = False
    # print(request)
    today = django.utils.timezone.now()
    credit_rs = EngageboostCreditPoint.objects.filter(isdeleted='n', isblocked='n', loyal_end_date__gte=today, loyal_type="burn").last()
    # credit_data = EngageboostCreditPointSerializer(credit_rs)
    # if credit_data and credit_data is not None:
    if credit_rs and credit_rs is not None:
        credit_data = EngageboostCreditPointSerializer(credit_rs)
        credit_data = credit_data.data
        if credit_data["CreditPointConditions"]:
            if len(credit_data["CreditPointConditions"]) > 0 :
                for creadit_point in credit_data["CreditPointConditions"]:
                    if creadit_point["fields"] == 0:  ### For Category Checking
                        all_category_ids = creadit_point["all_category_id"].split(',')
                        result = common_data(all_category_ids, category_ids, creadit_point["condition"])
                        category_flag = result
                        flag = result
                        # print(result)

                    if creadit_point["fields"] == 13633:  ### For SKU Checking
                        all_product_ids = creadit_point["all_product_id"].split(',')
                        result = common_data(all_product_ids, product_ids, creadit_point["condition"])
                        product_flag = result
                        # print(result)

                    if creadit_point["fields"] == -1:  ### For Order Amount Checking
                        order_amount = creadit_point["value"]
                        condition = str(creadit_point["condition"])
                        # print('Order Amount', condition)
                        if condition == '<=':
                            if int(order_amount) <= int(price):
                                order_amount = True
                        if condition == '>=':
                            if int(order_amount) >= int(price):
                                order_amount = True
                        if condition == '==':
                            if int(order_amount) == int(price):
                                order_amount = True
                        if condition == '!=':
                            if int(order_amount) != int(price):
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
            # if customer_group_flag == True and coustomer_flag == True and order_amount == True and product_flag == True and category_flag == True:
            if flag == True:
                if credit_data["applied_as"] == 'percentage':
                    earn_points = ((float(price) / float(100)) * float(credit_data["points"]))
                if credit_data["applied_as"] == 'fixed':
                    earn_points_in_price = (float(price) / float(credit_data["per_rupees"]))
                    earn_points = float(credit_data["points"]) * float(earn_points_in_price)
                    # ((float(price) / float(credit_data["per_rupees"])) * float(credit_data["points"]))
                valid_to = django.utils.timezone.now() + timedelta(days=credit_data["loyalty_expire_days"])

        data = {"status":1,"burn_point":earn_points}
    else:
        data = {"status":0,"burn_point":0}
    return data

# get_creadit_points()

def save_burn_points(request):
    if request and int(request['order_id'])>0:
        check_exist = EngageboostCustomerLoyaltypoints.objects.filter(order_id=request['order_id'], status='burn').count()
        if check_exist>0:
            save_loyalty_points = EngageboostCustomerLoyaltypoints.objects.filter(order_id=request['order_id'], status='burn').update(**request)
            data={"status":1,"message": "loyelty points save successfully."}
        else:
            save_loyalty_points = EngageboostCustomerLoyaltypoints.objects.create(**request)
            data={"status":1,"message": "loyelty points save successfully."}
        return data

def GetUserLoyaltyBalance(user_id):
    now_utc = datetime.now(timezone('UTC')).astimezone(timezone('Asia/Dubai'))
    to_day      = now_utc.strftime('%Y-%m-%d')
    rs_loyalty = EngageboostCustomerLoyaltypoints.objects.filter(customer_id =user_id, valid_form__date__gte=to_day, expiry_date__date__gte=to_day).annotate(total_amount = Sum('amount')).values('status', 'total_amount')
    balance_amount = 0
    earn_amount = 0
    burn_amount = 0
    if rs_loyalty:
        for loyalty_amount in rs_loyalty:
            if loyalty_amount['status'].lower() == 'earn':
                earn_amount = loyalty_amount['total_amount']
            if loyalty_amount['status'].lower() == 'burn':
                burn_amount = loyalty_amount['total_amount']
        if float(earn_amount) > float(burn_amount):
            balance_amount = float(earn_amount) - float(burn_amount)
    return balance_amount
    # print(balance_amount)

class LoyaltyPointsLog(APIView):
    def get(self, request, format=None):
        user = request.user
        user_id = user.id
        str_status = ""
        rs_loyalty = EngageboostCustomerLoyaltypoints.objects.filter(customer_id = user_id).order_by('created', 'id')
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

def GetLoyaltyBalance(order_id , web_id = None):
    website_id = 1
    if web_id is not None:
        website_id = web_id

    loyelty = []
    # requestdata = request.data
    # user = request.user
    # user_id = user.id
    # order_id = requestdata["order_id"]
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
    return data

# END LOYALTY POINTS


def ChangeCouponCodeStatus(applied_coupon = None, warehouse_id = None):
    applied_coupon = applied_coupon
    if warehouse_id is None:
        warehouse_id = 4
    print("warehouse_id==", warehouse_id)
    if applied_coupon is not None:
        discount_array = discount.generate_discount_conditions_coupon(1,None,applied_coupon, warehouse_id)
        print("discount_array====", json.dumps(discount_array))
        if discount_array:
            if "status" in discount_array[0] and discount_array[0]["status"]==0:
                pass
            else:
                discount_array = discount_array[0]
                if discount_array['coupon_type'] ==1:
                    if discount_array['has_multiplecoupons'] == 'y':
                        # multiple discount coupon single user scenario ...
                        # if discount_array['DiscountMastersCoupons'] and discount_array['DiscountMastersCoupons']['is_used']=='n':
                        if discount_array['DiscountMasterCoupon'] and discount_array['DiscountMasterCoupon']['is_used']=='n':
                            update_array = {
                                "is_used":'y'
                            }
                            EngageboostDiscountMastersCoupons.objects.filter(id=discount_array['DiscountMasterCoupon']['id']).update(**update_array)
                    else:
                        update_array = {
                            "used_coupon":1
                        }
                        EngageboostDiscountMasters.objects.filter(id=discount_array['id']).update(**update_array)

class CartCount(APIView):
    permission_classes = []
    def get(self, request, format=None):
        requestdata = request.data
        user                = request.user
        user_id             = user.id
        website_id = request.META.get('HTTP_WID')
        device_id           = request.META.get('HTTP_DEVICEID')
        data_count = 0
        rs_cart = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id)
        if user_id and user_id>0:
            rs_cart = rs_cart.filter(customer_id=user_id)
        elif device_id and device_id is not None:
            rs_cart = rs_cart.filter(device_id=device_id).exclude(customer_id__isnull=False)

        cart_count = rs_cart.count()
        data = {"cart_count":cart_count}
        return Response(data)


class add_to_cart(APIView):
    def get_queryset(self):
        # print('Debug: I am starting...\n\n\n\n')
        # do a lot of things filtering data from Django models by some information on neo4j and saving data in the queryset...
        return self.queryset

    permission_classes = []
    def post(self, request, *args, **kwargs):

        website_id = get_company_website_id_by_url()
        company_id = get_company_id_by_url()
        warehouse_id           = request.META.get('HTTP_WAREHOUSE')
        data        = []
        returnData  = []
        cartData    = []
        user_id     = 0
        saved_amount = 0
        total_amount = 0
        total_cart_count    = 0

        requestdata = request.data
        user                = request.user
        user_id             = user.id
        device_id   = None
        customer_id = None
        product_id  = 0
        quantity    = 0
        cartdata    = {}
        msg   		= ""
        custom_field_name = None
        custom_field_value = None
        is_age_verification =""
        isRestrected = False
        if warehouse_id is None:
            if "warehouse_id" in requestdata:
                warehouse_id = requestdata["warehouse_id"]
            else:
                warehouse_id = 34

        if "device_id" in requestdata: device_id = requestdata['device_id']
        # if "customer_id" in requestdata: customer_id = requestdata['customer_id']
        if "product_id" in requestdata: product_id = requestdata['product_id']
        if "custom_field_name" in requestdata: custom_field_name = requestdata['custom_field_name']
        if "custom_field_value" in requestdata: custom_field_value = requestdata['custom_field_value']
        if "quantity" in requestdata: quantity = requestdata['quantity']
        if user_id is not None:
            rs_customer = EngageboostCustomers.objects.filter(auth_user_id = user_id).first()
            if rs_customer:
                customer_id = rs_customer.id
        year_check = None
        if "year_check" in requestdata and requestdata['year_check'] !='':
            year_check  = requestdata ['year_check']
        # if device_id  and customer_id:
        if device_id or customer_id:
            # product_count = EngageboostProducts.objects.filter(isdeleted='n', isblocked='n', status='n', default_price__gt=0, id=product_id).count()
            product_count = EngageboostProducts.objects.filter(isdeleted='n', isblocked='n', id=product_id).count()
            # print("product_count+++++++++++", product_count.query)
            if product_count <=0:
                status = 0
                ack = "fail"
                msg = "Product not available."

            else:
                RestrectedCategory =[386,397]
                if year_check != "Y":
                    productCategories = EngageboostProductCategories.objects.filter(isdeleted='n', isblocked='n', product_id=product_id).first()

                    if productCategories:
                        if productCategories.category.parent_id==0:
                            category_id = productCategories.category.id
                        else:
                            category_id = productCategories.category.parent_id
                        if category_id in RestrectedCategory:
                            isRestrected = True
                            status = 0
                            ack = "fail"
                            # msg = "The sale and delivery of tobacco based products are prohibited by law to persons under the age of 18."
                            msg = "The sale and delivery of tobacco products are prohibited by law to people under the age of 18."
                            is_age_verification = 'False'
                if not isRestrected or year_check == "Y":
                    if quantity>0:
                        dataProductAvailability = check_instock_quantity(product_id,quantity,warehouse_id,customer_id,device_id)
                        if dataProductAvailability['ack']:
                            cartCount = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id ).all()
                            # if customer_id and  customer_id is not None and customer_id>0:
                            if user_id and  user_id is not None and user_id>0:
                                cartCount = cartCount.filter(customer_id=user_id)
                            elif device_id:
                                # cartCount = cartCount.filter(customer_id=0, device_id=device_id)
                                cartCount = cartCount.filter(device_id=device_id, customer_id__isnull=True)
                            cartCount = cartCount.count()
                            if cartCount<=0:
                                if quantity<=0:
                                    status = 0
                                    ack = 'fail'
                                    msg = 'provide quantity to be added.'
                                else:
                                    cartArr = {}
                                    # cartArr.update({"website_id":website_id, "device_id":device_id, "product_id":product_id, "quantity":quantity})
                                    cartArr.update(
                                        {"website_id": website_id, "device_id": device_id, "product_id": product_id,
                                         "quantity": quantity, "custom_field_name": custom_field_name,
                                         "custom_field_value": custom_field_value})
                                    if user_id and user_id is not None:
                                        cartArr.update({"customer_id":user_id})
                                    insert_id = EngageboostTemporaryShoppingCarts.objects.create(**cartArr)
                                    if insert_id.id>0:
                                        status = 1
                                        ack = 'success'
                                        msg = 'Product added to cart.'
                                    else:
                                        status = 0
                                        ack = 'fail'
                                        msg = 'Product not added to cart.'
                            else:
                                if quantity>0:
                                    cartArr = {}
                                    if customer_id and customer_id is not None:
                                        # EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, device_id=device_id, customer_id=user_id, product_id=product_id).delete()
                                        # cartArr.update({"website_id":website_id, "device_id":device_id, "product_id":product_id, "quantity":quantity, "customer_id":user_id})
                                        # insert_id = EngageboostTemporaryShoppingCarts.objects.create(**cartArr)
                                        # update_id = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, customer_id=user_id, product_id=product_id).update(quantity=quantity,device_id=device_id)
                                        update_id = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, customer_id=user_id, product_id=product_id).update(quantity=quantity)
                                    elif device_id:
                                        # EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, device_id=device_id, customer_id=user_id, product_id=product_id).delete()
                                        # cartArr.update({"website_id":website_id, "device_id":device_id, "product_id":product_id, "quantity":quantity})
                                        # insert_id = EngageboostTemporaryShoppingCarts.objects.create(**cartArr)
                                        update_id = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, device_id=device_id, product_id=product_id, customer_id__isnull=True).update(quantity=quantity)
                                    status = 1
                                    ack = 'success'
                                    msg = 'Cart quantity updated.'
                                else:
                                    if customer_id and customer_id>0:
                                        EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, customer_id=user_id ).delete()
                                    elif device_id:
                                        EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, device_id=device_id,customer_id__isnull=True).delete()
                                    status = 1
                                    ack = 'success'
                                    msg = 'Product deleted from cart.'
                        else:
                            status = 0
                            ack = 'fail'
                            msg = dataProductAvailability['msg']
                    else:
                        cartCount = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id ).all()
                        if customer_id and customer_id>0:
                            cartCount = cartCount.filter(customer_id=user_id)
                        elif device_id:
                            cartCount = cartCount.filter(device_id=device_id, customer_id__isnull=True)
                        cartCount = cartCount.count()

                        if cartCount>0:
                            if customer_id and customer_id>0:
                                EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, customer_id=user_id ).delete()
                            elif device_id:
                                EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, device_id=device_id,customer_id__isnull=True).delete()
                            status = 1
                            ack = 'success'
                            msg = 'Product deleted from cart.'
                        else:
                            status = 0
                            ack = 'fail'
                            msg = "Quantity should not be 0."
        else:
            status = 0,
            ack = "fail"
            msg = "User not Found"
        if not isRestrected or year_check == "Y":
            # cart_data = discount.GetCartDetails(1,1,customer_id, device_id, None, None,None,None,user_id,None,None,warehouse_id)
            if customer_id or device_id:
                cart_data = discount.GetCartDetails(1,1,customer_id, device_id, None, None,None,None,user_id,None,None,warehouse_id,'addtocart')
                cartdata = cart_data.data
            else:
                cart_data = []
                cartdata['cartdetails']=[]

            return_details = []
            if cart_data:
                cnt = 0
                for i in range(len(cartdata['cartdetails'])):
                  if int(cartdata['cartdetails'][i]['id']) == int(product_id):
                      cartdata['cartdetails'][i]['new_default_price'] = float(cartdata['cartdetails'][i]['new_default_price']) + float(cartdata['cartdetails'][i]['tax_price'])
                      cartdata['cartdetails'][i]['new_default_price_unit'] = float(cartdata['cartdetails'][i]['new_default_price_unit']) + float(cartdata['cartdetails'][i]['tax_price_unit'])
                      return_details.append(cartdata['cartdetails'][i])
            cartdata['cartdetails'] = return_details

        total_cart_count = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id).all()
        if customer_id and customer_id > 0:
            total_cart_count = total_cart_count.filter(customer_id=user_id)
        elif device_id:
            total_cart_count = total_cart_count.filter(device_id=device_id, customer_id__isnull=True)
        total_cart_count = total_cart_count.count()
        data = {
            "status": status,
            "ack": ack,
            "msg": msg,
            "is_age_verification": is_age_verification,
            # "cart_data":cart_data.data
            "cart_data": cartdata,
            "total_cart_count": total_cart_count
        }
        # data = {
        #     "status":status,
        #     "ack":ack,
        #     "msg":msg,
        #     "is_age_verification":is_age_verification,
        #     # "cart_data":cart_data.data
        #     "cart_data":cartdata
        # }
        return Response(data)