package com.gogrocery.view;

import android.app.Dialog;
import android.content.DialogInterface;
import android.content.Intent;

import androidx.appcompat.app.AlertDialog;
import androidx.cardview.widget.CardView;
import androidx.core.content.ContextCompat;
import androidx.core.widget.NestedScrollView;
import androidx.databinding.DataBindingUtil;
import androidx.annotation.Nullable;

import com.afollestad.materialdialogs.MaterialDialog;
import com.android.volley.NetworkResponse;
import com.android.volley.ServerError;
import com.android.volley.toolbox.HttpHeaderParser;
import com.facebook.appevents.AppEventsConstants;
import com.facebook.appevents.AppEventsLogger;
import com.gogrocery.Adapters.MapAddressAdapter;
import com.gogrocery.Adapters.MyCardAdapter;
import com.gogrocery.Adapters.PaymentMethodTypesAdapter;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.PaymentCardInterface;
import com.gogrocery.Interfaces.PaymentMethodTypesInterface;
import com.gogrocery.Interfaces.SelectAddressInterface;
import com.gogrocery.Models.MyCardList.Card;
import com.gogrocery.Models.MyCardList.CardListModel;
import com.gogrocery.Models.MyOrdersFromMailModel.MyOrdersFromMailData;
import com.gogrocery.Models.MyOrdersHistoryModel.Data;
import com.gogrocery.Models.PaymentTransaction.PaymentTransactionModel;
import com.gogrocery.Models.PaymentTypesModel.ApiStatus;
import com.gogrocery.Models.PaymentTypesModel.PaymentMethodModel;
import com.gogrocery.R;
import com.google.android.material.bottomsheet.BottomSheetDialog;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowManager;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
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
import com.github.ybq.android.spinkit.SpinKitView;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Customs.RecyclerTouchListener;
import com.gogrocery.Models.CartSummaryModel.CartSummaryModel;
import com.gogrocery.Models.DeliverySlotModel.DeliverySlotModel;
import com.gogrocery.Models.MyAddressesModel.MyAddressesModel;
import com.gogrocery.databinding.ActivityDeliveryDetailBinding;
import com.google.android.material.textfield.TextInputEditText;
import com.google.android.material.textfield.TextInputLayout;
import com.google.firebase.analytics.FirebaseAnalytics;
import com.google.gson.Gson;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
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

public class DeliveryDetail extends AppCompatActivity implements PaymentMethodTypesInterface, CustomModel.OnCustomStateListener, PaymentCardInterface {

    AppEventsLogger logger;
    private FirebaseAnalytics mFirebaseAnalytics;
    private SharedPreferenceManager mSharedPreferenceManager;
    private ActivityDeliveryDetailBinding mActivityDeliveryDetailBinding;
    private RecyclerTouchListener onTouchListener;
    private boolean isMyaddressLoaded = false, isDeliverySlotLoaded = false;
    private String address_book_id = "", delivery_slot_time = "", delivery_slot_date = "";
    private BottomSheetDialog mBottomSheetDialogDeliverySlot;
    private Dialog mPromocodeDialog;
    private String order_id = "", rule_id = "", usability_limit = "";
    private String paramRedeemAmount = "0.0", paramCouponcode = "", productNameLists = "", productIdList = "";
    private List<ApiStatus> mApiStatusList = new ArrayList<>();
    private List<Card> mCardList = new ArrayList<>();
    private PaymentMethodTypesAdapter mPaymentMethodTypesAdapter;
    private String isWhichPaymentType = "";
    private String paymentgateway_type_id = "", type_id = "", type_name = "";
    private String OrderDetail = "", OrderId = "", cust_orders_id = "", mTotalAmount = "", mWarehouseId = "";
    private String mTransactionId = "";
    private String addressSelected = "";
private MyCardAdapter myCardAdapter;
    private Dialog orderSummaryDialog;
    private boolean isOrderConfirm = false;;

    // private MyOrdersFromMailData myOrdersFromMailData;
    private JSONObject order_summary;
    private JSONObject delivery_address;
    private String billing_name = "", billing_street_address = "", billing_country_name = "", billing_state_name = "", billing_email = "", billing_phone = "", billing_city = "";
    private String delivery_name = "", delivery_street_address = "", delivery_country_name = "", delivery_state_name = "", delivery_email = "", delivery_phone = "", delivery_city = "",si_ref_no="";
    BottomSheetDialog mChangeAddressDialog;
    // boolean isSelectAddress = false;
    @Override

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityDeliveryDetailBinding = DataBindingUtil.setContentView(this, R.layout.activity_delivery_detail);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        mActivityDeliveryDetailBinding.btnPay.setClickable(true);
        mFirebaseAnalytics = FirebaseAnalytics.getInstance(this);
        logger = AppEventsLogger.newLogger(this);
        CustomModel.getInstance().setListener(this);
        hideStatusBarColor();
  /*      mActivityDeliveryDetailBinding.rlOffertag.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showPromoCodeDialog();
            }
        });*/

        getBundel();
        setClickListners();
        try {
            if (Constants.isInternetConnected(DeliveryDetail.this)) {
           /*     if(mSharedPreferenceManager.getSelectedAddressId()!=null&&!mSharedPreferenceManager.getSelectedAddressId().isEmpty()) {



                    mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.VISIBLE);
                }else {
                    Intent ivPinLocation = new Intent(DeliveryDetail.this, AddNewAddress.class);
                    ivPinLocation.putExtra("from","");
                    startActivityForResult(ivPinLocation, 1);
                }*/
                /*  requestCheckDeliveryAddresses();*/
             /*   if(Constants.VARIABLES.SELECTED_ADDRESS_ID == null && Constants.VARIABLES.SELECTED_ADDRESS_ID.isEmpty()){
                    requestCheckDeliveryAddresses();
                }*/
                requestPaymentMethods();

                requestDeliverySlot();
                requestCheckLoyaltyBalance();

                requestMyCardList();

            } else {

                Constants.setSnackBar(DeliveryDetail.this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));

            }
        } catch (JSONException e) {
            e.printStackTrace();
        }



        Constants.VARIABLES.CURRENT_CURRENCY = mSharedPreferenceManager.getCurrentCurrency();
    }

    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }

    private void setPaymentMethodRecyclerView() {
        mPaymentMethodTypesAdapter = new PaymentMethodTypesAdapter(getApplicationContext(), mApiStatusList, this);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.VERTICAL, false);
        mActivityDeliveryDetailBinding.rvPaymentTypes.setLayoutManager(mLayoutManager);
      /*  mActivityDeliveryDetailBinding.rvPaymentTypes.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        mActivityDeliveryDetailBinding.rvPaymentTypes.setItemAnimator(new DefaultItemAnimator());*/
        mActivityDeliveryDetailBinding.rvPaymentTypes.setAdapter(mPaymentMethodTypesAdapter);
        mActivityDeliveryDetailBinding.rvPaymentTypes.setNestedScrollingEnabled(false);
    }

    private void setCardPaymentListRecyclerView() {
        myCardAdapter = new MyCardAdapter(getApplicationContext(), mCardList, this,"");
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.VERTICAL, false);
        mActivityDeliveryDetailBinding.rvPaymentCardList.setLayoutManager(mLayoutManager);
      /*  mActivityDeliveryDetailBinding.rvPaymentTypes.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        mActivityDeliveryDetailBinding.rvPaymentTypes.setItemAnimator(new DefaultItemAnimator());*/
        mActivityDeliveryDetailBinding.rvPaymentCardList.setAdapter(myCardAdapter);
        mActivityDeliveryDetailBinding.rvPaymentCardList.setNestedScrollingEnabled(false);
    }



    private void setupSpinnerTme(String[] argDeliverySlot, String[] mDeliverySlotDate, String[] mDeliverySlotTime) {
      /*  timeSlot = new ArrayList<>();
        timeSlot.add("Select Time");
        timeSlot.addAll(getTimeSlot());*/
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, R.layout.spinner_item, argDeliverySlot);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        mActivityDeliveryDetailBinding.spDeliverySlot.setAdapter(adapter);

        mActivityDeliveryDetailBinding.spDeliverySlot.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                /* if (position != 0) {*/
                  /*  SelectedTime = getTimeList().get(position);
                    isSelectedTime = true;*/
                delivery_slot_date = mDeliverySlotDate[position];
                delivery_slot_time = mDeliverySlotTime[position];

                //   }
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                // isSelectedTime = false;

            }
        });
    }

    private void getBundel() {
        Bundle mBundle = getIntent().getExtras();

        order_id = mBundle.getString("order_id");
        paramCouponcode = mBundle.getString("coupon_code");
  /*      mActivityDeliveryDetailBinding.tvSubtotal.setText(mBundle.getString("subtotal"));
        mActivityDeliveryDetailBinding.tvDiscount.setText(mBundle.getString("discount"));
        mActivityDeliveryDetailBinding.tvDeliveryCharges.setText(mBundle.getString("delivery_charges"));
        mActivityDeliveryDetailBinding.tvEstimatedTax.setText(mBundle.getString("estimated_tax"));
        mActivityDeliveryDetailBinding.tvTotalSumPrice.setText(mBundle.getString("final_amount"));
        mActivityDeliveryDetailBinding.tvPlaceOrderPrice.setText(mBundle.getString("final_amount"));*/


    }

    private void setClickListners() {
        mActivityDeliveryDetailBinding.btnChangeAddAddresses.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent btnChangeAddAddresses = new Intent(DeliveryDetail.this, MyAddresses.class);
                btnChangeAddAddresses.putExtra("from", "Delivery_Detail");
                startActivityForResult(btnChangeAddAddresses, 1);
            }
        });

        mActivityDeliveryDetailBinding.btnPay.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                if (delivery_slot_date.isEmpty() || delivery_slot_time.isEmpty()) {
                    Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.please_choose_delivery_slot));

                    // Toast.makeText(getApplicationContext(), "Please choose delivery slot", Toast.LENGTH_LONG).show();
                } else {
                    setPassingParam();

                    switch (isWhichPaymentType) {

                        case "cash":
                            if(!isOrderConfirm) {
                                showOrderSummaryDialog(String.valueOf(mActivityDeliveryDetailBinding.tvTotalSumPrice.getText()), getResources().getString(R.string.cash_on_delivery), String.valueOf(mActivityDeliveryDetailBinding.tvAddress.getText()));

                            }
                         /*   try {


                                requestSelectAddress(address_book_id);
                                //    requestPayment(OrderId);
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }*/
                            break;
                        case "card":
                            if(!isOrderConfirm) {
                                if (si_ref_no != null && !si_ref_no.equals("")) {
                                    showOrderSummaryDialog(String.valueOf(mActivityDeliveryDetailBinding.tvTotalSumPrice.getText()), getResources().getString(R.string.online_payment), String.valueOf(mActivityDeliveryDetailBinding.tvAddress.getText()));
                                } else {
                                    Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.please_select_any_card_from_the_list));
                                }
                            }

                            /*
                            try {
                                requestSelectAddress(address_book_id);
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }*/
                            break;
                        case "card_on_delivery":
                            if(!isOrderConfirm) {
                                showOrderSummaryDialog(String.valueOf(mActivityDeliveryDetailBinding.tvTotalSumPrice.getText()), getResources().getString(R.string.card_on_delivery), String.valueOf(mActivityDeliveryDetailBinding.tvAddress.getText()));
                            }
                          /*  try {
                                requestSelectAddress(address_book_id);
                                /// requestPayment(OrderId);
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }*/
                            break;
                        default:
                            Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.please_select_any_one_payment_option));
                            //  Toast.makeText(getApplicationContext(), "Please select any one Payment Option", Toast.LENGTH_LONG).show();
                            break;
                    }
                 /*   try {
                        requestSelectAddress(address_book_id);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }*/
                }
            }
        });

        mActivityDeliveryDetailBinding.btnChangeCard.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                changeCardDialog();
                //   setPassingParam();
            }
        });


        mActivityDeliveryDetailBinding.ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
        mActivityDeliveryDetailBinding.rlApplyPromo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showPromoCodeDialog();
            }
        });

        mActivityDeliveryDetailBinding.cvClose.setOnClickListener(v -> {
            mActivityDeliveryDetailBinding.cvClose.setVisibility(View.GONE);
            try {
                requestRemoveApplyPromoCode("");
            } catch (JSONException e) {
                e.printStackTrace();
            }
        });


