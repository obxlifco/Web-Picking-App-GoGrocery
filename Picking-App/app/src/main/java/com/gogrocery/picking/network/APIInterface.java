package com.gogrocery.picking.network;

import com.gogrocery.picking.response_pojo.category_list_pojo.CategoryListResponse;
import com.gogrocery.picking.response_pojo.confirm_return_pojo.ConfirmReturnResponse;
import com.gogrocery.picking.response_pojo.dashboard_pojo.DashboardResponse;
import com.gogrocery.picking.response_pojo.forgot_pwd_pojo.ForgotPwdResponse;
import com.gogrocery.picking.response_pojo.general_pojo.GeneralResponse;
import com.gogrocery.picking.response_pojo.generate_picklist_pojo.GeneratePicklistResponse;
import com.gogrocery.picking.response_pojo.grn_update_pojo.GrnUpdateResponse;
import com.gogrocery.picking.response_pojo.latest_order_pojo.LatestOrderResponse;
import com.gogrocery.picking.response_pojo.login_pojo.LoginResponse;
import com.gogrocery.picking.response_pojo.order_detail_csv_pojo.OrderDetailCSVResponse;
import com.gogrocery.picking.response_pojo.order_detail_pojo.OrderDetailResponse;
import com.gogrocery.picking.response_pojo.order_list_pojo.OrderListResponse;
import com.gogrocery.picking.response_pojo.product_list_pojo.ProductListResponse;
import com.gogrocery.picking.response_pojo.search_return_pojo.SearchReturnResponse;
import com.gogrocery.picking.response_pojo.stock_list_pojo.StockListResponse;
import com.gogrocery.picking.response_pojo.update_order_detail_pojo.UpdateOrderDetailResponse;
import com.gogrocery.picking.response_pojo.version_pojo.VersionResponse;

import java.util.Map;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.Header;
import retrofit2.http.Headers;
import retrofit2.http.POST;

public interface APIInterface {
    @POST(Urls.URL_PICKER_LOGIN)
    @Headers({"Content-Type: application/json"})
    Call<LoginResponse> pickerLogin(@Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_FORGOT_PWD)
    @Headers({"Content-Type: application/json"})
    Call<ForgotPwdResponse> pickerForgotPwd(@Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_RESET_PWD)
    @Headers({"Content-Type: application/json"})
    Call<GeneralResponse> pickerResetPwd(@Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_DASHBOARD)
    @Headers({"Content-Type: application/json"})
    Call<DashboardResponse> pickerDashboard(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_ORDERLIST)
    @Headers({"Content-Type: application/json"})
    Call<OrderListResponse> pickerOrderList(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_ORDERDETAILS)
    @Headers({"Content-Type: application/json"})
    Call<OrderDetailResponse> pickerOrderDetails(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_GENERATE_PICKLIST)
    @Headers({"Content-Type: application/json"})
    Call<GeneratePicklistResponse> pickerGeneratePicklist(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_PRODUCTLIST)
    @Headers({"Content-Type: application/json"})
    Call<ProductListResponse> pickerProductList(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_ADDMOREPRODUCT)
    @Headers({"Content-Type: application/json"})
    Call<GeneralResponse> pickerAddMoreProduct(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_SUBSTITUTEPRODUCTLIST)
    @Headers({"Content-Type: application/json"})
    Call<ProductListResponse> pickerSubstituteProductList(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_ADD_SUBSTITUTEPRODUCT)
    @Headers({"Content-Type: application/json"})
    Call<GeneralResponse> pickerAddSubstituteProduct(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_UPDATE_PRODUCT_INFO)
    @Headers({"Content-Type: application/json"})
    Call<GeneralResponse> pickerUpdateProductInfo(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_GRN_COMPLETE)
    @Headers({"Content-Type: application/json"})
    Call<GeneralResponse> pickerGrnComplete(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_GRN_UPDATE)
    @Headers({"Content-Type: application/json"})
    Call<GrnUpdateResponse> pickerGrnUpdate(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_STOCK_CATEGORY)
    @Headers({"Content-Type: application/json"})
    Call<CategoryListResponse> pickerCategoryList(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_STOCK_SEARCH)
    @Headers({"Content-Type: application/json"})
    Call<StockListResponse> pickerStockSearch(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_MANAGE_STOCK)
    @Headers({"Content-Type: application/json"})
    Call<GeneralResponse> pickerManageStock(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_SEARCH_RETURN)
    @Headers({"Content-Type: application/json"})
    Call<SearchReturnResponse> pickerSearchReturn(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_CONFIRM_RETURN)
    @Headers({"Content-Type: application/json"})
    Call<ConfirmReturnResponse> pickerConfirmReturn(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_ADD_SUBSTITUTE)
    @Headers({"Content-Type: application/json"})
    Call<GeneralResponse> pickerAddSubstitute(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_UPDATE_DEVICE_DETAILS)
    @Headers({"Content-Type: application/json"})
    Call<GeneralResponse> pickerUpdateDeviceDetails(@Header("Authorization") String authToken, @Body Map<String, Object> data,
                                                    @Header("DEVICEID") String device_id);

    @POST(Urls.URL_PICKER_SEND_APPROVAL)
    @Headers({"Content-Type: application/json"})
    Call<GeneralResponse> pickerSendApproval(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_RESET_SEND_APPROVAL)
    @Headers({"Content-Type: application/json"})
    Call<GeneralResponse> pickerResetSendApproval(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_LOG_OUT)
    @Headers({"Content-Type: application/json"})
    Call<GeneralResponse> pickerLogout(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_LATEST_ORDER)
    @Headers({"Content-Type: application/json"})
    Call<LatestOrderResponse> pickerLatestOrder(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_UPDATE_ORDER_DETAILS)
    @Headers({"Content-Type: application/json"})
    Call<UpdateOrderDetailResponse> pickerUpdateOrderDetails(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @POST(Urls.URL_PICKER_ORDER_DETAILS_CSV)
    @Headers({"Content-Type: application/json"})
    Call<OrderDetailCSVResponse> pickerOrderDetailsCSV(@Header("Authorization") String authToken, @Body Map<String, Object> data);

    @GET(Urls.URL_PICKER_APP_VERSION)
    @Headers({"Content-Type: application/json"})
    Call<VersionResponse> pickerAppVersion();

    @POST(Urls.URL_PICKER_UPDATE_BILL_NO)
    @Headers({"Content-Type: application/json"})
    Call<GeneralResponse> pickerUpdateBillNumber(@Header("Authorization") String authToken, @Body Map<String, Object> data);
}
