
import {throwError as observableThrowError,  Observable } from 'rxjs';

import {catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 

 
 
import {GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';

@Injectable()
export class AutoResponderService {
    
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(private _http: Http,private globalService:GlobalService) {}

    autoResponderLoad(id:number){

        if(id>0){

            return this._http.get(this.baseApiUrl+'emailnotification/'+id+'/', this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
        }else{

            return this._http.get(this.baseApiUrl+'autoresponderviewset/', this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
        }
        
        
    }

    autoResponderAddEdit(data: any, id:any){

        if(id>0){
            return this._http.put(this.baseApiUrl+'emailnotification/'+id+'/', data, this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
        }else{
            return this._http.post(this.baseApiUrl+'emailnotification/', data, this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
        }       
        
    }


    private handleError(error: Response) { 
      return observableThrowError(error || "Server err"); 
    } 
    
 }      