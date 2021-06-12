package com.gogrocery.picking.response_pojo.search_return_pojo;

import javax.annotation.Generated;
import com.google.gson.annotations.SerializedName;

@Generated("com.robohorse.robopojogenerator")
public class CustomerAddressbook{

	@SerializedName("lat_val")
	private String latVal;

	@SerializedName("long_val")
	private String longVal;

	public void setLatVal(String latVal){
		this.latVal = latVal;
	}

	public String getLatVal(){
		return latVal;
	}

	public void setLongVal(String longVal){
		this.longVal = longVal;
	}

	public String getLongVal(){
		return longVal;
	}

	@Override
 	public String toString(){
		return 
			"CustomerAddressbook{" + 
			"lat_val = '" + latVal + '\'' + 
			",long_val = '" + longVal + '\'' + 
			"}";
		}
}