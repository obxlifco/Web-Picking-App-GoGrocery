package com.gogrocery.view;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.widget.NestedScrollView;
import androidx.databinding.DataBindingUtil;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import androidx.recyclerview.widget.SimpleItemAnimator;

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
import android.os.Looper;
import android.os.Parcelable;
import android.provider.Settings;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.gogrocery.Adapters.MapAddressAdapter;
import com.gogrocery.Adapters.MyAddressesAdapter;
import com.gogrocery.Adapters.StoreTypeAdapter;
import com.gogrocery.Adapters.StoreTypeOldStyleAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Interfaces.SelectAddressInterface;
import com.gogrocery.Interfaces.StoreTypeItemClickListner;
import com.gogrocery.Models.MyAddressesModel.MyAddressesModel;
import com.gogrocery.Models.StoreTypeModel.DataItem;
import com.gogrocery.Models.StoreTypeModel.StoreTypeModel;
import com.gogrocery.Models.WarehouseModel.Data;
import com.gogrocery.Models.WarehouseModel.WarehouseListModel;
import com.gogrocery.Models.WarehouseModel.WarehouseModel;
import com.gogrocery.R;
import com.gogrocery.ViewModel.StoreCategoryModel;
import com.gogrocery.databinding.ActivitySelectCategoryBinding;
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
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.android.material.bottomsheet.BottomSheetDialog;
import com.google.gson.Gson;
import com.google.gson.JsonIOException;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static java.security.AccessController.getContext;

