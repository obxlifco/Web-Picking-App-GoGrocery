package com.gogrocery.view;

import androidx.appcompat.app.AppCompatActivity;
import androidx.databinding.DataBindingUtil;

import android.content.Intent;
import android.database.DatabaseUtils;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Models.LoginModel.LoginModel;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityOtpCheckBinding;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class OtpCheck extends AppCompatActivity {
ActivityOtpCheckBinding activityOtpCheckBinding;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        activityOtpCheckBinding= DataBindingUtil.setContentView(this,R.layout.activity_otp_check);
        //getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_HIDDEN);
        initView();
        setUpOnClick();
    }

    private void initView(){

    }
    private void setUpOnClick(){
        activityOtpCheckBinding.btnSignup.setOnClickListener(v->{
            Intent i = new Intent(OtpCheck.this, IntroStepOne.class);
            startActivity(i);
            finish();
        });
    }

    private void validation() {
        String otp = activityOtpCheckBinding.pinview.getValue();
        if ("".equals(otp)) {
            Toast.makeText(this, getString(R.string.error_msg_enter_otp), Toast.LENGTH_LONG).show();
        } else {

            try {
                requestRegisterOTP( "+971"  + otp);
            } catch (Exception e) {
                e.printStackTrace();
            }
            //requestRegisterNew(name, address, mobile, email, password);
        }
    }

    private void requestRegisterOTP(String otp) {
        activityOtpCheckBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        JSONObject mJsonObject = new JSONObject();
        try {
            mJsonObject.put("otp", otp);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        System.out.println("Response : OtpCheck : requestRegisterOTP : param : " + mJsonObject);


        JsonObjectRequest mJsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.SIGN_UP, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        activityOtpCheckBinding.progressSpinKitView.setVisibility(View.GONE);
                        Gson gson = new Gson();
                        LoginModel mLoginModel = gson.fromJson(response.toString(), LoginModel.class);
                        if (mLoginModel != null) {

                            String responseString = gson.toJson(mLoginModel);
                            System.out.println("Response : OtpCheck : requestRegisterOTP : " + responseString);
                            if (mLoginModel != null) {
                                if (mLoginModel.getStatus() == Integer.parseInt(Constants.VARIABLES.STATUS_SUCESS_CODE)) {

                                } else {
                                    Constants.showToastInMiddle(getApplicationContext(), mLoginModel.getMessage());
                                    // Toast.makeText(getApplicationContext(), mLoginModel.getMessage(), Toast.LENGTH_LONG).show();
                                }

                            } else {
                                //Toast.makeText(getApplicationContext(), "Enter Valid Credentials", Toast.LENGTH_LONG).show();
                            }
                        } else {
                            System.out.println("Response : OtpCheck : requestRegisterOTP : null : ");
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                activityOtpCheckBinding.progressSpinKitView.setVisibility(View.GONE);
                try {
                    String responseBody = new String(error.networkResponse.data, "utf-8");
                    JSONObject data = new JSONObject(responseBody);

                    String message = data.getString("message");
                    Constants.showToastInMiddle(getApplicationContext(), message);

                    //Toast.makeText(getApplicationContext(), message, Toast.LENGTH_LONG).show();
                } catch (Exception ee) {
                    System.out.println("OtpCheck : requestRegisterOTP : onErrorResponse : " + ee);
                }
                if (error.networkResponse.statusCode == 417) {

                    //Toast.makeText(getApplicationContext(), "Email / Mobile already exist", Toast.LENGTH_SHORT).show();
                }

            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("DEVICEID", Constants.getDeviceId(getApplicationContext()));
                return headers;
            }


        };


        // Adding request to request queue
        mJsonObjectRequest.setRetryPolicy(new RetryPolicy() {
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
        queue.add(mJsonObjectRequest);
    }
}