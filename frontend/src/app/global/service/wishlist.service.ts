import { Injectable } from '@angular/core';
import { throwError as observableThrowError,  Observable,BehaviorSubject} from 'rxjs';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {GlobalVariable} from './global';
import {AuthenticationService} from './authentication.service';
import {} from './app.global.service';


@Injectable({
  providedIn: 'root'
})
export class WishlistService {
 public totalWishListCount;
 readonly apiBaseUrl = GlobalVariable.BASE_API_URL;
 constructor(private _authService : AuthenticationService) { }

  getTotalWishListCount() {
  	

  }

}
