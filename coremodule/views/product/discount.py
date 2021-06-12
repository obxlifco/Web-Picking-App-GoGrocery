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
from coremodule.coremodule_serializers import *

import json
import base64

import datetime


class ProductDiscountCalculation(generics.ListAPIView):
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


def generate_discount_conditions(website_id,user_group_id,discountIds=None):
    now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
    if user_group_id:
        DiscountMasterCond = EngageboostDiscountMasters.objects.order_by("discount_priority").filter(website_id=website_id,disc_start_date__lte=now_utc,disc_end_date__gte=now_utc,customer_group__iregex=r"\y{0}\y".format(user_group_id),isdeleted='n',isblocked='n',discount_master_type=0).all()
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

def getproductforcart(product_id):
    condition = EngageboostProducts.objects.filter(isdeleted='n',isblocked='n',id=product_id).all().values("id","name","brand","hsn_id","sku","slug","description","default_price","weight","taxclass_id","amazon_itemid","twitter_addstatus","amazon_addstatus","status","warehouse")
    # print(condition.query)
    product_details = BasicinfoSerializer(condition,many=True)
    # print(product_details.data)
    conditions = EngageboostProductCategories.objects.filter(product_id=product_id).first()
    if conditions:
        product_details.data[0]["category_id"]=conditions.category_id
    
    return product_details.data

def genrate_new_prodcut_with_discount(user_id=None,product_array=None,discount_array_new=None,category_id=None,sub_category_id=None,cart_subtotal=None):
    # print(json.dumps(discount_array_new, indent=4, sort_keys=True))
    if discount_array_new:
        for discount_array in discount_array_new:
            for product in product_array:
                return_price = check_in_prod_disc(user_id,product,discount_array,category_id,sub_category_id,cart_subtotal)
                price_array = return_price.split('^')
                if price_array[1] != "product" and price_array[1] > "0" and float(product["default_price"]) != float(price_array[0]):
                    product["new_default_price_unit"]   = float(price_array[0])
                    product["new_default_price"]        = float(price_array[0])*float(product["qty"])
                    product["discount_price_unit"]      = float(price_array[1])
                    product["discount_price"]           = float(price_array[1])*float(product["qty"])
                    product["discount_amount"]          = float(discount_array["amount"])
                    product["disc_type"]                = discount_array["disc_type"]
                    product["coupon"]                   = discount_array["name"]
                else:
                    product["new_default_price_unit"] = float(product["default_price"])
                    product["new_default_price"] = float(product["default_price"])*float(product["qty"])
                    product["discount_price_unit"] = float(price_array[1])
                    product["discount_price"] = float(price_array[1])*float(product["qty"])
                    product["discount_amount"] = float(0)
                    product["disc_type"] = ""
                    product["coupon"] = ""
    else:
        for product in product_array:
            product["new_default_price_unit"] = float(product["default_price"])
            product["new_default_price"] = float(product["default_price"])*float(product["qty"])
            product["discount_price_unit"] = float(0)
            product["discount_price"] = float(0)*float(product["qty"])
            product["discount_amount"] = float(0)
            product["disc_type"] = ""
            product["coupon"] = ""

    return product_array

def check_in_prod_disc(user_id=None,ind_product=None,discount_array=None,category_id=None,sub_category_id=None,cart_subtotal=None):
    discount_array_condition = discount_array["discount_conditions"]
    product_array_disc_applied = []
    i=0
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
            print(json.dumps(ind_product, indent=4, sort_keys=True))
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

    return str(default_price)+"^"+str(discount_price)

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

def rate_flat(website_id='1',company_id=None,country_id=None,state_id=None,post_code=None,order_from='front'):
    #******** FOR FLAT RATE CALCULATION ********#
    if state_id:
        conditions = EngageboostShippingMastersSettings.objects.filter(website_id=website_id,country_ids__iregex=r"\y{0}\y".format(country_id),state_id__iregex=r"\y{0}\y".format(state_id),shipping_method_id='4',isblocked='n',isdeleted='n').all()
    else:
        conditions = EngageboostShippingMastersSettings.objects.filter(website_id=website_id,country_ids__iregex=r"\y{0}\y".format(country_id),shipping_method_id='4',isblocked='n',isdeleted='n').all()

    data={"shipping_type":"Flat Shipping","mthod_type":0,"mthod_name":"orderwise","flat_price":float(0),"handling_fees_type":0,"handling_price":float(0)}

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

