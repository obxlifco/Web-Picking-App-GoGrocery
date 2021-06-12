package com.gogrocery.Adapters;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.bumptech.glide.Glide;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Fragment.SubstituteFragment;
import com.gogrocery.Interfaces.CustomFieldChooseInterface;
import com.gogrocery.Interfaces.SubstituteListClickListener;
import com.gogrocery.Models.OrderListDetailsModel.SubstituteProductsItem;
import com.gogrocery.R;
import com.gogrocery.view.SubstituteActivity;

import java.util.List;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import static com.facebook.FacebookSdk.getApplicationContext;

public class SubstituteListAdapter extends RecyclerView.Adapter<SubstituteListAdapter.SubstituteListViewHolder>{
    Context context;
    SubstituteListClickListener substituteListClickListener;
    CustomFieldChooseInterface mCustomFieldChooseInterface;
    List<SubstituteProductsItem> substituteProducts;

    Integer shortage = 0 ;

    public SubstituteListAdapter(Context context, List<SubstituteProductsItem> substituteProducts, SubstituteListClickListener substituteListClickListener,int shortage,CustomFieldChooseInterface mCustomFieldChooseInterface) {
        this.context = context;
        this.mCustomFieldChooseInterface = mCustomFieldChooseInterface;
        this.substituteListClickListener = substituteListClickListener;
        this.substituteProducts = substituteProducts;
        this.shortage = shortage;



    }

    @NonNull
    @Override
    public SubstituteListViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.substitute_list_row, parent, false);

        return new SubstituteListAdapter.SubstituteListViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull SubstituteListViewHolder holder, int position) {
        if (substituteProducts.get(position).getProduct().getProductImages().get(0).getLink() != null &&
                substituteProducts.get(position).getProduct().getProductImages().get(0).getLink().length() > 0) {
            Glide.with(context).load(substituteProducts.get(position).getProduct().getProductImages().get(0).getLink() +
                    substituteProducts.get(position).getProduct().getProductImages().get(0).getImg()).placeholder(R.drawable.dummy_item_img).into(holder.ivPicSubsListRow);
        }
        holder.tvNameSubsListRow.setText(substituteProducts.get(position).getProduct().getName());
        holder.tvValueReturnRow.setText(substituteProducts.get(position).getGrnQuantity()+"");
        holder.tvWeightSubsListRow.setText(substituteProducts.get(position).getWeight() + " " + substituteProducts.get(position).getProduct().getUom().getUomName());
        holder.tvPriceSubsListRow.setText(new SharedPreferenceManager(getApplicationContext()).getCurrentCurrency() + " " + Constants.twoDecimalRoundOff(substituteProducts.get(position).getProductPrice()));

        if (substituteProducts.get(position).getGrnQuantity() == 0) {
            holder.llReturnRow.setVisibility(View.GONE);
            holder.tvReturnRow.setVisibility(View.VISIBLE);
            //bsp_itemClick_interface.connectMain(Integer.parseInt(mHitInner.getId()), 0);
        } else {
            holder.llReturnRow.setVisibility(View.VISIBLE);
            holder.tvReturnRow.setVisibility(View.GONE);
        }

        holder.tvReturnRow.setOnClickListener(v -> {
            if(((SubstituteActivity)context).isProcessable){
            if(checkMaxLimit(position)){

                if(substituteProducts.get(position).getProduct().getCustomField()!=null&&!substituteProducts.get(position).getProduct().getCustomField().isEmpty()&&substituteProducts.get(position).getProduct().getCustomField().size()>0) {
                    String custom_field_name = substituteProducts.get(position).getProduct().getCustomField().get(0).getFieldName();
                        String custom_field_value = substituteProducts.get(position).getProduct().getCustomField().get(0).getValue();
                        mCustomFieldChooseInterface.selectedCustomFieldValue(position,custom_field_name,custom_field_value);


                }else {
                     increaseAvailable(position);
                }


            }else {
                Toast.makeText(context,"Quantity should not be greater than Shortage Quantity",Toast.LENGTH_SHORT).show();

            }}
        });

        holder.tvIncreaseReturnRow.setOnClickListener(v -> {
            if(((SubstituteActivity)context).isProcessable) {
                if (checkMaxLimit(position)) {
                    increaseAvailable(position);
                } else {
                    Toast.makeText(context, "Quantity should not be greater than Shortage Quantity", Toast.LENGTH_SHORT).show();

                }
            }

        });

        holder.tvDecreaseReturnRow.setOnClickListener(v -> {
            if(((SubstituteActivity)context).isProcessable) {
                decreaseAvailable(position);
            }
        });


    }

    private boolean checkMaxLimit(int position) {
        int qty=0;
        for(int i=0;i<substituteProducts.size();i++){
            qty=qty+substituteProducts.get(i).getGrnQuantity();
        }
        if(qty>=shortage){
            return false;
        }else{
            return true;
        }
    }

    public void increaseAvailable(int pos) {
        substituteProducts.get(pos).setGrnQuantity(substituteProducts.get(pos).getGrnQuantity() + 1);
        substituteListClickListener.substituteQuantity(pos);
    }

    public void decreaseAvailable(int pos) {
        substituteProducts.get(pos).setGrnQuantity(substituteProducts.get(pos).getGrnQuantity() - 1);
        substituteListClickListener.substituteQuantity(pos);
    }

    @Override
    public int getItemCount() {
        return substituteProducts.size();
    }


    public void selectedCustomFieldValue(int pos,String custom_field_name, String custom_field_value) {
        substituteProducts.get(pos).setGrnQuantity(substituteProducts.get(pos).getGrnQuantity() + 1);
        substituteProducts.get(pos).setCustomFieldName(custom_field_name);
        substituteProducts.get(pos).setCustomFieldValue(custom_field_value);
        substituteListClickListener.substituteQuantity(pos);
    }

    public class SubstituteListViewHolder extends RecyclerView.ViewHolder {
        ImageView ivPicSubsListRow;
        ImageView tvReturnRow;
        LinearLayout llReturnRow;
        LinearLayout llAddToCart;
        RelativeLayout tvDecreaseReturnRow;
        RelativeLayout tvIncreaseReturnRow;
        TextView tvNameSubsListRow, tvWeightSubsListRow, tvPriceSubsListRow,tvValueReturnRow;

        public SubstituteListViewHolder(@NonNull View itemView) {
            super(itemView);
            ivPicSubsListRow = itemView.findViewById(R.id.ivPicSubsListRow);
            tvNameSubsListRow = itemView.findViewById(R.id.tvNameSubsListRow);
            tvWeightSubsListRow = itemView.findViewById(R.id.tvWeightSubsListRow);
            tvPriceSubsListRow = itemView.findViewById(R.id.tvPriceSubsListRow);
            tvDecreaseReturnRow = itemView.findViewById(R.id.tvDecreaseReturnRow);
            tvIncreaseReturnRow = itemView.findViewById(R.id.tvIncreaseReturnRow);
            tvValueReturnRow = itemView.findViewById(R.id.tvValueReturnRow);
            llReturnRow = itemView.findViewById(R.id.llReturnRow);
            llAddToCart = itemView.findViewById(R.id.llAddToCart);
            tvReturnRow = itemView.findViewById(R.id.tvReturnRow);
        }
    }

    

}
