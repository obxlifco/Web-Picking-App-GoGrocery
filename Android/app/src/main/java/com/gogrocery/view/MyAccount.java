package com.gogrocery.view;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;

import androidx.core.content.ContextCompat;
import androidx.databinding.DataBindingUtil;
import androidx.appcompat.app.AppCompatActivity;

import android.content.res.Configuration;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;

import com.afollestad.materialdialogs.MaterialDialog;
import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.facebook.login.LoginManager;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Models.MyAccountModel.MyAccountModel;
import com.gogrocery.Models.MyCardList.CardListModel;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityMyAccountBinding;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

public class MyAccount extends AppCompatActivity implements View.OnClickListener {


    private ActivityMyAccountBinding myAccountBinding;
    private SharedPreferenceManager mSharedPreferenceManager;
    private String responsePass = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        myAccountBinding = DataBindingUtil.setContentView(this, R.layout.activity_my_account);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
/*        if (Constants.VARIABLES.CART_COUNT > 0) {
            myAccountBinding.badgeNotification.setVisibility(View.VISIBLE);
            myAccountBinding.badgeNotification.setText("" + Constants.VARIABLES.CART_COUNT);
        } else {
            myAccountBinding.badgeNotification.setVisibility(View.GONE);
        }*/
/*        Intent intent =
                null;
        try {
            intent = new PlaceAutocomplete.IntentBuilder(PlaceAutocomplete.MODE_OVERLAY)
                    .build(MyAccount.this);
        } catch (GooglePlayServicesRepairableException e) {
            e.printStackTrace();
        } catch (GooglePlayServicesNotAvailableException e) {
            e.printStackTrace();
        }
        startActivityForResult(intent, 101);*/

        if(Constants.VARIABLES.USER_LANG_CODE.equals("en")){
        /*    iv_back.setImageDrawable(getResources().getDrawable(R.drawable.ic_back));
            ivBtn_editProfile.setImageDrawable(getResources().getDrawable(R.drawable.ic_edit));
            iv_currency_more.setImageDrawable(getResources().getDrawable(R.drawable.ic_nav_menu_right));
            iv_delivery_address_rtl.setImageDrawable(getResources().getDrawable(R.drawable.ic_nav_menu_right));
            iv_all_order_rtl.setImageDrawable(getResources().getDrawable(R.drawable.ic_nav_menu_right));
            iv_language_more.setImageDrawable(getResources().getDrawable(R.drawable.ic_nav_menu_right));
            iv_notifi.setImageDrawable(getResources().getDrawable(R.drawable.ic_nav_menu_right));
            iv_offerIcon.setImageDrawable(getResources().getDrawable(R.drawable.ic_nav_offer));*/
            myAccountBinding.tvLanguage.setText("("+getResources().getString(R.string.eng)+")");
        }else{
   /*         iv_back.setImageDrawable(getResources().getDrawable(R.drawable.ic_back_rtl));
            ivBtn_editProfile.setImageDrawable(getResources().getDrawable(R.drawable.ic_edit_rtl));
            iv_currency_more.setImageDrawable(getResources().getDrawable(R.drawable.ic_nav_menu_right_rtl));
            iv_delivery_address_rtl.setImageDrawable(getResources().getDrawable(R.drawable.ic_nav_menu_right_rtl));
            iv_all_order_rtl.setImageDrawable(getResources().getDrawable(R.drawable.ic_nav_menu_right_rtl));
            iv_language_more.setImageDrawable(getResources().getDrawable(R.drawable.ic_nav_menu_right_rtl));
            iv_notifi.setImageDrawable(getResources().getDrawable(R.drawable.ic_nav_menu_right_rtl));
            iv_offerIcon.setImageDrawable(getResources().getDrawable(R.drawable.ic_nav_offer_rtl));*/
            myAccountBinding.tvLanguage.setText("("+getResources().getString(R.string.eng)+")");
        }

        setListners();
hideStatusBarColor();

    }

    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        try {
            requestMyProfile();
            requestMyCardList();
        } catch (JSONException e) {
            e.printStackTrace();
        }
