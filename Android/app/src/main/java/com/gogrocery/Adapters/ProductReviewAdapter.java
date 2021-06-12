package com.gogrocery.Adapters;

import android.content.Context;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.gogrocery.Constants.Constants;
import com.gogrocery.Interfaces.ActivityRedirection;
import com.gogrocery.Models.RatingReviewModel.ReviewData;
import com.gogrocery.R;

import java.util.List;


public class ProductReviewAdapter extends RecyclerView.Adapter<ProductReviewAdapter.MyViewHolder> {


    private Context mContext;
    private List<ReviewData> mReviewDataList;
    private ActivityRedirection mActivityRedirectionListner;


    public ProductReviewAdapter(Context mContext,
                                List<ReviewData> mReviewDataList) {

        this.mContext = mContext;
        this.mReviewDataList = mReviewDataList;

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.review_and_rating_row, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        try {
            ReviewData mReviewDataInner = mReviewDataList.get(position);
            holder.tvRating.setText("" + mReviewDataInner.getRating());
            holder.tvReviewTitle.setText(mReviewDataInner.getTitle());
            holder.tvReviewDescription.setText(mReviewDataInner.getReview());
            String date = mReviewDataInner.getCreated().split("T")[0].split("-")[2];
            String order = "";
            if (date.substring((date.length() - 1), date.length()).equals("1")) {
                order = "st";
            } else if (date.substring((date.length() - 1), date.length()).equals("2")) {
                order = "nd";
            } else if (date.substring((date.length() - 1), date.length()).equals("3")) {
                order = "rd";
            } else {
                order = "th";

            }

            switch (mReviewDataInner.getRating()) {
                case 1:
                    holder.llrating.setBackground(mContext.getResources().getDrawable(R.drawable.one_rating_single_bg));
                    break;
                case 2:
                    holder.llrating.setBackground(mContext.getResources().getDrawable(R.drawable.two_rating_single_bg));
                    break;
                case 3:
                    holder.llrating.setBackground(mContext.getResources().getDrawable(R.drawable.five_rating_single_bg));
                    break;
                case 4:
                    holder.llrating.setBackground(mContext.getResources().getDrawable(R.drawable.five_rating_single_bg));
                    break;
                case 5:
                    holder.llrating.setBackground(mContext.getResources().getDrawable(R.drawable.five_rating_single_bg));
                    break;
                default:
                    break;
            }

            holder.tvReviewNameNDate.setText(mReviewDataInner.getUserName() + ", " +
                    mReviewDataInner.getCreated().split("T")[0].split("-")[2] + order + " " +
                    Constants.getSeperateValuesFromDate(mReviewDataInner.getCreated().split("T")[0], 3) + " " +
                    mReviewDataInner.getCreated().split("T")[0].split("-")[0]);

        } catch (Exception e) {

        }
    }


    @Override
    public int getItemCount() {
        return mReviewDataList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {

        private TextView tvRating, tvReviewTitle, tvReviewDescription, tvReviewNameNDate;
        private LinearLayout llrating;

        public MyViewHolder(View view) {
            super(view);

            tvRating = view.findViewById(R.id.tvRating);
            tvReviewTitle = view.findViewById(R.id.tvReviewTitle);
            tvReviewDescription = view.findViewById(R.id.tvReviewDescription);
            tvReviewNameNDate = view.findViewById(R.id.tvReviewNameNDate);
            llrating = view.findViewById(R.id.llrating);


        }

    }


}
