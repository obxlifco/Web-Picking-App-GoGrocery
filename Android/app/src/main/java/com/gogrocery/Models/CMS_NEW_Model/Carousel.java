package com.gogrocery.Models.CMS_NEW_Model;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Carousel {

    @SerializedName("id")
    @Expose
    private Integer id;
    @SerializedName("primary_image_name")
    @Expose
    private String primaryImageName;
    @SerializedName("applicable_for")
    @Expose
    private String applicableFor;
    @SerializedName("banner_link_to")
    @Expose
    private String bannerLinkTo;
    @SerializedName("link")
    @Expose
    private String link;
    @SerializedName("promotion_id")
    @Expose
    private Object promotionId;
    @SerializedName("product_id")
    @Expose
    private Object productId;
    @SerializedName("category_id")
    @Expose
    private Object categoryId;
    @SerializedName("start_date")
    @Expose
    private String startDate;
    @SerializedName("end_date")
    @Expose
    private String endDate;
    @SerializedName("order_no")
    @Expose
    private Object orderNo;
    @SerializedName("banner_caption1")
    @Expose
    private Object bannerCaption1;
    @SerializedName("banner_caption2")
    @Expose
    private Object bannerCaption2;
    @SerializedName("is_notification_enabled_val")
    @Expose
    private String isNotificationEnabledVal;
    @SerializedName("notification_msg")
    @Expose
    private Object notificationMsg;
    @SerializedName("created")
    @Expose
    private String created;
    @SerializedName("modified")
    @Expose
    private String modified;
    @SerializedName("isdeleted")
    @Expose
    private String isdeleted;
    @SerializedName("isblocked")
    @Expose
    private String isblocked;
    @SerializedName("category_banner")
    @Expose
    private Integer categoryBanner;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getPrimaryImageName() {
        return primaryImageName;
    }

    public void setPrimaryImageName(String primaryImageName) {
        this.primaryImageName = primaryImageName;
    }

    public String getApplicableFor() {
        return applicableFor;
    }

    public void setApplicableFor(String applicableFor) {
        this.applicableFor = applicableFor;
    }

    public String getBannerLinkTo() {
        return bannerLinkTo;
    }

    public void setBannerLinkTo(String bannerLinkTo) {
        this.bannerLinkTo = bannerLinkTo;
    }

    public String getLink() {
        return link;
    }

    public void setLink(String link) {
        this.link = link;
    }

    public Object getPromotionId() {
        return promotionId;
    }

    public void setPromotionId(Object promotionId) {
        this.promotionId = promotionId;
    }

    public Object getProductId() {
        return productId;
    }

    public void setProductId(Object productId) {
        this.productId = productId;
    }

    public Object getCategoryId() {
        return categoryId;
    }

    public void setCategoryId(Object categoryId) {
        this.categoryId = categoryId;
    }

    public String getStartDate() {
        return startDate;
    }

    public void setStartDate(String startDate) {
        this.startDate = startDate;
    }

    public String getEndDate() {
        return endDate;
    }

    public void setEndDate(String endDate) {
        this.endDate = endDate;
    }

    public Object getOrderNo() {
        return orderNo;
    }

    public void setOrderNo(Object orderNo) {
        this.orderNo = orderNo;
    }

    public Object getBannerCaption1() {
        return bannerCaption1;
    }

    public void setBannerCaption1(Object bannerCaption1) {
        this.bannerCaption1 = bannerCaption1;
    }

    public Object getBannerCaption2() {
        return bannerCaption2;
    }

    public void setBannerCaption2(Object bannerCaption2) {
        this.bannerCaption2 = bannerCaption2;
    }

    public String getIsNotificationEnabledVal() {
        return isNotificationEnabledVal;
    }

    public void setIsNotificationEnabledVal(String isNotificationEnabledVal) {
        this.isNotificationEnabledVal = isNotificationEnabledVal;
    }

    public Object getNotificationMsg() {
        return notificationMsg;
    }

    public void setNotificationMsg(Object notificationMsg) {
        this.notificationMsg = notificationMsg;
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

    public String getIsdeleted() {
        return isdeleted;
    }

    public void setIsdeleted(String isdeleted) {
        this.isdeleted = isdeleted;
    }

    public String getIsblocked() {
        return isblocked;
    }

    public void setIsblocked(String isblocked) {
        this.isblocked = isblocked;
    }

    public Integer getCategoryBanner() {
        return categoryBanner;
    }

    public void setCategoryBanner(Integer categoryBanner) {
        this.categoryBanner = categoryBanner;
    }


}