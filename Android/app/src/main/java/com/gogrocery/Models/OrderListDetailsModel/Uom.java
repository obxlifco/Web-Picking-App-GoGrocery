package com.gogrocery.Models.OrderListDetailsModel;

import com.google.gson.annotations.SerializedName;

public class Uom{

	@SerializedName("uom_name")
	private String uomName;

	@SerializedName("uom_full_name")
	private String uomFullName;

	public String getUomName(){
		return uomName;
	}

	public String getUomFullName(){
		return uomFullName;
	}
}