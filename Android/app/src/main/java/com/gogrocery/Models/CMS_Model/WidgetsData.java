package com.gogrocery.Models.CMS_Model;


import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class WidgetsData {

@SerializedName("widgets_id")
@Expose
private Integer widgetsId;
@SerializedName("parent_category_list")
@Expose
private List<ParentCategoryList> parentCategoryList = null;
@SerializedName("best_sell_product")
@Expose
private List<BestSellProduct> bestSellProduct = null;
@SerializedName("properties")
@Expose
private List<Property> properties = null;

public Integer getWidgetsId() {
return widgetsId;
}

public void setWidgetsId(Integer widgetsId) {
this.widgetsId = widgetsId;
}

public List<ParentCategoryList> getParentCategoryList() {
return parentCategoryList;
}

public void setParentCategoryList(List<ParentCategoryList> parentCategoryList) {
this.parentCategoryList = parentCategoryList;
}

public List<BestSellProduct> getBestSellProduct() {
return bestSellProduct;
}

public void setBestSellProduct(List<BestSellProduct> bestSellProduct) {
this.bestSellProduct = bestSellProduct;
}

public List<Property> getProperties() {
return properties;
}

public void setProperties(List<Property> properties) {
this.properties = properties;
}

}