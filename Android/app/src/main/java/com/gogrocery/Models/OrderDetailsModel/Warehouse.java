package com.gogrocery.Models.OrderDetailsModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Warehouse {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("website_id")
@Expose
private Integer websiteId;
@SerializedName("name")
@Expose
private String name;
@SerializedName("code")
@Expose
private String code;
@SerializedName("contact_person")
@Expose
private String contactPerson;
@SerializedName("address")
@Expose
private String address;
@SerializedName("country_id")
@Expose
private Integer countryId;
@SerializedName("state_id")
@Expose
private Integer stateId;
@SerializedName("state_name")
@Expose
private Object stateName;
@SerializedName("city")
@Expose
private String city;
@SerializedName("zipcode")
@Expose
private String zipcode;
@SerializedName("phone")
@Expose
private String phone;
@SerializedName("email")
@Expose
private String email;
@SerializedName("isblocked")
@Expose
private String isblocked;
@SerializedName("isdeleted")
@Expose
private String isdeleted;
@SerializedName("channel_id")
@Expose
private String  channelId;
@SerializedName("order_id_format")
@Expose
private String orderIdFormat;
@SerializedName("shipping_id_format")
@Expose
private String shippingIdFormat;
@SerializedName("invoice_id_format")
@Expose
private String invoiceIdFormat;
@SerializedName("text_color")
@Expose
private String textColor;
@SerializedName("product_stock_code")
@Expose
private Object productStockCode;
@SerializedName("latitude")
@Expose
private String latitude;
@SerializedName("longitude")
@Expose
private String longitude;
@SerializedName("max_distance_sales")
@Expose
private String maxDistanceSales;
@SerializedName("created")
@Expose
private String created;
@SerializedName("modified")
@Expose
private String modified;
@SerializedName("createdby")
@Expose
private String createdby;
@SerializedName("updatedby")
@Expose
private String updatedby;
@SerializedName("ip_address")
@Expose
private Object ipAddress;

public Integer getId() {
return id;
}

public void setId(Integer id) {
this.id = id;
}

public Integer getWebsiteId() {
return websiteId;
}

public void setWebsiteId(Integer websiteId) {
this.websiteId = websiteId;
}

public String getName() {
return name;
}

public void setName(String name) {
this.name = name;
}

public String getCode() {
return code;
}

public void setCode(String code) {
this.code = code;
}

public String getContactPerson() {
return contactPerson;
}

public void setContactPerson(String contactPerson) {
this.contactPerson = contactPerson;
}

public String getAddress() {
return address;
}

public void setAddress(String address) {
this.address = address;
}

public Integer getCountryId() {
return countryId;
}

public void setCountryId(Integer countryId) {
this.countryId = countryId;
}

public Integer getStateId() {
return stateId;
}

public void setStateId(Integer stateId) {
this.stateId = stateId;
}

public Object getStateName() {
return stateName;
}

public void setStateName(Object stateName) {
this.stateName = stateName;
}

public String getCity() {
return city;
}

public void setCity(String city) {
this.city = city;
}

public String getZipcode() {
return zipcode;
}

public void setZipcode(String zipcode) {
this.zipcode = zipcode;
}

public String getPhone() {
return phone;
}

public void setPhone(String phone) {
this.phone = phone;
}

public String getEmail() {
return email;
}

public void setEmail(String email) {
this.email = email;
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

public String getChannelId() {
return channelId;
}

public void setChannelId(String channelId) {
this.channelId = channelId;
}

public String getOrderIdFormat() {
return orderIdFormat;
}

public void setOrderIdFormat(String orderIdFormat) {
this.orderIdFormat = orderIdFormat;
}

public String getShippingIdFormat() {
return shippingIdFormat;
}

public void setShippingIdFormat(String shippingIdFormat) {
this.shippingIdFormat = shippingIdFormat;
}

public String getInvoiceIdFormat() {
return invoiceIdFormat;
}

public void setInvoiceIdFormat(String invoiceIdFormat) {
this.invoiceIdFormat = invoiceIdFormat;
}

public String getTextColor() {
return textColor;
}

public void setTextColor(String textColor) {
this.textColor = textColor;
}

public Object getProductStockCode() {
return productStockCode;
}

public void setProductStockCode(Object productStockCode) {
this.productStockCode = productStockCode;
}

public String getLatitude() {
return latitude;
}

public void setLatitude(String latitude) {
this.latitude = latitude;
}

public String getLongitude() {
return longitude;
}

public void setLongitude(String longitude) {
this.longitude = longitude;
}

public String getMaxDistanceSales() {
return maxDistanceSales;
}

public void setMaxDistanceSales(String maxDistanceSales) {
this.maxDistanceSales = maxDistanceSales;
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

public String getCreatedby() {
return createdby;
}

public void setCreatedby(String createdby) {
this.createdby = createdby;
}

public String getUpdatedby() {
return updatedby;
}

public void setUpdatedby(String updatedby) {
this.updatedby = updatedby;
}

public Object getIpAddress() {
return ipAddress;
}

public void setIpAddress(Object ipAddress) {
this.ipAddress = ipAddress;
}

}