/*
        if (Constants.VARIABLES.CART_COUNT > 0) {
            myAccountBinding.badgeNotification.setVisibility(View.VISIBLE);
            myAccountBinding.badgeNotification.setText("" + Constants.VARIABLES.CART_COUNT);
        } else {
            myAccountBinding.badgeNotification.setVisibility(View.GONE);
        }*/
    }

    private void setListners() {

        myAccountBinding.ivBack.setOnClickListener(this);
        myAccountBinding.rlMyAddress.setOnClickListener(this);
        myAccountBinding.rlLogout.setOnClickListener(this);
        myAccountBinding.rlMyOrder.setOnClickListener(this);
        myAccountBinding.ivRight.setOnClickListener(this);
        myAccountBinding.rlChangesPassword.setOnClickListener(this);
        myAccountBinding.rlMyDetails.setOnClickListener(this);
        myAccountBinding.rlMyPaymentMethod.setOnClickListener(this);
      /*  myAccountBinding.rlNotificationPreferences.setOnClickListener(this);*/
        myAccountBinding.rlLogout.setOnClickListener(this);
        myAccountBinding.rlLanguage.setOnClickListener(this);
    /*    myAccountBinding.rlMyWalletCards.setOnClickListener(this);
        myAccountBinding.rlMySaveList.setOnClickListener(this);
        myAccountBinding.rlProductSubstitute.setOnClickListener(this);
*/

    }



    public void requestMyProfile() throws JSONException {
        if (Constants.isInternetConnected(MyAccount.this)) {
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            System.out.println("Rahul : MyAccount : requestMyProfile : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
            JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                    Constants.BASE_URL + Constants.API_METHODS.MY_PROFILE, null,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {


                            System.out.println("Rahul : MyAccount : requestMyProfile : mJsonObject : " + response);

                            responsePass = response.toString();
                            setPageUI(response.toString());

                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {

                    System.out.println("Rahul : MyAccount : requestMyProfile : VolleyError : " + error.toString());
                }
            }) {
                @Override
                public Map<String, String> getHeaders() throws AuthFailureError {
                    HashMap<String, String> headers = new HashMap<String, String>();
                    headers.put("Content-Type", "application/json");
                    headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));

                    return headers;
                }


            };


            // Adding request to request queue
            queue.add(jsonObjReq);
        } else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }


    private void setPageUI(String argResponse) {
        Gson mGson = new Gson();
        MyAccountModel myAccountModel = mGson.fromJson(argResponse, MyAccountModel.class);

        myAccountBinding.tvUsername.setText(myAccountModel.getData().getFirstName() + myAccountModel.getData().getLastName());
        if(myAccountModel.getData().getPhone()!=null&&!myAccountModel.getData().getPhone().isEmpty()){
            myAccountBinding.tvNumber.setText(myAccountModel.getData().getPhone());
            myAccountBinding.tvNumber.setVisibility(View.VISIBLE);
        }else {
            myAccountBinding.tvNumber.setVisibility(View.GONE);
        }

       // myAccountBinding.tvEmailAddress.setText(myAccountModel.getData().getEmail());

/*
        Glide.with(getApplicationContext())
                .load("")
                .listener(new RequestListener<Drawable>() {

                    @Override
                    public boolean onLoadFailed(@Nullable GlideException e, Object model, Target<Drawable> target, boolean isFirstResource) {
                        supportStartPostponedEnterTransition();
                        new Handler().postDelayed(new Runnable() {
                            @Override
                            public void run() {
                                Glide.with(getApplicationContext())
                                        .load(R.drawable.)
                                        .into(mActivityUserProfileBinding.contentUserProfile.profileImage);
                            }
                        },1000);


                        return false;
                    }

                    @Override
                    public boolean onResourceReady(Drawable resource, Object model, Target<Drawable> target, DataSource dataSource, boolean isFirstResource) {
                        supportStartPostponedEnterTransition();
                        return false;
                    }
                })
                .into(myAccountBinding.civProfilePic);*/


    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.ivBack:
                finish();
                break;
            case R.id.ivRight:
                Intent ivEditProfile = new Intent(MyAccount.this, AccountSettings.class);
                ivEditProfile.putExtra("profile_data", responsePass);
                startActivity(ivEditProfile);
                break;
            case R.id.rl_changesPassword:
                myAccountBinding.rlChangesPassword.setBackgroundResource(R.drawable.green_round_side);
                myAccountBinding.rlLanguage.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlMyOrder.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlLogout.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlMyAddress.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlMyDetails.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlMyPaymentMethod.setBackgroundResource(R.drawable.gray_round_side);
                Intent ivSearch = new Intent(MyAccount.this, ChangePassword.class);
                startActivity(ivSearch);
                break;
            case R.id.rl_myAddress:
                myAccountBinding.rlMyAddress.setBackgroundResource(R.drawable.green_round_side);

                myAccountBinding.rlMyOrder.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlLogout.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlChangesPassword.setBackgroundResource(R.drawable.gray_round_side);

                myAccountBinding.rlMyPaymentMethod.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlLanguage.setBackgroundResource(R.drawable.gray_round_side);
                Intent ivCart = new Intent(MyAccount.this, MyAddresses.class);
                ivCart.putExtra("from", "my_account");
                startActivity(ivCart);
                break;
            case R.id.rl_myOrder:
                myAccountBinding.rlMyAddress.setBackgroundResource(R.drawable.gray_round_side);

                myAccountBinding.rlMyOrder.setBackgroundResource(R.drawable.green_round_side);
                myAccountBinding.rlLogout.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlChangesPassword.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlLanguage.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlMyPaymentMethod.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlLanguage.setBackgroundResource(R.drawable.gray_round_side);
                Intent rlMyOrders = new Intent(MyAccount.this, MyOrders.class);
                startActivity(rlMyOrders);
                break;
           case R.id.rl_language:
               myAccountBinding.rlMyAddress.setBackgroundResource(R.drawable.gray_round_side);
               myAccountBinding.rlChangesPassword.setBackgroundResource(R.drawable.gray_round_side);
               myAccountBinding.rlLanguage.setBackgroundResource(R.drawable.green_round_side);
               myAccountBinding.rlLogout.setBackgroundResource(R.drawable.gray_round_side);
               myAccountBinding.rlChangesPassword.setBackgroundResource(R.drawable.gray_round_side);
               myAccountBinding.rlMyOrder.setBackgroundResource(R.drawable.gray_round_side);
               myAccountBinding.rlMyPaymentMethod.setBackgroundResource(R.drawable.gray_round_side);
               myAccountBinding.rlMyDetails.setBackgroundResource(R.drawable.gray_round_side);
               showChangeLanguageDialog();
                break;

            case R.id.rl_myDetails:
                myAccountBinding.rlMyAddress.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlChangesPassword.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlMyDetails.setBackgroundResource(R.drawable.green_round_side);
                myAccountBinding.rlLogout.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlChangesPassword.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlMyOrder.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlMyPaymentMethod.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlLanguage.setBackgroundResource(R.drawable.gray_round_side);
                Intent ivProfile = new Intent(MyAccount.this, AccountSettings.class);
                ivProfile.putExtra("profile_data", responsePass);
                startActivity(ivProfile);
                break;
            case R.id.rl_myPaymentMethod:
                myAccountBinding.rlMyAddress.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlChangesPassword.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlMyPaymentMethod.setBackgroundResource(R.drawable.green_round_side);
                myAccountBinding.rlLogout.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlChangesPassword.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlMyOrder.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlLanguage.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlMyDetails.setBackgroundResource(R.drawable.gray_round_side);
                Intent rlMyWalletCards = new Intent(MyAccount.this, PaymentCard.class);
                startActivity(rlMyWalletCards);
                break;
          /*     case R.id.rlAccountSettings:
                Intent rlAccountSettings = new Intent(MyAccount.this, AccountSettings.class);
                rlAccountSettings.putExtra("profile_data", responsePass);
                startActivity(rlAccountSettings);
                break;*/
            case R.id.rlProductSubstitute:
                Intent rlProductSubstitute = new Intent(MyAccount.this, ProductSubstitutions.class);
                startActivity(rlProductSubstitute);
                break;
            case R.id.rl_logout:
                myAccountBinding.rlMyAddress.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlLanguage.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlMyDetails.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlMyOrder.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlLogout.setBackgroundResource(R.drawable.green_round_side);
                myAccountBinding.rlChangesPassword.setBackgroundResource(R.drawable.gray_round_side);
                myAccountBinding.rlMyOrder.setBackgroundResource(R.drawable.gray_round_side);
                showLogoutPopup();
                break;

        }
    }

    private void showLogoutPopup() {
        new MaterialDialog.Builder(this)
                .title(getResources().getString(R.string.dialogTitle_logout))
                .content(getResources().getString(R.string.dialogMessage_logout))
                .positiveText(getResources().getString(R.string.dialogPositiveButtonText_logout))
                .positiveColor(ContextCompat.getColor(this, R.color.app_red_clr))
                .negativeText(getResources().getString(R.string.dialogPositiveButtonText_cancel))
                .negativeColor(ContextCompat.getColor(this, R.color.Title))
                .onPositive((dialog, which) -> {
                    try {
                        requestLogout();
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                })
                .onNegative((dialog, which) -> {
                    dialog.dismiss();
                }).show();
    }


    public void requestLogout() throws JSONException {
        if (Constants.isInternetConnected(MyAccount.this)) {
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            JSONObject mJsonObject = new JSONObject();
            mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));
            mJsonObject.put("ip_address", "");
            myAccountBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            System.out.println("Rahul : MyAccount : requestMyProfile : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
            JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                    Constants.BASE_URL_SUBSTITUTE + Constants.API_METHODS.LOGOUT, mJsonObject,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            myAccountBinding.progressSpinKitView.setVisibility(View.GONE);
                            try {
                                if (response.getInt("status") == 1) {

                                    Intent rlLogout = new Intent(MyAccount.this, LoginActivity.class);
                                    if (Constants.mGoogleSignInClient != null) {
                                        Constants.mGoogleSignInClient.signOut();
                                    }

                                    LoginManager.getInstance().logOut();
                                    mSharedPreferenceManager.logoutUser();
                                    startActivity(rlLogout);
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }

                            System.out.println("Rahul : MyAccount : requestLogout : mJsonObject : " + response);


                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {
                    myAccountBinding.progressSpinKitView.setVisibility(View.GONE);
                    System.out.println("Rahul : MyAccount : requestLogout : VolleyError : " + error.toString());
                }
            }) {
                @Override
                public Map<String, String> getHeaders() throws AuthFailureError {
                    HashMap<String, String> headers = new HashMap<String, String>();
                    headers.put("Content-Type", "application/json");
                    headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));

                    return headers;
                }


            };


            // Adding request to request queue
            queue.add(jsonObjReq);
        } else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }


    private void showChangeLanguageDialog(){
        int checkedItem = -1;
        final String [] listItem = {
                "English","عربى"
        };
        if(Constants.VARIABLES.USER_LANG_CODE.equals("en")){
            checkedItem = 0;
        }else{
            checkedItem=1;
        }

        AlertDialog.Builder mbuilder = new AlertDialog.Builder(MyAccount.this);
        mbuilder.setTitle(getResources().getString(R.string.choose_your_language));

        mbuilder.setSingleChoiceItems(listItem, checkedItem, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {


                if(i== 0){

                    myAccountBinding.tvLanguage.setText("(ENG)");
                    mSharedPreferenceManager.setLocalLanguage("en");
                    setLocale("en");
                    //  recreate();
                }else {

                    myAccountBinding.tvLanguage.setText("("+"عربى"+")");
                    Constants.VARIABLES.USER_LANG_CODE= "ar";
                    mSharedPreferenceManager.setLocalLanguage("ar");
                    setLocale("ar");
                    //   recreate();
                }
                dialogInterface.dismiss();
            }
        });
        AlertDialog mDialog = mbuilder.create();
        mDialog.show();
    }

    private void setLocale(String lang) {

        if (lang.equalsIgnoreCase(""))
            return;
        Locale myLocale = new Locale(lang);//Set Selected Locale

        mSharedPreferenceManager.setLocalLanguage(lang);

        Locale.setDefault(myLocale);//set new locale as default

        Configuration config = new Configuration();//get Configuration
        config.locale = myLocale;//set config locale as selected locale
        getBaseContext().getResources().updateConfiguration(config, getBaseContext().getResources().getDisplayMetrics());
        restartApp();


    }

    public void requestMyCardList() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        //findViewById(R.id.progressSpinKitView).setVisibility(View.VISIBLE);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.PAYMENT_REQUEST_SI_CHARGES_LIST, null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : DeliveryDetails : requestCardList : response : " + response.toString());
                        findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                        try {
                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                // Constants.VARIABLES.SELECTED_ADDRESS_ID="";

                                Gson mGson = new Gson();
                                CardListModel mCardListModel = mGson.fromJson(response.toString(), CardListModel.class);
                                System.out.println("Rahul : DeliveryDetail : requestCardList : mCardListModel: " + mGson.toJson(mCardListModel));

                                if (mCardListModel.getCardList().size() > 0) {
                              myAccountBinding.rlMyPaymentMethod.setVisibility(View.VISIBLE);

                                }else {

                                    myAccountBinding.rlMyPaymentMethod.setVisibility(View.GONE);
                                    //Toast.makeText(getApplicationContext(), "No Card added in your list", Toast.LENGTH_LONG).show();
                                }
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                System.out.println("Rahul : MapLocationSelectionUpdate : requestEmptyCart : VolleyError : " + error.toString());
            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                if (mSharedPreferenceManager.isLoggedIn()) {
                    headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                }

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




    private void restartApp(){


        try{
            SharedPreferenceManager mSharedPreferenceManager= new SharedPreferenceManager(getApplicationContext());
            Intent mStartActivity = new Intent(MyAccount.this, SelectCategory.class);
            mStartActivity.putExtra("latitude", mSharedPreferenceManager.getLatitude());
            mStartActivity.putExtra("longitude", mSharedPreferenceManager.getLongitude());
            mStartActivity.putExtra("select_category_list","");
            mStartActivity.putExtra("from_where","start");


            this.startActivity(mStartActivity);
            this.finishAffinity();
        }catch (Exception e){
            e.printStackTrace();
        }
    }




}
