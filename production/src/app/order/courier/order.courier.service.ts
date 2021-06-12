
import {throwError as observableThrowError,  Observable } from 'rxjs';

import {map, catchError} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 

 
 
import {CookieService} from 'ngx-cookie';
import {GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';

@Injectable()
export class CourierService {	
  private baseApiUrl = GlobalVariable.BASE_API_URL;

	constructor(private _http: Http,private globalService:GlobalService,private _cookieService:CookieService) {}
		private handleError(error: Response) { 
	    return observableThrowError(error || "Server err"); 
	} 

	doGrid(data:any,page:number) {
       if(!page){var url=this.baseApiUrl+'view_awb_details/';}
       else{var url=this.baseApiUrl+'view_awb_details/?page='+page;}
       return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
       map(res =>  res.json()),
       catchError(this.handleError),); 
    }


  	saveCourierDetails(data: any, id:any) {
	  	if(id>0) {
			return this._http.post(this.baseApiUrl+'add_courier/', data, this.globalService.getHttpOption()).pipe(
	       	map(res =>  res.json()),
	       	catchError(this.handleError),);
		} else {
			return this._http.post(this.baseApiUrl+'add_courier/', data, this.globalService.getHttpOption()).pipe(
	       	map(res =>  res.json()),
	    	catchError(this.handleError),);
		}	
    }

    loadCourierDetails(id:number) {
    	if(id > 0) {
	      	return this._http.get(this.baseApiUrl+'get_courier/'+id+'/',this.globalService.getHttpOption()).pipe(
	      	map(res=>res.json()),
	        catchError(this.handleError),);
    	}
    }

    addAwbMasters(data:any) {
		return this._http.post(this.baseApiUrl+'add_awb_number/', data, this.globalService.getHttpOption()).pipe(
       	map(res =>  res.json()),
       	catchError(this.handleError),);
    }
}	