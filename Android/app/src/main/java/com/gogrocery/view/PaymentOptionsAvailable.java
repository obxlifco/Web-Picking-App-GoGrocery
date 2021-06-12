package com.gogrocery.view;

import android.content.Intent;
import androidx.databinding.DataBindingUtil;
import android.net.Uri;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;

import android.view.View;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.facebook.appevents.AppEventsConstants;
import com.facebook.appevents.AppEventsLogger;
import com.gogrocery.Adapters.PaymentMethodTypesAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Interfaces.PaymentMethodTypesInterface;
import com.gogrocery.Models.MyOrdersFromMailModel.MyOrdersFromMailData;
import com.gogrocery.Models.MyOrdersFromMailModel.MyOrdersFromMailModel;
import com.gogrocery.Models.MyOrdersHistoryModel.Data;

import com.gogrocery.Models.PaymentTransaction.PaymentTransactionModel;
import com.gogrocery.Models.PaymentTypesModel.ApiStatus;
import com.gogrocery.Models.PaymentTypesModel.PaymentMethodModel;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityPaymentOptionsGogroceryBinding;
import com.google.firebase.analytics.FirebaseAnalytics;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import mumbai.dev.sdkdubai.BillingAddress;
import mumbai.dev.sdkdubai.CustomModel;
import mumbai.dev.sdkdubai.MerchantDetails;
import mumbai.dev.sdkdubai.PaymentOptions;
import mumbai.dev.sdkdubai.ShippingAddress;
import mumbai.dev.sdkdubai.StandardInstructions;

public class PaymentOptionsAvailable extends AppCompatActivity implements CustomModel.OnCustomStateListener, PaymentMethodTypesInterface {

    private ActivityPaymentOptionsGogroceryBinding mActivityPaymentOptionsBinding;
    private SharedPreferenceManager mSharedPreferenceManager;
    private String OrderDetail = "", OrderId = "", cust_orders_id = "", mTotalAmount = "", mWarehouseId = "";
    private String mTransactionId = "";
    private Data mData;
    private FirebaseAnalytics mFirebaseAnalytics;
    AppEventsLogger logger;
    private MyOrdersFromMailData myOrdersFromMailData;
    private JSONObject order_summary;
    private JSONObject delivery_address;
    private String billing_name = "", billing_street_address = "", billing_country_name = "", billing_state_name = "", billing_email = "", billing_phone = "", billing_city = "";
    private String delivery_name = "", delivery_street_address = "", delivery_country_name = "", delivery_state_name = "", delivery_email = "", delivery_phone = "", delivery_city = "";

    private List<ApiStatus> mApiStatusList = new ArrayList<>();
    private PaymentMethodTypesAdapter mPaymentMethodTypesAdapter;
    private String isWhichPaymentType = "";
    private String paymentgateway_type_id = "", type_id = "", type_name = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityPaymentOptionsBinding = DataBindingUtil.setContentView(this, R.layout.activity_payment_options_gogrocery);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        mFirebaseAnalytics = FirebaseAnalytics.getInstance(this);
        logger = AppEventsLogger.newLogger(this);
        CustomModel.getInstance().setListener(this);


        try {
            requestPaymentMethods();
        } catch (JSONException e) {
            e.printStackTrace();
        }
        setPaymentMethodRecyclerView();
        mActivityPaymentOptionsBinding.ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        getOrderIdBundel();

        mActivityPaymentOptionsBinding.btnPlaceOrder.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                setPassingParam();
                if (isWhichPaymentType.equals("cash")) {
                    try {
                      requestPayment(OrderId);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                } else if (isWhichPaymentType.equals("card")) {

                    try {
                        requestPaymentTransaction();
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                } else if (isWhichPaymentType.equals("card_on_delivery")) {
                    try {
                        requestPayment(OrderId);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                } else {
                    Constants.showToastInMiddle(getApplicationContext(), "Please select any one Payment Option");
                    //  Toast.makeText(getApplicationContext(), "Please select any one Payment Option", Toast.LENGTH_LONG).show();
                }
            }
        });

