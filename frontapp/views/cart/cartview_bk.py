from django.shortcuts import render
from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# import datetime
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
from frontapp.views.sitecommon import common_functions


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


class add_to_cart(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):

        website_id = get_company_website_id_by_url()
        company_id = get_company_id_by_url()
        
        data        = []
        returnData  = []
        cartData    = []
        user_id     = 0
        saved_amount = 0
        total_amount = 0
        total_cart_count    = 0

        requestdata = request.data
        device_id   = None
        customer_id = None
        product_id  = 0
        quantity    = 0
        if "device_id" in requestdata: device_id = requestdata['device_id']
        if "customer_id" in requestdata: customer_id = requestdata['customer_id']
        if "product_id" in requestdata: product_id = requestdata['product_id']
        if "quantity" in requestdata: quantity = requestdata['quantity']

        # if device_id  and customer_id:
        if device_id:
            product_count = EngageboostProducts.objects.filter(isdeleted='n', isblocked='n', status='n', default_price__gt=0, id=product_id).count()
            if product_count <=0:
                status = 0
                ack = "fail"
                msg = "Product not available."
            else:
                if quantity>0:
                    dataProductAvailability = check_instock_quantity(product_id,quantity,customer_id,device_id)
                    if dataProductAvailability['ack']:
                        cartCount = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id ).all()
                        if customer_id and  customer_id is not None and customer_id>0:
                            cartCount = cartCount.filter(customer_id=customer_id)
                        if device_id:
                            # cartCount = cartCount.filter(customer_id=0, device_id=device_id)
                            cartCount = cartCount.filter(device_id=device_id)
                        # print(cartCount.query)
                        cartCount = cartCount.count()
                        if cartCount<=0:
                            if quantity<=0:
                                status = 0
                                ack = 'fail'
                                msg = 'provide quantity to be added.'
                            else:
                                cartArr = {}
                                cartArr.update({"website_id":website_id, "device_id":device_id, "product_id":product_id, "quantity":quantity})
                                if customer_id and customer_id is not None:
                                    cartArr.update({"customer_id":customer_id})
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
                            # print("quantity",quantity)
                            if quantity>0:
                                if customer_id and customer_id is not None:
                                    update_id = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, device_id=device_id, customer_id=customer_id, product_id=product_id).update(quantity=quantity)
                                elif device_id:
                                    update_id = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, device_id=device_id, product_id=product_id).update(quantity=quantity)
                                status = 1
                                ack = 'success'
                                msg = 'Cart quantity updated.'
                            else:
                                if customer_id and customer_id>0:
                                    EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, customer_id=customer_id ).delete()
                                elif device_id:
                                    EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, device_id=device_id ).delete()
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
                        cartCount = cartCount.filter(customer_id=customer_id)
                    elif device_id:
                        cartCount = cartCount.filter(device_id=device_id)
                    cartCount = cartCount.count()
                    if cartCount>0:
                        if customer_id and customer_id>0:
                            EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, customer_id=customer_id ).delete()
                        elif device_id:
                            EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, device_id=device_id ).delete()
                        status = 1
                        ack = 'success'
                        msg = 'Product deleted from cart.'
                    else:                        
                        status = 0
                        ack = 'fail'
                        msg = "Quantity should not be 0."
        cart_data = discount.GetCartDetails(1,1,customer_id, device_id)
        cartdata = cart_data.data
        return_details = []
        if cart_data:
            cnt = 0
            for i in range(len(cartdata['cartdetails'])):
              if int(cartdata['cartdetails'][i]['id']) == int(product_id):
                  return_details.append(cartdata['cartdetails'][i])
        # GetCartDetails(company_id, website_id, customer_id=None, device_id=None, webshop_id=None, country_id = None, state_id = None, post_code = None, user_id = None, user_group_id = None, coupon_code = None):
        cartdata['cartdetails'] = return_details
        data = {
            "status":status,
            "ack":ack,
            "msg":msg,
            # "cart_data":cart_data.data
            "cart_data":cartdata
        }
        return Response(data)

