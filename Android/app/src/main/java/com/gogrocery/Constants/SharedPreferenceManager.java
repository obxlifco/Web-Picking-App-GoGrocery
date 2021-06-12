package com.gogrocery.Constants;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;

import com.gogrocery.Models.SideMenuModel.MenuBar;
import com.gogrocery.Models.StoreTypeModel.DataItem;
import com.gogrocery.ViewModel.StoreCategoryModel;
import com.gogrocery.view.MainActivityNew;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.lang.reflect.Type;
import java.util.List;


public class SharedPreferenceManager {
    // Shared Preferences
    SharedPreferences pref;

    // Editor for Shared preferences
    Editor editor;

    // Context
    Context _context;

    // Shared pref mode
    int PRIVATE_MODE = 0;

    // Sharedpref file name
    private static final String PREF_NAME = "GoGrocery";

    // All Shared Preferences Keys
    private static final String IS_LOGIN = "IsLoggedIn";

    // User name (make variable public to access from outside)
    public static final String KEY_NAME = "name";
    public static final String KEY_RECENT_SEARCH = "recent_search";
    public static final String KEY_SHOP_BY_CATEGORY = "shop_by_category";
    private static final String CATEGORY_LIST="category";
    private static final String SELECTED_CATEGORY_LIST="selected_category";

    // Email address (make variable public to access from outside)
    public static final String KEY_EMAIL = "email";
    public String key_name = "name";
    public String key_email = "email";
    public String key_mobile = "mobile";
    public String key_profile_pic = "profile_pic";
    public String key_token = "token";
    public String key_product_quantity_local = "product_quantity_local";
    public String KEY_LONGITUDE = "long";
    public String KEY_LATITUDE = "lat";
    public String CURRENT_CURRENCY = "currency";
    public String key_lat_long = "lat_long";
    public String key_warehouse_id = "warehouse_id";
    public String key_address_id = "address_id";
    public String key_warehouse_name = "warehouse_name";
    public String key_type_warehouse_name = "type_warehouse_name";
    public String key_type_warehouse_id = "type_warehouse_id";
    public String key_location_address = "location_address";
    public String key_wishlist = "wishlist";
    public String key_latitude = "latitude";
    public String key_longitude = "longitude";
    public String year_check = "year_check";
    private static final String SETTING_LNG="lang";
    private static final String DEV_KEY="dev_key";

    // Constructor
    public SharedPreferenceManager(Context context) {
        this._context = context;
        pref = _context.getSharedPreferences(PREF_NAME, PRIVATE_MODE);
        editor = pref.edit();
    }

    /**
     * Create login session
     */

    /*public void storeLoginDetails(String argLoginDetails) {
        editor.putBoolean(IS_LOGIN, true);
        editor.putString(Constants.SHARED_PREFERENCE_KEYS.LOGIN_DETAIL, argLoginDetails);
        editor.commit();
    }*/

   /* public void storeLastLoginDetails(String argEmail, String argPassword) {

        System.out.println("Rahul : storeLastLoginDetails : argEmail : "+argEmail);
        System.out.println("Rahul : storeLastLoginDetails : argPassword : "+argPassword);

        editor.putString("Remember_Email", argEmail);
        editor.putString("Remember_Password", argPassword);

        editor.commit();
    }*/
    public void storeUserProfileDetail(String argName, String argEmail,
                                       String argMobile, String argProfilePic, String argToken) {

        editor.putString(key_name, argName);
        editor.putString(key_email, argEmail);
        editor.putString(key_mobile, argMobile);
        editor.putString(key_profile_pic, argProfilePic);
        editor.putString(key_token, argToken);
        editor.putBoolean(IS_LOGIN, true);
        editor.commit();
    }


    public String getUserProfileDetail(String argWhat) {

        String returnResult = "";
        switch (argWhat) {
            case "name":
                returnResult = pref.getString(key_name, "");
                break;
            case "email":
                returnResult = pref.getString(key_email, "");
                break;
            case "mobile":
                returnResult = pref.getString(key_mobile, "");
                break;
            case "profile_pic":
                returnResult = pref.getString(key_profile_pic, "");
                break;
            case "token":
                returnResult = pref.getString(key_token, "");
                break;


        }
        return returnResult;
    }

    public void storeProductQuantityLocalJson(String argProductQuantityLocalJson) {

        editor.putString(key_product_quantity_local, argProductQuantityLocalJson);
        editor.commit();
    }

    public String getProductQuantityLocalJson() {

        return pref.getString(key_product_quantity_local, "");

    }

    public String getLastLoginEmail() {
        return pref.getString("Remember_Email", "");

    }

    public String getLastLoginPassword() {
        return pref.getString("Remember_Password", "");
    }

    public String getLoginDetails() {

        return pref.getString(Constants.SHARED_PREFERENCE_KEYS.LOGIN_DETAIL, null);

    }


    public void storeLatLong(String argLatLong) {

        editor.putString(key_lat_long, argLatLong);
        editor.commit();
    }

    public String getLatLong() {


        return pref.getString(key_lat_long, "");

    }
    public void saveYearCheck(String yearCheck) {

        editor.putString(year_check, yearCheck);
        editor.commit();
    }

    public String getYearCheck() {


        return pref.getString(year_check, "");

    }

    public void storeLatitude(String argLatLong) {

        editor.putString(key_latitude, argLatLong);
        editor.commit();
    }

    public String getLatitude() {


        return pref.getString(key_latitude, "");

    }

