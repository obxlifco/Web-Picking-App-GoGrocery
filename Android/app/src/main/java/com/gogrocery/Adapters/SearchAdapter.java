package com.gogrocery.Adapters;

import android.content.Context;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.gogrocery.Interfaces.SingleStringPassingInterface;
import com.gogrocery.R;

import java.util.List;


public class SearchAdapter extends RecyclerView.Adapter<SearchAdapter.MyViewHolder> {


    private Context mContext;
    private List<String> mRecentSearchModelList;
    private SingleStringPassingInterface mSingleStringPassingInterface;


    public SearchAdapter(Context mContext, List<String> mRecentSearchModelList,SingleStringPassingInterface mSingleStringPassingInterface) {

        this.mContext = mContext;
        this.mRecentSearchModelList = mRecentSearchModelList;
        this.mSingleStringPassingInterface=mSingleStringPassingInterface;
        System.out.println("Rahul : SearchAdapter : mRecentSearchModelList : " + mRecentSearchModelList.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.recent_search_row, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        String mRecentSearchModelInner = mRecentSearchModelList.get(position);

        holder.tvName.setText(mRecentSearchModelInner);

        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mSingleStringPassingInterface.passValue(holder.tvName.getText().toString());
            }
        });


    }


    @Override
    public int getItemCount() {

        if (mRecentSearchModelList.size() > 12) {
            return 12;
        } else {
            return mRecentSearchModelList.size();
        }
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {


        private TextView tvName;


        public MyViewHolder(View view) {
            super(view);


            tvName = view.findViewById(R.id.tvName);


        }

    }


}
