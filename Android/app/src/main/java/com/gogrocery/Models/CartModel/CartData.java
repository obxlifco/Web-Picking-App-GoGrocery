package com.gogrocery.Models.CartModel;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class CartData {

@SerializedName("cartdetails")
@Expose
private List<Cartdetail> cartdetails = null;
@SerializedName("orderamountdetails")
@Expose
private List<Orderamountdetail> orderamountdetails = null;

    @SerializedName("cart_count")
    @Expose
    private String cart_count;

/*
@SerializedName("applied_coupon")
@Expose
private List<Object> appliedCoupon = null;
@SerializedName("shipping_flat")
@Expose
private ShippingFlat shippingFlat;
@SerializedName("shipping_table")
@Expose
private ShippingTable shippingTable;
*/

public List<Cartdetail> getCartdetails() {
return cartdetails;
}

public void setCartdetails(List<Cartdetail> cartdetails) {
this.cartdetails = cartdetails;
}

public List<Orderamountdetail> getOrderamountdetails() {
return orderamountdetails;
}

public void setOrderamountdetails(List<Orderamountdetail> orderamountdetails) {
this.orderamountdetails = orderamountdetails;
}

/*
public List<Object> getAppliedCoupon() {
return appliedCoupon;
}

public void setAppliedCoupon(List<Object> appliedCoupon) {
this.appliedCoupon = appliedCoupon;
}

public ShippingFlat getShippingFlat() {
return shippingFlat;
}

public void setShippingFlat(ShippingFlat shippingFlat) {
this.shippingFlat = shippingFlat;
}

public ShippingTable getShippingTable() {
return shippingTable;
}

public void setShippingTable(ShippingTable shippingTable) {
this.shippingTable = shippingTable;
}
*/

    public String getCart_count() {
        return cart_count;
    }

    public void setCart_count(String cart_count) {
        this.cart_count = cart_count;
    }
}