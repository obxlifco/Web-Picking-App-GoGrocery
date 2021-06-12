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
import json

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCustomers
        fields='__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    user_id = CustomerSerializer(many=True)
    class Meta:
        model = EngageboostUsers
        fields='__all__'
        
class EngageboostCategoryMastersLangSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCategoryMastersLang
        fields='__all__'


class CategoriesNewSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    lang_data = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostCategoryMasters
        fields=("id","parent_id","display_order","name","description","image","thumb_image","banner_image","page_title","meta_description","meta_keywords","category_url","slug","type","website_id","is_ebay_store_category","customer_group_id","display_mobile_app","show_navigation","product_count","lang_data")
    
    def get_product_count(self, EngageboostCategoryMasters):
        cnt_prod = EngageboostProductCategories.objects.filter(category_id=EngageboostCategoryMasters.id,product__visibility_id=1, isblocked='n', isdeleted='n').count()
        return cnt_prod

    def get_lang_data(self, EngageboostCategoryMasters):
        rs_lang     = EngageboostCategoryMastersLang.objects.filter(category_id=EngageboostCategoryMasters.id, isblocked='n', isdeleted='n').all().iterator()
        lang_data   = EngageboostCategoryMastersLangSerializer(rs_lang, many=True)
        return lang_data.data
class PagesSerializerNew(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPages
        fields=['id','page_name','page_title','url','meta_key','meta_data','meta_desc']

class CmsMenusNewSerializer(serializers.ModelSerializer):
    page_details = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostCmsMenus
        fields=['id','parent_id','page_id','page_details']
        #fields = '__all__'

    def get_page_details(self, EngageboostCmsMenus):
        if self.context.get('website_id'):
            website_id = self.context.get('website_id')
            page_qs = EngageboostPages.objects.filter(id=EngageboostCmsMenus.page_id,isblocked='n',isdeleted='n',company_website_id=website_id).all().iterator()
            page_data = PagesSerializerNew(page_qs,many=True)
            return page_data.data

class CategoryMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCategoryMasters
        fields = ["id","parent_id","display_order","name","description","image","thumb_image","banner_image","page_title","meta_description","meta_keywords","category_url","slug","type","is_ebay_store_category","customer_group_id","display_mobile_app","applicable_imei","isadded_in_tally"]

class CmsPageSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCmsPageSettings
        fields='__all__'

class ProductimagesnewSerializer(serializers.ModelSerializer):

    class Meta:
        model = EngageboostProductimages
        fields = ['is_cover','img']

class ProductimagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductimages
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()
    stock_data = serializers.SerializerMethodField()
    channel_price = serializers.SerializerMethodField()
    uom = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProducts
        fields = ['id','name','sku','default_price','weight','slug','veg_nonveg_type','product_image','stock_data','brand','website_id','channel_price','uom']
    
    def get_product_image(self, EngageboostProducts):
        qs = EngageboostProductimages.objects.filter(product_id=EngageboostProducts.id).all().iterator()
        product_image = ProductimagesnewSerializer(qs, many=True)
        return product_image.data

    def get_stock_data(self, EngageboostProducts):
        if self.context.get('warehouse_id'):
            warehouse_id = self.context.get('warehouse_id')
            qs_stock_data = EngageboostProductStocks.objects.filter(product_id=EngageboostProducts.id, warehouse_id=warehouse_id).first()
            products_stock = ProductStocksSerializer(qs_stock_data)
            return products_stock.data
        else:
            return {}

    def get_channel_price(self, EngageboostProducts):
        if self.context.get('warehouse_id'):
            warehouse_id = self.context.get('warehouse_id')
            qs_price_data = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=EngageboostProducts.id, warehouse_id=warehouse_id, product_price_type_id__price_type_id=1).first()
            if qs_price_data:
                return qs_price_data.price
            else:
                return 0
        else:
            return 0
    def get_uom(self, EngageboostProducts):
        # uom_data = {
        #     "uom_id":EngageboostProducts.uom,
        #     "uom_name":""
        # }
        uom_data = ""
        if EngageboostProducts.uom and EngageboostProducts.uom!="" and int(EngageboostProducts.uom)>0:
            rs_unit  = EngageboostUnitMasters.objects.filter(id = EngageboostProducts.uom).first()
            # uom_data = {
            #     "uom_id":rs_unit.id,
            #     "uom_name":rs_unit.unit_name
            # }
            uom_data = rs_unit.unit_name
        return uom_data

class BrandMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostBrandMasters
        fields = ['id', 'name','slug']

class CategoryMastersSerializer(serializers.ModelSerializer):

    class Meta:
        model = EngageboostCategoryMasters
        fields = ["id","parent_id","display_order","name","description","image","thumb_image","banner_image","page_title","meta_description","meta_keywords","category_url","slug","type","is_ebay_store_category","customer_group_id","display_mobile_app","applicable_imei","isadded_in_tally"]

class ProductStocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductStocks
        fields = ['product_id', 'real_stock', 'warehouse_id']

class ProductsViewSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    custom_field = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProducts
        fields = ['id', 'name', 'sku', 'default_price', 'brand', 'slug','veg_nonveg_type', 'mp_description', 'mp_features', 'product_image', 'custom_field','stock']

    def get_product_image(self, EngageboostProducts):
        qs = EngageboostProductimages.objects.filter(product_id=EngageboostProducts.id, is_cover=1).first()
        product_image = ProductimagesSerializer(qs)
        return product_image.data

    def get_brand(self, EngageboostProducts):
        qs = EngageboostBrandMasters.objects.filter(
            id=EngageboostProducts.brand, isblocked='n', isdeleted='n').all()
        brand = BrandMastersSerializer(qs, many=True)
        return brand.data
    def get_custom_field(self, EngageboostProducts):
        rs = EngageboostMarketplaceFieldValue.objects.filter(product_id = EngageboostProducts.id)
        rs_data = EngageboostMarketplaceFieldValueViewSerializer(rs, many = True)
        return rs_data.data
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
        qs = EngageboostProducts.objects.filter(id=EngageboostCossSellProducts.cross_product_id).all()
        coss_product = ProductsViewSerializer(qs, many=True)
        return coss_product.data


class CossSellProductsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCossSellProducts
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()
    variant_product = serializers.SerializerMethodField()
    custom_field = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    channel_price = serializers.SerializerMethodField()
    uom = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProducts
        fields = '__all__'

    def get_product_image(self, EngageboostProducts):
        qs = EngageboostProductimages.objects.filter(product_id=EngageboostProducts.id).all()
        product_image = ProductimagesSerializer(qs, many=True)
        return product_image.data
    def get_variant_product(self, EngageboostProducts):
        qs = EngageboostCossSellProducts.objects.filter(product_id=EngageboostProducts.id).all()
        coss_product = CossSellProductsSerializer(qs, many=True)
        coss_product = coss_product.data
        ret_data = []
        if coss_product:
            for crossproduct in coss_product:
                if "cross_product" in crossproduct:
                    if len(crossproduct['cross_product'])>0:
                        ret_data.append(crossproduct['cross_product'][0])
        return ret_data
    def get_custom_field(self, EngageboostProducts):
        rs = EngageboostMarketplaceFieldValue.objects.filter(product_id = EngageboostProducts.id)
        rs_data = EngageboostMarketplaceFieldValueViewSerializer(rs, many = True)
        return rs_data.data
    def get_brand(self, EngageboostProducts):
        rs = EngageboostBrandMasters.objects.filter(id=EngageboostProducts.brand).first()
        if rs:
            data = {
                "name":rs.name,
                "id":rs.id
            }
        else:
            data = {}
        return data
    def get_category(self, EngageboostProducts):
        rs = EngageboostProductCategories.objects.filter(product_id=EngageboostProducts.id).values('category_id','category_id__name', 'category_id__slug').first()
        if rs:
            data = {
                "name":rs['category_id__name'],
                "slug":rs['category_id__slug'],
                "id":rs['category_id']
            }
        else:
            data = {}
        return data
    def get_channel_price(self, EngageboostProducts):
        if self.context.get('warehouse_id'):
            warehouse_id = self.context.get('warehouse_id')
            qs_price_data = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=EngageboostProducts.id, warehouse_id=warehouse_id, product_price_type_id__price_type_id=1).first()
            if qs_price_data:
                return qs_price_data.price
            else:
                return 0
    def get_uom(self, EngageboostProducts):
        # uom_data = {
        #     "uom_id":EngageboostProducts.uom,
        #     "uom_name":""
        # }
        uom_data = ""
        if EngageboostProducts.uom and EngageboostProducts.uom!="" and int(EngageboostProducts.uom)>0:
            rs_unit  = EngageboostUnitMasters.objects.filter(id = EngageboostProducts.uom).first()
            # uom_data = {
            #     "uom_id":rs_unit.id,
            #     "uom_name":rs_unit.unit_name
            # }
            uom_data = rs_unit.unit_name
        return uom_data
