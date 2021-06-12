package com.gogrocery.Interfaces;

public interface WishlistInterface {

    void removeNullChannelPriceData(int argPosition);
    void removeItemFromWishlist(int argProductid,int argPosition);
    public void connectMain(int argProductId,int argQuantity,int argPosition);
    void connectToDetail(int argProductId, String argSlug);
}
