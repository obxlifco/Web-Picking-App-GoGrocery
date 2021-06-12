package com.gogrocery.Models.ApplyLoyaltyResponseModel;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Data {

@SerializedName("id")
@Expose
private Integer id;
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
private Integer websiteId;
@SerializedName("company_id")
@Expose
private Integer companyId;
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
private Integer paymentMethodId;
@SerializedName("payment_type_id")
@Expose
private Integer paymentTypeId;
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
private String billingEmailAddress;
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
private Integer billingState;
@SerializedName("billing_state_name")
@Expose
private String billingStateName;
@SerializedName("billing_country")
@Expose
private Integer billingCountry;
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
private Integer addressBookId;
@SerializedName("delivery_company")
@Expose
private Object deliveryCompany;
@SerializedName("delivery_email_address")
@Expose
private String deliveryEmailAddress;
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
private Integer deliveryState;
@SerializedName("delivery_state_name")
@Expose
private String deliveryStateName;
@SerializedName("delivery_sap_ecustomer_state_no")
@Expose
private Object deliverySapEcustomerStateNo;
@SerializedName("delivery_country")
@Expose
private Integer deliveryCountry;
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
private Object customMsg;
@SerializedName("applied_coupon")
@Expose
private Object appliedCoupon;
@SerializedName("gross_amount")
@Expose
private Integer grossAmount;
@SerializedName("net_amount")
@Expose
private Integer netAmount;
@SerializedName("shipping_cost")
@Expose
private Integer shippingCost;
@SerializedName("shipping_cost_excl_tax")
@Expose
private Object shippingCostExclTax;
@SerializedName("paid_amount")
@Expose
private Integer paidAmount;
@SerializedName("gross_discount_amount")
@Expose
private Integer grossDiscountAmount;
@SerializedName("tax_amount")
@Expose
private Integer taxAmount;
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
private Integer orderStatus;
@SerializedName("buy_status")
@Expose
private Integer buyStatus;
@SerializedName("currency_code")
@Expose
private String currencyCode;
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
private Integer cartDiscount;
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
private Integer codCharge;
@SerializedName("send_notes")
@Expose
private Object sendNotes;
@SerializedName("received_amount")
@Expose
private Object receivedAmount;
@SerializedName("received_status")
@Expose
private String receivedStatus;
@SerializedName("pay_wallet_amount")
@Expose
private Integer payWalletAmount;
@SerializedName("refund_wallet_amount")
@Expose
private Integer refundWalletAmount;
@SerializedName("assign_to")
@Expose
private Integer assignTo;
@SerializedName("assign_wh")
@Expose
private Integer assignWh;
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
private Integer shipmentId;
@SerializedName("zone_id")
@Expose
private Integer zoneId;
@SerializedName("time_slot_date")
@Expose
private String timeSlotDate;
@SerializedName("time_slot_id")
@Expose
private String timeSlotId;
@SerializedName("slot_start_time")
@Expose
private String slotStartTime;
@SerializedName("slot_end_time")
@Expose
private String slotEndTime;
@SerializedName("return_status")
@Expose
private Object returnStatus;
@SerializedName("sort_by_distance")
@Expose
private Integer sortByDistance;
@SerializedName("signature_image")
@Expose
private String signatureImage;
@SerializedName("flag_order")
@Expose
private Integer flagOrder;
@SerializedName("area_id")
@Expose
private Object areaId;
@SerializedName("trent_picklist_id")
@Expose
private Integer trentPicklistId;
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
private String grnCreatedDate;
@SerializedName("shipment_status")
@Expose
private String shipmentStatus;
@SerializedName("rule_id")
@Expose
private Integer ruleId;
@SerializedName("applied_loyalty_amount")
@Expose
private Integer appliedLoyaltyAmount;

public Integer getId() {
return id;
}

public void setId(Integer id) {
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

public Integer getWebsiteId() {
return websiteId;
}

public void setWebsiteId(Integer websiteId) {
this.websiteId = websiteId;
}

public Integer getCompanyId() {
return companyId;
}

public void setCompanyId(Integer companyId) {
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

public Integer getPaymentMethodId() {
return paymentMethodId;
}

public void setPaymentMethodId(Integer paymentMethodId) {
this.paymentMethodId = paymentMethodId;
}

public Integer getPaymentTypeId() {
return paymentTypeId;
}

public void setPaymentTypeId(Integer paymentTypeId) {
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

public String getBillingEmailAddress() {
return billingEmailAddress;
}

public void setBillingEmailAddress(String billingEmailAddress) {
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

public Integer getBillingState() {
return billingState;
}

public void setBillingState(Integer billingState) {
this.billingState = billingState;
}

public String getBillingStateName() {
return billingStateName;
}

public void setBillingStateName(String billingStateName) {
this.billingStateName = billingStateName;
}

public Integer getBillingCountry() {
return billingCountry;
}

public void setBillingCountry(Integer billingCountry) {
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

public Integer getAddressBookId() {
return addressBookId;
}

public void setAddressBookId(Integer addressBookId) {
this.addressBookId = addressBookId;
}

public Object getDeliveryCompany() {
return deliveryCompany;
}

public void setDeliveryCompany(Object deliveryCompany) {
this.deliveryCompany = deliveryCompany;
}

public String getDeliveryEmailAddress() {
return deliveryEmailAddress;
}

public void setDeliveryEmailAddress(String deliveryEmailAddress) {
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

public Integer getDeliveryState() {
return deliveryState;
}

public void setDeliveryState(Integer deliveryState) {
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

public Integer getDeliveryCountry() {
return deliveryCountry;
}

public void setDeliveryCountry(Integer deliveryCountry) {
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

public Object getCustomMsg() {
return customMsg;
}

public void setCustomMsg(Object customMsg) {
this.customMsg = customMsg;
}

public Object getAppliedCoupon() {
return appliedCoupon;
}

public void setAppliedCoupon(Object appliedCoupon) {
this.appliedCoupon = appliedCoupon;
}

public Integer getGrossAmount() {
return grossAmount;
}

public void setGrossAmount(Integer grossAmount) {
this.grossAmount = grossAmount;
}

public Integer getNetAmount() {
return netAmount;
}

public void setNetAmount(Integer netAmount) {
this.netAmount = netAmount;
}

public Integer getShippingCost() {
return shippingCost;
}

public void setShippingCost(Integer shippingCost) {
this.shippingCost = shippingCost;
}

public Object getShippingCostExclTax() {
return shippingCostExclTax;
}

public void setShippingCostExclTax(Object shippingCostExclTax) {
this.shippingCostExclTax = shippingCostExclTax;
}

public Integer getPaidAmount() {
return paidAmount;
}

public void setPaidAmount(Integer paidAmount) {
this.paidAmount = paidAmount;
}

public Integer getGrossDiscountAmount() {
return grossDiscountAmount;
}

public void setGrossDiscountAmount(Integer grossDiscountAmount) {
this.grossDiscountAmount = grossDiscountAmount;
}

public Integer getTaxAmount() {
return taxAmount;
}

public void setTaxAmount(Integer taxAmount) {
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

public Integer getOrderStatus() {
return orderStatus;
}

public void setOrderStatus(Integer orderStatus) {
this.orderStatus = orderStatus;
}

public Integer getBuyStatus() {
return buyStatus;
}

public void setBuyStatus(Integer buyStatus) {
this.buyStatus = buyStatus;
}

public String getCurrencyCode() {
return currencyCode;
}

public void setCurrencyCode(String currencyCode) {
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

public Integer getCartDiscount() {
return cartDiscount;
}

public void setCartDiscount(Integer cartDiscount) {
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

public Integer getCodCharge() {
return codCharge;
}

public void setCodCharge(Integer codCharge) {
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

public Integer getPayWalletAmount() {
return payWalletAmount;
}

public void setPayWalletAmount(Integer payWalletAmount) {
this.payWalletAmount = payWalletAmount;
}

public Integer getRefundWalletAmount() {
return refundWalletAmount;
}

public void setRefundWalletAmount(Integer refundWalletAmount) {
this.refundWalletAmount = refundWalletAmount;
}

public Integer getAssignTo() {
return assignTo;
}

public void setAssignTo(Integer assignTo) {
this.assignTo = assignTo;
}

public Integer getAssignWh() {
return assignWh;
}

public void setAssignWh(Integer assignWh) {
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

public Integer getShipmentId() {
return shipmentId;
}

public void setShipmentId(Integer shipmentId) {
this.shipmentId = shipmentId;
}

public Integer getZoneId() {
return zoneId;
}

public void setZoneId(Integer zoneId) {
this.zoneId = zoneId;
}

public String getTimeSlotDate() {
return timeSlotDate;
}

public void setTimeSlotDate(String timeSlotDate) {
this.timeSlotDate = timeSlotDate;
}

public String getTimeSlotId() {
return timeSlotId;
}

public void setTimeSlotId(String timeSlotId) {
this.timeSlotId = timeSlotId;
}

public String getSlotStartTime() {
return slotStartTime;
}

public void setSlotStartTime(String slotStartTime) {
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

public Integer getSortByDistance() {
return sortByDistance;
}

public void setSortByDistance(Integer sortByDistance) {
this.sortByDistance = sortByDistance;
}

public String getSignatureImage() {
return signatureImage;
}

public void setSignatureImage(String signatureImage) {
this.signatureImage = signatureImage;
}

public Integer getFlagOrder() {
return flagOrder;
}

public void setFlagOrder(Integer flagOrder) {
this.flagOrder = flagOrder;
}

public Object getAreaId() {
return areaId;
}

public void setAreaId(Object areaId) {
this.areaId = areaId;
}

public Integer getTrentPicklistId() {
return trentPicklistId;
}

public void setTrentPicklistId(Integer trentPicklistId) {
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

public String getGrnCreatedDate() {
return grnCreatedDate;
}

public void setGrnCreatedDate(String grnCreatedDate) {
this.grnCreatedDate = grnCreatedDate;
}

public String getShipmentStatus() {
return shipmentStatus;
}

public void setShipmentStatus(String shipmentStatus) {
this.shipmentStatus = shipmentStatus;
}

public Integer getRuleId() {
return ruleId;
}

public void setRuleId(Integer ruleId) {
this.ruleId = ruleId;
}

public Integer getAppliedLoyaltyAmount() {
return appliedLoyaltyAmount;
}

public void setAppliedLoyaltyAmount(Integer appliedLoyaltyAmount) {
this.appliedLoyaltyAmount = appliedLoyaltyAmount;
}

}