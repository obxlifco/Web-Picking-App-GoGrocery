package com.gogrocery.Adapters;

import android.content.Context;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import com.gogrocery.Constants.Constants;
import com.gogrocery.Interfaces.ActivityRedirection;
import com.gogrocery.Models.DetailsPage.VariantProduct;
import com.gogrocery.R;

import java.util.List;


public class ProductVariantAdapter extends RecyclerView.Adapter<ProductVariantAdapter.MyViewHolder> {


    private Context mContext;
    private List<VariantProduct> mVariantProductList;
    private ActivityRedirection mActivityRedirectionListner;


    public ProductVariantAdapter(Context mContext,
                                 List<VariantProduct> mVariantProductList) {

        this.mContext = mContext;
        this.mVariantProductList = mVariantProductList;
        this.mActivityRedirectionListner=mActivityRedirectionListner;
        System.out.println("Rahul : ProductVariantAdapter : mVariantProductList : " + mVariantProductList.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.available_variant, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        VariantProduct mVariantProductInner = mVariantProductList.get(position);


        holder.variantAvailable.setText(mVariantProductInner.getCustomField().get(0).getValue()+" @ "+""+Constants.VARIABLES.CURRENT_CURRENCY+" "+mVariantProductInner.getDefaultPrice());
        holder.variantAvailable.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                holder.variantAvailable.setBackground(mContext.getResources().getDrawable(R.drawable.available_variant_selected));

            }
        });
    }


    @Override
    public int getItemCount() {
        return mVariantProductList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {


        private Button variantAvailable;


        public MyViewHolder(View view) {
            super(view);

            variantAvailable=view.findViewById(R.id.variantAvailable);


        }

    }


}
