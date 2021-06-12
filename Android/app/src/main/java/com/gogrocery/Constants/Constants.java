package com.gogrocery.Constants;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.Dialog;
import android.content.Context;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.res.Configuration;
import android.location.Address;
import android.location.Geocoder;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Build;
import android.provider.Settings;
import android.text.InputFilter;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.TextUtils;
import android.util.Log;
import android.view.Gravity;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowManager;
import android.view.inputmethod.InputMethodManager;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.gogrocery.Models.WarehouseModel.WarehouseModel;
import com.gogrocery.R;
import com.gogrocery.application.GoGrocery;
import com.google.android.gms.auth.api.signin.GoogleSignInClient;
import com.google.android.material.snackbar.Snackbar;
import com.google.android.material.textfield.TextInputEditText;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.math.BigDecimal;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.TimeZone;

public final class Constants {
    /* TESTING IN DEVELOPMENT URL */
/*   public final static String BASE_URL = "http://15.185.126.44:8062/api/front/v1/";  //live kolyan
    public final static String BASE_URL_SUBSTITUTE = "http://15.185.126.44:8062/api/";  //live kolyan
    public final static String ELASTIC_SEARCH_LISTING = "http://15.185.126.44:8062/api/search_elastic/";// develop kolyan*/
    /* TESTING IN LIVE URL */
     public final static String BASE_URL_SUBSTITUTE = "http://gogrocery.ae:81/api/";  //live
     public final static String BASE_URL = "https://www.gogrocery.ae/api/front/v1/";  //live
 public final static String ELASTIC_SEARCH_LISTING = "https://www.gogrocery.ae/api/search_elastic/";

    //public final static String ELASTIC_SEARCH_LISTING = "http://navsoft.co.in:9200/lifco_product_1/data/_search/";
    //public final static String ELASTIC_SEARCH_LISTING = "http://157.175.131.51:9200/lifco_product_1/data/_search";
    //public final static String ELASTIC_SEARCH_LISTING = "https://www.gogrocery.ae/elastic/lifco_product_1/data/_search";
    // public final static String ELASTIC_SEARCH_LISTING = "https://www.gogrocery.ae/elastic/lifco1_product_1/data/_search";


    //  public final static String ELASTIC_SEARCH_LISTING = "http://15.185.126.44:9200/lifco1_product_1/data/_search";

    // public final static String IMAGE_SLIDER_URL =  "http://boostmysale.s3.amazonaws.com/Lifco/lifco/CategoryBanner/800x800/";
    public final static String IMAGE_SLIDER_URL = "https://lifcogrocery.s3.amazonaws.com/Lifco/lifco/CategoryBanner/800x800/";
    public final static String IMAGE_BASE_URL = "https://lifcogrocery.s3.amazonaws.com/Lifco/lifco/product/";
    public final static String IMAGE_URL_CATEGOERY_BANNER = "https://lifcogrocery.s3.amazonaws.com/Lifco/lifco/CategoryBanner/800x800/";
    public final static String IMAGE_URL_BANNER = "https://lifcogrocery.s3.amazonaws.com/Lifco/lifco/cmsimages/";
    public final static String IMAGE_URL_BRAND = "https://lifcogrocery.s3.amazonaws.com/Lifco/lifco/brand/200x200/";
    public static GoogleSignInClient mGoogleSignInClient;
    public final static String IMAGE_URL_CATEGOERY = "https://lifcogrocery.s3.amazonaws.com/Lifco/lifco/category/200x200/";
    public final static String IMAGE_PRODUCT_URL = "https://lifcogrocery.s3.amazonaws.com/Lifco/lifco/product/400x400/";
    public final static String IMAGE_CART_URL = "https://lifcogrocery.s3.amazonaws.com/Lifco/lifco/product/200x200/";
    public final static String WAREHOUSE_LOGO = "https://lifcogrocery.s3.amazonaws.com/Lifco/lifco/warehouselogo/800x800/";
    public final static String STORE_TYPE_LOGO = "https://lifcogrocery.s3.amazonaws.com/Lifco/lifco/storecategorylogo/800x800/";
    // public final static String API_KEY = "AIzaSyDdnHSfwdG3jfIIL7pPw1S36RM0tcXvwgo";//Live Key from Pandit da
    public final static String API_KEY = "AIzaSyBus_gcbVKcO5MFinVIX3yNpuYHO6fHJao";//Live Key from Sukdev
    // public final static String API_KEY = "AIzaSyDwJfFz9Hyur4RkbEa_Hlt6Fkibr6rYhJo";//old


