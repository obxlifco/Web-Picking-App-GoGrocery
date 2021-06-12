package com.gogrocery.Adapters;

import android.content.Context;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CheckBox;
import android.widget.LinearLayout;

import com.gogrocery.Constants.Constants;
import com.gogrocery.view.FilterActivity;
import com.gogrocery.Interfaces.FilterRightMenuInterface;
import com.gogrocery.Models.FilterModel.Child;
import com.gogrocery.R;
import com.gogrocery.view.FilterActivityNew;
import com.gogrocery.view.MainActivityNew;

import java.util.List;


public class FilterRightSideMenuAdapter extends RecyclerView.Adapter<FilterRightSideMenuAdapter.MyViewHolder> {


    private Context mContext;
    private List<Child> mFilterModelList;
    private FilterRightMenuInterface mFilterRightMenuInterface;
    private FilterActivityNew argFilterType;
    private LinearLayout.LayoutParams params;

    public FilterRightSideMenuAdapter(Context mContext,
                                      List<Child> mFilterModelList, FilterRightMenuInterface mFilterRightMenuInterface, FilterActivityNew argFilterType) {
        this.mContext = mContext;
        this.mFilterModelList = mFilterModelList;
        this.argFilterType = argFilterType;
        this.mFilterRightMenuInterface = mFilterRightMenuInterface;

    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.filter_right_menu_row, parent, false);
        params = new LinearLayout.LayoutParams(0, 0);

        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        Child mFilterModelInner = mFilterModelList.get(position);

        holder.cbRightMenuTitle.setText(mFilterModelInner.getName());
        if (Constants.VARIABLES.mFilterAddedList.contains(mFilterModelInner.getName())) {
            holder.cbRightMenuTitle.setChecked(true);
        } else {
            holder.cbRightMenuTitle.setChecked(false);
        }


        if (mFilterModelInner.getName() == null || mFilterModelInner.getName().isEmpty()) {
            holder.itemView.setLayoutParams(params);
        }
     /*   holder.cbRightMenuTitle.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {

                System.out.println("Rahul : FilterRightSideMenuAdapter : argFilterType : " + argFilterType);
                System.out.println("Rahul : FilterRightSideMenuAdapter : getId : " + mFilterModelInner.getId());
                if (argFilterType.mFilterType.toLowerCase().equals("price")) {
                    if (isChecked) {
                        mFilterRightMenuInterface.addFilters(argFilterType.mFilterType, mFilterModelInner.getMin() + "-" + mFilterModelInner.getMax(), "add");
                    } else {
                        mFilterRightMenuInterface.addFilters(argFilterType.mFilterType, mFilterModelInner.getMin() + "-" + mFilterModelInner.getMax(), "remove");

                    }
                } else if (argFilterType.mFilterType.toLowerCase().equals("brand")) {
                    double brndid = (double) mFilterModelInner.getId();
                    int brn = (int) brndid;
                    if (isChecked) {
                        mFilterRightMenuInterface.addFilters(argFilterType.mFilterType, String.valueOf(brn), "add");
                    } else {
                        mFilterRightMenuInterface.addFilters(argFilterType.mFilterType, String.valueOf(brn), "add");

                    }


                } else {
                    if (isChecked) {
                        mFilterRightMenuInterface.addFilters(argFilterType.mFilterType, mFilterModelInner.getName(), "add");
                    } else {
                        mFilterRightMenuInterface.addFilters(argFilterType.mFilterType, mFilterModelInner.getName(), "remove");

                    }
                }

                if (isChecked) {
                    Constants.VARIABLES.mFilterAddedList.add(mFilterModelInner.getName());
                } else {
                    Constants.VARIABLES.mFilterAddedList.remove(mFilterModelInner.getName());
                }
            }
        });*/

        holder.cbRightMenuTitle.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                System.out.println("Rahul : FilterRightSideMenuAdapter : argFilterType : " + argFilterType);
                // System.out.println("Rahul : FilterRightSideMenuAdapter : getId : " + mFilterModelInner.getId());
                if (argFilterType.mFilterType.toLowerCase().equals("categories")) {
                    if (holder.cbRightMenuTitle.isChecked()) {
                        mFilterRightMenuInterface.addFilters(argFilterType.mFilterType, mFilterModelInner.getId(), "add");
                    } else {
                        mFilterRightMenuInterface.addFilters(argFilterType.mFilterType, mFilterModelInner.getId(), "remove");

                    }
                } else if (argFilterType.mFilterType.toLowerCase().equals("price")) {
                    if (holder.cbRightMenuTitle.isChecked()) {
                        mFilterRightMenuInterface.addFilters(argFilterType.mFilterType, mFilterModelInner.getMin() + "-" + mFilterModelInner.getMax(), "add");
                    } else {
                        mFilterRightMenuInterface.addFilters(argFilterType.mFilterType, mFilterModelInner.getMin() + "-" + mFilterModelInner.getMax(), "remove");

                    }
                } else if (argFilterType.mFilterType.toLowerCase().equals("brand")) {
                   /* double brndid = (double) mFilterModelInner.getId();
                    int brn = (int) brndid;*/
                    if (holder.cbRightMenuTitle.isChecked()) {
                        mFilterRightMenuInterface.addFilters(argFilterType.mFilterType, mFilterModelInner.getId(), "add");
                    } else {
                        mFilterRightMenuInterface.addFilters(argFilterType.mFilterType, mFilterModelInner.getId(), "remove");

                    }


                } else {
                    if (holder.cbRightMenuTitle.isChecked()) {
                        mFilterRightMenuInterface.addFilters(argFilterType.mFilterType, mFilterModelInner.getName(), "add");
                    } else {
                        mFilterRightMenuInterface.addFilters(argFilterType.mFilterType, mFilterModelInner.getName(), "remove");

                    }
                }

                if (holder.cbRightMenuTitle.isChecked()) {
                    Constants.VARIABLES.mFilterAddedList.add(mFilterModelInner.getName());
                } else {
                    Constants.VARIABLES.mFilterAddedList.remove(mFilterModelInner.getName());
                }
            }
        });

    }


    @Override
    public int getItemCount() {
        return mFilterModelList.size();
    }


    public class MyViewHolder extends RecyclerView.ViewHolder {


        private CheckBox cbRightMenuTitle;


        public MyViewHolder(View view) {
            super(view);


            cbRightMenuTitle = view.findViewById(R.id.cbRightMenuTitle);


        }

    }


}
