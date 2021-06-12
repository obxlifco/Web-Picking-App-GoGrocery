package com.gogrocery.helper;

import android.app.Activity;
import android.app.Dialog;
import android.content.Context;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.Drawable;
import android.view.Gravity;
import android.view.View;
import android.view.Window;

import com.gogrocery.R;

public class LoadingDialog{

    private Context context;
    private Activity activity;
    Dialog dialog;

    View parentView;

    private Drawable drawableImage;
    private String messageString = "";
    public LoadingDialog(Context context) {
        this.context = context;
        dialog = new Dialog(this.context);
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);

        dialog.setContentView(R.layout.layout_loading_dialog);
        Window window = dialog.getWindow();
        window.setGravity(Gravity.CENTER);
        dialog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
        dialog.setCancelable(false);
        // Inflate the layout for this fragment

    }



//    private void initFields(){
//
//        Sprite doubleBounce = new FadingCircle();
//        doubleBounce.setColor(ColorModel.parseColor("#008577"));
//        loading.setIndeterminateDrawable(doubleBounce);
//
//
//    }


    public void showDialog() {

        dialog.show();
    }

    public void hideDialog() {
        dialog.dismiss();
    }

}
