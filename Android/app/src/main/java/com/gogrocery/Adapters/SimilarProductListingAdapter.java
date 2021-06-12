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
import com.bumptech.glide.request.target.Target;
import com.github.ybq.android.spinkit.SpinKitView;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.DatabaseHandler.DatabaseHandler;
import com.gogrocery.Interfaces.BSP_ItemClick_Interface;
import com.gogrocery.Interfaces.PrepareViewOpenInterface;
import com.gogrocery.Interfaces.ProductListingInterface;
import com.gogrocery.Models.SimilarProductModel.Data;
import com.gogrocery.R;

import java.util.List;


public class SimilarProductListingAdapter extends RecyclerView.Adapter<RecyclerView.ViewHolder> {


    private Context mContext;
    private List<Data> mProductItemListing;
    private ProductListingInterface mProductListingInterface;
    private static final int TYPE_ITEM = 0;
    private static final int TYPE_FOOTER = 1;
    private BSP_ItemClick_Interface bsp_itemClick_interface;
    private PrepareViewOpenInterface mPrepareViewOpenInterface;
    public SpinKitView mSpinKitView;
    private DatabaseHandler mDatabaseHandler;
    private SharedPreferenceManager mSharedPreferenceManager;

    public SimilarProductListingAdapter(Context mContext,
                                        List<Data> mProductItemListing, ProductListingInterface mProductListingInterface, BSP_ItemClick_Interface bsp_itemClick_interface, DatabaseHandler mDatabaseHandler,PrepareViewOpenInterface mPrepareViewOpenInterface) {
        this.mContext = mContext;
        this.mProductItemListing = mProductItemListing;
        this.mProductListingInterface = mProductListingInterface;
        this.mDatabaseHandler = mDatabaseHandler;
        this.bsp_itemClick_interface = bsp_itemClick_interface;
        this.mPrepareViewOpenInterface =mPrepareViewOpenInterface;
        System.out.println("Rahul : ItemListingAdapter : mProductItemListing : " + mProductItemListing.size());
        mSharedPreferenceManager = new SharedPreferenceManager(mContext);
    }

