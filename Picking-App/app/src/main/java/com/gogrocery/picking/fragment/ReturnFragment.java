package com.gogrocery.picking.fragment;

import android.app.Dialog;
import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextUtils;
import android.text.TextWatcher;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;
import com.gogrocery.picking.R;
import com.gogrocery.picking.activity.BaseActivity;
import com.gogrocery.picking.adapter.ReturnAdapter;
import com.gogrocery.picking.network.APIClient;
import com.gogrocery.picking.network.APIInterface;
import com.gogrocery.picking.prefrences.AppPreferences;
import com.gogrocery.picking.response_pojo.confirm_return_pojo.ConfirmReturnResponse;
import com.gogrocery.picking.response_pojo.search_return_pojo.OrderProductsItem;
import com.gogrocery.picking.response_pojo.search_return_pojo.SearchReturnItem;
import com.gogrocery.picking.response_pojo.search_return_pojo.SearchReturnResponse;
import com.gogrocery.picking.utils.AppUtilities;
import com.gogrocery.picking.utils.MyDialog;
import com.gogrocery.picking.utils.SimpleDividerItemDecoration;

import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashMap;
import java.util.List;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ReturnFragment extends Fragment {
    RecyclerView rvReturn;
    TextView tvSelectDateReturn, tvSearchReturn, tvBarcodeReturn, tvOrdNumberReturn, tvAddressReturn, tvSubtotalReturn, tvTotalPriceReturn;
    TextView tvDeliveryFeeReturn, tvConfirmReturn,tvDiscountReturn,tvReturnAmtReturn,tvBillNoReturn;
    EditText etBillNumberReturn, etOrdNumberReturn, etSearchTextReturn;
    RelativeLayout rlSelectDateReturn, rlMainDetailsReturn;
    String date = "", searchText = "";
    SearchReturnItem searchReturnDetails;
    List<Integer> initReturnQty = new ArrayList<>();
    DecimalFormat formater = new DecimalFormat("0.00");

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        //return super.onCreateView(inflater, container, savedInstanceState);
        View view = inflater.inflate(R.layout.fragment_return, container, false);
        Log.e("onCreateView", "onCreateView");
        initView(view);
        return view;
    }

    private void initView(View view) {
        rvReturn = view.findViewById(R.id.rvReturn);
        tvSelectDateReturn = view.findViewById(R.id.tvSelectDateReturn);
        rlSelectDateReturn = view.findViewById(R.id.rlSelectDateReturn);
        etBillNumberReturn = view.findViewById(R.id.etBillNumberReturn);
        etOrdNumberReturn = view.findViewById(R.id.etOrdNumberReturn);
        etSearchTextReturn = view.findViewById(R.id.etSearchTextReturn);
        tvSearchReturn = view.findViewById(R.id.tvSearchReturn);
        tvBarcodeReturn = view.findViewById(R.id.tvBarcodeReturn);
        tvOrdNumberReturn = view.findViewById(R.id.tvOrdNumberReturn);
        tvAddressReturn = view.findViewById(R.id.tvAddressReturn);
        tvBillNoReturn = view.findViewById(R.id.tvBillNoReturn);
        tvSubtotalReturn = view.findViewById(R.id.tvSubtotalReturn);
        tvTotalPriceReturn = view.findViewById(R.id.tvTotalPriceReturn);
        tvDeliveryFeeReturn = view.findViewById(R.id.tvDeliveryFeeReturn);
        rlMainDetailsReturn = view.findViewById(R.id.rlMainDetailsReturn);
        tvConfirmReturn = view.findViewById(R.id.tvConfirmReturn);
        tvDiscountReturn = view.findViewById(R.id.tvDiscountReturn);
        tvReturnAmtReturn = view.findViewById(R.id.tvReturnAmtReturn);
        etSearchTextReturn.setSaveEnabled(false);
        etBillNumberReturn.setSaveEnabled(false);
        etOrdNumberReturn.setSaveEnabled(false);

        rlSelectDateReturn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openDatePicker();
            }
        });
        etSearchTextReturn.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {
            }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {
                searchText = charSequence.toString();
            }

            @Override
            public void afterTextChanged(Editable editable) {
            }
        });
        tvSearchReturn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (etOrdNumberReturn.getText().length() > 0) {
                    if (AppUtilities.isOnline(getActivity())) {
                        AppUtilities.hideKeyboard(view);
                        rlMainDetailsReturn.setVisibility(View.GONE);
                        callSearchReturnApi();
                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                    }
                } else {
                    Toast.makeText(getActivity(), getActivity().getResources().getString(R.string.txtEnterOrderNumber), Toast.LENGTH_SHORT).show();
                }
            }
        });
        tvBarcodeReturn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //etSearchTextReturn.setText("");
                IntentIntegrator.forSupportFragment(ReturnFragment.this).initiateScan();
            }
        });
        tvConfirmReturn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                JsonArray jaDetails = new JsonArray();
                for (int i = 0; i < searchReturnDetails.getOrderProducts().size(); i++) {
                    if (searchReturnDetails.getOrderProducts().get(i).getReturns() > 0 &&
                            searchReturnDetails.getOrderProducts().get(i).getReturns() > initReturnQty.get(i)) {
                        JsonObject jo = new JsonObject();
                        try {
                            jo.addProperty("product_id", searchReturnDetails.getOrderProducts().get(i).getProduct().getId());
                            jo.addProperty("order_product_id", searchReturnDetails.getOrderProducts().get(i).getId());
                            jo.addProperty("return_qty", searchReturnDetails.getOrderProducts().get(i).getReturns() - initReturnQty.get(i));
                            jaDetails.add(jo);
                        } catch (Exception e) {
                            e.printStackTrace();
                        }

                    }
                }
                if (jaDetails.size() > 0) {
                    if (AppUtilities.isOnline(getActivity())) {
                        callConfirmReturnApi(jaDetails);
                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                    }
                } else {

                }
            }
        });
        rlMainDetailsReturn.setVisibility(View.GONE);
        etSearchTextReturn.setText("");
        etBillNumberReturn.setText("");
        etOrdNumberReturn.setText("");
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        IntentResult result = IntentIntegrator.parseActivityResult(requestCode, resultCode, data);
        if (result != null) {
            if (result.getContents() == null) {
                Toast.makeText(getActivity(), "Cancelled", Toast.LENGTH_LONG).show();
            } else {
                //Toast.makeText(getActivity(), "Scanned: " + result.getContents(), Toast.LENGTH_LONG).show();
                etSearchTextReturn.setText(result.getContents());
            }
        } else {
            super.onActivityResult(requestCode, resultCode, data);
        }
    }

    private void openDatePicker() {
        final Dialog dialog = new Dialog(getActivity());
        dialog.setContentView(R.layout.dialog_datepickerview);
        dialog.setTitle("");

        DatePicker datePicker = (DatePicker) dialog.findViewById(R.id.datePicker1);
        Calendar calendar = Calendar.getInstance();
        calendar.setTimeInMillis(System.currentTimeMillis());
        final int[] selectedDate = {calendar.get(Calendar.DAY_OF_MONTH)};
        final int[] selectedMonth = {calendar.get(Calendar.MONTH)};
        final int[] selectedYear = {calendar.get(Calendar.YEAR)};
        datePicker.setMaxDate(System.currentTimeMillis());
        datePicker.init(calendar.get(Calendar.YEAR), calendar.get(Calendar.MONTH), calendar.get(Calendar.DAY_OF_MONTH), new DatePicker.OnDateChangedListener() {

            @Override
            public void onDateChanged(DatePicker datePicker, int year, int month, int dayOfMonth) {
                if (selectedDate[0] == dayOfMonth && selectedMonth[0] == month && selectedYear[0] == year) {

                    //tvEndDateSetupCampaign.setText("Year=" + year + " Month=" + (month + 1) + " day=" + dayOfMonth);
                    if (dayOfMonth < 10) {
                        tvSelectDateReturn.setText("0" + dayOfMonth + "-" + (month + 1) + "-" + year);
                        date = year + "-" + (month + 1) + "-" + "0" + dayOfMonth;
                    } else {
                        tvSelectDateReturn.setText(dayOfMonth + "-" + (month + 1) + "-" + year);
                        date = year + "-" + (month + 1) + "-" + dayOfMonth;
                    }

                    dialog.dismiss();
                } else {
                    if (selectedDate[0] != dayOfMonth) {
                        //tvEndDateSetupCampaign.setText("Year=" + year + " Month=" + (month + 1) + " day=" + dayOfMonth);
                        if (dayOfMonth < 10) {
                            tvSelectDateReturn.setText("0" + dayOfMonth + "-" + (month + 1) + "-" + year);
                            date = year + "-" + (month + 1) + "-" + "0" + dayOfMonth;
                        } else {
                            tvSelectDateReturn.setText(dayOfMonth + "-" + (month + 1) + "-" + year);
                            date = year + "-" + (month + 1) + "-" + dayOfMonth;
                        }
                        dialog.dismiss();
                    } else {
                        if (selectedMonth[0] != month) {
                            //tvEndDateSetupCampaign.setText("Year=" + year + " Month=" + (month + 1) + " day=" + dayOfMonth);

                            if (dayOfMonth < 10) {
                                tvSelectDateReturn.setText("0" + dayOfMonth + "-" + (month + 1) + "-" + year);
                                date = year + "-" + (month + 1) + "-" + "0" + dayOfMonth;
                            } else {
                                tvSelectDateReturn.setText(dayOfMonth + "-" + (month + 1) + "-" + year);
                                date = year + "-" + (month + 1) + "-" + dayOfMonth;
                            }

                            dialog.dismiss();
                        }
                    }
                }
                selectedDate[0] = dayOfMonth;
                selectedMonth[0] = (month);
                selectedYear[0] = year;
            }
        });
        dialog.show();
    }

    private void callSearchReturnApi() {
        ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("warehouse_id", AppPreferences.getInstance().getWarehouseID());
        logReq.put("order_date", date);
        logReq.put("order_no", etOrdNumberReturn.getText().toString());
        logReq.put("invoice_no", etBillNumberReturn.getText().toString());
        logReq.put("search", searchText);

        Call<SearchReturnResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerSearchReturn(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<SearchReturnResponse>() {
            @Override
            public void onResponse(Call<SearchReturnResponse> call, Response<SearchReturnResponse> response) {
                ((BaseActivity) getActivity()).hideProgressDialog();
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                            rlMainDetailsReturn.setVisibility(View.GONE);
                        } else {
                            searchReturnDetails = response.body().getResponse().get(0);
                            setupDetailSection(response.body().getResponse());

                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<SearchReturnResponse> call, Throwable t) {
                Log.e("callSearchReturnApi", "onFailure" + t.getLocalizedMessage());
            }
        });
    }

    private void setupDetailSection(List<SearchReturnItem> response) {
        tvOrdNumberReturn.setText(getActivity().getResources().getString(R.string.txtOrder) + " " + response.get(0).getCustomOrderId());
        StringBuilder strAddress = new StringBuilder();
        if (response.get(0).getDeliveryName() != null && response.get(0).getDeliveryName().length() > 0) {
            strAddress.append(response.get(0).getDeliveryName() + " , ");
        }
        if (response.get(0).getDeliveryStreetAddress() != null && response.get(0).getDeliveryStreetAddress().length() > 0) {
            strAddress.append(response.get(0).getDeliveryStreetAddress() + " , ");
        }
        if (response.get(0).getDeliveryStreetAddress1() != null && response.get(0).getDeliveryStreetAddress1().length() > 0) {
            strAddress.append(response.get(0).getDeliveryStreetAddress1() + " , ");
        }
        if (response.get(0).getDeliveryCity() != null && response.get(0).getDeliveryCity().length() > 0) {
            strAddress.append(response.get(0).getDeliveryCity() + " , ");
        }
        if (response.get(0).getDeliveryPostcode() != null && response.get(0).getDeliveryPostcode().length() > 0) {
            strAddress.append(response.get(0).getDeliveryPostcode() + " , ");
        }
        if (response.get(0).getDeliveryStateName() != null && response.get(0).getDeliveryStateName().length() > 0) {
            strAddress.append(response.get(0).getDeliveryStateName() + " , ");
        }
        if (response.get(0).getDeliveryPhone() != null && response.get(0).getDeliveryPhone().length() > 0) {
            strAddress.append("\n\n" + response.get(0).getDeliveryPhone() + " , ");
        }
        tvAddressReturn.setText(strAddress.toString().substring(0, strAddress.toString().length() - 2));
        if (response.get(0).getChannelOrderId() != null || !TextUtils.isEmpty(response.get(0).getChannelOrderId())) {
            tvBillNoReturn.setText(getActivity().getResources().getString(R.string.txtBillNumber)+" "+response.get(0).getChannelOrderId());
            tvBillNoReturn.setVisibility(View.VISIBLE);
        }else{
            tvBillNoReturn.setVisibility(View.GONE);
        }
        tvSubtotalReturn.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(response.get(0).getNetAmount()));
        tvTotalPriceReturn.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(response.get(0).getGrossAmount()));
        tvDeliveryFeeReturn.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(response.get(0).getShippingCost()));
        tvDiscountReturn.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(response.get(0).getCartDiscount()));
        tvReturnAmtReturn.setText(AppPreferences.getInstance().getCurrency() + " " + formater.format(response.get(0).getReturn_amount()));
        tvConfirmReturn.setAlpha(.5f);
        tvConfirmReturn.setClickable(false);
        List<OrderProductsItem> tmpProduct=response.get(0).getOrderProducts();
        if (response.get(0).getOrderSubstituteProducts().size() > 0) {
            for (int i = 0; i < response.get(0).getOrderSubstituteProducts().size(); i++) {
                if (response.get(0).getOrderSubstituteProducts().get(i).getSend_approval() != null) {
                    if (response.get(0).getOrderSubstituteProducts().get(i).getSend_approval().equalsIgnoreCase("approve")) {
                        Gson gson = new Gson();
                        String json = gson.toJson(response.get(0).getOrderSubstituteProducts().get(i));
                        tmpProduct.add(gson.fromJson(json, OrderProductsItem.class));
                    }
                }
            }
            setupRecycler(tmpProduct);
        } else {
            setupRecycler(tmpProduct);
        }
        //setupRecycler(response.get(0).getOrderProducts());
        rlMainDetailsReturn.setVisibility(View.VISIBLE);
    }

    private void setupRecycler(List<OrderProductsItem> orderProducts) {
        initReturnQty.clear();
        for (int i = 0; i < orderProducts.size(); i++) {
            initReturnQty.add(orderProducts.get(i).getReturns());
        }
        rvReturn.setLayoutManager(new LinearLayoutManager(getActivity()));
        rvReturn.setAdapter(new ReturnAdapter(getActivity(), orderProducts, initReturnQty, new ReturnAdapter.ReturnListClickListener() {
            @Override
            public void returnListClick(int position) {
                boolean isChange=false;
                for (int i = 0; i < searchReturnDetails.getOrderProducts().size(); i++) {
                    if (searchReturnDetails.getOrderProducts().get(i).getReturns() > 0 &&
                            searchReturnDetails.getOrderProducts().get(i).getReturns() > initReturnQty.get(i)) {
                        isChange=true;
                        break;
                    }
                }
                if(isChange){
                    tvConfirmReturn.setAlpha(1f);
                    tvConfirmReturn.setClickable(true);
                }else{
                    tvConfirmReturn.setAlpha(.5f);
                    tvConfirmReturn.setClickable(false);
                }
            }
        }));
        rvReturn.addItemDecoration(new SimpleDividerItemDecoration(getActivity()));
    }

    private void callConfirmReturnApi(JsonArray jaDetails) {
        ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("user_id", AppPreferences.getInstance().getUserID());
        logReq.put("order_id", searchReturnDetails.getId());
        logReq.put("shipment_id", searchReturnDetails.getShipmentId());
        logReq.put("trent_picklist_id", searchReturnDetails.getTrentPicklistId());
        logReq.put("return_details", jaDetails);

        Call<ConfirmReturnResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerConfirmReturn(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<ConfirmReturnResponse>() {
            @Override
            public void onResponse(Call<ConfirmReturnResponse> call, Response<ConfirmReturnResponse> response) {
                ((BaseActivity) getActivity()).hideProgressDialog();
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                        } else {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                            MyDialog.defaultShowInfoPopup(getActivity(),"Return Amount",String.valueOf(response.body().getResponse().getCurrentReturnAmount()),"Ok");
                            callSearchReturnApi();
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<ConfirmReturnResponse> call, Throwable t) {

            }
        });
    }
}
