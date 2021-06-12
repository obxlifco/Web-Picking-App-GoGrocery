package com.gogrocery.Models.MenuCmsModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Property {
    @SerializedName("label")
    @Expose
    private String label;
    @SerializedName("selector")
    @Expose
    private String selector;
    @SerializedName("value")
    @Expose
    private String value;
    @SerializedName("is_hint")
    @Expose
    private Boolean isHint;
    @SerializedName("hint_text")
    @Expose
    private String hintText;
    @SerializedName("is_file")
    @Expose
    private Boolean isFile;

    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        this.label = label;
    }

    public String getSelector() {
        return selector;
    }

    public void setSelector(String selector) {
        this.selector = selector;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }

    public Boolean getHint() {
        return isHint;
    }

    public void setHint(Boolean hint) {
        isHint = hint;
    }

    public String getHintText() {
        return hintText;
    }

    public void setHintText(String hintText) {
        this.hintText = hintText;
    }

    public Boolean getFile() {
        return isFile;
    }

    public void setFile(Boolean file) {
        isFile = file;
    }
}
