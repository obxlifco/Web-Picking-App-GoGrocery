package com.gogrocery.Models.CartModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class ProductImage {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("img")
@Expose
private String img;
@SerializedName("status")
@Expose
private String status;
@SerializedName("is_cover")
@Expose
private Integer isCover;
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
@SerializedName("product")
@Expose
private Integer product;

public Integer getId() {
return id;
}

public void setId(Integer id) {
this.id = id;
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

public Integer getProduct() {
return product;
}

public void setProduct(Integer product) {
this.product = product;
}

}