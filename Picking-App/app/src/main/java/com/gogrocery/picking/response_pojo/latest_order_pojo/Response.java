package com.gogrocery.picking.response_pojo.latest_order_pojo;

import com.google.gson.annotations.SerializedName;

public class Response{

	@SerializedName("no_of_latest_order")
	private int noOfLatestOrder;

	@SerializedName("last_order")
	private int lastOrder;

	@SerializedName("substitute_in")
	private int substitute_in;

	@SerializedName("substitute_out")
	private int substitute_out;

	public void setNoOfLatestOrder(int noOfLatestOrder){
		this.noOfLatestOrder = noOfLatestOrder;
	}

	public int getNoOfLatestOrder(){
		return noOfLatestOrder;
	}

	public void setLastOrder(int lastOrder){
		this.lastOrder = lastOrder;
	}

	public int getLastOrder(){
		return lastOrder;
	}

	public int getSubstitute_in() {
		return substitute_in;
	}

	public void setSubstitute_in(int substitute_in) {
		this.substitute_in = substitute_in;
	}

	public int getSubstitute_out() {
		return substitute_out;
	}

	public void setSubstitute_out(int substitute_out) {
		this.substitute_out = substitute_out;
	}
}