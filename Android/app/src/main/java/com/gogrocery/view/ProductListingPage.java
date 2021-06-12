package com.gogrocery.view;

import android.app.Dialog;
import android.content.Intent;
import androidx.databinding.DataBindingUtil;
import android.os.AsyncTask;
import android.os.Build;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.RadioButton;
import android.widget.RadioGroup;

import com.android.volley.AuthFailureError;
import com.android.volley.RequestQueue;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.facebook.appevents.AppEventsConstants;
import com.facebook.appevents.AppEventsLogger;
import com.gogrocery.Adapters.ProductListingAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Customs.GridSpacingItemDecoration;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.BSP_ItemClick_Interface;
import com.gogrocery.Interfaces.ProductListingInterface;
import com.gogrocery.Models.CartModel.AddToCartModel;
import com.gogrocery.Models.ElasticSearch.Hit;
import com.gogrocery.Models.ElasticSearch.SearchModel;
import com.gogrocery.Models.ProductQuantityLocal;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityItemListingBinding;
import com.google.firebase.analytics.FirebaseAnalytics;
import com.google.gson.Gson;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class ProductListingPage extends AppCompatActivity implements View.OnClickListener, ProductListingInterface, BSP_ItemClick_Interface {

    private ActivityItemListingBinding mActivityItemListingBinding;
    private ProductListingAdapter mProductListingAdapter;
    private List<Hit> mSearchModelList = new ArrayList<>();
    private Dialog mSortDialog;
    private int pastVisiblesItems, visibleItemCount, totalItemCount;
    private boolean loading = true;
    private int page = 0;//Limit
    private GridLayoutManager mGridLayoutManager;
    AppEventsLogger logger;
    private FirebaseAnalytics mFirebaseAnalytics;
    private DatabaseHandler mDatabaseHandler;
    private SharedPreferenceManager mSharedPreferenceManager;
    private String category_id = "";
    private String paramPassElasticQuery = "";
    private String initialparamPassElasticQuery = "";
    private String initialparamPassElasticQuerySBB = "";
    private String initialparamPassElasticQuerySFQ = "";
    private String sortOptionSelected = "";
    private boolean isListingLoaded = false;
    private Dialog mSaveListDialog;
    private String mTerms_base64 = "";
    private int paginationSize = 18;
    String terms_array  = "";
    String terms_base64 = "";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityItemListingBinding = DataBindingUtil.setContentView(this, R.layout.activity_item_listing);
        mFirebaseAnalytics = FirebaseAnalytics.getInstance(this);
        logger = AppEventsLogger.newLogger(this);
        mDatabaseHandler = new DatabaseHandler(getApplicationContext());
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());

        setBestSellingProductRecyclerView();
        //itemListingRequest();
        mActivityItemListingBinding.sfl.startShimmer();

        mActivityItemListingBinding.rvItemListing.addOnScrollListener(new RecyclerView.OnScrollListener() {
            @Override
            public void onScrolled(RecyclerView recyclerView, int dx, int dy) {
                // Log.e(TAG, "onScrolled: " + dx + " " + dy);
//                if (dx > 0) {
                System.out.println("Rahul : ProductListingPage : requestProductListiing : 6 : ");

                visibleItemCount = mGridLayoutManager.getChildCount();
                totalItemCount = mGridLayoutManager.getItemCount();
                pastVisiblesItems = mGridLayoutManager.findFirstVisibleItemPosition();
                // Log.e(TAG, "onScrolled: " + loading);
                if (loading) {
                    System.out.println("Rahul : ProductListingPage : requestProductListiing : 7 : ");

                    //  Log.e(TAG, "onScrolled2: ");
                    if ((visibleItemCount + pastVisiblesItems) >= totalItemCount) {
                        System.out.println("Rahul : ProductListingPage : requestProductListiing : 8 : ");

                        Log.v("...", "Last Item Wow !");

                        //loading = false;
                        page = page + paginationSize;
                        try {
                            System.out.println("Rahul : ProductListingPage : requestProductListiing : 9 : ");

                            System.out.println("Rahul : ProductListingPage : onCreate : requestProductListiing : page : " + page);

                            JSONObject mJsonObject = new JSONObject(paramPassElasticQuery);
                            mJsonObject.remove("from");
                            mJsonObject.put("from", page);
                            paramPassElasticQuery = mJsonObject.toString();

                            JSONObject melastic = new JSONObject();

                            melastic.put("table_name","EngageboostProducts")
                                    .put("website_id",1)
                                    .put("data",new JSONObject(paramPassElasticQuery));


                            System.out.println("Rahul : ProductListingPage : onCreate : requestProductListiing : paramPassElasticQuery : " + paramPassElasticQuery);
                            requestProductListiing(melastic.toString());
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }


                    }
                }
//            }
            }
        });
        getBundelExtras();

        setListners();


    }

    @Override
    protected void onResume() {
        if (mProductListingAdapter != null) {
            mProductListingAdapter.notifyDataSetChanged();
        }

        if (Constants.VARIABLES.CART_COUNT > 0) {
            mActivityItemListingBinding.badgeNotification.setVisibility(View.VISIBLE);
            mActivityItemListingBinding.badgeNotification.setText("" + Constants.VARIABLES.CART_COUNT);
        } else {
            mActivityItemListingBinding.badgeNotification.setVisibility(View.GONE);
        }
        super.onResume();

    }

    private void getBundelExtras() {
        Bundle b = getIntent().getExtras();
        if (b != null) {
            Constants.VARIABLES.page_title = b.getString("PageTitle");
            System.out.println("Rahul : ProductListingPage : getBundelExtras : page_title : " + Constants.VARIABLES.page_title);
            category_id = b.getString("Category_slug");
            if (Constants.VARIABLES.page_title != null) {
                if (Constants.VARIABLES.page_title.contains("shop_by_brand")) {
                    mActivityItemListingBinding.tvListingTitle.setText(Constants.VARIABLES.page_title.split("#GoGrocery#")[1]);
                    Constants.VARIABLES.page_title = "shop_by_brand";
                    generateShopByBrandQuery();
                } else if (Constants.VARIABLES.page_title.contains("search_page")) {
                    mActivityItemListingBinding.tvListingTitle.setVisibility(View.GONE);
                    generateSearchQuery(b.getString("terms_array"), b.getString("terms_base64"));
                    //mActivityItemListingBinding.cvFooter.setVisibility(View.GONE);
                    terms_array = b.getString("terms_array");
                    terms_base64 = b.getString("terms_base64");
                } else {
                    generateIniElasticSearchQuery();
                    mActivityItemListingBinding.tvListingTitle.setText(b.getString("PageTitle"));
                }
            } else {
                generateIniElasticSearchQuery();
                mActivityItemListingBinding.tvListingTitle.setText(b.getString("PageTitle"));
            }

        }


        try {

            System.out.println("Rahul : ProductListingPage : getBundelExtras : requestProductListiing : page : " + page);

            JSONObject melastic = new JSONObject();

            melastic.put("table_name","EngageboostProducts")
                    .put("website_id",1)
                    .put("data",new JSONObject(paramPassElasticQuery));

            requestProductListiing(melastic.toString());
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private void setListners() {
        mActivityItemListingBinding.rlSort.setOnClickListener(this);
        mActivityItemListingBinding.rlFilters.setOnClickListener(this);
        mActivityItemListingBinding.ivBack.setOnClickListener(this);
        mActivityItemListingBinding.ivCart.setOnClickListener(this);
        mActivityItemListingBinding.ivSearch.setOnClickListener(this);
        mActivityItemListingBinding.ivLocationPin.setOnClickListener(this);
    }

    private void setBestSellingProductRecyclerView() {
        mProductListingAdapter = new ProductListingAdapter(getApplicationContext(), mSearchModelList, this, this, mDatabaseHandler);
        //  LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.HORIZONTAL, false);
        mGridLayoutManager = new GridLayoutManager(getApplicationContext(), 2);
        mActivityItemListingBinding.rvItemListing.setLayoutManager(mGridLayoutManager);
        mActivityItemListingBinding.rvItemListing.addItemDecoration(new GridSpacingItemDecoration(2, GridSpacingItemDecoration.dpToPx(getApplicationContext(), 1), true));
        mActivityItemListingBinding.rvItemListing.setItemAnimator(new DefaultItemAnimator());
        mActivityItemListingBinding.rvItemListing.setAdapter(mProductListingAdapter);
        mActivityItemListingBinding.rvItemListing.setNestedScrollingEnabled(false);
    }

    /* private void itemListingRequest() {
         // Update the list when the data changes

         MainViewModel mainViewModel;
         mainViewModel = ViewModelProviders.of(this).get(MainViewModel.class);

         //Param
         HashMap<String, Object> param = new HashMap<>();
         param.put("website_id", "1");
         param.put("warehouse_id", "7");
         param.put("category_id", "2");
         System.out.println("Response : ProductListingPage : itemListingRequest : param : " + param);
         //ViewModel Request
         mainViewModel.itemListing(param)

                 .observe(this, responseBodyResponse -> {

                     if (responseBodyResponse != null) {
                         Gson gson = new Gson();
                         String responseString = gson.toJson(responseBodyResponse);
                         mProductItemListing.addAll(responseBodyResponse.getData().get(0).getProduct());
                         System.out.println("Response : ProductListingPage : itemListingRequest : " + responseString);
                         System.out.println("Response : ProductListingPage : itemListingRequest : mItemListingDataList : " + gson.toJson(mProductItemListing));
                         mItemListingAdapter.notifyDataSetChanged();

                     } else {

                         System.out.println("Response : ProductListingPage : itemListingRequest : null : ");
                     }
                 });

     }*/


    private void generateShopByBrandQuery() {
        JSONObject mJsonObject = new JSONObject();
       /* {
            "query": {
            "bool": {
                "must": [
                {
                    "match": {
                    "brand_slug": {
                        "query": "johsons",
                                "operator": "and"
                    }
                }
                },
                {
                    "match": {
                    "isdeleted": "n"
                }
                },
                {
                    "match": {
                    "isblocked": "n"
                }
                },
                {
                    "match": {
                    "inventory.id": 2
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
      ]
            }
        },
            "from": 0,
                "size": "paginationSize",
                "sort": [
            {}
  ]
        }*/



       /* {
            "query": {
            "bool": {
                "must": [
                {
                    "match": {
                    "category_slug": {
                        "query": "personal-care",
                                "operator": "and"
                    }
                }
                },
                {
                    "match": {
                    "isdeleted": "n"
                }
                },
                {
                    "match": {
                    "isblocked": "n"
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
                                "inventory.id": 33
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
                                "channel_currency_product_price.warehouse_id": 33
                            }
                            }
                ]
                        }
                    }
                }
                }
      ],
                "must_not": {
                    "term": {
                        "product_images.img": ""
                    }
                }
            }
        },
            "from": 0,
                "size": 18,
                "sort": [
            {

            }
  ]
        }*/


        try {
          /*  mJsonObject.put("table_name","EngageboostProducts")
                    .put("website_id",1)
                    .put("data",new JSONObject()*/
                            mJsonObject.put("query", new JSONObject()
                    .put("bool", new JSONObject()
                            .put("must", new JSONArray()
                                            .put(new JSONObject().put("match", new JSONObject().put("brand_slug", new JSONObject().put("query", category_id).put("operator", "and"))))
                                            .put(new JSONObject().put("match", new JSONObject().put("isdeleted", "n")))
                                            .put(new JSONObject().put("match", new JSONObject().put("isblocked", "n")))
                                            /*.put(new JSONObject().put("range", new JSONObject().put("inventory.stock", new JSONObject().put("gt", 0))))
                                            .put(new JSONObject().put("match", new JSONObject().put("inventory.id", mSharedPreferenceManager.getWarehouseId())))*/
                                            .put(new JSONObject().put("match", new JSONObject().put("visibility_id", new JSONObject()
                                                    .put("query", "Catalog Search")
                                                    .put("operator", "and")
                                            )))
                                    /*.put(new JSONObject().put("match", new JSONObject().put("channel_currency_product_price.warehouse_id", mSharedPreferenceManager.getWarehouseId())))
                                    .put(new JSONObject().put("term", new JSONObject().put("product_images.is_cover", 1)))
                                    .put(new JSONObject().put("range", new JSONObject().put("channel_currency_product_price.new_default_price", new JSONObject().put("gt", "0"))))*/)
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
                                                                            .put("term", new JSONObject()
                                                                                    .put("channel_currency_product_price.warehouse_id", mSharedPreferenceManager.getWarehouseId())))
                                                                    .put(new JSONObject()
                                                                            .put("range", new JSONObject()
                                                                                    .put("channel_currency_product_price.new_default_price", new JSONObject()
                                                                                            .put("gt", 0))))
                                                            )))))
                                    .put(new JSONObject().put("nested", new JSONObject()
                                            .put("path", "product_images")
                                            .put("query", new JSONObject()
                                                    .put("bool", new JSONObject()
                                                            .put("must", new JSONArray()
                                                                    .put(new JSONObject()
                                                                            .put("term", new JSONObject()
                                                                                    .put("product_images.is_cover", 1)))
                                                            ))))))
                            .put("must_not", new JSONObject().put("term", new JSONObject().put("product_images.img", ""))))).put("from", page)
                    .put("size", paginationSize)
                    .put("sort", new JSONArray().put(new JSONObject()));
            initialparamPassElasticQuerySBB = mJsonObject.toString();
            paramPassElasticQuery = mJsonObject.toString();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private void generateSearchQuery(String argSearchQuery, String argTerms) {
        System.out.println("Rahul : ProductListingPage : generateSearchQuery : argSearchQuery : " + argSearchQuery);
        System.out.println("Rahul : ProductListingPage : generateSearchQuery : argTerms : " + argTerms);
       /* try {
            JSONObject mJsonObject = new JSONObject();
            mJsonObject.put("query", new JSONObject().put("bool", new JSONObject().put("must", new JSONArray()
                    .put(new JSONObject().put("query_string", new JSONObject().put("fields", new JSONArray().put("brand").put("name").put("sku").put("category")).put("query", "*" + argSearchQuery + "*")))
                    .put(new JSONObject().put("match", new JSONObject().put("inventory.id", mSharedPreferenceManager.getWarehouseId())))
                    .put(new JSONObject().put("match", new JSONObject().put("visibility_id", new JSONObject()
                            .put("query", "Catalog Search")
                            .put("operator", "and")
                    )))

            )));
            initialparamPassElasticQuery = mJsonObject.toString();
            paramPassElasticQuery = mJsonObject.toString();
        } catch (JSONException e) {
            e.printStackTrace();
        }*/
        mTerms_base64 = argTerms;
        String decodedTermstext = "";
        JSONArray termsJSJsonArray = null;
        try {
            byte[] decrypt = Base64.decode(argTerms, Base64.NO_WRAP);
            try {
                decodedTermstext = new String(decrypt, "UTF-8");
                System.out.println("Rahul : ProductListingPage : generateSearchQuery : decodedTermstext : " + decodedTermstext);

                termsJSJsonArray = new JSONArray(argSearchQuery);
                System.out.println("Rahul : ProductListingPage : generateSearchQuery : termsJSJsonArray : " + termsJSJsonArray);

            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }
            JSONObject mJsonObject = new JSONObject();

         /*   mJsonObject.put("table_name","EngageboostProducts")
                    .put("website_id",1)
                    .put("data",new JSONObject()*/
                            mJsonObject .put("query", new JSONObject()
                    .put("bool", new JSONObject()
                            .put("must", new JSONArray()
                                            .put(new JSONObject().put("match", new JSONObject().put("isdeleted", "n")))
                                            .put(new JSONObject().put("match", new JSONObject().put("isblocked", "n")))
                                            /*.put(new JSONObject().put("range", new JSONObject().put("inventory.stock", new JSONObject().put("gt", 0))))
                                            .put(new JSONObject().put("match", new JSONObject().put("inventory.id", mSharedPreferenceManager.getWarehouseId())))*/
                                            .put(new JSONObject().put("match", new JSONObject().put("visibility_id", new JSONObject()
                                                    .put("query", "Catalog Search")
                                                    .put("operator", "and")
                                            )))
                                    /*.put(new JSONObject().put("match", new JSONObject().put("channel_currency_product_price.warehouse_id", mSharedPreferenceManager.getWarehouseId())))
                                    .put(new JSONObject().put("term", new JSONObject().put("product_images.is_cover", 1)))
                                    .put(new JSONObject().put("range", new JSONObject().put("channel_currency_product_price.new_default_price", new JSONObject().put("gt", "0"))))*/)
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
                                                                                    .put("gt", 0)))))
                                                    ))
                                            .put("score_mode", "avg")))
                                    .put(new JSONObject().put("nested", new JSONObject()
                                            .put("path", "channel_currency_product_price")
                                            .put("query", new JSONObject()
                                                    .put("bool", new JSONObject()
                                                            .put("must", new JSONArray()
                                                                    .put(new JSONObject()
                                                                            .put("term", new JSONObject()
                                                                                    .put("channel_currency_product_price.warehouse_id", mSharedPreferenceManager.getWarehouseId())))
                                                                    .put(new JSONObject()
                                                                            .put("range", new JSONObject()
                                                                                    .put("channel_currency_product_price.new_default_price", new JSONObject()
                                                                                            .put("gt", 0)))))))))
                                    .put(new JSONObject().put("nested", new JSONObject()
                                            .put("path", "product_images")
                                            .put("query", new JSONObject()
                                                    .put("bool", new JSONObject()
                                                            .put("must", new JSONArray()
                                                                    .put(new JSONObject()
                                                                            .put("term", new JSONObject()
                                                                                    .put("product_images.is_cover", 1)))
                                                            )))))
                                    .put(new JSONObject().put("terms", new JSONObject().put("id", termsJSJsonArray))))
                            .put("must_not", new JSONObject().put("term", new JSONObject().put("product_images.img", "")))))
                    .put("from", page)
                    .put("size", paginationSize)
                    .put("sort", new JSONArray().put(new JSONObject()));


            initialparamPassElasticQuery = mJsonObject.toString();
            initialparamPassElasticQuerySFQ = mJsonObject.toString();
            paramPassElasticQuery = mJsonObject.toString();

            System.out.println("Rahul : ProductListingPage : generateSearchQuery : paramPassElasticQuery : " + paramPassElasticQuery);

        } catch (JSONException e) {
            e.printStackTrace();
        }

    }

    private void generateIniElasticSearchQuery() {
        JSONObject mJsonObject = new JSONObject();

        try {

            /*mJsonObject.put("table_name","EngageboostProducts")
                    .put("website_id",1)
                    .put("data",new JSONObject()*/
                            mJsonObject.put("query", new JSONObject()
                                    .put("bool", new JSONObject()
                                            .put("must", new JSONArray()
                                                            .put(new JSONObject().put("terms", new JSONObject().put("category_slug.keyword", new JSONArray().put(category_id))))
                                                            .put(new JSONObject().put("match", new JSONObject().put("isdeleted", "n")))
                                                            .put(new JSONObject().put("match", new JSONObject().put("isblocked", "n")))
                                                            /*.put(new JSONObject().put("range", new JSONObject().put("inventory.stock", new JSONObject().put("gt", 0))))
                                                            .put(new JSONObject().put("match", new JSONObject().put("inventory.id", mSharedPreferenceManager.getWarehouseId())))*/
                                                            .put(new JSONObject().put("match", new JSONObject().put("visibility_id", new JSONObject()
                                                                    .put("query", "Catalog Search")
                                                                    .put("operator", "and")
                                                            )))
                                    /*.put(new JSONObject().put("match", new JSONObject().put("channel_currency_product_price.warehouse_id", mSharedPreferenceManager.getWarehouseId())))
                                    .put(new JSONObject().put("term", new JSONObject().put("product_images.is_cover", 1)))
                                    .put(new JSONObject().put("range", new JSONObject().put("channel_currency_product_price.new_default_price", new JSONObject().put("gt", "0"))))*/)
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
                                                                                                    .put("gt", 0)))))
                                                                    ))
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
                                                                                                    .put("channel_currency_product_price.warehouse_id", mSharedPreferenceManager.getWarehouseId()))))))))

                                                    .put(new JSONObject().put("nested", new JSONObject()
                                                            .put("path", "product_images")
                                                            .put("query", new JSONObject()
                                                                    .put("bool", new JSONObject()
                                                                            .put("must", new JSONArray()
                                                                                    .put(new JSONObject()
                                                                                            .put("term", new JSONObject()
                                                                                                    .put("product_images.is_cover", 1)))
                                                                            ))))))
                                            .put("must_not", new JSONObject().put("term", new JSONObject().put("product_images.img", ""))))).put("from", page)
                            .put("size", paginationSize)
                            .put("sort", new JSONArray().put(new JSONObject().put("category", new JSONObject().put("order", "desc"))));



            initialparamPassElasticQuery = mJsonObject.toString();
            paramPassElasticQuery = mJsonObject.toString();
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }

    public void requestProductListiing(String argJsonObject) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        System.out.println("Rahul : ProductListingPage : requestProductListiing : param : " + argJsonObject);

