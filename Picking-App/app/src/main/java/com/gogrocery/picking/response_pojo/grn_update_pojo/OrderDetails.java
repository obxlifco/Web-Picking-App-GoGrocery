package com.gogrocery.picking.response_pojo.grn_update_pojo;

import javax.annotation.Generated;
import com.google.gson.annotations.SerializedName;

@Generated("com.robohorse.robopojogenerator")
public class OrderDetails{

	@SerializedName("tax_amount")
	private double taxAmount;

	@SerializedName("shipping_cost")
	private double shippingCost;

	@SerializedName("cart_discount")
	private double cartDiscount;

	@SerializedName("paid_amount")
	private double paidAmount;

	@SerializedName("refund_wallet_amount")
	private double refundWalletAmount;

	@SerializedName("gross_amount")
	private double grossAmount;

	@SerializedName("net_amount")
	private double netAmount;

	@SerializedName("pay_wallet_amount")
	private double payWalletAmount;

	@SerializedName("gross_discount_amount")
	private double grossDiscountAmount;

	public void setTaxAmount(double taxAmount){
		this.taxAmount = taxAmount;
	}

	public double getTaxAmount(){
		return taxAmount;
	}

	public void setShippingCost(double shippingCost){
		this.shippingCost = shippingCost;
	}

	public double getShippingCost(){
		return shippingCost;
	}

	public void setCartDiscount(double cartDiscount){
		this.cartDiscount = cartDiscount;
	}

	public double getCartDiscount(){
		return cartDiscount;
	}

	public void setPaidAmount(double paidAmount){
		this.paidAmount = paidAmount;
	}

	public double getPaidAmount(){
		return paidAmount;
	}

	public void setRefundWalletAmount(double refundWalletAmount){
		this.refundWalletAmount = refundWalletAmount;
	}

	public double getRefundWalletAmount(){
		return refundWalletAmount;
	}

	public void setGrossAmount(double grossAmount){
		this.grossAmount = grossAmount;
	}

	public double getGrossAmount(){
		return grossAmount;
	}

	public void setNetAmount(double netAmount){
		this.netAmount = netAmount;
	}

	public double getNetAmount(){
		return netAmount;
	}

	public void setPayWalletAmount(double payWalletAmount){
		this.payWalletAmount = payWalletAmount;
	}

	public double getPayWalletAmount(){
		return payWalletAmount;
	}

	public void setGrossDiscountAmount(double grossDiscountAmount){
		this.grossDiscountAmount = grossDiscountAmount;
	}

	public double getGrossDiscountAmount(){
		return grossDiscountAmount;
	}

	@Override
 	public String toString(){
		return 
			"OrderDetails{" + 
			"tax_amount = '" + taxAmount + '\'' + 
			",shipping_cost = '" + shippingCost + '\'' + 
			",cart_discount = '" + cartDiscount + '\'' + 
			",paid_amount = '" + paidAmount + '\'' + 
			",refund_wallet_amount = '" + refundWalletAmount + '\'' + 
			",gross_amount = '" + grossAmount + '\'' + 
			",net_amount = '" + netAmount + '\'' + 
			",pay_wallet_amount = '" + payWalletAmount + '\'' + 
			",gross_discount_amount = '" + grossDiscountAmount + '\'' + 
			"}";
		}
}