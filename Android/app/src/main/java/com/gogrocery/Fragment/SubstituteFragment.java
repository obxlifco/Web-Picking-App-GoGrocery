package com.gogrocery.Fragment;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.bumptech.glide.Glide;
import com.gogrocery.Adapters.SubstituteListAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Customs.GridSpacingItemDecoration;
import com.gogrocery.Interfaces.CustomFieldChooseInterface;
import com.gogrocery.Interfaces.SubstituteListClickListener;
import com.gogrocery.Models.OrderListDetailsModel.OrderProductsItem;
import com.gogrocery.R;
import com.gogrocery.view.DialogPrepareView;
import com.gogrocery.view.MainActivityNew;
import com.gogrocery.view.SubstituteActivity;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import org.json.JSONException;

import de.hdodenhof.circleimageview.CircleImageView;

import static com.facebook.FacebookSdk.getApplicationContext;

public class SubstituteFragment extends Fragment implements SubstituteListClickListener, CustomFieldChooseInterface {
    View view;
    CircleImageView ivPicSubsFrag;
    TextView tvNameSubsFrag,tvWeightSubsFrag,tvPriceSubsFrag,tvReplacementHeader;
    RecyclerView rvSubsFrag;
    OrderProductsItem orderProductsItem;
    int position;
    private SharedPreferenceManager mSharedPreferenceManager;
    SubstituteListAdapter substituteListAdapter;
    public static SubstituteFragment newInstance(int position, OrderProductsItem orderProductsItem) {
        SubstituteFragment fragment = new SubstituteFragment();
        fragment.position = position;
        fragment.orderProductsItem = orderProductsItem;
        return fragment;
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.fragment_substitute, container, false);
        initView(view);
        return view;
    }

    private void initView(View view) {
        rvSubsFrag = view.findViewById(R.id.rvSubsFrag);
        ivPicSubsFrag = view.findViewById(R.id.ivPicSubsFrag);
        tvNameSubsFrag = view.findViewById(R.id.tv_productName);
        tvWeightSubsFrag = view.findViewById(R.id.tv_productWeight);
        tvPriceSubsFrag = view.findViewById(R.id.tv_productPrice);
        tvReplacementHeader = view.findViewById(R.id.tvReplacementHeader);

        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());

        setupDetails();
        setupSubstituteRecycler();
    }

    private void setupDetails() {
        if (orderProductsItem.getProduct().getProductImages().get(0).getLink() != null &&
                orderProductsItem.getProduct().getProductImages().get(0).getLink().length() > 0) {
            Glide.with(getActivity()).load(orderProductsItem.getProduct().getProductImages().get(0).getLink() +
                    orderProductsItem.getProduct().getProductImages().get(0).getImg()).placeholder(R.drawable.dummy_item_img).into(ivPicSubsFrag);
        }
        tvNameSubsFrag.setText(orderProductsItem.getProduct().getName());
/*        Choose Replacemet : Max  \(maxQuantity ?? 0) Quantity"*/
        tvReplacementHeader.setText("Choose Replacement"+" : Max "+orderProductsItem.getShortage()+" Quantity");
        tvWeightSubsFrag.setText(orderProductsItem.getWeight()+" "+orderProductsItem.getProduct().getUom().getUomName());
        tvPriceSubsFrag.setText(mSharedPreferenceManager.getCurrentCurrency()+" "+ Constants.twoDecimalRoundOff(orderProductsItem.getProductPrice()));
    }

    private void setupSubstituteRecycler() {
    //    rvSubsFrag.setLayoutManager(new GridLayoutManager(getActivity(), 3));
        GridLayoutManager mGridLayoutManager = new GridLayoutManager(getApplicationContext(), 3);
        rvSubsFrag.setLayoutManager(mGridLayoutManager);
        rvSubsFrag.addItemDecoration(new GridSpacingItemDecoration(3, GridSpacingItemDecoration.dpToPx(getApplicationContext(), 1), true));
        rvSubsFrag.setItemAnimator(new DefaultItemAnimator());
        substituteListAdapter = new SubstituteListAdapter(getActivity(),orderProductsItem.getSubstituteProducts(), this,orderProductsItem.getShortage(),this);
        rvSubsFrag.setAdapter(substituteListAdapter);
    }

    @Override
    public void substituteListClick(int position) {

    }

    @Override
    public void substituteQuantity(int pos) {
        ((SubstituteActivity)getActivity()).setApprovalDetails(orderProductsItem,position);
        rvSubsFrag.getAdapter().notifyDataSetChanged();
    }

    @Override
    public void selectedCustomFieldValue(int pos, String custom_field_name, String custom_field_value) {

        Intent i = new Intent(getActivity(), DialogPrepareView.class);
        i.putExtra("custom_field_name", custom_field_name);
        i.putExtra("custom_field_value", custom_field_value);
        i.putExtra("product_id", pos+"");
        startActivityForResult(i,101);
    }



    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == 101) {
            if(resultCode == Activity.RESULT_OK){

                try {

                    substituteListAdapter.selectedCustomFieldValue(Integer.parseInt(data.getStringExtra("argProductId")),data.getStringExtra("custom_field_name"),data.getStringExtra("custom_field_value"));
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
