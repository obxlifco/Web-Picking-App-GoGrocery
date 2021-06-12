import {Component,OnInit,Input} from '@angular/core';

@Component({
  selector: 'my-app',
  template: `<global-grid [childData]='childData'></global-grid>`,
})
export class ContactsComponent { 
	childData = {};
	constructor(){
      this.childData = {
        table : 'EngageboostEmktContacts',
        heading : 'Contacts',
        ispopup:'N',
        is_import: 'N',
        is_export: 'Y',
        tablink:'contacts',
        tabparrentid:'0',
        screen:'list'
      }
    }
}
