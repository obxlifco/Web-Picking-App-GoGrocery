import { Injectable } from '@angular/core';
import {Subject} from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class LoaderService {
  isLoading = new Subject<boolean>();
  constructor() { }
  show() {
    // console.log("***************** Loader show  called ******************");
  	this.isLoading.next(true);
  }
  hide() {
  	// console.log("***************** Loader hide called ********************");
  	  this.isLoading.next(false);
  }
}
