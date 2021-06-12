package com.gogrocery.picking.response_pojo.order_list_pojo;

import javax.annotation.Generated;
import com.google.gson.annotations.SerializedName;

@Generated("com.robohorse.robopojogenerator")
public class OrderActivity{

	@SerializedName("activity_comments")
	private String activityComments;

	@SerializedName("user_id")
	private int userId;

	@SerializedName("activity_type")
	private int activityType;

	@SerializedName("product_id")
	private Object productId;

	@SerializedName("purchase_order_id")
	private Object purchaseOrderId;

	@SerializedName("activity_date")
	private String activityDate;

	@SerializedName("id")
	private int id;

	@SerializedName("user_ip_address")
	private String userIpAddress;

	@SerializedName("order_id")
	private int orderId;

	@SerializedName("username")
	private Object username;

	@SerializedName("status")
	private int status;

	public void setActivityComments(String activityComments){
		this.activityComments = activityComments;
	}

	public String getActivityComments(){
		return activityComments;
	}

	public void setUserId(int userId){
		this.userId = userId;
	}

	public int getUserId(){
		return userId;
	}

	public void setActivityType(int activityType){
		this.activityType = activityType;
	}

	public int getActivityType(){
		return activityType;
	}

	public void setProductId(Object productId){
		this.productId = productId;
	}

	public Object getProductId(){
		return productId;
	}

	public void setPurchaseOrderId(Object purchaseOrderId){
		this.purchaseOrderId = purchaseOrderId;
	}

	public Object getPurchaseOrderId(){
		return purchaseOrderId;
	}

	public void setActivityDate(String activityDate){
		this.activityDate = activityDate;
	}

	public String getActivityDate(){
		return activityDate;
	}

	public void setId(int id){
		this.id = id;
	}

	public int getId(){
		return id;
	}

	public void setUserIpAddress(String userIpAddress){
		this.userIpAddress = userIpAddress;
	}

	public String getUserIpAddress(){
		return userIpAddress;
	}

	public void setOrderId(int orderId){
		this.orderId = orderId;
	}

	public int getOrderId(){
		return orderId;
	}

	public void setUsername(Object username){
		this.username = username;
	}

	public Object getUsername(){
		return username;
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
			"OrderActivity{" + 
			"activity_comments = '" + activityComments + '\'' + 
			",user_id = '" + userId + '\'' + 
			",activity_type = '" + activityType + '\'' + 
			",product_id = '" + productId + '\'' + 
			",purchase_order_id = '" + purchaseOrderId + '\'' + 
			",activity_date = '" + activityDate + '\'' + 
			",id = '" + id + '\'' + 
			",user_ip_address = '" + userIpAddress + '\'' + 
			",order_id = '" + orderId + '\'' + 
			",username = '" + username + '\'' + 
			",status = '" + status + '\'' + 
			"}";
		}
}