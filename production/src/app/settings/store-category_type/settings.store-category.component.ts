import {Component,OnInit,Input} from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';
@Component({
  selector: 'my-app',
  template: `<global-grid [childData]='childData'></global-grid>`,
})
export class StoreCategoryComponent {
  public tabIndex: number;
  public parentId: number = 0;
	childData = {};
	constructor(private _globalService:GlobalService){
      this.tabIndex = +_globalService.getCookie('active_tabs');
      this.parentId = _globalService.getParentId(this.tabIndex);
      this.childData = {
        table : 'EngageboostTemplateIndustryMasters',
        heading : 'Store Category',
        ispopup:'N',
        tablink:'store-category',
        is_import: 'N',
        is_export: 'Y',
        tabparrentid:this.parentId,
        screen:'list'
      }
    }
}
