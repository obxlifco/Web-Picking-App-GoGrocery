package com.gogrocery.picking.adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.bumptech.glide.Glide;
import com.gogrocery.picking.R;
import com.gogrocery.picking.model.AddItemModel;
import com.gogrocery.picking.prefrences.AppPreferences;
import com.suke.widget.SwitchButton;

import java.text.DecimalFormat;
import java.util.List;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

public class SelectProductAdapter extends RecyclerView.Adapter<SelectProductAdapter.SelectProductViewHolder> {
    Context context;
    List<AddItemModel> addListItem;
    DecimalFormat formater = new DecimalFormat("0.00");

    public SelectProductAdapter(Context context, List<AddItemModel> addListItem) {
        this.context = context;
        this.addListItem = addListItem;
    }

    @NonNull
    @Override
    public SelectProductViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(context).inflate(R.layout.row_add_product, parent, false);
        return new SelectProductViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull SelectProductViewHolder holder, int position) {
        holder.tvNameRowProductListRow.setText(addListItem.get(position).getName());
        holder.tvWeightProductListRow.setText(addListItem.get(position).getWeight());
        holder.tvPriceProductListRow.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(addListItem.get(position).getPrice()) + "");
        if (addListItem.get(position).getImage().length() > 0) {
            Glide.with(context).load(addListItem.get(position).getImage()).placeholder(R.drawable.ic_product_default).into(holder.ivProductListRow);
        }
        holder.sbProductListRow.setVisibility(View.GONE);
        holder.tvQtyProductListRow.setText(context.getResources().getString(R.string.txtQty) + " : " +
                addListItem.get(position).getQty());
    }

    @Override
    public int getItemCount() {
        return addListItem.size();
    }

    public class SelectProductViewHolder extends RecyclerView.ViewHolder {
        ImageView ivProductListRow;
        TextView tvNameRowProductListRow, tvWeightProductListRow, tvPriceProductListRow, tvQtyProductListRow;
        SwitchButton sbProductListRow;
        LinearLayout llProductListRow;
        public SelectProductViewHolder(@NonNull View itemView) {
            super(itemView);
            ivProductListRow = itemView.findViewById(R.id.ivProductListRow);
            tvNameRowProductListRow = itemView.findViewById(R.id.tvNameRowProductListRow);
            tvWeightProductListRow = itemView.findViewById(R.id.tvWeightProductListRow);
            tvPriceProductListRow = itemView.findViewById(R.id.tvPriceProductListRow);
            sbProductListRow = itemView.findViewById(R.id.sbProductListRow);
            llProductListRow = itemView.findViewById(R.id.llProductListRow);
            tvQtyProductListRow = itemView.findViewById(R.id.tvQtyProductListRow);
        }
    }
}
