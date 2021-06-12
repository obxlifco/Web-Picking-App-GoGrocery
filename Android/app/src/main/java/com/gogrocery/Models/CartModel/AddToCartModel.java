package com.gogrocery.Models.CartModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class AddToCartModel {

@SerializedName("status")
@Expose
private Integer status;
@SerializedName("ack")
@Expose
private String ack;
@SerializedName("msg")
@Expose
private String msg;
@SerializedName("cart_data")
@Expose
private CartData cartData;

public Integer getStatus() {
return status;
}

public void setStatus(Integer status) {
this.status = status;
}

public String getAck() {
return ack;
}

public void setAck(String ack) {
this.ack = ack;
}

public String getMsg() {
return msg;
}

public void setMsg(String msg) {
this.msg = msg;
}

public CartData getCartData() {
return cartData;
}

public void setCartData(CartData cartData) {
this.cartData = cartData;
}

}