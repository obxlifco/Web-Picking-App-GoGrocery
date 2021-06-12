import { Pipe, PipeTransform } from '@angular/core';
import {GlobalService} from '../service/app.global.service';

@Pipe({
  name: 'money'
})
export class MoneyPipe implements PipeTransform {

 public currencySymbol = 'AED';
 constructor(private _globalService:GlobalService) {
 	this.currencySymbol = this._globalService.getCurrencySymbol();

 }

  transform(value: any, args?: any): any {
  	value = value ? value : 0;
  	return this.currencySymbol+' '+ parseFloat(value).toFixed(2);
    
  }

}
