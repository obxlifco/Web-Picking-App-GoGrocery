package com.gogrocery.Adapters;

import android.app.Activity;
import android.content.Context;
import androidx.annotation.NonNull;
import androidx.core.content.ContextCompat;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.PopupMenu;
import android.widget.RadioButton;
import android.widget.TextView;

import com.afollestad.materialdialogs.MaterialDialog;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.MyAddressSelected;
import com.gogrocery.R;

import java.util.List;


public class MyAddressesAdapter extends RecyclerView.Adapter<MyAddressesAdapter.MyViewHolder> {

private Activity activity;
    private Context mContext;
    private DatabaseHandler mDatabaseHandler;
    private List<com.gogrocery.Models.MyAddressesModel.Data> mMyAddressesList;
    private MyAddressSelected mMyAddressSelected;
   private int lastSelected = -1;
    private String isFrom = "";

    public MyAddressesAdapter(Context mContext,Activity activity,
                              List<com.gogrocery.Models.MyAddressesModel.Data> mMyAddressesList, MyAddressSelected mMyAddressSelected, String isFrom) {

        this.mContext = mContext;
        this.activity = activity;
        this.mMyAddressesList = mMyAddressesList;
        this.mMyAddressSelected = mMyAddressSelected;
        this.mDatabaseHandler = mDatabaseHandler;
        this.isFrom = isFrom;
        System.out.println("Rahul : MyCartAdapter : mMyAddressesList : " + mMyAddressesList.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.my_addresses_row, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {

        com.gogrocery.Models.MyAddressesModel.Data mDataInner = mMyAddressesList.get(position);
//String selectedId = String.valueOf(mMyAddressesList.get(position).getId());

        /*if (lastSelected == position) {
            holder.rbSelection.setChecked(true);

        } else {
            holder.rbSelection.setChecked(false);
        }*/



        if (lastSelected == -1) {
            holder.rbSelection.setChecked(false);
        } else {
            if (lastSelected == position) {
                holder.rbSelection.setChecked(true);
            } else {
                holder.rbSelection.setChecked(false);
            }
        }

        holder.tvName.setText(mDataInner.getDeliveryName());
        holder.tvAddress.setText(mDataInner.getDeliveryStreetAddress() +", "+ mDataInner.getDeliveryLandmark() + "\n" +
                mDataInner.getDeliveryStateName() + " " + mDataInner.getDeliveryCountryName());
        holder.tvMobileNumber.setText(mDataInner.getDeliveryPhone());

        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
               // lastSelected = position;
                holder.rbSelection.setChecked(true);
                if (lastSelected !=position) {
                    notifyItemChanged(lastSelected);
                    lastSelected = position;
                }


                mMyAddressSelected.selectedAddressData(holder.tvName.getText().toString(), holder.tvMobileNumber.getText().toString(), holder.tvAddress.getText().toString(), String.valueOf(mMyAddressesList.get(position).getId()),mMyAddressesList.get(position).getLatVal(),mMyAddressesList.get(position).getLongVal());
            }
        });

        holder.rbSelection.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                holder.rbSelection.setChecked(true);
                if (lastSelected !=position) {
                    notifyItemChanged(lastSelected);
                    lastSelected = position;
                }

                mMyAddressSelected.selectedAddressData(holder.tvName.getText().toString(), holder.tvMobileNumber.getText().toString(), holder.tvAddress.getText().toString(), String.valueOf(mMyAddressesList.get(position).getId()),mMyAddressesList.get(position).getLatVal(),mMyAddressesList.get(position).getLongVal());

            }
        });

        if (isFrom.equals("")) {
            holder.rbSelection.setVisibility(View.GONE);
        }


        holder.ivMoreAddress.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    PopupMenu popup = new PopupMenu(mContext, v);

                    popup.inflate(R.menu.my_address_menu);

                    popup.setOnMenuItemClickListener(new PopupMenu.OnMenuItemClickListener() {
                        @Override
                        public boolean onMenuItemClick(MenuItem item) {
                            switch (item.getItemId()) {
                            case R.id.edit:
                                mMyAddressSelected.myAddressMenu("edit","" + mDataInner.getId(), position);
                                break;
                                case R.id.delete:
                                   // mMyAddressSelected.myAddressMenu("delete","" + mDataInner.getId(), position);

                                    deleteItemPopup(position);
                                    break;

                            }
                            return false;
                        }


                    });

                    popup.show();
                } catch (Exception e) {
                    System.out.println("Rahul : MyAddressesAdapter : Exception " + e);
                }
            }
        });

        if (mMyAddressesList.get(position).getSetPrimary() == 1) {
            holder.tvIsDefault.setVisibility(View.VISIBLE);
            //  holder.rbSelection.setChecked(true);
        } else {
            holder.tvIsDefault.setVisibility(View.INVISIBLE);
          //  holder.rbSelection.setChecked(false);


        }
    }


    @Override
    public int getItemCount() {
        return mMyAddressesList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {


        private TextView tvName, tvMobileNumber, tvAddress, tvIsDefault;
        private RadioButton rbSelection;
        private ImageView ivMoreAddress;

        public MyViewHolder(View view) {
            super(view);


            tvName = view.findViewById(R.id.tvName);
            tvMobileNumber = view.findViewById(R.id.tvMobileNumber);
            tvAddress = view.findViewById(R.id.tvAddress);
            tvIsDefault = view.findViewById(R.id.tvIsDefault);
            rbSelection = view.findViewById(R.id.rbSelection);
            ivMoreAddress = view.findViewById(R.id.ivMoreAddress);


        }

    }



    private void deleteItemPopup(int position) {
        new MaterialDialog.Builder(activity)
                .title(activity.getResources().getString(R.string.dialogTitle_deleteFromMyAddress))
                .content(activity.getResources().getString(R.string.dialogMessage_deleteFromMyAddress))
                .positiveText(activity.getResources().getString(R.string.dialogPositiveButtonText_delete))
                .positiveColor(ContextCompat.getColor(activity, R.color.app_red_clr))
                .negativeText(activity.getResources().getString(R.string.dialogPositiveButtonText_cancel))
                .negativeColor(ContextCompat.getColor(activity, R.color.black))
                .onPositive((dialog, which) -> {

                    mMyAddressSelected.myAddressMenu("delete","" + mMyAddressesList.get(position).getId(), position);
                })
                .onNegative((dialog, which) -> {
                    dialog.dismiss();
                }).show();
    }


}
