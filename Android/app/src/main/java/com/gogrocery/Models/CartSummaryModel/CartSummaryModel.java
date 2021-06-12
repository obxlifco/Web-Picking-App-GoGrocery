package com.gogrocery.Models.CartSummaryModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class CartSummaryModel {

    @SerializedName("status")
    @Expose
    private String status;
    @SerializedName("data")
    @Expose
    private Data data;
    @SerializedName("usable_loyalty")
    @Expose
    private String usableLoyalty;
    @SerializedName("remain_loyalty")
    @Expose
    private String remainLoyalty;
    @SerializedName("rule_id")
    @Expose
    private String ruleId;
    @SerializedName("redeem_limit")
    @Expose
    private String redeemLimit;

    @SerializedName("minimum_order_amount")
    @Expose
    private String minimum_order_amount;


    @SerializedName("minimum_order_amount_check")
    @Expose
    private String minimum_order_amount_check;


    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public Data getData() {
        return data;
    }

    public void setData(Data data) {
        this.data = data;
    }

    public String getUsableLoyalty() {
        return usableLoyalty;
    }

    public void setUsableLoyalty(String usableLoyalty) {
        this.usableLoyalty = usableLoyalty;
    }

    public String getRemainLoyalty() {
        return remainLoyalty;
    }

    public void setRemainLoyalty(String remainLoyalty) {
        this.remainLoyalty = remainLoyalty;
    }

    public String getRuleId() {
        return ruleId;
    }

    public void setRuleId(String ruleId) {
        this.ruleId = ruleId;
    }

    public String getRedeemLimit() {
        return redeemLimit;
    }

    public void setRedeemLimit(String redeemLimit) {
        this.redeemLimit = redeemLimit;
    }

    public String getMinimum_order_amount() {
        return minimum_order_amount;
    }

    public void setMinimum_order_amount(String minimum_order_amount) {
        this.minimum_order_amount = minimum_order_amount;
    }

    public String getMinimum_order_amount_check() {
        return minimum_order_amount_check;
    }

    public void setMinimum_order_amount_check(String minimum_order_amount_check) {
        this.minimum_order_amount_check = minimum_order_amount_check;
    }
}