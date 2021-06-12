package com.gogrocery.Models.ElasticSearch;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Hits {

@SerializedName("total")
@Expose
private Integer total;
@SerializedName("max_score")
@Expose
private Double maxScore;
@SerializedName("hits")
@Expose
private List<Hit> hits = null;

public Integer getTotal() {
return total;
}

public void setTotal(Integer total) {
this.total = total;
}

public Double getMaxScore() {
return maxScore;
}

public void setMaxScore(Double maxScore) {
this.maxScore = maxScore;
}

public List<Hit> getHits() {
return hits;
}

public void setHits(List<Hit> hits) {
this.hits = hits;
}

}