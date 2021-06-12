package com.gogrocery.Models.OrderDetailsModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Product {

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
    private String defaultPrice;
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
    private Object ean;
    @SerializedName("product_image")
    @Expose
    private ProductImage productImage;
    @SerializedName("uom")
    @Expose
    private Object uom;

    public Object getUom() {
        return uom;
    }

    public void setUom(Object uom) {
        this.uom = uom;
    }

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

    public String getDefaultPrice() {
        return defaultPrice;
    }

    public void setDefaultPrice(String defaultPrice) {
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

    public Object getEan() {
        return ean;
    }

    public void setEan(Object ean) {
        this.ean = ean;
    }

    public ProductImage getProductImage() {
        return productImage;
    }

    public void setProductImage(ProductImage productImage) {
        this.productImage = productImage;
    }

}