public class SelectCategory extends AppCompatActivity implements StoreTypeItemClickListner, LocationListener, GoogleApiClient.ConnectionCallbacks,
        GoogleApiClient.OnConnectionFailedListener {
    ActivitySelectCategoryBinding activitySelectCategoryBinding;
    private SharedPreferenceManager mSharedPreferenceManager;
   // StoreTypeAdapter mStoreTypeAdapter;
   StoreTypeOldStyleAdapter mStoreTypeAdapter;
    ArrayList<StoreCategoryModel> typeModels = new ArrayList<>();
    JSONArray typeID;
    String latitude = "";
    String longitude = "";
    String from_where = "";
    String locationAddress = "";
    LoadingDialog loadingDialog;
    private List<Data> mWarehouseList;
    List<DataItem> storeCategoryList = new ArrayList<>();
    Bundle requestBundle;
    BottomSheetDialog mChangeAddressDialog;
    Dialog mSomethingwentworng;
    int PERMISSION_ID = 44;
    boolean isDeliveryAddressSelected = false;
    FusedLocationProviderClient mFusedLocationClient;
    private GoogleApiClient googleApiClient;
    List<com.gogrocery.Models.MyAddressesModel.Data> myAddressList = new ArrayList<>();
    boolean isDeliveryAddressLoaded = false;
    boolean isCategoryDataLoaded = false;
    private Location mylocation;
    boolean isCurrentLocationEnable = true;

    private final static int REQUEST_CHECK_SETTINGS_GPS = 0x1;
    private final static int REQUEST_ID_MULTIPLE_PERMISSIONS = 0x2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        activitySelectCategoryBinding = DataBindingUtil.setContentView(this, R.layout.activity_select_category);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        mFusedLocationClient = LocationServices.getFusedLocationProviderClient(this);
        setUpGClient();

        try {
            if (mSharedPreferenceManager.isLoggedIn()) {
                activitySelectCategoryBinding.ivEditType.setVisibility(View.VISIBLE);
                requestMyAddresses();
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
        hideStatusBarColor();

        initView();
        setUpOnClick();


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

    private void initView() {
        loadingDialog = new LoadingDialog(this);
        latitude = getIntent().getStringExtra("latitude");
        longitude = getIntent().getStringExtra("longitude");
        from_where = getIntent().getStringExtra("from_where");
        locationAddress = getIntent().getStringExtra("selected_address");
        isDeliveryAddressSelected = getIntent().getBooleanExtra("selected_address_id", isDeliveryAddressSelected);

        if (locationAddress != null && !locationAddress.isEmpty()) {
            activitySelectCategoryBinding.tvDeliveryTo.setText(locationAddress);
        } else {
            activitySelectCategoryBinding.tvDeliveryTo.setText(getResources().getString(R.string.show_store_delivering_to)+"\n" + mSharedPreferenceManager.getLocationAddress());
        }
        //  typeModels = (ArrayList<StoreCategoryModel>) getIntent().getSerializableExtra("select_category_list");
     /*   Log.e("latitude", latitude);
        Log.e("longitude", longitude);*/

        // Log.e("typeModels", typeModels.toString());

       /* try {
            if (from_where != null && !from_where.isEmpty()) {
                if (from_where.equals("store")) {
                    requestStoreTypeList(Double.parseDouble(latitude), Double.parseDouble(longitude));
                } else {
                    getLastLocation();
                }

            } else {
                if (latitude != null && !latitude.isEmpty() && longitude != null && !longitude.isEmpty()) {

           *//*         if (mSharedPreferenceManager.getSelectedCategoryList() != null && !mSharedPreferenceManager.getSelectedCategoryList().isEmpty()) {
                        storeCategoryList.clear();
                        storeCategoryList.addAll(mSharedPreferenceManager.getSelectedCategoryList());
                        typeModels.add(new StoreCategoryModel("All", 0, false, 0));
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

                        setUpRecyclerView();
                    } else {*//*
                    requestStoreTypeList(Double.parseDouble(latitude), Double.parseDouble(longitude));
                    //    }


                } else {
                    showNoDeliveryDialog();

                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }*/
/*
        if(isLocationEnabled()){
           getLastLocation();
        }else {
            checkPermissions();
        }*/

    }


    public void requestStoreTypeList(double latitude, double longitude) throws JSONException {
        if(Constants.isInternetConnected(getApplicationContext())) {

            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            JSONObject mJsonObject = new JSONObject();
            mJsonObject.put("latitude", latitude);
            mJsonObject.put("longitude", longitude);
            mJsonObject.put("website_id", 1);
            Log.e("latitude", latitude + "");
            Log.e("longitude", longitude + "");
            loadingDialog.showDialog();
            System.out.println("Rahul : MapLocationSelectionUpdate : requestStoreTypeList : mJsonObject : " + mJsonObject);
            JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                    Constants.BASE_URL + Constants.API_METHODS.STORE_TYPE, mJsonObject,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            loadingDialog.hideDialog();
                            System.out.println("Rahul : MapLocationSelectionUpdate : requestStoreTypeList : response : " + response);
                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            StoreTypeModel storeTypeModel = mGson.fromJson(response.toString(), StoreTypeModel.class);
                            if (storeTypeModel.getStatus() == 1) {

                                // isClickable=false;
                                if (storeTypeModel.getData().size() > 0) {
                                    storeCategoryList.clear();
                                    storeCategoryList.addAll(storeTypeModel.getData());
                                    //For new Activity
                                    int count = 0;
                                    typeModels = new ArrayList<>();
                                    typeModels.clear();
                                    typeModels.add(new StoreCategoryModel(getResources().getString(R.string.all), 0, false, 0));
                                    for (int i = 0; i < storeCategoryList.size(); i++) {
                                        boolean isSelected;
                                        if (storeCategoryList.get(i).getHas_store() == 1) {
                                            isSelected = true;
                                            count += 1;
                                        } else {
                                            isSelected = false;
                                        }


                                        StoreCategoryModel tmp = new StoreCategoryModel(storeCategoryList.get(i).getName(), storeCategoryList.get(i).getId(), isSelected, storeCategoryList.get(i).getHas_store());
                                        typeModels.add(tmp);
                                    }
                                    if (count == storeCategoryList.size()) {
                                        typeModels.set(0, new StoreCategoryModel(getResources().getString(R.string.all), 0, true, 0));
                                    }
                                    isCategoryDataLoaded = true;
                                    setUpRecyclerView();
                            /*    Intent i = new Intent(MapLocationSelectionUpdate.this, SelectCategory.class);
                                i.putExtra("latitude", latitude+"");
                                i.putExtra("longitude", longitude+"");
                                i.putExtra("select_category_list",typeModels);
                                startActivity(i);*/
                                    //showBottomSheetTypeDialog(storeCategoryList, latitude, longitude);
                                }
                            } else {
                                isCategoryDataLoaded = false;
                                // isClickable = false;
                                showNoDeliveryDialog();
                            }
                        }

                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {
                    loadingDialog.hideDialog();
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
        }else {
             Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }

    public void showNoDeliveryDialog() {
        Dialog mSomethingwentworng = new Dialog(SelectCategory.this);
        mSomethingwentworng.setCancelable(false);
        mSomethingwentworng.setContentView(R.layout.no_delivery_dialog);
        TextView txtOk = mSomethingwentworng.findViewById(R.id.txtOk);
        txtOk.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mSomethingwentworng.dismiss();
            }
        });
        mSomethingwentworng.show();

    }


    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }

    private void setUpRecyclerView() {
        //mStoreTypeAdapter = new StoreTypeAdapter(SelectCategory.this, typeModels, this);
        mStoreTypeAdapter = new StoreTypeOldStyleAdapter(SelectCategory.this, storeCategoryList, this);
        //LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.VERTICAL, false);
       GridLayoutManager mGridLayoutManager = new GridLayoutManager(getApplicationContext(), 2);
        activitySelectCategoryBinding.rvStoreType.setLayoutManager(mGridLayoutManager);
        ((SimpleItemAnimator) activitySelectCategoryBinding.rvStoreType.getItemAnimator()).setSupportsChangeAnimations(false);
       // activitySelectCategoryBinding.rvStoreType.setLayoutManager(mLayoutManager);
        activitySelectCategoryBinding.rvStoreType.setAdapter(mStoreTypeAdapter);
        activitySelectCategoryBinding.rvStoreType.setNestedScrollingEnabled(false);
    }

    private void setUpOnClick() {
        activitySelectCategoryBinding.ivBack.setOnClickListener(v -> {
            if (from_where != null && !from_where.isEmpty()) {
                Intent ivEditLocation = new Intent(SelectCategory.this, MapLocationSelectionUpdate.class);
                ivEditLocation.putExtra("from", "category");
                startActivity(ivEditLocation);
                //   finish();

            } else {
                onBackPressed();
            }


        });
        activitySelectCategoryBinding.ivEditType.setOnClickListener(v -> {
            isCurrentLocationEnable = false;
            if (mSharedPreferenceManager.isLoggedIn() && isDeliveryAddressLoaded) {
                changeAddressDialog();
            } else {
                Intent i = new Intent(SelectCategory.this, MapLocationSelectionUpdate.class);
                i.putExtra("from", "category");
                startActivity(i);
                finish();
            }
        });

        activitySelectCategoryBinding.llStart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.e("checked list", "" + Arrays.toString(typeModels.toArray()));
                if (isCategoryDataLoaded) {
                    JSONArray storetype_id = new JSONArray();
                    for (int i = 0; i < typeModels.size(); i++) {
                        if (typeModels.get(i).isSelect()) {
                            storetype_id.put(typeModels.get(i).getId());
                        }
                    }
                    if (storetype_id.length() > 0) {

                        typeID = storetype_id;

              /*  mSharedPreferenceManager.storeTypeWarehouseName(name);
                mSharedPreferenceManager.storeTypeWarehouseId(id);*/
                        if (latitude != null && !latitude.isEmpty() && longitude != null && !longitude.isEmpty()) {
                            //   requestWarehouseList(Double.parseDouble(latitude), Double.parseDouble(longitude), storetype_id);
                            if (!isDeliveryAddressSelected) {
                                mSharedPreferenceManager.storeSelectedAddressId("");

                            }
                            isCategoryDataLoaded= false;
                            Intent i = new Intent(SelectCategory.this, SelectStore.class);
                            i.putExtra("type_id", String.valueOf(typeID));
                            i.putExtra("latitude", latitude);
                            i.putExtra("longitude", longitude);
                            i.putExtra("from_where", "category");
                            i.putExtra("selected_address", String.valueOf(activitySelectCategoryBinding.tvDeliveryTo.getText()));
                            startActivity(i);
                        }
                    } else {
                        new AlertDialog.Builder(SelectCategory.this)
                                .setTitle(getResources().getString(R.string.note))
                                .setMessage(getResources().getString(R.string.please_select_category_to_start_shopping))

                                // Specifying a listener allows you to take an action before dismissing the dialog.
                                // The dialog is automatically dismissed when a dialog button is clicked.
                                .setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() {
                                    public void onClick(DialogInterface dialog, int which) {
                                        dialog.dismiss();
                                    }
                                })

                                // A null listener allows the button to dismiss the dialog and take no further action.
                                //.setNegativeButton(android.R.string.no, null)
                                .setIcon(android.R.drawable.ic_dialog_alert)
                                .show();
                        //Constants.showToastInMiddle(MapLocationSelectionUpdate.this,"Please select category to start shopping");
                        //showNoStoreDialog();
                    }

                }
            }
        });

    }

    @Override
    public void clickStoreTypeItemClickListner(long id, String name, int position) {


        try {
            if(storeCategoryList.get(position).getHas_store()==1) {

                  JSONArray storetype_id = new JSONArray();

/*    for (int i = 0; i < typeModels.size(); i++) {*/

                    //    if (typeModels.get(i).isSelect()) {
                            storetype_id.put(id);
                  //      }
                //    }
                    if (storetype_id.length() > 0) {

                        typeID = storetype_id;


                    }
                typeID = storetype_id;
                if (latitude != null && !latitude.isEmpty() && longitude != null && !longitude.isEmpty()) {
                    //   requestWarehouseList(Double.parseDouble(latitude), Double.parseDouble(longitude), storetype_id);
                    if (!isDeliveryAddressSelected) {
                        mSharedPreferenceManager.storeSelectedAddressId("");

                    }
                    isCategoryDataLoaded= false;
                    Intent i = new Intent(SelectCategory.this, SelectStore.class);
                    i.putExtra("type_id", String.valueOf(typeID));
                    i.putExtra("latitude", latitude);
                    i.putExtra("longitude", longitude);
                    i.putExtra("from_where", "category");
                    i.putExtra("selected_address", String.valueOf(activitySelectCategoryBinding.tvDeliveryTo.getText()));
                    startActivity(i);
                }
            }else{
                showNoStoreDialog();
            }

        } catch (Exception e) {
            e.printStackTrace();
        }


    }


    public void requestWarehouseList(double argLat, double argLong, JSONArray storetype_id) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(SelectCategory.this);
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
                            mWarehouseList = new ArrayList<>();
                            mWarehouseList.clear();
                            mWarehouseList.addAll(mWarehouseModel.getData());
                            Constants.VARIABLES.mWarehouseModel = mWarehouseModel;
                            //For new Activity
                            //
                            System.out.println("Rahul : MapLocationSelectionUpdate : requestWarehouseList : mWarehouseList : " + mGson.toJson(mWarehouseList));
