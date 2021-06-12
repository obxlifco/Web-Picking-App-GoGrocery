import {Component,OnInit,Input} from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';

@Component({
  selector: 'my-app',
  template: `<global-grid [childData]='childData'></global-grid>`,
})
export class CustomerGroupComponent { 

  public tabIndex: number;
  public parentId: number = 0;

	childData = {};
	constructor(private _globalService:GlobalService){
      this.tabIndex = +_globalService.getCookie('active_tabs');
      this.parentId = _globalService.getParentId(this.tabIndex);
      this.childData = {
        table : 'EngageboostCustomerGroup',
        heading : 'Customer Group',
        ispopup:'N',
        is_import: 'N',
        is_export: 'Y',
        tablink:'customer_group',
        tabparrentid:this.parentId,
        screen:'list'
      }
    }
}