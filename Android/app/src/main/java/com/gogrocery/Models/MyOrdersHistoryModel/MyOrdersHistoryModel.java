package com.gogrocery.Models.MyOrdersHistoryModel;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class MyOrdersHistoryModel {

@SerializedName("status")
@Expose
private Integer status;
@SerializedName("data")
@Expose
private List<Data> data = null;


    public Integer getStatus() {
return status;
}

public void setStatus(Integer status) {
this.status = status;
}

public List<Data> getData() {
return data;
}

public void setData(List<Data> data) {
this.data = data;
}

}