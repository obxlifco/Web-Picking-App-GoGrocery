import { throwError as observableThrowError,  Observable } from 'rxjs';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import { Injectable} from '@angular/core'; 
import { GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService} from 'ngx-cookie';

@Injectable()
export class ProductService {
    private baseApiUrl = GlobalVariable.BASE_API_URL;
    private elasticUrl  = GlobalVariable.elasticURL;
    constructor(private _http: Http, private globalService: GlobalService, private _cookieService: CookieService) {}
    public post_data = {};
    doGrid(data: any, page: number) {
        if (!page) {
            var url = this.baseApiUrl + 'productlist/';
        } else {
            var url = this.baseApiUrl + 'productlist/?page=' + page;
        }
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    loadColumnVisibility(data: any) {
        var url = this.baseApiUrl + 'grid_layout/';
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    loadGrid(moduleName: any, page: number, keywords: any, pageSize: number, sortFields: any, show_variant_product, sortOrder, advancedSearch, websiteId) {
        let from = 0;
        if(page <= 0) {
            page = 1;
            from = 0;
        } else {
            let start = page -1 ;
            from = start*pageSize;
            from = from-1;
        }
        if(sortFields == '') {
            sortFields = 'id';
        }
        let orderType = 'asc';
        if(sortOrder == '+') {
            orderType = 'asc'
        } else {
            orderType = 'desc'
        }
        let userData = this._cookieService.getObject('userData');
        if (userData["elastic_store_name"] != "") {
            userData["elastic_url"] = userData["elastic_url"] + userData["elastic_store_name"]+"_";
        }
        let url = userData["elastic_url"] + 'product_' + websiteId + '/data/_search';
        //url = this.elasticUrl + 'product_'+websiteId+'/data/_search'

        let payload :any = {}
         payload.table_name = "EngageboostProducts";
         payload.website_id = 1;
         payload.data = advancedSearch;

        return this._http.post(this.baseApiUrl + 'search_elastic/', payload, this.globalService.getHttpOptionNotLogin()).pipe(
        map(res => res.json()),
        catchError(this.handleError), );

        // return this._http.post(url, advancedSearch, this.globalService.getHttpOptionNotLogin()).pipe(
        // map(res => res.json()),
        // catchError(this.handleError), );
    }

    loadHsnCodeMaster() {
        return this._http.get(this.baseApiUrl + 'hsncode_list/', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError));
    }

    doStatusUpdate(model: any, bulk_ids: any, type: any) {
        var up_arr: any = [];
        bulk_ids.forEach(function(item: any) {
            var obj = {
                "id": item
            };
            up_arr.push(obj);
        });
        if (type == 2) {
            var field_name = 'isdeleted';
            var val = 'y';
        } else if (type == 1) {
            var field_name = 'isblocked';
            var val = 'y';
        } else if (type == 0) {
            var field_name = 'isblocked';
            var val = 'n';
        }
        this.post_data = {
            "table": {
                "table": model,
                "field_name": field_name,
                "value": val
            },
            "data": up_arr
        }

        return this._http.post(this.baseApiUrl + 'globalupdate/', this.post_data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }
    doGridFilter(model: any, isdefault: any, cols: any, screen: any) {
        if (isdefault == 1) {
            this.post_data = {
                model: model,
                is_default: isdefault,
                screen_name: screen,
                "header_name": "",
                "field_name": ""
            }
        } else {
            var header_name: any = [];
            var field_name: any = [];
            cols.forEach(function(item: any) {
                if (item.show == 1) {
                    header_name.push(item.title);
                    if (item.child != '') {
                        field_name.push(item.field + '.' + item.child);
                    } else {
                        field_name.push(item.field);
                    }
                }
            });
            var header_name = header_name.join("@@");
            var field_name = field_name.join("@@");
            this.post_data = {
                model: model,
                screen_name: screen,
                "header_name": header_name,
                "field_name": field_name
            }
        }
        return this._http.post(this.baseApiUrl + 'global_list_filter/', this.post_data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }
    productBasicInfoLoad() {
        return this._http.get(this.baseApiUrl + 'basicinfo_load/', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }
    productBasicInfoEdit(id: any) {
        return this._http.get(this.baseApiUrl + 'basicinfo/' + id + '/', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    basicInfoAddEdit(data: any, id: any) {
        this.globalService.showLoaderSpinner(true);
        let userData = this._cookieService.getObject('userData');
        let headers = new Headers({
            'Authorization': 'Token ' + userData['auth_token']
        });
        let options = new RequestOptions({
            headers: headers
        });
        if (id > 0) {
            return this._http.put(this.baseApiUrl + 'basicinfo/' + id + '/', data, options).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        } else {
            return this._http.post(this.baseApiUrl + 'basicinfo/', data, options).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        }

    }
    getChildCategory(parent_id: number, id: number, lvl: number) {

        if (parent_id > 0) {

            return this._http.post(this.baseApiUrl + 'getchild/', {
                "category_id": parent_id,
                "id": id,
                "lvl": lvl
            }, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        }


    }
    productAdvanceInfoLoad(id: any, channel: any) {
        return this._http.get(this.baseApiUrl + 'advanceinfo/' + id + '/' + channel + '/', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }
    productAdvanceInfoAddEdit(data: any) {
        return this._http.post(this.baseApiUrl + 'advanceinfo/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }
    productDefaultPriceLoad(id: any) {
        return this._http.get(this.baseApiUrl + 'productpriceSet/' + id + '/1/', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }
    defaultPriceAddEdit(request_data: any, id: any) {
        return this._http.put(this.baseApiUrl + 'productpriceSet/' + id + '/1/', request_data, this.globalService.getHttpOptionFile()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }
    deleteVariant(id: any) {
        return this._http.delete(this.baseApiUrl + 'productpriceSet/' + id + '/1/', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }
    doGridRelated(data: any, page: number) {

        if (!page) {
            var url = this.baseApiUrl + 'relatedproduct_list/';
        } else {
            var url = this.baseApiUrl + 'relatedproduct_list/?page=' + page;
        }
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    doRelatedProduct(id: any, type: any) {
        return this._http.get(this.baseApiUrl + 'relatedproduct/' + id + '/' + type + '/', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    doRelatedProductAddEdit(data: any) {
        return this._http.post(this.baseApiUrl + 'relatedproduct/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    productImageDelete(data: any) {
        return this._http.post(this.baseApiUrl + 'product_image_delete/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    setCoverImage(data: any) {
        return this._http.post(this.baseApiUrl + 'set_cover_image/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }


    private handleError(error: Response) {
        return observableThrowError(error || "Server err");
    }

    loadProductDetails(id: number) {
        if (id > 0) {
            return this._http.get(this.baseApiUrl + 'product_details/' + id + '/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        }
    }
    
    loadOrderProductGrid(data: any, page: number, product_id: number) {
        if (!page) {
            var url = this.baseApiUrl + 'stocklist/';
        } else {
            var url = this.baseApiUrl + 'stocklist/' + '/?page=' + page;
        }
        if(data) {
            return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
        } else {
            return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
        }
    }
    
    import_file_data(data: any,importType:any) {
        if(importType == 'Related') { 
            return this._http.post(this.baseApiUrl + 'import_file_related_products/', data, this.globalService.getHttpOptionFile()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
        } else { // Product Import
            return this._http.post(this.baseApiUrl + 'import_file_products/', data, this.globalService.getHttpOptionFile()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
        }
    }

    save_file_data(data: any,importType:any) {
        if(importType == 'Related') {
            return this._http.post(this.baseApiUrl + 'save_file_related_data/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
        } else {
            return this._http.post(this.baseApiUrl + 'save_file_data/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
        }
    }

    load_preview_grid(data: any, page: number,importType:any) {
        let preview_save_data = 'preview_save_data'; // this is for product preview..
        if(importType == 'Related') {
            preview_save_data = 'preview_save_related_data';
        } else {
            preview_save_data = 'preview_save_data';
        }
        if (!page) {
            var url = this.baseApiUrl + preview_save_data+'/';
        } else {
            var url = this.baseApiUrl + preview_save_data+'/?page=' + page;
        }
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    get_child_category(data: any) {
        return this._http.post(this.baseApiUrl + 'get_child_category/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    show_all_imported_data(data: any,importType:any) {
        var url = this.baseApiUrl + 'show_all_imported_data/';
        if(importType == 'Related') {
            var url = this.baseApiUrl + 'save_all_imported_related_data/';
        } else {
            var url = this.baseApiUrl + 'show_all_imported_data/';
        }
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    generateProductSheet(module_name: string) {
        var url = this.baseApiUrl + 'export_product/1/';
        return this._http.get(url, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    //CREADIT EARN CONDITIONS ADD EDIT PAGE STRAT
    conditionLoad(id: number) {
        if (id > 0) {
            return this._http.get(this.baseApiUrl + 'discountconditions/' + id, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        }
    }

    conditionAddEdit(data: any, id: any) {
            return this._http.post(this.baseApiUrl + 'discountconditions/', data, this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        }
        //CREADIT EARN CONDITIONS ADD EDIT PAGE END
    allCategoryLoad() {
        return this._http.get(this.baseApiUrl + 'catrgoryconditionsset/', this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    categoryLoad(id: number) {
        if (id > 0) {
            return this._http.get(this.baseApiUrl + 'categorieslistdiscount/' + id + '/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        } else {
            return this._http.get(this.baseApiUrl + 'category_load/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        }
    }

    productLoad(data) {
        return this._http.post(this.baseApiUrl + 'productload/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    customerGroupLoad(data) {
        return this._http.post(this.baseApiUrl + 'customertype/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );

    }

    customerLoad(data) {
        return this._http.post(this.baseApiUrl + 'discountcustomer/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    savePointsFileData(data: any) {
        return this._http.post(this.baseApiUrl + 'savehsncode/', data, this.globalService.getHttpOptionFile()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }
    //WARE HOUSE LIST FOLLOWD BY SUPPLIERS
    wareHousList(data) {
        return this._http.post(this.baseApiUrl + 'warehousesuppliermaplist/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    supplierList(data:any,page:number){
        if (!page) {
            var url = this.baseApiUrl + 'global_list/';
        } else {
            var url = this.baseApiUrl + 'global_list/?page=' + page;
        }
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }


    deletePrice(data:any) {
        return this._http.post(this.baseApiUrl + 'channelcurrencypricedelete/', data,this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError));
    }

    doGridVariant(id: any, search: any) {
        return this._http.get(this.baseApiUrl + 'variableproduct/' + id+ '/?q='+ search, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),catchError(this.handleError), );
    }

    saveVariantProduct(data) {
        return this._http.post(this.baseApiUrl + 'variableproduct/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    productLoadPaging(data, page: number) {
        if (!page) {
            var url = this.baseApiUrl + 'productload-paging/';
        } else {
            var url = this.baseApiUrl + 'productload-paging/?page=' + page;
        }
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    //GET PROMOTION LIST BY PRODUCT ID
    getPromotionList(id:number){
        if (id) {
            return this._http.get(this.baseApiUrl + 'get_promotions_by_id/' + id + '/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        }
    }
    //GET  TOP CUSTOMERS BY PRODUCT ID
    getTopCustomers(id:number){
        if (id) {
            return this._http.get(this.baseApiUrl + 'get_top_customers_by_id/' + id + '/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        }
    }
    //GET  TOP SUPPLIERS BY PRODUCT ID
    getSuppliers(id:number){
        if (id) {
            return this._http.get(this.baseApiUrl + 'get_suppliers_by_id/' + id + '/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        }
    }
    //GET ACTIVITY FEED BY PRODUCT ID
    getFeeds(id:number){
        if (id) {
            return this._http.get(this.baseApiUrl + 'get_product_activity_by_id/' + id + '/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        }
    }

    getAllCounters(id:number){
        if (id) {
            return this._http.get(this.baseApiUrl + 'get_all_counters/' + id + '/', this.globalService.getHttpOption()).pipe(
                map(res => res.json()),
                catchError(this.handleError), );
        }
    }

    //PRODUCT PRICE IMPORT START
    import_product_price(data: any) {
        return this._http.post(this.baseApiUrl + 'import_price/', data, this.globalService.getHttpOptionFile()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }


    
    
    addEditCategoryBanner(data: any,formId:any) {
        if(formId > 0) {
            return this._http.put(this.baseApiUrl + 'categorybanner/'+formId+'/', data, this.globalService.getHttpOptionFile()).pipe(
                map(res => res.json()),
                catchError(this.handleError));
        } else {
            return this._http.post(this.baseApiUrl + 'categorybanner/', data, this.globalService.getHttpOptionFile()).pipe(
                map(res => res.json()),
                catchError(this.handleError));
        }
        
    }

    save_product_price(data: any) {
        return this._http.post(this.baseApiUrl + 'save_file_price/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    load_product_price_preview_grid(data: any, page: number) {
        //console.log(data);
        if (!page) {
            var url = this.baseApiUrl + 'preview_save_price/';
        } else {
            var url = this.baseApiUrl + 'preview_save_price/?page=' + page;
        }
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }

    show_all_product_price_imported(data: any) {
        var url = this.baseApiUrl + 'save_all_imported_price/';
        return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError), );
    }
    //PRODUCT PRICE IMPORT ENAD

    getProductsES(advancedSearch, websiteId) {
        let userData = this._cookieService.getObject('userData');
        if (userData["elastic_store_name"] != "") {
            userData["elastic_url"] = userData["elastic_url"] + userData["elastic_store_name"] + "_";
        }
        let url = userData["elastic_url"] + 'product_' + websiteId + '/data/_search';
        //let url = this.elasticUrl + 'product_' + websiteId + '/data/_search'
        return this._http.post(url, advancedSearch, this.globalService.getHttpOptionNotLogin()).pipe(
            map(res => res.json()),
            catchError(this.handleError));
    }
    

    categoryBannerDelete(data: any) {
        return this._http.post(this.baseApiUrl + 'categorybanner_image_delete/', data, this.globalService.getHttpOption()).pipe(
            map(res => res.json()),
            catchError(this.handleError));
    }


    //SERVICE FOR PRODUCT DETAILS START
    graphLoad(data_id:number,graph_for:any,data:any){
        if(graph_for=='sales'){

            // return this._http.post(this.baseApiUrl + 'sales-graph/', data, this.globalService.getHttpOption2()).pipe(map(res => res.json()),catchError(this.handleError),);
            return this._http.post(this.baseApiUrl + 'product-view-sales-graph/', data, this.globalService.getHttpOption2()).pipe(map(res => res.json()),catchError(this.handleError),);
        }
        if(graph_for=='stock'){

            return this._http.post(this.baseApiUrl + 'product-view-stock/', data, this.globalService.getHttpOption2()).pipe(map(res => res.json()),catchError(this.handleError),);
        }
        if(graph_for=='visitor'){

            return this._http.post(this.baseApiUrl + 'product-view-visitors/',data, this.globalService.getHttpOption2()).pipe(map(res => res.json()),catchError(this.handleError),);
        }
    }
    //SERCVICE FOR PRODUCT DETAILS END

    warehouseLoad(websiteId,userId){
        return this._http.get(this.baseApiUrl + 'warehousestockmanagement/' + websiteId + '/' + userId+'/', this.globalService.getHttpOption()).pipe(
                 map(res =>  res.json()),
                 catchError(this.handleError),);
        }
}