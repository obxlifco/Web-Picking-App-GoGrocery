package com.gogrocery.Models.StateListModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Data {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("country_id")
@Expose
private Integer countryId;
@SerializedName("state_code")
@Expose
private String stateCode;
@SerializedName("state_name")
@Expose
private String stateName;
@SerializedName("sap_ecustomer_state_no")
@Expose
private String sapEcustomerStateNo;
@SerializedName("sap_plant_no")
@Expose
private String sapPlantNo;

public Integer getId() {
return id;
}

public void setId(Integer id) {
this.id = id;
}

public Integer getCountryId() {
return countryId;
}

public void setCountryId(Integer countryId) {
this.countryId = countryId;
}

public String getStateCode() {
return stateCode;
}

public void setStateCode(String stateCode) {
this.stateCode = stateCode;
}

public String getStateName() {
return stateName;
}

public void setStateName(String stateName) {
this.stateName = stateName;
}

public String getSapEcustomerStateNo() {
return sapEcustomerStateNo;
}

public void setSapEcustomerStateNo(String sapEcustomerStateNo) {
this.sapEcustomerStateNo = sapEcustomerStateNo;
}

public String getSapPlantNo() {
return sapPlantNo;
}

public void setSapPlantNo(String sapPlantNo) {
this.sapPlantNo = sapPlantNo;
}

}