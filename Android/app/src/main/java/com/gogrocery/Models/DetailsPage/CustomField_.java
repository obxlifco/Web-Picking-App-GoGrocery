package com.gogrocery.Models.DetailsPage;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class CustomField_ {

@SerializedName("product_id")
@Expose
private Integer productId;
@SerializedName("field_name")
@Expose
private String fieldName;
@SerializedName("field_label")
@Expose
private String fieldLabel;
@SerializedName("value")
@Expose
private String value;
@SerializedName("is_variant")
@Expose
private String isVariant;

public Integer getProductId() {
return productId;
}

public void setProductId(Integer productId) {
this.productId = productId;
}

public String getFieldName() {
return fieldName;
}

public void setFieldName(String fieldName) {
this.fieldName = fieldName;
}

public String getFieldLabel() {
return fieldLabel;
}

public void setFieldLabel(String fieldLabel) {
this.fieldLabel = fieldLabel;
}

public String getValue() {
return value;
}

public void setValue(String value) {
this.value = value;
}

public String getIsVariant() {
return isVariant;
}

public void setIsVariant(String isVariant) {
this.isVariant = isVariant;
}

}