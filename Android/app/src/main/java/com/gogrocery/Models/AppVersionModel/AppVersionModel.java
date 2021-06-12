package com.gogrocery.Models.AppVersionModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class AppVersionModel {

@SerializedName("status")
@Expose
private Integer status;
@SerializedName("data")
@Expose
private AppVersionData data;

public Integer getStatus() {
return status;
}

public void setStatus(Integer status) {
this.status = status;
}

public AppVersionData getData() {
return data;
}

public void setData(AppVersionData data) {
this.data = data;
}

}