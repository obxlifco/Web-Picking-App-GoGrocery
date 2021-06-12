package com.gogrocery.Adapters;

import android.app.Activity;
import android.content.Context;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import android.util.DisplayMetrics;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.engine.DiskCacheStrategy;
import com.bumptech.glide.request.RequestOptions;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Interfaces.ActivityRedirection;
import com.gogrocery.Models.CMS_NEW_Model.CategoryBanner;
import com.gogrocery.R;
import com.makeramen.roundedimageview.RoundedImageView;

import java.util.List;


public class NewCMS_CategoryBannerAdapter extends RecyclerView.Adapter<NewCMS_CategoryBannerAdapter.MyViewHolder> {


    private Activity mContext;
    private List<CategoryBanner> mCategoryBannerList;
    private ActivityRedirection mActivityRedirectionListner;

    private LinearLayout.LayoutParams params;

    public NewCMS_CategoryBannerAdapter(Activity mContext,
                                        List<CategoryBanner> mCategoryBannerList, ActivityRedirection mActivityRedirectionListner) {

        this.mContext = mContext;
        this.mCategoryBannerList = mCategoryBannerList;
        this.mActivityRedirectionListner = mActivityRedirectionListner;
        System.out.println("Rahul : NewCMS_CategoryBannerAdapter : mCategoryBannerList : " + mCategoryBannerList.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.category_banner_row, parent, false);
        params = new LinearLayout.LayoutParams(0, 0);

        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        try {
            CategoryBanner mCategoryBannerInner = mCategoryBannerList.get(position);


            holder.itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    // mActivityRedirectionListner.redirect("sbc",mMenuBarInner.getName());
                    if (!mCategoryBannerInner.getCategory_name().isEmpty() && mCategoryBannerInner.getCategory_name()!=null&&!mCategoryBannerInner.getLink().isEmpty()&&mCategoryBannerInner.getLink()!=null) {
//                        mActivityRedirectionListner.redirect("category_banner", mCategoryBannerInner.getLink().split("/")[1] + "#GoGrocery#" + mCategoryBannerInner.getLink().split("/")[1].toUpperCase());
//
//                    } else {
                        mActivityRedirectionListner.redirect("category_banner", mCategoryBannerInner.getLink().split("/")[1] + "#GoGrocery#" + mCategoryBannerInner.getCategory_name());
                    }
                }
            });

            Glide.with(mContext)
                    .load(Constants.IMAGE_URL_CATEGOERY_BANNER + mCategoryBannerInner.getPrimaryImageName())
                   /* .apply(new RequestOptions().override(340, 114))*/
                    .diskCacheStrategy(DiskCacheStrategy.NONE) .skipMemoryCache(true)
                    .into(holder.ivCategoryBanner);
        }catch (Exception e){e.printStackTrace();}


    }


    @Override
    public int getItemCount() {
        return mCategoryBannerList.size();
    }


    public static class MyViewHolder extends RecyclerView.ViewHolder {

        private RoundedImageView ivCategoryBanner;


        public MyViewHolder(View view) {
            super(view);


            ivCategoryBanner = view.findViewById(R.id.ivCategoryBanner);


        }

    }


}
