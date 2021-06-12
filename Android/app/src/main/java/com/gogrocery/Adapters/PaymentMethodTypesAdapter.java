package com.gogrocery.Adapters;

import android.content.Context;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RadioButton;
import android.widget.RelativeLayout;
import android.widget.TextView;

import com.gogrocery.Interfaces.CountryStateListListner;
import com.gogrocery.Interfaces.PaymentMethodTypesInterface;
import com.gogrocery.Models.PaymentTypesModel.ApiStatus;
import com.gogrocery.Models.PaymentTypesModel.EngageboostPaymentgatewayMethodId;
import com.gogrocery.R;

import java.util.List;


public class PaymentMethodTypesAdapter extends RecyclerView.Adapter<PaymentMethodTypesAdapter.MyViewHolder> {


    private Context mContext;
    private List<ApiStatus> mApiStatusList;
    private int lastSelected = -1;
    private PaymentMethodTypesInterface mPaymentMethodTypesInterface;
    private boolean isCardSaved;


    public PaymentMethodTypesAdapter(Context mContext,
                                     List<ApiStatus> mApiStatusList, PaymentMethodTypesInterface mPaymentMethodTypesInterface) {

        this.mContext = mContext;
        this.mApiStatusList = mApiStatusList;
        this.mPaymentMethodTypesInterface = mPaymentMethodTypesInterface;

        System.out.println("Rahul : PaymentMethodTypesAdapter : mApiStatusList : " + mApiStatusList.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.payment_options_type_row, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {


        holder.rbPaymentType.setText(mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getName());
        if (lastSelected == -1) {
            holder.rbPaymentType.setChecked(false);
        } else {
            if (lastSelected == position) {
                holder.rbPaymentType.setChecked(true);
                if (isCardSaved) {
                    holder.tv_instruction.setVisibility(View.GONE);
                } else {
                    holder.tv_instruction.setVisibility(View.VISIBLE);

                }

            } else {
                holder.rbPaymentType.setChecked(false);
                holder.tv_instruction.setVisibility(View.GONE);
            }
        }


        holder.rlPaymentType.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (lastSelected != position) {
                    notifyItemChanged(lastSelected);
                    lastSelected = position;
                }

//                lastSelected = position;
                if (mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getId() == 51) {
                    if (holder.rbPaymentType.isClickable()) {
                        if (isCardSaved) {
                            holder.tv_instruction.setVisibility(View.GONE);
                        } else {
                            holder.tv_instruction.setVisibility(View.VISIBLE);

                        }

                    } else {
                        holder.tv_instruction.setVisibility(View.GONE);
                    }


                    mPaymentMethodTypesInterface.selectPaymentMethod("card", "" + mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getId(), "" + mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getPaymentgatewayTypeId(), mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getName());

                } else if (mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getId() == 16) {
                    holder.tv_instruction.setVisibility(View.GONE);


                    mPaymentMethodTypesInterface.selectPaymentMethod("cash", "" + mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getId(), "" + mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getPaymentgatewayTypeId(), mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getName());

                } else if (mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getId() == 59) {
                    holder.tv_instruction.setVisibility(View.GONE);


                    mPaymentMethodTypesInterface.selectPaymentMethod("card_on_delivery", "" + mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getId(), "" + mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getPaymentgatewayTypeId(), mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getName());

                }

            }
        });

        holder.rbPaymentType.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (lastSelected != position) {
                    notifyItemChanged(lastSelected);
                    lastSelected = position;
                }

                if (mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getId() == 51) {

                    if (holder.rbPaymentType.isClickable()) {

                        if (isCardSaved) {
                            holder.tv_instruction.setVisibility(View.GONE);
                        } else {
                            holder.tv_instruction.setVisibility(View.VISIBLE);

                        }
                    } else {
                        holder.tv_instruction.setVisibility(View.GONE);
                    }

                    mPaymentMethodTypesInterface.selectPaymentMethod("card", "" + mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getId(), "" + mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getPaymentgatewayTypeId(), mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getName());

                } else if (mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getId() == 16) {
                    holder.tv_instruction.setVisibility(View.GONE);


                    mPaymentMethodTypesInterface.selectPaymentMethod("cash", "" + mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getId(), "" + mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getPaymentgatewayTypeId(), mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getName());

                } else if (mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getId() == 59) {
                    holder.tv_instruction.setVisibility(View.GONE);

                    mPaymentMethodTypesInterface.selectPaymentMethod("card_on_delivery", "" + mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getId(), "" + mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getPaymentgatewayTypeId(), mApiStatusList.get(position).getEngageboostPaymentgatewayMethodId().getName());

                }
            }
        });


    }


    @Override
    public int getItemCount() {
        return mApiStatusList.size();
    }


    public static class MyViewHolder extends RecyclerView.ViewHolder {


        private RadioButton rbPaymentType;
        private RelativeLayout rlPaymentType;
        private TextView tv_instruction;


        public MyViewHolder(View view) {
            super(view);


            rbPaymentType = view.findViewById(R.id.rbPaymentType);
            rlPaymentType = view.findViewById(R.id.rlPaymentType);
            tv_instruction = view.findViewById(R.id.tv_instruction);

        }

    }

    public void isAlreadySavedCard(boolean isCardSaved) {
        this.isCardSaved = isCardSaved;
    }


}
