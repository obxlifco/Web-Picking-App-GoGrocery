package com.gogrocery.view;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.widget.NestedScrollView;
import androidx.databinding.DataBindingUtil;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.app.Dialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.LinearLayout;
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
import com.gogrocery.Adapters.WarehouseAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.SelectAddressInterface;
import com.gogrocery.Interfaces.WarehouseItemClickListner;
import com.gogrocery.Models.MyAddressesModel.MyAddressesModel;
import com.gogrocery.Models.StoreTypeModel.DataItem;
import com.gogrocery.Models.StoreTypeModel.StoreTypeModel;
import com.gogrocery.Models.WarehouseModel.Data;
import com.gogrocery.Models.WarehouseModel.WarehouseListModel;
import com.gogrocery.Models.WarehouseModel.WarehouseModel;
import com.gogrocery.R;
import com.gogrocery.ViewModel.StoreCategoryModel;
import com.gogrocery.databinding.ActivitySelectStoreBinding;
import com.gogrocery.helper.LoadingDialog;
import com.google.android.material.bottomsheet.BottomSheetDialog;
import com.google.gson.Gson;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SelectStore extends AppCompatActivity implements WarehouseItemClickListner, SelectAddressInterface {
    ActivitySelectStoreBinding activitySelectStoreBinding;
    WarehouseAdapter mWarehouseAdapter;
    LoadingDialog loadingDialog;
    WarehouseModel mWarehouseModel;
    private SharedPreferenceManager mSharedPreferenceManager;
    private List<Data> mWarehouseList;
    String typeID = "";
    String fromWhere = "";
    String latitude = "";
    String longitude = "";
    Dialog mDialog;
    boolean isDeliveryAddressLoaded = false;
    Bundle requestBundle;
    boolean isDeliveryAddressSelected = false;
    String locationAddress = "";
    BottomSheetDialog mChangeAddressDialog;
    Dialog mSomethingwentworng;
    List<com.gogrocery.Models.MyAddressesModel.Data> myAddressList =new ArrayList<>();
    List<DataItem> storeCategoryList = new ArrayList<>();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        activitySelectStoreBinding = DataBindingUtil.setContentView(this, R.layout.activity_select_store);
        loadingDialog = new LoadingDialog(this);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
       locationAddress = getIntent().getStringExtra("selected_address");
        if (locationAddress != null && !locationAddress.isEmpty()) {
            activitySelectStoreBinding.tvDeliveryTo.setText(locationAddress);
        } else {
            activitySelectStoreBinding.tvDeliveryTo.setText(getResources().getString(R.string.show_store_delivering_to)+"\n" + mSharedPreferenceManager.getLocationAddress());
        }
        try {
            if(mSharedPreferenceManager.isLoggedIn()) {
                activitySelectStoreBinding.ivEditType.setVisibility(View.VISIBLE);
                requestMyAddresses();
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
        hideStatusBarColor();

        initView();
        setUpOnClick();
    }


    private void initView() {
        mWarehouseModel = new WarehouseModel();

        typeID = getIntent().getStringExtra("type_id");
        fromWhere = getIntent().getStringExtra("from_where");
        latitude = getIntent().getStringExtra("latitude");
        longitude = getIntent().getStringExtra("longitude");
      /*  Log.e("latitude", latitude);
        Log.e("longitude", longitude);*/
        try {
            if(typeID!=null&&!typeID.isEmpty()) {
                JSONArray jsonArray = new JSONArray(typeID);
                requestWarehouseList(Double.parseDouble(latitude), Double.parseDouble(longitude), jsonArray);
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

       if(fromWhere!=null&&!fromWhere.isEmpty()&&fromWhere.equals("home")) {
           activitySelectStoreBinding.ivClose.setVisibility(View.VISIBLE);
       }else {
           activitySelectStoreBinding.ivClose.setVisibility(View.GONE);
       }

    }


    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }


    public void requestWarehouseList(double argLat, double argLong, JSONArray storetype_id) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(SelectStore.this);
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
                        mSharedPreferenceManager.storeLatitude("" + latitude);
                        mSharedPreferenceManager.storeLongitude("" + longitude);
                        System.out.println("Rahul : MapLocationSelectionUpdate : requestWarehouseList : response : " + response);
                        WarehouseModel mWarehouseModel = mGson.fromJson(response.toString(), WarehouseModel.class);
                        if (!mWarehouseModel.getStatus().equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                            mWarehouseList = new ArrayList<>();
                            mWarehouseList.clear();
                            mWarehouseList.addAll(mWarehouseModel.getData());
                            setUpRecyclerview();


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
        Dialog mSomethingwentworng = new Dialog(SelectStore.this);
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

    private void setUpRecyclerview() {
        mWarehouseAdapter = new WarehouseAdapter(SelectStore.this, mWarehouseList, this);
        GridLayoutManager mLayoutManager = new GridLayoutManager(getApplicationContext(), 2);
        activitySelectStoreBinding.rvWarehouse.setLayoutManager(mLayoutManager);
        activitySelectStoreBinding.rvWarehouse.setAdapter(mWarehouseAdapter);
        activitySelectStoreBinding.rvWarehouse.setNestedScrollingEnabled(false);
    }

    private void setUpOnClick() {
        activitySelectStoreBinding.ivBack.setOnClickListener(v -> {
            if(fromWhere!=null&&!fromWhere.isEmpty()){
                Intent i = new Intent(SelectStore.this, SelectCategory.class);
                i.putExtra("latitude", latitude);
                i.putExtra("longitude", longitude);
                i.putExtra("select_category_list","");
                i.putExtra("from_where","store");
                i.putExtra("selected_address_id",isDeliveryAddressSelected);
                i.putExtra("selected_address", String.valueOf(activitySelectStoreBinding.tvDeliveryTo.getText()));
                startActivity(i);
                finish();

            }else {
                onBackPressed();

            }

        });
        activitySelectStoreBinding.ivEditType.setOnClickListener(v->{

                if(mSharedPreferenceManager.isLoggedIn()&&isDeliveryAddressLoaded) {
                    changeAddressDialog();
                }else {
                    Intent i = new Intent(SelectStore.this, MapLocationSelectionUpdate.class);
                    startActivity(i);
                    finish();
                }
        });

        activitySelectStoreBinding.ivClose.setOnClickListener(v->{
            finish();
        });
    }

    @Override
    public void clickWarehouseItemClickListner(double argLat, double argLong, String argWarehouseId, String argWarehouseName) {
        System.out.println("Rahul : SelectStore : clickWarehouseItemClickListner : argWarehouseID : " + argWarehouseId);
        System.out.println("Rahul : SelectStore : clickWarehouseItemClickListner : getWarehouseId : " + new SharedPreferenceManager(getApplicationContext()).getWarehouseId());
        try {
            String[] selectedAddress=String.valueOf(activitySelectStoreBinding.tvDeliveryTo.getText()).split("\n");
            mSharedPreferenceManager.storeLocationAddress(selectedAddress[1]);
            System.out.println("Rahul : SelectAddress : clickWarehouseItemClickListner : argSelectAddress : " + selectedAddress[1]);
        }catch (Exception e){
            e.printStackTrace();
        }

        if (new SharedPreferenceManager(getApplicationContext()).getWarehouseId().isEmpty()) {
            Intent i = new Intent(SelectStore.this, MainActivityNew.class);
            startActivity(i);
            SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
            mSharedPreferenceManager.storeLatLong(String.valueOf(argLat) + "," + argLong);
            mSharedPreferenceManager.storeWarehouseId(argWarehouseId);
            mSharedPreferenceManager.storeWarehouseName(argWarehouseName);
            mSharedPreferenceManager.storeTypeWarehouseName(argWarehouseName);
            mSharedPreferenceManager.storeTypeWarehouseId(String.valueOf(typeID));

            finish();
        } else if (argWarehouseId.equals(new SharedPreferenceManager(getApplicationContext()).getWarehouseId())) {
            Intent i = new Intent(SelectStore.this, MainActivityNew.class);
            startActivity(i);
            SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
            mSharedPreferenceManager.storeLatLong(String.valueOf(argLat) + "," + argLong);
            mSharedPreferenceManager.storeWarehouseId(argWarehouseId);
            mSharedPreferenceManager.storeWarehouseName(argWarehouseName);
            mSharedPreferenceManager.storeTypeWarehouseName(argWarehouseName);
            mSharedPreferenceManager.storeTypeWarehouseId(String.valueOf(typeID));

            finish();
        } else if (Constants.VARIABLES.CART_COUNT == 0) {
            Intent i = new Intent(SelectStore.this, MainActivityNew.class);
            startActivity(i);
            SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
            mSharedPreferenceManager.storeLatLong(String.valueOf(argLat) + "," + argLong);
            mSharedPreferenceManager.storeWarehouseId(argWarehouseId);
            mSharedPreferenceManager.storeWarehouseName(argWarehouseName);
            mSharedPreferenceManager.storeTypeWarehouseName(argWarehouseName);
            mSharedPreferenceManager.storeTypeWarehouseId(String.valueOf(typeID));

            finish();
        } else {

            mDialog= new Dialog(SelectStore.this);
            mDialog.setCancelable(false);
            mDialog.setContentView(R.layout.change_warehouse_dialog);

            Button btnYes, btnNo;
            btnYes = mDialog.findViewById(R.id.btnYes);
            btnNo = mDialog.findViewById(R.id.btnNo);


            btnYes.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    try {
                        requestEmptyCart(argLat, argLong, argWarehouseId, argWarehouseName);
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


    public void requestMyAddresses() throws JSONException {
        if (Constants.isInternetConnected(SelectStore.this)) {
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
                                    if(mMyAddressesModel.getData().size()>0) {
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



    @Override
    protected void onPause() {

        if (mDialog != null) {
            mDialog.dismiss();

        }
        if (mChangeAddressDialog != null) {
            mChangeAddressDialog.dismiss();

        }
        if (mSomethingwentworng != null) {
            mSomethingwentworng.dismiss();

        }
        super.onPause();

    }

    @Override
    protected void onDestroy() {
        if (mDialog != null) {
            mDialog.dismiss();

        }
        if (mChangeAddressDialog != null) {
            mChangeAddressDialog.dismiss();

        }
        if (mSomethingwentworng != null) {
            mSomethingwentworng.dismiss();

        }
        super.onDestroy();
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
                                //Constants.VARIABLES.SELECTED_ADDRESS_ID="";

                                new DatabaseHandler(getApplicationContext()).deleteAllRecord();
                                Intent i = new Intent(SelectStore.this, MainActivityNew.class);
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

    @Override
    public void onSelectedAddressData(String lat, String lng, String argAddress, String argAddressBookId) {
        this.latitude = lat;
        this.longitude=lng;
        try {
            requestStoreTypeList(Double.parseDouble(lat),Double.parseDouble(lng),argAddress,argAddressBookId);
        } catch (JSONException e) {
            e.printStackTrace();
        }


    }


    public void requestStoreTypeList(double latitude, double longitude ,String argAddress, String argAddressBookId) throws JSONException {

        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("latitude", latitude);
        mJsonObject.put("longitude", longitude);
        mJsonObject.put("website_id", 1);
loadingDialog.showDialog();
        System.out.println("Rahul : MapLocationSelectionUpdate : requestStoreTypeList : mJsonObject : " + mJsonObject);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.STORE_TYPE, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : MapLocationSelectionUpdate : requestStoreTypeList : response : " + response);
                        Gson mGson = new Gson();
                        loadingDialog.hideDialog();
                        JSONObject mJsonObject = response;
                        StoreTypeModel storeTypeModel = mGson.fromJson(response.toString(), StoreTypeModel.class);
                        if (storeTypeModel.getStatus() == 1) {
                            isDeliveryAddressSelected = true;
                            // isClickable=false;
                            try {
                                requestSelectAddress(argAddressBookId);
                            } catch (JSONException e) {

                            }
                            activitySelectStoreBinding.tvDeliveryTo.setText(getResources().getString(R.string.show_store_delivering_to)+"\n" +argAddress);

                            mSharedPreferenceManager.storeLocationAddress(argAddress);
                            mSharedPreferenceManager.storeSelectedAddressId(argAddressBookId);
                           // Constants.VARIABLES.SELECTED_ADDRESS_ID=argAddressBookId;
                            boolean isSelectedCategory = false;
                            if (storeTypeModel.getData().size() > 0) {
                                storeCategoryList.clear();
                                storeCategoryList.addAll(storeTypeModel.getData());
                                mSharedPreferenceManager.saveSelectedCategoryList(storeCategoryList);
                                //For new Activity
                                ArrayList<StoreCategoryModel> typeModels = new ArrayList<>();
                                typeModels.add(new StoreCategoryModel(getResources().getString(R.string.all), 0, false, 1));
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

                                    Intent i = new Intent(SelectStore.this, SelectCategory.class);
                                    i.putExtra("latitude", latitude + "");
                                    i.putExtra("longitude", longitude + "");
                                    i.putExtra("from_where","store");
                                    i.putExtra("selected_address_id",isDeliveryAddressSelected);
                                    //  i.putExtra("select_category_list", typeModels);
                                    startActivity(i);
                                } else {
                                    showNoDeliveryDialog();
                                }
                                //showBottomSheetTypeDialog(storeCategoryList, latitude, longitude);
                            }
                        } else {
                            showNoDeliveryDialog();
                            // isClickable = false;

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
    }
/*
    @Override
    public void addNewAddress() {
        Intent ivPinLocation = new Intent(SelectStore.this, MapLocationSelectionUpdate.class);
        ivPinLocation.putExtra("from","add");
        startActivity(ivPinLocation);
        finish();
    }
*/



    public void showNoDeliveryDialog() {
        mSomethingwentworng = new Dialog(SelectStore.this);
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
        if(myAddressList.size()>6) {
            LinearLayout.LayoutParams layoutParams = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 1200);
            layoutParams.setMargins(0, 0, 0, 0);
            nsView.setLayoutParams(layoutParams);
        }else {
            LinearLayout.LayoutParams layoutParams = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
            layoutParams.setMargins(0, 0, 0, 0);
            nsView.setLayoutParams(layoutParams);
        }

        mRecyclerView.setAdapter(new MapAddressAdapter(this, myAddressList, new SelectAddressInterface() {

            @Override
            public void onSelectedAddressData(String lat, String lng, String argAddress, String argAddressBookId) {

                new AlertDialog.Builder(SelectStore.this)
                        .setTitle(getResources().getString(R.string.select_address))
                        .setMessage(getResources().getString(R.string.do_you_confirm_this_address))

                        // Specifying a listener allows you to take an action before dismissing the dialog.
                        // The dialog is automatically dismissed when a dialog button is clicked.
                        .setPositiveButton(R.string.yes, new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int which) {
                                try {
                                    mChangeAddressDialog.dismiss();
                                    requestStoreTypeList(Double.parseDouble(lat),Double.parseDouble(lng),argAddress,argAddressBookId);
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
                Intent ivPinLocation = new Intent(SelectStore.this, MapLocationSelectionUpdate.class);
                ivPinLocation.putExtra("from","add");
                startActivity(ivPinLocation);
               // finish();
            }
        });
        mChangeAddressDialog.show();

    }


    public void requestSelectAddress( String argAddressBookId) throws JSONException {

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
                if(mSharedPreferenceManager.getWarehouseId()!=null&&!mSharedPreferenceManager.getWarehouseId().isEmpty()) {

                    headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());
                }else {
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
    }

}