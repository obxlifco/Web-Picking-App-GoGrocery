
import {throwError as observableThrowError,  Observable } from 'rxjs';

import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 

 
 
import {GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';

@Injectable()
export class DeliverymanagerService {
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

  
    saveMasterData(data:any) {
      return this._http.post(this.baseApiUrl + 'delivery_manager/', data, this.globalService.getHttpOptionFile()).pipe(
          map(res => res.json()),
          catchError(this.handleError),);
    }

    getManagereDetails(manager_id:number) {
      return this._http.get(this.baseApiUrl + 'delivery-manager-details/'+manager_id+'/', this.globalService.getHttpOption()).pipe(
      map(res => res.json()),
      catchError(this.handleError),);      
    }
}