import { Observable,throwError} from 'rxjs';
import { catchError, map} from 'rxjs/operators'; 
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import { Injectable} from '@angular/core'; 
import { BehaviorSubject } from 'rxjs';
import { CookieService} from 'ngx-cookie';
import { GlobalService } from './app.global.service';
import {GlobalVariable} from './global';
import { Router } from '@angular/router';
import * as FormData from 'form-data';

@Injectable({
  providedIn: 'root'
})
export class MenuService {

  readonly apiBaseUrl = GlobalVariable.BASE_API_URL;
  private _websiteId;
  private _latitude;
  private _longitude;
 
  public signinSignuppopup$ = new BehaviorSubject({});
  public signinsignUPObservable = this.signinSignuppopup$.asObservable();

  constructor(private _gs:GlobalService,
  	          private _http: Http, 
        	  private _cookieService:CookieService,
            ) { 
  	this._websiteId = this._gs.getFrontedWebsiteId();
  	let coordinateInstance = this._gs.getCurrentUserLatitudeLongitude();
  	/*console.log("******************** Coordinate data ****************");
  	console.log(coordinateInstance);*/
  	this._latitude =  coordinateInstance['latitude'] ? coordinateInstance['latitude'] : '';
  	this._longitude = coordinateInstance['longitude'] ? coordinateInstance['longitude'] : '';
  	


  }

  /**
   * Method for fetching header menu
   * @access public
   * @return menuData
  */
  getHeaderMenu(warehouseId) {
    let requestMenuData = new FormData();
    requestMenuData.append('website_id',this._websiteId);
    requestMenuData.append('latitude',this._latitude);
    requestMenuData.append('longitude',this._longitude);
    requestMenuData.append('warehouse_id',warehouseId);

    requestMenuData.append('lang_code','en');
    return this._http.post(this.apiBaseUrl+'menu_bar/',requestMenuData).pipe(map(res => res.json()),catchError(err => this._handleError(err)));;

  }
   /**
    * Method for handaling error
    * @access private
   */
   private _handleError(error: Response) { 
     return Observable.throw(error || "Server error");
        //return Observable.throw(error || "Server err");  

    }

}
