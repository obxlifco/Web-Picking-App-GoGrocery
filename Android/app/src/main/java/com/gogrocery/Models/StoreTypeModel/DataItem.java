package com.gogrocery.Models.StoreTypeModel;

import com.google.gson.annotations.SerializedName;

public class DataItem{

	@SerializedName("image")
	private Object image;

	@SerializedName("isblocked")
	private String isblocked;

	@SerializedName("createdby")
	private int createdby;

	@SerializedName("created")
	private Object created;

	@SerializedName("name")
	private String name;

	@SerializedName("modified")
	private Object modified;

	@SerializedName("modifiedby")
	private Object modifiedby;

	@SerializedName("id")
	private int id;

	@SerializedName("has_store")
	private int has_store;

	@SerializedName("website_id")
	private int websiteId;

	@SerializedName("isdeleted")
	private String isdeleted;

	@SerializedName("order")
	private Object order;

	public void setImage(Object image){
		this.image = image;
	}

	public Object getImage(){
		return image;
	}

	public void setIsblocked(String isblocked){
		this.isblocked = isblocked;
	}

	public String getIsblocked(){
		return isblocked;
	}

	public void setCreatedby(int createdby){
		this.createdby = createdby;
	}

	public int getCreatedby(){
		return createdby;
	}

	public void setCreated(Object created){
		this.created = created;
	}

	public Object getCreated(){
		return created;
	}

	public void setName(String name){
		this.name = name;
	}

	public String getName(){
		return name;
	}

	public void setModified(Object modified){
		this.modified = modified;
	}

	public Object getModified(){
		return modified;
	}

	public void setModifiedby(Object modifiedby){
		this.modifiedby = modifiedby;
	}

	public Object getModifiedby(){
		return modifiedby;
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

	public void setIsdeleted(String isdeleted){
		this.isdeleted = isdeleted;
	}

	public String getIsdeleted(){
		return isdeleted;
	}

	public void setOrder(Object order){
		this.order = order;
	}

	public Object getOrder(){
		return order;
	}

	public int getHas_store() {
		return has_store;
	}

	public void setHas_store(int has_store) {
		this.has_store = has_store;
	}
}