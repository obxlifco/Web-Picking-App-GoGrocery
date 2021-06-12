package com.gogrocery.Models.CartSummaryModel;

import java.util.List;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Data {

    @SerializedName("cartdetails")
    @Expose
    private List<Cartdetail> cartdetails = null;
    @SerializedName("orderamountdetails")
    @Expose
    private List<Orderamountdetail> orderamountdetails = null;
    /*@SerializedName("applied_coupon")
    @Expose
    private List<Object> appliedCoupon = null;
    @SerializedName("shipping_flat")
    @Expose
    private ShippingFlat shippingFlat;
    @SerializedName("shipping_table")
    @Expose
    private ShippingTable shippingTable;
    @SerializedName("cart_count")
    @Expose
    private String cartCount;*/
    @SerializedName("loyalty_details")
    @Expose
    private LoyaltyDetails loyaltyDetails;


    public List<Orderamountdetail> getOrderamountdetails() {
        return orderamountdetails;
    }

    public void setOrderamountdetails(List<Orderamountdetail> orderamountdetails) {
        this.orderamountdetails = orderamountdetails;
    }

    public LoyaltyDetails getLoyaltyDetails() {
        return loyaltyDetails;
    }

    public void setLoyaltyDetails(LoyaltyDetails loyaltyDetails) {
        this.loyaltyDetails = loyaltyDetails;
    }

    public List<Cartdetail> getCartdetails() {
        return cartdetails;
    }

    public void setCartdetails(List<Cartdetail> cartdetails) {
        this.cartdetails = cartdetails;
    }
}