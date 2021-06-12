package com.gogrocery.Models.ViewCartModel;

import java.util.List;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class ViewCartModel {

    @SerializedName("status")
    @Expose
    private String status;
    @SerializedName("msg")
    @Expose
    private String msg;
    @SerializedName("cart_count_itemwise")
    @Expose
    private String cart_count_itemwise;
    @SerializedName("cart_count")
    @Expose
    private String cartCount;
    @SerializedName("saved_amount")
    @Expose
    private String savedAmount;
    @SerializedName("stock_message")
    @Expose
    private String stockMessage;
    @SerializedName("total_amount")
    @Expose
    private String totalAmount;
    @SerializedName("data")
    @Expose
    private List<Data> data = null;
    @SerializedName("minimum_order_amount")
    @Expose
    private String minimumOrderAmount;
    @SerializedName("minimum_order_amount_check")
    @Expose
    private String minimumOrderAmountCheck;
    @SerializedName("shipping_amount")
    @Expose
    private String shippingAmount;
    @SerializedName("final_amount")
    @Expose
    private String finalAmount;

    public String getStockMessage() {
        return stockMessage;
    }

    public void setStockMessage(String stockMessage) {
        this.stockMessage = stockMessage;
    }

    public String getMinimumOrderAmount() {
        return minimumOrderAmount;
    }

    public void setMinimumOrderAmount(String minimumOrderAmount) {
        this.minimumOrderAmount = minimumOrderAmount;
    }

    public String getMinimumOrderAmountCheck() {
        return minimumOrderAmountCheck;
    }

    public void setMinimumOrderAmountCheck(String minimumOrderAmountCheck) {
        this.minimumOrderAmountCheck = minimumOrderAmountCheck;
    }

    public String getShippingAmount() {
        return shippingAmount;
    }

    public void setShippingAmount(String shippingAmount) {
        this.shippingAmount = shippingAmount;
    }

    public String getFinalAmount() {
        return finalAmount;
    }

    public void setFinalAmount(String finalAmount) {
        this.finalAmount = finalAmount;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

    public String getCartCount() {
        return cartCount;
    }

    public void setCartCount(String cartCount) {
        this.cartCount = cartCount;
    }

    public String getSavedAmount() {
        return savedAmount;
    }

    public void setSavedAmount(String savedAmount) {
        this.savedAmount = savedAmount;
    }

    public String getTotalAmount() {
        return totalAmount;
    }

    public void setTotalAmount(String totalAmount) {
        this.totalAmount = totalAmount;
    }

    public List<Data> getData() {
        return data;
    }

    public void setData(List<Data> data) {
        this.data = data;
    }

    public String getCart_count_itemwise() {
        return cart_count_itemwise;
    }

    public void setCart_count_itemwise(String cart_count_itemwise) {
        this.cart_count_itemwise = cart_count_itemwise;
    }
}