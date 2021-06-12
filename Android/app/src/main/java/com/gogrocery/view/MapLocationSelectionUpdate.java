package com.gogrocery.view;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentSender;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.provider.Settings;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.FragmentActivity;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Models.StoreTypeModel.DataItem;
import com.gogrocery.Models.StoreTypeModel.StoreTypeModel;
import com.gogrocery.Models.WarehouseModel.Data;
import com.gogrocery.Models.WarehouseModel.WarehouseModel;
import com.gogrocery.R;
import com.gogrocery.ViewModel.StoreCategoryModel;
import com.gogrocery.helper.LoadingDialog;
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
import com.google.android.gms.location.LocationSettingsStatusCodes;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.CircleOptions;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.android.libraries.places.api.Places;
import com.google.android.libraries.places.api.model.Place;
import com.google.android.libraries.places.api.net.PlacesClient;
import com.google.android.libraries.places.widget.AutocompleteSupportFragment;
import com.google.android.libraries.places.widget.listener.PlaceSelectionListener;
import com.google.gson.Gson;
import com.karumi.dexter.Dexter;
import com.karumi.dexter.MultiplePermissionsReport;
import com.karumi.dexter.PermissionToken;
import com.karumi.dexter.listener.PermissionRequest;
import com.karumi.dexter.listener.multi.MultiplePermissionsListener;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static com.gogrocery.Constants.Constants.API_KEY;

