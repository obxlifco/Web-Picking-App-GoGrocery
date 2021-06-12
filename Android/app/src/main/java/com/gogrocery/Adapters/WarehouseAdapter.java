package com.gogrocery.Adapters;

import android.app.Activity;
import android.content.Context;
import android.content.DialogInterface;
import android.graphics.drawable.Drawable;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.core.content.ContextCompat;
import androidx.recyclerview.widget.RecyclerView;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import com.afollestad.materialdialogs.MaterialDialog;
import com.bumptech.glide.Glide;
import com.bumptech.glide.load.DataSource;
import com.bumptech.glide.load.engine.DiskCacheStrategy;
import com.bumptech.glide.load.engine.GlideException;
import com.bumptech.glide.request.RequestListener;
import com.bumptech.glide.request.RequestOptions;
import com.bumptech.glide.request.target.Target;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Interfaces.WarehouseItemClickListner;
import com.gogrocery.R;
import com.makeramen.roundedimageview.RoundedImageView;

import org.json.JSONException;

import java.util.List;


public class WarehouseAdapter extends RecyclerView.Adapter<WarehouseAdapter.MyViewHolder> {


    private Activity mContext;
    private List<com.gogrocery.Models.WarehouseModel.Data> mWarehouseModelDataList;
    private WarehouseItemClickListner mWarehouseItemClickListner;
    private SharedPreferenceManager mSharedPreferenceManager;
    public WarehouseAdapter(Activity mContext,
                            List<com.gogrocery.Models.WarehouseModel.Data> mWarehouseModelDataList, WarehouseItemClickListner mWarehouseItemClickListner) {

        this.mContext = mContext;
        this.mWarehouseModelDataList = mWarehouseModelDataList;
        this.mWarehouseItemClickListner = mWarehouseItemClickListner;
        mSharedPreferenceManager = new SharedPreferenceManager(mContext);
        System.out.println("Rahul : WarehouseAdapter : mWarehouseModelDataList : " + mWarehouseModelDataList.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.warehouse_row, parent, false);
        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        com.gogrocery.Models.WarehouseModel.Data mDataInner = mWarehouseModelDataList.get(position);
        holder.tvWarehouseTitle.setText(mDataInner.getName());
        holder.itemView.setOnClickListener(v->{
            if(mDataInner.getStoreOpen()||mDataInner.getNextday()) {
                if (mDataInner.getCurrency().getCurrencyName() != null && mDataInner.getCurrency().getCurrencyName().isEmpty()) {
                    //  Constants.VARIABLES.CURRENT_CURRENCY = mDataInner.getCurrency().getCurrencyName();
                    mSharedPreferenceManager.saveCurrency(mDataInner.getCurrency().getCurrencyName());
                } else {
                    Constants.VARIABLES.CURRENT_CURRENCY = "AED";
                    mSharedPreferenceManager.saveCurrency("AED");
                }
                mWarehouseItemClickListner.clickWarehouseItemClickListner(Double.parseDouble(mDataInner.getLatitude()), Double.parseDouble(mDataInner.getLongitude()), String.valueOf(mDataInner.getId()), mDataInner.getName());
            }

            else {

                new MaterialDialog.Builder(mContext)
                        .title("Closed Store")
                        .content("Sorry, the store is currently closed")
                        .positiveText("Okay")
                        .positiveColor(ContextCompat.getColor(mContext, R.color.app_red_clr))

                        .onPositive((dialog, which) -> {

dialog.dismiss();

                        })
                       .show();

            }

        });

        try {

            String imageUrl =Constants.WAREHOUSE_LOGO + mDataInner.getWarehouse_logo();


            String imagePath =imageUrl.replaceAll(" ", "%20");

            Glide.with(mContext)
                    .load(imagePath)
                    .listener(new RequestListener<Drawable>() {
                        @Override
                        public boolean onLoadFailed(@Nullable GlideException e, Object model, Target<Drawable> target, boolean isFirstResource) {
                            new android.os.Handler().postDelayed(new Runnable() {
                                @Override
                                public void run() {
                                    Glide.with(mContext)
                                            .load(R.drawable.image_not_available)
                                          //  .apply(new RequestOptions().override(300, 300))
                                         //   .diskCacheStrategy(DiskCacheStrategy.NONE) .skipMemoryCache(true)
                                            .into(holder.ivWarehouse);
                                }
                            }, 10);


                            return false;
                        }

                        @Override
                        public boolean onResourceReady(Drawable resource, Object model, Target<Drawable> target, DataSource dataSource, boolean isFirstResource) {
                            return false;
                        }


                    })
                  //  .diskCacheStrategy(DiskCacheStrategy.NONE) .skipMemoryCache(true)
                    .into(holder.ivWarehouse);
        } catch (Exception e) {
            System.out.println("Rahul : GlideExceptiion : " + e.getMessage());
            Glide.with(mContext)
                    .load(R.drawable.image_not_available)
                  //  .diskCacheStrategy(DiskCacheStrategy.NONE) .skipMemoryCache(true)
                    .into(holder.ivWarehouse);
        }


        try {

if(mDataInner.getStoreOpen()){

if(mDataInner.getOpenTime().equals(mDataInner.getCloseTime())){


    if(mDataInner.getStoreTimeDisplay()) {
        holder.tvWarehouseTime.setVisibility(View.VISIBLE);
        holder.tvWarehouseTime.setText("24/7 ");
        holder.tvWarehouseStatus.setText("Open");
        holder.ivOpenCloseStatus.setImageDrawable(mContext.getResources().getDrawable(R.drawable.bg_green_circle));
    }else {
        holder.tvWarehouseStatus.setText("Closed");
        holder.ivOpenCloseStatus.setImageDrawable(mContext.getResources().getDrawable(R.drawable.bg_green_red));
        holder.tvWarehouseTime.setVisibility(View.GONE);
    }
}else {

    holder.tvWarehouseStatus.setText("Open");
    holder.ivOpenCloseStatus.setImageDrawable(mContext.getResources().getDrawable(R.drawable.bg_green_circle));
    if(mDataInner.getStoreTimeDisplay()) {
        holder.tvWarehouseTime.setVisibility(View.VISIBLE);
        holder.tvWarehouseTime.setText(mDataInner.getOpenTime()+" to "+mDataInner.getCloseTime());
    }else {
        holder.tvWarehouseTime.setVisibility(View.GONE);
    }
}


}else {
    if(mDataInner.getNextday()){

        holder.tvWarehouseStatus.setText("Next Day Delivery");
        holder.ivOpenCloseStatus.setImageDrawable(mContext.getResources().getDrawable(R.drawable.bg_green_blue));
        if(mDataInner.getStoreTimeDisplay()) {
            holder.tvWarehouseTime.setVisibility(View.VISIBLE);
            holder.tvWarehouseTime.setText(mDataInner.getOpenTime()+" to "+mDataInner.getCloseTime());
        }else {
            holder.tvWarehouseTime.setVisibility(View.GONE);
        }
    }else {

        holder.tvWarehouseStatus.setText("Closed");
        holder.ivOpenCloseStatus.setImageDrawable(mContext.getResources().getDrawable(R.drawable.bg_green_red));
        if(mDataInner.getStoreTimeDisplay()) {
            holder.tvWarehouseTime.setVisibility(View.VISIBLE);
            holder.tvWarehouseTime.setText(mDataInner.getOpenTime()+" to "+mDataInner.getCloseTime());
        }else {
            holder.tvWarehouseTime.setVisibility(View.GONE);
        }
    }

}
        }catch (Exception e){
            e.printStackTrace();
        }






    }


    @Override
    public int getItemCount() {
        return mWarehouseModelDataList.size();
    }


    public static class MyViewHolder extends RecyclerView.ViewHolder {

        private RoundedImageView ivWarehouse;
        private TextView tvWarehouseTitle;
        private TextView tvWarehouseStatus;
        private TextView tvWarehouseTime;
        private ImageView ivOpenCloseStatus;


        public MyViewHolder(View view) {
            super(view);


            ivWarehouse = view.findViewById(R.id.ivWarehouse);
            ivOpenCloseStatus = view.findViewById(R.id.ivOpenCloseStatus);
            tvWarehouseTitle = view.findViewById(R.id.tvWarehouseTitle);
            tvWarehouseStatus = view.findViewById(R.id.tvWarehouseStatus);
            tvWarehouseTime = view.findViewById(R.id.tvWarehouseTime);


        }

    }


}
