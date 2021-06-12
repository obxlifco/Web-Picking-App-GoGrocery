package com.gogrocery.Models.MenuCmsModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.List;

public class InnerCMSModel {
    @SerializedName("id")
    @Expose
    private Integer id;
    @SerializedName("is_distributor")
    @Expose
    private Integer isDistributor;
    @SerializedName("widget_category")
    @Expose
    private Integer widgetCategory;
    @SerializedName("label")
    @Expose
    private String label;
    @SerializedName("type")
    @Expose
    private Integer type;
    @SerializedName("favicon")
    @Expose
    private String favicon;
    @SerializedName("component")
    @Expose
    private String component;
    @SerializedName("insertables")
    @Expose
    private List<Insertable> insertables = null;
    @SerializedName("widget_id")
    @Expose
    private Integer widgetId;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getIsDistributor() {
        return isDistributor;
    }

    public void setIsDistributor(Integer isDistributor) {
        this.isDistributor = isDistributor;
    }

    public Integer getWidgetCategory() {
        return widgetCategory;
    }

    public void setWidgetCategory(Integer widgetCategory) {
        this.widgetCategory = widgetCategory;
    }

    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        this.label = label;
    }

    public Integer getType() {
        return type;
    }

    public void setType(Integer type) {
        this.type = type;
    }

    public String getFavicon() {
        return favicon;
    }

    public void setFavicon(String favicon) {
        this.favicon = favicon;
    }

    public String getComponent() {
        return component;
    }

    public void setComponent(String component) {
        this.component = component;
    }

    public List<Insertable> getInsertables() {
        return insertables;
    }

    public void setInsertables(List<Insertable> insertables) {
        this.insertables = insertables;
    }

    public Integer getWidgetId() {
        return widgetId;
    }

    public void setWidgetId(Integer widgetId) {
        this.widgetId = widgetId;
    }
}
