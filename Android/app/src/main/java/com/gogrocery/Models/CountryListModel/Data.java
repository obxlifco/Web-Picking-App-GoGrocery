package com.gogrocery.Models.CountryListModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Data {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("country_name")
@Expose
private String countryName;
@SerializedName("country_code")
@Expose
private String countryCode;
@SerializedName("countries_iso_code_3")
@Expose
private String countriesIsoCode3;
@SerializedName("ebay_countrycode")
@Expose
private String ebayCountrycode;
@SerializedName("address_format_id")
@Expose
private Integer addressFormatId;
@SerializedName("created")
@Expose
private Object created;
@SerializedName("modified")
@Expose
private Object modified;
@SerializedName("isdeleted")
@Expose
private String isdeleted;
@SerializedName("isblocked")
@Expose
private String isblocked;
@SerializedName("createdby")
@Expose
private Object createdby;
@SerializedName("updatedby")
@Expose
private Object updatedby;
@SerializedName("ip_address")
@Expose
private Object ipAddress;

public Integer getId() {
return id;
}

public void setId(Integer id) {
this.id = id;
}

public String getCountryName() {
return countryName;
}

public void setCountryName(String countryName) {
this.countryName = countryName;
}

public String getCountryCode() {
return countryCode;
}

public void setCountryCode(String countryCode) {
this.countryCode = countryCode;
}

public String getCountriesIsoCode3() {
return countriesIsoCode3;
}

public void setCountriesIsoCode3(String countriesIsoCode3) {
this.countriesIsoCode3 = countriesIsoCode3;
}

public String getEbayCountrycode() {
return ebayCountrycode;
}

public void setEbayCountrycode(String ebayCountrycode) {
this.ebayCountrycode = ebayCountrycode;
}

public Integer getAddressFormatId() {
return addressFormatId;
}

public void setAddressFormatId(Integer addressFormatId) {
this.addressFormatId = addressFormatId;
}

public Object getCreated() {
return created;
}

public void setCreated(Object created) {
this.created = created;
}

public Object getModified() {
return modified;
}

public void setModified(Object modified) {
this.modified = modified;
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

public Object getIpAddress() {
return ipAddress;
}

public void setIpAddress(Object ipAddress) {
this.ipAddress = ipAddress;
}

}