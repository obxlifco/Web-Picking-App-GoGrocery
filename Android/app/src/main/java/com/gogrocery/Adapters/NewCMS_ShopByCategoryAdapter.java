package com.gogrocery.Adapters;

import android.content.Context;
import android.graphics.Color;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.engine.DiskCacheStrategy;
import com.bumptech.glide.request.RequestOptions;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Interfaces.ActivityRedirection;
import com.gogrocery.Interfaces.CallbackOnSelectCategory;
import com.gogrocery.Models.CMS_NEW_Model.ShopByCategory;
import com.gogrocery.Models.SideMenuModel.MenuBar;
import com.gogrocery.R;

import java.util.List;


public class NewCMS_ShopByCategoryAdapter extends RecyclerView.Adapter<NewCMS_ShopByCategoryAdapter.MyViewHolder> {


    private Context mContext;
    private List<com.gogrocery.Models.SideMenuModel.MenuBar> mCMS_parentCategoryLists;
    private CallbackOnSelectCategory mActivityRedirectionListner;
    private String[] colorcode = {"#F96C26", "#F35355", "#C3386E", "#2F6CA8", "#3CB9E2", "#3AC47B", "#90B85C", "#E7B13D", "#F96C26", "#F35355", "#C3386E", "#2F6CA8", "#3CB9E2", "#3AC47B", "#90B85C", "#E7B13D", "#F96C26", "#F35355", "#C3386E", "#2F6CA8", "#3CB9E2", "#3AC47B", "#90B85C", "#E7B13D",
            "#F96C26", "#F35355", "#C3386E", "#2F6CA8", "#3CB9E2", "#3AC47B", "#90B85C", "#E7B13D", "#F96C26", "#F35355", "#C3386E", "#2F6CA8", "#3CB9E2", "#3AC47B", "#90B85C", "#E7B13D", "#F96C26", "#F35355", "#C3386E", "#2F6CA8", "#3CB9E2", "#3AC47B", "#90B85C", "#E7B13D",
            "#F96C26", "#F35355", "#C3386E", "#2F6CA8", "#3CB9E2", "#3AC47B", "#90B85C", "#E7B13D"};
 /*   private int[] img={R.drawable.artboard_1,R.drawable.artboard_2,R.drawable.artboard_3,R.drawable.artboard_4,R.drawable.artboard_5,
            R.drawable.artboard_6,R.drawable.artboard_7,R.drawable.artboard_8,R.drawable.artboard_9,R.drawable.artboard_10,
            R.drawable.artboard_11,R.drawable.artboard_12,R.drawable.artboard_13,R.drawable.artboard_14,R.drawable.artboard_15};*/

/*    private int[] img_sel={R.drawable.artboard_1_sel,R.drawable.artboard_2_sel,R.drawable.artboard_3_sel,R.drawable.artboard_4_sel,R.drawable.artboard_5_sel,
            R.drawable.artboard_6_sel,R.drawable.artboard_7_sel,R.drawable.artboard_8_sel,R.drawable.artboard_9_sel,R.drawable.artboard_10_sel,
            R.drawable.artboard_11_sel,R.drawable.artboard_12_sel,R.drawable.artboard_13_sel,R.drawable.artboard_14_sel,R.drawable.artboard_15_sel};*/
    private String[] names={"Bakery","Babies","Beverages","Canned","Dairy",
            "Bakery","Babies","Beverages","Canned","Dairy",
            "Bakery","Babies","Beverages","Canned","Dairy"};
    private int checkedPosition = 0;

    private LinearLayout.LayoutParams params;
    private int colorCode = 0,row_index=0;

