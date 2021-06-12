package com.gogrocery.Adapters;

import android.content.Context;
import android.graphics.Paint;
import android.graphics.drawable.Drawable;
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

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.recyclerview.widget.RecyclerView;

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
import com.gogrocery.Models.BestSellingProductModel.Datum;
import com.gogrocery.Models.SimilarProductModel.Data;
import com.gogrocery.R;

import java.util.List;

public class BestSellingProductNewAdapter extends RecyclerView.Adapter<RecyclerView.ViewHolder> {


    private Context mContext;
    private List<Datum> mProductItemListing;
    private ProductListingInterface mProductListingInterface;
    private static final int TYPE_ITEM = 0;
    private static final int TYPE_FOOTER = 1;
    private BSP_ItemClick_Interface bsp_itemClick_interface;
    public SpinKitView mSpinKitView;
    private DatabaseHandler mDatabaseHandler;
    private SharedPreferenceManager mSharedPreferenceManager;

    public BestSellingProductNewAdapter(Context mContext,
                                        List<Datum> mProductItemListing, ProductListingInterface mProductListingInterface, BSP_ItemClick_Interface bsp_itemClick_interface, DatabaseHandler mDatabaseHandler) {
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


        if (viewType == TYPE_ITEM) {
            View itemView = LayoutInflater.from(parent.getContext())
                    .inflate(R.layout.item_listing_row, parent, false);
            return new BestSellingProductNewAdapter.MyViewHolder(itemView);
        } else if (viewType == TYPE_FOOTER) {
            //Inflating footer view
            View itemView = LayoutInflater.from(parent.getContext()).inflate(R.layout.layout_loading, parent, false);
            return new BestSellingProductNewAdapter.FooterViewHolder(itemView);
        } else return null;

    }

    @Override
    public void onBindViewHolder(@NonNull RecyclerView.ViewHolder argholder, int position) {

        if (argholder instanceof BestSellingProductNewAdapter.MyViewHolder) {
            BestSellingProductNewAdapter.MyViewHolder holder = (BestSellingProductNewAdapter.MyViewHolder) argholder;

            Datum mDataInner = mProductItemListing.get(position);
            String[] variant;

            try {
                holder.tvItemName.setText(mDataInner.getProduct().getName());

                holder.tvItemBrand.setText(mDataInner.getProduct().getBrand().getName());
                holder.tvDiscountedPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " +Constants.twoDecimalRoundOff( mDataInner.getProduct().getNewDefaultPrice()));


                if (mDataInner.getProduct().getVegNonvegType() != null) {
                    if (!mDataInner.getProduct().getVegNonvegType().equals("veg")) {
                        holder.ivVeg.setVisibility(View.GONE);
                    } else {
                        holder.ivVeg.setVisibility(View.VISIBLE);
                    }
                }

                if (mDatabaseHandler.CheckIsDataAlreadyInDBorNot(String.valueOf(mDataInner.getProduct().getId()))) {
                    holder.btnAddToCart.setVisibility(View.INVISIBLE);
                    holder.llAddToCart.setVisibility(View.VISIBLE);
                    holder.tvQuantity.setText("" + mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(mDataInner.getProduct().getId())));
                } else {
                    holder.btnAddToCart.setVisibility(View.VISIBLE);
                    holder.llAddToCart.setVisibility(View.INVISIBLE);
                }


                if (mDataInner.getProduct().getChannelPrice() != null || Double.parseDouble(mDataInner.getProduct().getChannelPrice()) != 0) {
                    Double getChannel_price = Double.parseDouble(mDataInner.getProduct().getChannelPrice());
                    Double getNew_default_price_unit = (mDataInner.getProduct().getNewDefaultPriceUnit());
                    if (getChannel_price > getNew_default_price_unit) {

                        holder.tvOriginalPrice.setVisibility(View.VISIBLE);
                        holder.tvOriginalPrice.setPaintFlags(holder.tvOriginalPrice.getPaintFlags() | Paint.STRIKE_THRU_TEXT_FLAG);
                        holder.tvOriginalPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(getChannel_price));

                        if (!mDataInner.getProduct().getDiscType().isEmpty()) {
                            if (mDataInner.getProduct().getDiscType().equals("1")) // % wise
                            {
                                holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                                holder.tvDiscountOffer.setText("(" + mDataInner.getProduct().getDiscountAmount() + "% OFF.)");

                            } else { // Currency wise
                                holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                                holder.tvDiscountOffer.setText("(" + Constants.VARIABLES.CURRENT_CURRENCY + " " + mDataInner.getProduct().getDiscountAmount() + " OFF.)");
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
                variant[0] = mDataInner.getProduct().getName();
        /*for (int i = 1; i < mDataInner.getVariantProduct().size(); i++) {
            variant[i] = mDataInner.getVariantProduct().get(i).getName();

        }*/
                setDropdownVariant(holder.actvVariant, variant);
            }catch (Exception e){e.printStackTrace();}


            try {
                System.out.println("Rahul : ItemListingAdapter : mProductItemListing : " + mDataInner.getProduct().getProductImage().get(0).getImg());
                Glide.with(mContext)
                        .load("https://d1fw2ui0wj5vn1.cloudfront.net/Lifco/lifco/product/400x400/" + mDataInner.getProduct().getProductImage().get(0).getImg())
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
                        .diskCacheStrategy(DiskCacheStrategy.NONE) .skipMemoryCache(true)
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
                   /* holder.btnAddToCart.setVisibility(View.INVISIBLE);
                    holder.llAddToCart.setVisibility(View.VISIBLE);*/
                    bsp_itemClick_interface.connectMain(mDataInner.getProduct().getId(), 1,position);

                }
            });

            holder.rlPlus.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {


                    int qty = Integer.parseInt(holder.tvQuantity.getText().toString());

                    holder.tvQuantity.setText("" + (qty + 1));
                    bsp_itemClick_interface.connectMain(mDataInner.getProduct().getId(), Integer.parseInt(holder.tvQuantity.getText().toString().trim()),position);

                }
            });

