package com.gogrocery.view;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import androidx.databinding.DataBindingUtil;
import android.os.AsyncTask;
import android.os.Build;
import android.speech.RecognizerIntent;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import androidx.recyclerview.widget.SimpleItemAnimator;

import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.view.inputmethod.EditorInfo;
import android.widget.TextView;

import com.android.volley.AuthFailureError;
import com.android.volley.RequestQueue;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.facebook.appevents.AppEventsConstants;
import com.gogrocery.Adapters.SearchAdapter;
import com.gogrocery.Adapters.SearchPageListAdapter;
import com.gogrocery.Adapters.ShopByCategoryAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.ActivityRedirection;
import com.gogrocery.Interfaces.BSP_ItemClick_Interface;
import com.gogrocery.Interfaces.PrepareViewOpenInterface;
import com.gogrocery.Interfaces.ProductListingInterface;
import com.gogrocery.Interfaces.SearchActivityLoadingInterface;
import com.gogrocery.Interfaces.SingleStringPassingInterface;
import com.gogrocery.Models.CartModel.AddToCartModel;
import com.gogrocery.Models.ElasticSearch.Hit;
import com.gogrocery.Models.ElasticSearch.SearchModel;
import com.gogrocery.Models.ProductQuantityLocal;
import com.gogrocery.Models.RecentSearchModel;
import com.gogrocery.Models.SearchPageShopByCategory;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivitySearchBinding;
import com.google.android.flexbox.FlexDirection;
import com.google.android.flexbox.FlexboxLayoutManager;
import com.google.android.flexbox.JustifyContent;
import com.google.firebase.analytics.FirebaseAnalytics;
import com.google.gson.Gson;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.concurrent.TimeUnit;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.RequestBody;

public class SearchActivity extends AppCompatActivity implements ActivityRedirection, ProductListingInterface, SingleStringPassingInterface, SearchActivityLoadingInterface, BSP_ItemClick_Interface, PrepareViewOpenInterface {

    private List<Hit> mSearchHitList = new ArrayList<>();
    private SearchPageListAdapter mSearchPageListAdapter;
    private ActivitySearchBinding mActivitySearchBinding;
    private final int REQ_CODE_SPEECH_INPUT = 100;
    private SharedPreferenceManager mSharedPreferenceManager;
    private SearchAdapter mSearchAdapter;
    private List<String> mRecentSearchModelList = new ArrayList<>();
    private RecentSearchModel mRecentSearchModel;
    private ShopByCategoryAdapter mShopByCategoryAdapter;
    private List<String> mShopByCategoriesList = new ArrayList<>();
    private String queryPass = "";
    private List<String> argTermSearchFilter = new ArrayList<>();
    private String paramV = "";
    private GridLayoutManager mGridLayoutManager;
    private int pastVisiblesItems, visibleItemCount, totalItemCount;
    private boolean loading = true;
    private  boolean searchFilterDataLoad = false;
    private int page = 0;//Limit
  //  private LinearLayoutManager mLayoutManager;
    private String paramPassElasticQuery = "";
    private FirebaseAnalytics mFirebaseAnalytics;
    private DatabaseHandler mDatabaseHandler;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivitySearchBinding = DataBindingUtil.setContentView(this, R.layout.activity_search);
        mDatabaseHandler = new DatabaseHandler(getApplicationContext());
        mFirebaseAnalytics = FirebaseAnalytics.getInstance(this);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        mRecentSearchModel = new RecentSearchModel();
        hideStatusBarColor();
        /*setRecentSearchRecyclerView();
        setCategoryRecyclerView();*/
        searchRecentUISetup();
        shopByCategoryUISetup();
        setSearchListRecyclerView();
        /*try {
            requestCmsContent();
        } catch (JSONException e) {
            e.printStackTrace();
        }*/


