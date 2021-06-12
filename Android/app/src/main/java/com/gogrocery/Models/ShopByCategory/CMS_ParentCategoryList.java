package com.gogrocery.Models.ShopByCategory;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class CMS_ParentCategoryList {

    @SerializedName("id")
    @Expose
    private Integer id;
    @SerializedName("parent_id")
    @Expose
    private Integer parentId;
    @SerializedName("display_order")
    @Expose
    private Integer displayOrder;
    @SerializedName("name")
    @Expose
    private String name;
    @SerializedName("description")
    @Expose
    private String description;
    @SerializedName("image")
    @Expose
    private String image;
    @SerializedName("thumb_image")
    @Expose
    private String thumbImage;
    @SerializedName("banner_image")
    @Expose
    private String bannerImage;
    @SerializedName("page_title")
    @Expose
    private String pageTitle;
    @SerializedName("meta_description")
    @Expose
    private Object metaDescription;
    @SerializedName("meta_keywords")
    @Expose
    private Object metaKeywords;
    @SerializedName("category_url")
    @Expose
    private String categoryUrl;
    @SerializedName("slug")
    @Expose
    private String slug;
    @SerializedName("type")
    @Expose
    private Object type;
    @SerializedName("is_ebay_store_category")
    @Expose
    private String isEbayStoreCategory;
    @SerializedName("customer_group_id")
    @Expose
    private Object customerGroupId;
    @SerializedName("display_mobile_app")
    @Expose
    private String displayMobileApp;
    @SerializedName("applicable_imei")
    @Expose
    private String applicableImei;
    @SerializedName("isadded_in_tally")
    @Expose
    private String isaddedInTally;

    public CMS_ParentCategoryList( String name) {

        this.name = name;

    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getParentId() {
        return parentId;
    }

    public void setParentId(Integer parentId) {
        this.parentId = parentId;
    }

    public Integer getDisplayOrder() {
        return displayOrder;
    }

    public void setDisplayOrder(Integer displayOrder) {
        this.displayOrder = displayOrder;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getImage() {
        return image;
    }

    public void setImage(String image) {
        this.image = image;
    }

    public String getThumbImage() {
        return thumbImage;
    }

    public void setThumbImage(String thumbImage) {
        this.thumbImage = thumbImage;
    }

    public String getBannerImage() {
        return bannerImage;
    }

    public void setBannerImage(String bannerImage) {
        this.bannerImage = bannerImage;
    }

    public String getPageTitle() {
        return pageTitle;
    }

    public void setPageTitle(String pageTitle) {
        this.pageTitle = pageTitle;
    }

    public Object getMetaDescription() {
        return metaDescription;
    }

    public void setMetaDescription(Object metaDescription) {
        this.metaDescription = metaDescription;
    }

    public Object getMetaKeywords() {
        return metaKeywords;
    }

    public void setMetaKeywords(Object metaKeywords) {
        this.metaKeywords = metaKeywords;
    }

    public String getCategoryUrl() {
        return categoryUrl;
    }

    public void setCategoryUrl(String categoryUrl) {
        this.categoryUrl = categoryUrl;
    }

    public String getSlug() {
        return slug;
    }

    public void setSlug(String slug) {
        this.slug = slug;
    }

    public Object getType() {
        return type;
    }

    public void setType(Object type) {
        this.type = type;
    }

    public String getIsEbayStoreCategory() {
        return isEbayStoreCategory;
    }

    public void setIsEbayStoreCategory(String isEbayStoreCategory) {
        this.isEbayStoreCategory = isEbayStoreCategory;
    }

    public Object getCustomerGroupId() {
        return customerGroupId;
    }

    public void setCustomerGroupId(Object customerGroupId) {
        this.customerGroupId = customerGroupId;
    }

    public String getDisplayMobileApp() {
        return displayMobileApp;
    }

    public void setDisplayMobileApp(String displayMobileApp) {
        this.displayMobileApp = displayMobileApp;
    }

    public String getApplicableImei() {
        return applicableImei;
    }

    public void setApplicableImei(String applicableImei) {
        this.applicableImei = applicableImei;
    }

    public String getIsaddedInTally() {
        return isaddedInTally;
    }

    public void setIsaddedInTally(String isaddedInTally) {
        this.isaddedInTally = isaddedInTally;
    }

}