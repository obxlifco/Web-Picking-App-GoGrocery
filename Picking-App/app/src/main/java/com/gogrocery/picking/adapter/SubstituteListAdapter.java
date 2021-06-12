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
import com.gogrocery.picking.response_pojo.order_detail_pojo.OrderProductsItem;
import com.gogrocery.picking.response_pojo.order_detail_pojo.OrderSubstituteProductsItem;

import java.util.List;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

public class SubstituteListAdapter extends RecyclerView.Adapter<SubstituteListAdapter.SubstituteListViewHolder> {
    Context context;
    SubstituteListClickListener substituteListClickListener;
    List<OrderSubstituteProductsItem> orderSubstituteProducts;
    List<OrderProductsItem> orderProducts;

    public SubstituteListAdapter(Context context, List<OrderSubstituteProductsItem> orderSubstituteProducts, List<OrderProductsItem> orderProducts, SubstituteListClickListener substituteListClickListener) {
        this.context = context;
        this.orderSubstituteProducts = orderSubstituteProducts;
        this.substituteListClickListener = substituteListClickListener;
        this.orderProducts = orderProducts;
    }

    @NonNull
    @Override
    public SubstituteListViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(context).inflate(R.layout.row_substitute_list, parent, false);
        return new SubstituteListViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull SubstituteListViewHolder holder, int position) {
        Glide.with(context).load(orderSubstituteProducts.get(position).getProduct().getProductImages().get(0).getLink()+
                orderSubstituteProducts.get(position).getProduct().getProductImages().get(0).getImg())
                .placeholder(R.drawable.ic_product_default).into(holder.ivPicSubstituteRow);
        holder.tvNameSubstituteRow.setText(orderSubstituteProducts.get(position).getProduct().getName());
        holder.tvQtySubstituteRow.setText(orderSubstituteProducts.get(position).getQuantity()+"");
        holder.tvPriceSubstituteRow.setText(AppPreferences.getInstance().getCurrency()+" "+orderSubstituteProducts.get(position).getProductPrice()+"");
        if(orderSubstituteProducts.get(position).getProduct().getWeight()==null|| TextUtils.isEmpty(orderSubstituteProducts.get(position).getProduct().getWeight())){
            holder.tvWeightSubstituteRow.setText("");
        }else {
            holder.tvWeightSubstituteRow.setText(orderSubstituteProducts.get(position).getProduct().getWeight()+" "+
                    orderSubstituteProducts.get(position).getProduct().getUom().getUomName());
        }

        for(int i=0;i<orderProducts.size();i++){
            if(orderProducts.get(i).getProduct().getId()==orderSubstituteProducts.get(position).getSubstituteProductId()){
                holder.tvSubsNameSubstituteRow.setText(context.getResources().getString(R.string.txtSubstituteProductFor)+" : "+orderProducts.get(i).getProduct().getName());
            }
        }

        holder.tvValueAvail.setText(orderSubstituteProducts.get(position).getGrnQuantity()+"");
    }

    @Override
    public int getItemCount() {
        return orderSubstituteProducts.size();
    }

    public class SubstituteListViewHolder extends RecyclerView.ViewHolder {
        ImageView ivPicSubstituteRow;
        TextView tvNameSubstituteRow,tvWeightSubstituteRow,tvPriceSubstituteRow,tvDecreaseAvail,tvValueAvail,tvIncreaseAvail,
                tvQtySubstituteRow,tvSubsNameSubstituteRow;
        public SubstituteListViewHolder(@NonNull View itemView) {
            super(itemView);
            ivPicSubstituteRow=itemView.findViewById(R.id.ivPicSubstituteRow);
            tvNameSubstituteRow=itemView.findViewById(R.id.tvNameSubstituteRow);
            tvWeightSubstituteRow=itemView.findViewById(R.id.tvWeightSubstituteRow);
            tvPriceSubstituteRow=itemView.findViewById(R.id.tvPriceSubstituteRow);
            tvDecreaseAvail=itemView.findViewById(R.id.tvDecreaseAvail);
            tvValueAvail=itemView.findViewById(R.id.tvValueAvail);
            tvIncreaseAvail=itemView.findViewById(R.id.tvIncreaseAvail);
            tvQtySubstituteRow=itemView.findViewById(R.id.tvQtySubstituteRow);
            tvSubsNameSubstituteRow=itemView.findViewById(R.id.tvSubsNameSubstituteRow);
            itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    substituteListClickListener.substituteListClick(getAdapterPosition());
                }
            });
        }
    }

    public interface SubstituteListClickListener{
        public void substituteListClick(int position);
    }
}
