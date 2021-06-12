package com.gogrocery.picking.activity;

import androidx.appcompat.widget.PopupMenu;
import androidx.databinding.DataBindingUtil;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Build;
import android.os.Bundle;
import android.text.TextUtils;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Toast;
import com.bumptech.glide.Glide;
import com.google.android.material.tabs.TabLayout;
import com.gogrocery.picking.R;
import com.gogrocery.picking.databinding.ActivityMainBinding;
import com.gogrocery.picking.fragment.HomeFragment;
import com.gogrocery.picking.fragment.OrdersFragment;
import com.gogrocery.picking.fragment.ReturnFragment;
import com.gogrocery.picking.fragment.StockFragment;
import com.gogrocery.picking.network.APIClient;
import com.gogrocery.picking.network.APIInterface;
import com.gogrocery.picking.prefrences.AppPreferences;
import com.gogrocery.picking.response_pojo.general_pojo.GeneralResponse;
import com.gogrocery.picking.utils.AppUtilities;
import java.util.HashMap;

public class MainActivity extends BaseActivity implements PopupMenu.OnMenuItemClickListener {
    private FragmentManager mFragmentManager;
    private FragmentTransaction mFragmentTransaction;
    private Fragment mFragment;
    public ActivityMainBinding activityMainBinding;
    public final static String HOME = "Home.GoGrocery";
    public final static String ORDER = "Order.GoGrocery";
    public final static String STOCK = "Stock.GoGrocery";
    public final static String RETURN = "Return.GoGrocery";
    HomeFragment homeFragment = null;
    OrdersFragment ordersFragment = null;
    StockFragment stockFragment = null;
    ReturnFragment returnFragment = null;
    TokenReceiver tokenReceiver;
    String pushOrderID = "", order_status = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        activityMainBinding = DataBindingUtil.setContentView(this, R.layout.activity_main);
        activityMainBinding.setClickHandler(new MainClickHandler(this));
        mFragmentManager = getSupportFragmentManager();
        setupToolBar();
        setTabView();
        tokenReceiver = new TokenReceiver();
        registerReceiver(tokenReceiver, new IntentFilter("com.gogrocery.picking.receiver.NEW_TOKEN"));
        sendTokenToServer(AppPreferences.getInstance().getFirebaseToken());
        if (getIntent().getStringExtra("pushOrderID") != null && !TextUtils.isEmpty(getIntent().getStringExtra("pushOrderID"))) {
            Log.e("pushOrderID", "" + getIntent().getStringExtra("pushOrderID"));
            pushOrderID = getIntent().getStringExtra("pushOrderID");
            activityMainBinding.tlMain.getTabAt(1).select();
            //loadOrdersFragment();
        } else {
            loadHomeFragment();
        }
    }

    private void setupToolBar() {
        if (AppPreferences.getInstance().getUserImage().length() > 0) {
            Glide.with(this).load(AppPreferences.getInstance().getUserImage()).into(activityMainBinding.civProfileMain);
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        unregisterReceiver(tokenReceiver);
    }

    @Override
    public boolean onMenuItemClick(MenuItem item) {
        switch (item.getItemId()) {
            case R.id.logout_item:
                if (AppUtilities.isOnline(MainActivity.this)) {
                    callLogoutApi();
                } else {
                    Toast.makeText(MainActivity.this, getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                }
                return true;
            default:
                return false;
        }
    }

    public class MainClickHandler {
        Context context;

        public MainClickHandler(Context context) {
            this.context = context;
        }

        public void onBackClicked(View view) {
            onBackPressed();
        }

        public void onProfileImageClicked(View view) {
            PopupMenu popup = new PopupMenu(MainActivity.this, activityMainBinding.civProfileMain);
            popup.setOnMenuItemClickListener(MainActivity.this);
            popup.inflate(R.menu.main_popup);
            Menu menuOpts = popup.getMenu();
            //menuOpts.getItem(0).setTitle(AppPreferences.getInstance().getUserName());
            //menuOpts.getItem(0).setVisible(false);
            menuOpts.getItem(0).setTitle(getResources().getString(R.string.txtLogout));
            popup.show();
        }

        public void onNotifyClicked(View view) {
            //loadOrdersFragment("pending");
            if (mFragment instanceof OrdersFragment && activityMainBinding.llNotifyCount.getVisibility() == View.VISIBLE) {
                ((OrdersFragment) mFragment).initOrderData();
                activityMainBinding.llNotifyCount.setVisibility(View.INVISIBLE);
            }
        }
    }

    private void loadHomeFragment() {
        if (homeFragment == null)
            homeFragment = new HomeFragment();
        mFragment = homeFragment;
        loadFragment(HOME, false, mFragment, false);
        activityMainBinding.rlNotifyOrder.setVisibility(View.GONE);
    }

    public void setOrderStatus(String order_status) {
        this.order_status = order_status;
    }

    public void loadOrdersFragment(String order_status) {
        if (ordersFragment == null)
            ordersFragment = new OrdersFragment();
        mFragment = ordersFragment;
        Bundle bundle = new Bundle();
        bundle.putString("pushOrderID", pushOrderID);
        bundle.putString("order_status", order_status);
        mFragment.setArguments(bundle);
        loadFragment(ORDER, false, mFragment, false);
        if (!order_status.equalsIgnoreCase("shipped")&&!order_status.equalsIgnoreCase("cancelled")) {
            activityMainBinding.rlNotifyOrder.setVisibility(View.VISIBLE);
        } else {
            activityMainBinding.rlNotifyOrder.setVisibility(View.GONE);
        }
    }

    private void loadStockFragment() {
        if (stockFragment == null)
            stockFragment = new StockFragment();
        mFragment = stockFragment;
        loadFragment(STOCK, false, mFragment, false);
        activityMainBinding.rlNotifyOrder.setVisibility(View.GONE);
    }

    private void loadReturnFragment() {
        if (returnFragment == null)
            returnFragment = new ReturnFragment();
        mFragment = returnFragment;
        loadFragment(RETURN, false, mFragment, false);
        activityMainBinding.rlNotifyOrder.setVisibility(View.GONE);
    }


    public void loadFragment(String tag, boolean addToStack, Fragment setFragment, boolean applyAnimation) {
        mFragmentTransaction = mFragmentManager.beginTransaction();
        mFragment = setFragment;
        if (addToStack) {
            if (applyAnimation) {
                //mFragmentTransaction.setCustomAnimations(R.anim.recycler_slide_right, 0);
                //mFragmentTransaction.setCustomAnimations(R.anim.activity_open_translate, R.anim.activity_close_translate);
            }
            mFragmentTransaction.add(R.id.frameContainer, mFragment, tag);
            mFragmentTransaction.addToBackStack(tag).commit();
        } else {
            if (applyAnimation) {
                //mFragmentTransaction.setCustomAnimations(R.anim.recycler_slide_right, 0);
                //mFragmentTransaction.setCustomAnimations(R.anim.activity_open_translate, R.anim.activity_close_translate);
            }
            mFragmentTransaction.replace(R.id.frameContainer, mFragment, tag);
            mFragmentTransaction.commitAllowingStateLoss();
        }
    }

    private void setTabView() {
        activityMainBinding.tlMain.addOnTabSelectedListener(new TabLayout.OnTabSelectedListener() {
            @Override
            public void onTabSelected(TabLayout.Tab tab) {
                switch (tab.getPosition()) {
                    case 0:
                        loadHomeFragment();
                        break;
                    case 1:
                        loadOrdersFragment("");
                        break;
                    case 2:
                        loadStockFragment();
                        break;
                    case 3:
                        loadReturnFragment();
                        break;
                }
            }

            @Override
            public void onTabUnselected(TabLayout.Tab tab) {

            }

            @Override
            public void onTabReselected(TabLayout.Tab tab) {

            }
        });
    }

    public class TokenReceiver extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            //Toast.makeText(MainActivity.this,intent.getStringExtra("token"),Toast.LENGTH_LONG).show();
            sendTokenToServer(intent.getStringExtra("token"));
        }
    }

    private void sendTokenToServer(String token) {
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("os_version", Build.VERSION.SDK_INT);
        logReq.put("device_token", token);
        logReq.put("version", AppUtilities.getAppVersion(MainActivity.this));
        logReq.put("device_type", "a");
        //logReq.put("device_id", AppPreferences.getInstance().getDeviceId());

        Call<GeneralResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerUpdateDeviceDetails(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq, AppPreferences.getInstance().getDeviceId());
        response1.enqueue(new Callback<GeneralResponse>() {
            @Override
            public void onResponse(Call<GeneralResponse> call, Response<GeneralResponse> response) {
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            //Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                        } else {
                            //Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<GeneralResponse> call, Throwable t) {

            }
        });
    }

    private void callLogoutApi() {
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("device_id", AppPreferences.getInstance().getDeviceId());
        logReq.put("ip_address", "");

        Call<GeneralResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerLogout(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<GeneralResponse>() {
            @Override
            public void onResponse(Call<GeneralResponse> call, Response<GeneralResponse> response) {
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(MainActivity.this, response.body().getMessage(), Toast.LENGTH_SHORT).show();
                        } else {
                            Toast.makeText(MainActivity.this, response.body().getMessage(), Toast.LENGTH_SHORT).show();
                            performLogout();
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<GeneralResponse> call, Throwable t) {

            }
        });
    }

    public void updateOrderCount(String count) {
        if (Integer.parseInt(count) > 0) {
            activityMainBinding.tvNotifyCount.setText(count);
            activityMainBinding.llNotifyCount.setVisibility(View.VISIBLE);
        } else {
            activityMainBinding.tvNotifyCount.setText("");
            activityMainBinding.llNotifyCount.setVisibility(View.INVISIBLE);
        }

    }
}
