package com.gogrocery.view;

import android.app.Activity;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import androidx.databinding.DataBindingUtil;

import com.android.volley.RetryPolicy;
import com.gogrocery.Models.StoreTypeModel.DataItem;
import com.gogrocery.Models.StoreTypeModel.StoreTypeModel;
import com.gogrocery.R;
import com.gogrocery.ViewModel.StoreCategoryModel;
import com.google.android.material.bottomsheet.BottomSheetDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.content.res.Configuration;
import android.content.res.Resources;
import android.location.Address;
import android.location.Geocoder;
import android.os.Build;
import android.os.Bundle;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import androidx.appcompat.widget.SearchView;

import android.os.Handler;
import android.os.Message;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.CompoundButton;
import android.widget.TextView;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.gogrocery.Adapters.CountryListAdapter;
import com.gogrocery.Adapters.StateListAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Interfaces.CountryStateListListner;
import com.gogrocery.Models.CountryListModel.CountryListModel;
import com.gogrocery.Models.CountryListModel.Data;
import com.gogrocery.Models.StateListModel.StateListModel;
import com.gogrocery.databinding.ActivityAddNewAddressBinding;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

public class AddNewAddress extends AppCompatActivity implements CountryStateListListner {

    private ActivityAddNewAddressBinding mActivityAddNewAddressBinding;
    private SharedPreferenceManager mSharedPreferenceManager;


    private Dialog mBottomSheetDialog;
    private List<Data> mCountryListModelList = new ArrayList<>();
    private List<com.gogrocery.Models.StateListModel.Data> mStateListModelList = new ArrayList<>();
    private boolean isCountryLoaded = true;
    private boolean isStateLoaded = false;
    private int countryID = 0, stateID = 0;
    private int isDefault = 0;
    private int customer_address_id = 0;
    private String paramCountryName = "";
    private String StateName = "";
    private String isFromWhere = "";
    private String isEdit = "";
    private String lat = "";
    private String lng = "";
    private List<String> AddressNameList = new ArrayList<>();
    View rootView;
    List<DataItem> storeCategoryList = new ArrayList<>();
    Dialog mSomethingwentworng;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityAddNewAddressBinding = DataBindingUtil.setContentView(this, R.layout.activity_add_new_address);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        setLocale(AddNewAddress.this, "en");
        hideStatusBarColor();
        rootView = this.findViewById(android.R.id.content).getRootView();
        Constants.setupUI(rootView, AddNewAddress.this);
isEdit= getIntent().getStringExtra("edit");
        isFromWhere=getIntent().getStringExtra("from");
        if(!mSharedPreferenceManager.isLoggedIn()){
            Intent i = new Intent(AddNewAddress.this, LoginActivity.class);
            i.putExtra("from_where", "add_address");
            startActivity(i);
        }



        if (mSharedPreferenceManager.getLongitude() != null && !mSharedPreferenceManager.getLongitude().isEmpty() && mSharedPreferenceManager.getLatitude() != null && !mSharedPreferenceManager.getLatitude().isEmpty()) {
            getAddressFromLocation(Double.parseDouble(mSharedPreferenceManager.getLatitude()), Double.parseDouble(mSharedPreferenceManager.getLongitude()));


        }
/*
        try {
            mActivityAddNewAddressBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            if (Constants.isInternetConnected(AddNewAddress.this)) {
                requestStateList();

            } else {
                Constants.setSnackBar(AddNewAddress.this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
            }
            //requestCountryList();

        } catch (JSONException e) {
            e.printStackTrace();
        }
*/

        setClickListners();
        if (isEdit!=null&&!isEdit.isEmpty()) {
            try {
                mActivityAddNewAddressBinding.tvToolbarTitle.setText(getResources().getString(R.string.edit_address));
                mActivityAddNewAddressBinding.btnUpdate.setText(getResources().getString(R.string.change_password_update));
                setEditFields();

            } catch (Exception e) {
                e.printStackTrace();
            }
        } else {

            mActivityAddNewAddressBinding.btnUpdate.setText(getResources().getString(R.string.add));
        }

