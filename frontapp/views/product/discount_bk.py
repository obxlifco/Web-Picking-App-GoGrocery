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

# Import Model And Serializer
from webservices.models import *
# from frontapp.frontapp_serializers import *
from coremodule.coremodule_serializers import *

import json
import base64

import sys,math
import traceback

import datetime
from pytz import timezone
from decimal import Decimal


class ProductDiscountCalculation(APIView):
    def post(self, request, format=None):
        # company_db = loginview.db_active_connection(request)
        company_id = request.data["company_id"]
        website_id = request.data["website_id"]
        webshop_id = request.data["webshop_id"] if request.data.get("webshop_id") else 6
        product_ids= request.data["product_ids"]
        qtys       = request.data["qtys"]
        prod_price = request.data["prod_price"]
        country_id = request.data["country_id"] if request.data.get("country_id") else ""
        state_id = request.data["state_id"] if request.data.get("state_id") else ""
        post_code = request.data["post_code"] if request.data.get("post_code") else ""
        payment_method_id = request.data["payment_method_id"] if request.data.get("payment_method_id") else None
        user_id = request.data["user_id"] if request.data.get("user_id") else None
        user_group_id = request.data["user_group_id"] if request.data.get("user_group_id") else None
        coupon_code = request.data["coupon_code"] if request.data.get("coupon_code") else None
        paid_amount = float(request.data["paid_amount"]) if request.data.get("paid_amount") else float(0)

        cartdetails=[];checkout_info=[];new_unit_netamount=[];new_total_netamount=[]

        shipper_address=EngageboostCompanyWebsites.objects.filter(id=website_id).first()
        cod_min_amount=cod_max_amount=None
        cod_charge=0
        if payment_method_id:
            if int(payment_method_id)==15 or int(payment_method_id)==16:
                payment_method_onepage=payment_method_onepage_checkout(website_id)
            else:
                payment_method_onepage=payment_method_onepage_checkout(website_id)
        else:
            payment_method_onepage=payment_method_onepage_checkout(website_id)

        # return Response(payment_method_onepage)
        for value in payment_method_onepage:
            if value['payment_type_id']==4:
                # flag=False
                if value["setting_key"]=="min_amount":
                    cod_min_amount=float(value["setting_val"])
                if value["setting_key"]=="max_amount":
                    cod_max_amount=float(value["setting_val"])
                if value["setting_key"]=="cod_charge":
                    cod_charge=float(value["setting_val"])

        product_ids=product_ids.split(",")
        quantity=qtys.split(",")
        prod_price=prod_price.split(",")
        for index in range(len(product_ids)):
            product_id = product_ids[index]
            # checkout_info_dict = {"product_id":product_ids[index],"quantity":quantity[index],"product_price":prod_price[index]}
            # checkout_info.append(checkout_info_dict)
            new_unit_netamount.append(float(prod_price[index])/float(quantity[index]))
            new_total_netamount.append(float(prod_price[index])*float(quantity[index]))
            discount_array_net = generate_discount_conditions(website_id,user_group_id)
            getproductforcart_net = getproductforcart(product_id)
            for getproductforcartnet in getproductforcart_net:
                getproductforcartnet["qty"]=quantity[index]
                try:
                    if getproductforcartnet["new_default_price"]: getproductforcartnet["new_default_price"] = getproductforcartnet["new_default_price"]
                    else: getproductforcartnet["new_default_price"] = getproductforcartnet["default_price"]
                except KeyError: getproductforcartnet["new_default_price"] = getproductforcartnet["default_price"]

            #********Apply Discount and Get New Product Amount********#
            product_detail_net = genrate_new_prodcut_with_discount(user_id,getproductforcart_net,discount_array_net)
            product_detail_net = product_detail_net[0]

            #********Tax Calculation********#
            # if country_id!="" or state_id!="" or post_code!="":
            tax_price_arr = get_price_including_tax(website_id,company_id,product_detail_net,country_id,state_id,post_code,'back')

            company_info = EngageboostCompanyWebsites.objects.filter(id=website_id).first()
            if company_info:
                company_state=company_info.state
            else:
                company_state=0

            if str(company_state)!=str(state_id):
                product_tax={"tax_price_unit":float(tax_price_arr["tax_igst"]),"tax_price":float(tax_price_arr["tax_igst"])*float(product_detail_net["qty"]),"tax_percentage":tax_price_arr["igst"],"tax_name":tax_price_arr["tax_name"],"cgst":tax_price_arr["cgst"],"sgst":tax_price_arr["sgst"],"igst":tax_price_arr["igst"],"cess":tax_price_arr["cess"],"is_igst":"yes","tax_type":tax_price_arr["tax_type"]}
            else:
                product_tax={"tax_price_unit":float(tax_price_arr["tax_igst"]),"tax_price":float(tax_price_arr["tax_igst"])*float(product_detail_net["qty"]),"tax_percentage":tax_price_arr["igst"],"tax_name":tax_price_arr["tax_name"],"cgst":tax_price_arr["cgst"],"sgst":tax_price_arr["sgst"],"igst":tax_price_arr["igst"],"cess":tax_price_arr["cess"],"is_igst":"no","tax_type":tax_price_arr["tax_type"]}
            
            product_detail_net=dict(product_detail_net,**product_tax)

            if product_detail_net["tax_type"]=="including":
                product_detail_net["new_default_price_unit"]=float(product_detail_net["new_default_price_unit"])-float(product_detail_net["tax_price_unit"])
                product_detail_net["new_default_price"]=float(product_detail_net["new_default_price"])-float(product_detail_net["tax_price"])
            #********Tax Calculation (END)********#

            cartdetails.append(product_detail_net)

        order_total=0
        order_weight=0
        if cartdetails:
            for products in cartdetails:
                if products["tax_type"]=="including":
                    order_total = float(order_total)+float(products["new_default_price"])+float(products["tax_price"])
                else:
                    order_total = float(order_total)+float(products["new_default_price"])
                if products["weight"]:
                    order_weight = float(order_weight)+float(products["weight"])

        #********Shipping Calculation********#
        shipping_amount_arr={"shipping_amount":0,"mthod_type":0,"mthod_name":"orderwise","handling_fees_type":0,"handling_price":0}
        if cartdetails:
            shipping_flat = rate_flat(website_id,company_id,country_id,state_id,post_code,'back')
            shipping_table = rate_table(website_id,company_id,cartdetails,country_id,state_id,post_code,'back')
            shipping_free = rate_free(website_id,company_id,country_id,state_id)

            if shipping_flat:
                if float(shipping_flat["flat_price"])>float(0) and float(order_total)<float(shipping_free["minimum_order_amount"]):
                    shipping_amount_arr={"shipping_amount":float(shipping_flat["flat_price"]),"mthod_type":shipping_flat["mthod_type"],"mthod_name":shipping_flat["mthod_name"],"handling_fees_type":shipping_flat["handling_fees_type"],"handling_price":shipping_flat["handling_price"]}

            if shipping_table:
                if float(shipping_table["flat_price"])>float(0) and float(order_total)<float(shipping_free["minimum_order_amount"]):
                    shipping_amount_arr={"shipping_amount":float(shipping_table["flat_price"]),"mthod_type":shipping_table["mthod_type"],"mthod_name":shipping_table["mthod_name"],"handling_fees_type":shipping_table["handling_fees_type"],"handling_price":shipping_table["handling_price"]}
        #********Shipping Calculation (END)********#

        #********APPLY COUPON CODE********#
        if cartdetails and coupon_code is not None:
            discount_array_coupon=generate_discount_conditions_coupon(website_id,user_group_id,coupon_code)

            if discount_array_coupon and discount_array_coupon[0]["name"]!="invalid":
                if discount_array_coupon[0]["disc_type"]!=3:
                    if discount_array_coupon[0]["coupon_type"]==2:
                        cartdetails=genrate_new_prodcut_with_discount_coupon(user_id,cartdetails,discount_array_coupon,order_total)
                    else:
                        if discount_array_coupon[0]["used_coupon"]==0:
                            cartdetails=genrate_new_prodcut_with_discount_coupon(user_id,cartdetails,discount_array_coupon,order_total)
                else:
                    if discount_array_coupon[0]["coupon_type"]==2:
                        coupon_details=genrate_new_prodcut_with_discount_coupon_order_total(user_id,cartdetails,discount_array_coupon,order_total)
                    else:
                        if discount_array_coupon[0]["used_coupon"]==0:
                            coupon_details=genrate_new_prodcut_with_discount_coupon_order_total(user_id,cartdetails,discount_array_coupon,order_total)
        #********APPLY COUPON CODE (END)********#
        orderamountdetails=[]
        applied_coupon=[]
        order_total=0
        order_weight=0
        total_tax=0
        shipping_amount=0
        handling_charge=0
        order_total_with_handling_price=0
        gross_discount_amount = 0
        grandtotal=subtotal=nettotal=cart_discount=0
        if cartdetails:
            for products in cartdetails:
                order_total = float(order_total)+float(products["new_default_price"])+float(products["tax_price"])
                total_tax = float(total_tax)+float(products["tax_price"])
                #********PRODUCT TOTAL DISCOUNT (EXCLUDING WHOLE CART DISCOUNT)********#
                gross_discount_amount = float(gross_discount_amount)+float(products["discount_price"])

                if shipping_amount_arr["mthod_type"]!=0:
                    shipping_price=float(shipping_amount_arr["shipping_amount"])*float(products["qty"])
                    shipping_amount=float(shipping_amount)+float(shipping_price)
                else:
                    shipping_amount=float(shipping_amount_arr["shipping_amount"])

            if shipping_amount_arr["handling_fees_type"]==0:
                handling_charge = shipping_amount_arr["handling_price"]
                order_total_with_handling_price = float(order_total)+float(handling_charge)
            else:
                handling_charge = float(order_total)*float(shipping_amount_arr["handling_price"])/float(100)
                order_total_with_handling_price = float(order_total)+float(handling_charge)

            #********TOTAL AMOUNT PRODUCT PRICE + SHIPPING CHARGE + HANDLING CHARGE ********#
            grandtotal = float(order_total_with_handling_price)+float(shipping_amount)

            #********APPLY COD CHAGE********#
            if cod_min_amount is not None and cod_max_amount is not None:
                if float(cod_min_amount)<=float(grandtotal) and float(grandtotal)<=float(cod_max_amount):
                    grandtotal = float(grandtotal)+float(cod_charge)
                    applied_cod_charge = float(cod_charge)
                else:
                    grandtotal = grandtotal
                    applied_cod_charge = float(0)
            else:
                grandtotal = grandtotal
                applied_cod_charge = float(0)

            #********APPLY COUPON DISCOUNT ON WHOLE CART********#
            if coupon_code is not None:
                if discount_array_coupon and discount_array_coupon[0]["name"]!="invalid":
                    if discount_array_coupon[0]["disc_type"]==3:
                        grandtotal = float(grandtotal)
                        subtotal = float(grandtotal)-float(coupon_details["coupon_discount_amount"])
                        cart_discount = float(grandtotal)-float(subtotal)
                    else:
                        grandtotal = float(grandtotal)
                        subtotal = float(grandtotal)
                        cart_discount = float(grandtotal)-float(subtotal)

                    applied_coupon_dict={"name":discount_array_coupon[0]["name"],"coupon_code":discount_array_coupon[0]["coupon_code"],"disc_type":discount_array_coupon[0]["disc_type"],"amount":discount_array_coupon[0]["amount"]}
                    applied_coupon.append(applied_coupon_dict)
                else:
                    grandtotal = float(grandtotal)
                    subtotal = float(grandtotal)
                    cart_discount = float(grandtotal)-float(subtotal)
                    applied_coupon_dict={"name":discount_array_coupon[0]["name"],"coupon_code":discount_array_coupon[0]["coupon_code"],"message":discount_array_coupon[0]["message"]}
                    applied_coupon.append(applied_coupon_dict)
            else:
                grandtotal = float(grandtotal)
                subtotal = float(grandtotal)
                cart_discount = float(grandtotal)-float(subtotal)
            #********APPLY COUPON DISCOUNT ON WHOLE CART(END)********#

        nettotal = float(subtotal)-float(total_tax)-float(shipping_amount)-float(handling_charge)-float(applied_cod_charge)
        balance_due = float(subtotal)-float(paid_amount)
        orderamountdetails_dict={"company_id":company_id,"website_id":website_id,"webshop_id":webshop_id,"payment_method_id":payment_method_id,"tax_amount":total_tax,"shipping_charge":shipping_amount,"handling_charge":handling_charge,"cod_charge":applied_cod_charge,"gross_discount":gross_discount_amount,"min_amount":cod_min_amount,"max_amount":cod_max_amount,"grand_total":grandtotal,"sub_total":subtotal,"net_total":nettotal,"cart_discount":cart_discount,"paid_amount":paid_amount,"balance_due":balance_due}
        orderamountdetails.append(orderamountdetails_dict)
        data={"cartdetails":cartdetails,"orderamountdetails":orderamountdetails,"applied_coupon":applied_coupon,"shipping_flat":shipping_flat,"shipping_table":shipping_table}

        return Response(data)


