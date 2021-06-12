from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from webservices.views import *
from webservices.views.employee import *
from webservices.views.settings import *
from webservices.views.product import *
from webservices.views.order import *
from webservices.views.inventory import *
from webservices.views.shortcuts import *
from webservices.views.common import *
from webservices.views.cron import *
from webservices.views.deliveryapp import *
from webservices.views.pickingapp import *
from webservices.views.frontend import *
from webservices.views.contentmanagement import *
from webservices.views.report import *

from webservices.views.operation_settings import *
from webservices.views.common.common import getAutoResponderDetails

from webservices import *
from rest_framework.routers import DefaultRouter
from webservices.views.frontend.category import categoryview
from webservices.views.frontend.product import productview
from webservices.views.frontend.banner import bannerview
from webservices.views.dashboard import *
from webservices.views.frontend.brand import brandview

# Pg
from frontapp.views.payment.paymentgateway import update_ccavenue_order_status_cron

from apscheduler.schedulers.background import BackgroundScheduler

urlpatterns = [ 
    # Session Login
    url(r'^login/$', views.login, name='login'),
    url(r'^usercreate/$', views.usercreate, name='usercreate'),
    url(r'^createotp/$', views.createotp, name='createotp'),
    url(r'^checkotp/$', views.checkotp, name='checkotp'),
    url(r'^signup/$', views.insertdata, name='signup'),
    url(r'^forgotpassword/$', views.forgotpassword, name='forgotpassword'),
    url(r'^verification/$', views.verification, name='verification'),
    url(r'^changepassword/$', views.changepassword, name='changepassword'),

    
    # """ Menu """ 
    url(r'^getmenu/(?P<pk>[0-9]+)/$', views.MenuViewSet.as_view({'get':'list'}), name='MenuViewSet'),  
    url(r'^getmenu_group/$', views.MenuGroup.as_view({'get':'list'}), name='MenuGroup'),  

    # # """ Role """ 
    #  url(r'^list_role/$', views.RoleMasterViewSet.as_view({'get':'list_role'}), name='RoleMasterViewSet'),
    #  url(r'^delete_role/$', views.delete_role, name='delete_role'),
    #  url(r'^add_role/$', views.add_role, name='add_role'),
    #  url(r'^statuschange_role/$', views.statuschange_role, name='statuschange_role'),

    # ************** Common Function **************** #
    url(r'^countrylist/$', views.common.CommonCountries.as_view()),
    url(r'^countrylist/(?P<pk>[0-9]+)/$', views.common.CountryDetails.as_view()),
    url(r'^countrystatelist/(?P<country_id>[0-9]+)/$', views.common.StateList.as_view()),
    url(r'^customer_information/(?P<customer_id>[0-9]+)/(?P<email>[\w\d@\.-]+)/$', views.common.CustomerById.as_view()),
    url(r'^customer_group_list/$', views.common.CustomerGroupList.as_view()),
    url(r'^marketplace_list/$', views.common.MarketPlaceList.as_view()),
    url(r'^marketplace_list_by_id/(?P<id>[0-9]+)/$', views.common.MarketPlaceListById.as_view()),
    url(r'^tag_list/$',views.common.TagList.as_view()),
    url(r'^warehouse-list/$',views.common.WarehouseList.as_view()),
    url(r'^courier_list/$',views.common.CourierList.as_view()),
    url(r'^getglobalsettings/(?P<website_id>[0-9]+)/$',views.common.GetGlobalSettings.as_view()),
    url(r'^update_product_price/$',views.common.update_product_price),
    

    # ******************  New ***************************************
    url(r'^currencylist/$', views.common.CommonCurrencyList.as_view(), name='currencylist'),

    # ************** Common Function(END) **************** #
    
    # ************************ DASHBOARD ************************************
    url(r'^dashboard/$', views.dashboard.ShowDashboard.as_view(), name='dashboard'),
    url(r'^sales-graph/$', views.dashboard.sales_report.as_view(), name='sales-graph'),
    
     # ************************ END DASHBOARD *******************************

    # ************** ORDER **************** #
    url(r'^assign_to_warehouse/$', views.order.AssignToWarehouse.as_view()),
    url(r'^update_order_status/$', views.order.UpdateOrderStatus.as_view()),
    url(r'^tag/(?P<id>[0-9]+)/$', views.order.GetTags.as_view()),
    url(r'^manage_tags/$', views.order.ManageTags.as_view()),
    url(r'^assign_tag/$',views.order.AssignTag.as_view()),
    url(r'^find_customer/$', views.order.FindCustomer.as_view()),
    url(r'^get_customer_info/$', views.order.GetCustomerInfo.as_view()),
    url(r'^generate_order_id/(?P<channel_id>[0-9]+)/$',views.order.GenerateOrderId.as_view()),
    url(r'^payment_method_list/$',views.order.PaymentGatewayList.as_view()),
    url(r'^warehousewise_product/$',views.order.WarehouseWiseProduct.as_view()),
    url(r'^product_discount_calculation/$',views.order.ProductDiscountCalculation.as_view()),
    url(r'^save-order/$', views.order.SaveOrder.as_view()),
    url(r'^ordersloadview/(?P<website_id>[0-9]+)/$', views.order.OrdersLoadView.as_view()),
    url(r'^orderinfoviewset/$', views.order.OrderInfoViewSet.as_view()), # add order - related load data
    # orderinfoviewset - edit order load data for get method..../ put method for edit order save data
    url(r'^orderinfoviewset/(?P<pk>[0-9]+)/(?P<website_id>[0-9]+)/$', views.order.OrderList.as_view()),
    # open open popup products for add end edit order...
    url(r'^orders_load_view_product/$', views.order.OrdersLoadViewProduct.as_view()),
    url(r'^order_delivery/$', views.order.OrderDelivery.as_view()),

    url(r'^payments/$', views.order.Paymentmethodtype.as_view()),
    url(r'^testtest/$', views.order.test.as_view()),
    url(r'^get-order-activity/(?P<order_id>[0-9]+)/(?P<website_id>[0-9]+)/$', views.order.OrderActivity.as_view()),
    url(r'^post_activity/$', views.order.OrderActivity.as_view()),
    # ************   New ******
    url(r'^delivery-slot/$', views.order.get_delivery_slot.as_view(), name='delivery-slot'),
    url(r'^available-promo/$', views.order.GetAvailablePromo.as_view(), name='available-promo'),
    url(r'^area-subarea/$', DeliverySlot.get_all_sub_areas.as_view(), name='area-subarea'),
    url(r'^view-order/(?P<pk>[0-9]+)/$', views.order.ViewOrder.as_view(), name='view-order'),
    url(r'^edit-order/$', views.order.EditOrder.as_view(), name='edit-order'),
    url(r'^delete-order/$', views.order.DeleteOrder.as_view(), name='delete-order'),
    url(r'^order-delivery-slot/$', views.order.GetOrderDeliverySlot.as_view(), name='order-delivery-slot'),
    url(r'^order-export/$', views.order.OrderExport.as_view(), name='order-export'),
    
    url(r'^manage-order-details/(?P<pk>[0-9]+)/$', views.order.ManageOrderDetails.as_view(), name='manage-order-details'),
    url(r'^test-order/$', views.order.testorder.as_view()),
    url(r'^user-loyalty-points/$', views.order.LoyaltyPointsDetails.as_view(), name = 'user-loyalty-points'),
    
    # ************** ORDER(END) **************** #

    # ************** SHIPMENT **************** #
    url(r'^picklist/$', views.order.PickList.as_view()),
    url(r'^create_picklist/$', views.order.CreatePicklist.as_view()),
    url(r'^shipment/$', views.order.Shipment.as_view()),
    url(r'^invoice/$', views.order.Invoice.as_view()),
    url(r'^invoice-new/$', views.order.Invoice_new.as_view()),
    url(r'^invoice-si/$', views.order.Invoice_si.as_view()),
    url(r'^delivery-planner/$', views.order.DeliveryPlanner.as_view()),
    url(r'^save-sortby-distance/$', views.order.saveSortBydistance.as_view()),
    url(r'^assign_vehicle/$', views.order.AssignVehicle.as_view()),
    url(r'^create_assign_vehicle/$', views.order.CreateAssignVehicle.as_view()),
    url(r'^remove-from-shipment/$', views.order.RemoveOrderShipment.as_view()),
    url(r'^delete-shipment/$', views.order.DeleteShipment.as_view()), # this is for delete shipment from  shipment grid
    url(r'^delete-picklist/$', views.order.DeletePicklist.as_view()), # this is for delete picklist from  pickist grid
    url(r'^printinvoice/$', views.order.InvoicePrint.as_view()),
    url(r'^printpicklist/$', views.order.PicklistPrint.as_view()),
    
    # url(r'^shipping_label/$', views.order.ShipingLabel.as_view()),
    # url(r'^shipping_label_popup/$', views.order.ShipingLabelPopup.as_view()),
    # url(r'^create_shipping_label/$', views.order.CreateShippingLabel.as_view()),
    # url(r'^print_shipping_label/$', views.order.PrintShippingLabel.as_view()),
    
    url(r'^shipping_manifest/$', views.order.ShipingManifest.as_view()),
    url(r'^create_shipping_manifest/$', views.order.CreateShipingManifest.as_view()),
    url(r'^print_manifest/$', views.order.PrintManifest.as_view()),
    url(r'^print-barcode/$', views.order.print_barcode.as_view(), name = 'print-barcode'),
    url(r'^picklist-order/(?P<pk>[0-9]+)/$', views.order.OrderlistByPicklist.as_view(), name = 'picklist-order'),
    url(r'^picklist-order-details/(?P<pk>[0-9]+)/(?P<website_id>[0-9]+)/$', views.order.OrderDetailsByPicklistid.as_view(), name = 'picklist-order-details'),
    # url(r'^picklist-order-shipment-order/(?P<pk>[0-9]+)/$', views.order.OrderDetailsByShipmentOrder.as_view(), name = 'picklist-order-shipment-order'),
    url(r'^grn_order_details/$', views.order.get_grn_order_details.as_view(), name = 'grn_order_details'),
    url(r'^get_order_products_info/$', views.order.get_order_products_info.as_view()),
    url(r'^grn_draft/$', views.order.grn_save_as_draft.as_view(), name = 'grn_draft'),
    url(r'^grn_order_details_by_order_id/$', views.order.get_grn_order_details_by_order_id.as_view(), name = 'grn_order_details_by_order_id'),
    url(r'^grn_complete/$', views.order.grn_complete.as_view(), name = 'grn_complete'),
    
    url(r'^search-picked-products/$', views.order.search_picked_products.as_view(), name = 'search-picked-products'),
    url(r'^add-crates/$', views.order.add_crates.as_view(), name = 'add-crates'),
    url(r'^delete-crates/$', views.order.delete_crates.as_view(), name = 'delete-crates'),
    url(r'^crate-list/$', views.order.get_all_crates.as_view(), name = 'crate-list'),
    
    # url(r'^shipping_methods/$', views.inventory.Shipping_methods_list.as_view()),
    # ************** SHIPMENT(END) **************** #

    # ************** PRESET MANAGEMENT ************** #
    url(r'^save_preset/$', views.order.PresetSetup.as_view()),
    url(r'^preset/(?P<pk>[0-9]+)/$', views.order.PresetListView.as_view()),
    url(r'^preset_data/$', views.order.Presetdata.as_view()),
    url(r'^preset_services/(?P<shipping_service_id>[0-9]+)/$', views.order.ServicesList.as_view()),
    url(r'^preset_packege/$', views.order.PackegeList.as_view()),
    # ************** PRESET MANAGEMENT(END) ************** #


    # ************** COURIER MANAGEMENT ************** #
    url(r'^add_courier/$', views.order.CourierAdd.as_view()),
    url(r'^get_courier/(?P<id>[0-9]+)/$', views.order.GetCourierInfo.as_view()),
    url(r'^view_awb_details/$', views.order.ViewAwbDetails.as_view()),
    url(r'^add_awb_number/$', views.order.AddAwbNumber.as_view()),
    # ************** COURIER MANAGEMENT(END) ************** #


    # ************** SETTINGS ************** #
    # """---- Global Settings ----""" 
    url(r'^globalsettings/$', views.settings.Glsettings.as_view()),
    url(r'^globalsettings/(?P<pk>[0-9]+)/$', views.settings.Glsettingsup.as_view()),
    url(r'^globalsettings_list/$', views.settings.GlobalsettingsList.as_view()),
    url(r'^countries/$', views.settings.Glsettingscountries.as_view()),
    url(r'^timezone/$', views.settings.Glsettingstimezone.as_view()),
    url(r'^list_of_websites/$', views.settings.CompanyWebsites.as_view()),
    # """---- Basic Setup ----"""
    url(r'^basicsettings/$', views.settings.BasicsettingsList.as_view()),
    url(r'^basicsettings/(?P<pk>[0-9]+)/$', views.settings.Basicsettingsup.as_view()),
    url(r'^basicsettings_load/$', views.settings.IndustryList.as_view()),
    url(r'^templateslist/$', views.settings.TemplatesList.as_view()),
    url(r'^check/$', views.settings.check.as_view()),
    url(r'^store_image_delete/$', views.settings.WebstoreImageDelete.as_view()),
    # """---- Payment Gateway ----"""
    url(r'^paymentmethods/$', views.settings.PaymentMethodList.as_view()),
    url(r'^paymentsetup/$', views.settings.PaymentSetup.as_view()),
    url(r'^paymentsetup/(?P<pk>[0-9]+)/$', views.settings.PaymentSetupView.as_view()),
    # """---- Shipping Method Setup ----"""
    #url(r'^shippinglist/$', views.settings.ShippingList.as_view()),
    url(r'^shippinglist/(?P<shipping_method_id>[0-9]+)/(?P<shipping_type>\w+)/(?P<table_rate_type>[0-9]+)/(?P<shipping_id>[0-9]+)/$', views.settings.ShippingList.as_view()),
    url(r'^shippingsetup/$', views.settings.ShippingSetup.as_view()),
    url(r'^shippingsetuptablerate/$', views.settings.SaveTableRate.as_view()),
    url(r'^statelist_shipping_method/(?P<pk>[0-9]+)/$', views.settings.StateList.as_view()),
    url(r'^shippinglistgetupdate/(?P<pk>[0-9]+)/$', views.settings.ShippingMethodUpdate.as_view()),
    url(r'^shippinglistcod/$', views.settings.FedexZipcodeList.as_view()),
    url(r'^shippingsetupcod/$', views.settings.FedexZipcodeSetup.as_view()),
    url(r'^del-cod/$', views.settings.FedexZipcodeDelete.as_view()),

    # url(r'^shippinglistgetupdate/(?P<pk>[0-9]+)/$', views.settings.ShippingMethodUpdate.as_view()),
    # url(r'^shippinglistgetupdate/(?P<pk>[0-9]+)/$', views.settings.ShippingMethodUpdate.as_view()),

    # """---- Channel Setup ----"""
    # url(r'^channellist/$', views.settings.ChannelList.as_view()),
    # url(r'^channelsetup/$', views.settings.ChannelSetup.as_view()),
    url(r'^channellistview/(?P<pk>[0-9]+)/$', views.settings.ChannelViewList.as_view()),
    url(r'^activedeactivechannel/$', views.settings.ActiveDeactiveChannel.as_view()),
    url(r'^amazoncredential/(?P<website_id>[0-9]+)/(?P<channel_id>[0-9]+)/$', views.settings.AmazonCredential.as_view()),
    url(r'^amazoncredentialsave/$', views.settings.AmazonCredentialSave.as_view()),
    url(r'^flipkartcredentialsave/$', views.settings.FlipkartCredentialSave.as_view()),
    url(r'^ebaycredentialsave/$', views.settings.EbayCredentialSave.as_view()),
    url(r'^snapcredentialsave/$', views.settings.SnapdealCredentialSave.as_view()),
    # ************** SETTINGS(END) ************** #


    # ************** PRODUCT ************** #
    url(r'^basicinfo/$', views.product.BasicInformationViewSet.as_view()),
    url(r'^basicinfo/(?P<pk>[0-9]+)/$', views.product.BasicProductSet.as_view()),
    url(r'^basicinfo_load/$', views.product.BasicInformationLoadViewSet.as_view()),
    url(r'^advanceinfo/$', views.product.AdvanceInformationViewSet.as_view()),
    url(r'^advanceinfo/(?P<pk>[0-9]+)/(?P<channel_id>[0-9]+)/$', views.product.AdvanceInformationLoadViewSet.as_view()),
    url(r'^product_list/$', views.product.ProductList.as_view()),
    url(r'^product_setup/$', views.product.Productsetup.as_view()),
    url(r'^defaultprice/(?P<pk>[0-9]+)/$', views.product.DefaultPriceList.as_view()),
    url(r'^relatedproduct/$', views.product.RelatedProductList.as_view()),
    url(r'^relatedproduct/(?P<product_id>[0-9]+)/(?P<product_type>[0-9]+)/$', views.product.RelatedProductList.as_view()),
    url(r'^relatedproduct_list/$', views.product.RelatedProductSet.as_view()),
    url(r'^product_priceing/$', views.product.Productpricingadd.as_view()),
    url(r'^getchildProduct/$', views.product.GetProductChild.as_view()),
    url(r'^multiplebarcodes/(?P<pk>[0-9]+)/$', views.product.MultipleBarcodes.as_view()),
    url(r'^importbarcodes/$', views.product.ImportBarcodes.as_view()),
    url(r'^previewimportedbarcodes/$', views.product.PreviewImportedBarcodes.as_view()),
    url(r'^saveallimportedbarcodes/$', views.product.SaveAllImportedBarcodes.as_view()),
    url(r'^getbarcodedetails/$', views.product.GetBarcodeDetails.as_view()),

    url(r'^geteanProduct/$', views.product.getEanProduct.as_view()),

    url(r'^variableproduct/$', views.product.VariableProductList.as_view()),
    url(r'^variableproduct/(?P<product_id>[0-9]+)/$', views.product.VariableProductList.as_view()),
    
    # """---- HSN CODE ----"""
    url(r'^gethsncode/(?P<id>[0-9]+)/$', views.product.HsncodeSetup.as_view()),
    url(r'^savehsncode/$', views.product.HsncodeSetup.as_view()),
    url(r'^exporthsncode/$', views.product.HsncodeExport.as_view()),
    url(r'^hsncode_list/$', views.product.HsnCodeList.as_view()),

    # """---- Promotoin Add and Import ----"""
    url(r'^import_product_promotion/$', views.product.ProductPromotionImport.as_view()),

    # """---- Product View Details ----"""
    url(r'^product_details/(?P<pid>[0-9]+)/$', views.product.ViewProductDetails.as_view()),
    url(r'^product_inventory_details/(?P<pid>[0-9]+)/(?P<user_id>[0-9]+)/$', views.product.ViewProductInventoryDetails.as_view()),
    url(r'^product_purchase_order_details/(?P<pid>[0-9]+)/(?P<user_id>[0-9]+)/$', views.product.ViewProductPurchaseOrderDetails.as_view()),
    url(r'^product_receipt_details/(?P<pid>[0-9]+)/(?P<user_id>[0-9]+)/$', views.product.ViewProductReceiptDetails.as_view()),
    url(r'^product_order_details/(?P<pid>[0-9]+)/(?P<user_id>[0-9]+)/$', views.product.ViewProductOrderDetails.as_view()),
    url(r'^product_invoice_details/(?P<pid>[0-9]+)/(?P<user_id>[0-9]+)/$', views.product.ViewProductInvoiceDetails.as_view()),
    # url(r'^product_packing_details/(?P<pid>[0-9]+)/(?P<user_id>[0-9]+)/$', views.product.ViewProductPackingDetails.as_view()),
    url(r'^product_adjustment_details/(?P<pid>[0-9]+)/(?P<user_id>[0-9]+)/$', views.product.ViewProductAdjustmentDetails.as_view()),

    #PRODUCT DETAILS BY ID  ====   View Product
    url(r'^get_suppliers_by_id/(?P<pk>[0-9]+)/$', views.product.ProductSuppliers.as_view()),
    url(r'^get_promotions_by_id/(?P<pk>[0-9]+)/$', views.product.ProductPromotion.as_view()),
    url(r'^get_top_customers_by_id/(?P<pk>[0-9]+)/$', views.product.TopCustomers.as_view()),
    url(r'^get_product_activity_by_id/(?P<pk>[0-9]+)/$', views.product.ProductActivity.as_view()),
    url(r'^get_product_rac_no_by_id/(?P<pk>[0-9]+)/$', views.product.ProductRACNO.as_view()),
    url(r'^product-view-summary/$', views.product.productDetailsSummary.as_view(), name='product-view-summary'),
    url(r'^product-view-sales-graph/$', views.product.productDetailsSummarySalesReportGraph.as_view(), name='product-view-sales-graph'),
    url(r'^product-view-marketplace/$', views.product.productDetailsMarketplaceReportGraph.as_view(), name='product-view-marketplace'),
    url(r'^product-view-visitors/$', views.product.productDetailsVisitorsReportGraph.as_view(), name='product-view-visitors'),
    url(r'^product-view-stock/$', views.product.productDetailsStockReportGraph.as_view(), name='product-view-stock'),

    # """---- Product Import and Export ----"""
    url(r'^get_child_category/$', views.product.GetChildCategory.as_view()),
    url(r'^import_file_products/$', views.product.ImportFileProducts.as_view()),
    url(r'^save_file_data/$', views.product.SaveFileData.as_view()),
    url(r'^preview_save_data/$', views.product.PreviewSaveFileData.as_view()),
    url(r'^show_all_imported_data/$', views.product.SaveAllImportedData.as_view()),
    url(r'^export_product/(?P<website_id>[0-9]+)/$', views.product.ProductExport.as_view()),
    url(r'^categoriesexport/$', views.product.CategoryExport.as_view()),

    url(r'^import_file_related_products/$', views.product.ImportFileRelatedProducts.as_view()),
    url(r'^save_file_related_data/$', views.product.SaveFileRelatedData.as_view()),
    url(r'^preview_save_related_data/$', views.product.PreviewSaveFileRelated.as_view()),
    url(r'^save_all_imported_related_data/$', views.product.SaveAllImportedRelated.as_view()),
    # ************** PRODUCT(END) ************** #

    # ************** TAX ************** #
    url(r'^producttaxclass/$', views.product.ProductTaxClass.as_view()),
    url(r'^view_producttaxclass/(?P<pk>[0-9]+)/$', views.product.ProductTaxClass.as_view()),
    url(r'^customertaxclass/$', views.product.CustomerTaxClass.as_view()),
    url(r'^view_customertaxclass/(?P<pk>[0-9]+)/$', views.product.CustomerTaxClass.as_view()),
    url(r'^taxrate/$', views.product.TaxRate.as_view()),
    url(r'^view_taxrate/(?P<pk>[0-9]+)/$', views.product.TaxRate.as_view()),
    url(r'^taxrule/$', views.product.TaxRule.as_view()),
    url(r'^view_taxrule/(?P<pk>[0-9]+)/$', views.product.TaxRule.as_view()),
    url(r'^taxsettings/$', views.product.TaxSettings.as_view()),
    url(r'^taxsettings/(?P<pk>[0-9]+)/$', views.product.TaxSettings.as_view()), 
    # ************** TAX(END) ************** #

    # ************** CUSTOMER ************** # 
    url(r'^customer/(?P<pk>[0-9]+)/$', views.order.CustomerList.as_view()),
    url(r'^customer_add/$', views.order.CustomerAdd.as_view()),
    url(r'^customer_edit/(?P<customer_id>[0-9]+)/$', views.order.CustomerEdit.as_view()),
    url(r'^get_customer_address/(?P<customer_id>[0-9]+)/$', views.order.CustomerAddressFetch.as_view()),
    url(r'^customer_address_setup/$', views.order.CustomerAddressSetup.as_view()),
    url(r'^customer_orderlist/$', views.order.CustomerOrderList.as_view()),
    url(r'^customer_invoicelist/$', views.order.CustomerInvoiceList.as_view()),
    url(r'^customeraddressdelete/$', views.order.CustomerAddressDelete.as_view()),
    url(r'^customeraddresssetprimary/$', views.order.CustomerAddressSetPrimary.as_view()),
    # # Customer Address Information
    # url(r'^cutomersetup/$', views.order.CustomerSetup.as_view()),
    # url(r'^cutomersetup/(?P<pk>[0-9]+)/$', views.order.CustomerSetupList.as_view()),
    # ************** CUSTOMER(END) ************** #




     #***************** ZONE MANAGEMENT *******************#

    url(r'^manager_list/$', ManagerList.as_view(), name='manager_list'), 
    url(r'^manager_list/(?P<pk>[0-9]+)/$', ManagerListWareHouse.as_view(), name='manager_list_warehouse'), 
    url(r'^zone/$', ZoneAdd.as_view(), name='zone_add'),
    
    url(r'^zone_list/$', ZoneAdd.as_view(), name='zone_list'),
    url(r'^zone_list/(?P<pk>[0-9]+)/$', Get_Zone_Idbased.as_view(), name='zone_list_id'),
   
    url(r'^import_zipcodes/$', ZipCodeManager.as_view(), name='import_zipcodes'),
    url(r'^import_area/$', ImportArea.as_view(), name='import_area'),
    url(r'^export_area/$', ExportArea.as_view(), name='export_area'),


    url(r'^zipcode_list/$', Get_Zipcodes.as_view(), name='zipcode_list'),
    url(r'^areaname_list/$', Get_Areanames.as_view(), name='areaname_list'),

   
    #**************** ZONE MANAGEMENT (END) **************#


    #***************** Vehicle Management ****************#
    url(r'^vehicle/$', VehicleMaster.as_view(), name='vehicle_add'), 
    url(r'^vehicle/(?P<pk>[0-9]+)/$', VehicleMaster.as_view(), name='vehicle_details'), 

    #***************** Vehicle Management (Ends)****************#


    #****************** Delivery  Management **************#
    url(r'^delivery_manager/$', DManagerMaster.as_view(), name='manager_add'), 
    url(r'^delivery-manager-list/$', DeliveryManagerLists.as_view(), name='delivery-manager-list'),
    url(r'^delivery-manager-details/(?P<pk>[0-9]+)/$', DeliveryManagerDetails.as_view(), name='delivery-manager-details'),
    url(r'^delivery_slot/$', DeliverySlotManager.as_view(), name='delivery_slot'),
    url(r'^delivery_slot_update/$', DeliverySlotUpdate.as_view(), name='delivery_slot_update'), 
    url(r'^delivery_slot_delete/$', DeliverySlotDelete.as_view(), name='delivery_slot_delete'), 
    url(r'^delivery_slot_list/$', DeliverySlot.DeliverySlotList.as_view(), name='delivery_slot_list'),   

    #****************** Delivery  Management Ends **************#


    #=================== Price Fromula Management ========================
    url(r'^price_formula/$', PriceFormulaManager.as_view(), name='price_formula'),
    url(r'^price_formula-details/(?P<pk>[0-9]+)/$', PriceFormulaManagerDetails.as_view(), name='price_formula-details'),
    #=================== Price Fromula Management Ends ===================

    #******************** ShopOn Credit ***************************#
    url(r'^shop_credit/$', ShopOnGoCreditManager.as_view(), name='shop_credit'),


    #******************** ShopOn Credit Ends ***************************#

    #******************** Get Product Cost ***************************#
    # url(r'^product_cost/$', views.product.ProductCost.as_view(), name='product_cost'),
    #******************** Get Product Cost ***************************#


    # ************** INVENTORY ************** #
    url(r'^import_sheet/$', views.inventory.ImportStockSheet.as_view()),
    url(r'^update_temp_stock/(?P<website_id>[0-9]+)/(?P<company_id>[0-9]+)/$', views.inventory.UpdateTempStock.as_view()),
    url(r'^update_temp_stock_via_cron/(?P<website_id>[0-9]+)/(?P<company_id>[0-9]+)/$', views.inventory.UpdateTempStockViaCron.as_view()),
    # url(r'^update_stock_via_cron/$', views.inventory.UpdateStockViaCron.as_view()),

    url(r'^add_received_product_details/$', views.inventory.AddReceivedPeoductDetails.as_view()),
    
    url(r'^prchaseOrder/grn/(?P<pk>[0-9]+)/$', views.inventory.PurchaseOrderGrnDetails.as_view()),

    # ************** INVENTORY(END) ************** #

    #Global Update
    url(r'^globalupdate/$', views.settings.Globalupdate.as_view()),

    #Global Listing
    url(r'^global_list/$', views.settings.GlobalList.as_view()),
    # url(r'^global_list/(?P<module>[\w-]+)/(?P<pk>[0-9]+)/$', views.settings.GlobalList.as_view()),
    url(r'^global_list/(?P<pk>[0-9]+)/$', views.settings.GlobalList.as_view()),
    url(r'^global_list_filter/$', views.settings.GlobalListFilter.as_view()),  
    url(r'^global_list_export/$', views.settings.GlobalListExport.as_view()), 
    url(r'^grid_layout/$', views.settings.GridLayout.as_view()),
    url(r'^advanced_filter/$', views.settings.AdvancedFilter.as_view()),

    # """ Role """ 
    url(r'^roles/$', views.employee.RoleMasterViewSet.as_view()),
    url(r'^roles/(?P<pk>[0-9]+)/$', views.employee.RoleMasterDetail.as_view()),
    url(r'^role_list/$', views.employee.RoleList.as_view()),
    url(r'^groupname/$', views.employee.Groupname.as_view()),
    url(r'^user_list/$', views.employee.UsersName.as_view()),
    url(r'^get_role_menu/$', views.employee.GetRoleMenu.as_view()),
    url(r'^edit_role/$', views.employee.EditRole.as_view()),
     
    # """ User """ 
     url(r'^users/$', views.employee.UserAction.as_view()),
     url(r'^users/(?P<pk>[0-9]+)/$', views.employee.UserDetail.as_view()),
     url(r'^users_list/$', views.employee.UserList.as_view()),
     url(r'^users_changepass/(?P<pk>[0-9]+)/$', views.employee.UserChangePassword.as_view()),
     url(r'^role_assign/$', views.employee.RoleAssign.as_view()),

    # """ Groups """ 
     url(r'^group/$', views.employee.GroupsAction.as_view()),
     url(r'^group/(?P<pk>[0-9]+)/$', views.employee.GroupsDetail.as_view()),
     url(r'^group_list/$', views.employee.GroupsList.as_view()),
     url(r'^all-active-inactive/$', views.employee.Active.as_view()),

    # """ Elastic Search """
    url(r'^esmenu/$', views.ESMenuViewSet.as_view()),
    url(r'^db_change/$', views.DB.as_view()),
    url(r'^es/$', views.ESMenuActionViewSet.as_view()),
    url(r'^add_data_es/$', views.ESDataActionViewSet.as_view()),
    url(r'^modify_sku/$', views.ModifySku.as_view()),
    url(r'^search_elastic/$', views.ESsearchdata.as_view()),

    
    # Categories
    url(r'^category/$', views.product.CategoriesInfoViewSet.as_view()),
    url(r'^category/(?P<pk>[0-9]+)/$', views.product.CategoriesList.as_view()),
    url(r'^basicinfoload/$', views.product.BasicInfoLoad.as_view()  ),
    url(r'^customfields/$', views.product.customfields.as_view()),
    url(r'^customfields/(?P<pk>[0-9]+)/(?P<cat>[0-9]+)/$', views.product.customfieldsedit.as_view()),
    url(r'^field_list/(?P<category_id>[0-9]+)/(?P<channel_id>[0-9]+)/$', views.product.field_list.as_view()),
    url(r'^customfieldsimport/$', views.product.customfieldsimport.as_view()),
    url(r'^customvalueupdate/$', views.product.customvalueupdate.as_view()),
    url(r'^customfieldsystem/$', views.product.customfieldsystem.as_view()),
    url(r'^categorybanner/$', views.product.CategoryBanner.as_view()),
    url(r'^categorybanner/(?P<pk>[0-9]+)/$', views.product.CategoryBanner.as_view()),
    url(r'^categorybanner_image_delete/$', views.product.CategoryBannerImageDelete.as_view()),
    url(r'^categorybanner-new/$', views.product.CategoryBannerNew.as_view(), name='categorybanner-new'),

    
    # Brands
    url(r'^brand/$', views.product.Brand.as_view()),
    url(r'^brand/(?P<pk>[0-9]+)/$', views.product.BrandList.as_view()),

    # Reviews 
    url(r'^reviews/(?P<pk>[0-9]+)/$', views.product.ReviewsList.as_view()),
    url(r'^reviews/$', views.product.flag.as_view()),
    url(r'^product_reviews/$', views.product.ProductReviews.as_view()),

    # Discount
    url(r'^discount/$', views.product.DiscountSet.as_view()),
    url(r'^discount/(?P<pk>[0-9]+)/$', views.product.DiscountList.as_view()),
    url(r'^discountconditions/$', views.product.DiscountConditions.as_view()),
    # new
    # url(r'^discountconditionsnew/$', views.product.DiscountConditionsNew.as_view()),
    
    url(r'^discountconditions/(?P<pk>[0-9]+)/$', views.product.DiscountConditionsSet.as_view()),
    url(r'^discount_load/(?P<discount_master_id>[0-9]+)/$', views.product.CustomerGroupDiscount.as_view()),
    url(r'^discount_load/$', views.product.CustomerLoed.as_view()),

    #Import Discount
    url(r'^import_discount/$', views.product.ImportFileDiscounts.as_view()),
    url(r'^save_file_discounts/$', views.product.SaveFileDiscounts.as_view()),
    url(r'^preview_save_discounts/$', views.product.PreviewSaveFileDiscounts.as_view()),
    url(r'^save_all_imported_price/$', views.product.SaveAllImportedPrice.as_view()),

    #Import Price
    url(r'^import_price/$', views.product.ImportFilePriceProducts.as_view()),
    # url(r'^fix_img/$', views.product.FixImageProducts.as_view()),
    url(r'^save_file_price/$', views.product.SaveFilePriceData.as_view()),
    url(r'^preview_save_price/$', views.product.PreviewSaveFilePrice.as_view()),
    url(r'^save_all_imported_discounts/$', views.product.SaveAllImportedDiscounts.as_view()),

    #Conditions
    url(r'^discountcouponcondition/$', views.product.DiscountCouponCondition.as_view()),
    url(r'^freediscounts/$', views.product.DiscountProductFree.as_view()),
    url(r'^couponexport/$', views.product.CouponExport.as_view()),

    # Loyalty
    url(r'^loyalty/$', views.order.LoyaltySet.as_view()),
    url(r'^loyalty/(?P<pk>[0-9]+)/$', views.order.LoyaltyList.as_view()),
    url(r'^loyaltyconditions/$', views.order.LoyaltyConditions.as_view()),
    url(r'^loyaltyconditions/(?P<pk>[0-9]+)/$', views.order.LoyaltyConditions.as_view()),

    #Gift Cards
    url(r'^giftcards/$', views.product.GiftCard.as_view()),
    url(r'^giftcards/(?P<pk>[0-9]+)/$', views.product.GiftCard.as_view()),

    #Contact Groups
    url(r'^contact/$', views.product.ContactViewSet.as_view()),
    url(r'^contact/(?P<pk>[0-9]+)/$', views.product.ContactList.as_view()),

    #Contacts
    url(r'^contacts/$', views.product.ContactsSetView.as_view()),
    url(r'^contacts/(?P<pk>[0-9]+)/$', views.product.ContactsList.as_view()),
    url(r'^contacts_list/$', views.product.Contacts.as_view()),

    url(r'^segments/$', views.product.Segments.as_view()),
    url(r'^segments/(?P<pk>[0-9]+)/$', views.product.SegmentsList.as_view()),

    # Payment Methods
    url(r'^payment_method/$', views.inventory.PaymentMethod.as_view()),
    url(r'^payment_method/(?P<pk>[0-9]+)/$', views.inventory.PaymentMethodList.as_view()),
    
    # Shipping Methods
    url(r'^shipping_method/$', views.inventory.ShippingMethod.as_view()),
    url(r'^shipping_method/(?P<pk>[0-9]+)/$', views.inventory.ShippingMethodList.as_view()),

    # Courier

    url(r'^courier/$', views.order.ShippingMaster.as_view()),
    url(r'^courier/(?P<pk>[0-9]+)/$', views.order.ShippingMasterList.as_view()),
    

    # Unit Management

    url(r'^units/$', views.settings.Unitsettings.as_view()),
    url(r'^units/(?P<pk>[0-9]+)/$', views.settings.Unitsettingsup.as_view()),

    # Currency Rate Settings
    url(r'^currencymanagement/$', views.settings.currencysettingsup.as_view()),
    url(r'^basecurrencyset/(?P<pk>[0-9]+)/$', views.settings.BaseCurrencyset.as_view()),


    # Suppliers

    url(r'^suppliers/$', views.inventory.Suppliers.as_view()),
    url(r'^suppliers/(?P<pk>[0-9]+)/$', views.inventory.SuppliersList.as_view()),
    url(r'^Suppliersadd/$', views.inventory.Suppliersadd.as_view()),
    url(r'^po_list/$', views.inventory.SupplierPoList.as_view()),

    url(r'^statelist/(?P<country_id>[0-9]+)/$', views.inventory.statelist.as_view()),

    url(r'^warehouse/$', views.inventory.Warehouse.as_view()),
    url(r'^warehouse_list/$', views.inventory.WarehouseAllList.as_view()),
    url(r'^warehouse/(?P<pk>[0-9]+)/$', views.inventory.WarehouseList.as_view()),

    #-----Binayak Start 02-02-2021-----#
    # url(r'^warehouse_timing/(?P<pk>[0-9]+)/$', views.inventory.WarehouseTiming.as_view()),
    url(r'^update_bulk_elastic_test/(?P<field_name>\w+)/(?P<start>[0-9]+)/(?P<end>[0-9]+)/$', views.common.UpdateBulkElasticCheck.as_view()),
    # url(r'^save_price_from_temp_to_table_test/$', views.product.SavePriceFromTempToTableTest.as_view()),
    #-----Binayak End 02-02-2021-----#

    url(r'^warehouse_price_delete/$', views.inventory.DuplicatePriceRemove.as_view()),

    #-------Tax Settings--


    url(r'^taxsettings/$', views.settings.Taxsettingsview.as_view()),
    url(r'^taxsettingsup/(?P<pk>[0-9]+)/$', views.settings.Taxsettingsup.as_view()),

    #Images
    url(r'^image/$', views.product.Image.as_view()),
    url(r'^positionchange/$', views.product.positionchange.as_view()),
    #Auto Responer
    url(r'^emailnotification/$', views.order.Emailnotification.as_view()),
    url(r'^emailnotification/(?P<pk>[0-9]+)/$', views.order.EmailnotificationList.as_view()),

    url(r'^templatesedit/(?P<pk>[0-9]+)/$', views.settings.TemplatesEdit.as_view()),

    
    url(r'^getchild/$', views.product.Getchild.as_view()),

    #chortcut menus
    url(r'^shortcuts/$', views.shortcuts.ShortcutsViewSet.as_view()),
    url(r'^shortcuts/(?P<pk>[0-9]+)/$', views.shortcuts.ShortcutsListView.as_view()),
    #Product Pricings 
    url(r'^productpriceSet/$', views.product.ProductpriceSet.as_view()),
    url(r'^productpriceSet/(?P<pk>[0-9]+)/(?P<website_id>[0-9]+)/$', views.product.ProductpriceSetView.as_view()),
    url(r'^productpricetype/$', views.product.ProductPriceType.as_view()),
    url(r'^productpricetype/(?P<pk>[0-9]+)/$', views.product.ProductPriceType.as_view()),

    url(r'^pricetype/$', views.product.PriceType.as_view()),
    url(r'^pricetype/(?P<pk>[0-9]+)/$', views.product.PriceType.as_view()),

    url(r'^productpricetypelist/$', views.product.ProductPriceTypeList.as_view()),

    url(r'^productwarehouselist/$', views.product.ProductWareHouse.as_view()),
    url(r'^channelcurrencyproductprice/$', views.product.ChannelCurrencyProductPrice.as_view()),
    url(r'^channelcurrencypricedelete/$', views.product.ChannelCurrencyPriceDelete.as_view()),
    

    # Customer Groups
    url(r'^customersname/$', views.order.Customers.as_view()),
    url(r'^get_customer_name/$', views.employee.CustomerDataFetch.as_view()),
    url(r'^customergroup/$', views.order.CustomerGroup.as_view()),
    url(r'^customergrouplist/(?P<pk>[0-9]+)/$', views.order.CustomerGroupList.as_view()),
    url(r'^channelusers/$', views.settings.Channelusers.as_view()),
    url(r'^channeluserslist/(?P<pk>[0-9]+)/(?P<company_website_id>[0-9]+)/$', views.settings.ChannelusersList.as_view()),
    url(r'^customfieldsimport/$', views.product.customfieldsimport.as_view()),
    url(r'^category_load/$', views.product.CategoryLoed.as_view()),
    url(r'^getchild_category/$', views.product.Getchild_category.as_view()),
    url(r'^productload/$', views.product.ProductLoad.as_view()),
    url(r'^productload-paging/$', views.product.ProductLoadPaging.as_view()),
    url(r'^category_image_delete/$', views.product.ImageDelete.as_view()),

    url(r'^product_image_delete/$', views.product.ProductImageDelete.as_view()),
    url(r'^set_cover_image/$', views.product.SetCoverImage.as_view()),
    url(r'^orders_load_view/$', views.order.OrdersLoadView.as_view()),
    url(r'^promotionscoupon/$', views.order.Promotionscoupon.as_view()),
    url(r'^customsuccessfieldimport/$', views.product.customsuccessfieldimport.as_view()),
    url(r'^customertype/$', views.product.CustomerType.as_view()),
    url(r'^discountcustomer/$', views.product.DiscountCustomer.as_view()),
    url(r'^channelscustomfield/$', views.product.Channelscustomfield.as_view()),
    url(r'^catrgoryconditionsset/$', views.product.CatrgoryConditionsSet.as_view()),
    url(r'^categorieslistdiscount/(?P<pk>[0-9]+)/$', views.product.CategoriesListDiscount.as_view()),
    url(r'^autoresponderviewset/$', views.order.AutoresponderViewSet.as_view()),
    url(r'^categorieslistdiscount/(?P<pk>[0-9]+)/$', views.product.CategoriesListDiscount.as_view()),
    url(r'^purchaseorder/$', views.inventory.PurchaseOrder.as_view()),
    
    url(r'^suppliers_purchase/$', views.inventory.SuppliersDropdown.as_view()),
    url(r'^suppliersaddress/$', views.inventory.SuppliersAddress.as_view()),
    url(r'^supplierslist/$', views.inventory.SuppliersCurrency.as_view()),
    url(r'^suppliersproducts/$', views.inventory.SuppliersProducts.as_view()),
    url(r'^productlist/$', views.product.ProductList.as_view()),
    url(r'^allproductcategoryimages/$', views.product.AllProductImages.as_view()),
    url(r'^basecurrencychange/$', views.settings.BaseCurrencyChange.as_view()),
    url(r'^warehousestockmanagement/$', views.inventory.WarehouseStockManagement.as_view()),
    url(r'^warehousestockmanagement/(?P<pk>[0-9]+)/$', views.inventory.WarehouseStockManagement.as_view()),
    url(r'^warehousestockmanagement/(?P<pk>[0-9]+)/(?P<user_id>[0-9]+)/$', views.inventory.WarehouseStockManagement.as_view()),
    url(r'^stocklist/$', views.inventory.StockList.as_view()),
    url(r'^invoicelist/$', views.order.InvoiceList.as_view()),
    url(r'^stocklistview/$', views.inventory.StockListView.as_view()),
    url(r'^managestockload/$', views.inventory.StockSuppliers.as_view()),
    url(r'^stockmove/$', views.inventory.StockMove.as_view()),
    url(r'^purchaseorderviewlist/(?P<pk>[0-9]+)/$', views.inventory.PurchaseOrderViewList.as_view()),
    url(r'^purchaseorderview/(?P<pk>[0-9]+)/$', views.inventory.PurchaseOrderView.as_view()),
    url(r'^stockadjustmentlist/$', views.inventory.StockAdjustmentList.as_view()),
    url(r'^purchaseorderlist/$', views.inventory.PurchaseOrderList.as_view()),
    url(r'^purchaseordersstatuschange/$', views.inventory.PurchaseOrdersStatusChange.as_view()),
    url(r'^suppliersemail/$', views.inventory.SuppliersEmail.as_view()),
    url(r'^purchaseorderreceived/$', views.inventory.PoReceived.as_view()),
    url(r'^channelmapping/$', views.product.ChannelMapping.as_view()),
    url(r'^child_channel/$', views.product.child.as_view()),
    url(r'^currencyexchangerate/$', views.settings.CurrencyExchangerate.as_view()),
    url(r'^poreceivedget/$', views.inventory.poreceivedget.as_view()),
    url(r'^grnsend/$', views.inventory.GrnSend.as_view()),
    url(r'^updatesafetystock/$', views.inventory.UpdateSafetyStock.as_view()),
    url(r'^warehousesuppliermap/$', views.inventory.WarehouseSupplierMap.as_view()),
    url(r'^warehousesuppliermaplist/$', views.inventory.WarehouseSupplierMapList.as_view()),
    url(r'^warehousesuppliermapdelete/$', views.inventory.WarehouseSupplierMapDelete.as_view()),
    
    url(r'^update-product-stock/$', views.inventory.ProductStockUpdate.as_view(), name='update-product-stock'),
    url(r'^update-product-price/$', views.inventory.ProductPriceUpdate.as_view(), name='update-product-price'),

    url(r'^check-duplicate-price/$', views.inventory.CheckDuplicatePrice.as_view(), name='check-duplicate-price'),
    
    url(r'^save-elastic-user/$', views.common.SaveElasticByUser.as_view(), name='save-elastic-products'),
    url(r'^save-elastic-user-new/$', views.common.SaveElasticByUserNew.as_view(), name='save-elastic-products-new'),
    # Search
    url(r'^autocomplete/$', views.settings.AutoComplete.as_view()),
    #url(r'^autocomplete-frontend/$', csrf_exempt(views.settings.AutoCompleteFrontend.as_view())),

    # url(r'^get_mail_template/$', get_mail_template, name='get_mail_template')
    # **********************  Test ********************
    
    url(r'^test-report/$', views.order.testreport.as_view(), name='test-report'),

    url(r'^currency-by-code/$', views.common.get_currency_details_by_code.as_view(), name='currency-by-code'),
    url(r'^all-language/$', views.common.AllLanguages.as_view(), name='all-language'),

    url(r'^testcron/$', views.cron.image.save_temp_img_to_product, name='testcron'),
    url(r'^stock_cron/$', views.cron.image.product_stock_cron, name='stock_cron'),
    url(r'^category_product_stock/$', views.cron.image.category_product_stock, name='category_product_stock'),

    # *************************  Delivery App ******************************
    url(r'^driver-login/$', views.deliveryapp.DriverLogin, name='driver-login'),
    url(r'^delivery-orders/$', views.deliveryapp.list_order_for_delivery.as_view(), name='delivery-orders'),
    url(r'^driver-checkin/$', views.deliveryapp.driver_checkin_time.as_view(), name='driver-checkin'),
    url(r'^driver-checkout/$', views.deliveryapp.driver_checkout_time.as_view(), name='driver-checkout'),
    url(r'^delivery-attempt/$', views.deliveryapp.delivery_attempt.as_view(), name='delivery-attempt'),
    url(r'^delivery-orders-details/$', views.deliveryapp.delivery_order_details.as_view(), name='delivery-orders-details'),
    url(r'^delivery-status/$', views.deliveryapp.update_delivery_status.as_view(), name='delivery-status'),   
    url(r'^delivery-orders-list/$', views.deliveryapp.delivery_order_list_and_details.as_view(), name='delivery-orders-list'),
    url(r'^notify-order-area/$', views.deliveryapp.notify_order_area.as_view(), name='notify-order-area'),
    url(r'^reshedule-order/$', views.deliveryapp.list_reshedule_order.as_view(), name='reshedule-order'),
    # url(r'^return-orders-details/$', views.deliveryapp.return_delivery_order_details.as_view(), name='return-orders-details'),
    url(r'^return-process/$', views.deliveryapp.ReturnProcess.as_view(), name='return-process'),
    url(r'^return-closed/$', views.deliveryapp.ReturnClosed.as_view(), name='return-closed'),
    url(r'^partial-return/$', views.deliveryapp.PartialReturn.as_view(), name='partial-return'),
    url(r'^add-wallet/$', views.deliveryapp.AddLoyalty.as_view(), name='add-wallet'),
    url(r'^view-wallet/$', views.deliveryapp.ViewLoyalty.as_view(), name='view-wallet'),
    
    

    # *************************  End Delivery App  *************************

    #  Frontend url....contentmanagement - CMS pages....
    url(r'^basic-info-page-load/(?P<pk>.*)/$', views.frontend.Pageloadsettings.as_view()),
    # url(r'^page_url_to_id/', views.contentmanagement.Pageslurtoidload.as_view()),
    url(r'^page_url_to_id/', views.contentmanagement.Pageslurtoidload),
    url(r'^cms_form_data/', views.contentmanagement.PageFormData.as_view()),
    url(r'^all_menu/(?P<pk>[0-9]+)/(?P<website_id>[0-9]+)/$', views.contentmanagement.AllMenu.as_view()),  
    url(r'^category_list/', views.contentmanagement.CategoryList),
    url(r'^parent_category_list/', views.contentmanagement.ParentCategoryList),   
    url(r'^brand_list/', views.contentmanagement.BrandList), 

    url(r'^new_page_create/$', views.contentmanagement.AddPage.as_view()),
    url(r'^page_update/(?P<pk>[0-9]+)/$', views.contentmanagement.EditPage.as_view()),
    url(r'^all_pages/(?P<pk>[0-9]+)/$', views.contentmanagement.LoadPage.as_view()),
    # url(r'^category_list/(?P<website_id>[0-9]+)/$', views.contentmanagement.CategoriesListMenu.as_view()),
    url(r'^create_menu/$', views.contentmanagement.MenuAdd.as_view()),
    url(r'^menu_edit/(?P<pk>[0-9]+)/(?P<flag>[0-9]+)/$', views.contentmanagement.EditMenu.as_view()),
    url(r'^parent_menus/(?P<pk>[0-9]+)/(?P<website_id>[0-9]+)/$', views.contentmanagement.HeaderMenu.as_view()),
    url(r'^add_page_content/', views.contentmanagement.EditPageContent.as_view()),
    url(r'^temp_image_load/', views.contentmanagement.Tempimage.as_view()),
    url(r'^page_search/(?P<pk>[0-9]+)/$', views.contentmanagement.LoadPageByPage.as_view()),

    url(r'^language-data/(?P<pk>[0-9]+)/$', views.settings.LanguageData.as_view()),
    url(r'^language-data/$', views.settings.LanguageData.as_view()),
    # Api for category
    url(r'^parent-category-list/$', views.frontend.category.categoryview.ParentCategoryListView, name='parent-category-list'),
    url(r'^menu_bar/$',views.frontend.category.categoryview.menu_bar,name ='menu_bar'),                        # Shift
    url(r'^footer_menu/$',views.frontend.category.categoryview.footermenu,name ='footer_menu'),                # Shift
    url(r'^shop_by_category/$',views.frontend.category.categoryview.ShopByCategory,name ='shop_by_category'),  # Shift
    url(r'^shop_by_categoryids/$',views.frontend.category.categoryview.ShopByCategoryByCatId,name ='shop_by_categoryids'), # Shift
    # Api for product
    url(r'^best_selling_product/$', views.frontend.product.productview.BestSellingProduct, name='best_selling_product'),
    url(r'^deals_of_the_day/$', views.frontend.product.productview.DealsOfTheDay, name='deals_of_the_day'),
    url(r'^product-list/$',views.frontend.product.productview.CategoryProductListView,name='product-list'),
    
    # Api for category banner
    url(r'^category_banner_for_home/$',views.frontend.banner.bannerview.CategoryBannerForHome,name='category_banner_for_home'),
    #url(r'^category_banner_for_promotion/$',views.frontend.banner.bannerview.CategoryBannerForPromotion,name='category_banner_for_promotion'),
    url(r'^banner_list/$',views.frontend.banner.bannerview.BannerList,name='banner_list'),
    url(r'^cms-content/$',views.frontend.banner.bannerview.CmsContent,name='CmsContent'),
    # ************************   REPORT ***************************************
    url(r'^order-report/$', views.report.OrderReport.as_view(), name='order-report'),
    url(r'^customer-report/$', views.report.CustomerReport.as_view(), name='customer-report'), 
    url(r'^new-customer-report/$', views.report.NewCustomerReport.as_view(), name='new-customer-report'), 
    url(r'^itemwise-order-report/$', views.report.ItemwiseOrderReport.as_view(), name='itemwise-order-report'),
    url(r'^sales-report/$', views.report.SalesReport.as_view(), name='sales-report'),
    url(r'^product-report/$', views.report.ProductReport.as_view(), name='product-report'),

    url(r'^order-report-all/$', views.report.OrderReportAll.as_view(), name='order-report-all'),
    url(r'^export-product-stock/$', views.report.ExportProductStock.as_view(), name='export-product-stock'),
    
    # Testing planner url by chakradhar for testing purpose
    url(r'^make_planner/$', views.order.make_planner, name='make_planner'),
    url(r'^get_grn_products_info/$', views.order.getGrnProductsInfo.as_view()),
    url(r'^save_edit_grn/$', views.order.saveEditGRN.as_view()),
    url(r'^save_edit_price/$', views.order.saveEditPrice.as_view()),
    url(r'^save_substitute_product/$', views.order.saveSubstituteProduct.as_view()),
    # Return order API data...
    url(r'^order_item_return_popup/$', views.order.OrderReturnRequest.as_view()),
    url(r'^order_item_status_change/$', views.order.OrderReturnApprove.as_view()),
    # url(r'^order_return_view/$', views.order.OrderReturnView.as_view()),
    #url(r'^order_return_complete/$', views.order.OrderReturnComplete.as_view()),
    url(r'^view_order_return/(?P<pk>[0-9]+)/$', views.order.ViewOrderReturn.as_view()),
    url(r'^cancel_order_for_refund/$', views.order.CancelOrderRefund.as_view()),
    url(r'^refund_orders/(?P<pk>[0-9]+)/$', views.order.RefundOrders.as_view()),
    url(r'^assign_vehicle_return/$', views.order.AssignVehicleReturn.as_view()),
    url(r'^create_assign_vehicle_return/$', views.order.CreateAssignVehicleReturn.as_view()),
    # Return order API data...

    url(r'^timeline/$', views.order.TimeLine.as_view()),
    url(r'^category_banner/',views.frontend.banner.bannerview.category_banner,name='category_banner'),
    url(r'^listing_filters/$',views.frontend.product.productview.listing_filters,name='listing_filters'),
    ################# api for brandlist##################################################################################
    url(r'^brand_list_by_brandid/$',views.frontend.brand.brandview.BrandListByBrandId,name ='brand_list_by_brandid'),
    
    # ***********************   IMAGE UPLOAD **************************
    url(r'^upload-image/$', views.product.AllImageUpload.as_view(), name='upload-image'),
    ########################################## api for category banner promotion ############################################ 
    url(r'^category-banner-for-promotion/$',views.frontend.banner.bannerview.CategoryBannerForPromotion,name ='category-banner-for-promotion'),
    ########################################## api for category banner promotion ############################################ 

    # *************************  Picking App Webservices ******************************
    url(r'^picker-login/$', views.pickingapp.PickerLogin, name='picker-login'),
    url(r'^picker-logout/$', views.pickingapp.picker_logout.as_view(), name='picker-logout'),
    url(r'^picker-forgot-password/$', views.pickingapp.PickerForgotPassword.as_view()),
    url(r'^picker-reset-password/$', views.pickingapp.PickerResetPassword.as_view()),
    url(r'^picker-dashboard/$', views.pickingapp.PickerDashboard.as_view()),
    url(r'^picker-orderlist/$', views.pickingapp.PickerOrderList.as_view()),
    url(r'^picker-orderdetails/$', views.pickingapp.PickerOrderDetails.as_view()),
    url(r'^picker-generatepicklist/$', views.pickingapp.PickerGeneratePicklist.as_view()),
    url(r'^picker-productlist/$', views.pickingapp.PickerProductList.as_view()),
    url(r'^picker-addmoreproduct/$', views.pickingapp.PickerAddMoreProduct.as_view()),
    url(r'^picker-substituteproductlist/$', views.pickingapp.PickerSubstituteProductList.as_view()),
    url(r'^picker-add-product-as-substitute/$', views.pickingapp.AddProductAsSubstitute.as_view()),
    url(r'^picker-addsubstituteproduct/$', views.pickingapp.PickerAddSubstituteProduct.as_view()),
    url(r'^picker-sendapproval/$', views.pickingapp.PickerSendApproval.as_view()),
    url(r'^picker-acceptapproval/$', views.pickingapp.PickerAcceptApproval.as_view()),
    url(r'^picker-resetsendapproval/$', views.pickingapp.PickerResetSendApproval.as_view()),
    url(r'^picker-picklistproductinfo/$', views.pickingapp.PickerPicklistProductInfo.as_view()),
    url(r'^picker-updatepicklistproductinfo/$', views.pickingapp.PickerUpdatePicklistProductInfo.as_view()),
    url(r'^picker-grn-complete/$', views.pickingapp.PickerGrnComplete.as_view()),
    url(r'^picker-updategrnquantity/$', views.pickingapp.PickerUpdateGrnQuantity.as_view()),
    url(r'^picker-stockcategory/$', views.pickingapp.PickerStockCategory.as_view()),
    url(r'^picker-searchstock/$', views.pickingapp.PickerSearchStock.as_view()),
    url(r'^picker-managestock/$', views.pickingapp.PickerManageStock.as_view()),
    url(r'^picker-searchreturn/$', views.pickingapp.PickerSearchReturn.as_view()),
    url(r'^picker-confirmreturn/$', views.pickingapp.PickerConfirmReturn.as_view()),
    url(r'^picker-orderlistdetails/$', views.pickingapp.PickerOrderListDetails.as_view()),
    url(r'^picker-latestorders/$', views.pickingapp.PickerLatestOrders.as_view()),
    url(r'^picker-sendpushnotification/$', views.pickingapp.PickerSendPushNotification.as_view()),
    url(r'^picker-updateorderdetails/$', views.pickingapp.PickerUpdateOrderDetails.as_view()),
    url(r'^picker-updateorderbillnumber/$', views.pickingapp.PickerUpdateOrderBillNumber.as_view()),
    url(r'^picker-orderdetailscsv/$', views.pickingapp.PickerOrderDetailsCsv.as_view()),

    # url(r'^get_all_zone_wise_slot/$', views.pickingapp.get_all_zone_wise_slot.as_view(), name='get_all_zone_wise_slot'),
    # url(r'^get_all_zone_and_slot_wise_order_list/$', views.pickingapp.get_all_zone_and_slot_wise_order_list.as_view(), name='get_all_zone_and_slot_wise_order_list'),


    #-------------FirebaseNotification Binayak Start--------------#
    # url(r'^device-notification/$', views.common.FirebaseNotification_test.as_view(), name='device-notification'),
    #------Binayak End------#

    # url(r'^grn_mobile/$', views.pickingapp.grn_mobile.as_view(), name='grn_mobile'),
    # url(r'^scan_products/$', views.pickingapp.scan_products.as_view(), name='scan_products'),
    # url(r'^picker_grn_save_as_draft/$', views.pickingapp.picker_grn_save_as_draft.as_view(), name='picker_grn_save_as_draft'),
    # url(r'^picker_grn_complete/$', views.pickingapp.picker_grn_complete.as_view(), name='picker_grn_complete'),
    # url(r'^grn_status/$', views.pickingapp.grn_status.as_view(), name='grn_status'),
    # *************************  Picking App Webservices ******************************
    
    # """---- Shipping Method Setup ----"""
    url(r'^shippingmethodstatus/(?P<website_id>[0-9]+)/(?P<shipping_method_id>[0-9]+)/$', views.settings.ShippingMethodStatus.as_view()),
    url(r'^shippingmethodstatus/$', views.settings.ShippingMethodStatus.as_view()),

    url(r'^storetypeadd/$', views.settings.StoreTypeAdd.as_view()),
    url(r'^storetypeadd/(?P<pk>[0-9]+)/$', views.settings.StoreTypeAdd.as_view()),
    url(r'^get_storetype/$', views.settings.StoreTypeAll.as_view(), name='get_storetype'),
    # url(r'^get_storetype/$', frontapp.views.sitecommon.StoreTypeAll.as_view(), name='get_storetype'),
    url(r'^get_categoryall/$', views.settings.CategoryAll.as_view(), name='get_categoryall'),

    url(r'^payment-method/$', views.settings.PaymentMethodList.as_view(), name='get_paymentmethod_list'),
    url(r'^get_store_type_categories/$', views.settings.GetStoreTypeCategories.as_view(), name='get_store_type_categories'),
    url(r'^saveprice_temp_to_table/$', views.product.saveprice_temp_to_table, name='saveprice_temp_to_table'),
    url(r'^product-sync-manual/$', views.product.ProductSyncManual.as_view(), name='product_sync_manual'),
    url(r'^productwarehouse-desync-manual/(?P<pk>[0-9]+)/$', views.product.ProductDesyncManual.as_view(), name='productwarehouse_desync_manual'),


    url(r'^update_stock_test_cron/(?P<pk>[0-9]+)/$', views.inventory.UpadateStockTestCron.as_view(), name='update_stock_test_cron'),

]

