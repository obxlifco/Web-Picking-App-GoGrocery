package com.gogrocery.picking.response_pojo.product_list_pojo;

import javax.annotation.Generated;
import com.google.gson.annotations.SerializedName;

@Generated("com.robohorse.robopojogenerator")
public class ProductStock{

	@SerializedName("islabel")
	private Object islabel;

	@SerializedName("avg_sales_week")
	private String avgSalesWeek;

	@SerializedName("product")
	private int product;

	@SerializedName("virtual_stock")
	private int virtualStock;

	@SerializedName("updatedby")
	private int updatedby;

	@SerializedName("avg_sales_month")
	private String avgSalesMonth;

	@SerializedName("created")
	private String created;

	@SerializedName("warehouse")
	private int warehouse;

	@SerializedName("isdeleted")
	private String isdeleted;

	@SerializedName("safety_stock")
	private int safetyStock;

	@SerializedName("isblocked")
	private String isblocked;

	@SerializedName("user_id")
	private Object userId;

	@SerializedName("createdby")
	private Object createdby;

	@SerializedName("modified")
	private String modified;

	@SerializedName("islot")
	private Object islot;

	@SerializedName("id")
	private int id;

	@SerializedName("real_stock")
	private int realStock;

	@SerializedName("stock")
	private int stock;

	@SerializedName("stock_unit")
	private int stockUnit;

	public void setIslabel(Object islabel){
		this.islabel = islabel;
	}

	public Object getIslabel(){
		return islabel;
	}

	public void setAvgSalesWeek(String avgSalesWeek){
		this.avgSalesWeek = avgSalesWeek;
	}

	public String getAvgSalesWeek(){
		return avgSalesWeek;
	}

	public void setProduct(int product){
		this.product = product;
	}

	public int getProduct(){
		return product;
	}

	public void setVirtualStock(int virtualStock){
		this.virtualStock = virtualStock;
	}

	public int getVirtualStock(){
		return virtualStock;
	}

	public void setUpdatedby(int updatedby){
		this.updatedby = updatedby;
	}

	public int getUpdatedby(){
		return updatedby;
	}

	public void setAvgSalesMonth(String avgSalesMonth){
		this.avgSalesMonth = avgSalesMonth;
	}

	public String getAvgSalesMonth(){
		return avgSalesMonth;
	}

	public void setCreated(String created){
		this.created = created;
	}

	public String getCreated(){
		return created;
	}

	public void setWarehouse(int warehouse){
		this.warehouse = warehouse;
	}

	public int getWarehouse(){
		return warehouse;
	}

	public void setIsdeleted(String isdeleted){
		this.isdeleted = isdeleted;
	}

	public String getIsdeleted(){
		return isdeleted;
	}

	public void setSafetyStock(int safetyStock){
		this.safetyStock = safetyStock;
	}

	public int getSafetyStock(){
		return safetyStock;
	}

	public void setIsblocked(String isblocked){
		this.isblocked = isblocked;
	}

	public String getIsblocked(){
		return isblocked;
	}

	public void setUserId(Object userId){
		this.userId = userId;
	}

	public Object getUserId(){
		return userId;
	}

	public void setCreatedby(Object createdby){
		this.createdby = createdby;
	}

	public Object getCreatedby(){
		return createdby;
	}

	public void setModified(String modified){
		this.modified = modified;
	}

	public String getModified(){
		return modified;
	}

	public void setIslot(Object islot){
		this.islot = islot;
	}

	public Object getIslot(){
		return islot;
	}

	public void setId(int id){
		this.id = id;
	}

	public int getId(){
		return id;
	}

	public void setRealStock(int realStock){
		this.realStock = realStock;
	}

	public int getRealStock(){
		return realStock;
	}

	public void setStock(int stock){
		this.stock = stock;
	}

	public int getStock(){
		return stock;
	}

	public void setStockUnit(int stockUnit){
		this.stockUnit = stockUnit;
	}

	public int getStockUnit(){
		return stockUnit;
	}

	@Override
 	public String toString(){
		return 
			"ProductStock{" + 
			"islabel = '" + islabel + '\'' + 
			",avg_sales_week = '" + avgSalesWeek + '\'' + 
			",product = '" + product + '\'' + 
			",virtual_stock = '" + virtualStock + '\'' + 
			",updatedby = '" + updatedby + '\'' + 
			",avg_sales_month = '" + avgSalesMonth + '\'' + 
			",created = '" + created + '\'' + 
			",warehouse = '" + warehouse + '\'' + 
			",isdeleted = '" + isdeleted + '\'' + 
			",safety_stock = '" + safetyStock + '\'' + 
			",isblocked = '" + isblocked + '\'' + 
			",user_id = '" + userId + '\'' + 
			",createdby = '" + createdby + '\'' + 
			",modified = '" + modified + '\'' + 
			",islot = '" + islot + '\'' + 
			",id = '" + id + '\'' + 
			",real_stock = '" + realStock + '\'' + 
			",stock = '" + stock + '\'' + 
			",stock_unit = '" + stockUnit + '\'' + 
			"}";
		}
}