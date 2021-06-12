import {Component,OnInit,Input} from '@angular/core';

@Component({
  selector: 'my-app',
  template: `<global-grid [childData]='childData'></global-grid>`,
})
export class CoupanPromotionComponent { 
	childData = {};
	constructor(){
      this.childData = {
        table : 'EngageboostDiscountMasters',
        heading : 'Coupon Specific Discount',
        ispopup:'N',
        tablink:'discount_coupon',
        tabparrentid:'0',
        screen:'list1',
        is_import: 'Y',
        is_export: 'Y'
      }
    }
}
