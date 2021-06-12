package com.gogrocery.Models.SaveListDetailPage;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class SaveListDetailListData {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("name")
@Expose
private String name;
@SerializedName("sku")
@Expose
private String sku;
@SerializedName("weight")
@Expose
private Object weight;
@SerializedName("visibility_id")
@Expose
private Integer visibilityId;
@SerializedName("default_price")
@Expose
private Object defaultPrice;
@SerializedName("slug")
@Expose
private String slug;
@SerializedName("twitter_addstatus")
@Expose
private Object twitterAddstatus;
@SerializedName("amazon_addstatus")
@Expose
private Object amazonAddstatus;
@SerializedName("ean")
@Expose
private String ean;
@SerializedName("product_image")
@Expose
private List<ProductImage> productImage = null;
@SerializedName("product")
@Expose
private Product product;
@SerializedName("savelist_name")
@Expose
private String savelistName;
@SerializedName("savelist_id")
@Expose
private Integer savelistId;

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

public Object getWeight() {
return weight;
}

public void setWeight(Object weight) {
this.weight = weight;
}

public Integer getVisibilityId() {
return visibilityId;
}

public void setVisibilityId(Integer visibilityId) {
this.visibilityId = visibilityId;
}

public Object getDefaultPrice() {
return defaultPrice;
}

public void setDefaultPrice(Object defaultPrice) {
this.defaultPrice = defaultPrice;
}

public String getSlug() {
return slug;
}

public void setSlug(String slug) {
this.slug = slug;
}

public Object getTwitterAddstatus() {
return twitterAddstatus;
}

public void setTwitterAddstatus(Object twitterAddstatus) {
this.twitterAddstatus = twitterAddstatus;
}

public Object getAmazonAddstatus() {
return amazonAddstatus;
}

public void setAmazonAddstatus(Object amazonAddstatus) {
this.amazonAddstatus = amazonAddstatus;
}

public String getEan() {
return ean;
}

public void setEan(String ean) {
this.ean = ean;
}

public List<ProductImage> getProductImage() {
return productImage;
}

public void setProductImage(List<ProductImage> productImage) {
this.productImage = productImage;
}

public Product getProduct() {
return product;
}

public void setProduct(Product product) {
this.product = product;
}

public String getSavelistName() {
return savelistName;
}

public void setSavelistName(String savelistName) {
this.savelistName = savelistName;
}

public Integer getSavelistId() {
return savelistId;
}

public void setSavelistId(Integer savelistId) {
this.savelistId = savelistId;
}

}