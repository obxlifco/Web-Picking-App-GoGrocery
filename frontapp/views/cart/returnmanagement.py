from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from datetime import *
import pytz
import django
from django import utils
from django.db.models import TimeField

# Import Model And Serializer
from webservices.models import *
from pos.pos_serializers import *
import json
from collections import Counter
import string
from django.db.models import Count, Sum
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db.models.aggregates import Aggregate
from django.contrib.postgres.aggregates import *
# from pos.views.sales.salesview import manage_stock, customer_detalils
# from pos.views.sales.discount import get_creadit_points

def get_creadit_points(request):
    # print(request)
    website_id              = request['website_id']
    product_ids             = request['product_ids']
    category_ids            = request['category_ids']
    customer_ids            = request['customer_ids']
    price                   = request['price']
    rule_id                 = request['rule_id']
    # order_id                = request['order_id']
    # customer_contact_no     = request['customer_contact_no']
    earn_points             = 0
    category_flag           = False
    product_flag            = False
    coustomer_flag          = False
    customer_group_flag     = False
    order_amount_flag       = False

    today = django.utils.timezone.now()
    credit_rs = EngageboostCreditPoint.objects.filter(isdeleted='n', isblocked='n', id=rule_id).first()
    
    if credit_rs and credit_rs is not None:
        # print('credit_rs')
        credit_data = EngageboostCreditPointSerializer(credit_rs)
        credit_data = credit_data.data
        # print(credit_data)
        if credit_data["CreditPointConditions"]:
            if len(credit_data["CreditPointConditions"]) > 0 :
                # print(credit_data["CreditPointConditions"])
                for creadit_point in credit_data["CreditPointConditions"]:
                    if creadit_point["fields"] == 0:  ### For Category Checking
                        all_category_ids = creadit_point["all_category_id"].split(',')
                        result = common_data(all_category_ids, category_ids, creadit_point["condition"])
                        category_flag = result 
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
                                order_amount_flag = True
                        if condition == '>=':
                            if int(order_amount) >= int(price):
                                order_amount_flag = True
                        if condition == '==':
                            if int(order_amount) == int(price):
                                order_amount_flag = True
                        if condition == '!=':
                            if int(order_amount) != int(price):
                                order_amount_flag = True

                    if creadit_point["fields"] == -2:  ### For Customer Checking
                        all_customer_ids = creadit_point["all_customer_id"].split(',')
                        result = common_data(all_customer_ids, customer_ids, creadit_point["condition"])
                        coustomer_flag = result
                        # print(result)

                    if creadit_point["fields"] == -3:  ### For Customer Group Checking
                        all_customer_group_ids = creadit_point["all_customer_id"].split(',')
                        result = common_data(all_customer_group_ids, customer_ids, creadit_point["condition"])
                        customer_group_flag = result
                        # print(result)
            else:
                category_flag           = True
                product_flag            = True
                coustomer_flag          = True
                customer_group_flag     = True
                order_amount_flag       = True
            # print('category_flag', category_flag)
            # print('product_flag', product_flag)
            # print('coustomer_flag', coustomer_flag)
            # print('customer_group_flag', customer_group_flag)
            # print('order_amount_flag', order_amount_flag)
            if customer_group_flag == True and coustomer_flag == True and order_amount_flag == True and product_flag == True and category_flag == True:
                if credit_data["applied_as"] == 'percentage':
                    earn_points = ((float(price) / float(100)) * float(credit_data["points"]))
                if credit_data["applied_as"] == 'fixed':
                    earn_points_in_price = (float(price) / float(credit_data["per_rupees"]))
                    earn_points = float(credit_data["points"]) * float(earn_points_in_price)
                    # ((float(price) / float(credit_data["per_rupees"])) * float(credit_data["points"]))
                valid_to = django.utils.timezone.now() + timedelta(days=credit_data["loyalty_expire_days"])
        data = {"status":1,"earn_point":earn_points}
    else:
        data = {"status":0,"earn_point":0}
    return data

def customer_detalils(phone, web_id):
        website_id = web_id
        phone_no = phone
        customerObj = EngageboostCustomers.objects.filter(isdeleted='n', isblocked='n', website_id=website_id)
        if phone_no!=None:
            customerObj = customerObj.filter(phone=phone_no)

        rs_customer 	= customerObj.first()
        # print(rs_customer)
        if rs_customer is not None:
            customer_data 	= CustomerSerializer(rs_customer)
            customer_data 	= customer_data.data
            data = {
                "status":1,
                "msg":"success",				
                "customers" :customer_data				
            }            
        else:
                data ={
                "status":0,
                "msg" :"No Data Found.",
                "customers" :[]			
            }

        return data

