package com.gogrocery.Models.OrderListDetailsModel;

import java.util.List;
import com.google.gson.annotations.SerializedName;

public class OrderListDetailsModel{

	@SerializedName("response")
	private List<ResponseItem> response;

	@SerializedName("api_status")
	private String apiStatus;

	@SerializedName("message")
	private String message;

	@SerializedName("status")
	private int status;

	public List<ResponseItem> getResponse(){
		return response;
	}

	public String getApiStatus(){
		return apiStatus;
	}

	public String getMessage(){
		return message;
	}

	public int getStatus(){
		return status;
	}
}