package com.gogrocery.Adapters;

import android.content.Context;
import android.graphics.Color;
import android.graphics.drawable.Drawable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RadioButton;
import android.widget.RelativeLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.cardview.widget.CardView;
import androidx.recyclerview.widget.RecyclerView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.DataSource;
import com.bumptech.glide.load.engine.GlideException;
import com.bumptech.glide.request.RequestListener;
import com.bumptech.glide.request.RequestOptions;
import com.bumptech.glide.request.target.Target;
import com.gogrocery.Constants.Constants;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.PaymentCardInterface;
import com.gogrocery.Models.MyCardList.Card;
import com.gogrocery.Models.ProductQuantityLocal;
import com.gogrocery.Models.ViewCartModel.Data;
import com.gogrocery.R;

import java.util.List;


public class MyCardAdapter extends RecyclerView.Adapter<MyCardAdapter.MyViewHolder> {


    private Context mContext;
    private int checkedPosition = -1;
    private List<Card> mCardList;
    private PaymentCardInterface mPaymentCardInterface;


private String from="";
    public MyCardAdapter(Context mContext,
                         List<Card> mCardList, PaymentCardInterface mPaymentCardInterface,String from) {

        this.mContext = mContext;
        this.mCardList = mCardList;
        this.mPaymentCardInterface = mPaymentCardInterface;
        this.from=from;
        System.out.println("Rahul : MyCard : MyCardAdapter : mCardList : " + mCardList.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView;
        if(from!=null&&!from.isEmpty()) {
            itemView = LayoutInflater.from(parent.getContext())
                    .inflate(R.layout.item_card_layout_payment, parent, false);
        }else {
            itemView = LayoutInflater.from(parent.getContext())
                    .inflate(R.layout.item_card_layout, parent, false);
        }

        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {

/*        try {
            if (checkedPosition == -1) {
                holder.cv_cardView.setCardBackgroundColor(Color.parseColor("#DFECC5"));
            } else {
                if (checkedPosition == position) {
                    holder.cv_cardView.setCardBackgroundColor(Color.parseColor("#98D81D"));
                    holder.tvPreferences.setTextColor(Color.parseColor("#FFFFFF"));
                   // callback.onSelectedCoupon(couponList.get(position).getCouponCode());
                } else {
                    holder.cv_cardView.setCardBackgroundColor(Color.parseColor("#DFECC5"));
                    holder.tvPreferences.setTextColor(Color.parseColor("#000000"));
                }
            }
            if(!mCardList.get(position).getSiSubRefNo().equals("0")) {
                holder.tvPreferences.setPadding(0, 0, 0, 0);
                holder.tvPreferences.setText(mCardList.get(position).getCardType() + "\n **** **** **** " + mCardList.get(position).getCardSuffix());
            }else {
                holder.tvPreferences.setPadding(0, 30, 0, 30);
                holder.tvPreferences.setText(mCardList.get(position).getCardType());

            }

        } catch (Exception e) {
            e.printStackTrace();
        }*/






        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (checkedPosition != position) {
                    notifyItemChanged(checkedPosition);
                    checkedPosition = position;
          /*          holder.cv_cardView.setCardBackgroundColor(Color.parseColor("#98D81D"));
                    holder.tvPreferences.setTextColor(Color.parseColor("#FFFFFF"));*/
                }
                mPaymentCardInterface.onSelectedCard(mCardList.get(position).getCardType() + "\n **** **** **** " + mCardList.get(position).getCardSuffix(),mCardList.get(position).getSiSubRefNo());
            }
        });


        try {

            if (checkedPosition == -1) {
                holder.rbSelection.setChecked(false);
            } else {
                if (checkedPosition == position) {
                    holder.rbSelection.setChecked(true);
                } else {
                    holder.rbSelection.setChecked(false);
                }

            }
            if(!mCardList.get(position).getSiSubRefNo().equals("0")) {
                holder.tvPreferences.setPadding(0, 0, 0, 0);
                holder.tvPreferences.setText(mCardList.get(position).getCardType() + "\n **** **** **** " + mCardList.get(position).getCardSuffix());
            }else {
                holder.tvPreferences.setPadding(0, 30, 0, 30);
                holder.tvPreferences.setText(mCardList.get(position).getCardType());

            }


            holder.itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (checkedPosition != position) {
                        notifyItemChanged(checkedPosition);
                        checkedPosition = position;
          /*          holder.cv_cardView.setCardBackgroundColor(Color.parseColor("#98D81D"));
                    holder.tvPreferences.setTextColor(Color.parseColor("#FFFFFF"));*/
                    }
                    mPaymentCardInterface.onSelectedCard(mCardList.get(position).getCardType() + "\n **** **** **** " + mCardList.get(position).getCardSuffix(),mCardList.get(position).getSiSubRefNo());

                }
            });


            holder.rbSelection.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (checkedPosition != position) {
                        notifyItemChanged(checkedPosition);
                        checkedPosition = position;
          /*          holder.cv_cardView.setCardBackgroundColor(Color.parseColor("#98D81D"));
                    holder.tvPreferences.setTextColor(Color.parseColor("#FFFFFF"));*/
                    }
                    mPaymentCardInterface.onSelectedCard(mCardList.get(position).getCardType() + "\n **** **** **** " + mCardList.get(position).getCardSuffix(),mCardList.get(position).getSiSubRefNo());


                }
            });
        } catch (Exception e) {
            System.out.println("Rahul : PreparationAdapter : Exception : " + e);
        }

    }


    @Override
    public int getItemCount() {
        return mCardList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {


        private TextView tvPreferences;
        private RadioButton rbSelection;

        public MyViewHolder(View view) {
            super(view);


            tvPreferences = view.findViewById(R.id.tvPreferences);
          //  cv_cardView = view.findViewById(R.id.cv_cardView);
            rbSelection = view.findViewById(R.id.rbSelection);

        }

    }


}
