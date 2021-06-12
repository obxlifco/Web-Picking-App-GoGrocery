import { Injectable,Inject} from '@angular/core';
//import { HttpClient } from '@angular/common/http';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import { BehaviorSubject, Observable } from 'rxjs';
//import { Http, Headers,RequestOptions} from '@angular/http';
import { map,catchError} from 'rxjs/operators';
import { GlobalVariable } from "../../global/service/global";
import {GlobalService} from "../../global/service/app.global.service";
import {CartService} from "../../global/service/cart.service";
import { Router } from '@angular/router';
import { LOCAL_STORAGE , WINDOW} from '@ng-toolkit/universal';
import { AuthService } from "angularx-social-login";

@Injectable({ providedIn: 'root' })
export class AuthenticationService {
    private currentUserSubject: BehaviorSubject<any>;
    public currentUser: Observable<any>;
    public userLastName:any;
    public userFirstName:any;
    public isSocialLogin:boolean = false;
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    //public isUser
    constructor(
        private http: Http,
        private _globalService:GlobalService,
        private _router: Router,
        private _cartService:CartService,
        private authService: AuthService,
        @Inject(LOCAL_STORAGE) private localStorage: any,
        @Inject(WINDOW) private window: Window

    ) {
        let currentUserData = this.localStorage.getItem('currentUser') ? JSON.parse(this.localStorage.getItem('currentUser')) : '';
        this.currentUserSubject = new BehaviorSubject<any>(currentUserData);
        this.currentUser = this.currentUserSubject.asObservable();
    }

    public get currentUserValue(): any {
        return this.currentUserSubject.value;
    }

    login(user_mail: string, user_password: string) {
        let deviceId = this._globalService.getGlobalDataByKey('requested_ip');
        let headers = new Headers({'DEVICEID' : deviceId});
        let requestOptions = new RequestOptions({ headers: headers });
        let userLoginData ={ user_mail, user_password };
        //return this.http.post(this.baseApiUrl+'login/',userLoginData,requestOptions)
        return this.http.post(this.baseApiUrl+'login/',userLoginData,requestOptions).pipe(map(user => {
            user = user.json();
            if (user && user['data'] && user['status']==200) {
                this.localStorage.setItem('currentUser', JSON.stringify(user['data']));
                this.currentUserSubject.next(user);
                /*this._cartService.syncCartData().subscribe(response => {
                    console.log("**************** Sync data response ******************",response);
                    
                });*/
                this._cartService.syncCartDataAndRestoreItem();
                
                if(this.currentUserSubject.value.first_name==undefined){
                    this.userFirstName=user['data'].first_name;
                    this.userLastName=user['data'].last_name;
                }
                this.getSaveListCount();
            }
            return user;
        }),
        catchError(error => this._globalService.handleError(error))); 
    }
    getSaveListCount(){
		this._cartService.saveListCount().subscribe(
			data => {
				// alert(JSON.stringify(data));
				if (data.status==200) {
					this._cartService.wishlistCount=data.total_count;
				}
			},
			err => { },
			function () {
				//completed callback
			}
		);
	}
    currentUserVal(): any {
        return this.currentUserSubject.value;
    }
    logout() {
        // remove user from local storage to log user out
        let userData = this.localStorage.getItem('currentUser') ? JSON.parse(this.localStorage.getItem('currentUser')) : {};
        if(userData && userData['login-type'] && (userData['login-type'] == 'facebook' || userData['login-type'] == 'google')) {
            console.log("************** Social login *************");
            this.authService.signOut();
        }
        this.localStorage.removeItem('currentUser');
        this.userFirstName=null;
        this.userLastName=null;
        let routerUrl=this._router.url;

        /*if(routerUrl.includes('profile') || routerUrl.includes('checkout')){
            this._router.navigate(['/home']);
        }*/
        this._cartService.wishlistCount=0;
        this._router.navigate(['/home']);
    }
    signup(userSignupObject = {}) {
        let deviceId = this._globalService.getGlobalDataByKey('requested_ip');
        let headers = new Headers({'DEVICEID' : deviceId});
        let requestOptions = new RequestOptions({ headers: headers });
        userSignupObject['address'] = 'TEST';
        return this.http.post(this.baseApiUrl+'signup-test/',userSignupObject,requestOptions).pipe(
           map(user => {
                user = user.json();
                if (user && user['status'] == 200 && user['data']) {
                    this.localStorage.setItem('currentUser', JSON.stringify(user['data']));
                    this._cartService.syncCartDataAndRestoreItem();
                    this.currentUserSubject.next(user);
                    if(this.currentUserSubject.value.first_name==undefined){
                        this.userFirstName=user['data'].first_name;
                        this.userLastName=user['data'].last_name;
                    }
                }
               return user;
            }),
           catchError(error => this._globalService.handleError(error)));
    }

    private handleError(error: Response) { 
        return Observable.throw(error || "Server err"); 
    }

    forgetPassword(email){
       let userName={
           email:email
       }
        return this.http.post(this.baseApiUrl+'forgotpassword/',userName).pipe(
            map(res =>  res.json()),
        catchError(error => this._globalService.handleError(error))); 
    }

    confirmPassword(data){
        return this.http.post(this.baseApiUrl+'confirm-password/',data).pipe(
            map(res =>  res.json()),
        catchError(error => this._globalService.handleError(error))); 
    }
    /**
     * Method for social login
    */
    socialLogin(socialLoginData) {
        let deviceId = socialLoginData['device_id'];
        let headers = new Headers({
          'DEVICEID': deviceId
        });
      let options = new RequestOptions({ headers: headers });
        return this.http.post(this.baseApiUrl+'social-login/',socialLoginData,options).pipe(
           map(user => {
                user = user.json();
                if (user && user['status'] == 200 && user['data']) {
                    this.localStorage.setItem('currentUser', JSON.stringify(user['data']));
                    this._cartService.syncCartDataAndRestoreItem();
                    this.currentUserSubject.next(user);
                    if(this.currentUserSubject.value.first_name==undefined){
                        this.userFirstName=user['data'].first_name;
                        this.userLastName=user['data'].last_name;
                    }
                }
               return user;
            }),
           catchError(error => this._globalService.handleError(error)));
        
    }

}