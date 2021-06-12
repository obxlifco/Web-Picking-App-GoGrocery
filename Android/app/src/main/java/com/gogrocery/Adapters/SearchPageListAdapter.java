package com.gogrocery.Adapters;

import android.content.Context;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.content.res.ResourcesCompat;
import androidx.recyclerview.widget.RecyclerView;

import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Typeface;
import android.graphics.drawable.Drawable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AutoCompleteTextView;
import android.widget.EditText;
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
import com.gogrocery.Interfaces.ActivityRedirection;
import com.gogrocery.Interfaces.BSP_ItemClick_Interface;
import com.gogrocery.Interfaces.PrepareViewOpenInterface;
import com.gogrocery.Interfaces.ProductListingInterface;
import com.gogrocery.Interfaces.SearchActivityLoadingInterface;
import com.gogrocery.Models.ElasticSearch.Hit;
import com.gogrocery.R;
import com.squareup.picasso.Picasso;

import java.util.List;


public class SearchPageListAdapter extends RecyclerView.Adapter<RecyclerView.ViewHolder> {


    private Context mContext;
    private List<Hit> mSearchHitList;
    private ActivityRedirection mActivityRedirectionListner;
    private SharedPreferenceManager mSharedPreferenceManager;
    private ProductListingInterface mProductListingInterface;
    private SearchActivityLoadingInterface mSearchActivityLoadingInterface;
    private BSP_ItemClick_Interface bsp_itemClick_interface;
private PrepareViewOpenInterface mPrepareViewOpenInterface;
    private DatabaseHandler mDatabaseHandler;
    private static final int TYPE_ITEM = 0;
    private static final int TYPE_FOOTER = 1;

    public SearchPageListAdapter(Context mContext,
                                 List<Hit> mSearchHitList, ActivityRedirection mActivityRedirectionListner, ProductListingInterface mProductListingInterface, SearchActivityLoadingInterface mSearchActivityLoadingInterface, BSP_ItemClick_Interface bsp_itemClick_interface, DatabaseHandler mDatabaseHandler,PrepareViewOpenInterface mPrepareViewOpenInterface) {

        this.mContext = mContext;
        this.mSearchHitList = mSearchHitList;
        this.mActivityRedirectionListner = mActivityRedirectionListner;
        this.mProductListingInterface = mProductListingInterface;
        this.bsp_itemClick_interface = bsp_itemClick_interface;
        this.mDatabaseHandler = mDatabaseHandler;
        this.mPrepareViewOpenInterface= mPrepareViewOpenInterface;
        this.mSearchActivityLoadingInterface = mSearchActivityLoadingInterface;
        System.out.println("Rahul : SearchPageListAdapter : mSearchHitList : " + mSearchHitList.size());
        mSharedPreferenceManager = new SharedPreferenceManager(mContext);
    }

    @NonNull
    @Override
    public RecyclerView.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {

        if (viewType == TYPE_ITEM) {
            View itemView = LayoutInflater.from(parent.getContext())
                    .inflate(R.layout.search_list_row, parent, false);


            return new MyViewHolder(itemView);
        } else if (viewType == TYPE_FOOTER) {
            //Inflating footer view
            View itemView = LayoutInflater.from(parent.getContext()).inflate(R.layout.layout_loading, parent, false);
            return new FooterViewHolder(itemView);
        } else return null;


    }

