package com.gogrocery.picking.response_pojo.stock_list_pojo;

import javax.annotation.Generated;
import com.google.gson.annotations.SerializedName;

@Generated("com.robohorse.robopojogenerator")
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

	public void setImg(String img){
		this.img = img;
	}

	public String getImg(){
		return img;
	}

	public void setProduct(int product){
		this.product = product;
	}

	public int getProduct(){
		return product;
	}

	public void setUpdatedby(int updatedby){
		this.updatedby = updatedby;
	}

	public int getUpdatedby(){
		return updatedby;
	}

	public void setCreated(String created){
		this.created = created;
	}

	public String getCreated(){
		return created;
	}

	public void setLink(String link){
		this.link = link;
	}

	public String getLink(){
		return link;
	}

	public void setIsCover(int isCover){
		this.isCover = isCover;
	}

	public int getIsCover(){
		return isCover;
	}

	public void setImgAlt(Object imgAlt){
		this.imgAlt = imgAlt;
	}

	public Object getImgAlt(){
		return imgAlt;
	}

	public void setIpAddress(Object ipAddress){
		this.ipAddress = ipAddress;
	}

	public Object getIpAddress(){
		return ipAddress;
	}

	public void setImgOrder(Object imgOrder){
		this.imgOrder = imgOrder;
	}

	public Object getImgOrder(){
		return imgOrder;
	}

	public void setCreatedby(int createdby){
		this.createdby = createdby;
	}

	public int getCreatedby(){
		return createdby;
	}

	public void setModified(String modified){
		this.modified = modified;
	}

	public String getModified(){
		return modified;
	}

	public void setId(int id){
		this.id = id;
	}

	public int getId(){
		return id;
	}

	public void setWebsiteId(int websiteId){
		this.websiteId = websiteId;
	}

	public int getWebsiteId(){
		return websiteId;
	}

	public void setStatus(String status){
		this.status = status;
	}

	public String getStatus(){
		return status;
	}

	public void setImgTitle(Object imgTitle){
		this.imgTitle = imgTitle;
	}

	public Object getImgTitle(){
		return imgTitle;
	}

	@Override
 	public String toString(){
		return 
			"ProductImagesItem{" + 
			"img = '" + img + '\'' + 
			",product = '" + product + '\'' + 
			",updatedby = '" + updatedby + '\'' + 
			",created = '" + created + '\'' + 
			",link = '" + link + '\'' + 
			",is_cover = '" + isCover + '\'' + 
			",img_alt = '" + imgAlt + '\'' + 
			",ip_address = '" + ipAddress + '\'' + 
			",img_order = '" + imgOrder + '\'' + 
			",createdby = '" + createdby + '\'' + 
			",modified = '" + modified + '\'' + 
			",id = '" + id + '\'' + 
			",website_id = '" + websiteId + '\'' + 
			",status = '" + status + '\'' + 
			",img_title = '" + imgTitle + '\'' + 
			"}";
		}
}