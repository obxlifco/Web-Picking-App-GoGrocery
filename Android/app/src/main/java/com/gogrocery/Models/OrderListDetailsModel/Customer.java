package com.gogrocery.Models.OrderListDetailsModel;

import com.google.gson.annotations.SerializedName;

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

	public String getAddress(){
		return address;
	}

	public Object getGroupId(){
		return groupId;
	}

	public String getPhone(){
		return phone;
	}

	public Object getVat(){
		return vat;
	}

	public String getLastName(){
		return lastName;
	}

	public int getId(){
		return id;
	}

	public String getFirstName(){
		return firstName;
	}

	public Object getCountryId(){
		return countryId;
	}

	public String getEmail(){
		return email;
	}
}