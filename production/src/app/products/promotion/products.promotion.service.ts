import { throwError as observableThrowError,  Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { Injectable } from '@angular/core';
import { GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';

@Injectable()
export class PromotionService {
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(private _http: Http,private globalService:GlobalService) {}
    promotionLoad(id:number){
        if(id>0){
            return this._http.get(this.baseApiUrl+'discount/'+id+'/', this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
        } else {
            return this._http.get(this.baseApiUrl+'discount_load/', this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
        }
    }

    promotionAddEdit(data: any, id:any) {
        if(id>0){
            return this._http.put(this.baseApiUrl+'discount/'+id+'/', data, this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
        } else {
            return this._http.post(this.baseApiUrl+'discount/', data, this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
        }
    }

    conditionLoad(id: number){
        if(id>0){
            return this._http.get(this.baseApiUrl+'discountconditions/'+id+'/', this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
        }else{

        }
    } 

    conditionAddEdit(data: any, id:any){    
        return this._http.post(this.baseApiUrl+'discountconditions/', data, this.globalService.getHttpOption()).pipe(
        map(res =>  res.json()),
        catchError(this.handleError),);
    } 

    allCategoryLoad(){
        return this._http.get(this.baseApiUrl+'catrgoryconditionsset/', this.globalService.getHttpOption()).pipe(
        map(res =>  res.json()),
        catchError(this.handleError),);
    }         

    categoryLoad(id: number) {
        if(id>0){
            return this._http.get(this.baseApiUrl+'categorieslistdiscount/'+id+'/', this.globalService.getHttpOption()).pipe(
            map(res =>  res.json()),
            catchError(this.handleError),);
        }else{
            return this._http.get(this.baseApiUrl+'category_load/', this.globalService.getHttpOption()).pipe(
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

    productLoad(data:any,page:number) {
        if (!page) {
            var url = this.baseApiUrl + 'product_list/';
        } else {
            var url = this.baseApiUrl + 'product_list/?page=' + page;
        }
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
        map(res =>  res.json()),
        catchError(this.handleError));
    }  
  
    customerGroupLoad(data:any,page:number){
        if (!page) {
            var url = this.baseApiUrl + 'global_list/';
        } else {
            var url = this.baseApiUrl + 'global_list/?page=' + page;
        }
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    customerLoad(data:any,page:number){
        if (!page) {
            var url = this.baseApiUrl + 'global_list/';
        } else {
            var url = this.baseApiUrl + 'global_list/?page=' + page;
        }
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }     

    private handleError(error: Response) { 
      return observableThrowError(error || "Server err"); 
    } 
    
    //CREDIT POINT EARN START
    savePromotionFileData(data: any) {
        return this._http.post(this.baseApiUrl + 'import_discount/', data, this.globalService.getHttpOptionFile()).pipe(
            //return this._http.post(this.baseApiUrl + 'savehsncode/', data, this.globalService.getHttpOptionFile()).pipe(
            map(res => res.json()),
            catchError(this.handleError),);
    }
    
    conditionPointAddEdit(data: any, id:any){
        return this._http.post(this.baseApiUrl+'loyaltyconditions/', data, this.globalService.getHttpOption()).pipe(
        map(res =>  res.json()),
        catchError(this.handleError),);
    }
    //CREDIT POINT EARN END

    //PROMOTION IMPORT START
    import_promotion_file_data(data: any) {
        return this._http.post(this.baseApiUrl + 'import_discount/', data, this.globalService.getHttpOptionFile()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    save_promotion_file_data(data: any) {
        return this._http.post(this.baseApiUrl + 'save_file_discounts/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    load_promotion_preview_grid(data: any, page: number) {
        //console.log(data);
        if (!page) {
            var url = this.baseApiUrl + 'preview_save_discounts/';
        } else {
            var url = this.baseApiUrl + 'preview_save_discounts/?page=' + page;
        }
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    show_all_promotion_imported(data: any) {
        var url = this.baseApiUrl + 'save_all_imported_discounts/';
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }
    //PROMOTION IMPORT ENAD

    warehouseLoad(data:any){
        var url = this.baseApiUrl + 'global_list/';
        
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }
 }      