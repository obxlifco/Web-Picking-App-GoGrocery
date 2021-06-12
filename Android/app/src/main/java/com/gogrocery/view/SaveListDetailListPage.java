package com.gogrocery.view;

import android.content.Intent;
import androidx.databinding.DataBindingUtil;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.GridLayoutManager;
import android.view.View;
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
import com.gogrocery.Adapters.SaveListDetailPageAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Customs.GridSpacingItemDecoration;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.SaveListDetailInterface;
import com.gogrocery.Models.CartModel.AddToCartModel;
import com.gogrocery.Models.ProductQuantityLocal;
import com.gogrocery.Models.SaveListDetailPage.SaveListDetailListData;
import com.gogrocery.Models.SaveListDetailPage.SaveListDetailModel;
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

import static com.gogrocery.Constants.Constants.BASE_URL;

public class SaveListDetailListPage extends AppCompatActivity implements SaveListDetailInterface {

    private ActivityWishListPageBinding mActivityWishListPageBinding;
    private SharedPreferenceManager mSharedPreferenceManager;
    private SaveListDetailPageAdapter mMyWishlistAdapter;
    private List<SaveListDetailListData> mWishlist = new ArrayList<>();
    private DatabaseHandler mDatabaseHandler;
    private String slug = "";

    private FirebaseAnalytics mFirebaseAnalytics;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityWishListPageBinding = DataBindingUtil.setContentView(this, R.layout.activity_wish_list_page);
        mFirebaseAnalytics = FirebaseAnalytics.getInstance(this);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        mDatabaseHandler = new DatabaseHandler(getApplicationContext());


       // mActivityWishListPageBinding.tvListingTitle.setText(getIntent().getExtras().getString("slug").split("#GOGROCERY#")[0]);
        slug = getIntent().getExtras().getString("slug").split("#GOGROCERY#")[1];

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
/*
        mActivityWishListPageBinding.ivCart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent ivCart = new Intent(SaveListDetailListPage.this, MyCart.class);
                startActivity(ivCart);
            }
        });*/


