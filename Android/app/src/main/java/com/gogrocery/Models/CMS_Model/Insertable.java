package com.gogrocery.Models.CMS_Model;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Insertable {

@SerializedName("label")
@Expose
private String label;
@SerializedName("add_more")
@Expose
private Boolean addMore;
@SerializedName("maximum_item")
@Expose
private Integer maximumItem;
@SerializedName("default_object")
@Expose
private String defaultObject;
@SerializedName("properties")
@Expose
private List<Property_> properties = null;

public String getLabel() {
return label;
}

public void setLabel(String label) {
this.label = label;
}

public Boolean getAddMore() {
return addMore;
}

public void setAddMore(Boolean addMore) {
this.addMore = addMore;
}

public Integer getMaximumItem() {
return maximumItem;
}

public void setMaximumItem(Integer maximumItem) {
this.maximumItem = maximumItem;
}

public String getDefaultObject() {
return defaultObject;
}

public void setDefaultObject(String defaultObject) {
this.defaultObject = defaultObject;
}

public List<Property_> getProperties() {
return properties;
}

public void setProperties(List<Property_> properties) {
this.properties = properties;
}

}