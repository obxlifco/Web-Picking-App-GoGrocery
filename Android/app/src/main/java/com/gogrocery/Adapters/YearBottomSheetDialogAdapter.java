package com.gogrocery.Adapters;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.gogrocery.Interfaces.SingleStringPassingInterface;
import com.gogrocery.R;


import com.gogrocery.Models.MonthYearModel;

import java.util.List;


public class YearBottomSheetDialogAdapter extends RecyclerView.Adapter<YearBottomSheetDialogAdapter.MyViewHolder> {


    private List<MonthYearModel> mMonthYearModel;
    private SingleStringPassingInterface mSingleStringPassingInterface;

    public YearBottomSheetDialogAdapter(List<MonthYearModel> mMonthYearModel, SingleStringPassingInterface mSingleStringPassingInterface) {
        this.mMonthYearModel = mMonthYearModel;
        this.mSingleStringPassingInterface = mSingleStringPassingInterface;
    }

    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.single_text_row_layout, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        MonthYearModel mCountryList = mMonthYearModel.get(position);


        holder.countryName.setText(mCountryList.getYear());
        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                mSingleStringPassingInterface.passValue(holder.countryName.getText().toString()+"#GoGrocery#"+(position+1));
                //  mCountryListClick.CountryRowClick(mCountryList.getYear()+":"+position,"");
            }
        });
    }

    @Override
    public int getItemCount() {
        return mMonthYearModel.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {
        public TextView countryName;


        public MyViewHolder(View view) {
            super(view);
            countryName = view.findViewById(R.id.countryName);

        }
    }
}