            holder.rlMinus.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    int qty = Integer.parseInt(holder.tvQuantity.getText().toString());
                    if (qty == 1) {
                        holder.llAddToCart.setVisibility(View.INVISIBLE);
                        holder.btnAddToCart.setVisibility(View.VISIBLE);
                        bsp_itemClick_interface.connectMain(mDataInner.getProduct().getId(), 0,position);
                    } else {
                        holder.tvQuantity.setText("" + (qty - 1));
                        bsp_itemClick_interface.connectMain(mDataInner.getProduct().getId(), Integer.parseInt(holder.tvQuantity.getText().toString().trim()),position);
                    }
                }
            });


            holder.itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    mProductListingInterface.sendSlug(mDataInner.getProduct().getSlug() + "#GoGrocery#" + mDataInner.getProduct().getName(), mDataInner.getProduct().getId());
                }
            });

            holder.ivSavelist.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    mProductListingInterface.savelist(String.valueOf(mDataInner.getProduct().getId()));

                }
            });

            String Oum = mProductItemListing.get(position).getProduct().getUom();
            String weight = mProductItemListing.get(position).getProduct().getWeight();


            if (Oum != null || weight != null) {
                holder.tvGrams.setText(weight + " " + Oum);
            } else {
                holder.tvGrams.setVisibility(View.GONE);
            }


        } else if (argholder instanceof BestSellingProductNewAdapter.FooterViewHolder) {


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

        if(mProductItemListing.size()>=6){
            return 6;
        }else{
            return mProductItemListing.size() + 1;
        }


    }

    @Override
    public int getItemViewType(int position) {
        if (position == mProductItemListing.size()) {
            return TYPE_FOOTER;
        }
        return TYPE_ITEM;
    }

    private void setDropdownVariant(AutoCompleteTextView mAutoCompleteTextView, String[] argVartiantName) {

        ArrayAdapter adapter = new ArrayAdapter(mContext, android.R.layout.simple_list_item_1, argVartiantName);

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
        private ImageView ivItemImage, ivVeg, ivSavelist;
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
            tvGrams = view.findViewById(R.id.tvUOM);
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
            ivSavelist = view.findViewById(R.id.ivSavelist);


        }
    }

}