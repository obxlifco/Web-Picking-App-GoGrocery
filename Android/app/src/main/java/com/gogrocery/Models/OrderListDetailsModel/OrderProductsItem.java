package com.gogrocery.Models.OrderListDetailsModel;

import java.util.List;
import com.google.gson.annotations.SerializedName;

public class OrderProductsItem{

	@SerializedName("sgst")
	private int sgst;

	@SerializedName("giftwrap_price_base")
	private String giftwrapPriceBase;

	@SerializedName("cgst_percentage")
	private String cgstPercentage;

	@SerializedName("product_price")
	private double productPrice;

	@SerializedName("substitute_products")
	private List<SubstituteProductsItem> substituteProducts;

	@SerializedName("product_discount_price")
	private String productDiscountPrice;

	@SerializedName("shortage")
	private int shortage;

	@SerializedName("hsn_id")
	private Object hsnId;

	@SerializedName("shipping_cgst_percentage")
	private int shippingCgstPercentage;

	@SerializedName("id")
	private int id;

	@SerializedName("shipping_price_base")
	private String shippingPriceBase;

	@SerializedName("order")
	private int order;

	@SerializedName("shipping_price")
	private String shippingPrice;

	@SerializedName("shipping_tax_base")
	private String shippingTaxBase;

	@SerializedName("created")
	private String created;

	@SerializedName("excise_duty_per")
	private Object exciseDutyPer;

	@SerializedName("weight")
	private String weight;

	@SerializedName("assign_wh")
	private int assignWh;

	@SerializedName("shipping_igst")
	private int shippingIgst;

	@SerializedName("tags")
	private Object tags;

	@SerializedName("shipping_igst_percentage")
	private int shippingIgstPercentage;

	@SerializedName("product_disc_type")
	private int productDiscType;

	@SerializedName("trents_picklist_id")
	private int trentsPicklistId;

	@SerializedName("giftwrap_tax_base")
	private String giftwrapTaxBase;

	@SerializedName("pick_as_substitute")
	private String pickAsSubstitute;

	@SerializedName("returns")
	private int returns;

	@SerializedName("status")
	private int status;

	@SerializedName("maximum_substitute_limit")
	private int maximumSubstituteLimit;

	@SerializedName("giftwrap_price")
	private String giftwrapPrice;

	@SerializedName("product_price_base")
	private double productPriceBase;

	@SerializedName("shipping_sgst")
	private String shippingSgst;

	@SerializedName("assign_to")
	private int assignTo;

	@SerializedName("cess_percentage")
	private String cessPercentage;

	@SerializedName("product_discount_name")
	private String productDiscountName;

	@SerializedName("grn_quantity")
	private int grnQuantity;

	@SerializedName("minimum_substitute_limit")
	private int minimumSubstituteLimit;

	@SerializedName("shipping_discount_base")
	private String shippingDiscountBase;

	@SerializedName("igst")
	private int igst;

	@SerializedName("shipping_sgst_percentage")
	private String shippingSgstPercentage;

	@SerializedName("product_tax_price")
	private String productTaxPrice;

	@SerializedName("igst_percentage")
	private String igstPercentage;

	@SerializedName("cost_price")
	private double costPrice;

	@SerializedName("shipping_tax")
	private String shippingTax;

	@SerializedName("product")
	private Product product;

	@SerializedName("quantity")
	private int quantity;

	@SerializedName("substitute_product_id")
	private int substituteProductId;

	@SerializedName("tax_name")
	private Object taxName;

	@SerializedName("product_discount_price_base")
	private String productDiscountPriceBase;

	@SerializedName("mrp")
	private double mrp;

	@SerializedName("cgst")
	private int cgst;

	@SerializedName("send_approval")
	private Object sendApproval;

	@SerializedName("cess")
	private int cess;

	@SerializedName("shipping_cgst")
	private int shippingCgst;

	@SerializedName("is_substitute")
	private String isSubstitute;

	@SerializedName("deleted_quantity")
	private int deletedQuantity;

