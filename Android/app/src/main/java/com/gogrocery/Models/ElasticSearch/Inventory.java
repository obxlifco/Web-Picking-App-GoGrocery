package com.gogrocery.Models.ElasticSearch;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Inventory {

@SerializedName("warehouse_id")
@Expose
private Integer warehouseId;
@SerializedName("name")
@Expose
private String name;
@SerializedName("code")
@Expose
private String code;
@SerializedName("stock")
@Expose
private Integer stock;

public Integer getWarehouseId() {
return warehouseId;
}

public void setWarehouseId(Integer warehouseId) {
this.warehouseId = warehouseId;
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