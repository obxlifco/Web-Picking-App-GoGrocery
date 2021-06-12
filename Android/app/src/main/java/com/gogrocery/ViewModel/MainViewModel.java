package com.gogrocery.ViewModel;

import android.app.Application;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;
import androidx.annotation.NonNull;

import com.gogrocery.Models.DealsOfTheDay.DealsOfTheDay;
import com.gogrocery.Models.DetailsPage.DetailsPage;
import com.gogrocery.Models.ItemListing.ItemListing;
import com.gogrocery.Models.LoginModel.LoginModel;
import com.gogrocery.Models.ShopByCategory.ShopByCategory;
import com.gogrocery.Networks.ProjectRepository;

import java.util.HashMap;

import okhttp3.ResponseBody;
import retrofit2.Response;

/**
 * Created by nav on 24/01/18.
 */

public class MainViewModel extends AndroidViewModel {

    private static final String TAG = "LoginViewModel";
    private LiveData<Response<ResponseBody>> mObservable;
    private LiveData<DealsOfTheDay> mDealsOfTheDayLiveData;
    private LiveData<ItemListing> mProductItemListing;
    private LiveData<ShopByCategory> mShopByCategoryLiveData;
    private LiveData<LoginModel> mLoginModelLiveData;

    private LiveData<DetailsPage> mDetailsPageLiveData;
    private ProjectRepository projectRepository;


    public MainViewModel(@NonNull Application application) {
        super(application);
        projectRepository = ProjectRepository.getInstance();

    }


    public LiveData<DealsOfTheDay> deals_of_the_day(HashMap<String, Object> arRequest) {
        mDealsOfTheDayLiveData = projectRepository.deals_of_the_day(arRequest);
        return mDealsOfTheDayLiveData;
    }
    public LiveData<DealsOfTheDay> best_selling_product(HashMap<String, Object> arRequest) {
        mDealsOfTheDayLiveData = projectRepository.best_selling_product(arRequest);
        return mDealsOfTheDayLiveData;
    }

    public LiveData<Response<ResponseBody>> bannerList(HashMap<String, Object> arRequest) {
        mObservable = projectRepository.bannerList(arRequest);
        return mObservable;
    }

    public LiveData<ItemListing> itemListing(HashMap<String, Object> arRequest) {
        mProductItemListing = projectRepository.itemListing(arRequest);
        return mProductItemListing;
    }

    public LiveData<ShopByCategory> shopByCategory(HashMap<String, Object> arRequest) {
        mShopByCategoryLiveData = projectRepository.shopByCategory(arRequest);
        return mShopByCategoryLiveData;
    }

    public LiveData<LoginModel> login(HashMap<String, Object> arRequest) {
        mLoginModelLiveData = projectRepository.login(arRequest);
        return mLoginModelLiveData;
    }
    public LiveData<LoginModel> register(HashMap<String, Object> arRequest) {
        mLoginModelLiveData = projectRepository.register(arRequest);
        return mLoginModelLiveData;
    }



    public LiveData<DetailsPage> productDetails() {
        mDetailsPageLiveData = projectRepository.productDetails();
        return mDetailsPageLiveData;
    }

}
