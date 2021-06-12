import { throwError as observableThrowError,  Observable } from 'rxjs';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
/*import { HttpClient, HttpHeaders } from '@angular/common/http';*/
import { Injectable} from '@angular/core'; 
import { CookieService} from 'ngx-cookie';
import { GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';
import { LoaderService } from '../../global/service/loader.service';

@Injectable()
export class PageService {
	private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(
        private _http: Http,
        private _loader:LoaderService,
        private globalService:GlobalService
        ) {
        
    }

    pageLoad(data:any){
        //this._loader.show();
        return this._http.post(GlobalVariable.BASE_API_URL+'page_url_to_id/', data).pipe(
        map(res =>  res.json()),
        catchError(this.handleError));
    }

    private handleError(error: Response) { 
        return Observable.throw(error || "Server err"); 
   	}     
}	