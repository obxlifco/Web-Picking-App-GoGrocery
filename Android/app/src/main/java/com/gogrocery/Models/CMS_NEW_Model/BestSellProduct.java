package com.gogrocery.Models.CMS_NEW_Model;

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
    @SerializedName("channel_price")
    @Expose
    private String channel_price;
    @SerializedName("new_default_price")
    @Expose
    private String new_default_price;

    @SerializedName("new_default_price_unit")
    @Expose
    private String new_default_price_unit;

    @SerializedName("discount_price_unit")
    @Expose
    private String discount_price_unit;

    @SerializedName("discount_price")
    @Expose
    private String discount_price;

    @SerializedName("discount_amount")
    @Expose
    private String discount_amount;

    @SerializedName("disc_type")
    @Expose
    private String disc_type;

    @SerializedName("coupon")
    @Expose
    private String coupon;


    @SerializedName("weight")
    @Expose
    private String weight;
    @SerializedName("uom")
    @Expose
    private String uom;

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

    public String getWeight() {
        return weight;
    }

    public void setWeight(String weight) {
        this.weight = weight;
    }

    public String getUom() {
        return uom;
    }

    public void setUom(String uom) {
        this.uom = uom;
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

    public String getChannel_price() {
        return channel_price;
    }

    public void setChannel_price(String channel_price) {
        this.channel_price = channel_price;
    }

    public String getNew_default_price() {
        return new_default_price;
    }

    public void setNew_default_price(String new_default_price) {
        this.new_default_price = new_default_price;
    }

    public String getNew_default_price_unit() {
        return new_default_price_unit;
    }

    public void setNew_default_price_unit(String new_default_price_unit) {
        this.new_default_price_unit = new_default_price_unit;
    }

    public String getDiscount_price_unit() {
        return discount_price_unit;
    }

    public void setDiscount_price_unit(String discount_price_unit) {
        this.discount_price_unit = discount_price_unit;
    }

    public String getDiscount_price() {
        return discount_price;
    }

    public void setDiscount_price(String discount_price) {
        this.discount_price = discount_price;
    }

    public String getDiscount_amount() {
        return discount_amount;
    }

    public void setDiscount_amount(String discount_amount) {
        this.discount_amount = discount_amount;
    }

    public String getDisc_type() {
        return disc_type;
    }

    public void setDisc_type(String disc_type) {
        this.disc_type = disc_type;
    }

    public String getCoupon() {
        return coupon;
    }

    public void setCoupon(String coupon) {
        this.coupon = coupon;
    }
}