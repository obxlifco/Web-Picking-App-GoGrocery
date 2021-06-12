package com.gogrocery.view;

import android.app.Dialog;
import android.content.Intent;

import androidx.core.content.ContextCompat;
import androidx.databinding.DataBindingUtil;

import android.graphics.Color;
import android.os.Build;
import android.os.Handler;
import android.os.Message;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.text.Editable;
import android.text.InputFilter;
import android.text.TextWatcher;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;

import com.afollestad.materialdialogs.MaterialDialog;
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
import com.github.ybq.android.spinkit.SpinKitView;
import com.gogrocery.Adapters.MyCartAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.CartItemInterface;
import com.gogrocery.Models.CartModel.AddToCartModel;
import com.gogrocery.Models.CartSummaryModel.CartSummaryModel;
import com.gogrocery.Models.ProductQuantityLocal;
import com.gogrocery.Models.ViewCartModel.Data;
import com.gogrocery.Models.ViewCartModel.ViewCartModel;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityMyCartBinding;
import com.gogrocery.helper.SwipeHelper;
import com.gogrocery.helper.WrapContentLinearLayoutManager;
import com.google.android.material.textfield.TextInputEditText;
import com.google.android.material.textfield.TextInputLayout;
import com.google.firebase.analytics.FirebaseAnalytics;
import com.google.gson.Gson;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static com.gogrocery.Constants.Constants.EMOJI_FILTER;

public class MyCart extends AppCompatActivity implements CartItemInterface {

    View rootView;
    private ActivityMyCartBinding mActivityMyCartBinding;
    private DatabaseHandler mDatabaseHandler;
    private SharedPreferenceManager mSharedPreferenceManager;
    private MyCartAdapter mMyCartAdapter;
    private List<Data> mViewCartList = new ArrayList<>();
    private Dialog mPromocodeDialog;
    private Handler mHandler;
    private Double shippingCost = 0.00;
    private FirebaseAnalytics mFirebaseAnalytics;
    AppEventsLogger logger;
    private String paramCouponcode = "";
    private boolean isViewCartLoaded = false, isCartSummaryLoaded = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityMyCartBinding = DataBindingUtil.setContentView(this, R.layout.activity_my_cart);
        rootView = this.findViewById(android.R.id.content).getRootView();
        Constants.setupUI(rootView, MyCart.this);
        mActivityMyCartBinding.etAddNote.setFilters(new InputFilter[]{EMOJI_FILTER});
        mFirebaseAnalytics = FirebaseAnalytics.getInstance(this);
        logger = AppEventsLogger.newLogger(this);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        mDatabaseHandler = new DatabaseHandler(getApplicationContext());
        mActivityMyCartBinding.btnPlaceOrder.setClickable(true);
        hideStatusBarColor();
        setViewCartRecyclerView();

        Constants.VARIABLES.CURRENT_CURRENCY = mSharedPreferenceManager.getCurrentCurrency();
        try {

            requestViewCart();
            mActivityMyCartBinding.sfl.startShimmer();
        } catch (JSONException e) {
            e.printStackTrace();
        }

