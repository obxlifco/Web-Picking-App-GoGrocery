package com.gogrocery.view;

import android.content.DialogInterface;
import android.content.Intent;

import androidx.appcompat.app.AlertDialog;
import androidx.databinding.DataBindingUtil;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Build;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
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
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityForgetPasswordBinding;
import com.gogrocery.helper.LoadingDialog;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class ForgetPassword extends AppCompatActivity {

View rootView;
    private ActivityForgetPasswordBinding mActivityForgetPasswordBinding;
    private SharedPreferenceManager mSharedPreferenceManager;
    LoadingDialog loadingDialog;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityForgetPasswordBinding = DataBindingUtil.setContentView(this, R.layout.activity_forget_password);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        loadingDialog = new LoadingDialog(this);

        rootView = this.findViewById(android.R.id.content).getRootView();
        Constants.setupUI(rootView, ForgetPassword.this);
        hideStatusBarColor();
        mActivityForgetPasswordBinding.ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
       /* mActivityForgetPasswordBinding.tvSignIn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(ForgetPassword.this, LoginActivity.class);
                startActivity(i);
            }
        });*/

        mActivityForgetPasswordBinding.btnResendLink.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {

                    if (mActivityForgetPasswordBinding.edtEmail.getText().toString().isEmpty()) {
                        mActivityForgetPasswordBinding.edtEmail.setError(getString(R.string.error_msg_enter_email));
                    } else  if(!Constants.emailPatternValidtion(mActivityForgetPasswordBinding.edtEmail.getText().toString())){
                        mActivityForgetPasswordBinding.edtEmail.setError(getString(R.string.error_msg_enter_valid_email));
                    }else {
                        mActivityForgetPasswordBinding.btnResendLink.setClickable(false);
                        if(Constants.isInternetConnected(ForgetPassword.this)) {

                            requestForgotPassword();
                        }else {
                            Constants.setSnackBar(ForgetPassword.this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
                        }

                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });


        mActivityForgetPasswordBinding.edtEmail.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if (s.toString().contains(" ")) {
                    Constants.showToastInMiddle(getApplicationContext(), getString(R.string.error_msg_space_not_allowed));               }
            }

            @Override
            public void afterTextChanged(Editable s) {
                String result = s.toString().replaceAll(" ", "");
                if (!s.toString().equals(result)) {
                    mActivityForgetPasswordBinding.edtEmail.setText(result);
                    mActivityForgetPasswordBinding.edtEmail.setSelection(result.length());
                    // alert the user
                }
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
    public void requestForgotPassword() throws JSONException {
        loadingDialog.showDialog();

        //   mActivityForgetPasswordBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("email", mActivityForgetPasswordBinding.edtEmail.getText().toString().toLowerCase());

        System.out.println("Rahul : ForgetPassword : requestLogin : " + mJsonObject);
        JsonObjectRequest mJsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.FORGOT_PASSWORD, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : ForgetPassword : requestLogin : response: " + response);
                        // mActivityForgetPasswordBinding.progressSpinKitView.setVisibility(View.GONE);
                        loadingDialog.hideDialog();


                        if (response != null) {
                            try {
                                if (response.getString("status").equals("1")) {
                                    mActivityForgetPasswordBinding.btnResendLink.setClickable(false);
                                    //  Constants.showToastInMiddle(getApplicationContext(), response.getString("message"));
                                    showDailog(response.getString("message"));


                                } else {
                                    mActivityForgetPasswordBinding.btnResendLink.setClickable(true);
                                    showErrorDailog(response.getString("message"));
                                    //  Constants.showToastInMiddle(getApplicationContext(), response.getString("message"));
                                    //Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();
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
                loadingDialog.hideDialog();
                // mActivityForgetPasswordBinding.progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : ForgetPassword : requestLogin : VolleyError : " + error.toString());
                //  Toast.makeText(getApplicationContext(), "Enter Valid Credentials", Toast.LENGTH_LONG).show();
            }
        })

        {
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


    private void showDailog(String message){
        new AlertDialog.Builder(ForgetPassword.this)
                .setTitle(getResources().getString(R.string.forgetpass_page))
                .setMessage(message)
                .setPositiveButton(getResources().getString(R.string.ok), new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        finish();
                    }
                })

                .show();
    }


    private void showErrorDailog(String message){
        new AlertDialog.Builder(ForgetPassword.this)
                .setTitle(getResources().getString(R.string.error))
                .setMessage(message)
                .setPositiveButton(getResources().getString(R.string.ok), new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                })

                .show();
    }
}