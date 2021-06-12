import { throwError as observableThrowError,  Observable } from 'rxjs';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import { Injectable} from '@angular/core'; 
import { CookieService} from 'ngx-cookie';
import { GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';

@Injectable()
export class HomeService {
	private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor( 
        private _http: Http,
        private globalService:GlobalService
    ) {
        
    }
    pageLoad(data:any){
        return this._http.post(GlobalVariable.BASE_API_URL+'page_url_to_id/', data).pipe(
        map(res =>  res.json()),
        catchError(this.handleError));
    }   

    private handleError(error: Response) { 
        return Observable.throw(error || "Server err"); 
   	}     
}	