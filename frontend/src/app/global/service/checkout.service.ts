import { Injectable } from '@angular/core';
import { throwError as observableThrowError,  Observable, BehaviorSubject} from 'rxjs';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {MatSnackBar} from '@angular/material';
import {GlobalService} from './app.global.service';
import {GlobalVariable} from './global';
import { CookieService} from 'ngx-cookie';
import { DatePipe } from '@angular/common';
@Injectable({
  providedIn: 'root'
})
export class CheckoutService {

   private _authorizationToken;
 // private _authorizationToken = 'Token 1a3384885ac0bf69f02c93138c6c891512db750d';
  readonly apiBaseUrl = GlobalVariable.BASE_API_URL;
  constructor( 
    private _http:Http,
    private _globalService:GlobalService,
    private _cookieService:CookieService,
    private datePipe: DatePipe,
  ) {
    //this._authorizationToken = = 'Token '+this._globalService.getCurrentUserToken();
  }
  /**
   * Method for getting all delivery address
   * @access public
  */

  getAllDeliveryAddress() {
 
    let requestOption = this._globalService.getHttpOptionFrontendUsers();
  	return this._http.get(this.apiBaseUrl+'delivery-address/',requestOption).pipe(
           map(res =>  res.json()),
           catchError(err => this._globalService.handleError(err)));
  }
  // getAllDeliveryAddress() {

  // }

  /**
    * Method for getting country list
    * @access public
   */
   getCountryList() {
     let countryData = {};
     return this._http.post(this.apiBaseUrl+'countries-list/',countryData).pipe(
        map(res =>  res ? res.json():''),
        catchError(err => this._globalService.handleError));
   }
   /**
    * Method for getting state list
    * @access public
   */
   getStateListByCountryId(countryId) {
     let stateData = new FormData();
     stateData.append('country_id',countryId);
     return this._http.post(this.apiBaseUrl+'states-list/',stateData).pipe(
           map(res =>  res.json()),
           catchError(err => this._globalService.handleError(err)));

     
   }
   /**
    * Add new delivery address
    * @access public
   */
   addNewDeliveryAddress(deliveryAddressData = {}) {
    /* let headersData = {
      'Content-Type' : 'application/json',
      'Authorization' : this._authorizationToken
    }
    const headers = new Headers(headersData);
    let requestOptions = new RequestOptions({ headers: headers });*/
    let requestOptions = this._globalService.getHttpOptionFrontendUsers();

    let addedDeliveryAddressData:Object = {
      'name' : deliveryAddressData['name'],
      // 'last_name' : deliveryAddressData['last_name'],
      'address' : deliveryAddressData['apartment_name'],
      // 'landmark' : deliveryAddressData['nearest_landmark'],
      'country' : 221,
      'state' : deliveryAddressData['state'] ? deliveryAddressData['state'] : '',
      'area' : deliveryAddressData['area'],
      // 'city' : deliveryAddressData['city'],
      // 'pincode' : deliveryAddressData['pincode'],
      'mobile_no' : deliveryAddressData['mobile_no'],
      // 'alternative_mobile_no' : deliveryAddressData['alternative_mobile_no'],

      'check' : deliveryAddressData['is_default'] ? 1 : 0

     }
     return this._http.post(this.apiBaseUrl+'delivery-address/',addedDeliveryAddressData,requestOptions).pipe(
           map(res =>  res.json()),
           catchError(err => this._globalService.handleError(err)));

   }


   EditDeliveryAddress(deliveryAddressData = {},id) {
    /* let headersData = {
      'Content-Type' : 'application/json',
      'Authorization' : this._authorizationToken
    }
    const headers = new Headers(headersData);
    let requestOptions = new RequestOptions({ headers: headers });*/
    let requestOptions = this._globalService.getHttpOptionFrontendUsers();

    let addedDeliveryAddressData:Object = {
      'name' : deliveryAddressData['name'],
      // 'last_name' : deliveryAddressData['last_name'],
      'address' : deliveryAddressData['apartment_name'],
      // 'landmark' : deliveryAddressData['nearest_landmark'],
      'country' : 221,
      'state' : deliveryAddressData['state'] ? deliveryAddressData['state'] : '',
      'area' : deliveryAddressData['area'],
      // 'city' : deliveryAddressData['city'],
      // 'pincode' : deliveryAddressData['pincode'],
      'mobile_no' : deliveryAddressData['mobile_no'],
      'customers_addressId' : id,

      // 'alternative_mobile_no' : deliveryAddressData['alternative_mobile_no'],

      'check' : deliveryAddressData['is_default'] ? 1 : 0
      
     }
     console.log(addedDeliveryAddressData);
     return this._http.put(this.apiBaseUrl+'delivery-address/',addedDeliveryAddressData,requestOptions).pipe(
           map(res =>  res.json()),
           catchError(err => this._globalService.handleError(err)));

   }


  removeDeliveryAddress(addressId) {
    let requestOptions = this._globalService.getHttpOptionFrontendUsers();
    return this._http.get(this.apiBaseUrl+'delete-address/'+addressId+'/',requestOptions).pipe(
           map(res =>  res.json()),
           catchError(err => this._globalService.handleError(err)));
    

  }
  /**
   * Method on for valicate promocode
   * @access public
  */
  applyPromoCode(couponData = {}) {
    let requestOptions = this._globalService.getHttpOptionFrontendUsers();
   /* let couponData = {
      'coupon_code' : promocode
    }*/
    return this._http.post(this.apiBaseUrl+'apply-coupon/',couponData,requestOptions).pipe(
      map(res =>  res.json()),
      catchError(err => this._globalService.handleError(err)));
  }