def manage_stock(request):
    # print('Stock', request)
    data = {"status":0, "msg":'falure'}
    stock_qset = EngageboostProductStocks.objects.filter(isdeleted='n', isblocked='n', product_id=request['product_id'],warehouse_id=request['warehouse_id']).first()
    # print('stock_qset', stock_qset)
    if stock_qset:
        if request['manage_type'] == "return":  ##### Incrise stock
            current_stock = int(stock_qset.real_stock) + int(request['qtys'])
            # print('current Stock', current_stock)
            instance = EngageboostProductStocks.objects.filter(isdeleted='n', isblocked='n', product_id=request['product_id'],warehouse_id=request['warehouse_id']).first()#.update(real_stock=current_stock)
            instance.real_stock=current_stock
            instance.save()
            data = {"status":1, "msg":'stock incrise'}
        if request['manage_type'] == "sell":  ##### Decrise stock
            # print(request['qtys'])
            current_stock = int(stock_qset.real_stock) - int(request['qtys'])
            instance = EngageboostProductStocks.objects.filter(isdeleted='n', isblocked='n', product_id=request['product_id'],warehouse_id=request['warehouse_id']).first()#.update(real_stock=current_stock)
            instance.real_stock=current_stock
            instance.save()
            data = {"status":2, "msg":'stock decrise'}
    # stock_details =  ProductStocksSerializer(stock_qset)
    return data

def order_status_master(order_status, buy_status):
    if order_status == 99 and buy_status == 1:
        return 'Waiting Approval'
    
    if order_status == 0 and buy_status == 1:
        return 'Pending'
    
    if order_status == 100 and buy_status == 1:
        return 'Processing'
    
    if order_status == 1 and buy_status == 1:
        return 'Shipped'
    
    if order_status == 2 and buy_status == 1:
        return 'Cancelled'
    
    if order_status == 4 and buy_status == 1:
        return 'Completed'
    
    if order_status == 5 and buy_status == 1:
        return 'Full Refund'
    
    if order_status == 6 and buy_status == 1:
        return 'Partial Refund'
    
    if order_status == 11 and buy_status == 1:
        return 'Partial Refund'
    
    if order_status == 12 and buy_status == 1:
        return 'Assigned to Showroom'
    
    if order_status == 13 and buy_status == 1:
        return 'Delivered'
    
    if order_status == 16 and buy_status == 1:
        return 'Closed'
    
    if order_status == 18 and buy_status == 1:
        return 'Pending Service'

    if order_status == 9999 and buy_status == 1:
        return 'Hold'

    if order_status == 3 and buy_status == 0:
        return 'Abandoned'
    
    if order_status == 999 and buy_status == 0:
        return 'Failed'

    else :
        return 'Invoiced'

