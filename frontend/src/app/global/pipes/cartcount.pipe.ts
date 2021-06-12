import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'cartcount'
})
export class CartcountPipe implements PipeTransform {

  transform(value: any, args?: any): any {
    return null;
  }

}
