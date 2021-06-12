package com.gogrocery.picking.response_pojo.product_list_pojo;

import java.util.List;
import javax.annotation.Generated;
import com.google.gson.annotations.SerializedName;

@Generated("com.robohorse.robopojogenerator")
public class ProductListResponse{

	@SerializedName("next_page")
	private int nextPage;

	@SerializedName("per_page")
	private int perPage;

	@SerializedName("response")
	private List<ProductListItem> response;

	@SerializedName("total_page")
	private int totalPage;

	@SerializedName("api_status")
	private String apiStatus;

	@SerializedName("current_page")
	private int currentPage;

	@SerializedName("status")
	private int status;

	@SerializedName("total_order")
	private int totalOrder;

	@SerializedName("message")
	private String message;

	public void setNextPage(int nextPage){
		this.nextPage = nextPage;
	}

	public int getNextPage(){
		return nextPage;
	}

	public void setPerPage(int perPage){
		this.perPage = perPage;
	}

	public int getPerPage(){
		return perPage;
	}

	public void setResponse(List<ProductListItem> response){
		this.response = response;
	}

	public List<ProductListItem> getResponse(){
		return response;
	}

	public void setTotalPage(int totalPage){
		this.totalPage = totalPage;
	}

	public int getTotalPage(){
		return totalPage;
	}

	public void setApiStatus(String apiStatus){
		this.apiStatus = apiStatus;
	}

	public String getApiStatus(){
		return apiStatus;
	}

	public void setCurrentPage(int currentPage){
		this.currentPage = currentPage;
	}

	public int getCurrentPage(){
		return currentPage;
	}

	public void setStatus(int status){
		this.status = status;
	}

	public int getStatus(){
		return status;
	}

	public void setTotalOrder(int totalOrder){
		this.totalOrder = totalOrder;
	}

	public int getTotalOrder(){
		return totalOrder;
	}

	public String getMessage() {
		return message;
	}

	public void setMessage(String message) {
		this.message = message;
	}

	@Override
 	public String toString(){
		return 
			"ProductListResponse{" + 
			"next_page = '" + nextPage + '\'' + 
			",per_page = '" + perPage + '\'' + 
			",response = '" + response + '\'' + 
			",total_page = '" + totalPage + '\'' + 
			",api_status = '" + apiStatus + '\'' + 
			",current_page = '" + currentPage + '\'' + 
			",status = '" + status + '\'' + 
			",total_order = '" + totalOrder + '\'' + 
			",message = '" + message + '\'' +
			"}";
		}
}