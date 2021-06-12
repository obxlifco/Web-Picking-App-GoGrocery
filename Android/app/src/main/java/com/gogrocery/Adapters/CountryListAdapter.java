package com.gogrocery.Adapters;

import android.content.Context;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Filter;
import android.widget.Filterable;
import android.widget.TextView;

import com.gogrocery.Interfaces.CountryStateListListner;
import com.gogrocery.Models.CountryListModel.Data;
import com.gogrocery.R;
import com.google.gson.Gson;

import java.util.ArrayList;
import java.util.List;


public class CountryListAdapter extends RecyclerView.Adapter<CountryListAdapter.MyViewHolder> implements Filterable {


    private Context mContext;
    private List<Data> mCountryDatalist;
    private CountryStateListListner mCountryStateListListner;
    private List<Data> mCountryListModelFilteredList;

    public CountryListAdapter(Context mContext,
                              List<Data> mCountryDatalist, CountryStateListListner mCountryStateListListner) {

        this.mContext = mContext;
        this.mCountryDatalist = mCountryDatalist;
        this.mCountryStateListListner = mCountryStateListListner;
        mCountryListModelFilteredList = mCountryDatalist;
        System.out.println("Rahul : CountryListAdapter : mCountryDatalist : " + mCountryDatalist.size());

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.single_text_row, parent, false);


        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        Data mDataInner = mCountryListModelFilteredList.get(position);

        System.out.println("Rahul : CountryListAdapter : mCountryDatalist : mDataInner.getCountryName() :  " + mDataInner.getCountryName());
        holder.tvTitle.setText(mDataInner.getCountryName());
        System.out.println("Rahul : CountryListAdapter : mCountryDatalist : holder.tvTitle :  " + holder.tvTitle.getText().toString());

        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mCountryStateListListner.passID("country", mDataInner.getId(), mDataInner.getCountryName());
            }
        });
    }



    @Override
    public int getItemCount() {
        return mCountryListModelFilteredList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {


        private TextView tvTitle;


        public MyViewHolder(View view) {
            super(view);


            tvTitle = view.findViewById(R.id.tvTitle);


        }

    }
    @Override
    public Filter getFilter() {
        return new Filter() {
            @Override
            protected FilterResults performFiltering(CharSequence charSequence) {
                String charString = charSequence.toString();
                System.out.println("Rahul : PaymentHistoryAdapter : getFilter : " + charString);
                if (charString.isEmpty()) {
                    mCountryListModelFilteredList = mCountryDatalist;
                } else {
                    List<Data> filteredList = new ArrayList<>();
                    for (Data row : mCountryDatalist) {

                        // name match condition. this might differ depending on your requirement
                        // here we are looking for name or phone number match
                        if (row.getCountryName().toLowerCase().contains(charString.toLowerCase())) {
                            filteredList.add(row);
                        }
                    }

                    mCountryListModelFilteredList = filteredList;

                }

                FilterResults filterResults = new FilterResults();
                filterResults.values = mCountryListModelFilteredList;
                return filterResults;
            }

            @Override
            protected void publishResults(CharSequence charSequence, FilterResults filterResults) {
                mCountryListModelFilteredList = (ArrayList<Data>) filterResults.values;

                System.out.println("Rahul : PaymentHistoryAdapter : mPaymentHistoryModelFilteredList : " + new Gson().toJson(mCountryListModelFilteredList));
                if (mCountryListModelFilteredList.size() == 0) {
                    mCountryListModelFilteredList = mCountryDatalist;
                }

                // refresh the list with filtered data
                notifyDataSetChanged();
                // notifyDataSetChanged();
                //  notifyDataSetChanged();
                //  ((PaymentHistory)getActivity()) notifyDataSetChanged();
            }
        };
    }
}
