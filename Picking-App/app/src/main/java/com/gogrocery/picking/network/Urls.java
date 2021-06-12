package com.gogrocery.picking.network;


public interface Urls {
    String BASE_URL1 = "http://";//Live
    /*String BASE_URL2 = "15.185.126.44:81";//Staging
    String BASE_URL2 = "gogrocery.ae:81";//Live*/

 //String BASE_URL2 = "15.185.126.44:8062";//Staging
 String BASE_URL2 = "gogrocery.ae:8062";//Live

    String URL_PICKER_LOGIN = "api/picker-login/";
    String URL_PICKER_FORGOT_PWD = "api/picker-forgot-password/";
    String URL_PICKER_RESET_PWD = "api/picker-reset-password/";
    String URL_PICKER_DASHBOARD = "api/picker-dashboard/";
    String URL_PICKER_ORDERLIST = "api/picker-orderlist/";
    String URL_PICKER_ORDERDETAILS = "api/picker-orderdetails/";
    String URL_PICKER_GENERATE_PICKLIST = "api/picker-generatepicklist/";
    String URL_PICKER_PRODUCTLIST = "api/picker-productlist/";
    String URL_PICKER_ADDMOREPRODUCT = "api/picker-addmoreproduct/";
    String URL_PICKER_SUBSTITUTEPRODUCTLIST = "api/picker-substituteproductlist/";
    String URL_PICKER_ADD_SUBSTITUTEPRODUCT = "api/picker-addsubstituteproduct/";
    String URL_PICKER_UPDATE_PRODUCT_INFO = "api/picker-updatepicklistproductinfo/";
    String URL_PICKER_GRN_COMPLETE = "api/picker-grn-complete/";
    String URL_PICKER_GRN_UPDATE = "api/picker-updategrnquantity/";
    String URL_PICKER_STOCK_CATEGORY = "api/picker-stockcategory/";
    String URL_PICKER_STOCK_SEARCH = "api/picker-searchstock/";
    String URL_PICKER_MANAGE_STOCK = "api/picker-managestock/";
    String URL_PICKER_SEARCH_RETURN = "api/picker-searchreturn/";
    String URL_PICKER_CONFIRM_RETURN = "api/picker-confirmreturn/";
    String URL_PICKER_ADD_SUBSTITUTE = "api/picker-add-product-as-substitute/";
    String URL_PICKER_SEND_APPROVAL = "api/picker-sendapproval/";
    String URL_PICKER_RESET_SEND_APPROVAL = "api/picker-resetsendapproval/";
    String URL_PICKER_LOG_OUT = "api/picker-logout/";
    String URL_PICKER_LATEST_ORDER = "api/picker-latestorders/";
    String URL_PICKER_UPDATE_ORDER_DETAILS = "api/picker-updateorderdetails/";
    String URL_PICKER_UPDATE_BILL_NO = "api/picker-updateorderbillnumber/";
    String URL_PICKER_ORDER_DETAILS_CSV = "api/picker-orderdetailscsv/";
    String URL_PICKER_APP_VERSION = "/api/front/v1/get-app-version/?type=picking";
    String URL_PICKER_UPDATE_DEVICE_DETAILS = "/api/front/v1/update-device-details/";

}