/*{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "category_slug": "baby-care"
          }
        },
        {
          "match": {
            "isdeleted": "n"
          }
        },
        {
          "match": {
            "isblocked": "n"
          }
        },
        {
          "match": {
            "inventory.id": 2
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
      ]
    }
  },
  "from": 0,
  "size": "paginationSize",
  "sort": [
    {
      "channel_currency_product_price.price": {
        "order": "asc"
      }
    }
  ]
}*/

        /*{
            "query": {
            "bool": {
                "must": [
                {
                    "match": {
                    "category_id.id": "175"
                }
                },
                {
                    "match": {
                    "isdeleted": "n"
                }
                },
                {
                    "match": {
                    "isblocked": "n"
                }
                },
                {
                    "match": {
                    "inventory.id": "7"
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
      ]
            }
        },
            "from": 30,
                "size": "paginationSize",
                "sort": [
            {
                "numberof_view": {
                "order": "desc"
            }
            }
  ]
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

        OkHttpClient client = new OkHttpClient();

        MediaType mediaType = MediaType.parse("application/json");
        RequestBody body = RequestBody.create(mediaType, argJsonObject);
        Request request = new Request.Builder()
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
                    Response response = client.newCall(request).execute();
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
            protected void onPostExecute(String s) {
                super.onPostExecute(s);
                JSONObject mJsonObjectResponse = null;
                System.out.println("Rahul : ProductListingPage : requestProductListiing : response : " + s);
                Gson mGson = new Gson();
                SearchModel mSearchModel = null;
                try {
                    mJsonObjectResponse = new JSONObject(s);
                    mSearchModel = mGson.fromJson(mJsonObjectResponse.toString(), SearchModel.class);

                    for (int i = 0; i < mSearchModel.getHits().getHits().size(); i++) {

                       /* final boolean[] isImageLoaded = {true};

                        for (int jj = 0; jj < mSearchModel.getHits().getHits().get(i).getSource().getProductImages().size(); jj++) {

                            if (mSearchModel.getHits().getHits().get(i).getSource().getProductImages().get(jj).getIsCover() == 1) {
                                System.out.println("Rahul : ProductListingPage : requestProductListiing : getIsCover : " + mSearchModel.getHits().getHits().get(i).getSource().getProductImages().get(jj).getLink() + mSearchModel.getHits().getHits().get(i).getSource().getProductImages().get(jj).getImg());
*//*

                                try {
                                    Glide.with(getApplicationContext())
                                            .load(mSearchModel.getHits().getHits().get(i).getSource().getProductImages().get(jj).getLink() + mSearchModel.getHits().getHits().get(i).getSource().getProductImages().get(jj).getImg())
                                            .listener(new RequestListener<Drawable>() {

                                                @Override
                                                public boolean onLoadFailed(@Nullable GlideException e, Object model, Target<Drawable> target, boolean isFirstResource) {

                                                    System.out.println("Rahul : ProductListingPage : requestProductListiing : Glide : onLoadFailed : ");
                                                    isImageLoaded[0]=false;
                                                    return false;
                                                }

                                                @Override
                                                public boolean onResourceReady(Drawable resource, Object model, Target<Drawable> target, DataSource dataSource, boolean isFirstResource) {
                                                    System.out.println("Rahul : ProductListingPage : requestProductListiing : Glide : onResourceReady : ");

                                                    return false;
                                                }


                                            })
                                            .into(mActivityItemListingBinding.ivfake);
                                }catch (Exception e)
                                {
                                    System.out.println("Rahul : ProductListingPage : requestProductListiing : Glide : Exception : "+e);
                                }*//*


                                if (isImageLoaded[0]) {
                                    System.out.println("Rahul : ProductListingPage : requestProductListiing : Glide : getIsCover : " + mSearchModel.getHits().getHits().get(i).getSource().getProductImages().get(jj).getIsCover());
                                    System.out.println("Rahul : ProductListingPage : requestProductListiing : Glide : getName : " + mSearchModel.getHits().getHits().get(i).getSource().getName());
                                    System.out.println("Rahul : ProductListingPage : requestProductListiing : Glide : contains : " + mSearchModelList.contains(mSearchModel.getHits().getHits().get(i)));

                                    if (!mSearchModelList.contains(mSearchModel.getHits().getHits().get(i))) {
                                        mSearchModelList.add(mSearchModel.getHits().getHits().get(i));
                                    }
                                }


                            }
                        }*/

                        for (int j = 0; j < mSearchModel.getHits().getHits().get(i).getSource().getInventory().size(); j++) {
                          /*  System.out.println("Rahul : ProductListingPage : requestProductListiing : instock : getId : "+mSearchModel.getHits().getHits().get(i).getSource().getInventory().get(j).getId());
                            System.out.println("Rahul : ProductListingPage : requestProductListiing : instock : getWarehouseId : "+mSharedPreferenceManager.getWarehouseId());
*/
                            if (mSearchModel.getHits().getHits().get(i).getSource().getInventory().get(j).getId() == Integer.parseInt(mSharedPreferenceManager.getWarehouseId())) {
                                if (mSearchModel.getHits().getHits().get(i).getSource().getInventory().get(j).getStock() != 0) {
                                    // System.out.println("Rahul : ProductListingPage : requestProductListiing : instock : getStock 1 : " + mSearchModel.getHits().getHits().get(i).getSource().getInventory().get(j).getStock());
                                    // System.out.println("Rahul : ProductListingPage : requestProductListiing : contains : " + mSearchModelList.contains(mSearchModel.getHits().getHits().get(i)));

                                    if (!mSearchModelList.contains(mSearchModel.getHits().getHits().get(i))) {
                                        // System.out.println("Rahul : ProductListingPage : requestProductListiing : instock : getStock 2 : " + mSearchModel.getHits().getHits().get(i).getSource().getInventory().get(j).getStock());

                                        mSearchModelList.add(mSearchModel.getHits().getHits().get(i));
                                    }
                                }
                            }

                        }


                        //  if(mSearchModel.getHits().getHits().get(i).getSource().getProductImages().get(0).)
                        // mSearchModelList
                    }
                    // mSearchModelList.addAll(mSearchModel.getHits().getHits());

                    System.out.println("Rahul : ProductListingPage : mSearchModelList size : " + mSearchModelList.size());
                    if (mSearchModel.getHits().getHits().size() < paginationSize) {
                        loading = false;
                        if (mProductListingAdapter.mSpinKitView != null) {
                            mProductListingAdapter.mSpinKitView.setVisibility(View.GONE);
                        }
                        System.out.println("Rahul : ProductListingPage : requestProductListiing : 1 : ");
                    }
                    if (mSearchModelList.size() == 0 && mSearchModel.getHits().getHits().size() == 0) {

                        mActivityItemListingBinding.sfl.setVisibility(View.GONE);
                        mActivityItemListingBinding.sfl.stopShimmer();
                        mActivityItemListingBinding.rvItemListing.setVisibility(View.GONE);
                        mActivityItemListingBinding.noProductAvailable.setVisibility(View.VISIBLE);
                        mActivityItemListingBinding.cvFooter.setVisibility(View.GONE);
                        // mActivityItemListingBinding.cvFooter.setVisibility(View.GONE);
                        System.out.println("Rahul : ProductListingPage : requestProductListiing : 2 : ");
                    } else {

                        if (mSearchModel.getHits().getHits().size() > 0) {

                            mProductListingAdapter.notifyDataSetChanged();
                            mActivityItemListingBinding.sfl.setVisibility(View.GONE);
                            mActivityItemListingBinding.sfl.stopShimmer();
                            mActivityItemListingBinding.rvItemListing.setVisibility(View.VISIBLE);
                            if (mProductListingAdapter.mSpinKitView != null) {
                                mProductListingAdapter.mSpinKitView.setVisibility(View.GONE);
                            }
                            mActivityItemListingBinding.noProductAvailable.setVisibility(View.GONE);
                            System.out.println("Rahul : ProductListingPage : requestProductListiing : 3 : ");
                        } else {
                            System.out.println("Rahul : ProductListingPage : requestProductListiing : 3else : ");
                            loading = false;
                        }
                    }

                } catch (
                        JSONException e) {
                    e.printStackTrace();
                    System.out.println("Rahul : ProductListingPage : onPostExecute JSONException : ");
                    System.out.println("Rahul : ProductListingPage : requestProductListiing : 4 : ");
                    mActivityItemListingBinding.sfl.setVisibility(View.GONE);
                    mActivityItemListingBinding.sfl.stopShimmer();
                    mActivityItemListingBinding.rvItemListing.setVisibility(View.GONE);
                    if (mSearchModelList.size() <= 0) {
                        mActivityItemListingBinding.somethingwentwrong.setVisibility(View.VISIBLE);
                    }
                    // mActivityItemListingBinding.cvFooter.setVisibility(View.GONE);
                } catch (
                        NullPointerException e) {
                    System.out.println("Rahul : ProductListingPage : requestProductListiing : 5 : ");
                    System.out.println("Rahul : ProductListingPage : onPostExecute NullPointerException : ");
                    mActivityItemListingBinding.sfl.setVisibility(View.GONE);
                    mActivityItemListingBinding.sfl.stopShimmer();
                    mActivityItemListingBinding.rvItemListing.setVisibility(View.GONE);
                    if (mSearchModelList.size() <= 0) {
                        mActivityItemListingBinding.somethingwentwrong.setVisibility(View.VISIBLE);
                    }
                    //mActivityItemListingBinding.cvFooter.setVisibility(View.GONE);
                }
                
               /* if(mSearchModel.getHits()==null)
                {
                    Toast.makeText(getApplicationContext(),"No product available",Toast.LENGTH_LONG).show();
                }else {*/

            }
             /*   Gson mGson = new Gson();
                JSONObject mJsonObject = null;
                try {
                    if (mJsonObject == null) {
                        if(mSearchModelList.size()==0)
                        {
                            Toast.makeText(getApplicationContext(),"No product available",Toast.LENGTH_LONG).show();
                        }
                    } else {
                        mJsonObject = new JSONObject(s);
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                if (mProductListingAdapter.mSpinKitView != null) {
                    mProductListingAdapter.mSpinKitView.setVisibility(View.GONE);
                }

                System.out.println("Rahul : ProductListingPage : response : " + mJsonObject.toString());
                SearchModel mSearchModel = mGson.fromJson(mJsonObject.toString(), SearchModel.class);

                mSearchModelList.addAll(mSearchModel.getHits().getHits());
                System.out.println("Rahul : ProductListingPage : mSearchModelList size : " + mSearchModelList.size());
                mProductListingAdapter.notifyDataSetChanged();


                mActivityItemListingBinding.sfl.setVisibility(View.GONE);
                mActivityItemListingBinding.sfl.stopShimmer();
                mActivityItemListingBinding.rvItemListing.setVisibility(View.VISIBLE);*/
            //  }
        };

        asyncTask.execute();



        /* System.out.println("Rahul : ProductListingPage : param : " + mJsonObject.toString());
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                "http://navsoft.co.in:9200/lifco_product_1/data/_search/",mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {

                        try {
                            Gson mGson = new Gson();
                            JSONObject mJsonObject =response;

                            System.out.println("Rahul : ProductListingPage : response : " + response);
                            SearchModel mSearchModel = mGson.fromJson(mJsonObject.toString(), SearchModel.class);

                            mSearchModelList.addAll(mSearchModel.getHits().getHits());
                            System.out.println("Rahul : ProductListingPage : mSearchModelList size : " + mSearchModelList.size());
                            mItemListingAdapter.notifyDataSetChanged();
                        } catch (Exception exception) {
                            System.out.println("Rahul : ProductListingPage : error : " + exception.getCause());
                        }

                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : ProductListingPage :  : VolleyError : " + error.toString());

               *//* Gson mGson = new Gson();
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
                                    *//**//*JSONArray parent_category_list = widget_data.getJSONObject(i).getJSONArray("parent_category_list");
                                    System.out.println("Response : Fingureprint_login : requestCmsContent : parent_category_list : " + parent_category_list);
                                    for (int j = 0; j < parent_category_list.length(); j++) {
                                        CMS_ParentCategoryList mCms_parentCategoryList = new CMS_ParentCategoryList(parent_category_list.getJSONObject(j).getString("name"));
                                        mCms_parentCategoryLists.add(mCms_parentCategoryList);
                                    }*//**//*
                        }


                    }

                } catch (JSONException e) {
                    e.printStackTrace();
                }

                System.out.println("Rahul requestCmsContent : response : " + staticRes);
                System.out.println("Response : Fingureprint_login : requestCmsContent : mCms_parentCategoryLists : " + new Gson().toJson(mCms_parentCategoryLists));
                mCms_shopByCategoryAdapter.notifyDataSetChanged();
              *//*

            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                return headers;
            }

            @Override
            protected Map<String, String> getParams() throws AuthFailureError {

                HashMap<String,String> mRStringHashMap=new HashMap<>();
                mRStringHashMap=new Gson().fromJson(mJsonObject.toString(),HashMap.class);
                System.out.println("Rahul : ProductListingPage : getParams : "+mRStringHashMap.toString());
                return mRStringHashMap;
            }
        };


        // Adding request to request queue
        queue.add(jsonObjReq);*/
    }


    private void sortDialog() {
        mSortDialog = new Dialog(this);
        mSortDialog.setContentView(R.layout.sort_option_dialog);
        RadioGroup rgSortOption;
        RadioButton rbPopularity, rbPriceHTL, rbPriceLTH, rbNewestFirst;
        Button dialogBtnCancel, dialogBtnApply;


        dialogBtnCancel = mSortDialog.findViewById(R.id.dialogBtnCancel);
        dialogBtnApply = mSortDialog.findViewById(R.id.dialogBtnApply);
        rgSortOption = mSortDialog.findViewById(R.id.rgSortOption);
        rbPopularity = mSortDialog.findViewById(R.id.rbPopularity);
        rbPriceHTL = mSortDialog.findViewById(R.id.rbPriceHTL);
        rbPriceLTH = mSortDialog.findViewById(R.id.rbPriceLTH);
        rbNewestFirst = mSortDialog.findViewById(R.id.rbNewestFirst);

        //.put("sort",new JSONArray().put(new JSONObject().put("numberof_view",new JSONObject().put("order","desc"))))


        switch (sortOptionSelected) {
            case "rbPriceHTL":
                rbPriceHTL.setChecked(true);
                break;
            case "rbPriceLTH":
                rbPriceLTH.setChecked(true);
                break;
            case "rbNewestFirst":
                rbNewestFirst.setChecked(true);
                break;
        }


        dialogBtnApply.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                System.out.println("Rahul : ProductListingPage : sortDialog : selected : " + rgSortOption.getCheckedRadioButtonId());
                JSONObject mJ = null;
                if (!paramPassElasticQuery.isEmpty()) {
                    if (rgSortOption.getCheckedRadioButtonId() != -1) {

                        switch (rgSortOption.getCheckedRadioButtonId()) {
                            case R.id.rbPriceHTL:
                                try {

                                    mJ = new JSONObject(paramPassElasticQuery);
                                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
                                        mJ.remove("from");
                                        mJ.put("from", 0);
                                        mJ.getJSONArray("sort").remove(0);
                                        mJ.getJSONArray("sort").put(new JSONObject().put("channel_currency_product_price.new_default_price", new JSONObject().put("order", "desc")
                                                .put("mode", "avg")
                                                .put("nested_path", "channel_currency_product_price")
                                                .put("nested_filter", new JSONObject().put("term", new JSONObject().put("channel_currency_product_price.warehouse_id", mSharedPreferenceManager.getWarehouseId())))));

                                    }

                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }
                                System.out.println("Rahul : ProductListingPage : sortDialog : selected : 1" + rgSortOption.getCheckedRadioButtonId());
                                sortOptionSelected = "rbPriceHTL";
                                break;
                            case R.id.rbPriceLTH:
                                try {
                                    mJ = new JSONObject(paramPassElasticQuery);
                                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
                                        mJ.remove("from");
                                        mJ.put("from", 0);
                                        mJ.getJSONArray("sort").remove(0);
                                        mJ.getJSONArray("sort").put(new JSONObject().put("channel_currency_product_price.new_default_price", new JSONObject().put("order", "asc")
                                                .put("mode", "avg")
                                                .put("nested_path", "channel_currency_product_price")
                                                .put("nested_filter", new JSONObject().put("term", new JSONObject().put("channel_currency_product_price.warehouse_id", mSharedPreferenceManager.getWarehouseId())))));

                                    }

                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }
                                System.out.println("Rahul : ProductListingPage : sortDialog : selected : 2" + rgSortOption.getCheckedRadioButtonId());
                                sortOptionSelected = "rbPriceLTH";
                                break;
                            case R.id.rbNewestFirst:

                                try {
                                    mJ = new JSONObject(paramPassElasticQuery);
                                    mJ.remove("from");
                                    mJ.put("from", 0);
                                    mJ = new JSONObject(paramPassElasticQuery);
                                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
                                        mJ.getJSONArray("sort").remove(0);
                                        mJ.getJSONArray("sort").put(new JSONObject().put("category", new JSONObject().put("order", "desc")));

                                    }

                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }
                                System.out.println("Rahul : ProductListingPage : sortDialog : selected : 3" + rgSortOption.getCheckedRadioButtonId());
                                sortOptionSelected = "rbNewestFirst";
                                break;
                            case R.id.rbPopularity:
                                try {
                                    mJ = new JSONObject(paramPassElasticQuery);
                                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
                                        mJ.getJSONArray("sort").remove(0);
                                        mJ.getJSONArray("sort").put(new JSONObject().put("numberof_view", new JSONObject().put("order", "desc")));

                                    }

                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }
                                System.out.println("Rahul : ProductListingPage : sortDialog : selected : 4" + rgSortOption.getCheckedRadioButtonId());
                                break;
                        }

                        try {
                            mJ.remove("from");
                            mJ.put("from", 0);
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                        paramPassElasticQuery = mJ.toString();
                        System.out.println("Rahul : ProductListingPage : sortDialog : paramPassElasticQuery : " + paramPassElasticQuery);

                        mSearchModelList.clear();

                        setBestSellingProductRecyclerView();

                        try {

                            JSONObject melastic = new JSONObject();

                            melastic.put("table_name","EngageboostProducts")
                                    .put("website_id",1)
                                    .put("data",new JSONObject(paramPassElasticQuery));
                            requestProductListiing(melastic.toString());
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }
                System.out.println("Rahul : ProductListingPage : loading : " + loading);
                mSortDialog.dismiss();
            }
        });

        dialogBtnCancel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mSortDialog.dismiss();
            }
        });
        mSortDialog.show();

    }

    @Override
    public void onClick(View v) {

        switch (v.getId()) {
            case R.id.rlSort:
                sortDialog();
                break;
            case R.id.rlFilters:
                Intent rlFilters = new Intent(ProductListingPage.this, FilterActivity.class);
                rlFilters.putExtra("slug", category_id);
                rlFilters.putExtra("term_base64", mTerms_base64);
                if (Constants.VARIABLES.page_title.contains("shop_by_brand")) {
                    rlFilters.putExtra("json_query", initialparamPassElasticQuerySBB);
                } else if(Constants.VARIABLES.page_title.contains("search_page")) {
                    rlFilters.putExtra("json_query",initialparamPassElasticQuerySFQ);
                }else{
                    rlFilters.putExtra("json_query", initialparamPassElasticQuery);
                }
                startActivityForResult(rlFilters, 1);
                break;
            case R.id.ivBack:
                Constants.VARIABLES.mFilterAddedList.clear();

                Constants.VARIABLES.mFilterAddedList.clear();
                Constants.VARIABLES.categoryFilterList.clear();
                Constants.VARIABLES.priceFilterList.clear();
                Constants.VARIABLES.brandFilterList.clear();
                Constants.VARIABLES.sizeFilterList.clear();
                Constants.VARIABLES.discountFilterList.clear();
                finish();
                break;
            case R.id.ivCart:
                Intent ivCart = new Intent(ProductListingPage.this, MyCart.class);
                startActivity(ivCart);
                break;
            case R.id.ivSearch:
                Intent ivSearch = new Intent(ProductListingPage.this, SearchActivity.class);
                startActivity(ivSearch);
                break;
            case R.id.ivLocationPin:
                Intent ivLocationPin = new Intent(ProductListingPage.this, MapLocationSelectionUpdate.class);
                startActivity(ivLocationPin);
                break;
        }
    }


    @Override
    public void sendSlug(String argSlug, int argProductId) {

        Intent i = new Intent(ProductListingPage.this, DetailActivity.class);
        i.putExtra("slug", argSlug.split("#GoGrocery#")[0]);
        i.putExtra("title", argSlug.split("#GoGrocery#")[1]);
        i.putExtra("product_id", argProductId);
        startActivity(i);
    }

    @Override
    public void sendProductIdForWishlist(int argProductId, String argAction) {
        if (mSharedPreferenceManager.isLoggedIn()) {
            try {
                requestAddToWishlist(argProductId, argAction);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        } else {
            Intent i = new Intent(ProductListingPage.this, LoginActivity.class);
            i.putExtra("from_where", "ProductListing");
            startActivity(i);
        }
    }

    @Override
    public void savelist(String argProductId) {


        if (mSharedPreferenceManager.isLoggedIn()) {
            Intent i = new Intent(ProductListingPage.this, SaveListPage.class);
            i.putExtra("product_id", argProductId);
            startActivity(i);
        } else {
            Intent i = new Intent(ProductListingPage.this, LoginActivity.class);
            startActivity(i);
        }
        //showCreateSaveListDialog();
    }


    private void showCreateSaveListDialog() {
        mSaveListDialog = new Dialog(ProductListingPage.this, R.style.DialogSlideAnimStyle);
        mSaveListDialog.setContentView(R.layout.create_save_list_dialog);
        mSaveListDialog.setCancelable(true);

        RecyclerView mRecyclerView = mSaveListDialog.findViewById(R.id.rvMySaveList);

        ImageView ivBack = mSaveListDialog.findViewById(R.id.ivBack);

        ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mSaveListDialog.dismiss();
            }
        });

      /*  WarehouseAdapter mWarehouseAdapter = new WarehouseAdapter(getApplicationContext(), mWarehouseList, this);
        GridLayoutManager mGridLayoutManager = new GridLayoutManager(getApplicationContext(), 2);
        mRecyclerView.setLayoutManager(mGridLayoutManager);
        mRecyclerView.addItemDecoration(new GridSpacingItemDecoration(2, GridSpacingItemDecoration.dpToPx(getApplicationContext(), 10), true));

        // mRecyclerView.addItemDecoration(new ItemDecorationAlbumColumns(10, 100));
        mRecyclerView.setLayoutManager(mGridLayoutManager);
        mRecyclerView.setItemAnimator(new DefaultItemAnimator());
        mRecyclerView.setAdapter(mWarehouseAdapter);
        mRecyclerView.setNestedScrollingEnabled(false);*/


        if (!mSaveListDialog.isShowing()) {
            mSaveListDialog.show();
        }
    }

    @Override
    public void connectMain(int argProductId, int argQuantity,int position) {


        try {
            requestAddToCart(argProductId, argQuantity);
        } catch (JSONException e) {
            e.printStackTrace();
        }


    }


    public void requestAddToWishlist(int argProductId, String argAction) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("website_id", 1);
        mJsonObject.put("product_id", argProductId);

        System.out.println("Rahul : MainActivityNew : requestAddToWishlist : param : " + mJsonObject);
        String CURRENT_URL = "";
        if (argAction.equals("add")) {
            CURRENT_URL = Constants.BASE_URL + Constants.API_METHODS.MY_WISH_LIST;
        } else {
            CURRENT_URL = Constants.BASE_URL + Constants.API_METHODS.DELETE_WISHLIST;
        }

        mActivityItemListingBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(com.android.volley.Request.Method.POST,
                CURRENT_URL, mJsonObject,
                new com.android.volley.Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        mActivityItemListingBinding.progressSpinKitView.setVisibility(View.GONE);
                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        System.out.println("Rahul : MainActivityNew : requestAddToWishlist : mJsonObject : " + mJsonObject);

                        try {
                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                Constants.showToastInMiddle(getApplicationContext(), response.getString("message"));
                                //Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();
                                if (argAction.equals("add")) {
                                    if (!mDatabaseHandler.checkWishlistAvailable("" + argProductId)) {
                                        mDatabaseHandler.addWishlistData("" + argProductId);
                                    }

                                    Bundle params = new Bundle();
                                    params.putString("productName",response.getJSONObject("data").getJSONObject("product").getString("name"));
                                    params.putString("productId",argProductId+"");
                                    params.putString("content_type","product");
                                    mFirebaseAnalytics.logEvent(FirebaseAnalytics.Event.ADD_TO_WISHLIST, params);
                                    logger.logEvent(AppEventsConstants.EVENT_NAME_ADDED_TO_WISHLIST, params);

                                } else {
                                    if (mDatabaseHandler.checkWishlistAvailable("" + argProductId)) {
                                        mDatabaseHandler.deleteWishlistSingleRecord("" + argProductId);
                                    }
                                }
                                mProductListingAdapter.notifyDataSetChanged();
                            } else {
                                Constants.showToastInMiddle(getApplicationContext(), response.getString("message"));

                                // Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();

                            }
                        } catch (JSONException e) {
                            e.printStackTrace();

                        }

                    }
                }, new com.android.volley.Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : MainActivityNew : requestAddToCart : VolleyError : " + error.toString());
                mActivityItemListingBinding.progressSpinKitView.setVisibility(View.GONE);

            }
        }) {
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

    public void requestAddToCart(int argProductId, int argQty) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));
        mJsonObject.put("product_id", argProductId);
        mJsonObject.put("quantity", argQty);
        mJsonObject.put("year_check", mSharedPreferenceManager.getYearCheck());
        System.out.println("Rahul : ProductListingPage : requestAddToCart : param : " + mJsonObject);
        System.out.println("Rahul : ProductListingPage : requestAddToCart : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));


        mActivityItemListingBinding.progressSpinKitView.setVisibility(View.VISIBLE);
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
                                logger.logEvent(AppEventsConstants.EVENT_NAME_ADDED_TO_CART, params);
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
                                mActivityItemListingBinding.badgeNotification.setVisibility(View.GONE);

                            } else {
                                Constants.VARIABLES.CART_COUNT = Integer.parseInt(mAddToCartModel.getCartData().getCart_count());
                                mActivityItemListingBinding.badgeNotification.setText(mAddToCartModel.getCartData().getCart_count());
                                AnimateBell();
                            }


                        } else {

                            try {
                                if(response.getString("is_age_verification").equals("False")) {
                                    Intent i = new Intent(ProductListingPage.this, TobacoCatActivity.class);
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
                        mProductListingAdapter.notifyDataSetChanged();
                        mActivityItemListingBinding.progressSpinKitView.setVisibility(View.GONE);

                    }
                }, new com.android.volley.Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : ProductListingPage : requestAddToCart : VolleyError : " + error.toString());
                mActivityItemListingBinding.progressSpinKitView.setVisibility(View.GONE);
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

    public void AnimateBell() {
        Animation shake = AnimationUtils.loadAnimation(getApplicationContext(), R.anim.shake);
        mActivityItemListingBinding.badgeNotification.setVisibility(View.VISIBLE);
        mActivityItemListingBinding.ivCart.setImageResource(R.drawable.ic_cart);
        mActivityItemListingBinding.ivCart.setAnimation(shake);
        mActivityItemListingBinding.ivCart.startAnimation(shake);

    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        // check if the request code is same as what is passed  here it is 2

        if (requestCode == 1) {
            try {
                if (data != null) {
                    if (data.getStringExtra("getFilterQuery").equals("clear")) {
                        try {
                            if (Constants.VARIABLES.page_title.equals("shop_by_brand")) {
                                generateShopByBrandQuery();
                            } else if(Constants.VARIABLES.page_title.equals("search_page")){
                                page = 0;
                                generateSearchQuery(terms_array, terms_base64);
                            }else{
                                generateIniElasticSearchQuery();

                            }
                            page = 0;
                            System.out.println("Rahul : ProductListingPage : onCreate : requestProductListiing : page : " + page);
                            mSearchModelList.clear();


                            JSONObject melastic = new JSONObject();

                            melastic.put("table_name","EngageboostProducts")
                                    .put("website_id",1)
                                    .put("data",new JSONObject(paramPassElasticQuery));
                            requestProductListiing(melastic.toString());
                            mActivityItemListingBinding.ivFilterAppliedTick.setVisibility(View.GONE);
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    } else {
                        System.out.println("Rahul : ProductListingPage : onActivityResult : getFilterQuery : " + data.getStringExtra("getFilterQuery"));
                        mSearchModelList.clear();
                        page = 0;

                        JSONObject mJsonObjectUpdateWithSort = new JSONObject(data.getStringExtra("getFilterQuery"));
                        JSONObject mJsonObjectUpdateWithSort1 = new JSONObject(paramPassElasticQuery);
                        mJsonObjectUpdateWithSort.remove("sort");
                        mJsonObjectUpdateWithSort.put("sort", mJsonObjectUpdateWithSort1.getJSONArray("sort"));

                        paramPassElasticQuery = mJsonObjectUpdateWithSort.toString();
                        JSONObject melastic = new JSONObject();

                        melastic.put("table_name","EngageboostProducts")
                                .put("website_id",1)
                                .put("data",new JSONObject(paramPassElasticQuery));

                        requestProductListiing(melastic.toString());

                        if (initialparamPassElasticQuerySBB.equals(paramPassElasticQuery)) {
                            mActivityItemListingBinding.ivFilterAppliedTick.setVisibility(View.GONE);
                        } else if (initialparamPassElasticQuery.equals(paramPassElasticQuery)) {
                            mActivityItemListingBinding.ivFilterAppliedTick.setVisibility(View.GONE);
                        }  else if(initialparamPassElasticQuerySFQ.equals(paramPassElasticQuery)){
                            mActivityItemListingBinding.ivFilterAppliedTick.setVisibility(View.GONE);
                        }else  {
                            mActivityItemListingBinding.ivFilterAppliedTick.setVisibility(View.VISIBLE);
                        }
                    }
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();

        Constants.VARIABLES.mFilterAddedList.clear();

        Constants.VARIABLES.mFilterAddedList.clear();
        Constants.VARIABLES.categoryFilterList.clear();
        Constants.VARIABLES.priceFilterList.clear();
        Constants.VARIABLES.brandFilterList.clear();
        Constants.VARIABLES.sizeFilterList.clear();
        Constants.VARIABLES.discountFilterList.clear();
        finish();
    }
}
