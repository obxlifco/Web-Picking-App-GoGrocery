package com.gogrocery.picking.response_pojo.order_detail_csv_pojo;

import com.google.gson.annotations.SerializedName;

public class OrderDetailCSVResponse{

	@SerializedName("file_name")
	private String file_name;

	@SerializedName("export_file_path")
	private String exportFilePath;

	@SerializedName("api_status")
	private String apiStatus;

	@SerializedName("message")
	private String message;

	@SerializedName("status")
	private int status;

	public void setResponse(String response){
		this.file_name = response;
	}

	public String getResponse(){
		return file_name;
	}

	public void setExportFilePath(String exportFilePath){
		this.exportFilePath = exportFilePath;
	}

	public String getExportFilePath(){
		return exportFilePath;
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