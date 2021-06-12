package com.gogrocery.Models;

import java.util.List;

public class SearchPageShopByCategory {

    private List<String> searchText;

    public SearchPageShopByCategory(String argsearchText) {
        searchText = searchText;
    }

    public SearchPageShopByCategory() {

    }

    public List<String> getSearchText() {
        return searchText;
    }


    public void setSearchText(List<String> searchText) {
        this.searchText = searchText;
    }
}