public class MapLocationSelectionUpdate extends FragmentActivity implements OnMapReadyCallback, LocationListener,GoogleApiClient.ConnectionCallbacks,
        GoogleApiClient.OnConnectionFailedListener {

    private Location mLastKnownLocation;
    private LocationCallback locationCallback;
    PlacesClient placesClient;
    private ImageView currentLocationBtn;
    private ImageView ivBackNav;
    private LinearLayout btnConfirmLocationDeliveryHere;
    private ImageView ivCloseNav;
    TextView tvDeliveryAt;
    private GoogleMap mMap;
    double lat = 0.0;
    double longitude = 0.0;
    private MarkerOptions mMarker;
    private List<Data> mWarehouseList = new ArrayList<>();
    private Dialog mBottomSheetDialog, mBottomSheetTypeDialog;
    private LatLng mLatLngMain;
    private final float DEFAULT_ZOOM = 15;
    int PERMISSION_ID = 44;
    private SharedPreferenceManager mSharedPreferenceManager;
    private FusedLocationProviderClient mFusedLocationProviderClient;
    LoadingDialog loadingDialog;
    View mapView;
    List<DataItem> storeCategoryList = new ArrayList<>();
    boolean isClickable = false;
    boolean doubleBackToExitPressedOnce = false;
    boolean isCurrentLocationBtnOn = false;
    String locationAddress = "";
    String isFromWhere = "";
    JSONArray typeID;
    private Location mylocation;
    private GoogleApiClient googleApiClient;
    Dialog mSomethingwentworng;
    private final static int REQUEST_CHECK_SETTINGS_GPS=0x1;
    private final static int REQUEST_ID_MULTIPLE_PERMISSIONS=0x2;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_map_location_selection2);
        isFromWhere = getIntent().getStringExtra("from");
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        setUpGClient();
        //  mFusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(this);
        currentLocationBtn = findViewById(R.id.ivBtn_currentLocation);
        ivBackNav = findViewById(R.id.ivBack);
        ivCloseNav = findViewById(R.id.ivClose);
        tvDeliveryAt = findViewById(R.id.tvDeliveryAt);
        btnConfirmLocationDeliveryHere = findViewById(R.id.btnConfirmLocationDeliveryHere);
        mFusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(MapLocationSelectionUpdate.this);
        loadingDialog = new LoadingDialog(MapLocationSelectionUpdate.this);
        hideStatusBarColor();
        // RelativeLayout searchBtn = findViewById(R.id.tvbtn_search);
        try {
            if (!Places.isInitialized()) {
                Places.initialize(getApplicationContext(), API_KEY);
                placesClient = Places.createClient(this);

//                PlacesClient placesClient = Places.createClient(this);
             /*   if(mSharedPreferenceManager.getLatitude().isEmpty()&& mSharedPreferenceManager.getLongitude().isEmpty()){
                 // getCurrentLocation();
                    getDeviceLocation();
                }*/
            }
            // Retrieve a PlacesClient (previously initialized - see MainActivity)


        } catch (Exception e) {
            e.printStackTrace();
        }

        openMapView();

        // String apiKey = "AIzaSyC0WHcWkovQFGhtjPfgQu4pNrtE5ikwtmY";

        openSearchView();

        ivCloseNav.setOnClickListener(v -> {
            if(isFromWhere!=null&&!isFromWhere.isEmpty()){
                if(isFromWhere.equals("guest")){
                    Intent i = new Intent(MapLocationSelectionUpdate.this, LoginActivity.class);
                    startActivity(i);
                    finish();
                }else if(isFromWhere.equals("start")) {
                    if (lat != 0.0 && longitude != 0.0) {
                        try {
                            requestStoreTypeList(lat, longitude,isFromWhere);
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }else {
                        Toast.makeText(MapLocationSelectionUpdate.this, "Do not close this view", Toast.LENGTH_SHORT).show();
                    }
                }else {
                    super.onBackPressed();
                }

            }else {
                finish();
            }
        });

        currentLocationBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                isCurrentLocationBtnOn= true;
                checkPermissions();
             /*   if (isLocationEnabled()) {
                    getDeviceLocation();

                } else {
                    showSettingsDialog();
                }*/

            }
        });
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


    private void openMapView() {
        try {
            SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager().findFragmentByTag("mapFragmentTag");
//                .findFragmentById(R.id.mp_map);
            if(mapFragment!=null) {
                mapView = mapFragment.getView();
                mapFragment.getMapAsync(this);
                mMarker = new MarkerOptions();
                mMarker.draggable(true);
                View locationButton = ((View) mapView.findViewById(Integer.parseInt("1")).getParent()).findViewById(Integer.parseInt("2"));
                RelativeLayout.LayoutParams rlp = (RelativeLayout.LayoutParams) locationButton.getLayoutParams();
// position on right bottom
                rlp.addRule(RelativeLayout.ALIGN_END, 0);
                rlp.addRule(RelativeLayout.ALIGN_PARENT_END, RelativeLayout.TRUE);
                rlp.setMargins(0, 280, 180, 0);


                findViewById(R.id.btnConfirmLocationDeliveryHere).setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        mMap.clear();
                        //    if (findViewById(R.id.progressSpinKitView).getVisibility() == View.GONE) {
                        try {
                            if (lat != 0.0 && longitude != 0.0) {
                                //requestWarehouseList(mLatLngMain.latitude, mLatLngMain.longitude);

                                if (lat != 0.0 && longitude != 0.0) {
                                    mMap.clear();
                                    LatLng initialLatLon = new LatLng(lat, longitude);
                                    mLatLngMain = initialLatLon;
                                    mMap.addMarker(new MarkerOptions().position(initialLatLon).icon(BitmapDescriptorFactory.fromResource(R.drawable.ic_combine_marker)).anchor(0.5f, 0.5f));
                                    mMap.addCircle(new CircleOptions().center(new LatLng(lat, longitude)).radius(300).strokeColor(getResources().getColor(R.color.map_radius_new)).fillColor(getResources().getColor(R.color.map_radius_new)));
                                    //  mMap.moveCamera(CameraUpdateFactory.newLatLng(initialLatLon));
                                    mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(initialLatLon.latitude, initialLatLon.longitude), 15.0f));
                                    //  mSharedPreferenceManager.storeLocationAddress(Constants.getAddress(getApplicationContext(), mLatLngMain.latitude, mLatLngMain.longitude));
                                    tvDeliveryAt.setText(Constants.getAddress(getApplicationContext(), lat, longitude));
                                    btnConfirmLocationDeliveryHere.setVisibility(View.VISIBLE);

                                }


                                {


                                    requestStoreTypeList(mLatLngMain.latitude, mLatLngMain.longitude, isFromWhere);


                                }
                            } else {
                                // getCurrentLocation();
                                //   getDeviceLocation();
                                checkPermissions();
                            }
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                        //  }
                    }
                });
            }
        }catch (Exception e){e.printStackTrace();}



    }

    private void openSearchView() {

        AutocompleteSupportFragment autocompleteSupportFragment =
                (AutocompleteSupportFragment) getSupportFragmentManager().findFragmentById(R.id.autocomplete_fragment);

        assert autocompleteSupportFragment != null;
        autocompleteSupportFragment.setPlaceFields(Arrays.asList(Place.Field.ID, Place.Field.NAME, Place.Field.LAT_LNG, Place.Field.ADDRESS));
        autocompleteSupportFragment.setHint("Write here your address");


        autocompleteSupportFragment.setOnPlaceSelectedListener(
                new PlaceSelectionListener() {
                    @Override
                    public void onPlaceSelected(@NonNull Place place) {
                        final LatLng latLng = place.getLatLng();
                        assert latLng != null;
                        lat = latLng.latitude;
                        longitude = latLng.longitude;
                        //  Toast.makeText(MapLocationSelectionUpdate.this, "" + lat + " "+longitude, Toast.LENGTH_SHORT).show();

                        if (lat != 0.0 && longitude != 0.0) {
                            mSharedPreferenceManager.storeLatitude("" + lat);
                            mSharedPreferenceManager.storeLongitude("" + longitude);
                            mSharedPreferenceManager.storeLocationAddress(Constants.getAddress(getApplicationContext(), lat, longitude));
                            tvDeliveryAt.setText(Constants.getAddress(getApplicationContext(), lat, longitude));
                            btnConfirmLocationDeliveryHere.setVisibility(View.VISIBLE);

                            mMap.clear();
                            LatLng initialLatLon = new LatLng(lat, longitude);
                            mLatLngMain = initialLatLon;
                            mMap.addMarker(new MarkerOptions().position(initialLatLon).icon(BitmapDescriptorFactory.fromResource(R.drawable.ic_combine_marker)).anchor(0.5f, 0.5f));
                            mMap.addCircle(new CircleOptions().center(new LatLng(lat, longitude)).radius(300).strokeColor(getResources().getColor(R.color.map_radius_new)).fillColor(getResources().getColor(R.color.map_radius_new)));
                            //  mMap.moveCamera(CameraUpdateFactory.newLatLng(initialLatLon));
                            mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(initialLatLon.latitude, initialLatLon.longitude), 15.0f));


                        }
                        new Handler().postDelayed(new Runnable() {
                            @Override
                            public void run() {

                                autocompleteSupportFragment.setText("");
                            }
                        }, 65);
                    }

                    @Override
                    public void onError(Status status) {
                        // Toast.makeText(MapLocationSelectionUpdate.this, "" + status.getStatusMessage(), Toast.LENGTH_SHORT).show();
                        Log.e("Error", "Map" + status.getStatusMessage());
                        autocompleteSupportFragment.setText("");
                    }
                });

    }

    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            // TODO: Consider calling
            //    ActivityCompat#requestPermissions

            return;
        }
        mMap.clear();
        mMap.setMyLocationEnabled(true);
        mMap.getUiSettings().setMyLocationButtonEnabled(false);
        mMap.getUiSettings().setZoomControlsEnabled(false);