/*        mActivityDeliveryDetailBinding.cbApplyWallet.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    if (mActivityDeliveryDetailBinding.cbApplyWallet.isChecked()) {
                        paramRedeemAmount = usability_limit;
                        requestApplyLoyalty(usability_limit);

                    } else {
                        paramRedeemAmount = "0.0";
                        requestApplyLoyalty("0");
                    }
                } catch (Exception e) {

                }
            }

        });*/
    }

    public void requestPaymentTransaction(String orderId,String siRefNo) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("order_id", orderId);
        if(!siRefNo.equals("0")) {
            mJsonObject.put("si_ref_no", siRefNo);
        }

        System.out.println("Rahul : PaymentOptionsAvailable : requestPaymentTransaction : mJsonObject : " + mJsonObject.toString());

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.PAYMENT_TRANSACTION, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                        System.out.println("Rahul : PaymentOptionsAvailable : requestPaymentTransaction : response : " + response.toString());
                        try {
                            Gson mGson = new Gson();
                            PaymentTransactionModel mPaymentTransactionModel = mGson.fromJson(response.toString(), PaymentTransactionModel.class);

                            mTransactionId = mPaymentTransactionModel.getTransactionData().getTransactionId();
                            if(mPaymentTransactionModel.getTransactionData().getPaymentRedirect()||siRefNo.equals("0")) {

                                setCCAvenueInitialDetails();
                            }else {

                                Intent orderSuccess = new Intent(DeliveryDetail.this, OrderSuccess.class);
                                orderSuccess.putExtra("status", "Success");
                                orderSuccess.putExtra("order_id", OrderId);
                                orderSuccess.putExtra("order_summary", order_summary.toString());
                                orderSuccess.putExtra("delivery_address", delivery_address.toString());
                                startActivity(orderSuccess);
                            }

                            Bundle params = new Bundle();
                            params.putString("payment_method_name", type_name);
                            params.putString("delivery_address", delivery_address.toString());
                            params.putString("OrderFrom", "Android");
                            params.putString("order_id", orderId);
                            params.putString("order_summary", order_summary.toString());
                            params.putString("total_amount_purchased", "" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mTotalAmount)));
                            params.putString("content_type", "product_group");
                            params.putString("total_item_count", Constants.VARIABLES.CART_COUNT + "");
                            params.putString("currency", Constants.VARIABLES.CURRENT_CURRENCY);
                            params.putString("customer", mActivityDeliveryDetailBinding.tvName.getText().toString() + "," + mActivityDeliveryDetailBinding.tvAddress.getText().toString() + "," + mActivityDeliveryDetailBinding.tvMobileNumber.getText().toString() + "," + mSharedPreferenceManager.key_email);
                            logger.logEvent("AddPaymentInfo", params);
                            mFirebaseAnalytics.logEvent("AddPaymentInfo", params);

                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : PaymentOptionsAvailable : requestPaymentTransaction : VolleyError : " + error.toString());
            }
        }) {
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


    public void requestSaveOrder() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        mActivityDeliveryDetailBinding.btnPay.setClickable(false);
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));
        mJsonObject.put("address_book_id", Integer.parseInt(address_book_id));
        mJsonObject.put("time_slot_date", delivery_slot_date);
        mJsonObject.put("time_slot_time", delivery_slot_time);
        mJsonObject.put("special_instruction", Constants.VARIABLES.SPECIAL_INSTRUCTION);
        mJsonObject.put("coupon_code", paramCouponcode);
        mJsonObject.put("redeem_amount", Double.parseDouble(paramRedeemAmount));
        mJsonObject.put("rule_id", "");
        mJsonObject.put("website_id", 1);
        mJsonObject.put("webshop_id", 32);
        mJsonObject.put("warehouse_id", Integer.parseInt(mSharedPreferenceManager.getWarehouseId()));
        mJsonObject.put("payment_method_id", Integer.parseInt(paymentgateway_type_id));
        mJsonObject.put("payment_type_id", Integer.parseInt(type_id));
        mJsonObject.put("payment_method_name", type_name);
        if(!si_ref_no.equals("0")&&!si_ref_no.equals("")) {
            mJsonObject.put("si_ref_no", si_ref_no);
        }

       /* {
            "device_id":"CBGTD44KDH",
                "user_id":1,
                "address_book_id":47,
                "time_slot_date":"2019-05-14",
                "time_slot_time":"17:00-19:30",
                "special_instruction":"",
                "coupon_code":"TESTLFC",
                "time_slot_id":"5:00 PM-7:30 PM",
                "website_id":1,
                "warehousid":""
        }*/
        System.out.println("Rahul : DeliveryDetail : requestSaveOrder : param : " + mJsonObject);
        System.out.println("Rahul : DeliveryDetail : requestSaveOrder : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST, Constants.BASE_URL + Constants.API_METHODS.SAVE_CART_SI, mJsonObject,//Live
                //  JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST, Constants.BASE_URL + Constants.API_METHODS.SAVE_CART, mJsonObject,//development
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : DeliveryDetail : requestSaveOrder : response : " + response);
                        try {
                            if (response.getInt("status") == 200) {


                                if (isWhichPaymentType.equals("card")) {


                                    //                            OrderDetail = getIntent().getExtras().getString("order_detail");

                                    try {
                                        OrderId = response.getString("order_id");
                                        cust_orders_id = response.getString("order_id");
                                        Double totalPrice = Double.parseDouble(response.getJSONObject("order_data").getString("gross_amount"));
                                        String totalvalue = String.valueOf(totalPrice.intValue());

                                        mTotalAmount = Constants.twoDecimalRoundOff(Double.parseDouble(totalvalue));
                                        String billingName = response.getJSONObject("order_data").getJSONObject("customer_info").getString("billing_name");
                                        String billingStreetAddress = response.getJSONObject("order_data").getJSONObject("customer_info").getString("billing_street_address");
                                        String billingCountryName = response.getJSONObject("order_data").getJSONObject("customer_info").getString("billing_country_name");
                                        String billingStateName = response.getJSONObject("order_data").getJSONObject("customer_info").getString("billing_state_name");
                                        String billingPhone = response.getJSONObject("order_data").getJSONObject("customer_info").getString("billing_phone");

                                        String deliveryName = response.getJSONObject("order_data").getJSONObject("customer_info").getString("delivery_name");
                                        String deliveryStreetAddress = response.getJSONObject("order_data").getJSONObject("customer_info").getString("delivery_street_address");
                                        String deliveryCountryName = response.getJSONObject("order_data").getJSONObject("customer_info").getString("delivery_country_name");
                                        String deliveryStateName = response.getJSONObject("order_data").getJSONObject("customer_info").getString("delivery_state_name");
                                        String deliveryEmail = response.getJSONObject("order_data").getJSONObject("customer_info").getString("delivery_email_address");
                                        String deliveryPhone = response.getJSONObject("order_data").getJSONObject("customer_info").getString("delivery_phone");
                                        JSONObject delivery_address = new JSONObject();


                                        delivery_address.put("address", mActivityDeliveryDetailBinding.tvAddress.getText().toString());
                                        delivery_address.put("number", mActivityDeliveryDetailBinding.tvMobileNumber.getText().toString());
                                        delivery_address.put("name", mActivityDeliveryDetailBinding.tvName.getText().toString());
                                        if (billingName != null) {
                                            billing_name = billingName;
                                        }
                                        if (billingStreetAddress != null) {
                                            billing_street_address = billingStreetAddress;
                                        }

                                        if (billingCountryName != null) {
                                            billing_country_name = billingCountryName;
                                        }

                                        if (billingStateName != null) {
                                            billing_state_name = billingStateName;
                                        }

                                        if (billingPhone != null) {
                                            billing_phone = billingPhone;
                                        }

                                        if (deliveryName != null) {
                                            delivery_name = deliveryName;

                                        }

                                        if (deliveryStreetAddress != null) {
                                            delivery_street_address = deliveryStreetAddress;
                                        }

                                        if (deliveryEmail != null) {
                                            delivery_email = deliveryEmail;
                                        }

                                        if (deliveryPhone != null) {
                                            delivery_phone = deliveryPhone;
                                        }

                                        if (deliveryCountryName != null) {
                                            delivery_country_name = deliveryCountryName;

                                        }
                                        if (deliveryStateName != null) {
                                            delivery_street_address = deliveryStateName;
                                        }


                                        billing_city = "Basara";
                                        delivery_city = "Basara";


                                        requestPaymentTransaction(OrderId,si_ref_no);
                                    } catch (JSONException e) {
                                        e.printStackTrace();
                                    }

                                } else {
                                    try {
                                        requestEmptyCartOrderSuccess();

                                    } catch (JSONException e) {
                                        e.printStackTrace();
                                    }

                                    try {
                                        Constants.VARIABLES.SPECIAL_INSTRUCTION = "";
                                        JSONObject order_summary = new JSONObject();
                                        JSONObject delivery_address = new JSONObject();

                                        order_summary.put("subtotal", mActivityDeliveryDetailBinding.tvSubtotal.getText().toString());
                                        if (mActivityDeliveryDetailBinding.tvAppliedLoyaltyAmount.getText().equals("AED 0.00")) {
                                            order_summary.put("loyalty_amount", "0.00");
                                        } else {
                                            order_summary.put("loyalty_amount", mActivityDeliveryDetailBinding.tvAppliedLoyaltyAmount.getText().toString());
                                        }

                                        order_summary.put("coupon_discount", mActivityDeliveryDetailBinding.tvDiscount.getText().toString());
                                        order_summary.put("delivery", mActivityDeliveryDetailBinding.tvDeliveryCharges.getText().toString());
                                        order_summary.put("tax", mActivityDeliveryDetailBinding.tvEstimatedTax.getText().toString());
                                        order_summary.put("final_total", mActivityDeliveryDetailBinding.tvTotalSumPrice.getText().toString());

                                        delivery_address.put("name", mActivityDeliveryDetailBinding.tvName.getText().toString());
                                        delivery_address.put("address", mActivityDeliveryDetailBinding.tvAddress.getText().toString());
                                        delivery_address.put("number", mActivityDeliveryDetailBinding.tvMobileNumber.getText().toString());


                                        Intent orderSuccess = new Intent(DeliveryDetail.this, OrderSuccess.class);
                                        orderSuccess.putExtra("status", "Success");
                                        orderSuccess.putExtra("order_id", response.getString("order_id"));
                                        orderSuccess.putExtra("order_summary", order_summary.toString());
                                        orderSuccess.putExtra("delivery_address", delivery_address.toString());
                                        startActivity(orderSuccess);
                                        Bundle params = new Bundle();
                                        params.putString("total_amount_purchased", mActivityDeliveryDetailBinding.tvTotalSumPrice.getText().toString());
                                        params.putString("address_book_id", address_book_id);
                                        params.putString("warehouse_id", mSharedPreferenceManager.getWarehouseId());
                                        params.putString("order_id", response.getString("order_id"));
                                        params.putString("OrderFrom", "Android");
                                        params.putString("order_summary", order_summary.toString());
                                        params.putString("content_type", "product_group");
                                        params.putString("productName", productNameLists);
                                        params.putString("productId", productIdList);
                                        params.putString("total_item_count", Constants.VARIABLES.CART_COUNT + "");
                                        params.putString("currency", Constants.VARIABLES.CURRENT_CURRENCY);
                                        params.putString("customer", mActivityDeliveryDetailBinding.tvName.getText().toString() + "," + mActivityDeliveryDetailBinding.tvAddress.getText().toString() + "," + mActivityDeliveryDetailBinding.tvMobileNumber.getText().toString() + "," + mSharedPreferenceManager.key_email);
                                        mFirebaseAnalytics.logEvent("Purchase", params);
                                        logger.logEvent("Purchase", params);

                                    } catch (JSONException e) {
                                        e.printStackTrace();
                                        System.out.println("Rahul : DeliveryDetail : requestSaveOrder : response : " + e);
                                    }
                                }
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                        mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                        mActivityDeliveryDetailBinding.btnPay.setClickable(true);

                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                NetworkResponse response = error.networkResponse;
                if (error instanceof ServerError && response != null) {

                    String res = null;
                    try {
                        res = new String(response.data,
                                HttpHeaderParser.parseCharset(response.headers, "utf-8"));
                        JSONObject obj = null;
                        try {
                            obj = new JSONObject(res);
                            String message = obj.getString("message");

                            // CommonValidation.alertDialogShow(DeliveryActivity.this,getResources().getString(R.string.error),obj.getString("message"));
                            mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                            new AlertDialog.Builder(DeliveryDetail.this)
                                    .setTitle(getResources().getString(R.string.confirmation))
                                    .setMessage(getResources().getString(R.string.you_can_not_purchase_only_prepaid_card))

                                    // Specifying a listener allows you to take an action before dismissing the dialog.
                                    // The dialog is automatically dismissed when a dialog button is clicked.
                                    .setPositiveButton(R.string.okey, new DialogInterface.OnClickListener() {
                                        public void onClick(DialogInterface dialog, int which) {
                                      /*      startActivity(new Intent(DeliveryDetail.this, MainActivityNew.class));
                                            finish();
*/
                                        }
                                    })

                                    // A null listener allows the button to dismiss the dialog and take no further action.
                                    // .setNegativeButton(android.R.string.no, null)
                                    .setIcon(android.R.drawable.ic_dialog_alert)
                                    .show();
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    } catch (UnsupportedEncodingException e) {
                        e.printStackTrace();
                    }
                    // Now you can use any deserializer to make sense of data


                    // callback.onError();







               /* if(error.networkResponse.statusCode==417)
                {
                    System.out.println("Rahul : DeliveryDetail : requestSaveOrder : 1 : "+error.networkResponse.data.toString());
                    System.out.println("Rahul : DeliveryDetail : requestSaveOrder : 2 : "+error.networkResponse.toString());
                    System.out.println("Rahul : DeliveryDetail : requestSaveOrder : 3 : "+new Gson().toJson(error.networkResponse.toString()));
                    System.out.println("Rahul : DeliveryDetail : requestSaveOrder : 1 : "+error.networkResponse.data.toString());
                }*/

                    mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                    //   mActivityDeliveryDetailBinding.btnContinue.setClickable(true);

                }
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


    public void requestMyAddresses() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        System.out.println("Rahul : MyAddresses : requestMyAddresses : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.ADDRESSES, null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        isMyaddressLoaded = true;

                        try {
                            if (response.getJSONArray("data").length() == 0) {
                                Intent i = new Intent(DeliveryDetail.this, AddNewAddress.class);
                                i.putExtra("from", "");
                                startActivityForResult(i, 1);

                            } else {
                                try {
                                    if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                        System.out.println("Rahul : MyAddresses : requestMyAddresses : response : " + response);

                                        setPageUI(response);
                                    } else {
                                        Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.no_address_found));

                                        //Toast.makeText(getApplicationContext(), "No Address Found!", Toast.LENGTH_LONG).show();
                                    }

                                } catch (JSONException e) {
                                    e.printStackTrace();
                                    isMyaddressLoaded = true;
                                    if (isDeliverySlotLoaded && isMyaddressLoaded) {
                                        mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                                    }
                                }

                            }
                        } catch (JSONException e) {
                            isMyaddressLoaded = true;
                            e.printStackTrace();
                            if (isDeliverySlotLoaded && isMyaddressLoaded) {
                                mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                            }
                        }
                        if (isDeliverySlotLoaded && isMyaddressLoaded) {
                            mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                if (error.getClass().toString().contains("class com.android.volley.ParseError")) {
                    Intent i = new Intent(DeliveryDetail.this, AddNewAddress.class);
                    i.putExtra("from", "");
                    startActivityForResult(i, 1);
                    mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);

                } else {
                    NetworkResponse response = error.networkResponse;
                    if (error instanceof ServerError && response != null) {
                        try {
                            String res = new String(response.data,
                                    HttpHeaderParser.parseCharset(response.headers, "utf-8"));
                            // Now you can use any deserializer to make sense of data
                            JSONObject obj = new JSONObject(res);
                            String message = obj.getString("message");
                            // CommonValidation.alertDialogShow(DeliveryActivity.this,getResources().getString(R.string.error),obj.getString("message"));
                            mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                            new AlertDialog.Builder(DeliveryDetail.this)
                                    .setTitle(getResources().getString(R.string.user_blocked))
                                    .setMessage(message)

                                    // Specifying a listener allows you to take an action before dismissing the dialog.
                                    // The dialog is automatically dismissed when a dialog button is clicked.
                                    .setPositiveButton(R.string.okey, new DialogInterface.OnClickListener() {
                                        public void onClick(DialogInterface dialog, int which) {
                                            try {
                                                requestEmptyCart();
                                                dialog.dismiss();
                                            } catch (JSONException e) {
                                                e.printStackTrace();
                                            }

                                        }
                                    })

                                    // A null listener allows the button to dismiss the dialog and take no further action.
                                    //.setNegativeButton(android.R.string.no, null)
                                    .setIcon(android.R.drawable.ic_dialog_alert)
                                    .show();


                            // callback.onError();
                        } catch (UnsupportedEncodingException e1) {
                            // Couldn't properly decode data to string
                            e1.printStackTrace();
                        } catch (JSONException e2) {
                            // returned data is not JSONObject?
                            e2.printStackTrace();
                        }
                    }
                }

                isMyaddressLoaded = true;
                System.out.println("Sukdev : MyAddresses : requestMyAddresses : VolleyError : " + error.getClass());
                if (isDeliverySlotLoaded && isMyaddressLoaded) {
                    mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                }
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
    }


    public void requestCheckDeliveryAddresses() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        System.out.println("Rahul : MyAddresses : requestMyAddresses : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("lat", mSharedPreferenceManager.getLatitude());
        mJsonObject.put("lng", mSharedPreferenceManager.getLongitude());
        System.out.println("Rahul : CheckDeliveryAddress : checkDelivery : mJsonObject : " + mJsonObject.toString());
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.CHECK_DELIVERY_ADDRESS, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : CheckDeliveryAddress : checkDelivery : response : " + response.toString());
                        isMyaddressLoaded = true;
                        //  {"status":200,"addressMatch":false,"data":{},"distance":999999999999}
                        try {
                            if (response.getString("addressMatch").equals("false")) {
                                if (response.getJSONArray("data").length() > 0) {

                                    showNotMatchAnyAddressPopup();
                                } else {
                                    showAddAddressPopup();
                                }
                         /*       Intent i = new Intent(DeliveryDetail.this, AddNewAddress.class);
                                i.putExtra("from","");
                                startActivityForResult(i, 1);*/

                            } else {
                                try {
                                    if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                        System.out.println("Rahul : MyAddresses : requestMyAddresses : response : " + response);

                                        setPageUIFromCheckAddress(response);
                                    } else {
                                        Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.no_address_found));

                                        //Toast.makeText(getApplicationContext(), "No Address Found!", Toast.LENGTH_LONG).show();
                                    }

                                } catch (JSONException e) {
                                    e.printStackTrace();
                                    isMyaddressLoaded = true;
                                    if (isDeliverySlotLoaded && isMyaddressLoaded) {
                                        mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                                    }
                                }

                            }
                        } catch (JSONException e) {
                            isMyaddressLoaded = true;
                            e.printStackTrace();
                            if (isDeliverySlotLoaded && isMyaddressLoaded) {
                                mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                            }
                        }
                        if (isDeliverySlotLoaded && isMyaddressLoaded) {
                            mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                if (error.getClass().toString().contains("class com.android.volley.ParseError")) {
                    Intent i = new Intent(DeliveryDetail.this, AddNewAddress.class);
                    i.putExtra("from", "");
                    startActivityForResult(i, 1);
                    mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);

                } else {
                    NetworkResponse response = error.networkResponse;
                    if (error instanceof ServerError && response != null) {
                        try {
                            String res = new String(response.data,
                                    HttpHeaderParser.parseCharset(response.headers, "utf-8"));
                            // Now you can use any deserializer to make sense of data
                            JSONObject obj = new JSONObject(res);
                            String message = obj.getString("message");
                            // CommonValidation.alertDialogShow(DeliveryActivity.this,getResources().getString(R.string.error),obj.getString("message"));
                            mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);

                            // callback.onError();
                        } catch (UnsupportedEncodingException e1) {
                            // Couldn't properly decode data to string
                            e1.printStackTrace();
                        } catch (JSONException e2) {
                            // returned data is not JSONObject?
                            e2.printStackTrace();
                        }
                    }
                }

                isMyaddressLoaded = true;
                System.out.println("Sukdev : MyAddresses : requestMyAddresses : VolleyError : " + error.getClass());
                if (isDeliverySlotLoaded && isMyaddressLoaded) {
                    mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                }
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
    }


    public void requestEmptyCart() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        findViewById(R.id.progressSpinKitView).setVisibility(View.VISIBLE);
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));
        mJsonObject.put("website_id", 1);
        System.out.println("Rahul : MapLocationSelectionUpdate : requestEmptyCart : mJsonObject : " + mJsonObject.toString());

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.EMPTY_CART, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : MapLocationSelectionUpdate : requestEmptyCart : response : " + response.toString());
                        findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                        try {
                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                // Constants.VARIABLES.SELECTED_ADDRESS_ID="";

                                new DatabaseHandler(getApplicationContext()).deleteAllRecord();
                                Intent i = new Intent(DeliveryDetail.this, LoginActivity.class);
                                startActivity(i);

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

    public void requestEmptyCartOrderSuccess() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        //findViewById(R.id.progressSpinKitView).setVisibility(View.VISIBLE);
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));
        mJsonObject.put("website_id", 1);

        System.out.println("Rahul : MapLocationSelectionUpdate : requestEmptyCart : mJsonObject : " + mJsonObject.toString());

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.EMPTY_CART, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : MapLocationSelectionUpdate : requestEmptyCart : response : " + response.toString());
                        //  findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                        try {
                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                new DatabaseHandler(getApplicationContext()).deleteAllRecord();
                                // Constants.VARIABLES.SELECTED_ADDRESS_ID="";
                                mSharedPreferenceManager.storeSelectedAddressId("");
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                // findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
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

    public void requestMyCardList() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        findViewById(R.id.progressSpinKitView).setVisibility(View.VISIBLE);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.PAYMENT_REQUEST_SI_CHARGES_LIST, null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : DeliveryDetails : requestCardList : response : " + response.toString());
                        findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                        try {
                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                // Constants.VARIABLES.SELECTED_ADDRESS_ID="";

                                Gson mGson = new Gson();
                                CardListModel mCardListModel = mGson.fromJson(response.toString(), CardListModel.class);
                                System.out.println("Rahul : DeliveryDetail : requestCardList : mCardListModel: " + mGson.toJson(mCardListModel));

                                if (mCardListModel.getCardList().size() > 0) {
                                    mCardList.clear();
                                    mCardList.addAll(mCardListModel.getCardList());

                                    for(int i=0 ; i<mCardList.size();i++) {
                                        if (mCardList.get(i).getIsDefault().equals("y")){
                                            mActivityDeliveryDetailBinding.tvPreferences.setText(mCardList.get(i).getCardType() + "\n **** **** **** " + mCardList.get(i).getCardSuffix());
                                        si_ref_no = mCardList.get(i).getSiSubRefNo();
                                            mPaymentMethodTypesAdapter.isAlreadySavedCard(true);

                                    }else {

                                            mActivityDeliveryDetailBinding.tvPreferences.setText(mCardList.get(0).getCardType() + "\n **** **** **** " + mCardList.get(0).getCardSuffix());
                                            si_ref_no = mCardList.get(0).getSiSubRefNo();
                                            mPaymentMethodTypesAdapter.isAlreadySavedCard(true);
                                        }

                                    }
                               /*     Card mCard= new Card();
                                    mCard.setCardSuffix("");
                                    mCard.setCardType("Add New Card");
                                    mCard.setSiSubRefNo("0");
                                    mCardList.add(mCard);*/
                               //     setCardPaymentListRecyclerView();

                                    System.out.println("Rahul : DeliveryDetail : requestDeliverySlot : requestCardList : size : " + mCardListModel.getCardList().size());

                                }
                                else {
                                    si_ref_no= "0";

                               /*     mCardList.clear();
                                    Card mCard= new Card();
                                    mCard.setCardSuffix("");
                                    mCard.setCardType("Add Card");
                                    mCard.setSiSubRefNo("0");
                                    mCardList.add(mCard);
                                    mActivityDeliveryDetailBinding.cvBtnAddNewCard.setVisibility(View.GONE);*/
                                }
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                mPaymentMethodTypesAdapter.isAlreadySavedCard(false);
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

    public void requestDeliverySlot() throws JSONException {
        //  mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.VISIBLE);

        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        System.out.println("Rahul : MyAddresses : requestDeliverySlot : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.DELIVERY_SLOT + mSharedPreferenceManager.getWarehouseId() + "/", null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        isDeliverySlotLoaded = true;
                        System.out.println("Rahul : DeliveryDetail : requestDeliverySlot : response : " + response);
                        Gson mGson = new Gson();
                        DeliverySlotModel mDeliverySlotModel = mGson.fromJson(response.toString(), DeliverySlotModel.class);
                        System.out.println("Rahul : DeliveryDetail : requestDeliverySlot : mDeliverySlotModel : " + mGson.toJson(mDeliverySlotModel));

                        if (mDeliverySlotModel.getDeliverySlot().size() > 0) {
                            List<String> mSize = new ArrayList<>();
                            for (int i = 0; i < mDeliverySlotModel.getDeliverySlot().size(); i++) {
                                if (mDeliverySlotModel.getDeliverySlot().get(i).getAvailableSlot().size() != 0) {
                                    mSize.add(mDeliverySlotModel.getDeliverySlot().get(i).getAvailableSlot().get(0).getBasedOn());

                                    //System.out.println("Rahul : DeliveryDetail :  mDeliverySlotTitle : " + mDeliverySlotTitle[i]);
                                }
                            }
                            System.out.println("Rahul : DeliveryDetail : requestDeliverySlot : mDeliverySlotModel : size : " + mDeliverySlotModel.getDeliverySlot().size());
                            System.out.println("Rahul : DeliveryDetail : requestDeliverySlot : mDeliverySlotModel : size : " + mSize.size());
                            // System.out.println("Rahul : DeliveryDetail : requestDeliverySlot : mDeliverySlotModel : getAvailableSlot : " + mDeliverySlotModel.getDeliverySlot().get(0).getAvailableSlot().size());

                            String[] mDeliverySlotTitle = new String[mDeliverySlotModel.getDeliverySlot().size()];
                            String[] mDeliverySlotId = new String[mDeliverySlotModel.getDeliverySlot().size()];
                            String[] mDeliverySlotTime = new String[mDeliverySlotModel.getDeliverySlot().size()];
                            String[] mDeliverySlotDate = new String[mDeliverySlotModel.getDeliverySlot().size()];
                            for (int j = 0; j < mDeliverySlotModel.getDeliverySlot().size(); j++) {
                                if (mDeliverySlotModel.getDeliverySlot().get(j).getAvailableSlot().size() != 0) {
                                    if (mDeliverySlotModel.getDeliverySlot().get(j).getAvailableSlot().get(0).getBasedOn().toString().toLowerCase().equalsIgnoreCase("sameday")) {
                                        mDeliverySlotTitle[j] = "Same Day";
                                    } else if (mDeliverySlotModel.getDeliverySlot().get(j).getAvailableSlot().get(0).getBasedOn().toString().toLowerCase().equalsIgnoreCase("nextday")) {
                                        mDeliverySlotTitle[j] = "Next Day";
                                    }

                                    mDeliverySlotId[j] = mDeliverySlotModel.getDeliverySlot().get(j).getAvailableSlot().get(0).getDayId().toString();
                                    mDeliverySlotDate[j] = mDeliverySlotModel.getDeliverySlot().get(j).getDeliveryDate();
                                    mDeliverySlotTime[j] = mDeliverySlotModel.getDeliverySlot().get(j).getAvailableSlot().get(0).getStartTime() + "-" + mDeliverySlotModel.getDeliverySlot().get(j).getAvailableSlot().get(0).getEndTime();
                                    System.out.println("Rahul : DeliveryDetail :  mDeliverySlotTitle : " + mDeliverySlotTitle[0]);
                                }
                            }
                            setupSpinnerTme(mDeliverySlotTitle, mDeliverySlotDate, mDeliverySlotTime);
                            // setAutoCompleteDeliverySlot(mDeliverySlotTitle, mDeliverySlotId, mDeliverySlotDate, mDeliverySlotTime);

                            if (isDeliverySlotLoaded && isMyaddressLoaded) {
                                mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                            }
                        } else {
                            Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.no_delivery_slot_available));

                            //Toast.makeText(getApplicationContext(), "No delivery slot available", Toast.LENGTH_LONG).show();
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                isDeliverySlotLoaded = true;
                System.out.println("Rahul : MyAddresses : requestDeliverySlot : VolleyError : " + error.toString());
                if (isDeliverySlotLoaded && isMyaddressLoaded) {
                    mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                }

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
    }

    private void showDeliverySlot() {
        mBottomSheetDialogDeliverySlot = new BottomSheetDialog(this);
        mBottomSheetDialogDeliverySlot.setContentView(R.layout.delivery_slot_layout);
    }

    private void setPageUI(JSONObject argJSONResponse) {
        Gson mGson = new Gson();
        JSONObject mJsonObject = argJSONResponse;
        MyAddressesModel mMyAddressesModel = mGson.fromJson(mJsonObject.toString(), MyAddressesModel.class);
//String selectedAddressId = Constants.VARIABLES.SELECTED_ADDRESS_ID;
        String selectedAddressId = mSharedPreferenceManager.getSelectedAddressId();
        ;
        if (selectedAddressId != null && !selectedAddressId.isEmpty()) {
            if (mMyAddressesModel.getData().size() > 1) {
                for (int i = 0; i < mMyAddressesModel.getData().size(); i++) {
                    if (String.valueOf(mMyAddressesModel.getData().get(i).getId()).equals(selectedAddressId)) {
                        mActivityDeliveryDetailBinding.nsvDeliveryDetail.setVisibility(View.VISIBLE);
                        address_book_id = mMyAddressesModel.getData().get(i).getId().toString();
                        mActivityDeliveryDetailBinding.tvName.setText(mMyAddressesModel.getData().get(i).getDeliveryName());
                        mActivityDeliveryDetailBinding.tvAddress.setText(mMyAddressesModel.getData().get(i).getDeliveryStreetAddress() + ", " + mMyAddressesModel.getData().get(i).getDeliveryLandmark()
                                + "\n" +
                                mMyAddressesModel.getData().get(i).getDeliveryStateName() + " " + mMyAddressesModel.getData().get(i).getDeliveryCountryName());
                        mActivityDeliveryDetailBinding.tvMobileNumber.setText(mMyAddressesModel.getData().get(i).getDeliveryPhone());


                        billing_name = mMyAddressesModel.getData().get(i).getBillingName();
                        billing_street_address = mMyAddressesModel.getData().get(i).getBillingStreetAddress();
                        billing_country_name = mMyAddressesModel.getData().get(i).getBillingCountryName();
                        billing_state_name = mMyAddressesModel.getData().get(i).getBillingStateName();
                        billing_email = mMyAddressesModel.getData().get(i).getBillingEmailAddress();
                        billing_phone = mMyAddressesModel.getData().get(i).getBillingPhone();
                        billing_city = "Basara";

                        delivery_name = mMyAddressesModel.getData().get(i).getDeliveryName();
                        delivery_street_address = mMyAddressesModel.getData().get(i).getDeliveryStreetAddress();
                        delivery_country_name = mMyAddressesModel.getData().get(i).getDeliveryCountryName();
                        delivery_state_name = mMyAddressesModel.getData().get(i).getDeliveryStateName();
                        delivery_email = mMyAddressesModel.getData().get(i).getDeliveryEmailAddress();
                        delivery_phone = mMyAddressesModel.getData().get(i).getDeliveryPhone();
                        delivery_city = "Basara";
                    }
                }
            } else {
                mActivityDeliveryDetailBinding.nsvDeliveryDetail.setVisibility(View.VISIBLE);
                address_book_id = mMyAddressesModel.getData().get(0).getId().toString();
                mActivityDeliveryDetailBinding.tvName.setText(mMyAddressesModel.getData().get(0).getDeliveryName());
                mActivityDeliveryDetailBinding.tvAddress.setText(mMyAddressesModel.getData().get(0).getDeliveryStreetAddress() + ", " + mMyAddressesModel.getData().get(0).getDeliveryLandmark()
                        + "\n" +
                        mMyAddressesModel.getData().get(0).getDeliveryStateName() + " " + mMyAddressesModel.getData().get(0).getDeliveryCountryName());
                mActivityDeliveryDetailBinding.tvMobileNumber.setText(mMyAddressesModel.getData().get(0).getDeliveryPhone());


                billing_name = mMyAddressesModel.getData().get(0).getBillingName();
                billing_street_address = mMyAddressesModel.getData().get(0).getBillingStreetAddress();
                billing_country_name = mMyAddressesModel.getData().get(0).getBillingCountryName();
                billing_state_name = mMyAddressesModel.getData().get(0).getBillingStateName();
                billing_email = mMyAddressesModel.getData().get(0).getBillingEmailAddress();
                billing_phone = mMyAddressesModel.getData().get(0).getBillingPhone();
                billing_city = "Basara";

                delivery_name = mMyAddressesModel.getData().get(0).getDeliveryName();
                delivery_street_address = mMyAddressesModel.getData().get(0).getDeliveryStreetAddress();
                delivery_country_name = mMyAddressesModel.getData().get(0).getDeliveryCountryName();
                delivery_state_name = mMyAddressesModel.getData().get(0).getDeliveryStateName();
                delivery_email = mMyAddressesModel.getData().get(0).getDeliveryEmailAddress();
                delivery_phone = mMyAddressesModel.getData().get(0).getDeliveryPhone();
                delivery_city = "Basara";
            }


        }
    }/*else {
    int setprimary_count = 0;
    for (int i = 0; i < mMyAddressesModel.getData().size(); i++) {
        if (mMyAddressesModel.getData().get(i).getSetPrimary() == 1) {
            setprimary_count = setprimary_count + 1;
            mActivityDeliveryDetailBinding.nsvDeliveryDetail.setVisibility(View.VISIBLE);
            address_book_id = mMyAddressesModel.getData().get(i).getId().toString();
            mActivityDeliveryDetailBinding.tvName.setText(mMyAddressesModel.getData().get(i).getDeliveryName());
            mActivityDeliveryDetailBinding.tvAddress.setText(mMyAddressesModel.getData().get(i).getDeliveryStreetAddress() + mMyAddressesModel.getData().get(i).getDeliveryLandmark()
                    + "\n" +
                    mMyAddressesModel.getData().get(i).getDeliveryStateName() + " " + mMyAddressesModel.getData().get(i).getDeliveryCountryName());
            mActivityDeliveryDetailBinding.tvMobileNumber.setText(mMyAddressesModel.getData().get(i).getDeliveryPhone());


            billing_name = mMyAddressesModel.getData().get(i).getBillingName();
            billing_street_address = mMyAddressesModel.getData().get(i).getBillingStreetAddress();
            billing_country_name = mMyAddressesModel.getData().get(i).getBillingCountryName();
            billing_state_name = mMyAddressesModel.getData().get(i).getBillingStateName();
            billing_email = mMyAddressesModel.getData().get(i).getBillingEmailAddress();
            billing_phone = mMyAddressesModel.getData().get(i).getBillingPhone();
            billing_city = "Basara";

            delivery_name = mMyAddressesModel.getData().get(i).getDeliveryName();
            delivery_street_address = mMyAddressesModel.getData().get(i).getDeliveryStreetAddress();
            delivery_country_name = mMyAddressesModel.getData().get(i).getDeliveryCountryName();
            delivery_state_name = mMyAddressesModel.getData().get(i).getDeliveryStateName();
            delivery_email = mMyAddressesModel.getData().get(i).getDeliveryEmailAddress();
            delivery_phone = mMyAddressesModel.getData().get(i).getDeliveryPhone();
            delivery_city = "Basara";

        }
        else {
            mActivityDeliveryDetailBinding.nsvDeliveryDetail.setVisibility(View.VISIBLE);
            address_book_id = mMyAddressesModel.getData().get(0).getId().toString();
            mActivityDeliveryDetailBinding.tvName.setText(mMyAddressesModel.getData().get(0).getDeliveryName());
            mActivityDeliveryDetailBinding.tvAddress.setText(mMyAddressesModel.getData().get(0).getDeliveryStreetAddress() + mMyAddressesModel.getData().get(0).getDeliveryLandmark()
                    + "\n" +
                    mMyAddressesModel.getData().get(0).getDeliveryStateName() + " " + mMyAddressesModel.getData().get(0).getDeliveryCountryName());
            mActivityDeliveryDetailBinding.tvMobileNumber.setText(mMyAddressesModel.getData().get(0).getDeliveryPhone());


            billing_name = mMyAddressesModel.getData().get(0).getBillingName();
            billing_street_address = mMyAddressesModel.getData().get(0).getBillingStreetAddress();
            billing_country_name = mMyAddressesModel.getData().get(0).getBillingCountryName();
            billing_state_name = mMyAddressesModel.getData().get(0).getBillingStateName();
            billing_email = mMyAddressesModel.getData().get(0).getBillingEmailAddress();
            billing_phone = mMyAddressesModel.getData().get(0).getBillingPhone();
            billing_city = "Basara";

            delivery_name = mMyAddressesModel.getData().get(0).getDeliveryName();
            delivery_street_address = mMyAddressesModel.getData().get(0).getDeliveryStreetAddress();
            delivery_country_name = mMyAddressesModel.getData().get(0).getDeliveryCountryName();
            delivery_state_name = mMyAddressesModel.getData().get(0).getDeliveryStateName();
            delivery_email = mMyAddressesModel.getData().get(0).getDeliveryEmailAddress();
            delivery_phone = mMyAddressesModel.getData().get(0).getDeliveryPhone();
            delivery_city = "Basara";

        }
    }
*//*    if (setprimary_count == 0) {
        showNotMatchDefaultAddressPopup();
     *//**//*   mActivityDeliveryDetailBinding.nsvDeliveryDetail.setVisibility(View.GONE);
        Intent newi = new Intent(DeliveryDetail.this, AddNewAddress.class);
        newi.putExtra("from","");
        startActivityForResult(newi, 1);*//**//*

    }*//*
}*/


    private void setPageUIFromCheckAddress(JSONObject argJSONResponse) {
        Gson mGson = new Gson();
        JSONObject mJsonObject = argJSONResponse;
        MyAddressesModel mMyAddressesModel = mGson.fromJson(mJsonObject.toString(), MyAddressesModel.class);
        int setprimary_count = 0;

        if (mMyAddressesModel.getData().size() > 1) {
            for (int i = 0; i < mMyAddressesModel.getData().size(); i++) {

                if (mMyAddressesModel.getData().get(i).getSetPrimary() == 1) {

                    setprimary_count = setprimary_count + 1;
                    mActivityDeliveryDetailBinding.nsvDeliveryDetail.setVisibility(View.VISIBLE);
                    address_book_id = mMyAddressesModel.getData().get(i).getId().toString();
                    mActivityDeliveryDetailBinding.tvName.setText(mMyAddressesModel.getData().get(i).getDeliveryName());
                    mActivityDeliveryDetailBinding.tvAddress.setText(mMyAddressesModel.getData().get(i).getDeliveryStreetAddress() + ", " + mMyAddressesModel.getData().get(i).getDeliveryLandmark()
                            + "\n" + mMyAddressesModel.getData().get(i).getDeliveryStateName() + " " + mMyAddressesModel.getData().get(i).getDeliveryCountryName());
                    mActivityDeliveryDetailBinding.tvMobileNumber.setText(mMyAddressesModel.getData().get(i).getDeliveryPhone());


                    billing_name = mMyAddressesModel.getData().get(i).getBillingName();
                    billing_street_address = mMyAddressesModel.getData().get(i).getBillingStreetAddress();
                    billing_country_name = mMyAddressesModel.getData().get(i).getBillingCountryName();
                    billing_state_name = mMyAddressesModel.getData().get(i).getBillingStateName();
                    billing_email = mMyAddressesModel.getData().get(i).getBillingEmailAddress();
                    billing_phone = mMyAddressesModel.getData().get(i).getBillingPhone();
                    billing_city = "Basara";

                    delivery_name = mMyAddressesModel.getData().get(i).getDeliveryName();
                    delivery_street_address = mMyAddressesModel.getData().get(i).getDeliveryStreetAddress();
                    delivery_country_name = mMyAddressesModel.getData().get(i).getDeliveryCountryName();
                    delivery_state_name = mMyAddressesModel.getData().get(i).getDeliveryStateName();
                    delivery_email = mMyAddressesModel.getData().get(i).getDeliveryEmailAddress();
                    delivery_phone = mMyAddressesModel.getData().get(i).getDeliveryPhone();
                    delivery_city = "Basara";


                }
            }
            if (setprimary_count == 0) {
                showNotMatchDefaultAddressPopup();
            }
        } else {
            mActivityDeliveryDetailBinding.nsvDeliveryDetail.setVisibility(View.VISIBLE);
            address_book_id = mMyAddressesModel.getData().get(0).getId().toString();
            mActivityDeliveryDetailBinding.tvName.setText(mMyAddressesModel.getData().get(0).getDeliveryName());
            mActivityDeliveryDetailBinding.tvAddress.setText(mMyAddressesModel.getData().get(0).getDeliveryStreetAddress() + ", " + mMyAddressesModel.getData().get(0).getDeliveryLandmark()
                    + "\n" +
                    mMyAddressesModel.getData().get(0).getDeliveryStateName() + " " + mMyAddressesModel.getData().get(0).getDeliveryCountryName());
            mActivityDeliveryDetailBinding.tvMobileNumber.setText(mMyAddressesModel.getData().get(0).getDeliveryPhone());


            billing_name = mMyAddressesModel.getData().get(0).getBillingName();
            billing_street_address = mMyAddressesModel.getData().get(0).getBillingStreetAddress();
            billing_country_name = mMyAddressesModel.getData().get(0).getBillingCountryName();
            billing_state_name = mMyAddressesModel.getData().get(0).getBillingStateName();
            billing_email = mMyAddressesModel.getData().get(0).getBillingEmailAddress();
            billing_phone = mMyAddressesModel.getData().get(0).getBillingPhone();
            billing_city = "Basara";

            delivery_name = mMyAddressesModel.getData().get(0).getDeliveryName();
            delivery_street_address = mMyAddressesModel.getData().get(0).getDeliveryStreetAddress();
            delivery_country_name = mMyAddressesModel.getData().get(0).getDeliveryCountryName();
            delivery_state_name = mMyAddressesModel.getData().get(0).getDeliveryStateName();
            delivery_email = mMyAddressesModel.getData().get(0).getDeliveryEmailAddress();
            delivery_phone = mMyAddressesModel.getData().get(0).getDeliveryPhone();
            delivery_city = "Basara";

        }
    }


    private void showPromoCodeDialog() {
        mPromocodeDialog = new Dialog(this);
        mPromocodeDialog.setContentView(R.layout.apply_promocode_dialog);
        mPromocodeDialog.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        mPromocodeDialog.setCanceledOnTouchOutside(false);
        TextInputEditText edtPromocode = mPromocodeDialog.findViewById(R.id.edtPromocode);
        TextInputLayout tilEnterPromocode = mPromocodeDialog.findViewById(R.id.tilEnterPromocode);
        Button btnApplyCode = mPromocodeDialog.findViewById(R.id.btnApplyPromocode);
        CardView cv_close = mPromocodeDialog.findViewById(R.id.cv_close);
        ProgressBar mPromocodeSpin = mPromocodeDialog.findViewById(R.id.progressSpinKitView);


        btnApplyCode.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (edtPromocode.getText().toString().isEmpty()) {
                    tilEnterPromocode.setError(getResources().getString(R.string.enter_valid_code));
                } else {
                    try {
                        if (mActivityDeliveryDetailBinding.tvCoupon.getText().toString().equalsIgnoreCase(getResources().getString(R.string.add_coupon))) {
                            requestApplyPromoCode(edtPromocode.getText().toString().trim(), mPromocodeSpin);
                        } else {

                        }

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            }
        });

        cv_close.setOnClickListener(v->{
            mPromocodeDialog.dismiss();
        });
        mPromocodeDialog.show();

    }


    public void requestApplyLoyalty(String argUsabilityLimit) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        System.out.println("Rahul : DeliveryDetail : requestApplyLoyalty : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
        JSONObject mParam = new JSONObject();
        mParam.put("redeem_amount", Double.parseDouble(argUsabilityLimit));
        mParam.put("rule_id", rule_id);
        if (!paramCouponcode.isEmpty()) {
            mParam.put("coupon_code", paramCouponcode);
        }

        mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        System.out.println("Rahul : DeliveryDetail : requestApplyLoyalty : mParam : " + mParam);

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.APPLY_COUPON, mParam,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                        System.out.println("Rahul : DeliveryDetail : requestApplyLoyalty : mJsonObject : " + mJsonObject);
                        try {
                            CartSummaryModel mCartSummaryModel = mGson.fromJson(response.toString(), CartSummaryModel.class);
                            if (mCartSummaryModel.getStatus().equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {

                                if (argUsabilityLimit.equals("0")) {
                                    mActivityDeliveryDetailBinding.llLoyaltyPoints.setVisibility(View.GONE);
                                    mActivityDeliveryDetailBinding.tvAppliedLoyaltyAmount.setText(Constants.VARIABLES.CURRENT_CURRENCY + "0.00");
                                } else {
                                    mActivityDeliveryDetailBinding.llLoyaltyPoints.setVisibility(View.VISIBLE);
                                    mActivityDeliveryDetailBinding.tvAppliedLoyaltyAmount.setText(Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mCartSummaryModel.getData().getOrderamountdetails().get(0).getApplied_loyalty_amount())));
                                    //  mActivityDeliveryDetailBinding.tvLoyaltyUsabilityDetail.setText("You can use upto " + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mCartSummaryModel.getData().getOrderamountdetails().get(0).getApplied_loyalty_amount())) + " for this order");

                                }
                                mActivityDeliveryDetailBinding.tvSubtotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mCartSummaryModel.getData().getOrderamountdetails().get(0).getSubTotal())));
                                mActivityDeliveryDetailBinding.tvTotalSumPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mCartSummaryModel.getData().getOrderamountdetails().get(0).getGrandTotal())));
                                // mActivityDeliveryDetailBinding.tvPlaceOrderPrice.setText(mActivityDeliveryDetailBinding.tvTotalSumPrice.getText().toString());
                                // mActivityDeliveryDetailBinding.tvDiscount.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mCartSummaryModel.getData().getOrderamountdetails().get(0).getCartDiscount())));
                                mActivityDeliveryDetailBinding.tvDeliveryCharges.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mCartSummaryModel.getData().getOrderamountdetails().get(0).getShippingCharge())));
                                mActivityDeliveryDetailBinding.tvEstimatedTax.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mCartSummaryModel.getData().getOrderamountdetails().get(0).getTaxAmount())));
                            }

                        } catch (Exception e) {
                            e.printStackTrace();
                        }


                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());

                return headers;
            }


        };


        // Adding request to request queue
        queue.add(jsonObjReq);
    }

    public void requestApplyPromoCode(String argCouponCode, ProgressBar mSpinKitView) throws JSONException {
        if (Constants.isInternetConnected(DeliveryDetail.this)) {
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            System.out.println("Rahul : MyCart : requestApplyPromoCode : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
            JSONObject mParam = new JSONObject();
            mParam.put("coupon_code", argCouponCode);
        /*if (mActivityDeliveryDetailBinding.cbApplyWallet.isChecked()) {
            mParam.put("redeem_amount", Double.parseDouble(usability_limit));
            mParam.put("rule_id", rule_id);
        }*/
            mSpinKitView.setVisibility(View.VISIBLE);
            System.out.println("Rahul : MyCart : requestApplyPromoCode : mParam : " + mParam);

            JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                    Constants.BASE_URL + Constants.API_METHODS.APPLY_COUPON, mParam,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            mSpinKitView.setVisibility(View.GONE);
                            System.out.println("Rahul : MyCart : requestApplyPromoCode : mJsonObject : " + mJsonObject);
                            try {
                                if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {

                                    JSONArray mAppliedCouponDetail = response.getJSONObject("data").getJSONArray("applied_coupon");
                                    JSONObject mAppliedCouponObject = mAppliedCouponDetail.getJSONObject(0);
                                    JSONObject mOrderAmountDetails = response.getJSONObject("data").getJSONArray("orderamountdetails").getJSONObject(0);
                                    System.out.println("Rahul : MyCart : requestApplyPromoCode : mAppliedCouponDetail :" + mAppliedCouponDetail.toString());
                                    mActivityDeliveryDetailBinding.tvCoupon.setText(paramCouponcode);


                                    if (mAppliedCouponObject.getInt("status") == 1) {
                                        mActivityDeliveryDetailBinding.cvClose.setVisibility(View.VISIBLE);
                                        // Toast.makeText(getApplicationContext(), mAppliedCouponObject.getString("message"), Toast.LENGTH_LONG).show();
                                        paramCouponcode = argCouponCode;
                                        mPromocodeDialog.dismiss();
                                        mActivityDeliveryDetailBinding.tvSubtotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("sub_total"))));
                                        mActivityDeliveryDetailBinding.tvTotalSumPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("grand_total"))));
                                        mActivityDeliveryDetailBinding.llDiscount.setVisibility(View.VISIBLE);
                                        mActivityDeliveryDetailBinding.llCoupon.setVisibility(View.GONE);
                                        //mActivityDeliveryDetailBinding.tvPlaceOrderPrice.setText(mActivityDeliveryDetailBinding.tvTotalSumPrice.getText().toString());
                                        mActivityDeliveryDetailBinding.tvDiscount.setText("- " + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mAppliedCouponObject.getString("amount"))));

                                        mActivityDeliveryDetailBinding.tvDiscount.setTextColor(getApplicationContext().getResources().getColor(R.color.green_dark_new));
                                        mActivityDeliveryDetailBinding.tvEstimatedTax.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("tax_amount"))));
                                        //    mActivityDeliveryDetailBinding.txtApplyPromoCode.setText("You have saved " + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mAppliedCouponObject.getString("amount"))));

                                    /*if (mOrderAmountDetails.getString("applied_loyalty_amount") != null) {
                                        mActivityDeliveryDetailBinding.llLoyaltyPoints.setVisibility(View.VISIBLE);
                                        mActivityDeliveryDetailBinding.tvAppliedLoyaltyAmount.setText(Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("applied_loyalty_amount"))));
                                        mActivityDeliveryDetailBinding.tvLoyaltyUsabilityDetail.setText("You can use upto " + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("applied_loyalty_amount"))) + " for this order");

                                    } else {
                                        mActivityDeliveryDetailBinding.llLoyaltyPoints.setVisibility(View.GONE);
                                        mActivityDeliveryDetailBinding.tvAppliedLoyaltyAmount.setText(Constants.VARIABLES.CURRENT_CURRENCY + " 0.00");

                                    }*/


                                    } else {
                                        Constants.showToastInMiddle(getApplicationContext(), mAppliedCouponObject.getString("message"));
                                        mActivityDeliveryDetailBinding.cvClose.setVisibility(View.GONE);
                                        mActivityDeliveryDetailBinding.llDiscount.setVisibility(View.GONE);
                                        mActivityDeliveryDetailBinding.llCoupon.setVisibility(View.VISIBLE);
                                      //  mActivityDeliveryDetailBinding.txtApplyPromoCode.setText(getResources().getString(R.string.my_cart_apc));
                                        mActivityDeliveryDetailBinding.tvCoupon.setText(getResources().getString(R.string.add_coupon));
                                        mActivityDeliveryDetailBinding.ivCoupon.setBackground(getResources().getDrawable(R.drawable.tick_black));
                                        //Toast.makeText(getApplicationContext(), mAppliedCouponObject.getString("message"), Toast.LENGTH_LONG).show();
                                    }

                                } else {
                                    mActivityDeliveryDetailBinding.llCoupon.setVisibility(View.VISIBLE);
                                    mActivityDeliveryDetailBinding.cvClose.setVisibility(View.GONE);
                                 //   mActivityDeliveryDetailBinding.txtApplyPromoCode.setText(getResources().getString(R.string.my_cart_apc));
                                    mActivityDeliveryDetailBinding.tvCoupon.setText(getResources().getString(R.string.add_coupon));
                                    mActivityDeliveryDetailBinding.ivCoupon.setBackground(getResources().getDrawable(R.drawable.tick_black));
                                    Constants.showToastInMiddle(getApplicationContext(), getString(R.string.something_went_wrong));

                                    //Toast.makeText(getApplicationContext(), getString(R.string.something_went_wrong), Toast.LENGTH_LONG).show();
                                }


                            } catch (JSONException e) {
                                e.printStackTrace();
                            }


                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {
                    mSpinKitView.setVisibility(View.GONE);
                }
            }) {
                @Override
                public Map<String, String> getHeaders() throws AuthFailureError {
                    HashMap<String, String> headers = new HashMap<String, String>();
                    headers.put("Content-Type", "application/json");
                    headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                    headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());

                    return headers;
                }


            };


            // Adding request to request queue
            queue.add(jsonObjReq);
        } else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }
    public void requestRemoveApplyPromoCode(String argCouponCode) throws JSONException {
        if (Constants.isInternetConnected(DeliveryDetail.this)) {
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            System.out.println("Rahul : MyCart : requestApplyPromoCode : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
            JSONObject mParam = new JSONObject();

        /*if (mActivityDeliveryDetailBinding.llLoyaltyPoints.getVisibility() == View.VISIBLE) {
            mParam.put("redeem_amount", Double.parseDouble(mActivityDeliveryDetailBinding.tvAppliedLoyaltyAmount.getText().toString().trim().replace(Constants.VARIABLES.CURRENT_CURRENCY, "")));
            mParam.put("rule_id", rule_id);
        }*/
            mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            System.out.println("Rahul : MyCart : requestApplyPromoCode : mParam : " + mParam);

            JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                    Constants.BASE_URL + Constants.API_METHODS.APPLY_COUPON, mParam,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                            System.out.println("Rahul : MyCart : requestApplyPromoCode : mJsonObject : " + mJsonObject);
                            try {
                                if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                    paramCouponcode = argCouponCode;
                                    JSONArray mAppliedCouponDetail = response.getJSONObject("data").getJSONArray("applied_coupon");
                                    // JSONObject mAppliedCouponObject = mAppliedCouponDetail.getJSONObject(0);
                                    JSONObject mOrderAmountDetails = response.getJSONObject("data").getJSONArray("orderamountdetails").getJSONObject(0);
                                    System.out.println("Rahul : MyCart : requestApplyPromoCode : mAppliedCouponDetail :" + mAppliedCouponDetail.toString());

                                    // Toast.makeText(getApplicationContext(), mAppliedCouponObject.getString("message"), Toast.LENGTH_LONG).show();

                                    mPromocodeDialog.dismiss();
                                    mActivityDeliveryDetailBinding.tvSubtotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("sub_total"))));
                                    mActivityDeliveryDetailBinding.tvTotalSumPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("grand_total"))));
                                    //mActivityDeliveryDetailBinding.tvPlaceOrderPrice.setText(mActivityDeliveryDetailBinding.tvTotalSumPrice.getText().toString());
                                    mActivityDeliveryDetailBinding.tvDiscount.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " 0.0");
                                    mActivityDeliveryDetailBinding.llDiscount.setVisibility(View.GONE);
                                    mActivityDeliveryDetailBinding.llCoupon.setVisibility(View.VISIBLE);
                                    //mActivityDeliveryDetailBinding.tvDiscount.setTextColor(getApplicationContext().getResources().getColor(R.color.app_red_clr));
                                    mActivityDeliveryDetailBinding.tvEstimatedTax.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("tax_amount"))));
                                 //   mActivityDeliveryDetailBinding.txtApplyPromoCode.setText("Apply Promo Code");
                                    mActivityDeliveryDetailBinding.tvCoupon.setText("Add Coupon");
                                    mActivityDeliveryDetailBinding.ivCoupon.setBackground(getResources().getDrawable(R.drawable.tick_black));
                                /*if (mOrderAmountDetails.getString("applied_loyalty_amount") != null) {
                                    mActivityDeliveryDetailBinding.llLoyaltyPoints.setVisibility(View.VISIBLE);
                                    mActivityDeliveryDetailBinding.tvAppliedLoyaltyAmount.setText(Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("applied_loyalty_amount"))));
                                    mActivityDeliveryDetailBinding.tvLoyaltyUsabilityDetail.setText("You can use upto " + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("applied_loyalty_amount"))) + " for this order");

                                } else {
                                    mActivityDeliveryDetailBinding.llLoyaltyPoints.setVisibility(View.GONE);
                                    mActivityDeliveryDetailBinding.tvAppliedLoyaltyAmount.setText(Constants.VARIABLES.CURRENT_CURRENCY + " 0.00");

                                }*/


                                } else {
                                    paramCouponcode = "";
                                    Constants.showToastInMiddle(getApplicationContext(), getString(R.string.something_went_wrong));
                                    mActivityDeliveryDetailBinding.llCoupon.setVisibility(View.GONE);
                                    // Toast.makeText(getApplicationContext(), getString(R.string.something_went_wrong), Toast.LENGTH_LONG).show();
                                }


                            } catch (JSONException e) {
                                e.printStackTrace();
                            }


                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {
                    mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                }
            }) {
                @Override
                public Map<String, String> getHeaders() throws AuthFailureError {
                    HashMap<String, String> headers = new HashMap<String, String>();
                    headers.put("Content-Type", "application/json");
                    headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                    headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());

                    return headers;
                }


            };


            // Adding request to request queue
            queue.add(jsonObjReq);
        } else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }

    public void requestCheckLoyaltyBalance() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        System.out.println("Rahul : DeliveryDetail : requestCheckLoyaltyBalance : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
        JSONObject mParam = new JSONObject();
        mParam.put("warehouse_id", mSharedPreferenceManager.getWarehouseId());
        mParam.put("address_id", address_book_id);
        mParam.put("coupon_code", paramCouponcode);
        System.out.println("Rahul : DeliveryDetail : requestCheckLoyaltyBalance : mParam : " + mParam);

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.CART_SUMMARY, mParam,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                        System.out.println("Rahul : DeliveryDetail : requestCheckLoyaltyBalance : mJsonObject : " + mJsonObject);
                        try {
                            CartSummaryModel mCartSummaryModel = mGson.fromJson(response.toString(), CartSummaryModel.class);
                            if (mCartSummaryModel.getStatus().equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                if (mCartSummaryModel.getRemainLoyalty().equals("0")) {
                                   /* mActivityDeliveryDetailBinding.tvLoyaltyUsabilityDetail.setVisibility(View.GONE);
                                    mActivityDeliveryDetailBinding.tvWalletPoints.setText("Wallet Balance - " + Constants.VARIABLES.CURRENT_CURRENCY + " 0.00");
                                    mActivityDeliveryDetailBinding.cbApplyWallet.setVisibility(View.GONE);*/

                                } else {
                                  /*  mActivityDeliveryDetailBinding.tvLoyaltyUsabilityDetail.setVisibility(View.VISIBLE);
                                    mActivityDeliveryDetailBinding.cbApplyWallet.setVisibility(View.VISIBLE);

                                    mActivityDeliveryDetailBinding.tvWalletPoints.setText("Wallet Balance - " + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mCartSummaryModel.getRemainLoyalty())));
                                    mActivityDeliveryDetailBinding.tvLoyaltyUsabilityDetail.setText("You can use upto " + Constants.VARIABLES.CURRENT_CURRENCY + " " + mCartSummaryModel.getUsableLoyalty() + " for this order");
*/
                                    rule_id = String.valueOf(mCartSummaryModel.getRuleId());
                                    usability_limit = String.valueOf(mCartSummaryModel.getUsableLoyalty());

                                }

                                ArrayList<String> productNameList = new ArrayList<>();
                                ArrayList<String> productId = new ArrayList<>();

                                for (int i = 0; i < mCartSummaryModel.getData().getCartdetails().size(); i++) {

                                    productNameList.add(mCartSummaryModel.getData().getCartdetails().get(i).getName() + ",");
                                    productId.add(mCartSummaryModel.getData().getCartdetails().get(i).getId() + ",");

                                }
                                productIdList = productId.toString();
                                productNameLists = productNameList.toString();

                                mActivityDeliveryDetailBinding.tvSubtotal.setText(Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mCartSummaryModel.getData().getOrderamountdetails().get(0).getSubTotal())));
                                mActivityDeliveryDetailBinding.tvDeliveryCharges.setText(Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mCartSummaryModel.getData().getOrderamountdetails().get(0).getShippingCharge())));
                                mActivityDeliveryDetailBinding.tvTotalSumPrice.setText(Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mCartSummaryModel.getData().getOrderamountdetails().get(0).getGrandTotal())));
                                // mActivityDeliveryDetailBinding.tvPlaceOrderPrice.setText(Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mCartSummaryModel.getData().getOrderamountdetails().get(0).getGrandTotal())));
                                if (paramCouponcode != null && !paramCouponcode.isEmpty()) {
                                    mActivityDeliveryDetailBinding.llDiscount.setVisibility(View.VISIBLE);
                                    //  mActivityDeliveryDetailBinding.llCoupon.setVisibility(View.GONE);
                                    JSONArray mAppliedCouponDetail = response.getJSONObject("data").getJSONArray("applied_coupon");
                                    JSONObject mAppliedCouponObject = mAppliedCouponDetail.getJSONObject(0);
                                    mActivityDeliveryDetailBinding.tvDiscount.setText("-" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mAppliedCouponObject.getString("amount"))));
                                    mActivityDeliveryDetailBinding.tvDiscount.setTextColor(getApplicationContext().getResources().getColor(R.color.green_dark_new));
                                } else {
                                    mActivityDeliveryDetailBinding.llDiscount.setVisibility(View.GONE);
                                    //  mActivityDeliveryDetailBinding.llCoupon.setVisibility(View.VISIBLE);
                                }
                            }

                        } catch (Exception e) {
                            e.printStackTrace();
                            System.out.println("Rahul : DeliveryDetail : requestCheckLoyaltyBalance : Exception : " + e);
                        }


                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : DeliveryDetail : requestCheckLoyaltyBalance : VolleyError : " + error);

            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());

                return headers;
            }


        };


        // Adding request to request queue
        queue.add(jsonObjReq);
    }
 /*    intent.putExtra("latitude", lat);
                                        intent.putExtra("longitude", lng);*/

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        System.out.println("Rahul : DeliveryDetail : onActivityResult : 1 : ");
        if (requestCode == 1) {
            System.out.println("Rahul : DeliveryDetail : onActivityResult : 2 : ");
            if (data != null) {
                addressSelected = "selected";
                System.out.println("Rahul : DeliveryDetail : onActivityResult : selected_name : " + data.getStringExtra("selected_name"));
                String name = data.getStringExtra("selected_name");
                String mobile = data.getStringExtra("selected_mobile");
                String address = data.getStringExtra("selected_address");
                address_book_id = data.getStringExtra("selected_address_book_id");

                String lat = data.getStringExtra("latitude");
                String lng = data.getStringExtra("longitude");
                Constants.log(lat + "deliver" + lng);
                if (lat != null && !lat.isEmpty() && lng != null && !lng.isEmpty()) {
                    mSharedPreferenceManager.storeLatitude(lat);
                    mSharedPreferenceManager.storeLongitude(lng);
                }
                //   mSharedPreferenceManager.storeSelectedAddressId(address_book_id);
                if (name != null && !name.isEmpty()) {


                    mActivityDeliveryDetailBinding.tvName.setText(name);
                    mActivityDeliveryDetailBinding.tvMobileNumber.setText(mobile);
                    mActivityDeliveryDetailBinding.tvAddress.setText(address);


                    mActivityDeliveryDetailBinding.nsvDeliveryDetail.setVisibility(View.VISIBLE);
                }
            } else {

                if (address_book_id != null && !address_book_id.isEmpty()) {

                } else {
                    finish();
                }
            }
        }
    }


    public void requestSelectAddress(String argAddrerssId) throws JSONException {
        if (Constants.isInternetConnected(DeliveryDetail.this)) {
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

            JSONObject mjsonObj = new JSONObject();
            mjsonObj.put("address_id", argAddrerssId);

            System.out.println("Rahul : MyAddresses : requestDeleteAddress : token : " + mSharedPreferenceManager.getUserProfileDetail("token") + "   " + mjsonObj.toString());
            mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.VISIBLE);
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
                                        requestSaveOrder();

                                    /*new MaterialDialog.Builder(DeliveryDetail.this)
                                            .title("Note")
                                            .content("Dear customer, please note that for meats, vegetables, and fruits, the final/total price may be different than what is currently shown. This is due to weight variations in the products. Thank you for your understanding.")
                                            .positiveText("Okay")
                                            .positiveColor(ContextCompat.getColor(DeliveryDetail.this, R.color.app_green_clr))
                                            // .negativeText(getResources().getString(R.string.dialogPositiveButtonText_cancel))
                                            // .negativeColor(ContextCompat.getColor(this, R.color.selectIconColor))
                                            .onPositive((dialog, which) -> {
                                                try {
                                                    requestSaveOrder();
                                                } catch (JSONException e) {
                                                    e.printStackTrace();
                                                }

                                            })
                                            *//* .onNegative((dialog, which) -> {
                                                 dialog.dismiss();
                                             })*//*.show();*/

                                    } else {


                                        new AlertDialog.Builder(DeliveryDetail.this)
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


                                } else {

                                    //  mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                                    Toast.makeText(getApplicationContext(), getResources().getString(R.string.no_address_found), Toast.LENGTH_LONG).show();
                                }

                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                            mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);

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
            Constants.setSnackBar(DeliveryDetail.this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }


    public void requestPaymentMethods() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.VISIBLE);

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.PAYMENT_METHODS, null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Log.d("payment Option", response.toString());
                        Gson mGson = new Gson();
                        mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                        PaymentMethodModel mPaymentMethodModel = mGson.fromJson(response.toString(), PaymentMethodModel.class);

                        mApiStatusList.clear();
                        mApiStatusList.addAll(mPaymentMethodModel.getApiStatus());
                        setPaymentMethodRecyclerView();
                      //  mPaymentMethodTypesAdapter.notifyDataSetChanged();

                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                System.out.println("Rahul : PaymentOptionsAvailable : onErrorResponse : error : " + error);
                mActivityDeliveryDetailBinding.progressSpinKitView.setVisibility(View.GONE);


            }
        }) {
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

    @Override
    public void selectPaymentMethod(String argType, String paymentgateway_type_id, String type_id, String type_name) {
        //  mPaymentMethodTypesAdapter.notifyDataSetChanged();
        this.paymentgateway_type_id = paymentgateway_type_id;
        this.type_id = type_id;
        this.type_name = type_name;
        Log.d("Selected payment Type", type_name);
        switch (argType) {
            case "cash":
                isWhichPaymentType = "cash";
                si_ref_no="";
                mActivityDeliveryDetailBinding.rvPaymentCardList.setVisibility(View.GONE);
                mActivityDeliveryDetailBinding.cvBtnAddNewCard.setVisibility(View.GONE);
                mActivityDeliveryDetailBinding.cvCardView.setVisibility(View.GONE);
                mActivityDeliveryDetailBinding.btnChangeCard.setVisibility(View.GONE);
                break;
            case "card":
                isWhichPaymentType = "card";
              //  si_ref_no="";
                mActivityDeliveryDetailBinding.rvPaymentCardList.setVisibility(View.GONE);
                mActivityDeliveryDetailBinding.btnPay.setText("Next");
                if(mCardList.size()>0) {
                    mActivityDeliveryDetailBinding.btnChangeCard.setVisibility(View.VISIBLE);
                    mActivityDeliveryDetailBinding.cvCardView.setVisibility(View.VISIBLE);
                  //  setCardPaymentListRecyclerView();
                }else {
                    mActivityDeliveryDetailBinding.cvCardView.setVisibility(View.GONE);
                    mActivityDeliveryDetailBinding.btnChangeCard.setVisibility(View.GONE);
                }


                break;
            case "card_on_delivery":
                isWhichPaymentType = "card_on_delivery";
                si_ref_no="";
                mActivityDeliveryDetailBinding.rvPaymentCardList.setVisibility(View.GONE);
                mActivityDeliveryDetailBinding.cvBtnAddNewCard.setVisibility(View.GONE);
                mActivityDeliveryDetailBinding.cvCardView.setVisibility(View.GONE);
                mActivityDeliveryDetailBinding.btnChangeCard.setVisibility(View.GONE);
                break;

        }
    }


    @Override
    protected void onResume() {
        super.onResume();
        String modelState = CustomModel.getInstance().getState();
        System.out.println("Rahul : PaymentOptionsAvailable : onResume : modelState : " + modelState);
        Constants.VARIABLES.CURRENT_CURRENCY = mSharedPreferenceManager.getCurrentCurrency();
        SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        try {
            if ((addressSelected != null && !addressSelected.isEmpty()) || (mSharedPreferenceManager.getSelectedAddressId() != null && !mSharedPreferenceManager.getSelectedAddressId().isEmpty())) {
                requestMyAddresses();
            } else {
                requestCheckDeliveryAddresses();

            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }

    @Override
    protected void onRestart() {
        super.onRestart();
        String modelState = CustomModel.getInstance().getState();
        System.out.println("Rahul : PaymentOptionsAvailable : onResume : onRestart : " + modelState);
    }


    private void setCCAvenueInitialDetails() {
        String access_code = "AVZO03HA32BC46OZCB";//live
       String merchant_id = "46319";//live
        //String access_code = "AVCG03HF47CJ43GCJC";//dev
      // String merchant_id = "43366";//dev*/


        MerchantDetails m = new MerchantDetails();
        //   m.setAccess_code("AVUP03GL28CI81PUIC");//old
        //  m.setAccess_code("AVCG03HF47CJ43GCJC");
        m.setAccess_code(access_code);
        // m.setMerchant_id("45990");//Old
        //m.setMerchant_id("43366");
        m.setMerchant_id(merchant_id);

        m.setCurrency(Constants.VARIABLES.CURRENT_CURRENCY);
        // m.setAmount(mTotalAmount);
        m.setAmount("1.00");
        m.setRedirect_url("https://www.gogrocery.ae/api/front/v1/payment-res-si/");//Live
        m.setCancel_url("https://www.gogrocery.ae/api/front/v1/payment-res-si/");//Live
          //m.setRsa_url("https://www.gogrocery.ae/api/front/v1/get-rsa/");

          m.setRsa_url("https://www.gogrocery.ae/api/front/v1/get-rsa-si/?order_id=" + cust_orders_id);

//        http://15.185.126.44:8062/api/front/v1/
        //  m.setRedirect_url("http://15.185.126.44:8062/api/front/v1/payment-res/");
      /*  m.setRedirect_url("http://15.185.126.44:8062/api/front/v1/payment-res-demo/");
        m.setCancel_url("http://15.185.126.44:8062/api/front/v1/payment-res-demo/");
        m.setRsa_url("http://15.185.126.44:8062/api/front/v1/get-rsa-demo/?order_id=" + cust_orders_id);*/
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

        Intent i = new Intent(DeliveryDetail.this, PaymentOptions.class);
        //Intent i =new Intent(MainActivity.this,PaymentOptions.class);
        // Intent i =new Intent(MainActivity.this,PaymentDetails.class);
        i.putExtra("merchant", m);
        i.putExtra("billing", b);
        i.putExtra("shipping", s);
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


    @Override
    public void stateChanged() {
        String modelState = CustomModel.getInstance().getState();
        System.out.println("Rahul : PaymentOptionsAvailable : stateChanged : modelState : " + modelState);
        try {
            JSONObject mJsonObject = new JSONObject(modelState);

            if (mJsonObject.getString("status_message").equalsIgnoreCase("Approved")) {

                Intent orderSuccess = new Intent(DeliveryDetail.this, OrderSuccess.class);
                orderSuccess.putExtra("status", "Success");
                orderSuccess.putExtra("order_id", OrderId);
                orderSuccess.putExtra("order_summary", order_summary.toString());
                orderSuccess.putExtra("delivery_address", delivery_address.toString());
                startActivity(orderSuccess);

                Bundle params = new Bundle();
                params.putString("payment_method_name", type_name);
                params.putString("delivery_address", delivery_address.toString());
                params.putString("order_id", OrderId);
                params.putString("OrderFrom", "Android");
                params.putString("order_summary", order_summary.toString());
                mFirebaseAnalytics.logEvent(FirebaseAnalytics.Event.PURCHASE, params);
                logger.logEvent("purchase", params);
                finish();
            } else {
                Intent orderSuccess = new Intent(DeliveryDetail.this, OrderSuccess.class);
                orderSuccess.putExtra("status", "Failure");
                orderSuccess.putExtra("order_id", OrderId);
                orderSuccess.putExtra("order_summary", order_summary.toString());
                orderSuccess.putExtra("delivery_address", delivery_address.toString());
                startActivity(orderSuccess);
                Constants.showToastInMiddle(getApplicationContext(), mJsonObject.getString("status_message"));
                Bundle params = new Bundle();
                params.putString("payment_method_name", type_name);
                params.putString("delivery_address", delivery_address.toString());
                params.putString("order_id", OrderId);
                params.putString("OrderFrom", "Android");
                params.putString("order_summary", order_summary.toString());
                mFirebaseAnalytics.logEvent("payment_failed", params);
                logger.logEvent("payment_failed", params);
            }
        } catch (JSONException e) {
            e.printStackTrace();

            Intent orderSuccess = new Intent(DeliveryDetail.this, OrderSuccess.class);
            orderSuccess.putExtra("status", "Failure");
            orderSuccess.putExtra("order_id", OrderId);
            orderSuccess.putExtra("order_summary", String.valueOf(order_summary));
            orderSuccess.putExtra("delivery_address", String.valueOf(delivery_address));
            startActivity(orderSuccess);
            Constants.showToastInMiddle(getApplicationContext(), modelState);

            Bundle params = new Bundle();
            params.putString("payment_method_name", type_name);
            params.putString("delivery_address",String.valueOf( delivery_address));
            params.putString("order_id", OrderId);
            params.putString("OrderFrom", "Android");
            params.putString("order_summary", String.valueOf(order_summary.toString()));
            mFirebaseAnalytics.logEvent("payment_failed", params);
            logger.logEvent("payment_failed", params);
        }

        //Toast.makeText(getApplicationContext(),modelState,Toast.LENGTH_SHORT).show();
        //Intent i =new Intent(PaymentOptionsAvailable.class,)
    }


    private void setPassingParam() {
        try {
            order_summary = new JSONObject();
            delivery_address = new JSONObject();

            order_summary.put("subtotal", mActivityDeliveryDetailBinding.tvSubtotal.getText().toString());
            order_summary.put("discount", mActivityDeliveryDetailBinding.tvDiscount.getText().toString());
            //  order_summary.put("loyalty_amount", mActivityDeliveryDetailBinding.tvAppliedLoyaltyAmount.getText().toString());
            order_summary.put("delivery", mActivityDeliveryDetailBinding.tvDeliveryCharges.getText().toString());
            order_summary.put("tax", mActivityDeliveryDetailBinding.tvEstimatedTax.getText().toString());
            order_summary.put("final_total", mActivityDeliveryDetailBinding.tvTotalSumPrice.getText().toString());
            if (mActivityDeliveryDetailBinding.tvAppliedLoyaltyAmount.getText().toString().contains("0.00")) {
                order_summary.put("loyalty_amount", "0.00");
            } else {
                order_summary.put("loyalty_amount", mActivityDeliveryDetailBinding.tvAppliedLoyaltyAmount.getText().toString());
            }

            if (mActivityDeliveryDetailBinding.tvDiscount.getText().toString().equals("AED 0.00")) {
                order_summary.put("coupon_discount", "0.00");
            } else if (mActivityDeliveryDetailBinding.tvDiscount.getText().toString().equals("AED 0.0")) {
                order_summary.put("coupon_discount", "0.00");
            } else if (mActivityDeliveryDetailBinding.tvDiscount.getText().toString().equals("AED 0")) {
                order_summary.put("coupon_discount", "0.00");
            } else {
                order_summary.put("coupon_discount", mActivityDeliveryDetailBinding.tvDiscount.getText().toString());
            }

            delivery_address.put("name", mActivityDeliveryDetailBinding.tvName.getText().toString());
            delivery_address.put("address", mActivityDeliveryDetailBinding.tvAddress.getText().toString());
            delivery_address.put("number", mActivityDeliveryDetailBinding.tvMobileNumber.getText().toString());
        } catch (JSONException e) {

        }
    }


    private void showNotMatchAnyAddressPopup() {
        new MaterialDialog.Builder(this)
                .title(getResources().getString(R.string.no_related_address_found_for_this_area_from_your_address))
                .content(getResources().getString(R.string.you_can_either_choose_any_address_from_the_list_or_you_can_add_new_address))
                .positiveText(getResources().getString(R.string.add_new_address))
                .canceledOnTouchOutside(false)
                .cancelable(false)

                .positiveColor(ContextCompat.getColor(this, R.color.grey_new))
                .negativeText(getResources().getString(R.string.choose_one_address))
                .negativeColor(ContextCompat.getColor(this, R.color.grey_new))
                .onPositive((dialog, which) -> {
                    Intent ivPinLocation = new Intent(DeliveryDetail.this, AddNewAddress.class);
                    ivPinLocation.putExtra("from", "");
                    startActivityForResult(ivPinLocation, 1);
                    dialog.dismiss();
                })
                .onNegative((dialog, which) -> {
                    Intent btnChangeAddAddresses = new Intent(DeliveryDetail.this, MyAddresses.class);
                    btnChangeAddAddresses.putExtra("from", "Delivery_Detail");
                    startActivityForResult(btnChangeAddAddresses, 1);
                    dialog.dismiss();
                }).show();
    }

    private void showAddAddressPopup() {
        new MaterialDialog.Builder(this)
                .title(getResources().getString(R.string.no_related_address_found_for_this_area_from_your_address))
                .content(getResources().getString(R.string.please_add_new_address_so_that_we_can_deliver_product_at_your_door_step))
                .positiveText(getResources().getString(R.string.add_new_address))
                .cancelable(false)
                .positiveColor(ContextCompat.getColor(this, R.color.grey_new))
                .canceledOnTouchOutside(false)
                /* .negativeText("Choose One Address")
                 .negativeColor(ContextCompat.getColor(this, R.color.grey_new))*/
                .onPositive((dialog, which) -> {
                    Intent ivPinLocation = new Intent(DeliveryDetail.this, AddNewAddress.class);
                    ivPinLocation.putExtra("from", "");
                    startActivityForResult(ivPinLocation, 1);
                    dialog.dismiss();
                })
                /*    .onNegative((dialog, which) -> {
                        Intent btnChangeAddAddresses = new Intent(DeliveryDetail.this, MyAddresses.class);
                        btnChangeAddAddresses.putExtra("from", "Delivery_Detail");
                        startActivityForResult(btnChangeAddAddresses, 1);
                        dialog.dismiss();
                    })*/.show();
    }


    private void showNotMatchDefaultAddressPopup() {
        new MaterialDialog.Builder(this)
                .title(getResources().getString(R.string.choose_a_saved_address))
                .content(getResources().getString(R.string.you_have_more_than_one_saved_address))
                .canceledOnTouchOutside(false)
                .cancelable(false)
                .positiveText(getResources().getString(R.string.ok))
                .positiveColor(ContextCompat.getColor(this, R.color.grey_new))
                /*.negativeText("Choose Address")
                .negativeColor(ContextCompat.getColor(this, R.color.grey_new))*/
                .onPositive((dialog, which) -> {
                    Intent btnChangeAddAddresses = new Intent(DeliveryDetail.this, MyAddresses.class);
                    btnChangeAddAddresses.putExtra("from", "Delivery_Detail");
                    startActivityForResult(btnChangeAddAddresses, 1);
                    dialog.dismiss();
                })
                /*.onNegative((dialog, which) -> {
                    dialog.dismiss();
                })*/.show();
    }

    private void showOrderSummaryDialog(String totalAmount, String paymentType, String deliveryAddress) {
        orderSummaryDialog = new Dialog(this);
        orderSummaryDialog.setContentView(R.layout.order_summary_dialog);
        orderSummaryDialog.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        orderSummaryDialog.setCanceledOnTouchOutside(false);
        ImageView close = orderSummaryDialog.findViewById(R.id.ivRemove);
        TextView tvDeliveryAddress = orderSummaryDialog.findViewById(R.id.tv_deliveryAddress);
        TextView tvTotalAmount = orderSummaryDialog.findViewById(R.id.tv_grandTotal);
        TextView tvPaymentType = orderSummaryDialog.findViewById(R.id.tv_paymentType);
        Button btnOrderConfirm = orderSummaryDialog.findViewById(R.id.btnOrderConfirm);
        tvDeliveryAddress.setText(deliveryAddress);
        tvTotalAmount.setText(totalAmount);
        tvPaymentType.setText(paymentType);

        close.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                isOrderConfirm= false;
                orderSummaryDialog.dismiss();
            }
        });


        btnOrderConfirm.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    isOrderConfirm= true;
                    requestSelectAddress(address_book_id);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                orderSummaryDialog.dismiss();
            }
        });

        orderSummaryDialog.show();

    }

    @Override
    public void onBackPressed() {
        //  super.onBackPressed();
    }

    @Override
    protected void onPause() {
        if (orderSummaryDialog != null) {
            orderSummaryDialog.dismiss();
        }
        if (mChangeAddressDialog != null) {
            mChangeAddressDialog.dismiss();

        }
        super.onPause();

    }

    @Override
    protected void onDestroy() {
        if (mChangeAddressDialog != null) {
            mChangeAddressDialog.dismiss();

        }
        if (orderSummaryDialog != null) {
            orderSummaryDialog.dismiss();
        }
        super.onDestroy();
    }

    @Override
    public void onSelectedCard(String cardNo,String argSI) {

        this.si_ref_no=argSI;
    }



    private void changeCardDialog() {
        mChangeAddressDialog = new BottomSheetDialog(this, R.style.BottomSheetDialog);
        View sheetView = this.getLayoutInflater().inflate(R.layout.bottom_sheet_select_my_card, null);
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
        if (mCardList.size() > 4) {
            LinearLayout.LayoutParams layoutParams = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 1200);
            layoutParams.setMargins(0, 0, 0, 0);
            nsView.setLayoutParams(layoutParams);
        } else {
            LinearLayout.LayoutParams layoutParams = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
            layoutParams.setMargins(0, 0, 0, 0);
            nsView.setLayoutParams(layoutParams);
        }


        mRecyclerView.setAdapter(new MyCardAdapter(this, mCardList, new PaymentCardInterface() {


            @Override
            public void onSelectedCard(String cardNo,String argSI) {
                mActivityDeliveryDetailBinding.tvPreferences.setText(cardNo);
                si_ref_no=argSI;
                mChangeAddressDialog.dismiss();
            }
        },""));
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
                si_ref_no="0";
                if (si_ref_no != null && !si_ref_no.equals("")) {
                    showOrderSummaryDialog(String.valueOf(mActivityDeliveryDetailBinding.tvTotalSumPrice.getText()), getResources().getString(R.string.online_payment), String.valueOf(mActivityDeliveryDetailBinding.tvAddress.getText()));
                } else {
                    Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.please_select_any_card_from_the_list));
                }


            }
        });
        mChangeAddressDialog.show();

    }


}