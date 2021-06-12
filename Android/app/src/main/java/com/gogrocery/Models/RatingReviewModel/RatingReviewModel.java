package com.gogrocery.Models.RatingReviewModel;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class RatingReviewModel {

@SerializedName("status")
@Expose
private String status;
@SerializedName("rating_data")
@Expose
private List<RatingData> ratingData = null;
@SerializedName("review_data")
@Expose
private List<ReviewData> reviewData = null;
@SerializedName("review_avg")
@Expose
private double reviewAvg;

public String getStatus() {
return status;
}

public void setStatus(String status) {
this.status = status;
}

public List<RatingData> getRatingData() {
return ratingData;
}

public void setRatingData(List<RatingData> ratingData) {
this.ratingData = ratingData;
}

public List<ReviewData> getReviewData() {
return reviewData;
}

public void setReviewData(List<ReviewData> reviewData) {
this.reviewData = reviewData;
}

public double getReviewAvg() {
return reviewAvg;
}

public void setReviewAvg(double reviewAvg) {
this.reviewAvg = reviewAvg;
}

}