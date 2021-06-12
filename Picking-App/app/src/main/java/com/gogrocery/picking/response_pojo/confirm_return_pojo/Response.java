package com.gogrocery.picking.response_pojo.confirm_return_pojo;

import com.google.gson.annotations.SerializedName;

public class Response{

	@SerializedName("current_return_amount")
	private double currentReturnAmount;

	@SerializedName("order_id")
	private int orderId;

	public void setCurrentReturnAmount(double currentReturnAmount){
		this.currentReturnAmount = currentReturnAmount;
	}

	public double getCurrentReturnAmount(){
		return currentReturnAmount;
	}

	public void setOrderId(int orderId){
		this.orderId = orderId;
	}

	public int getOrderId(){
		return orderId;
	}
}