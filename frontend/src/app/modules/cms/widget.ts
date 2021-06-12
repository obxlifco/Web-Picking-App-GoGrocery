import { Type } from '@angular/core';
export class Widget {
  constructor(public id: number,public is_distributor:number, public widget_category:number, public label: string, public type:number, public favicon:String, public component:string,public htmlTemplate: String, public insertables: any) { }
  getHtml() {
    var html = this.htmlTemplate;
      for (var i = 0; i < this.insertables.length; i++) {
        for (var j = 0; j < this.insertables[i].properties.length; j++) {
          var selector = '{{' + this.insertables[i].properties[j].selector + '}}';
          var val = this.insertables[i].properties[j].value;
          html = html.replace(selector, val);
        }
      }
    return html;
  }

  getLabel(){
    return this.label;
  }

  getWidgetCategory(){
    return this.widget_category;
  }

  getType(){
    return this.type;
  }

  getFavicon(){
    return this.favicon;
  }
  
  getComponent(){
    return this.component;
  }

  getID() {
    return this.id; //Math.floor((Math.random() * 100) + 1)
  }

  getHtmlTemplate() {
    return this.htmlTemplate;
  }

  getInsertables() {
    return this.insertables;
  }

  getIsDistributor() {
    return this.is_distributor;
  }
}