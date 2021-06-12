import { throwError as observableThrowError,  Observable } from 'rxjs';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import { Injectable} from '@angular/core'; 
import { GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';

@Injectable()
export class ReturnService {
	private baseApiUrl = GlobalVariable.BASE_API_URL;
	private elasticUrl = GlobalVariable.elasticURL;
	public post_data = {};
	constructor( 
		private _http: Http,
		private globalService: GlobalService,
		private _cookieService: CookieService
	) {
	}
	
	private handleError(error: Response) {
		return observableThrowError(error || "Server err");
	}

	// order_item_return_listing
	doGridOrderReturnRequest(data:any,page:number) {
		var url = '';
		url=this.baseApiUrl+'global_list/';
		if(!page){
		} else {
			url=url+'?page='+page;
		}
		return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError)); 
	}

	getOrderActivity(id:number) {
		let website_id:number = this.globalService.getWebsiteId();
		return this._http.get(this.baseApiUrl+'get-order-activity/'+id+'/'+website_id+'/',this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	returnProductRequest(data:any){
        return this._http.post(this.baseApiUrl+'order_item_return_popup/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
    } 

	
	returnRequestProcess(data:any) {
		return this._http.post(this.baseApiUrl+'order_item_status_change/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	viewOrderReturn(data:any){
		return this._http.post(this.baseApiUrl+'view_order_return/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	saveReturn(data:any){
		return this._http.post(this.baseApiUrl+'order_return_complete/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	
	postComments(data:any){
		return this._http.post(this.baseApiUrl+'timeline/', data,this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}
}