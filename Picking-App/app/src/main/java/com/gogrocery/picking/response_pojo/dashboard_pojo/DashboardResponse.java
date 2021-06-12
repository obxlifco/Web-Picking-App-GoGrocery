package com.gogrocery.picking.response_pojo.dashboard_pojo;

import javax.annotation.Generated;
import com.google.gson.annotations.SerializedName;

@Generated("com.robohorse.robopojogenerator")
public class DashboardResponse{

	@SerializedName("shipped_order")
	private int shippedOrder;

	@SerializedName("api_status")
	private String apiStatus;

	@SerializedName("status")
	private int status;

	@SerializedName("total_order")
	private int totalOrder;

	@SerializedName("pending_order")
	private int pending_order;

	@SerializedName("pending_processing_order")
	private int pending_processing_order;

	@SerializedName("cancel_order")
	private int cancel_order;

	@SerializedName("substitution_sent_order")
	private int substitution_sent_order;

	@SerializedName("substitution_received_order")
	private int substitution_received_order;

	public void setShippedOrder(int shippedOrder){
		this.shippedOrder = shippedOrder;
	}

	public int getShippedOrder(){
		return shippedOrder;
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

	public void setTotalOrder(int totalOrder){
		this.totalOrder = totalOrder;
	}

	public int getTotalOrder(){
		return totalOrder;
	}

	public int getPending_order() {
		return pending_order;
	}

	public void setPending_order(int pending_order) {
		this.pending_order = pending_order;
	}

	public int getPending_processing_order() {
		return pending_processing_order;
	}

	public void setPending_processing_order(int pending_processing_order) {
		this.pending_processing_order = pending_processing_order;
	}

	public int getCancel_order() {
		return cancel_order;
	}

	public void setCancel_order(int cancel_order) {
		this.cancel_order = cancel_order;
	}

	public int getSubstitution_sent_order() {
		return substitution_sent_order;
	}

	public void setSubstitution_sent_order(int substitution_sent_order) {
		this.substitution_sent_order = substitution_sent_order;
	}

	public int getSubstitution_received_order() {
		return substitution_received_order;
	}

	public void setSubstitution_received_order(int substitution_received_order) {
		this.substitution_received_order = substitution_received_order;
	}

	@Override
 	public String toString(){
		return 
			"DashboardResponse{" + 
			"shipped_order = '" + shippedOrder + '\'' + 
			",api_status = '" + apiStatus + '\'' + 
			",status = '" + status + '\'' + 
			",total_order = '" + totalOrder + '\'' + 
			",pending_order = '" + pending_order + '\'' +
			",pending_processing_order = '" + pending_processing_order + '\'' +
			",cancel_order = '" + cancel_order + '\'' +
			",substitution_received_order = '" + substitution_received_order + '\'' +
			",substitution_sent_order = '" + substitution_sent_order + '\'' +
			"}";
		}
}