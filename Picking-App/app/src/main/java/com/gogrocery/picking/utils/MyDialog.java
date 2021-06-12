package com.gogrocery.picking.utils;

import android.app.ProgressDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.graphics.Color;
import android.graphics.PorterDuff;
import android.graphics.drawable.Drawable;
import android.text.InputType;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;


import com.gogrocery.picking.R;

import androidx.appcompat.app.AlertDialog;
import androidx.core.content.ContextCompat;

/**
 * Created by Pratim on 6/12/17.
 */

public class MyDialog {

    static ProgressDialog progressDoalog;
    static LayoutInflater layoutInflater;

    public static void showOkCancelPopup(String message, String positive, String negative, Context ctx,
                                         final OkCancelPopupCallback obj) {
        AlertDialog.Builder alertDialog = new AlertDialog.Builder(ctx);
        alertDialog.setMessage(message);
        alertDialog.setCancelable(false);

        alertDialog.setPositiveButton(positive,
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                        obj.onPositiveClick();

                    }
                });

        alertDialog.setNegativeButton(negative,
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                });

        AlertDialog alert = alertDialog.create();
        alert.show();
        alert.getWindow().getAttributes();

        TextView textView = (TextView) alert.findViewById(android.R.id.message);
        textView.setTextSize(18);
        alert.getButton(AlertDialog.BUTTON_NEGATIVE).setTextColor(Color.parseColor("#696969"));
        /*AlertDialog alert=alertDialog.create();
        TextView msgTxt = (TextView) alert.findViewById(android.R.id.message);
        msgTxt.setTextSize(TypedValue.COMPLEX_UNIT_PX, ctx.getResources().getDimension(R.dimen._50sdp));*/


    }

    public static void showOkPopupCallBack(String message, String positive, Context ctx,
                                           final OkCancelPopupCallback obj) {
        AlertDialog.Builder alertDialog = new AlertDialog.Builder(ctx);
        alertDialog.setMessage(message);
        alertDialog.setCancelable(false);

        alertDialog.setPositiveButton(positive,
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                        obj.onPositiveClick();

                    }
                });
        alertDialog.show();
        //alertDialog.get(AlertDialog.BUTTON_POSITIVE).setTextColor(Color.parseColor("#00b5f1"));
        /*AlertDialog alert=alertDialog.create();
        TextView msgTxt = (TextView) alert.findViewById(android.R.id.message);
        msgTxt.setTextSize(TypedValue.COMPLEX_UNIT_PX, ctx.getResources().getDimension(R.dimen._50sdp));*/


    }

    public static void showCustomEditTextOkCancelPopup(final Context ctx, final String msg, String hint, String defText,
                                                       final CustomEditTextOkCancelPopupCallback obj) {

        layoutInflater = LayoutInflater.from(ctx);
        final View view = layoutInflater.inflate(R.layout.dialog_edit_text, null);
        final AlertDialog alertDialog = new AlertDialog.Builder(ctx).create();
        alertDialog.setTitle(msg);
        alertDialog.setCancelable(false);


        final EditText etDialogMailID = (EditText) view.findViewById(R.id.etDialogMailID);
        final LinearLayout llMainDialog = (LinearLayout) view.findViewById(R.id.llMainDialog);
        etDialogMailID.setHint(hint);
        if (defText.length() > 0) {
            etDialogMailID.setText(defText);
        }
        if (ctx.getResources().getString(R.string.txtEmail).equalsIgnoreCase(hint)) {
            etDialogMailID.setInputType(InputType.TYPE_CLASS_TEXT);
        } else {
            etDialogMailID.setInputType(InputType.TYPE_CLASS_NUMBER);
        }

        alertDialog.setButton(AlertDialog.BUTTON_POSITIVE, "OK", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {

            }
        });

        alertDialog.setButton(AlertDialog.BUTTON_NEGATIVE, "Cancel", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {

            }
        });

        alertDialog.setOnShowListener(new DialogInterface.OnShowListener() {
            @Override
            public void onShow(DialogInterface arg0) {
                alertDialog.getButton(AlertDialog.BUTTON_NEGATIVE).setTextColor(ctx.getResources().getColor(R.color.appColorDarkGrey));
            }
        });
        alertDialog.setView(view);
        alertDialog.show();

        alertDialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //AppUtilities.hideSoftKeyboard(ctx);
                if (etDialogMailID.getText().toString().trim().length() > 0) {
                    obj.onDoneClick(etDialogMailID.getText().toString(), alertDialog);
                }
            }
        });

        alertDialog.getButton(AlertDialog.BUTTON_NEGATIVE).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                obj.onCancelClick(alertDialog);
            }
        });


    }

    /*public static void showErrorPopup(final Context ctx, String msg, String btnText) {
        AlertDialog.Builder builder = new AlertDialog.Builder(ctx);
        builder.setMessage(msg)
                .setCancelable(false)
                .setPositiveButton(btnText, new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        //do things
                        dialog.dismiss();
                    }
                });
        AlertDialog alert = builder.create();
        alert.show();
        final Dialog dialog = new Dialog(ctx);
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialog.setCancelable(true);
        dialog.setContentView(R.layout.dialog_error);

        final RelativeLayout rl_parent = (RelativeLayout) dialog.findViewById(R.id.rl_parent);
        final TextView tvEnterAccount = (TextView) dialog.findViewById(R.id.tvError);
        //initial EditText value
        tvEnterAccount.setText(msg);
        tvEnterAccount.setTextColor(Color.BLACK);
        Button btn_done = (Button) dialog.findViewById(R.id.btnError);
        btn_done.setText(btnText);
        btn_done.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                dialog.dismiss();

            }
        });

        dialog.show();
        Window window = dialog.getWindow();
        window.setLayout(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
    }*/

    public static void defaultShowErrorPopup(final Context ctx, String msg, String btnText) {
        AlertDialog.Builder builder = new AlertDialog.Builder(ctx);
        builder.setTitle("Error..");
        builder.setMessage(msg)
                .setCancelable(false)
                .setPositiveButton(btnText, new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        //do things
                        dialog.dismiss();
                    }
                });
        AlertDialog alert = builder.create();
        alert.show();
        alert.getButton(AlertDialog.BUTTON_POSITIVE).setTextColor(Color.parseColor("#00b5f1"));
    }

    public static void defaultShowInfoPopup(final Context ctx,String title, String msg, String btnText) {
        AlertDialog.Builder builder = new AlertDialog.Builder(ctx);
        builder.setTitle(title);
        builder.setMessage(msg)
                .setCancelable(false)
                .setPositiveButton(btnText, new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        //do things
                        dialog.dismiss();
                    }
                });
        AlertDialog alert = builder.create();
        alert.show();
        alert.getButton(AlertDialog.BUTTON_POSITIVE).setTextColor(Color.parseColor("#00b5f1"));
    }

    public static void showProgressLoader(final Context ctx, String msg) {
        //progressDoalog = new ProgressDialog(ctx, R.style.MyProgressDialogTheme);
        progressDoalog = new ProgressDialog(ctx);
        progressDoalog.setMessage(msg);
        progressDoalog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        Drawable drawable = new ProgressBar(ctx).getIndeterminateDrawable().mutate();
        drawable.setColorFilter(ContextCompat.getColor(ctx, R.color.colorPrimary),
                PorterDuff.Mode.SRC_IN);
        //progressDoalog.setIndeterminateDrawable(drawable);
        //progressDoalog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
        progressDoalog.show();
    }

    public static void dismissProgressLoader() {
        if (progressDoalog != null && progressDoalog.isShowing()) {
            progressDoalog.dismiss();
        }
    }

    public interface OkCancelPopupCallback {
        void onPositiveClick();

        void onNegativeClick();
    }

    public interface CustomEditTextOkCancelPopupCallback {
        void onDoneClick(String val, AlertDialog alertDialog);

        void onCancelClick(AlertDialog alertDialog);
    }
}
