package com.gogrocery.picking.response_pojo.login_pojo;

import javax.annotation.Generated;
import com.google.gson.annotations.SerializedName;

@Generated("com.robohorse.robopojogenerator")
public class UserData{

	@SerializedName("company_id")
	private int companyId;

	@SerializedName("last_name")
	private String lastName;

	@SerializedName("isSuperAdmin")
	private String isSuperAdmin;

	@SerializedName("token")
	private String token;

	@SerializedName("defaultwebsite")
	private String defaultwebsite;

	@SerializedName("currencysymbol")
	private String currencysymbol;

	@SerializedName("image_name")
	private String image_name;

	@SerializedName("user_id")
	private int userId;

	@SerializedName("id")
	private int id;

	@SerializedName("defaultcurrency")
	private String defaultcurrency;

	@SerializedName("first_name")
	private String firstName;

	@SerializedName("website_id")
	private int websiteId;

	@SerializedName("email")
	private String email;

	@SerializedName("username")
	private String username;

	@SerializedName("warehouse_id")
	private int warehouseId;

	public void setCompanyId(int companyId){
		this.companyId = companyId;
	}

	public int getCompanyId(){
		return companyId;
	}

	public void setLastName(String lastName){
		this.lastName = lastName;
	}

	public String getLastName(){
		return lastName;
	}

	public void setIsSuperAdmin(String isSuperAdmin){
		this.isSuperAdmin = isSuperAdmin;
	}

	public String getIsSuperAdmin(){
		return isSuperAdmin;
	}

	public void setToken(String token){
		this.token = token;
	}

	public String getToken(){
		return token;
	}

	public void setDefaultwebsite(String defaultwebsite){
		this.defaultwebsite = defaultwebsite;
	}

	public String getDefaultwebsite(){
		return defaultwebsite;
	}

	public void setCurrencysymbol(String currencysymbol){
		this.currencysymbol = currencysymbol;
	}

	public String getCurrencysymbol(){
		return currencysymbol;
	}

	public void setUserId(int userId){
		this.userId = userId;
	}

	public int getUserId(){
		return userId;
	}

	public void setId(int id){
		this.id = id;
	}

	public int getId(){
		return id;
	}

	public void setDefaultcurrency(String defaultcurrency){
		this.defaultcurrency = defaultcurrency;
	}

	public String getDefaultcurrency(){
		return defaultcurrency;
	}

	public void setFirstName(String firstName){
		this.firstName = firstName;
	}

	public String getFirstName(){
		return firstName;
	}

	public void setWebsiteId(int websiteId){
		this.websiteId = websiteId;
	}

	public int getWebsiteId(){
		return websiteId;
	}

	public void setEmail(String email){
		this.email = email;
	}

	public String getEmail(){
		return email;
	}

	public void setUsername(String username){
		this.username = username;
	}

	public String getUsername(){
		return username;
	}

	public void setWarehouseId(int warehouseId){
		this.warehouseId = warehouseId;
	}

	public int getWarehouseId(){
		return warehouseId;
	}

	public String getImage_name() {
		return image_name;
	}

	public void setImage_name(String image_name) {
		this.image_name = image_name;
	}

	@Override
 	public String toString(){
		return 
			"UserData{" + 
			"company_id = '" + companyId + '\'' + 
			",last_name = '" + lastName + '\'' + 
			",isSuperAdmin = '" + isSuperAdmin + '\'' + 
			",token = '" + token + '\'' + 
			",defaultwebsite = '" + defaultwebsite + '\'' + 
			",currencysymbol = '" + currencysymbol + '\'' + 
			",user_id = '" + userId + '\'' + 
			",id = '" + id + '\'' + 
			",defaultcurrency = '" + defaultcurrency + '\'' + 
			",first_name = '" + firstName + '\'' + 
			",website_id = '" + websiteId + '\'' + 
			",email = '" + email + '\'' + 
			",username = '" + username + '\'' + 
			",warehouse_id = '" + warehouseId + '\'' + 
			",image_name = '" + image_name + '\'' +
			"}";
		}
}