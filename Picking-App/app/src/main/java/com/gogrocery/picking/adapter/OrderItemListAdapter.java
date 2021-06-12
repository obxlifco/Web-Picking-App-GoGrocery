package com.gogrocery.picking.adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.afollestad.materialdialogs.MaterialDialog;
import com.bumptech.glide.Glide;
import com.gogrocery.picking.R;
import com.gogrocery.picking.prefrences.AppPreferences;
import com.gogrocery.picking.response_pojo.order_detail_pojo.OrderProductsItem;
import com.gogrocery.picking.utils.AppUtilities;

import java.text.DecimalFormat;
import java.util.List;

import androidx.annotation.NonNull;
import androidx.core.content.ContextCompat;
import androidx.recyclerview.widget.RecyclerView;

public class OrderItemListAdapter extends RecyclerView.Adapter<OrderItemListAdapter.OrderItemViewHolder> {
    Context context;
    OrderListItemClickListener orderListItemClickListener;
    List<OrderProductsItem> orderProducts;
    int orderStatus;
    DecimalFormat formater = new DecimalFormat("0.00");

    public OrderItemListAdapter(Context context, List<OrderProductsItem> orderProducts, int orderStatus, OrderListItemClickListener orderListItemClickListener) {
        this.context = context;
        this.orderListItemClickListener = orderListItemClickListener;
        this.orderProducts = orderProducts;
        this.orderStatus = orderStatus;
    }

