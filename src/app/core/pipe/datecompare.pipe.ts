import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'datecompare'
})
export class DatecomparePipe implements PipeTransform {

  transform(events: any): any {
    if (!events) return events
     return events.filter(function (event:any) {
      return Date.parse(event.dateStart) < Date.now();
    })
  }

}