        mActivityAddNewAddressBinding.ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        mActivityAddNewAddressBinding.edtCarrierNo.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                if (hasFocus) {
                    carrierDialog();
                }

            }
        });
        mActivityAddNewAddressBinding.edtCarrierNo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                carrierDialog();
            }
        });
    }


    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }

    private void setEditFields() throws JSONException {

        com.gogrocery.Models.MyAddressesModel.Data mAData = new Gson().fromJson(getIntent().getExtras().getString("edit_address"), com.gogrocery.Models.MyAddressesModel.Data.class);

        mActivityAddNewAddressBinding.edtFullName.setText(mAData.getDeliveryName());
        mActivityAddNewAddressBinding.edtApartmentNameHNSN.setText(mAData.getDeliveryStreetAddress());
        mActivityAddNewAddressBinding.edtStreetName.setText(mAData.getDeliveryLandmark());


        mActivityAddNewAddressBinding.edtMobileNumber.setText(mAData.getDeliveryPhone());

        String carrier_code = "", mobile_no = "";
        if (mAData.getDeliveryPhone().contains("+971")) {
            carrier_code = mAData.getDeliveryPhone().replace("+971", "").substring(0, 2);
            mobile_no = mAData.getDeliveryPhone().substring(6, mAData.getDeliveryPhone().length());

            mActivityAddNewAddressBinding.edtCarrierNo.setText(carrier_code);
            mActivityAddNewAddressBinding.edtMobileNumber.setText(mobile_no);
        } else {
            mobile_no = mAData.getDeliveryPhone();
            mActivityAddNewAddressBinding.edtMobileNumber.setText(mobile_no);
        }


        mActivityAddNewAddressBinding.edtStates.setText(mAData.getDeliveryStateName());
        mActivityAddNewAddressBinding.edtStates.setHint(mAData.getDeliveryStateName());
        paramCountryName = mAData.getDeliveryCountryName();
        stateID = Integer.parseInt(mAData.getDeliveryState());
        lat=mAData.getLatVal();
        lng=mAData.getLongVal();

        //mActivityAddNewAddressBinding.edtAlternativeMobileNumber.setText(mAData.getDeliveryPhone());

        customer_address_id = mAData.getId();

        if (mAData.getSetPrimary() == 1) {
            mActivityAddNewAddressBinding.cbSetAsDefault.setChecked(true);
        }


    }

    private void carrierDialog() {
        Dialog mCarrierDilog = new Dialog(AddNewAddress.this);
        mCarrierDilog.setContentView(R.layout.carrier_code_dialog);
        TextView tv50, tv52, tv53, tv54, tv55, tv56, tv58;
        tv50 = mCarrierDilog.findViewById(R.id.tv50);
        tv52 = mCarrierDilog.findViewById(R.id.tv52);
        tv53 = mCarrierDilog.findViewById(R.id.tv53);
        tv54 = mCarrierDilog.findViewById(R.id.tv54);
        tv55 = mCarrierDilog.findViewById(R.id.tv55);
        tv56 = mCarrierDilog.findViewById(R.id.tv56);
        tv58 = mCarrierDilog.findViewById(R.id.tv58);
        String selected = "";

        tv50.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                mActivityAddNewAddressBinding.edtCarrierNo.setText(getResources().getString(R.string._50)+"  ");
                mCarrierDilog.dismiss();
            }
        });
        tv52.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityAddNewAddressBinding.edtCarrierNo.setText(getResources().getString(R.string._52)+"  ");
                mCarrierDilog.dismiss();
            }
        });
        tv53.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityAddNewAddressBinding.edtCarrierNo.setText(getResources().getString(R.string._53)+"  ");
                mCarrierDilog.dismiss();
            }
        });
        tv54.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityAddNewAddressBinding.edtCarrierNo.setText(getResources().getString(R.string._54)+"  ");
                mCarrierDilog.dismiss();
            }
        });
        tv55.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityAddNewAddressBinding.edtCarrierNo.setText(getResources().getString(R.string._55)+"  ");
                mCarrierDilog.dismiss();
            }
        });
        tv56.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityAddNewAddressBinding.edtCarrierNo.setText(getResources().getString(R.string._56)+"  ");
                mCarrierDilog.dismiss();
            }
        });
        tv58.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityAddNewAddressBinding.edtCarrierNo.setText(getResources().getString(R.string._58)+"  ");
                mCarrierDilog.dismiss();
            }
        });


        mCarrierDilog.show();
    }

    private void setClickListners() {
       /* mActivityAddNewAddressBinding.edtCountry.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showCountryBottomSheetDialog();
            }
        });

        mActivityAddNewAddressBinding.edtCountry.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                if (hasFocus) {
                    showCountryBottomSheetDialog();
                }
            }
        });*/

        mActivityAddNewAddressBinding.edtStates.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showStateBottomSheetDialog();
            }
        });


        mActivityAddNewAddressBinding.edtStates.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                if (hasFocus) {
                    showStateBottomSheetDialog();
                }
            }
        });

