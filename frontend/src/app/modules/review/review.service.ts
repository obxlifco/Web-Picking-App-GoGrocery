import { Injectable } from '@angular/core';
import {Observable,throwError, Subject} from 'rxjs';
import { catchError, map} from 'rxjs/operators'; 
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {GlobalVariable} from '../../global/service/global';
import {GlobalService} from '../../global/service/app.global.service';
@Injectable({
  providedIn: 'root'
})
export class ReviewService {
  readonly apiBaseUrl = GlobalVariable.BASE_API_URL;
  //readonly apiBaseUrl ='http://192.168.0.228:8062/api/front/v1/'
  constructor(
    private _http:Http,
    private _gs:GlobalService,
  ) { }
  getProductReviewByProductID(productId:number) {
    let data = {"product_id":productId}
    let requestedProductDetailsUrl = this.apiBaseUrl+'view-review/';
    return this._http.post(requestedProductDetailsUrl,data).pipe(map(res =>  res.json()),catchError(err => this._gs.handleError));
  }
  addProductReview(reviewData){
    //console.log(reviewData);

    let requestOption = this._gs.getHttpOptionFrontendUser();
    return this._http.post(this.apiBaseUrl+'product-review/',reviewData,requestOption).pipe(map(res =>  res.json()),catchError(err => this._gs.handleError(err)));
   
  }
  reviewData = new Subject<any>();
  ratingData = new Subject<any>();
  rating = new Subject<any>();
}
