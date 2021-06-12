package com.gogrocery.Adapters;

import android.content.Context;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import com.gogrocery.Interfaces.ActivityRedirection;
import com.gogrocery.Interfaces.SingleStringPassingInterface;
import com.gogrocery.R;

import java.util.List;


public class ShopByCategoryAdapter extends RecyclerView.Adapter<ShopByCategoryAdapter.MyViewHolder> {


    private Context mContext;
    private List<String> mShopByCategoryList;
    private ActivityRedirection mActivityRedirectionListner;
    private SingleStringPassingInterface mSingleStringPassingInterface;


    public ShopByCategoryAdapter(Context mContext,
                                 List<String> mShopByCategoryList,SingleStringPassingInterface mSingleStringPassingInterface) {

        this.mContext = mContext;
        this.mShopByCategoryList = mShopByCategoryList;
     this.mSingleStringPassingInterface=mSingleStringPassingInterface;
        System.out.println("Rahul : ShopByCategoryAdapter : mShopByCategoryList : " + mShopByCategoryList.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.search_page_category_row, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        String mShopByCategoryInner = mShopByCategoryList.get(position);

        holder.tvName.setText(mShopByCategoryInner);

        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                mSingleStringPassingInterface.passValue(holder.tvName.getText().toString());
            }
        });
    }


    @Override
    public int getItemCount() {
        return mShopByCategoryList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {

        private ImageView ivCategory;
        private TextView tvName;


        public MyViewHolder(View view) {
            super(view);



            tvName = view.findViewById(R.id.tvName);


        }

    }


}
