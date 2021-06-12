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
import com.github.ybq.android.spinkit.SpinKitView;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.BSP_ItemClick_Interface;
import com.gogrocery.Interfaces.ProductListingInterface;
import com.gogrocery.Models.ElasticSearch.Hit;

import java.util.List;

import com.gogrocery.R;


public class ProductListingAdapter extends RecyclerView.Adapter<RecyclerView.ViewHolder> {


    private Context mContext;
    private List<Hit> mProductItemListing;
    private ProductListingInterface mProductListingInterface;
    private static final int TYPE_ITEM = 0;
    private static final int TYPE_FOOTER = 1;
    private BSP_ItemClick_Interface bsp_itemClick_interface;
    public SpinKitView mSpinKitView;
    private DatabaseHandler mDatabaseHandler;
    private SharedPreferenceManager mSharedPreferenceManager;
    private LinearLayout.LayoutParams params;

    public ProductListingAdapter(Context mContext, List<Hit> mProductItemListing, ProductListingInterface mProductListingInterface, BSP_ItemClick_Interface bsp_itemClick_interface, DatabaseHandler mDatabaseHandler) {
        this.mContext = mContext;
        this.mProductItemListing = mProductItemListing;
        this.mProductListingInterface = mProductListingInterface;
        this.mDatabaseHandler = mDatabaseHandler;
        this.bsp_itemClick_interface = bsp_itemClick_interface;
        System.out.println("Rahul : ItemListingAdapter : mProductItemListing : " + mProductItemListing.size());
        mSharedPreferenceManager = new SharedPreferenceManager(mContext);
    }

    @NonNull
    @Override
    public RecyclerView.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {

        params = new LinearLayout.LayoutParams(0, 0);
        if (viewType == TYPE_ITEM) {
            View itemView = LayoutInflater.from(parent.getContext())
                    .inflate(R.layout.item_listing_row, parent, false);
            return new MyViewHolder(itemView);
        } else if (viewType == TYPE_FOOTER) {
            //Inflating footer view
            View itemView = LayoutInflater.from(parent.getContext()).inflate(R.layout.layout_loading, parent, false);
            return new FooterViewHolder(itemView);
        } else return null;

    }

