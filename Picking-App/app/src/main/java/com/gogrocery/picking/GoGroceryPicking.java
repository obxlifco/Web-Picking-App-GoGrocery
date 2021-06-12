package com.gogrocery.picking;

import android.app.Application;
import android.content.Context;
import android.provider.Settings;
import android.util.Log;

import com.gogrocery.picking.prefrences.AppPreferences;

public class GoGroceryPicking extends Application {
    public static volatile Context applicationContext;
    private static GoGroceryPicking mInstance;
    @Override
    protected void attachBaseContext(Context base) {
        super.attachBaseContext(base);
        //MultiDex.install(this);
    }

    @Override
    public void onCreate() {
        super.onCreate();
        //FacebookSdk.sdkInitialize(getApplicationContext());
        //AppEventsLogger.activateApp(this);
        // especially, if you're using Facebook UI elements.
        mInstance=this;
        GoGroceryPicking.applicationContext = this.getApplicationContext();
        getDeviceID();

    }

    private void getDeviceID() {
        String android_id = Settings.Secure.getString(mInstance.getContentResolver(),
                Settings.Secure.ANDROID_ID);
        AppPreferences.getInstance().storeDeviceId(android_id);
        Log.e("deviceID",""+android_id);
    }
}
