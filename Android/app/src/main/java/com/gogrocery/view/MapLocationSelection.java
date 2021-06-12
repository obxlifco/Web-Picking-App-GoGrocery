package com.gogrocery.view;

import android.app.Dialog;
import android.content.Intent;

import androidx.fragment.app.FragmentActivity;

import android.os.Bundle;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.gogrocery.Adapters.WarehouseAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Customs.GridSpacingItemDecoration;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.WarehouseItemClickListner;
import com.gogrocery.Models.WarehouseModel.Data;
import com.gogrocery.Models.WarehouseModel.WarehouseModel;
import com.gogrocery.R;
import com.google.android.gms.common.GooglePlayServicesNotAvailableException;
import com.google.android.gms.common.GooglePlayServicesRepairableException;
import com.google.android.gms.location.places.ui.PlaceAutocomplete;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MapLocationSelection extends FragmentActivity implements OnMapReadyCallback, WarehouseItemClickListner {

    private GoogleMap mMap;
    private MarkerOptions mMarker;
    private List<Data> mWarehouseList = new ArrayList<>();
    private Dialog mBottomSheetDialog;
    private LatLng mLatLngMain;
    private SharedPreferenceManager mSharedPreferenceManager;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_map_location_selection);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
        mMarker = new MarkerOptions();
        mMarker.draggable(true);

        findViewById(R.id.btnConfirmLocation).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                if (findViewById(R.id.progressSpinKitView).getVisibility() == View.GONE) {
                    try {
                        requestWarehouseList(mLatLngMain.latitude, mLatLngMain.longitude);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            }
        });

        findViewById(R.id.svLocation).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent =
                        null;
                try {
                    intent = new PlaceAutocomplete.IntentBuilder(PlaceAutocomplete.MODE_OVERLAY)
                            .build(MapLocationSelection.this);
                } catch (GooglePlayServicesRepairableException e) {
                    e.printStackTrace();
                } catch (GooglePlayServicesNotAvailableException e) {
                    e.printStackTrace();
                }
                startActivityForResult(intent, 101);
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
        double lat = 0.0;
        double longitude = 0.0;
try {

}catch (Exception e){
    e.printStackTrace();
}
        if (mSharedPreferenceManager.getLatitude().isEmpty()) {
            lat = getIntent().getExtras().getDouble("lat");
            longitude = getIntent().getExtras().getDouble("long");

            mSharedPreferenceManager.storeLatitude("" + lat);
            mSharedPreferenceManager.storeLongitude("" + longitude);

        } else {
            lat = Double.parseDouble(mSharedPreferenceManager.getLatitude());
            longitude = Double.parseDouble(mSharedPreferenceManager.getLongitude());

        }