//Paid API KEY
        //AIzaSyDwJfFz9Hyur4RkbEa_Hlt6Fkibr6rYhJo

        // Add a marker in Sydney and move the camera
        //LatLng initialLatLon = new LatLng(25.2048, 55.2708);
        mMap.clear();
        if (lat != 0.0 && longitude != 0.0) {
            LatLng initialLatLon = new LatLng(lat, longitude);

            mLatLngMain = initialLatLon;
            //mMap.addMarker(new MarkerOptions().position(initialLatLon));
            mMap.addMarker(new MarkerOptions().position(initialLatLon).icon(BitmapDescriptorFactory.fromResource(R.drawable.ic_combine_marker)).anchor(0.5f, 0.5f));
            mMap.addCircle(new CircleOptions().center(new LatLng(lat, longitude)).radius(300).strokeColor(getResources().getColor(R.color.map_radius_new)).fillColor(getResources().getColor(R.color.map_radius_new)));
            //  mMap.moveCamera(CameraUpdateFactory.newLatLng(initialLatLon));
            mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(initialLatLon.latitude, initialLatLon.longitude), 15.0f));
            tvDeliveryAt.setText(Constants.getAddress(getApplicationContext(), lat, longitude));
        }
        mMap.setOnMapClickListener(new GoogleMap.OnMapClickListener() {
            @Override
            public void onMapClick(LatLng latLng) {
                LatLng newLoca = new LatLng(latLng.latitude, latLng.longitude);
                mMap.clear();
                lat = latLng.latitude;
                longitude = latLng.longitude;
                mSharedPreferenceManager.storeLatitude("" + newLoca.latitude);
                mSharedPreferenceManager.storeLongitude("" + newLoca.longitude);
                mSharedPreferenceManager.storeLocationAddress(Constants.getAddress(getApplicationContext(), newLoca.latitude, newLoca.longitude));
                tvDeliveryAt.setText(Constants.getAddress(getApplicationContext(), lat, longitude));
                mLatLngMain = latLng;

                try {
                    if (lat != 0.0 && longitude != 0.0) {
                        LatLng initialLatLon = new LatLng(lat, longitude);
                        mMap.clear();
                        mLatLngMain = initialLatLon;

                        //mMap.addMarker(new MarkerOptions().position(initialLatLon));
                        mMap.addMarker(new MarkerOptions().position(initialLatLon).icon(BitmapDescriptorFactory.fromResource(R.drawable.ic_combine_marker)).anchor(0.5f, 0.5f));
                        mMap.addCircle(new CircleOptions().center(new LatLng(lat, longitude)).radius(300).strokeColor(getResources().getColor(R.color.map_radius_new)).fillColor(getResources().getColor(R.color.map_radius_new)));
                        mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(newLoca.latitude, newLoca.longitude), 15.0f));
                        mSharedPreferenceManager.storeLocationAddress(Constants.getAddress(getApplicationContext(), lat, longitude));
                        tvDeliveryAt.setText(Constants.getAddress(getApplicationContext(), lat, longitude));
                        btnConfirmLocationDeliveryHere.setVisibility(View.VISIBLE);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }


            }
        });


        mMap.setOnMapLongClickListener(new GoogleMap.OnMapLongClickListener() {
            @Override
            public void onMapLongClick(LatLng latLng) {
                LatLng newLoca = new LatLng(latLng.latitude, latLng.longitude);
                mMap.clear();
                lat = latLng.latitude;
                longitude = latLng.longitude;
                mSharedPreferenceManager.storeLatitude("" + newLoca.latitude);
                mSharedPreferenceManager.storeLongitude("" + newLoca.longitude);
                mSharedPreferenceManager.storeLocationAddress(Constants.getAddress(getApplicationContext(), newLoca.latitude, newLoca.longitude));
                tvDeliveryAt.setText(Constants.getAddress(getApplicationContext(), lat, longitude));
                mLatLngMain = latLng;

                try {
                    if (lat != 0.0 && longitude != 0.0) {
                        LatLng initialLatLon = new LatLng(lat, longitude);
                        mMap.clear();
                        mLatLngMain = initialLatLon;
                        //mMap.addMarker(new MarkerOptions().position(initialLatLon));
                        mMap.addMarker(new MarkerOptions().position(initialLatLon).icon(BitmapDescriptorFactory.fromResource(R.drawable.ic_combine_marker)).anchor(0.5f, 0.5f));
                        mMap.addCircle(new CircleOptions().center(new LatLng(lat, longitude)).radius(300).strokeColor(getResources().getColor(R.color.map_radius_new)).fillColor(getResources().getColor(R.color.map_radius_new)));
                        mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(newLoca.latitude, newLoca.longitude), 15.0f));
                        mSharedPreferenceManager.storeLocationAddress(Constants.getAddress(getApplicationContext(), lat, longitude));
                        tvDeliveryAt.setText(Constants.getAddress(getApplicationContext(), lat, longitude));
                        btnConfirmLocationDeliveryHere.setVisibility(View.VISIBLE);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }

            }
        });

        try {
         /*   if (mSharedPreferenceManager.getLatitude().isEmpty() && mSharedPreferenceManager.getLongitude().isEmpty()) {


            } else {
                lat = Double.parseDouble(mSharedPreferenceManager.getLatitude());
                longitude = Double.parseDouble(mSharedPreferenceManager.getLongitude());

            }*/

//            checkPermissions();
            checkPermissions_new();
            // getDeviceLocation();
        } catch (Exception e) {
            e.printStackTrace();
        }


    }


    private boolean isLocationEnabled() {
        LocationManager locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        return locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER) || locationManager.isProviderEnabled(
                LocationManager.NETWORK_PROVIDER
        );
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        int permissionLocation = ContextCompat.checkSelfPermission(MapLocationSelectionUpdate.this,
                Manifest.permission.ACCESS_FINE_LOCATION);
        if (permissionLocation == PackageManager.PERMISSION_GRANTED) {
            openMapView();
          getMyLocation();
        }
      /*  if (requestCode == PERMISSION_ID) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                getDeviceLocation();
            }
        }*/
    }
