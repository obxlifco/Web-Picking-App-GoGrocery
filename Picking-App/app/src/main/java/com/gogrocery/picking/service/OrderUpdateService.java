package com.gogrocery.picking.service;

import android.app.Service;
import android.content.Intent;
import android.os.Handler;
import android.os.IBinder;

import com.gogrocery.picking.GoGroceryPicking;
import com.gogrocery.picking.network.APIClient;
import com.gogrocery.picking.network.APIInterface;
import com.gogrocery.picking.prefrences.AppPreferences;
import com.gogrocery.picking.response_pojo.latest_order_pojo.LatestOrderResponse;
import com.gogrocery.picking.utils.AppUtilities;

import java.util.HashMap;
import java.util.Timer;
import java.util.TimerTask;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;


public class OrderUpdateService extends Service {
    //public static final int notify = 300000;  //interval between two services(Here Service run every 5 Minute)
    public static final int notify = 15000;
    private Handler mHandler = new Handler();   //run on another Thread to avoid crash
    private Timer mTimer = null;    //timer handling

    @Override
    public IBinder onBind(Intent intent) {
        throw new UnsupportedOperationException("Not yet implemented");
    }

    @Override
    public void onCreate() {
        if (mTimer != null) // Cancel if already existed
            mTimer.cancel();
        else
            mTimer = new Timer();   //recreate new
        mTimer.scheduleAtFixedRate(new TimeDisplay(), 0, notify);   //Schedule task
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        mTimer.cancel();    //For Cancel Timer
        //Toast.makeText(this, "Service is Destroyed", Toast.LENGTH_SHORT).show();
    }

    //class TimeDisplay for handling task
    class TimeDisplay extends TimerTask {
        @Override
        public void run() {
            if (AppUtilities.isOnline(getApplicationContext())) {
                callLatestOrderApi();
            }
        }
    }

    private void callLatestOrderApi() {
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("order_id",AppPreferences.getInstance().getLatestOrderID() );
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("warehouse_id", AppPreferences.getInstance().getWarehouseID());
        logReq.put("order_id_for_substitute_checking", AppPreferences.getInstance().getViewOrderID());

        Call<LatestOrderResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerLatestOrder(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<LatestOrderResponse>() {
            @Override
            public void onResponse(Call<LatestOrderResponse> call, Response<LatestOrderResponse> response) {
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                        } else {
                            Intent i=new Intent("com.gogrocery.picking.receiver.ORDER_UPDATE");
                            i.putExtra("newOrderCount",String.valueOf(response.body().getResponse().getNoOfLatestOrder()));
                            i.putExtra("substitute_in",String.valueOf(response.body().getResponse().getSubstitute_in()));
                            i.putExtra("substitute_out",String.valueOf(response.body().getResponse().getSubstitute_out()));
                            GoGroceryPicking.applicationContext.sendBroadcast(i);
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<LatestOrderResponse> call, Throwable t) {

            }
        });
    }
}
