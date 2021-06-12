package com.gogrocery.Models.PaymentTypesModel;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class PaymentMethodModel {

@SerializedName("api_status")
@Expose
private List<ApiStatus> apiStatus = null;

public List<ApiStatus> getApiStatus() {
return apiStatus;
}

public void setApiStatus(List<ApiStatus> apiStatus) {
this.apiStatus = apiStatus;
}

}