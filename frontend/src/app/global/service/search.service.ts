import { Injectable } from '@angular/core';
import { throwError as observableThrowError,  Observable } from 'rxjs';
import { catchError, map} from 'rxjs/operators'; 
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import { BehaviorSubject } from 'rxjs';
import { CookieService} from 'ngx-cookie';
import { GlobalService } from './app.global.service';
import { WarehouseService  } from './warehouse.service';
import {GlobalVariable,Global} from './global';


@Injectable({
  providedIn: 'root'
})
export class SearchService {

  readonly apiBaseUrl = GlobalVariable.BASE_API_URL;

  constructor(private _http:Http,private _gs:GlobalService) { }


  /**
   * Method for getting base64 encoded id
   * @access public
  */
  getEncodedId(productId = []) {
  	if(productId.length == 0) {
  		return;
  	}
  	let productIdString = productId.toString();
  	return btoa(productIdString);

  }
  /**
   * Method for get filter data by product id
   * @access public
  */
  getFilterDataByProductId(encodedString = '') {
  	let httpRequestOption = this._gs.getHttpOptionFrontendUser(); 
  	return this._http.get(this.apiBaseUrl+'search-filter/?v='+encodedString,httpRequestOption).pipe(map(res =>  res.json()), 
       catchError((err:any) => this._gs.handleError(err)))



  }
}
