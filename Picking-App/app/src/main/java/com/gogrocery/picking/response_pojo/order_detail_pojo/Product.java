package com.gogrocery.picking.response_pojo.order_detail_pojo;

import java.util.List;
import javax.annotation.Generated;
import com.google.gson.annotations.SerializedName;

@Generated("com.robohorse.robopojogenerator")
public class Product{

	@SerializedName("amazon_addstatus")
	private Object amazonAddstatus;

	@SerializedName("default_price")
	private Object defaultPrice;

	@SerializedName("weight")
	private String weight;

	@SerializedName("description")
	private Object description;

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

	public void setAmazonAddstatus(Object amazonAddstatus){
		this.amazonAddstatus = amazonAddstatus;
	}

	public Object getAmazonAddstatus(){
		return amazonAddstatus;
	}

	public void setDefaultPrice(Object defaultPrice){
		this.defaultPrice = defaultPrice;
	}

	public Object getDefaultPrice(){
		return defaultPrice;
	}

	public void setWeight(String weight){
		this.weight = weight;
	}

	public String getWeight(){
		return weight;
	}

	public void setDescription(Object description){
		this.description = description;
	}

	public Object getDescription(){
		return description;
	}

	public void setProductImages(List<ProductImagesItem> productImages){
		this.productImages = productImages;
	}

	public List<ProductImagesItem> getProductImages(){
		return productImages;
	}

	public void setUom(Uom uom){
		this.uom = uom;
	}

	public Uom getUom(){
		return uom;
	}

	public void setEan(String ean){
		this.ean = ean;
	}

	public String getEan(){
		return ean;
	}

	public void setTwitterAddstatus(Object twitterAddstatus){
		this.twitterAddstatus = twitterAddstatus;
	}

	public Object getTwitterAddstatus(){
		return twitterAddstatus;
	}

	public void setName(String name){
		this.name = name;
	}

	public String getName(){
		return name;
	}

	public void setId(int id){
		this.id = id;
	}

	public int getId(){
		return id;
	}

	public void setSku(String sku){
		this.sku = sku;
	}

	public String getSku(){
		return sku;
	}

	public void setVisibilityId(int visibilityId){
		this.visibilityId = visibilityId;
	}

	public int getVisibilityId(){
		return visibilityId;
	}

	public void setBrand(String brand){
		this.brand = brand;
	}

	public String getBrand(){
		return brand;
	}

	public void setSlug(String slug){
		this.slug = slug;
	}

	public String getSlug(){
		return slug;
	}

	@Override
 	public String toString(){
		return 
			"Product{" + 
			"amazon_addstatus = '" + amazonAddstatus + '\'' + 
			",default_price = '" + defaultPrice + '\'' + 
			",weight = '" + weight + '\'' + 
			",description = '" + description + '\'' + 
			",product_images = '" + productImages + '\'' + 
			",uom = '" + uom + '\'' + 
			",ean = '" + ean + '\'' + 
			",twitter_addstatus = '" + twitterAddstatus + '\'' + 
			",name = '" + name + '\'' + 
			",id = '" + id + '\'' + 
			",sku = '" + sku + '\'' + 
			",visibility_id = '" + visibilityId + '\'' + 
			",brand = '" + brand + '\'' + 
			",slug = '" + slug + '\'' + 
			"}";
		}
}