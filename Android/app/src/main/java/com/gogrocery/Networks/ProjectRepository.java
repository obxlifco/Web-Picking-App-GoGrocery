package com.gogrocery.Networks;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import android.util.Base64;
import android.util.Log;

import com.gogrocery.Constants.Constants;
import com.gogrocery.Models.DealsOfTheDay.DealsOfTheDay;
import com.gogrocery.Models.DetailsPage.DetailsPage;
import com.gogrocery.Models.ItemListing.ItemListing;
import com.gogrocery.Models.LoginModel.LoginModel;
import com.gogrocery.Models.ShopByCategory.ShopByCategory;

import java.io.IOException;
import java.util.HashMap;
import java.util.concurrent.TimeUnit;
import okhttp3.Interceptor;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.ResponseBody;
import okhttp3.logging.HttpLoggingInterceptor;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ProjectRepository {
    private static final String TAG = "ProjectRepository";
    private static ProjectRepository projectRepository;
    private RetrofitAPIService retrofitAPIService;

    private ProjectRepository() {
        HttpLoggingInterceptor logging = new HttpLoggingInterceptor();
// set your desired log level
        logging.setLevel(HttpLoggingInterceptor.Level.BODY);

        OkHttpClient httpClient = new OkHttpClient.Builder()
                .addInterceptor(logging)
                .connectTimeout(30, TimeUnit.SECONDS)
                .readTimeout(30, TimeUnit.SECONDS)
                .writeTimeout(30, TimeUnit.SECONDS)
                .addInterceptor(new Interceptor() {
                    @Override
                    public okhttp3.Response intercept(Chain chain) throws IOException {
                        Request request = chain
                                .request()
                                .newBuilder()
                                .build();
                        return chain.proceed(request);
                    }
                })
                .build();


        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl(Constants.BASE_URL)
                .client(httpClient)
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        retrofitAPIService = retrofit.create(RetrofitAPIService.class);
    }

    public synchronized static ProjectRepository getInstance() {
        //TODO No need to implement this singleton in Part #2 since Dagger will handle it ...
        if (projectRepository == null) {
            if (projectRepository == null) {
                projectRepository = new ProjectRepository();
            }
        }
        return projectRepository;
    }

    public String getAuth() {
        String userName = "";
        String password = "";
        String base = userName + ":" + password;
        return "Basic " + Base64.encodeToString(base.getBytes(), Base64.NO_WRAP);
    }

    public LiveData<DealsOfTheDay> deals_of_the_day(HashMap<String, Object> arRequest) {
        final MutableLiveData<DealsOfTheDay> data = new MutableLiveData<>();



        retrofitAPIService.deals_of_the_day(arRequest)
                .enqueue(new Callback<DealsOfTheDay>() {
                    @Override
                    public void onResponse(Call<DealsOfTheDay> call, Response<DealsOfTheDay> response) {
                        data.setValue(response.body());

                    }

                    @Override
                    public void onFailure(Call<DealsOfTheDay> call, Throwable t) {
                        Log.e(TAG, "onFailure: " + t.toString());
                        Log.e(TAG, "onFailure: " + t.getMessage());
                        data.setValue(null);
                    }
                });

        return data;
    }
    public LiveData<DealsOfTheDay> best_selling_product(HashMap<String, Object> arRequest) {
        final MutableLiveData<DealsOfTheDay> data = new MutableLiveData<>();



        retrofitAPIService.best_selling_product(arRequest)
                .enqueue(new Callback<DealsOfTheDay>() {
                    @Override
                    public void onResponse(Call<DealsOfTheDay> call, Response<DealsOfTheDay> response) {
                        data.setValue(response.body());

                    }

                    @Override
                    public void onFailure(Call<DealsOfTheDay> call, Throwable t) {
                        Log.e(TAG, "onFailure: " + t.toString());
                        Log.e(TAG, "onFailure: " + t.getMessage());
                        data.setValue(null);
                    }
                });

        return data;
    }

    public LiveData<Response<ResponseBody>> bannerList(HashMap<String, Object> arRequest) {
        final MutableLiveData<Response<ResponseBody>> data = new MutableLiveData<>();



        retrofitAPIService.bannerList(arRequest)
                .enqueue(new Callback<ResponseBody>() {

                    @Override
                    public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
                        data.setValue(response);
                    }

                    @Override
                    public void onFailure(Call<ResponseBody> call, Throwable t) {
                        Log.e(TAG, "onFailure: " + t.toString());
                        Log.e(TAG, "onFailure: " + t.getMessage());
                        data.setValue(null);
                    }
                });

        return data;
    }


    public LiveData<LoginModel> register(HashMap<String, Object> arRequest) {
        final MutableLiveData<LoginModel> data = new MutableLiveData<>();



        retrofitAPIService.register(arRequest)
                .enqueue(new Callback<LoginModel>() {

                    @Override
                    public void onResponse(Call<LoginModel> call, Response<LoginModel> response) {
                        data.setValue(response.body());
                    }

                    @Override
                    public void onFailure(Call<LoginModel> call, Throwable t) {
                        Log.e(TAG, "onFailure: " + t.toString());
                        Log.e(TAG, "onFailure: " + t.getMessage());
                        data.setValue(null);
                    }
                });

        return data;
    }

    public LiveData<ItemListing> itemListing(HashMap<String, Object> arRequest) {
        final MutableLiveData<ItemListing> data = new MutableLiveData<>();



        retrofitAPIService.itemListing(arRequest)
                .enqueue(new Callback<ItemListing>() {
                    @Override
                    public void onResponse(Call<ItemListing> call, Response<ItemListing> response) {
                        data.setValue(response.body());

                    }

                    @Override
                    public void onFailure(Call<ItemListing> call, Throwable t) {
                        Log.e(TAG, "onFailure: " + t.toString());
                        Log.e(TAG, "onFailure: " + t.getMessage());
                        data.setValue(null);
                    }
                });

        return data;
    }

    public LiveData<ShopByCategory> shopByCategory(HashMap<String, Object> arRequest) {
        final MutableLiveData<ShopByCategory> data = new MutableLiveData<>();



        retrofitAPIService.shopByCategory(arRequest)
                .enqueue(new Callback<ShopByCategory>() {
                    @Override
                    public void onResponse(Call<ShopByCategory> call, Response<ShopByCategory> response) {
                        data.setValue(response.body());

                    }

                    @Override
                    public void onFailure(Call<ShopByCategory> call, Throwable t) {
                        Log.e(TAG, "onFailure: " + t.toString());
                        Log.e(TAG, "onFailure: " + t.getMessage());
                        data.setValue(null);
                    }
                });

        return data;
    }

    public LiveData<LoginModel> login(HashMap<String, Object> arRequest) {
        final MutableLiveData<LoginModel> data = new MutableLiveData<>();



        retrofitAPIService.login(arRequest)
                .enqueue(new Callback<LoginModel>() {
                    @Override
                    public void onResponse(Call<LoginModel> call, Response<LoginModel> response) {
                        data.setValue(response.body());

                    }

                    @Override
                    public void onFailure(Call<LoginModel> call, Throwable t) {
                        Log.e(TAG, "onFailure: " + t.toString());
                        Log.e(TAG, "onFailure: " + t.getMessage());
                        data.setValue(null);
                    }
                });

        return data;
    }
    public LiveData<DetailsPage> productDetails() {
        final MutableLiveData<DetailsPage> data = new MutableLiveData<>();



      /*  retrofitAPIService.productDetails()
                .enqueue(new Callback<DetailsPage>() {
                    @Override
                    public void onResponse(Call<DetailsPage> call, Response<DetailsPage> response) {
                        data.setValue(response.body());

                    }

                    @Override
                    public void onFailure(Call<DetailsPage> call, Throwable t) {
                        Log.e(TAG, "onFailure: " + t.toString());
                        Log.e(TAG, "onFailure: " + t.getMessage());
                        data.setValue(null);
                    }
                });*/

        return data;
    }


}
