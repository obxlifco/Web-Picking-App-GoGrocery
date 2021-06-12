package com.gogrocery.view;

import androidx.databinding.DataBindingUtil;
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
import com.gogrocery.Adapters.WalletAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Models.WalletModel.WalletData;
import com.gogrocery.Models.WalletModel.WalletModel;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityMyWalletPageBinding;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MyWalletPage extends AppCompatActivity {


    private ActivityMyWalletPageBinding mActivityMyWalletPageBinding;
    private SharedPreferenceManager mSharedPreferenceManager;
    private List<WalletData> mWalletDataList = new ArrayList<>();
    private WalletAdapter mWalletAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityMyWalletPageBinding = DataBindingUtil.setContentView(this, R.layout.activity_my_wallet_page);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());


        mActivityMyWalletPageBinding.ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        setWalletList();
        try {
            requestMyWallet();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private void setWalletList() {
        mWalletAdapter = new WalletAdapter(getApplicationContext(), mWalletDataList);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.VERTICAL, false);
        mActivityMyWalletPageBinding.rvWalletList.setLayoutManager(mLayoutManager);
        mActivityMyWalletPageBinding.rvWalletList.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        mActivityMyWalletPageBinding.rvWalletList.setItemAnimator(new DefaultItemAnimator());
        mActivityMyWalletPageBinding.rvWalletList.setAdapter(mWalletAdapter);
        mActivityMyWalletPageBinding.rvWalletList.setNestedScrollingEnabled(false);
    }

    public void requestMyWallet() throws JSONException {
        mActivityMyWalletPageBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        System.out.println("Rahul : MyWalletPage : requestMyWallet : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.MY_WALLET, null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        mActivityMyWalletPageBinding.progressSpinKitView.setVisibility(View.GONE);
                        try {
                            System.out.println("Rahul : MyWalletPage : requestMyWallet : response : " + response);
                            Gson mGson = new Gson();
                            WalletModel mWalletModel = mGson.fromJson(response.toString(), WalletModel.class);
                            System.out.println("Rahul : MyWalletPage : requestMyWallet : mWalletModel : " + mGson.toJson(mWalletModel));
                            if (mWalletModel.getStatus() == 200) {
                                mWalletDataList.addAll(mWalletModel.getData());
                                mWalletAdapter.notifyDataSetChanged();
                            }
                        } catch (Exception e) {
                            System.out.println("Rahul : MyWalletPage : requestMyWallet : Exception : " + e);

                        }

                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mActivityMyWalletPageBinding.progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : MyWalletPage : requestMyWallet : VolleyError : " + error.toString());

            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());
                headers.put("Authorization", "Token "+mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_token));
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
