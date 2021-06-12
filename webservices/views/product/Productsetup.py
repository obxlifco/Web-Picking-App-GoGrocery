from webservices.models import *
from webservices.models import EngageboostProducts
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import generics
from itertools import chain
from django.core import serializers
from django.http import HttpResponse
from webservices.views import loginview
from webservices.serializers import *
from django.db import connection
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
import os
import socket
import json
import requests
import datetime
import random
import tinys3
import urllib
import base64
import pytz
import xlsxwriter
import xlrd
import time
import string
import math
import ast
import re
import unidecode
from django.template.defaultfilters import slugify
from webservices.views.common import common
from django.db.models.aggregates import Aggregate
from django.contrib.postgres.aggregates import *
from webservices.views.common.threading import *
from webservices.views.emailcomponent import emailcomponent
from elasticsearch import helpers

class Productsetup(generics.ListAPIView):
    # """ List all users, or create a new user """
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        obj = EngageboostProducts.objects.using(company_db).latest('id')
        last_id = obj.id
        requestdata = JSONParser().parse(request)
        default_price = requestdata['default_price']
        EngageboostProducts.objects.using(company_db).filter(id=last_id).update(default_price=default_price)

        data ={'status':1,'message':'Successfully Inserted'}

        return Response(data)

class ViewProductDetails(generics.ListAPIView):
    def get(self, request, pid, format=None):
        company_db = loginview.db_active_connection(request)
        
        stock = 0
        safetyStock = 0
        virtualStock = 0
        realStock = 0
        product_amount = 0
        product_discount = 0
        cancel_product_amount = 0
        cancel_product_discount = 0
        totalamount = 0
        product_info=dict()

        ProductDetailsCond = EngageboostProducts.objects.using(company_db).filter(id=pid).first()
        if ProductDetailsCond:
            ProductDetails = BasicinfoSerializer(ProductDetailsCond,partial=True)
            product_info["name"] = ProductDetails.data['name']
            product_info["sku"] = ProductDetails.data['sku']
            product_info["description"] = ProductDetails.data['description']
            
            ean = ""
            prodObj = EngageboostMultipleBarcodes.objects.values().filter(product_id=pid)
            if prodObj.count()>0:
                prodObjDefault = prodObj.filter(default_ean='y')
                if prodObjDefault.count()>0:
                    prodObj = prodObjDefault.first()
                else:
                    prodObj = prodObj.first()    
                ean = prodObj['barcode']    


            product_info["ean"] = ean
            if ProductDetails.data['status'] == 'n':
                product_info["status"] = 'Disable'
            else:
                product_info["status"] = 'Enable'

            if ProductDetails.data['brand']:
                brands = []
                brand_list= ProductDetails.data['brand'].split(',')
                BrandDetailsObj = EngageboostBrandMasters.objects.using(company_db).filter(id__in=brand_list,isblocked='n',isdeleted='n')
                if BrandDetailsObj.count()>0:
                    BrandDetails = BrandDetailsObj.all()
                    for item in BrandDetails:   
                        brands.append(item.name)
                    if len(brands)>0:
                        product_info["brand"] = ','.join(brands)
                    else:
                        product_info["brand"] = ''
                else:
                    product_info["brand"] = ''
            else:
                product_info["brand"] = ''

            ProductImage = EngageboostProductimages.objects.using(company_db).filter(product_id=pid,is_cover=1).first()
            if ProductImage:
                product_info["image"] = ProductImage.img
            else:
                product_info["image"] = ''
        
        # ProductStockCond = EngageboostProductStocks.objects.using(company_db).all().filter(product_id=pid)
        # if ProductStockCond:
        #     # ProductStockList = StockSerializer(ProductStockCond,many=True)
        #     # return Response(ProductStockList.data)
        #     for ProductStock in ProductStockCond:
        #         # return Response(ProductStock)
        #         if ProductStock.stock >= 0:
        #             stock = stock+ProductStock.stock

        #         if ProductStock.safety_stock:
        #             safetyStock = safetyStock+ProductStock.safety_stock

        #         if ProductStock.virtual_stock:
        #             virtualStock = virtualStock+ProductStock.virtual_stock

        #         if ProductStock.real_stock >= 0:
        #             realStock = realStock+ProductStock.real_stock


        # OrderProductsCond = EngageboostOrderProducts.objects.using(company_db).all().filter(product_id=pid)
        # if OrderProductsCond:
        #     OrderProductsDetails = OrderProductsSerializer(OrderProductsCond,many=True)
        #     for OrderProducts in OrderProductsDetails.data:
        #         product_price_base = OrderProducts["product_price_base"] if OrderProducts["product_price_base"] else 0
        #         product_discount_price_base = OrderProducts["product_discount_price_base"] if OrderProducts["product_discount_price_base"] else 0
        #         quantity = OrderProducts["quantity"] if OrderProducts["quantity"] else 0
        #         deleted_quantity = OrderProducts["deleted_quantity"] if OrderProducts["deleted_quantity"] else 0
                
        #         product_amount = product_amount+(product_price_base*quantity)
        #         product_discount = product_discount+(product_discount_price_base*quantity)

        #         cancel_product_amount = cancel_product_amount+(product_price_base*deleted_quantity)
        #         cancel_product_discount = cancel_product_discount+(product_discount_price_base*deleted_quantity)

        #         totalamount = (product_amount-product_discount)-(cancel_product_amount-cancel_product_discount)
        
        #********* Start Stock Summary **********#
        # cursor = connection.cursor()
        # cursor.execute("SELECT PurchaseOrderReceived.*,PurchaseOrderReceivedProduct.quantity as qty,PurchaseOrderReceivedProduct.product_id as product_id,PurchaseOrderReceivedProduct.purchase_order_received_id FROM engageboost_purchase_order_received_products PurchaseOrderReceivedProduct JOIN engageboost_purchase_orders_received PurchaseOrderReceived ON PurchaseOrderReceived.id = PurchaseOrderReceivedProduct.purchase_order_received_id WHERE PurchaseOrderReceivedProduct.product_id="+pid+" AND ((PurchaseOrderReceived.order_id = '0' AND PurchaseOrderReceived.action IN ('Increase','Decrease','Refund','increase','decrease','refund')) OR PurchaseOrderReceived.action = 'Refund')")
        
        # col_names = [product_id[0] for product_id in cursor.description]
        # StockSummaryArr=[]
        # for row in cursor.fetchall():
        #     row_dict = []
        #     for field in zip(col_names, row):
        #         row_dict.append(field)
        #     StockSummaryArr.append(dict(row_dict))

        # if StockSummaryArr:
        #     qty_in_hand = 0
        #     for StockSummary in StockSummaryArr:
        #         StockSummary.pop('quantity')
        #         StockSummary['received_date'] = covert_time(StockSummary['received_date'],"UTC","Asia/Kolkata")
        #         StockSummary['quantity'] = StockSummary['qty']
        #         StockSummary.pop('qty')

        #         PurchaseOrders = EngageboostPurchaseOrders.objects.using(company_db).filter(id=StockSummary['purchase_order_master_id']).first()
        #         if PurchaseOrders:
        #             StockSummary['purchase_order_id'] = PurchaseOrders.purchase_order_id

        #         SuppliersDetails = EngageboostSuppliers.objects.using(company_db).filter(id=StockSummary['supplier_id']).first()
        #         if SuppliersDetails:
        #             StockSummary['supplier_name'] = SuppliersDetails.name

        #         OrderDetails = EngageboostOrdermaster.objects.using(company_db).filter(id=StockSummary['order_id']).first()
        #         if OrderDetails:
        #             StockSummary['custom_order_id'] = OrderDetails.custom_order_id
        #         else:
        #             StockSummary['custom_order_id'] = ''
        #********* End Stock Summary **********#

        #********* Start Purchase Order **********#
        # ProductDetails = EngageboostProducts.objects.using(company_db).filter(id=pid).first()
        # if ProductDetails:
        PurchaseOrderProductsDetailsData = []
        PurchaseOrderProductsDetailsCond = EngageboostPurchaseOrderProducts.objects.using(company_db).filter(product_id=pid)
        if PurchaseOrderProductsDetailsCond:
            PurchaseOrderProductsDetails = PurchaseOrderProductSerializer(PurchaseOrderProductsDetailsCond,many=True)
            for PurchaseOrderProducts in PurchaseOrderProductsDetails.data:
                PurchaseOrdersCond = EngageboostPurchaseOrders.objects.using(company_db).filter(id=PurchaseOrderProducts['purchase_order_id']).first()
                if PurchaseOrdersCond:
                    PurchaseOrders = PurchaseOrderSerializer(PurchaseOrdersCond,partial=True)
                    purchase_ord_prd_order_date = PurchaseOrders.data['order_date'].split('T')
                    PurchaseOrders.data['order_date'] = covert_time(purchase_ord_prd_order_date[0],"UTC","Asia/Kolkata")
                    PurchaseOrderProducts["PurchaseOrder"]=PurchaseOrders.data

                    SuppliersDetailsCond = EngageboostSuppliers.objects.using(company_db).filter(id=PurchaseOrders.data['supplier_id']).first()
                    if SuppliersDetailsCond:
                        SuppliersDetails = SuppliersSerializer(SuppliersDetailsCond,partial=True)
                        PurchaseOrderProducts["supplier"] = SuppliersDetails.data

                    WarehouseDetailsCond = EngageboostWarehouseMasters.objects.using(company_db).filter(id=PurchaseOrders.data['warehouse_id']).first()
                    if WarehouseDetailsCond:
                        WarehouseDetails = WarehousemastersSerializer(WarehouseDetailsCond,partial=True)
                        PurchaseOrderProducts["warehouse"] = WarehouseDetails.data
            PurchaseOrderProductsDetailsData = PurchaseOrderProductsDetails.data
        #********* End Purchase Order **********#
        
        #********* Start Receipt Section **********#
        # EngageboostPurchaseOrdersReceived
        ProductReceiptArray = []
        PurchaseOrderReceivedProductsCond = EngageboostPurchaseOrderReceivedProducts.objects.using(company_db).filter(product_id=pid).all()
        if PurchaseOrderReceivedProductsCond:
            PurchaseOrderReceivedProductsDetails = PurchaseOrderReceivedProductsSerializer(PurchaseOrderReceivedProductsCond, many=True)
            for PurchaseOrderReceivedProducts in PurchaseOrderReceivedProductsDetails.data:
                ProductReceiptDict = dict()
                ProductReceiptDict["PurchaseOrderReceivedProduct"] = PurchaseOrderReceivedProducts
                # PurchaseOrderReceivedProducts.update({"purchase_order_received":PurchaseOrderReceivedProducts})
                if PurchaseOrderReceivedProducts:
                    if PurchaseOrderReceivedProducts['purchase_order_received'] is not None:
                        ProductReceiptDict["PurchaseOrdersReceived"] = PurchaseOrderReceivedProducts
                        PurchaseOrdersCond = EngageboostPurchaseOrders.objects.using(company_db).filter(id=PurchaseOrderReceivedProducts['purchase_order_received']['purchase_order_master_id']).first()
                        if PurchaseOrdersCond:
                            PurchaseOrdersDetails = PurchaseOrderSerializer(PurchaseOrdersCond,many=True)
                            ProductReceiptDict["PurchaseOrder"] = PurchaseOrders.data                            

                        SuppliersDetailsCond = EngageboostSuppliers.objects.using(company_db).filter(id=PurchaseOrderReceivedProducts['purchase_order_received']['supplier_id']).first()
                        if SuppliersDetailsCond:
                            SuppliersDetails = SuppliersSerializer(SuppliersDetailsCond,partial=True)
                            ProductReceiptDict["Supplier"] = SuppliersDetails.data

                        WarehouseDetailsCond = EngageboostWarehouseMasters.objects.using(company_db).filter(id=PurchaseOrderReceivedProducts['purchase_order_received']['warehouse_id']).first()
                        if WarehouseDetailsCond:
                            WarehouseDetails = WarehousemastersSerializer(WarehouseDetailsCond,partial=True)
                            ProductReceiptDict["Warehouse"] = WarehouseDetails.data

                        ProductMoveTrackCond = EngageboostProductMoveTrack.objects.using(company_db).filter(purchase_order_received_id=PurchaseOrderReceivedProducts['purchase_order_received']['id'])
                        if ProductMoveTrackCond:
                            ProductMoveTrackDetails = ProductMoveTrackSerializer(ProductMoveTrackCond,partial=True)
                            ProductReceiptDict["ProductMoveTrack"] = ProductMoveTrackDetails.data

                ProductReceiptArray.append(ProductReceiptDict)
        #********* Start Receipt Section **********#

        #********* List of Product Promotion **********#
        promotion_list_cond = EngageboostDiscountMastersConditions.objects.filter(all_product_id__iregex=r"\y{0}\y".format(pid)).all().values("id","discount_master_id")
        if promotion_list_cond:
            # promotion_list = DiscountConditionsSerializer(promotion_list_cond,many=True)
            for promotionlist in promotion_list_cond:
                discount_master = EngageboostDiscountMasters.objects.filter(id=promotionlist['discount_master_id']).first()
                if discount_master:
                    promotionlist["discount_name"]=discount_master.name
                else:
                    promotionlist["discount_name"]=""
            # promotionList=promotion_list.data
        else:
            promotionList=[]
        #********* List of product promotion **********#
        product_data={
            "status":1, 
            "product_details":product_info,
            # "stock":stock,
            # "safetyStock":safetyStock,
            # "virtualStock":virtualStock,
            # "realStock":realStock,
            "totalamount":totalamount,
            # "product_stock_summary":StockSummaryArr,
            "product_purchase_order":PurchaseOrderProductsDetailsData,
            "product_receipt_details":ProductReceiptArray,
            "product_promotion":promotion_list_cond
        }
        return Response(product_data)

class ViewProductInventoryDetails(generics.ListAPIView):
    def get(self, request, pid, user_id, format=None):
        company_db = loginview.db_active_connection(request)
        
        stock = 0
        safetyStock = 0
        virtualStock = 0
        realStock = 0
        product_amount = 0
        product_discount = 0
        cancel_product_amount = 0
        cancel_product_discount = 0
        totalamount = 0
        
        #********* Start Stock Summary **********#
        cursor = connection.cursor()
        cursor.execute("SELECT PurchaseOrderReceived.*,PurchaseOrderReceivedProduct.quantity as qty,PurchaseOrderReceivedProduct.product_id as product_id,PurchaseOrderReceivedProduct.purchase_order_received_id FROM engageboost_purchase_order_received_products PurchaseOrderReceivedProduct JOIN engageboost_purchase_orders_received PurchaseOrderReceived ON PurchaseOrderReceived.id = PurchaseOrderReceivedProduct.purchase_order_received_id WHERE PurchaseOrderReceivedProduct.product_id="+pid+" AND ((PurchaseOrderReceived.order_id = '0' AND PurchaseOrderReceived.action IN ('Increase','Decrease','Refund','increase','decrease','refund')) OR PurchaseOrderReceived.action = 'Refund')")
        col_names = [product_id[0] for product_id in cursor.description]
        
        StockSummaryArr=[]
        # result = cursor.fetchaone()
        # row_dict = dict(zip(col_names, row))
        for row in cursor.fetchall():
            row_dict = []
            for field in zip(col_names, row):
                row_dict.append(field)
            StockSummaryArr.append(dict(row_dict))
        # return Response(StockSummaryArr)
        if StockSummaryArr:
            qty_in_hand = 0
            for StockSummary in StockSummaryArr:
                StockSummary.pop('quantity')
                StockSummary['received_date'] = covert_time(StockSummary['received_date'],"UTC","Asia/Kolkata")
                StockSummary['quantity'] = StockSummary['qty']
                StockSummary.pop('qty')

                PurchaseOrders = EngageboostPurchaseOrders.objects.using(company_db).filter(id=StockSummary['purchase_order_master_id']).first()
                if PurchaseOrders:
                    StockSummary['purchase_order_id'] = PurchaseOrders.purchase_order_id

                SuppliersDetails = EngageboostSuppliers.objects.using(company_db).filter(id=StockSummary['supplier_id']).first()
                if SuppliersDetails:
                    StockSummary['supplier_name'] = SuppliersDetails.name

                OrderDetails = EngageboostOrdermaster.objects.using(company_db).filter(id=StockSummary['order_id']).first()
                if OrderDetails:
                    StockSummary['custom_order_id'] = OrderDetails.custom_order_id
                else:
                    StockSummary['custom_order_id'] = ''
        #********* End Stock Summary **********#

        #********* Start Grid Headings *********#
        row_dict={}
        row=[]
        module='ProductStockSummary'
        screen_name='list-custom'
        layout_fetch=EngageboostGridLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
        layout_header=layout_fetch.header_name.split("@@")
        layout_field=layout_fetch.field_name.split("@@")
        layout_check=EngageboostGridColumnLayouts.objects.using(company_db).filter(module=module,screen_name=screen_name).count()
        layout={}
        layout_arr=[]

        for header,field in zip(layout_header,layout_field):
            ex_layout_field=field.split(".")
            is_numeric_field=field.split("#")
            field_name=ex_layout_field[0]
            
            if len(is_numeric_field)>1:
                field_type=is_numeric_field[1]
                field_name=is_numeric_field[0]
            else:
                field_type=''   

            if len(ex_layout_field)>1:
                child_name=ex_layout_field[1]
                field_name=ex_layout_field[0]
            else:
                child_name=''            

            if(layout_check):
                layout_column_fetch=EngageboostGridColumnLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
                layout_column_header=layout_column_fetch.header_name
                layout_column_field=layout_column_fetch.field_name

                if header in layout_column_header:
                    status=1
                else:
                    status=0
            else:
                status=1        
            layout={"title":header,"field":field_name,"child":child_name,"show":status,"field_type":field_type}
            layout_arr.append(layout)
        #********* End Grid Headings *********#

        #********* Start Role Permission *********#
        users = EngageboostUsers.objects.using(company_db).filter(id=user_id).first()
        # issuperadmin = users.is_superadmin
        role_id = users.role_id
        role_permission={}
        if users.is_superadmin:
            add='Y'
            edit='Y'
            delete='Y'
            status='Y'
            role_permission={"add":"Y","edit":"Y","delete":"Y","view":"Y","block":"Y","import_field":0,"export":0,"shipping_processes":0,"print":0}
        else:
            role_per = EngageboostRoleMenuPermissions.objects.using(company_db).get(role_id=role_id,master_id=menu_id,isblocked=0,isdeleted=0)
            role_permission={"add":role_per.add,"edit":role_per.edit,"delete":role_per.delete,"view":role_per.view,"block":role_per.block,"import_field":role_per.import_field,"export":role_per.export,"shipping_processes":role_per.shipping_processes,"print":role_per.print}
            add=role_per.add
            edit=role_per.edit
            delete=role_per.delete
            status=role_per.block
        #********* End Role Permission *********#

        result_all = len(StockSummaryArr)
        StockSummaryArrActive = filter_deck(StockSummaryArr,isblocked="n")
        result1 = len(StockSummaryArrActive)
        StockSummaryArrDeactive = filter_deck(StockSummaryArr,isblocked="y")
        result2 = len(StockSummaryArrDeactive)

        pre_data={}
        results_arr=[]     
        pre_data['all']=result_all
        pre_data['inactive']=result2
        pre_data['active']=result1 
        pre_data['result']=StockSummaryArr
        pre_data['layout']=layout_arr
        pre_data['role_permission']=role_permission
        # results_arr.append(pre_data)

        product_data = self_pagination(pre_data)
        return Response(product_data)
        # return Response(str(stock)+' '+str(safetyStock)+' '+str(virtualStock)+' '+str(realStock))

