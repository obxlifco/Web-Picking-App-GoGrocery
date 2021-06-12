package com.gogrocery.Models.CartSummaryModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class ProductImage {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("website_id")
@Expose
private Integer websiteId;
@SerializedName("img")
@Expose
private String img;
@SerializedName("status")
@Expose
private String status;
@SerializedName("is_cover")
@Expose
private Integer isCover;
@SerializedName("img_title")
@Expose
private Object imgTitle;
@SerializedName("img_alt")
@Expose
private Object imgAlt;
@SerializedName("img_order")
@Expose
private Object imgOrder;
@SerializedName("created")
@Expose
private String created;
@SerializedName("modified")
@Expose
private String modified;
@SerializedName("createdby")
@Expose
private Integer createdby;
@SerializedName("updatedby")
@Expose
private Integer updatedby;
@SerializedName("ip_address")
@Expose
private Object ipAddress;
@SerializedName("product")
@Expose
private Integer product;

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

public String getImg() {
return img;
}

public void setImg(String img) {
this.img = img;
}

public String getStatus() {
return status;
}

public void setStatus(String status) {
this.status = status;
}

public Integer getIsCover() {
return isCover;
}

public void setIsCover(Integer isCover) {
this.isCover = isCover;
}

public Object getImgTitle() {
return imgTitle;
}

public void setImgTitle(Object imgTitle) {
this.imgTitle = imgTitle;
}

public Object getImgAlt() {
return imgAlt;
}

public void setImgAlt(Object imgAlt) {
this.imgAlt = imgAlt;
}

public Object getImgOrder() {
return imgOrder;
}

public void setImgOrder(Object imgOrder) {
this.imgOrder = imgOrder;
}

public String getCreated() {
return created;
}

public void setCreated(String created) {
this.created = created;
}

public String getModified() {
return modified;
}

public void setModified(String modified) {
this.modified = modified;
}

public Integer getCreatedby() {
return createdby;
}

public void setCreatedby(Integer createdby) {
this.createdby = createdby;
}

public Integer getUpdatedby() {
return updatedby;
}

public void setUpdatedby(Integer updatedby) {
this.updatedby = updatedby;
}

public Object getIpAddress() {
return ipAddress;
}

public void setIpAddress(Object ipAddress) {
this.ipAddress = ipAddress;
}

public Integer getProduct() {
return product;
}

public void setProduct(Integer product) {
this.product = product;
}

}