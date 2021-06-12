import {Observable,throwError} from 'rxjs';
import { catchError, map} from 'rxjs/operators'; 
import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {GlobalVariable} from './global';
import {GlobalService} from './app.global.service';
import { WarehouseService } from '../service/warehouse.service';


@Injectable({
  providedIn: 'root'
})
export class DetailsService {

  readonly apiBaseUrl = GlobalVariable.BASE_API_URL;
  //http://192.168.0.228:8085/api/front/v1/product-details/johnsons-baby-wipes-gentle-cln/

  constructor(private _http:Http,private _gs:GlobalService,private _warehouseService:WarehouseService) { 


  }
  /**
   * Method for getting product details by product slug
   * @access public
  */
  getProductDetailsByProductSlug(slugName:string) {
    let WAREHOUSE=''
    this._warehouseService.warehouseData$.subscribe(response=>{
      WAREHOUSE=response['selected_warehouse_id'];
    })
    var token='';
    if (localStorage) {
      if(localStorage.getItem('currentUser')) {
        var userData = JSON.parse(localStorage.getItem('currentUser'));
        token = 'Token '+ userData['token'];
      }
    }
    let headers = new Headers({'WAREHOUSE' : WAREHOUSE,'Authorization': token});

    let requestOptions = new RequestOptions({ headers: headers });

    let requestedProductDetailsUrl = this.apiBaseUrl+'product-details/'+slugName+'/';
    return this._http.get(requestedProductDetailsUrl,requestOptions).pipe(map(res =>  res.json()),catchError(err => this.handleError));

  }
  /**
   * Method for  handaling error
  */
   private handleError(err) { 
     return Observable.throw(err);
     

        

    }
    
}
