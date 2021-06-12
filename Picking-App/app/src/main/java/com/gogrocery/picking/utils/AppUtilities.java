package com.gogrocery.picking.utils;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.ActivityManager;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.drawable.Drawable;
import android.location.Address;
import android.location.Geocoder;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.Uri;
import android.os.Build;
import android.os.IBinder;
import android.provider.OpenableColumns;
import android.telephony.TelephonyManager;
import android.text.Editable;
import android.text.Html;
import android.text.TextUtils;
import android.util.Base64;
import android.util.Log;
import android.util.Patterns;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;

import com.google.android.material.snackbar.Snackbar;
import com.gogrocery.picking.GoGroceryPicking;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.text.DateFormat;
import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Locale;
import java.util.TimeZone;
import java.util.regex.Matcher;

import androidx.annotation.RequiresApi;


public class AppUtilities {
    private static AppUtilities comminInstance = null;
    private Context mContext;
    private static Context context = null;
    private static DecimalFormatSymbols symbolsEN_US;
    private static DecimalFormat df;

    /**
     * Recently set context will be returned.
     * If not set it from current class it will
     * be null.
     *
     * @return Context
     */
    public static final Context getContext() {
        return AppUtilities.context;
    }

    /**
     * First set context from every activity
     * before use any static method of AppUtils class.
     *
     * @param ctx
     */
    public static final void setContext(Context ctx) {
        AppUtilities.context = ctx;
    }

    private AppUtilities() {
    }

    public static AppUtilities getInstance(Context mContext) {
        if (comminInstance == null) {
            comminInstance = new AppUtilities();
        }
        comminInstance.mContext = mContext;
        return comminInstance;
    }

    /**
     * Validate Email
     *
     * @param target
     * @return
     */
    public final static boolean isValidEmail(CharSequence target) {
        if (TextUtils.isEmpty(target)) {
            return false;
        } else {
            return Patterns.EMAIL_ADDRESS.matcher(target).matches();
        }
    }

    public static void showSnackBar(View parentLayout, String messege, int length) {

        Snackbar snackbar = Snackbar.make(parentLayout, messege, length);
/*                    View snackBarView = snackbar.getView();
                    snackBarView.setBackgroundColor(ContextCompat.getColor(this, R.color.colorPrimary));*/

        snackbar.show();
    }

    public static String getColorHexValueAsString(Context context, int color) {
        return String.format("#%06X", (0xFFFFFF & context.getResources().getColor(color)));
    }

