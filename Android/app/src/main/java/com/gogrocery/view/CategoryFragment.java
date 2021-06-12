package com.gogrocery.view;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;

import androidx.appcompat.app.AppCompatActivity;
import androidx.databinding.DataBindingUtil;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;
import androidx.recyclerview.widget.LinearLayoutManager;

import com.facebook.appevents.AppEventsConstants;
import com.facebook.appevents.AppEventsLogger;
import com.gogrocery.Adapters.SideMenuCategoryAdapter;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Fragment.FragmentSideMenuChild;
import com.gogrocery.Interfaces.ActivityRedirection;
import com.gogrocery.Interfaces.CallbackToBack;
import com.gogrocery.Models.SideMenuModel.MenuBar;
import com.gogrocery.R;
import com.gogrocery.databinding.FragmentCategoryBinding;
import com.gogrocery.helper.LoadingDialog;
import com.gogrocery.view.MainActivityNew;
import com.gogrocery.view.ProductListingPage;
import com.google.firebase.analytics.FirebaseAnalytics;

import java.util.ArrayList;
import java.util.List;

import static com.facebook.FacebookSdk.getApplicationContext;

public class CategoryFragment extends AppCompatActivity implements ActivityRedirection {
    private List<MenuBar> categoryDetailsList = new ArrayList<>();
    private View rootView;
   private Context mContext;
    FragmentCategoryBinding categoryBinding;
    FragmentSideMenuChild fragmentSideMenuChild;
    private FragmentManager fm;
    AppEventsLogger logger;
    private SharedPreferenceManager mSharedPreferenceManager;
    private FirebaseAnalytics mFirebaseAnalytics;
    LoadingDialog loadingDialog;
    SideMenuCategoryAdapter mSideMenuCategoryAdapter;
 /*   public CategoryFragment() {
        // Required empty public constructor
    }*/
    @Override
    public void onResume() {
        super.onResume();
        Window window = this.getWindow();
        int width = getResources().getDimensionPixelSize(R.dimen.height_dialogFragment_chat_term);
        int height = getResources().getDimensionPixelSize(R.dimen.width_dialogFragment_chat_term);
        window.setLayout(width, height);
        window.setBackgroundDrawable(getResources().getDrawable(R.drawable.bg_dialog_fragment));
        // initDataLogicScan();
    }


    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        categoryBinding = DataBindingUtil.setContentView(this, R.layout.fragment_category);
        this.setFinishOnTouchOutside(true);

