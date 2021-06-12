package com.gogrocery.Fragment;

import android.content.Intent;
import androidx.databinding.DataBindingUtil;
import android.os.Bundle;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.LinearLayoutManager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
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
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.PaymentPageRedirectionInterface;
import com.gogrocery.Models.MyOrdersHistoryModel.Data;
import com.gogrocery.Models.MyOrdersHistoryModel.MyOrdersHistoryModel;
import com.gogrocery.view.MyOrders;
import com.gogrocery.view.MyOrdersDetailPage;
import com.gogrocery.R;
import com.gogrocery.databinding.MyOrdersFragmentBinding;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MyOrdersFragmentPast extends Fragment implements PaymentPageRedirectionInterface {

    public MyOrdersFragmentPast() {
        // Required empty public constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }


    private MyOrdersFragmentBinding mMyOrdersFragmentBinding;
    private SharedPreferenceManager mSharedPreferenceManager;
    private DatabaseHandler mDatabaseHandler;
    private List<Data> mMyOrdersHistoryList = new ArrayList<>();
    private MyOrdersHistoryAdapter mMyOrdersHistoryAdapter;
    private String order_req_type = "";

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        mMyOrdersFragmentBinding = DataBindingUtil.inflate(
                inflater, R.layout.my_orders_fragment, container, false);
        View view = mMyOrdersFragmentBinding.getRoot();
        mSharedPreferenceManager = new SharedPreferenceManager(getContext());


        setMyOrdersList();
        try {
            requestMyOrdersHistoryList();
        } catch (JSONException e) {
            e.printStackTrace();
        }
//        order_req_type = getArguments().getString("order_req_type");

        return view;


    }

    private void setMyOrdersList() {
        mMyOrdersHistoryAdapter = new MyOrdersHistoryAdapter(getContext(), mMyOrdersHistoryList, this);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getContext(), LinearLayoutManager.VERTICAL, false);
        mMyOrdersFragmentBinding.rvMyOrdersRecyclerView.setLayoutManager(mLayoutManager);
        //mActivityMyOrdersBinding.rvMyOrdersRecyclerView.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        mMyOrdersFragmentBinding.rvMyOrdersRecyclerView.setItemAnimator(new DefaultItemAnimator());
        mMyOrdersFragmentBinding.rvMyOrdersRecyclerView.setAdapter(mMyOrdersHistoryAdapter);
        mMyOrdersFragmentBinding.rvMyOrdersRecyclerView.setNestedScrollingEnabled(false);
    }

    public void requestMyOrdersHistoryList() throws JSONException {
        mMyOrdersFragmentBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        String mOrderType = "";
        int tabPosition = ((MyOrders) getActivity()).tabSelected;
        System.out.println("Rahul : MyOrdersFragmentPast : requestMyOrdersHistoryList : tabPosition : " + tabPosition);
        if (tabPosition == 1) {
            mOrderType = "present";
        } else {
            mOrderType = "past";
        }


        RequestQueue queue = Volley.newRequestQueue(getContext());
        System.out.println("Rahul : MyOrdersFragmentPast : requestMyOrdersHistoryList : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.ORDER_HISTORY + "?req_type=past", null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            mMyOrdersFragmentBinding.progressSpinKitView.setVisibility(View.GONE);
                            mMyOrdersHistoryList.clear();
                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            System.out.println("Rahul : MyOrdersFragmentPast : requestMyOrdersHistoryList : mJsonObject : " + mJsonObject);
                            if (response.getInt("status") == 204) {

                                //Toast.makeText(getContext(), response.getString("message"), Toast.LENGTH_SHORT).show();
                            } else {
                                MyOrdersHistoryModel mMyOrdersHistoryModel = mGson.fromJson(mJsonObject.toString(), MyOrdersHistoryModel.class);
                                mMyOrdersHistoryList.addAll(mMyOrdersHistoryModel.getData());

                                mMyOrdersHistoryAdapter.notifyDataSetChanged();
                            }

                        } catch (Exception e) {
                            mMyOrdersFragmentBinding.somethingwentwrong.setVisibility(View.VISIBLE);
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mMyOrdersFragmentBinding.progressSpinKitView.setVisibility(View.GONE);
                mMyOrdersFragmentBinding.somethingwentwrong.setVisibility(View.VISIBLE);
                System.out.println("Rahul : MyOrdersFragmentPast : requestMyOrdersHistoryList : VolleyError : " + error.toString());

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


    public void requestOrderCancel(String argOrderId, int argPosition) throws JSONException {
        mMyOrdersFragmentBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        RequestQueue queue = Volley.newRequestQueue(getContext());
        System.out.println("Rahul : MyOrdersFragmentPast : requestOrderCancel : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
        System.out.println("Rahul : MyOrdersFragmentPast : requestOrderCancel : argOrderId : " + argOrderId);

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.CANCEL_ORDER + argOrderId + "/", null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : MyOrdersFragmentPast : requestOrderCancel : response : " + response);
                        mMyOrdersFragmentBinding.progressSpinKitView.setVisibility(View.GONE);
                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        try {
                            if (mJsonObject.getString("status").equals("200")) {
                              /*  mMyOrdersHistoryList.remove(argPosition);
                                mMyOrdersHistoryAdapter.notifyItemRemoved(argPosition);
                                mMyOrdersHistoryAdapter.notifyItemRangeChanged(argPosition, mMyOrdersHistoryList.size());*/
                                mMyOrdersHistoryList.get(argPosition).setStrOrderStatus("Cancelled");
                                mMyOrdersHistoryAdapter.notifyDataSetChanged();
                                Toast.makeText(getContext(), "Order cancelled successfully", Toast.LENGTH_LONG).show();

                            } else {
                                Toast.makeText(getContext(), "Something wrong! Try again later", Toast.LENGTH_LONG).show();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mMyOrdersFragmentBinding.progressSpinKitView.setVisibility(View.GONE);
                mMyOrdersFragmentBinding.somethingwentwrong.setVisibility(View.VISIBLE);
                System.out.println("Rahul : MyOrdersFragmentPast : requestOrderCancel : VolleyError : " + error.toString());

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

    @Override
    public void redirect(String argOrderId, String argOrderDetail) {

    }

    @Override
    public void redirectTODetailPage(String argOrderId, String cust_order_id, String argOrderDetail) {
        Intent i = new Intent(getActivity(), MyOrdersDetailPage.class);
        i.putExtra("orders_id", argOrderId);
        i.putExtra("cust_orders_id", cust_order_id);
        i.putExtra("order_detail", argOrderDetail);
        startActivity(i);
    }

    @Override
    public void requestForCancelOrder(String argOrderId, int argPosition) {

    }

    @Override
    public void onResume() {
        super.onResume();
        System.out.println("Rahul : MyOrdersFragmentPast : onResume : ");
    }

    @Override
    public void onPause() {
        super.onPause();
        System.out.println("Rahul : MyOrdersFragmentPast : onPause : ");
    }

    @Override
    public void onDetach() {
        super.onDetach();
        System.out.println("Rahul : MyOrdersFragmentPast : onDetach : ");
    }

    @Override
    public void onStop() {
        super.onStop();
        System.out.println("Rahul : MyOrdersFragmentPast : onStop : ");
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        System.out.println("Rahul : MyOrdersFragmentPast : onDestroyView : ");
    }
}