def order_payment_return(request):
    data = {}
    if request['return_method_id']:
        payment_method_details = EngageboostPaymentgatewayMethods.objects.filter(id=request["return_method_id"]).first()
        customer_dtl = customer_detalils(request["contact_no"], request["website_id"])

        if payment_method_details:
            paymentdetailsObj = EngageboostOrderPaymentDetails.objects.filter(order_id_id=request["order_id"], payment_method_id=request["return_method_id"], isblocked='n', isdeleted='n')
            paymentdetails_rs = paymentdetailsObj.first()
            if paymentdetails_rs is not None:
                new_payment_amount =  float(paymentdetails_rs.payment_amount) - float(request["return_amount"])
                new_return_amount = float(paymentdetails_rs.return_amount) + float(request["return_amount"])
            if payment_method_details.id == 16: ### cash
                if paymentdetails_rs is not None:
                    paymentdetailsObj.update(payment_amount=new_payment_amount, return_amount=new_return_amount)
                    data = {
                        "status":1,
                        "message": 'Cash Return Successfully'
                    }
            if payment_method_details.id == 24: ### loyalty
                if paymentdetails_rs is not None:
                    if paymentdetails_rs.payment_amount < request["return_amount"]:
                        data = {
                            "status":0,
                            "message": 'Return amount is grater then loyalty amount'
                        }
                    else:
                        paymentdetailsObj.update(payment_amount=new_payment_amount, return_amount=new_return_amount)
                        data = {
                            "status":1,
                            "message": 'Loyalty Return Successfully'
                        }
            if payment_method_details.id == 15: ### giftcard
                if paymentdetails_rs.payment_amount < request["return_amount"]:
                        data = {
                            "status":0,
                            "message": 'Return amount is grater then gift card amount'
                        }
                else:
                    #### Return Gift card amount in customer loyelty points table ####
                    loyaltyObj = EngageboostCustomerLoyaltypoints.objects.filter(customer_id=customer_dtl['customers']['id'], order_id=request["order_id"], status='giftcard')
                    loyalty_rs = loyaltyObj.first()
                    if loyalty_rs is not None:
                        if loyalty_rs.amount < request["return_amount"]:
                            new_gift_card_amount = float(0.00)
                        else:
                            new_gift_card_amount = float(loyalty_rs.amount) - float(request["return_amount"])
                        loyaltyObj.update(amount=new_gift_card_amount)
                    paymentdetailsObj.update(payment_amount=new_payment_amount, return_amount=new_return_amount)
                    data = {
                        "status":1,
                        "message": 'Gift Card Return Successfully.'
                    }
            if payment_method_details.id == 59: #### card
                # print('payment_method_name')
                data = {
                    "status":1,
                    "message": 'Card Return Successfully'
                }
    else:
        data = {
            "status":0,
            "message": 'Payment method id not define '
        }
    return data

def get_split_payment_percentage(request):
    # print(request)
    data = {}
    ### get persentage calculate total pay ###
    get_percentage = ((float(request['payment_amount']) * float(100)) / float(request['order_amount']))
    # print(get_percentage)
    return_amount = (float(get_percentage) * float(request['return_amount']) / float(100))
    # print(return_amount)
    data = {'status':1, 'pay_percentage':get_percentage, 'return_amount':return_amount}
    return data

def return_payment(request, contact_no, website_id):
    # print('Paylode',request)
    print('contact_no',contact_no)
    contact_no = contact_no
    # print('website_id',website_id)
    ### Get Global Details ####
    global_rs = EngageboostGlobalSettings.objects.filter(website_id=website_id).first()
    ### Get Customer Details ####
    customer_dtl = customer_detalils(contact_no, website_id)
    if contact_no == "":
        contact_no = customer_dtl['customers']['phone']
    # print(global_rs.query)
    for pay in request:
        return_obj = {}
        return_obj = {
            "order_id_id":pay['order_id'],
            "journal_id":pay['journal'],
            "register_id":pay['register'],
            "payment_method_id":pay['payment_method_id'],
            "payment_type_id":pay['payment_type_id'],
            "payment_method_name":pay['payment_method_name'],
            "payment_amount":pay['return_amount'],
            "order_amount":pay['order_amount'],
            "createdby":pay['createdby'],
            "modifiedby":pay['createdby'],
            "device_id":pay['device_id'],
            "created":django.utils.timezone.now(),
            "modified":django.utils.timezone.now(),
            "status":'refund'
        }
        return_obj = dict(return_obj,**return_obj)
        save_payment = EngageboostOrderPaymentDetails.objects.create(**return_obj)
        save_payment_id = save_payment.id

        ####### Return Amount Insert Into Customer loyalty Points Table ######
        return_loyalty_valid = 1
        if global_rs:
            loyelty_serializer_arr = {}
            if global_rs.payment_return_method == 'Y':
                if global_rs.payment_return_validity != '':
                    return_loyalty_valid = global_rs.payment_return_validity
                valid_to = django.utils.timezone.now() + timedelta(days=return_loyalty_valid)
                loyaltypoints_obj = {}
                loyaltypoints_obj = {
                    "website_id": website_id,
                    "rule_id": 0,
                    "customer_id": int(customer_dtl['customers']['id']),
                    "order_id": int(pay['order_id']),
                    "customer_contact_no": contact_no,
                    "description": 'This is return loyelty points',
                    "received_points": pay['return_amount'],
                    "burnt_points": 0.00,
                    "amount": pay['return_amount'],
                    "received_burnt": 0.00,
                    "status": "return",
                    "created": django.utils.timezone.now(),
                    "valid_form": django.utils.timezone.now(),
                    "expiry_date": valid_to,
                    "processing_status": 'complete'
                }
                loyelty_serializer_arr = dict(loyelty_serializer_arr,**loyaltypoints_obj)
                save_loyalty_points = EngageboostCustomerLoyaltypoints.objects.create(**loyelty_serializer_arr)
            else:
                valid_to = django.utils.timezone.now() + timedelta(days=return_loyalty_valid)
                if pay['payment_method_id'] == 24 or pay['payment_method_id'] == 15:
                    loyaltypoints_obj = {}
                    loyaltypoints_obj = {
                        "website_id": website_id,
                        "rule_id": 0,
                        "customer_id": int(customer_dtl['customers']['id']),
                        "order_id": int(pay['order_id']),
                        "customer_contact_no": contact_no,
                        "description": 'This is return loyelty points',
                        "received_points": pay['return_amount'],
                        "burnt_points": 0.00,
                        "amount": pay['return_amount'],
                        "received_burnt": 0.00,
                        "status": "return",
                        "created": django.utils.timezone.now(),
                        "valid_form": django.utils.timezone.now(),
                        "expiry_date": valid_to,
                        "processing_status": 'complete'
                    }
                    loyelty_serializer_arr = dict(loyelty_serializer_arr,**loyaltypoints_obj)
                    save_loyalty_points = EngageboostCustomerLoyaltypoints.objects.create(**loyelty_serializer_arr)
                # print(save_payment_id)
        data = {'status':1}
    return data

