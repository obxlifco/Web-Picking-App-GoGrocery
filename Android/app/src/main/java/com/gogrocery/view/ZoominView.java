package com.gogrocery.view;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;
import androidx.viewpager.widget.PagerAdapter;
import androidx.viewpager.widget.ViewPager;

import android.content.Context;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowManager;
import android.widget.ImageView;
import android.widget.LinearLayout;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.engine.DiskCacheStrategy;
import com.github.chrisbanes.photoview.PhotoView;
import com.gogrocery.Adapters.ImageSliderBannnerAdapter;
import com.gogrocery.R;


import java.util.ArrayList;
import java.util.List;

public class ZoominView extends AppCompatActivity {

    private List<String> imageSliderUrlList = new ArrayList<>();
    int dotscount;
     ImageView[] dots;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.setFinishOnTouchOutside(true);
        setContentView( R.layout.activity_zoomin_view);
        hideStatusBarColor();
        ViewPager viewPager = findViewById(R.id.view_pager);
        ImageView ivBtnClose = findViewById(R.id.ivBtnClose);
        LinearLayout mSliderDots = findViewById(R.id.SliderDots);
        imageSliderUrlList.clear();
        imageSliderUrlList = getIntent().getStringArrayListExtra("image_url_list");
        final SamplePagerAdapter mImageSliderBannnerAdapter = new SamplePagerAdapter(getApplicationContext(), imageSliderUrlList);

       viewPager.setAdapter(mImageSliderBannnerAdapter);


        dotscount = mImageSliderBannnerAdapter.getCount();
        dots = new ImageView[dotscount];


        for (int i = 0; i < dotscount; i++) {

            dots[i] = new ImageView(getApplicationContext());
            dots[i].setImageDrawable(ContextCompat.getDrawable(getApplicationContext(), R.drawable.detail_page_non_active_dots));

            LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT);

            params.setMargins(8, 0, 8, 0);

            if (dotscount > 1) {

               mSliderDots.addView(dots[i], params);
            }


        }


        if (dotscount > 0) {
            dots[0].setImageDrawable(ContextCompat.getDrawable(getApplicationContext(), R.drawable.detail_page_active_dots));
        }

      viewPager.addOnPageChangeListener(new ViewPager.OnPageChangeListener() {
            @Override
            public void onPageScrolled(int position, float positionOffset, int positionOffsetPixels) {

            }

            @Override
            public void onPageSelected(int position) {

                for (int i = 0; i < dotscount; i++) {
                    dots[i].setImageDrawable(ContextCompat.getDrawable(getApplicationContext(), R.drawable.detail_page_non_active_dots));
                }

                dots[position].setImageDrawable(ContextCompat.getDrawable(getApplicationContext(), R.drawable.detail_page_active_dots));

            }

            @Override
            public void onPageScrollStateChanged(int state) {

            }
        });






       ivBtnClose.setOnClickListener(v -> {
            finish();
        });
    }


    private void hideStatusBarColor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

            window.setStatusBarColor(getResources().getColor(R.color.colorPrimaryDark));
        }
    }

    @Override
    public void onResume() {
        super.onResume();
        Window window = this.getWindow();

        window.setLayout(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT);
       // window.setBackgroundDrawable(getResources().getDrawable(R.drawable.bg_dialog_fragment));

    }
    static class SamplePagerAdapter extends PagerAdapter {
        private Context context;
        private List<String> imageSliderUrlList;

        public SamplePagerAdapter(Context context, List<String> imageSliderUrlList) {
            this.context = context;
            this.imageSliderUrlList = imageSliderUrlList;
        }

        @Override
        public int getCount() {
            return imageSliderUrlList.size();
        }

        @Override
        public View instantiateItem(ViewGroup container, int position) {
            PhotoView photoView = new PhotoView(container.getContext());
            //   photoView.setImageResource(sDrawables[position]);
            try {
                System.out.println("Sukdev : onBindViewHolder : imageSliderUrlList.get(position) : " + imageSliderUrlList.get(position));
                Glide.with(container)
                        .load(imageSliderUrlList.get(position))
                        .diskCacheStrategy(DiskCacheStrategy.NONE).skipMemoryCache(true)
                        .into(photoView);

            } catch (java.lang.NullPointerException ex) {

            }
            // Now just add PhotoView to ViewPager and return it
            container.addView(photoView, ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT);
            return photoView;
        }

        @Override
        public void destroyItem(ViewGroup container, int position, Object object) {
            container.removeView((View) object);
        }

        @Override
        public boolean isViewFromObject(View view, Object object) {
            return view == object;
        }

    }
}