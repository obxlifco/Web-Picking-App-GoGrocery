package com.gogrocery.Models.WalletModel;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class WalletModel {

@SerializedName("status")
@Expose
private Integer status;
@SerializedName("data")
@Expose
private List<WalletData> data = null;

public Integer getStatus() {
return status;
}

public void setStatus(Integer status) {
this.status = status;
}

public List<WalletData> getData() {
return data;
}

public void setData(List<WalletData> data) {
this.data = data;
}

}