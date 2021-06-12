package com.gogrocery.Models.WarehouseModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.io.Serializable;

public class Data {


    @SerializedName("currency")
    @Expose
    private Currency currency;
    @SerializedName("id")
    @Expose
    private Integer id;
    @SerializedName("website_id")
    @Expose
    private Integer websiteId;
    @SerializedName("name")
    @Expose
    private String name;
    @SerializedName("code")
    @Expose
    private String code;
    @SerializedName("address")
    @Expose
    private String address;
    @SerializedName("country_id")
    @Expose
    private Integer countryId;
    @SerializedName("state_id")
    @Expose
    private Integer stateId;
    @SerializedName("state_name")
    @Expose
    private Object stateName;
    @SerializedName("city")
    @Expose
    private String city;
    @SerializedName("zipcode")
    @Expose
    private String zipcode;
    @SerializedName("phone")
    @Expose
    private String phone;
    @SerializedName("email")
    @Expose
    private String email;
    @SerializedName("channel_id")
    @Expose
    private Object channelId;
    @SerializedName("latitude")
    @Expose
    private String latitude;
    @SerializedName("longitude")
    @Expose
    private String longitude;
    @SerializedName("max_distance_sales")
    @Expose
    private String maxDistanceSales;
    @SerializedName("distance")
    @Expose
    private String distance;
    @SerializedName("warehouse_logo")
    @Expose
    private String warehouse_logo;
    @SerializedName("store_open")
    @Expose
    private Boolean storeOpen;
    @SerializedName("store_time_display")
    @Expose
    private Boolean storeTimeDisplay;
    @SerializedName("open_time")
    @Expose
    private String openTime;
    @SerializedName("close_time")
    @Expose
    private String closeTime;
    @SerializedName("nextday")
    @Expose
    private Boolean nextday;

    public Boolean getStoreTimeDisplay() {
        return storeTimeDisplay;
    }

    public void setStoreTimeDisplay(Boolean storeTimeDisplay) {
        this.storeTimeDisplay = storeTimeDisplay;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getWebsiteId() {
        return websiteId;
    }

    public void setWebsiteId(Integer websiteId) {
        this.websiteId = websiteId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public Integer getCountryId() {
        return countryId;
    }

    public void setCountryId(Integer countryId) {
        this.countryId = countryId;
    }

    public Integer getStateId() {
        return stateId;
    }

    public void setStateId(Integer stateId) {
        this.stateId = stateId;
    }

    public Object getStateName() {
        return stateName;
    }

    public void setStateName(Object stateName) {
        this.stateName = stateName;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public String getZipcode() {
        return zipcode;
    }

    public void setZipcode(String zipcode) {
        this.zipcode = zipcode;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public Object getChannelId() {
        return channelId;
    }

    public void setChannelId(Object channelId) {
        this.channelId = channelId;
    }

    public String getLatitude() {
        return latitude;
    }

    public void setLatitude(String latitude) {
        this.latitude = latitude;
    }

    public String getLongitude() {
        return longitude;
    }

    public void setLongitude(String longitude) {
        this.longitude = longitude;
    }

    public String getMaxDistanceSales() {
        return maxDistanceSales;
    }

    public void setMaxDistanceSales(String maxDistanceSales) {
        this.maxDistanceSales = maxDistanceSales;
    }

    public String getDistance() {
        return distance;
    }

    public void setDistance(String distance) {
        this.distance = distance;
    }

    public String getWarehouse_logo() {
        return warehouse_logo;
    }

    public void setWarehouse_logo(String warehouse_logo) {
        this.warehouse_logo = warehouse_logo;
    }

    public Currency getCurrency() {
        return currency;
    }

    public void setCurrency(Currency currency) {
        this.currency = currency;
    }

    public Boolean getStoreOpen() {
        return storeOpen;
    }

    public void setStoreOpen(Boolean storeOpen) {
        this.storeOpen = storeOpen;
    }

    public String getOpenTime() {
        return openTime;
    }

    public void setOpenTime(String openTime) {
        this.openTime = openTime;
    }

    public String getCloseTime() {
        return closeTime;
    }

    public void setCloseTime(String closeTime) {
        this.closeTime = closeTime;
    }

    public Boolean getNextday() {
        return nextday;
    }

    public void setNextday(Boolean nextday) {
        this.nextday = nextday;
    }
}