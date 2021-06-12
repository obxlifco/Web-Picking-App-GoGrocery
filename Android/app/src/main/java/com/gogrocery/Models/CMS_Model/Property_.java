package com.gogrocery.Models.CMS_Model;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Property_ {

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
@SerializedName("type")
@Expose
private Integer type;
@SerializedName("image_size")
@Expose
private ImageSize imageSize;
@SerializedName("is_icon")
@Expose
private Boolean isIcon;
@SerializedName("associative_fields")
@Expose
private List<AssociativeField> associativeFields = null;

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

public Boolean getIsHint() {
return isHint;
}

public void setIsHint(Boolean isHint) {
this.isHint = isHint;
}

public String getHintText() {
return hintText;
}

public void setHintText(String hintText) {
this.hintText = hintText;
}

public Boolean getIsFile() {
return isFile;
}

public void setIsFile(Boolean isFile) {
this.isFile = isFile;
}

public Integer getType() {
return type;
}

public void setType(Integer type) {
this.type = type;
}

public ImageSize getImageSize() {
return imageSize;
}

public void setImageSize(ImageSize imageSize) {
this.imageSize = imageSize;
}

public Boolean getIsIcon() {
return isIcon;
}

public void setIsIcon(Boolean isIcon) {
this.isIcon = isIcon;
}

public List<AssociativeField> getAssociativeFields() {
return associativeFields;
}

public void setAssociativeFields(List<AssociativeField> associativeFields) {
this.associativeFields = associativeFields;
}

}