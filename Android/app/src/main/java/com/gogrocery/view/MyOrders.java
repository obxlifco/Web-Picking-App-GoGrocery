package com.gogrocery.view;

import android.content.Intent;
import androidx.databinding.DataBindingUtil;

import com.gogrocery.R;
import com.google.android.material.tabs.TabLayout;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentPagerAdapter;
import androidx.fragment.app.FragmentTransaction;
import androidx.viewpager.widget.ViewPager;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Build;
import android.os.Bundle;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.LinearLayoutManager;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;

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
import com.gogrocery.Customs.RecyclerTouchListener;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Fragment.MyOrdersFragmentPast;
import com.gogrocery.Fragment.MyOrdersFragmentPresent;
import com.gogrocery.Interfaces.PaymentPageRedirectionInterface;
import com.gogrocery.Models.MyOrdersHistoryModel.Data;
import com.gogrocery.Models.MyOrdersHistoryModel.MyOrdersHistoryModel;
import com.gogrocery.databinding.ActivityMyOrdersBinding;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


public class MyOrders extends AppCompatActivity implements PaymentPageRedirectionInterface {

    private ActivityMyOrdersBinding mActivityMyOrdersBinding;
    public int tabSelected = 0;
    private SharedPreferenceManager mSharedPreferenceManager;
    private DatabaseHandler mDatabaseHandler;
    private List<Data> mMyOrdersHistoryList = new ArrayList<>();
    private MyOrdersHistoryAdapter mMyOrdersHistoryAdapter;
    private RecyclerTouchListener onTouchListener;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityMyOrdersBinding = DataBindingUtil.setContentView(this, R.layout.activity_my_orders);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        mDatabaseHandler = new DatabaseHandler(getApplicationContext());
hideStatusBarColor();
       /* setViewCartRecyclerView();
        try {
            requestMyOrdersHistoryList();
        } catch (JSONException e) {
            e.printStackTrace();
        }*/

        mActivityMyOrdersBinding.ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

/*        mActivityMyOrdersBinding.rlBadge.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(MyOrders.this, MyCart.class);
                startActivity(i);
                finish();
            }
        });*/

/*        mActivityMyOrdersBinding.ivCart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent ivCart = new Intent(MyOrders.this, MyCart.class);
                startActivity(ivCart);
            }
        });*/
/*

        if (Constants.VARIABLES.CART_COUNT > 0) {
            mActivityMyOrdersBinding.badgeNotification.setVisibility(View.VISIBLE);
            mActivityMyOrdersBinding.badgeNotification.setText("" + Constants.VARIABLES.CART_COUNT);
        } else {
            mActivityMyOrdersBinding.rlBadge.setVisibility(View.GONE);
        }
*/

        // intiateSwipe();
            setupViewPager(mActivityMyOrdersBinding.viewpager);
        mActivityMyOrdersBinding.tabs.setupWithViewPager(mActivityMyOrdersBinding.viewpager);


        mActivityMyOrdersBinding.tabs.addOnTabSelectedListener(new TabLayout.BaseOnTabSelectedListener() {
            @Override
            public void onTabSelected(TabLayout.Tab tab) {
                System.out.println("Rahul : MyOrders : addOnTabSelectedListener : onTabSelected : " + tab.getPosition());
                tabSelected = tab.getPosition();
            }

            @Override
            public void onTabUnselected(TabLayout.Tab tab) {
                System.out.println("Rahul : MyOrders : addOnTabSelectedListener : onTabUnselected : " + tab.getPosition());
            }

            @Override
            public void onTabReselected(TabLayout.Tab tab) {
                System.out.println("Rahul : MyOrders : addOnTabSelectedListener : onTabReselected : " + tab.getPosition());
            }
        });

