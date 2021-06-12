package com.gogrocery.Adapters;

import android.content.Context;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Typeface;
import android.graphics.drawable.Drawable;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.content.res.ResourcesCompat;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
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
import com.bumptech.glide.request.target.Target;
import com.gogrocery.Constants.Constants;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.PrepareViewOpenInterface;
import com.gogrocery.Interfaces.WishlistInterface;
import com.gogrocery.R;
import com.gogrocery.view.WishListPage;

import java.util.ArrayList;
import java.util.List;


public class MyWishlistAdapter extends RecyclerView.Adapter<MyWishlistAdapter.MyViewHolder> {


    private Context mContext;
    private DatabaseHandler mDatabaseHandler;
    private List<com.gogrocery.Models.WishlistModel.Data> mMyWishlistData;
    private WishlistInterface mWishlistInterface;
    private PrepareViewOpenInterface mPrepareViewOpenInterface;
  //  public MyViewHolder mMyViewHolderMain;
    public LinearLayout.LayoutParams params;

    public MyWishlistAdapter(Context mContext, DatabaseHandler mDatabaseHandler, WishlistInterface mWishlistInterface,PrepareViewOpenInterface mPrepareViewOpenInterface) {

        this.mContext = mContext;
      mMyWishlistData = new ArrayList<>();
        this.mDatabaseHandler = mDatabaseHandler;
        this.mWishlistInterface = mWishlistInterface;
        this.mPrepareViewOpenInterface=mPrepareViewOpenInterface;
        System.out.println("Rahul : MyCart : MyCartAdapter : mViewCartList : " + mMyWishlistData.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {

        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.wishlist_row, parent, false);
        params = new LinearLayout.LayoutParams(0, 0);

        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        com.gogrocery.Models.WishlistModel.Data mDataInner = mMyWishlistData.get(position);

        try {

            //mMyViewHolderMain.tvItemBrand.setText(mDataInner.getProduct().getCustomField().get(0).we);
            //mMyViewHolderMain.tvQuantity.setText("" + mDataInner.getQuantity());
      /*  if (mDataInner.getProduct().getChannelPrice() == null) {
            //  mWishlistInterface.removeNullChannelPriceData(position);
            holder.itemView.setLayoutParams(params);
        } else {
            holder.tvDiscountedPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + mDataInner.getProduct().getChannelPrice().getChannelPrice());
        }*/
            holder.tvItemName.setText(mDataInner.getProduct().getName());


            holder.tvItemBrand.setText(mDataInner.getProduct().getBrand().getName());

            holder.tvDiscountedPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mDataInner.getNewDefaultPrice())));




