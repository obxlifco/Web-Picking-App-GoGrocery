package com.gogrocery.Adapters;

import android.content.Context;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.drawable.Drawable;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.DataSource;
import com.bumptech.glide.load.engine.GlideException;
import com.bumptech.glide.request.RequestListener;
import com.bumptech.glide.request.RequestOptions;
import com.bumptech.glide.request.target.Target;
import com.gogrocery.Constants.Constants;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.CartItemInterface;
import com.gogrocery.Models.ProductQuantityLocal;
import com.gogrocery.Models.ViewCartModel.Data;
import com.gogrocery.R;

import java.util.List;


public class MyCartAdapter extends RecyclerView.Adapter<MyCartAdapter.MyViewHolder> {


    private Context mContext;
    private DatabaseHandler mDatabaseHandler;
    private List<Data> mViewCartList;
    private CartItemInterface mCartItemInterface;
    private int row_index = -1;


    public MyCartAdapter(Context mContext,
                         List<Data> mViewCartList, DatabaseHandler mDatabaseHandler, CartItemInterface mCartItemInterface) {

        this.mContext = mContext;
        this.mViewCartList = mViewCartList;
        this.mCartItemInterface = mCartItemInterface;
        this.mDatabaseHandler = mDatabaseHandler;
        System.out.println("Rahul : MyCart : MyCartAdapter : mViewCartList : " + mViewCartList.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.my_cart_row, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        Data mDataInner = mViewCartList.get(position);

        try {
            holder.tvItemName.setText(mDataInner.getProductName());
            if (mDataInner.getProductId().getBrand().size() != 0) {
                holder.tvItemBrand.setText(mDataInner.getProductId().getBrand().get(0).getName());
            } else {
                holder.tvItemBrand.setVisibility(View.GONE);
            }


            holder.etQuantity.setText("" + mDataInner.getQuantity());
            holder.tvDiscountedPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mDataInner.getNewDefaultPrice())));
            //holder.tvItemWeight.setText(""+mDataInner.get());
            if ((mDataInner.getWeight() != null && !mDataInner.getWeight().isEmpty() )|| (mDataInner.getUnit() != null&&!mDataInner.getUnit().isEmpty())) {
                holder.tvItemWeight.setVisibility(View.VISIBLE);
                holder.tvItemWeight.setText(mDataInner.getWeight() + " " + mDataInner.getUnit());
            } else {
                holder.tvItemWeight.setVisibility(View.INVISIBLE);
            }

            if (mDataInner.getProductId().getChannel_price() != null || Double.parseDouble(mDataInner.getProductId().getChannel_price()) != 0) {
                Double getChannel_price = Double.parseDouble(mDataInner.getProductId().getChannel_price());
                Double getNew_default_price_unit = Double.parseDouble(mDataInner.getNewDefaultPriceUnit());
                if (getChannel_price > getNew_default_price_unit) {

            /*holder.tvOriginalPrice.setVisibility(View.VISIBLE);
            holder.tvOriginalPrice.setPaintFlags(holder.tvOriginalPrice.getPaintFlags() | Paint.STRIKE_THRU_TEXT_FLAG);
            holder.tvOriginalPrice.setText(""+Constants.VARIABLES.CURRENT_CURRENCY+" "+Constants.twoDecimalRoundOff(getChannel_price));*/

              /*  if (!mDataInner.getDisc_type().isEmpty()) {
                    if (mDataInner.getDisc_type().equals("1")) // % wise
                    {
                        holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                        holder.tvDiscountOffer.setText("(" + mDataInner.getDiscountAmount() + "% OFF.)");

                    } else { // Currency wise
                        holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                        holder.tvDiscountOffer.setText("(" + Constants.VARIABLES.CURRENT_CURRENCY + " " +mDataInner.getDiscountAmount() + " OFF.)");
                    }
                }
*/
                }
            }

            if(mDataInner.getCustomFieldName()!=null&&mDataInner.getCustomFieldValue()!=null&&!mDataInner.getCustomFieldName().isEmpty()&&!mDataInner.getCustomFieldValue().isEmpty()){
                holder.ll_preparationView.setVisibility(View.VISIBLE);
                holder.tvCustomFieldName.setText(mDataInner.getCustomFieldName() + " :");
                holder.tvCustomFieldValue.setText(mDataInner.getCustomFieldValue());
            }else {
                holder.ll_preparationView.setVisibility(View.GONE);
            }
       /* if (mDataInner.getDefaultPrice() != null) {
            holder.tvDiscountedPrice.setText("$" + mDataInner.getNewDefaultPrice());
        }*/

