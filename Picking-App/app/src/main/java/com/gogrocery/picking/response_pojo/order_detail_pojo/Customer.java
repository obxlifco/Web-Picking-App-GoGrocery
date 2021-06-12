package com.gogrocery.picking.response_pojo.order_detail_pojo;

import javax.annotation.Generated;
import com.google.gson.annotations.SerializedName;

@Generated("com.robohorse.robopojogenerator")
public class Customer{

	@SerializedName("address")
	private String address;

	@SerializedName("group_id")
	private Object groupId;

	@SerializedName("phone")
	private String phone;

	@SerializedName("vat")
	private Object vat;

	@SerializedName("last_name")
	private String lastName;

	@SerializedName("id")
	private int id;

	@SerializedName("first_name")
	private String firstName;

	@SerializedName("country_id")
	private Object countryId;

	@SerializedName("email")
	private String email;

	public void setAddress(String address){
		this.address = address;
	}

	public String getAddress(){
		return address;
	}

	public void setGroupId(Object groupId){
		this.groupId = groupId;
	}

	public Object getGroupId(){
		return groupId;
	}

	public void setPhone(String phone){
		this.phone = phone;
	}

	public String getPhone(){
		return phone;
	}

	public void setVat(Object vat){
		this.vat = vat;
	}

	public Object getVat(){
		return vat;
	}

	public void setLastName(String lastName){
		this.lastName = lastName;
	}

	public String getLastName(){
		return lastName;
	}

	public void setId(int id){
		this.id = id;
	}

	public int getId(){
		return id;
	}

	public void setFirstName(String firstName){
		this.firstName = firstName;
	}

	public String getFirstName(){
		return firstName;
	}

	public void setCountryId(Object countryId){
		this.countryId = countryId;
	}

	public Object getCountryId(){
		return countryId;
	}

	public void setEmail(String email){
		this.email = email;
	}

	public String getEmail(){
		return email;
	}

	@Override
 	public String toString(){
		return 
			"Customer{" + 
			"address = '" + address + '\'' + 
			",group_id = '" + groupId + '\'' + 
			",phone = '" + phone + '\'' + 
			",vat = '" + vat + '\'' + 
			",last_name = '" + lastName + '\'' + 
			",id = '" + id + '\'' + 
			",first_name = '" + firstName + '\'' + 
			",country_id = '" + countryId + '\'' + 
			",email = '" + email + '\'' + 
			"}";
		}
}