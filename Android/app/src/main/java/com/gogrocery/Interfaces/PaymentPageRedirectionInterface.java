package com.gogrocery.Interfaces;

public interface PaymentPageRedirectionInterface {

    void redirect(String argOrderId,String argOrderDetail);
    void redirectTODetailPage(String argOrderId,String cust_order_id,String argOrderDetail);
    void requestForCancelOrder(String argOrderId,int argPosition);
}
