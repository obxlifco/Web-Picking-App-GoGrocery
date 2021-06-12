package com.gogrocery.Models.DeliverySlotModel;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class DeliverySlot {

@SerializedName("delivery_date")
@Expose
private String deliveryDate;
@SerializedName("available_slot")
@Expose
private List<AvailableSlot> availableSlot = null;

public String getDeliveryDate() {
return deliveryDate;
}

public void setDeliveryDate(String deliveryDate) {
this.deliveryDate = deliveryDate;
}

public List<AvailableSlot> getAvailableSlot() {
return availableSlot;
}

public void setAvailableSlot(List<AvailableSlot> availableSlot) {
this.availableSlot = availableSlot;
}

}