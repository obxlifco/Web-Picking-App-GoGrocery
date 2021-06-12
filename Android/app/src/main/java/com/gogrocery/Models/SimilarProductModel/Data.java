package com.gogrocery.Models.SimilarProductModel;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Data {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("product")
@Expose
private Product product;
@SerializedName("category")
@Expose
private Category_ category;
@SerializedName("parent_id")
@Expose
private Object parentId;
@SerializedName("is_parent")
@Expose
private String isParent;
@SerializedName("isblocked")
@Expose
private String isblocked;
@SerializedName("isdeleted")
@Expose
private String isdeleted;
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
@SerializedName("stock_details")
@Expose
private List<StockDetail> stockDetails = null;
    @SerializedName("channel_price")
    @Expose
    private String channel_price;
    @SerializedName("new_default_price")
    @Expose
    private String new_default_price;

    @SerializedName("new_default_price_unit")
    @Expose
    private String new_default_price_unit;

    @SerializedName("discount_price_unit")
    @Expose
    private String discount_price_unit;

    @SerializedName("discount_price")
    @Expose
    private String discount_price;

    @SerializedName("discount_amount")
    @Expose
    private String discount_amount;

    @SerializedName("disc_type")
    @Expose
    private String disc_type;

public Integer getId() {
return id;
}

public void setId(Integer id) {
this.id = id;
}

public Product getProduct() {
return product;
}

public void setProduct(Product product) {
this.product = product;
}

public Category_ getCategory() {
return category;
}

public void setCategory(Category_ category) {
this.category = category;
}

public Object getParentId() {
return parentId;
}

public void setParentId(Object parentId) {
this.parentId = parentId;
}

public String getIsParent() {
return isParent;
}

public void setIsParent(String isParent) {
this.isParent = isParent;
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

    public List<StockDetail> getStockDetails() {
        return stockDetails;
    }

    public void setStockDetails(List<StockDetail> stockDetails) {
        this.stockDetails = stockDetails;
    }

    public String getChannel_price() {
        return channel_price;
    }

    public void setChannel_price(String channel_price) {
        this.channel_price = channel_price;
    }

    public String getNew_default_price() {
        return new_default_price;
    }

    public void setNew_default_price(String new_default_price) {
        this.new_default_price = new_default_price;
    }

    public String getNew_default_price_unit() {
        return new_default_price_unit;
    }

    public void setNew_default_price_unit(String new_default_price_unit) {
        this.new_default_price_unit = new_default_price_unit;
    }

    public String getDiscount_price_unit() {
        return discount_price_unit;
    }

    public void setDiscount_price_unit(String discount_price_unit) {
        this.discount_price_unit = discount_price_unit;
    }

    public String getDiscount_price() {
        return discount_price;
    }

    public void setDiscount_price(String discount_price) {
        this.discount_price = discount_price;
    }

    public String getDiscount_amount() {
        return discount_amount;
    }

    public void setDiscount_amount(String discount_amount) {
        this.discount_amount = discount_amount;
    }

    public String getDisc_type() {
        return disc_type;
    }

    public void setDisc_type(String disc_type) {
        this.disc_type = disc_type;
    }
}