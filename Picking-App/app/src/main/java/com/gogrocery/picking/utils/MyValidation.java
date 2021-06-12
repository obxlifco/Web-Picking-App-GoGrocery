package com.gogrocery.picking.utils;

import android.content.Context;
import android.text.TextUtils;
import android.util.Patterns;
import android.widget.Toast;

import com.gogrocery.picking.R;


public class MyValidation {

    Context context;

    public MyValidation(Context context) {
        this.context = context;
    }

    public boolean validateLogin(String userName,String pwd) {
        Boolean is_error = false;
        if (userName.toString().trim().length() == 0) {
            is_error = true;
            Toast.makeText(context,context.getResources().getString(R.string.txtEmailOrUserName)+" "+
                    context.getResources().getString(R.string.txtCantEmpty), Toast.LENGTH_SHORT).show();
        }/*else if(!isValidEmail(userName)){
            is_error = true;
            Toast.makeText(context,context.getResources().getString(R.string.txtEmailOrUserName)+" "+
                    context.getResources().getString(R.string.txtNotValid),Toast.LENGTH_SHORT).show();
        }*/else if (pwd.toString().trim().length() == 0) {
            is_error = true;
            Toast.makeText(context,context.getResources().getString(R.string.txtPassword)+" "+
                    context.getResources().getString(R.string.txtCantEmpty), Toast.LENGTH_SHORT).show();
        }
        if (!is_error) {
            return true;
        } else {
            return false;
        }
    }

    public boolean validateForgotPwd(String userName) {
        Boolean is_error = false;
        if (userName.toString().trim().length() == 0) {
            is_error = true;
            Toast.makeText(context,context.getResources().getString(R.string.txtEmailOrUserName)+" "+
                    context.getResources().getString(R.string.txtCantEmpty), Toast.LENGTH_SHORT).show();
        }else if(!isValidEmail(userName)){
            is_error = true;
            Toast.makeText(context,context.getResources().getString(R.string.txtEmailOrUserName)+" "+
                    context.getResources().getString(R.string.txtNotValid),Toast.LENGTH_SHORT).show();
        }
        if (!is_error) {
            return true;
        } else {
            return false;
        }
    }

    public boolean validateResetPwd(String otp,String pwd,String confirmPwd) {
        Boolean is_error = false;
        if (otp.toString().trim().length() == 0) {
            is_error = true;
            Toast.makeText(context,context.getResources().getString(R.string.txtOTP)+" "+
                    context.getResources().getString(R.string.txtCantEmpty), Toast.LENGTH_SHORT).show();
        }else if(pwd.length()<6){
            is_error = true;
            Toast.makeText(context,context.getResources().getString(R.string.txtPassword)+" "+
                    context.getResources().getString(R.string.txtPwdLengthError),Toast.LENGTH_SHORT).show();
        }
        else if(!pwd.equalsIgnoreCase(confirmPwd)){
            is_error = true;
            Toast.makeText(context,context.getResources().getString(R.string.txtPassword)+" "+
                            context.getResources().getString(R.string.txtAnd)+" "+
                            context.getResources().getString(R.string.txtConfirmPassword)+" "+
                    context.getResources().getString(R.string.txtNotMatched),Toast.LENGTH_SHORT).show();
        }
        if (!is_error) {
            return true;
        } else {
            return false;
        }
    }

    Boolean isValidEmail(CharSequence target) {
        if (TextUtils.isEmpty(target)) {
            return false;
        } else {
            return (!TextUtils.isEmpty(target) && Patterns.EMAIL_ADDRESS.matcher(target).matches());
        }
    }
}