def check_user(contact_no, website_id, customer_id):
    # print(contact_no)
    data = {
        'status':0,
    }
    if contact_no != '':
        customer_dtl = customer_detalils(contact_no, website_id)
    else:
        customer_dtl = customer_detalils('0000000000', 1)

    order_customer_rs = EngageboostCustomers.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, id=customer_id).first()
    if order_customer_rs is not None:
        order_customer_contact_no = order_customer_rs.phone
        if str(order_customer_contact_no) == str(contact_no):
            data = {
                'status':1,
                'new_customer_id': order_customer_rs.id
            }
        else:
            if str(order_customer_contact_no) == '0000000000':
                if customer_dtl['status'] == 1:
                    data = {
                        'status':1,
                        'new_customer_id': customer_dtl['customers']['id']
                    }
                else:
                    customer_obj = {}
                    data={
                        'first_name':'',
                        'last_name':'',			
                        'email':'',
                        'phone':contact_no,
                        'created_date':django.utils.timezone.now(),
                        'modified_date':django.utils.timezone.now()
                    }
                    insertAuth 	= EngageboostUsers.objects.create(**data)			
			        # latestID 	= EngageboostUsers.objects.latest('id')
                    customer_obj = {
                        'auth_user_id':insertAuth.id,
                        'first_name':'',
                        'last_name':'',			
                        'email':'',
                        'phone':contact_no,
                        'website_id':website_id,
                        'created':django.utils.timezone.now(),
                        'modified':django.utils.timezone.now()
                    }
                    customer_obj=dict(customer_obj,**customer_obj)						
                    insertCustomer = EngageboostCustomers.objects.create(**customer_obj)
                    customer_id = insertCustomer.id if insertCustomer else 0
                    data = {
                        'status':1,
                        'new_customer_id': customer_id
                    }
            else:
                data = {
                        'status':0,
                    }

    return data