class EngageboostMarketplaceFieldValueSerializer(serializers.ModelSerializer):
    product_id = serializers.SerializerMethodField()

    class Meta:
        model = EngageboostMarketplaceFieldValue
        fields = ['product_id', 'field_name', 'field_label', 'value']

    def get_product_id(self, EngageboostMarketplaceFieldValue):
        qs = EngageboostProducts.objects.filter(id=EngageboostMarketplaceFieldValue.product_id).all()
        coss_product = ProductsViewSerializer(qs, many=True)
        return coss_product.data


class EngageboostMarketplaceFieldValueViewSerializer(serializers.ModelSerializer):
    is_variant = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostMarketplaceFieldValue
        fields = ['product_id', 'field_name', 'field_label', 'value', 'is_variant']

    def get_is_variant(self, EngageboostMarketplaceFieldValue):
        rs = EngageboostDefaultsFields.objects.filter(id=EngageboostMarketplaceFieldValue.field_id).first()
        # data = {
        #     "is_variant":rs.is_variant
        # }
        if rs:
            return rs.is_variant
        else:
            return ""

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

class BasicinfoSerializer(serializers.ModelSerializer):
    customer_group  = CustomerGroupSerializer(read_only=True)
    taxclass        = ProducttaxclassesSerializer(read_only=True)
    po_taxclass     = ProducttaxclassesSerializer(read_only=True)
    max_price_rule  = ProductpriceroulSerializer(read_only=True)
    min_price_rule  = ProductpriceroulSerializer(read_only=True)
    product_images  = ProductimagesSerializer(many=True, read_only=True)
    channel_price = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProducts
        fields = '__all__'

    def get_channel_price(self, EngageboostProducts):
        if self.context.get('warehouse_id'):
            warehouse_id = self.context.get('warehouse_id')
            qs_price_data = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=EngageboostProducts.id, warehouse_id=warehouse_id, product_price_type_id__price_type_id=1).first()
            if qs_price_data:
                return qs_price_data.price
            else:
                return 0
        else:
            return 0
                
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostBrandMasters
        fields='__all__'

class CategoryBannersImagesNewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EngageboostCategoryBannersImages
        fields ='__all__'

class CategoryBannersNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCategoryBanners
        fields=['id','website_id','banner_name','category_id','order_no','banner_type','parent_id'] 

    # def get_banner_images(self, EngageboostCategoryBanners):
    #     if self.context.get('applicable_for'):
    #         applicable_for = self.context.get('applicable_for')
    #         qs_bannerimg = EngageboostCategoryBannersImages.objects.filter(category_banner_id=EngageboostCategoryBanners.id, applicable_for=applicable_for,isdeleted='n',isblocked='n').all()
    #         banner_image = CategoryBannersImagesNewSerializer(qs_bannerimg, many=True)
    #         return banner_image.data

# class EngageboostRelatedProducts(serializers.ModelSerializer)


class EngageboostUsersSerializers(serializers.ModelSerializer):  ##"""Serializers for login"""
    class Meta:
        model = EngageboostUsers
        fields = ['first_name','last_name','email','phone','image_name']
    


# class EngageboostRelatedProducts(serializers.ModelSerializer)

class CategoryBannersForPromotionSerializer(serializers.ModelSerializer):
    """serializers for category banner promotion"""
    banner_image = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostCategoryBanners
        fields=['id','website_id','banner_name','banner_type','banner_image'] 

    def get_banner_image(self, EngageboostCategoryBanners):
        bannerimage_qs =EngageboostCategoryBannersImages.objects.filter(category_banner_id=EngageboostCategoryBanners.id,isdeleted='n', isblocked='n',applicable_for='category').exclude(promotion_id__isnull=True).first()   
        bannerimage_data=CategoryBannersImagesNewSerializer(bannerimage_qs)
        return bannerimage_data.data


class EngageboostCategoriesSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostCategoryMasters
        fields=("id","parent_id","display_order","name","description","image","thumb_image","banner_image","page_title","meta_description","meta_keywords","category_url","slug","type","website_id","is_ebay_store_category","customer_group_id","display_mobile_app","show_navigation","product_count")
    def get_product_count(self, EngageboostCategoryMasters):

        # lst_cat = categorymasters.objects \
        #                 .filter(
        #                     parent_id=EngageboostCategoryMasters.id,
        #                     isdeleted='n',
        #                     isblocked='n').values_list('id',flat=True)
        warehouse_id =''
        if self.context.get("warehouse_id"):
            warehouse_id =self.context.get("warehouse_id")
        lst_cat = EngageboostCategoryWarehouse.objects.filter(category_id=EngageboostCategoryMasters.id, warehouse_id=warehouse_id).values_list("category_id",flat=True)

        if(lst_cat):
            product_lst = EngageboostProductCategories.objects.filter(category_id=EngageboostCategoryMasters.id,product__visibility_id=1,product__warehouse_id=warehouse_id, isblocked='n', isdeleted='n').values_list('product_id',flat=True)
            cnt_prod = EngageboostChannelCurrencyProductPrice.objects.filter(product_id__in = list(product_lst), warehouse_id=warehouse_id).distinct().count()
            return cnt_prod
        else:
          return 0

class MarketplaceFieldValueSerializerListing(serializers.ModelSerializer):
    class Meta:
        model = EngageboostMarketplaceFieldValue
        fields = "__all__"  

class CategoryBannersSerializer(serializers.ModelSerializer):
    # category_banners_images = CategoryBannersImagesSerializer(read_only=True)
    class Meta:
        model = EngageboostCategoryBanners
        fields='__all__'

class ProductImagesSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProductimages
        fields = '__all__'
    def get_link(self, EngageboostTempProductimages):
        return settings.IMAGE_URL   
        
class EngageboostProductsSerializer(serializers.ModelSerializer):
    product_images = ProductImagesSerializer(many=True)
    variant_product = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProducts
        fields=("id","name","sku","brand","weight","visibility_id","default_price","slug","twitter_addstatus","amazon_addstatus", "ean", "description", "product_images", 'variant_product')
    def get_variant_product(self, EngageboostProducts):
        qs = EngageboostCossSellProducts.objects.filter(product_id=EngageboostProducts.id).all()
        coss_product = CossSellProductsSerializer(qs, many=True)
        coss_product = coss_product.data
        ret_data = []
        if coss_product:
            for crossproduct in coss_product:
                if "cross_product" in crossproduct:
                    if len(crossproduct['cross_product'])>0:
                        ret_data.append(crossproduct['cross_product'][0])
        return ret_data
 
class CategoriesSerializer(serializers.ModelSerializer):
    lang_data = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostCategoryMasters
        # fields = ('id','lft','rght','check_id','createdby', 'parent_id', 'name','isblocked','description','display_order','customer_group_id','applicable_imei','page_title','meta_keywords','website_id','image','thumb_image','banner_image','display_mobile_app','created','modified')
        fields='__all__'
    def get_lang_data(self, EngageboostCategoryMasters):
        # if EngageboostCategoryMasters['id']:
        #     c_id=EngageboostCategoryMasters['id']
        # else:
        #     c_id=EngageboostCategoryMasters.id
        rs_lang = EngageboostCategoryMastersLang.objects.filter(category_id=EngageboostCategoryMasters.id, isblocked='n', isdeleted='n').all()
        lang_data = EngageboostCategoryMastersLangSerializer(rs_lang, many=True)
        return lang_data.data

class ProductCategoriesSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()
    # product = EngageboostProductsSerializer()
    category = CategoriesSerializer()
    class Meta:
        model = EngageboostProductCategories
        # fields = ('id','is_parent','category_id','product_id','isblocked','isdeleted','created','createdby','ip_address','modified','updatedby','parent_id')
        fields='__all__'


