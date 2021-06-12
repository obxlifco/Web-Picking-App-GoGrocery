import { Injectable, Inject,PLATFORM_ID} from '@angular/core';
import { Observable,throwError} from 'rxjs'; 
import {map,catchError} from 'rxjs/operators';
import { Subject }    from 'rxjs';
import { Router } from '@angular/router';
import { CookieService} from 'ngx-cookie';
import { Http, Headers,RequestOptions} from '@angular/http';
import {HttpClient} from '@angular/common/http';
import { MatSnackBar} from '@angular/material';
import { DecimalPipe, DatePipe } from '@angular/common';
import { ProductDetailSnakbarComponent } from '../../ui/snackbar/app.snackbar.component';
import { WINDOW,LOCAL_STORAGE} from '@ng-toolkit/universal';
import {GlobalVariable} from './global';
import { Meta, Title } from '@angular/platform-browser';
declare let fbq:Function;
declare let gtag:Function;


@Injectable()
export class GlobalService {
    // Observable

    readonly apiBaseUrl = GlobalVariable.BASE_API_URL;
    private profileNameSource = new Subject<string>();
    public imageArraySource = new Subject<any>();
    public libArraySource = new Subject<any>();
    private loadSpinnerSource = new Subject<boolean>();

    public isLoginSource = new Subject<boolean>();
    public globalDataSource = new Subject<boolean>();
    public paypalBtnSource = new Subject<boolean>();
    public langChangeSource = new Subject<any>();
    // folow and unfollow
    public isFollowSource = new Subject<any>();
    

    // Observable number streams
    profileNameChange$ = this.profileNameSource.asObservable();
    imageArrayChange$ = this.imageArraySource.asObservable();
    libArrayChange$ = this.libArraySource.asObservable();
    loadSpinnerChange$ = this.loadSpinnerSource.asObservable();

    isLoginChange$ = this.isLoginSource.asObservable();
    globalDataChange$ = this.globalDataSource.asObservable();
    paypalBtnChange$ = this.paypalBtnSource.asObservable();
    langChange$ = this.langChangeSource.asObservable();
    // folow and unfollow
    followChange$ = this.isFollowSource.asObservable();

    constructor(@Inject(WINDOW) private window: Window, 
      private _router: Router, 
      private _cookieService:CookieService,
      private snackBar: MatSnackBar,
      private decimalPipe: DecimalPipe,
      private http:HttpClient,
      private _http: Http,
      private datePipe: DatePipe,
       @Inject(LOCAL_STORAGE) private localStorage: any,
       public metaService:Meta,
       public titleService:Title,
       @Inject(PLATFORM_ID) private platformId: Object
    ) {
    }

    getUserId(){
      var userData = this._cookieService.getObject('userData');
      var user_id = 0;
      if(userData && userData.hasOwnProperty('uid')){
        user_id = userData['uid'];
      }
      return user_id;
    }

    getCompanyId(){
      var userData = this._cookieService.getObject('userData');
      var company_id = 0;
      if(userData && userData.hasOwnProperty('company_id')){
        company_id = userData['company_id'];
      }  
      return company_id;
    } 

    getWebsiteId() { 
      var globalData = this._cookieService.getObject('globalData');
      var website_id = 0;
      if(globalData && globalData.hasOwnProperty('website_id')){
        website_id = globalData['website_id'];
      }
      return website_id;
    }  

    getFrontedWebsiteId(){
      var globalData = this._cookieService.getObject('globalData');
      var website_id = 0;
      if(globalData && globalData.hasOwnProperty('website_id')){
        website_id = globalData['website_id'];
      }
      return website_id;
    } 

    getWebsiteName(){
      var globalData = this._cookieService.getObject('globalData');
      var  websitename = '';
      if(globalData && globalData.hasOwnProperty('websitename')){
        websitename = globalData['websitename'];
      }
      return websitename;
     
    }

    getFrontedCompanyId(){
        var globalData = this._cookieService.getObject('globalData');
        var company_id = 0;
        if(globalData && globalData.hasOwnProperty('company_id')){
          company_id = globalData['company_id'];
        }
        return company_id;
    }  

    getFrontedCompanyName(){
        var globalData = this._cookieService.getObject('globalData');
        let company_name:string = '';
        if(globalData && globalData.hasOwnProperty('company_name') && globalData['company_name']!=null) {
            company_name = globalData['company_name'];
        } else {
            company_name = 'Grocery';
        }
        return company_name;
    }          