        //loadFragment(new MyOrdersFragmentPresent(),"present");
    }


    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }
    public void loadFragment(Fragment fragment, String extraInfo) {

        Bundle bundle = new Bundle();
        bundle.putString("order_req_type", extraInfo);
// create a FragmentManager
        FragmentManager fm = getSupportFragmentManager();//****for v4 use getSupportFragmentManager
// create a FragmentTransaction to begin the transaction and replace the Fragment
        FragmentTransaction fragmentTransaction = fm.beginTransaction();
        fragment.setArguments(bundle);
        fragmentTransaction.setCustomAnimations(R.anim.enter_from_right, R.anim.exit_to_left, R.anim.enter_from_right, R.anim.exit_to_left);

        //fragmentTransaction.addToBackStack("" + currentFragPosition);
// replace the FrameLayout with new Fragment
        fragmentTransaction.replace(R.id.frameLayout, fragment);


        fragmentTransaction.commit(); // save the changes
    }

    private void setupViewPager(ViewPager viewPager) {
        ViewPagerAdapter adapter = new ViewPagerAdapter(getSupportFragmentManager());
      //  adapter.addFragment(new ProductSubstitutionsFragment(), "Product Substitutions");
        adapter.addFragment(new MyOrdersFragmentPresent(), "Present Orders");
        adapter.addFragment(new MyOrdersFragmentPast(), "Past Orders");

        viewPager.setAdapter(adapter);
    }

    class ViewPagerAdapter extends FragmentPagerAdapter {
        private final List<Fragment> mFragmentList = new ArrayList<>();
        private final List<String> mFragmentTitleList = new ArrayList<>();

        public ViewPagerAdapter(FragmentManager manager) {
            super(manager);
        }

        @Override
        public Fragment getItem(int position) {
            return mFragmentList.get(position);
        }

        @Override
        public int getCount() {
            return mFragmentList.size();
        }

        public void addFragment(Fragment fragment, String title) {
            mFragmentList.add(fragment);
            mFragmentTitleList.add(title);
        }

        @Override
        public CharSequence getPageTitle(int position) {
            return mFragmentTitleList.get(position);
        }
    }

  /*  @Override
    protected void onResume() {
        super.onResume();
        mActivityMyOrdersBinding.rvMyOrdersRecyclerView.addOnItemTouchListener(onTouchListener);
    }

    @Override
    protected void onPause() {
        super.onPause();
        mActivityMyOrdersBinding.rvMyOrdersRecyclerView.removeOnItemTouchListener(onTouchListener);
    }*/


  /*  private void intiateSwipe() {
        onTouchListener = new RecyclerTouchListener(this, mActivityMyOrdersBinding.rvMyOrdersRecyclerView);
        onTouchListener
                .setClickable(new RecyclerTouchListener.OnRowClickListener() {
                    @Override
                    public void onRowClicked(int position) {
                        //Toast.makeText(getApplicationContext(), "Row " + (position + 1) + " clicked!", Toast.LENGTH_LONG).show();
                    }

                    @Override
                    public void onIndependentViewClicked(int independentViewID, int position) {
                        //Toast.makeText(getApplicationContext(), "Button in row " + (position + 1) + " clicked!", Toast.LENGTH_LONG).show();
                    }
                })
                .setLongClickable(true, new RecyclerTouchListener.OnRowLongClickListener() {
                    @Override
                    public void onRowLongClicked(int position) {
                        // Toast.makeText(getApplicationContext(), "Row " + (position + 1) + " long clicked!", Toast.LENGTH_LONG).show();
                    }
                })
                .setSwipeOptionViews(R.id.add)
                .setSwipeable(R.id.cvDeliveryDetail, R.id.rowBG, new RecyclerTouchListener.OnSwipeOptionsClickListener() {
                    @Override
                    public void onSwipeOptionClicked(int viewID, int position) {
                        String message = "";
                        if (viewID == R.id.add) {
                            message += "Add";
                           *//* try {
                                //requestDeleteAddress(String.valueOf(mMyOrdersHistoryList.get(position).getId()), position);
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }*//*

                        }  *//*else if (viewID == R.id.change) {
                            message += "Change";
                        }*//*
                        message += " clicked for row " + (position + 1);
                        // Toast.makeText(getApplicationContext(), message, Toast.LENGTH_LONG).show();
                    }
                });


    }*/

        private void setViewCartRecyclerView() {
            mMyOrdersHistoryAdapter = new MyOrdersHistoryAdapter(getApplicationContext(), mMyOrdersHistoryList, this);
            LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.VERTICAL, false);
            mActivityMyOrdersBinding.rvMyOrdersRecyclerView.setLayoutManager(mLayoutManager);
            //mActivityMyOrdersBinding.rvMyOrdersRecyclerView.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
            mActivityMyOrdersBinding.rvMyOrdersRecyclerView.setItemAnimator(new DefaultItemAnimator());
            mActivityMyOrdersBinding.rvMyOrdersRecyclerView.setAdapter(mMyOrdersHistoryAdapter);
            mActivityMyOrdersBinding.rvMyOrdersRecyclerView.setNestedScrollingEnabled(false);
        }

        public void requestMyOrdersHistoryList() throws JSONException {
            mActivityMyOrdersBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            System.out.println("Rahul : MyOrders : requestMyOrdersHistoryList : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
            JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                    Constants.BASE_URL + Constants.API_METHODS.ORDER_HISTORY, null,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {

                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            System.out.println("Rahul : MyOrders : requestMyOrdersHistoryList : mJsonObject : " + mJsonObject);
                            MyOrdersHistoryModel mMyOrdersHistoryModel = mGson.fromJson(mJsonObject.toString(), MyOrdersHistoryModel.class);
                            mMyOrdersHistoryList.addAll(mMyOrdersHistoryModel.getData());

                            mMyOrdersHistoryAdapter.notifyDataSetChanged();
                            mActivityMyOrdersBinding.progressSpinKitView.setVisibility(View.GONE);
                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {
                    mActivityMyOrdersBinding.progressSpinKitView.setVisibility(View.GONE);
                    mActivityMyOrdersBinding.somethingwentwrong.setVisibility(View.VISIBLE);
                    System.out.println("Rahul : MyOrders : requestMyOrdersHistoryList : VolleyError : " + error.toString());

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
            mActivityMyOrdersBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
            System.out.println("Rahul : MyOrders : requestOrderCancel : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
            System.out.println("Rahul : MyOrders : requestOrderCancel : argOrderId : " + argOrderId);

            JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.GET,
                    Constants.BASE_URL + Constants.API_METHODS.CANCEL_ORDER + argOrderId + "/", null,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            System.out.println("Rahul : MyOrders : requestOrderCancel : response : " + response);
                            mActivityMyOrdersBinding.progressSpinKitView.setVisibility(View.GONE);
                            Gson mGson = new Gson();
                            JSONObject mJsonObject = response;
                            try {
                                if (mJsonObject.getString("status").equals("200")) {
                              /*  mMyOrdersHistoryList.remove(argPosition);
                                mMyOrdersHistoryAdapter.notifyItemRemoved(argPosition);
                                mMyOrdersHistoryAdapter.notifyItemRangeChanged(argPosition, mMyOrdersHistoryList.size());*/
                                    mMyOrdersHistoryList.get(argPosition).setStrOrderStatus("Cancelled");
                                    mMyOrdersHistoryAdapter.notifyDataSetChanged();
                                    Constants.showToastInMiddle(getApplicationContext(),"Order cancelled successfully");
                                    //Toast.makeText(getApplicationContext(), "Order cancelled successfully", Toast.LENGTH_LONG).show();

                                } else {
                                    Constants.showToastInMiddle(getApplicationContext(),"Something wrong! Try again later");

                                    //Toast.makeText(getApplicationContext(), "Something wrong! Try again later", Toast.LENGTH_LONG).show();
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {
                    mActivityMyOrdersBinding.progressSpinKitView.setVisibility(View.GONE);
                    mActivityMyOrdersBinding.somethingwentwrong.setVisibility(View.VISIBLE);
                    System.out.println("Rahul : MyOrders : requestOrderCancel : VolleyError : " + error.toString());

                }
            })

            {
                @Override
                public Map<String, String> getHeaders() throws AuthFailureError {
                    HashMap<String, String> headers = new HashMap<String, String>();
                    headers.put("Content-Type", "application/json");
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
        public void redirect(String argOrderID, String argOrderDetail) {
            Intent i = new Intent(MyOrders.this, PaymentOptionsAvailable.class);
            i.putExtra("orders_id", argOrderID);
            i.putExtra("order_detail", argOrderDetail);
            startActivity(i);
        }

        @Override
        public void redirectTODetailPage(String argOrderId, String cust_order_id, String argOrderDetail) {
            Intent i = new Intent(MyOrders.this, MyOrdersDetailPage.class);
            i.putExtra("orders_id", argOrderId);
            i.putExtra("cust_orders_id", cust_order_id);
            i.putExtra("order_detail", argOrderDetail);
            startActivity(i);
        }

        @Override
        public void requestForCancelOrder(String argOrderId, int argPosition) {
            try {
                requestOrderCancel(argOrderId, argPosition);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
}