//Paid API KEY
        //AIzaSyDwJfFz9Hyur4RkbEa_Hlt6Fkibr6rYhJo

        // Add a marker in Sydney and move the camera
        //LatLng initialLatLon = new LatLng(25.2048, 55.2708);
        LatLng initialLatLon = new LatLng(lat, longitude);

        mLatLngMain = initialLatLon;
        mMap.addMarker(new MarkerOptions().position(initialLatLon));
        mMap.moveCamera(CameraUpdateFactory.newLatLng(initialLatLon));
        mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(initialLatLon.latitude, initialLatLon.longitude), 12.0f));
        mMap.setOnMapClickListener(new GoogleMap.OnMapClickListener() {
            @Override
            public void onMapClick(LatLng latLng) {
                LatLng newLoca = new LatLng(latLng.latitude, latLng.longitude);
                mSharedPreferenceManager.storeLatitude("" + newLoca.latitude);
                mSharedPreferenceManager.storeLongitude("" + newLoca.longitude);
                mLatLngMain = latLng;
                mMap.clear();
                mMap.addMarker(mMarker.position(newLoca).title("Your selected location"));
                mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(newLoca.latitude, newLoca.longitude), 12.0f));


            }
        });
    }

    private void showBottomSheetDialog() {

        mBottomSheetDialog = new Dialog(MapLocationSelection.this, R.style.DialogSlideAnimStyle);
        mBottomSheetDialog.setContentView(R.layout.bottom_sheet_warehouse);
        mBottomSheetDialog.setCancelable(true);

        RecyclerView mRecyclerView = mBottomSheetDialog.findViewById(R.id.rvWarehouse);

        ImageView ivBack = mBottomSheetDialog.findViewById(R.id.ivBack);

        ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mBottomSheetDialog.dismiss();
            }
        });

        WarehouseAdapter mWarehouseAdapter = new WarehouseAdapter(MapLocationSelection.this, mWarehouseList, this);
        GridLayoutManager mGridLayoutManager = new GridLayoutManager(getApplicationContext(), 2);
        mRecyclerView.setLayoutManager(mGridLayoutManager);
        mRecyclerView.addItemDecoration(new GridSpacingItemDecoration(2, GridSpacingItemDecoration.dpToPx(getApplicationContext(), 10), true));

        // mRecyclerView.addItemDecoration(new ItemDecorationAlbumColumns(10, 100));
        mRecyclerView.setLayoutManager(mGridLayoutManager);
        mRecyclerView.setItemAnimator(new DefaultItemAnimator());
        mRecyclerView.setAdapter(mWarehouseAdapter);
        mRecyclerView.setNestedScrollingEnabled(false);

        try {
            if (!mBottomSheetDialog.isShowing()) {
                mBottomSheetDialog.show();
            }
        }catch (Exception e){
            e.printStackTrace();
        }


       /* getWindow().setGravity(Gravity.BOTTOM);
        getWindow().setBackgroundDrawableResource(android.R.color.transparent);*/
    }

    @Override
    protected void onPause() {

        if (mBottomSheetDialog != null) {
            mBottomSheetDialog.dismiss();
        }
        super.onPause();

    }

    @Override
    protected void onDestroy() {
        if (mBottomSheetDialog != null) {
            mBottomSheetDialog.dismiss();
        }

        super.onDestroy();
    }

    public void requestWarehouseList(double argLat, double argLong) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        findViewById(R.id.progressSpinKitView).setVisibility(View.VISIBLE);
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("latitude", argLat);
        mJsonObject.put("longitude", argLong);
        mJsonObject.put("website_id", 1);

        System.out.println("Rahul : MapLocationSelection : requestWarehouseList : mJsonObject : " + mJsonObject);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.WAREHOUSE_LIST, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {

                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        System.out.println("Rahul : MapLocationSelection : requestWarehouseList : response : " + response);
                        WarehouseModel mWarehouseModel = mGson.fromJson(response.toString(), WarehouseModel.class);
                        if (!mWarehouseModel.getStatus().equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                            mWarehouseList.clear();
                            mWarehouseList.addAll(mWarehouseModel.getData());
                            System.out.println("Rahul : MapLocationSelection : requestWarehouseList : mWarehouseList : " + mGson.toJson(mWarehouseList));
                            showBottomSheetDialog();

                        } else {

                        }
                        findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                    }

                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : MainActivityNew : requestViewCart : VolleyError : " + error.toString());
                findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                showNoDeliveryDialog();
            }
        })

        {
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
        Dialog mSomethingwentworng = new Dialog(this);
        mSomethingwentworng.setCancelable(true);
        mSomethingwentworng.setContentView(R.layout.no_delivery_dialog);

        mSomethingwentworng.show();

    }

    public void requestEmptyCart(double argLat, double argLong, String argWarehouseID, String argWarehouseName) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        findViewById(R.id.progressSpinKitView).setVisibility(View.VISIBLE);
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));
        mJsonObject.put("website_id", 1);

        System.out.println("Rahul : MapLocationSelection : requestEmptyCart : mJsonObject : " + mJsonObject.toString());

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.EMPTY_CART, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : MapLocationSelection : requestEmptyCart : response : " + response.toString());
                        findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                        try {
                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                new DatabaseHandler(getApplicationContext()).deleteAllRecord();
                                Intent i = new Intent(MapLocationSelection.this, MainActivityNew.class);
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
                findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                System.out.println("Rahul : MapLocationSelection : requestEmptyCart : VolleyError : " + error.toString());
            }
        })

        {
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


    @Override
    public void clickWarehouseItemClickListner(double argLat, double argLong, String argWarehouseID, String argWarehouseName) {

        System.out.println("Rahul : MapLocationSelection : clickWarehouseItemClickListner : argWarehouseID : " + argWarehouseID);
        System.out.println("Rahul : MapLocationSelection : clickWarehouseItemClickListner : getWarehouseId : " + new SharedPreferenceManager(getApplicationContext()).getWarehouseId());
        if (new SharedPreferenceManager(getApplicationContext()).getWarehouseId().isEmpty()) {
            Intent i = new Intent(MapLocationSelection.this, MainActivityNew.class);
            startActivity(i);
            SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
            mSharedPreferenceManager.storeLatLong(String.valueOf(argLat) + "," + argLong);
            mSharedPreferenceManager.storeWarehouseId(argWarehouseID);
            mSharedPreferenceManager.storeWarehouseName(argWarehouseName);
            finish();
        } else if (argWarehouseID.equals(new SharedPreferenceManager(getApplicationContext()).getWarehouseId())) {
            Intent i = new Intent(MapLocationSelection.this, MainActivityNew.class);
            startActivity(i);
            SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
            mSharedPreferenceManager.storeLatLong(String.valueOf(argLat) + "," + argLong);
            mSharedPreferenceManager.storeWarehouseId(argWarehouseID);
            mSharedPreferenceManager.storeWarehouseName(argWarehouseName);
            finish();
        } else {

            Dialog mDialog = new Dialog(this);
            mDialog.setCancelable(false);
            mDialog.setContentView(R.layout.change_warehouse_dialog);

            Button btnYes, btnNo;
            btnYes = mDialog.findViewById(R.id.btnYes);
            btnNo = mDialog.findViewById(R.id.btnNo);


            btnYes.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    try {
                        requestEmptyCart(argLat, argLong, argWarehouseID, argWarehouseName);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            });

            btnNo.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    mDialog.dismiss();
                }
            });
            mDialog.show();


        }

    }

}