/*        mActivityAddNewAddressBinding.btnCancel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                finish();
            }
        });*/

        mActivityAddNewAddressBinding.cbSetAsDefault.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    isDefault = 1;
                } else {
                    isDefault = 0;
                }

            }
        });

        mActivityAddNewAddressBinding.btnUpdate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

              /*  if (mActivityAddNewAddressBinding.edtFirstName.getText().toString().trim().equals("")) {
                    mActivityAddNewAddressBinding.edtFirstName.setError(getResources().getString(R.string.add_new_address_error_fn));
                } else if (mActivityAddNewAddressBinding.edtLastName.getText().toString().trim().equals("")) {
                    mActivityAddNewAddressBinding.edtLastName.setError(getResources().getString(R.string.add_new_address_error_ln));
                } else if (mActivityAddNewAddressBinding.edtApartmentName.getText().toString().trim().equals("")) {
                    mActivityAddNewAddressBinding.edtApartmentName.setError(getResources().getString(R.string.add_new_address_error_an));
                } else if (mActivityAddNewAddressBinding.edtStreetName.getText().toString().trim().equals("")) {
                    mActivityAddNewAddressBinding.edtStreetName.setError(getResources().getString(R.string.add_new_address_error_sn));
                } else if (mActivityAddNewAddressBinding.edtCountry.getText().toString().trim().equals("")) {
                    mActivityAddNewAddressBinding.edtCountry.setError(getResources().getString(R.string.add_new_address_error_country));
                } else if (mActivityAddNewAddressBinding.edtCity.getText().toString().trim().equals("")) {
                    mActivityAddNewAddressBinding.edtCity.setError(getResources().getString(R.string.add_new_address_error_city));
                } else if (mActivityAddNewAddressBinding.edtMobileNumber.getText().toString().trim().equals("")) {
                    mActivityAddNewAddressBinding.edtMobileNumber.setError(getResources().getString(R.string.add_new_address_error_mobile));
                } else {
                    try {
                        requestAddAddressesUpdate();
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }


*/


                if (mActivityAddNewAddressBinding.edtApartmentNameHNSN.getText().toString().trim().equals("")) {
                    mActivityAddNewAddressBinding.layoutAddress.setError(getResources().getString(R.string.add_new_address_error_field_empty));
                } else if (mActivityAddNewAddressBinding.edtStreetName.getText().toString().trim().equals("")) {
                    mActivityAddNewAddressBinding.layoutStreetName.setError(getResources().getString(R.string.add_new_address_hnosn));
                }
                   else if (mActivityAddNewAddressBinding.edtFullName.getText().toString().trim().equals("")) {
                        mActivityAddNewAddressBinding.layoutFullName.setError(getResources().getString(R.string.add_new_address_error_n));

                }/* else if (mActivityAddNewAddressBinding.edtArea.getText().toString().trim().equals("")) {
                    mActivityAddNewAddressBinding.layoutArea.setError(getResources().getString(R.string.add_new_address_error_field_empty));
                } else if (mActivityAddNewAddressBinding.edtStates.getText().toString().trim().equals("")) {
                    mActivityAddNewAddressBinding.layoutEmirates.setError(getResources().getString(R.string.add_new_address_error_field_empty));
                }*/ else if (mActivityAddNewAddressBinding.edtCarrierNo.getText().toString().isEmpty()) {
                    Constants.showToastInMiddle(getApplicationContext(), getString(R.string.error_msg_enter_carrier_code));
                } else if (mActivityAddNewAddressBinding.edtMobileNumber.getText().toString().length() != 7) {
                    mActivityAddNewAddressBinding.tilmobileno.setError(getString(R.string.error_msg_enter_7_digit_mobile_no));
                } else if (mActivityAddNewAddressBinding.edtMobileNumber.getText().toString().trim().equals("")) {
                    mActivityAddNewAddressBinding.tilmobileno.setError(getResources().getString(R.string.add_new_address_error_field_empty));
                } else {
                    try {
                        if (Constants.isInternetConnected(AddNewAddress.this)) {
                            if (mActivityAddNewAddressBinding.btnUpdate.getText().toString().equalsIgnoreCase(getResources().getString(R.string.add))) {
                                mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
                                lat=mSharedPreferenceManager.getLatitude();
                                lng= mSharedPreferenceManager.getLongitude();
                                if(lat!=null&&!lat.isEmpty()&&lng!=null&&!lng.isEmpty()) {
                                    requestAddAddressesUpdate(lat, lng);
                                }else {
                                    Constants.showToastInMiddle(getApplicationContext(), getString(R.string.error_msg_please_location));
                                }
                            } else if (mActivityAddNewAddressBinding.btnUpdate.getText().toString().equalsIgnoreCase(getResources().getString(R.string.change_password_update))) {

                                if(lat!=null&&!lat.isEmpty()&&lng!=null&&!lng.isEmpty()) {
                                    requestEditAddressesUpdate(lat, lng);
                                }else {
                                    Constants.showToastInMiddle(getApplicationContext(), getString(R.string.error_msg_please_location));
                                }
                            }
                        } else {
                            Constants.setSnackBar(AddNewAddress.this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
                        }
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }

            }
        });
    }

    public void getAddressFromLocation(double latitude, double longitude) {


        StringBuilder result = new StringBuilder();
        try {

            Geocoder geocoder = new Geocoder(AddNewAddress.this, Locale.ENGLISH);
            List<Address> addresses = geocoder.getFromLocation(latitude, longitude, 1);
            if (addresses.size() > 0) {
                Address address = addresses.get(0);
                if (address.getLocality() != null) {
                    result.append(address.getLocality()).append(", ");
                    //  mActivityAddNewAddressBinding.edtStates.setText(address.getLocality());
                }
                if (address.getSubLocality() != null) {
                    result.append(address.getSubLocality()).append(", ");
                }
                if (address.getPostalCode() != null) {
                    result.append(address.getCountryName()).append(", ");
                    result.append(address.getPostalCode()).append(".");
                } else {
                    result.append(address.getCountryName()).append(".");
                }

                //  String city = addresses.get(0).getLocality();
                StateName = result.toString();
                 /*   String locality = addresses.get(0).getAdminArea();
                    String county = addresses.get(0).getCountryName();
                    String postalcode = addresses.get(0).getPremises();
                    String subarea = addresses.get(0).getSubLocality();*
                    Log.e("City:",city);
                  */

                AddressNameList = Arrays.asList(result.toString().split(","));
                Log.e("State:", StateName);
                Log.e("Address:", addresses.toString());


            }

            mActivityAddNewAddressBinding.edtArea.setText(result.toString());
        } catch (IOException e) {
            Log.e("tag", e.getMessage());
        }


    }






    public static void setLocale(Activity activity, String languageCode) {
        Locale locale = new Locale(languageCode);
        Locale.setDefault(locale);
        Resources resources = activity.getResources();
        Configuration config = resources.getConfiguration();
        config.setLocale(locale);
        resources.updateConfiguration(config, resources.getDisplayMetrics());
    }
    public void requestCountryList() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.COUNTRY_LIST, null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        isCountryLoaded = true;
                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        try {
                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                CountryListModel mCountryListModel = mGson.fromJson(mJsonObject.toString(), CountryListModel.class);
                                System.out.println("Rahul : MyAddresses : requestMyAddresses : response : " + response);

                                mCountryListModelList.addAll(mCountryListModel.getData());

                                // mCountryListAdapter.notifyDataSetChanged();


                            } else {
                                Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.no_address_found));

                                //Toast.makeText(getApplicationContext(), "No Address Found!", Toast.LENGTH_LONG).show();
                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                        hideprogressSpinKitView();
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : MyAddresses : requestMyAddresses : VolleyError : " + error.toString());

            }
        })

        {
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
    }

    public void requestAddAddressesUpdate(String lat,String lng) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JSONObject mJSONParam = new JSONObject();
        mJSONParam.put("name", mActivityAddNewAddressBinding.edtFullName.getText().toString());
        mJSONParam.put("address", mActivityAddNewAddressBinding.edtApartmentNameHNSN.getText().toString());
        mJSONParam.put("lat_val",lat );
        mJSONParam.put("long_val", lng);