/*

    private boolean checkPermissions() {
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED &&
                ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            return true;
        }
        return false;
    }
*/


    private void showSettingsDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(MapLocationSelectionUpdate.this);
        builder.setTitle(getResources().getString(R.string.need_permissions));
        builder.setMessage(getResources().getString(R.string.this_app_needs_permission_to_use_this_feature));
        builder.setPositiveButton(getResources().getString(R.string.go_to_settings), new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.cancel();
               // Toast.makeText(MapLocationSelectionUpdate.this, "Turn on location", Toast.LENGTH_LONG).show();
                Intent intent = new Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS);
                startActivity(intent);
            }
        });
        builder.setNegativeButton(getResources().getString(R.string.cancel), new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.cancel();
            }
        });
        builder.show();

    }


/*
    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 51) {
            if (resultCode == RESULT_OK) {
                getDeviceLocation();
            }
        }
    }
*/

    private void requestPermissions() {

        if (ContextCompat.checkSelfPermission(MapLocationSelectionUpdate.this,
                Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED){
            if (ActivityCompat.shouldShowRequestPermissionRationale(MapLocationSelectionUpdate.this,
                    Manifest.permission.ACCESS_FINE_LOCATION)){
                ActivityCompat.requestPermissions(MapLocationSelectionUpdate.this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_ID);
            }else{
                ActivityCompat.requestPermissions(MapLocationSelectionUpdate.this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_ID);
            }
        }
    }


    @Override
    protected void onPause() {
        if (mSomethingwentworng != null) {
            mSomethingwentworng.dismiss();

        }
        if (mBottomSheetDialog != null) {
            mBottomSheetDialog.dismiss();

        }
        if (mBottomSheetTypeDialog != null) {
            mBottomSheetTypeDialog.dismiss();

        }
        super.onPause();

    }

    @Override
    protected void onDestroy() {
        if (mSomethingwentworng != null) {
            mSomethingwentworng.dismiss();

        }
        if (mBottomSheetDialog != null) {
            mBottomSheetDialog.dismiss();

        }
        if (mBottomSheetTypeDialog != null) {
            mBottomSheetTypeDialog.dismiss();

        }

        super.onDestroy();
    }

    public void requestStoreTypeList(double latitude, double longitude ,String fromWhere) throws JSONException {

        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("latitude", latitude);
        mJsonObject.put("longitude", longitude);
        mJsonObject.put("website_id", 1);

        System.out.println("Rahul : MapLocationSelectionUpdate : requestStoreTypeList : mJsonObject : " + mJsonObject);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.STORE_TYPE, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : MapLocationSelectionUpdate : requestStoreTypeList : response : " + response);
                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        StoreTypeModel storeTypeModel = mGson.fromJson(response.toString(), StoreTypeModel.class);
                        if (storeTypeModel.getStatus() == 1) {

                            boolean isSelectedCategory = false;
                            if (storeTypeModel.getData().size() > 0) {
                                storeCategoryList.clear();
                                storeCategoryList.addAll(storeTypeModel.getData());
                                mSharedPreferenceManager.saveSelectedCategoryList(storeCategoryList);
                                //For new Activity
                                ArrayList<StoreCategoryModel> typeModels = new ArrayList<>();
                                typeModels.add(new StoreCategoryModel("All", 0, false, 1));
                                for (int i = 0; i < storeCategoryList.size(); i++) {
                                    boolean isSelected;
                                    if (storeCategoryList.get(i).getHas_store() == 1) {
                                        isSelected = true;
                                    } else {
                                        isSelected = false;
                                    }
                                    StoreCategoryModel tmp = new StoreCategoryModel(storeCategoryList.get(i).getName(), storeCategoryList.get(i).getId(), isSelected, storeCategoryList.get(i).getHas_store());
                                    typeModels.add(tmp);
                                }

                                for (int i = 0; i < typeModels.size(); i++) {
                                    if (typeModels.get(i).isSelect()) {
                                        isSelectedCategory = true;
                                    }
                                }
                                if (isSelectedCategory) {

                                    if(!isClickable) {
                                        if (fromWhere != null && !fromWhere.isEmpty()) {
                                            if (fromWhere.equals("add")) {
                                                isClickable= true;
                                                Intent i = new Intent(MapLocationSelectionUpdate.this, AddNewAddress.class);
                                                i.putExtra("from", "add");
                                                startActivity(i);
                                                finish();
                                            } else {
                                                mSharedPreferenceManager.storeLocationAddress(String.valueOf(tvDeliveryAt.getText()));
                                                Intent i = new Intent(MapLocationSelectionUpdate.this, SelectCategory.class);
                                                i.putExtra("latitude", latitude + "");
                                                i.putExtra("longitude", longitude + "");
                                                i.putExtra("from_where", "map");
                                                i.putExtra("selected_address", "Show Store delivering to : \n" + String.valueOf(tvDeliveryAt.getText()));
                                                isClickable= true;
                                                startActivity(i);
                                            }
                                        } else {
                                            mSharedPreferenceManager.storeLocationAddress(String.valueOf(tvDeliveryAt.getText()));
                                            Intent i = new Intent(MapLocationSelectionUpdate.this, SelectCategory.class);
                                            i.putExtra("latitude", latitude + "");
                                            i.putExtra("longitude", longitude + "");
                                            i.putExtra("from_where", "map");
                                            i.putExtra("selected_address", "Show Store delivering to : \n" + String.valueOf(tvDeliveryAt.getText()));
                                            isClickable= true;
                                            startActivity(i);
                                        }
                                    }

                                }
                                else {

                                    showNoDeliveryDialog();
                                }
                                //showBottomSheetTypeDialog(storeCategoryList, latitude, longitude);
                            }
                        } else {
                            showNoDeliveryDialog();


                        }
                    }

                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                showNoDeliveryDialog();
                System.out.println("Rahul : MapLocationSelectionUpdate : requestStoreTypeList : error : " + error);
            }
        });

        // Adding request to request queue
        jsonObjReq.setRetryPolicy(new RetryPolicy() {
            @Override
            public int getCurrentTimeout() {
                return 50000;
            }

            @Override
            public int getCurrentRetryCount() {
                return 50000;
            }

            @Override
            public void retry(VolleyError error) throws VolleyError {

            }
        });
        queue.add(jsonObjReq);
    }


    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }


    public void requestWarehouseList(double argLat, double argLong, JSONArray storetype_id) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(MapLocationSelectionUpdate.this);
        loadingDialog.showDialog();
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("latitude", argLat);
        mJsonObject.put("longitude", argLong);
        mJsonObject.put("website_id", 1);
        mJsonObject.put("storetype_id", storetype_id);

        System.out.println("Rahul : MapLocationSelectionUpdate : requestWarehouseList : mJsonObject : " + mJsonObject);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.WAREHOUSE_LIST, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        loadingDialog.hideDialog();
                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        System.out.println("Rahul : MapLocationSelectionUpdate : requestWarehouseList : response : " + response);
                        WarehouseModel mWarehouseModel = mGson.fromJson(response.toString(), WarehouseModel.class);
                        if (!mWarehouseModel.getStatus().equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                            mBottomSheetTypeDialog.dismiss();

                            mWarehouseList.clear();
                            mWarehouseList.addAll(mWarehouseModel.getData());
                            System.out.println("Rahul : MapLocationSelectionUpdate : requestWarehouseList : mWarehouseList : " + mGson.toJson(mWarehouseList));
                            //  showBottomSheetDialog();

                        } else {

                        }