        rootView = categoryBinding.getRoot();
        this.mContext = getApplicationContext();
        loadingDialog = new LoadingDialog(this);
        setSideMenuRecyclerView();
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        mFirebaseAnalytics = FirebaseAnalytics.getInstance(getApplicationContext());
        logger = AppEventsLogger.newLogger(CategoryFragment.this);
        categoryDetailsList.clear();
        if(mSharedPreferenceManager.getCategoryList()!=null&&!mSharedPreferenceManager.getCategoryList().isEmpty()) {
            categoryDetailsList.addAll(mSharedPreferenceManager.getCategoryList());
        }
        fragmentSideMenuChild = new FragmentSideMenuChild();
        //fragmentSideMenuChild.setCallback(CategoryFragment.this);
        categoryBinding.txtRS.setOnClickListener(v->{
         finish();

        });
        categoryBinding.ivClose.setOnClickListener(v->{
       finish();
        });
    }




    private void setSideMenuRecyclerView() {
        mSideMenuCategoryAdapter = new SideMenuCategoryAdapter(CategoryFragment.this, categoryDetailsList, this);
        LinearLayoutManager mLayoutManager = new LinearLayoutManager(CategoryFragment.this, LinearLayoutManager.VERTICAL, false);
        categoryBinding.rvSideMenuCategory.setLayoutManager(mLayoutManager);
//        rvSideMenus.addItemDecoration(new DividerItemDecoration(getApplicationContext(), LinearLayoutManager.VERTICAL));
//        rvSideMenus.setItemAnimator(new DefaultItemAnimator());
        categoryBinding.rvSideMenuCategory.setAdapter(mSideMenuCategoryAdapter);
        categoryBinding.rvSideMenuCategory.setNestedScrollingEnabled(false);
    }


    @Override
    public void redirect(String argWhich, String argExtraInfo) {
        switch (argWhich) {
            case "sideMenu":
              /*  Intent sbc = new Intent(MainActivityNew.this, ProductListingPage.class);
                sbc.putExtra("PageTitle", argPageTitile);
                startActivity(sbc);*/
                categoryBinding.rvSideMenuCategory.setVisibility(View.GONE);
                categoryBinding.flSubmenu.setVisibility(View.VISIBLE);
              /*  Animation  moveToLeft = AnimationUtils.loadAnimation(getApplicationContext(),
                        R.anim.exit_to_left);
                mActivityMainBinding.nsvSideMenu.startAnimation(moveToLeft);*/
                loadFragment(new FragmentSideMenuChild(), argExtraInfo);//extra info is child json response
                break;
            case "sbcMain":

                Intent sbc = new Intent(CategoryFragment.this, ProductListingPage.class);
                sbc.putExtra("PageTitle", argExtraInfo.split("#GoGrocery#")[0]); // extra info is page title
                sbc.putExtra("Category_slug", argExtraInfo.split("#GoGrocery#")[1]); // extra info is category_slug
                startActivity(sbc);
                Constants.VARIABLES.FILTER_TYPE = "category";
                Bundle params = new Bundle();
                params.putString(FirebaseAnalytics.Param.ITEM_CATEGORY, argExtraInfo.split("#GoGrocery#")[1]);
                mFirebaseAnalytics.logEvent("visit_category", params);
                params.putString(AppEventsConstants.EVENT_PARAM_PRODUCT_CATEGORY, argExtraInfo.split("#GoGrocery#")[1]);
                logger.logEvent("visit_category", params);


                break;
            case "category_banner":
                Intent promotional_banner = new Intent(CategoryFragment.this, ProductListingPage.class);
                promotional_banner.putExtra("Category_slug", argExtraInfo.split("#GoGrocery#")[0]); // extra info is category_id
                promotional_banner.putExtra("PageTitle", argExtraInfo.split("#GoGrocery#")[1]); // extra info is category_id
                startActivity(promotional_banner);
                Constants.VARIABLES.FILTER_TYPE = "category";
                Bundle params_cat = new Bundle();

                params_cat.putString(FirebaseAnalytics.Param.ITEM_CATEGORY, argExtraInfo.split("#GoGrocery#")[1]);
                mFirebaseAnalytics.logEvent("visit_category", params_cat);
                params_cat.putString(AppEventsConstants.EVENT_PARAM_PRODUCT_CATEGORY, argExtraInfo.split("#GoGrocery#")[1]);
                logger.logEvent("visit_category", params_cat);
                break;
            case "childSideMenu":
                Intent childSideMenu = new Intent(CategoryFragment.this, ProductListingPage.class);
                childSideMenu.putExtra("PageTitle", argExtraInfo.split("#GoGrocery#")[1]); // extra info is page title
                childSideMenu.putExtra("Category_slug", argExtraInfo.split("#GoGrocery#")[0]); // extra info is category_slug
                startActivity(childSideMenu);
                Constants.VARIABLES.FILTER_TYPE = "category";
                Bundle paramsCat = new Bundle();
                paramsCat.putString(FirebaseAnalytics.Param.ITEM_CATEGORY, argExtraInfo.split("#GoGrocery#")[1]);
                mFirebaseAnalytics.logEvent("visit_category", paramsCat);
                paramsCat.putString(AppEventsConstants.EVENT_PARAM_PRODUCT_CATEGORY, argExtraInfo.split("#GoGrocery#")[1]);
                logger.logEvent("visit_category", paramsCat);
                break;
            case "shop_by_brand":
                Intent shop_by_brand = new Intent(CategoryFragment.this, ProductListingPage.class);
                shop_by_brand.putExtra("Category_slug", argExtraInfo.split("#GoGrocery#")[0]); // extra info is category_slug
                shop_by_brand.putExtra("PageTitle", "shop_by_brand#GoGrocery#" + argExtraInfo.split("#GoGrocery#")[1]); // extra info is category_slug
                startActivity(shop_by_brand);
                Constants.VARIABLES.FILTER_TYPE = "brand";
                Bundle params_brand = new Bundle();
                params_brand.putString(FirebaseAnalytics.Param.ITEM_BRAND, argExtraInfo.split("#GoGrocery#")[1]);
                mFirebaseAnalytics.logEvent("view_brand", params_brand);
                params_brand.putString("Item_brand", argExtraInfo.split("#GoGrocery#")[1]);
                logger.logEvent("view_brand", params_brand);

                break;

        }
        }





    public void loadFragment(Fragment fragment, String extraInfo) {

        Bundle bundle = new Bundle();
        bundle.putString("extraInfo", extraInfo);

// create a FragmentManager
        fm = getSupportFragmentManager();//****for v4 use getSupportFragmentManager
// create a FragmentTransaction to begin the transaction and replace the Fragment
        FragmentTransaction fragmentTransaction = fm.beginTransaction();
        fragment.setArguments(bundle);
        fragmentTransaction.setCustomAnimations(R.anim.enter_from_right, R.anim.exit_to_left, R.anim.enter_from_right, R.anim.exit_to_left);

        fragmentTransaction.addToBackStack("childfrag");
// replace the FrameLayout with new Fragment
        fragmentTransaction.replace(R.id.flSubmenu, fragment);


        fragmentTransaction.commit(); // save the changes
    }



    public void backTo(){

        categoryBinding.rvSideMenuCategory.setVisibility(View.VISIBLE);
        categoryBinding.flSubmenu.setVisibility(View.GONE);
      /*  fragmentSideMenuChild = new FragmentSideMenuChild();
        fragmentSideMenuChild.setCallback(CategoryFragment.this);*/

    }

  /*  @Override
    public void onclick() {
        backTo();
    }*/
}
