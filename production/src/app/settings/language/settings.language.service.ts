
import {throwError as observableThrowError,  Observable } from 'rxjs';

import {map, catchError} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions, Jsonp} from '@angular/http';
import {Injectable} from '@angular/core'; 

 
 
import {GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';

@Injectable()
export class LanguageService {
    
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(private _http: Http,private globalService:GlobalService, private jsonp:Jsonp) {}

    // languageLoad(id:number){
    // 		return this._http.get(this.baseApiUrl+'language/', this.globalService.getHttpOption()).pipe(
	//        	map(res =>  res.json()),
	//        	catchError(this.handleError),);    
	// }

    languageManage(data: any){
    		return this._http.post(this.baseApiUrl+'languagemanagement/', data, this.globalService.getHttpOption()).pipe(
	       	map(res =>  res.json()),
	    	catchError(this.handleError),);
    }
    
    languageLoad(id:number){
    	if(id>0) {
    		return this._http.get(this.baseApiUrl+'language-data/'+id+'/', this.globalService.getHttpOption()).pipe(
	       	map(res =>  res.json()),
	       	catchError(this.handleError),);
    	}else{
			return this._http.get(this.baseApiUrl+'all-language/', this.globalService.getHttpOption()).pipe(
				map(res =>  res.json()),
				catchError(this.handleError),);
    	}
    }
    

    setBaseLanguage(id:any){
            return this._http.put(this.baseApiUrl+'baselanguageset/'+id+'/', '', this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
    }
    private handleError(error: Response) { 
      return observableThrowError(error || "Server err"); 
   	} 

    syncLang(updatedby:number){
       return this._http.post(this.baseApiUrl+'languageexchangerate/',{"updatedby":updatedby}, this.globalService.getHttpOptionFile()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
  
  
    }   

    updateSyncLanguage(data:any){
        return this._http.put(this.baseApiUrl+'baselanguagechange/', data, this.globalService.getHttpOption()).pipe(
        map(res =>  res.json()),
        catchError(this.handleError),);
    }
    languageAddEdit(data: any, id:any){
    	if(id>0){
    		return this._http.put(this.baseApiUrl+'language-data/'+id+'/', data, this.globalService.getHttpOption()).pipe(
	       	map(res =>  res.json()),
	       	catchError(this.handleError),);
    	} else {
    		return this._http.post(this.baseApiUrl+'language-data/', data, this.globalService.getHttpOption()).pipe(
	       	map(res =>  res.json()),
	    	catchError(this.handleError),);
    	}
    }
    
 }		