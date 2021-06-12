package com.gogrocery.Models.CMS_NEW_Model;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.List;

public class VariantProductByCategoryId {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("name")
@Expose
private String name;
@SerializedName("sku")
@Expose
private String sku;
@SerializedName("default_price")
@Expose
private Integer defaultPrice;
@SerializedName("weight")
@Expose
private String weight;
@SerializedName("slug")
@Expose
private String slug;
@SerializedName("veg_nonveg_type")
@Expose
private String vegNonvegType;
@SerializedName("product_image")
@Expose
private List<ProductImage_> productImage = null;
@SerializedName("stock_data")
@Expose
private StockData_ stockData;
@SerializedName("brand")
@Expose
private String brand;
@SerializedName("website_id")
@Expose
private Integer websiteId;

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

public Integer getDefaultPrice() {
return defaultPrice;
}

public void setDefaultPrice(Integer defaultPrice) {
this.defaultPrice = defaultPrice;
}

public String getWeight() {
return weight;
}

public void setWeight(String weight) {
this.weight = weight;
}

public String getSlug() {
return slug;
}

public void setSlug(String slug) {
this.slug = slug;
}

public String getVegNonvegType() {
return vegNonvegType;
}

public void setVegNonvegType(String vegNonvegType) {
this.vegNonvegType = vegNonvegType;
}

public List<ProductImage_> getProductImage() {
return productImage;
}

public void setProductImage(List<ProductImage_> productImage) {
this.productImage = productImage;
}

public StockData_ getStockData() {
return stockData;
}

public void setStockData(StockData_ stockData) {
this.stockData = stockData;
}

public String getBrand() {
return brand;
}

public void setBrand(String brand) {
this.brand = brand;
}

public Integer getWebsiteId() {
return websiteId;
}

public void setWebsiteId(Integer websiteId) {
this.websiteId = websiteId;
}

}