package com.gogrocery.Fragment;

import android.content.Intent;
import androidx.databinding.DataBindingUtil;
import android.os.Bundle;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.gogrocery.Adapters.SideMenuChildAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Interfaces.ActivityRedirection;
import com.gogrocery.Interfaces.CallbackToBack;
import com.gogrocery.Models.SideMenuModel.Child;
import com.gogrocery.Models.SideMenuModel.MenuBar;
import com.gogrocery.view.CategoryFragment;
import com.gogrocery.view.ProductListingPage;
import com.gogrocery.R;
import com.gogrocery.databinding.FragmentSideMenuChildBinding;
import com.google.gson.Gson;

import java.util.ArrayList;
import java.util.List;


public class FragmentSideMenuChild extends Fragment implements ActivityRedirection {


    private FragmentSideMenuChildBinding mFragmentSideMenuChildBinding;
    private SideMenuChildAdapter mSideMenuChildAdapter;
    private List<Child> mSideMenuChildList = new ArrayList<>();
   // CallbackToBack callback;
    private String childJSONResponse;


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment

        mFragmentSideMenuChildBinding = DataBindingUtil.inflate(
                inflater, R.layout.fragment_side_menu_child, container, false);
        View view = mFragmentSideMenuChildBinding.getRoot();

        String splitRes = getArguments().getString("extraInfo");
        System.out.println("Rahul : FragmentSideMenuChild : splitRes : " + splitRes);
        childJSONResponse = splitRes.split("#GoGrocery#")[0];
        mFragmentSideMenuChildBinding.tvParentName.setText(splitRes.split("#GoGrocery#")[1]);


        mFragmentSideMenuChildBinding.ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
               /* ((RegisterVehicleSteps) getActivity()).currentFragPosition = 4;
                ((RegisterVehicleSteps) getActivity()).onBackPressed();*/
           /*   getActivity().onBackPressed();*/
                //callback.onclick();
                backtoPrevious();
            }
        });

        setPageUI();
        return view;


    }

    public void backtoPrevious(){
        ((CategoryFragment)getActivity()).backTo();
    }

    private void setPageUI() {


        setSideMenuRecyclerView();
        Gson mGson = new Gson();
        MenuBar mChild = mGson.fromJson(childJSONResponse, MenuBar.class);
        mSideMenuChildList.addAll(mChild.getChild());
    }

    private void setSideMenuRecyclerView() {
        mSideMenuChildAdapter = new SideMenuChildAdapter(getContext(), mSideMenuChildList, this);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(getContext(), LinearLayoutManager.VERTICAL, false);
        mFragmentSideMenuChildBinding.rvChildMenu.setLayoutManager(mLayoutManager);
        mFragmentSideMenuChildBinding.rvChildMenu.addItemDecoration(new DividerItemDecoration(getContext(), LinearLayoutManager.VERTICAL));
        mFragmentSideMenuChildBinding.rvChildMenu.setItemAnimator(new DefaultItemAnimator());
        mFragmentSideMenuChildBinding.rvChildMenu.setAdapter(mSideMenuChildAdapter);
        mFragmentSideMenuChildBinding.rvChildMenu.setNestedScrollingEnabled(false);
    }

    @Override
    public void redirect(String argWhich, String argPageTitle) {
        Intent shop_by_brand = new Intent(getActivity(), ProductListingPage.class);
        shop_by_brand.putExtra("PageTitle", argPageTitle.split("#GoGrocery#")[1]);
        shop_by_brand.putExtra("Category_slug", argPageTitle.split("#GoGrocery#")[0]); // extra info is category_slug
        startActivity(shop_by_brand);
        Constants.VARIABLES.FILTER_TYPE = "category";
    }
}
