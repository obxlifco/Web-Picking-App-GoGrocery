# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-19 12:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservices', '0015_auto_20190219_1041'),
    ]

    operations = [
        migrations.CreateModel(
            name='EngageboostFacebookProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_id', models.BigIntegerField(blank=True, null=True)),
                ('website_id', models.BigIntegerField(blank=True, null=True)),
                ('product_id', models.BigIntegerField(blank=True, null=True)),
                ('is_blocked', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2)),
                ('is_deleted', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2)),
                ('added_on', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'engageboost_facebook_products',
            },
        ),
        migrations.CreateModel(
            name='EngageboostFbaPlanProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_plan_id', models.IntegerField(blank=True, null=True)),
                ('product_id', models.IntegerField(blank=True, null=True)),
                ('sku', models.CharField(blank=True, max_length=11, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('labeled_by', models.CharField(choices=[('Merchant', 'Merchant'), ('Amazon', 'Amazon')], default='Merchant', max_length=20)),
                ('prep_by', models.CharField(choices=[('Merchant', 'Merchant'), ('Amazon', 'Amazon')], default='Merchant', max_length=20)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'engageboost_fba_plan_products',
            },
        ),
        migrations.CreateModel(
            name='EngageboostFbaShipmentProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_plan_id', models.IntegerField(blank=True, null=True)),
                ('fba_shipment_id', models.CharField(blank=True, max_length=250, null=True)),
                ('shipment_id', models.IntegerField(blank=True, null=True)),
                ('warehouse_id', models.IntegerField(blank=True, null=True)),
                ('sku', models.CharField(blank=True, max_length=250, null=True)),
                ('product_id', models.IntegerField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('received_quantity', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'engageboost_fba_shipment_products',
            },
        ),
        migrations.CreateModel(
            name='EngageboostFbaShipments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_plan_id', models.IntegerField(blank=True, null=True)),
                ('shipment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('shipment_name', models.CharField(blank=True, max_length=250, null=True)),
                ('msku', models.CharField(blank=True, max_length=50, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('product_id', models.IntegerField(blank=True, null=True)),
                ('warehouse_id', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('shipment_type', models.CharField(blank=True, max_length=100, null=True)),
                ('shipping_service_type', models.CharField(blank=True, max_length=250, null=True)),
                ('shipping_service_code', models.CharField(blank=True, max_length=250, null=True)),
                ('shipping_tracking_code', models.CharField(blank=True, max_length=255, null=True)),
                ('transport_status', models.CharField(blank=True, max_length=250, null=True)),
                ('shipment_packing', models.CharField(blank=True, max_length=250, null=True)),
                ('shipment_label', models.CharField(blank=True, max_length=250, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('is_blocked', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2)),
                ('is_deleted', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2)),
            ],
            options={
                'db_table': 'engageboost_fba_shipments',
            },
        ),
        migrations.CreateModel(
            name='EngageboostFbaShippingBoxes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipment_id', models.IntegerField(blank=True, null=True)),
                ('amazon_shipment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('tracking_id', models.CharField(blank=True, max_length=250, null=True)),
                ('box_weight', models.IntegerField(blank=True, null=True)),
                ('box_length', models.IntegerField(blank=True, null=True)),
                ('box_width', models.IntegerField(blank=True, null=True)),
                ('box_height', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('is_blocked', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2)),
                ('is_deleted', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2)),
            ],
            options={
                'db_table': 'engageboost_fba_shipping_boxes',
            },
        ),
        migrations.CreateModel(
            name='EngageboostFbaShippingPlanFeedSubmissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_plan_id', models.IntegerField(blank=True, null=True)),
                ('feed_submission_id', models.BigIntegerField(blank=True, null=True)),
                ('result', models.TextField(blank=True, null=True)),
                ('website_id', models.IntegerField(blank=True, null=True)),
                ('channel_id', models.IntegerField(blank=True, null=True)),
                ('is_called', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2)),
                ('feed_type', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('report_id', models.BigIntegerField(blank=True, null=True)),
                ('report_call_status', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2, null=True)),
            ],
            options={
                'db_table': 'engageboost_fba_shipping_plan_feed_submissions',
            },
        ),
        migrations.CreateModel(
            name='EngageboostFbaShippingplans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website_id', models.IntegerField(blank=True, null=True)),
                ('plan_name', models.CharField(blank=True, max_length=250, null=True)),
                ('warehouse_id', models.IntegerField(blank=True, null=True)),
                ('channel_id', models.IntegerField(blank=True, null=True)),
                ('plan_id', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(choices=[('inprocess', 'inprocess'), ('success', 'success'), ('error', 'error'), ('working', 'working')], default='inprocess', max_length=20, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'engageboost_fba_shippingplans',
            },
        ),
        migrations.CreateModel(
            name='EngageboostFbaShippingServices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_service_name', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_service_code', models.CharField(blank=True, max_length=255, null=True)),
                ('channel_id', models.IntegerField(blank=True, null=True)),
                ('service_type', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'engageboost_fba_shipping_services',
            },
        ),
        migrations.CreateModel(
            name='EngageboostFbaSteps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('step_url', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'engageboost_fba_steps',
            },
        ),
        migrations.CreateModel(
            name='EngageboostFbPageProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_id', models.BigIntegerField(blank=True, null=True)),
                ('company_id', models.IntegerField(blank=True, null=True)),
                ('website_url', models.CharField(blank=True, max_length=222, null=True)),
                ('website_id', models.IntegerField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=222, null=True)),
                ('ses_id', models.IntegerField(blank=True, null=True)),
                ('is_added', models.CharField(choices=[('0', '0'), ('1', '1')], default='0', max_length=2)),
                ('is_blocked', models.CharField(choices=[('0', '0'), ('1', '1')], default='0', max_length=2)),
                ('is_deleted', models.CharField(choices=[('0', '0'), ('1', '1')], default='0', max_length=2)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('store_url', models.CharField(blank=True, max_length=255, null=True)),
                ('store_name', models.CharField(blank=True, max_length=255, null=True)),
                ('page_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'engageboost_fb_page_products',
            },
        ),
        migrations.CreateModel(
            name='EngageboostFbTempUserDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.IntegerField(blank=True, null=True)),
                ('website_id', models.IntegerField(blank=True, null=True)),
                ('fb_user_id', models.CharField(blank=True, max_length=250, null=True)),
                ('fb_access_token', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'engageboost_fb_temp_user_details',
            },
        ),
        migrations.CreateModel(
            name='EngageboostFedexZipcodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website_id', models.IntegerField(blank=True, null=True)),
                ('country_id', models.IntegerField(blank=True, null=True)),
                ('pincode', models.CharField(blank=True, max_length=255, null=True)),
                ('prepaid', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2)),
                ('cod', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2)),
                ('city_name', models.CharField(blank=True, max_length=255, null=True)),
                ('state_id', models.IntegerField(blank=True, null=True)),
                ('state_name', models.CharField(blank=True, max_length=255, null=True)),
                ('cod_capability', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'engageboost_fedex_zipcodes',
            },
        ),
        migrations.CreateModel(
            name='EngageboostFeeMasters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_name', models.CharField(blank=True, max_length=255, null=True)),
                ('channel_id', models.IntegerField(blank=True, null=True)),
                ('fee_applicable_for', models.CharField(choices=[('shipping', 'shipping'), ('transaction', 'transaction')], default='shipping', max_length=20)),
                ('fee_based_on', models.CharField(choices=[('range', 'range'), ('fixed', 'fixed')], default='range', max_length=20)),
                ('fee_for', models.CharField(blank=True, max_length=50, null=True)),
                ('payment_type', models.CharField(blank=True, max_length=255, null=True)),
                ('account_type_id', models.IntegerField(blank=True, null=True)),
                ('website_id', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('isblocked', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2)),
                ('isdeleted', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2)),
            ],
            options={
                'db_table': 'engageboost_fee_masters',
            },
        ),
        migrations.CreateModel(
            name='EngageboostFeeSettingMasters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_master_id', models.IntegerField(blank=True, null=True)),
                ('slab_name', models.CharField(blank=True, max_length=500, null=True)),
                ('slab_start', models.FloatField(blank=True, null=True)),
                ('slab_end', models.FloatField(blank=True, null=True)),
                ('interval_range', models.FloatField(blank=True, null=True)),
                ('uom', models.CharField(blank=True, max_length=100, null=True)),
                ('shipping_local', models.IntegerField(blank=True, null=True)),
                ('shipping_zonal', models.IntegerField(blank=True, null=True)),
                ('shipping_national', models.IntegerField(blank=True, null=True)),
                ('shipping_international', models.IntegerField(blank=True, null=True)),
                ('slab_value', models.IntegerField(blank=True, null=True)),
                ('fee_type', models.CharField(choices=[('F', 'F'), ('P', 'P')], default='F', max_length=2)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('isblocked', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2)),
                ('isdeleted', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2)),
            ],
            options={
                'db_table': 'engageboost_fee_setting_masters',
            },
        ),
        migrations.CreateModel(
            name='EngageboostFlipkartOrderTransactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField(blank=True, null=True)),
                ('flipkart_order_id', models.CharField(blank=True, max_length=255, null=True)),
                ('orderitemid', models.BigIntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('orderdate', models.DateTimeField(blank=True, null=True)),
                ('sla', models.CharField(blank=True, max_length=50, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('product_id', models.IntegerField(blank=True, null=True)),
                ('listingid', models.CharField(blank=True, max_length=255, null=True)),
                ('fsn', models.CharField(blank=True, max_length=255, null=True)),
                ('sku', models.CharField(blank=True, max_length=255, null=True)),
                ('sellingprice', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('customerprice', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('shippingcharge', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('totalprice', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('dispatchafterdate', models.DateTimeField(blank=True, null=True)),
                ('dispatchbydate', models.DateTimeField(blank=True, null=True)),
                ('deliverbydate', models.DateTimeField(blank=True, null=True)),
                ('updatedat', models.DateTimeField(blank=True, null=True)),
                ('paymenttype', models.CharField(blank=True, max_length=100, null=True)),
                ('shipmentid', models.CharField(blank=True, max_length=100, null=True)),
                ('shipmenttype', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'engageboost_flipkart_order_transactions',
            },
        ),
        migrations.CreateModel(
            name='EngageboostFlipkartReconciliations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_id', models.IntegerField(blank=True, null=True)),
                ('website_id', models.IntegerField(blank=True, null=True)),
                ('reconciliation_file_id', models.IntegerField(blank=True, null=True)),
                ('boost_order_id', models.IntegerField(blank=True, null=True)),
                ('flipkart_txn_id', models.IntegerField(blank=True, null=True)),
                ('boost_order_product_id', models.IntegerField(blank=True, null=True)),
                ('sheet_settlement_ref_no', models.CharField(blank=True, max_length=255, null=True)),
                ('sheet_order_type', models.CharField(blank=True, max_length=100, null=True)),
                ('sheet_fulfilment_type', models.CharField(blank=True, max_length=100, null=True)),
                ('sheet_seller_sku', models.CharField(blank=True, max_length=255, null=True)),
                ('sheet_wsn', models.CharField(blank=True, max_length=255, null=True)),
                ('sheet_order_id_fsn', models.CharField(blank=True, max_length=255, null=True)),
                ('sheet_order_item_id', models.CharField(blank=True, max_length=100, null=True)),
                ('sheet_order_date', models.DateTimeField(blank=True, null=True)),
                ('sheet_dispatch_date', models.DateTimeField(blank=True, null=True)),
                ('sheet_delivery_date', models.DateTimeField(blank=True, null=True)),
                ('sheet_cancellation_date', models.DateTimeField(blank=True, null=True)),
                ('sheet_settlement_date', models.DateTimeField(blank=True, null=True)),
                ('sheet_order_status', models.CharField(blank=True, max_length=100, null=True)),
                ('sheet_quantity', models.IntegerField(blank=True, null=True)),
                ('sheet_order_item_value', models.FloatField(blank=True, null=True)),
                ('sheet_sale_transaction_amount', models.FloatField(blank=True, null=True)),
                ('sheet_discount_transaction_amount', models.FloatField(blank=True, null=True)),
                ('sheet_refund', models.FloatField(blank=True, null=True)),
                ('sheet_protection_fund', models.FloatField(blank=True, null=True)),
                ('sheet_total_marketplace_fee', models.FloatField(blank=True, null=True)),
                ('sheet_service_tax', models.FloatField(blank=True, null=True)),
                ('sheet_sb_cess_tax', models.FloatField(blank=True, null=True)),
                ('sheet_kk_cess_tax', models.FloatField(blank=True, null=True)),
                ('sheet_settlement_value', models.FloatField(blank=True, null=True)),
                ('sheet_commission_rate', models.FloatField(blank=True, null=True)),
                ('sheet_commission', models.FloatField(blank=True, null=True)),
                ('sheet_payment_rate', models.FloatField(blank=True, null=True)),
                ('sheet_payment_fee', models.FloatField(blank=True, null=True)),
                ('sheet_fee_discount', models.FloatField(blank=True, null=True)),
                ('sheet_cancellation_fee', models.FloatField(blank=True, null=True)),
                ('sheet_fixed_fee', models.FloatField(blank=True, null=True)),
                ('sheet_admonetaisation_fee', models.FloatField(blank=True, null=True)),
                ('sheet_dead_weight', models.FloatField(blank=True, null=True)),
                ('sheet_chargeable_wt_slab', models.FloatField(blank=True, null=True)),
                ('sheet_chargeable_weight_type', models.CharField(blank=True, max_length=100, null=True)),
                ('sheet_lenght_breadth_height', models.CharField(blank=True, max_length=100, null=True)),
                ('sheet_volumetric_weight_in_kg', models.FloatField(blank=True, null=True)),
                ('sheet_shipping_fee', models.FloatField(blank=True, null=True)),
                ('sheet_reverse_shipping_fee', models.FloatField(blank=True, null=True)),
                ('sheet_shipping_fee_reversal', models.FloatField(blank=True, null=True)),
                ('sheet_shipping_zone', models.CharField(blank=True, max_length=100, null=True)),
                ('sheet_token_of_apology', models.FloatField(blank=True, null=True)),
                ('sheet_pick_and_pack_fee', models.FloatField(blank=True, null=True)),
                ('sheet_storage_fee', models.FloatField(blank=True, null=True)),
                ('sheet_removal_fee', models.FloatField(blank=True, null=True)),
                ('sheet_invoice_id', models.CharField(blank=True, max_length=255, null=True)),
                ('sheet_invoice_date', models.DateTimeField(blank=True, null=True)),
                ('sheet_invoice_amount', models.FloatField(blank=True, null=True)),
                ('sheet_sub_category', models.CharField(blank=True, max_length=255, null=True)),
                ('sheet_total_offer_amount', models.FloatField(blank=True, null=True)),
                ('sheet_my_offer_share', models.FloatField(blank=True, null=True)),
                ('sheet_flipkart_offer_share', models.FloatField(blank=True, null=True)),
                ('sheet_service_cancellation_fee', models.FloatField(blank=True, null=True)),
                ('sheet_ndd_amount', models.FloatField(blank=True, null=True)),
                ('sheet_ndd_fee', models.FloatField(blank=True, null=True)),
                ('sheet_sdd_amount', models.FloatField(blank=True, null=True)),
                ('sheet_sdd_fee', models.FloatField(blank=True, null=True)),
                ('sheet_sellable_regular_storage_fee', models.FloatField(blank=True, null=True)),
                ('sheet_unsellable_regular_storage_fee', models.FloatField(blank=True, null=True)),
                ('sheet_sellable_long_term_1_storage_fee', models.FloatField(blank=True, null=True)),
                ('sheet_unsellable_longterm_1_storage_fee', models.FloatField(blank=True, null=True)),
                ('sheet_unsellable_longterm_2_storage_fee', models.FloatField(blank=True, null=True)),
                ('sheet_is_replacement', models.CharField(blank=True, max_length=100, null=True)),
                ('sheet_multi_product', models.CharField(blank=True, max_length=100, null=True)),
                ('sheet_profiler_dead_weight', models.FloatField(blank=True, null=True)),
                ('sheet_seller_dead_weight', models.FloatField(blank=True, null=True)),
                ('sheet_customer_shipping_amount', models.FloatField(blank=True, null=True)),
                ('sheet_customer_shipping_fee', models.FloatField(blank=True, null=True)),
                ('sheet_payment_mode_changed', models.CharField(blank=True, max_length=100, null=True)),
                ('isdeleted', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2)),
                ('isblocked', models.CharField(choices=[('y', 'y'), ('n', 'n')], default='n', max_length=2)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'engageboost_flipkart_reconciliations',
            },
        ),
    ]