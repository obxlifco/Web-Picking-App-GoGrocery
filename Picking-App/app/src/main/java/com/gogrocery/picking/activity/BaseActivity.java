package com.gogrocery.picking.activity;

import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.view.Window;
import android.view.WindowManager;

import com.gogrocery.picking.prefrences.AppPreferences;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

public class BaseActivity extends AppCompatActivity {
    ProgressDialog mProgressDialog;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
    }

    @Override
    public void onStop() {
        super.onStop();
        hideProgressDialog();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
    }

    public void showProgressDialog(Context ctx, String msg) {
        if (mProgressDialog == null) {
            mProgressDialog = new ProgressDialog(this);
            mProgressDialog.setMessage(msg);
            mProgressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
            mProgressDialog.setCancelable(false);
        }
        mProgressDialog.show();
    }


    public void hideProgressDialog() {
        if (mProgressDialog != null && mProgressDialog.isShowing()) {
            mProgressDialog.dismiss();
        }
    }

    public void performLogout() {
        AppPreferences.getInstance().removeUserToken();
        AppPreferences.getInstance().removeUserName();
        AppPreferences.getInstance().removeUserImage();
        AppPreferences.getInstance().removeCurrency();
        AppPreferences.getInstance().removeWarehouseID();
        AppPreferences.getInstance().removeWebsiteID();
        AppPreferences.getInstance().removeFirebaseToken();
        startActivity(new Intent(BaseActivity.this, LoginActivity.class));
        this.finishAffinity();
    }
}
