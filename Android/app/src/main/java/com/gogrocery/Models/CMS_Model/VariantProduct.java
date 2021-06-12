package com.gogrocery.Models.CMS_Model;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class VariantProduct {

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
    private Object weight;
    @SerializedName("slug")
    @Expose
    private String slug;
    @SerializedName("veg_nonveg_type")
    @Expose
    private String vegNonvegType;
    @SerializedName("brand")
    @Expose
    private Brand brand;
    @SerializedName("product_image")
    @Expose
    private List<Object> productImage = null;
    @SerializedName("warehouse_id")
    @Expose
    private Integer warehouseId;
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

    public Brand getBrand() {
        return brand;
    }

    public void setBrand(Brand brand) {
        this.brand = brand;
    }

    public List<Object> getProductImage() {
        return productImage;
    }

    public void setProductImage(List<Object> productImage) {
        this.productImage = productImage;
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
}
