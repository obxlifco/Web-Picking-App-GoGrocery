import { throwError as observableThrowError,  Observable } from 'rxjs';
import { catchError, map} from 'rxjs/operators'; 
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import { Injectable} from '@angular/core'; 
import { BehaviorSubject } from 'rxjs';
import { CookieService} from 'ngx-cookie';
import { GlobalService } from './app.global.service';
import {GlobalVariable} from './global';
import { Router } from '@angular/router';
import * as FormData from 'form-data';

@Injectable({
  providedIn: 'root'
})
export class CategoryService {

  readonly apiBaseUrl = GlobalVariable.BASE_API_URL;
  private _websiteId;
  private _warehouseId;

  constructor(private _gs:GlobalService,
  	          private _http: Http, 
        	  private _cookieService:CookieService
            ) {
  	this._websiteId = this._gs.getFrontedWebsiteId();
    this._warehouseId = this._gs.getWareHouseId();

   }
  /**
   * Method for getting all parent category list
   * @access public
   * @return CategoryDetails
   */
   getParentCategoryList() {
   	let headers = new Headers({
   		'WID' : this._websiteId,
     });
   	let options = new RequestOptions({headers:headers});
   	return this._http.post(this.apiBaseUrl+'parent-category-list/',{},options).pipe(map(res =>  res.json()), 
       catchError(this._handleError))

   }
   /**
    * Method for getting shop by category
    * @access public
   */
   getShopByCategoryData() {
     let headers = new Headers({
       'WID' : this._websiteId,
     });
     let options = new RequestOptions({headers:headers});
     return this._http.get(this.apiBaseUrl+'shop_by_category/',options).pipe(map(res =>  res.json()),catchError(this._handleError));

   }
   getShopByCategoryDataByCategoryId(categoryId = [], warehouseIdShopByCategory:any) {
     console.log("************* Category ids **********");
     console.log(categoryId);
     let categoryData:FormData = new FormData();
     categoryData.append('website_id',this._websiteId);
     categoryId.forEach(singleCategoryData => {

       categoryData.append('category_ids[]',singleCategoryData);

     });
     categoryData.append('warehouse_id',warehouseIdShopByCategory);
     console.log(categoryData)
     return this._http.post(this.apiBaseUrl+'shop_by_categoryids/',categoryData).pipe(map(res => res.json()),catchError(this._handleError));

     
   }
   /**
    * Method for getting product by parent category id
    * @param categoryId
    * @access public
    * @return categoryList
   */
   getProductByCategoryId(categoryId,warehouseId) {
     let categoryData:FormData = new FormData();
     categoryData.append('warehouse_id',warehouseId);
     categoryData.append('website_id',this._websiteId);
     categoryData.append('category_id',categoryId);
     return this._http.post(this.apiBaseUrl+'product-list/',categoryData).pipe(map(res => res.json()),catchError(this._handleError));
   }
   /**
    * Method for getting category banner data
    * @return categoryBannerData
   */
   getCategoryBannerList() {
     let categoryBannerData:FormData = new FormData();
     categoryBannerData.append('website_id',this._websiteId);
     categoryBannerData.append('applicable_for','web');
     categoryBannerData.append('banner_type','C');
     return this._http.post(this.apiBaseUrl+'category_banner_for_home/',categoryBannerData).pipe(map(res => res.json()),catchError(this._handleError));
   }
   /**
    * Method for getting promotion banner list
    * @access public
   */
   getPromotionsBanner() {
     let headers = new Headers({
        'WID': this._websiteId
      });
      let options = new RequestOptions({ headers: headers });
    
     return this._http.get(this.apiBaseUrl+'promotional-banner-list/',options).pipe(map(res => res.json()),catchError(this._handleError));

   }
   /**
    * Method for getting banner details by banner id and banner type
    * @access public

   */
   public  getCategoryBannerByBannerId(bannerId = [],bannerType = '',warehouse_id) {
     let warehouse_ids:number  
     warehouse_ids = warehouse_id
     let bannerData = new FormData();
     bannerData.append('banner_type',bannerType);
     bannerData.append('applicable_for','category');
     bannerData.append('website_id',this._websiteId);
     bannerData.append('warehouse_id',warehouse_ids);
     bannerId.forEach(singleBannerId => {
       bannerData.append('category_banner_id[]',singleBannerId);

     });
     return this._http.post(this.apiBaseUrl+'banner_list/',bannerData).pipe(map(res => res.json()),catchError(this._handleError));
     

   }
   /**
    * Method for getting banner details by banner id and banner type
    * @access public

   */
   public  getPromotionalBannerByBannerId(bannerId = [],bannerType = '') {
     let bannerData = new FormData();
     bannerData.append('banner_type',bannerType);
     bannerData.append('website_id',this._websiteId);
     bannerId.forEach(singleBannerId => {
       bannerData.append('banner_ids[]',singleBannerId);

     });
     return this._http.post(this.apiBaseUrl+'promotional-banner/',bannerData).pipe(map(res => res.json()),catchError(this._handleError));
     

   }

   /**
    * Method for getting brand list data
    * @access public
    * @param brandId List
   */
   getBrandListByBrandId(brandListId = []) {
     let brandData = new FormData();
     brandData.append('website_id',this._websiteId);
     brandListId.forEach(singleBrandId => {
       brandData.append('brand_ids[]',singleBrandId);
     });
     return this._http.post(this.apiBaseUrl+'brand_list_by_brandid/',brandData).pipe(map(res => res.json()),catchError(this._handleError)); 
   }
   getBrands() {
    return this._http.post(this.apiBaseUrl+'brand_list/',{}).pipe(
       map(res =>  res.json()),
       catchError(this._handleError));

    }
   /**
    * Method for handaling error
    * @access private
   */
   private _handleError(error: Response) { 
        return Observable.throw(error || "Server err");  

    }
}
