package com.gogrocery.Adapters;

import android.app.Activity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import com.bumptech.glide.request.RequestOptions;
import com.gogrocery.R;
import com.smarteist.autoimageslider.SliderViewAdapter;


public class ImageSliderAdapter extends SliderViewAdapter<ImageSliderAdapter.SliderAdapterVH> {

    private Activity activity;


    public ImageSliderAdapter(Activity context ) {
        this.activity = context;

    }

    @Override
    public SliderAdapterVH onCreateViewHolder(ViewGroup parent) {
        View inflate = LayoutInflater.from(parent.getContext()).inflate(R.layout.layout_welcome_page_item, null);
        return new SliderAdapterVH(inflate);
    }

    @Override
    public void onBindViewHolder(SliderAdapterVH viewHolder, int position) {
try {
    switch (position) {
        case 0:
            viewHolder.imageViewBackground.setBackgroundResource(R.drawable.anim_rabbitscene1);
            viewHolder.textViewDescription1.setText(activity.getResources().getString(R.string.txtStartedOneHeader));
            viewHolder.textViewDescription2.setText(activity.getResources().getString(R.string.txtStartedOneDesc));

            break;
        case 1:
            viewHolder.imageViewBackground.setBackgroundResource(R.drawable.anim_rabbitscene2);
            viewHolder.textViewDescription1.setText(activity.getResources().getString(R.string.txtStartedTwoHeader));
            viewHolder.textViewDescription2.setText(activity.getResources().getString(R.string.txtStartedTwoDesc));
            break;
        case 2:
            viewHolder.imageViewBackground.setBackgroundResource(R.drawable.anim_rabbitscene3);
            viewHolder.textViewDescription1.setText(activity.getResources().getString(R.string.txtStartedThreeHeader));
            viewHolder.textViewDescription2.setText(activity.getResources().getString(R.string.txtStartedThreeDesc));
            break;
        default:
            viewHolder.imageViewBackground.setBackgroundResource(R.drawable.anim_rabbitscene1);
            viewHolder.textViewDescription1.setText(activity.getResources().getString(R.string.txtStartedOneHeader));
            viewHolder.textViewDescription2.setText(activity.getResources().getString(R.string.txtStartedOneDesc));
            break;


    }
}catch (Exception e){
    e.printStackTrace();
}





    }

    @Override
    public int getCount() {

            return 3;


    }


    static class SliderAdapterVH extends SliderViewAdapter.ViewHolder {

        View itemView;
        ImageView imageViewBackground;
        TextView textViewDescription1;
        TextView textViewDescription2;

        public SliderAdapterVH(View itemView) {
            super(itemView);
            imageViewBackground = itemView.findViewById(R.id.iv_auto_image_slider);
            textViewDescription1 = itemView.findViewById(R.id.tv_title);
            textViewDescription2 = itemView.findViewById(R.id.tv_description);
            this.itemView = itemView;
        }
    }




}

