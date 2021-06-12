import { Injectable } from '@angular/core';
import { CanActivate, CanActivateChild, Router,GuardsCheckEnd } from '@angular/router';
import {GlobalService} from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { filter } from 'rxjs/operators';
import { Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
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
