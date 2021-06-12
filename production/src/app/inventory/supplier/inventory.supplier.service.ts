import {throwError as observableThrowError,  Observable } from 'rxjs';
import {map, catchError} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 
import {GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';

@Injectable()

export class SupplierService {
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(private _http: Http, private globalService: GlobalService) {}
    
    supplierLoad(id: number) {
        if (id > 0) {
            return this._http.get(this.baseApiUrl + 'suppliers/' + id + '/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        } else {
            return this._http.get(this.baseApiUrl + 'Suppliersadd/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        }
    }

    supplierAddEdit(data: any, id: any) {
        if (id > 0) {
            return this._http.put(this.baseApiUrl + 'suppliers/' + id + '/', data, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        } else {
            return this._http.post(this.baseApiUrl + 'suppliers/', data, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        }
    }

    supplierState(id: any) {
        return this._http.get(this.baseApiUrl + 'statelist/' + id + '/', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }
    
    private handleError(error: Response) {
        return observableThrowError(error || "Server err");
    }
}   