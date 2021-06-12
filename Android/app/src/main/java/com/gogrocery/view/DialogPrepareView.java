package com.gogrocery.view;

import androidx.appcompat.app.AppCompatActivity;
import androidx.databinding.DataBindingUtil;
import androidx.recyclerview.widget.LinearLayoutManager;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.Toast;

import com.gogrocery.Adapters.MyAddressesAdapter;
import com.gogrocery.Adapters.PreparationAdapter;
import com.gogrocery.Interfaces.SelectPreparationValue;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityDialogPreparaViewBinding;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class DialogPrepareView extends AppCompatActivity implements SelectPreparationValue {
    View rootView;
    String preparationType = "";
    String preparationValue = "";
    String selectedPreparationValue = "";
    String argProductId = "";
    String arg_which = "";
    String position = "";
    ActivityDialogPreparaViewBinding prepareViewBinding;
    List<String> customFieldList = new ArrayList<>();
    PreparationAdapter preparationAdapter;

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
        prepareViewBinding = DataBindingUtil.setContentView(this, R.layout.activity_dialog_prepara_view);
        this.setFinishOnTouchOutside(true);
        rootView = this.findViewById(android.R.id.content).getRootView();
        preparationType = getIntent().getStringExtra("custom_field_name");
        preparationValue = getIntent().getStringExtra("custom_field_value");

        argProductId = getIntent().getStringExtra("product_id");
        arg_which = getIntent().getStringExtra("arg_which");
        position = getIntent().getStringExtra("position");
        if (preparationValue != null && !preparationValue.isEmpty() && !preparationType.isEmpty()) {
            prepareViewBinding.tvItemName.setText(preparationType);

            String[] customValue = preparationValue.split("##");

           customFieldList = new ArrayList<String>(Arrays.asList(customValue));
           /* for (String item : customValue) {
                customFieldList.add(item);
            }*/
           // customFieldList.addAll(Arrays.asList(customValue));
            preparationAdapter = new PreparationAdapter(DialogPrepareView.this, customFieldList, this);
            LinearLayoutManager mLayoutManager = new LinearLayoutManager(getApplicationContext(), LinearLayoutManager.VERTICAL, false);
            prepareViewBinding.rgPreparation.setLayoutManager(mLayoutManager);
            prepareViewBinding.rgPreparation.setAdapter(preparationAdapter);
            prepareViewBinding.rgPreparation.setNestedScrollingEnabled(false);

        }
        prepareViewBinding.btnApplyContinue.setOnClickListener(v -> {
            if (selectedPreparationValue != null && !selectedPreparationValue.isEmpty()) {
                Intent i = new Intent();
                i.putExtra("custom_field_name", preparationType);
                i.putExtra("custom_field_value", selectedPreparationValue);
                i.putExtra("argProductId", argProductId);
                i.putExtra("arg_which", arg_which);
                i.putExtra("position", position);
                setResult(Activity.RESULT_OK, i);
                finish();
            } else {
                Toast.makeText(getApplicationContext(), getResources().getString(R.string.error_msg_select_any_one_option), Toast.LENGTH_SHORT).show();
            }
        });

        prepareViewBinding.ivClose.setOnClickListener(v -> {
            finish();
        });
    }

    @Override
    public void selectedCustomFieldValue(String custom_field_value) {
        this.selectedPreparationValue = custom_field_value;
    }
}