class EngageboostUsersNewSerializers(serializers.ModelSerializer):  ##"""Serializers for MyProfile"""
    class Meta:
        model = EngageboostUsers
        fields = ['first_name','last_name','email','phone']
    

class ShippingMastersSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostShippingMastersSettings
        fields='__all__'
        
class EngageboostTemporaryShoppingCartsSerializer(serializers.ModelSerializer):
    product_id = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostTemporaryShoppingCarts
        fields = "__all__"

    def get_product_id(self, EngageboostTemporaryShoppingCarts):
        if self.context.get('warehouse_id'):
            warehouse_id = self.context.get('warehouse_id')

        qs = EngageboostProducts.objects.filter(id=EngageboostTemporaryShoppingCarts.product_id, isblocked='n', isdeleted='n').first()
        cart_product = ProductsViewSerializer(qs, context={'warehouse_id': warehouse_id})
        cart_product = cart_product.data
        if self.context.get('warehouse_id'):
            warehouse_id = self.context.get('warehouse_id')
            qs_price_data = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=EngageboostTemporaryShoppingCarts.product_id, warehouse_id=warehouse_id, product_price_type_id__price_type_id=1).first()
            if qs_price_data:
                cart_product.update({"channel_price":qs_price_data.price})
            else:
                cart_product['channel_price']=0

        return cart_product

    def get_weight(self, EngageboostTemporaryShoppingCarts):
        qs = EngageboostProducts.objects.filter(id=EngageboostTemporaryShoppingCarts.product_id, isblocked='n',isdeleted='n').first()
        if qs:
            return qs.weight
        else:
            return ''

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostOrderProducts
        fields=['id','order_id','product_id', 'quantity']
        
class EngageboostOrdermasterSerializers(serializers.ModelSerializer):  ##"""Serializers for Order History"""
    order_products  = OrderProductSerializer(many=True)
    customer_details = serializers.SerializerMethodField()
    warehouse_name = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostOrdermaster
        fields = '__all__'
    def get_customer_details(self, EngageboostOrdermaster):
        rs_customer = EngageboostCustomers.objects.filter(id = EngageboostOrdermaster.customer_id).first()
        customer_data = CustomerViewSerializer(rs_customer).data
        return customer_data

    def get_warehouse_name(self, EngageboostOrdermaster):
        rs_warehouse = EngageboostWarehouseMasters.objects.filter(id = EngageboostOrdermaster.assign_wh).first()
        warehouse_data = rs_warehouse.name
        return warehouse_data
    # def get_order_product(self, EngageboostOrdermaster):
    #     qs = EngageboostProducts.objects.filter(order_id=EngageboostOrdermaster.id, isblocked='n', isdeleted='n')
    #     cart_product = ProductsViewSerializer(qs)
    #     return cart_product.data
        
class PaymentgatewaySettingInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPaymentgatewaySettingInformation
        fields = '__all__'

class WebsitePaymentmethodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostWebsitePaymentmethods
        fields = '__all__'

class DeliverySlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDeliverySlot
        fields = '__all__'

class CustomersAddressBookSerializer(serializers.ModelSerializer):
    billing_state_name = serializers.SerializerMethodField()
    delivery_state_name = serializers.SerializerMethodField()
    billing_country_name = serializers.SerializerMethodField()
    delivery_country_name = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostCustomersAddressBook
        fields ='__all__'
    def get_billing_state_name(self, EngageboostCustomersAddressBook):
        if EngageboostCustomersAddressBook.billing_state:
            rs = EngageboostStates.objects.filter(id=int(EngageboostCustomersAddressBook.billing_state)).first()
            if rs:
                return rs.state_name
            else:
                return ""
        else:
            return ""
    def get_delivery_state_name(self, EngageboostCustomersAddressBook):
        if EngageboostCustomersAddressBook.billing_state:
            rs = EngageboostStates.objects.filter(id=int(EngageboostCustomersAddressBook.billing_state)).first()
            if rs:
                return rs.state_name
            else:
                return ""
        else:
            return ""
    def get_billing_country_name(self, EngageboostCustomersAddressBook):
        if EngageboostCustomersAddressBook.billing_country:
            rs = EngageboostCountries.objects.filter(id=int(EngageboostCustomersAddressBook.billing_country)).first()
            if rs:
                return rs.country_name
            else:
                return ""
        else:
            return ""

    def get_delivery_country_name(self, EngageboostCustomersAddressBook):
        if EngageboostCustomersAddressBook.delivery_country:
            rs = EngageboostCountries.objects.filter(id=int(EngageboostCustomersAddressBook.delivery_country)).first()
            if rs:
                return rs.country_name
            else:
                return ""
        else:
            return ""
            
class EngageboostCountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCountries
        fields ='__all__'

class EngageboostStatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostStates
        fields ='__all__'

class EmailTypeContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostEmailTypeContents
        fields='__all__'

class ApplicableAutorespondersSerializer(serializers.ModelSerializer):
    auto_responder=EmailTypeContentsSerializer()
    class Meta:
        model = EngageboostApplicableAutoresponders
        fields='__all__'

class EngageboostMysavelistSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostMysavelist
        #fields=['id','user_id','savelist_name', 'product_ids']
        fields='__all__'

class ChannelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostChannels
        fields='__all__'

class CustomerViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCustomers
        fields=("id","first_name","last_name","ebayusername","address","country_id","group_id","email","phone","vat","tin","excise_regn_no")

class EngageboostProductsViewOrderSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()
    uom = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProducts
        fields=("id","name","sku","weight","visibility_id","default_price","slug","twitter_addstatus","amazon_addstatus", "ean", "product_image", "uom")
    def get_product_image(self, EngageboostProducts):
        qs = EngageboostProductimages.objects.filter(product_id=EngageboostProducts.id, is_cover=1).first()
        product_image = ProductimagesnewSerializer(qs)
        return product_image.data
    
    def get_uom(self, EngageboostProducts):
        uom_data = {
            "uom_id":EngageboostProducts.uom,
            "uom_name":""
        }
        uom_data = ""
        if EngageboostProducts.uom and EngageboostProducts.uom!="" and int(EngageboostProducts.uom)>0:
            rs_unit  = EngageboostUnitMasters.objects.filter(id = EngageboostProducts.uom).first()
            uom_data = {
                "uom_id":rs_unit.id,
                "uom_name":rs_unit.unit_name
            }
        return uom_data

class OrderProductsViewOrderSerializer(serializers.ModelSerializer):
    product=EngageboostProductsViewOrderSerializer()
    invoice_product = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    new_default_price = serializers.SerializerMethodField()
    new_default_price_unit = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostOrderProducts
        fields='__all__'
    
    def get_invoice_product(self, EngageboostOrderProducts):
        rs = EngageboostInvoiceProducts.objects.filter(order_id=EngageboostOrderProducts.order_id, product_id=EngageboostOrderProducts.product_id)
        quantity = 0
        if rs.count()>0:
            rs  = rs.first()
            quantity = rs.quantity
        return quantity
    def get_new_default_price_unit(self, EngageboostOrderProducts):
        product_price = EngageboostOrderProducts.product_price
        product_price = float(product_price)
        return product_price

    def get_new_default_price(self, EngageboostOrderProducts):
        product_price = EngageboostOrderProducts.product_price
        quantity = EngageboostOrderProducts.quantity
        deleted_quantity = EngageboostOrderProducts.deleted_quantity
        return_quantity = EngageboostOrderProducts.returns
        shortage_quantity = EngageboostOrderProducts.shortage
        quantity = int(quantity)-int(deleted_quantity)-int(return_quantity)-int(shortage_quantity)
        product_price = float(product_price)*float(quantity)
        return product_price
    def get_quantity(self, EngageboostOrderProducts):
        quantity = EngageboostOrderProducts.quantity
        deleted_quantity = EngageboostOrderProducts.deleted_quantity
        if EngageboostOrderProducts.shortage:
            shortage = EngageboostOrderProducts.shortage
        else:
            shortage = 0
        if EngageboostOrderProducts.returns:
            returns = EngageboostOrderProducts.returns
        else:
            returns = 0
        total_quantity = int(quantity)-int(deleted_quantity)-int(shortage)-int(returns)
        if EngageboostOrderProducts.grn_quantity > 0:
            total_quantity = EngageboostOrderProducts.grn_quantity
        if total_quantity and total_quantity > 0:
            pass
        else:
            total_quantity = 0
        return total_quantity

