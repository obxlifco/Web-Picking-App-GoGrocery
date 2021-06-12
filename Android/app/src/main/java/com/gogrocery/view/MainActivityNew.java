package com.gogrocery.view;

import android.app.Activity;
import android.app.Dialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.util.Base64;
import android.util.Log;
import android.view.Gravity;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowManager;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AlertDialog;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.cardview.widget.CardView;
import androidx.core.content.ContextCompat;
import androidx.core.view.GravityCompat;
import androidx.databinding.DataBindingUtil;
import androidx.drawerlayout.widget.DrawerLayout;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import androidx.recyclerview.widget.SimpleItemAnimator;
import androidx.transition.Slide;
import androidx.transition.Transition;
import androidx.transition.TransitionManager;

import com.afollestad.materialdialogs.MaterialDialog;
import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.facebook.appevents.AppEventsConstants;
import com.facebook.appevents.AppEventsLogger;
import com.facebook.login.LoginManager;
import com.gogrocery.Adapters.BestSellingProductAdapter;
import com.gogrocery.Adapters.CMS_BestSellingProductAdapter;
import com.gogrocery.Adapters.CMS_ShopByCategoryAdapter;
import com.gogrocery.Adapters.FilterLeftSideMenuAdapter;
import com.gogrocery.Adapters.FilterRightSideMenuAdapter;
import com.gogrocery.Adapters.MainItemListingAdapter;
import com.gogrocery.Adapters.MapAddressAdapter;
import com.gogrocery.Adapters.NewCMS_BestSellingProductAdapter;
import com.gogrocery.Adapters.NewCMS_CategoryBannerAdapter;
import com.gogrocery.Adapters.NewCMS_DealsOfTheDayAdapter;
import com.gogrocery.Adapters.NewCMS_PromotionBannerAdapter;
import com.gogrocery.Adapters.NewCMS_PromotionalProductsAdapter;
import com.gogrocery.Adapters.NewCMS_ShopByBrandAdapter;
import com.gogrocery.Adapters.NewCMS_ShopByCategoryAdapter;
import com.gogrocery.Adapters.NewSubCatAdapter;
import com.gogrocery.Adapters.SideMenuCategoryAdapter;
import com.gogrocery.Adapters.StoreTypeAdapter;
import com.gogrocery.Adapters.WarehouseAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Fragment.FragmentSideMenuChild;
import com.gogrocery.Interfaces.ActivityRedirection;
import com.gogrocery.Interfaces.BSP_ItemClick_Interface;
import com.gogrocery.Interfaces.CallbackOnSelectCategory;
import com.gogrocery.Interfaces.FilterMenuConnectInterface;
import com.gogrocery.Interfaces.FilterRightMenuInterface;
import com.gogrocery.Interfaces.PrepareViewOpenInterface;
import com.gogrocery.Interfaces.ProductListingInterface;
import com.gogrocery.Interfaces.SelectAddressInterface;
import com.gogrocery.Interfaces.StoreTypeItemClickListner;
import com.gogrocery.Interfaces.WarehouseItemClickListner;
import com.gogrocery.Models.CMS_Model.BestSellProduct;
import com.gogrocery.Models.CMS_Model.ParentCategoryList;
import com.gogrocery.Models.CMS_NEW_Model.ShopByCategory;
import com.gogrocery.Models.CartModel.AddToCartModel;
import com.gogrocery.Models.DealsOfTheDay.Data;
import com.gogrocery.Models.ElasticSearch.Hit;
import com.gogrocery.Models.ElasticSearch.SearchModel;
import com.gogrocery.Models.FilterModel.FilterModel;
import com.gogrocery.Models.FilterModel.FilterModelMain;
import com.gogrocery.Models.ProductQuantityLocal;
import com.gogrocery.Models.SideMenuModel.Child;
import com.gogrocery.Models.SideMenuModel.SideMenuModel;
import com.gogrocery.Models.StoreTypeModel.DataItem;
import com.gogrocery.Models.StoreTypeModel.StoreTypeModel;
import com.gogrocery.Models.ViewCartModel.ViewCartModel;
import com.gogrocery.Models.WarehouseModel.WarehouseModel;
import com.gogrocery.R;
import com.gogrocery.ViewModel.StoreCategoryModel;
import com.gogrocery.databinding.ActivityMainNewBinding;
import com.gogrocery.helper.LoadingDialog;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.android.material.bottomsheet.BottomSheetDialog;
import com.google.android.material.navigation.NavigationView;
import com.google.firebase.analytics.FirebaseAnalytics;
import com.google.firebase.iid.FirebaseInstanceId;
import com.google.firebase.iid.InstanceIdResult;
import com.google.gson.Gson;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.RequestBody;

