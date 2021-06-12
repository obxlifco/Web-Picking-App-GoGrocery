package com.gogrocery.Models.ApplyLoyaltyResponseModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class OrderProduct {

@SerializedName("id")
@Expose
private Integer id;
@SerializedName("product")
@Expose
private Product product;
@SerializedName("invoice_product")
@Expose
private Integer invoiceProduct;
@SerializedName("new_default_price")
@Expose
private Integer newDefaultPrice;
@SerializedName("new_default_price_unit")
@Expose
private Integer newDefaultPriceUnit;
@SerializedName("warehouse_id")
@Expose
private Integer warehouseId;
@SerializedName("quantity")
@Expose
private Integer quantity;
@SerializedName("deleted_quantity")
@Expose
private Integer deletedQuantity;
@SerializedName("cost_price")
@Expose
private Integer costPrice;
@SerializedName("mrp")
@Expose
private Integer mrp;
@SerializedName("product_price")
@Expose
private Integer productPrice;
@SerializedName("product_discount_price")
@Expose
private Integer productDiscountPrice;
@SerializedName("product_discount_name")
@Expose
private Object productDiscountName;
@SerializedName("product_disc_type")
@Expose
private Object productDiscType;
@SerializedName("product_discount_rate")
@Expose
private Integer productDiscountRate;
@SerializedName("product_excise_duty")
@Expose
private Integer productExciseDuty;
@SerializedName("excise_duty_per")
@Expose
private Object exciseDutyPer;
@SerializedName("product_tax_price")
@Expose
private Integer productTaxPrice;
@SerializedName("tax_percentage")
@Expose
private Integer taxPercentage;
@SerializedName("tax_name")
@Expose
private Object taxName;
@SerializedName("status")
@Expose
private Integer status;
@SerializedName("product_price_base")
@Expose
private Integer productPriceBase;
@SerializedName("product_discount_price_base")
@Expose
private Integer productDiscountPriceBase;
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
private Integer assignTo;
@SerializedName("assign_wh")
@Expose
private Integer assignWh;
@SerializedName("tags")
@Expose
private Object tags;
@SerializedName("shortage")
@Expose
private Integer shortage;
@SerializedName("returns")
@Expose
private Integer returns;
@SerializedName("grn_quantity")
@Expose
private Integer grnQuantity;
@SerializedName("trents_picklist_id")
@Expose
private Integer trentsPicklistId;
@SerializedName("created")
@Expose
private String created;
@SerializedName("sgst")
@Expose
private Integer sgst;
@SerializedName("cgst")
@Expose
private Integer cgst;
@SerializedName("igst")
@Expose
private Integer igst;
@SerializedName("cess")
@Expose
private Integer cess;
@SerializedName("sgst_percentage")
@Expose
private Integer sgstPercentage;
@SerializedName("cgst_percentage")
@Expose
private Integer cgstPercentage;
@SerializedName("igst_percentage")
@Expose
private Integer igstPercentage;
@SerializedName("cess_percentage")
@Expose
private Integer cessPercentage;
@SerializedName("hsn_id")
@Expose
private Object hsnId;
@SerializedName("shipping_igst")
@Expose
private Integer shippingIgst;
@SerializedName("shipping_sgst")
@Expose
private Integer shippingSgst;
@SerializedName("shipping_cgst")
@Expose
private Integer shippingCgst;
@SerializedName("shipping_cgst_percentage")
@Expose
private Integer shippingCgstPercentage;
@SerializedName("shipping_sgst_percentage")
@Expose
private Integer shippingSgstPercentage;
@SerializedName("shipping_igst_percentage")
@Expose
private Integer shippingIgstPercentage;
@SerializedName("substitute_product_id")
@Expose
private Integer substituteProductId;
@SerializedName("weight")
@Expose
private String weight;
@SerializedName("order")
@Expose
private Integer order;

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

public Integer getInvoiceProduct() {
return invoiceProduct;
}

public void setInvoiceProduct(Integer invoiceProduct) {
this.invoiceProduct = invoiceProduct;
}

public Integer getNewDefaultPrice() {
return newDefaultPrice;
}

public void setNewDefaultPrice(Integer newDefaultPrice) {
this.newDefaultPrice = newDefaultPrice;
}

public Integer getNewDefaultPriceUnit() {
return newDefaultPriceUnit;
}

public void setNewDefaultPriceUnit(Integer newDefaultPriceUnit) {
this.newDefaultPriceUnit = newDefaultPriceUnit;
}

public Integer getWarehouseId() {
return warehouseId;
}

public void setWarehouseId(Integer warehouseId) {
this.warehouseId = warehouseId;
}

public Integer getQuantity() {
return quantity;
}

public void setQuantity(Integer quantity) {
this.quantity = quantity;
}

public Integer getDeletedQuantity() {
return deletedQuantity;
}

public void setDeletedQuantity(Integer deletedQuantity) {
this.deletedQuantity = deletedQuantity;
}

public Integer getCostPrice() {
return costPrice;
}

public void setCostPrice(Integer costPrice) {
this.costPrice = costPrice;
}

public Integer getMrp() {
return mrp;
}

public void setMrp(Integer mrp) {
this.mrp = mrp;
}

public Integer getProductPrice() {
return productPrice;
}

public void setProductPrice(Integer productPrice) {
this.productPrice = productPrice;
}

public Integer getProductDiscountPrice() {
return productDiscountPrice;
}

public void setProductDiscountPrice(Integer productDiscountPrice) {
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

public Integer getProductDiscountRate() {
return productDiscountRate;
}

public void setProductDiscountRate(Integer productDiscountRate) {
this.productDiscountRate = productDiscountRate;
}

public Integer getProductExciseDuty() {
return productExciseDuty;
}

public void setProductExciseDuty(Integer productExciseDuty) {
this.productExciseDuty = productExciseDuty;
}

public Object getExciseDutyPer() {
return exciseDutyPer;
}

public void setExciseDutyPer(Object exciseDutyPer) {
this.exciseDutyPer = exciseDutyPer;
}

public Integer getProductTaxPrice() {
return productTaxPrice;
}

public void setProductTaxPrice(Integer productTaxPrice) {
this.productTaxPrice = productTaxPrice;
}

public Integer getTaxPercentage() {
return taxPercentage;
}

public void setTaxPercentage(Integer taxPercentage) {
this.taxPercentage = taxPercentage;
}

public Object getTaxName() {
return taxName;
}

public void setTaxName(Object taxName) {
this.taxName = taxName;
}

public Integer getStatus() {
return status;
}

public void setStatus(Integer status) {
this.status = status;
}

public Integer getProductPriceBase() {
return productPriceBase;
}

public void setProductPriceBase(Integer productPriceBase) {
this.productPriceBase = productPriceBase;
}

public Integer getProductDiscountPriceBase() {
return productDiscountPriceBase;
}

public void setProductDiscountPriceBase(Integer productDiscountPriceBase) {
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

public Integer getAssignTo() {
return assignTo;
}

public void setAssignTo(Integer assignTo) {
this.assignTo = assignTo;
}

public Integer getAssignWh() {
return assignWh;
}

public void setAssignWh(Integer assignWh) {
this.assignWh = assignWh;
}

public Object getTags() {
return tags;
}

public void setTags(Object tags) {
this.tags = tags;
}

public Integer getShortage() {
return shortage;
}

public void setShortage(Integer shortage) {
this.shortage = shortage;
}

public Integer getReturns() {
return returns;
}

public void setReturns(Integer returns) {
this.returns = returns;
}

public Integer getGrnQuantity() {
return grnQuantity;
}

public void setGrnQuantity(Integer grnQuantity) {
this.grnQuantity = grnQuantity;
}

public Integer getTrentsPicklistId() {
return trentsPicklistId;
}

public void setTrentsPicklistId(Integer trentsPicklistId) {
this.trentsPicklistId = trentsPicklistId;
}

public String getCreated() {
return created;
}

public void setCreated(String created) {
this.created = created;
}

public Integer getSgst() {
return sgst;
}

public void setSgst(Integer sgst) {
this.sgst = sgst;
}

public Integer getCgst() {
return cgst;
}

public void setCgst(Integer cgst) {
this.cgst = cgst;
}

public Integer getIgst() {
return igst;
}

public void setIgst(Integer igst) {
this.igst = igst;
}

public Integer getCess() {
return cess;
}

public void setCess(Integer cess) {
this.cess = cess;
}

public Integer getSgstPercentage() {
return sgstPercentage;
}

public void setSgstPercentage(Integer sgstPercentage) {
this.sgstPercentage = sgstPercentage;
}

public Integer getCgstPercentage() {
return cgstPercentage;
}

public void setCgstPercentage(Integer cgstPercentage) {
this.cgstPercentage = cgstPercentage;
}

public Integer getIgstPercentage() {
return igstPercentage;
}

public void setIgstPercentage(Integer igstPercentage) {
this.igstPercentage = igstPercentage;
}

public Integer getCessPercentage() {
return cessPercentage;
}

public void setCessPercentage(Integer cessPercentage) {
this.cessPercentage = cessPercentage;
}

public Object getHsnId() {
return hsnId;
}

public void setHsnId(Object hsnId) {
this.hsnId = hsnId;
}

public Integer getShippingIgst() {
return shippingIgst;
}

public void setShippingIgst(Integer shippingIgst) {
this.shippingIgst = shippingIgst;
}

public Integer getShippingSgst() {
return shippingSgst;
}

public void setShippingSgst(Integer shippingSgst) {
this.shippingSgst = shippingSgst;
}

public Integer getShippingCgst() {
return shippingCgst;
}

public void setShippingCgst(Integer shippingCgst) {
this.shippingCgst = shippingCgst;
}

public Integer getShippingCgstPercentage() {
return shippingCgstPercentage;
}

public void setShippingCgstPercentage(Integer shippingCgstPercentage) {
this.shippingCgstPercentage = shippingCgstPercentage;
}

public Integer getShippingSgstPercentage() {
return shippingSgstPercentage;
}

public void setShippingSgstPercentage(Integer shippingSgstPercentage) {
this.shippingSgstPercentage = shippingSgstPercentage;
}

public Integer getShippingIgstPercentage() {
return shippingIgstPercentage;
}

public void setShippingIgstPercentage(Integer shippingIgstPercentage) {
this.shippingIgstPercentage = shippingIgstPercentage;
}

public Integer getSubstituteProductId() {
return substituteProductId;
}

public void setSubstituteProductId(Integer substituteProductId) {
this.substituteProductId = substituteProductId;
}

public String getWeight() {
return weight;
}

public void setWeight(String weight) {
this.weight = weight;
}

public Integer getOrder() {
return order;
}

public void setOrder(Integer order) {
this.order = order;
}

}