    getClientId(){
      var userData = this._cookieService.getObject('clientData');
      var user_id = 0;
      if(userData && userData.hasOwnProperty('uid')){
        user_id = userData['uid'];
      }
      return user_id;
    }
     handleError(res: Response) {

     let response = res ? res.json() : {'message' : 'something went wrong'};
     return throwError(response); 
    }

    getCustomerId(){
      var userData = this._cookieService.getObject('clientData');
      var user_id = 0;
      if(userData && userData.hasOwnProperty('customer_id')){
        user_id = userData['customer_id'];
      }
      return user_id;
    }    

    getGoogleClientId(){
      var userData = this._cookieService.getObject('globalData');
      var auth_id = '';
      if(userData && userData.hasOwnProperty('google_login_client_id')){
        auth_id = userData['google_login_client_id'];
      }
      return auth_id;
    }

    getFBAppId(){
      var userData = this._cookieService.getObject('globalData');
      var auth_id = '';
      if(userData && userData.hasOwnProperty('fb_login_id')){
        auth_id = userData['fb_login_id'];
      }
      return auth_id;
    }

    getGlobalDataByKey(key:string) {
      var globalData = this._cookieService.getObject('globalData');
      var value = '';
      if(globalData && globalData.hasOwnProperty(key)){
        value = globalData[key];
      }
      return value; 
    }
    getRequestedIpFromCookie() {
      // let cookieData = this._cookieService.get('client_ip');
      // return cookieData;
      let localData = localStorage.getItem('client_ip').toString();
      return localData;
    }

    updateUserCookie(data: any) {
      var cookie_data: any = {};
      cookie_data = this._cookieService.getObject('userData');
      if(cookie_data){
         cookie_data.first_name = data.first_name;
         cookie_data.last_name = data.last_name;
         cookie_data.email = data.email;
         this._cookieService.putObject('userData', cookie_data);

         this.profileNameSource.next(data.first_name);
      }
    }
    /**
     * Method for removing cookie data by key
     * @access public
     * @param key
     * @return void
    */
    removeCookieByKey(key) {
      this._cookieService.remove(key);
    }
    /**
     * Update user cookie by key and data
     * @acccess public
    */
    updateCookieByKeyAndData(data:Object = {},keyname = '') {
      let response = {};
      try {
        if(Object.keys(data).length == 0 || keyname == '') {
          throw new Error("Data or cookie key name is blank");
        }
        this._cookieService.putObject(keyname,data);
        response = {
          'status' : 200,
          'message' : 'Data successfully saved'
        }
      } catch(e) {
        response = {
          'status' : 400,
          'message' : e.message
        }

      }
      return response;
      
    }

    isLoggedIn() {
      var userData = this._cookieService.getObject('userData');
      if(userData && userData.hasOwnProperty('isLoggedIn')){
        return userData['isLoggedIn'];
      }else{
       return false;
      }
      
    }

    isLoggedInFrontend(){
      var userData = this._cookieService.getObject('clientData');
      if(userData && userData.hasOwnProperty('isLoggedIn')){
        return userData['isLoggedIn'];
      }else{
       return false;
      }
    }
    isLoggedInCustomer(){
      let userData = this.localStorage.getItem('currentUser') ? JSON.parse(localStorage.getItem('currentUser')) : '';
      if(userData && userData.hasOwnProperty('first_name')){
        console.log(userData);

        return userData;
      }else{
       return false;
      }
    }  

    getCookie(key: string){
      return this._cookieService.get(key) ? this._cookieService.get(key):'';
    }

    getDistributorType() {
      let userData = this._cookieService.getObject('clientData');
      if(userData && userData.hasOwnProperty('distributor_user_type')){
        return userData['distributor_user_type'];
      } else {
        return false;
      }
    }

    getDistributorDefaultWarehouse(){
      let userData = this._cookieService.getObject('clientData');
      if(userData && userData.hasOwnProperty('default_warehouse_type')){
        return userData['default_warehouse_type'];
      }else{
        return 'default';
      }
    }

    getDistributorMinOrder(type: string){
      let globalData = this._cookieService.getObject('globalData');
      let min_order_amount: number = 0;
      if(type==='retail'){
        min_order_amount = globalData['min_order_amount']['retailer_min_order'];
      }else if(type==='wholesale'){
        min_order_amount = globalData['min_order_amount']['wholesaler_min_order'];
      }
      return min_order_amount;
    }