class OrderReturn(APIView):
    def get(self, request, invoiceno, format=None):
            website_id = request.META.get('HTTP_WID')
            warehouse_id = request.META.get('HTTP_WAREHOUSE')
            if website_id:
                pass
            else:
                website_id = 1
            # requestdata = JSONParser().parse(request)
            user                = request.user
            sold_by = user.first_name + ' ' + user.last_name
            custom_invoice_no   = str(invoiceno)[:-1]
            check_sum_digit     = str(invoiceno)[-1]
            data_arr = []
            invoice_rs = EngageboostInvoicemaster.objects.filter(isdeleted='n', isblocked='n', custom_invoice_id=custom_invoice_no, checksum_digit=check_sum_digit).first()
            if invoice_rs:
                order_query = EngageboostOrdermaster.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, id=invoice_rs.order_id).first()
                if order_query:
                    order_data = EngageboostOrderMasterSerializer(order_query).data
                    result = order_status_master(order_data['order_status'], order_data['buy_status'])
                    order_data.update({'status':result})
                    order_data.update({'sold_by':sold_by})
                    # for product in order_data['order_products']:
                    #     barcode_rs = EngageboostMultipleBarcodes.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, product_id=product['product']['id']).all()
                    #     if barcode_rs:
                    #         barcode_data = MultipleBarcodesSerializer(barcode_rs, many=True).data
                    #         product['product'].update({'barcode':barcode_data})
                    data_arr.append(order_data)
                    data = {
                        "status":1,
                        "message": 'Success',
                        "data":data_arr
                    }
                else:   
                    data = {
                        "status":0,
                        "message":'Order Not found.',
                        "data":[]
                    }
            else:
                data = {
                    "status":0,
                    "message":'Invoice Not Avalable.',
                    "data":[]
                }
                
            return Response (data)

    def post(self, request, format=None):
            website_id = request.META.get('HTTP_WID')
            warehouse_id = request.META.get('HTTP_WAREHOUSE')
            if website_id:
                pass
            else:
                website_id = 1
            requestdata         = JSONParser().parse(request)
            user                = request.user
            order_id            = requestdata['order_id']
            product_ids         = requestdata['product_ids']
            quantities          = requestdata['quantities']
            payment_method      = requestdata['return_payment_method']
            contact_no          = requestdata['contact_no']
            data                = {}
            return_amount       = 0
            return_earn_points  = 0
            data_arr            = []

            orderObj = EngageboostOrdermaster.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, id=order_id)
            order_query = orderObj.first()
            ##### Check user phone no is valid or not #####
            user_result = check_user(contact_no, website_id, order_query.customer_id)
            # data = {
            #         "status":0,
            #         "message": 'Order Not Avalable.',
            #         "data":user_result
            #     }
                
            # return Response (user_result)
            if order_query:
                if contact_no != "":
                    if user_result['status'] == 1:
                        order_data = EngageboostHoldOrderMasterSerializer(order_query).data
                        for index in range(len(product_ids)):
                            return_serializer_obj = {}
                            every_return_price = 0
                            product_id = product_ids[index]
                            return_quantity = quantities[index]
                            orderproductObj = EngageboostOrderProducts.objects.filter(order_id=order_id, product_id=product_id)
                            orderproduct_rs = orderproductObj.first()
                            if orderproduct_rs:
                                ##### Order Stock Return #####
                                request_data = {
                                        'website_id' : website_id,
                                        'company_id' : 1,
                                        'product_id' : product_id,
                                        'qtys' : return_quantity,
                                        'warehouse_id': orderproduct_rs.warehouse_id,
                                        'manage_type': 'return'
                                    }
                                stock_return = manage_stock(request_data)
                                if stock_return['status'] == 1:
                                    ### Insert Data In Engageboost Order Return Details Table ###
                                    return_obj = {
                                        "order_id":order_query.id,
                                        "website_id":website_id,
                                        "product_id":product_id,
                                        "return_by_id":order_query.customer_id,
                                        "quantity":return_quantity,
                                        "reason":'Product Return',
                                        "created":django.utils.timezone.now(),
                                        "modified":django.utils.timezone.now(),
                                        "return_status":'Authorized'
                                    }
                                    return_serializer_obj = dict(return_serializer_obj,**return_obj)
                                    save_return_order = EngageboostOrderReturnDetails.objects.create(**return_serializer_obj)
                                    return_order_id = save_return_order.id
                                    # print(return_order_id)
                                    every_return_price = float(orderproduct_rs.product_price) * float(return_quantity)
                                    return_amount += float(every_return_price)
                                    new_product_order_quentity = int(orderproduct_rs.quantity) - int(return_quantity) 
                                    orderproductObj.update(returns=return_quantity, deleted_quantity=return_quantity, quantity=new_product_order_quentity)
                                # print(orderproduct_rs)
                                
                                #### Return Earn Points ####
                                creditObj = EngageboostCustomerLoyaltypoints.objects.filter(customer_id=order_query.customer_id, order_id=order_query.id, status='earn')
                                credit_rs = creditObj.first()
                                if credit_rs is not None:
                                    earn_category_array = []
                                    earn_product_array = []
                                    customer_ids = []
                                    categories_rs = EngageboostProductCategories.objects.filter(isdeleted='n', isblocked='n', product_id=product_id).first()
                                    if categories_rs is not None:
                                        earn_category_array.append(categories_rs.category_id)
                                    earn_product_array.append(product_id)
                                    customer_ids.append(order_query.customer_id)
                                    request_data = {
                                        "website_id": website_id,
                                        "product_ids":earn_product_array,
                                        "price":order_query.net_amount,
                                        "customer_ids":customer_ids,
                                        "category_ids":earn_category_array,
                                        "rule_id":credit_rs.rule_id
                                    }
                                    creadit_points_return = get_creadit_points(request_data)
                                    if creadit_points_return['status'] == 1:
                                        return_earn_points += creadit_points_return['earn_point']
                                    # print('Earn Points', creadit_points_return)
                                    #### Update Loyalty points Table #####
                                    earn_points = int(credit_rs.received_points) - int(return_earn_points)
                                    new_earn_amount = float(credit_rs.received_points) - float(return_earn_points)
                                    creditObj.update(received_points=earn_points, amount=new_earn_amount)

                        
                        refund = return_payment(payment_method, contact_no, website_id)
                        if refund['status'] == 1:
                            new_order_amount = float(order_query.net_amount) - float(return_amount)
                            orderObj.update(net_amount=new_order_amount, net_amount_base=new_order_amount, paid_amount_base=new_order_amount, paid_amount=new_order_amount, received_amount=new_order_amount, gross_amount=new_order_amount, gross_amount_base=new_order_amount, modified=django.utils.timezone.now(), customer_id=user_result['new_customer_id'])
                            if float(order_query.net_amount) == float(return_amount):
                                order_status = 5
                                text = 'Full Refund'
                                orderObj.update(order_status=5, return_status=text)
                            else:
                                order_status = 6
                                text = 'Partial Refund'
                                orderObj.update(order_status=6, return_status=text)
                            data_arr.append(order_data)
                            data = {
                                "status":1,
                                "message": 'Success',
                                "data":return_amount
                            }
                        else:
                            data = {
                                "status":1,
                                "message": 'Payment Not Insert',
                                "data":return_amount
                            }
                    else:
                        data = {
                            "status":0,
                            "message": 'Phone no mismatch',
                            "data":[]
                        }
                else:
                    order_data = EngageboostHoldOrderMasterSerializer(order_query).data
                    for index in range(len(product_ids)):
                        return_serializer_obj = {}
                        every_return_price = 0
                        product_id = product_ids[index]
                        return_quantity = quantities[index]
                        orderproductObj = EngageboostOrderProducts.objects.filter(order_id=order_id, product_id=product_id)
                        orderproduct_rs = orderproductObj.first()
                        if orderproduct_rs:
                            ##### Order Stock Return #####
                            request_data = {
                                    'website_id' : website_id,
                                    'company_id' : 1,
                                    'product_id' : product_id,
                                    'qtys' : return_quantity,
                                    'warehouse_id': orderproduct_rs.warehouse_id,
                                    'manage_type': 'return'
                                }
                            stock_return = manage_stock(request_data)
                            if stock_return['status'] == 1:
                                ### Insert Data In Engageboost Order Return Details Table ###
                                return_obj = {
                                    "order_id":order_query.id,
                                    "website_id":website_id,
                                    "product_id":product_id,
                                    "return_by_id":order_query.customer_id,
                                    "quantity":return_quantity,
                                    "reason":'Product Return',
                                    "created":django.utils.timezone.now(),
                                    "modified":django.utils.timezone.now(),
                                    "return_status":'Authorized'
                                }
                                return_serializer_obj = dict(return_serializer_obj,**return_obj)
                                save_return_order = EngageboostOrderReturnDetails.objects.create(**return_serializer_obj)
                                return_order_id = save_return_order.id
                                # print(return_order_id)
                                every_return_price = float(orderproduct_rs.product_price) * float(return_quantity)
                                return_amount += float(every_return_price)
                                new_product_order_quentity = int(orderproduct_rs.quantity) - int(return_quantity) 
                                orderproductObj.update(returns=return_quantity, deleted_quantity=return_quantity, quantity=new_product_order_quentity)
                            # print(orderproduct_rs)
                            
                            #### Return Earn Points ####
                            creditObj = EngageboostCustomerLoyaltypoints.objects.filter(customer_id=order_query.customer_id, order_id=order_query.id, status='earn')
                            credit_rs = creditObj.first()
                            if credit_rs is not None:
                                earn_category_array = []
                                earn_product_array = []
                                customer_ids = []
                                categories_rs = EngageboostProductCategories.objects.filter(isdeleted='n', isblocked='n', product_id=product_id).first()
                                if categories_rs is not None:
                                    earn_category_array.append(categories_rs.category_id)
                                earn_product_array.append(product_id)
                                customer_ids.append(order_query.customer_id)
                                request_data = {
                                    "website_id": website_id,
                                    "product_ids":earn_product_array,
                                    "price":order_query.net_amount,
                                    "customer_ids":customer_ids,
                                    "category_ids":earn_category_array,
                                    "rule_id":credit_rs.rule_id
                                }
                                creadit_points_return = get_creadit_points(request_data)
                                if creadit_points_return['status'] == 1:
                                    return_earn_points += creadit_points_return['earn_point']
                                # print('Earn Points', creadit_points_return)
                                #### Update Loyalty points Table #####
                                earn_points = int(credit_rs.received_points) - int(return_earn_points)
                                new_earn_amount = float(credit_rs.received_points) - float(return_earn_points)
                                creditObj.update(received_points=earn_points, amount=new_earn_amount)

                    
                    refund = return_payment(payment_method, '0000000000', website_id)
                    if refund['status'] == 1:
                        new_order_amount = float(order_query.net_amount) - float(return_amount)
                        orderObj.update(net_amount=new_order_amount, net_amount_base=new_order_amount, paid_amount_base=new_order_amount, paid_amount=new_order_amount, received_amount=new_order_amount, gross_amount=new_order_amount, gross_amount_base=new_order_amount, modified=django.utils.timezone.now())
                        if float(order_query.net_amount) == float(return_amount):
                            order_status = 5
                            text = 'Full Refund'
                            orderObj.update(order_status=5, return_status=text)
                        else:
                            order_status = 6
                            text = 'Partial Refund'
                            orderObj.update(order_status=6, return_status=text)
                        data_arr.append(order_data)
                        data = {
                            "status":1,
                            "message": 'Success',
                            "data":return_amount
                        }
                    else:
                        data = {
                            "status":1,
                            "message": 'Payment Not Insert',
                            "data":return_amount
                        }
            else:
                data = {
                    "status":0,
                    "message": 'Order Not Avalable.',
                    "data":[]
                }
                
            return Response (data)

