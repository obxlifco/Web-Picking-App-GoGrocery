package com.gogrocery.Models.ElasticSearch;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Variation {

@SerializedName("field_name")
@Expose
private String fieldName;

@SerializedName("field_id")
@Expose
private Integer fieldId;
@SerializedName("field_label")
@Expose
private String fieldLabel;
@SerializedName("is_parent")
@Expose
private String isParent;
@SerializedName("product_details")
@Expose
private ProductDetails productDetails;

public String getFieldName() {
return fieldName;
}

public void setFieldName(String fieldName) {
this.fieldName = fieldName;
}


public Integer getFieldId() {
return fieldId;
}

public void setFieldId(Integer fieldId) {
this.fieldId = fieldId;
}

public String getFieldLabel() {
return fieldLabel;
}

public void setFieldLabel(String fieldLabel) {
this.fieldLabel = fieldLabel;
}

public String getIsParent() {
return isParent;
}

public void setIsParent(String isParent) {
this.isParent = isParent;
}

public ProductDetails getProductDetails() {
return productDetails;
}

public void setProductDetails(ProductDetails productDetails) {
this.productDetails = productDetails;
}

}