	@SerializedName("shipping_discount")
	private String shippingDiscount;

	@SerializedName("sgst_percentage")
	private String sgstPercentage;

	@SerializedName("tax_percentage")
	private String taxPercentage;

	@SerializedName("substitute_notes")
	private String substituteNotes;

	@SerializedName("product_discount_rate")
	private String productDiscountRate;

	@SerializedName("giftwrap_tax")
	private String giftwrapTax;

	@SerializedName("created_time")
	private String created_time;

	@SerializedName("warehouse_id")
	private int warehouseId;

	@SerializedName("product_excise_duty")
	private String productExciseDuty;
	@SerializedName("custom_field_name")
	private String customFieldName;
	@SerializedName("custom_field_value")
	private String customFieldValue;

	public int getSgst(){
		return sgst;
	}

	public String getGiftwrapPriceBase(){
		return giftwrapPriceBase;
	}

	public String getCgstPercentage(){
		return cgstPercentage;
	}

	public double getProductPrice(){
		return productPrice;
	}

	public List<SubstituteProductsItem> getSubstituteProducts(){
		return substituteProducts;
	}

	public String getProductDiscountPrice(){
		return productDiscountPrice;
	}

	public int getShortage(){
		return shortage;
	}

	public Object getHsnId(){
		return hsnId;
	}

	public int getShippingCgstPercentage(){
		return shippingCgstPercentage;
	}

	public int getId(){
		return id;
	}

	public String getShippingPriceBase(){
		return shippingPriceBase;
	}

	public int getOrder(){
		return order;
	}

	public String getShippingPrice(){
		return shippingPrice;
	}

	public String getShippingTaxBase(){
		return shippingTaxBase;
	}

	public String getCreated(){
		return created;
	}

	public Object getExciseDutyPer(){
		return exciseDutyPer;
	}

	public String  getWeight(){
		return weight;
	}

	public int getAssignWh(){
		return assignWh;
	}

	public int getShippingIgst(){
		return shippingIgst;
	}

	public Object getTags(){
		return tags;
	}

	public int getShippingIgstPercentage(){
		return shippingIgstPercentage;
	}

	public int getProductDiscType(){
		return productDiscType;
	}

	public int getTrentsPicklistId(){
		return trentsPicklistId;
	}

	public String getGiftwrapTaxBase(){
		return giftwrapTaxBase;
	}

	public String getPickAsSubstitute(){
		return pickAsSubstitute;
	}

	public int getReturns(){
		return returns;
	}

	public int getStatus(){
		return status;
	}

	public int getMaximumSubstituteLimit(){
		return maximumSubstituteLimit;
	}

	public String getGiftwrapPrice(){
		return giftwrapPrice;
	}

	public double getProductPriceBase(){
		return productPriceBase;
	}

	public String getShippingSgst(){
		return shippingSgst;
	}

	public int getAssignTo(){
		return assignTo;
	}

	public String getCessPercentage(){
		return cessPercentage;
	}

	public String getProductDiscountName(){
		return productDiscountName;
	}

	public int getGrnQuantity(){
		return grnQuantity;
	}

	public int getMinimumSubstituteLimit(){
		return minimumSubstituteLimit;
	}

	public String getShippingDiscountBase(){
		return shippingDiscountBase;
	}

	public int getIgst(){
		return igst;
	}

	public String getShippingSgstPercentage(){
		return shippingSgstPercentage;
	}

	public String getProductTaxPrice(){
		return productTaxPrice;
	}

	public String getIgstPercentage(){
		return igstPercentage;
	}

	public double getCostPrice(){
		return costPrice;
	}

	public String getShippingTax(){
		return shippingTax;
	}

	public Product getProduct(){
		return product;
	}

	public int getQuantity(){
		return quantity;
	}

	public int getSubstituteProductId(){
		return substituteProductId;
	}

	public Object getTaxName(){
		return taxName;
	}

	public String getProductDiscountPriceBase(){
		return productDiscountPriceBase;
	}

	public double getMrp(){
		return mrp;
	}

