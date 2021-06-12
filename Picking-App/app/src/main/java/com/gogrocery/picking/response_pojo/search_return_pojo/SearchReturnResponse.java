package com.gogrocery.picking.response_pojo.search_return_pojo;

import java.util.List;
import javax.annotation.Generated;
import com.google.gson.annotations.SerializedName;

@Generated("com.robohorse.robopojogenerator")
public class SearchReturnResponse{

	@SerializedName("response")
	private List<SearchReturnItem> response;

	@SerializedName("api_status")
	private String apiStatus;

	@SerializedName("message")
	private String message;

	@SerializedName("status")
	private int status;

	public void setResponse(List<SearchReturnItem> response){
		this.response = response;
	}

	public List<SearchReturnItem> getResponse(){
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

	@Override
 	public String toString(){
		return 
			"SearchReturnResponse{" + 
			"response = '" + response + '\'' + 
			",api_status = '" + apiStatus + '\'' + 
			",message = '" + message + '\'' + 
			",status = '" + status + '\'' + 
			"}";
		}
}