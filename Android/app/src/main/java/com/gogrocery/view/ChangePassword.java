package com.gogrocery.view;

import androidx.databinding.DataBindingUtil;
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
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityChangePasswordBinding;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class ChangePassword extends AppCompatActivity {

    private ActivityChangePasswordBinding mActivityChangePasswordBinding;
View rootView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityChangePasswordBinding = DataBindingUtil.setContentView(this, R.layout.activity_change_password);
        textvalidchcek();
        rootView = this.findViewById(android.R.id.content).getRootView();
        Constants.setupUI(rootView, ChangePassword.this);
        hideStatusBarColor();
   /*     mActivityChangePasswordBinding.btnCancel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });*/
        mActivityChangePasswordBinding.ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
        mActivityChangePasswordBinding.btnSave.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (checkvalidation()) {
                    try {
                        requestChangePassword();
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            }

        });


    }


    private boolean checkvalidation(){
        boolean validated = true;
        int validationcount = 0;
        if ((mActivityChangePasswordBinding.edtCurrentPassword.getText().toString().trim().equals("")) || (mActivityChangePasswordBinding.edtCurrentPassword.getText().length() == 0)) {


            mActivityChangePasswordBinding.tilCurrentPassword.setError(getString(R.string.error_msg_enter_old_password));
            mActivityChangePasswordBinding.tilCurrentPassword.requestFocus();
            return false;
        }


        if ((mActivityChangePasswordBinding.edtNewPassword.getText().toString().trim().equals(""))) {


            mActivityChangePasswordBinding.tilNewPassword.setError(getString(R.string.error_msg_enter_new_password));
            mActivityChangePasswordBinding.tilNewPassword.requestFocus();
            return false;
        }


        if (mActivityChangePasswordBinding.edtNewPassword.getText().length()<5){
            mActivityChangePasswordBinding.tilNewPassword.setError(getString(R.string.error_msg_enter_password_lenght));
            mActivityChangePasswordBinding.tilNewPassword.requestFocus();
            return false;
        }

        if ((mActivityChangePasswordBinding.edtConfirmNewPassword.getText().toString().trim().equals("")) || (mActivityChangePasswordBinding.edtConfirmNewPassword.getText().length()<5)) {


            mActivityChangePasswordBinding.tilConfirmNewPassword.setError(getString(R.string.error_msg_enter_confirm_password));
            mActivityChangePasswordBinding.tilConfirmNewPassword.requestFocus();
            return false;
        }

  /*      else {
            validated = true;
            validationcount++;
        }*/

        if (!(mActivityChangePasswordBinding.edtNewPassword.getText().toString().trim().equals(mActivityChangePasswordBinding.edtConfirmNewPassword.getText().toString().trim()))) {


            mActivityChangePasswordBinding.tilConfirmNewPassword.setError(getString(R.string.error_msg_enter_confirm_password_match));
            mActivityChangePasswordBinding.tilConfirmNewPassword.requestFocus();
            return  false;
        }


        return validated;
    }


    private void textvalidchcek(){
        mActivityChangePasswordBinding.edtCurrentPassword.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                String result = s.toString().replaceAll(" ", "");
                if (!s.toString().equals(result)) {
                    mActivityChangePasswordBinding.edtCurrentPassword.setText(result);
                    mActivityChangePasswordBinding.edtCurrentPassword.setSelection(result.length());
                    // alert the user
                }
                mActivityChangePasswordBinding.tilCurrentPassword.setError(null);
            }
        });

        mActivityChangePasswordBinding.edtNewPassword.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                String result = s.toString().replaceAll(" ", "");
                if (!s.toString().equals(result)) {
                    mActivityChangePasswordBinding.edtNewPassword.setText(result);
                    mActivityChangePasswordBinding.edtNewPassword.setSelection(result.length());
                    // alert the user
                }
                mActivityChangePasswordBinding.tilNewPassword.setError(null);
            }
        });

        mActivityChangePasswordBinding.edtConfirmNewPassword.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                String result = s.toString().replaceAll(" ", "");
                if (!s.toString().equals(result)) {
                    mActivityChangePasswordBinding.edtConfirmNewPassword.setText(result);
                    mActivityChangePasswordBinding.edtConfirmNewPassword.setSelection(result.length());
                    // alert the user
                }
                mActivityChangePasswordBinding.tilConfirmNewPassword.setError(null);
            }
        });
    }
    public void requestChangePassword() throws JSONException {
        if (Constants.isInternetConnected(ChangePassword.this)) {
            mActivityChangePasswordBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

            JSONObject mJsonObject = new JSONObject();
            mJsonObject.put("current_password", mActivityChangePasswordBinding.edtCurrentPassword.getText().toString());
            mJsonObject.put("new_password", mActivityChangePasswordBinding.edtNewPassword.getText().toString());
            mJsonObject.put("confirm_password", mActivityChangePasswordBinding.edtConfirmNewPassword.getText().toString());

            System.out.println("Rahul : ChangePassword : requestChangePassword : mJsonObject : " + mJsonObject);
            JsonObjectRequest mJsonObjectRequest = new JsonObjectRequest(Request.Method.PUT,
                    Constants.BASE_URL + Constants.API_METHODS.CHANGE_PASSWORD, mJsonObject,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            System.out.println("Rahul : ChangePassword : requestChangePassword : response : " + response);
                            mActivityChangePasswordBinding.progressSpinKitView.setVisibility(View.GONE);

                            if (response != null) {
                                try {
                                    if (response.getString("status").equals("200")) {
                                        Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();
                                        finish();

                                    } else {
                                        Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();
                                    }
                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }

                            } else {

                            }
                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {
                    mActivityChangePasswordBinding.progressSpinKitView.setVisibility(View.GONE);
                    System.out.println("Rahul : ChangePassword : requestChangePassword : VolleyError : " + error.toString());
                    //  Toast.makeText(getApplicationContext(), "Enter Valid Credentials", Toast.LENGTH_LONG).show();
                }
            }) {
                @Override
                public Map<String, String> getHeaders() throws AuthFailureError {
                    HashMap<String, String> headers = new HashMap<String, String>();
                    headers.put("Content-Type", "application/json");
                    headers.put(Constants.VARIABLES.WAREHOUSE_KEY, new SharedPreferenceManager(getApplicationContext()).getWarehouseId());
                    headers.put("Authorization", "Token " + new SharedPreferenceManager(getApplicationContext()).getUserProfileDetail("token"));
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
            Constants.setSnackBar(ChangePassword.this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }

    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }
}
