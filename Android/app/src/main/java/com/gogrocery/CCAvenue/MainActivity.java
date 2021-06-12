package com.gogrocery.CCAvenue;

import android.app.DatePickerDialog;
import android.content.Intent;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;
import android.widget.Toast;

import com.gogrocery.Constants.Constants;
import com.google.gson.Gson;

import net.cachapa.expandablelayout.ExpandableLayout;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Locale;
import java.util.Random;
import com.gogrocery.R;

import mumbai.dev.sdkdubai.BillingAddress;
import mumbai.dev.sdkdubai.CustomModel;
import mumbai.dev.sdkdubai.MerchantDetails;
import mumbai.dev.sdkdubai.PaymentOptions;
import mumbai.dev.sdkdubai.ShippingAddress;
import mumbai.dev.sdkdubai.StandardInstructions;

public class MainActivity extends AppCompatActivity implements View.OnClickListener,CustomModel.OnCustomStateListener/*, responseinterface*/ {
    ExpandableLayout exp_merchant_details, exp_billing_address, exp_shipping_address, exp_standard_instructions;

    Button btn_billing_address, btn_merchant_details, btn_shipping_address,btn_standard_instructions,sdk;
    EditText ed_access_code,ed_merchant_id,ed_currency,ed_amount,ed_redirect_url,ed_cancel_url,ed_rsa_url,ed_customer_id,ed_order_id,ed_promo_code;
    EditText ed_address_b,ed_name_b,ed_country_b,ed_state_b,ed_city_b,ed_telephone_b,ed_email_b;
    EditText ed_address_s,ed_name_s,ed_country_s,ed_state_s,ed_city_s,ed_telephone_s,ed_email_s,ed_add1,ed_add2,ed_add3,ed_add4,ed_add5;
    CheckBox chk_show,chk_ccPromo/*,chk_validate*/;
    LinearLayout layout_si_content,layout_start_date,layout_si_ref_no,layout_si_setup_amt,layout_si_amt,layout_si_freq_type,layout_si_frequency,layout_si_bill_cycle;
    TextView start_date;

    RadioGroup radioGroup_si_type,radioGroup_setup_amt,radioGroup_freq_type;
    RadioButton radio_btn_fixed,radio_btn_ondemand,radio_btn_none,radio_btn_yes,radio_btn_no,radio_btn_days,radio_btn_month,radio_btn_year;
    EditText ed_si_ref_no,ed_si_amount,ed_si_freq,ed_bill_cycle;

