package com.gogrocery.view;

import android.Manifest;
import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.content.IntentSender;
import android.content.pm.PackageManager;

import androidx.appcompat.app.AppCompatDelegate;
import androidx.databinding.DataBindingUtil;

import android.location.Location;

import android.net.Uri;
import android.os.Build;
import android.os.Handler;
import android.os.Message;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.android.volley.AuthFailureError;
import com.bumptech.glide.Glide;
import com.bumptech.glide.request.RequestOptions;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Models.ProductQuantityLocal;
import com.gogrocery.Models.ViewCartModel.ViewCartModel;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivitySplashBinding;
import com.google.android.material.bottomsheet.BottomSheetDialog;

import androidx.core.app.ActivityCompat;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import com.gogrocery.Constants.Constants;
import com.gogrocery.Models.AppVersionModel.AppVersionModel;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.common.api.PendingResult;
import com.google.android.gms.common.api.ResultCallback;
import com.google.android.gms.common.api.Status;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.location.LocationSettingsRequest;
import com.google.android.gms.location.LocationSettingsResult;
import com.google.android.gms.location.LocationSettingsStates;
import com.google.android.gms.location.LocationSettingsStatusCodes;

import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class SplashActivity extends AppCompatActivity {

    private ActivitySplashBinding mActivitySplashBinding;

    private boolean isTimerLoaded = false, isGetVersionLoaded = false;
    private Handler mHandler;
    private DatabaseHandler mDatabaseHandler;
    private boolean isOlderVersion = false;
    private SharedPreferenceManager mSharedPreferenceManager;
View view;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivitySplashBinding = DataBindingUtil.setContentView(this, R.layout.activity_splash);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        mDatabaseHandler = new DatabaseHandler(SplashActivity.this);
        hideStatusBar();
        AppCompatDelegate.setCompatVectorFromResourcesEnabled(true);
        if(mSharedPreferenceManager.getLocalLanguage().equals("")||(mSharedPreferenceManager.getLocalLanguage().isEmpty())){
            Constants.VARIABLES.USER_LANG_CODE="en";
            Constants.setApplicationLanguage(SplashActivity.this,"en");
            // AppData.USER_CURRENCY_CODE="USD";
        }else{
            Constants.VARIABLES.USER_LANG_CODE=mSharedPreferenceManager.getLocalLanguage();
            Constants.setApplicationLanguage(SplashActivity.this,mSharedPreferenceManager.getLocalLanguage());
        }
       /* String dried = "dried mango sliced";

        String dried1 = dried;

        dried1="\\"+"\""+dried+"\\"+"\"";
        System.out.println("Rahul : SplashScreen : dried : " + "\""+dried1+"\"");*/

        Thread background = new Thread() {
            public void run() {

                try {
                    sleep(3000);

                    isTimerLoaded = true;

                    mHandler.sendEmptyMessage(1);
                    //  findViewById(R.id.progressBar).setVisibility(View.GONE);

                } catch (InterruptedException e) {
                    e.printStackTrace();
                }


            }
        };
        background.start();



        mHandler = new Handler(new Handler.Callback() {
            @Override
            public boolean handleMessage(Message msg) {

                if (isGetVersionLoaded && isTimerLoaded) {
                    if (isOlderVersion) {
                        BottomSheetDialog bottomSheetDialog = new BottomSheetDialog(SplashActivity.this);
                        bottomSheetDialog.setContentView(R.layout.app_version_update);

                        Button btnUpgrade = bottomSheetDialog.findViewById(R.id.btnUpgrade);


                        assert btnUpgrade != null;
                        btnUpgrade.setOnClickListener(new View.OnClickListener() {
                            @Override
                            public void onClick(View v) {
                                final String appPackageName = getPackageName(); // getPackageName() from Context or Activity object
                                try {
                                    startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse("market://details?id=" + appPackageName)));
                                } catch (android.content.ActivityNotFoundException anfe) {
                                    startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse("https://play.google.com/store/apps/details?id=" + appPackageName)));
                                }
                                bottomSheetDialog.dismiss();

                                //For HUAWEI mobile
                                /*try {
                                    Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse("appmarket://details?id=" + appPackageName));
                                    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                                    startActivity(intent);
                                    bottomSheetDialog.dismiss();
                                } catch (ActivityNotFoundException anfe) {
                                    Toast.makeText(SplashActivity.this, "Huawei AppGallery not found!", Toast.LENGTH_SHORT).show();
                                }*/

                            }
                        });
                        try {
                            if (bottomSheetDialog != null) {
                                if (!bottomSheetDialog.isShowing()) {
                                    bottomSheetDialog.show();
                                }
                            }

                        }catch (Exception e){
                            e.printStackTrace();
                        }



                    } else {
                         SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(SplashActivity.this);
                        if(mSharedPreferenceManager.isLoggedIn()){

                           // if(mSharedPreferenceManager.getWarehouseId()!=null&&!mSharedPreferenceManager.getWarehouseId().isEmpty() &&  mSharedPreferenceManager.getTypeWarehouseId()!=null&&!mSharedPreferenceManager.getTypeWarehouseId().isEmpty()){
                            if(mSharedPreferenceManager.getLongitude()!=null&&!mSharedPreferenceManager.getLongitude().isEmpty()){
                                Intent i = new Intent(SplashActivity.this, SelectCategory.class);
                                i.putExtra("latitude", mSharedPreferenceManager.getLatitude());
                                i.putExtra("longitude", mSharedPreferenceManager.getLongitude());
                                i.putExtra("select_category_list","");
                                i.putExtra("from_where","start");
                                startActivity(i);
                                finish();
                            }else {
                                Intent i = new Intent(SplashActivity.this, IntroStepOne.class);
                                i.putExtra("from","start");
                                startActivity(i);
                                finish();
                            }



                        }else {
                            if(mSharedPreferenceManager.getLongitude()!=null&&!mSharedPreferenceManager.getLongitude().isEmpty()){
                                Intent i = new Intent(SplashActivity.this, LoginActivity.class);
                                startActivity(i);
                                finish();
                            }else {
                                Intent i = new Intent(SplashActivity.this, StartedActivity.class);

                                startActivity(i);
                                finish();
                            }

                        }
                    }
                }

                return false;
            }
        });

    }


    public int getImage(String imageName) {

        int drawableResourceId = this.getResources().getIdentifier(imageName, "drawable", this.getPackageName());

        return drawableResourceId;
    }

    public void requestVersionUpdate() throws JSONException {

        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        //findViewById(R.id.progressSpinKitView).setVisibility(View.VISIBLE);
      /*  JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("latitude", argLat);
        mJsonObject.put("longitude", argLong);
        mJsonObject.put("website_id", 1);*/

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.GET_APP_VERSION, null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        isGetVersionLoaded = true;
                        System.out.println("Rahul : SplashActivity : requestVersionUpdate : response : " + response);
                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        AppVersionModel mAppVersionModel = mGson.fromJson(mJsonObject.toString(), AppVersionModel.class);
                        System.out.println("Rahul : SplashActivity : requestVersionUpdate : check : " + "1.0.0".equals(mAppVersionModel.getData().getUpgradeTo()));


                   if (!Constants.getAppVersion(SplashActivity.this).equals(mAppVersionModel.getData().getUpgradeTo())) {
                     //   if (!"1.2.7".equals(mAppVersionModel.getData().getUpgradeTo())) {/*develop*/

                         try {
                             requestViewCart();
                         } catch (JSONException e) {
                             e.printStackTrace();
                         }
                         isOlderVersion = true;
                        } else {

                        }

                        mHandler.sendEmptyMessage(1);
                    }

                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                System.out.println("Rahul : SplashActivity : requestVersionUpdate : error : " + error);
                isGetVersionLoaded = true;
                mHandler.sendEmptyMessage(1);
            }
        });


        // Adding request to request queue
        jsonObjReq.setRetryPolicy(new RetryPolicy() {
            @Override
            public int getCurrentTimeout() {
                return 50000;
            }

            @Override
            public int getCurrentRetryCount() {
                return 50000;
            }

            @Override
            public void retry(VolleyError error) throws VolleyError {

            }
        });
        queue.add(jsonObjReq);
    }

    @Override
    protected void onStart() {
        super.onStart();

    }

    @Override
    protected void onStop() {
        super.onStop();

    }



    @Override
    protected void onResume() {
        super.onResume();
        try {
            if(Constants.isInternetConnected(SplashActivity.this)){
            requestVersionUpdate();
            }
            else {
                Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }


    public void requestViewCart() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        System.out.println("Rahul : MainActivityNew : requestViewCart : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.VIEW_CART, null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {

                        System.out.println("Rahul : MainActivityNew : requestViewCart : mJsonObject : " + response);
                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        System.out.println("Rahul : MainActivityNew : requestViewCart : mJsonObject : " + mJsonObject);
                        ViewCartModel mViewCartModel = mGson.fromJson(response.toString(), ViewCartModel.class);
                        if (!mViewCartModel.getCartCount().equals("0")) {
                            //mActivityMainBinding.appBarInclude.badgeNotification.setVisibility(View.VISIBLE);
                            //mActivityMainBinding.appBarInclude.badgeNotification.setText(mViewCartModel.getCart_count_itemwise());

                            Constants.VARIABLES.CART_COUNT = Integer.parseInt(mViewCartModel.getCart_count_itemwise());
                            for (int i = 0; i < mViewCartModel.getData().size(); i++) {
                                ProductQuantityLocal mProductQuantityLocal = new ProductQuantityLocal(String.valueOf(mViewCartModel.getData().get(i).getProductId()), String.valueOf(mViewCartModel.getData().get(i).getQuantity()));
                                if (!mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(mViewCartModel.getData().get(i).getProductId())).equals("0")) {
                                    mDatabaseHandler.updateProductQuantityById(mProductQuantityLocal);
                                } else {
                                    mDatabaseHandler.addProductQty(mProductQuantityLocal);
                                }

                            }

                        } else {
                            mDatabaseHandler.deleteAllRecord();
                            Constants.VARIABLES.CART_COUNT = 0;

                            //mActivityMainBinding.appBarInclude.badgeNotification.setVisibility(View.GONE);
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                Constants.VARIABLES.CART_COUNT = 0;
                mDatabaseHandler.deleteAllRecord();
                //mActivityMainBinding.appBarInclude.badgeNotification.setVisibility(View.GONE);

                System.out.println("Rahul : MainActivityNew : requestViewCart : VolleyError : " + error.toString());
                if (error.equals("com.android.volley.ParseError")) {
                    System.out.println("Rahul : MainActivityNew : requestViewCart : VolleyError : ParseError ");

                }
            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put(Constants.VARIABLES.WAREHOUSE_KEY, mSharedPreferenceManager.getWarehouseId());
                if (mSharedPreferenceManager.isLoggedIn()) {
                    headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                } else {
                    headers.put("DEVICEID", Constants.getDeviceId(getApplicationContext()));
                }

               /* if (mSharedPreferenceManager.isLoggedIn()) {
                    headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                } else {
                    headers.put("DEVICEID", Constants.getDeviceId(getApplicationContext()));
                }*/

                return headers;
            }


        };


        // Adding request to request queue
        jsonObjReq.setRetryPolicy(new RetryPolicy() {
            @Override
            public int getCurrentTimeout() {
                return 50000;
            }

            @Override
            public int getCurrentRetryCount() {
                return 50000;
            }

            @Override
            public void retry(VolleyError error) throws VolleyError {

            }
        });
        queue.add(jsonObjReq);
    }

    private void hideStatusBar() {
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN);
    }


}
