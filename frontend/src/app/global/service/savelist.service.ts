import { Injectable } from '@angular/core';
import { Observable,throwError} from 'rxjs'
import { catchError, map} from 'rxjs/operators'; 
import { Http, Response, Headers, RequestOptions,} from '@angular/http';
import { HttpParams } from '@angular/common/http';
import { GlobalService } from './app.global.service';
import {GlobalVariable} from './global';

@Injectable({
  providedIn: 'root'
})
export class SavelistService {

  readonly apiBaseUrl = GlobalVariable.BASE_API_URL;

  constructor(private _gs:GlobalService,private _http:Http) { 

  }
  /**
   * Metod for getting savelist
  */
  getSaveList() {
  	let httpRequestOption = this._gs.getHttpOptionFrontendUser();
  	return this._http.get(this.apiBaseUrl+'save-list/',httpRequestOption).pipe(
			   map(res =>  res.json()),
			   catchError(error => this._gs.handleError(error)));
  }
  /**
   * Delete saveList
  */
  deleteSaveList(saveListId) {
  	let httpRequestOption = this._gs.getHttpOptionFrontendUser();
  	return this._http.delete(this.apiBaseUrl+'addeditdelete-from-savelist/'+saveListId+'/',httpRequestOption).pipe(
			   map(res =>  res.json()),
			   catchError(error => this._gs.handleError(error)));


  }


}
