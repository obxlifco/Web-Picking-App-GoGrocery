package com.gogrocery.picking.adapter;

import android.content.Context;
import android.text.TextUtils;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import com.bumptech.glide.Glide;
import com.gogrocery.picking.R;
import com.gogrocery.picking.prefrences.AppPreferences;
import com.gogrocery.picking.response_pojo.stock_list_pojo.StockItem;
import com.gogrocery.picking.utils.MyDialog;
import com.suke.widget.SwitchButton;

import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

public class StockListAdapter extends RecyclerView.Adapter<StockListAdapter.StockListViewHolder> {
    Context context;
    StockListClickListener stockListClickListener;
    List<StockItem> stockItems = new ArrayList<>();
    DecimalFormat formater = new DecimalFormat("0.00");

    public StockListAdapter(Context context, List<StockItem> stockItems, StockListClickListener stockListClickListener) {
        this.context = context;
        this.stockListClickListener = stockListClickListener;
        this.stockItems = stockItems;
    }

    @NonNull
    @Override
    public StockListViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(context).inflate(R.layout.row_stock_list, parent, false);
        return new StockListViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull StockListViewHolder holder, int position) {
        if (stockItems.get(position).getProductImages() != null && stockItems.get(position).getProductImages().size() > 0 && !TextUtils.isEmpty(stockItems.get(position).getProductImages().get(0).getLink())) {
            Glide.with(context).load(stockItems.get(position).getProductImages().get(0).getLink() +
                    stockItems.get(position).getProductImages().get(0).getImg())
                    .placeholder(R.drawable.ic_product_default).into(holder.ivPicStockRow);
        }
        holder.tvNameStockRow.setText(stockItems.get(position).getName());
        holder.tvPriceStockRow.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(stockItems.get(position).getChannelCurrencyProductPrice().getPrice()));
        if (stockItems.get(position).getWeight() == null || TextUtils.isEmpty(stockItems.get(position).getWeight())) {
            holder.tvWeightStockRow.setText("");
            holder.tvWeightStockRow.setVisibility(View.GONE);
        } else {
            holder.tvWeightStockRow.setVisibility(View.VISIBLE);
            holder.tvWeightStockRow.setText(stockItems.get(position).getWeight() + " " + stockItems.get(position).getUomName());
        }
        //holder.sbStockRow.setClickable(false);
        if (stockItems.get(position).getProductStock().getRealStock() > 0) {
            holder.sbStockRow.setChecked(true);
        } else {
            holder.sbStockRow.setChecked(false);
        }
    }

    @Override
    public int getItemCount() {
        return stockItems.size();
    }

    public class StockListViewHolder extends RecyclerView.ViewHolder {
        TextView tvEditStockRow, tvNameStockRow, tvWeightStockRow, tvPriceStockRow;
        ImageView ivPicStockRow;
        SwitchButton sbStockRow;

        public StockListViewHolder(@NonNull View itemView) {
            super(itemView);
            tvEditStockRow = itemView.findViewById(R.id.tvEditStockRow);
            ivPicStockRow = itemView.findViewById(R.id.ivPicStockRow);
            tvNameStockRow = itemView.findViewById(R.id.tvNameStockRow);
            tvWeightStockRow = itemView.findViewById(R.id.tvWeightStockRow);
            tvPriceStockRow = itemView.findViewById(R.id.tvPriceStockRow);
            sbStockRow = itemView.findViewById(R.id.sbStockRow);

            tvEditStockRow.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    stockListClickListener.onEditClick(getAdapterPosition());
                }
            });
            sbStockRow.setOnCheckedChangeListener(new SwitchButton.OnCheckedChangeListener() {
                @Override
                public void onCheckedChanged(SwitchButton view, boolean isChecked) {
                    if (isChecked) {
                        if(stockItems.get(getAdapterPosition()).getChannelCurrencyProductPrice().getPrice()>0) {
                            stockListClickListener.stockListClick(getAdapterPosition(), sbStockRow.isChecked());
                        }else{
                            notifyItemChanged(getAdapterPosition());
                            MyDialog.defaultShowInfoPopup(context,"Set price","The price must be set first before the stock","Ok");
                        }
                    } else {
                        stockListClickListener.stockListClick(getAdapterPosition(), sbStockRow.isChecked());
                    }

                }
            });
        }
    }

    public interface StockListClickListener {
        public void stockListClick(int position, boolean checked);

        public void onEditClick(int position);
    }
}
