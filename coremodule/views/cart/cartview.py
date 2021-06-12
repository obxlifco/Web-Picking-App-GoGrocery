from django.shortcuts import render

from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# Import Model And Serializer
from webservices.models import *
from coremodule.coremodule_serializers import *
from coremodule.views.product import discount



import json
import base64
# import hashlib


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


class add_to_cart(generics.ListAPIView):

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

        device_id           = requestdata['device_id']
        customer_id         = requestdata['customer_id']
        product_id          = requestdata['product_id']
        quantity            = requestdata['quantity']

        if device_id  and customer_id:
            product_count = EngageboostProducts.objects.filter(isdeleted='n', isblocked='n', status='n').count()
            if product_count <=0:
                status = 0
                ack = "fail"
                msg = "Product not available."
            else:
                if quantity>0:
                    dataProductAvailability = check_instock_quantity(product_id,quantity,customer_id,device_id)
                    print(dataProductAvailability)
                    if dataProductAvailability['ack']:
                        
                        cartCount = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id ).all()
                        if customer_id and customer_id>0:
                            cartCount = cartCount.filter(customer_id=customer_id)
                        elif device_id:
                            cartCount = cartCount.filter(customer_id=0, device_id=device_id)
                        cartCount = cartCount.count()

                        if cartCount<=0:
                            if quantity<=0:
                                status = 0
                                ack = 'fail'
                                msg = 'provide quantity to be added.'
                            else:
                                cartArr = {}
                                cartArr.update({"website_id":website_id, "device_id":device_id, "customer_id":customer_id, "product_id":product_id, "quantity":quantity})
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
                                update_id = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, device_id=device_id, customer_id=customer_id, product_id=product_id).update(quantity=quantity)
                                status = 1
                                ack = 'success'
                                msg = 'Cart quantity updated.'
                            else:
                                if customer_id and customer_id>0:
                                    EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, customer_id=customer_id ).delete()
                                elif device_id:
                                    EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, customer_id=0, device_id=device_id ).delete()
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
                        cartCount = cartCount.filter(customer_id=0, device_id=device_id)
                    cartCount = cartCount.count()
                    if cartCount>0:                        
                        if customer_id and customer_id>0:
                            EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, customer_id=customer_id ).delete()
                        elif device_id:
                            EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, customer_id=0, device_id=device_id ).delete()
                        status = 1
                        ack = 'success'
                        msg = 'Product deleted from cart.'
                    else:
                        status = 0
                        ack = "fail"
                        mag = "Quantity shouldnot be 0."
        cart_data = discount.GetCartDetails(1,1,1)
        data = {
            "status":status,
            "ack":ack,
            "msg":msg,
            "cart_data":cart_data.data
        }
        return Response(data)

def check_instock_quantity(product_id, qty, user_id=None, device_id=None):
    data = []
    qty  = abs(qty)

    warehouse_id = warehouse_id_by_user_id(user_id , device_id)
    if product_id and qty:
        max_order_unit = get_max_order_unit()
        rs_prod_qty = EngageboostProducts.objects.filter(id=product_id).first()
        prod_qty_data = ProductsViewNewSerializer(rs_prod_qty)

        if prod_qty_data['max_order_unit']:
            max_order_unit= prod_qty_data['max_order_unit']
        default_price = 2000
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
        product_quantity = stock_data['real_stock']
        return product_quantity

def get_default_warehouse_id():
    warehouse_id = 5
    return warehouse_id

class remove_cart(generics.ListAPIView):
    def post(self, request, *args, **kwargs):
        requestdata = request.data
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
            data = {
                "status":cart_data['status'],
                "msg":cart_data['msg']
            }
        else:
            data = {
                "status":0,
                "msg":"Provide Product_id."
            }
        
        disc_pro = discount.GetCartDetails(1,1,1)
        data.update({"data":disc_pro.data})
        return Response(data)

def RemoveFromCart(product_id, website_id, customer_id=None, device_id=None):
    status = 0
    msg = ""
    if customer_id and customer_id>0:
        EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, customer_id=customer_id ).delete()
        status = 1
        msg = "success"
    elif device_id:
        EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id, product_id=product_id, customer_id=0, device_id=device_id ).delete()
        status = 1
        msg = "success"
    else:
        status = 0
        msg = "Provide Customer Id or Device Id."
    data = {"status":status, "msg":msg}
    return data
