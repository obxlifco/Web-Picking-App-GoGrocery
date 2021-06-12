
import {throwError as observableThrowError,  Observable } from 'rxjs';

import {map, catchError} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 
import {GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';
@Injectable()
export class WarehouseService {
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(private _http: Http,private globalService:GlobalService) {}
    warehouseLoad(id:number){
    	if(id>0) {
    		return this._http.get(this.baseApiUrl+'warehouse/'+id+'/', this.globalService.getHttpOption()).pipe(
	       	map(res =>  res.json()),
	       	catchError(this.handleError),);
    	} else {
            return this._http.get(this.baseApiUrl+'warehouse_list/', this.globalService.getHttpOption()).pipe(
               map(res =>  res.json()),
               catchError(this.handleError),);
    	}
    	
	}

    warehouseAddEdit(data: any, id:any){
    	if(id>0){
    		return this._http.put(this.baseApiUrl+'warehouse/'+id+'/', data, this.globalService.getHttpOption()).pipe(
	       	map(res =>  res.json()),
	       	catchError(this.handleError),);
    	} else {
    		return this._http.post(this.baseApiUrl+'warehouse/', data, this.globalService.getHttpOption()).pipe(
	       	map(res =>  res.json()),
	    	catchError(this.handleError),);
    	}		
        
	}	

    warehouseState(id:any){
        return this._http.get(this.baseApiUrl+'statelist/'+id+'/', this.globalService.getHttpOption()).pipe(
           map(res =>  res.json()),
           catchError(this.handleError),);
    }
    private handleError(error: Response) { 
      return observableThrowError(error || "Server err"); 
	} 
	   
	getAllStoreType() {
        return this._http.get(this.baseApiUrl+'get_storetype/',this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError));
	}
	
	getAllCategory() {
        return this._http.get(this.baseApiUrl+'get_categoryall/',this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError));
	}
	
	getPaymentMethod() {
        return this._http.get(this.baseApiUrl+'payment-method/',this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError));
	}
    
 }		