   private handleError(error: Response) { 
      return Observable.throw(error || "Server err"); 
   }
   /**
    * Method on store discount code
    * @access public
   */
   storeCouponCode(coupon_code:string = '') {
     if(coupon_code != '') {
       this._cookieService.put('coupon_code', coupon_code);
     }
   }
   /**
    * Method of getting all delivery address
    * @access public
   */
   getAllDeliverySlot(){
     let wareHouseId = this._globalService.getWareHouseId();
     let headersData = this._globalService.getHttpOptionFrontendUser();
     // console.log("***************** Headers data **************");
     // console.log(headersData);
     return this._http.get(this.apiBaseUrl+'delivery-slot/'+wareHouseId+'/',headersData).pipe(
           map(res =>  res.json()),
           catchError(err => this._globalService.handleError(err)));
   }
   /**
    * Method on place order
    * @access public
   */
   placeOrder(orderData) {
     /*let userData = localStorage.getItem('currentUser');
     userData     = JSON.parse(userData);*/
     let wareHouseId = this._globalService.getWareHouseId();
     let headersData = this._globalService.getHttpOptionFrontendUser();
     let websiteId = 1;
     orderData['website_id'] = websiteId;
     orderData['device_id'] = this._globalService.getGlobalDataByKey('requested_ip');
     orderData['warehouse_id'] = this._globalService.getWareHouseId();
     orderData['redeem_amount'] = orderData['redeem_amount'] ? orderData['redeem_amount'] : 0;
    /* let coupon_code = '';
     if(this._cookieService.get('coupon_code')) {
        coupon_code = this._cookieService.get('coupon_code');
     }*/
     //orderData['coupon_code'] = coupon_code;
    
    //  return this._http.post(this.apiBaseUrl+'save-cart/',orderData,headersData).pipe(map(res =>  res.json()),catchError(err => this._globalService.handleError(err)));
     return this._http.post(this.apiBaseUrl+'save-cart-si/',orderData,headersData).pipe(map(res =>  res.json()),catchError(err => this._globalService.handleError(err)));
   }
   /**
    * Metod for getting checkout summary
    * @access public
   */
   getCheckoutSummary(checkoutObject) {
     let headersData = this._globalService.getHttpOptionFrontendUser();
     return this._http.post(this.apiBaseUrl+'cart-summary/',checkoutObject,headersData).pipe(
              map(res => res.json()),
              catchError(err => this._globalService.handleError(err))
            )
   }
   /**
    * Method for getting loyalty point
    * @access public
   */
   getLoyaltyPoint(orderId) {

     let headersData = this._globalService.getHttpOptionFrontendUser();
     let loyaltyData = {
       "order_id" : orderId
     }
     return this._http.post(this.apiBaseUrl+'check-balance/',loyaltyData,headersData).pipe(
              map(res => res.json()),
              catchError(err => this._globalService.handleError(err))
            )


   }
   /**
    * Method for doint card payment
    * @access public
   */
   doCardPayment(cardData) {
     let headerData = this._globalService.getHttpOptionFrontendUser();
     return this._http.post(this.apiBaseUrl+'payment/',cardData,headerData).pipe(
              map(res => res.json()),
              catchError(err => this._globalService.handleError(err))
            )
   }
   /**
    * Method for ccavenue payment
    * @access public
   */
   doCcAvenuePayment(paymentData) {
     let headerData = this._globalService.getHttpOptionFrontendUser();
     return this._http.post(this.apiBaseUrl+'payment-request/',paymentData,headerData).pipe(
              map(res => res.json()),
              catchError(err => this._globalService.handleError(err))
            );
   
   }

   do_CcAvenue_Payment(paymentData) {
    let headerData = this._globalService.getHttpOptionFrontendUser();
    return this._http.post(this.apiBaseUrl+'payment-request-si-si/',paymentData,headerData).pipe(
             map(res => res.json()),
             catchError(err => this._globalService.handleError(err))
           );
  
  }

    /**
    * Method for ccavenue payment
    * @access public
   */
   chekAddressRange(address) {
     let headerData = this._globalService.getHttpOptionFrontendUser();
     return this._http.post(this.apiBaseUrl+'select-address/',address,headerData).pipe(
              map(res => res.json()),
              catchError(err => this._globalService.handleError(err))
            );
   
   }

   convertDate(date: any, format: any= '') {
    return this.datePipe.transform(date, format); // format will need to implement from global settings
  }

  getPaymentMethod() {
    let headerDataLoad = this._globalService.getHttpOptionFrontendUser();
    console.log(headerDataLoad)
    let wareHouseId = this._globalService.getWareHouseId();
    headerDataLoad['WAREHOUSE'] = wareHouseId;
    return this._http.get(this.apiBaseUrl+'payment-method/',headerDataLoad).pipe(
      map(res =>  res.json()),
      catchError(err => this._globalService.handleError(err))
      );
  }
  
}
