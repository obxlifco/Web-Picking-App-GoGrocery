package com.gogrocery.picking.response_pojo.order_list_pojo;

import com.google.gson.annotations.SerializedName;

public class OrderShipment{

	@SerializedName("picklist_id")
	private int picklistId;

	@SerializedName("shipping_method_id")
	private Object shippingMethodId;

	@SerializedName("created")
	private String created;

	@SerializedName("created_by_name")
	private String createdByName;

	@SerializedName("created_by")
	private int createdBy;

	@SerializedName("isdeleted")
	private String isdeleted;

	@SerializedName("zone_id")
	private Object zoneId;

	@SerializedName("isblocked")
	private String isblocked;

	@SerializedName("no_of_vehicles")
	private int noOfVehicles;

	@SerializedName("modified")
	private String modified;

	@SerializedName("id")
	private int id;

	@SerializedName("website_id")
	private int websiteId;

	@SerializedName("custom_shipment_id")
	private String customShipmentId;

	@SerializedName("warehouse_id")
	private int warehouseId;

	@SerializedName("shipment_status")
	private String shipmentStatus;

	public void setPicklistId(int picklistId){
		this.picklistId = picklistId;
	}

	public int getPicklistId(){
		return picklistId;
	}

	public void setShippingMethodId(Object shippingMethodId){
		this.shippingMethodId = shippingMethodId;
	}

	public Object getShippingMethodId(){
		return shippingMethodId;
	}

	public void setCreated(String created){
		this.created = created;
	}

	public String getCreated(){
		return created;
	}

	public void setCreatedByName(String createdByName){
		this.createdByName = createdByName;
	}

	public String getCreatedByName(){
		return createdByName;
	}

	public void setCreatedBy(int createdBy){
		this.createdBy = createdBy;
	}

	public int getCreatedBy(){
		return createdBy;
	}

	public void setIsdeleted(String isdeleted){
		this.isdeleted = isdeleted;
	}

	public String getIsdeleted(){
		return isdeleted;
	}

	public void setZoneId(Object zoneId){
		this.zoneId = zoneId;
	}

	public Object getZoneId(){
		return zoneId;
	}

	public void setIsblocked(String isblocked){
		this.isblocked = isblocked;
	}

	public String getIsblocked(){
		return isblocked;
	}

	public void setNoOfVehicles(int noOfVehicles){
		this.noOfVehicles = noOfVehicles;
	}

	public int getNoOfVehicles(){
		return noOfVehicles;
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

	public void setCustomShipmentId(String customShipmentId){
		this.customShipmentId = customShipmentId;
	}

	public String getCustomShipmentId(){
		return customShipmentId;
	}

	public void setWarehouseId(int warehouseId){
		this.warehouseId = warehouseId;
	}

	public int getWarehouseId(){
		return warehouseId;
	}

	public void setShipmentStatus(String shipmentStatus){
		this.shipmentStatus = shipmentStatus;
	}

	public String getShipmentStatus(){
		return shipmentStatus;
	}
}