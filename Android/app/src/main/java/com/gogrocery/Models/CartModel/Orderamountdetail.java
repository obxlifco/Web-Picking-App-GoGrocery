package com.gogrocery.Models.CartModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Orderamountdetail {

@SerializedName("company_id")
@Expose
private String companyId;
@SerializedName("website_id")
@Expose
private String websiteId;
@SerializedName("webshop_id")
@Expose
private String webshopId;
@SerializedName("payment_method_id")
@Expose
private String paymentMethodId;
@SerializedName("tax_amount")
@Expose
private String taxAmount;
@SerializedName("shipping_charge")
@Expose
private String shippingCharge;
@SerializedName("handling_charge")
@Expose
private String handlingCharge;
@SerializedName("cod_charge")
@Expose
private String codCharge;
@SerializedName("gross_discount")
@Expose
private Double grossDiscount;
@SerializedName("grand_total")
@Expose
private Double grandTotal;
@SerializedName("sub_total")
@Expose
private Double subTotal;
@SerializedName("net_total")
@Expose
private Double netTotal;
@SerializedName("cart_discount")
@Expose
private String cartDiscount;
@SerializedName("paid_amount")
@Expose
private String paidAmount;
@SerializedName("balance_due")
@Expose
private Double balanceDue;

public String getCompanyId() {
return companyId;
}

public void setCompanyId(String companyId) {
this.companyId = companyId;
}

public String getWebsiteId() {
return websiteId;
}

public void setWebsiteId(String websiteId) {
this.websiteId = websiteId;
}

public String getWebshopId() {
return webshopId;
}

public void setWebshopId(String webshopId) {
this.webshopId = webshopId;
}

public String getPaymentMethodId() {
return paymentMethodId;
}

public void setPaymentMethodId(String paymentMethodId) {
this.paymentMethodId = paymentMethodId;
}

public String getTaxAmount() {
return taxAmount;
}

public void setTaxAmount(String taxAmount) {
this.taxAmount = taxAmount;
}

public String getShippingCharge() {
return shippingCharge;
}

public void setShippingCharge(String shippingCharge) {
this.shippingCharge = shippingCharge;
}

public String getHandlingCharge() {
return handlingCharge;
}

public void setHandlingCharge(String handlingCharge) {
this.handlingCharge = handlingCharge;
}

public String getCodCharge() {
return codCharge;
}

public void setCodCharge(String codCharge) {
this.codCharge = codCharge;
}

public Double getGrossDiscount() {
return grossDiscount;
}

public void setGrossDiscount(Double grossDiscount) {
this.grossDiscount = grossDiscount;
}

public Double getGrandTotal() {
return grandTotal;
}

public void setGrandTotal(Double grandTotal) {
this.grandTotal = grandTotal;
}

public Double getSubTotal() {
return subTotal;
}

public void setSubTotal(Double subTotal) {
this.subTotal = subTotal;
}

public Double getNetTotal() {
return netTotal;
}

public void setNetTotal(Double netTotal) {
this.netTotal = netTotal;
}

public String getCartDiscount() {
return cartDiscount;
}

public void setCartDiscount(String cartDiscount) {
this.cartDiscount = cartDiscount;
}

public String getPaidAmount() {
return paidAmount;
}

public void setPaidAmount(String paidAmount) {
this.paidAmount = paidAmount;
}

public Double getBalanceDue() {
return balanceDue;
}

public void setBalanceDue(Double balanceDue) {
this.balanceDue = balanceDue;
}

}