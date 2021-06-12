package com.gogrocery.view;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;

import androidx.core.content.res.ResourcesCompat;
import androidx.databinding.DataBindingUtil;

import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Typeface;
import android.os.Build;
import android.os.Handler;
import android.os.Message;

import androidx.annotation.Nullable;
import androidx.core.content.ContextCompat;
import androidx.recyclerview.widget.SimpleItemAnimator;
import androidx.viewpager.widget.ViewPager;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.LinearLayoutManager;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowManager;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.bumptech.glide.Glide;
import com.bumptech.glide.load.engine.DiskCacheStrategy;
import com.facebook.appevents.AppEventsConstants;
import com.facebook.appevents.AppEventsLogger;
import com.gogrocery.Adapters.BestSellingProductAdapter;
import com.gogrocery.Adapters.BestSellingProductNewAdapter;
import com.gogrocery.Adapters.ImageSliderBannnerAdapter;
import com.gogrocery.Adapters.ProductReviewAdapter;
import com.gogrocery.Adapters.ProductVariantAdapter;
import com.gogrocery.Adapters.SimilarProductListingAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Customs.GridSpacingItemDecoration;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.BSP_ItemClick_Interface;
import com.gogrocery.Interfaces.PrepareViewOpenInterface;
import com.gogrocery.Interfaces.ProductListingInterface;
import com.gogrocery.Interfaces.goToZoomImageList;
import com.gogrocery.Models.BestSellingProductModel.BestSellingProductModel;
import com.gogrocery.Models.BestSellingProductModel.Datum;
import com.gogrocery.Models.CartModel.AddToCartModel;
import com.gogrocery.Models.DetailsPage.CustomField;
import com.gogrocery.Models.DetailsPage.DetailsPage;
import com.gogrocery.Models.DetailsPage.VariantProduct;
import com.gogrocery.Models.ProductQuantityLocal;
import com.gogrocery.Models.RatingReviewModel.RatingReviewModel;
import com.gogrocery.Models.RatingReviewModel.ReviewData;
import com.gogrocery.Models.SimilarProductModel.Data;
import com.gogrocery.Models.SimilarProductModel.SimilarProductModel;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityDetailBinding;
import com.google.firebase.analytics.FirebaseAnalytics;
import com.google.gson.Gson;
import com.smarteist.autoimageslider.SliderAnimations;
import com.smarteist.autoimageslider.SliderView;
import com.smarteist.autoimageslider.SliderViewAdapter;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class DetailActivity extends AppCompatActivity implements View.OnClickListener, ProductListingInterface, BSP_ItemClick_Interface, PrepareViewOpenInterface ,goToZoomImageList{


    private ActivityDetailBinding mActivityDetailBinding;
    private SharedPreferenceManager mSharedPreferenceManager;
    private ProductVariantAdapter mProductVariantAdapter;
    AppEventsLogger logger;
    private FirebaseAnalytics mFirebaseAnalytics;
    private List<VariantProduct> mVariantProductList = new ArrayList<>();
    private DatabaseHandler mDatabaseHandler;
    //   private DatabaseHandlerWishlist mDatabaseHandlerWishlist;
    private int productID = 0;
    private SimilarProductListingAdapter mSimilarProductListingAdapter;
    private BestSellingProductNewAdapter mBestSellingProductAdapter;
    private List<Data> mSimilarProductModelList = new ArrayList<>();
    private List<Datum> mBestSellingProduct = new ArrayList<>();
    private boolean isDetailInfoLoaded = false, isSimilarProductLoaded = false, isBestProductLoaded = false, isProductRatingReviewLoaded = false;
    private SliderAdapterDetail mSliderAdapterDetail;
    private String argProductId = "";
    private ProductReviewAdapter mProductReviewAdapter;
    private List<ReviewData> mReviewDataList = new ArrayList<>();
    private Handler mHandler;
    private String paramSlug = "", paramBrandName = "";
    private String customFieldName = "", customFieldValue = "",selectedCustomFieldValue = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityDetailBinding = DataBindingUtil.setContentView(this, R.layout.activity_detail);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        mDatabaseHandler = new DatabaseHandler(getApplicationContext());
        mFirebaseAnalytics = FirebaseAnalytics.getInstance(this);
        logger = AppEventsLogger.newLogger(this);
        //mDatabaseHandlerWishlist = new DatabaseHandlerWishlist(getApplicationContext());
        mActivityDetailBinding.view5.setVisibility(View.GONE);
        mActivityDetailBinding.view6.setVisibility(View.GONE);
        mActivityDetailBinding.ivWishList.setBackground(getApplicationContext().getResources().getDrawable(R.drawable.ic_defult_like));
        mActivityDetailBinding.ivWishList.setVisibility(View.GONE);
        setListners();
        hideStatusBarColor();
        setProductVariantRecyclerView();
        setSimilarProductRecyclerView();
        setBestProductRecyclerView();
        try {
            Bundle mBundle = getIntent().getExtras();
            argProductId = String.valueOf(mBundle.getInt("product_id"));

            mActivityDetailBinding.tvTitle.setText(mBundle.getString("title"));
            if (Constants.isInternetConnected(DetailActivity.this)) {

                requestProductDetails(mBundle.getString("slug"));

                requestSimilarProduct(argProductId);
                requestBestSellingProduct(argProductId);
            } else {
                Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
            }

            if (mDatabaseHandler.checkWishlistAvailable("" + argProductId)) {
                mActivityDetailBinding.ivWishList.setBackground(getApplicationContext().getResources().getDrawable(R.drawable.wishlist_added));
                //mActivityDetailBinding.tvWishlistAdd.setText("SAVED");

            } else {
                mActivityDetailBinding.ivWishList.setBackground(getApplicationContext().getResources().getDrawable(R.drawable.ic_defult_like));
                //mActivityDetailBinding.tvWishlistAdd.setText("WISHLIST");

            }

        } catch (JSONException e) {
            e.printStackTrace();
        }
        /*if (Constants.VARIABLES.CART_COUNT > 0) {
            mActivityDetailBinding.badgeNotification.setVisibility(View.VISIBLE);
            mActivityDetailBinding.badgeNotification.setText("" + Constants.VARIABLES.CART_COUNT);
        } else {
            mActivityDetailBinding.badgeNotification.setVisibility(View.GONE);
        }*/

        mHandler = new Handler() {
            @Override
            public void handleMessage(Message msg) {


                if (isDetailInfoLoaded && isSimilarProductLoaded && isBestProductLoaded) {
                    mActivityDetailBinding.nsvProductDetailPage.setVisibility(View.VISIBLE);
                    mActivityDetailBinding.progressSpinKitView.setVisibility(View.GONE);

                    try {
                        // requestProductRatingReview();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }

            }
        };

        mActivityDetailBinding.ivFav.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent ivCart = new Intent(DetailActivity.this, MyCart.class);
                startActivity(ivCart);
            }
        });

        mActivityDetailBinding.btnGoToCart.setOnClickListener(v->{
            Intent ivCart = new Intent(DetailActivity.this, MyCart.class);
            startActivity(ivCart);
        });

        if (Constants.VARIABLES.CART_COUNT > 0) {
            mActivityDetailBinding.tvCartCount.setVisibility(View.VISIBLE);
            mActivityDetailBinding.tvCartCount.setText("" + Constants.VARIABLES.CART_COUNT);
        } else {
            mActivityDetailBinding.tvCartCount.setVisibility(View.GONE);
        }


    }

    private void setListners() {
        mActivityDetailBinding.txtProductDescription.setOnClickListener(this);
        mActivityDetailBinding.ivBack.setOnClickListener(this);
        mActivityDetailBinding.txtOtherProductInfo.setOnClickListener(this);
        mActivityDetailBinding.btnAddToCart.setOnClickListener(this);
        mActivityDetailBinding.btnGoToCart.setOnClickListener(this);
        mActivityDetailBinding.rlPlus.setOnClickListener(this);
        //mActivityDetailBinding.ivCart.setOnClickListener(this);
        mActivityDetailBinding.rlMinus.setOnClickListener(this);
        mActivityDetailBinding.ivWishList.setOnClickListener(this);
        mActivityDetailBinding.ivWishlistAdd.setOnClickListener(this);
        mActivityDetailBinding.tvRateProduct.setOnClickListener(this);
        mActivityDetailBinding.ivFav.setOnClickListener(this);

    }

 /*   private void requestProductDetails() {
        // Update the list when the data changes
        Bundle mBundle = getIntent().getExtras();


        MainViewModel mainViewModel;
        mainViewModel = ViewModelProviders.of(this).get(MainViewModel.class);

        Constants.API_METHODS.PRODUCT_DETAILS_SLUG=mBundle.getString("slug")+"/";
        System.out.println("Response : DetailActivity : requestProductDetails : url : " + Constants.API_METHODS.PRODUCT_DETAILS_SLUG);
        //ViewModel Request
        mainViewModel.productDetails()

                .observe(this, responseBodyResponse -> {

                    if (responseBodyResponse != null) {
                        Gson gson = new Gson();
                        String responseString = gson.toJson(responseBodyResponse);
                        System.out.println("Response : DetailActivity : requestProductDetails : " + responseString);

                    } else {
                        System.out.println("Response : DetailActivity : requestProductDetails : null : ");
                    }
                });

    }*/

    public void requestProductDetails(String argSlug) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        mActivityDetailBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        System.out.println("Response : DetailActivity : requestProductDetails : url : " + Constants.BASE_URL + Constants.API_METHODS.PRODUCT_DETAILS + argSlug + "/");
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.PRODUCT_DETAILS + argSlug + "/", null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {

                        System.out.println("Response : DetailActivity : requestProductDetails : response : " + response);
                        Gson mGson = new Gson();

                        //  setDetailPageUI(mGson.fromJson(response.toString(), DetailsPage.class));


                        try {
                            List<String> imgList = new ArrayList<>();

                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                isDetailInfoLoaded = true;

                                mHandler.sendEmptyMessage(1);
                            }

                            for (int j = 0; j < response.getJSONObject("data").getJSONArray("product_image").length(); j++) {

                                imgList.add(Constants.IMAGE_PRODUCT_URL + response.getJSONObject("data").getJSONArray("product_image").getJSONObject(j).getString("img"));
                                System.out.println("Sukdev : DetailActivity : setDetailPageUI : imgList : " + imgList.get(j));
                            }


                            mSliderAdapterDetail = new SliderAdapterDetail(getApplicationContext(), imgList,DetailActivity.this);
                            mActivityDetailBinding.imageSlider.setSliderAdapter(mSliderAdapterDetail);

                            //  mActivityMainBinding.appBarInclude.imageSlider.setIndicatorAnimation(0); //set indicator animation by using SliderLayout.IndicatorAnimations. :WORM or THIN_WORM or COLOR or DROP or FILL or NONE or SCALE or SCALE_DOWN or SLIDE and SWAP!!
                            mActivityDetailBinding.imageSlider.setSliderTransformAnimation(SliderAnimations.SIMPLETRANSFORMATION);
                            mActivityDetailBinding.imageSlider.setAutoCycleDirection(SliderView.AUTO_CYCLE_DIRECTION_BACK_AND_FORTH);
                            mActivityDetailBinding.imageSlider.setIndicatorSelectedColor(Color.parseColor("#DFECC5"));
                            mActivityDetailBinding.imageSlider.setIndicatorUnselectedColor(Color.parseColor("#E3E9F2"));
                            mActivityDetailBinding.imageSlider.setScrollTimeInSec(4); //set scroll delay in seconds :
                            // mActivityDetailBinding.imageSlider.startAutoCycle();

                            productID = response.getJSONObject("data").getInt("id");
                            if (response.getJSONObject("data").getJSONObject("brand") != null) {

                                if (response.getJSONObject("data").getJSONObject("category").length() == 0) {
                                    mActivityDetailBinding.tvItemNameCategory.setVisibility(View.GONE);
                                    mActivityDetailBinding.tvMoreBy.setVisibility(View.GONE);
                                    mActivityDetailBinding.tvItemNameCategoryVariant.setVisibility(View.GONE);
                                } else {
                                    mActivityDetailBinding.tvItemNameCategory.setText(response.getJSONObject("data").getJSONObject("category").getString("name"));
                                    mActivityDetailBinding.tvItemNameCategoryVariant.setText(response.getJSONObject("data").getJSONObject("category").getString("name"));


                                    mActivityDetailBinding.tvItemNameCategoryVariant.setOnClickListener(new View.OnClickListener() {
                                        @Override
                                        public void onClick(View v) {

                                            try {
                                                paramBrandName = response.getJSONObject("data").getJSONObject("category").getString("name");
                                                paramSlug = response.getJSONObject("data").getJSONObject("category").getString("slug");
                                            } catch (JSONException e) {
                                                e.printStackTrace();
                                            }


                                            Intent shop_by_brand = new Intent(DetailActivity.this, ProductListingPage.class);
                                            shop_by_brand.putExtra("Category_slug", paramSlug); // extra info is category_slug
                                            shop_by_brand.putExtra("PageTitle", paramBrandName); // extra info is category_slug
                                            startActivity(shop_by_brand);
                                            Constants.VARIABLES.FILTER_TYPE = "category";
                                        }
                                    });
                                }
                            } else {
                                mActivityDetailBinding.tvMoreBy.setVisibility(View.GONE);
                                mActivityDetailBinding.tvItemNameCategoryVariant.setVisibility(View.GONE);
                                mActivityDetailBinding.tvItemNameCategory.setVisibility(View.GONE);
                            }


                            mActivityDetailBinding.tvItemName.setText(response.getJSONObject("data").getString("name"));
                            if(response.getJSONObject("data").getString("name").length()>24) {
                                ViewGroup.LayoutParams paramItemName = (RelativeLayout.LayoutParams) mActivityDetailBinding.tvItemName.getLayoutParams();
                                paramItemName.width = 600;
                                mActivityDetailBinding.tvItemName.setLayoutParams(paramItemName);
                            }else {
                                ViewGroup.LayoutParams paramItemName = (RelativeLayout.LayoutParams) mActivityDetailBinding.tvItemName.getLayoutParams();
                                paramItemName.width = ViewGroup.LayoutParams.WRAP_CONTENT;
                                mActivityDetailBinding.tvItemName.setLayoutParams(paramItemName);
                            }

                            Bundle params = new Bundle();
                            params.putString(FirebaseAnalytics.Param.ITEM_NAME, response.getJSONObject("data").getString("name"));
                            //params.putString("item_name",response.getJSONObject("data").getString("name"));
                            //params.putString("category",response.getJSONObject("data").getJSONObject("category").getString("name"));
                            params.putString("category", response.getJSONObject("data").getJSONObject("category").getString("name"));
                            params.putString("Id", String.valueOf(response.getJSONObject("data").getInt("id")));
                            params.putString("default_price", String.valueOf(response.getJSONObject("data").getString("new_default_price_unit")));
                            params.putString("currency", "AED");
                            params.putString("content_type", "product");
                            mFirebaseAnalytics.logEvent("view_product", params);
                            logger.logEvent("view_product", params);

                            if (response.getJSONObject("data").getString("weight") != null && response.getJSONObject("data").getString("weight") != "null") {

                                if (!response.getJSONObject("data").getString("weight").isEmpty()) {

                                    mActivityDetailBinding.tvWeight.setText(response.getJSONObject("data").getString("weight") + " " + response.getJSONObject("data").getString("uom"));
                                    /*mActivityDetailBinding.tvProductSize.setText(response.getJSONObject("data").getString("weight") + " " + response.getJSONObject("data").getString("uom"));
                                    mActivityDetailBinding.tvProductSize.setVisibility(View.VISIBLE);*/
                                }
                            }/* else {
                                mActivityDetailBinding.tvProductSize.setVisibility(View.GONE);
                            }*/

                            Double channel_price = 0.0, new_default_price_unit = 0.0,discount = 0.0;;
                            if (response.getJSONObject("data").getString("channel_price") != null || !(response.getJSONObject("data").getString("channel_price").isEmpty())) {
                                channel_price = Double.parseDouble(response.getJSONObject("data").getString("channel_price"));
                            }
                            if (response.getJSONObject("data").getString("new_default_price_unit") != null || !(response.getJSONObject("data").getString("new_default_price_unit").isEmpty())) {
                                new_default_price_unit = Double.parseDouble(response.getJSONObject("data").getString("new_default_price_unit"));
                            }

                            if ( response.getJSONObject("data").getString("discount_amount") != null && !( response.getJSONObject("data").getString("discount_amount").isEmpty())) {
                                discount = Double.parseDouble(response.getJSONObject("data").getString("discount_amount"));
                            }
                            System.out.println("Sukdev : DetailActivity : requestProductDetails : channel_price : " + channel_price);
                            System.out.println("Sukdev : DetailActivity : requestProductDetails : new_default_price_unit : " + new_default_price_unit);

                            //if (channel_price > new_default_price_unit) {
                            if (discount > 0.0) {
                                mActivityDetailBinding.tvOriginalPrice.setVisibility(View.VISIBLE);
                                mActivityDetailBinding.tvOriginalPrice.setPaintFlags(mActivityDetailBinding.tvOriginalPrice.getPaintFlags() | Paint.STRIKE_THRU_TEXT_FLAG);
                                mActivityDetailBinding.tvOriginalPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(channel_price));
                                mActivityDetailBinding.tvDiscounrPrice.setTextColor(Color.parseColor("#C32D4A"));
                                Typeface typeface = ResourcesCompat.getFont(getApplicationContext(), R.font.proxima_bold);
                                mActivityDetailBinding.tvDiscounrPrice.setTypeface(typeface);
                                if (!response.getJSONObject("data").getString("disc_type").isEmpty()) {
                                    if (response.getJSONObject("data").getString("disc_type").equals("1")) // % wise
                                    {
                                        mActivityDetailBinding.tvDiscountOffer.setVisibility(View.VISIBLE);
                                        mActivityDetailBinding.tvDiscountOffer.setText( response.getJSONObject("data").getString("discount_amount") +" "+ getResources().getString(R.string._pen_off));

                                    } else { // Currency wise
                                        mActivityDetailBinding.tvDiscountOffer.setVisibility(View.VISIBLE);
                                        mActivityDetailBinding.tvDiscountOffer.setText(Constants.VARIABLES.CURRENT_CURRENCY + " " + response.getJSONObject("data").getString("discount_amount") +" "+getResources().getString(R.string._off));

                                    }
                                }


                            } else {
                                mActivityDetailBinding.tvOriginalPrice.setVisibility(View.GONE);
                                mActivityDetailBinding.tvDiscountOffer.setVisibility(View.GONE);
                                mActivityDetailBinding.tvDiscounrPrice.setTextColor(Color.parseColor("#2E6B0B"));
                                Typeface typeface = ResourcesCompat.getFont(getApplicationContext(), R.font.proxima_regular);
                                mActivityDetailBinding.tvDiscounrPrice.setTypeface(typeface);
                            }
                            mActivityDetailBinding.tvDiscounrPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(response.getJSONObject("data").getString("new_default_price_unit"))));
                            // mActivityDetailBinding.tvDiscountOffer.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + response.getJSONObject("data").getString("discount_amount") + " OFF");

                            System.out.println("Sukdev : DetailActivity : variant_product : " + response.getJSONObject("data").getJSONArray("variant_product").toString());







                            if (response.getJSONObject("data").getJSONArray("custom_field").length() > 0) {
                                for (int j = 0; j < response.getJSONObject("data").getJSONArray("custom_field").length(); j++) {

                                    System.out.println("Sukdev : DetailActivity : custom_field : " + response.getJSONObject("data").getJSONArray("custom_field").getJSONObject(j).toString());
                                    CustomField mCustomFieldProduct = mGson.fromJson(response.getJSONObject("data").getJSONArray("custom_field").getJSONObject(j).toString(), CustomField.class);
                                  customFieldName=mCustomFieldProduct.getFieldName();
                                  customFieldValue=mCustomFieldProduct.getValue();
                                    System.out.println("Sukdev : DetailActivity : customFieldName : " +customFieldName);
                                    System.out.println("Sukdev : DetailActivity : customFieldValue : "  +customFieldValue);
                                }

                            }else {
                                customFieldName="";
                                customFieldValue="";
                            }




                            if (response.getJSONObject("data").getJSONArray("variant_product").length() > 0) {
                                for (int j = 0; j < response.getJSONObject("data").getJSONArray("variant_product").length(); j++) {

                                    System.out.println("Sukdev : DetailActivity : variant_product : " + response.getJSONObject("data").getJSONArray("variant_product").getJSONObject(j).toString());
                                    VariantProduct mVariantProduct = mGson.fromJson(response.getJSONObject("data").getJSONArray("variant_product").getJSONObject(j).toString(), VariantProduct.class);
                                    mVariantProductList.add(mVariantProduct);

                                }
                                System.out.println("Sukdev : DetailActivity : mVariantProductList  : " + mGson.toJson(mVariantProductList));

                                mProductVariantAdapter.notifyDataSetChanged();
                            } else {
                                mActivityDetailBinding.tvAvailablein.setVisibility(View.GONE);
                                mActivityDetailBinding.view5.setVisibility(View.GONE);
                                mActivityDetailBinding.rvAvailableVariant.setVisibility(View.GONE);
                            }

                            if (response.getJSONObject("data").getString("description").equals("null") || response.getJSONObject("data").getString("description") == null) {
                                mActivityDetailBinding.txtProductDescription.setVisibility(View.GONE);
                                mActivityDetailBinding.ivBtnDescription.setVisibility(View.GONE);
                                mActivityDetailBinding.tvProductDescription.setVisibility(View.GONE);
                                mActivityDetailBinding.view7.setVisibility(View.GONE);

                            } else {
                                mActivityDetailBinding.ivBtnDescription.setVisibility(View.VISIBLE);
                                mActivityDetailBinding.tvProductDescription.setText(response.getJSONObject("data").getString("description"));
                                mActivityDetailBinding.ivBtnDescription.setOnClickListener(v->{
                                    try {
                                        if(response.getJSONObject("data").getString("description")!=null&&!response.getJSONObject("data").getString("description").isEmpty()) {
                                            Intent i = new Intent(DetailActivity.this, ProductDetailsView.class);
                                            i.putExtra("product_name", response.getJSONObject("data").getString("name"));
                                            i.putExtra("product_description", response.getJSONObject("data").getString("description"));

                                            startActivity(i);
                                        }
                                    } catch (JSONException e) {
                                        e.printStackTrace();
                                    }
                                });
                            }


                            if (response.getJSONObject("data").getString("sku").equals("null") || response.getJSONObject("data").getString("sku") == null) {
                                mActivityDetailBinding.layoutSku.setVisibility(View.GONE);

                            } else {
                                mActivityDetailBinding.layoutSku.setVisibility(View.GONE);
                                mActivityDetailBinding.tvSkuNumber.setText(response.getJSONObject("data").getString("sku"));

                            }

                            if (response.getJSONObject("data").getString("features").equals("null") || response.getJSONObject("data").getString("features") == null) {
                                mActivityDetailBinding.txtOtherProductInfo.setVisibility(View.GONE);
                                mActivityDetailBinding.tvOtherInfo.setVisibility(View.GONE);
                                mActivityDetailBinding.view9.setVisibility(View.GONE);
                            } else {
                                mActivityDetailBinding.tvOtherInfo.setText(response.getJSONObject("data").getString("features"));
                            }

                            if (mDatabaseHandler.CheckIsDataAlreadyInDBorNot(response.getJSONObject("data").getString("id"))) {
                                mActivityDetailBinding.llAddToCart.setVisibility(View.VISIBLE);
                                mActivityDetailBinding.cvAddToCart.setVisibility(View.VISIBLE);
                                mActivityDetailBinding.btnGoToCart.setVisibility(View.VISIBLE);
                                mActivityDetailBinding.btnAddToCart.setVisibility(View.GONE);
                        /*        mActivityDetailBinding.btnAddToCart.setAlpha(.1f);
                                mActivityDetailBinding.btnAddToCart.setClickable(false);*/
                                //mActivityDetailBinding.llPlusMins.setVisibility(View.VISIBLE);
                                mActivityDetailBinding.etQuantity.setText("" + mDatabaseHandler.checkAndSendProductQtyById(response.getJSONObject("data").getString("id")));
                            } else {
                                mActivityDetailBinding.llAddToCart.setVisibility(View.INVISIBLE);
                                mActivityDetailBinding.cvAddToCart.setVisibility(View.INVISIBLE);
                                mActivityDetailBinding.btnAddToCart.setAlpha(1f);
                                mActivityDetailBinding.btnGoToCart.setVisibility(View.GONE);
                                mActivityDetailBinding.btnAddToCart.setVisibility(View.VISIBLE);
                                mActivityDetailBinding.btnAddToCart.setClickable(true);
                                //mActivityDetailBinding.llPlusMins.setVisibility(View.GONE);
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                            mActivityDetailBinding.progressSpinKitView.setVisibility(View.GONE);

                        }


                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mActivityDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Response : DetailActivity : requestProductDetails : error : " + error);
            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());
                headers.put(Constants.VARIABLES.WAREHOUSE_KEY, mSharedPreferenceManager.getWarehouseId());
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

    public void requestSimilarProduct(String argPoductId) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        System.out.println("Sukdev : DetailActivity : requestSimilarProduct : param : " + Constants.BASE_URL + Constants.API_METHODS.SIMILAR_PRODUCT + argPoductId + "/");
        StringRequest jsonObjReq = new StringRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.SIMILAR_PRODUCT + argPoductId + "/",
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        System.out.println("Sukdev : DetailActivity : requestSimilarProduct : " + response);

                        isSimilarProductLoaded = true;
                        Gson mGson = new Gson();
                        mHandler.sendEmptyMessage(1);
                        try {
                            SimilarProductModel mSimilarProductModel = mGson.fromJson(response, SimilarProductModel.class);

                            for (int i = 0; i < mSimilarProductModel.getData().size(); i++) {
                                if (mSimilarProductModel.getData().get(i).getProduct().getChannelPrice() != null) {
                                    if (mSimilarProductModel.getData().get(i).getProduct().getChannelPrice().equals("0.0")) {

                                    } else if (mSimilarProductModel.getData().get(i).getProduct().getChannelPrice().equals("0")) {

                                    } else {
                                        mSimilarProductModelList.add(mSimilarProductModel.getData().get(i));
                                    }

                                }
                            }
                            // mSimilarProductModelList.addAll(mSimilarProductModel.getData());
                            mSimilarProductListingAdapter.notifyDataSetChanged();

                            if (mSimilarProductModelList.size() == 0) {
                                mActivityDetailBinding.txtSimilarProducts.setVisibility(View.GONE);
                            } else {
                                mActivityDetailBinding.txtSimilarProducts.setVisibility(View.VISIBLE);
                            }

                        } catch (NullPointerException e) {
                            isSimilarProductLoaded = true;
                            mHandler.sendEmptyMessage(1);
                            System.out.println("Sukdev : DetailActivity : requestSimilarProduct : NullPointerException : " + e);
                            mActivityDetailBinding.txtSimilarProducts.setVisibility(View.GONE);
                            mHandler.sendEmptyMessage(1);
                            e.printStackTrace();
                        }


                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                isSimilarProductLoaded = true;
                mHandler.sendEmptyMessage(1);
                System.out.println("Sukdev : DetailActivity : requestSimilarProduct : VolleyError : " + error.toString());

            }
        }) {

            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> mHashMap = new HashMap<>();
                mHashMap.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());
                mHashMap.put("DEVICEID", Constants.getDeviceId(getApplicationContext()));
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
    }


    public void requestBestSellingProduct(String argPoductId) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        System.out.println("Sukdev : DetailActivity : requestSimilarProduct : param : " + Constants.BASE_URL + Constants.API_METHODS.POPULAR_PRODUCT + argPoductId + "/");
        StringRequest jsonObjReq = new StringRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.POPULAR_PRODUCT + argPoductId + "/",
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        System.out.println("Sukdev : DetailActivity : requestBestSellingProduct : " + response);

                        isBestProductLoaded = true;
                        Gson mGson = new Gson();
                        mHandler.sendEmptyMessage(1);
                        try {
                            BestSellingProductModel bestSellingProductModel = mGson.fromJson(response, BestSellingProductModel.class);

                            for (int i = 0; i < bestSellingProductModel.getData().size(); i++) {
                                if (bestSellingProductModel.getData().get(i).getProduct().getChannelPrice() != null) {
                                    if (bestSellingProductModel.getData().get(i).getProduct().getChannelPrice().equals("0.0")) {

                                    } else if (bestSellingProductModel.getData().get(i).getProduct().getChannelPrice().equals("0")) {

                                    } else {
                                        mBestSellingProduct.add(bestSellingProductModel.getData().get(i));
                                    }

                                }
                            }
                            // mSimilarProductModelList.addAll(mSimilarProductModel.getData());
                            mBestSellingProductAdapter.notifyDataSetChanged();

                            if (mBestSellingProduct.size() == 0) {
                                mActivityDetailBinding.txtBestSellingProducts.setVisibility(View.GONE);
                            }

                        } catch (NullPointerException e) {
                            isBestProductLoaded = true;
                            mHandler.sendEmptyMessage(1);
                            System.out.println("Sukdev : DetailActivity : requestBestSellingProduct : NullPointerException : " + e);
                            mActivityDetailBinding.txtBestSellingProducts.setVisibility(View.GONE);
                            mHandler.sendEmptyMessage(1);
                            e.printStackTrace();
                        }


                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                isBestProductLoaded = true;
                mHandler.sendEmptyMessage(1);
                System.out.println("Sukdev : DetailActivity : requestBestSellingProduct : VolleyError : " + error.toString());

            }
        }) {

            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> mHashMap = new HashMap<>();
                mHashMap.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());
                mHashMap.put("DEVICEID", Constants.getDeviceId(getApplicationContext()));
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
    }

    public void requestProductRatingReview() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        mActivityDetailBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        JSONObject mParam = new JSONObject();
        mParam.put("product_id", Integer.parseInt(argProductId));
        System.out.println("Sukdev : DetailActivity : requestProductRatingReview : url : " + Constants.BASE_URL + Constants.API_METHODS.VIEW_RATING_REVIEW);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.VIEW_RATING_REVIEW, mParam,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            mActivityDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                            System.out.println("Sukdev : DetailActivity : requestProductRatingReview : response : " + response);

                            Gson gson = new Gson();
                            JSONObject mRatingReview = response;
                            RatingReviewModel mRatingReviewModel = gson.fromJson(mRatingReview.toString(), RatingReviewModel.class);
                            System.out.println("Sukdev : DetailActivity : requestProductRatingReview : mRatingReviewModel : " + gson.toJson(mRatingReviewModel));

                            if (mRatingReviewModel.getRatingData().size() > 0) {
                                for (int i = 0; i < mRatingReviewModel.getRatingData().size(); i++) {
                                    switch (mRatingReviewModel.getRatingData().get(i).getRating()) {
                                        case 1:
                                            System.out.println("Sukdev : DetailActivity : requestProductRatingReview : case 0 : ");
                                            mActivityDetailBinding.tvOneStarCount.setText(mRatingReviewModel.getRatingData().get(i).getRatingCount().toString());

                                            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
                                                System.out.println("Sukdev : DetailActivity : requestProductRatingReview : case 0.1 : ");
                                                mActivityDetailBinding.pbOneStar.setProgress((int) mRatingReviewModel.getRatingData().get(i).getPercent(), true);
                                            } else {
                                                System.out.println("Sukdev : DetailActivity : requestProductRatingReview : case 0.2 : ");
                                                mActivityDetailBinding.pbOneStar.setProgress((int) mRatingReviewModel.getRatingData().get(i).getPercent());
                                            }
                                            break;
                                        case 2:
                                            System.out.println("Sukdev : DetailActivity : requestProductRatingReview : case 1 : ");
                                            mActivityDetailBinding.tvTwoStarCount.setText(mRatingReviewModel.getRatingData().get(i).getRatingCount().toString());

                                            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
                                                System.out.println("Sukdev : DetailActivity : requestProductRatingReview : case 1.1 : ");

                                                mActivityDetailBinding.pbTwoStar.setProgress((int) mRatingReviewModel.getRatingData().get(i).getPercent(), true);
                                            } else {
                                                System.out.println("Sukdev : DetailActivity : requestProductRatingReview : case 1.2 : ");

                                                mActivityDetailBinding.pbTwoStar.setProgress((int) mRatingReviewModel.getRatingData().get(i).getPercent());
                                            }
                                            break;
                                        case 3:
                                            mActivityDetailBinding.tvThreeStarCount.setText(mRatingReviewModel.getRatingData().get(i).getRatingCount().toString());
                                            System.out.println("Sukdev : DetailActivity : requestProductRatingReview : case 2 : ");

                                            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
                                                mActivityDetailBinding.pbThreeStar.setProgress((int) mRatingReviewModel.getRatingData().get(i).getPercent(), true);
                                                System.out.println("Sukdev : DetailActivity : requestProductRatingReview : case 2.1 : ");

                                            } else {
                                                System.out.println("Sukdev : DetailActivity : requestProductRatingReview : case 2.2 : ");

                                                mActivityDetailBinding.pbThreeStar.setProgress((int) mRatingReviewModel.getRatingData().get(i).getPercent());
                                            }
                                            break;
                                        case 4:
                                            System.out.println("Sukdev : DetailActivity : requestProductRatingReview : case 3 : ");

                                          /*  System.out.println("Sukdev : DetailActivity : requestProductRatingReview : case 3 : getRatingCount : "+mRatingReviewModel.getRatingData().get(i).getRatingCount());
                                            System.out.println("Sukdev : DetailActivity : requestProductRatingReview : case 3 : getPercent : "+(int) mRatingReviewModel.getRatingData().get(i).getPercent());
*/
                                          /*  mActivityDetailBinding.tvFourStarCount.setText(mRatingReviewModel.getRatingData().get(i).getRatingCount().toString());
                                            mActivityDetailBinding.pbFourStar.setProgress((int) mRatingReviewModel.getRatingData().get(i).getPercent());
*/
                                            mActivityDetailBinding.tvFourStarCount.setText(mRatingReviewModel.getRatingData().get(i).getRatingCount().toString());
                                            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
                                                System.out.println("Sukdev : DetailActivity : requestProductRatingReview : case 3.1 : ");
                                                mActivityDetailBinding.pbFourStar.setProgress((int) mRatingReviewModel.getRatingData().get(i).getPercent(), true);
                                            } else {
                                                System.out.println("Sukdev : DetailActivity : requestProductRatingReview : case 3.2 : ");
                                                mActivityDetailBinding.pbFourStar.setProgress((int) mRatingReviewModel.getRatingData().get(i).getPercent());
                                            }
                                            break;
                                        case 5:
                                            System.out.println("Sukdev : DetailActivity : requestProductRatingReview : case 4 : ");

                                            mActivityDetailBinding.tvFiveStarCount.setText(mRatingReviewModel.getRatingData().get(i).getRatingCount().toString());

                                            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
                                                System.out.println("Sukdev : DetailActivity : requestProductRatingReview : case 4.1 : ");

                                                mActivityDetailBinding.pbFiveStar.setProgress((int) mRatingReviewModel.getRatingData().get(i).getPercent(), true);
                                            } else {
                                                System.out.println("Sukdev : DetailActivity : requestProductRatingReview : case 4.2 : ");

                                                mActivityDetailBinding.pbFiveStar.setProgress((int) mRatingReviewModel.getRatingData().get(i).getPercent());
                                            }
                                            break;
                                    }
                                }

                                mActivityDetailBinding.tvRatingAverage.setText("" + Constants.twoDecimalRoundOff(mRatingReviewModel.getReviewAvg()));
                                mActivityDetailBinding.rbAverageRating.setRating((float) mRatingReviewModel.getReviewAvg());


                                if (mRatingReviewModel.getReviewData().size() > 0) {
                                    System.out.println("Sukdev : DetailActivity : requestProductRatingReview : Visible : ");

                                    mActivityDetailBinding.tvTotalReview.setText("All " + mRatingReviewModel.getReviewData().size() + " Reviews");

                                    mReviewDataList.clear();
                                    mReviewDataList.addAll(mRatingReviewModel.getReviewData());

                                    mProductReviewAdapter = new ProductReviewAdapter(getApplicationContext(), mReviewDataList);
                                    LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.VERTICAL, false);
                                    mActivityDetailBinding.rvReview.setLayoutManager(mLayoutManager);
                                    mActivityDetailBinding.rvReview.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
                                    mActivityDetailBinding.rvReview.setItemAnimator(new DefaultItemAnimator());
                                    mActivityDetailBinding.rvReview.setAdapter(mProductReviewAdapter);
                                    mActivityDetailBinding.rvReview.setNestedScrollingEnabled(false);
                                    //mActivityDetailBinding.rlAllReviews.setVisibility(View.VISIBLE);

                                } else {
                                    System.out.println("Sukdev : DetailActivity : requestProductRatingReview : gone : ");
                                    mActivityDetailBinding.rlAllReviews.setVisibility(View.GONE);
                                }
                            }
                            mActivityDetailBinding.rlReviewsAndRating.setVisibility(View.GONE);

                        } catch (Exception e) {
                            mActivityDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                            System.out.println("Response : DetailActivity : requestProductRatingReview : Exception : " + e);
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mActivityDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Response : DetailActivity : requestProductRatingReview : error : " + error);
            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());
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

    private void setRatingReviewUI() {

    }

   /* public void requestAddToCart(int argProductId, int argQty) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));
        mJsonObject.put("product_id", argProductId);
        mJsonObject.put("quantity", argQty);
        mJsonObject.put("warehouse_id", mSharedPreferenceManager.getWarehouseId());
        mJsonObject.put("year_check", mSharedPreferenceManager.getYearCheck());

        System.out.println("Sukdev : ProductListingPage : requestAddToCart : param : " + mJsonObject);
        System.out.println("Sukdev : ProductListingPage : requestAddToCart : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));


        mActivityDetailBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(com.android.volley.Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.ADD_TO_CART, mJsonObject,
                new com.android.volley.Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {

                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        System.out.println("Sukdev : ProductListingPage : requestAddToCart : mJsonObject : " + mJsonObject);

                        AddToCartModel mAddToCartModel = mGson.fromJson(mJsonObject.toString(), AddToCartModel.class);
                        if (mAddToCartModel.getStatus() == 1) {

                            if (argQty == 0) {
                                mDatabaseHandler.deleteSingleRecord(String.valueOf(argProductId));
                            } else {

                                Bundle params = new Bundle();
                                params.putString("productName",mAddToCartModel.getCartData().getCartdetails().get(0).getName());
                                params.putString("productId",mAddToCartModel.getCartData().getCartdetails().get(0).getId());
                                params.putString("addedQuanity",mAddToCartModel.getCartData().getCart_count());
                                //params.putString("productName",mAddToCartModel.getCartData().getCartdetails().get(0).getName());
                                params.putString("content_type","product");
                                params.putString("currency", Constants.VARIABLES.CURRENT_CURRENCY);
                                mFirebaseAnalytics.logEvent(FirebaseAnalytics.Event.ADD_TO_CART, params);
                                logger.logEvent(AppEventsConstants.EVENT_NAME_ADDED_TO_CART, params);
                           *//* int cartItemCount = 0;
                            for (int i = 0; i < mAddToCartModel.getCartData().getCartdetails().size(); i++) {
                                cartItemCount = cartItemCount + Integer.parseInt(mAddToCartModel.getCartData().getCartdetails().get(i).getQty());

                            }*//*
                                //mActivityMainBinding.appBarInclude.badgeNotification.setText("" + cartItemCount);

                                ProductQuantityLocal mProductQuantityLocal = new ProductQuantityLocal(String.valueOf(argProductId), String.valueOf(argQty));
                                if (!mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(argProductId)).equals("0")) {
                                    mDatabaseHandler.updateProductQuantityById(mProductQuantityLocal);
                                } else {
                                    mDatabaseHandler.addProductQty(mProductQuantityLocal);
                                }


                                System.out.println("Sukdev : ProductListingPage : checkDbCount : " + mDatabaseHandler.getAllProductQtyData().size());
                            }
                            Constants.VARIABLES.CART_COUNT = Integer.parseInt(mAddToCartModel.getCartData().getCart_count());
                            mActivityDetailBinding.tvCartCount.setVisibility(View.VISIBLE);
                            mActivityDetailBinding.tvCartCount.setText(mAddToCartModel.getCartData().getCart_count());
                            //mActivityDetailBinding.badgeNotification.setText(mAddToCartModel.getCartData().getCart_count());


                            //AnimateBell();
                        } else {
                            try {
                                if(response.getString("is_age_verification").equals("False")) {
                                    Intent i = new Intent(DetailActivity.this, TobacoCatActivity.class);
                                    i.putExtra("message", mAddToCartModel.getMsg());
                                    startActivity(i);
                                }else{
                                    Constants.showToastInMiddle(getApplicationContext(), mAddToCartModel.getMsg());
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }

                        }
                        mSimilarProductListingAdapter.notifyDataSetChanged();
                        mBestSellingProductAdapter.notifyDataSetChanged();
                        mActivityDetailBinding.progressSpinKitView.setVisibility(View.GONE);

                    }
                }, new com.android.volley.Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Sukdev : ProductListingPage : requestAddToCart : VolleyError : " + error.toString());
                mActivityDetailBinding.progressSpinKitView.setVisibility(View.GONE);
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

                System.out.println("Sukdev requestCmsContent : response : " + staticRes);
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
                headers.put(Constants.VARIABLES.WAREHOUSE_KEY, mSharedPreferenceManager.getWarehouseId());
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

    private void setProductVariantRecyclerView() {
        mProductVariantAdapter = new ProductVariantAdapter(getApplicationContext(), mVariantProductList);
        //  LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.HORIZONTAL, false);
        GridLayoutManager mGridLayoutManager = new GridLayoutManager(getApplicationContext(), 2);
        mActivityDetailBinding.rvAvailableVariant.setLayoutManager(mGridLayoutManager);
        mActivityDetailBinding.rvAvailableVariant.addItemDecoration(new GridSpacingItemDecoration(2, GridSpacingItemDecoration.dpToPx(getApplicationContext(), 1), true));
        mActivityDetailBinding.rvAvailableVariant.setItemAnimator(new DefaultItemAnimator());
        mActivityDetailBinding.rvAvailableVariant.setAdapter(mProductVariantAdapter);
        mActivityDetailBinding.rvAvailableVariant.setNestedScrollingEnabled(false);
    }

    private void setSimilarProductRecyclerView() {
        mSimilarProductListingAdapter = new SimilarProductListingAdapter(getApplicationContext(), mSimilarProductModelList, this, this, mDatabaseHandler,this);
        // LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.HORIZONTAL, false);
        GridLayoutManager mGridLayoutManager = new GridLayoutManager(getApplicationContext(), 2);
        mActivityDetailBinding.rvSimilarProduct.setLayoutManager(mGridLayoutManager);
        ((SimpleItemAnimator) mActivityDetailBinding.rvSimilarProduct.getItemAnimator()).setSupportsChangeAnimations(false);
  /*      mActivityDetailBinding.rvSimilarProduct.addItemDecoration(new GridSpacingItemDecoration(2, GridSpacingItemDecoration.dpToPx(getApplicationContext(), 1), true));
        mActivityDetailBinding.rvSimilarProduct.setItemAnimator(new DefaultItemAnimator());*/
        mActivityDetailBinding.rvSimilarProduct.setAdapter(mSimilarProductListingAdapter);
        mActivityDetailBinding.rvSimilarProduct.setNestedScrollingEnabled(false);
    }


    private void setBestProductRecyclerView() {
        mBestSellingProductAdapter = new BestSellingProductNewAdapter(getApplicationContext(), mBestSellingProduct, this, this, mDatabaseHandler);
        //  LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.HORIZONTAL, false);
        GridLayoutManager mGridLayoutManager = new GridLayoutManager(getApplicationContext(), 2);
        mActivityDetailBinding.rvBestSellingProduct.setLayoutManager(mGridLayoutManager);
        ((SimpleItemAnimator) mActivityDetailBinding.rvBestSellingProduct.getItemAnimator()).setSupportsChangeAnimations(false);
/*        mActivityDetailBinding.rvBestSellingProduct.addItemDecoration(new GridSpacingItemDecoration(2, GridSpacingItemDecoration.dpToPx(getApplicationContext(), 1), true));
        mActivityDetailBinding.rvBestSellingProduct.setItemAnimator(new DefaultItemAnimator());*/
        mActivityDetailBinding.rvBestSellingProduct.setAdapter(mBestSellingProductAdapter);
        mActivityDetailBinding.rvBestSellingProduct.setNestedScrollingEnabled(false);
    }

    public void requestAddToWishlist(int argProductId, String argAction) throws JSONException {
        if (Constants.isInternetConnected(DetailActivity.this)) {
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            JSONObject mJsonObject = new JSONObject();
            mJsonObject.put("website_id", 1);
            mJsonObject.put("product_id", argProductId);

            System.out.println("Sukdev : MainActivityNew : requestAddToWishlist : param : " + mJsonObject);

            String CURRENT_URL = "";
            if (argAction.equals("add")) {
                CURRENT_URL = Constants.BASE_URL + Constants.API_METHODS.MY_WISH_LIST;
            } else {
                CURRENT_URL = Constants.BASE_URL + Constants.API_METHODS.DELETE_WISHLIST;
            }

            mActivityDetailBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            JsonObjectRequest jsonObjReq = new JsonObjectRequest(com.android.volley.Request.Method.POST,
                    CURRENT_URL, mJsonObject,
                    new com.android.volley.Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            mActivityDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            System.out.println("Sukdev : MainActivityNew : requestAddToWishlist : mJsonObject : " + mJsonObject);


                            try {
                                if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                    Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();
                                    if (argAction.equals("add")) {

                                        Bundle params = new Bundle();
                                        params.putString("productName", response.getJSONObject("data").getJSONObject("product").getString("name"));
                                        params.putString("productId", argProductId + "");
                                        params.putString("content_type", "product");
                                        mFirebaseAnalytics.logEvent(FirebaseAnalytics.Event.ADD_TO_WISHLIST, params);
                                        logger.logEvent(AppEventsConstants.EVENT_NAME_ADDED_TO_WISHLIST, params);

                                        if (!mDatabaseHandler.checkWishlistAvailable("" + argProductId)) {
                                            mDatabaseHandler.addWishlistData("" + argProductId);
                                            mActivityDetailBinding.ivWishList.setBackground(getApplicationContext().getResources().getDrawable(R.drawable.ic_like));
                                            //mActivityDetailBinding.tvWishlistAdd.setText("SAVED");
                                        }

                                    } else {
                                        if (mDatabaseHandler.checkWishlistAvailable("" + argProductId)) {
                                            mDatabaseHandler.deleteWishlistSingleRecord("" + argProductId);
                                            mActivityDetailBinding.ivWishList.setBackground(getApplicationContext().getResources().getDrawable(R.drawable.ic_defult_like));
                                            //mActivityDetailBinding.tvWishlistAdd.setText("WISHLIST");
                                        }
                                    }
                              /*  if (argAction.equals("add")) {
                                   // mDatabaseHandlerWishlist.addWishlistData(String.valueOf(argProductId));
                                    Constants.VARIABLES.mWishlistModelAddedList.add(String.valueOf(argProductId));
                                    mActivityDetailBinding.ivWishList.setBackground(getApplicationContext().getResources().getDrawable(R.drawable.wishlist));
                                    mSharedPreferenceManager.storeWishlistData(Constants.VARIABLES.mWishlistModelAddedList.toString());
                                } else {
                                 //   mDatabaseHandlerWishlist.deleteSingleRecordWishlist(String.valueOf(argProductId));
                                    Constants.VARIABLES.mWishlistModelAddedList.remove("" + argProductId);
                                    mActivityDetailBinding.ivWishList.setBackground(getApplicationContext().getResources().getDrawable(R.drawable.wishlist_added));
                                    mSharedPreferenceManager.storeWishlistData(Constants.VARIABLES.mWishlistModelAddedList.toString());
                                }*/

                                } else {
                                    Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();

                                }
                            } catch (JSONException e) {
                                e.printStackTrace();

                            }

                        }
                    }, new com.android.volley.Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {

                    System.out.println("Sukdev : MainActivityNew : requestAddToWishlist : VolleyError : " + error.toString());
                    mActivityDetailBinding.progressSpinKitView.setVisibility(View.GONE);

                }
            }) {
                @Override
                public Map<String, String> getHeaders() throws AuthFailureError {
                    HashMap<String, String> headers = new HashMap<String, String>();
                    headers.put("Content-Type", "application/json");
                    headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());
                    headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                    System.out.println("Sukdev : MainActivityNew : requestAddToWishlist : VolleyError : " + headers.toString());

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
        } else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }

    private void setDetailPageUI(DetailsPage argDetailsPage) {

        List<String> imgList = new ArrayList<>();

        for (int j = 0; j < argDetailsPage.getData().getProductImage().size(); j++) {

            imgList.add(argDetailsPage.getData().getProductImage().get(j).getImg());
            System.out.println("Sukdev : DetailActivity : setDetailPageUI : imgList : " + imgList.get(j));
        }

        setSlider(imgList);

        mActivityDetailBinding.tvItemNameCategory.setText(argDetailsPage.getData().getBrand().getName());
        mActivityDetailBinding.tvItemName.setText(argDetailsPage.getData().getName());
        mActivityDetailBinding.tvItemNameCategoryVariant.setText(argDetailsPage.getData().getBrand().getName());
    }

    public void setSlider(List<String> argList) {

        List<String> murlList = argList;


        final int dotscount;
        final ImageView[] dots;

        final ImageSliderBannnerAdapter mImageSliderBannnerAdapter = new ImageSliderBannnerAdapter(getApplicationContext(), murlList);

        mActivityDetailBinding.viewPager.setAdapter(mImageSliderBannnerAdapter);

        dotscount = mImageSliderBannnerAdapter.getCount();
        dots = new ImageView[dotscount];


        for (int i = 0; i < dotscount; i++) {

            dots[i] = new ImageView(getApplicationContext());
            dots[i].setImageDrawable(ContextCompat.getDrawable(getApplicationContext(), R.drawable.detail_page_non_active_dots));

            LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT);

            params.setMargins(8, 0, 8, 0);

            if (dotscount > 1) {

                mActivityDetailBinding.SliderDots.addView(dots[i], params);
            }


        }


        if (dotscount > 0) {
            dots[0].setImageDrawable(ContextCompat.getDrawable(getApplicationContext(), R.drawable.detail_page_active_dots));
        }

        mActivityDetailBinding.viewPager.addOnPageChangeListener(new ViewPager.OnPageChangeListener() {
            @Override
            public void onPageScrolled(int position, float positionOffset, int positionOffsetPixels) {

            }

            @Override
            public void onPageSelected(int position) {

                for (int i = 0; i < dotscount; i++) {
                    dots[i].setImageDrawable(ContextCompat.getDrawable(getApplicationContext(), R.drawable.detail_page_non_active_dots));
                }

                dots[position].setImageDrawable(ContextCompat.getDrawable(getApplicationContext(), R.drawable.detail_page_active_dots));

            }

            @Override
            public void onPageScrollStateChanged(int state) {

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

    @Override
    public void onClick(View v) {
        final Handler handler = new Handler();
        //mActivityDetailBinding.llProductDescription.startAnimation(new ScaleAnimToHide(1.0f, 1.0f, 1.0f, 0.0f, 500, mActivityDetailBinding.llProductDescription, true));

        switch (v.getId()) {
            case R.id.txtProductDescription:
                if (mActivityDetailBinding.llProductDescription.getVisibility() == View.GONE) {
                    // mActivityDetailBinding.llProductDescription.startAnimation(new ScaleAnimToShow(1.0f, 1.0f, 1.0f, 0.0f, 500, mActivityDetailBinding.llProductDescription, true));
                    mActivityDetailBinding.txtProductDescription.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.drawable.minus, 0);
                    mActivityDetailBinding.llProductDescription.setVisibility(View.VISIBLE);


                } else {
                    //mActivityDetailBinding.llProductDescription.startAnimation(new ScaleAnimToHide(1.0f, 1.0f, 1.0f, 0.0f, 500, mActivityDetailBinding.llProductDescription, true));
                    mActivityDetailBinding.txtProductDescription.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.drawable.plus, 0);
                    mActivityDetailBinding.llProductDescription.setVisibility(View.GONE);
                   /* handler.postDelayed(new Runnable() {
                        @Override
                        public void run() {
                            // Do something after 5s = 5000ms
                            mActivityDetailBinding.llProductDescription.setVisibility(View.GONE);
                        }
                    }, 501);*/
                }
                break;
            case R.id.txtOtherProductInfo:
                if (mActivityDetailBinding.tvOtherInfo.getVisibility() == View.GONE) {
                    // mActivityDetailBinding.llProductDescription.startAnimation(new ScaleAnimToShow(1.0f, 1.0f, 1.0f, 0.0f, 500, mActivityDetailBinding.llProductDescription, true));
                    mActivityDetailBinding.txtOtherProductInfo.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.drawable.minus, 0);
                    mActivityDetailBinding.tvOtherInfo.setVisibility(View.VISIBLE);


                } else {
                    //mActivityDetailBinding.llProductDescription.startAnimation(new ScaleAnimToHide(1.0f, 1.0f, 1.0f, 0.0f, 500, mActivityDetailBinding.llProductDescription, true));
                    mActivityDetailBinding.txtOtherProductInfo.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.drawable.plus, 0);
                    mActivityDetailBinding.tvOtherInfo.setVisibility(View.GONE);
                   /* handler.postDelayed(new Runnable() {
                        @Override
                        public void run() {
                            // Do something after 5s = 5000ms
                            mActivityDetailBinding.llProductDescription.setVisibility(View.GONE);
                        }
                    }, 501);*/
                }
                break;
            case R.id.btnAddToCart:
                if(customFieldName!=null&&!customFieldName.isEmpty()&&customFieldValue!=null&&!customFieldValue.isEmpty()){
                    Intent i = new Intent(DetailActivity.this, DialogPrepareView.class);
                    i.putExtra("custom_field_name", customFieldName);
                    i.putExtra("custom_field_value", customFieldValue);
                    i.putExtra("product_id", argProductId + "");
                    i.putExtra("arg_which", "llAddToCart");
                    startActivityForResult(i, 101);
                }else {
                    try {
                        requestAddToCart(productID, 1, "llAddToCart","","",0);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }


                break;
            case R.id.rlPlus:
                int qty = Integer.parseInt(mActivityDetailBinding.etQuantity.getText().toString());
                qty = qty + 1;
                try {
                    requestAddToCart(productID, qty, "rlPlus", "", "",0);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                break;
            case R.id.rlMinus:
                int qtyMinus = Integer.parseInt(mActivityDetailBinding.etQuantity.getText().toString());
                if (qtyMinus == 1) {
                    try {
                        requestAddToCart(productID, 0, "rlMinus", "", "",0);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                } else {
                    qtyMinus = qtyMinus - 1;
                    try {
                        requestAddToCart(productID, qtyMinus, "rlMinus", "", "",0);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                }
                break;
            case R.id.ivCart:
                Intent ivCart = new Intent(DetailActivity.this, MyCart.class);
                startActivity(ivCart);
                break;
            case R.id.ivWishlistAdd:


                if (mSharedPreferenceManager.isLoggedIn()) {
                    Intent i = new Intent(DetailActivity.this, SaveListPage.class);
                    i.putExtra("product_id", argProductId);
                    startActivity(i);
                } else {
                    Intent i = new Intent(DetailActivity.this, LoginActivity.class);
                    i.putExtra("from_where", "DetailPage");
                    startActivity(i);
                }

        /*        if (mSharedPreferenceManager.isLoggedIn()) {
                    try {
                        if (mDatabaseHandler.checkWishlistAvailable("" + argProductId)) {
                            requestAddToWishlist(Integer.parseInt(argProductId), "remove");
                        } else {
                            requestAddToWishlist(Integer.parseInt(argProductId), "add");
                        }

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }*/
                  /*  try {
                        if (Constants.VARIABLES.mWishlistModelAddedList.contains(argProductId)) {
                            requestAddToWishlist(Integer.parseInt(argProductId), "add");
                        } else {
                            requestAddToWishlist(Integer.parseInt(argProductId), "remove");
                        }

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }*/
      /*          } else {
                    Intent ivWishListLogin = new Intent(DetailActivity.this, LoginActivity.class);
                    ivWishListLogin.putExtra("from_where", "DetailPage");
                    startActivity(ivWishListLogin);
                }*/
                break;
            case R.id.ivBack:
                finish();
                break;
            case R.id.ivWishList:
                if (mSharedPreferenceManager.isLoggedIn()) {
                    try {
                        if (mDatabaseHandler.checkWishlistAvailable("" + argProductId)) {
                            requestAddToWishlist(Integer.parseInt(argProductId), "remove");
                        } else {
                            requestAddToWishlist(Integer.parseInt(argProductId), "add");
                        }
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                  /*  try {
                        if (Constants.VARIABLES.mWishlistModelAddedList.contains(argProductId)) {
                            requestAddToWishlist(Integer.parseInt(argProductId), "add");
                        } else {
                            requestAddToWishlist(Integer.parseInt(argProductId), "remove");
                        }

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }*/
                } else {
                    Intent ivWishListLogin = new Intent(DetailActivity.this, LoginActivity.class);
                    ivWishListLogin.putExtra("from_where", "DetailPage");
                    startActivity(ivWishListLogin);
                }
                break;
            case R.id.tvRateProduct:
                if (mSharedPreferenceManager.isLoggedIn()) {
                    Intent tvRateProduct = new Intent(DetailActivity.this, ReviewProductPage.class);
                    tvRateProduct.putExtra("product_id", "" + productID);
                    startActivityForResult(tvRateProduct, 1);
                } else {
                    Intent tvRateProduct = new Intent(DetailActivity.this, LoginActivity.class);
                    tvRateProduct.putExtra("from_where", "DetailPage");
                    startActivity(tvRateProduct);
                }
                break;

        }
    }


    @Override
    protected void onResume() {
        super.onResume();

        if (mSimilarProductListingAdapter != null) {
            mSimilarProductListingAdapter.notifyDataSetChanged();
        }


        if (mDatabaseHandler.checkWishlistAvailable("" + argProductId)) {
            mActivityDetailBinding.ivWishList.setBackground(getApplicationContext().getResources().getDrawable(R.drawable.wishlist_added));
            //mActivityDetailBinding.tvWishlistAdd.setText("SAVED");

        } else {
            mActivityDetailBinding.ivWishList.setBackground(getApplicationContext().getResources().getDrawable(R.drawable.ic_defult_like));
            //mActivityDetailBinding.tvWishlistAdd.setText("WISHLIST");

        }
        if (mDatabaseHandler.CheckIsDataAlreadyInDBorNot("" + argProductId)) {
            mActivityDetailBinding.llAddToCart.setVisibility(View.VISIBLE);
            mActivityDetailBinding.cvAddToCart.setVisibility(View.VISIBLE);
            mActivityDetailBinding.btnGoToCart.setVisibility(View.VISIBLE);
            mActivityDetailBinding.btnAddToCart.setVisibility(View.GONE);
                        /*        mActivityDetailBinding.btnAddToCart.setAlpha(.1f);
                                mActivityDetailBinding.btnAddToCart.setClickable(false);*/
            //mActivityDetailBinding.llPlusMins.setVisibility(View.VISIBLE);
            mActivityDetailBinding.etQuantity.setText("" + mDatabaseHandler.checkAndSendProductQtyById("" + argProductId));
        } else {
            mActivityDetailBinding.llAddToCart.setVisibility(View.INVISIBLE);
            mActivityDetailBinding.cvAddToCart.setVisibility(View.INVISIBLE);
            mActivityDetailBinding.btnAddToCart.setAlpha(1f);
            mActivityDetailBinding.btnGoToCart.setVisibility(View.GONE);
            mActivityDetailBinding.btnAddToCart.setVisibility(View.VISIBLE);
            mActivityDetailBinding.btnAddToCart.setClickable(true);
            //mActivityDetailBinding.llPlusMins.setVisibility(View.GONE);
        }

        if (Constants.VARIABLES.CART_COUNT > 0) {
            mActivityDetailBinding.tvCartCount.setVisibility(View.VISIBLE);
            mActivityDetailBinding.tvCartCount.setText("" + Constants.VARIABLES.CART_COUNT);
        } else {
            mActivityDetailBinding.tvCartCount.setVisibility(View.GONE);
            mActivityDetailBinding.llAddToCart.setVisibility(View.INVISIBLE);
            mActivityDetailBinding.cvAddToCart.setVisibility(View.INVISIBLE);
//            mActivityDetailBinding.btnAddToCart.setVisibility(View.VISIBLE);
//            mActivityDetailBinding.btnAddToCart.setAlpha(1f);
//            mActivityDetailBinding.btnAddToCart.setClickable(true);
        }

    }
    public void requestAddToCart(int argProductId, int argQty, String argWhich, String mCustomFieldName, String mCustomFieldValue,int position) throws JSONException {
        if (Constants.isInternetConnected(DetailActivity.this)) {

            mActivityDetailBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            JSONObject mJsonObject = new JSONObject();
            mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));
            mJsonObject.put("product_id", argProductId);
            mJsonObject.put("quantity", argQty);
            mJsonObject.put("year_check", mSharedPreferenceManager.getYearCheck());
            mJsonObject.put("custom_field_name", mCustomFieldName);
            mJsonObject.put("custom_field_value", mCustomFieldValue);
            System.out.println("Sukdev : MyCart : requestAddToCart : param : " + mJsonObject);
            System.out.println("Sukdev : MyCart : requestAddToCart : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));

            JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                    Constants.BASE_URL + Constants.API_METHODS.ADD_TO_CART, mJsonObject,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {

                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            System.out.println("Sukdev : MyCart : requestAddToCart : mJsonObject : " + mJsonObject);
                            mActivityDetailBinding.progressSpinKitView.setVisibility(View.GONE);
                            try {
                                if(mJsonObject.getInt("status")==1) {
                                    AddToCartModel mAddToCartModel = mGson.fromJson(mJsonObject.toString(), AddToCartModel.class);
                                    if (mAddToCartModel.getStatus() != 0) {

                                        if (argQty == 0) {
                                            mDatabaseHandler.deleteSingleRecord(String.valueOf(argProductId));


                                            switch (argWhich) {
                                                case "llAddToCart":
                                                    //mActivityDetailBinding.llPlusMins.setVisibility(View.GONE);
                                                    mActivityDetailBinding.llAddToCart.setVisibility(View.INVISIBLE);
                                                    mActivityDetailBinding.cvAddToCart.setVisibility(View.INVISIBLE);
                                                    mActivityDetailBinding.btnAddToCart.setAlpha(1f);
                                                    mActivityDetailBinding.btnAddToCart.setVisibility(View.VISIBLE);
                                                    mActivityDetailBinding.btnGoToCart.setVisibility(View.GONE);
                                                    mActivityDetailBinding.btnAddToCart.setClickable(true);
                                                    break;
                                                case "rlMinus":
                                                    mActivityDetailBinding.llAddToCart.setVisibility(View.INVISIBLE);
                                                    mActivityDetailBinding.cvAddToCart.setVisibility(View.INVISIBLE);
                                                    mActivityDetailBinding.btnAddToCart.setAlpha(1f);
                                                    mActivityDetailBinding.btnGoToCart.setVisibility(View.GONE);
                                                    mActivityDetailBinding.btnAddToCart.setVisibility(View.VISIBLE);
                                                    mActivityDetailBinding.btnAddToCart.setClickable(true);
                                                case "related":
                                                   // mSimilarProductListingAdapter.notifyDataSetChanged();
                                                    mSimilarProductListingAdapter.notifyItemChanged(position);
                                                    break;


                                            }
                                        } else {

                                            switch (argWhich) {
                                                case "llAddToCart":
                                                    mActivityDetailBinding.etQuantity.setText("1");
                                                    //mActivityDetailBinding.llPlusMins.setVisibility(View.VISIBLE);
                                                    mActivityDetailBinding.llAddToCart.setVisibility(View.VISIBLE);
                                                    mActivityDetailBinding.cvAddToCart.setVisibility(View.VISIBLE);
                                              /*  mActivityDetailBinding.btnAddToCart.setAlpha(.1f);
                                                mActivityDetailBinding.btnAddToCart.setClickable(false);*/
                                                    mActivityDetailBinding.btnGoToCart.setVisibility(View.VISIBLE);
                                                    mActivityDetailBinding.btnAddToCart.setVisibility(View.GONE);
                                                    break;
                                                case "rlPlus":
                                                    mActivityDetailBinding.etQuantity.setText("" + argQty);
                                                    break;
                                                case "rlMinus":
                                                    mActivityDetailBinding.etQuantity.setText("" + argQty);
                                                    break;
                                                case "related":
                                                  //  mSimilarProductListingAdapter.notifyDataSetChanged();
                                                    mSimilarProductListingAdapter.notifyItemChanged(position);
                                                    break;
                                            }

                                            ProductQuantityLocal mProductQuantityLocal = new ProductQuantityLocal(String.valueOf(argProductId), String.valueOf(argQty));
                                            if (!mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(argProductId)).equals("0")) {
                                                mDatabaseHandler.updateProductQuantityById(mProductQuantityLocal);
                                            } else {
                                                mDatabaseHandler.addProductQty(mProductQuantityLocal);
                                            }


                                        }


                                        System.out.println("Sukdev : MyCart : checkDbCount : " + mDatabaseHandler.getAllProductQtyData().size());
                                        Constants.VARIABLES.CART_COUNT = Integer.parseInt(mAddToCartModel.getCartData().getCart_count());
                                        Constants.VARIABLES.CART_SUB_AMOUNT = Constants.twoDecimalRoundOff(mAddToCartModel.getCartData().getOrderamountdetails().get(0).getSubTotal());
                                        if (Constants.VARIABLES.CART_COUNT > 0) {
                                            mActivityDetailBinding.tvCartCount.setVisibility(View.VISIBLE);
                                            mActivityDetailBinding.tvCartCount.setText(mAddToCartModel.getCartData().getCart_count());
                                        } else {
                                            mActivityDetailBinding.tvCartCount.setVisibility(View.GONE);
                                        }

                                        //mActivityDetailBinding.badgeNotification.setText("" + mAddToCartModel.getCartData().getCart_count());
                                        //AnimateBell();
                                    }
                                }else {

                            /*        if (argQty == 0) {
                                        mDatabaseHandler.deleteSingleRecord(String.valueOf(argProductId));
                                        switch (argWhich) {

                                            case "llAddToCart":
                                                //mActivityDetailBinding.llPlusMins.setVisibility(View.GONE);
                                                mActivityDetailBinding.llAddToCart.setVisibility(View.INVISIBLE);
                                                mActivityDetailBinding.cvAddToCart.setVisibility(View.INVISIBLE);
                                                mActivityDetailBinding.btnAddToCart.setAlpha(1f);
                                                mActivityDetailBinding.btnGoToCart.setVisibility(View.GONE);
                                                mActivityDetailBinding.btnAddToCart.setVisibility(View.VISIBLE);
                                                mActivityDetailBinding.btnAddToCart.setClickable(true);
                                                break;
                                            case "rlMinus":
                                                mActivityDetailBinding.llAddToCart.setVisibility(View.INVISIBLE);
                                                mActivityDetailBinding.cvAddToCart.setVisibility(View.INVISIBLE);
                                                mActivityDetailBinding.btnAddToCart.setAlpha(1f);
                                                mActivityDetailBinding.btnAddToCart.setClickable(true);
                                                mActivityDetailBinding.btnGoToCart.setVisibility(View.GONE);
                                                mActivityDetailBinding.btnAddToCart.setVisibility(View.VISIBLE);
                                            case "related":
                                                mSimilarProductListingAdapter.notifyDataSetChanged();
                                                break;
                                        }
                                    } else {
                                        switch (argWhich) {
                                            case "llAddToCart":
                                                mActivityDetailBinding.etQuantity.setText("1");
                                                //mActivityDetailBinding.llPlusMins.setVisibility(View.VISIBLE);
                                                mActivityDetailBinding.llAddToCart.setVisibility(View.VISIBLE);
                                                mActivityDetailBinding.cvAddToCart.setVisibility(View.VISIBLE);
                                                mActivityDetailBinding.btnGoToCart.setVisibility(View.VISIBLE);
                                                mActivityDetailBinding.btnAddToCart.setVisibility(View.GONE);
                                              *//*  mActivityDetailBinding.btnAddToCart.setAlpha(.1f);
                                                mActivityDetailBinding.btnAddToCart.setClickable(false);*//*
                                                break;
                                            case "rlPlus":
                                                mActivityDetailBinding.etQuantity.setText("" + argQty);
                                                break;
                                            case "rlMinus":
                                                mActivityDetailBinding.etQuantity.setText("" + argQty);
                                                break;
                                            case "related":
                                                mSimilarProductListingAdapter.notifyDataSetChanged();
                                                break;



                                        }
                                        ProductQuantityLocal mProductQuantityLocal = new ProductQuantityLocal(String.valueOf(argProductId), String.valueOf(argQty));
                                        if (!mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(argProductId)).equals("0")) {
                                            mDatabaseHandler.updateProductQuantityById(mProductQuantityLocal);
                                        } else {
                                            mDatabaseHandler.addProductQty(mProductQuantityLocal);
                                        }
                                    }
    */
                                    try {
                                        if (response.getString("is_age_verification").equals("False")) {
                                            Intent i = new Intent(DetailActivity.this, TobacoCatActivity.class);
                                            i.putExtra("message", mJsonObject.getString("msg"));
                                            startActivity(i);
                                        } else {
                                            Constants.showToastInMiddle(getApplicationContext(),  mJsonObject.getString("msg"));
                                        }
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

                    System.out.println("Sukdev : MyCart : requestAddToCart : VolleyError : " + error.toString());
                    mActivityDetailBinding.progressSpinKitView.setVisibility(View.GONE);

                }
            }) {
                @Override
                public Map<String, String> getHeaders() throws AuthFailureError {
                    HashMap<String, String> headers = new HashMap<String, String>();
                    headers.put("Content-Type", "application/json");
                    headers.put(Constants.VARIABLES.WAREHOUSE_KEY, mSharedPreferenceManager.getWarehouseId());
                    if (mSharedPreferenceManager.isLoggedIn()) {
                        headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));

                    }
                    return headers;
                }


            };


            // Adding request to request queue
            queue.add(jsonObjReq);
        } else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }

    public void AnimateBell() {

        Animation shake = AnimationUtils.loadAnimation(getApplicationContext(), R.anim.shake);
        //mActivityDetailBinding.badgeNotification.setVisibility(View.VISIBLE);
        mActivityDetailBinding.ivWishlistAdd.setImageResource(R.drawable.wishlist_added);
        mActivityDetailBinding.ivWishlistAdd.setAnimation(shake);
        mActivityDetailBinding.ivWishlistAdd.startAnimation(shake);

    }

    @Override
    public void connectMain(int argProductId, int argQuantity,int position) {

        try {
            requestAddToCart(argProductId, argQuantity, "related", "", "",position);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void sendSlug(String argSlug, int argProductId) {
        Intent i = new Intent(DetailActivity.this, DetailActivity.class);
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

        if (mSharedPreferenceManager.isLoggedIn()) {
            Intent i = new Intent(DetailActivity.this, SaveListPage.class);
            i.putExtra("product_id", argProductId);
            startActivity(i);
        } else {
            Intent i = new Intent(DetailActivity.this, LoginActivity.class);
            i.putExtra("from_where", "DetailPage");
            startActivity(i);
        }


    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        System.out.println("Sukdev : DeliveryDetail : onActivityResult : 1 : ");
        if (requestCode == 1) {
            System.out.println("Sukdev : DeliveryDetail : onActivityResult : 2 : ");
            if (data != null) {

                if (data.getStringExtra("review_done_or_not") != null) {
                    try {
                        requestProductRatingReview();
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            }
        } else {
            if (resultCode == Activity.RESULT_OK) {

                try {

                    requestAddToCart(Integer.parseInt(data.getStringExtra("argProductId")), 1, data.getStringExtra("arg_which"), data.getStringExtra("custom_field_name"), data.getStringExtra("custom_field_value"),Integer.parseInt(data.getStringExtra("position")));
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    @Override
    public void customFieldValueSelect(int argProductId, int argQuantity, String custom_field_name, String custom_field_value,int position) {

        Intent i = new Intent(DetailActivity.this, DialogPrepareView.class);
        i.putExtra("custom_field_name", custom_field_name);
        i.putExtra("custom_field_value", custom_field_value);
        i.putExtra("product_id", argProductId + "");
        i.putExtra("arg_which", "related");
        i.putExtra("position", position+"");
        startActivityForResult(i, 101);
    }

    @Override
    public void goToImageList(List<String> imageSliderUrlList) {
        if(imageSliderUrlList.size()>0) {
            Intent i = new Intent(DetailActivity.this, ZoominView.class);
            i.putStringArrayListExtra("image_url_list", (ArrayList<String>) imageSliderUrlList);
            startActivity(i);
        }
    }
}

class SliderAdapterDetail extends SliderViewAdapter<SliderAdapterDetail.SliderAdapterVH> {

    private Context context;
    private List<String> imageSliderUrlList;
private goToZoomImageList mGoToZoomImageList;
    public SliderAdapterDetail(Context context, List<String> imageSliderUrlList,goToZoomImageList mGoToZoomImageList) {
        this.context = context;
        this.mGoToZoomImageList=mGoToZoomImageList;
        this.imageSliderUrlList = imageSliderUrlList;
    }

    @Override
    public SliderAdapterVH onCreateViewHolder(ViewGroup parent) {
        View inflate = LayoutInflater.from(parent.getContext()).inflate(R.layout.detail_slider_layout, null);
        return new SliderAdapterVH(inflate);
    }

    @Override
    public void onBindViewHolder(SliderAdapterVH viewHolder, int position) {
        //viewHolder.textViewDescription.setText("This is slider item " + position);

        try {
            System.out.println("Sukdev : onBindViewHolder : imageSliderUrlList.get(position) : " + imageSliderUrlList.get(position));
            Glide.with(viewHolder.itemView)
                    .load(imageSliderUrlList.get(position))
                    .diskCacheStrategy(DiskCacheStrategy.NONE).skipMemoryCache(true)
                    .into(viewHolder.imageViewBackground);

        } catch (java.lang.NullPointerException ex) {

        }

        viewHolder.itemView.setOnClickListener(v->{
            mGoToZoomImageList.goToImageList(imageSliderUrlList);
        });
        /*switch (position) {
            case 0:
                Glide.with(viewHolder.itemView)
                        .load("https://images.pexels.com/photos/218983/pexels-photo-218983.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260")
                        .into(viewHolder.imageViewBackground);
                break;
            case 1:
                Glide.with(viewHolder.itemView)
                        .load("https://images.pexels.com/photos/747964/pexels-photo-747964.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260")
                        .into(viewHolder.imageViewBackground);
                break;
            case 2:
                Glide.with(viewHolder.itemView)
                        .load("https://images.pexels.com/photos/929778/pexels-photo-929778.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260")
                        .into(viewHolder.imageViewBackground);
                break;
            default:
                Glide.with(viewHolder.itemView)
                        .load("https://images.pexels.com/photos/218983/pexels-photo-218983.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260")
                        .into(viewHolder.imageViewBackground);
                break;

        }*/

    }

    @Override
    public int getCount() {
        //slider view count could be dynamic size

        try {
            return imageSliderUrlList.size();

        } catch (java.lang.NullPointerException ex) {
            return 0;
        }
    }

    class SliderAdapterVH extends SliderViewAdapter.ViewHolder {

        View itemView;
        ImageView imageViewBackground;
        TextView textViewDescription;

        public SliderAdapterVH(View itemView) {
            super(itemView);
            imageViewBackground = itemView.findViewById(R.id.iv_auto_image_slider);
            textViewDescription = itemView.findViewById(R.id.tv_auto_image_slider);
            this.itemView = itemView;
        }
    }
}