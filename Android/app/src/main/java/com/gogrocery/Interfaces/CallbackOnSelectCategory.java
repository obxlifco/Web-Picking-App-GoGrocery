package com.gogrocery.Interfaces;

import com.gogrocery.Models.SideMenuModel.Child;

import java.util.List;

public interface CallbackOnSelectCategory {
    void onSelectCategory(List<Child> child,String argWhich, String argPageTitle);
}