    public NewCMS_ShopByCategoryAdapter(Context mContext,
                                        List<com.gogrocery.Models.SideMenuModel.MenuBar> mCMS_parentCategoryLists, CallbackOnSelectCategory mActivityRedirectionListner) {

        this.mContext = mContext;
        this.mCMS_parentCategoryLists = mCMS_parentCategoryLists;
        this.mActivityRedirectionListner = mActivityRedirectionListner;
        System.out.println("Rahul : DealsOfTheDayAdapter : mDealsOfTheDayDataList : " + mCMS_parentCategoryLists.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.shop_by_category_row, parent, false);
        params = new LinearLayout.LayoutParams(0, 0);

        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        MenuBar mMenuBarInner = mCMS_parentCategoryLists.get(position);
        try {
        holder.tvCategoryName.setText(mMenuBarInner.getName());
        System.out.println("Rahul : NewCMS_ShopByCategoryAdapter : ImageLink : " + mMenuBarInner.getName() + "Positions : " + position + " : " + Constants.IMAGE_URL_CATEGOERY + mMenuBarInner.getImage());
        //http://lifcogrocery.s3.amazonaws.com/Lifco/lifco/category/200x200/HeaderImage_beverages--juices.png

         //if (!(mMenuBarInner.getImage().isEmpty())) {
        Glide.with(mContext)
                .load(Constants.IMAGE_URL_CATEGOERY + mMenuBarInner.getImage())
                .apply(new RequestOptions().override(200, 200))
                //.diskCacheStrategy(DiskCacheStrategy.NONE) .skipMemoryCache(true)
                .into(holder.ivCategory);


            System.out.println("Rahul : NewCMS_ShopByCategoryAdapter : position : " + position);
            System.out.println("Rahul : NewCMS_ShopByCategoryAdapter : colorcode : " + colorcode.length);
                if(position>colorcode.length)
                {
                    System.out.println("Rahul : NewCMS_ShopByCategoryAdapter : if : ");
                    colorCode=0;
                }
        } catch (IndexOutOfBoundsException exc) {
            System.out.println("Rahul : NewCMS_ShopByCategoryAdapter : catch : ");

        }


        if (checkedPosition == -1) {
            holder.rlBg.setVisibility(View.VISIBLE);
            holder.rlBg.setBackgroundResource(R.drawable.oval_selected);

        } else {
            if (checkedPosition == position) {
                holder.rlBg.setVisibility(View.VISIBLE);
                holder.rlBg.setBackgroundResource(R.drawable.oval_selected);

            } else {
                holder.rlBg.setVisibility(View.VISIBLE);
                holder.rlBg.setBackgroundResource(R.drawable.bg_parent_category);

            }
        }
       /* } else {
            holder.itemView.setLayoutParams(params);
        }*/
        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
          /*      row_index=position;
                notifyDataSetChanged();*/

                holder.rlBg.setVisibility(View.VISIBLE);
                holder.rlBg.setBackgroundResource(R.drawable.oval_selected);

                if (checkedPosition !=position) {
                    notifyItemChanged(checkedPosition);
                    checkedPosition = position;
                }

                mActivityRedirectionListner.onSelectCategory( mCMS_parentCategoryLists.get(position).getChild(),"sbcMain", mMenuBarInner.getName() + "#GoGrocery#" + mMenuBarInner.getSlug() + "#GoGrocery#" + mMenuBarInner.getParentId());
            }
        });

       // holder.tvCategoryName.setText(names[position]);
   /*     if(row_index==position){
            holder.rlBg.setBackground(mContext.getResources().getDrawable(R.drawable.bg_sel_parent_category));
            Glide.with(mContext)
                    .load(img_sel[position])
                    .apply(new RequestOptions().override(200, 200))
                    //.diskCacheStrategy(DiskCacheStrategy.NONE) .skipMemoryCache(true)
                    .into(holder.ivCategory);
        }
        else
        {
            holder.rlBg.setBackground(mContext.getResources().getDrawable(R.drawable.bg_parent_category));
            Glide.with(mContext)
                    .load(img[position])
                    .apply(new RequestOptions().override(200, 200))
                    //.diskCacheStrategy(DiskCacheStrategy.NONE) .skipMemoryCache(true)
                    .into(holder.ivCategory);
        }*/


    }


    @Override
    public int getItemCount() {
        return mCMS_parentCategoryLists.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {

        private ImageView ivCategory;
        private TextView tvCategoryName;
        private RelativeLayout rlBg;


        public MyViewHolder(View view) {
            super(view);


            ivCategory = view.findViewById(R.id.ivCategory);
            tvCategoryName = view.findViewById(R.id.tvCategoryName);
            rlBg = view.findViewById(R.id.rlBg);


        }

    }


}
