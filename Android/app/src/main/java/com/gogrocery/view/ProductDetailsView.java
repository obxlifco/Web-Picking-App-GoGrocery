package com.gogrocery.view;

import androidx.appcompat.app.AppCompatActivity;
import androidx.databinding.DataBindingUtil;

import android.os.Build;
import android.os.Bundle;
import android.text.Html;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;

import com.gogrocery.R;
import com.gogrocery.databinding.ActivityProductDetailsViewBinding;

public class ProductDetailsView extends AppCompatActivity {
ActivityProductDetailsViewBinding productDetailsViewBinding;
    View rootView;
    String productName = "";
    String productDescription = "";
    @Override
    public void onResume() {
        super.onResume();
        Window window = this.getWindow();
        int width = getResources().getDimensionPixelSize(R.dimen.width_dialogFragment_chat);
        int height = getResources().getDimensionPixelSize(R.dimen.height_dialogFragment_chat);
        window.setLayout(width, ViewGroup.LayoutParams.WRAP_CONTENT);
        window.setBackgroundDrawable(getResources().getDrawable(R.drawable.bg_dialog_fragment));

    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        productDetailsViewBinding= DataBindingUtil.setContentView(this,R.layout.activity_product_details_view);
        this.setFinishOnTouchOutside(true);
        rootView = this.findViewById(android.R.id.content).getRootView();
        productName = getIntent().getStringExtra("product_name");
        productDescription = getIntent().getStringExtra("product_description");
       /* productDescription = "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of \"de Finibus Bonorum et Malorum\" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, \"Lorem ipsum dolor sit amet..\", comes from a line in section 1.10.32.\n" +
                "\n" +
                "The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from \"de Finibus Bonorum et Malorum\" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham\n" +
                "\n" +
                "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.";*/
        if(productName!=null&&!productName.isEmpty()) {
            productDetailsViewBinding.tvItemName.setText(productName);
        }
        if(productDescription!=null&&!productDescription.isEmpty()) {

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
                productDetailsViewBinding.tvProductDescription.setText(Html.fromHtml(productDescription, Html.FROM_HTML_MODE_COMPACT));

            } else {
                productDetailsViewBinding.tvProductDescription.setText(Html.fromHtml(productDescription));
            }


        }
        productDetailsViewBinding.ivBtnClose.setOnClickListener(v->{
            finish();
        });

        productDetailsViewBinding.txtOk.setOnClickListener(v->{
            finish();
        });
    }
}