    @Override
    public void onBindViewHolder(@NonNull RecyclerView.ViewHolder argholder, int position) {

        if (argholder instanceof MyViewHolder) {
            MyViewHolder holder = (MyViewHolder) argholder;

            Hit mHitInner = mSearchHitList.get(position);

            String[] variant;

            holder.tvItemName.setText(mHitInner.getSource().getName());
            if (mHitInner.getSource().getWeight() != null || !mHitInner.getSource().getUnit().isEmpty()) {
                holder.tvUOM.setVisibility(View.VISIBLE);
                holder.tvUOM.setText(mHitInner.getSource().getWeight() + " " + mHitInner.getSource().getUnit());
            } else {
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
                //System.out.println("Rahul : MainItemListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : size : " + mHitInner.getSource().getChannelCurrencyProductPrice().size());
                for (int i = 0; i < mHitInner.getSource().getChannelCurrencyProductPrice().size(); i++) {
                   /* System.out.println("Rahul : MainItemListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : 1 : " + mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getWarehouseId());
                    System.out.println("Rahul : MainItemListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : 2 : " + mSharedPreferenceManager.getWarehouseId());
*/
                    if (mSharedPreferenceManager.getWarehouseId().equals(String.valueOf(mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getWarehouseId())) && (mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPriceType().equalsIgnoreCase("1"))) {
                        System.out.println("Rahul : MainItemListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : 3 : " + mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice());
                        /*if (mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice() != null) {
                            holder.tvDiscountedPrice.setText("$" + mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice());
                        } else {
                            holder.tvDiscountedPrice.setText("$0.00");
                        }*/
//                        if(mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPriceType().equalsIgnoreCase("1"))
                        isWarehouseAvailable = true;
                        holder.tvDiscountedPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getNewDefaultPriceUnit()));
                        System.out.println("Rahul : MainItemListingAdapter : mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice() : " + mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice());

                        System.out.println("Rahul : MainItemListingAdapter : mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getNewDefaultPriceUnit() : " + mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getNewDefaultPriceUnit());
                        String discountPrice=mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getDiscountAmount();
                      //  if (mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice() > mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getNewDefaultPriceUnit()) {
                        if (discountPrice!=null&&!discountPrice.isEmpty()&&Double.parseDouble(discountPrice) > 0.0) {
                            holder.tvOriginalPrice.setVisibility(View.VISIBLE);
                            holder.tvOriginalPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice()));
                            holder.tvOriginalPrice.setPaintFlags(holder.tvOriginalPrice.getPaintFlags() | Paint.STRIKE_THRU_TEXT_FLAG);
                            holder.tvDiscountedPrice.setTextColor(Color.parseColor("#C32D4A"));
                            Typeface typeface = ResourcesCompat.getFont(mContext, R.font.proxima_bold);
                            holder.tvDiscountedPrice.setTypeface(typeface);
                            if (!mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getDiscType().isEmpty()) {
                                if (mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getDiscType().equals("1")) // % wise
                                {
                                    holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                                    holder.tvDiscountOffer.setText( mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getDiscountAmount() + mContext.getResources().getString(R.string._pen_off));

                                } else { // Currency wise
                                    holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                                    holder.tvDiscountOffer.setText(Constants.VARIABLES.CURRENT_CURRENCY + " " + mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getDiscountAmount() + mContext.getResources().getString(R.string._off));
                                }
                            }

                        }else {
                            holder.tvDiscountOffer.setVisibility(View.GONE);
                            holder.tvOriginalPrice.setVisibility(View.GONE);
                            holder.tvDiscountedPrice.setTextColor(Color.parseColor("#2E6B0B"));
                            Typeface typeface = ResourcesCompat.getFont(mContext, R.font.proxima_regular);
                            holder.tvDiscountedPrice.setTypeface(typeface);
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
                holder.btnAddToCart.setVisibility(View.GONE);
                holder.llAddToCart.setVisibility(View.VISIBLE);
                holder.tvQuantity.setText("" + mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(mHitInner.getId())));
            } else {
                holder.btnAddToCart.setVisibility(View.VISIBLE);
                holder.llAddToCart.setVisibility(View.GONE);
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
                        System.out.println("Rahul : MainItemListingAdapter : ProductName : " + mHitInner.getSource().getName());
                        System.out.println("Rahul : MainItemListingAdapter : ImageLink : " + mHitInner.getSource().getProductImages().get(i).getLink() + mHitInner.getSource().getProductImages().get(i).getImg());
                        String imageUrl = mHitInner.getSource().getProductImages().get(i).getLink() + mHitInner.getSource().getProductImages().get(i).getImg();


                        String imagePath = imageUrl.replaceAll(" ", "%20");

                        Glide.with(mContext)
                                .load(imagePath)
                                // .load(ApiConstant.IMAGE_PRODUCT_URL + productList.get(position).getProductImage().get(i).getImg())
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

                                .into(holder.ivItemImage);
                    }
                }
             //   System.out.println("Rahul : ItemListingAdapter : mProductItemListingImages : " + mProductItemListing.get(position).getSource().getProductImages().get(0).getLink() + mHitInner.getSource().getProductImages().get(i).getImg());

            } catch (Exception e) {
                System.out.println("Rahul : GlideExceptiion : " + e.getMessage());
                Glide.with(mContext)
                        .load(R.drawable.image_not_available)

                        .into(holder.ivItemImage);
                //isImageError[0] = true;
            }

