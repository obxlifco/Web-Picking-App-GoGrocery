package com.gogrocery.picking.prefrences;

import android.app.Activity;
import android.content.Context;
import android.content.SharedPreferences;

import com.gogrocery.picking.GoGroceryPicking;

public class AppPreferences {
    private static final String APP_SHARED_PREFS = "com.android.gogrocerypicking";
    private static AppPreferences instance;
    private static SharedPreferences appSharedPrefs;
    private SharedPreferences.Editor prefsEditor;

    private AppPreferences(Context context) {
        this.appSharedPrefs = context.getSharedPreferences(APP_SHARED_PREFS, Activity.MODE_PRIVATE);
        this.prefsEditor = appSharedPrefs.edit();
    }

    public static AppPreferences getInstance() {
        if (instance instanceof AppPreferences) {
            return instance;
        } else {
            instance = new AppPreferences(GoGroceryPicking.applicationContext);
            return instance;
        }
    }

    public void clearAll() {
        prefsEditor.clear().apply();
    }

    public void storeDeviceId(String deviceID) {//firebase reg id.
        prefsEditor.putString("deviceID", deviceID);
        prefsEditor.apply();
    }

    public String getDeviceId() {//firebase id
        return appSharedPrefs.getString("deviceID", "");
    }

    public void removeDeviceId() {
        prefsEditor.remove("deviceID");
        prefsEditor.putString("deviceID", "");
        prefsEditor.apply();
    }

    public void storeUserToken(String deviceID) {
        prefsEditor.putString("userToken", deviceID);
        prefsEditor.apply();
    }

    public String getUserToken() {
        return appSharedPrefs.getString("userToken", "");
    }

    public void removeUserToken() {
        prefsEditor.remove("userToken");
        prefsEditor.putString("userToken", "");
        prefsEditor.apply();
    }

    public void storeCurrency(String currency) {
        prefsEditor.putString("currency", currency);
        prefsEditor.apply();
    }

    public String getCurrency() {
        return appSharedPrefs.getString("currency", "");
    }

    public void removeCurrency() {
        prefsEditor.remove("currency");
        prefsEditor.putString("currency", "");
        prefsEditor.apply();
    }

    public void storeUserID(Integer userID) {
        prefsEditor.putInt("userID", userID);
        prefsEditor.apply();
    }

    public Integer getUserID() {
        return appSharedPrefs.getInt("userID",0);
    }

    public void removeUserID() {
        prefsEditor.remove("userID");
        prefsEditor.putInt("userID",0);
        prefsEditor.apply();
    }

    public void storeUserImage(String userImage) {
        prefsEditor.putString("userImage", userImage);
        prefsEditor.apply();
    }

    public String getUserImage() {
        return appSharedPrefs.getString("userImage","");
    }

    public void removeUserImage() {
        prefsEditor.remove("userImage");
        prefsEditor.putString("userImage","");
        prefsEditor.apply();
    }

    public void storeUserName(String userName) {
        prefsEditor.putString("userName", userName);
        prefsEditor.apply();
    }

    public String getUserName() {
        return appSharedPrefs.getString("userName","");
    }

    public void removeUserName() {
        prefsEditor.remove("userName");
        prefsEditor.putString("userName","");
        prefsEditor.apply();
    }

    public void storeWebsiteID(Integer websiteID) {
        prefsEditor.putInt("websiteID", websiteID);
        prefsEditor.apply();
    }

    public Integer getWebsiteID() {
        return appSharedPrefs.getInt("websiteID",0);
    }

    public void removeWebsiteID() {
        prefsEditor.remove("websiteID");
        prefsEditor.putInt("websiteID",0);
        prefsEditor.apply();
    }

    public void storeWarehouseID(Integer warehouseID) {
        prefsEditor.putInt("warehouseID", warehouseID);
        prefsEditor.apply();
    }

    public Integer getWarehouseID() {
        return appSharedPrefs.getInt("warehouseID",0);
    }

    public void removeWarehouseID() {
        prefsEditor.remove("warehouseID");
        prefsEditor.putInt("warehouseID",0);
        prefsEditor.apply();
    }

    public void storeFirebaseToken(String token) {
        prefsEditor.putString("firebaseToken", token);
        prefsEditor.apply();
    }

    public String getFirebaseToken() {
        return appSharedPrefs.getString("firebaseToken", "");
    }

    public void removeFirebaseToken() {
        prefsEditor.remove("firebaseToken");
        prefsEditor.putString("firebaseToken", "");
        prefsEditor.apply();
    }

    public void storeLatestOrderID(Integer orderID) {
        prefsEditor.putInt("orderID", orderID);
        prefsEditor.apply();
    }

    public Integer getLatestOrderID() {
        return appSharedPrefs.getInt("orderID",0);
    }

    public void removeLatestOrderID() {
        prefsEditor.remove("orderID");
        prefsEditor.putInt("orderID",0);
        prefsEditor.apply();
    }

    public void storeViewOrderID(Integer orderID) {
        prefsEditor.putInt("viewOrderID", orderID);
        prefsEditor.apply();
    }

    public Integer getViewOrderID() {
        return appSharedPrefs.getInt("viewOrderID",0);
    }

    public void removeViewOrderID() {
        prefsEditor.remove("viewOrderID");
        prefsEditor.putInt("viewOrderID",0);
        prefsEditor.apply();
    }

}
