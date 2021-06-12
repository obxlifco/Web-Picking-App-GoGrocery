import { Injectable } from '@angular/core';
import { throwError as observableThrowError,  Observable } from 'rxjs';
import { catchError, map} from 'rxjs/operators'; 
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import { BehaviorSubject } from 'rxjs';
import { CookieService} from 'ngx-cookie';
import { GlobalService } from './app.global.service';
import { WarehouseService  } from './warehouse.service';
import {GlobalVariable,Global} from './global';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class DealsorsellService {

  readonly apiBaseUrl = GlobalVariable.BASE_API_URL;
  private _websiteId;
  private _warehouseId;
  constructor(private _gs:GlobalService,
  	          private _http: Http, 
        	  private _cookieService:CookieService,
            private _wareHouseService : WarehouseService
        	 
        	  ) {
              this._wareHouseService.warehouseData$.subscribe(response => {
       
                this._warehouseId = response['selected_warehouse_id'];
          
              });
  	this._websiteId   = this._gs.getFrontedWebsiteId();
  
   
   }
   /**
   * Method for getting sells of the day
   * @access public
   * @return sellsOfTheDay
   */
   getBestSellsOfTheDay() {
    
   	let sellsData:FormData = new FormData();
   	sellsData.append('website_id',this._websiteId);
   	sellsData.append('warehouse_id',this._warehouseId);
   	return this._http.post(this.apiBaseUrl+'best_selling_product/',sellsData).pipe(map(res =>  res.json()), 
       catchError((err:any) => this._gs.handleError(err)))
   }
   /**
    * Method for getting deals of the day
    * @access public
    * @return sellsOfDay
   */
   getBestDealsOFtheDay() {
   	let dealsData:FormData = new FormData();
   	dealsData.append('website_id',this._websiteId);
   	dealsData.append('warehouse_id',this._warehouseId);
   	return this._http.post(this.apiBaseUrl+'deals_of_the_day/',dealsData).pipe(map(res => res.json()),
   		catchError((err:any) => this._gs.handleError(err)))
 	
   }

}
