import {throwError as observableThrowError,  Observable } from 'rxjs';
import {catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { Injectable } from '@angular/core';
import {GlobalVariable}from '../../global/service/global';
import {   GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';

@Injectable()
export class BasicSetupService {
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(private _http: Http, private globalService: GlobalService, private _cookieService: CookieService) {}
    settingsLoad(id: number) {
        if (id > 0) {
            return this._http.get(this.baseApiUrl + 'basicsettings/' + id + '/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError),);
        } else {}
    }
    getIndustriesList() {
        return this._http.get(this.baseApiUrl + 'basicsettings_load/', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError),);
    }
    settingsAddEdit(data: any, id: any) {
        let userData = this._cookieService.getObject('userData');
        let headers = new Headers({
            'Authorization': 'Token ' + userData['auth_token']
        });
        let options = new RequestOptions({
            headers: headers
        });
        if (id > 0) {
            return this._http.put(this.baseApiUrl + 'basicsettings/' + id + '/', data, options).pipe(
                map(res => res.json()),
                catchError(this.handleError),);
        } else {
            return this._http.post(this.baseApiUrl + 'basicsettings/', data, options).pipe(
                map(res => res.json()),
                catchError(this.handleError),);
        }
    }
    templatesLoad(id: number) {
        if (id > 0) {
            return this._http.get(this.baseApiUrl + 'templatesedit/' + id + '/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError),);
        } else {}
    }
    templatesEdit(data: any, id: number) {
        if (id > 0) {
            return this._http.put(this.baseApiUrl + 'templatesedit/' + id + '/', data, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError),);
        }
    }
    paymentLoad(id: number) {
        return this._http.get(this.baseApiUrl + 'paymentsetup/' + id + '/', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError),);
    }
    paymentSave(data: any, id: number) {
        if (id > 0) {
            return this._http.put(this.baseApiUrl + 'paymentsetup/' + id + '/', data, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError),);
        }
    }
    taxLoad(id: number) {
        if (id > 0) {
            return this._http.get(this.baseApiUrl + 'basictaxsettings/' + id + '/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError),);
        } else {}
    }
    saveTax(data: any, id: any) {
        if (id > 0) {
            return this._http.put(this.baseApiUrl + 'basictaxsettings/' + id + '/', data, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError),);
        }
    }
    shippingLoad(id: number, shipping_master_type_id: number) {
        if (id > 0) {
            return this._http.get(this.baseApiUrl + 'shippinglist/' + shipping_master_type_id + '/Shipping/0/' + id + '/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError),);
        } else {}
    }
    shipAddEdit(data: any, id: number) {
        if (id > 0) {
            return this._http.put(this.baseApiUrl + 'shippinglistgetupdate/' + id + '/', data, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError),);
        } else {
            return this._http.post(this.baseApiUrl + 'shippingsetup/', data, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError),);
        }
    }
    getStates(data: any) {
        return this._http.post(this.baseApiUrl + 'countriesstate/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError),);
    }
    loadCountry() {
        return this._http.get(this.baseApiUrl + 'countrylist/', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError),);
    }

    loadStateEdit(country_id, shipping_method_id: any,editId:any) {
        if (shipping_method_id > 0) {
            return this._http.get(this.baseApiUrl + 'countrystatelist/' + country_id + '/?shipping_method_id=' + shipping_method_id+"&editId="+editId, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError));
        }
    }

    loadStates(country_id, shipping_method_id:any) {
        if (shipping_method_id > 0) {
            return this._http.get(this.baseApiUrl + 'countrystatelist/' + country_id + '/?shipping_method_id=' + shipping_method_id, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError));
        } else {
            return this._http.get(this.baseApiUrl + 'countrystatelist/' + country_id + '/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError));
        }
    }
    imageDelete(data: any) {
        return this._http.post(this.baseApiUrl + 'store_image_delete/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError),);
    }
    private handleError(error: Response) {
        return observableThrowError(error || "Server err");
    }
    loadChannelSettings(channel_id: number, website_id: number) { // Loading market place channel settings 
        if (channel_id > 0) {
            return this._http.get(this.baseApiUrl + 'amazoncredential/' + website_id + '/' + channel_id + '/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError),);
        }
    }
    channelSetupList(website_id: number) {
        if (website_id > 0) {
            return this._http.get(this.baseApiUrl + 'channellistview/' + website_id + '/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError),);
        }
    }
    activateChannel(data) {
        if (data.website_id > 0) {
            return this._http.post(this.baseApiUrl + 'activedeactivechannel/', data, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError),);
        }
    }
    saveMarketplaceSettings(data: any, id: number) {
        let webservice_action = 'saveFlipkartSettings/';
        if (id == 20) {
            let webservice_action = 'flipkartcredentialsave/';
        } else if (id == 21) {
            let webservice_action = 'snapcredentialsave/';
        } else if (id == 23) {
            let webservice_action = 'savePaytmSettings/';
        } else if (id == 17 || id == 18 || id == 19) {
            let webservice_action = 'amazoncredentialsave/';
        } else if (id == 11 || id == 12 || id == 13 || id == 14) { // this is the Ebay Settings
            let webservice_action = 'ebaycredentialsave/';
        }
        if (id > 0) { // Setting Flipkart data 
            return this._http.post(this.baseApiUrl + webservice_action, data, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError),);
        }
    }
    get_country_state(id: any) {
        return this._http.get(this.baseApiUrl + 'statelist/' + id + '/', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError),);
    }
    saveFlatRateData(data: any) {
        return this._http.post(this.baseApiUrl + 'shippingsetuptablerate/', data, this.globalService.getHttpOptionFile()).pipe(
            map(res => res.json()),
            catchError(this.handleError),);
    }
    saveCODZipcodes(data: any) {
        return this._http.post(this.baseApiUrl + 'shippingsetupcod/', data, this.globalService.getHttpOptionFile()).pipe(
            map(res => res.json()),
            catchError(this.handleError),);
    }
    loadShippingSettings(shipping_method_id: number) {
        return this._http.get(this.baseApiUrl + 'shippinglist/' + shipping_method_id + '/Courier/0/0/', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError),);
    }
    saveShippingSettingsData(data: any) {
        return this._http.post(this.baseApiUrl + "shippingsetup/", data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError),);
    }

    checksettings(website_id,shipping_method_id) {
        return this._http.get(this.baseApiUrl + 'shippingmethodstatus/' + shipping_method_id + '/' + website_id+'/', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError));
    }
}