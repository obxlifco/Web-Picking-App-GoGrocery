package com.gogrocery.Adapters;

import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Typeface;
import android.graphics.drawable.Drawable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
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
import com.bumptech.glide.request.RequestOptions;
import com.bumptech.glide.request.target.Target;
import com.github.ybq.android.spinkit.SpinKitView;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.BSP_ItemClick_Interface;
import com.gogrocery.Interfaces.PrepareViewOpenInterface;
import com.gogrocery.Interfaces.ProductListingInterface;
import com.gogrocery.Models.ElasticSearch.Hit;
import com.gogrocery.R;
import com.gogrocery.view.DetailActivity;
import com.gogrocery.view.MainActivityNew;

import java.util.List;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.content.res.ResourcesCompat;
import androidx.recyclerview.widget.RecyclerView;


public class MainItemListingAdapter extends RecyclerView.Adapter<RecyclerView.ViewHolder> {

    private RequestOptions options;
    private Context mContext;
    private List<Hit> mProductItemListing;
    private ProductListingInterface mProductListingInterface;
    private static final int TYPE_ITEM = 0;
    private static final int TYPE_FOOTER = 1;
    private int noOfColumn = 1;
    private BSP_ItemClick_Interface bsp_itemClick_interface;
    public SpinKitView mSpinKitView;
    private DatabaseHandler mDatabaseHandler;
    private SharedPreferenceManager mSharedPreferenceManager;
    private LinearLayout.LayoutParams params;
    private PrepareViewOpenInterface prepareViewOpenInterface;

    public MainItemListingAdapter(Context mContext, List<Hit> mProductItemListing, ProductListingInterface mProductListingInterface, BSP_ItemClick_Interface bsp_itemClick_interface, DatabaseHandler mDatabaseHandler, PrepareViewOpenInterface prepareViewOpenInterface) {
        this.mContext = mContext;
        this.mProductItemListing = mProductItemListing;
        this.mProductListingInterface = mProductListingInterface;
        this.mDatabaseHandler = mDatabaseHandler;
        this.bsp_itemClick_interface = bsp_itemClick_interface;
        this.prepareViewOpenInterface = prepareViewOpenInterface;
        //    this.noOfColumn=noOfColumn;
        System.out.println("Rahul : ItemListingAdapter : mProductItemListing : " + mProductItemListing.size());
        mSharedPreferenceManager = new SharedPreferenceManager(mContext);
    }

    @NonNull
    @Override
    public RecyclerView.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {

        params = new LinearLayout.LayoutParams(0, 0);
        if (viewType == TYPE_ITEM) {
            View itemView;
     /*       if(noOfColumn==3) {
                itemView = LayoutInflater.from(parent.getContext())
                        .inflate(R.layout.main_item_listing_row, parent, false);
            }else {*/
            itemView = LayoutInflater.from(parent.getContext())
                    .inflate(R.layout.main_item_listing_row_sea_food, parent, false);
            //  }
            return new MyViewHolder(itemView);

        } else if (viewType == TYPE_FOOTER) {
            //Inflating footer view
            View itemView = LayoutInflater.from(parent.getContext()).inflate(R.layout.layout_loading, parent, false);
            return new MainItemListingAdapter.FooterViewHolder(itemView);
        } else return null;

    }

