import { Injectable } from '@angular/core';
import {GlobalService} from './app.global.service';
import {GlobalVariable} from './global';
import { throwError as observableThrowError,  Observable} from 'rxjs';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';


@Injectable({
  providedIn: 'root'
})
export class MyProfileService {

  
  readonly apiBaseUrl = GlobalVariable.BASE_API_URL;

  constructor(private _gs:GlobalService,private _http:Http) { }

  getActiveUserProfileDetails() {
  	let authorizedHeader = this._gs.getHttpOptionFrontendUser();
  	return this._http.get(this.apiBaseUrl+'my-profile/',authorizedHeader).pipe(
			   map(res =>  res.json()),
			   catchError(err => this._gs.handleError(err)));

  }

  
}