class OrderReturnAmountDetals(APIView):

    def post(self, request, format=None):
            website_id = request.META.get('HTTP_WID')
            if website_id:
                pass
            else:
                website_id = 1
            requestdata         = JSONParser().parse(request)
            user                = request.user
            order_id            = requestdata['order_id']
            product_ids         = requestdata['product_ids']
            quantities          = requestdata['quantities']
            data                = {}
            return_amount       = 0
            full_paid_in_loyalty = 'No'
            payment_array = []
            #### Get Global settings ####
            global_rs = EngageboostGlobalSettings.objects.filter(website_id=website_id).first()

            orderObj = EngageboostOrdermaster.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, id=order_id)
            order_query = orderObj.first()
            if order_query:
                order_data = EngageboostHoldOrderMasterSerializer(order_query).data
                for index in range(len(product_ids)):
                    every_return_price = 0
                    product_id = product_ids[index]
                    return_quantity = quantities[index]
                    orderproductObj = EngageboostOrderProducts.objects.filter(order_id=order_id, product_id=product_id)
                    orderproduct_rs = orderproductObj.first()
                    if orderproduct_rs:
                        every_return_price = float(orderproduct_rs.product_price) * float(return_quantity)
                        return_amount += float(every_return_price)
                #### Get payment Details ####
                payment_rs = EngageboostOrderPaymentDetails.objects.filter(isdeleted='n', isblocked='n', order_id_id=order_id, status='pay').all()
                print(payment_rs.query)
                if payment_rs:
                    payment_data = ReturnOrderPaymentDetailsSerializer(payment_rs, many=True).data
                    if payment_data:
                        payment_array = []
                        for pay in payment_data:
                            request_data ={} 
                            request_data ={
                                'order_amount':pay['order_amount'],
                                'return_amount':return_amount,
                                'payment_amount':pay['payment_amount']
                            }
                            print('pay', pay)
                            # get_return = get_split_payment_percentage(request_data)
                            # if get_return['status'] == 1:
                            #     pay.update({'pay_percentage':get_return['pay_percentage'],'return_amount':get_return['return_amount']})

                            if global_rs:
                                if global_rs.payment_return_method == 'Y':
                                    full_paid_in_loyalty = 'Yes'
                                    payment_array = []
                                    pay.update({'pay_percentage':100,'return_amount':return_amount, 'payment_method_id':24, "payment_method_name": "Loyalty"})
                                    payment_array.append(pay)
                                else:
                                    get_return = get_split_payment_percentage(request_data)
                                    if get_return['status'] == 1:
                                        pay.update({'pay_percentage':get_return['pay_percentage'],'return_amount':get_return['return_amount']})
                                        payment_array = payment_data
                            else:
                                get_return = get_split_payment_percentage(request_data)
                                if get_return['status'] == 1:
                                    pay.update({'pay_percentage':get_return['pay_percentage'],'return_amount':get_return['return_amount']})
                                    payment_array = payment_data
                        # payment_array.append({'full_paid_in_loyalty':full_paid_in_loyalty})
                data = {
                    "status":1,
                    "message": 'Success',
                    "data":payment_array,
                }
            else:
                data = {
                    "status":0,
                    "message": 'Falure',
                    "data":[]
                }
                
            return Response (data)

