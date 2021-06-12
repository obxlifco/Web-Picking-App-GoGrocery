package com.gogrocery.Models.MyAddressesModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.io.Serializable;

public class Data  implements Serializable {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("billing_state_name")
@Expose
private String billingStateName;
@SerializedName("delivery_state_name")
@Expose
private String deliveryStateName;
@SerializedName("billing_country_name")
@Expose
private String billingCountryName;
@SerializedName("delivery_country_name")
@Expose
private String deliveryCountryName;
@SerializedName("customers_id")
@Expose
private Integer customersId;
@SerializedName("set_primary")
@Expose
private Integer setPrimary;
@SerializedName("billing_name")
@Expose
private String billingName;
@SerializedName("billing_company")
@Expose
private String billingCompany;
@SerializedName("billing_email_address")
@Expose
private String billingEmailAddress;
@SerializedName("billing_street_address")
@Expose
private String billingStreetAddress;
@SerializedName("billing_street_address1")
@Expose
private String billingStreetAddress1;
@SerializedName("billing_landmark")
@Expose
private String billingLandmark;
@SerializedName("billing_city")
@Expose
private String billingCity;
@SerializedName("billing_postcode")
@Expose
private String billingPostcode;
@SerializedName("billing_state")
@Expose
private String billingState;
@SerializedName("billing_country")
@Expose
private Integer billingCountry;
@SerializedName("billing_phone")
@Expose
private String billingPhone;
@SerializedName("billing_fax")
@Expose
private String billingFax;
@SerializedName("delivery_name")
@Expose
private String deliveryName;
@SerializedName("delivery_company")
@Expose
private String deliveryCompany;
@SerializedName("delivery_email_address")
@Expose
private String deliveryEmailAddress;
@SerializedName("delivery_street_address")
@Expose
private String deliveryStreetAddress;
@SerializedName("delivery_street_address1")
@Expose
private String deliveryStreetAddress1;
@SerializedName("delivery_landmark")
@Expose
private String deliveryLandmark;
@SerializedName("delivery_city")
@Expose
private String deliveryCity;
@SerializedName("delivery_postcode")
@Expose
private String deliveryPostcode;
@SerializedName("delivery_state")
@Expose
private String deliveryState;
@SerializedName("delivery_country")
@Expose
private Integer deliveryCountry;
@SerializedName("delivery_phone")
@Expose
private String deliveryPhone;
@SerializedName("delivery_fax")
@Expose
private String deliveryFax;
@SerializedName("lat_val")
@Expose
private String latVal;
@SerializedName("long_val")
@Expose
private String longVal;
@SerializedName("isdeleted")
@Expose
private String isdeleted;
@SerializedName("isblocked")
@Expose
private String isblocked;
@SerializedName("created")
@Expose
private String created;
@SerializedName("modified")
@Expose
private String modified;

public Integer getId() {
return id;
}

public void setId(Integer id) {
this.id = id;
}

public String getBillingStateName() {
return billingStateName;
}

public void setBillingStateName(String billingStateName) {
this.billingStateName = billingStateName;
}

public String getDeliveryStateName() {
return deliveryStateName;
}

public void setDeliveryStateName(String deliveryStateName) {
this.deliveryStateName = deliveryStateName;
}

public String getBillingCountryName() {
return billingCountryName;
}

public void setBillingCountryName(String billingCountryName) {
this.billingCountryName = billingCountryName;
}

public String getDeliveryCountryName() {
return deliveryCountryName;
}

public void setDeliveryCountryName(String deliveryCountryName) {
this.deliveryCountryName = deliveryCountryName;
}

public Integer getCustomersId() {
return customersId;
}

public void setCustomersId(Integer customersId) {
this.customersId = customersId;
}

public Integer getSetPrimary() {
return setPrimary;
}

public void setSetPrimary(Integer setPrimary) {
this.setPrimary = setPrimary;
}

public String getBillingName() {
return billingName;
}

public void setBillingName(String billingName) {
this.billingName = billingName;
}

public String getBillingCompany() {
return billingCompany;
}

public void setBillingCompany(String billingCompany) {
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

public String getBillingStreetAddress1() {
return billingStreetAddress1;
}

public void setBillingStreetAddress1(String billingStreetAddress1) {
this.billingStreetAddress1 = billingStreetAddress1;
}

public String getBillingLandmark() {
return billingLandmark;
}

public void setBillingLandmark(String billingLandmark) {
this.billingLandmark = billingLandmark;
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

public Integer getBillingCountry() {
return billingCountry;
}

public void setBillingCountry(Integer billingCountry) {
this.billingCountry = billingCountry;
}

public String getBillingPhone() {
return billingPhone;
}

public void setBillingPhone(String billingPhone) {
this.billingPhone = billingPhone;
}

public String getBillingFax() {
return billingFax;
}

public void setBillingFax(String billingFax) {
this.billingFax = billingFax;
}

public String getDeliveryName() {
return deliveryName;
}

public void setDeliveryName(String deliveryName) {
this.deliveryName = deliveryName;
}

public String getDeliveryCompany() {
return deliveryCompany;
}

public void setDeliveryCompany(String deliveryCompany) {
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

public String getDeliveryStreetAddress1() {
return deliveryStreetAddress1;
}

public void setDeliveryStreetAddress1(String deliveryStreetAddress1) {
this.deliveryStreetAddress1 = deliveryStreetAddress1;
}

public String getDeliveryLandmark() {
return deliveryLandmark;
}

public void setDeliveryLandmark(String deliveryLandmark) {
this.deliveryLandmark = deliveryLandmark;
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

public Integer getDeliveryCountry() {
return deliveryCountry;
}

public void setDeliveryCountry(Integer deliveryCountry) {
this.deliveryCountry = deliveryCountry;
}

public String getDeliveryPhone() {
return deliveryPhone;
}

public void setDeliveryPhone(String deliveryPhone) {
this.deliveryPhone = deliveryPhone;
}

public String getDeliveryFax() {
return deliveryFax;
}

public void setDeliveryFax(String deliveryFax) {
this.deliveryFax = deliveryFax;
}

public String getLatVal() {
return latVal;
}

public void setLatVal(String latVal) {
this.latVal = latVal;
}

public String getLongVal() {
return longVal;
}

public void setLongVal(String longVal) {
this.longVal = longVal;
}

public String getIsdeleted() {
return isdeleted;
}

public void setIsdeleted(String isdeleted) {
this.isdeleted = isdeleted;
}

public String getIsblocked() {
return isblocked;
}

public void setIsblocked(String isblocked) {
this.isblocked = isblocked;
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

}
