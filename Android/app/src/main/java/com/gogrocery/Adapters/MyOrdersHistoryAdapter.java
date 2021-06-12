package com.gogrocery.Adapters;

import android.content.Context;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;

import com.gogrocery.Constants.Constants;
import com.gogrocery.Interfaces.PaymentPageRedirectionInterface;
import com.gogrocery.R;
import com.google.gson.Gson;

import java.text.ParseException;
import java.util.List;


public class MyOrdersHistoryAdapter extends RecyclerView.Adapter<MyOrdersHistoryAdapter.MyViewHolder> {


    private Context mContext;
    private int isVisible=-1;
    private List<com.gogrocery.Models.MyOrdersHistoryModel.Data> mMyOrdersHistoryList;
    private PaymentPageRedirectionInterface mPaymentPageRedirectionInterface;


    public MyOrdersHistoryAdapter(Context mContext,
                                  List<com.gogrocery.Models.MyOrdersHistoryModel.Data> mMyOrdersHistoryList, PaymentPageRedirectionInterface mPaymentPageRedirectionInterface) {

        this.mContext = mContext;
        this.mMyOrdersHistoryList = mMyOrdersHistoryList;
        this.mPaymentPageRedirectionInterface = mPaymentPageRedirectionInterface;
        System.out.println("Rahul : MyOrdersHistoryAdapter : mMyOrdersHistoryList : " + mMyOrdersHistoryList.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.my_orders_history_row, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        com.gogrocery.Models.MyOrdersHistoryModel.Data mDataInner = mMyOrdersHistoryList.get(position);

        try {

            holder.tvOrderNumber.setText(" "+mDataInner.getCustomOrderId());
            holder.tvStoreName.setText(mDataInner.getWarehouseName());
            holder.tvAddress.setText(mDataInner.getDeliveryStreetAddress() + "\n" +mDataInner.getDeliveryCountryName() + mDataInner.getDeliveryState());
            holder.tvBillAmount.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " +Constants.twoDecimalRoundOff(Double.parseDouble(mDataInner.getGrossAmount())));
        }catch (Exception e){
            e.printStackTrace();
        }


        if (mDataInner.getPaymentMethodName().isEmpty()) {
            holder.tvPaymentMode.setVisibility(View.GONE);
            holder.txtPaymentmode.setVisibility(View.GONE);
        } else {
            holder.tvPaymentMode.setText(mDataInner.getPaymentMethodName());
        }

        //  holder.tvpaymentStatus.setText(mDataInner.getstat);
        String am_pm = "";
        if (Integer.parseInt(mDataInner.getCreated().split("T")[1].split(":")[0]) >= 12) {
            am_pm = "PM";
        } else {
            am_pm = "AM";
        }

        holder.tvDateNTime.setText(mDataInner.getCreated().split("T")[0].split("-")[2] + " " +
                Constants.getSeperateValuesFromDate(mDataInner.getCreated().split("T")[0], 3) + " " +
                mDataInner.getCreated().split("T")[0].split("-")[0] + " , " + mDataInner.getCreated().split("T")[1].split(":")[0] + ":" + mDataInner.getCreated().split("T")[1].split(":")[1] + " " + am_pm
        );
        /*try {
            holder.tvDateNTime.setText(mDataInner.getCreated().split("T")[0].split("-")[2] + " " +
                    Constants.getSeperateValuesFromDate(mDataInner.getCreated().split("T")[0], 3) + " " +
                    mDataInner.getCreated().split("T")[0].split("-")[0] + " , " + Constants.convertUTCToTimeFormatWithAM(mDataInner.getCreated())
            );
        } catch (ParseException e) {
            e.printStackTrace();
        }*/

        holder.tvPaymentStatus.setText(mDataInner.getStrPaymentStatus());


        switch (mDataInner.getStrPaymentStatus()) {
            case "Unpaid":
                // holder.tvPaymentStatus.setBackground(mContext.getResources().getDrawable(R.drawable.my_order_payment_status_unpaid_bg));
                holder.tvPaymentStatus.setTextColor(mContext.getResources().getColor(R.color.my_orders_row_color_unpaid));
                break;
            case "Successful":
                holder.tvPaymentStatus.setTextColor(mContext.getResources().getColor(R.color.my_orders_row_color_successfull));
                //holder.tvPaymentStatus.setBackground(mContext.getResources().getDrawable(R.drawable.my_order_payment_status_successfull_bg));
                break;
            case "Failed":
                // holder.tvPaymentStatus.setBackground(mContext.getResources().getDrawable(R.drawable.my_order_payment_status_failed_bg));
                holder.tvPaymentStatus.setTextColor(mContext.getResources().getColor(R.color.my_orders_row_color_failed));
                break;

        }

        switch (mDataInner.getStrOrderStatus()) {
            case "Approved":
                holder.tvOrderStatus.setTextColor(mContext.getResources().getColor(R.color.my_orders_row_color_green));
                break;
            case "Cancelled":
                holder.tvOrderStatus.setTextColor(mContext.getResources().getColor(R.color.my_orders_row_color_red));
                break;

        }
        if (mDataInner.getStrOrderStatus() != null) {
            if (!mDataInner.getStrOrderStatus().isEmpty()) {
                holder.tvOrderStatus.setText(mDataInner.getStrOrderStatus());
            }

        }
        try {
            holder.tvOrderTime.setText(Constants.getFormattedDate(Constants.getMonthFormatDate(mDataInner.getTimeSlotDate()))+" "+mDataInner.getSlotEndTime());
        } catch (ParseException e) {
            e.printStackTrace();
        }

        switch (mDataInner.getShipment_status()) {
            case "Invoicing":
                // holder.tvPaymentStatus.setTextColor(mContext.getResources().getColor(R.color.my_orders_row_color_unpaid));
                holder.tvPayNow.setVisibility(View.VISIBLE);
                break;
        }


        switch (mDataInner.getShipment_status()) {
            case "Invoicing":
                holder.tvCancel.setVisibility(View.VISIBLE);
                break;
            case "Pending":
                holder.tvCancel.setVisibility(View.VISIBLE);
                break;
            case "Picking":
                holder.tvCancel.setVisibility(View.VISIBLE);
                break;
            case "":
                // holder.tvCancel.setVisibility(View.VISIBLE);
                break;
        }

        if (isVisible == -1) {
            holder.rl_orderSummery.setVisibility(View.GONE);

            holder.ivToDetail.setBackgroundResource(R.drawable.action_down);


        } else {
            if (isVisible == position) {
                holder.rl_orderSummery.setVisibility(View.VISIBLE);

                holder.ivToDetail.setBackgroundResource(R.drawable.action_up);

            } else {
                holder.rl_orderSummery.setVisibility(View.GONE);

                holder.ivToDetail.setBackgroundResource(R.drawable.action_down);

            }
        }
        holder.ivToDetail.setOnClickListener(v->{



           // holder.rl_orderSummery.setTextColor(Color.parseColor("#FFFFFF"));
            if (isVisible !=position) {
                notifyItemChanged(isVisible);
                isVisible = position;
                holder.rl_orderSummery.setVisibility(View.VISIBLE);
                holder.ivToDetail.setBackgroundResource(R.drawable.action_up);
            }else {
              //  notifyItemChanged(isVisible);
                isVisible = -1;
                holder.rl_orderSummery.setVisibility(View.GONE);
                holder.ivToDetail.setBackgroundResource(R.drawable.action_down);
            }
        });

        holder.tvCancel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                mPaymentPageRedirectionInterface.requestForCancelOrder(mDataInner.getId(), position);
            }
        });

        holder.tvPayNow.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                mPaymentPageRedirectionInterface.redirect(mDataInner.getCustomOrderId(), new Gson().toJson(mDataInner));

            }
        });
        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mPaymentPageRedirectionInterface.redirectTODetailPage(mDataInner.getId(), mDataInner.getCustomOrderId(), new Gson().toJson(mDataInner));
            }
        });
    }


    @Override
    public int getItemCount() {
        return mMyOrdersHistoryList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {


        private TextView tvOrderNumber, tvDateNTime, tvBillAmount, tvPaymentMode, tvPaymentStatus, tvOrderStatus, tvPayNow, tvCancel, txtPaymentmode,tvOrderTime,tvStoreName,tvAddress;
private ImageView ivToDetail;
private RelativeLayout rl_orderSummery;

        public MyViewHolder(View view) {
            super(view);


            tvOrderNumber = view.findViewById(R.id.tvOrderNumber);
            tvDateNTime = view.findViewById(R.id.tvDateNTime);
            tvStoreName = view.findViewById(R.id.tvStoreName);
            ivToDetail = view.findViewById(R.id.ivToDetail);
            tvBillAmount = view.findViewById(R.id.tvTotalAmount);
            tvAddress = view.findViewById(R.id.tvAddress);
            rl_orderSummery = view.findViewById(R.id.rl_orderSummery);
            tvPaymentMode = view.findViewById(R.id.tvPaymentMode);
            tvPaymentStatus = view.findViewById(R.id.tvPaymentStatus);
            tvOrderStatus = view.findViewById(R.id.tvOrderStatus);
            tvPayNow = view.findViewById(R.id.tvPayNow);
            txtPaymentmode = view.findViewById(R.id.txtPaymentmode);
            tvCancel = view.findViewById(R.id.tvCancel);
            tvOrderTime = view.findViewById(R.id.tvOrderTime);

        }

    }


}
