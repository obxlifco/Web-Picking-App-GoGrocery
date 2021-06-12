package com.gogrocery.Models.WishlistModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class ChannelPrice {

@SerializedName("channel_price")
@Expose
private String channelPrice;
@SerializedName("warehouse_id")
@Expose
private Integer warehouseId;

public String getChannelPrice() {
return channelPrice;
}

public void setChannelPrice(String channelPrice) {
this.channelPrice = channelPrice;
}

public Integer getWarehouseId() {
return warehouseId;
}

public void setWarehouseId(Integer warehouseId) {
this.warehouseId = warehouseId;
}

}