    Calendar myCalendar = Calendar.getInstance();
    String myFormat = "dd-MM-yyyy"; //In which you need put here
    SimpleDateFormat sdf = new SimpleDateFormat(myFormat, Locale.US);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_ccavenue);

        CustomModel.getInstance().setListener(this);
        ed_address_s = (EditText) findViewById(R.id.ed_address_s);
        ed_name_s = (EditText) findViewById(R.id.ed_name_s);
        ed_country_s = (EditText) findViewById(R.id.ed_country_s);
        ed_state_s = (EditText) findViewById(R.id.ed_state_s);
        ed_city_s = (EditText) findViewById(R.id.ed_city_s);

        ed_telephone_s = (EditText) findViewById(R.id.ed_telephone_s);
        ed_email_s = (EditText) findViewById(R.id.ed_email_s);



        ed_address_b = (EditText) findViewById(R.id.ed_address_b);
        ed_name_b = (EditText) findViewById(R.id.ed_name_b);
        ed_country_b = (EditText) findViewById(R.id.ed_country_b);
        ed_state_b = (EditText) findViewById(R.id.ed_state_b);
        ed_city_b = (EditText) findViewById(R.id.ed_city_b);

        ed_telephone_b = (EditText) findViewById(R.id.ed_telephone_b);
        ed_email_b = (EditText) findViewById(R.id.ed_email_b);

        ed_access_code = (EditText) findViewById(R.id.ed_access_code);
        ed_merchant_id = (EditText) findViewById(R.id.ed_merchant_id);
        ed_currency = (EditText) findViewById(R.id.ed_currency);
        ed_order_id = (EditText) findViewById(R.id.ed_order_id);
        ed_amount = (EditText) findViewById(R.id.ed_amount);
        ed_redirect_url = (EditText) findViewById(R.id.ed_redirect_url);
        ed_cancel_url = (EditText) findViewById(R.id.ed_cancel_url);
        ed_rsa_url = (EditText) findViewById(R.id.ed_rsa_url);
        ed_customer_id = (EditText) findViewById(R.id.ed_customer_id);
        ed_promo_code = (EditText) findViewById(R.id.ed_promo_code);

        ed_add1 = (EditText) findViewById(R.id.ed_add1);
        ed_add2 = (EditText) findViewById(R.id.ed_add2);
        ed_add3 = (EditText) findViewById(R.id.ed_add3);
        ed_add4 = (EditText) findViewById(R.id.ed_add4);
        ed_add5 = (EditText) findViewById(R.id.ed_add5);

        ed_si_ref_no = (EditText) findViewById(R.id.ed_ref_no);
        ed_si_amount = (EditText) findViewById(R.id.ed_si_amount);
        ed_si_freq = (EditText) findViewById(R.id.ed_si_freq);
        ed_bill_cycle = (EditText) findViewById(R.id.ed_bill_cycle);

        chk_show= (CheckBox) findViewById(R.id.chk_show);
        chk_ccPromo= (CheckBox) findViewById(R.id.chk_ccPromo);

        sdk = (Button) findViewById(R.id.sdk);
        btn_merchant_details = (Button) findViewById(R.id.btn_merchant_details);
        btn_billing_address = (Button) findViewById(R.id.btn_billing_address);
        btn_shipping_address = (Button) findViewById(R.id.btn_shipping_address);
        btn_standard_instructions = (Button) findViewById(R.id.btn_standard_instructions);

        exp_merchant_details = (ExpandableLayout) findViewById(R.id.exp_merchant_details);
        exp_billing_address = (ExpandableLayout) findViewById(R.id.exp_billing_address);
        exp_shipping_address = (ExpandableLayout) findViewById(R.id.exp_shipping_address);
        exp_standard_instructions = (ExpandableLayout) findViewById(R.id.exp_standard_instructions);

        layout_si_content = (LinearLayout)findViewById(R.id.layout_si_content);
        layout_si_setup_amt = (LinearLayout)findViewById(R.id.layout_setup_amt);
        layout_si_ref_no = (LinearLayout)findViewById(R.id.layout_si_ref_no);
        layout_start_date = (LinearLayout)findViewById(R.id.layout_select_date);
        layout_si_amt = (LinearLayout)findViewById(R.id.layout_amt);
        layout_si_freq_type = (LinearLayout)findViewById(R.id.layout_freq_type);
        layout_si_frequency = (LinearLayout)findViewById(R.id.layout_si_frequency);
        layout_si_bill_cycle = (LinearLayout)findViewById(R.id.layout_si_bill_cycle);

        start_date = (TextView) findViewById(R.id.txt_start_date) ;

        radioGroup_si_type = (RadioGroup) findViewById(R.id.radio_grp_si_type) ;
        radioGroup_setup_amt = (RadioGroup) findViewById(R.id.radio_grp_setup_amt) ;
        radioGroup_freq_type = (RadioGroup) findViewById(R.id.radio_grp_freq_type) ;

        radio_btn_fixed = (RadioButton) findViewById(R.id.radio_fixed);
        radio_btn_ondemand = (RadioButton) findViewById(R.id.radio_on_demand);
        radio_btn_none = (RadioButton) findViewById(R.id.radio_none);
        radio_btn_yes = (RadioButton) findViewById(R.id.radio_yes);
        radio_btn_no = (RadioButton) findViewById(R.id.radio_no);
        radio_btn_days = (RadioButton) findViewById(R.id.radio_days);
        radio_btn_month = (RadioButton) findViewById(R.id.radio_month);
        radio_btn_year = (RadioButton) findViewById(R.id.radio_year);


        btn_merchant_details.setOnClickListener(this);
        btn_billing_address.setOnClickListener(this);
        btn_shipping_address.setOnClickListener(this);
        btn_standard_instructions.setOnClickListener(this);
        sdk.setOnClickListener(this);
        chk_ccPromo.setOnClickListener(this);

        layout_start_date.setOnClickListener(this);
        radio_btn_fixed.setOnClickListener(this);
        radio_btn_ondemand.setOnClickListener(this);
        radio_btn_none.setOnClickListener(this);
        radio_btn_days.setOnClickListener(this);
        radio_btn_month.setOnClickListener(this);
        radio_btn_year.setOnClickListener(this);


      /*
        chk_validate.setOnClickListener(this);*/

       /* Intent intent=getIntent();
        BillingAddress searchRequest = (BillingAddress) intent.getParcelableExtra("billing");

        String aa= searchRequest.getCity();
        int a=1;
        a=a*2;*/
        Log.d("CCA RSA","Hiii");

    }

    @Override
    protected void onStart() {
        super.onStart();

        Integer randomNum = randInt(0, 9999999);

        ed_order_id.setText(randomNum.toString());
    }

    @Override
    public void onClick(View v) {

        int id = v.getId();

        if(id== R.id.sdk)
        {

            MerchantDetails m= new MerchantDetails();
            m.setAccess_code("AVUP03GL28CI81PUIC");
            m.setMerchant_id("45990");
            m.setCurrency(Constants.VARIABLES.CURRENT_CURRENCY);
            m.setAmount("1.00");
            m.setRedirect_url("https://www.gogrocery.ae/api/front/v1/payment-res/");
            m.setCancel_url("https://www.gogrocery.ae/api/front/v1/payment-res/");
            m.setRsa_url("https://www.gogrocery.ae/api/front/v1/get-rsa/");
            m.setOrder_id("960");
            m.setCustomer_id("50000960");
            m.setShow_addr(false);
            m.setCCAvenue_promo(false);
            m.setPromo_code("");
            m.setAdd1("");
            m.setAdd2("");
            m.setAdd3("");
            m.setAdd4("");
            m.setAdd5("");

            BillingAddress b =new BillingAddress();
            b.setName(ed_name_b.getText().toString().trim());
            b.setAddress(ed_address_b.getText().toString().trim());
            b.setCountry(ed_country_b.getText().toString().trim());
            b.setState(ed_state_b.getText().toString().trim());
            b.setCity(ed_city_b.getText().toString().trim());

            b.setTelephone(ed_telephone_b.getText().toString().trim());
            b.setEmail(ed_email_b.getText().toString().trim());


            ShippingAddress s =new ShippingAddress();
            s.setName(ed_name_s.getText().toString().trim());
            s.setAddress(ed_address_s.getText().toString().trim());
            s.setCountry(ed_country_s.getText().toString().trim());
            s.setState(ed_state_s.getText().toString().trim());
            s.setCity(ed_city_s.getText().toString().trim());

            s.setTelephone(ed_telephone_s.getText().toString().trim());


            if(chk_ccPromo.isChecked())
                m.setCCAvenue_promo(true);
            else
                m.setCCAvenue_promo(false);

            if(chk_show.isChecked())
                m.setShow_addr(true);
            else
                m.setShow_addr(false);


            // SI data //
            StandardInstructions si = new StandardInstructions();

            String setup_amt ="";
            int selected_setup_amt = radioGroup_setup_amt.getCheckedRadioButtonId();
            if (selected_setup_amt == R.id.radio_yes){
                setup_amt = "Y";
            }else if (selected_setup_amt == R.id.radio_no) {
                setup_amt = "N";
            }

            String freq_type = "";
            int selected_freq_type = radioGroup_freq_type.getCheckedRadioButtonId();
            if (selected_freq_type == R.id.radio_days){
                freq_type = "days";
            }else if (selected_freq_type == R.id.radio_month){
                freq_type = "month";
            }else if (selected_freq_type == R.id.radio_year){
                freq_type = "year";
            }

            String si_type = "";
            int selected_si_type = radioGroup_si_type.getCheckedRadioButtonId();
            if (selected_si_type == R.id.radio_fixed){
                si_type = "FIXED";
                if (!setup_amt.equals("") && !ed_si_amount.getText().toString().equals("")
                        && !start_date.getText().toString().equals("") && !ed_si_freq.getText().toString().equals("")
                        && !ed_bill_cycle.getText().toString().equals("") && !freq_type.equals("")){

                    si.setSi_type(si_type);
                    si.setSi_mer_ref_no(ed_si_ref_no.getText().toString());
                    si.setSi_is_setup_amt(setup_amt);
                    si.setSi_amount(ed_si_amount.getText().toString());
                    si.setSi_start_date(start_date.getText().toString());
                    si.setSi_frequency_type(freq_type);
                    si.setSi_frequency(ed_si_freq.getText().toString());
                    si.setSi_bill_cycle(ed_bill_cycle.getText().toString());
                    System.out.println("Rahul : Fingureprint_login : onClick : 1 : ");
                    Intent i =new Intent(MainActivity.this,PaymentOptions.class);
                    //Intent i =new Intent(Fingureprint_login.this,PaymentOptionsPage.class);
                    // Intent i =new Intent(Fingureprint_login.this,PaymentDetails.class);
                    i.putExtra("merchant",m);
                    i.putExtra("billing",b);
                    i.putExtra("shipping",s);
                    i.putExtra("standard instructions", si);
                    startActivity(i);

                }else {
                    Toast.makeText(this, "SI Parameters missing", Toast.LENGTH_SHORT).show();
                }

            }else if (selected_si_type == R.id.radio_on_demand){
                si_type = "ONDEMAND";
                if (!start_date.getText().toString().equals("") && !setup_amt.equals("")){

                    si.setSi_type(si_type);
                    si.setSi_mer_ref_no(ed_si_ref_no.getText().toString());
                    si.setSi_is_setup_amt(setup_amt);
                    si.setSi_start_date(start_date.getText().toString());
                    System.out.println("Rahul : Fingureprint_login : onClick : 2 : ");
                    Intent i =new Intent(MainActivity.this,PaymentOptions.class);
                    //Intent i =new Intent(Fingureprint_login.this,PaymentOptionsPage.class);
                    // Intent i =new Intent(Fingureprint_login.this,PaymentDetails.class);
                    i.putExtra("merchant",m);
                    i.putExtra("billing",b);
                    i.putExtra("shipping",s);
                    i.putExtra("standard instructions", si);
                    startActivity(i);

                }else {
                    Toast.makeText(this, "SI Parameters missing", Toast.LENGTH_SHORT).show();
                }
            }else {

                si.setSi_type("");
                System.out.println("Rahul : Fingureprint_login : onClick : 3 : ");
                Intent i =new Intent(MainActivity.this,PaymentOptions.class);
                //Intent i =new Intent(Fingureprint_login.this,PaymentOptionsPage.class);
                // Intent i =new Intent(Fingureprint_login.this,PaymentDetails.class);
                i.putExtra("merchant",m);
                i.putExtra("billing",b);
                i.putExtra("shipping",s);
                i.putExtra("standard instructions", si);
                startActivity(i);
            }
            Gson mGson=new Gson();
            System.out.println("Rahul : PaymentOptionsAvailable : setCCAvenueInitialDetails : MerchantDetails : " + mGson.toJson(m));
            System.out.println("Rahul : PaymentOptionsAvailable : setCCAvenueInitialDetails : BillingAddress : " + mGson.toJson(b));
            System.out.println("Rahul : PaymentOptionsAvailable : setCCAvenueInitialDetails : ShippingAddress : " + mGson.toJson(s));
            System.out.println("Rahul : PaymentOptionsAvailable : setCCAvenueInitialDetails : standard instructions : " + mGson.toJson(si));

        }


        else if (id == R.id.btn_merchant_details) {
            // toggle expand and collapse
            exp_merchant_details.toggle();


            if (exp_merchant_details.isExpanded()) {
                btn_merchant_details.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_more, 0);
            } else {
                btn_merchant_details.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_less, 0);
            }

            if (exp_billing_address.isExpanded()) {
                exp_billing_address.toggle();
                btn_billing_address.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_less, 0);
            }
            if (exp_shipping_address.isExpanded()) {
                exp_shipping_address.toggle();
                btn_shipping_address.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_less, 0);
            }

            if (exp_standard_instructions.isExpanded()) {
                exp_standard_instructions.toggle();
                btn_standard_instructions.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_less, 0);
            }

        }

        else if (id == R.id.btn_billing_address) {
            // toggle expand and collapse
            exp_billing_address.toggle();

            if (exp_billing_address.isExpanded()) {
                btn_billing_address.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_more, 0);
            } else {
                btn_billing_address.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_less, 0);
            }

            if (exp_merchant_details.isExpanded()) {
                exp_merchant_details.toggle();
                btn_merchant_details.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_less, 0);
            }

            if (exp_shipping_address.isExpanded()) {
                exp_shipping_address.toggle();
                btn_shipping_address.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_less, 0);
            }

            if (exp_standard_instructions.isExpanded()) {
                exp_standard_instructions.toggle();
                btn_standard_instructions.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_less, 0);
            }
        }




        else if (id == R.id.btn_shipping_address) {
            // toggle expand and collap6se
            exp_shipping_address.toggle();

            if (exp_shipping_address.isExpanded()) {
                btn_shipping_address.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_more, 0);
            } else {
                btn_shipping_address.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_less, 0);
            }

            if (exp_standard_instructions.isExpanded()) {
                exp_standard_instructions.toggle();
                btn_standard_instructions.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_less, 0);
            }

            if (exp_billing_address.isExpanded()) {
                exp_billing_address.toggle();
                btn_billing_address.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_less, 0);
            }

            if (exp_merchant_details.isExpanded()) {
                exp_merchant_details.toggle();
                btn_merchant_details.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_less, 0);
            }
        }

        else if (id == R.id.btn_standard_instructions) {
            // toggle expand and collapse
            exp_standard_instructions.toggle();

            if (exp_standard_instructions.isExpanded()) {
                btn_standard_instructions.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_more, 0);
            } else {
                btn_standard_instructions.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_less, 0);
            }

            if (exp_shipping_address.isExpanded()) {
                exp_shipping_address.toggle();
                btn_shipping_address.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_less, 0);
            }

            if (exp_billing_address.isExpanded()) {
                exp_billing_address.toggle();
                btn_billing_address.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_less, 0);
            }

            if (exp_merchant_details.isExpanded()) {
                exp_merchant_details.toggle();
                btn_merchant_details.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.mipmap.expand_less, 0);
            }
        }

        else if (id == R.id.layout_select_date) {

            new DatePickerDialog(MainActivity.this, date, myCalendar
                    .get(Calendar.YEAR), myCalendar.get(Calendar.MONTH),
                    myCalendar.get(Calendar.DAY_OF_MONTH)).show();
        }

        else if (id == R.id.radio_fixed) {

            layout_si_content.setVisibility(View.VISIBLE);

            ed_si_ref_no.setText("");
            ed_si_amount.setText("");
            start_date.setText("");
            ed_si_freq.setText("");
            ed_bill_cycle.setText("");
            radioGroup_freq_type.clearCheck();
            radioGroup_setup_amt.clearCheck();

            layout_si_amt.setVisibility(View.VISIBLE);
            layout_si_freq_type.setVisibility(View.VISIBLE);
            layout_si_frequency.setVisibility(View.VISIBLE);
            layout_si_bill_cycle.setVisibility(View.VISIBLE);

        }

        else if (id == R.id.radio_on_demand) {

            layout_si_content.setVisibility(View.VISIBLE);

            ed_si_ref_no.setText("");
            start_date.setText("");
            radioGroup_setup_amt.clearCheck();

            layout_si_amt.setVisibility(View.GONE);
            layout_si_freq_type.setVisibility(View.GONE);
            layout_si_frequency.setVisibility(View.GONE);
            layout_si_bill_cycle.setVisibility(View.GONE);

        }

        else if (id == R.id.radio_none) {

            layout_si_content.setVisibility(View.GONE);

            ed_si_ref_no.setText("");
            ed_si_amount.setText("");
            start_date.setText("");
            ed_si_freq.setText("");
            ed_bill_cycle.setText("");
            radioGroup_freq_type.clearCheck();
            radioGroup_setup_amt.clearCheck();

            layout_si_amt.setVisibility(View.GONE);
            layout_si_freq_type.setVisibility(View.GONE);
            layout_si_frequency.setVisibility(View.GONE);
            layout_si_bill_cycle.setVisibility(View.GONE);

        }
    }

    public static int randInt(int min, int max) {
        // Usually this should be a field rather than a method variable so
        // that it is not re-seeded every call.
        Random rand = new Random();

        // nextInt is normally exclusive of the top value,
        // so add 1 to make it inclusive
        int randomNum = rand.nextInt((max - min) + 1) + min;

        return randomNum;
    }


    @Override
    public void stateChanged() {
        String modelState = CustomModel.getInstance().getState();
        System.out.println("Rahul : Fingureprint_login : stateChanged : modelState : "+modelState);
       // System.out.println("Rahul : Fingureprint_login : stateChanged : modelState : "+new Gson().toJson(CustomModel.getInstance()));
        /*Intent intent = new Intent(getApplicationContext(), St.class);
        intent.putExtra("transStatus", modelState);
        startActivity(intent);*//**/
    }


    DatePickerDialog.OnDateSetListener date = new DatePickerDialog.OnDateSetListener() {

        @Override
        public void onDateSet(DatePicker view, int year, int monthOfYear,
                              int dayOfMonth) {
            // TODO Auto-generated method stub
            myCalendar.set(Calendar.YEAR, year);
            myCalendar.set(Calendar.MONTH, monthOfYear);
            myCalendar.set(Calendar.DAY_OF_MONTH, dayOfMonth);
            updateLabel();
        }

    };

    private void updateLabel() {
        String myFormat = "dd-MM-yyyy"; //In which you need put here
        SimpleDateFormat sdf = new SimpleDateFormat(myFormat, Locale.US);

        start_date.setText(sdf.format(myCalendar.getTime()));
        //dt = start_date.getText().toString();
    }
}
