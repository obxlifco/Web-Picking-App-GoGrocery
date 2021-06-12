package com.gogrocery.Models.MyOrdersFromMailModel;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class MyOrdersFromMailData {

@SerializedName("id")
@Expose
private String id;
@SerializedName("customer")
@Expose
private Customer customer;
@SerializedName("order_products")
@Expose
private List<OrderProduct> orderProducts = null;
@SerializedName("custom_order_id")
@Expose
private String customOrderId;
@SerializedName("payment_method_id")
@Expose
private String paymentMethodId;
@SerializedName("payment_type_id")
@Expose
private String paymentTypeId;
@SerializedName("payment_method_name")
@Expose
private String paymentMethodName;
@SerializedName("billing_name")
@Expose
private String billingName;
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
private Object billingCity;
@SerializedName("billing_postcode")
@Expose
private Object billingPostcode;
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
private String deliveryEmailAddress;
@SerializedName("delivery_street_address")
@Expose
private String deliveryStreetAddress;
@SerializedName("delivery_street_address1")
@Expose
private Object deliveryStreetAddress1;
@SerializedName("delivery_city")
@Expose
private Object deliveryCity;
@SerializedName("delivery_postcode")
@Expose
private Object deliveryPostcode;
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
private Object customMsg;
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
@SerializedName("order_status")
@Expose
private String orderStatus;
@SerializedName("buy_status")
@Expose
private String buyStatus;
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
@SerializedName("cart_discount")
@Expose
private String cartDiscount;
@SerializedName("channel_shipping_status")
@Expose
private String channelShippingStatus;
@SerializedName("received_status")
@Expose
private String receivedStatus;
@SerializedName("pay_wallet_amount")
@Expose
private String payWalletAmount;
@SerializedName("refund_wallet_amount")
@Expose
private String refundWalletAmount;
@SerializedName("assign_to")
@Expose
private String assignTo;
@SerializedName("assign_wh")
@Expose
private String assignWh;
@SerializedName("shipment_id")
@Expose
private String shipmentId;
@SerializedName("zone_id")
@Expose
private String zoneId;
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
@SerializedName("trent_picklist_id")
@Expose
private String trentPicklistId;
@SerializedName("grn_created_date")
@Expose
private String grnCreatedDate;
@SerializedName("shipment_status")
@Expose
private String shipmentStatus;

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

public List<OrderProduct> getOrderProducts() {
return orderProducts;
}

public void setOrderProducts(List<OrderProduct> orderProducts) {
this.orderProducts = orderProducts;
}

public String getCustomOrderId() {
return customOrderId;
}

public void setCustomOrderId(String customOrderId) {
this.customOrderId = customOrderId;
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

public String getBillingName() {
return billingName;
}

public void setBillingName(String billingName) {
this.billingName = billingName;
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

public Object getBillingCity() {
return billingCity;
}

public void setBillingCity(Object billingCity) {
this.billingCity = billingCity;
}

public Object getBillingPostcode() {
return billingPostcode;
}

public void setBillingPostcode(Object billingPostcode) {
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

public Object getDeliveryCity() {
return deliveryCity;
}

public void setDeliveryCity(Object deliveryCity) {
this.deliveryCity = deliveryCity;
}

public Object getDeliveryPostcode() {
return deliveryPostcode;
}

public void setDeliveryPostcode(Object deliveryPostcode) {
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

public Object getCustomMsg() {
return customMsg;
}

public void setCustomMsg(Object customMsg) {
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

public String getCartDiscount() {
return cartDiscount;
}

public void setCartDiscount(String cartDiscount) {
this.cartDiscount = cartDiscount;
}

public String getChannelShippingStatus() {
return channelShippingStatus;
}

public void setChannelShippingStatus(String channelShippingStatus) {
this.channelShippingStatus = channelShippingStatus;
}

public String getReceivedStatus() {
return receivedStatus;
}

public void setReceivedStatus(String receivedStatus) {
this.receivedStatus = receivedStatus;
}

public String getPayWalletAmount() {
return payWalletAmount;
}

public void setPayWalletAmount(String payWalletAmount) {
this.payWalletAmount = payWalletAmount;
}

public String getRefundWalletAmount() {
return refundWalletAmount;
}

public void setRefundWalletAmount(String refundWalletAmount) {
this.refundWalletAmount = refundWalletAmount;
}

public String getAssignTo() {
return assignTo;
}

public void setAssignTo(String assignTo) {
this.assignTo = assignTo;
}

public String getAssignWh() {
return assignWh;
}

public void setAssignWh(String assignWh) {
this.assignWh = assignWh;
}

public String getShipmentId() {
return shipmentId;
}

public void setShipmentId(String shipmentId) {
this.shipmentId = shipmentId;
}

public String getZoneId() {
return zoneId;
}

public void setZoneId(String zoneId) {
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

public String getTrentPicklistId() {
return trentPicklistId;
}

public void setTrentPicklistId(String trentPicklistId) {
this.trentPicklistId = trentPicklistId;
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

}