def generate_discount_conditions(website_id,user_group_id,discountIds=None, warehouse_id = None):
    now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
    if user_group_id:
        if warehouse_id is not None:
            DiscountMasterCond = EngageboostDiscountMasters.objects.order_by("discount_priority").filter(website_id=website_id,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc,customer_group__iregex=r"\y{0}\y".format(user_group_id),isdeleted='n',isblocked='n',discount_master_type=0, warehouse_id__iregex=r"\y{0}\y".format(warehouse_id)).all()
        else:
            DiscountMasterCond = EngageboostDiscountMasters.objects.order_by("discount_priority").filter(website_id=website_id,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc,customer_group__iregex=r"\y{0}\y".format(user_group_id),isdeleted='n',isblocked='n',discount_master_type=0).all()
    else:
        if warehouse_id is not None:
            DiscountMasterCond = EngageboostDiscountMasters.objects.order_by("discount_priority").filter(website_id=website_id,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc,isdeleted='n',isblocked='n',discount_master_type=0, warehouse_id__iregex=r"\y{0}\y".format(warehouse_id)).all()
        else:
            DiscountMasterCond = EngageboostDiscountMasters.objects.order_by("discount_priority").filter(website_id=website_id,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc,isdeleted='n',isblocked='n',discount_master_type=0).all()
    if discountIds:
        DiscountMasterCond = DiscountMasterCond.filter(id__in=discountIds)
    DiscountMasterSerializerData = DiscountMasterSerializer(DiscountMasterCond,many=True)

    if DiscountMasterSerializerData:
        for DiscountMaster in DiscountMasterSerializerData.data:
            DiscountMastersConditionsCond = EngageboostDiscountMastersConditions.objects.filter(discount_master_id=DiscountMaster["id"]).all()
            if DiscountMastersConditionsCond:
                DiscountMastersConditionsSerializerData = DiscountConditionsSerializer(DiscountMastersConditionsCond,many=True)
                DiscountMastersConditionsSerializerData = DiscountMastersConditionsSerializerData.data
            else:
                DiscountMastersConditionsSerializerData = []

            DiscountMaster["discount_conditions"] = DiscountMastersConditionsSerializerData
    return DiscountMasterSerializerData.data

def getproductforcart(product_id,warehouse_id=None):
    # condition = EngageboostProducts.objects.filter(isdeleted='n',isblocked='n',id=product_id).values("id","name","brand","hsn_id","sku","slug","description","default_price","weight","taxclass_id","amazon_itemid","twitter_addstatus","amazon_addstatus","status","warehouse").first()
    # condition = EngageboostProducts.objects.filter(isdeleted='n',isblocked='n',id=product_id).first()
    condition = EngageboostProducts.objects.filter(id=product_id).first()
    if warehouse_id is not None:
        context = {"warehouse_id": warehouse_id}
        product_details = BasicinfoSerializer(condition, context=context)
    else:
         product_details = BasicinfoSerializer(condition)

    product_details = product_details.data
    # print(product_details)
    qs_price_data = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=product_id, warehouse_id=warehouse_id, product_price_type_id__price_type_id=1).first()
    # qs_price_data = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=product_id, warehouse_id=warehouse_id).first()
    if qs_price_data:
        product_details.update({"channel_price":qs_price_data.price})
        product_details['default_price'] = qs_price_data.price
    else:
        product_details.update({"channel_price":0})
        product_details['default_price'] = 0

    conditions = EngageboostProductCategories.objects.filter(product_id=product_id).first()
    if conditions:
        product_details["category_id"]=conditions.category_id
    
    return product_details

def genrate_new_prodcut_with_discount(user_id=None,product_array=None,discount_array_new=None,category_id=None,sub_category_id=None,cart_subtotal=None):
    # print(json.dumps(discount_array_new, indent=4, sort_keys=True))
    if discount_array_new:
        for discount_array in discount_array_new:
            # for product in product_array:
            return_price = check_in_prod_disc(user_id,product_array,discount_array,category_id,sub_category_id,cart_subtotal)
            price_array = return_price.split('^')
            if price_array[2] != "false":
                if price_array[1] != "product" and float(price_array[1])!= 0.0 and float(product_array["channel_price"]) != float(price_array[0]):
                    product_array["new_default_price_unit"]   = float(product_array["channel_price"])-float(price_array[1])
                    product_array["new_default_price"]        = (float(product_array["channel_price"])-float(price_array[1]))*float(product_array["qty"])  #float(price_array[0])*float(product_array["qty"])
                    product_array["discount_price_unit"]      = float(price_array[1])
                    product_array["discount_price"]           = float(price_array[1])*float(product_array["qty"])
                    product_array["discount_amount"]          = float(discount_array["amount"])
                    product_array["disc_type"]                = discount_array["disc_type"]
                    product_array["coupon"]                   = discount_array["name"]
                else:
                    product_array["new_default_price_unit"] = float(product_array["channel_price"]) if product_array["channel_price"] else 0.0
                    if product_array["default_price"] and product_array["qty"]:
                        product_array["new_default_price"] = float(product_array["channel_price"])*int(product_array["qty"])
                    else:
                        product_array["new_default_price"] = 0.0
                    product_array["discount_price_unit"] = float(price_array[1])
                    product_array["discount_price"] = float(price_array[1])*float(product_array["qty"])
                    product_array["discount_amount"] = 0.0
                    product_array["disc_type"] = ""
                    product_array["coupon"] = ""
            # else:
            #     product_array["new_default_price_unit"] = float(product_array["channel_price"]) if product_array["channel_price"] else 0.0
            #     if product_array["default_price"] and product_array["qty"]:
            #         product_array["new_default_price"] = float(product_array["channel_price"])*int(product_array["qty"])
            #     else:
            #         product_array["new_default_price"] = 0.0
            #     product_array["discount_price_unit"] = float(price_array[1])
            #     product_array["discount_price"] = float(price_array[1])*float(product_array["qty"])
            #     product_array["discount_amount"] = 0.0
            #     product_array["disc_type"] = ""
            #     product_array["coupon"] = ""
          
    else:
        # for product in product_array:
        product_array["new_default_price_unit"] = float(product_array["default_price"]) if product_array["default_price"] is not None else 0
        if product_array["default_price"]:
            product_array["new_default_price"] = float(product_array["default_price"])*int(product_array["qty"])
        else:
            product_array["new_default_price"] = 0.00

        product_array["discount_price_unit"] = float(0)
        product_array["discount_price"] = float(0)*int(product_array["qty"])
        product_array["discount_amount"] = float(0)
        product_array["disc_type"] = ""
        product_array["coupon"] = ""

    return product_array

def check_in_prod_disc(user_id=None,ind_product=None,discount_array=None,category_id=None,sub_category_id=None,cart_subtotal=None):
    discount_array_condition = discount_array["discount_conditions"]
    product_array_disc_applied = []
    i=0
    previos_flag = "false"
    for ind_cond in discount_array_condition:
        if ind_cond["fields"]==-1:
            if cart_subtotal:
                if ind_cond["condition"] == "==":
                    flag = "true" if float(cart_subtotal) == float(ind_cond["value"]) else "false"
                elif ind_cond["condition"] == ">=":
                    flag = "true" if float(cart_subtotal) >= float(ind_cond["value"]) else "false"
                else:
                    flag = "false" if float(cart_subtotal) >= float(ind_cond["value"]) else "true"
            else:
                flag = "false"
        elif ind_cond["all_category_id"]:
            category_id_array = ind_cond["all_category_id"].split(",")
            find_category = EngageboostProductCategories.objects.filter(product_id=ind_product["id"]).all()
            sub_category_id_array = []               
            
            if find_category:
                ptcArr = ProductCategoriesSerializer(find_category,many=True)
                for pro in ptcArr.data:
                    sub_category_id_array.append(pro["category_id"])

            if sub_category_id_array:
                for index in range(len(sub_category_id_array)):
                    if ind_cond["condition"] == "==":
                        if str(sub_category_id_array[index]) in category_id_array:
                            flag = "true"
                            break
                        else:
                            flag = "false"
                    else:
                        if str(sub_category_id_array[index]) in category_id_array:
                            flag = "false"
                            break
                        else:
                            flag = "true"
            else:
                if ind_cond["condition"] == "==": 
                    if category_id in category_id_array:
                        flag = "true"
                    else:
                        flag = "false"
                else:
                    if category_id in category_id_array:
                        flag = "false"
                    else:
                        flag = "true"
        elif ind_cond["all_product_id"]:
            product_id_array = ind_cond["all_product_id"].split(",")
            # print(ind_product["id"])
            if ind_cond["condition"] == "==":
                if str(ind_product["id"]) in product_id_array:
                    flag = "true"
                else:
                    flag = "false"
            else:
                if ind_product["id"] in product_id_array:
                    flag = "false"
                else:
                    flag = "true"
        elif ind_cond["all_customer_id"]:
            customer_id_array = ind_cond["all_customer_id"].split(",")
            if user_id:
                if ind_cond["condition"] == "==":
                    if user_id in customer_id_array:
                        flag = "true"
                    else:
                        flag = "false"
                else:
                    if user_id in customer_id_array:
                        flag = "false"
                    else:
                        flag = "true"
            else:
                flag = "false"
        if i!=0:
            if previos_condition=="AND":
                if flag=="true" and previos_flag=="true":
                    previos_flag="true"
                else:
                    previos_flag="false"

            if previos_condition=="OR":
                if flag=="false" and previos_flag=="false":
                    previos_flag="false"
                else:
                    previos_flag="true"
        else:
            previos_flag = flag

        previos_condition=ind_cond["condition_type"]
        i=i+1

    if previos_flag == "true":
        if discount_array["disc_type"]==1:
            discount_array["discountPrice"]=float(ind_product["default_price"])*float(discount_array["amount"])/float(100)
        else:
            discount_array["discountPrice"]=float(discount_array["amount"])

        if discount_array["disc_type"]!=4:
            if ind_product["new_default_price"]:
                if ind_product["new_default_price"]=="0":
                    if float(ind_product["default_price"])>float(discount_array["discountPrice"]):
                        default_price=float(ind_product["default_price"])-float(discount_array["discountPrice"])
                        discount_price=float(ind_product["discount_price"])+float(discount_array["discountPrice"])
                    else:
                        default_price=float(ind_product["default_price"])
                        discount_price=float(ind_product["discount_price"])

                    product_array_disc_applied.append(ind_product["id"])
                else:
                    if float(ind_product["default_price"])>float(discount_array["discountPrice"]):
                        default_price = float(ind_product["new_default_price"])-float(discount_array["discountPrice"])
                        discount_price = float(discount_array["discountPrice"])
                    else:
                        default_price = float(ind_product["new_default_price"])
                        discount_price = float(0)
                    product_array_disc_applied.append(ind_product["id"])
            else:
                if float(ind_product["default_price"])>float(discount_array["discountPrice"]):
                    default_price=float(ind_product["default_price"])-float(discount_array["discountPrice"])
                    discount_price=float(discount_array["discountPrice"])
                    product_array_disc_applied.append(ind_product["id"])
                else:
                    default_price  = float(0)
                    discount_price = float(0)
        else:
            default_price = discount_array["product_id"]
            discount_price = "product"
    else:
        if ind_product["new_default_price"]:
            default_price = float(ind_product["new_default_price"])
            discount_price = float(0)
        else:
            default_price  = float(0)
            discount_price = float(0)
    # return $default_price."^".$discount_price."^".$previos_flag."^".$discount_array['DiscountMaster']['amount']."^".$discount_array['DiscountMaster']['disc_type'];
    return str(default_price)+"^"+str(discount_price)+"^"+str(previos_flag)
    

