package com.gogrocery.Models.PaymentTransaction;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class PaymentTransactionModel {

@SerializedName("status")
@Expose
private Integer status;
@SerializedName("msg")
@Expose
private String msg;
@SerializedName("transaction_status")
@Expose
private String transactionStatus;
@SerializedName("transaction_data")
@Expose
private TransactionData transactionData;

public Integer getStatus() {
return status;
}

public void setStatus(Integer status) {
this.status = status;
}

public String getMsg() {
return msg;
}

public void setMsg(String msg) {
this.msg = msg;
}

public String getTransactionStatus() {
return transactionStatus;
}

public void setTransactionStatus(String transactionStatus) {
this.transactionStatus = transactionStatus;
}

public TransactionData getTransactionData() {
return transactionData;
}

public void setTransactionData(TransactionData transactionData) {
this.transactionData = transactionData;
}

}