    public final static class VARIABLES {

        public final static String STATUS_SUCESS_CODE = "200";
        public static String DEVICEID = "";
        public static String WAREHOUSE_KEY = "WAREHOUSE";
        public static int CART_COUNT = 0;
        public static String CART_SUB_AMOUNT = "";
        public static String CURRENT_CURRENCY = "";
        public static String SPECIAL_INSTRUCTION = "";
        public static String FILTER_TYPE = "";
        public static String USER_LANG_CODE = "";
        //public static String SELECTED_ADDRESS_ID = "";
        public static WarehouseModel mWarehouseModel;
        public static List<String> mFilterAddedList = new ArrayList<>();
        public static List<String> mWishlistModelAddedList = new ArrayList<String>();

        public static List<String> categoryFilterList = new ArrayList<>();
        public static List<String> priceFilterList = new ArrayList<>();
        public static List<String> brandFilterList = new ArrayList<>();
        public static List<String> sizeFilterList = new ArrayList<>();
        public static List<String> discountFilterList = new ArrayList<>();
        public static String page_title = "";
    }


    public final static class API_METHODS {
        /* TESTING IN LIVE */
        public final static String CART_SUMMARY = "cart-summary-test/";
        public final static String APPLY_COUPON = "apply-coupon-test/";
        public final static String WAREHOUSE_LIST = "warehouse-list-test/";
        public final static String VIEW_CART = "view-cart-test/";
        public final static String MY_PROFILE = "my-profile-test/";
        public final static String SIGN_UP = "signup-test//";
        public final static String LOGIN = "login-test/";
        public final static String ADDRESSES = "delivery-address-test/";
        public final static String DELETE_WISHLIST = "delete-wishlist-test/";
        public final static String CHECK_DELIVERY_ADDRESS = "check-delivery-address-test/";
        public final static String PAYMENT_REQUEST_SI_CHARGES_LIST = "payment-request-si-charge-list/";
        public final static String REMOVE_SAVED_CARD = "remove-saved-card/";
      public final static String SAVE_CART_SI = "save-cart-si/";

        /* TESTING IN DEVELOPMENT */
/*        public final static String WAREHOUSE_LIST = "warehouse-list/";
        public final static String SIGN_UP = "signup/";
        public final static String APPLY_COUPON = "apply-coupon/";
        public final static String DELETE_WISHLIST = "delete-wishlist/";
        public final static String VIEW_CART = "view-cart/";
        public final static String LOGIN = "login/";//OLD
        public final static String CART_SUMMARY = "cart-summary/";
        public final static String SAVE_CART_SI = "save-cart/";
        public final static String CHECK_DELIVERY_ADDRESS = "check-delivery-address/";
        public final static String ADDRESSES = "delivery-address/";
        public final static String PAYMENT_REQUEST_SI_CHARGES_LIST = "payment-request-si-charge-list/";
        public final static String REMOVE_SAVED_CARD = "remove-saved-card/";
        public final static String MY_PROFILE = "my-profile/";*/


        public final static String deals_of_the_day = "deals_of_the_day/";
        public final static String best_selling_product = "best_selling_product/";
        public final static String banner_list = "banner_list/";
        public final static String product_list = "product-list/";
        public final static String categories = "menu_bar/";
        public final static String HOME_CMS = "home-cms/";
        // public final static String SIDE_MENU = "menu_bar/";
        public final static String SIDE_MENU = "menu_bar_app/";


        public final static String ADD_TO_CART = "add-to-cart/";
        public final static String PRODUCT_DETAILS = "product-details/";


