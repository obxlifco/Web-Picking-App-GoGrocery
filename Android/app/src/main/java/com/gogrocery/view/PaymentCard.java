package com.gogrocery.view;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;
import androidx.databinding.DataBindingUtil;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Toast;

import com.afollestad.materialdialogs.MaterialDialog;
import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.gogrocery.Adapters.MyCardAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Interfaces.PaymentCardInterface;
import com.gogrocery.Models.MyCardList.Card;
import com.gogrocery.Models.MyCardList.CardListModel;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityPaymentCardBinding;
import com.gogrocery.helper.SwipeHelper;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class PaymentCard extends AppCompatActivity implements PaymentCardInterface {
ActivityPaymentCardBinding paymentCardBinding;
    private SharedPreferenceManager mSharedPreferenceManager;
    private MyCardAdapter myCardAdapter;
    private List<Card> mCardList = new ArrayList<>();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        paymentCardBinding= DataBindingUtil.setContentView(this,R.layout.activity_payment_card);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        hideStatusBarColor();
        try {
            requestMyCardList();
        } catch (JSONException e) {
            e.printStackTrace();
        }



        paymentCardBinding.ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
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

    private void setCardPaymentListRecyclerView() {
        myCardAdapter = new MyCardAdapter(getApplicationContext(), mCardList, this,"payment");
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.VERTICAL, false);
        paymentCardBinding.rvPaymentCardList.setLayoutManager(mLayoutManager);
      /*  mActivityDeliveryDetailBinding.rvPaymentTypes.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        paymentCardBinding.rvPaymentTypes.setItemAnimator(new DefaultItemAnimator());*/
        paymentCardBinding.rvPaymentCardList.setAdapter(myCardAdapter);
        paymentCardBinding.rvPaymentCardList.setNestedScrollingEnabled(false);
        SwipeHelper swipeHelper = new SwipeHelper(this,  paymentCardBinding.rvPaymentCardList) {
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
                                    showRemovePopup(mCardList.get(pos).getId());
                                  //  requestRemoveList(mCardList.get(pos).getId());
                                } catch (Exception e) {
                                    e.printStackTrace();
                                }
                                //deleteOrderItem(pos);
                            }
                        }
                ));
            }
        };
    }



    private void showRemovePopup(String id) {
        new MaterialDialog.Builder(this)
                .title("Remove Card")
                .content("Do you want to remove this card?")
                .positiveText(getApplicationContext().getResources().getString(R.string.confirm))
                .positiveColor(ContextCompat.getColor(getApplicationContext(), R.color.app_red_clr))
                .negativeText(getApplicationContext().getResources().getString(R.string.dialogPositiveButtonText_cancel))
                .negativeColor(ContextCompat.getColor(getApplicationContext(), R.color.black))
                .onPositive((dialog, which) -> {

                    try {
                        requestRemoveList(id);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                })
                .onNegative((dialog, which) -> {
                    dialog.dismiss();
                }).show();
    }


    @Override
    public void onSelectedCard(String cardNo,String argSI) {

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
                                    paymentCardBinding.rlNoCardFound.setVisibility(View.GONE);
                                 /*   Card mCard= new Card();
                                    mCard.setCardSuffix("");
                                    mCard.setCardType("Add New Payment Method");
                                    mCard.setSiSubRefNo("0");
                                    mCardList.add(mCard);*/
                                    setCardPaymentListRecyclerView();

                                    System.out.println("Rahul : DeliveryDetail : requestDeliverySlot : requestCardList : size : " + mCardListModel.getCardList().size());

                                }else {
                                    paymentCardBinding.rlNoCardFound.setVisibility(View.VISIBLE);
                                    mCardList.clear();
                                    setCardPaymentListRecyclerView();

                                    //Toast.makeText(getApplicationContext(), "No Card added in your list", Toast.LENGTH_LONG).show();
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



    public void requestRemoveList(String id) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        findViewById(R.id.progressSpinKitView).setVisibility(View.VISIBLE);
        System.out.println("Rahul : PaymentCard : requestCardRemoveList : Url : " + Constants.BASE_URL + Constants.API_METHODS.REMOVE_SAVED_CARD+
                id+"/");
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.REMOVE_SAVED_CARD+
                id+"/", null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : DeliveryDetails : requestCardList : response : " + response.toString());
                        findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                        try {
                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                // Constants.VARIABLES.SELECTED_ADDRESS_ID="";
                                try {
                                    requestMyCardList();
                                } catch (JSONException e) {
                                    e.printStackTrace();
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
}