class ReturnOrderListBySoldby(APIView):

    def post(self, request, format=None):
        website_id = request.META.get('HTTP_WID')
        if website_id:
            pass
        else:
            website_id = 1       
        requestdata = JSONParser().parse(request)
        user  = request.user
        sold_by = user.first_name + ' ' + user.last_name
        search_by       = requestdata['search_by'].upper()
        # customer_name   = requestdata['customer_name']        
        # order_date      = requestdata['order_date']         
        # receipt_no      = requestdata['receipt_no']
        start_index     = requestdata['start_index']
        no_of_list 	    = requestdata['no_of_list']
        user            = request.user
        data            = {}

        order_query = EngageboostOrdermaster.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, order_status__in=[6,5]).filter(createdby=user.id).all()
        
        if search_by:
            order_query = order_query.filter(custom_order_id__icontains=search_by)
        ##### Set Pagination ####
        if no_of_list == 0 and start_index == 0:
            data['no_of_page'] = 1
            data['next_start_index'] = 0
            data['prev_start_index'] = 0
        else:
            data['no_of_page'] = int(len(order_query) / no_of_list) if(int(len(order_query) % no_of_list) == 0) else int(len(order_query) / no_of_list) + 1
            data['next_start_index'] = start_index if int(start_index + no_of_list) >= len(order_query) else int(start_index + no_of_list)
            data['prev_start_index'] = start_index if int(start_index - no_of_list) < 0 else int(start_index - no_of_list)
        data['total_number_row'] = len(order_query)
        if no_of_list != 0:
            order_query = order_query.order_by('-id')[int(start_index):int(start_index) + int(no_of_list)]
        order_details =  ReturnOrderListSerializer(order_query, many=True)
        order_data = order_details.data
        if order_data:
            for order in order_data:
                result = order_status_master(order['order_status'], order['buy_status'])
                order.update({'status':result})
                order.update({'sold_by':sold_by})
            data.update({"status":1, "data":order_details.data})         
        else:
            data = {
                "status":0,
                "data":"Data not found."
            }
        return Response (data)

    def get(self, request, order_id, format=None):
        website_id = request.META.get('HTTP_WID')
        if website_id:
            pass
        else:
            website_id = 1       
        user        = request.user
        sold_by     = user.first_name + ' ' + user.last_name
        order_id    = order_id
        data        = {}
        order_query = EngageboostOrdermaster.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, pk=order_id).first()
        if order_query is not None:
            order_details =  ReturnOrderDetailsSerializer(order_query)
            order_data = order_details.data
            order_status = order_status_master(order_data['order_status'], order_data['buy_status'])
            if order_status:
                order_data['received_status'] = order_status
            if order_data:        
                data = {
                    "status":1,
                    "message": 'Success',
                    "data":order_data
                }
            else:
                data = {
                    "status":0,
                    "message": 'Falure',
                    "data":[]
                }
        else:
            data = {
                "status":0,
                "message": 'Falure',
                "data":[]
            }
        return Response (data)