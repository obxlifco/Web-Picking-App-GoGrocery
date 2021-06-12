package com.gogrocery.Models.PaymentTypesModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class ApiStatus {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("engageboost_paymentgateway_method_id")
@Expose
private EngageboostPaymentgatewayMethodId engageboostPaymentgatewayMethodId;

public Integer getId() {
return id;
}

public void setId(Integer id) {
this.id = id;
}

public EngageboostPaymentgatewayMethodId getEngageboostPaymentgatewayMethodId() {
return engageboostPaymentgatewayMethodId;
}

public void setEngageboostPaymentgatewayMethodId(EngageboostPaymentgatewayMethodId engageboostPaymentgatewayMethodId) {
this.engageboostPaymentgatewayMethodId = engageboostPaymentgatewayMethodId;
}

}