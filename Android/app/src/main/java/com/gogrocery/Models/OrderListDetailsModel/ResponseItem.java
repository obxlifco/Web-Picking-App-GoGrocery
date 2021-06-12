package com.gogrocery.Models.OrderListDetailsModel;

import java.util.List;
import com.google.gson.annotations.SerializedName;

public class ResponseItem{

	@SerializedName("tracking_mail_send")
	private Object trackingMailSend;

	@SerializedName("delivery_company")
	private Object deliveryCompany;

	@SerializedName("channel_order_id")
	private Object channelOrderId;

	@SerializedName("custom_msg")
	private String customMsg;

	@SerializedName("tally_sales_entered")
	private Object tallySalesEntered;

	@SerializedName("isdeleted")
	private String isdeleted;

	@SerializedName("order_status")
	private int orderStatus;

	@SerializedName("picker_name")
	private Object pickerName;

	@SerializedName("cod_charge")
	private int codCharge;

	@SerializedName("billing_state_name")
	private String billingStateName;

	@SerializedName("time_slot_date")
	private String timeSlotDate;

	@SerializedName("id")
	private int id;

	@SerializedName("payment_type_id")
	private int paymentTypeId;

	@SerializedName("order_shipment")
	private OrderShipment orderShipment;

	@SerializedName("gross_discount_amount")
	private String grossDiscountAmount;

	@SerializedName("tracking_company_name")
	private Object trackingCompanyName;

	@SerializedName("delivery_phone")
	private String deliveryPhone;

	@SerializedName("shipping_method_id")
	private Object shippingMethodId;

	@SerializedName("delivery_state")
	private int deliveryState;

	@SerializedName("shipment_id")
	private int shipmentId;

	@SerializedName("sort_by_distance")
	private Object sortByDistance;

	@SerializedName("grn_created_date")
	private Object grnCreatedDate;

	@SerializedName("shipping_cost_base")
	private Object shippingCostBase;

	@SerializedName("tags")
	private Object tags;

	@SerializedName("billing_postcode")
	private Object billingPostcode;

	@SerializedName("paid_amount")
	private String paidAmount;

	@SerializedName("flag_order")
	private Object flagOrder;

	@SerializedName("trent_picklist_id")
	private int trentPicklistId;

	@SerializedName("maximum_substitute_limit")
	private int maximumSubstituteLimit;

	@SerializedName("delivery_name")
	private String deliveryName;

	@SerializedName("send_notes")
	private Object sendNotes;

	@SerializedName("assign_to")
	private int assignTo;

	@SerializedName("pay_txntranid")
	private Object payTxntranid;

	@SerializedName("cart_discount")
	private String cartDiscount;

	@SerializedName("security_amount")
	private Object securityAmount;

	@SerializedName("refund_wallet_amount")
	private String refundWalletAmount;

	@SerializedName("minimum_substitute_limit")
	private int minimumSubstituteLimit;

	@SerializedName("custom_order_id")
	private String customOrderId;

	@SerializedName("currency_code")
	private String currencyCode;

	@SerializedName("response_msg")
	private Object responseMsg;

	@SerializedName("assign_to_name")
	private String assignToName;

	@SerializedName("order_products")
	private List<OrderProductsItem> orderProducts;

	@SerializedName("billing_state")
	private int billingState;

	@SerializedName("substitute_approval_time")
	private int substitute_approval_time;

	@SerializedName("delivery_email_address")
	private String deliveryEmailAddress;

	@SerializedName("tracking_url")
	private Object trackingUrl;

	@SerializedName("delivery_country_name")
	private String deliveryCountryName;

	@SerializedName("company_id")
	private int companyId;

	@SerializedName("delivery_street_address1")
	private Object deliveryStreetAddress1;

	@SerializedName("order_activity")
	private List<OrderActivityItem> orderActivity;

	@SerializedName("billing_country")
	private int billingCountry;

	@SerializedName("net_amount_base")
	private double netAmountBase;

	@SerializedName("refferal_code")
	private Object refferalCode;

	@SerializedName("payment_method_name")
	private String paymentMethodName;

	@SerializedName("delivery_sap_ecustomer_state_no")
	private Object deliverySapEcustomerStateNo;

