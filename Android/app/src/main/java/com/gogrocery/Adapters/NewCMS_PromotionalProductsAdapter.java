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
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.DataSource;
import com.bumptech.glide.load.engine.DiskCacheStrategy;
import com.bumptech.glide.load.engine.GlideException;
import com.bumptech.glide.request.RequestListener;
import com.bumptech.glide.request.target.Target;
import com.gogrocery.Constants.Constants;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.BSP_ItemClick_Interface;
import com.gogrocery.Interfaces.ProductListingInterface;
import com.gogrocery.Models.CMS_NEW_Model.Product;
import com.gogrocery.R;

import java.util.List;


public class NewCMS_PromotionalProductsAdapter extends RecyclerView.Adapter<NewCMS_PromotionalProductsAdapter.MyViewHolder> {


    private Context mContext;
    private List<Product> mPromotionalProductList;
    private DatabaseHandler mDatabaseHandler;
    private BSP_ItemClick_Interface bsp_itemClick_interface;
    private ProductListingInterface mProductListingInterface;
    private LinearLayout.LayoutParams params;

    public NewCMS_PromotionalProductsAdapter(Context mContext,
                                             List<Product> mPromotionalProductList, BSP_ItemClick_Interface bsp_itemClick_interface,
                                             DatabaseHandler mDatabaseHandler, ProductListingInterface mProductListingInterface) {

        this.mContext = mContext;
        this.mPromotionalProductList = mPromotionalProductList;
        this.bsp_itemClick_interface = bsp_itemClick_interface;
        this.mDatabaseHandler = mDatabaseHandler;
        this.mProductListingInterface = mProductListingInterface;
        System.out.println("Rahul : NewCMS_PromotionalProductsAdapter : mPromotionalProductList : " + mPromotionalProductList.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.deals_of_the_day_row, parent, false);
        params = new LinearLayout.LayoutParams(0, 0);

        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        Product mProductInner = mPromotionalProductList.get(position);
        String[] variant;

        holder.tvItemName.setText(mProductInner.getName());
        if (mProductInner.getWeight() != null || !mProductInner.getUom().isEmpty()) {
            holder.tvUOM.setText(mProductInner.getWeight() + " " + mProductInner.getUom());
        }

        if (mProductInner.getBrand() != null) {
            if (mProductInner.getBrandName() != null) {
                holder.tvItemBrand.setVisibility(View.VISIBLE);
                holder.tvItemBrand.setText(mProductInner.getBrandName());
            } else {
                holder.tvItemBrand.setVisibility(View.INVISIBLE);
            }
        } else {
            holder.tvItemBrand.setVisibility(View.INVISIBLE);
        }

        if (mProductInner.getDefaultPrice() != null) {
            holder.tvDiscountedPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mProductInner.getNew_default_price_unit().trim())));
        } else {
            holder.itemView.setLayoutParams(params);
        }

        if (mProductInner.getVegNonvegType() != null) {
            if (!mProductInner.getVegNonvegType().equals("veg")) {
                holder.ivVeg.setVisibility(View.INVISIBLE);
            } else {
                holder.ivVeg.setVisibility(View.VISIBLE);
            }
        }

        if (mDatabaseHandler.CheckIsDataAlreadyInDBorNot(String.valueOf(mProductInner.getId()))) {
            holder.btnAddToCart.setVisibility(View.INVISIBLE);
            holder.llAddToCart.setVisibility(View.VISIBLE);
            holder.tvQuantity.setText("" + mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(mProductInner.getId())));
        } else {
            holder.btnAddToCart.setVisibility(View.VISIBLE);
            holder.llAddToCart.setVisibility(View.INVISIBLE);
        }


        if (mProductInner.getChannel_price() != null || Double.parseDouble(mProductInner.getChannel_price()) != 0) {
            Double getChannel_price = Double.parseDouble(mProductInner.getChannel_price());
            Double getNew_default_price_unit = Double.parseDouble(mProductInner.getNew_default_price_unit());
            if (getChannel_price > getNew_default_price_unit) {

                holder.tvOriginalPrice.setVisibility(View.VISIBLE);
                holder.tvOriginalPrice.setPaintFlags(holder.tvOriginalPrice.getPaintFlags() | Paint.STRIKE_THRU_TEXT_FLAG);
                holder.tvOriginalPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + getChannel_price);

                if (!mProductInner.getDisc_type().isEmpty()) {
                    if (mProductInner.getDisc_type().equals("1")) // % wise
                    {
                        holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                        holder.tvDiscountOffer.setText("(" + mProductInner.getDiscount_amount() + "% OFF.)");

                    } else { // Currency wise
                        holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                        holder.tvDiscountOffer.setText("(" + Constants.VARIABLES.CURRENT_CURRENCY + " " + mProductInner.getDiscount_amount() + " OFF.)");
                    }
                }

            }
        }

       /* if (mDataInner.getVariantProduct().size() >= 1) {
            variant = new String[mDataInner.getVariantProduct().size() + 1];


        } else {
            variant = new String[1];
        }*/
        variant = new String[1];
        variant[0] = mProductInner.getName();
        /*for (int i = 1; i < mDataInner.getVariantProduct().size(); i++) {
            variant[i] = mDataInner.getVariantProduct().get(i).getName();

        }*/
        setDropdownVariant(holder.actvVariant, variant);

        try {
            System.out.println("Rahul : DealsOfTheDayAdapter : IMAGE_BASE_URL : " + Constants.IMAGE_BASE_URL + mProductInner.getProductImage().get(0).getImg());
            Glide.with(mContext)
                    .load(Constants.IMAGE_BASE_URL + "400x400/" + mProductInner.getProductImage().get(0).getImg())
                    .diskCacheStrategy(DiskCacheStrategy.NONE) .skipMemoryCache(true)
                    .listener(new RequestListener<Drawable>() {

                        @Override
                        public boolean onLoadFailed(@Nullable GlideException e, Object model, Target<Drawable> target, boolean isFirstResource) {

                           /* new android.os.Handler().postDelayed(new Runnable() {
                                @Override
                                public void run() {
                                    Glide.with(mContext)
                                            .load(R.drawable.image_not_available)
                                            .into(holder.ivItemImage);
                                }
                            }, 100);
*/

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
                    .diskCacheStrategy(DiskCacheStrategy.NONE) .skipMemoryCache(true)
                    .into(holder.ivItemImage);
        }
        holder.btnAddToCart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                holder.btnAddToCart.setVisibility(View.INVISIBLE);
                holder.llAddToCart.setVisibility(View.VISIBLE);
                bsp_itemClick_interface.connectMain(mProductInner.getId(), 1,position);

            }
        });


        holder.rlPlus.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int qty = Integer.parseInt(holder.tvQuantity.getText().toString());
                holder.tvQuantity.setText("" + (qty + 1));
                bsp_itemClick_interface.connectMain(mProductInner.getId(), Integer.parseInt(holder.tvQuantity.getText().toString().trim()),position);

            }
        });

        holder.rlMinus.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                int qty = Integer.parseInt(holder.tvQuantity.getText().toString());
                if (qty == 1) {
                    holder.llAddToCart.setVisibility(View.INVISIBLE);
                    holder.btnAddToCart.setVisibility(View.VISIBLE);
                    bsp_itemClick_interface.connectMain(mProductInner.getId(), 0,position);
                } else {
                    holder.tvQuantity.setText("" + (qty - 1));
                    bsp_itemClick_interface.connectMain(mProductInner.getId(), Integer.parseInt(holder.tvQuantity.getText().toString().trim()),position);

                }


            }
        });

        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mProductListingInterface.sendSlug(mProductInner.getSlug() + "#GoGrocery#" + mProductInner.getName(), mProductInner.getId());
            }
        });

      /*  holder.ivWishList.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                if (mDatabaseHandler.checkWishlistAvailable("" + mProductInner.getId())) {
                    mProductListingInterface.sendProductIdForWishlist(mProductInner.getId(), "remove");
                } else {
                    mProductListingInterface.sendProductIdForWishlist(mProductInner.getId(), "add");
                }

            }
        });

        try {
            if (mDatabaseHandler.checkWishlistAvailable("" + mProductInner.getId())) {
                holder.ivWishList.setBackground(mContext.getResources().getDrawable(R.drawable.wishlist_added));

            } else {
                holder.ivWishList.setBackground(mContext.getResources().getDrawable(R.drawable.wishlist));

            }
        } catch (Exception e) {
            holder.ivWishList.setBackground(mContext.getResources().getDrawable(R.drawable.wishlist));
        }*/

        holder.ivSaveList.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mProductListingInterface.savelist(String.valueOf(mProductInner.getId()));

            }
        });
    }

    private void setDropdownVariant(AutoCompleteTextView mAutoCompleteTextView, String[] argVartiantName) {

        ArrayAdapter adapter = new
                ArrayAdapter(mContext, android.R.layout.simple_list_item_1, argVartiantName);

        mAutoCompleteTextView.setAdapter(adapter);

        System.out.println("Rahul : DealsOfTheDayAdapter : setDropdownVariant : argVartiantName : " + argVartiantName.toString());
        mAutoCompleteTextView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                System.out.println("Rautocomplete : " + argVartiantName[i]);
              /*  mVehicleType = argCarTypeID[i];
                mCategoryId = argCarTypeID[i];
                mAutoCompleteTextView.setError(null);
                mPassingVehicleType = argCarType[i];*/
            }
        });


        mAutoCompleteTextView.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                mAutoCompleteTextView.setEnabled(false);
                mAutoCompleteTextView.dismissDropDown();

                System.out.println("Rautocomplete : " + argVartiantName[i]);

            }

            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {

            }
        });

       /* mAutoCompleteTextView.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
                switch (motionEvent.getAction()) {
                    case MotionEvent.ACTION_UP: {
                        //   getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_HIDDEN);

                        mAutoCompleteTextView.setEnabled(true);
                        mAutoCompleteTextView.showDropDown();
                    }
                }

                return true;
            }
        });*/
        mAutoCompleteTextView.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                if (hasFocus) {
                    // mAutoCompleteTextView.setEnabled(true);
                    mAutoCompleteTextView.showDropDown();
                }
            }
        });

        mAutoCompleteTextView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // mAutoCompleteTextView.setEnabled(true);
                mAutoCompleteTextView.showDropDown();
            }
        });
    }

    @Override
    public int getItemCount() {
        return mPromotionalProductList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {

        private ImageView ivItemImage, ivVeg, ivWishList, ivSaveList;
        private TextView tvItemBrand, tvItemName, tvGrams, tvPrice, tvDiscountedPrice, tvOriginalPrice, tvDiscountOffer, tvQuantity, tvUOM;
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
            tvDiscountOffer = view.findViewById(R.id.tvDiscountOffer);
            actvVariant = view.findViewById(R.id.actvVariant);
            ivVeg = view.findViewById(R.id.ivVeg);
            btnAddToCart = view.findViewById(R.id.btnAddToCart);
            llAddToCart = view.findViewById(R.id.llAddToCart);
            rlMinus = view.findViewById(R.id.rlMinus);
            rlPlus = view.findViewById(R.id.rlPlus);
            tvQuantity = view.findViewById(R.id.tvQuantity);
            ivWishList = view.findViewById(R.id.ivWishList);
            ivSaveList = view.findViewById(R.id.ivSavelist);
            tvUOM = view.findViewById(R.id.tvUOM);

        }

    }


}
