package com.gogrocery.picking.response_pojo.generate_picklist_pojo;

import javax.annotation.Generated;
import com.google.gson.annotations.SerializedName;

@Generated("com.robohorse.robopojogenerator")
public class GeneratePicklistResponse{

	@SerializedName("picklist_id")
	private int picklistId;

	@SerializedName("api_status")
	private String apiStatus;

	@SerializedName("shipment_id")
	private int shipmentId;

	@SerializedName("message")
	private String message;

	@SerializedName("status")
	private int status;

	public void setPicklistId(int picklistId){
		this.picklistId = picklistId;
	}

	public int getPicklistId(){
		return picklistId;
	}

	public void setApiStatus(String apiStatus){
		this.apiStatus = apiStatus;
	}

	public String getApiStatus(){
		return apiStatus;
	}

	public void setShipmentId(int shipmentId){
		this.shipmentId = shipmentId;
	}

	public int getShipmentId(){
		return shipmentId;
	}

	public void setMessage(String message){
		this.message = message;
	}

	public String getMessage(){
		return message;
	}

	public void setStatus(int status){
		this.status = status;
	}

	public int getStatus(){
		return status;
	}

	@Override
 	public String toString(){
		return 
			"GeneratePicklistResponse{" + 
			"picklist_id = '" + picklistId + '\'' + 
			",api_status = '" + apiStatus + '\'' + 
			",shipment_id = '" + shipmentId + '\'' + 
			",message = '" + message + '\'' + 
			",status = '" + status + '\'' + 
			"}";
		}
}