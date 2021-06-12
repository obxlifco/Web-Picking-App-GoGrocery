package com.gogrocery.Adapters;

import com.gogrocery.Fragment.SubstituteFragment;
import com.gogrocery.Models.OrderListDetailsModel.OrderProductsItem;

import java.util.List;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentStatePagerAdapter;

public class SubstitutePagerAdapter extends FragmentStatePagerAdapter {
    int numPage;
    List<OrderProductsItem> orderProductsItemList;
    public SubstitutePagerAdapter(@NonNull FragmentManager fm, int behavior, int numPage, List<OrderProductsItem> orderProductsItemList) {
        super(fm, behavior);
        this.numPage=numPage;
        this.orderProductsItemList=orderProductsItemList;
    }

    @NonNull
    @Override
    public Fragment getItem(int position) {
        return SubstituteFragment.newInstance(position,orderProductsItemList.get(position));
    }

    @Override
    public int getCount() {
        return numPage;
    }
}
