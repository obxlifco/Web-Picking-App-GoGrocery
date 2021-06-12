package com.gogrocery.Models.MenuCmsModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.List;

public class Insertable {

    @SerializedName("label")
    @Expose
    private String label;
    @SerializedName("properties")
    @Expose
    private List<Property> properties = null;

    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        this.label = label;
    }

    public List<Property> getProperties() {
        return properties;
    }

    public void setProperties(List<Property> properties) {
        this.properties = properties;
    }
}
