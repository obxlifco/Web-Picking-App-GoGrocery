package com.gogrocery.Networks;


import com.gogrocery.Constants.Constants;
import com.gogrocery.Models.DealsOfTheDay.DealsOfTheDay;
import com.gogrocery.Models.ItemListing.ItemListing;
import com.gogrocery.Models.LoginModel.LoginModel;
import com.gogrocery.Models.ShopByCategory.ShopByCategory;

import java.util.Map;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.FieldMap;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.Headers;
import retrofit2.http.POST;

interface RetrofitAPIService {


    /*
        @FormUrlEncoded
        @POST(Constants.METHOD_NAMES.LOGIN)
        Call<Response<ResponseBody>> login(@Header("Content-Type") String Content_Type,
                                           @Field(Constants.ATRRIBUTE_NAMES.USERNAME) String username,
                                           @Field(Constants.ATRRIBUTE_NAMES.PASSWORD) String password

        );
    */
    @POST(Constants.API_METHODS.deals_of_the_day)
    @FormUrlEncoded
   // @Headers({"Content-Type: application/x-www-form-urlencoded; charset=UTF-8"})
    Call<DealsOfTheDay> deals_of_the_day(@FieldMap Map<String, Object> req);


    @POST(Constants.API_METHODS.best_selling_product)
    @FormUrlEncoded
    Call<DealsOfTheDay> best_selling_product(@FieldMap Map<String, Object> req);

    @POST(Constants.API_METHODS.banner_list)
    @FormUrlEncoded
    Call<ResponseBody> bannerList(@FieldMap Map<String, Object> req);

    @POST(Constants.API_METHODS.product_list)
    @FormUrlEncoded
    Call<ItemListing> itemListing(@FieldMap Map<String, Object> req);

    @POST(Constants.API_METHODS.categories)
    @FormUrlEncoded
    Call<ShopByCategory> shopByCategory(@FieldMap Map<String, Object> req);

    @POST(Constants.API_METHODS.LOGIN)
    @Headers({"Content-Type: application/json"})
    Call<LoginModel> login(@Body Map<String, Object> req);

    @POST(Constants.API_METHODS.SIGN_UP)
    @Headers({"Content-Type: application/json"})
    Call<LoginModel> register(@Body Map<String, Object> req);
    /*@GET(Constants.API_METHODS.LOGIN)
    Call<DetailsPage> productDetails();*/
}
