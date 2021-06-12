
import {throwError as observableThrowError, 
    Observable
} from 'rxjs';

import {catchError, map} from 'rxjs/operators';
import {
    Http, Response, Headers, RequestOptions
}
from '@angular/http';
import {
    Injectable
}
from '@angular/core';



import {
    GlobalVariable
}
from '../../global/service/global';
import {
    GlobalService
}
from '../../global/service/app.global.service';@
Injectable()
export class GroupService {
    private baseApiUrl = GlobalVariable.BASE_API_URL; //set base url of the api
    constructor(private _http: Http, private globalService: GlobalService) {}
        // Call api at the time of group page load
    groupLoad(id: number) {
            if (id > 0) { // Get a particular group info at the time of edit group
                return this._http.get(this.baseApiUrl + 'group/' + id + '/', this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError),);
            } else { // Get necessary info at the time of add group
                return this._http.get(this.baseApiUrl + 'getmenu_group/', this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError),);
            }
        }
        // Call api at the time of group add or edit to submit form
    groupAddEdit(data: any, id: any) {
            if (id > 0) { //update group
                return this._http.put(this.baseApiUrl + 'group/' + id + '/', data, this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError),);
            } else { //add group
                return this._http.post(this.baseApiUrl + 'group/', data, this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError),);
            }
        }
        // Error handler method
    private handleError(error: Response) {
        return observableThrowError(error || "Server err");
    }
}