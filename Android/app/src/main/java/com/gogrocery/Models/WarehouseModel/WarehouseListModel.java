package com.gogrocery.Models.WarehouseModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.io.Serializable;

public class WarehouseListModel implements Serializable {

    private Currency currency;

    private Integer id;

    private Integer websiteId;

    private String name;

    private String code;

    private String address;

    private Integer countryId;

    private Integer stateId;

    private Object stateName;

    private String city;

    private String zipcode;

    private String phone;

    private String email;

    private Object channelId;

    private String latitude;

    private String longitude;

    private String maxDistanceSales;

    private String distance;

    private String warehouse_logo;

    public WarehouseListModel(Currency currency, Integer id, Integer websiteId, String name, String code, String address, Integer countryId, Integer stateId, Object stateName, String city, String zipcode, String phone, String email, Object channelId, String latitude, String longitude, String maxDistanceSales, String distance, String warehouse_logo) {
        this.currency = currency;
        this.id = id;
        this.websiteId = websiteId;
        this.name = name;
        this.code = code;
        this.address = address;
        this.countryId = countryId;
        this.stateId = stateId;
        this.stateName = stateName;
        this.city = city;
        this.zipcode = zipcode;
        this.phone = phone;
        this.email = email;
        this.channelId = channelId;
        this.latitude = latitude;
        this.longitude = longitude;
        this.maxDistanceSales = maxDistanceSales;
        this.distance = distance;
        this.warehouse_logo = warehouse_logo;
    }

    public Currency getCurrency() {
        return currency;
    }

    public Integer getId() {
        return id;
    }

    public Integer getWebsiteId() {
        return websiteId;
    }

    public String getName() {
        return name;
    }

    public String getCode() {
        return code;
    }

    public String getAddress() {
        return address;
    }

    public Integer getCountryId() {
        return countryId;
    }

    public Integer getStateId() {
        return stateId;
    }

    public Object getStateName() {
        return stateName;
    }

    public String getCity() {
        return city;
    }

    public String getZipcode() {
        return zipcode;
    }

    public String getPhone() {
        return phone;
    }

    public String getEmail() {
        return email;
    }

    public Object getChannelId() {
        return channelId;
    }

    public String getLatitude() {
        return latitude;
    }

    public String getLongitude() {
        return longitude;
    }

    public String getMaxDistanceSales() {
        return maxDistanceSales;
    }

    public String getDistance() {
        return distance;
    }

    public String getWarehouse_logo() {
        return warehouse_logo;
    }

    public void setCurrency(Currency currency) {
        this.currency = currency;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public void setWebsiteId(Integer websiteId) {
        this.websiteId = websiteId;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public void setCountryId(Integer countryId) {
        this.countryId = countryId;
    }

    public void setStateId(Integer stateId) {
        this.stateId = stateId;
    }

    public void setStateName(Object stateName) {
        this.stateName = stateName;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public void setZipcode(String zipcode) {
        this.zipcode = zipcode;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setChannelId(Object channelId) {
        this.channelId = channelId;
    }

    public void setLatitude(String latitude) {
        this.latitude = latitude;
    }

    public void setLongitude(String longitude) {
        this.longitude = longitude;
    }

    public void setMaxDistanceSales(String maxDistanceSales) {
        this.maxDistanceSales = maxDistanceSales;
    }

    public void setDistance(String distance) {
        this.distance = distance;
    }

    public void setWarehouse_logo(String warehouse_logo) {
        this.warehouse_logo = warehouse_logo;
    }
}
