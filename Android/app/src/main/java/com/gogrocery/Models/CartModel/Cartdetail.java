package com.gogrocery.Models.CartModel;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Cartdetail {

@SerializedName("id")
@Expose
private String id;
@SerializedName("product_images")
@Expose
private List<ProductImage> productImages = null;
@SerializedName("order_id")
@Expose
private String orderId;
@SerializedName("website_id")
@Expose
private String websiteId;
@SerializedName("name")
@Expose
private String name;
@SerializedName("sku")
@Expose
private String sku;
@SerializedName("description")
@Expose
private String description;
@SerializedName("url")
@Expose
private String url;
@SerializedName("visibility_id")
@Expose
private String visibilityId;
@SerializedName("status")
@Expose
private String status;
@SerializedName("brand")
@Expose
private String brand;
@SerializedName("default_price")
@Expose
private String defaultPrice;
@SerializedName("order_price")
@Expose
private String orderPrice;
@SerializedName("slug")
@Expose
private String slug;
@SerializedName("created")
@Expose
private String created;
@SerializedName("modified")
@Expose
private String modified;
@SerializedName("visible_in_listing")
@Expose
private String visibleInListing;
@SerializedName("category_id")
@Expose
private String categoryId;
@SerializedName("qty")
@Expose
private String qty;
@SerializedName("new_default_price")
@Expose
private Double newDefaultPrice;
@SerializedName("new_default_price_unit")
@Expose
private Double newDefaultPriceUnit;
@SerializedName("discount_price_unit")
@Expose
private Double discountPriceUnit;
@SerializedName("discount_price")
@Expose
private Double discountPrice;
@SerializedName("discount_amount")
@Expose
private String discountAmount;
@SerializedName("disc_type")
@Expose
private String discType;
@SerializedName("coupon")
@Expose
private String coupon;
@SerializedName("tax_price_unit")
@Expose
private String taxPriceUnit;
@SerializedName("tax_price")
@Expose
private String taxPrice;
@SerializedName("tax_percentage")
@Expose
private String taxPercentage;
@SerializedName("tax_name")
@Expose
private String taxName;
@SerializedName("cgst")
@Expose
private String cgst;
@SerializedName("sgst")
@Expose
private String sgst;
@SerializedName("igst")
@Expose
private String igst;
@SerializedName("cess")
@Expose
private String cess;
@SerializedName("is_igst")
@Expose
private String isIgst;
@SerializedName("tax_type")
@Expose
private String taxType;

public String getId() {
return id;
}

public void setId(String id) {
this.id = id;
}

public List<ProductImage> getProductImages() {
return productImages;
}

public void setProductImages(List<ProductImage> productImages) {
this.productImages = productImages;
}

public String getOrderId() {
return orderId;
}

public void setOrderId(String orderId) {
this.orderId = orderId;
}

public String getWebsiteId() {
return websiteId;
}

public void setWebsiteId(String websiteId) {
this.websiteId = websiteId;
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

public String getDescription() {
return description;
}

public void setDescription(String description) {
this.description = description;
}

public String getUrl() {
return url;
}

public void setUrl(String url) {
this.url = url;
}

public String getVisibilityId() {
return visibilityId;
}

public void setVisibilityId(String visibilityId) {
this.visibilityId = visibilityId;
}

public String getStatus() {
return status;
}

public void setStatus(String status) {
this.status = status;
}

public String getBrand() {
return brand;
}

public void setBrand(String brand) {
this.brand = brand;
}

public String getDefaultPrice() {
return defaultPrice;
}

public void setDefaultPrice(String defaultPrice) {
this.defaultPrice = defaultPrice;
}

public String getOrderPrice() {
return orderPrice;
}

public void setOrderPrice(String orderPrice) {
this.orderPrice = orderPrice;
}

public String getSlug() {
return slug;
}

public void setSlug(String slug) {
this.slug = slug;
}

public String getCreated() {
return created;
}

public void setCreated(String created) {
this.created = created;
}

public String getModified() {
return modified;
}

public void setModified(String modified) {
this.modified = modified;
}

public String getVisibleInListing() {
return visibleInListing;
}

public void setVisibleInListing(String visibleInListing) {
this.visibleInListing = visibleInListing;
}

public String getCategoryId() {
return categoryId;
}

public void setCategoryId(String categoryId) {
this.categoryId = categoryId;
}

public String getQty() {
return qty;
}

public void setQty(String qty) {
this.qty = qty;
}

public Double getNewDefaultPrice() {
return newDefaultPrice;
}

public void setNewDefaultPrice(Double newDefaultPrice) {
this.newDefaultPrice = newDefaultPrice;
}

public Double getNewDefaultPriceUnit() {
return newDefaultPriceUnit;
}

public void setNewDefaultPriceUnit(Double newDefaultPriceUnit) {
this.newDefaultPriceUnit = newDefaultPriceUnit;
}

public Double getDiscountPriceUnit() {
return discountPriceUnit;
}

public void setDiscountPriceUnit(Double discountPriceUnit) {
this.discountPriceUnit = discountPriceUnit;
}

public Double getDiscountPrice() {
return discountPrice;
}

public void setDiscountPrice(Double discountPrice) {
this.discountPrice = discountPrice;
}

public String getDiscountAmount() {
return discountAmount;
}

public void setDiscountAmount(String discountAmount) {
this.discountAmount = discountAmount;
}

public String getDiscType() {
return discType;
}

public void setDiscType(String discType) {
this.discType = discType;
}

public String getCoupon() {
return coupon;
}

public void setCoupon(String coupon) {
this.coupon = coupon;
}

public String getTaxPriceUnit() {
return taxPriceUnit;
}

public void setTaxPriceUnit(String taxPriceUnit) {
this.taxPriceUnit = taxPriceUnit;
}

public String getTaxPrice() {
return taxPrice;
}

public void setTaxPrice(String taxPrice) {
this.taxPrice = taxPrice;
}

public String getTaxPercentage() {
return taxPercentage;
}

public void setTaxPercentage(String taxPercentage) {
this.taxPercentage = taxPercentage;
}

public String getTaxName() {
return taxName;
}

public void setTaxName(String taxName) {
this.taxName = taxName;
}

public String getCgst() {
return cgst;
}

public void setCgst(String cgst) {
this.cgst = cgst;
}

public String getSgst() {
return sgst;
}

public void setSgst(String sgst) {
this.sgst = sgst;
}

public String getIgst() {
return igst;
}

public void setIgst(String igst) {
this.igst = igst;
}

public String getCess() {
return cess;
}

public void setCess(String cess) {
this.cess = cess;
}

public String getIsIgst() {
return isIgst;
}

public void setIsIgst(String isIgst) {
this.isIgst = isIgst;
}

public String getTaxType() {
return taxType;
}

public void setTaxType(String taxType) {
this.taxType = taxType;
}

}