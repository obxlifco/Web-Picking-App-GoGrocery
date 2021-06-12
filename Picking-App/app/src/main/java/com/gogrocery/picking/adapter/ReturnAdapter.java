package com.gogrocery.picking.adapter;

import android.content.Context;
import android.text.TextUtils;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.bumptech.glide.Glide;
import com.gogrocery.picking.R;
import com.gogrocery.picking.prefrences.AppPreferences;
import com.gogrocery.picking.response_pojo.search_return_pojo.OrderProductsItem;

import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

public class ReturnAdapter extends RecyclerView.Adapter<ReturnAdapter.ReturnViewHolder> {
    Context context;
    ReturnListClickListener returnListClickListener;
    List<OrderProductsItem> orderProducts;
    List<Integer> initReturnQty =new ArrayList<>();
    DecimalFormat formater = new DecimalFormat("0.00");

    public ReturnAdapter(Context context, List<OrderProductsItem> orderProducts,List<Integer> initReturnQty, ReturnListClickListener returnListClickListener) {
        this.context = context;
        this.returnListClickListener = returnListClickListener;
        this.orderProducts = orderProducts;
        this.initReturnQty = initReturnQty;
    }

    @NonNull
    @Override
    public ReturnViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(context).inflate(R.layout.row_return_item, parent, false);
        return new ReturnViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull ReturnViewHolder holder, int position) {
        if(orderProducts.get(position).getProduct().getProductImages()!=null&&orderProducts.get(position).getProduct().getProductImages().size()>0&& !TextUtils.isEmpty(orderProducts.get(position).getProduct().getProductImages().get(0).getLink())){
            Glide.with(context).load(orderProducts.get(position).getProduct().getProductImages().get(0).getLink()+
                    orderProducts.get(position).getProduct().getProductImages().get(0).getImg())
                    .placeholder(R.drawable.ic_product_default).into(holder.ivPicReturnRow);
        }
        holder.tvNameReturnRow.setText(orderProducts.get(position).getProduct().getName());
        if (orderProducts.get(position).getProduct().getWeight() == null||orderProducts.get(position).getProduct().getWeight().length()==0) {
            holder.tvWeightReturnRow.setText("");
        } else {
            holder.tvWeightReturnRow.setText(orderProducts.get(position).getProduct().getWeight() + " " +
                    orderProducts.get(position).getProduct().getUom().getUomName());
        }
        holder.tvQtyReturnRow.setText(context.getResources().getString(R.string.txtQty)+" : "+
                orderProducts.get(position).getGrnQuantity());
        holder.tvPriceReturnRow.setText(AppPreferences.getInstance().getCurrency()+" "+formater.format(orderProducts.get(position).getProductPrice()));
        holder.tvValueReturnRow.setText(orderProducts.get(position).getReturns()+"");
        if(orderProducts.get(position).getReturns()>0){
            holder.llReturnRow.setVisibility(View.VISIBLE);
            holder.tvReturnRow.setVisibility(View.GONE);
        }else{
            holder.llReturnRow.setVisibility(View.GONE);
            holder.tvReturnRow.setVisibility(View.VISIBLE);
        }
    }

    @Override
    public int getItemCount() {
        return orderProducts.size();
    }

    public class ReturnViewHolder extends RecyclerView.ViewHolder {
        ImageView ivPicReturnRow;
        LinearLayout llReturnRow;
        TextView tvNameReturnRow,tvWeightReturnRow,tvQtyReturnRow,tvPriceReturnRow,tvReturnRow,tvDecreaseReturnRow,tvValueReturnRow,tvIncreaseReturnRow;
        public ReturnViewHolder(@NonNull View itemView) {
            super(itemView);
            ivPicReturnRow=itemView.findViewById(R.id.ivPicReturnRow);
            tvNameReturnRow=itemView.findViewById(R.id.tvNameReturnRow);
            tvWeightReturnRow=itemView.findViewById(R.id.tvWeightReturnRow);
            tvQtyReturnRow=itemView.findViewById(R.id.tvQtyReturnRow);
            tvPriceReturnRow=itemView.findViewById(R.id.tvPriceReturnRow);
            tvReturnRow=itemView.findViewById(R.id.tvReturnRow);
            llReturnRow=itemView.findViewById(R.id.llReturnRow);
            tvDecreaseReturnRow=itemView.findViewById(R.id.tvDecreaseReturnRow);
            tvValueReturnRow=itemView.findViewById(R.id.tvValueReturnRow);
            tvIncreaseReturnRow=itemView.findViewById(R.id.tvIncreaseReturnRow);

            tvIncreaseReturnRow.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    if (orderProducts.get(getAdapterPosition()).getGrnQuantity() > orderProducts.get(getAdapterPosition()).getReturns()) {
                        increaseReturn(getAdapterPosition());
                        notifyDataSetChanged();
                    }
                }
            });
            tvDecreaseReturnRow.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    if (orderProducts.get(getAdapterPosition()).getReturns() > 0 &&
                            orderProducts.get(getAdapterPosition()).getReturns()> initReturnQty.get(getAdapterPosition())) {
                        decreaseReturn(getAdapterPosition());
                        notifyDataSetChanged();
                    }
                }
            });
            tvReturnRow.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    if (orderProducts.get(getAdapterPosition()).getGrnQuantity() > orderProducts.get(getAdapterPosition()).getReturns()) {
                        increaseReturn(getAdapterPosition());
                        notifyDataSetChanged();
                    }
                }
            });
        }
    }

    public void increaseReturn(int pos) {
        orderProducts.get(pos).setReturns(orderProducts.get(pos).getReturns() + 1);
        returnListClickListener.returnListClick(pos);
    }

    public void decreaseReturn(int pos) {
        orderProducts.get(pos).setReturns(orderProducts.get(pos).getReturns() - 1);
        returnListClickListener.returnListClick(pos);
    }

    public interface ReturnListClickListener{
        public void returnListClick(int position);
    }
}
