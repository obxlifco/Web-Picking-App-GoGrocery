package com.gogrocery.Models.ViewCartModel;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class ProductId {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("name")
@Expose
private String name;
@SerializedName("sku")
@Expose
private String sku;
@SerializedName("default_price")
@Expose
private String defaultPrice;
@SerializedName("brand")
@Expose
private List<Brand> brand = null;
@SerializedName("slug")
@Expose
private String slug;
@SerializedName("veg_nonveg_type")
@Expose
private String vegNonvegType;
@SerializedName("mp_description")
@Expose
private Object mpDescription;
@SerializedName("mp_features")
@Expose
private Object mpFeatures;
@SerializedName("product_image")
@Expose
private ProductImage productImage = null;
@SerializedName("custom_field")
@Expose
private List<CustomField> customField = null;

    @SerializedName("channel_price")
    @Expose
    private String channel_price;

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

public String getSku() {
return sku;
}

public void setSku(String sku) {
this.sku = sku;
}

public String getDefaultPrice() {
return defaultPrice;
}

public void setDefaultPrice(String defaultPrice) {
this.defaultPrice = defaultPrice;
}

public List<Brand> getBrand() {
return brand;
}

public void setBrand(List<Brand> brand) {
this.brand = brand;
}

public String getSlug() {
return slug;
}

public void setSlug(String slug) {
this.slug = slug;
}

public String getVegNonvegType() {
return vegNonvegType;
}

public void setVegNonvegType(String vegNonvegType) {
this.vegNonvegType = vegNonvegType;
}

public Object getMpDescription() {
return mpDescription;
}

public void setMpDescription(Object mpDescription) {
this.mpDescription = mpDescription;
}

public Object getMpFeatures() {
return mpFeatures;
}

public void setMpFeatures(Object mpFeatures) {
this.mpFeatures = mpFeatures;
}

public ProductImage getProductImage() {
return productImage;
}

public void setProductImage(ProductImage productImage) {
this.productImage = productImage;
}

public List<CustomField> getCustomField() {
return customField;
}

public void setCustomField(List<CustomField> customField) {
this.customField = customField;
}

    public String getChannel_price() {
        return channel_price;
    }

    public void setChannel_price(String channel_price) {
        this.channel_price = channel_price;
    }
}