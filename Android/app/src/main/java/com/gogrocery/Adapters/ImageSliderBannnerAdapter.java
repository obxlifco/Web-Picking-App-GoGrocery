package com.gogrocery.Adapters;

import android.content.Context;
import android.graphics.drawable.Drawable;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.viewpager.widget.PagerAdapter;
import androidx.viewpager.widget.ViewPager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.DataSource;
import com.bumptech.glide.load.engine.GlideException;
import com.bumptech.glide.request.RequestListener;
import com.bumptech.glide.request.target.Target;
import com.gogrocery.R;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Sanket on 27-Feb-17.
 */

public class ImageSliderBannnerAdapter extends PagerAdapter {

    private Context context;
    private LayoutInflater layoutInflater;
private List<String> urlList=new ArrayList<>();

    public ImageSliderBannnerAdapter(Context context,List<String> urlList) {
        this.context = context;
        this.urlList=urlList;
    }

    @Override
    public int getCount() {
        return urlList.size();

    }

    @Override
    public boolean isViewFromObject(View view, Object object) {
        return view == object;
    }

    @NonNull
    @Override
    public Object instantiateItem(ViewGroup container, final int position) {

        layoutInflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        View view = layoutInflater.inflate(R.layout.image_slider_banner, null);
        ImageView imageView = (ImageView) view.findViewById(R.id.customImage);


       /* Glide.with(context)
                .load(R.drawable.single_image_spinner)
                .into(single_image_spinner);*/

        System.out.println("Rahul : ImageSliderBannnerAdapter : instantiateItem : position : "+position+" : "+urlList.get(position));
        Glide.with(context)
                .load(urlList.get(position))
                .listener(new RequestListener<Drawable>() {

                    @Override
                    public boolean onLoadFailed(@Nullable GlideException e, Object model, Target<Drawable> target, boolean isFirstResource) {

                       // single_image_spinner.setVisibility(View.GONE);
                        return false;
                    }

                    @Override
                    public boolean onResourceReady(Drawable resource, Object model, Target<Drawable> target, DataSource dataSource, boolean isFirstResource) {
                       // single_image_spinner.setVisibility(View.GONE);
                        return false;
                    }
                })
                .into(imageView);


        ViewPager vp = (ViewPager) container;
        vp.addView(view, 0);
        return view;

    }

    @Override
    public void destroyItem(ViewGroup container, int position, Object object) {

        ViewPager vp = (ViewPager) container;
        View view = (View) object;
        vp.removeView(view);

    }

    @Override
    public void notifyDataSetChanged() {
        super.notifyDataSetChanged();

    }
}