            System.out.println("Rahul : MyCart : MyCartAdapter : onBindViewHolder : getProductName : " + mDataInner.getProductName());

       /* if(!mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(mDataInner.getId())).equals("0"))
        {

            holder.etQuantity.setText(""+mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(mDataInner.getId())));
        }
*/
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {

            Glide.with(mContext)
                    .load(Constants.IMAGE_CART_URL + mDataInner.getProductId().getProductImage().getImg())
                    .apply(new RequestOptions().override(100, 100))
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

        /*holder.itemView.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                row_index=position;
                //notifyDataSetChanged();
                return false;
            }
        });

        if(row_index==position){
            holder.rlMain.setBackground(mContext.getResources().getDrawable(R.drawable.bg_search));
        }else{
            holder.rlMain.setBackground(mContext.getResources().getDrawable(R.drawable.bg_white_round_corner));
        }*/


        holder.rlPlus.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int qty = Integer.parseInt(holder.etQuantity.getText().toString());
                System.out.println("Rahul : MyCardAdapter : rlMinus : qty : " + qty);
                holder.etQuantity.setText("" + (qty + 1));

                mCartItemInterface.connectCartMain(mDataInner.getProductId().getId(), Integer.parseInt(holder.etQuantity.getText().toString().trim()), position);

            }
        });

        holder.rlMinus.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                int qty = Integer.parseInt(holder.etQuantity.getText().toString());
                System.out.println("Rahul : MyCardAdapter : rlMinus : qty : " + qty);
                if (qty == 1) {
                    mCartItemInterface.connectCartMain(mDataInner.getProductId().getId(), 0, position);

                } else {
                    holder.etQuantity.setText("" + (qty - 1));
                    mCartItemInterface.connectCartMain(mDataInner.getProductId().getId(), Integer.parseInt(holder.etQuantity.getText().toString().trim()), position);

                }


            }
        });

        ProductQuantityLocal mProductQuantityLocal = new ProductQuantityLocal(String.valueOf(mDataInner.getProductId().getId()), String.valueOf(mDataInner.getQuantity()));
        if (!mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(mDataInner.getProductId().getId())).equals("0")) {
            mDatabaseHandler.updateProductQuantityById(mProductQuantityLocal);
        } else {
            mDatabaseHandler.addProductQty(mProductQuantityLocal);
        }

        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mCartItemInterface.connectCartToDetail(mDataInner.getProductId().getId(), mDataInner.getProductId().getSlug() + "#GoGrocery#" + mDataInner.getProductName());
            }
        });
    }


    @Override
    public int getItemCount() {
        return mViewCartList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {

        private ImageView ivItemImage;
        private TextView tvItemBrand, tvItemName, tvItemWeight, tvPrice, tvDiscountedPrice, tvOriginalPrice, tvDiscountOffer,tvCustomFieldName,tvCustomFieldValue;
        EditText etQuantity;
        private Button btnAddToCart;
        private AutoCompleteTextView actvVariant;
        private LinearLayout llAddToCart;
        private LinearLayout ll_preparationView;
        private RelativeLayout rlMinus,rlMain;
        private RelativeLayout rlPlus;

        public MyViewHolder(View view) {
            super(view);


            ivItemImage = view.findViewById(R.id.ivItemImage);
            tvItemBrand = view.findViewById(R.id.tvItemBrand);
            tvItemName = view.findViewById(R.id.tvItemName);
            tvItemWeight = view.findViewById(R.id.tvItemWeight);
            tvPrice = view.findViewById(R.id.tvPrice);
            tvDiscountedPrice = view.findViewById(R.id.tvDiscountedPrice);
            tvOriginalPrice = view.findViewById(R.id.tvOriginalPrice);
            ll_preparationView = view.findViewById(R.id.ll_preparationView);
            //   tvDiscountOffer = view.findViewById(R.id.tvDiscountOffer);
          /*  actvVariant = view.findViewById(R.id.actvVariant);
            ivVeg = view.findViewById(R.id.ivVeg);*/
            //btnAddToCart = view.findViewById(R.id.btnAddToCart);
            llAddToCart = view.findViewById(R.id.llAddToCart);
            rlMinus = view.findViewById(R.id.rlMinus);
            rlPlus = view.findViewById(R.id.rlPlus);
            etQuantity = view.findViewById(R.id.etQuantity);
            rlMain = view.findViewById(R.id.rlMain);
            tvCustomFieldName = view.findViewById(R.id.tvCustomFieldName);
            tvCustomFieldValue = view.findViewById(R.id.tvCustomFieldValue);

        }

    }


}
