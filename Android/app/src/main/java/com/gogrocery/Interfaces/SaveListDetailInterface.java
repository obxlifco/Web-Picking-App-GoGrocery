package com.gogrocery.Interfaces;

public interface SaveListDetailInterface {

    void removeNullChannelPriceData(int argPosition);
    void removeItemFromWishlist(int argProductid,int argListId,int argPosition);
    public void connectMain(int argProductId,int argQuantity,int argPosition);
    void connectToDetail(int argProductId, String argSlug);
}
