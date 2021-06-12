package com.gogrocery.Models.PaymentTransaction;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class TransactionData {

    @SerializedName("customer_id")
    @Expose
    private String customerId;
    @SerializedName("custom_order_id")
    @Expose
    private String customOrderId;
    @SerializedName("transaction_id")
    @Expose
    private String transactionId;
    @SerializedName("order_amount")
    @Expose
    private String orderAmount;
    @SerializedName("payment_redirect")
    @Expose
    private Boolean paymentRedirect;

    public Boolean getPaymentRedirect() {
        return paymentRedirect;
    }

    public void setPaymentRedirect(Boolean paymentRedirect) {
        this.paymentRedirect = paymentRedirect;
    }

    public String getCustomerId() {
        return customerId;
    }

    public void setCustomerId(String customerId) {
        this.customerId = customerId;
    }

    public String getCustomOrderId() {
        return customOrderId;
    }

    public void setCustomOrderId(String customOrderId) {
        this.customOrderId = customOrderId;
    }

    public String getTransactionId() {
        return transactionId;
    }

    public void setTransactionId(String transactionId) {
        this.transactionId = transactionId;
    }

    public String getOrderAmount() {
        return orderAmount;
    }

    public void setOrderAmount(String orderAmount) {
        this.orderAmount = orderAmount;
    }

}