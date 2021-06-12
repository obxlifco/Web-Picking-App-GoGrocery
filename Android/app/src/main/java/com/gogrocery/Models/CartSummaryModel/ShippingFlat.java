package com.gogrocery.Models.CartSummaryModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class ShippingFlat {

@SerializedName("shipping_type")
@Expose
private String shippingType;
@SerializedName("mthod_type")
@Expose
private Integer mthodType;
@SerializedName("mthod_name")
@Expose
private String mthodName;
@SerializedName("flat_price")
@Expose
private Double flatPrice;
@SerializedName("handling_fees_type")
@Expose
private Integer handlingFeesType;
@SerializedName("handling_price")
@Expose
private Double handlingPrice;

public String getShippingType() {
return shippingType;
}

public void setShippingType(String shippingType) {
this.shippingType = shippingType;
}

public Integer getMthodType() {
return mthodType;
}

public void setMthodType(Integer mthodType) {
this.mthodType = mthodType;
}

public String getMthodName() {
return mthodName;
}

public void setMthodName(String mthodName) {
this.mthodName = mthodName;
}

public Double getFlatPrice() {
return flatPrice;
}

public void setFlatPrice(Double flatPrice) {
this.flatPrice = flatPrice;
}

public Integer getHandlingFeesType() {
return handlingFeesType;
}

public void setHandlingFeesType(Integer handlingFeesType) {
this.handlingFeesType = handlingFeesType;
}

public Double getHandlingPrice() {
return handlingPrice;
}

public void setHandlingPrice(Double handlingPrice) {
this.handlingPrice = handlingPrice;
}

}