    /**
     * Format Date
     *
     * @param date
     * @return
     */
    public static String getFormattedDate(String s) {
        Date date = null;
        try {
            date = new SimpleDateFormat("MM-dd-yyyy", Locale.ENGLISH).parse(s);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        //2nd of march 2015
        int day = cal.get(Calendar.DATE);

        if (!((day > 10) && (day < 19)))
            switch (day % 10) {
                case 1:
                    return new SimpleDateFormat("d'st' MMM , yyyy").format(date);
                case 2:
                    return new SimpleDateFormat("d'nd' MMM , yyyy").format(date);
                case 3:
                    return new SimpleDateFormat("d'rd' MMM , yyyy").format(date);
                default:
                    return new SimpleDateFormat("d'th' MMM , yyyy").format(date);
            }
        return new SimpleDateFormat("d'th' MMM , yyyy").format(date);
    }

    public static String getFormattedDateYYYY(String s) {
        Date date = null;
        try {
            date = new SimpleDateFormat("yyyy-dd-MM").parse(s);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        //2nd of march 2015
        int day = cal.get(Calendar.DATE);

        if (!((day > 10) && (day < 19)))
            switch (day % 10) {
                case 1:
                    return new SimpleDateFormat("d'st' MMM , yyyy").format(date);
                case 2:
                    return new SimpleDateFormat("d'nd' MMM , yyyy").format(date);
                case 3:
                    return new SimpleDateFormat("d'rd' MMM , yyyy").format(date);
                default:
                    return new SimpleDateFormat("d'th' MMM , yyyy").format(date);
            }
        return new SimpleDateFormat("d'th' MMM , yyyy").format(date);
    }

    public static String formatDate (String date, String initDateFormat, String endDateFormat) throws ParseException {

        Date initDate = new SimpleDateFormat(initDateFormat).parse(date);
        SimpleDateFormat formatter = new SimpleDateFormat(endDateFormat);
        String parsedDate = formatter.format(initDate);

        return parsedDate;
    }

    public static String getFormattedDateGraph(String date) {
        Date d = null;
        try {
            d = new SimpleDateFormat("yyyy-MM-dd", Locale.ENGLISH).parse(date);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        Calendar cal = Calendar.getInstance();
        cal.setTime(d);
        //2nd of march 2015
        int day = cal.get(Calendar.DATE);

        if (!((day > 10) && (day < 19)))
            switch (day % 10) {
                case 1:
                    return new SimpleDateFormat("d'st' MMM ").format(d);
                case 2:
                    return new SimpleDateFormat("d'nd' MMM ").format(d);
                case 3:
                    return new SimpleDateFormat("d'rd' MMM ").format(d);
                default:
                    return new SimpleDateFormat("d'th' MMM ").format(d);
            }
        return new SimpleDateFormat("d'th' MMM ").format(d);
    }

    public static String getFormattedDateConversation(String date) throws ParseException {
        Date d = new SimpleDateFormat("yyyy-MM-dd", Locale.ENGLISH).parse(date);
        Calendar cal = Calendar.getInstance();
        cal.setTime(d);
        String monthFormatDate = new SimpleDateFormat("MMMM yyyy").format(cal.getTime());
        return monthFormatDate;
    }

    public static String getMonthFormatDate(String date) throws ParseException {
        Date d = new SimpleDateFormat("yyyy-MM-dd", Locale.ENGLISH).parse(date);
        Calendar cal = Calendar.getInstance();
        cal.setTime(d);
        String monthFormatDate = new SimpleDateFormat("MM-dd-yyyy").format(cal.getTime());
        return monthFormatDate;
    }

    public static String getMonthFormatDateTime(String date) throws ParseException {
        Date d = new SimpleDateFormat("MM-dd-yyyy", Locale.ENGLISH).parse(date);
        Calendar cal = Calendar.getInstance();
        cal.setTime(d);
        String monthFormatDate = new SimpleDateFormat("EEEE MMM dd, yyyy").format(cal.getTime());
        return monthFormatDate;
    }

    public static String withNumberSuffix(long count) {
        if (count < 1000) return "" + count;
        int exp = (int) (Math.log(count) / Math.log(1000));
        return String.format("%.1f %c",
                count / Math.pow(1000, exp),
                "kMGTPE".charAt(exp - 1));
    }

    /**
     * Check Online Status
     *
     * @return
     */
    public static boolean isOnline(Context mContext) {
        ConnectivityManager cm = (ConnectivityManager) mContext.getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo netInfo = cm.getActiveNetworkInfo();
        /*if(netInfo != null && netInfo.isConnectedOrConnecting()){
            try {
                return isConnected();
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }*/
        return netInfo != null && netInfo.isConnectedOrConnecting();
    }

    public static boolean isConnected() throws InterruptedException, IOException {
        final String command = "ping -c 1 google.com";
        return Runtime.getRuntime().exec(command).waitFor() == 0;
    }

    public static String CapsFirst(String str) {
        String[] words = str.split(" ");
        StringBuilder ret = new StringBuilder();
        for (int i = 0; i < words.length; i++) {
            ret.append(Character.toUpperCase(words[i].charAt(0)));
            ret.append(words[i].substring(1));
            if (i < words.length - 1) {
                ret.append(' ');
            }
        }
        return ret.toString();
    }

    public static void hideKeyboard(View currentFocusView) {
        if (currentFocusView != null) {
            IBinder windowToken = currentFocusView.getWindowToken();
            if (windowToken != null) {
                InputMethodManager inputMethodManager = (InputMethodManager) currentFocusView.getContext().getApplicationContext().getSystemService(Context.INPUT_METHOD_SERVICE);
                inputMethodManager.hideSoftInputFromWindow(windowToken, 0);
            }
        }
    }

    public static void hideSoftKeyboard(Activity activity) {
        InputMethodManager inputManager = (InputMethodManager) activity
                .getSystemService(Context.INPUT_METHOD_SERVICE);

        // check if no view has focus:
        View currentFocusedView = activity.getCurrentFocus();
        if (currentFocusedView != null) {
            inputManager.hideSoftInputFromWindow(currentFocusedView.getWindowToken(), InputMethodManager.HIDE_NOT_ALWAYS);
        }
    }

    public static void hideKeyboardFragment(Context context, View view) {
        InputMethodManager imm = (InputMethodManager) context.getSystemService(Activity.INPUT_METHOD_SERVICE);
        imm.hideSoftInputFromWindow(view.getWindowToken(), 0);
    }

    public static void hideSoftKeyboard(View view, Context context) {
        InputMethodManager imm = (InputMethodManager) context.getSystemService(Context.INPUT_METHOD_SERVICE);
        imm.hideSoftInputFromWindow(view.getWindowToken(), 0);
    }

    public static String getAddress(Context mContext, double latitude, double longitude) {
        String full_add = null;
        Geocoder geocoder = new Geocoder(mContext, Locale.getDefault());
        List<Address> addresses = null;
        try {
            addresses = geocoder.getFromLocation(latitude, longitude, 1);
            if (addresses.size() > 0) {
                String cityName = addresses.get(0).getAddressLine(0);
                String stateName = addresses.get(0).getAddressLine(1);
                String countryName = addresses.get(0).getAddressLine(2);
                String postalCode = addresses.get(0).getPostalCode();

                full_add = cityName + "," + stateName + "," + postalCode;
            }
            return full_add;
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }


    public static boolean checkAllCon(Activity activity) {

        ConnectivityManager mConnectivity = (ConnectivityManager) activity.getSystemService(Context.CONNECTIVITY_SERVICE);
        TelephonyManager mTelephony = (TelephonyManager) activity.getSystemService(Context.TELEPHONY_SERVICE);
        // Skip if no connection, or background data disabled
        NetworkInfo info = mConnectivity.getActiveNetworkInfo();
        if (info == null || !mConnectivity.getBackgroundDataSetting()) {
            return false;
        }

        // Only update if WiFi or 3G is connected and not roaming
        int netType = info.getType();
        int netSubtype = info.getSubtype();

        if (netType == ConnectivityManager.TYPE_WIFI || netType == ConnectivityManager.TYPE_MOBILE) {
            return info.isConnected();
        } else if (netType == ConnectivityManager.TYPE_MOBILE && netSubtype == TelephonyManager.NETWORK_TYPE_UMTS && !mTelephony.isNetworkRoaming()) {
            return info.isConnected();
        } else {
            return false;
        }
    }

    public static String encodeBase64(String str) {
        byte[] data = new byte[0];
        try {
            data = str.getBytes("UTF-8");
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        String base64 = Base64.encodeToString(data, Base64.DEFAULT);
        return base64;
    }

    public static Bitmap getBitmapFromBase64(String str) {
        byte[] imageBytes = Base64.decode(str, Base64.DEFAULT);
        Bitmap decodedImage = BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.length);
        decodedImage= Bitmap.createScaledBitmap(decodedImage, 300, 150, false);
        decodedImage.compress(Bitmap.CompressFormat.PNG, 100, new ByteArrayOutputStream());
        return decodedImage;}

    public static String[] extractLinks(String text) {
        List<String> links = new ArrayList<String>();
        Matcher m = Patterns.WEB_URL.matcher(text);
        while (m.find()) {
            String url = m.group();
            Log.d("TAG", "URL extracted: " + url);
            links.add(url);
        }

        return links.toArray(new String[links.size()]);
    }

    public static String getFileName(Context context, Uri uri) {
        String result = null;
        if (uri.getScheme().equals("content")) {
            Cursor cursor = context.getContentResolver().query(uri, null, null, null, null);
            try {
                if (cursor != null && cursor.moveToFirst()) {
                    result = cursor.getString(cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME));
                }
            } finally {
                cursor.close();
            }
        }
        if (result == null) {
            result = uri.getPath();
            int cut = result.lastIndexOf('/');
            if (cut != -1) {
                result = result.substring(cut + 1);
            }
        }
        return result;
    }

    public static void showEditTextsAsMandatory(EditText... ets) {
        for (EditText et : ets) {
            String hint = et.getHint().toString();

            et.setHint(Html.fromHtml(hint + "<font color=\"#ff0000\">" + " *" + "</font>"));
        }
    }

    public static void showTextViewsAsMandatory(TextView... tvs) {
        for (TextView tv : tvs) {
            String text = tv.getText().toString();

            tv.setText(Html.fromHtml(text + "<font color=\"#ff0000\">" + " *" + "</font>"));
        }
    }

    public static void showSpinnerAsMandatory(Spinner... sps) {
        for (Spinner spinner : sps) {
            ((TextView) spinner.getSelectedView()).setText(Html.fromHtml(((TextView) spinner.getSelectedView()).getText() + "<font color=\"#ff0000\">" + " *" + "</font>"));
        }
    }

    public static DecimalFormat formatDecimal() {
        symbolsEN_US = DecimalFormatSymbols.getInstance(Locale.US);
        df = new DecimalFormat("0.00", symbolsEN_US);
        return df;
    }

    public static void changeLang(Context context, String lang) {
        Locale myLocale = new Locale(lang);
        Locale.setDefault(myLocale);
        android.content.res.Configuration config = new android.content.res.Configuration();
        config.locale = myLocale;
        config.setLayoutDirection(myLocale);
        context.getResources().updateConfiguration(config, context.getResources().getDisplayMetrics());
        Intent i = context.getPackageManager()
                .getLaunchIntentForPackage(context.getPackageName());
        i.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        context.startActivity(i);
    }

    public static void changeLangWithoutRestart(Context context, String lang) {
        Locale myLocale = new Locale(lang);
        Locale.setDefault(myLocale);
        android.content.res.Configuration config = new android.content.res.Configuration();
        config.locale = myLocale;
        config.setLayoutDirection(myLocale);
        context.getResources().updateConfiguration(config, context.getResources().getDisplayMetrics());
    }

    public static String getCurrentDate() {
        return new SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(new Date());
    }

    public static String getCurrentDateWithDay() {
        return new SimpleDateFormat("EEEE MMM,dd yyyy", Locale.getDefault()).format(new Date());
    }

    public static String getCurrentDateTime() {
        return new SimpleDateFormat("MM-dd-yyyy HH:mm:ss", Locale.getDefault()).format(new Date());
    }

    public static Date convertStringToDate(String s) {
        DateFormat parser = new SimpleDateFormat("MM-dd-yyyy HH:mm:ss");
        Date date = null;
        try {
            date = (Date) parser.parse(s);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return date;
    }

    public static String getCurrentTime() {
        Date d = new Date();
        SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss");
        return (sdf.format(d));
    }

    public static String getCustomFormatDate(String date, String format) {
        Date d = null;
        try {
            d = new SimpleDateFormat("yyyy-MM-dd", Locale.ENGLISH).parse(date);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        Calendar cal = Calendar.getInstance();
        cal.setTime(d);
        String monthFormatDate = new SimpleDateFormat(format).format(cal.getTime());
        return monthFormatDate;
    }

    public static String convertUTCToNewFormat(String ourDate) throws ParseException {
        try {
            SimpleDateFormat formatter;
            if (ourDate.contains("T") || ourDate.contains("Z")) {
                formatter = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");
            } else {
                formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            }
            //formatter.setTimeZone(TimeZone.getTimeZone("Asia/Dubai"));
            Date value = formatter.parse(ourDate);

            SimpleDateFormat dateFormatter = new SimpleDateFormat("MM-dd-yyyy HH:mm:ss"); //this format changeable
            dateFormatter.setTimeZone(TimeZone.getDefault());
            //dateFormatter.setTimeZone(TimeZone.getTimeZone("Asia/Dubai"));
            ourDate = dateFormatter.format(value);

            //Log.d("ourDate", ourDate);
        } catch (Exception e) {
            //ourDate = "00-00-0000 00:08";
            ourDate = getCurrentDate() + " " + getCurrentTime();
        }
        return ourDate;
    }

    public static String convertUTCToNewFormatDubai(String ourDate) throws ParseException {
        try {
            SimpleDateFormat formatter;
            if (ourDate.contains("T") || ourDate.contains("Z")) {
                formatter = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");
            } else {
                formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            }
            //formatter.setTimeZone(TimeZone.getTimeZone("Asia/Dubai"));
            Date value = formatter.parse(ourDate);

            SimpleDateFormat dateFormatter = new SimpleDateFormat("MM-dd-yyyy HH:mm:ss"); //this format changeable
            //dateFormatter.setTimeZone(TimeZone.getDefault());
            dateFormatter.setTimeZone(TimeZone.getTimeZone("Asia/Dubai"));
            ourDate = dateFormatter.format(value);

            //Log.d("ourDate", ourDate);
        } catch (Exception e) {
            //ourDate = "00-00-0000 00:08";
            ourDate = getCurrentDate() + " " + getCurrentTime();
        }
        return ourDate;
    }

    public static String convertUTCToDateFormat(String ourDate) throws ParseException {
        try {
            SimpleDateFormat formatter;
            if (ourDate.contains("T") || ourDate.contains("Z")) {
                formatter = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");
            } else {
                formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            }
            //formatter.setTimeZone(TimeZone.getTimeZone("UTC"));
            Date value = formatter.parse(ourDate);

            SimpleDateFormat dateFormatter = new SimpleDateFormat("MM-dd-yyyy"); //this format changeable
            dateFormatter.setTimeZone(TimeZone.getDefault());
            ourDate = dateFormatter.format(value);

            //Log.d("ourDate", ourDate);
        } catch (Exception e) {
            ourDate = "00-00-0000 00:08";
        }
        return ourDate;
    }

    public static String convertUTCToTimeFormat(String ourDate) throws ParseException {
        try {
            SimpleDateFormat formatter;
            if (ourDate.contains("T") || ourDate.contains("Z")) {
                formatter = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");
            } else {
                formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            }
            //formatter.setTimeZone(TimeZone.getTimeZone("UTC"));
            Date value = formatter.parse(ourDate);

            SimpleDateFormat dateFormatter = new SimpleDateFormat("HH:mm"); //this format changeable
            dateFormatter.setTimeZone(TimeZone.getDefault());
            ourDate = dateFormatter.format(value);

            //Log.d("ourDate", ourDate);
        } catch (Exception e) {
            ourDate = "00-00-0000 00:08";
        }
        return ourDate;
    }

    public static String convertUTCToTimeFormatWithAM(String ourDate) throws ParseException {
        try {
            SimpleDateFormat formatter;
            if (ourDate.contains("T") || ourDate.contains("Z")) {
                formatter = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");
            } else {
                formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            }
            //formatter.setTimeZone(TimeZone.getTimeZone("UTC"));
            Date value = formatter.parse(ourDate);

            SimpleDateFormat dateFormatter = new SimpleDateFormat("HH:mm a"); //this format changeable
            dateFormatter.setTimeZone(TimeZone.getDefault());
            ourDate = dateFormatter.format(value);

            //Log.d("ourDate", ourDate);
        } catch (Exception e) {
            ourDate = "00-00-0000 00:08";
        }
        return ourDate;
    }

    public static String convertUTCToDatePrintFormat(String ourDate) throws ParseException {
        try {
            SimpleDateFormat formatter;
            if (ourDate.contains("T") || ourDate.contains("Z")) {
                formatter = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");
            } else {
                formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            }
            formatter.setTimeZone(TimeZone.getTimeZone("UTC"));
            Date value = formatter.parse(ourDate);

            SimpleDateFormat dateFormatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss"); //this format changeable
            //dateFormatter.setTimeZone(TimeZone.getTimeZone("Asia/Calcutta"));
            dateFormatter.setTimeZone(TimeZone.getDefault());
            ourDate = dateFormatter.format(value);

            //Log.d("ourDate", ourDate);
        } catch (Exception e) {
            ourDate = "00-00-0000 00:08";
        }
        return ourDate;
    }

    public static String convertLocalToDatePrintFormat(String ourDate) throws ParseException {
        try {
            SimpleDateFormat formatter;
            if (ourDate.contains("T") || ourDate.contains("Z")) {
                formatter = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");
            } else {
                formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            }
            //formatter.setTimeZone(TimeZone.getTimeZone("UTC"));
            Date value = formatter.parse(ourDate);

            SimpleDateFormat dateFormatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss"); //this format changeable
            //dateFormatter.setTimeZone(TimeZone.getTimeZone("Asia/Calcutta"));
            dateFormatter.setTimeZone(TimeZone.getDefault());
            ourDate = dateFormatter.format(value);

            //Log.d("ourDate", ourDate);
        } catch (Exception e) {
            ourDate = "00-00-0000 00:08";
        }
        return ourDate;
    }

    public static String convertUTCToTimePrintFormat(String ourDate) throws ParseException {
        try {
            SimpleDateFormat formatter;
            if (ourDate.contains("T") || ourDate.contains("Z")) {
                formatter = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");
            } else {
                formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            }
            //formatter.setTimeZone(TimeZone.getTimeZone("UTC"));
            Date value = formatter.parse(ourDate);

            SimpleDateFormat dateFormatter = new SimpleDateFormat("HH:mm:ss"); //this format changeable
            dateFormatter.setTimeZone(TimeZone.getDefault());
            ourDate = dateFormatter.format(value);

            //Log.d("ourDate", ourDate);
        } catch (Exception e) {
            ourDate = "00-00-0000 00:08";
        }
        return ourDate;
    }

    public static String getTimeAfterMinutes(String currentDate, int min) {

        SimpleDateFormat format = new SimpleDateFormat("MM-dd-yyyy HH:mm:ss");
        try {
            // Get calendar set to current date and time with Singapore time zone
            Calendar calendar = new GregorianCalendar(TimeZone.getTimeZone("Asia/Calcutta"));
            calendar.setTime(format.parse(currentDate));

            //Set calendar before 10 minutes
            calendar.add(Calendar.MINUTE, min);
            //Formatter
            DateFormat formatter = new SimpleDateFormat("MM-dd-yyyy HH:mm:ss");
            formatter.setTimeZone(TimeZone.getTimeZone("Asia/Calcutta"));
            return formatter.format(calendar.getTime());
        } catch (ParseException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

        return null;
    }

    public static boolean compareTime(String time, String endtime) {

        String pattern = "MM-dd-yyyy HH:mm:ss";
        SimpleDateFormat sdf = new SimpleDateFormat(pattern);

        try {
            Date date1 = sdf.parse(time);
            Date date2 = sdf.parse(endtime);

            if (date1.before(date2)) {
                return true;
            } else {
                return false;
            }
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return false;
    }

    public static boolean isInputCorrect(Editable s, int size, int dividerPosition, char divider) {
        boolean isCorrect = s.length() <= size;
        for (int i = 0; i < s.length(); i++) {
            if (i > 0 && (i + 1) % dividerPosition == 0) {
                isCorrect &= divider == s.charAt(i);
            } else {
                isCorrect &= Character.isDigit(s.charAt(i));
            }
        }
        return isCorrect;
    }

    public static String concatString(char[] digits, int dividerPosition, char divider) {
        final StringBuilder formatted = new StringBuilder();

        for (int i = 0; i < digits.length; i++) {
            if (digits[i] != 0) {
                formatted.append(digits[i]);
                if ((i > 0) && (i < (digits.length - 1)) && (((i + 1) % dividerPosition) == 0)) {
                    formatted.append(divider);
                }
            }
        }

        return formatted.toString();
    }

    public static char[] getDigitArray(final Editable s, final int size) {
        char[] digits = new char[size];
        int index = 0;
        for (int i = 0; i < s.length() && index < size; i++) {
            char current = s.charAt(i);
            if (Character.isDigit(current)) {
                digits[index] = current;
                index++;
            }
        }
        return digits;
    }

    //create bitmap from view and returns it
    public static Bitmap getBitmapFromView(View view) {
        //Define a bitmap with the same size as the view
        Bitmap returnedBitmap = Bitmap.createBitmap(view.getWidth(), view.getHeight(), Bitmap.Config.ARGB_8888);
        //Bind a canvas to it
        Canvas canvas = new Canvas(returnedBitmap);
        //Get the view's background
        Drawable bgDrawable = view.getBackground();
        if (bgDrawable != null) {
            //has background drawable, then draw it on the canvas
            bgDrawable.draw(canvas);
        } else {
            //does not have background drawable, then draw white background on the canvas
            canvas.drawColor(Color.WHITE);
        }
        // draw the view on the canvas
        view.draw(canvas);
        //return the bitmap
        return returnedBitmap;
    }

    public static HashMap<String, String> convertToHashMap(String jsonString) {
        HashMap<String, String> myHashMap = new HashMap<String, String>();
        if (jsonString!=null) {
            try {
                //JSONArray jArray = new JSONArray(jsonString);
                JSONObject jObject = new JSONObject(jsonString);
                for (Iterator<String> it = jObject.keys(); it.hasNext(); ) {
                    String keys = it.next();
                    myHashMap.put(keys, jObject.getString(keys));
                }
            } catch (JSONException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
        return myHashMap;
    }

    public static boolean isMyServiceRunning(Context ctx, Class<?> serviceClass) {
        ActivityManager manager = (ActivityManager) ctx.getSystemService(Context.ACTIVITY_SERVICE);
        for (ActivityManager.RunningServiceInfo service : manager.getRunningServices(Integer.MAX_VALUE)) {
            if (serviceClass.getName().equals(service.service.getClassName())) {
                return true;
            }
        }
        return false;
    }

    public static double roundDecimal(double value, int places) {
        if (places < 0) throw new IllegalArgumentException();

        long factor = (long) Math.pow(10, places);
        value = value * factor;
        long tmp = Math.round(value);
        return (double) tmp / factor;
    }

    public static String calculateDifferenceBWDateTime(String startDate, String endDate) {
        //milliseconds
        SimpleDateFormat simpleDateFormat = new SimpleDateFormat("MM-dd-yyyy HH:mm:ss");

        try {
            Date date1 = simpleDateFormat.parse(startDate);
            Date date2 = simpleDateFormat.parse(endDate);
            long different = date2.getTime() - date1.getTime();

            long secondsInMilli = 1000;
            long minutesInMilli = secondsInMilli * 60;
            long hoursInMilli = minutesInMilli * 60;
            long daysInMilli = hoursInMilli * 24;

            long elapsedDays = different / daysInMilli;
            different = different % daysInMilli;

            long elapsedHours = different / hoursInMilli;
            different = different % hoursInMilli;

            long elapsedMinutes = different / minutesInMilli;
            different = different % minutesInMilli;

            long elapsedSeconds = different / secondsInMilli;

            return elapsedDays+","+elapsedHours+","+elapsedMinutes+","+elapsedSeconds;
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return "0,0";

    }

    @RequiresApi(api = Build.VERSION_CODES.Q)
    public static boolean isAppIsInBackground(Context context) {
        boolean isInBackground = true;
        ActivityManager am = (ActivityManager) context.getSystemService(Context.ACTIVITY_SERVICE);
        if (Build.VERSION.SDK_INT > Build.VERSION_CODES.KITKAT_WATCH) {
            List<ActivityManager.RunningAppProcessInfo> runningProcesses = am.getRunningAppProcesses();
            for (ActivityManager.RunningAppProcessInfo processInfo : runningProcesses) {
                if (processInfo.importance == ActivityManager.RunningAppProcessInfo.IMPORTANCE_FOREGROUND) {
                    for (String activeProcess : processInfo.pkgList) {
                        if (activeProcess.equals(context.getPackageName())) {
                            isInBackground = false;
                        }
                    }
                }
            }
        } else {
            List<ActivityManager.RunningTaskInfo> taskInfo = am.getRunningTasks(1);
            ComponentName componentInfo = taskInfo.get(0).topActivity;
            if (componentInfo.getPackageName().equals(context.getPackageName())) {
                isInBackground = false;
            }
        }

        return isInBackground;
    }

    public static String getAppVersion(Context context){
        String version="";
        try {
            PackageManager pm = context.getPackageManager();
            PackageInfo pInfo = pm.getPackageInfo(GoGroceryPicking.applicationContext.getPackageName(), 0);
            version = pInfo.versionName;

        } catch (PackageManager.NameNotFoundException e) {
            e.printStackTrace();
        }
        return version;
    }

    public static String twoDecimalRoundOff(double argValue) {

        System.out.println("Sukdev: twoDecimalRoundOff : argValue : " + argValue);
        if (argValue == 0) {
            return String.valueOf(0.00);
        }/*else if(String.valueOf(argValue).split(".")[0].length()==1) {
           if(String.valueOf(argValue).split(".")[0].equals("0")) {
               DecimalFormat df = new DecimalFormat("##.00");
               df.setMaximumFractionDigits(2);

               return "0"+df.format(argValue);
           }else {
               DecimalFormat df = new DecimalFormat("##.00");
               df.setMaximumFractionDigits(2);

               return df.format(argValue);
           }
        }*/ else {
//            DecimalFormat df = new DecimalFormat("##.##");
//            df.setMaximumFractionDigits(2);
            @SuppressLint("DefaultLocale") String raoundValue = String.format("%.2f", argValue);
            return raoundValue;
        }
    }



    public static String removeTrailingZero(String argValue) {
String s;
       // s = argValue.indexOf(".") < 0 ? argValue : argValue.replaceAll("0*$", "").replaceAll("\\.$", "");
        s = argValue.contains(".") ? argValue.replaceAll("0*$","").replaceAll("\\.$","") : argValue;
            return s;
        }

}