//                        findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                    }

                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : MapLocationSelectionUpdate : requestWarehouseList : VolleyError : " + error.toString());
                loadingDialog.hideDialog();
                //  findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                //  showNoDeliveryDialog();
                showNoDeliveryDialog();
            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");

                return headers;
            }


        };


        // Adding request to request queue
        jsonObjReq.setRetryPolicy(new RetryPolicy() {
            @Override
            public int getCurrentTimeout() {
                return 50000;
            }

            @Override
            public int getCurrentRetryCount() {
                return 50000;
            }

            @Override
            public void retry(VolleyError error) throws VolleyError {

            }
        });
        queue.add(jsonObjReq);
    }


    public void showNoDeliveryDialog() {
        mSomethingwentworng = new Dialog(MapLocationSelectionUpdate.this);
        mSomethingwentworng.setCancelable(false);
        mSomethingwentworng.setContentView(R.layout.no_store_available_dialog);
        TextView txtOk = mSomethingwentworng.findViewById(R.id.txtOk);
        txtOk.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                mSomethingwentworng.dismiss();
            }
        });

        mSomethingwentworng.show();

    }


    public void requestEmptyCart(double argLat, double argLong, String argWarehouseID, String argWarehouseName) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        loadingDialog.showDialog();
//        findViewById(R.id.progressSpinKitView).setVisibility(View.VISIBLE);
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));
        mJsonObject.put("website_id", 1);

        System.out.println("Rahul : MapLocationSelectionUpdate : requestEmptyCart : mJsonObject : " + mJsonObject.toString());

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.EMPTY_CART, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        loadingDialog.hideDialog();
                        System.out.println("Rahul : MapLocationSelectionUpdate : requestEmptyCart : response : " + response.toString());
