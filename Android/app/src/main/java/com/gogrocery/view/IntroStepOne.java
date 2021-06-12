package com.gogrocery.view;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentSender;
import android.content.pm.PackageManager;

import android.location.Location;
import android.location.LocationManager;
import android.net.Uri;
import android.os.Build;
import android.os.Handler;

import android.os.Bundle;
import android.os.Looper;
import android.provider.Settings;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.databinding.DataBindingUtil;

import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityIntroStepOneBinding;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.common.api.PendingResult;
import com.google.android.gms.common.api.ResultCallback;
import com.google.android.gms.common.api.Status;
import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationCallback;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationResult;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.location.LocationSettingsRequest;
import com.google.android.gms.location.LocationSettingsResult;
import com.google.android.gms.location.LocationSettingsStates;
import com.google.android.gms.location.LocationSettingsStatusCodes;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;
import com.karumi.dexter.Dexter;
import com.karumi.dexter.MultiplePermissionsReport;
import com.karumi.dexter.PermissionToken;
import com.karumi.dexter.listener.DexterError;
import com.karumi.dexter.listener.PermissionRequest;
import com.karumi.dexter.listener.PermissionRequestErrorListener;
import com.karumi.dexter.listener.multi.MultiplePermissionsListener;

import org.json.JSONException;

import java.util.ArrayList;
import java.util.List;

public class IntroStepOne extends AppCompatActivity implements GoogleApiClient.ConnectionCallbacks,
        GoogleApiClient.OnConnectionFailedListener,
        LocationListener {
    private SharedPreferenceManager mSharedPreferenceManager;
    private ActivityIntroStepOneBinding mActivityIntroStepOneBinding;
    int PERMISSION_ID = 44;

    String isFrom= "";
   // FusedLocationProviderClient mFusedLocationClient;
    private Location mylocation;
    private GoogleApiClient googleApiClient;
    private final static int REQUEST_CHECK_SETTINGS_GPS=0x1;
    private final static int REQUEST_ID_MULTIPLE_PERMISSIONS=0x2;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityIntroStepOneBinding = DataBindingUtil.setContentView(this, R.layout.activity_intro_step_one);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        isFrom = getIntent().getStringExtra("from");
     //   mFusedLocationClient = LocationServices.getFusedLocationProviderClient(this);
        setUpGClient();

hideStatusBarColor();


        mActivityIntroStepOneBinding.tvEnableLocation.setOnClickListener(v->{
            checkPermissions();

          /*  checkLocationPermission();*/
        });

        if (ActivityCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED &&
                ActivityCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            Intent i = new Intent(IntroStepOne.this, MapLocationSelectionUpdate.class);
            i.putExtra("from",isFrom);
            startActivity(i);
            finish();

        }
    }



    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }





    private LocationCallback mLocationCallback = new LocationCallback() {
        @Override
        public void onLocationResult(LocationResult locationResult) {
            Location mLastLocation = locationResult.getLastLocation();
      /*      latTextView.setText(mLastLocation.getLatitude()+"");
            lonTextView.setText(mLastLocation.getLongitude()+"");*/

            System.out.println("Sukdev : splashscreen location : getLatitude : " + mLastLocation.getLatitude());
            System.out.println("Sukdev : splashscreen location : getLongitude : " + mLastLocation.getLongitude());
            mSharedPreferenceManager.storeLatitude("" + mLastLocation.getLatitude());
            mSharedPreferenceManager.storeLongitude("" + mLastLocation.getLongitude());
            mSharedPreferenceManager.storeLocationAddress(Constants.getAddress(getApplicationContext(),mLastLocation.getLatitude(), mLastLocation.getLongitude()));
            Intent i = new Intent(IntroStepOne.this, MapLocationSelectionUpdate.class);
            i.putExtra("from",isFrom);
            startActivity(i);
            finish();
        }
    };

/*
    private boolean checkPermissions() {
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED &&
                ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            return true;
        }
        return false;
    }
*/


    private boolean isLocationEnabled() {
        LocationManager locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        return locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER) || locationManager.isProviderEnabled(
                LocationManager.NETWORK_PROVIDER
        );
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        int permissionLocation = ContextCompat.checkSelfPermission(IntroStepOne.this,
                Manifest.permission.ACCESS_FINE_LOCATION);
        if (permissionLocation == PackageManager.PERMISSION_GRANTED) {
            getMyLocation();
        }else  if(permissionLocation != PackageManager.PERMISSION_GRANTED){
            mSharedPreferenceManager.storeLatitude("0.00");
            mSharedPreferenceManager.storeLongitude("0.00");
            Toast.makeText(getApplicationContext(), "Permissions denied", Toast.LENGTH_SHORT).show();
            Intent i = new Intent(IntroStepOne.this, MapLocationSelectionUpdate.class);
            i.putExtra("from", isFrom);
            startActivity(i);
        }

