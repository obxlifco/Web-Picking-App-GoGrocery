package com.gogrocery.Models.SaveListDetailPage;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Product {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("warehouse_id")
@Expose
private String warehouseId;
@SerializedName("quantity")
@Expose
private String quantity;
@SerializedName("deleted_quantity")
@Expose
private String deletedQuantity;
@SerializedName("cost_price")
@Expose
private String costPrice;
@SerializedName("mrp")
@Expose
private String mrp;
@SerializedName("product_price")
@Expose
private Double productPrice;
@SerializedName("product_discount_price")
@Expose
private String productDiscountPrice;
@SerializedName("product_discount_name")
@Expose
private Object productDiscountName;
@SerializedName("product_disc_type")
@Expose
private Object productDiscType;
@SerializedName("product_discount_rate")
@Expose
private String productDiscountRate;
@SerializedName("product_excise_duty")
@Expose
private String productExciseDuty;
@SerializedName("excise_duty_per")
@Expose
private Object exciseDutyPer;
@SerializedName("product_tax_price")
@Expose
private String productTaxPrice;
@SerializedName("tax_percentage")
@Expose
private String taxPercentage;
@SerializedName("tax_name")
@Expose
private Object taxName;
@SerializedName("status")
@Expose
private String status;
@SerializedName("product_price_base")
@Expose
private String productPriceBase;
@SerializedName("product_discount_price_base")
@Expose
private String productDiscountPriceBase;
@SerializedName("shipping_price")
@Expose
private String shippingPrice;
@SerializedName("shipping_price_base")
@Expose
private String shippingPriceBase;
@SerializedName("shipping_tax")
@Expose
private String shippingTax;
@SerializedName("shipping_tax_base")
@Expose
private String shippingTaxBase;
@SerializedName("giftwrap_price")
@Expose
private String giftwrapPrice;
@SerializedName("giftwrap_price_base")
@Expose
private String giftwrapPriceBase;
@SerializedName("giftwrap_tax")
@Expose
private String giftwrapTax;
@SerializedName("giftwrap_tax_base")
@Expose
private String giftwrapTaxBase;
@SerializedName("shipping_discount")
@Expose
private String shippingDiscount;
@SerializedName("shipping_discount_base")
@Expose
private String shippingDiscountBase;
@SerializedName("assign_to")
@Expose
private String assignTo;
@SerializedName("assign_wh")
@Expose
private String assignWh;
@SerializedName("tags")
@Expose
private Object tags;
@SerializedName("shortage")
@Expose
private String shortage;
@SerializedName("returns")
@Expose
private String returns;
@SerializedName("grn_quantity")
@Expose
private String grnQuantity;
@SerializedName("trents_picklist_id")
@Expose
private String trentsPicklistId;
@SerializedName("created")
@Expose
private String created;
@SerializedName("sgst")
@Expose
private String sgst;
@SerializedName("cgst")
@Expose
private String cgst;
@SerializedName("igst")
@Expose
private String igst;
@SerializedName("cess")
@Expose
private String cess;
@SerializedName("sgst_percentage")
@Expose
private String sgstPercentage;
@SerializedName("cgst_percentage")
@Expose
private String cgstPercentage;
@SerializedName("igst_percentage")
@Expose
private String igstPercentage;
@SerializedName("cess_percentage")
@Expose
private String cessPercentage;
@SerializedName("hsn_id")
@Expose
private Object hsnId;
@SerializedName("shipping_igst")
@Expose
private String shippingIgst;
@SerializedName("shipping_sgst")
@Expose
private String shippingSgst;
@SerializedName("shipping_cgst")
@Expose
private String shippingCgst;
@SerializedName("shipping_cgst_percentage")
@Expose
private String shippingCgstPercentage;
@SerializedName("shipping_sgst_percentage")
@Expose
private String shippingSgstPercentage;
@SerializedName("shipping_igst_percentage")
@Expose
private String shippingIgstPercentage;
@SerializedName("substitute_product_id")
@Expose
private String substituteProductId;
@SerializedName("weight")
@Expose
private String weight;
@SerializedName("order")
@Expose
private String order;
@SerializedName("product")
@Expose
private String product;

public Integer getId() {
return id;
}

public void setId(Integer id) {
this.id = id;
}

public String getWarehouseId() {
return warehouseId;
}

public void setWarehouseId(String warehouseId) {
this.warehouseId = warehouseId;
}

public String getQuantity() {
return quantity;
}

public void setQuantity(String quantity) {
this.quantity = quantity;
}

public String getDeletedQuantity() {
return deletedQuantity;
}

public void setDeletedQuantity(String deletedQuantity) {
this.deletedQuantity = deletedQuantity;
}

public String getCostPrice() {
return costPrice;
}

public void setCostPrice(String costPrice) {
this.costPrice = costPrice;
}

public String getMrp() {
return mrp;
}

public void setMrp(String mrp) {
this.mrp = mrp;
}

public Double getProductPrice() {
return productPrice;
}

public void setProductPrice(Double productPrice) {
this.productPrice = productPrice;
}

public String getProductDiscountPrice() {
return productDiscountPrice;
}

public void setProductDiscountPrice(String productDiscountPrice) {
this.productDiscountPrice = productDiscountPrice;
}

public Object getProductDiscountName() {
return productDiscountName;
}

public void setProductDiscountName(Object productDiscountName) {
this.productDiscountName = productDiscountName;
}

public Object getProductDiscType() {
return productDiscType;
}

public void setProductDiscType(Object productDiscType) {
this.productDiscType = productDiscType;
}

public String getProductDiscountRate() {
return productDiscountRate;
}

public void setProductDiscountRate(String productDiscountRate) {
this.productDiscountRate = productDiscountRate;
}

public String getProductExciseDuty() {
return productExciseDuty;
}

public void setProductExciseDuty(String productExciseDuty) {
this.productExciseDuty = productExciseDuty;
}

public Object getExciseDutyPer() {
return exciseDutyPer;
}

public void setExciseDutyPer(Object exciseDutyPer) {
this.exciseDutyPer = exciseDutyPer;
}

public String getProductTaxPrice() {
return productTaxPrice;
}

public void setProductTaxPrice(String productTaxPrice) {
this.productTaxPrice = productTaxPrice;
}

public String getTaxPercentage() {
return taxPercentage;
}

public void setTaxPercentage(String taxPercentage) {
this.taxPercentage = taxPercentage;
}

public Object getTaxName() {
return taxName;
}

public void setTaxName(Object taxName) {
this.taxName = taxName;
}

public String getStatus() {
return status;
}

public void setStatus(String status) {
this.status = status;
}

public String getProductPriceBase() {
return productPriceBase;
}

public void setProductPriceBase(String productPriceBase) {
this.productPriceBase = productPriceBase;
}

public String getProductDiscountPriceBase() {
return productDiscountPriceBase;
}

public void setProductDiscountPriceBase(String productDiscountPriceBase) {
this.productDiscountPriceBase = productDiscountPriceBase;
}

public String getShippingPrice() {
return shippingPrice;
}

public void setShippingPrice(String shippingPrice) {
this.shippingPrice = shippingPrice;
}

public String getShippingPriceBase() {
return shippingPriceBase;
}

public void setShippingPriceBase(String shippingPriceBase) {
this.shippingPriceBase = shippingPriceBase;
}

public String getShippingTax() {
return shippingTax;
}

public void setShippingTax(String shippingTax) {
this.shippingTax = shippingTax;
}

public String getShippingTaxBase() {
return shippingTaxBase;
}

public void setShippingTaxBase(String shippingTaxBase) {
this.shippingTaxBase = shippingTaxBase;
}

public String getGiftwrapPrice() {
return giftwrapPrice;
}

public void setGiftwrapPrice(String giftwrapPrice) {
this.giftwrapPrice = giftwrapPrice;
}

public String getGiftwrapPriceBase() {
return giftwrapPriceBase;
}

public void setGiftwrapPriceBase(String giftwrapPriceBase) {
this.giftwrapPriceBase = giftwrapPriceBase;
}

public String getGiftwrapTax() {
return giftwrapTax;
}

public void setGiftwrapTax(String giftwrapTax) {
this.giftwrapTax = giftwrapTax;
}

public String getGiftwrapTaxBase() {
return giftwrapTaxBase;
}

public void setGiftwrapTaxBase(String giftwrapTaxBase) {
this.giftwrapTaxBase = giftwrapTaxBase;
}

public String getShippingDiscount() {
return shippingDiscount;
}

public void setShippingDiscount(String shippingDiscount) {
this.shippingDiscount = shippingDiscount;
}

public String getShippingDiscountBase() {
return shippingDiscountBase;
}

public void setShippingDiscountBase(String shippingDiscountBase) {
this.shippingDiscountBase = shippingDiscountBase;
}

public String getAssignTo() {
return assignTo;
}

public void setAssignTo(String assignTo) {
this.assignTo = assignTo;
}

public String getAssignWh() {
return assignWh;
}

public void setAssignWh(String assignWh) {
this.assignWh = assignWh;
}

public Object getTags() {
return tags;
}

public void setTags(Object tags) {
this.tags = tags;
}

public String getShortage() {
return shortage;
}

public void setShortage(String shortage) {
this.shortage = shortage;
}

public String getReturns() {
return returns;
}

public void setReturns(String returns) {
this.returns = returns;
}

public String getGrnQuantity() {
return grnQuantity;
}

public void setGrnQuantity(String grnQuantity) {
this.grnQuantity = grnQuantity;
}

public String getTrentsPicklistId() {
return trentsPicklistId;
}

public void setTrentsPicklistId(String trentsPicklistId) {
this.trentsPicklistId = trentsPicklistId;
}

public String getCreated() {
return created;
}

public void setCreated(String created) {
this.created = created;
}

public String getSgst() {
return sgst;
}

public void setSgst(String sgst) {
this.sgst = sgst;
}

public String getCgst() {
return cgst;
}

public void setCgst(String cgst) {
this.cgst = cgst;
}

public String getIgst() {
return igst;
}

public void setIgst(String igst) {
this.igst = igst;
}

public String getCess() {
return cess;
}

public void setCess(String cess) {
this.cess = cess;
}

public String getSgstPercentage() {
return sgstPercentage;
}

public void setSgstPercentage(String sgstPercentage) {
this.sgstPercentage = sgstPercentage;
}

public String getCgstPercentage() {
return cgstPercentage;
}

public void setCgstPercentage(String cgstPercentage) {
this.cgstPercentage = cgstPercentage;
}

public String getIgstPercentage() {
return igstPercentage;
}

public void setIgstPercentage(String igstPercentage) {
this.igstPercentage = igstPercentage;
}

public String getCessPercentage() {
return cessPercentage;
}

public void setCessPercentage(String cessPercentage) {
this.cessPercentage = cessPercentage;
}

public Object getHsnId() {
return hsnId;
}

public void setHsnId(Object hsnId) {
this.hsnId = hsnId;
}

public String getShippingIgst() {
return shippingIgst;
}

public void setShippingIgst(String shippingIgst) {
this.shippingIgst = shippingIgst;
}

public String getShippingSgst() {
return shippingSgst;
}

public void setShippingSgst(String shippingSgst) {
this.shippingSgst = shippingSgst;
}

public String getShippingCgst() {
return shippingCgst;
}

public void setShippingCgst(String shippingCgst) {
this.shippingCgst = shippingCgst;
}

public String getShippingCgstPercentage() {
return shippingCgstPercentage;
}

public void setShippingCgstPercentage(String shippingCgstPercentage) {
this.shippingCgstPercentage = shippingCgstPercentage;
}

public String getShippingSgstPercentage() {
return shippingSgstPercentage;
}

public void setShippingSgstPercentage(String shippingSgstPercentage) {
this.shippingSgstPercentage = shippingSgstPercentage;
}

public String getShippingIgstPercentage() {
return shippingIgstPercentage;
}

public void setShippingIgstPercentage(String shippingIgstPercentage) {
this.shippingIgstPercentage = shippingIgstPercentage;
}

public String getSubstituteProductId() {
return substituteProductId;
}

public void setSubstituteProductId(String substituteProductId) {
this.substituteProductId = substituteProductId;
}

public String getWeight() {
return weight;
}

public void setWeight(String weight) {
this.weight = weight;
}

public String getOrder() {
return order;
}

public void setOrder(String order) {
this.order = order;
}

public String getProduct() {
return product;
}

public void setProduct(String product) {
this.product = product;
}

}