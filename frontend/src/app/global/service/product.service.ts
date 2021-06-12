import {Observable,throwError} from 'rxjs';
import { catchError, map} from 'rxjs/operators'; 
import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {GlobalVariable} from './global';
import {GlobalService} from './app.global.service';
import { WarehouseService } from './warehouse.service';

@Injectable({
  providedIn: 'root'
})
export class ProductService {

  readonly apiBaseUrl = GlobalVariable.BASE_API_URL;
  readonly api_Base_Url = GlobalVariable.BASE_BACKEND_API_URL;

  constructor(private _http:Http,private _gs:GlobalService,private _warehouseservice:WarehouseService) { 

  }
  /**
   * Method for getting similar product by product id
   * @access public
   * @param productId
  */
  getSimilarProductByProductId(productId) {
    let warehouseId='';
    this._warehouseservice.warehouseData$.subscribe(res=>{
      warehouseId=res['selected_warehouse_id'];
    })
    let requestedIp = this._gs.getGlobalDataByKey('requested_ip');
    let headersData = {
      'Content-Type' : 'application/json',
      'DEVICEID' : requestedIp,
      'WAREHOUSE' : warehouseId,
    }
    const headers = new Headers(headersData);
    let requestOptions = new RequestOptions({ headers: headers });
  	return this._http.get(this.apiBaseUrl+'similar-product/'+productId+'/',requestOptions).pipe(map(res =>  res.json()), 
       catchError(this._gs.handleError));


  }
  /**
   * Method for getting  popular product
   * @access public
  */
  getPopularProductByProductId(productId) {
    let warehouseId='';
    this._warehouseservice.warehouseData$.subscribe(res=>{
      warehouseId=res['selected_warehouse_id'];
    })
    
    let requestedIp = this._gs.getGlobalDataByKey('requested_ip');
    let headersData = {
      'Content-Type' : 'application/json',
      'DEVICEID' : requestedIp,
      'WAREHOUSE' : warehouseId,
    }
    const headers = new Headers(headersData);
    let requestOptions = new RequestOptions({ headers: headers });
  	return this._http.get(this.apiBaseUrl+'popular-product/'+productId+'/',requestOptions).pipe(map(res =>  res.json()), 
       catchError(this._gs.handleError));

  }
  getIdFromSlug(slugName,listingType) {
    let data = {
      'slug' : slugName,
      'listingType': listingType
    }
    return this._http.post(this.apiBaseUrl+'slug/',data).pipe(map(res =>  res.json()), 
       catchError(this._gs.handleError));
  }

  addToWishList(){
    alert()
  }

  getSubstituteProduct(postdata) {
    return this._http.post(this.api_Base_Url+'picker-orderlistdetails/',postdata).pipe(map(res =>  res.json()), 
       catchError(this._gs.handleError));
  }

  submitReplacementProduct(data: any){
    return this._http.post(this.api_Base_Url+'picker-acceptapproval/',data).pipe(map(res =>  res.json()), 
       catchError(this._gs.handleError));
  }
  
}
