package com.gogrocery.view;

import android.app.Activity;
import android.content.Intent;
import androidx.databinding.DataBindingUtil;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Build;
import android.os.Bundle;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.SimpleItemAnimator;

import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
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
import com.facebook.appevents.AppEventsConstants;
import com.facebook.appevents.AppEventsLogger;
import com.gogrocery.Adapters.MyWishlistAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Customs.GridSpacingItemDecoration;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.PrepareViewOpenInterface;
import com.gogrocery.Interfaces.WishlistInterface;
import com.gogrocery.Models.CartModel.AddToCartModel;
import com.gogrocery.Models.ProductQuantityLocal;
import com.gogrocery.Models.WishlistModel.Data;
import com.gogrocery.Models.WishlistModel.MyWishlistModel;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityWishListPageBinding;
import com.google.firebase.analytics.FirebaseAnalytics;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class WishListPage extends AppCompatActivity implements WishlistInterface , PrepareViewOpenInterface {

    private ActivityWishListPageBinding mActivityWishListPageBinding;
    private SharedPreferenceManager mSharedPreferenceManager;
    private MyWishlistAdapter mMyWishlistAdapter;
    private List<Data> mWishlist ;
    private DatabaseHandler mDatabaseHandler;
    AppEventsLogger logger;
    private FirebaseAnalytics mFirebaseAnalytics;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityWishListPageBinding = DataBindingUtil.setContentView(this, R.layout.activity_wish_list_page);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        mDatabaseHandler = new DatabaseHandler(getApplicationContext());
        mFirebaseAnalytics = FirebaseAnalytics.getInstance(WishListPage.this);
        logger = AppEventsLogger.newLogger(this);
        mWishlist = new ArrayList<>();
        setMyWishlistRecyclerView();
        try {
            requestWishlist();


        } catch (JSONException e) {
            e.printStackTrace();
        }
        mActivityWishListPageBinding.ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        mActivityWishListPageBinding.ivFav.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent ivCart = new Intent(WishListPage.this, MyCart.class);
                startActivity(ivCart);
            }
        });

        if (Constants.VARIABLES.CART_COUNT > 0) {
            mActivityWishListPageBinding.tvCartCount.setVisibility(View.VISIBLE);
            mActivityWishListPageBinding.tvCartCount.setText("" + Constants.VARIABLES.CART_COUNT);
        } else {
            mActivityWishListPageBinding.tvCartCount.setVisibility(View.GONE);
        }

