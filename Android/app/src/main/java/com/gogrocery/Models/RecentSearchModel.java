package com.gogrocery.Models;

import java.util.List;

public class RecentSearchModel {

    private List<String> searchText;

    public RecentSearchModel(String argsearchText) {
        searchText = searchText;
    }

    public RecentSearchModel() {

    }

    public List<String> getSearchText() {
        return searchText;
    }


    public void setSearchText(List<String> searchText) {
        this.searchText = searchText;
    }
}
