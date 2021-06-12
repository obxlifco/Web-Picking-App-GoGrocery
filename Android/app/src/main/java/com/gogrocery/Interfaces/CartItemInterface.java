package com.gogrocery.Interfaces;

public interface CartItemInterface {

     void connectCartMain(int argProductId, int argQuantity,int argPosition);
    void connectCartToDetail(int argProductId, String argSlug);
}
