package com.gogrocery.Models.FilterModel;

import java.util.List;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class FilterModel {

    @SerializedName("field_name")
    @Expose
    private String fieldName;
    @SerializedName("child")
    @Expose
    private List<Child> child = null;



   // private boolean isSelected;

    public String getFieldName() {
        return fieldName;
    }

    public void setFieldName(String fieldName) {
        this.fieldName = fieldName;
    }

    public List<Child> getChild() {
        return child;
    }


    public void setChild(List<Child> child) {

        this.child = child;
    }


   /* public boolean isSelected() {
        return isSelected;
    }

    public void setSelected(boolean selected) {
        isSelected = selected;
    }*/

    public FilterModel(String fieldName,  List<Child> child) {
        this.fieldName = fieldName;
        this.child = child;
    }


}