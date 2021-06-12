package com.gogrocery.view;

import android.content.Intent;
import androidx.databinding.DataBindingUtil;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
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
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityReviewProductPageBinding;
import com.willy.ratingbar.BaseRatingBar;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class ReviewProductPage extends AppCompatActivity {

    private ActivityReviewProductPageBinding mActivityReviewProductPageBinding;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityReviewProductPageBinding = DataBindingUtil.setContentView(this, R.layout.activity_review_product_page);
        int product_id = 0;
        try {


            if (getIntent() != null) {
                if (getIntent().getExtras() != null) {

                    if (getIntent().getExtras().getString("product_id") != null) {
                        product_id = Integer.parseInt(getIntent().getExtras().getString("product_id"));


                    }
                }
            }


            mActivityReviewProductPageBinding.ivBack.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    finish();
                }
            });

            mActivityReviewProductPageBinding.btnCancel.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    finish();
                }
            });


            int finalProduct_id = product_id;
            mActivityReviewProductPageBinding.btnSubmit.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (mActivityReviewProductPageBinding.edtReviewTitle.getText().toString().isEmpty()) {
                        mActivityReviewProductPageBinding.edtReviewTitle.setError("Review title is empty");
                    } else if (mActivityReviewProductPageBinding.edtReviewDescription.getText().toString().isEmpty()) {
                        mActivityReviewProductPageBinding.edtReviewDescription.setError("Review description is empty");

                    } else if (mActivityReviewProductPageBinding.simpleRatingBar.getRating() == 0.0) {
                        Toast.makeText(getApplicationContext(), "Rating cannot be zero!", Toast.LENGTH_LONG).show();

                    } else {
                        try {
                            requestProductReview(finalProduct_id, mActivityReviewProductPageBinding.edtReviewTitle.getText().toString(),
                                    mActivityReviewProductPageBinding.edtReviewDescription.getText().toString(), mActivityReviewProductPageBinding.simpleRatingBar.getRating());
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }
            });
        } catch (Exception e) {
        }

        mActivityReviewProductPageBinding.simpleRatingBar.setOnRatingChangeListener(new BaseRatingBar.OnRatingChangeListener() {
            @Override
            public void onRatingChange(BaseRatingBar ratingBar, float rating, boolean fromUser) {
                System.out.println("Rahul : ReviewProductPage : rating : " + rating);
                System.out.println("Rahul : ReviewProductPage : ratingBar : " + ratingBar.getRating());
                System.out.println("Rahul : ReviewProductPage : fromUser : " + fromUser);
                if(rating==1.0)
                {
                    mActivityReviewProductPageBinding.tvRatingExpression.setVisibility(View.VISIBLE);
                    mActivityReviewProductPageBinding.tvRatingExpression.setText("Worst");
                    mActivityReviewProductPageBinding.tvRatingExpression.setTextColor(getResources().getColor(R.color.worst));
                }else if(rating==2.0)
                {
                    mActivityReviewProductPageBinding.tvRatingExpression.setVisibility(View.VISIBLE);
                    mActivityReviewProductPageBinding.tvRatingExpression.setText("Average");
                    mActivityReviewProductPageBinding.tvRatingExpression.setTextColor(getResources().getColor(R.color.average));
                }
                else if(rating==3.0)
                {  mActivityReviewProductPageBinding.tvRatingExpression.setVisibility(View.VISIBLE);
                    mActivityReviewProductPageBinding.tvRatingExpression.setText("Good");
                    mActivityReviewProductPageBinding.tvRatingExpression.setTextColor(getResources().getColor(R.color.good));
                }
                else if(rating==4.0)
                {  mActivityReviewProductPageBinding.tvRatingExpression.setVisibility(View.VISIBLE);
                    mActivityReviewProductPageBinding.tvRatingExpression.setText("Good");
                    mActivityReviewProductPageBinding.tvRatingExpression.setTextColor(getResources().getColor(R.color.good));
                }
                else if(rating==5.0)
                {  mActivityReviewProductPageBinding.tvRatingExpression.setVisibility(View.VISIBLE);
                    mActivityReviewProductPageBinding.tvRatingExpression.setText("Very Good");
                    mActivityReviewProductPageBinding.tvRatingExpression.setTextColor(getResources().getColor(R.color.good));
                }else{
                    mActivityReviewProductPageBinding.tvRatingExpression.setVisibility(View.GONE);
                    mActivityReviewProductPageBinding.tvRatingExpression.setText("");
                }
            }
        });
    }

    public void requestProductReview(int argProductID, String argReviewTitle, String argReviewMessage, float argReviewStar) throws JSONException {
        mActivityReviewProductPageBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("product_id", argProductID);
        mJsonObject.put("review_title", argReviewTitle);
        mJsonObject.put("review_message", argReviewMessage);
        mJsonObject.put("review_star",argReviewStar);

        System.out.println("Rahul : ReviewProductPage : requestProductReview : " + mJsonObject);
        JsonObjectRequest mJsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.PRODUCT_REVIEW, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            System.out.println("Rahul : ReviewProductPage : requestProductReview : response: " + response);
                            mActivityReviewProductPageBinding.progressSpinKitView.setVisibility(View.GONE);
                            if (response.getString("status").equals("1"))
                            {
                                Toast.makeText(getApplicationContext(),response.getString("msg"),Toast.LENGTH_SHORT).show();
                                Intent intent = new Intent();
                                intent.putExtra("review_done_or_not", "yes");
                                setResult(1, intent);

                            }
                        }catch (Exception e)
                        {

                        }

                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mActivityReviewProductPageBinding.progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : ReviewProductPage : requestProductReview : VolleyError : " + error.toString());
                Toast.makeText(getApplicationContext(), R.string.error_try_again_later, Toast.LENGTH_LONG).show();
            }
        })

        {

            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("Authorization", "Token " + mSharedPreferenceManager.getUserProfileDetail(mSharedPreferenceManager.key_token));
                headers.put("WAREHOUSE", mSharedPreferenceManager.getWarehouseId());
                return headers;
            }


        };


        // Adding request to request queue
        queue.add(mJsonObjectRequest);
    }

}