/*
        if (requestCode == PERMISSION_ID) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                getMyLocation();
            } else {
                mSharedPreferenceManager.storeLatitude("0.00");
                mSharedPreferenceManager.storeLongitude("0.00");
                Toast.makeText(getApplicationContext(), "Permissions denied", Toast.LENGTH_SHORT).show();
                Intent i = new Intent(IntroStepOne.this, MapLocationSelectionUpdate.class);
                i.putExtra("from", isFrom);
                startActivity(i);
                // finish();
            }

        }*/
    }


    @Override
    public void onResume(){
        super.onResume();
  //    checkPermissions();

    }


    private synchronized void setUpGClient() {
        googleApiClient = new GoogleApiClient.Builder(this)
                .enableAutoManage(this, 0, this)
                .addConnectionCallbacks(this)
                .addOnConnectionFailedListener(this)
                .addApi(LocationServices.API)
                .build();
        googleApiClient.connect();
    }

    private void checkPermissions(){
        int permissionLocation = ContextCompat.checkSelfPermission(IntroStepOne.this,
                android.Manifest.permission.ACCESS_FINE_LOCATION);
        List<String> listPermissionsNeeded = new ArrayList<>();
        if (permissionLocation != PackageManager.PERMISSION_GRANTED) {
            if (ActivityCompat.shouldShowRequestPermissionRationale(IntroStepOne.this,
                    Manifest.permission.ACCESS_FINE_LOCATION)) {
                ActivityCompat.requestPermissions(IntroStepOne.this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_ID);
            } else {
                ActivityCompat.requestPermissions(IntroStepOne.this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_ID);
            }
        }else{
            getMyLocation();
        }

    }

    @Override
    public void onConnected(@Nullable Bundle bundle) {
//        checkPermissions();
    }

    @Override
    public void onConnectionSuspended(int i) {
        //Do whatever you need
        //You can display a message here
    }

    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {
        //You can display a message here
    }

    @Override
    public void onLocationChanged(Location location) {
        mylocation = location;
        if (mylocation != null) {
         /*   Double latitude=mylocation.getLatitude();
            Double longitude=mylocation.getLongitude();
            latitudeTextView.setText("Latitude : "+latitude);
            longitudeTextView.setText("Longitude : "+longitude);*/
            mSharedPreferenceManager.storeLatitude("" + location.getLatitude());
            mSharedPreferenceManager.storeLongitude("" + location.getLongitude());
            mSharedPreferenceManager.storeLocationAddress(Constants.getAddress(getApplicationContext(),location.getLatitude(), location.getLongitude()));
            Intent i = new Intent(IntroStepOne.this, MapLocationSelectionUpdate.class);
            i.putExtra("from","start");
            startActivity(i);
            finish();
            //Or Do whatever you want with your location
        }
    }

    private void getMyLocation(){
        if(googleApiClient!=null) {
            if (googleApiClient.isConnected()) {
                int permissionLocation = ContextCompat.checkSelfPermission(IntroStepOne.this,
                        Manifest.permission.ACCESS_FINE_LOCATION);
                if (permissionLocation == PackageManager.PERMISSION_GRANTED) {
                    mylocation =                     LocationServices.FusedLocationApi.getLastLocation(googleApiClient);
                    LocationRequest locationRequest = new LocationRequest();
                    locationRequest.setInterval(10 * 1000);
                    locationRequest.setFastestInterval(5000);
                    locationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
                    LocationSettingsRequest.Builder builder = new LocationSettingsRequest.Builder()
                            .addLocationRequest(locationRequest);
                    builder.setAlwaysShow(true);
                    LocationServices.FusedLocationApi
                            .requestLocationUpdates(googleApiClient, locationRequest, this);
                    PendingResult<LocationSettingsResult> result =
                            LocationServices.SettingsApi
                                    .checkLocationSettings(googleApiClient, builder.build());
                    result.setResultCallback(new ResultCallback<LocationSettingsResult>() {

                        @Override
                        public void onResult(LocationSettingsResult result) {
                            final Status status = result.getStatus();
                            switch (status.getStatusCode()) {
                                case LocationSettingsStatusCodes.SUCCESS:
                                    // All location settings are satisfied.
                                    // You can initialize location requests here.
                                    int permissionLocation = ContextCompat
                                            .checkSelfPermission(IntroStepOne.this,
                                                    Manifest.permission.ACCESS_FINE_LOCATION);
                                    if (permissionLocation == PackageManager.PERMISSION_GRANTED) {
                                        mylocation = LocationServices.FusedLocationApi
                                                .getLastLocation(googleApiClient);
                                    }
                                    break;
                                case LocationSettingsStatusCodes.RESOLUTION_REQUIRED:
                                    // Location settings are not satisfied.
                                    // But could be fixed by showing the user a dialog.
                                    try {
                                        // Show the dialog by calling startResolutionForResult(),
                                        // and check the result in onActivityResult().
                                        // Ask to turn on GPS automatically
                                        status.startResolutionForResult(IntroStepOne.this,
                                                REQUEST_CHECK_SETTINGS_GPS);
                                    } catch (IntentSender.SendIntentException e) {
                                        // Ignore the error.
                                    }
                                    break;
                                case LocationSettingsStatusCodes.SETTINGS_CHANGE_UNAVAILABLE:
                                    // Location settings are not satisfied.
                                    // However, we have no way
                                    // to fix the
                                    // settings so we won't show the dialog.
                                    // finish();
                                    break;
                            }
                        }
                    });
                }
            }
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        switch (requestCode) {
            case REQUEST_CHECK_SETTINGS_GPS:
                switch (resultCode) {
                    case Activity.RESULT_OK:
                        getMyLocation();
                        break;
                    case Activity.RESULT_CANCELED:
                       // finish();
                        break;
                }
                break;
        }
    }

    @Override
    public void onBackPressed() {
        //super.onBackPressed();
    }
}