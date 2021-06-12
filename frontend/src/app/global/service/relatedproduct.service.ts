import { Injectable } from '@angular/core';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {GlobalVariable} from './global';

@Injectable({
  providedIn: 'root'
})
export class RelatedproductService {

  readonly apiBaseUrl = GlobalVariable.BASE_API_URL;

  constructor(private _http:Http) { }

  /**
   * Method to get related product by category slug
   * @access public
  */
  getRelatedProductByCategorySlug(categorySlug:string) {
  	
  }
}
