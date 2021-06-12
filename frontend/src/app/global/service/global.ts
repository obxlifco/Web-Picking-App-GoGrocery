/*import { throwError as observableThrowError,Observable } from 'rxjs';*/
import { Observable,throwError} from 'rxjs'
import { catchError, map} from 'rxjs/operators'; 
import { Http, Response, Headers, RequestOptions,} from '@angular/http';
import { HttpParams } from '@angular/common/http';
import { Injectable} from '@angular/core'; 
import { BehaviorSubject } from 'rxjs';
import { CookieService} from 'ngx-cookie';
import { GlobalService } from './app.global.service';
import { Router } from '@angular/router';
// import { Subject }    from 'rxjs/Subject';
export const GlobalVariable = Object.freeze({

    
    
     BASE_API_URL: 'https://www.gogrocery.ae/api/front/v1/',

    //BASE_API_URL: 'http://192.168.0.205:8062/api/front/v1/',

     BASE_BACKEND_API_URL: 'https://www.gogrocery.ae/api/',
    //BASE_BACKEND_API_URL : 'http://192.168.0.205:8062/api/',

    //BASE_API_URL: 'http://192.168.0.205:8062/api/front/v1/',
    
    COMPANY_URL: 'https://www.gogrocery.ae/',
    // COMPANY_URL:'http://localhost/',

    BASE_URL:'https://www.gogrocery.ae/',
    // BASE_URL:'http://localhost:55/',
    
    GOOGLE_CLIENT_ID: '74854632065-86uci4hndsgo2eljc8nh45uh2ol2qgtg.apps.googleusercontent.com',
    FACEBOOK_APP_ID: '199136490666622', //LIVE
    // FACEBOOK_APP_ID: '2077610695813299', //LOCAL
    S3_URL: 'https://d1fw2ui0wj5vn1.cloudfront.net/Lifco/lifco/',
    BASE_CDN_URL: 'https://d1fw2ui0wj5vn1.cloudfront.net/Lifco/lifco/',
   
    // BASE_Backend_URL: 'https://app.localhost:73',
    BASE_Backend_URL:'http://gogrocery.ae:81/',

    //elasticUrl:'http://192.168.0.65:9200/',
    //elasticUrl:'http://gogrocery.ae:9200/',
    elasticUrl:'https://www.gogrocery.ae/elastic/', 

    DEFAULT_WAREHOUSE_DATA : {
      'selected_warehouse_id' : 34,
      'selected_warehouse_name' : 'LIFCO SUPERMARKET – SHARJAH'
    },
    CARRIER_CODE : [50,52,54,55,56,58],
    COUNTRY_CODE : '971',
    APPLICATION_NAME : 'GoGrocery : UAE'
});

@Injectable({
    providedIn:'root'
})
export class Global {    
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    private baseBackendUrl = GlobalVariable.BASE_BACKEND_API_URL;
    private elasticUrl=GlobalVariable.elasticUrl;
    constructor(
        private _http: Http, 
        private _cookieService:CookieService,
        private globalService:GlobalService,
        private _router: Router
    ) {}
    public post_data = {};

