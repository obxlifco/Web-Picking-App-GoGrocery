package com.gogrocery.Models.SideMenuModel;

import java.util.List;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class SideMenuModel {

@SerializedName("status")
@Expose
private Integer status;
@SerializedName("menu_bar")
@Expose
private List<MenuBar> menuBar = null;

public Integer getStatus() {
return status;
}

public void setStatus(Integer status) {
this.status = status;
}

public List<MenuBar> getMenuBar() {
return menuBar;
}

public void setMenuBar(List<MenuBar> menuBar) {
this.menuBar = menuBar;
}

}