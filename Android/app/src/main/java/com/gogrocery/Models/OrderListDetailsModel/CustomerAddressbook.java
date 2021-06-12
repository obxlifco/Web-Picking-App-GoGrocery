package com.gogrocery.Models.OrderListDetailsModel;

import com.google.gson.annotations.SerializedName;

public class CustomerAddressbook{

	@SerializedName("lat_val")
	private String latVal;

	@SerializedName("long_val")
	private String longVal;

	public String getLatVal(){
		return latVal;
	}

	public String getLongVal(){
		return longVal;
	}
}