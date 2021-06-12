from rest_framework import serializers
from .models import *
import json
from django.db.models import Q
from django.db.models.functions import Cast
from django.db.models.functions import Concat
from django.db.models import Value
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostRolemasters
        fields='__all__'

class GlobalsettingscountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCountries
        fields='__all__'

class StatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostStates
        fields='__all__'  

class UserSerializer(serializers.ModelSerializer):
    role=RoleSerializer()
    country=GlobalsettingscountriesSerializer()
    class Meta:
        model = EngageboostUsers
        fields='__all__'
        search_fields = ('first_name')
        depth = 1

class EmailTypeContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostEmailTypeContents
        fields='__all__'

class ApplicableAutorespondersSerializer(serializers.ModelSerializer):
    auto_responder=EmailTypeContentsSerializer()
    class Meta:
        model = EngageboostApplicableAutoresponders
        fields='__all__'

class CustomerGroupSerializer(serializers.ModelSerializer):
    customers = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostCustomerGroup
        fields='__all__'
    def get_customers(self, EngageboostCustomerGroup):
        cust_ids = EngageboostCustomerGroup.customer_ids
        if cust_ids!=None and cust_ids!="":
            ids = cust_ids.split(',')
            rs = EngageboostCustomers.objects.filter(id__in=ids, isblocked='n', isdeleted='n').values_list('email', flat=True)
            return rs

class ProducttaxclassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductTaxClasses
        fields='__all__'

class WarehousemastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostWarehouseMasters
        fields='__all__'

class ProductpriceroulSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostRepricingMaximumMinRules
        fields='__all__'

class HsnCodeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostHsnCodeMaster
        fields='__all__'

class ProductImagesSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProductimages
        fields = '__all__'
    def get_link(self, EngageboostTempProductimages):
        return settings.IMAGE_URL

class EngageboostProductMastersLangSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductMastersLang
        fields = '__all__'

class StockViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductStocks
        fields='__all__'

class BasicinfoSerializer(serializers.ModelSerializer):
    customer_group = CustomerGroupSerializer(read_only=True)
    taxclass = ProducttaxclassesSerializer(read_only=True)
    po_taxclass = ProducttaxclassesSerializer(read_only=True)
    max_price_rule = ProductpriceroulSerializer(read_only=True)
    min_price_rule = ProductpriceroulSerializer(read_only=True)
    product_images = ProductImagesSerializer(many=True, read_only=True)
    channel_currency_product_price = serializers.SerializerMethodField()
    lang_data = serializers.SerializerMethodField()
    uom_name = serializers.SerializerMethodField()
    product_stock = StockViewSerializer(many=True, read_only=True)
    category_id = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProducts
        fields='__all__'
    def get_channel_currency_product_price(self, EngageboostProducts):
        rs = EngageboostChannelCurrencyProductPrice.objects.filter(product_id = EngageboostProducts.id).all()
        if self.context.get("channel_id"):
            rs = rs.filter(channel_id=self.context.get("channel_id"))
        if self.context.get("currency_id"):
            rs = rs.filter(currency_id=self.context.get("currency_id"))
        serializar_data = ChannelCurrencyProductPriceSerializer(rs, many=True)
        return serializar_data.data
    def get_lang_data(self, EngageboostProducts):
        rs_lang = EngageboostProductMastersLang.objects.filter(product_id=EngageboostProducts.id, isblocked='n', isdeleted='n').all()
        lang_data = EngageboostProductMastersLangSerializer(rs_lang, many=True)
        return lang_data.data
    def get_uom_name(self, EngageboostProducts):
        UOM = EngageboostProducts.uom
        if UOM is not None:
            if UOM.isnumeric()==True:
                rs_uom = EngageboostUnitMasters.objects.filter(id=int(EngageboostProducts.uom), isblocked='n', isdeleted='n').first()
                if rs_uom:
                    return rs_uom.unit_name
                else:
                    return ''
            else:
                rs_uom = EngageboostUnitMasters.objects.filter(unit_name=EngageboostProducts.uom, isblocked='n', isdeleted='n').first()
                if rs_uom:
                    return rs_uom.unit_name
                else:
                    return ''
        else:
            return ''
    def get_category_id(self, EngageboostProducts):
        rs = EngageboostProductCategories.objects.filter(product_id=EngageboostProducts.id).values('category_id','category_id__name', 'category_id__slug').first()
        if rs:
            # data = {
            #     "name":rs['category_id__name'],
            #     "slug":rs['category_id__slug'],
            #     "id":rs['category_id']
            # }
            data = rs['category_id']
        else:
            data = ""
        return data

class EngageboostProductsSerializer(serializers.ModelSerializer):
    product_images = ProductImagesSerializer(many=True)
    ean = serializers.SerializerMethodField()
    uom = serializers.SerializerMethodField()
    custom_fields = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProducts
        fields=("id","name","sku","brand","weight","visibility_id","default_price","slug","twitter_addstatus","amazon_addstatus", "ean", "description", "product_images","uom", "custom_fields")
    def get_ean(self, EngageboostProducts):
        rs = EngageboostMultipleBarcodes.objects.filter(product_id=EngageboostProducts.id, isblocked='n', isdeleted='n').first()
        barcode = ""
        if rs:
            barcode = rs.barcode
        return barcode
    def get_uom(self, EngageboostProducts):
        rs = EngageboostUnitMasters.objects.filter(id=EngageboostProducts.uom, isblocked='n', isdeleted='n').first()
        uom = {}
        uom_name = ""
        uom_full_name = ""
        if rs:
            uom_name = rs.unit_name
            uom_full_name = rs.unit_full_name
        uom = {
            "uom_name":uom_name,
            "uom_full_name":uom_full_name
        }
        return uom

    def get_custom_fields(self, EngageboostProducts):
        channel_id = '6'
        # product_categories = EngageboostProductCategories.objects.filter(product_id=EngageboostProducts.id, isblocked='n', isdeleted='n').first()
        # custom_fields_data = EngageboostDefaultModuleLayoutFields.objects.using(company_db).all().filter(
        #     category_id=product_categories.category_id).filter(
        #     Q(show_market_places__startswith=channel_id + ',') | Q(show_market_places__endswith=',' + channel_id) | Q(
        #         show_market_places__contains=',{0},'.format(channel_id)) | Q(
        #         show_market_places__exact=channel_id)).order_by('section_row', 'section_col')

        # custom_fields_data = EngageboostDefaultModuleLayoutFields.objects.all().filter(
        #     category_id=product_categories.category_id,is_system='y').filter(
        #     Q(show_market_places__startswith=channel_id+',') | Q(show_market_places__endswith=','+channel_id) | Q(
        #         show_market_places__contains=',{0},'.format(channel_id)) | Q(show_market_places__exact=channel_id) ).order_by('section_row','section_col')

        custom_fields_data = EngageboostMarketplaceFieldValue.objects.all().filter(product_id=EngageboostProducts.id)
        serializer_productcustom = MarketplaceFieldValueSerializer(custom_fields_data, many=True)

        custom_fields = []
        for field in serializer_productcustom.data:
            # print('################----->', field['id'])
            data = {
                "field_id": field['id'],
                "field_label": field['field_label'],
                "field_label_l": field['field_label'],
                "field_name": field['field_name'],
                "value": field['value']
            }

            custom_fields.append(data)
        return custom_fields

class CategoriesReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCategoryMasters
        fields = ['id', 'name']

class EngageboostProductsCategoriesSerializerReport(serializers.ModelSerializer):
    category = CategoriesReportSerializer()
    class Meta:
            model = EngageboostProductCategories
            fields=("id","category","product_id")

class EngageboostProductsSerializerListView(serializers.ModelSerializer):
    # product_list = EngageboostProductsCategoriesSerializerReport(many=True)
    product_category = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProducts
        fields=("id","name","sku","brand","weight","visibility_id","default_price","slug", "product_category")
        read_only_fields = fields
        
    def get_product_category(self, EngageboostProducts):
        rs_cat = EngageboostProductCategories.objects.filter(product_id = EngageboostProducts.id, isblocked='n', isdeleted='n').first()
        if rs_cat:
            ret_cat_data = recv_cat(rs_cat.category_id)
            return ret_cat_data

def recv_cat(cat_id):
    ret_cat_name = ""
    ret_cat_id = cat_id
    rs_ca_master = EngageboostCategoryMasters.objects.filter(id = cat_id, isblocked='n', isdeleted='n').first()
    if rs_ca_master and rs_ca_master.parent_id is not None:
        if int(rs_ca_master.parent_id) >0:
            data = recv_cat(rs_ca_master.parent_id)
        else:
            ret_cat_id = rs_ca_master.id
            ret_cat_name = rs_ca_master.name
            data = {"ret_cat_id":ret_cat_id, "ret_cat_name":ret_cat_name}
    else:
        # print("k1==========", cat_id)
        rs_ca_master = EngageboostCategoryMasters.objects.filter(id = cat_id).first()
        if int(rs_ca_master.parent_id) >0:
            data = recv_cat(rs_ca_master.parent_id)
        else:
            ret_cat_id = rs_ca_master.id
            ret_cat_name = rs_ca_master.name
            data = {"ret_cat_id":ret_cat_id, "ret_cat_name":ret_cat_name}

    return data
        
class CustomerSerializer(serializers.ModelSerializer):
    auth_user=UserSerializer()
    country=GlobalsettingscountriesSerializer()
    customer_group=CustomerGroupSerializer()
    class Meta:
        model = EngageboostCustomers
        fields='__all__'
        depth =1

class CustomerListViewSerializer(serializers.ModelSerializer):
    auth_user=UserSerializer(read_only=True)
    country=GlobalsettingscountriesSerializer(read_only=True)
    customer_group=CustomerGroupSerializer(read_only=True)
    class Meta:
        model = EngageboostCustomers
        fields='__all__'
        depth =1

class CustomerViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCustomers
        fields=("id","first_name","last_name","address","country_id","group_id","email","phone","vat")

class CustomersAddressBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCustomersAddressBook
        fields='__all__'

class CustomerActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCustomerActivities
        fields='__all__'

class CustomerLoyaltypointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCustomerLoyaltypoints
        fields='__all__'

class CustomerReturnStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCustomerReturnStatus
        fields='__all__'

class CustomerTaxClassesSerializer(serializers.ModelSerializer):
    customer_group = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostCustomerTaxClasses
        fields='__all__'

    def get_customer_group(self, EngageboostCustomerTaxClasses):
        rs = EngageboostCustomerGroup.objects.filter(id=EngageboostCustomerTaxClasses.customer_type, isblocked='n', isdeleted='n').all()
        podata = CustomerGroupSerializer(rs, many=True)
        return podata.data    

# class CustomerWiselistsSerializer(serializers.ModelSerializer):
#     product=EngageboostProductsSerializer()
#     class Meta:
#         model = EngageboostCustomerWiselists
#         fields='__all__'

class ChannelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostChannels
        fields=("id","name","image","website_name")
        # fields='__all__'

class ChannelCategoryMappingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostChannelCategoryMappings
        fields='__all__'

class ChannelCurrencyProductPriceSerializer(serializers.ModelSerializer):
    promotions = serializers.SerializerMethodField()
    price_type = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostChannelCurrencyProductPrice
        fields='__all__'
    def get_promotions(self,EngageboostChannelCurrencyProductPrice):
        discountsObj = EngageboostDiscountMasters.objects.filter(product_id=EngageboostChannelCurrencyProductPrice.product_id,warehouse_id=EngageboostChannelCurrencyProductPrice.warehouse_id,isdeleted="n",isblocked="n")   
        if discountsObj.count()>0:
            discounts = discountsObj.all()
            discounts_data = DiscountMasterSerializer(discounts,many=True)
            return discounts_data.data
    def get_price_type(self,EngageboostChannelCurrencyProductPrice):
        type_id = None
        if(EngageboostChannelCurrencyProductPrice.product_price_type):
            objprice_type = EngageboostProductPriceTypeMaster.objects.filter(id=EngageboostChannelCurrencyProductPrice.product_price_type.id).first()
            if(objprice_type):
                type_id = int(objprice_type.price_type.id)
        return type_id

class ChannelCurrencyProductPriceImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostChannelCurrencyProductPrice
        fields='__all__'

class TempProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTempProductPrice
        fields='__all__'

# class ChannelErrorsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostChannelErrors
#         fields='__all__'

# class ChannelItemlistingfeesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostChannelItemlistingfees
#         fields='__all__'

# class ChannelOrdertransactionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostChannelOrdertransactions
#         fields='__all__'

# class ChannelSettingsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostChannelSettings
#         fields='__all__'

# class ChannelShippingMapsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostChannelShippingMaps
#         fields='__all__'

# class ChannelShippingservicesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostChannelShippingservices
#         fields='__all__'

# class ChannelSitesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostChannelSites
#         fields='__all__'

# class ChannelSkuSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostChannelSku
#         fields='__all__'

class ChannelUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostChannelUsers
        fields='__all__'

class TaxclassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductTaxClasses
        fields='__all__'

class OrderProductsSerializer(serializers.ModelSerializer):
    product     = EngageboostProductsSerializer()
    class Meta:
        model = EngageboostOrderProducts
        fields='__all__'

class OrderSubstituteProductsSerializer(serializers.ModelSerializer):
    product     = EngageboostProductsSerializer()
    class Meta:
        model = EngageboostOrderSubstituteProducts
        fields='__all__'

class OrderProductsSerializerListView(serializers.ModelSerializer):
    product     = EngageboostProductsSerializerListView()
    class Meta:
        model = EngageboostOrderProducts
        fields= ['quantity', 'deleted_quantity', 'shortage', 'returns', 'grn_quantity','product_price','product_discount_price','product']
        read_only_fields = fields

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPurchaseOrders
        fields='__all__'
