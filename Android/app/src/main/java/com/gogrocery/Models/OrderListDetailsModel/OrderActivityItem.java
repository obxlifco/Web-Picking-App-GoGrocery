package com.gogrocery.Models.OrderListDetailsModel;

import com.google.gson.annotations.SerializedName;

public class OrderActivityItem{

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

	public String getActivityComments(){
		return activityComments;
	}

	public int getUserId(){
		return userId;
	}

	public int getActivityType(){
		return activityType;
	}

	public Object getProductId(){
		return productId;
	}

	public Object getPurchaseOrderId(){
		return purchaseOrderId;
	}

	public String getActivityDate(){
		return activityDate;
	}

	public int getId(){
		return id;
	}

	public String getUserIpAddress(){
		return userIpAddress;
	}

	public int getOrderId(){
		return orderId;
	}

	public Object getUsername(){
		return username;
	}

	public int getStatus(){
		return status;
	}
}