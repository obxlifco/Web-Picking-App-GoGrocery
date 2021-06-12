package com.gogrocery.view;

import android.content.Intent;
import androidx.databinding.DataBindingUtil;
import android.net.Uri;
import android.os.Build;
import android.os.Handler;
import android.os.Message;

import com.gogrocery.R;
import com.google.android.material.bottomsheet.BottomSheetDialog;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
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
import com.gogrocery.Adapters.ItemsInTheOrderAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Models.OrderDetailsModel.OrderDetailsModel;
import com.gogrocery.Models.OrderDetailsModel.OrderProduct;
import com.gogrocery.databinding.ActivityMyOrdersDetailPageBinding;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.text.ParseException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MyOrdersDetailPage extends AppCompatActivity {

    private ActivityMyOrdersDetailPageBinding mActivityMyOrdersDetailPageBinding;
    private SharedPreferenceManager mSharedPreferenceManager;
    private ItemsInTheOrderAdapter mItemsInTheOrderAdapter;
    private List<OrderProduct> mOrderProductList = new ArrayList<>();
    private String order_id = "", order_detail = "", cust_orders_id = "";
    private BottomSheetDialog bottomSheetDialogReason;
    private Handler mHandler;
    public static List<Integer> mProductId = new ArrayList<>();
    public static List<Integer> mProductQuantity = new ArrayList<>();
    private int addTocartPosition = 0;
    private String deepLinkUrl = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityMyOrdersDetailPageBinding = DataBindingUtil.setContentView(this, R.layout.activity_my_orders_detail_page);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        Constants.VARIABLES.CURRENT_CURRENCY = mSharedPreferenceManager.getCurrentCurrency();
hideStatusBarColor();
        try {

            Intent intent = getIntent();
            String action = intent.getAction();
            if (intent.getData() != null) {
                Uri data = intent.getData();
                System.out.println("Rahul : PaymentOptionsAvailable : getOrderIdBundel : data : " + data);
                try {

                    requestOrderDetailsPayment(data.toString());

                } catch (JSONException e) {
                    e.printStackTrace();
                }
            } else {
                order_id = getIntent().getExtras().getString("orders_id");
                cust_orders_id = getIntent().getExtras().getString("cust_orders_id");
                order_detail = getIntent().getExtras().getString("order_detail");
                System.out.println("Rahul : MyOrdersDetailPage : order_id : " + order_id);
                System.out.println("Rahul : MyOrdersDetailPage : cust_orders_id : " + cust_orders_id);
                System.out.println("Rahul : MyOrdersDetailPage : order_detail : " + order_detail);

                requestOrderDetails(order_id);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        mActivityMyOrdersDetailPageBinding.ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

/*        if (Constants.VARIABLES.CART_COUNT > 0) {
            mActivityMyOrdersDetailPageBinding.rlBadge.setVisibility(View.VISIBLE);
            mActivityMyOrdersDetailPageBinding.badgeNotification.setText("" + Constants.VARIABLES.CART_COUNT);
        } else {
            mActivityMyOrdersDetailPageBinding.rlBadge.setVisibility(View.GONE);
        }
        mActivityMyOrdersDetailPageBinding.ivCart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent ivCart = new Intent(MyOrdersDetailPage.this, MyCart.class);
                startActivity(ivCart);
            }
        });*/


        mActivityMyOrdersDetailPageBinding.btnPayNow.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                Intent i = new Intent(MyOrdersDetailPage.this, PaymentOptionsAvailable.class);
                JSONObject order_detail_json = null;
                if (!deepLinkUrl.isEmpty()) {
                    i.putExtra("is_deep_linking", deepLinkUrl);
                    startActivity(i);
                } else {
                    i.putExtra("orders_id", order_id);
                    i.putExtra("cust_orders_id", cust_orders_id);

                    try {
                        order_detail_json = new JSONObject(order_detail);
                        if (mActivityMyOrdersDetailPageBinding.tvAppliedLoyaltyAmount.getText().toString().equals("AED 0.00")) {
                            order_detail_json.put("loyalty_amount", "0.00");
                        } else {
                            order_detail_json.put("loyalty_amount", mActivityMyOrdersDetailPageBinding.tvAppliedLoyaltyAmount.getText().toString());
                        }


                        if (mActivityMyOrdersDetailPageBinding.tvDiscount.getText().toString().equals("AED 0.00")) {
                            order_detail_json.put("coupon_discount", "0.00");
                        } else if (mActivityMyOrdersDetailPageBinding.tvDiscount.getText().toString().equals("AED 0.0")) {
                            order_detail_json.put("coupon_discount", "0.00");
                        } else if (mActivityMyOrdersDetailPageBinding.tvDiscount.getText().toString().equals("AED 0")) {
                            order_detail_json.put("coupon_discount", "0.00");
                        } else {
                            order_detail_json.put("coupon_discount", mActivityMyOrdersDetailPageBinding.tvDiscount.getText().toString());
                        }
                        order_detail_json.put("display_address", mActivityMyOrdersDetailPageBinding.tvAddress.getText().toString());
                        i.putExtra("order_detail", order_detail_json.toString());
                        startActivity(i);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }


            }
        });

        mActivityMyOrdersDetailPageBinding.btnCancel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


                bottomSheetDialogReason = new BottomSheetDialog(MyOrdersDetailPage.this);
                bottomSheetDialogReason.setContentView(R.layout.order_cancel_reason);
                Button cancel = bottomSheetDialogReason.findViewById(R.id.btnNo);
                Button submit = bottomSheetDialogReason.findViewById(R.id.btnYes);
                AutoCompleteTextView actvReason = bottomSheetDialogReason.findViewById(R.id.actvReason);
                String[] mList = {getResources().getString(R.string.wrong_product_selected),getResources().getString(R.string.wrong_price),getResources().getString(R.string.ordered_by_mistake),getResources().getString(R.string.other)};
                setDropdownReason(actvReason, mList);

                ImageView ivBack = bottomSheetDialogReason.findViewById(R.id.ivBack);
                ivBack.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        bottomSheetDialogReason.dismiss();
                    }
                });

                cancel.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        bottomSheetDialogReason.dismiss();
                    }
                });

                submit.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        try {
                            if (actvReason.getText().toString().isEmpty()) {
                                actvReason.setError(getResources().getString(R.string.please_select_any_reason));
                            } else {
                                if (!order_id.isEmpty()) {
                                    requestOrderCancel(order_id, actvReason.getText().toString());
                                }
                                bottomSheetDialogReason.dismiss();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                });

                bottomSheetDialogReason.show();

            }
        });

        mActivityMyOrdersDetailPageBinding.tvRepeatOrder.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    requestEmptyCart();
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });

        mHandler = new Handler() {
            @Override
            public void handleMessage(Message msg) {

                if (!(("" + mProductId.size()).equals("" + addTocartPosition))) {

                    System.out.println("Rahul : MyOrdersDetailPage : Message : " + msg.toString());
                    switch (msg.what) {
                        case 1:
                            try {
                                requestAddToCart(mProductId.get(addTocartPosition), mProductQuantity.get(addTocartPosition));
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                            break;
                    }
                } else {
                    mActivityMyOrdersDetailPageBinding.progressSpinKitView.setVisibility(View.GONE);
                    Intent toCart = new Intent(MyOrdersDetailPage.this, MyCart.class);
                    startActivity(toCart);
                }
            }
        };
        // ATTENTION: This was auto-generated to handle app links.

    }


    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }
    public void requestEmptyCart() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        findViewById(R.id.progressSpinKitView).setVisibility(View.VISIBLE);
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));
        mJsonObject.put("website_id", 1);

        System.out.println("Rahul : MyOrdersDetailPage : requestEmptyCart : mJsonObject : " + mJsonObject.toString());

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.EMPTY_CART, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : MyOrdersDetailPage : requestEmptyCart : response : " + response.toString());
                        try {
                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                new DatabaseHandler(getApplicationContext()).deleteAllRecord();
                                System.out.println("Rahul : MyOrdersDetailPage : requestEmptyCart : response2: " + response.toString());
                                mHandler.sendEmptyMessage(1);

                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                System.out.println("Rahul : MyOrdersDetailPage : requestEmptyCart : VolleyError : " + error.toString());
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

    private void setDropdownReason(AutoCompleteTextView mAutoCompleteTextView, String[] argVartiantName) {

        ArrayAdapter adapter = new
                ArrayAdapter(getApplicationContext(), android.R.layout.simple_list_item_1, argVartiantName);

        mAutoCompleteTextView.setAdapter(adapter);

        System.out.println("Rahul : DealsOfTheDayAdapter : setDropdownVariant : argVartiantName : " + argVartiantName.toString());
        mAutoCompleteTextView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                System.out.println("Rautocomplete : " + argVartiantName[i]);
              /*  mVehicleType = argCarTypeID[i];
                mCategoryId = argCarTypeID[i];
                mAutoCompleteTextView.setError(null);
                mPassingVehicleType = argCarType[i];*/
            }
        });


        mAutoCompleteTextView.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                mAutoCompleteTextView.setEnabled(false);
                mAutoCompleteTextView.dismissDropDown();

                System.out.println("Rautocomplete : " + argVartiantName[i]);

            }

            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {

            }
        });

       /* mAutoCompleteTextView.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
                switch (motionEvent.getAction()) {
                    case MotionEvent.ACTION_UP: {
                        //   getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_HIDDEN);

                        mAutoCompleteTextView.setEnabled(true);
                        mAutoCompleteTextView.showDropDown();
                    }
                }

                return true;
            }
        });*/
        mAutoCompleteTextView.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                if (hasFocus) {
                    // mAutoCompleteTextView.setEnabled(true);
                    mAutoCompleteTextView.showDropDown();
                }
            }
        });

        mAutoCompleteTextView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // mAutoCompleteTextView.setEnabled(true);
                mAutoCompleteTextView.showDropDown();
            }
        });


    }


    public void requestOrderDetails(String argOrderId) throws JSONException {
       mActivityMyOrdersDetailPageBinding.rlShimmer.setVisibility(View.VISIBLE);
       mActivityMyOrdersDetailPageBinding.rlShimmer.startShimmer();
        mActivityMyOrdersDetailPageBinding.nsvMyOrdersDetail.setVisibility(View.GONE);
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        mActivityMyOrdersDetailPageBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        System.out.println("Rahul : MyOrdersDetailPage : requestOrderDetails : mJsonObject : url : " + Constants.BASE_URL + Constants.API_METHODS.ORDER_DETAILS + argOrderId + "/");
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.ORDER_DETAILS + argOrderId + "/", null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        mActivityMyOrdersDetailPageBinding.rlShimmer.setVisibility(View.GONE);
                        mActivityMyOrdersDetailPageBinding.rlShimmer.stopShimmer();
                        mActivityMyOrdersDetailPageBinding.progressSpinKitView.setVisibility(View.GONE);
                        mActivityMyOrdersDetailPageBinding.nsvMyOrdersDetail.setVisibility(View.VISIBLE);
                        System.out.println("Rahul : MyOrdersDetailPage : requestOrderDetails : mJsonObject : " + response);
                        //  MyOrdersHistoryModel mMyOrdersHistoryModel = mGson.fromJson(mJsonObject.toString(), MyOrdersHistoryModel.class);
                        setPageUI(response);

                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                mActivityMyOrdersDetailPageBinding.progressSpinKitView.setVisibility(View.GONE);
                mActivityMyOrdersDetailPageBinding.rlShimmer.setVisibility(View.GONE);

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

    public void requestOrderDetailsPayment(String argEncryptedData) throws JSONException {
        if (Constants.isInternetConnected(MyOrdersDetailPage.this)) {
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            mActivityMyOrdersDetailPageBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            System.out.println("Rahul : MyOrdersDetailPage : requestOrderDetailsPayment : mJsonObject : url : https://www.gogrocery.ae/api/front/v1/order-details-payment/" + argEncryptedData.split("/place-order/")[1] + "/");

            JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                    "https://www.gogrocery.ae/api/front/v1/order-details-payment/" + argEncryptedData.split("/place-order/")[1] + "/", null,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            Gson mGson = new Gson();
                            mActivityMyOrdersDetailPageBinding.progressSpinKitView.setVisibility(View.GONE);
                            mActivityMyOrdersDetailPageBinding.nsvMyOrdersDetail.setVisibility(View.VISIBLE);
                            deepLinkUrl = "https://www.gogrocery.ae/api/front/v1/order-details-payment/" + argEncryptedData.split("/place-order/")[1] + "/";
                            // mActivityPaymentOptionsBinding.nsvMyOrdersDetail.setVisibility(View.VISIBLE);
                            System.out.println("Rahul : MyOrdersDetailPage : requestOrderDetailsPayment " + response);
                            //  MyOrdersHistoryModel mMyOrdersHistoryModel = mGson.fromJson(mJsonObject.toString(), MyOrdersHistoryModel.class);
                            //  MyOrdersFromMailModel mMyOrdersFromMailModel = mGson.fromJson(response.toString(), MyOrdersFromMailModel.class);

                        /*OrderId = mMyOrdersFromMailModel.getData().getCustomOrderId();
                        cust_orders_id = mMyOrdersFromMailModel.getData().getCustomer().getId().toString();
                        mWarehouseId = mMyOrdersFromMailModel.getData().getOrderProducts().get(0).getWarehouseId();
                        System.out.println("Rahul : MyOrdersDetailPage : requestOrderDetails : mWarehouseId : " + mWarehouseId);*/
                            try {
                                setPageUI(response);
                            } catch (Exception e) {
                                System.out.println("Rahul : MyOrdersDetailPage : requestOrderDetailsPayment Exception " + e);

                            }

                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {
                    System.out.println("Rahul : PaymentOptionsAvailable : onErrorResponse : error : " + error);
                    mActivityMyOrdersDetailPageBinding.progressSpinKitView.setVisibility(View.GONE);


                }
            }) {
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
        } else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }

    private void setPageUI(JSONObject response) {

        Gson mGson = new Gson();
        JSONObject mJsonObject = response;
        OrderDetailsModel mOrderDetailsModel = mGson.fromJson(mJsonObject.toString(), OrderDetailsModel.class);
        Constants.VARIABLES.CURRENT_CURRENCY = String.valueOf(mOrderDetailsModel.getData().getCurrencyCode());
        mActivityMyOrdersDetailPageBinding.tvOrderNumber.setText(" " + mOrderDetailsModel.getData().getCustomOrderId());
        try {
            mActivityMyOrdersDetailPageBinding.tvOrderTime.setText(" "+Constants.getFormattedDate(Constants.getMonthFormatDate(mOrderDetailsModel.getData().getTimeSlotDate()))+" "+mOrderDetailsModel.getData().getSlotEndTime());
        } catch (ParseException e) {
            e.printStackTrace();
        }
        mActivityMyOrdersDetailPageBinding.tvDateNTime.setText(mOrderDetailsModel.getData().getCreated().split("T")[0].split("-")[2] + " " +
                Constants.getSeperateValuesFromDate(mOrderDetailsModel.getData().getCreated().split("T")[0], 3) + " " +
                mOrderDetailsModel.getData().getCreated().split("T")[0].split("-")[0] + " , " + mOrderDetailsModel.getData().getCreated().split("T")[1].split(":")[0] + ":" + mOrderDetailsModel.getData().getCreated().split("T")[1].split(":")[1]
        );
        if (mOrderDetailsModel.getData().getDeliveryDate() != null) {
            mActivityMyOrdersDetailPageBinding.tvDeliveryDate.setText(mOrderDetailsModel.getData().getDeliveryDate().split("T")[0].split("-")[2] + " " +
                    Constants.getSeperateValuesFromDate(mOrderDetailsModel.getData().getCreated().split("T")[0], 3) + " " +
                    mOrderDetailsModel.getData().getCreated().split("T")[0].split("-")[0] + " , " + mOrderDetailsModel.getData().getCreated().split("T")[1].split(":")[0] + ":" + mOrderDetailsModel.getData().getCreated().split("T")[1].split(":")[1]
            );
        } else {
            mActivityMyOrdersDetailPageBinding.txtDeliveryDetail.setVisibility(View.GONE);
            mActivityMyOrdersDetailPageBinding.cvDeliveryDetail.setVisibility(View.GONE);
        }

        if(mOrderDetailsModel.getData().getCustomMsg() != null){
            mActivityMyOrdersDetailPageBinding.llSpecial.setVisibility(View.VISIBLE);
            mActivityMyOrdersDetailPageBinding.tvSpecialInstrucion.setText(mOrderDetailsModel.getData().getCustomMsg());

        }else{
            mActivityMyOrdersDetailPageBinding.llSpecial.setVisibility(View.GONE);
        }

        mActivityMyOrdersDetailPageBinding.tvName.setText(mOrderDetailsModel.getData().getBillingName());
        if(mOrderDetailsModel.getData().getDeliveryLandmark()!=null) {
            mActivityMyOrdersDetailPageBinding.tvAddress.setText(mOrderDetailsModel.getData().getDeliveryStreetAddress()+ ", "  +mOrderDetailsModel.getData().getDeliveryLandmark() + "\n" + mOrderDetailsModel.getData().getDeliveryCountryName() + mOrderDetailsModel.getData().getDeliveryState());
        }else {
            mActivityMyOrdersDetailPageBinding.tvAddress.setText(mOrderDetailsModel.getData().getDeliveryStreetAddress() + "\n" + mOrderDetailsModel.getData().getDeliveryCountryName() + mOrderDetailsModel.getData().getDeliveryState());
        }
        mActivityMyOrdersDetailPageBinding.tvMobileNumber.setText(mOrderDetailsModel.getData().getBillingPhone());


        mActivityMyOrdersDetailPageBinding.tvSubtotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderDetailsModel.getData().getNetAmount())));
        mActivityMyOrdersDetailPageBinding.tvDiscount.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderDetailsModel.getData().getCartDiscount())));
        mActivityMyOrdersDetailPageBinding.tvDeliveryCharges.setText(Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderDetailsModel.getData().getShippingCost())));
        //mActivityMyOrdersDetailPageBinding.tvEstimatedTax.setText(mBundle.getString("estimated_tax"));
        mActivityMyOrdersDetailPageBinding.tvTotalSumPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderDetailsModel.getData().getGrossAmount())));


        if (mOrderDetailsModel.getData().getPaymentMethodName().isEmpty()) {
            mActivityMyOrdersDetailPageBinding.txtPaymentmode.setVisibility(View.GONE);
            mActivityMyOrdersDetailPageBinding.tvPaymentMode.setVisibility(View.GONE);
        } else {
            mActivityMyOrdersDetailPageBinding.tvPaymentMode.setText(mOrderDetailsModel.getData().getPaymentMethodName());
        }

        mOrderProductList.addAll(mOrderDetailsModel.getData().getOrderProducts());
        setmItemsInTheOrderAdapterRecyclerView();

        if (mOrderDetailsModel.getData().getPay_wallet_amount().equals("0")) {
            mActivityMyOrdersDetailPageBinding.llLoyaltyPoints.setVisibility(View.GONE);
        } else {
            mActivityMyOrdersDetailPageBinding.llLoyaltyPoints.setVisibility(View.VISIBLE);
            mActivityMyOrdersDetailPageBinding.tvAppliedLoyaltyAmount.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderDetailsModel.getData().getPay_wallet_amount())));
        }

        switch (mOrderDetailsModel.getData().getShipment_status()) {
            case "Invoicing":
                // holder.tvPaymentStatus.setTextColor(mContext.getResources().getColor(R.color.my_orders_row_color_unpaid));
                mActivityMyOrdersDetailPageBinding.btnPayNow.setVisibility(View.GONE);
                break;
        }


        System.out.println("Rahul : MyOrdersDetailPage : getStrOrderStatus : " + mOrderDetailsModel.getData().getStrOrderStatus());
        System.out.println("Rahul : MyOrdersDetailPage : getShipment_status : " + mOrderDetailsModel.getData().getShipment_status());


        switch (mOrderDetailsModel.getData().getShipment_status()) {
            case "Invoicing":
                mItemsInTheOrderAdapter.argShipmentStatus = "Invoicing";
                mActivityMyOrdersDetailPageBinding.btnCancel.setVisibility(View.VISIBLE);
                break;
            case "Pending":
                mActivityMyOrdersDetailPageBinding.btnCancel.setVisibility(View.VISIBLE);
                break;
            case "Picking":
                mActivityMyOrdersDetailPageBinding.btnCancel.setVisibility(View.VISIBLE);
                break;
            case "":
                mActivityMyOrdersDetailPageBinding.btnCancel.setVisibility(View.VISIBLE);
                break;
        }

        try {
            switch (mOrderDetailsModel.getData().getStrOrderStatus()) {
                case "Cancelled":
                    // holder.tvPaymentStatus.setTextColor(mContext.getResources().getColor(R.color.my_orders_row_color_unpaid));
                    mActivityMyOrdersDetailPageBinding.btnCancel.setVisibility(View.GONE);
                    break;
                case "Completed":
                    // holder.tvPaymentStatus.setTextColor(mContext.getResources().getColor(R.color.my_orders_row_color_unpaid));
                    mActivityMyOrdersDetailPageBinding.tvRepeatOrder.setVisibility(View.VISIBLE);
                    break;
            }
        } catch (Exception e) {

        }
        /*mOrderDetailsModel.getData().getOrderProducts().get(0).getProduct().getId()
        mOrderDetailsModel.getData().getOrderProducts().get(0).getQuantity()*/

    }

    private void setmItemsInTheOrderAdapterRecyclerView() {
        mItemsInTheOrderAdapter = new ItemsInTheOrderAdapter(getApplicationContext(), mOrderProductList);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.VERTICAL, false);
        mActivityMyOrdersDetailPageBinding.rvItemsOrdered.setLayoutManager(mLayoutManager);
        mActivityMyOrdersDetailPageBinding.rvItemsOrdered.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        mActivityMyOrdersDetailPageBinding.rvItemsOrdered.setItemAnimator(new DefaultItemAnimator());
        mActivityMyOrdersDetailPageBinding.rvItemsOrdered.setAdapter(mItemsInTheOrderAdapter);
        mActivityMyOrdersDetailPageBinding.rvItemsOrdered.setNestedScrollingEnabled(false);
    }


    public void requestOrderCancel(String argOrderId, String argReason) throws JSONException {
        if (Constants.isInternetConnected(MyOrdersDetailPage.this)) {
            mActivityMyOrdersDetailPageBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            System.out.println("Rahul : MyOrdersDetailPage : requestOrderCancel : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
            System.out.println("Rahul : MyOrdersDetailPage : requestOrderCancel : argOrderId : " + argOrderId);
            JSONObject mParam = new JSONObject();
            mParam.put("order_id", Integer.parseInt(argOrderId));
            mParam.put("return_note", argReason);

            JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                    Constants.BASE_URL + Constants.API_METHODS.CANCEL_ORDER + argOrderId + "/", mParam,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            System.out.println("Rahul : MyOrdersDetailPage : requestOrderCancel : response : " + response);
                            mActivityMyOrdersDetailPageBinding.progressSpinKitView.setVisibility(View.GONE);
                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            try {
                                if (mJsonObject.getString("status").equals("200")) {
                                    Constants.showToastInMiddle(getApplicationContext(), "Order cancelled successfully");
                                    //Toast.makeText(getApplicationContext(), "Order cancelled successfully", Toast.LENGTH_LONG).show();
                                    mActivityMyOrdersDetailPageBinding.btnCancel.setVisibility(View.GONE);
                                    mActivityMyOrdersDetailPageBinding.btnPayNow.setVisibility(View.GONE);//for testing
                                } else {
                                    Constants.showToastInMiddle(getApplicationContext(), "Something wrong! Try again later");

                                    //Toast.makeText(getApplicationContext(), "Something wrong! Try again later", Toast.LENGTH_LONG).show();
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {
                    try {
                        String responseBody = new String(error.networkResponse.data, "utf-8");
                        JSONObject data = new JSONObject(responseBody);

                        String message = data.getString("message");
                        Constants.showToastInMiddle(getApplicationContext(), message);

                        //Toast.makeText(getApplicationContext(), message, Toast.LENGTH_LONG).show();
                    } catch (Exception ee) {
                        System.out.println("Rahul : DeliveryDetail : requestSaveOrder : onErrorResponse : " + ee);
                    }
                    mActivityMyOrdersDetailPageBinding.progressSpinKitView.setVisibility(View.GONE);
                    //mActivityMyOrdersDetailPageBinding.somethingwentwrong.setVisibility(View.VISIBLE);
                    System.out.println("Rahul : MyOrdersDetailPage : requestOrderCancel : VolleyError : " + error.toString());

                }
            }) {
                @Override
                public Map<String, String> getHeaders() throws AuthFailureError {
                    HashMap<String, String> headers = new HashMap<String, String>();
                    headers.put("Content-Type", "application/json");
                    headers.put(Constants.VARIABLES.WAREHOUSE_KEY, mSharedPreferenceManager.getWarehouseId());
                    headers.put("WID", "1");
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
        } else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }

    public void requestAddToCart(int argProductId, int argQty) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));
        mJsonObject.put("product_id", argProductId);
        mJsonObject.put("quantity", argQty);
        mJsonObject.put("year_check", mSharedPreferenceManager.getYearCheck());
        System.out.println("Rahul : MyOrdersDetailPage : requestAddToCart : param : " + mJsonObject);
        System.out.println("Rahul : MyOrdersDetailPage : requestAddToCart : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));


        JsonObjectRequest jsonObjReq = new JsonObjectRequest(com.android.volley.Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.ADD_TO_CART, mJsonObject,
                new com.android.volley.Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        addTocartPosition++;
                        System.out.println("Rahul : MyOrdersDetailPage : requestAddToCart : response : " + response);
                        mHandler.sendEmptyMessage(1);
                    }
                }, new com.android.volley.Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put(Constants.VARIABLES.WAREHOUSE_KEY, mSharedPreferenceManager.getWarehouseId());
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
}
