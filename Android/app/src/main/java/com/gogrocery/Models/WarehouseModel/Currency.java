package com.gogrocery.Models.WarehouseModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Currency {

@SerializedName("currency_id")
@Expose
private Integer currencyId;
@SerializedName("currency_name")
@Expose
private String currencyName;

public Integer getCurrencyId() {
return currencyId;
}

public void setCurrencyId(Integer currencyId) {
this.currencyId = currencyId;
}

public String getCurrencyName() {
return currencyName;
}

public void setCurrencyName(String currencyName) {
this.currencyName = currencyName;
}

}