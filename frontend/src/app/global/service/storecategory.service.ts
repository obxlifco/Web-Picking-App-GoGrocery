import { Injectable,Inject} from '@angular/core';
import { throwError as observableThrowError,  Observable,BehaviorSubject} from 'rxjs';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
/*import { BehaviorSubject, Observable } from 'rxjs';*/
import {GlobalVariable} from './global';
import { WINDOW,LOCAL_STORAGE} from '@ng-toolkit/universal';

@Injectable({
  providedIn: 'root'
})
export class StoreCategoryService {
  readonly apiBaseUrl = GlobalVariable.BASE_API_URL;
  readonly baseBackendApiUrl = GlobalVariable.BASE_BACKEND_API_URL;
  private _websiteId = 1;
  public warehouse_id:number;
  public requestedIp = '';
  public wishlistCount :any= 0;
  
  //public requestedIpData = this._globalServ

  constructor(
	private _http:Http,
	@Inject(LOCAL_STORAGE) private localStorage: any,
	) {
	//this.getCartDetails();
	//alert("hiii");

	}

	private handleError(error: Response) { 
		return Observable.throw(error || "Server err"); 
	}

	// getAllStoreCategory() {
  //   return this._http.get(this.apiBaseUrl+'get_storetype/').pipe(map(res => res.json()),catchError(this.handleError));
  // }
  
  
  getAllStoreCategory(data: any) {
    return this._http.post(this.apiBaseUrl+'get_storetype/', data).pipe(
      map(res =>  res.json()),
   catchError(this.handleError),);
	}
  
  
	getAllCategory() {
    return this._http.get(this.apiBaseUrl+'get_categoryall/').pipe(map(res => res.json()),catchError(this.handleError));
  }

}