def get_price_including_tax(website_id='1',company_id=None,product_arr=None,country_id=None,state_id=None,post_code=None,order_from='front'):
    state_id=state_id
    tax_price_arr = []
    tax_price = "0.00"
    excise_duty = "0.00"
    discount_price = "0.00"
    coupon_disc_amount_nw = "0.00"
    is_tax_find = 'No'
    tax_name = ""
    tax_rate = "0.00"
    rate_of_duty  = "0.00"
    tax_type = "excluding"

    if product_arr["hsn_id"]:
        hsnDetails = EngageboostHsnCodeMaster.objects.filter(id=product_arr["hsn_id"]).first()
        if hsnDetails:
            tax_rate = hsnDetails.igst
            if tax_type=="excluding":
                tax_price = float(product_arr["new_default_price_unit"])*float(tax_rate)/float(100)
                data={"tax_cgst":float(tax_price)/float(2),"tax_sgst":float(tax_price)/float(2),"tax_igst":float(tax_price),"tax_name":hsnDetails.hsn_code,"cgst":float(tax_rate)/float(2),"sgst":float(tax_rate)/float(2),"igst":float(tax_rate),"cess":float(hsnDetails.cess),"tax_type":"excluding"}
            else:
                tax_price = (float(product_arr["new_default_price_unit"])*float(tax_rate))/(float(100)+float(tax_rate))
                data={"tax_cgst":float(tax_price)/float(2),"tax_sgst":float(tax_price)/float(2),"tax_igst":float(tax_price),"tax_name":hsnDetails.hsn_code,"cgst":float(tax_rate)/float(2),"sgst":float(tax_rate)/float(2),"igst":float(tax_rate),"cess":float(hsnDetails.cess),"tax_type":"including"}
        else:
            data={"tax_cgst":float(0),"tax_sgst":float(0),"tax_igst":float(0),"tax_name":"","cgst":float(0),"sgst":float(0),"igst":float(0),"cess":float(0),"tax_type":""}
    else:
        data={"tax_cgst":float(0),"tax_sgst":float(0),"tax_igst":float(0),"tax_name":"","cgst":float(0),"sgst":float(0),"igst":float(0),"cess":float(0),"tax_type":""}

    return data

def rate_flat(website_id='1',company_id=None,country_id=None,state_id=None,post_code=None,order_from='front',warehouse_id=None, str_from=None):
    #******** FOR FLAT RATE CALCULATION ********#
    
    zone_id=''
    isShippingChargeFound = False
    if warehouse_id is not None:
        zonemaster_exists = EngageboostZoneMasters.objects.filter(warehouse_id=warehouse_id,location_type='Z',isblocked='n',isdeleted='n').exists()
    
        if zonemaster_exists:
            zonemaster_qs = EngageboostZoneMasters.objects.filter(warehouse_id=warehouse_id,location_type='Z',isblocked='n',isdeleted='n').latest('id')

            if zonemaster_qs:
                zone_id = zonemaster_qs.id
            else:
                zone_id=''
                
        else:
            zone_id=''
    # print("zone_id====", zone_id)
    data={"shipping_type":"Flat Shipping","mthod_type":0,"mthod_name":"orderwise","flat_price":float(0),"handling_fees_type":0,"handling_price":float(0)}
    if state_id and zone_id and zone_id !='':
        conditions = EngageboostShippingMastersSettings.objects.filter(website_id=website_id,country_ids__iregex=r"\y{0}\y".format(country_id),zone_id__iregex=r"\y{0}\y".format(zone_id),shipping_method_id='4',isblocked='n',isdeleted='n').all()
        isShippingChargeFound = True

    elif state_id is None and zone_id and zone_id !='':
        conditions = EngageboostShippingMastersSettings.objects.filter(website_id=website_id,country_ids__iregex=r"\y{0}\y".format(country_id),zone_id__iregex=r"\y{0}\y".format(zone_id),shipping_method_id='4',isblocked='n',isdeleted='n').all()
        isShippingChargeFound = True

    elif state_id and zone_id =='':
        conditions = EngageboostShippingMastersSettings.objects.filter(website_id=website_id,country_ids__iregex=r"\y{0}\y".format(country_id),state_id__iregex=r"\y{0}\y".format(state_id),shipping_method_id='4',isblocked='n',isdeleted='n').all()
        isShippingChargeFound = True
    else:
        if str_from is None:
            GlobalSettings_qs = EngageboostGlobalSettings.objects.filter(isblocked='n',isdeleted='n').first()
            shipping_charge = GlobalSettings_qs.shipping_charge
            isShippingChargeFound = False
        else:
            shipping_charge = 0
            isShippingChargeFound = False

        # if company_id is not None and state_id is not None:
        #     # conditions = EngageboostShippingMastersSettings.objects.filter(website_id=website_id,country_ids__iregex=r"\y{0}\y".format(country_id),shipping_method_id='4',isblocked='n',isdeleted='n').all()
        #     GlobalSettings_qs = EngageboostGlobalSettings.objects.filter(isblocked='n',isdeleted='n').first()
        #     shipping_charge = GlobalSettings_qs.shipping_charge
        #     #print('shipping_charge',shipping_charge)
        #     isShippingChargeFound = False
        # else:
        #     shipping_charge = 0
        #     isShippingChargeFound = False

    # data={"shipping_type":"Flat Shipping","mthod_type":0,"mthod_name":"orderwise","flat_price":float(0),"handling_fees_type":0,"handling_price":float(0)}

    if isShippingChargeFound:
        if conditions:
            settings_info = ShippingMastersSettingsSerializer(conditions,many=True)
            for settingsinfo in settings_info.data:
                data={}
                if settingsinfo["mthod_type"]:
                    if settingsinfo["mthod_type"]=="1": #****ITEMWISE
                        if float(settingsinfo["flat_price"])>float(0):
                            data={"shipping_type":"Flat Shipping","shipping_setting_id":settingsinfo["id"],"mthod_type":1,"mthod_name":"itemwise","flat_price":float(settingsinfo["flat_price"])}
                        else:
                            data={"shipping_type":"Flat Shipping","mthod_type":1,"mthod_name":"itemwise","flat_price":float(0)}
                    else:
                        if float(settingsinfo["flat_price"])>float(0):
                            data={"shipping_type":"Flat Shipping","shipping_setting_id":settingsinfo["id"],"mthod_type":0,"mthod_name":"orderwise","flat_price":float(settingsinfo["flat_price"])}
                        else:
                            data={"shipping_type":"Flat Shipping","mthod_type":0,"mthod_name":"orderwise","flat_price":float(0)}
                else:
                    data={"shipping_type":"Flat Shipping","mthod_type":0,"mthod_name":"orderwise","flat_price":float(0)}

                if settingsinfo["handling_fees_type"] is not None:
                    if settingsinfo["handling_fees_type"]==0: #****FIXED PRICE
                        if float(settingsinfo["handling_price"])>float(0):
                            d1={"shipping_type":"Flat Shipping","handling_fees_type":0,"handling_price":float(settingsinfo["handling_price"])}
                        else:
                            d1={"shipping_type":"Flat Shipping","handling_fees_type":0,"handling_price":float(0)}
                    else:
                        if float(settingsinfo["handling_price"])>float(0):
                            d1={"shipping_type":"Flat Shipping","handling_fees_type":1,"handling_price":float(settingsinfo["handling_price"])}
                        else:
                            d1={"shipping_type":"Flat Shipping","handling_fees_type":1,"handling_price":float(0)}
                else:
                    d1={"shipping_type":"Flat Shipping","handling_fees_type":0,"handling_price":float(0)}

                data=dict(data,**d1)
        else:
            GlobalSettings_qs = EngageboostGlobalSettings.objects.filter(isblocked='n', isdeleted='n').first()
            shipping_charge = GlobalSettings_qs.shipping_charge
            if str_from is None:
                data = {"shipping_type": "Flat Shipping", "mthod_type": 0, "mthod_name": "orderwise","flat_price": float(shipping_charge), "handling_fees_type": 0, "handling_price": float(0)}
            else:
                data = {"shipping_type": "Flat Shipping", "mthod_type": 0, "mthod_name": "orderwise","flat_price": 0, "handling_fees_type": 0, "handling_price": float(0)}
    else:
        data={"shipping_type":"Flat Shipping","mthod_type":0,"mthod_name":"orderwise","flat_price":float(shipping_charge),"handling_fees_type":0,"handling_price":float(0)}
    #******** FOR FLAT RATE CALCULATION (END) ********#
    return data

def rate_table(website_id='1',company_id=None,cartdetails=None,country_id=None,state_id=None,post_code=None,order_from='front'):
    data={"shipping_type":"Table Rate Shipping","mthod_type":0,"mthod_name":"orderwise","flat_price":float(0),"handling_fees_type":0,"handling_price":float(0)}
    order_total=0
    order_weight=0
    for products in cartdetails:
        if products["tax_type"]=="including":
            order_total = float(order_total)+float(products["new_default_price"])+float(products["tax_price"])
        else:
            order_total = float(order_total)+float(products["new_default_price"])
        if products["weight"]:
            if type(products["weight"])== int:
                order_weight = float(order_weight)+float(products["weight"])
        
    #******** FOR TABLE RATE CALCULATION ********#
    conditionss = EngageboostShippingMastersSettings.objects.order_by("id").filter(website_id=website_id,shipping_method_id='5',isblocked='n',isdeleted='n').all()
    if conditionss:
        settings_info2 = ShippingMastersSettingsSerializer(conditionss,many=True)
        for settingsinfos in settings_info2.data:
            if country_id:
                conditions2 = EngageboostShippingTableRateOrderAmount.objects.order_by("id").filter(shipping_masters_setting_id=settingsinfos["id"],country_id__iregex=r"\y{0}\y".format(country_id)).all()
            else:
                conditions2 = EngageboostShippingTableRateOrderAmount.objects.order_by("id").filter(shipping_masters_setting_id=settingsinfos["id"]).all()

            if state_id:
                conditions2 = conditions2.order_by("id").filter(shipping_masters_setting_id=settingsinfos["id"],state_id__iregex=r"\y{0}\y".format(state_id)).all()
            else:
                conditions2 = conditions2

            if post_code:
                conditions2 = conditions2.order_by("id").filter(shipping_masters_setting_id=settingsinfos["id"],zip_code__iregex=r"\y{0}\y".format(post_code)).all()
            else:
                conditions2 = conditions2

            if conditions2:
                settings_order_amount_info = ShippingTableRateOrderAmountSerializer(conditions2,many=True)

                for settings_orderamount_info in settings_order_amount_info.data:
                    if settings_orderamount_info["order_subtotal"]:
                        if float(order_total)>=float(settings_orderamount_info["order_subtotal"]):
                            data={"shipping_type":"Table Rate Shipping","shipping_setting_id":settings_orderamount_info["id"],"mthod_type":1,"mthod_name":"orderwise","flat_price":float(settings_orderamount_info["shipping_price"])}

                    if settings_orderamount_info["weight"]:
                        if float(order_weight)>=float(settings_orderamount_info["weight"]):
                            data={"shipping_type":"Table Rate Shipping","shipping_setting_id":settings_orderamount_info["id"],"mthod_type":0,"mthod_name":"orderwise","flat_price":float(settings_orderamount_info["shipping_price"])}
             
            if settingsinfos["handling_fees_type"] is not None:
                if int(settingsinfos["handling_fees_type"])==0: #****FIXED PRICE
                    if float(settingsinfos["handling_price"])>float(0):
                        d1={"handling_fees_type":0,"handling_price":float(settingsinfos["handling_price"])}
                    else:
                        d1={"handling_fees_type":0,"handling_price":float(0)}
                else:
                    if float(settingsinfos["handling_price"])>float(0):
                        d1={"handling_fees_type":1,"handling_price":float(settingsinfos["handling_price"])}
                    else:
                        d1={"handling_fees_type":1,"handling_price":float(0)}
            else:
                d1={"handling_fees_type":0,"handling_price":float(0)}

            data=dict(data,**d1)
    #******** FOR TABLE RATE CALCULATION (END) ********#
    return data

