import base64
from django.contrib.auth.models import Group, GroupManager
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.conf import settings
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from webservices.models import *

from datetime import datetime
from django.db.models import Sum
from settings import settings


class GlobalSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostGlobalSettings
        fields = '__all__'


class CategoryBannersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCategoryBanners
        fields = '__all__'


class EngageboostUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostUsers
        fields = ["image_name"]


class CustomerListSerializer(serializers.ModelSerializer):
    imagename = serializers.SerializerMethodField()

    class Meta:
        model = EngageboostCustomers
        fields = ["first_name", "last_name", "email", "phone", "imagename",
                  "address", "street", "website_id", "created", "modified", "auth_user_id"]

    def get_imagename(self, EngageboostCustomers):
        qs = EngageboostUsers.objects.filter(
            id=EngageboostCustomers.auth_user_id, isdeleted='n', isblocked='n').values('image_name').all()
        image_data = EngageboostUsersSerializer(qs, many=True)
        if image_data.data:
            return image_data.data[0]['image_name']
        else:
            return None


class CategoryMastersSerializer(serializers.ModelSerializer):
    CategorBanner = serializers.SerializerMethodField()

    class Meta:
        model = EngageboostCategoryMasters
        fields = ["id", "parent_id", "display_order", "name", "description", "image", "thumb_image", "banner_image",
                  "page_title", "meta_description", "meta_keywords", "category_url", "slug", "CategorBanner"]

    def get_CategorBanner(self, EngageboostCategoryMasters):
        qs = EngageboostCategoryBanners.objects.filter(
            category_id=EngageboostCategoryMasters.id, isdeleted='n', isblocked='n', banner_type='c').all()
        category_banner = CategoryBannersSerializer(qs, many=True)
        return category_banner.data


class BrandMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostBrandMasters
        fields = ['id', 'name']


class ProductimagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductimages
        fields = '__all__'


class ProductStocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductStocks
        fields = ['product_id', 'real_stock', 'warehouse_id']


class ProductsViewSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProducts
        fields = ['id', 'name', 'sku', 'default_price', 'brand', 'slug',
                  'veg_nonveg_type', 'mp_description', 'mp_features', 'product_image', 'stock']

    def get_product_image(self, EngageboostProducts):
        qs = EngageboostProductimages.objects.filter(
            product_id=EngageboostProducts.id, status=0).all()
        product_image = ProductimagesSerializer(qs, many=True)
        return product_image.data

    def get_brand(self, EngageboostProducts):
        qs = EngageboostBrandMasters.objects.filter(
            id=EngageboostProducts.brand, isblocked='n', isdeleted='n').all()
        brand = BrandMastersSerializer(qs, many=True)
        return brand.data
    def get_stock(self, EngageboostProducts):
        ret_stock = 0
        if self.context.get('warehouse_id'):
            warehouse_id = self.context.get('warehouse_id')
            rs_stock = EngageboostProductStocks.objects.filter(product_id = EngageboostProducts.id,  warehouse_id = warehouse_id).first()
            if rs_stock:
                ret_stock = rs_stock.real_stock
        
        if float(ret_stock)>0:
            stock_data = {
                "stock_value":ret_stock,
                "stock_status":"available"
            }
        else:
            # stock_data = {
            #     "stock_value":0,
            #     "stock_status":"out of stock"
            # } 
            stock_data = {
                "stock_value":1,
                "stock_status":"available"
            }
        return stock_data

class ProductsViewNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProducts
        fields = ['id', 'name', 'sku', 'default_price', 'brand', 'slug',
                  'veg_nonveg_type', 'mp_description', 'mp_features', 'max_order_unit']


class CossSellProductsSerializer(serializers.ModelSerializer):
    cross_product = serializers.SerializerMethodField()

    class Meta:
        model = EngageboostCossSellProducts
        fields = '__all__'

    def get_cross_product(self, EngageboostCossSellProducts):
        qs = EngageboostProducts.objects.filter(
            id=EngageboostCossSellProducts.cross_product_id).all()
        coss_product = ProductsViewSerializer(qs, many=True)
        return coss_product.data


class CossSellProductsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCossSellProducts
        fields = '__all__'


class ShippingTableRateOrderAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostShippingTableRateOrderAmount
        fields='__all__'


class ShippingMastersSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostShippingMastersSettings
        fields='__all__'

class ProductsSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()
    variant_product = serializers.SerializerMethodField()

    class Meta:
        model = EngageboostProducts
        fields = '__all__'

    def get_product_image(self, EngageboostProducts):
        qs = EngageboostProductimages.objects.filter(
            product_id=EngageboostProducts.id, status=0).all()
        product_image = ProductimagesSerializer(qs, many=True)
        return product_image.data

    def get_variant_product(self, EngageboostProducts):
        qs = EngageboostCossSellProducts.objects.filter(
            product_id=EngageboostProducts.id).all()
        coss_product = CossSellProductsSerializer(qs, many=True)
        return coss_product.data


class ProductCategoriesSerializer(serializers.ModelSerializer):
    product = ProductsViewSerializer()

    class Meta:
        model = EngageboostProductCategories
        fields = ['id', 'category_id', 'product']


class ProductCategoriesViewSerializer(serializers.ModelSerializer):
    # product = ProductsViewSerializer()
    class Meta:
        model = EngageboostProductCategories
        fields = ['id', 'category_id', 'product']


class EngageboostMarketplaceFieldValueSerializer(serializers.ModelSerializer):
    product_id = serializers.SerializerMethodField()

    class Meta:
        model = EngageboostMarketplaceFieldValue
        fields = ['product_id', 'field_name', 'field_label', 'value']

    def get_product_id(self, EngageboostMarketplaceFieldValue):
        qs = EngageboostProducts.objects.filter(
            id=EngageboostMarketplaceFieldValue.product_id).all()
        coss_product = ProductsViewSerializer(qs, many=True)
        return coss_product.data


class CustomerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCustomerGroup
        fields = '__all__'


class ProducttaxclassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductTaxClasses
        fields = '__all__'


class ProductpriceroulSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostRepricingMaximumMinRules
        fields = '__all__'


class DiscountConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDiscountMastersConditions
        fields = '__all__'


class DiscountMasterCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDiscountMastersCoupons
        fields = '__all__'


class DiscountMasterSerializer(serializers.ModelSerializer):
    DiscountMastersConditions = DiscountConditionsSerializer(many=True)
    DiscountMastersCoupons = DiscountMasterCouponSerializer(many=True)

    class Meta:
        model = EngageboostDiscountMasters
        fields = '__all__'


class PaymentgatewaySettingInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPaymentgatewaySettingInformation
        fields = '__all__'


class WebsitePaymentmethodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostWebsitePaymentmethods
        fields = '__all__'


class BasicinfoSerializer(serializers.ModelSerializer):
    customer_group = CustomerGroupSerializer(read_only=True)
    taxclass = ProducttaxclassesSerializer(read_only=True)
    po_taxclass = ProducttaxclassesSerializer(read_only=True)
    max_price_rule = ProductpriceroulSerializer(read_only=True)
    min_price_rule = ProductpriceroulSerializer(read_only=True)
    product_images = ProductimagesSerializer(many=True, read_only=True)
    stock = serializers.SerializerMethodField()

    class Meta:
        model = EngageboostProducts
        fields = '__all__'
    def get_stock(self, EngageboostProducts):
        ret_stock = 0
        if self.context.get('warehouse_id'):
            warehouse_id = self.context.get('warehouse_id')
            rs_stock = EngageboostProductStocks.objects.filter(product_id = EngageboostProducts.id,  warehouse_id = warehouse_id).first()
            if rs_stock:
                ret_stock = rs_stock.real_stock
        
        if float(ret_stock)>0:
            stock_data = {
                "stock_value":ret_stock,
                "stock_status":"available"
            }
        else:
            # stock_data = {
            #     "stock_value":0,
            #     "stock_status":"out of stock"
            # }
            stock_data = {
                "stock_value":1,
                "stock_status":"available"
            }
        return stock_data

class CurrencyRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCurrencyRates
        fields = '__all__'


class EngageboostTemporaryShoppingCartsSerializer(serializers.ModelSerializer):
    product_id = serializers.SerializerMethodField()

    class Meta:
        model = EngageboostTemporaryShoppingCarts
        # fields = ['customer_id', 'product_id','product_name', 'product_sku', 'quantity']
        fields = '__all__'

    def get_product_id(self, EngageboostTemporaryShoppingCarts):
        if self.context.get('warehouse_id'):
            warehouse_id = self.context.get('warehouse_id')
        qs = EngageboostProducts.objects.filter(id=EngageboostTemporaryShoppingCarts.product_id, isblocked='n', isdeleted='n').first()
        cart_product = ProductsViewSerializer(qs,  context={'warehouse_id': warehouse_id})
        return cart_product.data


class CustomerListSerializers(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCustomers
        fields = ['first_name', 'last_name']


class EngageboostOrderMasterSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()

    class Meta:
        model = EngageboostOrdermaster
        fields = ["id", "created", "gross_amount_base", "customer"]

    def get_customer(self, EngageboostOrdermaster):
        qs = EngageboostCustomers.objects.filter(
            id=EngageboostOrdermaster.customer_id, isdeleted='n', isblocked='n').values('first_name', 'last_name').all()
        # customer_data = CustomerListSerializers(qs, many=True)
        if qs:
            return qs
        else:
            return None


class EngageboostOrderProductsSerializer(serializers.ModelSerializer):

    pruducts = serializers.SerializerMethodField()

    class Meta:
        model = EngageboostOrderProducts
        # fields= ['name','product_price','quantity','product_price','product_discount_price']
        fields = '__all__'

    def get_pruducts(self, EngageboostOrderProducts):
        qs = EngageboostProducts.objects.filter(
            id=EngageboostOrderProducts.product_id).values('name').all()
        if qs:
            return qs
        else:
            return None


class CategoryMastersNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = EngageboostCategoryMasters
        fields = ["id", "parent_id", "display_order", "name", "slug"]


class Productimages_linkSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()

    def get_img_url(self, EngageboostProductimages):
        return settings.directory_prduct2 + EngageboostProductimages.img

    class Meta:
        model = EngageboostProductimages
        fields = '__all__'


class EngageboostProductsSerializer(serializers.ModelSerializer):
    product_images = serializers.SerializerMethodField()

    class Meta:
        model = EngageboostProducts
        fields = '__all__'

    def get_product_images(self, EngageboostProducts):
        qs = EngageboostProductimages.objects.filter(
            product_id=EngageboostProducts.id, status=0).all()
        product_image = Productimages_linkSerializer(qs, many=True)
        return product_image.data


class EngageboostProductRatingsSerializers(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductRatings
        fields = '__all__'


class RelatedProductsSerializer(serializers.ModelSerializer):
    product_detail = serializers.SerializerMethodField()

    class Meta:
        model = EngageboostRelatedProducts
        fields = '__all__'

    def get_product_detail(self, EngageboostRelatedProducts):
        seri_data = EngageboostProducts.objects.filter(
            id=EngageboostRelatedProducts.related_product_id).all()
        product_detail = EngageboostProductsSerializer(seri_data, many=True)
        return product_detail.data


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCategoryMasters
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostBrandMasters
        fields = '__all__'


class EngageboostProductCategoriesSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = EngageboostProductCategories
        fields = '__all__'

    def get_category(self, EngageboostProductCategories):
        seri_data = EngageboostCategoryMasters.objects.filter(
            id=EngageboostProductCategories.category_id).all()
        category_detail = CategoriesSerializer(seri_data, many=True)
        return category_detail.data
