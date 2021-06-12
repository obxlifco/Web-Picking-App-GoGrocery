package com.gogrocery.picking.activity;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

import com.gogrocery.picking.R;
import com.gogrocery.picking.databinding.ActivityResetPwdBinding;
import com.gogrocery.picking.network.APIClient;
import com.gogrocery.picking.network.APIInterface;
import com.gogrocery.picking.response_pojo.forgot_pwd_pojo.ForgotPwdResponse;
import com.gogrocery.picking.response_pojo.general_pojo.GeneralResponse;
import com.gogrocery.picking.utils.AppUtilities;
import com.gogrocery.picking.utils.MyValidation;

import java.util.HashMap;

import androidx.annotation.Nullable;
import androidx.databinding.DataBindingUtil;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ResetPwdActivity extends BaseActivity {
    ActivityResetPwdBinding resetPwdBinding;
    String email="";

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        resetPwdBinding = DataBindingUtil.setContentView(this, R.layout.activity_reset_pwd);
        resetPwdBinding.setClickHandler(new ResetPwdClickHandler(this));
        //onNewIntent(getIntent());
        email=getIntent().getStringExtra("mail");

    }

    public class ResetPwdClickHandler {
        Context context;
        public ResetPwdClickHandler(Context context) {
            this.context = context;
        }

        public void onResetClicked(View view) {
            if (AppUtilities.isOnline(ResetPwdActivity.this)) {
                if (new MyValidation(context).validateResetPwd(resetPwdBinding.etOtpReset.getText().toString(),
                        resetPwdBinding.etPasswordReset.getText().toString(),resetPwdBinding.etConfirmPasswordReset.getText().toString())) {
                    AppUtilities.hideKeyboard(getCurrentFocus());
                    callResetPwdAPI();
                }
            } else {
                Toast.makeText(ResetPwdActivity.this, getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
            }
        }

        public void onResendClicked(View view) {
            if (AppUtilities.isOnline(ResetPwdActivity.this)) {
                callForgotPwdApi(email);
            } else {
                Toast.makeText(ResetPwdActivity.this, getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
            }
        }
    }

    private void callResetPwdAPI() {
        showProgressDialog(ResetPwdActivity.this, getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("email", email);
        logReq.put("otp", resetPwdBinding.etOtpReset.getText().toString());
        logReq.put("new_password", resetPwdBinding.etPasswordReset.getText().toString());
        logReq.put("confirm_password", resetPwdBinding.etConfirmPasswordReset.getText().toString());
        Call<GeneralResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerResetPwd(logReq);
        response1.enqueue(new Callback<GeneralResponse>() {
            @Override
            public void onResponse(Call<GeneralResponse> call, Response<GeneralResponse> response) {
                hideProgressDialog();
                Log.e("response", "forgot : " + response.toString());
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(ResetPwdActivity.this, response.body().getMessage(), Toast.LENGTH_SHORT).show();
                        } else {
                            Toast.makeText(ResetPwdActivity.this,response.body().getMessage(), Toast.LENGTH_SHORT).show();
                            onBackPressed();
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<GeneralResponse> call, Throwable t) {

            }
        });
    }

    private void callForgotPwdApi(final String val) {
        showProgressDialog(ResetPwdActivity.this, getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("email", val);
        Call<ForgotPwdResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerForgotPwd(logReq);
        response1.enqueue(new Callback<ForgotPwdResponse>() {
            @Override
            public void onResponse(Call<ForgotPwdResponse> call, Response<ForgotPwdResponse> response) {
                hideProgressDialog();
                Log.e("response", "forgot : " + response.toString());
                if (response.code() == 200) {
                    if (response.body().getStatus() == 0) {
                        Toast.makeText(ResetPwdActivity.this, response.body().getMessage(), Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(ResetPwdActivity.this, response.body().getMessage(), Toast.LENGTH_SHORT).show();
                        resetPwdBinding.etConfirmPasswordReset.setText("");
                        resetPwdBinding.etPasswordReset.setText("");
                        resetPwdBinding.etOtpReset.setText("");
                    }
                }////http://15.185.126.44:81/resetpassword/c3ViaGFzaXMuZGVibmF0aEBuYXZzb2Z0Lmlu
            }

            @Override
            public void onFailure(Call<ForgotPwdResponse> call, Throwable t) {

            }
        });

    }

    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        String action = intent.getAction();
        String data = intent.getDataString();
        if (Intent.ACTION_VIEW.equals(action) && data != null) {
            Log.e("data", "" + data);
        }
    }
}
