import {Component,OnInit,Input} from '@angular/core';

@Component({
  selector: 'my-app',
  template: `<global-grid [childData]='childData'></global-grid>`,
})
export class ContactGroupComponent { 
	childData = {};
	constructor(){
      this.childData = {
        table : 'EngageboostEmktContactlists',
        heading : 'Contact Group',
        ispopup:'N',
        is_import: 'N',
        is_export: 'Y',
        tablink:'contactlists',
        tabparrentid:'0',
        screen:'list'
      }
    }
}
