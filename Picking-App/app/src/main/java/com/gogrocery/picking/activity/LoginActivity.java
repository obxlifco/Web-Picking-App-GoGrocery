package com.gogrocery.picking.activity;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.iid.FirebaseInstanceId;
import com.google.firebase.iid.InstanceIdResult;
import com.gogrocery.picking.R;
import com.gogrocery.picking.databinding.ActivityLoginBinding;
import com.gogrocery.picking.network.APIClient;
import com.gogrocery.picking.network.APIInterface;
import com.gogrocery.picking.prefrences.AppPreferences;
import com.gogrocery.picking.response_pojo.forgot_pwd_pojo.ForgotPwdResponse;
import com.gogrocery.picking.response_pojo.login_pojo.LoginResponse;
import com.gogrocery.picking.utils.AppUtilities;
import com.gogrocery.picking.utils.MyDialog;
import com.gogrocery.picking.utils.MyValidation;

import java.util.HashMap;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.databinding.DataBindingUtil;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class LoginActivity extends BaseActivity {
    ActivityLoginBinding loginBinding;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        loginBinding = DataBindingUtil.setContentView(this, R.layout.activity_login);
        loginBinding.setClickHandler(new LoginClickHandler(this));
        getToken();
    }

    public class LoginClickHandler {
        Context context;

        public LoginClickHandler(Context context) {
            this.context = context;
        }

        public void onLoginClicked(View view) {
            if (AppUtilities.isOnline(LoginActivity.this)) {
                if (new MyValidation(context).validateLogin(loginBinding.etUserNameLogin.getText().toString().trim(),
                        loginBinding.etPasswordLogin.getText().toString())) {
                    callLoginApi();
                }
            } else {
                Toast.makeText(LoginActivity.this, getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
            }
        }

        public void onForgotClicked(final View view) {
            MyDialog.showCustomEditTextOkCancelPopup(LoginActivity.this, getResources().getString(R.string.txtForgotPassword),
                    getResources().getString(R.string.txtEmail), "",new MyDialog.CustomEditTextOkCancelPopupCallback() {
                        @Override
                        public void onDoneClick(String val, AlertDialog alertDialog) {
                            if (AppUtilities.isOnline(LoginActivity.this)) {
                                if (new MyValidation(context).validateForgotPwd(val)) {
                                    AppUtilities.hideKeyboard(alertDialog.getCurrentFocus());
                                    alertDialog.dismiss();
                                    callForgotPwdApi(val);
                                }
                            } else {
                                Toast.makeText(LoginActivity.this, getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                            }
                        }

                        @Override
                        public void onCancelClick(AlertDialog alertDialog) {
                            AppUtilities.hideKeyboard(alertDialog.getCurrentFocus());
                            alertDialog.dismiss();
                        }
                    });
        }
    }

    private void callForgotPwdApi(final String val) {
        showProgressDialog(LoginActivity.this, getResources().getString(R.string.txtLoading));
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
                        Toast.makeText(LoginActivity.this, response.body().getMessage(), Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(LoginActivity.this, response.body().getMessage(), Toast.LENGTH_SHORT).show();
                        Intent i=new Intent(LoginActivity.this,ResetPwdActivity.class);
                        i.putExtra("mail",val);
                        startActivity(i);
                    }
                }////http://15.185.126.44:81/resetpassword/c3ViaGFzaXMuZGVibmF0aEBuYXZzb2Z0Lmlu
            }

            @Override
            public void onFailure(Call<ForgotPwdResponse> call, Throwable t) {

            }
        });

    }

    private void callLoginApi() {
        /*subhasis.debnath@navsoft.in
        Boost1234@*/
        showProgressDialog(LoginActivity.this, getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("username", loginBinding.etUserNameLogin.getText().toString().trim());
        logReq.put("password", loginBinding.etPasswordLogin.getText().toString());
        logReq.put("device_id", AppPreferences.getInstance().getDeviceId());
        //logReq.put("device_token", AppPreferences.getInstance().getFirebaseToken());
        Call<LoginResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerLogin(logReq);
        response1.enqueue(new Callback<LoginResponse>() {
            @Override
            public void onResponse(Call<LoginResponse> call, Response<LoginResponse> response) {
                hideProgressDialog();
                if (response.code() == 200) {
                    if (response.body().getStatus() == 0) {
                        Toast.makeText(LoginActivity.this, response.body().getMsg(), Toast.LENGTH_SHORT).show();
                    } else {
                        AppPreferences.getInstance().storeUserToken(response.body().getUserData().getToken());
                        AppPreferences.getInstance().storeUserID(response.body().getUserData().getUserId());
                        AppPreferences.getInstance().storeCurrency(response.body().getUserData().getCurrencysymbol());
                        if(response.body().getUserData().getImage_name()!=null&&response.body().getUserData().getImage_name().length()>0){
                            AppPreferences.getInstance().storeUserImage(response.body().getUserData().getImage_name());
                        }
                        AppPreferences.getInstance().storeWebsiteID(response.body().getUserData().getWebsiteId());
                        AppPreferences.getInstance().storeWarehouseID(response.body().getUserData().getWarehouseId());
                        AppPreferences.getInstance().storeUserName(response.body().getUserData().getFirstName()+" "+
                                response.body().getUserData().getLastName());
                        startActivity(new Intent(LoginActivity.this, MainActivity.class));
                        finish();
                    }
                }

            }
            @Override
            public void onFailure(Call<LoginResponse> call, Throwable t) {
                hideProgressDialog();
                Toast.makeText(LoginActivity.this, t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void getToken() {
        FirebaseInstanceId.getInstance().getInstanceId()
                .addOnCompleteListener(new OnCompleteListener<InstanceIdResult>() {
                    @Override
                    public void onComplete(@NonNull Task<InstanceIdResult> task) {
                        if (!task.isSuccessful()) {
                            Log.e("TAG", "getInstanceId failed", task.getException());
                            return;
                        }

                        // Get new Instance ID token
                        String token = task.getResult().getToken();
                        Log.e("TAG",""+ token);
                        AppPreferences.getInstance().storeFirebaseToken(token);
                        // Log and toast
                        /*String msg = getString(R.string.msg_token_fmt, token);
                        Log.d("TAG",""+ msg);
                        Toast.makeText(SplashActivity.this, msg, Toast.LENGTH_SHORT).show();*/
                    }
                });
    }
}
