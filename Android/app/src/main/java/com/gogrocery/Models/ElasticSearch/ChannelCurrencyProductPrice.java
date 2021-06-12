package com.gogrocery.Models.ElasticSearch;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class ChannelCurrencyProductPrice {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("promotions")
@Expose
private Object promotions;
@SerializedName("channel_id")
@Expose
private Integer channelId;
@SerializedName("currency_id")
@Expose
private Integer currencyId;
@SerializedName("product_id")
@Expose
private Integer productId;
@SerializedName("price")
@Expose
private Double price;
@SerializedName("cost")
@Expose
private Double cost;
@SerializedName("mrp")
@Expose
private Double mrp;
@SerializedName("min_quantity")
@Expose
private Object minQuantity;
@SerializedName("max_quantity")
@Expose
private Object maxQuantity;
@SerializedName("warehouse_id")
@Expose
private Integer warehouseId;
@SerializedName("website_id")
@Expose
private Integer websiteId;
@SerializedName("start_date")
@Expose
private String startDate;
@SerializedName("end_date")
@Expose
private Object endDate;
@SerializedName("product_price_type")
@Expose
private Integer productPriceType;

public Integer getId() {
return id;
}

public void setId(Integer id) {
this.id = id;
}

public Object getPromotions() {
return promotions;
}

public void setPromotions(Object promotions) {
this.promotions = promotions;
}

public Integer getChannelId() {
return channelId;
}

public void setChannelId(Integer channelId) {
this.channelId = channelId;
}

public Integer getCurrencyId() {
return currencyId;
}

public void setCurrencyId(Integer currencyId) {
this.currencyId = currencyId;
}

public Integer getProductId() {
return productId;
}

public void setProductId(Integer productId) {
this.productId = productId;
}

public Double getPrice() {
return price;
}

public void setPrice(Double price) {
this.price = price;
}

public Double getCost() {
return cost;
}

public void setCost(Double cost) {
this.cost = cost;
}

public Double getMrp() {
return mrp;
}

public void setMrp(Double mrp) {
this.mrp = mrp;
}

public Object getMinQuantity() {
return minQuantity;
}

public void setMinQuantity(Object minQuantity) {
this.minQuantity = minQuantity;
}

public Object getMaxQuantity() {
return maxQuantity;
}

public void setMaxQuantity(Object maxQuantity) {
this.maxQuantity = maxQuantity;
}

public Integer getWarehouseId() {
return warehouseId;
}

public void setWarehouseId(Integer warehouseId) {
this.warehouseId = warehouseId;
}

public Integer getWebsiteId() {
return websiteId;
}

public void setWebsiteId(Integer websiteId) {
this.websiteId = websiteId;
}

public String getStartDate() {
return startDate;
}

public void setStartDate(String startDate) {
this.startDate = startDate;
}

public Object getEndDate() {
return endDate;
}

public void setEndDate(Object endDate) {
this.endDate = endDate;
}

public Integer getProductPriceType() {
return productPriceType;
}

public void setProductPriceType(Integer productPriceType) {
this.productPriceType = productPriceType;
}

}