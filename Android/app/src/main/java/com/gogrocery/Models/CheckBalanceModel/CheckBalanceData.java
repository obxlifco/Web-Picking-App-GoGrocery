package com.gogrocery.Models.CheckBalanceModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class CheckBalanceData {

@SerializedName("burn_loyalty")
@Expose
private BurnLoyalty burnLoyalty;
@SerializedName("return_loyalty")
@Expose
private ReturnLoyalty returnLoyalty;

public BurnLoyalty getBurnLoyalty() {
return burnLoyalty;
}

public void setBurnLoyalty(BurnLoyalty burnLoyalty) {
this.burnLoyalty = burnLoyalty;
}

public ReturnLoyalty getReturnLoyalty() {
return returnLoyalty;
}

public void setReturnLoyalty(ReturnLoyalty returnLoyalty) {
this.returnLoyalty = returnLoyalty;
}

}