def generate_discount_conditions_coupon(website_id,user_group_id=None,coupon_code=None):
    now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
    all_discount_data=[]
    discount_multi_coupon=EngageboostDiscountMastersCoupons.objects.filter(isdeleted='n',coupon_code=coupon_code).first()
    if discount_multi_coupon:
        discount_master_id=discount_multi_coupon.discount_master_id
        condition_discount_coupon_part=EngageboostDiscountMasters.objects.filter(id=discount_master_id).all()
    else:
        condition_discount_coupon_part=EngageboostDiscountMasters.objects.filter(coupon_code=coupon_code).all()

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

                discount_master_coupon = EngageboostDiscountMastersCoupons.objects.order_by("id").filter(discount_master_id=condition_discount_coupon["id"],isdeleted='n').all()
                if discount_master_coupon:
                    discount_master_coupon_serializer = DiscountMasterCouponSerializer(discount_master_coupon,many=True)
                    condition_discount_coupon["DiscountMasterCoupon"]=discount_master_coupon_serializer.data

            all_discount_data=condition_discount_coupon_part_serialize.data
        else:
            data={"name":"invalid","coupon_code":coupon_code,"message":"Coupon code expired or Condition not satisfied"}
            all_discount_data.append(data)
    else:
        data={"name":"invalid","coupon_code":coupon_code,"message":"Invalid Coupon Code"}
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
                product["coupon_disc_type"] = discount_array["disc_type"]
                product["coupon_name"] = discount_array["name"]
                product["coupon_code"] = discount_array["coupon_code"]
            else:
                product["coupon_discount_amount"] = float(0)
                product["coupon_disc_type"] = ""
                product["coupon_name"] = ""
                product["coupon_code"] = ""

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
                    sub_category_id_array.append(pro["category"]["id"])

            if sub_category_id_array:
                for index in range(len(sub_category_id_array)):
                    if ind_cond["condition"] == "==":
                        if sub_category_id_array[index] in category_id_array:
                            flag = "true"
                            break
                        else:
                            flag = "false"
                    else:
                        if sub_category_id_array[index] in category_id_array:
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
        coupon_details_dict={"coupon_discount_amount":float(0),"coupon_disc_type":coupon_details["coupon_disc_type"],"coupon_name":coupon_details["coupon_name"],"coupon_code":coupon_details["coupon_code"]}
        return coupon_details_dict
    else:
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
                    sub_category_id_array.append(pro["category"]["id"])

            if sub_category_id_array:
                for index in range(len(sub_category_id_array)):
                    if ind_cond["condition"] == "==":
                        if sub_category_id_array[index] in category_id_array:
                            flag = "true"
                            break
                        else:
                            flag = "false"
                    else:
                        if sub_category_id_array[index] in category_id_array:
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

def payment_method_onepage_checkout(website_id):
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
    # listing_products = [{
    #     "amazon_addstatus": "1",
    #     "amazon_itemid": "1",
    #     "brand": "1",
    #     "category_id": 1,
    #     "default_price": "100.00",
    #     "id": 1,
    #     "name": "Fortune Sunflower Refined Oil",
    #     "new_default_price": "100.00",
    #     "qty": "1",
    #     "sku": "FRTN542",
    #     "slug": "fortune-sunflower-refined-oil",
    #     "status": "n",
    #     "twitter_addstatus": "1"
    # }]
    # print(json.dumps(listing_products, indent=4, sort_keys=True))
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


class TestClass(generics.ListAPIView):
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


