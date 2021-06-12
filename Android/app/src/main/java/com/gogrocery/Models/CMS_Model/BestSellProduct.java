package com.gogrocery.Models.CMS_Model;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class BestSellProduct {

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
private String defaultPrice;
@SerializedName("weight")
@Expose
private Object weight;
@SerializedName("slug")
@Expose
private String slug;
@SerializedName("veg_nonveg_type")
@Expose
private String vegNonvegType;
@SerializedName("product_image")
@Expose
private List<ProductImage> productImage = null;
@SerializedName("stock_data")
@Expose
private StockData stockData;
@SerializedName("brand")
@Expose
private Brand brand;
@SerializedName("warehouse_id")
@Expose
private Integer warehouseId;
@SerializedName("website_id")
@Expose
private Integer websiteId;
@SerializedName("variant_product")
@Expose
private List<VariantProduct> variantProduct = null;

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

public String getDefaultPrice() {
return defaultPrice;
}

public void setDefaultPrice(String defaultPrice) {
this.defaultPrice = defaultPrice;
}

public Object getWeight() {
return weight;
}

public void setWeight(Object weight) {
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

public List<ProductImage> getProductImage() {
return productImage;
}

public void setProductImage(List<ProductImage> productImage) {
this.productImage = productImage;
}

public StockData getStockData() {
return stockData;
}

public void setStockData(StockData stockData) {
this.stockData = stockData;
}

public Brand getBrand() {
return brand;
}

public void setBrand(Brand brand) {
this.brand = brand;
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

public List<VariantProduct> getVariantProduct() {
return variantProduct;
}

public void setVariantProduct(List<VariantProduct> variantProduct) {
this.variantProduct = variantProduct;
}

}