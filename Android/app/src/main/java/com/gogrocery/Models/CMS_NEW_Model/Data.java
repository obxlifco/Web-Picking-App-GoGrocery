
package com.gogrocery.Models.CMS_NEW_Model;

import java.util.List;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Data {

    @SerializedName("carousel")
    @Expose
    private List<Carousel> carousel = null;
    @SerializedName("best_sell_product")
    @Expose
    private List<BestSellProduct> bestSellProduct = null;
    @SerializedName("Shop_By_Category")
    @Expose
    private List<ShopByCategory> shopByCategory = null;
    @SerializedName("total_widgets")
    @Expose
    private Integer totalWidgets;

    @SerializedName("deals_of_the_day")
    @Expose
    private List<DealsOfTheDay> dealsOfTheDay = null;

    public List<DealsOfTheDay> getDealsOfTheDay() {
        return dealsOfTheDay;
    }

    public void setDealsOfTheDay(List<DealsOfTheDay> dealsOfTheDay) {
        this.dealsOfTheDay = dealsOfTheDay;
    }

    @SerializedName("category_banner")
    @Expose
    private List<CategoryBanner> categoryBanners = null;


    public List<CategoryBanner> getCategoryBanners() {
        return categoryBanners;
    }

    @SerializedName("shop_by_brand")
    @Expose
    private List<ShopByBrand> shopByBrand = null;

    public List<ShopByBrand> getShopByBrand() {
        return shopByBrand;
    }

    public void setShopByBrand(List<ShopByBrand> shopByBrand) {
        this.shopByBrand = shopByBrand;
    }


    @SerializedName("product_by_categoryid")
    @Expose
    private List<ProductByCategoryid> productByCategoryid = null;

    public List<ProductByCategoryid> getProductByCategoryid() {
        return productByCategoryid;
    }

    public void setProductByCategoryid(List<ProductByCategoryid> productByCategoryid) {
        this.productByCategoryid = productByCategoryid;
    }
    public void setCategoryBanners(List<CategoryBanner> categoryBanners) {
        this.categoryBanners = categoryBanners;
    }

    public List<Carousel> getCarousel() {
        return carousel;
    }

    public void setCarousel(List<Carousel> carousel) {
        this.carousel = carousel;
    }

    public List<BestSellProduct> getBestSellProduct() {
        return bestSellProduct;
    }

    public void setBestSellProduct(List<BestSellProduct> bestSellProduct) {
        this.bestSellProduct = bestSellProduct;
    }

    public List<ShopByCategory> getShopByCategory() {
        return shopByCategory;
    }

    public void setShopByCategory(List<ShopByCategory> shopByCategory) {
        this.shopByCategory = shopByCategory;
    }

    public Integer getTotalWidgets() {
        return totalWidgets;
    }

    public void setTotalWidgets(Integer totalWidgets) {
        this.totalWidgets = totalWidgets;
    }
    @SerializedName("promotional_banner")
    @Expose
    private List<PromotionalBanner> promotionalBanner = null;

    public List<PromotionalBanner> getPromotionalBanner() {
        return promotionalBanner;
    }

    public void setPromotionalBanner(List<PromotionalBanner> promotionalBanner) {
        this.promotionalBanner = promotionalBanner;
    }

}