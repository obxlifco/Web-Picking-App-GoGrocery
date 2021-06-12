package com.gogrocery.view;

import androidx.appcompat.app.AppCompatActivity;
import androidx.databinding.DataBindingUtil;

import android.os.Build;
import android.os.Bundle;
import android.text.Html;
import android.util.Log;
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
import com.gogrocery.Models.MenuCmsModel.InnerCMSModel;
import com.gogrocery.Models.MenuCmsModel.MenuCmsModel;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityQualityStandardsBinding;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class QualityStandards extends AppCompatActivity implements View.OnClickListener{
ActivityQualityStandardsBinding qualityStandardsBinding;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        qualityStandardsBinding= DataBindingUtil.setContentView(this,R.layout.activity_quality_standards);
        initFields();
        setUpClick();
        hideStatusBarColor();
    }


    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }

    private void initFields(){
        try {
            requestCmsMenu("quality-standards");
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }


    private void setUpClick() {
        qualityStandardsBinding.ivBack.setOnClickListener(this);
        qualityStandardsBinding.ivBack.setOnClickListener(v->{
            super.onBackPressed();
        });

    }
    @Override
    public void onClick(View view) {

    }

    public void requestCmsMenu(String urlRequest) throws JSONException {
        qualityStandardsBinding.loading.setVisibility(View.VISIBLE);
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        JSONObject mJsonObject = new JSONObject();
   /*     {
{
  "url": "terms-conditions",
  "template_id": 1,
  "company_website_id": 1
}
        */


        mJsonObject.put("url",urlRequest);
        mJsonObject.put("template_id",1);
        mJsonObject.put("company_website_id", 1);


        System.out.println("Rahul : ChangePassword : requestChangePassword : mJsonObject : " + mJsonObject);
        JsonObjectRequest mJsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.PAGE_URL_TO_ID, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : ChangePassword : requestChangePassword : response : " + response);
                        qualityStandardsBinding.loading.setVisibility(View.GONE);

                        if (response != null) {
                            try {
                                Gson mGson = new Gson();
                                JSONObject mJsonObject = response;
                                MenuCmsModel menuCmsModel = mGson.fromJson(mJsonObject.toString(), MenuCmsModel.class);

                                if (menuCmsModel.getStatus().equals(1)) {

                                    String json = menuCmsModel.getCmsWidgets().get(0).getPropertyValue();

                                    try {

                                        JSONObject obj = new JSONObject(json);

                                        InnerCMSModel innerCMSModel = mGson.fromJson(obj.toString(), InnerCMSModel.class);

                                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
                                            qualityStandardsBinding.tvText.setText(Html.fromHtml(innerCMSModel.getInsertables().get(0).getProperties().get(0).getValue(), Html.FROM_HTML_MODE_COMPACT));

                                        } else {
                                            qualityStandardsBinding.tvText.setText(Html.fromHtml(innerCMSModel.getInsertables().get(0).getProperties().get(0).getValue()));
                                        }

                                        //  qualityStandardsBinding.tvText.setText(innerCMSModel.getInsertables().get(0).getProperties().get(0).getValue());


                                        Log.e("Menu CMS", obj.toString());

                                    } catch (Throwable t) {
                                        Log.e("My App", "Could not parse malformed JSON: \"" + json + "\"");
                                    }


                                    //Toast.makeText(getApplicationContext(), response.getString("message"), Toast.LENGTH_LONG).show();
                                    // successPopup();

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
                qualityStandardsBinding.loading.setVisibility(View.GONE);
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
                headers.put("Authorization", "Token " + new SharedPreferenceManager(getApplicationContext()).getUserProfileDetail("token"));
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
}