        public final static String STORE_TYPE = "get_storetype/";
        public final static String COUNTRY_LIST = "countries-list/";
        public final static String STATE_LIST = "states-list/";


        public final static String DELETE_ADDRESS = "delete-address/";
        public final static String ORDER_HISTORY = "order-history/";
        public final static String CHECKOUT = "checkout/";
        public final static String LISTING_FILTERS = "listing_filters/";
        public final static String ORDER_DETAILS = "order-details/";
        public final static String DELIVERY_SLOT = "delivery-slot/";
        public final static String GET_SLUG = "slug/";
        public final static String EMPTY_CART = "empty-cart/";
        public final static String MY_WISH_LIST = "my-wish-list/";

        public final static String SIMILAR_PRODUCT = "similar-product/";
        public final static String POPULAR_PRODUCT = "popular-product/";
        public final static String FORGOT_PASSWORD = "forgotpassword/";
        public final static String CHANGE_PASSWORD = "change-password/";
        public final static String CANCEL_ORDER = "cancel-order/";
        public final static String PRODUCT_REVIEW = "product-review/";
        public final static String MY_WALLET = "points-log/";
        public final static String VIEW_RATING_REVIEW = "view-review/";
        public final static String CHECK_BALANCE = "check-balance/";
        public final static String APPLY_LOYALTY = "apply-loyalty/";
        public final static String UPDATE_DEVICE_DETAILS = "update-device-details/";

        public final static String CARD_PAYMENT = "payment/";
        public final static String SAVE_LIST = "save-list/";
        public final static String SAVE_LIST_DATAIL_LIST = "savelist-details/";
        public final static String DELETE_SINGLE_SAVE_LIST = "addeditdelete-from-savelist/";
        public final static String DELETE_PRODUCT_FROM_SAVE_LIST = "addremove-from-savelist/";
        public final static String EDIT_SINGLE_SAVE_LIST_NAME = "addeditdelete-from-savelist/";
        public final static String ADD_PRODUCT_TO_SAVE_LIST = "addremove-from-savelist/";
        public final static String ADD_SINGLE_SAVE_LIST_WITHOUT_PRODUCT_ID = "addeditdelete-from-savelist/";
        public final static String SOCIAL_LOGIN = "social-login/";
        public final static String SEARCH_FILTER = "search-filter/";
        public final static String PAYMENT_TRANSACTION = "payment-transaction/";
        public final static String CONFIRM_PASSWORD = "confirm-password/";
        public final static String GET_APP_VERSION = "get-app-version/";
        public final static String PAYMENT_METHODS = "payment-method/";
        public final static String CUSTOMER_QUERY = "customer-query/";
        public final static String PAGE_URL_TO_ID = "page_url_to_id/";
        public final static String SELECT_ADDRESS = "select-address/";
        public final static String ORDER_LIST_DETAILS = "picker-orderlistdetails/";
        public final static String SUBMIT_SUBSTITUTE_PRODUCT = "picker-acceptapproval/";
        public final static String PICKER_RESET_APPROVAL = "picker-resetsendapproval/";
        public final static String LOGOUT = "picker-logout/";
        public final static String PICKER_SEND_NOTIFICATION = "picker-sendpushnotification/";


        public static String PRODUCT_DETAILS_SLUG = "";

    }

    public static final class SHARED_PREFERENCE_KEYS {
        public static final String LOGIN_DETAIL = "login_detail";
    }

    public static void getAddressFromLocation(Context argContext, double mLat, double mLng) {
        System.out.println("Rahul : Constants : getAddressFromLocation : mLat : " + mLat);
        System.out.println("Rahul : Constants : getAddressFromLocation : mLng : " + mLng);
        Geocoder geocoder;
        List<Address> addresses = null;
        geocoder = new Geocoder(argContext, Locale.getDefault());

        try {
            System.out.println("getAddressFromLocation : Location : " + geocoder.getFromLocation(mLat, mLng, 1));
            addresses = geocoder.getFromLocation(mLat, mLng, 1);
        } catch (IOException e) {
            e.printStackTrace();
        }
        // Here 1 represent max location result to returned, by documents it recommended 1 to 5

        //String address = addresses.get(0).getAddressLine(0); // If any additional address line present than only, check with max available address lines by getMaxAddressLineIndex()
        String mcity = addresses.get(1).getLocality();
        String mstate = addresses.get(1).getAdminArea();
        String mcountry = addresses.get(1).getCountryName();
        String postalCode = addresses.get(1).getPostalCode();
        String knownName = addresses.get(1).getFeatureName();


    }