class ViewProductPurchaseOrderDetails(generics.ListAPIView):
    def get(self, request, pid,user_id, format=None):
        company_db = loginview.db_active_connection(request)
        
        #********* Start Purchase Order **********#
        # ProductDetails = EngageboostProducts.objects.using(company_db).filter(id=pid).first()
        # if ProductDetails:
        PurchaseOrderProductsDetailsData = []
        PurchaseOrderProductsDetailsCond = EngageboostPurchaseOrderProducts.objects.using(company_db).filter(product_id=pid)
        if PurchaseOrderProductsDetailsCond:
            PurchaseOrderProductsDetails = PurchaseOrderProductSerializer(PurchaseOrderProductsDetailsCond,many=True)
            for PurchaseOrderProducts in PurchaseOrderProductsDetails.data:
                PurchaseOrdersCond = EngageboostPurchaseOrders.objects.using(company_db).filter(id=PurchaseOrderProducts['purchase_order_id']).first()
                if PurchaseOrdersCond:
                    PurchaseOrders = PurchaseOrderSerializer(PurchaseOrdersCond,partial=True)
                    purchase_ord_prd_order_date = PurchaseOrders.data['order_date'].split('T')
                    PurchaseOrders.data['order_date'] = covert_time(purchase_ord_prd_order_date[0],"UTC","Asia/Kolkata")
                    PurchaseOrderProducts["PurchaseOrder"]=PurchaseOrders.data

                    SuppliersDetailsCond = EngageboostSuppliers.objects.using(company_db).filter(id=PurchaseOrders.data['supplier_id']).first()
                    if SuppliersDetailsCond:
                        SuppliersDetails = SuppliersSerializer(SuppliersDetailsCond,partial=True)
                        PurchaseOrderProducts["supplier"] = SuppliersDetails.data

                    WarehouseDetailsCond = EngageboostWarehouseMasters.objects.using(company_db).filter(id=PurchaseOrders.data['warehouse_id']).first()
                    if WarehouseDetailsCond:
                        WarehouseDetails = WarehousemastersSerializer(WarehouseDetailsCond,partial=True)
                        PurchaseOrderProducts["warehouse"] = WarehouseDetails.data
            PurchaseOrderProductsDetailsData = PurchaseOrderProductsDetails.data
        #********* End Purchase Order **********#

        #********* Start Grid Headings *********#
        row_dict={}
        row=[]
        module='ProductStockSummary'
        screen_name='list-custom'
        layout_fetch=EngageboostGridLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
        layout_header=layout_fetch.header_name.split("@@")
        layout_field=layout_fetch.field_name.split("@@")
        layout_check=EngageboostGridColumnLayouts.objects.using(company_db).filter(module=module,screen_name=screen_name).count()
        layout={}
        layout_arr=[]

        for header,field in zip(layout_header,layout_field):
            ex_layout_field=field.split(".")
            is_numeric_field=field.split("#")
            field_name=ex_layout_field[0]
            
            if len(is_numeric_field)>1:
                field_type=is_numeric_field[1]
                field_name=is_numeric_field[0]
            else:
                field_type=''   

            if len(ex_layout_field)>1:
                child_name=ex_layout_field[1]
                field_name=ex_layout_field[0]
            else:
                child_name=''            

            if(layout_check):
                layout_column_fetch=EngageboostGridColumnLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
                layout_column_header=layout_column_fetch.header_name
                layout_column_field=layout_column_fetch.field_name

                if header in layout_column_header:
                    status=1
                else:
                    status=0
            else:
                status=1        
            layout={"title":header,"field":field_name,"child":child_name,"show":status,"field_type":field_type}
            layout_arr.append(layout)
        #********* End Grid Headings *********#

        #********* Start Role Permission *********#
        users = EngageboostUsers.objects.using(company_db).get(id=user_id)
        issuperadmin = users.issuperadmin
        role_id = users.role_id
        role_permission={}
        if issuperadmin=='Y':
            add='Y'
            edit='Y'
            delete='Y'
            status='Y'
            role_permission={"add":"Y","edit":"Y","delete":"Y","view":"Y","block":"Y","import_field":0,"export":0,"shipping_processes":0,"print":0}
        else:
            role_per = EngageboostRoleMenuPermissions.objects.using(company_db).get(role_id=role_id,master_id=menu_id,isblocked=0,isdeleted=0)
            role_permission={"add":role_per.add,"edit":role_per.edit,"delete":role_per.delete,"view":role_per.view,"block":role_per.block,"import_field":role_per.import_field,"export":role_per.export,"shipping_processes":role_per.shipping_processes,"print":role_per.print}
            add=role_per.add
            edit=role_per.edit
            delete=role_per.delete
            status=role_per.block
        #********* End Role Permission *********#

        # product_data={"product_purchase_order":PurchaseOrderProductsDetailsData}
        # return Response(product_data)

        result_all = len(PurchaseOrderProductsDetailsData)
        # PurchaseOrderProductsDetailsDataActive = filter_deck(PurchaseOrderProductsDetailsData,isblocked="n")
        # result1 = len(PurchaseOrderProductsDetailsDataActive)
        # PurchaseOrderProductsDetailsDataDeactive = filter_deck(PurchaseOrderProductsDetailsData,isblocked="y")
        # result2 = len(PurchaseOrderProductsDetailsDataDeactive)

        pre_data={}
        results_arr=[]     
        pre_data['all']=result_all
        # pre_data['inactive']=result2
        # pre_data['active']=result1 
        pre_data['result']=PurchaseOrderProductsDetailsData
        pre_data['layout']=layout_arr
        pre_data['role_permission']=role_permission
        # results_arr.append(pre_data)

        product_data = self_pagination(pre_data)
        return Response(product_data)

class ViewProductReceiptDetails(generics.ListAPIView):
    def get(self, request, pid, user_id, format=None):
        company_db = loginview.db_active_connection(request)

        #********* Start Receipt Section **********#
        # EngageboostPurchaseOrdersReceived
        ProductReceiptArray = []
        PurchaseOrderReceivedProductsCond = EngageboostPurchaseOrderReceivedProducts.objects.using(company_db).filter(product_id=pid)
        if PurchaseOrderReceivedProductsCond:
            PurchaseOrderReceivedProductsDetails = PurchaseOrderReceivedProductsSerializer(PurchaseOrderReceivedProductsCond,many=True)
            # return Response(PurchaseOrderReceivedProductsDetails.data)
            for PurchaseOrderReceivedProducts in PurchaseOrderReceivedProductsDetails.data:
                ProductReceiptDict = dict()
                ProductReceiptDict["PurchaseOrderReceivedProduct"] = PurchaseOrderReceivedProducts
                if PurchaseOrderReceivedProducts["purchase_order_received"]:
                    # return Response(PurchaseOrderReceivedProducts["purchase_order_received"]["purchase_order_master_id"])
                    ProductReceiptDict["PurchaseOrdersReceived"] = PurchaseOrderReceivedProducts["purchase_order_received"]
                    PurchaseOrdersCond = EngageboostPurchaseOrders.objects.using(company_db).filter(id=PurchaseOrderReceivedProducts["purchase_order_received"]["purchase_order_master_id"]).first()
                    if PurchaseOrdersCond:
                        PurchaseOrdersDetails = PurchaseOrderSerializer(PurchaseOrdersCond,partial=True)
                        ProductReceiptDict["PurchaseOrder"] = PurchaseOrdersDetails.data                            

                    SuppliersDetailsCond = EngageboostSuppliers.objects.using(company_db).filter(id=PurchaseOrderReceivedProducts['purchase_order_received']['supplier_id']).first()
                    if SuppliersDetailsCond:
                        SuppliersDetails = SuppliersSerializer(SuppliersDetailsCond,partial=True)
                        ProductReceiptDict["Supplier"] = SuppliersDetails.data

                    WarehouseDetailsCond = EngageboostWarehouseMasters.objects.using(company_db).filter(id=PurchaseOrderReceivedProducts['purchase_order_received']['warehouse_id']).first()
                    if WarehouseDetailsCond:
                        WarehouseDetails = WarehousemastersSerializer(WarehouseDetailsCond,partial=True)
                        ProductReceiptDict["Warehouse"] = WarehouseDetails.data

                    ProductMoveTrackCond = EngageboostProductMoveTrack.objects.using(company_db).filter(purchase_order_received_id=PurchaseOrderReceivedProducts['purchase_order_received']['id'])
                    if ProductMoveTrackCond:
                        ProductMoveTrackDetails = ProductMoveTrackSerializer(ProductMoveTrackCond,partial=True)
                        ProductReceiptDict["ProductMoveTrack"] = ProductMoveTrackDetails.data

                ProductReceiptArray.append(ProductReceiptDict)
        #********* End Receipt Section **********#

        product_data={"product_receipt_details":ProductReceiptArray}
        return Response(product_data)

class ViewProductOrderDetails(generics.ListAPIView):
    def get(self, request, pid, user_id, format=None):
        company_db = loginview.db_active_connection(request)

        #********* Start Product Order Section **********#
        ProductOrderArray = []
        OrderProductsCond = EngageboostOrderProducts.objects.using(company_db).filter(product_id=pid)
        if OrderProductsCond:
            OrderProductsDetails = OrderProductsSerializer(OrderProductsCond,many=True)
            for OrderProducts in OrderProductsDetails.data:
                ProductOrderDict = dict()
                ProductOrderDict["OrderProducts"] = OrderProducts
                # return Response(OrderProducts['order_id'])
                if OrderProducts["order_id"]:
                    OrdermasterCond = EngageboostOrdermaster.objects.using(company_db).filter(id=OrderProducts["order_id"]).first()
                    if OrdermasterCond:
                        OrdermasterDetails = OrderMasterSerializer(OrdermasterCond,partial=True)
                        # return Response(OrdermasterDetails.data)
                        ProductOrderDict["OrderList"] = OrdermasterDetails.data

                        ProductCond = EngageboostProducts.objects.using(company_db).filter(id=pid).first()
                        if ProductCond:
                            ProductDetails = BasicinfoSerializer(ProductCond,partial=True)
                            ProductOrderDict["Product"] = ProductDetails.data
                        else:
                            ProductOrderDict["Product"] = {}

                        CustomersCond = EngageboostCustomers.objects.using(company_db).filter(id=OrdermasterDetails.data["customer_id"]).first()
                        if CustomersCond:
                            CustomersDetails = CustomerSerializer(CustomersCond,partial=True)
                            ProductOrderDict["Customer"] = CustomersDetails.data
                        else:
                            ProductOrderDict["Customer"] = {}

                        ChannelsCond = EngageboostChannels.objects.using(company_db).filter(id=OrdermasterDetails.data["webshop_id"]).first()
                        if ChannelsCond:
                            ChannelsDetails = ChannelsSerializer(ChannelsCond,partial=True)
                            ProductOrderDict["Channels"] = ChannelsDetails.data
                        else:
                            ProductOrderDict["Channels"] = {}
                        
                    else:
                        ProductOrderDict["OrderList"] = {}
                else:
                    ProductOrderDict["OrderList"] = {}
                    ProductOrderDict["Product"] = {}
                    ProductOrderDict["Customer"] = {}
                    ProductOrderDict["Channels"] = {}

                ProductOrderArray.append(ProductOrderDict)
        #********* End Product Order Section **********#

        #********* Start Grid Headings *********#
        row_dict={}
        row=[]
        module='ProductStockSummary'
        screen_name='list-custom'
        layout_fetch=EngageboostGridLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
        layout_header=layout_fetch.header_name.split("@@")
        layout_field=layout_fetch.field_name.split("@@")
        layout_check=EngageboostGridColumnLayouts.objects.using(company_db).filter(module=module,screen_name=screen_name).count()
        layout={}
        layout_arr=[]

        for header,field in zip(layout_header,layout_field):
            ex_layout_field=field.split(".")
            is_numeric_field=field.split("#")
            field_name=ex_layout_field[0]
            
            if len(is_numeric_field)>1:
                field_type=is_numeric_field[1]
                field_name=is_numeric_field[0]
            else:
                field_type=''   

            if len(ex_layout_field)>1:
                child_name=ex_layout_field[1]
                field_name=ex_layout_field[0]
            else:
                child_name=''            

            if(layout_check):
                layout_column_fetch=EngageboostGridColumnLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
                layout_column_header=layout_column_fetch.header_name
                layout_column_field=layout_column_fetch.field_name

                if header in layout_column_header:
                    status=1
                else:
                    status=0
            else:
                status=1        
            layout={"title":header,"field":field_name,"child":child_name,"show":status,"field_type":field_type}
            layout_arr.append(layout)
        #********* End Grid Headings *********#

        #********* Start Role Permission *********#
        users = EngageboostUsers.objects.using(company_db).get(id=user_id)
        issuperadmin = users.issuperadmin
        role_id = users.role_id
        role_permission={}
        if issuperadmin=='Y':
            add='Y'
            edit='Y'
            delete='Y'
            status='Y'
            role_permission={"add":"Y","edit":"Y","delete":"Y","view":"Y","block":"Y","import_field":0,"export":0,"shipping_processes":0,"print":0}
        else:
            role_per = EngageboostRoleMenuPermissions.objects.using(company_db).get(role_id=role_id,master_id=menu_id,isblocked=0,isdeleted=0)
            role_permission={"add":role_per.add,"edit":role_per.edit,"delete":role_per.delete,"view":role_per.view,"block":role_per.block,"import_field":role_per.import_field,"export":role_per.export,"shipping_processes":role_per.shipping_processes,"print":role_per.print}
            add=role_per.add
            edit=role_per.edit
            delete=role_per.delete
            status=role_per.block
        #********* End Role Permission *********#

        # product_data={"product_order_details":ProductOrderArray}
        # return Response(product_data)

        result_all = len(ProductOrderArray)

        pre_data={}
        results_arr=[]     
        pre_data['all']=result_all
        pre_data['result']=ProductOrderArray
        pre_data['layout']=layout_arr
        pre_data['role_permission']=role_permission

        product_data = self_pagination(pre_data)
        return Response(product_data)

