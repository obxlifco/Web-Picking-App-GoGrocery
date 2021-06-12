package com.gogrocery.Models.OrderListDetailsModel;

import com.gogrocery.Models.ElasticSearch.CustomField;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.List;

public class SubstituteProductsItem{

	@SerializedName("id")
	@Expose
	private Integer id;
	@SerializedName("product")
	@Expose
	private Product product;
	@SerializedName("warehouse_id")
	@Expose
	private Integer warehouseId;
	@SerializedName("quantity")
	@Expose
	private Integer quantity;
	@SerializedName("deleted_quantity")
	@Expose
	private Integer deletedQuantity;
	@SerializedName("shortage")
	@Expose
	private Integer shortage;
	@SerializedName("returns")
	@Expose
	private Integer returns;
	@SerializedName("grn_quantity")
	@Expose
	private Integer grnQuantity;
	@SerializedName("product_price")
	@Expose
	private Double productPrice;
	@SerializedName("product_discount_price")
	@Expose
	private Double productDiscountPrice;
	@SerializedName("product_discount_name")
	@Expose
	private String productDiscountName;
	@SerializedName("product_disc_type")
	@Expose
	private Integer productDiscType;
	@SerializedName("product_discount_rate")
	@Expose
	private Double productDiscountRate;
	@SerializedName("product_excise_duty")
	@Expose
	private Double productExciseDuty;
	@SerializedName("product_tax_price")
	@Expose
	private Double productTaxPrice;
	@SerializedName("tax_percentage")
	@Expose
	private Double taxPercentage;
	@SerializedName("shipping_price")
	@Expose
	private String shippingPrice;
	@SerializedName("shipping_tax")
	@Expose
	private String shippingTax;
	@SerializedName("created")
	@Expose
	private String created;
	@SerializedName("modified")
	@Expose
	private Object modified;
	@SerializedName("substitute_product_id")
	@Expose
	private Integer substituteProductId;
	@SerializedName("weight")
	@Expose
	private Double weight;
	@SerializedName("is_substitute")
	@Expose
	private String isSubstitute;
	@SerializedName("substitute_notes")
	@Expose
	private Object substituteNotes;
	@SerializedName("pick_as_substitute")
	@Expose
	private String pickAsSubstitute;
	@SerializedName("send_approval")
	@Expose
	private String sendApproval;
	@SerializedName("send_approval_interval")
	@Expose
	private Object sendApprovalInterval;
	@SerializedName("order")
	@Expose
	private String order;
	@SerializedName("created_time")
	@Expose
	private String createdTime;

	@SerializedName("custom_field_name")
	private String customFieldName;
	@SerializedName("custom_field_value")
	private String customFieldValue;

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

	public Double getProductPrice() {
		return productPrice;
	}

	public void setProductPrice(Double productPrice) {
		this.productPrice = productPrice;
	}

	public Double getProductDiscountPrice() {
		return productDiscountPrice;
	}

	public void setProductDiscountPrice(Double productDiscountPrice) {
		this.productDiscountPrice = productDiscountPrice;
	}

	public String getProductDiscountName() {
		return productDiscountName;
	}

	public void setProductDiscountName(String productDiscountName) {
		this.productDiscountName = productDiscountName;
	}

	public Integer getProductDiscType() {
		return productDiscType;
	}

	public void setProductDiscType(Integer productDiscType) {
		this.productDiscType = productDiscType;
	}

	public Double getProductDiscountRate() {
		return productDiscountRate;
	}

	public void setProductDiscountRate(Double productDiscountRate) {
		this.productDiscountRate = productDiscountRate;
	}

	public Double getProductExciseDuty() {
		return productExciseDuty;
	}

	public void setProductExciseDuty(Double productExciseDuty) {
		this.productExciseDuty = productExciseDuty;
	}

	public Double getProductTaxPrice() {
		return productTaxPrice;
	}

	public void setProductTaxPrice(Double productTaxPrice) {
		this.productTaxPrice = productTaxPrice;
	}

	public Double getTaxPercentage() {
		return taxPercentage;
	}

	public void setTaxPercentage(Double taxPercentage) {
		this.taxPercentage = taxPercentage;
	}

	public String getShippingPrice() {
		return shippingPrice;
	}

	public void setShippingPrice(String shippingPrice) {
		this.shippingPrice = shippingPrice;
	}

	public String getShippingTax() {
		return shippingTax;
	}

	public void setShippingTax(String shippingTax) {
		this.shippingTax = shippingTax;
	}

	public String getCreated() {
		return created;
	}

	public void setCreated(String created) {
		this.created = created;
	}

	public Object getModified() {
		return modified;
	}

	public void setModified(Object modified) {
		this.modified = modified;
	}

	public Integer getSubstituteProductId() {
		return substituteProductId;
	}

	public void setSubstituteProductId(Integer substituteProductId) {
		this.substituteProductId = substituteProductId;
	}

	public Double getWeight() {
		return weight;
	}

	public void setWeight(Double weight) {
		this.weight = weight;
	}

	public String getIsSubstitute() {
		return isSubstitute;
	}

	public void setIsSubstitute(String isSubstitute) {
		this.isSubstitute = isSubstitute;
	}

	public Object getSubstituteNotes() {
		return substituteNotes;
	}

	public void setSubstituteNotes(Object substituteNotes) {
		this.substituteNotes = substituteNotes;
	}

	public String getPickAsSubstitute() {
		return pickAsSubstitute;
	}

	public void setPickAsSubstitute(String pickAsSubstitute) {
		this.pickAsSubstitute = pickAsSubstitute;
	}

	public String getSendApproval() {
		return sendApproval;
	}

	public void setSendApproval(String sendApproval) {
		this.sendApproval = sendApproval;
	}

	public Object getSendApprovalInterval() {
		return sendApprovalInterval;
	}

	public void setSendApprovalInterval(Object sendApprovalInterval) {
		this.sendApprovalInterval = sendApprovalInterval;
	}

	public String getOrder() {
		return order;
	}

	public void setOrder(String order) {
		this.order = order;
	}

	public String getCreatedTime() {
		return createdTime;
	}

	public void setCreatedTime(String createdTime) {
		this.createdTime = createdTime;
	}
}