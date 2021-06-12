package com.gogrocery.Models.DeliverySlotModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class AvailableSlot {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("location_id")
@Expose
private Integer locationId;
@SerializedName("zone_id")
@Expose
private Object zoneId;
@SerializedName("day_id")
@Expose
private Integer dayId;
@SerializedName("start_time")
@Expose
private String startTime;
@SerializedName("end_time")
@Expose
private String endTime;
@SerializedName("cutoff_time")
@Expose
private String cutoffTime;
@SerializedName("order_qty_per_slot")
@Expose
private Integer orderQtyPerSlot;
@SerializedName("based_on")
@Expose
private String basedOn;
@SerializedName("isdeleted")
@Expose
private String isdeleted;
@SerializedName("isblocked")
@Expose
private String isblocked;
@SerializedName("created")
@Expose
private String created;
@SerializedName("modified")
@Expose
private String modified;
@SerializedName("warehouse")
@Expose
private Integer warehouse;
@SerializedName("is_active")
@Expose
private String isActive;

public Integer getId() {
return id;
}

public void setId(Integer id) {
this.id = id;
}

public Integer getLocationId() {
return locationId;
}

public void setLocationId(Integer locationId) {
this.locationId = locationId;
}

public Object getZoneId() {
return zoneId;
}

public void setZoneId(Object zoneId) {
this.zoneId = zoneId;
}

public Integer getDayId() {
return dayId;
}

public void setDayId(Integer dayId) {
this.dayId = dayId;
}

public String getStartTime() {
return startTime;
}

public void setStartTime(String startTime) {
this.startTime = startTime;
}

public String getEndTime() {
return endTime;
}

public void setEndTime(String endTime) {
this.endTime = endTime;
}

public String getCutoffTime() {
return cutoffTime;
}

public void setCutoffTime(String cutoffTime) {
this.cutoffTime = cutoffTime;
}

public Integer getOrderQtyPerSlot() {
return orderQtyPerSlot;
}

public void setOrderQtyPerSlot(Integer orderQtyPerSlot) {
this.orderQtyPerSlot = orderQtyPerSlot;
}

public String getBasedOn() {
return basedOn;
}

public void setBasedOn(String basedOn) {
this.basedOn = basedOn;
}

public String getIsdeleted() {
return isdeleted;
}

public void setIsdeleted(String isdeleted) {
this.isdeleted = isdeleted;
}

public String getIsblocked() {
return isblocked;
}

public void setIsblocked(String isblocked) {
this.isblocked = isblocked;
}

public String getCreated() {
return created;
}

public void setCreated(String created) {
this.created = created;
}

public String getModified() {
return modified;
}

public void setModified(String modified) {
this.modified = modified;
}

public Integer getWarehouse() {
return warehouse;
}

public void setWarehouse(Integer warehouse) {
this.warehouse = warehouse;
}

public String getIsActive() {
return isActive;
}

public void setIsActive(String isActive) {
this.isActive = isActive;
}

}