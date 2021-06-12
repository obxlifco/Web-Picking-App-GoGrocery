package com.gogrocery.Adapters;

import android.content.Context;
import android.graphics.drawable.Drawable;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
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
import com.gogrocery.Interfaces.SaveListDetailInterface;
import com.gogrocery.Models.SaveListDetailPage.SaveListDetailListData;
import com.gogrocery.R;

import java.util.List;


public class SaveListDetailPageAdapter extends RecyclerView.Adapter<SaveListDetailPageAdapter.MyViewHolder> {


    private Context mContext;
    private DatabaseHandler mDatabaseHandler;
    private List<SaveListDetailListData> mMyWishlistData;
    private SaveListDetailInterface mWishlistInterface;
   // private MyViewHolder mMyViewHolderMain;
    public LinearLayout.LayoutParams params;

    public SaveListDetailPageAdapter(Context mContext,
                                     List<SaveListDetailListData> mMyWishlistData, DatabaseHandler mDatabaseHandler, SaveListDetailInterface mWishlistInterface) {

        this.mContext = mContext;
        this.mMyWishlistData = mMyWishlistData;
        this.mDatabaseHandler = mDatabaseHandler;
        this.mWishlistInterface = mWishlistInterface;
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
        SaveListDetailListData mDataInner = mMyWishlistData.get(position);


try {
    holder.tvItemName.setText(mDataInner.getName());
    // mMyViewHolderMain.tvItemBrand.setText(mDataInner.getProduct().getBrand().getName());
    //mMyViewHolderMain.tvQuantity.setText("" + mDataInner.getQuantity());
      /*  if (mDataInner.getProduct().getChannelPrice() == null) {
            //  mWishlistInterface.removeNullChannelPriceData(position);
            holder.itemView.setLayoutParams(params);
        } else {
            holder.tvDiscountedPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + mDataInner.getProduct().getChannelPrice().getChannelPrice());
        }*/
    holder.tvDiscountedPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff((mDataInner.getProduct().getProductPrice())));


       /* if (mDataInner.getDefaultPrice() != null) {
            holder.tvDiscountedPrice.setText("$" + mDataInner.getNewDefaultPrice());
        }*/

    if (!mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(mDataInner.getId())).equals("0")) {

        holder.tvQuantity.setText("" + mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(mDataInner.getId())));
        holder.btnAddToCart.setVisibility(View.INVISIBLE);
        holder.llAddToCart.setVisibility(View.VISIBLE);
    }else {
        holder.btnAddToCart.setVisibility(View.VISIBLE);
        holder.llAddToCart.setVisibility(View.INVISIBLE);
    }

}catch (Exception e){
    e.printStackTrace();
}

        holder.btnAddToCart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                   /* holder.btnAddToCart.setVisibility(View.INVISIBLE);
                    holder.llAddToCart.setVisibility(View.VISIBLE);*/
                mWishlistInterface.connectMain(mDataInner.getId(), 1, position);

            }
        });

        try {

            Glide.with(mContext)
                    .load(Constants.IMAGE_CART_URL + mDataInner.getProductImage().get(0).getImg())
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

                mWishlistInterface.connectMain(mDataInner.getId(), Integer.parseInt(holder.tvQuantity.getText().toString().trim()), position);

            }
        });

        holder.rlMinus.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                int qty = Integer.parseInt(holder.tvQuantity.getText().toString());
                System.out.println("Rahul : MyCardAdapter : rlMinus : qty : " + qty);
                if (qty == 1) {
                    mWishlistInterface.connectMain(mDataInner.getId(), 0, position);

                } else {
                    holder.tvQuantity.setText("" + (qty - 1));
                    mWishlistInterface.connectMain(mDataInner.getId(), Integer.parseInt(holder.tvQuantity.getText().toString().trim()), position);

                }


            }
        });

        holder.ivRemove.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mWishlistInterface.removeItemFromWishlist(mDataInner.getId(), mDataInner.getSavelistId(), position);
            }
        });


        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mWishlistInterface.connectToDetail(mDataInner.getProduct().getId(), mDataInner.getSlug() + "#GoGrocery#" + mDataInner.getName());
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


    public class MyViewHolder extends RecyclerView.ViewHolder {

        private ImageView ivItemImage, ivRemove;
        private TextView tvItemBrand, tvItemName, tvGrams, tvPrice, tvDiscountedPrice, tvOriginalPrice, tvDiscountOffer, tvQuantity;
        private Button btnAddToCart;
        private AutoCompleteTextView actvVariant;
        private LinearLayout llAddToCart;
        private RelativeLayout rlMinus;
        private RelativeLayout rlPlus;

        public MyViewHolder(View view) {
            super(view);


            ivItemImage = view.findViewById(R.id.ivItemImage);
            tvItemBrand = view.findViewById(R.id.tvItemBrand);
            tvItemName = view.findViewById(R.id.tvItemName);
            tvGrams = view.findViewById(R.id.tvGrams);
            tvPrice = view.findViewById(R.id.tvPrice);
            tvDiscountedPrice = view.findViewById(R.id.tvDiscountedPrice);
            tvOriginalPrice = view.findViewById(R.id.tvOriginalPrice);
            //     tvDiscountOffer = view.findViewById(R.id.tvDiscountOffer);
          /*  actvVariant = view.findViewById(R.id.actvVariant);
            ivVeg = view.findViewById(R.id.ivVeg);*/
            btnAddToCart = view.findViewById(R.id.btnAddToCart);
            ivRemove = view.findViewById(R.id.ivRemove);
            llAddToCart = view.findViewById(R.id.llAddToCart);
            rlMinus = view.findViewById(R.id.rlMinus);
            rlPlus = view.findViewById(R.id.rlPlus);
            tvQuantity = view.findViewById(R.id.tvQuantity);

        }

    }


}
