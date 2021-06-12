package com.gogrocery.Models.SaveListModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class SaveListData {

    @SerializedName("id")
    @Expose
    private String id;
    @SerializedName("website_id")
    @Expose
    private Integer websiteId;
    @SerializedName("company_id")
    @Expose
    private Integer companyId;
    @SerializedName("user_id")
    @Expose
    private Integer userId;
    @SerializedName("savelist_name")
    @Expose
    private String savelistName;
    @SerializedName("product_ids")
    @Expose
    private String productIds;
    @SerializedName("isdeleted")
    @Expose
    private String isdeleted;
    @SerializedName("created")
    @Expose
    private String created;
    @SerializedName("modified")
    @Expose
    private String modified;
    @SerializedName("count")
    @Expose
    private String count;
    @SerializedName("slug")
    @Expose
    private String slug;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Integer getWebsiteId() {
        return websiteId;
    }

    public void setWebsiteId(Integer websiteId) {
        this.websiteId = websiteId;
    }

    public Integer getCompanyId() {
        return companyId;
    }

    public void setCompanyId(Integer companyId) {
        this.companyId = companyId;
    }

    public Integer getUserId() {
        return userId;
    }

    public void setUserId(Integer userId) {
        this.userId = userId;
    }

    public String getSavelistName() {
        return savelistName;
    }

    public void setSavelistName(String savelistName) {
        this.savelistName = savelistName;
    }

    public String getProductIds() {
        return productIds;
    }

    public void setProductIds(String productIds) {
        this.productIds = productIds;
    }

    public String getIsdeleted() {
        return isdeleted;
    }

    public void setIsdeleted(String isdeleted) {
        this.isdeleted = isdeleted;
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

    public String getCount() {
        return count;
    }

    public void setCount(String count) {
        this.count = count;
    }

    public String getSlug() {
        return slug;
    }

    public void setSlug(String slug) {
        this.slug = slug;
    }
}