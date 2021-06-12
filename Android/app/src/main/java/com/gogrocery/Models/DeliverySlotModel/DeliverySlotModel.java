package com.gogrocery.Models.DeliverySlotModel;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class DeliverySlotModel {

@SerializedName("status")
@Expose
private Integer status;
@SerializedName("delivery_slot")
@Expose
private List<DeliverySlot> deliverySlot = null;

public Integer getStatus() {
return status;
}

public void setStatus(Integer status) {
this.status = status;
}

public List<DeliverySlot> getDeliverySlot() {
return deliverySlot;
}

public void setDeliverySlot(List<DeliverySlot> deliverySlot) {
this.deliverySlot = deliverySlot;
}

}