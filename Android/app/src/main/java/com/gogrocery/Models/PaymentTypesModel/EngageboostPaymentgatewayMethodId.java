package com.gogrocery.Models.PaymentTypesModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class EngageboostPaymentgatewayMethodId {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("name")
@Expose
private String name;
@SerializedName("description")
@Expose
private String description;
@SerializedName("paymentgateway_type_id")
@Expose
private Integer paymentgatewayTypeId;
@SerializedName("destination_url")
@Expose
private String destinationUrl;
@SerializedName("destination_sandbox_url")
@Expose
private String destinationSandboxUrl;
@SerializedName("notification_url")
@Expose
private String notificationUrl;
@SerializedName("notification_sandbox_url")
@Expose
private String notificationSandboxUrl;
@SerializedName("cancel_url")
@Expose
private String cancelUrl;
@SerializedName("cancel_sandbox_url")
@Expose
private String cancelSandboxUrl;
@SerializedName("ebay_term")
@Expose
private String ebayTerm;
@SerializedName("createdby")
@Expose
private Integer createdby;
@SerializedName("isblocked")
@Expose
private String isblocked;
@SerializedName("isdeleted")
@Expose
private String isdeleted;

public Integer getId() {
return id;
}

public void setId(Integer id) {
this.id = id;
}

public String getName() {
return name;
}

public void setName(String name) {
this.name = name;
}

public String getDescription() {
return description;
}

public void setDescription(String description) {
this.description = description;
}

public Integer getPaymentgatewayTypeId() {
return paymentgatewayTypeId;
}

public void setPaymentgatewayTypeId(Integer paymentgatewayTypeId) {
this.paymentgatewayTypeId = paymentgatewayTypeId;
}

public String getDestinationUrl() {
return destinationUrl;
}

public void setDestinationUrl(String destinationUrl) {
this.destinationUrl = destinationUrl;
}

public String getDestinationSandboxUrl() {
return destinationSandboxUrl;
}

public void setDestinationSandboxUrl(String destinationSandboxUrl) {
this.destinationSandboxUrl = destinationSandboxUrl;
}

public String getNotificationUrl() {
return notificationUrl;
}

public void setNotificationUrl(String notificationUrl) {
this.notificationUrl = notificationUrl;
}

public String getNotificationSandboxUrl() {
return notificationSandboxUrl;
}

public void setNotificationSandboxUrl(String notificationSandboxUrl) {
this.notificationSandboxUrl = notificationSandboxUrl;
}

public String getCancelUrl() {
return cancelUrl;
}

public void setCancelUrl(String cancelUrl) {
this.cancelUrl = cancelUrl;
}

public String getCancelSandboxUrl() {
return cancelSandboxUrl;
}

public void setCancelSandboxUrl(String cancelSandboxUrl) {
this.cancelSandboxUrl = cancelSandboxUrl;
}

public String getEbayTerm() {
return ebayTerm;
}

public void setEbayTerm(String ebayTerm) {
this.ebayTerm = ebayTerm;
}

public Integer getCreatedby() {
return createdby;
}

public void setCreatedby(Integer createdby) {
this.createdby = createdby;
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

}