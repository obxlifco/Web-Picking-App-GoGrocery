package com.gogrocery.Adapters;

import android.content.Context;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.gogrocery.Interfaces.ActivityRedirection;
import com.gogrocery.R;
import com.google.gson.Gson;

import java.util.List;


public class SideMenuCategoryAdapter extends RecyclerView.Adapter<SideMenuCategoryAdapter.MyViewHolder> {


    private Context mContext;
    private List<com.gogrocery.Models.SideMenuModel.MenuBar> mCategoryList;
    private ActivityRedirection mActivityRedirectionListner;


    public SideMenuCategoryAdapter(Context mContext,
                                   List<com.gogrocery.Models.SideMenuModel.MenuBar> mCategoryList, ActivityRedirection mActivityRedirectionListner) {

        this.mContext = mContext;
        this.mCategoryList = mCategoryList;
        this.mActivityRedirectionListner=mActivityRedirectionListner;
        System.out.println("Rahul : DealsOfTheDayAdapter : mDealsOfTheDayDataList : " + mCategoryList.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.side_menus_row, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        com.gogrocery.Models.SideMenuModel.MenuBar mMenuBarInner = mCategoryList.get(position);

        holder.tvSideMenuTitle.setText(mMenuBarInner.getName());

        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

               mActivityRedirectionListner.redirect("sideMenu",new Gson().toJson(mCategoryList.get(position))+"#GoGrocery#"+mMenuBarInner.getName());
            }
        });
    }


    @Override
    public int getItemCount() {
        return mCategoryList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {


        private TextView tvSideMenuTitle;


        public MyViewHolder(View view) {
            super(view);

            tvSideMenuTitle=view.findViewById(R.id.tvSideMenuTitle);


        }

    }


}
