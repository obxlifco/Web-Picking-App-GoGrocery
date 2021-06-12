import { throwError as observableThrowError,  Observable } from 'rxjs';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import { Injectable} from '@angular/core'; 
import { BehaviorSubject } from 'rxjs';
import { CookieService} from 'ngx-cookie';
import { GlobalService } from './app.global.service';
import { Router } from '@angular/router';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
'use strict';
export const GlobalVariable = Object.freeze({
    //BASE_API_URL: 'http://' + window.location.hostname + ':8062/api/',
    BASE_API_URL: 'http://192.168.0.228:8062/api/',
    // BASE_API_URL: 'http://navsoft.co.in:8062/api/',
    GOOGLE_CLIENT_ID: '74854632065-86uci4hndsgo2eljc8nh45uh2ol2qgtg.apps.googleusercontent.com',
    //S3_URL: 'https://s3-ap-southeast-1.amazonaws.com/primemallnew/'   
    S3_URL: 'http://boostmysale.s3.amazonaws.com/Lifco/lifco/',
    apiPort:8062,
    elasticURL: 'http://navsoft.co.in:9200/',
    //elasticURL: 'http://192.168.0.65:9200/',
    
    // BASE_Frontend_URL: 'http://navsoft.co.in:55/',
    BASE_Frontend_URL: 'http://192.168.0.228:55/',
});

@Injectable()
export class Global {
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    private frontUrl = GlobalVariable.BASE_Frontend_URL;
    constructor(
        private _http: Http,
        private _cookieService: CookieService, 
        private globalService: GlobalService, 
        private _router: Router,
        public dialog: MatDialog,

    ) {}
    public post_data = {};
    private globalData = new BehaviorSubject < any > (0);
    globalDataSet = this.globalData.asObservable();
    setData(val: any) {
        this.globalData.next(val);
    }

    doGrid(data: any, page: number) {
        if (!page) {
            var url = this.baseApiUrl + 'global_list/';
        } else {
            var url = this.baseApiUrl + 'global_list/?page=' + page;
        }
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    doGridInvoice(data: any, page: number) {
        if (!page) {
            var url = this.baseApiUrl + 'invoicelist/?page=1';
        } else {
            var url = this.baseApiUrl + 'invoicelist/?page=' + page;
        }
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }
    doGridPurchase(data: any, page: number) {
        if (!page) {
            var url = this.baseApiUrl + 'purchaseorderlist/?page=1';
        } else {
            var url = this.baseApiUrl + 'purchaseorderlist/?page=' + page;
        }
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }
    
    private handleError(error: Response) {
        return observableThrowError(error || "Server err");
    }

    doStatusUpdate(model: any, bulk_ids: any, type: any) {
        var up_arr: any = [];
        bulk_ids.forEach(function(item: any) {
            var obj = {
                "id": item
            };
            up_arr.push(obj);
        });
        if (type == 2) {
            var field_name = 'isdeleted';
            var val = 'y';
        } else if (type == 1) {
            var field_name = 'isblocked';
            var val = 'y';
        } else if (type == 0) {
            var field_name = 'isblocked';
            var val = 'n';
        }
        this.post_data = {
            "table": {
                "table": model,
                "field_name": field_name,
                "value": val
            },
            "data": up_arr
        }

        return this._http.post(this.baseApiUrl + 'globalupdate/', this.post_data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }
    
    doGridFilter(model: any, isdefault: any, cols: any, screen: any) {
        if (isdefault == 1) {
            this.post_data = {
                model: model,
                is_default: isdefault,
                screen_name: screen,
                "header_name": "",
                "field_name": "",
                website_id: this.globalService.getWebsiteId(),
                company_id: this.globalService.getCompanyId()
            }
        } else {
            var header_name: any = [];
            var field_name: any = [];
            cols.forEach(function(item: any) {
                if (item.show == 1) {
                    header_name.push(item.title);
                    if (item.child != '') {
                        field_name.push(item.field + '.' + item.child);
                    } else {
                        field_name.push(item.field);
                    }
                }
            });
            var header_name = header_name.join("@@");
            var field_name = field_name.join("@@");
            this.post_data = {
                model: model,
                screen_name: screen,
                "header_name": header_name,
                "field_name": field_name,
                website_id: this.globalService.getWebsiteId(),
                company_id: this.globalService.getCompanyId()
            }
        }

        return this._http.post(this.baseApiUrl + 'global_list_filter/', this.post_data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }


    Ipaddress() {
        //return this._http.get('https://freegeoip.net/json/', {})
        return this._http.get('http://api.ipstack.com/182.71.170.222?access_key=f39f58470675618d96e26d751a2d24f0', {}).pipe(
            map(res => res.json()),
            catchError(this.handleError), );

    }

    libLoad(type: string) {

        return this._http.post(this.baseApiUrl + 'allproductcategoryimages/', {
            type: type
        }, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    globalAutocomplete(data: any) {
        var url = this.baseApiUrl + 'autocomplete/';
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    exportData(data: any, page: number) {
        if (!page) {
            var url = this.baseApiUrl + 'global_list_export/';
        } else {
            var url = this.baseApiUrl + 'global_list_export/?page=' + page;
        }

        data['website_id'] = this.globalService.getWebsiteId();
        data['company_id'] = this.globalService.getCompanyId();
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError),);
    }

    viewNotification(obj: any) {
        if (obj.action_type == 'order') {
            this._router.navigate(['/orders/view/' + obj.data.id]);
        }
    }

    getWebServiceData(action: any, method: any, data: any, id: any) {
        if (method == 'GET') {
            if (id != '') {
                return this._http.get(this.baseApiUrl + action + '/' + id+'/', this.globalService.getHttpOption()).pipe(
                    map(res => res.json()),
                    catchError(this.handleError), );
            } else {
                return this._http.get(this.baseApiUrl + action + '/', this.globalService.getHttpOption()).pipe(
                    map(res => res.json()),
                    catchError(this.handleError), );
            }
        } else if (method == 'PUT') {
            if(id > 0) {
                return this._http.put(this.baseApiUrl + action + '/' + id + '/', data, this.globalService.getHttpOptionFile()).pipe(
                    map(res => res.json()),
                    catchError(this.handleError), );
            } else {
                return this._http.put(this.baseApiUrl + action + '/' + id, data, this.globalService.getHttpOptionFile()).pipe(
                    map(res => res.json()),
                    catchError(this.handleError), );
            }
            
        } else {
            return this._http.post(this.baseApiUrl + action + '/', data, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        }
    }

    uploadFile(action: any, method: any, data: any) {
        return this._http.post(this.baseApiUrl + action + '/', data, this.globalService.getHttpOptionFile()).pipe(
            map(res => res.json()),
            catchError(this.handleError));
    }

    getTaxSettings(website_id) {
      return this._http.get(this.baseApiUrl + 'taxsettings/'+website_id+'/', this.globalService.getHttpOption()).pipe(
          map(res => res.json()),
          catchError(this.handleError),);
    }

    generateSheet(link){
        let url = this.baseApiUrl +link;
        return this._http.post(url,'', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    openEditor(page) { 
        window.open(this.frontUrl+"editor/page/"+page, "_blank");
    }

    loadColumnVisibility(data: any) {
        var url = this.baseApiUrl + 'grid_layout/';
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError));
    }
    
    reset_dialog(){
        this.dialog.afterOpen.subscribe(() => {
            let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
            containerElem.classList.remove('pop-box-up');
        });
    }
}