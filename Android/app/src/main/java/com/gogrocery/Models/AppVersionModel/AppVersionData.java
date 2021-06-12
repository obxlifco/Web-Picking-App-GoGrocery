package com.gogrocery.Models.AppVersionModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class AppVersionData {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("version_a")
@Expose
private String versionA;
@SerializedName("version_i")
@Expose
private Object versionI;
@SerializedName("is_mandatory")
@Expose
private String isMandatory;
@SerializedName("upgrade_to")
@Expose
private String upgradeTo;

public Integer getId() {
return id;
}

public void setId(Integer id) {
this.id = id;
}

public String getVersionA() {
return versionA;
}

public void setVersionA(String versionA) {
this.versionA = versionA;
}

public Object getVersionI() {
return versionI;
}

public void setVersionI(Object versionI) {
this.versionI = versionI;
}

public String getIsMandatory() {
return isMandatory;
}

public void setIsMandatory(String isMandatory) {
this.isMandatory = isMandatory;
}

public String getUpgradeTo() {
return upgradeTo;
}

public void setUpgradeTo(String upgradeTo) {
this.upgradeTo = upgradeTo;
}

}