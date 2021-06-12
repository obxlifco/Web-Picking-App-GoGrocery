package com.gogrocery.Models.RatingReviewModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class ReviewData {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("website_id")
@Expose
private Integer websiteId;
@SerializedName("channel_id")
@Expose
private Integer channelId;
@SerializedName("user_ip")
@Expose
private String userIp;
@SerializedName("user_name")
@Expose
private String userName;
@SerializedName("user_designation")
@Expose
private Object userDesignation;
@SerializedName("user_email")
@Expose
private Object userEmail;
@SerializedName("user_city")
@Expose
private Object userCity;
@SerializedName("user_state")
@Expose
private Object userState;
@SerializedName("user_country")
@Expose
private String userCountry;
@SerializedName("title")
@Expose
private String title;
@SerializedName("review")
@Expose
private String review;
@SerializedName("rating")
@Expose
private Integer rating;
@SerializedName("reply")
@Expose
private Object reply;
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
private Object updatedby;
@SerializedName("replied")
@Expose
private Object replied;
@SerializedName("isblocked")
@Expose
private String isblocked;
@SerializedName("isdeleted")
@Expose
private String isdeleted;
@SerializedName("isflagged")
@Expose
private String isflagged;
@SerializedName("ispurchased")
@Expose
private String ispurchased;
@SerializedName("ip_address")
@Expose
private Object ipAddress;
@SerializedName("product")
@Expose
private Integer product;
@SerializedName("user")
@Expose
private Integer user;

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

public Integer getChannelId() {
return channelId;
}

public void setChannelId(Integer channelId) {
this.channelId = channelId;
}

public String getUserIp() {
return userIp;
}

public void setUserIp(String userIp) {
this.userIp = userIp;
}

public String getUserName() {
return userName;
}

public void setUserName(String userName) {
this.userName = userName;
}

public Object getUserDesignation() {
return userDesignation;
}

public void setUserDesignation(Object userDesignation) {
this.userDesignation = userDesignation;
}

public Object getUserEmail() {
return userEmail;
}

public void setUserEmail(Object userEmail) {
this.userEmail = userEmail;
}

public Object getUserCity() {
return userCity;
}

public void setUserCity(Object userCity) {
this.userCity = userCity;
}

public Object getUserState() {
return userState;
}

public void setUserState(Object userState) {
this.userState = userState;
}

public String getUserCountry() {
return userCountry;
}

public void setUserCountry(String userCountry) {
this.userCountry = userCountry;
}

public String getTitle() {
return title;
}

public void setTitle(String title) {
this.title = title;
}

public String getReview() {
return review;
}

public void setReview(String review) {
this.review = review;
}

public Integer getRating() {
return rating;
}

public void setRating(Integer rating) {
this.rating = rating;
}

public Object getReply() {
return reply;
}

public void setReply(Object reply) {
this.reply = reply;
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

public Object getUpdatedby() {
return updatedby;
}

public void setUpdatedby(Object updatedby) {
this.updatedby = updatedby;
}

public Object getReplied() {
return replied;
}

public void setReplied(Object replied) {
this.replied = replied;
}

public String getIsblocked() {
return isblocked;
}

public void setIsblocked(String isblocked) {
this.isblocked = isblocked;
}

public String getIsdeleted() {
return isdeleted;
}

public void setIsdeleted(String isdeleted) {
this.isdeleted = isdeleted;
}

public String getIsflagged() {
return isflagged;
}

public void setIsflagged(String isflagged) {
this.isflagged = isflagged;
}

public String getIspurchased() {
return ispurchased;
}

public void setIspurchased(String ispurchased) {
this.ispurchased = ispurchased;
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

public Integer getUser() {
return user;
}

public void setUser(Integer user) {
this.user = user;
}

}