    public static boolean emailPatternValidtion(String argEmailId) {
        String emailPattern = "[a-zA-Z0-9._-]+@[a-z]+\\.+[a-z]+";

        return argEmailId.matches(emailPattern);
    }


    public static String getDeviceId(Context argContext) {
        String android_id = Settings.Secure.getString(argContext.getContentResolver(),
                Settings.Secure.ANDROID_ID);
        Log.e("device_id", android_id);
        return android_id;
    }

    /*    public static int checkProductLocalQuantity(Context argContext,String argProductId) {
            SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(argContext);
            int returnProductQty = 0;
            try {
                JSONObject mJsonObject = new JSONObject(mSharedPreferenceManager.getProductQuantityLocalJson());

                for (int i = 0; i < mJsonObject.length(); i++) {
                    if (mJsonObject.getString("").equals("")) {
                        returnProductQty = Integer.parseInt(mJsonObject.getString(""));

                    }
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
     //       ProductQuantityLocalMain mProductQuantityLocalMain = new Gson().fromJson(mSharedPreferenceManager.getProductQuantityLocalJson(), ProductQuantityLocalMain.class);

            return returnProductQty;

        }
        public static int updateProductLocalQuantity(Context argContext,String argProductId,String argQty) {
            SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(argContext);
            int returnProductQty = 0;
            try {
                JSONObject mJsonObject = new JSONObject(mSharedPreferenceManager.getProductQuantityLocalJson());

                for (int i = 0; i < mJsonObject.length(); i++) {
                    if (mJsonObject.getString("").equals("")) {
                        returnProductQty = Integer.parseInt(mJsonObject.getString(""));

                    }
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
            //       ProductQuantityLocalMain mProductQuantityLocalMain = new Gson().fromJson(mSharedPreferenceManager.getProductQuantityLocalJson(), ProductQuantityLocalMain.class);

            return returnProductQty;

        }*/
    public static String getSeperateValuesFromDate(String argDate, int i) {

        //2019-03-28
        String result = "";
        SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd");
        try {
            Date date = format.parse(argDate);

            String dayOfTheWeek = (String) android.text.format.DateFormat.format("EEEE", date); // Thursday
            String dayNumber = (String) android.text.format.DateFormat.format("dd", date); // 20
            String monthString = (String) android.text.format.DateFormat.format("MMM", date); // Jun
            String monthNumber = (String) android.text.format.DateFormat.format("MM", date); // 06
            String year = (String) android.text.format.DateFormat.format("yyyy", date); // 2013
            String hour = (String) android.text.format.DateFormat.format("hh", date); // 2013

            System.out.println("Rahul Experiment : dayOfTheWeek : " + dayOfTheWeek);
            System.out.println("Rahul Experiment : day : " + dayNumber);
            System.out.println("Rahul Experiment : monthString : " + monthString);
            System.out.println("Rahul Experiment : monthNumber : " + monthNumber);
            System.out.println("Rahul Experiment : year : " + year);
            System.out.println("Rahul Experiment : hour : " + hour);

            switch (i) {
                case 1:
                    result = dayOfTheWeek;
                    break;
                case 2:
                    result = dayNumber;
                    break;
                case 3:
                    result = monthString;
                    break;
                case 4:
                    result = monthNumber;
                    break;
                case 5:
                    result = year;
                    break;
            }
        } catch (ParseException e) {
            e.printStackTrace();
        }

        return result;
    }


    public static void showErrorDialog(Activity mContext) {
        Dialog mSomethingwentworng = new Dialog(mContext);
        mSomethingwentworng.setCancelable(true);
        mSomethingwentworng.setContentView(R.layout.something_went_wrong);

        mSomethingwentworng.show();

    }