def rate_free(website_id='1',company_id=None,country_id=None,state_id=None):
    minimum_order_amount=0
    data={"minimum_order_amount":minimum_order_amount}

    conditions = EngageboostShippingMastersSettings.objects.order_by("id").filter(website_id=website_id,shipping_method_id='6',isblocked='n',isdeleted='n').all()
    if country_id:
        conditions = conditions.order_by("id").filter(country_ids__iregex=r"\y{0}\y".format(country_id)).all()
    else:
        conditions = conditions

    if state_id:
        conditions = conditions.order_by("id").filter(state_id__iregex=r"\y{0}\y".format(state_id)).all()
    else:
        conditions = conditions

    if conditions:
        settings_info = ShippingMastersSettingsSerializer(conditions,many=True)
        for settingsinfo in settings_info.data:
            if settingsinfo["minimum_order_amount"] is not None:
                data={"shipping_setting_id":settingsinfo["id"],"minimum_order_amount":float(settingsinfo["minimum_order_amount"])}
    return data

def generate_discount_conditions_coupon(website_id,user_group_id=None,coupon_code=None, warehouse_id=None):
    # now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
    now_utc = datetime.datetime.now(timezone('UTC')).astimezone(timezone('Asia/Dubai'))
    all_discount_data=[]
    # discount_multi_coupon=EngageboostDiscountMastersCoupons.objects.filter(isdeleted='n',coupon_code=coupon_code)
    discount_multi_coupon=EngageboostDiscountMastersCoupons.objects.filter(isdeleted='n',coupon_code=coupon_code, is_used='n')
    if warehouse_id:
        discount_multi_coupon = discount_multi_coupon.filter(discount_master_id__warehouse_id__iregex=r"\y{0}\y".format(warehouse_id))
    discount_multi_coupon = discount_multi_coupon.first()   

    if discount_multi_coupon:
        discount_master_id = discount_multi_coupon.discount_master_id
        condition_discount_coupon_part = EngageboostDiscountMasters.objects.filter(id=discount_master_id).all()
    else:
        condition_discount_coupon_part=EngageboostDiscountMasters.objects.filter(coupon_code=coupon_code, used_coupon=0)
        if warehouse_id:
            condition_discount_coupon_part = condition_discount_coupon_part.filter(warehouse_id__iregex=r"\y{0}\y".format(warehouse_id))
        condition_discount_coupon_part = condition_discount_coupon_part.all()

    if condition_discount_coupon_part:
        condition_discount_coupon_part=condition_discount_coupon_part.filter(website_id=website_id,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc,isdeleted='n',isblocked='n',discount_master_type='1').all()
        if user_group_id:
            condition_discount_coupon_part=condition_discount_coupon_part.filter(customer_group__iregex=r"\y{0}\y".format(user_group_id)).all()

        if condition_discount_coupon_part:
            condition_discount_coupon_part_serialize=DiscountMasterSerializer(condition_discount_coupon_part,many=True)
            for condition_discount_coupon in condition_discount_coupon_part_serialize.data:
                discount_master_condition = EngageboostDiscountMastersConditions.objects.order_by("id").filter(discount_master_id=condition_discount_coupon["id"]).all()
                if discount_master_condition:
                    discount_master_condition_serializer = DiscountConditionsSerializer(discount_master_condition,many=True)
                    condition_discount_coupon["DiscountMasterCondition"]=discount_master_condition_serializer.data

                # discount_master_coupon = EngageboostDiscountMastersCoupons.objects.order_by("id").filter(discount_master_id=condition_discount_coupon["id"],isdeleted='n').all()
                discount_master_coupon = EngageboostDiscountMastersCoupons.objects.order_by("id").filter(discount_master_id=condition_discount_coupon["id"],isdeleted='n', coupon_code=coupon_code).first()
                # print("discount_master_coupon===========", discount_master_coupon.query)
                if discount_master_coupon:
                    # discount_master_coupon_serializer = DiscountMasterCouponSerializer(discount_master_coupon,many=True)
                    discount_master_coupon_serializer = DiscountMasterCouponSerializer(discount_master_coupon)
                    condition_discount_coupon["DiscountMasterCoupon"]=discount_master_coupon_serializer.data

            all_discount_data=condition_discount_coupon_part_serialize.data
        else:
            data={"name":"invalid","coupon_code":coupon_code,"message":"Coupon code expired or Condition not satisfied", "status":0}
            all_discount_data.append(data)
    else:
        data={"name":"invalid","coupon_code":coupon_code,"message":"Invalid Coupon Code", "status":0}
        all_discount_data.append(data)
    
    return all_discount_data

def genrate_new_prodcut_with_discount_coupon(user_id=None,cartdetails=None,discount_array_coupon=None,order_total=None):
    for discount_array in discount_array_coupon:
        for product in cartdetails:
            # product = getproductforcart(product_detail["id"])
            return_price = check_in_prod_disc_coupon(user_id,product,discount_array,order_total)
            price_array = return_price.split('^')
            if price_array[2] != "false":
                product["new_default_price_unit"] = float(price_array[0])
                product["new_default_price"] = float(price_array[0])*float(product["qty"])
                product["discount_price_unit"] = float(product["discount_price_unit"])+float(price_array[1])
                product["discount_price"] = float(product["discount_price"])+float(price_array[1])*float(product["qty"])
                product["coupon_discount_amount"] = float(discount_array["amount"])
                product["product_coupon_discount_price"] = float(price_array[1])*float(product["qty"])
                product["coupon_disc_type"] = discount_array["disc_type"]
                product["coupon_name"] = discount_array["name"]
                product["coupon_code"] = discount_array["coupon_code"]
            else:
                product["coupon_discount_amount"] = float(0)
                product["coupon_disc_type"] = ""
                product["coupon_name"] = ""
                product["coupon_code"] = ""
                product["product_coupon_discount_price"] = 0

    return cartdetails

def check_in_prod_disc_coupon(user_id=None,ind_product=None,discount_array=None,cart_subtotal=None):
    discount_array_condition = discount_array["DiscountMasterCondition"]
    product_array_disc_applied = []
    i=0
    flag = "false"
    for ind_cond in discount_array_condition:
        if ind_cond["fields"]==-1:
            if cart_subtotal:
                if ind_cond["condition"] == "==":
                    flag = "true" if float(cart_subtotal) == float(ind_cond["value"]) else "false"
                elif ind_cond["condition"] == ">=":
                    flag = "true" if float(cart_subtotal) >= float(ind_cond["value"]) else "false"
                else:
                    flag = "false" if float(cart_subtotal) >= float(ind_cond["value"]) else "true"
            else:
                flag = "false"
        elif ind_cond["all_category_id"]:
            category_id_array = ind_cond["all_category_id"].split(",")
            find_category = EngageboostProductCategories.objects.filter(product_id=ind_product["id"]).all()
            
            sub_category_id_array = []
            
            if find_category:
                ptcArr = ProductCategoriesSerializer(find_category,many=True)
                for pro in ptcArr.data:
                    # sub_category_id_array.append(pro["category"]["id"])
                    sub_category_id_array.append(pro["category_id"])
            if sub_category_id_array:
                for index in range(len(sub_category_id_array)):
                    if ind_cond["condition"] == "==":
                        if str(sub_category_id_array[index]) in category_id_array:
                            flag = "true"
                            break
                        else:
                            flag = "false"
                    else:
                        if str(sub_category_id_array[index]) in category_id_array:
                            flag = "false"
                            break
                        else:
                            flag = "true"
            else:
                if ind_cond["condition"] == "==": 
                    if ind_product["category_id"] in category_id_array:
                        flag = "true"
                    else:
                        flag = "false"
                else:
                    if ind_product["category_id"] in category_id_array:
                        flag = "false"
                    else:
                        flag = "true"
        elif ind_cond["all_product_id"]:
            product_id_array = ind_cond["all_product_id"].split(",")
            if ind_cond["condition"] == "==":
                if str(ind_product["id"]) in product_id_array:
                    flag = "true"
                else:
                    flag = "false"
            else:
                if ind_product["id"] in product_id_array:
                    flag = "false"
                else:
                    flag = "true"
        elif ind_cond["all_customer_id"]:
            customer_id_array = ind_cond["all_customer_id"].split(",")
            if user_id:
                if ind_cond["condition"] == "==":
                    if user_id in customer_id_array:
                        flag = "true"
                    else:
                        flag = "false"
                else:
                    if user_id in customer_id_array:
                        flag = "false"
                    else:
                        flag = "true"
            else:
                flag = "false"

        if i!=0:
            if previos_condition=="AND":
                if flag=="true" and previos_flag=="true":
                    previos_flag="true"
                else:
                    previos_flag="false"

            if previos_condition=="OR":
                if flag=="false" and previos_flag=="false":
                    previos_flag="false"
                else:
                    previos_flag="true"
        else:
            previos_flag = flag

        previos_condition=ind_cond["condition_type"]
        i=i+1

    if previos_flag == "true":
        if discount_array["disc_type"]==1:
            discount_array["discountPrice"]=float(ind_product["new_default_price_unit"])*float(discount_array["amount"])/float(100)
        else:
            discount_array["discountPrice"]=float(discount_array["amount"])

        if ind_product["new_default_price_unit"]:
            if float(ind_product["new_default_price_unit"])<=float(0):
                if float(ind_product["new_default_price_unit"])>float(discount_array["discountPrice"]):
                    default_price=float(ind_product["new_default_price_unit"])-float(discount_array["discountPrice"])
                    discount_price=float(ind_product["discount_price_unit"])+float(discount_array["discountPrice"])
                else:
                    default_price=float(ind_product["new_default_price_unit"])
                    discount_price=float(ind_product["discount_price_unit"])

                product_array_disc_applied.append(ind_product["id"])
            else:
                if float(ind_product["default_price"])>float(discount_array["discountPrice"]):
                    default_price = float(ind_product["new_default_price_unit"])-float(discount_array["discountPrice"])
                    discount_price = float(discount_array["discountPrice"])
                else:
                    default_price = float(ind_product["new_default_price_unit"])
                    discount_price = float(ind_product["discount_price_unit"])
                product_array_disc_applied.append(ind_product["id"])
        else:
            if float(ind_product["default_price"])>float(discount_array["discountPrice"]):
                default_price=float(ind_product["default_price"])-float(discount_array["discountPrice"])
                discount_price=float(discount_array["discountPrice"])
                product_array_disc_applied.append(ind_product["id"])
            else:
                default_price  = float(0)
                discount_price = float(0)
    else:
        if ind_product["new_default_price_unit"]:
            default_price = float(ind_product["new_default_price_unit"])
            discount_price = float(ind_product["discount_price_unit"])
        else:
            default_price  = float(0)
            discount_price = float(0)

    return str(default_price)+"^"+str(discount_price)+"^"+str(previos_flag)

def genrate_new_prodcut_with_discount_coupon_order_total(user_id=None,cartdetails=None,discount_array_coupon=None,order_total=None):
    set_of_response=[]
    coupon_details_dict={}
    for discount_array in discount_array_coupon:
        coupon_details={"coupon_discount_amount":float(discount_array["amount"]),"coupon_disc_type":discount_array["disc_type"],"coupon_name":discount_array["name"],"coupon_code":discount_array["coupon_code"]}
        for product in cartdetails:
            return_price = check_in_prod_disc_coupon_order_total(user_id,product,discount_array,order_total)
            price_array = return_price
            set_of_response.append(price_array)

    check_string="false"
    if check_string in set_of_response:
        coupon_details_dict = {"coupon_discount_amount": float(0),
                               "coupon_disc_type": coupon_details["coupon_disc_type"],
                               "coupon_name": coupon_details["coupon_name"],
                               "coupon_code": coupon_details["coupon_code"], "status": "false"}
        return coupon_details_dict
    else:
        coupon_details['status'] = "true"
        return coupon_details

