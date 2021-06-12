package com.gogrocery.Interfaces;

public interface ProductListingInterface {

     void sendSlug(String argSlug,int argProductId);
     void sendProductIdForWishlist(int argProductId,String argAction);
     void savelist(String argProductId);
}