//                            showBottomSheetDialog();
                            Intent i = new Intent(SelectCategory.this, SelectStore.class);
                            i.putExtra("type_id", typeID.toString());
                            //i.putExtra("store_list",warehouseList);
                            startActivity(i);

                        } else {
                            showNoStoreDialog();
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
                showNoStoreDialog();
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


    public void showNoStoreDialog() {
        mSomethingwentworng = new Dialog(SelectCategory.this);
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

    public void requestMyAddresses() throws JSONException {
        if (Constants.isInternetConnected(SelectCategory.this)) {
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            System.out.println("Rahul : MyAddresses1 : requestMyAddresses : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));

            JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                    Constants.BASE_URL + Constants.API_METHODS.ADDRESSES, null,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            System.out.println("Rahul : MyAddresses1 : requestMyAddresses : response : " + response);
                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            isDeliveryAddressLoaded = true;
                            try {
                                if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                    MyAddressesModel mMyAddressesModel = mGson.fromJson(mJsonObject.toString(), MyAddressesModel.class);
                                    System.out.println("Rahul : MyAddresses : requestMyAddresses : response : " + response);
                      /*      for (int i = 0 ; i<mMyAddressesModel.getData().size();i++){
                                if(mMyAddressesModel.getData().get(i).getSetPrimary().equals(1)){
                                    argAddressBookId =String.valueOf(mMyAddressesModel.getData().get(i).getId());
                                }
                            }
*/
                                    if (mMyAddressesModel.getData().size() > 0) {
                                        myAddressList = new ArrayList<>();
                                        myAddressList.clear();
                                        myAddressList.addAll(mMyAddressesModel.getData());

                                    }
                                    //  mActivityMyAddressesBinding.tvAddressesCount.setText(mMyAddressesModel.getData().size() + " SAVED ADRESSES");


                                } else {
                                    //mActivityMyAddressesBinding.tvAddressesCount.setVisibility(View.GONE);
                                    Toast.makeText(getApplicationContext(), getResources().getString(R.string.no_address_found), Toast.LENGTH_LONG).show();
                                }

                            } catch (JSONException e) {
                                e.printStackTrace();
                            }


                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {

                    System.out.println("Rahul : MyAddresses1 : requestMyAddresses : VolleyError : " + error.toString());


                }
            }) {
                @Override
                public Map<String, String> getHeaders() throws AuthFailureError {
                    HashMap<String, String> headers = new HashMap<String, String>();
                    headers.put("Content-Type", "application/json");
                    headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_token));

                    return headers;
                }


            };


            // Adding request to request queue
            queue.add(jsonObjReq);
        } else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }


    public void requestStoreTypeListFromAddress(double latitude, double longitude, String argAddress, String argAddressBookId) throws JSONException {
if(Constants.isInternetConnected(getApplicationContext())) {
    RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
    JSONObject mJsonObject = new JSONObject();
    mJsonObject.put("latitude", latitude);
    mJsonObject.put("longitude", longitude);
    mJsonObject.put("website_id", 1);
    loadingDialog.showDialog();
    Log.e("latitude_from_address", latitude + "");
    Log.e("longitude_from_address", longitude + "");
    loadingDialog.showDialog();
    System.out.println("Rahul : MapLocationSelectionUpdate : requestStoreTypeList : mJsonObject : " + mJsonObject);
    JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
            Constants.BASE_URL + Constants.API_METHODS.STORE_TYPE, mJsonObject,
            new Response.Listener<JSONObject>() {
                @Override
                public void onResponse(JSONObject response) {
                    System.out.println("Rahul : MapLocationSelectionUpdate : requestStoreTypeList : response : " + response);
                    Gson mGson = new Gson();
                    JSONObject mJsonObject = response;
                    loadingDialog.hideDialog();

                    StoreTypeModel storeTypeModel = mGson.fromJson(response.toString(), StoreTypeModel.class);
                    if (storeTypeModel.getStatus() == 1) {
                        // isClickable=false;
                        isDeliveryAddressSelected = true;
                        try {
                            requestSelectAddress(argAddressBookId);
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
                        locationAddress = getResources().getString(R.string.show_store_delivering_to) + "\n" + argAddress;
                        activitySelectCategoryBinding.tvDeliveryTo.setText(getResources().getString(R.string.show_store_delivering_to) + "\n" + argAddress);
                        mSharedPreferenceManager.storeLocationAddress(argAddress);
                        mSharedPreferenceManager.storeSelectedAddressId(argAddressBookId);
                        //   Constants.VARIABLES.SELECTED_ADDRESS_ID=argAddressBookId;
                        boolean isSelectedCategory = false;
                        if (storeTypeModel.getData().size() > 0) {
                            storeCategoryList = new ArrayList<>();
                            storeCategoryList.clear();
                            storeCategoryList.addAll(storeTypeModel.getData());
                            mSharedPreferenceManager.saveSelectedCategoryList(storeCategoryList);
                            //For new Activity
                            int count = 0;
                            typeModels = new ArrayList<>();
                            typeModels.add(new StoreCategoryModel(getResources().getString(R.string.all), 0, false, 1));
                            for (int i = 0; i < storeCategoryList.size(); i++) {
                                boolean isSelected;
                                if (storeCategoryList.get(i).getHas_store() == 1) {
                                    isSelected = true;
                                    count += 1;
                                } else {
                                    isSelected = false;
                                }
                                StoreCategoryModel tmp = new StoreCategoryModel(storeCategoryList.get(i).getName(), storeCategoryList.get(i).getId(), isSelected, storeCategoryList.get(i).getHas_store());
                                typeModels.add(tmp);
                            }

                            if (count == storeCategoryList.size()) {
                                typeModels.set(0, new StoreCategoryModel(getResources().getString(R.string.all), 0, true, 0));
                            }
                            for (int i = 0; i < typeModels.size(); i++) {
                                if (typeModels.get(i).isSelect()) {
                                    isSelectedCategory = true;
                                }
                            }
                            if (isSelectedCategory) {
                                isCategoryDataLoaded = true;

                                setUpRecyclerView();

                                  /*  Intent i = new Intent(SelectStore.this, SelectCategory.class);
                                    i.putExtra("latitude", latitude + "");
                                    i.putExtra("longitude", longitude + "");
                                    //  i.putExtra("select_category_list", typeModels);
                                    startActivity(i);*/
                            } else {
                                isCategoryDataLoaded = false;
                                showNoDeliveryDialog();
                            }
                            //showBottomSheetTypeDialog(storeCategoryList, latitude, longitude);
                        }
                    } else {
                        showNoDeliveryDialog();
                        // isClickable = false;
                        isDeliveryAddressSelected = false;
                    }
                }

            }, new Response.ErrorListener() {

        @Override
        public void onErrorResponse(VolleyError error) {
            loadingDialog.hideDialog();
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
}else {
     Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
}
    }


    public void requestSelectAddress(String argAddressBookId) throws JSONException {
if(Constants.isInternetConnected(getApplicationContext())) {
    RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
    JSONObject mJsonObject = new JSONObject();
    mJsonObject.put("addressId", argAddressBookId);

    //loadingDialog.showDialog();
    System.out.println("Rahul : requestSelectAddress : requestSelectAddress : mJsonObject : " + mJsonObject);
    JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.PATCH,
            Constants.BASE_URL + Constants.API_METHODS.ADDRESSES, mJsonObject,
            new Response.Listener<JSONObject>() {
                @Override
                public void onResponse(JSONObject response) {
                    System.out.println("Rahul : requestSelectAddress : requestSelectAddress : response : " + response);
                    Gson mGson = new Gson();
                    JSONObject mJsonObject = response;
                    //   loadingDialog.hideDialog();


                }

            }, new Response.ErrorListener() {

        @Override
        public void onErrorResponse(VolleyError error) {
            // loadingDialog.hideDialog();
            //   showNoDeliveryDialog();
            System.out.println("Rahul : requestSelectAddress : requestSelectAddress : error : " + error);
        }
    }) {
        @Override
        public Map<String, String> getHeaders() throws AuthFailureError {
            HashMap<String, String> headers = new HashMap<String, String>();
            headers.put("Content-Type", "application/json");
            headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_token));
            if (mSharedPreferenceManager.getWarehouseId() != null && !mSharedPreferenceManager.getWarehouseId().isEmpty()) {

                headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());
            } else {
                headers.put("WAREHOUSE", "0");
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
}else {
    Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
}
    }


    private void changeAddressDialog() {
        mChangeAddressDialog = new BottomSheetDialog(this, R.style.BottomSheetDialog);
        View sheetView = this.getLayoutInflater().inflate(R.layout.bottom_sheet_select_delivery_address, null);
        mChangeAddressDialog.setContentView(sheetView);
        RecyclerView mRecyclerView;
        LinearLayout addNewAddress;
        NestedScrollView nsView;


        mRecyclerView = mChangeAddressDialog.findViewById(R.id.rv_selectDeliveryAddress);
        addNewAddress = mChangeAddressDialog.findViewById(R.id.layout_top);
        nsView = mChangeAddressDialog.findViewById(R.id.nsView);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext());
        mRecyclerView.setLayoutManager(mLayoutManager);
        mRecyclerView.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        if (myAddressList.size() > 6) {
            LinearLayout.LayoutParams layoutParams = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 1200);
            layoutParams.setMargins(0, 0, 0, 0);
            nsView.setLayoutParams(layoutParams);
        } else {
            LinearLayout.LayoutParams layoutParams = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
            layoutParams.setMargins(0, 0, 0, 0);
            nsView.setLayoutParams(layoutParams);
        }


        mRecyclerView.setAdapter(new MapAddressAdapter(this, myAddressList, new SelectAddressInterface() {

            @Override
            public void onSelectedAddressData(String lat, String lng, String argAddress, String argAddressBookId) {

                new AlertDialog.Builder(SelectCategory.this)
                        .setTitle(getResources().getString(R.string.select_address))
                        .setMessage(getResources().getString(R.string.do_you_confirm_this_address))

                        // Specifying a listener allows you to take an action before dismissing the dialog.
                        // The dialog is automatically dismissed when a dialog button is clicked.
                        .setPositiveButton(R.string.yes, new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int which) {
                                try {
                                    mChangeAddressDialog.dismiss();
                                    latitude = lat;
                                    longitude = lng;
                                    requestStoreTypeListFromAddress(Double.parseDouble(lat), Double.parseDouble(lng), argAddress, argAddressBookId);
                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }
                                dialog.dismiss();
                            }
                        })

                        // A null listener allows the button to dismiss the dialog and take no further action.
                        .setNegativeButton(R.string.no, new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                mChangeAddressDialog.dismiss();
                            }
                        })

                        .show();


            }


        }));
        mRecyclerView.setNestedScrollingEnabled(false);

        try {
            if (!mChangeAddressDialog.isShowing()) {
                mChangeAddressDialog.show();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }


        addNewAddress.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent ivPinLocation = new Intent(SelectCategory.this, MapLocationSelectionUpdate.class);
                ivPinLocation.putExtra("from", "add");
                startActivity(ivPinLocation);
              //  finish();
            }
        });
        mChangeAddressDialog.show();

    }


    @Override
    protected void onPause() {

        if (mSomethingwentworng != null) {
            mSomethingwentworng.dismiss();

        }
        if (mChangeAddressDialog != null) {
            mChangeAddressDialog.dismiss();

        }
        super.onPause();

    }

    @Override
    protected void onDestroy() {
        if (mSomethingwentworng != null) {
            mSomethingwentworng.dismiss();

        }
        if (mChangeAddressDialog != null) {
            mChangeAddressDialog.dismiss();

        }
        super.onDestroy();
    }


    @SuppressLint("MissingPermission")
    private void getLastLocation() {
        /*if (checkPermissions()) {
            if (isLocationEnabled()) {*/
        mFusedLocationClient.getLastLocation().addOnCompleteListener(
                new OnCompleteListener<Location>() {
                    @Override
                    public void onComplete(@NonNull Task<Location> task) {
                        Location location = task.getResult();
                        if (location == null) {
                            requestNewLocationData();
                        } else {
                                   /* latTextView.setText(location.getLatitude()+"");
                                    lonTextView.setText(location.getLongitude()+"");*/


                            activitySelectCategoryBinding.tvDeliveryTo.setText(getResources().getString(R.string.show_store_delivering_to)+"\n" + Constants.getAddress(getApplicationContext(), location.getLatitude(), location.getLongitude()));
                            try {
                                latitude = location.getLatitude() + "";
                                longitude = location.getLongitude() + "";
                                requestStoreTypeList(location.getLatitude(), location.getLongitude());
                                //  requestStoreTypeListFromAddress(Double.parseDouble(latitude), Double.parseDouble(longitude), mSharedPreferenceManager.getLocationAddress(), mSharedPreferenceManager.getSelectedAddressId());
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }


                            System.out.println("Sukdev : splashscreen location : getLatitude : " + location.getLatitude());
                            System.out.println("Sukdev : splashscreen location : getLongitude : " + location.getLongitude());
                        }
                    }
                }
        );

    }

    private boolean isCheckPermissions() {
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED &&
                ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            return true;
        }
        return false;
    }

    private void requestPermissions() {
        if (ContextCompat.checkSelfPermission(SelectCategory.this,
                Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            if (ActivityCompat.shouldShowRequestPermissionRationale(SelectCategory.this,
                    Manifest.permission.ACCESS_FINE_LOCATION)) {
                ActivityCompat.requestPermissions(SelectCategory.this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_ID);
            } else {
                ActivityCompat.requestPermissions(SelectCategory.this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_ID);
            }
        }
    }

    private void checkPermissions() {
        int permissionLocation = ContextCompat.checkSelfPermission(SelectCategory.this,
                android.Manifest.permission.ACCESS_FINE_LOCATION);
        //   List<String> listPermissionsNeeded = new ArrayList<>();
        if (permissionLocation != PackageManager.PERMISSION_GRANTED) {
            if (ActivityCompat.shouldShowRequestPermissionRationale(SelectCategory.this,
                    Manifest.permission.ACCESS_FINE_LOCATION)) {
                ActivityCompat.requestPermissions(SelectCategory.this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_ID);
            } else {
                ActivityCompat.requestPermissions(SelectCategory.this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_ID);
            }
        } else {
            getMyLocation();
        }

    }


    private void checkPermissions_new() {
        int permissionLocation = ContextCompat.checkSelfPermission(SelectCategory.this,
                android.Manifest.permission.ACCESS_FINE_LOCATION);
        //   List<String> listPermissionsNeeded = new ArrayList<>();
        if (permissionLocation != PackageManager.PERMISSION_GRANTED) {
            if (ActivityCompat.shouldShowRequestPermissionRationale(SelectCategory.this,
                    Manifest.permission.ACCESS_FINE_LOCATION)) {
                ActivityCompat.requestPermissions(SelectCategory.this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_ID);
            } else {
                ActivityCompat.requestPermissions(SelectCategory.this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_ID);
            }
        } else {
//           getMyLocation();
            getLastLocation();
        }

    }

    private boolean isLocationEnabled() {
        LocationManager locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        return locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER) || locationManager.isProviderEnabled(
                LocationManager.NETWORK_PROVIDER
        );
    }

    @SuppressLint("MissingPermission")
    private void requestNewLocationData() {

        LocationRequest mLocationRequest = new LocationRequest();
        mLocationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
        mLocationRequest.setInterval(0);
        mLocationRequest.setFastestInterval(0);
        mLocationRequest.setNumUpdates(1);

        mFusedLocationClient = LocationServices.getFusedLocationProviderClient(this);
        mFusedLocationClient.requestLocationUpdates(
                mLocationRequest, mLocationCallback,
                Looper.myLooper()
        );

    }

    private LocationCallback mLocationCallback = new LocationCallback() {
        @Override
        public void onLocationResult(LocationResult locationResult) {
            Location mLastLocation = locationResult.getLastLocation();
      /*      latTextView.setText(mLastLocation.getLatitude()+"");
            lonTextView.setText(mLastLocation.getLongitude()+"");*/

            System.out.println("Sukdev : splashscreen location : getLatitude : " + mLastLocation.getLatitude());
            System.out.println("Sukdev : splashscreen location : getLongitude : " + mLastLocation.getLongitude());
  /*          mSharedPreferenceManager.storeLatitude("" + mLastLocation.getLatitude());
            mSharedPreferenceManager.storeLongitude("" + mLastLocation.getLongitude());
            mSharedPreferenceManager.storeLocationAddress(Constants.getAddress(getApplicationContext(),mLastLocation.getLatitude(), mLastLocation.getLongitude()));*/
            activitySelectCategoryBinding.tvDeliveryTo.setText(getResources().getString(R.string.show_store_delivering_to)+"\n" + Constants.getAddress(getApplicationContext(), mLastLocation.getLatitude(), mLastLocation.getLongitude()));
            try {
                latitude = mLastLocation.getLatitude() + "";
                longitude = mLastLocation.getLongitude() + "";
                requestStoreTypeList(mLastLocation.getLatitude(), mLastLocation.getLongitude());
                //  requestStoreTypeListFromAddress(Double.parseDouble(latitude), Double.parseDouble(longitude), mSharedPreferenceManager.getLocationAddress(), mSharedPreferenceManager.getSelectedAddressId());
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    };


/*    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 100) {

            getLastLocation();

        }
    }*/

    @Override
    protected void onResume() {
        super.onResume();
        mFusedLocationClient = LocationServices.getFusedLocationProviderClient(this);
        if (from_where != null && !from_where.isEmpty()) {
            if (from_where.equals("store")||from_where.equals("map")) {
                try {
                    requestStoreTypeList(Double.parseDouble(latitude), Double.parseDouble(longitude));
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            } else {
                if (isCurrentLocationEnable) {
                    if (isLocationEnabled()&&isCheckPermissions()) {
                        checkPermissions_new();
                    } else {
                        checkPermissions();
                    }
                }


            }

        } /*else {
            if (latitude != null && !latitude.isEmpty() && longitude != null && !longitude.isEmpty()) {
                try {
                    requestStoreTypeList(Double.parseDouble(latitude), Double.parseDouble(longitude));
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }*/
        }

 /*       try {
            if (from_where != null && !from_where.isEmpty()) {
                if (from_where.equals("store")) {
                    requestStoreTypeList(Double.parseDouble(latitude), Double.parseDouble(longitude));
                } else {

                }

            } else {
                if (latitude != null && !latitude.isEmpty() && longitude != null && !longitude.isEmpty()) {


           *//*         if (mSharedPreferenceManager.getSelectedCategoryList() != null && !mSharedPreferenceManager.getSelectedCategoryList().isEmpty()) {
                        storeCategoryList.clear();
                        storeCategoryList.addAll(mSharedPreferenceManager.getSelectedCategoryList());
                        typeModels.add(new StoreCategoryModel("All", 0, false, 0));
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

                        setUpRecyclerView();
                    } else {*//*
                    requestStoreTypeList(Double.parseDouble(latitude), Double.parseDouble(longitude));
                    //    }


                } else {
                    showNoDeliveryDialog();

                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }*/
 //   }

    private void getMyLocation() {
        if (googleApiClient != null) {
            if (googleApiClient.isConnected()) {
                int permissionLocation = ContextCompat.checkSelfPermission(SelectCategory.this,
                        Manifest.permission.ACCESS_FINE_LOCATION);
                if (permissionLocation == PackageManager.PERMISSION_GRANTED) {
                    mylocation = LocationServices.FusedLocationApi.getLastLocation(googleApiClient);
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
                                            .checkSelfPermission(SelectCategory.this,
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
                                        status.startResolutionForResult(SelectCategory.this,
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
    public void onConnected(@Nullable Bundle bundle) {
        if (from_where != null && !from_where.isEmpty()&&  isCurrentLocationEnable) {
            switch (from_where) {
                case "store":
                case "map":

                    break;
                default:
                    if (isLocationEnabled()&&isCheckPermissions()) {
                        getLastLocation();
                    } else {

                        getMyLocation();
                    }
                    break;
            }
        }

    }

    @Override
    public void onConnectionSuspended(int i) {

    }

    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {

    }

    @Override
    public void onLocationChanged(Location location) {
        if (isCurrentLocationEnable) {
            if (from_where != null && !from_where.isEmpty()) {
                if (!from_where.equals("store")) {

                    mylocation = location;
                    if (mylocation != null) {
                        activitySelectCategoryBinding.tvDeliveryTo.setText(getResources().getString(R.string.show_store_delivering_to)+"\n" + Constants.getAddress(getApplicationContext(), mylocation.getLatitude(), mylocation.getLongitude()));
                        try {
                            latitude = mylocation.getLatitude() + "";
                            longitude = mylocation.getLongitude() + "";
                            isCurrentLocationEnable = false;
                            requestStoreTypeList(mylocation.getLatitude(), mylocation.getLongitude());
                            //  requestStoreTypeListFromAddress(Double.parseDouble(latitude), Double.parseDouble(longitude), mSharedPreferenceManager.getLocationAddress(), mSharedPreferenceManager.getSelectedAddressId());
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
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
                        isCurrentLocationEnable = true;
                       getLastLocation();
                        break;
                    case Activity.RESULT_CANCELED:
                        isCurrentLocationEnable = false;
                        //  finish();
                        try {
                            latitude = mSharedPreferenceManager.getLatitude();
                            longitude = mSharedPreferenceManager.getLongitude();
                            requestStoreTypeListFromAddress(Double.parseDouble(latitude), Double.parseDouble(longitude), mSharedPreferenceManager.getLocationAddress(), mSharedPreferenceManager.getSelectedAddressId());
                            // dialog.dismiss();
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                        break;
                }
                break;
        }
    }

    @Override
    protected void onRestart() {
        super.onRestart();

    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        int permissionLocation = ContextCompat.checkSelfPermission(SelectCategory.this,
                Manifest.permission.ACCESS_FINE_LOCATION);
        if (permissionLocation == PackageManager.PERMISSION_GRANTED) {
            getLastLocation();
        }else {
            isCurrentLocationEnable = false;
            try {
                latitude = mSharedPreferenceManager.getLatitude();
                longitude = mSharedPreferenceManager.getLongitude();
                if(latitude != null && !latitude.isEmpty() && longitude != null && !longitude.isEmpty())
                {
                    requestStoreTypeListFromAddress(Double.parseDouble(latitude), Double.parseDouble(longitude), mSharedPreferenceManager.getLocationAddress(), mSharedPreferenceManager.getSelectedAddressId());
                    // dialog.dismiss();
                }else{
                    Constants.showToastInMiddle(getApplicationContext(),getResources().getString(R.string.choose_location_from_map));
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }


    }
}