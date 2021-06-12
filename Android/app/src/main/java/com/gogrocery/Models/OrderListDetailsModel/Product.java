package com.gogrocery.Models.OrderListDetailsModel;

import java.util.List;

import com.gogrocery.Models.ElasticSearch.CustomField;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Product {

	@SerializedName("amazon_addstatus")
	private Object amazonAddstatus;

	@SerializedName("default_price")
	private String defaultPrice;

	@SerializedName("weight")
	private String weight;

	@SerializedName("description")
	private String description;

	@SerializedName("product_images")
	private List<ProductImagesItem> productImages;

	@SerializedName("uom")
	private Uom uom;

	@SerializedName("ean")
	private String ean;

	@SerializedName("twitter_addstatus")
	private Object twitterAddstatus;

	@SerializedName("name")
	private String name;

	@SerializedName("id")
	private int id;

	@SerializedName("sku")
	private String sku;

	@SerializedName("visibility_id")
	private int visibilityId;

	@SerializedName("brand")
	private String brand;

	@SerializedName("slug")
	private String slug;


	@SerializedName("custom_fields")
	@Expose
	private List<CustomField> customField = null;

	public List<CustomField> getCustomField() {
		return customField;
	}

	public void setCustomField(List<CustomField> customField) {
		this.customField = customField;
	}

	public Object getAmazonAddstatus() {
		return amazonAddstatus;
	}

	public void setAmazonAddstatus(Object amazonAddstatus) {
		this.amazonAddstatus = amazonAddstatus;
	}

	public String getDefaultPrice() {
		return defaultPrice;
	}

	public void setDefaultPrice(String defaultPrice) {
		this.defaultPrice = defaultPrice;
	}

	public String getWeight() {
		return weight;
	}

	public void setWeight(String weight) {
		this.weight = weight;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public List<ProductImagesItem> getProductImages() {
		return productImages;
	}

	public void setProductImages(List<ProductImagesItem> productImages) {
		this.productImages = productImages;
	}

	public Uom getUom() {
		return uom;
	}

	public void setUom(Uom uom) {
		this.uom = uom;
	}

	public String getEan() {
		return ean;
	}

	public void setEan(String ean) {
		this.ean = ean;
	}

	public Object getTwitterAddstatus() {
		return twitterAddstatus;
	}

	public void setTwitterAddstatus(Object twitterAddstatus) {
		this.twitterAddstatus = twitterAddstatus;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getSku() {
		return sku;
	}

	public void setSku(String sku) {
		this.sku = sku;
	}

	public int getVisibilityId() {
		return visibilityId;
	}

	public void setVisibilityId(int visibilityId) {
		this.visibilityId = visibilityId;
	}

	public String getBrand() {
		return brand;
	}

	public void setBrand(String brand) {
		this.brand = brand;
	}

	public String getSlug() {
		return slug;
	}

	public void setSlug(String slug) {
		this.slug = slug;
	}
}

