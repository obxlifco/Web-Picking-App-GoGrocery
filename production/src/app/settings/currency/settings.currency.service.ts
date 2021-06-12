
import {throwError as observableThrowError,  Observable } from 'rxjs';

import {map, catchError} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions, Jsonp} from '@angular/http';
import {Injectable} from '@angular/core'; 

 
 
import {GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';

@Injectable()
export class CurrencyService {
    
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(private _http: Http,private globalService:GlobalService, private jsonp:Jsonp) {}

    currencyLoad(id:number){
    		return this._http.get(this.baseApiUrl+'currencymanagement/', this.globalService.getHttpOption()).pipe(
	       	map(res =>  res.json()),
	       	catchError(this.handleError),);    
	}

    currencyManage(data: any){
    		return this._http.post(this.baseApiUrl+'currencymanagement/', data, this.globalService.getHttpOption()).pipe(
	       	map(res =>  res.json()),
	    	catchError(this.handleError),);
	}	

    setBaseCurrency(id:any){
            return this._http.put(this.baseApiUrl+'basecurrencyset/'+id+'/', '', this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
    }
    private handleError(error: Response) { 
      return observableThrowError(error || "Server err"); 
   	} 

    syncCurr(updatedby:number){
       return this._http.post(this.baseApiUrl+'currencyexchangerate/',{"updatedby":updatedby}, this.globalService.getHttpOptionFile()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
  
  
    }   

    updateSyncCurrency(data:any){
        return this._http.put(this.baseApiUrl+'basecurrencychange/', data, this.globalService.getHttpOption()).pipe(
        map(res =>  res.json()),
        catchError(this.handleError),);
    }
    
 }		