	public int getCgst(){
		return cgst;
	}

	public Object getSendApproval(){
		return sendApproval;
	}

	public int getCess(){
		return cess;
	}

	public int getShippingCgst(){
		return shippingCgst;
	}

	public String getIsSubstitute(){
		return isSubstitute;
	}

	public int getDeletedQuantity(){
		return deletedQuantity;
	}

	public String getShippingDiscount(){
		return shippingDiscount;
	}

	public String getSgstPercentage(){
		return sgstPercentage;
	}

	public String getTaxPercentage(){
		return taxPercentage;
	}

	public String getSubstituteNotes(){
		return substituteNotes;
	}

	public String getProductDiscountRate(){
		return productDiscountRate;
	}

	public String getGiftwrapTax(){
		return giftwrapTax;
	}

	public int getWarehouseId(){
		return warehouseId;
	}

	public String getProductExciseDuty(){
		return productExciseDuty;
	}

	public void setSgst(int sgst) {
		this.sgst = sgst;
	}

	public void setGiftwrapPriceBase(String giftwrapPriceBase) {
		this.giftwrapPriceBase = giftwrapPriceBase;
	}

	public void setCgstPercentage(String cgstPercentage) {
		this.cgstPercentage = cgstPercentage;
	}

	public void setProductPrice(double productPrice) {
		this.productPrice = productPrice;
	}

	public void setSubstituteProducts(List<SubstituteProductsItem> substituteProducts) {
		this.substituteProducts = substituteProducts;
	}

	public void setProductDiscountPrice(String productDiscountPrice) {
		this.productDiscountPrice = productDiscountPrice;
	}

	public void setShortage(int shortage) {
		this.shortage = shortage;
	}

	public void setHsnId(Object hsnId) {
		this.hsnId = hsnId;
	}

	public void setShippingCgstPercentage(int shippingCgstPercentage) {
		this.shippingCgstPercentage = shippingCgstPercentage;
	}

	public void setId(int id) {
		this.id = id;
	}

	public void setShippingPriceBase(String shippingPriceBase) {
		this.shippingPriceBase = shippingPriceBase;
	}

	public void setOrder(int order) {
		this.order = order;
	}

	public void setShippingPrice(String shippingPrice) {
		this.shippingPrice = shippingPrice;
	}

	public void setShippingTaxBase(String shippingTaxBase) {
		this.shippingTaxBase = shippingTaxBase;
	}

	public void setCreated(String created) {
		this.created = created;
	}

	public void setExciseDutyPer(Object exciseDutyPer) {
		this.exciseDutyPer = exciseDutyPer;
	}

	public void setWeight(String weight) {
		this.weight = weight;
	}

	public void setAssignWh(int assignWh) {
		this.assignWh = assignWh;
	}

	public void setShippingIgst(int shippingIgst) {
		this.shippingIgst = shippingIgst;
	}

	public void setTags(Object tags) {
		this.tags = tags;
	}

	public void setShippingIgstPercentage(int shippingIgstPercentage) {
		this.shippingIgstPercentage = shippingIgstPercentage;
	}

	public void setProductDiscType(int productDiscType) {
		this.productDiscType = productDiscType;
	}

	public void setTrentsPicklistId(int trentsPicklistId) {
		this.trentsPicklistId = trentsPicklistId;
	}

	public void setGiftwrapTaxBase(String giftwrapTaxBase) {
		this.giftwrapTaxBase = giftwrapTaxBase;
	}

	public void setPickAsSubstitute(String pickAsSubstitute) {
		this.pickAsSubstitute = pickAsSubstitute;
	}

	public void setReturns(int returns) {
		this.returns = returns;
	}

	public void setStatus(int status) {
		this.status = status;
	}

	public void setMaximumSubstituteLimit(int maximumSubstituteLimit) {
		this.maximumSubstituteLimit = maximumSubstituteLimit;
	}

	public void setGiftwrapPrice(String giftwrapPrice) {
		this.giftwrapPrice = giftwrapPrice;
	}

