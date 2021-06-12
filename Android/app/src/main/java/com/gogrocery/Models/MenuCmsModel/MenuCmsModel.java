package com.gogrocery.Models.MenuCmsModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.List;

public class MenuCmsModel {
    @SerializedName("status")
    @Expose
    private Integer status;
    @SerializedName("page_id")
    @Expose
    private Integer pageId;
    @SerializedName("page_title")
    @Expose
    private String pageTitle;
    @SerializedName("page_meta_keywords")
    @Expose
    private String pageMetaKeywords;
    @SerializedName("page_meta_description")
    @Expose
    private String pageMetaDescription;
    @SerializedName("page_meta_data")
    @Expose
    private String pageMetaData;
    @SerializedName("cms_widgets")
    @Expose
    private List<CmsWidget> cmsWidgets = null;
    @SerializedName("funnel_data")
    @Expose
    private List<Object> funnelData = null;

    public Integer getStatus() {
        return status;
    }

    public void setStatus(Integer status) {
        this.status = status;
    }

    public Integer getPageId() {
        return pageId;
    }

    public void setPageId(Integer pageId) {
        this.pageId = pageId;
    }

    public String getPageTitle() {
        return pageTitle;
    }

    public void setPageTitle(String pageTitle) {
        this.pageTitle = pageTitle;
    }

    public String getPageMetaKeywords() {
        return pageMetaKeywords;
    }

    public void setPageMetaKeywords(String pageMetaKeywords) {
        this.pageMetaKeywords = pageMetaKeywords;
    }

    public String getPageMetaDescription() {
        return pageMetaDescription;
    }

    public void setPageMetaDescription(String pageMetaDescription) {
        this.pageMetaDescription = pageMetaDescription;
    }

    public String getPageMetaData() {
        return pageMetaData;
    }

    public void setPageMetaData(String pageMetaData) {
        this.pageMetaData = pageMetaData;
    }

    public List<CmsWidget> getCmsWidgets() {
        return cmsWidgets;
    }

    public void setCmsWidgets(List<CmsWidget> cmsWidgets) {
        this.cmsWidgets = cmsWidgets;
    }

    public List<Object> getFunnelData() {
        return funnelData;
    }

    public void setFunnelData(List<Object> funnelData) {
        this.funnelData = funnelData;
    }
}
