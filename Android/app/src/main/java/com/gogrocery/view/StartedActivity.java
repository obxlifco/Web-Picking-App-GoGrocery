package com.gogrocery.view;

import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowManager;
import android.widget.ImageView;
import android.widget.TextView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.engine.DiskCacheStrategy;
import com.bumptech.glide.request.RequestOptions;
import com.gogrocery.Adapters.ImageSliderAdapter;
import com.gogrocery.Models.StartedSliderModel.StartedModel;
import com.gogrocery.R;
import com.gogrocery.databinding.ActivityStartedBinding;
import com.smarteist.autoimageslider.IndicatorAnimations;
import com.smarteist.autoimageslider.SliderAnimations;
import com.smarteist.autoimageslider.SliderView;
import com.smarteist.autoimageslider.SliderViewAdapter;

import java.util.ArrayList;
import java.util.List;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.databinding.DataBindingUtil;
import androidx.fragment.app.Fragment;

public class StartedActivity extends AppCompatActivity {
    ActivityStartedBinding activityStartedBinding;
    ArrayList<StartedModel> startedModelArrayList=new ArrayList<>();
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        activityStartedBinding = DataBindingUtil.setContentView(this, R.layout.activity_started);

      initImageSlider();
      hideStatusBarColor();

        activityStartedBinding.btnGetStarted.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(StartedActivity.this, LoginActivity.class);
                startActivity(i);
                finish();
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

    private void initImageSlider() {
        activityStartedBinding.imageSliderGetStarted.setSliderAdapter(new ImageSliderAdapter(StartedActivity.this));

        activityStartedBinding.imageSliderGetStarted.setIndicatorAnimation(IndicatorAnimations.SWAP); //set indicator animation by using 	  SliderLayout.IndicatorAnimations. :WORM or THIN_WORM or COLOR or DROP or FILL or NONE or SCALE or SCALE_DOWN or SLIDE and SWAP!!
        activityStartedBinding.imageSliderGetStarted.setSliderTransformAnimation(SliderAnimations.SIMPLETRANSFORMATION);
        activityStartedBinding.imageSliderGetStarted.setIndicatorSelectedColor(Color.GRAY);
        activityStartedBinding.imageSliderGetStarted.setIndicatorUnselectedColor(Color.parseColor("#E3E9F2"));
        //imageSlider.setAutoCycleDirection(SliderView.AUTO_CYCLE_DIRECTION_BACK_AND_FORTH);
/*        activityStartedBinding.imageSliderGetStarted.setScrollTimeInSec(5); //set scroll delay in seconds :
        activityStartedBinding.imageSliderGetStarted.startAutoCycle();*/


    }

/*    private void setupSlider() {
        startedModelArrayList.add(new StartedModel(getResources().getString(R.string.txtStartedOneHeader),getResources().getString(R.string.txtStartedOneDesc),R.drawable.anim_rabbitscene1));
        startedModelArrayList.add(new StartedModel(getResources().getString(R.string.txtStartedTwoHeader),getResources().getString(R.string.txtStartedTwoDesc),R.drawable.anim_rabbitscene2));
        startedModelArrayList.add(new StartedModel(getResources().getString(R.string.txtStartedThreeHeader),getResources().getString(R.string.txtStartedThreeDesc),R.drawable.anim_rabbitscene3));
        SliderAdapterExample mSliderAdapterExample = new SliderAdapterExample(getApplicationContext(), startedModelArrayList);
        activityStartedBinding.imageSliderGetStarted.setSliderAdapter(mSliderAdapterExample);

        //  mActivityMainBinding.appBarInclude.imageSlider.setIndicatorAnimation(0); //set indicator animation by using SliderLayout.IndicatorAnimations. :WORM or THIN_WORM or COLOR or DROP or FILL or NONE or SCALE or SCALE_DOWN or SLIDE and SWAP!!
        activityStartedBinding.imageSliderGetStarted.setSliderTransformAnimation(SliderAnimations.SIMPLETRANSFORMATION);
        //activityStartedBinding.imageSliderGetStarted.setAutoCycleDirection(SliderView.AUTO_CYCLE_DIRECTION_BACK_AND_FORTH);
        activityStartedBinding.imageSliderGetStarted.setIndicatorSelectedColor(Color.GRAY);
        activityStartedBinding.imageSliderGetStarted.setIndicatorUnselectedColor(Color.parseColor("#E3E9F2"));
        //activityStartedBinding.imageSliderGetStarted.setScrollTimeInSec(4); //set scroll delay in seconds :
        //activityStartedBinding.imageSliderGetStarted.startAutoCycle();
    }

    class SliderAdapterExample extends SliderViewAdapter<SliderAdapterExample.SliderAdapterVH> {

        private Context context;
        private ArrayList<StartedModel> imageSliderUrlList;

        public SliderAdapterExample(Context context, ArrayList<StartedModel> imageSliderUrlList) {
            this.context = context;
            this.imageSliderUrlList = imageSliderUrlList;
        }

        @Override
        public SliderAdapterVH onCreateViewHolder(ViewGroup parent) {
            View inflate = LayoutInflater.from(parent.getContext()).inflate(R.layout.started_image_slider_layout_item, null);
            return new SliderAdapterVH(inflate);
        }

        @Override
        public void onBindViewHolder(SliderAdapterExample.SliderAdapterVH viewHolder, int position) {
            try {
                System.out.println("Rahul : onBindViewHolder : imageSliderUrlList.get(position) : " + imageSliderUrlList.get(position));
                *//*Glide.with(viewHolder.itemView)
                        .load(imageSliderUrlList.get(position).getImg())
                        .apply(new RequestOptions().override(400, 400))
                        .diskCacheStrategy(DiskCacheStrategy.NONE).skipMemoryCache(true)
                        .into(viewHolder.imageViewBackground);*//*

                viewHolder.imageViewBackground.setImageResource(imageSliderUrlList.get(position).getImg());
                viewHolder.tv_Header.setText(imageSliderUrlList.get(position).getHeader());
                viewHolder.tv_Description.setText(imageSliderUrlList.get(position).getDescription());

            } catch (java.lang.NullPointerException ex) {

            }

        }

        @Override
        public int getCount() {
            //slider view count could be dynamic size

            try {
                return imageSliderUrlList.size();

            } catch (java.lang.NullPointerException ex) {
                return 0;
            }
        }

        class SliderAdapterVH extends SliderViewAdapter.ViewHolder {

            View itemView;
            ImageView imageViewBackground;
            TextView tv_Header,tv_Description;

            public SliderAdapterVH(View itemView) {
                super(itemView);
                imageViewBackground = itemView.findViewById(R.id.iv_auto_image_slider);
                tv_Header = itemView.findViewById(R.id.tv_header);
                tv_Description = itemView.findViewById(R.id.tv_description);
                this.itemView = itemView;
            }
        }
        private void loadFragment(Fragment fragment) {

        }

    }*/
}