	public void setProductPriceBase(double productPriceBase) {
		this.productPriceBase = productPriceBase;
	}

	public void setShippingSgst(String shippingSgst) {
		this.shippingSgst = shippingSgst;
	}

	public void setAssignTo(int assignTo) {
		this.assignTo = assignTo;
	}

	public void setCessPercentage(String cessPercentage) {
		this.cessPercentage = cessPercentage;
	}

	public void setProductDiscountName(String productDiscountName) {
		this.productDiscountName = productDiscountName;
	}

	public void setGrnQuantity(int grnQuantity) {
		this.grnQuantity = grnQuantity;
	}

	public void setMinimumSubstituteLimit(int minimumSubstituteLimit) {
		this.minimumSubstituteLimit = minimumSubstituteLimit;
	}

	public void setShippingDiscountBase(String shippingDiscountBase) {
		this.shippingDiscountBase = shippingDiscountBase;
	}

	public void setIgst(int igst) {
		this.igst = igst;
	}

	public void setShippingSgstPercentage(String shippingSgstPercentage) {
		this.shippingSgstPercentage = shippingSgstPercentage;
	}

	public void setProductTaxPrice(String productTaxPrice) {
		this.productTaxPrice = productTaxPrice;
	}

	public void setIgstPercentage(String igstPercentage) {
		this.igstPercentage = igstPercentage;
	}

	public void setCostPrice(double costPrice) {
		this.costPrice = costPrice;
	}

	public void setShippingTax(String shippingTax) {
		this.shippingTax = shippingTax;
	}

	public void setProduct(Product product) {
		this.product = product;
	}

	public void setQuantity(int quantity) {
		this.quantity = quantity;
	}

	public void setSubstituteProductId(int substituteProductId) {
		this.substituteProductId = substituteProductId;
	}

	public void setTaxName(Object taxName) {
		this.taxName = taxName;
	}

	public void setProductDiscountPriceBase(String productDiscountPriceBase) {
		this.productDiscountPriceBase = productDiscountPriceBase;
	}

	public void setMrp(double mrp) {
		this.mrp = mrp;
	}

	public void setCgst(int cgst) {
		this.cgst = cgst;
	}

	public void setSendApproval(Object sendApproval) {
		this.sendApproval = sendApproval;
	}

	public void setCess(int cess) {
		this.cess = cess;
	}

	public void setShippingCgst(int shippingCgst) {
		this.shippingCgst = shippingCgst;
	}

	public void setIsSubstitute(String isSubstitute) {
		this.isSubstitute = isSubstitute;
	}

	public void setDeletedQuantity(int deletedQuantity) {
		this.deletedQuantity = deletedQuantity;
	}

	public void setShippingDiscount(String shippingDiscount) {
		this.shippingDiscount = shippingDiscount;
	}

	public void setSgstPercentage(String sgstPercentage) {
		this.sgstPercentage = sgstPercentage;
	}

	public void setTaxPercentage(String taxPercentage) {
		this.taxPercentage = taxPercentage;
	}

	public void setSubstituteNotes(String substituteNotes) {
		this.substituteNotes = substituteNotes;
	}

	public void setProductDiscountRate(String productDiscountRate) {
		this.productDiscountRate = productDiscountRate;
	}

	public void setGiftwrapTax(String giftwrapTax) {
		this.giftwrapTax = giftwrapTax;
	}

	public String getCreated_time() {
		return created_time;
	}

	public void setCreated_time(String created_time) {
		this.created_time = created_time;
	}

	public void setWarehouseId(int warehouseId) {
		this.warehouseId = warehouseId;
	}

	public void setProductExciseDuty(String productExciseDuty) {
		this.productExciseDuty = productExciseDuty;
	}

	public String getCustomFieldName() {
		return customFieldName;
	}

	public void setCustomFieldName(String customFieldName) {
		this.customFieldName = customFieldName;
	}

	public String getCustomFieldValue() {
		return customFieldValue;
	}

	public void setCustomFieldValue(String customFieldValue) {
		this.customFieldValue = customFieldValue;
	}
}