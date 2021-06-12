package com.gogrocery.view;

import android.annotation.SuppressLint;
import android.app.Dialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.viewpager.widget.ViewPager;

import com.android.volley.AuthFailureError;
import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.ServerError;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.HttpHeaderParser;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.github.ybq.android.spinkit.SpinKitView;
import com.gogrocery.Adapters.SubstitutePagerAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Models.OrderListDetailsModel.OrderListDetailsModel;
import com.gogrocery.Models.OrderListDetailsModel.OrderProductsItem;
import com.gogrocery.R;
import com.google.gson.Gson;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.concurrent.TimeUnit;

public class SubstituteActivity extends AppCompatActivity {
    ViewPager subsViewPager;
    TextView tvNumberMissingItem, tv_timeRemaining, tvBtn_submitReplacement, tvBtn_notReplacement;
    ImageView ivBack, ivClose;
    LinearLayout llDone;
    String pushOrderID = "";
    SpinKitView progressSpinKitView;
    List<OrderProductsItem> orderProductsItemList = new ArrayList<>();
    OrderListDetailsModel orderListDetailsModel;
    private SharedPreferenceManager mSharedPreferenceManager;
    int count = 0;
    JSONArray jsonArrayApprovalDetails = new JSONArray();
    JSONArray jsonArrayNotApprovalDetails = new JSONArray();
    HashMap<Long, Boolean> submitProductMap = new HashMap<>();
    int submitCount = 0;
    public boolean isProcessable = true;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_substitute);

        pushOrderID = getIntent().getStringExtra("pushOrderID");
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        hideStatusBarColor();
        initView();

    }

    @SuppressLint("ClickableViewAccessibility")
    private void initView() {
        subsViewPager = findViewById(R.id.subsViewPager);
        tvNumberMissingItem = findViewById(R.id.tv_toolbarTitle);
        progressSpinKitView = findViewById(R.id.progressSpinKitView);
        tv_timeRemaining = findViewById(R.id.tv_timeRemaining);
        tvBtn_submitReplacement = findViewById(R.id.tvBtn_submitReplacement);
        tvBtn_notReplacement = findViewById(R.id.tvBtn_notReplacement);
        ivBack = findViewById(R.id.ivBack);
        ivClose = findViewById(R.id.ivClose);
        llDone = findViewById(R.id.llDone);
        Log.e("pushOrderID", "" + getIntent().getStringExtra("pushOrderID"));
/*       // setupTimerUpdate();
        if (getIntent().getStringExtra("pushOrderID") != null && !TextUtils.isEmpty(getIntent().getStringExtra("pushOrderID"))) {
            Log.e("pushOrderID", "" + getIntent().getStringExtra("pushOrderID"));

        }*/
        if (pushOrderID != null && !pushOrderID.isEmpty()) {
            try {
                if(Constants.isInternetConnected(SubstituteActivity.this)) {
                    requestOrderDetailsList();
                }else {
                    Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
                }

            } catch (JSONException e) {
                e.printStackTrace();
            }

        }
  /*      try {
            requestOrderDetailsList();
        } catch (JSONException e) {
            e.printStackTrace();
        }*/
        ivBack.setOnClickListener(v -> {

            if (jsonArrayApprovalDetails.length() > 0) {


                subsViewPager.setOnTouchListener(new View.OnTouchListener() {

                    public boolean onTouch(View arg0, MotionEvent arg1) {
                        return true;
                    }
                });


                new AlertDialog.Builder(SubstituteActivity.this)
                        .setTitle(getResources().getString(R.string.confirmation))
                        .setMessage(getResources().getString(R.string.there_are_items_added_in_the_list_please_submit_replacement))
                        .setCancelable(false)
                        // Specifying a listener allows you to take an action before dismissing the dialog.
                        // The dialog is automatically dismissed when a dialog button is clicked.
                        .setPositiveButton(R.string.yes, new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int which) {
                                subsViewPager.setOnTouchListener(null);

                                /*    try {
                                      //  requestPickerResetSendApproval();
                                    } catch (JSONException e) {
                                        e.printStackTrace();
                                    }*/
                                dialog.dismiss();
                            }
                        })

                        /*        // A null listener allows the button to dismiss the dialog and take no further action.
                                .setNegativeButton(android.R.string.no, null)*/
                        // .setIcon(android.R.drawable.ic_dialog_alert)
                        .show();
            } else {

                if (count >= 1) {
                    subsViewPager.setCurrentItem(count - 1);
                }

                subsViewPager.setOnTouchListener(null);
            }


        });
        tvBtn_notReplacement.setOnClickListener(v -> {
            if (isProcessable) {
                new AlertDialog.Builder(SubstituteActivity.this)
                        .setTitle(getResources().getString(R.string.confirmation))
                        .setMessage(getResources().getString(R.string.are_you_sure_that_you_want_to_reject_the_substitutions))
                        .setCancelable(false)
                        // Specifying a listener allows you to take an action before dismissing the dialog.
                        // The dialog is automatically dismissed when a dialog button is clicked.
                        .setPositiveButton(R.string.yes, new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int which) {

                                dialog.dismiss();
                                try {
                                    requestSubmitDontWantReplacement(jsonArrayNotApprovalDetails);
                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }

                            }
                        })

                        // A null listener allows the button to dismiss the dialog and take no further action.
                        .setNegativeButton(R.string.no, null)
                        // .setIcon(android.R.drawable.ic_dialog_alert)
                        .show();
            }

        });
        ivClose.setOnClickListener(v -> {


            Dialog mDialog = new Dialog(SubstituteActivity.this);
            mDialog.setCancelable(false);
            mDialog.setContentView(R.layout.custom_dialog_substitute);

            Button btnYes, btnNo;
            btnYes = mDialog.findViewById(R.id.btnYes);
            btnNo = mDialog.findViewById(R.id.btnNo);


            btnYes.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    try {
                        requestPickerResetSendApproval();
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


            //   Constants.showToastInMiddle(getApplicationContext(), mLoginModel.getMessage());
            // Toast.makeText(getApplicationContext(), mLoginModel.getMessage(), Toast.LENGTH_LONG).show();


        });


        tvBtn_submitReplacement.setOnClickListener(v -> {

            if (!submitProductMap.get(Long.valueOf(orderProductsItemList.get(count).getProduct().getId())) && isProcessable) {
                if (jsonArrayApprovalDetails.length() > 0) {

/*                    if(jsonArrayApprovalDetails.length()<orderProductsItemList.get(0).getShortage()){
String message = "You can add "+(orderProductsItemList.get(0).getShortage()-jsonArrayApprovalDetails.length())
                        +"more items \n Do you still want to submit ?";
                        WantSubmitDialog(message);
                    }else {*/
                    new AlertDialog.Builder(SubstituteActivity.this)
                            .setTitle(getResources().getString(R.string.confirmation))
                            .setMessage(getResources().getString(R.string.are_you_sure_that_you_want_to_accept_the_substitutions))
                            .setCancelable(false)
                            // Specifying a listener allows you to take an action before dismissing the dialog.
                            // The dialog is automatically dismissed when a dialog button is clicked.
                            .setPositiveButton(R.string.yes, new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int which) {

                                    dialog.dismiss();
                                    try {
                                        requestSubmitReplacement(jsonArrayApprovalDetails);
                                    } catch (JSONException e) {
                                        e.printStackTrace();
                                    }

                                }
                            })

                            // A null listener allows the button to dismiss the dialog and take no further action.
                            .setNegativeButton(R.string.no, null)
                            // .setIcon(android.R.drawable.ic_dialog_alert)
                            .show();



                    //  }

                }
            } else {
                AlreadySubmitDialog();
                /// Show Already submit dialog
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


    private void setupPager(List<OrderProductsItem> orderProductsItemList) {
        SubstitutePagerAdapter substitutePagerAdapter = new SubstitutePagerAdapter(getSupportFragmentManager(), 0, orderProductsItemList.size(), orderProductsItemList);
        subsViewPager.setAdapter(substitutePagerAdapter);

        subsViewPager.addOnPageChangeListener(new ViewPager.OnPageChangeListener() {
            @Override
            public void onPageScrolled(int position, float positionOffset, int positionOffsetPixels) {
                if (checkIsProcess(orderProductsItemList.get(position))) {
                    tvNumberMissingItem.setText("Missing items " + (position + 1) + " of " + orderProductsItemList.size());
                    if (position == 0) {
                        // ivBack.setBackground(getResources().getDrawable(R.drawable.ic_close_black));
                        ivBack.setVisibility(View.GONE);
                        ivClose.setVisibility(View.VISIBLE);
                    } else {
                        ivBack.setVisibility(View.VISIBLE);
                        ivClose.setVisibility(View.GONE);
                    }
                } /*else {
                    ivBack.setVisibility(View.GONE);
                    ivClose.setVisibility(View.VISIBLE);
                    Log.e("checkIsProcess", "false");
                }*/
                if (orderProductsItemList.get(position).getSubstituteNotes() != null && !orderProductsItemList.get(position).getSubstituteNotes().isEmpty()) {
                    if (orderProductsItemList.get(position).getSubstituteNotes().equalsIgnoreCase("Approve") ||
                            orderProductsItemList.get(position).getSubstituteNotes().equalsIgnoreCase("Decline")) {
                        llDone.setVisibility(View.VISIBLE);
                        isProcessable = false;
                    } else {
                        llDone.setVisibility(View.GONE);
                        isProcessable = true;
                    }
                } else {
                    llDone.setVisibility(View.GONE);
                    isProcessable = true;
                }

                if (jsonArrayApprovalDetails.length() > 0) {


                    subsViewPager.setOnTouchListener(new View.OnTouchListener() {

                        public boolean onTouch(View arg0, MotionEvent arg1) {
                            return true;
                        }
                    });


                    new AlertDialog.Builder(SubstituteActivity.this)
                            .setTitle(getResources().getString(R.string.confirmation))
                            .setMessage(getResources().getString(R.string.there_are_items_added_in_the_list_please_submit_replacement))
                            .setCancelable(false)
                            // Specifying a listener allows you to take an action before dismissing the dialog.
                            // The dialog is automatically dismissed when a dialog button is clicked.
                            .setPositiveButton(R.string.yes, new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int which) {
                                    subsViewPager.setOnTouchListener(null);

                                /*    try {
                                      //  requestPickerResetSendApproval();
                                    } catch (JSONException e) {
                                        e.printStackTrace();
                                    }*/
                                    dialog.dismiss();
                                }
                            })

                            /*        // A null listener allows the button to dismiss the dialog and take no further action.
                                    .setNegativeButton(android.R.string.no, null)*/
                            // .setIcon(android.R.drawable.ic_dialog_alert)
                            .show();
                } else {
                    subsViewPager.setOnTouchListener(null);

                }


            }

            @Override
            public void onPageSelected(int position) {
                count = position;
                Log.e("position", position + "");
                //getApprovalDetails(position+1);
                tvNumberMissingItem.setText(getResources().getString(R.string.missing_items) + (position + 1) + " "+getResources().getString(R.string.of)+" " + orderProductsItemList.size());
                setDontApprovalDetails();
            }

            @Override
            public void onPageScrollStateChanged(int state) {

            }
        });
    }

    private boolean checkIsProcess(OrderProductsItem orderProductsItem) {
        boolean isProcess = true;
        for (int i = 0; i < orderProductsItem.getSubstituteProducts().size(); i++) {
            if (orderProductsItem.getSubstituteProducts().get(i).getGrnQuantity() > 0) {
                isProcess = false;
                break;
            }
        }
        return isProcess;

    }

    /*private boolean checkIsProcess(OrderProductsItem orderProductsItem) {
        boolean isProcess = true;
        for (int i = 0; i < orderProductsItem.getSubstituteProducts().size(); i++) {
            if (orderProductsItem.getSubstituteProducts().get(i).getGrnQuantity() > 0) {
                isProcess = false;
                break;
            }
        }
    *//*    if(isProcess){
        subsViewPager.setPagingEnabled(true);
    }else{
        subsViewPager.setPagingEnabled(false);
    }*//*
    return isProcess;

}*/
    public void requestOrderDetailsList() throws JSONException {
        progressSpinKitView.setVisibility(View.VISIBLE);
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("website_id", "1");
        mJsonObject.put("order_id", pushOrderID);
        // mJsonObject.put("order_id", 2955);
        System.out.println("Rahul : SubstituteActivity : requestOrderDetailsList : " + mJsonObject);
        JsonObjectRequest mJsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL_SUBSTITUTE + Constants.API_METHODS.ORDER_LIST_DETAILS, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : SubstituteActivity : requestOrderDetailsList : response: " + response);
                        progressSpinKitView.setVisibility(View.GONE);
                        try {
                            if (response.getInt("status") == 1) {
                                Gson gson = new Gson();
                                orderListDetailsModel = gson.fromJson(response.toString(), OrderListDetailsModel.class);
                                orderProductsItemList.clear();

                                orderProductsItemList.addAll(orderListDetailsModel.getResponse().get(0).getOrderProducts());
                                for (int i = 0; i < orderProductsItemList.size(); i++) {
                                    submitProductMap.put(Long.valueOf(orderProductsItemList.get(i).getProduct().getId()), false);
                                }

                                setDontApprovalDetails();
                                if (orderListDetailsModel != null) {
                                    if (countDownTimer != null) {
                                        countDownTimer.cancel();
                                    }
                                    setupPager(orderProductsItemList);
                                    try {
                                        String[] strDiff = Constants.calculateDifferenceBWDateTime(
                                                Constants.convertUTCToDatePrintFormat(orderListDetailsModel.getResponse().get(0).getOrderProducts().get(0).getSubstituteProducts().get(0).getCreatedTime()),
                                                (getCurrentDate() + " " + Constants.getCurrentTime())
                                        ).split(",");
                                        if (Integer.parseInt(strDiff[0]) == 0 && Integer.parseInt(strDiff[1]) == 0) {
                                            if (Integer.parseInt(strDiff[2]) > orderListDetailsModel.getResponse().get(0).getSubstitute_approval_time()) {
                                                //Show times up dialog
                                                TimeFinishDialog();
                                                Log.e("Times up", "");
/*
                                                Intent i = new Intent(SubstituteActivity.this, MainActivityNew.class);
                                                startActivity(i);
                                                finish();*/

                                            } else {
                                                long t = (orderListDetailsModel.getResponse().get(0).getSubstitute_approval_time() * 60L) - ((Integer.parseInt(strDiff[2]) * 60L) + Integer.parseInt(strDiff[3]));
                                                long timeDiff = TimeUnit.SECONDS.toMillis(t);
                                                setupTimer(timeDiff);
                                            }
                                        } else {
                                            //Show times up dialog
                                            Log.e("Times up", "");
                                            TimeFinishDialog();
                                        /*    Intent i = new Intent(SubstituteActivity.this, MainActivityNew.class);
                                            startActivity(i);
                                            finish();*/
                                        }
                                    } catch (ParseException e) {
                                        e.printStackTrace();
                                    }

                                } else {
                                    Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.enter_valid_credentials));
                                    //Toast.makeText(getApplicationContext(), "Enter Valid Credentials", Toast.LENGTH_LONG).show();
                                }
                            } else {
                                Constants.showToastInMiddle(getApplicationContext(), response.getString("message"));
                                Intent i = new Intent(SubstituteActivity.this, MainActivityNew.class);
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
                progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : SubstituteActivity : requestOrderDetailsList : VolleyError : " + error.toString());
                Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.enter_valid_credentials));

                //Toast.makeText(getApplicationContext(), "Enter Valid Credentials", Toast.LENGTH_LONG).show();
            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                // headers.put("Authorization", "Token 05e6d4f06468663995554d3f6fbd95ff3888fb12");
                //System.out.println("Rahul : SubstituteActivity : Token : " + mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_token));
                return headers;
            }


        };


        // Adding request to request queue
        queue.add(mJsonObjectRequest);
    }

