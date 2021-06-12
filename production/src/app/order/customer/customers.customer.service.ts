import {throwError as observableThrowError,  Observable } from 'rxjs';
import {catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 
import {CookieService} from 'ngx-cookie';
import {GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';

@Injectable()
export class CustomerService {
	private baseApiUrl = GlobalVariable.BASE_API_URL;
  constructor(private _http: Http,private globalService:GlobalService,private _cookieService:CookieService) {}
  private handleError(error: Response) { 
    return observableThrowError(error || "Server err"); 
  } 

  doGridCustomersAddEdit(data:any,page:number,steps:number) {
    var action_name = 'customer_orderlist';
    if(steps == 2) { // Order List
      action_name = 'customer_invoicelist';
    }
    if(!page){var url=this.baseApiUrl+action_name+'/';}
    else{var url=this.baseApiUrl+action_name+'/?page='+page;}
    return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
    map(res =>  res.json()),
    catchError(this.handleError),); 
  }

  loadCustomerGeneralInfo(customer_id :number) {
    if(customer_id > 0) {
      return this._http.get(this.baseApiUrl+'customer_edit/'+customer_id+'/',this.globalService.getHttpOption()).pipe(
      map(res=>res.json()),
        catchError(this.handleError),);
    }
  }

  loadAddressInfo(customer_id :number) {
    if(customer_id > 0) {
      return this._http.get(this.baseApiUrl+'get_customer_address/'+customer_id+'/',this.globalService.getHttpOption()).pipe(
      map(res=>res.json()),
        catchError(this.handleError),);
    }
  }

  saveBasicInfoCustomer(data: any, id:any) {
    let userData = this._cookieService.getObject('userData');
    let headers = new Headers({
      'Authorization': 'Token '+userData['auth_token']
    });
    let options = new RequestOptions({ headers: headers });
    if(id>0){
      return this._http.post(this.baseApiUrl+'customer_add/', data, options).pipe(
         map(res =>  res.json()),
         catchError(this.handleError),);
    }else{
      return this._http.post(this.baseApiUrl+'customer_add/', data, options).pipe(
         map(res =>  res.json()),
      catchError(this.handleError),);
    }
  }

  saveAddressInformation(data: any, id:any) {
    let userData = this._cookieService.getObject('userData');
    let headers = new Headers({
      'Authorization': 'Token '+userData['auth_token']
    });
    let options = new RequestOptions({ headers: headers });
    if(id>0) {
      return this._http.post(this.baseApiUrl+'customer_address_setup/', data, options).pipe(
         map(res =>  res.json()),
         catchError(this.handleError),);
    } else {
      return this._http.post(this.baseApiUrl+'customer_address_setup/', data, options).pipe(
         map(res =>  res.json()),
      catchError(this.handleError),);
    }
  }

  loadCountry() {
    return this._http.get(this.baseApiUrl + 'countrylist/', this.globalService.getHttpOption()).pipe(
    map(res => res.json()),
    catchError(this.handleError),);
  }

  loadStates(country_id) {
      return this._http.get(this.baseApiUrl + 'countrystatelist/' + country_id+'/', this.globalService.getHttpOption()).pipe(
          map(res => res.json()),
          catchError(this.handleError),);
  }

  loadCustomerGroup() {
     return this._http.get(this.baseApiUrl + 'customer_group_list/', this.globalService.getHttpOption()).pipe(
    map(res => res.json()),
    catchError(this.handleError),);
  }
}