package com.gogrocery.view;

import androidx.appcompat.app.AppCompatActivity;
import androidx.databinding.DataBindingUtil;

import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;

import com.gogrocery.R;
import com.gogrocery.databinding.ActivityOurVisionPurposeBinding;

public class OurVisionPurpose extends AppCompatActivity implements View.OnClickListener {
ActivityOurVisionPurposeBinding activityOurVisionPurposeBinding;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        activityOurVisionPurposeBinding= DataBindingUtil.setContentView(this,R.layout.activity_our_vision_purpose);
        initFields();
        setUpClick();
        hideStatusBarColor();
    }

    @Override
    public void onClick(View view) {

    }

    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }
    private void initFields(){

    }


    private void setUpClick() {
        activityOurVisionPurposeBinding.ivBack.setOnClickListener(this);
        activityOurVisionPurposeBinding.ivBack.setOnClickListener(v->{
            super.onBackPressed();
        });

    }


}