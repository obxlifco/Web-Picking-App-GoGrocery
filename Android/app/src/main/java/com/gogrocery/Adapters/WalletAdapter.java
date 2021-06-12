package com.gogrocery.Adapters;

import android.content.Context;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.gogrocery.Interfaces.WarehouseItemClickListner;
import com.gogrocery.Models.WalletModel.WalletData;
import com.gogrocery.R;

import java.util.List;


public class WalletAdapter extends RecyclerView.Adapter<WalletAdapter.MyViewHolder> {


    private Context mContext;
    private List<WalletData> mWalletDataList;
    private WarehouseItemClickListner mWarehouseItemClickListner;

    public WalletAdapter(Context mContext,
                         List<WalletData> mWalletDataList) {

        this.mContext = mContext;
        this.mWalletDataList = mWalletDataList;
        System.out.println("Rahul : WalletAdapter : mWarehouseModelDataList : " + mWalletDataList.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.my_wallet_row_new, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {

        try {

            WalletData mDataInner = mWalletDataList.get(position);

            //holder.tvDate.setText(mDataInner.get());
          /*  if (mDataInner.getStatus().equals("earn")) {
                holder.tvStatus.setTextColor(mContext.getResources().getColor(R.color.earned_color));
                holder.tvStatus.setBackground(mContext.getResources().getDrawable(R.drawable.my_order_payment_status_unpaid_bg));
                holder.tvStatus.setText("Earned");

            } else {
                holder.tvStatus.setText("Redeem");
                holder.tvStatus.setTextColor(mContext.getResources().getColor(R.color.redeem_color));
                holder.tvStatus.setBackground(mContext.getResources().getDrawable(R.drawable.my_order_payment_status_failed_bg));
            }*/

            // holder.tvPoints.setText(mDataInner.getBurntPoints());
            holder.tvDate.setText(mDataInner.getCreated().split("T")[0].split("-")[2] + "/" + mDataInner.getCreated().split("T")[0].split("-")[1] + "/" + mDataInner.getCreated().split("T")[0].split("-")[0]);
            holder.tvEP.setText(mDataInner.getReceivedPoints());
            holder.tvUP.setText(mDataInner.getBurntPoints());
            holder.tvRP.setText(mDataInner.getRemainingBalance());

            holder.itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                }
            });
        } catch (Exception e) {
            System.out.println("Rahul : WalletAdapter : Exception : " + e);
        }

    }


    @Override
    public int getItemCount() {
        return mWalletDataList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {

        private TextView tvDate, tvEP, tvUP, tvRP;

        public MyViewHolder(View view) {
            super(view);


            tvDate = view.findViewById(R.id.tvDate);
            tvEP = view.findViewById(R.id.tvEP);
            tvUP = view.findViewById(R.id.tvUP);
            tvRP = view.findViewById(R.id.tvRP);

        }

    }


}
