import {throwError as observableThrowError,  Observable } from 'rxjs';
import {catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 
import {GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';
@Injectable()
export class StockService {
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(
        private _http: Http,
        private globalService:GlobalService
    ) {

    }
  warehouseLoad(websiteId,userId){
    return this._http.get(this.baseApiUrl + 'warehousestockmanagement/' + websiteId + '/' + userId+'/', this.globalService.getHttpOption()).pipe(
         	map(res =>  res.json()),
         	catchError(this.handleError),);
    }

    stockLoad(data: any, page:number){
      if(page==0){var url=this.baseApiUrl+'stocklist/';}
      else{var url=this.baseApiUrl+'stocklist/?page='+page;}
      return this._http.post(url, data,this.globalService.getHttpOption()).pipe(
         map(res =>  res.json()),
         catchError(this.handleError),);
    }

    manageStockLoad(){
      return this._http.get(this.baseApiUrl+'managestockload/', this.globalService.getHttpOption()).pipe(
           map(res =>  res.json()),
           catchError(this.handleError),);
    }

    stockAdjustment(data: any){
      return this._http.put(this.baseApiUrl+'stocklistview/', data,this.globalService.getHttpOption()).pipe(
         map(res =>  res.json()),
         catchError(this.handleError),);
    }

    stockMove(data: any){

      return this._http.put(this.baseApiUrl+'stockmove/', data,this.globalService.getHttpOption()).pipe(
         map(res =>  res.json()),
         catchError(this.handleError),);
    } 

    safetyStockUpdate(data: any){

      return this._http.post(this.baseApiUrl+'updatesafetystock/', data,this.globalService.getHttpOption()).pipe(
         map(res =>  res.json()),
         catchError(this.handleError),);
    }        
  
    private handleError(error: Response) { 
      return observableThrowError(error || "Server err"); 
     } 
     
  SaveStockFileData(data: any) {
    return this._http.post(this.baseApiUrl + 'import_sheet/', data, this.globalService.getHttpOptionFile()).pipe(
      map(res => res.json()),
      catchError(this.handleError),);
  }
    
 }		