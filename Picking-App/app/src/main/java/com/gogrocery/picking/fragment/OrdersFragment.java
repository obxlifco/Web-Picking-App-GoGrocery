package com.gogrocery.picking.fragment;

import android.Manifest;
import android.app.Dialog;
import android.app.TimePickerDialog;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.os.Handler;
import android.text.Editable;
import android.text.TextUtils;
import android.text.TextWatcher;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.TimePicker;
import android.widget.Toast;

import com.gogrocery.picking.GoGroceryPicking;
import com.gogrocery.picking.adapter.SelectProductAdapter;
import com.gogrocery.picking.network.Urls;
import com.gogrocery.picking.response_pojo.category_list_pojo.CategoryListItem;
import com.gogrocery.picking.response_pojo.category_list_pojo.CategoryListResponse;
import com.gogrocery.picking.response_pojo.latest_order_pojo.LatestOrderResponse;
import com.gogrocery.picking.response_pojo.order_detail_csv_pojo.OrderDetailCSVResponse;
import com.gogrocery.picking.response_pojo.update_order_detail_pojo.UpdateOrderDetailResponse;
import com.gogrocery.picking.utils.DownloadFileHelper;
import com.gogrocery.picking.utils.MyDialog;
import com.gogrocery.picking.utils.PermissionUtilities;
import com.google.android.material.textfield.TextInputEditText;
import com.google.android.material.textfield.TextInputLayout;
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;
import com.gogrocery.picking.R;
import com.gogrocery.picking.activity.BaseActivity;
import com.gogrocery.picking.activity.MainActivity;
import com.gogrocery.picking.adapter.AddProductListAdapter;
import com.gogrocery.picking.adapter.OrderItemListAdapter;
import com.gogrocery.picking.adapter.OrderListAdapter;
import com.gogrocery.picking.adapter.SubstituteListAdapter;
import com.gogrocery.picking.model.AddItemModel;
import com.gogrocery.picking.network.APIClient;
import com.gogrocery.picking.network.APIInterface;
import com.gogrocery.picking.prefrences.AppPreferences;
import com.gogrocery.picking.response_pojo.general_pojo.GeneralResponse;
import com.gogrocery.picking.response_pojo.generate_picklist_pojo.GeneratePicklistResponse;
import com.gogrocery.picking.response_pojo.grn_update_pojo.GrnUpdateResponse;
import com.gogrocery.picking.response_pojo.order_detail_pojo.OrderDetailResponse;
import com.gogrocery.picking.response_pojo.order_detail_pojo.OrderProductsItem;
import com.gogrocery.picking.response_pojo.order_detail_pojo.OrderSubstituteProductsItem;
import com.gogrocery.picking.response_pojo.order_detail_pojo.ResponseItem;
import com.gogrocery.picking.response_pojo.order_list_pojo.OrderListItem;
import com.gogrocery.picking.response_pojo.order_list_pojo.OrderListResponse;
import com.gogrocery.picking.response_pojo.product_list_pojo.ProductListResponse;
import com.gogrocery.picking.service.OrderUpdateService;
import com.gogrocery.picking.utils.AppUtilities;
import com.gogrocery.picking.utils.SimpleDividerItemDecoration;
import com.karumi.dexter.MultiplePermissionsReport;
import com.karumi.dexter.PermissionToken;
import com.karumi.dexter.listener.PermissionRequest;
import com.karumi.dexter.listener.multi.MultiplePermissionsListener;
import com.toptoche.searchablespinnerlibrary.SearchableSpinner;

