import {Component,OnInit,Input} from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';

@Component({
  selector: 'my-app',
  template: `<global-grid [childData]='childData'></global-grid>`,
})
export class HsnCodeComponent { 

  public tabIndex: number;
  public parentId: number = 0;

	childData = {};
	constructor(private _globalService:GlobalService){
      this.tabIndex = +_globalService.getCookie('active_tabs');
      this.parentId = _globalService.getParentId(this.tabIndex);
      this.childData = {
        table: 'EngageboostHsnCodeMaster',
        heading : 'HSN Code',
        ispopup:'Y',
        tablink:'hsn',
        tabparrentid:this.parentId,
        screen:'list',
        is_import: 'Y',
        is_export: 'N',
      }
    }

  
}
