package com.gogrocery.Models.MyCardList;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Card {
    @SerializedName("id")
    @Expose
    private String id;
    @SerializedName("card_type")
    @Expose
    private String cardType;
    @SerializedName("si_sub_ref_no")
    @Expose
    private String siSubRefNo;
    @SerializedName("card_suffix")
    @Expose
    private String cardSuffix;
    @SerializedName("is_default")
    @Expose
    private String isDefault;

    public String getIsDefault() {
        return isDefault;
    }

    public void setIsDefault(String isDefault) {
        this.isDefault = isDefault;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getCardType() {
        return cardType;
    }

    public void setCardType(String cardType) {
        this.cardType = cardType;
    }

    public String getSiSubRefNo() {
        return siSubRefNo;
    }

    public void setSiSubRefNo(String siSubRefNo) {
        this.siSubRefNo = siSubRefNo;
    }

    public String getCardSuffix() {
        return cardSuffix;
    }

    public void setCardSuffix(String cardSuffix) {
        this.cardSuffix = cardSuffix;
    }



}