            if (mDataInner.getProduct().getChannelPrice() != null || Double.parseDouble(mDataInner.getProduct().getChannelPrice().getChannelPrice()) != 0.0) {
                double getChannel_price = Double.parseDouble(mDataInner.getProduct().getChannelPrice().getChannelPrice());
                double getNew_default_price_unit = Double.parseDouble(mDataInner.getNewDefaultPriceUnit());
                String discountPrice=mDataInner.getDiscountAmount();
                //  if (mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice() > mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getNewDefaultPriceUnit()) {
                if (discountPrice!=null&&!discountPrice.isEmpty()&&Double.parseDouble(discountPrice) > 0.0) {
            //    if (getChannel_price > getNew_default_price_unit) {
                    holder.tvDiscountedPrice.setTextColor(Color.parseColor("#C32D4A"));
                    Typeface typeface = ResourcesCompat.getFont(mContext, R.font.proxima_bold);
                    holder.tvDiscountedPrice.setTypeface(typeface);
                    holder.tvOriginalPrice.setVisibility(View.VISIBLE);
                    holder.tvOriginalPrice.setPaintFlags(holder.tvOriginalPrice.getPaintFlags() | Paint.STRIKE_THRU_TEXT_FLAG);
                    holder.tvOriginalPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(getChannel_price));

                    if (!mDataInner.getDiscType().isEmpty()) {
                        if (mDataInner.getDiscType().equals("1")) // % wise
                        {
                            holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                            holder.tvDiscountOffer.setText( mDataInner.getDiscountAmount() + mContext.getResources().getString(R.string._pen_off));

                        } else { // Currency wise
                            holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                            holder.tvDiscountOffer.setText( Constants.VARIABLES.CURRENT_CURRENCY + " " + mDataInner.getDiscountAmount() + mContext.getResources().getString(R.string._off));
                        }
                    }

                }else {
                    holder.tvOriginalPrice.setVisibility(View.GONE);
                    holder.tvDiscountOffer.setVisibility(View.GONE);
                    holder.tvDiscountedPrice.setTextColor(Color.parseColor("#2E6B0B"));
                    Typeface typeface = ResourcesCompat.getFont(mContext, R.font.proxima_regular);
                    holder.tvDiscountedPrice.setTypeface(typeface);
                }
            }
        }catch (Exception e){e.printStackTrace();}





       /* if (mDataInner.getDefaultPrice() != null) {
            holder.tvDiscountedPrice.setText("$" + mDataInner.getNewDefaultPrice());
        }*/

       /* if(!mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(mDataInner.getId())).equals("0"))
        {

            holder.tvQuantity.setText(""+mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(mDataInner.getId())));
        }
*/

        if (mDatabaseHandler.CheckIsDataAlreadyInDBorNot(String.valueOf(mDataInner.getProduct().getId()))) {
            holder.btnAddToCart.setVisibility(View.GONE);
            holder.llAddToCart.setVisibility(View.VISIBLE);
            holder.tvQuantity.setText("" + mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(mDataInner.getProduct().getId())));
        } else {
            holder.btnAddToCart.setVisibility(View.VISIBLE);
            holder.llAddToCart.setVisibility(View.GONE);
        }
        holder.btnAddToCart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                   /* holder.btnAddToCart.setVisibility(View.INVISIBLE);
                    holder.llAddToCart.setVisibility(View.VISIBLE);*/


                        /*  holder.btnAddToCart.setVisibility(View.GONE);
                    holder.llAddToCart.setVisibility(View.VISIBLE);
                    bsp_itemClick_interface.connectMain(mDataInner.getProduct().getId(), 1);*/

                if(mDataInner.getProduct().getCustomField()!=null&&!mDataInner.getProduct().getCustomField().isEmpty()&&mDataInner.getProduct().getCustomField().size()>0) {
                     /*   holder.btnAddToCart.setVisibility(View.GONE);
                        holder.llAddToCart.setVisibility(View.VISIBLE);*/
                    if(mDataInner.getProduct().getCustomField().size()>0) {
                        String custom_field_name = mDataInner.getProduct().getCustomField().get(0).getFieldName();
                        String custom_field_value = mDataInner.getProduct().getCustomField().get(0).getValue();
                        mPrepareViewOpenInterface.customFieldValueSelect(mDataInner.getProduct().getId(), 1, custom_field_name, custom_field_value,position);
                    }

                }else {
                      /*  holder.btnAddToCart.setVisibility(View.GONE);
                        holder.llAddToCart.setVisibility(View.VISIBLE);*/
                    mWishlistInterface.connectMain(mDataInner.getProduct().getId(), 1,position);
                }

              //  mWishlistInterface.connectMain(mDataInner.getProduct().getId(), 1,position);

            }
        });

        try {

            Glide.with(mContext)
                    .load(Constants.IMAGE_CART_URL + mDataInner.getProduct().getProductImage().get(0).getImg())
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




        holder.rlPlus.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int qty = Integer.parseInt(holder.tvQuantity.getText().toString());
                System.out.println("Rahul : MyCardAdapter : rlMinus : qty : " + qty);
                holder.tvQuantity.setText("" + (qty + 1));

                  mWishlistInterface.connectMain(mDataInner.getProduct().getId(), Integer.parseInt(holder.tvQuantity.getText().toString().trim()), position);

            }
        });

        holder.rlMinus.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                int qty = Integer.parseInt(holder.tvQuantity.getText().toString());
                System.out.println("Rahul : MyCardAdapter : rlMinus : qty : " + qty);
                if (qty == 1) {
                    holder.llAddToCart.setVisibility(View.GONE);
                    holder.btnAddToCart.setVisibility(View.VISIBLE);
                     mWishlistInterface.connectMain(mDataInner.getProduct().getId(), 0, position);

                } else {
                    holder.tvQuantity.setText("" + (qty - 1));
                    mWishlistInterface.connectMain(mDataInner.getProduct().getId(), Integer.parseInt(holder.tvQuantity.getText().toString().trim()), position);

                }


            }
        });

        holder.ivRemove.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mWishlistInterface.removeItemFromWishlist(mDataInner.getProduct().getId(), position);
            }
        });


        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mWishlistInterface.connectToDetail(mDataInner.getProduct().getId(), mDataInner.getProduct().getSlug() + "#GoGrocery#" + mDataInner.getProduct().getName());
            }
        });

       /* if (!mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(mDataInner.getProduct().getId())).equals("0")) {
            mDatabaseHandler.updateProductQuantityById(mProductQuantityLocal);
        } else {
            mDatabaseHandler.addProductQty(mProductQuantityLocal);
        }*/
    }


    @Override
    public int getItemCount() {
        return mMyWishlistData.size();
    }


    public static class MyViewHolder extends RecyclerView.ViewHolder {

        private ImageView ivItemImage, ivVeg, ivWishList, ivSaveList;
        private TextView tvItemBrand, tvItemName, tvGrams, tvPrice, tvDiscountedPrice, tvOriginalPrice, tvDiscountOffer, tvUOM;
        private ImageView btnAddToCart;
        private ImageView ivRemove;
        private AutoCompleteTextView actvVariant;
        private LinearLayout llAddToCart;
        private RelativeLayout rlMinus;
        private RelativeLayout rlPlus;
        private EditText tvQuantity;
        public MyViewHolder(View view) {
            super(view);

            ivItemImage = view.findViewById(R.id.ivItemImage);
            tvItemBrand = view.findViewById(R.id.tvItemBrand);
            tvItemName = view.findViewById(R.id.tvItemName);
            tvUOM = view.findViewById(R.id.tvUOM);
            // tvGrams = view.findViewById(R.id.tvGrams);
            tvPrice = view.findViewById(R.id.tvPrice);
            tvDiscountedPrice = view.findViewById(R.id.tvDiscountedPrice);
            tvOriginalPrice = view.findViewById(R.id.tvOriginalPrice);
            tvDiscountOffer = view.findViewById(R.id.tvDiscountOffer);
            actvVariant = view.findViewById(R.id.actvVariant);
            ivVeg = view.findViewById(R.id.ivVeg);
            btnAddToCart = view.findViewById(R.id.ivAddCart);
            ivRemove = view.findViewById(R.id.ivRemove);
            llAddToCart = view.findViewById(R.id.llAddToCart);
            rlMinus = view.findViewById(R.id.rlMinus);
            rlPlus = view.findViewById(R.id.rlPlus);
            tvQuantity = view.findViewById(R.id.etQuantity);
            //ivWishList = view.findViewById(R.id.ivWishList);
            ivSaveList = view.findViewById(R.id.ivSavelist);

        }

    }

    public void addAllWishList(List<com.gogrocery.Models.WishlistModel.Data> mMyWishlistData) {
        this.mMyWishlistData.addAll(mMyWishlistData);
    }

    public void clearWishList() {
        if (mMyWishlistData != null) {
            this.mMyWishlistData.clear();
        }
    }


}