def check_in_prod_disc_coupon_order_total(user_id=None,ind_product=None,discount_array=None,cart_subtotal=None):
    discount_array_condition = discount_array["DiscountMasterCondition"]
    product_array_disc_applied = []
    i=0
    flag = "false"
    for ind_cond in discount_array_condition:
        if ind_cond["fields"]==-1:
            if cart_subtotal:
                if ind_cond["condition"] == "==":
                    flag = "true" if float(cart_subtotal) == float(ind_cond["value"]) else "false"
                elif ind_cond["condition"] == ">=":
                    flag = "true" if float(cart_subtotal) >= float(ind_cond["value"]) else "false"
                else:
                    flag = "false" if float(cart_subtotal) >= float(ind_cond["value"]) else "true"
            else:
                flag = "false"
        elif ind_cond["all_category_id"]:
            category_id_array = ind_cond["all_category_id"].split(",")
            find_category = EngageboostProductCategories.objects.filter(product_id=ind_product["id"]).all()
            
            sub_category_id_array = []
            
            if find_category:
                ptcArr = ProductCategoriesSerializer(find_category,many=True)
                for pro in ptcArr.data:
                    sub_category_id_array.append(pro["category_id"])

            if sub_category_id_array:
                for index in range(len(sub_category_id_array)):
                    if ind_cond["condition"] == "==":
                        if str(sub_category_id_array[index]) in category_id_array:
                            flag = "true"
                            break
                        else:
                            flag = "false"
                    else:
                        if str(sub_category_id_array[index]) in category_id_array:
                            flag = "false"
                            break
                        else:
                            flag = "true"
            else:
                if ind_cond["condition"] == "==": 
                    if ind_product["category_id"] in category_id_array:
                        flag = "true"
                    else:
                        flag = "false"
                else:
                    if ind_product["category_id"] in category_id_array:
                        flag = "false"
                    else:
                        flag = "true"
        elif ind_cond["all_product_id"]:
            product_id_array = ind_cond["all_product_id"].split(",")
            if ind_cond["condition"] == "==":
                if str(ind_product["id"]) in product_id_array:
                    flag = "true"
                else:
                    flag = "false"
            else:
                if ind_product["id"] in product_id_array:
                    flag = "false"
                else:
                    flag = "true"
        elif ind_cond["all_customer_id"]:
            customer_id_array = ind_cond["all_customer_id"].split(",")
            if user_id:
                if ind_cond["condition"] == "==":
                    if user_id in customer_id_array:
                        flag = "true"
                    else:
                        flag = "false"
                else:
                    if user_id in customer_id_array:
                        flag = "false"
                    else:
                        flag = "true"
            else:
                flag = "false"

        if i!=0:
            if previos_condition=="AND":
                if flag=="true" and previos_flag=="true":
                    previos_flag="true"
                else:
                    previos_flag="false"

            if previos_condition=="OR":
                if flag=="false" and previos_flag=="false":
                    previos_flag="false"
                else:
                    previos_flag="true"
        else:
            previos_flag = flag

        previos_condition=ind_cond["condition_type"]
        i=i+1

    return str(previos_flag)


def GetProductDiscount(self, request, format=None):
    company_id = request.data["company_id"]
    website_id = request.data["website_id"]
    webshop_id = request.data["webshop_id"] if request.data.get("webshop_id") else 6
    product_ids= request.data["product_ids"]
    qtys       = request.data["qtys"]
    prod_price = request.data["prod_price"]
    country_id = request.data["country_id"] if request.data.get("country_id") else ""
    state_id = request.data["state_id"] if request.data.get("state_id") else ""
    post_code = request.data["post_code"] if request.data.get("post_code") else ""
    payment_method_id = request.data["payment_method_id"] if request.data.get("payment_method_id") else None
    user_id = request.data["user_id"] if request.data.get("user_id") else None
    user_group_id = request.data["user_group_id"] if request.data.get("user_group_id") else None
    coupon_code = request.data["coupon_code"] if request.data.get("coupon_code") else None
    paid_amount = float(request.data["paid_amount"]) if request.data.get("paid_amount") else float(0)

    cartdetails=[];checkout_info=[];new_unit_netamount=[];new_total_netamount=[]

    shipper_address=EngageboostCompanyWebsites.objects.filter(id=website_id).first()
    cod_min_amount=cod_max_amount=None
    cod_charge=0

    if int(payment_method_id)==15 or int(payment_method_id)==16:
        payment_method_onepage=payment_method_onepage_checkout(website_id)
    else:
        payment_method_onepage=payment_method_onepage_checkout(website_id)

    # return Response(payment_method_onepage)
    for value in payment_method_onepage:
        if value['payment_type_id']==4:
            # flag=False
            if value["setting_key"]=="min_amount":
                cod_min_amount=float(value["setting_val"])
            if value["setting_key"]=="max_amount":
                cod_max_amount=float(value["setting_val"])
            if value["setting_key"]=="cod_charge":
                cod_charge=float(value["setting_val"])

    product_ids=product_ids.split(",")
    quantity=qtys.split(",")
    prod_price=prod_price.split(",")
    for index in range(len(product_ids)):
        product_id = product_ids[index]
        # checkout_info_dict = {"product_id":product_ids[index],"quantity":quantity[index],"product_price":prod_price[index]}
        # checkout_info.append(checkout_info_dict)
        new_unit_netamount.append(float(prod_price[index])/float(quantity[index]))
        new_total_netamount.append(float(prod_price[index])*float(quantity[index]))
        discount_array_net = generate_discount_conditions(website_id,user_group_id)
        getproductforcart_net = getproductforcart(product_id)
        for getproductforcartnet in getproductforcart_net:
            getproductforcartnet["qty"]=quantity[index]
            try:
                if getproductforcartnet["new_default_price"]: getproductforcartnet["new_default_price"] = getproductforcartnet["new_default_price"]
                else: getproductforcartnet["new_default_price"] = getproductforcartnet["default_price"]
            except KeyError: getproductforcartnet["new_default_price"] = getproductforcartnet["default_price"]

        #********Apply Discount and Get New Product Amount********#
        product_detail_net = genrate_new_prodcut_with_discount(user_id,getproductforcart_net,discount_array_net)
        product_detail_net = product_detail_net[0]

        #********Tax Calculation********#
        # if country_id!="" or state_id!="" or post_code!="":
        tax_price_arr = get_price_including_tax(website_id,company_id,product_detail_net,country_id,state_id,post_code,'back')

        company_info = EngageboostCompanyWebsites.objects.filter(id=website_id).first()
        if company_info:
            company_state=company_info.state
        else:
            company_state=0

        if str(company_state)!=str(state_id):
            product_tax={"tax_price_unit":float(tax_price_arr["tax_igst"]),"tax_price":float(tax_price_arr["tax_igst"])*float(product_detail_net["qty"]),"tax_percentage":tax_price_arr["igst"],"tax_name":tax_price_arr["tax_name"],"cgst":tax_price_arr["cgst"],"sgst":tax_price_arr["sgst"],"igst":tax_price_arr["igst"],"cess":tax_price_arr["cess"],"is_igst":"yes","tax_type":tax_price_arr["tax_type"]}
        else:
            product_tax={"tax_price_unit":float(tax_price_arr["tax_igst"]),"tax_price":float(tax_price_arr["tax_igst"])*float(product_detail_net["qty"]),"tax_percentage":tax_price_arr["igst"],"tax_name":tax_price_arr["tax_name"],"cgst":tax_price_arr["cgst"],"sgst":tax_price_arr["sgst"],"igst":tax_price_arr["igst"],"cess":tax_price_arr["cess"],"is_igst":"no","tax_type":tax_price_arr["tax_type"]}
        
        product_detail_net=dict(product_detail_net,**product_tax)

        if product_detail_net["tax_type"]=="including":
            product_detail_net["new_default_price_unit"]=float(product_detail_net["new_default_price_unit"])-float(product_detail_net["tax_price_unit"])
            product_detail_net["new_default_price"]=float(product_detail_net["new_default_price"])-float(product_detail_net["tax_price"])
        #********Tax Calculation (END)********#

        cartdetails.append(product_detail_net)

    order_total=0
    order_weight=0
    if cartdetails:
        for products in cartdetails:
            if products["tax_type"]=="including":
                order_total = float(order_total)+float(products["new_default_price"])+float(products["tax_price"])
            else:
                order_total = float(order_total)+float(products["new_default_price"])
            if products["weight"]:
                order_weight = float(order_weight)+float(products["weight"])

    #********Shipping Calculation********#
    shipping_amount_arr={"shipping_amount":0,"mthod_type":0,"mthod_name":"orderwise","handling_fees_type":0,"handling_price":0}
    if cartdetails:
        shipping_flat = rate_flat(website_id,company_id,country_id,state_id,post_code,'back')
        shipping_table = rate_table(website_id,company_id,cartdetails,country_id,state_id,post_code,'back')
        shipping_free = rate_free(website_id,company_id,country_id,state_id)

        if shipping_flat:
            if float(shipping_flat["flat_price"])>float(0) and float(order_total)<float(shipping_free["minimum_order_amount"]):
                shipping_amount_arr={"shipping_amount":float(shipping_flat["flat_price"]),"mthod_type":shipping_flat["mthod_type"],"mthod_name":shipping_flat["mthod_name"],"handling_fees_type":shipping_flat["handling_fees_type"],"handling_price":shipping_flat["handling_price"]}

        if shipping_table:
            if float(shipping_table["flat_price"])>float(0) and float(order_total)<float(shipping_free["minimum_order_amount"]):
                shipping_amount_arr={"shipping_amount":float(shipping_table["flat_price"]),"mthod_type":shipping_table["mthod_type"],"mthod_name":shipping_table["mthod_name"],"handling_fees_type":shipping_table["handling_fees_type"],"handling_price":shipping_table["handling_price"]}
    #********Shipping Calculation (END)********#

    #********APPLY COUPON CODE********#
    if cartdetails and coupon_code is not None:
        discount_array_coupon=generate_discount_conditions_coupon(website_id,user_group_id,coupon_code)

        if discount_array_coupon and discount_array_coupon[0]["name"]!="invalid":
            if discount_array_coupon[0]["disc_type"]!=3:
                if discount_array_coupon[0]["coupon_type"]==2:
                    cartdetails=genrate_new_prodcut_with_discount_coupon(user_id,cartdetails,discount_array_coupon,order_total)
                else:
                    if discount_array_coupon[0]["used_coupon"]==0:
                        cartdetails=genrate_new_prodcut_with_discount_coupon(user_id,cartdetails,discount_array_coupon,order_total)
            else:
                if discount_array_coupon[0]["coupon_type"]==2:
                    coupon_details=genrate_new_prodcut_with_discount_coupon_order_total(user_id,cartdetails,discount_array_coupon,order_total)
                else:
                    if discount_array_coupon[0]["used_coupon"]==0:
                        coupon_details=genrate_new_prodcut_with_discount_coupon_order_total(user_id,cartdetails,discount_array_coupon,order_total)
    #********APPLY COUPON CODE (END)********#
    orderamountdetails=[]
    applied_coupon=[]
    order_total=0
    order_weight=0
    total_tax=0
    shipping_amount=0
    handling_charge=0
    order_total_with_handling_price=0
    gross_discount_amount = 0
    grandtotal=subtotal=nettotal=cart_discount=0
    if cartdetails:
        for products in cartdetails:
            order_total = float(order_total)+float(products["new_default_price"])+float(products["tax_price"])
            total_tax = float(total_tax)+float(products["tax_price"])
            #********PRODUCT TOTAL DISCOUNT (EXCLUDING WHOLE CART DISCOUNT)********#
            gross_discount_amount = float(gross_discount_amount)+float(products["discount_price"])

            if shipping_amount_arr["mthod_type"]!=0:
                shipping_price=float(shipping_amount_arr["shipping_amount"])*float(products["qty"])
                shipping_amount=float(shipping_amount)+float(shipping_price)
            else:
                shipping_amount=float(shipping_amount_arr["shipping_amount"])

        if shipping_amount_arr["handling_fees_type"]==0:
            handling_charge = shipping_amount_arr["handling_price"]
            order_total_with_handling_price = float(order_total)+float(handling_charge)
        else:
            handling_charge = float(order_total)*float(shipping_amount_arr["handling_price"])/float(100)
            order_total_with_handling_price = float(order_total)+float(handling_charge)

        #********TOTAL AMOUNT PRODUCT PRICE + SHIPPING CHARGE + HANDLING CHARGE ********#
        grandtotal = float(order_total_with_handling_price)+float(shipping_amount)

        #********APPLY COD CHAGE********#
        if cod_min_amount is not None and cod_max_amount is not None:
            if float(cod_min_amount)<=float(grandtotal) and float(grandtotal)<=float(cod_max_amount):
                grandtotal = float(grandtotal)+float(cod_charge)
                applied_cod_charge = float(cod_charge)
            else:
                grandtotal = grandtotal
                applied_cod_charge = float(0)
        else:
            grandtotal = grandtotal
            applied_cod_charge = float(0)

        #********APPLY COUPON DISCOUNT ON WHOLE CART********#
        if coupon_code is not None:
            if discount_array_coupon and discount_array_coupon[0]["name"]!="invalid":
                if discount_array_coupon[0]["disc_type"]==3:
                    grandtotal = float(grandtotal)
                    subtotal = float(grandtotal)-float(coupon_details["coupon_discount_amount"])
                    cart_discount = float(grandtotal)-float(subtotal)
                else:
                    grandtotal = float(grandtotal)
                    subtotal = float(grandtotal)
                    cart_discount = float(grandtotal)-float(subtotal)

                applied_coupon_dict={"name":discount_array_coupon[0]["name"],"coupon_code":discount_array_coupon[0]["coupon_code"],"disc_type":discount_array_coupon[0]["disc_type"],"amount":discount_array_coupon[0]["amount"], "status":1}
                applied_coupon.append(applied_coupon_dict)
            else:
                grandtotal = float(grandtotal)
                subtotal = float(grandtotal)
                cart_discount = float(grandtotal)-float(subtotal)
                applied_coupon_dict={"name":discount_array_coupon[0]["name"],"coupon_code":discount_array_coupon[0]["coupon_code"],"message":discount_array_coupon[0]["message"], "status":0}
                applied_coupon.append(applied_coupon_dict)
        else:
            grandtotal = float(grandtotal)
            subtotal = float(grandtotal)
            cart_discount = float(grandtotal)-float(subtotal)
        #********APPLY COUPON DISCOUNT ON WHOLE CART(END)********#

    nettotal = float(subtotal)-float(total_tax)-float(shipping_amount)-float(handling_charge)-float(applied_cod_charge)
    balance_due = float(subtotal)-float(paid_amount)
    orderamountdetails_dict={"company_id":company_id,"website_id":website_id,"webshop_id":webshop_id,"payment_method_id":payment_method_id,"tax_amount":total_tax,"shipping_charge":shipping_amount,"handling_charge":handling_charge,"cod_charge":applied_cod_charge,"gross_discount":gross_discount_amount,"min_amount":cod_min_amount,"max_amount":cod_max_amount,"grand_total":grandtotal,"sub_total":subtotal,"net_total":nettotal,"cart_discount":cart_discount,"paid_amount":paid_amount,"balance_due":balance_due}
    orderamountdetails.append(orderamountdetails_dict)

    data={"cartdetails":cartdetails,"orderamountdetails":orderamountdetails,"applied_coupon":applied_coupon,"shipping_flat":shipping_flat,"shipping_table":shipping_table}

    return Response(data)

