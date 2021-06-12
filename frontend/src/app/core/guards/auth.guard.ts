import { Injectable } from '@angular/core';
import { CanActivate, CanActivateChild, Router,GuardsCheckEnd } from '@angular/router';
import {GlobalService} from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { filter } from 'rxjs/operators';
import { Observable} from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate, CanActivateChild {

  public after_login_url:string;
  constructor(
      private _router: Router, 
      public _globalService:GlobalService,
      public _cookieService: CookieService
    ){}

    // canActivate() {
    //   if(!this._globalService.isLoggedInFrontend()){         
    //     this._router.events.pipe(
    //         filter((event: any) => event instanceof GuardsCheckEnd)
    //         ).subscribe((res) => {
    //             if(!res.shouldActivate){
    //               this.after_login_url = res.url;
    //               this._cookieService.put('after_login_redirect',this.after_login_url);
    //             }
    //     });
    //     this._router.navigate(['/home']);
    //     return false;
    //   } else {        
    //     return true;
    //   }
    // }

    // canActivateChild() {
    //   if(!this._globalService.isLoggedInCustomer()){         
    //     this._router.events.pipe(
    //       filter((event: any) => event instanceof GuardsCheckEnd)
    //       ).subscribe((res) => {
    //           console.log('canActivateChild');
    //           console.log(res);
    //           alert()
    //           if(!res.shouldActivate){
    //             this.after_login_url = res.url;
    //             // this._cookieService.put('after_login_redirect',this.after_login_url);
    //           }
    //     });
    //     this._router.navigate(['/home']);
    //     return false;
    //   } else {
    //     return true;
    //   }
    // }


    canActivate() {
      console.log(this._globalService.isLoggedInCustomer());
      
    	if(!this._globalService.isLoggedInCustomer()){
  			this._router.navigate(['/home']);
    		return false;
  		}else{
  			return true;
  		} 
  	}

  	canActivateChild() {
    	if(!this._globalService.isLoggedInCustomer()){
  			this._router.navigate(['/home']);
    		return false;
  		}else{
  			return true;
  		}    	
  	}
}