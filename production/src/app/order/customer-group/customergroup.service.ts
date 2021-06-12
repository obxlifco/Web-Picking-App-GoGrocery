
import {throwError as observableThrowError,  Observable } from 'rxjs';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 
import {GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';

@Injectable()
export class CustomergroupService {
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    public post_data = {};
    constructor(private _http: Http, private globalService: GlobalService) {}

    private handleError(error: Response) {
      return observableThrowError(error || "Server err");
    }

    // customerLoad(data) {
    //     return this._http.post(this.baseApiUrl+'discountcustomer/', data, this.globalService.getHttpOption()).pipe(
    //     map(res =>  res.json()),
    //     catchError(this.handleError),);
    // } 

    // customerLoad(data:any,page:number) {
    //     if(!page){    
    //        var url=this.baseApiUrl+'customersname/';
    //     } else {
    //        var url=this.baseApiUrl+'customersname/?page='+page;
    //     }
    //    return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
    //     map(res =>  res.json()),
    //     catchError(this.handleError));
    // }
    customerLoad(data:any,page:number){
        if (!page) {
            var url = this.baseApiUrl + 'global_list/';
        } else {
            var url = this.baseApiUrl + 'global_list/?page=' + page;
        }
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }
    getCustomerName(data:any) {
       return this._http.post(this.baseApiUrl+'get_customer_name/', data, this.globalService.getHttpOption()).pipe(
        map(res =>  res.json()),
        catchError(this.handleError));
    }

}