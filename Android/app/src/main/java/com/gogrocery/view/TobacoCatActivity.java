package com.gogrocery.view;

import androidx.appcompat.app.AppCompatActivity;
import androidx.databinding.DataBindingUtil;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.Window;

import com.android.volley.AuthFailureError;
import com.android.volley.RequestQueue;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.facebook.appevents.AppEventsConstants;
import com.facebook.appevents.AppEventsLogger;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Models.CartModel.AddToCartModel;
import com.gogrocery.Models.ProductQuantityLocal;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityTobacoCatBinding;
import com.gogrocery.helper.LoadingDialog;
import com.google.firebase.analytics.FirebaseAnalytics;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class TobacoCatActivity extends AppCompatActivity {
    ActivityTobacoCatBinding activityTobacoCatBinding;
    LoadingDialog loadingDialog;
    AppEventsLogger logger;
    private FirebaseAnalytics mFirebaseAnalytics;
    String message = "";

    private DatabaseHandler mDatabaseHandler;
    private SharedPreferenceManager mSharedPreferenceManager;

    @Override
    public void onResume() {
        super.onResume();
        Window window = this.getWindow();
        int width = getResources().getDimensionPixelSize(R.dimen.width_dialogFragment_chat);
        int height = getResources().getDimensionPixelSize(R.dimen.height_dialogFragment__tobaco);
        window.setLayout(width, height);
        window.setBackgroundDrawable(getResources().getDrawable(R.drawable.bg_dialog_fragment));
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        activityTobacoCatBinding = DataBindingUtil.setContentView(this, R.layout.activity_tobaco_cat);
        this.setFinishOnTouchOutside(true);
        loadingDialog = new LoadingDialog(this);
        message = getIntent().getStringExtra("message");
      /*  productId = getIntent().getStringExtra("product_id");
        qty = getIntent().getStringExtra("qty");*/
        activityTobacoCatBinding.tvMessage.setText(message);
        logger = AppEventsLogger.newLogger(this);
        mFirebaseAnalytics = FirebaseAnalytics.getInstance(this);
        mDatabaseHandler = new DatabaseHandler(getApplicationContext());
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());

        activityTobacoCatBinding.tvBtnIAm21below.setOnClickListener(v -> {
            mSharedPreferenceManager.saveYearCheck("N");
            finish();
        });
        activityTobacoCatBinding.tvBtnIAm21Above.setOnClickListener(v -> {
            mSharedPreferenceManager.saveYearCheck("Y");
            finish();

        });
    }


}