    @NonNull
    @Override
    public OrderItemViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(context).inflate(R.layout.row_item_order_list, parent, false);
        return new OrderItemViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull OrderItemViewHolder holder, int position) {
        orderListItemClickListener.orderListItemProcessCheck(orderProducts);
        if (orderProducts.get(position).getProduct().getProductImages().size() > 0) {
            Glide.with(context).load(orderProducts.get(position).getProduct().getProductImages().get(0).getLink() +
                    orderProducts.get(position).getProduct().getProductImages().get(0).getImg())
                    .placeholder(R.drawable.ic_product_default).into(holder.ivPicItemRow);
        }
        holder.tvNameItemRow.setText(orderProducts.get(position).getProduct().getName());
        holder.tvQtyItemRow.setText((orderProducts.get(position).getQuantity() - orderProducts.get(position).getReturns()) + "");
        holder.tvPriceItemRow.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(orderProducts.get(position).getProductPrice()) + "");
        holder.tvTotalPriceItemRow.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(orderProducts.get(position).getProductPrice() * orderProducts.get(position).getGrnQuantity()) + "");
        if (orderProducts.get(position).getWeight() == null || orderProducts.get(position).getWeight() == 0) {
            holder.tvWeightItemRow.setText("");
            holder.tvUnitWeightItemRow.setText("");
            holder.tvEditWeightOrderListRow.setVisibility(View.GONE);
            holder.llEditWeightOrderListRow.setVisibility(View.GONE);
            holder.llUnitWeightItemRow.setVisibility(View.GONE);
            holder.llWeightItemRow.setVisibility(View.GONE);
        } else {
           /* holder.tvWeightItemRow.setText((orderProducts.get(position).getWeight().intValue() * (orderProducts.get(position).getQuantity() - orderProducts.get(position).getReturns())) + " " +
                    orderProducts.get(position).getProduct().getUom().getUomName());*///Old
            holder.tvWeightItemRow.setText(AppUtilities.removeTrailingZero(AppUtilities.twoDecimalRoundOff(orderProducts.get(position).getWeight() * (orderProducts.get(position).getQuantity() - orderProducts.get(position).getReturns()))) + " " +
                    orderProducts.get(position).getProduct().getUom().getUomName());
           // holder.tvUnitWeightItemRow.setText((orderProducts.get(position).getWeight().intValue() + " " +orderProducts.get(position).getProduct().getUom().getUomName()));//old
            holder.tvUnitWeightItemRow.setText((AppUtilities.removeTrailingZero(AppUtilities.twoDecimalRoundOff(orderProducts.get(position).getWeight())) + " " +orderProducts.get(position).getProduct().getUom().getUomName()));
            holder.tvEditWeightOrderListRow.setVisibility(View.VISIBLE);
            holder.llEditWeightOrderListRow.setVisibility(View.VISIBLE);
            holder.llUnitWeightItemRow.setVisibility(View.VISIBLE);
            holder.llWeightItemRow.setVisibility(View.VISIBLE);
            /*if (checkCategory(position)) {
                *//*holder.tvWeightItemRow.setText((orderProducts.get(position).getWeight().intValue() * (orderProducts.get(position).getQuantity() - orderProducts.get(position).getReturns())) + " " +
                        orderProducts.get(position).getProduct().getUom().getUomName());*//*
                holder.tvEditWeightOrderListRow.setVisibility(View.VISIBLE);
            } else {
                //holder.tvWeightItemRow.setText("");
                holder.tvEditWeightOrderListRow.setVisibility(View.GONE);
            }*/
        }
        holder.tvValueAvail.setText(orderProducts.get(position).getGrnQuantity() + "");
        holder.tvValueNotAvail.setText(orderProducts.get(position).getShortage() + "");
        if(orderProducts.get(position).getProduct().getSku()!=null&&!orderProducts.get(position).getProduct().getSku().isEmpty()){
            holder.llSkuItemRow.setVisibility(View.VISIBLE);
            holder.tvSkuItemRow.setText(orderProducts.get(position).getProduct().getSku());
        }else {
            holder.llSkuItemRow.setVisibility(View.GONE);
        }
        if(orderProducts.get(position).getProduct().getEan()!=null&&!orderProducts.get(position).getProduct().getEan().isEmpty()){
            holder.llBarcodeItemRow.setVisibility(View.VISIBLE);
            holder.tvBarcodeItemRow.setText(orderProducts.get(position).getProduct().getEan());
        }else {
            holder.tvBarcodeItemRow.setText(orderProducts.get(position).getProduct().getSku());
            holder.llBarcodeItemRow.setVisibility(View.VISIBLE);
        }


        if ((orderProducts.get(position).getQuantity() - orderProducts.get(position).getReturns()) <= orderProducts.get(position).getShortage() +
                orderProducts.get(position).getGrnQuantity()) {
            holder.llDoneRowItemList.setVisibility(View.VISIBLE);
        } else {
            holder.llDoneRowItemList.setVisibility(View.GONE);
        }
        if(orderProducts.get(position).getPickAsSubstitute().equalsIgnoreCase("n")){
            holder.tvIsSubsItemRow.setVisibility(View.GONE);
        }else{
            holder.tvIsSubsItemRow.setVisibility(View.VISIBLE);
        }

        if(orderProducts.get(position).getCustomFieldName()!=null&&orderProducts.get(position).getCustomFieldValue()!=null&&!orderProducts.get(position).getCustomFieldName().isEmpty()&&!orderProducts.get(position).getCustomFieldValue().isEmpty()){
            holder.llCustomFieldRow.setVisibility(View.VISIBLE);
         //   holder.tv_custom_field_name.setText(orderProducts.get(position).getCustomFieldName() + ":");
            holder.tv_custom_field_name.setText( "Prep Options :");
            holder.tv_custom_field_value.setText(orderProducts.get(position).getCustomFieldValue());
            holder.llCustomFieldRow.setOnClickListener(v->{
                showPrepOptionPopup(orderProducts.get(position).getCustomFieldName() + ":",orderProducts.get(position).getCustomFieldValue());
            });
        }else {
            holder.llCustomFieldRow.setVisibility(View.GONE);
        }
    }




    private boolean checkCategory(int position) {
        boolean isWeightable = false;
        for (int i = 0; i < orderProducts.get(position).getProduct_all_category().size(); i++) {
            if (orderProducts.get(position).getProduct_all_category().get(i).contains("Meats") ||
                    orderProducts.get(position).getProduct_all_category().get(i).contains("Dairies") ||
                    orderProducts.get(position).getProduct_all_category().get(i).contains("Vegetables") ||
                    orderProducts.get(position).getProduct_all_category().get(i).contains("Fruits") ||
                    orderProducts.get(position).getProduct_all_category().get(i).contains("Herbs")) {
                isWeightable = true;
            }
        }
        return isWeightable;
    }

    @Override
    public int getItemCount() {
        return orderProducts.size();
    }

    public class OrderItemViewHolder extends RecyclerView.ViewHolder {
        LinearLayout llDoneRowItemList, llNotAvailable,llWeightItemRow,llUnitWeightItemRow,llEditWeightOrderListRow,llCustomFieldRow,llSkuItemRow,llBarcodeItemRow;
        TextView tvValueNotAvail, tvEditWeightOrderListRow, tvNameItemRow, tvPriceItemRow, tvWeightItemRow,tvUnitWeightItemRow, tvQtyItemRow,
                tvDecreaseAvail, tvIncreaseAvail, tvValueAvail, tvDecreaseNotAvail, tvIncreaseNotAvail, tvTotalPriceItemRow,tvIsSubsItemRow,tv_custom_field_value,tv_custom_field_name,tvSkuItemRow,tvBarcodeItemRow;
        ImageView ivPicItemRow;

        public OrderItemViewHolder(@NonNull View itemView) {
            super(itemView);
            llDoneRowItemList = itemView.findViewById(R.id.llDoneRowItemList);
            llNotAvailable = itemView.findViewById(R.id.llNotAvailable);
            tvValueNotAvail = itemView.findViewById(R.id.tvValueNotAvail);
            ivPicItemRow = itemView.findViewById(R.id.ivPicItemRow);
            tvNameItemRow = itemView.findViewById(R.id.tvNameItemRow);
            tvPriceItemRow = itemView.findViewById(R.id.tvPriceItemRow);
            tvTotalPriceItemRow = itemView.findViewById(R.id.tvTotalPriceItemRow);
            tvWeightItemRow = itemView.findViewById(R.id.tvWeightItemRow);
            tvUnitWeightItemRow = itemView.findViewById(R.id.tvUnitWeightItemRow);
            tvQtyItemRow = itemView.findViewById(R.id.tvQtyItemRow);
            tvDecreaseAvail = itemView.findViewById(R.id.tvDecreaseAvail);
            tvIncreaseAvail = itemView.findViewById(R.id.tvIncreaseAvail);
            tvValueAvail = itemView.findViewById(R.id.tvValueAvail);
            tvValueNotAvail = itemView.findViewById(R.id.tvValueNotAvail);
            tvIsSubsItemRow = itemView.findViewById(R.id.tvIsSubsItemRow);
            tvSkuItemRow = itemView.findViewById(R.id.tvSkuItemRow);
            llWeightItemRow = itemView.findViewById(R.id.llWeightItemRow);
            llUnitWeightItemRow = itemView.findViewById(R.id.llUnitWeightItemRow);

            tvEditWeightOrderListRow = itemView.findViewById(R.id.tvEditWeightOrderListRow);
            llEditWeightOrderListRow = itemView.findViewById(R.id.llEditWeightOrderListRow);
            tvDecreaseNotAvail = itemView.findViewById(R.id.tvDecreaseNotAvail);
            tvIncreaseNotAvail = itemView.findViewById(R.id.tvIncreaseNotAvail);
            tv_custom_field_name = itemView.findViewById(R.id.tv_custom_field_name);
            tv_custom_field_value = itemView.findViewById(R.id.tv_custom_field_value);
            llCustomFieldRow = itemView.findViewById(R.id.llCustomFieldRow);
            llSkuItemRow = itemView.findViewById(R.id.llSkuItemRow);
            tvBarcodeItemRow = itemView.findViewById(R.id.tvBarcodeItemRow);
            llBarcodeItemRow = itemView.findViewById(R.id.llBarcodeItemRow);
            itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    if (orderStatus == 100 && orderProducts.get(getAdapterPosition()).getPickAsSubstitute().equalsIgnoreCase("n")) {
                        orderListItemClickListener.orderListItemClick(getAdapterPosition());
                    }
                }
            });
            /*llNotAvailable.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    if (orderStatus==100) {
                        if (Integer.parseInt(tvValueNotAvail.getText().toString()) == 0) {
                            orderListItemClickListener.openAddSubstitute(getAdapterPosition());
                        }
                    }
                }
            });*/
            llEditWeightOrderListRow.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    if (orderStatus == 100 && orderProducts.get(getAdapterPosition()).getPickAsSubstitute().equalsIgnoreCase("n")) {
                        orderListItemClickListener.editItemWeightClick(getAdapterPosition());
                    }
                }
            });
            /*tvPriceItemRow.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    if (orderStatus == 100 && orderProducts.get(getAdapterPosition()).getPickAsSubstitute().equalsIgnoreCase("n")) {
                        orderListItemClickListener.editItemPriceClick(getAdapterPosition());
                    }
                }
            });*/
            tvDecreaseAvail.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    if (orderStatus == 100 && orderProducts.get(getAdapterPosition()).getPickAsSubstitute().equalsIgnoreCase("n")) {
                        if (orderProducts.get(getAdapterPosition()).getGrnQuantity() > 0) {
                            decreaseAvailable(getAdapterPosition());
                            //notifyDataSetChanged();
                        }
                    }
                }
            });
            tvIncreaseAvail.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    if (orderStatus == 100 && orderProducts.get(getAdapterPosition()).getPickAsSubstitute().equalsIgnoreCase("n")) {
                        if ((orderProducts.get(getAdapterPosition()).getQuantity() - orderProducts.get(getAdapterPosition()).getReturns())
                                > orderProducts.get(getAdapterPosition()).getShortage() +
                                orderProducts.get(getAdapterPosition()).getGrnQuantity()) {
                            increaseAvailable(getAdapterPosition());
                            //notifyDataSetChanged();
                        }

                    }
                }
            });
            tvDecreaseNotAvail.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    if (orderStatus == 100 && orderProducts.get(getAdapterPosition()).getPickAsSubstitute().equalsIgnoreCase("n")) {
                        if (orderProducts.get(getAdapterPosition()).getShortage() > 0) {
                            decreaseShortage(getAdapterPosition());
                            //notifyDataSetChanged();
                        }
                    }
                }
            });
            tvIncreaseNotAvail.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    if (orderStatus == 100 && orderProducts.get(getAdapterPosition()).getPickAsSubstitute().equalsIgnoreCase("n")) {
                        if ((orderProducts.get(getAdapterPosition()).getQuantity() - orderProducts.get(getAdapterPosition()).getReturns()) > orderProducts.get(getAdapterPosition()).getShortage() +
                                orderProducts.get(getAdapterPosition()).getGrnQuantity()) {
                            orderListItemClickListener.openAddSubstitute(getAdapterPosition());
                        }

                    }
                }
            });
        }
    }

    public void increaseAvailable(int pos) {
        orderProducts.get(pos).setGrnQuantity(orderProducts.get(pos).getGrnQuantity() + 1);
        orderListItemClickListener.updateGRNShortage(pos, false);
    }

    public void decreaseAvailable(int pos) {
        orderProducts.get(pos).setGrnQuantity(orderProducts.get(pos).getGrnQuantity() - 1);
        orderListItemClickListener.updateGRNShortage(pos, false);
    }

    public void increaseShortage(int pos) {
        orderProducts.get(pos).setShortage(orderProducts.get(pos).getShortage() + 1);
    }

    public void decreaseShortage(int pos) {
        orderProducts.get(pos).setShortage(orderProducts.get(pos).getShortage() - 1);
        orderListItemClickListener.updateGRNShortage(pos, true);
    }

    public void setOrderStatus(int status) {
        this.orderStatus = status;
    }

    public interface OrderListItemClickListener {
        public void orderListItemClick(int position);

        public void openAddSubstitute(int position);

        public void editItemWeightClick(int position);

        public void editItemPriceClick(int position);

        public void updateGRNShortage(int position, Boolean isShortage);

        public void orderListItemProcessCheck(List<OrderProductsItem> orderProducts);
    }



    private void showPrepOptionPopup(String prepOption,String PreType) {
        new MaterialDialog.Builder(context)
                .title(prepOption)
                .content(PreType)
                .positiveText("Ok")
                .titleColor(ContextCompat.getColor(context, R.color.appGreen))
                .positiveColor(ContextCompat.getColor(context, R.color.appGreen))
                .contentColor(ContextCompat.getColor(context, R.color.appColorDarkGrey))

                .onPositive((dialog, which) -> {
                    dialog.dismiss();

                }).show();
    }

}