   /*     if (Constants.VARIABLES.CART_COUNT > 0) {
            mActivityWishListPageBinding.badgeNotification.setVisibility(View.VISIBLE);
            mActivityWishListPageBinding.badgeNotification.setText("" + Constants.VARIABLES.CART_COUNT);
        } else {
            mActivityWishListPageBinding.badgeNotification.setVisibility(View.GONE);
        }
*/

    }

    private void setMyWishlistRecyclerView() {
        mMyWishlistAdapter = new SaveListDetailPageAdapter(getApplicationContext(), mWishlist, mDatabaseHandler, this);
        GridLayoutManager mGridLayoutManager = new GridLayoutManager(getApplicationContext(), 2);
        mActivityWishListPageBinding.rvMyWhishlist.setLayoutManager(mGridLayoutManager);
        mActivityWishListPageBinding.rvMyWhishlist.addItemDecoration(new GridSpacingItemDecoration(2, GridSpacingItemDecoration.dpToPx(getApplicationContext(), 1), true));
        mActivityWishListPageBinding.rvMyWhishlist.setItemAnimator(new DefaultItemAnimator());
        mActivityWishListPageBinding.rvMyWhishlist.setAdapter(mMyWishlistAdapter);
        mActivityWishListPageBinding.rvMyWhishlist.setNestedScrollingEnabled(false);
    }


    public void requestWishlist() throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        System.out.println("Rahul : SaveListDetailListPage : requestWishlist : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
        System.out.println("Rahul : SaveListDetailListPage : requestWishlist : URL : " + Constants.BASE_URL + Constants.API_METHODS.SAVE_LIST_DATAIL_LIST + slug + "/");
        StringRequest jsonObjReq = new StringRequest(Request.Method.GET,
                Constants.BASE_URL + Constants.API_METHODS.SAVE_LIST_DATAIL_LIST + slug + "/",
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {

            /*            Gson mGson = new Gson();
                        JSONObject mJsonObject = null;
                        try {
                            mJsonObject = new JSONObject(response);
                            System.out.println("Rahul : SaveListDetailListPage : requestWishlist : mJsonObject : " + mJsonObject);
                            SaveListDetailModel myWishlistModel = mGson.fromJson(response, SaveListDetailModel.class);
                            if (myWishlistModel.getStatus() == Integer.parseInt(Constants.VARIABLES.STATUS_SUCESS_CODE)) {

                                if (myWishlistModel.getData().size() > 0) {
                                    mWishlist.addAll(myWishlistModel.getData());
                                    System.out.println("Rahul : SaveListDetailListPage : requestWishlist : mWishlist.size : " + mWishlist.size());
                                    System.out.println("Rahul : SaveListDetailListPage : requestWishlist : mWishlist : " + mGson.toJson(mWishlist));
                                    System.out.println("Rahul : SaveListDetailListPage : requestWishlist : myWishlistModel.getData() : " + mGson.toJson(myWishlistModel.getData()));

                                    mActivityWishListPageBinding.sfl.stopShimmer();
                                    mActivityWishListPageBinding.sfl.setVisibility(View.GONE);
                                    mActivityWishListPageBinding.rvMyWhishlist.setVisibility(View.VISIBLE);

                                    mMyWishlistAdapter.notifyDataSetChanged();

                                } else {
                                    mActivityWishListPageBinding.sfl.stopShimmer();
                                    mActivityWishListPageBinding.sfl.setVisibility(View.GONE);
                                    mActivityWishListPageBinding.includeNoResponse.tvWishlistTitle.setText("Your Savelist is empty!");
                                    mActivityWishListPageBinding.includeNoResponse.btnShopNow.setVisibility(View.GONE);
                                    mActivityWishListPageBinding.noResponse.setVisibility(View.VISIBLE);
                                    mActivityWishListPageBinding.badgeNotification.setVisibility(View.GONE);
                                }
                            } else {
                                System.out.println("Rahul : SaveListDetailListPage : requestWishlist : mWishlist : " + mGson.toJson(mWishlist));
                                mActivityWishListPageBinding.sfl.stopShimmer();
                                mActivityWishListPageBinding.sfl.setVisibility(View.GONE);
                                mActivityWishListPageBinding.noResponse.setVisibility(View.GONE);
                                mActivityWishListPageBinding.badgeNotification.setVisibility(View.GONE);

                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                            mActivityWishListPageBinding.sfl.stopShimmer();
                            mActivityWishListPageBinding.sfl.setVisibility(View.GONE);
                            mActivityWishListPageBinding.includeNoResponse.tvWishlistTitle.setText("Your Savelist is empty!");
                            mActivityWishListPageBinding.includeNoResponse.btnShopNow.setVisibility(View.GONE);
                            mActivityWishListPageBinding.noResponse.setVisibility(View.VISIBLE);
                            mActivityWishListPageBinding.badgeNotification.setVisibility(View.GONE);
                        } catch (Exception exception) {
                            exception.printStackTrace();
                            mActivityWishListPageBinding.sfl.stopShimmer();
                            mActivityWishListPageBinding.sfl.setVisibility(View.GONE);
                            mActivityWishListPageBinding.includeNoResponse.tvWishlistTitle.setText("Your Savelist is empty!");
                            mActivityWishListPageBinding.includeNoResponse.btnShopNow.setVisibility(View.GONE);
                            mActivityWishListPageBinding.noResponse.setVisibility(View.VISIBLE);
                            mActivityWishListPageBinding.badgeNotification.setVisibility(View.GONE);
                        }
*/
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                Constants.VARIABLES.mWishlistModelAddedList.clear();
                System.out.println("Rahul : SaveListDetailListPage : requestWishlist : VolleyError : " + error.toString());
          /*      mActivityWishListPageBinding.sfl.stopShimmer();
                mActivityWishListPageBinding.sfl.setVisibility(View.GONE);
                mActivityWishListPageBinding.includeNoResponse.tvWishlistTitle.setText("Your Savelist is empty!");
                mActivityWishListPageBinding.includeNoResponse.btnShopNow.setVisibility(View.GONE);
                mActivityWishListPageBinding.noResponse.setVisibility(View.VISIBLE);
                mActivityWishListPageBinding.badgeNotification.setVisibility(View.GONE);*/

            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));
                headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());
                return headers;
            }


        };


        // Adding request to request queue
        queue.add(jsonObjReq);
    }

    public void requestRemoveFromSaveList(int argProductId, int argListId, int argPosition) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JSONObject mJsonObject = new JSONObject();

        mJsonObject.put("website_id", 1);
        mJsonObject.put("product_id", argProductId);
        mJsonObject.put("action", "del");
        mJsonObject.put("list_id", argListId);

        System.out.println("Rahul : SaveListDetailListPage : requestRemoveFromWishlist : param : " + mJsonObject);


        mActivityWishListPageBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.PUT,
                BASE_URL + Constants.API_METHODS.DELETE_PRODUCT_FROM_SAVE_LIST, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        mActivityWishListPageBinding.progressSpinKitView.setVisibility(View.GONE);
                        Gson mGson = new Gson();
                        JSONObject mJsonObject = response;
                        System.out.println("Rahul : SaveListDetailListPage : requestRemoveFromWishlist : mJsonObject : " + mJsonObject);

                        try {
                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                Toast.makeText(getApplicationContext(), response.getString("msg"), Toast.LENGTH_LONG).show();

                                mWishlist.remove(argPosition);
                                mMyWishlistAdapter.notifyItemRemoved(argPosition);
                                mMyWishlistAdapter.notifyItemRangeChanged(argPosition, mWishlist.size());

                                if (mDatabaseHandler.checkWishlistAvailable("" + argProductId)) {

                                    mDatabaseHandler.deleteWishlistSingleRecord("" + argProductId);
                                }
                                mMyWishlistAdapter.notifyDataSetChanged();
                            } else {
                                Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();

                            }
                        } catch (JSONException e) {
                            e.printStackTrace();

                        } catch (Exception e) {
                            e.printStackTrace();

                        }

                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : SaveListDetailListPage : requestRemoveFromWishlist : VolleyError : " + error.toString());
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

    public void requestAddToCart(int argProductId, int argQty, int argPosition) throws JSONException {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));
        mJsonObject.put("product_id", argProductId);
        mJsonObject.put("quantity", argQty);
        mJsonObject.put("year_check", mSharedPreferenceManager.getYearCheck());
        System.out.println("Rahul : SaveListDetailListPage : requestAddToCart : param : " + mJsonObject);
        System.out.println("Rahul : SaveListDetailListPage : requestAddToCart : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));


        mActivityWishListPageBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                BASE_URL + Constants.API_METHODS.ADD_TO_CART, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {

                        try {
                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            System.out.println("Rahul : SaveListDetailListPage : requestAddToCart : mJsonObject : " + mJsonObject);

                            AddToCartModel mAddToCartModel = mGson.fromJson(mJsonObject.toString(), AddToCartModel.class);
                            if (mAddToCartModel.getStatus() == 1) {
                                if (argQty == 0) {
                                    mDatabaseHandler.deleteSingleRecord(String.valueOf(argProductId));
                                } else {

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


                                    System.out.println("Rahul : SaveListDetailListPage : checkDbCount : " + mDatabaseHandler.getAllProductQtyData().size());
                                }

                       /*         if (Integer.parseInt(mAddToCartModel.getCartData().getCart_count()) == 0) {
                                    mActivityWishListPageBinding.badgeNotification.setVisibility(View.GONE);

                                } else {
                                    Constants.VARIABLES.CART_COUNT = Integer.parseInt(mAddToCartModel.getCartData().getCart_count());
                                    mActivityWishListPageBinding.badgeNotification.setText(mAddToCartModel.getCartData().getCart_count());


                                    AnimateBell();
                                }*/
                                Bundle params = new Bundle();
                                params.putString(FirebaseAnalytics.Param.ITEM_NAME,mAddToCartModel.getCartData().getCartdetails().get(0).getName());
                                params.putString("total_qty_of_items",mAddToCartModel.getCartData().getCart_count());
                                mFirebaseAnalytics.logEvent(FirebaseAnalytics.Event.ADD_TO_CART, params);
                            } else {
                                try {
                                    if(response.getString("is_age_verification").equals("False")) {
                                        Intent i = new Intent(SaveListDetailListPage.this, TobacoCatActivity.class);
                                        i.putExtra("message", mAddToCartModel.getMsg());
                                        startActivity(i);
                                    }else{
                                        Constants.showToastInMiddle(getApplicationContext(), mAddToCartModel.getMsg());
                                    }
                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }

                            }
                            mMyWishlistAdapter.notifyDataSetChanged();
                            mActivityWishListPageBinding.progressSpinKitView.setVisibility(View.GONE);
                        } catch (Exception exception) {
                            exception.printStackTrace();
                            System.out.println("Rahul : SaveListDetailListPage : Exception : " + exception);

                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : SaveListDetailListPage : requestAddToCart : VolleyError : " + error.toString());
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
    public void removeItemFromWishlist(int argProductid, int argListId, int argPosition) {
        try {
            requestRemoveFromSaveList(argProductid, argListId, argPosition);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void connectMain(int argProductId, int argQuantity, int argPosition) {
        try {
            requestAddToCart(argProductId, argQuantity, argPosition);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void connectToDetail(int argProductId, String argSlug) {
        Intent i = new Intent(SaveListDetailListPage.this, DetailActivity.class);
        i.putExtra("slug", argSlug.split("#GoGrocery#")[0]);
        i.putExtra("title", argSlug.split("#GoGrocery#")[1]);
        i.putExtra("product_id", argProductId);
        startActivity(i);
    }


}
