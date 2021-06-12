
import {throwError as observableThrowError,  Observable } from 'rxjs';

import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 

 
 
import {GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';

@Injectable()
export class vehicleService {
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    public post_data = {};
    constructor(private _http: Http, private globalService: GlobalService) {}

    private handleError(error: Response) {
        return observableThrowError(error || "Server err");
    }

    loadCountry() {
        return this._http.get(this.baseApiUrl + 'countrylist/', this.globalService.getHttpOption()).pipe(
        map(res => res.json()),
        catchError(this.handleError),);
    }

    loadStates(country_id) {
      return this._http.get(this.baseApiUrl + 'countrystatelist/' + country_id+'/', this.globalService.getHttpOption()).pipe(
          map(res => res.json()),
          catchError(this.handleError),);
    }

    loadManagerList(data:any) {
        return this._http.post(this.baseApiUrl + 'delivery-manager-list/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError),);
    }

    loadZoneMaster() {
        return this._http.get(this.baseApiUrl + 'zone_list/', this.globalService.getHttpOption()).pipe(
          map(res => res.json()),
          catchError(this.handleError),);   
    }

    loadWarehouseList() {
        return this._http.get(this.baseApiUrl + 'warehouse-list/', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError));
    }

    saveVehicleData(data:any) {
        return this._http.post(this.baseApiUrl + 'vehicle/', data, this.globalService.getHttpOptionFile()).pipe(
            map(res => res.json()),
            catchError(this.handleError),);
    }

    loadVehicleDetails(vehicleId:number) {
        return this._http.get(this.baseApiUrl + 'vehicle/'+vehicleId+'/', this.globalService.getHttpOption()).pipe(
        map(res => res.json()),
        catchError(this.handleError),);
    }
    
}
