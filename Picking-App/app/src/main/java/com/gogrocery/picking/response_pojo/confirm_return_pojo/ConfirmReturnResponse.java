package com.gogrocery.picking.response_pojo.confirm_return_pojo;

import com.google.gson.annotations.SerializedName;

public class ConfirmReturnResponse{

	@SerializedName("response")
	private Response response;

	@SerializedName("api_status")
	private String apiStatus;

	@SerializedName("message")
	private String message;

	@SerializedName("status")
	private int status;

	public void setResponse(Response response){
		this.response = response;
	}

	public Response getResponse(){
		return response;
	}

	public void setApiStatus(String apiStatus){
		this.apiStatus = apiStatus;
	}

	public String getApiStatus(){
		return apiStatus;
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
}