package com.gogrocery.Models.OrderDetailsModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class BurnLoyalty {

@SerializedName("minimum_order_amount")
@Expose
private String minimumOrderAmount;
@SerializedName("total_earn_amount")
@Expose
private String totalEarnAmount;
@SerializedName("total_earn_points")
@Expose
private String totalEarnPoints;
@SerializedName("total_burn_amount")
@Expose
private String totalBurnAmount;
@SerializedName("total_burn_points")
@Expose
private String totalBurnPoints;
@SerializedName("max_loyalty_amount_use_limit")
@Expose
private String maxLoyaltyAmountUseLimit;
@SerializedName("loyalty_amount")
@Expose
private String loyaltyAmount;
@SerializedName("loyalty_points")
@Expose
private String loyaltyPoints;
@SerializedName("remaning_earn_amount")
@Expose
private String remaningEarnAmount;
@SerializedName("remaning_earn_points")
@Expose
private String remaningEarnPoints;
@SerializedName("loyalty_end_date")
@Expose
private String loyaltyEndDate;
@SerializedName("rule_id")
@Expose
private String ruleId;
@SerializedName("loyalty_points_amount")
@Expose
private String loyaltyPointsAmount;

public String getMinimumOrderAmount() {
return minimumOrderAmount;
}

public void setMinimumOrderAmount(String minimumOrderAmount) {
this.minimumOrderAmount = minimumOrderAmount;
}

public String getTotalEarnAmount() {
return totalEarnAmount;
}

public void setTotalEarnAmount(String totalEarnAmount) {
this.totalEarnAmount = totalEarnAmount;
}

public String getTotalEarnPoints() {
return totalEarnPoints;
}

public void setTotalEarnPoints(String totalEarnPoints) {
this.totalEarnPoints = totalEarnPoints;
}

public String getTotalBurnAmount() {
return totalBurnAmount;
}

public void setTotalBurnAmount(String totalBurnAmount) {
this.totalBurnAmount = totalBurnAmount;
}

public String getTotalBurnPoints() {
return totalBurnPoints;
}

public void setTotalBurnPoints(String totalBurnPoints) {
this.totalBurnPoints = totalBurnPoints;
}

public String getMaxLoyaltyAmountUseLimit() {
return maxLoyaltyAmountUseLimit;
}

public void setMaxLoyaltyAmountUseLimit(String maxLoyaltyAmountUseLimit) {
this.maxLoyaltyAmountUseLimit = maxLoyaltyAmountUseLimit;
}

public String getLoyaltyAmount() {
return loyaltyAmount;
}

public void setLoyaltyAmount(String loyaltyAmount) {
this.loyaltyAmount = loyaltyAmount;
}

public String getLoyaltyPoints() {
return loyaltyPoints;
}

public void setLoyaltyPoints(String loyaltyPoints) {
this.loyaltyPoints = loyaltyPoints;
}

public String getRemaningEarnAmount() {
return remaningEarnAmount;
}

public void setRemaningEarnAmount(String remaningEarnAmount) {
this.remaningEarnAmount = remaningEarnAmount;
}

public String getRemaningEarnPoints() {
return remaningEarnPoints;
}

public void setRemaningEarnPoints(String remaningEarnPoints) {
this.remaningEarnPoints = remaningEarnPoints;
}

public String getLoyaltyEndDate() {
return loyaltyEndDate;
}

public void setLoyaltyEndDate(String loyaltyEndDate) {
this.loyaltyEndDate = loyaltyEndDate;
}

public String getRuleId() {
return ruleId;
}

public void setRuleId(String ruleId) {
this.ruleId = ruleId;
}

public String getLoyaltyPointsAmount() {
return loyaltyPointsAmount;
}

public void setLoyaltyPointsAmount(String loyaltyPointsAmount) {
this.loyaltyPointsAmount = loyaltyPointsAmount;
}

}