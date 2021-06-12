package com.gogrocery.Models.CheckBalanceModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class BurnLoyalty {

@SerializedName("minimum_order_amount")
@Expose
private Integer minimumOrderAmount;
@SerializedName("total_earn_amount")
@Expose
private Integer totalEarnAmount;
@SerializedName("total_earn_points")
@Expose
private Integer totalEarnPoints;
@SerializedName("total_burn_amount")
@Expose
private Integer totalBurnAmount;
@SerializedName("total_burn_points")
@Expose
private Integer totalBurnPoints;
@SerializedName("max_loyalty_amount_use_limit")
@Expose
private Integer maxLoyaltyAmountUseLimit;
@SerializedName("loyalty_amount")
@Expose
private Integer loyaltyAmount;
@SerializedName("loyalty_points")
@Expose
private Integer loyaltyPoints;
@SerializedName("remaning_earn_amount")
@Expose
private Integer remaningEarnAmount;
@SerializedName("remaning_earn_points")
@Expose
private Integer remaningEarnPoints;
@SerializedName("loyalty_end_date")
@Expose
private String loyaltyEndDate;
@SerializedName("rule_id")
@Expose
private Integer ruleId;

public Integer getMinimumOrderAmount() {
return minimumOrderAmount;
}

public void setMinimumOrderAmount(Integer minimumOrderAmount) {
this.minimumOrderAmount = minimumOrderAmount;
}

public Integer getTotalEarnAmount() {
return totalEarnAmount;
}

public void setTotalEarnAmount(Integer totalEarnAmount) {
this.totalEarnAmount = totalEarnAmount;
}

public Integer getTotalEarnPoints() {
return totalEarnPoints;
}

public void setTotalEarnPoints(Integer totalEarnPoints) {
this.totalEarnPoints = totalEarnPoints;
}

public Integer getTotalBurnAmount() {
return totalBurnAmount;
}

public void setTotalBurnAmount(Integer totalBurnAmount) {
this.totalBurnAmount = totalBurnAmount;
}

public Integer getTotalBurnPoints() {
return totalBurnPoints;
}

public void setTotalBurnPoints(Integer totalBurnPoints) {
this.totalBurnPoints = totalBurnPoints;
}

public Integer getMaxLoyaltyAmountUseLimit() {
return maxLoyaltyAmountUseLimit;
}

public void setMaxLoyaltyAmountUseLimit(Integer maxLoyaltyAmountUseLimit) {
this.maxLoyaltyAmountUseLimit = maxLoyaltyAmountUseLimit;
}

public Integer getLoyaltyAmount() {
return loyaltyAmount;
}

public void setLoyaltyAmount(Integer loyaltyAmount) {
this.loyaltyAmount = loyaltyAmount;
}

public Integer getLoyaltyPoints() {
return loyaltyPoints;
}

public void setLoyaltyPoints(Integer loyaltyPoints) {
this.loyaltyPoints = loyaltyPoints;
}

public Integer getRemaningEarnAmount() {
return remaningEarnAmount;
}

public void setRemaningEarnAmount(Integer remaningEarnAmount) {
this.remaningEarnAmount = remaningEarnAmount;
}

public Integer getRemaningEarnPoints() {
return remaningEarnPoints;
}

public void setRemaningEarnPoints(Integer remaningEarnPoints) {
this.remaningEarnPoints = remaningEarnPoints;
}

public String getLoyaltyEndDate() {
return loyaltyEndDate;
}

public void setLoyaltyEndDate(String loyaltyEndDate) {
this.loyaltyEndDate = loyaltyEndDate;
}

public Integer getRuleId() {
return ruleId;
}

public void setRuleId(Integer ruleId) {
this.ruleId = ruleId;
}

}