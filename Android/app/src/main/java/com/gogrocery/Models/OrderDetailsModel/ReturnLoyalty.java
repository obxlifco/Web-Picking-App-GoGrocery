package com.gogrocery.Models.OrderDetailsModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class ReturnLoyalty {

@SerializedName("return_loyalty_valid_from")
@Expose
private String returnLoyaltyValidFrom;
@SerializedName("return_loyalty_valid_to")
@Expose
private String returnLoyaltyValidTo;
@SerializedName("return_loyalty_amount")
@Expose
private Integer returnLoyaltyAmount;
@SerializedName("return_loyalty_points")
@Expose
private Integer returnLoyaltyPoints;

public String getReturnLoyaltyValidFrom() {
return returnLoyaltyValidFrom;
}

public void setReturnLoyaltyValidFrom(String returnLoyaltyValidFrom) {
this.returnLoyaltyValidFrom = returnLoyaltyValidFrom;
}

public String getReturnLoyaltyValidTo() {
return returnLoyaltyValidTo;
}

public void setReturnLoyaltyValidTo(String returnLoyaltyValidTo) {
this.returnLoyaltyValidTo = returnLoyaltyValidTo;
}

public Integer getReturnLoyaltyAmount() {
return returnLoyaltyAmount;
}

public void setReturnLoyaltyAmount(Integer returnLoyaltyAmount) {
this.returnLoyaltyAmount = returnLoyaltyAmount;
}

public Integer getReturnLoyaltyPoints() {
return returnLoyaltyPoints;
}

public void setReturnLoyaltyPoints(Integer returnLoyaltyPoints) {
this.returnLoyaltyPoints = returnLoyaltyPoints;
}

}