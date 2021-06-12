import {throwError as observableThrowError,  Observable } from 'rxjs';
import {catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 
import {CookieService} from 'ngx-cookie';
import { GlobalVariable } from '../global/service/global';
import { GlobalService } from '../global/service/app.global.service';

@Injectable()
export class DashboardService {
    
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(private _http: Http, private _cookieService: CookieService, private globalService: GlobalService) {}

    getCookie(key: string){
      return this._cookieService.get(key);
    }

    dashboardLoad(data:any){
      return this._http.post(this.baseApiUrl + 'dashboard/', data, this.globalService.getHttpOption2()).pipe(map(res => res.json()),catchError(this.handleError),);
    }

    graphLoad(data:any){
      return this._http.post(this.baseApiUrl + 'sales-graph/', data, this.globalService.getHttpOption2()).pipe(map(res => res.json()),catchError(this.handleError),);
    }

  warehouseLoad(websiteId){
    return this._http.get(this.baseApiUrl + 'warehousestockmanagement/' + websiteId+'/', this.globalService.getHttpOption()).pipe(
         	map(res =>  res.json()),
         	catchError(this.handleError),);
    }

    private handleError(error: Response) { 
      return observableThrowError(error || "Server err"); 
   } 


    
 }