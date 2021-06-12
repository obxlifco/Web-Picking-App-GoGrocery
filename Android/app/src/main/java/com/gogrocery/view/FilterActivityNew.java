package com.gogrocery.view;

import android.content.Intent;
import android.graphics.Point;
import android.os.Bundle;
import android.view.Display;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;

import androidx.appcompat.app.AppCompatActivity;
import androidx.databinding.DataBindingUtil;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.Volley;
import com.gogrocery.Adapters.FilterLeftSideMenuAdapter;
import com.gogrocery.Adapters.FilterRightSideMenuAdapter;
import com.gogrocery.Adapters.FilterRightSideMenuOldAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.FilterMenuConnectInterface;
import com.gogrocery.Interfaces.FilterRightMenuInterface;
import com.gogrocery.Models.FilterModel.Child;
import com.gogrocery.Models.FilterModel.FilterModel;
import com.gogrocery.Models.FilterModel.FilterModelMain;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityFilterBinding;
import com.gogrocery.databinding.FilterDialogBinding;
import com.google.gson.Gson;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class FilterActivityNew extends AppCompatActivity implements FilterMenuConnectInterface, FilterRightMenuInterface {

    FilterDialogBinding mActivityFilterBinding;
    private SharedPreferenceManager mSharedPreferenceManager;
    private FilterLeftSideMenuAdapter mFilterLeftSideMenuAdapter;
    private List<FilterModel> mFilterModelList = new ArrayList<>();
    private List<Child> mChidList = new ArrayList<>();
    private FilterRightSideMenuAdapter mRightSideMenuAdapter;


    private String mJSONQuery = "";
    private JSONObject mJSONElasticQuery;
    private String gte = "", lte = "";
    public static String mFilterType;
    private String brandFilter = "";


    private DatabaseHandler mDatabaseHandler;

    @Override
    public void onResume() {
        super.onResume();
        Window window = this.getWindow();
        Display display = getWindowManager().getDefaultDisplay();
        Point size = new Point();
        display.getSize(size);
        double width = size.x * 0.9;
        double height = size.y * 0.9;
/*        int width = getResources().getDimensionPixelSize(R.dimen.width_dialogFragment_chat);
        int height = getResources().getDimensionPixelSize(R.dimen.height_dialogFragment_chat);*/
        window.setLayout(Integer.parseInt(String.format("%.0f", width)), Integer.parseInt(String.format("%.0f", height)));
        window.setBackgroundDrawable(getResources().getDrawable(R.drawable.bg_dialog_fragment));

    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityFilterBinding = DataBindingUtil.setContentView(this, R.layout.filter_dialog);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        mDatabaseHandler = new DatabaseHandler(getApplicationContext());
        getBundelExtra();
        setSideMenuFilterCategory();
        setRightSideMenuFilterCategory();


        mActivityFilterBinding.ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                finish();
            }
        });

        mActivityFilterBinding.btnCancel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        mActivityFilterBinding.tvClearAll.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                Constants.VARIABLES.mFilterAddedList.clear();
                Constants.VARIABLES.categoryFilterList.clear();
                Constants.VARIABLES.priceFilterList.clear();
                Constants.VARIABLES.brandFilterList.clear();
                Constants.VARIABLES.sizeFilterList.clear();
                Constants.VARIABLES.discountFilterList.clear();

                Intent intent = new Intent();
                intent.putExtra("getFilterQuery", "clear");
                setResult(1, intent);
                finish();
            }
        });
        mActivityFilterBinding.btnApplyFilter.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                System.out.println("Rahul : FilterActivity : btnApplyFilter : mSizeList : size : " + Constants.VARIABLES.sizeFilterList.size());
                //System.out.println("Rahul : FilterActivity : btnApplyFilter : mSizeList : mSizeList.toString() : " + mSizeList.toString().replace("[", "").replace("]", ""));

                try {

                    System.out.println("Rahul : FilterActivity : btnApplyFilter : mPriceRangeList : " + Constants.VARIABLES.priceFilterList.size());
                    if (Constants.VARIABLES.sizeFilterList.size() > 0) {
                        System.out.println("Rahul : FilterActivity : btnApplyFilter : mSizeList : 1");

                        try {
                            mJSONElasticQuery.getJSONObject("query").getJSONObject("bool").getJSONArray("must")
                                    .put(new JSONObject().put("match", new JSONObject().put("custom_fields.field_name", new JSONObject().put("query", "Size").put("operator", "or"))))
                                    .put(new JSONObject().put("match", new JSONObject().put("custom_fields.value", new JSONObject().put("query", Constants.VARIABLES.sizeFilterList.toString().replace("[", "").replace("]", "")).put("operator", "or"))));

                        } catch (JSONException e) {
                            e.printStackTrace();
                            System.out.println("Rahul : FilterActivity : btnApplyFilter : mSizeList : 2");

                        }
                    }
                    if (Constants.VARIABLES.priceFilterList.size() > 0) {
                        System.out.println("Rahul : FilterActivity : btnApplyFilter : mPriceRangeList : 3");

                        for (int i = 0; i < Constants.VARIABLES.priceFilterList.size(); i++) {
                            try {
                                String gteInner = Constants.VARIABLES.priceFilterList.get(i).split("-")[0];
                                String lteInner = Constants.VARIABLES.priceFilterList.get(i).split("-")[1];

                                if (gteInner.equals("0")) {
                                    mJSONElasticQuery.getJSONObject("query").getJSONObject("bool").getJSONArray("must").put(new JSONObject().put("range", new JSONObject().put("channel_currency_product_price.new_default_price", new JSONObject().put("gt", gteInner).put("lte", lteInner))));

                                } else {
                                    mJSONElasticQuery.getJSONObject("query").getJSONObject("bool").getJSONArray("must").put(new JSONObject().put("range", new JSONObject().put("channel_currency_product_price.new_default_price", new JSONObject().put("gte", gteInner).put("lte", lteInner))));

                                }
                            } catch (JSONException e) {
                                System.out.println("Rahul : FilterActivity : btnApplyFilter : mPriceRangeList : 4");
                                e.printStackTrace();
                            } catch (IndexOutOfBoundsException e) {
                                try {
                                    String gteInner = Constants.VARIABLES.priceFilterList.get(i).split("-")[0];
                                    mJSONElasticQuery.getJSONObject("query").getJSONObject("bool").getJSONArray("must").put(new JSONObject().put("range", new JSONObject().put("channel_currency_product_price.new_default_price", new JSONObject().put("gte", gteInner))));
                                } catch (JSONException e1) {
                                    e1.printStackTrace();
                                }

                            }
                        }
                    }

                    if (Constants.VARIABLES.brandFilterList.size() > 0) {
                        System.out.println("Rahul : FilterActivity : btnApplyFilter : brandFilterList : 5" + Constants.VARIABLES.brandFilterList.toString());
                        JSONArray mJsonArrayBranFIlter = new JSONArray();
                        for (int i = 0; i < Constants.VARIABLES.brandFilterList.size(); i++) {
                            mJsonArrayBranFIlter.put(Integer.parseInt(Constants.VARIABLES.brandFilterList.get(i)));
                        }
                        try {
                            //  mJSONElasticQuery.getJSONObject("query").getJSONObject("bool").getJSONArray("must").put(new JSONObject().put("match", new JSONObject().put("brand_slug", new JSONObject().put("query", Constants.VARIABLES.brandFilterList.toString().replace("[", "").replace("]", "")).put("operator", "or"))));
                            // mJSONElasticQuery.getJSONObject("query").getJSONObject("bool").getJSONArray("must").put(new JSONObject().put("terms", new JSONObject().put("brand_id", mJsonArrayBranFIlter)));
                            mJSONElasticQuery.getJSONObject("query").getJSONObject("bool").getJSONArray("must").put(new JSONObject().put("terms", new JSONObject().put("brand_id", mJsonArrayBranFIlter)));
                        } catch (JSONException e) {
                            System.out.println("Rahul : FilterActivity : btnApplyFilter : brandFilterList : 6");

                            e.printStackTrace();
                        }
                    }

                    if (Constants.VARIABLES.categoryFilterList.size() > 0) {
                        JSONArray mJsonArraycategoryFilterList = new JSONArray();
                        for (int i = 0; i < Constants.VARIABLES.categoryFilterList.size(); i++) {
                            mJsonArraycategoryFilterList.put(Integer.parseInt(Constants.VARIABLES.categoryFilterList.get(i)));
                        }
                        try {
                            // mJSONElasticQuery.getJSONObject("query").getJSONObject("bool").getJSONArray("must").put(new JSONObject().put("match", new JSONObject().put("category_slug", new JSONObject().put("query", Constants.VARIABLES.categoryFilterList.toString().replace("[", "").replace("]", "")).put("operator", "or"))));

                            mJSONElasticQuery.getJSONObject("query").getJSONObject("bool").getJSONArray("must").put(new JSONObject().put("terms", new JSONObject().put("category_id", mJsonArraycategoryFilterList)));

                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }


                System.out.println("Rahul : FilterActivity : btnApplyFilter : mJSONElasticQuery : " + mJSONElasticQuery);
                Intent intent = new Intent();
                intent.putExtra("getFilterQuery", mJSONElasticQuery.toString());
                setResult(1, intent);
                finish();
            }

        });
    }

    private void getBundelExtra() {
        String argSlug = getIntent().getExtras().getString("slug");

        mJSONQuery = getIntent().getExtras().getString("json_query");
        try {
            mJSONElasticQuery = new JSONObject(mJSONQuery);
        } catch (JSONException e) {

        }

        if (!getIntent().getExtras().getString("term_base64").isEmpty()) {
            String mTermBase64 = getIntent().getExtras().getString("term_base64");
            try {
                requestSearchFilter(mTermBase64);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        } else {
            try {
                Constants.VARIABLES.FILTER_TYPE = "category";
                requestFilter(argSlug);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }

    }

    private void setSideMenuFilterCategory() {
        mFilterLeftSideMenuAdapter = new FilterLeftSideMenuAdapter(getApplicationContext(), mFilterModelList, this);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.VERTICAL, false);
        mActivityFilterBinding.rvSideMenuCategory.setLayoutManager(mLayoutManager);
        mActivityFilterBinding.rvSideMenuCategory.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        mActivityFilterBinding.rvSideMenuCategory.setItemAnimator(new DefaultItemAnimator());
        mActivityFilterBinding.rvSideMenuCategory.setAdapter(mFilterLeftSideMenuAdapter);
        mActivityFilterBinding.rvSideMenuCategory.setNestedScrollingEnabled(false);
    }

    private void setRightSideMenuFilterCategory() {
        mRightSideMenuAdapter = new FilterRightSideMenuAdapter(getApplicationContext(), mChidList, this, this);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.VERTICAL, false);
        mActivityFilterBinding.rvRightMenu.setLayoutManager(mLayoutManager);
        // mActivityFilterBinding.rvRightMenu.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        mActivityFilterBinding.rvRightMenu.setItemAnimator(new DefaultItemAnimator());
        mActivityFilterBinding.rvRightMenu.setAdapter(mRightSideMenuAdapter);
        mActivityFilterBinding.rvRightMenu.setNestedScrollingEnabled(false);
    }

    public void requestFilter(String argSlug) throws JSONException {
        mActivityFilterBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        System.out.println("Rahul : FilterActivity : requestFilter : url : " + Constants.BASE_URL + Constants.API_METHODS.LISTING_FILTERS + "?slug=" + argSlug + "&type=" + Constants.VARIABLES.FILTER_TYPE + "&warehouse_id=" + mSharedPreferenceManager.getWarehouseId() + "&website_id=1");
        //Constants.BASE_URL + Constants.API_METHODS.LISTING_FILTERS + "?slug=" + argSlug + "&warehouse_id=" + argWarehouseid + "&website_id=" + argWebsiteid
        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.LISTING_FILTERS + "?slug=" + argSlug + "&type=" + Constants.VARIABLES.FILTER_TYPE + "&warehouse_id=" + mSharedPreferenceManager.getWarehouseId() + "&website_id=1", null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        System.out.println("Rahul : FilterActivity : requestFilter : response : " + response);
                        Gson mGson = new Gson();
                        try {

                            JSONObject mJsonObject = new JSONObject();
                            mJsonObject.put("Filter", response);
                            System.out.println("Rahul : FilterActivity : requestFilter : mJsonObject : " + mJsonObject);
                            FilterModelMain filterModelMain = mGson.fromJson(mJsonObject.toString(), FilterModelMain.class);

                            if (filterModelMain.getmFilterModel().size() == 0) {

                            } else {
                                //   mActivityFilterBinding.menuDividerBelow.setVisibility(View.VISIBLE);

                                for (int i = 0; i < filterModelMain.getmFilterModel().size(); i++) {
                                    if (filterModelMain.getmFilterModel().get(i).getChild().size() > 0) {
                                        if (!filterModelMain.getmFilterModel().get(i).getFieldName().equalsIgnoreCase("price") && !filterModelMain.getmFilterModel().get(i).getFieldName().equalsIgnoreCase("categories")) {
                                            FilterModel mFilterModel = new FilterModel(filterModelMain.getmFilterModel().get(i).getFieldName(), filterModelMain.getmFilterModel().get(i).getChild());
                                            mFilterModelList.clear();
                                            mFilterModelList.add(mFilterModel);
                                        }
                                    }
                                }

                                //mFilterModelList.addAll(filterModelMain.getmFilterModel());
                                System.out.println("Rahul : FilterActivity : requestFilter : mFilterModelList : " + mGson.toJson(mFilterModelList));

                                System.out.println("Rahul : FilterActivity : requestFilter : mFilterModelList : get(0) : " + mGson.toJson(mFilterModelList.get(0)));

                                for (int i = 0; i < mFilterModelList.size(); i++) {
                                    if (mFilterModelList.get(i).getChild().size() > 0) {
                                        if (mFilterModelList.get(i).getFieldName().equalsIgnoreCase("brand")) {
                                            FilterModel mFilterModel = mGson.fromJson(mGson.toJson(mFilterModelList.get(i)), FilterModel.class);
                                            mChidList.clear();
                                            mChidList.addAll(mFilterModel.getChild());
                                            mFilterType = mFilterModelList.get(i).getFieldName();
                                        }
                                    }
                                }

                           /*     FilterModel mFilterModel = mGson.fromJson(mGson.toJson(mFilterModelList.get(0)), FilterModel.class);
                                mChidList.clear();
                                mChidList.addAll(mFilterModel.getChild());
                                mFilterType = mFilterModelList.get(0).getFieldName();*/

                                mRightSideMenuAdapter.notifyDataSetChanged();
                                mFilterLeftSideMenuAdapter.notifyDataSetChanged();
                            }


                        } catch (JSONException e) {
                            e.getCause();
                            e.printStackTrace();
                        } catch (NullPointerException e) {

                        }

                        mActivityFilterBinding.progressSpinKitView.setVisibility(View.GONE);

                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                System.out.println("Rahul : FilterActivity : requestFilter : VolleyError : " + error.toString());
                mActivityFilterBinding.progressSpinKitView.setVisibility(View.GONE);
            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put(Constants.VARIABLES.WAREHOUSE_KEY, mSharedPreferenceManager.getWarehouseId());
                // headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                return headers;
            }


        };


        // Adding request to request queue
        queue.add(jsonArrayRequest);
    }

    public void requestSearchFilter(String argTermBase64) throws JSONException {
        mActivityFilterBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        System.out.println("Rahul : FilterActivity : requestSearchFilter : argTermBase64 : " + Constants.BASE_URL + Constants.API_METHODS.SEARCH_FILTER + "?v=" + argTermBase64);

        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.SEARCH_FILTER + "?v=" + argTermBase64, null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        System.out.println("Rahul : FilterActivity : requestSearchFilter : response : " + response);
                        Gson mGson = new Gson();
                        try {

                            JSONObject mJsonObject = new JSONObject();
                            mJsonObject.put("Filter", response);
                            System.out.println("Rahul : FilterActivity : requestSearchFilter : mJsonObject : " + mJsonObject);
                            FilterModelMain filterModelMain = mGson.fromJson(mJsonObject.toString(), FilterModelMain.class);

                            if (filterModelMain.getmFilterModel().size() == 0) {

                            } else {
                                mActivityFilterBinding.menuDividerBelow.setVisibility(View.VISIBLE);

                                for (int i = 0; i < filterModelMain.getmFilterModel().size(); i++) {
                                    if (filterModelMain.getmFilterModel().get(i).getChild().size() > 0) {
                                        if (!filterModelMain.getmFilterModel().get(i).getFieldName().equalsIgnoreCase("Price")) {
                                            FilterModel mFilterModel = new FilterModel(filterModelMain.getmFilterModel().get(i).getFieldName(), filterModelMain.getmFilterModel().get(i).getChild());
                                            mFilterModelList.add(mFilterModel);
                                        }/* else if (!filterModelMain.getmFilterModel().get(i).getFieldName().equalsIgnoreCase("sort_by")) {
                                            FilterModel mFilterModel = new FilterModel(filterModelMain.getmFilterModel().get(i).getFieldName(), filterModelMain.getmFilterModel().get(i).getChild());
                                            mFilterModelList.add(mFilterModel);
                                        }*/
                                    }


                                }

                                for (int i = 0; i < mFilterModelList.size(); i++) {

                                    if (mFilterModelList.get(i).getFieldName().equalsIgnoreCase("sort_by")) {
                                        mFilterModelList.remove(i);
                                    }

                                }


                                //mFilterModelList.addAll(filterModelMain.getmFilterModel());
                                System.out.println("Rahul : FilterActivity : requestSearchFilter : mFilterModelList : " + mGson.toJson(mFilterModelList));

                                System.out.println("Rahul : FilterActivity : requestSearchFilter : mFilterModelList : get(0) : " + mGson.toJson(mFilterModelList.get(0)));

                                FilterModel mFilterModel = mGson.fromJson(mGson.toJson(mFilterModelList.get(0)), FilterModel.class);
                                mChidList.clear();
                                mChidList.addAll(mFilterModel.getChild());
                                mFilterType = mFilterModelList.get(0).getFieldName();

                                mRightSideMenuAdapter.notifyDataSetChanged();
                                mFilterLeftSideMenuAdapter.notifyDataSetChanged();
                            }


                        } catch (JSONException e) {
                            e.getCause();
                            e.printStackTrace();
                        } catch (NullPointerException e) {

                        }


                        mActivityFilterBinding.progressSpinKitView.setVisibility(View.GONE);
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mActivityFilterBinding.progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : FilterActivity : requestSearchFilter : VolleyError : " + error.toString());

            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put(Constants.VARIABLES.WAREHOUSE_KEY, mSharedPreferenceManager.getWarehouseId());
                //headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                return headers;
            }


        };


        // Adding request to request queue
        queue.add(jsonArrayRequest);
    }

    @Override
    public void connectLeftToRight(int argPosition, String argChildJson, String argFilterType) {
        System.out.println("Rahul : FilterActivity : connectLeftToRight : argChildJson : " + argChildJson);
        Gson mGson = new Gson();
        FilterModel mFilterModel = mGson.fromJson(argChildJson, FilterModel.class);
        mChidList.clear();
        mChidList.addAll(mFilterModel.getChild());
        mFilterType = argFilterType;

        mFilterLeftSideMenuAdapter.notifyDataSetChanged();
        mRightSideMenuAdapter.notifyDataSetChanged();

    }

    @Override
    public void addFilters(String argFilterType, String argFilterListString, String argAction) {

        System.out.println("Rahul : FilterActivity : addFilters : argFilterType : " + argFilterType);
        System.out.println("Rahul : FilterActivity : addFilters : mFilterType : " + mFilterType);
        System.out.println("Rahul : FilterActivity : addFilters : argFilterListString : " + argFilterListString);
        System.out.println("Rahul : FilterActivity : addFilters : argAction : " + argAction);

        switch (mFilterType.toLowerCase()) {
            case "size":
                if (argAction.equals("add")) {
                    Constants.VARIABLES.sizeFilterList.add(argFilterListString);
                } else {
                    Constants.VARIABLES.sizeFilterList.remove(argFilterListString);
                }
                break;
            case "price":
                System.out.println("Rahul : FilterActivity : addFilters : contains : " + Constants.VARIABLES.priceFilterList.contains(argFilterListString));
                if (argAction.equals("add")) {
                 /*   lte = argFilterListString.split("-")[1];
                    gte = argFilterListString.split("-")[0];*/
                    Constants.VARIABLES.priceFilterList.add(argFilterListString);
                } else {
                   /* lte = "";
                    gte = "";*/
                    Constants.VARIABLES.priceFilterList.remove(argFilterListString);
                }

                System.out.println("Rahul : FilterActivity : addFilters : priceFilterList : " + Constants.VARIABLES.priceFilterList.toString());

                break;
            case "brand":
                if (argAction.equals("add")) {
                    Constants.VARIABLES.brandFilterList.add(argFilterListString);

                } else {
                    Constants.VARIABLES.brandFilterList.remove(argFilterListString);

                }

                break;
            case "categories":
                if (argAction.equals("add")) {
                    Constants.VARIABLES.categoryFilterList.add(argFilterListString);

                } else {
                    Constants.VARIABLES.categoryFilterList.remove(argFilterListString);

                }

                break;
        }

    }

    @Override
    protected void onStop() {
        super.onStop();
    }
}
