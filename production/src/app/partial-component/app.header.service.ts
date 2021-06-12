import {throwError as observableThrowError,  Observable } from 'rxjs';
import {catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 
import {CookieService} from 'ngx-cookie';
import { GlobalVariable } from '../global/service/global';
import { GlobalService } from '../global/service/app.global.service';
@Injectable()
export class HeaderService {
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    private elasticUrl  = GlobalVariable.elasticURL;
    constructor(
      private _http: Http,
      private _cookieService:CookieService,
      private globalService:GlobalService
      ) {
    }
    doSearch(data:any) {
       data={"key":data}
       return this._http.post(this.baseApiUrl+'esmenu/', data, this.globalService.getHttpOption()).pipe(
       map(res =>  res.json()),
       catchError(this.handleError),);
    }

    doSearchDirect(data:any) {
      //let url = this.elasticUrl+'searchdata/_search?q=*'+data+'*';
      let userData = this._cookieService.getObject('userData');
      let websiteId = this.globalService.getWebsiteId();
      if (userData["elastic_store_name"] != "") {
        userData["elastic_url"] = userData["elastic_url"] + userData["elastic_store_name"] + "_";
      }
      let url = userData["elastic_url"] + 'product_' + websiteId + ',order_' + websiteId + '/data/_search?q='+ data;
      return this._http.get(url, this.globalService.getHttpOptionNotLogin()).pipe(
            map(res => res.json()),catchError(this.handleError), );
    }

    updatePassword(data: any, id:any){
        return this._http.put(this.baseApiUrl+'users_changepass/'+id+'/', data, this.globalService.getHttpOption()).pipe(
          map(res =>  res.json()),
          catchError(this.handleError),);
    }

    private handleError(error: Response) { 
      return observableThrowError(error || "Server err");
    }

    getwebsiteList(data:any){
      return this._http.post(this.baseApiUrl + 'list_of_websites/',data,this.globalService.getHttpOption()).pipe(
        map(res => res.json()),
        catchError(this.handleError),);
    }
 }