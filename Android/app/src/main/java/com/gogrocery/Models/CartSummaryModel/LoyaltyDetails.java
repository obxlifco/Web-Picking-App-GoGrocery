package com.gogrocery.Models.CartSummaryModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class LoyaltyDetails {

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

}