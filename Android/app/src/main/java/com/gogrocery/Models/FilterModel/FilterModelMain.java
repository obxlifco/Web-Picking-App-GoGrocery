package com.gogrocery.Models.FilterModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.List;

public class FilterModelMain {



 /*   @SerializedName("status")
    @Expose
    private String status;*/

    @SerializedName("Filter")
    @Expose
    private List<FilterModel> Filter;

    public List<FilterModel> getmFilterModel() {
        return Filter;
    }

    public void setmFilterModel(List<FilterModel> mFilterModel) {
        this.Filter = mFilterModel;
    }

   /* public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }*/
}