def payment_method_onepage_checkout_old(website_id):
    # EngageboostCompanyWebsites.objects.filter(id=website_id).all()
    website_methods=[]
    payment_setting_info_list=[]
    website_data_cond = EngageboostWebsitePaymentmethods.objects.filter(engageboost_company_website_id=website_id).all()
    website_data=WebsitePaymentmethodsSerializer(website_data_cond,many=True)
    for websitedata in website_data.data:
        website_methods.append(websitedata["engageboost_paymentgateway_method_id"])

    
    payment_setting_info_cond=EngageboostPaymentgatewaySettingInformation.objects.filter(website_id=website_id,isblocked='n',isdeleted='n').all()
    payment_setting_info=PaymentgatewaySettingInformationSerializer(payment_setting_info_cond,many=True)

    for payment_settinginfo in payment_setting_info.data:
        payment_setting_type=EngageboostPaymentgatewayTypes.objects.filter(id=payment_settinginfo["paymentgateway_type_id"]).first()
        payment_setting_method=EngageboostPaymentgatewayMethods.objects.filter(id=payment_settinginfo["paymentgateway_method_id"]).first()

        if payment_setting_type:
            payment_settinginfo["payment_type_name"]=payment_setting_type.name
            payment_settinginfo["payment_type_image"]=payment_setting_type.image
            payment_settinginfo["payment_type_id"]=payment_setting_type.id

        if payment_setting_method:
            payment_settinginfo["name"]=payment_setting_method.name
            payment_settinginfo["destination_url"]=payment_setting_method.destination_url
            payment_settinginfo["payment_method_id"]=payment_setting_method.id

    return payment_setting_info.data

def payment_method_onepage_checkout(website_id):
    # EngageboostCompanyWebsites.objects.filter(id=website_id).all()
    website_methods=[]
    payment_setting_info_list=[]
    website_data_cond = EngageboostWebsitePaymentmethods.objects.filter(engageboost_company_website_id=website_id, engageboost_paymentgateway_method_id = 16).last()
    website_data=WebsitePaymentmethodsSerializer(website_data_cond)
    website_data = website_data.data
    # for websitedata in website_data.data:
    website_methods.append(website_data["engageboost_paymentgateway_method_id"])
    
    payment_setting_info_cond=EngageboostPaymentgatewaySettingInformation.objects.filter(website_id=website_id,isblocked='n',isdeleted='n', paymentgateway_method_id = 16).all()
    payment_setting_info=PaymentgatewaySettingInformationSerializer(payment_setting_info_cond,many=True)

    for payment_settinginfo in payment_setting_info.data:
        payment_setting_type=EngageboostPaymentgatewayTypes.objects.filter(id=payment_settinginfo["paymentgateway_type_id"]).first()
        payment_setting_method=EngageboostPaymentgatewayMethods.objects.filter(id=payment_settinginfo["paymentgateway_method_id"]).first()

        if payment_setting_type:
            payment_settinginfo["payment_type_name"]=payment_setting_type.name
            payment_settinginfo["payment_type_image"]=payment_setting_type.image
            payment_settinginfo["payment_type_id"]=payment_setting_type.id

        if payment_setting_method:
            payment_settinginfo["name"]=payment_setting_method.name
            payment_settinginfo["destination_url"]=payment_setting_method.destination_url
            payment_settinginfo["payment_method_id"]=payment_setting_method.id

    return payment_setting_info.data

def getcurrencycode(webID):
    currency_code = ""
    if webID>0:
        cur_code = ""
        if cur_code:
            pass
        else:
            rs_currency = EngageboostCurrencyRates.objects.filter(isbasecurrency='y', engageboost_company_website_id=webID).first()
            currency_data = CurrencyRatesSerializer(rs_currency)
            currency_data = currency_data.data
            currency_code = currency_data['currency_code'] if currency_data['currency_code'] else ""
    return currency_code

def product_offer_discount_price(website_id, listing_products,user_id=None):
    #  listing_products should be listing Array
    currency_code = getcurrencycode(website_id)
    if listing_products:
        list_arr = []
        list_arr.insert[listing_products]
        discount_array = generate_discount_conditions(website_id,None);
        if discount_array:
            listing_products = genrate_new_prodcut_with_discount(None,list_arr, discount_array)

        for prod_details in listing_products:
            if prod_details['new_default_price'] and prod_details['new_default_price']>0 and prod_details['disc_type']:
                zero_replace_blank_offer_price="";
                zero_replace_blank_offer_price = str(prod_details['discount_amount']).replace('.00','') 
                product_price_content = ""
                if prod_details['disc_type']==1:
                    product_price_content = zero_replace_blank_offer_price +"% OFF"
                    prod_details['discount_price'] = zero_replace_blank_offer_price+"%"
                if prod_details['disc_type']==2:
                    zero_replace_blank_offer_price = prod_details['discount_amount']
                    product_price_content = "Rs. "+zero_replace_blank_offer_price+" OFF"
                    listing_products['discount_price'] = zero_replace_blank_offer_price
            else:
                product_price_content = ""

            prod_details['offer_price'] = int(10)        #str(product_price_content)

            zero_replace_blank_default_price = str(prod_details['default_price']).replace('.00','')
            prod_details['original_price'] = zero_replace_blank_default_price
            if prod_details['new_default_price'] and prod_details['new_default_price']>0:
                zero_replace_blank_new_default_price = prod_details['new_default_price']
                price = str(zero_replace_blank_default_price) + str(zero_replace_blank_new_default_price)
                prod_details['effective_price'] = zero_replace_blank_new_default_price
            else:
                price = zero_replace_blank_default_price
                prod_details['effective_price'] = zero_replace_blank_default_price

            prod_details['final_price'] = price
#             //stock related quantity ....
#             if(!empty($prod_details['StockData']['id'])) {
#                 $listing_products[$key]['Product']['quantity'] = $prod_details['StockData']['real_stock'];
#             }

    return listing_products


class TestClass(APIView):
    def get(self, request, format=None):    
        # discount_array = generate_discount_conditions(1, None);
        # disc_pro = product_offer_discount_price(1, None)
        disc_pro = GetCartDetails(1,1,1, None, None )
        print("KC1")
        print(json.dumps(disc_pro.data, indent=4, sort_keys=True))
        print("KC2")
        
        data = {
            "status":1,
            "data":disc_pro.data
        }
        return Response(data)


# product_offer_discount_price
# genrate_new_prodcut_with_discount
# print(json.dumps(jsn, indent=4, sort_keys=True))


