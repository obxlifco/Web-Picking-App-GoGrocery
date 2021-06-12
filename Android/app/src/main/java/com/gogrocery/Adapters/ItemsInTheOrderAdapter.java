package com.gogrocery.Adapters;

import android.content.Context;
import android.graphics.Paint;
import android.graphics.drawable.Drawable;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.DataSource;
import com.bumptech.glide.load.engine.GlideException;
import com.bumptech.glide.request.RequestListener;
import com.bumptech.glide.request.target.Target;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Models.OrderDetailsModel.OrderProduct;
import com.gogrocery.Models.OrderDetailsModel.Uom;
import com.gogrocery.view.MyOrdersDetailPage;
import com.gogrocery.R;
import com.google.gson.Gson;

import java.util.List;


public class ItemsInTheOrderAdapter extends RecyclerView.Adapter<ItemsInTheOrderAdapter.MyViewHolder> {


    private Context mContext;
    private List<OrderProduct> mOrderProductList;
    public MyViewHolder mMyViewHolderMain;
    public String argShipmentStatus="";

    public ItemsInTheOrderAdapter(Context mContext,
                                  List<OrderProduct> mOrderProductList) {

        this.mContext = mContext;
        this.mOrderProductList = mOrderProductList;

    }

    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.items_in_the_order_row, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        OrderProduct mOrderProductInner = mOrderProductList.get(position);

        mMyViewHolderMain = holder;
        try {
            mMyViewHolderMain.tvItemName.setText(mOrderProductInner.getProduct().getName());
            holder.tvDiscountedPrice.setText("Price : " + "" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderProductInner.getNewDefaultPrice())));

            if (!mOrderProductInner.getProduct().getUom().toString().isEmpty()) {

                Gson mGson = new Gson();
                Uom mUom = mGson.fromJson(mGson.toJson(mOrderProductInner.getProduct().getUom()), Uom.class);


                holder.tvProductUOM.setText("Product Unit : " + mOrderProductInner.getProduct().getWeight() + " " + mUom.getUom_name() + " x " + mOrderProductInner.getQuantity());
            } else {
                holder.tvProductUOM.setText("Product Unit : " + mOrderProductInner.getProduct().getWeight() + " " + " x " + mOrderProductInner.getQuantity());

            }
            holder.tvUnitPrice.setText("Unit Price : " + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mOrderProductInner.getNewDefaultPriceUnit())));
            if (mOrderProductInner.getCostPrice() != null || Double.parseDouble(mOrderProductInner.getCostPrice()) != 0) {
                Double getChannel_price = Double.parseDouble(mOrderProductInner.getCostPrice());
                Double getNew_default_price_unit = Double.parseDouble(mOrderProductInner.getNewDefaultPriceUnit());
                if (getChannel_price > getNew_default_price_unit) {

                    holder.tvOriginalPrice.setVisibility(View.VISIBLE);
                    holder.tvOriginalPrice.setPaintFlags(holder.tvOriginalPrice.getPaintFlags() | Paint.STRIKE_THRU_TEXT_FLAG);
                    holder.tvOriginalPrice.setText(Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(getChannel_price));


               /* if (!mOrderProductInner.getProductDiscType().isEmpty()) {
                    if (mOrderProductInner.getProductDiscType().equals("1")) // % wise
                    {
                        holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                        holder.tvDiscountOffer.setText("(" + mDataInner.getDiscount_amount() + "% OFF.)");

                    } else { // Currency wise
                        holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                        holder.tvDiscountOffer.setText("(" + Constants.VARIABLES.CURRENT_CURRENCY + " " + mDataInner.getDiscount_amount() + " OFF.)");
                    }
                }*/

                }
            }

               if(mOrderProductInner.getCustomFieldName()!=null&&mOrderProductInner.getCustomFieldValue()!=null&&!mOrderProductInner.getCustomFieldName().isEmpty()&&!mOrderProductInner.getCustomFieldValue().isEmpty()){
                holder.ll_preparationView.setVisibility(View.VISIBLE);
                holder.tvCustomFieldName.setText(mOrderProductInner.getCustomFieldName() + " :");
                holder.tvCustomFieldValue.setText(mOrderProductInner.getCustomFieldValue());
            }else {
                holder.ll_preparationView.setVisibility(View.GONE);
            }
            if (mOrderProductInner.getGrnQuantity() != null) {
                if (mOrderProductInner.getGrnQuantity() == 0 && argShipmentStatus.equals("Invoicing")) {
                    holder.tvQuantity.setTextColor(mContext.getResources().getColor(R.color.app_red_clr));
                    holder.tvQuantity.setText("Out of stock");
                } else {
                    holder.tvQuantity.setText("Quantity : " + mOrderProductInner.getQuantity());
                }
            }

            MyOrdersDetailPage.mProductId.add(mOrderProductInner.getProduct().getId());
            MyOrdersDetailPage.mProductQuantity.add(mOrderProductInner.getQuantity());
        }catch (Exception e){e.printStackTrace();}



        try {

            Glide.with(mContext)
                    .load(Constants.IMAGE_CART_URL + mOrderProductInner.getProduct().getProductImage().getImg())
                    .listener(new RequestListener<Drawable>() {

                        @Override
                        public boolean onLoadFailed(@Nullable GlideException e, Object model, Target<Drawable> target, boolean isFirstResource) {

                            new android.os.Handler().postDelayed(new Runnable() {
                                @Override
                                public void run() {
                                    Glide.with(mContext)
                                            .load(R.drawable.image_not_available)
                                            .into(holder.ivItemImage);
                                }
                            }, 100);


                            return false;
                        }

                        @Override
                        public boolean onResourceReady(Drawable resource, Object model, Target<Drawable> target, DataSource dataSource, boolean isFirstResource) {

                            return false;
                        }


                    })
                    .into(holder.ivItemImage);
        } catch (Exception e) {
            System.out.println("Rahul : GlideExceptiion : " + e.getMessage());
            Glide.with(mContext)
                    .load(R.drawable.image_not_available)
                    .into(holder.ivItemImage);
        }


    }


    @Override
    public int getItemCount() {
        return mOrderProductList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {

        private ImageView ivItemImage;
        private LinearLayout ll_preparationView;
        private TextView tvItemBrand, tvItemName, tvDiscountedPrice, tvQuantity, tvProductUOM, tvOriginalPrice, tvUnitPrice,tvCustomFieldName,tvCustomFieldValue;

        public MyViewHolder(View view) {
            super(view);


            ivItemImage = view.findViewById(R.id.ivItemImage);
            tvItemBrand = view.findViewById(R.id.tvItemBrand);
            tvItemName = view.findViewById(R.id.tvItemName);
            tvDiscountedPrice = view.findViewById(R.id.tvDiscountedPrice);
            tvProductUOM = view.findViewById(R.id.tvProductUOM);
            tvQuantity = view.findViewById(R.id.tvQuantity);
            tvOriginalPrice = view.findViewById(R.id.tvOriginalPrice);
            tvUnitPrice = view.findViewById(R.id.tvUnitPrice);
            ll_preparationView = view.findViewById(R.id.ll_preparationView);
            tvCustomFieldName = view.findViewById(R.id.tvCustomFieldName);
            tvCustomFieldValue = view.findViewById(R.id.tvCustomFieldValue);


        }

    }


}