        mActivityPaymentOptionsBinding.tvChangeAddress.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent btnChangeAddAddresses = new Intent(PaymentOptionsAvailable.this, MyAddresses.class);
                btnChangeAddAddresses.putExtra("from", "Delivery_Detail");
                startActivityForResult(btnChangeAddAddresses, 1);
            }
        });

        mActivityPaymentOptionsBinding.rlCreditDebitCard.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityPaymentOptionsBinding.rbCreditCard.setChecked(true);
                mActivityPaymentOptionsBinding.rbCOD.setChecked(false);


                if (mData != null) {


                    //requestPaymentTransaction();
                }
                /*Intent rlCreditDebitCard = new Intent(PaymentOptionsAvailable.this, CreditCardActivity.class);
                rlCreditDebitCard.putExtra("orders_id", OrderId);
                rlCreditDebitCard.putExtra("order_detail", OrderDetail);
                startActivity(rlCreditDebitCard);*/
            }
        });

        mActivityPaymentOptionsBinding.rbCOD.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityPaymentOptionsBinding.rbCreditCard.setChecked(false);
                /*if (mData != null) {
                    setCCAvenueInitialDetails();
                }*/
            }
        });
        mActivityPaymentOptionsBinding.rbCreditCard.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
               /* Intent rlCreditDebitCard = new Intent(PaymentOptionsAvailable.this, CreditCardActivity.class);
                rlCreditDebitCard.putExtra("orders_id", OrderId);
                rlCreditDebitCard.putExtra("order_detail", OrderDetail);
                startActivity(rlCreditDebitCard);*/
                if (mData != null) {
                    //  setCCAvenueInitialDetails();
                    //requestPaymentTransaction();
                }
                mActivityPaymentOptionsBinding.rbCOD.setChecked(false);
            }
        });
    }

    private void setPaymentMethodRecyclerView() {
        mPaymentMethodTypesAdapter = new PaymentMethodTypesAdapter(getApplicationContext(), mApiStatusList, this);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.VERTICAL, false);
        mActivityPaymentOptionsBinding.rvPaymentTypes.setLayoutManager(mLayoutManager);
        mActivityPaymentOptionsBinding.rvPaymentTypes.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        mActivityPaymentOptionsBinding.rvPaymentTypes.setItemAnimator(new DefaultItemAnimator());
        mActivityPaymentOptionsBinding.rvPaymentTypes.setAdapter(mPaymentMethodTypesAdapter);
        mActivityPaymentOptionsBinding.rvPaymentTypes.setNestedScrollingEnabled(false);
    }

    private void setPassingParam() {
        try {
            order_summary = new JSONObject();
            delivery_address = new JSONObject();

            order_summary.put("subtotal", mActivityPaymentOptionsBinding.tvSubtotal.getText().toString());
            order_summary.put("discount", mActivityPaymentOptionsBinding.tvDiscount.getText().toString());
            //  order_summary.put("loyalty_amount", mActivityDeliveryDetailBinding.tvAppliedLoyaltyAmount.getText().toString());
            order_summary.put("delivery", mActivityPaymentOptionsBinding.tvDeliveryCharges.getText().toString());
            order_summary.put("tax", mActivityPaymentOptionsBinding.tvEstimatedTax.getText().toString());
            order_summary.put("final_total", mActivityPaymentOptionsBinding.tvTotalSumPrice.getText().toString());
            if (mActivityPaymentOptionsBinding.tvAppliedLoyaltyAmount.getText().toString().contains("0.00")) {
                order_summary.put("loyalty_amount", "0.00");
            } else {
                order_summary.put("loyalty_amount", mActivityPaymentOptionsBinding.tvAppliedLoyaltyAmount.getText().toString());
            }

            if (mActivityPaymentOptionsBinding.tvDiscount.getText().toString().equals("AED 0.00")) {
                order_summary.put("coupon_discount", "0.00");
            } else if (mActivityPaymentOptionsBinding.tvDiscount.getText().toString().equals("AED 0.0")) {
                order_summary.put("coupon_discount", "0.00");
            } else if (mActivityPaymentOptionsBinding.tvDiscount.getText().toString().equals("AED 0")) {
                order_summary.put("coupon_discount", "0.00");
            } else {
                order_summary.put("coupon_discount", mActivityPaymentOptionsBinding.tvDiscount.getText().toString());
            }

            delivery_address.put("name", mActivityPaymentOptionsBinding.tvName.getText().toString());
            delivery_address.put("address", mActivityPaymentOptionsBinding.tvAddress.getText().toString());
            delivery_address.put("number", mActivityPaymentOptionsBinding.tvMobileNumber.getText().toString());
        } catch (JSONException e) {

        }
    }
   /* http://15.185.126.44:8062/api/front/v1/get-rsa-demo/?order_id=50002234
    http://15.185.126.44:8062/api/front/v1/payment-res-demo/
    http://15.185.126.44:8062/api/front/v1/payment-res-demo/*/

    private void setCCAvenueInitialDetails() {

        String access_code = "AVZO03HA32BC46OZCB";//live
        String merchant_id = "46319";//live
        MerchantDetails m = new MerchantDetails();
    //   m.setAccess_code("AVUP03GL28CI81PUIC");//old
       //m.setAccess_code("AVCG03HF47CJ43GCJC");
       m.setAccess_code(access_code);
       // m.setMerchant_id("45990");//Old
       // m.setMerchant_id("43366");
        m.setMerchant_id(merchant_id);
        m.setCurrency(Constants.VARIABLES.CURRENT_CURRENCY);
      //  m.setAmount(mTotalAmount);
        m.setAmount("1.00");
        m.setRedirect_url("https://www.gogrocery.ae/api/front/v1/payment-res/");
        m.setCancel_url("https://www.gogrocery.ae/api/front/v1/payment-res/");
        m.setRsa_url("https://www.gogrocery.ae/api/front/v1/get-rsa/");
//        http://15.185.126.44:8062/api/front/v1/
      //  m.setRedirect_url("http://15.185.126.44:8062/api/front/v1/payment-res/");
/*        m.setRedirect_url("http://15.185.126.44:8062/api/front/v1/payment-res-demo/");
        m.setCancel_url("http://15.185.126.44:8062/api/front/v1/payment-res-demo/");
        m.setRsa_url("http://15.185.126.44:8062/api/front/v1/get-rsa-demo/?order_id="+cust_orders_id);*/
        //m.setOrder_id(OrderId);
        m.setOrder_id(cust_orders_id);
        //m.setCustomer_id(cust_orders_id);
        m.setCustomer_id(OrderId);
        m.setShow_addr(false);
        m.setCCAvenue_promo(false);
        m.setPromo_code("");
        m.setAdd1(mTransactionId);
        m.setAdd2("");
        m.setAdd3("");
        m.setAdd4("");
        m.setAdd5("");


        BillingAddress b = new BillingAddress();
        b.setName(billing_name);
        b.setAddress(billing_street_address);
        b.setCountry(billing_country_name);
        b.setState(billing_state_name);
        b.setCity(billing_city);
        b.setTelephone(billing_phone);
        b.setEmail(billing_email);

        ShippingAddress s = new ShippingAddress();
        s.setName(delivery_name);
        s.setAddress(delivery_street_address);
        s.setCountry(delivery_country_name);
        s.setState(delivery_state_name);
        s.setCity(delivery_city);
        s.setTelephone(delivery_phone);

        Gson mGson = new Gson();

        System.out.println("Rahul : PaymentOptionsAvailable : setCCAvenueInitialDetails : MerchantDetails : " + mGson.toJson(m));
        System.out.println("Rahul : PaymentOptionsAvailable : setCCAvenueInitialDetails : BillingAddress : " + mGson.toJson(b));
        System.out.println("Rahul : PaymentOptionsAvailable : setCCAvenueInitialDetails : ShippingAddress : " + mGson.toJson(s));
        // SI data //
        StandardInstructions si = new StandardInstructions();
        String si_type = "ONDEMAND";


            si.setSi_type(si_type);
         //   si.setSi_mer_ref_no("1234");
            si.setSi_is_setup_amt("N");
            si.setSi_start_date(Constants.getCurrentDate());
        System.out.println("Rahul : PaymentOptionsAvailable : setCCAvenueInitialDetails : SI Info : " + mGson.toJson(si));
            Intent i =new Intent(PaymentOptionsAvailable.this,PaymentOptions.class);
            //Intent i =new Intent(MainActivity.this,PaymentOptions.class);
            // Intent i =new Intent(MainActivity.this,PaymentDetails.class);
            i.putExtra("merchant",m);
            i.putExtra("billing",b);
            i.putExtra("shipping",s);
            i.putExtra("standard instructions", si);
            startActivity(i);







/*
        si.setSi_type("");
        Intent i = new Intent(PaymentOptionsAvailable.this, PaymentOptions.class);
        i.putExtra("merchant", m);
        i.putExtra("billing", b);
        i.putExtra("shipping", s);
        i.putExtra("standard instructions", si);
        startActivity(i);
*/


    }

    private void getOrderIdBundel() {

        Intent intent = getIntent();
        String action = intent.getAction();
        if (getIntent().getExtras().getString("is_deep_linking")!=null) {
            Uri data = intent.getData();
            System.out.println("Rahul : PaymentOptionsAvailable : getOrderIdBundel : data : " + data);
            try {

                requestOrderDetails(getIntent().getExtras().getString("is_deep_linking"));

            } catch (JSONException e) {
                e.printStackTrace();
            }
        } else {
            System.out.println("Rahul : PaymentOptionsAvailable : getOrderIdBundel : data : else : ");

            OrderId = getIntent().getExtras().getString("cust_orders_id");
            cust_orders_id = getIntent().getExtras().getString("cust_orders_id");

            OrderDetail = getIntent().getExtras().getString("order_detail");

            setPageUI(OrderDetail);
        }
    }

    private void setPageUI(String argOrderDetail) {
        mData = new Gson().fromJson(argOrderDetail, Data.class);

        mActivityPaymentOptionsBinding.tvSubtotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mData.getNetAmount())));
        mActivityPaymentOptionsBinding.tvDiscount.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mData.getCartDiscount())));
        mActivityPaymentOptionsBinding.tvDeliveryCharges.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mData.getShippingCost())));
        mActivityPaymentOptionsBinding.tvTotalSumPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mData.getGrossAmount())));
        mActivityPaymentOptionsBinding.tvPlaceOrderPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mData.getGrossAmount())));


     //   mTotalAmount = Constants.twoDecimalRoundOff(Double.parseDouble(mData.getGrossAmount()));//Live