    public static void showNoDeliveryDialog(Activity mContext) {
        Dialog mSomethingwentworng = new Dialog(mContext);
        mSomethingwentworng.setCancelable(true);
        mSomethingwentworng.setContentView(R.layout.no_delivery_dialog);

        mSomethingwentworng.show();

    }

/*    public static void hideSoftKeyboard(Activity activity) {
        InputMethodManager inputMethodManager =
                (InputMethodManager) activity.getSystemService(
                        Activity.INPUT_METHOD_SERVICE);
        inputMethodManager.hideSoftInputFromWindow(
                activity.getCurrentFocus().getWindowToken(), 0);
    }*/

    public static List<String> stringToArrayList(String argString) {
        System.out.println("Rahul : Constants : stringToArrayList : argString : " + argString);
        String str[] = argString.split(",");
        List<String> al = new ArrayList<String>();
        al = Arrays.asList(str);
        for (String s : al) {
            System.out.println("Rahul : Constants : stringToArrayList : s : " + s);
        }
        return al;
    }


    /*  public static String twoDecimalRoundOff(double argValue) {

          System.out.println("Rahul : twoDecimalRoundOff : argValue : " + argValue);
          if (argValue == 0) {
              System.out.println("Rahul : twoDecimalRoundOff : 1 : ");

              return String.valueOf(0.00);
          }*//*else if(String.valueOf(argValue).split(".")[0].length()==1) {
           if(String.valueOf(argValue).split(".")[0].equals("0")) {
               DecimalFormat df = new DecimalFormat("##.00");
               df.setMaximumFractionDigits(2);

               return "0"+df.format(argValue);
           }else {
               DecimalFormat df = new DecimalFormat("##.00");
               df.setMaximumFractionDigits(2);

               return df.format(argValue);
           }
        }*//* else {
     *//* if(String.valueOf(argValue).split(".")[0].length()==1&&String.valueOf(argValue).split(".")[0].equals("0"))
            {
                System.out.println("Rahul : twoDecimalRoundOff : 3.1 : ");
            }else {
                System.out.println("Rahul : twoDecimalRoundOff : 3.2 : ");

            }*//*

            System.out.println("Rahul : twoDecimalRoundOff : 2 : ");

            DecimalFormat df = new DecimalFormat("##.00");
            df.setMaximumFractionDigits(2);

            System.out.println("Rahul : twoDecimalRoundOff : 3 : " + df.format(argValue));
            //String forformat=df.format(argValue);
          *//*  if(forformat.split(".")[0].length()==1&&forformat.split(".")[0].equals("0"))
            {
                System.out.println("Rahul : twoDecimalRoundOff : 3.1 : ");
            }else {
                System.out.println("Rahul : twoDecimalRoundOff : 3.2 : ");

            }*//*
            return df.format(argValue);
        }
    }*/
/*
    public static String twoDecimalRoundOff(double argValue) {
        BigDecimal bigDecimal = new BigDecimal(argValue);
        bigDecimal = bigDecimal.setScale(2,
                BigDecimal.ROUND_HALF_UP);
        return "" + bigDecimal.doubleValue();
    }
*/


    public static String twoDecimalRoundOff(double argValue) {

        System.out.println("Sukdev: twoDecimalRoundOff : argValue : " + argValue);
        if (argValue == 0) {
            return String.valueOf(0.00);
        }/*else if(String.valueOf(argValue).split(".")[0].length()==1) {
           if(String.valueOf(argValue).split(".")[0].equals("0")) {
               DecimalFormat df = new DecimalFormat("##.00");
               df.setMaximumFractionDigits(2);

               return "0"+df.format(argValue);
           }else {
               DecimalFormat df = new DecimalFormat("##.00");
               df.setMaximumFractionDigits(2);

               return df.format(argValue);
           }
        }*/ else {
//            DecimalFormat df = new DecimalFormat("##.##");
//            df.setMaximumFractionDigits(2);
            @SuppressLint("DefaultLocale") String raoundValue = String.format("%.2f", argValue);
            return raoundValue;
        }
    }
   /* public static String twoDecimalRoundOff(double argValue) {

        System.out.println("Rahul : twoDecimalRoundOffSubString : argValue : "+argValue);

        String argConv= String.valueOf(argValue);
        System.out.println("Rahul : twoDecimalRoundOffSubString : argConv : "+argConv);
        if(argConv.contains("."))
        {
            return argConv.split(".")[0] + "" + argConv.split(".")[0].substring(1);
        }else {

            return argConv;
        }

    }*/

