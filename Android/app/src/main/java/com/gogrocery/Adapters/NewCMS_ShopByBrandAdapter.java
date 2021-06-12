package com.gogrocery.Adapters;

import android.content.Context;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.engine.DiskCacheStrategy;
import com.bumptech.glide.request.RequestOptions;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Interfaces.ActivityRedirection;
import com.gogrocery.Models.CMS_NEW_Model.ShopByBrand;
import com.gogrocery.R;
import com.makeramen.roundedimageview.RoundedImageView;

import java.util.List;


public class NewCMS_ShopByBrandAdapter extends RecyclerView.Adapter<NewCMS_ShopByBrandAdapter.MyViewHolder> {


    private Context mContext;
    private List<ShopByBrand> mShopByBrandList;
    private ActivityRedirection mActivityRedirectionListner;


    public NewCMS_ShopByBrandAdapter(Context mContext,
                                     List<ShopByBrand> mShopByBrandList, ActivityRedirection mActivityRedirectionListner) {

        this.mContext = mContext;
        this.mShopByBrandList = mShopByBrandList;
        this.mActivityRedirectionListner = mActivityRedirectionListner;
        System.out.println("Rahul : ShopByBrand : mShopByBrandList : " + mShopByBrandList.size());

    }

    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.shop_by_brand_row, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        ShopByBrand mSopShopByBrandInner = mShopByBrandList.get(position);


        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                mActivityRedirectionListner.redirect("shop_by_brand",mSopShopByBrandInner.getSlug()+"#GoGrocery#"+mSopShopByBrandInner.getName());
            }
        });

        System.out.println("Rahul : NewCMS_ShopByBrandAdapter : getBrandLogo : "+Constants.IMAGE_URL_BRAND+mSopShopByBrandInner.getBrandLogo());

        Glide.with(mContext)
                .load(Constants.IMAGE_URL_BRAND+mSopShopByBrandInner.getBrandLogo())
                .apply(new RequestOptions().override(160, 84))
                .diskCacheStrategy(DiskCacheStrategy.NONE) .skipMemoryCache(true)
                .into(holder.ivShopByBrand);



    }


    @Override
    public int getItemCount() {
        return mShopByBrandList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {

        private RoundedImageView ivShopByBrand;


        public MyViewHolder(View view) {
            super(view);


            ivShopByBrand = view.findViewById(R.id.ivShopByBrand);



        }

    }


}
