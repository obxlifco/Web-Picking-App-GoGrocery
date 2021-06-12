import {throwError as observableThrowError,  Observable } from 'rxjs';
import {catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {Injectable} from '@angular/core'; 
import {GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';

@Injectable()
export class PurchaseOrderService {
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    constructor(
        private _http: Http,
        private globalService: GlobalService
    ) {

    }
    // View Purchase order....
    purchaseOrderView(id: number) {
        return this._http.get(this.baseApiUrl + 'purchaseorderview/' + id + '/', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    purchaseOrderLoad(id: number) {
        if (id > 0) {
            return this._http.get(this.baseApiUrl + 'purchaseorderviewlist/' + id + '/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        } else {
            return this._http.get(this.baseApiUrl + 'supplierslist/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        }
    }

    getProducts(id: number, data: any, product_spec: string) {
        if (id > 0 && product_spec == 'exclusive') {
            data['supplier_id'] = id;
            return this._http.post(this.baseApiUrl + 'suppliersproducts/', data, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        } else {
            return this._http.post(this.baseApiUrl + 'productload/', data, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        }
    }

    poAddEdit(data: any, id: number) {
        if (id > 0) {
            return this._http.put(this.baseApiUrl + 'purchaseorderviewlist/' + id + '/', data, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        } else {
            return this._http.post(this.baseApiUrl + 'purchaseorder/', data, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        }
    }

    doGrid(data: any, page: number) {
        if (!page) {
            var url = this.baseApiUrl + 'purchaseorderlist/';
        } else {
            var url = this.baseApiUrl + 'purchaseorderlist/?page=' + page;
        }
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    changePoStatus(data: any) {
        return this._http.post(this.baseApiUrl + 'purchaseordersstatuschange/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    getSupplierEmail(id: number) {
        let data: any = {};
        data['id'] = id;
        return this._http.post(this.baseApiUrl + 'suppliersemail/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    getPoReceived(id: number) {
        let data: any = {};
        data['purchase_order_id'] = id;
        return this._http.post(this.baseApiUrl + 'poreceivedget/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    finishGRN(data: any) {
        return this._http.post(this.baseApiUrl + 'add_received_product_details/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    poGrnEdit(data: any) {
        return this._http.post(this.baseApiUrl + 'grnsend/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    private handleError(error: Response) {
        return observableThrowError(error || "Server err");
    }

    scanItemDetails(id: number) {
        return this._http.get(this.baseApiUrl + 'purchaseorderviewlist/' + id + '/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
    }

    getProductFromEan(data:any) {
        return this._http.post(this.baseApiUrl + 'geteanProduct/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }
}