package com.gogrocery.view;

import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;

import androidx.appcompat.app.AlertDialog;
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

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
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
import com.gogrocery.databinding.ActivityLoginBinding;
import com.google.android.gms.auth.api.signin.GoogleSignIn;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.auth.api.signin.GoogleSignInResult;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.ApiException;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.iid.FirebaseInstanceId;
import com.google.firebase.iid.InstanceIdResult;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class LoginActivity extends AppCompatActivity implements View.OnClickListener, GoogleApiClient.OnConnectionFailedListener {


    private static final String TAG = "LoginActivity";
    private ActivityLoginBinding mActivityLoginBinding;
    private CallbackManager callbackManager;
    private SharedPreferenceManager mSharedPreferenceManager;
    private static int RC_SIGN_IN = 101;
    private GoogleApiClient googleApiClient;
    private String navigateTo = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mActivityLoginBinding = DataBindingUtil.setContentView(this, R.layout.activity_login);
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
        EditTextCheckValidate();
        hideStatusBarColor();
        if (Constants.isInternetConnected(LoginActivity.this)) {
            getFcmToken();
            facebookLoginMethod();
            setOnClickListners();
            googleLoginMethod();

        } else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
/*
        GoogleSignInOptions gso = new GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                .requestEmail()
                .requestProfile()
                .requestIdToken("805854465820-fvhop986oam1u1105580va0u5p64sivg.apps.googleusercontent.com")
                .build();
        googleApiClient = new GoogleApiClient.Builder(this)
                .enableAutoManage(this, this)
                .addApi(Auth.GOOGLE_SIGN_IN_API, gso)
                .build();


        mActivityLoginBinding.llGoogle.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = Auth.GoogleSignInApi.getSignInIntent(googleApiClient);
                startActivityForResult(intent, RC_SIGN_IN);
            }
        });*/
        getBundelExtra();

    }

    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }

    private void getBundelExtra() {
        Bundle b = getIntent().getExtras();
        if (b != null) {
            navigateTo = b.getString("from_where");
        }
    }

    private void setOnClickListners() {
        mActivityLoginBinding.btnSignin.setOnClickListener(this);
        mActivityLoginBinding.btnGuest.setOnClickListener(this);
        mActivityLoginBinding.tvForgetPassword.setOnClickListener(this);
        mActivityLoginBinding.tvSignUp.setOnClickListener(this);
        mActivityLoginBinding.llFacebook.setOnClickListener(this);

        /*if (ActivityCompat.checkSelfPermission(this, Manifest.permission.GET_ACCOUNTS) != PackageManager.PERMISSION_GRANTED) {

            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.GET_ACCOUNTS}, 111);
            return;
        }*/
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        switch (requestCode) {
            case 111:
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {

                }
                break;
        }
    }


    private void googleLoginMethod() {
        GoogleSignInOptions gso = new GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                .requestProfile()
                .requestEmail()
                .build();

        // Build a GoogleSignInClient with the options specified by gso.
        if (Constants.mGoogleSignInClient != null) {
            Constants.mGoogleSignInClient = null;
        }
        Constants.mGoogleSignInClient = GoogleSignIn.getClient(LoginActivity.this, gso);


        mActivityLoginBinding.llGoogle.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                LoginManager.getInstance().logOut();
                if (Constants.mGoogleSignInClient != null) {
                    Constants.mGoogleSignInClient.signOut();
                }
                assert Constants.mGoogleSignInClient != null;
                Intent signInIntent = Constants.mGoogleSignInClient.getSignInIntent();
                startActivityForResult(signInIntent, RC_SIGN_IN);
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
                                            String firstName = "";
                                            String lastName = "";
                                            URL imageURL = new URL("https://graph.facebook.com/" + facebook_id + "/picture?type=large");
                                            System.out.println("fbresponse : imageURL : " + imageURL.toString());
                                            try {
                                                if (name.contains(" ")) {
                                                    String[] FirstLastName = name.split(" ");
                                                    firstName = FirstLastName[0];
                                                    lastName = FirstLastName[1];
                                                } else {
                                                    firstName = name;
                                                }
                                                // facebookUserLogin(facebook_id, FirstLastName[0], FirstLastName[1], email, imageURL.toString());
                                                mSharedPreferenceManager.storeUserProfileDetail(firstName + "" + lastName, email, "", imageURL.toString(), "");
                                                //  String birthday = object.getString("birthday"); // 01/31/1980 format
                                            }catch (Exception e){
                                                e.printStackTrace();
                                            }

                                            requestSocialLogin("", facebook_id, email, firstName, lastName, "", imageURL.toString());

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
                        Constants.showToastInMiddle(getApplicationContext(),  getResources().getString(R.string.error_msg_login_cancelled));
                        //Toast.makeText(LoginActivity.this, "Login Cancel", Toast.LENGTH_LONG).show();
                    }

                    @Override
                    public void onError(FacebookException exception) {
                        Constants.showToastInMiddle(getApplicationContext(), exception.getMessage());

                        // Toast.makeText(LoginActivity.this, exception.getMessage(), Toast.LENGTH_LONG).show();
                    }
                });

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

    private void handleSignInResult(GoogleSignInResult result) {
        if (result.isSuccess()) {
            System.out.println("Rahul : GoogleSignInAccount : 1 : " + new Gson().toJson(result));
            System.out.println("Rahul : handleSignInResult : name :  1 :  " + result.getSignInAccount().getDisplayName());
            System.out.println("Rahul : handleSignInResult : getDisplayName :  1 :  " + result.getSignInAccount().getEmail());
            System.out.println("Rahul : handleSignInResult : getEmail :  1 :  " + result.getSignInAccount().getPhotoUrl());

        } else {
            Constants.showToastInMiddle(getApplicationContext(), "Sign in cancel");

            // Toast.makeText(getApplicationContext(), "Sign in cancel", Toast.LENGTH_LONG).show();
        }
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
                        //Toast.makeText(getApplicationContext(), "Login Cancelled", Toast.LENGTH_SHORT).show();
                    }
                }
            });

        } catch (ApiException e) {
            // The ApiException status code indicates the detailed failure reason.
            // Please refer to the GoogleSignInStatusCodes class reference for more information.
            Log.w(TAG, "signInResult:failed code=" + e.getStatusCode());
            Constants.showToastInMiddle(getApplicationContext(),  getResources().getString(R.string.error_msg_login_cancelled));
            // Toast.makeText(getApplicationContext(), "Login Cancelled", Toast.LENGTH_SHORT).show();
            //updateUI(null);
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
            case R.id.btnSignin:
               /* Intent i = new Intent(this, MainActivityNew.class);
                startActivity(i);*/
                loginValidity();
                // requestLogin();
                break;
            case R.id.btnGuest:
                Intent i = new Intent(LoginActivity.this, IntroStepOne.class);
                i.putExtra("from","guest");
                startActivity(i);
                finish();
                break;
            case R.id.tvForgetPassword:
                Intent i1 = new Intent(this, ForgetPassword.class);
                startActivity(i1);
                break;
            case R.id.tvSignUp:
                Intent i2 = new Intent(this, RegisterActivity.class);
                i2.putExtra("from_where", navigateTo);
                startActivity(i2);
                break;
            case R.id.llFacebook:
                LoginManager.getInstance().logInWithReadPermissions(LoginActivity.this, Arrays.asList("public_profile", "email"));
                if (Constants.mGoogleSignInClient != null) {
                    Constants.mGoogleSignInClient.signOut();
                }
                break;
        }
    }

    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {

    }

    private void loginValidity() {
        String email_mobile = mActivityLoginBinding.edtUsername.getText().toString().trim();
        String password = mActivityLoginBinding.edtPassword.getText().toString().trim();
             /*   if ("".equals(email_mobile) && "".equals(password)) {
                    System.out.println("Rahul : btnContinue : validations 2");
                    mLoginBinding.contentLogin.edtEmailMobile.setError(getString(R.string.login_field_error));
                    Toast.makeText(getApplicationContext(),getString(R.string.login_password_error),Toast.LENGTH_SHORT).show();
                } else */
        if ("".equals(email_mobile)) {
            System.out.println("Rahul : loginValidity : validations 3");
            mActivityLoginBinding.tilUsername.setError(getResources().getString(R.string.error_msg_your_email_is_empty));
        } else if (!Constants.emailPatternValidtion(email_mobile)) {
            System.out.println("Rahul : loginValidity : validations 5");
            mActivityLoginBinding.tilUsername.setError(getString(R.string.login_field_error));
        } else if ("".equals(password)) {
            System.out.println("Rahul : loginValidity : validations 4");
            // Constants.showToastInMiddle(getApplicationContext(), getString(R.string.login_password_error));
            mActivityLoginBinding.tilPassword.setError(getString(R.string.login_password_error));
            //Toast.makeText(getApplicationContext(), getString(R.string.login_password_error), Toast.LENGTH_SHORT).show();
        } else {
            try {
                requestLogin();
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }


    private void EditTextCheckValidate() {
        mActivityLoginBinding.edtUsername.addTextChangedListener(new TextWatcher() {
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
                    mActivityLoginBinding.edtUsername.setText(result);
                    mActivityLoginBinding.edtUsername.setSelection(result.length());
                    // alert the user
                }
                mActivityLoginBinding.tilUsername.setError(null);
//                if (s.length() > layout_inputName.getCounterMaxLength())
//                    layout_inputName.setError("Please enter name ");
//                else
//                    layout_inputName.setError(null);

            }
        });

        mActivityLoginBinding.edtPassword.addTextChangedListener(new TextWatcher() {
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
                    mActivityLoginBinding.edtPassword.setText(result);
                    mActivityLoginBinding.edtPassword.setSelection(result.length());
                    // alert the user
                }
                mActivityLoginBinding.tilUsername.setError(null);
//
//                if (s.length() > layout_email.getCounterMaxLength())
//                    layout_email.setError("Please enter valid email ");
//                else
//                    layout_email.setError(null);

            }
        });
    }


    public void requestLogin() throws JSONException {
        if (Constants.isInternetConnected(LoginActivity.this)) {


            mActivityLoginBinding.progressSpinKitView.setVisibility(View.VISIBLE);
            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());

            JSONObject mJsonObject = new JSONObject();
            mJsonObject.put("user_mail", mActivityLoginBinding.edtUsername.getText().toString().toLowerCase().trim());
            mJsonObject.put("user_password", mActivityLoginBinding.edtPassword.getText().toString());
            System.out.println("Rahul : LoginActivity : requestLogin : " + mJsonObject);
            JsonObjectRequest mJsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                    Constants.BASE_URL + Constants.API_METHODS.LOGIN, mJsonObject,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            System.out.println("Rahul : LoginActivity : requestLogin : response: " + response);
                            mActivityLoginBinding.progressSpinKitView.setVisibility(View.GONE);
                            Gson gson = new Gson();
                            LoginModel mLoginModel = gson.fromJson(response.toString(), LoginModel.class);

                            if (mLoginModel != null) {
                                if (mLoginModel.getStatus() == Integer.parseInt(Constants.VARIABLES.STATUS_SUCESS_CODE)) {

                                    SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
                                    mSharedPreferenceManager.storeUserProfileDetail(mLoginModel.getData().getFirstName() + " " + mLoginModel.getData().getLastName(), mLoginModel.getData().getEmail(), mLoginModel.getData().getPhone(), "", mLoginModel.getData().getToken());


                                    switch (navigateTo) {
                                        case "MyCart": {
                                            Intent i = new Intent(LoginActivity.this, MyCart.class);
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
                                            Intent i = new Intent(LoginActivity.this, SubstituteActivity.class);
                                            i.putExtra("pushOrderID", getIntent().getExtras().getString("pushOrderID"));
                                            startActivity(i);
                                            break;
                                        }
                                        case "home": {
                                            Intent i = new Intent(LoginActivity.this, MainActivityNew.class);
                                            startActivity(i);
                                            finish();
                                            break;
                                        }
                                        default:
                                            if (mSharedPreferenceManager.getLatitude() != null && !mSharedPreferenceManager.getLatitude().isEmpty() && mSharedPreferenceManager.getLongitude() != null && !mSharedPreferenceManager.getLongitude().isEmpty()) {
                                                Intent i = new Intent(LoginActivity.this, SelectCategory.class);
                                                i.putExtra("latitude", mSharedPreferenceManager.getLatitude());
                                                i.putExtra("longitude", mSharedPreferenceManager.getLongitude());
                                                i.putExtra("select_category_list","");
                                                i.putExtra("from_where","start");
                                                startActivity(i);
                                                finish();
                                            } else {
                                                Intent i = new Intent(LoginActivity.this, IntroStepOne.class);
                                                i.putExtra("from","start");
                                                startActivity(i);
                                                finish();
                                            }

                                            break;
                                    }


                                } else {

                                    new AlertDialog.Builder(LoginActivity.this)
                                            .setTitle("Login")
                                            .setMessage(mLoginModel.getMessage())

                                            // Specifying a listener allows you to take an action before dismissing the dialog.
                                            // The dialog is automatically dismissed when a dialog button is clicked.
                                            .setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() {
                                                public void onClick(DialogInterface dialog, int which) {
                                                    dialog.dismiss();
                                                }
                                            })

                                            // A null listener allows the button to dismiss the dialog and take no further action.
                                            //.setNegativeButton(android.R.string.no, null)
                                            .setIcon(android.R.drawable.ic_dialog_alert)
                                            .show();


                                    //   Constants.showToastInMiddle(getApplicationContext(), mLoginModel.getMessage());
                                    // Toast.makeText(getApplicationContext(), mLoginModel.getMessage(), Toast.LENGTH_LONG).show();
                                }

                            } else {
                                Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.enter_valid_credentials));
                                //Toast.makeText(getApplicationContext(), "Enter Valid Credentials", Toast.LENGTH_LONG).show();
                            }
                        }
                    }, new Response.ErrorListener() {

                @Override
                public void onErrorResponse(VolleyError error) {
                    mActivityLoginBinding.progressSpinKitView.setVisibility(View.GONE);
                    System.out.println("Rahul : LoginActivity : requestLogin : VolleyError : " + error.toString());
                    Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.enter_valid_credentials));

                    //Toast.makeText(getApplicationContext(), "Enter Valid Credentials", Toast.LENGTH_LONG).show();
                }
            }) {
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
        } else {
            Constants.setSnackBar(this.findViewById(android.R.id.content).getRootView(), getResources().getString(R.string.no_connection));
        }
    }

    public void requestSocialLogin(String argGoogleLoginId, String argFbLoginId, String argUserEmail,
                                   String argFName, String argLName, String argPhone, String argImageName) throws JSONException {
        mActivityLoginBinding.progressSpinKitView.setVisibility(View.VISIBLE);
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
                        mActivityLoginBinding.progressSpinKitView.setVisibility(View.GONE);
                        Gson gson = new Gson();
                        LoginModel mLoginModel = gson.fromJson(response.toString(), LoginModel.class);

                        if (mLoginModel != null) {
                            if (mLoginModel.getStatus() == Integer.parseInt(Constants.VARIABLES.STATUS_SUCESS_CODE)) {

                                SharedPreferenceManager mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
                                mSharedPreferenceManager.storeUserProfileDetail(mLoginModel.getData().getFirstName() + " " + mLoginModel.getData().getLastName(), mLoginModel.getData().getEmail(), mLoginModel.getData().getPhone(), "", mLoginModel.getData().getToken());
                                switch (navigateTo) {
                                    case "MyCart": {
                                        Intent i = new Intent(LoginActivity.this, MyCart.class);
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
                                        Intent i = new Intent(LoginActivity.this, SubstituteActivity.class);
                                        i.putExtra("pushOrderID", getIntent().getExtras().getString("pushOrderID"));
                                        startActivity(i);
                                        break;
                                    }
                                    case "home": {
                                        Intent i = new Intent(LoginActivity.this, MainActivityNew.class);
                                        startActivity(i);
                                        finish();
                                        break;
                                    }
                                    default:
                                        if (mSharedPreferenceManager.getLatitude() != null && !mSharedPreferenceManager.getLatitude().isEmpty() && mSharedPreferenceManager.getLongitude() != null && !mSharedPreferenceManager.getLongitude().isEmpty()) {
                                            Intent i = new Intent(LoginActivity.this, SelectCategory.class);
                                            i.putExtra("latitude", mSharedPreferenceManager.getLatitude());
                                            i.putExtra("longitude", mSharedPreferenceManager.getLongitude());
                                            i.putExtra("select_category_list","");
                                            i.putExtra("from_where","start");
                                            startActivity(i);

                                            finish();
                                        } else {
                                            Intent i = new Intent(LoginActivity.this, IntroStepOne.class);
                                            i.putExtra("from","start");
                                            startActivity(i);
                                            finish();
                                        }
                                        break;
                                }

                            } else {
                                try {
                                    String message = response.getString("message");
                                    new AlertDialog.Builder(LoginActivity.this)
                                            .setTitle(getResources().getString(R.string.login))
                                            .setMessage(message)

                                            // Specifying a listener allows you to take an action before dismissing the dialog.
                                            // The dialog is automatically dismissed when a dialog button is clicked.
                                            .setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() {
                                                public void onClick(DialogInterface dialog, int which) {
                                                    dialog.dismiss();
                                                }
                                            })

                                            // A null listener allows the button to dismiss the dialog and take no further action.
                                            //.setNegativeButton(android.R.string.no, null)
                                            .setIcon(android.R.drawable.ic_dialog_alert)
                                            .show();
                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }


                                //  Constants.showToastInMiddle(getApplicationContext(), mLoginModel.getMessage());

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
                mActivityLoginBinding.progressSpinKitView.setVisibility(View.GONE);
                System.out.println("Rahul : LoginActivity : requestSocialLogin : VolleyError : " + error.toString());
                Constants.showToastInMiddle(getApplicationContext(), getResources().getString(R.string.enter_valid_credentials));

                //Toast.makeText(getApplicationContext(), "Enter Valid Credentials", Toast.LENGTH_LONG).show();
            }
        }) {
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


    private void getFcmToken() {
        FirebaseInstanceId.getInstance().getInstanceId()
                .addOnCompleteListener(new OnCompleteListener<InstanceIdResult>() {
                    @Override
                    public void onComplete(@NonNull Task<InstanceIdResult> task) {
                        if (!task.isSuccessful()) {
//                            Log.w(TAG, "getInstanceId failed", task.getException());
                            return;
                        }

                        // Get new Instance ID token
                        String token = task.getResult().getToken();
                        mSharedPreferenceManager.saveDevKey(token);
                        Log.e(TAG, token.toString());
                        // Log and toast
//            String msg = getString(R.string.msg_token_fmt, token);
//            Log.d(TAG, msg);
//            Toast.makeText(SplashScreenActivity.this, msg, Toast.LENGTH_SHORT).show();
                    }
                });
    }


    @Override
    public void onBackPressed() {

    }
}