def check_instock_quantity(product_id, qty, user_id=None, device_id=None):
    data = []
    qty  = abs(qty)

    # warehouse_id = warehouse_id_by_user_id(user_id , device_id)
    warehouse_id = 1
    if product_id and qty:
        max_order_unit = get_max_order_unit()
        rs_prod_qty = EngageboostProducts.objects.filter(id=product_id).first()
        prod_qty_data = ProductsViewNewSerializer(rs_prod_qty)

        if prod_qty_data['max_order_unit']:
            max_order_unit= prod_qty_data['max_order_unit']
        default_price = 1
        max_order_unit = 5
        qty = 2
        # if str(prod_qty_data['default_price'])=="2000.00":  
        if default_price>0:           
            if max_order_unit >= qty:
                product_quantity = product_stock_count(product_id,warehouse_id);
                product_quantity = 10
                if product_quantity > 0:
                    if qty <= product_quantity:
                        ack=1
                        msg="available"
                    else:
                        ack = 1
                        msg = product_quantity + " qty of this product is available."
                else:
                    ack=0
                    msg="out of stock"
            else:
                ack=1
                msg="You can purchase only "+ max_order_unit+" qty of this product."
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
            if requestdata['customer_id']: 
                customer_id = requestdata['customer_id']
            else: 
                customer_id = None
        except KeyError:
            customer_id = None
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
        
        disc_pro = discount.GetCartDetails( 1,1,customer_id, device_id)
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
        EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id,device_id=device_id ).delete()
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

        try:
            if requestdata['customer_id']: 
                customer_id = requestdata['customer_id']
            else: 
                customer_id = None
        except KeyError:
            customer_id = None
        
        str_status  = ""
        msg         = ""
        if customer_id and customer_id>0:
            EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, customer_id=customer_id ).delete()
            str_status = status.HTTP_200_OK
            msg = "success"
        elif device_id:
            EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, device_id=device_id ).delete()
            str_status = status.HTTP_200_OK
            msg = "success"
        else:
            str_status = status.HTTP_400_BAD_REQUEST
            msg = "Provide Customer Id or Device Id."
        data = {"status":str_status, "msg":msg}

        # disc_pro = discount.GetCartDetails( 1,1,customer_id, device_id)       
        # data.update({"data":disc_pro.data})
        return Response(data, str_status)


class Viewcart(APIView):
    permission_classes = []
    # def post(self, request, *args, **kwargs):
    def get(self, request, format=None):

        requestdata = request.data
        user                = request.user
        user_id             = user.id
        device_id           = request.META.get('HTTP_DEVICEID')
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
            cartData = get_cart_view(device_id,customer_id)

            total_cart_count    = cartData['cart_count']
            saved_amount        = cartData['saved_amount']
            total_amount        = cartData['total_amount']
            returnArray         = cartData['cart_details']
            cart_count_itemwise = cartData['cart_count_itemwise']
            if int(total_cart_count)>0:
                str_status = status.HTTP_200_OK
                msg = "Success"
            else:
                str_status = status.HTTP_204_NO_CONTENT
                msg = 'Cart is empty'

        data = {
            "status":str_status,
            "msg":msg,
            "cart_count":total_cart_count,
            "cart_count_itemwise":cart_count_itemwise,
            "saved_amount":saved_amount,
            "total_amount":total_amount,
            "data":returnArray
        }
        return Response(data, str_status)