	@SerializedName("assigned_show_room")
	private Object assignedShowRoom;

	@SerializedName("isblocked")
	private String isblocked;

	@SerializedName("shipping_cost_excl_tax")
	private Object shippingCostExclTax;

	@SerializedName("gross_amount_base")
	private double grossAmountBase;

	@SerializedName("channel_shipping_status")
	private String channelShippingStatus;

	@SerializedName("delivery_postcode")
	private Object deliveryPostcode;

	@SerializedName("delivery_state_name")
	private String deliveryStateName;

	@SerializedName("delivery_city")
	private Object deliveryCity;

	@SerializedName("pay_wallet_amount")
	private String payWalletAmount;

	@SerializedName("applied_coupon")
	private String appliedCoupon;

	@SerializedName("tax_amount")
	private String taxAmount;

	@SerializedName("billing_street_address")
	private String billingStreetAddress;

	@SerializedName("excise_duty")
	private Object exciseDuty;

	@SerializedName("updatedby")
	private Object updatedby;

	@SerializedName("gross_amount")
	private double grossAmount;

	@SerializedName("area_id")
	private Object areaId;

	@SerializedName("gross_discount_amount_base")
	private String grossDiscountAmountBase;

	@SerializedName("createdby")
	private Object createdby;

	@SerializedName("billing_country_name")
	private String billingCountryName;

	@SerializedName("address_book_id")
	private int addressBookId;

	@SerializedName("order_amount")
	private Object orderAmount;

	@SerializedName("modified")
	private String modified;

	@SerializedName("dispatch_date")
	private Object dispatchDate;

	@SerializedName("campaign_id")
	private Object campaignId;

	@SerializedName("pay_txndate")
	private Object payTxndate;

	@SerializedName("time_slot_id")
	private String timeSlotId;

	@SerializedName("created")
	private String created;

	@SerializedName("customer_addressbook")
	private CustomerAddressbook customerAddressbook;

	@SerializedName("assign_wh")
	private int assignWh;

	@SerializedName("pos_device_id")
	private Object posDeviceId;

	@SerializedName("slot_end_time")
	private String slotEndTime;

	@SerializedName("billing_city")
	private Object billingCity;

	@SerializedName("delivery_date")
	private Object deliveryDate;

	@SerializedName("webshop")
	private int webshop;

	@SerializedName("paid_amount_base")
	private Object paidAmountBase;

	@SerializedName("tracking_no")
	private Object trackingNo;

	@SerializedName("is_mail")
	private Object isMail;

	@SerializedName("lat_val")
	private String latVal;

	@SerializedName("website_id")
	private int websiteId;

	@SerializedName("long_val")
	private String longVal;

	@SerializedName("billing_phone")
	private String billingPhone;

	@SerializedName("received_status")
	private String receivedStatus;

	@SerializedName("billing_street_address1")
	private Object billingStreetAddress1;

	@SerializedName("return_note")
	private Object returnNote;

	@SerializedName("received_amount")
	private Object receivedAmount;

	@SerializedName("expected_delivery_date")
	private Object expectedDeliveryDate;

	@SerializedName("zone_id")
	private int zoneId;

	@SerializedName("buy_status")
	private int buyStatus;

	@SerializedName("channel_orderlineitem_id")
	private Object channelOrderlineitemId;

	@SerializedName("billing_fax")
	private Object billingFax;

	@SerializedName("billing_email_address")
	private String billingEmailAddress;

	@SerializedName("delivery_country")
	private int deliveryCountry;

	@SerializedName("slot_start_time")
	private String slotStartTime;

	@SerializedName("shipping_cost")
	private double shippingCost;

	@SerializedName("signature_image")
	private Object signatureImage;

	@SerializedName("ip_address")
	private Object ipAddress;

	@SerializedName("billing_name")
	private String billingName;

	@SerializedName("fulfillment_id")
	private Object fulfillmentId;

	@SerializedName("payment_method_id")
	private int paymentMethodId;

	@SerializedName("billing_company")
	private Object billingCompany;

	@SerializedName("delivery_fax")
	private Object deliveryFax;

	@SerializedName("return_status")
	private Object returnStatus;

	@SerializedName("net_amount")
	private double netAmount;

