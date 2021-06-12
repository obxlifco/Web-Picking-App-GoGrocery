package com.gogrocery.view;

import android.content.Intent;
import androidx.databinding.DataBindingUtil;
import android.net.Uri;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Build;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.view.Window;
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
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityForgetPasswordDeepLinkPageBinding;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class ForgetPasswordDeepLinkPage extends AppCompatActivity {

    private ActivityForgetPasswordDeepLinkPageBinding mActivityForgetPasswordDeepLinkPageBinding;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityForgetPasswordDeepLinkPageBinding = DataBindingUtil.setContentView(this, R.layout.activity_forget_password_deep_link_page);
hideStatusBarColor();
        Intent intent = getIntent();
        String action = intent.getAction();
        Uri data = intent.getData();


        mActivityForgetPasswordDeepLinkPageBinding.ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
        mActivityForgetPasswordDeepLinkPageBinding.btnSubmit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (mActivityForgetPasswordDeepLinkPageBinding.edtNewPassword.getText().toString().isEmpty()) {
                    mActivityForgetPasswordDeepLinkPageBinding.edtCurrentPassword.setError( getString(R.string.error_msg_enter_new_password));
                } else if (mActivityForgetPasswordDeepLinkPageBinding.edtConfirmNewPassword.getText().toString().isEmpty()) {
                    mActivityForgetPasswordDeepLinkPageBinding.edtCurrentPassword.setError( getString(R.string.error_msg_enter_confirm_password));
                } else if (mActivityForgetPasswordDeepLinkPageBinding.edtCurrentPassword.getText().toString().contains(" ")) {
                    mActivityForgetPasswordDeepLinkPageBinding.edtCurrentPassword.setError( getString(R.string.error_msg_space_not_allowed));
                } else if (mActivityForgetPasswordDeepLinkPageBinding.edtNewPassword.getText().toString().contains(" ")) {
                    mActivityForgetPasswordDeepLinkPageBinding.edtNewPassword.setError( getString(R.string.error_msg_space_not_allowed));
                } else if (mActivityForgetPasswordDeepLinkPageBinding.edtConfirmNewPassword.getText().toString().contains(" ")) {
                    mActivityForgetPasswordDeepLinkPageBinding.edtConfirmNewPassword.setError( getString(R.string.error_msg_space_not_allowed));
                } else {
                    try {
                        requestChangePassword(data.toString().split("/reset-password/")[1]);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            }
        });


        mActivityForgetPasswordDeepLinkPageBinding.edtNewPassword.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if (s.toString().contains(" ")) {
                    Constants.showToastInMiddle(getApplicationContext(), getString(R.string.error_msg_space_not_allowed));
                }
            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });

        mActivityForgetPasswordDeepLinkPageBinding.edtConfirmNewPassword.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if (s.toString().contains(" ")) {
                    Constants.showToastInMiddle(getApplicationContext(), getString(R.string.error_msg_space_not_allowed));
                }
            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });

    }


    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }
    public void requestChangePassword(String argPincode) throws JSONException {
        if (Constants.isInternetConnected(ForgetPasswordDeepLinkPage.this)) {
            mActivityForgetPasswordDeepLinkPageBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

            JSONObject mJsonObject = new JSONObject();
            mJsonObject.put("pin_code", argPincode);
            mJsonObject.put("new_password", mActivityForgetPasswordDeepLinkPageBinding.edtNewPassword.getText().toString());
            mJsonObject.put("confirm_password", mActivityForgetPasswordDeepLinkPageBinding.edtConfirmNewPassword.getText().toString());

            System.out.println("Rahul : ForgetPasswordDeepLinkPage : requestChangePassword : mJsonObject : " + mJsonObject);
            JsonObjectRequest mJsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                    Constants.BASE_URL + Constants.API_METHODS.CONFIRM_PASSWORD, mJsonObject,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            System.out.println("Rahul : ForgetPasswordDeepLinkPage : requestChangePassword : response : " + response);
                            mActivityForgetPasswordDeepLinkPageBinding.progressSpinKitView.setVisibility(View.GONE);

                            if (response != null) {
                                try {
                                    if (response.getString("status").equals("200")) {
                                        Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();


                                    } else {
                                        Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();
                                    }
                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }

                                Intent i = new Intent(ForgetPasswordDeepLinkPage.this, LoginActivity.class);
                                startActivity(i);
                                finish();

                            } else {

                            }
                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {
                    mActivityForgetPasswordDeepLinkPageBinding.progressSpinKitView.setVisibility(View.GONE);
                    System.out.println("Rahul : ForgetPasswordDeepLinkPage : requestChangePassword : VolleyError : " + error.toString());
                    //  Toast.makeText(getApplicationContext(), "Enter Valid Credentials", Toast.LENGTH_LONG).show();
                }
            }) {
                @Override
                public Map<String, String> getHeaders() throws AuthFailureError {
                    HashMap<String, String> headers = new HashMap<String, String>();
                    headers.put("Content-Type", "application/json");
              /*  headers.put(Constants.VARIABLES.WAREHOUSE_KEY, new SharedPreferenceManager(getApplicationContext()).getWarehouseId());
                headers.put("Authorization", "Token " + new SharedPreferenceManager(getApplicationContext()).getUserProfileDetail("token"));*/
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
        } else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }
}
