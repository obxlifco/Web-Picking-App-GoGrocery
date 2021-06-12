package com.gogrocery.picking.adapter;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.gogrocery.picking.R;
import com.gogrocery.picking.prefrences.AppPreferences;
import com.gogrocery.picking.response_pojo.order_list_pojo.OrderListItem;
import com.gogrocery.picking.utils.AppUtilities;

import java.text.DecimalFormat;
import java.text.ParseException;
import java.util.List;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

public class OrderListAdapter extends RecyclerView.Adapter<OrderListAdapter.OrderListViewHolder> {
    Context context;
    OrderListClickListener orderListClickListener;
    List<OrderListItem> orderListItem;
    int row_index = 0;
    DecimalFormat formater = new DecimalFormat("0.00");

    public OrderListAdapter(Context context, List<OrderListItem> orderListItem, OrderListClickListener orderListClickListener) {
        this.context = context;
        this.orderListItem = orderListItem;
        this.orderListClickListener = orderListClickListener;
    }

    @NonNull
    @Override
    public OrderListViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(context).inflate(R.layout.row_order_list, parent, false);
        return new OrderListViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull OrderListViewHolder holder, int position) {
        if (orderListItem.get(position).getOrderStatus() == 0) {
            holder.tvOrdIdStatusRowOrdList.setText(orderListItem.get(position).getCustomOrderId() + " - " +
                    context.getResources().getString(R.string.txtPending));
            holder.tvOrdIdStatusRowOrdList.setBackground(context.getResources().getDrawable(R.drawable.bg_red_round_corner));
            //holder.llScheduleRowOrdList.setVisibility(View.VISIBLE);
            holder.llAssignRowOrdList.setVisibility(View.GONE);
            holder.tvScheduleTimeRowOrdList.setText(orderListItem.get(position).getTimeSlotId());
            try {
                holder.tvScheduleDateRowOrdList.setText(AppUtilities.getFormattedDate(AppUtilities.formatDate(
                        orderListItem.get(position).getTimeSlotDate(), "yyyy-MM-dd", "MM-dd-yyyy")));
            } catch (ParseException e) {
                e.printStackTrace();
            }
        } else if (orderListItem.get(position).getOrderStatus() == 100) {

            if(orderListItem.get(position).getSubstitute_status().equalsIgnoreCase("pending")){
                holder.tvOrdIdStatusRowOrdList.setBackground(context.getResources().getDrawable(R.drawable.bg_light_blue_round_corner));
                holder.tvOrdIdStatusRowOrdList.setText(orderListItem.get(position).getCustomOrderId() + " - " +
                        context.getResources().getString(R.string.txtInSubsOut));
            }else if(orderListItem.get(position).getSubstitute_status().equalsIgnoreCase("done")){
                holder.tvOrdIdStatusRowOrdList.setBackground(context.getResources().getDrawable(R.drawable.bg_dark_blue_round_corner));
                holder.tvOrdIdStatusRowOrdList.setText(orderListItem.get(position).getCustomOrderId() + " - " +
                        context.getResources().getString(R.string.txtSubsIn));
            }else{
                holder.tvOrdIdStatusRowOrdList.setBackground(context.getResources().getDrawable(R.drawable.bg_green_round_corner));
                holder.tvOrdIdStatusRowOrdList.setText(orderListItem.get(position).getCustomOrderId() + " - " +
                        context.getResources().getString(R.string.txtInProcessing));
            }
            //holder.llScheduleRowOrdList.setVisibility(View.GONE);
            holder.llAssignRowOrdList.setVisibility(View.VISIBLE);
            //holder.tvAssigneeNameRowOrdList.setText();

        } else if (orderListItem.get(position).getOrderStatus() == 1) {
            holder.tvOrdIdStatusRowOrdList.setText(orderListItem.get(position).getCustomOrderId() + " - " +
                    context.getResources().getString(R.string.txtInShipping));
            holder.tvOrdIdStatusRowOrdList.setBackground(context.getResources().getDrawable(R.drawable.bg_silver_round_corner));
            //holder.llScheduleRowOrdList.setVisibility(View.VISIBLE);
            holder.llAssignRowOrdList.setVisibility(View.VISIBLE);
            holder.tvScheduleTimeRowOrdList.setText(orderListItem.get(position).getTimeSlotId());
            try {
                holder.tvScheduleDateRowOrdList.setText(AppUtilities.getFormattedDate(AppUtilities.formatDate(
                        orderListItem.get(position).getTimeSlotDate(), "yyyy-MM-dd", "MM-dd-yyyy")));
            } catch (ParseException e) {
                e.printStackTrace();
            }

        }else if (orderListItem.get(position).getOrderStatus() == 2) {
            holder.tvOrdIdStatusRowOrdList.setText(orderListItem.get(position).getCustomOrderId() + " - " +
                    context.getResources().getString(R.string.txtCancelled));
            holder.tvOrdIdStatusRowOrdList.setBackground(context.getResources().getDrawable(R.drawable.bg_purple_round_corner));
            //holder.llScheduleRowOrdList.setVisibility(View.VISIBLE);
            holder.llAssignRowOrdList.setVisibility(View.GONE);
            holder.tvScheduleTimeRowOrdList.setText(orderListItem.get(position).getTimeSlotId());
            try {
                holder.tvScheduleDateRowOrdList.setText(AppUtilities.getFormattedDate(AppUtilities.formatDate(
                        orderListItem.get(position).getTimeSlotDate(), "yyyy-MM-dd", "MM-dd-yyyy")));
            } catch (ParseException e) {
                e.printStackTrace();
            }

        }
        StringBuilder strAddress = new StringBuilder();
        if (orderListItem.get(position).getDeliveryName() != null && orderListItem.get(position).getDeliveryName().length() > 0) {
            strAddress.append(orderListItem.get(position).getDeliveryName() + ", ");
        }

        if (orderListItem.get(position).getDeliveryStreetAddress() != null && orderListItem.get(position).getDeliveryStreetAddress().length() > 0) {
            strAddress.append(orderListItem.get(position).getDeliveryStreetAddress() + ", ");
        }
        if (orderListItem.get(position).getDeliveryLandmark()!= null && orderListItem.get(position).getDeliveryLandmark().length() > 0) {
            strAddress.append(orderListItem.get(position).getDeliveryLandmark() + ", ");
        }
        if (orderListItem.get(position).getDeliveryStreetAddress1() != null && orderListItem.get(position).getDeliveryStreetAddress1().length() > 0) {
            strAddress.append(orderListItem.get(position).getDeliveryStreetAddress1() + ", ");
        }
        if (orderListItem.get(position).getDeliveryCity() != null && orderListItem.get(position).getDeliveryCity().length() > 0) {
            strAddress.append(orderListItem.get(position).getDeliveryCity() + ", ");
        }
        if (orderListItem.get(position).getDeliveryPostcode() != null && orderListItem.get(position).getDeliveryPostcode().length() > 0) {
            strAddress.append(orderListItem.get(position).getDeliveryPostcode() + ", ");
        }
        if (orderListItem.get(position).getDeliveryStateName() != null && orderListItem.get(position).getDeliveryStateName().length() > 0) {
            strAddress.append(orderListItem.get(position).getDeliveryStateName() + ", ");
        }
        try {
            if (orderListItem.get(position).getOrderShipment().getCreatedByName() == null) {
                holder.tvAssigneeNameRowOrdList.setText(orderListItem.get(position).getPicker_name());
            } else {
                holder.tvAssigneeNameRowOrdList.setText(orderListItem.get(position).getOrderShipment().getCreatedByName());
            }
            holder.tvTimeRowOrdList.setText(AppUtilities.convertUTCToTimeFormat(orderListItem.get(position).getCreated()));
            holder.tvAddressRowOrdList.setText(strAddress.toString().substring(0, strAddress.toString().length() - 2));
            holder.tvPayMethodRowOrdList.setText(orderListItem.get(position).getPaymentMethodName());
            holder.tvPriceRowOrdList.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(orderListItem.get(position).getGrossAmount()));
            holder.tvOrderTimeRowOrdList.setText(AppUtilities.getFormattedDate(AppUtilities.convertUTCToDateFormat(orderListItem.get(position).getCreated())) + "\n" +
                    AppUtilities.convertUTCToTimeFormatWithAM(orderListItem.get(position).getCreated()));
            String[] strDiff = AppUtilities.calculateDifferenceBWDateTime(
                    AppUtilities.convertUTCToNewFormat(orderListItem.get(position).getCreated()),
                    AppUtilities.getCurrentDateTime()
            ).split(",");
            if (strDiff[0].length() > 0 && !strDiff[0].contains("0")) {
                holder.tvElapseTimeRowOrdList.setText(strDiff[0] + " " + context.getResources().getString(R.string.txtDay) +
                        " " + strDiff[1] + " " + context.getResources().getString(R.string.txtHoursAgo));
            } else {
                holder.tvElapseTimeRowOrdList.setText(strDiff[1] + " " + context.getResources().getString(R.string.txtHoursAgo));
            }
        } catch (ParseException e) {
            e.printStackTrace();
        }
        Log.e("position", "---" + position);
        if (row_index == position) {
            holder.llStatusRowOrdList.setBackground(context.getDrawable(R.drawable.bg_rect_dark_select_round_corner));
        } else {
            holder.llStatusRowOrdList.setBackground(context.getDrawable(R.drawable.bg_rect_dark_round_corner));
        }

    }

    @Override
    public int getItemCount() {
        return orderListItem.size();
    }

    public class OrderListViewHolder extends RecyclerView.ViewHolder {
        TextView tvOrdIdStatusRowOrdList, tvTimeRowOrdList, tvElapseTimeRowOrdList, tvScheduleTimeRowOrdList, tvAddressRowOrdList,
                tvAssigneeNameRowOrdList, tvPriceRowOrdList, tvPayMethodRowOrdList, tvOrderTimeRowOrdList, tvScheduleDateRowOrdList;
        LinearLayout llScheduleRowOrdList, llAssignRowOrdList, llStatusRowOrdList;

        public OrderListViewHolder(@NonNull View itemView) {
            super(itemView);
            tvOrdIdStatusRowOrdList = itemView.findViewById(R.id.tvOrdIdStatusRowOrdList);
            tvTimeRowOrdList = itemView.findViewById(R.id.tvTimeRowOrdList);
            tvElapseTimeRowOrdList = itemView.findViewById(R.id.tvElapseTimeRowOrdList);
            llScheduleRowOrdList = itemView.findViewById(R.id.llScheduleRowOrdList);
            tvScheduleTimeRowOrdList = itemView.findViewById(R.id.tvScheduleTimeRowOrdList);
            tvAddressRowOrdList = itemView.findViewById(R.id.tvAddressRowOrdList);
            llAssignRowOrdList = itemView.findViewById(R.id.llAssignRowOrdList);
            tvAssigneeNameRowOrdList = itemView.findViewById(R.id.tvAssigneeNameRowOrdList);
            tvPriceRowOrdList = itemView.findViewById(R.id.tvPriceRowOrdList);
            tvPayMethodRowOrdList = itemView.findViewById(R.id.tvPayMethodRowOrdList);
            tvOrderTimeRowOrdList = itemView.findViewById(R.id.tvOrderTimeRowOrdList);
            llStatusRowOrdList = itemView.findViewById(R.id.llStatusRowOrdList);
            tvScheduleDateRowOrdList = itemView.findViewById(R.id.tvScheduleDateRowOrdList);
            itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    row_index = getAdapterPosition();
                    orderListClickListener.orderListClick(getAdapterPosition());
                    notifyDataSetChanged();
                }
            });
        }
    }

    public interface OrderListClickListener {
        public void orderListClick(int position);
    }
}
