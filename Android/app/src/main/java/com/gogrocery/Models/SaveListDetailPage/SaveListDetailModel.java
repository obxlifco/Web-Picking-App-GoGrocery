package com.gogrocery.Models.SaveListDetailPage;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class SaveListDetailModel {

@SerializedName("status")
@Expose
private Integer status;
@SerializedName("message")
@Expose
private String message;
@SerializedName("data")
@Expose
private List<SaveListDetailListData> data = null;

public Integer getStatus() {
return status;
}

public void setStatus(Integer status) {
this.status = status;
}

public String getMessage() {
return message;
}

public void setMessage(String message) {
this.message = message;
}

public List<SaveListDetailListData> getData() {
return data;
}

public void setData(List<SaveListDetailListData> data) {
this.data = data;
}

}