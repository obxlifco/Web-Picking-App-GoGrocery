package com.gogrocery.picking.response_pojo.forgot_pwd_pojo;

import javax.annotation.Generated;
import com.google.gson.annotations.SerializedName;

@Generated("com.robohorse.robopojogenerator")
public class ForgotPwdResponse{

	@SerializedName("name")
	private String name;

	@SerializedName("api_status")
	private String apiStatus;

	@SerializedName("message")
	private String message;

	@SerializedName("status")
	private int status;

	public void setName(String name){
		this.name = name;
	}

	public String getName(){
		return name;
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
			"ForgotPwdResponse{" + 
			"name = '" + name + '\'' + 
			",api_status = '" + apiStatus + '\'' + 
			",message = '" + message + '\'' + 
			",status = '" + status + '\'' + 
			"}";
		}
}