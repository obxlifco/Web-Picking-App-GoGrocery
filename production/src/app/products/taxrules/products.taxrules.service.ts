
import {throwError as observableThrowError,  Observable } from 'rxjs';

import {catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 

 
 
import {GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';
import {CookieService} from 'ngx-cookie';

@Injectable()
export class TaxrulesService {

    private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(private _http: Http, private globalService: GlobalService, private _cookieService: CookieService) {}
    public post_data = {};



    private handleError(error: Response) {
        return observableThrowError(error || "Server err");
    }

   
    allCategoryLoad() {

        return this._http.get(this.baseApiUrl + 'catrgoryconditionsset/', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    categoryLoad(id: number) {

        if (id > 0) {
            return this._http.get(this.baseApiUrl + 'categorieslistdiscount/' + id + '/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        } else {
            return this._http.get(this.baseApiUrl + 'category_load/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        }
    }

    productLoad(data) {

        return this._http.post(this.baseApiUrl + 'productload/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );

    }

    customerGroupLoad(data) {

        return this._http.post(this.baseApiUrl + 'customertype/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );

    }

    customerLoad(data) {

        return this._http.post(this.baseApiUrl + 'discountcustomer/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );

    }
}