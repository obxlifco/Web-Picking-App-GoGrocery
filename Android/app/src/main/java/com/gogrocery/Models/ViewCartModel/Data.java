package com.gogrocery.Models.ViewCartModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Data {

    @SerializedName("id")
    @Expose
    private Integer id;
    @SerializedName("product_id")
    @Expose
    private ProductId productId;
    @SerializedName("website_id")
    @Expose
    private Integer websiteId;
    @SerializedName("device_id")
    @Expose
    private String deviceId;
    @SerializedName("product_name")
    @Expose
    private String productName;
    @SerializedName("product_sku")
    @Expose
    private String productSku;
    @SerializedName("quantity")
    @Expose
    private Integer quantity;

    @SerializedName("new_default_price")
    @Expose
    private String newDefaultPrice;
    @SerializedName("new_default_price_unit")
    @Expose
    private String newDefaultPriceUnit;
    @SerializedName("discount_price_unit")
    @Expose
    private String discountPriceUnit;
    @SerializedName("discount_price")
    @Expose
    private String discountPrice;
    @SerializedName("discount_amount")
    @Expose
    private String discountAmount;

    @SerializedName("default_price")
    @Expose
    private String defaultPrice;
    @SerializedName("disc_type")
    @Expose
    private String disc_type;
    @SerializedName("custom_field_name")
    @Expose
    private String customFieldName;
    @SerializedName("custom_field_value")
    @Expose
    private String customFieldValue;
    @SerializedName("weight")
    @Expose
    private String weight;
    @SerializedName("unit")
    @Expose
    private String unit;

    public String getCustomFieldName() {
        return customFieldName;
    }

    public void setCustomFieldName(String customFieldName) {
        this.customFieldName = customFieldName;
    }

    public String getCustomFieldValue() {
        return customFieldValue;
    }

    public void setCustomFieldValue(String customFieldValue) {
        this.customFieldValue = customFieldValue;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public ProductId getProductId() {
        return productId;
    }

    public void setProductId(ProductId productId) {
        this.productId = productId;
    }

    public Integer getWebsiteId() {
        return websiteId;
    }

    public void setWebsiteId(Integer websiteId) {
        this.websiteId = websiteId;
    }

    public String getDeviceId() {
        return deviceId;
    }

    public void setDeviceId(String deviceId) {
        this.deviceId = deviceId;
    }


    public String getProductName() {
        return productName;
    }

    public void setProductName(String productName) {
        this.productName = productName;
    }

    public String getProductSku() {
        return productSku;
    }

    public void setProductSku(String productSku) {
        this.productSku = productSku;
    }


    public Integer getQuantity() {
        return quantity;
    }

    public void setQuantity(Integer quantity) {
        this.quantity = quantity;
    }


    public String getNewDefaultPrice() {
        return newDefaultPrice;
    }

    public void setNewDefaultPrice(String newDefaultPrice) {
        this.newDefaultPrice = newDefaultPrice;
    }

    public String getNewDefaultPriceUnit() {
        return newDefaultPriceUnit;
    }

    public void setNewDefaultPriceUnit(String newDefaultPriceUnit) {
        this.newDefaultPriceUnit = newDefaultPriceUnit;
    }

    public String getDiscountPriceUnit() {
        return discountPriceUnit;
    }

    public void setDiscountPriceUnit(String discountPriceUnit) {
        this.discountPriceUnit = discountPriceUnit;
    }

    public String getDiscountPrice() {
        return discountPrice;
    }

    public void setDiscountPrice(String discountPrice) {
        this.discountPrice = discountPrice;
    }

    public String getDiscountAmount() {
        return discountAmount;
    }

    public void setDiscountAmount(String discountAmount) {
        this.discountAmount = discountAmount;
    }


    public String getDefaultPrice() {
        return defaultPrice;
    }

    public void setDefaultPrice(String defaultPrice) {
        this.defaultPrice = defaultPrice;
    }

    public String getDisc_type() {
        return disc_type;
    }

    public void setDisc_type(String disc_type) {
        this.disc_type = disc_type;
    }

    public String getWeight() {
        return weight;
    }

    public void setWeight(String weight) {
        this.weight = weight;
    }

    public String getUnit() {
        return unit;
    }

    public void setUnit(String unit) {
        this.unit = unit;
    }
}