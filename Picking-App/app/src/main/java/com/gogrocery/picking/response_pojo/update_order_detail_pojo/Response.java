package com.gogrocery.picking.response_pojo.update_order_detail_pojo;

import com.google.gson.annotations.SerializedName;

public class Response{

	@SerializedName("old_order_amount")
	private double oldOrderAmount;

	@SerializedName("order_amount")
	private double orderAmount;

	@SerializedName("order_net_amount")
	private double orderNetAmount;

	public void setOldOrderAmount(double oldOrderAmount){
		this.oldOrderAmount = oldOrderAmount;
	}

	public double getOldOrderAmount(){
		return oldOrderAmount;
	}

	public void setOrderAmount(double orderAmount){
		this.orderAmount = orderAmount;
	}

	public double getOrderAmount(){
		return orderAmount;
	}

	public void setOrderNetAmount(double orderNetAmount){
		this.orderNetAmount = orderNetAmount;
	}

	public double getOrderNetAmount(){
		return orderNetAmount;
	}
}