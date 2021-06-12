package com.gogrocery.Adapters;

import android.app.Activity;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RadioButton;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.core.content.ContextCompat;
import androidx.recyclerview.widget.RecyclerView;

import com.afollestad.materialdialogs.MaterialDialog;
import com.gogrocery.Interfaces.SelectAddressInterface;
import com.gogrocery.R;

import java.util.ArrayList;
import java.util.List;

public class MapAddressAdapter extends RecyclerView.Adapter<MapAddressAdapter.MyViewHolder> {


    private Activity mContext;
    private List<com.gogrocery.Models.MyAddressesModel.Data> myAddressList;
    private int checkedPosition = -1;
    SelectAddressInterface mSelectAddressInterface;
    public MapAddressAdapter(Activity mContext,List<com.gogrocery.Models.MyAddressesModel.Data> myAddressList,SelectAddressInterface mSelectAddressInterface) {

        this.mContext = mContext;
        this.myAddressList = myAddressList;
        this.mSelectAddressInterface= mSelectAddressInterface;


    }

    @NonNull
    @Override
    public MapAddressAdapter.MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.layout_map_address_view, parent, false);


        return new MapAddressAdapter.MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MapAddressAdapter.MyViewHolder holder, int position) {

        try {

            if (checkedPosition == -1) {
                holder.rbSelection.setChecked(false);
            } else {
                if (checkedPosition == position) {
                    holder.rbSelection.setChecked(true);
                } else {
                    holder.rbSelection.setChecked(false);
                }

            }
           holder.tvAddress.setText(myAddressList.get(position).getDeliveryStreetAddress() + " " + myAddressList.get(position).getDeliveryLandmark() + "\n" +
                   myAddressList.get(position).getDeliveryStateName() + " " + myAddressList.get(position).getDeliveryCountryName());


            holder.itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    holder.rbSelection.setChecked(true);
                    if (checkedPosition !=position) {
                        notifyItemChanged(checkedPosition);
                        checkedPosition = position;
                    }
                    mSelectAddressInterface.onSelectedAddressData(myAddressList.get(position).getLatVal(),myAddressList.get(position).getLongVal(),myAddressList.get(position).getDeliveryStreetAddress() + ", " + myAddressList.get(position).getDeliveryLandmark() + ", " +
                            myAddressList.get(position).getDeliveryStateName() + ", " + myAddressList.get(position).getDeliveryCountryName(),String.valueOf(myAddressList.get(position).getId()));

                }
            });


            holder.rbSelection.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    holder.rbSelection.setChecked(true);
                    if (checkedPosition !=position) {
                        notifyItemChanged(checkedPosition);
                        checkedPosition = position;
                    }
                    mSelectAddressInterface.onSelectedAddressData(myAddressList.get(position).getLatVal(),myAddressList.get(position).getLongVal(),myAddressList.get(position).getDeliveryStreetAddress() + " " + myAddressList.get(position).getDeliveryLandmark() + "," +
                            myAddressList.get(position).getDeliveryStateName() + " " + myAddressList.get(position).getDeliveryCountryName(),String.valueOf(myAddressList.get(position).getId()));


                }
            });
        } catch (Exception e) {
            System.out.println("Rahul : PreparationAdapter : Exception : " + e);
        }

    }


    @Override
    public int getItemCount() {

        return myAddressList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {
        private TextView tvAddress;
        private RadioButton rbSelection;

        public MyViewHolder(View view) {
            super(view);

            tvAddress = view.findViewById(R.id.tvAddress);
            rbSelection = view.findViewById(R.id.rbSelection);


        }

    }


    private void selectAddressItemPopup(int position) {
        new MaterialDialog.Builder(mContext)
                .title("Select Address")
                .content("Do you confirm this address?")
                .positiveText(mContext.getResources().getString(R.string.yes))
                .positiveColor(ContextCompat.getColor(mContext, R.color.green_dark_new))
                .negativeText(mContext.getResources().getString(R.string.no))
                .negativeColor(ContextCompat.getColor(mContext, R.color.gray_dark))
                .onPositive((dialog, which) -> {
                    mSelectAddressInterface.onSelectedAddressData(myAddressList.get(position).getLatVal(),myAddressList.get(position).getLongVal(),myAddressList.get(position).getDeliveryStreetAddress() + " " + myAddressList.get(position).getDeliveryLandmark() + "," +
                            myAddressList.get(position).getDeliveryStateName() + " " + myAddressList.get(position).getDeliveryCountryName(),String.valueOf(myAddressList.get(position).getId()));

                })
                .onNegative((dialog, which) -> {
                    dialog.dismiss();
                }).show();
    }


/*
    public void AddAllDeliveryAddress(List<com.gogrocery.Models.MyAddressesModel.Data> deliveryAddressList) {
        this.myAddressList.addAll(deliveryAddressList);

    }
    public void setCallback(SelectAddressInterface callback) {
        this.mSelectAddressInterface = callback;
    }
    public void clearListData() {
        this.myAddressList.clear();
    }*/

}