class PurchaseOrderProductSerializer(serializers.ModelSerializer):
    PO_receive_pro_details = serializers.SerializerMethodField()
    product=EngageboostProductsSerializer()
    class Meta:
        model = EngageboostPurchaseOrderProducts
        fields='__all__'
        depth=1

    def get_PO_receive_pro_details(self, EngageboostPurchaseOrderProducts):
        rs = EngageboostPurchaseOrderReceivedProductDetails.objects.filter(purchase_order_id=EngageboostPurchaseOrderProducts.purchase_order_id, purchase_order_product_id=EngageboostPurchaseOrderProducts.product_id).order_by('-expiry_date').all()
        podata = EngageboostPurchaseOrderReceivedProductDetailsSerializer(rs, many=True)
        return podata.data

class OrderMasterSerializer(serializers.ModelSerializer):
    customer        = CustomerViewSerializer()
    webshop         = ChannelsSerializer()
    order_products  = OrderProductsSerializer(many=True)
    zone_name       = serializers.SerializerMethodField()
    shipping_status = serializers.SerializerMethodField()
    webshop_id = serializers.SerializerMethodField()
    CustomersAddressBook = serializers.SerializerMethodField()
    time_slot = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostOrdermaster
        fields='__all__'
    def get_zone_name(self, EngageboostOrdermaster):
        rs = EngageboostZoneMasters.objects.filter(id=EngageboostOrdermaster.zone_id).first()
        zone_name = ""
        if rs:
            rs_data = ZoneMastersSerializer(rs)
            rs_data = rs_data.data
            zone_name = rs_data['name']
            return zone_name
        else:
            return zone_name
    def get_shipping_status(self, EngageboostOrdermaster):
        shipping_status = "Pending"
        if EngageboostOrdermaster.trent_picklist_id is not None and EngageboostOrdermaster.trent_picklist_id>0:
            rs = EngageboostShipmentOrders.objects.filter(trent_picklist_id=EngageboostOrdermaster.trent_picklist_id).first()
            if rs:
                shipping_status = rs.shipment_status
        return shipping_status
    def get_CustomersAddressBook(self, EngageboostOrdermaster):
        data = []
        if EngageboostOrdermaster.address_book_id is not None and EngageboostOrdermaster.address_book_id>0:
            rs = EngageboostCustomersAddressBook.objects.filter(id=EngageboostOrdermaster.address_book_id)
            if rs.count()>0:
                rs = rs.values('id','customers_id','long_val','lat_val').first()
                rs_data = CustomersAddressBookSerializer(rs)
                data = rs_data.data
        return data
    def get_webshop_id(self, EngageboostOrdermaster):
        return EngageboostOrdermaster.webshop_id
    def get_time_slot(self, EngageboostOrdermaster):
        time_slot_id = EngageboostOrdermaster.time_slot_id
        if time_slot_id:
            time_slot_id = time_slot_id.replace(" ", "")
            time_slot_id = time_slot_id.lower()
            times = time_slot_id.split('-')
            try:
                if ":" in times[0]:
                    start = datetime.strptime(times[0], "%I:%M%p")
                    start = datetime.strftime(start, "%I:%M%p")
                else:
                    start = datetime.strptime(times[0], "%I%p")
                    start = datetime.strftime(start, "%I:%M%p")
                if ":" in times[1]:
                    end = datetime.strptime(times[1], "%I:%M%p")
                    end = datetime.strftime(end, "%I:%M%p")
                else:
                    end = datetime.strptime(times[1], "%I%p")
                    end = datetime.strftime(end, "%I:%M%p") 
            except:
                if ":" in times[0]:
                    start = datetime.strptime(times[0], "%H:%M%p")
                    start = datetime.strftime(start, "%H:%M%p")
                else:
                    start = datetime.strptime(times[0], "%H%p")
                    start = datetime.strftime(start, "%H:%M%p")
                if ":" in times[1]:
                    end = datetime.strptime(times[1], "%H:%M%p")
                    end = datetime.strftime(end, "%H:%M%p")
                else:
                    end = datetime.strptime(times[1], "%H%p")
                    end = datetime.strftime(end, "%H:%M%p")
            time_slot_id = str(start)+"-"+str(end)
            time_slot_id = time_slot_id.lower()
            time_slot_id = time_slot_id.replace("-","")
            time_slot_id = time_slot_id.replace(":","")
        return time_slot_id


class OrderMasterSerializerList(serializers.ModelSerializer):
    customer        = CustomerViewSerializer()
    webshop         = ChannelsSerializer()
    # order_products  = OrderProductsSerializerListView(many=True)
    zone_name       = serializers.SerializerMethodField()
    shipping_status = serializers.SerializerMethodField()
    webshop_id = serializers.SerializerMethodField()
    CustomersAddressBook = serializers.SerializerMethodField()
    time_slot = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostOrdermaster
        fields= ["id","time_slot", "website_id", "company_id", "custom_order_id", "payment_method_id", "payment_type_id", "payment_method_name", "shipping_method_id", "delivery_name", "address_book_id", "delivery_company", "delivery_email_address", "delivery_street_address", "delivery_street_address1", "delivery_city", "delivery_postcode", "delivery_state", "delivery_country", "delivery_phone", "delivery_fax", "custom_msg", "applied_coupon", "gross_amount", "net_amount", "shipping_cost", "paid_amount", "gross_discount_amount", "tax_amount", "gross_amount_base", "net_amount_base", "paid_amount_base", "gross_discount_amount_base", "order_status", "buy_status", "currency_code", "ip_address", "created", "modified", "cart_discount", "response_msg", "cod_charge", "send_notes", "received_status", "pay_wallet_amount", "refund_wallet_amount", "assign_to", "assign_wh", "tags", "pay_txntranid", "pay_txndate", "return_note", "delivery_date", "dispatch_date", "shipment_id", "zone_id", "time_slot_date", "time_slot_id", "slot_start_time", "slot_end_time", "return_status", "flag_order", "area_id", "grn_created_date","isblocked", "isdeleted", "trent_picklist_id","customer", "webshop", "zone_name", "shipping_status", "webshop_id", "CustomersAddressBook", "time_slot"]
        read_only_fields = fields
        # fields="__all__"
    def get_zone_name(self, EngageboostOrdermaster):
        rs = EngageboostZoneMasters.objects.filter(id=EngageboostOrdermaster.zone_id).first()
        zone_name = ""
        if rs:
            rs_data = ZoneMastersSerializer(rs)
            rs_data = rs_data.data
            zone_name = rs_data['name']
            return zone_name
        else:
            return zone_name
    def get_shipping_status(self, EngageboostOrdermaster):
        shipping_status = "Pending"
        if EngageboostOrdermaster.trent_picklist_id is not None and EngageboostOrdermaster.trent_picklist_id>0:
            rs = EngageboostShipmentOrders.objects.filter(trent_picklist_id=EngageboostOrdermaster.trent_picklist_id).first()
            if rs:
                shipping_status = rs.shipment_status
        return shipping_status
    def get_CustomersAddressBook(self, EngageboostOrdermaster):
        data = []
        if EngageboostOrdermaster.address_book_id is not None and EngageboostOrdermaster.address_book_id>0:
            rs = EngageboostCustomersAddressBook.objects.filter(id=EngageboostOrdermaster.address_book_id)
            if rs.count()>0:
                rs = rs.values('id','customers_id','long_val','lat_val').first()
                rs_data = CustomersAddressBookSerializer(rs)
                data = rs_data.data
        return data
    def get_webshop_id(self, EngageboostOrdermaster):
        return EngageboostOrdermaster.webshop_id
    def get_time_slot(self, EngageboostOrdermaster):
        time_slot_id = EngageboostOrdermaster.time_slot_id
        if time_slot_id:
            time_slot_id = time_slot_id.replace(" ", "")
            time_slot_id = time_slot_id.lower()
            times = time_slot_id.split('-')
            try:
                if ":" in times[0]:
                    start = datetime.strptime(times[0], "%I:%M%p")
                    start = datetime.strftime(start, "%I:%M%p")
                else:
                    start = datetime.strptime(times[0], "%I%p")
                    start = datetime.strftime(start, "%I:%M%p")
                if ":" in times[1]:
                    end = datetime.strptime(times[1], "%I:%M%p")
                    end = datetime.strftime(end, "%I:%M%p")
                else:
                    end = datetime.strptime(times[1], "%I%p")
                    end = datetime.strftime(end, "%I:%M%p") 
            except:
                if ":" in times[0]:
                    start = datetime.strptime(times[0], "%H:%M%p")
                    start = datetime.strftime(start, "%H:%M%p")
                else:
                    start = datetime.strptime(times[0], "%H%p")
                    start = datetime.strftime(start, "%H:%M%p")
                if ":" in times[1]:
                    end = datetime.strptime(times[1], "%H:%M%p")
                    end = datetime.strftime(end, "%H:%M%p")
                else:
                    end = datetime.strptime(times[1], "%H%p")
                    end = datetime.strftime(end, "%H:%M%p")
            time_slot_id = str(start)+"-"+str(end)
            time_slot_id = time_slot_id.lower()
            time_slot_id = time_slot_id.replace("-","")
            time_slot_id = time_slot_id.replace(":","")
        return time_slot_id

class OrderViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostOrdermaster
        fields='__all__'

class OrderAndOrderProductSerializer(serializers.ModelSerializer):
    order_products = OrderProductsSerializer(many=True)
    customer        = CustomerViewSerializer(read_only = True)
    order_activity  = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostOrdermaster
        fields='__all__'

    def get_order_activity(self, EngageboostOrdermaster):
        rs = EngageboostOrderActivity.objects.filter(order_id=EngageboostOrdermaster.id).all().order_by('-id')
        serializer = OrderActivitySerializer(rs, many=True)
        return serializer.data

class OrderProductsViewSerializer(serializers.ModelSerializer):
    product=EngageboostProductsSerializer(read_only = True)
    order=OrderViewSerializer(read_only = True)
    class Meta:
        model = EngageboostOrderProducts
        fields='__all__'

class TempOrdermasterSerializer(serializers.ModelSerializer):
    customer=CustomerViewSerializer()
    webshop=ChannelsSerializer()
    class Meta:
        model = EngageboostTempOrdermaster
        fields='__all__'

class ShipmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostShipments
        fields='__all__'

class ShipmentOrderProductsSerializer(serializers.ModelSerializer):
    shipment=ShipmentsSerializer()
    order=OrderMasterSerializer()
    product=EngageboostProductsSerializer()
    order_product=OrderProductsSerializer()
    class Meta:
        model = EngageboostShipmentOrderProducts
        fields='__all__'

class ShipmentOrderProductsViewSerializer(serializers.ModelSerializer):
    product=EngageboostProductsSerializer()
    class Meta:
        model = EngageboostShipmentOrderProducts
        fields='__all__'

class WishlistsSerializer(serializers.ModelSerializer):
    product=EngageboostProductsSerializer()
    class Meta:
        model = EngageboostWishlists
        fields='__all__'

class WebsiteActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostWebsiteActivities
        fields='__all__'

class WebsiteChannelFieldValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostWebsiteChannelFieldValues
        fields='__all__'

class WebsiteChannelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostWebsiteChannels
        fields='__all__'

class ShipmentsOrdersSerializer(serializers.ModelSerializer):
    order = OrderMasterSerializer()
    shipment_order_products = ShipmentOrderProductsSerializer(many=True)
    class Meta:
        model = EngageboostShipmentOrders
        fields='__all__'

class ShipmentsOrdersViewSerializer(serializers.ModelSerializer):
    order = OrderViewSerializer()
    # shipment_order_products = ShipmentOrderProductsViewSerializer(many=True)
    # shipment_order_products = ShipmentOrderProductsSerializer(many=True)
    class Meta:        
        model = EngageboostShipmentOrders
        # fields='__all__'
        # , "shipment_order_products"
        fields = [ "id","shipment","trent_picklist_id","custom_order_id","webshop_id","warehouse_id","shipping_method_id","ccrcrdref","destinationarea","destinationlocation","actualweight","total_quantity","dimension","schedule_pickup_date","schedule_pickup_time","zone_id","time_slot_id","no_of_crates","return_delivery_date","return_driver_id","shipment_status","order"]
        read_only_fields = fields

class AttemptedDeliveryDetailsSerializer(serializers.ModelSerializer):
    shipment=ShipmentsSerializer()
    order=OrderMasterSerializer()
    class Meta:
        model = EngageboostAttemptedDeliveryDetails
        fields='__all__'

# class FlipkartOrderProcessSerializer(serializers.ModelSerializer):
#     order=OrderMasterSerializer()
#     class Meta:
#         model = EngageboostFlipkartOrderProcess
#         fields='__all__'

class EngageboostCategoryMastersLangSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCategoryMastersLang
        fields='__all__'

class CategoriesSerializer(serializers.ModelSerializer):
    lang_data = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostCategoryMasters
        # fields = ('id','lft','rght','check_id','createdby', 'parent_id', 'name','isblocked','description','display_order','customer_group_id','applicable_imei','page_title','meta_keywords','website_id','image','thumb_image','banner_image','display_mobile_app','created','modified')
        fields='__all__'
    def get_lang_data(self, EngageboostCategoryMasters):
        rs_lang = EngageboostCategoryMastersLang.objects.filter(category_id=EngageboostCategoryMasters.id, isblocked='n', isdeleted='n').all()
        lang_data = EngageboostCategoryMastersLangSerializer(rs_lang, many=True)
        return lang_data.data

class CategoriesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCategoryMasters
        # fields = ('id','lft','rght','check_id','createdby', 'parent_id', 'name','isblocked','description','display_order','customer_group_id','applicable_imei','page_title','meta_keywords','website_id','image','thumb_image','banner_image','display_mobile_app','created','modified')
        fields='__all__'

class CategoriesCountSerializer(serializers.ModelSerializer):
    active_count = serializers.SerializerMethodField()
    inactive_count = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProductCategories
        fields= '__all__'
    def get_active_count(self, EngageboostProductCategories):
        count = EngageboostProducts.objects.filter(isdeleted='n',id=EngageboostProductCategories.product_id).count()
        return count
    def get_inactive_count(self, EngageboostProductCategories):
        count = EngageboostProducts.objects.filter(isdeleted='y',id=EngageboostProductCategories.product_id).count()
        return count

class CategoryBannersImagesSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostCategoryBannersImages
        fields='__all__'
    def get_image_url(self,EngageboostCategoryBannersImages):
        catObj = EngageboostCategoryBanners.objects.filter(id=EngageboostCategoryBannersImages.category_banner_id)
        if catObj.count()>0:
            link = ""
            catResult = catObj.first()
            website_id = catResult.website_id
            website = EngageboostCompanyWebsites.objects.get(id=website_id)
            company_name = website.company_name
            s3folder_name = website.s3folder_name
            module_name = 'CategoryBanner'
            link = settings.AMAZON_BASE_URL+company_name+'/'+s3folder_name+'/'+module_name+'/'
            return link
            

class CategoryBannersSerializer(serializers.ModelSerializer):
    # warehouse = WarehousemastersSerializer()
    warehouse_id = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostCategoryBanners
        fields='__all__'
    def get_warehouse_id(self, EngageboostCategoryBanners):
        str_warehouse_id = EngageboostCategoryBanners.warehouse_id
        
        if str_warehouse_id is not None and str_warehouse_id!="":
            lst_warehouse_ids = str_warehouse_id.split(",")
            rs_warehouse  = EngageboostWarehouseMasters.objects.filter(id__in = lst_warehouse_ids)
            if rs_warehouse:
                warehouse_data = serializer = WarehousemastersSerializer(rs_warehouse, many=True).data
            else:
                warehouse_data = []
        else:
            warehouse_data = []
        return warehouse_data

class EngageboostBrandMastersLangSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostBrandMastersLang
        fields='__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostBrandMasters
        fields='__all__'

class BrandEditSerializer(serializers.ModelSerializer):
    lang_data = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostBrandMasters
        fields='__all__'

    def get_lang_data(self, EngageboostCategoryMasters):
        rs_lang = EngageboostBrandMastersLang.objects.filter(brand_id=EngageboostCategoryMasters.id, isblocked='n', isdeleted='n').all()
        lang_data = EngageboostBrandMastersLangSerializer(rs_lang, many=True)
        return lang_data.data

class ProductCategoriesSerializer(serializers.ModelSerializer):
    product = EngageboostProductsSerializer()
    category = CategoriesSerializer()
    class Meta:
        model = EngageboostProductCategories
        fields='__all__'
        
class ProductImeisSerializer(serializers.ModelSerializer):
    order=OrderMasterSerializer()
    product=EngageboostProductsSerializer()
    class Meta:
        model = EngageboostProductImeis
        fields='__all__'

# class ProductItemSpecificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostProductItemSpecification
#         fields='__all__'

# class ProductItemSpecificationValueSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostProductItemSpecificationValue
#         fields='__all__'

class ProductKeyTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductKeyTypes
        fields='__all__'

class ProductMarketplacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductMarketplaces
        fields='__all__'

class ProductMoveTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductMoveTrack
        fields='__all__'

# class ProductPricingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostProductPricing
#         fields='__all__'

class ProductPushSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductPush
        fields='__all__'

class ProductRatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductRatings
        fields='__all__'

class ProductRepriceRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductRepriceRule
        fields='__all__'

class ReviewSerializer(serializers.ModelSerializer):
    product=EngageboostProductsSerializer()
    user=UserSerializer()
    class Meta:
        model = EngageboostProductReviews
        fields='__all__'

class ProductStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductStatus
        fields='__all__'

class StockSerializer(serializers.ModelSerializer):
    product=EngageboostProductsSerializer()
    warehouse=WarehousemastersSerializer()
    class Meta:
        model = EngageboostProductStocks
        fields='__all__'

class WarehouseStockSerializer(serializers.ModelSerializer):
    warehouse=WarehousemastersSerializer()
    class Meta:
        model = EngageboostProductStocks
        fields='__all__'

class ProductStockCronsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductStockCrons
        fields='__all__'

class ProductTemplateMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductTemplateMasters
        fields='__all__'

class ProductTierPriceSerializer(serializers.ModelSerializer):
    product=EngageboostProductsSerializer()
    class Meta:
        model = EngageboostProductTierPrice
        fields='__all__'

class ProductVisibilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductVisibilities
        fields='__all__'

class ProductworksheetimagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductworksheetimages
        fields='__all__'                

class OrderStatusMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostOrderStatusMasters
        fields='__all__'

class ReturnOrderImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostReturnOrderImages
        fields='__all__'

class AffiliateContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAffiliateContacts
        fields='__all__'

class CategorieschannelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostChannelsCategoriesMaster
        fields='__all__'

class EmiSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostEmiSettings
        fields='__all__'

class OutofstockNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostOutofstockNotification
        fields='__all__'

class ProductRateperpacksSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductRateperpacks
        fields='__all__'

class RateperpacksSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostRateperpacks
        fields='__all__'

class TallyLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTallyLogs
        fields='__all__'

class CheckoutReturnDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engageboost2CheckoutReturnDetails
        fields='__all__'

class AccountChannelsSerializer(serializers.ModelSerializer):
    channel=ChannelsSerializer()
    class Meta:
        model = EngageboostAccountChannels
        fields='__all__'

class AccountTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAccountTypes
        fields='__all__'

class ActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostActivities
        fields='__all__'

class ActivitySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostActivitySettings
        fields='__all__'

class AffiliateDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAffiliateDetails
        fields='__all__'

class AmazonBoostCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAmazonBoostCategories
        fields='__all__'

class AmazonCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAmazonCategories
        fields='__all__'

class AmazonCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAmazonCredentials
        fields='__all__'

class AmazonFeedReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAmazonFeedReport
        fields='__all__'

class AmazonFeedStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAmazonFeedStatus
        fields='__all__'

class AmazonFlatFileHeadersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAmazonFlatFileHeaders
        fields='__all__'

class AmazonItemTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAmazonItemTransactions
        fields='__all__'

class AmazonOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAmazonOrders
        fields='__all__'

class AmazonProductBulletpointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAmazonProductBulletpoints
        fields='__all__'

class EngageboostAmazonebtgSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAmazonebtg
        fields='__all__'

class AppCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAppCategory
        fields='__all__'

class AppMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAppMaster
        fields='__all__'

class AppReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAppReviews
        fields='__all__'

class AppWebsitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAppWebsites
        fields='__all__'

class ApplicableZipcodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostApplicableZipcodes
        fields='__all__'

class AppstoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAppstores
        fields='__all__'

class AssetPathsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAssetPaths
        fields='__all__'

class AtompaynetReturnurlDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAtompaynetReturnurlDetails
        fields='__all__'

class AuthorizeNetReturnDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAuthorizeNetReturnDetails
        fields='__all__'

class AutoProductUploadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAutoProductUploads
        fields='__all__'

class AwbMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAwbMasters
        fields='__all__'

class AwbMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAwbMasters
        fields='__all__'

class CcavenueReturnDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCcavenueReturnDetails
        fields='__all__'

class CcavenueUpgradedReturnDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCcavenueUpgradedReturnDetails
        fields='__all__'

class AxisReturnDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAxisReturnDetails
        fields='__all__'

class CmsMenusSerializer(serializers.ModelSerializer):
    product=EngageboostProductsSerializer()
    category=CategoriesSerializer()
    class Meta:
        model = EngageboostCmsMenus
        fields='__all__'

class CmsPageSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCmsPageSettings
        fields='__all__'

class CommissionSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCommissionSettings
        fields='__all__'

class CompaniesSerializer(serializers.ModelSerializer):
    country=GlobalsettingscountriesSerializer()
    class Meta:
        model = EngageboostCompanies
        fields='__all__'

class CompaniesCronsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCompaniesCrons
        fields='__all__'

class CompanyAuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCompanyAuthentication
        fields='__all__'

class CompanyWebsiteMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCompanyWebsiteMap
        fields='__all__'

