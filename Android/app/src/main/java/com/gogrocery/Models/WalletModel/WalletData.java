package com.gogrocery.Models.WalletModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class WalletData {

@SerializedName("id")
@Expose
private String id;
@SerializedName("website_id")
@Expose
private String websiteId;
@SerializedName("rule_id")
@Expose
private String ruleId;
@SerializedName("customer_id")
@Expose
private String customerId;
@SerializedName("order_id")
@Expose
private String orderId;
@SerializedName("custom_order_id")
@Expose
private String customOrderId;
@SerializedName("customer_contact_no")
@Expose
private Object customerContactNo;
@SerializedName("description")
@Expose
private String description;
@SerializedName("received_points")
@Expose
private String receivedPoints;
@SerializedName("burnt_points")
@Expose
private String burntPoints;
@SerializedName("amount")
@Expose
private String amount;
@SerializedName("received_burnt")
@Expose
private String receivedBurnt;
@SerializedName("status")
@Expose
private String status;
@SerializedName("burn_type")
@Expose
private Object burnType;
@SerializedName("card_id")
@Expose
private Object cardId;
@SerializedName("created")
@Expose
private String created;
@SerializedName("modified")
@Expose
private Object modified;
@SerializedName("valid_form")
@Expose
private String validForm;
@SerializedName("expiry_date")
@Expose
private Object expiryDate;
@SerializedName("remaining_balance")
@Expose
private String remainingBalance;
@SerializedName("view_status")
@Expose
private Object viewStatus;

public String getId() {
return id;
}

public void setId(String id) {
this.id = id;
}

public String getWebsiteId() {
return websiteId;
}

public void setWebsiteId(String websiteId) {
this.websiteId = websiteId;
}

public String getRuleId() {
return ruleId;
}

public void setRuleId(String ruleId) {
this.ruleId = ruleId;
}

public String getCustomerId() {
return customerId;
}

public void setCustomerId(String customerId) {
this.customerId = customerId;
}

public String getOrderId() {
return orderId;
}

public void setOrderId(String orderId) {
this.orderId = orderId;
}

public String getCustomOrderId() {
return customOrderId;
}

public void setCustomOrderId(String customOrderId) {
this.customOrderId = customOrderId;
}

public Object getCustomerContactNo() {
return customerContactNo;
}

public void setCustomerContactNo(Object customerContactNo) {
this.customerContactNo = customerContactNo;
}

public String getDescription() {
return description;
}

public void setDescription(String description) {
this.description = description;
}

public String getReceivedPoints() {
return receivedPoints;
}

public void setReceivedPoints(String receivedPoints) {
this.receivedPoints = receivedPoints;
}

public String getBurntPoints() {
return burntPoints;
}

public void setBurntPoints(String burntPoints) {
this.burntPoints = burntPoints;
}

public String getAmount() {
return amount;
}

public void setAmount(String amount) {
this.amount = amount;
}

public String getReceivedBurnt() {
return receivedBurnt;
}

public void setReceivedBurnt(String receivedBurnt) {
this.receivedBurnt = receivedBurnt;
}

public String getStatus() {
return status;
}

public void setStatus(String status) {
this.status = status;
}

public Object getBurnType() {
return burnType;
}

public void setBurnType(Object burnType) {
this.burnType = burnType;
}

public Object getCardId() {
return cardId;
}

public void setCardId(Object cardId) {
this.cardId = cardId;
}

public String getCreated() {
return created;
}

public void setCreated(String created) {
this.created = created;
}

public Object getModified() {
return modified;
}

public void setModified(Object modified) {
this.modified = modified;
}

public String getValidForm() {
return validForm;
}

public void setValidForm(String validForm) {
this.validForm = validForm;
}

public Object getExpiryDate() {
return expiryDate;
}

public void setExpiryDate(Object expiryDate) {
this.expiryDate = expiryDate;
}

public String getRemainingBalance() {
return remainingBalance;
}

public void setRemainingBalance(String remainingBalance) {
this.remainingBalance = remainingBalance;
}

public Object getViewStatus() {
return viewStatus;
}

public void setViewStatus(Object viewStatus) {
this.viewStatus = viewStatus;
}

}