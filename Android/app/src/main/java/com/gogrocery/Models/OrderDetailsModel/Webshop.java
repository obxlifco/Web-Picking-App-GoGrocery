package com.gogrocery.Models.OrderDetailsModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Webshop {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("name")
@Expose
private String name;
@SerializedName("image")
@Expose
private String image;
@SerializedName("image_small")
@Expose
private String imageSmall;
@SerializedName("description")
@Expose
private String description;
@SerializedName("order_id")
@Expose
private Integer orderId;
@SerializedName("is_on_product_setup")
@Expose
private String isOnProductSetup;
@SerializedName("country_code")
@Expose
private Object countryCode;
@SerializedName("country_id")
@Expose
private Integer countryId;
@SerializedName("website_code")
@Expose
private String websiteCode;
@SerializedName("site")
@Expose
private Object site;
@SerializedName("website_name")
@Expose
private Object websiteName;
@SerializedName("isblocked")
@Expose
private String isblocked;
@SerializedName("isdeleted")
@Expose
private String isdeleted;
@SerializedName("parent_id")
@Expose
private Integer parentId;
@SerializedName("parent_logo")
@Expose
private String parentLogo;
@SerializedName("parent_name")
@Expose
private String parentName;
@SerializedName("test")
@Expose
private Integer test;
@SerializedName("sandbox_login_link")
@Expose
private Object sandboxLoginLink;
@SerializedName("sandbox_api_link")
@Expose
private Object sandboxApiLink;
@SerializedName("live_login_link")
@Expose
private Object liveLoginLink;
@SerializedName("live_api_link")
@Expose
private Object liveApiLink;
@SerializedName("sandbox_app_id")
@Expose
private Object sandboxAppId;
@SerializedName("live_app_id")
@Expose
private Object liveAppId;
@SerializedName("live_cert_id")
@Expose
private Object liveCertId;
@SerializedName("live_runame")
@Expose
private String liveRuname;
@SerializedName("developer_id")
@Expose
private String developerId;
@SerializedName("compatibility_level")
@Expose
private Integer compatibilityLevel;
@SerializedName("sandbox_cert_id")
@Expose
private Object sandboxCertId;
@SerializedName("sandbox_runame")
@Expose
private Object sandboxRuname;
@SerializedName("channel_url")
@Expose
private String channelUrl;
@SerializedName("amazon_fulfillment_center")
@Expose
private String amazonFulfillmentCenter;

public Integer getId() {
return id;
}

public void setId(Integer id) {
this.id = id;
}

public String getName() {
return name;
}

public void setName(String name) {
this.name = name;
}

public String getImage() {
return image;
}

public void setImage(String image) {
this.image = image;
}

public String getImageSmall() {
return imageSmall;
}

public void setImageSmall(String imageSmall) {
this.imageSmall = imageSmall;
}

public String getDescription() {
return description;
}

public void setDescription(String description) {
this.description = description;
}

public Integer getOrderId() {
return orderId;
}

public void setOrderId(Integer orderId) {
this.orderId = orderId;
}

public String getIsOnProductSetup() {
return isOnProductSetup;
}

public void setIsOnProductSetup(String isOnProductSetup) {
this.isOnProductSetup = isOnProductSetup;
}

public Object getCountryCode() {
return countryCode;
}

public void setCountryCode(Object countryCode) {
this.countryCode = countryCode;
}

public Integer getCountryId() {
return countryId;
}

public void setCountryId(Integer countryId) {
this.countryId = countryId;
}

public String getWebsiteCode() {
return websiteCode;
}

public void setWebsiteCode(String websiteCode) {
this.websiteCode = websiteCode;
}

public Object getSite() {
return site;
}

public void setSite(Object site) {
this.site = site;
}

public Object getWebsiteName() {
return websiteName;
}

public void setWebsiteName(Object websiteName) {
this.websiteName = websiteName;
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

public Integer getParentId() {
return parentId;
}

public void setParentId(Integer parentId) {
this.parentId = parentId;
}

public String getParentLogo() {
return parentLogo;
}

public void setParentLogo(String parentLogo) {
this.parentLogo = parentLogo;
}

public String getParentName() {
return parentName;
}

public void setParentName(String parentName) {
this.parentName = parentName;
}

public Integer getTest() {
return test;
}

public void setTest(Integer test) {
this.test = test;
}

public Object getSandboxLoginLink() {
return sandboxLoginLink;
}

public void setSandboxLoginLink(Object sandboxLoginLink) {
this.sandboxLoginLink = sandboxLoginLink;
}

public Object getSandboxApiLink() {
return sandboxApiLink;
}

public void setSandboxApiLink(Object sandboxApiLink) {
this.sandboxApiLink = sandboxApiLink;
}

public Object getLiveLoginLink() {
return liveLoginLink;
}

public void setLiveLoginLink(Object liveLoginLink) {
this.liveLoginLink = liveLoginLink;
}

public Object getLiveApiLink() {
return liveApiLink;
}

public void setLiveApiLink(Object liveApiLink) {
this.liveApiLink = liveApiLink;
}

public Object getSandboxAppId() {
return sandboxAppId;
}

public void setSandboxAppId(Object sandboxAppId) {
this.sandboxAppId = sandboxAppId;
}

public Object getLiveAppId() {
return liveAppId;
}

public void setLiveAppId(Object liveAppId) {
this.liveAppId = liveAppId;
}

public Object getLiveCertId() {
return liveCertId;
}

public void setLiveCertId(Object liveCertId) {
this.liveCertId = liveCertId;
}

public String getLiveRuname() {
return liveRuname;
}

public void setLiveRuname(String liveRuname) {
this.liveRuname = liveRuname;
}

public String getDeveloperId() {
return developerId;
}

public void setDeveloperId(String developerId) {
this.developerId = developerId;
}

public Integer getCompatibilityLevel() {
return compatibilityLevel;
}

public void setCompatibilityLevel(Integer compatibilityLevel) {
this.compatibilityLevel = compatibilityLevel;
}

public Object getSandboxCertId() {
return sandboxCertId;
}

public void setSandboxCertId(Object sandboxCertId) {
this.sandboxCertId = sandboxCertId;
}

public Object getSandboxRuname() {
return sandboxRuname;
}

public void setSandboxRuname(Object sandboxRuname) {
this.sandboxRuname = sandboxRuname;
}

public String getChannelUrl() {
return channelUrl;
}

public void setChannelUrl(String channelUrl) {
this.channelUrl = channelUrl;
}

public String getAmazonFulfillmentCenter() {
return amazonFulfillmentCenter;
}

public void setAmazonFulfillmentCenter(String amazonFulfillmentCenter) {
this.amazonFulfillmentCenter = amazonFulfillmentCenter;
}

}