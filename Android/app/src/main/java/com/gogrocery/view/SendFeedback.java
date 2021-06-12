package com.gogrocery.view;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.databinding.DataBindingUtil;

import android.content.DialogInterface;
import android.os.Build;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivitySendFeedbackBinding;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class SendFeedback extends AppCompatActivity implements View.OnClickListener {
ActivitySendFeedbackBinding sendFeedbackBinding;
    private SharedPreferenceManager mSharedPreferenceManager;
    View rootView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        sendFeedbackBinding= DataBindingUtil.setContentView(this,R.layout.activity_send_feedback);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());

        rootView = this.findViewById(android.R.id.content).getRootView();
        Constants.setupUI(rootView, SendFeedback.this);
        initFields();
        setUpClick();
        textValidCheck();
        hideStatusBarColor();
    }



    private void initFields(){
        String mobile =     mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_mobile);
        String email =    mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_email);
        if (mobile!=null && !mobile.isEmpty()) {
            sendFeedbackBinding.edtPhoneNumber.setText(mobile);
        }
        if (email!=null && !email.isEmpty()) {
            sendFeedbackBinding.edtEmailAddress.setText(email);
        }

    }


    private void setUpClick() {
        sendFeedbackBinding.ivBack.setOnClickListener(this);
        sendFeedbackBinding.btnSendFeedback.setOnClickListener(this);
        sendFeedbackBinding.ivBack.setOnClickListener(v->{
            super.onBackPressed();
        });

        sendFeedbackBinding.btnSendFeedback.setOnClickListener(V->{
            validation();
        });

    }




    private void validation() {
        String name = String.valueOf(sendFeedbackBinding.edtname.getText());
        String mobile = String.valueOf(sendFeedbackBinding.edtPhoneNumber.getText());
        String email = String.valueOf(sendFeedbackBinding.edtEmailAddress.getText());
        String query = String.valueOf(sendFeedbackBinding.tilQuery.getText());

        if ("".equals(name) || name.isEmpty()) {
            sendFeedbackBinding.tilName.setError(getResources().getString(R.string.add_new_address_error_n));

        }else if ("".equals(email)) {
            sendFeedbackBinding.tilEmailAddress.setError(getResources().getString(R.string.error_msg_enter_email));
        } else if ("".equals(mobile)) {
            sendFeedbackBinding.tilPhoneNumber.setError(getResources().getString(R.string.error_msg_enter_mobile_no));
        }
        else if ("".equals(query)) {
            sendFeedbackBinding.tilQuery.setError(getResources().getString(R.string.error_msg_enter_your_query));

        }else if (!Constants.emailPatternValidtion(sendFeedbackBinding.edtEmailAddress.getText().toString())) {
            System.out.println("Rahul : loginValidity : validations 5");
            sendFeedbackBinding.tilEmailAddress.setError(getResources().getString(R.string.login_field_error));
        }else{
            try {
                requestQuerySubmit();
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }

        //requestRegisterNew(name, address, mobile, email, passwo
    }
    @Override
    public void onClick(View view) {

    }

    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }


        public void requestQuerySubmit() throws JSONException {
        sendFeedbackBinding.loading.setVisibility(View.VISIBLE);
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        JSONObject mJsonObject = new JSONObject();
   /*     {
            "name": "sukdev",
                "email": "sukdev.adhikary@navsoft.in",
                "phone": "9647483265",
                "message": "Test"
        }
*/


        mJsonObject.put("name", String.valueOf(sendFeedbackBinding.edtname.getText()));
        mJsonObject.put("email", String.valueOf(sendFeedbackBinding.edtEmailAddress.getText()));
        mJsonObject.put("phone", String.valueOf(sendFeedbackBinding.edtPhoneNumber.getText()));
        mJsonObject.put("message", String.valueOf(sendFeedbackBinding.tilQuery.getText()));

        System.out.println("Rahul : ChangePassword : requestChangePassword : mJsonObject : " + mJsonObject);
        JsonObjectRequest mJsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.CUSTOMER_QUERY, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : ChangePassword : requestChangePassword : response : " + response);
                        sendFeedbackBinding.loading.setVisibility(View.GONE);

                        if (response != null) {
                            try {
                                if (response.getString("status").equals("200")) {
                                    //Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();
                                    successPopup();

                                } else {
                                    Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }

                        } else {

                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                sendFeedbackBinding.loading.setVisibility(View.GONE);
                System.out.println("Rahul : ChangePassword : requestChangePassword : VolleyError : " + error.toString());
                //  Toast.makeText(getApplicationContext(), "Enter Valid Credentials", Toast.LENGTH_LONG).show();
            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
               // headers.put(Constants.VARIABLES.WAREHOUSE_KEY, new SharedPreferenceManager(getApplicationContext()).getWarehouseId());
              //  headers.put("Authorization", "Token " + new SharedPreferenceManager(getApplicationContext()).getUserProfileDetail("token"));
                return headers;
            }


        };


        // Adding request to request queue
        mJsonObjectRequest.setRetryPolicy(new RetryPolicy() {
            @Override
            public int getCurrentTimeout() {
                return 50000;
            }

            @Override
            public int getCurrentRetryCount() {
                return 50000;
            }

            @Override
            public void retry(VolleyError error) throws VolleyError {

            }
        });
        queue.add(mJsonObjectRequest);
    }


    private void successPopup(){
        new AlertDialog.Builder(SendFeedback.this)
                .setTitle(getResources().getString(R.string.success))
                .setMessage(getResources().getString(R.string.query_submitted_successfully))
                .setPositiveButton(getResources().getString(R.string.ok), new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        finish();
                    }
                })

                .show();
    }

    private void textValidCheck(){
        sendFeedbackBinding.edtname.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                if(s.toString().length()>1){}else{
                    String result = s.toString().replaceAll(" ", "");
                    if (!s.toString().equals(result)) {
                        sendFeedbackBinding.edtname.setText(result);
                        sendFeedbackBinding.edtname.setSelection(result.length());
                        // alert the user
                    }
                }
                sendFeedbackBinding.tilName.setError(null);
            }
        });

        sendFeedbackBinding.edtEmailAddress.addTextChangedListener(new TextWatcher() {
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
                    sendFeedbackBinding.edtEmailAddress.setText(result);
                    sendFeedbackBinding.edtEmailAddress.setSelection(result.length());
                    // alert the user
                }
                sendFeedbackBinding.tilEmailAddress.setError(null);
            }
        });

        sendFeedbackBinding.edtPhoneNumber.addTextChangedListener(new TextWatcher() {
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
                    sendFeedbackBinding.edtPhoneNumber.setText(result);
                    sendFeedbackBinding.edtPhoneNumber.setSelection(result.length());
                    // alert the user
                }
                sendFeedbackBinding.tilPhoneNumber.setError(null);
            }
        });


        sendFeedbackBinding.tilQuery.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {

                sendFeedbackBinding.tilQuery.setError(null);
            }
        });
    }

}