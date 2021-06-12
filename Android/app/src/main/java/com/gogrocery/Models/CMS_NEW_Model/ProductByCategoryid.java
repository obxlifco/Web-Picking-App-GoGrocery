package com.gogrocery.Models.CMS_NEW_Model;

import java.util.List;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class ProductByCategoryid {

    @SerializedName("category_id")
    @Expose
    private Integer categoryId;
    @SerializedName("product")
    @Expose
    private List<Product> product = null;

    @SerializedName("label_value")
    @Expose
    private String label_value = null;


    public Integer getCategoryId() {
        return categoryId;
    }

    public void setCategoryId(Integer categoryId) {
        this.categoryId = categoryId;
    }

    public List<Product> getProduct() {
        return product;
    }

    public void setProduct(List<Product> product) {
        this.product = product;
    }

    public String getLabel_value() {
        return label_value;
    }

    public void setLabel_value(String label_value) {
        this.label_value = label_value;
    }
}