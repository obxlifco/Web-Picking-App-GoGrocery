package com.gogrocery.Adapters;

import android.content.Context;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.gogrocery.Interfaces.CountryStateListListner;
import com.gogrocery.Models.StateListModel.Data;
import com.gogrocery.R;

import java.util.List;


public class DeliverySlotAdapter extends RecyclerView.Adapter<DeliverySlotAdapter.MyViewHolder> {


    private Context mContext;
    private List<Data> mStateDataList;
    private CountryStateListListner mCountryStateListListner;


    public DeliverySlotAdapter(Context mContext,
                               List<Data> mStateDataList, CountryStateListListner mCountryStateListListner) {

        this.mContext = mContext;
        this.mStateDataList = mStateDataList;
        this.mCountryStateListListner = mCountryStateListListner;
        System.out.println("Rahul : StateListAdapter : mStateDataList : " + mStateDataList.size());

    }

    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.single_text_row, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        Data mDataInner = mStateDataList.get(position);

        holder.tvTitle.setText(mDataInner.getStateName());
        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mCountryStateListListner.passID("state", mDataInner.getId(),mDataInner.getStateName());
            }
        });
    }


    @Override
    public int getItemCount() {
        return mStateDataList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {


        private TextView tvTitle;


        public MyViewHolder(View view) {
            super(view);


            tvTitle = view.findViewById(R.id.tvTitle);


        }

    }


}
