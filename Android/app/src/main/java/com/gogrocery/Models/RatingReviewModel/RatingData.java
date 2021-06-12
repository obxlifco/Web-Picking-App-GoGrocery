package com.gogrocery.Models.RatingReviewModel;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class RatingData {

@SerializedName("rating")
@Expose
private Integer rating;
@SerializedName("rating_count")
@Expose
private Integer ratingCount;
@SerializedName("percent")
@Expose
private double percent;

public Integer getRating() {
return rating;
}

public void setRating(Integer rating) {
this.rating = rating;
}

public Integer getRatingCount() {
return ratingCount;
}

public void setRatingCount(Integer ratingCount) {
this.ratingCount = ratingCount;
}

public double getPercent() {
return percent;
}

public void setPercent(double percent) {
this.percent = percent;
}

}