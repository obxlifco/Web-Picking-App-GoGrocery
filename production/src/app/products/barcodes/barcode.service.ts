
import {throwError as observableThrowError,  Observable } from 'rxjs';

import {catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 

 
 
import {GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';

@Injectable({
  providedIn: 'root'
})
export class BarcodeService {

  private baseApiUrl = GlobalVariable.BASE_API_URL;
  constructor(private _http: Http,private globalService:GlobalService) {}


      

  private handleError(error: Response) { 
    return observableThrowError(error || "Server err"); 
  } 
  
  
  //CREDIT POINT EARN START
  savePromotionFileData(data: any) {
      return this._http.post(this.baseApiUrl + 'importbarcodes/', data, this.globalService.getHttpOptionFile()).pipe(
        //return this._http.post(this.baseApiUrl + 'savehsncode/', data, this.globalService.getHttpOptionFile()).pipe(
        map(res => res.json()),
        catchError(this.handleError),);
  }
  
  
  //CREDIT POINT EARN END

  //PROMOTION IMPORT START
  import_barcode_file_data(data: any) {
    return this._http.post(this.baseApiUrl + 'importbarcodes/', data, this.globalService.getHttpOptionFile()).pipe(
        map(res => res.json()),
        catchError(this.handleError), );
  }

  save_promotion_file_data(data: any) {
    return this._http.post(this.baseApiUrl + 'saveallimportedbarcodes/', data, this.globalService.getHttpOption()).pipe(
      map(res => res.json()),
      catchError(this.handleError), );
  }

  load_barcode_preview(data: any, page: number=null) {
      //console.log(data);
      if (!page) {
          var url = this.baseApiUrl + 'previewimportedbarcodes/';
      } else {
          var url = this.baseApiUrl + 'previewimportedbarcodes/?page=' + page;
      }
      return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
          map(res => res.json()),
          catchError(this.handleError), );
  }

  show_all_barcode_imported(data: any) {
      var url = this.baseApiUrl + 'saveallimportedbarcodes/';
      return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
          map(res => res.json()),
          catchError(this.handleError), );
  }
  //PROMOTION IMPORT ENAD
}
