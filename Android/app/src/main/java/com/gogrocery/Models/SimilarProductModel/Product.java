package com.gogrocery.Models.SimilarProductModel;

import java.util.List;

import com.gogrocery.Models.CartModel.ProductImage;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Product {
    @SerializedName("id")
    @Expose
    private Integer id;
    @SerializedName("product_image")
    @Expose
    private List<ProductImage> productImage = null;
    @SerializedName("variant_product")
    @Expose
    private List<Object> variantProduct = null;
    @SerializedName("custom_field")
    @Expose
    private List<CustomField> customField = null;
    @SerializedName("brand")
    @Expose
    private Brand brand;
    @SerializedName("category")
    @Expose
    private Category category;
    @SerializedName("channel_price")
    @Expose
    private String channelPrice;
    @SerializedName("uom")
    @Expose
    private String uom;
    @SerializedName("order_id")
    @Expose
    private Integer orderId;
    @SerializedName("website_id")
    @Expose
    private Integer websiteId;
    @SerializedName("ebay_item_id")
    @Expose
    private Object ebayItemId;
    @SerializedName("amazon_itemid")
    @Expose
    private String amazonItemid;
    @SerializedName("ebay_addstatus")
    @Expose
    private Object ebayAddstatus;
    @SerializedName("twitter_addstatus")
    @Expose
    private String twitterAddstatus;
    @SerializedName("amazon_addstatus")
    @Expose
    private String amazonAddstatus;
    @SerializedName("ebay_listing_starttime")
    @Expose
    private Object ebayListingStarttime;
    @SerializedName("ebay_listing_endtime")
    @Expose
    private Object ebayListingEndtime;
    @SerializedName("ebay_listing_build")
    @Expose
    private Object ebayListingBuild;
    @SerializedName("ebay_listing_version")
    @Expose
    private Object ebayListingVersion;
    @SerializedName("ebay_listing_time")
    @Expose
    private Object ebayListingTime;
    @SerializedName("total_listingfee")
    @Expose
    private Object totalListingfee;
    @SerializedName("name")
    @Expose
    private String name;
    @SerializedName("sku")
    @Expose
    private String sku;
    @SerializedName("title")
    @Expose
    private Object title;
    @SerializedName("weight")
    @Expose
    private String weight;
    @SerializedName("meta_url")
    @Expose
    private String metaUrl;
    @SerializedName("meta_title")
    @Expose
    private Object metaTitle;
    @SerializedName("meta_key_word")
    @Expose
    private Object metaKeyWord;
    @SerializedName("meta_description")
    @Expose
    private Object metaDescription;
    @SerializedName("description")
    @Expose
    private String description;
    @SerializedName("shippingclass_id")
    @Expose
    private Object shippingclassId;
    @SerializedName("url")
    @Expose
    private String url;
    @SerializedName("visibility_id")
    @Expose
    private Integer visibilityId;
    @SerializedName("supplier_id")
    @Expose
    private Object supplierId;
    @SerializedName("status")
    @Expose
    private String status;
    @SerializedName("new_date")
    @Expose
    private Object newDate;
    @SerializedName("isbn")
    @Expose
    private Object isbn;
    @SerializedName("asin")
    @Expose
    private Object asin;
    @SerializedName("ean")
    @Expose
    private String ean;
    @SerializedName("npn")
    @Expose
    private Object npn;
    @SerializedName("supc")
    @Expose
    private Object supc;
    @SerializedName("max_order_unit")
    @Expose
    private Object maxOrderUnit;
    @SerializedName("video")
    @Expose
    private Object video;
    @SerializedName("mp_description")
    @Expose
    private Object mpDescription;
    @SerializedName("mp_features")
    @Expose
    private Object mpFeatures;
    @SerializedName("mp_system_requirements")
    @Expose
    private Object mpSystemRequirements;
    @SerializedName("mp_templates")
    @Expose
    private Object mpTemplates;
    @SerializedName("features")
    @Expose
    private Object features;
    @SerializedName("last_cost")
    @Expose
    private Object lastCost;
    @SerializedName("avg_cost")
    @Expose
    private Object avgCost;
    @SerializedName("default_price")
    @Expose
    private Double defaultPrice;
    @SerializedName("cost_per_unit")
    @Expose
    private Object costPerUnit;
    @SerializedName("quantity")
    @Expose
    private Object quantity;
    @SerializedName("pdf_file_path")
    @Expose
    private Object pdfFilePath;
    @SerializedName("isblocked")
    @Expose
    private String isblocked;
    @SerializedName("isdeleted")
    @Expose
    private String isdeleted;
    @SerializedName("is_import")
    @Expose
    private Object isImport;
    @SerializedName("is_auctionable")
    @Expose
    private Object isAuctionable;
    @SerializedName("numberof_sale")
    @Expose
    private Integer numberofSale;
    @SerializedName("numberof_view")
    @Expose
    private Integer numberofView;
    @SerializedName("ebay")
    @Expose
    private Integer ebay;
    @SerializedName("amazon")
    @Expose
    private Integer amazon;
    @SerializedName("webshop")
    @Expose
    private Integer webshop;
    @SerializedName("order_price")
    @Expose
    private Integer orderPrice;
    @SerializedName("slug")
    @Expose
    private String slug;
    @SerializedName("best_selling")
    @Expose
    private Object bestSelling;
    @SerializedName("created")
    @Expose
    private String created;
    @SerializedName("modified")
    @Expose
    private String modified;
    @SerializedName("org_pro_con")
    @Expose
    private Object orgProCon;
    @SerializedName("is_facebook_product")
    @Expose
    private Object isFacebookProduct;
    @SerializedName("sla")
    @Expose
    private Object sla;
    @SerializedName("veg_nonveg_type")
    @Expose
    private Object vegNonvegType;
    @SerializedName("price_formula_id_for_customer")
    @Expose
    private Object priceFormulaIdForCustomer;
    @SerializedName("price_formula_id_for_supplier")
    @Expose
    private Object priceFormulaIdForSupplier;
    @SerializedName("product_offer_desc")
    @Expose
    private Object productOfferDesc;
    @SerializedName("product_offer_start_date")
    @Expose
    private Object productOfferStartDate;
    @SerializedName("product_offer_end_date")
    @Expose
    private Object productOfferEndDate;
    @SerializedName("ip_address")
    @Expose
    private Object ipAddress;
    @SerializedName("hsn_id")
    @Expose
    private String hsnId;
    @SerializedName("visible_in_listing")
    @Expose
    private String visibleInListing;
    @SerializedName("related_product_skus")
    @Expose
    private Object relatedProductSkus;
    @SerializedName("meta_og_tags")
    @Expose
    private Object metaOgTags;
    @SerializedName("customer_group")
    @Expose
    private Object customerGroup;
    @SerializedName("taxclass")
    @Expose
    private Object taxclass;
    @SerializedName("po_taxclass")
    @Expose
    private Object poTaxclass;
    @SerializedName("warehouse")
    @Expose
    private Object warehouse;
    @SerializedName("max_price_rule")
    @Expose
    private Object maxPriceRule;
    @SerializedName("min_price_rule")
    @Expose
    private Object minPriceRule;
    @SerializedName("new_default_price")
    @Expose
    private String newDefaultPrice;
    @SerializedName("new_default_price_unit")
    @Expose
    private String newDefaultPriceUnit;
    @SerializedName("discount_price_unit")
    @Expose
    private String discountPriceUnit;
    @SerializedName("discount_price")
    @Expose
    private String discountPrice;
    @SerializedName("discount_amount")
    @Expose
    private String discountAmount;
    @SerializedName("disc_type")
    @Expose
    private String discType;
    @SerializedName("coupon")
    @Expose
    private String coupon;





public Integer getId() {
return id;
}

public void setId(Integer id) {
this.id = id;
}

public List<ProductImage> getProductImage() {
return productImage;
}

public void setProductImage(List<ProductImage> productImage) {
this.productImage = productImage;
}

public List<Object> getVariantProduct() {
return variantProduct;
}

public void setVariantProduct(List<Object> variantProduct) {
this.variantProduct = variantProduct;
}

public List<CustomField> getCustomField() {
return customField;
}

public void setCustomField(List<CustomField> customField) {
this.customField = customField;
}

public Brand getBrand() {
return brand;
}

public void setBrand(Brand brand) {
this.brand = brand;
}

public Category getCategory() {
return category;
}

public void setCategory(Category category) {
this.category = category;
}

public String getChannelPrice() {
return channelPrice;
}

public void setChannelPrice(String channelPrice) {
this.channelPrice = channelPrice;
}

public Integer getOrderId() {
return orderId;
}

public void setOrderId(Integer orderId) {
this.orderId = orderId;
}

public Integer getWebsiteId() {
return websiteId;
}

public void setWebsiteId(Integer websiteId) {
this.websiteId = websiteId;
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

public Object getTitle() {
return title;
}

public void setTitle(Object title) {
this.title = title;
}

public String getWeight() {
return weight;
}

public void setWeight(String weight) {
this.weight = weight;
}

public String getMetaUrl() {
return metaUrl;
}

public void setMetaUrl(String metaUrl) {
this.metaUrl = metaUrl;
}

public Object getMetaTitle() {
return metaTitle;
}

public void setMetaTitle(Object metaTitle) {
this.metaTitle = metaTitle;
}

public Object getMetaKeyWord() {
return metaKeyWord;
}

public void setMetaKeyWord(Object metaKeyWord) {
this.metaKeyWord = metaKeyWord;
}

public Object getMetaDescription() {
return metaDescription;
}

public void setMetaDescription(Object metaDescription) {
this.metaDescription = metaDescription;
}

public String getDescription() {
return description;
}

public void setDescription(String description) {
this.description = description;
}

public Object getShippingclassId() {
return shippingclassId;
}

public void setShippingclassId(Object shippingclassId) {
this.shippingclassId = shippingclassId;
}

public String getUrl() {
return url;
}

public void setUrl(String url) {
this.url = url;
}

public Integer getVisibilityId() {
return visibilityId;
}

public void setVisibilityId(Integer visibilityId) {
this.visibilityId = visibilityId;
}

public String getStatus() {
return status;
}

public void setStatus(String status) {
this.status = status;
}

public String getEan() {
return ean;
}

public void setEan(String ean) {
this.ean = ean;
}

public Object getNpn() {
return npn;
}

public void setNpn(Object npn) {
this.npn = npn;
}

public Object getSupc() {
return supc;
}

public void setSupc(Object supc) {
this.supc = supc;
}

public Object getMaxOrderUnit() {
return maxOrderUnit;
}

public void setMaxOrderUnit(Object maxOrderUnit) {
this.maxOrderUnit = maxOrderUnit;
}

public Object getFeatures() {
return features;
}

public void setFeatures(Object features) {
this.features = features;
}

public Object getLastCost() {
return lastCost;
}

public void setLastCost(Object lastCost) {
this.lastCost = lastCost;
}

public Object getAvgCost() {
return avgCost;
}

public void setAvgCost(Object avgCost) {
this.avgCost = avgCost;
}

public Double getDefaultPrice() {
return defaultPrice;
}

public void setDefaultPrice(Double defaultPrice) {
this.defaultPrice = defaultPrice;
}

public Object getCostPerUnit() {
return costPerUnit;
}

public void setCostPerUnit(Object costPerUnit) {
this.costPerUnit = costPerUnit;
}

public Object getQuantity() {
return quantity;
}

public void setQuantity(Object quantity) {
this.quantity = quantity;
}

public Object getPdfFilePath() {
return pdfFilePath;
}

public void setPdfFilePath(Object pdfFilePath) {
this.pdfFilePath = pdfFilePath;
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

public Object getIsImport() {
return isImport;
}

public void setIsImport(Object isImport) {
this.isImport = isImport;
}

public Object getIsAuctionable() {
return isAuctionable;
}

public void setIsAuctionable(Object isAuctionable) {
this.isAuctionable = isAuctionable;
}

public Integer getNumberofSale() {
return numberofSale;
}

public void setNumberofSale(Integer numberofSale) {
this.numberofSale = numberofSale;
}

public Integer getNumberofView() {
return numberofView;
}

public void setNumberofView(Integer numberofView) {
this.numberofView = numberofView;
}

public Integer getEbay() {
return ebay;
}

public void setEbay(Integer ebay) {
this.ebay = ebay;
}

public Integer getAmazon() {
return amazon;
}

public void setAmazon(Integer amazon) {
this.amazon = amazon;
}

public Integer getWebshop() {
return webshop;
}

public void setWebshop(Integer webshop) {
this.webshop = webshop;
}

public Integer getOrderPrice() {
return orderPrice;
}

public void setOrderPrice(Integer orderPrice) {
this.orderPrice = orderPrice;
}

public String getSlug() {
return slug;
}

public void setSlug(String slug) {
this.slug = slug;
}

public Object getBestSelling() {
return bestSelling;
}

public void setBestSelling(Object bestSelling) {
this.bestSelling = bestSelling;
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

public Object getOrgProCon() {
return orgProCon;
}

public void setOrgProCon(Object orgProCon) {
this.orgProCon = orgProCon;
}

public Object getIsFacebookProduct() {
return isFacebookProduct;
}

public void setIsFacebookProduct(Object isFacebookProduct) {
this.isFacebookProduct = isFacebookProduct;
}

public Object getSla() {
return sla;
}

public void setSla(Object sla) {
this.sla = sla;
}

public Object getVegNonvegType() {
return vegNonvegType;
}

public void setVegNonvegType(Object vegNonvegType) {
this.vegNonvegType = vegNonvegType;
}

public Object getPriceFormulaIdForCustomer() {
return priceFormulaIdForCustomer;
}

public void setPriceFormulaIdForCustomer(Object priceFormulaIdForCustomer) {
this.priceFormulaIdForCustomer = priceFormulaIdForCustomer;
}

public Object getPriceFormulaIdForSupplier() {
return priceFormulaIdForSupplier;
}

public void setPriceFormulaIdForSupplier(Object priceFormulaIdForSupplier) {
this.priceFormulaIdForSupplier = priceFormulaIdForSupplier;
}

public String getUom() {
return uom;
}

public void setUom(String uom) {
this.uom = uom;
}

public Object getProductOfferDesc() {
return productOfferDesc;
}

public void setProductOfferDesc(Object productOfferDesc) {
this.productOfferDesc = productOfferDesc;
}

public Object getProductOfferStartDate() {
return productOfferStartDate;
}

public void setProductOfferStartDate(Object productOfferStartDate) {
this.productOfferStartDate = productOfferStartDate;
}

public Object getProductOfferEndDate() {
return productOfferEndDate;
}

public void setProductOfferEndDate(Object productOfferEndDate) {
this.productOfferEndDate = productOfferEndDate;
}

public Object getIpAddress() {
return ipAddress;
}

public void setIpAddress(Object ipAddress) {
this.ipAddress = ipAddress;
}

public String getHsnId() {
return hsnId;
}

public void setHsnId(String hsnId) {
this.hsnId = hsnId;
}

public String getVisibleInListing() {
return visibleInListing;
}

public void setVisibleInListing(String visibleInListing) {
this.visibleInListing = visibleInListing;
}

public Object getRelatedProductSkus() {
return relatedProductSkus;
}

public void setRelatedProductSkus(Object relatedProductSkus) {
this.relatedProductSkus = relatedProductSkus;
}

public Object getMetaOgTags() {
return metaOgTags;
}

public void setMetaOgTags(Object metaOgTags) {
this.metaOgTags = metaOgTags;
}

public Object getCustomerGroup() {
return customerGroup;
}

public void setCustomerGroup(Object customerGroup) {
this.customerGroup = customerGroup;
}

public Object getTaxclass() {
return taxclass;
}

public void setTaxclass(Object taxclass) {
this.taxclass = taxclass;
}

public Object getPoTaxclass() {
return poTaxclass;
}

public void setPoTaxclass(Object poTaxclass) {
this.poTaxclass = poTaxclass;
}

public Object getWarehouse() {
return warehouse;
}

public void setWarehouse(Object warehouse) {
this.warehouse = warehouse;
}

public Object getMaxPriceRule() {
return maxPriceRule;
}

public void setMaxPriceRule(Object maxPriceRule) {
this.maxPriceRule = maxPriceRule;
}

public Object getMinPriceRule() {
return minPriceRule;
}

public void setMinPriceRule(Object minPriceRule) {
this.minPriceRule = minPriceRule;
}

public String getNewDefaultPrice() {
return newDefaultPrice;
}

public void setNewDefaultPrice(String newDefaultPrice) {
this.newDefaultPrice = newDefaultPrice;
}

public String getNewDefaultPriceUnit() {
return newDefaultPriceUnit;
}

public void setNewDefaultPriceUnit(String newDefaultPriceUnit) {
this.newDefaultPriceUnit = newDefaultPriceUnit;
}

public String getDiscountPriceUnit() {
return discountPriceUnit;
}

public void setDiscountPriceUnit(String discountPriceUnit) {
this.discountPriceUnit = discountPriceUnit;
}

public String getDiscountPrice() {
return discountPrice;
}

public void setDiscountPrice(String discountPrice) {
this.discountPrice = discountPrice;
}

public String getDiscountAmount() {
return discountAmount;
}

public void setDiscountAmount(String discountAmount) {
this.discountAmount = discountAmount;
}

public String getDiscType() {
return discType;
}

public void setDiscType(String discType) {
this.discType = discType;
}

public String getCoupon() {
return coupon;
}

public void setCoupon(String coupon) {
this.coupon = coupon;
}

    public Object getEbayItemId() {
        return ebayItemId;
    }

    public void setEbayItemId(Object ebayItemId) {
        this.ebayItemId = ebayItemId;
    }

    public String getAmazonItemid() {
        return amazonItemid;
    }

    public void setAmazonItemid(String amazonItemid) {
        this.amazonItemid = amazonItemid;
    }

    public Object getEbayAddstatus() {
        return ebayAddstatus;
    }

    public void setEbayAddstatus(Object ebayAddstatus) {
        this.ebayAddstatus = ebayAddstatus;
    }

    public String getTwitterAddstatus() {
        return twitterAddstatus;
    }

    public void setTwitterAddstatus(String twitterAddstatus) {
        this.twitterAddstatus = twitterAddstatus;
    }

    public String getAmazonAddstatus() {
        return amazonAddstatus;
    }

    public void setAmazonAddstatus(String amazonAddstatus) {
        this.amazonAddstatus = amazonAddstatus;
    }

    public Object getEbayListingStarttime() {
        return ebayListingStarttime;
    }

    public void setEbayListingStarttime(Object ebayListingStarttime) {
        this.ebayListingStarttime = ebayListingStarttime;
    }

    public Object getEbayListingEndtime() {
        return ebayListingEndtime;
    }

    public void setEbayListingEndtime(Object ebayListingEndtime) {
        this.ebayListingEndtime = ebayListingEndtime;
    }

    public Object getEbayListingBuild() {
        return ebayListingBuild;
    }

    public void setEbayListingBuild(Object ebayListingBuild) {
        this.ebayListingBuild = ebayListingBuild;
    }

    public Object getEbayListingVersion() {
        return ebayListingVersion;
    }

    public void setEbayListingVersion(Object ebayListingVersion) {
        this.ebayListingVersion = ebayListingVersion;
    }

    public Object getEbayListingTime() {
        return ebayListingTime;
    }

    public void setEbayListingTime(Object ebayListingTime) {
        this.ebayListingTime = ebayListingTime;
    }

    public Object getTotalListingfee() {
        return totalListingfee;
    }

    public void setTotalListingfee(Object totalListingfee) {
        this.totalListingfee = totalListingfee;
    }

    public Object getSupplierId() {
        return supplierId;
    }

    public void setSupplierId(Object supplierId) {
        this.supplierId = supplierId;
    }

    public Object getNewDate() {
        return newDate;
    }

    public void setNewDate(Object newDate) {
        this.newDate = newDate;
    }

    public Object getIsbn() {
        return isbn;
    }

    public void setIsbn(Object isbn) {
        this.isbn = isbn;
    }

    public Object getAsin() {
        return asin;
    }

    public void setAsin(Object asin) {
        this.asin = asin;
    }

    public Object getVideo() {
        return video;
    }

    public void setVideo(Object video) {
        this.video = video;
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

    public Object getMpSystemRequirements() {
        return mpSystemRequirements;
    }

    public void setMpSystemRequirements(Object mpSystemRequirements) {
        this.mpSystemRequirements = mpSystemRequirements;
    }

    public Object getMpTemplates() {
        return mpTemplates;
    }

    public void setMpTemplates(Object mpTemplates) {
        this.mpTemplates = mpTemplates;
    }
}