/*
            try {

                for (int i = 0; i < mHitInner.getSource().getProductImages().size(); i++) {
                    if (mHitInner.getSource().getProductImages().get(i).getIsCover() == 1) {
                        System.out.println("Rahul : MainItemListingAdapter : ProductName : " + mHitInner.getSource().getName());
                        System.out.println("Rahul : MainItemListingAdapter : ImageLink : " + mHitInner.getSource().getProductImages().get(i).getLink() + mHitInner.getSource().getProductImages().get(i).getImg());
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
                                .diskCacheStrategy(DiskCacheStrategy.NONE).skipMemoryCache(true)
                                .into(holder.ivItemImage);
                    }
                }

                System.out.println("Rahul : ItemListingAdapter : mProductItemListingImages : " + mHitInner.getSource().getProductImages().get(0).getLink() + mHitInner.getSource().getProductImages().get(0).getImg());

            } catch (Exception e) {
                System.out.println("Rahul : GlideExceptiion : " + e.getMessage());
                Glide.with(mContext)
                        .load(R.drawable.image_not_available)
                     ///   .diskCacheStrategy(DiskCacheStrategy.NONE).skipMemoryCache(true)
                        .into(holder.ivItemImage);
                //isImageError[0] = true;
            }*/


            holder.btnAddToCart.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if(mHitInner.getSource().getCustomField()!=null&&!mHitInner.getSource().getCustomField().isEmpty()&&mHitInner.getSource().getCustomField().size()>0) {
                     /*   holder.btnAddToCart.setVisibility(View.GONE);
                        holder.llAddToCart.setVisibility(View.VISIBLE);*/
                        if(mHitInner.getSource().getCustomField().size()>0) {
                            String custom_field_name = mHitInner.getSource().getCustomField().get(0).getFieldName();
                            String custom_field_value = mHitInner.getSource().getCustomField().get(0).getValue();
                            mPrepareViewOpenInterface.customFieldValueSelect(Integer.parseInt(mHitInner.getId()), 1, custom_field_name, custom_field_value,position);
                        }

                    }else {
                      /*  holder.btnAddToCart.setVisibility(View.GONE);
                        holder.llAddToCart.setVisibility(View.VISIBLE);*/
                        bsp_itemClick_interface.connectMain(Integer.parseInt(mHitInner.getId()), 1,position);
                    }




                 /*

                    holder.btnAddToCart.setVisibility(View.GONE);
                    holder.llAddToCart.setVisibility(View.VISIBLE);
                    bsp_itemClick_interface.connectMain(Integer.parseInt(mHitInner.getId()), 1);*/

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
                        holder.llAddToCart.setVisibility(View.GONE);
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

        /*    holder.ivSaveList.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    mProductListingInterface.savelist(mHitInner.getId());

                }
            });*/

          /*  if (isImageError[0]) {
                holder.itemView.setLayoutParams(params);
            }*/





         /*   if (mHitInner.getSource().getProductImages().size() > 0) {
                for (int i = 0; i < mHitInner.getSource().getProductImages().size(); i++) {
                    if (mHitInner.getSource().getProductImages().get(i).getIsCover() == 1) {

                        Picasso.get().load(mHitInner.getSource().getProductImages().get(i).getLink() + mHitInner.getSource().getProductImages().get(i).getImg()).centerInside().fit().into(holder.ivSearchItemImage);

                    }
                }


            }
            holder.tvSearchItemName.setText(mHitInner.getSource().getName());
            if(mHitInner.getSource().getCategory().size()>0){
                holder.tvSearchItemCategory.setText(mHitInner.getSource().getCategory().get(0));
            }else{
                holder.tvSearchItemCategory.setText("");
            }

            if (mHitInner.getSource().getChannelCurrencyProductPrice().size() > 0) {
                //System.out.println("Rahul : ProductListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : size : " + mHitInner.getSource().getChannelCurrencyProductPrice().size());
                for (int i = 0; i < mHitInner.getSource().getChannelCurrencyProductPrice().size(); i++) {
                   *//* System.out.println("Rahul : ProductListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : 1 : " + mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getWarehouseId());
                    System.out.println("Rahul : ProductListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : 2 : " + mSharedPreferenceManager.getWarehouseId());
*//*
                    if (mSharedPreferenceManager.getWarehouseId().equals(String.valueOf(mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getWarehouseId()))&&(mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPriceType().equalsIgnoreCase("1"))) {
                        //System.out.println("Rahul : ProductListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : 3 : "+mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice());
                        *//*if (mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice() != null) {
                            holder.tvDiscountedPrice.setText("$" + mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice());
                        } else {
                            holder.tvDiscountedPrice.setText("$0.00");
                        }*//*
                        holder.tvSearchItemPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice()));
                    }
                }
            }
*/
            holder.itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    System.out.println("Rahul : mHitInner.getSource().getSlug() : " + mHitInner.getSource().getSlug());
                    mProductListingInterface.sendSlug(mHitInner.getSource().getSlug() + "#GoGrocery#" + mHitInner.getSource().getName(), mHitInner.getSource().getId());
                }
            });
        } else if (argholder instanceof FooterViewHolder) {

            mSearchActivityLoadingInterface.callLoading();

        }

       /* if (!((SearchActivity) mContext).argTermSearchFilter.contains(mHitInner.getId())) {
            ((SearchActivity) mContext).argTermSearchFilter.add(mHitInner.getId());
        }*/

    }


    @Override
    public int getItemCount() {
        return mSearchHitList.size();
    }

    public class FooterViewHolder extends RecyclerView.ViewHolder {

        public FooterViewHolder(View view) {
            super(view);

        }
    }

    public class MyViewHolder extends RecyclerView.ViewHolder {


        private ImageView ivItemImage, ivVeg, ivWishList, ivSaveList;
        private TextView tvItemBrand, tvItemName, tvGrams, tvPrice, tvDiscountedPrice, tvOriginalPrice, tvDiscountOffer, tvUOM;
        private ImageView btnAddToCart;
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
            tvGrams = view.findViewById(R.id.tvGrams);
            tvPrice = view.findViewById(R.id.tvPrice);
            tvDiscountedPrice = view.findViewById(R.id.tvDiscountedPrice);
            tvOriginalPrice = view.findViewById(R.id.tvOriginalPrice);
            tvDiscountOffer = view.findViewById(R.id.tvDiscountOffer);
            actvVariant = view.findViewById(R.id.actvVariant);
            ivVeg = view.findViewById(R.id.ivVeg);
            btnAddToCart = view.findViewById(R.id.ivAddCart);
            llAddToCart = view.findViewById(R.id.llAddToCart);
            rlMinus = view.findViewById(R.id.rlMinus);
            rlPlus = view.findViewById(R.id.rlPlus);
            tvQuantity = view.findViewById(R.id.etQuantity);
            //ivWishList = view.findViewById(R.id.ivWishList);
            ivSaveList = view.findViewById(R.id.ivSavelist);


        }

    }


}
