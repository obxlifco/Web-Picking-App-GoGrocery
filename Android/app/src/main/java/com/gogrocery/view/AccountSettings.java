package com.gogrocery.view;

import android.app.Activity;
import android.app.Dialog;
import android.content.Context;
import android.content.Intent;
import androidx.databinding.DataBindingUtil;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Build;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowManager;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Models.MyAccountModel.MyAccountModel;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityAccountSettingsBinding;
import com.google.android.material.textfield.TextInputEditText;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class AccountSettings extends AppCompatActivity {

    private ActivityAccountSettingsBinding mActivityAccountSettingsBinding;
    private String responsePass = "";
    private SharedPreferenceManager mSharedPreferenceManager;
View rootView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityAccountSettingsBinding = DataBindingUtil.setContentView(this, R.layout.activity_account_settings);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());

        rootView = this.findViewById(android.R.id.content).getRootView();
        Constants.setupUI(rootView, AccountSettings.this);
        hideStatusBarColor();

        mActivityAccountSettingsBinding.ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
        EditTextCheckValidate();
        setPageUI();
        mActivityAccountSettingsBinding.btnSave.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (mActivityAccountSettingsBinding.edtFirstName.getText().toString().isEmpty()) {
                    mActivityAccountSettingsBinding.tilFirstname.setError(getString(R.string.error_msg_enter_first_name));
                } else if (mActivityAccountSettingsBinding.edtLastName.getText().toString().isEmpty()) {
                    mActivityAccountSettingsBinding.tilLastName.setError(getString(R.string.error_msg_enter_last_name));
                } else if (mActivityAccountSettingsBinding.edtEmailAddress.getText().toString().isEmpty()) {
                    mActivityAccountSettingsBinding.tilEmailAddress.setError(getString(R.string.error_msg_enter_email));
                } else if (mActivityAccountSettingsBinding.edtMObileNo.getText().toString().isEmpty()) {
                    mActivityAccountSettingsBinding.tilMobileNo.setError(getString(R.string.error_msg_enter_mobile_no));
                } else if (mActivityAccountSettingsBinding.edtCarrierNo.getText().toString().isEmpty()) {
                    Constants.showToastInMiddle(getApplicationContext(),  getString(R.string.error_msg_enter_carrier_code));
                } else if (mActivityAccountSettingsBinding.edtMObileNo.length() != 7) {
                    mActivityAccountSettingsBinding.tilMobileNo.setError(getString(R.string.error_msg_enter_7_digit_mobile_no));
                } else {
                    try {
                        requestMyProfileUpdate();
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            }
        });