class ViewProductInvoiceDetails(generics.ListAPIView):
    def get(self, request, pid, user_id, format=None):
        company_db = loginview.db_active_connection(request)

        #********* Start Product Invoice Section **********#
        ProductInvoiceArray = []
        InvoiceProductsCond = EngageboostInvoiceProducts.objects.using(company_db).filter(product_id=pid)
        if InvoiceProductsCond:
            InvoiceProductsDetails = InvoiceproductSerializer(InvoiceProductsCond,many=True)
            for InvoiceProducts in InvoiceProductsDetails.data:
                ProductInvoiceDict = dict()
                ProductInvoiceDict["InvoiceProducts"] = InvoiceProducts

                InvoicemasterCond = EngageboostInvoicemaster.objects.using(company_db).filter(id=InvoiceProducts["invoice_id"]).first()
                if InvoicemasterCond:
                    InvoicemasterDetails = InvoicemasterSerializer(InvoicemasterCond,partial=True)
                    # return Response(OrdermasterDetails.data)
                    ProductInvoiceDict["Invoicemaster"] = InvoicemasterDetails.data

                    OrdermasterCond = EngageboostOrdermaster.objects.using(company_db).filter(id=InvoicemasterDetails.data["order_id"]).first()
                    if OrdermasterCond:
                        OrdermasterDetails = OrderMasterSerializer(OrdermasterCond,partial=True)
                        # return Response(OrdermasterDetails.data)
                        ProductInvoiceDict["OrderList"] = OrdermasterDetails.data
                    else:
                        ProductInvoiceDict["OrderList"] = {}

                    CustomersCond = EngageboostCustomers.objects.using(company_db).filter(id=InvoicemasterDetails.data["customer_id"]).first()
                    if CustomersCond:
                        CustomersDetails = CustomerSerializer(CustomersCond,partial=True)
                        ProductInvoiceDict["Customer"] = CustomersDetails.data
                    else:
                        ProductInvoiceDict["Customer"] = {}

                    ChannelsCond = EngageboostChannels.objects.using(company_db).filter(id=InvoicemasterDetails.data["webshop_id"]).first()
                    if ChannelsCond:
                        ChannelsDetails = ChannelsSerializer(ChannelsCond,partial=True)
                        ProductInvoiceDict["Channels"] = ChannelsDetails.data
                    else:
                        ProductInvoiceDict["Channels"] = {}
                else:
                    ProductInvoiceDict["Invoicemaster"] = {}
                    ProductInvoiceDict["OrderList"] = {}
                    ProductInvoiceDict["Customer"] = {}
                    ProductInvoiceDict["Channels"] = {}

                ProductInvoiceArray.append(ProductInvoiceDict)
        #********* End Product Invoice Section **********#

        #********* Start Grid Headings *********#
        row_dict={}
        row=[]
        module='ProductStockSummary'
        screen_name='list-custom'
        layout_fetch=EngageboostGridLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
        layout_header=layout_fetch.header_name.split("@@")
        layout_field=layout_fetch.field_name.split("@@")
        layout_check=EngageboostGridColumnLayouts.objects.using(company_db).filter(module=module,screen_name=screen_name).count()
        layout={}
        layout_arr=[]

        for header,field in zip(layout_header,layout_field):
            ex_layout_field=field.split(".")
            is_numeric_field=field.split("#")
            field_name=ex_layout_field[0]
            
            if len(is_numeric_field)>1:
                field_type=is_numeric_field[1]
                field_name=is_numeric_field[0]
            else:
                field_type=''   

            if len(ex_layout_field)>1:
                child_name=ex_layout_field[1]
                field_name=ex_layout_field[0]
            else:
                child_name=''            

            if(layout_check):
                layout_column_fetch=EngageboostGridColumnLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
                layout_column_header=layout_column_fetch.header_name
                layout_column_field=layout_column_fetch.field_name

                if header in layout_column_header:
                    status=1
                else:
                    status=0
            else:
                status=1        
            layout={"title":header,"field":field_name,"child":child_name,"show":status,"field_type":field_type}
            layout_arr.append(layout)
        #********* End Grid Headings *********#

        #********* Start Role Permission *********#
        users = EngageboostUsers.objects.using(company_db).get(id=user_id)
        issuperadmin = users.issuperadmin
        role_id = users.role_id
        role_permission={}
        if issuperadmin=='Y':
            add='Y'
            edit='Y'
            delete='Y'
            status='Y'
            role_permission={"add":"Y","edit":"Y","delete":"Y","view":"Y","block":"Y","import_field":0,"export":0,"shipping_processes":0,"print":0}
        else:
            role_per = EngageboostRoleMenuPermissions.objects.using(company_db).get(role_id=role_id,master_id=menu_id,isblocked=0,isdeleted=0)
            role_permission={"add":role_per.add,"edit":role_per.edit,"delete":role_per.delete,"view":role_per.view,"block":role_per.block,"import_field":role_per.import_field,"export":role_per.export,"shipping_processes":role_per.shipping_processes,"print":role_per.print}
            add=role_per.add
            edit=role_per.edit
            delete=role_per.delete
            status=role_per.block
        #********* End Role Permission *********#

        # product_data={"product_invoice_details":ProductInvoiceArray}
        # return Response(product_data)

        result_all = len(ProductInvoiceArray)

        pre_data={}
        results_arr=[]     
        pre_data['all']=result_all
        pre_data['result']=ProductInvoiceArray
        pre_data['layout']=layout_arr
        pre_data['role_permission']=role_permission
        product_data = self_pagination(pre_data)
        return Response(product_data)

class ViewProductAdjustmentDetails(generics.ListAPIView):
    def get(self, request, pid, user_id, format=None):
        company_db = loginview.db_active_connection(request)

        #********* Start Receipt Section **********#
        # EngageboostPurchaseOrdersReceived
        ProductAdjustmentArray = []
        PurchaseOrderReceivedProductsCond = EngageboostPurchaseOrderReceivedProducts.objects.using(company_db).filter(product_id=pid)
        if PurchaseOrderReceivedProductsCond:
            PurchaseOrderReceivedProductsDetails = PurchaseOrderReceivedProductsSerializer(PurchaseOrderReceivedProductsCond,many=True)
            # return Response(PurchaseOrderReceivedProductsDetails.data)
            for PurchaseOrderReceivedProducts in PurchaseOrderReceivedProductsDetails.data:
                ProductAdjustmentDict = dict()
                if PurchaseOrderReceivedProducts["purchase_order_received"]:
                    if PurchaseOrderReceivedProducts["purchase_order_received"]["action"] == 'Move' or PurchaseOrderReceivedProducts["purchase_order_received"]["action"] == 'move':
                        # return Response(PurchaseOrderReceivedProducts['purchase_order_received'])
                        ProductAdjustmentDict["PurchaseOrderReceivedProduct"] = PurchaseOrderReceivedProducts
                        ProductAdjustmentDict["PurchaseOrdersReceived"] = PurchaseOrderReceivedProducts["purchase_order_received"]

                        PurchaseOrdersCond = EngageboostPurchaseOrders.objects.using(company_db).filter(id=PurchaseOrderReceivedProducts["purchase_order_received"]["purchase_order_master_id"]).first()
                        if PurchaseOrdersCond:
                            PurchaseOrdersDetails = PurchaseOrderSerializer(PurchaseOrdersCond,partial=True)
                            ProductAdjustmentDict["PurchaseOrder"] = PurchaseOrdersDetails.data
                        else:
                            ProductAdjustmentDict["PurchaseOrder"] ={}                           

                        SuppliersDetailsCond = EngageboostSuppliers.objects.using(company_db).filter(id=PurchaseOrderReceivedProducts["purchase_order_received"]["supplier_id"]).first()
                        if SuppliersDetailsCond:
                            SuppliersDetails = SuppliersSerializer(SuppliersDetailsCond,partial=True)
                            ProductAdjustmentDict["Supplier"] = SuppliersDetails.data
                        else:
                            ProductAdjustmentDict["Supplier"] = {}    

                        WarehouseDetailsCond = EngageboostWarehouseMasters.objects.using(company_db).filter(id=PurchaseOrderReceivedProducts["purchase_order_received"]["warehouse_id"]).first()
                        if WarehouseDetailsCond:
                            WarehouseDetails = WarehousemastersSerializer(WarehouseDetailsCond,partial=True)
                            ProductAdjustmentDict["Warehouse"] = WarehouseDetails.data
                        else:
                            ProductAdjustmentDict["Warehouse"] = {}

                        ProductMoveTrackCond = EngageboostProductMoveTrack.objects.using(company_db).filter(purchase_order_received_id=PurchaseOrderReceivedProducts["purchase_order_received"]["id"])
                        if ProductMoveTrackCond:
                            ProductMoveTrackDetails = ProductMoveTrackSerializer(ProductMoveTrackCond,partial=True)
                            ProductAdjustmentDict["ProductMoveTrack"] = ProductMoveTrackDetails.data
                        else:
                            ProductAdjustmentDict["ProductMoveTrack"] = {}    
                    else:
                        ProductAdjustmentDict["PurchaseOrdersReceived"] = {}
                        ProductAdjustmentDict["PurchaseOrder"] ={}
                        ProductAdjustmentDict["Supplier"] = {}
                        ProductAdjustmentDict["Warehouse"] = {}
                        ProductAdjustmentDict["ProductMoveTrack"] = {}
                else:
                    ProductAdjustmentDict["PurchaseOrdersReceived"] = {}
                    ProductAdjustmentDict["PurchaseOrder"] ={}
                    ProductAdjustmentDict["Supplier"] = {}
                    ProductAdjustmentDict["Warehouse"] = {}
                    ProductAdjustmentDict["ProductMoveTrack"] = {}

                ProductAdjustmentArray.append(ProductAdjustmentDict)
        #********* End Receipt Section **********#

        product_data={"product_adjustment_details":ProductAdjustmentArray}
        return Response(product_data)


def covert_time(date,from_zone,target_zone):
    tz1 = pytz.timezone(from_zone)
    tz2 = pytz.timezone(target_zone)

    dt = datetime.datetime.strptime(str(date)+" 00:00:00.0","%Y-%m-%d %H:%M:%S.%f")
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime("%d-%m-%Y %H:%M:%S")
    return dt

def covert_date_with_timezone(date,from_zone,target_zone):
    tz1 = pytz.timezone(from_zone)
    tz2 = pytz.timezone(target_zone)

    dt = datetime.datetime.strptime(str(date),"%Y-%m-%d %H:%M:%S.%f")
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime("%d-%m-%Y %H:%M:%S")
    return dt

def get_time(gettime,zone,date):
    datetime = gettime.replace('T',' ')
    data_time=datetime.replace('Z',' ')
    a=data_time.split(".")
    b=a[0].replace(':',' ')
    c=b.replace('-',' ')
    date_format=c.split(" ")
    import datetime
    import time
    a1 = datetime.datetime(int(date_format[0]), int(date_format[1]), int(date_format[2]), int(date_format[3]), int(date_format[4]), int(date_format[5]))
    if zone.offset == 5.5:
        b1 = a1 + datetime.timedelta(hours=5,minutes=29) # days, seconds, then other fields.
        added_time=b1.time()
        ad_time=str(added_time).split(":")
    else:
        b1 = a1 + datetime.timedelta(hours=zone.offset) # days, seconds, then other fields.
        added_time=b1.time()
        ad_time=str(added_time).split(":")
        
    t = (int(date_format[0]), int(date_format[1]), int(date_format[2]), int(ad_time[0]), int(ad_time[1]), int(ad_time[2]),0,0,0)
    t = time.mktime(t)
    format1 =date.date_format
    datetime_object=time.strftime(format1+" %I:%M %p", time.gmtime(t))
    return datetime_object


def test_card(card, name, values):
    is_list = {'isblocked': False}
    if is_list[name]: # values is a list
        return any(value in card[name] for value in values)
    else:             # values is a single value
        return card[name] == values

def filter_deck(deck, **filters): # filters is a dict of keyword args
    r = []
    for d in deck:
        #print "Filtering", d, "on", filters
        if any(test_card(d, n, v) for n, v in filters.items()):
            r.append(d)
    return r

def get_page_size():
    settings = EngageboostGlobalSettings.objects.get(isdeleted='n',isblocked='n',website_id=1)
    size=settings.itemlisting_backend
    return size 

def self_pagination(array_list):
    results_arr=[]
    page_size = get_page_size()
    length_of_list = len(array_list['result'])
    results_arr.append(array_list)
    result = {"count":length_of_list,"per_page_count": math.ceil(length_of_list/page_size),"page_size":page_size,"results":results_arr}
    return result