class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model= EngageboostOrderPaymentDetails
        fields = '__all__'

class WarehousemastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostWarehouseMasters
        fields='__all__'

class ViewOrderSerializer(serializers.ModelSerializer):
    customer        = CustomerViewSerializer(read_only = True)
    webshop         = ChannelsSerializer(read_only = True)
    order_products = serializers.SerializerMethodField()
    # zone_name       = serializers.SerializerMethodField()
    order_payment   = serializers.SerializerMethodField()
    warehouse       = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostOrdermaster
        fields='__all__'

    # def get_zone_name(self, EngageboostOrdermaster):
    #     rs = EngageboostZoneMasters.objects.filter(id=EngageboostOrdermaster.zone_id).first()
    #     zone_name = ""
    #     if rs:
    #         rs_data = ZoneMastersSerializer(rs)
    #         rs_data = rs_data.data
    #         zone_name = rs_data['name']
    #         return zone_name
    #     else:
    #         return zone_name

    def get_order_payment(self, EngageboostOrdermaster):
        rs = EngageboostOrderPaymentDetails.objects.filter(order_id_id=EngageboostOrdermaster.id).all().order_by('-id')
        serializer = OrderPaymentSerializer(rs, many=True)
        return serializer.data
    def get_warehouse(self, EngageboostOrdermaster):
        rs = EngageboostWarehouseMasters.objects.filter(website_id=EngageboostOrdermaster.website_id,isblocked='n',isdeleted='n').all().order_by('-id')
        serializer = WarehousemastersSerializer(rs, many=True)
        return serializer.data
    def get_order_products(self, EngageboostOrdermaster):
        if EngageboostOrdermaster.order_status in (0,999,21,100):
            rs = EngageboostOrderProducts.objects.filter(order_id=EngageboostOrdermaster.id)
        else:
            rs = EngageboostOrderProducts.objects.filter(order_id=EngageboostOrdermaster.id, grn_quantity__gt=0)

        # rs = EngageboostOrderProducts.objects.filter(order_id=EngageboostOrdermaster.id, grn_quantity__gt=0)
        serializer = OrderProductsViewOrderSerializer(rs, many=True)
        return serializer.data

class WishlistsProductsSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()
    custom_field = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    channel_price = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProducts
        fields = ['id','name','slug','default_price','website_id','product_image','custom_field','brand','channel_price']

    def get_product_image(self, EngageboostProducts):
        qs = EngageboostProductimages.objects.filter(product_id=EngageboostProducts.id, status=0).all()
        product_image = ProductimagesSerializer(qs, many=True)
        return product_image.data

    def get_custom_field(self, EngageboostProducts):
        rs = EngageboostMarketplaceFieldValue.objects.filter(product_id = EngageboostProducts.id)
        rs_data = EngageboostMarketplaceFieldValueViewSerializer(rs, many = True)
        return rs_data.data
    def get_brand(self, EngageboostProducts):
        rs = EngageboostBrandMasters.objects.filter(id=EngageboostProducts.brand).first()
        if rs:
            data = {
                "name":rs.name,
                "id":rs.id
            }
        else:
            data = {}
        return data

    def get_channel_price(self, EngageboostProducts):
        if self.context.get('warehouse_id'):
            warehouse_id = self.context.get('warehouse_id')
            qs_price_data = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=EngageboostProducts.id, warehouse_id=warehouse_id).first()
            if qs_price_data:
                data ={
                    "channel_price":qs_price_data.price,
                    "warehouse_id":qs_price_data.warehouse_id
                }
                # return qs_price_data.price
            else:
                data = {}
            return data

class WishlistsSerializer(serializers.ModelSerializer):
    product = WishlistsProductsSerializer()
    class Meta:
        model = EngageboostWishlists
        fields='__all__'

class PaymentMethodListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPaymentgatewayTypes
        fields='__all__'

class PaymentgatewayMethodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPaymentgatewayMethods
        fields='__all__'

class PaymentgatewaySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPaymentgatewaySettings
        fields='__all__'

class WebsitePaymentmethodsViewSerializer(serializers.ModelSerializer):
    engageboost_paymentgateway_method_id = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostWebsitePaymentmethods
        fields = ['id', 'engageboost_paymentgateway_method_id']

    def get_engageboost_paymentgateway_method_id(self, EngageboostWebsitePaymentmethods):
        rs_method = EngageboostPaymentgatewayMethods.objects.filter(id=EngageboostWebsitePaymentmethods.engageboost_paymentgateway_method_id).first()
        data = PaymentgatewayMethodsSerializer(rs_method).data
        return data


class EngageboostProductsByBrandSlugSerializers(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProducts
        fields='__all__'

class EngageboostInvoiceProductsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostInvoiceProducts
        fields = '__all__'

class EngageboostCreditPointConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCreditPointConditions
        # fields=["id","custom_order_id","created","gross_amount_base","paid_amount","net_amount","customer","order_status","buy_status"]
        fields =  '__all__'

class EngageboostCreditPointSerializer(serializers.ModelSerializer):
    CreditPointConditions  = EngageboostCreditPointConditionsSerializer(read_only=True, many=True)
    class Meta:
        model = EngageboostCreditPoint
        # fields=["id","custom_order_id","created","gross_amount_base","paid_amount","net_amount","customer","order_status","buy_status"]
        fields =  '__all__'


class EngageboostCustomerLoyaltypointsSerializer(serializers.ModelSerializer):
    # CreditPointConditions  = EngageboostCreditPointConditionsSerializer(read_only=True, many=True)
    class Meta:
        model = EngageboostCustomerLoyaltypoints
        # fields=["id","custom_order_id","created","gross_amount_base","paid_amount","net_amount","customer","order_status","buy_status"]
        fields =  '__all__'


class OrderProductForSavelistDetails(serializers.ModelSerializer):
    #product = EngageboostProductsViewOrderSerializer()
    class Meta:
        model = EngageboostOrderProducts
        fields='__all__'

class SavelistDetailsSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    channel_price = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProducts
        fields=["id","name","sku","weight","visibility_id","default_price","slug","twitter_addstatus","amazon_addstatus", "ean", "product_image","product", "channel_price"]
        
    def get_product_image(self, EngageboostProducts):
        qs = EngageboostProductimages.objects.filter(product_id=EngageboostProducts.id, is_cover=1).all()
        product_image = ProductimagesnewSerializer(qs,many=True)
        return product_image.data

    def get_product(self, EngageboostProducts):
        qs = EngageboostOrderProducts.objects.filter(product_id=EngageboostProducts.id).first()
        order_details = OrderProductForSavelistDetails(qs)
        return order_details.data

    def get_channel_price(self, EngageboostProducts):
        if self.context.get('warehouse_id'):
            warehouse_id = self.context.get('warehouse_id')
            qs_price_data = EngageboostChannelCurrencyProductPrice.objects.filter(product_id=EngageboostProducts.id, warehouse_id=warehouse_id, product_price_type_id__price_type_id=1).first()
            if qs_price_data:
                return qs_price_data.price
            else:
                return 0
        else:
            return 0

class EngageboostProductReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductReviews
        fields = "__all__"

class EngageboostCurrencyMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCurrencyMasters
        fields = "__all__"

class GlobalsettingCurrenciesSerializer(serializers.ModelSerializer):
    currency_data = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostGlobalsettingCurrencies
        fields = "__all__"
    def get_currency_data(self, EngageboostGlobalsettingCurrencies):
        qs = EngageboostCurrencyMasters.objects.filter(id=EngageboostGlobalsettingCurrencies.currency_id).first()
        currency = EngageboostCurrencyMastersSerializer(qs)
        return currency.data

class EmktContactserializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostEmktContacts
        fields = "__all__"

class GlobalSettingserializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostGlobalSettings
        fields = "__all__"

class AppVersionControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAppVersionControl
        fields = ("id", "version_a", "version_i", "picking_android", "is_mandatory", "upgrade_to", "appstore_check")