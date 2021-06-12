package com.gogrocery.Adapters;

import android.content.Context;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.PopupMenu;
import android.widget.TextView;

import com.gogrocery.Interfaces.SaveListInterface;
import com.gogrocery.Interfaces.WarehouseItemClickListner;
import com.gogrocery.Models.SaveListModel.SaveListData;
import com.gogrocery.R;
import com.gogrocery.view.SaveListPage;

import java.util.List;


public class SaveListAdapter extends RecyclerView.Adapter<SaveListAdapter.MyViewHolder> {


    private Context mContext;
    private List<SaveListData> mSaveListDataList;
    private WarehouseItemClickListner mWarehouseItemClickListner;
    private SaveListInterface mSaveListInterface;

    public SaveListAdapter(Context mContext,
                           List<SaveListData> mSaveListDataList, SaveListInterface mSaveListInterface) {

        this.mContext = mContext;
        this.mSaveListDataList = mSaveListDataList;
        this.mSaveListInterface = mSaveListInterface;
        System.out.println("Rahul : SaveListAdapter : mSaveListDataList : " + mSaveListDataList.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.my_save_list_row, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {

        try {

            SaveListData mDataInner = mSaveListDataList.get(position);

            holder.tvSavelitsTitle.setText(mDataInner.getSavelistName());
            holder.tvDateNCount.setText(mDataInner.getCreated().split("T")[0].split("-")[2] + "/" +
                    mDataInner.getCreated().split("T")[0].split("-")[1] + "/" +
                    mDataInner.getCreated().split("T")[0].split("-")[0] + " | " + mDataInner.getCount() + " Items");

            holder.itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    String check = ((SaveListPage) mContext).product_id;
                    if (check.isEmpty()) {
                        mSaveListInterface.getInfo(mDataInner.getSavelistName()+"#GOGROCERY#"+mDataInner.getSlug(), "slug");

                    } else {
                        mSaveListInterface.getInfo(mDataInner.getId() + "#GoGrocery#" + mDataInner.getProductIds(), "add");
                    }

                }
            });


            holder.ivMore.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    PopupMenu popup = new PopupMenu(mContext, v);

                    popup.inflate(R.menu.save_list_menu);

                    popup.setOnMenuItemClickListener(new PopupMenu.OnMenuItemClickListener() {
                        @Override
                        public boolean onMenuItemClick(MenuItem item) {
                            switch (item.getItemId()) {
                                case R.id.edit:
                                    mSaveListInterface.getInfo(holder.tvSavelitsTitle.getText().toString() + "#GoGrocery#" + mDataInner.getId(), "edit");
                                    break;


                                case R.id.delete:
                                    mSaveListInterface.getInfo(mDataInner.getId(), "delete");
                                    break;

                            }
                            return false;
                        }


                    });

                    popup.show();
                }
            });


        } catch (Exception e) {
            System.out.println("Rahul : SaveListAdapter : " + e.getMessage());
        }

    }


    @Override
    public int getItemCount() {
        return mSaveListDataList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {

        private TextView tvSavelitsTitle, tvDateNCount;
        private ImageView ivMore;

        public MyViewHolder(View view) {
            super(view);


            tvSavelitsTitle = view.findViewById(R.id.tvSavelitsTitle);
            tvDateNCount = view.findViewById(R.id.tvDateNCount);
            ivMore = view.findViewById(R.id.ivMore);

        }

    }


}
