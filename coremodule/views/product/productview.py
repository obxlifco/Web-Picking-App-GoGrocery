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
from coremodule.views.product import discount
# from coremodule.comm
# from coremodule.views import common_function

from django.http import JsonResponse
import json
import base64
# import hashlib
# from Crypto import Random
# from Crypto.Cipher import AES
# from pkcs7 import PKCS7Encoder


@csrf_exempt
def get_company_website_id_by_url():
    website_id = 1
    return website_id


def get_max_order_unit():
    return 10


def warehouse_id_by_user_id(user_id, device_id):
    warehouse_id = 1
    return warehouse_id

# @csrf_exempt


class CategoryProductListView(generics.ListAPIView):
    def options(self,request,format=None):
        print("**************** Category prodyuct request ************")
    def get(self, request, format=None):
        website_id = request.META.get('HTTP_WID')
        category_id = request.META.get('HTTP_CAT')
        print("************category id *************")
        print(category_id)
        warehouse_id = 1
        # category_id = 2

        if website_id:
            pass
        else:
            website_id = 1
        product = []

        # Get sorting data
        filter_var = self.request.GET.get("filter")

        list_order_by = '-product__numberof_sale'
        if filter_var is not None and filter_var == "popular":
            list_order_by = "-product__numberof_sale"
        elif filter_var is not None and filter_var == "price-low-high":
            list_order_by = "product__default_price"
        elif filter_var is not None and filter_var == "price-high-low":
            list_order_by = "-product__default_price"
        else:
            list_order_by = "-product__numberof_sale"

        # View Only Parent Products
        product_ids = EngageboostProductCategories.objects.filter(category_id=category_id, isblocked='n', isdeleted='n', product__isdeleted='n', product__isblocked='n', product__visibility_id=1).all()

        # Product Filter

        #  Price Range
        price_range = self.request.GET.get("price_range")

        lower_price = 0
        upper_price = 0
        if price_range:
            price_range_arr = price_range.split("-")
            if len(price_range_arr) > 0:
                if price_range_arr[0] is not None:
                    lower_price = price_range_arr[0]
                if price_range_arr[1] is not None:
                    upper_price = price_range_arr[1]

            product_ids = product_ids.filter(product__default_price__gte=lower_price, product__default_price__lte=upper_price)

        # Brand
        brand = self.request.GET.get("brand")
        if brand:
            brand_arr = brand.split(",")
            product_ids = product_ids.filter(product__brand__in=brand_arr)

        # Order By (Sorting)
        product_ids = product_ids.order_by(list_order_by)

        # print(product_ids.query)

        # product_data = ProductCategoriesSerializer(product_ids, many=True)

        page = self.paginate_queryset(product_ids)
        if page is not None:
            serializer = ProductCategoriesSerializer(page, many=True)
            for products in serializer.data:
                # print(json.dumps(products, indent=4, sort_keys=True))
                # Get Product Stock
                qs_stock = EngageboostProductStocks.objects.filter(
                    product_id=products['id'], warehouse_id=warehouse_id).all()
                stock_data = ProductStocksSerializer(qs_stock, many=True)
                # Get variant Products
                cross_prod_arr = get_cross_products(products['id'])
                products.update(
                    {'varient_product': cross_prod_arr, 'stock_details': stock_data.data})
                # for cross_product in cross_prod_arr
                request_data = {
                    'website_id': website_id,
                    'company_id': website_id,
                    'product_ids': products['product']['id'],
                    'qtys': '1',
                    'prod_price': products['product']['default_price']
                }
                products_discount = discount.get_discount_detalils(request_data)

                for productsdiscount in products_discount:
                    products_discount_data = {
                        "new_default_price": productsdiscount['new_default_price'],
                        "new_default_price_unit": productsdiscount['new_default_price_unit'],
                        "discount_price_unit": productsdiscount['discount_price_unit'],
                        "discount_price": productsdiscount['discount_price'],
                        "discount_amount": productsdiscount['discount_amount'],
                        "disc_type": productsdiscount['disc_type'],
                        "coupon": productsdiscount['coupon']
                    }
                    products['product'].update(products_discount_data)
                product.append(products)
        return self.get_paginated_response(serializer.data)


