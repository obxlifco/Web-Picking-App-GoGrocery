package com.gogrocery.Models.ElasticSearch;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class ProductDetails {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("name")
@Expose
private String name;
@SerializedName("sku")
@Expose
private String sku;
@SerializedName("brand")
@Expose
private String brand;
@SerializedName("weight")
@Expose
private String weight;
@SerializedName("visibility_id")
@Expose
private Integer visibilityId;
@SerializedName("default_price")
@Expose
private Integer defaultPrice;
@SerializedName("slug")
@Expose
private String slug;
@SerializedName("twitter_addstatus")
@Expose
private String twitterAddstatus;
@SerializedName("amazon_addstatus")
@Expose
private String amazonAddstatus;
@SerializedName("ean")
@Expose
private String ean;
@SerializedName("description")
@Expose
private String description;
@SerializedName("product_images")
@Expose
private List<ProductImage> productImages = null;
@SerializedName("inventory")
@Expose
private List<Inventory> inventory = null;
@SerializedName("channel_currency_product_price")
@Expose
private List<ChannelCurrencyProductPrice> channelCurrencyProductPrice = null;

public Integer getId() {
return id;
}

public void setId(Integer id) {
this.id = id;
}

public String getName() {
return name;
}

public void setName(String name) {
this.name = name;
}

public String getSku() {
return sku;
}

public void setSku(String sku) {
this.sku = sku;
}

public String getBrand() {
return brand;
}

public void setBrand(String brand) {
this.brand = brand;
}

public String getWeight() {
return weight;
}

public void setWeight(String weight) {
this.weight = weight;
}

public Integer getVisibilityId() {
return visibilityId;
}

public void setVisibilityId(Integer visibilityId) {
this.visibilityId = visibilityId;
}

public Integer getDefaultPrice() {
return defaultPrice;
}

public void setDefaultPrice(Integer defaultPrice) {
this.defaultPrice = defaultPrice;
}

public String getSlug() {
return slug;
}

public void setSlug(String slug) {
this.slug = slug;
}

public String getTwitterAddstatus() {
return twitterAddstatus;
}

public void setTwitterAddstatus(String twitterAddstatus) {
this.twitterAddstatus = twitterAddstatus;
}

public String getAmazonAddstatus() {
return amazonAddstatus;
}

public void setAmazonAddstatus(String amazonAddstatus) {
this.amazonAddstatus = amazonAddstatus;
}

public String getEan() {
return ean;
}

public void setEan(String ean) {
this.ean = ean;
}

public String getDescription() {
return description;
}

public void setDescription(String description) {
this.description = description;
}

public List<ProductImage> getProductImages() {
return productImages;
}

public void setProductImages(List<ProductImage> productImages) {
this.productImages = productImages;
}

public List<Inventory> getInventory() {
return inventory;
}

public void setInventory(List<Inventory> inventory) {
this.inventory = inventory;
}

public List<ChannelCurrencyProductPrice> getChannelCurrencyProductPrice() {
return channelCurrencyProductPrice;
}

public void setChannelCurrencyProductPrice(List<ChannelCurrencyProductPrice> channelCurrencyProductPrice) {
this.channelCurrencyProductPrice = channelCurrencyProductPrice;
}

}