	@SerializedName("delivery_street_address")
	private String deliveryStreetAddress;

	@SerializedName("customer")
	private Customer customer;

	public Object getTrackingMailSend(){
		return trackingMailSend;
	}

	public Object getDeliveryCompany(){
		return deliveryCompany;
	}

	public Object getChannelOrderId(){
		return channelOrderId;
	}

	public String getCustomMsg(){
		return customMsg;
	}

	public Object getTallySalesEntered(){
		return tallySalesEntered;
	}

	public String getIsdeleted(){
		return isdeleted;
	}

	public int getOrderStatus(){
		return orderStatus;
	}

	public Object getPickerName(){
		return pickerName;
	}

	public int getCodCharge(){
		return codCharge;
	}

	public String getBillingStateName(){
		return billingStateName;
	}

	public String getTimeSlotDate(){
		return timeSlotDate;
	}

	public int getId(){
		return id;
	}

	public int getPaymentTypeId(){
		return paymentTypeId;
	}

	public OrderShipment getOrderShipment(){
		return orderShipment;
	}

	public String getGrossDiscountAmount(){
		return grossDiscountAmount;
	}

	public Object getTrackingCompanyName(){
		return trackingCompanyName;
	}

	public String getDeliveryPhone(){
		return deliveryPhone;
	}

	public Object getShippingMethodId(){
		return shippingMethodId;
	}

	public int getDeliveryState(){
		return deliveryState;
	}

	public int getShipmentId(){
		return shipmentId;
	}

	public Object getSortByDistance(){
		return sortByDistance;
	}

	public Object getGrnCreatedDate(){
		return grnCreatedDate;
	}

	public Object getShippingCostBase(){
		return shippingCostBase;
	}

	public Object getTags(){
		return tags;
	}

	public Object getBillingPostcode(){
		return billingPostcode;
	}

	public String getPaidAmount(){
		return paidAmount;
	}

	public Object getFlagOrder(){
		return flagOrder;
	}

	public int getTrentPicklistId(){
		return trentPicklistId;
	}

	public int getMaximumSubstituteLimit(){
		return maximumSubstituteLimit;
	}

	public String getDeliveryName(){
		return deliveryName;
	}

	public Object getSendNotes(){
		return sendNotes;
	}

	public int getAssignTo(){
		return assignTo;
	}

	public Object getPayTxntranid(){
		return payTxntranid;
	}

	public String getCartDiscount(){
		return cartDiscount;
	}

	public Object getSecurityAmount(){
		return securityAmount;
	}

	public String getRefundWalletAmount(){
		return refundWalletAmount;
	}

	public int getMinimumSubstituteLimit(){
		return minimumSubstituteLimit;
	}

	public String getCustomOrderId(){
		return customOrderId;
	}

	public String getCurrencyCode(){
		return currencyCode;
	}

	public Object getResponseMsg(){
		return responseMsg;
	}

	public String getAssignToName(){
		return assignToName;
	}

	public List<OrderProductsItem> getOrderProducts(){
		return orderProducts;
	}

	public int getBillingState(){
		return billingState;
	}

	public String getDeliveryEmailAddress(){
		return deliveryEmailAddress;
	}

	public Object getTrackingUrl(){
		return trackingUrl;
	}

	public String getDeliveryCountryName(){
		return deliveryCountryName;
	}

	public int getCompanyId(){
		return companyId;
	}

	public Object getDeliveryStreetAddress1(){
		return deliveryStreetAddress1;
	}

	public List<OrderActivityItem> getOrderActivity(){
		return orderActivity;
	}

	public int getBillingCountry(){
		return billingCountry;
	}

	public double getNetAmountBase(){
		return netAmountBase;
	}

	public Object getRefferalCode(){
		return refferalCode;
	}

	public String getPaymentMethodName(){
		return paymentMethodName;
	}

	public Object getDeliverySapEcustomerStateNo(){
		return deliverySapEcustomerStateNo;
	}

	public Object getAssignedShowRoom(){
		return assignedShowRoom;
	}

	public String getIsblocked(){
		return isblocked;
	}

	public Object getShippingCostExclTax(){
		return shippingCostExclTax;
	}

	public double getGrossAmountBase(){
		return grossAmountBase;
	}

