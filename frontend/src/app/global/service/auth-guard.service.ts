import { Injectable, Inject } from '@angular/core';
import { CanActivate, CanActivateChild, Router,GuardsCheckEnd, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { GlobalService } from './app.global.service';
import { GlobalVariable } from '../../global/service/global';
import { ShoppingCartService } from './app.cart.service';
import { CookieService } from 'ngx-cookie';
import { Observable } from 'rxjs';
import { filter } from 'rxjs/operators';
import { WINDOW } from '@ng-toolkit/universal';
import { AuthenticationService } from './authentication.service';
@Injectable()
export class AuthGuardEditor implements CanActivate, CanActivateChild {
	constructor(@Inject(WINDOW) private window: Window, 
      private _router: Router, 
      public _globalService:GlobalService,
    ){}

  	canActivate() {
    	if(!this._globalService.isLoggedIn()){
        let editor_url: string = GlobalVariable.BASE_Backend_URL+'login';
        this.window.open(editor_url, "_parent");
  			return false;
  		} else {
    		return true;
  		}
  	}

  	canActivateChild() {
  		if(!this._globalService.isLoggedIn()){
        let editor_url: string = GlobalVariable.BASE_Backend_URL+'login';
        this.window.open(editor_url, "_parent");
  			// this._router.navigate(['/list']);
    		return false;
  		} else {
    		return true;
  		}
  	}
}

// @Injectable()
// export class AuthGuard implements CanActivate, CanActivateChild {

//   public after_login_url:string;
//   constructor(
//       private _router: Router, 
//       public _globalService:GlobalService,
//       public _cookieService: CookieService
//     ){}

//     canActivate() {
//       if(!this._globalService.isLoggedInFrontend()){         
//         this._router.events.pipe(
//             filter((event: any) => event instanceof GuardsCheckEnd)
//             ).subscribe((res) => {
//                 if(!res.shouldActivate){
//                   this.after_login_url = res.url;
//                   this._cookieService.put('after_login_redirect',this.after_login_url);
//                 }
//         });
//         this._router.navigate(['/login']);
//         return false;
//       } else {        
//         return true;
//       }
//     }

//     canActivateChild() {
//       if(!this._globalService.isLoggedInFrontend()){         
//         this._router.events.pipe(
//              filter((event: any) => event instanceof GuardsCheckEnd)
//             ).subscribe((res) => {
//                 if(!res.shouldActivate){
//                   this.after_login_url = res.url;
//                   this._cookieService.put('after_login_redirect',this.after_login_url);
//                 }
//         });
//         this._router.navigate(['/login']);
//         return false;
//       } else {
//         return true;
//       }
//     }
// }

@Injectable()
export class AuthGuardMerchant implements CanActivate, CanActivateChild {
  constructor(
      private _router: Router, 
      public _globalService:GlobalService,
    ){}

    canActivate() {
      if(this._globalService.isLoggedInFrontend()){
        this._router.navigate(['/']);
        return false;
      } else {
        return true;
      }
    }

    canActivateChild() {
      if(!this._globalService.isLoggedInFrontend()){
        this._router.navigate(['/']);
        return false;
      } else {
        return true;
      }
    }
}




@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
    constructor(
        private router: Router,
        private authenticationService: AuthenticationService
    ) { }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
        const currentUser = this.authenticationService.currentUserValue;
        if (currentUser) {
            // logged in so return true
            return true;
        }

        // not logged in so redirect to login page with the return url
        this.router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
        return false;
    }
}