class ProductDetailsView(generics.ListAPIView):
    def get(self, request, pk, format=None):
        product_id = pk
        # warehouse_id = request.GET('warehouse_id')
        website_id = request.META.get('HTTP_WID')
        if website_id:
            pass
        else:
            website_id = 1
        warehouse_id = 3
        rs_product = EngageboostProducts.objects.filter(id=product_id).first()
        if rs_product:
            product_data = ProductsSerializer(rs_product)
            product_data = product_data.data

            # Get Product Stock
            rs_stock = EngageboostProductStocks.objects.filter(
                product_id=product_id, isblocked='n', isdeleted='n', warehouse_id=warehouse_id).first()
            stock_data = ProductStocksSerializer(rs_stock)
            product_data.update({'stock_data': stock_data.data})

            # Get Variant Product
            coss_product = get_cross_products(product_id)
            product_data.pop('supplier_id')
            product_data.pop('new_date')
            product_data.pop('isbn')
            product_data.pop('ebay_item_id')
            product_data.pop('amazon_itemid')
            product_data.pop('ebay_addstatus')
            product_data.pop('twitter_addstatus')
            product_data.pop('ebay_listing_starttime')
            product_data.pop('ebay_listing_endtime')
            product_data.pop('ebay_listing_build')
            product_data.pop('ebay_listing_version')
            product_data.pop('ebay_listing_time')
            product_data.pop('total_listingfee')
            request_data = {
                'website_id': website_id,
                'company_id': website_id,
                'product_ids': product_id,
                'qtys': '1',
                'prod_price': product_data['default_price']
            }
            productsdiscount = discount.get_discount_detalils(request_data)
            products_discount_data = {
                "new_default_price": productsdiscount[0]['new_default_price'],
                "new_default_price_unit": productsdiscount[0]['new_default_price_unit'],
                "discount_price_unit": productsdiscount[0]['discount_price_unit'],
                "discount_price": productsdiscount[0]['discount_price'],
                "discount_amount": productsdiscount[0]['discount_amount'],
                "disc_type": productsdiscount[0]['disc_type'],
                "coupon": productsdiscount[0]['coupon']
            }
            product_data.update(products_discount_data)

            data = {
                "status": 1,
                "data": product_data
            }
        else:
            data = {
                "status": 0,
                "msg": "Product not found."
            }

        # ***************************************************************************************
        result = {'data': data}

        return Response(data)


class GetCossProduct(generics.ListAPIView):
    def get(self, request, format=None):
        cossdata = get_cross_products(4)
        data = {
            "status": 1
        }
        return Response(data)


def get_cross_products(product_id):
    # Let Product id is a parent Product
    coss_data = []
    parent_product_id = []
    cross_product_list = EngageboostCossSellProducts.objects.filter(
        product_id=product_id).all().values_list('cross_product_id', flat=True)
    if cross_product_list:
        coss_data = CossSellProductsViewSerializer(
            cross_product_list, many=True)
        # coss_data = coss_data.data
    else:
        # Let given product is a coss product, Find the parent and then find coss for that parent
        rs_parent = EngageboostCossSellProducts.objects.filter(
            cross_product_id=product_id).first()
        if rs_parent:
            cross_product_list = EngageboostCossSellProducts.objects.filter(
                product_id=rs_parent.product_id).values_list('cross_product_id', flat=True)

    rs_variant = EngageboostMarketplaceFieldValue.objects.filter(
        product_id__in=cross_product_list).all()
    variant_data = EngageboostMarketplaceFieldValueSerializer(
        rs_variant, many=True)
    return variant_data.data


class TestProd(generics.ListAPIView):
    def get(self, request, format=None):
        category_id = [2, 3]
        products_ids = get_product_id_list(category_id)
        # print(products_ids)
        if products_ids:
            product_data = ProductCategoriesSerializer(products_ids, many=True)

            for productlist in product_data.data:
                # print("kkkk123")
                # print(json.dumps(productlist["product"], indent=4, sort_keys=True))
                discount_data = discount.product_offer_discount_price(
                    1, productlist["product"])

            data = {
                "status": 1,
                "data": product_data.data
            }
        else:
            data = {
                "status": 0,
                "msg": "No product found."
            }
        return Response(data)


def get_product_id_list(cat_id_list=None):
    category_id = cat_id_list
    rs_product = EngageboostProductCategories.objects.filter(
        category_id__in=category_id, isblocked='n', isdeleted='n', product__isdeleted='n', product__isblocked='n', product__visibility_id=1).all()
    return rs_product


def category_children(category_id=0):
    category_ids = EngageboostProductCategories.objects.filter(
        parent_id__in=category_id, isblocked='n', isdeleted='n').all()
    return category_ids


def get_Product_detail(request, pk):
    if(request.method == "GET"):

        cnt_prod = EngageboostProducts.objects.filter(id=pk).count()
        if(cnt_prod != 0):
            objProduct = EngageboostProducts.objects.get(id=pk)

            objData = EngageboostProductsSerializer(objProduct)
            serializer_data = objData.data

            discount_seri_data = EngageboostDiscountMasters.objects \
                .filter(
                    isdeleted='n',
                    isblocked='n',
                    discount_type='p',
                    product_id__icontains=str(pk),
                    disc_start_date__lte=datetime.now(),
                    disc_end_date__gte=datetime.now()
                )
            #print(discount_seri_data)
            discount_data = DiscountMasterSerializer(
                discount_seri_data, many=True).data

            rating = EngageboostProductRatings.objects.filter(product_id=pk)

            rating_data = EngageboostProductRatingsSerializers(
                rating, many=True)

            related_prod = EngageboostRelatedProducts.objects.filter(
                product_id=pk)

            Related_Serializer = RelatedProductsSerializer(
                related_prod, many=True)

            serializer_data['RelatedProducts'] = Related_Serializer.data

            serializer_data['Product_rating'] = rating_data.data

            serializer_data['discount_data'] = discount_data

            data = {
                "status": 1,
                "message": "success",
                "Data": serializer_data
            }
        else:
            data = {
                "status": 0,
                "message": "Product not found"
            }
    else:
        data = {
            "status": 0,
            "message": "invalid request"
        }

    return JsonResponse(data)