public class MainActivityNew extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener,
        ActivityRedirection, View.OnClickListener,
        BSP_ItemClick_Interface, ProductListingInterface, CallbackOnSelectCategory, PrepareViewOpenInterface {
    AppEventsLogger logger;
    private FirebaseAnalytics mFirebaseAnalytics;
    private ActivityMainNewBinding mActivityMainBinding;
    private SharedPreferenceManager mSharedPreferenceManager;
    private DatabaseHandler mDatabaseHandler;
    private boolean doubleBackToExitPressedOnce;
    private Dialog mChangeStoreLocation;
    private Dialog mPrepareItemSelect;
    // private SliderAdapterExample mSliderAdapterExample;
    private List<String> imageSliderUrlList;
    private NewCMS_DealsOfTheDayAdapter mNewCMS_dealsOfTheDayAdapter;
    private List<com.gogrocery.Models.CMS_NEW_Model.DealsOfTheDay> mDealsOfTheDayListNew = new ArrayList<>();
    private BestSellingProductAdapter mBestSellingProductAdapter;
    private CMS_BestSellingProductAdapter mCms_bestSellingProductAdapter;
    private List<Data> mBestSellingProductDataList = new ArrayList<>();
    private List<BestSellProduct> mCMS_BestSellProductsList = new ArrayList<>();
    private JSONObject mJSONElasticQuery;
    private SideMenuCategoryAdapter mSideMenuCategoryAdapter;

    private CMS_ShopByCategoryAdapter mCms_shopByCategoryAdapter;
    private List<com.gogrocery.Models.SideMenuModel.MenuBar> mCategoryList = new ArrayList<>();


    private List<ParentCategoryList> mCms_parentCategoryLists = new ArrayList<>();

    private NewCMS_ShopByCategoryAdapter mNewCMS_shopByCategoryAdapter;
    private List<ShopByCategory> mShopByCategoriesListNew = new ArrayList<>();

    private NewCMS_BestSellingProductAdapter mNewCMSBestSellingProductAdapter;
    private List<com.gogrocery.Models.CMS_NEW_Model.BestSellProduct> mBestSellProductListNew = new ArrayList<>();

    private NewCMS_CategoryBannerAdapter mNewCMSCategoryBannerAdapter;
    private NewSubCatAdapter newSubCatAdapter;
    private List<com.gogrocery.Models.CMS_NEW_Model.CategoryBanner> mCategoryBannerListNew = new ArrayList<>();

    MainItemListingAdapter mainItemListingAdapter;

    private NewCMS_ShopByBrandAdapter mNewCMSShopByBrandAdapter;
    private List<com.gogrocery.Models.CMS_NEW_Model.ShopByBrand> mShopByBrandListNew = new ArrayList<>();

    private NewCMS_PromotionBannerAdapter mNewCMSPromotionBannerAdapter;
    private List<com.gogrocery.Models.CMS_NEW_Model.PromotionalBanner> mPromotionalBannerList = new ArrayList<>();

    private NewCMS_PromotionalProductsAdapter mNewCMSPromotionalProductsAdapter;
    private List<com.gogrocery.Models.CMS_NEW_Model.Product> mPromotionalProductListNew = new ArrayList<>();
    private List<Child> subCategory;
    String typeName = "";
    JSONArray typeID;
    private FragmentManager fm;
    DrawerLayout drawer;
    private Dialog mUpdateDialog;
    private Dialog mBottomSheetDialog, mBottomSheetTypeDialog;
    private List<com.gogrocery.Models.WarehouseModel.Data> mWarehouseList = new ArrayList<>();
    LoadingDialog loadingDialog;
    private String sortOptionSelected = "";
    //New implement
    private String category_id = "";
    private String main_category_id = "";
    private String paramPassElasticQuery = "";
    private String initialparamPassElasticQuery = "";
    private String initialparamPassElasticQuerySBB = "";
    private String initialparamPassElasticQuerySFQ = "";
    private int pastVisiblesItems, visibleItemCount, totalItemCount;
    private boolean loading = true;
    private int page = 0;//Limit
    private int noOfColumn = 2;//Limit
    private boolean isListingLoaded = false;
    private Dialog mSaveListDialog;
    private String mTerms_base64 = "";
    private int paginationSize = 18;
    String terms_array = "";
    String terms_base64 = "";
    private GridLayoutManager mGridLayoutManager;
    private List<Hit> mSearchModelList = new ArrayList<>();
    private List<FilterModel> mFilterModelList = new ArrayList<>();
    private List<com.gogrocery.Models.FilterModel.Child> mChidList = new ArrayList<>();
    private String gte = "", lte = "";
    public static String mFilterType;
    private String brandFilter = "";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityMainBinding = DataBindingUtil.setContentView(this, R.layout.activity_main_new);
        mFirebaseAnalytics = FirebaseAnalytics.getInstance(this);
        logger = AppEventsLogger.newLogger(this);
        mDatabaseHandler = new DatabaseHandler(getApplicationContext());

        getFcmToken();

        //getBundelExtras();
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        System.out.println("Rahul : MainActivityNew : isLoggedIn : " + mSharedPreferenceManager.isLoggedIn());

        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        subCategory = new ArrayList<>();
        //Removes title from action_bar
        getSupportActionBar().setDisplayShowTitleEnabled(false);
        getSupportActionBar().setElevation(0);

        drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);
        Constants.VARIABLES.CURRENT_CURRENCY = mSharedPreferenceManager.getCurrentCurrency();
        mActivityMainBinding.appBarInclude.sfl.startShimmer();
        mActivityMainBinding.appBarInclude.itemSfl.startShimmer();
        mActivityMainBinding.appBarInclude.itemSfl.setVisibility(View.VISIBLE);
        // setSlider();
       /* try {
            requestDealsOfTheDay();
        } catch (JSONException e) {
            e.printStackTrace();
    }*/
        loadingDialog = new LoadingDialog(this);


        //bannerList();

        //shopByCategoryRequest();
        //setShopByCategoryRecyclerView();
        //setCMSShopByCategoryRecyclerView();
        setNewCMSShopByCategoryRecyclerView();
        // setSideMenuRecyclerView();


        //setDealsOfTheDayRecyclerView();
        //dealsOfTheDayRequest();

        //setBestSellingProductRecyclerView();
        //bestSellingProductRequest();
        //setCMSBestSellingProductRecyclerView();

  /*      setNewCMSDealsOfTheDayRecyclerView();
        setNewCMSBestSellingProductRecyclerView();
        setNewCMSCategoryBannerRecyclerView();*/

   /*     setNewCMSShopByBrandRecyclerView();
        setNewCMSPromotionalBannerRecyclerView();
        setNewCMSPromotionalProductRecyclerView();
        setSideMenuRecyclerView();*/
        setNewChideCategoryRecyclerView();

        try {
            //requestCmsContent();
            //   requestCmsContentNew();
            requestViewCart();
            requestSideMenu();

            if (mSharedPreferenceManager.isLoggedIn()) {
                mActivityMainBinding.ivRight.setVisibility(View.GONE);
                requestUpdateToken();

            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

//New

        mActivityMainBinding.appBarInclude.rvItemList.addOnScrollListener(new RecyclerView.OnScrollListener() {
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

                            melastic.put("table_name", "EngageboostProducts")
                                    .put("website_id", 1)
                                    .put("data", new JSONObject(paramPassElasticQuery));


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
        // getBundelExtras();

        setListners();
        hideStatusBarColor();
    }

    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }

    private void setListners() {
        mActivityMainBinding.rlLogout.setOnClickListener(this);
        mActivityMainBinding.rlProductSubstitute.setOnClickListener(this);
        mActivityMainBinding.rlContactUs.setOnClickListener(this);
        mActivityMainBinding.rlAboutUS.setOnClickListener(this);
        mActivityMainBinding.rlPrivacyPolicy.setOnClickListener(this);
        mActivityMainBinding.rlQulaityStandard.setOnClickListener(this);
        mActivityMainBinding.rlTermAndCondition.setOnClickListener(this);
        mActivityMainBinding.rlOurVisionPurpose.setOnClickListener(this);
        mActivityMainBinding.appBarInclude.llSearch.setOnClickListener(this);
        mActivityMainBinding.appBarInclude.ivContactUs.setOnClickListener(this);
        mActivityMainBinding.appBarInclude.ivContactUs.setOnClickListener(this);
        mActivityMainBinding.navHeaderProfile.setOnClickListener(this);
        mActivityMainBinding.appBarInclude.ivEditType.setOnClickListener(this);
        mActivityMainBinding.appBarInclude.ivEditLocation.setOnClickListener(this);
        mActivityMainBinding.appBarInclude.llChangeStore.setOnClickListener(this);
        mActivityMainBinding.appBarInclude.ivEditLocationName.setOnClickListener(this);
       // mActivityMainBinding.appBarInclude.ivCart.setOnClickListener(this);
        mActivityMainBinding.appBarInclude.tvViewCart.setOnClickListener(this);
        mActivityMainBinding.appBarInclude.ivSortBy.setOnClickListener(this);
        mActivityMainBinding.appBarInclude.ivFav.setOnClickListener(this);
        mActivityMainBinding.rlLogin.setOnClickListener(this);
        mActivityMainBinding.rlMyAccount.setOnClickListener(this);
        mActivityMainBinding.rlMyCart.setOnClickListener(this);
        mActivityMainBinding.rlMyOrders.setOnClickListener(this);
        mActivityMainBinding.rlMyWishlist.setOnClickListener(this);
        mActivityMainBinding.ivRight.setOnClickListener(this);
        mActivityMainBinding.appBarInclude.ivLocationPin.setOnClickListener(this);
        mActivityMainBinding.appBarInclude.rlBtnCart.setOnClickListener(this);
        mActivityMainBinding.appBarInclude.txtFilter.setOnClickListener(this);
        mActivityMainBinding.rlShopCategory.setOnClickListener(this);
        mActivityMainBinding.rlHome.setOnClickListener(this);
        mActivityMainBinding.rlLanguage.setOnClickListener(this);
        mActivityMainBinding.rlChangeStore.setOnClickListener(this);
        mActivityMainBinding.appBarInclude.tvLocation.setText(mSharedPreferenceManager.getWarehouseName());
        mActivityMainBinding.appBarInclude.tvType.setText(mSharedPreferenceManager.getWarehouseName());
        mActivityMainBinding.appBarInclude.tvLocationName.setText(mSharedPreferenceManager.getLocationAddress());

    }


    private void setNewCMSShopByCategoryRecyclerView() {
        //if (mShopByCategoriesListNew.size() > 0) {
        //mActivityMainBinding.appBarInclude.rlShopByCategory.setVisibility(View.VISIBLE);
        mNewCMS_shopByCategoryAdapter = new NewCMS_ShopByCategoryAdapter(getApplicationContext(), mCategoryList, this);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.HORIZONTAL, false);
        mActivityMainBinding.appBarInclude.rvShopByCategory.setLayoutManager(mLayoutManager);
        //mActivityMainBinding.appBarInclude.rvDealsOfTheDay.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
        mActivityMainBinding.appBarInclude.rvShopByCategory.setItemAnimator(new DefaultItemAnimator());
        mActivityMainBinding.appBarInclude.rvShopByCategory.setAdapter(mNewCMS_shopByCategoryAdapter);
        mActivityMainBinding.appBarInclude.rvShopByCategory.setNestedScrollingEnabled(false);
        /*} else {
            mActivityMainBinding.appBarInclude.rlShopByCategory.setVisibility(View.GONE);
        }*/
    }


    private void setNewChideCategoryRecyclerView() {

        newSubCatAdapter = new NewSubCatAdapter(MainActivityNew.this);
        newSubCatAdapter.setCallback(this);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.HORIZONTAL, false);
        mActivityMainBinding.appBarInclude.rvAllCategoryList.setLayoutManager(mLayoutManager);
        mActivityMainBinding.appBarInclude.rvAllCategoryList.setAdapter(newSubCatAdapter);
        mActivityMainBinding.appBarInclude.rvAllCategoryList.setNestedScrollingEnabled(false);

    }


    private void setItemRecyclerView() {
        mainItemListingAdapter = new MainItemListingAdapter(this, mSearchModelList, MainActivityNew.this, MainActivityNew.this, mDatabaseHandler, this);
        mGridLayoutManager = new GridLayoutManager(getApplicationContext(), noOfColumn);
        mActivityMainBinding.appBarInclude.rvItemList.setLayoutManager(mGridLayoutManager);
        ((SimpleItemAnimator) mActivityMainBinding.appBarInclude.rvItemList.getItemAnimator()).setSupportsChangeAnimations(false);
        //mActivityMainBinding.appBarInclude.rvDealsOfTheDay.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
    //    mActivityMainBinding.appBarInclude.rvItemList.setItemAnimator(new DefaultItemAnimator());
        mActivityMainBinding.appBarInclude.rvItemList.setAdapter(mainItemListingAdapter);
        mActivityMainBinding.appBarInclude.rvItemList.setNestedScrollingEnabled(false);
    }


    public void requestSideMenu() throws JSONException {
        if (Constants.isInternetConnected(MainActivityNew.this)) {
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            JSONObject mJsonObject = new JSONObject();
            mJsonObject.put("website_id", 1);
            mJsonObject.put("warehouse_id", mSharedPreferenceManager.getWarehouseId());
            mJsonObject.put("lang_code", "en");

            String staticRes = "";

       /* website_id: 1
        latitude: 22.572646
        longitude: 88.36389499999996
        lang_code: en*/
            System.out.println("Rahul : requestSideMenu : param : " + mJsonObject);
            mActivityMainBinding.appBarInclude.sfl.startShimmer();
            mActivityMainBinding.appBarInclude.sfl.setVisibility(View.VISIBLE);
            StringRequest jsonObjReq = new StringRequest(Request.Method.POST,
                    Constants.BASE_URL + Constants.API_METHODS.SIDE_MENU,
                    new Response.Listener<String>() {
                        @Override
                        public void onResponse(String response) {
                            System.out.println("Rahul : requestSideMenu : response : " + response);

                            Gson mGson = new Gson();
                            JSONObject mJsonObject = null;
                            try {
                                mJsonObject = new JSONObject(response);
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }

                            SideMenuModel mSideMenuModel = mGson.fromJson(mJsonObject.toString(), SideMenuModel.class);
                            mCategoryList.clear();
                            mCategoryList.addAll(mSideMenuModel.getMenuBar());
                            System.out.println("Rahul : requestSideMenu : mCategoryList : " + mGson.toJson(mCategoryList));
                            mSharedPreferenceManager.saveCategoryList(mCategoryList);
                            // mSideMenuCategoryAdapter.notifyDataSetChanged();
                            if (mSideMenuModel.getMenuBar().size() > 0) {
                                if (mSideMenuModel.getMenuBar().get(0).getChild().size() != 0) {
                                    subCategory.clear();
                                    subCategory.addAll(mSideMenuModel.getMenuBar().get(0).getChild());
                                    newSubCatAdapter.clearList();
                                    newSubCatAdapter.AddSubcategoryList(subCategory, 0);
                                    newSubCatAdapter.notifyDataSetChanged();
                                    category_id = "";
                                    page = 0;

                                    category_id = mSideMenuModel.getMenuBar().get(0).getSlug();
                                    main_category_id = mSideMenuModel.getMenuBar().get(0).getSlug();
                          /*          try {
                                        for (int i = 0; i < mSideMenuModel.getMenuBar().size(); i++) {
                                            if (mSideMenuModel.getMenuBar().get(i).getId().equals(275) || mSideMenuModel.getMenuBar().get(i).getId().equals(402)) {
                                                noOfColumn = 2;
                                            } else {
                                                noOfColumn = 3;
                                            }
                                        }
                                    }catch (Exception e){
                                        e.printStackTrace();
                                    }*/
                                    sortOptionSelected = "";
                                    setItemRecyclerView();
                                    generateIniElasticSearchQuery();
                                    try {

                                        System.out.println("Rahul : ProductListingPage : getBundelExtras : requestProductListiing : page : " + page);

                                        JSONObject melastic = new JSONObject();

                                        melastic.put("table_name", "EngageboostProducts")
                                                .put("website_id", 1)
                                                .put("data", new JSONObject(paramPassElasticQuery));

                                        requestProductListiing(melastic.toString());
                                    } catch (JSONException e) {
                                        e.printStackTrace();
                                    }

                                    Constants.VARIABLES.FILTER_TYPE = "category";

                                    //  mActivityMainBinding.appBarInclude.tabs.addTab(mActivityMainBinding.appBarInclude.tabs.newTab().setText("All"));
   /* for (int k = 0; k < subCategory.size(); k++) {
        mActivityMainBinding.appBarInclude.tabs.addTab(mActivityMainBinding.appBarInclude.tabs.newTab().setText(subCategory.get(k).getName()));
    }*/
                                }
                            }

                            // setTabView(mCategoryList);
                            mActivityMainBinding.appBarInclude.sfl.stopShimmer();
                            mActivityMainBinding.appBarInclude.sfl.setVisibility(View.GONE);
                            //mActivityMainBinding.appBarInclude.rl2.setVisibility(View.VISIBLE);
                            //mActivityMainBinding.appBarInclude.rl2Type.setVisibility(View.VISIBLE);
                            //mActivityMainBinding.appBarInclude.rl2Location.setVisibility(View.VISIBLE);
                            mActivityMainBinding.appBarInclude.nsv.setVisibility(View.VISIBLE);
                            mActivityMainBinding.appBarInclude.parent.setVisibility(View.VISIBLE);


                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {

                    System.out.println("Rahul : requestSideMenu : VolleyError : " + error.toString());
                    mActivityMainBinding.appBarInclude.sfl.stopShimmer();
                    mActivityMainBinding.appBarInclude.sfl.setVisibility(View.GONE);
                    //mActivityMainBinding.appBarInclude.rl2.setVisibility(View.VISIBLE);
                    //mActivityMainBinding.appBarInclude.rl2Type.setVisibility(View.VISIBLE);
                    //mActivityMainBinding.appBarInclude.rl2Location.setVisibility(View.VISIBLE);
                    mActivityMainBinding.appBarInclude.nsv.setVisibility(View.VISIBLE);
                    mActivityMainBinding.appBarInclude.parent.setVisibility(View.VISIBLE);

                }
            }) {

                @Override
                protected Map<String, String> getParams() throws AuthFailureError {
                    HashMap<String, String> mHashMap = new HashMap<>();
                    mHashMap.put("website_id", "1");
                    mHashMap.put("warehouse_id", mSharedPreferenceManager.getWarehouseId());
                    mHashMap.put("lang_code", "en");
                    return mHashMap;
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
        } else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }


    @Override
    public void onSelectCategory(List<Child> child, String argWhich, String argPageTitle) {

        subCategory.clear();
        subCategory.addAll(child);
        newSubCatAdapter.clearList();
        newSubCatAdapter.AddSubcategoryList(subCategory, 0);
        newSubCatAdapter.notifyDataSetChanged();
        category_id = "";
        page = 0;
        category_id = argPageTitle.split("#GoGrocery#")[1];
        main_category_id = argPageTitle.split("#GoGrocery#")[1];
        Log.e("select_category_main", main_category_id);
        JSONObject mJ = null;
        sortOptionSelected = "";
        if (!paramPassElasticQuery.isEmpty()) {
            try {
                mJ = new JSONObject(paramPassElasticQuery);
                mJ.remove("from");
                mJ.put("from", 0);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
        paramPassElasticQuery = mJ.toString();
        System.out.println("Rahul : ProductListingPage : sortDialog : paramPassElasticQuery : " + paramPassElasticQuery);

        mSearchModelList.clear();
        Constants.VARIABLES.FILTER_TYPE = "category";
        setItemRecyclerView();
        mActivityMainBinding.appBarInclude.itemSfl.startShimmer();
        mActivityMainBinding.appBarInclude.itemSfl.setVisibility(View.VISIBLE);
        generateIniElasticSearchQuery();
        sortOptionSelected = "";
        try {

            JSONObject melastic = new JSONObject();

            melastic.put("table_name", "EngageboostProducts")
                    .put("website_id", 1)
                    .put("data", new JSONObject(paramPassElasticQuery));
            requestProductListiing(melastic.toString());
        } catch (JSONException e) {
            e.printStackTrace();
        }

        // mActivityItemListingBinding.tvListingTitle.setText(b.getString("PageTitle"));

        //   mActivityMainBinding.appBarInclude.tabs.addTab(mActivityMainBinding.appBarInclude.tabs.newTab().setText("All"));

    }


/*    private void setTabView(List<MenuBar> mCategoryList) {
       // mActivityMainBinding.appBarInclude.tabs.addTab(mActivityMainBinding.appBarInclude.tabs.newTab().setText("All"));
        for (int k = mActivityMainBinding.appBarInclude.tabs.getTabCount(); k < mCategoryList.size(); k++) {
            mActivityMainBinding.appBarInclude.tabs.addTab(mActivityMainBinding.appBarInclude.tabs.newTab().setText(mCategoryList.get(k).getName()));
        }
    }*/


    @Override
    public void onBackPressed() {
        drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (fm != null) {
            if (fm.getBackStackEntryCount() > 0) {
                fm.popBackStackImmediate();
                // fm.popBackStack("childfrag", 0);
                System.out.println("Rahul : MainActivityNew : onBackPressed : getBackStackEntryCount : ");
            /* if (drawer.isDrawerOpen(GravityCompat.START)) {
                 drawer.closeDrawer(GravityCompat.START);
             }*/
                mActivityMainBinding.nsvSideMenu.setVisibility(View.VISIBLE);
                mActivityMainBinding.flSubmenu.setVisibility(View.GONE);

            } else if (drawer.isDrawerOpen(GravityCompat.START)) {
                drawer.closeDrawer(GravityCompat.START);
            } else {
                //super.onBackPressed();
            }
        } else {


            if (doubleBackToExitPressedOnce) {
                super.onBackPressed();
                exitApp();
            }
            this.doubleBackToExitPressedOnce = true;
            Toast.makeText(this, getResources().getString(R.string.msg_please_click_back_again_to_exit), Toast.LENGTH_SHORT).show();
            new Handler().postDelayed(new Runnable() {

                @Override
                public void run() {
                    doubleBackToExitPressedOnce = false;
                }
            }, 2000);
//                navigation.setCurrentItem(0);
//                super.onBackPressed();

//            navigation.setCurrentItem(0);
//            super.onBackPressed();
        }

    }


    private void exitApp() {
        Intent intent = new Intent(this, MainActivityNew.class);
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        finish();
    }


    /*@Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }*/

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.nav_camera) {
            // Handle the camera action
        } else if (id == R.id.nav_gallery) {

        } else if (id == R.id.nav_slideshow) {

        } else if (id == R.id.nav_manage) {

        } else if (id == R.id.nav_share) {

        } else if (id == R.id.nav_send) {

        }

        drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

    @Override
    public void redirect(String argWhich, String argExtraInfo) {

        switch (argWhich) {
            case "sideMenu":
              /*  Intent sbc = new Intent(MainActivityNew.this, ProductListingPage.class);
                sbc.putExtra("PageTitle", argPageTitile);
                startActivity(sbc);*/
                mActivityMainBinding.nsvSideMenu.setVisibility(View.GONE);
                mActivityMainBinding.flSubmenu.setVisibility(View.VISIBLE);
              /*  Animation  moveToLeft = AnimationUtils.loadAnimation(getApplicationContext(),
                        R.anim.exit_to_left);
                mActivityMainBinding.nsvSideMenu.startAnimation(moveToLeft);*/
                loadFragment(new FragmentSideMenuChild(), argExtraInfo);//extra info is child json response
                break;
            case "sbcMain":
                if (argExtraInfo.split("#GoGrocery#")[0].equals("All")) {

                    category_id = "";
                    page = 0;
                    category_id = main_category_id;
                    Log.e("select_category", category_id);
                    JSONObject mJ = null;
                    if (!paramPassElasticQuery.isEmpty()) {
                        try {
                            mJ = new JSONObject(paramPassElasticQuery);
                            mJ.remove("from");
                            mJ.put("from", 0);
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                    paramPassElasticQuery = mJ.toString();
                    System.out.println("Rahul : ProductListingPage : sortDialog : paramPassElasticQuery : " + paramPassElasticQuery);

                    mSearchModelList.clear();
                    sortOptionSelected = "";
                    setItemRecyclerView();
                    mActivityMainBinding.appBarInclude.itemSfl.startShimmer();
                    mActivityMainBinding.appBarInclude.itemSfl.setVisibility(View.VISIBLE);
                    generateIniElasticSearchQuery();


                    if (Constants.VARIABLES.brandFilterList.size() > 0) {
                        System.out.println("Rahul : FilterActivity : btnApplyFilter : brandFilterList : 5" + Constants.VARIABLES.brandFilterList.toString());
                        try {
                            mJSONElasticQuery = new JSONObject(initialparamPassElasticQuery);
                        } catch (JSONException e) {

                        }
                        JSONArray mJsonArrayBranFIlter = new JSONArray();
                        for (int i = 0; i < Constants.VARIABLES.brandFilterList.size(); i++) {
                            mJsonArrayBranFIlter.put(Integer.parseInt(Constants.VARIABLES.brandFilterList.get(i)));
                        }
                        try {
                            //  mJSONElasticQuery.getJSONObject("query").getJSONObject("bool").getJSONArray("must").put(new JSONObject().put("match", new JSONObject().put("brand_slug", new JSONObject().put("query", Constants.VARIABLES.brandFilterList.toString().replace("[", "").replace("]", "")).put("operator", "or"))));
                            // mJSONElasticQuery.getJSONObject("query").getJSONObject("bool").getJSONArray("must").put(new JSONObject().put("terms", new JSONObject().put("brand_id", mJsonArrayBranFIlter)));
                            mJSONElasticQuery.getJSONObject("query").getJSONObject("bool").getJSONArray("must").put(new JSONObject().put("terms", new JSONObject().put("brand_id", mJsonArrayBranFIlter)));
                            JSONObject mJsonObjectUpdateWithSort1 = new JSONObject(paramPassElasticQuery);
                            mJSONElasticQuery.remove("sort");
                            mJSONElasticQuery.put("sort", mJsonObjectUpdateWithSort1.getJSONArray("sort"));

                            paramPassElasticQuery = mJSONElasticQuery.toString();
                        } catch (JSONException e) {
                            System.out.println("Rahul : FilterActivity : btnApplyFilter : brandFilterList : 6");

                            e.printStackTrace();
                        }
                    }
                    try {

                        JSONObject melastic = new JSONObject();

                        melastic.put("table_name", "EngageboostProducts")
                                .put("website_id", 1)
                                .put("data", new JSONObject(paramPassElasticQuery));
                        requestProductListiing(melastic.toString());
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                } else {


                    category_id = "";
                    page = 0;
                    sortOptionSelected = "";
                    category_id = argExtraInfo.split("#GoGrocery#")[1];
                    Log.e("select_childe_category", category_id);
                    JSONObject mJ = null;
                    if (!paramPassElasticQuery.isEmpty()) {
                        try {
                            mJ = new JSONObject(paramPassElasticQuery);
                            mJ.remove("from");
                            mJ.put("from", 0);
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                    paramPassElasticQuery = mJ.toString();
                    System.out.println("Rahul : ProductListingPage : sortDialog : paramPassElasticQuery : " + paramPassElasticQuery);

                    mSearchModelList.clear();

                    setItemRecyclerView();
                    mActivityMainBinding.appBarInclude.itemSfl.startShimmer();
                    mActivityMainBinding.appBarInclude.itemSfl.setVisibility(View.VISIBLE);
                    generateIniElasticSearchQuery();

                    if (Constants.VARIABLES.brandFilterList.size() > 0) {
                        System.out.println("Rahul : FilterActivity : btnApplyFilter : brandFilterList : 5" + Constants.VARIABLES.brandFilterList.toString());
                        try {
                            mJSONElasticQuery = new JSONObject(initialparamPassElasticQuery);
                        } catch (JSONException e) {

                        }
                        JSONArray mJsonArrayBranFIlter = new JSONArray();
                        for (int i = 0; i < Constants.VARIABLES.brandFilterList.size(); i++) {
                            mJsonArrayBranFIlter.put(Integer.parseInt(Constants.VARIABLES.brandFilterList.get(i)));
                        }
                        try {
                            //  mJSONElasticQuery.getJSONObject("query").getJSONObject("bool").getJSONArray("must").put(new JSONObject().put("match", new JSONObject().put("brand_slug", new JSONObject().put("query", Constants.VARIABLES.brandFilterList.toString().replace("[", "").replace("]", "")).put("operator", "or"))));
                            // mJSONElasticQuery.getJSONObject("query").getJSONObject("bool").getJSONArray("must").put(new JSONObject().put("terms", new JSONObject().put("brand_id", mJsonArrayBranFIlter)));
                            mJSONElasticQuery.getJSONObject("query").getJSONObject("bool").getJSONArray("must").put(new JSONObject().put("terms", new JSONObject().put("brand_id", mJsonArrayBranFIlter)));
                            JSONObject mJsonObjectUpdateWithSort1 = new JSONObject(paramPassElasticQuery);
                            mJSONElasticQuery.remove("sort");
                            mJSONElasticQuery.put("sort", mJsonObjectUpdateWithSort1.getJSONArray("sort"));

                            paramPassElasticQuery = mJSONElasticQuery.toString();
                        } catch (JSONException e) {
                            System.out.println("Rahul : FilterActivity : btnApplyFilter : brandFilterList : 6");

                            e.printStackTrace();
                        }
                    }

                    try {

                        JSONObject melastic = new JSONObject();

                        melastic.put("table_name", "EngageboostProducts")
                                .put("website_id", 1)
                                .put("data", new JSONObject(paramPassElasticQuery));
                        requestProductListiing(melastic.toString());
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                }
            /*    Intent sbc = new Intent(MainActivityNew.this, ProductListingPage.class);
                sbc.putExtra("PageTitle", argExtraInfo.split("#GoGrocery#")[0]); // extra info is page title
                sbc.putExtra("Category_slug", argExtraInfo.split("#GoGrocery#")[1]); // extra info is category_slug
                startActivity(sbc);
                Constants.VARIABLES.FILTER_TYPE = "category";
                Bundle params = new Bundle();
                params.putString(FirebaseAnalytics.Param.ITEM_CATEGORY, argExtraInfo.split("#GoGrocery#")[1]);
                mFirebaseAnalytics.logEvent("visit_category", params);
                params.putString(AppEventsConstants.EVENT_PARAM_PRODUCT_CATEGORY, argExtraInfo.split("#GoGrocery#")[1]);
                logger.logEvent("visit_category", params);*/


                break;
            case "category_banner":
                Intent promotional_banner = new Intent(MainActivityNew.this, ProductListingPage.class);
                promotional_banner.putExtra("Category_slug", argExtraInfo.split("#GoGrocery#")[0]); // extra info is category_id
                promotional_banner.putExtra("PageTitle", argExtraInfo.split("#GoGrocery#")[1]); // extra info is category_id
                startActivity(promotional_banner);
                Constants.VARIABLES.FILTER_TYPE = "category";
                Bundle params_cat = new Bundle();

                params_cat.putString(FirebaseAnalytics.Param.ITEM_CATEGORY, argExtraInfo.split("#GoGrocery#")[1]);
                mFirebaseAnalytics.logEvent("visit_category", params_cat);
                params_cat.putString(AppEventsConstants.EVENT_PARAM_PRODUCT_CATEGORY, argExtraInfo.split("#GoGrocery#")[1]);
                logger.logEvent("visit_category", params_cat);
                break;
            case "childSideMenu":
                Intent childSideMenu = new Intent(MainActivityNew.this, ProductListingPage.class);
                childSideMenu.putExtra("PageTitle", argExtraInfo.split("#GoGrocery#")[1]); // extra info is page title
                childSideMenu.putExtra("Category_slug", argExtraInfo.split("#GoGrocery#")[0]); // extra info is category_slug
                startActivity(childSideMenu);
                Constants.VARIABLES.FILTER_TYPE = "category";
                Bundle paramsCat = new Bundle();
                paramsCat.putString(FirebaseAnalytics.Param.ITEM_CATEGORY, argExtraInfo.split("#GoGrocery#")[1]);
                mFirebaseAnalytics.logEvent("visit_category", paramsCat);
                paramsCat.putString(AppEventsConstants.EVENT_PARAM_PRODUCT_CATEGORY, argExtraInfo.split("#GoGrocery#")[1]);
                logger.logEvent("visit_category", paramsCat);
                break;
            case "shop_by_brand":
                Intent shop_by_brand = new Intent(MainActivityNew.this, ProductListingPage.class);
                shop_by_brand.putExtra("Category_slug", argExtraInfo.split("#GoGrocery#")[0]); // extra info is category_slug
                shop_by_brand.putExtra("PageTitle", "shop_by_brand#GoGrocery#" + argExtraInfo.split("#GoGrocery#")[1]); // extra info is category_slug
                startActivity(shop_by_brand);
                Constants.VARIABLES.FILTER_TYPE = "brand";
                Bundle params_brand = new Bundle();
                params_brand.putString(FirebaseAnalytics.Param.ITEM_BRAND, argExtraInfo.split("#GoGrocery#")[1]);
                mFirebaseAnalytics.logEvent("view_brand", params_brand);
                params_brand.putString("Item_brand", argExtraInfo.split("#GoGrocery#")[1]);
                logger.logEvent("view_brand", params_brand);

                break;


        }
    }

    public void loadFragment(Fragment fragment, String extraInfo) {

        Bundle bundle = new Bundle();
        bundle.putString("extraInfo", extraInfo);

// create a FragmentManager
        fm = getSupportFragmentManager();//****for v4 use getSupportFragmentManager
// create a FragmentTransaction to begin the transaction and replace the Fragment
        FragmentTransaction fragmentTransaction = fm.beginTransaction();
        fragment.setArguments(bundle);
        fragmentTransaction.setCustomAnimations(R.anim.enter_from_right, R.anim.exit_to_left, R.anim.enter_from_right, R.anim.exit_to_left);

        fragmentTransaction.addToBackStack("childfrag");
// replace the FrameLayout with new Fragment
        fragmentTransaction.replace(R.id.flSubmenu, fragment);


        fragmentTransaction.commit(); // save the changes
    }

    @Override
    public void onClick(View v) {

        switch (v.getId()) {
            case R.id.rlLogout:
                showLogoutPopup();
                break;
            case R.id.llSearch:
                Intent llSearch = new Intent(MainActivityNew.this, SearchActivity.class);
                startActivity(llSearch);
                drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                drawer.closeDrawer(GravityCompat.START);
                break;
            case R.id.ivContactUs:
         /*       Uri uri = Uri.parse("https://www.gogrocery.ae/contact-us"); // missing 'http://' will cause crashed
                Intent intent = new Intent(Intent.ACTION_VIEW, uri);
                startActivity(intent);*/

                Intent contact = new Intent(MainActivityNew.this, Contactus.class);
           /*     Intent contact= new Intent(MainActivityNew.this, SubstituteActivity.class);
                contact.putExtra("pushOrderID","3195");*/
                startActivity(contact);

                //  }

                break;
            case R.id.rlContactUs:

                Intent con = new Intent(MainActivityNew.this, Contactus.class);
                startActivity(con);
                drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                drawer.closeDrawer(GravityCompat.START);
//        }

                break;
            case R.id.rlHome:

                Intent ivEditLocation = new Intent(MainActivityNew.this, MapLocationSelectionUpdate.class);
                startActivity(ivEditLocation);
                drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                drawer.closeDrawer(GravityCompat.START);
                break;
            case R.id.rlAboutUS:

                Intent menuAboutus = new Intent(MainActivityNew.this, AboutUs.class);
                menuAboutus.putExtra("menuCms", "1");
                startActivity(menuAboutus);
                drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                drawer.closeDrawer(GravityCompat.START);


                break;
            case R.id.rlPrivacyPolicy:

                Intent menuPrivacyPolicy = new Intent(MainActivityNew.this, PrivacyPolicy.class);
                menuPrivacyPolicy.putExtra("menuCms", "2");
                startActivity(menuPrivacyPolicy);
                drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                drawer.closeDrawer(GravityCompat.START);


                break;
            case R.id.rlTermAndCondition:

                Intent navTermAndCondition = new Intent(MainActivityNew.this, MenuCms.class);
                // navTermAndCondition.putExtra("menuCms", "3");
                startActivity(navTermAndCondition);
                drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                drawer.closeDrawer(GravityCompat.START);


                break;
            case R.id.rlQulaityStandard:

                Intent navQulaityStandard = new Intent(MainActivityNew.this, QualityStandards.class);
                navQulaityStandard.putExtra("menuCms", "4");
                startActivity(navQulaityStandard);
                drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                drawer.closeDrawer(GravityCompat.START);


                break;
            case R.id.rlOurVisionPurpose:

                Intent navisionPurpose = new Intent(MainActivityNew.this, OurVisionPurpose.class);
                navisionPurpose.putExtra("menuCms", "5");
                startActivity(navisionPurpose);
                drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                drawer.closeDrawer(GravityCompat.START);


                break;

            case R.id.rlLanguage:

                Intent iLanguage = new Intent(MainActivityNew.this, LanguageActivity.class);

                startActivity(iLanguage);
                drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                drawer.closeDrawer(GravityCompat.START);


                break;

            case R.id.navHeaderProfile:
                if (mSharedPreferenceManager.isLoggedIn()) {
                    Intent navHeaderProfile = new Intent(MainActivityNew.this, MyAccount.class);
                    startActivity(navHeaderProfile);
                    drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                    drawer.closeDrawer(GravityCompat.START);
                } else {
                 /*   Intent navHeaderProfile = new Intent(MainActivityNew.this, LoginActivity.class);
                    navHeaderProfile.putExtra("from_where", "home");
                    startActivity(navHeaderProfile);
                    finish();*/
                    drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                    drawer.closeDrawer(GravityCompat.START);
                }
                break;
            case R.id.ivRight:

                drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                drawer.closeDrawer(GravityCompat.START);
                break;
            case R.id.ivEditType:
            case R.id.tvType:
            case R.id.ivPinType:
                //requestStoreTypeList(Double.parseDouble(mSharedPreferenceManager.getLatitude()), Double.parseDouble(mSharedPreferenceManager.getLongitude()));
                break;
            case R.id.rlChangeStore:

                /* showChangeLocationStoreDialog();*/

                try {
                    if (mSharedPreferenceManager.getTypeWarehouseId() != null && !mSharedPreferenceManager.getTypeWarehouseId().isEmpty() && mSharedPreferenceManager.getLatitude() != null && !mSharedPreferenceManager.getLatitude().isEmpty() && mSharedPreferenceManager.getLongitude() != null && !mSharedPreferenceManager.getLatitude().isEmpty()) {
                        typeID = new JSONArray(mSharedPreferenceManager.getTypeWarehouseId());
                      /*  requestWarehouseList(Double.parseDouble(mSharedPreferenceManager.getLatitude()), Double.parseDouble(mSharedPreferenceManager.getLongitude()), typeID);*/
                        Intent i = new Intent(MainActivityNew.this, SelectStore.class);
                        i.putExtra("type_id",typeID.toString());
                        i.putExtra("latitude", mSharedPreferenceManager.getLatitude());
                        i.putExtra("longitude", mSharedPreferenceManager.getLongitude());
                        i.putExtra("from_where", "home");
                        //i.putExtra("store_list",warehouseList);
                        startActivity(i);
                        drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                        drawer.closeDrawer(GravityCompat.START);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }

                break;
            case R.id.llChangeStore:

                try {
                    if (mSharedPreferenceManager.getTypeWarehouseId() != null && !mSharedPreferenceManager.getTypeWarehouseId().isEmpty() && mSharedPreferenceManager.getLatitude() != null && !mSharedPreferenceManager.getLatitude().isEmpty() && mSharedPreferenceManager.getLongitude() != null && !mSharedPreferenceManager.getLatitude().isEmpty()) {
                        typeID = new JSONArray(mSharedPreferenceManager.getTypeWarehouseId());
                        /*  requestWarehouseList(Double.parseDouble(mSharedPreferenceManager.getLatitude()), Double.parseDouble(mSharedPreferenceManager.getLongitude()), typeID);*/
                        Intent i = new Intent(MainActivityNew.this, SelectStore.class);
                        i.putExtra("type_id",typeID.toString());
                        i.putExtra("latitude", mSharedPreferenceManager.getLatitude());
                        i.putExtra("longitude", mSharedPreferenceManager.getLongitude());
                        i.putExtra("from_where", "home");
                        //i.putExtra("store_list",warehouseList);
                        startActivity(i);
                        drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                        drawer.closeDrawer(GravityCompat.START);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }

                break;

            case R.id.ivEditLocationName:
                Intent ivEditLocationName = new Intent(MainActivityNew.this, MapLocationSelectionUpdate.class);
                startActivity(ivEditLocationName);
                break;
            case R.id.tvLocationName:
                Intent tvLocationName = new Intent(MainActivityNew.this, MapLocationSelectionUpdate.class);
                startActivity(tvLocationName);
                break;
            case R.id.ivPinLocation:
                Intent ivPinLocation = new Intent(MainActivityNew.this, MapLocationSelectionUpdate.class);
                startActivity(ivPinLocation);
                break;

            case R.id.ivLocationPin:
                Intent location = new Intent(MainActivityNew.this, MapLocationSelectionUpdate.class);
                startActivity(location);
                break;
            case R.id.tvViewCart:
                Intent ivCart = new Intent(MainActivityNew.this, MyCart.class);
                startActivity(ivCart);
                break;
            case R.id.ivSortBy:
                sortDialog();
                break;
            case R.id.ivFav:

                Intent rlCart = new Intent(MainActivityNew.this, MyCart.class);
                startActivity(rlCart);
              /*  if (mActivityMainBinding.appBarInclude.rlExpandViewCart.getVisibility() == View.VISIBLE) {
                    mActivityMainBinding.appBarInclude.rlExpandViewCart.setVisibility(View.GONE);
                } else {
                    Transition transition = new Slide(Gravity.END);
                    transition.setDuration(600);
                    transition.addTarget(R.id.image);

                    TransitionManager.beginDelayedTransition(mActivityMainBinding.appBarInclude.parent, transition);
                    mActivityMainBinding.appBarInclude.rlExpandViewCart.setVisibility(View.VISIBLE);
                }*/
                break;
            case R.id.rlBtnCart:
                Intent ivcart = new Intent(MainActivityNew.this, MyCart.class);
                startActivity(ivcart);
                break;


            case R.id.rlMyCart:
                Intent rlMyCart = new Intent(MainActivityNew.this, MyCart.class);
                startActivity(rlMyCart);
                drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                drawer.closeDrawer(GravityCompat.START);
                break;
            case R.id.rlMyAccount:
                if (mSharedPreferenceManager.isLoggedIn()) {
                    Intent rlMyAccount = new Intent(MainActivityNew.this, MyAccount.class);
                    startActivity(rlMyAccount);
                    drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                    drawer.closeDrawer(GravityCompat.START);
                } else {
                    Intent i = new Intent(MainActivityNew.this, LoginActivity.class);
                    i.putExtra("from_where", "home");
                    startActivity(i);
                    finish();
                }
                break;
            case R.id.rlMyWishlist:
                if (mSharedPreferenceManager.isLoggedIn()) {
                    Intent rlMyWishlist = new Intent(MainActivityNew.this, WishListPage.class);
                    startActivity(rlMyWishlist);
                    drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                    drawer.closeDrawer(GravityCompat.START);
                } else {
                    Intent i = new Intent(MainActivityNew.this, LoginActivity.class);
                    i.putExtra("from_where", "home");
                    startActivity(i);
                    drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                    drawer.closeDrawer(GravityCompat.START);
                }
                break;
            case R.id.rlMyOrders:
                if (mSharedPreferenceManager.isLoggedIn()) {
                    Intent rlMyOrders = new Intent(MainActivityNew.this, MyOrders.class);

                    startActivity(rlMyOrders);
                    drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                    drawer.closeDrawer(GravityCompat.START);


                } else {
                    Intent i = new Intent(MainActivityNew.this, LoginActivity.class);
                    i.putExtra("from_where", "home");
                    startActivity(i);
                    drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                    drawer.closeDrawer(GravityCompat.START);
                }
                break;
            case R.id.rlShopCategory:
                Intent i2 = new Intent(MainActivityNew.this, CategoryFragment.class);
                drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                drawer.closeDrawer(GravityCompat.START);
                startActivity(i2);


                break;
            case R.id.rlLogin:
                Intent i = new Intent(MainActivityNew.this, LoginActivity.class);
                i.putExtra("from_where", "home");
                startActivity(i);
                break;
            case R.id.txtFilter:

                Intent rlFilters = new Intent(MainActivityNew.this, FilterActivityNew.class);
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
             //   filterDialog();
                break;
            case R.id.rlProductSubstitute:
                if (mSharedPreferenceManager.isLoggedIn()) {

                    Intent rlProductSubstitute = new Intent(MainActivityNew.this, ProductSubstitutions.class);
                    startActivity(rlProductSubstitute);
                    drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                    drawer.closeDrawer(GravityCompat.START);
                } else {
                    Intent ps = new Intent(MainActivityNew.this, LoginActivity.class);
                    ps.putExtra("from_where", "home");
                    startActivity(ps);
                    drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                    drawer.closeDrawer(GravityCompat.START);
                }
                break;

        }


    }


    private void sortDialog() {
        BottomSheetDialog mSortDialog = new BottomSheetDialog(this, R.style.BottomSheetDialog);
        View sheetView = this.getLayoutInflater().inflate(R.layout.sort_option_dialog, null);
        mSortDialog.setContentView(sheetView);
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

        rgSortOption.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            public void onCheckedChanged(RadioGroup group, int checkedId) {
                System.out.println("Rahul : ProductListingPage : sortDialog : selected : " + checkedId);
                JSONObject mJ = null;
                if(paramPassElasticQuery!=null&&!paramPassElasticQuery.isEmpty()) {
                    switch (checkedId) {
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
                            // do operations specific to this selection
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
                }

                try {

                    mJ.remove("from");
                    mJ.put("from", 0);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                paramPassElasticQuery = String.valueOf(mJ);
                System.out.println("Rahul : ProductListingPage : sortDialog : paramPassElasticQuery : " + paramPassElasticQuery);

                mSearchModelList.clear();
                mActivityMainBinding.appBarInclude.itemSfl.startShimmer();
                mActivityMainBinding.appBarInclude.itemSfl.setVisibility(View.VISIBLE);
                setItemRecyclerView();

                try {

                    JSONObject melastic = new JSONObject();

                    melastic.put("table_name", "EngageboostProducts")
                            .put("website_id", 1)
                            .put("data", new JSONObject(paramPassElasticQuery));
                    requestProductListiing(melastic.toString());
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                mSortDialog.dismiss();
            }
        });


    /*    {

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

                    setItemRecyclerView();

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
        }*/

      /*  dialogBtnApply.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
        });
*/
        dialogBtnCancel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mSortDialog.dismiss();
            }
        });
        mSortDialog.show();

    }

  /*  public void requestStoreTypeList(double latitude, double longitude) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("latitude", latitude);
        mJsonObject.put("longitude", longitude);
        mJsonObject.put("website_id", 1);

        System.out.println("Rahul : MapLocationSelectionUpdate : requestStoreTypeList : mJsonObject : " + mJsonObject);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.STORE_TYPE, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : MapLocationSelectionUpdate : requestStoreTypeList : response : " + response);
                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        StoreTypeModel storeTypeModel = mGson.fromJson(response.toString(), StoreTypeModel.class);
                        if (storeTypeModel.getStatus() == 1) {
                            showBottomSheetTypeDialog(storeTypeModel.getData(), latitude, longitude);

                        } else {

                        }
                    }

                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                System.out.println("Rahul : MapLocationSelectionUpdate : requestStoreTypeList : error : " + error);
            }
        });

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
    }*/

   /* private void showBottomSheetTypeDialog(List<DataItem> data, double latitude, double longitude) {

        mBottomSheetTypeDialog = new Dialog(MainActivityNew.this, R.style.DialogSlideAnimStyle);
        mBottomSheetTypeDialog.setContentView(R.layout.bottom_sheet_store_type);
        mBottomSheetTypeDialog.setCancelable(true);

        RecyclerView mRecyclerView = mBottomSheetTypeDialog.findViewById(R.id.rvStoreType);

        ImageView ivBack = mBottomSheetTypeDialog.findViewById(R.id.ivBack);
        LinearLayout llStart = mBottomSheetTypeDialog.findViewById(R.id.llStart);
        ArrayList<StoreCategoryModel> typeModels = new ArrayList<>();
        typeModels.add(new StoreCategoryModel("All", 0, true, 1));
        for (int i = 0; i < data.size(); i++) {
            StoreCategoryModel tmp = new StoreCategoryModel(data.get(i).getName(), data.get(i).getId(), true, data.get(i).getHas_store());
            typeModels.add(tmp);
        }

        llStart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    JSONArray storetype_id = new JSONArray();
                    for (int i = 0; i < typeModels.size(); i++) {
                        if (typeModels.get(i).isSelect()) {
                            storetype_id.put(typeModels.get(i).getId());
                        }
                    }
                    if (storetype_id.length() > 0) {
                        typeID = storetype_id;
                        requestWarehouseList(latitude, longitude, storetype_id);
                    } else {
                        new AlertDialog.Builder(MainActivityNew.this)
                                .setTitle("NOTE")
                                .setMessage("Please select category to start shopping")

                                // Specifying a listener allows you to take an action before dismissing the dialog.
                                // The dialog is automatically dismissed when a dialog button is clicked.
                                .setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() {
                                    public void onClick(DialogInterface dialog, int which) {
                                        dialog.dismiss();
                                    }
                                })

                                // A null listener allows the button to dismiss the dialog and take no further action.
                                //.setNegativeButton(android.R.string.no, null)
                                .setIcon(android.R.drawable.ic_dialog_alert)
                                .show();
                        //Constants.showToastInMiddle(MainActivityNew.this,"Please select category to start shopping");
                        //showNoStoreDialog();
                    }

                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });

        ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent ivEditLocation = new Intent(MainActivityNew.this, MapLocationSelectionUpdate.class);
                startActivity(ivEditLocation);
                mBottomSheetTypeDialog.dismiss();
            }
        });
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext());
        mRecyclerView.setLayoutManager(mLayoutManager);
        *//* mRecyclerView.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));*//*

        mRecyclerView.setAdapter(new StoreTypeAdapter(this, typeModels, new StoreTypeItemClickListner() {
            @Override
            public void clickStoreTypeItemClickListner(long id, String name, int position) {
            }
        }));
        mRecyclerView.setNestedScrollingEnabled(false);

        try {
            if (!mBottomSheetTypeDialog.isShowing()) {
                mBottomSheetTypeDialog.show();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }


       *//* getWindow().setGravity(Gravity.BOTTOM);
        getWindow().setBackgroundDrawableResource(android.R.color.transparent);*//*
    }*/

   /* public void requestWarehouseList(double argLat, double argLong, JSONArray storetype_id) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(MainActivityNew.this);
        loadingDialog.showDialog();
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("latitude", argLat);
        mJsonObject.put("longitude", argLong);
        mJsonObject.put("website_id", 1);
        mJsonObject.put("storetype_id", storetype_id);

        System.out.println("Rahul : MapLocationSelectionUpdate : requestWarehouseList : mJsonObject : " + mJsonObject);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.WAREHOUSE_LIST, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        loadingDialog.hideDialog();
                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        System.out.println("Rahul : MapLocationSelectionUpdate : requestWarehouseList : response : " + response);
                        WarehouseModel mWarehouseModel = mGson.fromJson(response.toString(), WarehouseModel.class);
                        if (!mWarehouseModel.getStatus().equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                            if (mBottomSheetTypeDialog != null) {
                                mBottomSheetTypeDialog.dismiss();
                            }
                            mWarehouseList.clear();
                            mWarehouseList.addAll(mWarehouseModel.getData());
                            System.out.println("Rahul : MapLocationSelectionUpdate : requestWarehouseList : mWarehouseList : " + mGson.toJson(mWarehouseList));
                            showBottomSheetDialog();

                        } else {

                        }
//                        findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                    }

                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : MapLocationSelectionUpdate : requestWarehouseList : VolleyError : " + error.toString());
                loadingDialog.hideDialog();
                //  findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                //showNoDeliveryDialog();
                showNoStoreDialog();
            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");

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
    }*/

   /* private void showBottomSheetDialog() {

        mBottomSheetDialog = new Dialog(MainActivityNew.this, R.style.DialogSlideAnimStyle);
        mBottomSheetDialog.setContentView(R.layout.bottom_sheet_warehouse);
        mBottomSheetDialog.setCancelable(true);

        RecyclerView mRecyclerView = mBottomSheetDialog.findViewById(R.id.rvWarehouse);

        ImageView ivBack = mBottomSheetDialog.findViewById(R.id.ivBack);
        ImageView ivClose = mBottomSheetDialog.findViewById(R.id.ivClose);
        ivClose.setVisibility(View.VISIBLE);
        ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    if (mSharedPreferenceManager.getLatitude() != null && !mSharedPreferenceManager.getLatitude().isEmpty() && mSharedPreferenceManager.getLongitude() != null && !mSharedPreferenceManager.getLatitude().isEmpty()) {
                        requestStoreTypeList(Double.parseDouble(mSharedPreferenceManager.getLatitude()), Double.parseDouble(mSharedPreferenceManager.getLongitude()));
                    }
                    mBottomSheetDialog.dismiss();
                } catch (JSONException e) {
                    e.printStackTrace();
                }

            }
        });

        ivClose.setOnClickListener(v -> {
            mBottomSheetDialog.dismiss();
        });

        WarehouseAdapter mWarehouseAdapter = new WarehouseAdapter(getApplicationContext(), mWarehouseList, new WarehouseItemClickListner() {
            @Override
            public void clickWarehouseItemClickListner(double argLat, double argLong, String argWarehouseID, String argWarehouseName) {
                if (new SharedPreferenceManager(getApplicationContext()).getWarehouseId().isEmpty()) {
                    Intent i = new Intent(MainActivityNew.this, MainActivityNew.class);
                    startActivity(i);
                    SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
                    mSharedPreferenceManager.storeLatLong(String.valueOf(argLat) + "," + argLong);
                    mSharedPreferenceManager.storeWarehouseId(argWarehouseID);
                    mSharedPreferenceManager.storeWarehouseName(argWarehouseName);
                    mSharedPreferenceManager.storeTypeWarehouseName(argWarehouseName);
                    mSharedPreferenceManager.storeTypeWarehouseId(typeID.toString());
                    finish();
                } else if (argWarehouseID.equals(new SharedPreferenceManager(getApplicationContext()).getWarehouseId())) {
                    Intent i = new Intent(MainActivityNew.this, MainActivityNew.class);
                    startActivity(i);
                    SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
                    mSharedPreferenceManager.storeLatLong(String.valueOf(argLat) + "," + argLong);
                    mSharedPreferenceManager.storeWarehouseId(argWarehouseID);
                    mSharedPreferenceManager.storeWarehouseName(argWarehouseName);
                    mSharedPreferenceManager.storeTypeWarehouseName(argWarehouseName);
                    mSharedPreferenceManager.storeTypeWarehouseId(typeID.toString());
                    finish();
                } else if (Constants.VARIABLES.CART_COUNT == 0) {
                    Intent i = new Intent(MainActivityNew.this, MainActivityNew.class);
                    startActivity(i);
                    SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
                    mSharedPreferenceManager.storeLatLong(String.valueOf(argLat) + "," + argLong);
                    mSharedPreferenceManager.storeWarehouseId(argWarehouseID);
                    mSharedPreferenceManager.storeWarehouseName(argWarehouseName);
                    mSharedPreferenceManager.storeTypeWarehouseName(argWarehouseName);
                    mSharedPreferenceManager.storeTypeWarehouseId(typeID.toString());
                    finish();
                } else {

                    Dialog mDialog = new Dialog(MainActivityNew.this);
                    mDialog.setCancelable(false);
                    mDialog.setContentView(R.layout.change_warehouse_dialog);

                    Button btnYes, btnNo;
                    btnYes = mDialog.findViewById(R.id.btnYes);
                    btnNo = mDialog.findViewById(R.id.btnNo);


                    btnYes.setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View v) {
                            try {
                                requestEmptyCart(argLat, argLong, argWarehouseID, argWarehouseName);
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


                }
            }
        });
       *//* GridLayoutManager mGridLayoutManager = new GridLayoutManager(getApplicationContext(), 2);
        mRecyclerView.setLayoutManager(mGridLayoutManager);
        mRecyclerView.addItemDecoration(new GridSpacingItemDecoration(2, GridSpacingItemDecoration.dpToPx(getApplicationContext(), 10), true));

        // mRecyclerView.addItemDecoration(new ItemDecorationAlbumColumns(10, 100));
        mRecyclerView.setLayoutManager(mGridLayoutManager);
        mRecyclerView.setItemAnimator(new DefaultItemAnimator());*//*

        GridLayoutManager mLayoutManager = new GridLayoutManager(getApplicationContext(), 2);
        mRecyclerView.setLayoutManager(mLayoutManager);
        *//* mRecyclerView.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));*//*

        mRecyclerView.setAdapter(mWarehouseAdapter);
        mRecyclerView.setNestedScrollingEnabled(false);
        try {

            if (!mBottomSheetDialog.isShowing()) {
                mBottomSheetDialog.show();
            }

        } catch (Exception e) {
            e.printStackTrace();

        }


       *//* getWindow().setGravity(Gravity.BOTTOM);
        getWindow().setBackgroundDrawableResource(android.R.color.transparent);*//*
    }*/

   /* public void requestEmptyCart(double argLat, double argLong, String argWarehouseID, String argWarehouseName) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        loadingDialog.showDialog();
//        findViewById(R.id.progressSpinKitView).setVisibility(View.VISIBLE);
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));
        mJsonObject.put("website_id", 1);

        System.out.println("Rahul : MapLocationSelectionUpdate : requestEmptyCart : mJsonObject : " + mJsonObject.toString());

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.EMPTY_CART, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        loadingDialog.hideDialog();
                        System.out.println("Rahul : MapLocationSelectionUpdate : requestEmptyCart : response : " + response.toString());
//                        findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                        try {
                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                new DatabaseHandler(getApplicationContext()).deleteAllRecord();
                                Constants.VARIABLES.CART_COUNT = 0;
                                mActivityMainBinding.appBarInclude.tvCartCount.setVisibility(View.GONE);
                                mActivityMainBinding.appBarInclude.tvCartSubTotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble("0.00")));
                                Intent i = new Intent(MainActivityNew.this, MainActivityNew.class);
                                startActivity(i);
                                SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
                                mSharedPreferenceManager.storeLatLong(String.valueOf(argLat) + "," + argLong);
                                mSharedPreferenceManager.storeWarehouseId(argWarehouseID);
                                mSharedPreferenceManager.storeWarehouseName(argWarehouseName);
                                finish();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
//                findViewById(R.id.progressSpinKitView).setVisibility(View.GONE);
                loadingDialog.hideDialog();
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
    }*/

    public void showNoDeliveryDialog() {
        Dialog mSomethingwentworng = new Dialog(MainActivityNew.this);
        mSomethingwentworng.setCancelable(false);
        mSomethingwentworng.setContentView(R.layout.no_delivery_dialog);
        TextView txtOk = mSomethingwentworng.findViewById(R.id.txtOk);
        txtOk.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mSomethingwentworng.dismiss();
            }
        });
        mSomethingwentworng.show();

    }

    public void showNoStoreDialog() {
        Dialog mSomethingwentworng = new Dialog(MainActivityNew.this);
        mSomethingwentworng.setCancelable(false);
        mSomethingwentworng.setContentView(R.layout.no_store_available_dialog);
        TextView txtOk = mSomethingwentworng.findViewById(R.id.txtOk);
        txtOk.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mSomethingwentworng.dismiss();
            }
        });

        mSomethingwentworng.show();

    }

    private void getFcmToken() {
        FirebaseInstanceId.getInstance().getInstanceId()
                .addOnCompleteListener(new OnCompleteListener<InstanceIdResult>() {
                    @Override
                    public void onComplete(@NonNull Task<InstanceIdResult> task) {
                        if (!task.isSuccessful()) {
//                            Log.w(TAG, "getInstanceId failed", task.getException());
                            return;
                        }

                        // Get new Instance ID token
                        String token = task.getResult().getToken();

                        mSharedPreferenceManager.saveDevKey(token);
                        Log.e("Dev_key", token.toString());
                        // Log and toast
//            String msg = getString(R.string.msg_token_fmt, token);
//            Log.d(TAG, msg);
//            Toast.makeText(SplashScreenActivity.this, msg, Toast.LENGTH_SHORT).show();
                    }
                });
    }

    public void AnimateBell() {
        Animation shake = AnimationUtils.loadAnimation(getApplicationContext(), R.anim.shake);


        mActivityMainBinding.appBarInclude.tvCartCount.setVisibility(View.VISIBLE);
      //  mActivityMainBinding.appBarInclude.ivFav.setImageResource(R.drawable.cart);
        mActivityMainBinding.appBarInclude.ivFav.setAnimation(shake);
        mActivityMainBinding.appBarInclude.ivFav.startAnimation(shake);


        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {

            }
        }, 500);
        System.out.println("Rahul : MainActivityNew : AnimateBell : ");
    }

    @Override
    public void connectMain(int argProductId, int argQuantity,int position) {


        try {

            requestAddToCart(argProductId, argQuantity, "", "",position);
        } catch (JSONException e) {
            e.printStackTrace();
        }


    }


    public void requestAddToCart(int argProductId, int argQty, String customFieldName, String customFieldValue,int position) throws JSONException {
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


        mActivityMainBinding.appBarInclude.progressSpinKitView.setVisibility(View.VISIBLE);
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
                                Constants.VARIABLES.CART_COUNT = 0;
                                mActivityMainBinding.appBarInclude.tvCartCount.setVisibility(View.GONE);
                                mActivityMainBinding.appBarInclude.tvCartSubTotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble("0.00")));
                            } else {

                                mActivityMainBinding.appBarInclude.tvCartCount.setVisibility(View.VISIBLE);
                                mActivityMainBinding.appBarInclude.tvCartCount.setText(mAddToCartModel.getCartData().getCart_count());
                                Constants.VARIABLES.CART_COUNT = Integer.parseInt(mAddToCartModel.getCartData().getCart_count());
                                mActivityMainBinding.appBarInclude.tvCartSubTotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff((mAddToCartModel.getCartData().getOrderamountdetails().get(0).getGrandTotal())));

                                Bundle params = new Bundle();
                         /*       params.putString("productName",mAddToCartModel.getCartData().getCartdetails().get(0).getName());
                                params.putString("productId",mAddToCartModel.getCartData().getCartdetails().get(0).getId());
                                params.putString("addedQuanity",mAddToCartModel.getCartData().getCart_count());
                                params.putString("content_type","product");
                                params.putString("currency", Constants.VARIABLES.CURRENT_CURRENCY);
                                mFirebaseAnalytics.logEvent(FirebaseAnalytics.Event.ADD_TO_CART, params);
                                logger.logEvent(AppEventsConstants.EVENT_NAME_ADDED_TO_CART, params);*/
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
                                AnimateBell();

                                System.out.println("Rahul : ProductListingPage : checkDbCount : " + mDatabaseHandler.getAllProductQtyData().size());
                            }

                            if (Integer.parseInt(mAddToCartModel.getCartData().getCart_count()) == 0) {
                                Constants.VARIABLES.CART_COUNT = 0;
                                mActivityMainBinding.appBarInclude.tvCartCount.setVisibility(View.GONE);
                                mActivityMainBinding.appBarInclude.tvCartSubTotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble("0.00")));
                                // mActivityItemListingBinding.badgeNotification.setVisibility(View.GONE);

                            } else {
                                mActivityMainBinding.appBarInclude.tvCartCount.setVisibility(View.VISIBLE);
                                mActivityMainBinding.appBarInclude.tvCartCount.setText(mAddToCartModel.getCartData().getCart_count());
                                Constants.VARIABLES.CART_COUNT = Integer.parseInt(mAddToCartModel.getCartData().getCart_count());
                                mActivityMainBinding.appBarInclude.tvCartSubTotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff((mAddToCartModel.getCartData().getOrderamountdetails().get(0).getGrandTotal())));
                            }


                        } else {

                            try {
                                if (response.getString("is_age_verification").equals("False")) {
                                    Intent i = new Intent(MainActivityNew.this, TobacoCatActivity.class);
                                    i.putExtra("message", mAddToCartModel.getMsg());
                                    startActivity(i);
                                } else {
                                    Constants.showToastInMiddle(getApplicationContext(), mAddToCartModel.getMsg());
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }


                            //Toast.makeText(getApplicationContext(), mAddToCartModel.getMsg(), Toast.LENGTH_LONG).show();

                        }
                     //   mainItemListingAdapter.notifyDataSetChanged();
                        mainItemListingAdapter.notifyItemChanged(position);
                        mActivityMainBinding.appBarInclude.progressSpinKitView.setVisibility(View.GONE);

                    }
                }, new com.android.volley.Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : ProductListingPage : requestAddToCart : VolleyError : " + error.toString());
                mActivityMainBinding.appBarInclude.progressSpinKitView.setVisibility(View.GONE);
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

    public void requestViewCart() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        System.out.println("Rahul : MainActivityNew : requestViewCart : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.VIEW_CART, null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {

                        System.out.println("Rahul : MainActivityNew : requestViewCart : mJsonObject : " + response);
                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        System.out.println("Rahul : MainActivityNew : requestViewCart : mJsonObject : " + mJsonObject);
                        ViewCartModel mViewCartModel = mGson.fromJson(response.toString(), ViewCartModel.class);
                        if (!mViewCartModel.getCartCount().equals("0")) {
                            //mActivityMainBinding.appBarInclude.badgeNotification.setVisibility(View.VISIBLE);
                            //mActivityMainBinding.appBarInclude.badgeNotification.setText(mViewCartModel.getCart_count_itemwise());
                            mActivityMainBinding.appBarInclude.tvCartCount.setVisibility(View.VISIBLE);
                            mActivityMainBinding.appBarInclude.tvCartCount.setText(mViewCartModel.getCart_count_itemwise());
                            mActivityMainBinding.appBarInclude.tvCartSubTotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mViewCartModel.getTotalAmount())));
                            Constants.VARIABLES.CART_SUB_AMOUNT = Constants.twoDecimalRoundOff(Double.parseDouble(mViewCartModel.getTotalAmount()));

                            Constants.VARIABLES.CART_COUNT = Integer.parseInt(mViewCartModel.getCart_count_itemwise());
                            for (int i = 0; i < mViewCartModel.getData().size(); i++) {
                                ProductQuantityLocal mProductQuantityLocal = new ProductQuantityLocal(String.valueOf(mViewCartModel.getData().get(i).getProductId()), String.valueOf(mViewCartModel.getData().get(i).getQuantity()));
                                if (!mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(mViewCartModel.getData().get(i).getProductId())).equals("0")) {
                                    mDatabaseHandler.updateProductQuantityById(mProductQuantityLocal);
                                } else {
                                    mDatabaseHandler.addProductQty(mProductQuantityLocal);
                                }

                            }

                        } else {
                            mDatabaseHandler.deleteAllRecord();
                            Constants.VARIABLES.CART_COUNT = 0;
                            mActivityMainBinding.appBarInclude.tvCartCount.setVisibility(View.GONE);
                            mActivityMainBinding.appBarInclude.tvCartSubTotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble("0.00")));
                            //mActivityMainBinding.appBarInclude.badgeNotification.setVisibility(View.GONE);
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                Constants.VARIABLES.CART_COUNT = 0;
                mDatabaseHandler.deleteAllRecord();
                //mActivityMainBinding.appBarInclude.badgeNotification.setVisibility(View.GONE);
                mActivityMainBinding.appBarInclude.tvCartCount.setVisibility(View.GONE);
                mActivityMainBinding.appBarInclude.tvCartSubTotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble("0.00")));
                System.out.println("Rahul : MainActivityNew : requestViewCart : VolleyError : " + error.toString());
                if (error.equals("com.android.volley.ParseError")) {
                    System.out.println("Rahul : MainActivityNew : requestViewCart : VolleyError : ParseError ");

                }
            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put(Constants.VARIABLES.WAREHOUSE_KEY, mSharedPreferenceManager.getWarehouseId());
                if (mSharedPreferenceManager.isLoggedIn()) {
                    headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                } else {
                    headers.put("DEVICEID", Constants.getDeviceId(getApplicationContext()));
                }

               /* if (mSharedPreferenceManager.isLoggedIn()) {
                    headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                } else {
                    headers.put("DEVICEID", Constants.getDeviceId(getApplicationContext()));
                }*/

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
        mActivityMainBinding.appBarInclude.progressSpinKitView.setVisibility(View.VISIBLE);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                CURRENT_URL, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        mActivityMainBinding.appBarInclude.progressSpinKitView.setVisibility(View.GONE);
                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        System.out.println("Rahul : MainActivityNew : requestAddToWishlist : mJsonObject : " + mJsonObject);

                        try {
                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();
                                if (argAction.equals("add")) {
                                    if (!mDatabaseHandler.checkWishlistAvailable("" + argProductId)) {
                                        mDatabaseHandler.addWishlistData("" + argProductId);
                                    }

                                } else {
                                    if (mDatabaseHandler.checkWishlistAvailable("" + argProductId)) {
                                        mDatabaseHandler.deleteWishlistSingleRecord("" + argProductId);
                                    }
                                }

                                if (mNewCMSBestSellingProductAdapter != null) {
                                    mNewCMSBestSellingProductAdapter.notifyDataSetChanged();
                                }
                                if (mNewCMSPromotionalProductsAdapter != null) {
                                    mNewCMSPromotionalProductsAdapter.notifyDataSetChanged();
                                }
                            } else {
                                Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();

                            }
                        } catch (JSONException e) {
                            e.printStackTrace();

                        }

                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : MainActivityNew : requestAddToCart : VolleyError : " + error.toString());
                mActivityMainBinding.appBarInclude.progressSpinKitView.setVisibility(View.GONE);

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


    private void showLogoutPopup() {
        new MaterialDialog.Builder(this)
                .title(getResources().getString(R.string.dialogTitle_logout))
                .content(getResources().getString(R.string.dialogMessage_logout))
                .positiveText(getResources().getString(R.string.dialogPositiveButtonText_logout))
                .positiveColor(ContextCompat.getColor(this, R.color.green_new))
                .negativeText(getResources().getString(R.string.dialogPositiveButtonText_cancel))
                .negativeColor(ContextCompat.getColor(this, R.color.Title))
                .onPositive((dialog, which) -> {
                    try {
                        requestLogout();
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                })
                .onNegative((dialog, which) -> {
                    drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
                    drawer.closeDrawer(GravityCompat.START);
                    dialog.dismiss();
                }).show();
    }

    public void requestLogout() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));
        mJsonObject.put("ip_address", "");
        mActivityMainBinding.appBarInclude.progressSpinKitView.setVisibility(View.VISIBLE);
        System.out.println("Rahul : MyAccount : requestMyProfile : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL_SUBSTITUTE + Constants.API_METHODS.LOGOUT, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        mActivityMainBinding.appBarInclude.progressSpinKitView.setVisibility(View.GONE);
                        try {
                            if (response.getInt("status") == 1) {
                                Intent rlLogout = new Intent(MainActivityNew.this, LoginActivity.class);
                                if (Constants.mGoogleSignInClient != null) {
                                    Constants.mGoogleSignInClient.signOut();
                                }


                                LoginManager.getInstance().logOut();
                                mSharedPreferenceManager.logoutUser();
                              /*  mDatabaseHandler.deleteAllRecord();
                                mDatabaseHandler.deleteAllRecordWishlist();*/
                                startActivity(rlLogout);
                                finish();


                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                        System.out.println("Rahul : MyAccount : requestLogout : mJsonObject : " + response);


                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mActivityMainBinding.appBarInclude.progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : MyAccount : requestLogout : VolleyError : " + error.toString());
            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));

                return headers;
            }


        };


        // Adding request to request queue
        queue.add(jsonObjReq);
    }


    public void requestUpdateToken() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JSONObject mJsonObject = new JSONObject();


        mJsonObject.put("os_version", android.os.Build.VERSION.SDK_INT);
        mJsonObject.put("device_token", mSharedPreferenceManager.getDebKey());
        mJsonObject.put("device_type", "a");
        mJsonObject.put("version", Constants.getAppVersion(getApplicationContext()));//dev
        System.out.println("Sukdev : MainActivityNew : updateToken : param : " + mJsonObject);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.UPDATE_DEVICE_DETAILS, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {

                        ;
                        JSONObject mJsonObject = response;
                        System.out.println("Sukdev : Main : requestUpdateToken response  : " + mJsonObject);


                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {


                System.out.println("Sukdev : Main : requestUpdateToken : VolleyError : " + error.toString());

            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put(Constants.VARIABLES.WAREHOUSE_KEY, mSharedPreferenceManager.getWarehouseId());
                headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                headers.put("DEVICEID", Constants.getDeviceId(getApplicationContext()));


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
        // Adding request to request queue
        queue.add(jsonObjReq);
    }


    private void showChangeLocationStoreDialog() {
        mChangeStoreLocation = new Dialog(this);
        mChangeStoreLocation.setContentView(R.layout.change_location_store_dialog);
        mChangeStoreLocation.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        mChangeStoreLocation.setCanceledOnTouchOutside(true);
        CardView close = mChangeStoreLocation.findViewById(R.id.cv_close);
        Button btnChangeStore = mChangeStoreLocation.findViewById(R.id.btnChangeStore);
        Button btnChangeStoreType = mChangeStoreLocation.findViewById(R.id.btnChangeStoreType);
        Button btnChangeLocation = mChangeStoreLocation.findViewById(R.id.btnChangeLocation);


        close.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mChangeStoreLocation.dismiss();
            }
        });

        btnChangeStore.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    if (mSharedPreferenceManager.getTypeWarehouseId() != null && !mSharedPreferenceManager.getTypeWarehouseId().isEmpty() && mSharedPreferenceManager.getLatitude() != null && !mSharedPreferenceManager.getLatitude().isEmpty() && mSharedPreferenceManager.getLongitude() != null && !mSharedPreferenceManager.getLatitude().isEmpty()) {
                        typeID = new JSONArray(mSharedPreferenceManager.getTypeWarehouseId());
                       // requestWarehouseList(Double.parseDouble(mSharedPreferenceManager.getLatitude()), Double.parseDouble(mSharedPreferenceManager.getLongitude()), typeID);
                    }
                    mChangeStoreLocation.dismiss();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });
        btnChangeStoreType.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    if (mSharedPreferenceManager.getLatitude() != null && !mSharedPreferenceManager.getLatitude().isEmpty() && mSharedPreferenceManager.getLongitude() != null && !mSharedPreferenceManager.getLatitude().isEmpty()) {
                       // requestStoreTypeList(Double.parseDouble(mSharedPreferenceManager.getLatitude()), Double.parseDouble(mSharedPreferenceManager.getLongitude()));
                    }
                    mChangeStoreLocation.dismiss();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });
        btnChangeLocation.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent ivEditLocation = new Intent(MainActivityNew.this, MapLocationSelectionUpdate.class);
                startActivity(ivEditLocation);
                mChangeStoreLocation.dismiss();
            }
        });

        mChangeStoreLocation.show();

    }







    @Override
    protected void onResume() {
        if (mainItemListingAdapter != null) {
            mainItemListingAdapter.notifyDataSetChanged();
        }

        if (Constants.VARIABLES.CART_COUNT > 0) {

            mActivityMainBinding.appBarInclude.tvCartCount.setVisibility(View.VISIBLE);
            mActivityMainBinding.appBarInclude.tvCartCount.setText("" + Constants.VARIABLES.CART_COUNT);

            mActivityMainBinding.appBarInclude.tvCartSubTotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.VARIABLES.CART_SUB_AMOUNT);
        } else {
            mActivityMainBinding.appBarInclude.tvCartCount.setVisibility(View.GONE);
            mActivityMainBinding.appBarInclude.tvCartCount.setVisibility(View.GONE);
            mActivityMainBinding.appBarInclude.tvCartSubTotal.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble("0.00")));
        }
        super.onResume();

        if (mSharedPreferenceManager.isLoggedIn()) {
            mActivityMainBinding.tvUsername.setText(mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_name));
            mActivityMainBinding.ivRight.setVisibility(View.GONE);
            if (mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_mobile) != null && !mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_mobile).isEmpty()) {
                mActivityMainBinding.tvNumber.setVisibility(View.VISIBLE);
                mActivityMainBinding.tvNumber.setText(mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_mobile));
            } else {
                mActivityMainBinding.tvNumber.setVisibility(View.GONE);
            }

            mActivityMainBinding.rlLogout.setVisibility(View.VISIBLE);

            mActivityMainBinding.rlLogin.setVisibility(View.GONE);
            try {
                requestViewCart();
                requestUpdateToken();
            } catch (JSONException e) {
                e.printStackTrace();
            }
