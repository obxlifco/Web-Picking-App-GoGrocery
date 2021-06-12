package com.gogrocery.Adapters;

import android.content.Context;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.gogrocery.Interfaces.ActivityRedirection;
import com.gogrocery.Models.CMS_Model.ParentCategoryList;
import com.gogrocery.R;

import java.util.List;


public class SearchPageCategoryAdapter extends RecyclerView.Adapter<SearchPageCategoryAdapter.MyViewHolder> {


    private Context mContext;
    private List<ParentCategoryList> mCMS_parentCategoryLists;
    private ActivityRedirection mActivityRedirectionListner;


    public SearchPageCategoryAdapter(Context mContext,
                                     List<ParentCategoryList> mCMS_parentCategoryLists, ActivityRedirection mActivityRedirectionListner) {

        this.mContext = mContext;
        this.mCMS_parentCategoryLists = mCMS_parentCategoryLists;
        this.mActivityRedirectionListner=mActivityRedirectionListner;
        System.out.println("Rahul : DealsOfTheDayAdapter : mDealsOfTheDayDataList : " + mCMS_parentCategoryLists.size());

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
        ParentCategoryList mMenuBarInner = mCMS_parentCategoryLists.get(position);

        holder.tvName.setText(mMenuBarInner.getName());

    }


    @Override
    public int getItemCount() {
        return mCMS_parentCategoryLists.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {


        private TextView tvName;


        public MyViewHolder(View view) {
            super(view);


            tvName = view.findViewById(R.id.tvName);



        }

    }


}