    public static void showToastInMiddle(Context argContext, String argMessage) {
        Toast toast = Toast.makeText(argContext,
                argMessage, Toast.LENGTH_SHORT);
        toast.setGravity(Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL, 0, 0);
        toast.show();
    }


    public static String getCurrentDate() {
        String date = new SimpleDateFormat("dd/MM/yyyy", Locale.getDefault()).format(new Date());
        return date;
    }

    public static String getAppVersion(Context context) {
        String version = "";
        try {
            PackageManager pm = context.getPackageManager();
            PackageInfo pInfo = pm.getPackageInfo(context.getPackageName(), 0);
            version = pInfo.versionName;

        } catch (PackageManager.NameNotFoundException e) {
            e.printStackTrace();
        }
        return version;
    }

    public static String getCurrentTime() {
        Date d = new Date();
        SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss");
        return (sdf.format(d));
    }

    public static String getCurrentDate_new() {
        return new SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(new Date());
    }

    public static String convertUTCToDatePrintFormat(String ourDate) throws ParseException {
        try {
            SimpleDateFormat formatter;
            if (ourDate.contains("T") || ourDate.contains("Z")) {
                formatter = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");
            } else {
                formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            }
            formatter.setTimeZone(TimeZone.getTimeZone("UTC"));
            Date value = formatter.parse(ourDate);

            SimpleDateFormat dateFormatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss"); //this format changeable
            //dateFormatter.setTimeZone(TimeZone.getTimeZone("Asia/Calcutta"));
            dateFormatter.setTimeZone(TimeZone.getDefault());
            ourDate = dateFormatter.format(value);

            //Log.d("ourDate", ourDate);
        } catch (Exception e) {
            ourDate = "00-00-0000 00:08";
        }
        return ourDate;

    }