        mActivitySearchBinding.ivMicrophone.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                promptSpeechInput();
            }
        });

        mActivitySearchBinding.tvSearchContent.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if (s.length() > 1) {
                    try {
                        page =0;
                        mActivitySearchBinding.noProductAvailable.setVisibility(View.GONE);
                        requestSearchListing(s.toString(), "onTextChanged");
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                } else if (s.length() < 2) {
                    page = 0;

                }
            }

            @Override
            public void afterTextChanged(Editable s) {

                page =0;
            }
        });

     /*   mActivitySearchBinding.tvSearchContent.setOnEditorActionListener(new TextView.OnEditorActionListener() {
            @Override
            public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
                Constants.VARIABLES.page_title = "search_page";
                if (actionId == EditorInfo.IME_ACTION_SEARCH) {
                    System.out.println("Rahul : SearchActivity : tvSearchContent : mRecentSearchModelList : size : " + mRecentSearchModelList.size());
                    if (mActivitySearchBinding.tvSearchContent.getText().length() != 0) {

                        if (!mRecentSearchModelList.contains(mActivitySearchBinding.tvSearchContent.getText().toString().toLowerCase())) {

                            mRecentSearchModelList.add(mActivitySearchBinding.tvSearchContent.getText().toString().toLowerCase());

                            HashSet<String> hs = new HashSet<>(mRecentSearchModelList);
                            mRecentSearchModelList.clear();
                            mRecentSearchModelList.addAll(hs);
                            mRecentSearchModel.setSearchText(mRecentSearchModelList);

                            mSharedPreferenceManager.storeRecentSearches(new Gson().toJson(mRecentSearchModel));
                        }

                        if(searchFilterDataLoad){

                        Intent tvSearchContent = new Intent(SearchActivity.this, ProductListingPage.class);
                        tvSearchContent.putExtra("PageTitle", "search_page");
                        tvSearchContent.putExtra("terms_array", argTermSearchFilter.toString());
                        tvSearchContent.putExtra("terms_base64", paramV);
                        startActivity(tvSearchContent);
                    }}

                    //idBase64Encode();
                }
                return false;
            }
        });*/

        mActivitySearchBinding.backImg.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });


        mActivitySearchBinding.rvSearchList.addOnScrollListener(new RecyclerView.OnScrollListener() {
            @Override
            public void onScrolled(RecyclerView recyclerView, int dx, int dy) {
                // Log.e(TAG, "onScrolled: " + dx + " " + dy);
//                if (dx > 0) {
                System.out.println("Rahul : ProductListingPage : addOnScrollListener : requestProductListiing : 6 : ");

                visibleItemCount = mGridLayoutManager.getChildCount();
                totalItemCount = mGridLayoutManager.getItemCount();
                pastVisiblesItems = mGridLayoutManager.findFirstVisibleItemPosition();


                System.out.println("Rahul : ProductListingPage : addOnScrollListener : visibleItemCount : " + visibleItemCount);
                System.out.println("Rahul : ProductListingPage : addOnScrollListener : totalItemCount : " + totalItemCount);
                System.out.println("Rahul : ProductListingPage : addOnScrollListener : pastVisiblesItems : " + pastVisiblesItems);

                // Log.e(TAG, "onScrolled: " + loading);
                if (loading) {
                    System.out.println("Rahul : ProductListingPage : addOnScrollListener : requestProductListiing : 7 : ");

                    //  Log.e(TAG, "onScrolled2: ");
                    if ((visibleItemCount + pastVisiblesItems) >= totalItemCount) {
                        System.out.println("Rahul : ProductListingPage : addOnScrollListener : requestProductListiing : 8 : ");

                        Log.v("...", "Last Item Wow !");

                        //loading = false;
                        page = page + 18;
                        try {
                            System.out.println("Rahul : ProductListingPage : addOnScrollListener : requestProductListiing : 9 : ");

                            System.out.println("Rahul : ProductListingPage : addOnScrollListener : requestProductListiing : page : " + page);

                            /*JSONObject mJsonObject = new JSONObject(paramPassElasticQuery);
                            mJsonObject.remove("from");
                            mJsonObject.put("from", page);
                            paramPassElasticQuery = mJsonObject.toString();*/
                            //System.out.println("Rahul : ProductListingPage : addOnScrollListener : requestProductListiing : paramPassElasticQuery : " + paramPassElasticQuery);
                            requestSearchListing(mActivitySearchBinding.tvSearchContent.getText().toString(), "onScrolled");
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }


                    }
                }
//            }
            }
        });


        mActivitySearchBinding.ivFav.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent ivCart = new Intent(SearchActivity.this, MyCart.class);
                startActivity(ivCart);
            }
        });

        if (Constants.VARIABLES.CART_COUNT > 0) {
            mActivitySearchBinding.tvCartCount.setVisibility(View.VISIBLE);
            mActivitySearchBinding.tvCartCount.setText("" + Constants.VARIABLES.CART_COUNT);
        } else {
            mActivitySearchBinding.tvCartCount.setVisibility(View.GONE);
        }
    }

    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }

