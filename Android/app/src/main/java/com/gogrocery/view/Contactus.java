package com.gogrocery.view;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.databinding.DataBindingUtil;

import android.Manifest;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Toast;

import com.afollestad.materialdialogs.DialogAction;
import com.afollestad.materialdialogs.MaterialDialog;
import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.gogrocery.Constants.Constants;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityContactusBinding;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class Contactus extends AppCompatActivity implements View.OnClickListener  {
    ActivityContactusBinding activityContactusBinding;
//   LoadingDialog loadingDialog;
  private boolean loadingFinished = true;
    private boolean redirect = false;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        activityContactusBinding = DataBindingUtil.setContentView(this,R.layout.activity_contactus);
        getWindow().setFeatureInt(Window.FEATURE_PROGRESS,
                Window.PROGRESS_VISIBILITY_ON);
      //  textValidCheck();
        setListners();
        activityContactusBinding.ivBack.setOnClickListener(v->{
            super.onBackPressed();
        });
        hideStatusBarColor();
        //initFields();
    }


    private void setListners() {
        //activityContactusBinding.btnCancel.setOnClickListener(this);
        activityContactusBinding.ivSendfeedBack.setOnClickListener(this);
        activityContactusBinding.ivBack.setOnClickListener(this);
        activityContactusBinding.ivEmail.setOnClickListener(this);
        activityContactusBinding.ivCall.setOnClickListener(this);


    }

   /* public void initFields() {
      //  loadingDialog = new LoadingDialog(this);


*//*

      //  loadingDialog.showDialog();
        WebSettings settings =   activityContactusBinding.webView.getSettings();

        activityContactusBinding.webView.loadUrl(url);
        activityContactusBinding.webView.setWebViewClient(new WebViewClient());
        activityContactusBinding.webView.setInitialScale(1);
        settings.setBuiltInZoomControls(false);
        settings.setUseWideViewPort(true);
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);;
        activityContactusBinding.webView.clearView();
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);

        final Activity MyActivity = this;
        activityContactusBinding.webView.setWebChromeClient(new WebChromeClient()
        {
            public void onProgressChanged(WebView view, int progress)
            {
                MyActivity.setTitle("Loading...");
                MyActivity.setProgress(progress * 100);

                if(progress == 100)
                 //   loadingDialog.hideDialog();
             //   MyActivity.setTitle("JobCard Details");
            }
        });
*//*

        activityContactusBinding.loading.setVisibility(View.VISIBLE);
        String url = "https://www.gogrocery.ae/contact-us";

        WebSettings webSettings = activityContactusBinding.webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setAppCacheEnabled(true);
        webSettings.setDatabaseEnabled(true);
        webSettings.setAllowFileAccessFromFileURLs(true);
        webSettings.setAllowUniversalAccessFromFileURLs(true);
        webSettings.setUseWideViewPort(true);
        webSettings.setLoadWithOverviewMode(true);
        activityContactusBinding.webView.loadUrl(url);


        activityContactusBinding.webView.setWebViewClient(new WebViewClient() {

            @Override
            public boolean shouldOverrideUrlLoading(
                    WebView view, WebResourceRequest request) {
                if (!loadingFinished) {
                    redirect = true;
                }

                loadingFinished = false;
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                    activityContactusBinding.webView.loadUrl(request.getUrl().toString());
                }
                return true;
            }

            @Override
            public void onPageStarted(
                    WebView view, String url, Bitmap favicon) {
                super.onPageStarted(view, url, favicon);
                loadingFinished = false;
                //SHOW LOADING IF IT ISNT ALREADY VISIBLE
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                if(!redirect){
                    loadingFinished = true;
                }

                if(loadingFinished && !redirect){
                    activityContactusBinding.loading.setVisibility(View.GONE);
                    //HIDE LOADING IT HAS FINISHED // HIDE YOUR SPLASH/LOADING VIEW
                } else{
                    redirect = false;
                }
            }
        });

    }*/



/*

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (event.getAction() == KeyEvent.ACTION_DOWN) {
            switch (keyCode) {
                case KeyEvent.KEYCODE_BACK:
                    if ( activityContactusBinding.webView.canGoBack()) {
                        activityContactusBinding.webView.goBack();
                    } else {
                        finish();
                    }
                    return true;
            }

        }
        return super.onKeyDown(keyCode, event);
    }
*/


