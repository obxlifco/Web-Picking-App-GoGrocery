package com.gogrocery.Models.MenuCmsModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class CmsWidget {
    @SerializedName("id")
    @Expose
    private Integer id;
    @SerializedName("company_website_id")
    @Expose
    private Integer companyWebsiteId;
    @SerializedName("temp_id")
    @Expose
    private Integer tempId;
    @SerializedName("page_id")
    @Expose
    private Integer pageId;
    @SerializedName("widgets")
    @Expose
    private Integer widgets;
    @SerializedName("property_value")
    @Expose
    private String propertyValue;
    @SerializedName("created")
    @Expose
    private String created;
    @SerializedName("modified")
    @Expose
    private String modified;
    @SerializedName("createdby")
    @Expose
    private Integer createdby;
    @SerializedName("updatedby")
    @Expose
    private Integer updatedby;
    @SerializedName("lang")
    @Expose
    private String lang;
    @SerializedName("ip_address")
    @Expose
    private String ipAddress;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getCompanyWebsiteId() {
        return companyWebsiteId;
    }

    public void setCompanyWebsiteId(Integer companyWebsiteId) {
        this.companyWebsiteId = companyWebsiteId;
    }

    public Integer getTempId() {
        return tempId;
    }

    public void setTempId(Integer tempId) {
        this.tempId = tempId;
    }

    public Integer getPageId() {
        return pageId;
    }

    public void setPageId(Integer pageId) {
        this.pageId = pageId;
    }

    public Integer getWidgets() {
        return widgets;
    }

    public void setWidgets(Integer widgets) {
        this.widgets = widgets;
    }

    public String getPropertyValue() {
        return propertyValue;
    }

    public void setPropertyValue(String propertyValue) {
        this.propertyValue = propertyValue;
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

    public Integer getCreatedby() {
        return createdby;
    }

    public void setCreatedby(Integer createdby) {
        this.createdby = createdby;
    }

    public Integer getUpdatedby() {
        return updatedby;
    }

    public void setUpdatedby(Integer updatedby) {
        this.updatedby = updatedby;
    }

    public String getLang() {
        return lang;
    }

    public void setLang(String lang) {
        this.lang = lang;
    }

    public String getIpAddress() {
        return ipAddress;
    }

    public void setIpAddress(String ipAddress) {
        this.ipAddress = ipAddress;
    }
}
