package com.gogrocery.Models.OrderListDetailsModel;

import com.google.gson.annotations.SerializedName;

public class ProductImagesItem{

	@SerializedName("img")
	private String img;

	@SerializedName("product")
	private int product;

	@SerializedName("updatedby")
	private int updatedby;

	@SerializedName("created")
	private String created;

	@SerializedName("link")
	private String link;

	@SerializedName("is_cover")
	private int isCover;

	@SerializedName("img_alt")
	private Object imgAlt;

	@SerializedName("ip_address")
	private Object ipAddress;

	@SerializedName("img_order")
	private Object imgOrder;

	@SerializedName("createdby")
	private int createdby;

	@SerializedName("modified")
	private String modified;

	@SerializedName("id")
	private int id;

	@SerializedName("website_id")
	private int websiteId;

	@SerializedName("status")
	private String status;

	@SerializedName("img_title")
	private Object imgTitle;

	public String getImg(){
		return img;
	}

	public int getProduct(){
		return product;
	}

	public int getUpdatedby(){
		return updatedby;
	}

	public String getCreated(){
		return created;
	}

	public String getLink(){
		return link;
	}

	public int getIsCover(){
		return isCover;
	}

	public Object getImgAlt(){
		return imgAlt;
	}

	public Object getIpAddress(){
		return ipAddress;
	}

	public Object getImgOrder(){
		return imgOrder;
	}

	public int getCreatedby(){
		return createdby;
	}

	public String getModified(){
		return modified;
	}

	public int getId(){
		return id;
	}

	public int getWebsiteId(){
		return websiteId;
	}

	public String getStatus(){
		return status;
	}

	public Object getImgTitle(){
		return imgTitle;
	}
}