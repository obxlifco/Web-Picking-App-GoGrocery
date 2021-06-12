package com.gogrocery.picking.fragment;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.gogrocery.picking.R;
import com.gogrocery.picking.activity.BaseActivity;
import com.gogrocery.picking.activity.MainActivity;
import com.gogrocery.picking.network.APIClient;
import com.gogrocery.picking.network.APIInterface;
import com.gogrocery.picking.prefrences.AppPreferences;
import com.gogrocery.picking.response_pojo.dashboard_pojo.DashboardResponse;
import com.gogrocery.picking.utils.AppUtilities;

import java.util.HashMap;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class HomeFragment extends Fragment {
    TextView tvShippedOrder,tvTotalOrder,tvPendingOrder,tvProcessOrder,tvCancelOrder,tvSubsOutOrder,tvSubsInOrder;
    LinearLayout llMainTotalOrder;
    RelativeLayout rlMainShippedOrder,rlMainProcessingOrder,rlMainCancelOrder;
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        //return super.onCreateView(inflater, container, savedInstanceState);
        View view = inflater.inflate(R.layout.fragment_home, container, false);
        initView(view);
        return view;
    }

    private void initView(View view) {
        tvShippedOrder=view.findViewById(R.id.tvShippedOrder);
        tvTotalOrder=view.findViewById(R.id.tvTotalOrder);
        llMainTotalOrder=view.findViewById(R.id.llMainTotalOrder);
        rlMainShippedOrder=view.findViewById(R.id.rlMainShippedOrder);
        rlMainCancelOrder=view.findViewById(R.id.rlMainCancelOrder);
        rlMainProcessingOrder=view.findViewById(R.id.rlMainProcessingOrder);
        tvPendingOrder=view.findViewById(R.id.tvPendingOrder);
        tvProcessOrder=view.findViewById(R.id.tvProcessOrder);
        tvCancelOrder=view.findViewById(R.id.tvCancelOrder);
        tvSubsOutOrder=view.findViewById(R.id.tvSubsOutOrder);
        tvSubsInOrder=view.findViewById(R.id.tvSubsInOrder);
        if (AppUtilities.isOnline(getActivity())) {
            callDashboardAPI();
        } else {
            Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
        }
        llMainTotalOrder.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ((MainActivity)getActivity()).activityMainBinding.tlMain.getTabAt(1).select();
                ((MainActivity)getActivity()).loadOrdersFragment("");
            }
        });
        rlMainShippedOrder.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ((MainActivity)getActivity()).activityMainBinding.tlMain.getTabAt(1).select();
                ((MainActivity)getActivity()).loadOrdersFragment("shipped");
            }
        });
        rlMainCancelOrder.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ((MainActivity)getActivity()).activityMainBinding.tlMain.getTabAt(1).select();
                ((MainActivity)getActivity()).loadOrdersFragment("cancelled");
            }
        });
        rlMainProcessingOrder.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ((MainActivity)getActivity()).activityMainBinding.tlMain.getTabAt(1).select();
                ((MainActivity)getActivity()).loadOrdersFragment("processing");
            }
        });
    }

    private void callDashboardAPI() {
        ((BaseActivity)getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("warehouse_id", AppPreferences.getInstance().getWarehouseID());
        Call<DashboardResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerDashboard(
                "Token " + AppPreferences.getInstance().getUserToken(),logReq);
        response1.enqueue(new Callback<DashboardResponse>() {
            @Override
            public void onResponse(Call<DashboardResponse> call, Response<DashboardResponse> response) {

                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(getActivity(), response.body().getApiStatus(), Toast.LENGTH_SHORT).show();
                        } else {
                            tvTotalOrder.setText(response.body().getPending_processing_order()+"");
                            tvShippedOrder.setText(response.body().getShippedOrder()+"");
                            tvPendingOrder.setText(response.body().getPending_order()+"");
                            tvCancelOrder.setText(response.body().getCancel_order()+"");
                            tvSubsOutOrder.setText(response.body().getSubstitution_sent_order()+"");
                            tvSubsInOrder.setText(response.body().getSubstitution_received_order()+"");
                            tvProcessOrder.setText(response.body().getPending_processing_order()-response.body().getPending_order()+"");
                        }
                        ((MainActivity)getActivity()).hideProgressDialog();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }else {
                    ((MainActivity)getActivity()).hideProgressDialog();
                }
            }

            @Override

            public void onFailure(Call<DashboardResponse> call, Throwable t) {

            }
        });
    }
}