/*    private void footerViewLastLoading() {
        if (loading) {
            System.out.println("Rahul : ProductListingPage : requestProductListiing : 7 : ");

            //  Log.e(TAG, "onScrolled2: ");
            if ((visibleItemCount + pastVisiblesItems) >= totalItemCount) {
                System.out.println("Rahul : ProductListingPage : requestProductListiing : 8 : ");

                Log.v("...", "Last Item Wow !");

                //loading = false;
                page = page + 18;
                try {
                    System.out.println("Rahul : ProductListingPage : requestProductListiing : 9 : ");

                    System.out.println("Rahul : ProductListingPage : onCreate : requestProductListiing : page : " + page);

                          *//*  JSONObject mJsonObject = new JSONObject(paramPassElasticQuery);
                            mJsonObject.remove("from");
                            mJsonObject.put("from", page);
                            paramPassElasticQuery = mJsonObject.toString();*//*
                    System.out.println("Rahul : ProductListingPage : onCreate : requestProductListiing : paramPassElasticQuery : " + paramPassElasticQuery);
                    requestSearchListing(mActivitySearchBinding.tvSearchContent.getText().toString());
                } catch (JSONException e) {
                    e.printStackTrace();
                }


            }
        }
    }*/

    public void idBase64Encode() {
        System.out.println("Rahul : SearchActivity : requestSearchListing : argTermSearchFilter : " + argTermSearchFilter);
        //System.out.println("Rahul : SearchActivity : requestSearchListing : argTermSearchFilter : " + argTermSearchFilter.toArray().toString());
        String idBase64Encode = argTermSearchFilter.toString().replace("[", "").replace("]", "").replace("\"", "");

        byte[] data1 = idBase64Encode.getBytes(StandardCharsets.UTF_8);
        paramV = android.util.Base64.encodeToString(data1, android.util.Base64.NO_WRAP);

    }

    private void searchRecentUISetup() {


        if (!mSharedPreferenceManager.getRecentSearch().isEmpty()) {
            System.out.println("Rahul : SearchActivity : searchRecentUISetup : mRecentSearchList : " + mSharedPreferenceManager.getRecentSearch());
            RecentSearchModel mRecentSearch = new Gson().fromJson(mSharedPreferenceManager.getRecentSearch(), RecentSearchModel.class);
            mRecentSearchModelList = mRecentSearch.getSearchText();
            mActivitySearchBinding.txtRS.setVisibility(View.VISIBLE);
            mActivitySearchBinding.v2.setVisibility(View.VISIBLE);
            setRecentSearchRecyclerView();
        } else {
            mActivitySearchBinding.txtRS.setVisibility(View.GONE);
            mActivitySearchBinding.v2.setVisibility(View.GONE);
        }


    }

    private void shopByCategoryUISetup() {


        if (!mSharedPreferenceManager.getShopByCategory().isEmpty()) {
            SearchPageShopByCategory mSearchPageShopByCategory = new Gson().fromJson(mSharedPreferenceManager.getShopByCategory(), SearchPageShopByCategory.class);
            mShopByCategoriesList = mSearchPageShopByCategory.getSearchText();
            setCategoryRecyclerView();
        } else {

        }


    }


    /**
     * Showing google speech input dialog
     */
    private void promptSpeechInput() {
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
        intent.putExtra(RecognizerIntent.EXTRA_PROMPT,
                getString(R.string.speech_prompt));
        try {
            startActivityForResult(intent, REQ_CODE_SPEECH_INPUT);
        } catch (ActivityNotFoundException a) {

            Constants.showToastInMiddle(getApplicationContext(), getString(R.string.speech_not_supported));

            /*Toast.makeText(getApplicationContext(),
                    getString(R.string.speech_not_supported),
                    Toast.LENGTH_SHORT).show();*/
        }
    }

    /**
     * Receiving speech input
     */
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == REQ_CODE_SPEECH_INPUT) {
            if (resultCode == RESULT_OK && null != data) {

                ArrayList<String> result = data
                        .getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
                mActivitySearchBinding.tvSearchContent.setText(result.get(0));
            }
        }else {
            if(resultCode == Activity.RESULT_OK){

                try {

                    requestAddToCart(Integer.parseInt(data.getStringExtra("argProductId")), 1,data.getStringExtra("custom_field_name"),data.getStringExtra("custom_field_value"),Integer.parseInt(data.getStringExtra("position")));
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    private void setRecentSearchRecyclerView() {
        mSearchAdapter = new SearchAdapter(getApplicationContext(), mRecentSearchModelList, this);
        // LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.HORIZONTAL, false);
        FlexboxLayoutManager layoutManager = new FlexboxLayoutManager(this);
        layoutManager.setFlexDirection(FlexDirection.ROW);
        layoutManager.setJustifyContent(JustifyContent.FLEX_START);
        mActivitySearchBinding.rvRecentSearch.setLayoutManager(layoutManager);
        //mActivityMainBinding.appBarInclude.rvDealsOfTheDay.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        mActivitySearchBinding.rvRecentSearch.setItemAnimator(new DefaultItemAnimator());
        mActivitySearchBinding.rvRecentSearch.setAdapter(mSearchAdapter);
        mActivitySearchBinding.rvRecentSearch.setNestedScrollingEnabled(false);


    }


    /*private void setRecentSearchRecyclerView() {
        mSearchAdapter = new SearchAdapter(getApplicationContext(), mCms_parentCategoryLists, this);
        // LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.HORIZONTAL, false);
        FlexboxLayoutManager layoutManager = new FlexboxLayoutManager(this);
        layoutManager.setFlexDirection(FlexDirection.ROW);
        layoutManager.setJustifyContent(JustifyContent.FLEX_START);
        mActivitySearchBinding.rvRecentSearch.setLayoutManager(layoutManager);
        //mActivityMainBinding.appBarInclude.rvDealsOfTheDay.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        mActivitySearchBinding.rvRecentSearch.setItemAnimator(new DefaultItemAnimator());
        mActivitySearchBinding.rvRecentSearch.setAdapter(mSearchAdapter);
        mActivitySearchBinding.rvRecentSearch.setNestedScrollingEnabled(false);


    }

    private void setCategoryRecyclerView() {
        mSearchPageCategoryAdapter = new SearchPageCategoryAdapter(getApplicationContext(), mCms_parentCategoryLists, this);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.HORIZONTAL, false);
        mActivitySearchBinding.rvCategory.setLayoutManager(mLayoutManager);
        //mActivityMainBinding.appBarInclude.rvDealsOfTheDay.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        mActivitySearchBinding.rvCategory.setItemAnimator(new DefaultItemAnimator());
        mActivitySearchBinding.rvCategory.setAdapter(mSearchPageCategoryAdapter);
        mActivitySearchBinding.rvCategory.setNestedScrollingEnabled(false);


    }*/

    private void setSearchListRecyclerView() {
        mSearchPageListAdapter = new SearchPageListAdapter(this, mSearchHitList, this, this, this,this,mDatabaseHandler,this);
        mGridLayoutManager = new GridLayoutManager(getApplicationContext(), 2);
        mActivitySearchBinding.rvSearchList.setLayoutManager(mGridLayoutManager);
        ((SimpleItemAnimator) mActivitySearchBinding.rvSearchList.getItemAnimator()).setSupportsChangeAnimations(false);
       /*
        mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.VERTICAL, false);
        mActivitySearchBinding.rvSearchList.setLayoutManager(mLayoutManager);*/
    /*    mActivitySearchBinding.rvSearchList.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        mActivitySearchBinding.rvSearchList.setItemAnimator(new DefaultItemAnimator());*/
        mActivitySearchBinding.rvSearchList.setAdapter(mSearchPageListAdapter);
        mActivitySearchBinding.rvSearchList.setNestedScrollingEnabled(false);


    }

    private void setCategoryRecyclerView() {
        mShopByCategoryAdapter = new ShopByCategoryAdapter(getApplicationContext(), mShopByCategoriesList, this);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.HORIZONTAL, false);
        mActivitySearchBinding.rvCategory.setLayoutManager(mLayoutManager);
        //mActivityMainBinding.appBarInclude.rvDealsOfTheDay.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        mActivitySearchBinding.rvCategory.setItemAnimator(new DefaultItemAnimator());
        mActivitySearchBinding.rvCategory.setAdapter(mShopByCategoryAdapter);
        mActivitySearchBinding.rvCategory.setNestedScrollingEnabled(false);


    }


    public void requestSearchListing(String argSearchQuery, String argFrom) throws JSONException {
        if(Constants.isInternetConnected(SearchActivity.this)) {
            //     RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            JSONObject mJsonObject = new JSONObject();

            mActivitySearchBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            mJsonObject.put("table_name", "EngageboostProducts")
                    .put("website_id", 1)
                    .put("data", new JSONObject()
                            .put("query", new JSONObject()
                                    .put("bool", new JSONObject()
                                            .put("must", new JSONArray()
                                                    .put(new JSONObject().put("query_string", new JSONObject().put("query", "\"" + argSearchQuery + "\"")))
                                                    /*.put(new JSONObject().put("match", new JSONObject().put("isdeleted", "n")))
                                                    .put(new JSONObject().put("match", new JSONObject().put("isblocked", "n")))
                                                    .put(new JSONObject().put("match", new JSONObject().put("inventory.id", mSharedPreferenceManager.getWarehouseId())))*/
                                                    .put(new JSONObject().put("match", new JSONObject().put("visibility_id", new JSONObject()
                                                            .put("query", "Catalog Search")
                                                            .put("operator", "and")
                                                    )))

                                            )
                                            .put("filter", new JSONArray()
                                                    .put(new JSONObject().put("nested", new JSONObject()
                                                            .put("path", "inventory")
                                                            .put("query", new JSONObject()
                                                                    .put("bool", new JSONObject()
                                                                            .put("must", new JSONArray()
                                                                                    .put(new JSONObject()
                                                                                            .put("term", new JSONObject()
                                                                                                    .put("inventory.id", mSharedPreferenceManager.getWarehouseId())))
                                                                                    .put(new JSONObject().put("range", new JSONObject()
                                                                                            .put("inventory.stock", new JSONObject()
                                                                                                    .put("gt", 0))))
                                                                            )))
                                                            .put("score_mode", "avg")))
                                                    .put(new JSONObject().put("nested", new JSONObject()
                                                            .put("path", "channel_currency_product_price")
                                                            .put("query", new JSONObject()
                                                                    .put("bool", new JSONObject()
                                                                            .put("must", new JSONArray()

                                                                                    .put(new JSONObject()
                                                                                            .put("range", new JSONObject()
                                                                                                    .put("channel_currency_product_price.new_default_price", new JSONObject()
                                                                                                            .put("gt", 0))))
                                                                                    .put(new JSONObject()
                                                                                            .put("term", new JSONObject()
                                                                                                    .put("channel_currency_product_price.warehouse_id", mSharedPreferenceManager.getWarehouseId())))
                                                                            )))))
                                                    .put(new JSONObject().put("nested", new JSONObject()
                                                            .put("path", "product_images")
                                                            .put("query", new JSONObject()
                                                                    .put("bool", new JSONObject()
                                                                            .put("must", new JSONArray()
                                                                                    .put(new JSONObject()
                                                                                            .put("term", new JSONObject()
                                                                                                    .put("product_images.is_cover", 1)))
                                                                            )))))
                                            )
                                    )).put("from", page).put("size", 20));

            System.out.println("Rahul : SearchActivity : requestSearchListing : ParamQuery : " + mJsonObject.toString());
        /*{
            "query": {
            "bool": {
                "must": [
                {
                    "query_string": {
                    "query": "*hugg*"
                }
                },
                {
                    "match": {
                    "visibility_id": {
                        "query": "Catalog Search",
                                "operator": "and"
                    }
                }
                }
      ],
                "filter": [
                {
                    "nested": {
                    "path": "inventory",
                            "query": {
                        "bool": {
                            "must": [
                            {
                                "term": {
                                "inventory.id": 36
                            }
                            },
                            {
                                "range": {
                                "inventory.stock": {
                                    "gt": 0
                                }
                            }
                            }
                ]
                        }
                    },
                    "score_mode": "avg"
                }
                },
                {
                    "nested": {
                    "path": "channel_currency_product_price",
                            "query": {
                        "bool": {
                            "must": [
                            {
                                "range": {
                                "channel_currency_product_price.new_default_price": {
                                    "gt": 0
                                }
                            }
                            },
                            {
                                "term": {
                                "channel_currency_product_price.warehouse_id": 36
                            }
                            }
                ]
                        }
                    }
                }
                },
                {
                    "nested": {
                    "path": "product_images",
                            "query": {
                        "bool": {
                            "must": [
                            {
                                "term": {
                                "product_images.is_cover": 1
                            }
                            }
                ]
                        }
                    }
                }
                }
      ]
            }
        },
            "from": 0,
                "size": 10000
        }*/
       /* {
            "query": {
            "bool": {
                "must": [
                {
                    "query_string": {
                    "fields": [
                    "brand",
                            "name",
                            "sku",
                            "category"
            ],
                    "query": "*pamp*"
                }
                },
                {
                    "match": {
                    "visibility_id": {
                        "query": "Catalog Search",
                                "operator": "and"
                    }
                }
                },
                {
                    "match": {
                    "inventory.id": 36
                }
                },
                {
                    "match": {
                    "channel_currency_product_price.warehouse_id": 36
                }
                },
                {
                    "range": {
                    "channel_currency_product_price.new_default_price": {
                        "gt": 0
                    }
                }
                }
      ]
            }
        }
        }*/

        /*{
  "query": {
    "bool": {
      "must": [
        {
          "query_string": {
            "fields": [
              "brand",
              "name",
              "sku",
              "category"
            ],
            "query": "*joh*"
          }
        },
        {
          "match": {
            "visibility_id": {
              "query": "Catalog Search",
              "operator": "and"
            }
          }
        },
        {
          "match": {
            "inventory.id": "7"
          }
        }
      ]
    }
  }
}*/
       /* mJsonObject.put("company_website_id", 1);
        mJsonObject.put("page_id", 7);
        mJsonObject.put("lang", "en");
        mJsonObject.put("template_id", 1);
        mJsonObject.put("start_limit", 0);
        mJsonObject.put("end_limit", 70);
        mJsonObject.put("warehouse_id", 7);
*/
            String staticRes = "";

            OkHttpClient client = new OkHttpClient.Builder().connectTimeout(60, TimeUnit.SECONDS).readTimeout(60, TimeUnit.SECONDS).writeTimeout(60, TimeUnit.SECONDS).build();

            MediaType mediaType = MediaType.parse("application/json");
            RequestBody body = RequestBody.create(mediaType, mJsonObject.toString());
            okhttp3.Request request = new okhttp3.Request.Builder()
                    .url(Constants.ELASTIC_SEARCH_LISTING)
                    .get()
                    .post(body)
                    .addHeader("Content-Type", "application/json")
                    .addHeader("cache-control", "no-cache")
                    .build();

            AsyncTask<Void, Void, String> asyncTask = new AsyncTask<Void, Void, String>() {
                @Override
                protected String doInBackground(Void... params) {
                    try {
                        okhttp3.Response response = client.newCall(request).execute();
                        if (!response.isSuccessful()) {
                            return null;
                        }
                        return response.body().string();
                    } catch (Exception e) {
                        e.printStackTrace();
                        return null;
                    }
                }

                @Override
                protected void onProgressUpdate(Void... values) {
                    super.onProgressUpdate(values);
                    mActivitySearchBinding.progressSpinKitView.setVisibility(View.GONE);
                }

                @Override
                protected void onPostExecute(String s) {
                    super.onPostExecute(s);

                    Bundle params = new Bundle();
                    params.putString(FirebaseAnalytics.Param.SEARCH_TERM, argSearchQuery);
                    mFirebaseAnalytics.logEvent(FirebaseAnalytics.Event.SEARCH, params);
                    mActivitySearchBinding.progressSpinKitView.setVisibility(View.GONE);
                    Gson mGson = new Gson();
                    JSONObject mJsonObject = null;
                    try {
                        mJsonObject = new JSONObject(s);
                        SearchModel mSearchModel = mGson.fromJson(mJsonObject.toString(), SearchModel.class);
                        switch (argFrom) {
                            case "onTextChanged":
                                argTermSearchFilter.clear();
                                mSearchHitList.clear();
                                searchFilterDataLoad = false;
                                break;
                        }
                        //argTermSearchFilter.clear();
                        //mSearchHitList.clear();
                        mSearchHitList.addAll(mSearchModel.getHits().getHits());
                        for (int i = 0; i < mSearchHitList.size(); i++) {

                            argTermSearchFilter.add("\"" + mSearchHitList.get(i).getId() + "\"");
                            searchFilterDataLoad = true;

                        }
                        if (mSearchModel.getHits().getHits().size() == 0) {
                            loading = false;
                        } else {
                            loading = true;
                        }

                        idBase64Encode();

                        System.out.println("Rahul : SearchActivity : requestSearchListing : response : " + s);
                        System.out.println("Rahul : SearchActivity : requestSearchListing : mSearchModel : " + new Gson().toJson(mSearchModel));
                        System.out.println("Rahul : SearchActivity : requestSearchListing : mSearchHitList : " + new Gson().toJson(mSearchHitList));

                        // mSearchAdapter.notifyDataSetChanged();
                        //mSearchPageCategoryAdapter.notifyDataSetChanged();

                        if (mSearchHitList.size() == 0 && mSearchModel.getHits().getHits().size() == 0) {
                            //mActivitySearchBinding..setVisibility(View.VISIBLE);
                            mActivitySearchBinding.noProductAvailable.setVisibility(View.VISIBLE);
                        } else {
                            mActivitySearchBinding.noProductAvailable.setVisibility(View.GONE);
                        }
                        mSearchPageListAdapter.notifyDataSetChanged();
                    } catch (JSONException e) {
                        e.printStackTrace();
                    } catch (NullPointerException e) {

                    }


                }
            };

            asyncTask.execute();


        }else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }

    }


    @Override
    public void redirect(String argWhich, String argPageTtile) {

    }

    @Override
    public void sendSlug(String argSlug, int argProductId) {

        System.out.println("Rahul : sendSlug : mRecentSearchModelList:  " + mRecentSearchModelList.contains(queryPass));
        if (mRecentSearchModelList.contains(mActivitySearchBinding.tvSearchContent.getText().toString())) {


        } else {
            mRecentSearchModelList.add(mActivitySearchBinding.tvSearchContent.getText().toString());
            mRecentSearchModel.setSearchText(mRecentSearchModelList);

            mSharedPreferenceManager.storeRecentSearches(new Gson().toJson(mRecentSearchModel));
        }
        Intent i = new Intent(SearchActivity.this, DetailActivity.class);
        i.putExtra("slug", argSlug.split("#GoGrocery#")[0]);
        i.putExtra("title", argSlug.split("#GoGrocery#")[1]);
        i.putExtra("product_id", argProductId);
        startActivity(i);
    }

    @Override
    public void sendProductIdForWishlist(int argProductId, String argAction) {

    }

    @Override
    public void savelist(String argProductId) {

    }

    @Override
    protected void onResume() {
        super.onResume();

        if (mSearchAdapter != null) {
            mSearchAdapter.notifyDataSetChanged();
        }


        if (Constants.VARIABLES.CART_COUNT > 0) {

            mActivitySearchBinding.tvCartCount.setVisibility(View.VISIBLE);
            mActivitySearchBinding.tvCartCount.setText("" + Constants.VARIABLES.CART_COUNT);

        } else {
            mActivitySearchBinding.tvCartCount.setVisibility(View.GONE);
        }
    }

    @Override
    public void passValue(String argPass) {
        queryPass = argPass;
        mActivitySearchBinding.tvSearchContent.setText(argPass);
    }

    @Override
    public void callLoading() {
        //footerViewLastLoading();
        System.out.println("Rahul : SearchActivity : callLoading : ");
    }

    @Override
    public void connectMain(int argProductId, int argQuantity,int position) {
        try {
            requestAddToCart(argProductId, argQuantity,"","",position);
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }


    public void requestAddToCart(int argProductId, int argQty, String customFieldName,String customFieldValue,int position) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));
        mJsonObject.put("product_id", argProductId);
        mJsonObject.put("quantity", argQty);
        mJsonObject.put("year_check", mSharedPreferenceManager.getYearCheck());
        mJsonObject.put("custom_field_name", customFieldName);
        mJsonObject.put("custom_field_value", customFieldValue);
        System.out.println("Rahul : ProductListingPage : requestAddToCart : param : " + mJsonObject);
        System.out.println("Rahul : ProductListingPage : requestAddToCart : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));


        mActivitySearchBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(com.android.volley.Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.ADD_TO_CART, mJsonObject,
                new com.android.volley.Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {

                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        System.out.println("Rahul : ProductListingPage : requestAddToCart : mJsonObject : " + mJsonObject);

                        AddToCartModel mAddToCartModel = mGson.fromJson(mJsonObject.toString(), AddToCartModel.class);
                        if (mAddToCartModel.getStatus() == 1) {
                            if (argQty == 0) {
                                mDatabaseHandler.deleteSingleRecord(String.valueOf(argProductId));
                            } else {


                                Bundle params = new Bundle();
                                params.putString("productName",mAddToCartModel.getCartData().getCartdetails().get(0).getName());
                                params.putString("productId",mAddToCartModel.getCartData().getCartdetails().get(0).getId());
                                params.putString("addedQuanity",mAddToCartModel.getCartData().getCart_count());
                                params.putString("content_type","product");
                                params.putString("currency", Constants.VARIABLES.CURRENT_CURRENCY);
                                mFirebaseAnalytics.logEvent(FirebaseAnalytics.Event.ADD_TO_CART, params);
                             //   logger.logEvent(AppEventsConstants.EVENT_NAME_ADDED_TO_CART, params);
                           /* int cartItemCount = 0;
                            for (int i = 0; i < mAddToCartModel.getCartData().getCartdetails().size(); i++) {
                                cartItemCount = cartItemCount + Integer.parseInt(mAddToCartModel.getCartData().getCartdetails().get(i).getQty());

                            }*/
                                //mActivityMainBinding.appBarInclude.badgeNotification.setText("" + cartItemCount);

                                ProductQuantityLocal mProductQuantityLocal = new ProductQuantityLocal(String.valueOf(argProductId), String.valueOf(argQty));
                                if (!mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(argProductId)).equals("0")) {
                                    mDatabaseHandler.updateProductQuantityById(mProductQuantityLocal);
                                } else {
                                    mDatabaseHandler.addProductQty(mProductQuantityLocal);
                                }


                                System.out.println("Rahul : ProductListingPage : checkDbCount : " + mDatabaseHandler.getAllProductQtyData().size());
                            }

                            if (Integer.parseInt(mAddToCartModel.getCartData().getCart_count()) == 0) {
                                mActivitySearchBinding.tvCartCount.setVisibility(View.GONE);
                                // mActivityItemListingBinding.badgeNotification.setVisibility(View.GONE);

                            } else {
                                Constants.VARIABLES.CART_COUNT = Integer.parseInt(mAddToCartModel.getCartData().getCart_count());
                                Constants.VARIABLES.CART_SUB_AMOUNT = Constants.twoDecimalRoundOff(mAddToCartModel.getCartData().getOrderamountdetails().get(0).getSubTotal());
                                mActivitySearchBinding.tvCartCount.setVisibility(View.VISIBLE);
                                mActivitySearchBinding.tvCartCount.setText(mAddToCartModel.getCartData().getCart_count());

                            }


                        } else {

                            try {
                                if(response.getString("is_age_verification").equals("False")) {
                                    Intent i = new Intent(SearchActivity.this, TobacoCatActivity.class);
                                    i.putExtra("message", mAddToCartModel.getMsg());
                                    startActivity(i);
                                }else{
                                    Constants.showToastInMiddle(getApplicationContext(), mAddToCartModel.getMsg());
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }


                            //Toast.makeText(getApplicationContext(), mAddToCartModel.getMsg(), Toast.LENGTH_LONG).show();

                        }
                       // mSearchPageListAdapter.notifyDataSetChanged();
                        mSearchPageListAdapter.notifyItemChanged(position);
                        mActivitySearchBinding.progressSpinKitView.setVisibility(View.GONE);

                    }
                }, new com.android.volley.Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : ProductListingPage : requestAddToCart : VolleyError : " + error.toString());
                mActivitySearchBinding.progressSpinKitView.setVisibility(View.GONE);
               /* Gson mGson = new Gson();
                JSONObject mJsonObject = null;
                try {
                    mJsonObject = new JSONObject(staticRes);
                } catch (JSONException e) {
                    e.printStackTrace();
                }

                CMS_HomePageModel mCms_homePageModel = mGson.fromJson(mJsonObject.toString(), CMS_HomePageModel.class);

                JSONArray mJsonArrayData;
                try {
                    mJsonArrayData = mJsonObject.getJSONArray("data");
                    JSONObject mJsonObjectDataInside = mJsonArrayData.getJSONObject(0);
                    JSONArray widget_data = mJsonObjectDataInside.getJSONArray("widgets_data");
                    for (int i = 0; i < widget_data.length(); i++) {
                        if (widget_data.getJSONObject(i).getString("widgets_id").trim().equals("20")) {

                            mCms_parentCategoryLists.addAll(mCms_homePageModel.getData().get(0).getWidgetsData().get(i).getParentCategoryList());
                            //Toast.makeText(getApplicationContext(), widget_data.getJSONObject(i).getString("label"), Toast.LENGTH_SHORT).show();
                            //widget_data.getJSONObject(i).getJSONArray("parent_category_list");
                                    *//*JSONArray parent_category_list = widget_data.getJSONObject(i).getJSONArray("parent_category_list");
                                    System.out.println("Response : Fingureprint_login : requestCmsContent : parent_category_list : " + parent_category_list);
                                    for (int j = 0; j < parent_category_list.length(); j++) {
                                        CMS_ParentCategoryList mCms_parentCategoryList = new CMS_ParentCategoryList(parent_category_list.getJSONObject(j).getString("name"));
                                        mCms_parentCategoryLists.add(mCms_parentCategoryList);
                                    }*//*
                        }


                    }

                } catch (JSONException e) {
                    e.printStackTrace();
                }

                System.out.println("Rahul requestCmsContent : response : " + staticRes);
                System.out.println("Response : Fingureprint_login : requestCmsContent : mCms_parentCategoryLists : " + new Gson().toJson(mCms_parentCategoryLists));
                mCms_shopByCategoryAdapter.notifyDataSetChanged();
              */

            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());
                if (mSharedPreferenceManager.isLoggedIn()) {
                    headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                    headers.put(Constants.VARIABLES.WAREHOUSE_KEY, mSharedPreferenceManager.getWarehouseId());
                }
                return headers;
            }


        };


        // Adding request to request queue
        queue.add(jsonObjReq);
    }

    @Override
    public void customFieldValueSelect(int argProductId, int argQuantity, String custom_field_name, String custom_field_value,int position) {
        Intent i = new Intent(SearchActivity.this, DialogPrepareView.class);
        i.putExtra("custom_field_name", custom_field_name);
        i.putExtra("custom_field_value", custom_field_value);
        i.putExtra("product_id", argProductId+"");
        i.putExtra("position", position+"");
        startActivityForResult(i,101);
    }




}
