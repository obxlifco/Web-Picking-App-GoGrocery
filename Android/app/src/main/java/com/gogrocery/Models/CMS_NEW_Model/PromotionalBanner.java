package com.gogrocery.Models.CMS_NEW_Model;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class PromotionalBanner {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("website_id")
@Expose
private Integer websiteId;
@SerializedName("banner_name")
@Expose
private String bannerName;
@SerializedName("banner_type")
@Expose
private String bannerType;
@SerializedName("banner_image")
@Expose
private BannerImage bannerImage;
@SerializedName("product_count")
@Expose
private Integer productCount;

public Integer getId() {
return id;
}

public void setId(Integer id) {
this.id = id;
}

public Integer getWebsiteId() {
return websiteId;
}

public void setWebsiteId(Integer websiteId) {
this.websiteId = websiteId;
}

public String getBannerName() {
return bannerName;
}

public void setBannerName(String bannerName) {
this.bannerName = bannerName;
}

public String getBannerType() {
return bannerType;
}

public void setBannerType(String bannerType) {
this.bannerType = bannerType;
}

public BannerImage getBannerImage() {
return bannerImage;
}

public void setBannerImage(BannerImage bannerImage) {
this.bannerImage = bannerImage;
}

public Integer getProductCount() {
return productCount;
}

public void setProductCount(Integer productCount) {
this.productCount = productCount;
}

}