    @Override
    public void onBindViewHolder(@NonNull RecyclerView.ViewHolder argholder, int position) {

        final boolean[] isImageError = {false};
        if (argholder instanceof MainItemListingAdapter.MyViewHolder) {
            MainItemListingAdapter.MyViewHolder holder = (MainItemListingAdapter.MyViewHolder) argholder;

           // Hit mProductItemListing.get(position) = mProductItemListing.get(position);
            String[] variant;

            holder.tvItemName.setText(mProductItemListing.get(position).getSource().getName());

            try {

                for (int i = 0; i < mProductItemListing.get(position).getSource().getProductImages().size(); i++) {
                    if (mProductItemListing.get(position).getSource().getProductImages().get(i).getIsCover() == 1) {
                        System.out.println("Rahul : MainItemListingAdapter : ProductName : " + mProductItemListing.get(position).getSource().getName());
                        System.out.println("Rahul : MainItemListingAdapter : ImageLink : " + mProductItemListing.get(position).getSource().getProductImages().get(i).getLink() + mProductItemListing.get(position).getSource().getProductImages().get(i).getImg());
                        String imageUrl = mProductItemListing.get(position).getSource().getProductImages().get(i).getLink() + mProductItemListing.get(position).getSource().getProductImages().get(i).getImg();


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
                System.out.println("Rahul : ItemListingAdapter : mProductItemListingImages : " + mProductItemListing.get(position).getSource().getProductImages().get(0).getLink() + mProductItemListing.get(position).getSource().getProductImages().get(0).getImg());

            } catch (Exception e) {
                System.out.println("Rahul : GlideExceptiion : " + e.getMessage());
                Glide.with(mContext)
                        .load(R.drawable.image_not_available)

                        .into(holder.ivItemImage);
                //isImageError[0] = true;
            }

            if (mDatabaseHandler.CheckIsDataAlreadyInDBorNot(String.valueOf(mProductItemListing.get(position).getId()))) {
                holder.btnAddToCart.setVisibility(View.GONE);
                holder.llAddToCart.setVisibility(View.VISIBLE);
                holder.tvQuantity.setText("" + mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(mProductItemListing.get(position).getId())));
            } else {
                holder.btnAddToCart.setVisibility(View.VISIBLE);
                holder.llAddToCart.setVisibility(View.GONE);
            }


            boolean isWarehouseAvailable = false;
            if (mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().size() > 0) {
                //System.out.println("Rahul : MainItemListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : size : " + mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().size());
                for (int i = 0; i < mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().size(); i++) {
                   /* System.out.println("Rahul : MainItemListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : 1 : " + mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getWarehouseId());
                    System.out.println("Rahul : MainItemListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : 2 : " + mSharedPreferenceManager.getWarehouseId());
*/
                    if (mSharedPreferenceManager.getWarehouseId().equals(String.valueOf(mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getWarehouseId())) && (mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getPriceType().equalsIgnoreCase("1"))) {
                        System.out.println("Rahul : MainItemListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : 3 : " + mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getPrice());
                        /*if (mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getPrice() != null) {
                            holder.tvDiscountedPrice.setText("$" + mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getPrice());
                        } else {
                            holder.tvDiscountedPrice.setText("$0.00");
                        }*/
//                        if(mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getPriceType().equalsIgnoreCase("1"))
                        isWarehouseAvailable = true;
                        holder.tvDiscountedPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getNewDefaultPriceUnit()));
                        System.out.println("Rahul : MainItemListingAdapter : mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getPrice() : " + mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getPrice());

                        System.out.println("Rahul : MainItemListingAdapter : mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getNewDefaultPriceUnit() : " + mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getNewDefaultPriceUnit());
String discountPrice= mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getDiscountAmount();
                      //  if (mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getPrice() > mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getNewDefaultPriceUnit()) {
                        if (discountPrice!=null&&!discountPrice.isEmpty()&&Double.parseDouble( mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getDiscountAmount()) > 0.0) {
                            holder.tvOriginalPrice.setVisibility(View.VISIBLE);
                            holder.tvDiscountedPrice.setTextColor(Color.parseColor("#C32D4A"));
                            Typeface typeface = ResourcesCompat.getFont(mContext, R.font.proxima_bold);
                            holder.tvDiscountedPrice.setTypeface(typeface);
                            holder.tvOriginalPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getPrice()));
                            holder.tvOriginalPrice.setPaintFlags(holder.tvOriginalPrice.getPaintFlags() | Paint.STRIKE_THRU_TEXT_FLAG);

                            if (!mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getDiscType().isEmpty()) {
                                if (mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getDiscType().equals("1")) // % wise
                                {
                                    holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                                    holder.tvDiscountOffer.setText( mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getDiscountAmount() + mContext.getResources().getString(R.string._pen_off));

                                } else { // Currency wise
                                    holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                                    holder.tvDiscountOffer.setText(Constants.VARIABLES.CURRENT_CURRENCY + " " + mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getDiscountAmount()+" "+ mContext.getResources().getString(R.string._off));
                                }
                            }else {
                                holder.tvDiscountOffer.setVisibility(View.GONE);
                            }

                        }else {
                            holder.tvOriginalPrice.setVisibility(View.GONE);
                            holder.tvDiscountOffer.setVisibility(View.GONE);
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


            if (mProductItemListing.get(position).getSource().getVegNonvegType() != null) {
                if (!mProductItemListing.get(position).getSource().getVegNonvegType().equals("veg")) {
                    holder.ivVeg.setVisibility(View.GONE);
                } else {
                    holder.ivVeg.setVisibility(View.VISIBLE);
                }
            }


       /* if (mDataInner.getVariantProduct().size() >= 1) {
            variant = new String[mDataInner.getVariantProduct().size() + 1];


        } else {
            variant = new String[1];
        }*/
            variant = new String[1];
            variant[0] = mProductItemListing.get(position).getSource().getName();
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


            holder.btnAddToCart.setOnClickListener(v -> {
                if (mProductItemListing.get(position).getSource().getCustomField() != null && !mProductItemListing.get(position).getSource().getCustomField().isEmpty() && mProductItemListing.get(position).getSource().getCustomField().size() > 0) {
                     /*   holder.btnAddToCart.setVisibility(View.GONE);
                        holder.llAddToCart.setVisibility(View.VISIBLE);*/
                    if (mProductItemListing.get(position).getSource().getCustomField().size() > 0) {
                        String custom_field_name = mProductItemListing.get(position).getSource().getCustomField().get(0).getFieldName();
                        String custom_field_value = mProductItemListing.get(position).getSource().getCustomField().get(0).getValue();
                        prepareViewOpenInterface.customFieldValueSelect(Integer.parseInt(mProductItemListing.get(position).getId()), 1, custom_field_name, custom_field_value,position);
                    }

                } else {
                      /*  holder.btnAddToCart.setVisibility(View.GONE);
                        holder.llAddToCart.setVisibility(View.VISIBLE);*/
                    bsp_itemClick_interface.connectMain(Integer.parseInt(mProductItemListing.get(position).getId()), 1,position);
                }
            });


            holder.rlPlus.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {


                    int qty = Integer.parseInt(holder.tvQuantity.getText().toString());

                    holder.tvQuantity.setText("" + (qty + 1));
                    bsp_itemClick_interface.connectMain(Integer.parseInt(mProductItemListing.get(position).getId()), Integer.parseInt(holder.tvQuantity.getText().toString().trim()),position);

                }
            });

            holder.rlMinus.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    int qty = Integer.parseInt(holder.tvQuantity.getText().toString());
                    if (qty == 1) {
                        holder.llAddToCart.setVisibility(View.GONE);
                        holder.btnAddToCart.setVisibility(View.VISIBLE);
                        bsp_itemClick_interface.connectMain(Integer.parseInt(mProductItemListing.get(position).getId()), 0,position);
                    } else {
                        holder.tvQuantity.setText("" + (qty - 1));
                        bsp_itemClick_interface.connectMain(Integer.parseInt(mProductItemListing.get(position).getId()), Integer.parseInt(holder.tvQuantity.getText().toString().trim()),position);
                    }
                }
            });


            holder.itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    mProductListingInterface.sendSlug(mProductItemListing.get(position).getSource().getSlug() + "#GoGrocery#" + mProductItemListing.get(position).getSource().getName(), mProductItemListing.get(position).getSource().getId());
                }
            });

            if (mProductItemListing.get(position).getSource().getWeight() != null || !mProductItemListing.get(position).getSource().getUnit().isEmpty()) {
                holder.tvUOM.setVisibility(View.VISIBLE);
                holder.tvUOM.setText(mProductItemListing.get(position).getSource().getWeight() + " " + mProductItemListing.get(position).getSource().getUnit());
            } else {
                holder.tvUOM.setVisibility(View.INVISIBLE);
            }

            if (mProductItemListing.get(position).getSource().getBrand() != null) {
                if (mProductItemListing.get(position).getSource().getBrand() != null) {
                    holder.tvItemBrand.setVisibility(View.INVISIBLE);
                    holder.tvItemBrand.setText(mProductItemListing.get(position).getSource().getBrand());
                } else {
                    holder.tvItemBrand.setVisibility(View.INVISIBLE);
                }
            } else {
                holder.tvItemBrand.setVisibility(View.INVISIBLE);
            }
            /*holder.ivWishList.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (mDatabaseHandler.checkWishlistAvailable("" + mProductItemListing.get(position).getId())) {
                        mProductListingInterface.sendProductIdForWishlist(Integer.parseInt(mProductItemListing.get(position).getId()), "remove");
                    } else {
                        mProductListingInterface.sendProductIdForWishlist(Integer.parseInt(mProductItemListing.get(position).getId()), "add");

                    }
                }
            });*/

          /*  if (mDatabaseHandler.checkWishlistAvailable("" + mProductItemListing.get(position).getId())) {
                holder.ivWishList.setBackgroundResource(R.drawable.wishlist_added);

            } else {
                holder.ivWishList.setBackgroundResource(R.drawable.wishlist);

            }*/

        /*    holder.ivSaveList.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    mProductListingInterface.savelist(mProductItemListing.get(position).getId());

                }
            });*/

          /*  if (isImageError[0]) {
                holder.itemView.setLayoutParams(params);
            }*/

        } else if (argholder instanceof MainItemListingAdapter.FooterViewHolder) {


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
/* extends RecyclerView.Adapter<RecyclerView.ViewHolder> {


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


    public MainItemListingAdapter(Context mContext,
                                  List<Hit> mProductItemListing, ProductListingInterface mProductListingInterface, BSP_ItemClick_Interface bsp_itemClick_interface, DatabaseHandler mDatabaseHandler) {
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
                    .inflate(R.layout.main_item_listing_row, parent, false);
            return new MainItemListingAdapter.MyViewHolder(itemView);
        } else if (viewType == TYPE_FOOTER) {
            //Inflating footer view
            View itemView = LayoutInflater.from(parent.getContext()).inflate(R.layout.layout_loading, parent, false);
            return new MainItemListingAdapter.FooterViewHolder(itemView);
        } else return null;

    }

    @Override
    public void onBindViewHolder(@NonNull RecyclerView.ViewHolder argholder, int position) {

        final boolean[] isImageError = {false};
        if (argholder instanceof MainItemListingAdapter.MyViewHolder) {
            MainItemListingAdapter.MyViewHolder holder = (MainItemListingAdapter.MyViewHolder) argholder;

            Hit mProductItemListing.get(position) = mProductItemListing.get(position);
            String[] variant;

            holder.tvItemName.setText(mProductItemListing.get(position).getSource().getName());
            if (mProductItemListing.get(position).getSource().getWeight() != null || !mProductItemListing.get(position).getSource().getUnit().isEmpty()) {
                holder.tvUOM.setVisibility(View.VISIBLE);
                holder.tvUOM.setText(mProductItemListing.get(position).getSource().getWeight() + " " + mProductItemListing.get(position).getSource().getUnit());
            } else {
                holder.tvUOM.setVisibility(View.INVISIBLE);
            }

            if (mProductItemListing.get(position).getSource().getBrand() != null) {
                if (mProductItemListing.get(position).getSource().getBrand() != null) {
                    holder.tvItemBrand.setVisibility(View.VISIBLE);
                    holder.tvItemBrand.setText(mProductItemListing.get(position).getSource().getBrand());
                } else {
                    holder.tvItemBrand.setVisibility(View.INVISIBLE);
                }
            } else {
                holder.tvItemBrand.setVisibility(View.INVISIBLE);
            }

            boolean isWarehouseAvailable = false;
            if (mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().size() > 0) {
                //System.out.println("Rahul : MainItemListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : size : " + mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().size());
                for (int i = 0; i < mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().size(); i++) {
                   *//* System.out.println("Rahul : MainItemListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : 1 : " + mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getWarehouseId());
                    System.out.println("Rahul : MainItemListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : 2 : " + mSharedPreferenceManager.getWarehouseId());
*//*
                    if (mSharedPreferenceManager.getWarehouseId().equals(String.valueOf(mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getWarehouseId())) && (mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getPriceType().equalsIgnoreCase("1"))) {
                        System.out.println("Rahul : MainItemListingAdapter : onBindViewHolder : getChannelCurrencyProductPrice : 3 : " + mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getPrice());
                        *//*if (mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getPrice() != null) {
                            holder.tvDiscountedPrice.setText("$" + mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getPrice());
                        } else {
                            holder.tvDiscountedPrice.setText("$0.00");
                        }*//*
//                        if(mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getPriceType().equalsIgnoreCase("1"))
                        isWarehouseAvailable = true;
                        holder.tvDiscountedPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getNewDefaultPriceUnit()));
                        System.out.println("Rahul : MainItemListingAdapter : mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getPrice() : " + mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getPrice());

                        System.out.println("Rahul : MainItemListingAdapter : mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getNewDefaultPriceUnit() : " + mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getNewDefaultPriceUnit());

                        if (mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getPrice() > mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getNewDefaultPriceUnit()) {
                            holder.tvOriginalPrice.setVisibility(View.VISIBLE);
                            holder.tvOriginalPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getPrice()));
                            holder.tvOriginalPrice.setPaintFlags(holder.tvOriginalPrice.getPaintFlags() | Paint.STRIKE_THRU_TEXT_FLAG);

                            if (!mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getDiscType().isEmpty()) {
                                if (mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getDiscType().equals("1")) // % wise
                                {
                                    holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                                    holder.tvDiscountOffer.setText("(" + mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getDiscountAmount() + "% OFF.)");

                                } else { // Currency wise
                                    holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                                    holder.tvDiscountOffer.setText("(" + Constants.VARIABLES.CURRENT_CURRENCY + " " + mProductItemListing.get(position).getSource().getChannelCurrencyProductPrice().get(i).getDiscountAmount() + " OFF.)");
                                }
                            }

                        }
                    }
                }
                if (!isWarehouseAvailable) {
                    // holder.itemView.setLayoutParams(params);
                }
            }


            if (mProductItemListing.get(position).getSource().getVegNonvegType() != null) {
                if (!mProductItemListing.get(position).getSource().getVegNonvegType().equals("veg")) {
                    holder.ivVeg.setVisibility(View.GONE);
                } else {
                    holder.ivVeg.setVisibility(View.VISIBLE);
                }
            }

            if (mDatabaseHandler.CheckIsDataAlreadyInDBorNot(String.valueOf(mProductItemListing.get(position).getId()))) {
                holder.btnAddToCart.setVisibility(View.INVISIBLE);
                holder.llAddToCart.setVisibility(View.VISIBLE);
                holder.tvQuantity.setText("" + mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(mProductItemListing.get(position).getId())));
            } else {
                holder.btnAddToCart.setVisibility(View.VISIBLE);
                holder.llAddToCart.setVisibility(View.INVISIBLE);
            }
       *//* if (mDataInner.getVariantProduct().size() >= 1) {
            variant = new String[mDataInner.getVariantProduct().size() + 1];


        } else {
            variant = new String[1];
        }*//*
            variant = new String[1];
            variant[0] = mProductItemListing.get(position).getSource().getName();
        *//*for (int i = 1; i < mDataInner.getVariantProduct().size(); i++) {
            variant[i] = mDataInner.getVariantProduct().get(i).getName();

        }*//*

 *//*if(mDataInner.getChannel_price()!=null||Double.parseDouble(mDataInner.getChannel_price())!=0)
            {
                Double getChannel_price= Double.parseDouble(mDataInner.getChannel_price());
                Double getNew_default_price_unit= Double.parseDouble(mDataInner.getNew_default_price_unit());
                if(getChannel_price>getNew_default_price_unit)
                {
                    holder.tvOriginalPrice.setPaintFlags(holder.tvOriginalPrice.getPaintFlags() | Paint.STRIKE_THRU_TEXT_FLAG);

                }
            }*//*
            //setDropdownVariant(holder.actvVariant, variant);

            try {

                for (int i = 0; i < mProductItemListing.get(position).getSource().getProductImages().size(); i++) {
                    if (mProductItemListing.get(position).getSource().getProductImages().get(i).getIsCover() == 1) {
                        System.out.println("Rahul : MainItemListingAdapter : ProductName : " + mProductItemListing.get(position).getSource().getName());
                        System.out.println("Rahul : MainItemListingAdapter : ImageLink : " + mProductItemListing.get(position).getSource().getProductImages().get(i).getLink() + mProductItemListing.get(position).getSource().getProductImages().get(i).getImg());
                        Glide.with(mContext)
                                .load(mProductItemListing.get(position).getSource().getProductImages().get(i).getLink() + mProductItemListing.get(position).getSource().getProductImages().get(i).getImg())
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

                System.out.println("Rahul : ItemListingAdapter : mProductItemListingImages : " + mProductItemListing.get(position).getSource().getProductImages().get(0).getLink() + mProductItemListing.get(position).getSource().getProductImages().get(0).getImg());

            } catch (Exception e) {
                System.out.println("Rahul : GlideExceptiion : " + e.getMessage());
                Glide.with(mContext)
                        .load(R.drawable.image_not_available)
                        .diskCacheStrategy(DiskCacheStrategy.NONE).skipMemoryCache(true)
                        .into(holder.ivItemImage);
                //isImageError[0] = true;
            }


            holder.btnAddToCart.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                   *//* holder.btnAddToCart.setVisibility(View.INVISIBLE);
                    holder.llAddToCart.setVisibility(View.VISIBLE);*//*
                    bsp_itemClick_interface.connectMain(Integer.parseInt(mProductItemListing.get(position).getId()), 1);

                }
            });

            holder.rlPlus.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {


                    int qty = Integer.parseInt(holder.tvQuantity.getText().toString());

                    holder.tvQuantity.setText("" + (qty + 1));
                    bsp_itemClick_interface.connectMain(Integer.parseInt(mProductItemListing.get(position).getId()), Integer.parseInt(holder.tvQuantity.getText().toString().trim()));

                }
            });

            holder.rlMinus.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    int qty = Integer.parseInt(holder.tvQuantity.getText().toString());
                    if (qty == 1) {
                        holder.llAddToCart.setVisibility(View.INVISIBLE);
                        holder.btnAddToCart.setVisibility(View.VISIBLE);
                        bsp_itemClick_interface.connectMain(Integer.parseInt(mProductItemListing.get(position).getId()), 0);
                    } else {
                        holder.tvQuantity.setText("" + (qty - 1));
                        bsp_itemClick_interface.connectMain(Integer.parseInt(mProductItemListing.get(position).getId()), Integer.parseInt(holder.tvQuantity.getText().toString().trim()));
                    }
                }
            });


            holder.itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    mProductListingInterface.sendSlug(mProductItemListing.get(position).getSource().getSlug() + "#GoGrocery#" + mProductItemListing.get(position).getSource().getName(), mProductItemListing.get(position).getSource().getId());
                }
            });


            *//*holder.ivWishList.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (mDatabaseHandler.checkWishlistAvailable("" + mProductItemListing.get(position).getId())) {
                        mProductListingInterface.sendProductIdForWishlist(Integer.parseInt(mProductItemListing.get(position).getId()), "remove");
                    } else {
                        mProductListingInterface.sendProductIdForWishlist(Integer.parseInt(mProductItemListing.get(position).getId()), "add");

                    }
                }
            });*//*

 *//*  if (mDatabaseHandler.checkWishlistAvailable("" + mProductItemListing.get(position).getId())) {
                holder.ivWishList.setBackgroundResource(R.drawable.wishlist_added);

            } else {
                holder.ivWishList.setBackgroundResource(R.drawable.wishlist);

            }*//*

            holder.ivSaveList.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    mProductListingInterface.savelist(mProductItemListing.get(position).getId());

                }
            });

          *//*  if (isImageError[0]) {
                holder.itemView.setLayoutParams(params);
            }*//*

        } else if (argholder instanceof MainItemListingAdapter.FooterViewHolder) {


        }


        //------------- pAgionation
      *//*  System.out.println("Rahul : pAgionation : position : "+position);
        System.out.println("Rahul : pAgionation : mMyBookingModel.size : "+mMyBookingModel.size());*//*
 *//* if(position==mMyBookingModel.size()-1)
        {
         myBookingPagePagination.updatePage();
        }*//*

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

   *//* private void setDropdownVariant(AutoCompleteTextView mAutoCompleteTextView, String[] argVartiantName) {

        ArrayAdapter adapter = new
                ArrayAdapter(mContext, android.R.layout.simple_list_item_1, argVartiantName);

        mAutoCompleteTextView.setAdapter(adapter);

        System.out.println("Rahul : DealsOfTheDayAdapter : setDropdownVariant : argVartiantName : " + argVartiantName.toString());
        mAutoCompleteTextView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                System.out.println("Rautocomplete : " + argVartiantName[i]);
              *//**//*  mVehicleType = argCarTypeID[i];
                mCategoryId = argCarTypeID[i];
                mAutoCompleteTextView.setError(null);
                mPassingVehicleType = argCarType[i];*//**//*
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

       *//**//* mAutoCompleteTextView.setOnTouchListener(new View.OnTouchListener() {
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
        });*//**//*
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
    }*//*

    public class FooterViewHolder extends RecyclerView.ViewHolder {

        public FooterViewHolder(View view) {
            super(view);
            mSpinKitView = view.findViewById(R.id.spin_kit);
        }
    }




    public class MyViewHolder extends RecyclerView.ViewHolder {
        private ImageView ivItemImage, ivVeg, ivWishList, ivSaveList;
        private TextView tvItemBrand, tvItemName, tvGrams, tvPrice, tvDiscountedPrice, tvOriginalPrice, tvDiscountOffer,tvUOM;
        private Button btnAddToCart;
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
            btnAddToCart = view.findViewById(R.id.btnAddToCart);
            llAddToCart = view.findViewById(R.id.llAddToCart);
            rlMinus = view.findViewById(R.id.rlMinus);
            rlPlus = view.findViewById(R.id.rlPlus);
            tvQuantity = view.findViewById(R.id.etQuantity);
            //ivWishList = view.findViewById(R.id.ivWishList);
            ivSaveList = view.findViewById(R.id.ivSavelist);


        }
    }




}*/
