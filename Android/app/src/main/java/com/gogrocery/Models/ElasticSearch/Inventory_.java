package com.gogrocery.Models.ElasticSearch;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Inventory_ {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("name")
@Expose
private String name;
@SerializedName("code")
@Expose
private String code;
@SerializedName("stock")
@Expose
private Integer stock;

public Integer getId() {
return id;
}

public void setId(Integer id) {
this.id = id;
}

public String getName() {
return name;
}

public void setName(String name) {
this.name = name;
}

public String getCode() {
return code;
}

public void setCode(String code) {
this.code = code;
}

public Integer getStock() {
return stock;
}

public void setStock(Integer stock) {
this.stock = stock;
}

}