package com.gogrocery.Adapters;

import android.app.Activity;
import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.recyclerview.widget.RecyclerView;

import com.gogrocery.Interfaces.ActivityRedirection;
import com.gogrocery.Models.SideMenuModel.Child;
import com.gogrocery.R;

import java.util.ArrayList;
import java.util.List;

public class NewSubCatAdapter  extends RecyclerView.Adapter<NewSubCatAdapter.ViewHolder> {

    private Activity activity;
    private List<Child> mCMS_parentCategoryLists;
    private ActivityRedirection mActivityRedirectionListner;


    private int checkedPosition = 0;

    public NewSubCatAdapter(Activity activity) {
        this.activity = activity;
        mCMS_parentCategoryLists = new ArrayList<>();

    }


    @Override
    public NewSubCatAdapter.ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        // infalte the item Layout
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.child_text_row, parent, false);
        // set the view's size, margins, paddings and layout parameters
        NewSubCatAdapter.ViewHolder viewholder = new NewSubCatAdapter.ViewHolder(v);
        return viewholder;
    }

    @Override
    public void onBindViewHolder(NewSubCatAdapter.ViewHolder holder, final int position) {


        holder.tvCategoryName.setText(mCMS_parentCategoryLists.get(position).getName());
        if (checkedPosition == -1) {
            holder.tvCategoryName.setVisibility(View.VISIBLE);
            holder.tvCategoryName.setBackgroundResource(R.drawable.tab_background_unselected);
            holder.tvCategoryName.setTextColor(Color.parseColor("#575757"));
        } else {
            if (checkedPosition == position) {
                holder.tvCategoryName.setVisibility(View.VISIBLE);
                holder.tvCategoryName.setBackgroundResource(R.drawable.tab_background_selected);
                holder.tvCategoryName.setTextColor(Color.parseColor("#FFFFFF"));
            } else {
                holder.tvCategoryName.setVisibility(View.VISIBLE);
                holder.tvCategoryName.setBackgroundResource(R.drawable.tab_background_unselected);
                holder.tvCategoryName.setTextColor(Color.parseColor("#575757"));
            }
        }

        holder.itemView.setOnClickListener(v->{

            holder.tvCategoryName.setVisibility(View.VISIBLE);
            holder.tvCategoryName.setBackgroundResource(R.drawable.tab_background_selected);
            holder.tvCategoryName.setTextColor(Color.parseColor("#FFFFFF"));
            if (checkedPosition !=position) {
                notifyItemChanged(checkedPosition);
                checkedPosition = position;
            }

            mActivityRedirectionListner.redirect( "sbcMain", mCMS_parentCategoryLists.get(position).getName() + "#GoGrocery#" + mCMS_parentCategoryLists.get(position).getSlug() + "#GoGrocery#" + mCMS_parentCategoryLists.get(position).getParentId());



        });


    }

    @Override
    public int getItemCount() {

        return mCMS_parentCategoryLists.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvCategoryName;// init the item view's


        public ViewHolder(View itemView) {
            super(itemView);
            tvCategoryName = (TextView) itemView.findViewById(R.id.tvTitle);



        }
    }

    public void AddSubcategoryList(List<Child> subCategoryList,int checkedPosition) {
        this.mCMS_parentCategoryLists.addAll(subCategoryList);
       this.checkedPosition=checkedPosition;
    }

    public void clearList() {
        if (mCMS_parentCategoryLists != null) {
            this.mCMS_parentCategoryLists.clear();
        }
    }


    public void setCallback(ActivityRedirection callback) {
        this.mActivityRedirectionListner = callback;
    }

}
 /*extends RecyclerView.Adapter<NewSubCatAdapter.MyViewHolder> {


    private Context mContext;
    private List<Child> mCMS_parentCategoryLists;
    private ActivityRedirection mActivityRedirectionListner;





    public NewSubCatAdapter(Context mContext, ActivityRedirection mActivityRedirectionListner) {
        mCMS_parentCategoryLists= new ArrayList<>();
        this.mContext = mContext;
        this.mActivityRedirectionListner = mActivityRedirectionListner;


    }
    @NonNull
    @Override
    public NewSubCatAdapter.MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.single_text_row, parent, false);

        return new MyViewHolder(itemView);
    }


    @Override
    public void onBindViewHolder(@NonNull NewSubCatAdapter.MyViewHolder holder, int position) {
       // Child mMenuBarInner = mCMS_parentCategoryLists.get(position);
   *//*     try {
            holder.tvCategoryName.setText(mCMS_parentCategoryLists.get(position).getName());

        } catch (IndexOutOfBoundsException exc) {
            System.out.println("Rahul : NewSubCatAdapter : catch : ");

        }*//*
       *//* } else {
            holder.itemView.setLayoutParams(params);
        }*//*





        // holder.tvCategoryName.setText(names[position]);
   *//*     if(row_index==position){
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
        }*//*


    }


    @Override
    public int getItemCount() {
      //  return mCMS_parentCategoryLists.size();
        return names.length;
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {

      //  private ImageView ivCategory;
        private TextView tvCategoryName;
      //  private RelativeLayout rlBg;


        public MyViewHolder(View view) {
            super(view);


            //ivCategory = view.findViewById(R.id.ivCategory);
            tvCategoryName = view.findViewById(R.id.tvTitle);
          //  rlBg = view.findViewById(R.id.rlBg);


        }
    }
*/

//}