def GetCartDetails(company_id, website_id, customer_id=None, device_id=None, webshop_id=None, country_id = None, state_id = None, post_code = None, user_id = None, user_group_id = None, coupon_code = None, warehouse_id=None, str_from=None):
    # company_db = loginview.db_active_connection(request)
    company_id = company_id
    website_id = website_id
    webshop_id = webshop_id if webshop_id else 6
    warehouse_id = warehouse_id
    cart_count = 0
    rs_cart = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id)
    if customer_id:
        has_customer = EngageboostCustomers.objects.filter(id=customer_id).first()
        if has_customer:
            user_id = has_customer.auth_user_id
        rs_cart = rs_cart.filter(customer_id=user_id)
    elif device_id:
        rs_cart = rs_cart.filter(device_id=device_id, customer_id__isnull=True)
    # elif device_id:
    #     rs_cart = rs_cart.filter(customer_id=0, device_id=device_id)

    cart_data = EngageboostTemporaryShoppingCartsSerializer(rs_cart, context={'warehouse_id': warehouse_id}, many=True)
    # print("**************** Cart data 123**************")
    country_id      = country_id
    state_id        = state_id
    post_code       = post_code
    user_id         = user_id
    user_group_id   = user_group_id
    coupon_code     = coupon_code
    shipping_flat   = []
    shipping_table  = []
    shipping_free   = []
    lst_product_cat = []
    payment_method_id   = 16
    paid_amount         = 0
    cartdetails = []; checkout_info = []; new_unit_netamount = []; new_total_netamount = []

    shipper_address = EngageboostCompanyWebsites.objects.filter(id=website_id).first()
    cod_min_amount  = cod_max_amount=None
    cod_charge      = 0
    if payment_method_id:
        if int(payment_method_id)==15 or int(payment_method_id)==16:
            payment_method_onepage=payment_method_onepage_checkout(website_id)
        else:
            payment_method_onepage=payment_method_onepage_checkout(website_id)
    else:
        payment_method_onepage=payment_method_onepage_checkout(website_id)

    # return Response(payment_method_onepage)
    for value in payment_method_onepage:
        if value['payment_type_id']==4:
            # flag=False
            if value["setting_key"]=="min_amount":
                cod_min_amount=float(value["setting_val"])
            if value["setting_key"]=="max_amount":
                cod_max_amount=float(value["setting_val"])
            if value["setting_key"]=="cod_charge":
                cod_charge=float(value["setting_val"])
    
    check_stock = 1
    check_stock_msg = ""

    for cartdata in cart_data.data:
        if "id" in cartdata['product_id']:
            product_id = cartdata['product_id']['id']
            if cartdata['product_id']['default_price'] and cartdata['quantity']:
                new_unit_netamount.append(float(cartdata['product_id']['default_price'])/float(cartdata['quantity']))
                new_total_netamount.append(float(cartdata['product_id']['default_price'])/float(cartdata['quantity']))
            else:
                new_unit_netamount.append(0.00)
                new_total_netamount.append(0.00)

            if float(cartdata['product_id']['stock']['stock_value'])>0:
                pass
            else:
                check_stock = 0
                check_stock_msg = "stock check fail."  
        else:
            EngageboostTemporaryShoppingCarts.objects.filter(id=cartdata['id']).delete()

        discount_array_net = generate_discount_conditions(website_id, user_group_id, None, warehouse_id)
        getproductforcart_net = getproductforcart(product_id, warehouse_id)
        # for getproductforcartnet in getproductforcart_net:
        #     getproductforcartnet["qty"]=int(cartdata['quantity'])
        #     try:
        #         if getproductforcartnet["new_default_price"]: getproductforcartnet["new_default_price"] = getproductforcartnet["new_default_price"]
        #         else: getproductforcartnet["new_default_price"] = getproductforcartnet["default_price"]
        #     except KeyError: getproductforcartnet["new_default_price"] = getproductforcartnet["default_price"]

        if getproductforcart_net:
            getproductforcart_net["qty"]=int(cartdata['quantity'])

            getproductforcart_net["custom_field_name"] = cartdata['custom_field_name']
            getproductforcart_net["custom_field_value"] = cartdata['custom_field_value']

            cart_count = cart_count + int(cartdata['quantity'])
            try:
                if getproductforcart_net["new_default_price"]: 
                    getproductforcart_net["new_default_price"] = float(getproductforcart_net["channel_price"])*int(cartdata['quantity'])
                    getproductforcart_net["new_default_price_unit"] = float(getproductforcart_net["channel_price"]) if getproductforcart_net["channel_price"] else 0.0
                    getproductforcart_net["discount_price_unit"] = 0.00   
                    getproductforcart_net["discount_price"] = 0.00
                    getproductforcart_net["discount_amount"] = 0.00
                    getproductforcart_net["disc_type"] =""
                    getproductforcart_net["coupon"] = ""

                else: 
                    getproductforcart_net["new_default_price"] = float(getproductforcart_net["channel_price"])*int(cartdata['quantity'])
                    getproductforcart_net["new_default_price_unit"] = float(getproductforcart_net["channel_price"]) if getproductforcart_net["channel_price"] else 0.0
                    getproductforcart_net["discount_price_unit"] = 0.00   
                    getproductforcart_net["discount_price"] = 0.00
                    getproductforcart_net["discount_amount"] = 0.00
                    getproductforcart_net["disc_type"] =""
                    getproductforcart_net["coupon"] = ""

            except KeyError: 
                getproductforcart_net["new_default_price"] = float(getproductforcart_net["default_price"])*int(cartdata['quantity'])
                getproductforcart_net["new_default_price_unit"] = float(getproductforcart_net["channel_price"]) if getproductforcart_net["channel_price"] else 0.0
                getproductforcart_net["discount_price_unit"] = 0.00   
                getproductforcart_net["discount_price"] = 0.00
                getproductforcart_net["discount_amount"] = 0.00
                getproductforcart_net["disc_type"] =""
                getproductforcart_net["coupon"] = ""

        #********Apply Discount and Get New Product Amount********#        
        product_detail_net = genrate_new_prodcut_with_discount(user_id,getproductforcart_net,discount_array_net)
        product_detail_net = product_detail_net

        #********Tax Calculation********#
        # if country_id!="" or state_id!="" or post_code!="":
        tax_price_arr = get_price_including_tax(website_id,company_id,product_detail_net,country_id,state_id,post_code,'back')

        company_info = EngageboostCompanyWebsites.objects.filter(id=website_id).first()
        if company_info:
            company_state=company_info.state
        else:
            company_state=0

        if str(company_state)!=str(state_id):
            product_tax={"tax_price_unit":float(tax_price_arr["tax_igst"]),"tax_price":float(tax_price_arr["tax_igst"])*float(product_detail_net["qty"]),"tax_percentage":tax_price_arr["igst"],"tax_name":tax_price_arr["tax_name"],"cgst":tax_price_arr["cgst"],"sgst":tax_price_arr["sgst"],"igst":tax_price_arr["igst"],"cess":tax_price_arr["cess"],"is_igst":"yes","tax_type":tax_price_arr["tax_type"]}
        else:
            product_tax={"tax_price_unit":float(tax_price_arr["tax_igst"]),"tax_price":float(tax_price_arr["tax_igst"])*float(product_detail_net["qty"]),"tax_percentage":tax_price_arr["igst"],"tax_name":tax_price_arr["tax_name"],"cgst":tax_price_arr["cgst"],"sgst":tax_price_arr["sgst"],"igst":tax_price_arr["igst"],"cess":tax_price_arr["cess"],"is_igst":"no","tax_type":tax_price_arr["tax_type"]}
        
        product_detail_net=dict(product_detail_net,**product_tax)

        if product_detail_net["tax_type"]=="including":
            product_detail_net["new_default_price_unit"]=float(product_detail_net["new_default_price_unit"])-float(product_detail_net["tax_price_unit"])
            product_detail_net["new_default_price"]=float(product_detail_net["new_default_price"])-float(product_detail_net["tax_price"])
        #********Tax Calculation (END)********#
        cartdetails.append(product_detail_net)

    order_total=0
    order_weight=0
    if cartdetails:
        for products in cartdetails:
            lst_product_cat.append(products['category_id'])
            if products["tax_type"]=="including":
                order_total = float(order_total)+float(products["new_default_price"])+float(products["tax_price"])
            else:
                order_total = float(order_total)+float(products["new_default_price"])
            if products["weight"]:
                if type(products["weight"])== int:
                    order_weight = float(order_weight)+float(products["weight"])

    #********Shipping Calculation********#
    shipping_amount_arr={"shipping_amount":0,"mthod_type":0,"mthod_name":"orderwise","handling_fees_type":0,"handling_price":0}
    if cartdetails:
        shipping_flat = rate_flat(website_id,company_id,country_id,state_id,post_code,'back',warehouse_id,str_from)
        shipping_table = rate_table(website_id,company_id,cartdetails,country_id,state_id,post_code,'back')
        shipping_free = rate_free(website_id,company_id,country_id,state_id)


        if shipping_flat:
            if float(shipping_flat["flat_price"])>float(0) and float(order_total)<float(shipping_free["minimum_order_amount"]):
                shipping_amount_arr={"shipping_amount":float(shipping_flat["flat_price"]),"mthod_type":shipping_flat["mthod_type"],"mthod_name":shipping_flat["mthod_name"],"handling_fees_type":shipping_flat["handling_fees_type"],"handling_price":shipping_flat["handling_price"]}

        if shipping_table:
            if float(shipping_table["flat_price"])>float(0) and float(order_total)<float(shipping_free["minimum_order_amount"]):
                shipping_amount_arr={"shipping_amount":float(shipping_table["flat_price"]),"mthod_type":shipping_table["mthod_type"],"mthod_name":shipping_table["mthod_name"],"handling_fees_type":shipping_table["handling_fees_type"],"handling_price":shipping_table["handling_price"]}
    #********Shipping Calculation (END)********#
    print("shipping_amount_arr===", json.dumps(shipping_amount_arr))
    #********APPLY COUPON CODE********#
    coupon_details = {}
    if cartdetails and coupon_code is not None:
        discount_array_coupon=generate_discount_conditions_coupon(website_id,user_group_id,coupon_code, warehouse_id)
        if discount_array_coupon and discount_array_coupon[0]["name"]!="invalid":
            if discount_array_coupon[0]["disc_type"] not in (3, 7):
                if discount_array_coupon[0]["coupon_type"]==2:
                    cartdetails=genrate_new_prodcut_with_discount_coupon(user_id,cartdetails,discount_array_coupon,order_total)
                else:
                    if discount_array_coupon[0]["used_coupon"]==0:
                        cartdetails=genrate_new_prodcut_with_discount_coupon(user_id,cartdetails,discount_array_coupon,order_total)
            else:
                if discount_array_coupon[0]["coupon_type"]==2:
                    coupon_details=genrate_new_prodcut_with_discount_coupon_order_total(user_id,cartdetails,discount_array_coupon,order_total)
                else:
                    if discount_array_coupon[0]["used_coupon"]==0:
                        coupon_details=genrate_new_prodcut_with_discount_coupon_order_total(user_id,cartdetails,discount_array_coupon,order_total)
    # print("coupon_details",json.dumps(coupon_details))
    
    #********APPLY COUPON CODE (END)********#
    orderamountdetails  = []
    applied_coupon      = []
    order_total         = 0
    order_weight        = 0
    total_tax           = 0
    shipping_amount     = 0
    handling_charge     = 0
    order_total_with_handling_price = 0
    gross_discount_amount = 0
    grandtotal= subtotal = nettotal = cart_discount = 0
    applied_cod_charge = float(0)
    product_cart_discount = 0
    if cartdetails:
        for products in cartdetails:
            order_total = float(order_total)+float(products["new_default_price"])+float(products["tax_price"])
            total_tax = float(total_tax)+float(products["tax_price"])
            #********PRODUCT TOTAL DISCOUNT (EXCLUDING WHOLE CART DISCOUNT)********#
            gross_discount_amount = float(gross_discount_amount)+float(products["discount_price"])
            if "coupon_code" in products and products["coupon_code"] is not None and products["coupon_code"]!="":
                    product_cart_discount = float(product_cart_discount) + float(products["product_coupon_discount_price"])

            print("product_cart_discount++++++", product_cart_discount)        
            if shipping_amount_arr["mthod_type"]!=0:
                shipping_price=float(shipping_amount_arr["shipping_amount"])*float(products["qty"])
                shipping_amount=float(shipping_amount)+float(shipping_price)
            else:
                shipping_amount=float(shipping_amount_arr["shipping_amount"])

        if shipping_amount_arr["handling_fees_type"]==0:
            handling_charge = shipping_amount_arr["handling_price"]
            order_total_with_handling_price = float(order_total)+float(handling_charge)
        else:
            handling_charge = float(order_total)*float(shipping_amount_arr["handling_price"])/float(100)
            order_total_with_handling_price = float(order_total)+float(handling_charge)

        #********TOTAL AMOUNT PRODUCT PRICE + SHIPPING CHARGE + HANDLING CHARGE ********#
        
        grandtotal = float(order_total_with_handling_price)+float(shipping_amount)
        

        #********APPLY COD CHAGE********#

        if cod_min_amount is not None and cod_max_amount is not None:
            if float(cod_min_amount)<=float(grandtotal) and float(grandtotal)<=float(cod_max_amount):
                grandtotal = float(grandtotal)+float(cod_charge)
                applied_cod_charge = float(cod_charge)
            else:
                grandtotal = grandtotal
                applied_cod_charge = float(0)
        else:
            grandtotal = grandtotal
            applied_cod_charge = float(0)

        #********APPLY COUPON DISCOUNT ON WHOLE CART********#
        if coupon_code and coupon_code is not None:
            if discount_array_coupon and discount_array_coupon[0]["name"]!="invalid":
                if discount_array_coupon[0]["disc_type"]==3:
                    grandtotal = float(grandtotal)
                    subtotal = float(grandtotal)-float(coupon_details["coupon_discount_amount"])
                    cart_discount = float(grandtotal)-float(subtotal)

                elif discount_array_coupon[0]["disc_type"]==7 and coupon_details['status'] == 'true':
                    grandtotal = float(grandtotal)
                    subtotal = float(grandtotal) - float(shipping_amount)
                    cart_discount = float(shipping_amount)
                    # shipping_amount = 0
                    gross_discount_amount = float(shipping_amount)

                else:
                    grandtotal = float(grandtotal)
                    subtotal = float(grandtotal)
                    cart_discount = float(grandtotal)-float(subtotal)

                # if coupon_details and float(coupon_details["coupon_discount_amount"]) >0:
                if coupon_details and coupon_details["status"] == 'true':
                    if discount_array_coupon[0]["disc_type"] == 7:
                        if float(shipping_amount) > 0:
                            applied_coupon_dict = {"name": discount_array_coupon[0]["name"],
                                                   "coupon_code": discount_array_coupon[0]["coupon_code"],
                                                   "disc_type": discount_array_coupon[0]["disc_type"],
                                                   "amount": cart_discount, "status": 1}

                        else:
                            applied_coupon_dict = {"name": discount_array_coupon[0]["name"],
                                                   "coupon_code": discount_array_coupon[0]["coupon_code"],
                                                   "disc_type": discount_array_coupon[0]["disc_type"],
                                                   "message": "Shipping charge is already zero", "status": 0}
                    else:
                        if float(coupon_details["coupon_discount_amount"]) > 0:
                            applied_coupon_dict = {"name": discount_array_coupon[0]["name"],
                                                   "coupon_code": discount_array_coupon[0]["coupon_code"],
                                                   "disc_type": discount_array_coupon[0]["disc_type"],
                                                   "amount": discount_array_coupon[0]["amount"], "status": 1}
                        else:
                            applied_coupon_dict = {"name": discount_array_coupon[0]["name"],
                                                   "coupon_code": discount_array_coupon[0]["coupon_code"],
                                                   "disc_type": discount_array_coupon[0]["disc_type"],
                                                   "message": "Invalid Coupon", "status": 0}
                else:
                    # if gross_discount_amount>0:
                    if float(cart_discount) >0:
                        applied_coupon_dict={"name":discount_array_coupon[0]["name"],"coupon_code":discount_array_coupon[0]["coupon_code"],"disc_type":discount_array_coupon[0]["disc_type"],"amount":gross_discount_amount,"status":1}
                    else:
                        if gross_discount_amount>0 and float(discount_array_coupon[0]["amount"])>0:
                            applied_coupon_dict={"name":discount_array_coupon[0]["name"],"coupon_code":discount_array_coupon[0]["coupon_code"],"disc_type":discount_array_coupon[0]["disc_type"], "amount":gross_discount_amount,"status":1}
                        else:
                            applied_coupon_dict={"name":discount_array_coupon[0]["name"],"coupon_code":discount_array_coupon[0]["coupon_code"],"disc_type":discount_array_coupon[0]["disc_type"],"message":"Minimum order amount not satisfied","status":0}

                applied_coupon.append(applied_coupon_dict)
            else:
                grandtotal = float(grandtotal)
                subtotal = float(grandtotal)
                cart_discount = float(grandtotal)-float(subtotal)
                applied_coupon_dict = {"name": discount_array_coupon[0]["name"],
                                       "coupon_code": discount_array_coupon[0]["coupon_code"],
                                       "message": discount_array_coupon[0]["message"], "status": 0, "disc_type": 0}
                applied_coupon.append(applied_coupon_dict)
        else:
            grandtotal = float(grandtotal)
            subtotal = float(grandtotal)
            cart_discount = float(grandtotal)-float(subtotal)

        #********APPLY COUPON DISCOUNT ON WHOLE CART(END)********#
    add_shipping_discount = 0
    if applied_coupon and int(applied_coupon[0]['disc_type']) == 7 and int(applied_coupon[0]['status']) == 1:
        add_shipping_discount = applied_coupon[0]['amount']

    # subtotal = float(subtotal) - float(shipping_amount)
    nettotal = float(subtotal)-float(total_tax)-float(shipping_amount)-float(handling_charge)-float(applied_cod_charge)
    balance_due = float(subtotal)-float(paid_amount)

    # Minimum order Amount
    minimum_order_amount = 0
    minimum_order_amount_check = 'yes'
    rs_min_order = EngageboostWarehouseMasters.objects.filter(id=warehouse_id).first()
    if rs_min_order.min_order_amount is not None and float(rs_min_order.min_order_amount)>0:
        minimum_order_amount = float(rs_min_order.min_order_amount)
    else:            
        rs_global_settings = EngageboostGlobalSettings.objects.filter(isblocked='n', isdeleted='n', website_id= website_id).first()
        if rs_global_settings and float(rs_global_settings.min_order_amount)>0:
            minimum_order_amount = float(rs_global_settings.min_order_amount)

    if float(subtotal)<float(minimum_order_amount):
        minimum_order_amount_check = 'no'

    orderamountdetails_dict = {
        "company_id": company_id,
        "website_id": website_id,
        "webshop_id": webshop_id,
        "payment_method_id": payment_method_id,
        "tax_amount": Decimal(total_tax).quantize(Decimal('.00')),
        "shipping_charge": shipping_amount,
        "handling_charge": Decimal(handling_charge).quantize(Decimal('.00')),
        "cod_charge": Decimal(applied_cod_charge).quantize(Decimal('.00')),
        "gross_discount": Decimal(gross_discount_amount).quantize(Decimal('.00')),
        "product_cart_discount": Decimal(product_cart_discount).quantize(Decimal('.00')),
        "min_amount": cod_min_amount,
        "max_amount": cod_max_amount,
        "grand_total": Decimal(grandtotal - float(add_shipping_discount)).quantize(Decimal('.00')),
        "sub_total": Decimal(subtotal - float(shipping_amount) + float(add_shipping_discount)).quantize(Decimal('.00')),
        "net_total": Decimal(nettotal + float(add_shipping_discount)).quantize(Decimal('.00')),
        "cart_discount": Decimal(cart_discount).quantize(Decimal('.00')),
        "paid_amount": Decimal(paid_amount).quantize(Decimal('.00')),
        "balance_due": Decimal(balance_due).quantize(Decimal('.00')),
        "minimum_order_amount": minimum_order_amount,
        "minimum_order_amount_check": minimum_order_amount_check,
        "check_stock_msg": check_stock_msg,
        "check_stock": check_stock,
        "product_categories": lst_product_cat,
        "add_shipping_discount": Decimal(add_shipping_discount).quantize(Decimal('.00'))
    }

    orderamountdetails.append(orderamountdetails_dict)

    # data={"cartdetails":cartdetails,"orderamountdetails":orderamountdetails,"min_amount":cod_min_amount,"max_amount":cod_max_amount,"cod_charge":cod_charge,"shipping_flat":shipping_flat,"shipping_table":shipping_table,"shipping_free":shipping_free,"discount_array_coupon":discount_array_coupon}
    data={"cartdetails":cartdetails,"orderamountdetails":orderamountdetails,"applied_coupon":applied_coupon,"shipping_flat":shipping_flat,"shipping_table":shipping_table, "cart_count":cart_count}
    return Response(data)
    # return data
