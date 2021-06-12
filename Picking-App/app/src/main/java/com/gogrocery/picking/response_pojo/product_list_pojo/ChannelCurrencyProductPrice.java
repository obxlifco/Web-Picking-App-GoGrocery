package com.gogrocery.picking.response_pojo.product_list_pojo;

import javax.annotation.Generated;
import com.google.gson.annotations.SerializedName;

@Generated("com.robohorse.robopojogenerator")
public class ChannelCurrencyProductPrice{

	@SerializedName("end_date")
	private Object endDate;

	@SerializedName("product")
	private int product;

	@SerializedName("cost")
	private Double cost;

	@SerializedName("max_quantity")
	private int maxQuantity;

	@SerializedName("mrp")
	private Double mrp;

	@SerializedName("promotions")
	private Object promotions;

	@SerializedName("min_quantity")
	private int minQuantity;

	@SerializedName("price")
	private Double price;

	@SerializedName("price_type")
	private int priceType;

	@SerializedName("id")
	private int id;

	@SerializedName("product_price_type")
	private int productPriceType;

	@SerializedName("channel_id")
	private int channelId;

	@SerializedName("website_id")
	private Object websiteId;

	@SerializedName("currency_id")
	private Object currencyId;

	@SerializedName("warehouse_id")
	private int warehouseId;

	@SerializedName("start_date")
	private String startDate;

	public void setEndDate(Object endDate){
		this.endDate = endDate;
	}

	public Object getEndDate(){
		return endDate;
	}

	public void setProduct(int product){
		this.product = product;
	}

	public int getProduct(){
		return product;
	}

	public void setCost(Double cost){
		this.cost = cost;
	}

	public Double getCost(){
		return cost;
	}

	public void setMaxQuantity(int maxQuantity){
		this.maxQuantity = maxQuantity;
	}

	public int getMaxQuantity(){
		return maxQuantity;
	}

	public void setMrp(Double mrp){
		this.mrp = mrp;
	}

	public Double getMrp(){
		return mrp;
	}

	public void setPromotions(Object promotions){
		this.promotions = promotions;
	}

	public Object getPromotions(){
		return promotions;
	}

	public void setMinQuantity(int minQuantity){
		this.minQuantity = minQuantity;
	}

	public int getMinQuantity(){
		return minQuantity;
	}

	public void setPrice(Double price){
		this.price = price;
	}

	public Double getPrice(){
		return price;
	}

	public void setPriceType(int priceType){
		this.priceType = priceType;
	}

	public int getPriceType(){
		return priceType;
	}

	public void setId(int id){
		this.id = id;
	}

	public int getId(){
		return id;
	}

	public void setProductPriceType(int productPriceType){
		this.productPriceType = productPriceType;
	}

	public int getProductPriceType(){
		return productPriceType;
	}

	public void setChannelId(int channelId){
		this.channelId = channelId;
	}

	public int getChannelId(){
		return channelId;
	}

	public void setWebsiteId(Object websiteId){
		this.websiteId = websiteId;
	}

	public Object getWebsiteId(){
		return websiteId;
	}

	public void setCurrencyId(Object currencyId){
		this.currencyId = currencyId;
	}

	public Object getCurrencyId(){
		return currencyId;
	}

	public void setWarehouseId(int warehouseId){
		this.warehouseId = warehouseId;
	}

	public int getWarehouseId(){
		return warehouseId;
	}

	public void setStartDate(String startDate){
		this.startDate = startDate;
	}

	public String getStartDate(){
		return startDate;
	}

	@Override
 	public String toString(){
		return 
			"ChannelCurrencyProductPrice{" + 
			"end_date = '" + endDate + '\'' + 
			",product = '" + product + '\'' + 
			",cost = '" + cost + '\'' + 
			",max_quantity = '" + maxQuantity + '\'' + 
			",mrp = '" + mrp + '\'' + 
			",promotions = '" + promotions + '\'' + 
			",min_quantity = '" + minQuantity + '\'' + 
			",price = '" + price + '\'' + 
			",price_type = '" + priceType + '\'' + 
			",id = '" + id + '\'' + 
			",product_price_type = '" + productPriceType + '\'' + 
			",channel_id = '" + channelId + '\'' + 
			",website_id = '" + websiteId + '\'' + 
			",currency_id = '" + currencyId + '\'' + 
			",warehouse_id = '" + warehouseId + '\'' + 
			",start_date = '" + startDate + '\'' + 
			"}";
		}
}