import { Component, OnInit } from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';

@Component({
  selector: 'my-app',
  template: `<global-grid [childData]='childData'></global-grid>`,
  styleUrls: ['./templates/giftcards.component.css']
})
export class GiftcardsComponent{

  public tabIndex: number;
  public parentId: number = 0;

	childData = {};
	constructor(private _globalService:GlobalService){
      this.tabIndex = +_globalService.getCookie('active_tabs');
      this.parentId = _globalService.getParentId(this.tabIndex);
      this.childData = {
        table : 'EngageboostGiftCardMasters',
        heading : 'Gift Cards',
        ispopup:'N',
        is_import: 'N',
        is_export: 'Y',
        tablink:'gift_cards',
        tabparrentid:this.parentId,
        screen:'list'
      }
    }

}