class ImportFileProducts(generics.ListAPIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        datas = []
        db_fields = []
        product_path = 'products'
        module_id = 1
        temp_model = 'TempProduct'
        model = 'Product'
        filepath = 'importfile'

        post_data = request.data

        if 'import_file' in request.FILES:
            rand = str(random.randint(1,99999))
            file1 = request.FILES['import_file']
            file_name=file1.name
            ext = file_name.split('.')[-1]
            new_file_name='ProductImport_'+rand
            fs=FileSystemStorage()
            filename = fs.save(filepath+'/'+product_path+'/'+new_file_name+'.'+ext, file1)
            uploaded_file_url = fs.url(filename)
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            csvReader = xlrd.open_workbook(settings.BASE_DIR+uploaded_file_url)
            # sheet = csvReader.sheet_by_name('Sheet1')
            sheet = csvReader.sheet_by_index(0)
            # length=len(sheet.col_values(0))
            # for x in range(length):
            #     if(sheet.col_values(0)[x]=='Product Name'):
            #         pass
            #     else:
            #         pass
            headers = [str(cell.value) for cell in sheet.row(0)]
            headers = {k: k for k in headers}


        db_fields = get_db_fields(post_data['import_file_type'])

        for db_field in db_fields:
            has_record = EngageboostImportMapFields.objects.last()
            if has_record:
                last_entry_of_table = EngageboostImportMapFields.objects.order_by('-id').latest('id')
                row_id = int(last_entry_of_table.id)+int(1)
            else:
                row_id = 1

            savemaplist = EngageboostImportMapFields.objects.using(company_db).create(id=row_id,website_id=post_data['website_id'],module_id=module_id,file_field_name=db_field['field_label'],db_label_name=db_field['field_label'],db_field_name=db_field['model_field_value'],module_layout_field_id=db_field['id'],file_type='Excel',file_name=new_file_name+'.'+ext)
            if savemaplist:
                last_mapping_id = savemaplist.id
                datas.append(last_mapping_id)
            else:
                datas.append('failed')

        #********* List Of Parent Category *********#
        category_lists = []
        category_cond = EngageboostCategoryMasters.objects.using(company_db).all().filter(website_id=post_data['website_id'],parent_id=0,isblocked="n",isdeleted="n").values('id','name','parent_id','created','modified','website_id').order_by('name')
        if category_cond:
            category_list = CategoriesViewSerializer(category_cond,many=True)
            category_lists = category_list.data
        else:
            category_lists = []

        datas = {"category_list":category_lists,"filename":new_file_name+'.'+ext,"xls_header":headers,"db_fields":db_fields}
        return Response(datas)


def get_db_fields(model_name, primary_cat_id=0, import_type='Import'):
    website_id = 1
    module_list_id = ''
    new_db_fields = []
    new_db_field_filter = []
    new_custom_field = {}
    new_db_field = {}
    if model_name == 'Product' or model_name == 'product':
        module_id = 1
        module_details = EngageboostModuleLayouts.objects.filter(website_id=website_id,module_id=module_id).first()
        if module_details:
            module_list_id = module_details.id

        # if module_list_id:
        #     new_db_fields_cond = EngageboostDefaultModuleLayoutFields.objects.all().filter(module_list_id=module_list_id).values('field_label','model_field_value','field_id','id','module_layout_section_id')
        #     if new_db_fields_cond:
        #         new_db_fields = DefaultModuleLayoutFieldsSerializer(new_db_fields_cond,many=True)
        #         new_db_fields = new_db_fields.data                
        #     else:
        #         new_db_fields = []

        # "Image 1":"image_0","Image 2":"image_1","Image 3":"image_2","Image 4":"image_3","Image 5":"image_4",

        basic_field_map = {"Product Name":"name", "SKU":"sku", "PO Tax Class":"po_taxclass_id", "Gross Weight":"weight", "Sales Tax Class":"taxclass_id", "ASIN":"asin", "EAN/UPC":"ean", "ISBN":"isbn", "SUPC":"supc", "Expected Delivery Days(sla)":"sla", "Cost Per Unit":"cost_per_unit", "Features":"features", "Large Description":"description", "Shipping Class":"shippingclass_id", "Small Description":"mp_system_requirements", "Status":"status", "Parent SKU":"parent_product_id","Category 1":"category1","Category 2":"category2","Category 3":"category3","Category 4":"category4", "Supplier":"supplier_id", "Brand":"brand", "Features":"features", "META Page URL":"meta_url", "META Page Title":"metatitle", "META Keyword":"metatag", "META Description":"metadescription", "Price":"defaultprice", "Supc":"supc", "Expected Delivery Days":"sla", "AmazonIN Price":"amazonin_price", "AmazonUK Price":"amazonuk_price", "AmazonUs Price":"amazonus_price", "Ebayau Price":"ebayau_price", "Ebayin Price":"ebayin_price", "Ebayuk Price":"ebayuk_price", "Ebayusa Price":"ebayusa_price", "FlipKart Price":"flipkart_price", "Paytm Price":"paytm_price", "SnapDeal Price":"snapdeal_price", "Customer Group":"customer_group_id", "Unit Of Measurement":"uom", "AmazonIN SKU":"amazonin_sku", "AmazonUK SKU":"amazonuk_sku", "AmazonUs SKU":"amazonus_sku", "Ebayau SKU":"ebayau_sku", "Ebayin SKU":"ebayin_sku", "Ebayuk SKU":"ebayuk_sku", "Ebayusa SKU":"ebayusa_sku", "FlipKart SKU":"flipkart_sku", "Paytm SKU":"paytm_sku", "SnapDeal SKU":"snapdeal_sku", "NPN":"npn", "Max Order Unit":"max_order_unit", "HSN Code":"hsn_id", "Visible In Listing":"visible_in_listing", "Related Product SKU":"related_product_skus", "Image 1":"image_0","Image 2":"image_1","Image 3":"image_2","Image 4":"image_3","Image 5":"image_4","Barcode":"barcodes"} 

        # basic_field_map = {"Product Name":"name","SKU":"sku","Billing Category":"npn","Gross Weight":"weight","Sales Tax Class":"taxclass_id","ASIN":"asin","EAN/UPC":"ean","PLU Code":"isbn","Expected Delivery Days(sla)":"sla","Food Type":"veg_nonveg_type","Cost Per Unit":"cost_per_unit","Features":"features","Large Description":"description","Shipping Class":"shippingclass_id","Small Description":"mp_system_requirements","Status":"status","Parent SKU":"parent_product_id","Category 1":"category1","Category 2":"category2","Category 3":"category3","Category 4":"category4","Supplier":"supplier_id","Brand":"brand","Features":"features","META Page URL":"meta_url","META Page Title":"metatitle","META Keyword":"metatag","META Description":"metadescription","Price":"defaultprice","Image 1":"image_0","Image 2":"image_1","Image 3":"image_2","Image 4":"image_3","Image 5":"image_4","Customer Group" :"customer_group_id","Unit Of Measurement":"supc","Price Formula(Customer)":"price_formula_id_for_customer","Price Formula(Supplier)":"price_formula_id_for_supplier","Max Order Unit":"max_order_unit","Offer Description":"product_offer_desc","Offer Start Date":"product_offer_start_date","Offer End Date":"product_offer_end_date","Substitute Product 1": "Subt_1","Substitute Product 2": "Subt_2","Substitute Product 3": "Subt_3","Substitute Product 4": "Subt_4","Substitute Product 5": "Subt_5","HSN Code":"hsn_id","Promo":"is_promo","Promo Start Date":"promo_start_date","Promo End Date":"promo_end_date"} 
                
        for key,val in iter(basic_field_map.items()):
            extra_values =  {"field_label":key,"model_field_value":val}
            new_db_fields.append(extra_values)

        if primary_cat_id != 0:
            # module = EngageboostModules.objects.filter(module_name="category",status=1,model="category").first()
            # module_id = module.id
            # module_layouts_details = EngageboostModuleLayouts.objects.filter(website_id=website_id,module_id=module_id).first()
            # if module_layouts_details:
            #     layout_id = module_layouts_details.id

            # condtions_section = EngageboostDefaultModuleLayoutSections.objects.filter(module_list_id=layout_id,section_order_pos=2,module_id=module_id).first()
            # if condtions_section:
            #     section_id = condtions_section.id
           
            # new_db_fields_cond = EngageboostDefaultModuleLayoutFields.objects.all().filter(module_list_id=layout_id,module_id=module_id,module_layout_section_id=section_id,category_id=primary_cat_id).filter(~Q(field_label="Status")).values('field_label','model_field_value','field_id','id','module_layout_section_id')
            category_custom_field_cond = EngageboostDefaultModuleLayoutFields.objects.all().filter(category_id=primary_cat_id).filter(~Q(field_label="Status")).values('field_label','model_field_value','field_id','id','module_layout_section_id')
            if category_custom_field_cond:
                new_custom_db_fields = DefaultModuleLayoutFieldsSerializer(category_custom_field_cond,many=True)
                for category_custom_field in new_custom_db_fields.data:
                    if category_custom_field["field_label"]:
                        d11 ={"field_label":category_custom_field["field_label"]}; new_custom_field=dict(new_custom_field,**d11)
                    else:
                        d11 ={"field_label":""}; new_custom_field=dict(new_custom_field,**d11)

                    if category_custom_field["model_field_value"]:
                        d11 ={"model_field_value":category_custom_field["model_field_value"]}; new_custom_field=dict(new_custom_field,**d11)
                    elif category_custom_field["field_label"]:
                        d11 ={"model_field_value":category_custom_field["field_label"]}; new_custom_field=dict(new_custom_field,**d11)
                    else:
                        d11 ={"model_field_value":""}; new_custom_field=dict(new_custom_field,**d11)

                    try:
                        if category_custom_field["id"]: ids = category_custom_field["id"]
                        else: ids = None
                    except KeyError: ids = None
                    d11 ={"id":ids}; new_custom_field=dict(new_custom_field,**d11)

                    new_db_fields.append(new_custom_field)

                # new_custom_db_fields = DefaultModuleLayoutFieldsSerializer(category_custom_field_cond,many=True)
                # new_custom_db_fields = new_custom_db_fields.data
                # new_db_fields.append(new_custom_db_fields)
       
        # print(new_db_fields)
        for db_fields in new_db_fields:
            if db_fields["field_label"]:
                d1 ={"field_label":db_fields['field_label']}; new_db_field=dict(new_db_field,**d1)
            else:
                d1 ={"field_label":""}; new_db_field=dict(new_db_field,**d1)

            if db_fields["model_field_value"]:
                d1 ={"model_field_value":db_fields['model_field_value']}; new_db_field=dict(new_db_field,**d1)
            else:
                d1 ={"model_field_value":""}; new_db_field=dict(new_db_field,**d1)

            try:
                if db_fields['id']: ids = db_fields['id']
                else: ids = None
            except KeyError: ids = None

            d1 ={"id":ids}; new_db_field=dict(new_db_field,**d1)

            new_db_field_filter.append(new_db_field)

        return new_db_field_filter

class GetChildCategory(generics.ListAPIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        post_data = request.data
        module_id = 1
        datas = []
        category_lists = []
        category_cond = EngageboostCategoryMasters.objects.using(company_db).all().filter(website_id=post_data['website_id'],parent_id=post_data['category_id'],isblocked="n",isdeleted="n").values('id','name','parent_id','created','modified','website_id').order_by('name')
        if category_cond:
            # category_list = CategoriesSerializer(category_cond,many=True)
            category_list = CategoriesViewSerializer(category_cond,many=True)
            category_lists = category_list.data
        else:
            category_lists = []


        db_fields = get_db_fields("product",post_data['category_id'])

        for db_field in db_fields:
            findmaplist = EngageboostImportMapFields.objects.using(company_db).filter(website_id=post_data['website_id'],module_id=module_id,file_field_name=db_field['field_label'],file_type='Excel',file_name=post_data["filename"]).first()
            if findmaplist:
                savemaplist = EngageboostImportMapFields.objects.using(company_db).filter(website_id=post_data['website_id'],module_id=module_id,file_field_name=db_field['field_label'],file_type='Excel',file_name=post_data["filename"]).update(db_label_name=db_field['field_label'],db_field_name=db_field['model_field_value'],module_layout_field_id=db_field['id'])
            else:
                has_record = EngageboostImportMapFields.objects.last()
                if has_record:
                    last_entry_of_table = EngageboostImportMapFields.objects.order_by('-id').latest('id')
                    row_id = int(last_entry_of_table.id)+int(1)
                else:
                    row_id = 1

                savemaplist = EngageboostImportMapFields.objects.using(company_db).create(id=row_id,website_id=post_data['website_id'],module_id=module_id,file_field_name=db_field['field_label'],db_label_name=db_field['field_label'],db_field_name=db_field['model_field_value'],module_layout_field_id=db_field['id'],file_type='Excel',file_name=post_data["filename"])

            if savemaplist:
                last_mapping_id = savemaplist
                datas.append(last_mapping_id)
            else:
                datas.append('failed')

        datas = {"category_list":category_lists,"filename":post_data["filename"],"db_fields":db_fields}
        return Response(datas)


class SaveFileData(generics.ListAPIView):
    #-----Binayak Start-----#
    def post(self, request, format=None):
        product_path = 'products'
        module_id = 1
        temp_model = 'TempProduct'
        model = 'Product'
        filepath = 'importfile'
        datas = []
        custom_field_datas = []

        post_data = request.data
        # map_fields = ast.literal_eval(post_data['map_fields'])
        map_fields = eval(json.dumps(post_data["map_fields"]))
        # print('map_fields======>', map_fields)
        # deleteMapField = EngageboostImportMapFields.objects.filter(file_name=post_data["filename"],file_type='Excel').delete()
        if map_fields:
            for key, val in iter(map_fields.items()):
                # has_importmap_record = EngageboostImportMapFields.objects.last()
                # if has_importmap_record:
                #     last_importmap_entry_of_table = EngageboostImportMapFields.objects.order_by('-id').latest('id')
                #     importmap = int(last_importmap_entry_of_table.id)+int(1)
                # else:
                #     importmap = 1

                if val['id'] == 0:
                    # savemaplist = EngageboostImportMapFields.objects.filter(website_id=post_data['website_id'],module_id=module_id,file_field_name=key,file_type='Excel',file_name=post_data["filename"]).update(db_label_name=key,map_field_name=val['field_name'],module_layout_field_id=None)
                    savemaplist = EngageboostImportMapFields.objects.filter(website_id=post_data['website_id'],
                                                                            module_id=module_id,
                                                                            db_field_name=val['field_name'],
                                                                            file_type='Excel',
                                                                            file_name=post_data["filename"]).update(
                        file_field_name=key, map_field_name=val['field_name'], module_layout_field_id=None)
                else:
                    savemaplist = EngageboostImportMapFields.objects.filter(website_id=post_data['website_id'],
                                                                            module_id=module_id,
                                                                            db_field_name=val['field_name'],
                                                                            file_type='Excel',
                                                                            file_name=post_data["filename"]).update(
                        file_field_name=key, map_field_name=val['field_name'], module_layout_field_id=val['id'])

        # Read xls Data
        fs = FileSystemStorage()
        filename = filepath + '/' + product_path + '/' + post_data["filename"]
        uploaded_file_url = fs.url(filename)

        # if os.path.exists(uploaded_file_url):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csvReader = xlrd.open_workbook(settings.BASE_DIR + uploaded_file_url)

        sheet = csvReader.sheet_by_index(0)
        length = len(sheet.col_values(0))
        xls_column_header_info = []
        xls_column_info = {}
        row_no_in_xls = sheet.ncols
        # max_column = sheet.ncols
        for x in range(length):
            if x == 0:
                for i in range(row_no_in_xls):
                    # if sheet.col_values(i)[x]!="":
                    # print(sheet.col_values(i)[x])
                    d11 = {"column_name": sheet.col_values(i)[x], "column_number": i};
                    xls_column_info = dict(xls_column_info, **d11)
                    xls_column_header_info.append(xls_column_info)
                    # print('xls_column_header_info===>', xls_column_header_info)
            else:
                pass

        # return Response(xls_column_header_info)

        for x in range(length):
            if x == 0:
                pass
            else:
                has_record = EngageboostTempProducts.objects.last()
                if has_record:
                    last_entry_of_table = EngageboostTempProducts.objects.order_by('-id').latest('id')
                    row_id = int(last_entry_of_table.id) + int(1)
                else:
                    row_id = 1

                serializer_data = {}
                CF_serializer_data = {}
                custom_field_list = []

                # product_name        =sheet.col_values(0)[x] if sheet.col_values(0)[x] else None

                d1 = {"id": row_id, "website_id": post_data['website_id'], "file_name": post_data['filename']};
                serializer_data = dict(serializer_data, **d1)

                # -----Binayak Start 26-10-2020-----#
                flag = 0
                key_value = ''
                # -----Binayak End 26-10-2020-----#
                try:
                    if map_fields:
                        for key, val in iter(map_fields.items()):
                            # print(str(key))
                            for xls_column_header in xls_column_header_info:
                                if str(key) == str(xls_column_header["column_name"]):
                                    column_number = xls_column_header["column_number"]
                                    field_value = sheet.col_values(column_number)[x] if sheet.col_values(column_number)[
                                        x] else None
                                    # print(field_value)
                            # print(field_value)

                            # -----Binayak Start 26-10-2020-----#
                            if str(key) == 'SKU':
                                key_value = field_value


                            if str(key) == "Product Name" and field_value != '':
                                flag = 1
                            # -----Binayak End 26-10-2020-----#


                            if map_fields[key][
                                "field_name"] != "no" and key != "parent_category_selected" and key != "second_label_categorys" and key != "third_label_categorys" and key != "forth_label_categorys":
                                if map_fields[key][
                                    'id'] != 0:  # If map with any custom field
                                    CF_d1 = {"field_name": map_fields[key]['field_name'], "field_value": field_value}
                                    custom_field_list.append(CF_d1)
                                    # print('i am here')
                                else:
                                    # if map_fields[key]['field_name'] == "ean" or map_fields[key]['field_name'] == "asin" or map_fields[key]['field_name'] == "hsn_id":
                                    if type(field_value) == float:
                                        if int(field_value) == field_value and isinstance(field_value, float):
                                            field_value = int(round(field_value))
                                        else:
                                            field_value = field_value
                                    else:
                                        field_value = field_value

                                    d1 = {map_fields[key]['field_name']: field_value};
                                    serializer_data = dict(serializer_data, **d1)

                        # -----Binayak Start 26-10-2020-----#
                        if int(flag) == 0:
                            prod_sku = EngageboostProducts.objects.filter(sku=key_value, isblocked='n', isdeleted='n')
                            # print("prod_sku=======", prod_sku.query)
                            if prod_sku.count()>0:
                                prod_sku = prod_sku.first()

                                prod_sku_cat = EngageboostProductCategories.objects.filter(product_id=prod_sku.id)
                                # prod_cat = prod_sku_cat.category_id
                                # category = EngageboostCategoryMasters.objects.filter(id=prod_sku_cat.category_id)
                                if prod_sku_cat.count()>0:
                                    prod_sku_cat = prod_sku_cat.first()
                                    category_detail = EngageboostCategoryMasters.objects.filter(id=prod_sku_cat.category_id).values(
                                        'name').first()
                                    prod_cat = common.get_parent_cat(prod_sku_cat.category_id)
                                    if prod_cat['status'] != 0:
                                        d1 = {'category1': prod_cat['name']}
                                        # print("=====here 1======", d1)
                                    else:
                                        d1 = {'name': prod_sku.name, 'category1': category_detail['name']}
                                    serializer_data = dict(serializer_data, **d1)
                        # -----Binayak End 26-10-2020-----#

                        if int(flag) == 1 and post_data.get("with_category") != None:
                            prod_sku = EngageboostProducts.objects.filter(sku=key_value, isblocked='n', isdeleted='n')

                            if prod_sku.count():
                                prod_sku = prod_sku.first()

                                prod_sku_cat = EngageboostProductCategories.objects.filter(
                                    product_id=prod_sku.id)

                                # prod_cat = prod_sku_cat.category_id
                                # category = EngageboostCategoryMasters.objects.filter(id=prod_sku_cat.category_id)
                                if prod_sku_cat.count():
                                    prod_sku_cat = prod_sku_cat.first()

                                    category_detail = EngageboostCategoryMasters.objects.filter(
                                        id=prod_sku_cat.category_id).values(
                                        'name').first()

                                    prod_cat = common.get_parent_cat(prod_sku_cat.category_id)
                                    if prod_cat['status'] != 0:
                                        d1 = {'category1': prod_cat['name']}
                                        # print("=====here 2======", d1)
                                    else:
                                        d1 = {'category1': category_detail['name']}
                                    serializer_data = dict(serializer_data, **d1)
                        # print('serializer_data====>', serializer_data)
                except KeyError:
                    no = ""

                # try:
                #     if map_fields["Product Name"]["field_name"] != "no":
                #         if map_fields['Product Name']['id'] !=0:  #If map with any custom field
                #             CF_d1 = {"field_name":map_fields['Product Name']['field_name'],"field_value":product_name}
                #             custom_field_list.append(CF_d1)
                #         else: d1 = {map_fields['Product Name']['field_name']:product_name};serializer_data=dict(serializer_data,**d1)
                # except KeyError: no=""

                current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
                d1 = {"is_import": "y", "created": current_time, "modified": current_time};
                serializer_data = dict(serializer_data, **d1)

                # print(serializer_data)
                # serializer_data.update({'taxclass_id': EngageboostProductTaxClasses.objects.filter(name=serializer_data['taxclass_id']).last()})
                if 'taxclass_id' in serializer_data.keys():
                    taxclass_id = EngageboostProductTaxClasses.objects.filter(
                        name=serializer_data['taxclass_id']).last()
                    # serializer_data.pop('taxclass_id')
                # print("======================",serializer_data,"==========================")
                # return Response(serializer_data)
                if 'name' in serializer_data:
                    save_temp_product = EngageboostTempProducts.objects.create(**serializer_data)
                else:
                    save_temp_product = False

                # print("save_temp_product=========", save_temp_product)

                # save_temp_product = EngageboostTempProducts.objects.create(**serializer_data)
                if save_temp_product:
                    last_saved_id = save_temp_product.id
                    if last_saved_id:
                        for custom_fields in custom_field_list:
                            has_c_record = EngageboostTempProductCustomFields.objects.last()
                            if has_c_record:
                                last_customfield_entry_of_table = EngageboostTempProductCustomFields.objects.order_by(
                                    '-id').latest('id')
                                row_id = int(last_customfield_entry_of_table.id) + int(1)
                            else:
                                row_id = 1

                            SaveEngageboostTempProductCustomFields = EngageboostTempProductCustomFields.objects.create(
                                id=row_id, product_id=last_saved_id, field_name=custom_fields["field_name"],
                                field_value=custom_fields["field_value"])
                            if SaveEngageboostTempProductCustomFields:
                                TempProduct_CustomFields_id = SaveEngageboostTempProductCustomFields.id
                            custom_field_datas.append(TempProduct_CustomFields_id)
                else:
                    datas.append('failed')

        if datas:
            data_status = {"status": 1, "filename": post_data["filename"], "custom_field_data": custom_field_datas}
        else:
            data_status = {"status": 0, "filename": post_data["filename"], "custom_field_data": custom_field_datas}

        try:
            if post_data["category_id"]:
                data_status.update({"category_id": post_data["category_id"]})
        except:
            pass

        try:
            if post_data["with_category"]:
                data_status.update({"with_category": post_data["with_category"]})
        except:
            pass

        os.remove(settings.BASE_DIR + uploaded_file_url)

        return Response(data_status)
    #-----Binayak End-----#
    

class PreviewSaveFileData(generics.ListAPIView):
    #-----Binayak Start-----#
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        post_data = request.data
        fetch_all_data = []
        data = {}

        if post_data["model"] == "product":
            fetch_all_data_cond = EngageboostTempProducts.objects.all().filter(website_id=post_data['website_id'],
                                                                               file_name=post_data[
                                                                                   'filename'])  # fetch from temp product table

            if fetch_all_data_cond:
                fetch_all_datas = TempProductsSerializer(fetch_all_data_cond, many=True)
                # fetch_all_data = fetch_all_datas.data
                for fad in fetch_all_datas.data:
                    error = []
                    special_char = 'no'

                    skucount = EngageboostProducts.objects.filter(website_id=post_data['website_id'], sku=fad["sku"],
                                                                  isdeleted="n")

                    if not fad["name"]:
                        error.append("Product name is required for product import")

                    if not fad["sku"]:
                        error.append("Product SKU is required for product import")

                    # try:
                    #     if post_data["with_category"]:
                    #         # data_status.update({"with_category":post_data["with_category"]})
                    #         data.update({"with_category":post_data["with_category"]})
                    # except:
                    #     pass

                    try:
                        if post_data["with_category"] != "" and post_data["with_category"] != None and post_data[
                            "with_category"] == 1:
                            if not fad["category1"]:
                                error.append("Product Category should not be blank")
                            else:
                                hascategory = EngageboostCategoryMasters.objects.filter(
                                    website_id=post_data['website_id'], name=fad["category1"], isdeleted='n',
                                    isblocked='n')
                                if not hascategory:
                                    error.append("Product Category does not exists")
                    except:
                        pass

                    # if fad["sku"]==fad["parent_product_id"]:
                    #     error.append("Product SKU and parent product must not be same")

                    # if skucount.count()>0:
                    #     error.append("Product SKU already exists")

                    # if not fad["defaultprice"]:
                    #     error.append("Product price shouldn't be blank")

                    # if fad["asin"]:
                    #     if type(fad["asin"]) == float:
                    #         error.append("ASIN number shouldn't be decimal number")

                    # if fad["ean"]:
                    #     if type(fad["ean"]) == float:
                    #         error.append("EAN number shouldn't be decimal number")

                    # if fad["hsn_id"]:
                    #     if re.findall("[^a-zA-Z0-9]+",str(fad["hsn_id"])):
                    #         error.append("No special character or decimal number or space allowed in HSN code")

                    # if re.match('[\d./-]+$',str(fad["defaultprice"])):
                    #     special_char="no"
                    # else:
                    #     special_char="yes"

                    # if special_char=="yes":
                    #     error.append("No special character allowed in product price")

                    if error:
                        fad["error"] = 1
                        fad["error_message"] = error
                    else:
                        error.append("SUCCESS")
                        fad["error"] = 0
                        fad["error_message"] = error

                    fetch_custom_field_cond = EngageboostTempProductCustomFields.objects.all().filter(
                        product_id=fad["id"])  # fetch temp custom fields
                    if fetch_custom_field_cond:
                        fetch_custom_field_datas = TempProductCustomFieldsSerializer(fetch_custom_field_cond, many=True)
                        for custom_fields in fetch_custom_field_datas.data:
                            fad[custom_fields["field_name"]] = custom_fields["field_value"]

                fetch_all_data = fetch_all_datas.data

            data = {"preview_data": fetch_all_data, "filename": post_data['filename']}
            try:
                if post_data["category_id"]:
                    data.update({"category_id": post_data["category_id"]})
            except:
                pass

            try:
                if post_data["with_category"]:
                    # data_status.update({"with_category":post_data["with_category"]})
                    data.update({"with_category": post_data["with_category"]})
            except:
                pass
        return Response(data)

class SaveAllImportedDataOld(generics.ListAPIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        product_path = 'products'
        module_id = 1
        temp_model = 'TempProduct'
        model = 'Product'
        datas = []
        fetch_temp_datas = []
        map_field_dict="";map_field_array=[]
        post_data = request.data
        request_ip = get_client_ip(request)

        product_ids = []

        responseDatas = {}

        map_field_list_cond = EngageboostImportMapFields.objects.using(company_db).all().filter(website_id=post_data['website_id'],module_id=module_id,file_type='Excel',file_name=post_data["filename"],module_layout_field_id=None).filter(~Q(map_field_name=None))

        map_field_list = ImportMapFieldsSerializer(map_field_list_cond,many=True)
        # return Response(map_field_list.data)
        # for map_fields in map_field_list.data:
        #     if map_fields["map_field_name"] is not None:
        #         map_field_dict = {map_fields["file_field_name"]:map_fields}
        #         map_field_array.append(dict(map_field_dict))


        selectedIds = post_data["selected_ids"].split(',')

        for i in selectedIds:
            fetch_temp_data_cond = EngageboostTempProducts.objects.using(company_db).filter(id=int(i)).first()
            if fetch_temp_data_cond:
                fetch_temp_data = TempProductsSerializer(fetch_temp_data_cond,partial=True)
                fetch_temp_datas.append(fetch_temp_data.data)

        for fetchtempdatas in fetch_temp_datas:
            serializer_data = {}
            tmp_image = {}
            tmp_image1 = []

            secondary_category = {}
            secondary_category1 = []
            # print(map_field_list.data,fetchtempdatas)
            for map_fields in map_field_list.data:
                d1 = {}
                if map_fields["map_field_name"] != "taxclass_id" and map_fields["map_field_name"] != "supplier_id" and map_fields["map_field_name"] != "hsn_id" and map_fields["map_field_name"] != "customer_group_id" and map_fields["map_field_name"] != "customer_group_id" and map_fields["map_field_name"] != "brand":
                    if map_fields["map_field_name"] == "defaultprice":
                        d1={"default_price":fetchtempdatas[map_fields['map_field_name']] if fetchtempdatas[map_fields['map_field_name']] else 0}
                    elif map_fields["map_field_name"] == "ean" or map_fields["map_field_name"] == "asin":
                        if type(fetchtempdatas[map_fields['map_field_name']]) == float:
                            fetchtempdatas[map_fields['map_field_name']]=int(round(fetchtempdatas[map_fields['map_field_name']]))
                        else:
                            fetchtempdatas[map_fields['map_field_name']]=fetchtempdatas[map_fields['map_field_name']]

                        d1={map_fields["map_field_name"]:fetchtempdatas[map_fields['map_field_name']] if fetchtempdatas[map_fields['map_field_name']] else None}
                    elif map_fields["map_field_name"] == "image_0" or map_fields["map_field_name"] == "image_1" or map_fields["map_field_name"] == "image_2" or map_fields["map_field_name"] == "image_3" or map_fields["map_field_name"] == "image_4":
                        # print("Field Name================",map_fields["map_field_name"])
                        # print("Field Value================",fetchtempdatas[map_fields["map_field_name"]])
                        is_cover = 1 if map_fields["map_field_name"] == "image_0" else None
                        tmp_image={"img":fetchtempdatas[map_fields["map_field_name"]] if fetchtempdatas[map_fields["map_field_name"]] else 0,"is_cover":is_cover}
                        # print("Tmp Image================",tmp_image)
                        tmp_image1.append(tmp_image)

                    elif map_fields["map_field_name"] == "category1" or map_fields["map_field_name"] == "category2" or map_fields["map_field_name"] == "category3" or map_fields["map_field_name"] == "category4":
                        # print("Field Name================",map_fields["map_field_name"])
                        # print("Field Value================",fetchtempdatas[map_fields["map_field_name"]])
                        findcat = EngageboostCategoryMasters.objects.filter(name__iexact=fetchtempdatas[map_fields["map_field_name"]],isdeleted='n')
                        if findcat.count()>0:
                            findcat = findcat.first()
                            secondary_category={"is_parent":"n","category_id":findcat.id}
                            # print("Tmp Image================",tmp_image)
                            secondary_category1.append(secondary_category)

                    else:                        
                        d1={map_fields["map_field_name"]:fetchtempdatas[map_fields['map_field_name']] if fetchtempdatas[map_fields['map_field_name']] else None}
                    serializer_data = dict(serializer_data,**d1)
                    # defaultprice = fetchtempdatas["defaultprice"] if fetchtempdatas["defaultprice"] else 0
                    # max_order_unit = fetchtempdatas["max_order_unit"] if fetchtempdatas["max_order_unit"] else None
                    # status = fetchtempdatas["status"] if fetchtempdatas["status"] else None
                    # description = fetchtempdatas["description"] if fetchtempdatas["description"] else None
                    # small_description = fetchtempdatas["mp_system_requirements"] if fetchtempdatas["mp_system_requirements"] else None
                    # features = fetchtempdatas["features"] if fetchtempdatas["features"] else None
                    # asin = fetchtempdatas["asin"] if fetchtempdatas["asin"] else None
                    # ean = fetchtempdatas["ean"] if fetchtempdatas["ean"] else None
                else:
                    if map_fields["map_field_name"] == "taxclass_id":
                        if fetchtempdatas["taxclass_id"]:
                            tax_class_id = get_tax_class_id(fetchtempdatas["taxclass_id"],fetchtempdatas["website_id"])
                        else:
                            tax_class_id = 0
                        d1={"taxclass_id":tax_class_id};serializer_data = dict(serializer_data,**d1)

                    elif map_fields["map_field_name"] == "supplier_id":
                        if fetchtempdatas["supplier_id"]:
                            supplier_id = get_supplier_id(fetchtempdatas["supplier_id"],fetchtempdatas["website_id"])
                        else:
                            supplier_id = 0
                        d1={"supplier_id":supplier_id};serializer_data = dict(serializer_data,**d1)
                    elif map_fields["map_field_name"] == "hsn_id":
                        if type(fetchtempdatas["hsn_id"]) == float:
                            fetchtempdatas["hsn_id"]=int(round(fetchtempdatas["hsn_id"]))
                        else:
                            fetchtempdatas["hsn_id"]=fetchtempdatas["hsn_id"]

                        if fetchtempdatas["hsn_id"]:
                            hsn_id = get_hsn_id(fetchtempdatas["hsn_id"],fetchtempdatas["website_id"])
                        else:
                            hsn_id = None
                        d1={"hsn_id":hsn_id};serializer_data = dict(serializer_data,**d1)
                    elif map_fields["map_field_name"] == "customer_group_id":
                        if fetchtempdatas["customer_group_id"]:
                            customer_group_id = get_customer_group_id(fetchtempdatas["customer_group_id"],fetchtempdatas["website_id"])
                        else:
                            customer_group_id = 0
                        d1={"customer_group_id":customer_group_id};serializer_data = dict(serializer_data,**d1)
                    elif map_fields["map_field_name"] == "brand":
                        if fetchtempdatas["brand"]:
                            brand_id = get_brand_id(fetchtempdatas["brand"],fetchtempdatas["website_id"])
                        else:
                            brand_id = 0
                        d1={"brand":brand_id};serializer_data = dict(serializer_data,**d1)



            main_product_sku = None
            find_parent_sku = None
            main_product_sku = checksku_no(fetchtempdatas["website_id"],fetchtempdatas["sku"])
            parent_product_id = fetchtempdatas["parent_product_id"]
            # if parent_product_id:

            if not parent_product_id:
                visibility_id = 1
            else:
                if parent_product_id==fetchtempdatas["sku"]:
                    visibility_id = 1
                else:
                    find_parent_sku = checksku_no(fetchtempdatas["website_id"],parent_product_id)
                    if find_parent_sku!=0:
                        visibility_id = 4
                    else:
                        visibility_id = 1

            # d1 = {"website_id":fetchtempdatas["website_id"],"name":fetchtempdatas["name"],"sku":fetchtempdatas["sku"],"weight":weight,"tax_class_id":tax_class_id,"supplier_id":supplier_id,"customer_group_id":customer_group_id,"defaultprice":defaultprice,"hsn_id":hsn_id,"max_order_unit":max_order_unit,"status":status,"description":description,"mp_system_requirements":small_description,"features":features,"asin":asin,"ean":ean,"brand":brand_id,"main_product_sku":main_product_sku,"find_parent_sku":find_parent_sku}

            # print("================================",tmp_image1)
            current_time = datetime.datetime.now(datetime.timezone.utc).date()
            d1 = {"website_id":fetchtempdatas["website_id"],"main_product_sku":main_product_sku,"find_parent_sku":find_parent_sku,"visibility_id":visibility_id,"created":current_time,"modified":current_time}

            serializer_data = dict(serializer_data,**d1)

            datas.append(serializer_data)
            tmp_image.update({"website_id":fetchtempdatas["website_id"]})
            if "uom" in fetchtempdatas:
                created_uom_id = create_or_update_uom(fetchtempdatas["uom"],fetchtempdatas["website_id"],request_ip)
                uom_id = {"uom":created_uom_id}
                serializer_data = dict(serializer_data,**uom_id)

            hasproduct = EngageboostProducts.objects.using(company_db).filter(sku=fetchtempdatas["sku"],isdeleted='n').first()

            if hasproduct:
                try:
                    product_slug = common.create_product_slug(fetchtempdatas["name"],hasproduct.id)
                    product_slug = unidecode.unidecode(product_slug).lower()
                    product_slug = re.sub(r'\W+', '-', product_slug)
                    product_slug = slugify(product_slug)

                    method    = request.scheme
                    current_url = request.META['HTTP_HOST']
                    url=method+'://'+current_url+'/product/'+product_slug

                    # if not hasproduct.url:
                    #     d1 = {"url":url};serializer_data = dict(serializer_data,**d1)
                    # if not hasproduct.slug:
                    #     d1 = {"slug":product_slug};serializer_data = dict(serializer_data,**d1)
                    d1 = {"url":url,"slug":product_slug};serializer_data = dict(serializer_data,**d1)
                except:
                    pass
                existingproduct = EngageboostProducts.objects.using(company_db).get(id=hasproduct.id)
                serializer = BasicinfoSerializer(existingproduct, data=serializer_data,partial=True)
                new_product_entry = "no"
            else:
                product_slug = common.create_product_slug(fetchtempdatas["name"])
                product_slug = unidecode.unidecode(product_slug).lower()
                product_slug = re.sub(r'\W+', '-', product_slug)
                product_slug = slugify(product_slug)

                method    = request.scheme
                current_url = request.META['HTTP_HOST']
                url=method+'://'+current_url+'/product/'+product_slug

                d1 = {"url":url,"slug":product_slug};serializer_data = dict(serializer_data,**d1)

                serializer = BasicinfoSerializer(data=serializer_data,partial=True)
                new_product_entry = "yes"

            if serializer.is_valid():
                serializer.save()

                try:
                    if serializer_data['barcodes']:
                        barcodes = str(serializer_data['barcodes'])
                        barcodes = barcodes.split(',')
                        if len(barcodes)>0:
                            EngageboostMultipleBarcodes.objects.filter(product_id=serializer.data['id']).delete()
                            for i in barcodes:
                                exists = EngageboostMultipleBarcodes.objects.filter(barcode=i,isdeleted="n",isblocked='n')
                                if exists.count()==0:
                                    bar_data = {
                                        'product_id':serializer.data['id'],
                                        'barcode':i,
                                        'website_id':serializer.data['website_id'],
                                        'created':current_time,
                                        'modified':current_time

                                    }
                                    EngageboostMultipleBarcodes.objects.create(**bar_data)
                except:
                    pass


                tmp_image.update({"product":serializer.data['id']})
                custom_field_value = EngageboostTempProductCustomFields.objects.using(company_db).all().filter(product_id=fetchtempdatas["id"])
                if custom_field_value:
                    saved_custom_value_list = save_import_product_custom_fields_value(fetchtempdatas["website_id"],fetchtempdatas["id"],serializer.data['id'],module_id,post_data["filename"],custom_field_value)


                serializer_product_category={}
                dict_prod_cat = {}
                current_time = datetime.datetime.now(datetime.timezone.utc).date()
                # product_category_obj = ProductCategoriesSerializer(product_id=serializer.data['id'],category_id=post_data["category_id"])
                #-----Binayak Start-----#
                if "category_id" in post_data:
                    if post_data['category_id'] is not None and int(post_data['category_id'])>0:
                        dict_prod_cat = {"product_id":serializer.data['id'],"category_id":post_data['category_id'],"is_parent":'y',"created":current_time,"modified":current_time};
                #-----Binayak End------#
                serializer_product_category=dict(serializer_product_category,**dict_prod_cat)
                serializer2 = ProductCategoriesSerializer(data=serializer_product_category,partial=True)

                if serializer2.is_valid():
                    # -----Binayak Start 26-10-2020-----#
                    # EngageboostProductCategories.objects.using(company_db).filter(product_id=serializer.data['id']).delete() # Delete previous product category
                    # -----Binayak End 26-10-2020-----#
                    # serializer2.save()

                    has_record = EngageboostProductCategories.objects.last()
                    if has_record:
                        last_entry_of_table = EngageboostProductCategories.objects.order_by('-id').latest('id')
                        row_id = int(last_entry_of_table.id)+int(1)
                    else:
                        row_id = 1
                    dict_prod_cat = {"id":row_id};serializer_product_category=dict(serializer_product_category,**dict_prod_cat)

                    serializer2 = EngageboostProductCategories.objects.using(company_db).create(**serializer_product_category)
                    if serializer2:
                        last_prod_cat_id = serializer2.id
                    else:
                        last_prod_cat_id = 0
                    data ={'status':1,'api_status':last_prod_cat_id,'message':'Product Category Updated Successfully'}
                    datas.append(data)
                else:
                    data ={'status':0,'api_status':serializer2.errors,'message':'Error Occured in Product Category'}
                    datas.append(data)

                if visibility_id == 4:
                    serializer_cross_sell_product={}
                    dict_cross_sell = {"cross_product_id":serializer.data['id'],"product_id":find_parent_sku};serializer_cross_sell_product=dict(serializer_cross_sell_product,**dict_cross_sell)

                    serializer3 = CossSellProductsSerializer(data=serializer_cross_sell_product,partial=True)

                    if serializer3.is_valid():
                        EngageboostCossSellProducts.objects.using(company_db).filter(cross_product_id=serializer.data['id']).delete()
                        # serializer3.save()
                        cross_obj = EngageboostCossSellProducts.objects.using(company_db).create(**dict_cross_sell)
                        data ={'status':1,'api_status':cross_obj.id,'message':'Product Variant Updated Successfully'}
                        datas.append(data)
                    else:
                        data ={'status':0,'api_status':serializer3.errors,'message':'Error Occured in Product Variant'}
                        datas.append(data)


                if new_product_entry == "yes":
                    save_product_inventory_with_zero_quantity(serializer.data['id'])

                # print(tmp_image)
                if len(tmp_image1)>0:
                    for tmp_item in tmp_image1:
                        if tmp_item['is_cover']==1:
                            EngageboostTempProductimages.objects.using(company_db).filter(product=serializer.data['id'],is_cover=1).update(is_cover=0)
                        tmp_item.update({"created":current_time, "modified":current_time,"product":serializer.data['id'],"website_id":serializer.data['website_id']})
                        EngageboostTempProductimages.objects.using(company_db).create(**tmp_item)
                        # print("Image to temp============")

                if len(secondary_category1)>0:
                    common.update_db_sequences("product_categories")
                    for secondary_category in secondary_category1:

                        secondary_category.update({"created":current_time, "modified":current_time,"product_id":serializer.data['id']})
                        print("Category Mapp=====================",secondary_category)
                        EngageboostProductCategories.objects.using(company_db).create(**secondary_category)

                # elastic = common.save_data_to_elastic(serializer.data['id'],'EngageboostProducts')

                product_ids.append(serializer.data['id'])

                responseDatas = {"status":1,"api_response":datas,"message":'Product Saved'}
            else:
                data ={'status':0,'api_status':serializer.errors,'message':'Error Occured'}
                datas.append(data)

                responseDatas = {"status":0,"api_response":datas,"message":'Error Occured in Product'}

        common.products_to_elastic(product_ids)

        EngageboostImportMapFields.objects.using(company_db).delete()
        # EngageboostTempProducts.objects.using(company_db).delete()
        EngageboostTempProductCustomFields.objects.using(company_db).delete()
        return Response(responseDatas)


class SaveAllImportedData(generics.ListAPIView):
    # permission_classes = []

    def post(self, request, format=None):
        post_data = request.data
        company_db = loginview.db_active_connection(request)
        request_ip = get_client_ip(request)
        save_all_imported_data(post_data, company_db, request_ip, request)
        datas= []
        data = {'status': 1, 'api_status': 1, 'message': 'Product Category Updated Successfully'}
        datas.append(data)
        responseDatas = {"status": 1, "api_response": datas, "message": 'Request is under process'}
        return Response(responseDatas)

@postpone
def save_all_imported_data(post_data, company_db, request_ip, request):

    product_path = 'products'
    module_id = 1
    temp_model = 'TempProduct'
    model = 'Product'
    datas = []
    fetch_temp_datas = []
    map_field_dict = "";
    map_field_array = []
    post_data = post_data
    request_ip = request_ip

    # ------Binayak Start 19-03-2021------#
    product_ids = []
    # ------Binayak End 19-03-2021------#

    responseDatas = {}

    map_field_list_cond = EngageboostImportMapFields.objects.using(company_db).all().filter(
        website_id=post_data['website_id'], module_id=module_id, file_type='Excel', file_name=post_data["filename"],
        module_layout_field_id=None).filter(~Q(map_field_name=None))

    map_field_list = ImportMapFieldsSerializer(map_field_list_cond, many=True)
    # return Response(map_field_list.data)
    # for map_fields in map_field_list.data:
    #     if map_fields["map_field_name"] is not None:
    #         map_field_dict = {map_fields["file_field_name"]:map_fields}
    #         map_field_array.append(dict(map_field_dict))

    selectedIds = post_data["selected_ids"].split(',')

    for i in selectedIds:
        fetch_temp_data_cond = EngageboostTempProducts.objects.using(company_db).filter(id=int(i)).first()
        if fetch_temp_data_cond:
            fetch_temp_data = TempProductsSerializer(fetch_temp_data_cond, partial=True)
            fetch_temp_datas.append(fetch_temp_data.data)

    for fetchtempdatas in fetch_temp_datas:
        serializer_data = {}
        tmp_image = {}
        tmp_image1 = []

        secondary_category = {}
        secondary_category1 = []
        # print(map_field_list.data,fetchtempdatas)
        for map_fields in map_field_list.data:
            d1 = {}
            if map_fields["map_field_name"] != "taxclass_id" and map_fields["map_field_name"] != "supplier_id" and \
                    map_fields["map_field_name"] != "hsn_id" and map_fields["map_field_name"] != "customer_group_id" and \
                    map_fields["map_field_name"] != "customer_group_id" and map_fields["map_field_name"] != "brand":
                if map_fields["map_field_name"] == "defaultprice":
                    d1 = {"default_price": fetchtempdatas[map_fields['map_field_name']] if fetchtempdatas[
                        map_fields['map_field_name']] else 0}
                elif map_fields["map_field_name"] == "ean" or map_fields["map_field_name"] == "asin":
                    if type(fetchtempdatas[map_fields['map_field_name']]) == float:
                        fetchtempdatas[map_fields['map_field_name']] = int(
                            round(fetchtempdatas[map_fields['map_field_name']]))
                    else:
                        fetchtempdatas[map_fields['map_field_name']] = fetchtempdatas[map_fields['map_field_name']]

                    d1 = {map_fields["map_field_name"]: fetchtempdatas[map_fields['map_field_name']] if fetchtempdatas[
                        map_fields['map_field_name']] else None}
                elif map_fields["map_field_name"] == "image_0" or map_fields["map_field_name"] == "image_1" or \
                        map_fields["map_field_name"] == "image_2" or map_fields["map_field_name"] == "image_3" or \
                        map_fields["map_field_name"] == "image_4":
                    # print("Field Name================",map_fields["map_field_name"])
                    # print("Field Value================",fetchtempdatas[map_fields["map_field_name"]])
                    is_cover = 1 if map_fields["map_field_name"] == "image_0" else None
                    tmp_image = {"img": fetchtempdatas[map_fields["map_field_name"]] if fetchtempdatas[
                        map_fields["map_field_name"]] else 0, "is_cover": is_cover}
                    # print("Tmp Image================",tmp_image)
                    tmp_image1.append(tmp_image)

                elif map_fields["map_field_name"] == "category1" or map_fields["map_field_name"] == "category2" or \
                        map_fields["map_field_name"] == "category3" or map_fields["map_field_name"] == "category4":
                    # print("Field Name================",map_fields["map_field_name"])
                    # print("Field Value================",fetchtempdatas[map_fields["map_field_name"]])
                    findcat = EngageboostCategoryMasters.objects.filter(
                        name__iexact=fetchtempdatas[map_fields["map_field_name"]], isdeleted='n')
                    if findcat.count() > 0:
                        findcat = findcat.first()
                        secondary_category = {"is_parent": "n", "category_id": findcat.id}
                        # print("Tmp Image================",tmp_image)
                        secondary_category1.append(secondary_category)

                else:
                    d1 = {map_fields["map_field_name"]: fetchtempdatas[map_fields['map_field_name']] if fetchtempdatas[
                        map_fields['map_field_name']] else None}
                serializer_data = dict(serializer_data, **d1)
                # defaultprice = fetchtempdatas["defaultprice"] if fetchtempdatas["defaultprice"] else 0
                # max_order_unit = fetchtempdatas["max_order_unit"] if fetchtempdatas["max_order_unit"] else None
                # status = fetchtempdatas["status"] if fetchtempdatas["status"] else None
                # description = fetchtempdatas["description"] if fetchtempdatas["description"] else None
                # small_description = fetchtempdatas["mp_system_requirements"] if fetchtempdatas["mp_system_requirements"] else None
                # features = fetchtempdatas["features"] if fetchtempdatas["features"] else None
                # asin = fetchtempdatas["asin"] if fetchtempdatas["asin"] else None
                # ean = fetchtempdatas["ean"] if fetchtempdatas["ean"] else None
            else:
                if map_fields["map_field_name"] == "taxclass_id":
                    if fetchtempdatas["taxclass_id"]:
                        tax_class_id = get_tax_class_id(fetchtempdatas["taxclass_id"], fetchtempdatas["website_id"])
                    else:
                        tax_class_id = 0
                    d1 = {"taxclass_id": tax_class_id};
                    serializer_data = dict(serializer_data, **d1)

                elif map_fields["map_field_name"] == "supplier_id":
                    if fetchtempdatas["supplier_id"]:
                        supplier_id = get_supplier_id(fetchtempdatas["supplier_id"], fetchtempdatas["website_id"])
                    else:
                        supplier_id = 0
                    d1 = {"supplier_id": supplier_id};
                    serializer_data = dict(serializer_data, **d1)
                elif map_fields["map_field_name"] == "hsn_id":
                    if type(fetchtempdatas["hsn_id"]) == float:
                        fetchtempdatas["hsn_id"] = int(round(fetchtempdatas["hsn_id"]))
                    else:
                        fetchtempdatas["hsn_id"] = fetchtempdatas["hsn_id"]

                    if fetchtempdatas["hsn_id"]:
                        hsn_id = get_hsn_id(fetchtempdatas["hsn_id"], fetchtempdatas["website_id"])
                    else:
                        hsn_id = None
                    d1 = {"hsn_id": hsn_id};
                    serializer_data = dict(serializer_data, **d1)
                elif map_fields["map_field_name"] == "customer_group_id":
                    if fetchtempdatas["customer_group_id"]:
                        customer_group_id = get_customer_group_id(fetchtempdatas["customer_group_id"],
                                                                  fetchtempdatas["website_id"])
                    else:
                        customer_group_id = 0
                    d1 = {"customer_group_id": customer_group_id};
                    serializer_data = dict(serializer_data, **d1)
                elif map_fields["map_field_name"] == "brand":
                    if fetchtempdatas["brand"]:
                        brand_id = get_brand_id(fetchtempdatas["brand"], fetchtempdatas["website_id"])
                    else:
                        brand_id = 0
                    d1 = {"brand": brand_id};
                    serializer_data = dict(serializer_data, **d1)

        main_product_sku = None
        find_parent_sku = None
        main_product_sku = checksku_no(fetchtempdatas["website_id"], fetchtempdatas["sku"])
        parent_product_id = fetchtempdatas["parent_product_id"]
        # if parent_product_id:

        if not parent_product_id:
            visibility_id = 1
        else:
            if parent_product_id == fetchtempdatas["sku"]:
                visibility_id = 1
            else:
                find_parent_sku = checksku_no(fetchtempdatas["website_id"], parent_product_id)
                if find_parent_sku != 0:
                    visibility_id = 4
                else:
                    visibility_id = 1

        # d1 = {"website_id":fetchtempdatas["website_id"],"name":fetchtempdatas["name"],"sku":fetchtempdatas["sku"],"weight":weight,"tax_class_id":tax_class_id,"supplier_id":supplier_id,"customer_group_id":customer_group_id,"defaultprice":defaultprice,"hsn_id":hsn_id,"max_order_unit":max_order_unit,"status":status,"description":description,"mp_system_requirements":small_description,"features":features,"asin":asin,"ean":ean,"brand":brand_id,"main_product_sku":main_product_sku,"find_parent_sku":find_parent_sku}

        # print("================================",tmp_image1)
        current_time = datetime.datetime.now(datetime.timezone.utc).date()
        d1 = {"website_id": fetchtempdatas["website_id"], "main_product_sku": main_product_sku,
              "find_parent_sku": find_parent_sku, "visibility_id": visibility_id, "created": current_time,
              "modified": current_time}

        serializer_data = dict(serializer_data, **d1)

        datas.append(serializer_data)
        tmp_image.update({"website_id": fetchtempdatas["website_id"]})
        if "uom" in fetchtempdatas:
            created_uom_id = create_or_update_uom(fetchtempdatas["uom"], fetchtempdatas["website_id"], request_ip)
            uom_id = {"uom": created_uom_id}
            serializer_data = dict(serializer_data, **uom_id)

        hasproduct = EngageboostProducts.objects.using(company_db).filter(sku=fetchtempdatas["sku"],
                                                                          isdeleted='n').first()

        if hasproduct:
            try:
                product_slug = common.create_product_slug(fetchtempdatas["name"], hasproduct.id)
                product_slug = unidecode.unidecode(product_slug).lower()
                product_slug = re.sub(r'\W+', '-', product_slug)
                product_slug = slugify(product_slug)

                method = request.scheme
                current_url = request.META['HTTP_HOST']
                url = method + '://' + current_url + '/product/' + product_slug

                # if not hasproduct.url:
                #     d1 = {"url":url};serializer_data = dict(serializer_data,**d1)
                # if not hasproduct.slug:
                #     d1 = {"slug":product_slug};serializer_data = dict(serializer_data,**d1)
                d1 = {"url": url, "slug": product_slug};
                serializer_data = dict(serializer_data, **d1)
            except:
                pass
            existingproduct = EngageboostProducts.objects.using(company_db).get(id=hasproduct.id)
            serializer = BasicinfoSerializer(existingproduct, data=serializer_data, partial=True)
            new_product_entry = "no"
        else:
            product_slug = common.create_product_slug(fetchtempdatas["name"])
            product_slug = unidecode.unidecode(product_slug).lower()
            product_slug = re.sub(r'\W+', '-', product_slug)
            product_slug = slugify(product_slug)

            method = request.scheme
            current_url = request.META['HTTP_HOST']
            url = method + '://' + current_url + '/product/' + product_slug

            d1 = {"url": url, "slug": product_slug};
            serializer_data = dict(serializer_data, **d1)

            serializer = BasicinfoSerializer(data=serializer_data, partial=True)
            new_product_entry = "yes"

        if serializer.is_valid():
            serializer.save()

            try:
                if serializer_data['barcodes']:
                    barcodes = str(serializer_data['barcodes'])
                    barcodes = barcodes.split(',')
                    if len(barcodes) > 0:
                        EngageboostMultipleBarcodes.objects.filter(product_id=serializer.data['id']).delete()
                        for i in barcodes:
                            exists = EngageboostMultipleBarcodes.objects.filter(barcode=i, isdeleted="n", isblocked='n')
                            if exists.count() == 0:
                                bar_data = {
                                    'product_id': serializer.data['id'],
                                    'barcode': i,
                                    'website_id': serializer.data['website_id'],
                                    'created': current_time,
                                    'modified': current_time

                                }
                                EngageboostMultipleBarcodes.objects.create(**bar_data)
            except:
                pass

            tmp_image.update({"product": serializer.data['id']})
            custom_field_value = EngageboostTempProductCustomFields.objects.using(company_db).all().filter(
                product_id=fetchtempdatas["id"])
            if custom_field_value:
                saved_custom_value_list = save_import_product_custom_fields_value(fetchtempdatas["website_id"],
                                                                                  fetchtempdatas["id"],
                                                                                  serializer.data['id'], module_id,
                                                                                  post_data["filename"],
                                                                                  custom_field_value)

            serializer_product_category = {}
            dict_prod_cat = {}
            current_time = datetime.datetime.now(datetime.timezone.utc).date()
            # product_category_obj = ProductCategoriesSerializer(product_id=serializer.data['id'],category_id=post_data["category_id"])
            # -----Binayak Start-----#
            if "category_id" in post_data:
                if post_data['category_id'] is not None and int(post_data['category_id']) > 0:
                    dict_prod_cat = {"product_id": serializer.data['id'], "category_id": post_data['category_id'],
                                     "is_parent": 'y', "created": current_time, "modified": current_time};
            # -----Binayak End------#
            serializer_product_category = dict(serializer_product_category, **dict_prod_cat)
            serializer2 = ProductCategoriesSerializer(data=serializer_product_category, partial=True)

            if serializer2.is_valid():
                # -----Binayak Start 26-10-2020-----#
                # EngageboostProductCategories.objects.using(company_db).filter(product_id=serializer.data['id']).delete() # Delete previous product category
                # -----Binayak End 26-10-2020-----#
                # serializer2.save()

                has_record = EngageboostProductCategories.objects.last()
                if has_record:
                    last_entry_of_table = EngageboostProductCategories.objects.order_by('-id').latest('id')
                    row_id = int(last_entry_of_table.id) + int(1)
                else:
                    row_id = 1
                dict_prod_cat = {"id": row_id};
                serializer_product_category = dict(serializer_product_category, **dict_prod_cat)

                serializer2 = EngageboostProductCategories.objects.using(company_db).create(
                    **serializer_product_category)
                if serializer2:
                    last_prod_cat_id = serializer2.id
                else:
                    last_prod_cat_id = 0
                data = {'status': 1, 'api_status': last_prod_cat_id, 'message': 'Product Category Updated Successfully'}
                datas.append(data)
            else:
                data = {'status': 0, 'api_status': serializer2.errors, 'message': 'Error Occured in Product Category'}
                datas.append(data)

            if visibility_id == 4:
                serializer_cross_sell_product = {}
                dict_cross_sell = {"cross_product_id": serializer.data['id'], "product_id": find_parent_sku};
                serializer_cross_sell_product = dict(serializer_cross_sell_product, **dict_cross_sell)

                serializer3 = CossSellProductsSerializer(data=serializer_cross_sell_product, partial=True)

                if serializer3.is_valid():
                    EngageboostCossSellProducts.objects.using(company_db).filter(
                        cross_product_id=serializer.data['id']).delete()
                    # serializer3.save()
                    cross_obj = EngageboostCossSellProducts.objects.using(company_db).create(**dict_cross_sell)
                    data = {'status': 1, 'api_status': cross_obj.id, 'message': 'Product Variant Updated Successfully'}
                    datas.append(data)
                else:
                    data = {'status': 0, 'api_status': serializer3.errors,
                            'message': 'Error Occured in Product Variant'}
                    datas.append(data)

            if new_product_entry == "yes":
                save_product_inventory_with_zero_quantity(serializer.data['id'])

            # print(tmp_image)
            if len(tmp_image1) > 0:
                for tmp_item in tmp_image1:
                    if tmp_item['is_cover'] == 1:
                        EngageboostTempProductimages.objects.using(company_db).filter(product=serializer.data['id'],
                                                                                      is_cover=1).update(is_cover=0)
                    tmp_item.update(
                        {"created": current_time, "modified": current_time, "product": serializer.data['id'],
                         "website_id": serializer.data['website_id']})
                    EngageboostTempProductimages.objects.using(company_db).create(**tmp_item)
                    # print("Image to temp============")

            if len(secondary_category1) > 0:
                common.update_db_sequences("product_categories")
                # -----Binayak Start 22-12-2020------#
                EngageboostProductCategories.objects.using(company_db).filter(product_id=serializer.data['id']).update(
                    isblocked='y', isdeleted='y')
                # -----Binayak End 22-12-2020------#
                for secondary_category in secondary_category1:
                    secondary_category.update(
                        {"created": current_time, "modified": current_time, "product_id": serializer.data['id']})
                    print("Category Mapp=====================", secondary_category)
                    EngageboostProductCategories.objects.using(company_db).create(**secondary_category)

            # ------Binayak Start 19-03-2021------#
            # elastic = common.save_data_to_elastic(serializer.data['id'],'EngageboostProducts')
            product_ids.append(serializer.data['id'])
            # elastic_data_string = save_data_to_elastic_single_data_generate_for_bulk(serializer.data['id'],'EngageboostProducts')
            # ------Binayak End 19-03-2021------#

            responseDatas = {"status": 1, "api_response": datas, "message": 'Product Saved'}
        else:
            data = {'status': 0, 'api_status': serializer.errors, 'message': 'Error Occured'}
            datas.append(data)

            responseDatas = {"status": 0, "api_response": datas, "message": 'Error Occured in Product'}

    # ------Binayak Start 19-03-2021------#
    common.products_to_elastic(product_ids)
    # ------Binayak End 19-03-2021------#

    EngageboostImportMapFields.objects.using(company_db).delete()
    # EngageboostTempProducts.objects.using(company_db).delete()
    EngageboostTempProductCustomFields.objects.using(company_db).delete()
    return


def save_import_product_custom_fields_value(website_id,temp_product_id,product_id,module_id,filename,tempcustomfielddatas):
    datas=[]
    if temp_product_id:
        customfielddatas = TempProductCustomFieldsSerializer(tempcustomfielddatas,many=True)
        for tempcustomfielddata in customfielddatas.data:
            field_name = tempcustomfielddata['field_name']
            label_value = tempcustomfielddata['field_value']
            find_mapped_data_cond = EngageboostImportMapFields.objects.filter(db_field_name=field_name,website_id=website_id,module_id=module_id,file_name=filename).first()
            if find_mapped_data_cond:
                find_mapped_data = ImportMapFieldsSerializer(find_mapped_data_cond)
                module_layout_field_id = find_mapped_data.data["module_layout_field_id"]

                current_field_arr_cond = EngageboostDefaultModuleLayoutFields.objects.filter(id=module_layout_field_id).first()
                current_field_arr = DefaultModuleLayoutFieldsSerializer(current_field_arr_cond)
                if current_field_arr and current_field_arr.data["show_market_places"]:                    
                    field_id = current_field_arr.data["field_id"]
                    label = current_field_arr.data["field_label"]
                    channel_id_arr = current_field_arr.data["show_market_places"].split(',')

                    for channel_id in channel_id_arr:
                        label_value = label_value
                        if label:
                            MarketplaceFieldValue = {}
                            check_data_cond = EngageboostMarketplaceFieldValue.objects.filter(field_label=label,field_id=field_id,product_id=product_id,channel_id=channel_id).first()
                            
                            current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
                            d1 = {"product_id":product_id,"channel_id":channel_id,"field_id":field_id,"value":label_value,"website_id":website_id,"field_name":label,"field_label":label,"created":current_time,"modified":current_time}
                            MarketplaceFieldValue = dict(MarketplaceFieldValue,**d1)

                            if check_data_cond:
                                check_data = MarketplaceFieldValueSerializer(check_data_cond)

                                save_market_place_field_value = EngageboostMarketplaceFieldValue.objects.filter(id=check_data.data["id"]).update(**MarketplaceFieldValue)
                                if save_market_place_field_value:
                                    save_market_place_field_value_id = save_market_place_field_value
                                else:
                                    save_market_place_field_value_id = 0

                                datas.append(save_market_place_field_value_id)
                            else:
                                has_record = EngageboostMarketplaceFieldValue.objects.last()
                                if has_record:
                                    last_entry_of_table = EngageboostMarketplaceFieldValue.objects.order_by('-id').latest('id')
                                    row_id = int(last_entry_of_table.id)+int(1)
                                else:
                                    row_id = 1
                                d1 = {"id":row_id};MarketplaceFieldValue = dict(MarketplaceFieldValue,**d1)

                                save_market_place_field_value = EngageboostMarketplaceFieldValue.objects.create(**MarketplaceFieldValue)
                                if save_market_place_field_value:
                                    save_market_place_field_value_id = save_market_place_field_value.id
                                else:
                                    save_market_place_field_value_id = 0

                                datas.append(save_market_place_field_value_id)
    return Response(datas)

def save_product_inventory_with_zero_quantity(product_id):
    web_id = 1
    conditionWareHouse = EngageboostWarehouseMasters.objects.all().filter(isblocked='n',isdeleted='n',website_id=web_id)
    if conditionWareHouse:
        WarehouseMasterData = WarehousemastersSerializer(conditionWareHouse,many=True)
        for WarehouseMaster in WarehouseMasterData.data:
            has_stocks = EngageboostProductStocks.objects.filter(product_id=product_id,warehouse_id=WarehouseMaster["id"]).first()
            if has_stocks:
                pass
            else:
                current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
                EngageboostProductStocks.objects.create(product_id=product_id,warehouse_id=WarehouseMaster["id"],stock=0,safety_stock=0,real_stock=0,virtual_stock=0,stock_unit=0,created=current_time,modified=current_time)

def get_tax_class_id(tax_name,website_id,enquiry_type="id"):
    if enquiry_type=="id":
        tax_class_details = EngageboostProductTaxClasses.objects.filter(website_id=website_id,name=tax_name,isdeleted="n",isblocked="n").first()
        if tax_class_details:
            tax_class_id = tax_class_details.id
        else:
            tax_class_id = 0
    else:
        tax_class_details = EngageboostProductTaxClasses.objects.filter(website_id=website_id,id=tax_name,isdeleted="n",isblocked="n").first()
        if tax_class_details:
            tax_class_id = tax_class_details.name
        else:
            tax_class_id = ''

    return tax_class_id

def get_supplier_id(supplier_name,website_id,enquiry_type="id"):
    supplier_id = 0
    if enquiry_type=="id": 
        supplier_details = EngageboostSuppliers.objects.filter(website_id=website_id,name=supplier_name,isdeleted="n").first()

        if supplier_details:
            supplier_id = supplier_details.id
        else:
            has_record = EngageboostSuppliers.objects.last()
            if has_record:
                last_entry_of_table = EngageboostSuppliers.objects.order_by('-id').latest('id')
                row_id = int(last_entry_of_table.id)+int(1)
            else:
                row_id = 1 

            serializer_data={}
            d1 = {"id":row_id,"name":supplier_name,"code":supplier_name,"website_id":website_id,"status":"Enabled","isdeleted":"n","isblocked":"n","owner_id":0}
            serializer_data = dict(serializer_data,**d1)
            save_supplier = EngageboostSuppliers.objects.create(**serializer_data)

            if save_supplier:
                supplier_id = save_supplier.id
            else:
                supplier_id = 0
    else:
        supplier_id_list=[]
        supplierIds = supplier_name.split(',')
        for supplierId in supplierIds:
            supplier_details = EngageboostSuppliers.objects.filter(website_id=website_id,id=supplierId,isdeleted="n").first()
            if supplier_details:
                supplier_id = supplier_details.name
                supplier_id_list.append(str(supplier_id))
            else:
                supplier_id = ''

        if supplier_id_list:        
            supplier_id = ','.join(supplier_id_list)
        else:
            supplier_id = ''

    return supplier_id

def get_customer_group_id(customer_group_name,website_id):
    customer_group_id = 0
    customer_list = EngageboostCustomerGroup.objects.filter(website_id=website_id,name=customer_group_name,isdeleted="n",isblocked="n").first()
    if customer_list:
        customer_group_id = customer_list.id
    else:
        customer_group_id = 0

    return customer_group_id

def get_hsn_id(hsn_id,website_id):
    if type(hsn_id) == float:
        hsn_code=int(hsn_id)
    else:
        hsn_code=hsn_id
    hsn_details = EngageboostHsnCodeMaster.objects.filter(hsn_code=hsn_code).first()
    if hsn_details:
        hsn_id = hsn_details.id
    else:
        hsn_id = None

    return hsn_id

def get_brand_id(brand_name,website_id,enquiry_type="id"):
    if enquiry_type=="id":
        brand_details = EngageboostBrandMasters.objects.filter(website_id=website_id,name__iexact=brand_name,isdeleted="n",isblocked="n").first()
        if brand_details:
            brand_id = brand_details.id
        else:
            has_record = EngageboostBrandMasters.objects.last()
            if has_record:
                last_entry_of_table = EngageboostBrandMasters.objects.order_by('-id').latest('id')
                row_id = int(last_entry_of_table.id)+int(1)
            else:
                row_id = 1 

            serializer_data={}
            namejson = brand_name
            name = namejson.lower()
            name1 = name.replace(" ", "-")
            nametrns = name1.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~=+"})
            nametrns = slugify(nametrns)

            d1 = {"id":row_id,"name":brand_name,"website_id":website_id,"isdeleted":"n","isblocked":"n","slug":nametrns}
            serializer_data = dict(serializer_data,**d1)
            save_brand = EngageboostBrandMasters.objects.create(**serializer_data)

            if save_brand:
                brand_id = save_brand.id
            else:
                brand_id = 0
    else:
        brand_id_arr = brand_name.split(',')
        if len(brand_id_arr)>0:
            # brand_details = EngageboostBrandMasters.objects.filter(website_id=website_id,id__in=brand_name,isdeleted="n",isblocked="n").first()
            brand_details = EngageboostBrandMasters.objects.filter(website_id=website_id,id__in=brand_id_arr,isdeleted="n",isblocked="n").aggregate(name_list=ArrayAgg('name'))
            if brand_details:
                brand_id = ', '.join(brand_details['name_list']) 
            else:
                brand_id = ''
        else:
            brand_id = ''
    return brand_id

def checksku_no(website_id,sku,enquiry_type="id"):
    ids = 0
    if enquiry_type=="id":
        condition = EngageboostProducts.objects.filter(website_id=website_id,sku=sku,isdeleted="n").first()
        ids = 0
        # if($product_id > 0) {
        #     $condition = " AND Product.id!={$product_id}";
        # }
        # number_of_data = BasicinfoSerializer(condition,many=True)
        # ids = {}
        # for nod in number_of_data.data:
        #     p_id = {str(nod['id']):nod["id"]}
        #     ids = dict(ids,**p_id)
        if condition:
            number_of_data = BasicinfoSerializer(condition)
            ids = number_of_data.data["id"]
    else:
        condition = EngageboostProducts.objects.filter(website_id=website_id,id=sku,isdeleted="n").first()
        if condition:
            ids = condition.sku
        else:
            ids = ''
    return ids


class ProductExport(generics.ListAPIView):
    def get(self, request, website_id,format=None):
        company_db  = loginview.db_active_connection(request)
        today = datetime.datetime.today()
        today = today.strftime("%Y-%m-%d")
        file_name = "BMS_products_" + str(today) + ".xls"
        export_file_path = settings.MEDIA_ROOT+'/exportfile/'+file_name
        download_path = settings.MEDIA_URL + 'exportfile/'+file_name
        
        workbook    = xlsxwriter.Workbook(export_file_path)
        export_file_path = export_file_path[1:]
        worksheet   = workbook.add_worksheet()
        ProductListCond = EngageboostProducts.objects.using(company_db).all().filter(isdeleted='n').order_by('-id')
        ProductLists    = BasicinfoSerializer(ProductListCond, many=True)
        bold    = workbook.add_format({'bold': True})
        row     = 1
        worksheet.write(0,0,'Product Name',bold)
        worksheet.write(0,1,'SKU',bold)
        worksheet.write(0,2,'Category',bold)
        worksheet.write(0,3,'Gross Weight',bold)
        worksheet.write(0,4,'Sales Tax Class',bold)
        worksheet.write(0,5,'ASIN',bold)
        worksheet.write(0,6,'EAN/UPC',bold)
        worksheet.write(0,7,'Expected Delivery Days(sla)',bold)
        worksheet.write(0,8,'Cost Per Unit',bold)
        worksheet.write(0,9,'Features',bold)
        worksheet.write(0,10,'Large Description',bold)
        worksheet.write(0,11,'Small Description',bold)
        worksheet.write(0,12,'Status',bold)
        worksheet.write(0,13,'Parent SKU',bold)
        worksheet.write(0,14,'Supplier',bold)
        worksheet.write(0,15,'Brand',bold)
        worksheet.write(0,16,'Price',bold)
        worksheet.write(0,17,'Unit Of Measurement',bold)
        # return Response(ProductLists.data)
        for ProductList in ProductLists.data:
            prod_cat_list=[];prod_cat_list_string=''
            # ****** PRODUCT CATEGORIES ******#
            prod_cat_cond = EngageboostProductCategories.objects.using(company_db).all().filter(product_id=ProductList["id"])
            prod_cats = ProductCategoriesSerializer(prod_cat_cond,many=True)
            for prod_cat in prod_cats.data:
                cat_details = EngageboostCategoryMasters.objects.using(company_db).filter(id=prod_cat["category"]['id'],isdeleted='n').first()
                if cat_details:
                    prod_cat_list.append(str(cat_details.name))
            prod_cat_list_string = ','.join(prod_cat_list)
            # ****** PRODUCT SALES TAX ******#
            if ProductList["taxclass"]:
                tax_class_id = get_tax_class_id(ProductList["taxclass"]["id"],website_id,'name')
            else:
                tax_class_id = ''
            # ****** PRODUCT PARENT ******#
            cross_sell_product_cond = EngageboostCossSellProducts.objects.using(company_db).filter(cross_product_id=ProductList["id"]).first()
            # cross_sell_product = CossSellProductsSerializer(cross_sell_product_cond,partial=True)
            if cross_sell_product_cond:
                parent_sku = checksku_no(website_id,cross_sell_product_cond.product_id,'sku')
            else:
                parent_sku = ''
            # ****** PRODUCT SUPPLIER ******#
            if ProductList["supplier_id"]:
                supplier_name = get_supplier_id(ProductList["supplier_id"],website_id,'name')
            else:
                supplier_name = ''
            # ****** PRODUCT BRAND ******#
            if ProductList["brand"]:
                brand_name = get_brand_id(ProductList["brand"],website_id,'name')
            else:
                brand_name = ''
            worksheet.write(row,0,ProductList['name'],0)
            worksheet.write(row,1,ProductList['sku'],0)
            worksheet.write(row,2,prod_cat_list_string,0)
            worksheet.write(row,3,ProductList['weight'],0)
            worksheet.write(row,4,tax_class_id,0)
            worksheet.write(row,5,ProductList['asin'],0)
            worksheet.write(row,6,ProductList['ean'],0)
            worksheet.write(row,7,ProductList['sla'],0)
            worksheet.write(row,8,ProductList['cost_per_unit'],0)
            worksheet.write(row,9,ProductList['features'],0)
            worksheet.write(row,10,ProductList['description'],0)
            worksheet.write(row,11,ProductList['mp_system_requirements'],0)
            if ProductList['status'] and ProductList['status']=='n':
                product_status = 'Inactive'
            else:
                product_status = 'Active'
            worksheet.write(row,12,product_status,0)
            worksheet.write(row,13,parent_sku,0)
            worksheet.write(row,14,supplier_name,0)
            worksheet.write(row,15,brand_name,0)
            worksheet.write(row,16,ProductList['default_price'],0)
            worksheet.write(row,17,ProductList['uom_name'],0)
            row = row+1
        workbook.close()
        data ={'status':1, "file_path": download_path}
        return Response(data)

class getEanProduct(generics.ListAPIView):
    def post(self, request):
        post_data = request.data
        itemId = post_data['itemId'].split(',')
        if not 'ean' in post_data:
            return Response({"status":0, "Message": "Please Provide an ean no"})
        if not 'website_id' in post_data:
            return Response({"status":0, "Message": "Please Provide an website id"})
        data = []
        if EngageboostProducts.objects.filter(ean=post_data['ean'], website_id=post_data['website_id'],id__in=itemId).exists():
            get_product = EngageboostProducts.objects.filter(ean=post_data['ean'],  website_id=post_data['website_id'],id__in=itemId).first()
            serializer = EngageboostProductsSerializer(get_product)
            data.append(serializer.data) 
            if get_product.isblocked == 'y':
                return Response({'status':1, "Message": "Product is Inactive", "data":serializer.data})
            else:
                return Response({'status':1, "Message": "Product is active", "data":serializer.data})
        else:
            return Response({'status':0, "Message":"Invalid EAN number."})

class ImportFileRelatedProducts(generics.ListAPIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        datas = []
        db_fields = []
        product_path = 'products'
        module_id = 1
        temp_model = 'TempRelatedProducts'
        model = 'RelatedProducts'
        filepath = 'importfile'
        post_data = request.data
        if 'import_file' in request.FILES:
            rand = str(random.randint(1,99999))
            file1 = request.FILES['import_file']
            file_name=file1.name
            ext = file_name.split('.')[-1]
            time_stamp = str(int(datetime.datetime.now().timestamp()))
            new_file_name='RelatedProducts_'+rand+time_stamp
            fs=FileSystemStorage()
            filename = fs.save(filepath+'/'+product_path+'/'+new_file_name+'.'+ext, file1)
            uploaded_file_url = fs.url(filename)
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            csvReader = xlrd.open_workbook(settings.BASE_DIR+uploaded_file_url)
            sheet = csvReader.sheet_by_index(0)
            headers = [str(cell.value) for cell in sheet.row(0)]
            headers = {k: k for k in headers}
        db_fields = common.get_db_fields(post_data['import_file_type'])
        for db_field in db_fields:
            has_record = EngageboostImportMapFields.objects.last()
            if has_record:
                last_entry_of_table = EngageboostImportMapFields.objects.order_by('-id').latest('id')
                row_id = int(last_entry_of_table.id)+int(1)
            else:
                row_id = 1
            savemaplist = EngageboostImportMapFields.objects.using(company_db).create(id=row_id,website_id=post_data['website_id'],module_id=module_id,file_field_name=db_field['field_label'],db_label_name=db_field['field_label'],db_field_name=db_field['model_field_value'],module_layout_field_id=db_field['id'],file_type='Excel',file_name=new_file_name+'.'+ext)
            if savemaplist:
                last_mapping_id = savemaplist.id
                datas.append(last_mapping_id)
            else:
                datas.append('failed')
        datas = {"filename":new_file_name+'.'+ext,"xls_header":headers,"db_fields":db_fields}
        return Response(datas) 

class SaveFileRelatedData(generics.ListAPIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        product_path = 'products'
        module_id = 1
        temp_model = 'TempRelatedProducts'
        model = 'RelatedProducts'
        filepath = 'importfile'
        datas = []
        custom_field_datas=[]
        errors = []
        post_data = request.data
        map_fields = eval(json.dumps(post_data["map_fields"]))
        if map_fields:
            for key,val in iter(map_fields.items()):
                if val['id'] == 0:
                    savemaplist = EngageboostImportMapFields.objects.using(company_db).filter(website_id=post_data['website_id'],module_id=module_id,db_field_name=val['field_name'],file_type='Excel',file_name=post_data["filename"]).update(file_field_name=key,map_field_name=val['field_name'],module_layout_field_id=None)
                else:
                    savemaplist = EngageboostImportMapFields.objects.using(company_db).filter(website_id=post_data['website_id'],module_id=module_id,db_field_name=val['field_name'],file_type='Excel',file_name=post_data["filename"]).update(file_field_name=key,map_field_name=val['field_name'],module_layout_field_id=val['id'])

        # Read xls Data
        fs=FileSystemStorage()
        filename = filepath+'/'+product_path+'/'+post_data["filename"]
        uploaded_file_url = fs.url(filename)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csvReader = xlrd.open_workbook(settings.BASE_DIR+uploaded_file_url)
        sheet = csvReader.sheet_by_index(0)
        length=len(sheet.col_values(0))
        xls_column_header_info = []
        xls_column_info={}
        row_no_in_xls= sheet.ncols
        for x in range(length):
            if x==0:
                for i in range(row_no_in_xls):
                    d11 ={"column_name":sheet.col_values(i)[x],"column_number":i}; xls_column_info=dict(xls_column_info,**d11)
                    xls_column_header_info.append(xls_column_info)
            else:
                pass

        for x in range(length):
            if x==0:
                pass
            else:
                error=[]
                has_record = EngageboostTempProducts.objects.last()
                if has_record:
                    last_entry_of_table = EngageboostTempProducts.objects.order_by('-id').latest('id')
                    row_id = int(last_entry_of_table.id)+int(1)
                else:
                    row_id = 1

                serializer_data={}
                CF_serializer_data={}
                custom_field_list=[]

                product_name = ""
                d1 = {"id":row_id,"website_id":post_data['website_id'],"file_name":post_data['filename']};
                serializer_data=dict(serializer_data,**d1)
                
                try:
                    if map_fields:
                        for key,val in iter(map_fields.items()):
                            for xls_column_header in xls_column_header_info:
                                if str(key) == str(xls_column_header["column_name"]):
                                    column_number = xls_column_header["column_number"]
                                    field_value = sheet.col_values(column_number)[x] if sheet.col_values(column_number)[x] else None
                            
                            field_value = str(field_value)
                            field_value     = field_value.split('.')[0]
                            
                            if map_fields[key]["field_name"] != "no" and key != "parent_category_selected" and key != "second_label_categorys" and key !="third_label_categorys" and key != "forth_label_categorys":
                                if str(map_fields[key]["field_name"])=="upsell_product_skus" or str(map_fields[key]["field_name"])=="cross_product_skus" or str(map_fields[key]["field_name"])=="related_product_skus" or str(map_fields[key]["field_name"])=="substitude_product_skus" or str(map_fields[key]["field_name"])=="associated_product_skus":
                                    fieldArr = field_value.split(",")
                                    skufields = []
                                    if len(fieldArr)>0:
                                        for skus in fieldArr:
                                            skus = skus.strip()
                                            countsku = EngageboostProducts.objects.filter(sku=skus,isdeleted='n').count()

                                            if countsku==0:
                                                error.append({"sku":skus,"msg":"Invalid Product","field":key})
                                            else:
                                                skufields.append(skus)     
                                    field_value = ",".join(skufields)
                                else:
                                    fieldArr = field_value
                                    fieldArr = fieldArr.strip()
                                    if fieldArr:
                                        countsku = EngageboostProducts.objects.filter(sku=fieldArr,isdeleted='n').count()

                                        if countsku==0:
                                            error.append({"sku":fieldArr,"msg":"Invalid Product","field":key})
                                        else:
                                            proObj = EngageboostProducts.objects.filter(sku=fieldArr,isdeleted='n').last()
                                            product_name = proObj.name
                                    field_value = fieldArr
                                d1 = {map_fields[key]['field_name']:field_value,"name":product_name};
                                serializer_data=dict(serializer_data,**d1)
                except KeyError: no=""
                current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
                d1={"is_import":"y","created":current_time,"modified":current_time};
                serializer_data=dict(serializer_data,**d1)
                save_temp_product = EngageboostTempProducts.objects.using(company_db).create(**serializer_data)
                if save_temp_product:
                    datas.append('success')
                else:
                    datas.append('failed')
                if len(error)>0:
                    errors.append(error)
        if datas:
            data_status = {"status":1,"filename":post_data["filename"],"error":errors}
        else:
            data_status = {"status":0,"filename":post_data["filename"],"error":errors}

        os.remove(settings.BASE_DIR+uploaded_file_url)
        return Response(data_status)

class PreviewSaveFileRelated(generics.ListAPIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        post_data = request.data
        fetch_all_data = []
        data = {}
        if post_data["model"] == "related_product":
            fetch_all_data_cond = EngageboostTempProducts.objects.using(company_db).values("id","website_id","name","sku","status","isdeleted","isblocked","created","modified","related_product_skus","upsell_product_skus","cross_product_skus","associated_product_skus","substitude_product_skus").all().filter(website_id=post_data['website_id'],file_name=post_data['filename']) #fetch from temp product table
            if fetch_all_data_cond:
                fetch_all_datas = TempProductsSerializer(fetch_all_data_cond,many=True)
                # fetch_all_data = fetch_all_datas.data
                for fad in fetch_all_datas.data:
                    error=[]
                    count = EngageboostProducts.objects.filter(sku=fad['sku'],isdeleted='n').count()
                    if count==0:
                        error.append('Product not found')
                    special_char='no'
                    if error:
                        fad["error"] = 1
                        fad["error_message"] = error
                    else:
                        error.append("SUCCESS")
                        fad["error"] = 0
                        fad["error_message"] = error
                fetch_all_data = fetch_all_datas.data
            data = {"preview_data":fetch_all_data,"filename":post_data['filename']}
        return Response(data)

class SaveAllImportedRelated(generics.ListAPIView):
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        datas = []
        db_fields = []
        product_path = 'products'
        module_id = 1
        temp_model = 'TempRelatedProducts'
        model = 'RelatedProducts'
        filepath = 'importfile'
        fetch_temp_datas = []
        post_data = request.data
        selectedIds = post_data["selected_ids"].split(',')
        tempObj = EngageboostTempProducts.objects.using(company_db).values("id","website_id","name","sku","status","isdeleted","isblocked","created","modified","related_product_skus","upsell_product_skus","cross_product_skus","associated_product_skus","substitude_product_skus").filter(id__in=selectedIds)
        if tempObj.count()>0:
            fetch_temp_data_cond = tempObj.all()
            fetch_temp_data = TempProductsSerializer(fetch_temp_data_cond,many=True)
            for fetchtempdatas in fetch_temp_data.data:
                proObj = EngageboostProducts.objects.filter(sku=fetchtempdatas['sku'],isdeleted='n')
                if proObj.count()>0:
                    pros = proObj.last()
                    product_id = pros.id
                    if fetchtempdatas['related_product_skus']:
                        arr = fetchtempdatas['related_product_skus'].split(",")
                        for item in arr:
                            relObj = EngageboostProducts.objects.filter(sku=item).last()
                            relproduct_id = relObj.id
                            EngageboostRelatedProducts.objects.create(product_id=product_id,related_product_id=relproduct_id,related_product_type=1)
                    if fetchtempdatas['upsell_product_skus']:
                        arr = fetchtempdatas['upsell_product_skus'].split(",")
                        for item in arr:
                            relObj = EngageboostProducts.objects.filter(sku=item).last()
                            relproduct_id = relObj.id
                            EngageboostRelatedProducts.objects.create(product_id=product_id,related_product_id=relproduct_id,related_product_type=2)
                    if fetchtempdatas['cross_product_skus']:
                        arr = fetchtempdatas['cross_product_skus'].split(",")
                        for item in arr:
                            relObj = EngageboostProducts.objects.filter(sku=item).last()
                            relproduct_id = relObj.id
                            EngageboostRelatedProducts.objects.create(product_id=product_id,related_product_id=relproduct_id,related_product_type=3)
                    if fetchtempdatas['associated_product_skus']:
                        arr = fetchtempdatas['associated_product_skus'].split(",")
                        for item in arr:
                            relObj = EngageboostProducts.objects.filter(sku=item).last()
                            relproduct_id = relObj.id
                            EngageboostRelatedProducts.objects.create(product_id=product_id,related_product_id=relproduct_id,related_product_type=4)
                    if fetchtempdatas['substitude_product_skus']:
                        arr = fetchtempdatas['substitude_product_skus'].split(",")
                        for item in arr:
                            relObj = EngageboostProducts.objects.filter(sku=item).last()
                            relproduct_id = relObj.id
                            EngageboostRelatedProducts.objects.create(product_id=product_id,related_product_id=relproduct_id,related_product_type=5)
                    data ={'status':1,'api_status':fetchtempdatas,'message':'Success'}
                else:
                    data ={'status':0,'api_status':fetchtempdatas,'message':'Product Not Found'}
                datas.append(data)
            responseDatas = {"status":1,"api_response":datas,"message":'Product Saved'}
        else:
            responseDatas ={'status':0,'api_status':"",'message':'Error Occured'}
        EngageboostTempProducts.objects.using(company_db).filter(file_name=post_data['filename']).delete()
        return Response(responseDatas)

def create_or_update_uom(uom,website_id,request_ip):
    try:
        if website_id is None:
            raise Exception("website id is required")
        if uom is None:
            return
        curent_user_id = 1        
        if not EngageboostUnitMasters.objects.filter(website_id=website_id,unit_name__iexact=uom).exists():
            current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
            created_unit = EngageboostUnitMasters.objects.create(website_id=website_id,
                                                                unit_name=uom,
                                                                created=current_time,
                                                                modified=current_time,
                                                                unit_full_name=uom,
                                                                ip_address = request_ip,
                                                                createdby = curent_user_id,
                                                                updatedby = curent_user_id
                                                                )
        else:
            created_unit = EngageboostUnitMasters.objects.filter(website_id=website_id,unit_name__iexact=uom).last()       
        return created_unit.id
    except Exception as e:
        print("Exception occurred during creating a uom"+str(e))

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip




@csrf_exempt
def uploadImage(request):
    rs_tmp_image = EngageboostTempProductimages.objects.filter(status=0)
    if rs_tmp_image:
        for allimage in rs_tmp_image:
            if allimage.img and allimage.img is not None:
                # resp_arr = UploadImageFromUrl('https://jpeg.org/images/jpegsystems-home.jpg', 'product', 1)
                resp_arr = UploadImageFromUrl(allimage.img, 'product', 1)
                print(resp_arr)
                img_data = resp_arr[0][80]['image_name']
                current_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
                insert_id = EngageboostProductimages.objects.create(product_id=allimage.product,created=current_time,modified=current_time,img=img_data,is_cover=1)
                if insert_id.id>0:
                    EngageboostTempProductimages.objects.filter(product=allimage.product).delete()

    data = {
        "status":"success"
    }
    return JsonResponse(data)

def UploadImageFromUrl(image_url, module_name, website_id):
    product = "product"
    file1       = image_url
    extrev      = file1[::-1]
    extrevore   = extrev.split(".")
    ext         = extrevore[0][::-1]
    timestamp   = time.strftime("%Y%m%d%H%M%s")
    name1       = timestamp

    resize_arr = [80,100,200,400,800]
    return_arr = []
    
    for i in resize_arr:
        f_path = str(i)+'x'+str(i)
        img,headers = urllib.request.urlretrieve(file1, 'media/'+module_name+'/'+f_path+'/'+module_name+'_'+name1+'.'+ext)
        uploaded_image = product+'_'+name1+'.'+ext
        fs          = FileSystemStorage()
        BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uploaded_file_url = fs.url(img)

        return_obj = {}
        cdn_return = ResizeImageAndUpload(uploaded_image,i, website_id)

        return_obj.update({i:cdn_return})
        return_arr.append(return_obj)
    return return_arr
    # EngageboostProductimages.objects.using(company_db).create(product_id=last_id,created=datetime.now().date(),modified=datetime.now().date(),img=uploaded_image,is_cover=1,img_alt=image_meta_cover_data['img_alt'],img_title=image_meta_cover_data['img_title'],img_order=image_meta_cover_data['img_order']) 

def ResizeImageAndUpload(str_image_file,resolution, website_id):
    from PIL import Image
    import os
    import urllib.request

    other_image         = str_image_file
    resolution          = int(resolution)
    imgresolutionstr    = str(resolution)
    module_name         = 'product'
    str_resolution      = str(resolution)+'x'+str(resolution)

    website         = EngageboostCompanyWebsites.objects.get(id=website_id)
    company_name    = website.company_name
    s3folder_name   = website.s3folder_name

    image = Image.open(settings.BASE_DIR+'/media/'+module_name+'/'+str_resolution+'/'+other_image)
    width_origenal, height_origenal=image.size
    imageresizeon = 'Width'
    if imageresizeon =='Width':
        if width_origenal >int(resolution):
            ratio = width_origenal/height_origenal
            width=int(resolution)
            height=int(resolution*height_origenal/width_origenal)
        else:
            width=width_origenal
            height=height_origenal

    if imageresizeon =='Height':
        if height_origenal >resolution:
            ratio = height_origenal/width_origenal
            width=int(resolution*width_origenal/height_origenal)
            height=resolution
        else:
            width=width_origenal
            height=height_origenal
    img_anti = image.resize((width, height), Image.ANTIALIAS)
    new_image_file = settings.MEDIA_ROOT+'/'+module_name+'/'+str_resolution+'/'+other_image
    img_anti.save(new_image_file)
    cdn_return = common.amazons3_global_fileupload_new(other_image,imgresolutionstr,module_name,company_name,s3folder_name)
    cdn_return.update({"image_name":other_image})
    # returnarr = {
    #     "image_name":other_image,
    #     "cdn_return":cdn_return
    # }

    return cdn_return

class ProductSyncManual(generics.ListAPIView):
    def post(self, request, format=None):
        request_data = JSONParser().parse(request)
        ids = request_data['ids']
        common.products_to_elastic(ids)
        print("=========ids==============")
        data = {'status': 1, 'api_status': 'success', 'message': 'Successfully Updated'}
        return Response(data)



class ProductDesyncManual(generics.ListAPIView):
    def get(self, request, pk):
        manual_desync(pk)
        data = {'status': 1, 'api_status': 'success', 'message': 'Successfully Started'}
        return Response(data)

@postpone
def manual_desync(warehouse_id):
    es = common.connect_elastic()
    table_name = 'EngageboostProducts'
    product_ids = EngageboostChannelCurrencyProductPrice.objects.filter(warehouse_id=warehouse_id).values_list('product_id',
                                                                                                     flat=True)

    # print("======product_ids=======>", product_ids)


    response = emailcomponent.testmail('binayak.santra@navsoft.in',
    								   "Data Desync Started @@@ProductDesyncManualTest@@@",
    								   'Data Desync Started, PRODUCT_COUNT =====>' + str(
    									   product_ids.count()) + ' @ ' + str(
    									   datetime.datetime.now()))

    # print("======threading.active_count()=======", active_schedulers())

    datas = []
    docs = []
    current_product_chunk = []
    processed_product_chunk = []

    total_len_count = len(product_ids)

    if total_len_count > 0:

        index_name = common.get_index_name_elastic(product_ids[0], table_name)
        chunk_size = 500
        fragment_size, remainder = divmod(total_len_count, chunk_size)
        print("fragment_size====", fragment_size, remainder)
        if int(remainder) > 0:
            fragment_size += 1
        for i in range(fragment_size):
            docs = []
            datas = []
            data_string = []
            current_product_chunk = []
            processed_product_chunk = []
            try:

                # datas = []
                start_pos = i * chunk_size
                end_pos = (i + 1) * chunk_size

                if i == fragment_size - 1:
                    end_pos = start_pos + remainder

                print("======start_pos======", start_pos)
                print("======end_pos======", end_pos)
                current_product_chunk.extend(product_ids[start_pos:end_pos])

                for prod_id in current_product_chunk:
                    # for id in product_ids:
                    id_string = {
                        "_id": prod_id,
                        "_source": {
                                "include": ["channel_currency_product_price", "inventory"]
                            }
                    }
                    data_string.append(id_string)
                print("======data_string======", data_string)
                prod_exists = es.mget(body=json.dumps({"docs": data_string}), index=index_name, doc_type="data")

                # docs = []
                for item in prod_exists['docs']:
                    cm_id = item['_id']
                    if item['found'] == True:
                        price_data = item['_source']['channel_currency_product_price']

                        # warehouse_list = warehouse_id.copy()
                        warehouse_list = list(map(int, [warehouse_id]))
                        modified_price_data = common.remove_warehouse_channel_currency_price_update_string(cm_id,
                                                                                                           price_data,
                                                                                                           warehouse_list)

                        # print("=====modified_price_data=====", modified_price_data)

                        data = {"channel_currency_product_price": modified_price_data}

                        header = {
                            "_op_type": 'update',
                            "_index": index_name,
                            "_type": "data",
                            "_id": cm_id,
                            "doc": data
                        }
                        docs.append(header)
            except Exception as error:
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                datas.append({"status": 0, "api_status": traceback.format_exc(), "error_line": line,
                         "error_message": str(error),
                         "message": str(error)})


            finally:
                print('=======in finally========')
                # print("======docs=======", docs)
                obj = helpers.bulk(es, docs)

                datas.append({"obj": obj})

                response = emailcomponent.testmail('binayak.santra@navsoft.in',
                                                   "Data Desync to Elastic @@@ProductDesyncManualTest@@@",
                                                   'Data Desync Completed and Pushed to Elastic, PRODUCT_COUNT =====>' + str(
                                                       len(current_product_chunk)) + ' @ ' + str(
                                                       datetime.datetime.now()) + ' datas==123===>' + str(datas))

                manual_warehouse_product_price_sync(warehouse_id, current_product_chunk)


def manual_warehouse_product_price_sync(warehouse_id, prod_list):
    table_name = 'EngageboostProducts'
    field_name = 'channel_currency_product_price'
    warehouse_list = list(map(int, [warehouse_id]))
    common.update_bulk_elastic_now_process(table_name, item_ids=prod_list, field_name=field_name, action='index', warehouse=warehouse_list)