    getUserType() {
      let user_type:string;
      let userData = this._cookieService.getObject('clientData');
      if(userData && userData.hasOwnProperty('user_type')){
        user_type = userData['user_type'];
      }
      return user_type;
    }

    getHttpOptionNotLogin() {
        let headers = new Headers({
            'Content-Type': 'application/json',
        });
        let options = new RequestOptions({
            headers: headers
        });
        return options;
    }

    getDistributorWarehouseType() {
      let globalData = this._cookieService.getObject('globalData');
      let warehouse_type = 'default';
      if(globalData && globalData.hasOwnProperty('warehouse_type')){
        warehouse_type = globalData['warehouse_type'];
      }
      return warehouse_type;
    }

    getHttpOption(){
       let userData = this._cookieService.getObject('userData');
       let headersData = {
         'Content-Type': 'application/json',
       }
       if(userData && userData['auth_token']) {
         headersData['Authorization'] = 'Token '+userData['auth_token'];

       }

       let headers = new Headers(headersData);
       let options = new RequestOptions({ headers: headers });
       return options;
    }
    getHttpOptionClient(){
       let userData = this._cookieService.getObject('clientData');
       let headers = new Headers({
          'Content-Type': 'application/json',
          'Authorization': 'Token '+userData['auth_token']
        });
       let options = new RequestOptions({ headers: headers });
       return options;
    }
    getCarouselBanner(applicableFor = 'mobile') {
      let websiteId = this.getWebsiteId().toString();
      let warehosuseId = this.getWareHouseId().toString();
      let carouselData = new FormData();
      carouselData.append('website_id',websiteId);
      carouselData.append('warehouse_id',warehosuseId);
      carouselData.append('applicable_for',applicableFor);
      return this.http.post(this.apiBaseUrl+'banner-list-for-home/',carouselData).pipe(
         map(res =>  res),
         catchError(err => this.handleError(err)));
    }
    
    getHttpOptionFrontendUser(){
      let headersData = {};
      headersData['Content-Type'] = 'application/json';

      if(localStorage.getItem('currentUser')) {
        let userData = JSON.parse(localStorage.getItem('currentUser'));
        headersData['Authorization'] = 'Token '+userData['token'];
      }
      
      // Warehouse Id and website Id passing in header...based data filter....
      let website_id = this.getWebsiteId();
      headersData['WID'] = website_id;

      let warehouse_id = this.getWareHouseId()
      headersData['WAREHOUSE'] = warehouse_id;
      // Warehouse Id and website Id passing in header...based data filter....

      let header = new Headers(headersData);
      let options = new RequestOptions({ headers: header });
      return options;
    }
    getHttpOptionFrontendUsers(){
      let headersData = {};
      headersData['Content-Type'] = 'application/json';

      if(localStorage.getItem('currentUser')) {
        let userData = JSON.parse(localStorage.getItem('currentUser'));
        headersData['Authorization'] = 'Token '+userData['token'];
      }
      let warehouse_id = this.getWareHouseId()
      headersData['WAREHOUSE'] = warehouse_id;
      // Warehouse Id and website Id passing in header...based data filter....

      let header = new Headers(headersData);
      let options = new RequestOptions({ headers: header });
      return options;
    }
    
    getHttpOptionFile(){
       let userData = this._cookieService.getObject('userData');
       let headers = new Headers({
          'Authorization': 'Token '+userData['auth_token']
        });
       let options = new RequestOptions({ headers: headers });
       return options;
    }
    getCurrentUserToken() {
      let currentUserAuthToken = '';
      if(localStorage.getItem('currentUser')) {
        let currentUserData = localStorage.getItem('currentUser');
        currentUserData = JSON.parse(currentUserData);
        currentUserAuthToken = currentUserData['token'];
        
      }
      return currentUserAuthToken;
    }

    showToast(msg: string){
      this.snackBar.open(msg, 'x', {
        duration: 5000,
        verticalPosition : 'top',
        panelClass: ['material_snack_bar']
      });
    } 

