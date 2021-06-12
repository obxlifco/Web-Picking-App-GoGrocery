package com.gogrocery.view;

import androidx.appcompat.app.AppCompatActivity;
import androidx.databinding.DataBindingUtil;

import android.content.Intent;
import android.content.res.Configuration;
import android.database.DatabaseUtils;
import android.os.Bundle;
import android.view.View;
import android.widget.RadioGroup;

import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityLanguageBinding;

import java.util.Locale;

public class LanguageActivity extends AppCompatActivity {
ActivityLanguageBinding activityLanguageBinding;
SharedPreferenceManager sharedPreferenceManager;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
     activityLanguageBinding= DataBindingUtil.setContentView(this,R.layout.activity_language);
     sharedPreferenceManager= new SharedPreferenceManager(getApplicationContext());
     initFields();
     setupOnClick();
    }




    public void initFields() {
        activityLanguageBinding.tvToolbarTitle.setText(getResources().getString(R.string.toolbar_title_language));

        String langChoice = sharedPreferenceManager.getLocalLanguage();

        if ("ar".equals(langChoice)) {
            activityLanguageBinding.rbIraq.setChecked(true);
        } else {
            activityLanguageBinding.rbEnglish.setChecked(true);
        }


        if(Constants.VARIABLES.USER_LANG_CODE.equals("en")){
            activityLanguageBinding.ivBack.setImageDrawable(getResources().getDrawable(R.drawable.ic_back));
        }else{
            activityLanguageBinding.ivBack.setImageDrawable(getResources().getDrawable(R.drawable.ic_back));
        }
    }


    public void setupOnClick() {

       activityLanguageBinding.ivBack.setOnClickListener(v->{
            super.onBackPressed();
        });

       activityLanguageBinding.rgRadioGroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup group, int i) {
                int id =  activityLanguageBinding.rgRadioGroup.getCheckedRadioButtonId();
                switch (id){
                    case R.id.rb_iraq:
                       sharedPreferenceManager.setLocalLanguage("ar");
                        setLocale("ar");

                        break;
                    case R.id.rb_english:
                        sharedPreferenceManager.setLocalLanguage("en");
                        setLocale("en");
                        break;
//                    default:
//                        BasraCenter.getAppSharedPreference().setLocalLanguage("en");
//                        setLocale("en");
//
//                        break;
                }

            }
        });



    }

    private void setLocale(String lang) {

        if (lang.equalsIgnoreCase(""))
            return;
        Locale myLocale = new Locale(lang);//Set Selected Locale
      sharedPreferenceManager.setLocalLanguage(lang);

        Locale.setDefault(myLocale);//set new locale as default
        Configuration config = new Configuration();//get Configuration
        config.locale = myLocale;//set config locale as selected locale
        getBaseContext().getResources().updateConfiguration(config, getBaseContext().getResources().getDisplayMetrics());
        restartApp();

    }



    private void restartApp(){


        try{
            SharedPreferenceManager mSharedPreferenceManager= new SharedPreferenceManager(getApplicationContext());
            Intent mStartActivity = new Intent(LanguageActivity.this, SelectCategory.class);
            mStartActivity.putExtra("latitude", mSharedPreferenceManager.getLatitude());
            mStartActivity.putExtra("longitude", mSharedPreferenceManager.getLongitude());
            mStartActivity.putExtra("select_category_list","");
            mStartActivity.putExtra("from_where","start");


            this.startActivity(mStartActivity);
            this.finishAffinity();
        }catch (Exception e){
            e.printStackTrace();
        }
    }

}