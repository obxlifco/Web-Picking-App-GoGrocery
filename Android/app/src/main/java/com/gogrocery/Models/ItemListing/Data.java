package com.gogrocery.Models.ItemListing;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Data {

@SerializedName("category_id")
@Expose
private String categoryId;
@SerializedName("product")
@Expose
private List<Product> product = null;

public String getCategoryId() {
return categoryId;
}

public void setCategoryId(String categoryId) {
this.categoryId = categoryId;
}

public List<Product> getProduct() {
return product;
}

public void setProduct(List<Product> product) {
this.product = product;
}

}