    showProductSnakbar(data: any){
      this.snackBar.openFromComponent(ProductDetailSnakbarComponent, {
        duration: 5000,
        data: data
      });
    }
    /**
     * Method for getting latitude and longitude
     * @access public
     * @return coordinateObject
    */
    getCurrentUserLatitudeLongitude() {
      let currentUserLocation = this._cookieService.getObject('current_user_location');
      let coordinateObject = {};
      if(currentUserLocation) {
        coordinateObject['latitude'] = currentUserLocation['latitude'] ? currentUserLocation['latitude'] : '';
        coordinateObject['longitude'] = currentUserLocation['longitude'] ? currentUserLocation['longitude'] : '';
      }
      return coordinateObject;

      /*let coordinateObject = {
        'latitude' : '22.572646',
        'longitude': '88.36389499999996',
      }
      return coordinateObject;*/
    }
    
    showLoaderSpinner(show: boolean){
      this.loadSpinnerSource.next(show);
    }

    get_order_status(code: number){
      let status:any = [
        {code:0, name:'Pending'},
        {code:100, name:'Processing'},
        {code:2, name:'Cancelled'},
        {code:3, name:'Abondoned'},
        {code:4, name:'Completed'},
        {code:1, name:'Shipped'},
        {code:5, name:'Full Refund'},
        {code:6, name:'Partial Refund'},
        {code:99, name:'Waiting for Payment'},
        {code:7, name:'Payment Confirm'},
        {code:8, name:'Shipping Approval Pending'},
        {code:999, name:'Failed'},
        {code:11, name:'Paid'},
        {code:12, name:'Pre Order'},
        {code:13, name:'Delivered'},
        {code:14, name:'Damaged'},
      ];
      let status_text:any = '';
      status.forEach(function(item:any){
        if(code==item.code){
          status_text = item.name;
        }
      });
      return status_text;
    }

    check_file_ext(type: string){

        var return_result = 0;
        switch (type) {
            case "image/png":
                return_result= 1;
                break;
            case "image/gif":
                return_result= 1;
                break;
            case "image/jpeg":
                return_result= 1;
                break;
            
            default:
                return_result= 0;
                break;
        }

        return return_result;
    }


    check_file_size(size: number){

        let return_result: boolean;
        size = (size)/(1024*1024); // in MB

        if(size>2){
            return_result = false;
        }else{
            return_result = true;
        }

        return return_result;
    }    


  calculateProductDiscount(disc_type:number,discount_amount:number,price:number){
    let discounted_price:number;
    if(disc_type==1){ //percentage discount
      discounted_price = price - (price*(discount_amount/100));
    }else if(disc_type==2){ // fixed amount discount
      discounted_price = price - discount_amount;
    }

    if(discounted_price<0)
      discounted_price = 0;

    return discounted_price;
  }


  getCurrencySymbol() {
    let currency:string = '';
    let globalData = this._cookieService.getObject('globalData');
    if(globalData && globalData.hasOwnProperty('currency_symbol')){
      currency = globalData['currency_symbol'];
    }
    return currency;
  }

  exchangeRate(price:number,price_marketplace:any=[]) {
    let exchanged_price: number;
    let globalData:any = this._cookieService.getObject('globalData');
    price_marketplace = [];
    if(price_marketplace.length>0){
      
      let selected_curr:any = price_marketplace.filter((curr) => curr.currency_id == globalData.currency_id);
      if(selected_curr.length>0){
        exchanged_price = selected_curr[0].price;
      }else{
        if(globalData && globalData.hasOwnProperty('currency_exchange')){
          exchanged_price = parseFloat((price * globalData['currency_exchange']).toFixed(2));
        }else{
          exchanged_price = price;
        }  
      }
      
    }else{
      if(globalData && globalData.hasOwnProperty('currency_exchange')){
        exchanged_price = parseFloat((price * globalData['currency_exchange']).toFixed(2));
      }else{
        exchanged_price = price;
      }  
    }
    
    return parseFloat(exchanged_price.toFixed(2));
  }

    redirectToHome() {
        if(this.getFrontedWebsiteId() > 1) {
          this._router.navigate(['/page/home']);
        } else {
          this._router.navigate(['/']);
        }
    }
 
    getCookieOption() {
        //let site_url = window.location.hostname;
        //console.log('CDS site url => '+ site_url);
        let cookieOption:any =  {
            //domain: '.navsoft.co.in',
           // domain: 'localhost',
            path: '/' 
        }
        return cookieOption;
    }

