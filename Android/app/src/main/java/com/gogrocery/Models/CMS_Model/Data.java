package com.gogrocery.Models.CMS_Model;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Data {

@SerializedName("total_widgets")
@Expose
private Integer totalWidgets;
@SerializedName("widgets_data")
@Expose
private List<WidgetsData> widgetsData = null;

public Integer getTotalWidgets() {
return totalWidgets;
}

public void setTotalWidgets(Integer totalWidgets) {
this.totalWidgets = totalWidgets;
}

public List<WidgetsData> getWidgetsData() {
return widgetsData;
}

public void setWidgetsData(List<WidgetsData> widgetsData) {
this.widgetsData = widgetsData;
}

}