def get_cart_view(device_id=None, user_id=None):
    website_id = get_company_website_id_by_url()
    # company_id = get_company_id_by_url()
    returnArray     = []
    saved_amount    = 0
    total_amount    = 0
    cart_count      = 0
    counter         = 0
    cart_count_itemwise = 0

    rs_cart = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id)
    if user_id and user_id>0:
        rs_cart = rs_cart.filter(customer_id=user_id)
    elif device_id and device_id is not None:
        rs_cart = rs_cart.filter(device_id=device_id)

    cart_count = rs_cart.count()
    cart_data = []
    if cart_count>0:
        rs_cart = rs_cart.all()
        cart_data = EngageboostTemporaryShoppingCartsSerializer(rs_cart, many=True)
        cart_data = cart_data.data
        saved_amount = 0
        total_amount = 0
        
        for cartvalue in  cart_data:
            cart_count_itemwise = cart_count_itemwise + int(cartvalue['quantity'])
            request_data = {
                'website_id': website_id,
                'company_id': website_id,
                'product_ids': cartvalue['product_id']['id'],
                'qtys': cartvalue['quantity'],
                'prod_price': cartvalue['product_id']['default_price']
            }
            productsdiscount = discount.get_discount_detalils(request_data)
            
            # field_name="'size'";
            # primary_category_id = $ContentManagements->category_ids_from_product_ids($product_id);
            # customfield=$this->get_custom_fields_var($primary_category_id, $product_id,6,1,'','', $field_name);
            # variant_name=$customfield[0]['MarketplaceFieldValue']['value'];            
            cartvalue['product_name']    = cartvalue['product_id']['name']
            cartvalue['product_sku']    = cartvalue['product_id']['sku']
            cartvalue['product_slug']    = cartvalue['product_id']['slug']
            cartvalue['original_price']  = cartvalue['product_id']['default_price']
            cartvalue['new_default_price']       = productsdiscount[0]['new_default_price']
            cartvalue['new_default_price_unit']  = productsdiscount[0]['new_default_price_unit']
            cartvalue['discount_price_unit']     = productsdiscount[0]['discount_price_unit']
            cartvalue['discount_price']          = productsdiscount[0]['discount_price']
            cartvalue['discount_amount']         = productsdiscount[0]['discount_amount']
            cartvalue['disc_type']               = productsdiscount[0]['disc_type']
            cartvalue['coupon']                  = productsdiscount[0]['coupon']

            cartvalue['veg_nonveg_type'] = cartvalue['veg_nonveg_type']
            cartvalue['default_price']   = cartvalue['product_id']['default_price']
            # discount_price=$original_price-$selling_price;
            saved_amount = float(saved_amount) + float(productsdiscount[0]['discount_price'])
            total_amount = float(total_amount) + float(productsdiscount[0]['new_default_price'])
           
    data = {
        "cart_details":cart_data,
        "cart_count":cart_count,
        "cart_count_itemwise":cart_count_itemwise,
        "total_amount":total_amount,
        "saved_amount":saved_amount
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
            now     = datetime.now()
            today   = now.date()                
            new_date = ''  
            new_date = now_utc + timedelta(days=x)
            next_day_arr.append(new_date)

        rs_data     = EngageboostDeliverySlot.objects.filter(isdeleted='n', isblocked='n', warehouse_id=warehouse_id).order_by('day_id','start_time').all()
        slot_data   = DeliverySlotSerializer(rs_data, many=True)
        DeliverySlot = []
        current_time = datetime.now().strftime('%H:%M:%S')
        to_day      = datetime.now().strftime('%Y-%m-%d')            
        order_data  = EngageboostOrdermaster.objects.filter(time_slot_date__gte=to_day,buy_status = 1, webshop_id=warehouse_id).exclude(order_status=2).all().values('time_slot_date','slot_start_time').order_by('time_slot_date','slot_start_time').annotate(total=Count('slot_start_time'))
        # print(order_data.query)
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

class SaveCart(APIView):
    def post(self, request, format=None):
        now_utc                = datetime.now(timezone.utc).astimezone()
        shipping_label_content = ""
        #  *************  Get Base currency
        base_currency = "INR"
        try:
            postdata                = request.data
            user                = request.user
            user_id             = user.id
            device_id               = postdata['device_id']
            # user_id               = postdata['user_id']
            address_book_id         = postdata['address_book_id']
            time_slot_date          = postdata['time_slot_date']
            time_slot_time          = postdata['time_slot_time']
            special_instruction     = postdata['special_instruction']
            coupon_code             = postdata['coupon_code']
            if 'time_slot_id' in postdata:
                time_slot_id            = postdata['time_slot_id']
            website_id              = postdata['website_id']
            warehouse_id = 4
            if warehouse_id:
                warehouse_id            = postdata['warehouse_id']
            customer_id = user_id
            order_serializer_arr    = {}
            website_id              = website_id
            # *** Get Customer details
            # customerdetails         = postdata["customerdetails"]
            payment_type_id         = 0
            str_status = ""
            #********FETCH PAYMENT TYPE********#
            if coupon_code:
                applied_coupon = coupon_code
            else:
                applied_coupon = ""

            #******** SAVE CUSTOMER INFORMATION ********#
           
            address_book_id = address_book_id
            try:
                has_customer = EngageboostCustomers.objects.filter(customer_group_id=user_id).first()
                # geo_location = common.get_geo_location(customerdetails["billing_street_address"],customerdetails["billing_city"],customerdetails["billing_postcode"],customerdetails["billing_state"],customerdetails["billing_country"])
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
                cartData = discount.GetCartDetails(1,1,customer_id, device_id, warehouse_id, None, None, None, None, None,"TESTLFC")
                cartData = cartData.data
                if cartData:
                    order_info = {
                        "website_id":website_id,
                        "company_id":1,
                        "webshop_id":warehouse_id,
                        "payment_method_id":0,
                        "payment_type_id":0,
                        "payment_method_name":"cash On Delivery",
                        "gross_amount":cartData['orderamountdetails'][0]['grand_total'],
                        "net_amount":cartData['orderamountdetails'][0]['net_total'],
                        "shipping_cost":cartData['orderamountdetails'][0]['shipping_charge'],
                        "paid_amount":cartData['orderamountdetails'][0]['paid_amount'],
                        "gross_discount_amount":cartData['orderamountdetails'][0]['gross_discount'],
                        "tax_amount":cartData['orderamountdetails'][0]["tax_amount"],
                        "order_status":99,
                        "buy_status":1,
                        "created":now_utc,
                        "modified":now_utc,
                        "cart_discount":cartData['orderamountdetails'][0]["cart_discount"],
                        "cod_charge":cartData['orderamountdetails'][0]["cod_charge"],
                        "applied_coupon":applied_coupon,
                        # "custom_msg":cartData['orderamountdetails'][0]["custom_msg"],
                        # "custom_order_id":"SAMPLE-ORD#82",
                        "customer_id":user_id,
                        # "pay_txndate":postdata['pay_txndate']
                    }
                    if 'gross_total' in postdata:
                        order_info.update({ "order_amount":cartData['orderamountdetails'][0]['grand_total']})
                    # if 'zone_id' in postdata:
                    #     order_info.update({"zone_id":postdata["zone_id"]})
                    # if 'area_id' in postdata:
                    #     order_info.update({"area_id":postdata["area_id"]})
                    if 'time_slot_date' in postdata:
                        order_info.update({"time_slot_date":postdata["time_slot_date"]})
                    if 'time_slot_id' in postdata:
                        order_info.update({"time_slot_id":postdata["time_slot_id"]})
                    if 'slot_start_time' in postdata:
                        order_info.update({"slot_start_time":postdata["slot_start_time"]})
                    if 'slot_end_time' in postdata:
                        order_info.update({"slot_end_time":postdata["slot_end_time"]})
                    # if 'currency_id' in postdata:
                    #     currency = common.get_currency_details(postdata["currency_id"])
                    #     order_info.update({"currency_code":currency["currency"]})
                    # else:
                    #     order_info.update({"currency_code":base_currency["currency_code"]})

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
                    else:
                        order_serializer_arr['custom_order_id']=custom_order_id
                        save_order_master = EngageboostOrdermaster.objects.create(**order_serializer_arr)
                        order_id = save_order_master.id if save_order_master else 0
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
                            "product_id":cartdetails["id"],
                            "quantity":cartdetails["qty"],
                            "deleted_quantity":0,
                            "product_price":cartdetails["new_default_price_unit"],
                            "product_discount_price":cartdetails["discount_price_unit"],
                            "product_tax_price":cartdetails["tax_price_unit"],
                            "tax_percentage":cartdetails["tax_percentage"],
                            "product_price_base":cartdetails["new_default_price_unit"],
                            "product_discount_price_base":cartdetails["discount_price_unit"],
                            "created":now_utc
                        }

                        price_obj = EngageboostProductPriceTypeMaster.objects.filter(isblocked='n',isdeleted='n',product_id=cartdetails["id"], price_type_id=1)
                        
                        if price_obj.count()>0:
                            priceData = price_obj.first()
                            obj = EngageboostChannelCurrencyProductPrice.objects.filter(product_price_type_id=priceData.id,warehouse_id=warehouse_id,product_id=cartdetails["id"])
                            if obj.count()>0:
                                channelData = obj.first()
                                order_product_arr["mrp"] = channelData.mrp
                                order_product_arr["cost_price"] = channelData.cost
                        save_order_product = EngageboostOrderProducts.objects.create(**order_product_arr)
                        common.update_stock_all(cartdetails["id"],1,cartdetails["qty"],"Decrease","virtual",order_id,website_id)

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
            #******** SAVE ORDER ACTIVITY (END)********#

            #******** GENERATE AUTO RESPONDER ********#
            # buffer_data = common_functions.getAutoResponder("","","","","",3)
            # if buffer_data and buffer_data["content"]:
            #     autoResponderData  = buffer_data["content"]
            #     if autoResponderData["email_type"] == 'T':
            #         emailContent = autoResponderData["email_content_text"]
            #     else:
            #         emailContent = autoResponderData["email_content"]
            #     emailContent = str(emailContent)
            #     emailContent = emailContent.replace('{@first_name}',customerdetails["billing_name"])
            #     emailContent = emailContent.replace('{@custom_order_id}',postdata["custom_order_id"])
            #     emailContent = emailContent.replace('{@delivery_name}',customerdetails["billing_name"])
            #     emailContent = emailContent.replace('{@delivery_street_address}',customerdetails["delivery_street_address"])
            #     emailContent = emailContent.replace('{@delivery_city}',customerdetails["delivery_city"])
            #     emailContent = emailContent.replace('{@delivery_postcode}',customerdetails["delivery_postcode"])
            #     emailContent = emailContent.replace('{@delivery_state}',billing_state_name)
            #     emailContent = emailContent.replace('{@delivery_country}',billing_country_name)
            #     emailContent = emailContent.replace('{@delivery_phone}',customerdetails["billing_phone"])
            #     emailContent = emailContent.replace('{@payment_method_name}',payment_method_name)

            #     emailContent = emailContent.replace('{@gross_amount}',str(postdata["sub_total"]))
            #     emailContent = emailContent.replace('{@shipping_cost}',str(postdata["shipping_charge"]))
            #     emailContent = emailContent.replace('{@tax_amount}',str(postdata["tax_amount"]))
            #     emailContent = emailContent.replace('{@discount_amount}',str(postdata["gross_discount"]))
            #     emailContent = emailContent.replace('{@net_amount}',str(postdata["net_total"]))
                #******** GENERATE AUTO RESPONDER (END)********#
            # emailcomponent.sendOrderMail(company_db,customerdetails["billing_email_address"],autoResponderData["email_from"],autoResponderData["subject"],emailContent)
            
            EngageboostTemporaryShoppingCarts.objects.filter(customer_id=user_id).delete()
            elastic = common.save_data_to_elastic(order_id,'EngageboostOrdermaster')
            str_status = status.HTTP_200_OK
            data={"status":1,"api_status":"Order created successfully","message":"Order created successfully"}
        except Exception as error:
            str_status = status.HTTP_417_EXPECTATION_FAILED
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            data={"status":str_status,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Something went wrong"}
        return Response(data, str_status)

class checkout(APIView):
    def put(self, request, format=None):
        now_utc             = datetime.now(timezone.utc).astimezone()
        user                = request.user
        user_id             = user.id

        requestdata         = request.data
        order_id            = requestdata['order_id']
        payment_method_id   = requestdata["payment_method_id"]
        payment_type_id     = requestdata["payment_type_id"]
        payment_method_name = requestdata["payment_method_name"]
        str_status = ""
        msg = ""
        update_arr = {
            "payment_method_id":payment_method_id,
            "payment_type_id":payment_type_id,
            "payment_method_name":payment_method_name,
            "order_status":0,
            "buy_status":1
        }
        rs_check            = EngageboostOrdermaster.objects.filter(customer_id=user_id, custom_order_id=order_id).first()
        if rs_check:
            str_status = status.HTTP_200_OK
            EngageboostOrdermaster.objects.filter(customer_id=user_id, custom_order_id=order_id).update(**update_arr)
            msg= "Payment create successfully."
        else:
            str_status = status.HTTP_401_UNAUTHORIZED
            msg= "You are not allowed to make this payment."
        data = {
            "status":str_status,
            "msg":msg
        }
        return Response(data, str_status)

def GenerateOrderId(website_id=None):
    if website_id is None:
        website_id = 1

    imageresizeon = EngageboostGlobalSettings.objects.get(website_id=website_id)
    orders = EngageboostOrdermaster.objects.last()
    Order1 =int(orders.id)+int(1)
    cust_order_id = str(imageresizeon.orderid_format)+str(Order1)
    return cust_order_id


class ViewOrderDetails(APIView):
    def get(self, request, order_id, format=None):
        now_utc = datetime.now(timezone.utc).astimezone()
        user                = request.user
        user_id             = user.id
        str_status = ""
        try:
            rs_order    = EngageboostOrdermaster.objects.filter(id=order_id, customer_id=user_id).first()
            if rs_order:
                order_data  = ViewOrderSerializer(rs_order)
                order_data  = order_data.data
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
        rs_up = EngageboostTemporaryShoppingCarts.objects.filter(device_id=device_id).update(customer_id=user_id)
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

        website_id = get_company_website_id_by_url()
        company_id = get_company_id_by_url()

        requestdata = request.data
        coupon_code = None
        if "coupon_code" in requestdata:
            coupon_code = requestdata["coupon_code"]

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
            cartData = discount.GetCartDetails(company_id,website_id,user_id, device_id, None, None, None, None, None, None,coupon_code)
            # GetCartDetails(company_id, website_id, customer_id=None, device_id=None, webshop_id=None, country_id = None, state_id = None, post_code = None, user_id = None, user_group_id = None, coupon_code = None):
            cartData = cartData.data
            data = {
                "status":str_status,
                "data":cartData
            }
        return Response(data,str_status)

class CartSummary(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        user                = request.user
        user_id             = user.id
        device_id           = request.META.get('HTTP_DEVICEID')

        website_id = get_company_website_id_by_url()
        company_id = get_company_id_by_url()
        requestdata = request.data
        country_id = None
        state_id = None
        post_code = None

        if "warehouse_id" in requestdata:
            warehouse_id = requestdata["warehouse_id"]
        else:
            warehouse_id = 2
            
        coupon_code = None
        if "coupon_code" in requestdata:
            coupon_code = requestdata["coupon_code"]

        if "address_id" in requestdata:
            address_id = requestdata["address_id"]
            rs_address = EngageboostCustomersAddressBook.objects.filter(id=address_id).first()
            if rs_address:
                country_id = rs_address.delivery_country
                state_id = rs_address.delivery_state
                post_code = rs_address.delivery_postcode
        else:
            if user_id is not None:
                rs_address = EngageboostCustomersAddressBook.objects.filter(customers_id=user_id, set_primary=1).first()
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
            cartData = discount.GetCartDetails(company_id,website_id,user_id, device_id, warehouse_id, country_id, state_id, post_code, None, None,coupon_code)
            # GetCartDetails(company_id, website_id, customer_id=None, device_id=None, webshop_id=None, country_id = None, state_id = None, post_code = None, user_id = None, user_group_id = None, coupon_code = None):
            cartData = cartData.data
            data = {
                "status":str_status,
                "data":cartData
            }
        return Response(data,str_status)

def save_cart():
    customer_id = None
    device_id = "CBGTD44KDH"
    cartData = discount.GetCartDetails(1,1,customer_id, device_id, None, None, None, None, None, None,"TESTLFC")
    # cartData = discount.GetCartDetails(1,1,customer_id, device_id)
    print("KK")
    print(json.dumps(cartData.data))

 # GetCartDetails(company_id, website_id, customer_id=None, device_id=None, webshop_id=None, country_id = None, state_id = None, post_code = None, user_id = None, user_group_id = None, coupon_code = None):

def test():
    order_id = 82
    now_utc     = now_utc = datetime.now(timezone.utc).astimezone()
    activityType = 1
    # activity_details = common_functions.save_order_activity(order_id,now_utc,0,"Order has been placed",'',activityType)
    buffer_data = common_functions.getAutoResponder("","","","","",3)  
    # c = {
    #     'first_name':"Kalyanasis Roy",
    #     'custom_order_id':"SAMPLE-ORD#82",
    #     'delivery_name':"Kalyanasis Roy",
    #     'delivery_street_address':"86A Topsia",
    #     'delivery_city':"Kolkata",
    #     'delivery_postcode':"700046",
    #     'delivery_state':"West Bengal",
    #     'delivery_country':"India",
    #     'delivery_phone':"5462311458",
    #     'payment_method_name':"Cash On Delivery",
    #     'gross_amount':571.50,
    #     'shipping_cost':0.00,
    #     'tax_amount':0.00,
    #     'discount_amount':71.50,
    #     'net_amount':500,
    # }

    # email_template_data =  common_functions.getAutoResponder("","","","","",3)
    # str_template        = template.Template(email_template_data['content']['email_content'])
    # str_context         = template.Context(c)
    # message             = str_template.render(str_context)

    rs_customerdetails = EngageboostCustomersAddressBook.objects.filter(id=47).first()
    customerdetails = CustomersAddressBookSerializer(rs_customerdetails)
    customerdetails = customerdetails.data

    cartData = discount.GetCartDetails(1,1,1, None, None, None, None, None, None, None,"TESTLFC")
    cartData = cartData.data
    # print(json.dumps(cartData))
    # if buffer_data and buffer_data["content"]:
    #     autoResponderData  = buffer_data["content"]
    #     if autoResponderData["email_type"] == 'T':
    #         emailContent = autoResponderData["email_content_text"]
    #     else:
    #         emailContent = autoResponderData["email_content"]
    #     emailContent = str(emailContent)
    #     emailContent = emailContent.replace('{@first_name}',customerdetails["billing_name"])
    #     emailContent = emailContent.replace('{@custom_order_id}',cartData['orderamountdetails']["custom_order_id"])
    #     emailContent = emailContent.replace('{@delivery_name}',customerdetails["billing_name"])
    #     emailContent = emailContent.replace('{@delivery_street_address}',customerdetails["delivery_street_address"])
    #     emailContent = emailContent.replace('{@delivery_city}',customerdetails["delivery_city"])
    #     emailContent = emailContent.replace('{@delivery_postcode}',customerdetails["delivery_postcode"])
    #     emailContent = emailContent.replace('{@delivery_state}',billing_state_name)
    #     emailContent = emailContent.replace('{@delivery_country}',billing_country_name)
    #     emailContent = emailContent.replace('{@delivery_phone}',customerdetails["billing_phone"])
    #     emailContent = emailContent.replace('{@payment_method_name}',payment_method_name)

    #     emailContent = emailContent.replace('{@gross_amount}',str(cartData['orderamountdetails']["grand_total"]))
    #     emailContent = emailContent.replace('{@shipping_cost}',str(cartData['orderamountdetails']["shipping_charge"]))
    #     emailContent = emailContent.replace('{@tax_amount}',str(cartData['orderamountdetails']["tax_amount"]))
    #     emailContent = emailContent.replace('{@discount_amount}',str(cartData['orderamountdetails']["gross_discount"]))
    #     emailContent = emailContent.replace('{@net_amount}',str(cartData['orderamountdetails']["net_total"]))

    # print(emailContent)

# test()