package com.gogrocery.picking.response_pojo.version_pojo;

import com.google.gson.annotations.SerializedName;

public class Data{

	@SerializedName("version_i")
	private String versionI;

	@SerializedName("upgrade_to")
	private String upgradeTo;

	@SerializedName("is_mandatory")
	private String isMandatory;

	@SerializedName("id")
	private int id;

	@SerializedName("version_a")
	private String versionA;

	@SerializedName("picking_android")
	private String pickingAndroid;

	public void setVersionI(String versionI){
		this.versionI = versionI;
	}

	public String getVersionI(){
		return versionI;
	}

	public void setUpgradeTo(String upgradeTo){
		this.upgradeTo = upgradeTo;
	}

	public String getUpgradeTo(){
		return upgradeTo;
	}

	public void setIsMandatory(String isMandatory){
		this.isMandatory = isMandatory;
	}

	public String getIsMandatory(){
		return isMandatory;
	}

	public void setId(int id){
		this.id = id;
	}

	public int getId(){
		return id;
	}

	public void setVersionA(String versionA){
		this.versionA = versionA;
	}

	public String getVersionA(){
		return versionA;
	}

	public void setPickingAndroid(String pickingAndroid){
		this.pickingAndroid = pickingAndroid;
	}

	public String getPickingAndroid(){
		return pickingAndroid;
	}
}