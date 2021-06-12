package com.gogrocery.Adapters;

import android.content.Context;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.engine.DiskCacheStrategy;
import com.bumptech.glide.request.RequestOptions;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Interfaces.ActivityRedirection;
import com.gogrocery.Models.CMS_NEW_Model.PromotionalBanner;
import com.gogrocery.R;

import java.util.List;


public class NewCMS_PromotionBannerAdapter extends RecyclerView.Adapter<NewCMS_PromotionBannerAdapter.MyViewHolder> {


    private Context mContext;
    private List<PromotionalBanner> mPromotionalBannerList;
    private ActivityRedirection mActivityRedirectionListner;
    private LinearLayout.LayoutParams params;


    public NewCMS_PromotionBannerAdapter(Context mContext,
                                         List<PromotionalBanner> mPromotionalBannerList, ActivityRedirection mActivityRedirectionListner) {

        this.mContext = mContext;
        this.mPromotionalBannerList = mPromotionalBannerList;
        this.mActivityRedirectionListner = mActivityRedirectionListner;
        System.out.println("Rahul : NewCMS_PromotionBannerAdapter : mPromotionalBannerList : " + mPromotionalBannerList.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.promotional_banner_row_layout, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        try {
            PromotionalBanner mPromotionalBannerInner = mPromotionalBannerList.get(position);
            params = new LinearLayout.LayoutParams(0, 0);


            holder.itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    // mActivityRedirectionListner.redirect("sbc",mMenuBarInner.getName());
                    mActivityRedirectionListner.redirect("promotional_banner", "");

                }
            });

            holder.tvBannerTitile.setText(mPromotionalBannerInner.getBannerName());
            holder.tvNumberOfProducts.setText("" + mPromotionalBannerInner.getProductCount() + " Products");
            Glide.with(mContext)
                    .load(Constants.IMAGE_URL_CATEGOERY_BANNER + mPromotionalBannerInner.getBannerImage().getPrimaryImageName())
                    .apply(new RequestOptions().override(400, 130))
                    .diskCacheStrategy(DiskCacheStrategy.NONE) .skipMemoryCache(true)
                    .into(holder.ivCategoryBanner);

            System.out.println("Rahul : NewCMS_PromotionBannerAdapter : getProductCount : " + mPromotionalBannerInner.getProductCount());

            if (mPromotionalBannerInner.getProductCount()==0) {
                holder.itemView.setLayoutParams(params);
            }
        }catch (Exception e){e.printStackTrace();}

    }


    @Override
    public int getItemCount() {
        return mPromotionalBannerList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {

        private ImageView ivCategoryBanner;
        private TextView tvBannerTitile, tvNumberOfProducts;

        public MyViewHolder(View view) {
            super(view);


            ivCategoryBanner = view.findViewById(R.id.ivCategoryBanner);
            tvBannerTitile = view.findViewById(R.id.tvBannerTitile);
            tvNumberOfProducts = view.findViewById(R.id.tvNumberOfProducts);


        }

    }


}
