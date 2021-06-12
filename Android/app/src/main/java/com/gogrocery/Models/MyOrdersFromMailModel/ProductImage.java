package com.gogrocery.Models.MyOrdersFromMailModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class ProductImage {

@SerializedName("is_cover")
@Expose
private Integer isCover;
@SerializedName("img")
@Expose
private String img;

public Integer getIsCover() {
return isCover;
}

public void setIsCover(Integer isCover) {
this.isCover = isCover;
}

public String getImg() {
return img;
}

public void setImg(String img) {
this.img = img;
}

}