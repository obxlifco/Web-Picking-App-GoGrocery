
import {throwError as observableThrowError,  Observable } from 'rxjs';

import {catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 

 
 
import {GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';
import {CookieService} from 'ngx-cookie';

@Injectable()
export class CategoryService {
    
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(private _http: Http,private globalService:GlobalService,private _cookieService:CookieService) {}

    basicInfoLoad(id:number){

        if(id>0){

            return this._http.get(this.baseApiUrl+'category/'+id+'/', this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
        }else{

            return this._http.get(this.baseApiUrl+'basicinfoload/', this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
        }
        
        
    }

    basicInfoAddEdit(data: any, id:any){

        this.globalService.showLoaderSpinner(true);
        let userData = this._cookieService.getObject('userData');

        let headers = new Headers({
          'Authorization': 'Token '+userData['auth_token']
        });
        let options = new RequestOptions({ headers: headers });

        if(id>0){
            return this._http.put(this.baseApiUrl+'category/'+id+'/', data, options).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
        }else{
            return this._http.post(this.baseApiUrl+'category/', data, options).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
        }       
        
    }  

    getChildCategory(parent_id:number,id:number,lvl:number){

        if(parent_id>0){

            return this._http.post(this.baseApiUrl+'getchild/', { "category_id": parent_id, "id":id,"lvl":lvl }, this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
        }

        
        
    }  
    getMarketplaceCategory(parent_id:number,channel:number){

        if(parent_id>0){

            return this._http.post(this.baseApiUrl+'child_channel/', {"channel_id":channel,"parent_id":parent_id}, this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
        }
        else{
             return this._http.post(this.baseApiUrl+'channelmapping/', { "channel_id": channel}, this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
        }
        
        
    }  

    categoryImageDelete(data:any){

        return this._http.post(this.baseApiUrl+'category_image_delete/', data, this.globalService.getHttpOption()).pipe(
        map(res =>  res.json()),
        catchError(this.handleError),);        
    }    

    categoryBannerDelete(data: any) {
        return this._http.post(this.baseApiUrl + 'categorybanner_image_delete/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError));
    }  

    categoryCustomField(id:any,channel:any){
            return this._http.get(this.baseApiUrl+'field_list/'+id+'/'+channel+'/', this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
    }
    categoryCustomFieldAddLoad(){
            return this._http.get(this.baseApiUrl+'channelscustomfield/', this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
    }
    categoryCustomFieldEdit(id:number,cat:number){
            return this._http.get(this.baseApiUrl+'customfields/'+id+'/'+cat+'/', this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
    }
    categoryCustomFieldDelete(id:number,cat:number){
            return this._http.delete(this.baseApiUrl+'customfields/'+id+'/'+cat+'/', this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
    }
    categoryCustomFieldAddEdit(data:any,id:any,cat:any){
            if(id>0){
            return this._http.put(this.baseApiUrl+'customfields/'+id+'/'+cat+'/', data, this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
            }else{
                return this._http.post(this.baseApiUrl+'customfields/', data, this.globalService.getHttpOption()).pipe(
                map(res =>  res.json()),
                catchError(this.handleError),);
            } 
    }
    categoryDefaultFieldAddEdit(data:any){
                return this._http.post(this.baseApiUrl+'customvalueupdate/', data, this.globalService.getHttpOption()).pipe(
                map(res =>  res.json()),
                catchError(this.handleError),);
    }
    categoryCustomFieldImport(data:any){
        return this._http.post(this.baseApiUrl+'customfieldsimport/', data, this.globalService.getHttpOptionFile()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
    }
    categoryCustomFieldSystem(data:any){
        return this._http.post(this.baseApiUrl+'customfieldsystem/', data, this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
    }
    categoryImportInsert(data:any){
        return this._http.post(this.baseApiUrl+'customsuccessfieldimport/', data, this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
    }
    /**
     * Metod for getting all warehouse list
     * @access public
     * @return wareHouseList object
    */
    getAllWareHouseList() {
        return this._http.get(this.baseApiUrl+'warehouse-list/',this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError));
    }
    private handleError(error: Response) { 
      return observableThrowError(error || "Server err"); 
    } 
    
    
 }      