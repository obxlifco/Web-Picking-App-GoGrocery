
import {throwError as observableThrowError,  Observable } from 'rxjs';

import {catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 

 
 
import {GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';

@Injectable()
export class ContactService {
    
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(private _http: Http,private globalService:GlobalService) {}

    contactLoad(id:number){

    	if(id>0){

    		return this._http.get(this.baseApiUrl+'contacts/'+id+'/', this.globalService.getHttpOption()).pipe(
	       	map(res =>  res.json()),
	       	catchError(this.handleError),);
    	}else{
           return this._http.get(this.baseApiUrl+'contacts_list/', this.globalService.getHttpOption()).pipe(
           map(res =>  res.json()),
           catchError(this.handleError),);
    	}
    	
        
	}

    contactAddEdit(data: any, id:any){

    	if(id>0){
    		return this._http.put(this.baseApiUrl+'contacts/'+id+'/', data, this.globalService.getHttpOption()).pipe(
	       	map(res =>  res.json()),
	       	catchError(this.handleError),);
    	}else{
    		return this._http.post(this.baseApiUrl+'contacts/', data, this.globalService.getHttpOption()).pipe(
	       	map(res =>  res.json()),
	    	catchError(this.handleError),);
    	}		
        
	}	

    private handleError(error: Response) { 
      return observableThrowError(error || "Server err"); 
   	} 
    
 }		