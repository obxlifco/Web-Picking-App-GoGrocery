import { Component, OnInit } from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';

@Component({
  selector: 'app-category-banner',
  template: `<global-grid [childData]='childData'></global-grid>`,
  styleUrls: ['./templates/category-banner-addedit.component.css']

})
export class CategoryBannerComponent {

  public tabIndex: number;
  public parentId: number = 0;

	childData = {};
	constructor(private _globalService:GlobalService){
    this.tabIndex = +_globalService.getCookie('active_tabs');
    this.parentId = _globalService.getParentId(this.tabIndex);
    this.childData = {
      table : 'EngageboostCategoryBanners',
      heading : 'Category Banners',
      ispopup:'N',
      is_import: 'N',
      is_export: 'N',
      tablink:'category-banner',
      tabparrentid:this.parentId,
      screen:'list'
    }
  }

}