    @Override
    public void onBindViewHolder(@NonNull RecyclerView.ViewHolder argholder, int position) {

        final boolean[] isImageError = {false};
        if (argholder instanceof MyViewHolder) {
            MyViewHolder holder = (MyViewHolder) argholder;

            Hit mHitInner = mProductItemListing.get(position);
            String[] variant;

            holder.tvItemName.setText(mHitInner.getSource().getName());
            if (mHitInner.getSource().getWeight() != null || !mHitInner.getSource().getUnit().isEmpty()) {
                holder.tvUOM.setVisibility(View.VISIBLE);
                holder.tvUOM.setText(mHitInner.getSource().getWeight() + " " + mHitInner.getSource().getUnit());
            }else{
                holder.tvUOM.setVisibility(View.INVISIBLE);
            }

            if (mHitInner.getSource().getBrand() != null) {
                if (mHitInner.getSource().getBrand() != null) {
                    holder.tvItemBrand.setVisibility(View.VISIBLE);
                    holder.tvItemBrand.setText(mHitInner.getSource().getBrand());
                } else {
                    holder.tvItemBrand.setVisibility(View.INVISIBLE);
                }
            } else {
                holder.tvItemBrand.setVisibility(View.INVISIBLE);
            }

            boolean isWarehouseAvailable = false;
            if (mHitInner.getSource().getChannelCurrencyProductPrice().size() > 0) {
                //System.out.println("Rahul : ProductListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : size : " + mHitInner.getSource().getChannelCurrencyProductPrice().size());
                for (int i = 0; i < mHitInner.getSource().getChannelCurrencyProductPrice().size(); i++) {
                   /* System.out.println("Rahul : ProductListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : 1 : " + mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getWarehouseId());
                    System.out.println("Rahul : ProductListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : 2 : " + mSharedPreferenceManager.getWarehouseId());
*/
                    if (mSharedPreferenceManager.getWarehouseId().equals(String.valueOf(mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getWarehouseId()))&&(mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPriceType().equalsIgnoreCase("1"))) {
                        System.out.println("Rahul : ProductListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : 3 : "+mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice());
                        /*if (mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice() != null) {
                            holder.tvDiscountedPrice.setText("$" + mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice());
                        } else {
                            holder.tvDiscountedPrice.setText("$0.00");
                        }*/
//                        if(mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPriceType().equalsIgnoreCase("1"))
                        isWarehouseAvailable = true;
                        holder.tvDiscountedPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getNewDefaultPriceUnit()));
                        System.out.println("Rahul : ProductListingAdapter : mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice() : " + mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice());

                        System.out.println("Rahul : ProductListingAdapter : mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getNewDefaultPriceUnit() : " + mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getNewDefaultPriceUnit());

                        if (mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice() > mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getNewDefaultPriceUnit()) {
                            holder.tvOriginalPrice.setVisibility(View.VISIBLE);
                            holder.tvOriginalPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice()));
                            holder.tvOriginalPrice.setPaintFlags(holder.tvOriginalPrice.getPaintFlags() | Paint.STRIKE_THRU_TEXT_FLAG);

                            if (!mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getDiscType().isEmpty()) {
                                if (mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getDiscType().equals("1")) // % wise
                                {
                                    holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                                    holder.tvDiscountOffer.setText("(" + mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getDiscountAmount() + "% OFF.)");

                                } else { // Currency wise
                                    holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                                    holder.tvDiscountOffer.setText("(" + Constants.VARIABLES.CURRENT_CURRENCY + " " + mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getDiscountAmount() + " OFF.)");
                                }
                            }

                        }
                    }
                }
                if (!isWarehouseAvailable) {
                    // holder.itemView.setLayoutParams(params);
                }
            }


            if (mHitInner.getSource().getVegNonvegType() != null) {
                if (!mHitInner.getSource().getVegNonvegType().equals("veg")) {
                    holder.ivVeg.setVisibility(View.GONE);
                } else {
                    holder.ivVeg.setVisibility(View.VISIBLE);
                }
            }

            if (mDatabaseHandler.CheckIsDataAlreadyInDBorNot(String.valueOf(mHitInner.getId()))) {
                holder.btnAddToCart.setVisibility(View.INVISIBLE);
                holder.llAddToCart.setVisibility(View.VISIBLE);
                holder.tvQuantity.setText("" + mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(mHitInner.getId())));
            } else {
                holder.btnAddToCart.setVisibility(View.VISIBLE);
                holder.llAddToCart.setVisibility(View.INVISIBLE);
            }
       /* if (mDataInner.getVariantProduct().size() >= 1) {
            variant = new String[mDataInner.getVariantProduct().size() + 1];


        } else {
            variant = new String[1];
        }*/
            variant = new String[1];
            variant[0] = mHitInner.getSource().getName();
        /*for (int i = 1; i < mDataInner.getVariantProduct().size(); i++) {
            variant[i] = mDataInner.getVariantProduct().get(i).getName();

        }*/

            /*if(mDataInner.getChannel_price()!=null||Double.parseDouble(mDataInner.getChannel_price())!=0)
            {
                Double getChannel_price= Double.parseDouble(mDataInner.getChannel_price());
                Double getNew_default_price_unit= Double.parseDouble(mDataInner.getNew_default_price_unit());
                if(getChannel_price>getNew_default_price_unit)
                {
                    holder.tvOriginalPrice.setPaintFlags(holder.tvOriginalPrice.getPaintFlags() | Paint.STRIKE_THRU_TEXT_FLAG);

                }
            }*/
            //setDropdownVariant(holder.actvVariant, variant);

            try {

                for (int i = 0; i < mHitInner.getSource().getProductImages().size(); i++) {
                    if (mHitInner.getSource().getProductImages().get(i).getIsCover() == 1) {
                        System.out.println("Rahul : ProductListingAdapter : ProductName : " + mHitInner.getSource().getName());
                        System.out.println("Rahul : ProductListingAdapter : ImageLink : " + mHitInner.getSource().getProductImages().get(i).getLink() + mHitInner.getSource().getProductImages().get(i).getImg());
                        Glide.with(mContext)
                                .load(mHitInner.getSource().getProductImages().get(i).getLink() + mHitInner.getSource().getProductImages().get(i).getImg())
                                .listener(new RequestListener<Drawable>() {

                                    @Override
                                    public boolean onLoadFailed(@Nullable GlideException e, Object model, Target<Drawable> target, boolean isFirstResource) {

                                        new android.os.Handler().postDelayed(new Runnable() {
                                            @Override
                                            public void run() {
                                                Glide.with(mContext)
                                                        .load(R.drawable.image_not_available)
                                                        //.apply(new RequestOptions().override(400, 400))
                                                        .into(holder.ivItemImage);
                                                //isImageError[0] = true;
                                            }
                                        }, 10);


                                        return false;
                                    }

                                    @Override
                                    public boolean onResourceReady(Drawable resource, Object model, Target<Drawable> target, DataSource dataSource, boolean isFirstResource) {

                                        return false;
                                    }


                                })
                                .diskCacheStrategy(DiskCacheStrategy.NONE) .skipMemoryCache(true)
                                .into(holder.ivItemImage);
                    }
                }

                System.out.println("Rahul : ItemListingAdapter : mProductItemListingImages : " + mHitInner.getSource().getProductImages().get(0).getLink() + mHitInner.getSource().getProductImages().get(0).getImg());

            } catch (Exception e) {
                System.out.println("Rahul : GlideExceptiion : " + e.getMessage());
                Glide.with(mContext)
                        .load(R.drawable.image_not_available)
                        .diskCacheStrategy(DiskCacheStrategy.NONE) .skipMemoryCache(true)
                        .into(holder.ivItemImage);
                //isImageError[0] = true;
            }


            holder.btnAddToCart.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                   /* holder.btnAddToCart.setVisibility(View.INVISIBLE);
                    holder.llAddToCart.setVisibility(View.VISIBLE);*/
                    bsp_itemClick_interface.connectMain(Integer.parseInt(mHitInner.getId()), 1,position);

                }
            });

            holder.rlPlus.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {


                    int qty = Integer.parseInt(holder.tvQuantity.getText().toString());

                    holder.tvQuantity.setText("" + (qty + 1));
                    bsp_itemClick_interface.connectMain(Integer.parseInt(mHitInner.getId()), Integer.parseInt(holder.tvQuantity.getText().toString().trim()),position);

                }
            });

            holder.rlMinus.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    int qty = Integer.parseInt(holder.tvQuantity.getText().toString());
                    if (qty == 1) {
                        holder.llAddToCart.setVisibility(View.INVISIBLE);
                        holder.btnAddToCart.setVisibility(View.VISIBLE);
                        bsp_itemClick_interface.connectMain(Integer.parseInt(mHitInner.getId()), 0,position);
                    } else {
                        holder.tvQuantity.setText("" + (qty - 1));
                        bsp_itemClick_interface.connectMain(Integer.parseInt(mHitInner.getId()), Integer.parseInt(holder.tvQuantity.getText().toString().trim()),position);
                    }
                }
            });


            holder.itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    mProductListingInterface.sendSlug(mHitInner.getSource().getSlug() + "#GoGrocery#" + mHitInner.getSource().getName(), mHitInner.getSource().getId());
                }
            });


            /*holder.ivWishList.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (mDatabaseHandler.checkWishlistAvailable("" + mHitInner.getId())) {
                        mProductListingInterface.sendProductIdForWishlist(Integer.parseInt(mHitInner.getId()), "remove");
                    } else {
                        mProductListingInterface.sendProductIdForWishlist(Integer.parseInt(mHitInner.getId()), "add");

                    }
                }
            });*/

          /*  if (mDatabaseHandler.checkWishlistAvailable("" + mHitInner.getId())) {
                holder.ivWishList.setBackgroundResource(R.drawable.wishlist_added);

            } else {
                holder.ivWishList.setBackgroundResource(R.drawable.wishlist);

            }*/

            holder.ivSaveList.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    mProductListingInterface.savelist(mHitInner.getId());

                }
            });

          /*  if (isImageError[0]) {
                holder.itemView.setLayoutParams(params);
            }*/

        } else if (argholder instanceof FooterViewHolder) {


        }


        //------------- pAgionation
      /*  System.out.println("Rahul : pAgionation : position : "+position);
        System.out.println("Rahul : pAgionation : mMyBookingModel.size : "+mMyBookingModel.size());*/
       /* if(position==mMyBookingModel.size()-1)
        {
         myBookingPagePagination.updatePage();
        }*/

    }

    @Override
    public int getItemCount() {
        return mProductItemListing.size() + 1;
    }

    @Override
    public int getItemViewType(int position) {
        if (position == mProductItemListing.size()) {
            return TYPE_FOOTER;
        }
        return TYPE_ITEM;
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

    public class FooterViewHolder extends RecyclerView.ViewHolder {

        public FooterViewHolder(View view) {
            super(view);
            mSpinKitView = view.findViewById(R.id.spin_kit);
        }
    }

    public class MyViewHolder extends RecyclerView.ViewHolder {
        private ImageView ivItemImage, ivVeg, ivWishList, ivSaveList;
        private TextView tvItemBrand, tvItemName, tvGrams, tvPrice, tvDiscountedPrice, tvOriginalPrice, tvDiscountOffer, tvQuantity,tvUOM;
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
            tvUOM = view.findViewById(R.id.tvUOM);
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
            //ivWishList = view.findViewById(R.id.ivWishList);
            ivSaveList = view.findViewById(R.id.ivSavelist);


        }
    }


}