    public void storeLongitude(String argLatLong) {

        editor.putString(key_longitude, argLatLong);
        editor.commit();
    }

    public String getLongitude() {

        return pref.getString(key_longitude, "");

    }


    public void storeWarehouseId(String argWarehouseid) {

        editor.putString(key_warehouse_id, argWarehouseid);
        editor.commit();
    }

    public String getWarehouseId() {

        return pref.getString(key_warehouse_id, "");

    }

    public void storeSelectedAddressId(String argAddressId) {

        editor.putString(key_address_id, argAddressId);
        editor.commit();
    }

    public String getSelectedAddressId() {


        return pref.getString(key_address_id, "");

    }


    public void storeWarehouseName(String argWarehoouseName) {

        editor.putString(key_warehouse_name, argWarehoouseName);
        editor.commit();
    }

    public String getWarehouseName() {


        return pref.getString(key_warehouse_name, "");

    }

    public void storeTypeWarehouseName(String argWarehoouseTypeName) {

        editor.putString(key_type_warehouse_name, argWarehoouseTypeName);
        editor.commit();
    }

    public String getTypeWarehouseName() {


        return pref.getString(key_type_warehouse_name, "");

    }

    public void storeTypeWarehouseId(String argWarehoouseTypeId) {

        editor.putString(key_type_warehouse_id, argWarehoouseTypeId);
        editor.commit();
    }

    public String getTypeWarehouseId() {

        return pref.getString(key_type_warehouse_id, "");

    }

    public void storeLocationAddress(String locationName) {

        editor.putString(key_location_address, locationName);
        editor.commit();
    }

    public String getLocationAddress() {


        return pref.getString(key_location_address, "");

    }

    public void storeWishlistData(String argWishlistData) {

        editor.putString(key_wishlist, argWishlistData);
        editor.commit();
    }

    public String getWishlistData() {


        return pref.getString(key_wishlist, "");

    }

    public void saveCurrency(String currency) {

        editor.putString(CURRENT_CURRENCY, currency);
        editor.commit();
    }

    public String getCurrentCurrency() {


        return pref.getString(CURRENT_CURRENCY, "");

    }

    public boolean checkLogin() {
        // Check login status
        System.out.println("called : checkLogin : " + isLoggedIn());
       /* if (!this.isLoggedIn()) {
            // user is not logged in redirect him to Login Activity
            Intent i = new Intent(_context, IntroPage.class);
            // Closing all the Activities
            i.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);

            // Add new Flag to start new Activity
            i.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);

            // Staring Login Activity
            _context.startActivity(i);
        }
*/
        return isLoggedIn();
    }


    /**
     * Clear session details
     */
    public void logoutUser() {
        // Clearing all data from Shared Preferences
       /* editor.clear();
        editor.commit();*/

        clearLoginDetail();

        // After logout redirect user to Loing Activity
        Intent i = new Intent(_context, MainActivityNew.class);
        // Closing all the Activities
        i.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
        i.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        // Add new Flag to start new Activity
        i.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);

        // Staring Login Activity
        _context.startActivity(i);
    }


    private void clearLoginDetail() {
        editor.putBoolean(IS_LOGIN, false);
        editor.putString(Constants.SHARED_PREFERENCE_KEYS.LOGIN_DETAIL, "");
        editor.putString(KEY_RECENT_SEARCH, "");
        editor.putString(key_address_id, "");
        editor.commit();
    }


    /**
     * Quick check for login
     **/
    // Get Login State
    public boolean isLoggedIn() {
        return pref.getBoolean(IS_LOGIN, false);
    }

    public void storeRecentSearches(String argSearchJson) {

        editor.putString(KEY_RECENT_SEARCH, argSearchJson);
        editor.commit();
    }

    public String getRecentSearch() {

        return pref.getString(KEY_RECENT_SEARCH, "");
    }

    public void storeShopByCategory(String argSearchJson) {

        editor.putString(KEY_SHOP_BY_CATEGORY, argSearchJson);
        editor.commit();
    }

    public String getShopByCategory() {

        return pref.getString(KEY_SHOP_BY_CATEGORY, "");
    }

    public void saveDevKey(String token){
        editor.putString(DEV_KEY,token);
        editor.commit();
    }
    public String getDebKey(){
        return pref.getString(DEV_KEY,"");
    }


    public void saveCategoryList(List<MenuBar> mCategoryList) {
        Gson gson = new Gson();
        String json = gson.toJson(mCategoryList);
        editor.putString(CATEGORY_LIST, json);
        editor.apply();
    }





    public List<MenuBar>  getCategoryList() {
        Gson gson = new Gson();
        String json = pref.getString(CATEGORY_LIST, null);
        Type type = new TypeToken<List<MenuBar>>() {
        }.getType();
        return gson.fromJson(json, type);
    }


    public void saveSelectedCategoryList(List<DataItem> mCategoryList) {
        Gson gson = new Gson();
        String json = gson.toJson(mCategoryList);
        editor.putString(SELECTED_CATEGORY_LIST, json);
        editor.apply();
    }


    public void setLocalLanguage(String localLanguage) {

        editor.putString(SETTING_LNG, localLanguage);
        editor.commit();
    }

    public String getLocalLanguage() {

        return pref.getString(SETTING_LNG, "");
    }



    public List<DataItem>  getSelectedCategoryList() {
        Gson gson = new Gson();
        String json = pref.getString(SELECTED_CATEGORY_LIST, null);
        Type type = new TypeToken<List<DataItem>>() {
        }.getType();
        return gson.fromJson(json, type);
    }

}