import threading
scheduler = BackgroundScheduler()
scheduler.start()

# scheduler.add_job(views.cron.image.save_temp_img_to_product, 'cron', second=10)
#scheduler.add_job(views.cron.image.product_stock_cron, 'cron', hour = 1)

scheduler.add_job(views.cron.image.ProcessCronQueue, 'interval', minutes=5)


scheduler.add_job(views.product.save_price_from_temp_to_table, 'interval', minutes=15)
scheduler.add_job(views.cron.image.save_temp_img_to_product, 'interval', minutes=10)
scheduler.add_job(views.cron.image.product_stock_cron, 'interval', minutes=10)
scheduler.add_job(views.common.sync_db_seq, 'interval',hours=12, replace_existing=True)
scheduler.add_job(update_ccavenue_order_status_cron, 'interval', minutes=10)
scheduler.add_job(views.cron.image.check_category_product_stock,'cron', day_of_week='mon-sun', hour=20, minute=00, replace_existing=True)
scheduler.add_job(views.cron.image.UpdateDiscountCron, 'cron', day_of_week='mon-sun', hour=22, minute=00, replace_existing=True)
scheduler.add_job(views.cron.image.check_and_update_expired_discounts, 'cron', day_of_week='mon-sun', hour=23, minute=00, replace_existing=True)
scheduler.add_job(views.cron.image.ProductsToElasticCron, 'interval', minutes=30)
# scheduler.add_job(views.inventory.UpadateStockTestCron, 'interval', minutes=1, max_instances=1, replace_existing=False)
# scheduler.add_job(views.cron.image.ProductsToElasticCronResync, 'cron', day_of_week='mon-sun', hour=24, minute=00, replace_existing=True)

# scheduler.add_job(views.cron.image.check_category_product_stock,'cron', day_of_week='mon-sun', hour=10, minute=35, replace_existing=True)
scheduler.print_jobs()