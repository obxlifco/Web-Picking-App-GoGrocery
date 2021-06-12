package com.gogrocery.view;

import android.content.Intent;
import androidx.databinding.DataBindingUtil;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.LinearLayoutManager;
import android.view.View;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.gogrocery.Adapters.SaveListAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.SaveListInterface;
import com.gogrocery.Models.SaveListModel.SaveListAddModel;
import com.gogrocery.Models.SaveListModel.SaveListData;
import com.gogrocery.Models.SaveListModel.SaveListModel;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivitySaveListPageBinding;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SaveListPage extends AppCompatActivity implements SaveListInterface {

    private ActivitySaveListPageBinding mActivitySaveListPageBinding;
    private SharedPreferenceManager mSharedPreferenceManager;
    private DatabaseHandler mDatabaseHandler;
    private String action = "create";
    private String save_list_id_for_edit = "";
    public String product_id = "";

    private SaveListAdapter mSaveListAdapter;
    private List<SaveListData> mSaveListDataList = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivitySaveListPageBinding = DataBindingUtil.setContentView(this, R.layout.activity_save_list_page);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        mDatabaseHandler = new DatabaseHandler(getApplicationContext());
        if (getIntent().getExtras() == null) {

            mActivitySaveListPageBinding.tvListingTitle.setText("My Save List");
            mActivitySaveListPageBinding.tvAddNew.setVisibility(View.VISIBLE);
            mActivitySaveListPageBinding.txtCNL.setVisibility(View.GONE);
            mActivitySaveListPageBinding.txtMSL.setVisibility(View.GONE);
            mActivitySaveListPageBinding.cvCreate.setVisibility(View.GONE);

        } else {
            product_id = getIntent().getExtras().getString("product_id");
        }

        setSaveList();

        mActivitySaveListPageBinding.btnCreate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                try {
                    if (mActivitySaveListPageBinding.edtSaveListName.getText().toString().isEmpty()) {
                        mActivitySaveListPageBinding.edtSaveListName.setError("Should not be empty");
                    } else {

                        switch (action) {
                            case "edit":
                                requestEditSaveList();
                                break;
                            case "create":
                                requestAddCreateSaveList(product_id);
                                break;

                        }

                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });

        mActivitySaveListPageBinding.ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        mActivitySaveListPageBinding.tvAddNew.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                action = "create";
                mActivitySaveListPageBinding.edtSaveListName.setText("");
                mActivitySaveListPageBinding.btnCreate.setText("CREATE & ADD");
                mActivitySaveListPageBinding.txtCNL.setVisibility(View.VISIBLE);
                mActivitySaveListPageBinding.txtMSL.setVisibility(View.VISIBLE);
                mActivitySaveListPageBinding.cvCreate.setVisibility(View.VISIBLE);

            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        try {
            requestSaveList();
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }

    private void setSaveList() {
        mSaveListAdapter = new SaveListAdapter(this, mSaveListDataList, this);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.VERTICAL, false);
        mActivitySaveListPageBinding.rvMySaveList.setLayoutManager(mLayoutManager);
        //mActivitySaveListPageBinding.rvMySaveList.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        mActivitySaveListPageBinding.rvMySaveList.setItemAnimator(new DefaultItemAnimator());
        mActivitySaveListPageBinding.rvMySaveList.setAdapter(mSaveListAdapter);
        mActivitySaveListPageBinding.rvMySaveList.setNestedScrollingEnabled(false);
    }


    public void requestSaveList() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        mActivitySaveListPageBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.SAVE_LIST, null,
                new com.android.volley.Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        mActivitySaveListPageBinding.progressSpinKitView.setVisibility(View.GONE);
                        try {
                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            System.out.println("Rahul : SaveListPage : requestSaveList : mJsonObject : " + mJsonObject);
                            if (response.getString("status").equals("1")) {
                                mActivitySaveListPageBinding.txtMSL.setVisibility(View.VISIBLE);
                                mSaveListDataList.clear();
                                SaveListModel mSaveListModel = mGson.fromJson(mJsonObject.toString(), SaveListModel.class);
                                mSaveListDataList.addAll(mSaveListModel.getData());
                                mSaveListAdapter.notifyDataSetChanged();
                                //Toast.makeText(getApplicationContext(), response.getString("msg"), Toast.LENGTH_LONG).show();

                            } else {

                                mActivitySaveListPageBinding.txtMSL.setVisibility(View.GONE);
                                mSaveListDataList.clear();
                                SaveListModel mSaveListModel = mGson.fromJson(mJsonObject.toString(), SaveListModel.class);
                                mSaveListDataList.addAll(mSaveListModel.getData());
                                mSaveListAdapter.notifyDataSetChanged();

                             //   Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();

                            }
                        } catch (JSONException e) {
                            e.printStackTrace();

                        }

                    }
                }, new com.android.volley.Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : MainActivityNew : requestAddToCart : VolleyError : " + error.toString());
                mActivitySaveListPageBinding.progressSpinKitView.setVisibility(View.GONE);

            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());
                headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));

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

    public void requestAddCreateSaveList(String argProductId) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        JSONObject mParam = new JSONObject();

        mParam.put("website_id", 1);
        mParam.put("name", mActivitySaveListPageBinding.edtSaveListName.getText().toString());
        if (product_id.isEmpty()) {

        } else {
            mParam.put("product_id", argProductId);
        }


        System.out.println("Rahul : SaveListPage : requestAddCreateSaveList : mParam : " + mParam);

        mActivitySaveListPageBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.SAVE_LIST, mParam,
                new com.android.volley.Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            mActivitySaveListPageBinding.progressSpinKitView.setVisibility(View.GONE);
                            System.out.println("Rahul : SaveListPage : requestAddCreateSaveList : mJsonObject : " + response);
                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                mActivitySaveListPageBinding.edtSaveListName.setText("");
                              //  Toast.makeText(getApplicationContext(), R.string.error_try_again_later, Toast.LENGTH_LONG).show();

                               /* SaveListModel mSaveListModel=new SaveListModel();
                                mSaveListDataList.addAll(mSaveListModel.getData());
                                mSaveListAdapter.notifyDataSetChanged();*/
                                requestSaveList();

                            } else {
                                Toast.makeText(getApplicationContext(), R.string.error_try_again_later, Toast.LENGTH_LONG).show();

                            }
                        } catch (JSONException e) {
                            e.printStackTrace();

                        }

                    }
                }, new com.android.volley.Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : SaveListPage : requestAddCreateSaveList : VolleyError : " + error.toString());
                mActivitySaveListPageBinding.progressSpinKitView.setVisibility(View.GONE);

            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());
                headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));

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

    public void requestAddProductToSaveList(String argSaveListId, String argAction) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        JSONObject mParam = new JSONObject();

        mParam.put("website_id", 1);
        mParam.put("product_id", product_id);
        mParam.put("action", argAction);
        mParam.put("list_id", argSaveListId);
        System.out.println("Rahul : SaveListPage : requestAddProductSaveList : mJsonObject : " + mParam);

        mActivitySaveListPageBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.PUT,
                Constants.BASE_URL + Constants.API_METHODS.ADD_PRODUCT_TO_SAVE_LIST, mParam,
                new com.android.volley.Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            mActivitySaveListPageBinding.progressSpinKitView.setVisibility(View.GONE);

                            Gson mGson = new Gson();
                            JSONObject mJsonObject = null;

                            mJsonObject = new JSONObject(response.toString());

                            System.out.println("Rahul : SaveListPage : requestAddProductSaveList : mJsonObject : " + mJsonObject);
                            SaveListAddModel saveListAddModel = mGson.fromJson(response.toString().trim(), SaveListAddModel.class);
                            if (saveListAddModel.getStatus() == Integer.parseInt(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                requestSaveList();
                            } else {
                                Toast.makeText(SaveListPage.this, "Error", Toast.LENGTH_SHORT).show();
                            }


                        } catch (JSONException e) {
                            e.printStackTrace();


                        }
                    }


                }, new com.android.volley.Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : SaveListPage : requestAddCreateSaveList : VolleyError : " + error.toString());
                mActivitySaveListPageBinding.progressSpinKitView.setVisibility(View.GONE);

            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());
                headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));

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

    public void requestDeleteSaveList(String argSaveListId) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        /*JSONObject mParam = new JSONObject();

        mParam.put("website_id", 1);
        mParam.put("product_id", argProductId);
        mParam.put("action", argProductId);
        mParam.put("name", mActivitySaveListPageBinding.edtSaveListName.getText().toString());*/


        mActivitySaveListPageBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.DELETE,
                Constants.BASE_URL + Constants.API_METHODS.DELETE_SINGLE_SAVE_LIST + argSaveListId + "/", null,
                new com.android.volley.Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {

                        mActivitySaveListPageBinding.progressSpinKitView.setVisibility(View.GONE);
                        try {



                            Gson mGson = new Gson();
                            JSONObject mJsonObject = null;

                            mJsonObject = new JSONObject(response.toString());

                            System.out.println("Rahul : SaveListPage : requestAddProductSaveList : mJsonObject : " + mJsonObject);
                            SaveListAddModel saveListAddModel = mGson.fromJson(response.toString().trim(), SaveListAddModel.class);
                            if (saveListAddModel.getStatus() == Integer.parseInt(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                requestSaveList();
                            } else {
                                Toast.makeText(SaveListPage.this, "Error", Toast.LENGTH_SHORT).show();
                            }


                        } catch (Exception e) {
                            e.printStackTrace();
                        }

                    }
                }, new com.android.volley.Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : SaveListPage : requestAddCreateSaveList : VolleyError : " + error.toString());
                mActivitySaveListPageBinding.progressSpinKitView.setVisibility(View.GONE);

            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());
                headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));

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

    public void requestEditSaveList() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        JSONObject mParam = new JSONObject();

        mParam.put("name", mActivitySaveListPageBinding.edtSaveListName.getText().toString());
        mParam.put("savelist_id", save_list_id_for_edit);

        System.out.println("Rahul : SaveListPage : requestEditSaveList : mParam : " + mParam);

        mActivitySaveListPageBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.PUT,
                Constants.BASE_URL + Constants.API_METHODS.EDIT_SINGLE_SAVE_LIST_NAME, mParam,
                new com.android.volley.Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            System.out.println("Rahul : SaveListPage : requestEditSaveList : mJsonObject : " + response);

                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {

                                requestSaveList();
                            } else {
                               // Toast.makeText(getApplicationContext(), R.string.error_try_again_later, Toast.LENGTH_LONG).show();

                            }
                        } catch (Exception e) {
                            e.printStackTrace();

                        }

                    }
                }, new com.android.volley.Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : SaveListPage : requestEditSaveList : VolleyError : " + error.toString());
                mActivitySaveListPageBinding.progressSpinKitView.setVisibility(View.GONE);

            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());
                headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));

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
    public void getInfo(String argInfo, String argAction) {


        // mActivitySaveListPageBinding.edtSaveListName.setText(argInfo);
        action = argAction;

        switch (argAction) {

            case "add":
                if (product_id.isEmpty()) {

                } else {
                    try {
                        requestAddProductToSaveList(argInfo.split("#GoGrocery#")[0], "add");
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }

                break;
            case "delete":
                try {
                    requestDeleteSaveList(argInfo);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                break;
            case "edit":
                save_list_id_for_edit = argInfo.split("#GoGrocery#")[1];
                mActivitySaveListPageBinding.btnCreate.setText("Update");
                mActivitySaveListPageBinding.edtSaveListName.setText(argInfo.split("#GoGrocery#")[0]);
                mActivitySaveListPageBinding.txtCNL.setVisibility(View.VISIBLE);
                mActivitySaveListPageBinding.txtMSL.setVisibility(View.VISIBLE);
                mActivitySaveListPageBinding.cvCreate.setVisibility(View.VISIBLE);

                break;
            case "slug":
                Intent saveListDetail = new Intent(SaveListPage.this, SaveListDetailListPage.class);
                saveListDetail.putExtra("slug", argInfo);
                startActivity(saveListDetail);

                break;
        }
    }

    @Override
    public void redirectToDetail(String argSlug) {

    }
}
