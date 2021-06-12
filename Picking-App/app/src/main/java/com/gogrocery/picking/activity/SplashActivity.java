package com.gogrocery.picking.activity;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import com.google.android.material.bottomsheet.BottomSheetDialog;
import com.gogrocery.picking.R;
import com.gogrocery.picking.network.APIClient;
import com.gogrocery.picking.network.APIInterface;
import com.gogrocery.picking.prefrences.AppPreferences;
import com.gogrocery.picking.response_pojo.version_pojo.VersionResponse;
import com.gogrocery.picking.utils.AppUtilities;

import androidx.annotation.Nullable;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class SplashActivity extends BaseActivity {
    String pushOrderID="";
    private boolean isTimerLoaded = false, isGetVersionLoaded = false;
    private Handler mHandler;
    private boolean isOlderVersion = false;
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);
        if(getIntent().getExtras()!=null){
            Log.e("pushOrderID",""+getIntent().getExtras().getString("pushOrderID"));
            pushOrderID=getIntent().getExtras().getString("pushOrderID");
        }
        /*final Handler handler = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                if(AppPreferences.getInstance().getUserToken().length()>0){
                    Intent i=new Intent(SplashActivity.this, MainActivity.class);
                    i.putExtra("pushOrderID",pushOrderID);
                    startActivity(i);
                }else{
                    startActivity(new Intent(SplashActivity.this,LoginActivity.class));
                }

                finish();
            }
        }, 2000);*/

        Thread background = new Thread() {
            public void run() {

                try {
                    sleep(2000);
                    isTimerLoaded = true;
                    mHandler.sendEmptyMessage(1);
                    //  findViewById(R.id.progressBar).setVisibility(View.GONE);

                } catch (InterruptedException e) {
                    e.printStackTrace();
                }


            }
        };
        background.start();



        mHandler = new Handler(new Handler.Callback() {
            @Override
            public boolean handleMessage(Message msg) {

                if (isGetVersionLoaded && isTimerLoaded) {
                    if (isOlderVersion) {
                        BottomSheetDialog bottomSheetDialog = new BottomSheetDialog(SplashActivity.this);
                        bottomSheetDialog.setContentView(R.layout.app_version_update);
                        Button btnUpgrade = bottomSheetDialog.findViewById(R.id.btnUpgrade);
                        assert btnUpgrade != null;
                        btnUpgrade.setOnClickListener(new View.OnClickListener() {
                            @Override
                            public void onClick(View v) {
                                final String appPackageName = getPackageName(); // getPackageName() from Context or Activity object
                                try {
                                    startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse("market://details?id=" + appPackageName)));
                                } catch (android.content.ActivityNotFoundException anfe) {
                                    startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse("https://play.google.com/store/apps/details?id=" + appPackageName)));
                                }
                                bottomSheetDialog.dismiss();
                            }
                        });
                        try {
                            if (bottomSheetDialog != null) {
                                if (!bottomSheetDialog.isShowing()) {
                                    bottomSheetDialog.show();
                                }
                            }

                        }catch (Exception e){
                            e.printStackTrace();
                        }



                    } else {
                        if(AppPreferences.getInstance().getUserToken().length()>0){
                            Intent i=new Intent(SplashActivity.this, MainActivity.class);
                            i.putExtra("pushOrderID",pushOrderID);
                            startActivity(i);
                        }else{
                            startActivity(new Intent(SplashActivity.this,LoginActivity.class));
                        }
                        finish();
                    }
                }

                return false;
            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        try {
            requestVersionUpdate();
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    public void requestVersionUpdate(){

        Call<VersionResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerAppVersion();
        response1.enqueue(new Callback<VersionResponse>() {
            @Override
            public void onResponse(Call<VersionResponse> call, Response<VersionResponse> response) {
                if (response.code() == 200) {
                    isGetVersionLoaded = true;
                    try {
                        if (response.body().getStatus() == 0) {
                        } else {
                       if (!AppUtilities.getAppVersion(SplashActivity.this).equals(response.body().getData().getPickingAndroid())) {/*Live*/
                      //  if (!"1.1.0".equals(response.body().getData().getPickingAndroid())) {/*develop*/
                            //if (!"1.0.0".equals(response.body().getData().getPickingAndroid())) {/*develop*/
                                isOlderVersion = true;
                            }
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    mHandler.sendEmptyMessage(1);
                }
            }

            @Override
            public void onFailure(Call<VersionResponse> call, Throwable t) {
                isGetVersionLoaded = true;
                mHandler.sendEmptyMessage(1);
            }
        });
    }

}
