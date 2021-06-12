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
import com.gogrocery.R;

import java.util.List;


public class SideMenuChildAdapter extends RecyclerView.Adapter<SideMenuChildAdapter.MyViewHolder> {


    private Context mContext;
    private List<com.gogrocery.Models.SideMenuModel.Child> mSideMenuChildList;
    private ActivityRedirection mActivityRedirectionListner;


    public SideMenuChildAdapter(Context mContext,
                                List<com.gogrocery.Models.SideMenuModel.Child> mSideMenuChildList, ActivityRedirection mActivityRedirectionListner) {

        this.mContext = mContext;
        this.mSideMenuChildList = mSideMenuChildList;
        this.mActivityRedirectionListner = mActivityRedirectionListner;
        System.out.println("Rahul : SideMenuChildAdapter : mSideMenuChildList : " + mSideMenuChildList.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.child_menu_row, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        com.gogrocery.Models.SideMenuModel.Child mChildInner = mSideMenuChildList.get(position);

        holder.tvChildMenu.setText(mChildInner.getName());

        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                mActivityRedirectionListner.redirect("childSideMenu", mChildInner.getSlug()+"#GoGrocery#"+mChildInner.getName());
            }
        });
    }


    @Override
    public int getItemCount() {
        return mSideMenuChildList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {


        private TextView tvChildMenu;
        private ImageView iv2;


        public MyViewHolder(View view) {
            super(view);

            tvChildMenu = view.findViewById(R.id.tvChildMenu);
            iv2 = view.findViewById(R.id.iv2);
        }

    }


}
