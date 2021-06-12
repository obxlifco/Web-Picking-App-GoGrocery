package com.gogrocery.Models.WishlistModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Data {

    @SerializedName("id")
    @Expose
    private Integer id;
    @SerializedName("product")
    @Expose
    private Product product;
    @SerializedName("user_id")
    @Expose
    private Integer userId;
    @SerializedName("website_id")
    @Expose
    private Integer websiteId;
    @SerializedName("name")
    @Expose
    private String name;
    @SerializedName("count")
    @Expose
    private Object count;
    @SerializedName("created")
    @Expose
    private String created;
    @SerializedName("modified")
    @Expose
    private String modified;
    @SerializedName("isblocked")
    @Expose
    private String isblocked;
    @SerializedName("isdeleted")
    @Expose
    private String isdeleted;
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
    @SerializedName("disc_type")
    @Expose
    private String discType;
    @SerializedName("coupon")
    @Expose
    private String coupon;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Product getProduct() {
        return product;
    }

    public void setProduct(Product product) {
        this.product = product;
    }

    public Integer getUserId() {
        return userId;
    }

    public void setUserId(Integer userId) {
        this.userId = userId;
    }

    public Integer getWebsiteId() {
        return websiteId;
    }

    public void setWebsiteId(Integer websiteId) {
        this.websiteId = websiteId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Object getCount() {
        return count;
    }

    public void setCount(Object count) {
        this.count = count;
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

    public String getIsblocked() {
        return isblocked;
    }

    public void setIsblocked(String isblocked) {
        this.isblocked = isblocked;
    }

    public String getIsdeleted() {
        return isdeleted;
    }

    public void setIsdeleted(String isdeleted) {
        this.isdeleted = isdeleted;
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
}