package com.gogrocery.Adapters;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RadioButton;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.gogrocery.Interfaces.SelectPreparationValue;
import com.gogrocery.R;

import java.util.List;

public class PreparationAdapter extends RecyclerView.Adapter<PreparationAdapter.MyViewHolder> {


    private Context mContext;
    private List<String> preparationList;
    private int checkedPosition = -1;
    SelectPreparationValue selectPreparationValue;
    public PreparationAdapter(Context mContext,
                              List<String> mPreparationList,SelectPreparationValue selectPreparationValue) {

        this.mContext = mContext;
        this.preparationList = mPreparationList;
        this.selectPreparationValue= selectPreparationValue;
        System.out.println("Rahul : PreparationAdapter : mWarehouseModelDataList : " + mPreparationList.size());

    }

    @NonNull
    @Override
    public PreparationAdapter.MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.layout_preperation_view, parent, false);


        return new PreparationAdapter.MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull PreparationAdapter.MyViewHolder holder, int position) {

        try {

            if (checkedPosition == -1) {
                holder.rbNoPreparation.setChecked(false);
            } else {
                holder.rbNoPreparation.setChecked(checkedPosition == position);
            }
           holder.rbNoPreparation.setText(preparationList.get(position));


            holder.rbNoPreparation.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    {
                        if (checkedPosition != position) {
                            notifyItemChanged(checkedPosition);
                            checkedPosition = position;
                        }
                        selectPreparationValue.selectedCustomFieldValue(holder.rbNoPreparation.getText().toString());
                    }

                }
            });
        } catch (Exception e) {
            System.out.println("Rahul : PreparationAdapter : Exception : " + e);
        }

    }


    @Override
    public int getItemCount() {

        return preparationList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {

        private RadioButton rbNoPreparation;

        public MyViewHolder(View view) {
            super(view);


            rbNoPreparation = view.findViewById(R.id.rbNoPreparation);


        }

    }


}