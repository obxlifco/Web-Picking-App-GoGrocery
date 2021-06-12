package com.gogrocery.ViewModel;

import java.io.Serializable;

public class StoreCategoryModel implements Serializable {
    private String name;
    private int id;
    private boolean isSelect;
    private int has_store;

    public StoreCategoryModel(String name, int id, boolean isSelect, int has_store) {
        this.name = name;
        this.id = id;
        this.isSelect = isSelect;
        this.has_store = has_store;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public boolean isSelect() {
        return isSelect;
    }

    public void setSelect(boolean select) {
        isSelect = select;
    }

    public int getHas_store() {
        return has_store;
    }

    public void setHas_store(int has_store) {
        this.has_store = has_store;
    }
}