        mActivityMyCartBinding.ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                onBackPressed();
            }
        });

        mActivityMyCartBinding.rlApplyPromo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showPromoCodeDialog();
            }
        });

        mActivityMyCartBinding.btnPlaceOrder.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (mSharedPreferenceManager.isLoggedIn()) {
                    try {
                        requestCartSummary("btnPlaceOrder");
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }


                    try {


                        //requestCartSummary("btnPlaceOrder");
                    /*    new MaterialDialog.Builder(MyCart.this)
                                .title("Note")
                                .content("Dear customer, please note that for meats, vegetables, and fruits, the final/total price may be different than what is currently shown. This is due to weight variations in the products. Thank you for your understanding.")
                                .positiveText("Okay")
                                .positiveColor(ContextCompat.getColor(MyCart.this, R.color.app_green_clr))
                                // .negativeText(getResources().getString(R.string.dialogPositiveButtonText_cancel))
                                // .negativeColor(ContextCompat.getColor(this, R.color.selectIconColor))
                                .onPositive((dialog, which) -> {
                                    try {
                                        requestCartSummary("btnPlaceOrder");
                                    } catch (JSONException e) {
                                        e.printStackTrace();
                                    }

                                })
                                *//* .onNegative((dialog, which) -> {
                                     dialog.dismiss();
                                 })*//*.show();*/

                    } catch (Exception e) {
                        e.printStackTrace();
                    }

//            Picasso.with(getApplicationContext()).load(mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_profile_pic)).centerInside().fit().into(mActivityMainBinding.ivProfile);
                } else {

                    Intent i = new Intent(MyCart.this, LoginActivity.class);
                    i.putExtra("from_where", "MyCart");
                    startActivity(i);
                    finish();
                }
            }
        });

        mActivityMyCartBinding.includeEmptyCart.btnShopNow.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
                Intent btnShopNow = new Intent(MyCart.this, MainActivityNew.class);
                startActivity(btnShopNow);
            }
        });

        mActivityMyCartBinding.ivSearch.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent ivSearch = new Intent(MyCart.this, SearchActivity.class);
                startActivity(ivSearch);
            }
        });

        mActivityMyCartBinding.cvClose.setOnClickListener(v -> {
            mActivityMyCartBinding.cvClose.setVisibility(View.GONE);
            try {
                requestRemoveApplyPromoCode("");
            } catch (JSONException e) {
                e.printStackTrace();
            }
        });

        mHandler = new Handler(new Handler.Callback() {
            @Override
            public boolean handleMessage(Message msg) {

                if (isViewCartLoaded && isCartSummaryLoaded) {
                    mActivityMyCartBinding.progressSpinKitView.setVisibility(View.GONE);
                }
                return false;
            }
        });
        mActivityMyCartBinding.etAddNote.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
                mActivityMyCartBinding.etAddNote.setFilters(new InputFilter[]{EMOJI_FILTER});
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {

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

    private void setViewCartRecyclerView() {
        mMyCartAdapter = new MyCartAdapter(getApplicationContext(), mViewCartList, mDatabaseHandler, this);
        WrapContentLinearLayoutManager mLayoutManager = new WrapContentLinearLayoutManager(getApplicationContext());
        mActivityMyCartBinding.rvViewCart.setLayoutManager(mLayoutManager);
 /*       mActivityMyCartBinding.rvViewCart.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        mActivityMyCartBinding.rvViewCart.setItemAnimator(new DefaultItemAnimator());*/
        mActivityMyCartBinding.rvViewCart.setAdapter(mMyCartAdapter);
        mActivityMyCartBinding.rvViewCart.setNestedScrollingEnabled(false);
        SwipeHelper swipeHelper = new SwipeHelper(this, mActivityMyCartBinding.rvViewCart) {
            @Override
            public void instantiateUnderlayButton(RecyclerView.ViewHolder viewHolder, List<UnderlayButton> underlayButtons) {
                underlayButtons.add(new SwipeHelper.UnderlayButton(
                        "", R.drawable.ic_close_white,
                        Color.parseColor("#93C88D"),
                        new SwipeHelper.UnderlayButtonClickListener() {
                            @Override
                            public void onClick(int pos) {
                                // TODO: onDelete
                                try {
                                    requestAddToCart(mViewCartList.get(pos).getProductId().getId(), 0, pos);
                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }
                                //deleteOrderItem(pos);
                            }
                        }
                ));
            }
        };
    }

    private void showPromoCodeDialog() {
        mPromocodeDialog = new Dialog(this);
        mPromocodeDialog.setContentView(R.layout.apply_promocode_dialog);

        TextInputEditText edtPromocode = mPromocodeDialog.findViewById(R.id.edtPromocode);
        TextInputLayout tilEnterPromocode = mPromocodeDialog.findViewById(R.id.tilEnterPromocode);
        Button btnApplyCode = mPromocodeDialog.findViewById(R.id.btnApplyPromocode);
        ProgressBar mPromocodeSpin = mPromocodeDialog.findViewById(R.id.progressSpinKitView);


        btnApplyCode.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (edtPromocode.getText().toString().isEmpty()) {
                    tilEnterPromocode.setError(getResources().getString(R.string.enter_valid_code));
                } else {
                    try {
                        if (mActivityMyCartBinding.tvCoupon.getText().toString().equalsIgnoreCase(getResources().getString(R.string.add_coupon))) {
                            requestApplyPromoCode(edtPromocode.getText().toString().trim(), mPromocodeSpin);
                        } else {

                        }

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            }
        });

        mPromocodeDialog.show();

    }

    public void requestApplyPromoCode(String argCouponCode, ProgressBar mSpinKitView) throws JSONException {
        if (Constants.isInternetConnected(MyCart.this)) {
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
                                    mActivityMyCartBinding.tvCoupon.setText(paramCouponcode);


                                    if (mAppliedCouponObject.getInt("status") == 1) {
                                        mActivityMyCartBinding.cvClose.setVisibility(View.VISIBLE);
                                        // Toast.makeText(getApplicationContext(), mAppliedCouponObject.getString("message"), Toast.LENGTH_LONG).show();
                                        paramCouponcode = argCouponCode;
                                        mPromocodeDialog.dismiss();
                                        mActivityMyCartBinding.tvSubtotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("sub_total"))));
                                        mActivityMyCartBinding.tvTotalSumPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("grand_total"))));
                                        mActivityMyCartBinding.llDiscount.setVisibility(View.VISIBLE);
                                        mActivityMyCartBinding.llCoupon.setVisibility(View.GONE);
                                        //mActivityMyCartBinding.tvPlaceOrderPrice.setText(mActivityDeliveryDetailBinding.tvTotalSumPrice.getText().toString());
                                        mActivityMyCartBinding.tvDiscount.setText("- " + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mAppliedCouponObject.getString("amount"))));

                                        mActivityMyCartBinding.tvDiscount.setTextColor(getApplicationContext().getResources().getColor(R.color.green_dark_new));
                                        mActivityMyCartBinding.tvEstimatedTax.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("tax_amount"))));
                                        //    mActivityMyCartBinding.txtApplyPromoCode.setText("You have saved " + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mAppliedCouponObject.getString("amount"))));

                                    /*if (mOrderAmountDetails.getString("applied_loyalty_amount") != null) {
                                        mActivityMyCartBinding.llLoyaltyPoints.setVisibility(View.VISIBLE);
                                        mActivityMyCartBinding.tvAppliedLoyaltyAmount.setText(Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("applied_loyalty_amount"))));
                                        mActivityMyCartBinding.tvLoyaltyUsabilityDetail.setText("You can use upto " + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("applied_loyalty_amount"))) + " for this order");

                                    } else {
                                        mActivityMyCartBinding.llLoyaltyPoints.setVisibility(View.GONE);
                                        mActivityMyCartBinding.tvAppliedLoyaltyAmount.setText(Constants.VARIABLES.CURRENT_CURRENCY + " 0.00");

                                    }*/


                                    } else {
                                        Constants.showToastInMiddle(getApplicationContext(), mAppliedCouponObject.getString("message"));
                                        mActivityMyCartBinding.cvClose.setVisibility(View.GONE);
                                        mActivityMyCartBinding.llDiscount.setVisibility(View.GONE);
                                        mActivityMyCartBinding.llCoupon.setVisibility(View.VISIBLE);
                                        mActivityMyCartBinding.txtApplyPromoCode.setText(getResources().getString(R.string.my_cart_apc));
                                        mActivityMyCartBinding.tvCoupon.setText(getResources().getString(R.string.add_coupon));
                                        mActivityMyCartBinding.ivCoupon.setBackground(getResources().getDrawable(R.drawable.tick_black));
                                        //Toast.makeText(getApplicationContext(), mAppliedCouponObject.getString("message"), Toast.LENGTH_LONG).show();
                                    }

                                } else {
                                    mActivityMyCartBinding.llCoupon.setVisibility(View.VISIBLE);
                                    mActivityMyCartBinding.cvClose.setVisibility(View.GONE);
                                    mActivityMyCartBinding.txtApplyPromoCode.setText(getResources().getString(R.string.my_cart_apc));
                                    mActivityMyCartBinding.tvCoupon.setText(getResources().getString(R.string.add_coupon));
                                    mActivityMyCartBinding.ivCoupon.setBackground(getResources().getDrawable(R.drawable.tick_black));
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
        if (Constants.isInternetConnected(MyCart.this)) {
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            System.out.println("Rahul : MyCart : requestApplyPromoCode : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
            JSONObject mParam = new JSONObject();

        /*if (mActivityMyCartBinding.llLoyaltyPoints.getVisibility() == View.VISIBLE) {
            mParam.put("redeem_amount", Double.parseDouble(mActivityMyCartBinding.tvAppliedLoyaltyAmount.getText().toString().trim().replace(Constants.VARIABLES.CURRENT_CURRENCY, "")));
            mParam.put("rule_id", rule_id);
        }*/
            mActivityMyCartBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            System.out.println("Rahul : MyCart : requestApplyPromoCode : mParam : " + mParam);

            JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                    Constants.BASE_URL + Constants.API_METHODS.APPLY_COUPON, mParam,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            mActivityMyCartBinding.progressSpinKitView.setVisibility(View.GONE);
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
                                    mActivityMyCartBinding.tvSubtotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("sub_total"))));
                                    mActivityMyCartBinding.tvTotalSumPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("grand_total"))));
                                    //mActivityMyCartBinding.tvPlaceOrderPrice.setText(mActivityDeliveryDetailBinding.tvTotalSumPrice.getText().toString());
                                    mActivityMyCartBinding.tvDiscount.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " 0.0");
                                    mActivityMyCartBinding.llDiscount.setVisibility(View.GONE);
                                    mActivityMyCartBinding.llCoupon.setVisibility(View.VISIBLE);
                                    //mActivityDeliveryDetailBinding.tvDiscount.setTextColor(getApplicationContext().getResources().getColor(R.color.app_red_clr));
                                    mActivityMyCartBinding.tvEstimatedTax.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("tax_amount"))));
                                    mActivityMyCartBinding.txtApplyPromoCode.setText("Apply Promo Code");
                                    mActivityMyCartBinding.tvCoupon.setText("Add Coupon");
                                    mActivityMyCartBinding.ivCoupon.setBackground(getResources().getDrawable(R.drawable.tick_black));
                                /*if (mOrderAmountDetails.getString("applied_loyalty_amount") != null) {
                                    mActivityMyCartBinding.llLoyaltyPoints.setVisibility(View.VISIBLE);
                                    mActivityMyCartBinding.tvAppliedLoyaltyAmount.setText(Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("applied_loyalty_amount"))));
                                    mActivityMyCartBinding.tvLoyaltyUsabilityDetail.setText("You can use upto " + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderAmountDetails.getString("applied_loyalty_amount"))) + " for this order");

                                } else {
                                    mActivityMyCartBinding.llLoyaltyPoints.setVisibility(View.GONE);
                                    mActivityMyCartBinding.tvAppliedLoyaltyAmount.setText(Constants.VARIABLES.CURRENT_CURRENCY + " 0.00");

                                }*/


                                } else {
                                    paramCouponcode = "";
                                    Constants.showToastInMiddle(getApplicationContext(), getString(R.string.something_went_wrong));
                                    mActivityMyCartBinding.llCoupon.setVisibility(View.GONE);
                                    // Toast.makeText(getApplicationContext(), getString(R.string.something_went_wrong), Toast.LENGTH_LONG).show();
                                }


                            } catch (JSONException e) {
                                e.printStackTrace();
                            }


                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {
                    mActivityMyCartBinding.progressSpinKitView.setVisibility(View.GONE);
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


    public void requestViewCart() throws JSONException {
        if (Constants.isInternetConnected(MyCart.this)) {
            mActivityMyCartBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            System.out.println("Rahul : MyCart : requestViewCart : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
            JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                    Constants.BASE_URL + Constants.API_METHODS.VIEW_CART, null,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            mActivityMyCartBinding.progressSpinKitView.setVisibility(View.GONE);
                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            System.out.println("Rahul : MyCart : requestViewCart : mJsonObject : " + mJsonObject);
                            ViewCartModel mViewCartModel = mGson.fromJson(response.toString(), ViewCartModel.class);
                            if (!mViewCartModel.getCartCount().equals("0")) {
                                mDatabaseHandler.deleteAllRecord();
                                mViewCartList.addAll(mViewCartModel.getData());
                                System.out.println("Rahul : MyCart : requestViewCart : mViewCartList.size : " + mViewCartList.size());
                                mActivityMyCartBinding.sfl.stopShimmer();
                                mActivityMyCartBinding.sfl.setVisibility(View.GONE);
                                mActivityMyCartBinding.nsvMyCart.setVisibility(View.VISIBLE);

                                mMyCartAdapter.notifyDataSetChanged();

                                setPageUI(mViewCartModel);
                                System.out.println("Rahul : MyCart : requestViewCart : mViewCartList : " + mGson.toJson(mViewCartList));
                            } else {
                                mDatabaseHandler.deleteAllRecord();
                                mActivityMyCartBinding.sfl.stopShimmer();
                                mActivityMyCartBinding.sfl.setVisibility(View.GONE);
                                mActivityMyCartBinding.noResponse.setVisibility(View.VISIBLE);
                                mActivityMyCartBinding.nsvMyCart.setVisibility(View.GONE);
                                mActivityMyCartBinding.rlBadge.setVisibility(View.GONE);
                                mActivityMyCartBinding.cvFooter.setVisibility(View.GONE);
                            }
                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {

                    mDatabaseHandler.deleteAllRecord();
                    System.out.println("Rahul : MyCart : requestViewCart : VolleyError : " + error.toString());
                    mActivityMyCartBinding.sfl.stopShimmer();
                    mActivityMyCartBinding.sfl.setVisibility(View.GONE);
                    mActivityMyCartBinding.noResponse.setVisibility(View.VISIBLE);
                    mActivityMyCartBinding.nsvMyCart.setVisibility(View.GONE);
                    mActivityMyCartBinding.rlBadge.setVisibility(View.GONE);
                    mActivityMyCartBinding.cvFooter.setVisibility(View.GONE);
                }
            }) {
                @Override
                public Map<String, String> getHeaders() throws AuthFailureError {
                    HashMap<String, String> headers = new HashMap<String, String>();
                    headers.put("Content-Type", "application/json");
                    headers.put(Constants.VARIABLES.WAREHOUSE_KEY, mSharedPreferenceManager.getWarehouseId());
                    if (mSharedPreferenceManager.isLoggedIn()) {
                        headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                    } else {
                        headers.put("DEVICEID", Constants.getDeviceId(getApplicationContext()));
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
            // Adding request to request queue
            queue.add(jsonObjReq);
        } else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }

    public void requestCartSummary(String argFrom) throws JSONException {
        if (Constants.isInternetConnected(MyCart.this)) {
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            System.out.println("Rahul : DeliveryDetail : requestCheckLoyaltyBalance : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
            JSONObject mParam = new JSONObject();
            mParam.put("warehouse_id", mSharedPreferenceManager.getWarehouseId());
            mParam.put("address_id", "");
            mParam.put("coupon_code", paramCouponcode);
            System.out.println("Rahul : DeliveryDetail : requestCheckLoyaltyBalance : mParam : " + mParam);

            JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                    Constants.BASE_URL + Constants.API_METHODS.CART_SUMMARY, mParam,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {


                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            mActivityMyCartBinding.progressSpinKitView.setVisibility(View.GONE);
                            mActivityMyCartBinding.btnPlaceOrder.setClickable(true);
                            System.out.println("Rahul : DeliveryDetail : requestCheckLoyaltyBalance : mJsonObject : " + mJsonObject);
                            try {


                                CartSummaryModel mCartSummaryModel = mGson.fromJson(response.toString(), CartSummaryModel.class);
                                if (mCartSummaryModel.getStatus().equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                    mActivityMyCartBinding.tvSubtotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mCartSummaryModel.getData().getOrderamountdetails().get(0).getSubTotal())));
                                    mActivityMyCartBinding.tvTotalSumPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mCartSummaryModel.getData().getOrderamountdetails().get(0).getGrandTotal())));
                                    mActivityMyCartBinding.tvDeliveryCharges.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mCartSummaryModel.getData().getOrderamountdetails().get(0).getShippingCharge())));
                                    if (paramCouponcode != null && !paramCouponcode.isEmpty()) {
                                        mActivityMyCartBinding.llDiscount.setVisibility(View.VISIBLE);
                                        mActivityMyCartBinding.llCoupon.setVisibility(View.GONE);
                                        JSONArray mAppliedCouponDetail = response.getJSONObject("data").getJSONArray("applied_coupon");
                                        JSONObject mAppliedCouponObject = mAppliedCouponDetail.getJSONObject(0);
                                        mActivityMyCartBinding.tvDiscount.setText("-" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mAppliedCouponObject.getString("amount"))));
                                    } else {
                                        mActivityMyCartBinding.llDiscount.setVisibility(View.GONE);
                                        mActivityMyCartBinding.llCoupon.setVisibility(View.GONE);
                                    }
                                    if (!mCartSummaryModel.getData().getOrderamountdetails().get(0).getShippingCharge().equalsIgnoreCase("0")) {

                                        mActivityMyCartBinding.tvDeliveryCharges.setText(Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mCartSummaryModel.getData().getOrderamountdetails().get(0).getShippingCharge())));
                                    }
                                    switch (argFrom) {
                                        case "btnPlaceOrder":
                                            ArrayList<String> productNameList = new ArrayList<>();
                                            ArrayList<String> productId = new ArrayList<>();
                                            if (mCartSummaryModel.getMinimum_order_amount_check().equalsIgnoreCase("yes")) {
                                                mActivityMyCartBinding.btnPlaceOrder.setClickable(false);


                                                for (int i = 0; i < mCartSummaryModel.getData().getCartdetails().size(); i++) {

                                                    productNameList.add(mCartSummaryModel.getData().getCartdetails().get(i).getName() + ",");
                                                    productId.add(mCartSummaryModel.getData().getCartdetails().get(i).getId() + ",");

                                                }

                                                Bundle params = new Bundle();
                                                params.putString("productName", productNameList.toString());
                                                params.putString("productId", productId.toString());
                                                params.putString("total_item_count", Constants.VARIABLES.CART_COUNT + "");
                                                params.putString("orderamountdetails", mActivityMyCartBinding.tvTotalSumPrice.getText().toString());
                                                params.putString("content_type", "product_group");
                                                params.putString("currency", Constants.VARIABLES.CURRENT_CURRENCY);
                                                mFirebaseAnalytics.logEvent("Initiate_checkout", params);
                                                logger.logEvent("Initiate_checkout", params);


                                                Intent btnPlaceOrder = new Intent(MyCart.this, DeliveryDetail.class);
                                                btnPlaceOrder.putExtra("subtotal", mActivityMyCartBinding.tvSubtotal.getText().toString());
                                                btnPlaceOrder.putExtra("coupon_code", paramCouponcode);
                                                btnPlaceOrder.putExtra("discount", mActivityMyCartBinding.tvDiscount.getText().toString());
                                                btnPlaceOrder.putExtra("delivery_charges", mActivityMyCartBinding.tvDeliveryCharges.getText().toString());
                                                btnPlaceOrder.putExtra("estimated_tax", mActivityMyCartBinding.tvEstimatedTax.getText().toString());
                                                btnPlaceOrder.putExtra("final_amount", mActivityMyCartBinding.tvTotalSumPrice.getText().toString());
                                                btnPlaceOrder.putExtra("product_name", productNameList.toString());
                                                btnPlaceOrder.putExtra("product_id", productId.toString());
                                                btnPlaceOrder.putExtra("final_amount", mActivityMyCartBinding.tvTotalSumPrice.getText().toString());
                                                Constants.VARIABLES.SPECIAL_INSTRUCTION = mActivityMyCartBinding.etAddNote.getText().toString();
                                                startActivity(btnPlaceOrder);
                                            } else {

                                                Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.minimum_order_should_be_above) + Constants.VARIABLES.CURRENT_CURRENCY + " " + mCartSummaryModel.getMinimum_order_amount());

                                                //Toast.makeText(getApplicationContext(), "Minimum Order Anount " + Constants.VARIABLES.CURRENT_CURRENCY + " " + mCartSummaryModel.getMinimum_order_amount(), Toast.LENGTH_SHORT).show();
                                            }

                                            break;
                                        case "":

                                            break;
                                    }


                                }

                            } catch (
                                    Exception e) {
                                e.printStackTrace();
                                System.out.println("Rahul : DeliveryDetail : requestCheckLoyaltyBalance : Exception : " + e);
                            }


                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {
                    mActivityMyCartBinding.progressSpinKitView.setVisibility(View.GONE);
                    mActivityMyCartBinding.btnPlaceOrder.setClickable(true);
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

        } else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }


    private void setPageUI(ViewCartModel mViewCartModel) {
        mActivityMyCartBinding.tvSubtotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mViewCartModel.getTotalAmount())));
        mActivityMyCartBinding.tvTotalSumPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mViewCartModel.getFinalAmount())));
        mActivityMyCartBinding.tvDeliveryCharges.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mViewCartModel.getShippingAmount())));
        shippingCost = Double.parseDouble(mViewCartModel.getShippingAmount());
        mActivityMyCartBinding.badgeNotification.setText(mViewCartModel.getCart_count_itemwise());
        Constants.VARIABLES.CART_COUNT = Integer.parseInt(mViewCartModel.getCart_count_itemwise());
        Constants.VARIABLES.CART_SUB_AMOUNT = Constants.twoDecimalRoundOff(Double.parseDouble(mViewCartModel.getTotalAmount()));
    }

    public void requestAddToCart(int argProductId, int argQty, int argPosition) throws JSONException {
        if (Constants.isInternetConnected(MyCart.this)) {
            mActivityMyCartBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            JSONObject mJsonObject = new JSONObject();
            mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));
            mJsonObject.put("product_id", argProductId);
            mJsonObject.put("quantity", argQty);
            mJsonObject.put("year_check", mSharedPreferenceManager.getYearCheck());
            System.out.println("Rahul : MyCart : requestAddToCart : param : " + mJsonObject);
            System.out.println("Rahul : MyCart : requestAddToCart : argPosition : " + argPosition);

            System.out.println("Rahul : MyCart : requestAddToCart : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));

            JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                    Constants.BASE_URL + Constants.API_METHODS.ADD_TO_CART, mJsonObject,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            try {
                                Gson mGson = new Gson();
                                JSONObject mJsonObject = response;
                                System.out.println("Rahul : MyCart : requestAddToCart : mJsonObject : " + mJsonObject);
                                mActivityMyCartBinding.progressSpinKitView.setVisibility(View.GONE);
                                AddToCartModel mAddToCartModel = mGson.fromJson(mJsonObject.toString(), AddToCartModel.class);
                                if (mAddToCartModel.getStatus() != 0) {
                                    if (mAddToCartModel.getCartData().getCart_count().equals("0")) {
                                        mActivityMyCartBinding.sfl.stopShimmer();
                                        mActivityMyCartBinding.sfl.setVisibility(View.GONE);
                                        mActivityMyCartBinding.noResponse.setVisibility(View.VISIBLE);
                                        mActivityMyCartBinding.rlBadge.setVisibility(View.GONE);
                                        mActivityMyCartBinding.cvFooter.setVisibility(View.GONE);
                                        mActivityMyCartBinding.nsvMyCart.setVisibility(View.GONE);
                                    }

                                    if (argQty == 0) {
                                        mViewCartList.remove(argPosition);
                                        mMyCartAdapter.notifyItemRemoved(argPosition);
                                        mMyCartAdapter.notifyItemRangeChanged(argPosition, mViewCartList.size());
                                        mDatabaseHandler.deleteSingleRecord(String.valueOf(argProductId));
                                    } else {
                                        int cartItemCount = 0;
                                        for (int i = 0; i < mAddToCartModel.getCartData().getCartdetails().size(); i++) {
                                            cartItemCount = cartItemCount + Integer.parseInt(mAddToCartModel.getCartData().getCartdetails().get(i).getQty());

                                        }


                                        ProductQuantityLocal mProductQuantityLocal = new ProductQuantityLocal(String.valueOf(argProductId), String.valueOf(argQty));
                                        if (!mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(argProductId)).equals("0")) {
                                            mDatabaseHandler.updateProductQuantityById(mProductQuantityLocal);
                                        } else {
                                            mDatabaseHandler.addProductQty(mProductQuantityLocal);
                                        }
                                        System.out.println("Rahul : MyCart : checkDbCount : " + mDatabaseHandler.getAllProductQtyData().size());
                                        for (int i = 0; i < mAddToCartModel.getCartData().getCartdetails().size(); i++) {
                                            if (argProductId == Integer.parseInt(mAddToCartModel.getCartData().getCartdetails().get(i).getId())) {
                                                mViewCartList.get(argPosition).setNewDefaultPrice(String.valueOf(mAddToCartModel.getCartData().getCartdetails().get(i).getNewDefaultPrice()));
                                                mViewCartList.get(argPosition).setQuantity(Integer.valueOf(mAddToCartModel.getCartData().getCartdetails().get(i).getQty()));
                                            }
                                        }

                                        Constants.showToastInMiddle(getApplicationContext(), mAddToCartModel.getMsg());
                                        // Toast.makeText(getApplicationContext(), mAddToCartModel.getMsg(), Toast.LENGTH_LONG).show();
                                        mMyCartAdapter.notifyDataSetChanged();
                                    }

                                    mActivityMyCartBinding.tvSubtotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(mAddToCartModel.getCartData().getOrderamountdetails().get(0).getSubTotal()));
                                    mActivityMyCartBinding.tvTotalSumPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(shippingCost + mAddToCartModel.getCartData().getOrderamountdetails().get(0).getGrandTotal()));
                                    //  mActivityMyCartBinding.tvTotalSumPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mViewCartModel.getFinalAmount())));
                                    //mActivityMyCartBinding.tvPlaceOrderPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(mAddToCartModel.getCartData().getOrderamountdetails().get(0).getGrandTotal()));
                                    mActivityMyCartBinding.badgeNotification.setText(mAddToCartModel.getCartData().getCart_count());
                                    Constants.VARIABLES.CART_COUNT = Integer.parseInt(mAddToCartModel.getCartData().getCart_count());
                                    Constants.VARIABLES.CART_SUB_AMOUNT = Constants.twoDecimalRoundOff(mAddToCartModel.getCartData().getOrderamountdetails().get(0).getSubTotal());
                                    mActivityMyCartBinding.badgeNotification.setText("" + mAddToCartModel.getCartData().getCart_count());
                                    Bundle params = new Bundle();
                                    if (mAddToCartModel.getCartData().getCartdetails().size() > 0) {
                                        params.putString("productName", mAddToCartModel.getCartData().getCartdetails().get(0).getName());
                                        params.putString("productId", mAddToCartModel.getCartData().getCartdetails().get(0).getId());
                                    }
                                    params.putString("addedQuanity", mAddToCartModel.getCartData().getCart_count());
                                    params.putString("content_type", "product");
                                    params.putString("currency", Constants.VARIABLES.CURRENT_CURRENCY);
                                    mFirebaseAnalytics.logEvent(FirebaseAnalytics.Event.ADD_TO_CART, params);
                                    logger.logEvent(AppEventsConstants.EVENT_NAME_ADDED_TO_CART, params);

                                    AnimateBell();

                                } else {
                                    for (int i = 0; i < mAddToCartModel.getCartData().getCartdetails().size(); i++) {
                                        if (argProductId == Integer.parseInt(mAddToCartModel.getCartData().getCartdetails().get(i).getId())) {
                                            mViewCartList.get(argPosition).setNewDefaultPrice(Constants.twoDecimalRoundOff(mAddToCartModel.getCartData().getCartdetails().get(i).getNewDefaultPrice()));
                                            mViewCartList.get(argPosition).setQuantity(Integer.valueOf(mAddToCartModel.getCartData().getCartdetails().get(i).getQty()));
                                        }
                                    }
//
                                    try {
                                        if (response.getString("is_age_verification").equals("False")) {
                                            Intent i = new Intent(MyCart.this, TobacoCatActivity.class);
                                            i.putExtra("message", mAddToCartModel.getMsg());
                                            startActivity(i);
                                        } else {
                                            Constants.showToastInMiddle(getApplicationContext(), mAddToCartModel.getMsg());
                                        }
                                    } catch (JSONException e) {
                                        e.printStackTrace();
                                    }
                                    mMyCartAdapter.notifyItemChanged(argPosition);

                                    // Toast.makeText(getApplicationContext(), mAddToCartModel.getMsg(), Toast.LENGTH_LONG).show();
                                }

                            } catch (Exception e) {
                                e.printStackTrace();
                            }


                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {

                    System.out.println("Rahul : MyCart : requestAddToCart : VolleyError : " + error.toString());
                    mActivityMyCartBinding.progressSpinKitView.setVisibility(View.GONE);

                }
            }) {
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
            // Adding request to request queue
            queue.add(jsonObjReq);
        } else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }


    public void AnimateBell() {

        Animation shake = AnimationUtils.loadAnimation(getApplicationContext(), R.anim.shake);
        mActivityMyCartBinding.badgeNotification.setVisibility(View.VISIBLE);
        mActivityMyCartBinding.ivCart.setImageResource(R.drawable.ic_cart);
        mActivityMyCartBinding.ivCart.setAnimation(shake);
        mActivityMyCartBinding.ivCart.startAnimation(shake);

    }


    @Override
    public void connectCartMain(int argProductId, int argQuantity, int argPosition) {
        try {
            requestAddToCart(argProductId, argQuantity, argPosition);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void connectCartToDetail(int argProductId, String argSlug) {
        Intent i = new Intent(MyCart.this, DetailActivity.class);
        i.putExtra("slug", argSlug.split("#GoGrocery#")[0]);
        i.putExtra("title", argSlug.split("#GoGrocery#")[1]);
        i.putExtra("product_id", argProductId);
        startActivity(i);
    }

    @Override
    protected void onRestart() {
        super.onRestart();
        mActivityMyCartBinding.btnPlaceOrder.setClickable(true);
    }


}