    numberFormatPipe(amount: number){
        return this.decimalPipe.transform(amount, '1.2-2');
    }
     /**
     * Method for getting warehouse id
     * @access public
    */
    getWareHouseId() {
      let warehouse_id:any;
      if(this._cookieService.getObject('current_user_location')) {
        let warehouse_data = this._cookieService.getObject('current_user_location');
        warehouse_id = warehouse_data['selected_warehouse_id'];
      } else {
        let warehouse_data = GlobalVariable.DEFAULT_WAREHOUSE_DATA;
        warehouse_id = warehouse_data['selected_warehouse_id'];
      }
      return warehouse_id;
    }

    getHttpOptionFrontendUserByWarehouse(){
      let headersData = {};
      let warehouse_id:any;
      headersData['Content-Type'] = 'application/json';
      if(this._cookieService.getObject('current_user_location')) {
        let warehouse_data = this._cookieService.getObject('current_user_location');
        warehouse_id = warehouse_data['selected_warehouse_id'];

      } else {
        let warehouse_data = GlobalVariable.DEFAULT_WAREHOUSE_DATA;
        warehouse_id = warehouse_data['selected_warehouse_id'];

      }
      let website_id = this.getWebsiteId();
      headersData['website_id'] = website_id;
      if(localStorage.getItem('currentUser')) {
        let userData = JSON.parse(localStorage.getItem('currentUser'));
        headersData['Authorization'] = 'Token '+userData['token'];
        headersData['WID'] = warehouse_id;
      }
      let header = new Headers(headersData);
      let options = new RequestOptions({ headers: header });
      return options;
    }
    getIpAddress() {
      return this.http.get<{ip:string}>('https://api6.ipify.org?format=json');
    }
    subscribeToNewsLetter(email) {
      let postData = {
        email : email,
        website_id : this.getWebsiteId()
      };
      
      return this.http.post(this.apiBaseUrl+'subscribe-newsletter/',postData).pipe(
         map(res =>  res),
         catchError(this.handleError));
    }

    contactus(data) { 
      var token:any='';
      var headers:any
      if(localStorage.getItem('currentUser')) {
        var userData = JSON.parse(localStorage.getItem('currentUser'));
        token = 'Token '+ userData['token'];
         headers = new Headers({'Authorization': token});
      }
  
      let requestOptions = new RequestOptions({ headers: headers });

      return this._http.post(this.apiBaseUrl+'customer-query/', data, requestOptions).pipe(
        map(res =>  res),
        catchError(this.handleError));
    }

    facebookPixelEventLog(event,actionName:any,params:any) {
        console.log("Facebook event logged");
        console.log(actionName);
        console.log(params);
        fbq('track', actionName, params);        
    }

    googleEventLog(event,actionName:any,params:any) {
      console.log("Google Event Log");
      console.log(params);
        gtag(event,  actionName,  {
          "items": params
        }); 
    }

    convertDate(date: any, format: any= '') {
      console.log(date)
      return this.datePipe.transform(date, format, 'UTC+4'); // format will need to implement from global settings
    }

    setAdMetaData(ad_seo_data: any) {  
	
      setTimeout(() => {      
          if(ad_seo_data.title && ad_seo_data.title != ''){
            this.titleService.setTitle(ad_seo_data.title); 
          }
          if (ad_seo_data.metatitle && ad_seo_data.metatitle != ''){
            this.metaService.updateTag({ name: 'title', content: ad_seo_data.metatitle }); 
            
          }else{
            this.metaService.updateTag({ name: 'title', content: ad_seo_data.title });
        }
        this.metaService.updateTag({ property: 'og:site_name', content: ad_seo_data.curl });
      //   this.metaService.addTag({ name: 'curl', content: ad_seo_data.curl }); 
      //   this.metaService.removeTag('description');
      //   this.metaService.addTag({ name: 'description', content: ad_seo_data.description })
        this.metaService.updateTag({name: 'description', content: ad_seo_data.description });
      //   this.metaService.updateTag({ name: 'description', content: 'this' });
          if (ad_seo_data.keywords && ad_seo_data.keywords != '') {
        // this.metaService.removeTag('keywords');
        // this.metaService.addTag({ name: 'keywords', content: ad_seo_data.keywords })
            this.metaService.updateTag({name: 'keywords', content: ad_seo_data.keywords });
        } 
        return true;                  
      }, 1000);
     
    }
 }