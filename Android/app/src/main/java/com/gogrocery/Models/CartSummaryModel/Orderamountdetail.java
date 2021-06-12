package com.gogrocery.Models.CartSummaryModel;

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
    private String grossDiscount;
    @SerializedName("min_amount")
    @Expose
    private String minAmount;
    @SerializedName("max_amount")
    @Expose
    private String maxAmount;
    @SerializedName("grand_total")
    @Expose
    private String grandTotal;
    @SerializedName("sub_total")
    @Expose
    private String subTotal;
    @SerializedName("net_total")
    @Expose
    private String netTotal;
    @SerializedName("cart_discount")
    @Expose
    private String cartDiscount;
    @SerializedName("paid_amount")
    @Expose
    private String paidAmount;
    @SerializedName("balance_due")
    @Expose
    private String balanceDue;
    @SerializedName("applied_loyalty_amount")
    @Expose
    private String applied_loyalty_amount;


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

    public String getGrossDiscount() {
        return grossDiscount;
    }

    public void setGrossDiscount(String grossDiscount) {
        this.grossDiscount = grossDiscount;
    }

    public String getMinAmount() {
        return minAmount;
    }

    public void setMinAmount(String minAmount) {
        this.minAmount = minAmount;
    }

    public String getMaxAmount() {
        return maxAmount;
    }

    public void setMaxAmount(String maxAmount) {
        this.maxAmount = maxAmount;
    }

    public String getGrandTotal() {
        return grandTotal;
    }

    public void setGrandTotal(String grandTotal) {
        this.grandTotal = grandTotal;
    }

    public String getSubTotal() {
        return subTotal;
    }

    public void setSubTotal(String subTotal) {
        this.subTotal = subTotal;
    }

    public String getNetTotal() {
        return netTotal;
    }

    public void setNetTotal(String netTotal) {
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

    public String getBalanceDue() {
        return balanceDue;
    }

    public void setBalanceDue(String balanceDue) {
        this.balanceDue = balanceDue;
    }

    public String getApplied_loyalty_amount() {
        return applied_loyalty_amount;
    }

    public void setApplied_loyalty_amount(String applied_loyalty_amount) {
        this.applied_loyalty_amount = applied_loyalty_amount;
    }
}