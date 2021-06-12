package com.gogrocery.Adapters;

import android.content.Context;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.gogrocery.Interfaces.FilterMenuConnectInterface;
import com.gogrocery.Models.FilterModel.FilterModel;
import com.gogrocery.R;
import com.google.gson.Gson;

import java.util.List;


public class FilterLeftSideMenuAdapter extends RecyclerView.Adapter<FilterLeftSideMenuAdapter.MyViewHolder> {


    private Context mContext;
    private List<FilterModel> mFilterModelList;
    private FilterMenuConnectInterface mFilterMenuConnectInterface;
    private int lastSelected = 0;
    private LinearLayout.LayoutParams params;

    public FilterLeftSideMenuAdapter(Context mContext,
                                     List<FilterModel> mFilterModelList, FilterMenuConnectInterface mFilterMenuConnectInterface) {
        this.mContext = mContext;
        this.mFilterModelList = mFilterModelList;
        this.mFilterMenuConnectInterface = mFilterMenuConnectInterface;
    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.filter_side_menu_row, parent, false);

        params = new LinearLayout.LayoutParams(0, 0);
        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        FilterModel mFilterModelInner = mFilterModelList.get(position);
        try {
            if (mFilterModelInner.getChild().size() <= 0) {
                holder.itemView.setLayoutParams(params);
            }

            if (lastSelected == position) {
              // holder.itemView.setBackground(mContext.getResources().getDrawable(R.drawable.black_shadow_gradient));
                holder.mview.setVisibility(View.INVISIBLE);
                holder.itemView.setBackgroundColor(mContext.getResources().getColor(R.color.white));
            } else {
                //holder.itemView.setBackgroundColor(mContext.getResources().getColor(R.color.white));
                holder.mview.setVisibility(View.VISIBLE);
                holder.itemView.setBackgroundColor(mContext.getResources().getColor(R.color.filter_unselected));
            }


            holder.tvSideMenuCategory.setText(mFilterModelInner.getFieldName());
            holder.itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                   /* holder.mview.setVisibility(View.INVISIBLE);
                    holder.itemView.setBackgroundColor(mContext.getResources().getColor(R.color.white));*/
                    lastSelected = position;
                    mFilterMenuConnectInterface.connectLeftToRight(position, new Gson().toJson(mFilterModelInner), mFilterModelInner.getFieldName());
                }
            });
        } catch (NullPointerException e) {
        }
    }


    @Override
    public int getItemCount() {
        return mFilterModelList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {


        private TextView tvSideMenuCategory;
        private View mview;

        public MyViewHolder(View view) {
            super(view);


            tvSideMenuCategory = view.findViewById(R.id.tvSideMenuCategory);
            mview = view.findViewById(R.id.view);


        }

    }


}