/*
        mActivityAccountSettingsBinding.rlCp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent rlCp = new Intent(AccountSettings.this, ChangePassword.class);
                startActivity(rlCp);
            }
        });
*/

     /*   AutoCompleteTextView actvReason = bottomSheetDialogReason.findViewById(R.id.actvReason);
        String[] mList = {"Wrong product selected", "Wrong price", "Ordered by mistake", "Other"};
        setDropdownReason(actvReason, mList);*/

        mActivityAccountSettingsBinding.edtGender.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                if (hasFocus) {
                    genderDialog();
                }

            }
        });
        mActivityAccountSettingsBinding.edtGender.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                genderDialog();
            }
        });


        mActivityAccountSettingsBinding.edtCarrierNo.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                if (hasFocus) {
                    carrierDialog();
                }

            }
        });
        mActivityAccountSettingsBinding.edtCarrierNo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                carrierDialog();
            }
        });


    }

    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }
    private void EditTextCheckValidate(){
        mActivityAccountSettingsBinding.edtFirstName.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                String result = s.toString().replaceAll(" ", "");
                if (!s.toString().equals(result)) {
                    mActivityAccountSettingsBinding.edtFirstName.setText(result);
                    mActivityAccountSettingsBinding.edtFirstName.setSelection(result.length());
                    // alert the user
                }
                mActivityAccountSettingsBinding.tilFirstname.setError(null);

            }
        });

        mActivityAccountSettingsBinding.edtLastName.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {

                String result = s.toString().replaceAll(" ", "");
                if (!s.toString().equals(result)) {
                    mActivityAccountSettingsBinding.edtLastName.setText(result);
                    mActivityAccountSettingsBinding.edtLastName.setSelection(result.length());
                    // alert the user
                }
                mActivityAccountSettingsBinding.tilLastName.setError(null);
            }
        });

        mActivityAccountSettingsBinding.edtEmailAddress.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {

                String result = s.toString().replaceAll(" ", "");
                if (!s.toString().equals(result)) {
                    mActivityAccountSettingsBinding.edtEmailAddress.setText(result);
                    mActivityAccountSettingsBinding.edtEmailAddress.setSelection(result.length());
                    // alert the user
                }
                mActivityAccountSettingsBinding.tilEmailAddress.setError(null);
            }
        });
        mActivityAccountSettingsBinding.edtMObileNo.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {

                String result = s.toString().replaceAll(" ", "");
                if (!s.toString().equals(result)) {
                    mActivityAccountSettingsBinding.edtMObileNo.setText(result);
                    mActivityAccountSettingsBinding.edtMObileNo.setSelection(result.length());
                    // alert the user
                }
                mActivityAccountSettingsBinding.tilMobileNo.setError(null);
            }
        });






    }






















    private void genderDialog() {
        Dialog mGenderDialog = new Dialog(AccountSettings.this);
        mGenderDialog.setContentView(R.layout.gender_dialog);
        RadioGroup rgGenderOptions;
        RadioButton rbMale, rbFemale, rbOthers;
        Button dialogBtnCancel, dialogBtnApply;
        String setText = "";

        dialogBtnCancel = mGenderDialog.findViewById(R.id.dialogBtnCancel);
        dialogBtnApply = mGenderDialog.findViewById(R.id.dialogBtnApply);
        rgGenderOptions = mGenderDialog.findViewById(R.id.rgGenderOptions);
        rbMale = mGenderDialog.findViewById(R.id.rbMale);
        rbFemale = mGenderDialog.findViewById(R.id.rbFemale);
        rbOthers = mGenderDialog.findViewById(R.id.rbOthers);


        //.put("sort",new JSONArray().put(new JSONObject().put("numberof_view",new JSONObject().put("order","desc"))))

        switch (rgGenderOptions.getCheckedRadioButtonId()) {
            case R.id.rbMale:
                setText = "Male";
                break;
            case R.id.rbFemale:
                setText = "Female";
                break;
            case R.id.rbOthers:
                setText = "Other";
                break;
        }

        String finalSetText = setText;
        dialogBtnApply.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (rgGenderOptions.getCheckedRadioButtonId() == -1) {
                    Toast.makeText(getApplicationContext(), "Please select any one", Toast.LENGTH_SHORT).show();
                } else {
                    RadioButton mRadioButton = mGenderDialog.findViewById(rgGenderOptions.getCheckedRadioButtonId());
                    mActivityAccountSettingsBinding.edtGender.setText(mRadioButton.getText().toString());
                    mGenderDialog.dismiss();
                }
            }
        });
        dialogBtnCancel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mGenderDialog.dismiss();
            }
        });

        mGenderDialog.show();
    }


    private void carrierDialog() {
        Dialog mCarrierDilog = new Dialog(AccountSettings.this);
        mCarrierDilog.setContentView(R.layout.carrier_code_dialog);
        TextView tv50, tv52, tv53, tv54, tv55, tv56, tv58;
        tv50 = mCarrierDilog.findViewById(R.id.tv50);
        tv52 = mCarrierDilog.findViewById(R.id.tv52);
        tv53 = mCarrierDilog.findViewById(R.id.tv53);
        tv54 = mCarrierDilog.findViewById(R.id.tv54);
        tv55 = mCarrierDilog.findViewById(R.id.tv55);
        tv56 = mCarrierDilog.findViewById(R.id.tv56);
        tv58 = mCarrierDilog.findViewById(R.id.tv58);
        String selected = "";

        tv50.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                mActivityAccountSettingsBinding.edtCarrierNo.setText(getResources().getString(R.string._50)+"  ");
                mCarrierDilog.dismiss();
            }
        });
        tv52.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityAccountSettingsBinding.edtCarrierNo.setText(getResources().getString(R.string._52)+"  ");
                mCarrierDilog.dismiss();
            }
        });
        tv53.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityAccountSettingsBinding.edtCarrierNo.setText(getResources().getString(R.string._53)+"  ");
                mCarrierDilog.dismiss();
            }
        });
        tv54.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityAccountSettingsBinding.edtCarrierNo.setText(getResources().getString(R.string._54)+"  ");
                mCarrierDilog.dismiss();
            }
        });
        tv55.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityAccountSettingsBinding.edtCarrierNo.setText(getResources().getString(R.string._55)+"  ");
                mCarrierDilog.dismiss();
            }
        });
        tv56.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityAccountSettingsBinding.edtCarrierNo.setText(getResources().getString(R.string._56)+"  ");
                mCarrierDilog.dismiss();
            }
        });
        tv58.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityAccountSettingsBinding.edtCarrierNo.setText(getResources().getString(R.string._58)+"  ");
                mCarrierDilog.dismiss();
            }
        });


        mCarrierDilog.show();
    }

    private void setPageUI() {
        try {
            responsePass = getIntent().getExtras().getString("profile_data");
            System.out.println("Rahul : AccountSettings : setPageUI : responsePass : " + responsePass);
            Gson mGson = new Gson();
            MyAccountModel myAccountModel = mGson.fromJson(responsePass, MyAccountModel.class);
            mActivityAccountSettingsBinding.edtFirstName.setText(myAccountModel.getData().getFirstName());
            mActivityAccountSettingsBinding.edtLastName.setText(myAccountModel.getData().getLastName());
            mActivityAccountSettingsBinding.edtEmailAddress.setText(myAccountModel.getData().getEmail());

            System.out.println("Rahul : AccountSettings : setPageUI : getPhone : " + myAccountModel.getData().getPhone());

            String carrier_code = "", mobile_no = "";
            if(myAccountModel.getData().getPhone()!=null&&!myAccountModel.getData().getPhone().isEmpty()) {
                if (myAccountModel.getData().getPhone().contains("+971")) {

                    carrier_code = myAccountModel.getData().getPhone().replace("+971", "").substring(0, 2);
                    mobile_no = myAccountModel.getData().getPhone().substring(6, myAccountModel.getData().getPhone().length());

                    mActivityAccountSettingsBinding.edtCarrierNo.setText(carrier_code);
                    mActivityAccountSettingsBinding.edtMObileNo.setText(mobile_no);

                } else {
                    mobile_no = myAccountModel.getData().getPhone();
                    mActivityAccountSettingsBinding.edtMObileNo.setText(mobile_no);
                }
            }


            mActivityAccountSettingsBinding.edtGender.setText(myAccountModel.getData().getGender());
            mActivityAccountSettingsBinding.edtLocation.setText(myAccountModel.getData().getLocation());

        }catch (Exception e){e.printStackTrace();}



    }

    public void requestMyProfileUpdate() throws JSONException {
        if(Constants.isInternetConnected(AccountSettings.this)){
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        System.out.println("Rahul : AccountSettings : requestMyProfileUpdate : token : " + mSharedPreferenceManager.getUserProfileDetail("token"));
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("first_name", mActivityAccountSettingsBinding.edtFirstName.getText().toString());
        mJsonObject.put("last_name", mActivityAccountSettingsBinding.edtLastName.getText().toString());
        mJsonObject.put("email",  mActivityAccountSettingsBinding.edtEmailAddress.getText().toString().toLowerCase());
        mJsonObject.put("phone", "+971" +mActivityAccountSettingsBinding.edtCarrierNo.getText().toString().trim() + mActivityAccountSettingsBinding.edtMObileNo.getText().toString());
        mJsonObject.put("gender", mActivityAccountSettingsBinding.edtGender.getText().toString());
        mJsonObject.put("location", mActivityAccountSettingsBinding.edtLocation.getText().toString());

        mActivityAccountSettingsBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        System.out.println("Rahul : AccountSettings : requestMyProfileUpdate : mJsonObject : " + mJsonObject);

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.PUT,
                Constants.BASE_URL + Constants.API_METHODS.MY_PROFILE, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {

                        mActivityAccountSettingsBinding.progressSpinKitView.setVisibility(View.GONE);
                        try {
                            if (response.getString("status").equals(Constants.VARIABLES.STATUS_SUCESS_CODE)) {
                                Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();
                                mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
                                mSharedPreferenceManager.storeUserProfileDetail(mActivityAccountSettingsBinding.edtFirstName.getText().toString() + " " + mActivityAccountSettingsBinding.edtLastName.getText().toString(),
                                        mActivityAccountSettingsBinding.edtEmailAddress.getText().toString(),
                                        mActivityAccountSettingsBinding.edtMObileNo.getText().toString(),
                                        "",
                                        mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_token));
                                finish();

                            } else {
                                Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                        System.out.println("Rahul : AccountSettings : requestMyProfileUpdate : response : " + response);


                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {

                System.out.println("Rahul : AccountSettings : requestMyProfileUpdate : VolleyError : " + error.toString());
            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail("token"));

                return headers;
            }


        };


        // Adding request to request queue
        queue.add(jsonObjReq);
    }else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));}
    }



}
