from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from datetime import datetime
class EngageboostRolemasters(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    company_id = models.IntegerField()
    group_id = models.BigIntegerField()
    name = models.CharField(max_length=250,blank=True, null=True)
    user_role_type = models.CharField(max_length=255, default='Super Admin',blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices, default='n')
    createdby = models.IntegerField(default='0',blank=True, null=True)
    updatedby = models.IntegerField(default='0',blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    language_id = models.IntegerField(default='0',blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True,default='0')
    class Meta:
        db_table = 'engageboost_rolemasters'

class EngageboostCountries(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    country_name = models.CharField(max_length=255,blank=True, null=True)
    country_code = models.CharField(max_length=2,blank=True, null=True)
    countries_iso_code_3 = models.CharField(max_length=3,blank=True, null=True)
    ebay_countrycode = models.CharField(max_length=255, blank=True, null=True)
    address_format_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    createdby = models.IntegerField(default='0',blank=True, null=True)
    updatedby = models.IntegerField(default='0',blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_countries'

class EngageboostStates(models.Model):
    country_id = models.IntegerField()
    state_code = models.CharField(max_length=32)
    state_name = models.CharField(max_length=255)
    state_name_ar = models.CharField(max_length=255, blank=True, null=True)
    sap_ecustomer_state_no = models.CharField(max_length=255)
    sap_plant_no = models.CharField(max_length=255)
    class Meta:
        db_table = 'engageboost_states'

class EngageboostUsers(AbstractUser):
    enum_choices = (
      ('y', 'y'),
      ('n', 'n')
    )
    user_choices = (
      ('backend', 'backend'),
      ('frontend', 'frontend')
    )
    issuperadmin_choices = (
      ('Y', 'Y'),
      ('N', 'N')
    )
    company_id = models.BigIntegerField(blank=True, null=True)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    boost_url = models.CharField(max_length=255, blank=True, null=True)
    website_url = models.CharField(max_length=255, blank=True, null=True)
    company_logo = models.CharField(max_length=255, blank=True, null=True)
    employee_name = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    image_name = models.CharField(max_length=255, blank=True, null=True)
    reset_password=models.CharField(max_length=2,choices=enum_choices, default='n', blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(EngageboostCountries,on_delete=models.CASCADE, blank=True, null=True)
    role = models.ForeignKey(EngageboostRolemasters,on_delete=models.CASCADE, blank=True, null=True)
    issuperadmin = models.CharField(max_length=2,choices=issuperadmin_choices, default='N', blank=True, null=True)
    lead_manager_id = models.IntegerField(blank=True, null=True)
    createdby_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    modifiedby_id = models.IntegerField(blank=True, null=True)
    modified_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices, default='n', blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices, default='n', blank=True, null=True)
    is_verified=models.CharField(max_length=2,choices=enum_choices, default='n', blank=True, null=True)
    verified_code = models.CharField(max_length=30, blank=True, null=True)
    refferal_code = models.CharField(max_length=255, blank=True, null=True)
    google_login_id=models.CharField(max_length=255, blank=True, null=True)
    ip_address=models.CharField(max_length=255, blank=True, null=True)
    device_token_ios = models.TextField(blank=True, null=True)
    device_token_android = models.TextField(blank=True, null=True)
    user_type = models.CharField(max_length=10,choices=user_choices, default='frontend', blank=True, null=True)
    access_key = models.CharField(max_length=20, blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True, default=0)
    class Meta:
        db_table = 'auth_user'

class EngageboostEmailTypeContents(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    Type_CHOICES = (
        ('H', 'H'),
        ('T', 'T'),
        ('HT', 'HT')
    )
    Applied_CHOICES = (
        ('Others', 'Others'),
        ('Order', 'Order')
    )
    default_email_type_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    emarketing_website_template_id = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    subject = models.CharField(max_length=255,blank=True, null=True)
    email_type = models.CharField(max_length=2,choices=Type_CHOICES,default='T',blank=True, null=True)
    email_content = models.TextField(blank=True, null=True)
    email_content_text = models.TextField(blank=True, null=True)
    sms_subject = models.CharField(max_length=256, blank=True, null=True)
    sms_content_text = models.TextField(blank=True, null=True)
    notification_title = models.CharField(max_length=256, blank=True, null=True)
    notification_body = models.CharField(max_length=256, blank=True, null=True)
    notification_title_store = models.CharField(max_length=256, blank=True, null=True)
    notification_body_store = models.CharField(max_length=256, blank=True, null=True)
    reply_to_email = models.TextField(blank=True, null=True)
    bcc = models.CharField(max_length=255,blank=True, null=True)
    email_from = models.CharField(max_length=255,blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    file_name = models.CharField(max_length=100, blank=True, null=True)
    auto_responder_applied_for = models.CharField(max_length=20,choices=Applied_CHOICES,default='Others', null=True)
    shipment_status = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_email_type_contents'

class EngageboostApplicableAutoresponders(models.Model):
    Applicable_For_CHOICES = (
        ('Channel', 'Channel'),
        ('Warehouse', 'Warehouse'),
        ('ShippingProvider', 'ShippingProvider')
    )
    website_id = models.IntegerField()
    auto_responder = models.ForeignKey(EngageboostEmailTypeContents,on_delete=models.CASCADE,related_name='auto_responder',blank=True, null=True)
    applicable_chanel_id = models.IntegerField()
    applicable_for = models.CharField(max_length=20,choices=Applicable_For_CHOICES,default='Channel', blank=True, null=True)
    shipment_status = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    createdby = models.IntegerField(default='0')
    updatedby = models.IntegerField(default='0')
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_applicable_autoresponders'

class EngageboostCustomerGroup(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    customer_ids = models.TextField(blank=True, null=True)
    view_type = models.IntegerField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(default='0',blank=True, null=True)
    updatedby = models.IntegerField(default='0',blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_customer_group'

class EngageboostProductTaxClasses(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True, default='0')
    updatedby = models.IntegerField(blank=True, null=True, default='0')
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_tax_classes'

class EngageboostWarehouseMasters(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    website_id  = models.IntegerField(blank=True, null=True)
    name= models.CharField(max_length=255, blank=True, null=True)
    code= models.CharField(max_length=255, blank=True, null=True)
    contact_person  = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    country_id  = models.IntegerField(blank=True, null=True)
    state_id= models.IntegerField(blank=True, null=True)
    state_name  = models.CharField(max_length=255, blank=True, null=True)
    city= models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    phone   = models.CharField(max_length=255, blank=True, null=True)
    email   = models.CharField(max_length=255, blank=True, null=True)
    isblocked   = models.CharField(max_length=2,choices=enum_choices, default='n',blank=True, null=True)
    isdeleted   = models.CharField(max_length=2,choices=enum_choices, default='n',blank=True, null=True)
    channel_id  = models.IntegerField(blank=True, null=True)
    order_id_format = models.CharField(max_length=256, blank=True, null=True)
    shipping_id_format  = models.CharField(max_length=256, blank=True, null=True)
    invoice_id_format   = models.CharField(max_length=256, blank=True, null=True)
    text_color  = models.CharField(max_length=100, blank=True, null=True)
    product_stock_code  = models.CharField(max_length=20, blank=True, null=True)
    latitude 			= models.CharField(max_length=255, blank=True, null=True)
    longitude 			= models.CharField(max_length=255, blank=True, null=True)
    max_distance_sales  = models.FloatField(blank=True, null=True, default='0')
    warehouse_logo = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified= models.DateField(blank=True, null=True)
    createdby   = models.IntegerField(default='0',blank=True, null=True)
    updatedby   = models.IntegerField(default='0',blank=True, null=True)
    ip_address  = models.CharField(max_length=255, blank=True, null=True)
    min_order_amount = models.FloatField(blank=True, null=True, default=0)
    expected_delivery_time = models.IntegerField(default='0',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_warehouse_masters'

class EngageboostRepricingMaximumMinRules(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    rule_for = models.CharField(max_length=250,blank=True, null=True)
    based_on = models.CharField(max_length=250,blank=True, null=True)
    changed_by_or_to = models.CharField(max_length=250,blank=True, null=True)
    changed_value = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_repricing_maximum_min_rules'

class EngageboostHsnCodeMaster(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, default='1', null=True)
    hsn_code = models.CharField(max_length=255, blank=True, null=True)
    sgst = models.IntegerField(default='0', blank=True, null=True)
    cgst = models.IntegerField(default='0', blank=True, null=True)
    igst = models.IntegerField(default='0', blank=True, null=True)
    cess = models.IntegerField(default='0', blank=True, null=True)
    ctcs = models.IntegerField(default='0', blank=True, null=True)
    stcs = models.IntegerField(default='0', blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_hsn_code_masters'

class EngageboostProducts(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    order_id = models.IntegerField(default=0,blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    customer_group = models.ForeignKey(EngageboostCustomerGroup,on_delete=models.CASCADE,blank=True, null=True)
    ebay_item_id = models.CharField(max_length=255, blank=True, null=True)
    amazon_itemid = models.CharField(max_length=255,blank=True, null=True)
    ebay_addstatus = models.TextField(blank=True, null=True)
    twitter_addstatus = models.TextField(blank=True, null=True)
    amazon_addstatus = models.TextField(blank=True, null=True)
    ebay_listing_starttime = models.CharField(max_length=255, blank=True, null=True)
    ebay_listing_endtime = models.CharField(max_length=255, blank=True, null=True)
    ebay_listing_build = models.TextField(blank=True, null=True)
    ebay_listing_version = models.CharField(max_length=255, blank=True, null=True)
    ebay_listing_time = models.CharField(max_length=255, blank=True, null=True)
    total_listingfee = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    weight = models.TextField(blank=True, null=True)
    meta_url = models.CharField(max_length=255, blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_key_word = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    shippingclass_id = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    taxclass = models.ForeignKey(EngageboostProductTaxClasses,on_delete=models.CASCADE,blank=True, null=True,related_name='taxclass')
    po_taxclass = models.ForeignKey(EngageboostProductTaxClasses,on_delete=models.CASCADE,blank=True, null=True,related_name='po_taxclass')
    visibility_id = models.IntegerField(blank=True, null=True)
    supplier_id = models.CharField(max_length=255, blank=True, null=True)
    warehouse = models.ForeignKey(EngageboostWarehouseMasters,on_delete=models.CASCADE,blank=True, null=True)
    status = models.CharField(max_length=255,blank=True, null=True)
    new_date = models.CharField(max_length=255, blank=True, null=True)
    isbn = models.TextField(blank=True, null=True)
    asin = models.TextField(blank=True, null=True)
    ean = models.TextField(blank=True, null=True)
    npn = models.CharField(max_length=255, blank=True, null=True)
    supc = models.CharField(max_length=60, blank=True, null=True)
    max_order_unit = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    video = models.CharField(max_length=255, blank=True, null=True)
    mp_description = models.TextField(blank=True, null=True)
    mp_features = models.TextField(blank=True, null=True)
    mp_system_requirements = models.TextField(blank=True, null=True)
    mp_templates = models.TextField(blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    last_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    avg_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    default_price = models.FloatField(blank=True, null=True)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    pdf_file_path = models.CharField(max_length=255, blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    is_import = models.TextField(blank=True, null=True)
    is_auctionable = models.IntegerField(blank=True, null=True)
    numberof_sale = models.IntegerField(default=0,blank=True, null=True)
    numberof_view = models.IntegerField(default=0,blank=True, null=True)
    ebay = models.IntegerField(default=0,blank=True, null=True)
    amazon = models.IntegerField(default=0,blank=True, null=True)
    webshop = models.IntegerField(default=0,blank=True, null=True)
    order_price = models.IntegerField(default=0,blank=True, null=True)
    slug = models.TextField(blank=True, null=True)
    best_selling = models.IntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    org_pro_con = models.CharField(max_length=50, blank=True, null=True)
    is_facebook_product = models.TextField(blank=True, null=True)
    max_price_rule = models.ForeignKey(EngageboostRepricingMaximumMinRules,on_delete=models.CASCADE,blank=True, null=True,related_name='max_price_rule')
    min_price_rule = models.ForeignKey(EngageboostRepricingMaximumMinRules,on_delete=models.CASCADE,blank=True, null=True,related_name='min_price_rule')
    sla = models.IntegerField(blank=True, null=True)
    veg_nonveg_type = models.TextField(blank=True, null=True)
    price_formula_id_for_customer = models.IntegerField(blank=True, null=True)
    price_formula_id_for_supplier = models.IntegerField(blank=True, null=True)
    uom = models.CharField(max_length=255, blank=True, null=True)
    product_offer_desc = models.CharField(max_length=256, blank=True, null=True)
    product_offer_start_date = models.DateField(blank=True, null=True)
    product_offer_end_date = models.DateField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    hsn_id = models.TextField(blank=True, null=True)
    visible_in_listing = models.CharField(max_length=10, blank=True, null=True,default='n')
    related_product_skus = models.TextField(blank=True, null=True)
    meta_og_tags = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_products'

class EngageboostCustomers(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    Gender_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )
    auth_user   = models.ForeignKey(EngageboostUsers,on_delete=models.CASCADE,default=0, blank=True, null=True, related_name='user_id')
    website_id  = models.IntegerField(blank=True, null=True)
    first_name  = models.CharField(max_length=50, blank=True, null=True)
    last_name   = models.CharField(max_length=255, blank=True, null=True)
    gender 					= models.CharField(max_length=20,choices=Gender_CHOICES, default='Male')
    ebayusername= models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    country 	= models.ForeignKey(EngageboostCountries,on_delete=models.CASCADE, blank=True, null=True)
    group_id= models.IntegerField(blank=True, null=True)
    email   = models.CharField(max_length=255, blank=True, null=True)
    password= models.CharField(max_length=60, blank=True, null=True)
    street  = models.CharField(max_length=255, blank=True, null=True)
    post_code   = models.CharField(max_length=255, blank=True, null=True)
    city= models.CharField(max_length=255, blank=True, null=True)
    state   = models.CharField(max_length=255, blank=True, null=True)
    perfix  = models.CharField(max_length=10, blank=True, null=True)
    suffix  = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    phone   = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    owner_id= models.IntegerField(blank=True, null=True)
    customer_group  = models.ForeignKey(EngageboostCustomerGroup,on_delete=models.CASCADE,blank=True, null=True)
    view_time   = models.DateTimeField(blank=True, null=True)
    assignment  = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified= models.DateTimeField(blank=True, null=True)
    createdby   = models.IntegerField(blank=True, null=True)
    updatedby   = models.IntegerField(blank=True, null=True)
    isdeleted   = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked   = models.CharField(max_length=2,choices=enum_choices,default='n')
    is_import   = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    ext_txt1= models.TextField(blank=True, null=True)
    orders  = models.IntegerField(blank=True, null=True)
    avgorder= models.DecimalField(max_digits=10, decimal_places=0,blank=True, null=True)
    totalorder  = models.DecimalField(max_digits=10, decimal_places=0,blank=True, null=True)
    lastlogin   = models.DateField(blank=True, null=True)
    is_guest_user   = models.SmallIntegerField(default=0,blank=True, null=True)
    facebook_id = models.CharField(max_length=255, blank=True, null=True)
    vat = models.CharField(max_length=100, blank=True, null=True)
    tin = models.CharField(max_length=100, blank=True, null=True)
    excise_regn_no  = models.CharField(max_length=100, blank=True, null=True)
    cst_no  = models.CharField(max_length=100, blank=True, null=True)
    refferal_code   = models.CharField(max_length=255, blank=True, null=True)
    device_token_ios= models.TextField(blank=True, null=True)
    device_token_android= models.TextField(blank=True, null=True)
    referrer_code   = models.CharField(max_length=255, blank=True, null=True)
    is_ledger_created   = models.CharField(max_length=20,blank=True, null=True)
    ip_address  = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_customers'

class EngageboostZoneMasters(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    location_type = models.TextField(blank=True, null=True)
    zone_id = models.IntegerField(blank=True, null=True)
    area_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    state_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    manager_id = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    office_address1 = models.CharField(max_length=500, blank=True, null=True)
    office_address2 = models.CharField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    min_order_amount = models.FloatField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_zone_masters'

class EngageboostCustomersAddressBook(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    customers_id= models.IntegerField(blank=True, null=True)
    area_id   		= models.IntegerField(blank=True, null=True)
    set_primary = models.SmallIntegerField(blank=True, null=True, default=0)
    is_selected = models.SmallIntegerField(blank=True, null=True, default=0)
    billing_name= models.CharField(max_length=255, blank=True, null=True)
    billing_company = models.CharField(max_length=128, blank=True, null=True)
    billing_email_address   = models.CharField(max_length=128, blank=True, null=True)
    billing_street_address  = models.TextField(blank=True, null=True)
    billing_street_address1 = models.CharField(max_length=255, blank=True, null=True)
    billing_landmark= models.CharField(max_length=256, blank=True, null=True)
    billing_city= models.CharField(max_length=255, blank=True, null=True)
    billing_postcode= models.CharField(max_length=255, blank=True, null=True)
    billing_state   = models.CharField(max_length=255, blank=True, null=True)
    billing_country = models.IntegerField(blank=True, null=True)
    billing_phone   = models.CharField(max_length=255, blank=True, null=True)
    billing_fax = models.CharField(max_length=255, blank=True, null=True)
    delivery_name   = models.CharField(max_length=255, blank=True, null=True)
    delivery_company= models.CharField(max_length=255, blank=True, null=True)
    delivery_email_address  = models.CharField(max_length=255, blank=True, null=True)
    delivery_street_address = models.TextField(blank=True, null=True)
    delivery_street_address1 = models.CharField(max_length=255, blank=True, null=True)
    delivery_landmark   = models.CharField(max_length=256, blank=True, null=True)
    delivery_city   = models.CharField(max_length=255, blank=True, null=True)
    delivery_postcode   = models.CharField(max_length=255, blank=True, null=True)
    delivery_state  = models.CharField(max_length=255, blank=True, null=True)
    delivery_country= models.IntegerField(blank=True, null=True)
    delivery_phone  = models.CharField(max_length=255, blank=True, null=True)
    delivery_fax= models.CharField(max_length=255, blank=True, null=True)
    lat_val = models.CharField(max_length=100, blank=True, null=True)
    long_val= models.CharField(max_length=100, blank=True, null=True)
    isdeleted   = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isblocked   = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified= models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_customers_address_book'

class EngageboostCustomerActivities(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    activity_msg = models.CharField(max_length=255, blank=True, null=True)
    activity_details = models.TextField(blank=True, null=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    class Meta:
        db_table = 'engageboost_customer_activities'

class EngageboostCustomerLoyaltypoints(models.Model):
    website_id  = models.IntegerField(blank=True, null=True)
    rule_id = models.IntegerField(blank=True, null=True)
    customer_id = models.BigIntegerField(blank=True, null=True)
    order_id= models.BigIntegerField(blank=True, null=True)
    custom_order_id = models.CharField(max_length=28,blank=True, null=True)
    customer_contact_no = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    received_points = models.IntegerField(blank=True, null=True)
    burnt_points= models.IntegerField(blank=True, null=True)
    amount  = models.FloatField(blank=True, null=True)
    received_burnt  = models.CharField(max_length=28, blank=True, null=True)
    status  = models.CharField(max_length=20, blank=True, null=True)
    burn_type   = models.CharField(max_length=20, blank=True, null=True)
    card_id = models.BigIntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified 			= models.DateTimeField(blank=True, null=True)
    valid_form  = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    remaining_balance = models.FloatField(blank=True, null=True)
    view_status = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'engageboost_customer_loyaltypoints'

class EngageboostCustomerProductReviews(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    postedon = models.DateTimeField(blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    reviewby = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    websiteid = models.IntegerField(blank=True, null=True)
    productid = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=15,blank=True, null=True)
    reviewbyname = models.CharField(max_length=222,blank=True, null=True)
    city = models.CharField(max_length=222,blank=True, null=True)
    emailid = models.CharField(max_length=222,blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_customer_product_reviews'

class EngageboostCustomerReturnStatus(models.Model):
    enum_choices = (
        ('Return Initiated', 'Return Initiated'),
        ('Return Confirmed', 'Return Confirmed')
    )
    customer_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    customer_return_status = models.CharField(max_length=20,choices=enum_choices,default='n', null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_customer_return_status'

class EngageboostCustomerTaxClasses(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    tax_class_name = models.CharField(max_length=255,blank=True, null=True)
    customer_type = models.IntegerField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    class Meta:
        db_table = 'engageboost_customer_tax_classes'

class EngageboostCustomerWiselists(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    product = models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE,blank=True, null=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    class Meta:
        db_table = 'engageboost_customer_wiselists'

class EngageboostChannels(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    image_small = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    is_on_product_setup = models.CharField(max_length=2,choices=enum_choices,default='y', blank=True, null=True)
    country_code = models.CharField(max_length=50, blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    website_code = models.CharField(max_length=255, blank=True, null=True)
    site = models.CharField(max_length=50, blank=True, null=True)
    website_name = models.CharField(max_length=200, blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n', blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n', blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    parent_logo = models.CharField(max_length=100, blank=True, null=True)
    parent_name = models.CharField(max_length=255, blank=True, null=True)
    test = models.IntegerField(blank=True, null=True)
    sandbox_login_link = models.CharField(max_length=255, blank=True, null=True)
    sandbox_api_link = models.CharField(max_length=255, blank=True, null=True)
    live_login_link = models.CharField(max_length=255, blank=True, null=True)
    live_api_link = models.CharField(max_length=255, blank=True, null=True)
    sandbox_app_id = models.CharField(max_length=255, blank=True, null=True)
    live_app_id = models.CharField(max_length=255, blank=True, null=True)
    live_cert_id = models.CharField(max_length=255, blank=True, null=True)
    live_runame = models.CharField(max_length=255)
    developer_id = models.CharField(max_length=255)
    compatibility_level = models.IntegerField(blank=True, null=True)
    sandbox_cert_id = models.CharField(max_length=255, blank=True, null=True)
    sandbox_runame = models.CharField(max_length=255, blank=True, null=True)
    channel_url = models.CharField(max_length=255, blank=True, null=True)
    amazon_fulfillment_center = models.CharField(max_length=250, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_channels'

class EngageboostChannelCategoryMappings(models.Model):
    channel_category_id = models.IntegerField(blank=True, null=True)
    channel_parent_category_id = models.IntegerField(blank=True, null=True)
    boost_parent_category_id = models.IntegerField(blank=True, null=True)
    boost_category_id = models.IntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_channel_category_mappings'

class EngageboostPriceTypeMaster(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_price_type_master'

class EngageboostProductPriceTypeMaster(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    product = models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE, blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    warehouse_id = models.TextField(blank=True, null=True)
    price_type = models.ForeignKey(EngageboostPriceTypeMaster,on_delete=models.CASCADE, blank=True, null=True)
    min_quantity = models.IntegerField(blank=True, null=True)
    max_quantity = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_product_price_type_master'

class EngageboostChannelCurrencyProductPrice(models.Model):
    channel_id = models.IntegerField(blank=True, null=True)
    currency_id = models.IntegerField(blank=True, null=True)
    product = models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE, blank=True, null=True, related_name='channel_price') # models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    mrp = models.FloatField(default='0', blank=True, null=True)
    min_quantity = models.IntegerField(blank=True, null=True)
    max_quantity = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    product_price_type = models.ForeignKey(EngageboostProductPriceTypeMaster,on_delete=models.CASCADE,related_name='product_price_type_master', blank=True, null=True)
    class Meta:
        db_table = 'engageboost_channel_currency_product_price'

class EngageboostTempProductPrice(models.Model):
    channel_id = models.IntegerField(blank=True, null=True)
    currency_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    sku = models.TextField(blank=True, null=True)
    warehouse_code = models.TextField(blank=True, null=True)
    price_type = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    mrp = models.FloatField(default='0', blank=True, null=True)
    min_quantity = models.IntegerField(blank=True, null=True)
    max_quantity = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    product_price_type = models.ForeignKey(EngageboostProductPriceTypeMaster,on_delete=models.CASCADE,related_name='temp_product_price_type_master', blank=True, null=True)
    file_name = models.TextField(blank=True, null=True)
    err_flag = models.IntegerField(blank=True, null=True)
    error_text = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_temp_product_price'


class EngageboostChannelErrors(models.Model):
    Type_CHOICES = (
        ('additem', 'additem'),
        ('order', 'order')
    )
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    channel_id = models.IntegerField(blank=True, null=True)
    company_website_id = models.IntegerField(blank=True, null=True)
    channel_site_id = models.IntegerField(blank=True, null=True)
    error_type = models.CharField(max_length=20,choices=Type_CHOICES, blank=True, null=True)
    item_id = models.BigIntegerField(blank=True, null=True)
    errorname = models.TextField(blank=True, null=True)
    errorcode = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_channel_errors'

class EngageboostChannelItemlistingfees(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    channel_id = models.IntegerField(blank=True, null=True)
    company_website_id = models.IntegerField(blank=True, null=True)
    channel_site_id = models.IntegerField(blank=True, null=True)
    product_id = models.BigIntegerField(blank=True, null=True)
    channel_item_id = models.CharField(max_length=255, blank=True, null=True)
    feename = models.CharField(max_length=255,blank=True, null=True)
    feevalue = models.CharField(max_length=255,blank=True, null=True)
    currency = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_channel_itemlistingfees'

class EngageboostChannelOrdertransactions(models.Model):
    order_id = models.CharField(max_length=255, blank=True, null=True)
    buyeremailid = models.CharField(max_length=255, blank=True, null=True)
    orderstatus = models.CharField(max_length=255, blank=True, null=True)
    item_id = models.CharField(max_length=255, blank=True, null=True)
    adjustmentamount = models.CharField(max_length=255, blank=True, null=True)
    amountpaid = models.CharField(max_length=255, blank=True, null=True)
    externaltransactionid = models.CharField(max_length=255, blank=True, null=True)
    externaltransactiontime = models.CharField(max_length=255, blank=True, null=True)
    feeorcreditamount = models.CharField(max_length=255, blank=True, null=True)
    paymentrefundamount = models.CharField(max_length=255, blank=True, null=True)
    sellingmanagersalesrecordnumber = models.CharField(max_length=255, blank=True, null=True)
    transactionid = models.CharField(max_length=255, blank=True, null=True)
    transactionprice = models.CharField(max_length=255, blank=True, null=True)
    actualshippingcost = models.CharField(max_length=255, blank=True, null=True)
    actualhandlingcost = models.CharField(max_length=255, blank=True, null=True)
    orderlineitemid = models.CharField(max_length=255, blank=True, null=True)
    eiastoken = models.TextField(blank=True, null=True)
    channel_record_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_channel_ordertransactions'

class EngageboostChannelSettings(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    channel_id = models.IntegerField(blank=True, null=True)
    company_website_id = models.IntegerField(blank=True, null=True)
    channel_site_id = models.IntegerField(blank=True, null=True)
    defaultprimarycategory = models.CharField(max_length=255,blank=True, null=True)
    defaultsecondarycategory = models.CharField(max_length=255,blank=True, null=True)
    listing_type = models.CharField(max_length=255, blank=True, null=True)
    listing_duration = models.CharField(max_length=255, blank=True, null=True)
    item_condition = models.CharField(max_length=255, blank=True, null=True)
    return_policy = models.CharField(max_length=255, blank=True, null=True)
    refund_givenas = models.CharField(max_length=255, blank=True, null=True)
    refund_within = models.CharField(max_length=255, blank=True, null=True)
    return_shipping_paidby = models.CharField(max_length=255, blank=True, null=True)
    refund_desc = models.TextField(blank=True, null=True)
    paymentmethod = models.CharField(max_length=255, blank=True, null=True)
    ebay_paymentmethod = models.TextField(blank=True, null=True)
    shipping_required = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    max_shipping_cost = models.FloatField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_channel_settings'

class EngageboostChannelShippingMaps(models.Model):
    Shipping_CHOICES = (
        ('domestic', 'domestic'),
        ('international', 'international')
    )
    channel_id = models.IntegerField(blank=True, null=True)
    channel_site_id = models.IntegerField(blank=True, null=True)
    company_website_id = models.IntegerField(blank=True, null=True)
    channel_shippingservice_serviceid = models.IntegerField(blank=True, null=True)
    shipping_master_setting_id = models.IntegerField(blank=True, null=True)
    shipping_type = models.CharField(max_length=255, blank=True, null=True)
    shipping_additional_cost = models.FloatField(blank=True, null=True)
    dispatch_time_max = models.IntegerField()
    shippto = models.CharField(max_length=20,choices=Shipping_CHOICES,default='domestic', null=True)
    class Meta:
        db_table = 'engageboost_channel_shipping_maps'

class EngageboostChannelShippingservices(models.Model):
    enum_choices = (
        ('Y', 'Y'),
        ('N', 'N')
    )
    channel_id = models.IntegerField(blank=True, null=True)
    channel_site_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    shipping_service_id = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    service_id = models.IntegerField(blank=True, null=True)
    shipping_timemax = models.IntegerField(blank=True, null=True)
    shipping_timemin = models.IntegerField(blank=True, null=True)
    service_type = models.CharField(max_length=255, blank=True, null=True)
    shipping_package = models.TextField(blank=True, null=True)
    dimension_required = models.CharField(max_length=2,choices=enum_choices,default='N', null=True)
    surchargeapplicable = models.CharField(max_length=2,choices=enum_choices,default='N', null=True)
    expeditedservice = models.CharField(max_length=2,choices=enum_choices,default='N', null=True)
    internationalservice = models.CharField(max_length=2,choices=enum_choices,default='N', null=True)
    dimensionsrequired = models.CharField(max_length=2,choices=enum_choices,default='N', null=True)
    shippingcarrier = models.CharField(max_length=255, blank=True, null=True)
    shippingservicepackagedetail = models.TextField(blank=True, null=True)
    weightrequired = models.CharField(max_length=2,choices=enum_choices,default='N', null=True)
    shippingcategory = models.CharField(max_length=255, blank=True, null=True)
    detailversion = models.CharField(max_length=255, blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='N', null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='N', null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_channel_shippingservices'

class EngageboostChannelSites(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    channel_id = models.BigIntegerField(blank=True, null=True)
    website_name = models.CharField(max_length=255,blank=True, null=True)
    website_url = models.CharField(max_length=255,blank=True, null=True)
    website_code = models.CharField(max_length=255,blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    country_code = models.CharField(max_length=255,blank=True, null=True)
    image_big = models.CharField(max_length=255, blank=True, null=True)
    image_icon = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_channel_sites'

class EngageboostChannelSku(models.Model):
    product_id = models.IntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    bms_sku = models.CharField(max_length=250, blank=True, null=True)
    channel_sku = models.CharField(max_length=250, blank=True, null=True)
    channel_product_id = models.CharField(max_length=255,blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_channel_sku'

class EngageboostChannelUsers(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    Fullfilment_CHOICES = (
        ('standard', 'standard'),
        ('self_ship', 'self_ship')
    )
    channel_id = models.IntegerField()
    parent_id = models.IntegerField()
    company_website_id = models.IntegerField()
    company_id = models.IntegerField()
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    token = models.TextField()
    token_expired = models.DateTimeField()
    tokentype = models.CharField(max_length=255, blank=True, null=True)
    refreshtoken = models.CharField(max_length=255, blank=True, null=True)
    isvalidtoken = models.CharField(max_length=2,choices=enum_choices, null=True)
    channel_site_ids = models.TextField()
    default_ebay_category = models.IntegerField()
    created = models.DateField()
    modified = models.DateField()
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    address = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    zip = models.CharField(max_length=250, blank=True, null=True)
    fullfilment_by = models.CharField(max_length=20,choices=Fullfilment_CHOICES,default='standard')
    paytm_merchant_id = models.CharField(max_length=255, blank=True, null=True)
    paytm_code = models.CharField(max_length=255, blank=True, null=True)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    secret_code = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_channel_users'

class EngageboostOrdermaster(models.Model):
    channel_shipping = (
        ('yes', 'yes'),
        ('no', 'no')
    )
    received = (
        ('Payment Ok', 'Payment Ok'),
        ('Excess Of', 'Excess Of'),
        ('Deficit Of', 'Deficit Of'),
        ('Hold', 'Hold'),
    )
    return_status = (
        ('Pending', 'Pending'),
        ('Authorized', 'Authorized'),
        ('Processing', 'Processing'),
        ('Declined', 'Declined')
    )
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id  = models.IntegerField(blank=True, null=True)
    company_id  = models.BigIntegerField(blank=True, null=True)
    custom_order_id = models.CharField(max_length=255, blank=True, null=True)
    channel_order_id= models.CharField(max_length=255, blank=True, null=True)
    channel_orderlineitem_id= models.TextField(blank=True, null=True)
    customer= models.ForeignKey(EngageboostCustomers,on_delete=models.CASCADE, blank=True, null=True)
    webshop = models.ForeignKey(EngageboostChannels,on_delete=models.CASCADE, blank=True, null=True)
    payment_method_id   = models.IntegerField(blank=True, null=True)
    payment_type_id = models.IntegerField(blank=True, null=True)
    payment_method_name = models.CharField(max_length=255, blank=True, null=True)
    shipping_method_id  = models.CharField(max_length=50, blank=True, null=True)
    billing_name= models.CharField(max_length=255, blank=True, null=True)
    billing_company = models.CharField(max_length=255, blank=True, null=True)
    billing_email_address   = models.CharField(max_length=255, blank=True, null=True)
    billing_street_address  = models.CharField(max_length=255, blank=True, null=True)
    billing_street_address1 = models.CharField(max_length=255, blank=True, null=True)
    billing_landmark = models.CharField(max_length=256, blank=True, null=True)
    billing_city= models.CharField(max_length=255, blank=True, null=True)
    billing_postcode= models.CharField(max_length=255, blank=True, null=True)
    billing_state   = models.IntegerField(blank=True, null=True)
    billing_state_name  = models.CharField(max_length=100, blank=True, null=True)
    billing_country = models.IntegerField(blank=True, null=True)
    billing_country_name= models.CharField(max_length=100, blank=True, null=True)
    billing_phone   = models.CharField(max_length=255, blank=True, null=True)
    billing_fax = models.CharField(max_length=255, blank=True, null=True)
    delivery_name   = models.CharField(max_length=255, blank=True, null=True)
    address_book_id = models.IntegerField(blank=True, null=True)
    delivery_company= models.CharField(max_length=255, blank=True, null=True)
    delivery_email_address  = models.CharField(max_length=255, blank=True, null=True)
    delivery_street_address = models.CharField(max_length=255, blank=True, null=True)
    delivery_street_address1= models.CharField(max_length=255, blank=True, null=True)
    delivery_landmark = models.CharField(max_length=256, blank=True, null=True)
    delivery_city   = models.CharField(max_length=255, blank=True, null=True)
    delivery_postcode   = models.CharField(max_length=255, blank=True, null=True)
    delivery_state  = models.IntegerField(blank=True, null=True)
    delivery_state_name = models.CharField(max_length=100, blank=True, null=True)
    delivery_sap_ecustomer_state_no = models.CharField(max_length=255, blank=True, null=True)
    delivery_country= models.IntegerField(blank=True, null=True)
    delivery_country_name   = models.CharField(max_length=100, blank=True, null=True)
    delivery_phone  = models.CharField(max_length=255, blank=True, null=True)
    delivery_fax= models.CharField(max_length=255, blank=True, null=True)
    custom_msg  = models.TextField(blank=True, null=True)
    applied_coupon  = models.CharField(max_length=15, blank=True, null=True)
    gross_amount= models.FloatField(blank=True, null=True)
    net_amount  = models.FloatField(blank=True, null=True)
    shipping_cost   = models.FloatField(blank=True, null=True)
    shipping_cost_excl_tax  = models.FloatField(blank=True, null=True)
    paid_amount = models.FloatField(blank=True, null=True)
    gross_discount_amount   = models.FloatField(blank=True, null=True)
    tax_amount  = models.FloatField(blank=True, null=True)
    excise_duty = models.FloatField(blank=True, null=True)
    security_amount = models.FloatField(blank=True, null=True)
    gross_amount_base   = models.FloatField(blank=True, null=True)
    net_amount_base = models.FloatField(blank=True, null=True)
    shipping_cost_base  = models.FloatField(blank=True, null=True)
    paid_amount_base= models.FloatField(blank=True, null=True)
    gross_discount_amount_base  = models.FloatField(blank=True, null=True)
    order_status= models.IntegerField(blank=True, null=True)
    buy_status  = models.IntegerField(blank=True, null=True)
    currency_code   = models.CharField(max_length=50, blank=True, null=True)
    ip_address  = models.CharField(max_length=15,blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified= models.DateTimeField(blank=True, null=True)
    is_mail = models.IntegerField(blank=True, null=True)
    tracking_company_name   = models.CharField(max_length=255, blank=True, null=True)
    tracking_no = models.CharField(max_length=255, blank=True, null=True)
    tracking_url= models.CharField(max_length=255, blank=True, null=True)
    campaign_id = models.IntegerField(blank=True, null=True)
    cart_discount   = models.FloatField(blank=True, null=True)
    tracking_mail_send  = models.IntegerField(blank=True, null=True)
    response_msg= models.TextField(blank=True, null=True)
    channel_shipping_status = models.CharField(max_length=255,choices=channel_shipping,default='No')
    fulfillment_id  = models.IntegerField(blank=True, null=True)
    cod_charge  = models.FloatField(blank=True, null=True)
    send_notes  = models.TextField(blank=True, null=True)
    received_amount = models.FloatField(blank=True, null=True)
    received_status = models.CharField(max_length=255,choices=received,default='Payment Ok')
    pay_wallet_amount    = models.FloatField(blank=True, null=True, default=0)
    refund_wallet_amount = models.FloatField(blank=True, null=True, default=0)
    assign_to   = models.IntegerField(blank=True, null=True)
    assign_wh   = models.IntegerField(blank=True, null=True)
    tags= models.CharField(max_length=256, blank=True, null=True)
    pay_txntranid   = models.CharField(max_length=256, blank=True, null=True)
    pay_txndate   	= models.DateTimeField(blank=True, null=True)
    assigned_show_room  = models.IntegerField(blank=True, null=True)
    return_note = models.TextField(blank=True, null=True)
    delivery_date   = models.DateField(blank=True, null=True)
    expected_delivery_date  = models.DateField(blank=True, null=True)
    dispatch_date   = models.DateField(blank=True, null=True)
    shipment_id = models.IntegerField(blank=True, null=True, default=0)
    zone_id = models.IntegerField(blank=True, null=True)
    time_slot_date  = models.DateField(blank=True, null=True)
    time_slot_id= models.CharField(max_length=256, blank=True, null=True)
    slot_start_time = models.CharField(max_length=20, blank=True, null=True)
    slot_end_time   = models.CharField(max_length=20, blank=True, null=True)
    return_status   = models.CharField(max_length=255,choices=return_status, null=True)
    sort_by_distance= models.IntegerField(blank=True, null=True)
    signature_image = models.TextField(blank=True, null=True)
    flag_order  = models.IntegerField(blank=True, null=True)
    area_id = models.IntegerField(blank=True, null=True)
    trent_picklist_id   = models.IntegerField(blank=True, null=True, default=0)
    refferal_code   = models.CharField(max_length=255, blank=True, null=True)
    tally_sales_entered = models.CharField(max_length=50, blank=True, null=True)
    order_amount= models.FloatField(blank=True, null=True)
    order_net_amount= models.FloatField(blank=True, null=True)
    createdby   = models.IntegerField(blank=True, null=True)
    updatedby   = models.IntegerField(blank=True, null=True)
    isblocked   = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted   = models.CharField(max_length=2,choices=enum_choices,default='n')
    pos_device_id 	= models.CharField(max_length=100, blank=True, null=True)
    grn_created_date= models.DateTimeField(blank=True, null=True)
    picker_name = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_ordermaster'

class EngageboostOrderProducts(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    approval_choices = (
        ('pending', 'pending'),
        ('approve', 'approve'),
        ('declined', 'declined')
    )

    order 		= models.ForeignKey(EngageboostOrdermaster,on_delete=models.CASCADE,related_name='order_products',blank=True, null=True)
    product 	= models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE,blank=True, null=True)
    warehouse_id= models.IntegerField(blank=True, null=True)
    quantity= models.IntegerField(default='0', blank=True, null=True)
    deleted_quantity= models.IntegerField(default='0', blank=True, null=True)
    cost_price   	= models.FloatField(default='0', blank=True, null=True)
    mrp   			= models.FloatField(default='0', blank=True, null=True)
    product_price   = models.FloatField(default='0', blank=True, null=True)
    product_discount_price  = models.FloatField(default='0', blank=True, null=True)
    product_discount_name   = models.CharField(max_length=256, blank=True, null=True)
    product_disc_type   = models.SmallIntegerField(blank=True, null=True)
    product_discount_rate   = models.FloatField(default='0', blank=True, null=True)
    product_excise_duty = models.FloatField(default='0', blank=True, null=True)
    excise_duty_per = models.CharField(max_length=256, blank=True, null=True)
    product_tax_price   = models.FloatField(default='0', blank=True, null=True)
    tax_percentage  = models.FloatField(default='0', blank=True, null=True)
    tax_name= models.CharField(max_length=256, blank=True, null=True)
    status  = models.IntegerField(default='0', blank=True, null=True)
    product_price_base  = models.FloatField(default='0', blank=True, null=True)
    product_discount_price_base = models.FloatField(default='0', blank=True, null=True)
    shipping_price  = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default='0')
    shipping_price_base = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default='0')
    shipping_tax= models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default='0')
    shipping_tax_base   = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default='0')
    giftwrap_price  = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default='0')
    giftwrap_price_base = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default='0')
    giftwrap_tax= models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default='0')
    giftwrap_tax_base   = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default='0')
    shipping_discount   = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default='0')
    shipping_discount_base  = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default='0')
    assign_to   = models.IntegerField(blank=True, null=True)
    assign_wh   = models.IntegerField(default='0', blank=True, null=True)
    tags= models.CharField(max_length=100, blank=True, null=True)
    shortage= models.IntegerField(default='0', blank=True, null=True)
    returns = models.IntegerField(default='0', blank=True, null=True)
    grn_quantity= models.IntegerField(default='0', blank=True, null=True)
    trents_picklist_id  = models.IntegerField(default='0', blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    sgst= models.FloatField(default='0', blank=True, null=True)
    cgst= models.FloatField(default='0', blank=True, null=True)
    igst= models.FloatField(default='0', blank=True, null=True)
    cess= models.FloatField(default='0', blank=True, null=True)
    sgst_percentage = models.FloatField(default='0', blank=True, null=True)
    cgst_percentage = models.FloatField(default='0', blank=True, null=True)
    igst_percentage = models.FloatField(default='0', blank=True, null=True)
    cess_percentage = models.FloatField(default='0', blank=True, null=True)
    hsn_id  = models.CharField(max_length=150,blank=True, null=True)
    shipping_igst   = models.FloatField(default='0', blank=True, null=True)
    shipping_sgst   = models.FloatField(default='0', blank=True, null=True)
    shipping_cgst   = models.FloatField(default='0', blank=True, null=True)
    shipping_cgst_percentage= models.FloatField(default='0', blank=True, null=True)
    shipping_sgst_percentage= models.FloatField(default='0', blank=True, null=True)
    shipping_igst_percentage= models.FloatField(default='0', blank=True, null=True)
    substitute_product_id   = models.IntegerField(default=0, blank=True, null=True)
    weight                  = models.FloatField(default='0', blank=True, null=True)
    is_substitute           		= models.CharField(max_length=2,choices=enum_choices,default='n')
    substitute_notes 				= models.TextField(blank=True, null=True)
    pick_as_substitute 				= models.CharField(max_length=2,choices=enum_choices,default='n')
    send_approval = models.CharField(max_length=10,choices=approval_choices,blank=True, null=True)
    custom_field_name = models.CharField(max_length=255, blank=True, null=True)
    custom_field_value = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_order_products'

class EngageboostOrderSubstituteProducts(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    approval_choices = (
        ('pending', 'pending'),
        ('approve', 'approve'),
        ('declined', 'declined')
    )
    order                   = models.ForeignKey(EngageboostOrdermaster,on_delete=models.CASCADE,related_name='order_substitute_products',blank=True, null=True)
    product                 = models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE,blank=True, null=True)
    warehouse_id            = models.IntegerField(blank=True, null=True)
    quantity                = models.IntegerField(default='0', blank=True, null=True)
    deleted_quantity        = models.IntegerField(default='0', blank=True, null=True)
    shortage                = models.IntegerField(default='0', blank=True, null=True)
    returns                 = models.IntegerField(default='0', blank=True, null=True)
    grn_quantity            = models.IntegerField(default='0', blank=True, null=True)
    product_price           = models.FloatField(default='0', blank=True, null=True)
    product_discount_price  = models.FloatField(default='0', blank=True, null=True)
    product_discount_name   = models.CharField(max_length=256, blank=True, null=True)
    product_disc_type       = models.SmallIntegerField(blank=True, null=True)
    product_discount_rate   = models.FloatField(default='0', blank=True, null=True)
    product_excise_duty     = models.FloatField(default='0', blank=True, null=True)
    product_tax_price       = models.FloatField(default='0', blank=True, null=True)
    tax_percentage          = models.FloatField(default='0', blank=True, null=True)
    shipping_price          = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default='0')
    shipping_tax            = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default='0')
    created                 = models.DateTimeField(blank=True, null=True)
    modified                = models.DateTimeField(blank=True, null=True)
    substitute_product_id   = models.IntegerField(default=0, blank=True, null=True)
    weight                  = models.FloatField(default='0', blank=True, null=True)
    is_substitute           = models.CharField(max_length=2,choices=enum_choices,default='n')
    substitute_notes        = models.TextField(blank=True, null=True)
    pick_as_substitute      = models.CharField(max_length=2,choices=enum_choices,default='n')
    send_approval           = models.CharField(max_length=10,choices=approval_choices,blank=True, null=True)
    send_approval_interval  = models.CharField(max_length=10, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_order_substitute_products'

class EngageboostScannedOrderProducts(models.Model):
    is_deleted_status = (
        ('y', 'y'),
        ('n', 'n')
    )
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    order_product 					= models.ForeignKey(EngageboostOrderProducts,on_delete=models.CASCADE,related_name='scanned_order_products',blank=True, null=True)
    order 							= models.ForeignKey(EngageboostOrdermaster,on_delete=models.CASCADE,related_name='scanned_order',blank=True, null=True)
    product 						= models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE,related_name='scanned_products',blank=True, null=True)
    barcode 						= models.CharField(max_length=255, blank=True, null=True)
    quantity                        = models.IntegerField(default='0', blank=True, null=True)
    product_old_price               = models.FloatField(default='0', blank=True, null=True)
    product_new_price               = models.FloatField(default='0', blank=True, null=True)
    weight                          = models.FloatField(default='0', blank=True, null=True)
    product_discount_price          = models.FloatField(default='0', blank=True, null=True)
    product_tax_price               = models.FloatField(default='0', blank=True, null=True)
    created                         = models.DateTimeField(blank=True, null=True)
    modified                        = models.DateTimeField(blank=True, null=True)
    is_deleted 						= models.CharField(max_length=2,choices=is_deleted_status,default='n')
    is_blocked 						= models.CharField(max_length=2,choices=is_deleted_status,default='n')
    pick_as_substitute 				= models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_scanned_order_products'


class EngageboostTempOrdermaster(models.Model):
    channel_shipping_status_choice=(
        ('y', 'y'),
        ('n', 'n')
    )
    status_choice=(
        ('success', 'success'),
        ('error', 'error')
    )
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    channel_order_id = models.CharField(max_length=255, blank=True, null=True)
    order_item_id = models.CharField(max_length=21, blank=True, null=True)
    channel_orderlineitem_id = models.TextField(blank=True, null=True)
    customer = models.ForeignKey(EngageboostCustomers,on_delete=models.CASCADE, blank=True, null=True)
    webshop = models.ForeignKey(EngageboostChannels,on_delete=models.CASCADE, blank=True, null=True)
    payment_method_id = models.IntegerField(blank=True, null=True)
    payment_type_id = models.IntegerField(blank=True, null=True)
    payment_method_name = models.CharField(max_length=255, blank=True, null=True)
    shipping_method_id = models.CharField(max_length=50, blank=True, null=True)
    billing_name = models.CharField(max_length=255, blank=True, null=True)
    billing_company = models.CharField(max_length=255, blank=True, null=True)
    billing_email_address = models.CharField(max_length=255, blank=True, null=True)
    billing_street_address = models.CharField(max_length=255, blank=True, null=True)
    billing_street_address1 = models.CharField(max_length=255, blank=True, null=True)
    billing_city = models.CharField(max_length=255, blank=True, null=True)
    billing_postcode = models.CharField(max_length=255, blank=True, null=True)
    billing_state = models.CharField(max_length=255, blank=True, null=True)
    billing_country = models.IntegerField(blank=True, null=True)
    billing_country_name = models.CharField(max_length=100, blank=True, null=True)
    billing_phone = models.CharField(max_length=255, blank=True, null=True)
    billing_fax = models.CharField(max_length=255, blank=True, null=True)
    delivery_name = models.CharField(max_length=255, blank=True, null=True)
    address_book_id = models.IntegerField(blank=True, null=True)
    delivery_company = models.CharField(max_length=255, blank=True, null=True)
    delivery_email_address = models.CharField(max_length=255, blank=True, null=True)
    delivery_street_address = models.CharField(max_length=255, blank=True, null=True)
    delivery_street_address1 = models.CharField(max_length=255, blank=True, null=True)
    delivery_city = models.CharField(max_length=255, blank=True, null=True)
    delivery_postcode = models.CharField(max_length=255, blank=True, null=True)
    delivery_state = models.CharField(max_length=255, blank=True, null=True)
    delivery_sap_ecustomer_state_no = models.CharField(max_length=255, blank=True, null=True)
    delivery_country = models.IntegerField(blank=True, null=True)
    delivery_country_name = models.CharField(max_length=100, blank=True, null=True)
    delivery_phone = models.CharField(max_length=255, blank=True, null=True)
    delivery_fax = models.CharField(max_length=255, blank=True, null=True)
    custom_msg = models.TextField(blank=True, null=True)
    applied_coupon = models.CharField(max_length=15, blank=True, null=True)
    gross_amount = models.FloatField(blank=True, null=True)
    net_amount = models.FloatField(blank=True, null=True)
    shipping_cost = models.FloatField(blank=True, null=True)
    shipping_cost_excl_tax = models.FloatField(blank=True, null=True)
    paid_amount = models.FloatField(blank=True, null=True)
    gross_discount_amount = models.FloatField(blank=True, null=True)
    tax_amount = models.FloatField(blank=True, null=True)
    excise_duty = models.FloatField(blank=True, null=True)
    security_amount = models.FloatField(blank=True, null=True)
    gross_amount_base = models.FloatField(blank=True, null=True)
    net_amount_base = models.FloatField(blank=True, null=True)
    shipping_cost_base = models.FloatField(blank=True, null=True)
    paid_amount_base = models.FloatField(blank=True, null=True)
    gross_discount_amount_base = models.FloatField(blank=True, null=True)
    currency_code = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    created_time = models.TimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    tracking_company_name = models.CharField(max_length=255, blank=True, null=True)
    tracking_no = models.CharField(max_length=255, blank=True, null=True)
    tracking_url = models.CharField(max_length=255, blank=True, null=True)
    cart_discount = models.FloatField(blank=True, null=True)
    channel_shipping_status=models.CharField(max_length=2,choices=channel_shipping_status_choice, default='n')
    cod_charge = models.FloatField(blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    expected_delivery_date = models.DateTimeField(blank=True, null=True)
    dispatch_date = models.DateTimeField(blank=True, null=True)
    status=models.CharField(max_length=2,choices=status_choice, default='success')
    file_name = models.TextField(blank=True, null=True)
    err_flag = models.IntegerField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    buyer_date = models.DateTimeField(blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    item_name = models.CharField(max_length=500, blank=True, null=True)
    item_price = models.FloatField(blank=True, null=True)
    shipping_tax = models.FloatField(blank=True, null=True)
    shipment_type = models.CharField(max_length=100, blank=True, null=True)
    delivery_street_address3 = models.CharField(max_length=255, blank=True, null=True)
    delivery_time_zone = models.CharField(max_length=255, blank=True, null=True)
    delivery_end_date = models.DateTimeField(blank=True, null=True)
    item_promotion_id = models.CharField(max_length=100, blank=True, null=True)
    ship_promotion_discount = models.CharField(max_length=255, blank=True, null=True)
    ship_promotion_id = models.CharField(max_length=100, blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_temp_ordermaster'

class EngageboostShipments(models.Model):
    shipment_status_choice=(
        ('Created', 'Created'),
        ('Packed', 'Packed'),
        ('Picking', 'Picking'),
        ('Invoicing', 'Invoicing'),
        ('Create Shipment', 'Create Shipment'),
        ('Shipment Processing', 'Shipment Processing'),
        ('Ready to Ship', 'Ready to Ship'),
        ('Ready to Dispatch', 'Ready to Dispatch'),
        ('Dispatched', 'Dispatched'),
        ('Shipped', 'Shipped'),
        ('Completed', 'Completed')
    )
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    custom_shipment_id = models.CharField(max_length=100,blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    zone_id = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    picklist_id = models.IntegerField(blank=True, null=True)
    shipping_method_id = models.SmallIntegerField(blank=True, null=True)
    no_of_vehicles = models.IntegerField(blank=True, null=True)
    shipment_status=models.CharField(max_length=100,choices=shipment_status_choice, default='Created',blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_shipments'

class EngageboostShipmentOrders(models.Model):
    shipment_status_choice=(
        ('Created', 'Created'),
        ('Packed', 'Packed'),
        ('Picking', 'Picking'),
        ('Invoicing', 'Invoicing'),
        ('Create Shipment', 'Create Shipment'),
        ('Shipment Processing', 'Shipment Processing'),
        ('Ready to Ship', 'Ready to Ship'),
        ('Ready to Dispatch', 'Ready to Dispatch'),
        ('Dispatched', 'Dispatched'),
        ('Shipped', 'Shipped'),
        ('Completed', 'Completed')
    )
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    # shipment = models.ForeignKey(EngageboostShipments,on_delete=models.CASCADE, blank=True, null=True)
    shipment = models.IntegerField(blank=True, null=True)
    order = models.ForeignKey(EngageboostOrdermaster,on_delete=models.CASCADE,blank=True, null=True, related_name="shipment_order")
    trent_picklist_id = models.IntegerField(blank=True, null=True)
    custom_order_id = models.CharField(max_length=255,blank=True, null=True)
    webshop_id = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    shipping_method_id = models.SmallIntegerField(blank=True, null=True)
    tracking_no = models.CharField(max_length=100, blank=True, null=True)
    tracking_company_name = models.CharField(max_length=100, blank=True, null=True)
    routing_code = models.CharField(max_length=50, blank=True, null=True)
    ccrcrdref = models.CharField(max_length=50, blank=True, null=True)
    destinationarea = models.CharField(max_length=10, blank=True, null=True)
    destinationlocation = models.CharField(max_length=10, blank=True, null=True)
    actualweight = models.CharField(max_length=100, blank=True, null=True)
    total_quantity = models.IntegerField(blank=True, null=True)
    dimension = models.CharField(max_length=100,blank=True, null=True)
    schedule_pickup_date = models.DateField(blank=True, null=True)
    schedule_pickup_time = models.TimeField(blank=True, null=True)
    label_pdf_name = models.CharField(max_length=256, blank=True, null=True)
    zone_id = models.IntegerField(blank=True, null=True)
    time_slot_id = models.CharField(max_length=256, blank=True, null=True)
    no_of_crates = models.SmallIntegerField(blank=True, null=True)
    return_delivery_date  = models.DateField(blank=True, null=True)
    return_driver_id= models.IntegerField(blank=True, null=True)
    shipment_status=models.CharField(max_length=100,choices=shipment_status_choice, default='Created',blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_shipment_orders'

class EngageboostShipmentOrderProducts(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    shipment_order = models.ForeignKey(EngageboostShipmentOrders,on_delete=models.CASCADE,related_name='shipment_order_products',blank=True, null=True)
    # shipment = models.ForeignKey(EngageboostShipments,on_delete=models.CASCADE, blank=True, null=True)
    shipment = models.IntegerField(blank=True, null=True)
    order = models.ForeignKey(EngageboostOrdermaster,on_delete=models.CASCADE,blank=True, null=True)
    product = models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE,blank=True, null=True)
    trent_picklist_id = models.IntegerField(blank=True, null=True)
    order_product = models.ForeignKey(EngageboostOrderProducts,on_delete=models.CASCADE,blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    shortage = models.IntegerField(blank=True, null=True, default='0')
    returns = models.IntegerField(blank=True, null=True, default='0')
    grn_quantity = models.IntegerField(blank=True, null=True, default='0')
    grn_return = models.IntegerField(blank=True, null=True)
    shipment_status=models.CharField(max_length=100, default='Created',blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    pick_as_substitute 				= models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_shipment_order_products'

class EngageboostWishlists(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    user_id = models.BigIntegerField()
    website_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    product = models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE,blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_wishlists'

class EngageboostWebsiteActivities(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    customers_id = models.IntegerField(blank=True, null=True)
    notify_msg = models.CharField(max_length=255,blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    is_read = models.SmallIntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_website_activities'

class EngageboostWebsiteChannelFieldValues(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    engageboost_channel_id = models.IntegerField(blank=True, null=True)
    engageboost_channel_field_id = models.IntegerField(blank=True, null=True)
    engageboost_company_website_id = models.CharField(max_length=255,blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_website_channel_field_values'

class EngageboostWebsiteChannels(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    engageboost_channel_id = models.IntegerField(blank=True, null=True)
    engageboost_company_website_id = models.IntegerField(blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    currency_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_website_channels'

class EngageboostAttemptedDeliveryDetails(models.Model):
    shipment = models.ForeignKey(EngageboostShipments,on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(EngageboostOrdermaster,on_delete=models.CASCADE,blank=True, null=True)
    delivery_attempted_date = models.DateTimeField(blank=True, null=True)
    reason = models.CharField(max_length=255,blank=True, null=True)
    additional_note = models.TextField(blank=True, null=True)
    new_delivery_date = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    attempted_type = models.CharField(max_length=20,blank=True, null=True)
    class Meta:
        db_table = 'engageboost_attempted_delivery_details'

class EngageboostFlipkartOrderProcess(models.Model):
    order = models.ForeignKey(EngageboostOrdermaster,on_delete=models.CASCADE,blank=True, null=True)
    order_item_id = models.CharField(max_length=100, blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    request_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    api_for = models.CharField(max_length=100, blank=True, null=True)
    reponse_type = models.CharField(max_length=100, blank=True, null=True)
    error_code = models.CharField(max_length=100, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    custom_error_message = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_flipkart_order_process'

class EngageboostCategoryMasters(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    status_choices = (
        ('Y', 'Y'),
        ('N', 'N')
    )
    parent_id = models.IntegerField(blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    thumb_image = models.CharField(max_length=255, blank=True, null=True)
    banner_image = models.CharField(max_length=255, blank=True, null=True)
    page_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    category_url = models.CharField(max_length=255, blank=True, null=True)
    slug = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50,blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n', blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n', blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    is_ebay_store_category = models.CharField(max_length=2,choices=status_choices,default='N', null=True)
    customer_group_id = models.IntegerField(blank=True, null=True)
    display_mobile_app = models.CharField(max_length=2,choices=status_choices,default='N', blank=True, null=True)
    applicable_imei = models.CharField(max_length=2,choices=status_choices,default='N',blank=True, null=True)
    isadded_in_tally = models.CharField(max_length=2,choices=status_choices,default='N', blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    show_navigation = models.CharField(max_length=2,choices=status_choices,default='N', blank=True, null=True)
    class Meta:
        db_table = 'engageboost_category_masters'

class EngageboostCategoryBanners(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    Banner_Type_CHOICES = (
        ('C', 'C'),
        ('H', 'H')
    )
    website_id = models.IntegerField(blank=True, null=True)
    # warehouse = models.ForeignKey(EngageboostWarehouseMasters,on_delete=models.CASCADE,blank=True, null=True)
    warehouse_id = models.CharField(max_length=500, blank=True, null=True)
    banner_name = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices, default='n', null=True)
    category_id = models.IntegerField(blank=True, null=True)
    order_no = models.IntegerField(blank=True, null=True)
    banner_type = models.CharField(max_length=2,choices=Banner_Type_CHOICES,default='C')
    parent_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_category_banners'

class EngageboostCategoryBannersImages(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    Link_CHOICES = (
        ('external link', 'external link'),
        ('promotion', 'promotion'),
        ('category', 'category'),
        ('product', 'product')
    )
    Applicable_For_CHOICES = (
        ('mobile', 'mobile'),
        ('web', 'web'),
        ('category', 'category')
    )
    Enable_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    category_banner = models.ForeignKey(EngageboostCategoryBanners,on_delete=models.CASCADE,related_name='category_banners_images',blank=True, null=True)
    primary_image_name = models.CharField(max_length=255, blank=True, null=True)
    applicable_for = models.CharField(max_length=20,choices=Applicable_For_CHOICES,default='category')
    banner_link_to = models.CharField(max_length=20,choices=Link_CHOICES,default='category')
    link = models.CharField(max_length=500, blank=True, null=True)
    promotion_id = models.IntegerField(blank=True, null=True)
    product_id = models.CharField(max_length=500, blank=True, null=True)
    category_id = models.CharField(max_length=500, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    order_no = models.IntegerField(blank=True, null=True)
    banner_caption1 = models.TextField(blank=True, null=True)
    banner_caption2 = models.TextField(blank=True, null=True)
    is_notification_enabled_val = models.CharField(max_length=10,choices=Enable_CHOICES,default='No')
    notification_msg = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices, default='n', null=True)
    class Meta:
        db_table = 'engageboost_category_banners_images'



class EngageboostBrandMasters(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    brand_logo = models.CharField(max_length=255, blank=True, null=True)
    brand_url = models.CharField(max_length=255, blank=True, null=True)
    slug = models.TextField(blank=True, null=True)
    isblocked = models.CharField(max_length=255,default='n')
    isdeleted = models.CharField(max_length=255,default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_brand_masters'

class EngageboostProductCategories(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    product = models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE,blank=True, null=True, related_name='product_list')
    category = models.ForeignKey(EngageboostCategoryMasters,on_delete=models.CASCADE,blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    is_parent = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    createdby = models.IntegerField(default='0',blank=True, null=True)
    updatedby = models.IntegerField(default='0',blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_categories'

class EngageboostProductImeis(models.Model):
    order = models.ForeignKey(EngageboostOrdermaster,on_delete=models.CASCADE,blank=True, null=True)
    product = models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE,blank=True, null=True)
    packagereferencecode = models.CharField(max_length=250, blank=True, null=True)
    subordercode = models.CharField(max_length=250, blank=True, null=True)
    imei = models.CharField(max_length=50, blank=True, null=True)
    isdeleted = models.SmallIntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_imeis'

class EngageboostProductItemSpecification(models.Model):
    product_mktplace_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    item_specification = models.CharField(max_length=255,blank=True, null=True)
    fieldtype = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_item_specification'

class EngageboostProductItemSpecificationValue(models.Model):
    product_item_specification_id = models.IntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    value = models.CharField(max_length=255,blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_item_specification_value'

class EngageboostProductKeyTypes(models.Model):
    name = models.CharField(max_length=80,blank=True, null=True)
    short_name = models.CharField(max_length=20,blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_key_types'

class EngageboostProductMarketplaces(models.Model):
    ebay = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('success', 'success'),
        ('error', 'error'),
        ('completed', 'completed'),
        ('expiried', 'expiried')
    )
    amazon = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('success', 'success'),
        ('error', 'error'),
        ('processing', 'processing')
    )
    snapdeal = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('success', 'success'),
        ('error', 'error'),
        ('processing', 'processing')
    )
    twitter = (
        ('active', 'active'),
        ('inactive', 'inactive')
    )
    code = (
        ('EAN', 'EAN'),
        ('ASIN', 'ASIN'),
        ('GCID', 'GCID'),
        ('ISBN', 'ISBN'),
        ('SUPC', 'SUPC')
    )
    hitcounter = (
        ('BasicStyle', 'BasicStyle'),
        ('NoHitCounter', 'NoHitCounter'),
        ('RetroStyle', 'RetroStyle')
    )
    boldtitle = (
        ('yes', 'yes'),
        ('no', 'no')
    )
    border = (
        ('yes', 'yes'),
        ('no', 'no')
    )
    featured = (
        ('yes', 'yes'),
        ('no', 'no')
    )
    heighlight = (
        ('yes', 'yes'),
        ('no', 'no')
    )
    homepagefeatured = (
        ('yes', 'yes'),
        ('no', 'no')
    )
    is_ebay_auto_relist = (
        ('Y', 'N'),
        ('Y', 'N')
    )
    homepagefeatured = (
        ('yes', 'yes'),
        ('no', 'no')
    )

    is_deleted_status = (
        ('Y', 'Y'),
        ('N', 'N')
    )
    product_id = models.IntegerField(blank=True, null=True)
    ebay_item_id = models.CharField(max_length=255, blank=True, null=True)
    ebay_addstatus = models.CharField(max_length=2,choices=ebay,default='inactive')
    amazon_itemid = models.CharField(max_length=255, blank=True, null=True)
    amazon_addstatus = models.CharField(max_length=2,choices=amazon,default='inactive')
    snapdeal_addstatus = models.CharField(max_length=2,choices=snapdeal,default='inactive')
    twitter_addstatus = models.CharField(max_length=2,choices=twitter,default='inactive')
    ebay_listing_starttime = models.CharField(max_length=255, blank=True, null=True)
    ebay_listing_endtime = models.CharField(max_length=255, blank=True, null=True)
    ebay_listing_build = models.CharField(max_length=255, blank=True, null=True)
    ebay_listing_version = models.CharField(max_length=255, blank=True, null=True)
    ebay_listing_time = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    product_manufacturer = models.CharField(max_length=255)
    product_brand = models.CharField(max_length=255, blank=True, null=True)
    ean = models.CharField(max_length=255, blank=True, null=True)
    code_type = models.CharField(max_length=2,choices=code,default='EAN')
    video = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    system_requirements = models.TextField(blank=True, null=True)
    templates = models.TextField(blank=True, null=True)
    template_id = models.IntegerField(blank=True, null=True)
    pro_condotion = models.CharField(max_length=255, blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)
    category_name = models.CharField(max_length=255, blank=True, null=True)
    category_mapping = models.IntegerField(blank=True, null=True)
    listing_duration = models.CharField(max_length=255, blank=True, null=True)
    dispatch_time_max = models.CharField(max_length=255, blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    subtitle = models.TextField(blank=True, null=True)
    secondarycategoryname = models.CharField(max_length=255, blank=True, null=True)
    secondarycategoryid = models.IntegerField(blank=True, null=True)
    listingtype = models.CharField(max_length=255, blank=True, null=True)
    returnpolicy = models.CharField(max_length=255, blank=True, null=True)
    returnwithin = models.CharField(max_length=255, blank=True, null=True)
    return_shipping_paidby = models.CharField(max_length=255, blank=True, null=True)
    refund_desc = models.TextField(blank=True, null=True)
    channel_site_id = models.IntegerField(blank=True, null=True)
    hitcounter = models.CharField(max_length=2,choices=hitcounter,default='NoHitCounter',blank=True, null=True)
    boldtitle = models.CharField(max_length=2,choices=boldtitle,default='no',blank=True, null=True)
    border = models.CharField(max_length=2,choices=border,default='no',blank=True, null=True)
    featured = models.CharField(max_length=2,choices=featured,default='no',blank=True, null=True)
    heighlight = models.CharField(max_length=2,choices=heighlight,default='no',blank=True, null=True)
    homepagefeatured = models.CharField(max_length=2,choices=homepagefeatured,default='no',blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    is_ebay_auto_relist = models.CharField(max_length=2,choices=is_ebay_auto_relist,default='N',blank=True, null=True)
    product_disclaimer = models.TextField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    is_deleted = models.CharField(max_length=2,choices=is_deleted_status,default='N')
    mapping_price = models.FloatField(blank=True, null=True)
    competitive_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amazon_search_keyword = models.CharField(max_length=255, blank=True, null=True)
    recomended_node_id = models.IntegerField(blank=True, null=True)
    recomended_node_name = models.CharField(max_length=255, blank=True, null=True)
    recomended_node_id1 = models.IntegerField(blank=True, null=True)
    recomended_node_name1 = models.CharField(max_length=250, blank=True, null=True)
    product_asin = models.CharField(max_length=255, blank=True, null=True)
    fulfillment_center_id = models.CharField(max_length=50, blank=True, null=True)
    fnsku = models.CharField(max_length=255, blank=True, null=True)
    marketplace_product_id = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_marketplaces'

class EngageboostProductMoveTrack(models.Model):
    purchase_order_received_id = models.BigIntegerField(blank=True, null=True)
    website_id = models.BigIntegerField(blank=True, null=True)
    warehouse_id_from = models.IntegerField(blank=True, null=True)
    warehouse_id_to = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    createdby = models.BigIntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_move_track'

class EngageboostProductPricing(models.Model):
    product_id = models.IntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    rrp_formula_id = models.IntegerField(blank=True, null=True)
    rrp_value = models.FloatField(blank=True, null=True)
    quantity = models.BigIntegerField(blank=True, null=True)
    spec_price_formula_id = models.FloatField(blank=True, null=True)
    spec_price = models.FloatField(blank=True, null=True)
    spec_from_date = models.DateField(blank=True, null=True)
    spec_to_date = models.DateField(blank=True, null=True)
    auction_start_price = models.FloatField(blank=True, null=True)
    auction_end_price = models.FloatField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_pricing'

class EngageboostProductPush(models.Model):
    status_field = (
        ('Y', 'Y'),
        ('N', 'N')
    )
    product_id = models.IntegerField(blank=True, null=True)
    marketplace_id = models.IntegerField(blank=True, null=True)
    action = models.CharField(max_length=255,blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=2,choices=status_field,default='N',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_push'

class EngageboostProductRatings(models.Model):
    postedon = models.DateTimeField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=15,blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_ratings'

class EngageboostProductRepriceRule(models.Model):
    product_id = models.IntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    reprice_rule_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_reprice_rule'

class EngageboostProductReviews(models.Model):
    status_field = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    product = models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE,blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(EngageboostUsers,on_delete=models.CASCADE,blank=True, null=True)
    user_ip = models.CharField(max_length=100, blank=True, null=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    user_designation = models.CharField(max_length=100, blank=True, null=True)
    user_email = models.CharField(max_length=100, blank=True, null=True)
    user_city = models.CharField(max_length=100, blank=True, null=True)
    user_state = models.CharField(max_length=100, blank=True, null=True)
    user_country = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    reply = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(default='0')
    updatedby = models.IntegerField(blank=True, null=True)
    replied = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=status_field,default='y',blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=status_field,default='n',blank=True, null=True)
    isflagged = models.CharField(max_length=2,choices=status_field,default='n',blank=True, null=True)
    ispurchased = models.CharField(max_length=2,choices=status_field,default='n',blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_reviews'

class EngageboostProductStatus(models.Model):
    name = models.CharField(max_length=200,blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_status'

class EngageboostProductStocks(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    product = models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE,blank=True, null=True, related_name='product_stock')
    warehouse = models.ForeignKey(EngageboostWarehouseMasters,on_delete=models.CASCADE,blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True,default=0)
    safety_stock = models.IntegerField(blank=True, null=True,default=0)
    avg_sales_week = models.CharField(max_length=255,blank=True, null=True)
    avg_sales_month = models.CharField(max_length=255,blank=True, null=True)
    stock_unit = models.IntegerField(blank=True, null=True)
    islot = models.IntegerField(blank=True, null=True)
    islabel = models.IntegerField(blank=True, null=True)
    virtual_stock = models.IntegerField(blank=True, null=True,default=0)
    real_stock = models.IntegerField(blank=True, null=True,default=0)
    created = models.CharField(max_length=255,blank=True, null=True)
    modified = models.CharField(max_length=255,blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    createdby = models.IntegerField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_stocks'

class EngageboostProductStockCrons(models.Model):
    warehouse_id = models.CharField(max_length=255, blank=True, null=True)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    stock = models.CharField(max_length=255, blank=True, null=True)
    created = models.CharField(max_length=255,blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_stock_crons'

class EngageboostProductTemplateMasters(models.Model):
    ebay_groupid = models.BigIntegerField(blank=True, null=True)
    ebay_proddesc_themeid = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_template_masters'

class EngageboostProductTierPrice(models.Model):
    product = models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE,blank=True, null=True)
    customer_group_id = models.IntegerField(blank=True, null=True)
    formula_id = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_tier_price'

class EngageboostProductVisibilities(models.Model):
    name = models.CharField(max_length=200,blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_visibilities'

class EngageboostProductimages(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    product = models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE,related_name='product_images',blank=True, null=True)
    img = models.CharField(max_length=255, blank=True, null=True)
    status = models.TextField(blank=True, null=True, default='0')
    is_cover = models.IntegerField(blank=True, null=True)
    img_title = models.CharField(max_length=255, blank=True, null=True)
    img_alt = models.CharField(max_length=255, blank=True, null=True)
    img_order = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(default='0')
    updatedby = models.IntegerField(default='0')
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_productimages'

class EngageboostProductworksheetimages(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    product = models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE,blank=True, null=True)
    worksheet_product = models.CharField(max_length=255, blank=True, null=True)
    worksheet_product_name = models.CharField(max_length=255, blank=True, null=True)
    worksheet_capacity = models.CharField(max_length=255, blank=True, null=True)
    worksheet_min_microwable_size = models.CharField(max_length=255, blank=True, null=True)
    worksheet_serving_size = models.CharField(max_length=255, blank=True, null=True)
    worksheet_img = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_productworksheetimages'

class EngageboostOrderStatusMasters(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_default_status = models.CharField(max_length=2,choices=enum_choices,default='y')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    color_code = models.CharField(max_length=30, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    order_status_label_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_order_status_masters'

class EngageboostReturnOrderImages(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)
    image_name = models.CharField(max_length=255,blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_return_order_images'

class EngageboostAffiliateContacts(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_affiliate_contacts'

class EngageboostChannelsCategoriesMaster(models.Model):
    status_choices = (
        ('active', 'active'),
        ('inactive', 'inactive')
    )
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    category_name = models.CharField(max_length=225)
    parent_id = models.IntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    channel_category_id = models.IntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20,choices=status_choices,default='active')
    categorylevel = models.IntegerField(blank=True, null=True)
    categoryparentid = models.IntegerField(blank=True, null=True)
    leafcategory = models.CharField(max_length=255, blank=True, null=True)
    is_variation_enabled = models.CharField(max_length=555, blank=True, null=True)
    is_custom_iemspecification_enabled = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_channels_categories_master'

class EngageboostEmiSettings(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.BigIntegerField(blank=True, null=True)
    emisettings_name = models.CharField(max_length=250,blank=True, null=True)
    finaner_name = models.CharField(max_length=250, blank=True, null=True)
    financer_logo = models.CharField(max_length=250, blank=True, null=True)
    financer_desc = models.TextField(blank=True, null=True)
    financer_message = models.CharField(max_length=250, blank=True, null=True)
    starting_amount = models.FloatField(blank=True, null=True)
    downpayment = models.FloatField(blank=True, null=True)
    number_of_emi = models.IntegerField(blank=True, null=True)
    location_ids = models.TextField(blank=True, null=True)
    product_ids = models.TextField(blank=True, null=True)
    zipcode = models.TextField(blank=True, null=True)
    isactive = models.CharField(max_length=2,choices=enum_choices,default='y')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_emi_settings'

class EngageboostOutofstockNotification(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.BigIntegerField(blank=True, null=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    user_email = models.CharField(max_length=100, blank=True, null=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_outofstock_notification'

class EngageboostProductRateperpacks(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.BigIntegerField(blank=True, null=True)
    product_id = models.BigIntegerField(blank=True, null=True)
    sku = models.CharField(max_length=50, blank=True, null=True)
    product_title = models.CharField(max_length=250, blank=True, null=True)
    pack_id = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    createdby = models.IntegerField(default='1')
    updatedby = models.IntegerField(default='1')
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_rateperpacks'

class EngageboostRateperpacks(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.BigIntegerField(blank=True, null=True)
    pack_name = models.CharField(max_length=250,blank=True, null=True)
    pack = models.CharField(max_length=250, blank=True, null=True)
    qty_per_pack = models.CharField(max_length=250, blank=True, null=True)
    pack_unit = models.CharField(max_length=10, blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    createdby = models.IntegerField(default='1')
    updatedby = models.IntegerField(default='1')
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_rateperpacks'

class EngageboostTallyLogs(models.Model):
    Type_CHOICES = (
        ('Order', 'Order'),
        ('Inventory', 'Inventory'),
        ('Po', 'Po')
    )
    cron_run_date_time = models.DateTimeField(blank=True, null=True)
    last_transaction_id = models.IntegerField(blank=True, null=True)
    file_name = models.CharField(max_length=256, blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    tally_type = models.CharField(max_length=20,choices=Type_CHOICES,default='Order')
    class Meta:
        db_table = 'engageboost_tally_logs'

class Engageboost2CheckoutReturnDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    middle_initial = models.CharField(max_length=50, blank=True, null=True)
    sid = models.CharField(max_length=50, blank=True, null=True)
    ship_zip = models.CharField(max_length=50, blank=True, null=True)
    key = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    order_number = models.CharField(max_length=50, blank=True, null=True)
    cart_id = models.CharField(max_length=50, blank=True, null=True)
    currency_code = models.CharField(max_length=50, blank=True, null=True)
    lang = models.CharField(max_length=50, blank=True, null=True)
    ship_state = models.CharField(max_length=50, blank=True, null=True)
    invoice_id = models.CharField(max_length=50, blank=True, null=True)
    total = models.CharField(max_length=50, blank=True, null=True)
    ship_street_address2 = models.CharField(max_length=50, blank=True, null=True)
    credit_card_processed = models.CharField(max_length=50, blank=True, null=True)
    zip = models.CharField(max_length=50, blank=True, null=True)
    ship_name = models.CharField(max_length=50, blank=True, null=True)
    ship_method = models.CharField(max_length=50, blank=True, null=True)
    cart_weight = models.CharField(max_length=50, blank=True, null=True)
    fixed = models.CharField(max_length=50, blank=True, null=True)
    ship_country = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    street_address = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    ship_city = models.CharField(max_length=50, blank=True, null=True)
    cart_order_id = models.CharField(max_length=50, blank=True, null=True)
    merchant_order_id = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    ip_country = models.CharField(max_length=50, blank=True, null=True)
    demo = models.CharField(max_length=50, blank=True, null=True)
    ship_street_address = models.CharField(max_length=50, blank=True, null=True)
    pay_method = models.CharField(max_length=50, blank=True, null=True)
    cart_tangible = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    street_address2 = models.CharField(max_length=50, blank=True, null=True)
    x_receipt_link_url = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    card_holder_name = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_2checkout_return_details'

class EngageboostAccountChannels(models.Model):
    enum_choices = (
        ('0', '0'),
        ('1', '1')
    )
    engageboost_channel = models.ForeignKey(EngageboostChannels,on_delete=models.CASCADE,blank=True, null=True)
    engageboost_account_type_id = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=255,blank=True, null=True)
    password = models.CharField(max_length=255,blank=True, null=True)
    tokenid = models.TextField(blank=True, null=True)
    certificateid = models.CharField(max_length=255,blank=True, null=True)
    devkey = models.CharField(max_length=255,blank=True, null=True)
    company_name = models.CharField(max_length=255,blank=True, null=True)
    address1 = models.CharField(max_length=255,blank=True, null=True)
    address2 = models.CharField(max_length=255,blank=True, null=True)
    city = models.CharField(max_length=255,blank=True, null=True)
    state = models.CharField(max_length=255,blank=True, null=True)
    postcode = models.CharField(max_length=10,blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    phoneno = models.CharField(max_length=255,blank=True, null=True)
    logo = models.CharField(max_length=255,blank=True, null=True)
    product_type = models.CharField(max_length=255,blank=True, null=True)
    email = models.CharField(max_length=255,blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='0')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='0')
    class Meta:
        db_table = 'engageboost_account_channels'

class EngageboostAccountTypes(models.Model):
    enum_choices = (
        ('0', '0'),
        ('1', '1')
    )
    account_name = models.CharField(max_length=255,blank=True, null=True)
    createdby_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='0')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='0')
    class Meta:
        db_table = 'engageboost_account_types'

class EngageboostActivities(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    section_id = models.IntegerField(blank=True, null=True)
    section = models.CharField(max_length=255,blank=True, null=True)
    activity_master_id = models.IntegerField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    missing_image_type = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    action_type = models.CharField(max_length=45,blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_activities'

class EngageboostActivitySettings(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    activity_master_id = models.IntegerField(blank=True, null=True)
    web = models.SmallIntegerField(blank=True, null=True)
    email = models.SmallIntegerField(blank=True, null=True)
    sms = models.SmallIntegerField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_activity_settings'

class EngageboostAffiliateDetails(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phno = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_affiliate_details'

class EngageboostAmazonBoostCategories(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    name = models.CharField(max_length=255,blank=True, null=True)
    amazon_name = models.CharField(max_length=255,blank=True, null=True)
    parrent_id = models.IntegerField(blank=True, null=True)
    categorylevel = models.IntegerField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    iscreated = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_amazon_boost_categories'

class EngageboostAmazonCategories(models.Model):
    category_label = models.CharField(max_length=255,blank=True, null=True)
    category_name = models.CharField(max_length=255, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    categorylevel = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_amazon_categories'

class EngageboostAmazonCredentials(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    merchant_id = models.CharField(max_length=256, blank=True, null=True)
    access_key = models.CharField(max_length=255, blank=True, null=True)
    secret_key = models.CharField(max_length=255, blank=True, null=True)
    default_category = models.IntegerField(blank=True, null=True)
    channel_site_ids = models.CharField(max_length=255,blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    channel_parrent_id = models.IntegerField(blank=True, null=True)
    company_website_id = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    created_on = models.DateField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    merchant_identifier = models.CharField(max_length=255,blank=True, null=True)
    class Meta:
        db_table = 'engageboost_amazon_credentials'

class EngageboostAmazonFeedReport(models.Model):
    enum_choices = (
        ('success', 'success'),
        ('warning', 'warning'),
        ('error', 'error')
    )
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    company_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    amz_transacn_ids = models.BigIntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    marketplace_id = models.IntegerField(blank=True, null=True)
    product_sku = models.CharField(max_length=255,blank=True, null=True)
    status = models.CharField(max_length=20,choices=enum_choices,default='success')
    error_desc = models.TextField(blank=True, null=True)
    is_price = models.CharField(max_length=2,choices=enum_choices,default='n')
    is_inventory = models.CharField(max_length=2,choices=enum_choices,default='n')
    is_image = models.CharField(max_length=2,choices=enum_choices,default='n')
    last_modified = models.DateField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_amazon_feed_report'

class EngageboostAmazonFeedStatus(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    product_id = models.IntegerField(blank=True, null=True)
    marketplace_id = models.IntegerField(blank=True, null=True)
    amazon_process_id = models.BigIntegerField(blank=True, null=True)
    status = models.CharField(max_length=255,blank=True, null=True)
    is_result_called = models.CharField(max_length=2,choices=enum_choices,default='n')
    created_on = models.DateTimeField(blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    is_ready = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    class Meta:
        db_table = 'engageboost_amazon_feed_status'

class EngageboostAmazonFlatFileHeaders(models.Model):
    value = models.TextField(blank=True, null=True)
    rownumber = models.IntegerField(blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_amazon_flat_file_headers'

class EngageboostAmazonItemTransactions(models.Model):
    order_id = models.IntegerField(blank=True, null=True)
    amazon_order_id = models.CharField(max_length=255,blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    amazon_item_id = models.CharField(max_length=250,blank=True, null=True)
    product_title = models.CharField(max_length=255,blank=True, null=True)
    product_price = models.FloatField(blank=True, null=True)
    product_quantity = models.IntegerField(blank=True, null=True)
    currency_code = models.CharField(max_length=111,blank=True, null=True)
    shipping_currency = models.CharField(max_length=111,blank=True, null=True)
    shipping_price = models.FloatField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_amazon_item_transactions'

class EngageboostAmazonOrders(models.Model):
    website_id = models.IntegerField()
    amazon_order_id = models.CharField(max_length=255)
    purchase_date = models.DateTimeField()
    last_update_date = models.DateTimeField(blank=True, null=True)
    order_status = models.CharField(max_length=255)
    fullfillment_channel = models.CharField(max_length=255)
    sales_channel = models.CharField(max_length=255)
    ship_service_level = models.CharField(max_length=255, blank=True, null=True)
    shipping_to_name = models.CharField(max_length=255, blank=True, null=True)
    addr_line = models.CharField(max_length=255, blank=True, null=True)
    addr_line_2 = models.CharField(max_length=255, blank=True, null=True)
    shipping_city = models.CharField(max_length=255, blank=True, null=True)
    shipping_region = models.CharField(max_length=255, blank=True, null=True)
    shipping_postal_code = models.CharField(max_length=255, blank=True, null=True)
    shipping_country_code = models.CharField(max_length=255, blank=True, null=True)
    shipping_phone = models.CharField(max_length=255, blank=True, null=True)
    currency_code = models.CharField(max_length=255, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    no_of_item_shipped = models.IntegerField(blank=True, null=True)
    no_of_item_unshipped = models.IntegerField(blank=True, null=True)
    created_before = models.DateTimeField(blank=True, null=True)
    marketplace_id = models.CharField(max_length=255, blank=True, null=True)
    buyer_email = models.CharField(max_length=255, blank=True, null=True)
    buyer_name = models.CharField(max_length=255, blank=True, null=True)
    shipmentservicelevelcategory = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    class Meta:
        db_table = 'engageboost_amazon_orders'

class EngageboostAmazonProductBulletpoints(models.Model):
    product_id = models.IntegerField()
    channel_id = models.IntegerField()
    bullet_point = models.TextField()
    class Meta:
        db_table = 'engageboost_amazon_product_bulletpoints'

class EngageboostAmazonebtg(models.Model):
    node_id = models.BigIntegerField(blank=True, null=True)
    browse_name = models.CharField(max_length=100,blank=True, null=True)
    parent_node_id = models.BigIntegerField(blank=True, null=True)
    catagory = models.IntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    item_type = models.CharField(max_length=100,blank=True, null=True)
    categorylevel = models.IntegerField(blank=True, null=True)
    leafcategory = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_amazonebtg'

class EngageboostAppCategory(models.Model):
    appcategory = models.CharField(max_length=222,blank=True, null=True)
    numberofapp = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_app_category'

class EngageboostAppMaster(models.Model):
    appimage = models.CharField(max_length=222,blank=True, null=True)
    apptitle = models.CharField(max_length=222,blank=True, null=True)
    appnumrating = models.IntegerField(blank=True, null=True)
    apptotalrating = models.IntegerField(blank=True, null=True)
    appdescription = models.TextField(blank=True, null=True)
    appnotes = models.TextField(blank=True, null=True)
    appvideo = models.TextField(blank=True, null=True)
    apprice = models.FloatField(blank=True, null=True)
    appnuminstall = models.IntegerField(blank=True, null=True)
    appcategory = models.IntegerField(blank=True, null=True)
    otherimages = models.TextField(blank=True, null=True)
    techsupportmailid = models.CharField(max_length=222,blank=True, null=True)
    appdeveloper = models.CharField(max_length=222,blank=True, null=True)
    freetrial = models.IntegerField(blank=True, null=True)
    apppath = models.CharField(max_length=222,blank=True, null=True)
    class Meta:
        db_table = 'engageboost_app_master'

class EngageboostAppReviews(models.Model):
    appid = models.IntegerField(blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    reviewby = models.CharField(max_length=222,blank=True, null=True)
    reviewdate = models.DateField(blank=True, null=True)
    customerid = models.IntegerField(blank=True, null=True)
    reviewrate = models.IntegerField(blank=True, null=True)
    reviewtitle = models.CharField(max_length=222,blank=True, null=True)
    class Meta:
        db_table = 'engageboost_app_reviews'

class EngageboostAppWebsites(models.Model):
    appid = models.IntegerField(blank=True, null=True)
    websiteid = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_app_websites'

class EngageboostApplicableZipcodes(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    area_name = models.CharField(max_length=256, blank=True, null=True)
    isdeleted = models.SmallIntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_applicable_zipcodes'

class EngageboostAppointments(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    shipment_id = models.IntegerField(blank=True, null=True)
    order_id = models.TextField(blank=True, null=True)
    token_number = models.CharField(max_length=250, blank=True, null=True)
    shipping_provider = models.CharField(max_length=100, blank=True, null=True)
    shipping_method_id = models.SmallIntegerField(blank=True, null=True)
    appointment_date = models.DateTimeField(blank=True, null=True)
    send_mail_to_courier = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    courier_email = models.CharField(max_length=100, blank=True, null=True)
    email_subject = models.TextField(blank=True, null=True)
    email_body = models.TextField(blank=True, null=True)
    is_attach_manifest = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_appointments'

class EngageboostAppstores(models.Model):
    enum_choices = (
        ('0', '0'),
        ('1', '1')
    )
    menu_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=150,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    apprice = models.FloatField(blank=True, null=True)
    appimage = models.CharField(max_length=250,blank=True, null=True)
    support_email = models.CharField(max_length=250,blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    createdby = models.IntegerField(default='1')
    updatedby = models.IntegerField(default='1')
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_appstores'

class EngageboostAssetPaths(models.Model):
    Root_CHOICES = (
        ('cdn', 'cdn'),
        ('tpl', 'tpl'),
        ('live', 'live')
    )
    File_CHOICES = (
        ('css', 'css'),
        ('js', 'js')
    )
    Type_CHOICES = (
        ('web', 'web'),
        ('mob', 'mob'),
        ('fcb', 'fcb'),
        ('eby', 'eby')
    )
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    bucket = models.CharField(max_length=50, blank=True, null=True)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    website_name = models.CharField(max_length=50, blank=True, null=True)
    root = models.CharField(max_length=10,choices=Root_CHOICES, null=True)
    folder = models.CharField(max_length=50, blank=True, null=True)
    file = models.CharField(max_length=10,choices=File_CHOICES, null=True)
    type = models.CharField(max_length=10,choices=Type_CHOICES, null=True)
    ext = models.CharField(max_length=50, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices, default='n',null=True)
    ismodified = models.CharField(max_length=2,choices=enum_choices, default='n',null=True)
    class Meta:
        db_table = 'engageboost_asset_paths'

class EngageboostAtompaynetReturnurlDetails(models.Model):
    status = models.CharField(max_length=255,blank=True, null=True)
    website_id = models.BigIntegerField(blank=True, null=True)
    customer_id = models.BigIntegerField(blank=True, null=True)
    atom_txn_id = models.BigIntegerField(blank=True, null=True)
    mer_txn_id = models.BigIntegerField(blank=True, null=True)
    bank_txn_id = models.BigIntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    product = models.CharField(max_length=255,blank=True, null=True)
    txn_date = models.DateTimeField(blank=True, null=True)
    bank_name = models.CharField(max_length=255,blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_atompaynet_returnurl_details'

class EngageboostAuthorizeNetReturnDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    response_code = models.IntegerField(blank=True, null=True)
    response_subcode = models.IntegerField(blank=True, null=True)
    reason_code = models.IntegerField(blank=True, null=True)
    reason_text = models.TextField(blank=True, null=True)
    authorization_code = models.CharField(max_length=50, blank=True, null=True)
    avs_response = models.TextField(blank=True, null=True)
    transaction_id = models.TextField(blank=True, null=True)
    invoice_no = models.TextField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    method = models.CharField(max_length=255, blank=True, null=True)
    transaction_type = models.CharField(max_length=255, blank=True, null=True)
    customer_id = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)
    ship_to_first_name = models.CharField(max_length=255, blank=True, null=True)
    ship_to_last_name = models.CharField(max_length=255, blank=True, null=True)
    ship_to_company = models.CharField(max_length=255, blank=True, null=True)
    ship_to_addess = models.CharField(max_length=255, blank=True, null=True)
    ship_to_city = models.CharField(max_length=255, blank=True, null=True)
    ship_to_state = models.CharField(max_length=255, blank=True, null=True)
    ship_to_zipcode = models.CharField(max_length=255, blank=True, null=True)
    ship_to_country = models.CharField(max_length=255, blank=True, null=True)
    tax = models.CharField(max_length=255, blank=True, null=True)
    duty = models.CharField(max_length=255, blank=True, null=True)
    freight = models.CharField(max_length=255, blank=True, null=True)
    tax_exempt = models.CharField(max_length=255, blank=True, null=True)
    purchase_order_number = models.CharField(max_length=255, blank=True, null=True)
    md_hash = models.CharField(max_length=255, blank=True, null=True)
    card_code_response = models.CharField(max_length=255, blank=True, null=True)
    cardholder_verification_response = models.CharField(max_length=255, blank=True, null=True)
    account_no = models.CharField(max_length=255, blank=True, null=True)
    card_type = models.CharField(max_length=255, blank=True, null=True)
    split_tender_id = models.CharField(max_length=255, blank=True, null=True)
    requested_amount = models.CharField(max_length=255, blank=True, null=True)
    balance_on_card = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_authorize_net_return_details'

class EngageboostAutoProductUploads(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    file_name = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    is_completed = models.CharField(max_length=2,choices=enum_choices, default='n',null=True)
    date = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_auto_product_uploads'

class EngageboostAwbMasters(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    awb_number = models.CharField(max_length=256, blank=True, null=True)
    tracking_company_name = models.CharField(max_length=256, blank=True, null=True)
    shipping_method_id = models.SmallIntegerField(blank=True, null=True)
    isused = models.CharField(max_length=2,choices=enum_choices, default='n')
    order_id = models.IntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices, default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_awb_masters'

class EngageboostCcavenueReturnDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    merchant_id = models.TextField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    currency = models.TextField(blank=True, null=True)
    checksum = models.TextField(blank=True, null=True)
    checksumall = models.TextField(blank=True, null=True)
    merchant_param = models.TextField(blank=True, null=True)
    auth_status = models.TextField(blank=True, null=True)
    billing_cust_name = models.TextField(blank=True, null=True)
    billing_middle_name = models.TextField(blank=True, null=True)
    billing_last_name = models.TextField(blank=True, null=True)
    billing_cust_address = models.TextField(blank=True, null=True)
    billing_cust_city = models.TextField(blank=True, null=True)
    billing_cust_state = models.TextField(blank=True, null=True)
    billing_cust_zip = models.TextField(blank=True, null=True)
    billing_cust_country = models.TextField(blank=True, null=True)
    billing_cust_tel_ctry = models.TextField(blank=True, null=True)
    billing_cust_tel_area = models.TextField(blank=True, null=True)
    billing_cust_tel_no = models.TextField(blank=True, null=True)
    billing_cust_email = models.TextField(blank=True, null=True)
    billing_cust_notes = models.TextField(blank=True, null=True)
    delivery_cust_name = models.TextField(blank=True, null=True)
    delivery_middle_name = models.TextField(blank=True, null=True)
    delivery_last_name = models.TextField(blank=True, null=True)
    delivery_cust_address = models.TextField(blank=True, null=True)
    delivery_cust_city = models.TextField(blank=True, null=True)
    delivery_cust_state = models.TextField(blank=True, null=True)
    delivery_cust_country = models.TextField(blank=True, null=True)
    delivery_cust_zip = models.TextField(blank=True, null=True)
    delivery_cust_tel_ctry = models.TextField(blank=True, null=True)
    delivery_cust_tel_area = models.TextField(blank=True, null=True)
    delivery_cust_tel_no = models.TextField(blank=True, null=True)
    nb_bid = models.TextField(blank=True, null=True)
    nb_order_no = models.TextField(blank=True, null=True)
    card_category = models.TextField(blank=True, null=True)
    bank_name = models.TextField(blank=True, null=True)
    bankrespcode = models.TextField(blank=True, null=True)
    bankrespmsg = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_ccavenue_return_details'

class EngageboostCcavenueUpgradedReturnDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    tracking_id = models.CharField(max_length=50, blank=True, null=True)
    bank_ref_no = models.CharField(max_length=50, blank=True, null=True)
    si_ref_no = models.CharField(max_length=50, blank=True, null=True)
    order_status = models.CharField(max_length=20,blank=True, null=True)
    failure_message = models.CharField(max_length=255, blank=True, null=True)
    payment_mode = models.CharField(max_length=100, blank=True, null=True)
    card_name = models.CharField(max_length=100, blank=True, null=True)
    status_code = models.CharField(max_length=100, blank=True, null=True)
    status_message = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=5,blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    billing_name = models.CharField(max_length=100, blank=True, null=True)
    billing_address = models.CharField(max_length=255, blank=True, null=True)
    billing_city = models.CharField(max_length=50, blank=True, null=True)
    billing_state = models.CharField(max_length=50, blank=True, null=True)
    billing_zip = models.IntegerField(blank=True, null=True)
    billing_country = models.CharField(max_length=50, blank=True, null=True)
    billing_tel = models.CharField(max_length=20, blank=True, null=True)
    billing_email = models.CharField(max_length=100, blank=True, null=True)
    delivery_name = models.CharField(max_length=100, blank=True, null=True)
    delivery_address = models.CharField(max_length=255, blank=True, null=True)
    delivery_city = models.CharField(max_length=50, blank=True, null=True)
    delivery_state = models.CharField(max_length=50, blank=True, null=True)
    delivery_zip = models.IntegerField(blank=True, null=True)
    delivery_country = models.CharField(max_length=50, blank=True, null=True)
    delivery_tel = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    payment_response_full = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'engageboost_ccavenue_upgraded_return_details'

class EngageboostAxisReturnDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    vpc_amount = models.CharField(max_length=255, blank=True, null=True)
    vpc_locale = models.CharField(max_length=255, blank=True, null=True)
    vpc_batchno = models.CharField(max_length=255, blank=True, null=True)
    vpc_command = models.CharField(max_length=255, blank=True, null=True)
    vpc_message = models.CharField(max_length=255, blank=True, null=True)
    vpc_version = models.CharField(max_length=255, blank=True, null=True)
    vpc_card = models.CharField(max_length=255, blank=True, null=True)
    vpc_orderinfo = models.CharField(max_length=255, blank=True, null=True)
    vpc_receiptno = models.CharField(max_length=255, blank=True, null=True)
    vpc_merchant = models.CharField(max_length=255, blank=True, null=True)
    vpc_authorizeid = models.CharField(max_length=255, blank=True, null=True)
    vpc_merchtxnref = models.CharField(max_length=255, blank=True, null=True)
    vpc_transactionno = models.CharField(max_length=255, blank=True, null=True)
    vpc_acqresponsecode = models.CharField(max_length=255, blank=True, null=True)
    vpc_txnresponsecode = models.CharField(max_length=255, blank=True, null=True)
    vpc_vertype = models.CharField(max_length=255, blank=True, null=True)
    vpc_verstatus = models.CharField(max_length=255, blank=True, null=True)
    vpc_vertoken = models.CharField(max_length=255, blank=True, null=True)
    vpc_versecuritylevel = models.CharField(max_length=255, blank=True, null=True)
    vpc_3dsenrolled = models.CharField(max_length=255, blank=True, null=True)
    vpc_3dsxid = models.CharField(max_length=255, blank=True, null=True)
    vpc_3dseci = models.CharField(max_length=255, blank=True, null=True)
    vpc_3dsstatus = models.CharField(max_length=255, blank=True, null=True)
    tr_date = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_axis_return_details'


# checked and verified by cds on 13-06-2019
class EngageboostCmsMenus(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    parent_id = models.IntegerField(default=0)
    company_website_id = models.IntegerField(blank=True, null=True)
    flag = models.IntegerField(blank=True, null=True, default=0)
    page_id = models.IntegerField(blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    ulorder = models.IntegerField(blank=True, null=True)
    liorder = models.IntegerField(blank=True, null=True)
    label = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    device = models.CharField(blank=True, null=True, max_length=10)
    class Meta:
        db_table = 'engageboost_cms_menus'


class EngageboostCmsPageSettings(models.Model):

    company_website_id = models.IntegerField()
    temp_id = models.IntegerField()
    page_id = models.IntegerField()
    widgets = models.IntegerField(blank=True, null=True)
    property_value = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    createdby = models.IntegerField(null=True)
    updatedby = models.IntegerField(null=True)
    lang = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_cms_page_settings'

class EngageboostCommissionSettings(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    channel_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)
    category_name1 = models.CharField(max_length=255, blank=True, null=True)
    category_name2 = models.CharField(max_length=255, blank=True, null=True)
    category_name3 = models.CharField(max_length=255, blank=True, null=True)
    category_name4 = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    commission_rate = models.FloatField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_commission_settings'

class EngageboostCompanies(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    enum_choicess = (
        ('trial', 'trial'),
        ('paid', 'paid'),
        ('hold', 'hold')
    )
    username = models.CharField(max_length=255,blank=True, null=True)
    password = models.CharField(max_length=255,blank=True, null=True)
    email = models.CharField(max_length=255,blank=True, null=True)
    plan_id = models.BigIntegerField(blank=True, null=True)
    business_name = models.CharField(max_length=255,blank=True, null=True)
    company_name = models.CharField(max_length=255,blank=True, null=True)
    boost_url = models.CharField(max_length=255,blank=True, null=True)
    website_url = models.CharField(max_length=255,blank=True, null=True)
    company_logo = models.CharField(max_length=255,blank=True, null=True)
    city = models.CharField(max_length=255,blank=True, null=True)
    state = models.CharField(max_length=255,blank=True, null=True)
    postcode = models.CharField(max_length=255,blank=True, null=True)
    phone = models.CharField(max_length=255,blank=True, null=True)
    skype_id = models.TextField(blank=True, null=True)
    country = models.ForeignKey(EngageboostCountries,on_delete=models.CASCADE, blank=True, null=True)
    reset_password = models.CharField(max_length=2,choices=enum_choices,default='n')
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20,choices=enum_choicess,default='trial')
    is_verified = models.CharField(max_length=2,choices=enum_choices,default='y')
    verified_code = models.CharField(max_length=30,blank=True, null=True)
    database_name = models.CharField(max_length=255,blank=True, null=True)
    database_user_name = models.CharField(max_length=255,blank=True, null=True)
    database_password = models.CharField(max_length=255,blank=True, null=True)
    is_take_tour = models.IntegerField(blank=True, null=True)
    terms_condition_accepted = models.CharField(max_length=2,choices=enum_choices,default='n')
    terms_accepted_ip = models.CharField(max_length=255,blank=True, null=True)
    terms_accepted_browser = models.CharField(max_length=255,blank=True, null=True)
    terms_accepted_device = models.CharField(max_length=255,blank=True, null=True)
    terms_accepted_date = models.DateField(blank=True, null=True)
    is_permission_changed = models.CharField(max_length=2,choices=enum_choices,default='n')
    inactive_reason = models.TextField(blank=True, null=True)
    delete_reason = models.TextField(blank=True, null=True)
    last_login = models.DateField(blank=True, null=True)
    last_login_ip = models.CharField(max_length=50, blank=True, null=True)
    login_salt = models.CharField(max_length=255, blank=True, null=True)
    no_of_shipment = models.IntegerField(blank=True, null=True)
    no_of_product = models.IntegerField(blank=True, null=True)
    db_host = models.CharField(max_length=255,blank=True, null=True)
    is_seperated = models.CharField(max_length=2,choices=enum_choices,default='n')
    is_active_for = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_companies'

class EngageboostCompaniesCrons(models.Model):
    Type_CHOICES = (
        ('auto', 'auto'),
        ('fixed', 'fixed')
    )
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    company_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    cron_type = models.CharField(max_length=10,choices=Type_CHOICES,default='fixed')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_companies_crons'

class EngageboostCompanyAuthentication(models.Model):
    For_CHOICES = (
        ('POS', 'POS'),
        ('other', 'other')
    )
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    engageboost_company_id = models.IntegerField(blank=True, null=True)
    authkey = models.CharField(max_length=255,blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    for_option = models.CharField(max_length=10,choices=For_CHOICES)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_company_authentication'

class EngageboostCompanyWebsiteMap(models.Model):
    company_id = models.IntegerField()
    domain_name = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_company_website_map'

class EngageboostCompanyWebsites(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    Dns_CHOICES = (
        ('Ok', 'Ok'),
        ('Not Configured', 'Not Configured'),
        ('Failed', 'Failed')
    )
    engageboost_company_id = models.IntegerField()
    plan_id = models.BigIntegerField()
    business_name = models.CharField(max_length=255,blank=True, null=True)
    company_name = models.CharField(max_length=255,blank=True, null=True)
    email = models.CharField(max_length=255,blank=True, null=True)
    website_url = models.CharField(max_length=255,blank=True, null=True)
    domain_name = models.CharField(max_length=255, blank=True, null=True)
    s3folder_name = models.CharField(max_length=255, blank=True, null=True)
    websitename = models.CharField(max_length=255,blank=True, null=True)
    website_category_id = models.IntegerField()
    engageboost_template_master_id = models.IntegerField()
    engageboost_template_color_master_id = models.IntegerField()
    website_logo = models.CharField(max_length=255,blank=True, null=True)
    id_proof = models.CharField(max_length=255,blank=True, null=True)
    address_proof = models.CharField(max_length=255,blank=True, null=True)
    other_document = models.CharField(max_length=255,blank=True, null=True)
    first_name = models.CharField(max_length=255,blank=True, null=True)
    last_name = models.CharField(max_length=255,blank=True, null=True)
    address1 = models.CharField(max_length=255,blank=True, null=True)
    address2 = models.CharField(max_length=255,blank=True, null=True)
    city = models.CharField(max_length=255,blank=True, null=True)
    state = models.CharField(max_length=255,blank=True, null=True)
    postcode = models.CharField(max_length=255,blank=True, null=True)
    phone = models.CharField(max_length=255,blank=True, null=True)
    country = models.ForeignKey(EngageboostCountries,on_delete=models.CASCADE, blank=True, null=True)
    currency_id = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=255,blank=True, null=True)
    relation = models.CharField(max_length=255,blank=True, null=True)
    marital_status = models.CharField(max_length=255,blank=True, null=True)
    monthly_maintenance = models.CharField(max_length=255,blank=True, null=True)
    race = models.CharField(max_length=255,blank=True, null=True)
    bank_name = models.CharField(max_length=255,blank=True, null=True)
    account_no = models.CharField(max_length=255,blank=True, null=True)
    ifsc_code = models.CharField(max_length=255,blank=True, null=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    is_dns_configured = models.IntegerField(blank=True, null=True)
    signup_country = models.CharField(max_length=255,blank=True, null=True)
    dns_configured_date = models.DateField(blank=True, null=True)
    dns_status = models.CharField(max_length=20,choices=Dns_CHOICES,default='Not Configured', null=True)
    dns_folder_name = models.CharField(max_length=255, blank=True, null=True)
    live_or_sandbox = models.CharField(max_length=2,choices=enum_choices,default='y', null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_company_websites'

class EngageboostCossSellProducts(models.Model):
    product_id = models.IntegerField(blank=True, null=True)
    cross_product = models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE,blank=True, null=True)
    class Meta:
        db_table = 'engageboost_coss_sell_products'

class EngageboostCrates(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    crate_barcode = models.CharField(max_length=20, blank=True, null=True)
    # shipment_id = models.BigIntegerField(blank=True, null=True)
    trent_picklist_id = models.IntegerField(blank=True, null=True)
    order_id = models.BigIntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_crates'

class EngageboostCreditcardSettingInformations(models.Model):
    enum_choices = (
        ('Y', 'Y'),
        ('N', 'N')
    )
    website_id = models.IntegerField(blank=True, null=True)
    payment_type_id = models.IntegerField(blank=True, null=True)
    creditcard_id = models.IntegerField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='N', null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='N', null=True)
    class Meta:
        db_table = 'engageboost_creditcard_setting_informations'

class EngageboostCreditcardTypes(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    name = models.CharField(max_length=50, blank=True, null=True)
    value = models.CharField(max_length=50, blank=True, null=True)
    image = models.CharField(max_length=50, blank=True, null=True)
    ebay_term = models.CharField(max_length=255, blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    class Meta:
        db_table = 'engageboost_creditcard_types'

class EngageboostCurrencyMasters(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    engageboost_country = models.ForeignKey(EngageboostCountries,on_delete=models.CASCADE, blank=True, null=True)
    currencyname = models.CharField(max_length=255,blank=True, null=True)
    currency = models.CharField(max_length=255,blank=True, null=True)
    currencysymbol = models.CharField(max_length=255,blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_currency_masters'

class EngageboostCurrencyRates(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    country = models.ForeignKey(EngageboostCountries,on_delete=models.CASCADE, blank=True, null=True)
    engageboost_company_website_id = models.BigIntegerField()
    engageboost_currency_master = models.ForeignKey(EngageboostCurrencyMasters,on_delete=models.CASCADE,related_name='currency_rates',blank=True, null=True)
    currency_code = models.CharField(max_length=10,blank=True, null=True)
    exchange_rate = models.DecimalField(max_digits=15, decimal_places=4,blank=True, null=True)
    isbasecurrency = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    createdby = models.IntegerField(default='0')
    updatedby = models.IntegerField(default='0')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_currency_rates'

class EngageboostCustomEmails(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    user_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    page_id = models.IntegerField(blank=True, null=True)
    email_admin = models.CharField(max_length=2,choices=enum_choices,default='y')
    email_user = models.CharField(max_length=2,choices=enum_choices,default='n')
    email_from = models.TextField(blank=True, null=True)
    email_bcc = models.TextField(blank=True, null=True)
    admin_subject = models.TextField(blank=True, null=True)
    admin_body = models.TextField(blank=True, null=True)
    user_subject = models.TextField(blank=True, null=True)
    user_body = models.TextField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='y')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='y')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_custom_emails'

class EngageboostCustomFields(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    user_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    page_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    ftype = models.CharField(max_length=100, blank=True, null=True)
    def_val = models.CharField(max_length=100, blank=True, null=True)
    required = models.CharField(max_length=1, blank=True, null=True)
    options = models.TextField(blank=True, null=True)
    minlength = models.CharField(max_length=20, blank=True, null=True)
    maxlength = models.CharField(max_length=20, blank=True, null=True)
    rows = models.CharField(max_length=5, blank=True, null=True)
    cols = models.CharField(max_length=5, blank=True, null=True)
    style = models.TextField(blank=True, null=True)
    orders = models.IntegerField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='y')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='y')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_custom_fields'

class EngageboostCustomForms(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    user_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    page_id = models.IntegerField(blank=True, null=True)
    campaign_id = models.IntegerField(blank=True, null=True)
    ip = models.TextField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='y')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='y')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_custom_forms'

class EngageboostCustomValues(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    custom_form_id = models.IntegerField(blank=True, null=True)
    custom_field_id = models.IntegerField(blank=True, null=True)
    custom_field_value = models.CharField(max_length=255,blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='y')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='y')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_custom_values'

class EngageboostDbWebsitehits(models.Model):
    company_website_id = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    visits = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_db_websitehits'

class EngageboostDbWebsitestats(models.Model):
    company_website_id = models.IntegerField(blank=True, null=True)
    revenue = models.IntegerField(blank=True, null=True)
    products = models.IntegerField(blank=True, null=True)
    orders = models.IntegerField(blank=True, null=True)
    customers = models.IntegerField(blank=True, null=True)
    sitevisitors = models.IntegerField(blank=True, null=True)
    uniquevisitors = models.IntegerField(blank=True, null=True)
    amazon = models.IntegerField(blank=True, null=True)
    ebay = models.IntegerField(blank=True, null=True)
    webshop = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_db_websitestats'

class EngageboostDbWebsitevisitorshits(models.Model):
    company_website_id = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    visits = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_db_websitevisitorshits'

class EngageboostDefaultCategories(models.Model):
    website_category_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_default_categories'

class EngageboostDefaultEmailTypeContents(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    Type_CHOICES = (
        ('H', 'H'),
        ('T', 'T'),
        ('HT', 'HT')
    )
    description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    subject = models.CharField(max_length=255,blank=True, null=True)
    email_type = models.CharField(max_length=2,choices=Type_CHOICES,default='T')
    email_content = models.TextField(blank=True, null=True)
    email_content_text = models.TextField(blank=True, null=True)
    reply_to_email = models.TextField(blank=True, null=True)
    bcc = models.CharField(max_length=255,blank=True, null=True)
    email_from = models.CharField(max_length=255,blank=True, null=True)
    last_modified = models.DateField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    order_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_default_email_type_contents'

class EngageboostDefaultModuleLayoutFields(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    module_layout_section_id = models.BigIntegerField(blank=True, null=True)
    module_list_id = models.IntegerField(blank=True, null=True)
    field_id = models.IntegerField(blank=True, null=True)
    section_col = models.SmallIntegerField(blank=True, null=True)
    section_row = models.SmallIntegerField(blank=True, null=True)
    field_label = models.TextField(blank=True, null=True)
    model_field_value = models.TextField(blank=True, null=True)
    field_type = models.TextField(blank=True, null=True)
    input_type = models.TextField(blank=True, null=True)
    association_value = models.TextField(blank=True, null=True)
    default_values = models.TextField(blank=True, null=True)
    custom_values = models.TextField(blank=True, null=True)
    value_required = models.TextField(choices=enum_choices,default='n', null=True)
    is_system = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    is_optional = models.SmallIntegerField(blank=True, null=True)
    data_type = models.CharField(max_length=100, blank=True, null=True)
    data_length = models.CharField(max_length=100, blank=True, null=True)
    valid_rule = models.CharField(max_length=30, blank=True, null=True)
    err_msg = models.CharField(max_length=200, blank=True, null=True)
    score = models.CharField(max_length=150, blank=True, null=True)
    ajax_model = models.CharField(max_length=255,blank=True, null=True)
    ajax_field = models.CharField(max_length=255,blank=True, null=True)
    ajax_input_type = models.CharField(max_length=255,blank=True, null=True)
    ajax_update_field_id = models.IntegerField(blank=True, null=True)
    field_msg = models.CharField(max_length=255,blank=True, null=True)
    show_type = models.IntegerField(blank=True, null=True)
    show_market_places = models.CharField(max_length=255, blank=True, null=True)
    show_market_places_name = models.CharField(max_length=255, blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)
    channel_categories_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_default_module_layout_fields'

class EngageboostDefaultModuleLayoutSections(models.Model):
    module_list_id = models.BigIntegerField(blank=True, null=True)
    module_id = models.IntegerField(blank=True, null=True)
    default_section_id = models.IntegerField(blank=True, null=True)
    section_heading = models.CharField(max_length=100,blank=True, null=True)
    section_order_pos = models.SmallIntegerField(blank=True, null=True)
    seo_activate = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_default_module_layout_sections'

class EngageboostDefaultModuleLayouts(models.Model):
    layout_name = models.CharField(max_length=50,blank=True, null=True)
    module_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    module_name = models.CharField(max_length=50,blank=True, null=True)
    description = models.CharField(max_length=200,blank=True, null=True)
    class Meta:
        db_table = 'engageboost_default_module_layouts'

class EngageboostDefaultSections(models.Model):
    name = models.CharField(max_length=255,blank=True, null=True)
    module_id = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    seo_activate = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_default_sections'

class EngageboostDefaultsFields(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    is_variant_choices = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=25, blank=True, null=True)
    field_name = models.CharField(max_length=50, blank=True, null=True)
    associate_value = models.CharField(max_length=255, blank=True, null=True)
    is_optional = models.SmallIntegerField(blank=True, null=True,default='0')
    is_variant = models.CharField(max_length=10,choices=is_variant_choices,default='No', null=True)
    input_type = models.CharField(max_length=200, blank=True, null=True)
    custom_values = models.TextField(blank=True, null=True)
    data_type = models.CharField(max_length=100, blank=True, null=True)
    data_length = models.CharField(max_length=100, blank=True, null=True)
    callback_events = models.TextField(blank=True, null=True)
    err_msg = models.CharField(max_length=255, blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    createdby = models.IntegerField(default='1')
    updatedby = models.IntegerField(default='1')
    visible_in_filter = models.IntegerField(default=0)
    class Meta:
        db_table = 'engageboost_defaults_fields'

class EngageboostDeliveryManagers(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    zone = models.CharField(max_length=255, blank=True, null=True)
    warehouse_ids = models.CharField(max_length=255, blank=True, null=True)
    area = models.TextField(blank=True, null=True)
    address1 = models.CharField(max_length=500, blank=True, null=True)
    address2 = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    class Meta:
        db_table = 'engageboost_delivery_managers'

class EngageboostDeliveryPlanOrder(models.Model):
    order_id = models.IntegerField(blank=True, null=True)
    orders = models.IntegerField(blank=True, null=True)
    distance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    time = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shipment_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    virtual_vechile_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_delivery_plan_order'

class EngageboostDeliverySlot(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    based_on_choices = (
        ('SameDay', 'SameDay'),
        ('PrevDay', 'PrevDay')
    )
    location_id = models.IntegerField(blank=True, null=True)
    zone_id = models.IntegerField(blank=True, null=True)
    warehouse = models.ForeignKey(EngageboostWarehouseMasters,on_delete=models.CASCADE, blank=True, null=True)
    day_id = models.IntegerField(blank=True, null=True)
    start_time = models.CharField(max_length=20, blank=True, null=True)
    end_time = models.CharField(max_length=20, blank=True, null=True)
    cutoff_time = models.CharField(max_length=20, blank=True, null=True)
    order_qty_per_slot = models.IntegerField(blank=True, null=True)
    based_on = models.CharField(max_length=20,choices=based_on_choices,default='SameDay')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_delivery_slot'

class EngageboostDhlZipcodeLists(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    region = models.CharField(max_length=255,blank=True, null=True)
    dstarea = models.CharField(max_length=255,blank=True, null=True)
    dstsrvctr = models.CharField(max_length=255,blank=True, null=True)
    dpzone = models.CharField(max_length=255,blank=True, null=True)
    dpflag = models.CharField(max_length=255,blank=True, null=True)
    pincode = models.CharField(max_length=255,blank=True, null=True)
    careadesc = models.CharField(max_length=255,blank=True, null=True)
    cscrcddesc = models.CharField(max_length=255,blank=True, null=True)
    class Meta:
        db_table = 'engageboost_dhl_zipcode_lists'

class EngageboostDirecpayReturnDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    transaction_id = models.CharField(max_length=20,blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=4,blank=True, null=True)
    country = models.CharField(max_length=4,blank=True, null=True)
    status = models.CharField(max_length=10,blank=True, null=True)
    class Meta:
        db_table = 'engageboost_direcpay_return_details'

class EngageboostDiscountMasters(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    Type_CHOICES = (
        ('p', 'p'),
        ('c', 'c')
    )
    website_id = models.IntegerField()
    warehouse_id = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    disc_type = models.IntegerField(blank=True, null=True)
    disc_start_date = models.DateTimeField(blank=True, null=True)
    disc_end_date = models.DateTimeField(blank=True, null=True)
    customer_group = models.CharField(max_length=255, blank=True, null=True)
    discount_type = models.CharField(max_length=2,choices=Type_CHOICES,default='p')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    discount_master_type = models.IntegerField(blank=True, null=True)
    discount_priority = models.IntegerField(blank=True, null=True)
    coupon_code = models.CharField(max_length=255, blank=True, null=True)
    coupon_prefix = models.CharField(max_length=50, blank=True, null=True)
    coupon_suffix = models.CharField(max_length=50, blank=True, null=True)
    coupon_type = models.IntegerField(blank=True, null=True)
    has_multiplecoupons = models.CharField(max_length=2,choices=enum_choices,default='n')
    used_coupon = models.IntegerField(blank=True, null=True)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    freebies_product_ids = models.CharField(max_length=255, blank=True, null=True)
    freebies_product_sku = models.CharField(max_length=500, blank=True, null=True)
    no_of_quantity_per = models.IntegerField(blank=True, null=True)
    usage_limit_per_user = models.IntegerField(blank=True, null=True)
    condition_for_freebie_items = models.CharField(max_length=100, blank=True, null=True)
    offer_type = models.CharField(max_length=21, blank=True, null=True)
    up_to_discount = models.FloatField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_discount_masters'

class EngageboostDiscountFreebieMappings(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    discount_master = models.ForeignKey(EngageboostDiscountMasters,on_delete=models.CASCADE,related_name='DiscountFreebieMappings',blank=True, null=True)
    product = models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE,related_name='DiscountFreebieProducts',blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_discount_freebie_mappings'

class EngageboostTempDiscountMasters(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    Type_CHOICES = (
        ('p', 'p'),
        ('c', 'c')
    )
    master_type_choices = (
        ('product specific', 'Product Specific'),
        ('coupon specific discount', 'Coupon Specific')
    )
    website_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    disc_type = models.IntegerField(blank=True, null=True)
    disc_start_date = models.DateTimeField(blank=True, null=True)
    disc_end_date = models.DateTimeField(blank=True, null=True)
    customer_group = models.CharField(max_length=255, blank=True, null=True)
    discount_type  = models.CharField(max_length=2,choices=Type_CHOICES,default='p')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    discount_master_type = models.IntegerField(blank=True, null=True)
    discount_priority = models.IntegerField(blank=True, null=True)
    coupon_code = models.CharField(max_length=255, blank=True, null=True)
    coupon_prefix = models.CharField(max_length=50, blank=True, null=True)
    coupon_suffix = models.CharField(max_length=50, blank=True, null=True)
    coupon_type = models.IntegerField(blank=True, null=True)
    has_multiplecoupons = models.CharField(max_length=2,choices=enum_choices,default='n')
    used_coupon = models.IntegerField(blank=True, null=True)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    freebies_product_ids = models.CharField(max_length=255, blank=True, null=True)
    freebies_product_sku = models.CharField(max_length=500, blank=True, null=True)
    no_of_quantity_per = models.IntegerField(blank=True, null=True)
    condition_for_freebie_items = models.CharField(max_length=100, blank=True, null=True)
    offer_type = models.CharField(max_length=21, blank=True, null=True)
    up_to_discount = models.FloatField(blank=True, null=True)
    file_name = models.TextField(blank=True, null=True)
    err_flag = models.IntegerField(blank=True, null=True)
    sku_equals = models.CharField(max_length=255, blank=True, null=True)
    sku_not_equals = models.CharField(max_length=255, blank=True, null=True)
    category_equals = models.CharField(max_length=255, blank=True, null=True)
    category_not_equals = models.CharField(max_length=255, blank=True, null=True)
    amount_equals = models.FloatField(blank=True, null=True)
    amount_equals_greater = models.FloatField(blank=True, null=True)
    amount_equals_less = models.FloatField(blank=True, null=True)
    free_item_sku = models.CharField(max_length=255, blank=True, null=True)
    free_item_quantity = models.CharField(max_length=255, blank=True, null=True)
    weekly_equals = models.CharField(max_length=255, blank=True, null=True)
    weekly_not_equals = models.CharField(max_length=255, blank=True, null=True)
    customer_equals = models.TextField(blank=True, null=True)
    customer_not_equals = models.TextField(blank=True, null=True)
    free_shipping = models.CharField(max_length=255,blank=True, null=True)
    number_of_coupon = models.IntegerField(blank=True, null=True)
    error_text = models.CharField(max_length=255,blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_temp_discount_masters'

class EngageboostDiscountMastersConditions(models.Model):
    enum_choices = (
            ('y', 'y'),
            ('n', 'n')
        )
    discount_master = models.ForeignKey(EngageboostDiscountMasters,on_delete=models.CASCADE,related_name='DiscountMastersConditions',blank=True, null=True)
    fields = models.IntegerField(blank=True, null=True)
    condition = models.CharField(max_length=255, blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    all_category_id = models.TextField(blank=True, null=True)
    all_product_id = models.TextField(blank=True, null=True)
    all_product_qty = models.TextField(blank=True, null=True)
    all_customer_id = models.TextField(blank=True, null=True)
    all_day_id = models.CharField(max_length=21, blank=True, null=True)
    condition_type = models.CharField(max_length=255, blank=True, null=True)
    field_type = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    createdby = models.IntegerField(default='0')
    updatedby = models.IntegerField(default='0')
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_discount_masters_conditions'

class EngageboostDiscountMastersCoupons(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    discount_master = models.ForeignKey(EngageboostDiscountMasters,on_delete=models.CASCADE,related_name='DiscountMastersCoupons',blank=True, null=True)
    coupon_code = models.CharField(max_length=255,blank=True, null=True)
    is_used = models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    createdby = models.IntegerField(default='0')
    updatedby = models.IntegerField(default='0')
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_discount_masters_coupons'


class EngageboostDriverLoginDetails(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    vehicle_id = models.IntegerField(blank=True, null=True)
    driver_id = models.IntegerField(blank=True, null=True)
    device_id = models.CharField(max_length=255,blank=True, null=True)
    checkin_date = models.DateField(blank=True, null=True)
    checkin_time = models.DateTimeField(blank=True, null=True)
    checkin_kilometer = models.FloatField(blank=True, null=True)
    checkout_time = models.DateTimeField(blank=True, null=True)
    checkout_kilometer = models.FloatField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_driver_login_details'

class EngageboostDriverVeichleMap(models.Model):
    driver_id = models.IntegerField(blank=True, null=True)
    vehicle_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    shipment_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    virtual_vechile_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_driver_veichle_map'

class EngageboostEbayBoostCategories(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    channel_category_id = models.BigIntegerField(blank=True, null=True)
    categorylevel = models.IntegerField(blank=True, null=True)
    categoryname = models.CharField(max_length=120,blank=True, null=True)
    categoryparentid = models.IntegerField(blank=True, null=True)
    leafcategory = models.IntegerField(blank=True, null=True)
    autopayenabled = models.IntegerField(blank=True, null=True)
    allowreserveprice = models.CharField(max_length=2,choices=enum_choices,default='n')
    minimumreserveprice = models.FloatField(blank=True, null=True)
    version = models.CharField(max_length=255,blank=True, null=True)
    channel_site_id = models.IntegerField(blank=True, null=True)
    is_variation_enanbled = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    is_custom_item_itemspecification_enabled = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    class Meta:
        db_table = 'engageboost_ebay_boost_categories'

class EngageboostEbayItemSpecification(models.Model):
    ebay_cat_id = models.IntegerField(blank=True, null=True)
    item_specification = models.CharField(max_length=255,blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    fieldtype = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_ebay_item_specification'

class EngageboostEbayItemSpecificationValue(models.Model):
    ebay_category_id = models.IntegerField(blank=True, null=True)
    item_specification_id = models.IntegerField(blank=True, null=True)
    value = models.CharField(max_length=255,blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_ebay_item_specification_value'

class EngageboostEbayProductCondition(models.Model):
    ebay_condition_id = models.IntegerField(blank=True, null=True)
    ebay_condition_name = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_ebay_product_condition'

class EngageboostEbaystoreCategories(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    boost_category_id = models.IntegerField(blank=True, null=True)
    boost_parent_category_id = models.IntegerField(blank=True, null=True)
    ebay_storecategory_id = models.BigIntegerField(blank=True, null=True)
    ebay_storecategory_parent_id = models.BigIntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    category_name = models.CharField(max_length=255,blank=True, null=True)
    category_url = models.CharField(max_length=255,blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_ebaystore_categories'

class EngageboostEmailTypeMasters(models.Model):
    name = models.CharField(max_length=255,blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_email_type_masters'

class EngageboostEmktCampaigns(models.Model):
    Contact_Type_CHOICES = (
        ('contactlist', 'contactlist'),
        ('segment', 'segment')
    )
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    Mailing_Status_CHOICES = (
        ('draft', 'draft'),
        ('sent', 'sent')
    )
    Mailing_Type_CHOICES = (
        ('HTML', 'HTML'),
        ('TEXT', 'TEXT'),
        ('HTML&TEXT', 'HTML&TEXT')
    )
    Mailing_Status_CHOICES = (
        ('success', 'success'),
        ('failure', 'failure'),
        ('none', 'none')
    )
    Delivery_Status_CHOICES = (
        ('sent', 'sent'),
        ('notsent', 'notsent')
    )
    campaign_name = models.CharField(max_length=255, blank=True, null=True)
    contact_type = models.CharField(max_length=20,choices=Contact_Type_CHOICES)
    contactlist_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    template_id = models.IntegerField(blank=True, null=True)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    fromname = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    reply_email = models.CharField(max_length=255, blank=True, null=True)
    campaign_data = models.TextField(blank=True, null=True)
    track_facebook = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    track_twitter = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    track_google = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    mailing_status = models.CharField(max_length=20,choices=Mailing_Status_CHOICES,default='draft')
    mail_type = models.CharField(max_length=20,choices=Mailing_Type_CHOICES,default='HTML')
    text_content = models.TextField(blank=True, null=True)
    lastsent = models.DateField(blank=True, null=True)
    no_of_email = models.IntegerField(blank=True, null=True)
    test_email = models.CharField(max_length=255, blank=True, null=True)
    test_email_status = models.CharField(max_length=20,choices=Mailing_Status_CHOICES, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    delivery_hour = models.CharField(max_length=255, blank=True, null=True)
    delivery_minute = models.CharField(max_length=255, blank=True, null=True)
    delivery_timetype = models.CharField(max_length=255, blank=True, null=True)
    delivery_status = models.CharField(max_length=20,choices=Delivery_Status_CHOICES, default='notsent',null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    delivery_date_time = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_emkt_campaigns'

class EngageboostEmktContactlists(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    company_website_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    fromname = models.CharField(max_length=255, blank=True, null=True)
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    reply_email = models.CharField(max_length=255, blank=True, null=True)
    default_subject = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email_subscribe = models.CharField(max_length=255, blank=True, null=True)
    people_subscribe = models.CharField(max_length=2,choices=enum_choices,default='n')
    people_unsubscribe = models.CharField(max_length=2,choices=enum_choices,default='n')
    usertype = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isdefault = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    owner_email = models.CharField(max_length=255, blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_emkt_contactlists'

class EngageboostEmktContacts(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    Email_Format_CHOICES = (
        ('HTML', 'HTML'),
        ('TEXT', 'TEXT'),
        ('HTML&TEXT', 'HTML&TEXT')
    )
    Activity_CHOICES = (
        ('active', 'active'),
        ('subscribed', 'subscribed'),
        ('unsubscribed', 'unsubscribed')
    )
    Confirmation_CHOICES = (
        ('confirm', 'confirm'),
        ('unconfirm', 'unconfirm')
    )
    Gender_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    contact_list = models.ForeignKey(EngageboostEmktContactlists,on_delete=models.CASCADE,blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    company_website_id = models.IntegerField(blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    list_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    email_format = models.CharField(max_length=20,choices=Email_Format_CHOICES,default='HTML')
    activity_status = models.CharField(max_length=20,choices=Activity_CHOICES,default='active')
    confirmation_status = models.CharField(max_length=20,choices=Confirmation_CHOICES,default='unconfirm')
    date_of_birth = models.CharField(max_length=50, blank=True, null=True)
    anniversary_date = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(EngageboostCountries,on_delete=models.CASCADE,blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    confirm_date = models.CharField(max_length=50, blank=True, null=True)
    confirm_ip = models.CharField(max_length=255, blank=True, null=True)
    edeal = models.CharField(max_length=20,choices=enum_choices,default='n')
    interest = models.CharField(max_length=20,choices=enum_choices,default='n')
    opt_in = models.CharField(max_length=20,choices=enum_choices,default='n', null=True)
    e_deal = models.CharField(max_length=20,choices=enum_choices,default='n', null=True)
    mail_flag = models.CharField(max_length=20,choices=enum_choices,default='n', null=True)
    bounce_check_flag = models.CharField(max_length=20,choices=enum_choices,default='n', null=True)
    feedback = models.TextField(blank=True, null=True)
    unsub_date = models.CharField(max_length=50, blank=True, null=True)
    email_campaign_id = models.IntegerField(default=0)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    unsubscribed_opt = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    subscribe_checkbox_val = models.CharField(max_length=255, blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_emkt_contacts'

class EngageboostEmktPageVisitStat(models.Model):
    campaign_id = models.IntegerField(blank=True, null=True)
    page_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    page_link = models.CharField(max_length=255, blank=True, null=True)
    page_url = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=255, blank=True, null=True)
    number_of_visit = models.IntegerField(blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_emkt_page_visit_stat'

class EngageboostEmktSegments(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    Match_Type_CHOICES = (
        ('AND', 'AND'),
        ('OR', 'OR')
    )
    company_website_id = models.IntegerField(blank=True, null=True)
    segment_name = models.CharField(max_length=255, blank=True, null=True)
    match_type = models.CharField(max_length=5,choices=Match_Type_CHOICES,default='AND')
    fields = models.TextField(blank=True, null=True)
    condition = models.TextField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    createdby = models.IntegerField(default='0')
    updatedby = models.IntegerField(default='0')
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_emkt_segments'

class EngageboostEmktSegmentContactlists(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    segment_contactlistname = models.CharField(max_length=255, blank=True, null=True)
    segment = models.ForeignKey(EngageboostEmktSegments,on_delete=models.CASCADE,blank=True, null=True,default=0)
    contact = models.ForeignKey(EngageboostEmktContacts,on_delete=models.CASCADE,blank=True, null=True,default=0)
    contactlist = models.ForeignKey(EngageboostEmktContactlists,on_delete=models.CASCADE,blank=True, null=True,default=0)
    createdby = models.IntegerField(default='0')
    updatedby = models.IntegerField(default='0')
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_emkt_segment_contactlists'

class EngageboostEmktSendmail(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    contact_id = models.IntegerField(blank=True, null=True)
    mail_sent = models.CharField(max_length=2,choices=enum_choices,default='n')
    mail_date_time = models.DateTimeField(blank=True, null=True)
    is_opened = models.IntegerField(blank=True, null=True)
    is_clicked = models.IntegerField(blank=True, null=True)
    is_bounced = models.IntegerField(blank=True, null=True)
    is_unsubscribe = models.IntegerField(blank=True, null=True)
    open_date_time = models.DateTimeField(blank=True, null=True)
    email_id = models.CharField(max_length=255,blank=True, null=True)
    campaign_id = models.IntegerField(blank=True, null=True)
    contactlist_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_emkt_sendmail'

class EngageboostEmktTemplateMasters(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    Type_CHOICES = (
        ('product', 'product'),
        ('generic', 'generic')
    )
    name = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    template_data = models.TextField(blank=True, null=True)
    templatecategory_id = models.IntegerField(blank=True, null=True)
    template_type = models.CharField(max_length=20,choices=Type_CHOICES,default='generic')
    bigimage = models.CharField(max_length=255, blank=True, null=True)
    smallimage = models.CharField(max_length=255, blank=True, null=True)
    folder = models.CharField(max_length=255, blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_emkt_template_masters'

class EngageboostEmktTemplatecategoryMasters(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    name = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_emkt_templatecategory_masters'

class EngageboostEmktWebsiteTemplates(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    Type_CHOICES = (
        ('product', 'product'),
        ('generic', 'generic'),
        ('invoice', 'invoice')
    )
    Size_CHOICES = (
        ('small', 'small'),
        ('medium', 'medium'),
        ('large', 'large')
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    templatecategory_id = models.IntegerField(blank=True, null=True)
    template_type = models.CharField(max_length=20,choices=Type_CHOICES,default='generic')
    template_data = models.TextField(blank=True, null=True)
    bigimage = models.CharField(max_length=255, blank=True, null=True)
    smallimage = models.CharField(max_length=255, blank=True, null=True)
    image_size = models.CharField(max_length=20,choices=Size_CHOICES,default='small')
    folder = models.CharField(max_length=255, blank=True, null=True)
    set_default_template = models.IntegerField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_emkt_website_templates'

class EngageboostFacebookProducts(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    page_id = models.BigIntegerField(blank=True, null=True)
    website_id = models.BigIntegerField(blank=True, null=True)
    product_id = models.BigIntegerField(blank=True, null=True)
    is_blocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    is_deleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    added_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_facebook_products'

class EngageboostFbPageProducts(models.Model):
    enum_choices = (
        ('0', '0'),
        ('1', '1')
    )
    page_id = models.BigIntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    website_url = models.CharField(max_length=222, blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=222, blank=True, null=True)
    ses_id = models.IntegerField(blank=True, null=True)
    is_added = models.CharField(max_length=2,choices=enum_choices,default='0')
    is_blocked = models.CharField(max_length=2,choices=enum_choices,default='0')
    is_deleted = models.CharField(max_length=2,choices=enum_choices,default='0')
    created_date = models.DateTimeField(blank=True, null=True)
    store_url = models.CharField(max_length=255, blank=True, null=True)
    store_name = models.CharField(max_length=255, blank=True, null=True)
    page_name = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_fb_page_products'

class EngageboostFbTempUserDetails(models.Model):
    company_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    fb_user_id = models.CharField(max_length=250, blank=True, null=True)
    fb_access_token = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_fb_temp_user_details'

class EngageboostFbaPlanProducts(models.Model):
    enum_choices = (
        ('Merchant', 'Merchant'),
        ('Amazon', 'Amazon')
    )
    shipping_plan_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    sku = models.CharField(max_length=11,blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    labeled_by = models.CharField(max_length=20,choices=enum_choices,default='Merchant')
    prep_by = models.CharField(max_length=20,choices=enum_choices,default='Merchant')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_fba_plan_products'

class EngageboostFbaShipmentProducts(models.Model):
    shipping_plan_id = models.IntegerField(blank=True, null=True)
    fba_shipment_id = models.CharField(max_length=250,blank=True, null=True)
    shipment_id = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    sku = models.CharField(max_length=250,blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    received_quantity = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_fba_shipment_products'

class EngageboostFbaShipments(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    shipping_plan_id = models.IntegerField(blank=True, null=True)
    shipment_id = models.CharField(max_length=100, blank=True, null=True)
    shipment_name = models.CharField(max_length=250, blank=True, null=True)
    msku = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    shipment_type = models.CharField(max_length=100, blank=True, null=True)
    shipping_service_type = models.CharField(max_length=250, blank=True, null=True)
    shipping_service_code = models.CharField(max_length=250, blank=True, null=True)
    shipping_tracking_code = models.CharField(max_length=255, blank=True, null=True)
    transport_status = models.CharField(max_length=250, blank=True, null=True)
    shipment_packing = models.CharField(max_length=250, blank=True, null=True)
    shipment_label = models.CharField(max_length=250, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    is_blocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    is_deleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_fba_shipments'

class EngageboostFbaShippingBoxes(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    shipment_id = models.IntegerField(blank=True, null=True)
    amazon_shipment_id = models.CharField(max_length=100, blank=True, null=True)
    tracking_id = models.CharField(max_length=250, blank=True, null=True)
    box_weight = models.IntegerField(blank=True, null=True)
    box_length = models.IntegerField(blank=True, null=True)
    box_width = models.IntegerField(blank=True, null=True)
    box_height = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    is_blocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    is_deleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_fba_shipping_boxes'

class EngageboostFbaShippingPlanFeedSubmissions(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    shipping_plan_id = models.IntegerField(blank=True, null=True)
    feed_submission_id = models.BigIntegerField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    is_called = models.CharField(max_length=2,choices=enum_choices,default='n')
    feed_type = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    report_id = models.BigIntegerField(blank=True, null=True)
    report_call_status = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    class Meta:
        db_table = 'engageboost_fba_shipping_plan_feed_submissions'

class EngageboostFbaShippingServices(models.Model):
    shipping_service_name = models.CharField(max_length=255, blank=True, null=True)
    shipping_service_code = models.CharField(max_length=255, blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    service_type = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_fba_shipping_services'

class EngageboostFbaShippingplans(models.Model):
    enum_choices = (
        ('inprocess', 'inprocess'),
        ('success', 'success'),
        ('error', 'error'),
        ('working', 'working')
    )
    website_id = models.IntegerField(blank=True, null=True)
    plan_name = models.CharField(max_length=250,blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    plan_id = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=20,choices=enum_choices,default='inprocess', null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_fba_shippingplans'

class EngageboostFbaSteps(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    step_url = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_fba_steps'

class EngageboostFedexZipcodes(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    pincode = models.CharField(max_length=255,blank=True, null=True)
    prepaid = models.CharField(max_length=2,choices=enum_choices,default='n')
    cod = models.CharField(max_length=2,choices=enum_choices,default='n')
    city_name = models.CharField(max_length=255,blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    state_name = models.CharField(max_length=255, blank=True, null=True)
    cod_capability = models.CharField(max_length=255,blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_fedex_zipcodes'

class EngageboostFeeMasters(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    Applicable_CHOICES = (
        ('shipping', 'shipping'),
        ('transaction', 'transaction')
    )
    Fee_CHOICES = (
        ('range', 'range'),
        ('fixed', 'fixed')
    )
    fee_name = models.CharField(max_length=255, blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    fee_applicable_for = models.CharField(max_length=20,choices=Applicable_CHOICES,default='shipping')
    fee_based_on = models.CharField(max_length=20,choices=Fee_CHOICES,default='range')
    fee_for = models.CharField(max_length=50, blank=True, null=True)
    payment_type = models.CharField(max_length=255, blank=True, null=True)
    account_type_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_fee_masters'

class EngageboostFeeSettingMasters(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    Fee_CHOICES = (
        ('F', 'F'),
        ('P', 'P')
    )
    fee_master_id = models.IntegerField(blank=True, null=True)
    slab_name = models.CharField(max_length=500, blank=True, null=True)
    slab_start = models.FloatField(blank=True, null=True)
    slab_end = models.FloatField(blank=True, null=True)
    interval_range = models.FloatField(blank=True, null=True)
    uom = models.CharField(max_length=100, blank=True, null=True)
    shipping_local = models.IntegerField(blank=True, null=True)
    shipping_zonal = models.IntegerField(blank=True, null=True)
    shipping_national = models.IntegerField(blank=True, null=True)
    shipping_international = models.IntegerField(blank=True, null=True)
    slab_value = models.IntegerField(blank=True, null=True)
    fee_type = models.CharField(max_length=2,choices=Fee_CHOICES,default='F')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_fee_setting_masters'

class EngageboostFlipkartOrderTransactions(models.Model):
    order_id = models.IntegerField(blank=True, null=True)
    flipkart_order_id = models.CharField(max_length=255, blank=True, null=True)
    orderitemid = models.BigIntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    orderdate = models.DateTimeField(blank=True, null=True)
    sla = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    listingid = models.CharField(max_length=255, blank=True, null=True)
    fsn = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    sellingprice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    customerprice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shippingcharge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    totalprice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dispatchafterdate = models.DateTimeField(blank=True, null=True)
    dispatchbydate = models.DateTimeField(blank=True, null=True)
    deliverbydate = models.DateTimeField(blank=True, null=True)
    updatedat = models.DateTimeField(blank=True, null=True)
    paymenttype = models.CharField(max_length=100, blank=True, null=True)
    shipmentid = models.CharField(max_length=100, blank=True, null=True)
    shipmenttype = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_flipkart_order_transactions'

class EngageboostFlipkartReconciliations(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    channel_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    reconciliation_file_id = models.IntegerField(blank=True, null=True)
    boost_order_id = models.IntegerField(blank=True, null=True)
    flipkart_txn_id = models.IntegerField(blank=True, null=True)
    boost_order_product_id = models.IntegerField(blank=True, null=True)
    sheet_settlement_ref_no = models.CharField(max_length=255, blank=True, null=True)
    sheet_order_type = models.CharField(max_length=100, blank=True, null=True)
    sheet_fulfilment_type = models.CharField(max_length=100, blank=True, null=True)
    sheet_seller_sku = models.CharField(max_length=255, blank=True, null=True)
    sheet_wsn = models.CharField(max_length=255, blank=True, null=True)
    sheet_order_id_fsn = models.CharField(max_length=255, blank=True, null=True)
    sheet_order_item_id = models.CharField(max_length=100, blank=True, null=True)
    sheet_order_date = models.DateTimeField(blank=True, null=True)
    sheet_dispatch_date = models.DateTimeField(blank=True, null=True)
    sheet_delivery_date = models.DateTimeField(blank=True, null=True)
    sheet_cancellation_date = models.DateTimeField(blank=True, null=True)
    sheet_settlement_date = models.DateTimeField(blank=True, null=True)
    sheet_order_status = models.CharField(max_length=100, blank=True, null=True)
    sheet_quantity = models.IntegerField(blank=True, null=True)
    sheet_order_item_value = models.FloatField(blank=True, null=True)
    sheet_sale_transaction_amount = models.FloatField(blank=True, null=True)
    sheet_discount_transaction_amount = models.FloatField(blank=True, null=True)
    sheet_refund = models.FloatField(blank=True, null=True)
    sheet_protection_fund = models.FloatField(blank=True, null=True)
    sheet_total_marketplace_fee = models.FloatField(blank=True, null=True)
    sheet_service_tax = models.FloatField(blank=True, null=True)
    sheet_sb_cess_tax = models.FloatField(blank=True, null=True)
    sheet_kk_cess_tax = models.FloatField(blank=True, null=True)
    sheet_settlement_value = models.FloatField(blank=True, null=True)
    sheet_commission_rate = models.FloatField(blank=True, null=True)
    sheet_commission = models.FloatField(blank=True, null=True)
    sheet_payment_rate = models.FloatField(blank=True, null=True)
    sheet_payment_fee = models.FloatField(blank=True, null=True)
    sheet_fee_discount = models.FloatField(blank=True, null=True)
    sheet_cancellation_fee = models.FloatField(blank=True, null=True)
    sheet_fixed_fee = models.FloatField(blank=True, null=True)
    sheet_admonetaisation_fee = models.FloatField(blank=True, null=True)
    sheet_dead_weight = models.FloatField(blank=True, null=True)
    sheet_chargeable_wt_slab = models.FloatField(blank=True, null=True)
    sheet_chargeable_weight_type = models.CharField(max_length=100, blank=True, null=True)
    sheet_lenght_breadth_height = models.CharField(max_length=100, blank=True, null=True)
    sheet_volumetric_weight_in_kg = models.FloatField(blank=True, null=True)
    sheet_shipping_fee = models.FloatField(blank=True, null=True)
    sheet_reverse_shipping_fee = models.FloatField(blank=True, null=True)
    sheet_shipping_fee_reversal = models.FloatField(blank=True, null=True)
    sheet_shipping_zone = models.CharField(max_length=100, blank=True, null=True)
    sheet_token_of_apology = models.FloatField(blank=True, null=True)
    sheet_pick_and_pack_fee = models.FloatField(blank=True, null=True)
    sheet_storage_fee = models.FloatField(blank=True, null=True)
    sheet_removal_fee = models.FloatField(blank=True, null=True)
    sheet_invoice_id = models.CharField(max_length=255, blank=True, null=True)
    sheet_invoice_date = models.DateTimeField(blank=True, null=True)
    sheet_invoice_amount = models.FloatField(blank=True, null=True)
    sheet_sub_category = models.CharField(max_length=255, blank=True, null=True)
    sheet_total_offer_amount = models.FloatField(blank=True, null=True)
    sheet_my_offer_share = models.FloatField(blank=True, null=True)
    sheet_flipkart_offer_share = models.FloatField(blank=True, null=True)
    sheet_service_cancellation_fee = models.FloatField(blank=True, null=True)
    sheet_ndd_amount = models.FloatField(blank=True, null=True)
    sheet_ndd_fee = models.FloatField(blank=True, null=True)
    sheet_sdd_amount = models.FloatField(blank=True, null=True)
    sheet_sdd_fee = models.FloatField(blank=True, null=True)
    sheet_sellable_regular_storage_fee = models.FloatField(blank=True, null=True)
    sheet_unsellable_regular_storage_fee = models.FloatField(blank=True, null=True)
    sheet_sellable_long_term_1_storage_fee = models.FloatField(blank=True, null=True)
    sheet_unsellable_longterm_1_storage_fee = models.FloatField(blank=True, null=True)
    sheet_unsellable_longterm_2_storage_fee = models.FloatField(blank=True, null=True)
    sheet_is_replacement = models.CharField(max_length=100, blank=True, null=True)
    sheet_multi_product = models.CharField(max_length=100, blank=True, null=True)
    sheet_profiler_dead_weight = models.FloatField(blank=True, null=True)
    sheet_seller_dead_weight = models.FloatField(blank=True, null=True)
    sheet_customer_shipping_amount = models.FloatField(blank=True, null=True)
    sheet_customer_shipping_fee = models.FloatField(blank=True, null=True)
    sheet_payment_mode_changed = models.CharField(max_length=100, blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_flipkart_reconciliations'

class EngageboostFormulaDetails(models.Model):
    enum_choices = (
        ('LCOST', 'LCOST'),
        ('ACOST', 'ACOST')
    )
    formula_name_id = models.BigIntegerField(blank=True, null=True)
    w = models.CharField(max_length=20,choices=enum_choices,default='LCOST')
    x = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    y = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    z = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    r = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_formula_details'

class EngageboostFulfillments(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    address_one = models.CharField(max_length=255, blank=True, null=True)
    address_two = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    role_id = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    phone_two = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    class Meta:
        db_table = 'engageboost_fulfillments'

class EngageboostGlobalSettings(models.Model):
    status_type_block = (
        ('y', 'y'),
        ('n', 'n')
    )
    status_CHOICES = (
        ('Y', 'Y'),
        ('N', 'N')
    )
    order_auto_approval = (
        ('yes', 'yes'),
        ('no', 'no')
    )
    order_auto_approval1 = (
        ('yes', 'yes'),
        ('no', 'no')
    )
    drop_shipment_type = (
        ('Manual', 'Manual'),
        ('Automated', 'Automated')
    )
    drop_shipment_based_on = (
        ('Product', 'Product'),
        ('Shipping', 'Shipping'),
        ('Address', 'Address'),
        ('Marketplace', 'Marketplace')
    )
    order_prefix_type = (
        ('Unique', 'Unique'),
        ('Warehouse', 'Warehouse')
    )
    label_invoice_order = (
        ('Invoice', 'Invoice'),
        ('Shippinglabel', 'Shippinglabel')
    )
    applicable_tax_choice = (
        ('GST', 'GST'),
        ('VAT', 'VAT')
    )
    website_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_format = models.CharField(max_length=255, blank=True, null=True)
    image_resize = models.CharField(max_length=255, blank=True, null=True)
    timezone_id = models.BigIntegerField(blank=True, null=True)
    orderid_format = models.CharField(max_length=255, blank=True, null=True)
    orderconfirmemailid = models.TextField(blank=True, null=True)
    invoice_id_format = models.CharField(max_length=255, blank=True, null=True)
    shipping_id_format = models.CharField(max_length=255,blank=True, null=True)
    purchase_order_id_format = models.CharField(max_length=255, blank=True, null=True)
    receiptid_format = models.CharField(max_length=255, blank=True, null=True)
    shipping_charge = models.FloatField(blank=True, null=True)
    google_analytics = models.TextField(blank=True, null=True)
    google_analytics_profileid = models.CharField(max_length=255, blank=True, null=True)
    google_analytics_email = models.CharField(max_length=255, blank=True, null=True)
    google_analytics_password = models.CharField(max_length=255, blank=True, null=True)
    google_login_devoloper_key = models.TextField(blank=True, null=True)
    sku_prefix = models.CharField(max_length=255, blank=True, null=True)
    sku_suffix = models.CharField(max_length=255, blank=True, null=True)
    weight_unit = models.CharField(max_length=50, blank=True, null=True)
    itemlisting_front = models.IntegerField(blank=True, null=True)
    itemlisting_backend = models.IntegerField(blank=True, null=True)
    page_title = models.CharField(max_length=255, blank=True, null=True)
    meta_keyword = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    fb_store_app_id = models.TextField(blank=True, null=True)
    fb_store_secret = models.TextField(blank=True, null=True)
    fb_login_id = models.TextField(blank=True, null=True)
    fb_login_secret = models.TextField(blank=True, null=True)
    google_application_name = models.TextField(blank=True, null=True)
    google_login_client_id = models.TextField(blank=True, null=True)
    google_login_client_secret = models.TextField(blank=True, null=True)
    google_login_redirect_url = models.TextField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=status_type_block,default='n')
    isdeleted = models.CharField(max_length=2,choices=status_type_block,default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    is_ebay_store_on = models.CharField(max_length=2,choices=status_CHOICES,default='N')
    is_global_shipping_app = models.IntegerField(blank=True, null=True)
    review_moderation = models.CharField(max_length=2,choices=status_type_block,default='n')
    is_prepaid_payment = models.CharField(max_length=2,choices=status_type_block,default='n')
    min_prepayment = models.FloatField(blank=True, null=True)
    max_prepayment = models.FloatField(blank=True, null=True)
    prepay_percent = models.IntegerField(blank=True, null=True)
    order_auto_approval = models.CharField(max_length=255,choices=order_auto_approval,default='no')
    drop_shipment_type = models.CharField(max_length=255,choices=drop_shipment_type,default='Manual')
    drop_shipment_based_on = models.CharField(max_length=255,choices=drop_shipment_based_on, null=True)
    order_prefix_type = models.CharField(max_length=255,choices=order_prefix_type,default='Unique')
    new_arrival_days = models.IntegerField(blank=True, null=True)
    min_order_amount = models.IntegerField(blank=True,null=True)
    sms_check = models.CharField(max_length=2,choices=status_CHOICES,default='Y')
    sms_sender_id = models.CharField(max_length=50, blank=True, null=True)
    sms_auth_key = models.CharField(max_length=255, blank=True, null=True)
    sms_route = models.IntegerField(blank=True, null=True)
    google_analytics2 = models.TextField(blank=True, null=True)
    smtp_server = models.CharField(max_length=100, blank=True, null=True)
    smtp_port = models.IntegerField(blank=True, null=True)
    smtp_username = models.CharField(max_length=100, blank=True, null=True)
    smtp_password = models.CharField(max_length=100, blank=True, null=True)
    mail_sent_from = models.CharField(max_length=100, blank=True, null=True)
    mail_reply_to = models.CharField(max_length=100, blank=True, null=True)
    service_applicable = models.CharField(max_length=255,choices=order_auto_approval1,default='no')
    order_ship_in_days = models.IntegerField(blank=True, null=True)
    marketplace_order_process = models.CharField(max_length=2,choices=status_CHOICES,default='Y')
    applicable_imei = models.CharField(max_length=2,choices=status_CHOICES,default='Y')
    isgrn_exist = models.CharField(max_length=2,choices=status_CHOICES,default='N')
    label_invoice_order = models.CharField(max_length=255,choices=label_invoice_order)
    product_sla = models.IntegerField(blank=True, null=True)
    return_completion_days = models.IntegerField(blank=True, null=True)
    applicable_for_guest = models.CharField(max_length=50, blank=True, null=True)
    automatic_approve = models.CharField(max_length=50, blank=True, null=True)
    enable_cancel = models.CharField(max_length=50, blank=True, null=True)
    enable_print_label = models.CharField(max_length=50, blank=True, null=True)
    enable_reason = models.CharField(max_length=50, blank=True, null=True)
    enable_other_option = models.CharField(max_length=50, blank=True, null=True)
    enable_per_order_item = models.CharField(max_length=50, blank=True, null=True)
    enable_confirm_shipping = models.CharField(max_length=50, blank=True, null=True)
    algolia_search_status = models.CharField(max_length=2, blank=True, null=True)
    algolia_app_key = models.CharField(max_length=100, blank=True, null=True)
    algolia_app_token = models.CharField(max_length=100, blank=True, null=True)
    index_name = models.CharField(max_length=100, blank=True, null=True)
    is_review_grant_exist = models.CharField(max_length=2,choices=status_CHOICES,default='N')
    applicable_tax = models.CharField(max_length=10,choices=applicable_tax_choice, null=True)
    no_of_item_picklist = models.IntegerField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_global_settings'

class EngageboostAdditionalGlobalsettings(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    settings_key = models.TextField(blank=True, null=True)
    settings_value = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    class Meta:
        db_table = 'engageboost_additional_global_settings'

class EngageboostGlobalsettingCountries(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    global_setting_id = models.BigIntegerField(blank=True, null=True)
    country_id = models.BigIntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    class Meta:
        db_table = 'engageboost_globalsetting_countries'

class EngageboostGlobalsettingCurrencies(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    global_setting_id = models.BigIntegerField(blank=True, null=True)
    currency_id = models.BigIntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    class Meta:
        db_table = 'engageboost_globalsetting_currencies'

class EngageboostGlobalsettingLanguages(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    global_setting_id = models.BigIntegerField(blank=True, null=True)
    language_id = models.BigIntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    class Meta:
        db_table = 'engageboost_globalsetting_languages'

class EngageboostGlobalsettingSitemodules(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    global_setting_id = models.BigIntegerField(blank=True, null=True)
    sitemodule_id = models.BigIntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    class Meta:
        db_table = 'engageboost_globalsetting_sitemodules'

class EngageboostGooglecheckoutReturnDetails(models.Model):
    contents = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    order_id = models.TextField(blank=True, null=True)
    buyer_email = models.TextField(blank=True, null=True)
    buyer_contact_name = models.TextField(blank=True, null=True)
    buyer_company_name = models.TextField(blank=True, null=True)
    buyer_billing_address1 = models.TextField(blank=True, null=True)
    buyer_billing_phone = models.TextField(blank=True, null=True)
    buyer_billing_fax = models.TextField(blank=True, null=True)
    buyer_billing_country_code = models.TextField(blank=True, null=True)
    buyer_billing_city = models.TextField(blank=True, null=True)
    buyer_billing_region = models.TextField(blank=True, null=True)
    buyer_billing_postal_code = models.TextField(blank=True, null=True)
    timestamp = models.TextField(blank=True, null=True)
    google_order_number = models.TextField(blank=True, null=True)
    buyer_shipping_email = models.TextField(blank=True, null=True)
    buyer_shipping_contact_name = models.TextField(blank=True, null=True)
    buyer_shipping_company_name = models.TextField(blank=True, null=True)
    buyer_shipping_address1 = models.TextField(blank=True, null=True)
    buyer_shipping_address2 = models.TextField(blank=True, null=True)
    buyer_shipping_phone = models.TextField(blank=True, null=True)
    buyer_shipping_fax = models.TextField(blank=True, null=True)
    buyer_shipping_country_code = models.TextField(blank=True, null=True)
    buyer_shipping_city = models.TextField(blank=True, null=True)
    buyer_shipping_region = models.TextField(blank=True, null=True)
    buyer_shipping_postal_codel = models.TextField(blank=True, null=True)
    buyer_marketing_preferences_email = models.TextField(blank=True, null=True)
    order_total = models.TextField(blank=True, null=True)
    fulfillment_order_state = models.TextField(blank=True, null=True)
    financial_order_state = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_googlecheckout_return_details'

class EngageboostGoogleshopCategories(models.Model):
    code = models.IntegerField(blank=True, null=True)
    parent = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=255,blank=True, null=True)
    taxonomy = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_googleshop_categories'

class EngageboostGridLayouts(models.Model):
    enum_choices = (
        ('n', 'n'),
        ('y', 'y')
    )
    website_id = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    module = models.CharField(max_length=100, blank=True, null=True)
    screen_name = models.CharField(max_length=100, blank=True, null=True)
    header_name = models.TextField(blank=True, null=True)
    header_classname = models.TextField(blank=True, null=True)
    field_name = models.TextField(blank=True, null=True)
    folder_name = models.CharField(max_length=100, blank=True, null=True)
    module_name = models.CharField(max_length=150, blank=True, null=True)
    add_edit_url_popup = models.CharField(max_length=10, blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_grid_layouts'

class EngageboostGridColumnLayouts(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    module = models.CharField(max_length=100, blank=True, null=True)
    screen_name = models.CharField(max_length=100, blank=True, null=True)
    columns = models.TextField(blank=True, null=True)
    header_name = models.TextField(blank=True, null=True)
    header_classname = models.TextField(blank=True, null=True)
    field_name = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted = models.CharField(max_length=255,choices=enum_choices,default='n',blank=True, null=True)
    createdby = models.IntegerField(default='0', blank=True, null=True)
    updatedby = models.IntegerField(default='0', blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_grid_column_layouts'

class EngageboostAdvancedSearchLayouts(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    field_type_choices = (
        ('string', 'string'),
        ('int', 'int')
    )
    input_type_choices = (
        ('text', 'text'),
        ('select', 'select'),
        ('radio', 'radio'),
        ('checkbox', 'checkbox')

    )
    module_id = models.IntegerField(blank=True, null=True)
    columns = models.TextField(blank=True, null=True)
    field = models.TextField(blank=True, null=True)
    field_type = models.CharField(max_length=20,choices=field_type_choices,default='int',blank=True, null=True)
    input_type = models.CharField(max_length=20,choices=field_type_choices,default='text',blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    search_module = models.CharField(max_length=100, blank=True, null=True)
    title_field_name = models.CharField(max_length=100, blank=True, null=True)
    value_field_name = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    createdby = models.IntegerField(default='0', blank=True, null=True)
    updatedby = models.IntegerField(default='0', blank=True, null=True)
    class Meta:
        db_table = 'engageboost_advanced_search_layouts'

class EngageboostAdvancedSearchModules(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    search_type_choices = (
        ('e', 'Elastic'),
        ('d', 'Database')
    )
    field_type_choices = (
        ('string', 'string'),
        ('int', 'int')
    )
    website_id = models.IntegerField(blank=True, null=True)
    module = models.CharField(max_length=100, blank=True, null=True)
    screen_name = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    search_type = models.CharField(max_length=2,choices=search_type_choices,default='d',blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    createdby = models.IntegerField(default='0', blank=True, null=True)
    updatedby = models.IntegerField(default='0', blank=True, null=True)
    class Meta:
        db_table = 'engageboost_advanced_search_modules'

class EngageboostGroups(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    company_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=250,blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    masters = models.TextField(blank=True, null=True)
    website_id = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    createdby = models.IntegerField(default='0', blank=True, null=True)
    updatedby = models.IntegerField(default='0', blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    language_id = models.IntegerField(default='0')
    warehouse_id = models.IntegerField(blank=True, null=True, default='0')
    class Meta:
        db_table = 'engageboost_groups'

class EngageboostHdfcReturnDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    res_result = models.CharField(max_length=255, blank=True, null=True)
    txntrackid = models.CharField(max_length=255, blank=True, null=True)
    txnpaymentid = models.CharField(max_length=255, blank=True, null=True)
    txnref = models.CharField(max_length=255, blank=True, null=True)
    txntranid = models.CharField(max_length=255, blank=True, null=True)
    txnamount = models.CharField(max_length=255, blank=True, null=True)
    txnerror = models.CharField(max_length=255, blank=True, null=True)
    tr_date = models.DateTimeField(blank=True, null=True)
    paypageurl = models.TextField(blank=True, null=True)
    auth_code = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_hdfc_return_details'

class EngageboostIciciReturnDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    responsecode = models.CharField(max_length=20, blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    txnid = models.CharField(max_length=255, blank=True, null=True)
    epgtxnid = models.CharField(max_length=255, blank=True, null=True)
    authidcode = models.CharField(max_length=255, blank=True, null=True)
    rrn = models.CharField(max_length=255, blank=True, null=True)
    cvrespcode = models.CharField(max_length=255, blank=True, null=True)
    orderstatus = models.CharField(max_length=255, blank=True, null=True)
    reserve1 = models.CharField(max_length=255, blank=True, null=True)
    reserve2 = models.CharField(max_length=255, blank=True, null=True)
    reserve3 = models.CharField(max_length=255, blank=True, null=True)
    reserve4 = models.CharField(max_length=255, blank=True, null=True)
    reserve5 = models.CharField(max_length=255, blank=True, null=True)
    reserve6 = models.CharField(max_length=255, blank=True, null=True)
    reserve7 = models.CharField(max_length=255, blank=True, null=True)
    reserve8 = models.CharField(max_length=255, blank=True, null=True)
    reserve9 = models.CharField(max_length=255, blank=True, null=True)
    reserve10 = models.CharField(max_length=255, blank=True, null=True)
    dccfees = models.CharField(max_length=255, blank=True, null=True)
    dccmargins = models.CharField(max_length=255, blank=True, null=True)
    dcccommission = models.CharField(max_length=255, blank=True, null=True)
    dccbasecurrencyamt = models.CharField(max_length=255, blank=True, null=True)
    dcccardcurrencyamt = models.CharField(max_length=255, blank=True, null=True)
    dccuseraccepted = models.CharField(max_length=255, blank=True, null=True)
    dccsrcname = models.CharField(max_length=255, blank=True, null=True)
    dccexchangerate = models.CharField(max_length=255, blank=True, null=True)
    dcccurrency = models.CharField(max_length=255, blank=True, null=True)
    curralphacode = models.CharField(max_length=255, blank=True, null=True)
    tdate = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_icici_return_details'

class EngageboostHelpText(models.Model):
    page_id = models.IntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_help_text'

class EngageboostHolidaysMasters(models.Model):
    holidays_name = models.CharField(max_length=255, blank=True, null=True)
    holiday_date = models.DateTimeField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    is_openon_holidays = models.SmallIntegerField(blank=True, null=True)
    isblocked = models.SmallIntegerField(blank=True, null=True)
    isdeleted = models.SmallIntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_holidays_masters'

class EngageboostImportErrorLog(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    file_path = models.CharField(max_length=255,blank=True, null=True)
    class Meta:
        db_table = 'engageboost_import_error_log'

class EngageboostImportMapFields(models.Model):
    file_field_name = models.TextField(blank=True, null=True)
    db_label_name = models.TextField(blank=True, null=True)
    db_field_name = models.TextField(blank=True, null=True)
    map_field_name = models.TextField(blank=True, null=True)
    module_layout_field_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    module_id = models.IntegerField(blank=True, null=True)
    module_list_id = models.IntegerField(blank=True, null=True)
    file_type = models.TextField(blank=True, null=True)
    file_name = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_import_map_fields'

class EngageboostImportStockFiles(models.Model):
    stock_import = (
        ('Update', 'Update'),
        ('Append', 'Append')
    )
    imported_status_type = (
        ('Y', 'Y'),
        ('N', 'N')
    )
    company_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    original_file_name = models.CharField(max_length=100, blank=True, null=True)
    file_type = models.CharField(max_length=10, blank=True, null=True)
    stock_import_type = models.CharField(max_length=255,choices=stock_import,default='Update')
    imported_on = models.DateTimeField(blank=True, null=True)
    imported_status = models.CharField(max_length=255,choices=imported_status_type,default='N')
    live_stock_updated = models.CharField(max_length=255,choices=imported_status_type,default='N')
    queue_no = models.IntegerField(blank=True, null=True)
    total_sku = models.IntegerField(blank=True, null=True)
    total_success_sku = models.IntegerField(blank=True, null=True)
    total_error_sku = models.IntegerField(blank=True, null=True)
    is_blocked = models.CharField(max_length=255,choices=imported_status_type,default='N')
    is_deleted = models.CharField(max_length=255,choices=imported_status_type,default='N')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_import_stock_files'

class EngageboostImportedTempProductStocks(models.Model):
    is_imported_stock = (
        ('Y', 'Y'),
        ('N', 'N')
    )
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    warehouse_name = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    lot_number = models.IntegerField(blank=True, null=True)
    rack_number = models.IntegerField(blank=True, null=True)
    safety_stock = models.IntegerField(blank=True, null=True)
    stock_file_imorted_id = models.IntegerField(blank=True, null=True)
    error_log = models.CharField(max_length=255,blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    # is_imported = models.CharField(max_length=255,choices=is_imported_stock)
    is_imported = models.IntegerField(blank=True, null=True, default=0)
    imported_on = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=255,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=255,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_imported_temp_product_stocks'

class EngageboostInventoryMasters(models.Model):
    status_filed = (
        ('y', 'y'),
        ('n', 'n')
    )
    parent_id = models.IntegerField(blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    createdby = models.CharField(max_length=255,blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=status_filed,default='n')
    isblocked = models.CharField(max_length=2,choices=status_filed,default='n')
    class Meta:
        db_table = 'engageboost_inventory_masters'

class EngageboostInventoryProducts(models.Model):
    status_filed = (
        ('y', 'y'),
        ('n', 'n')
    )
    inventory_id = models.BigIntegerField(blank=True, null=True)
    product_id = models.BigIntegerField(blank=True, null=True)
    sku = models.CharField(max_length=255,blank=True, null=True)
    createdby = models.CharField(max_length=255,blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=status_filed,default='n')
    isblocked = models.CharField(max_length=2,choices=status_filed,default='n')
    class Meta:
        db_table = 'engageboost_inventory_products'

class EngageboostInvoiceContainers(models.Model):
    order_id = models.IntegerField(blank=True, null=True)
    shipped_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    container_no = models.CharField(max_length=255, blank=True, null=True)
    no_pkgs = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_invoice_containers'

class EngageboostInvoicemaster(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    order = models.ForeignKey(EngageboostOrdermaster,on_delete=models.CASCADE,blank=True, null=True, related_name="invoice_order")
    custom_order_id = models.CharField(max_length=70,blank=True, null=True)
    custom_invoice_id = models.CharField(max_length=255, blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    webshop_id = models.IntegerField(blank=True, null=True)
    shipping_method_id = models.CharField(max_length=50, blank=True, null=True)
    excise_duty = models.FloatField(blank=True, null=True)
    gross_amount = models.FloatField(blank=True, null=True)
    net_amount = models.FloatField(blank=True, null=True)
    paid_amount = models.FloatField(blank=True, null=True)
    shipment_id = models.IntegerField(blank=True, null=True, default=0)
    trent_picklist_id = models.IntegerField(blank=True, null=True, default=0)
    gst_invoice_no = models.CharField(max_length=255, blank=True, null=True)
    exempted_gst_invoice_no = models.CharField(max_length=255, blank=True, null=True)
    gst_shipping_invoice_no = models.CharField(max_length=255, blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_invoicemaster'

class EngageboostInvoiceProducts(models.Model):
    invoice = models.ForeignKey(EngageboostInvoicemaster,on_delete=models.CASCADE,related_name='invoice_order_products',blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_invoice_products'

class EngageboostMenuMasters(models.Model):
    curd = (
        ('0', '0'),
        ('1', '1'),
    )
    type_CHOICES = (
        ('F', 'F'),
        ('A', 'A')
    )
    name = models.CharField(max_length=250, blank=True, null=True)
    alt_name = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=250, blank=True, null=True)
    module = models.CharField(max_length=100, blank=True, null=True)
    css_class = models.CharField(max_length=255, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    orders = models.IntegerField(blank=True, null=True)
    all_action = models.CharField(max_length=2,choices=curd,default='0')
    add_action = models.CharField(max_length=2,choices=curd,default='0')
    edit_action = models.CharField(max_length=2,choices=curd,default='0')
    delete_action = models.CharField(max_length=2,choices=curd,default='0')
    view_action = models.CharField(max_length=2,choices=curd,default='0')
    block_action = models.CharField(max_length=2,choices=curd,default='0')
    import_action = models.CharField(max_length=2,choices=curd,default='0')
    export_action = models.CharField(max_length=2,choices=curd,default='0')
    shipping_processes = models.TextField(max_length=2,choices=curd,default='0')
    print = models.CharField(max_length=2,choices=curd,default='0')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=curd,default='0')
    isdeleted = models.CharField(max_length=2,choices=curd,default='0')
    menu_type = models.CharField(max_length=255,choices=type_CHOICES,default='F')
    class Meta:
        db_table = 'engageboost_menu_masters'

class EngageboostMenuShortcuts(models.Model):
    enum_choices = (
        ('n', 'n'),
        ('y', 'y')
    )
    name = models.CharField(max_length=250, blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    parent_menu_id = models.IntegerField(blank=True, null=True)
    order_by = models.IntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_menu_shortcuts'

class EngageboostLanguages(models.Model):
    status_filed = (
        ('y', 'y'),
        ('n', 'n')
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    lang_code 	= models.CharField(max_length=20, blank=True, null=True)
    image_small = models.CharField(max_length=255, blank=True, null=True)
    image_big = models.CharField(max_length=255, blank=True, null=True)
    isblocked = models.CharField(max_length=255,choices=status_filed,default='n')
    isdeleted = models.CharField(max_length=255,choices=status_filed,default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_languages'

class EngageboostManifests(models.Model):
    curd = (
        ('y', 'n'),
        ('y', 'n'),
    )
    manifest_no = models.CharField(max_length=100,blank=True, null=True)
    manifest_to = models.CharField(max_length=100,blank=True, null=True)
    shipping_provider = models.CharField(max_length=100,blank=True, null=True)
    shipping_method_id = models.SmallIntegerField(blank=True, null=True)
    shipping_service = models.CharField(max_length=100,blank=True, null=True)
    shipment_id = models.IntegerField(blank=True, null=True)
    order_id = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=curd,default='n')
    isdeleted = models.CharField(max_length=2,choices=curd,default='n')
    class Meta:
        db_table = 'engageboost_manifests'

class EngageboostModuleLayouts(models.Model):
    layout_name = models.CharField(max_length=50,blank=True, null=True)
    module_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    module_name = models.CharField(max_length=30,blank=True, null=True)
    description = models.CharField(max_length=200,blank=True, null=True)
    owner_id = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked = models.SmallIntegerField(blank=True, null=True)
    isdeleted = models.SmallIntegerField(blank=True, null=True)
    is_default = models.SmallIntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_module_layouts'

class EngageboostModules(models.Model):
    status = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3')

    )
    module_name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    related_id = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=2,choices=status, null=True)
    class_name = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_modules'

class EngageboostJwelleryAppSettings(models.Model):
    status_filed = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.BigIntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    gold_18kt = models.FloatField(blank=True, null=True)
    gold_14kt = models.FloatField(blank=True, null=True)
    diamond_si_ij = models.FloatField(blank=True, null=True)
    diamond_si_gh = models.FloatField(blank=True, null=True)
    diamond_vs_fg = models.FloatField(blank=True, null=True)
    diamond_vss_ef = models.FloatField(blank=True, null=True)
    making_charges = models.FloatField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=status_filed,default='n')
    isblocked = models.CharField(max_length=2,choices=status_filed,default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_jwellery_app_settings'

class EngageboostCreditPoint(models.Model):
    status_filed = (
        ('y', 'y'),
        ('n', 'n')
    )
    disc_choices = (
        ('fixed', 'Fixed'),
        ('percentage', 'Percentage')
    )
    redeem_choices = (
        ('loyalty', 'Loyalty'),
        ('order', 'Order')
    )
    redeem_amount_choices = (
        ('fixed', 'Fixed'),
        ('percentage', 'Percentage')
    )
    disc_master_choices = (
        ('earn', 'Earn'),
        ('burn', 'Burn')
    )
    website_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied_as = models.CharField(max_length=20,choices=disc_choices,default='fixed',blank=True, null=True)
    loyalty_desc = models.TextField(blank=True, null=True)
    points = models.FloatField(blank=True, null=True)
    per_rupees = models.FloatField(blank=True, null=True)
    loyal_type = models.CharField(max_length=20,choices=disc_master_choices,default='earn',blank=True, null=True)
    loyal_start_date = models.DateTimeField(blank=True, null=True)
    loyal_end_date = models.DateTimeField(blank=True, null=True)
    customer_group = models.CharField(max_length=255, blank=True, null=True)
    loyalty_expire_days = models.IntegerField(blank=True, null=True)
    is_redeem_limited = models.CharField(max_length=5,choices=status_filed,default='y',blank=True, null=True)
    redeem_amount_type = models.CharField(max_length=20,choices=redeem_amount_choices,default='fixed',blank=True, null=True)
    redeem_type = models.CharField(max_length=20,choices=redeem_choices,default='loyalty',blank=True, null=True)
    redeem_limit = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=5,choices=status_filed,default='y',blank=True, null=True)
    isblocked = models.CharField(max_length=5,choices=status_filed,default='n',blank=True, null=True)
    isdeleted = models.CharField(max_length=5,choices=status_filed,default='n',blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_credit_point'

class EngageboostCreditPointConditions(models.Model):
    loyalty_master = models.ForeignKey(EngageboostCreditPoint,on_delete=models.CASCADE,related_name='CreditPointConditions',blank=True, null=True)
    fields = models.IntegerField(blank=True, null=True)
    condition = models.CharField(max_length=255, blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    all_category_id = models.TextField(blank=True, null=True)
    all_product_id = models.TextField(blank=True, null=True)
    all_customer_id = models.TextField(blank=True, null=True)
    all_day_id = models.CharField(max_length=21, blank=True, null=True)
    condition_type = models.CharField(max_length=255, blank=True, null=True)
    field_type = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_credit_point_conditions'

class EngageboostMappedCategories(models.Model):
    checked_category_id = models.IntegerField(blank=True, null=True)
    mapped_category_id = models.IntegerField(blank=True, null=True)
    mapped_taxonomy = models.TextField(blank=True, null=True)
    mapped_for = models.CharField(max_length=255,blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    boost_category_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_mapped_categories'

class EngageboostMarketplaceManifestsFeedStatus(models.Model):
    is_called_CHOICES = (
        ('y', 'y'),
        ('n', 'n')
    )
    product_id = models.IntegerField(blank=True, null=True)
    marketplace_id = models.IntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    process_id = models.BigIntegerField(blank=True, null=True)
    process_status = models.CharField(max_length=255, blank=True, null=True)
    is_called = models.CharField(max_length=255,choices=is_called_CHOICES)
    company_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_marketplace_feed_status'

class EngageboostMarketplaceFieldLabels(models.Model):
    field_id = models.BigIntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    field_label = models.CharField(max_length=250,blank=True, null=True)
    variant = models.CharField(max_length=256, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_marketplace_field_labels'

class EngageboostMarketplaceFieldValue(models.Model):
    product_id = models.IntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    field_id = models.IntegerField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    field_name = models.CharField(max_length=250, blank=True, null=True)
    field_label = models.CharField(max_length=250, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_marketplace_field_value'

class EngageboostWarehouseManager(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    warehouse_id = models.IntegerField(blank=True, null=True)
    manager = models.ForeignKey(EngageboostUsers,blank=True, null=True, on_delete=models.CASCADE)
    created_date = models.CharField(max_length=255, blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    role = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_warehouse_manager'

class EngageboostWarehouseMasterApplicableChannels(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    warehouse_master_id = models.IntegerField(blank=True, null=True)
    applicable_channel_id = models.IntegerField(blank=True, null=True)
    applicable_channel_name = models.IntegerField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_warehouse_master_applicable_channels'

class EngageboostWarehouseMasterApplicableRegions(models.Model):
    ware_house_master_id = models.IntegerField(blank=True, null=True)
    applicable_country_id = models.IntegerField(blank=True, null=True)
    applicable_country_name = models.CharField(max_length=255, blank=True, null=True)
    applicable_state_id = models.IntegerField(blank=True, null=True)
    applicable_state_name = models.CharField(max_length=255, blank=True, null=True)
    applicable_city_id = models.IntegerField(blank=True, null=True)
    applicable_city_name = models.CharField(max_length=255, blank=True, null=True)
    applicable_zip_code = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_warehouse_master_applicable_regions'

class EngageboostZoneZipcodeMasters(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    zone = models.ForeignKey(EngageboostZoneMasters,on_delete=models.CASCADE,related_name='ZoneZipcodeMasters', blank=True, null=True)
    zip_code = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_zone_zipcode_masters'

class EngageboostTrafficReports(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    country_code = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=255, blank=True, null=True)
    average_duration = models.FloatField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    medium = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    totalvisit = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_traffic_reports'

class EngageboostTrafficReportsBrowsers(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    country_code = models.CharField(max_length=255, blank=True, null=True)
    return_user = models.CharField(max_length=255, blank=True, null=True)
    new_user = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=255, blank=True, null=True)
    average_duration = models.FloatField(blank=True, null=True)
    browser = models.CharField(max_length=255, blank=True, null=True)
    totalvisit = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_traffic_reports_browsers'

class EngageboostTrafficReportsMobiles(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    country_code = models.CharField(max_length=255, blank=True, null=True)
    return_user = models.CharField(max_length=255, blank=True, null=True)
    new_user = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=255, blank=True, null=True)
    average_duration = models.FloatField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    mobiledevice = models.CharField(max_length=255, blank=True, null=True)
    totalvisit = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_traffic_reports_mobiles'

class EngageboostTrafficReportsPages(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    country_code = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=255, blank=True, null=True)
    average_duration = models.FloatField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    medium = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    pagepath = models.CharField(max_length=255, blank=True, null=True)
    pageviews = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_traffic_reports_pages'

class EngageboostTrafficReportsSociales(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    social_net_work = models.CharField(max_length=255, blank=True, null=True)
    visits = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_traffic_reports_sociales'

class EngageboostTrafficReportsSources(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    country_code = models.CharField(max_length=255, blank=True, null=True)
    return_user = models.CharField(max_length=255, blank=True, null=True)
    new_user = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=255, blank=True, null=True)
    average_duration = models.FloatField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    browser = models.CharField(max_length=255, blank=True, null=True)
    totalvisit = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_traffic_reports_sources'

class EngageboostTemplateCategories(models.Model):
    template_category_master_id = models.IntegerField(blank=True, null=True)
    template_master_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_template_categories'

class EngageboostTemplateCategoryMasters(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    name = models.CharField(max_length=255,blank=True, null=True)
    createdby = models.CharField(max_length=255,blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_template_category_masters'

class EngageboostTemplateColorMasters(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    status_choices=(
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    status=models.CharField(max_length=2,choices=status_choices, default='Active')
    class Meta:
        db_table = 'engageboost_template_color_masters'

class EngageboostTemplateColors(models.Model):
    template_color_id = models.IntegerField(blank=True, null=True)
    template_master_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_template_colors'

class EngageboostTemplateIndustries(models.Model):
    industry_master_id = models.IntegerField(blank=True, null=True)
    template_master_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_template_industries'

class EngageboostTemplateIndustryMasters(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    name = models.CharField(max_length=255,blank=True, null=True)
    image = models.CharField(max_length=255,blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    modifiedby = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    store_type_categories_selected = models.CharField(max_length=255, blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_template_industry_masters'

class EngageboostTemplateMasters(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    name = models.CharField(max_length=255,blank=True, null=True)
    code = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    image = models.CharField(max_length=255,blank=True, null=True)
    zoom_image = models.CharField(max_length=255,blank=True, null=True)
    company_website_id = models.BigIntegerField(blank=True, null=True)
    folder_name = models.CharField(max_length=255,blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_template_masters'

class EngageboostTemplateRelations(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    relationtable_choices=(
        ('CAT', 'CAT'),
        ('COL', 'COL'),
        ('IND', 'IND')
    )
    template_master_id = models.IntegerField(blank=True, null=True)
    color_category_industry_id = models.IntegerField(blank=True, null=True)
    relationtable=models.CharField(max_length=2,choices=relationtable_choices, default='none')
    isdefault=models.CharField(max_length=2,choices=enum_choices, default='n')
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_template_relations'

class EngageboostTemplateSettings(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    template_id = models.IntegerField(blank=True, null=True)
    page_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    header_content = models.BinaryField(blank=True, null=True)
    footer_content = models.BinaryField(blank=True, null=True)
    leftpanel_content = models.BinaryField(blank=True, null=True)
    rightpanel_content = models.BinaryField(blank=True, null=True)
    contents = models.BinaryField(blank=True, null=True)
    is_published=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_template_settings'

class EngageboostTempCategoryMasters(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    parent_id = models.TextField(blank=True, null=True)
    lft = models.IntegerField(blank=True, null=True)
    rght = models.IntegerField(blank=True, null=True)
    check_id = models.IntegerField(blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    thumb_image = models.CharField(max_length=255, blank=True, null=True)
    page_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    category_url = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    error_text = models.TextField(blank=True, null=True)
    err_flag = models.TextField(blank=True, null=True)
    file_name = models.TextField(blank=True, null=True)
    customer_group_id = models.IntegerField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_temp_category_masters'

class EngageboostTempChannelCategoryMappings(models.Model):
    channel_category_id = models.IntegerField(blank=True, null=True)
    channel_parent_category_id = models.IntegerField(blank=True, null=True)
    boost_parent_category_id = models.IntegerField(blank=True, null=True)
    boost_category_id = models.IntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_temp_channel_category_mappings'

class EngageboostTempCustomers(models.Model):
    assignment_choices=(
        ('0', '0'),
        ('1', '1')
    )
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(EngageboostCountries,on_delete=models.CASCADE, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    post_code = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    perfix = models.CharField(max_length=10, blank=True, null=True)
    suffix = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    owner_id = models.IntegerField(blank=True, null=True)
    customer_group = models.ForeignKey(EngageboostCustomerGroup,on_delete=models.CASCADE,blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True)
    view_time = models.DateTimeField(blank=True, null=True)
    assignment=models.CharField(max_length=2,choices=assignment_choices, default='0')
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    is_import=models.CharField(max_length=2,choices=enum_choices, default='n')
    file_name = models.TextField(blank=True, null=True)
    err_flag = models.IntegerField(blank=True, null=True)
    error_text = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_temp_customers'

class EngageboostTempEmktContacts(models.Model):
    email_format_choice=(
        ('HTML', 'HTML'),
        ('TEXT', 'TEXT'),
        ('HTML&TEXT', 'HTML&TEXT')
    )
    activity_status_choice=(
        ('active', 'active'),
        ('subscribed', 'subscribed'),
        ('unsubscribed', 'unsubscribed')
    )
    confirmation_status_choice=(
        ('confirm', 'confirm'),
        ('unconfirm', 'unconfirm')
    )
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    contact_list_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    list_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    email_format=models.CharField(max_length=2,choices=email_format_choice, default='HTML')
    activity_status=models.CharField(max_length=2,choices=activity_status_choice, default='active')
    confirmation_status=models.CharField(max_length=2,choices=confirmation_status_choice, default='unconfirm')
    date_of_birth = models.CharField(max_length=50, blank=True, null=True)
    anniversary_date = models.CharField(max_length=50, blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    confirm_date = models.DateField(blank=True, null=True)
    confirm_ip = models.CharField(max_length=255, blank=True, null=True)
    edeal=models.CharField(max_length=2,choices=enum_choices, default='n')
    interest=models.CharField(max_length=2,choices=enum_choices, default='n')
    opt_in=models.CharField(max_length=2,choices=enum_choices, default='n')
    e_deal=models.CharField(max_length=2,choices=enum_choices, default='n')
    mail_flag=models.CharField(max_length=2,choices=enum_choices, default='n')
    bounce_check_flag=models.CharField(max_length=2,choices=enum_choices, default='n')
    feedback = models.TextField(blank=True, null=True)
    unsub_date = models.DateField(blank=True, null=True)
    email_campaign_id = models.IntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    file_name = models.TextField(blank=True, null=True)
    err_flag = models.IntegerField(blank=True, null=True)
    error_text = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_temp_emkt_contacts'

class EngageboostTempProductCustomFields(models.Model):
    product_id = models.CharField(max_length=255, blank=True, null=True)
    field_name = models.CharField(max_length=255, blank=True, null=True)
    field_value = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_temp_product_custom_fields'

class EngageboostTempProducts(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    veg_nonveg_type_choice=(
        ('Veg', 'Veg'),
        ('Non Veg', 'Non Veg'),
        ('NA', 'NA')
    )
    website_id = models.IntegerField(blank=True, null=True)
    customer_group_id = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    weight = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    shippingclass_id = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    taxclass_id = models.TextField(blank=True, null=True)
    po_taxclass_id = models.TextField(blank=True, null=True)
    visibility_id = models.TextField(blank=True, null=True)
    supplier_id = models.CharField(max_length=255, blank=True, null=True)
    parent_product_id = models.CharField(max_length=255, blank=True, null=True)
    variant_type = models.CharField(max_length=255, blank=True, null=True)
    category1 = models.CharField(max_length=255, blank=True, null=True)
    category2 = models.CharField(max_length=255, blank=True, null=True)
    category3 = models.CharField(max_length=255, blank=True, null=True)
    category4 = models.CharField(max_length=255, blank=True, null=True)
    meta_url = models.CharField(max_length=256, blank=True, null=True)
    metatitle = models.CharField(max_length=255, blank=True, null=True)
    metadescription = models.CharField(max_length=255, blank=True, null=True)
    metatag = models.CharField(max_length=255, blank=True, null=True)
    warehouse_name = models.CharField(max_length=255, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    safety_stock = models.IntegerField(blank=True, null=True)
    islot = models.IntegerField(blank=True, null=True)
    islabel = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    new_date = models.CharField(max_length=255, blank=True, null=True)
    isbn = models.TextField(blank=True, null=True)
    asin = models.TextField(blank=True, null=True)
    ean = models.TextField(blank=True, null=True)
    barcodes = models.TextField(blank=True, null=True)
    npn = models.CharField(max_length=255, blank=True, null=True)
    supc = models.CharField(max_length=60, blank=True, null=True)
    max_order_unit = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    video = models.CharField(max_length=255, blank=True, null=True)
    mp_description = models.TextField(blank=True, null=True)
    mp_features = models.TextField(blank=True, null=True)
    mp_system_requirements = models.TextField(blank=True, null=True)
    mp_templates = models.TextField(blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    last_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    avg_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    isdeleted = models.IntegerField(blank=True, null=True)
    isblocked = models.IntegerField(blank=True, null=True)
    is_import=models.CharField(max_length=2,choices=enum_choices, default='n')
    is_auctionable = models.IntegerField(blank=True, null=True)
    image_0 = models.CharField(max_length=255, blank=True, null=True)
    image_1 = models.CharField(max_length=255, blank=True, null=True)
    image_2 = models.CharField(max_length=255, blank=True, null=True)
    image_3 = models.CharField(max_length=255, blank=True, null=True)
    image_4 = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    marketplace = models.TextField(blank=True, null=True)
    ebaytitle = models.TextField(blank=True, null=True)
    webshoptitle = models.TextField(blank=True, null=True)
    webshopvideo = models.TextField(blank=True, null=True)
    webshopdecription = models.TextField(blank=True, null=True)
    webshopfeatures = models.TextField(blank=True, null=True)
    webshopsystemrequirements = models.TextField(blank=True, null=True)
    webshoptemplates = models.TextField(blank=True, null=True)
    webshopprocondotion = models.TextField(blank=True, null=True)
    webshopcategoryname = models.TextField(blank=True, null=True)
    webshoplisitngduration = models.TextField(blank=True, null=True)
    webshopdispatchtimemax = models.TextField(blank=True, null=True)
    webshopchannelid = models.TextField(blank=True, null=True)
    ebayvideo = models.TextField(blank=True, null=True)
    ebaydecription = models.TextField(blank=True, null=True)
    ebayfeatures = models.TextField(blank=True, null=True)
    ebaysystemrequirements = models.TextField(blank=True, null=True)
    ebaytemplates = models.TextField(blank=True, null=True)
    ebayprocondotion = models.TextField(blank=True, null=True)
    ebaycategoryname = models.TextField(blank=True, null=True)
    ebaylisitngduration = models.TextField(blank=True, null=True)
    ebaydispatchtimemax = models.TextField(blank=True, null=True)
    ebaychannelid = models.TextField(blank=True, null=True)
    amazontitle = models.TextField(blank=True, null=True)
    amazonvideo = models.TextField(blank=True, null=True)
    amazondecription = models.TextField(blank=True, null=True)
    amazonfeatures = models.TextField(blank=True, null=True)
    amazonsystemrequirements = models.TextField(blank=True, null=True)
    amazontemplates = models.TextField(blank=True, null=True)
    amazonprocondotion = models.TextField(blank=True, null=True)
    amazonategoryname = models.TextField(blank=True, null=True)
    amazonlisitngduration = models.TextField(blank=True, null=True)
    amazondispatchtimemax = models.TextField(blank=True, null=True)
    amazonchannelid = models.TextField(blank=True, null=True)
    availablequantity = models.TextField(blank=True, null=True)
    defaultprice = models.TextField(blank=True, null=True)
    amazonin_price = models.TextField(blank=True, null=True)
    amazonuk_price = models.TextField(blank=True, null=True)
    amazonus_price = models.TextField(blank=True, null=True)
    ebayau_price = models.TextField(blank=True, null=True)
    ebayin_price = models.TextField(blank=True, null=True)
    ebayuk_price = models.TextField(blank=True, null=True)
    ebayusa_price = models.TextField(blank=True, null=True)
    flipkart_price = models.TextField(blank=True, null=True)
    paytm_price = models.TextField(blank=True, null=True)
    snapdeal_price = models.TextField(blank=True, null=True)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    avgcost = models.TextField(blank=True, null=True)
    lastcost = models.TextField(blank=True, null=True)
    sla = models.IntegerField(blank=True, null=True)
    veg_nonveg_type=models.CharField(max_length=2,choices=veg_nonveg_type_choice, default='NA')
    file_name = models.TextField(blank=True, null=True)
    err_flag = models.IntegerField(blank=True, null=True)
    error_text = models.TextField(blank=True, null=True)
    price_formula_id_for_customer = models.CharField(max_length=255, blank=True, null=True)
    price_formula_id_for_supplier = models.CharField(max_length=255, blank=True, null=True)
    amazonin_sku = models.TextField(blank=True, null=True)
    snapdeal_sku = models.TextField(blank=True, null=True)
    amazonuk_sku = models.TextField(blank=True, null=True)
    amazonus_sku = models.TextField(blank=True, null=True)
    ebayau_sku = models.TextField(blank=True, null=True)
    ebayin_sku = models.TextField(blank=True, null=True)
    ebayuk_sku = models.TextField(blank=True, null=True)
    ebayusa_sku = models.TextField(blank=True, null=True)
    flipkart_sku = models.TextField(blank=True, null=True)
    paytm_sku = models.TextField(blank=True, null=True)
    uom = models.TextField(blank=True, null=True)
    product_offer_desc = models.CharField(max_length=256, blank=True, null=True)
    product_offer_start_date = models.DateField(blank=True, null=True)
    product_offer_end_date = models.DateField(blank=True, null=True)
    hsn_id = models.TextField(blank=True, null=True)
    visible_in_listing = models.CharField(max_length=10, blank=True, null=True,default='n')
    related_product_skus = models.TextField(blank=True, null=True)
    upsell_product_skus = models.TextField(blank=True, null=True)
    cross_product_skus = models.TextField(blank=True, null=True)
    associated_product_skus = models.TextField(blank=True, null=True)
    substitude_product_skus = models.TextField(blank=True, null=True)
    meta_og_tags = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_temp_products'

class EngageboostTempProductimages(models.Model):
    status_choice=(
        ('0','0'),
        ('1','1')
    )
    website_id = models.IntegerField(blank=True, null=True)
    # product = models.ForeignKey(EngageboostTempProducts,on_delete=models.CASCADE,related_name='product_images',blank=True, null=True)
    product = models.IntegerField(blank=True, null=True)
    img = models.CharField(max_length=255, blank=True, null=True)
    error_msg = models.CharField(max_length=255, blank=True, null=True)
    status=models.CharField(max_length=2,choices=status_choice, default='0')
    is_cover = models.IntegerField(blank=True, null=True)
    img_title = models.CharField(max_length=255, blank=True, null=True)
    img_alt = models.CharField(max_length=255, blank=True, null=True)
    img_order = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_temp_productimages'

class EngageboostTempSuppliers(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    address_one = models.CharField(max_length=255, blank=True, null=True)
    address_two = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=255, blank=True, null=True)
    vat_cst_number = models.CharField(max_length=256, blank=True, null=True)
    cst_number = models.CharField(max_length=256, blank=True, null=True)
    currency_id = models.TextField(blank=True, null=True)
    exchange_rate = models.FloatField(blank=True, null=True)
    lead_time = models.CharField(max_length=255, blank=True, null=True)
    credit_period = models.CharField(max_length=256, blank=True, null=True)
    carrier = models.CharField(max_length=255, blank=True, null=True)
    over_due = models.IntegerField(blank=True, null=True)
    owner_id = models.IntegerField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    view_time = models.DateTimeField(blank=True, null=True)
    assignment=models.CharField(max_length=2,choices=enum_choices, default='n')
    status = models.CharField(max_length=255, blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    is_import=models.CharField(max_length=2,choices=enum_choices, default='n')
    file_name = models.TextField(blank=True, null=True)
    err_flag = models.IntegerField(blank=True, null=True)
    error_text = models.TextField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_temp_suppliers'

class EngageboostTemporaryShoppingCarts(models.Model):
    veg_nonveg_type_choice=(
        ('Veg', 'Veg'),
        ('Non Veg', 'Non Veg'),
        ('NA', 'NA')
    )
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    device_id = models.CharField(max_length=255, blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    product_sku = models.CharField(max_length=255, blank=True, null=True)
    original_price = models.FloatField(blank=True, null=True)
    selling_price = models.FloatField(blank=True, null=True)
    offer = models.CharField(max_length=255, blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    variant_name = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    veg_nonveg_type=models.CharField(max_length=2,choices=veg_nonveg_type_choice, default='NA')
    warehouse_id = models.IntegerField(blank=True, null=True)
    custom_field_name = models.CharField(max_length=255, blank=True, null=True)
    custom_field_value = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_temporary_shopping_carts'

class EngageboostTmpPurchaseOrderProducts(models.Model):
    purchase_order_tmp_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_tmp_purchase_order_products'

class EngageboostTmpPurchaseOrders(models.Model):
    enum_choices=(
        ('p', 'p'),
        ('s', 's'),
        ('v', 'v'),
        ('r', 'r')
    )
    website_id = models.IntegerField(blank=True, null=True)
    purchase_order_id = models.CharField(max_length=255, blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    supplier_id = models.IntegerField(blank=True, null=True)
    gross_amount = models.FloatField(blank=True, null=True)
    paid_amount = models.FloatField(blank=True, null=True)
    discount_amount = models.FloatField(blank=True, null=True)
    currency_id = models.IntegerField(blank=True, null=True)
    status=models.CharField(max_length=2,choices=enum_choices ,default='p')
    class Meta:
        db_table = 'engageboost_tmp_purchase_orders'

class EngageboostTaxRates(models.Model):
    apply_choices=(
        ('b', 'b'),
        ('s', 's')
    )
    tax_type_choices=(
        ('VAT', 'VAT'),
        ('CST', 'CST'),
        ('Excise Duty', 'Excise Duty')

    )
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    apply = models.CharField(max_length=2,choices=apply_choices, default='b')
    percentage = models.FloatField(blank=True, null=True)
    tax_type = models.CharField(max_length=20,choices=tax_type_choices, default='VAT')
    country = models.ForeignKey(EngageboostCountries,on_delete=models.CASCADE, blank=True, null=True)
    state_id = models.TextField(blank=True, null=True)
    zipcode = models.TextField(blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_tax_rates'

class EngageboostTaxRatesConditions(models.Model):
    tax_rate = models.ForeignKey(EngageboostTaxRates,on_delete=models.CASCADE, related_name='TaxRatesConditions', blank=True, null=True)
    fields = models.IntegerField(blank=True, null=True)
    condition = models.CharField(max_length=255, blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)
    condition_type = models.CharField(max_length=255, blank=True, null=True)
    field_type = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_tax_rates_conditions'

class EngageboostTaxRuleTables(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    product_tax_class_id = models.CharField(max_length=255)
    customer_tax_class_id = models.CharField(max_length=255)
    priority = models.IntegerField(blank=True, null=True)
    tax_rate = models.ForeignKey(EngageboostTaxRates, on_delete=models.CASCADE, blank=True, null=True)
    rule_name = models.CharField(max_length=255, blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_tax_rule_tables'

class EngageboostTaxSettings(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    display_zero_tax_subtotal_choice=(
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    display_shipping_amount_choice=(
        ('Excluding Tax', 'Excluding Tax'),
        ('Including Tax', 'Including Tax'),
        ('Including and Excluding Tax', 'Including and Excluding Tax')
    )
    display_subtotal_choice=(
        ('Excluding Tax', 'Excluding Tax'),
        ('Including Tax', 'Including Tax'),
        ('Including and Excluding Tax', 'Including and Excluding Tax')
    )
    display_prices_choice=(
        ('Excluding Tax', 'Excluding Tax'),
        ('Including Tax', 'Including Tax'),
        ('Including and Excluding Tax', 'Including and Excluding Tax')
    )
    display_shipping_prices_choice=(
        ('Excluding Tax', 'Excluding Tax'),
        ('Including Tax', 'Including Tax'),
        ('Including and Excluding Tax', 'Including and Excluding Tax')
    )
    display_product_prices_in_catalog_choice=(
        ('Excluding Tax', 'Excluding Tax'),
        ('Including Tax', 'Including Tax'),
        ('Including and Excluding Tax', 'Including and Excluding Tax')
    )
    apply_discount_on_prices_choice=(
        ('Excluding Tax', 'Excluding Tax'),
        ('Including Tax', 'Including Tax'),
        ('Including and Excluding Tax', 'Including and Excluding Tax')
    )
    apply_customer_tax_choice=(
        ('Before Discount', 'Before Discount'),
        ('After Discount', 'After Discount')
    )
    shipping_price_Choice=(
        ('Excluding Tax', 'Excluding Tax'),
        ('Including Tax', 'Including Tax')
    )
    catalog_prices_choice=(
        ('Including Tax', 'Including Tax'),
        ('Excluding Tax', 'Excluding Tax')
    )
    tax_calculation_based_on_choice=(
        ('Shipping Address', 'Shipping Address'),
        ('Billing Address', 'Billing Address')
    )
    website_id = models.BigIntegerField(blank=True, null=True)
    shipping_tax_class = models.IntegerField(blank=True, null=True)
    tax_calculation_based_on=models.CharField(max_length=50,choices=tax_calculation_based_on_choice, default='Shipping Address', null=True)
    catalog_prices=models.CharField(max_length=50,choices=catalog_prices_choice, default='Excluding Tax', null=True)
    shipping_price=models.CharField(max_length=50,choices=shipping_price_Choice, default='Excluding Tax', null=True)
    apply_customer_tax=models.CharField(max_length=50,choices=apply_customer_tax_choice, default='Before Discount', null=True)
    apply_discount_on_prices=models.CharField(max_length=50,choices=apply_discount_on_prices_choice, default='null', null=True)
    display_product_prices_in_catalog=models.CharField(max_length=50,choices=display_product_prices_in_catalog_choice, default='null', null=True)
    display_shipping_prices=models.CharField(max_length=50,choices=display_shipping_prices_choice, default='null', null=True)
    display_prices=models.CharField(max_length=50,choices=display_prices_choice, default='null', null=True)
    display_subtotal=models.CharField(max_length=50,choices=display_subtotal_choice, default='null', null=True)
    display_shipping_amount=models.CharField(max_length=50,choices=display_shipping_amount_choice, default='null', null=True)
    include_tax_in_grand_total=models.CharField(max_length=50,choices=display_zero_tax_subtotal_choice, default='null', null=True)
    display_full_tax_summary=models.CharField(max_length=50,choices=display_zero_tax_subtotal_choice, default='null', null=True)
    display_zero_tax_subtotal=models.CharField(max_length=50,choices=display_zero_tax_subtotal_choice, default='null', null=True)
    cst_applicable=models.CharField(max_length=50,choices=display_zero_tax_subtotal_choice, default='null', null=True)
    excise_duty = models.FloatField(blank=True, null=True)
    shipping_tax_rate = models.FloatField(blank=True, null=True, default=0.00)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n', null=True)
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n', null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_tax_settings'

class EngageboostTaxclasses(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_taxclasses'

class EngageboostShippedorder(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    custom_order_id = models.CharField(max_length=70, blank=True, null=True)
    custom_ship_id = models.CharField(max_length=255, blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    webshop_id = models.IntegerField(blank=True, null=True)
    shipping_method_id = models.CharField(max_length=50, blank=True, null=True)
    excise_duty = models.FloatField(blank=True, null=True)
    gross_amount = models.FloatField(blank=True, null=True)
    net_amount = models.FloatField(blank=True, null=True)
    paid_amount = models.FloatField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    tracking_company_name = models.CharField(max_length=255, blank=True, null=True)
    tracking_no = models.CharField(max_length=255, blank=True, null=True)
    tracking_url = models.CharField(max_length=255, blank=True, null=True)
    shipment_id = models.IntegerField(blank=True, null=True)
    shipment_order = models.ForeignKey(EngageboostShipmentOrders,on_delete=models.CASCADE,related_name='shipped_order',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_shippedorder'

class EngageboostShippedProducts(models.Model):
    order_id = models.IntegerField(blank=True, null=True)
    shipped = models.ForeignKey(EngageboostShippedorder,on_delete=models.CASCADE,related_name='shipped_order_products',blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_shipped_products'

class EngageboostShippingMasters(models.Model):
    method_type_choices=(
        ('Manual', 'Manual'),
        ('Auto', 'Auto')
    )
    shipping_type_choice=(
        ('Shipping', 'Shipping'),
        ('Courier', 'Courier'),
        ('Marketplace', 'Marketplace')
    )
    tracking_type_choice=(
        ('Awb', 'Awb'),
        ('Range', 'Range')
    )
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    method_name = models.CharField(max_length=100, blank=True, null=True)
    short_name = models.CharField(max_length=100, blank=True, null=True)
    method_type=models.CharField(max_length=15,choices=method_type_choices, default='Manual')
    shipping_type=models.CharField(max_length=15,choices=shipping_type_choice, default='Shipping')
    tracking_type=models.CharField(max_length=15,choices=tracking_type_choice, default='Awb')
    tracking_url = models.CharField(max_length=250, blank=True, null=True)
    tracking_id_start = models.IntegerField(blank=True, null=True)
    tracking_id_end = models.IntegerField(blank=True, null=True)
    awb_prefix = models.CharField(max_length=50, blank=True, null=True)
    awb_suffix = models.CharField(max_length=50, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    website_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_shipping_masters'

class EngageboostShippingMastersSettings(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    applicable_for_choices=(
        ('w', 'w'),
        ('e', 'e'),
        ('a', 'a')
    )
    picking_choice = (
        ('HomeDelivery', 'HomeDelivery'),
        ('SelfPickup', 'SelfPickup')
    )
    fedex_user_id = models.CharField(max_length=50, blank=True, null=True)
    fedex_meter_no = models.CharField(max_length=50, blank=True, null=True)
    fedex_key = models.CharField(max_length=50, blank=True, null=True)
    fedex_password = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    shipping_method_id = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    method_name = models.CharField(max_length=255, blank=True, null=True)
    mthod_type = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    flat_price = models.FloatField(blank=True, null=True)
    handling_fees_type = models.IntegerField(blank=True, null=True)
    handling_price = models.FloatField(blank=True, null=True)
    allowed_countries = models.IntegerField(blank=True, null=True)
    country_ids = models.TextField(blank=True, null=True)
    table_rate_matrix_type = models.IntegerField(blank=True, null=True)
    minimum_order_amount = models.FloatField(blank=True, null=True)
    ups_account_number = models.CharField(max_length=50, blank=True, null=True)
    ups_user_id = models.CharField(max_length=255, blank=True, null=True)
    ups_password = models.CharField(max_length=255, blank=True, null=True)
    ups_weight_unit = models.CharField(max_length=255, blank=True, null=True)
    ups_min_weight = models.CharField(max_length=255, blank=True, null=True)
    ups_max_weight = models.CharField(max_length=255, blank=True, null=True)
    service_methods_free = models.IntegerField(blank=True, null=True)
    service_methods = models.TextField(blank=True, null=True)
    package_code = models.IntegerField(blank=True, null=True)
    usps_user_id = models.CharField(max_length=255, blank=True, null=True)
    usps_password = models.CharField(max_length=255, blank=True, null=True)
    usps_devolopment_mode = models.IntegerField(blank=True, null=True)
    usps_size = models.CharField(max_length=50, blank=True, null=True)
    usps_machinable = models.CharField(max_length=50, blank=True, null=True)
    usps_intr_package = models.IntegerField(blank=True, null=True)
    is_ebay=models.CharField(max_length=2,choices=enum_choices, default='n')
    dispatch_time_max = models.IntegerField(blank=True, null=True)
    state_id = models.TextField(blank=True, null=True)
    table_matrix_status = models.IntegerField(blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    applicable_for=models.CharField(max_length=2,choices=applicable_for_choices, default='w')
    customer_code = models.CharField(max_length=100, blank=True, null=True)
    customer_code_cod = models.CharField(max_length=100, blank=True, null=True)
    is_bluedart_live=models.CharField(max_length=2,choices=enum_choices, default='n')
    origin_area = models.CharField(max_length=100, blank=True, null=True)
    self_pickup_price = models.FloatField(blank=True, null=True, default=0)
    zone_id = models.TextField(blank=True, null=True)
    picking_type = models.CharField(max_length=20,choices=picking_choice,default='HomeDelivery')
    class Meta:
        db_table = 'engageboost_shipping_masters_settings'

class EngageboostShippingServiceNames(models.Model):
    service_name = models.CharField(max_length=50, blank=True, null=True)
    service_code = models.CharField(max_length=50, blank=True, null=True)
    subproduct_code = models.CharField(max_length=10, blank=True, null=True)
    ebay_term = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    shipping_method_type = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_shipping_service_names'

class EngageboostShippingPackagingtype(models.Model):
    package_name = models.CharField(max_length=50, blank=True, null=True)
    package_code = models.CharField(max_length=50, blank=True, null=True)
    shipping_method_id = models.IntegerField(blank=True, null=True)
    international_status = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_shipping_packagingtype'

class EngageboostTags(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    tag_name = models.CharField(max_length=100, blank=True, null=True)
    color_code = models.CharField(max_length=50, blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_tags'

class EngageboostSuppliers(models.Model):
    assignment_choices=(
        ('0', '0'),
        ('1', '1')
    )
    is_import_choices=(
        ('0', '0'),
        ('1', '1')
    )
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    address_one = models.CharField(max_length=255, blank=True, null=True)
    address_two = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=255, blank=True, null=True)
    vat_cst_number = models.CharField(max_length=256, blank=True, null=True)
    cst_number = models.CharField(max_length=256, blank=True, null=True)
    currency_id = models.IntegerField(blank=True, null=True)
    exchange_rate = models.FloatField(blank=True, null=True)
    lead_time = models.CharField(max_length=255, blank=True, null=True)
    default_warehouse_id = models.IntegerField(blank=True, null=True)
    credit_period = models.CharField(max_length=256, blank=True, null=True)
    carrier = models.CharField(max_length=255, blank=True, null=True)
    over_due = models.IntegerField(blank=True, null=True)
    owner_id = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True)
    view_time = models.DateTimeField(blank=True, null=True)
    assignment=models.CharField(max_length=2,choices=assignment_choices, default='0')
    status = models.CharField(max_length=255, blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    is_import=models.CharField(max_length=2,choices=is_import_choices, default='0')
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_suppliers'

class EngageboostPresets(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id  = models.IntegerField(blank=True, null=True)
    name= models.CharField(max_length=100, blank=True, null=True)
    shipping_method = models.ForeignKey(EngageboostShippingMasters,on_delete=models.CASCADE,related_name='presets',blank=True, null=True)
    service = models.ForeignKey(EngageboostShippingServiceNames,blank=True, null=True, on_delete=models.CASCADE)
    package = models.ForeignKey(EngageboostShippingPackagingtype,blank=True, null=True, on_delete=models.CASCADE)
    confirmation= models.CharField(max_length=100, blank=True, null=True)
    sizel   = models.IntegerField(blank=True, null=True)
    sizew   = models.IntegerField(blank=True, null=True)
    sizeh   = models.IntegerField(blank=True, null=True)
    weight  = models.CharField(max_length=100, blank=True, null=True)
    isblocked   = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted   = models.CharField(max_length=2,choices=enum_choices,default='n')
    created_date= models.DateTimeField(blank=True, null=True)
    modified_date   = models.DateTimeField(blank=True, null=True)
    createdby   = models.IntegerField(default='1')
    updatedby   = models.IntegerField(default='1')
    ip_address  = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_presets'

class EngageboostOrderActivity(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    activity_type = models.SmallIntegerField(blank=True, null=True) #1 for order, 2 for shipment, 3 for item, 4 for PO
    username = models.CharField(max_length=255, blank=True, null=True)
    user_ip_address = models.CharField(max_length=50, blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    purchase_order_id = models.IntegerField(blank=True, null=True)
    activity_comments = models.TextField(blank=True, null=True)
    activity_date = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_order_activity'

class EngageboostOrderDeliverySlot(models.Model):
    isdeleted = (
        ('n', 'n'),
        ('y', 'y')
    )
    order_id = models.BigIntegerField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    delivery_slot = models.CharField(max_length=100, blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=isdeleted,default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_order_delivery_slot'

class EngageboostOrderFilters(models.Model):
    filter_type = (
        ('Order', 'Order'),
        ('Shipment', 'Shipment')
    )
    name = models.CharField(max_length=256, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    store = models.CharField(max_length=100, blank=True, null=True)
    assign = models.CharField(max_length=100, blank=True, null=True)
    destination = models.CharField(max_length=100, blank=True, null=True)
    tags = models.CharField(max_length=100, blank=True, null=True)
    order_from_date = models.DateField(blank=True, null=True)
    order_to_date = models.DateField(blank=True, null=True)
    filter_type = models.CharField(max_length=2,choices=filter_type,default='Order')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isdeleted = models.SmallIntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_order_filters'

class EngageboostOrderLayouts(models.Model):
    isdeleted = (
        ('n', 'n'),
        ('y', 'y')

    )
    website_id = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    module = models.CharField(max_length=100, blank=True, null=True)
    screen_name = models.CharField(max_length=100, blank=True, null=True)
    header_name = models.TextField(blank=True, null=True)
    header_classname = models.TextField(blank=True, null=True)
    field_name = models.TextField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=isdeleted,default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_order_layouts'

class EngageboostOrderNotes(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    user_name = models.CharField(max_length=256, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    note_type = models.SmallIntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isdeleted = models.SmallIntegerField(blank=True, null=True)
    isblocked = models.SmallIntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_order_notes'

class EngageboostOrderReturnDetails(models.Model):
    isdeleted = (
       ('y', 'y'),
       ('n', 'n')
    )
    is_deleted = (
       ('y', 'y'),
       ('n', 'n')
    )
    order_id = models.BigIntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    return_by_id = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    return_status = models.CharField(max_length=100, blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=isdeleted, default="n")
    isblocked = models.CharField(max_length=2,choices=is_deleted, default="n")
    class Meta:
        db_table = 'engageboost_order_return_details'

class EngageboostOrderStatusSettings(models.Model):
    order_status_master_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_order_status_settings'

class EngageboostOrderSubscribe(models.Model):
    isdeleted = (
        ('n', 'n'),
        ('y', 'y')
    )
    website_id = models.BigIntegerField(blank=True, null=True)
    company_id = models.BigIntegerField(blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=isdeleted,default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_order_subscribe'

class EngageboostOrderSubscribeDetails(models.Model):
    isdeleted = (
        ('n', 'n'),
        ('y', 'y')
    )
    website_id = models.BigIntegerField(blank=True, null=True)
    company_id = models.BigIntegerField(blank=True, null=True)
    subscribe_id = models.BigIntegerField(blank=True, null=True)
    order_id = models.BigIntegerField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=isdeleted,default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_order_subscribe_details'

class EngageboostNewsletterSubcribes(models.Model):
    field_status = (
        ('n', 'n'),
        ('y', 'y')
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    unsubscribe = models.TextField(max_length=2,choices=field_status,default='n')
    isdeleted = models.CharField(max_length=2,choices=field_status,default='n')
    isblocked = models.CharField(max_length=2,choices=field_status,default='n')
    class Meta:
        db_table = 'engageboost_newsletter_subcribes'

class EngageboostPages(models.Model):
    field_status = (
        ('n', 'n'),
        ('y', 'y')
    )
    company_website_id = models.IntegerField(blank=True, null=True)
    page_name = models.CharField(max_length=250, blank=True, null=True)
    page_title = models.CharField(max_length=250, blank=True, null=True)
    url = models.CharField(max_length=250, blank=True, null=True)
    saved_page = models.CharField(max_length=50)
    meta_key = models.TextField(blank=True, null=True)
    meta_data = models.TextField(blank=True, null=True)
    meta_desc = models.CharField(max_length=255, blank=True, null=True)
    layout = models.IntegerField(blank=True, null=True)
    issaved = models.CharField(max_length=2,choices=field_status,default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=field_status,default='n')
    isblocked = models.CharField(max_length=2,choices=field_status,default='n')
    ispublished = models.CharField(max_length=2,choices=field_status,default='n')
    published = models.DateTimeField(blank=True, null=True)
    device = models.CharField(max_length=10, blank=True, null=True)
    template_image=models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_pages'

class EngageboostParentCategories(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    parent_category_id = models.IntegerField(blank=True, null=True)
    parent_two_category_id = models.IntegerField(default=0)
    parent_three_category_id = models.IntegerField(default=0)
    category_id = models.IntegerField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_parent_categories'

class EngageboostPaymentSetupDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    order_process_paid = models.IntegerField(blank=True, null=True)
    order_process_placed = models.IntegerField(blank=True, null=True)
    email_marketting_type = models.IntegerField(blank=True, null=True)
    contents = models.TextField(blank=True, null=True)
    refund = models.TextField(blank=True, null=True)
    privacy = models.TextField(blank=True, null=True)
    terms_of_service = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_payment_setup_details'

class EngageboostPaymentgatewayTypes(models.Model):
    enum_choices = (
        ('n', 'n'),
        ('y', 'y')
    )
    name = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    ebay_term = models.TextField(blank=True, null=True)
    order_by = models.IntegerField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_paymentgateway_types'

class EngageboostPaymentgatewayMethods(models.Model):
    isdeleted_status = (
        ('n', 'n'),
        ('y', 'y')
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    paymentgateway_type_id = models.IntegerField(blank=True, null=True)
    destination_url = models.TextField(blank=True, null=True)
    destination_sandbox_url = models.TextField(blank=True, null=True)
    notification_url = models.TextField(blank=True, null=True)
    notification_sandbox_url = models.TextField(blank=True, null=True)
    cancel_url = models.TextField(blank=True, null=True)
    cancel_sandbox_url = models.TextField(blank=True, null=True)
    ebay_term = models.CharField(max_length=255, blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=isdeleted_status,default='n')
    isdeleted = models.CharField(max_length=2,choices=isdeleted_status,default='n')
    class Meta:
        db_table = 'engageboost_paymentgateway_methods'

class EngageboostPaymentgatewaySettings(models.Model):
    is_status = (
        ('n', 'n'),
        ('y', 'y')
    )
    paymentgateway_method_id = models.IntegerField(blank=True, null=True)
    paymentgateway_type_id = models.IntegerField(blank=True, null=True)
    setting_order_by = models.IntegerField(blank=True, null=True)
    setting_label = models.TextField(blank=True, null=True)
    setting_key = models.TextField(blank=True, null=True)
    setting_default_val = models.TextField(blank=True, null=True)
    setting_desc = models.TextField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=is_status,default='n')
    isdeleted = models.CharField(max_length=2,choices=is_status,default='n')
    class Meta:
        db_table = 'engageboost_paymentgateway_settings'

class EngageboostPaymentgatewaySettingInformation(models.Model):
    is_status = (
        ('n', 'n'),
        ('y', 'y')
    )
    website_id = models.IntegerField(blank=True, null=True)
    paymentgateway_method_id = models.IntegerField(blank=True, null=True)
    paymentgateway_type_id = models.IntegerField(blank=True, null=True)
    setting_key = models.TextField(blank=True, null=True)
    setting_val = models.TextField(blank=True, null=True)
    paymentgateway_setting_id = models.IntegerField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=is_status,default='n')
    isdeleted = models.CharField(max_length=2,choices=is_status,default='n')
    class Meta:
        db_table = 'engageboost_paymentgateway_setting_information'

class EngageboostWebsitePaymentmethods(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    engageboost_company_website_id = models.IntegerField(blank=True, null=True)
    engageboost_paymentgateway_method_id = models.IntegerField(blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_website_paymentmethods'


class EngageboostPaymentWarehouse(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    warehouse_id = models.IntegerField(blank=True, null=True)
    payment_method_id = models.IntegerField(blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_payment_warehouse'


class EngageboostPaymentgatewaysGlobalsettings(models.Model):
    paypal_std_url = models.CharField(max_length=255, blank=True, null=True)
    paypal_expresscheckout_url = models.CharField(max_length=255, blank=True, null=True)
    paypal_pro_url = models.CharField(max_length=255, blank=True, null=True)
    ccavenue_url = models.CharField(max_length=255, blank=True, null=True)
    paypal_ipn = models.CharField(max_length=255, blank=True, null=True)
    googlecheckout_url = models.CharField(max_length=255, blank=True, null=True)
    authorize_net_url = models.CharField(max_length=255, blank=True, null=True)
    worldpay_url = models.CharField(max_length=255, blank=True, null=True)
    usaepay_url = models.CharField(max_length=255, blank=True, null=True)
    checkout_url = models.CharField(max_length=255, blank=True, null=True)
    barclaysepdq_url = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_paymentgateways_globalsettings'

class EngageboostTimezones(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    timezone_location = models.CharField(max_length=255, blank=True, null=True)
    gmt = models.CharField(max_length=255, blank=True, null=True)
    offset = models.FloatField(blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_timezones'

class EngageboostOtherLocation(models.Model):
    location = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_other_location'

class EngageboostPurchaseOrderProducts(models.Model):
    purchase_order_id = models.IntegerField(blank=True, null=True)
    product = models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE,blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    product_tax_price = models.FloatField(blank=True, null=True)
    discount_amount = models.FloatField(blank=True, null=True)
    tax_name = models.CharField(max_length=256, blank=True, null=True)
    tax_per = models.FloatField(blank=True, null=True)
    updated_quantity = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    lot_no = models.CharField(max_length=100, blank=True, null=True)
    rack_no = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_purchase_order_products'

class EngageboostPurchaseOrders(models.Model):
    shipping_cost_stats_choice=(
        ('e', 'e'),
        ('i', 'i')
    )
    status_choice=(
        ('Draft', 'Draft'),
        ('PO Sent', 'PO Sent'),
        ('Shipped', 'Shipped'),
        ('Cancel', 'Cancel'),
        ('Received Partial', 'Received Partial'),
        ('Grn Pending', 'Grn Pending'),
        ('Received Full', 'Received Full')
    )
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    purchase_order_id = models.CharField(max_length=255, blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    supplier_id = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    currency_id = models.IntegerField(blank=True, null=True)
    purchase_order_payment_id = models.IntegerField(blank=True, null=True)
    payment_method_description = models.TextField(blank=True, null=True)
    payment_due_date = models.DateField(blank=True, null=True)
    payment_days_credit = models.IntegerField(blank=True, null=True)
    purchase_order_shipping_id = models.IntegerField(blank=True, null=True)
    shipping_method_description = models.TextField(blank=True, null=True)
    shipping_cost = models.FloatField(blank=True, null=True)
    purchase_order_tax = models.FloatField(blank=True, null=True)
    gross_amount = models.FloatField(blank=True, null=True)
    net_amount = models.FloatField(blank=True, null=True)
    paid_amount = models.FloatField(blank=True, null=True)
    discount_amount = models.FloatField(blank=True, null=True)
    shipping_cost_base = models.FloatField(blank=True, null=True)
    purchase_order_tax_base = models.FloatField(blank=True, null=True)
    gross_amount_base = models.FloatField(blank=True, null=True)
    net_amount_base = models.FloatField(blank=True, null=True)
    paid_amount_base = models.FloatField(blank=True, null=True)
    discount_amount_base = models.FloatField(blank=True, null=True)
    shipping_cost_stats=models.CharField(max_length=2,choices=shipping_cost_stats_choice,default='e')
    status = models.CharField(max_length=255,choices=status_choice,default='Draft')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices,default='n')
    tracking_company = models.CharField(max_length=255, blank=True, null=True)
    tracking_id = models.CharField(max_length=255, blank=True, null=True)
    tracking_url = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_purchase_orders'

class EngageboostPurchaseOrdersReceived(models.Model):
    status_choice=(
        ('p', 'p'),
        ('s', 's'),
        ('v', 'v'),
        ('r', 'r')
    )
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    action_choice=(
        ('increase', 'increase'),
        ('decrease', 'decrease'),
        ('convert', 'convert'),
        ('move', 'move'),
        ('update', 'update'),
        ('imported', 'imported'),
        ('refund', 'refund'),
        ('none', 'none'),
        ('shortage', 'shortage'),
        ('damage', 'damage')
    )
    website_id = models.IntegerField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    purchase_order_master_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True, default=0)
    currency_id = models.IntegerField(blank=True, null=True)
    received_purchaseorder_id = models.CharField(max_length=255, blank=True, null=True)
    received_date = models.CharField(max_length=255,blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    supplier_id = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    product_id = models.CharField(max_length=255)
    quantity = models.IntegerField(blank=True, null=True)
    purchase_order_payment_id = models.IntegerField(blank=True, null=True)
    payment_method_description = models.TextField(blank=True, null=True)
    payment_due_date = models.DateField(blank=True, null=True)
    purchase_order_shipping_id = models.IntegerField(blank=True, null=True)
    shipping_method_description = models.TextField(blank=True, null=True)
    shipping_cost = models.FloatField(blank=True, null=True)
    purchase_order_tax = models.FloatField(blank=True, null=True)
    gross_amount = models.FloatField(blank=True, null=True)
    net_amount = models.FloatField(blank=True, null=True)
    paid_amount = models.FloatField(blank=True, null=True)
    discount_amount = models.FloatField(blank=True, null=True)
    gross_amount_base = models.FloatField(blank=True, null=True)
    net_amount_base = models.FloatField(blank=True, null=True)
    shipping_cost_base = models.FloatField(blank=True, null=True)
    purchase_order_tax_base = models.FloatField(blank=True, null=True)
    discount_amount_base = models.FloatField(blank=True, null=True)
    paid_amount_base = models.FloatField(blank=True, null=True)
    status=models.CharField(max_length=2,choices=status_choice,default='p')
    isblocked=models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices,default='n')
    action=models.CharField(max_length=255,choices=action_choice,default='null')
    class Meta:
        db_table = 'engageboost_purchase_orders_received'


class EngageboostPurchaseOrderReceivedProductDetails(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
        )
    condition_choices = (
            ('received', 'received'),
            ('damaged', 'damaged'),
            ('expired', 'expired'),
            ('shortage', 'shortage'),
            ('mrp_issue', 'mrp_issue')
        )
    website_id = models.IntegerField(blank=True, null=True)
    purchase_order_id = models.IntegerField(blank=True, null=True)
    purchase_order_product_id = models.IntegerField(blank=True, null=True)
    purchase_order_received_id = models.IntegerField(blank=True, null=True)
    lot_no = models.CharField(max_length=20, blank=True, null=True)
    rack_no = models.CharField(max_length=20, blank=True, null=True)
    received_quantity = models.IntegerField(blank=True, null=True)
    damaged_quantity = models.IntegerField(blank=True, null=True)
    shortage_quantity = models.IntegerField(blank=True, null=True)
    total_quantity = models.IntegerField(blank=True, null=True)
    manufactured_date = models.DateField(blank=True, null=True)
    received_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    expiry_issue_comment = models.TextField(blank=True, null=True)
    expiry_issue = models.CharField(max_length=2, choices=enum_choices, default='n')
    remarks = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    goods_condition = models.CharField(max_length=20, choices=enum_choices, default='received')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices,default='n')

    class Meta:
        db_table = 'engageboost_purchase_orders_received_product_details'


class EngageboostPurchaseOrderReceivedProducts(models.Model):
    exp_issue_choice=(
        ('y', 'y'),
        ('n', 'n')
    )
    mrp_issue_choice=(
        ('y', 'y'),
        ('n', 'n')
    )
    good_received_choice=(
        ('y', 'y'),
        ('n', 'n')
    )
    ok_to_ship_choice=(
        ('y', 'y'),
        ('n', 'n')
    )
    purchase_order_received = models.ForeignKey(EngageboostPurchaseOrdersReceived,blank=True, null=True, on_delete=models.CASCADE, related_name="purchase_order_received_product")
    product = models.ForeignKey(EngageboostProducts,blank=True, null=True, on_delete=models.CASCADE)
    price = models.FloatField(blank=True, null=True)
    discount = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    product_tax_price = models.FloatField(blank=True, null=True)
    discount_amount = models.FloatField(blank=True, null=True)
    tax_name = models.CharField(max_length=256, blank=True, null=True)
    tax_per = models.FloatField(blank=True, null=True)
    lot_no = models.CharField(max_length=255, blank=True, null=True)
    rec_no = models.CharField(max_length=255, blank=True, null=True)
    good_cond = models.IntegerField(blank=True, null=True)
    damage = models.IntegerField(blank=True, null=True)
    expiry_issue = models.IntegerField(blank=True, null=True)
    total_qty = models.IntegerField(blank=True, null=True)
    shortage = models.IntegerField(blank=True, null=True)
    invoice_qty = models.IntegerField(blank=True, null=True)
    manufact_date = models.DateField(blank=True, null=True)
    received_date = models.DateField(blank=True, null=True)
    standard_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    exp_issue=models.CharField(max_length=2,choices=exp_issue_choice,default='n')
    mrp_issue=models.CharField(max_length=2,choices=mrp_issue_choice,default='n')
    issues = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    good_received=models.CharField(max_length=2,choices=good_received_choice,default='n')
    ok_to_ship=models.CharField(max_length=2,choices=ok_to_ship_choice,default='n')
    class Meta:
        db_table = 'engageboost_purchase_order_received_products'

class EngageboostPurchaseOrdersPaymentMethods(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_purchase_orders_payment_methods'

class EngageboostPurchaseOrdersShippingMethods(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_purchase_orders_shipping_methods'

class EngageboostPermisions(models.Model):
    status_field = (
        ('1', '1'),
        ('0', '0')
    )
    name = models.CharField(max_length=250, blank=True, null=True)
    field_name = models.CharField(max_length=250, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=status_field,default='0')
    isblocked = models.CharField(max_length=2,choices=status_field,default='0')
    class Meta:
        db_table = 'engageboost_permisions'

class EngageboostPicklistProducts(models.Model):
    picklist_id = models.IntegerField(blank=True, null=True)
    shipment_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    shell_no = models.CharField(max_length=100, blank=True, null=True)
    batch_no = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_picklist_products'

class EngageboostPicklists(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    picklist_no = models.CharField(max_length=100, blank=True, null=True)
    trents_picklist_no = models.CharField(max_length=256, blank=True, null=True)
    barcode_id = models.CharField(max_length=100, blank=True, null=True)
    picked_by = models.IntegerField(blank=True, null=True)
    shipment_id = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_picklists'

class EngageboostPlanDetails(models.Model):
    plan_name = models.CharField(max_length=255, blank=True, null=True)
    plan_price = models.FloatField(blank=True, null=True)
    plan_commision = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    expiried = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_plan_details'

class EngageboostReceipeCategoryMasters(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    remote_image_upload_choice=(
        ('y', 'y'),
        ('n', 'n')
    )
    parent_id = models.IntegerField(blank=True, null=True)
    lft = models.IntegerField(blank=True, null=True)
    rght = models.IntegerField(blank=True, null=True)
    check_id = models.IntegerField(blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    thumb_image = models.CharField(max_length=255, blank=True, null=True)
    banner_image = models.CharField(max_length=255, blank=True, null=True)
    page_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    category_url = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    slug = models.TextField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isdeleted=models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked=models.CharField(max_length=2,choices=enum_choices,default='n')
    website_id = models.IntegerField(blank=True, null=True)
    remote_image_upload=models.CharField(max_length=2,choices=remote_image_upload_choice,default='n')
    class Meta:
        db_table = 'engageboost_receipe_category_masters'

class EngageboostRecipeCategories(models.Model):
    recipe_id = models.IntegerField(blank=True, null=True)
    recipe_category_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_recipe_categories'

class EngageboostRecipeIngradiants(models.Model):
    recipe_id = models.IntegerField(blank=True, null=True)
    ingradiant_value = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_recipe_ingradiants'

class EngageboostRecipeMasters(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    serve = models.CharField(max_length=255, blank=True, null=True)
    preparation = models.CharField(max_length=255, blank=True, null=True)
    cook = models.CharField(max_length=255, blank=True, null=True)
    direction = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    video = models.CharField(max_length=255, blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices,default='n')
    class Meta:
        db_table = 'engageboost_recipe_masters'

class EngageboostRecipeProducts(models.Model):
    recipe_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_recipe_products'

class EngageboostReconciliationFiles(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    file_type_choices=(
        ('excel', 'excel'),
        ('csv', 'csv')
    )
    name = models.CharField(max_length=500, blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_type=models.CharField(max_length=2,choices=file_type_choices,default='excel',)
    channel_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    isdeleted=models.CharField(max_length=2,choices=enum_choices,default='n')
    isblocked=models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_reconciliation_files'

class EngageboostRelatedProducts(models.Model):
    related_product_type_choice=(
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    # 1-> Related Product ,2-> Up Sell Product,3-> Cross Sell Product,4-> Associated Product,5-> Substitute Product
    product_id = models.IntegerField(blank=True, null=True)
    related_product_id = models.IntegerField(blank=True, null=True)
    related_product_type=models.CharField(max_length=2,choices=related_product_type_choice,default='1',)
    class Meta:
        db_table = 'engageboost_related_products'

class EngageboostReportCustomer(models.Model):
    date = models.DateField(blank=True, null=True)
    customer_name = models.CharField(max_length=45, blank=True, null=True)
    gross_amount = models.FloatField(blank=True, null=True)
    avg_order_price = models.FloatField(blank=True, null=True)
    shipping_amount = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    net_amount = models.FloatField(blank=True, null=True)
    cancelled_amount = models.FloatField(blank=True, null=True)
    cancelled_quantity = models.IntegerField(blank=True, null=True)
    total_sold = models.FloatField(blank=True, null=True)
    invoiced_amount = models.FloatField(blank=True, null=True)
    customer_email = models.CharField(max_length=255, blank=True, null=True)
    customer_mobile = models.CharField(max_length=45, blank=True, null=True)
    customer_city = models.CharField(max_length=45, blank=True, null=True)
    no_of_order = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_report_customer'

class EngageboostReportDate(models.Model):
    date = models.DateField(blank=True, null=True)
    gross_amount = models.FloatField(blank=True, null=True)
    avg_order_price = models.FloatField(blank=True, null=True)
    shipping_amount = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    cart_discount = models.FloatField(blank=True, null=True)
    net_amount = models.FloatField(blank=True, null=True)
    cancelled_amount = models.FloatField(blank=True, null=True)
    cancelled_quantity = models.IntegerField(blank=True, null=True)
    total_sold = models.FloatField(blank=True, null=True)
    no_of_order = models.IntegerField(blank=True, null=True)
    invoiced_amount = models.FloatField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_report_date'

class EngageboostReportLocation(models.Model):
    country_id = models.IntegerField(blank=True, null=True)
    country_name = models.CharField(max_length=255, blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    city_name = models.CharField(max_length=255, blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    state_name = models.CharField(max_length=255, blank=True, null=True)
    date = models.FloatField(blank=True, null=True)
    gross_amount = models.FloatField(blank=True, null=True)
    avg_order_price = models.FloatField(blank=True, null=True)
    shipping_amount = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    net_amount = models.FloatField(blank=True, null=True)
    cancelled_amount = models.FloatField(blank=True, null=True)
    cancelled_quantity = models.IntegerField(blank=True, null=True)
    total_sold = models.IntegerField(blank=True, null=True)
    no_of_order = models.IntegerField(blank=True, null=True)
    invoiced_amount = models.FloatField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_report_location'

class EngageboostReportOrder(models.Model):
    date = models.CharField(max_length=45, blank=True, null=True)
    gross_amount = models.FloatField(blank=True, null=True)
    avg_order_price = models.FloatField(blank=True, null=True)
    shipping_amount = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    cart_discount = models.FloatField(blank=True, null=True)
    net_amount = models.FloatField(blank=True, null=True)
    cancelled_amount = models.FloatField(blank=True, null=True)
    cancelled_quantity = models.FloatField(blank=True, null=True)
    total_sold = models.FloatField(blank=True, null=True)
    invoiced_amount = models.FloatField(blank=True, null=True)
    custom_order_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    no_of_order = models.IntegerField(blank=True, null=True)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    cat_name = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_report_order'

class EngageboostReportProduct(models.Model):
    date = models.DateField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    gross_amount = models.FloatField(blank=True, null=True)
    avg_order_price = models.FloatField(blank=True, null=True)
    shipping_amount = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    net_amount = models.FloatField(blank=True, null=True)
    cancelled_amount = models.FloatField(blank=True, null=True)
    cancelled_quantity = models.IntegerField(blank=True, null=True)
    total_sold = models.IntegerField(blank=True, null=True)
    no_of_order = models.IntegerField(blank=True, null=True)
    invoiced_amount = models.FloatField(blank=True, null=True)
    website_id = models.CharField(max_length=45, blank=True, null=True)
    cat_name = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_report_product'

class EngageboostShowroomManagers(models.Model):
    showroom_id = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    manager_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_showroom_managers'

class EngageboostShowroomMasters(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    showroom_name = models.CharField(max_length=100, blank=True, null=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=100, blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    text_color = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_showroom_masters'

class EngageboostSmsTypeContents(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    sms_type_choices=(
        ('t', 't'),
        ('ht', 'ht')
    )
    default_sms_type_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    sms_type=models.CharField(max_length=2,choices=sms_type_choices, default='t')
    sms_content_text = models.TextField(blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_sms_type_contents'

class EngageboostSmsTypeMasters(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_sms_type_masters'

class EngageboostTrentPicklists(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    trents_picklist_no = models.CharField(max_length=100, blank=True, null=True)
    isconfirmed=models.CharField(max_length=2,choices=enum_choices, default='n')
    is_sub_picklist = models.CharField(max_length=2,choices=enum_choices, default='n')
    picklist_status = models.CharField(max_length=20, blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    zone_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_trent_picklists'

class EngageboostTrentsPicklistProducts(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    sr_no = models.IntegerField(blank=True, null=True)
    trent_picklist = models.ForeignKey(EngageboostTrentPicklists,on_delete=models.CASCADE,blank=True, null=True, related_name='trents_picklist_products')
    product_id = models.IntegerField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    confirm_quantity = models.IntegerField(blank=True, null=True)
    variant = models.CharField(max_length=100, blank=True, null=True)
    uom = models.CharField(max_length=20, blank=True, null=True)
    unit_cost = models.FloatField(blank=True, null=True)
    pick_mrp = models.FloatField(blank=True, null=True)
    trent_unit_cost = models.FloatField(blank=True, null=True)
    trent_pick_mrp = models.FloatField(blank=True, null=True)
    product_tax_price = models.FloatField(blank=True, null=True)
    tax_percentage = models.FloatField(blank=True, null=True)
    tax_name = models.CharField(max_length=100, blank=True, null=True)
    stock_available=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_trents_picklist_products'

class EngageboostUnitMasters(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(default='1')
    unit_name = models.CharField(max_length=255, blank=True, null=True)
    unit_full_name = models.CharField(max_length=255, blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    createdby = models.IntegerField(default='0')
    updatedby = models.IntegerField(default='0')
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_unit_masters'

class EngageboostUnitRates(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    engageboost_company_website_id = models.BigIntegerField(blank=True, null=True)
    engageboost_unit_master_id = models.BigIntegerField(blank=True, null=True)
    engageboost_unit_master_rate_id = models.BigIntegerField(blank=True, null=True)
    unit_rate = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_unit_rates'

class EngageboostOTP(models.Model):
    mobile = models.CharField(max_length=11, blank=True, null=True)
    otp = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_otp'

class EngageboostStatePincodes(models.Model):
    country_id = models.IntegerField(blank=True, null=True)
    pin_code = models.CharField(max_length=50, blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_state_pincodes'

class EngageboostStorelocators(models.Model):
    is_emi_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    photo = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=15, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    latitude = models.CharField(max_length=15, blank=True, null=True)
    longitude = models.CharField(max_length=15, blank=True, null=True)
    is_emi=models.CharField(max_length=2,choices=is_emi_choices, default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    street_view = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_storelocators'

class EngageboostSuperadmins(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    susername = models.CharField(max_length=255, blank=True, null=True)
    spassword = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdelete=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_superadmins'

class EngageboostTwitterCredentials(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    auth_token = models.CharField(max_length=255, blank=True, null=True)
    auth_secret = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_twitter_credentials'

class EngageboostMysavelist(models.Model):
    isdeleted_status = (
        ('n', 'n'),
        ('y', 'y')
    )
    website_id = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    savelist_name = models.CharField(max_length=100, blank=True, null=True)
    product_ids = models.TextField(blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=isdeleted_status,default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_mysavelist'

class EngageboostNotificationReturn(models.Model):  
    banner_title = models.CharField(max_length=255, blank=True, null=True)
    send_to = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_notification_return'

class EngageboostRoleMenuPermissions(models.Model):
    add_choices=(
        ('Y', 'Y'),
        ('N', 'N')
    )
    import_field_choices=(
        ('0', '0'),
        ('1', '1')
    )
    role_id = models.BigIntegerField(blank=True, null=True)
    master_id = models.BigIntegerField(blank=True, null=True)
    add=models.CharField(max_length=2,choices=add_choices, default='N')
    edit=models.CharField(max_length=2,choices=add_choices, default='N')
    delete=models.CharField(max_length=2,choices=add_choices, default='N')
    view=models.CharField(max_length=2,choices=add_choices, default='N')
    block=models.CharField(max_length=2,choices=add_choices, default='N')
    import_field=models.CharField(max_length=2,choices=import_field_choices, default='0')
    export=models.CharField(max_length=2,choices=import_field_choices, default='0')
    shipping_processes=models.CharField(max_length=2,choices=import_field_choices, default='0')
    print=models.CharField(max_length=2,choices=import_field_choices, default='0')
    isdeleted=models.CharField(max_length=2,choices=import_field_choices, default='0')
    isblocked=models.CharField(max_length=2,choices=import_field_choices, default='0')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_role_menu_permissions'

class EngageboostSitemodules(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    image_small = models.CharField(max_length=255, blank=True, null=True)
    image_big = models.CharField(max_length=255, blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_sitemodules'

class EngageboostMarketplaceFtpCredentials(models.Model):
    channel_id = models.IntegerField(blank=True, null=True)
    host_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    portno = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    company_website_id = models.IntegerField(blank=True, null=True)
    vendor_code = models.CharField(max_length=50, blank=True, null=True)
    vendor_name = models.CharField(max_length=50)
    merchant_id = models.CharField(max_length=250, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_marketplace_ftp_credentials'

class EngageboostMarketplaceInventory(models.Model):
    status_CHOICES = (
        ('n', 'n'),
        ('y', 'y')
    )
    channel_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isdeleted = models.CharField(max_length=255,choices=status_CHOICES,default='n')
    isblocked = models.CharField(max_length=255,choices=status_CHOICES,default='n')
    class Meta:
        db_table = 'engageboost_marketplace_inventory'

class EngageboostMarketplaceInventoryPriceUpdate(models.Model):
    channel_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    update_type = models.CharField(max_length=50, blank=True, null=True)
    submission_id = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    error = models.CharField(max_length=50, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_marketplace_inventory_price_update'

class EngageboostRepricingRules(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    compete_action = models.CharField(max_length=250, blank=True, null=True)
    compete_value = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    compete_with = models.CharField(max_length=250, blank=True, null=True)
    no_competetion_value = models.CharField(max_length=255, blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n')
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n')
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_repricing_rules'

class EngageboostRepricingUpdateTrack(models.Model):
    product_id = models.IntegerField(blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    updated_price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_repricing_update_track'

class EngageboostSellerAccountTypes(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    account_type = models.CharField(max_length=255, blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_seller_account_types'

class EngageboostShippingErrorLogs(models.Model):
    shipping_method_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    error_text = models.TextField(blank=True, null=True)
    error_code = models.CharField(max_length=50, blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_shipping_error_logs'

class EngageboostShippingTableRateOrderAmount(models.Model):
    shipping_masters_setting_id = models.IntegerField(blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    state_id = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=50, blank=True, null=True)
    order_subtotal = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    shipping_price = models.FloatField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_shipping_table_rate_order_amount'

class EngageboostShippingTableRateWeight(models.Model):
    shipping_masters_setting_id = models.IntegerField(blank=True, null=True)
    start_weight = models.FloatField(blank=True, null=True)
    end_weight = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    cal_method = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_shipping_table_rate_weight'

class EngageboostShippingZipcodes(models.Model):
    zipcode = models.CharField(max_length=50, blank=True, null=True)
    shipping_method_id = models.SmallIntegerField(blank=True, null=True)
    routing_code = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_shipping_zipcodes'

class EngageboostUserAccounts(models.Model):
    account_type_id = models.IntegerField(blank=True, null=True)
    engageboost_user_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_user_accounts'

class EngageboostUserLoginDetails(models.Model):
    user_id = models.BigIntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=255,blank=True, null=True)
    in_time = models.DateTimeField(blank=True, null=True)
    out_time = models.DateTimeField(blank=True, null=True)
    city_name = models.CharField(max_length=255, blank=True, null=True)
    country_name = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_user_login_details'

class EngageboostUserPlanDetails(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    plan_id = models.BigIntegerField(blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    emailid = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    renewal = models.DateField(blank=True, null=True)
    payment_status=models.CharField(max_length=2,choices=enum_choices, default='n')
    payment_date = models.DateField(blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_user_plan_details'

class EngageboostUserSuggestions(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    review = models.TextField(blank=True, null=True)
    reviewby = models.CharField(max_length=222, blank=True, null=True)
    reviewdate = models.DateTimeField(blank=True, null=True)
    customerid = models.IntegerField(blank=True, null=True)
    reviewrate = models.IntegerField(blank=True, null=True)
    reviewtitle = models.CharField(max_length=222, blank=True, null=True)
    want_to_refer=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_user_suggestions'

class EngageboostUserWebsites(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    engageboost_user_id = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    website_url = models.CharField(max_length=255, blank=True, null=True)
    websitename = models.CharField(max_length=255, blank=True, null=True)
    engageboost_category_master_id = models.IntegerField(blank=True, null=True)
    engageboost_template_master_id = models.IntegerField(blank=True, null=True)
    engageboost_template_color_master_id = models.IntegerField(blank=True, null=True)
    website_logo = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_user_websites'

class EngageboostUspsMatrix(models.Model):
    service_id = models.IntegerField(blank=True, null=True)
    package_id = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    container = models.CharField(max_length=255, blank=True, null=True)
    machinable = models.CharField(max_length=255, blank=True, null=True)
    dimensions = models.CharField(max_length=255, blank=True, null=True)
    gith = models.CharField(max_length=255, blank=True, null=True)
    ship_date = models.CharField(max_length=255, blank=True, null=True)
    max_weight = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_usps_matrix'

class EngageboostVehicleMasters(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    vehicle_name = models.CharField(max_length=256, blank=True, null=True)
    vehicle_number = models.CharField(max_length=255, blank=True, null=True)
    vehicle_description = models.TextField(blank=True, null=True)
    manager_id = models.CharField(max_length=255, blank=True, null=True)
    zone_ids = models.CharField(max_length=255, blank=True, null=True)
    warehouse_ids = models.CharField(max_length=255, blank=True, null=True)
    model_no = models.CharField(max_length=256, blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    zip_code = models.CharField(max_length=11, blank=True, null=True)
    address2 = models.CharField(max_length=500, blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    state_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    address1 = models.CharField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    no_of_orders = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_vehicle_masters'

class EngageboostVendorSkus(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    vender_id = models.IntegerField(blank=True, null=True)
    vender_sku = models.CharField(max_length=100, blank=True, null=True)
    isdeleted = models.SmallIntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_vender_skus'

class EngageboostVisitContacts(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    telph = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    msg = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    user_id = models.IntegerField(default='0',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_visit_contacts'

class EngageboostTallyCronSettings(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    time_interval = models.CharField(max_length=256, blank=True, null=True)
    is_order=models.CharField(max_length=2,choices=enum_choices, default='n')
    is_po=models.CharField(max_length=2,choices=enum_choices, default='n')
    is_inventory=models.CharField(max_length=2,choices=enum_choices, default='n')
    channel_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_tally_cron_settings'

class EngageboostSnapdealCategories(models.Model):
    category_label = models.CharField(max_length=255, blank=True, null=True)
    category_name = models.CharField(max_length=255, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    categorylevel = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_snapdeal_categories'

class EngageboostSnapdealImageRefs(models.Model):
    product_id = models.IntegerField(blank=True, null=True)
    image_id = models.IntegerField(blank=True, null=True)
    snapdeal_image_ref = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_snapdeal_image_refs'

class EngageboostSnapdealOrderCancelReturns(models.Model):
    order_id = models.IntegerField(blank=True, null=True)
    packagereferencecode = models.CharField(max_length=255, blank=True, null=True)
    suborder_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    error = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    downloadlink = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_snapdeal_order_cancel_returns'

class EngageboostSnapdealOrderDetails(models.Model):
    packagereferencecode = models.CharField(max_length=250, blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    fulfillmentmodelcode = models.CharField(max_length=250, blank=True, null=True)
    awbno = models.CharField(max_length=250, blank=True, null=True)
    couriercode = models.CharField(max_length=250, blank=True, null=True)
    manifestbydate = models.CharField(max_length=250, blank=True, null=True)
    manifestcode = models.CharField(max_length=250, blank=True, null=True)
    slabreach = models.CharField(max_length=250, blank=True, null=True)
    subordercode = models.CharField(max_length=250, blank=True, null=True)
    orderdate = models.DateTimeField(blank=True, null=True)
    productname = models.CharField(max_length=250, blank=True, null=True)
    serializable = models.CharField(max_length=250, blank=True, null=True)
    serializeduniqueid = models.CharField(max_length=250, blank=True, null=True)
    attributes = models.CharField(max_length=250, blank=True, null=True)
    imageurl = models.CharField(max_length=250, blank=True, null=True)
    freebies = models.CharField(max_length=250, blank=True, null=True)
    incentive = models.CharField(max_length=250, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    sistatuscode = models.CharField(max_length=250, blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    paymentmode = models.CharField(max_length=250, blank=True, null=True)
    supc = models.CharField(max_length=250, blank=True, null=True)
    fulfillmentmodelcodeorder = models.CharField(max_length=250, blank=True, null=True)
    skucode = models.CharField(max_length=250, blank=True, null=True)
    sireferencecode = models.CharField(max_length=250, blank=True, null=True)
    customername = models.CharField(max_length=250, blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    area = models.CharField(max_length=250, blank=True, null=True)
    subarea = models.CharField(max_length=250, blank=True, null=True)
    deliverymode = models.CharField(max_length=250, blank=True, null=True)
    stateformrequired = models.CharField(max_length=250, blank=True, null=True)
    invoicenumber = models.CharField(max_length=250, blank=True, null=True)
    centrecode = models.CharField(max_length=250, blank=True, null=True)
    centrename = models.CharField(max_length=250, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_snapdeal_order_details'

class EngageboostSnapdealOrders(models.Model):
    order_id = models.IntegerField(blank=True, null=True)
    order_code = models.CharField(max_length=100, blank=True, null=True)
    sub_order_code = models.CharField(max_length=100, blank=True, null=True)
    reference_code = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_snapdeal_orders'

class EngageboostSnapdealUploadIdTrack(models.Model):
    upload_id = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    supc = models.CharField(max_length=255, blank=True, null=True)
    request_id = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_snapdeal_upload_id_track'

class EngageboostMerchantoneReturnDetails(models.Model):
    response_status = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3')
    )
    website_id = models.IntegerField(blank=True, null=True)
    transaction_id = models.CharField(max_length=20, blank=True, null=True)
    order_id = models.CharField(max_length=10, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=4, blank=True, null=True)
    response = models.CharField(max_length=2,choices=response_status, blank=True, null=True)
    responsetext = models.CharField(max_length=50, blank=True, null=True)
    authcode = models.IntegerField(blank=True, null=True)
    avsresponse = models.CharField(max_length=4, blank=True, null=True)
    avsresponse_code = models.CharField(max_length=100, blank=True, null=True)
    cvvresponse = models.CharField(max_length=4, blank=True, null=True)
    cvvresponse_code = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    response_code = models.IntegerField(blank=True, null=True)
    response_code_string = models.CharField(max_length=100, blank=True, null=True)
    customer_vault_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_merchantone_return_details'

class EngageboostNetazeptReturnDetails(models.Model):
    status = models.CharField(max_length=10, blank=True, null=True)
    card_transaction_id = models.IntegerField(blank=True, null=True)
    card_response = models.CharField(max_length=10, blank=True, null=True)
    payment_url = models.CharField(max_length=50, blank=True, null=True)
    merchant_id = models.CharField(max_length=25, blank=True, null=True)
    merchant_token = models.CharField(max_length=25, blank=True, null=True)
    auth_uri = models.CharField(max_length=255, blank=True, null=True)
    auth_id = models.CharField(max_length=25, blank=True, null=True)
    auth_response = models.CharField(max_length=10, blank=True, null=True)
    auth_execution_time = models.DateTimeField(blank=True, null=True)
    query1_uri = models.CharField(max_length=255, blank=True, null=True)
    query1_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    query1_execution_time = models.DateTimeField(blank=True, null=True)
    capture_uri = models.CharField(max_length=255, blank=True, null=True)
    capture_transaction_id = models.CharField(max_length=25, blank=True, null=True)
    capture_response = models.CharField(max_length=10, blank=True, null=True)
    capture_execution_time = models.DateTimeField(blank=True, null=True)
    query2_uri = models.CharField(max_length=255, blank=True, null=True)
    query2_order_id = models.CharField(max_length=10, blank=True, null=True)
    query2_execution_time = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_netazept_return_details'

class EngageboostPaypalExpresscheckoutDoReturnDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    token = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.CharField(max_length=50, blank=True, null=True)
    correlationid = models.CharField(max_length=50, blank=True, null=True)
    ack = models.CharField(max_length=50, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    build = models.CharField(max_length=50, blank=True, null=True)
    transactionid = models.CharField(max_length=50, blank=True, null=True)
    transactiontype = models.CharField(max_length=50, blank=True, null=True)
    paymenttype = models.CharField(max_length=50, blank=True, null=True)
    ordertime = models.CharField(max_length=50, blank=True, null=True)
    amt = models.CharField(max_length=50, blank=True, null=True)
    taxamt = models.CharField(max_length=50, blank=True, null=True)
    currencycode = models.CharField(max_length=50, blank=True, null=True)
    paymentstatus = models.CharField(max_length=50, blank=True, null=True)
    pendingreason = models.CharField(max_length=50, blank=True, null=True)
    reasoncode = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_paypal_expresscheckout_do_return_details'

class EngageboostPaypalExpresscheckoutGetReturnDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    token = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.CharField(max_length=50, blank=True, null=True)
    correlationid = models.CharField(max_length=50, blank=True, null=True)
    ack = models.CharField(max_length=50, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    build = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    payerid = models.CharField(max_length=50, blank=True, null=True)
    payerstatus = models.CharField(max_length=50, blank=True, null=True)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    countrycode = models.CharField(max_length=50, blank=True, null=True)
    shiptoname = models.CharField(max_length=50, blank=True, null=True)
    shiptostreet = models.CharField(max_length=50, blank=True, null=True)
    shiptostreet2 = models.CharField(max_length=50, blank=True, null=True)
    shiptocity = models.CharField(max_length=50, blank=True, null=True)
    shiptostate = models.CharField(max_length=50, blank=True, null=True)
    shiptozip = models.CharField(max_length=50, blank=True, null=True)
    shiptocountrycode = models.CharField(max_length=50, blank=True, null=True)
    shiptocountryname = models.CharField(max_length=50, blank=True, null=True)
    addressstatus = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_paypal_expresscheckout_get_return_details'

class EngageboostPaypalExpresscheckoutReturnDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    transaction_subject = models.TextField(blank=True, null=True)
    payment_date = models.CharField(max_length=200, blank=True, null=True)
    txn_type = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    residence_country = models.CharField(max_length=50, blank=True, null=True)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    payment_gross = models.FloatField(blank=True, null=True)
    mc_currency = models.CharField(max_length=50, blank=True, null=True)
    business = models.CharField(max_length=255, blank=True, null=True)
    payment_type = models.CharField(max_length=50, blank=True, null=True)
    protection_eligibility = models.CharField(max_length=50, blank=True, null=True)
    payer_status = models.CharField(max_length=50, blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    payer_email = models.CharField(max_length=255, blank=True, null=True)
    txn_id = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    receiver_email = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    payer_id = models.CharField(max_length=255, blank=True, null=True)
    receiver_id = models.CharField(max_length=255, blank=True, null=True)
    item_number = models.IntegerField(blank=True, null=True)
    handling_amount = models.FloatField(blank=True, null=True)
    payment_status = models.CharField(max_length=100, blank=True, null=True)
    payment_fee = models.FloatField(blank=True, null=True)
    mc_fee = models.FloatField(blank=True, null=True)
    shipping = models.FloatField(blank=True, null=True)
    mc_gross = models.FloatField(blank=True, null=True)
    custom = models.CharField(max_length=255, blank=True, null=True)
    charset = models.CharField(max_length=255, blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_paypal_expresscheckout_return_details'

class EngageboostPaypalproReturnDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    order_id = models.TextField(blank=True, null=True)
    timestamp = models.TextField(blank=True, null=True)
    correlationid = models.TextField(blank=True, null=True)
    ack = models.CharField(max_length=50, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    build = models.CharField(max_length=50, blank=True, null=True)
    amt = models.FloatField(blank=True, null=True)
    currencycode = models.CharField(max_length=50, blank=True, null=True)
    avscode = models.CharField(max_length=50, blank=True, null=True)
    cvv2match = models.CharField(max_length=50, blank=True, null=True)
    transactionid = models.TextField(blank=True, null=True)
    l_errorcode = models.TextField(blank=True, null=True)
    l_shortmessage = models.TextField(blank=True, null=True)
    l_serveritycode = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_paypalpro_return_details'

class EngageboostPaypalstdReturnDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    transaction_subject = models.TextField(blank=True, null=True)
    payment_date = models.CharField(max_length=200, blank=True, null=True)
    txn_type = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    residence_country = models.CharField(max_length=50, blank=True, null=True)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    payment_gross = models.FloatField(blank=True, null=True)
    mc_currency = models.CharField(max_length=50, blank=True, null=True)
    business = models.CharField(max_length=255, blank=True, null=True)
    payment_type = models.CharField(max_length=50, blank=True, null=True)
    protection_eligibility = models.CharField(max_length=50, blank=True, null=True)
    payer_status = models.CharField(max_length=50, blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    payer_email = models.CharField(max_length=255, blank=True, null=True)
    txn_id = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    receiver_email = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    payer_id = models.CharField(max_length=255, blank=True, null=True)
    receiver_id = models.CharField(max_length=255, blank=True, null=True)
    item_number = models.IntegerField(blank=True, null=True)
    handling_amount = models.FloatField(blank=True, null=True)
    payment_status = models.CharField(max_length=100, blank=True, null=True)
    payment_fee = models.FloatField(blank=True, null=True)
    mc_fee = models.FloatField(blank=True, null=True)
    shipping = models.FloatField(blank=True, null=True)
    mc_gross = models.FloatField(blank=True, null=True)
    custom = models.CharField(max_length=255, blank=True, null=True)
    charset = models.CharField(max_length=255, blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_paypalstd_return_details'

class EngageboostPaytmApiTracking(models.Model):
    api_for = models.CharField(max_length=255, blank=True, null=True)
    request_data = models.TextField(blank=True, null=True)
    response_data = models.TextField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    order_id = models.BigIntegerField(blank=True, null=True)
    order_item_id = models.CharField(max_length=255, blank=True, null=True)
    error_message = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_paytm_api_tracking'

class EngageboostPaytmItemTransactions(models.Model):
    order_id = models.IntegerField(blank=True, null=True)
    paytm_order_id = models.CharField(max_length=255, blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    paytm_item_id = models.CharField(max_length=250, blank=True, null=True)
    product_title = models.CharField(max_length=255, blank=True, null=True)
    product_price = models.FloatField(blank=True, null=True)
    product_quantity = models.IntegerField(blank=True, null=True)
    currency_code = models.CharField(max_length=111, blank=True, null=True)
    shipping_currency = models.CharField(max_length=111, blank=True, null=True)
    shipping_price = models.FloatField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_paytm_item_transactions'

class EngageboostPaytmOrderProcess(models.Model):
    boost_order_id = models.BigIntegerField(blank=True, null=True)
    boost_shipment_id = models.BigIntegerField(blank=True, null=True)
    paytm_order_id = models.CharField(max_length=100, blank=True, null=True)
    paytm_item_id = models.CharField(max_length=100, blank=True, null=True)
    request_data = models.TextField(blank=True, null=True)
    response_data = models.TextField(blank=True, null=True)
    reponse_useful_data = models.CharField(max_length=255, blank=True, null=True)
    api_for = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_paytm_order_process'

class EngageboostPaytmOrderTransactions(models.Model):
    boost_order_id = models.IntegerField(blank=True, null=True)
    order_id = models.CharField(max_length=255, blank=True, null=True)
    merchant_id = models.CharField(max_length=255, blank=True, null=True)
    item_id = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=250, blank=True, null=True)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    qty_ordered = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    paytm_product_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    ship_by_date = models.DateTimeField(blank=True, null=True)
    fulfillment_id = models.IntegerField(blank=True, null=True)
    fulfillment_req = models.CharField(max_length=50, blank=True, null=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shipping_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fulfillment_service = models.CharField(max_length=50, blank=True, null=True)
    custom_text1 = models.CharField(max_length=255, blank=True, null=True)
    fulfillment_mode = models.CharField(max_length=10, blank=True, null=True)
    ack_by = models.DateTimeField(blank=True, null=True)
    bulk_pricing = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    iscod = models.IntegerField(blank=True, null=True)
    isrefundattempted = models.IntegerField(blank=True, null=True)
    islmd = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_paytm_order_transactions'

class EngageboostPaytmProductDetails(models.Model):
    status_field = (
        ('Active', 'Active'),
        ('Inctive', 'Inctive')
    )
    status_field = (
        ('Active', 'Active'),
        ('Inctive', 'Inctive')
    )
    boost_product_id = models.IntegerField(blank=True, null=True)
    paytm_product_id = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    mrp = models.FloatField(blank=True, null=True)
    currency_code = models.CharField(max_length=255, blank=True, null=True)
    merchant_sku = models.CharField(max_length=255, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=2,choices=status_field,default='Active')
    vertical_id = models.CharField(max_length=200, blank=True, null=True)
    paytm_sku = models.CharField(max_length=255, blank=True, null=True)
    complex_product_id = models.CharField(max_length=255, blank=True, null=True)
    weight = models.CharField(max_length=255, blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    brand_id = models.CharField(max_length=255, blank=True, null=True)
    merchant_id = models.CharField(max_length=255, blank=True, null=True)
    max_dispatch_time = models.CharField(max_length=100, blank=True, null=True)
    offer_tag = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    search_keyword = models.CharField(max_length=255, blank=True, null=True)
    category_id = models.CharField(max_length=255, blank=True, null=True)
    dimensions = models.CharField(max_length=255, blank=True, null=True)
    url_key = models.CharField(max_length=500, blank=True, null=True)
    return_policy_id = models.IntegerField(blank=True, null=True)
    shipping_charge = models.FloatField(blank=True, null=True)
    thumbnail = models.TextField(blank=True, null=True)
    fulfillment_service = models.CharField(max_length=255, blank=True, null=True)
    validate = models.CharField(max_length=100, blank=True, null=True)
    salesforce_case_id = models.CharField(max_length=255, blank=True, null=True)
    convfee_id = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    category_path = models.TextField(blank=True, null=True)
    sf_1 = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    cod = models.CharField(max_length=100, blank=True, null=True)
    cc = models.CharField(max_length=100, blank=True, null=True)
    dc = models.CharField(max_length=100, blank=True, null=True)
    nb = models.CharField(max_length=100, blank=True, null=True)
    escrow = models.CharField(max_length=100, blank=True, null=True)
    ppi = models.CharField(max_length=100, blank=True, null=True)
    emi = models.CharField(max_length=100, blank=True, null=True)
    diy_info = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    template_id = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_paytm_product_details'

class EngageboostPaytmReturnDetails(models.Model):
    order_id = models.IntegerField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    transaction_amount = models.FloatField(blank=True, null=True)
    currency_mode = models.CharField(max_length=10, blank=True, null=True)
    transaction_id = models.CharField(max_length=50, blank=True, null=True)
    bank_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    response_code = models.CharField(max_length=10, blank=True, null=True)
    response_message = models.CharField(max_length=200, blank=True, null=True)
    gateway_name = models.CharField(max_length=20, blank=True, null=True)
    bank_name = models.CharField(max_length=50, blank=True, null=True)
    payment_mode = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_paytm_return_details'

class EngageboostPayupaisaReturnDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    mihpayid = models.TextField(blank=True, null=True)
    mode = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    unmappedstatus = models.TextField(blank=True, null=True)
    firstname = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    field1 = models.TextField(blank=True, null=True)
    field2 = models.TextField(blank=True, null=True)
    field3 = models.TextField(blank=True, null=True)
    field4 = models.TextField(blank=True, null=True)
    field5 = models.TextField(blank=True, null=True)
    field6 = models.TextField(blank=True, null=True)
    field7 = models.TextField(blank=True, null=True)
    field8 = models.TextField(blank=True, null=True)
    field9 = models.TextField(blank=True, null=True)
    pg_type = models.TextField(blank=True, null=True)
    bank_ref_num = models.TextField(blank=True, null=True)
    bankcode = models.TextField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    name_on_card = models.TextField(blank=True, null=True)
    cardnum = models.TextField(blank=True, null=True)
    cardhash = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_payupaisa_return_details'

class EngageboostPaywithamazonReturnDetails(models.Model):
    order_id = models.IntegerField(blank=True, null=True)
    amznpmtsorderids = models.CharField(max_length=255, blank=True, null=True)
    amznpmtsreqid = models.CharField(max_length=255, blank=True, null=True)
    amznpagesource = models.CharField(max_length=255, blank=True, null=True)
    amznpmtsyalink = models.CharField(max_length=255, blank=True, null=True)
    amznpmtspaymentstatus = models.CharField(max_length=255, blank=True, null=True)
    amznpmtsdate = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_paywithamazon_return_details'

class EngageboostReturnDetails(models.Model):
    order_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    return_id = models.IntegerField(blank=True, null=True)
    return_type = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_return_details'

class EngageboostSagepayReturnDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    status_detail = models.CharField(max_length=255, blank=True, null=True)
    vendor_tx_code = models.TextField(blank=True, null=True)
    vps_tx_id = models.TextField(blank=True, null=True)
    tx_auth_no = models.IntegerField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    avscv2 = models.CharField(max_length=30, blank=True, null=True)
    address_result = models.CharField(max_length=30, blank=True, null=True)
    post_code_result = models.CharField(max_length=30, blank=True, null=True)
    cv2_result = models.CharField(max_length=30, blank=True, null=True)
    gift_aid = models.IntegerField(blank=True, null=True)
    d_secure_status = models.CharField(max_length=30, blank=True, null=True)
    cavv = models.CharField(max_length=100, blank=True, null=True)
    card_type = models.CharField(max_length=30, blank=True, null=True)
    last4_digits = models.IntegerField(blank=True, null=True)
    address_status = models.IntegerField(blank=True, null=True)
    payer_status = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_sagepay_return_details'

class EngageboostSnapmintReturnDetails(models.Model):
    order_id = models.CharField(max_length=50, blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    merchant_id = models.IntegerField(blank=True, null=True)
    snapmint_id = models.CharField(max_length=50, blank=True, null=True)
    order_value = models.FloatField(blank=True, null=True)
    discount_code = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    emi_amount = models.FloatField(blank=True, null=True)
    subvention_fees = models.FloatField(blank=True, null=True)
    tenure = models.IntegerField(blank=True, null=True)
    down_payment_amt = models.FloatField(blank=True, null=True)
    processing_fees = models.FloatField(blank=True, null=True)
    down_payment_status = models.CharField(max_length=20, blank=True, null=True)
    emi_starts_from = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_snapmint_return_details'

class EngageboostUsaepayReturnDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    umversion = models.CharField(max_length=50, blank=True, null=True)
    umstatus = models.CharField(max_length=50, blank=True, null=True)
    umauthcode = models.CharField(max_length=50, blank=True, null=True)
    umrefnum = models.CharField(max_length=50, blank=True, null=True)
    umavsresult = models.CharField(max_length=50, blank=True, null=True)
    umavsresultcode = models.CharField(max_length=50, blank=True, null=True)
    umcvv2result = models.CharField(max_length=50, blank=True, null=True)
    umcvv2resultcode = models.CharField(max_length=50, blank=True, null=True)
    umresult = models.CharField(max_length=50, blank=True, null=True)
    umvpasresultcode = models.CharField(max_length=50, blank=True, null=True)
    umerror = models.CharField(max_length=50, blank=True, null=True)
    umerrorcode = models.CharField(max_length=50, blank=True, null=True)
    umcustnum = models.CharField(max_length=50, blank=True, null=True)
    umbatch = models.CharField(max_length=50, blank=True, null=True)
    umbatchrefnum = models.CharField(max_length=50, blank=True, null=True)
    umisduplicate = models.CharField(max_length=50, blank=True, null=True)
    umconvertedamount = models.CharField(max_length=50, blank=True, null=True)
    umconvertedamountcurrency = models.CharField(max_length=50, blank=True, null=True)
    umconversionrate = models.CharField(max_length=50, blank=True, null=True)
    umcustreceiptresult = models.CharField(max_length=50, blank=True, null=True)
    umprocrefnum = models.CharField(max_length=50, blank=True, null=True)
    umcardlevelresult = models.CharField(max_length=50, blank=True, null=True)
    umauthamount = models.CharField(max_length=50, blank=True, null=True)
    umfiller = models.CharField(max_length=50, blank=True, null=True)
    umcctransid = models.CharField(max_length=50, blank=True, null=True)
    umacsurl = models.CharField(max_length=50, blank=True, null=True)
    umpayload = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_usaepay_return_details'

class EngageboostWorldpayReturnDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    orderkey = models.CharField(max_length=50, blank=True, null=True)
    paymentstatus = models.CharField(max_length=50, blank=True, null=True)
    paymentamount = models.CharField(max_length=50, blank=True, null=True)
    paymentcurrency = models.CharField(max_length=50, blank=True, null=True)
    mac = models.CharField(max_length=50, blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True)
    order_id = models.CharField(max_length=50, blank=True, null=True)
    transid = models.CharField(max_length=50, blank=True, null=True)
    transstatus = models.CharField(max_length=50, blank=True, null=True)
    transtime = models.CharField(max_length=50, blank=True, null=True)
    authamount = models.CharField(max_length=50, blank=True, null=True)
    authcost = models.CharField(max_length=50, blank=True, null=True)
    authcurrency = models.CharField(max_length=50, blank=True, null=True)
    authamountstring = models.CharField(max_length=50, blank=True, null=True)
    rawauthmessage = models.CharField(max_length=50, blank=True, null=True)
    rawauthcode = models.CharField(max_length=50, blank=True, null=True)
    callbackpw = models.CharField(max_length=50, blank=True, null=True)
    cardtype = models.CharField(max_length=50, blank=True, null=True)
    countrymatch = models.CharField(max_length=50, blank=True, null=True)
    avs = models.CharField(max_length=50, blank=True, null=True)
    wafmerchmessage = models.CharField(max_length=50, blank=True, null=True)
    authentication = models.CharField(max_length=50, blank=True, null=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    charenc = models.CharField(max_length=50, blank=True, null=True)
    s_spcharenc = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_worldpay_return_details'

class EngageboostPriceFormula(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    formulla_choices=(
        ('customer', 'customer'),
        ('vendor', 'vendor')
    )
    website_id = models.IntegerField(blank=True, default='1', null=True)
    formulla_name = models.CharField(max_length=255, blank=True, null=True)
    price_name = models.CharField(max_length=255, blank=True, null=True)
    condition = models.CharField(max_length=100, blank=True, null=True)
    margin = models.IntegerField(blank=True, null=True)
    formulla_type = models.CharField(max_length=20,choices=formulla_choices,default='customer',blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_price_formulas'

class EngageboostTempMultipleBarcodes(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )

    sku = models.CharField(max_length=255, blank=True, null=True)
    barcode = models.CharField(max_length=255, blank=True, null=True)
    default_ean = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    file_name = models.CharField(max_length=255,blank=True, null=True)
    err_flag = models.IntegerField(blank=True, null=True)
    error_text = models.CharField(max_length=255 ,blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    modifiedby = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_temp_multiple_barcodes'

class EngageboostMultipleBarcodes(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )

    product = models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE,blank=True, null=True, related_name='barcode_product_id')
    barcode = models.CharField(max_length=255, blank=True, null=True)
    default_ean = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    modifiedby = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_multiple_barcodes'

class EngageboostOrderPaymentDetails(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )

    order_id = models.ForeignKey(EngageboostOrdermaster,on_delete=models.CASCADE,blank=True, null=True, related_name='paymeny_order_details')
    payment_method_id = models.IntegerField(blank=True, null=True)
    payment_type_id = models.IntegerField(blank=True, null=True)
    payment_method_name = models.CharField(max_length=100, blank=True, null=True)
    payment_amount = models.FloatField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    modifiedby = models.IntegerField(blank=True, null=True)
    device_id = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_order_payment_details'

class EngageboostDenominationDetails(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )

    order_payment_details = models.ForeignKey(EngageboostOrderPaymentDetails,on_delete=models.CASCADE,blank=True, null=True, related_name='paymeny_denomination_details')
    currency_code = models.CharField(max_length=255, blank=True, null=True)
    payment_type_id = models.IntegerField(blank=True, null=True)
    payment_method_name = models.CharField(max_length=100, blank=True, null=True)
    currency_amount = models.FloatField(blank=True, null=True)
    currency_count = models.IntegerField(blank=True, null=True)
    total_amount = models.FloatField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    modifiedby = models.IntegerField(blank=True, null=True)
    device_id = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_denomination_details'

class EngageboostDenominationCurrencyMaster(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    country = models.ForeignKey(EngageboostCountries,on_delete=models.CASCADE, blank=True, null=True, related_name='denomination_currency_master')
    currency_value = models.IntegerField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    modifiedby = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_denomination_currency_master'


class EnagageboostAttemptedDeliveryDetails(models.Model):
    attempted_type_choices=(
        ('attempt', 'attempt'),
        ('delivered', 'delivered')
    )
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    shipment_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    delivery_attempted_date = models.DateTimeField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    additional_note = models.TextField(blank=True, null=True)
    new_delivery_date = models.DateTimeField(blank=True, null=True)
    attempted_type = models.CharField(max_length=20,choices=attempted_type_choices,blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    class Meta:
        db_table = 'enagageboost_attempted_delivery_details'

class EngageboostNotifyOrderArea(models.Model):
    order_id 	= models.IntegerField(blank=True, null=True)
    driver_id 	= models.IntegerField(blank=True, null=True)
    lat_val 	= models.CharField(max_length=100, blank=True, null=True)
    long_val 	= models.CharField(max_length=100, blank=True, null=True)
    created 	= models.DateTimeField(blank=True, null=True)
    modified 	= models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'engageboost_notify_order_area'

class EngageboostCategoryMastersLang(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    language_id 	= models.IntegerField(blank=True, null=True)
    language_code 	= models.CharField(max_length=20, blank=True, null=True)
    category_id 	= models.IntegerField(blank=True, null=True)
    field_name 		= models.CharField(max_length=100, blank=True, null=True)
    field_value 	= models.TextField(blank=True, null=True)
    created 		= models.DateTimeField(blank=True, null=True)
    modified 		= models.DateTimeField(blank=True, null=True)
    isblocked 		= models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted 		= models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_category_masters_lang'

####################ANJAN#######################
class EngageboostWarehouseSupplierMappings(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    warehouse = models.ForeignKey(EngageboostWarehouseMasters,on_delete=models.CASCADE, blank=True, null=True, related_name='warehousesupplier_warehouse')
    supplier = models.ForeignKey(EngageboostSuppliers,on_delete=models.CASCADE, blank=True, null=True, related_name='warehousesupplier_supplier')
    product = models.ForeignKey(EngageboostProducts,on_delete=models.CASCADE, blank=True, null=True, related_name='warehousesupplier_product')
    supplier_sku = models.CharField(max_length=255, blank=True, null=True)
    base_cost = models.FloatField(blank=True, null=True)
    sale_per_pack_unit = models.FloatField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    modifiedby = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_warehouse_supplier_mappings'

class EngageboostGiftCardMasters(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    card_number = models.CharField(max_length=100, blank=True, null=True)
    card_name = models.CharField(max_length=100, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    modifiedby = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    website_id = models.IntegerField(blank=True, null=True)
    isblocked = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted = models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_gift_card_masters'

####################ANJAN#######################

class EngageboostEmktFunnelPages(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    funnel_id = models.IntegerField(blank=True, null=True)
    landing_page_id=models.IntegerField(blank=True, null=True)
    landing_page_temp_id=models.IntegerField(blank=True, null=True)
    thankyou_page_id=models.IntegerField(blank=True, null=True)
    thankyou_page_temp_id=models.IntegerField(blank=True, null=True)
    company_website_id=models.IntegerField(blank=True, null=True)
    email_campaign_id=models.IntegerField(blank=True, null=True)
    campaign_type=models.CharField(max_length=255,blank=True, null=True)
    product_ids=models.CharField(max_length=255,blank=True, null=True)
    createdby = models.IntegerField(null=True)
    updatedby = models.IntegerField(null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked=models.CharField(max_length=2,choices=enum_choices, default='n')
    isdeleted=models.CharField(max_length=2,choices=enum_choices, default='n')
    class Meta:
        db_table = 'engageboost_emkt_funnel_page'


class EngageboostBrandMastersLang(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    language_id 	= models.IntegerField(blank=True, null=True)
    language_code 	= models.CharField(max_length=20, blank=True, null=True)
    brand_id 		= models.IntegerField(blank=True, null=True)
    field_name 		= models.CharField(max_length=100, blank=True, null=True)
    field_value 	= models.TextField(blank=True, null=True)
    created 		= models.DateTimeField(blank=True, null=True)
    modified 		= models.DateTimeField(blank=True, null=True)
    isblocked 		= models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted 		= models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_brand_masters_lang'


class EngageboostProductMastersLang(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    language_id 	= models.IntegerField(blank=True, null=True)
    language_code 	= models.CharField(max_length=20, blank=True, null=True)
    product_id 		= models.IntegerField(blank=True, null=True)
    field_name 		= models.CharField(max_length=100, blank=True, null=True)
    field_value 	= models.TextField(blank=True, null=True)
    created 		= models.DateTimeField(blank=True, null=True)
    modified 		= models.DateTimeField(blank=True, null=True)
    isblocked 		= models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted 		= models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_masters_lang'

class EngageboostCustomFieldMastersLang(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    language_id 	= models.IntegerField(blank=True, null=True)
    language_code 	= models.CharField(max_length=20, blank=True, null=True)
    field_id 		= models.IntegerField(blank=True, null=True)
    category_id 	= models.IntegerField(blank=True, null=True)
    field_name 		= models.CharField(max_length=100, blank=True, null=True)
    field_value 	= models.TextField(blank=True, null=True)
    field_lable_value 	= models.TextField(blank=True, null=True)
    created 		= models.DateTimeField(blank=True, null=True)
    modified 		= models.DateTimeField(blank=True, null=True)
    isblocked 		= models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted 		= models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_customfield_masters_lang'

class EngageboostProductCustomFieldMastersLang(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    language_id 	= models.IntegerField(blank=True, null=True)
    language_code 	= models.CharField(max_length=20, blank=True, null=True)
    product_id 		= models.IntegerField(blank=True, null=True)
    field_id 		= models.IntegerField(blank=True, null=True)
    field_name 		= models.CharField(max_length=100, blank=True, null=True)
    field_value 	= models.TextField(blank=True, null=True)
    field_lable_value 	= models.TextField(blank=True, null=True)
    created 		= models.DateTimeField(blank=True, null=True)
    modified 		= models.DateTimeField(blank=True, null=True)
    isblocked 		= models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    isdeleted 		= models.CharField(max_length=2,choices=enum_choices,default='n',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_product_customfield_masters_lang'

class EngageboostCategoryWarehouse(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    category = models.ForeignKey(EngageboostCategoryMasters,on_delete=models.CASCADE,blank=True, null=True)
    warehouse = models.ForeignKey(EngageboostWarehouseMasters,on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2, choices=enum_choices, default='n', blank=True, null=True)
    isdeleted = models.CharField(max_length=2, choices=enum_choices, default='n', blank=True, null=True)
    product_count = models.IntegerField(blank=True, null=True, default=0)
    class Meta:
        db_table = 'engageboost_category_warehouse'


class EngageboostStoreType(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    type = models.ForeignKey(EngageboostTemplateIndustryMasters,on_delete=models.CASCADE,blank=True, null=True)
    warehouse = models.ForeignKey(EngageboostWarehouseMasters,on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    modifiedby = models.IntegerField(blank=True, null=True)
    isblocked = models.CharField(max_length=2, choices=enum_choices, default='n', blank=True, null=True)
    isdeleted = models.CharField(max_length=2, choices=enum_choices, default='n', blank=True, null=True)
    class Meta:
        db_table = 'engageboost_store_type'


class EngageboostOrderPriceChange(models.Model):
    enum_choices=(
        ('y', 'y'),
        ('n', 'n')
    )
    website_id = models.IntegerField(blank=True, null=True,default=0)
    warehouse_id = models.IntegerField(blank=True, null=True,default=0)
    order_id = models.BigIntegerField(blank=True, null=True,default=0)
    product_id = models.IntegerField(blank=True, null=True,default=0)
    old_product_price = models.FloatField(default='0', blank=True, null=True)
    new_product_price = models.FloatField(default='0', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    user_id = models.IntegerField(default='0',blank=True, null=True)
    class Meta:
        db_table = 'engageboost_order_price_changes'

class EngageboostBrandWarehouse(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    brand = models.ForeignKey(EngageboostBrandMasters,on_delete=models.CASCADE,blank=True, null=True)
    warehouse = models.ForeignKey(EngageboostWarehouseMasters,on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    isblocked = models.CharField(max_length=2, choices=enum_choices, default='n', blank=True, null=True)
    isdeleted = models.CharField(max_length=2, choices=enum_choices, default='n', blank=True, null=True)
    class Meta:
        db_table = 'engageboost_brand_warehouse'


class EngageboostMastercardPgReturnDetails(models.Model):
    website_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    tracking_id = models.CharField(max_length=50, blank=True, null=True)
    bank_ref_no = models.CharField(max_length=50, blank=True, null=True)
    order_status = models.CharField(max_length=20,blank=True, null=True)
    failure_message = models.CharField(max_length=255, blank=True, null=True)
    payment_mode = models.CharField(max_length=100, blank=True, null=True)
    card_name = models.CharField(max_length=100, blank=True, null=True)
    status_code = models.CharField(max_length=100, blank=True, null=True)
    status_message = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=5,blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    billing_name = models.CharField(max_length=100, blank=True, null=True)
    billing_address = models.CharField(max_length=255, blank=True, null=True)
    billing_city = models.CharField(max_length=50, blank=True, null=True)
    billing_state = models.CharField(max_length=50, blank=True, null=True)
    billing_zip = models.IntegerField(blank=True, null=True)
    billing_country = models.CharField(max_length=50, blank=True, null=True)
    billing_tel = models.CharField(max_length=20, blank=True, null=True)
    billing_email = models.CharField(max_length=100, blank=True, null=True)
    delivery_name = models.CharField(max_length=100, blank=True, null=True)
    delivery_address = models.CharField(max_length=255, blank=True, null=True)
    delivery_city = models.CharField(max_length=50, blank=True, null=True)
    delivery_state = models.CharField(max_length=50, blank=True, null=True)
    delivery_zip = models.IntegerField(blank=True, null=True)
    delivery_country = models.CharField(max_length=50, blank=True, null=True)
    delivery_tel = models.CharField(max_length=20, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_mastercard_payment_gateway_return_details'


class EngageboostAppVersionControl(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    version_a = models.CharField(max_length=50, blank=True, null=True)
    version_i = models.CharField(max_length=50, blank=True, null=True)
    picking_android = models.CharField(max_length=50, blank=True, null=True)
    is_mandatory = models.CharField(max_length=5, choices=enum_choices, default='y', blank=True, null=True)
    appstore_check = models.CharField(max_length=5, choices=enum_choices, default='y', blank=True, null=True)
    upgrade_to = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'enageboost_app_version_control'

class EngageboostAllUserDeviceToken(models.Model):
    user_id = models.IntegerField(default='0',blank=True, null=True)
    device_id = models.CharField(max_length=255, blank=True, null=True)
    device_token = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    os_version = models.CharField(max_length=100, blank=True, null=True)
    device_type = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'enageboost_alluser_devicetoken'

class EngageboostSmsLog(models.Model):
    mobile_number = models.CharField(max_length=50, blank=True, null=True)
    sms_subject = models.CharField(max_length=256, blank=True, null=True)
    sms_content_text = models.TextField(blank=True, null=True)
    response_code = models.CharField(max_length=50, blank=True, null=True)
    response_text = models.CharField(max_length=256, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'enageboost_sms_log'


class EngageboostUserSIList(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    customer = models.ForeignKey(EngageboostCustomers,on_delete=models.CASCADE, blank=True, null=True)
    si_ref_no = models.CharField(max_length=50, blank=True, null=True)
    is_default = models.CharField(max_length=2, choices=enum_choices, default='y')
    isdeleted = models.CharField(max_length=2, choices=enum_choices, default='n')
    isblocked = models.CharField(max_length=2, choices=enum_choices, default='n')
    # customer = models.ForeignKey(EngageboostCustomers, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        db_table = 'engageboost_usersi_list'


class EngageboostProcessQueueMaster(models.Model):
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )

    TYPE = (
        ('price', 'price'),
        ('inventory', 'inventory'),
        ('image', 'image'),
        ('product', 'product'),
        ('discount', 'discount')
    )

    process_type = models.CharField(max_length=15, choices=TYPE, default='n')
    weight = models.IntegerField(default=0)
    pending_count = models.IntegerField(default=0)
    is_running = models.CharField(max_length=15, choices=enum_choices, default='n')
    modified_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    class Meta:
        db_table = 'engageboost_process_queue_master'


class EngageboostUpdateQueue(models.Model):
    STATE = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed')
    )
    UPLOAD_TYPE = (
        ('single', 'single'),
        ('bulk', 'bulk')
    )
    OPERATION_FOR = (
        ('price', 'price'),
        ('inventory', 'inventory'),
        ('image', 'image'),
        ('product', 'product'),
        ('discount', 'discount')
    )

    product = models.ForeignKey(EngageboostProducts, on_delete=models.CASCADE, blank=True, null=True)
    warehouse = models.ForeignKey(EngageboostWarehouseMasters,on_delete=models.CASCADE,blank=True, null=True)
    process_queue = models.ForeignKey(EngageboostProcessQueueMaster, on_delete=models.CASCADE, blank=True, null=True)
    discount = models.ForeignKey(EngageboostDiscountMasters, on_delete=models.CASCADE, blank=True, null=True)
    prev_products = models.TextField(blank=True, null=True)
    prev_warehouses = models.TextField(blank=True, null=True)
    process_state = models.CharField(max_length=15, choices=STATE, default='Pending')
    process_type = models.CharField(max_length=15, choices=UPLOAD_TYPE, default='bulk')
    operation_for = models.CharField(max_length=15, choices=OPERATION_FOR, default='price')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'engageboost_update_queue'

#Notes:- We are adding the model name which we are using in our projects, if you want to use any exising model then first add in log for tracking - CDS on 25th Jan 2019
# auditlog.register(EngageboostCategoryWarehouse)
# auditlog.register(EngageboostGiftCardMasters)
# auditlog.register(EngageboostRolemasters)
# auditlog.register(EngageboostCountries)
# auditlog.register(EngageboostStates)
# auditlog.register(EngageboostUsers)
# auditlog.register(EngageboostEmailTypeContents)
# auditlog.register(EngageboostApplicableAutoresponders)
# auditlog.register(EngageboostCustomerGroup)
# auditlog.register(EngageboostProductTaxClasses)
# auditlog.register(EngageboostWarehouseMasters)
# auditlog.register(EngageboostRepricingMaximumMinRules)
# auditlog.register(EngageboostHsnCodeMaster)
# auditlog.register(EngageboostProducts)
# auditlog.register(EngageboostCustomers)
# auditlog.register(EngageboostCustomersAddressBook)
# auditlog.register(EngageboostCustomerActivities)
# auditlog.register(EngageboostCustomerLoyaltypoints)
# auditlog.register(EngageboostCustomerReturnStatus)
# auditlog.register(EngageboostCustomerTaxClasses)
# auditlog.register(EngageboostChannels)
# auditlog.register(EngageboostChannelCategoryMappings)
# auditlog.register(EngageboostChannelCurrencyProductPrice)
# auditlog.register(EngageboostChannelErrors)
# auditlog.register(EngageboostChannelItemlistingfees)
# auditlog.register(EngageboostChannelOrdertransactions)
# auditlog.register(EngageboostChannelSettings)
# auditlog.register(EngageboostChannelShippingMaps)
# auditlog.register(EngageboostChannelShippingservices)
# auditlog.register(EngageboostChannelSites)
# auditlog.register(EngageboostChannelSku)
# auditlog.register(EngageboostChannelUsers)
# auditlog.register(EngageboostOrdermaster)
# auditlog.register(EngageboostOrderProducts)
# auditlog.register(EngageboostTempOrdermaster)
# auditlog.register(EngageboostShipments)
# auditlog.register(EngageboostShipmentOrders)
# auditlog.register(EngageboostShipmentOrderProducts)
# auditlog.register(EngageboostWishlists)
# auditlog.register(EngageboostWebsiteActivities)
# auditlog.register(EngageboostWebsiteChannelFieldValues)
# auditlog.register(EngageboostWebsiteChannels)
# auditlog.register(EngageboostAttemptedDeliveryDetails)
# auditlog.register(EngageboostCategoryMasters)
# auditlog.register(EngageboostCategoryBanners)
# auditlog.register(EngageboostCategoryBannersImages)
# auditlog.register(EngageboostBrandMasters)
# auditlog.register(EngageboostProductCategories)
# auditlog.register(EngageboostProductImeis)
# auditlog.register(EngageboostProductKeyTypes)
# auditlog.register(EngageboostProductMarketplaces)
# auditlog.register(EngageboostProductMoveTrack)
# auditlog.register(EngageboostProductPush)
# auditlog.register(EngageboostProductRatings)
# auditlog.register(EngageboostProductRepriceRule)
# auditlog.register(EngageboostProductReviews)
# auditlog.register(EngageboostProductStatus)
# auditlog.register(EngageboostProductStocks)
# auditlog.register(EngageboostProductStockCrons)
# auditlog.register(EngageboostProductTemplateMasters)
# auditlog.register(EngageboostProductTierPrice)
# auditlog.register(EngageboostProductVisibilities)
# auditlog.register(EngageboostProductimages)
# auditlog.register(EngageboostProductworksheetimages)
# auditlog.register(EngageboostOrderStatusMasters)
# auditlog.register(EngageboostReturnOrderImages)
# auditlog.register(EngageboostAffiliateContacts)
# auditlog.register(EngageboostChannelsCategoriesMaster)
# auditlog.register(EngageboostEmiSettings)
# auditlog.register(EngageboostOutofstockNotification)
# auditlog.register(EngageboostProductRateperpacks)
# auditlog.register(EngageboostRateperpacks)
# auditlog.register(EngageboostTallyLogs)
# auditlog.register(Engageboost2CheckoutReturnDetails)
# auditlog.register(EngageboostAccountChannels)
# auditlog.register(EngageboostAccountTypes)
# auditlog.register(EngageboostActivities)
# auditlog.register(EngageboostActivitySettings)
# auditlog.register(EngageboostAffiliateDetails)
# auditlog.register(EngageboostAmazonBoostCategories)
# auditlog.register(EngageboostAmazonCategories)
# auditlog.register(EngageboostAmazonCredentials)
# auditlog.register(EngageboostAmazonFeedReport)
# auditlog.register(EngageboostAmazonFeedStatus)
# auditlog.register(EngageboostAmazonFlatFileHeaders)
# auditlog.register(EngageboostAmazonItemTransactions)
# auditlog.register(EngageboostAmazonOrders)
# auditlog.register(EngageboostAmazonProductBulletpoints)
# auditlog.register(EngageboostAmazonebtg)
# auditlog.register(EngageboostAppCategory)
# auditlog.register(EngageboostAppMaster)
# auditlog.register(EngageboostAppReviews)
# auditlog.register(EngageboostAppWebsites)
# auditlog.register(EngageboostApplicableZipcodes)
# auditlog.register(EngageboostAppstores)
# auditlog.register(EngageboostAssetPaths)
# auditlog.register(EngageboostAtompaynetReturnurlDetails)
# auditlog.register(EngageboostAuthorizeNetReturnDetails)
# auditlog.register(EngageboostAutoProductUploads)
# auditlog.register(EngageboostAwbMasters)
# auditlog.register(EngageboostCcavenueReturnDetails)
# auditlog.register(EngageboostCcavenueUpgradedReturnDetails)
# auditlog.register(EngageboostAxisReturnDetails)
# auditlog.register(EngageboostCmsMenus)
# auditlog.register(EngageboostCmsPageSettings)
# auditlog.register(EngageboostCommissionSettings)
# auditlog.register(EngageboostCompanies)
# auditlog.register(EngageboostCompaniesCrons)
# auditlog.register(EngageboostCompanyAuthentication)
# auditlog.register(EngageboostCompanyWebsiteMap)
# auditlog.register(EngageboostCompanyWebsites)
# auditlog.register(EngageboostCossSellProducts)
# auditlog.register(EngageboostCrates)
# auditlog.register(EngageboostCreditcardSettingInformations)
# auditlog.register(EngageboostCreditcardTypes)
# auditlog.register(EngageboostCurrencyMasters)
# auditlog.register(EngageboostCurrencyRates)
# auditlog.register(EngageboostCustomEmails)
# auditlog.register(EngageboostCustomFields)
# auditlog.register(EngageboostCustomForms)
# auditlog.register(EngageboostCustomValues)
# auditlog.register(EngageboostDbWebsitehits)
# auditlog.register(EngageboostDbWebsitestats)
# auditlog.register(EngageboostDbWebsitevisitorshits)
# auditlog.register(EngageboostDefaultCategories)
# auditlog.register(EngageboostDefaultEmailTypeContents)
# auditlog.register(EngageboostDefaultModuleLayoutFields)
# auditlog.register(EngageboostDefaultModuleLayoutSections)
# auditlog.register(EngageboostDefaultModuleLayouts)
# auditlog.register(EngageboostDefaultsFields)
# auditlog.register(EngageboostDeliveryManagers)
# auditlog.register(EngageboostDeliveryPlanOrder)
# auditlog.register(EngageboostDeliverySlot)
# auditlog.register(EngageboostDhlZipcodeLists)
# auditlog.register(EngageboostDirecpayReturnDetails)
# auditlog.register(EngageboostDiscountMasters)
# auditlog.register(EngageboostTempDiscountMasters)
# auditlog.register(EngageboostDiscountMastersConditions)
# auditlog.register(EngageboostDiscountMastersCoupons)
# auditlog.register(EngageboostDriverLoginDetails)
# auditlog.register(EngageboostDriverVeichleMap)
# auditlog.register(EngageboostEbayBoostCategories)
# auditlog.register(EngageboostEbayItemSpecification)
# auditlog.register(EngageboostEbayItemSpecificationValue)
# auditlog.register(EngageboostEbayProductCondition)
# auditlog.register(EngageboostEbaystoreCategories)
# auditlog.register(EngageboostEmailTypeMasters)
# auditlog.register(EngageboostEmktCampaigns)
# auditlog.register(EngageboostEmktContactlists)
# auditlog.register(EngageboostEmktContacts)
# auditlog.register(EngageboostEmktPageVisitStat)
# auditlog.register(EngageboostEmktSegmentContactlists)
# auditlog.register(EngageboostEmktSegments)
# auditlog.register(EngageboostEmktSendmail)
# auditlog.register(EngageboostEmktTemplateMasters)
# auditlog.register(EngageboostEmktTemplatecategoryMasters)
# auditlog.register(EngageboostEmktWebsiteTemplates)
# auditlog.register(EngageboostFacebookProducts)
# auditlog.register(EngageboostFedexZipcodes)
# auditlog.register(EngageboostFeeMasters)
# auditlog.register(EngageboostFeeSettingMasters)
# auditlog.register(EngageboostFlipkartOrderTransactions)
# auditlog.register(EngageboostFlipkartReconciliations)
# auditlog.register(EngageboostFormulaDetails)
# auditlog.register(EngageboostFulfillments)
# auditlog.register(EngageboostGlobalSettings)
# auditlog.register(EngageboostGlobalsettingCountries)
# auditlog.register(EngageboostGlobalsettingCurrencies)
# auditlog.register(EngageboostGlobalsettingLanguages)
# auditlog.register(EngageboostGlobalsettingSitemodules)
# auditlog.register(EngageboostGooglecheckoutReturnDetails)
# auditlog.register(EngageboostGoogleshopCategories)
# auditlog.register(EngageboostGridLayouts)
# auditlog.register(EngageboostGridColumnLayouts)
# auditlog.register(EngageboostGroups)
# auditlog.register(EngageboostHdfcReturnDetails)
# auditlog.register(EngageboostIciciReturnDetails)
# auditlog.register(EngageboostHelpText)
# auditlog.register(EngageboostHolidaysMasters)
# auditlog.register(EngageboostImportErrorLog)
# auditlog.register(EngageboostImportMapFields)
# auditlog.register(EngageboostImportStockFiles)
# auditlog.register(EngageboostImportedTempProductStocks)
# auditlog.register(EngageboostInventoryMasters)
# auditlog.register(EngageboostInventoryProducts)
# auditlog.register(EngageboostInvoiceContainers)
# auditlog.register(EngageboostInvoicemaster)
# auditlog.register(EngageboostInvoiceProducts)
# auditlog.register(EngageboostMenuMasters)
# auditlog.register(EngageboostMenuShortcuts)
# auditlog.register(EngageboostLanguages)
# auditlog.register(EngageboostManifests)
# auditlog.register(EngageboostModuleLayouts)
# auditlog.register(EngageboostModules)
# auditlog.register(EngageboostJwelleryAppSettings)
# auditlog.register(EngageboostCreditPoint)
# auditlog.register(EngageboostCreditPointConditions)
# auditlog.register(EngageboostMappedCategories)
# auditlog.register(EngageboostMarketplaceManifestsFeedStatus)
# auditlog.register(EngageboostMarketplaceFieldLabels)
# auditlog.register(EngageboostMarketplaceFieldValue)
# auditlog.register(EngageboostWarehouseManager)
# auditlog.register(EngageboostWarehouseMasterApplicableChannels)
# auditlog.register(EngageboostWarehouseMasterApplicableRegions)
# auditlog.register(EngageboostZoneMasters)
# auditlog.register(EngageboostZoneZipcodeMasters)
# auditlog.register(EngageboostTrafficReports)
# auditlog.register(EngageboostTrafficReportsBrowsers)
# auditlog.register(EngageboostTrafficReportsMobiles)
# auditlog.register(EngageboostTrafficReportsPages)
# auditlog.register(EngageboostTrafficReportsSociales)
# auditlog.register(EngageboostTrafficReportsSources)
# auditlog.register(EngageboostTemplateIndustryMasters)
# auditlog.register(EngageboostTemplateMasters)
# auditlog.register(EngageboostTempProductCustomFields)
# auditlog.register(EngageboostTempProducts)
# auditlog.register(EngageboostTempProductimages)
# auditlog.register(EngageboostTempSuppliers)
# auditlog.register(EngageboostTemporaryShoppingCarts)
# auditlog.register(EngageboostTaxRates)
# auditlog.register(EngageboostTaxRatesConditions)
# auditlog.register(EngageboostTaxRuleTables)
# auditlog.register(EngageboostTaxSettings)
# auditlog.register(EngageboostTaxclasses)
# auditlog.register(EngageboostShippingMasters)
# auditlog.register(EngageboostShippingMastersSettings)
# auditlog.register(EngageboostShippingServiceNames)
# auditlog.register(EngageboostShippingPackagingtype)
# auditlog.register(EngageboostTags)
# auditlog.register(EngageboostSuppliers)
# auditlog.register(EngageboostPresets)
# auditlog.register(EngageboostOrderActivity)
# auditlog.register(EngageboostOrderDeliverySlot)
# auditlog.register(EngageboostOrderFilters)
# auditlog.register(EngageboostOrderLayouts)
# auditlog.register(EngageboostOrderNotes)
# auditlog.register(EngageboostOrderReturnDetails)
# auditlog.register(EngageboostOrderStatusSettings)
# auditlog.register(EngageboostOrderSubscribe)
# auditlog.register(EngageboostOrderSubscribeDetails)
# auditlog.register(EngageboostNewsletterSubcribes)
# auditlog.register(EngageboostPages)
# auditlog.register(EngageboostParentCategories)
# auditlog.register(EngageboostPaymentSetupDetails)
# auditlog.register(EngageboostPaymentgatewayTypes)
# auditlog.register(EngageboostPaymentgatewayMethods)
# auditlog.register(EngageboostPaymentgatewaySettings)
# auditlog.register(EngageboostPaymentgatewaySettingInformation)
# auditlog.register(EngageboostWebsitePaymentmethods)
# auditlog.register(EngageboostPaymentgatewaysGlobalsettings)
# auditlog.register(EngageboostTimezones)
# auditlog.register(EngageboostOtherLocation)
# auditlog.register(EngageboostPurchaseOrderProducts)
# auditlog.register(EngageboostPurchaseOrders)
# auditlog.register(EngageboostPurchaseOrdersReceived)
# auditlog.register(EngageboostPurchaseOrderReceivedProducts)
# auditlog.register(EngageboostPurchaseOrdersPaymentMethods)
# auditlog.register(EngageboostPurchaseOrdersShippingMethods)
# auditlog.register(EngageboostPermisions)
# auditlog.register(EngageboostPicklistProducts)
# auditlog.register(EngageboostPicklists)
# auditlog.register(EngageboostPlanDetails)
# auditlog.register(EngageboostRelatedProducts)
# auditlog.register(EngageboostReportCustomer)
# auditlog.register(EngageboostReportDate)
# auditlog.register(EngageboostReportLocation)
# auditlog.register(EngageboostReportOrder)
# auditlog.register(EngageboostReportProduct)
# auditlog.register(EngageboostShowroomManagers)
# auditlog.register(EngageboostShowroomMasters)
# auditlog.register(EngageboostSmsTypeContents)
# auditlog.register(EngageboostSmsTypeMasters)
# auditlog.register(EngageboostTrentPicklists)
# auditlog.register(EngageboostTrentsPicklistProducts)
# auditlog.register(EngageboostUnitMasters)
# auditlog.register(EngageboostUnitRates)
# auditlog.register(EngageboostOTP)
# auditlog.register(EngageboostStatePincodes)
# auditlog.register(EngageboostStorelocators)
# auditlog.register(EngageboostSuperadmins)
# auditlog.register(EngageboostTwitterCredentials)
# auditlog.register(EngageboostMysavelist)
# auditlog.register(EngageboostNotificationReturn)
# auditlog.register(EngageboostRoleMenuPermissions)
# auditlog.register(EngageboostSitemodules)
# auditlog.register(EngageboostMarketplaceFtpCredentials)
# auditlog.register(EngageboostMarketplaceInventory)
# auditlog.register(EngageboostMarketplaceInventoryPriceUpdate)
# auditlog.register(EngageboostRepricingRules)
# auditlog.register(EngageboostRepricingUpdateTrack)
# auditlog.register(EngageboostSellerAccountTypes)
# auditlog.register(EngageboostShippingErrorLogs)
# auditlog.register(EngageboostShippingTableRateOrderAmount)
# auditlog.register(EngageboostShippingTableRateWeight)
# auditlog.register(EngageboostShippingZipcodes)
# auditlog.register(EngageboostUserAccounts)
# auditlog.register(EngageboostUserLoginDetails)
# auditlog.register(EngageboostUserPlanDetails)
# auditlog.register(EngageboostUserSuggestions)
# auditlog.register(EngageboostUserWebsites)
# auditlog.register(EngageboostUspsMatrix)
# auditlog.register(EngageboostVehicleMasters)
# auditlog.register(EngageboostVendorSkus)
# # auditlog.register(EngageboostVisitContacts)
# auditlog.register(EngageboostPaypalstdReturnDetails)
# auditlog.register(EngageboostPaytmItemTransactions)
# auditlog.register(EngageboostPaytmOrderProcess)
# auditlog.register(EngageboostPaytmOrderTransactions)
# auditlog.register(EngageboostPaytmProductDetails)
# auditlog.register(EngageboostPaytmReturnDetails)
# auditlog.register(EngageboostReturnDetails)
# auditlog.register(EngageboostPriceFormula)
# auditlog.register(EngageboostPurchaseOrderReceivedProductDetails)
# auditlog.register(EngageboostMultipleBarcodes)
# auditlog.register(EngageboostOrderPaymentDetails)
# auditlog.register(EngageboostTempMultipleBarcodes)
# auditlog.register(EngageboostPriceTypeMaster)
# auditlog.register(EngageboostProductPriceTypeMaster)
# auditlog.register(EngageboostWarehouseSupplierMappings)
# auditlog.register(EngageboostAdditionalGlobalsettings)
# auditlog.register(EngageboostDiscountFreebieMappings)
# auditlog.register(EngageboostAdvancedSearchLayouts)
# auditlog.register(EngageboostAdvancedSearchModules)
