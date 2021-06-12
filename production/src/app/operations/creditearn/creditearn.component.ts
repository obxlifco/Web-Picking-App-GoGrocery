import { Component, OnInit } from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';

@Component({
  selector: 'my-app',
    template: `<global-grid [childData]='childData'></global-grid>`,
})
export class CreditearnComponent  {

  childData = {};
  public tabIndex: number;
  public parentId: number = 0;
  constructor(private _globalService: GlobalService) {
      this.tabIndex = +_globalService.getCookie('active_tabs');
      this.parentId = _globalService.getParentId(this.tabIndex);
      this.childData = {
          table: 'EngageboostCreditPoint',
          heading: 'Credit Points Earned',
          ispopup: 'N',
          tablink: 'credit_points_earn',
          tabparrentid: this.parentId,
          screen: 'list_earn',
          is_import: 'N',
          is_export: 'N'
      }
  }
}
