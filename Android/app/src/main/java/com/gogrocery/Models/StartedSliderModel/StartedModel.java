package com.gogrocery.Models.StartedSliderModel;

import android.graphics.drawable.Drawable;

public class StartedModel {
    String header,description;
    int img;

    public StartedModel(String header, String description, int img) {
        this.header = header;
        this.description = description;
        this.img = img;
    }

    public String getHeader() {
        return header;
    }

    public void setHeader(String header) {
        this.header = header;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public int getImg() {
        return img;
    }

    public void setImg(int img) {
        this.img = img;
    }
}
