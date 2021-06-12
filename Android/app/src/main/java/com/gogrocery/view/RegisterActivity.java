package com.gogrocery.view;

import android.app.Dialog;
import androidx.lifecycle.ViewModelProviders;
import android.content.Intent;
import androidx.databinding.DataBindingUtil;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Build;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.TextView;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.facebook.CallbackManager;
import com.facebook.FacebookCallback;
import com.facebook.FacebookException;
import com.facebook.FacebookSdk;
import com.facebook.GraphRequest;
import com.facebook.GraphResponse;
import com.facebook.login.LoginManager;
import com.facebook.login.LoginResult;
import com.gogrocery.Constants.Constants;
import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.Models.LoginModel.LoginModel;
import com.gogrocery.R;
import com.gogrocery.ViewModel.MainViewModel;
import com.gogrocery.databinding.ActivityRegisterBinding;
import com.google.android.gms.auth.api.Auth;
import com.google.android.gms.auth.api.signin.GoogleSignIn;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.ApiException;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.tasks.Task;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class RegisterActivity extends AppCompatActivity implements View.OnClickListener, GoogleApiClient.OnConnectionFailedListener {

    private ActivityRegisterBinding mActivityRegisterBinding;
    private String navigateTo = "";
    private GoogleApiClient googleApiClient;
    private static int RC_SIGN_IN = 101;
    private CallbackManager callbackManager;
    private SharedPreferenceManager mSharedPreferenceManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityRegisterBinding = DataBindingUtil.setContentView(this, R.layout.activity_register);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        EditTextCheckValidate();
        hideStatusBarColor();

        getBundelExtra();
        setListners();
        if(Constants.isInternetConnected(RegisterActivity.this)) {
            facebookLoginMethod();
            GoogleSignInOptions gso = new GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                    .requestEmail()
                    .requestProfile()
                    .build();
            googleApiClient = new GoogleApiClient.Builder(this)
                    .enableAutoManage(this, this)
                    .addApi(Auth.GOOGLE_SIGN_IN_API, gso)
                    .build();
        } else {
        Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
    }


        mActivityRegisterBinding.llGoogle.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = Auth.GoogleSignInApi.getSignInIntent(googleApiClient);
                startActivityForResult(intent, RC_SIGN_IN);
            }
        });

        final boolean[] ishasfocus = {false};

       /* mActivityRegisterBinding.tvMobileRegister.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                if (hasFocus) {
                    mActivityRegisterBinding.tvMobileRegister.setText("+971 ");
                    ishasfocus[0] = hasFocus;
                    System.out.println("Rahul : RegisterActivity : onFocusChange : tvMobileRegister : " + hasFocus);
                } else {
                    ishasfocus[0] = hasFocus;
                    mActivityRegisterBinding.tvMobileRegister.clearFocus();
                    mActivityRegisterBinding.tvMobileRegister.clearComposingText();

                    System.out.println("Rahul : RegisterActivity : onFocusChange : tvMobileRegister : " + hasFocus);

                }
            }
        });*/

        /*mActivityRegisterBinding.tvMobileRegister.addTextChangedListener(new TextWatcher() {

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                // TODO Auto-generated method stub

            }

            @Override
            public void beforeTextChanged(CharSequence s, int start, int count,
                                          int after) {
                // TODO Auto-generated method stub

            }

            @Override
            public void afterTextChanged(Editable s) {
                System.out.println("Rahul : RegisterActivity : afterTextChanged : ishasfocus : "+ishasfocus[0]);
                if (ishasfocus[0]=true) {
                    if (!s.toString().startsWith("+971 ")) {
                        mActivityRegisterBinding.tvMobileRegister.setText("+971 ");
                        Selection.setSelection(mActivityRegisterBinding.tvMobileRegister.getText(), mActivityRegisterBinding.tvMobileRegister.getText().length());

                    }
                }

            }
        });*/

        mActivityRegisterBinding.edtCarrierNo.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                if (hasFocus) {
                    carrierDialog();
                }

            }
        });
        mActivityRegisterBinding.edtCarrierNo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                carrierDialog();
            }
        });
    }

    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }
    private void carrierDialog() {
        Dialog mCarrierDilog = new Dialog(RegisterActivity.this);
        mCarrierDilog.setContentView(R.layout.carrier_code_dialog);
        TextView tv50, tv52, tv53, tv54, tv55, tv56, tv58;
        tv50 = mCarrierDilog.findViewById(R.id.tv50);
        tv52 = mCarrierDilog.findViewById(R.id.tv52);
        tv53 = mCarrierDilog.findViewById(R.id.tv53);
        tv54 = mCarrierDilog.findViewById(R.id.tv54);
        tv55 = mCarrierDilog.findViewById(R.id.tv55);
        tv56 = mCarrierDilog.findViewById(R.id.tv56);
        tv58 = mCarrierDilog.findViewById(R.id.tv58);
        String selected = "";

        tv50.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                mActivityRegisterBinding.edtCarrierNo.setText(getResources().getString(R.string._50)+"  ");
                mCarrierDilog.dismiss();
            }
        });
        tv52.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityRegisterBinding.edtCarrierNo.setText(getResources().getString(R.string._52)+"  ");
                mCarrierDilog.dismiss();
            }
        });
        tv53.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityRegisterBinding.edtCarrierNo.setText(getResources().getString(R.string._53)+"  ");
                mCarrierDilog.dismiss();
            }
        });
        tv54.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityRegisterBinding.edtCarrierNo.setText(getResources().getString(R.string._54)+"  ");
                mCarrierDilog.dismiss();
            }
        });
        tv55.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityRegisterBinding.edtCarrierNo.setText(getResources().getString(R.string._55)+"  ");
                mCarrierDilog.dismiss();
            }
        });
        tv56.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityRegisterBinding.edtCarrierNo.setText(getResources().getString(R.string._56)+"  ");
                mCarrierDilog.dismiss();
            }
        });
        tv58.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mActivityRegisterBinding.edtCarrierNo.setText(getResources().getString(R.string._58)+"  ");
                mCarrierDilog.dismiss();
            }
        });


        mCarrierDilog.show();
    }

    private void getBundelExtra() {
        Bundle b = getIntent().getExtras();
        if (b != null) {
            navigateTo = b.getString("from_where");
        }
    }

    private void setListners() {
        mActivityRegisterBinding.btnSignup.setOnClickListener(this);
        mActivityRegisterBinding.llFacebook.setOnClickListener(this);
        mActivityRegisterBinding.llGoogle.setOnClickListener(this);
        mActivityRegisterBinding.tvSignIn.setOnClickListener(this);
    }


    private void EditTextCheckValidate(){
        mActivityRegisterBinding.tvNameRegister.addTextChangedListener(new TextWatcher() {
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
                        mActivityRegisterBinding.tvNameRegister.setText(result);
                        mActivityRegisterBinding.tvNameRegister.setSelection(result.length());
                        // alert the user
                    }
                }

                mActivityRegisterBinding.tilname.setError(null);

            }
        });

        mActivityRegisterBinding.tvMobileRegister.addTextChangedListener(new TextWatcher() {
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
                    mActivityRegisterBinding.tvMobileRegister.setText(result);
                    mActivityRegisterBinding.tvMobileRegister.setSelection(result.length());
                    // alert the user
                }
                mActivityRegisterBinding.tilmobileno.setError(null);
            }
        });

        mActivityRegisterBinding.tvEmailRegister.addTextChangedListener(new TextWatcher() {
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
                    mActivityRegisterBinding.tvEmailRegister.setText(result);
                    mActivityRegisterBinding.tvEmailRegister.setSelection(result.length());
                    // alert the user
                }
                mActivityRegisterBinding.tilemailaddress.setError(null);
            }
        });
        mActivityRegisterBinding.tvPasswordRegister.addTextChangedListener(new TextWatcher() {
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
                    mActivityRegisterBinding.tvPasswordRegister.setText(result);
                    mActivityRegisterBinding.tvPasswordRegister.setSelection(result.length());
                    // alert the user
                }
                mActivityRegisterBinding.tilPassword.setError(null);
            }
        });






    }






    private void facebookLoginMethod() {

        FacebookSdk.sdkInitialize(getApplicationContext());
        callbackManager = CallbackManager.Factory.create();


        // Callback registration

        LoginManager.getInstance().registerCallback(callbackManager,
                new FacebookCallback<LoginResult>() {
                    @Override
                    public void onSuccess(LoginResult loginResult) {
                        System.out.println("LoggedIn : " + loginResult.toString());
                        GraphRequest request = GraphRequest.newMeRequest(
                                loginResult.getAccessToken(), new GraphRequest.GraphJSONObjectCallback() {
                                    @Override
                                    public void onCompleted(JSONObject object, GraphResponse response) {
                                        Log.v("LoginActivity", response.toString());
                                        System.out.println("fbresponse : " + response.toString());
                                        System.out.println("fbresponse : object : " + object.toString());
                                        // Application code
                                        try {
                                            String email = object.getString("email");
                                            String facebook_id = object.getString("id");
                                            String name = object.getString("name");
                                            URL imageURL = new URL("https://graph.facebook.com/" + facebook_id + "/picture?type=large");
                                            System.out.println("fbresponse : imageURL : " + imageURL.toString());

                                            String[] FirstLastName = name.split(" ");
                                            // facebookUserLogin(facebook_id, FirstLastName[0], FirstLastName[1], email, imageURL.toString());
                                            mSharedPreferenceManager.storeUserProfileDetail(FirstLastName[0] + "" + FirstLastName[1], email, "", imageURL.toString(), "");
                                            //  String birthday = object.getString("birthday"); // 01/31/1980 format
                                            requestSocialLogin("", facebook_id, email, FirstLastName[0], FirstLastName[1], "", imageURL.toString());

                                        } catch (JSONException e) {
                                            e.printStackTrace();
                                        } catch (MalformedURLException e) {
                                            e.printStackTrace();
                                        }

                                    }
                                });
                        Bundle parameters = new Bundle();
                        parameters.putString("fields", "id,name,email,gender,birthday");
                        request.setParameters(parameters);
                        request.executeAsync();

                    }

                    @Override
                    public void onCancel() {
                        Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.error_msg_login_cancelled));
                        //Toast.makeText(RegisterActivity.this, "Login Cancel", Toast.LENGTH_LONG).show();
                    }

                    @Override
                    public void onError(FacebookException exception) {
                        Constants.showToastInMiddle(getApplicationContext(), exception.getMessage());
                        //Toast.makeText(RegisterActivity.this, exception.getMessage(), Toast.LENGTH_LONG).show();
                    }
                });

        mActivityRegisterBinding.llFacebook.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                LoginManager.getInstance().logInWithReadPermissions(RegisterActivity.this, Arrays.asList("public_profile", "email"));
                if (Constants.mGoogleSignInClient != null) {
                    Constants.mGoogleSignInClient.signOut();
                }
            }
        });


    }

    private void handleSignInResult(Task<GoogleSignInAccount> completedTask) {
        try {
            GoogleSignInAccount account = completedTask.getResult(ApiException.class);
            System.out.println("Rahul : GoogleSignInAccount : " + new Gson().toJson(account));
            System.out.println("Rahul : handleSignInResult : name :  " + account.getAccount().name);
            System.out.println("Rahul : handleSignInResult : getDisplayName :  " + account.getDisplayName());
            System.out.println("Rahul : handleSignInResult : getEmail :  " + account.getEmail());
            System.out.println("Rahul : handleSignInResult : getId :  " + account.getId());
            // System.out.println("Rahul : handleSignInResult : photo :  " + account.getPhotoUrl().getPath());


            // Signed in successfully, show authenticated UI.
            runOnUiThread(new Runnable() {
                public void run() {
                    if (account != null) {
                        // UI code goes here
                        updateUI(account);
                    } else {
                        Constants.showToastInMiddle(getApplicationContext(),  getResources().getString(R.string.error_msg_login_cancelled));

                        // Toast.makeText(getApplicationContext(), "Login Cancelled", Toast.LENGTH_SHORT).show();
                    }
                }
            });

        } catch (ApiException e) {
            // The ApiException status code indicates the detailed failure reason.
            // Please refer to the GoogleSignInStatusCodes class reference for more information.
            //Toast.makeText(getApplicationContext(), "Login Cancelled", Toast.LENGTH_SHORT).show();
            Constants.showToastInMiddle(getApplicationContext(),  getResources().getString(R.string.error_msg_login_cancelled));
            //updateUI(null);
        }
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (callbackManager != null) {
            callbackManager.onActivityResult(requestCode, resultCode, data);
        }
        super.onActivityResult(requestCode, resultCode, data);

        System.out.println("Rahul : requestCode : " + requestCode);
        // Result returned from launching the Intent from GoogleSignInClient.getSignInIntent(...);
        if (requestCode == RC_SIGN_IN) {
            // The Task returned from this call is always completed, no need to attach
            // a listener.
            //GoogleSignInResult result = Auth.GoogleSignInApi.getSignInResultFromIntent(data);

            Task<GoogleSignInAccount> task = GoogleSignIn.getSignedInAccountFromIntent(data);

            //handleSignInResult(result);
            handleSignInResult(task);
        } else {

        }
    }

    public void updateUI(GoogleSignInAccount account) {


        if (account.getId() != null) {
            System.out.println("Rahul : LoginActivity : updateUI : " + account.getId());
            System.out.println("Rahul : LoginActivity : updateUI : " + account.getEmail());
            System.out.println("Rahul : LoginActivity : updateUI : " + account.getDisplayName());
//        System.out.println("Rahul : LoginActivity : updateUI : " + account.getPhotoUrl().toString());

            try {

                requestSocialLogin(account.getId(), "", account.getEmail(), account.getDisplayName(), "", "", "");

            } catch (JSONException e) {
                e.printStackTrace();
            }
        } else {
            Constants.showToastInMiddle(getApplicationContext(),  getResources().getString(R.string.error_msg_login_cancelled));
            // Toast.makeText(getApplicationContext(), "Login Cancelled", Toast.LENGTH_SHORT).show();

        }

       /* mSharedPreferenceManager.storeUserProfileDetail(account.getDisplayName(), account.getEmail(), "", account.getPhotoUrl().toString(), "");
        Intent i = new Intent(this, MainActivityNew.class);
        startActivity(i);*/
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.btnSignup:
                validation();
                /*Intent i = new Intent(RegisterActivity.this, PhoneRegistration.class);
                startActivity(i);
                finish();*/
                break;
            case R.id.tvSignIn:
                Intent tvSignIn = new Intent(RegisterActivity.this, LoginActivity.class);
                startActivity(tvSignIn);

                break;
        }
    }

    private void validation() {
        String name = mActivityRegisterBinding.tvNameRegister.getText().toString();
        String lname = mActivityRegisterBinding.tvLastNameRegister.getText().toString();
        String address = mActivityRegisterBinding.tvAddressRegister.getText().toString();
        String mobile = mActivityRegisterBinding.tvMobileRegister.getText().toString();
        String email = mActivityRegisterBinding.tvEmailRegister.getText().toString().trim();
        String password = mActivityRegisterBinding.tvPasswordRegister.getText().toString().trim();

        if ("".equals(name) || name.isEmpty()) {
            mActivityRegisterBinding.tilname.setError(getString(R.string.error_msg_enter_name));
        }else if ("".equals(lname) || lname.isEmpty()) {
            mActivityRegisterBinding.tilLastName.setError(getString(R.string.error_msg_enter_last_name));
        }
        /*else if (mActivityRegisterBinding.edtCarrierNo.getText().toString().isEmpty()) {
            Constants.showToastInMiddle(getApplicationContext(), getString(R.string.error_msg_enter_carrier_code));
        } else if ("".equals(mobile)) {
            mActivityRegisterBinding.tilmobileno.setError(getString(R.string.error_msg_enter_mobile_no));
        } else if (mobile.length() != 7) {
            mActivityRegisterBinding.tilmobileno.setError(getString(R.string.error_msg_enter_7_digit_mobile_no));
        } */else if ("".equals(email)) {
            mActivityRegisterBinding.tilemailaddress.setError(getString(R.string.error_msg_enter_email));
        } else if ("".equals(password)) {
            mActivityRegisterBinding.tilPassword.setError(getString(R.string.error_msg_enter_password));
        } else if(password.length()<5){
            mActivityRegisterBinding.tilPassword.setError(getString(R.string.error_msg_enter_password_lenght));
        }else if (!Constants.emailPatternValidtion(mActivityRegisterBinding.tvEmailRegister.getText().toString())) {
            System.out.println("Rahul : loginValidity : validations 5");
            mActivityRegisterBinding.tilemailaddress.setError(getString(R.string.login_field_error));
        } else {

            try {
                requestRegistetNew(name,lname, address, "+971" + mActivityRegisterBinding.edtCarrierNo.getText().toString().trim() + mobile, email, password);
            } catch (JSONException e) {
                e.printStackTrace();
            }
            //requestRegisterNew(name, address, mobile, email, password);
        }
    }

    public void requestRegistetNew(String argName,String lname, String argAddress, String argMobileNumber, String argEmailAddress, String argPassword) throws JSONException {

        if(Constants.isInternetConnected(RegisterActivity.this)) {


        mActivityRegisterBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("first_name", argName);
        mJsonObject.put("last_name", lname);
        //mJsonObject.put("address", "");
        //mJsonObject.put("phone", argMobileNumber);
        mJsonObject.put("user_email", argEmailAddress.toLowerCase().trim());
        mJsonObject.put("user_password", argPassword);
        System.out.println("Response : RegisterActivity : requestRegister : param : " + mJsonObject);


        JsonObjectRequest mJsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.SIGN_UP, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        mActivityRegisterBinding.progressSpinKitView.setVisibility(View.GONE);
                        Gson gson = new Gson();
                        LoginModel mLoginModel = gson.fromJson(response.toString(), LoginModel.class);
                        if (mLoginModel != null) {

                            String responseString = gson.toJson(mLoginModel);
                            System.out.println("Response : RegisterActivity : requestRegister : " + responseString);
                            if (mLoginModel != null) {
                                if (mLoginModel.getStatus() == Integer.parseInt(Constants.VARIABLES.STATUS_SUCESS_CODE)) {


                                    mSharedPreferenceManager.storeUserProfileDetail(mLoginModel.getData().getFirstName() + " " + mLoginModel.getData().getLastName(), mLoginModel.getData().getEmail(), mLoginModel.getData().getPhone(), "", mLoginModel.getData().getToken());

                                    switch (navigateTo) {
                                        case "MyCart": {
                                            Intent i = new Intent(RegisterActivity.this, MyCart.class);
                                            startActivity(i);
                                            finish();
                                            break;
                                        }
                                        case "DetailPage":
                                            finish();
                                            break;
                                        case "add_address":
                                            finish();
                                            break;
                                        case "pushNotification": {
                                            Log.e("pushOrderID", "" + getIntent().getExtras().getString("pushOrderID"));
                                            Intent i = new Intent(RegisterActivity.this, SubstituteActivity.class);
                                            i.putExtra("pushOrderID", getIntent().getExtras().getString("pushOrderID"));
                                            startActivity(i);
                                            break;
                                        }
                                        case "home": {
                                            Intent i = new Intent(RegisterActivity.this, MainActivityNew.class);
                                            startActivity(i);
                                            finish();
                                            break;
                                        }
                                        default:
                                            if (mSharedPreferenceManager.getLatitude() != null && !mSharedPreferenceManager.getLatitude().isEmpty() && mSharedPreferenceManager.getLongitude() != null && !mSharedPreferenceManager.getLongitude().isEmpty()) {
                                                Intent i = new Intent(RegisterActivity.this, SelectCategory.class);
                                                i.putExtra("latitude", mSharedPreferenceManager.getLatitude());
                                                i.putExtra("longitude", mSharedPreferenceManager.getLongitude());
                                                i.putExtra("select_category_list","");
                                                i.putExtra("from_where","start");
                                                startActivity(i);
                                                finish();
                                            } else {
                                                Intent i = new Intent(RegisterActivity.this, IntroStepOne.class);
                                                i.putExtra("from","start");
                                                startActivity(i);
                                                finish();
                                            }
                                            break;
                                    }


                                } else {
                                    Constants.showToastInMiddle(getApplicationContext(), mLoginModel.getMessage());
                                    // Toast.makeText(getApplicationContext(), mLoginModel.getMessage(), Toast.LENGTH_LONG).show();
                                }

                            } else {
                                //Toast.makeText(getApplicationContext(), "Enter Valid Credentials", Toast.LENGTH_LONG).show();
                            }
                       /* SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
                        mSharedPreferenceManager.storeUserProfileDetail(responseBodyResponse.getData().getFirstName() + " " + responseBodyResponse.getData().getLastName(), "", "", "");
                        Intent i = new Intent(this, MainActivityNew.class);
                        startActivity(i);*/
                        } else {
                            System.out.println("Response : RegisterActivity : requestRegister : null : ");
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mActivityRegisterBinding.progressSpinKitView.setVisibility(View.GONE);
                try {
                    String responseBody = new String(error.networkResponse.data, "utf-8");
                    JSONObject data = new JSONObject(responseBody);

                    String message = data.getString("message");
                    Constants.showToastInMiddle(getApplicationContext(), message);

                    //Toast.makeText(getApplicationContext(), message, Toast.LENGTH_LONG).show();
                } catch (Exception ee) {
                    System.out.println("Rahul : DeliveryDetail : requestSaveOrder : onErrorResponse : " + ee);
                }
               /* if (error.networkResponse.statusCode == 417) {

                    //Toast.makeText(getApplicationContext(), "Email / Mobile already exist", Toast.LENGTH_SHORT).show();
                }*/
                System.out.println("Rahul : RegisterActivity : requestRegisterNew : VolleyError : " + error.toString());
                System.out.println("Rahul : RegisterActivity : requestRegisterNew : VolleyError : " + error);
                System.out.println("Rahul : RegisterActivity : requestRegisterNew : VolleyError : " + error.getMessage());
                System.out.println("Rahul : RegisterActivity : requestRegisterNew : VolleyError : " + error.networkResponse.data.toString());
                System.out.println("Rahul : RegisterActivity : requestRegisterNew : VolleyError : " + error.networkResponse.toString());
                System.out.println("Rahul : RegisterActivity : requestRegisterNew : VolleyError : " + new Gson().toJson(error));
                System.out.println("Rahul : RegisterActivity : requestRegisterNew : VolleyError : " + error.networkResponse.statusCode);
                System.out.println("Rahul : RegisterActivity : requestRegisterNew : VolleyError : " + error.networkResponse.headers);


            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("DEVICEID", Constants.getDeviceId(getApplicationContext()));
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
        }else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }

    private void requestRegister(String argName, String argAddress, String argMobileNumber, String argEmailAddress, String argPassword) {

        // Update the list when the data changes
        mActivityRegisterBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        MainViewModel mainViewModel;
        mainViewModel = ViewModelProviders.of(this).get(MainViewModel.class);

        //Param
        /*{
            "user_email":"rahul.sharma@navsoft.in",
                "user_password":"123456789",
                "username":"Rahul@Navsoft",
                "first_name":"Rahul",
                "last_name":"Sharma",
                "address":"Ghatkopar",
                "phone":"7977947039"
        }*/
        HashMap<String, Object> param = new HashMap<>();
        param.put("name", argName);
        param.put("address", argAddress);
        param.put("phone", argMobileNumber);
        param.put("user_email", argEmailAddress);
        param.put("user_password", argPassword);
        System.out.println("Response : RegisterActivity : requestRegister : param : " + param);
        //ViewModel Request
        mainViewModel.register(param)

                .observe(this, responseBodyResponse -> {
                    mActivityRegisterBinding.progressSpinKitView.setVisibility(View.GONE);
                    if (responseBodyResponse != null) {
                        Gson gson = new Gson();
                        String responseString = gson.toJson(responseBodyResponse);
                        System.out.println("Response : RegisterActivity : requestRegister : " + responseString);
                        if (responseBodyResponse != null) {
                            if (responseBodyResponse.getStatus() == Integer.parseInt(Constants.VARIABLES.STATUS_SUCESS_CODE)) {

                                SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
                                mSharedPreferenceManager.storeUserProfileDetail(responseBodyResponse.getData().getFirstName() + " " + responseBodyResponse.getData().getLastName(), responseBodyResponse.getData().getEmail(), responseBodyResponse.getData().getPhone(), "", responseBodyResponse.getData().getToken());
                                Intent i = new Intent(this, MainActivityNew.class);
                                startActivity(i);

                            } else {
                                Constants.showToastInMiddle(getApplicationContext(), responseBodyResponse.getMessage());
                                //Toast.makeText(getApplicationContext(), responseBodyResponse.getMessage(), Toast.LENGTH_LONG).show();
                            }

                        } else {
                            //Toast.makeText(getApplicationContext(), "Enter Valid Credentials", Toast.LENGTH_LONG).show();
                        }
                       /* SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
                        mSharedPreferenceManager.storeUserProfileDetail(responseBodyResponse.getData().getFirstName() + " " + responseBodyResponse.getData().getLastName(), "", "", "");
                        Intent i = new Intent(this, MainActivityNew.class);
                        startActivity(i);*/
                    } else {
                        System.out.println("Response : RegisterActivity : requestRegister : null : ");
                    }


                });

    }

    public void requestSocialLogin(String argGoogleLoginId, String argFbLoginId, String argUserEmail,
                                   String argFName, String argLName, String argPhone, String argImageName) throws JSONException {
        mActivityRegisterBinding.progressSpinKitView.setVisibility(View.VISIBLE);
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

        JSONObject mJsonObject = new JSONObject();
        mJsonObject.put("google_login_id", argGoogleLoginId);
        mJsonObject.put("facebook_id", argFbLoginId);
        mJsonObject.put("user_email", argUserEmail);
        mJsonObject.put("first_name", argFName);
        mJsonObject.put("last_name", argLName);
        mJsonObject.put("phone", argPhone);
        mJsonObject.put("image_name", argImageName);
        mJsonObject.put("device_id", Constants.getDeviceId(getApplicationContext()));


        System.out.println("Rahul : LoginActivity : requestSocialLogin : " + mJsonObject);
        JsonObjectRequest mJsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                Constants.BASE_URL + Constants.API_METHODS.SOCIAL_LOGIN, mJsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Rahul : LoginActivity : requestSocialLogin : response: " + response);
                        mActivityRegisterBinding.progressSpinKitView.setVisibility(View.GONE);
                        Gson gson = new Gson();
                        LoginModel mLoginModel = gson.fromJson(response.toString(), LoginModel.class);

                        if (mLoginModel != null) {
                            if (mLoginModel.getStatus() == Integer.parseInt(Constants.VARIABLES.STATUS_SUCESS_CODE)) {

                                SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
                                mSharedPreferenceManager.storeUserProfileDetail(mLoginModel.getData().getFirstName() + " " + mLoginModel.getData().getLastName(), mLoginModel.getData().getEmail(), mLoginModel.getData().getPhone(), "", mLoginModel.getData().getToken());

                                switch (navigateTo) {
                                    case "MyCart": {
                                        Intent i = new Intent(RegisterActivity.this, MyCart.class);
                                        startActivity(i);
                                        finish();
                                        break;
                                    }
                                    case "DetailPage":
                                        finish();
                                        break;
                                    case "add_address":
                                        finish();
                                        break;
                                    case "pushNotification": {
                                        Log.e("pushOrderID", "" + getIntent().getExtras().getString("pushOrderID"));
                                        Intent i = new Intent(RegisterActivity.this, SubstituteActivity.class);
                                        i.putExtra("pushOrderID", getIntent().getExtras().getString("pushOrderID"));
                                        startActivity(i);
                                        break;
                                    }
                                    case "home": {
                                        Intent i = new Intent(RegisterActivity.this, MainActivityNew.class);
                                        startActivity(i);
                                        finish();
                                        break;
                                    }
                                    default:
                                        SharedPreferenceManager preferenceManager = new SharedPreferenceManager(getApplicationContext());
                                        if (mSharedPreferenceManager.getLatitude() != null && !mSharedPreferenceManager.getLatitude().isEmpty() && mSharedPreferenceManager.getLongitude() != null && !mSharedPreferenceManager.getLongitude().isEmpty()) {
                                            Intent i = new Intent(RegisterActivity.this, SelectCategory.class);
                                            i.putExtra("latitude", mSharedPreferenceManager.getLatitude());
                                            i.putExtra("longitude", mSharedPreferenceManager.getLongitude());
                                            i.putExtra("select_category_list","");
                                            i.putExtra("from_where","start");
                                            startActivity(i);
                                            finish();
                                        }else {
                                            Intent i = new Intent(RegisterActivity.this, IntroStepOne.class);
                                            i.putExtra("from","start");
                                            startActivity(i);
                                            finish();
                                        }
                                        break;
                                }


                            } else {
                                Constants.showToastInMiddle(getApplicationContext(), mLoginModel.getMessage());

                                //Toast.makeText(getApplicationContext(), mLoginModel.getMessage(), Toast.LENGTH_LONG).show();
                            }

                        } else {
                            Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.enter_valid_credentials));

                            // Toast.makeText(getApplicationContext(), "Enter Valid Credentials", Toast.LENGTH_LONG).show();
                        }
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                mActivityRegisterBinding.progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : LoginActivity : requestSocialLogin : VolleyError : " + error.toString());
                Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.enter_valid_credentials));

                //Toast.makeText(getApplicationContext(), "Enter Valid Credentials", Toast.LENGTH_LONG).show();
            }
        })

        {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json");
                headers.put("DEVICEID", Constants.getDeviceId(getApplicationContext()));
                return headers;
            }


        };


        // Adding request to request queue
        queue.add(mJsonObjectRequest);
    }

    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {

    }
}
