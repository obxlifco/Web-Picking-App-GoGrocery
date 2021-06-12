package com.gogrocery.picking.response_pojo.grn_update_pojo;

import javax.annotation.Generated;
import com.google.gson.annotations.SerializedName;

@Generated("com.robohorse.robopojogenerator")
public class Response{

	@SerializedName("shortage")
	private int shortage;

	@SerializedName("grn_quantity")
	private int grnQuantity;

	@SerializedName("order_details")
	private OrderDetails orderDetails;

	public void setShortage(int shortage){
		this.shortage = shortage;
	}

	public int getShortage(){
		return shortage;
	}

	public void setGrnQuantity(int grnQuantity){
		this.grnQuantity = grnQuantity;
	}

	public int getGrnQuantity(){
		return grnQuantity;
	}

	public void setOrderDetails(OrderDetails orderDetails){
		this.orderDetails = orderDetails;
	}

	public OrderDetails getOrderDetails(){
		return orderDetails;
	}

	@Override
 	public String toString(){
		return 
			"Response{" + 
			"shortage = '" + shortage + '\'' + 
			",grn_quantity = '" + grnQuantity + '\'' + 
			",order_details = '" + orderDetails + '\'' + 
			"}";
		}
}