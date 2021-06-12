package com.gogrocery.Models.MyCardList;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.List;

public class CardListModel {
    @SerializedName("card_list")
    @Expose
    private List<Card> cardList = null;
    @SerializedName("status")
    @Expose
    private Integer status;

    public List<Card> getCardList() {
        return cardList;
    }

    public void setCardList(List<Card> cardList) {
        this.cardList = cardList;
    }

    public Integer getStatus() {
        return status;
    }

    public void setStatus(Integer status) {
        this.status = status;
    }
}