    public static String calculateDifferenceBWDateTime(String startDate, String endDate) {
        //milliseconds
        SimpleDateFormat simpleDateFormat = new SimpleDateFormat("MM-dd-yyyy HH:mm:ss");

        try {
            Date date1 = simpleDateFormat.parse(startDate);
            Date date2 = simpleDateFormat.parse(endDate);
            long different = date2.getTime() - date1.getTime();

            long secondsInMilli = 1000;
            long minutesInMilli = secondsInMilli * 60;
            long hoursInMilli = minutesInMilli * 60;
            long daysInMilli = hoursInMilli * 24;

            long elapsedDays = different / daysInMilli;
            different = different % daysInMilli;

            long elapsedHours = different / hoursInMilli;
            different = different % hoursInMilli;

            long elapsedMinutes = different / minutesInMilli;
            different = different % minutesInMilli;

            long elapsedSeconds = different / secondsInMilli;

            return elapsedDays + "," + elapsedHours + "," + elapsedMinutes + "," + elapsedSeconds;
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return "0,0";

    }

    public static String getAddress(Context ctx, double latitude, double longitude) {
        StringBuilder result = new StringBuilder();
        try {
            Geocoder geocoder = new Geocoder(ctx, Locale.ENGLISH);
            List<Address> addresses = geocoder.getFromLocation(latitude, longitude, 1);
            if (addresses.size() > 0) {
                Address address = addresses.get(0);
                if (address.getLocality() != null) {
                    result.append(address.getLocality()).append(", ");
                }
                if (address.getSubLocality() != null) {
                    result.append(address.getSubLocality()).append(", ");
                }
                if (address.getPostalCode() != null) {
                    result.append(address.getCountryName()).append(", ");
                    result.append(address.getPostalCode()).append(". ");
                } else {
                    result.append(address.getCountryName()).append(". ");
                }
            }
        } catch (IOException e) {
            Log.e("tag", e.getMessage());
        }

        return result.toString();
    }

    public static String getMonthFormatDate(String date) throws ParseException {
        Date d = new SimpleDateFormat("yyyy-MM-dd", Locale.ENGLISH).parse(date);
        Calendar cal = Calendar.getInstance();
        cal.setTime(d);
        String monthFormatDate = new SimpleDateFormat("MM-dd-yyyy").format(cal.getTime());
        return monthFormatDate;
    }

    public static String getFormattedDate(String s) {
        Date date = null;
        try {
            date = new SimpleDateFormat("MM-dd-yyyy", Locale.ENGLISH).parse(s);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        //2nd of march 2015
        int day = cal.get(Calendar.DATE);

        if (!((day > 10) && (day < 19)))
            switch (day % 10) {
                case 1:
                    return new SimpleDateFormat("dd MMM yyyy ,").format(date);
                case 2:
                    return new SimpleDateFormat("dd MMM yyyy ,").format(date);
                case 3:
                    return new SimpleDateFormat("dd MMM yyyy ,").format(date);
                default:
                    return new SimpleDateFormat("dd MMM yyyy ,").format(date);
            }
        return new SimpleDateFormat("dd MMM yyyy ,").format(date);
    }

    public static String convertUTCToTimeFormatWithAM(String ourDate) throws ParseException {
        try {
            SimpleDateFormat formatter;
            if (ourDate.contains("T") && ourDate.contains("Z")) {
                formatter = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");
            } else if (ourDate.contains("T")) {
                formatter = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");
            } else {
                formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            }
            //formatter.setTimeZone(TimeZone.getTimeZone("UTC"));
            Date value = formatter.parse(ourDate);

            SimpleDateFormat dateFormatter = new SimpleDateFormat("HH:mm a"); //this format changeable
            dateFormatter.setTimeZone(TimeZone.getDefault());
            ourDate = dateFormatter.format(value);

            //Log.d("ourDate", ourDate);
        } catch (Exception e) {
            ourDate = "00-00-0000 00:08";
        }
        return ourDate;
    }


    public static void hideSoftKeyboard(Activity activity) {
        View focusedView = activity.getCurrentFocus();
        if (focusedView != null) {
            InputMethodManager inputMethodManager = (InputMethodManager) activity.getSystemService(Context.INPUT_METHOD_SERVICE);
            inputMethodManager.hideSoftInputFromWindow(focusedView.getWindowToken(), 0);
        }
    }


    public static void setupUI(View view, AppCompatActivity activity) {

        // Set up touch listener for non-text box views to hide keyboard.
        if (!(view instanceof TextInputEditText)) {
            view.setOnTouchListener(new View.OnTouchListener() {
                public boolean onTouch(View v, MotionEvent event) {
                    hideSoftKeyboard(activity);
                    return false;
                }
            });
        }

        //If a layout container, iterate over children and seed recursion.
        if (view instanceof ViewGroup) {
            for (int i = 0; i < ((ViewGroup) view).getChildCount(); i++) {
                View innerView = ((ViewGroup) view).getChildAt(i);
                setupUI(innerView, activity);
            }
        }
    }

    public static boolean isInternetConnected(Context mContext) {
        ConnectivityManager manager = (ConnectivityManager) mContext.getSystemService(Context.CONNECTIVITY_SERVICE);
        assert manager != null;
        NetworkInfo info = manager.getActiveNetworkInfo();
        return info != null && info.isConnectedOrConnecting();
    }
    /*=============        ==================*/

    public static void setSnackBar(View root, String snackTitle) {


        Snackbar snackbar = Snackbar.make(root, snackTitle, Snackbar.LENGTH_SHORT);
        snackbar.show();
      /*  View view = snackbar.getView();
        TextView txtv = (TextView) view.findViewById(android.support.design.R.id.snackbar_text);
        txtv.setGravity(Gravity.CENTER_HORIZONTAL);*/
    }

    /*============ Edit Text disable  EMOJI */
    public static InputFilter EMOJI_FILTER = new InputFilter() {
        @Override
        public CharSequence filter(CharSequence source, int start, int end, Spanned dest, int dstart, int dend) {
            boolean keepOriginal = true;
            StringBuilder sb = new StringBuilder(end - start);
            for (int index = start; index < end; index++) {
                int type = Character.getType(source.charAt(index));
                if (type == Character.SURROGATE || type == Character.OTHER_SYMBOL) {

                    return "";
                }
        /*        char c = source.charAt(index);
                if (isCharAllowed(c))
                    sb.append(c);
                else
                    keepOriginal = false;*/
            }
            if (keepOriginal)
                return null;
            else {
                if (source instanceof Spanned) {
                    SpannableString sp = new SpannableString(sb);
                    TextUtils.copySpansFrom((Spanned) source, start, sb.length(), null, sp, 0);
                    return sp;
                } else {
                    return sb;
                }
            }
        }
    };

    private static boolean isCharAllowed(char c) {
        return Character.isLetterOrDigit(c) || Character.isSpaceChar(c);
    }

    public static void log(String msg) {
        Log.d("@@ ", "-> " + msg);
    }

    public static void nwLog(String msg) {
        Log.v("MSG", msg);
    }

    public static void dbLog(String msg) {
        Log.v("MSG", "QUERY-> " + msg);
    }

    public static void log(JSONObject msg) {
        try {
            Log.d("@@ ", msg.toString(2));
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    public static void setApplicationLanguage(Context context, String language) {
        SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(context);

        if (language.equalsIgnoreCase(""))
            return;
        Locale myLocale = new Locale(language);//Set Selected Locale
        mSharedPreferenceManager.setLocalLanguage(language);

        Locale.setDefault(myLocale);//set new locale as default
        Configuration config = new Configuration();//get Configuration
        config.locale = myLocale;//set config locale as selected locale
        context.getResources().updateConfiguration(config, context.getResources().getDisplayMetrics());

    }


    public static String changeToEnglish(String str) {
        return (((((((((((str.replaceAll("١", "1")).replaceAll("٢", "2")).replaceAll("٣", "3")).replaceAll("٤", "4"))
                .replaceAll("٥", "5")).replaceAll("٦", "6")).replaceAll("٧", "7")).replaceAll("٨", "8")).replaceAll("٩", "9")).replaceAll("٠", "0")).replaceAll("٫", "."));
    }

    public static String getConvertedTime(String time) {

        String timeFrom = "";


        try {


            SimpleDateFormat sdf = new SimpleDateFormat("H:mm");
            Date dateObj = sdf.parse(time);

            String timeConverted = new SimpleDateFormat("K:mm a", Locale.US).format(dateObj);
            // String newTime  =   timeConverted.replaceFirst("0", "");
            timeFrom = timeConverted.replace(":00", " ");

           /* timeFrom1  = new SimpleDateFormat("K:mm a",Locale.US).format(dateObj); // Eg: "5:30 PM"
            timeFrom2 = new SimpleDateFormat("h a",Locale.US).format(dateObj);*/
//            System.out.println(dateObj);
//            System.out.println(new SimpleDateFormat("hh:mm a",Locale.US).format(dateObj));
        } catch (final ParseException e) {
            e.printStackTrace();
        }

//        try {
//
//            SimpleDateFormat sdf = new SimpleDateFormat(UtilityConstants.TIME_FORMAT_PATTERN_TIMESTAMP_PATTERN);
////            sdf.setTimeZone(TimeZone.getTimeZone(UtilityConstants.TIME_ZONE_UTC));
//            Date date=sdf.parse(string);
//
//            SimpleDateFormat sdfLocal = new SimpleDateFormat(UtilityConstants.DATE_FORMAT_PATTERN_TIME_12HR);
//            sdf.setTimeZone(TimeZone.getTimeZone(Calendar.getInstance().getTimeZone().getID()));
//            time=sdfLocal.format(date);
//
////            String[] timeSection=date.split(" ");
////            String[] timeParts = timeSection[0].split(":");
////
////            time=timeParts[0]+":"+timeParts[1];
//
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
        return timeFrom;
    }


}
