package com.gogrocery.view;

import android.content.DialogInterface;
import android.content.Intent;

import androidx.appcompat.app.AlertDialog;
import androidx.databinding.DataBindingUtil;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Build;
import android.os.Bundle;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.gogrocery.Adapters.MyAddressesAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Customs.RecyclerTouchListener;
import com.gogrocery.Interfaces.MyAddressSelected;
import com.gogrocery.Models.MyAddressesModel.Data;
import com.gogrocery.Models.MyAddressesModel.MyAddressesModel;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityMyAddressesBinding;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MyAddresses extends AppCompatActivity implements MyAddressSelected {

    private ActivityMyAddressesBinding mActivityMyAddressesBinding;
    private SharedPreferenceManager mSharedPreferenceManager;
    private MyAddressesAdapter mMyAddressesAdapter;
    private List<Data> mAddressesList = new ArrayList<>();
    private RecyclerTouchListener onTouchListener;
    private String argName = "", argMobile = "", argAddress = "", argAddressBookId = "",latitude="",lng="";
    private String isFrom = "";
boolean isSelectAddress = false;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityMyAddressesBinding = DataBindingUtil.setContentView(this, R.layout.activity_my_addresses);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
hideStatusBarColor();

        if (getIntent().getExtras() != null) {
            if (getIntent().getStringExtra("from").equals("Delivery_Detail")) {

                isFrom = "Delivery_Detail";
               mActivityMyAddressesBinding.tvToolbarTitle.setText(getResources().getString(R.string.select_address));
                mActivityMyAddressesBinding.cvFooter.setVisibility(View.VISIBLE);

                mActivityMyAddressesBinding.btnDeliverHere.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {

                        try {
                            if(argAddressBookId != null &&!argAddressBookId.equals("")){

                                requestSelectAddress(argAddressBookId);
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();


                        }

                    }
                });
            }else {
                mActivityMyAddressesBinding.cvFooter.setVisibility(View.GONE);
                mActivityMyAddressesBinding.tvToolbarTitle.setText(getResources().getString(R.string.myaddresses));
            }
        }
        setMyAddressesRecyclerView();

        /*try {
            requestMyAddresses();
        } catch (JSONException e) {
            e.printStackTrace();
        }*/


        mActivityMyAddressesBinding.ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(isFrom.equals("Delivery_Detail")&&mAddressesList.size() ==0){
                    Intent cvAddNewAddress = new Intent(MyAddresses.this, MyCart.class);
                    startActivity(cvAddNewAddress);
                    finish();
                }else{
                    finish();
                }

            }
        });

        mActivityMyAddressesBinding.ivAddAddress.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent cvAddNewAddress = new Intent(MyAddresses.this, AddNewAddress.class);
                cvAddNewAddress.putExtra("from","");
                startActivityForResult(cvAddNewAddress, 1);
            }
        });


     /*   onTouchListener = new RecyclerTouchListener(this, mActivityMyAddressesBinding.rvMyAddresses);
        onTouchListener
                .setClickable(new RecyclerTouchListener.OnRowClickListener() {
                    @Override
                    public void onRowClicked(int position) {
                        //Toast.makeText(getApplicationContext(), "Row " + (position + 1) + " clicked!", Toast.LENGTH_LONG).show();
                    }

                    @Override
                    public void onIndependentViewClicked(int independentViewID, int position) {
                        //Toast.makeText(getApplicationContext(), "Button in row " + (position + 1) + " clicked!", Toast.LENGTH_LONG).show();
                    }
                })
                .setLongClickable(true, new RecyclerTouchListener.OnRowLongClickListener() {
                    @Override
                    public void onRowLongClicked(int position) {
                        // Toast.makeText(getApplicationContext(), "Row " + (position + 1) + " long clicked!", Toast.LENGTH_LONG).show();
                    }
                })
                .setSwipeOptionViews(R.id.add, R.id.edit, R.id.change)
                .setSwipeable(R.id.cvDeliveryDetail, R.id.rowBG, new RecyclerTouchListener.OnSwipeOptionsClickListener() {
                    @Override
                    public void onSwipeOptionClicked(int viewID, int position) {
                        String message = "";
                        if (viewID == R.id.add) {
                            message += "Add";
                            try {
                                requestDeleteAddress(String.valueOf(mAddressesList.get(position).getId()), position);
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }

                        } else if (viewID == R.id.edit) {
                            message += "Edit";
                            *//*Intent edt = new Intent(MyAddresses.this, AddNewAddress.class);
                            edt.putExtra("edit_address", new Gson().toJson(mAddressesList.get(position)));
                            startActivity(edt);*//*

                        } *//*else if (viewID == R.id.change) {
                            message += "Change";
                        }*//*
                        message += " clicked for row " + (position + 1);
                        // Toast.makeText(getApplicationContext(), message, Toast.LENGTH_LONG).show();
                    }
                });*/

        // onTouchListener.openSwipeOptions(0);

    }


    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        System.out.println("Rahul : MyAddresses : onActivityResult : 1 : ");
        if (requestCode == 1) {
            System.out.println("Rahul : MyAddresses : onActivityResult : 2 : ");
            if (data != null) {

                System.out.println("Rahul : MyAddresses : onActivityResult : selected_name : " + data.getStringExtra("selected_name"));
                argName = data.getStringExtra("selected_name");
                argMobile = data.getStringExtra("selected_mobile");
                argAddress = data.getStringExtra("selected_address");
                argAddressBookId = data.getStringExtra("selected_address_book_id");
                mSharedPreferenceManager.storeSelectedAddressId(argAddressBookId);
                mSharedPreferenceManager.storeLocationAddress(argAddress);

               // Constants.VARIABLES.SELECTED_ADDRESS_ID=argAddressBookId;
                Intent intent = new Intent();

                intent.putExtra("selected_name", argName);
                intent.putExtra("selected_mobile", argMobile);
                intent.putExtra("selected_address", argAddress);
                intent.putExtra("selected_address_book_id", argAddressBookId);
                intent.putExtra("latitude", latitude);
                intent.putExtra("longitude", lng);
                setResult(1, intent);

            }
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        //  mActivityMyAddressesBinding.rvMyAddresses.addOnItemTouchListener(onTouchListener);
        try {
            requestMyAddresses();

        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        //mActivityMyAddressesBinding.rvMyAddresses.removeOnItemTouchListener(onTouchListener);
    }

    private void setMyAddressesRecyclerView() {
        mMyAddressesAdapter = new MyAddressesAdapter(getApplicationContext(),MyAddresses.this, mAddressesList, this, isFrom);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.VERTICAL, false);
        mActivityMyAddressesBinding.rvMyAddresses.setLayoutManager(mLayoutManager);
        /*mActivityMyAddressesBinding.rvMyAddresses.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        mActivityMyAddressesBinding.rvMyAddresses.setItemAnimator(new DefaultItemAnimator());*/
        mActivityMyAddressesBinding.rvMyAddresses.setAdapter(mMyAddressesAdapter);
        mActivityMyAddressesBinding.rvMyAddresses.setNestedScrollingEnabled(false);
    }


    public void requestMyAddresses() throws JSONException {
        if (Constants.isInternetConnected(MyAddresses.this)) {
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            System.out.println("Rahul : MyAddresses1 : requestMyAddresses : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
            mActivityMyAddressesBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                    Constants.BASE_URL + Constants.API_METHODS.ADDRESSES, null,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            System.out.println("Rahul : MyAddresses1 : requestMyAddresses : response : " + response);
                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
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

                                        mAddressesList.clear();
                                        mAddressesList.addAll(mMyAddressesModel.getData());
                                        mMyAddressesAdapter.notifyDataSetChanged();
                                    }else {
                                        Toast.makeText(getApplicationContext(), getResources().getString(R.string.no_address_found), Toast.LENGTH_LONG).show();
                                        mActivityMyAddressesBinding.cvFooter.setVisibility(View.GONE);
                                    }
                                    //  mActivityMyAddressesBinding.tvAddressesCount.setText(mMyAddressesModel.getData().size() + " SAVED ADRESSES");


                                } else {
                                    mActivityMyAddressesBinding.cvFooter.setVisibility(View.GONE);
                                    //mActivityMyAddressesBinding.tvAddressesCount.setVisibility(View.GONE);
                                    Toast.makeText(getApplicationContext(), getResources().getString(R.string.no_address_found), Toast.LENGTH_LONG).show();
                                }

                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                            mActivityMyAddressesBinding.progressSpinKitView.setVisibility(View.GONE);

                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {

                    System.out.println("Rahul : MyAddresses1 : requestMyAddresses : VolleyError : " + error.toString());
                    mActivityMyAddressesBinding.progressSpinKitView.setVisibility(View.GONE);

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

    public void requestDeleteAddress(String argAddrerssId, int argPosition) throws JSONException {
        if (Constants.isInternetConnected(MyAddresses.this)) {
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            System.out.println("Rahul : MyAddresses : requestDeleteAddress : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
            mActivityMyAddressesBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                    Constants.BASE_URL + Constants.API_METHODS.DELETE_ADDRESS + argAddrerssId + "/", null,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            System.out.println("Rahul : MyAddresses : requestDeleteAddress : response : " + response);
                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            try {
                                if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {


                                    mAddressesList.remove(argPosition);
                                    mMyAddressesAdapter.notifyItemRemoved(argPosition);
                                    mMyAddressesAdapter.notifyItemRangeChanged(argPosition, mAddressesList.size());
                                    // mActivityMyAddressesBinding.tvAddressesCount.setText(mAddressesList.size() + " SAVED ADRESSES");
                                    requestMyAddresses();

                                } else {
                                    //   mActivityMyAddressesBinding.tvAddressesCount.setVisibility(View.GONE);
                                    Toast.makeText(getApplicationContext(), getResources().getString(R.string.no_address_found), Toast.LENGTH_LONG).show();
                                }

                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                            mActivityMyAddressesBinding.progressSpinKitView.setVisibility(View.GONE);

                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {

                    System.out.println("Rahul : MyAddresses : requestMyAddresses : VolleyError : " + error.toString());

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



    public void requestSelectAddressNew( String argAddressBookId) throws JSONException {

        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("addressId", argAddressBookId);


        System.out.println("Rahul : jsonPayload : requestSelectAddress : mJsonObject : " + mJsonObject);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.PATCH,
                Constants.BASE_URL + Constants.API_METHODS.ADDRESSES, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : requestSelectAddress : requestSelectAddress : response : " + response);
                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        mSharedPreferenceManager.storeSelectedAddressId(argAddressBookId);
                      //  Constants.VARIABLES.SELECTED_ADDRESS_ID=argAddressBookId;

                    }

                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {


                System.out.println("Rahul : requestSelectAddress : requestSelectAddress : error : " + error);
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

    public void requestSelectAddress(String argAddrerssId) throws JSONException {
        if (Constants.isInternetConnected(MyAddresses.this)) {
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

            JSONObject mjsonObj = new JSONObject();
            mjsonObj.put("address_id", argAddrerssId);

            System.out.println("Rahul : MyAddresses : request_select address : token : " + mSharedPreferenceManager.getUserProfileDetail("token") + "   " + mjsonObj.toString());
            mActivityMyAddressesBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                    Constants.BASE_URL + Constants.API_METHODS.SELECT_ADDRESS, mjsonObj,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            System.out.println("Rahul : MyAddresses : requestDeleteAddress : response : " + response);
                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            try {
                                if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {


                                    if (!response.getString("warehouseMatch").equals("n")) {
                                        Intent intent = new Intent();
                                        mSharedPreferenceManager.storeSelectedAddressId(argAddressBookId);
                                       // Constants.VARIABLES.SELECTED_ADDRESS_ID=argAddressBookId;
                                        intent.putExtra("selected_name", argName);
                                        intent.putExtra("selected_mobile", argMobile);
                                        intent.putExtra("selected_address", argAddress);
                                        intent.putExtra("selected_address_book_id", argAddressBookId);
                                        intent.putExtra("latitude", latitude);
                                        intent.putExtra("longitude", lng);
                                        setResult(1, intent);
                                        finish();
                                    } else {
                                        isSelectAddress = false;

                                        new AlertDialog.Builder(MyAddresses.this)
                                                .setTitle(getResources().getString(R.string.select_address))
                                                .setMessage(response.getString("message"))

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

                                    }


                                    if (response.getString("message").equals("No data found.")) {
                                        Toast.makeText(getApplicationContext(), getResources().getString(R.string.please_select_one_address), Toast.LENGTH_LONG).show();
                                    }

                                } else {
                                    isSelectAddress = false;
                                    // mActivityMyAddressesBinding.tvAddressesCount.setVisibility(View.GONE);
                                    Toast.makeText(getApplicationContext(), getResources().getString(R.string.no_address_found), Toast.LENGTH_LONG).show();
                                }

                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                            mActivityMyAddressesBinding.progressSpinKitView.setVisibility(View.GONE);

                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {

                    System.out.println("Rahul : MyAddresses : requestMyAddresses : VolleyError : " + error.toString());

                }
            }) {
                @Override
                public Map<String, String> getHeaders() throws AuthFailureError {
                    HashMap<String, String> headers = new HashMap<String, String>();
                    headers.put("Content-Type", "application/json");
                    headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());
                    headers.put("WID", "1");
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
    public void selectedAddressData(String argName, String argMobile, String argAddress, String argAddressBookId,String lat,String lot) {

        if (getIntent().getExtras() != null) {
            if (getIntent().getStringExtra("from").equals("Delivery_Detail")) {
       /*         Intent intent = new Intent();

                intent.putExtra("selected_name", argName);
                intent.putExtra("selected_mobile", argMobile);
                intent.putExtra("selected_address", argAddress);
                intent.putExtra("selected_address_book_id", argAddressBookId);
                setResult(1, intent);
                finish();*/
                mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
                mSharedPreferenceManager.storeLatitude(lat);
                mSharedPreferenceManager.storeLongitude(lot);
                mSharedPreferenceManager.storeSelectedAddressId(argAddressBookId);
                mSharedPreferenceManager.storeLocationAddress(argAddress);
                mMyAddressesAdapter.notifyDataSetChanged();

                this.argName = argName;
                this.argMobile = argMobile;
                this.argAddress = argAddress;
                this.argAddressBookId = argAddressBookId;
                this.latitude= lat;
                this.lng=lot;
                Constants.log(lat+"--"+lng);
                try {
                    requestSelectAddressNew(argAddressBookId);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                // Constants.VARIABLES.SELECTED_ADDRESS_ID=argAddressBookId;

            }
        }
    }


    @Override
    public void myAddressMenu(String argAction, String argId, int argPosition) {

        switch (argAction) {
            case "edit":
                Intent edt = new Intent(MyAddresses.this, AddNewAddress.class);
                edt.putExtra("edit_address", new Gson().toJson(mAddressesList.get(argPosition)));
                edt.putExtra("from", "");
                edt.putExtra("edit", "edit");
                startActivityForResult(edt, 1);
                break;
            case "delete":
                try {
                    requestDeleteAddress(argId, argPosition);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                break;
        }


    }
}
