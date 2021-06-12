package com.gogrocery.Models.BestSellingProductModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class StockDetail {
    @SerializedName("product_id")
    @Expose
    private Integer productId;
    @SerializedName("real_stock")
    @Expose
    private String realStock;
    @SerializedName("warehouse_id")
    @Expose
    private String warehouseId;

    public Integer getProductId() {
        return productId;
    }

    public void setProductId(Integer productId) {
        this.productId = productId;
    }

    public String getRealStock() {
        return realStock;
    }

    public void setRealStock(String realStock) {
        this.realStock = realStock;
    }

    public String getWarehouseId() {
        return warehouseId;
    }

    public void setWarehouseId(String warehouseId) {
        this.warehouseId = warehouseId;
    }
}