hideStatusBarColor();
    }


    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }

    private void setMyWishlistRecyclerView() {
        mMyWishlistAdapter = new MyWishlistAdapter(getApplicationContext(), mDatabaseHandler, this,this);
        GridLayoutManager mGridLayoutManager = new GridLayoutManager(getApplicationContext(), 2);
        mActivityWishListPageBinding.rvMyWhishlist.setLayoutManager(mGridLayoutManager);
        ((SimpleItemAnimator) mActivityWishListPageBinding.rvMyWhishlist.getItemAnimator()).setSupportsChangeAnimations(false);
 /*       mActivityWishListPageBinding.rvMyWhishlist.addItemDecoration(new GridSpacingItemDecoration(2, GridSpacingItemDecoration.dpToPx(getApplicationContext(), 1), true));
        mActivityWishListPageBinding.rvMyWhishlist.setItemAnimator(new DefaultItemAnimator());*/
        mActivityWishListPageBinding.rvMyWhishlist.setAdapter(mMyWishlistAdapter);
        mActivityWishListPageBinding.rvMyWhishlist.setNestedScrollingEnabled(false);
    }

    public void requestWishlist() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        System.out.println("Rahul : WishListPage : requestWishlist : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
        StringRequest jsonObjReq = new StringRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.MY_WISH_LIST,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {

                        Gson mGson = new Gson();
                        JSONObject mJsonObject = null;
                        try {
                            mJsonObject = new JSONObject(response);
                            System.out.println("Rahul : WishListPage : requestWishlist : mJsonObject : " + mJsonObject);
                            MyWishlistModel myWishlistModel = mGson.fromJson(response, MyWishlistModel.class);
                            if (myWishlistModel.getStatus() == Integer.parseInt(Constants.VARIABLES.STATUS_SUCESS_CODE)) {

                                if (myWishlistModel.getData().size() > 0) {
                                    mWishlist.addAll(myWishlistModel.getData());
                                    System.out.println("Rahul : WishListPage : requestWishlist : mWishlist.size : " + mWishlist.size());
                                    mActivityWishListPageBinding.sfl.stopShimmer();
                                    mActivityWishListPageBinding.sfl.setVisibility(View.GONE);
                                    mActivityWishListPageBinding.noWhishlist.setVisibility(View.GONE);
                                    mActivityWishListPageBinding.rvMyWhishlist.setVisibility(View.VISIBLE);
                                    mMyWishlistAdapter.clearWishList();
                                    mMyWishlistAdapter.addAllWishList(mWishlist);
                                    mMyWishlistAdapter.notifyDataSetChanged();

                                } else {
                                    mActivityWishListPageBinding.sfl.stopShimmer();
                                    mActivityWishListPageBinding.sfl.setVisibility(View.GONE);

                                    mActivityWishListPageBinding.noWhishlist.setVisibility(View.VISIBLE);
                                    mActivityWishListPageBinding.rvMyWhishlist.setVisibility(View.GONE);
                                    mActivityWishListPageBinding.tvCartCount.setVisibility(View.VISIBLE);
                                }
                            } else {
                                System.out.println("Rahul : WishListPage : requestWishlist : mWishlist : " + mGson.toJson(mWishlist));
                                mActivityWishListPageBinding.sfl.stopShimmer();
                                mActivityWishListPageBinding.sfl.setVisibility(View.GONE);

                                mActivityWishListPageBinding.noWhishlist.setVisibility(View.VISIBLE);
                                mActivityWishListPageBinding.rvMyWhishlist.setVisibility(View.GONE);
                                mActivityWishListPageBinding.tvCartCount.setVisibility(View.VISIBLE);

                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                            mActivityWishListPageBinding.sfl.stopShimmer();
                            mActivityWishListPageBinding.sfl.setVisibility(View.GONE);
                            mActivityWishListPageBinding.noWhishlist.setVisibility(View.VISIBLE);

                            mActivityWishListPageBinding.rvMyWhishlist.setVisibility(View.GONE);
                            mActivityWishListPageBinding.tvCartCount.setVisibility(View.GONE);
                            mActivityWishListPageBinding.sfl.stopShimmer();
                            mActivityWishListPageBinding.sfl.setVisibility(View.GONE);
                            mActivityWishListPageBinding.tvCartCount.setVisibility(View.VISIBLE);
                        }

                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                Constants.VARIABLES.mWishlistModelAddedList.clear();
                System.out.println("Rahul : WishListPage : requestWishlist : VolleyError : " + error.toString());
                mActivityWishListPageBinding.sfl.stopShimmer();
                mActivityWishListPageBinding.sfl.setVisibility(View.GONE);
                mActivityWishListPageBinding.noWhishlist.setVisibility(View.VISIBLE);
                mActivityWishListPageBinding.rvMyWhishlist.setVisibility(View.GONE);
              //  mActivityWishListPageBinding.tvCartCount.setVisibility(View.GONE);

            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                headers.put("WID", mSharedPreferenceManager.getWarehouseId());
                headers.put("website_id", "1");
                return headers;
            }


        };


        // Adding request to request queue
        queue.add(jsonObjReq);
    }

    public void requestRemoveFromWishlist(int argProductId, int argPosition) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("website_id", 1);
        mJsonObject.put("product_id", argProductId);
        mJsonObject.put("warehouse_id", mSharedPreferenceManager.getWarehouseId());

        System.out.println("Rahul : WishListPage : requestRemoveFromWishlist : param : " + mJsonObject);


        mActivityWishListPageBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(com.android.volley.Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.DELETE_WISHLIST, mJsonObject,
                new com.android.volley.Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        mActivityWishListPageBinding.progressSpinKitView.setVisibility(View.GONE);

                        System.out.println("Rahul : WishListPage : requestRemoveFromWishlist : mJsonObject : " + mJsonObject);

                        try {

                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            System.out.println("Rahul : WishListPage : requestRemoveFromWishlist : mJsonObject : " + mJsonObject);

                            MyWishlistModel myWishlistModel = mGson.fromJson(mJsonObject.toString(), MyWishlistModel.class);

                            if (myWishlistModel.getStatus() == Integer.parseInt(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                mWishlist = new ArrayList<>();
                                if (myWishlistModel.getData().size() > 0) {
                                    mWishlist.addAll(myWishlistModel.getData());
                                    System.out.println("Rahul : WishListPage : requestRemoveFromWishlist : mWishlist.size : " + mWishlist.size());
                                    mActivityWishListPageBinding.noWhishlist.setVisibility(View.GONE);
                                    mActivityWishListPageBinding.rvMyWhishlist.setVisibility(View.VISIBLE);
                                    mMyWishlistAdapter.clearWishList();
                                    mMyWishlistAdapter.addAllWishList(mWishlist);
                                    mMyWishlistAdapter.notifyDataSetChanged();

                                } else {

                                    mActivityWishListPageBinding.noWhishlist.setVisibility(View.VISIBLE);
                                    mActivityWishListPageBinding.rvMyWhishlist.setVisibility(View.GONE);
                                    mActivityWishListPageBinding.tvCartCount.setVisibility(View.VISIBLE);
                                }
                                if (mDatabaseHandler.checkWishlistAvailable("" + argProductId)) {

                                    mDatabaseHandler.deleteWishlistSingleRecord("" + argProductId);
                                }
                            } else {
                                System.out.println("Rahul : WishListPage : requestWishlist : mWishlist : " + mGson.toJson(mWishlist));

                                Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();
                                mActivityWishListPageBinding.noWhishlist.setVisibility(View.VISIBLE);
                                mActivityWishListPageBinding.rvMyWhishlist.setVisibility(View.GONE);
                                mActivityWishListPageBinding.tvCartCount.setVisibility(View.VISIBLE);

                            }

                        /*    if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();

                                mWishlist.remove(argPosition);
                                mMyWishlistAdapter.notifyItemRemoved(argPosition);
                                mMyWishlistAdapter.notifyItemRangeChanged(argPosition, mWishlist.size());


                                mMyWishlistAdapter.notifyDataSetChanged();


                            } else {


                            }*/
                        } catch (JSONException e) {
                            e.printStackTrace();

                        } catch (Exception e) {
                            e.printStackTrace();

                        }

                    }
                }, new com.android.volley.Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : WishListPage : requestRemoveFromWishlist : VolleyError : " + error.toString());
                mActivityWishListPageBinding.progressSpinKitView.setVisibility(View.GONE);

            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
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

    public void requestAddToCart(int argProductId, int argQty,String mCustomFieldName, String mCustomFieldValue,int position) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));
        mJsonObject.put("product_id", argProductId);
        mJsonObject.put("quantity", argQty);
        mJsonObject.put("year_check", mSharedPreferenceManager.getYearCheck());
        mJsonObject.put("custom_field_name", mCustomFieldName);
        mJsonObject.put("custom_field_value", mCustomFieldValue);
        System.out.println("Rahul : WishListPage : requestAddToCart : param : " + mJsonObject);
        System.out.println("Rahul : WishListPage : requestAddToCart : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));


        mActivityWishListPageBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(com.android.volley.Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.ADD_TO_CART, mJsonObject,
                new com.android.volley.Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {

                        try {
                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            System.out.println("Rahul : WishListPage : requestAddToCart : mJsonObject : " + mJsonObject);

                            AddToCartModel mAddToCartModel = mGson.fromJson(mJsonObject.toString(), AddToCartModel.class);
                            if (mAddToCartModel.getStatus() == 1) {
                                if (argQty == 0) {
                                    mDatabaseHandler.deleteSingleRecord(String.valueOf(argProductId));
                                } else {
                                    mActivityWishListPageBinding.tvCartCount.setVisibility(View.VISIBLE);
                                    Constants.VARIABLES.CART_COUNT = Integer.parseInt(mAddToCartModel.getCartData().getCart_count());
                                    mActivityWishListPageBinding.tvCartCount.setText(mAddToCartModel.getCartData().getCart_count());

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


                                    System.out.println("Rahul : WishListPage : checkDbCount : " + mDatabaseHandler.getAllProductQtyData().size());
                                }


                                if (Integer.parseInt(mAddToCartModel.getCartData().getCart_count()) == 0) {
                                    mActivityWishListPageBinding.tvCartCount.setVisibility(View.GONE);
                                    Constants.VARIABLES.CART_COUNT = 0;

                                } else {




                                   // AnimateBell();
                                }
                                Bundle params = new Bundle();
                           /*     params.putString("productName",mAddToCartModel.getCartData().getCartdetails().get(0).getName());
                                params.putString("productId",mAddToCartModel.getCartData().getCartdetails().get(0).getId());
                                params.putString("addedQuanity",mAddToCartModel.getCartData().getCart_count());
                                params.putString("content_type","product");
                                params.putString("currency", Constants.VARIABLES.CURRENT_CURRENCY);
                                mFirebaseAnalytics.logEvent(FirebaseAnalytics.Event.ADD_TO_CART, params);
                                logger.logEvent(AppEventsConstants.EVENT_NAME_ADDED_TO_CART, params);*/
                            } else {
                                try {
                                    if(response.getString("is_age_verification").equals("False")) {
                                        Intent i = new Intent(WishListPage.this, TobacoCatActivity.class);
                                        i.putExtra("message", mAddToCartModel.getMsg());
                                        startActivity(i);
                                    }else{
                                        Constants.showToastInMiddle(getApplicationContext(), mAddToCartModel.getMsg());
                                    }
                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }


                            }
                           // mMyWishlistAdapter.notifyDataSetChanged();
                            mMyWishlistAdapter.notifyItemChanged(position);
                            mActivityWishListPageBinding.progressSpinKitView.setVisibility(View.GONE);
                        } catch (Exception exception) {
                            exception.printStackTrace();
                            System.out.println("Rahul : WishListPage : Exception : " + exception);

                        }
                    }
                }, new com.android.volley.Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : WishListPage : requestAddToCart : VolleyError : " + error.toString());
                mActivityWishListPageBinding.progressSpinKitView.setVisibility(View.GONE);
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
        queue.add(jsonObjReq);
    }