/*        mJSONParam.put("country", 221);
        mJSONParam.put("state", stateID);*/
        mJSONParam.put("area", mActivityAddNewAddressBinding.edtStreetName.getText().toString());
        mJSONParam.put("mobile_no", "+971" + mActivityAddNewAddressBinding.edtCarrierNo.getText().toString().trim() + mActivityAddNewAddressBinding.edtMobileNumber.getText().toString());
       // mJSONParam.put("mobile_no", "+971" + mActivityAddNewAddressBinding.edtMobileNumber.getText().toString());
        mJSONParam.put("check", isDefault);


      /*
        old param
        mJSONParam.put("first_name", mActivityAddNewAddressBinding.edtFirstName.getText().toString());
        mJSONParam.put("last_name", mActivityAddNewAddressBinding.edtLastName.getText().toString());
        mJSONParam.put("address", mActivityAddNewAddressBinding.edtApartmentName.getText().toString() + ", " + mActivityAddNewAddressBinding.edtStreetName.getText().toString());
        mJSONParam.put("landmark", mActivityAddNewAddressBinding.edtLandmark.getText().toString());
        mJSONParam.put("country", countryID);
        mJSONParam.put("city", mActivityAddNewAddressBinding.edtCity.getText().toString());
        mJSONParam.put("state", 1);
        mJSONParam.put("pincode", 123);
        mJSONParam.put("mobile_no", mActivityAddNewAddressBinding.edtMobileNumber.getText().toString());
        mJSONParam.put("check", isDefault);
        mJSONParam.put("alternative_mobile_no", mActivityAddNewAddressBinding.edtAlternativeMobileNumber.getText().toString());*/


     /*
       new param
       {
            "name": "Rahull",
                "address": "Famousstudio ",
                "country": 221,
                "state": 156,
                "area": "Visa center",
                "mobile_no": "7208568889",
                "check": 0
        }*/

        mActivityAddNewAddressBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        System.out.println("Rahul : AddNewAddress : requestAddAddressesUpdate : mJSONParam : " + mJSONParam.toString());
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.ADDRESSES, mJSONParam,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        isCountryLoaded = true;
                        System.out.println("Rahul : AddNewAddress : requestAddAddressesUpdate : response : " + response);
                        mActivityAddNewAddressBinding.progressSpinKitView.setVisibility(View.GONE);
                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        try {
                            if (mJsonObject.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                //AddNewAddressModel mAddNewAddressModel = mGson.fromJson(mJsonObject.toString(), AddNewAddressModel.class);
                                System.out.println("Rahul : AddNewAddress : requestAddAddressesUpdate : response : " + response);
                                Constants.showToastInMiddle(getApplicationContext(), mJsonObject.getString("message"));
                                requestSelectAddressNew(response.getJSONObject("data").getString("id"));
                                // Toast.makeText(getApplicationContext(), mJsonObject.getString("message"), Toast.LENGTH_LONG).show();

                                //mCountryListModelList.addAll(mCountryListModelList.getData());
                                //showCountryBottomSheetDialog();
                                // mCountryListAdapter.notifyDataSetChanged();
                                if(isFromWhere.equals("add")) {
                                    mSharedPreferenceManager.storeLocationAddress(response.getJSONObject("data").getString("delivery_street_address") + ", " + response.getJSONObject("data").getString("delivery_landmark")
                                            + ", " + response.getJSONObject("data").getString("delivery_state_name") + ", " + response.getJSONObject("data").getString("delivery_country_name"));
                                    try {
                                        requestSelectAddress(Double.parseDouble(response.getJSONObject("data").getString("lat_val")),Double.parseDouble(response.getJSONObject("data").getString("long_val")),response.getJSONObject("data").getString("delivery_street_address") + ", " + response.getJSONObject("data").getString("delivery_landmark")
                                                + ", " + response.getJSONObject("data").getString("delivery_state_name") + ", " + response.getJSONObject("data").getString("delivery_country_name"),response.getJSONObject("data").getString("id"));
                                    } catch (JSONException e) {
                                        e.printStackTrace();
                                    }

                                }else {
                                    Intent intent = new Intent();

                                    intent.putExtra("selected_name", response.getJSONObject("data").getString("delivery_name"));
                                    intent.putExtra("selected_mobile", response.getJSONObject("data").getString("delivery_phone"));
                                    intent.putExtra("selected_address", response.getJSONObject("data").getString("delivery_street_address") + ", " + response.getJSONObject("data").getString("delivery_landmark")
                                            + "\n" + response.getJSONObject("data").getString("delivery_state_name") + ", " + response.getJSONObject("data").getString("delivery_country_name"));
                                    intent.putExtra("selected_address_book_id", response.getJSONObject("data").getString("id"));
                                    setResult(1, intent);
                                    mSharedPreferenceManager.storeSelectedAddressId( response.getJSONObject("data").getString("id"));
                                    mSharedPreferenceManager.storeLatitude( response.getJSONObject("data").getString("lat_val"));
                                    mSharedPreferenceManager.storeLongitude( response.getJSONObject("data").getString("long_val"));
                                   // Constants.VARIABLES.SELECTED_ADDRESS_ID= response.getJSONObject("data").getString("id");
                                    mSharedPreferenceManager.storeLocationAddress(response.getJSONObject("data").getString("delivery_street_address") + ", " + response.getJSONObject("data").getString("delivery_landmark")
                                            + ", " + response.getJSONObject("data").getString("delivery_state_name") + ", " + response.getJSONObject("data").getString("delivery_country_name"));
                                    finish();
                                }
                            } else {
                                Constants.showToastInMiddle(getApplicationContext(), mJsonObject.getString("message"));
                                // Toast.makeText(getApplicationContext(), mJsonObject.getString("message"), Toast.LENGTH_LONG).show();
                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                            System.out.println("Rahul : AddNewAddress : requestAddAddressesUpdate : error : " + e.getMessage());
                        }


                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mActivityAddNewAddressBinding.progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : MyAddresses : requestMyAddresses : VolleyError : " + error.toString());

            }
        })

        {
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
        queue.add(jsonObjReq);
    }




    public void requestEditAddressesUpdate(String lat,String lng) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JSONObject mJSONParam = new JSONObject();

        mJSONParam.put("customers_addressId", customer_address_id);
        mJSONParam.put("name", mActivityAddNewAddressBinding.edtFullName.getText().toString());
        mJSONParam.put("address", mActivityAddNewAddressBinding.edtApartmentNameHNSN.getText().toString());
        mJSONParam.put("lat_val",lat );
        mJSONParam.put("long_val", lng);
       /* mJSONParam.put("country", 221);
        mJSONParam.put("state", stateID);*/
      //  mJSONParam.put("area", mActivityAddNewAddressBinding.edtArea.getText().toString());
        mJSONParam.put("area", mActivityAddNewAddressBinding.edtStreetName.getText().toString());
        mJSONParam.put("mobile_no", "+971" + mActivityAddNewAddressBinding.edtCarrierNo.getText().toString().trim() + mActivityAddNewAddressBinding.edtMobileNumber.getText().toString());
        mJSONParam.put("check", isDefault);


        mActivityAddNewAddressBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        System.out.println("Rahul : AddNewAddress : requestEditAddressesUpdate : mJSONParam : " + mJSONParam.toString());
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.PUT,
                Constants.BASE_URL + Constants.API_METHODS.ADDRESSES, mJSONParam,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {

                        mActivityAddNewAddressBinding.progressSpinKitView.setVisibility(View.GONE);
                        System.out.println("Rahul : AddNewAddress : requestEditAddressesUpdate : response : " + response);

                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        try {
                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                //AddNewAddressModel mAddNewAddressModel = mGson.fromJson(mJsonObject.toString(), AddNewAddressModel.class);
                                System.out.println("Rahul : AddNewAddress : requestEditAddressesUpdate : response : " + response);

                                //mCountryListModelList.addAll(mCountryListModelList.getData());
                                //showCountryBottomSheetDialog();
                                // mCountryListAdapter.notifyDataSetChanged();
                    /*            Intent intent = new Intent();

                                intent.putExtra("selected_name", mActivityAddNewAddressBinding.edtName.getText().toString());
                                intent.putExtra("selected_mobile", mActivityAddNewAddressBinding.edtMobileNumber.getText().toString());
                                intent.putExtra("selected_address", mActivityAddNewAddressBinding.edtApartmentNameHNSN.getText().toString() + "" + mActivityAddNewAddressBinding.edtArea.getText().toString()
                                        + "\n" + mActivityAddNewAddressBinding.edtStates.getText().toString() + " " + paramCountryName);
                                intent.putExtra("selected_address_book_id", customer_address_id);
                                setResult(1, intent);*/
                                finish();

                            } else {
                                Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.no_address_found));
                                // Toast.makeText(getApplicationContext(), "No Address Found!", Toast.LENGTH_LONG).show();
                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                            System.out.println("Rahul : AddNewAddress : requestEditAddressesUpdate : error : " + e.getMessage());
                        }


                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mActivityAddNewAddressBinding.progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : MyAddresses : requestMyAddresses : requestEditAddressesUpdate : VolleyError : " + error.toString());

            }
        })

        {
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
        queue.add(jsonObjReq);
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
    public void requestStateList() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        JSONObject mParam = new JSONObject();
        mParam.put("country_id", 221);
        StringRequest stringRequest = new StringRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.STATE_LIST,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        isStateLoaded = true;
                        Gson mGson = new Gson();

                        try {
                            JSONObject mJsonObject = new JSONObject(response);
                            if (mJsonObject.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                StateListModel mStateListModel = mGson.fromJson(mJsonObject.toString(), StateListModel.class);
                                System.out.println("Rahul : MyAddresses : requestMyAddresses : response : " + response);
                                mStateListModelList.addAll(mStateListModel.getData());

                                for (int i =0; i<mStateListModelList.size();i++){
for (int j =0 ; j<AddressNameList.size();j++){
    if(mStateListModelList.get(i).getStateName().equals(AddressNameList.get(j)))
    {
mActivityAddNewAddressBinding.edtStates.setText(mStateListModelList.get(i).getStateName());
        stateID = mStateListModelList.get(i).getId();
    }
}
                                }
                                //mStateListAdapter.notifyDataSetChanged();

                            } else {
                                Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.no_address_found));

                                //Toast.makeText(getApplicationContext(), "No Address Found!", Toast.LENGTH_LONG).show();
                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                        hideprogressSpinKitView();
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : MyAddresses : requestMyAddresses : VolleyError : " + error.toString());

            }
        }) {

            @Override
            protected Map<String, String> getParams() throws AuthFailureError {
                HashMap<String, String> mHashMap = new HashMap<>();
                mHashMap.put("country_id", "221");
                return mHashMap;
            }


        };


        // Adding request to request queue
        queue.add(stringRequest);
    }

    private void hideprogressSpinKitView() {
        if (isStateLoaded && isCountryLoaded) {
            mActivityAddNewAddressBinding.progressSpinKitView.setVisibility(View.GONE);
        }
    }

    private void showStateBottomSheetDialog() {

        mBottomSheetDialog = new BottomSheetDialog(AddNewAddress.this);
        mBottomSheetDialog.setContentView(R.layout.state_bottom_sheet);
        mBottomSheetDialog.setCancelable(true);

        RecyclerView mRecyclerView = mBottomSheetDialog.findViewById(R.id.rvState);
      /*
        TextView mCloseDialog = mBottomSheetDialog.findViewById(R.id.closeDialog);

        mCloseDialog.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mBottomSheetDialog.dismiss();
            }
        });*/

        StateListAdapter mStateListAdapter = new StateListAdapter(getApplicationContext(), mStateListModelList, this);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.VERTICAL, false);


        // mRecyclerView.addItemDecoration(new ItemDecorationAlbumColumns(10, 100));
        mRecyclerView.setLayoutManager(mLayoutManager);
        mRecyclerView.setItemAnimator(new DefaultItemAnimator());
        mRecyclerView.setAdapter(mStateListAdapter);
        mRecyclerView.setNestedScrollingEnabled(false);


        if (!mBottomSheetDialog.isShowing()) {
            mBottomSheetDialog.show();
        }
    }


    private void showCountryBottomSheetDialog() {

        mBottomSheetDialog = new Dialog(AddNewAddress.this, android.R.style.Theme_Material_Light_NoActionBar);
        mBottomSheetDialog.setContentView(R.layout.country_bottom_sheet);
        mBottomSheetDialog.setCancelable(true);

        RecyclerView mRecyclerView = mBottomSheetDialog.findViewById(R.id.rvCountryList);
        TextView txt1 = mBottomSheetDialog.findViewById(R.id.txt1);

        SearchView searchView = mBottomSheetDialog.findViewById(R.id.searchView);
        searchView.setOnSearchClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View view1) {

                txt1.setVisibility(View.GONE);

            }
        });

        searchView.setOnCloseListener(new SearchView.OnCloseListener() {
            @Override
            public boolean onClose() {

                txt1.setVisibility(View.VISIBLE);

                return false;
            }
        });


        CountryListAdapter mCountryListAdapter = new CountryListAdapter(getApplicationContext(), mCountryListModelList, this);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.VERTICAL, false);
        // mRecyclerView.addItemDecoration(new ItemDecorationAlbumColumns(10, 100));
        mRecyclerView.setLayoutManager(mLayoutManager);
        mRecyclerView.setItemAnimator(new DefaultItemAnimator());
        mRecyclerView.setAdapter(mCountryListAdapter);
        mRecyclerView.setNestedScrollingEnabled(false);


        searchView.setOnQueryTextListener(new SearchView.OnQueryTextListener() {
            @Override
            public boolean onQueryTextSubmit(String query) {
                mCountryListAdapter.getFilter().filter(query);
                System.out.println("Rahul : setOnQueryTextListener : onQueryTextSubmit : " + query);
                return false;
            }

            @Override
            public boolean onQueryTextChange(String newText) {

                //System.out.println("Rahul : setOnQueryTextListener : onQueryTextChange : " + newText);
                mCountryListAdapter.getFilter().filter(newText);
                System.out.println("Rahul : setOnQueryTextListener : onQueryTextChange : " + newText);


                return false;
            }
        });
        mBottomSheetDialog.setOnDismissListener(new DialogInterface.OnDismissListener() {
            @Override
            public void onDismiss(DialogInterface dialogInterface) {
                Constants.hideSoftKeyboard(AddNewAddress.this);
            }
        });

        if (!mBottomSheetDialog.isShowing()) {
            mBottomSheetDialog.show();
        }
    }

    @Override
    public void passID(String argWhich, int argId, String argTitle) {
        switch (argWhich) {
            case "state":
                stateID = argId;
                mActivityAddNewAddressBinding.edtStates.setText(argTitle);
                mBottomSheetDialog.dismiss();
                break;
            case "country":
                countryID = argId;
                mActivityAddNewAddressBinding.edtStates.setText(argTitle);
                mBottomSheetDialog.dismiss();
                break;
        }

    }

    public void requestStoreTypeList(double latitude, double longitude ,String argAddress, String argAddressBookId) throws JSONException {

        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("latitude", latitude);
        mJsonObject.put("longitude", longitude);
        mJsonObject.put("website_id", 1);
        mActivityAddNewAddressBinding.progressSpinKitView.setVisibility(View.GONE);
        System.out.println("Rahul : MapLocationSelectionUpdate : requestStoreTypeList : mJsonObject : " + mJsonObject);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.STORE_TYPE, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : MapLocationSelectionUpdate : requestStoreTypeList : response : " + response);
                        Gson mGson = new Gson();
                        mActivityAddNewAddressBinding.progressSpinKitView.setVisibility(View.GONE);
                        JSONObject mJsonObject = response;
                        StoreTypeModel storeTypeModel = mGson.fromJson(response.toString(), StoreTypeModel.class);
                        if (storeTypeModel.getStatus() == 1) {
                            // isClickable=false;

                            mSharedPreferenceManager.storeSelectedAddressId(argAddressBookId);
                            mSharedPreferenceManager.storeLocationAddress(argAddress);

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
                                try {
                                    //requestSelectAddress(argAddressBookId);
                                } catch (Exception e) {
                                    e.printStackTrace();
                                }
                                if (isSelectedCategory) {
                                    Intent i = new Intent(AddNewAddress.this, SelectCategory.class);
                                    i.putExtra("latitude", latitude + "");
                                    i.putExtra("longitude", longitude + "");
                                    i.putExtra("from_where", "store");
                                    i.putExtra("selected_address_id",true);
                                    startActivity(i);
                                    finish();
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
                mActivityAddNewAddressBinding.progressSpinKitView.setVisibility(View.GONE);
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



    public void requestSelectAddress(double latitude, double longitude ,String argAddress, String argAddressBookId) throws JSONException {

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
                        mSharedPreferenceManager.storeLocationAddress(argAddress);
                        Intent i = new Intent(AddNewAddress.this, SelectCategory.class);
                        i.putExtra("latitude", latitude + "");
                        i.putExtra("longitude", longitude + "");
                        i.putExtra("from_where", "store");
                        i.putExtra("selected_address_id",true);
                        startActivity(i);
                        finish();

                    }

                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                showNoDeliveryDialog();
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
    public void showNoDeliveryDialog() {
        mSomethingwentworng = new Dialog(AddNewAddress.this);
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

    @Override
    public void onBackPressed() {
        super.onBackPressed();
    }

    private void textCheckListener() {


        mActivityAddNewAddressBinding.edtApartmentNameHNSN.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
          /*      String result = s.toString().replaceAll(" ", "");
                if (!s.toString().equals(result)) {
                    mActivityAddNewAddressBinding.edtApartmentNameHNSN.setText(result);
                    mActivityAddNewAddressBinding.edtApartmentNameHNSN.setSelection(result.length());
                    // alert the user
                }
*/

                mActivityAddNewAddressBinding.layoutAddress.setError(null);


            }
        });
        mActivityAddNewAddressBinding.edtStreetName.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                String result = s.toString().replaceAll(" ", "");
                if (!s.toString().equals(result)) {
                    mActivityAddNewAddressBinding.edtStreetName.setText(result);
                    mActivityAddNewAddressBinding.edtStreetName.setSelection(result.length());
                    // alert the user
                }

                mActivityAddNewAddressBinding.layoutStreetName.setError(null);


            }
        });
        mActivityAddNewAddressBinding.edtFullName.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
           /*     String result = s.toString().replaceAll(" ", "");
                if (!s.toString().equals(result)) {
                    et_input_houseName.setText(result);
                    et_input_houseName.setSelection(result.length());
                    // alert the user
                }
*/
                mActivityAddNewAddressBinding.layoutFullName.setError(null);


            }
        });
        mActivityAddNewAddressBinding.edtCarrierNo.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                String result = s.toString().replaceAll(" ", "");
                if (!s.toString().equals(result)) {
                    mActivityAddNewAddressBinding.edtCarrierNo.setText(result);
                    mActivityAddNewAddressBinding.edtCarrierNo.setSelection(result.length());
                    // alert the user
                }
                mActivityAddNewAddressBinding.tilCarrierNo.setError(null);


            }
        });
        mActivityAddNewAddressBinding.edtMobileNumber.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                mActivityAddNewAddressBinding.tilmobileno.setError(null);


            }
        });



    }
}
