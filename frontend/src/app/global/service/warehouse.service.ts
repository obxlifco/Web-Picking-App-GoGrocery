import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {map,catchError} from 'rxjs/operators'
import {GlobalVariable} from './global';
import {GlobalService} from './app.global.service';
import { CookieService} from 'ngx-cookie';
import { BehaviorSubject,Observable } from 'rxjs';
import {WarehouseData} from '../interface/warehouse';


@Injectable({
  providedIn: 'root'
})
export class WarehouseService {

  public wareHouseDetails:Object = this._cookieService.getObject('current_user_location') ? this._cookieService.getObject('current_user_location') : GlobalVariable.DEFAULT_WAREHOUSE_DATA;
  readonly apiBaseUrl = GlobalVariable.BASE_API_URL;
  private _wareHouseObservable = new BehaviorSubject(this.wareHouseDetails);
  public warehouseData$  = this._wareHouseObservable.asObservable();

  constructor(private _http:HttpClient,private _gs : GlobalService,private _cookieService:CookieService,) { 


  }
  /**
   * Method for getting warehouse by latitude and longitude
   * @access public
  */
  getWareHouseList(wareHouseData) {
  	return this._http.post(this.apiBaseUrl+'warehouse-list/',wareHouseData);
  	// pipe(map(res =>  res),catchError(err => this._gs.handleError(err)))
  }
  /**
   * Method on warehouse change

  */
  onWareHouseChangeData(warehouseData) {
    this._wareHouseObservable.next(warehouseData);
  }
  

}
