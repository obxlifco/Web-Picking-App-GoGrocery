package com.gogrocery.Models;

public class ProductQuantityLocal {

    private String productId;
    private String productQty;

    public ProductQuantityLocal() {
    }

    public ProductQuantityLocal(String productId, String productQty) {
        this.productId = productId;
        this.productQty = productQty;
    }

    public String getProductId() {
        return productId;
    }

    public void setProductId(String productId) {
        this.productId = productId;
    }

    public String getProductQty() {
        return productQty;
    }

    public void setProductQty(String productQty) {
        this.productQty = productQty;
    }
}