/*    private void validation() {
        String name = String.valueOf(activityContactusBinding.edtname.getText());
        String mobile = String.valueOf(activityContactusBinding.edtPhoneNumber.getText());
        String email = String.valueOf(activityContactusBinding.edtEmailAddress.getText());
        String query = String.valueOf(activityContactusBinding.editQuery.getText());

        if ("".equals(name) || name.isEmpty()) {
            activityContactusBinding.tilName.setError("Name should not be empty");

        }else if ("".equals(email)) {
            activityContactusBinding.tilEmailAddress.setError("Email Address should not be empty");
        } else if ("".equals(mobile)) {
            activityContactusBinding.tilPhoneNumber.setError("Mobile Number should not be empty");
        }
        else if ("".equals(query)) {
            activityContactusBinding.tilQuery.setError("Enter your Query");

        }else if (!Constants.emailPatternValidtion(activityContactusBinding.edtEmailAddress.getText().toString())) {
            System.out.println("Rahul : loginValidity : validations 5");
            activityContactusBinding.tilEmailAddress.setError(getString(R.string.login_field_error));
        }else{
            try {
                requestQuerySubmit();
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }

            //requestRegisterNew(name, address, mobile, email, passwo
    }*/


/*    private void textValidCheck(){
        activityContactusBinding.edtname.addTextChangedListener(new TextWatcher() {
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
                        activityContactusBinding.edtname.setText(result);
                        activityContactusBinding.edtname.setSelection(result.length());
                        // alert the user
                    }
                }
                activityContactusBinding.tilName.setError(null);
            }
        });

        activityContactusBinding.edtEmailAddress.addTextChangedListener(new TextWatcher() {
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
                    activityContactusBinding.edtEmailAddress.setText(result);
                    activityContactusBinding.edtEmailAddress.setSelection(result.length());
                    // alert the user
                }
                activityContactusBinding.tilEmailAddress.setError(null);
            }
        });

        activityContactusBinding.edtPhoneNumber.addTextChangedListener(new TextWatcher() {
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
                    activityContactusBinding.edtPhoneNumber.setText(result);
                    activityContactusBinding.edtPhoneNumber.setSelection(result.length());
                    // alert the user
                }
                activityContactusBinding.tilPhoneNumber.setError(null);
            }
        });


        activityContactusBinding.editQuery.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {

                activityContactusBinding.tilQuery.setError(null);
            }
        });
    }*/









    private void phoneCall() {
        try {
            if (Build.VERSION.SDK_INT > 22) {
                if (ActivityCompat.checkSelfPermission(Contactus.this, Manifest.permission.CALL_PHONE) != PackageManager.PERMISSION_GRANTED) {
                    ActivityCompat.requestPermissions(Contactus.this, new String[]{Manifest.permission.CALL_PHONE}, 101);
                    return;
                }
                Intent callIntent = new Intent(Intent.ACTION_DIAL);
                callIntent.setData(Uri.parse("tel:" + "+971 600 551685"));
                startActivity(callIntent);
            } else {
                Intent callIntent = new Intent(Intent.ACTION_DIAL);
                callIntent.setData(Uri.parse("tel:" + "+971 600 551685"));
                startActivity(callIntent);
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    private void sendEmail() {
        Intent i = new Intent(Intent.ACTION_SEND);
        i.setType("message/rfc822");
        i.putExtra(Intent.EXTRA_EMAIL, new String[]{"support@gogrocery.ae"});
        i.putExtra(Intent.EXTRA_SUBJECT, "Enter Your Subject.....");
        i.putExtra(Intent.EXTRA_TEXT, "Enter your query......");
        try {
            startActivity(Intent.createChooser(i, "Send mail..."));
        } catch (android.content.ActivityNotFoundException ex) {
            //Toast.makeText(MyActivity.this, "There are no email clients installed.", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public void onClick(View v) {

        switch (v.getId()) {

            case R.id.btnCancel:
               finish();

                break;
            case R.id.iv_call:
                phoneCall();
                break;
            case R.id.iv_email:
                sendEmail();
                break;

            case R.id.iv_sendfeedBack:
                gotoSendFeedback();
                break;
        }

    }

    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }
    private void gotoSendFeedback(){
        Intent i1 = new Intent(this, SendFeedback.class);
        startActivity(i1);
    }
}