    @NonNull
    @Override
    public RecyclerView.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {


        if (viewType == TYPE_ITEM) {
            View itemView = LayoutInflater.from(parent.getContext())
                    .inflate(R.layout.similar_product_row, parent, false);
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

            Data mDataInner = mProductItemListing.get(position);
            String[] variant;

            holder.tvItemName.setText(mDataInner.getProduct().getName());

            holder.tvItemBrand.setText(mDataInner.getProduct().getBrand().getName());
            holder.tvDiscountedPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(Double.parseDouble(mDataInner.getProduct().getNewDefaultPrice())));


            if (mDataInner.getProduct().getVegNonvegType() != null) {
                if (!mDataInner.getProduct().getVegNonvegType().equals("veg")) {
                    holder.ivVeg.setVisibility(View.GONE);
                } else {
                    holder.ivVeg.setVisibility(View.VISIBLE);
                }
            }

            if (mDatabaseHandler.CheckIsDataAlreadyInDBorNot(String.valueOf(mDataInner.getProduct().getId()))) {
                holder.btnAddToCart.setVisibility(View.GONE);
                holder.llAddToCart.setVisibility(View.VISIBLE);
                holder.tvQuantity.setText("" + mDatabaseHandler.checkAndSendProductQtyById(String.valueOf(mDataInner.getProduct().getId())));
            } else {
                holder.btnAddToCart.setVisibility(View.VISIBLE);
                holder.llAddToCart.setVisibility(View.GONE);
            }


            if (mDataInner.getProduct().getChannelPrice() != null || Double.parseDouble(mDataInner.getProduct().getChannelPrice()) != 0) {
                Double getChannel_price = Double.parseDouble(mDataInner.getProduct().getChannelPrice());
                Double getNew_default_price_unit = Double.parseDouble(mDataInner.getProduct().getNewDefaultPriceUnit());
                String discountPrice=mDataInner.getProduct().getDiscountAmount();
                //  if (mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getPrice() > mHitInner.getSource().getChannelCurrencyProductPrice().get(i).getNewDefaultPriceUnit()) {
                if (discountPrice!=null&&!discountPrice.isEmpty()&&Double.parseDouble(discountPrice) > 0.0) {
              //  if (getChannel_price > getNew_default_price_unit) {
                    holder.tvDiscountedPrice.setTextColor(Color.parseColor("#C32D4A"));
                    holder.tvOriginalPrice.setVisibility(View.VISIBLE);
                    holder.tvOriginalPrice.setPaintFlags(holder.tvOriginalPrice.getPaintFlags() | Paint.STRIKE_THRU_TEXT_FLAG);
                    holder.tvOriginalPrice.setText("" + Constants.VARIABLES.CURRENT_CURRENCY + " " + Constants.twoDecimalRoundOff(getChannel_price));
                    Typeface typeface = ResourcesCompat.getFont(mContext, R.font.proxima_bold);
                    holder.tvDiscountedPrice.setTypeface(typeface);

                    if (!mDataInner.getProduct().getDiscType().isEmpty()) {
                        if (mDataInner.getProduct().getDiscType().equals("1")) // % wise
                        {
                            holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                            holder.tvDiscountOffer.setText( mDataInner.getProduct().getDiscountAmount() + mContext.getResources().getString(R.string._pen_off));

                        } else { // Currency wise
                            holder.tvDiscountOffer.setVisibility(View.VISIBLE);
                            holder.tvDiscountOffer.setText( Constants.VARIABLES.CURRENT_CURRENCY + " " + mDataInner.getProduct().getDiscountAmount() + mContext.getResources().getString(R.string._off));
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
            variant = new String[1];
            variant[0] = mDataInner.getProduct().getName();
            //setDropdownVariant(holder.actvVariant, variant);

            try {



                        String imageUrl = "https://d1fw2ui0wj5vn1.cloudfront.net/Lifco/lifco/product/400x400/" + mDataInner.getProduct().getProductImage().get(0).getImg();


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


                //   System.out.println("Rahul : ItemListingAdapter : mProductItemListingImages : " + mProductItemListing.get(position).getSource().getProductImages().get(0).getLink() + mHitInner.getSource().getProductImages().get(i).getImg());

            } catch (Exception e) {
                System.out.println("Rahul : GlideExceptiion : " + e.getMessage());
                Glide.with(mContext)
                        .load(R.drawable.image_not_available)

                        .into(holder.ivItemImage);
                //isImageError[0] = true;
            }

/*            try {
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
                                           //     .diskCacheStrategy(DiskCacheStrategy.NONE) .skipMemoryCache(true)
                                                .into(holder.ivItemImage);
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
            } catch (Exception e) {
                System.out.println("Rahul : GlideExceptiion : " + e.getMessage());
                Glide.with(mContext)
                        .load(R.drawable.image_not_available)
                      //  .diskCacheStrategy(DiskCacheStrategy.NONE) .skipMemoryCache(true)
                        .into(holder.ivItemImage);
            }*/


            holder.btnAddToCart.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
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
                        bsp_itemClick_interface.connectMain(mDataInner.getProduct().getId(), 1,position);
                    }



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
                        holder.llAddToCart.setVisibility(View.GONE);
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

            /*holder.ivSavelist.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    mProductListingInterface.savelist(String.valueOf(mDataInner.getProduct().getId()));

                }
            });*/

            String Oum = mProductItemListing.get(position).getProduct().getUom();
            String weight = mProductItemListing.get(position).getProduct().getWeight();



            if (Oum != null && weight !=null&&!Oum.isEmpty()&&!weight.isEmpty()) {
                holder.tvUOM.setText(weight+ " "+Oum);
            }else{
                holder.tvUOM.setVisibility(View.GONE);
            }




        } else if (argholder instanceof FooterViewHolder) {


        }


    }

    @Override
    public int getItemCount() {

        /*if(mProductItemListing.size()>=6){
            return 6;
        }else{
            return mProductItemListing.size() + 1;
        }*/
        return mProductItemListing.size();

    }

    /*@Override
    public int getItemViewType(int position) {
        if (position == mProductItemListing.size()) {
            return TYPE_FOOTER;
        }
        return TYPE_ITEM;
    }*/

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
           // tvGrams = view.findViewById(R.id.tvGrams);
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