Double totalPrice = Double.parseDouble(mData.getGrossAmount());
       mTotalAmount = String.valueOf(totalPrice.intValue());
     //  mTotalAmount = "37";
        if (mData.getLoyalty_amount().equals("0.00")) {

        } else {
            mActivityPaymentOptionsBinding.llLoyaltyPoints.setVisibility(View.VISIBLE);
            mActivityPaymentOptionsBinding.tvAppliedLoyaltyAmount.setText(mData.getLoyalty_amount());
        }

        if (mData.getCoupon_discount().equals("0.00")) {
            mActivityPaymentOptionsBinding.tvDiscount.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " 0.00");
        } else {
            mActivityPaymentOptionsBinding.tvDiscount.setText(mData.getCoupon_discount());
        }


        mActivityPaymentOptionsBinding.tvName.setText(mData.getDeliveryName());
        mActivityPaymentOptionsBinding.tvAddress.setText(mData.getDisplay_address());
        mActivityPaymentOptionsBinding.tvMobileNumber.setText(mData.getDeliveryPhone());

        billing_name = mData.getBillingName();
        billing_street_address = mData.getBillingStreetAddress();
        billing_country_name = mData.getBillingCountryName();
        billing_state_name = mData.getBillingStateName();
        billing_email = mData.getBillingEmailAddress();
        billing_phone = mData.getBillingPhone();
        billing_city = "Basara";

        delivery_name = mData.getDeliveryName();
        delivery_street_address = mData.getDeliveryStreetAddress();
        delivery_country_name = mData.getDeliveryCountryName();
        delivery_state_name = mData.getDeliveryStateName();
        delivery_email = mData.getDeliveryEmailAddress();
        delivery_phone = mData.getDeliveryPhone();
        delivery_city = "Basara";

        mActivityPaymentOptionsBinding.nsv.setVisibility(View.VISIBLE);

    }


    private void setPageUI2(String argOrderDetail) {
        myOrdersFromMailData = new Gson().fromJson(argOrderDetail, MyOrdersFromMailData.class);
        Constants.VARIABLES.CURRENT_CURRENCY = myOrdersFromMailData.getCurrencyCode();
        mActivityPaymentOptionsBinding.tvSubtotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(myOrdersFromMailData.getNetAmount().toString())));
        mActivityPaymentOptionsBinding.tvDiscount.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(myOrdersFromMailData.getCartDiscount().toString())));
        mActivityPaymentOptionsBinding.tvDeliveryCharges.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(myOrdersFromMailData.getShippingCost().toString())));
        mActivityPaymentOptionsBinding.tvTotalSumPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(myOrdersFromMailData.getGrossAmount().toString())));
        mActivityPaymentOptionsBinding.tvPlaceOrderPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(myOrdersFromMailData.getGrossAmount().toString())));


        OrderId = myOrdersFromMailData.getCustomOrderId();
        cust_orders_id = myOrdersFromMailData.getCustomer().getId().toString();
        mTotalAmount = Constants.twoDecimalRoundOff(Double.parseDouble(myOrdersFromMailData.getGrossAmount().toString()));
        /*if (myOrdersFromMailData.getOrderProducts().getLoyalty_amount().equals("0.00")) {

        } else {
            mActivityPaymentOptionsBinding.llLoyaltyPoints.setVisibility(View.VISIBLE);
            mActivityPaymentOptionsBinding.tvAppliedLoyaltyAmount.setText(myOrdersFromMailData.getLoyalty_amount());
        }

        if (myOrdersFromMailData.getCoupon_discount().equals("0.00")) {
            mActivityPaymentOptionsBinding.tvDiscount.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " 0.00");
        } else {
            mActivityPaymentOptionsBinding.tvDiscount.setText(myOrdersFromMailData.getCoupon_discount());
        }*/


        mActivityPaymentOptionsBinding.tvName.setText(myOrdersFromMailData.getDeliveryName());
        mActivityPaymentOptionsBinding.tvAddress.setText(myOrdersFromMailData.getBillingStreetAddress() + "\n" + myOrdersFromMailData.getBillingStateName() + " " + myOrdersFromMailData.getBillingCountryName());
        mActivityPaymentOptionsBinding.tvMobileNumber.setText(myOrdersFromMailData.getDeliveryPhone());

        billing_name = myOrdersFromMailData.getBillingName();
        billing_street_address = myOrdersFromMailData.getBillingStreetAddress();
        billing_country_name = myOrdersFromMailData.getBillingCountryName();
        billing_state_name = myOrdersFromMailData.getBillingStateName();
        billing_email = myOrdersFromMailData.getBillingEmailAddress();
        billing_phone = myOrdersFromMailData.getBillingPhone();
        billing_city = "Basara";

        delivery_name = myOrdersFromMailData.getDeliveryName();
        delivery_street_address = myOrdersFromMailData.getDeliveryStreetAddress();
        delivery_country_name = myOrdersFromMailData.getDeliveryCountryName();
        delivery_state_name = myOrdersFromMailData.getDeliveryStateName();
        delivery_email = myOrdersFromMailData.getDeliveryEmailAddress();
        delivery_phone = myOrdersFromMailData.getDeliveryPhone();
        delivery_city = "Basara";
        mActivityPaymentOptionsBinding.nsv.setVisibility(View.VISIBLE);
    }


    public void requestPaymentMethods() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        mActivityPaymentOptionsBinding.progressSpinKitView.setVisibility(View.VISIBLE);

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.PAYMENT_METHODS, null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Gson mGson = new Gson();
                        mActivityPaymentOptionsBinding.progressSpinKitView.setVisibility(View.GONE);
                        PaymentMethodModel mPaymentMethodModel = mGson.fromJson(response.toString(), PaymentMethodModel.class);

                        mApiStatusList.clear();
                        mApiStatusList.addAll(mPaymentMethodModel.getApiStatus());
                        mPaymentMethodTypesAdapter.notifyDataSetChanged();

                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                System.out.println("Rahul : PaymentOptionsAvailable : onErrorResponse : error : " + error);
                mActivityPaymentOptionsBinding.progressSpinKitView.setVisibility(View.GONE);


            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());
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

    public void requestOrderDetails(String argEncryptedData) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        mActivityPaymentOptionsBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        System.out.println("Rahul : MyOrdersDetailPage : requestOrderDetails : mJsonObject : url : " + argEncryptedData);

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                argEncryptedData, null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Gson mGson = new Gson();
                        mActivityPaymentOptionsBinding.progressSpinKitView.setVisibility(View.GONE);
                        // mActivityPaymentOptionsBinding.nsvMyOrdersDetail.setVisibility(View.VISIBLE);
                        System.out.println("cc : " + response);
                        //  MyOrdersHistoryModel mMyOrdersHistoryModel = mGson.fromJson(mJsonObject.toString(), MyOrdersHistoryModel.class);
                        MyOrdersFromMailModel mMyOrdersFromMailModel = mGson.fromJson(response.toString(), MyOrdersFromMailModel.class);

                        OrderId = mMyOrdersFromMailModel.getData().getCustomOrderId();
                        cust_orders_id = mMyOrdersFromMailModel.getData().getCustomer().getId().toString();
                        mWarehouseId = mMyOrdersFromMailModel.getData().getOrderProducts().get(0).getWarehouseId();
                        System.out.println("Rahul : MyOrdersDetailPage : requestOrderDetails : mWarehouseId : " + mWarehouseId);

                        setPageUI2(mGson.toJson(mMyOrdersFromMailModel.getData()));

                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                System.out.println("Rahul : PaymentOptionsAvailable : onErrorResponse : error : " + error);
                mActivityPaymentOptionsBinding.progressSpinKitView.setVisibility(View.GONE);


            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                //headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_token));
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

    public void requestPayment(String argOrderId) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        System.out.println("Rahul : PaymentOptionsAvailable : requestPayment : order_id : " + argOrderId);
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("order_id", argOrderId);
        mJsonObject.put("payment_method_id", Integer.parseInt(paymentgateway_type_id));
        mJsonObject.put("payment_type_id", Integer.parseInt(type_id));
        mJsonObject.put("payment_method_name", type_name);


        System.out.println("Rahul : PaymentOptionsAvailable : requestPayment : param : " + mJsonObject);
        mActivityPaymentOptionsBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.PUT,
                Constants.BASE_URL + Constants.API_METHODS.CHECKOUT, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        mActivityPaymentOptionsBinding.progressSpinKitView.setVisibility(View.GONE);
                        System.out.println("Rahul : PaymentOptionsAvailable : requestPayment : mJsonObject : " + mJsonObject);
                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        System.out.println("Rahul : PaymentOptionsAvailable : requestPayment : mJsonObject : " + mJsonObject);
                        try {

                            Intent orderSuccess = new Intent(PaymentOptionsAvailable.this, OrderSuccess.class);
                            orderSuccess.putExtra("status", "Success");
                            orderSuccess.putExtra("order_id", response.getString("order_id"));
                            orderSuccess.putExtra("order_summary", order_summary.toString());
                            orderSuccess.putExtra("delivery_address", delivery_address.toString());
                            startActivity(orderSuccess);
                            Bundle params = new Bundle();
                            params.putString("payment_method_name",type_name);
                            params.putString("delivery_address",delivery_address.toString());
                            params.putString("OrderFrom","Android");
                            params.putString("order_id",response.getString("order_id"));
                            params.putString("order_summary",order_summary.toString());
                            logger.logEvent("AddPaymentInfo", params);
                            mFirebaseAnalytics.logEvent("AddPaymentInfo", params);


                       /* Intent orderSuccess = new Intent(PaymentOptionsAvailable.this, OrderSuccess.class);
                            orderSuccess.putExtra("order_id", response.getString("order_id"));
                            startActivity(orderSuccess);*/

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mActivityPaymentOptionsBinding.progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : PaymentOptionsAvailable : requestPayment : VolleyError : " + error.toString());

            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                if (mSharedPreferenceManager.getWarehouseId().isEmpty()) {
                    System.out.println("Rahul : mWarehouseId : " + mWarehouseId);
                    headers.put(Constants.VARIABLES.WAREHOUSE_KEY, mWarehouseId);
                } else {
                    headers.put(Constants.VARIABLES.WAREHOUSE_KEY, mSharedPreferenceManager.getWarehouseId());

                }
                //headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_token));
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
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        System.out.println("Rahul : DeliveryDetail : onActivityResult : 1 : ");
        if (requestCode == 1) {
            System.out.println("Rahul : DeliveryDetail : onActivityResult : 2 : ");
            if (data != null) {

                System.out.println("Rahul : DeliveryDetail : onActivityResult : selected_name : " + data.getStringExtra("selected_name"));
                String name = data.getStringExtra("selected_name");
                String mobile = data.getStringExtra("selected_mobile");
                String address = data.getStringExtra("selected_address");
                String address_book_id = data.getStringExtra("selected_address_book_id");


                mActivityPaymentOptionsBinding.tvName.setText(name);
                mActivityPaymentOptionsBinding.tvMobileNumber.setText(mobile);
                mActivityPaymentOptionsBinding.tvAddress.setText(address);
            }
        }
    }

    public void requestPaymentTransaction() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        mActivityPaymentOptionsBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("order_id", OrderId);

        System.out.println("Rahul : PaymentOptionsAvailable : requestPaymentTransaction : mJsonObject : " + mJsonObject.toString());

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.PAYMENT_TRANSACTION, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        mActivityPaymentOptionsBinding.progressSpinKitView.setVisibility(View.GONE);
                        System.out.println("Rahul : PaymentOptionsAvailable : requestPaymentTransaction : response : " + response.toString());
                        try {
                            Gson mGson = new Gson();
                            PaymentTransactionModel mPaymentTransactionModel = mGson.fromJson(response.toString(), PaymentTransactionModel.class);

                            mTransactionId = mPaymentTransactionModel.getTransactionData().getTransactionId();

                            setCCAvenueInitialDetails();

                            Bundle params = new Bundle();
                            params.putString("payment_method_name",type_name);
                            params.putString("delivery_address",delivery_address.toString());
                            params.putString("OrderFrom","Android");
                            params.putString("order_id",response.getString("order_id"));
                            params.putString("order_summary",order_summary.toString());
                            params.putString("total_amount_purchased","" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(myOrdersFromMailData.getGrossAmount().toString())));
                            params.putString("content_type","product_group");
                            params.putString("total_item_count",Constants.VARIABLES.CART_COUNT+"");
                            params.putString("currency",Constants.VARIABLES.CURRENT_CURRENCY);
                            params.putString("customer",mActivityPaymentOptionsBinding.tvName.getText().toString()+","+mActivityPaymentOptionsBinding.tvAddress.getText().toString()+","+mActivityPaymentOptionsBinding.tvMobileNumber.getText().toString()+","+mSharedPreferenceManager.key_email);
                            logger.logEvent("AddPaymentInfo", params);
                            mFirebaseAnalytics.logEvent("AddPaymentInfo", params);

                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mActivityPaymentOptionsBinding.progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : PaymentOptionsAvailable : requestPaymentTransaction : VolleyError : " + error.toString());
            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                // headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_token));

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
    public void stateChanged() {
        String modelState = CustomModel.getInstance().getState();
        System.out.println("Rahul : PaymentOptionsAvailable : stateChanged : modelState : " + modelState);
        try {
            JSONObject mJsonObject = new JSONObject(modelState);

            if (mJsonObject.getString("status_message").equalsIgnoreCase("Approved")) {

                Intent orderSuccess = new Intent(PaymentOptionsAvailable.this, OrderSuccess.class);
                orderSuccess.putExtra("status", "Success");
                orderSuccess.putExtra("order_id", OrderId);
                orderSuccess.putExtra("order_summary", order_summary.toString());
                orderSuccess.putExtra("delivery_address", delivery_address.toString());
                startActivity(orderSuccess);

                Bundle params = new Bundle();
                params.putString("payment_method_name",type_name);
                params.putString("delivery_address",delivery_address.toString());
                params.putString("order_id",OrderId);
                params.putString("OrderFrom","Android");
                params.putString("order_summary",order_summary.toString());
                mFirebaseAnalytics.logEvent(FirebaseAnalytics.Event.PURCHASE, params);
                logger.logEvent("purchase", params);
                finish();
            } else {
                Intent orderSuccess = new Intent(PaymentOptionsAvailable.this, OrderSuccess.class);
                orderSuccess.putExtra("status", "Failure");
                orderSuccess.putExtra("order_id", OrderId);
                orderSuccess.putExtra("order_summary", order_summary.toString());
                orderSuccess.putExtra("delivery_address", delivery_address.toString());
                startActivity(orderSuccess);
                Constants.showToastInMiddle(getApplicationContext(), mJsonObject.getString("status_message"));
                Bundle params = new Bundle();
                params.putString("payment_method_name",type_name);
                params.putString("delivery_address",delivery_address.toString());
                params.putString("order_id",OrderId);
                params.putString("OrderFrom","Android");
                params.putString("order_summary",order_summary.toString());
                mFirebaseAnalytics.logEvent("payment_failed", params);
                logger.logEvent("payment_failed", params);
            }
        } catch (JSONException e) {
            e.printStackTrace();

            Intent orderSuccess = new Intent(PaymentOptionsAvailable.this, OrderSuccess.class);
            orderSuccess.putExtra("status", "Failure");
            orderSuccess.putExtra("order_id", OrderId);
            orderSuccess.putExtra("order_summary", order_summary.toString());
            orderSuccess.putExtra("delivery_address", delivery_address.toString());
            startActivity(orderSuccess);
            Constants.showToastInMiddle(getApplicationContext(), modelState);

            Bundle params = new Bundle();
            params.putString("payment_method_name",type_name);
            params.putString("delivery_address",delivery_address.toString());
            params.putString("order_id",OrderId);
            params.putString("OrderFrom","Android");
            params.putString("order_summary",order_summary.toString());
            mFirebaseAnalytics.logEvent("payment_failed", params);
            logger.logEvent("payment_failed", params);
        }

        //Toast.makeText(getApplicationContext(),modelState,Toast.LENGTH_SHORT).show();
        //Intent i =new Intent(PaymentOptionsAvailable.class,)
    }

    @Override
    protected void onResume() {
        super.onResume();
        String modelState = CustomModel.getInstance().getState();
        System.out.println("Rahul : PaymentOptionsAvailable : onResume : modelState : " + modelState);

    }

    @Override
    protected void onRestart() {
        super.onRestart();
        String modelState = CustomModel.getInstance().getState();
        System.out.println("Rahul : PaymentOptionsAvailable : onResume : onRestart : " + modelState);
    }

    @Override
    public void selectPaymentMethod(String argType, String paymentgateway_type_id, String type_id, String type_name) {

        mPaymentMethodTypesAdapter.notifyDataSetChanged();
        this.paymentgateway_type_id = paymentgateway_type_id;
        this.type_id = type_id;
        this.type_name = type_name;
        switch (argType) {
            case "cash":
                isWhichPaymentType = "cash";

                break;
            case "card":
                isWhichPaymentType = "card";
                break;
            case "card_on_delivery":
                isWhichPaymentType = "card_on_delivery";
                break;

        }
    }
}
