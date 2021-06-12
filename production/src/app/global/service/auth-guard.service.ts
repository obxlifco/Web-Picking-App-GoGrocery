import { Injectable } from '@angular/core';
import { CanActivate, CanActivateChild } from '@angular/router';
import { Router } from '@angular/router';
import { GlobalService } from './app.global.service';

@Injectable()
export class AuthGuard implements CanActivate, CanActivateChild {
	constructor(
      private _router: Router, 
      private _globalService:GlobalService,
    ){}

  	canActivate() {
    	if(!this._globalService.isLoggedIn()){
  			this._router.navigate(['/login']);
    		return false;
  		}else{
  			return true;
  		}
  	}

  	canActivateChild() {
  		if(!this._globalService.isLoggedIn()){
  			this._router.navigate(['/login']);
    		return false;
  		}else{  			
    		return true;
  		}    	
  	}

}