import java.text.DecimalFormat;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.HashMap;
import java.util.List;
import java.util.concurrent.TimeUnit;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.widget.NestedScrollView;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class OrdersFragment extends Fragment implements MultiplePermissionsListener {
    RecyclerView rvOrderList, rvItemOrderList, rvSubstituteOrderList, rvAddProductDialog, rvSelectProductDialog;
    TextView tvNoValueOrderList, tvOrdIDOrderDetails, tvStatusOrderDetails, tvDateOrderDetails, tvCustomerNameOrderDetails, tvPayMethodOrderDetails;
    TextView tvAddressOrderDetails, tvViewMapOrderDetails, tvProductPriceOrderDetails, tvServiceChargeOrderDetails, tvTotalPriceOrderDetails, tvUpdatePriceOrderDetails;
    TextView tvCellOrderDetails, tvNoValueProductDialog, tvProcessOrderDetails, tvSendApprovalOrderDetails, tvRequestApprove, tvDiscountOrderDetails;
    TextView tvNoValueOrderDetails, tvNotifyCustomerOrderDetails, tvNoteOrderDetails, tvExpTimeOrderDetails, tvInvoiceOrderDetails, tvShippingDiscountOrderDetails;
    TextView tvBillNoOrderDetails;
    Dialog dialogAdd;
    ProgressBar pg_dia;
    ImageView ivExpTimeOrderDetails;
    LinearLayout llMainOrderDetails, llAddItemOrderDetails, llApproveContainer, llSubstituteContainer, llWaitApproveContainer, llSelectProductDialog, llNoteOrderDetails;
    LinearLayout llExpTimeOrderDetails, llInvoiceOrderDetails, llUpdatePriceOrderDetails, llCSVOrderDetails;
    NestedScrollView nsvMainOrderDetails;
    TextInputEditText etPrepareByOrderDetails;
    int start_index = 1, start_index_product = 1;
    List<OrderListItem> orderListItem = new ArrayList<>();
    List<AddItemModel> addListProduct = new ArrayList<>();
    List<Integer> addProductId = new ArrayList<>();
    List<Long> addProductQty = new ArrayList<>();
    OrderListResponse orderListResponse;
    Boolean isOrderListLoading = false, isProductListLoading = false;
    int detailPosition = -1, subProductId;
    String strSearchProduct = "", strEanSearchProduct = "";
    ResponseItem detailOrd;
    View view;
    boolean isScanForAdd = false, isGeneratePicklist;
    static DecimalFormat formatter = new DecimalFormat("#.00");
    OrderItemListAdapter orderItemListAdapter;
    String pushOrderID = "", order_status = "";
    DecimalFormat formater = new DecimalFormat("0.00");
    UpdateOrderReceiver updateOrderReceiver;
    Handler mHandler = new Handler();
    List<CategoryListItem> categoryList = new ArrayList<>();
    List<CategoryListItem> subCategoryList = new ArrayList<>();
    List<String> categorySpinnerStr = new ArrayList<>();
    List<String> subCategorySpinnerStr = new ArrayList<>();
    List<CategoryListItem> mainCategoryList = new ArrayList<>();
    String selCategoryID = "", selSubCategoryID = "";
    SearchableSpinner spSubCategoryAddProductDialog, spCategoryAddProductDialog;
    private int mHour, mMinute;
    private String[] requestPermission = {Manifest.permission.READ_EXTERNAL_STORAGE, Manifest.permission.WRITE_EXTERNAL_STORAGE};

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        //return super.onCreateView(inflater, container, savedInstanceState);
        view = inflater.inflate(R.layout.fragment_orders, container, false);
        initView(view);
        return view;
    }

    private void initView(View view) {
        rvOrderList = view.findViewById(R.id.rvOrderList);
        rvItemOrderList = view.findViewById(R.id.rvItemOrderList);
        rvSubstituteOrderList = view.findViewById(R.id.rvSubstituteOrderList);
        tvOrdIDOrderDetails = view.findViewById(R.id.tvOrdIDOrderDetails);
        tvStatusOrderDetails = view.findViewById(R.id.tvStatusOrderDetails);
        tvDateOrderDetails = view.findViewById(R.id.tvDateOrderDetails);
        tvCustomerNameOrderDetails = view.findViewById(R.id.tvCustomerNameOrderDetails);
        tvAddressOrderDetails = view.findViewById(R.id.tvAddressOrderDetails);
        tvViewMapOrderDetails = view.findViewById(R.id.tvViewMapOrderDetails);
        tvProductPriceOrderDetails = view.findViewById(R.id.tvProductPriceOrderDetails);
        tvServiceChargeOrderDetails = view.findViewById(R.id.tvServiceChargeOrderDetails);
        tvTotalPriceOrderDetails = view.findViewById(R.id.tvTotalPriceOrderDetails);
        tvUpdatePriceOrderDetails = view.findViewById(R.id.tvUpdatePriceOrderDetails);
        tvPayMethodOrderDetails = view.findViewById(R.id.tvPayMethodOrderDetails);
        tvCellOrderDetails = view.findViewById(R.id.tvCellOrderDetails);
        tvNoteOrderDetails = view.findViewById(R.id.tvNoteOrderDetails);
        nsvMainOrderDetails = view.findViewById(R.id.nsvMainOrderDetails);
        etPrepareByOrderDetails = view.findViewById(R.id.etPrepareByOrderDetails);
        llMainOrderDetails = view.findViewById(R.id.llMainOrderDetails);
        llAddItemOrderDetails = view.findViewById(R.id.llAddItemOrderDetails);
        llCSVOrderDetails = view.findViewById(R.id.llCSVOrderDetails);
        tvNoValueOrderList = view.findViewById(R.id.tvNoValueOrderList);
        llApproveContainer = view.findViewById(R.id.llApproveContainer);
        llSubstituteContainer = view.findViewById(R.id.llSubstituteContainer);
        tvProcessOrderDetails = view.findViewById(R.id.tvProcessOrderDetails);
        tvSendApprovalOrderDetails = view.findViewById(R.id.tvSendApprovalOrderDetails);
        tvNotifyCustomerOrderDetails = view.findViewById(R.id.tvNotifyCustomerOrderDetails);
        tvRequestApprove = view.findViewById(R.id.tvRequestApprove);
        llWaitApproveContainer = view.findViewById(R.id.llWaitApproveContainer);
        tvDiscountOrderDetails = view.findViewById(R.id.tvDiscountOrderDetails);
        tvShippingDiscountOrderDetails = view.findViewById(R.id.tvShippingDiscountOrderDetails);
        tvNoValueOrderDetails = view.findViewById(R.id.tvNoValueOrderDetails);
        llNoteOrderDetails = view.findViewById(R.id.llNoteOrderDetails);
        llExpTimeOrderDetails = view.findViewById(R.id.llExpTimeOrderDetails);
        tvExpTimeOrderDetails = view.findViewById(R.id.tvExpTimeOrderDetails);
        llInvoiceOrderDetails = view.findViewById(R.id.llInvoiceOrderDetails);
        tvInvoiceOrderDetails = view.findViewById(R.id.tvInvoiceOrderDetails);
        llUpdatePriceOrderDetails = view.findViewById(R.id.llUpdatePriceOrderDetails);
        ivExpTimeOrderDetails = view.findViewById(R.id.ivExpTimeOrderDetails);
        tvBillNoOrderDetails = view.findViewById(R.id.tvBillNoOrderDetails);
        pg_dia = view.findViewById(R.id.pg_dia);

        updateOrderReceiver = new UpdateOrderReceiver();
        getActivity().registerReceiver(updateOrderReceiver, new IntentFilter("com.gogrocery.picking.receiver.ORDER_UPDATE"));
        mHandler.postDelayed(new Runnable() {
            @Override
            public void run() {
                try {
                    getActivity().startService(new Intent(getActivity(), OrderUpdateService.class));
                } catch (Exception e) {
                }

            }
        }, 15000);

        Log.e("pushOrdersFragment", "" + getArguments().getString("pushOrderID"));
        pushOrderID = getArguments().getString("pushOrderID");
        order_status = getArguments().getString("order_status");

        rvOrderList.addOnScrollListener(new RecyclerView.OnScrollListener() {
            @Override
            public void onScrolled(@NonNull RecyclerView recyclerView, int dx, int dy) {
                super.onScrolled(recyclerView, dx, dy);
                if (dy > 0 && !isOrderListLoading) {
                    if (rvOrderList.getLayoutManager() != null && ((LinearLayoutManager) rvOrderList.getLayoutManager()).findLastCompletelyVisibleItemPosition() == orderListItem.size() - 1) {
                        //bottom of list!
                        isOrderListLoading = true;
                        onLoadNextPage();
                    }
                }
            }
        });

        tvViewMapOrderDetails.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (detailOrd.getOrderStatus() == 100 || detailOrd.getOrderStatus() == 1 || detailOrd.getOrderStatus() == 2) {
                    if (detailOrd.getLat_val() == null || TextUtils.isEmpty(detailOrd.getLat_val())) {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtLatLongNotAvailable), Toast.LENGTH_SHORT).show();
                    } else {
                        /*String uri = String.format(Locale.ENGLISH, "geo:%f,%f", Float.parseFloat(detailOrd.getLat_val()), Float.parseFloat(detailOrd.getLong_val()));
                        Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(uri));
                        getActivity().startActivity(intent);*/
                        String geoUri = "http://maps.google.com/maps?q=loc:" + detailOrd.getLat_val() + "," + detailOrd.getLong_val() + " (" + detailOrd.getDeliveryStreetAddress() + ")";
                        Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(geoUri));
                        getActivity().startActivity(intent);
                    }
                }
            }
        });
        llAddItemOrderDetails.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (detailOrd.getOrderStatus() == 100) {
                    addListProduct.clear();
                    addProductId.clear();
                    addProductQty.clear();
                    strSearchProduct = "";
                    strEanSearchProduct = "";
                    start_index_product = 1;
                    if (AppUtilities.isOnline(getActivity())) {
                        callProductListAPI(false, false,pg_dia);
                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                    }
                }
            }
        });
        llCSVOrderDetails.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (detailOrd.getOrderStatus() == 100 &&
                        !orderListItem.get(detailPosition).getSubstitute_status().equalsIgnoreCase("pending") &&
                        !orderListItem.get(detailPosition).getSubstitute_status().equalsIgnoreCase("done")) {
                    if (AppUtilities.isOnline(getActivity())) {
                        PermissionUtilities.multiplePermission(getActivity(), requestPermission, OrdersFragment.this);
                        //callUpdateOrderDetailsCSVApi();
                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                    }
                }
            }
        });
        tvProcessOrderDetails.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Boolean isProcess = true;
                for (int i = 0; i < detailOrd.getOrderProducts().size(); i++) {
                    if ((detailOrd.getOrderProducts().get(i).getQuantity() - detailOrd.getOrderProducts().get(i).getReturns()) > (detailOrd.getOrderProducts().get(i).getShortage() +
                            detailOrd.getOrderProducts().get(i).getGrnQuantity())) {
                        isProcess = false;
                        break;
                    }
                }
                if (isProcess) {
                    if (!tvBillNoOrderDetails.getText().toString().equalsIgnoreCase(getActivity().getResources().getString(R.string.txtEnterBillNumber))) {
                        if (AppUtilities.isOnline(getActivity())) {
                            String tmpProductVal = "";
                            if (detailOrd.getOrder_net_amount() != null) {
                                tmpProductVal = AppPreferences.getInstance().getCurrency() + " " + formater.format(Double.parseDouble(detailOrd.getOrder_net_amount()));
                            } else {
                                tmpProductVal = AppPreferences.getInstance().getCurrency() + " " + formater.format(detailOrd.getNetAmount());
                            }
                            MyDialog.showOkCancelPopup("Total Product Value = " + tmpProductVal+"\n"+
                                    "Shipping Charge = "+AppPreferences.getInstance().getCurrency()+" "+formater.format(detailOrd.getShippingCost())+"\n"+"Bill Number = "+tvBillNoOrderDetails.getText().toString()+"\n"+
                                    "Confirm?", "Yes",
                                    "No", getActivity(), new MyDialog.OkCancelPopupCallback() {
                                        @Override
                                        public void onPositiveClick() {
                                            callGRNCompleteApi(detailOrd.getOrderProducts());
                                        }

                                        @Override
                                        public void onNegativeClick() {

                                        }
                                    });

                        } else {
                            Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                        }
                    } else {

                        openBillNoDialog();
                        //Toast.makeText(getActivity(), getResources().getString(R.string.txtEnterBillNumber), Toast.LENGTH_SHORT).show();
                   /*     MyDialog.showOkPopupCallBack("Please, provide a bill number before processing the order.", "Ok", getActivity(), new MyDialog.OkCancelPopupCallback() {
                            @Override
                            public void onPositiveClick() {

                            }

                            @Override
                            public void onNegativeClick() {

                            }
                        });*/
                    }
                } else {
                    Toast.makeText(getActivity(), getResources().getString(R.string.txtPickingNotComplete), Toast.LENGTH_SHORT).show();
                }
            }
        });
        tvSendApprovalOrderDetails.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Boolean isProcess = true;
                for (int i = 0; i < detailOrd.getOrderProducts().size(); i++) {
                    if ((detailOrd.getOrderProducts().get(i).getQuantity() - detailOrd.getOrderProducts().get(i).getReturns()) > (detailOrd.getOrderProducts().get(i).getShortage() +
                            detailOrd.getOrderProducts().get(i).getGrnQuantity())) {
                        isProcess = false;
                        break;
                    }
                }
                if (isProcess) {
                    /*if (tvSendApprovalOrderDetails.getText().toString().equalsIgnoreCase(getActivity().getResources().getString(R.string.txtSendForApproval))) {
                        if (AppUtilities.isOnline(getActivity())) {
                            callSendApprovalApi(detailOrd.getOrderSubstituteProducts());

                        } else {
                            Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                        }
                    } else {
                        if (AppUtilities.isOnline(getActivity())) {
                            callResetSendApprovalApi();

                        } else {
                            Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                        }
                    }*/
                    if (AppUtilities.isOnline(getActivity())) {
                        callSendApprovalApi(detailOrd.getOrderSubstituteProducts());

                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                    }
                } else {
                    Toast.makeText(getActivity(), getResources().getString(R.string.txtPickingNotComplete), Toast.LENGTH_SHORT).show();
                }
            }
        });
        tvNotifyCustomerOrderDetails.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Boolean isProcess = true;
                for (int i = 0; i < detailOrd.getOrderProducts().size(); i++) {
                    if ((detailOrd.getOrderProducts().get(i).getQuantity() - detailOrd.getOrderProducts().get(i).getReturns()) > (detailOrd.getOrderProducts().get(i).getShortage() +
                            detailOrd.getOrderProducts().get(i).getGrnQuantity())) {
                        isProcess = false;
                        break;
                    }
                }
                if (isProcess) {
                    if (AppUtilities.isOnline(getActivity())) {
                        callResetSendApprovalApi();

                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                    }

                } else {
                    Toast.makeText(getActivity(), getResources().getString(R.string.txtPickingNotComplete), Toast.LENGTH_SHORT).show();
                }
            }
        });
        ivExpTimeOrderDetails.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (detailOrd.getOrderStatus() == 100) {
                    // Get Current Time
                    final Calendar c = Calendar.getInstance();
                    mHour = c.get(Calendar.HOUR_OF_DAY);
                    mMinute = c.get(Calendar.MINUTE);
                    // Launch Time Picker Dialog
                    TimePickerDialog timePickerDialog = new TimePickerDialog(getActivity(),android.R.style.Theme_Holo_Light_Dialog,
                            new TimePickerDialog.OnTimeSetListener() {

                                @Override
                                public void onTimeSet(TimePicker view, int hourOfDay,
                                                      int minute) {
                                    if (AppUtilities.isOnline(getActivity())) {
                                        String tmpMin = String.valueOf(minute);
                                        if (minute < 10) {
                                            tmpMin = "0" + minute;
                                        }
                                        try {
                                            tvExpTimeOrderDetails.setText(AppUtilities.getFormattedDate(AppUtilities.getMonthFormatDate(detailOrd.getTimeSlotDate())) + " " + hourOfDay + ":" + tmpMin);
                                        } catch (ParseException e) {
                                            e.printStackTrace();
                                        }
                                        /*mHour=hourOfDay;
                                        mMinute=minute;*/
                                        callUpdateOrderDetailsApi(hourOfDay + ":" + tmpMin, "", "");
                                    } else {
                                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                                    }
                                }
                            }, mHour, mMinute, true);
                    timePickerDialog.show();
                    timePickerDialog.getButton(timePickerDialog.BUTTON_NEGATIVE).setTextColor(Color.parseColor("#696969"));
                    timePickerDialog.getButton(timePickerDialog.BUTTON_POSITIVE).setTextColor(Color.parseColor("#5DA446"));
                }
            }
        });
        tvExpTimeOrderDetails.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (detailOrd.getOrderStatus() == 100) {
                    // Get Current Time
                    final Calendar c = Calendar.getInstance();
                    mHour = c.get(Calendar.HOUR_OF_DAY);
                    mMinute = c.get(Calendar.MINUTE);
                    // Launch Time Picker Dialog
                    TimePickerDialog timePickerDialog = new TimePickerDialog(getActivity(),android.R.style.Theme_Holo_Light_Dialog,
                            new TimePickerDialog.OnTimeSetListener() {

                                @Override
                                public void onTimeSet(TimePicker view, int hourOfDay,
                                                      int minute) {
                                    if (AppUtilities.isOnline(getActivity())) {
                                        String tmpMin = String.valueOf(minute);
                                        if (minute < 10) {
                                            tmpMin = "0" + minute;
                                        }
                                        try {
                                            tvExpTimeOrderDetails.setText(AppUtilities.getFormattedDate(AppUtilities.getMonthFormatDate(detailOrd.getTimeSlotDate())) + " " + hourOfDay + ":" + tmpMin);
                                        } catch (ParseException e) {
                                            e.printStackTrace();
                                        }
                                        /*mHour=hourOfDay;
                                        mMinute=minute;*/
                                        callUpdateOrderDetailsApi(hourOfDay + ":" + tmpMin, "", "");
                                    } else {
                                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                                    }
                                }
                            }, mHour, mMinute, false);
                    timePickerDialog.show();
                    timePickerDialog.getButton(timePickerDialog.BUTTON_NEGATIVE).setTextColor(Color.parseColor("#696969"));
                    timePickerDialog.getButton(timePickerDialog.BUTTON_POSITIVE).setTextColor(Color.parseColor("#5DA446"));
                }

            }
        });
        tvUpdatePriceOrderDetails.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (detailOrd.getOrderStatus() == 100) {
                    Boolean isProcess = true;
                    for (int i = 0; i < detailOrd.getOrderProducts().size(); i++) {
                        if ((detailOrd.getOrderProducts().get(i).getQuantity() - detailOrd.getOrderProducts().get(i).getReturns()) > (detailOrd.getOrderProducts().get(i).getShortage() +
                                detailOrd.getOrderProducts().get(i).getGrnQuantity())) {
                            isProcess = false;
                            break;
                        }
                    }
                    if (isProcess && llApproveContainer.getVisibility() == View.VISIBLE) {
                        if (tvUpdatePriceOrderDetails.getText().toString().equalsIgnoreCase(getActivity().getResources().getString(R.string.txtEnterPrice))) {
                            openUpdatePriceDialog(detailOrd.getNetAmount() + "");
                        } else {
                            String[] str = tvUpdatePriceOrderDetails.getText().toString().split(" ");
                            openUpdatePriceDialog(str[1]);
                        }
                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtPickingNotComplete), Toast.LENGTH_SHORT).show();
                    }
                }

            }
        });

        tvBillNoOrderDetails.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (detailOrd.getOrderStatus() == 100) {
                    openUpdateBillNoDialog();
                }
            }
        });
        initOrderData();
    }

    @Override
    public void onStart() {
        super.onStart();
        //initOrderData();
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        if (countDownTimer != null) {
            countDownTimer.cancel();
        }
        mHandler.removeCallbacksAndMessages(null);
        getActivity().unregisterReceiver(updateOrderReceiver);
        getActivity().stopService(new Intent(getActivity(), OrderUpdateService.class));
    }

    public void initOrderData() {
        start_index = 1;
        orderListItem.clear();
        if (AppUtilities.isOnline(getActivity())) {
            callOrderListApi(false);
        } else {
            Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
        }
    }

    private void onLoadNextPage() {
        start_index += 1;
        if (AppUtilities.isOnline(getActivity())) {
            callOrderListApi(true);
        } else {
            Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
        }
    }

    private void onLoadNextPageProductList() {
        start_index_product += 1;
        if (AppUtilities.isOnline(getActivity())) {
            callProductListAPI(true, false,pg_dia);
        } else {
            Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
        }
    }

    private void onLoadNextPageSubstituteProductList() {
        start_index_product += 1;
        if (AppUtilities.isOnline(getActivity())) {
            callSubstituteProductListAPI(true, false, -1,pg_dia);
        } else {
            Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
        }
    }

    private void callUpdateOrderDetailsApi(String time, String price, String updatePrice) {
        ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("order_id", detailOrd.getId());
        logReq.put("user_id", AppPreferences.getInstance().getUserID());
        if (time.length() > 0) {
            logReq.put("slot_start_time", time);
            logReq.put("slot_end_time", time);
        } else {
            logReq.put("order_amount", price);
            logReq.put("updated_order_amount", updatePrice);
        }


        Call<UpdateOrderDetailResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerUpdateOrderDetails(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<UpdateOrderDetailResponse>() {
            @Override
            public void onResponse(Call<UpdateOrderDetailResponse> call, Response<UpdateOrderDetailResponse> response) {
                ((BaseActivity) getActivity()).hideProgressDialog();
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                        } else {
                            tvTotalPriceOrderDetails.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(response.body().getResponse().getOrderAmount()));
                            orderListItem.get(detailPosition).setGrossAmount(response.body().getResponse().getOrderAmount());
                            rvOrderList.getAdapter().notifyItemChanged(detailPosition);
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<UpdateOrderDetailResponse> call, Throwable t) {

            }
        });
    }

    private void callUpdateOrderDetailsCSVApi() {
        ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("order_id", detailOrd.getId());

        Call<OrderDetailCSVResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerOrderDetailsCSV(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<OrderDetailCSVResponse>() {
            @Override
            public void onResponse(Call<OrderDetailCSVResponse> call, Response<OrderDetailCSVResponse> response) {
                ((BaseActivity) getActivity()).hideProgressDialog();
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                        } else {
                            DownloadFileHelper.downloadFile(getActivity(), Urls.BASE_URL1 + Urls.BASE_URL2 + "/" + response.body().getExportFilePath(),
                                    response.body().getResponse());
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<OrderDetailCSVResponse> call, Throwable t) {

            }
        });
    }

    private void callUpdateBillNumberApi(String billNo) {
        ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("order_id", detailOrd.getId());
        logReq.put("user_id", AppPreferences.getInstance().getUserID());
        logReq.put("order_bill_number", billNo);

        Call<GeneralResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerUpdateBillNumber(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<GeneralResponse>() {
            @Override
            public void onResponse(Call<GeneralResponse> call, Response<GeneralResponse> response) {
                ((BaseActivity) getActivity()).hideProgressDialog();
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                        } else {
                            tvBillNoOrderDetails.setText(billNo);
                            detailOrd.setChannelOrderId(billNo);
                        }
                        Toast.makeText(getActivity(),response.body().getMessage(),Toast.LENGTH_SHORT).show();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<GeneralResponse> call, Throwable t) {

            }
        });
    }

    public void callOrderListApi(final Boolean isLoadMore) {
        //0 = Pending,    100 = Processing
        ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("warehouse_id", AppPreferences.getInstance().getWarehouseID());
        logReq.put("page", start_index);
        logReq.put("per_page", 5);
        logReq.put("order_status", order_status);
        Call<OrderListResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerOrderList(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<OrderListResponse>() {
            @Override
            public void onResponse(Call<OrderListResponse> call, Response<OrderListResponse> response) {
                if (isLoadMore) {
                    ((BaseActivity) getActivity()).hideProgressDialog();
                }
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                            ((BaseActivity) getActivity()).hideProgressDialog();
                            tvNoValueOrderList.setVisibility(View.VISIBLE);
                            rvOrderList.setVisibility(View.GONE);
                            tvNoValueOrderDetails.setVisibility(View.VISIBLE);
                            llMainOrderDetails.setVisibility(View.GONE);
                        } else {
                            int lastPos = orderListItem.size();
                            orderListResponse = response.body();
                            orderListItem.addAll(response.body().getResponse());
                            if (orderListItem.size() > 0) {
                                if (isLoadMore) {
                                    rvOrderList.getAdapter().notifyItemChanged(orderListItem.size());
                                    isOrderListLoading = false;
                                } else {
                                    setupRecycler(isLoadMore);
                                }

                            } else {
                                tvNoValueOrderList.setVisibility(View.VISIBLE);
                                rvOrderList.setVisibility(View.GONE);
                            }
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<OrderListResponse> call, Throwable t) {
                Log.e("callOrderList", "onFailure" + t.getLocalizedMessage());

            }
        });
    }

    private void setupSubstituteRecycler(List<OrderSubstituteProductsItem> orderSubstituteProducts, List<OrderProductsItem> orderProducts) {
        rvSubstituteOrderList.setLayoutManager(new LinearLayoutManager(getActivity()));
        rvSubstituteOrderList.setAdapter(new SubstituteListAdapter(getActivity(), orderSubstituteProducts, orderProducts, new SubstituteListAdapter.SubstituteListClickListener() {
            @Override
            public void substituteListClick(int position) {
            }
        }));
    }

    private void setupItemRecycler(final List<OrderProductsItem> orderProducts, int orderStatus) {
        rvItemOrderList.setLayoutManager(new LinearLayoutManager(getActivity()));
        orderItemListAdapter = new OrderItemListAdapter(getActivity(), orderProducts, orderStatus, new OrderItemListAdapter.OrderListItemClickListener() {
            @Override
            public void orderListItemClick(int position) {
            }

            @Override
            public void openAddSubstitute(int position) {
                if (detailOrd.getOrderStatus() == 100) {
                    subProductId = orderProducts.get(position).getProduct().getId();
                    addListProduct.clear();
                    addProductId.clear();
                    addProductQty.clear();
                    strSearchProduct = "";
                    strEanSearchProduct = "";
                    start_index_product = 1;
                    orderProducts.get(position).setShortage(orderProducts.get(position).getShortage() + 1);
                    //rvItemOrderList.getAdapter().notifyDataSetChanged();
                    if (AppUtilities.isOnline(getActivity())) {
                        callSubstituteProductListAPI(false, false, position,pg_dia);
                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                    }
                }
            }

            @Override
            public void editItemWeightClick(int position) {
                openEditWeightDialog(orderProducts.get(position));
            }

            @Override
            public void editItemPriceClick(int position) {
                openEditPriceDialog(orderProducts.get(position));
            }

            @Override
            public void updateGRNShortage(int position, Boolean isShortage) {
                int shortage = orderProducts.get(position).getShortage();
                int grn = orderProducts.get(position).getGrnQuantity();
                int prodID = orderProducts.get(position).getProduct().getId();
                int ordProdID = orderProducts.get(position).getId();
                if (isShortage) {
                    /*int i = 0;
                    for (; i < detailOrd.getOrderSubstituteProducts().size(); i++) {
                        if (detailOrd.getOrderSubstituteProducts().get(i).getSubstituteProductId() == prodID) {
                            break;
                        }
                    }
                    if (i < detailOrd.getOrderSubstituteProducts().size()) {
                        rvItemOrderList.getAdapter().notifyDataSetChanged();
                        if (AppUtilities.isOnline(getActivity())) {
                            Integer[] arr = new Integer[1];
                            Long[] arrQty = new Long[1];
                            arrQty[0] = Long.valueOf(1);
                            arr[0] = detailOrd.getOrderSubstituteProducts().get(i).getProduct().getId();
                            callAddSubstituteProductApi("decrease", arr, arrQty, prodID);
                        } else {
                            Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                        }
                    } else {
                        rvItemOrderList.getAdapter().notifyDataSetChanged();
                        if (AppUtilities.isOnline(getActivity())) {
                            callUpdateGRNShortageAPI(grn, shortage, prodID, ordProdID, position);
                        } else {
                            Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                        }
                    }*/
                    rvItemOrderList.getAdapter().notifyDataSetChanged();
                    if (AppUtilities.isOnline(getActivity())) {
                        callUpdateGRNShortageAPI(grn, shortage, prodID, ordProdID, position);
                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                    }
                } else {
                    rvItemOrderList.getAdapter().notifyDataSetChanged();
                    if (AppUtilities.isOnline(getActivity())) {
                        callUpdateGRNShortageAPI(grn, shortage, prodID, ordProdID, position);
                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                    }
                }
            }

            @Override
            public void orderListItemProcessCheck(List<OrderProductsItem> orderProducts) {
                boolean isCancel = true;
                for (int i = 0; i < orderProducts.size(); i++) {
                    if (orderProducts.get(i).getGrnQuantity() > 0) {
                        isCancel = false;
                        break;
                    }else{
                        isCancel = true;
                    }
                }
                if (isCancel) {
                    tvProcessOrderDetails.setAlpha(.5f);
                    tvProcessOrderDetails.setClickable(false);
                } else {
                    if (isCardPaymentProcess()) {
                        tvProcessOrderDetails.setAlpha(1f);
                        tvProcessOrderDetails.setClickable(true);
                    } else {
                        tvProcessOrderDetails.setAlpha(.5f);
                        tvProcessOrderDetails.setClickable(false);

                    }
                }

            }
        });
        rvItemOrderList.setAdapter(orderItemListAdapter);
    }

    private boolean isCardPaymentProcess() {
        boolean isProcess = false;
        if (detailOrd.getPaymentMethodName().contains("Online Payment")) {
            if (detailOrd.getOrderProducts().size() > 0) {
                try {
                    String[] strDiff = AppUtilities.calculateDifferenceBWDateTime(
                            AppUtilities.convertUTCToDatePrintFormat(detailOrd.getOrderProducts().get(0).getCreated_time()),
                            (AppUtilities.getCurrentDate() + " " + AppUtilities.getCurrentTime())
                    ).split(",");
                    if (Integer.parseInt(strDiff[0]) == 0 && Integer.parseInt(strDiff[1]) == 0) {
                        if (Integer.parseInt(strDiff[2]) >= 30) {
                            isProcess = true;
                            tvProcessOrderDetails.setText(getActivity().getResources().getString(R.string.txtProcessTheOrder));
                        }else {
                            long t = (30 * 60L) - ((Integer.parseInt(strDiff[2]) * 60L) + Integer.parseInt(strDiff[3]));
                            long timeDiff = TimeUnit.SECONDS.toMillis(t);
                            setupTimerOnline(timeDiff);
                        }
                    } else {
                        isProcess = true;
                    }
                } catch (ParseException e) {
                    e.printStackTrace();
                }
            }
        } else {
            tvProcessOrderDetails.setText(getActivity().getResources().getString(R.string.txtProcessTheOrder));
            isProcess = true;
        }
        return isProcess;

    }

    private void callUpdateGRNShortageAPI(int grn, int shortage, int prodID, int ordProdID, int position) {
        ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("user_id", AppPreferences.getInstance().getUserID());
        logReq.put("order_id", orderListItem.get(detailPosition).getId());
        logReq.put("product_id", prodID);
        logReq.put("order_product_id", ordProdID);
        logReq.put("grn_quantity", grn);
        logReq.put("shortage", shortage);
        //logReq.put("grn_details", jaGrnDetails);

        Call<GrnUpdateResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerGrnUpdate(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<GrnUpdateResponse>() {
            @Override
            public void onResponse(Call<GrnUpdateResponse> call, Response<GrnUpdateResponse> response) {
                ((BaseActivity) getActivity()).hideProgressDialog();
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                        } else {
                            /*detailOrd.getOrderProducts().get(position).setGrnQuantity(response.body().getResponse().getGrnQuantity());
                            detailOrd.getOrderProducts().get(position).setShortage(response.body().getResponse().getShortage());
                            rvItemOrderList.getAdapter().notifyDataSetChanged();*/
                            tvProductPriceOrderDetails.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(response.body().getResponse().getOrderDetails().getNetAmount()));
                            tvTotalPriceOrderDetails.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(response.body().getResponse().getOrderDetails().getGrossAmount()));
                            tvServiceChargeOrderDetails.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(response.body().getResponse().getOrderDetails().getShippingCost()));
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<GrnUpdateResponse> call, Throwable t) {
            }
        });

    }

    private void openAddSubstituteDialog(final boolean isAdd, int position) {
        dialogAdd = new Dialog(getActivity());
        dialogAdd.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialogAdd.setCancelable(false);
        dialogAdd.setContentView(R.layout.dialog_add_product);
        int width = (int) (getResources().getDisplayMetrics().widthPixels * 0.90);
        int height = (int) (getResources().getDisplayMetrics().heightPixels * 0.80);
        dialogAdd.getWindow().setLayout(width, height);
        dialogAdd.show();

        LinearLayout llDialogClose = dialogAdd.findViewById(R.id.llDialogClose);
        LinearLayout llSearchAddProductDialog = dialogAdd.findViewById(R.id.llSearchAddProductDialog);
        llSelectProductDialog = dialogAdd.findViewById(R.id.llSelectProductDialog);
        rvAddProductDialog = dialogAdd.findViewById(R.id.rvAddProductDialog);
        rvSelectProductDialog = dialogAdd.findViewById(R.id.rvSelectProductDialog);
        tvNoValueProductDialog = dialogAdd.findViewById(R.id.tvNoValueProductDialog);
        TextView tvAddProductDialog = dialogAdd.findViewById(R.id.tvAddProductDialog);
        TextView tvHeaderAddProductDialog = dialogAdd.findViewById(R.id.tvHeaderAddProductDialog);
        EditText etSearchAddProductDialog = dialogAdd.findViewById(R.id.etSearchAddProductDialog);
        TextView tvScanAddProductDialog = dialogAdd.findViewById(R.id.tvScanAddProductDialog);
        ProgressBar pg_dialog = dialogAdd.findViewById(R.id.pg_dialog);
        spSubCategoryAddProductDialog = dialogAdd.findViewById(R.id.spSubCategoryAddProductDialog);
        spCategoryAddProductDialog = dialogAdd.findViewById(R.id.spCategoryAddProductDialog);
        isScanForAdd = isAdd;
        if (isAdd) {
            tvHeaderAddProductDialog.setText(getActivity().getResources().getString(R.string.txtAddNewProduct));
        }
        llDialogClose.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                /*if (!isAdd && position >= 0) {
                    int shortage = detailOrd.getOrderProducts().get(position).getShortage();
                    int grn = detailOrd.getOrderProducts().get(position).getGrnQuantity();
                    int prodID = detailOrd.getOrderProducts().get(position).getProduct().getId();
                    int ordProdID = detailOrd.getOrderProducts().get(position).getId();
                    rvItemOrderList.getAdapter().notifyDataSetChanged();
                    if (AppUtilities.isOnline(getActivity())) {
                        callUpdateGRNShortageAPI(grn, shortage, prodID, ordProdID, position);
                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                    }
                }*/
                AppUtilities.hideKeyboard(v);
                dialogAdd.dismiss();
            }
        });
        tvScanAddProductDialog.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                AppUtilities.hideKeyboard(view);
                IntentIntegrator.forSupportFragment(OrdersFragment.this).initiateScan();
            }
        });
        etSearchAddProductDialog.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {

                //new text change data Load
                if(charSequence.toString().length()>2) {
                    strSearchProduct = charSequence.toString();
                    strEanSearchProduct = "";
                    addListProduct.clear();
                    addProductId.clear();
                    start_index_product = 1;
                    if (isAdd) {
                        if (AppUtilities.isOnline(getActivity())) {
                            callProductListAPI(false, true,pg_dialog);
                        } else {
                            Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                        }
                    } else {
                        if (AppUtilities.isOnline(getActivity())) {
                            callSubstituteProductListAPI(false, true, -1,pg_dialog);
                        } else {
                            Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                        }
                    }
                }
            }

            @Override
            public void afterTextChanged(Editable editable) {
            }
        });
        llSearchAddProductDialog.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                AppUtilities.hideKeyboard(view);
                strSearchProduct = etSearchAddProductDialog.getText().toString();
                strEanSearchProduct = "";
                addListProduct.clear();
                //addProductId.clear();
                //addProductQty.clear();
                start_index_product = 1;
                if (isAdd) {
                    if (AppUtilities.isOnline(getActivity())) {
                        callProductListAPI(false, true ,pg_dialog);
                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                    }
                } else {
                    if (AppUtilities.isOnline(getActivity())) {
                        callSubstituteProductListAPI(false, true, -1,pg_dialog);
                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                    }
                }
                /*if (AppUtilities.isOnline(getActivity())) {
                    callProductListAPI(false, true);
                } else {
                    Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                }*/
            }
        });
        tvAddProductDialog.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (addProductId.size() > 0) {
                    if (isAdd) {
                        if (AppUtilities.isOnline(getActivity())) {
                            AppUtilities.hideKeyboard(view);
                            dialogAdd.dismiss();
                            callAddProductApi();
                        } else {
                            Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                        }
                    } else {
                        int shortage = detailOrd.getOrderProducts().get(position).getShortage();
                        int grn = detailOrd.getOrderProducts().get(position).getGrnQuantity();
                        int qty = detailOrd.getOrderProducts().get(position).getQuantity();
                        int ret = detailOrd.getOrderProducts().get(position).getReturns();
                        Integer[] arr = new Integer[addProductId.size()];
                        Long[] arrQty = new Long[addProductId.size()];
                        long totalQty = 0;
                        for (int i = 0; i < addProductId.size(); i++) {
                            arr[i] = addProductId.get(i);
                            arrQty[i] = addProductQty.get(i);
                            totalQty = totalQty + addProductQty.get(i);
                        }
                        //if (totalQty <= (qty - ret) - (grn + shortage)) {
                        if (detailOrd.getOrderProducts().get(0).getMinimum_substitute_limit() <= totalQty && totalQty <= detailOrd.getOrderProducts().get(0).getMaximum_substitute_limit()) {
                            if (AppUtilities.isOnline(getActivity())) {
                                AppUtilities.hideKeyboard(view);
                                dialogAdd.dismiss();
                                callAddSubstituteProductApi("increase", arr, arrQty, subProductId);
                            } else {
                                Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                            }
                        } else {
                            Toast.makeText(getActivity(), getActivity().getResources().getString(R.string.txtSubstituteProductError) + " " + detailOrd.getOrderProducts().get(0).getMinimum_substitute_limit() + " to " +
                                    detailOrd.getOrderProducts().get(0).getMaximum_substitute_limit(), Toast.LENGTH_SHORT).show();
                        }
                    }
                } else {
                    Toast.makeText(getActivity(), getActivity().getResources().getString(R.string.txtSelectProductToAdd), Toast.LENGTH_SHORT).show();
                }
            }
        });
        if (addListProduct.size() > 0) {
            tvNoValueProductDialog.setVisibility(View.GONE);
            rvAddProductDialog.setVisibility(View.VISIBLE);
        } else {
            tvNoValueProductDialog.setVisibility(View.VISIBLE);
            rvAddProductDialog.setVisibility(View.GONE);
        }

        spCategoryAddProductDialog.setTitle("Select Category");
        spSubCategoryAddProductDialog.setTitle("Select Sub Category");
        spCategoryAddProductDialog.setPositiveButton("Close");
        spSubCategoryAddProductDialog.setPositiveButton("Close");

        spCategoryAddProductDialog.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int i, long id) {
                if (i != 0 && categoryList.size() > 0) {
                    selCategoryID = String.valueOf(categoryList.get(i - 1).getId());
                } else {
                    selCategoryID = "";
                    //AppUtilities.showSpinnerAsMandatory(setupBinding.spRegister);
                }
                setupSubCategorySpinner(selCategoryID);
                AppUtilities.hideKeyboard(view);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
            }
        });
        spSubCategoryAddProductDialog.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int i, long id) {
                if (i != 0 && subCategoryList.size() > 0) {
                    selSubCategoryID = String.valueOf(subCategoryList.get(i - 1).getId());
                } else {
                    selSubCategoryID = "";
                    //AppUtilities.showSpinnerAsMandatory(setupBinding.spRegister);
                }
                AppUtilities.hideKeyboard(view);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
            }
        });
        if (AppUtilities.isOnline(getActivity())) {
            callCategoryListApi();
        } else {
            Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
        }
        setupAddProductRecycler(isAdd);
    }

    // Get the results:
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        IntentResult result = IntentIntegrator.parseActivityResult(requestCode, resultCode, data);
        if (result != null) {
            if (result.getContents() == null) {
                Toast.makeText(getActivity(), "Cancelled", Toast.LENGTH_LONG).show();
            } else {
                //Toast.makeText(getActivity(), "Scanned: " + result.getContents(), Toast.LENGTH_LONG).show();
                strSearchProduct = "";
                strEanSearchProduct = result.getContents();
                addListProduct.clear();
                //addProductId.clear();
                //addProductQty.clear();
                start_index_product = 1;
                /*if (isScanForAdd) {
                    if (AppUtilities.isOnline(getActivity())) {
                        callProductListAPI(false, true);
                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                    }
                } else {
                    if (AppUtilities.isOnline(getActivity())) {
                        callSubstituteProductListAPI(false, true, -1);
                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                    }
                }*/
                if (AppUtilities.isOnline(getActivity())) {
                    callProductListAPI(false, true,pg_dia);
                } else {
                    Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                }
            }
        } else {
            super.onActivityResult(requestCode, resultCode, data);
        }
    }

    private void setupSubCategorySpinner(String selCategoryID) {
        subCategorySpinnerStr.clear();
        subCategoryList.clear();
        subCategorySpinnerStr.add(getResources().getString(R.string.txtSubCategory));
        if (selCategoryID.length() > 0) {
            for (int i = 0; i < mainCategoryList.size(); i++) {
                if (mainCategoryList.get(i).getParentId() == Integer.parseInt(selCategoryID)) {
                    subCategorySpinnerStr.add(mainCategoryList.get(i).getName());
                    subCategoryList.add(mainCategoryList.get(i));
                }
            }
        }
        ArrayAdapter aaSubCategory = new ArrayAdapter(getActivity(), R.layout.spinner_layout, subCategorySpinnerStr);
        aaSubCategory.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        //Setting the ArrayAdapter data on the Spinner
        spSubCategoryAddProductDialog.setAdapter(aaSubCategory);
    }

    private void callCategoryListApi() {
        //((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("warehouse_id", AppPreferences.getInstance().getWarehouseID());
        Call<CategoryListResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerCategoryList(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<CategoryListResponse>() {
            @Override
            public void onResponse(Call<CategoryListResponse> call, Response<CategoryListResponse> response) {
                //((BaseActivity) getActivity()).hideProgressDialog();
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                        } else {
                            categoryList.clear();
                            mainCategoryList.clear();
                            mainCategoryList.addAll(response.body().getResponse());
                            for (int i = 0; i < mainCategoryList.size(); i++) {
                                if (mainCategoryList.get(i).getParentId() == 0) {
                                    categoryList.add(mainCategoryList.get(i));
                                }
                            }
                            setupSpinner();
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<CategoryListResponse> call, Throwable t) {
                Log.e("callCategoryListApi", "onFailure" + t.getLocalizedMessage());
            }
        });
    }

    private void setupSpinner() {
        categorySpinnerStr.clear();
        categorySpinnerStr.add(getResources().getString(R.string.txtCategory));
        for (int i = 0; i < categoryList.size(); i++) {
            categorySpinnerStr.add(categoryList.get(i).getName());
        }
        ArrayAdapter aaCategory = new ArrayAdapter(getActivity(), R.layout.spinner_layout, categorySpinnerStr);
        aaCategory.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        //Setting the ArrayAdapter data on the Spinner
        spCategoryAddProductDialog.setAdapter(aaCategory);
    }

    private void callAddProductApi() {
        ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        Integer[] arr = new Integer[addProductId.size()];
        Long[] arrQty = new Long[addProductId.size()];
        for (int i = 0; i < addProductId.size(); i++) {
            arr[i] = addProductId.get(i);
            arrQty[i] = addProductQty.get(i);
        }
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("user_id", AppPreferences.getInstance().getUserID());
        logReq.put("order_id", detailOrd.getId());
        logReq.put("warehouse_id", detailOrd.getAssignWh());
        logReq.put("shipment_id", detailOrd.getShipmentId());
        logReq.put("trent_picklist_id", detailOrd.getTrentPicklistId());
        logReq.put("product_ids", arr);
        logReq.put("action", "increase");
        logReq.put("product_qtys", arrQty);
        Call<GeneralResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerAddMoreProduct(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<GeneralResponse>() {
            @Override
            public void onResponse(Call<GeneralResponse> call, Response<GeneralResponse> response) {
                //((BaseActivity) getActivity()).hideProgressDialog();
                Log.e("response", "forgot : " + response.toString());
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                        } else {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                            callOrderDetailsApi(orderListItem.get(detailPosition).getId(), false);
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<GeneralResponse> call, Throwable t) {
            }
        });
    }

    private void callAddSubstituteProductApi(String action, Integer[] arr, Long[] arrQty, int subProductId) {
        ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("user_id", AppPreferences.getInstance().getUserID());
        logReq.put("order_id", detailOrd.getId());
        logReq.put("warehouse_id", detailOrd.getAssignWh());
        logReq.put("shipment_id", detailOrd.getShipmentId());
        logReq.put("trent_picklist_id", detailOrd.getTrentPicklistId());
        logReq.put("product_id", subProductId);
        logReq.put("sub_product_ids", arr);
        logReq.put("action", action);
        logReq.put("sub_product_qtys", arrQty);
        Call<GeneralResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerAddSubstituteProduct(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<GeneralResponse>() {
            @Override
            public void onResponse(Call<GeneralResponse> call, Response<GeneralResponse> response) {
                //((BaseActivity) getActivity()).hideProgressDialog();
                Log.e("response", "forgot : " + response.toString());
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                        } else {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                            callOrderDetailsApi(orderListItem.get(detailPosition).getId(), false);
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<GeneralResponse> call, Throwable t) {
            }
        });
    }

    private void setupAddProductRecycler(final boolean isAdd) {
        List<AddItemModel> selectProduct = new ArrayList<>();
        rvAddProductDialog.setLayoutManager(new LinearLayoutManager(getActivity()));
        rvAddProductDialog.setAdapter(new AddProductListAdapter(getActivity(), addListProduct, isAdd, new AddProductListAdapter.AddProductListClickListener() {

            @Override
            public void productListAdd(int position) {
                addProductId.add(addListProduct.get(position).getId());
                addProductQty.add(addListProduct.get(position).getQty());
                Log.e("productListAdd", " " + Arrays.toString(addProductId.toArray()) + " " +
                        Arrays.toString(addProductQty.toArray()));
                if (!isAdd) {
                    selectProduct.add(addListProduct.get(position));
                    rvSelectProductDialog.getAdapter().notifyDataSetChanged();
                    if (selectProduct.size() > 0) {
                        llSelectProductDialog.setVisibility(View.VISIBLE);
                    } else {
                        llSelectProductDialog.setVisibility(View.GONE);
                    }
                    ViewGroup.LayoutParams params = rvSelectProductDialog.getLayoutParams();
                    if (selectProduct.size() > 2) {
                        params.height = 200;
                    } else {
                        params.height = ViewGroup.LayoutParams.WRAP_CONTENT;
                    }
                    rvSelectProductDialog.setLayoutParams(params);
                }
            }

            @Override
            public void productListRemove(int position) {
                Object o = addListProduct.get(position).getId();
                int idPos = addProductId.indexOf(o);
                addProductId.remove(o);
                addProductQty.remove(idPos);
                Log.e("productListRemove", " " + Arrays.toString(addProductId.toArray()) + " " +
                        Arrays.toString(addProductQty.toArray()));
                if (!isAdd) {
                    Object obj = addListProduct.get(position);
                    selectProduct.remove(obj);
                    rvSelectProductDialog.getAdapter().notifyDataSetChanged();
                    if (selectProduct.size() > 0) {
                        llSelectProductDialog.setVisibility(View.VISIBLE);
                    } else {
                        llSelectProductDialog.setVisibility(View.GONE);
                    }
                    ViewGroup.LayoutParams params = rvSelectProductDialog.getLayoutParams();
                    if (selectProduct.size() > 2) {
                        params.height = 150;
                    } else {
                        params.height = ViewGroup.LayoutParams.WRAP_CONTENT;
                    }
                    rvSelectProductDialog.setLayoutParams(params);
                }

            }

            @Override
            public void addToSubstitute(int position) {
                if (AppUtilities.isOnline(getActivity())) {
                    callAddToSubstituteApi(subProductId, addListProduct.get(position).getId(), 5);
                } else {
                    Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                }
            }
        }));
        rvAddProductDialog.addItemDecoration(new SimpleDividerItemDecoration(getActivity()));

        rvAddProductDialog.addOnScrollListener(new RecyclerView.OnScrollListener() {
            @Override
            public void onScrolled(@NonNull RecyclerView recyclerView, int dx, int dy) {
                super.onScrolled(recyclerView, dx, dy);
                if (dy > 0 && !isProductListLoading) {
                    if (rvAddProductDialog.getLayoutManager() != null && ((LinearLayoutManager) rvAddProductDialog.getLayoutManager()).findLastCompletelyVisibleItemPosition() == addListProduct.size() - 1) {
                        //bottom of list!
                        isProductListLoading = true;
                        if (isAdd) {
                            onLoadNextPageProductList();
                        } else {
                            onLoadNextPageSubstituteProductList();
                        }
                    }
                }
            }
        });
        rvSelectProductDialog.setLayoutManager(new LinearLayoutManager(getActivity()));
        rvSelectProductDialog.setAdapter(new SelectProductAdapter(getActivity(), selectProduct));
    }

    private void setupRecycler(Boolean isLoadMore) {
        LinearLayoutManager layoutManager = new LinearLayoutManager(getActivity());
        rvOrderList.setLayoutManager(layoutManager);
        rvOrderList.setNestedScrollingEnabled(false);
        rvOrderList.setAdapter(new OrderListAdapter(getActivity(), orderListItem, new OrderListAdapter.OrderListClickListener() {
            @Override
            public void orderListClick(int position) {
                if (AppUtilities.isOnline(getActivity())) {
                    detailPosition = position;
                    rvOrderList.scrollToPosition(position);
                    AppPreferences.getInstance().storeViewOrderID(orderListItem.get(position).getId());
                    callOrderDetailsApi(orderListItem.get(position).getId(), true);
                } else {
                    Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                }
            }
        }));
        isOrderListLoading = false;
        if (!isLoadMore) {
            if (AppUtilities.isOnline(getActivity())) {
                detailPosition = 0;
                AppPreferences.getInstance().storeViewOrderID(orderListItem.get(0).getId());
                AppPreferences.getInstance().storeLatestOrderID(orderListItem.get(0).getId());
                callOrderDetailsApi(orderListItem.get(0).getId(), false);
            } else {
                Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
            }
        }
    }

    private void callOrderDetailsApi(int orderID, Boolean isFromSelection) {
        if (isFromSelection) {
            ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        }
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("warehouse_id", AppPreferences.getInstance().getWarehouseID());
        logReq.put("order_id", orderID);
        Call<OrderDetailResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerOrderDetails(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<OrderDetailResponse>() {
            @Override
            public void onResponse(Call<OrderDetailResponse> call, Response<OrderDetailResponse> response) {
                ((BaseActivity) getActivity()).hideProgressDialog();
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(getActivity(), response.body().getApiStatus(), Toast.LENGTH_SHORT).show();
                        } else {

                            setupOrderDetails(response.body(), isFromSelection);
                            isCardPaymentProcess();
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<OrderDetailResponse> call, Throwable t) {
                Log.e("callOrderDetail", "onFailure" + t.getLocalizedMessage());
            }
        });
    }

    private void setupOrderDetails(OrderDetailResponse detail, Boolean isFromSelection) {
        detailOrd = detail.getResponse().get(0);
        tvOrdIDOrderDetails.setText(detailOrd.getCustomOrderId() + "");
        tvProcessOrderDetails.setAlpha(.5f);
        tvProcessOrderDetails.setClickable(false);
        if(isCardPaymentProcess()){}

        if (detailOrd.getOrderStatus() == 0) {
            tvStatusOrderDetails.setText(getActivity().getResources().getString(R.string.txtPending));
            tvStatusOrderDetails.setTextColor(getActivity().getResources().getColor(R.color.appRed));
            etPrepareByOrderDetails.setEnabled(true);
            etPrepareByOrderDetails.setText("");
            isGeneratePicklist = true;
            llInvoiceOrderDetails.setVisibility(View.GONE);
            llUpdatePriceOrderDetails.setVisibility(View.VISIBLE);
        } else if (detailOrd.getOrderStatus() == 100) {
            if (orderListItem.get(detailPosition).getSubstitute_status().equalsIgnoreCase("pending")) {
                tvStatusOrderDetails.setText(getActivity().getResources().getString(R.string.txtInSubsOut));
                tvStatusOrderDetails.setTextColor(getActivity().getResources().getColor(R.color.appGreen));
            } else if (orderListItem.get(detailPosition).getSubstitute_status().equalsIgnoreCase("done")) {
                tvStatusOrderDetails.setText(getActivity().getResources().getString(R.string.txtSubsIn));
                tvStatusOrderDetails.setTextColor(getActivity().getResources().getColor(R.color.appGreen));
            } else {
                tvStatusOrderDetails.setText(getActivity().getResources().getString(R.string.txtInProcessing));
                tvStatusOrderDetails.setTextColor(getActivity().getResources().getColor(R.color.appGreen));
            }
            etPrepareByOrderDetails.setEnabled(false);
            etPrepareByOrderDetails.setText(detailOrd.getOrderShipment().getCreatedByName());
            isGeneratePicklist = false;
            llInvoiceOrderDetails.setVisibility(View.GONE);
            llUpdatePriceOrderDetails.setVisibility(View.VISIBLE);
        } else if (detailOrd.getOrderStatus() == 1) {
            tvStatusOrderDetails.setText(getActivity().getResources().getString(R.string.txtInShipping));
            tvStatusOrderDetails.setTextColor(getActivity().getResources().getColor(R.color.appGreen));
            etPrepareByOrderDetails.setEnabled(false);
            etPrepareByOrderDetails.setText(detailOrd.getOrderShipment().getCreatedByName());
            isGeneratePicklist = false;
            llInvoiceOrderDetails.setVisibility(View.VISIBLE);
            tvInvoiceOrderDetails.setText(detailOrd.getInvoice_number());
            llUpdatePriceOrderDetails.setVisibility(View.GONE);
        } else if (detailOrd.getOrderStatus() == 2) {
            tvStatusOrderDetails.setText(getActivity().getResources().getString(R.string.txtCancelled));
            tvStatusOrderDetails.setTextColor(getActivity().getResources().getColor(R.color.appPurple));
            etPrepareByOrderDetails.setEnabled(false);
            etPrepareByOrderDetails.setText(detailOrd.getOrderShipment().getCreatedByName());
            isGeneratePicklist = false;
            llInvoiceOrderDetails.setVisibility(View.GONE);
            llUpdatePriceOrderDetails.setVisibility(View.GONE);
        }

        try {
            tvDateOrderDetails.setText(AppUtilities.getFormattedDate(AppUtilities.convertUTCToDateFormat(detailOrd.getCreated())) + " " +
                    AppUtilities.convertUTCToTimeFormat(detailOrd.getCreated()));
        } catch (ParseException e) {
            e.printStackTrace();
        }

        //tvCustomerNameOrderDetails.setText(detailOrd.getCustomer().getFirstName() + " " + detailOrd.getCustomer().getLastName());
        if (detailOrd.getChannelOrderId() != null || !TextUtils.isEmpty(detailOrd.getChannelOrderId())) {
            tvBillNoOrderDetails.setText(detailOrd.getChannelOrderId());
        }else{
            tvBillNoOrderDetails.setText(getActivity().getResources().getString(R.string.txtEnterBillNumber));
        }
        tvCustomerNameOrderDetails.setText(detailOrd.getDeliveryName());
        StringBuilder strAddress = new StringBuilder();
        if (detailOrd.getDeliveryName() != null && detailOrd.getDeliveryName().length() > 0) {
            strAddress.append(detailOrd.getDeliveryName() + ", ");
        }
        if (detailOrd.getDeliveryStreetAddress() != null && detailOrd.getDeliveryStreetAddress().length() > 0) {
            strAddress.append(detailOrd.getDeliveryStreetAddress() + ", ");
        }
        if (detailOrd.getDeliveryLandmark()!= null && detailOrd.getDeliveryLandmark().length() > 0) {
            strAddress.append(detailOrd.getDeliveryLandmark() + ", ");
        }
        if (detailOrd.getDeliveryStreetAddress1() != null && detailOrd.getDeliveryStreetAddress1().length() > 0) {
            strAddress.append(detailOrd.getDeliveryStreetAddress1() + ", ");
        }
        if (detailOrd.getDeliveryCity() != null && detailOrd.getDeliveryCity().length() > 0) {
            strAddress.append(detailOrd.getDeliveryCity() + ", ");
        }
        if (detailOrd.getDeliveryPostcode() != null && detailOrd.getDeliveryPostcode().length() > 0) {
            strAddress.append(detailOrd.getDeliveryPostcode() + ", ");
        }
        if (detailOrd.getDeliveryStateName() != null && detailOrd.getDeliveryStateName().length() > 0) {
            strAddress.append(detailOrd.getDeliveryStateName() + ", ");
        }
        tvAddressOrderDetails.setText(strAddress.toString().substring(0, strAddress.toString().length() - 2));
        //tvCellOrderDetails.setText(detailOrd.getCustomer().getPhone());
        tvCellOrderDetails.setText(detailOrd.getDeliveryPhone());
        if (TextUtils.isEmpty(detailOrd.getCustomMsg())) {
            llNoteOrderDetails.setVisibility(View.GONE);
        } else {
            llNoteOrderDetails.setVisibility(View.VISIBLE);
        }
        tvNoteOrderDetails.setText(detailOrd.getCustomMsg());
        if(detailOrd.getTaxAmount()!=null) {
            tvProductPriceOrderDetails.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(detailOrd.getNetAmount() + detailOrd.getTaxAmount()));
        }else {
            tvProductPriceOrderDetails.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(detailOrd.getNetAmount()));
        }
        tvTotalPriceOrderDetails.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(detailOrd.getGrossAmount()));
        tvServiceChargeOrderDetails.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(detailOrd.getShippingCost()));
        tvDiscountOrderDetails.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(detailOrd.getGrossDiscountAmount()));
        tvShippingDiscountOrderDetails.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(detailOrd.getCartDiscount()));
        if (detailOrd.getOrder_amount() != null) {
            tvUpdatePriceOrderDetails.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(Double.parseDouble(detailOrd.getOrder_net_amount())));
        } else {
            tvUpdatePriceOrderDetails.setText(getActivity().getResources().getString(R.string.txtEnterPrice));
        }
        if(detailOrd.getWarehouseName()!=null&&!detailOrd.getWarehouseName().isEmpty()){
            if(detailOrd.getWarehouseName().equals("")){
                tvUpdatePriceOrderDetails.setClickable(false);
                tvUpdatePriceOrderDetails.setFocusable(false);
                tvUpdatePriceOrderDetails.setFocusableInTouchMode(false);
            }else {
                tvUpdatePriceOrderDetails.setClickable(true);
                tvUpdatePriceOrderDetails.setFocusable(true);
                tvUpdatePriceOrderDetails.setFocusableInTouchMode(true);
            }
        }
        tvPayMethodOrderDetails.setText(detailOrd.getPaymentMethodName());
        try {
            tvExpTimeOrderDetails.setText(AppUtilities.getFormattedDate(AppUtilities.getMonthFormatDate(detailOrd.getTimeSlotDate())) + " " + detailOrd.getSlotEndTime());
        } catch (ParseException e) {
            e.printStackTrace();
        }
        List<OrderProductsItem> tmpProduct = detailOrd.getOrderProducts();
        ////////////////////////////////////////
        if (countDownTimer != null) {
            countDownTimer.cancel();
        }
        boolean isSubsApprove = false;
        boolean isSubsDecline = false;
        if (detailOrd.getOrderSubstituteProducts().size() > 0) {
            for (int i = 0; i < detailOrd.getOrderSubstituteProducts().size(); i++) {
                if (detailOrd.getOrderSubstituteProducts().get(i).getSend_approval() != null) {
                    if (detailOrd.getOrderSubstituteProducts().get(i).getSend_approval().equalsIgnoreCase("approve")) {
                        Gson gson = new Gson();
                        String json = gson.toJson(detailOrd.getOrderSubstituteProducts().get(i));
                        tmpProduct.add(gson.fromJson(json, OrderProductsItem.class));
                    }
                    if (detailOrd.getOrderSubstituteProducts().get(i).getSend_approval().equalsIgnoreCase("approve")) {
                        isSubsApprove = true;
                    }
                    if (detailOrd.getOrderSubstituteProducts().get(i).getSend_approval().equalsIgnoreCase("declined")) {
                        isSubsDecline = true;
                    }
                }
            }
            setupItemRecycler(tmpProduct, detailOrd.getOrderStatus());
        } else {
            setupItemRecycler(tmpProduct, detailOrd.getOrderStatus());
        }
        //////////////////////////////////////////
        //setupItemRecycler(detailOrd.getOrderProducts(), detailOrd.getOrderStatus());
        if (detailOrd.getOrderSubstituteProducts().size() > 0) {
            if (detailOrd.getOrderSubstituteProducts().get(0).getSend_approval() == null) {
                setupSubstituteRecycler(detailOrd.getOrderSubstituteProducts(), detailOrd.getOrderProducts());
                llSubstituteContainer.setVisibility(View.VISIBLE);
                tvNotifyCustomerOrderDetails.setVisibility(View.GONE);
                tvSendApprovalOrderDetails.setText(getActivity().getResources().getString(R.string.txtSendForApproval));
                tvSendApprovalOrderDetails.setAlpha(1f);
                tvSendApprovalOrderDetails.setClickable(true);
                llApproveContainer.setVisibility(View.GONE);
                tvRequestApprove.setVisibility(View.GONE);
                llWaitApproveContainer.setVisibility(View.GONE);
            } else if (isSubsApprove || isSubsDecline) {
                llApproveContainer.setVisibility(View.VISIBLE);
                if (isSubsApprove) {
                    tvRequestApprove.setVisibility(View.VISIBLE);
                } else {
                    tvRequestApprove.setVisibility(View.GONE);
                }
                llSubstituteContainer.setVisibility(View.GONE);
                llWaitApproveContainer.setVisibility(View.GONE);
            } else {
                setupSubstituteRecycler(detailOrd.getOrderSubstituteProducts(), detailOrd.getOrderProducts());
                llApproveContainer.setVisibility(View.GONE);
                tvRequestApprove.setVisibility(View.GONE);
                llSubstituteContainer.setVisibility(View.VISIBLE);
                tvSendApprovalOrderDetails.setAlpha(.5f);
                tvSendApprovalOrderDetails.setClickable(false);
                llWaitApproveContainer.setVisibility(View.VISIBLE);

                try {
                    String[] strDiff = AppUtilities.calculateDifferenceBWDateTime(
                            AppUtilities.convertUTCToDatePrintFormat(detailOrd.getOrderSubstituteProducts().get(0).getCreated_time()),
                            (AppUtilities.getCurrentDate() + " " + AppUtilities.getCurrentTime())
                    ).split(",");
                    if (Integer.parseInt(strDiff[0]) == 0 && Integer.parseInt(strDiff[1]) == 0) {
                        if (Integer.parseInt(strDiff[2]) > detailOrd.getSubstitute_approval_time()) {
                            //tvSendApprovalOrderDetails.setText(getActivity().getResources().getString(R.string.txtNotifyCustomer));
                            tvSendApprovalOrderDetails.setText(getActivity().getResources().getString(R.string.txtSendForApproval));
                            tvNotifyCustomerOrderDetails.setVisibility(View.VISIBLE);
                            tvSendApprovalOrderDetails.setAlpha(1f);
                            tvSendApprovalOrderDetails.setClickable(true);
                        } else {
                            tvNotifyCustomerOrderDetails.setVisibility(View.GONE);
                            tvSendApprovalOrderDetails.setText(getActivity().getResources().getString(R.string.txtSendForApproval));
                            long t = (detailOrd.getSubstitute_approval_time() * 60L) - ((Integer.parseInt(strDiff[2]) * 60L) + Integer.parseInt(strDiff[3]));
                            long timeDiff = TimeUnit.SECONDS.toMillis(t);
                            setupTimer(timeDiff);
                        }
                    } else {
                        //tvSendApprovalOrderDetails.setText(getActivity().getResources().getString(R.string.txtNotifyCustomer));
                        tvSendApprovalOrderDetails.setText(getActivity().getResources().getString(R.string.txtSendForApproval));
                        tvNotifyCustomerOrderDetails.setVisibility(View.VISIBLE);
                        tvSendApprovalOrderDetails.setAlpha(1f);
                        tvSendApprovalOrderDetails.setClickable(true);
                    }
                } catch (ParseException e) {
                    e.printStackTrace();
                }
            }

        } else {
            llApproveContainer.setVisibility(View.VISIBLE);
            llSubstituteContainer.setVisibility(View.GONE);
            tvRequestApprove.setVisibility(View.GONE);
        }

        if (detailOrd.getOrderStatus() == 1 || detailOrd.getOrderStatus() == 2) {
            llApproveContainer.setVisibility(View.GONE);
            llSubstituteContainer.setVisibility(View.GONE);
        }
        if (isFromSelection) {
            nsvMainOrderDetails.scrollTo(0, 0);
        }


        etPrepareByOrderDetails.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View view, boolean hasFocus) {
                if (!hasFocus) {
                    if (AppUtilities.isOnline(getActivity())) {
                        if (isGeneratePicklist) {
                            if (etPrepareByOrderDetails.getText().toString().trim().length() > 0) {
                                isGeneratePicklist = false;
                                callGeneratePicklistAPI(detailOrd.getId(), etPrepareByOrderDetails.getText().toString().trim());
                            } else {
                                Toast.makeText(getActivity(), getResources().getString(R.string.txtEnterPreparedByName), Toast.LENGTH_SHORT).show();
                            }
                        }
                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                    }
                }
            }
        });

        llMainOrderDetails.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (etPrepareByOrderDetails.hasFocus()) {
                    etPrepareByOrderDetails.clearFocus();
                    if (AppUtilities.isOnline(getActivity())) {
                        if (isGeneratePicklist) {
                            if (etPrepareByOrderDetails.getText().toString().trim().length() > 0) {
                                isGeneratePicklist = false;
                                callGeneratePicklistAPI(detailOrd.getId(), etPrepareByOrderDetails.getText().toString().trim());
                            } else {
                                Toast.makeText(getActivity(), getResources().getString(R.string.txtEnterPreparedByName), Toast.LENGTH_SHORT).show();
                            }
                        }
                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                    }
                }
            }
        });
    }

    CountDownTimer countDownTimer = null;

    private void setupTimer(long timeDiff) {
        Log.e("remaining_time",String.valueOf(timeDiff));
        countDownTimer = new CountDownTimer(timeDiff, 1000) {
            public void onTick(long millisUntilFinished) {
                try {
                    tvSendApprovalOrderDetails.setText(getActivity().getResources().getString(R.string.txtSendForApproval) +
                            "(" + String.format("%d min, %d sec",
                            TimeUnit.MILLISECONDS.toMinutes(millisUntilFinished),
                            TimeUnit.MILLISECONDS.toSeconds(millisUntilFinished) -
                                    TimeUnit.MINUTES.toSeconds(TimeUnit.MILLISECONDS.toMinutes(millisUntilFinished))) + ")");
                    tvSendApprovalOrderDetails.setAlpha(.5f);
                    tvSendApprovalOrderDetails.setClickable(false);
                    tvNotifyCustomerOrderDetails.setVisibility(View.GONE);
                } catch (Exception e) {
                }
            }

            public void onFinish() {
                tvSendApprovalOrderDetails.setText(getActivity().getResources().getString(R.string.txtSendForApproval));
                tvNotifyCustomerOrderDetails.setVisibility(View.VISIBLE);
                tvSendApprovalOrderDetails.setAlpha(1f);
                tvSendApprovalOrderDetails.setClickable(true);
            }

        }.start();
    }

    private void setupTimerOnline(long timeDiff) {
        Log.e("remaining_time",String.valueOf(timeDiff));
        countDownTimer = new CountDownTimer(timeDiff, 1000) {
            public void onTick(long millisUntilFinished) {
                try {
                    tvProcessOrderDetails.setText(getActivity().getResources().getString(R.string.txtProcessTheOrder) +
                            "(" + String.format("%d min, %d sec",
                            TimeUnit.MILLISECONDS.toMinutes(millisUntilFinished),
                            TimeUnit.MILLISECONDS.toSeconds(millisUntilFinished) -
                                    TimeUnit.MINUTES.toSeconds(TimeUnit.MILLISECONDS.toMinutes(millisUntilFinished))) + ")");
                    tvSendApprovalOrderDetails.setAlpha(.5f);
                    tvSendApprovalOrderDetails.setClickable(false);
                    tvNotifyCustomerOrderDetails.setVisibility(View.GONE);
                } catch (Exception e) {
                }
            }

            public void onFinish() {
                tvSendApprovalOrderDetails.setText(getActivity().getResources().getString(R.string.txtSendForApproval));
                tvNotifyCustomerOrderDetails.setVisibility(View.VISIBLE);
                tvSendApprovalOrderDetails.setAlpha(1f);
                tvSendApprovalOrderDetails.setClickable(true);
            }

        }.start();
    }
    private void openEditWeightDialog(final OrderProductsItem orderProductsItem) {
        final Dialog dialogEdit = new Dialog(getActivity());
        dialogEdit.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialogEdit.setCancelable(false);
        dialogEdit.setContentView(R.layout.dialog_edit_weight);
        int width = (int) (getResources().getDisplayMetrics().widthPixels * 0.90);
        int height = (int) (getResources().getDisplayMetrics().heightPixels * 0.65);
        dialogEdit.getWindow().setLayout(width, height);
        dialogEdit.show();

        LinearLayout llDialogClose = dialogEdit.findViewById(R.id.llDialogClose);
        TextView tvSKUEditWeight = dialogEdit.findViewById(R.id.tvSKUEditWeight);
        TextView tvNameEditWeight = dialogEdit.findViewById(R.id.tvNameEditWeight);
        TextView tvPriceEditWeight = dialogEdit.findViewById(R.id.tvPriceEditWeight);
        TextView tvApplyEditWeight = dialogEdit.findViewById(R.id.tvApplyEditWeight);
        TextView tvWeightEditWeight = dialogEdit.findViewById(R.id.tvWeightEditWeight);
        final TextInputEditText etWeightEditWeight = dialogEdit.findViewById(R.id.etWeightEditWeight);
        final TextInputEditText etNewPriceEditWeight = dialogEdit.findViewById(R.id.etNewPriceEditWeight);
        final TextInputEditText etNotesEditWeight = dialogEdit.findViewById(R.id.etNotesEditWeight);
        tvSKUEditWeight.setText(orderProductsItem.getProduct().getSku());
        tvNameEditWeight.setText(orderProductsItem.getProduct().getName());
        tvPriceEditWeight.setText(AppPreferences.getInstance().getCurrency() + " " + (orderProductsItem.getProductPrice() * (orderProductsItem.getQuantity() - orderProductsItem.getReturns())));
        tvWeightEditWeight.setText(orderProductsItem.getWeight() * (orderProductsItem.getQuantity() - orderProductsItem.getReturns()) + " " +
                orderProductsItem.getProduct().getUom().getUomName());
        llDialogClose.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                AppUtilities.hideKeyboard(v);
                dialogEdit.dismiss();
            }
        });
        etWeightEditWeight.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                try {
                    if (s.toString().length() > 0) {
                        double parseDouble = orderProductsItem.getProductPrice() * (orderProductsItem.getQuantity() - orderProductsItem.getReturns());
                        //double parseInt = (double) Integer.parseInt(s.toString());
                        double parseInt = (Double.parseDouble(s.toString()));
                        Double.isNaN(parseInt);
                       // Double finalSellingPrice = Double.valueOf((parseDouble * parseInt) / Double.valueOf(orderProductsItem.getWeight().intValue() * (orderProductsItem.getQuantity() - orderProductsItem.getReturns())));
                        Double finalSellingPrice = Double.valueOf((parseDouble * parseInt) / Double.valueOf(orderProductsItem.getWeight() * (orderProductsItem.getQuantity() - orderProductsItem.getReturns())));
                        StringBuilder sb = new StringBuilder();
                        sb.append(String.format("%.2f", new Object[]{finalSellingPrice}));
                        sb.append("");
                        etNewPriceEditWeight.setText(String.valueOf(sb.toString()));
                    } else {
                        etNewPriceEditWeight.setText("0.00");
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });

        tvApplyEditWeight.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (AppUtilities.isOnline(getActivity())) {
                    AppUtilities.hideKeyboard(view);
                    dialogEdit.dismiss();
                    callUpdateProductIfoApi(orderProductsItem, Double.parseDouble(etNewPriceEditWeight.getText().toString()) / orderProductsItem.getQuantity(),
                            etNotesEditWeight.getText().toString(), String.valueOf(Double.parseDouble(String.valueOf(etWeightEditWeight.getText())) / orderProductsItem.getQuantity()), orderProductsItem.getIsSubstitute());
                } else {
                    Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    private void callUpdateProductIfoApi(OrderProductsItem orderProductsItem, Double newPrice, String notes, String newWeight, String isSubstitute) {
        ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("user_id", AppPreferences.getInstance().getUserID());
        logReq.put("order_id", orderListItem.get(detailPosition).getId());
        logReq.put("user_name", AppPreferences.getInstance().getUserName());
        logReq.put("product_id", orderProductsItem.getProduct().getId());
        logReq.put("sku", orderProductsItem.getProduct().getSku());
        logReq.put("order_product_id", orderProductsItem.getId());
        logReq.put("product_old_price", orderProductsItem.getProductPrice());
        logReq.put("product_new_price", formatter.format(newPrice));
        logReq.put("weight", newWeight);
        logReq.put("notes", notes);
        logReq.put("pick_as_substitute", isSubstitute);

        Call<GeneralResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerUpdateProductInfo(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<GeneralResponse>() {
            @Override
            public void onResponse(Call<GeneralResponse> call, Response<GeneralResponse> response) {
                ((BaseActivity) getActivity()).hideProgressDialog();
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                        } else {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                            callOrderDetailsApi(orderListItem.get(detailPosition).getId(), false);
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<GeneralResponse> call, Throwable t) {

            }
        });
    }

    private void callGeneratePicklistAPI(int id, String name) {
        ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("user_id", AppPreferences.getInstance().getUserID());
        logReq.put("picker_name", name);
        logReq.put("order_id", id);
        logReq.put("shipment_id", detailOrd.getShipmentId());
        logReq.put("order_status", detailOrd.getOrderStatus());
        Call<GeneratePicklistResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerGeneratePicklist(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<GeneratePicklistResponse>() {
            @Override
            public void onResponse(Call<GeneratePicklistResponse> call, Response<GeneratePicklistResponse> response) {
                //((BaseActivity) getActivity()).hideProgressDialog();
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            isGeneratePicklist = true;
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                            ((BaseActivity) getActivity()).hideProgressDialog();
                        } else {
                            orderListItem.get(detailPosition).setOrderStatus(100);
                            orderListItem.get(detailPosition).getOrderShipment().setCreatedByName(name);
                            rvOrderList.getAdapter().notifyItemChanged(detailPosition);
                            /*detailOrd.setOrderStatus(100);
                            tvStatusOrderDetails.setText(getActivity().getResources().getString(R.string.txtProcessing));
                            tvStatusOrderDetails.setTextColor(getActivity().getResources().getColor(R.color.appGreen));
                            etPrepareByOrderDetails.setEnabled(false);
                            orderItemListAdapter.setOrderStatus(100);
                            orderItemListAdapter.notifyDataSetChanged();*/
                            callOrderDetailsApi(id, false);
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<GeneratePicklistResponse> call, Throwable t) {

            }
        });
    }

    private void callProductListAPI(final Boolean isLoadMore, final Boolean isSearch,ProgressBar dialog) {
        dialog.setVisibility(View.VISIBLE);
        //((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("user_id", AppPreferences.getInstance().getUserID());
        logReq.put("warehouse_id", AppPreferences.getInstance().getWarehouseID());
        logReq.put("order_id", orderListItem.get(detailPosition).getId());
        logReq.put("page", start_index_product);
        logReq.put("per_page", 10);
        logReq.put("search", strSearchProduct);
        logReq.put("ean", strEanSearchProduct);
        if (selSubCategoryID.length() > 0) {
            logReq.put("category_id", selSubCategoryID);
        } else {
            logReq.put("category_id", selCategoryID);
        }
        Call<ProductListResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerProductList(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<ProductListResponse>() {
            @Override
            public void onResponse(Call<ProductListResponse> call, Response<ProductListResponse> response) {
                dialog.setVisibility(View.GONE);
               // ((BaseActivity) getActivity()).hideProgressDialog();
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                            if (isSearch) {
                                tvNoValueProductDialog.setVisibility(View.VISIBLE);
                                rvAddProductDialog.setVisibility(View.GONE);
                            }
                        } else {
                            for (int i = 0; i < response.body().getResponse().size(); i++) {
                                addListProduct.add(new AddItemModel(response.body().getResponse().get(i).getId(),
                                        response.body().getResponse().get(i).getName(), response.body().getResponse().get(i).getChannelCurrencyProductPrice().getPrice(),
                                        response.body().getResponse().get(i).getProductStock().getRealStock(), response.body().getResponse().get(i).getWeight() + response.body().getResponse().get(i).getUomName(),
                                        response.body().getResponse().get(i).getProductImages().get(0).getLink() +
                                                response.body().getResponse().get(i).getProductImages().get(0).getImg(), false,
                                        response.body().getResponse().get(i).getSubstitute_status(), response.body().getResponse().get(i).getSubstitute_message(), 1));
                            }
                            if (addListProduct.size() > 0) {
                                if (isSearch) {
                                    tvNoValueProductDialog.setVisibility(View.GONE);
                                    rvAddProductDialog.setVisibility(View.VISIBLE);
                                    rvAddProductDialog.getAdapter().notifyDataSetChanged();
                                    isProductListLoading = false;
                                } else {
                                    if (isLoadMore) {
                                        rvAddProductDialog.getAdapter().notifyItemChanged(addListProduct.size());
                                        isProductListLoading = false;
                                    } else {
                                        openAddSubstituteDialog(true, -1);
                                    }
                                }

                            } else {
                                if (isSearch) {
                                    tvNoValueProductDialog.setVisibility(View.VISIBLE);
                                    rvAddProductDialog.setVisibility(View.GONE);
                                }
                            }
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<ProductListResponse> call, Throwable t) {
                Log.e("error", "ProductList" + t.getLocalizedMessage());
            }
        });
    }

    private void callSubstituteProductListAPI(final Boolean isLoadMore, final Boolean isSearch, int position ,ProgressBar diaLog) {
        diaLog.setVisibility(View.VISIBLE);
       // ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("user_id", AppPreferences.getInstance().getUserID());
        logReq.put("warehouse_id", AppPreferences.getInstance().getWarehouseID());
        logReq.put("order_id", orderListItem.get(detailPosition).getId());
        logReq.put("page", start_index_product);
        logReq.put("per_page", 10);
        logReq.put("search", strSearchProduct);
        logReq.put("ean", strEanSearchProduct);
        logReq.put("product_id", subProductId);
        if (selSubCategoryID.length() > 0) {
            logReq.put("category_id", selSubCategoryID);
        } else {
            logReq.put("category_id", selCategoryID);
        }
        Call<ProductListResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerSubstituteProductList(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<ProductListResponse>() {
            @Override
            public void onResponse(Call<ProductListResponse> call, Response<ProductListResponse> response) {
                diaLog.setVisibility(View.GONE);
              //  ((BaseActivity) getActivity()).hideProgressDialog();
                if (position >= 0) {
                    int shortage = detailOrd.getOrderProducts().get(position).getShortage();
                    int grn = detailOrd.getOrderProducts().get(position).getGrnQuantity();
                    int prodID = detailOrd.getOrderProducts().get(position).getProduct().getId();
                    int ordProdID = detailOrd.getOrderProducts().get(position).getId();
                    rvItemOrderList.getAdapter().notifyDataSetChanged();
                    if (AppUtilities.isOnline(getActivity())) {
                        callUpdateGRNShortageAPI(grn, shortage, prodID, ordProdID, position);
                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                    }
                }
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                            if (isSearch) {
                                tvNoValueProductDialog.setVisibility(View.VISIBLE);
                                rvAddProductDialog.setVisibility(View.GONE);
                            } else {
                                /*if (position >= 0) {
                                    int shortage = detailOrd.getOrderProducts().get(position).getShortage();
                                    int grn = detailOrd.getOrderProducts().get(position).getGrnQuantity();
                                    int prodID = detailOrd.getOrderProducts().get(position).getProduct().getId();
                                    int ordProdID = detailOrd.getOrderProducts().get(position).getId();
                                    rvItemOrderList.getAdapter().notifyDataSetChanged();
                                    if (AppUtilities.isOnline(getActivity())) {
                                        callUpdateGRNShortageAPI(grn, shortage, prodID, ordProdID, position);
                                    } else {
                                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                                    }
                                    openAddSubstituteDialog(false, position);
                                }*/
                                if (position >= 0) {
                                    openAddSubstituteDialog(false, position);
                                }
                            }
                        } else {
                            for (int i = 0; i < response.body().getResponse().size(); i++) {
                                if(response.body().getResponse().get(i).getProductImages().size()>0) {
                                    addListProduct.add(new AddItemModel(response.body().getResponse().get(i).getId(),
                                            response.body().getResponse().get(i).getName(), response.body().getResponse().get(i).getChannelCurrencyProductPrice().getPrice(),
                                            response.body().getResponse().get(i).getProductStock().getRealStock(), response.body().getResponse().get(i).getWeight() + response.body().getResponse().get(i).getUomName()
                                            , response.body().getResponse().get(i).getProductImages().get(0).getLink() +
                                            response.body().getResponse().get(i).getProductImages().get(0).getImg(), false,
                                            response.body().getResponse().get(i).getSubstitute_status(), response.body().getResponse().get(i).getSubstitute_message(), 1));
                                }else {
                                    addListProduct.add(new AddItemModel(response.body().getResponse().get(i).getId(),
                                            response.body().getResponse().get(i).getName(), response.body().getResponse().get(i).getChannelCurrencyProductPrice().getPrice(),
                                            response.body().getResponse().get(i).getProductStock().getRealStock(), response.body().getResponse().get(i).getWeight() + response.body().getResponse().get(i).getUomName()
                                            , "https://ifmsa.org/wp-content/themes/ifmsa/assets/images/default.jpg", false,
                                            response.body().getResponse().get(i).getSubstitute_status(), response.body().getResponse().get(i).getSubstitute_message(), 1));
                                }
                            }

                            if (addListProduct.size() > 0) {
                                if (isSearch) {
                                    tvNoValueProductDialog.setVisibility(View.GONE);
                                    rvAddProductDialog.setVisibility(View.VISIBLE);
                                    rvAddProductDialog.getAdapter().notifyDataSetChanged();
                                    isProductListLoading = false;
                                } else {
                                    if (isLoadMore) {
                                        rvAddProductDialog.getAdapter().notifyItemChanged(addListProduct.size());
                                        isProductListLoading = false;
                                    } else {
                                        openAddSubstituteDialog(false, position);
                                    }
                                }

                            } else {
                                if (isSearch) {
                                    tvNoValueProductDialog.setVisibility(View.VISIBLE);
                                    rvAddProductDialog.setVisibility(View.GONE);
                                }
                            }
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<ProductListResponse> call, Throwable t) {
                Log.e("error", "ProductList" + t.getLocalizedMessage());
            }
        });
    }

    private void callGRNCompleteApi(List<OrderProductsItem> orderProducts) {
        /*JSONArray jaGrnDetails=new JSONArray();
        for(int i=0;i<orderProducts.size();i++){
            JSONObject jo=new JSONObject();
            try {
                jo.put("product_id",orderProducts.get(i).getProduct().getId());
                jo.put("grn_quantity",orderProducts.get(i).getGrnQuantity());
                jo.put("shortage",orderProducts.get(i).getShortage());
                jaGrnDetails.put(jo);
            } catch (JSONException e) {
                e.printStackTrace();
            }

        }*/
        ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("user_id", AppPreferences.getInstance().getUserID());
        logReq.put("order_id", orderListItem.get(detailPosition).getId());
        logReq.put("user_name", AppPreferences.getInstance().getUserName());
        logReq.put("warehouse_id", detailOrd.getAssignWh());
        logReq.put("shipment_id", detailOrd.getShipmentId());
        logReq.put("trent_picklist_id", detailOrd.getTrentPicklistId());
        //logReq.put("grn_details", jaGrnDetails);

        Call<GeneralResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerGrnComplete(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<GeneralResponse>() {
            @Override
            public void onResponse(Call<GeneralResponse> call, Response<GeneralResponse> response) {
                ((BaseActivity) getActivity()).hideProgressDialog();
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                        } else {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                            initOrderData();
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<GeneralResponse> call, Throwable t) {

            }
        });
    }

    public void callAddToSubstituteApi(int id, int related_product_id, int related_product_type) {
        ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("product_id", id);
        logReq.put("related_product_id", related_product_id);
        logReq.put("related_product_type", related_product_type);

        Call<GeneralResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerAddSubstitute(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<GeneralResponse>() {
            @Override
            public void onResponse(Call<GeneralResponse> call, Response<GeneralResponse> response) {
                ((BaseActivity) getActivity()).hideProgressDialog();
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                        } else {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<GeneralResponse> call, Throwable t) {

            }
        });
    }

    public void callSendApprovalApi(List<OrderSubstituteProductsItem> orderSubstituteProducts) {
        JsonArray jaDetails = new JsonArray();
        for (int i = 0; i < orderSubstituteProducts.size(); i++) {
            JsonObject jo = new JsonObject();
            try {
                jo.addProperty("product_id", orderSubstituteProducts.get(i).getProduct().getId());
                jo.addProperty("order_product_id", orderSubstituteProducts.get(i).getId());
                jaDetails.add(jo);
            } catch (Exception e) {
                e.printStackTrace();
            }

        }
        ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("user_id", AppPreferences.getInstance().getUserID());
        logReq.put("warehouse_id", AppPreferences.getInstance().getWarehouseID());
        logReq.put("order_id", detailOrd.getId());
        logReq.put("approval_details", jaDetails);

        Call<GeneralResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerSendApproval(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<GeneralResponse>() {
            @Override
            public void onResponse(Call<GeneralResponse> call, Response<GeneralResponse> response) {
                //((BaseActivity) getActivity()).hideProgressDialog();
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                            ((BaseActivity) getActivity()).hideProgressDialog();
                        } else {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                            orderListItem.get(detailPosition).setSubstitute_status("pending");
                            rvOrderList.getAdapter().notifyItemChanged(detailPosition);
                            callOrderDetailsApi(orderListItem.get(detailPosition).getId(), false);
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                } else {
                    ((BaseActivity) getActivity()).hideProgressDialog();
                }
            }

            @Override
            public void onFailure(Call<GeneralResponse> call, Throwable t) {

            }
        });
    }

    private void callResetSendApprovalApi() {
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("order_id", detailOrd.getId());

        Call<GeneralResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerResetSendApproval(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<GeneralResponse>() {
            @Override
            public void onResponse(Call<GeneralResponse> call, Response<GeneralResponse> response) {
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                        } else {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                            callOrderDetailsApi(orderListItem.get(detailPosition).getId(), false);
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<GeneralResponse> call, Throwable t) {

            }
        });
    }

    private void openEditPriceDialog(final OrderProductsItem orderProductsItem) {
        final Dialog dialogEdit = new Dialog(getActivity());
        dialogEdit.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialogEdit.setCancelable(false);
        dialogEdit.setContentView(R.layout.dialog_edit_price);
        int width = (int) (getResources().getDisplayMetrics().widthPixels * 0.90);
        int height = (int) (getResources().getDisplayMetrics().heightPixels * 0.35);
        dialogEdit.getWindow().setLayout(width, height);
        dialogEdit.show();

        LinearLayout llDialogClose = dialogEdit.findViewById(R.id.llDialogClose);
        TextView tvAddEditPrice = dialogEdit.findViewById(R.id.tvAddEditPrice);
        TextInputEditText etPriceEditPrice = dialogEdit.findViewById(R.id.etPriceEditPrice);

        tvAddEditPrice.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (AppUtilities.isOnline(getActivity())) {
                    if (etPriceEditPrice.getText().length() > 0) {
                        AppUtilities.hideKeyboard(view);
                        dialogEdit.dismiss();
                        callUpdateProductIfoApi(orderProductsItem, Double.parseDouble(etPriceEditPrice.getText().toString()),
                                "", String.valueOf(orderProductsItem.getWeight()), orderProductsItem.getIsSubstitute());
                    }
                } else {
                    Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                }
            }
        });
        llDialogClose.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                AppUtilities.hideKeyboard(v);
                dialogEdit.dismiss();
            }
        });
    }

    private void openUpdatePriceDialog(String price) {
        final Dialog dialogEdit = new Dialog(getActivity());
        dialogEdit.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialogEdit.setCancelable(false);
        dialogEdit.setContentView(R.layout.dialog_update_price);
        int width = (int) (getResources().getDisplayMetrics().widthPixels * 0.90);
        int height = (int) (getResources().getDisplayMetrics().heightPixels * 0.35);
        dialogEdit.getWindow().setLayout(width, height);
        dialogEdit.show();

        LinearLayout llDialogClose = dialogEdit.findViewById(R.id.llDialogClose);
        TextView tvAddEditPrice = dialogEdit.findViewById(R.id.tvAddEditPrice);
        TextInputEditText etPriceEditPrice = dialogEdit.findViewById(R.id.etPriceEditPrice);

        tvAddEditPrice.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (AppUtilities.isOnline(getActivity())) {
                    if (etPriceEditPrice.getText().length() > 0) {
                        AppUtilities.hideKeyboard(view);
                        dialogEdit.dismiss();
                        tvUpdatePriceOrderDetails.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(Double.parseDouble(etPriceEditPrice.getText().toString())));
                        detailOrd.setOrder_net_amount(formater.format(Double.parseDouble(etPriceEditPrice.getText().toString())));
                        callUpdateOrderDetailsApi("", price, etPriceEditPrice.getText().toString());
                    }
                } else {
                    Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                }
            }
        });
        llDialogClose.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                AppUtilities.hideKeyboard(v);
                dialogEdit.dismiss();
            }
        });
    }

    private void openUpdateBillNoDialog() {
        final Dialog dialogEdit = new Dialog(getActivity());
        dialogEdit.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialogEdit.setCancelable(false);
        dialogEdit.setContentView(R.layout.dialog_update_bill);
        int width = (int) (getResources().getDisplayMetrics().widthPixels * 0.90);
        int height = (int) (getResources().getDisplayMetrics().heightPixels * 0.30);
        dialogEdit.getWindow().setLayout(width, height);
        dialogEdit.show();

        LinearLayout llDialogClose = dialogEdit.findViewById(R.id.llDialogClose);
        TextView tvAddEditPrice = dialogEdit.findViewById(R.id.tvAddEditPrice);
        TextInputEditText etPriceEditPrice = dialogEdit.findViewById(R.id.etPriceEditPrice);

        tvAddEditPrice.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (AppUtilities.isOnline(getActivity())) {
                    if (etPriceEditPrice.getText().length() > 0) {
                        AppUtilities.hideKeyboard(view);
                        dialogEdit.dismiss();
                        callUpdateBillNumberApi(etPriceEditPrice.getText().toString());

                    }
                } else {
                    Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                }
            }
        });
        llDialogClose.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                AppUtilities.hideKeyboard(v);
                dialogEdit.dismiss();
            }
        });
    }

    private void openBillNoDialog() {
        final Dialog dialogEdit = new Dialog(getActivity());
        dialogEdit.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialogEdit.setCancelable(false);
        dialogEdit.setContentView(R.layout.dialog_update_bill_update);
        int width = (int) (getResources().getDisplayMetrics().widthPixels * 0.90);
        int height = (int) (getResources().getDisplayMetrics().heightPixels * 0.30);
        dialogEdit.getWindow().setLayout(width, height);
        dialogEdit.show();
dialogEdit.setCanceledOnTouchOutside(true);
        LinearLayout llDialogClose = dialogEdit.findViewById(R.id.llDialogClose);
        TextView tvAddEditPrice = dialogEdit.findViewById(R.id.tvAddEditPrice);
        TextInputEditText etPriceEditPrice = dialogEdit.findViewById(R.id.etPriceEditPrice);
        TextInputLayout til_billNo = dialogEdit.findViewById(R.id.til_billNo);

        tvAddEditPrice.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (AppUtilities.isOnline(getActivity())) {
                    if (etPriceEditPrice.getText().length() > 0) {
                        AppUtilities.hideKeyboard(view);
                        dialogEdit.dismiss();
                        callUpdateBillNumberApi(etPriceEditPrice.getText().toString());

                    }else {
                        til_billNo.setError("Enter Bill Number");
                    }
                } else {
                    Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                }
            }
        });
        llDialogClose.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                AppUtilities.hideKeyboard(v);
                dialogEdit.dismiss();
            }
        });
    }


    @Override
    public void onPermissionsChecked(MultiplePermissionsReport report) {
        if (report.areAllPermissionsGranted()) {
            callUpdateOrderDetailsCSVApi();
            Log.e("onPermissionsChecked", "yes");
        } else {
            Log.e("onPermissionsChecked", "no");
        }
    }

    @Override
    public void onPermissionRationaleShouldBeShown(List<PermissionRequest> permissions, PermissionToken token) {
        token.continuePermissionRequest();
    }

    public class UpdateOrderReceiver extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            ((MainActivity) getActivity()).updateOrderCount(intent.getStringExtra("newOrderCount"));
            if (Integer.parseInt(intent.getStringExtra("substitute_in")) > 0 &&
                    Integer.parseInt(intent.getStringExtra("substitute_out")) == 0) {
                orderListItem.get(detailPosition).setSubstitute_status("done");
                rvOrderList.getAdapter().notifyItemChanged(detailPosition);
                callOrderDetailsApi(orderListItem.get(detailPosition).getId(), false);
            }

        }
    }
}
