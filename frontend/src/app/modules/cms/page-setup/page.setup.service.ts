import { throwError as observableThrowError,  Observable } from 'rxjs';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import { Injectable} from '@angular/core'; 
import { CookieService} from 'ngx-cookie';
import { GlobalVariable } from '../../../global/service/global';
import { GlobalService } from '../../../global/service/app.global.service';

@Injectable()
export class PageSetupService {
	private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(private _http: Http,private globalService:GlobalService) {}
    pageAddEdit(data:any,id:number){
      if(id) {
        return this._http.put(this.baseApiUrl+'page_update/'+id+'/', data, this.globalService.getHttpOption()).pipe(
          map(res =>  res.json()),
          catchError(this.handleError));
      } else {
          return this._http.post(this.baseApiUrl+'new_page_create/', data, this.globalService.getHttpOption()).pipe(
          map(res =>  res.json()),
          catchError(this.handleError));
      }
    }

    pageLoad(id:number){
      return this._http.get(this.baseApiUrl+'page_update/'+id+'/', this.globalService.getHttpOption()).pipe(
        map(res =>  res.json()),
        catchError(this.handleError));
    }

    getAllPages(){
      return this._http.get(this.baseApiUrl+'all_pages/'+this.globalService.getWebsiteId()+'/', this.globalService.getHttpOption()).pipe(
        map(res =>  res.json()),
        catchError(this.handleError));
    }

    getAllCategories(){
      let website_id: number = this.globalService.getWebsiteId();
      return this._http.get(this.baseApiUrl+'category_list/'+website_id+'/', this.globalService.getHttpOption()).pipe(
        map(res =>  res.json()),
        catchError(this.handleError));
    } 

    getAllParents(header_footer: number){
      return this._http.get(this.baseApiUrl+'parent_menus/'+header_footer+'/'+this.globalService.getWebsiteId()+'/', this.globalService.getHttpOption()).pipe(
        map(res =>  res.json()),
        catchError(this.handleError));
    }

    navigationAddEdit(data:any,id:number,header_footer:number){

      if(id){
        return this._http.put(this.baseApiUrl+'menu_edit/'+id+'/'+header_footer+'/', data, this.globalService.getHttpOption()).pipe(
          map(res =>  res.json()),
          catchError(this.handleError));  
      }else{
        return this._http.post(this.baseApiUrl+'create_menu/', data, this.globalService.getHttpOption()).pipe(
          map(res =>  res.json()),
          catchError(this.handleError));  
      }
    }

    getHeaderMenus(header_footer:number){
      return this._http.get(this.baseApiUrl+'all_menu/'+header_footer+'/'+this.globalService.getWebsiteId()+'/', this.globalService.getHttpOption()).pipe(
        map(res =>  res.json()),
        catchError(this.handleError));
    }

    navigationLoad(id:number,header_footer:number){
      return this._http.get(this.baseApiUrl+'menu_edit/'+id+'/'+header_footer+'/', this.globalService.getHttpOption()).pipe(
        map(res =>  res.json()),
        catchError(this.handleError));
    }

    private handleError(error: Response) { 
      return Observable.throw(error || "Server err"); 
   	}     
}	