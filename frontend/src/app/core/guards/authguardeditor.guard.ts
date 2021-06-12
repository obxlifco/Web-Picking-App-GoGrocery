import { Injectable, Inject } from '@angular/core';
import { CanActivate, CanActivateChild, Router,GuardsCheckEnd } from '@angular/router';
import {GlobalService} from '../../global/service/app.global.service';
import {GlobalVariable} from '../../global/variable/global-variable';
import { CookieService } from 'ngx-cookie';
import { filter } from 'rxjs/operators';
import { Observable} from 'rxjs';
import { WINDOW } from '@ng-toolkit/universal';
@Injectable({
  providedIn: 'root'
})
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