def get_discount_detalils(data_arr):
    # company_db = loginview.db_active_connection(request)
    company_id = data_arr["company_id"]
    website_id = data_arr["website_id"]        
    product_ids= data_arr["product_ids"]
    qtys       = data_arr["qtys"]
    prod_price = data_arr["prod_price"]
    warehouse_id = data_arr["warehouse_id"]

    payment_method_id = data_arr["payment_method_id"] if data_arr.get("payment_method_id") else None
    user_id = data_arr["user_id"] if data_arr.get("user_id") else None
    user_group_id = data_arr["user_group_id"] if data_arr.get("user_group_id") else None
    
    cartdetails=[];checkout_info=[];new_unit_netamount=[];new_total_netamount=[]

    quantity = qtys
    if prod_price and quantity:
        new_unit_netamount.append(float(prod_price)/int(quantity))
        new_total_netamount.append(float(prod_price)*int(quantity))
    else:
        new_unit_netamount.append(0)
        new_total_netamount.append(0)

    discount_array_net = generate_discount_conditions(website_id,user_group_id, None, warehouse_id)
    getproductforcart_net = getproductforcart(product_ids, warehouse_id)

    # for getproductforcartnet in getproductforcart_net:
    #     getproductforcartnet["qty"]=int(quantity)
    #     try:
    #         if getproductforcartnet["new_default_price"]: getproductforcartnet["new_default_price"] = getproductforcartnet["new_default_price"]
    #         else: getproductforcartnet["new_default_price"] = getproductforcartnet["default_price"]
    #     except KeyError: getproductforcartnet["new_default_price"] = getproductforcartnet["default_price"]

    getproductforcart_net["qty"]=int(quantity)
    try:
        if getproductforcart_net["new_default_price"]: 
            getproductforcart_net["new_default_price"] = float(getproductforcart_net["new_default_price"])*int(getproductforcart_net["qty"])
            getproductforcart_net["new_default_price_unit"] = float(getproductforcart_net["channel_price"]) if getproductforcart_net["channel_price"] else 0.0
            getproductforcart_net["discount_price_unit"] = 0.00   
            getproductforcart_net["discount_price"] = 0.00
            getproductforcart_net["discount_amount"] = 0.00
            getproductforcart_net["disc_type"] =""
            getproductforcart_net["coupon"] = ""
        else: 
            getproductforcart_net["new_default_price"] = float(getproductforcart_net["default_price"])*int(getproductforcart_net["qty"])
            getproductforcart_net["new_default_price_unit"] = float(getproductforcart_net["channel_price"]) if getproductforcart_net["channel_price"] else 0.0
            getproductforcart_net["discount_price_unit"] = 0.00   
            getproductforcart_net["discount_price"] = 0.00
            getproductforcart_net["discount_amount"] = 0.00
            getproductforcart_net["disc_type"] = ""
            getproductforcart_net["coupon"] = ""
        
    except Exception as error:
        getproductforcart_net["new_default_price"] = float(getproductforcart_net["default_price"])*int(getproductforcart_net["qty"])
        getproductforcart_net["new_default_price_unit"] = float(getproductforcart_net["channel_price"]) if getproductforcart_net["channel_price"] else 0.0
        getproductforcart_net["discount_price_unit"] = 0.00   
        getproductforcart_net["discount_price"] = 0.00
        getproductforcart_net["discount_amount"] = 0.00
        getproductforcart_net["disc_type"] = ""
        getproductforcart_net["coupon"] = ""
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": "Error in order update."}

    # ********Apply Discount and Get New Product Amount********#
    product_detail_net = genrate_new_prodcut_with_discount(user_id,getproductforcart_net,discount_array_net)
    # product_detail_net = product_detail_net[0]



    #********Tax Calculation********#
    # if country_id!="" or state_id!="" or post_code!="":
    #     tax_price_arr = get_price_including_tax(website_id,company_id,product_detail_net,country_id,state_id,post_code,'back')

    #     company_info = EngageboostCompanyWebsites.objects.filter(id=website_id).first()
    #     if company_info:
    #         company_state=company_info.state
    #     else:
    #         company_state=0
    #     print("KKk")
    #     if str(company_state)!=str(state_id):
    #         product_tax={"tax_price_unit":float(tax_price_arr["tax_igst"]),"tax_price":float(tax_price_arr["tax_igst"])*float(product_detail_net["qty"]),"tax_percentage":tax_price_arr["igst"],"tax_name":tax_price_arr["tax_name"],"cgst":tax_price_arr["cgst"],"sgst":tax_price_arr["sgst"],"igst":tax_price_arr["igst"],"cess":tax_price_arr["cess"],"is_igst":"yes","tax_type":tax_price_arr["tax_type"]}
    #     else:
    #         product_tax={"tax_price_unit":float(tax_price_arr["tax_igst"]),"tax_price":float(tax_price_arr["tax_igst"])*float(product_detail_net["qty"]),"tax_percentage":tax_price_arr["igst"],"tax_name":tax_price_arr["tax_name"],"cgst":tax_price_arr["cgst"],"sgst":tax_price_arr["sgst"],"igst":tax_price_arr["igst"],"cess":tax_price_arr["cess"],"is_igst":"no","tax_type":tax_price_arr["tax_type"]}
    #     print(product_tax)
    #     product_detail_net=dict(product_detail_net,**product_tax)

    #     if product_detail_net["tax_type"]=="including":
    #         product_detail_net["new_default_price_unit"]=float(product_detail_net["new_default_price_unit"])-float(product_detail_net["tax_price_unit"])
    #         product_detail_net["new_default_price"]=float(product_detail_net["new_default_price"])-float(product_detail_net["tax_price"])
    #********Tax Calculation (END)********#

    cartdetails.append(product_detail_net)        
    return cartdetails
