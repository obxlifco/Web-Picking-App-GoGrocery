import {Component,OnInit,Input} from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';

@Component({
  selector: 'my-app',
  template: `<global-grid [childData]='childData'></global-grid>`,
})
export class SegmentComponent { 

  public tabIndex: number;
  public parentId: number = 0;

  childData = {};
  constructor(private _globalService:GlobalService){
      this.tabIndex = +_globalService.getCookie('active_tabs');
      this.parentId = _globalService.getParentId(this.tabIndex);
      this.childData = {
        table : 'EngageboostEmktSegments',
        heading : 'Segment',
        ispopup:'N',
        tablink:'segments',
        tabparrentid:this.parentId,
        screen:'list',
        is_import: 'N',
        is_export: 'N'
      }
    }
}
