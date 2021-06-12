
import {throwError as observableThrowError,  Observable } from 'rxjs';

import {map, catchError} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 

 
 
import {GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';
import {CookieService} from 'ngx-cookie';

@Injectable()
export class StockAdjustmentService {
    
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(private _http: Http,private globalService:GlobalService,private _cookieService:CookieService) {}
    public post_data = {};

    doGrid(data:any,page:number) {

       if(!page){var url=this.baseApiUrl+'stockadjustmentlist/';}
       else{var url=this.baseApiUrl+'stockadjustmentlist/?page='+page;}
       return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
       map(res =>  res.json()),
       catchError(this.handleError),); 
    } 
    doStatusUpdate(model:any,bulk_ids:any,type:any)
    {   
        var up_arr:any=[];
        bulk_ids.forEach(function(item:any){
          var obj={"id":item};
          up_arr.push(obj);
        }); 
        if(type==2){var field_name='isdeleted';var val='y';}
        else if(type==1){var field_name='isblocked';var val='y';}
        else if(type==0){var field_name='isblocked';var val='n';}
        this.post_data={"table":{"table":model,"field_name":field_name,"value":val},"data":up_arr}

        return this._http.post(this.baseApiUrl+'globalupdate/', this.post_data, this.globalService.getHttpOption()).pipe(
       map(res =>  res.json()),
       catchError(this.handleError),);
    }
    doGridFilter(model:any,isdefault:any,cols:any,screen:any)
    {
        if(isdefault==1)
         {
          this.post_data={model: model, is_default: isdefault, screen_name: screen, "header_name":"","field_name":""}
         }
         else{
          var header_name:any=[];
            var field_name:any=[];
            cols.forEach(function(item:any){
                if(item.show==1){
                  header_name.push(item.title);
                  if(item.child!=''){
                    field_name.push(item.field+'.'+item.child);  
                  }else{
                    field_name.push(item.field); 
                  } 
                }
            });
            var header_name = header_name.join("@@");
            var field_name = field_name.join("@@");
            this.post_data={model: model, screen_name: screen, "header_name":header_name,"field_name":field_name}
         }
        return this._http.post(this.baseApiUrl+'global_list_filter/', this.post_data, this.globalService.getHttpOption()).pipe(
       map(res =>  res.json()),
       catchError(this.handleError),);
    }

    private handleError(error: Response) { 
      return observableThrowError(error || "Server err"); 
       } 

    
 }		