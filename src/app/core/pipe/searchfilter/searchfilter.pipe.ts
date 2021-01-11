import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'searchfilter'
})
export class SearchfilterPipe implements PipeTransform {

  transform(items: any[], searchText: string): any[] {
    if (!items) {
      return [];
    }
    if (!searchText) {
      return items;
    }
    searchText = searchText.toLocaleLowerCase();
    // console.log("items : ",items);
    
    // return items.filter((it: any) => {
    //   return it.toLocaleLowerCase().includes(searchText);
    // });

    return items.filter(function (el: any) {   // <---- data type!
      return el.name.toLowerCase().indexOf(searchText) > -1;
  });
  }

}
