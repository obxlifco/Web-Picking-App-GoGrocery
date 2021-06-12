package com.gogrocery.Models.MyOrdersFromMailModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class MyOrdersFromMailModel {

@SerializedName("status")
@Expose
private Integer status;
@SerializedName("msg")
@Expose
private String msg;
@SerializedName("data")
@Expose
private MyOrdersFromMailData data;

public Integer getStatus() {
return status;
}

public void setStatus(Integer status) {
this.status = status;
}

public String getMsg() {
return msg;
}

public void setMsg(String msg) {
this.msg = msg;
}

public MyOrdersFromMailData getData() {
return data;
}

public void setData(MyOrdersFromMailData data) {
this.data = data;
}

}