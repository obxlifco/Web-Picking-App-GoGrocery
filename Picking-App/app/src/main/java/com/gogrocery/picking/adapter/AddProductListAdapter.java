package com.gogrocery.picking.adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.bumptech.glide.Glide;
import com.gogrocery.picking.R;
import com.gogrocery.picking.model.AddItemModel;
import com.gogrocery.picking.prefrences.AppPreferences;
import com.gogrocery.picking.utils.AppUtilities;
import com.gogrocery.picking.utils.MyDialog;
import com.suke.widget.SwitchButton;

import java.text.DecimalFormat;
import java.util.List;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.recyclerview.widget.RecyclerView;

public class AddProductListAdapter extends RecyclerView.Adapter<AddProductListAdapter.AddProductListViewHolder> {
    Context context;
    AddProductListClickListener addProductListClickListener;
    List<AddItemModel> addListItem;
    DecimalFormat formater = new DecimalFormat("0.00");
    boolean isAdd;

    public AddProductListAdapter(Context context, List<AddItemModel> addListItem, boolean isAdd, AddProductListClickListener addProductListClickListener) {
        this.context = context;
        this.addProductListClickListener = addProductListClickListener;
        this.addListItem = addListItem;
        this.isAdd = isAdd;
    }

    @NonNull
    @Override
    public AddProductListViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(context).inflate(R.layout.row_add_product, parent, false);
        return new AddProductListViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull AddProductListViewHolder holder, int position) {
        holder.tvNameRowProductListRow.setText(addListItem.get(position).getName());
        holder.tvWeightProductListRow.setText(addListItem.get(position).getWeight());
        holder.tvPriceProductListRow.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(addListItem.get(position).getPrice()) + "");
        if (addListItem.get(position).getImage().length() > 0) {
            Glide.with(context).load(addListItem.get(position).getImage()).placeholder(R.drawable.ic_product_default).into(holder.ivProductListRow);
        }
        holder.sbProductListRow.setClickable(false);
        if (addListItem.get(position).getStock() > 0) {
            holder.sbProductListRow.setChecked(true);
        } else {
            holder.sbProductListRow.setChecked(false);
        }
        if (addListItem.get(position).isSelect()) {
            holder.llProductListRow.setVisibility(View.VISIBLE);
        } else {
            holder.llProductListRow.setVisibility(View.GONE);
        }
        holder.tvQtyProductListRow.setText(context.getResources().getString(R.string.txtQty) + " : " +
                addListItem.get(position).getQty());
    }

    @Override
    public int getItemCount() {
        return addListItem.size();
    }

    public class AddProductListViewHolder extends RecyclerView.ViewHolder {
        ImageView ivProductListRow;
        TextView tvNameRowProductListRow, tvWeightProductListRow, tvPriceProductListRow, tvQtyProductListRow;
        SwitchButton sbProductListRow;
        LinearLayout llProductListRow;

        public AddProductListViewHolder(@NonNull View itemView) {
            super(itemView);
            ivProductListRow = itemView.findViewById(R.id.ivProductListRow);
            tvNameRowProductListRow = itemView.findViewById(R.id.tvNameRowProductListRow);
            tvWeightProductListRow = itemView.findViewById(R.id.tvWeightProductListRow);
            tvPriceProductListRow = itemView.findViewById(R.id.tvPriceProductListRow);
            sbProductListRow = itemView.findViewById(R.id.sbProductListRow);
            llProductListRow = itemView.findViewById(R.id.llProductListRow);
            tvQtyProductListRow = itemView.findViewById(R.id.tvQtyProductListRow);

            tvQtyProductListRow.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    if (addListItem.get(getAdapterPosition()).getStock() > 0 &&
                            llProductListRow.getVisibility() == View.GONE && isAdd) {
                        MyDialog.showCustomEditTextOkCancelPopup(context, context.getResources().getString(R.string.txtEnterQuantity),
                                context.getResources().getString(R.string.txtQty),String.valueOf(addListItem.get(getAdapterPosition()).getQty()), new MyDialog.CustomEditTextOkCancelPopupCallback() {
                                    @Override
                                    public void onDoneClick(String val, AlertDialog alertDialog) {
                                        if (addListItem.get(getAdapterPosition()).getStock() >= Long.parseLong(val)) {
                                            addListItem.get(getAdapterPosition()).setQty(Long.parseLong(val));
                                            notifyItemChanged(getAdapterPosition());
                                            AppUtilities.hideKeyboard(view);
                                            alertDialog.dismiss();
                                        } else {
                                            Toast.makeText(context, context.getResources().getString(R.string.txtStockNotAvailable), Toast.LENGTH_SHORT).show();
                                        }

                                    }

                                    @Override
                                    public void onCancelClick(AlertDialog alertDialog) {
                                        AppUtilities.hideKeyboard(view);
                                        alertDialog.dismiss();
                                    }
                                });
                    }
                }
            });

            itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    if (addListItem.get(getAdapterPosition()).getStock() > 0) {
                        if (isAdd) {
                            if (addListItem.get(getAdapterPosition()).isSelect()) {
                                addListItem.get(getAdapterPosition()).setSelect(false);
                                addProductListClickListener.productListRemove(getAdapterPosition());
                            } else {
                                addListItem.get(getAdapterPosition()).setSelect(true);
                                addProductListClickListener.productListAdd(getAdapterPosition());
                            }
                            notifyItemChanged(getAdapterPosition());
                        } else {
                            if (addListItem.get(getAdapterPosition()).getSubstituteStatus() == 0) {
                                MyDialog.showOkCancelPopup(addListItem.get(getAdapterPosition()).getSubstituteMsg(), "Ok",
                                        "Cancel", context, new MyDialog.OkCancelPopupCallback() {
                                            @Override
                                            public void onPositiveClick() {
                                                addProductListClickListener.addToSubstitute(getAdapterPosition());
                                                addListItem.get(getAdapterPosition()).setSubstituteStatus(1);
                                                addListItem.get(getAdapterPosition()).setSelect(true);
                                                addProductListClickListener.productListAdd(getAdapterPosition());
                                                notifyItemChanged(getAdapterPosition());
                                            }

                                            @Override
                                            public void onNegativeClick() {

                                            }
                                        });

                            } else {
                                if (addListItem.get(getAdapterPosition()).isSelect()) {
                                    addListItem.get(getAdapterPosition()).setSelect(false);
                                    addProductListClickListener.productListRemove(getAdapterPosition());
                                } else {
                                    addListItem.get(getAdapterPosition()).setSelect(true);
                                    addProductListClickListener.productListAdd(getAdapterPosition());
                                }
                                notifyItemChanged(getAdapterPosition());
                            }
                        }
                    }
                }
            });
        }
    }

    public interface AddProductListClickListener {
        public void productListAdd(int position);

        public void productListRemove(int position);

        public void addToSubstitute(int position);
    }
}
