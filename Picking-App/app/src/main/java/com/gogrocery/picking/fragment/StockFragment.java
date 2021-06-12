package com.gogrocery.picking.fragment;

import android.app.Dialog;
import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.material.textfield.TextInputEditText;
import com.gogrocery.picking.R;
import com.gogrocery.picking.activity.BaseActivity;
import com.gogrocery.picking.adapter.StockListAdapter;
import com.gogrocery.picking.network.APIClient;
import com.gogrocery.picking.network.APIInterface;
import com.gogrocery.picking.prefrences.AppPreferences;
import com.gogrocery.picking.response_pojo.category_list_pojo.CategoryListItem;
import com.gogrocery.picking.response_pojo.category_list_pojo.CategoryListResponse;
import com.gogrocery.picking.response_pojo.general_pojo.GeneralResponse;
import com.gogrocery.picking.response_pojo.stock_list_pojo.StockItem;
import com.gogrocery.picking.response_pojo.stock_list_pojo.StockListResponse;
import com.gogrocery.picking.utils.AppUtilities;
import com.gogrocery.picking.utils.SimpleDividerItemDecoration;
import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;
import com.toptoche.searchablespinnerlibrary.SearchableSpinner;

import java.util.ArrayList;
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

public class StockFragment extends Fragment {
    RecyclerView rvStock;
    Spinner spInStock, spHasPriceStock;
    SearchableSpinner spCategoryStock, spSubCategoryStock;
    TextView tvSearchStock, tvNoValueStock, tvScanStock;
    EditText etSearchStock;
    List<CategoryListItem> mainCategoryList = new ArrayList<>();
    List<CategoryListItem> categoryList = new ArrayList<>();
    List<CategoryListItem> subCategoryList = new ArrayList<>();
    List<String> categorySpinnerStr = new ArrayList<>();
    List<String> subCategorySpinnerStr = new ArrayList<>();
    List<String> instockSpinnerStr = new ArrayList<>();
    List<String> hasPriceSpinnerStr = new ArrayList<>();
    String selCategoryID, selSubCategoryID, strSearchProduct = "", selInstock = "y", selHasPrice = "y";
    int start_index_stock = 1;
    List<StockItem> stockItems = new ArrayList<>();
    Boolean isStockLoading = false;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        //return super.onCreateView(inflater, container, savedInstanceState);
        View view = inflater.inflate(R.layout.fragment_stock, container, false);
        initView(view);
        return view;
    }

    private void initView(View view) {
        rvStock = view.findViewById(R.id.rvStock);
        spCategoryStock = view.findViewById(R.id.spCategoryStock);
        spSubCategoryStock = view.findViewById(R.id.spSubCategoryStock);
        spInStock = view.findViewById(R.id.spInStock);
        spHasPriceStock = view.findViewById(R.id.spHasPriceStock);
        tvSearchStock = view.findViewById(R.id.tvSearchStock);
        tvNoValueStock = view.findViewById(R.id.tvNoValueStock);
        etSearchStock = view.findViewById(R.id.etSearchStock);
        tvScanStock = view.findViewById(R.id.tvScanStock);
        tvNoValueStock.setVisibility(View.VISIBLE);
        rvStock.setVisibility(View.GONE);

        spCategoryStock.setTitle("Select Category");
        spSubCategoryStock.setTitle("Select Sub Category");
        spCategoryStock.setPositiveButton("Close");
        spSubCategoryStock.setPositiveButton("Close");

        spCategoryStock.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
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
        spSubCategoryStock.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
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
        spInStock.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                if (i != 0 && instockSpinnerStr.size() > 0) {
                    if (i == 1) {
                        selInstock = "y";
                    } else {
                        selInstock = "n";
                    }
                    //selInstock = String.valueOf(instockSpinnerStr.get(i));
                } else {
                    selInstock = "";
                    //AppUtilities.showSpinnerAsMandatory(setupBinding.spRegister);
                }
            }

            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {
            }
        });

        spHasPriceStock.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                if (i != 0 && hasPriceSpinnerStr.size() > 0) {
                    if (i == 1) {
                        selHasPrice = "y";
                    } else {
                        selHasPrice = "n";
                    }
                    //selHasPrice = String.valueOf(hasPriceSpinnerStr.get(i));
                } else {
                    selHasPrice = "";
                    //AppUtilities.showSpinnerAsMandatory(setupBinding.spRegister);
                }
            }

            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {
            }
        });

        tvSearchStock.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                stockItems.clear();
                start_index_stock = 1;
                if (AppUtilities.isOnline(getActivity())) {
                    AppUtilities.hideKeyboard(view);
                    callSearchStock(false);
                } else {
                    Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                }
            }
        });

        rvStock.addOnScrollListener(new RecyclerView.OnScrollListener() {
            @Override
            public void onScrolled(@NonNull RecyclerView recyclerView, int dx, int dy) {
                super.onScrolled(recyclerView, dx, dy);
                if (dy > 0 && !isStockLoading) {
                    if (rvStock.getLayoutManager() != null && ((LinearLayoutManager) rvStock.getLayoutManager()).findLastCompletelyVisibleItemPosition() == stockItems.size() - 1) {
                        //bottom of list!
                        isStockLoading = true;
                        onLoadNextPageStock();
                    }
                }
            }
        });

        etSearchStock.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {
            }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {
                strSearchProduct = charSequence.toString();
            }

            @Override
            public void afterTextChanged(Editable editable) {
            }
        });
        if (AppUtilities.isOnline(getActivity())) {
            callCategoryListApi();
        } else {
            Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
        }

        tvScanStock.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                AppUtilities.hideKeyboard(view);
                IntentIntegrator.forSupportFragment(StockFragment.this).initiateScan();
            }
        });
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
                if (result.getContents().length() > 0) {
                    strSearchProduct = result.getContents();
                    stockItems.clear();
                    start_index_stock = 1;
                    if (AppUtilities.isOnline(getActivity())) {
                        callSearchStock(false);
                    } else {
                        Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                    }
                }
            }
        } else {
            super.onActivityResult(requestCode, resultCode, data);
        }
    }

    @Override
    public void onPause() {
        super.onPause();
        etSearchStock.setText("");
    }

    private void onLoadNextPageStock() {
        start_index_stock += 1;
        if (AppUtilities.isOnline(getActivity())) {
            callSearchStock(true);
        } else {
            Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
        }
    }

    private void setupRestockRecycler() {
        rvStock.setLayoutManager(new LinearLayoutManager(getActivity()));
        rvStock.setNestedScrollingEnabled(false);
        rvStock.setAdapter(new StockListAdapter(getActivity(), stockItems, new StockListAdapter.StockListClickListener() {
            @Override
            public void stockListClick(int position, boolean checked) {
                //openEditStockDialog(stockItems.get(position),position);
                if (AppUtilities.isOnline(getActivity())) {
                    if (checked) {
                        callManageStockApi(stockItems.get(position).getChannelCurrencyProductPrice().getPrice().toString(), stockItems.get(position).getId(), position, "100");
                    } else {
                        callManageStockApi(stockItems.get(position).getChannelCurrencyProductPrice().getPrice().toString(), stockItems.get(position).getId(), position, "0");
                    }
                } else {
                    Toast.makeText(getActivity(), getResources().getString(R.string.txtNetworkNotAvailable), Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onEditClick(int position) {
                openEditPriceDialog(stockItems.get(position), position);
            }
        }));
        rvStock.addItemDecoration(new SimpleDividerItemDecoration(getActivity()));
        isStockLoading = false;
    }

    private void openEditPriceDialog(StockItem stockItem, int position) {
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
                        callManageStockApi(etPriceEditPrice.getText().toString(), stockItem.getId(), position, "");
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

    private void openEditStockDialog(StockItem stockItem, int position) {
        final Dialog dialogEdit = new Dialog(getActivity());
        dialogEdit.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialogEdit.setCancelable(false);
        dialogEdit.setContentView(R.layout.dialog_edit_stock);
        int width = (int) (getResources().getDisplayMetrics().widthPixels * 0.90);
        int height = (int) (getResources().getDisplayMetrics().heightPixels * 0.35);
        dialogEdit.getWindow().setLayout(width, height);
        dialogEdit.show();

        LinearLayout llDialogClose = dialogEdit.findViewById(R.id.llDialogClose);
        llDialogClose.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                AppUtilities.hideKeyboard(v);
                dialogEdit.dismiss();
            }
        });
    }

    private void callManageStockApi(String newPrice, int id, int position, String stock) {
        ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("user_id", AppPreferences.getInstance().getUserID());
        logReq.put("product_id", id);
        logReq.put("warehouse_id", AppPreferences.getInstance().getWarehouseID());
        logReq.put("price", newPrice);
        logReq.put("stock", stock);

        Call<GeneralResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerManageStock(
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
                            stockItems.get(position).getChannelCurrencyProductPrice().setPrice(Double.parseDouble(newPrice));
                            if (stock.length() > 0) {
                                stockItems.get(position).getProductStock().setRealStock(Integer.parseInt(stock));
                            }
                            rvStock.getAdapter().notifyItemChanged(position);
                            //Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
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

    private void callCategoryListApi() {
        ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("warehouse_id", AppPreferences.getInstance().getWarehouseID());
        Call<CategoryListResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerCategoryList(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<CategoryListResponse>() {
            @Override
            public void onResponse(Call<CategoryListResponse> call, Response<CategoryListResponse> response) {
                ((BaseActivity) getActivity()).hideProgressDialog();
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

    private void callSearchStock(Boolean isLoadMore) {
        ((BaseActivity) getActivity()).showProgressDialog(getActivity(), getResources().getString(R.string.txtLoading));
        HashMap<String, Object> logReq = new HashMap<>();
        logReq.put("website_id", AppPreferences.getInstance().getWebsiteID());
        logReq.put("warehouse_id", AppPreferences.getInstance().getWarehouseID());
        if (selSubCategoryID.length() > 0) {
            logReq.put("category_id", selSubCategoryID);
        } else {
            logReq.put("category_id", selCategoryID);
        }
        logReq.put("in_stock", selInstock);
        logReq.put("has_price", selHasPrice);
        logReq.put("page", start_index_stock);
        logReq.put("per_page", 10);
        logReq.put("search", strSearchProduct);

        Call<StockListResponse> response1 = APIClient.getClient().create(APIInterface.class).pickerStockSearch(
                "Token " + AppPreferences.getInstance().getUserToken(), logReq);
        response1.enqueue(new Callback<StockListResponse>() {
            @Override
            public void onResponse(Call<StockListResponse> call, Response<StockListResponse> response) {
                ((BaseActivity) getActivity()).hideProgressDialog();
                if (response.code() == 200) {
                    try {
                        if (response.body().getStatus() == 0) {
                            Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                            tvNoValueStock.setVisibility(View.VISIBLE);
                            rvStock.setVisibility(View.GONE);
                        } else {
                            //Toast.makeText(getActivity(), response.body().getMessage(), Toast.LENGTH_SHORT).show();
                            stockItems.addAll(response.body().getResponse());
                            if (stockItems.size() > 0) {
                                if (isLoadMore) {
                                    rvStock.getAdapter().notifyItemChanged(stockItems.size());
                                    isStockLoading = false;
                                } else {
                                    setupRestockRecycler();
                                }
                                tvNoValueStock.setVisibility(View.GONE);
                                rvStock.setVisibility(View.VISIBLE);

                            } else {
                                tvNoValueStock.setVisibility(View.VISIBLE);
                                rvStock.setVisibility(View.GONE);
                            }
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void onFailure(Call<StockListResponse> call, Throwable t) {
                Log.e("callSearchStock", "onFailure" + t.getLocalizedMessage());
            }
        });
    }

    private void setupSpinner() {
        categorySpinnerStr.clear();
        instockSpinnerStr.clear();
        hasPriceSpinnerStr.clear();
        categorySpinnerStr.add(getResources().getString(R.string.txtCategory));
        instockSpinnerStr.add(getResources().getString(R.string.txtStock));
        instockSpinnerStr.add("In-stock");
        instockSpinnerStr.add("Out of stock");
        hasPriceSpinnerStr.add(getResources().getString(R.string.txtHasPrice));
        hasPriceSpinnerStr.add("Yes");
        hasPriceSpinnerStr.add("No");
        for (int i = 0; i < categoryList.size(); i++) {
            categorySpinnerStr.add(categoryList.get(i).getName());
        }
        ArrayAdapter aaCategory = new ArrayAdapter(getActivity(), R.layout.spinner_layout, categorySpinnerStr);
        aaCategory.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        //Setting the ArrayAdapter data on the Spinner
        spCategoryStock.setAdapter(aaCategory);

        ArrayAdapter aaInstock = new ArrayAdapter(getActivity(), R.layout.spinner_layout, instockSpinnerStr);
        aaInstock.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        //Setting the ArrayAdapter data on the Spinner
        spInStock.setAdapter(aaInstock);

        ArrayAdapter aaHasPrice = new ArrayAdapter(getActivity(), R.layout.spinner_layout, hasPriceSpinnerStr);
        aaHasPrice.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        //Setting the ArrayAdapter data on the Spinner
        spHasPriceStock.setAdapter(aaHasPrice);
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
        spSubCategoryStock.setAdapter(aaSubCategory);
    }
}