	public String getChannelShippingStatus(){
		return channelShippingStatus;
	}

	public Object getDeliveryPostcode(){
		return deliveryPostcode;
	}

	public String getDeliveryStateName(){
		return deliveryStateName;
	}

	public Object getDeliveryCity(){
		return deliveryCity;
	}

	public String getPayWalletAmount(){
		return payWalletAmount;
	}

	public String getAppliedCoupon(){
		return appliedCoupon;
	}

	public String getTaxAmount(){
		return taxAmount;
	}

	public String getBillingStreetAddress(){
		return billingStreetAddress;
	}

	public Object getExciseDuty(){
		return exciseDuty;
	}

	public Object getUpdatedby(){
		return updatedby;
	}

	public double getGrossAmount(){
		return grossAmount;
	}

	public Object getAreaId(){
		return areaId;
	}

	public String getGrossDiscountAmountBase(){
		return grossDiscountAmountBase;
	}

	public Object getCreatedby(){
		return createdby;
	}

	public String getBillingCountryName(){
		return billingCountryName;
	}

	public int getAddressBookId(){
		return addressBookId;
	}

	public Object getOrderAmount(){
		return orderAmount;
	}

	public String getModified(){
		return modified;
	}

	public Object getDispatchDate(){
		return dispatchDate;
	}

	public Object getCampaignId(){
		return campaignId;
	}

	public Object getPayTxndate(){
		return payTxndate;
	}

	public String getTimeSlotId(){
		return timeSlotId;
	}

	public String getCreated(){
		return created;
	}

	public CustomerAddressbook getCustomerAddressbook(){
		return customerAddressbook;
	}

	public int getAssignWh(){
		return assignWh;
	}

	public Object getPosDeviceId(){
		return posDeviceId;
	}

	public String getSlotEndTime(){
		return slotEndTime;
	}

	public Object getBillingCity(){
		return billingCity;
	}

	public Object getDeliveryDate(){
		return deliveryDate;
	}

	public int getWebshop(){
		return webshop;
	}

	public Object getPaidAmountBase(){
		return paidAmountBase;
	}

	public Object getTrackingNo(){
		return trackingNo;
	}

	public Object getIsMail(){
		return isMail;
	}

	public String getLatVal(){
		return latVal;
	}

	public int getWebsiteId(){
		return websiteId;
	}

	public String getLongVal(){
		return longVal;
	}

	public String getBillingPhone(){
		return billingPhone;
	}

	public String getReceivedStatus(){
		return receivedStatus;
	}

	public Object getBillingStreetAddress1(){
		return billingStreetAddress1;
	}

	public Object getReturnNote(){
		return returnNote;
	}

	public Object getReceivedAmount(){
		return receivedAmount;
	}

	public Object getExpectedDeliveryDate(){
		return expectedDeliveryDate;
	}

	public int getZoneId(){
		return zoneId;
	}

	public int getBuyStatus(){
		return buyStatus;
	}

	public Object getChannelOrderlineitemId(){
		return channelOrderlineitemId;
	}

	public Object getBillingFax(){
		return billingFax;
	}

	public String getBillingEmailAddress(){
		return billingEmailAddress;
	}

	public int getDeliveryCountry(){
		return deliveryCountry;
	}

	public String getSlotStartTime(){
		return slotStartTime;
	}

	public double getShippingCost(){
		return shippingCost;
	}

	public Object getSignatureImage(){
		return signatureImage;
	}

	public Object getIpAddress(){
		return ipAddress;
	}

	public String getBillingName(){
		return billingName;
	}

	public Object getFulfillmentId(){
		return fulfillmentId;
	}

	public int getPaymentMethodId(){
		return paymentMethodId;
	}

	public Object getBillingCompany(){
		return billingCompany;
	}

	public Object getDeliveryFax(){
		return deliveryFax;
	}

	public Object getReturnStatus(){
		return returnStatus;
	}

	public double getNetAmount(){
		return netAmount;
	}

	public String getDeliveryStreetAddress(){
		return deliveryStreetAddress;
	}

	public Customer getCustomer(){
		return customer;
	}

	public int getSubstitute_approval_time() {
		return substitute_approval_time;
	}
}