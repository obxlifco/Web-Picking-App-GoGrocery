package com.gogrocery.Adapters;

import android.content.Context;
import android.graphics.drawable.Drawable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.ToggleButton;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.recyclerview.widget.RecyclerView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.DataSource;
import com.bumptech.glide.load.engine.GlideException;
import com.bumptech.glide.request.RequestListener;
import com.bumptech.glide.request.target.Target;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Interfaces.StoreTypeItemClickListner;
import com.gogrocery.Models.StoreTypeModel.DataItem;
import com.gogrocery.R;
import com.gogrocery.ViewModel.StoreCategoryModel;
import com.makeramen.roundedimageview.RoundedImageView;

import java.util.List;


public class StoreTypeOldStyleAdapter extends RecyclerView.Adapter<StoreTypeOldStyleAdapter.MyViewHolder> {


    private Context mContext;
    private StoreTypeItemClickListner storeTypeItemClickListner;
    List<DataItem> data;

    public StoreTypeOldStyleAdapter(Context mContext,
                                    List<DataItem> data, StoreTypeItemClickListner storeTypeItemClickListner) {

        this.mContext = mContext;
        this.data = data;
        this.storeTypeItemClickListner = storeTypeItemClickListner;
    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.store_type_row_old, parent, false);
        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {

        holder.tvWarehouseTitle.setText(data.get(position).getName());
        if (data.get(position).getHas_store() == 1) {
            holder.tvAvailable.setVisibility(View.GONE);
        } else {
            holder.tvAvailable.setVisibility(View.VISIBLE);
        }
        holder.itemView.setOnClickListener(v -> {

            storeTypeItemClickListner.clickStoreTypeItemClickListner(data.get(position).getId(), data.get(position).getName(), position);

        });

        try {

            Glide.with(mContext)
                    .load(Constants.STORE_TYPE_LOGO + data.get(position).getImage())
                    .listener(new RequestListener<Drawable>() {
                        @Override
                        public boolean onLoadFailed(@Nullable GlideException e, Object model, Target<Drawable> target, boolean isFirstResource) {
                            new android.os.Handler().postDelayed(new Runnable() {
                                @Override
                                public void run() {
                                    Glide.with(mContext)
                                            .load(R.drawable.image_not_available)
                                            //.apply(new RequestOptions().override(200, 200))
                                        //    .diskCacheStrategy(DiskCacheStrategy.NONE).skipMemoryCache(true)
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
                  //  .diskCacheStrategy(DiskCacheStrategy.NONE).skipMemoryCache(true)
                    .into(holder.ivWarehouse);
        } catch (Exception e) {
            System.out.println("Rahul : GlideExceptiion : " + e.getMessage());
            Glide.with(mContext)
                    .load(R.drawable.image_not_available)
                  //  .diskCacheStrategy(DiskCacheStrategy.NONE).skipMemoryCache(true)
                    .into(holder.ivWarehouse);
        }
        holder.tvWarehouseTitle.setText(data.get(position).getName());
        holder.itemView.setOnClickListener(v -> {
            storeTypeItemClickListner.clickStoreTypeItemClickListner(data.get(position).getId(), data.get(position).getName(), position);

        });
      //  holder.tbType.setChecked(data.get(position).isSelect());
    }


    @Override
    public int getItemCount() {
        return data.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {
             private RoundedImageView ivWarehouse;
              private TextView tvWarehouseTitle, tvAvailable;

              public MyViewHolder(View view) {
                  super(view);
                  ivWarehouse = view.findViewById(R.id.ivWarehouse);
                  tvWarehouseTitle = view.findViewById(R.id.tvWarehouseTitle);
                  tvAvailable = view.findViewById(R.id.tvAvailable);


              }

          }
   /*     private TextView tvWarehouseTitle;
        ToggleButton tbType;

        public MyViewHolder(View view) {
            super(view);
            tvWarehouseTitle = view.findViewById(R.id.tvWarehouseTitle);
            tbType = view.findViewById(R.id.tbType);
            tbType.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (data.get(getAdapterPosition()).isSelect()) {
                        setCheckedChange(false, getAdapterPosition());
                    } else {
                        setCheckedChange(true, getAdapterPosition());
                    }
                }
            });

        }
    }

    private void setCheckedChange(boolean isChecked, int pos) {
        if (pos > 0) {
            data.get(pos).setSelect(isChecked);
            data.get(0).setSelect(allCheckedCheck());
        } else {
            for (int i = 0; i < data.size(); i++) {
                data.get(i).setSelect(isChecked);
            }
        }
        notifyDataSetChanged();
    }

    private boolean allCheckedCheck() {
        int chkCount = 0, nonChkCount = 0;
        for (int i = 1; i < data.size(); i++) {
            if (data.get(i).isSelect()) {
                chkCount++;
            } else {
                nonChkCount++;
            }
        }
        if (chkCount == data.size() - 1) {
            return true;
        } else {
            return false;
        }

    }*/
}



