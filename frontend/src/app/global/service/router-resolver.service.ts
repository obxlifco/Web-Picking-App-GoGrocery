import { Injectable } from '@angular/core';
import { Resolve, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Http } from '@angular/http';
import { Observable } from 'rxjs';
import { catchError, map} from 'rxjs/operators'; 
import { GlobalService } from './app.global.service';
import { Global,GlobalVariable } from "./global";


@Injectable({ providedIn: 'root' })
export class HomeRouterResolverService implements Resolve<any> {
    listingType:string = 'Category';
    detailsData = {};
    currentSlug = '';
    currentUrl = [];
    readonly apiBaseUrl = GlobalVariable.BASE_API_URL;
    constructor(
        private http: Http,
        private _globalService: GlobalService,
        private _global: Global
        ) { }   

    resolve(activatedRouteSnapshot: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
        this.currentSlug = activatedRouteSnapshot.params['slug'];
        this.currentUrl = state.url.split('/');
        if(this.currentUrl.length > 1) {
            if (this.currentUrl[1] == 'listing') {
                this.setSeoData('category');
            } else if (this.currentUrl[1] == 'details') {
                this.setSeoData('product');
            }
        }
        
        return true;
    }

    /**
     * Method for set Seo Data
     */
    setSeoData(type) {
        let curl = window.location.href;
        this.fetchMetaDetailsBySlug(type).subscribe(response => {
            if (response && response['status'] == 1) {
                this.detailsData = response['data'];
                let seoData: any = {};
                seoData['metatitle'] = (this.detailsData["meta_title"]) ? this.detailsData['meta_title'] : this.detailsData["name"] + ' : ' + GlobalVariable.APPLICATION_NAME;
                seoData['title'] = this.detailsData["name"] + ' : ' + GlobalVariable.APPLICATION_NAME;
                seoData['description'] = (this.detailsData['meta_description']) ?  this.detailsData['meta_description'] : seoData['title'];
                seoData['keywords'] = (this.detailsData['meta_keywords']) ?  this.detailsData['meta_keywords'] : seoData['title'];	
                seoData['curl'] = curl;				
                this.setMetaData(seoData);
            } 
        });
    }

    /**
     * Method for Set Meta Data
     * @param seoData 
     */
    setMetaData(seoData) {
        this._globalService.setAdMetaData(seoData); 
        return true;
    }

    /**
     * Method for fetching meta details by slug
     * @param type 
     */
    fetchMetaDetailsBySlug(type) {
        let curl = window.location.href;
        let requestObject = {};
        requestObject['slug'] = this.currentSlug;
        requestObject['type'] = type;

        return this.http.post(this.apiBaseUrl + 'get_slug/', requestObject).pipe(map(res =>  res.json()),catchError(err => this.handleError));
    }

    /**
   * Method for  handaling error
  */
   private handleError(err) { 
    return Observable.throw(err);
   }
}