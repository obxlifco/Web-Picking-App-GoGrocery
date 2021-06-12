package com.gogrocery.Models.OrderDetailsModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Customer {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("first_name")
@Expose
private String firstName;
@SerializedName("last_name")
@Expose
private String lastName;
@SerializedName("ebayusername")
@Expose
private Object ebayusername;
@SerializedName("address")
@Expose
private String address;
@SerializedName("country_id")
@Expose
private Object countryId;
@SerializedName("group_id")
@Expose
private Object groupId;
@SerializedName("email")
@Expose
private String email;
@SerializedName("phone")
@Expose
private String phone;
@SerializedName("vat")
@Expose
private Object vat;
@SerializedName("tin")
@Expose
private Object tin;
@SerializedName("excise_regn_no")
@Expose
private Object exciseRegnNo;

public Integer getId() {
return id;
}

public void setId(Integer id) {
this.id = id;
}

public String getFirstName() {
return firstName;
}

public void setFirstName(String firstName) {
this.firstName = firstName;
}

public String getLastName() {
return lastName;
}

public void setLastName(String lastName) {
this.lastName = lastName;
}

public Object getEbayusername() {
return ebayusername;
}

public void setEbayusername(Object ebayusername) {
this.ebayusername = ebayusername;
}

public String getAddress() {
return address;
}

public void setAddress(String address) {
this.address = address;
}

public Object getCountryId() {
return countryId;
}

public void setCountryId(Object countryId) {
this.countryId = countryId;
}

public Object getGroupId() {
return groupId;
}

public void setGroupId(Object groupId) {
this.groupId = groupId;
}

public String getEmail() {
return email;
}

public void setEmail(String email) {
this.email = email;
}

public String getPhone() {
return phone;
}

public void setPhone(String phone) {
this.phone = phone;
}

public Object getVat() {
return vat;
}

public void setVat(Object vat) {
this.vat = vat;
}

public Object getTin() {
return tin;
}

public void setTin(Object tin) {
this.tin = tin;
}

public Object getExciseRegnNo() {
return exciseRegnNo;
}

public void setExciseRegnNo(Object exciseRegnNo) {
this.exciseRegnNo = exciseRegnNo;
}

}