/*    public void AnimateBell() {
        Animation shake = AnimationUtils.loadAnimation(getApplicationContext(), R.anim.shake);
        mActivityWishListPageBinding.badgeNotification.setVisibility(View.VISIBLE);
        mActivityWishListPageBinding.ivCart.setImageResource(R.drawable.cart);
        mActivityWishListPageBinding.ivCart.setAnimation(shake);
        mActivityWishListPageBinding.ivCart.startAnimation(shake);

    }*/

    @Override
    public void removeNullChannelPriceData(int argPosition) {
        mWishlist.remove(argPosition);
//        mMyWishlistAdapter.notifyDataSetChanged();
    }

    @Override
    public void removeItemFromWishlist(int argProductid, int argPosition) {
        try {
            requestRemoveFromWishlist(argProductid, argPosition);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void connectMain(int argProductId, int argQuantity, int argPosition) {
        try {
            requestAddToCart(argProductId, argQuantity,"","",argPosition);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void connectToDetail(int argProductId, String argSlug) {
        Intent i = new Intent(WishListPage.this, DetailActivity.class);
        i.putExtra("slug", argSlug.split("#GoGrocery#")[0]);
        i.putExtra("title", argSlug.split("#GoGrocery#")[1]);
        i.putExtra("product_id", argProductId);
        startActivity(i);
    }


    @Override
    public void customFieldValueSelect(int argProductId, int argQuantity, String custom_field_name, String custom_field_value,int position) {
        Intent i = new Intent(WishListPage.this, DialogPrepareView.class);
        i.putExtra("custom_field_name", custom_field_name);
        i.putExtra("custom_field_value", custom_field_value);
        i.putExtra("product_id", argProductId+"");
        i.putExtra("position", position+"");
        startActivityForResult(i,101);
    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == 101) {
            if(resultCode == Activity.RESULT_OK){

                try {

                    requestAddToCart(Integer.parseInt(data.getStringExtra("argProductId")), 1,data.getStringExtra("custom_field_name"),data.getStringExtra("custom_field_value"),Integer.parseInt(data.getStringExtra("position")));
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
