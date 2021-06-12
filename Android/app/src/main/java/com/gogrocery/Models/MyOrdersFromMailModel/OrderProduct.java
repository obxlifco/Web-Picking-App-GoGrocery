package com.gogrocery.Models.MyOrdersFromMailModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class OrderProduct {

@SerializedName("id")
@Expose
private String id;
@SerializedName("product")
@Expose
private Product product;
@SerializedName("invoice_product")
@Expose
private String invoiceProduct;
@SerializedName("new_default_price")
@Expose
private String newDefaultPrice;
@SerializedName("new_default_price_unit")
@Expose
private String newDefaultPriceUnit;
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
private String productPrice;
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
@SerializedName("order")
@Expose
private String order;

public String getId() {
return id;
}

public void setId(String id) {
this.id = id;
}

public Product getProduct() {
return product;
}

public void setProduct(Product product) {
this.product = product;
}

public String getInvoiceProduct() {
return invoiceProduct;
}

public void setInvoiceProduct(String invoiceProduct) {
this.invoiceProduct = invoiceProduct;
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

public String getProductPrice() {
return productPrice;
}

public void setProductPrice(String productPrice) {
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

public String getOrder() {
return order;
}

public void setOrder(String order) {
this.order = order;
}

}