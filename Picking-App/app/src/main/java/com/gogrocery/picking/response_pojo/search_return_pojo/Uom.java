package com.gogrocery.picking.response_pojo.search_return_pojo;

import javax.annotation.Generated;
import com.google.gson.annotations.SerializedName;

@Generated("com.robohorse.robopojogenerator")
public class Uom{

	@SerializedName("uom_name")
	private String uomName;

	@SerializedName("uom_full_name")
	private String uomFullName;

	public void setUomName(String uomName){
		this.uomName = uomName;
	}

	public String getUomName(){
		return uomName;
	}

	public void setUomFullName(String uomFullName){
		this.uomFullName = uomFullName;
	}

	public String getUomFullName(){
		return uomFullName;
	}

	@Override
 	public String toString(){
		return 
			"Uom{" + 
			"uom_name = '" + uomName + '\'' + 
			",uom_full_name = '" + uomFullName + '\'' + 
			"}";
		}
}