class CompanyWebsiteSerializer1(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCompanyWebsites
        fields='__all__'

class CompanyWebsiteSerializer(serializers.ModelSerializer):
    country=GlobalsettingscountriesSerializer(read_only=True)
    #company_name = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostCompanyWebsites
        fields='__all__'
    # def get_company_name(self,EngageboostCompanyWebsites):
    #     obj = EngageboostCompanies.objects.get(id=EngageboostCompanyWebsites.engageboost_company_id)
    #     return obj.company_name   

class CossSellProductsSerializer(serializers.ModelSerializer):
    cross_product=EngageboostProductsSerializer()
    class Meta:
        model = EngageboostCossSellProducts
        fields='__all__'

class CratesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCrates
        fields='__all__'

class CreditcardSettingInformationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCreditcardSettingInformations
        fields='__all__'

class CreditcardTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCreditcardTypes
        fields='__all__'

class BaseCurrencyratesetSerializer(serializers.ModelSerializer):
    country=GlobalsettingscountriesSerializer()
    class Meta:
        model = EngageboostCurrencyRates
        fields='__all__'

class CurrencyMastersSerializer(serializers.ModelSerializer):
    currency_rates=BaseCurrencyratesetSerializer(many=True)
    engageboost_country=GlobalsettingscountriesSerializer()
    class Meta:
        model = EngageboostCurrencyMasters
        fields='__all__'

class BaseCurrencyratesetViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCurrencyRates
        fields=["id", "engageboost_company_website_id", "currency_code", "exchange_rate", "isbasecurrency",  "engageboost_currency_master"]

class CurrencyViewSerializer(serializers.ModelSerializer):
    # currency_rates=BaseCurrencyratesetViewSerializer(many=True)
    currency_rates = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostCurrencyMasters
        fields='__all__'
    def get_currency_rates(self, EngageboostCurrencyMasters):
        rs = EngageboostCurrencyRates.objects.filter(engageboost_currency_master_id=EngageboostCurrencyMasters.id).first()
        rs_data = BaseCurrencyratesetViewSerializer(rs)
        return rs_data.data

class CustomEmailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCustomEmails
        fields='__all__'

class CustomFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCustomFields
        fields='__all__'

class CustomFormsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCustomForms
        fields='__all__'

class CustomValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCustomValues
        fields='__all__'

class DbWebsitehitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDbWebsitehits
        fields='__all__'

class DbWebsitestatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDbWebsitestats
        fields='__all__'

class DbWebsitevisitorshitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDbWebsitevisitorshits
        fields='__all__'

class DefaultCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDefaultCategories
        fields='__all__'

class DefaultEmailTypeContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDefaultEmailTypeContents
        fields='__all__'

class DefaultModuleLayoutFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDefaultModuleLayoutFields
        fields='__all__'

class DefaultModuleLayoutSectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDefaultModuleLayoutSections
        fields='__all__'

class DefaultModuleLayoutsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDefaultModuleLayouts
        fields='__all__'

# class DefaultSectionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostDefaultSections
#         fields='__all__'

class DefaultsFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDefaultsFields
        fields='__all__'

class DeliveryManagersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDeliveryManagers
        fields='__all__'

class DeliveryPlanOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDeliveryPlanOrder
        fields='__all__'

class DeliverySlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDeliverySlot
        fields='__all__'

class DhlZipcodeListsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDhlZipcodeLists
        fields='__all__'

class DirecpayReturnDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDirecpayReturnDetails
        fields='__all__'

class DiscountConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDiscountMastersConditions
        fields='__all__'

class DiscountMasterCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDiscountMastersCoupons
        fields='__all__'

class DiscountFreebieMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDiscountFreebieMappings
        fields='__all__'

class DiscountMasterSerializer(serializers.ModelSerializer):
    DiscountMastersConditions = DiscountConditionsSerializer(many=True)
    DiscountMastersCoupons = DiscountMasterCouponSerializer(many=True)
    product_id_qty = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostDiscountMasters
        fields='__all__'
    def get_product_id_qty(self,EngageboostDiscountMasters):
        obj = EngageboostDiscountFreebieMappings.objects.filter(discount_master_id=EngageboostDiscountMasters.id).all()
        items = []
        all_items = ""
        for item in obj:
            qty = str(item.product_id)+"@"+str(item.qty)
            items.append(qty)
        if len(items)>0:
            all_items = ",".join(items)
        return all_items   

            


class DriverLoginDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDriverLoginDetails
        fields='__all__'

class DriverVeichleMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDriverVeichleMap
        fields='__all__'

class EbayBoostCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostEbayBoostCategories
        fields='__all__'

class EbayItemSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostEbayItemSpecification
        fields='__all__'

class EbayItemSpecificationValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostEbayItemSpecificationValue
        fields='__all__'

class EbayProductConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostEbayProductCondition
        fields='__all__'

class EbaystoreCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostEbaystoreCategories
        fields='__all__'

class EmailTypeMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostEmailTypeMasters
        fields='__all__'

class EmktCampaignsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostEmktCampaigns
        fields='__all__'

class EmktContactlistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostEmktContactlists
        fields='__all__'
        # depth =1

class ContactsSerializer(serializers.ModelSerializer):
    contact_list = EmktContactlistsSerializer()
    country=GlobalsettingscountriesSerializer()
    class Meta:
        model = EngageboostEmktContacts
        fields='__all__'
        depth =2

class EmktPageVisitStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostEmktPageVisitStat
        fields='__all__'

class SegmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostEmktSegments
        fields='__all__'

class SegmentsContactlistsSerializer(serializers.ModelSerializer):
    segment = SegmentsSerializer()
    contact = ContactsSerializer()
    contactlist = EmktContactlistsSerializer()
    class Meta:
        model = EngageboostEmktSegmentContactlists
        fields='__all__'

class EmktSendmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostEmktSendmail
        fields='__all__'

class EmktTemplateMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostEmktTemplateMasters
        fields='__all__'

class EmktTemplatecategoryMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostEmktTemplatecategoryMasters
        fields='__all__'

class EmktWebsiteTemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostEmktWebsiteTemplates
        fields='__all__'

class FacebookProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostFacebookProducts
        fields='__all__'

# class FbPageProductsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostFbPageProducts
#         fields='__all__'

# class FbTempUserDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostFbTempUserDetails
#         fields='__all__'

# class FbaPlanProductsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostFbaPlanProducts
#         fields='__all__'

# class FbaShipmentProductsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostFbaShipmentProducts
#         fields='__all__'

# class FbaShipmentsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostFbaShipments
#         fields='__all__'

# class FbaShippingBoxesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostFbaShippingBoxes
#         fields='__all__'

# class FbaShippingPlanFeedSubmissionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostFbaShippingPlanFeedSubmissions
#         fields='__all__'

# class ShippingServicesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostFbaShippingServices
#         fields='__all__'

# class FbaShippingplansSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostFbaShippingplans
#         fields='__all__'

# class FbaStepsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostFbaSteps
#         fields='__all__'

class FedexZipcodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostFedexZipcodes
        fields='__all__'

class FeeMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostFeeMasters
        fields='__all__'

class FeeSettingMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostFeeSettingMasters
        fields='__all__'

class FlipkartOrderTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostFlipkartOrderTransactions
        fields='__all__'

class FlipkartReconciliationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostFlipkartReconciliations
        fields='__all__'

class FormulaDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostFormulaDetails
        fields='__all__'

class FulfillmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostFulfillments
        fields='__all__'

class GlobalsettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostGlobalSettings
        fields='__all__'

class GlobalsettingCountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostGlobalsettingCountries
        fields='__all__'

class GlobalsettingCurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostGlobalsettingCurrencies
        fields='__all__'

class GlobalsettingLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostGlobalsettingLanguages
        fields='__all__'

class GlobalsettingSitemodulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostGlobalsettingSitemodules
        fields='__all__'

class GooglecheckoutReturnDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostGooglecheckoutReturnDetails
        fields='__all__'

class GoogleshopCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostGoogleshopCategories
        fields='__all__'

class GridLayoutsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostGridLayouts
        fields='__all__'

class GridColumnLayoutsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostGridColumnLayouts
        fields='__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostGroups
        fields='__all__'
        group_id = serializers.Field(source='id')

class HdfcReturnDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostHdfcReturnDetails
        fields='__all__'

class IciciReturnDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostIciciReturnDetails
        fields='__all__'

class HelpTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostHelpText
        fields='__all__'

class HolidaysMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostHolidaysMasters
        fields='__all__'

class ImportErrorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostImportErrorLog
        fields='__all__'

class ImportMapFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostImportMapFields
        fields='__all__'

class ImportStockFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostImportStockFiles
        fields='__all__'

class ImportedTempProductStocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostImportedTempProductStocks
        fields='__all__'

class InventoryMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostInventoryMasters
        fields='__all__'

class InventoryProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostInventoryProducts
        fields='__all__'

class InvoiceContainersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostInvoiceContainers
        fields='__all__'

class InvoiceproductSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostInvoiceProducts
        fields='__all__'

class InvoicemasterSerializer(serializers.ModelSerializer):
    order=OrderMasterSerializer()
    invoice_order_products=InvoiceproductSerializer(many=True)
    customer_name = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostInvoicemaster
        fields='__all__'
    def get_customer_name(self,EngageboostInvoicemaster):
        customers_obj = EngageboostCustomers.objects.filter(isdeleted="n",isblocked="n",id=EngageboostInvoicemaster.customer_id)
        customers_obj = customers_obj.annotate(name=Concat('first_name', Value(' '), 'last_name')).values()
        if customers_obj.count()>0:
            customers_obj = customers_obj.first()
            return customers_obj['name']

class InvoicemasterViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostInvoicemaster
        fields='__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostMenuMasters
        fields='__all__'

class ShortcutSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostMenuShortcuts
        fields='__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostLanguages
        fields='__all__'

class ManifestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostManifests
        fields='__all__'

class ModuleLayoutsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostModuleLayouts
        fields='__all__'

class ModulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostModules
        fields='__all__'

class JwelleryAppSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostJwelleryAppSettings
        fields='__all__'

class CreditPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCreditPoint
        fields='__all__'

class CreditPointConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCreditPointConditions
        fields='__all__'

class MappedCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostMappedCategories
        fields='__all__'

class MarketplaceManifestsFeedStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostMarketplaceManifestsFeedStatus
        fields='__all__'

class MarketplaceManifestsFeedStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostMarketplaceManifestsFeedStatus
        fields='__all__'

class MarketplaceFieldLabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostMarketplaceFieldLabels
        fields='__all__'

class WarehousemanagerSerializer(serializers.ModelSerializer):
    manager=UserSerializer()
    class Meta:
        model = EngageboostWarehouseManager
        fields='__all__'

class WarehousemasterapplicablechannelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostWarehouseMasterApplicableChannels
        fields='__all__'

class WarehouseMasterApplicableRegionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostWarehouseMasterApplicableRegions
        fields='__all__'   

class ZoneZipcodeMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostZoneZipcodeMasters
        fields='__all__'

class ZoneMastersSerializer(serializers.ModelSerializer):
    ZoneZipcodeMasters=ZoneZipcodeMastersSerializer(many=True)
    class Meta:
        model = EngageboostZoneMasters
        fields='__all__'

class TrafficReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTrafficReports
        fields='__all__'

class TrafficReportsBrowsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTrafficReportsBrowsers
        fields='__all__'

class TrafficReportsMobilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTrafficReportsMobiles
        fields='__all__'

class TrafficReportsPagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTrafficReportsPages
        fields='__all__'

class TrafficReportsSocialesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTrafficReportsSociales
        fields='__all__'

class TrafficReportsSourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTrafficReportsSources
        fields='__all__'

# class TemplateCategoriesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostTemplateCategories
#         fields='__all__'

# class TemplateCategoryMastersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostTemplateCategoryMasters
#         fields='__all__'

# class TemplateColorMastersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostTemplateColorMasters
#         fields='__all__'

# class TemplateColorsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostTemplateColors
#         fields='__all__'

# class TemplateIndustriesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostTemplateIndustries
#         fields='__all__'

class TemplateIndustryMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTemplateIndustryMasters
        fields='__all__'

class BasicTemplateMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTemplateMasters
        fields='__all__'

# class TemplateRelationsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostTemplateRelations
#         fields='__all__'

# class TemplateSettingsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostTemplateSettings
#         fields='__all__'

# class TempCategoryMastersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostTempCategoryMasters
#         fields='__all__'

# class TempChannelCategoryMappingsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostTempChannelCategoryMappings
#         fields='__all__'

# class TempCustomersSerializer(serializers.ModelSerializer):
#     country=GlobalsettingscountriesSerializer()
#     customer_group=CustomerGroupSerializer()
#     class Meta:
#         model = EngageboostTempCustomers
#         fields='__all__'

# class TempEmktContactsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostTempEmktContacts
#         fields='__all__'

class TempProductCustomFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTempProductCustomFields
        fields='__all__'

class TempProductimagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTempProductimages
        fields='__all__'
        

class TempProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTempProducts
        fields='__all__'

class TempDiscountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTempDiscountMasters
        fields='__all__'

class SupplierstempSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTempSuppliers
        fields='__all__'

class TemporaryShoppingCartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTemporaryShoppingCarts
        fields='__all__'

# class TmpPurchaseOrderProductsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostTmpPurchaseOrderProducts
#         fields='__all__'

# class TmpPurchaseOrdersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostTmpPurchaseOrders
#         fields='__all__'

class TaxRatesConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTaxRatesConditions
        fields='__all__'

class TaxratesSerializer(serializers.ModelSerializer):
    TaxRatesConditions = TaxRatesConditionsSerializer(many=True)
    country=GlobalsettingscountriesSerializer()
    class Meta:
        model = EngageboostTaxRates
        fields='__all__'

class TaxRuleTablesSerializer(serializers.ModelSerializer):
    tax_rate = TaxratesSerializer()
    tax_rate_name = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostTaxRuleTables
        fields='__all__'
    def get_tax_rate_name(self, EngageboostTaxRuleTables):
        rs = EngageboostTaxRates.objects.filter(id=EngageboostTaxRuleTables.tax_rate_id).first()
        return rs.name    

class Taxsettings(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTaxSettings
        fields='__all__'

class TaxclassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTaxclasses
        fields='__all__'

class ShippingServiceNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostShippingServiceNames
        fields='__all__'

class PackagSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostShippingPackagingtype
        fields='__all__'

class PresetsSerializer(serializers.ModelSerializer):
    service = ShippingServiceNamesSerializer()
    package = PackagSerializer()
    class Meta:
        model = EngageboostPresets
        fields='__all__'
        depth=3

class ShippingSerializer(serializers.ModelSerializer):
    presets=PresetsSerializer(many=True)
    class Meta:
        model = EngageboostShippingMasters
        fields='__all__'

class ShippingMastersSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostShippingMastersSettings
        fields='__all__'

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTags
        fields='__all__'

class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostSuppliers
        fields='__all__'

class OrderActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostOrderActivity
        fields='__all__'

class OrderDeliverySlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostOrderDeliverySlot
        fields='__all__'

class OrderFiltersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostOrderFilters
        fields='__all__'

class OrderLayoutsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostOrderLayouts
        fields='__all__'

class OrderNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostOrderNotes
        fields='__all__'

class OrderReturnDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostOrderReturnDetails
        fields='__all__'

class OrderStatusSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostOrderStatusSettings
        fields='__all__'

class OrderSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostOrderSubscribe
        fields='__all__'

class OrderSubscribeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostOrderSubscribeDetails
        fields='__all__'

class NewsletterSubcribesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostNewsletterSubcribes
        fields='__all__'

class PagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPages
        fields='__all__'

class ParentCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostParentCategories
        fields='__all__'

class PaymentSetupDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPaymentSetupDetails
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

class PaymentgatewaySettingInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPaymentgatewaySettingInformation
        fields='__all__'

class WebsitePaymentmethodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostWebsitePaymentmethods
        fields='__all__'

class PaymentgatewaysGlobalsettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPaymentgatewaysGlobalsettings
        fields='__all__'

class GlobalsettingstimezoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTimezones
        fields='__all__'

class OtherLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostOtherLocation
        fields='__all__'

class PurchaseordersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPurchaseOrders
        fields='__all__'

class PurchaseOrderReceivedProductsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPurchaseOrderReceivedProducts
        fields='__all__'

class PurchaseOrdersReceivedSerializer(serializers.ModelSerializer):
    purchase_order_received_product = PurchaseOrderReceivedProductsViewSerializer(many=True)
    class Meta:
        model = EngageboostPurchaseOrdersReceived
        fields='__all__'

class PurchaseOrderReceivedProductsSerializer(serializers.ModelSerializer):
    purchase_order_received = PurchaseOrdersReceivedSerializer()
    product                 = EngageboostProductsSerializer()
    PO_receive_pro_details  = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostPurchaseOrderReceivedProducts
        fields='__all__'
    def get_PO_receive_pro_details(self, EngageboostPurchaseOrderReceivedProducts):
        rs = EngageboostPurchaseOrderReceivedProductDetails.objects.filter(purchase_order_received_id=EngageboostPurchaseOrderReceivedProducts.purchase_order_received_id, purchase_order_product_id=EngageboostPurchaseOrderReceivedProducts.product_id).order_by('-expiry_date').all()
        podata = EngageboostPurchaseOrderReceivedProductDetailsSerializer(rs, many=True)
        return podata.data

class PurchaseOrdersPaymentMethodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPurchaseOrdersPaymentMethods
        fields='__all__'

class PurchaseOrdersShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPurchaseOrdersShippingMethods
        fields='__all__'

class PermisionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPermisions
        fields='__all__'

class PicklistProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPicklistProducts
        fields='__all__'

class PicklistProductsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPicklistProducts
        fields='__all__'

class PicklistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPicklists
        fields='__all__'

class PicklistsPlanDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPlanDetails
        fields='__all__'

class RelatedProductsSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_sku = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostRelatedProducts
        fields='__all__'
    def get_product_name(self, EngageboostRelatedProducts):
        get_record = EngageboostProducts.objects.filter(id=EngageboostRelatedProducts.related_product_id).first()
        return get_record.name
    def get_product_sku(self, EngageboostRelatedProducts):
        get_record = EngageboostProducts.objects.filter(id=EngageboostRelatedProducts.related_product_id).first()
        return get_record.sku 

class ReportCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostReportCustomer
        fields='__all__'

class ReportDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostReportDate
        fields='__all__'

class ReportLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostReportLocation
        fields='__all__'

class ReportOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostReportOrder
        fields='__all__'

class ReportProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostReportProduct
        fields='__all__'

class ShowroomManagersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostShowroomManagers
        fields='__all__'

class ShowroomMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostShowroomMasters
        fields='__all__'

class SmsTypeContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostSmsTypeContents
        fields='__all__'

class SmsTypeMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostSmsTypeMasters
        fields='__all__'

class TrentsPicklistProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTrentsPicklistProducts
        fields='__all__'

class TrentPicklistsSerializer(serializers.ModelSerializer):
    trents_picklist_products = TrentsPicklistProductsSerializer(many=True)
    class Meta:
        model = EngageboostTrentPicklists
        fields='__all__'
        depth=1

class UnitmasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostUnitMasters
        fields='__all__'

class UnitRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostUnitRates
        fields='__all__'

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostOTP
        fields='__all__'

class StatePincodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostStatePincodes
        fields='__all__'

class StorelocatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostStorelocators
        fields='__all__'

class SuperadminsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostSuperadmins
        fields='__all__'

class TwitterCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTwitterCredentials
        fields='__all__'

class MysavelistSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostMysavelist
        fields='__all__'

class NotificationReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostNotificationReturn
        fields='__all__'

class MenuPermitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostRoleMenuPermissions
        fields = ("role_id","master_id","add","edit","delete","view","isblocked","isdeleted","created","modified","block","import_field","export")

class SitemodulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostSitemodules
        fields='__all__'

class MarketplaceFtpCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostMarketplaceFtpCredentials
        fields='__all__'

class MarketplaceInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostMarketplaceInventory
        fields='__all__'

class MarketplaceInventoryPriceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostMarketplaceInventoryPriceUpdate
        fields='__all__'

class RepricingRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostRepricingRules
        fields='__all__'

class RepricingUpdateTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostRepricingUpdateTrack
        fields='__all__'

class SellerAccountTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostSellerAccountTypes
        fields='__all__'

class ShippingErrorLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostShippingErrorLogs
        fields='__all__'

class ShippingTableRateOrderAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostShippingTableRateOrderAmount
        fields='__all__'

class ShippingTableRateWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostShippingTableRateWeight
        fields='__all__'

class ShippingZipcodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostShippingZipcodes
        fields='__all__'

class UserAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostUserAccounts
        fields='__all__'

class UserLoginDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostUserLoginDetails
        fields='__all__'

class UserPlanDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostUserPlanDetails
        fields='__all__'

class UserSuggestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostUserSuggestions
        fields='__all__'

class UserWebsitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostUserWebsites
        fields='__all__'

class UspsMatrixSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostUspsMatrix
        fields='__all__'

class VehicleMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostVehicleMasters
        fields='__all__'

class VendorSkusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostVendorSkus
        fields='__all__'

class VisitContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostVisitContacts
        fields='__all__'

# class TallyCronSettingsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostTallyCronSettings
#         fields='__all__'

# class SnapdealCategoriesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostSnapdealCategories
#         fields='__all__'

# class SnapdealImageRefsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostSnapdealImageRefs
#         fields='__all__'

# class SnapdealOrderCancelReturnsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostSnapdealOrderCancelReturns
#         fields='__all__'

# class SnapdealOrderDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostSnapdealOrderDetails
#         fields='__all__'

# class SnapdealOrdersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostSnapdealOrders
#         fields='__all__'

# class SnapdealUploadIdTrackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostSnapdealUploadIdTrack
#         fields='__all__'

# class MerchantoneReturnDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostMerchantoneReturnDetails
#         fields='__all__'

# class NetazeptReturnDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostNetazeptReturnDetails
#         fields='__all__'

# class PaypalExpresscheckoutDoReturnDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostPaypalExpresscheckoutDoReturnDetails
#         fields='__all__'

# class PaypalExpresscheckoutGetReturnDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostPaypalExpresscheckoutGetReturnDetails
#         fields='__all__'

# class PaypalExpresscheckoutReturnDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostPaypalExpresscheckoutReturnDetails
#         fields='__all__'

# class PaypalproReturnDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostPaypalproReturnDetails
#         fields='__all__'

class PaypalstdReturnDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPaypalstdReturnDetails
        fields='__all__'

# class PaytmApiTrackingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostPaytmApiTracking
#         fields='__all__'

class PaytmItemTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPaytmItemTransactions
        fields='__all__'

class PaytmOrderProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPaytmOrderProcess
        fields='__all__'

class PaytmOrderTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPaytmOrderTransactions
        fields='__all__'

class PaytmProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPaytmProductDetails
        fields='__all__'

class PaytmReturnDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPaytmReturnDetails
        fields='__all__'

# class PayupaisaReturnDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostPayupaisaReturnDetails
#         fields='__all__'

class PaywithamazonReturnDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPaywithamazonReturnDetails
        fields='__all__'

class ReturnDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostReturnDetails
        fields='__all__'

# class SagepayReturnDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostSagepayReturnDetails
#         fields='__all__'

# class SnapmintReturnDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostSnapmintReturnDetails
#         fields='__all__'

# class UsaepayReturnDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostUsaepayReturnDetails
#         fields='__all__'

# class WorldpayReturnDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostWorldpayReturnDetails
#         fields='__all__'

class ZoneMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostZoneMasters
        fields = '__all__'

# for zone records only 
class ZoneMastersZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostZoneMasters
        #fields = ['name', 'country_id', 'state_name', 'city',  'isblocked']
        fields = '__all__'

# for area records only 
class ZoneMastersAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostZoneMasters
        #fields = ['name', 'zipcode', 'zone_id', 'isblocked']
        fields = '__all__'

# for subarea records only 
class ZoneMastersSubAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostZoneMasters
        #fields = ['name', 'zipcode', 'zone_id', 'area_id', 'isblocked']
        fields = '__all__'

#=================================================
class VehicleMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostVehicleMasters
        fields = '__all__'

class DeliveryManagerSerializer(serializers.ModelSerializer):
    warehouse_names = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostDeliveryManagers
        fields = '__all__'

    def get_warehouse_names(self, EngageboostDeliveryManagers):
        warehouseIdsArr = EngageboostDeliveryManagers.warehouse_ids.split(',')
        warehouse_names = EngageboostWarehouseMasters.objects.filter(id__in=warehouseIdsArr).values_list('name', flat=True)
        warehousenames = ','.join(warehouse_names)
        return warehousenames

class DeliverySlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDeliverySlot
        fields = '__all__'

class PriceFormulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPriceFormula
        fields = '__all__'

class EngageboostCreditPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCreditPoint
        fields = '__all__'

class EngageboostCreditPointConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCreditPointConditions
        fields = '__all__'

class ChannelsCategoriesMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostChannelsCategoriesMaster
        fields = '__all__'

class CreditPointConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCreditPointConditions
        fields = '__all__'
class CreditPointSerializer(serializers.ModelSerializer):
    CreditPointConditions = CreditPointConditionsSerializer(many=True)
    class Meta:
        model = EngageboostCreditPoint
        fields='__all__'

class EngageboostPurchaseOrderReceivedProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPurchaseOrderReceivedProductDetails
        fields = '__all__'

class EngageboostProductsViewOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProducts
        fields=("id","name","sku","weight","visibility_id","default_price","slug","twitter_addstatus","amazon_addstatus", "ean")

class EngageboostProductsUomSerializer(serializers.ModelSerializer):
    unit_name = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProducts
        fields=("id","name","sku","weight","visibility_id","default_price","slug","twitter_addstatus","amazon_addstatus", "ean", "uom", "unit_name")
    def get_unit_name(self, EngageboostProducts):
        if EngageboostProducts.uom:
            rs = EngageboostUnitMasters.objects.filter(id = EngageboostProducts.uom).first()
            return rs.unit_name
        else:
            return ""

class EngageboostInvoiceProductsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostInvoiceProducts
        fields = '__all__'

class OrderProductsViewOrderSerializer(serializers.ModelSerializer):
    product=EngageboostProductsViewOrderSerializer()
    invoice_product = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()
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
        quantity = int(quantity)-int(deleted_quantity)
        if quantity > 0:
            product_price = float(product_price)*float(quantity)
        else:
            product_price = 0.00
        return product_price
    def get_total_quantity(self, EngageboostOrderProducts):
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
        if total_quantity < 0:
            total_quantity = 0
        return total_quantity

class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model= EngageboostOrderPaymentDetails
        fields = '__all__'
        
class ViewOrderSerializer(serializers.ModelSerializer):
    customer        = CustomerViewSerializer(read_only = True)
    webshop         = ChannelsSerializer(read_only = True)
    order_products  = OrderProductsViewOrderSerializer(many=True)
    order_activity  = serializers.SerializerMethodField()
    warehouse_name       = serializers.SerializerMethodField()
    zone_name       = serializers.SerializerMethodField()
    order_payment   = serializers.SerializerMethodField()
    warehouse       = serializers.SerializerMethodField()
    assign_to_name = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostOrdermaster
        fields='__all__'
    def get_order_activity(self, EngageboostOrdermaster):
        rs = EngageboostOrderActivity.objects.filter(order_id=EngageboostOrdermaster.id).all().order_by('-id')
        serializer = OrderActivitySerializer(rs, many=True)
        return serializer.data
    def get_zone_name(self, EngageboostOrdermaster):
        rs = EngageboostZoneMasters.objects.filter(id=EngageboostOrdermaster.zone_id).first()
        zone_name = ""
        if rs:
            zone_name = rs.name
        return zone_name
    def get_order_payment(self, EngageboostOrdermaster):
        rs = EngageboostOrderPaymentDetails.objects.filter(order_id_id=EngageboostOrdermaster.id).all().order_by('-id')
        serializer = OrderPaymentSerializer(rs, many=True)
        return serializer.data
    def get_warehouse(self, EngageboostOrdermaster):
        rs = EngageboostWarehouseMasters.objects.filter(website_id=EngageboostOrdermaster.website_id,isblocked='n',isdeleted='n').all().order_by('-id')
        serializer = WarehousemastersSerializer(rs, many=True)
        return serializer.data
    def get_warehouse_name(self, EngageboostOrdermaster):
        rs = EngageboostWarehouseMasters.objects.filter(id=EngageboostOrdermaster.assign_wh).first()
        warehouse_name = ""
        if rs:
            warehouse_name = rs.name
        return warehouse_name

    def get_assign_to_name(self, EngageboostOrdermaster):
        assign_to_name = ""
        if EngageboostOrdermaster.assign_to is not None and EngageboostOrdermaster.assign_to!='':
            rs_user = EngageboostUsers.objects.filter(id=EngageboostOrdermaster.assign_to).first()
            if rs_user:
                assign_to_name = rs_user.first_name + " " + rs_user.last_name
#================================ Grn View Serializers ===================================
class GrnPurchaseOrderReceivedSerializer(serializers.ModelSerializer):
    purchase_order_received_products = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostPurchaseOrdersReceived
        fields = ('website_id','purchase_order_master_id','order_id','currency_id','received_purchaseorder_id','received_date','order_date','note','supplier_id','warehouse_id','product_id','quantity','purchase_order_payment_id','payment_method_description','payment_due_date','purchase_order_shipping_id','shipping_method_description','shipping_cost','purchase_order_tax','gross_amount','net_amount','paid_amount', 'discount_amount','gross_amount_base','net_amount_base','shipping_cost_base','purchase_order_tax_base','discount_amount_base','paid_amount_base','status','purchase_order_received_products')
    def get_purchase_order_received_products(self, EngageboostPurchaseOrdersReceived):
        get_record = EngageboostPurchaseOrderReceivedProducts.objects.filter(purchase_order_received_id=EngageboostPurchaseOrdersReceived.id)
        get_serializer =  GrnPurchaseOrderReceivedProductsSerializer(get_record, many=True)
        return get_serializer.data

class GrnPurchaseOrderReceivedProductsSerializer(serializers.ModelSerializer):
    product = BasicinfoSerializer()
    product_received_details = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostPurchaseOrderReceivedProducts
        fields = ('product', 'price','discount','quantity','product_tax_price','discount_amount','tax_name','tax_per','lot_no','rec_no',"good_cond",'damage','expiry_issue','total_qty','shortage','invoice_qty','manufact_date','received_date','standard_date','expiry_date','exp_issue','mrp_issue','issues','remarks','good_received','ok_to_ship', 'product_received_details')

    def get_product_received_details(self, EngageboostPurchaseOrderReceivedProducts):
        get_record = EngageboostPurchaseOrderReceivedProductDetails.objects.filter(purchase_order_received_id=EngageboostPurchaseOrderReceivedProducts.purchase_order_received_id)
        get_serializer = EngageboostPurchaseOrderReceivedProductDetailsSerializer(get_record, many=True)
        return get_serializer.data

#================================ Grn View Serializers ===================================
class MultipleBarcodeSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_sku = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostMultipleBarcodes
        fields='__all__'
    def get_product_name(self, EngageboostMultipleBarcodes):
        get_record = EngageboostProducts.objects.filter(id=EngageboostMultipleBarcodes.product_id).first()
        return get_record.name 
    def get_product_sku(self, EngageboostMultipleBarcodes):
        get_record = EngageboostProducts.objects.filter(id=EngageboostMultipleBarcodes.product_id).first()
        return get_record.sku  

class EngageboostTempMultipleBarcodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTempMultipleBarcodes
        fields = '__all__'

class PicklistOrderListSerializer(serializers.ModelSerializer):
    order_data = serializers.SerializerMethodField()
    shipment_data = serializers.SerializerMethodField()
    
    class Meta:
        model = EngageboostTrentPicklists
        fields = '__all__'
    def get_order_data(self, EngageboostTrentPicklists):
        rs_order = EngageboostOrdermaster.objects.filter(trent_picklist_id=EngageboostTrentPicklists.id).all()
        order_data = OrderViewSerializer(rs_order, many=True)
        orderdata = []
        orders = {}
        for order in order_data.data:
            orders.update({'order_id':order['id'], 'custom_order_id':order['custom_order_id']})
            orderdata.append(orders)
        return orderdata
    
    def get_shipment_data(self, EngageboostTrentPicklists):
        rs_shipment = EngageboostShipmentOrders.objects.filter(trent_picklist_id=EngageboostTrentPicklists.id).all()
        shipment_data = ShipmentsOrdersViewSerializer(rs_shipment, many=True)
        shipmentdata = []
        shipments = {}
        for shipment in shipment_data.data:
            shipments.update({'shipment_order_id':shipment['id'], 'shipment_status':shipment['shipment_status']})
            shipmentdata.append(shipments)
        return shipmentdata
# GRN
class OrderShipmentViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostOrdermaster
        fields='__all__'

class EngageboostShipmentOrderProductsSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostShipmentOrderProducts
        fields='__all__'
    def get_product_details(self, EngageboostShipmentOrderProducts):
        product_details = {}
        rs = EngageboostOrderProducts.objects.filter(product_id=EngageboostShipmentOrderProducts.product_id, order_id=EngageboostShipmentOrderProducts.order_id).first()
        if rs:
            product_price = round(float(rs.product_price)+float(rs.product_tax_price),2)
            product_details.update({'product_name':rs.product.name, 'sku':rs.product.sku,'ean':rs.product.ean, 'default_price':str(product_price)})
        return product_details

class EngageboostShipmentOrderProductsPicklistSerializer(serializers.ModelSerializer):
    order_product_details = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostShipmentOrderProducts
        fields='__all__'
    def get_order_product_details(self, EngageboostShipmentOrderProducts):
        product_details = {}
        rs = EngageboostOrderProducts.objects.filter(product_id=EngageboostShipmentOrderProducts.product_id, order_id=EngageboostShipmentOrderProducts.order_id).first()
        rs_data = OrderProductsSerializer(rs)
        # if rs:
        #     product_details.update({'product_name':rs.name, 'sku':rs.sku, 'default_price':str(rs.default_price)})
        return rs_data.data

class EngageboostShipmentOrderSerializer(serializers.ModelSerializer):
    # product_details         = serializers.SerializerMethodField()
    shipment_order_product  = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostShipmentOrders
        fields='__all__'
    def get_shipment_order_product(self, EngageboostShipmentOrders):
        rs      = EngageboostShipmentOrderProducts.objects.filter(shipment_order_id=EngageboostShipmentOrders.id).all()
        rs_data = EngageboostShipmentOrderProductsSerializer(rs, many=True)
        return rs_data.data

class EngageboostTrentsPicklistProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostTrentsPicklistProducts
        fields='__all__'

class TrentPicklistDetailsSerializer(serializers.ModelSerializer):
    trent_picklist_product = serializers.SerializerMethodField()
    shipment_order_product = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostTrentPicklists
        fields = '__all__'
    def get_trent_picklist_product(self, EngageboostTrentPicklists):
        rs = EngageboostTrentsPicklistProducts.objects.filter(trent_picklist_id=EngageboostTrentPicklists.id).all()
        rs_data = EngageboostTrentsPicklistProductsSerializer(rs, many=True)
        return rs_data.data
    def get_shipment_order_product(self, EngageboostTrentPicklists):
        rs = EngageboostShipmentOrderProducts.objects.filter(trent_picklist_id=EngageboostTrentPicklists.id).all()
        rs_data = EngageboostShipmentOrderProductsSerializer(rs, many=True)
        return rs_data.data

class PicklistProductDetailsSerializer(serializers.ModelSerializer):
    shipment_order_product  = serializers.SerializerMethodField()
    order_data = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostShipmentOrders
        fields='__all__'
    def get_shipment_order_product(self, EngageboostShipmentOrders):
        rs      = EngageboostShipmentOrderProducts.objects.filter(shipment_order_id=EngageboostShipmentOrders.id).all()
        rs_data = EngageboostShipmentOrderProductsPicklistSerializer(rs, many=True)
        return rs_data.data
    def get_order_data(self, EngageboostShipmentOrders):
        rs      = EngageboostOrdermaster.objects.filter(id=EngageboostShipmentOrders.order_id).first()
        # rs_data = EngageboostShipmentOrderProductsPicklistSerializer(rs, many=True)
        data = {
            "order_id":rs.id,
            "custom_order_id":rs.custom_order_id,
            "time_slot_date":str(rs.time_slot_date),
            "time_slot_id":rs.time_slot_id,
            "billing_phone":rs.billing_phone,
            "delivery_phone":rs.delivery_phone,
            "custom_msg":rs.custom_msg
        }
        return data

class PriceTypeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPriceTypeMaster
        fields='__all__'

class ProductPriceTypeMasterSerializer(serializers.ModelSerializer):
    price_type = PriceTypeMasterSerializer()
    class Meta:
        model = EngageboostProductPriceTypeMaster
        fields='__all__'

class OrderListBillingaddressSerializer(serializers.ModelSerializer):
    CustomerBillingAddress = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostOrdermaster
        fields='__all__'
    def get_CustomerBillingAddress(self, EngageboostOrdermaster):
        rs = EngageboostCustomersAddressBook.objects.filter(id =EngageboostOrdermaster.address_book_id).all()
        rs_data = CustomersAddressBookSerializer(rs)
        return rs_data.data

#  ****************  Delivery App *************************
class DeliveryOrderSerializer(serializers.ModelSerializer):
    DeliveryPlanOrder = serializers.SerializerMethodField()
    OrderList = serializers.SerializerMethodField()
    # CustomerBillingAddress = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostDriverVeichleMap
        fields='__all__'
    def get_DeliveryPlanOrder(self, EngageboostDriverVeichleMap):
        rs = EngageboostDeliveryPlanOrder.objects.filter(virtual_vechile_id=EngageboostDriverVeichleMap.virtual_vechile_id, shipment_id=EngageboostDriverVeichleMap.shipment_id).all()
        rs_data = DeliveryPlanOrderSerializer(rs, many=True)
        return rs_data.data
    def get_OrderList(self, EngageboostDriverVeichleMap):
        rs = EngageboostOrdermaster.objects.filter(shipment_id = EngageboostDriverVeichleMap.shipment_id, flag_order=0).exclude(order_status=4).order_by('sort_by_distance').all()
        rs_data = OrderListBillingaddressSerializer(rs, many=True)
        return rs_data.data

class VehicleDtailsSerializer(serializers.ModelSerializer):
    veichele_details = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostDriverVeichleMap
        fields='__all__'

    def get_veichele_details(self, EngageboostDriverVeichleMap):
        rs = EngageboostVehicleMasters.objects.filter(id=EngageboostDriverVeichleMap.vehicle_id).first()
        rs_data = VehicleMastersSerializer(rs)
        return rs_data.data

class DeliveryOrderDetailsSerializer(serializers.ModelSerializer):
    order_products = OrderProductsSerializer(many=True)
    class Meta:
        model = EngageboostOrdermaster
        fields='__all__'

class DeliveryPlanOrderViewSerializer(serializers.ModelSerializer):
    OrderList = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostDeliveryPlanOrder
        fields='__all__'
    def get_OrderList(self, EngageboostDeliveryPlanOrder):
        rs = EngageboostOrdermaster.objects.filter(id = EngageboostDeliveryPlanOrder.order_id, flag_order=0).exclude(order_status=4).order_by('sort_by_distance').all()
        rs_data = OrderListBillingaddressSerializer(rs, many=True)
        return rs_data.data

class DeliveryOrderListSerializer(serializers.ModelSerializer):
    DeliveryPlanOrder = serializers.SerializerMethodField()
    # OrderList = serializers.SerializerMethodField()
    # CustomerBillingAddress = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostDriverVeichleMap
        fields='__all__'
    def get_DeliveryPlanOrder(self, EngageboostDriverVeichleMap):
        rs = EngageboostDeliveryPlanOrder.objects.filter(virtual_vechile_id=EngageboostDriverVeichleMap.virtual_vechile_id, shipment_id=EngageboostDriverVeichleMap.shipment_id).all()
        rs_data = DeliveryPlanOrderViewSerializer(rs, many=True)
        return rs_data.data

class DeliveryOrdersSerializer(serializers.ModelSerializer):
    DeliveryPlanOrder = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostDriverVeichleMap
        fields='__all__'
    def get_DeliveryPlanOrder(self, EngageboostDriverVeichleMap):
        rs = EngageboostDeliveryPlanOrder.objects.filter(virtual_vechile_id=EngageboostDriverVeichleMap.virtual_vechile_id, shipment_id=EngageboostDriverVeichleMap.shipment_id).values('order_id').all()
        rs_data = DeliveryPlanOrderSerializer(rs, many=True)
        return rs_data.data

# *************************  End Delivery App *********************
class WarehouseSupplierMappingsSerializer(serializers.ModelSerializer):
    base_cost = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostWarehouseSupplierMappings
        fields='__all__'
    def get_base_cost(self, EngageboostWarehouseSupplierMappings):
        product_id = EngageboostWarehouseSupplierMappings.product_id
        warehouse_id = EngageboostWarehouseSupplierMappings.warehouse_id
        cost = ""
        PriceTypeObj = EngageboostProductPriceTypeMaster.objects.filter(price_type_id=1,product_id=product_id).last()
        
        if PriceTypeObj:
            CurrencyObj = EngageboostChannelCurrencyProductPrice.objects.filter(warehouse_id=warehouse_id,product_id=product_id,product_price_type_id=PriceTypeObj.id).last()
            if CurrencyObj: 
                cost = CurrencyObj.cost
        return cost

class AdditionalGlobalsettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostAdditionalGlobalsettings
        fields='__all__'

class GiftCardMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostGiftCardMasters
        fields='__all__'                

class CurrencyMaster_Serializer(serializers.ModelSerializer):
    engageboost_country=GlobalsettingscountriesSerializer()
    class Meta:
        model = EngageboostCurrencyMasters
        fields='__all__'

class BaseCurrencyRateSerializer(serializers.ModelSerializer):
    engageboost_currency_master=CurrencyMaster_Serializer()
    country=GlobalsettingscountriesSerializer()
    class Meta:
        model = EngageboostCurrencyRates
        fields='__all__'

class ProductActivitySerializer(serializers.ModelSerializer):
    customers = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostOrderActivity
        fields='__all__'

    def get_customers(self, EngageboostOrderActivity):
        orderObj = EngageboostOrdermaster.objects.filter(id=EngageboostOrderActivity.order_id)    
        if orderObj.count()>0:
            orderObj = orderObj.first()
            cust_ids = orderObj.customer_id
            if cust_ids!=None and cust_ids!="":
                rs = EngageboostCustomers.objects.filter(id=cust_ids, isblocked='n', isdeleted='n').annotate(name=Concat('first_name', Value(' '), 'last_name'))
                if rs.count()>0:
                    rs = rs.first()
                    #podata = CustomerGroupSerializer(rs, many=True)
                    return rs.name    
# *************************  Elastic Search Serializer *********************
class CustomerGroupSerializer_elastic(serializers.ModelSerializer):
    customers = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostCustomerGroup
        fields='__all__'

    def get_customers(self, EngageboostCustomerGroup):
        cust_ids = EngageboostCustomerGroup.customer_ids
        if cust_ids!=None and cust_ids!="":
            ids = cust_ids.split(',')
            rs = EngageboostCustomers.objects.filter(id__in=ids, isblocked='n', isdeleted='n').values_list('email', flat=True)
            names = ",".join(rs)
            #podata = CustomerGroupSerializer(rs, many=True)
            return names

class ProductCategoriesSerializer_elastic(serializers.ModelSerializer):
    category = CategoriesSerializer()
    class Meta:
        model = EngageboostProductCategories
        # fields = ('id','is_parent','category_id','product_id','isblocked','isdeleted','created','createdby','ip_address','modified','updatedby','parent_id')
        fields='__all__'

class BasicinfoSerializer_elastic(serializers.ModelSerializer):
    customer_group = CustomerGroupSerializer_elastic(read_only=True)
    # max_price_rule = ProductpriceroulSerializer(read_only=True)
    # min_price_rule = ProductpriceroulSerializer(read_only=True)
    product_images = ProductImagesSerializer(many=True, read_only=True)
    product_stock = StockSerializer(many=True)
    barcode_product_id = MultipleBarcodeSerializer(many=True)
    taxclass = ProducttaxclassesSerializer()
    po_taxclass = ProducttaxclassesSerializer() 
    product_list = ProductCategoriesSerializer_elastic(many=True)
    
    # taxclass = serializers.SerializerMethodField()
    # po_taxclass = serializers.SerializerMethodField()
    # channel_currency_product_price = serializers.SerializerMethodField()
    # supplier = serializers.SerializerMethodField()
    # category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    brand_id = serializers.SerializerMethodField()
    brand_slug = serializers.SerializerMethodField()
    visibility_id = serializers.SerializerMethodField()
    # barcode = serializers.SerializerMethodField()
    # inventory = serializers.SerializerMethodField()
    # category_id = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()
    # variations = serializers.SerializerMethodField()
    lang_data = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProducts
        # fields='__all__'
        fields = ('id','website_id','customer_group','name','sku','meta_url','meta_title','meta_key_word',
            'meta_description','description','taxclass','po_taxclass','visibility_id','supplier_id','brand','default_price',
            'isblocked','isdeleted','created','modified','veg_nonveg_type','uom','product_stock','barcode_product_id','product_images',
            'product_list','brand_id','lang_data','unit','brand_slug','slug','mp_system_requirements','weight','features')
        # depth=10
    
    def get_unit(self, EngageboostProducts):
        UOM = EngageboostProducts.uom
        if UOM is not None:
            obj = EngageboostUnitMasters.objects.filter(isblocked='n', isdeleted='n')
            if UOM.isnumeric()==True:
                rs_uom = obj.filter(id=int(EngageboostProducts.uom)).first()
            else:
                rs_uom = obj.filter(unit_name=EngageboostProducts.uom).first()
            if rs_uom:
                return rs_uom.unit_name
            else:
                return ''
        else:
            return ''

    def get_brand(self, EngageboostProducts):
        brandarr=[];
        brand_id = EngageboostProducts.brand
        if brand_id!="" and brand_id!=None:
            brands=brand_id.split(",")
            for bid in brands:
                if bid:
                    fetch_brand=EngageboostBrandMasters.objects.filter(id=bid,isdeleted='n',isblocked='n')
                    if fetch_brand.count()>0:
                        brandarr.append(fetch_brand.first().name)
            brand=','.join([str(i) for i in brandarr])
            brands_name=brand
        else:   
            brands_name=''
        return brands_name
    def get_brand_id(self, EngageboostProducts):
        brandarr=[];
        brand_id = EngageboostProducts.brand
        if brand_id:
            brands=brand_id.split(",")
        else:   
            brands=[]
        return brands

    def get_brand_slug(self, EngageboostProducts):
        brandarr=[];
        brand_id = EngageboostProducts.brand
        brands_slug = ""
        if brand_id:
            brands=brand_id.split(",")
            brands=EngageboostBrandMasters.objects.filter(id=brands[0],isdeleted='n',isblocked='n')
            if brands.count()>0:
                brands_slug = brands.first().slug
        else:   
            brands_slug = ""
        return brands_slug

    def get_visibility_id(self, EngageboostProducts):
        v_id = EngageboostProducts.visibility_id
        if v_id==1:
            visibility_id='Catalog Search'
        else:
            visibility_id='Not Visible..'
        return visibility_id

    def get_lang_data(self, EngageboostProducts):
        rs_lang = EngageboostProductMastersLang.objects.filter(product_id=EngageboostProducts.id, isblocked='n', isdeleted='n').all()
        lang_data = EngageboostProductMastersLangSerializer(rs_lang, many=True)
        return lang_data.data

class CategoriesSerializer_elastic(serializers.ModelSerializer):
    lang_data = serializers.SerializerMethodField()
    parent_category = serializers.SerializerMethodField() 
    class Meta:
        model = EngageboostCategoryMasters
        fields='__all__'
    def get_lang_data(self, EngageboostCategoryMasters):
        rs_lang = EngageboostCategoryMastersLang.objects.filter(category_id=EngageboostCategoryMasters.id, isblocked='n', isdeleted='n').all()
        lang_data = EngageboostCategoryMastersLangSerializer(rs_lang, many=True)
        return lang_data.data
    def get_parent_category(self, EngageboostCategoryMasters):
        return g_parent_category(EngageboostCategoryMasters.id)

class CustomerSerializer_elastic(serializers.ModelSerializer):
    auth_user=UserSerializer()
    country=GlobalsettingscountriesSerializer()
    customer_group=CustomerGroupSerializer()
    totalorder = serializers.SerializerMethodField()
    avgorder = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostCustomers
        fields='__all__'
        depth =1
    def get_totalorder(self, EngageboostCustomers):
        customer_id=EngageboostCustomers.id
        count=EngageboostOrdermaster.objects.filter(customer_id=customer_id).count()
        return count

    def get_avgorder(self, EngageboostCustomers):
        from django.db.models import Sum
        customer_id=EngageboostCustomers.id
        net_amount=EngageboostOrdermaster.objects.filter(customer_id=customer_id).aggregate(Sum('net_amount'))
        return net_amount['net_amount__sum']

class WarehousemastersSerializer_elastic(serializers.ModelSerializer):
    class Meta:
        model = EngageboostWarehouseMasters
        fields='__all__'

def g_parent_category(parent_id):
    if int(parent_id)>0:
        fetch_parent = EngageboostCategoryMasters.objects.filter(id=int(parent_id)).first()
        parent_category = fetch_parent.name
    else:
        parent_category = ''
    return parent_category
# *************************  Elastic Search Serializer *********************
class CustomFieldMastersLangSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCustomFieldMastersLang
        fields='__all__'

class EngageboostCategoryWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCategoryWarehouse
        fields = '__all__'
class DefaultsFieldsWithLangSerializer(serializers.ModelSerializer):
    lang_data = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostDefaultsFields
        fields='__all__'

    def get_lang_data(self, EngageboostDefaultsFields):
        if self.context.get("category_id"):
            category_id = self.context.get("category_id")
            rs_lang = EngageboostCustomFieldMastersLang.objects.filter(field_id=EngageboostDefaultsFields.id,category_id=category_id, isblocked='n', isdeleted='n').all()
        else:
            rs_lang = EngageboostCustomFieldMastersLang.objects.filter(field_id=EngageboostDefaultsFields.id, isblocked='n', isdeleted='n').all()
        lang_data = CustomFieldMastersLangSerializer(rs_lang, many=True)
        return lang_data.data


class DefaultModuleLayoutFieldsProductSerializer(serializers.ModelSerializer):
    lang_data = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostDefaultModuleLayoutFields
        fields='__all__'

    def get_lang_data(self, EngageboostDefaultModuleLayoutFields):
        rs_lang = EngageboostCustomFieldMastersLang.objects.filter(field_id=EngageboostDefaultModuleLayoutFields.field_id,category_id=EngageboostDefaultModuleLayoutFields.category_id, isblocked='n', isdeleted='n').all()
        lang_data = CustomFieldMastersLangSerializer(rs_lang, many=True)
        return lang_data.data

class EngageboostProductCustomFieldMastersLangSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductCustomFieldMastersLang
        fields='__all__'

class MarketplaceFieldValueSerializer(serializers.ModelSerializer):
    lang_data = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostMarketplaceFieldValue
        fields='__all__' 

    def get_lang_data(self, EngageboostMarketplaceFieldValue):
        rs_lang = EngageboostProductCustomFieldMastersLang.objects.filter(field_id=EngageboostMarketplaceFieldValue.field_id, product_id=EngageboostMarketplaceFieldValue.product_id, isblocked='n', isdeleted='n').all()
        lang_data = EngageboostProductCustomFieldMastersLangSerializer(rs_lang, many=True)

        return lang_data.data

class EngageboostOrderPriceChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostOrderPriceChange
        fields='__all__'

#serializers for category       
class CategoryMastersSerializer(serializers.ModelSerializer):

    class Meta:
        model = EngageboostCategoryMasters
        fields = ["id","parent_id","display_order","name","description","image","thumb_image","banner_image","page_title","meta_description","meta_keywords","category_url","slug","type","is_ebay_store_category","customer_group_id","display_mobile_app","applicable_imei","isadded_in_tally"]

class EngageboostCategoryMastersLangSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCategoryMastersLang
        fields=['id','language_id','language_code','category_id','field_name','field_value']

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
        rs_lang = EngageboostCategoryMastersLang.objects.filter(category_id=EngageboostCategoryMasters.id, isblocked='n', isdeleted='n').all()
        lang_data = EngageboostCategoryMastersLangSerializer(rs_lang, many=True)
        return lang_data.data

#************************** Product Serializer**********************************************
class ProductimagesnewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductimages
        fields = ['is_cover','img']

class BrandMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostBrandMasters
        fields = ['id', 'name']

class ProductStocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostProductStocks
        fields = ['product_id', 'real_stock', 'warehouse_id']


class CrossProductsViewSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()
    #stock_data = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProducts
        fields = ['id','name','sku','default_price','weight','slug','veg_nonveg_type','brand','product_image','website_id']
    
    def get_product_image(self, EngageboostProducts):
        qs = EngageboostProductimages.objects.filter(product_id=EngageboostProducts.id, status=0).all()
        product_image = ProductimagesnewSerializer(qs, many=True)
        return product_image.data


class ProductSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()
    stock_data = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostProducts
        fields = ['id','name','sku','default_price','weight','slug','veg_nonveg_type','product_image','stock_data','brand','website_id']
    
    def get_product_image(self, EngageboostProducts):
        qs = EngageboostProductimages.objects.filter(product_id=EngageboostProducts.id).all()
        product_image = ProductimagesnewSerializer(qs, many=True)
        return product_image.data

    def get_stock_data(self, EngageboostProducts):
        if self.context.get('warehouse_id'):
            warehouse_id = self.context.get('warehouse_id')
            qs_stock_data = EngageboostProductStocks.objects.filter(product_id=EngageboostProducts.id, warehouse_id=warehouse_id).first()
            products_stock = ProductStocksSerializer(qs_stock_data)
            return products_stock.data
                    

class DealsOfTheDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostDiscountMasters
        fields = ['product_id']


class ProductListByCategoriesSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = EngageboostProductCategories
        fields = ['id', 'category_id', 'product']

#**************************End Product Serializer*******************************************************************************************

#**************************************************Banners serializers*********************************************************************


class CategoryBannersImagesNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostCategoryBannersImages
        fields ='__all__'

class CategoryBannersNewSerializer(serializers.ModelSerializer):
    #banner_images = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostCategoryBanners
        fields=['id','website_id','banner_name','category_id','order_no','banner_type','parent_id'] 
    # def get_banner_images(self, EngageboostCategoryBanners):
    #     if self.context.get('applicable_for'):
    #         applicable_for = self.context.get('applicable_for')
    #         qs_bannerimg = EngageboostCategoryBannersImages.objects.filter(category_banner_id=EngageboostCategoryBanners.id, applicable_for=applicable_for,isdeleted='n',isblocked='n').all()
    #         banner_image = CategoryBannersImagesNewSerializer(qs_bannerimg, many=True)
    #         return banner_image.data

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

#**********************cmsmenu serializer********************************************************************************************************
class PagesSerializerNew(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPages
        fields=['id','page_name','page_title','url','meta_key','meta_data','meta_desc']

class CmsMenusNewSerializer(serializers.ModelSerializer):
    page_details = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostCmsMenus
        fields=['id','parent_id','page_id','page_details']

    def get_page_details(self, EngageboostCmsMenus):
        if self.context.get('website_id'):
            website_id = self.context.get('website_id')
            page_qs = EngageboostPages.objects.filter(id=EngageboostCmsMenus.page_id,isblocked='n',isdeleted='n',company_website_id=website_id).all()
            page_data = PagesSerializerNew(page_qs,many=True)
            return page_data.data

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

class EngageboostMastercardPgReturnDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostMastercardPgReturnDetails
        fields = "__all__"  


class OrderMasterSerializerReportSerializer(serializers.ModelSerializer):
    # order_products = OrderProductsSerializer(many=True)
    order_products = OrderProductsSerializerListView(many=True)
    invoice_order  = InvoicemasterViewSerializer(many=True)
    store_details = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostOrdermaster
        fields= ["id", "custom_order_id", "gross_amount", "net_amount", "shipping_cost","payment_method_id", "payment_type_id", "payment_method_name","order_status", "buy_status","billing_name","billing_email_address","created", "assign_wh","store_details", "order_products", "invoice_order"]
        read_only_fields = fields
    def get_store_details(self, EngageboostOrdermaster):
        str_warehouse = {"store_code":"","store_name":""}
        rs_warehouse = EngageboostWarehouseMasters.objects.filter(id=EngageboostOrdermaster.assign_wh).first()
        if rs_warehouse:
            str_warehouse["store_code"] = rs_warehouse.code
            str_warehouse["store_name"] = rs_warehouse.name
        
        return str_warehouse

class OrderMasterSerializerReportCustomerSerializer(serializers.ModelSerializer):
    # order_products = OrderProductsSerializer(many=True)
    order_products = OrderProductsSerializerListView(many=True)
    invoice_order = InvoicemasterViewSerializer(many=True)
    store_details = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()

    class Meta:
        model = EngageboostOrdermaster
        fields = ["id", "custom_order_id", "gross_amount", "net_amount", "shipping_cost", "payment_method_id",
                  "payment_type_id", "payment_method_name", "order_status", "buy_status", "billing_name",
                  "billing_email_address", "created", "assign_wh", "store_details", "order_products", "invoice_order",
                  "customer", "delivery_email_address"]
        read_only_fields = fields

    def get_store_details(self, EngageboostOrdermaster):
        str_warehouse = {"store_code": "", "store_name": ""}
        rs_warehouse = EngageboostWarehouseMasters.objects.filter(id=EngageboostOrdermaster.assign_wh).first()
        if rs_warehouse:
            str_warehouse["store_code"] = rs_warehouse.code
            str_warehouse["store_name"] = rs_warehouse.name

        return str_warehouse

    def get_customer(self, EngageboostOrdermaster):
        str_customer = {"first_name": "", "last_name": ""}
        rs_customer = EngageboostCustomers.objects.filter(id=EngageboostOrdermaster.customer_id).first()
        if rs_customer:
            str_customer["first_name"] = '' if rs_customer.first_name == None else rs_customer.first_name
            str_customer["last_name"] = '' if rs_customer.last_name == None else rs_customer.last_name

        return str_customer
# class EngageboostCategoriesSerializer(serializers.ModelSerializer):
#     product_count = serializers.SerializerMethodField()
#     child = serializers.SerializerMethodField()
#     class Meta:
#         model = EngageboostCategoryMasters
#         fields=("id","parent_id","display_order","name","description","image","thumb_image","banner_image","page_title","meta_description","meta_keywords","category_url","slug","type","website_id","is_ebay_store_category","customer_group_id","display_mobile_app","show_navigation","product_count","child")
#         #fields ='__all__'
#     def get_child(self,EngageboostCategoryMasters):
#         seri_data = categorymasters.objects.filter(parent_id=EngageboostCategoryMasters.id, isblocked='n', isdeleted='n').all()    
#         obj_seridata = EngageboostCategoriesSerializer(seri_data,many=True)
#         return obj_seridata.data
#     def get_product_count(self, EngageboostCategoryMasters):
#         lst_cat = categorymasters.objects \
#                         .filter(
#                             parent_id=EngageboostCategoryMasters.id,
#                             isdeleted='n',
#                             isblocked='n').values_list('id',flat=True)
#         if(lst_cat):
#             lst_cat = list(lst_cat)
#             lst_cat.append(EngageboostCategoryMasters.id)
#         else:
#             lst_cat = [EngageboostCategoryMasters.id]
#         product_lst = EngageboostProductCategories.objects.filter(category_id__in=lst_cat,product__visibility_id=1, isblocked='n', isdeleted='n').values_list('product_id',flat=True)
#         cnt_prod = EngageboostChannelCurrencyProductPrice.objects.filter(product_id__in = list(product_lst)).distinct().count()
#         return cnt_prod
# class CategoryBannersNewSerializer(serializers.ModelSerializer):
#     # banner_images = serializers.SerializerMethodField()
#     class Meta:
#         model = EngageboostCategoryBanners
#         fields=['id','website_id','banner_name','category_id','order_no','banner_type','parent_id']

#******** Picking App Serializer *************
class PickerBasicinfoSerializer(serializers.ModelSerializer):
    category_id = serializers.SerializerMethodField()
    uom_name = serializers.SerializerMethodField()
    channel_currency_product_price = serializers.SerializerMethodField()
    product_stock = serializers.SerializerMethodField()
    product_images = ProductImagesSerializer(many=True, read_only=True)
    class Meta:
        model = EngageboostProducts
        fields='__all__'
    def get_product_stock(self, EngageboostProducts):
        if self.context.get("warehouse_id"):
            warehouse_id =self.context.get("warehouse_id")
            product_stock = EngageboostProductStocks.objects.filter(product_id = EngageboostProducts.id,warehouse_id=warehouse_id,isblocked='n',isdeleted='n').order_by('-id').first()
            if product_stock:
                product_stock_serializer = StockViewSerializer(product_stock, partial=True)
                product_stock_serializer = product_stock_serializer.data
            else:
                product_stock_serializer = {"stock": 0,"safety_stock": 0,"virtual_stock": 0,"real_stock": 0}
        else:
            product_stock_serializer = {"stock": 0,"safety_stock": 0,"virtual_stock": 0,"real_stock": 0}
        return product_stock_serializer
    def get_channel_currency_product_price(self, EngageboostProducts):
        if self.context.get("warehouse_id"):
            warehouse_id =self.context.get("warehouse_id")
            price_obj = EngageboostChannelCurrencyProductPrice.objects.filter(product_id = EngageboostProducts.id,price__gte=0,product_price_type_id__price_type_id=1,warehouse_id=warehouse_id).order_by('-id').first()
        # else:
        #     price_obj = EngageboostChannelCurrencyProductPrice.objects.filter(product_id = EngageboostProducts.id,price__gte=0,product_price_type_id__price_type_id=1).order_by('-id').first()
            if price_obj:
                channelprice = ChannelCurrencyProductPriceSerializer(price_obj, partial=True)
                channelprice = channelprice.data
            else:
                channelprice = {"id": 0, "price_type": 1, "price": float(0),"cost": float(0),"mrp": float(0)}
        else:
            channelprice = {"id": 0, "price_type": 1, "price": float(0),"cost": float(0),"mrp": float(0)}
        return channelprice
    def get_uom_name(self, EngageboostProducts):
        UOM = EngageboostProducts.uom
        if UOM is not None:
            if UOM.isnumeric()==True:
                rs_uom = EngageboostUnitMasters.objects.filter(id=int(EngageboostProducts.uom), isblocked='n', isdeleted='n').first()
                if rs_uom:
                    return rs_uom.unit_name
                else:
                    return ''
            else:
                rs_uom = EngageboostUnitMasters.objects.filter(unit_name=EngageboostProducts.uom, isblocked='n', isdeleted='n').first()
                if rs_uom:
                    return rs_uom.unit_name
                else:
                    return ''
        else:
            return ''
    def get_category_id(self, EngageboostProducts):
        rs = EngageboostProductCategories.objects.filter(product_id=EngageboostProducts.id,isdeleted='n',isblocked='n').values('category_id','category_id__name', 'category_id__slug').first()
        if rs:
            data = rs['category_id']
        else:
            data = ""
        return data

class OrderListSerializerPickingApp(serializers.ModelSerializer):
    # order_products = OrderProductsSerializer(many=True)
    customer        = CustomerViewSerializer(read_only = True)
    order_activity  = serializers.SerializerMethodField()
    order_shipment  = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostOrdermaster
        fields='__all__'

    def get_order_activity(self, EngageboostOrdermaster):
        rs = EngageboostOrderActivity.objects.filter(order_id=EngageboostOrdermaster.id).order_by('-id').first()
        serializer = OrderActivitySerializer(rs)
        return serializer.data
    def get_order_shipment(self, EngageboostOrdermaster):
        shipment_details  = EngageboostShipments.objects.filter(id=EngageboostOrdermaster.shipment_id).order_by('-id').first()
        if shipment_details:
            shipmenrserializer = ShipmentsSerializer(shipment_details)
            shipmenrserializer = shipmenrserializer.data
        else:
            shipmenrserializer = {}
        return shipmenrserializer

class OrderAndOrderProductAndOrderSubstituteProductSerializer(serializers.ModelSerializer):
    # order_products = OrderProductsSerializer(many=True)
    order_products = serializers.SerializerMethodField()
    order_substitute_products = serializers.SerializerMethodField()
    customer        = CustomerViewSerializer(read_only = True)
    customer_addressbook  = serializers.SerializerMethodField()
    order_activity  = serializers.SerializerMethodField()
    order_shipment  = serializers.SerializerMethodField()
    invoice_number = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostOrdermaster
        fields='__all__'
    def get_customer_addressbook(self, EngageboostOrdermaster):
        if EngageboostOrdermaster.address_book_id is None or EngageboostOrdermaster.address_book_id == "":
            abserializer = {}
        else:
            addressbook_cond = EngageboostCustomersAddressBook.objects.filter(id=EngageboostOrdermaster.address_book_id).values('lat_val','long_val').first()
            if addressbook_cond:
                abserializer = CustomersAddressBookSerializer(addressbook_cond, partial=True)
                abserializer = abserializer.data
            else:
                abserializer = {}
        return abserializer
    def get_order_activity(self, EngageboostOrdermaster):
        rs = EngageboostOrderActivity.objects.filter(order_id=EngageboostOrdermaster.id).all().order_by('-id')
        serializer = OrderActivitySerializer(rs, many=True)
        return serializer.data
    def get_order_shipment(self, EngageboostOrdermaster):
        shipment_details  = EngageboostShipments.objects.filter(id=EngageboostOrdermaster.shipment_id).order_by('-id').first()
        if shipment_details:
            shipmenrserializer = ShipmentsSerializer(shipment_details)
            shipmenrserializer = shipmenrserializer.data
        else:
            shipmenrserializer = {}
        return shipmenrserializer
    def get_invoice_number(self, EngageboostOrdermaster):
        invoice_details = EngageboostInvoicemaster.objects.filter(order_id=EngageboostOrdermaster.id).order_by('-id').first()
        if invoice_details:
            invoice_number = invoice_details.custom_invoice_id
        else:
            invoice_number = ""
        return invoice_number
    def get_order_products(self, EngageboostOrdermaster):
        if self.context.get("product_ids"):
            product_ids =self.context.get("product_ids")
            if product_ids:
                op_cond = EngageboostOrderProducts.objects.filter(order_id=EngageboostOrdermaster.id,pick_as_substitute='n',product_id__in=product_ids,quantity__gt=0).all().order_by('-id')
            else:
                op_cond = EngageboostOrderProducts.objects.filter(order_id=EngageboostOrdermaster.id,pick_as_substitute='n',quantity__gt=0).exclude(product_id__gte=0).all().order_by('-id')
        else:
            op_cond = EngageboostOrderProducts.objects.filter(order_id=EngageboostOrdermaster.id,pick_as_substitute='n',quantity__gt=0).all().order_by('-id')
        if op_cond:
            opserializer = OrderProductsSerializer(op_cond, many=True)
            opserializer = opserializer.data
        else:
            opserializer = []
        return opserializer
    def get_order_substitute_products(self, EngageboostOrdermaster):
        if EngageboostOrdermaster.flag_order == 1:
            if self.context.get("product_ids"):
                product_ids =self.context.get("product_ids")
                if product_ids:
                    osp_cond = EngageboostOrderProducts.objects.filter(order_id=EngageboostOrdermaster.id,pick_as_substitute='y',product_id__in=product_ids,quantity__gt=0).all().order_by('-id')
                else:                
                    osp_cond = EngageboostOrderProducts.objects.filter(order_id=EngageboostOrdermaster.id,pick_as_substitute='y',quantity__gt=0).exclude(product_id__gte=0).all().order_by('-id')
            else:
                osp_cond = EngageboostOrderProducts.objects.filter(order_id=EngageboostOrdermaster.id,pick_as_substitute='y',quantity__gt=0).all().order_by('-id')        
            if osp_cond:
                ospserializer = OrderProductsSerializer(osp_cond, many=True)
                ospserializer = ospserializer.data
            else:
                ospserializer = []
        else:
            if self.context.get("product_ids"):
                product_ids =self.context.get("product_ids")
                if product_ids:
                    osp_cond = EngageboostOrderSubstituteProducts.objects.filter(order_id=EngageboostOrdermaster.id,pick_as_substitute='y',product_id__in=product_ids,quantity__gt=0).all().order_by('-id')
                else:                
                    osp_cond = EngageboostOrderSubstituteProducts.objects.filter(order_id=EngageboostOrdermaster.id,pick_as_substitute='y',quantity__gt=0).exclude(product_id__gte=0).all().order_by('-id')
            else:
                osp_cond = EngageboostOrderSubstituteProducts.objects.filter(order_id=EngageboostOrdermaster.id,pick_as_substitute='y',quantity__gt=0).all().order_by('-id')        
            if osp_cond:
                ospserializer = OrderSubstituteProductsSerializer(osp_cond, many=True)
                ospserializer = ospserializer.data
            else:
                ospserializer = []
        return ospserializer

class OrderAndOrderProductAndOrderSubstituteProductSerializerCustomerapp(serializers.ModelSerializer):
    # order_products = OrderProductsSerializer(many=True)
    order_products = serializers.SerializerMethodField()
    # order_substitute_products = serializers.SerializerMethodField()
    customer        = CustomerViewSerializer(read_only = True)
    customer_addressbook  = serializers.SerializerMethodField()
    order_activity  = serializers.SerializerMethodField()
    order_shipment  = serializers.SerializerMethodField()
    class Meta:
        model = EngageboostOrdermaster
        fields='__all__'
    def get_customer_addressbook(self, EngageboostOrdermaster):
        if EngageboostOrdermaster.address_book_id is None or EngageboostOrdermaster.address_book_id == "":
            abserializer = {}
        else:
            addressbook_cond = EngageboostCustomersAddressBook.objects.filter(id=EngageboostOrdermaster.address_book_id).values('lat_val','long_val').first()
            if addressbook_cond:
                abserializer = CustomersAddressBookSerializer(addressbook_cond, partial=True)
                abserializer = abserializer.data
            else:
                abserializer = {}
        return abserializer
    def get_order_activity(self, EngageboostOrdermaster):
        rs = EngageboostOrderActivity.objects.filter(order_id=EngageboostOrdermaster.id).all().order_by('-id')
        serializer = OrderActivitySerializer(rs, many=True)
        return serializer.data
    def get_order_shipment(self, EngageboostOrdermaster):
        shipment_details  = EngageboostShipments.objects.filter(id=EngageboostOrdermaster.shipment_id).order_by('-id').first()
        if shipment_details:
            shipmenrserializer = ShipmentsSerializer(shipment_details)
            shipmenrserializer = shipmenrserializer.data
        else:
            shipmenrserializer = {}
        return shipmenrserializer
    def get_order_products(self, EngageboostOrdermaster):
        if self.context.get("product_ids"):
            product_ids =self.context.get("product_ids")
            if product_ids:
                op_cond = EngageboostOrderProducts.objects.filter(order_id=EngageboostOrdermaster.id,pick_as_substitute='n',product_id__in=product_ids,quantity__gt=0).all().order_by('-id')
            else:
                op_cond = EngageboostOrderProducts.objects.filter(order_id=EngageboostOrdermaster.id,pick_as_substitute='n',quantity__gt=0).exclude(product_id__gte=0).all().order_by('-id')
        else:
            product_ids_has_substitute = EngageboostOrderSubstituteProducts.objects.filter(order_id=EngageboostOrdermaster.id,pick_as_substitute='y',quantity__gt=0).values_list('substitute_product_id',flat=True)
            op_cond = EngageboostOrderProducts.objects.filter(order_id=EngageboostOrdermaster.id,pick_as_substitute='n',quantity__gt=0).filter(product_id__in=product_ids_has_substitute).all().order_by('-id')
        if op_cond:
            opserializer = OrderProductsSerializer(op_cond, many=True)
            opserializer = opserializer.data
        else:
            opserializer = []
        return opserializer
    # def get_order_substitute_products(self, EngageboostOrdermaster):
    #     if self.context.get("product_ids"):
    #         product_ids =self.context.get("product_ids")
    #         if product_ids:
    #             osp_cond = EngageboostOrderProducts.objects.filter(order_id=EngageboostOrdermaster.id,pick_as_substitute='y',product_id__in=product_ids,quantity__gt=0).all().order_by('-id')
    #         else:                
    #             osp_cond = EngageboostOrderProducts.objects.filter(order_id=EngageboostOrdermaster.id,pick_as_substitute='y',quantity__gt=0).exclude(product_id__gte=0).all().order_by('-id')
    #     else:
    #         osp_cond = EngageboostOrderProducts.objects.filter(order_id=EngageboostOrdermaster.id,pick_as_substitute='y',quantity__gt=0).all().order_by('-id')        
    #     if osp_cond:
    #         ospserializer = OrderProductsSerializer(osp_cond, many=True)
    #         ospserializer = ospserializer.data
    #     else:
    #         ospserializer = []
    #     return ospserializer


class EngageboostStoreTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostStoreType
        fields = '__all__'

class EngageboostPaymentWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageboostPaymentWarehouse
        fields = '__all__'

# class PickerCategoriesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EngageboostCategoryMasters
#         fields = ("id","name","description","parent_id","slug","category_url")
#         # fields='__all__'

class OrderAndOrderProductAndOrderSubstituteProductCSVSerializer(serializers.ModelSerializer):
    # order_products = OrderProductsSerializer(many=True)
    order_products = serializers.SerializerMethodField()

    class Meta:
        model = EngageboostOrdermaster
        fields='__all__'

    def get_order_products(self, EngageboostOrdermaster):
        op_cond = EngageboostOrderProducts.objects.filter(order_id=EngageboostOrdermaster.id,pick_as_substitute='n',quantity__gt=0).all().order_by('-id')
        if op_cond:
            opserializer = OrderProductsSerializer(op_cond, many=True)
            opserializer = opserializer.data
        else:
            opserializer = []
        return opserializer
