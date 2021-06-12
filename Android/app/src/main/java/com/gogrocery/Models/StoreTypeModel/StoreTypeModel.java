package com.gogrocery.Models.StoreTypeModel;

import java.util.List;
import com.google.gson.annotations.SerializedName;

public class StoreTypeModel{

	@SerializedName("data")
	private List<DataItem> data;

	@SerializedName("Message")
	private String message;

	@SerializedName("api_status")
	private String apiStatus;

	@SerializedName("status")
	private int status;

	public void setData(List<DataItem> data){
		this.data = data;
	}

	public List<DataItem> getData(){
		return data;
	}

	public void setMessage(String message){
		this.message = message;
	}

	public String getMessage(){
		return message;
	}

	public void setApiStatus(String apiStatus){
		this.apiStatus = apiStatus;
	}

	public String getApiStatus(){
		return apiStatus;
	}

	public void setStatus(int status){
		this.status = status;
	}

	public int getStatus(){
		return status;
	}
}