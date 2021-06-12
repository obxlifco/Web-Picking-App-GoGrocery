import { throwError as observableThrowError,  Observable } from 'rxjs';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import { Injectable} from '@angular/core'; 
import { CookieService} from 'ngx-cookie';
import { GlobalVariable } from './global';
import { GlobalService } from './app.global.service';

@Injectable()
export class ProfileService {
	private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(
      private _http: Http,
      private globalService:GlobalService
    ) { }

    getWishlistProducts(data:any){
      return this._http.post(this.baseApiUrl+'wishlistdetails/', data,this.globalService.getHttpOptionClient()).pipe(
           map(res =>  res.json()),
           catchError(this.handleError));
    }

    getProductReviews(data:any){
      return this._http.post(this.baseApiUrl+'reviewdetails/', data,this.globalService.getHttpOptionClient()).pipe(
           map(res =>  res.json()),
           catchError(this.handleError));
    }

    removeWishlist(data:any){
      return this._http.post(this.baseApiUrl+'remove_wishlist/', data,this.globalService.getHttpOptionClient()).pipe(
           map(res =>  res.json()),
           catchError(this.handleError));
    }  

    getOrders(data:any){
      return this._http.post(this.baseApiUrl+'myorderdetails/', data,this.globalService.getHttpOptionClient()).pipe(
           map(res =>  res.json()),
           catchError(this.handleError));
    } 

    getOrderDetails(data:any){
      return this._http.post(this.baseApiUrl+'orderdetails/', data,this.globalService.getHttpOptionClient()).pipe(
           map(res =>  res.json()),
           catchError(this.handleError));
    }

    updatePassword(data: any, id:any){
        return this._http.put(this.baseApiUrl+'users_changepass/'+id+'/', data, this.globalService.getHttpOptionClient()).pipe(
          map(res =>  res.json()),
          catchError(this.handleError));
    }    

    getUserInfo(id:number){
      return this._http.get(this.baseApiUrl+'customerinfo/'+id+'/', this.globalService.getHttpOptionClient()).pipe(
          map(res =>  res.json()),
          catchError(this.handleError));
    }  

    updateProfileInfo(data:any, id:number){
        return this._http.put(this.baseApiUrl+'customerinfo/'+id+'/', data, this.globalService.getHttpOptionClient()).pipe(
          map(res =>  res.json()),
          catchError(this.handleError));
    }

    orderTrackInfo(data:any){
        return this._http.post(this.baseApiUrl+'shipment_wise_order_data/', data, this.globalService.getHttpOptionClient()).pipe(
          map(res =>  res.json()),
          catchError(this.handleError));
    }

    returnProductRequest(data:any){
        return this._http.post(this.baseApiUrl+'order_item_return_popup/', data, this.globalService.getHttpOptionClient()).pipe(
          map(res =>  res.json()),
          catchError(this.handleError));
    }  

    ticketCreate(data:any){
        return this._http.post(this.baseApiUrl+'create_ticket/', data, this.globalService.getHttpOptionClient()).pipe(
          map(res =>  res.json()),
          catchError(this.handleError));
    }   

    postComment(data:any){
        return this._http.post(this.baseApiUrl+'ticket_comment_save/', data, this.globalService.getHttpOptionClient()).pipe(
          map(res =>  res.json()),
          catchError(this.handleError));
    }  

    getTickets(data:any){
      return this._http.post(this.baseApiUrl+'frontend_ticket_listing/', data,this.globalService.getHttpOptionClient()).pipe(
           map(res =>  res.json()),
           catchError(this.handleError));
    }

    getTicketDetails(data:any){
      return this._http.post(this.baseApiUrl+'frontend_ticket_view/', data,this.globalService.getHttpOptionClient()).pipe(
           map(res =>  res.json()),
           catchError(this.handleError));
    }

    getNotifyPaymentOrders(data:any){
      return this._http.post(this.baseApiUrl+'fetch_unpaid_order/', data,this.globalService.getHttpOptionClient()).pipe(
      map(res =>  res.json()),
      catchError(this.handleError));
    }

    saveNotifyPayments(data:any){
      return this._http.post(this.baseApiUrl+'save_payment_notification/', data,this.globalService.getHttpOptionClient()).pipe(
      map(res =>  res.json()),
      catchError(this.handleError));
    }

    private handleError(error: Response) { 
      return Observable.throw(error || "Server err"); 
   	}
}	