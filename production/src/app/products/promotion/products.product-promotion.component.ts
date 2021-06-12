import {Component,OnInit,Input} from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';

@Component({
  selector: 'my-app',
  template: `<global-grid [childData]='childData'></global-grid>`,
})
export class ProductPromotionComponent { 
  
  public tabIndex: number;
  public parentId: number = 0;
  
	childData = {};
	constructor(private _globalService:GlobalService){
      this.tabIndex = +_globalService.getCookie('active_tabs');
      this.parentId = _globalService.getParentId(this.tabIndex);
      this.childData = {
        table : 'EngageboostDiscountMasters',
        heading : 'Product Specific Discount',
        ispopup:'N',
        tablink:'discount_product',
        tabparrentid:this.parentId,
        screen:'list2',
        is_import: 'Y',
        is_export: 'N',
      }
    }
}
