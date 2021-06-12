package com.gogrocery.view;

import androidx.appcompat.app.AppCompatActivity;
import androidx.databinding.DataBindingUtil;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

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
import com.gogrocery.databinding.ActivityPhoneRegistrationBinding;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class PhoneRegistration extends AppCompatActivity {
ActivityPhoneRegistrationBinding phoneRegistrationBinding;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        phoneRegistrationBinding= DataBindingUtil.setContentView(this,R.layout.activity_phone_registration);
        initView();
        setUpOnClick();
    }
    private void initView(){

    }
    private void setUpOnClick(){
       phoneRegistrationBinding.btnSignup.setOnClickListener(v->{
           Intent i = new Intent(PhoneRegistration.this, OtpCheck.class);
           startActivity(i);
           finish();
       });
    }

    private void validation() {
        String mobile = phoneRegistrationBinding.edtMobileNumber.getText().toString();
        if ("".equals(mobile)) {
            phoneRegistrationBinding.tilmobileno.setError(getString(R.string.error_msg_enter_mobile_no));
        } else {

            try {
                requestRegisterPhn( "+971"  + mobile);
            } catch (Exception e) {
                e.printStackTrace();
            }
            //requestRegisterNew(name, address, mobile, email, password);
        }
    }

    private void requestRegisterPhn(String mobile) {
        phoneRegistrationBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        JSONObject mJsonObject = new JSONObject();
        try {
            mJsonObject.put("phone", mobile);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        System.out.println("Response : PhoneRegistration : requestRegisterPhn : param : " + mJsonObject);


        JsonObjectRequest mJsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.SIGN_UP, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        phoneRegistrationBinding.progressSpinKitView.setVisibility(View.GONE);
                        Gson gson = new Gson();
                        LoginModel mLoginModel = gson.fromJson(response.toString(), LoginModel.class);
                        if (mLoginModel != null) {

                            String responseString = gson.toJson(mLoginModel);
                            System.out.println("Response : PhoneRegistration : requestRegisterPhn : " + responseString);
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
                            System.out.println("Response : PhoneRegistration : requestRegisterPhn : null : ");
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                phoneRegistrationBinding.progressSpinKitView.setVisibility(View.GONE);
                try {
                    String responseBody = new String(error.networkResponse.data, "utf-8");
                    JSONObject data = new JSONObject(responseBody);

                    String message = data.getString("message");
                    Constants.showToastInMiddle(getApplicationContext(), message);

                    //Toast.makeText(getApplicationContext(), message, Toast.LENGTH_LONG).show();
                } catch (Exception ee) {
                    System.out.println("PhoneRegistration : requestRegisterPhn : onErrorResponse : " + ee);
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