def GetCartDetails(company_id, website_id, customer_id=None, device_id=None, webshop_id=None, country_id = None, state_id = None, post_code = None, user_id = None, user_group_id = None, coupon_code = None):
    # company_db = loginview.db_active_connection(request)
    company_id = company_id
    website_id = website_id
    webshop_id = webshop_id if webshop_id else 6

    rs_cart = EngageboostTemporaryShoppingCarts.objects.filter(website_id=website_id)
    if customer_id:
        rs_cart = rs_cart.filter(customer_id=customer_id)
    elif device_id:
        rs_cart = rs_cart.filter(customer_id=0, device_id=device_id)

    cart_data = EngageboostTemporaryShoppingCartsSerializer(rs_cart, many=True)

    country_id = country_id
    state_id = state_id
    post_code = post_code
    user_id = user_id
    user_group_id = user_group_id
    coupon_code = coupon_code

    payment_method_id = 16
    paid_amount = 0
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

    for cartdata in cart_data.data:
        product_id = cartdata['product_id']['id']
        new_unit_netamount.append(float(cartdata['product_id']['default_price'])/float(cartdata['quantity']))
        new_total_netamount.append(float(cartdata['product_id']['default_price'])/float(cartdata['quantity']))
        discount_array_net = generate_discount_conditions(website_id,user_group_id)
        getproductforcart_net = getproductforcart(product_id)
        for getproductforcartnet in getproductforcart_net:
            getproductforcartnet["qty"]=cartdata['quantity']
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

    # data={"cartdetails":cartdetails,"orderamountdetails":orderamountdetails,"min_amount":cod_min_amount,"max_amount":cod_max_amount,"cod_charge":cod_charge,"shipping_flat":shipping_flat,"shipping_table":shipping_table,"shipping_free":shipping_free,"discount_array_coupon":discount_array_coupon}
    data={"cartdetails":cartdetails,"orderamountdetails":orderamountdetails,"applied_coupon":applied_coupon,"shipping_flat":shipping_flat,"shipping_table":shipping_table}

    return Response(data)
    
def get_discount_detalils(data_arr):
    # company_db = loginview.db_active_connection(request)
    company_id = data_arr["company_id"]
    website_id = data_arr["website_id"]        
    product_ids= data_arr["product_ids"]
    qtys       = data_arr["qtys"]
    prod_price = data_arr["prod_price"]        
    payment_method_id = data_arr["payment_method_id"] if data_arr.get("payment_method_id") else None
    user_id = data_arr["user_id"] if data_arr.get("user_id") else None
    user_group_id = data_arr["user_group_id"] if data_arr.get("user_group_id") else None
    

    cartdetails=[];checkout_info=[];new_unit_netamount=[];new_total_netamount=[]

    quantity = qtys
                
    new_unit_netamount.append(float(prod_price)/float(quantity))
    new_total_netamount.append(float(prod_price)*float(quantity))
    discount_array_net = generate_discount_conditions(website_id,user_group_id)
    getproductforcart_net = getproductforcart(product_ids)
    for getproductforcartnet in getproductforcart_net:
        getproductforcartnet["qty"]=quantity
        try:
            if getproductforcartnet["new_default_price"]: getproductforcartnet["new_default_price"] = getproductforcartnet["new_default_price"]
            else: getproductforcartnet["new_default_price"] = getproductforcartnet["default_price"]
        except KeyError: getproductforcartnet["new_default_price"] = getproductforcartnet["default_price"]

    # ********Apply Discount and Get New Product Amount********#
    product_detail_net = genrate_new_prodcut_with_discount(user_id,getproductforcart_net,discount_array_net)
    product_detail_net = product_detail_net[0]            
    cartdetails.append(product_detail_net)        
    return cartdetails

def GetCartDetailsPos(data_arr):
    # company_db = loginview.db_active_connection(request)
    print(data_arr)
    company_id = data_arr["company_id"]
    website_id = data_arr["website_id"]
    webshop_id = data_arr["webshop_id"] if data_arr.get("webshop_id") else 6
    product_ids= data_arr["product_ids"]
    qtys       = data_arr["qtys"]
    prod_price = data_arr["prod_price"]

    country_id = data_arr["country_id"] if data_arr.get("country_id") else ""
    state_id = data_arr["state_id"] if data_arr.get("state_id") else ""
    post_code = data_arr["post_code"] if data_arr.get("post_code") else ""
    payment_method_id = data_arr["payment_method_id"] if data_arr.get("payment_method_id") else None
    user_id = data_arr["user_id"] if data_arr.get("user_id") else None
    user_group_id = data_arr["user_group_id"] if data_arr.get("user_group_id") else None
    coupon_code = data_arr["coupon_code"] if data_arr.get("coupon_code") else None
    paid_amount = float(data_arr["paid_amount"]) if data_arr.get("paid_amount") else float(0)

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
    return data
   
   
