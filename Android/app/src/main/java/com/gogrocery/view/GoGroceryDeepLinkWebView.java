package com.gogrocery.view;

import android.content.Intent;
import androidx.databinding.DataBindingUtil;
import android.net.Uri;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

import com.gogrocery.R;
import com.gogrocery.databinding.ActivityGoGroceryDeepLinkWebViewBinding;

public class GoGroceryDeepLinkWebView extends AppCompatActivity {

    private ActivityGoGroceryDeepLinkWebViewBinding mActivityGoGroceryDeepLinkWebViewBinding;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityGoGroceryDeepLinkWebViewBinding = DataBindingUtil.setContentView(this, R.layout.activity_go_grocery_deep_link_web_view);

        Intent intent = getIntent();
        String action = intent.getAction();
        Uri data = intent.getData();
        System.out.println("Rahul : GoGroceryDeepLinkWebView : data : " + data);
        System.out.println("Rahul : GoGroceryDeepLinkWebView : action : " + action);


        /*mActivityGoGroceryDeepLinkWebViewBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        mActivityGoGroceryDeepLinkWebViewBinding.wvPayment.getSettings().setJavaScriptEnabled(true);
        mActivityGoGroceryDeepLinkWebViewBinding.wvPayment.getSettings().setLoadWithOverviewMode(true);
        mActivityGoGroceryDeepLinkWebViewBinding.wvPayment.getSettings().setUseWideViewPort(true);


        mActivityGoGroceryDeepLinkWebViewBinding.wvPayment.getSettings().setBuiltInZoomControls(false);
        mActivityGoGroceryDeepLinkWebViewBinding.wvPayment.getSettings().setSupportZoom(false);
        mActivityGoGroceryDeepLinkWebViewBinding.wvPayment.getSettings().setAllowFileAccess(true);
        mActivityGoGroceryDeepLinkWebViewBinding.wvPayment.getSettings().setDomStorageEnabled(true);

        mActivityGoGroceryDeepLinkWebViewBinding.wvPayment.setWebViewClient(new WebViewClient() {

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {

                System.out.println("Rahul : GoGroceryDeepLinkWebView : url : " + url);
                view.loadUrl(url);

                return true;
            }

            @Override
            public void onPageFinished(WebView view, final String url) {
                mActivityGoGroceryDeepLinkWebViewBinding.progressSpinKitView.setVisibility(View.GONE);
                mActivityGoGroceryDeepLinkWebViewBinding.wvPayment.setVisibility(View.VISIBLE);
            }

        });

        mActivityGoGroceryDeepLinkWebViewBinding.wvPayment.loadUrl("https://www.gogrocery.ae/approved-order/place-order/OTUzMTA0Nzk1Mw%3D%3D");

    }*/
    }
}
