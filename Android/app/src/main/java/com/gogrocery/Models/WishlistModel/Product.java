package com.gogrocery.Models.WishlistModel;

import java.util.List;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Product {

    @SerializedName("id")
    @Expose
    private Integer id;
    @SerializedName("name")
    @Expose
    private String name;
    @SerializedName("slug")
    @Expose
    private String slug;

    @SerializedName("product_image")
    @Expose
    private List<ProductImage> productImage = null;
    @SerializedName("custom_field")
    @Expose
    private List<CustomField> customField = null;
    @SerializedName("brand")
    @Expose
    private Brand brand;
    @SerializedName("channel_price")
    @Expose
    private ChannelPrice channelPrice;


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

    public String getSlug() {
        return slug;
    }

    public void setSlug(String slug) {
        this.slug = slug;
    }

    public List<ProductImage> getProductImage() {
        return productImage;
    }

    public void setProductImage(List<ProductImage> productImage) {
        this.productImage = productImage;
    }

    public List<CustomField> getCustomField() {
        return customField;
    }

    public void setCustomField(List<CustomField> customField) {
        this.customField = customField;
    }

    public Brand getBrand() {
        return brand;
    }

    public void setBrand(Brand brand) {
        this.brand = brand;
    }

    public ChannelPrice getChannelPrice() {
        return channelPrice;
    }

    public void setChannelPrice(ChannelPrice channelPrice) {
        this.channelPrice = channelPrice;
    }

}