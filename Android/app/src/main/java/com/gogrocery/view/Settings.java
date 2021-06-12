package com.gogrocery.view;

import androidx.appcompat.app.AppCompatActivity;
import androidx.databinding.DataBindingUtil;

import android.os.Bundle;
import android.view.View;

import com.gogrocery.R;
import com.gogrocery.databinding.ActivitySettingsBinding;

public class Settings extends AppCompatActivity implements View.OnClickListener {
ActivitySettingsBinding activitySettingsBinding;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
       activitySettingsBinding= DataBindingUtil.setContentView(this,R.layout.activity_settings);
       initFields();
       setUpClick();
    }

    private void initFields(){

    }


    private void setUpClick() {
        activitySettingsBinding.ivBack.setOnClickListener(this);
        activitySettingsBinding.ivBack.setOnClickListener(v->{
            super.onBackPressed();
        });

    }

    @Override
    public void onClick(View view) {

    }

}