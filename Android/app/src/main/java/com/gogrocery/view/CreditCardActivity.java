package com.gogrocery.view;

import android.content.Intent;
import androidx.databinding.DataBindingUtil;
import androidx.annotation.Nullable;

import com.gogrocery.R;
import com.google.android.material.bottomsheet.BottomSheetDialog;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.gogrocery.Adapters.YearBottomSheetDialogAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Interfaces.SingleStringPassingInterface;
import com.gogrocery.MasterCardPayment.ApiController;
import com.gogrocery.MasterCardPayment.Config;
import com.gogrocery.Models.MonthYearModel;
import com.gogrocery.Models.MyOrdersHistoryModel.Data;
import com.gogrocery.databinding.ActivityCreditCardBinding;
import com.google.gson.Gson;
import com.mastercard.gateway.android.sdk.Gateway;
import com.mastercard.gateway.android.sdk.GatewayCallback;
import com.mastercard.gateway.android.sdk.GatewayMap;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public class CreditCardActivity extends AppCompatActivity implements SingleStringPassingInterface {


    private ActivityCreditCardBinding mActivityCreditCardBinding;
    private String OrderDetail = "", OrderId = "";
    private SharedPreferenceManager mSharedPreferenceManager;
    private ArrayList<MonthYearModel> mMonthArrayList = new ArrayList<MonthYearModel>();
    private ArrayList<MonthYearModel> mYearArrayList = new ArrayList<MonthYearModel>();
    private BottomSheetDialog mYearBottomSheetDialog;
    private YearBottomSheetDialogAdapter mYearBottomSheetDialogAdapter;
    private boolean isMonth = false;
    private String expMonth = "", expYear = "";
    private String session_Id = "";


    //------------------------------------------------MARSTERCARD PAYMENT --------------------------
    static final int REQUEST_CARD_INFO = 100;

    // static for demo
    private String AMOUNT = "0.00";
    static final String CURRENCY = Constants.VARIABLES.CURRENT_CURRENCY;

    Gateway gateway;
    String sessionId, apiVersion = "53", threeDSecureId, orderId, transactionId;
    boolean isGooglePay = false;
    ApiController apiController = ApiController.getInstance();
    //------------------------------------------------MARSTERCARD PAYMENT --------------------------

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        mActivityCreditCardBinding = DataBindingUtil.setContentView(this, R.layout.activity_credit_card);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());

        Gateway gateway = new Gateway();
        gateway.setMerchantId("000008047730");
        gateway.setRegion(Gateway.Region.ASIA_PACIFIC);


        getOrderIdBundel();

        mActivityCreditCardBinding.tvChangeAddress.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent btnChangeAddAddresses = new Intent(CreditCardActivity.this, MyAddresses.class);
                btnChangeAddAddresses.putExtra("from", "Delivery_Detail");
                startActivityForResult(btnChangeAddAddresses, 1);
            }
        });

        mActivityCreditCardBinding.btnPayNow.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (mActivityCreditCardBinding.edtCardNumber.getText().toString().isEmpty()) {
                    mActivityCreditCardBinding.edtCardNumber.setError(getApplicationContext().getResources().getString(R.string.filed_empty_error));
                } else if (mActivityCreditCardBinding.edtNameOnCard.getText().toString().isEmpty()) {
                    mActivityCreditCardBinding.edtNameOnCard.setError(getApplicationContext().getResources().getString(R.string.filed_empty_error));

                } else if (mActivityCreditCardBinding.edtExpiryMonth.getText().toString().isEmpty()) {
                    mActivityCreditCardBinding.edtExpiryMonth.setError("");

                } else if (mActivityCreditCardBinding.edtExpiryYear.getText().toString().isEmpty()) {
                    mActivityCreditCardBinding.edtExpiryYear.setError("");

                } else if (mActivityCreditCardBinding.edtCvv.getText().toString().isEmpty()) {
                    mActivityCreditCardBinding.edtCvv.setError(getApplicationContext().getResources().getString(R.string.filed_empty_error));

                } else if (mActivityCreditCardBinding.edtCvv.getText().toString().length() > 3) {
                    mActivityCreditCardBinding.edtCvv.setError("CVV should be less than three digit");

                } else {

                   /* GatewayMap request = new GatewayMap()
                            .set("sourceOfFunds.provided.card.nameOnCard", mActivityCreditCardBinding.edtNameOnCard.getText().toString())
                            .set("sourceOfFunds.provided.card.number", mActivityCreditCardBinding.edtCardNumber.getText().toString())
                            .set("sourceOfFunds.provided.card.securityCode", mActivityCreditCardBinding.edtCvv.getText().toString())
                            .set("sourceOfFunds.provided.card.expiry.month", mActivityCreditCardBinding.edtExpiryMonth.getText().toString())
                            .set("sourceOfFunds.provided.card.expiry.year", mActivityCreditCardBinding.edtExpiryYear.getText().toString());


                    gateway.updateSession(sessionId, "53", request,  new UpdateSessionCallback());*/


                  /*  try {
                        requestUpdateSessionWithPayersData(session_Id, mActivityCreditCardBinding.edtCardNumber.getText().toString(), expMonth,
                                expYear, mActivityCreditCardBinding.edtCvv.getText().toString());
                    } catch (JSONException e) {
                        e.printStackTrace();
                        System.out.println("Rahul : CreditCardActivity : requestUpdateSessionWithPayersData : JSONException : " + e);
                    }
*/
                   /* try {
                        requestPayment();
                       *//* JSONObject mJsonObject = new JSONObject();
                        mJsonObject.put("order_id", Integer.parseInt(OrderId));
                        mJsonObject.put("payment_method_id", 51);
                        mJsonObject.put("payment_type_id", 2);
                        mJsonObject.put("payment_method_name", "Credit / Debit Card");
                        mJsonObject.put("card_number", mActivityCreditCardBinding.edtCardNumber.getText().toString());
                        mJsonObject.put("exp_month", expMonth);
                        mJsonObject.put("exp_year", expYear);
                        mJsonObject.put("sec_code", mActivityCreditCardBinding.edtCvv.getText().toString());
                        System.out.println("Rahul : CreditCardActivity : requestPayment : mJsonObject : " + mJsonObject);*//*
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }*/

                    String cardName = mActivityCreditCardBinding.edtNameOnCard.getText().toString();
                    String cardNumber = mActivityCreditCardBinding.edtCardNumber.getText().toString();
                    String cardExpiryMonth = expMonth;
                    String cardExpiryYear = expYear;
                    String cardCvv = mActivityCreditCardBinding.edtCvv.getText().toString();

                    updateSession(cardName, cardNumber, cardExpiryMonth, cardExpiryYear, cardCvv);
                }
            }
        });


        mActivityCreditCardBinding.backImg.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        mActivityCreditCardBinding.edtExpiryMonth.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                isMonth = true;
                setMonthEdtStuff();

            }
        });
        mActivityCreditCardBinding.edtExpiryMonth.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                if (hasFocus) {
                    isMonth = true;
                    setMonthEdtStuff();
                }
            }
        });

        mActivityCreditCardBinding.edtExpiryYear.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                isMonth = false;
                setYearEdtStuff();
            }
        });
        mActivityCreditCardBinding.edtExpiryYear.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                if (hasFocus) {
                    isMonth = false;
                    setYearEdtStuff();
                }
            }
        });

        initMarterCard();

    }

    void updateSession(String name, String number, String expiryMonth, String expiryYear, String cvv) {

        mActivityCreditCardBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        // build the gateway request
        GatewayMap request = new GatewayMap()
                .set("sourceOfFunds.provided.card.nameOnCard", name)
                .set("sourceOfFunds.provided.card.number", number)
                .set("sourceOfFunds.provided.card.securityCode", cvv)
                .set("sourceOfFunds.provided.card.expiry.month", expiryMonth)
                .set("sourceOfFunds.provided.card.expiry.year", expiryYear);

        System.out.println("Rahul : CreditCardActivity : updateSession : request  " + request);
        System.out.println("Rahul : CreditCardActivity : updateSession : sessionId  " + sessionId);
        System.out.println("Rahul : CreditCardActivity : updateSession : apiVersion  " + apiVersion);
        gateway.updateSession(sessionId, apiVersion, request, new UpdateSessionCallback());
    }


    private void initMarterCard() {
        // init api controller
        apiController.setMerchantServerUrl(Config.MERCHANT_URL.getValue(this));

        // init gateway
        gateway = new Gateway();
        gateway.setMerchantId(Config.MERCHANT_ID.getValue(this));
        try {
            Gateway.Region region = Gateway.Region.valueOf(Config.REGION.getValue(this));
            gateway.setRegion(region);
        } catch (Exception e) {
            Log.e(CreditCardActivity.class.getSimpleName(), "Invalid Gateway region value provided", e);
        }

        // random order/txn IDs for example purposes
        orderId = "891";
        transactionId = "891";

        createSession();

       /* // bind buttons
        binding.startButton.setOnClickListener(v -> createSession());
        binding.confirmButton.setOnClickListener(v -> {
            // 3DS is not applicable to Google Pay transactions
            if (isGooglePay) {
                processPayment();
            } else {
                check3dsEnrollment();
            }
        });
        binding.doneButton.setOnClickListener(v -> finish());*/
    }


    private void getOrderIdBundel() {

        OrderId = getIntent().getExtras().getString("orders_id");
        OrderDetail = getIntent().getExtras().getString("order_detail");

        setPageUI(OrderDetail);
    }


    void createSession() {

        apiController.createSession(new CreateSessionCallback());
    }

    class CreateSessionCallback implements ApiController.CreateSessionCallback {
        @Override
        public void onSuccess(String sessionId, String apiVersion) {
            Log.i("CreateSessionTask", "Session established");
         /*   binding.createSessionProgress.setVisibility(View.GONE);
            binding.createSessionSuccess.setVisibility(View.VISIBLE);*/
            mActivityCreditCardBinding.progressSpinKitView.setVisibility(View.GONE);
            CreditCardActivity.this.sessionId = sessionId;
            CreditCardActivity.this.apiVersion = "53";

            //collectCardInfo();
        }

        @Override
        public void onError(Throwable throwable) {
           /* Log.e(ProcessPaymentActivity.class.getSimpleName(), throwable.getMessage(), throwable);

            binding.createSessionProgress.setVisibility(View.GONE);
            binding.createSessionError.setVisibility(View.VISIBLE);

            showResult(R.drawable.failed, R.string.pay_error_unable_to_create_session);*/

            System.out.println("Rahul : CreditCardActivity : requestCreateSession : not Successfull : " + throwable);
        }
    }


    private void setPageUI(String argOrderDetail) {
        Data mData = new Gson().fromJson(argOrderDetail, Data.class);

        mActivityCreditCardBinding.tvSubtotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + mData.getNetAmount());
        mActivityCreditCardBinding.tvTotalSumPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + mData.getGrossAmount());
        mActivityCreditCardBinding.tvPlaceOrderPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + mData.getGrossAmount());

        AMOUNT = mData.getNetAmount();
        if (mData.getLoyalty_amount().equals("0.00")) {
            mActivityCreditCardBinding.llLoyaltyPoints.setVisibility(View.GONE);
        } else {
            mActivityCreditCardBinding.llLoyaltyPoints.setVisibility(View.VISIBLE);
            mActivityCreditCardBinding.tvAppliedLoyaltyAmount.setText(mData.getLoyalty_amount());
        }
        if (mData.getCoupon_discount().equals("0.00")) {
            mActivityCreditCardBinding.tvDiscount.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " 0.00");
        } else {
            mActivityCreditCardBinding.tvDiscount.setText(mData.getCoupon_discount());
        }

        mActivityCreditCardBinding.tvName.setText(mData.getDeliveryName());
        mActivityCreditCardBinding.tvAddress.setText(mData.getDeliveryStreetAddress() + mData.getDeliveryCity() + "\n" + mData.getDeliveryState() + "-" + mData.getDeliveryPostcode());
        mActivityCreditCardBinding.tvMobileNumber.setText(mData.getDeliveryPhone());

      /*  try {
            requestCreateSession();
        } catch (JSONException e) {
            e.printStackTrace();
        }*/
    }

    public void requestPayment() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        System.out.println("Rahul : PaymentOptionsAvailable : requestPayment : order_id : " + OrderId);
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("order_id", Integer.parseInt(OrderId));
        mJsonObject.put("payment_method_id", 51);
        mJsonObject.put("payment_type_id", 2);
        mJsonObject.put("payment_method_name", "Credit / Debit Card");
        mJsonObject.put("card_number", mActivityCreditCardBinding.edtCardNumber.getText().toString());
        mJsonObject.put("exp_month", expMonth);
        mJsonObject.put("exp_year", expYear);
        mJsonObject.put("sec_code", mActivityCreditCardBinding.edtCvv.getText().toString());


        System.out.println("Rahul : CreditCardActivity : requestPayment : mJsonObject : " + mJsonObject);
        mActivityCreditCardBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        System.out.println("Rahul : CreditCardActivity : requestPayment : param : " + mJsonObject);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.CARD_PAYMENT, new JSONObject("{\n" +
                "            \"order_id\":872,\n" +
                "                \"payment_method_id\":51,\n" +
                "                \"payment_type_id\":2,\n" +
                "                \"payment_method_name\":\"Credit / Debit Card\",\n" +
                "                \"card_number\":\"4375514503010000\",\n" +
                "                \"exp_month\":\"06\",\n" +
                "                \"exp_year\":\"20\",\n" +
                "                \"sec_code\":\"949\",\n" +
                "                \"device_type\":\"mob\"\n" +
                "\n" +
                "        }"),
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        mActivityCreditCardBinding.progressSpinKitView.setVisibility(View.GONE);

                        System.out.println("Rahul : CreditCardActivity : requestPayment : response : " + response);
                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;


                        try {
                            if (mJsonObject.getString("status").equalsIgnoreCase("200")) {
                                String acsUrl = mJsonObject.getJSONObject("response").getJSONObject("enroll_data").getJSONObject("3DSecure")
                                        .getJSONObject("authenticationRedirect").getJSONObject("customized").getString("acsUrl");
                                String PaReq = mJsonObject.getJSONObject("response").getJSONObject("enroll_data").getJSONObject("3DSecure")
                                        .getJSONObject("authenticationRedirect").getJSONObject("customized").getString("paReq");
                                /*Intent orderSuccess = new Intent(CreditCardActivity.this, WebviewActivity.class);
                                orderSuccess.putExtra("acsUrl", acsUrl);
                                orderSuccess.putExtra("PaReq", PaReq);
                                startActivity(orderSuccess);*/
                            }
                   /* {
                        "status": 200,
                            "response": {
                        "status": 1,
                                "enroll_data": {
                            "3DSecure": {
                                "authenticationRedirect": {
                                    "customized": {
                                        "acsUrl": "https://www.3dsecure.icicibank.com/ACSWeb/EnrollWeb/ICICIBank/server/AccessControlServer?idct=8112.V",
                                                "paReq": "eAFVUsFygjAUvDvjPzDcS0JAAecZB5WqnVEpaNUjDakyo2iDtrRf3wSltjll9yWbffsCvfKw1z64KLJj3tVNA+saz9kxzfJtV18uHh9cvUebDVjsBOfDmLOL4BSmvCiSLdeyVN7BGBPTw5blmo5OIfQj/k7hpkmlpEEA1VBeFWyX5GcKCXvvT2bUbtmu5wG6QThwMRlSKVotF9uOY2FAVxry5MDpfKb153401IJ1GAVxrMXjSRhOZiNAVR3Y8ZKfxRd1XBtQDeAi9nS8WIRxB6HVamWM5qNoPgiijeEHgFQV0N1eeFFGC9ltmaV0+5QW2cvJ/3wVZFOUHntj2+m6fGYb1gWkTkCanDkl2PRMQrCG2x3sdIgFqOIhOShP1A+GGjZwS/Z7JeCk3vGvQNJ/Ici0hRxH3UiNgJenY86lnEz2dw/obnkwVvmys0yydmSalkMs2yXWaYWLpfvdV5lXR5ReJuMiGLcrQQUAKRF0G6cMphq5ZP59hWbjB33stvw="
                                    }
                                },
                                "veResEnrolled": "Y",
                                        "xid": "gJdsiVpAwbr2Ysx9cfcgMXxQcYc="
                            },
                            "3DSecureId": "20122019060720_872",
                                    "merchant": "000008047730",
                                    "response": {
                                "gatewayRecommendation": "PROCEED"
                            }
                        }
                    },
                        "session_id": "SESSION0002640665589H7801513L26",
                            "message": "3D Check Successfull."
                    }*/
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    /*    System.out.println("Rahul : CreditCardActivity : requestPayment : mJsonObject : " + mJsonObject);
                        try {


                            if (response.getString("status").equalsIgnoreCase("200")) {
                                JSONObject order_summary = new JSONObject();
                                JSONObject delivery_address = new JSONObject();

                                order_summary.put("subtotal", mActivityCreditCardBinding.tvSubtotal.getText().toString());
                                order_summary.put("coupon_discount", mActivityCreditCardBinding.tvDiscount.getText().toString());
                                //  order_summary.put("loyalty_amount", mActivityDeliveryDetailBinding.tvAppliedLoyaltyAmount.getText().toString());
                                order_summary.put("delivery", mActivityCreditCardBinding.tvDeliveryCharges.getText().toString());
                                order_summary.put("tax", mActivityCreditCardBinding.tvEstimatedTax.getText().toString());
                                order_summary.put("loyalty_amount", mActivityCreditCardBinding.tvAppliedLoyaltyAmount.getText().toString());

                                order_summary.put("final_total", mActivityCreditCardBinding.tvTotalSumPrice.getText().toString());

                                delivery_address.put("name", mActivityCreditCardBinding.tvName.getText().toString());
                                delivery_address.put("address", mActivityCreditCardBinding.tvAddress.getText().toString());
                                delivery_address.put("number", mActivityCreditCardBinding.tvMobileNumber.getText().toString());

                                Intent orderSuccess = new Intent(CreditCardActivity.this, OrderSuccess.class);
                                orderSuccess.putExtra("order_id", "SAMPLE-ORD#" + response.getJSONObject("response").getJSONObject("order").getString("id"));
                                orderSuccess.putExtra("order_summary", order_summary.toString());
                                orderSuccess.putExtra("delivery_address", delivery_address.toString());
                                startActivity(orderSuccess);

                       *//* Intent orderSuccess = new Intent(PaymentOptionsAvailable.this, OrderSuccess.class);
                            orderSuccess.putExtra("order_id", response.getString("order_id"));
                            startActivity(orderSuccess);*//*
                            } else {

                                Toast.makeText(getApplicationContext(), "Please try again later", Toast.LENGTH_LONG).show();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
*/
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mActivityCreditCardBinding.progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : CreditCardActivity : requestPayment : VolleyError : " + error.toString());
                Constants.showToastInMiddle(getApplicationContext(), "Please enter valid credentials");
               // Toast.makeText(getApplicationContext(), "Please enter valid credentials", Toast.LENGTH_LONG).show();
            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put(Constants.VARIABLES.WAREHOUSE_KEY, mSharedPreferenceManager.getWarehouseId());
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

    /*void createSession() {
     *//*binding.startButton.setEnabled(false);
        binding.createSessionProgress.setVisibility(View.VISIBLE);*//*

        apiController.createSession(new CreateSessionCallback());
    }*/
    public void requestCreateSession() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
 /*       JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("order_id", Integer.parseInt(OrderId));
        mJsonObject.put("payment_method_id", 51);
        mJsonObject.put("payment_type_id", 2);
        mJsonObject.put("payment_method_name", "Credit / Debit Card");
        mJsonObject.put("card_number", mActivityCreditCardBinding.edtCardNumber.getText().toString());
        mJsonObject.put("exp_month", expMonth);
        mJsonObject.put("exp_year", expYear);
        mJsonObject.put("sec_code", mActivityCreditCardBinding.edtCvv.getText().toString());
        System.out.println("Rahul : CreditCardActivity : requestPayment : mJsonObject : " + mJsonObject);*/
        mActivityCreditCardBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        // System.out.println("Rahul : CreditCardActivity : requestPayment : param : " + mJsonObject);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                "https://ap-gateway.mastercard.com/api/rest/version/53/merchant/000008047730/session", null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        mActivityCreditCardBinding.progressSpinKitView.setVisibility(View.GONE);
                        System.out.println("Rahul : CreditCardActivity : requestCreateSession : onResponse : response : " + response);

                        GatewayMap mGatewayMap = new GatewayMap(response.toString());

        /*if (!response.containsKey("session")) {
            throw new RuntimeException("Could not read gateway response");
        }

        if (!response.containsKey("gatewayResponse.result") || !"SUCCESS".equalsIgnoreCase((String) response.get("gatewayResponse.result"))) {
            throw new RuntimeException("Create session result: " + response.get("gatewayResponse.result"));
        }*/

                        String apiVersion = (String) mGatewayMap.get("session.version");
                        String sessionId = (String) mGatewayMap.get("session.id");
                        session_Id = sessionId;
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mActivityCreditCardBinding.progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : CreditCardActivity : requestCreateSession : VolleyError : " + error.toString());
                Constants.showToastInMiddle(getApplicationContext(), "Please enter valid credentials");
                //Toast.makeText(getApplicationContext(), "Please enter valid credentials", Toast.LENGTH_LONG).show();
            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");

                String basicAuth = "merchant.000008047730" + ':' + "e10638a7b1c22c87b56b87d208715389";
                System.out.println("Rahul : ApiController : makeJsonRequest : basicAuth : " + basicAuth);
                basicAuth = Base64.encodeToString(basicAuth.getBytes(), Base64.DEFAULT);
                headers.put("Authorization", "Basic " + basicAuth);
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

    public void requestUpdateSessionWithPayersData(String argSessionId,
                                                   String argCardNumber,
                                                   String argMonth,
                                                   String argYear,
                                                   String argCvv) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        JSONObject mJsonObjectParam = new JSONObject();
        mJsonObjectParam.put("sourceOfFunds", new JSONObject()
                .put("type", "CARD").put("provided", new JSONObject().put("card", new JSONObject()
                        .put("number", argCardNumber).put("expiry", new JSONObject()
                                .put("month", argMonth).put("year", argYear)).put("securityCode", argCvv))
                ));


        System.out.println("Rahul : CreditCardActivity : requestPayment : mJsonObjectParam : " + mJsonObjectParam);

      /*  {
            "sourceOfFunds":{
            "type":"CARD",
                    "provided":{
                "card":{
                    "number":request_data["card_number"],
                            "expiry":{
                        "month":request_data["exp_month"],
                                "year":request_data["exp_year"]
                    },
                    "securityCode":request_data["sec_code"]
                }
            }
        }
        }*/

        mActivityCreditCardBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        // System.out.println("Rahul : CreditCardActivity : requestPayment : param : " + mJsonObject);
        System.out.println("Rahul : CreditCardActivity : requestUpdateSessionWithPayersData : url : " + "https://test-gateway.mastercard.com/api/rest/version/53/merchant/000008047730/session/" + argSessionId);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.PUT,
                "https://test-gateway.mastercard.com/api/rest/version/53/merchant/000008047730/session/" + argSessionId, mJsonObjectParam,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        mActivityCreditCardBinding.progressSpinKitView.setVisibility(View.GONE);
                        System.out.println("Rahul : CreditCardActivity : requestUpdateSessionWithPayersData : onResponse : response : " + response);

                        //response sample
                        /*{"merchant":"000008047730","session":{"id":"SESSION0002123219529J91303041J0","updateStatus":"SUCCESS","version":"3c5b421a02"},"sourceOfFunds":{"provided":{"card":{"brand":"VISA","expiry":{"month":"6","year":"25"},"fundingMethod":"CREDIT","number":"411111xxxxxx1111","scheme":"VISA","securityCode":"xxx"}},"type":"CARD"},"version":"53"}*/
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mActivityCreditCardBinding.progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : CreditCardActivity : requestUpdateSessionWithPayersData : VolleyError : " + error.toString());

            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");

                String basicAuth = "merchant.000008047730" + ':' + "e10638a7b1c22c87b56b87d208715389";
                System.out.println("Rahul : ApiController : makeJsonRequest : basicAuth : " + basicAuth);
                basicAuth = Base64.encodeToString(basicAuth.getBytes(), Base64.DEFAULT);
                headers.put("Authorization", "Basic " + basicAuth);
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


                mActivityCreditCardBinding.tvName.setText(name);
                mActivityCreditCardBinding.tvMobileNumber.setText(mobile);
                mActivityCreditCardBinding.tvAddress.setText(address);
            }
        }

        if (Gateway.handle3DSecureResult(requestCode, resultCode, data, null)) {
            System.out.println("Rahul : ProcessPaymentActivity : onActivityResult : 2 ");
            mActivityCreditCardBinding.progressSpinKitView.setVisibility(View.GONE);
            Constants.showToastInMiddle(getApplicationContext(), "Payment Unsuccessfull");
            //Toast.makeText(getApplicationContext(), "Payment Unsuccessfull", Toast.LENGTH_SHORT).show();
            return;
        }
    }

    private void setMonthEdtStuff() {

        mMonthArrayList.clear();
        isMonth = true;
        mMonthArrayList.add(new MonthYearModel("January"));
        mMonthArrayList.add(new MonthYearModel("February"));
        mMonthArrayList.add(new MonthYearModel("March"));
        mMonthArrayList.add(new MonthYearModel("April"));
        mMonthArrayList.add(new MonthYearModel("May"));
        mMonthArrayList.add(new MonthYearModel("June"));
        mMonthArrayList.add(new MonthYearModel("July"));
        mMonthArrayList.add(new MonthYearModel("August"));
        mMonthArrayList.add(new MonthYearModel("September"));
        mMonthArrayList.add(new MonthYearModel("October"));
        mMonthArrayList.add(new MonthYearModel("November"));
        mMonthArrayList.add(new MonthYearModel("December"));

        showBottomSheetDialogYear(mMonthArrayList);
    }

    private void setYearEdtStuff() {

        mYearArrayList.clear();
        isMonth = false;

        mYearArrayList.add(new MonthYearModel("2019"));
        mYearArrayList.add(new MonthYearModel("2020"));
        mYearArrayList.add(new MonthYearModel("2021"));
        mYearArrayList.add(new MonthYearModel("2022"));
        mYearArrayList.add(new MonthYearModel("2023"));
        mYearArrayList.add(new MonthYearModel("2024"));
        mYearArrayList.add(new MonthYearModel("2025"));
        mYearArrayList.add(new MonthYearModel("2026"));
        mYearArrayList.add(new MonthYearModel("2027"));
        mYearArrayList.add(new MonthYearModel("2028"));
        mYearArrayList.add(new MonthYearModel("2029"));
        mYearArrayList.add(new MonthYearModel("2030"));
        mYearArrayList.add(new MonthYearModel("2031"));
        mYearArrayList.add(new MonthYearModel("2032"));
        mYearArrayList.add(new MonthYearModel("2033"));
        mYearArrayList.add(new MonthYearModel("2034"));
        mYearArrayList.add(new MonthYearModel("2035"));
        mYearArrayList.add(new MonthYearModel("2036"));
        mYearArrayList.add(new MonthYearModel("2037"));
        mYearArrayList.add(new MonthYearModel("2038"));
        mYearArrayList.add(new MonthYearModel("2039"));
        mYearArrayList.add(new MonthYearModel("2040"));
        mYearArrayList.add(new MonthYearModel("2041"));


        showBottomSheetDialogYear(mYearArrayList);
    }


    public void showBottomSheetDialogYear(ArrayList<MonthYearModel> argArrayList) {
        mYearBottomSheetDialog = new BottomSheetDialog(this);
        mYearBottomSheetDialog.setContentView(R.layout.country_code_dialog_list);

        RecyclerView mYearRecyclerView = mYearBottomSheetDialog.findViewById(R.id.coountryList);
        TextView tvDialogTitle = mYearBottomSheetDialog.findViewById(R.id.tvDialogTitle);
        tvDialogTitle.setText("Select");
        mYearBottomSheetDialogAdapter = new YearBottomSheetDialogAdapter(argArrayList, this);
        RecyclerView.LayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext());
        mYearRecyclerView.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        mYearRecyclerView.setLayoutManager(mLayoutManager);
        mYearRecyclerView.setItemAnimator(new DefaultItemAnimator());
        mYearRecyclerView.setAdapter(mYearBottomSheetDialogAdapter);

        mYearBottomSheetDialog.show();

    }

    @Override
    public void passValue(String argPass) {
        if (isMonth) {

            mActivityCreditCardBinding.edtExpiryMonth.setText(argPass.split("#GoGrocery#")[0]);
            if (Integer.parseInt(argPass.split("#GoGrocery#")[1]) < 10) {
                expMonth = "0" + argPass.split("#GoGrocery#")[1];
            } else {
                expMonth = argPass.split("#GoGrocery#")[1];
            }


        } else {

            mActivityCreditCardBinding.edtExpiryYear.setText(argPass.split("#GoGrocery#")[0]);
            expYear = argPass.split("#GoGrocery#")[0].substring(2, 4);
        }

        mYearBottomSheetDialog.dismiss();

    }


    class UpdateSessionCallback implements GatewayCallback {
        @Override
        public void onSuccess(GatewayMap onSuccess) {
            // Log.i(ProcessPaymentActivity.class.getSimpleName(), "Successfully updated session");
            // mActivityCreditCardBinding.btnPayNow.setEnabled(true);
            check3dsEnrollment();

            System.out.println("Rahul : CreditCardActivity : UpdateSessionCallback : onSuccess : " + onSuccess);
        }

        @Override
        public void onError(Throwable throwable) {
            System.out.println("Rahul : CreditCardActivity : UpdateSessionCallback : onError : " + throwable.toString());

            mActivityCreditCardBinding.progressSpinKitView.setVisibility(View.GONE);
            Constants.showToastInMiddle(getApplicationContext(), throwable.getMessage());

            // Toast.makeText(getApplicationContext(), throwable.getMessage(), Toast.LENGTH_SHORT).show();
            /*Log.e(ProcessPaymentActivity.class.getSimpleName(), throwable.getMessage(), throwable);

            binding.updateSessionProgress.setVisibility(View.GONE);
            binding.updateSessionError.setVisibility(View.VISIBLE);

            showResult(R.drawable.failed, R.string.pay_error_unable_to_update_session);*/
        }
    }

    void check3dsEnrollment() {


        // generate a random 3DSecureId for testing
        String threeDSId = UUID.randomUUID().toString();
        threeDSId = threeDSId.substring(0, threeDSId.indexOf('-'));

        System.out.println("Rahul : ProcessPaymentActivity : check3dsEnrollment : threeDSId : " + threeDSId);
        System.out.println("Rahul : ProcessPaymentActivity : check3dsEnrollment : sessionId : " + sessionId);
        System.out.println("Rahul : ProcessPaymentActivity : check3dsEnrollment : AMOUNT : " + AMOUNT);
        System.out.println("Rahul : ProcessPaymentActivity : check3dsEnrollment : CURRENCY : " + CURRENCY);
        apiController.check3DSecureEnrollment(sessionId, AMOUNT, CURRENCY, threeDSId, new Check3DSecureEnrollmentCallback());
    }

    class Check3DSecureEnrollmentCallback implements ApiController.Check3DSecureEnrollmentCallback {
        @Override
        public void onSuccess(GatewayMap response) {
            // int apiVersionInt = Integer.valueOf(apiVersion);
            int apiVersionInt = 53;
            String threeDSecureId = (String) response.get("3DSecureID");

            String html = null;
            if (response.containsKey("3DSecure.authenticationRedirect.simple.htmlBodyContent")) {
                html = (String) response.get("3DSecure.authenticationRedirect.simple.htmlBodyContent");
            }

            // for API versions <= 46, you must use the summary status field to determine next steps for 3DS
            if (apiVersionInt <= 46) {
                String summaryStatus = (String) response.get("3DSecure.summaryStatus");

                if ("CARD_ENROLLED".equalsIgnoreCase(summaryStatus)) {
                    Gateway.start3DSecureActivity(CreditCardActivity.this, html);
                    return;
                }

              /*  binding.check3dsProgress.setVisibility(View.GONE);
                binding.check3dsSuccess.setVisibility(View.VISIBLE);*/
                CreditCardActivity.this.threeDSecureId = null;

                // for these 2 cases, you still provide the 3DSecureId with the pay operation
                if ("CARD_NOT_ENROLLED".equalsIgnoreCase(summaryStatus) || "AUTHENTICATION_NOT_AVAILABLE".equalsIgnoreCase(summaryStatus)) {
                    CreditCardActivity.this.threeDSecureId = threeDSecureId;
                }

                processPayment();
            }

            // for API versions >= 47, you must look to the gateway recommendation and the presence of 3DS info in the payload
            else {
                String gatewayRecommendation = (String) response.get("response.gatewayRecommendation");

                // if DO_NOT_PROCEED returned in recommendation, should stop transaction
                if ("DO_NOT_PROCEED".equalsIgnoreCase(gatewayRecommendation)) {
                  /*  binding.check3dsProgress.setVisibility(View.GONE);
                    binding.check3dsError.setVisibility(View.VISIBLE);*/

                    //showResult(R.drawable.failed, R.string.pay_error_3ds_authentication_failed);
                    return;
                }

                // if PROCEED in recommendation, and we have HTML for 3ds, perform 3DS
                if (html != null) {
                    Gateway.start3DSecureActivity(CreditCardActivity.this, html);
                    return;
                }

                CreditCardActivity.this.threeDSecureId = threeDSecureId;

                processPayment();
            }
        }

        @Override
        public void onError(Throwable throwable) {
            Log.e(CreditCardActivity.class.getSimpleName(), throwable.getMessage(), throwable);
            /*{"error":{"cause":"INVALID_REQUEST","explanation":"Value '0.00' is invalid. Transaction or order amount must be greater than zero","field":"order.amount","validationType":"INVALID"},"result":"ERROR"}*/
            System.out.println("Rahul : ProcessPaymentActivity : onError : throwable " + throwable.toString());
        /*    binding.check3dsProgress.setVisibility(View.GONE);
            binding.check3dsError.setVisibility(View.VISIBLE);*/

            // showResult(R.drawable.failed, R.string.pay_error_3ds_authentication_failed);
        }
    }

    void processPayment() {
        //binding.processPaymentProgress.setVisibility(View.VISIBLE);
        apiController.completeSession(sessionId, orderId, transactionId, AMOUNT, CURRENCY, threeDSecureId, isGooglePay, new CompleteSessionCallback());
    }

    class CompleteSessionCallback implements ApiController.CompleteSessionCallback {
        @Override
        public void onSuccess(String result) {
           /* binding.processPaymentProgress.setVisibility(View.GONE);
            binding.processPaymentSuccess.setVisibility(View.VISIBLE);

            showResult(R.drawable.success, R.string.pay_you_payment_was_successful);*/
        }

        @Override
        public void onError(Throwable throwable) {
            Log.e(CreditCardActivity.class.getSimpleName(), throwable.getMessage(), throwable);

           /* binding.processPaymentProgress.setVisibility(View.GONE);
            binding.processPaymentError.setVisibility(View.VISIBLE);

            showResult(R.drawable.failed, R.string.pay_error_processing_your_payment);*/
        }
    }

   /* @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        // handle the 3DSecure lifecycle
        System.out.println("Rahul : ProcessPaymentActivity : onActivityResult : 1 ");
      *//*  if (Gateway.handle3DSecureResult(requestCode, resultCode, data, new ThreeDSecureCallback())) {
            System.out.println("Rahul : ProcessPaymentActivity : onActivityResult : 2 ");
            return;
        }
     *//*

        super.onActivityResult(requestCode, resultCode, data);
    }*/
}