//                        findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                        try {
                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                new DatabaseHandler(getApplicationContext()).deleteAllRecord();

                                Intent i = new Intent(MapLocationSelectionUpdate.this, MainActivityNew.class);
                                startActivity(i);
                                SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
                                mSharedPreferenceManager.storeLatLong(String.valueOf(argLat) + "," + argLong);
                                mSharedPreferenceManager.storeWarehouseId(argWarehouseID);
                                mSharedPreferenceManager.storeWarehouseName(argWarehouseName);
                                finish();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
//                findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                loadingDialog.hideDialog();
                System.out.println("Rahul : MapLocationSelectionUpdate : requestEmptyCart : VolleyError : " + error.toString());
            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                if (mSharedPreferenceManager.isLoggedIn()) {
                    headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                }

                return headers;
            }


        };


        // Adding request to request queue
        jsonObjReq.setRetryPolicy(new RetryPolicy() {
            @Override
            public int getCurrentTimeout() {
                return 50000;
            }

            @Override
            public int getCurrentRetryCount() {
                return 50000;
            }

            @Override
            public void retry(VolleyError error) throws VolleyError {

            }
        });
        queue.add(jsonObjReq);
    }


    @SuppressLint("MissingPermission")
    private void getDeviceLocation() {
       // if (checkPermissions()) {
          //  if (isLocationEnabled()) {
                mFusedLocationProviderClient.getLastLocation()
                        .addOnCompleteListener(new OnCompleteListener<Location>() {
                            @Override
                            public void onComplete(@NonNull Task<Location> task) {
                                if (task.isSuccessful()) {
                                    mLastKnownLocation = task.getResult();
                                    if (mLastKnownLocation != null) {
                                        mMap.clear();
                                        /* mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(mLastKnownLocation.getLatitude(), mLastKnownLocation.getLongitude()), DEFAULT_ZOOM));*/

                                        // mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(mLastKnownLocation.getLatitude(), mLastKnownLocation.getLongitude()), DEFAULT_ZOOM));
                                        lat = mLastKnownLocation.getLatitude();
                                        longitude = mLastKnownLocation.getLongitude();
                                        //  Toast.makeText(MapLocationSelectionUpdate.this, "" + lat + " "+longitude, Toast.LENGTH_SHORT).show();

                                        if (lat != 0.0 && longitude != 0.0) {
                                            LatLng initialLatLon = new LatLng(lat, longitude);
                                            mLatLngMain = initialLatLon;
                                            //mMap.addMarker(new MarkerOptions().position(initialLatLon));
                                            mMap.addMarker(new MarkerOptions().position(initialLatLon).icon(BitmapDescriptorFactory.fromResource(R.drawable.ic_combine_marker)).anchor(0.5f, 0.5f));
                                            mMap.addCircle(new CircleOptions().center(new LatLng(lat, longitude)).radius(300).strokeColor(getResources().getColor(R.color.map_radius_new)).fillColor(getResources().getColor(R.color.map_radius_new)));
                                            //  mMap.moveCamera(CameraUpdateFactory.newLatLng(initialLatLon));

                                            mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(initialLatLon.latitude, initialLatLon.longitude), 15.0f));
                                             locationAddress=Constants.getAddress(getApplicationContext(), mLatLngMain.latitude, mLatLngMain.longitude);
                                            if (locationAddress != null && !locationAddress.isEmpty()) {
                                                tvDeliveryAt.setText(locationAddress);
                                                btnConfirmLocationDeliveryHere.setVisibility(View.VISIBLE);
                                            }
                                        }
                                    } else {
                                        mMap.clear();
                                        final LocationRequest locationRequest = LocationRequest.create();
                                        locationRequest.setInterval(10000);
                                        locationRequest.setFastestInterval(5000);
                                        locationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
                                        locationCallback = new LocationCallback() {
                                            @Override
                                            public void onLocationResult(LocationResult locationResult) {
                                                super.onLocationResult(locationResult);
                                                if (locationResult == null) {
                                                    return;
                                                }
                                                mLastKnownLocation = locationResult.getLastLocation();
                                                // mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(mLastKnownLocation.getLatitude(), mLastKnownLocation.getLongitude()), DEFAULT_ZOOM));
                                                lat = mLastKnownLocation.getLatitude();
                                                longitude = mLastKnownLocation.getLongitude();
                                                //  Toast.makeText(MapLocationSelectionUpdate.this, "" + lat + " "+longitude, Toast.LENGTH_SHORT).show();

                                                if (lat != 0.0 && longitude != 0.0) {
                                                    LatLng initialLatLon = new LatLng(lat, longitude);
                                                    mMap.clear();
                                                    mLatLngMain = initialLatLon;
                                                    //mMap.addMarker(new MarkerOptions().position(initialLatLon));
                                                    mMap.addMarker(new MarkerOptions().position(initialLatLon).icon(BitmapDescriptorFactory.fromResource(R.drawable.ic_combine_marker)).anchor(0.5f, 0.5f));
                                                    mMap.addCircle(new CircleOptions().center(new LatLng(lat, longitude)).radius(300).strokeColor(getResources().getColor(R.color.map_radius_new)).fillColor(getResources().getColor(R.color.map_radius_new)));
                                                    //    mMap.moveCamera(CameraUpdateFactory.newLatLng(initialLatLon));
                                                    mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(initialLatLon.latitude, initialLatLon.longitude), 15.0f));
                                                     locationAddress=Constants.getAddress(getApplicationContext(), mLatLngMain.latitude, mLatLngMain.longitude);
                                                  //  mSharedPreferenceManager.storeLocationAddress(Constants.getAddress(getApplicationContext(), mLatLngMain.latitude, mLatLngMain.longitude));
                                                    if (locationAddress!=null&&!locationAddress.isEmpty()) {
                                                        tvDeliveryAt.setText(locationAddress);
                                                        btnConfirmLocationDeliveryHere.setVisibility(View.VISIBLE);
                                                    }else {
                                                        btnConfirmLocationDeliveryHere.setVisibility(View.GONE);
                                                    }
                                                }


                                                mFusedLocationProviderClient.removeLocationUpdates(locationCallback);


                                            }
                                        };
                                        mFusedLocationProviderClient.requestLocationUpdates(locationRequest, locationCallback, null);

                                    }
                                } else {
                                    Toast.makeText(MapLocationSelectionUpdate.this, "unable to get last location", Toast.LENGTH_SHORT).show();
                                }
                            }
                        });
            } /*else {

                Toast.makeText(this, "Turn on location", Toast.LENGTH_LONG).show();
                new AlertDialog.Builder(MapLocationSelectionUpdate.this)
                        .setTitle(getResources().getString(R.string.need_permissions))
                        .setMessage(getResources().getString(R.string.this_app_needs_permission_to_use_this_feature))

                        // Specifying a listener allows you to take an action before dismissing the dialog.
                        // The dialog is automatically dismissed when a dialog button is clicked.
                        .setPositiveButton(getResources().getString(R.string.go_to_settings), new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int which) {

                                Intent intent = new Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS);
                                startActivity(intent);
                                dialog.dismiss();
                            }
                        })

                        // A null listener allows the button to dismiss the dialog and take no further action.
                        .setNegativeButton(R.string.no, null)

                        .show();
            }*/
      /*   }else {
            requestPermissions();
        }*/
  //  }


    @Override
    protected void onResume() {
        super.onResume();
        Log.i("location", "onResume: ");
//        checkPermissions();
    }


    @Override
    protected void onRestart() {
        super.onRestart();
        Log.i("location", "onRestart: ");
        checkPermissions_new();
        isCurrentLocationBtnOn=false;
    }

    @Override
    public void onBackPressed() {
        //  super.onBackPressed();
        isClickable = false;
    }

    private void checkPermissions(){
        int permissionLocation = ContextCompat.checkSelfPermission(MapLocationSelectionUpdate.this,
                android.Manifest.permission.ACCESS_FINE_LOCATION);
     //   List<String> listPermissionsNeeded = new ArrayList<>();
        if (permissionLocation != PackageManager.PERMISSION_GRANTED) {
            if (ActivityCompat.shouldShowRequestPermissionRationale(MapLocationSelectionUpdate.this,
                    Manifest.permission.ACCESS_FINE_LOCATION)) {
                ActivityCompat.requestPermissions(MapLocationSelectionUpdate.this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_ID);
            } else {
                ActivityCompat.requestPermissions(MapLocationSelectionUpdate.this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_ID);
            }
        }else{
            getMyLocation();
           // getDeviceLocation();
        }

    }
    private void checkPermissions_new(){
        int permissionLocation = ContextCompat.checkSelfPermission(MapLocationSelectionUpdate.this,
                android.Manifest.permission.ACCESS_FINE_LOCATION);
        //   List<String> listPermissionsNeeded = new ArrayList<>();
        if (permissionLocation != PackageManager.PERMISSION_GRANTED) {
            if (ActivityCompat.shouldShowRequestPermissionRationale(MapLocationSelectionUpdate.this,
                    Manifest.permission.ACCESS_FINE_LOCATION)) {
                ActivityCompat.requestPermissions(MapLocationSelectionUpdate.this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_ID);
            } else {
                ActivityCompat.requestPermissions(MapLocationSelectionUpdate.this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_ID);
            }
        }else{
//           getMyLocation();
            getDeviceLocation();
        }

    }


    private void getMyLocation(){
        if(googleApiClient!=null) {
            if (googleApiClient.isConnected()) {
                int permissionLocation = ContextCompat.checkSelfPermission(MapLocationSelectionUpdate.this,
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
                            .requestLocationUpdates(googleApiClient, locationRequest,this);
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
                                            .checkSelfPermission(MapLocationSelectionUpdate.this,
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
                                        status.startResolutionForResult(MapLocationSelectionUpdate.this,
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
                    //    finish();
                        break;
                }
                break;
        }
    }

    @Override
    public void onLocationChanged(Location location) {
        if (isCurrentLocationBtnOn) {

            if (location != null) {
                mMap.clear();
                /* mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(mLastKnownLocation.getLatitude(), mLastKnownLocation.getLongitude()), DEFAULT_ZOOM));*/

                // mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(mLastKnownLocation.getLatitude(), mLastKnownLocation.getLongitude()), DEFAULT_ZOOM));
                lat = location.getLatitude();
                longitude = location.getLongitude();
                //  Toast.makeText(MapLocationSelectionUpdate.this, "" + lat + " "+longitude, Toast.LENGTH_SHORT).show();

                if (lat != 0.0 && longitude != 0.0) {
                    LatLng initialLatLon = new LatLng(lat, longitude);
                    mLatLngMain = initialLatLon;
                    //mMap.addMarker(new MarkerOptions().position(initialLatLon));
                    mMap.addMarker(new MarkerOptions().position(initialLatLon).icon(BitmapDescriptorFactory.fromResource(R.drawable.ic_combine_marker)).anchor(0.5f, 0.5f));
                    mMap.addCircle(new CircleOptions().center(new LatLng(lat, longitude)).radius(300).strokeColor(getResources().getColor(R.color.map_radius_new)).fillColor(getResources().getColor(R.color.map_radius_new)));
                    //  mMap.moveCamera(CameraUpdateFactory.newLatLng(initialLatLon));
                    Log.i("location", "onLocationChanged: " + initialLatLon.latitude + ", " + initialLatLon.longitude);
                    mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(initialLatLon.latitude, initialLatLon.longitude), 15.0f));
                    isCurrentLocationBtnOn= false;
                  //  mSharedPreferenceManager.storeLocationAddress(Constants.getAddress(getApplicationContext(), mLatLngMain.latitude, mLatLngMain.longitude));
                     locationAddress=Constants.getAddress(getApplicationContext(), mLatLngMain.latitude, mLatLngMain.longitude);
                    if (locationAddress!=null&&!locationAddress.isEmpty()) {
                        tvDeliveryAt.setText(locationAddress);
                        btnConfirmLocationDeliveryHere.setVisibility(View.VISIBLE);
                    }
                }
            }
        }

    }

    @Override
    public void onConnected(@Nullable Bundle bundle) {
        Log.i("location", "onConnected: ");
      checkPermissions();
       /* if(isFromWhere!=null&&!isFromWhere.isEmpty()) {

        }*/
    }

    @Override
    public void onConnectionSuspended(int i) {

    }

    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {

    }
}

    
