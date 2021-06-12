import { catchError, map} from 'rxjs/operators'; 
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import { Injectable} from '@angular/core'; 
import { BehaviorSubject } from 'rxjs';
import { CookieService} from 'ngx-cookie';
import { GlobalService } from './app.global.service';
import {GlobalVariable} from './global';
import { Router } from '@angular/router';


@Injectable({
  providedIn: 'root'
})
export class LoyaltypointService {

  readonly apiBaseUrl = GlobalVariable.BASE_API_URL;

  constructor(private _globalService:GlobalService,private _http:Http) { }

  /**
   * Method for getting loyalty point using order id
   * @access public
  */
  applyLoyaltyPoint(loyaltyData) {

  	let requestOption = this._globalService.getHttpOptionFrontendUser();
  	return this._http.post(this.apiBaseUrl+'apply-loyalty/',loyaltyData,requestOption).pipe(
           map(res =>  res.json()),
           catchError(this._globalService.handleError));
  }
  /**
   * Method for getting users loyalty point data 
   * @access public
  */
  getUserLoyaltyData() {
    let userRequestOption = this._globalService.getHttpOptionFrontendUser();
    return this._http.get(this.apiBaseUrl+'points-log/',userRequestOption).pipe(
           map(res =>  res.json()),
           catchError(this._globalService.handleError));

  }
}
