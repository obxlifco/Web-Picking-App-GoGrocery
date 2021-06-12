
import {throwError as observableThrowError,  Observable } from 'rxjs';

import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 

 
 
import {GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';

@Injectable()
export class AreaService {
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    public post_data = {};
    constructor(private _http: Http, private globalService: GlobalService) {}

    private handleError(error: Response) {
        return observableThrowError(error || "Server err");
    }

    exportData(search_filter, location_type: any) {
        let data:any = {};
        data['search_filter'] = search_filter;
        data['location_type'] = location_type;
        data['website_id'] = this.globalService.getWebsiteId();
        return this._http.post(this.baseApiUrl + 'export_area/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    saveFileData(data: any) {
        return this._http.post(this.baseApiUrl + 'import_area/', data, this.globalService.getHttpOptionFile()).pipe(
            map(res => res.json()),
            catchError(this.handleError),);
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

    loadManagerList() {
        return this._http.get(this.baseApiUrl + 'manager_list/', this.globalService.getHttpOption()).pipe(
          map(res => res.json()),
          catchError(this.handleError),);   
    }

    loadZoneMaster() {
        return this._http.get(this.baseApiUrl + 'zone_list/', this.globalService.getHttpOption()).pipe(
          map(res => res.json()),
          catchError(this.handleError),);   
    }

    loadWarehouse() {
        return this._http.get(this.baseApiUrl + 'warehouse-list/', this.globalService.getHttpOption()).pipe(
          map(res => res.json()),
          catchError(this.handleError),);   
    }

    saveMasterData(data:any) {
        return this._http.post(this.baseApiUrl + 'zone/', data, this.globalService.getHttpOptionFile()).pipe(
            map(res => res.json()),
            catchError(this.handleError),);
    }

    getZoneDetails(zone_id:number) {
        return this._http.get(this.baseApiUrl + 'zone_list/'+zone_id+'/', this.globalService.getHttpOption()).pipe(
          map(res => res.json()),
          catchError(this.handleError),);      
    }

    loadZoneZipCode(data:any) {
        return this._http.post(this.baseApiUrl + 'zipcode_list/', data, this.globalService.getHttpOptionFile()).pipe(
            map(res => res.json()),
            catchError(this.handleError),);   
    }

    loadZoneArea(data:any) {
         return this._http.post(this.baseApiUrl + 'areaname_list/', data, this.globalService.getHttpOptionFile()).pipe(
            map(res => res.json()),
            catchError(this.handleError),);   
    }
}	
