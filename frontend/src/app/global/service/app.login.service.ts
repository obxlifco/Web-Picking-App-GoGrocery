import { throwError as observableThrowError,  Observable } from 'rxjs';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import { Injectable} from '@angular/core'; 
import { CookieService} from 'ngx-cookie';
import { GlobalVariable } from './global';
import { GlobalService } from './app.global.service';

@Injectable()
export class LoginService {
    
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(
      private _http: Http, 
      private _cookieService: CookieService, 
      private globalService: GlobalService) {}

    getCookie(key: string){
      return this._cookieService.get(key);
    }

    doLogin(data:any) {
   
       return this._http.post(this.baseApiUrl+'login/', data, {}).pipe(
       map(res =>  res.json()),
       catchError(this.handleError));     	    
    }

    GoogleLogin(data:any) {
       return this._http.post(this.baseApiUrl+'createusergoogle-facebook/', data, {}).pipe(
       map(res =>  res.json()),
       catchError(this.handleError));          
    }

    doRegister(data:any){
      return this._http.post(this.baseApiUrl+'createuser-frontend/', data, {}).pipe(
       map(res =>  res.json()),
       catchError(this.handleError)); 
    }

    checkEmail(data:any) {
       return this._http.post(this.baseApiUrl+'forgotpassword/', data, {}).pipe(
       map(res =>  res.json()),
       catchError(this.handleError));          
    }

    verifyCode(data:any) {
       return this._http.post(this.baseApiUrl+'verification/', data, {}).pipe(
       map(res =>  res.json()),
       catchError(this.handleError));          
    }

    changePwd(data:any){
      return this._http.post(this.baseApiUrl+'changepassword/', data, {}).pipe(
       map(res =>  res.json()),
       catchError(this.handleError)); 
    }

    optvaluesend(data:any){
        return this._http.post(this.baseApiUrl+'createotp/', data, {}).pipe(
       map(res =>  res.json()),
       catchError(this.handleError)); 

    }
    checkotp(data:any){
        return this._http.post(this.baseApiUrl+'checkotp/', data, {}).pipe(
       map(res =>  res.json()),
       catchError(this.handleError));
    }

    private handleError(error: Response) { 
      return Observable.throw(error || "Server err"); 
   }
   
 }		