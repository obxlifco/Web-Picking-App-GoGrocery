package com.gogrocery.application;

import android.app.Application;
import android.content.Context;


import com.facebook.FacebookSdk;
import com.facebook.appevents.AppEventsLogger;




import com.facebook.FacebookSdk;
import com.facebook.appevents.AppEventsLogger;



//
//import com.crashlytics.android.Crashlytics;
//
//import io.fabric.sdk.android.Fabric;


public class GoGrocery  extends Application {
    private static GoGrocery instance = null;
    private static Context appContext;





    public void onCreate() {
        super.onCreate();


        appContext = this;
        //Setting App Context
        GoGrocery.appContext = getApplicationContext();
        FacebookSdk.sdkInitialize(getApplicationContext());
        AppEventsLogger.activateApp(this);
        FacebookSdk.setAutoInitEnabled(true);
        FacebookSdk.fullyInitialize();
//

    }








}