/*
    private void setupTimer(long timeDiff) {
        new CountDownTimer(timeDiff, 1000) {


            public void onTick(long millisUntilFinished) {
                tv_timeRemaining.setText(getResources().getString(R.string.txtTimeRemaining) +
                        " (" + String.format("%d min, %d sec",
                        TimeUnit.MILLISECONDS.toMinutes(millisUntilFinished),
                        TimeUnit.MILLISECONDS.toSeconds(millisUntilFinished) -
                                TimeUnit.MINUTES.toSeconds(TimeUnit.MILLISECONDS.toMinutes(millisUntilFinished))) + ")");
            }


            public void onFinish() {
                //Show times up dialog
                Log.e("Times up", "");
            }

        }.start();
    }
*/


    private void setupTimerUpdate() {
        //new CountDownTimer(timeDiff, 1000) {
        new CountDownTimer(60 * 10 * 1000, 1000) {

            public void onTick(long millisUntilFinished) {
                tv_timeRemaining.setText(getResources().getString(R.string.txtTimeRemaining) +
                        " (" + String.format("%d min, %d sec",
                        TimeUnit.MILLISECONDS.toMinutes(millisUntilFinished),
                        TimeUnit.MILLISECONDS.toSeconds(millisUntilFinished) -
                                TimeUnit.MINUTES.toSeconds(TimeUnit.MILLISECONDS.toMinutes(millisUntilFinished))) + ")");


            }

            public void onFinish() {
                Log.e("Times up", "");

                Intent i = new Intent(SubstituteActivity.this, MainActivityNew.class);
                startActivity(i);
                finish();

            }
        }.start();
    }

    public static String getCurrentDate() {
        return new SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(new Date());
    }


    public void setApprovalDetails(OrderProductsItem orderProductsItem, int pos) {
        jsonArrayApprovalDetails = new JSONArray();

        if (orderProductsItem.getSubstituteProducts().size() != 0) {
            for (int i = 0; i < orderProductsItem.getSubstituteProducts().size(); i++) {
                if (orderProductsItem.getSubstituteProducts().get(i).getGrnQuantity() > 0) {
                    JSONObject jsonObject = new JSONObject();
                    try {
                        jsonObject.put("product_id", orderProductsItemList.get(pos).getProduct().getId());
                        jsonObject.put("substitute_product_id", orderProductsItem.getSubstituteProducts().get(i).getProduct().getId());
                        jsonObject.put("order_product_id", orderProductsItem.getSubstituteProducts().get(i).getId());
                        jsonObject.put("quantity", orderProductsItem.getSubstituteProducts().get(i).getQuantity());
                        jsonObject.put("grn_quantity", orderProductsItem.getSubstituteProducts().get(i).getGrnQuantity());
                        jsonObject.put("custom_field_name", orderProductsItem.getSubstituteProducts().get(i).getCustomFieldName());
                        jsonObject.put("custom_field_value", orderProductsItem.getSubstituteProducts().get(i).getCustomFieldValue());
                        jsonArrayApprovalDetails.put(jsonObject);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }

                //jsonArray.put(jsonObject);
            }
        }
        checkIsProcess(orderProductsItem);
        Log.e("Seleted_product", jsonArrayApprovalDetails.toString());


    }

    private JSONArray setDontApprovalDetails() {
        jsonArrayNotApprovalDetails = new JSONArray();
        if (orderProductsItemList.size() != 0) {
            if (orderProductsItemList.get(count).getSubstituteProducts().size() != 0) {
                for (int i = 0; i < orderProductsItemList.get(count).getSubstituteProducts().size(); i++) {
                    // if (orderProductsItemList.get(count).getSubstituteProducts().get(i).getGrnQuantity() > 0) {
                    JSONObject jsonObject = new JSONObject();
                    try {
                        jsonObject.put("product_id", orderProductsItemList.get(count).getProduct().getId());
                        jsonObject.put("substitute_product_id", orderProductsItemList.get(count).getSubstituteProducts().get(i).getProduct().getId());
                        jsonObject.put("order_product_id", orderProductsItemList.get(count).getSubstituteProducts().get(i).getId());
                        jsonObject.put("quantity", orderProductsItemList.get(count).getSubstituteProducts().get(i).getQuantity());
                        jsonObject.put("grn_quantity", 0);
                        jsonArrayNotApprovalDetails.put(jsonObject);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                    //  }

                    //jsonArray.put(jsonObject);
                }
            }
        }

        // checkIsProcess(orderProductsItem);
        Log.e("Seleted_product", jsonArrayNotApprovalDetails.toString());

        return jsonArrayNotApprovalDetails;

    }

    public void requestSubmitReplacement(JSONArray jsonArray) throws JSONException {
        progressSpinKitView.setVisibility(View.VISIBLE);
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        JSONObject mJsonObject = new JSONObject();
/*        {
            "website_id": 1,
                "user_id": 2,
                "order_id": 2841,
                "approval_details": [
            {
                "product_id": 10804,
                    "substitute_product_id": 13641,
                    "order_product_id": 10071,
                    "quantity": 1,
                    "grn_quantity": 3
            },
            {
                "product_id": 10804,
                    "substitute_product_id": 13642,
                    "order_product_id": 10072,
                    "quantity": 1,
                    "grn_quantity": 0
            }
    ]
        }
        */

        mJsonObject.put("website_id", 1);
        mJsonObject.put("order_id", Integer.parseInt(pushOrderID));
        //  mJsonObject.put("order_id", 2954);
        mJsonObject.put("user_id", mSharedPreferenceManager.getUserProfileDetail("token"));
        mJsonObject.put("approval_details", jsonArray);
        System.out.println("Rahul : SubstituteActivity : requestSubmitReplacement : " + mJsonObject);
        JsonObjectRequest mJsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL_SUBSTITUTE + Constants.API_METHODS.SUBMIT_SUBSTITUTE_PRODUCT, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : SubstituteActivity : requestSubmitReplacement : response: " + response);
                        progressSpinKitView.setVisibility(View.GONE);
                        Gson gson = new Gson();
                        try {
                            if (response.getInt("status") == 1) {

                                jsonArrayApprovalDetails = new JSONArray();
                                submitProductMap.put(Long.valueOf(orderProductsItemList.get(count).getProduct().getId()), true);

                                submitCount = submitCount + 1;
                                Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_SHORT).show();
                                orderProductsItemList.get(count).setSubstituteNotes("Approve");
                                if (orderProductsItemList.size() > count || count > 0) {
                                    subsViewPager.setCurrentItem(count + 1);
                                }
                                subsViewPager.setOnTouchListener(null);

                                if (orderProductsItemList.size() == submitCount) {
                                    SubmitDialog();
                                }


                            } else {
                                //  Toast.makeText(getApplicationContext(),response.getString("message"),Toast.LENGTH_SHORT).show();
                                Constants.showToastInMiddle(getApplicationContext(), response.getString("message"));
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : SubstituteActivity : requestSubmitReplacementt : VolleyError : " + error.toString());
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
                             Constants.showToastInMiddle(getApplicationContext(), message);
                            // CommonValidation.alertDialogShow(DeliveryActivity.this,getResources().getString(R.string.error),obj.getString("message"));

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    } catch (UnsupportedEncodingException e) {
                        e.printStackTrace();
                    }


                    //Toast.makeText(getApplicationContext(), "Enter Valid Credentials", Toast.LENGTH_LONG).show();
                }
            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                //headers.put("Authorization", "Token 05e6d4f06468663995554d3f6fbd95ff3888fb12");
                //System.out.println("Rahul : SubstituteActivity : Token : " + mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_token));
                return headers;
            }


        };


        // Adding request to request queue
        queue.add(mJsonObjectRequest);
    }


    public void requestSubmitDontWantReplacement(JSONArray jsonArray) throws JSONException {
        progressSpinKitView.setVisibility(View.VISIBLE);
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        JSONObject mJsonObject = new JSONObject();
/*        {
            "website_id": 1,
                "user_id": 2,
                "order_id": 2841,
                "approval_details": [
            {
                "product_id": 10804,
                    "substitute_product_id": 13641,
                    "order_product_id": 10071,
                    "quantity": 1,
                    "grn_quantity": 3
            },
            {
                "product_id": 10804,
                    "substitute_product_id": 13642,
                    "order_product_id": 10072,
                    "quantity": 1,
                    "grn_quantity": 0
            }
    ]
        }
        */

        mJsonObject.put("website_id", 1);
        mJsonObject.put("order_id", Integer.parseInt(pushOrderID));
        //  mJsonObject.put("order_id", 2954);
        mJsonObject.put("user_id", mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_token));
        mJsonObject.put("approval_details", jsonArray);
        System.out.println("Rahul : SubstituteActivity : requestSubmitReplacement : " + mJsonObject);
        JsonObjectRequest mJsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL_SUBSTITUTE + Constants.API_METHODS.SUBMIT_SUBSTITUTE_PRODUCT, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : SubstituteActivity : requestSubmitReplacement : response: " + response);
                        progressSpinKitView.setVisibility(View.GONE);
                        Gson gson = new Gson();
                        try {
                            if (response.getInt("status") == 1) {
                                orderProductsItemList.get(count).setSubstituteNotes("Decline");
                                submitProductMap.put(Long.valueOf(orderProductsItemList.get(count).getProduct().getId()), false);
                                submitCount = submitCount + 1;

                                if (orderProductsItemList.size() > count || count > 0) {
                                    subsViewPager.setCurrentItem(count + 1);
                                }
                                subsViewPager.setOnTouchListener(null);



                                Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_SHORT).show();
                                if (orderProductsItemList.size() == submitCount) {
                                    requestPickerSendNotification();

                                   /* Intent i = new Intent(SubstituteActivity.this, MainActivityNew.class);
                                    startActivity(i);
                                    finish();*/
                                }
                            } else {
                                //  Toast.makeText(getApplicationContext(),response.getString("message"),Toast.LENGTH_SHORT).show();
                                Constants.showToastInMiddle(getApplicationContext(), response.getString("message"));
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : SubstituteActivity : requestSubmitReplacementt : VolleyError : " + error.toString());
                Constants.showToastInMiddle(getApplicationContext(), "Enter Valid Credentials");

                //Toast.makeText(getApplicationContext(), "Enter Valid Credentials", Toast.LENGTH_LONG).show();
            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                //  headers.put("Authorization", "Token 05e6d4f06468663995554d3f6fbd95ff3888fb12");
                //System.out.println("Rahul : SubstituteActivity : Token : " + mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_token));
                return headers;
            }


        };


        // Adding request to request queue
        queue.add(mJsonObjectRequest);
    }

    public void requestPickerResetSendApproval() throws JSONException {
        progressSpinKitView.setVisibility(View.VISIBLE);
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        JSONObject mJsonObject = new JSONObject();

        mJsonObject.put("website_id", 1);
        mJsonObject.put("order_id", Integer.parseInt(pushOrderID));
        //  mJsonObject.put("order_id", 2954);
        System.out.println("Rahul : SubstituteActivity : requestResetSendApproval : " + mJsonObject);
        JsonObjectRequest mJsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL_SUBSTITUTE + Constants.API_METHODS.PICKER_RESET_APPROVAL, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : SubstituteActivity : requestResetSendApproval : response: " + response);
                        progressSpinKitView.setVisibility(View.GONE);
                        Gson gson = new Gson();
                        try {
                            if (response.getInt("status") == 1) {
                                Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_SHORT).show();
                                requestPickerSendNotification();
                            /*    Intent i = new Intent(SubstituteActivity.this, MainActivityNew.class);
                                startActivity(i);
                                finish();*/

                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : SubstituteActivity : requestSubmitReplacementt : VolleyError : " + error.toString());
                Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.enter_valid_credentials));

                //Toast.makeText(getApplicationContext(), "Enter Valid Credentials", Toast.LENGTH_LONG).show();
            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                // headers.put("Authorization", "Token 05e6d4f06468663995554d3f6fbd95ff3888fb12");
                System.out.println("Rahul : SubstituteActivity : Token : " + mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_token));
                return headers;
            }


        };


        // Adding request to request queue
        queue.add(mJsonObjectRequest);
    }


    public void requestPickerSendNotification() throws JSONException {
        progressSpinKitView.setVisibility(View.VISIBLE);
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        JSONObject mJsonObject = new JSONObject();

        //  mJsonObject.put("website_id", 1);
        mJsonObject.put("order_id", Integer.parseInt(pushOrderID));
        //  mJsonObject.put("order_id", 2954);
        System.out.println("Rahul : SubstituteActivity : requestSendNotification : " + mJsonObject);
        JsonObjectRequest mJsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL_SUBSTITUTE + Constants.API_METHODS.PICKER_SEND_NOTIFICATION, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : SubstituteActivity : requestSendNotification : response: " + response);
                        progressSpinKitView.setVisibility(View.GONE);
                        Gson gson = new Gson();
                        try {
                            //  if(response.getInt("status")==1){
                            //  Toast.makeText(getApplicationContext(),response.getString("message"),Toast.LENGTH_SHORT).show();
                            Intent i = new Intent(SubstituteActivity.this, MainActivityNew.class);
                            startActivity(i);
                            finish();

                            //    }
                        } catch (Exception e) {
                            e.printStackTrace();
                        }

                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : SubstituteActivity : requestSubmitReplacementt : VolleyError : " + error.toString());
                Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.enter_valid_credentials));

                //Toast.makeText(getApplicationContext(), "Enter Valid Credentials", Toast.LENGTH_LONG).show();
            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                // headers.put("Authorization", "Token 05e6d4f06468663995554d3f6fbd95ff3888fb12");
                System.out.println("Rahul : SubstituteActivity : Token : " + mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_token));
                return headers;
            }


        };


        // Adding request to request queue
        queue.add(mJsonObjectRequest);
    }


    @Override
    public void onDestroy() {
        super.onDestroy();
        if (countDownTimer != null) {
            countDownTimer.cancel();
        }
    }

    CountDownTimer countDownTimer = null;

    private void setupTimer(long timeDiff) {
        countDownTimer = new CountDownTimer(timeDiff, 1000) {


            public void onTick(long millisUntilFinished) {
                tv_timeRemaining.setText(getResources().getString(R.string.txtTimeRemaining) +
                        " (" + String.format("%d min, %d sec",
                        TimeUnit.MILLISECONDS.toMinutes(millisUntilFinished),
                        TimeUnit.MILLISECONDS.toSeconds(millisUntilFinished) -
                                TimeUnit.MINUTES.toSeconds(TimeUnit.MILLISECONDS.toMinutes(millisUntilFinished))) + ")");
            }


            public void onFinish() {
                //Show times up dialog
                Log.e("Times up", "");
                TimeFinishDialog();

            }

        }.start();
    }


    private void TimeFinishDialog() {

        new AlertDialog.Builder(SubstituteActivity.this)
                .setTitle(getResources().getString(R.string.confirmation))
                .setMessage(getResources().getString(R.string.your_session_for_substitute_product_has_been_expired))
                .setCancelable(false)


                // Specifying a listener allows you to take an action before dismissing the dialog.
                // The dialog is automatically dismissed when a dialog button is clicked.
                .setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {

                        dialog.dismiss();
                        try {
                            requestPickerSendNotification();
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                          /*  Intent i = new Intent(SubstituteActivity.this, MainActivityNew.class);
                            startActivity(i);
                            finish();*/
                    }
                }).show();

        // A null listener allows the button to dismiss the dialog and take no further action.
        // .setNegativeButton(android.R.string.no, null)
        // .setIcon(android.R.drawable.ic_dialog_alert)



    }


    private void SubmitDialog() {

        new AlertDialog.Builder(SubstituteActivity.this)
                .setTitle(getResources().getString(R.string.success))
                .setMessage(getResources().getString(R.string.you_have_successfully_added_substitute_products))
                .setCancelable(false)
                // Specifying a listener allows you to take an action before dismissing the dialog.
                // The dialog is automatically dismissed when a dialog button is clicked.
                .setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {

                        dialog.dismiss();
                        try {
                            requestPickerSendNotification();
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                      /*  Intent i = new Intent(SubstituteActivity.this, MainActivityNew.class);
                        startActivity(i);
                        finish();*/
                    }
                })

                // A null listener allows the button to dismiss the dialog and take no further action.
                //  .setNegativeButton(android.R.string.no, null)
                // .setIcon(android.R.drawable.ic_dialog_alert)
                .show();

    }

    private void AlreadySubmitDialog() {

        new AlertDialog.Builder(SubstituteActivity.this)
                .setTitle(getResources().getString(R.string.confirmation))
                .setMessage(getResources().getString(R.string.you_have_already_submitted_your_choice_for_this_product))

                // Specifying a listener allows you to take an action before dismissing the dialog.
                // The dialog is automatically dismissed when a dialog button is clicked.
                .setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {

                        dialog.dismiss();

                    }
                })

                // A null listener allows the button to dismiss the dialog and take no further action.
                //  .setNegativeButton(android.R.string.no, null)
                // .setIcon(android.R.drawable.ic_dialog_alert)
                .show();

    }


}