//            Picasso.with(getApplicationContext()).load(mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_profile_pic)).centerInside().fit().into(mActivityMainBinding.ivProfile);
        } else {
            mActivityMainBinding.rlLogin.setVisibility(View.VISIBLE);
            mActivityMainBinding.rlLogout.setVisibility(View.GONE);
            mActivityMainBinding.ivRight.setVisibility(View.VISIBLE);


         /*   Intent i = new Intent(MainActivityNew.this, LoginActivity.class);
            startActivity(i);
            finish();*/

        }


        try {

            if (mNewCMSBestSellingProductAdapter != null) {
                mNewCMSBestSellingProductAdapter.notifyDataSetChanged();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        if (mNewCMS_dealsOfTheDayAdapter != null) {
            mNewCMS_dealsOfTheDayAdapter.notifyDataSetChanged();
        }
        if (mNewCMSBestSellingProductAdapter != null) {
            mNewCMSBestSellingProductAdapter.notifyDataSetChanged();
        }
        if (mNewCMSPromotionalProductsAdapter != null) {
            mNewCMSPromotionalProductsAdapter.notifyDataSetChanged();
        }
        Constants.VARIABLES.CURRENT_CURRENCY = mSharedPreferenceManager.getCurrentCurrency();
    }

    @Override
    public void sendSlug(String argSlug, int argProductId) {
        Intent i = new Intent(MainActivityNew.this, DetailActivity.class);
        i.putExtra("slug", argSlug.split("#GoGrocery#")[0]);
        i.putExtra("title", argSlug.split("#GoGrocery#")[1]);
        i.putExtra("product_id", argProductId);
        startActivity(i);

        Bundle params = new Bundle();
        params.putString(FirebaseAnalytics.Param.ITEM_NAME, argSlug.split("#GoGrocery#")[0]);
        params.putString("title", argSlug.split("#GoGrocery#")[1]);
        mFirebaseAnalytics.logEvent("view_product", params);
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
            Intent i = new Intent(MainActivityNew.this, LoginActivity.class);
            i.putExtra("from_where", "Fingureprint_login");

            startActivity(i);
        }
    }

    @Override
    public void savelist(String argProductId) {
        if (mSharedPreferenceManager.isLoggedIn()) {
            Intent i = new Intent(MainActivityNew.this, SaveListPage.class);
            i.putExtra("product_id", argProductId);
            startActivity(i);
        } else {
            Intent i = new Intent(MainActivityNew.this, LoginActivity.class);
            i.putExtra("from_where", "home");
            startActivity(i);
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
            mJsonObject.put("query", new JSONObject()
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

    public void requestProductListiing(String argJsonObject) throws JSONException {
        if (Constants.isInternetConnected(MainActivityNew.this)) {
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

            OkHttpClient client = new OkHttpClient.Builder().connectTimeout(60, TimeUnit.SECONDS).readTimeout(60, TimeUnit.SECONDS).writeTimeout(60, TimeUnit.SECONDS).build();


            MediaType mediaType = MediaType.parse("application/json");
            RequestBody body = RequestBody.create(mediaType, argJsonObject);
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
                            if (mainItemListingAdapter.mSpinKitView != null) {
                                mainItemListingAdapter.mSpinKitView.setVisibility(View.GONE);
                            }
                            System.out.println("Rahul : ProductListingPage : requestProductListiing : 1 : ");
                        } else {
                            loading = true;
                        }
                        if (mSearchModelList.size() == 0 && mSearchModel.getHits().getHits().size() == 0) {

                            mActivityMainBinding.appBarInclude.itemSfl.setVisibility(View.GONE);
                            mActivityMainBinding.appBarInclude.itemSfl.stopShimmer();
                            mActivityMainBinding.appBarInclude.sfl.stopShimmer();
                            mActivityMainBinding.appBarInclude.rvItemList.setVisibility(View.GONE);
                            mActivityMainBinding.appBarInclude.noProductAvailable.setVisibility(View.VISIBLE);
                            // mainItemListingAdapter.cvFooter.setVisibility(View.GONE);
                            // mActivityItemListingBinding.cvFooter.setVisibility(View.GONE);
                            System.out.println("Rahul : ProductListingPage : requestProductListiing : 2 : ");
                        } else {

                            if (mSearchModel.getHits().getHits().size() > 0) {

                                mainItemListingAdapter.notifyDataSetChanged();
                                mActivityMainBinding.appBarInclude.itemSfl.setVisibility(View.GONE);
                                mActivityMainBinding.appBarInclude.itemSfl.stopShimmer();
                                mActivityMainBinding.appBarInclude.sfl.stopShimmer();
                                mActivityMainBinding.appBarInclude.rvItemList.setVisibility(View.VISIBLE);
                                if (mainItemListingAdapter.mSpinKitView != null) {
                                    mainItemListingAdapter.mSpinKitView.setVisibility(View.GONE);
                                }
                                mActivityMainBinding.appBarInclude.noProductAvailable.setVisibility(View.GONE);
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
                        mActivityMainBinding.appBarInclude.itemSfl.setVisibility(View.GONE);
                        mActivityMainBinding.appBarInclude.itemSfl.stopShimmer();
                        mActivityMainBinding.appBarInclude.sfl.stopShimmer();
                        mActivityMainBinding.appBarInclude.rvItemList.setVisibility(View.GONE);
                        if (mSearchModelList.size() <= 0) {
                            mActivityMainBinding.appBarInclude.somethingwentwrong.setVisibility(View.VISIBLE);
                        }
                        // mActivityItemListingBinding.cvFooter.setVisibility(View.GONE);
                    } catch (
                            NullPointerException e) {
                        System.out.println("Rahul : ProductListingPage : requestProductListiing : 5 : ");
                        System.out.println("Rahul : ProductListingPage : onPostExecute NullPointerException : ");
                        mActivityMainBinding.appBarInclude.itemSfl.setVisibility(View.GONE);
                        mActivityMainBinding.appBarInclude.itemSfl.stopShimmer();
                        mActivityMainBinding.appBarInclude.sfl.stopShimmer();
                        mActivityMainBinding.appBarInclude.rvItemList.setVisibility(View.GONE);
                        if (mSearchModelList.size() <= 0) {
                            mActivityMainBinding.appBarInclude.somethingwentwrong.setVisibility(View.VISIBLE);
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


        } else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }

    @Override
    public void customFieldValueSelect(int argProductId, int argQuantity, String custom_field_name, String custom_field_value,int position) {

        Intent i = new Intent(MainActivityNew.this, DialogPrepareView.class);
        i.putExtra("custom_field_name", custom_field_name);
        i.putExtra("custom_field_value", custom_field_value);
        i.putExtra("product_id", argProductId + "");
        i.putExtra("position", position + "");
        startActivityForResult(i, 101);
    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == 101) {
            if (resultCode == Activity.RESULT_OK) {

                try {

                    requestAddToCart(Integer.parseInt(data.getStringExtra("argProductId")), 1, data.getStringExtra("custom_field_name"), data.getStringExtra("custom_field_value"),Integer.parseInt(data.getStringExtra("position")));
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        }else  if (requestCode == 1) {
            try {
                if (data != null) {
                    if (data.getStringExtra("getFilterQuery").equals("clear")) {
                        try {
                            if (Constants.VARIABLES.page_title.equals("shop_by_brand")) {
                            //    generateShopByBrandQuery();
                            } else if(Constants.VARIABLES.page_title.equals("search_page")){
                                page = 0;
                                generateSearchQuery(terms_array, terms_base64);
                            }else{
                                page = 0;
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
                          //  mActivityItemListingBinding.ivFilterAppliedTick.setVisibility(View.GONE);
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    } else {
                        System.out.println("Rahul : ProductListingPage : onActivityResult : getFilterQuery selected: " + data.getStringExtra("getFilterQuery"));
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
                        //    mActivityItemListingBinding.ivFilterAppliedTick.setVisibility(View.GONE);
                        } else if (initialparamPassElasticQuery.equals(paramPassElasticQuery)) {
                          //  mActivityItemListingBinding.ivFilterAppliedTick.setVisibility(View.GONE);
                        }  else if(initialparamPassElasticQuerySFQ.equals(paramPassElasticQuery)){
                           // mActivityItemListingBinding.ivFilterAppliedTick.setVisibility(View.GONE);
                        }else  {
                           // mActivityItemListingBinding.ivFilterAppliedTick.setVisibility(View.VISIBLE);
                        }
                    }
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }



}



