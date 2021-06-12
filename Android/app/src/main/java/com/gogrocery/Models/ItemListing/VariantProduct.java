package com.gogrocery.Models.ItemListing;

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
    private String weight;
    @SerializedName("slug")
    @Expose
    private String slug;
    @SerializedName("veg_nonveg_type")
    @Expose
    private String vegNonvegType;
    @SerializedName("brand")
    @Expose
    private String brand;
    @SerializedName("product_image")
    @Expose
    private List<Object> productImage = null;
    @SerializedName("warehouse_id")
    @Expose
    private Integer warehouseId;
    @SerializedName("website_id")
    @Expose
    private Integer websiteId;
    @SerializedName("brand_name")
    @Expose
    private String brandName;

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

    public String getBrand() {
        return brand;
    }

    public void setBrand(String brand) {
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

    public String getBrandName() {
        return brandName;
    }

    public void setBrandName(String brandName) {
        this.brandName = brandName;
    }
}