    doGrid(data:any,page:number) {
       if(!page){var url=this.baseApiUrl+'global_list/';}
       else{var url=this.baseApiUrl+'global_list/?page='+page;}
       return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
       map(res =>  res.json()), 
       catchError(err => this.handleError(err))); 
    } 
    
    handleError(res: Response) { 
     let response = res ? res.json() : 'Server error';
     
     return throwError(response); 
    }

    doStatusUpdate(model:any,bulk_ids:any,type:any) {   
        var up_arr:any=[];
        bulk_ids.forEach(function(item:any){
          var obj={"id":item};
          up_arr.push(obj);
        }); 
        if(type==2){var field_name='isdeleted';var val='y';}
        else if(type==1){var field_name='isblocked';var val='y';}
        else if(type==0){var field_name='isblocked';var val='n';}
        this.post_data={"table":{"table":model,"field_name":field_name,"value":val},"data":up_arr, "website_id": this.globalService.getFrontedWebsiteId()}

        return this._http.post(this.baseApiUrl+'globalupdate/', this.post_data, this.globalService.getHttpOption()).pipe(
        map(res =>  res.json()),
        catchError(err => this.handleError(err))); 
    }

    doGridFilter(model:any,isdefault:any,cols:any,screen:any) {
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
       catchError(err => this.handleError(err)));
    }
    
    
    Ipaddress(){
        return this._http.get('https://api.ipstack.com/check?access_key=7b28c3b0e02bd812c01dcd6125459760', {}).pipe(
        map(res =>  res.json()),
        catchError(err => this.handleError(err)));
        
    }

    libLoad(type: string) {
      return this._http.post(this.baseApiUrl+'allproductcategoryimages/',{type: type}, this.globalService.getHttpOption()).pipe(
      map(res =>  res.json()),
      catchError(err => this.handleError(err)));
    }

    globalAutocomplete(data:any) {
        var url=this.baseApiUrl+'autocomplete-frontend/';
        return this._http.post(url, data).pipe(map(res =>  res.json()),catchError(err => this.handleError(err))); 
    }

    exportData(data:any, page:number){
      if(!page) {
          var url=this.baseApiUrl+'global_list_export/';
      } else{
          var url=this.baseApiUrl+'global_list_export/?page='+page;
      }
      return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
       map(res =>  res.json()),
       catchError(err => this.handleError(err))); 
    }

    getFontAwsomes(){
      return this._http.get('https://d2vltvjwlghbux.cloudfront.net/frontend/assets/font-awsome.json').pipe(map(res =>  res.json()),catchError(err => this.handleError(err)));
    }

    globalData() { 
      let store_name:any;
      let dstore: any = '';
      store_name = '1';
      //console.log(store_name);
      return this._http.get(this.baseApiUrl+'basic-info-page-load/'+store_name+'/').pipe(
          map(res =>  res.json()),
          catchError(err => this.handleError(err)));
    }

    getHeaderMenus() {
        return this._http.get(this.baseApiUrl+'all_menu/0/'+this.globalService.getFrontedWebsiteId()+'/').pipe(
            map(res =>  res.json()),
            catchError(err => this.handleError(err)));
    }   

    getFooterMenus() {
        return this._http.get(this.baseApiUrl+'all_menu/1/'+this.globalService.getFrontedWebsiteId()+'/').pipe(
            map(res =>  res.json()),
            catchError(err => this.handleError(err)));
    }    

    uploadCroppedImage(data:any){
      let userData = this._cookieService.getObject('userData');
      let headers = new Headers({
        'Authorization': 'Token '+userData['auth_token']
      });
      let options = new RequestOptions({ headers: headers });
      //return this._http.post(this.baseApiUrl+'temp_image_load/',data,options);

      return this._http.post(this.baseBackendUrl+'temp_image_load/', data, options).pipe(
        map(res =>  res.json()),
        catchError(err => this.handleError(err)));
    }   
    
    getFeaturedProducts() {
        return this._http.get(this.baseApiUrl+'featuredproductlist/'+this.globalService.getFrontedWebsiteId()+'/').pipe(
           map(res =>  res.json()),
           catchError(err => this.handleError(err)));
    }
    
    getCategories() {
        return this._http.post(this.baseApiUrl+'category_list/',{}).pipe(
           map(res =>  res.json()),
           catchError(err => this.handleError(err)));

    }
    
    getBrands() {
        return this._http.post(this.baseApiUrl+'brand_list/',{}).pipe(
           map(res =>  res.json()),
           catchError(err => this.handleError(err)));

    }
    getParentCategories(data:any) {
        return this._http.post(this.baseApiUrl+'parent_category_list/',data).pipe(
           map(res =>  res.json()),
           catchError(err => this.handleError(err)));

    }
    getNewProducts() {
        return this._http.get(this.baseApiUrl+'new_product/'+this.globalService.getFrontedWebsiteId()+'/').pipe(map(res =>  res.json()),catchError(err => this.handleError(err)));      
    }

    getBestSaleProducts() {
      return this._http.get(this.baseApiUrl+'best_sale_product/'+this.globalService.getFrontedWebsiteId()+'/').pipe(map(res =>  res.json()),catchError(err => this.handleError(err)));      
    }
   

    doStatusUpdateWebsite(model:any,bulk_ids:any,type:any) {   
        var up_arr:any=[];
        bulk_ids.forEach(function(item:any){
          var obj={"id":item};
          up_arr.push(obj);
        }); 
        if(type==2){var field_name='isdeleted';var val='y';}
        else if(type==1){var field_name='isblocked';var val='y';}
        else if(type==0){var field_name='isblocked';var val='n';}
        this.post_data={"table":{"table":model,"field_name":field_name,"value":val},"data":up_arr,"website_id": this.globalService.getFrontedWebsiteId()}
        return this._http.post(this.baseApiUrl+'globalupdate/', this.post_data, this.globalService.getHttpOptionClient()).pipe(
          map(res =>  res.json()),
          catchError(err => this.handleError(err)));
    }

    doSearch(data:any) {
        // data = {"key":data,"website_id": this.globalService.getFrontedWebsiteId() }
        // return this._http.post(this.baseApiUrl+'esmenufrontend/', data).pipe(map(res =>  res.json()),catchError(this.handleError));  
        let  url = this.elasticUrl+this.globalService.getWebsiteName()+'1_product_'+this.globalService.getWebsiteId()+'/data/_search';
        return this._http.post(url,data, this.globalService.getFrontedWebsiteId().toString()).pipe(
             map(res => res.json()),
             catchError(err => this.handleError(err)), );
    }

     doSearchServer(data:any) {
        // data = {"key":data,"website_id": this.globalService.getFrontedWebsiteId() }
        // return this._http.post(this.baseApiUrl+'esmenufrontend/', data).pipe(map(res =>  res.json()),catchError(this.handleError));  
        let  url = this.elasticUrl+this.globalService.getWebsiteName()+'1_product_'+this.globalService.getWebsiteId()+'/data/_search';

        let payload :any = {}
         payload.table_name = "EngageboostProducts";
         payload.website_id = 1;
         payload.data = data;

        return this._http.post(this.baseBackendUrl+'search_elastic/',payload, this.globalService.getFrontedWebsiteId().toString()).pipe(
             map(res => res.json()),
             catchError(err => this.handleError(err)), );
    }


    updateSubscribe(data:any){
        return this._http.post(this.baseApiUrl+'unsrbscribe/', data).pipe(map(res =>  res.json()),catchError(err => this.handleError(err)));
    }

    updateClick(data:any){
        return this._http.post(this.baseApiUrl+'clicked/', data).pipe(map(res =>  res.json()),catchError(err => this.handleError(err)));
    }  

    funnelTrack(data:any){
        return this._http.post(this.baseApiUrl+'add-tracking-data/', data).pipe(map(res =>  res.json()),catchError(err => this.handleError(err)));
    } 

    cmsFormSubmit(data:any){
        return this._http.post(GlobalVariable.BASE_API_URL+'cms_form_data/', data).pipe(map(res =>  res.json()),catchError(err => this.handleError(err))); 
    } 

    signupOtpCheck(data:any){
        return this._http.post(this.baseApiUrl+'verify_otp/', data).pipe(map(res =>  res.json()),catchError(err => this.handleError(err)));
    }

    signupOtpResend(data:any) {
        return this._http.post(this.baseApiUrl+'resend_otp/', data).pipe(map(res =>  res.json()),catchError(err => this.handleError(err)));
    }

    // public crc_code:any;
    // public qrcode = new Subject<string>();
    // qrcode$ = this.qrcode.asObservable();
    // generateQrCode(amount:any, order_no:any){
    //     let clientData: any = this._cookieService.getObject('clientData'); 
    //     let tag00 = '000201';
    //     let tag01 = '010212';
    //     let ord_no = order_no;
    //     let ord_length = parseInt(ord_no.length) >=10 ? ord_no.length : '0'+ord_no.length;
    //     let name = clientData.first_name+clientData.last_name;
    //     let name_length = parseInt(''+name.length) >=10 ? name.length : '0'+name.length;
    //     let name_val = parseInt(''+name.length) >20 ? name.substring(0,19).toUpperCase() : name.toUpperCase();
    //     let temp_tag30 = '0016A000000677010112011501055611522020102'+ord_length+ord_no+'03'+name_length+name_val;
    //     let tag30 = '30'+temp_tag30.length+temp_tag30;
    //     let amt = ''+parseFloat(amount).toFixed(2);
    //     let amt_length = parseInt(''+amt.length) >=10 ? amt.length : '0'+amt.length;
    //     let tag53 = '5303764';
    //     let tag54 = '54'+amt_length+parseFloat(amount).toFixed(2);
    //     let tag58 = '5802TH';
    //     let tag59 = '5908BARAWKAT';
    //     let tag63 = '6304';
    //     let qrcode_temp = tag00+tag01+tag30+tag53+tag54+tag58+tag59+tag63;
    //     this.getQrHexCode(qrcode_temp).subscribe(
    //       checkdata => { 
    //           if(checkdata.status==1){
    //             this.crc_code = checkdata.hex_data;
    //             //this.qrcode = qrcode_temp+this.crc_code; console.log('QR: '+this.qrcode);
    //             this.qrcode.next(qrcode_temp+this.crc_code); console.log('QR: '+this.qrcode);
    //            }
    //        },
    //     );
    //     return this.qrcode;
    // }
    
    getQrHexCode(code:string){
        let data: any = { requested_str: code };
        return this._http.post(this.baseApiUrl+'crc_generation/',data, this.globalService.getHttpOptionClient()).pipe(map(res =>  res.json()),catchError(err => this.handleError(err)));
    }

    countFollowers(data:any) {
        return this._http.post(this.baseApiUrl+'follow_count/', data).pipe(map(res =>  res.json()),catchError(err => this.handleError(err)));
    }

    public updateFollowers(data:any){
        return this._http.post(this.baseApiUrl+'follow_request/', data, this.globalService.getHttpOptionClient()).pipe(map(res =>  res.json()),catchError(err => this.handleError(err)));
    }
    
    newletter_mail(data:any) {
        return this._http.post(this.baseApiUrl+'news_letter_subscribe/',data).pipe(map(res =>  res.json()),catchError(err => this.handleError(err)));
    }

    agentRegister(data:any){
        return this._http.post(this.baseApiUrl+'create-agent-frontend/', data, {}).pipe(map(res =>  res.json()),catchError(err => this.handleError(err)));
    }
    getHeaderData(){
        return this._http.get(this.baseApiUrl+'common/category-tree/'+this.globalService.getFrontedWebsiteId()+'/').pipe(map(res =>  res.json()),catchError(err => this.handleError(err)));      
    }

  getListingData( advancedSearch) {
		let url = GlobalVariable.elasticUrl+this.globalService.getWebsiteName()+'1_product_'+this.globalService.getWebsiteId()+'/data/_search'
		return this._http.post(url, advancedSearch,this.globalService.getHttpOptionNotLogin()).pipe(
			map(res => res.json()),
			catchError(err => this.handleError(err)));
	}

   getListingDataServer( advancedSearch) {
     let payload :any = {}
     payload.table_name = "EngageboostProducts";
     payload.website_id = 1;
     payload.data = advancedSearch;
    let url = GlobalVariable.elasticUrl+this.globalService.getWebsiteName()+'1_product_'+this.globalService.getWebsiteId()+'/data/_search'
    return this._http.post(this.baseBackendUrl+'search_elastic/', payload,this.globalService.getHttpOptionFrontendUser()).pipe(
      map(res => res.json()),
      catchError(err => this.handleError(err)));
  }
  
  getMenuListingpageSidebar(slug,type) {
       const params = new HttpParams()
           .set('slug', slug)
           .set('type', type)
           .set('warehouse_id', this.globalService.getWareHouseId().toString())
           .set('website_id', this.globalService.getFrontedWebsiteId().toString());
       return this._http.get(this.baseApiUrl + 'listing_filters/?' + params.toString()).pipe(
           map(res => res.json()),
           catchError(err => this.handleError(err)));
   }

   getCateoryBannerWithSorting(slug,type='category') {
       const params = new HttpParams()
           .set('slug', slug)
           .set('type',type)
           .set('warehouse_id', this.globalService.getWareHouseId().toString())
           .set('website_id', this.globalService.getFrontedWebsiteId().toString());
           // console.log(this.baseApiUrl + 'category_banner/?' + params.toString())
       return this._http.get(this.baseApiUrl + 'category_banner/?' + params.toString()).pipe(
           map(res => res.json()),
           catchError(err => this.handleError(err)));
    }
    
    //GLOBAL GET - POST 
    getWebServiceData(action: any, method: any, data: any, id: any,queryParams?:string) {
      if (method == 'GET') {
        if (id != '') {
            //queryParams = queryParams ?  queryParams : '';

            return this._http.get(this.baseApiUrl + action + '/' + id+'/',this.globalService.getHttpOptionFrontendUser()).pipe(
                map(res => res.json()),
                catchError(err => this.handleError(err)), );
        } else {
            let url = this.baseApiUrl + action + '/';
            //queryParams ?  url+'/'+queryParams
            if(queryParams) {
              url = url+queryParams;
            }
            return this._http.get(url,this.globalService.getHttpOptionFrontendUser()).pipe(
                map(res => res.json()),
                catchError(err => this.handleError(err)), );
        }
      } else if (method == 'PUT') {
        if(id > 0) {
            return this._http.put(this.baseApiUrl + action + '/' + id + '/', data, this.globalService.getHttpOptionFrontendUser()).pipe(
                map(res => res.json()),
                catchError(err => this.handleError(err)), );
        } else {
            return this._http.put(this.baseApiUrl + action + '/' + id, data, this.globalService.getHttpOptionFrontendUser()).pipe(
                map(res => res.json()),
                catchError(err => this.handleError(err)), );
        }
      } else {
        return this._http.post(this.baseApiUrl + action + '/', data, this.globalService.getHttpOptionFrontendUser()).pipe(
          map(res => res.json()),
          catchError(err => this.handleError(err)), );
      }
    }

    getWishList(action: any, method: any, data: any, id: any) {
        if (method == 'GET') {
            if (id != '') {
                return this._http.get(this.baseApiUrl + action + '/' + id+'/',this.globalService.getHttpOptionFrontendUserByWarehouse()).pipe(
                    map(res => res.json()),
                    catchError(err => this.handleError(err)), );
            } else {
                return this._http.get(this.baseApiUrl + action + '/',this.globalService.getHttpOptionFrontendUserByWarehouse()).pipe(
                    map(res => res.json()),
                    catchError(err => this.handleError(err)), );
            }
        } 
    }
}