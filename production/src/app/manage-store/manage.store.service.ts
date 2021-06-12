import {throwError as observableThrowError,  Observable } from 'rxjs';
import {map, catchError} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 
import {GlobalVariable } from '../global/service/global';
import { GlobalService } from '../global/service/app.global.service';

@Injectable()
export class PageService {
	private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(private _http: Http,private globalService:GlobalService) {}
  /**
  * add new page
  * @param data - any (object)
  *  
  */
  pageAdd(data:any){  	
     return this._http.post(this.baseApiUrl+'new_page_create/', data, this.globalService.getHttpOption()).pipe(
       map(res =>  res.json()), 
      catchError(this.handleError));
  }

  /**
  * get the details of a page by its ID
  * @param id - number
  *  
  */
  pageLoad(id:number){
      return this._http.get(this.baseApiUrl+'page_update/'+id+'/', this.globalService.getHttpOption()).pipe(
         map(res =>  res.json()), 
         catchError(this.handleError));
  }

  private handleError(error: Response) { 
    return Observable.throw(error || "Server err"); 
 	}     
}	