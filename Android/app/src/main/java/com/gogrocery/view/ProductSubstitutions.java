package com.gogrocery.view;

import androidx.appcompat.app.AppCompatActivity;
import androidx.databinding.DataBindingUtil;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.LinearLayoutManager;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.gogrocery.Adapters.MyOrdersHistoryAdapter;
import com.gogrocery.Adapters.ProductSubstituteAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Interfaces.gotoSubstituteList;
import com.gogrocery.Models.MyOrdersHistoryModel.Data;
import com.gogrocery.Models.MyOrdersHistoryModel.MyOrdersHistoryModel;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityProductSubstitutionsBinding;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ProductSubstitutions extends AppCompatActivity implements gotoSubstituteList {
ActivityProductSubstitutionsBinding productSubstitutionsBinding;
    private SharedPreferenceManager mSharedPreferenceManager;
    private List<Data> mMyOrdersHistoryList = new ArrayList<>();
    private ProductSubstituteAdapter mMyOrdersHistoryAdapter;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        productSubstitutionsBinding = DataBindingUtil.setContentView(this,R.layout.activity_product_substitutions);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        productSubstitutionsBinding.ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

/*
        productSubstitutionsBinding.rlBadge.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(ProductSubstitutions.this, MyCart.class);
                startActivity(i);
                finish();
            }
        });
*/

  /*      productSubstitutionsBinding.ivCart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent ivCart = new Intent(ProductSubstitutions.this, MyCart.class);
                startActivity(ivCart);
            }
        });*/

 /*       if (Constants.VARIABLES.CART_COUNT > 0) {
            productSubstitutionsBinding.badgeNotification.setVisibility(View.VISIBLE);
            productSubstitutionsBinding.badgeNotification.setText("" + Constants.VARIABLES.CART_COUNT);
        } else {
            productSubstitutionsBinding.rlBadge.setVisibility(View.GONE);
        }*/
        setViewCartRecyclerView();

        try {
            requestProductSubstitutionList();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }


    private void setViewCartRecyclerView() {
        mMyOrdersHistoryAdapter = new ProductSubstituteAdapter(getApplicationContext(), mMyOrdersHistoryList, this);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.VERTICAL, false);
        productSubstitutionsBinding.rvMyOrdersRecyclerView.setLayoutManager(mLayoutManager);
        //mActivityMyOrdersBinding.rvMyOrdersRecyclerView.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        productSubstitutionsBinding.rvMyOrdersRecyclerView.setItemAnimator(new DefaultItemAnimator());
        productSubstitutionsBinding.rvMyOrdersRecyclerView.setAdapter(mMyOrdersHistoryAdapter);
        productSubstitutionsBinding.rvMyOrdersRecyclerView.setNestedScrollingEnabled(false);
    }

    public void requestProductSubstitutionList() throws JSONException {
        productSubstitutionsBinding.progressSpinKitView.setVisibility(View.VISIBLE);


        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        System.out.println("Rahul : MyOrdersFragmentPresent : requestMyOrdersHistoryList : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.ORDER_HISTORY + "?req_type=substitute", null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            productSubstitutionsBinding.progressSpinKitView.setVisibility(View.GONE);
                            mMyOrdersHistoryList.clear();
                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            System.out.println("Rahul : MyOrdersFragmentPresent : requestMyOrdersHistoryList : mJsonObject : " + mJsonObject);
                            if (response.getInt("status") == 204) {
                                productSubstitutionsBinding.noSubstituteProduct.setVisibility(View.VISIBLE);
                                productSubstitutionsBinding.rvMyOrdersRecyclerView.setVisibility(View.GONE);
                                Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_SHORT).show();
                            } else {
                                productSubstitutionsBinding.noSubstituteProduct.setVisibility(View.GONE);
                                productSubstitutionsBinding.rvMyOrdersRecyclerView.setVisibility(View.VISIBLE);
                                MyOrdersHistoryModel mMyOrdersHistoryModel = mGson.fromJson(mJsonObject.toString(), MyOrdersHistoryModel.class);
                                mMyOrdersHistoryList.addAll(mMyOrdersHistoryModel.getData());

                                mMyOrdersHistoryAdapter.notifyDataSetChanged();
                            }


                        } catch (Exception e) {
                            System.out.println("Rahul : MyOrdersFragmentPresent : requestMyOrdersHistoryList : Exception : " + e.toString());
                            productSubstitutionsBinding.somethingwentwrong.setVisibility(View.VISIBLE);
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                productSubstitutionsBinding.progressSpinKitView.setVisibility(View.GONE);
                productSubstitutionsBinding.somethingwentwrong.setVisibility(View.VISIBLE);
                System.out.println("Rahul : MyOrdersFragmentPresent : requestMyOrdersHistoryList : VolleyError : " + error.toString());

            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
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
    public void onSelectedItem(String orderId) {
        Intent i = new Intent(ProductSubstitutions.this, SubstituteActivity.class);
        i.putExtra("pushOrderID", orderId);
        startActivity(i);
    }
}