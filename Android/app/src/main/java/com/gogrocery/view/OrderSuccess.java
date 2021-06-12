package com.gogrocery.view;

import android.content.Intent;

import androidx.databinding.DataBindingUtil;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityOrderSuccessBinding;
import com.google.firebase.analytics.FirebaseAnalytics;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class OrderSuccess extends AppCompatActivity {

    private ActivityOrderSuccessBinding mActivityOrderSuccessBinding;
    private DatabaseHandler mDatabaseHandler;
    private JSONObject order_summary;
    private SharedPreferenceManager mSharedPreferenceManager;
    private JSONObject delivery_address = new JSONObject();
    String orderSuccess = "";
    private FirebaseAnalytics mFirebaseAnalytics;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityOrderSuccessBinding = DataBindingUtil.setContentView(this, R.layout.activity_order_success);
        mFirebaseAnalytics = FirebaseAnalytics.getInstance(this);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        hideStatusBarColor();
        try {


            mDatabaseHandler = new DatabaseHandler(getApplicationContext());
            mDatabaseHandler.deleteAllRecord();

            if (getIntent().getExtras().getString("status").equalsIgnoreCase("Success")) {
                orderSuccess = "1";

            } else {
                orderSuccess = "0";
                mActivityOrderSuccessBinding.ivStatusSuccess.setVisibility(View.GONE);
                mActivityOrderSuccessBinding.ivStatusFailure.setVisibility(View.VISIBLE);
                mActivityOrderSuccessBinding.tvOrderStatusMessage.setText(getResources().getString(R.string.your_order_has_been_failed));
                mActivityOrderSuccessBinding.tvOrderStatusMessage.setTextColor(getResources().getColor(R.color.app_red_clr));
                mActivityOrderSuccessBinding.tvOrderSuccessMessage.setVisibility(View.GONE);
                mActivityOrderSuccessBinding.btnContinueShopping.setVisibility(View.VISIBLE);
                mActivityOrderSuccessBinding.btnContinueShopping.setText(getResources().getString(R.string.retry_payment));
                mActivityOrderSuccessBinding.btnContinueShopping.setTextColor(getResources().getColor(R.color.black));

                mActivityOrderSuccessBinding.btnContinueShopping.setBackgroundResource(R.drawable.my_order_payment_status_failed_bg);


            }

            String order_id = getIntent().getExtras().getString("order_id");
            mActivityOrderSuccessBinding.tvOrderId.setText(getResources().getString(R.string.your_order_id) + order_id);

            order_summary = new JSONObject(getIntent().getExtras().getString("order_summary"));
            delivery_address = new JSONObject(getIntent().getExtras().getString("delivery_address"));


       /*     mActivityOrderSuccessBinding.tvSubtotal.setText(order_summary.getString("subtotal"));
            mActivityOrderSuccessBinding.tvDeliveryCharges.setText(order_summary.getString("delivery"));
            if (order_summary.getString("coupon_discount").contains(Constants.VARIABLES.CURRENT_CURRENCY)) {
                mActivityOrderSuccessBinding.tvDiscount.setText(order_summary.getString("coupon_discount"));
            } else {
                mActivityOrderSuccessBinding.tvDiscount.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + order_summary.getString("coupon_discount"));
            }*/

           /* if(Double.parseDouble(mActivityOrderSuccessBinding.tvDiscount.getText().toString().replace("AED","").trim())>0)
            {
                mActivityOrderSuccessBinding.tvDiscount.setTextColor(getApplicationContext().getResources().getColor(R.color.app_red_clr));
            }

            mActivityOrderSuccessBinding.tvDiscount.setText(order_summary.getString("discount"));*/
/*
            mActivityOrderSuccessBinding.tvEstimatedTax.setText(order_summary.getString("tax"));
            mActivityOrderSuccessBinding.tvTotalSumPrice.setText(order_summary.getString("final_total"));
*/


            System.out.println("Rahul : OrderSuccess : loyalty_amount : " + order_summary.getString("loyalty_amount"));
/*            if (order_summary.getString("loyalty_amount").equals(Constants.VARIABLES.CURRENT_CURRENCY+" 0.00")) {
                mActivityOrderSuccessBinding.llLoyaltyPoints.setVisibility(View.GONE);
            } else if (order_summary.getString("loyalty_amount").equals("0.00")) {
                mActivityOrderSuccessBinding.llLoyaltyPoints.setVisibility(View.GONE);
            } else if (order_summary.getString("loyalty_amount").equals(Constants.VARIABLES.CURRENT_CURRENCY+" 0.0")) {
                mActivityOrderSuccessBinding.llLoyaltyPoints.setVisibility(View.GONE);
            } else {
                mActivityOrderSuccessBinding.llLoyaltyPoints.setVisibility(View.VISIBLE);
                mActivityOrderSuccessBinding.tvAppliedLoyaltyAmount.setText(order_summary.getString("loyalty_amount"));
            }*/


          /*  if (order_summary.getString("coupon_discount").equals("0.00")) {
                mActivityOrderSuccessBinding.tvDiscount.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " 0.00" );
            } else {
                mActivityOrderSuccessBinding.tvDiscount.setText(order_summary.getString("coupon_discount"));
            }*/

     /*       mActivityOrderSuccessBinding.tvName.setText(delivery_address.getString("name"));
            mActivityOrderSuccessBinding.tvAddress.setText(delivery_address.getString("address"));
            mActivityOrderSuccessBinding.tvMobileNumber.setText(delivery_address.getString("number"));*/


            mActivityOrderSuccessBinding.btnContinueShopping.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (orderSuccess.equals("0")) {
                        Intent i = new Intent(OrderSuccess.this, MyCart.class);
                        startActivity(i);
                        finish();
                    } else {

                        try {
                            requestEmptyCart();
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                       /* Intent i = new Intent(OrderSuccess.this, MainActivityNew.class);
                        startActivity(i);
                        finish();*/
                    }

                }
            });

            mActivityOrderSuccessBinding.ivBack.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (orderSuccess.equals("0")) {
                        Intent i = new Intent(OrderSuccess.this, MyCart.class);
                        startActivity(i);
                        finish();
                    } else {

                        try {
                            requestEmptyCart();
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                       /* Intent i = new Intent(OrderSuccess.this, MainActivityNew.class);
                        startActivity(i);
                        finish();*/
                    }
                   /* Intent i = new Intent(OrderSuccess.this, MainActivityNew.class);
                    startActivity(i);
                    finish();*/
                }
            });
        } catch (Exception e) {

        }
    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
        Intent i = new Intent(OrderSuccess.this, MainActivityNew.class);
        startActivity(i);
        finish();
    }


    public void requestEmptyCart() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());


        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));
        mJsonObject.put("website_id", 1);

        System.out.println("Rahul : MapLocationSelectionUpdate : requestEmptyCart : mJsonObject : " + mJsonObject.toString());

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.EMPTY_CART, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : MapLocationSelectionUpdate : requestEmptyCart : response : " + response.toString());

                        try {
                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                               // Constants.VARIABLES.SELECTED_ADDRESS_ID="";

                                new DatabaseHandler(getApplicationContext()).deleteAllRecord();
                                Intent i = new Intent(OrderSuccess.this, MainActivityNew.class);
                                startActivity(i);
                                finish();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

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

    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }
}
