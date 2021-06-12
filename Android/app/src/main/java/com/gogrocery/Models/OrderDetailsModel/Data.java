package com.gogrocery.Models.OrderDetailsModel;

import java.util.List;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Data {

    @SerializedName("id")
    @Expose
    private String id;
    @SerializedName("customer")
    @Expose
    private Customer customer;
    @SerializedName("webshop")
    @Expose
    private Webshop webshop;
    @SerializedName("order_products")
    @Expose
    private List<OrderProduct> orderProducts = null;
    @SerializedName("order_payment")
    @Expose
    private List<Object> orderPayment = null;
    @SerializedName("warehouse")
    @Expose
    private List<Warehouse> warehouse = null;
    @SerializedName("website_id")
    @Expose
    private String websiteId;
    @SerializedName("company_id")
    @Expose
    private String companyId;
    @SerializedName("custom_order_id")
    @Expose
    private String customOrderId;
    @SerializedName("channel_order_id")
    @Expose
    private Object channelOrderId;
    @SerializedName("channel_orderlineitem_id")
    @Expose
    private Object channelOrderlineitemId;
    @SerializedName("payment_method_id")
    @Expose
    private String paymentMethodId;
    @SerializedName("payment_type_id")
    @Expose
    private String paymentTypeId;
    @SerializedName("payment_method_name")
    @Expose
    private String paymentMethodName;
    @SerializedName("shipping_method_id")
    @Expose
    private Object shippingMethodId;
    @SerializedName("billing_name")
    @Expose
    private String billingName;
    @SerializedName("billing_company")
    @Expose
    private Object billingCompany;
    @SerializedName("billing_email_address")
    @Expose
    private Object billingEmailAddress;
    @SerializedName("billing_street_address")
    @Expose
    private String billingStreetAddress;
    @SerializedName("billing_street_address1")
    @Expose
    private Object billingStreetAddress1;
    @SerializedName("billing_city")
    @Expose
    private String billingCity;
    @SerializedName("billing_postcode")
    @Expose
    private String billingPostcode;
    @SerializedName("billing_state")
    @Expose
    private String billingState;
    @SerializedName("billing_state_name")
    @Expose
    private String billingStateName;
    @SerializedName("billing_country")
    @Expose
    private String billingCountry;
    @SerializedName("billing_country_name")
    @Expose
    private String billingCountryName;
    @SerializedName("billing_phone")
    @Expose
    private String billingPhone;
    @SerializedName("billing_fax")
    @Expose
    private Object billingFax;
    @SerializedName("delivery_name")
    @Expose
    private String deliveryName;
    @SerializedName("address_book_id")
    @Expose
    private String addressBookId;
    @SerializedName("delivery_company")
    @Expose
    private Object deliveryCompany;
    @SerializedName("delivery_email_address")
    @Expose
    private Object deliveryEmailAddress;
    @SerializedName("delivery_street_address")
    @Expose
    private String deliveryStreetAddress;
    @SerializedName("delivery_street_address1")
    @Expose
    private Object deliveryStreetAddress1;
    @SerializedName("delivery_city")
    @Expose
    private String deliveryCity;
    @SerializedName("delivery_postcode")
    @Expose
    private String deliveryPostcode;
    @SerializedName("delivery_state")
    @Expose
    private String deliveryState;
    @SerializedName("delivery_state_name")
    @Expose
    private String deliveryStateName;
    @SerializedName("delivery_sap_ecustomer_state_no")
    @Expose
    private Object deliverySapEcustomerStateNo;
    @SerializedName("delivery_country")
    @Expose
    private String deliveryCountry;
    @SerializedName("delivery_country_name")
    @Expose
    private String deliveryCountryName;
    @SerializedName("delivery_phone")
    @Expose
    private String deliveryPhone;
    @SerializedName("delivery_fax")
    @Expose
    private Object deliveryFax;
    @SerializedName("custom_msg")
    @Expose
    private String customMsg;
    @SerializedName("applied_coupon")
    @Expose
    private String appliedCoupon;
    @SerializedName("gross_amount")
    @Expose
    private String grossAmount;
    @SerializedName("net_amount")
    @Expose
    private String netAmount;
    @SerializedName("shipping_cost")
    @Expose
    private String shippingCost;
    @SerializedName("shipping_cost_excl_tax")
    @Expose
    private Object shippingCostExclTax;
    @SerializedName("paid_amount")
    @Expose
    private String paidAmount;
    @SerializedName("gross_discount_amount")
    @Expose
    private String grossDiscountAmount;
    @SerializedName("tax_amount")
    @Expose
    private String taxAmount;
    @SerializedName("excise_duty")
    @Expose
    private Object exciseDuty;
    @SerializedName("security_amount")
    @Expose
    private Object securityAmount;
    @SerializedName("gross_amount_base")
    @Expose
    private Object grossAmountBase;
    @SerializedName("net_amount_base")
    @Expose
    private Object netAmountBase;
    @SerializedName("shipping_cost_base")
    @Expose
    private Object shippingCostBase;
    @SerializedName("paid_amount_base")
    @Expose
    private Object paidAmountBase;
    @SerializedName("gross_discount_amount_base")
    @Expose
    private Object grossDiscountAmountBase;
    @SerializedName("order_status")
    @Expose
    private String orderStatus;
    @SerializedName("buy_status")
    @Expose
    private String buyStatus;
    @SerializedName("currency_code")
    @Expose
    private Object currencyCode;
    @SerializedName("ip_address")
    @Expose
    private Object ipAddress;
    @SerializedName("created")
    @Expose
    private String created;
    @SerializedName("modified")
    @Expose
    private String modified;
    @SerializedName("is_mail")
    @Expose
    private Object isMail;
    @SerializedName("tracking_company_name")
    @Expose
    private Object trackingCompanyName;
    @SerializedName("tracking_no")
    @Expose
    private Object trackingNo;
    @SerializedName("tracking_url")
    @Expose
    private Object trackingUrl;
    @SerializedName("campaign_id")
    @Expose
    private Object campaignId;
    @SerializedName("cart_discount")
    @Expose
    private String cartDiscount;
    @SerializedName("tracking_mail_send")
    @Expose
    private Object trackingMailSend;
    @SerializedName("response_msg")
    @Expose
    private Object responseMsg;
    @SerializedName("channel_shipping_status")
    @Expose
    private String channelShippingStatus;
    @SerializedName("fulfillment_id")
    @Expose
    private Object fulfillmentId;
    @SerializedName("cod_charge")
    @Expose
    private String codCharge;
    @SerializedName("send_notes")
    @Expose
    private Object sendNotes;
    @SerializedName("received_amount")
    @Expose
    private Object receivedAmount;
    @SerializedName("received_status")
    @Expose
    private String receivedStatus;
    @SerializedName("mobiquest_point_discount")
    @Expose
    private Object mobiquestPointDiscount;
    @SerializedName("mobiquest_passcode")
    @Expose
    private Object mobiquestPasscode;
    @SerializedName("assign_to")
    @Expose
    private Object assignTo;
    @SerializedName("assign_wh")
    @Expose
    private Object assignWh;
    @SerializedName("tags")
    @Expose
    private Object tags;
    @SerializedName("pay_txntranid")
    @Expose
    private Object payTxntranid;
    @SerializedName("pay_txndate")
    @Expose
    private Object payTxndate;
    @SerializedName("assigned_show_room")
    @Expose
    private Object assignedShowRoom;
    @SerializedName("return_note")
    @Expose
    private Object returnNote;
    @SerializedName("delivery_date")
    @Expose
    private String deliveryDate;
    @SerializedName("expected_delivery_date")
    @Expose
    private Object expectedDeliveryDate;
    @SerializedName("dispatch_date")
    @Expose
    private Object dispatchDate;
    @SerializedName("shipment_id")
    @Expose
    private String shipmentId;
    @SerializedName("zone_id")
    @Expose
    private Object zoneId;
    @SerializedName("time_slot_date")
    @Expose
    private String timeSlotDate;
    @SerializedName("time_slot_id")
    @Expose
    private Object timeSlotId;
    @SerializedName("slot_start_time")
    @Expose
    private Object slotStartTime;
    @SerializedName("slot_end_time")
    @Expose
    private String slotEndTime;
    @SerializedName("return_status")
    @Expose
    private Object returnStatus;
    @SerializedName("sort_by_distance")
    @Expose
    private Object sortByDistance;
    @SerializedName("signature_image")
    @Expose
    private Object signatureImage;
    @SerializedName("flag_order")
    @Expose
    private Object flagOrder;
    @SerializedName("area_id")
    @Expose
    private Object areaId;
    @SerializedName("trent_picklist_id")
    @Expose
    private String trentPicklistId;
    @SerializedName("refferal_code")
    @Expose
    private Object refferalCode;
    @SerializedName("tally_sales_entered")
    @Expose
    private Object tallySalesEntered;
    @SerializedName("order_amount")
    @Expose
    private Object orderAmount;
    @SerializedName("createdby")
    @Expose
    private Object createdby;
    @SerializedName("updatedby")
    @Expose
    private Object updatedby;
    @SerializedName("isblocked")
    @Expose
    private String isblocked;
    @SerializedName("isdeleted")
    @Expose
    private String isdeleted;
    @SerializedName("pos_device_id")
    @Expose
    private Object posDeviceId;
    @SerializedName("grn_created_date")
    @Expose
    private Object grnCreatedDate;

    @SerializedName("pay_wallet_amount")
    @Expose
    private String pay_wallet_amount;

    @SerializedName("loyalty_details")
    @Expose
    private LoyaltyDetails loyaltyDetails;
    @SerializedName("shipment_status")
    @Expose
    private String shipment_status;
    @SerializedName("str_order_status")
    @Expose
    private String strOrderStatus;
    @SerializedName("str_payment_status")
    @Expose
    private String strPaymentStatus;
    @SerializedName("product_discount_price")
    @Expose
    private String product_discount_price;
    @SerializedName("delivery_landmark")
    @Expose
    private String deliveryLandmark;

    public String getProduct_discount_price() {
        return product_discount_price;
    }

    public void setProduct_discount_price(String product_discount_price) {
        this.product_discount_price = product_discount_price;
    }

    public String getStrOrderStatus() {
        return strOrderStatus;
    }

    public void setStrOrderStatus(String strOrderStatus) {
        this.strOrderStatus = strOrderStatus;
    }

    public String getStrPaymentStatus() {
        return strPaymentStatus;
    }

    public void setStrPaymentStatus(String strPaymentStatus) {
        this.strPaymentStatus = strPaymentStatus;
    }

    public LoyaltyDetails getLoyaltyDetails() {
        return loyaltyDetails;
    }

    public void setLoyaltyDetails(LoyaltyDetails loyaltyDetails) {
        this.loyaltyDetails = loyaltyDetails;
    }

    public String getPay_wallet_amount() {
        return pay_wallet_amount;
    }

    public void setPay_wallet_amount(String pay_wallet_amount) {
        this.pay_wallet_amount = pay_wallet_amount;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Customer getCustomer() {
        return customer;
    }

    public void setCustomer(Customer customer) {
        this.customer = customer;
    }

    public Webshop getWebshop() {
        return webshop;
    }

    public void setWebshop(Webshop webshop) {
        this.webshop = webshop;
    }

    public List<OrderProduct> getOrderProducts() {
        return orderProducts;
    }

    public void setOrderProducts(List<OrderProduct> orderProducts) {
        this.orderProducts = orderProducts;
    }

    public List<Object> getOrderPayment() {
        return orderPayment;
    }

    public void setOrderPayment(List<Object> orderPayment) {
        this.orderPayment = orderPayment;
    }

    public List<Warehouse> getWarehouse() {
        return warehouse;
    }

    public void setWarehouse(List<Warehouse> warehouse) {
        this.warehouse = warehouse;
    }

    public String getWebsiteId() {
        return websiteId;
    }

    public void setWebsiteId(String websiteId) {
        this.websiteId = websiteId;
    }

    public String getCompanyId() {
        return companyId;
    }

    public void setCompanyId(String companyId) {
        this.companyId = companyId;
    }

    public String getCustomOrderId() {
        return customOrderId;
    }

    public void setCustomOrderId(String customOrderId) {
        this.customOrderId = customOrderId;
    }

    public Object getChannelOrderId() {
        return channelOrderId;
    }

    public void setChannelOrderId(Object channelOrderId) {
        this.channelOrderId = channelOrderId;
    }

    public Object getChannelOrderlineitemId() {
        return channelOrderlineitemId;
    }

    public void setChannelOrderlineitemId(Object channelOrderlineitemId) {
        this.channelOrderlineitemId = channelOrderlineitemId;
    }

    public String getPaymentMethodId() {
        return paymentMethodId;
    }

    public void setPaymentMethodId(String paymentMethodId) {
        this.paymentMethodId = paymentMethodId;
    }

    public String getPaymentTypeId() {
        return paymentTypeId;
    }

    public void setPaymentTypeId(String paymentTypeId) {
        this.paymentTypeId = paymentTypeId;
    }

    public String getPaymentMethodName() {
        return paymentMethodName;
    }

    public void setPaymentMethodName(String paymentMethodName) {
        this.paymentMethodName = paymentMethodName;
    }

    public Object getShippingMethodId() {
        return shippingMethodId;
    }

    public void setShippingMethodId(Object shippingMethodId) {
        this.shippingMethodId = shippingMethodId;
    }

    public String getBillingName() {
        return billingName;
    }

    public void setBillingName(String billingName) {
        this.billingName = billingName;
    }

    public Object getBillingCompany() {
        return billingCompany;
    }

    public void setBillingCompany(Object billingCompany) {
        this.billingCompany = billingCompany;
    }

    public Object getBillingEmailAddress() {
        return billingEmailAddress;
    }

    public void setBillingEmailAddress(Object billingEmailAddress) {
        this.billingEmailAddress = billingEmailAddress;
    }

    public String getBillingStreetAddress() {
        return billingStreetAddress;
    }

    public void setBillingStreetAddress(String billingStreetAddress) {
        this.billingStreetAddress = billingStreetAddress;
    }

    public Object getBillingStreetAddress1() {
        return billingStreetAddress1;
    }

    public void setBillingStreetAddress1(Object billingStreetAddress1) {
        this.billingStreetAddress1 = billingStreetAddress1;
    }

    public String getBillingCity() {
        return billingCity;
    }

    public void setBillingCity(String billingCity) {
        this.billingCity = billingCity;
    }

    public String getBillingPostcode() {
        return billingPostcode;
    }

    public void setBillingPostcode(String billingPostcode) {
        this.billingPostcode = billingPostcode;
    }

    public String getBillingState() {
        return billingState;
    }

    public void setBillingState(String billingState) {
        this.billingState = billingState;
    }

    public String getBillingStateName() {
        return billingStateName;
    }

    public void setBillingStateName(String billingStateName) {
        this.billingStateName = billingStateName;
    }

    public String getBillingCountry() {
        return billingCountry;
    }

    public void setBillingCountry(String billingCountry) {
        this.billingCountry = billingCountry;
    }

    public String getBillingCountryName() {
        return billingCountryName;
    }

    public void setBillingCountryName(String billingCountryName) {
        this.billingCountryName = billingCountryName;
    }

    public String getBillingPhone() {
        return billingPhone;
    }

    public void setBillingPhone(String billingPhone) {
        this.billingPhone = billingPhone;
    }

    public Object getBillingFax() {
        return billingFax;
    }

    public void setBillingFax(Object billingFax) {
        this.billingFax = billingFax;
    }

    public String getDeliveryName() {
        return deliveryName;
    }

    public void setDeliveryName(String deliveryName) {
        this.deliveryName = deliveryName;
    }

    public String getAddressBookId() {
        return addressBookId;
    }

    public void setAddressBookId(String addressBookId) {
        this.addressBookId = addressBookId;
    }

    public Object getDeliveryCompany() {
        return deliveryCompany;
    }

    public void setDeliveryCompany(Object deliveryCompany) {
        this.deliveryCompany = deliveryCompany;
    }

    public Object getDeliveryEmailAddress() {
        return deliveryEmailAddress;
    }

    public void setDeliveryEmailAddress(Object deliveryEmailAddress) {
        this.deliveryEmailAddress = deliveryEmailAddress;
    }

    public String getDeliveryStreetAddress() {
        return deliveryStreetAddress;
    }

    public void setDeliveryStreetAddress(String deliveryStreetAddress) {
        this.deliveryStreetAddress = deliveryStreetAddress;
    }

    public Object getDeliveryStreetAddress1() {
        return deliveryStreetAddress1;
    }

    public void setDeliveryStreetAddress1(Object deliveryStreetAddress1) {
        this.deliveryStreetAddress1 = deliveryStreetAddress1;
    }

    public String getDeliveryCity() {
        return deliveryCity;
    }

    public void setDeliveryCity(String deliveryCity) {
        this.deliveryCity = deliveryCity;
    }

    public String getDeliveryPostcode() {
        return deliveryPostcode;
    }

    public void setDeliveryPostcode(String deliveryPostcode) {
        this.deliveryPostcode = deliveryPostcode;
    }

    public String getDeliveryState() {
        return deliveryState;
    }

    public void setDeliveryState(String deliveryState) {
        this.deliveryState = deliveryState;
    }

    public String getDeliveryStateName() {
        return deliveryStateName;
    }

    public void setDeliveryStateName(String deliveryStateName) {
        this.deliveryStateName = deliveryStateName;
    }

    public Object getDeliverySapEcustomerStateNo() {
        return deliverySapEcustomerStateNo;
    }

    public void setDeliverySapEcustomerStateNo(Object deliverySapEcustomerStateNo) {
        this.deliverySapEcustomerStateNo = deliverySapEcustomerStateNo;
    }

    public String getDeliveryCountry() {
        return deliveryCountry;
    }

    public void setDeliveryCountry(String deliveryCountry) {
        this.deliveryCountry = deliveryCountry;
    }

    public String getDeliveryCountryName() {
        return deliveryCountryName;
    }

    public void setDeliveryCountryName(String deliveryCountryName) {
        this.deliveryCountryName = deliveryCountryName;
    }

    public String getDeliveryPhone() {
        return deliveryPhone;
    }

    public void setDeliveryPhone(String deliveryPhone) {
        this.deliveryPhone = deliveryPhone;
    }

    public Object getDeliveryFax() {
        return deliveryFax;
    }

    public void setDeliveryFax(Object deliveryFax) {
        this.deliveryFax = deliveryFax;
    }

    public String getCustomMsg() {
        return customMsg;
    }

    public void setCustomMsg(String customMsg) {
        this.customMsg = customMsg;
    }

    public String getAppliedCoupon() {
        return appliedCoupon;
    }

    public void setAppliedCoupon(String appliedCoupon) {
        this.appliedCoupon = appliedCoupon;
    }

    public String getGrossAmount() {
        return grossAmount;
    }

    public void setGrossAmount(String grossAmount) {
        this.grossAmount = grossAmount;
    }

    public String getNetAmount() {
        return netAmount;
    }

    public void setNetAmount(String netAmount) {
        this.netAmount = netAmount;
    }

    public String getShippingCost() {
        return shippingCost;
    }

    public void setShippingCost(String shippingCost) {
        this.shippingCost = shippingCost;
    }

    public Object getShippingCostExclTax() {
        return shippingCostExclTax;
    }

    public void setShippingCostExclTax(Object shippingCostExclTax) {
        this.shippingCostExclTax = shippingCostExclTax;
    }

    public String getPaidAmount() {
        return paidAmount;
    }

    public void setPaidAmount(String paidAmount) {
        this.paidAmount = paidAmount;
    }

    public String getGrossDiscountAmount() {
        return grossDiscountAmount;
    }

    public void setGrossDiscountAmount(String grossDiscountAmount) {
        this.grossDiscountAmount = grossDiscountAmount;
    }

    public String getTaxAmount() {
        return taxAmount;
    }

    public void setTaxAmount(String taxAmount) {
        this.taxAmount = taxAmount;
    }

    public Object getExciseDuty() {
        return exciseDuty;
    }

    public void setExciseDuty(Object exciseDuty) {
        this.exciseDuty = exciseDuty;
    }

    public Object getSecurityAmount() {
        return securityAmount;
    }

    public void setSecurityAmount(Object securityAmount) {
        this.securityAmount = securityAmount;
    }

    public Object getGrossAmountBase() {
        return grossAmountBase;
    }

    public void setGrossAmountBase(Object grossAmountBase) {
        this.grossAmountBase = grossAmountBase;
    }

    public Object getNetAmountBase() {
        return netAmountBase;
    }

    public void setNetAmountBase(Object netAmountBase) {
        this.netAmountBase = netAmountBase;
    }

    public Object getShippingCostBase() {
        return shippingCostBase;
    }

    public void setShippingCostBase(Object shippingCostBase) {
        this.shippingCostBase = shippingCostBase;
    }

    public Object getPaidAmountBase() {
        return paidAmountBase;
    }

    public void setPaidAmountBase(Object paidAmountBase) {
        this.paidAmountBase = paidAmountBase;
    }

    public Object getGrossDiscountAmountBase() {
        return grossDiscountAmountBase;
    }

    public void setGrossDiscountAmountBase(Object grossDiscountAmountBase) {
        this.grossDiscountAmountBase = grossDiscountAmountBase;
    }

    public String getOrderStatus() {
        return orderStatus;
    }

    public void setOrderStatus(String orderStatus) {
        this.orderStatus = orderStatus;
    }

    public String getBuyStatus() {
        return buyStatus;
    }

    public void setBuyStatus(String buyStatus) {
        this.buyStatus = buyStatus;
    }

    public Object getCurrencyCode() {
        return currencyCode;
    }

    public void setCurrencyCode(Object currencyCode) {
        this.currencyCode = currencyCode;
    }

    public Object getIpAddress() {
        return ipAddress;
    }

    public void setIpAddress(Object ipAddress) {
        this.ipAddress = ipAddress;
    }

    public String getCreated() {
        return created;
    }

    public void setCreated(String created) {
        this.created = created;
    }

    public String getModified() {
        return modified;
    }

    public void setModified(String modified) {
        this.modified = modified;
    }

    public Object getIsMail() {
        return isMail;
    }

    public void setIsMail(Object isMail) {
        this.isMail = isMail;
    }

    public Object getTrackingCompanyName() {
        return trackingCompanyName;
    }

    public void setTrackingCompanyName(Object trackingCompanyName) {
        this.trackingCompanyName = trackingCompanyName;
    }

    public Object getTrackingNo() {
        return trackingNo;
    }

    public void setTrackingNo(Object trackingNo) {
        this.trackingNo = trackingNo;
    }

    public Object getTrackingUrl() {
        return trackingUrl;
    }

    public void setTrackingUrl(Object trackingUrl) {
        this.trackingUrl = trackingUrl;
    }

    public Object getCampaignId() {
        return campaignId;
    }

    public void setCampaignId(Object campaignId) {
        this.campaignId = campaignId;
    }

    public String getCartDiscount() {
        return cartDiscount;
    }

    public void setCartDiscount(String cartDiscount) {
        this.cartDiscount = cartDiscount;
    }

    public Object getTrackingMailSend() {
        return trackingMailSend;
    }

    public void setTrackingMailSend(Object trackingMailSend) {
        this.trackingMailSend = trackingMailSend;
    }

    public Object getResponseMsg() {
        return responseMsg;
    }

    public void setResponseMsg(Object responseMsg) {
        this.responseMsg = responseMsg;
    }

    public String getChannelShippingStatus() {
        return channelShippingStatus;
    }

    public void setChannelShippingStatus(String channelShippingStatus) {
        this.channelShippingStatus = channelShippingStatus;
    }

    public Object getFulfillmentId() {
        return fulfillmentId;
    }

    public void setFulfillmentId(Object fulfillmentId) {
        this.fulfillmentId = fulfillmentId;
    }

    public String getCodCharge() {
        return codCharge;
    }

    public void setCodCharge(String codCharge) {
        this.codCharge = codCharge;
    }

    public Object getSendNotes() {
        return sendNotes;
    }

    public void setSendNotes(Object sendNotes) {
        this.sendNotes = sendNotes;
    }

    public Object getReceivedAmount() {
        return receivedAmount;
    }

    public void setReceivedAmount(Object receivedAmount) {
        this.receivedAmount = receivedAmount;
    }

    public String getReceivedStatus() {
        return receivedStatus;
    }

    public void setReceivedStatus(String receivedStatus) {
        this.receivedStatus = receivedStatus;
    }

    public Object getMobiquestPointDiscount() {
        return mobiquestPointDiscount;
    }

    public void setMobiquestPointDiscount(Object mobiquestPointDiscount) {
        this.mobiquestPointDiscount = mobiquestPointDiscount;
    }

    public Object getMobiquestPasscode() {
        return mobiquestPasscode;
    }

    public void setMobiquestPasscode(Object mobiquestPasscode) {
        this.mobiquestPasscode = mobiquestPasscode;
    }

    public Object getAssignTo() {
        return assignTo;
    }

    public void setAssignTo(Object assignTo) {
        this.assignTo = assignTo;
    }

    public Object getAssignWh() {
        return assignWh;
    }

    public void setAssignWh(Object assignWh) {
        this.assignWh = assignWh;
    }

    public Object getTags() {
        return tags;
    }

    public void setTags(Object tags) {
        this.tags = tags;
    }

    public Object getPayTxntranid() {
        return payTxntranid;
    }

    public void setPayTxntranid(Object payTxntranid) {
        this.payTxntranid = payTxntranid;
    }

    public Object getPayTxndate() {
        return payTxndate;
    }

    public void setPayTxndate(Object payTxndate) {
        this.payTxndate = payTxndate;
    }

    public Object getAssignedShowRoom() {
        return assignedShowRoom;
    }

    public void setAssignedShowRoom(Object assignedShowRoom) {
        this.assignedShowRoom = assignedShowRoom;
    }

    public Object getReturnNote() {
        return returnNote;
    }

    public void setReturnNote(Object returnNote) {
        this.returnNote = returnNote;
    }

    public String getDeliveryDate() {
        return deliveryDate;
    }

    public void setDeliveryDate(String deliveryDate) {
        this.deliveryDate = deliveryDate;
    }

    public Object getExpectedDeliveryDate() {
        return expectedDeliveryDate;
    }

    public void setExpectedDeliveryDate(Object expectedDeliveryDate) {
        this.expectedDeliveryDate = expectedDeliveryDate;
    }

    public Object getDispatchDate() {
        return dispatchDate;
    }

    public void setDispatchDate(Object dispatchDate) {
        this.dispatchDate = dispatchDate;
    }

    public String getShipmentId() {
        return shipmentId;
    }

    public void setShipmentId(String shipmentId) {
        this.shipmentId = shipmentId;
    }

    public Object getZoneId() {
        return zoneId;
    }

    public void setZoneId(Object zoneId) {
        this.zoneId = zoneId;
    }

    public String getTimeSlotDate() {
        return timeSlotDate;
    }

    public void setTimeSlotDate(String timeSlotDate) {
        this.timeSlotDate = timeSlotDate;
    }

    public Object getTimeSlotId() {
        return timeSlotId;
    }

    public void setTimeSlotId(Object timeSlotId) {
        this.timeSlotId = timeSlotId;
    }

    public Object getSlotStartTime() {
        return slotStartTime;
    }

    public void setSlotStartTime(Object slotStartTime) {
        this.slotStartTime = slotStartTime;
    }

    public String getSlotEndTime() {
        return slotEndTime;
    }

    public void setSlotEndTime(String slotEndTime) {
        this.slotEndTime = slotEndTime;
    }

    public Object getReturnStatus() {
        return returnStatus;
    }

    public void setReturnStatus(Object returnStatus) {
        this.returnStatus = returnStatus;
    }

    public Object getSortByDistance() {
        return sortByDistance;
    }

    public void setSortByDistance(Object sortByDistance) {
        this.sortByDistance = sortByDistance;
    }

    public Object getSignatureImage() {
        return signatureImage;
    }

    public void setSignatureImage(Object signatureImage) {
        this.signatureImage = signatureImage;
    }

    public Object getFlagOrder() {
        return flagOrder;
    }

    public void setFlagOrder(Object flagOrder) {
        this.flagOrder = flagOrder;
    }

    public Object getAreaId() {
        return areaId;
    }

    public void setAreaId(Object areaId) {
        this.areaId = areaId;
    }

    public String getTrentPicklistId() {
        return trentPicklistId;
    }

    public void setTrentPicklistId(String trentPicklistId) {
        this.trentPicklistId = trentPicklistId;
    }

    public Object getRefferalCode() {
        return refferalCode;
    }

    public void setRefferalCode(Object refferalCode) {
        this.refferalCode = refferalCode;
    }

    public Object getTallySalesEntered() {
        return tallySalesEntered;
    }

    public void setTallySalesEntered(Object tallySalesEntered) {
        this.tallySalesEntered = tallySalesEntered;
    }

    public Object getOrderAmount() {
        return orderAmount;
    }

    public void setOrderAmount(Object orderAmount) {
        this.orderAmount = orderAmount;
    }

    public Object getCreatedby() {
        return createdby;
    }

    public void setCreatedby(Object createdby) {
        this.createdby = createdby;
    }

    public Object getUpdatedby() {
        return updatedby;
    }

    public void setUpdatedby(Object updatedby) {
        this.updatedby = updatedby;
    }

    public String getIsblocked() {
        return isblocked;
    }

    public void setIsblocked(String isblocked) {
        this.isblocked = isblocked;
    }

    public String getIsdeleted() {
        return isdeleted;
    }

    public void setIsdeleted(String isdeleted) {
        this.isdeleted = isdeleted;
    }

    public Object getPosDeviceId() {
        return posDeviceId;
    }

    public void setPosDeviceId(Object posDeviceId) {
        this.posDeviceId = posDeviceId;
    }

    public Object getGrnCreatedDate() {
        return grnCreatedDate;
    }

    public void setGrnCreatedDate(Object grnCreatedDate) {
        this.grnCreatedDate = grnCreatedDate;
    }

    public String getShipment_status() {
        return shipment_status;
    }

    public void setShipment_status(String shipment_status) {
        this.shipment_status = shipment_status;
    }

    public String getDeliveryLandmark() {
        return deliveryLandmark;
    }

    public void setDeliveryLandmark(String deliveryLandmark) {
        this.deliveryLandmark = deliveryLandmark;
    }
}