package com.gogrocery.Models.SimilarProductModel;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class SimilarProductModel {

@SerializedName("status")
@Expose
private String status;
@SerializedName("data")
@Expose
private List<Data> data = null;

public String getStatus() {
return status;
}

public void setStatus(String status) {
this.status = status;
}

public List<Data> getData() {
return data;
}

public void setData(List<Data> data) {
this.data = data;
}

    public SimilarProductModel(String status, List<Data> data) {
        this.status = status;
        this.data = data;
    }
}