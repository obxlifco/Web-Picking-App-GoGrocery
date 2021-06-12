package com.gogrocery.Models.CMS_Model;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class StockData {

@SerializedName("product_id")
@Expose
private Integer productId;
@SerializedName("real_stock")
@Expose
private Integer realStock;
@SerializedName("warehouse_id")
@Expose
private Integer warehouseId;

public Integer getProductId() {
return productId;
}

public void setProductId(Integer productId) {
this.productId = productId;
}

public Integer getRealStock() {
return realStock;
}

public void setRealStock(Integer realStock) {
this.realStock = realStock;
}

public Integer getWarehouseId() {
return warehouseId;
}

public void setWarehouseId(Integer warehouseId) {
this.warehouseId = warehouseId;
}

}