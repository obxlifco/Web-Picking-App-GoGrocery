package com.gogrocery.Models.OrderListDetailsModel;

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
	private int zoneId;

	@SerializedName("isblocked")
	private String isblocked;

	@SerializedName("no_of_vehicles")
	private Object noOfVehicles;

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

	public int getPicklistId(){
		return picklistId;
	}

	public Object getShippingMethodId(){
		return shippingMethodId;
	}

	public String getCreated(){
		return created;
	}

	public String getCreatedByName(){
		return createdByName;
	}

	public int getCreatedBy(){
		return createdBy;
	}

	public String getIsdeleted(){
		return isdeleted;
	}

	public int getZoneId(){
		return zoneId;
	}

	public String getIsblocked(){
		return isblocked;
	}

	public Object getNoOfVehicles(){
		return noOfVehicles;
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

	public String getCustomShipmentId(){
		return customShipmentId;
	}

	public int getWarehouseId(){
		return warehouseId;
	}

	public String getShipmentStatus(){
		return shipmentStatus;
	}
}