import { Injectable } from '@angular/core';
import {Router} from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class UtillService {

  constructor(private _router:Router) { }


  /**
   * Method for navigate to url
  */
  navigateToUrl(url:string = '') {
  	this._router.navigate([url]);

  }
}
