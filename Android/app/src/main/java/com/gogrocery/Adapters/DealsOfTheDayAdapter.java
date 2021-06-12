package com.gogrocery.Adapters;

import android.content.Context;
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
import android.widget.TextView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.DataSource;
import com.bumptech.glide.load.engine.DiskCacheStrategy;
import com.bumptech.glide.load.engine.GlideException;
import com.bumptech.glide.request.RequestListener;
import com.bumptech.glide.request.target.Target;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Models.DealsOfTheDay.Data;
import com.gogrocery.R;

import java.util.List;


public class DealsOfTheDayAdapter extends RecyclerView.Adapter<DealsOfTheDayAdapter.MyViewHolder> {


    private Context mContext;
    private List<Data> mDealsOfTheDayDataList;


    public DealsOfTheDayAdapter(Context mContext,
                                List<Data> mDealsOfTheDayDataList) {

        this.mContext = mContext;
        this.mDealsOfTheDayDataList = mDealsOfTheDayDataList;
        System.out.println("Rahul : DealsOfTheDayAdapter : mDealsOfTheDayDataList : " + mDealsOfTheDayDataList.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.deals_of_the_day_row, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        Data mDataInner = mDealsOfTheDayDataList.get(position);
        String[] variant;
try {
    holder.tvItemName.setText(mDataInner.getName());
    holder.tvItemBrand.setText(mDataInner.getBrand().getName());
    holder.tvDiscountedPrice.setText(""+Constants.VARIABLES.CURRENT_CURRENCY+" "+ mDataInner.getDefaultPrice().trim());
    if (mDataInner.getVegNonvegType() != null) {
        if (!mDataInner.getVegNonvegType().equals("veg")) {
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
    variant[0] = mDataInner.getName();
        /*for (int i = 1; i < mDataInner.getVariantProduct().size(); i++) {
            variant[i] = mDataInner.getVariantProduct().get(i).getName();

        }*/
    setDropdownVariant(holder.actvVariant, variant);
}catch (Exception e){e.printStackTrace();}


        try {
            System.out.println("Rahul : DealsOfTheDayAdapter : IMAGE_BASE_URL : " + Constants.IMAGE_BASE_URL + mDataInner.getProductImage().get(0).getImg());
            Glide.with(mContext)
                    .load(Constants.IMAGE_BASE_URL + "400x400/" + mDataInner.getProductImage().get(0).getImg())
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
                    .diskCacheStrategy(DiskCacheStrategy.NONE) .skipMemoryCache(true)
                    .into(holder.ivItemImage);
        } catch (Exception e) {
            System.out.println("Rahul : GlideExceptiion : " + e.getMessage());
            Glide.with(mContext)
                    .load(R.drawable.image_not_available)
                    .diskCacheStrategy(DiskCacheStrategy.NONE) .skipMemoryCache(true)
                    .into(holder.ivItemImage);
        }


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
        return mDealsOfTheDayDataList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {

        private ImageView ivItemImage, ivVeg;
        private TextView tvItemBrand, tvItemName, tvGrams, tvPrice, tvDiscountedPrice, tvOriginalPrice, tvDiscountOffer;
        private Button btnAddToCart;
        private AutoCompleteTextView actvVariant;

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


        }

    }


}
