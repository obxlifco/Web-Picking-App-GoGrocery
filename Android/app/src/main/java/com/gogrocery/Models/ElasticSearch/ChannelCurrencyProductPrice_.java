package com.gogrocery.Models.ElasticSearch;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class ChannelCurrencyProductPrice_ {

    @SerializedName("end_date")
    @Expose
    private Object endDate;
    @SerializedName("cost")
    @Expose
    private Double cost;
    @SerializedName("max_quantity")
    @Expose
    private Object maxQuantity;
    @SerializedName("mrp")
    @Expose
    private Double mrp;
    @SerializedName("promotions")
    @Expose
    private Object promotions;
    @SerializedName("min_quantity")
    @Expose
    private Object minQuantity;
    @SerializedName("price")
    @Expose
    private Double price;
    @SerializedName("product_id")
    @Expose
    private Integer productId;
    @SerializedName("id")
    @Expose
    private Integer id;
    @SerializedName("product_price_type")
    @Expose
    private Integer productPriceType;
    @SerializedName("channel_id")
    @Expose
    private Integer channelId;
    @SerializedName("website_id")
    @Expose
    private Integer websiteId;
    @SerializedName("currency_id")
    @Expose
    private Integer currencyId;
    @SerializedName("warehouse_id")
    @Expose
    private Integer warehouseId;
    @SerializedName("start_date")
    @Expose
    private String startDate;
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
    @SerializedName("price_type")
    @Expose
    private String priceType;

    public String getPriceType() {
        return priceType;
    }

    public void setPriceType(String priceType) {
        this.priceType = priceType;
    }

    public Object getEndDate() {
        return endDate;
    }

    public void setEndDate(Object endDate) {
        this.endDate = endDate;
    }

    public Double getCost() {
        return cost;
    }

    public void setCost(Double cost) {
        this.cost = cost;
    }

    public Object getMaxQuantity() {
        return maxQuantity;
    }

    public void setMaxQuantity(Object maxQuantity) {
        this.maxQuantity = maxQuantity;
    }

    public Double getMrp() {
        return mrp;
    }

    public void setMrp(Double mrp) {
        this.mrp = mrp;
    }

    public Object getPromotions() {
        return promotions;
    }

    public void setPromotions(Object promotions) {
        this.promotions = promotions;
    }

    public Object getMinQuantity() {
        return minQuantity;
    }

    public void setMinQuantity(Object minQuantity) {
        this.minQuantity = minQuantity;
    }

    public Double getPrice() {
        return price;
    }

    public void setPrice(Double price) {
        this.price = price;
    }

    public Integer getProductId() {
        return productId;
    }

    public void setProductId(Integer productId) {
        this.productId = productId;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getProductPriceType() {
        return productPriceType;
    }

    public void setProductPriceType(Integer productPriceType) {
        this.productPriceType = productPriceType;
    }

    public Integer getChannelId() {
        return channelId;
    }

    public void setChannelId(Integer channelId) {
        this.channelId = channelId;
    }

    public Integer getWebsiteId() {
        return websiteId;
    }

    public void setWebsiteId(Integer websiteId) {
        this.websiteId = websiteId;
    }

    public Integer getCurrencyId() {
        return currencyId;
    }

    public void setCurrencyId(Integer currencyId) {
        this.currencyId = currencyId;
    }

    public Integer getWarehouseId() {
        return warehouseId;
    }

    public void setWarehouseId(Integer warehouseId) {
        this.warehouseId = warehouseId;
    }

    public String getStartDate() {
        return startDate;
    }

    public void setStartDate(String startDate) {
        this.startDate = startDate;
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
}