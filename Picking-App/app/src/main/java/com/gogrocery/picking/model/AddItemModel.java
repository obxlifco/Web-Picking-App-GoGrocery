package com.gogrocery.picking.model;

public class AddItemModel {
    private int id;
    private long qty;
    private String name;
    private Double price;
    private long stock;
    private String weight;
    private String image;
    private boolean isSelect;
    private int substituteStatus;
    private String substituteMsg;

    public AddItemModel(int id, String name, Double price, long stock, String weight, String image, boolean isSelect,
                        int substituteStatus,String substituteMsg,long qty) {
        this.id = id;
        this.name = name;
        this.price = price;
        this.stock = stock;
        this.weight = weight;
        this.image = image;
        this.isSelect = isSelect;
        this.substituteStatus = substituteStatus;
        this.substituteMsg = substituteMsg;
        this.qty = qty;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Double getPrice() {
        return price;
    }

    public void setPrice(Double price) {
        this.price = price;
    }

    public long getStock() {
        return stock;
    }

    public void setStock(long stock) {
        this.stock = stock;
    }

    public String getWeight() {
        return weight;
    }

    public void setWeight(String weight) {
        this.weight = weight;
    }

    public String getImage() {
        return image;
    }

    public void setImage(String image) {
        this.image = image;
    }

    public boolean isSelect() {
        return isSelect;
    }

    public void setSelect(boolean select) {
        isSelect = select;
    }

    public int getSubstituteStatus() {
        return substituteStatus;
    }

    public void setSubstituteStatus(int substituteStatus) {
        this.substituteStatus = substituteStatus;
    }

    public String getSubstituteMsg() {
        return substituteMsg;
    }

    public void setSubstituteMsg(String substituteMsg) {
        this.substituteMsg = substituteMsg;
    }

    public long getQty() {
        return qty;
    }

    public void setQty(long qty) {
        this.qty = qty;
    }
}
