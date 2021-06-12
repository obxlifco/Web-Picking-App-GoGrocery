import { throwError as observableThrowError,  Observable } from 'rxjs';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import { Injectable} from '@angular/core'; 
import { GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';

@Injectable()
export class OrderService {
	private baseApiUrl = GlobalVariable.BASE_API_URL;
	private elasticUrl = GlobalVariable.elasticURL;
	public post_data = {};
	constructor( 
		private _http: Http,
		private globalService: GlobalService,
		private _cookieService: CookieService
	) {
	
	}

	doGrid(data: any, page: number) {
		if (!page) {
			var url = this.baseApiUrl + 'global_list/';
		} else {
			var url = this.baseApiUrl + 'global_list/?page=' + page;
		}
		return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
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
			cols.forEach(function (item: any) {
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
			catchError(this.handleError));
	}

	private handleError(error: Response) {
		return observableThrowError(error || "Server err");
	}

	loadTagMasters() {
		return this._http.get(this.baseApiUrl + 'tag_list/', this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	loadWebsiteChannels() {
		return this._http.get(this.baseApiUrl + 'marketplace_list/', this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	updateOrderStatus(data) {
		return this._http.post(this.baseApiUrl + 'update_order_status/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	setOrderTags(data) {
		return this._http.post(this.baseApiUrl + 'assign_tag/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	assignWarehouse(data: any) {
		return this._http.post(this.baseApiUrl + 'assign_to_warehouse/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	doGridManageTags(data: any, page: number) {
		if (!page) {
			var url = this.baseApiUrl + 'global_list/';
		} else {
			var url = this.baseApiUrl + 'global_list/?page=' + page;
		}
		return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	getAreaSubarea(keyword: any) {
		return this._http.get(this.baseApiUrl + 'area-subarea/?keyword=' + keyword, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}



	loadTagsDetails(id: number) {
		if (id > 0) {
			return this._http.get(this.baseApiUrl + 'tag/' + id + '/', this.globalService.getHttpOption()).pipe(
				map(res => res.json()),
				catchError(this.handleError));
		} else { }
	}

	tagAddEdit(data: any, id: any) {
		if (id > 0) {
			return this._http.post(this.baseApiUrl + 'manage_tags/', data, this.globalService.getHttpOption()).pipe(
				map(res => res.json()),
				catchError(this.handleError));
		} else {
			return this._http.post(this.baseApiUrl + 'manage_tags/', data, this.globalService.getHttpOption()).pipe(
				map(res => res.json()),
				catchError(this.handleError));
		}
	}

	loadWarehouseList() {
		return this._http.get(this.baseApiUrl + 'warehouse-list/', this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	loadChanneslMasters(website_id: number) {
		return this._http.get(this.baseApiUrl + 'marketplace_list/', this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	getCustomOrderId(webshop_id: number) {
		return this._http.get(this.baseApiUrl + 'generate_order_id/' + webshop_id + '/', this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	getWebsitePaymentMethods(data: number) {
		return this._http.post(this.baseApiUrl + 'payment_method_list/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	loadCountry() {
		return this._http.get(this.baseApiUrl + 'countrylist/', this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	loadStates(country_id) {
		return this._http.get(this.baseApiUrl + 'countrystatelist/' + country_id + '/', this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	filterCustomerList(data) {
		return this._http.post(this.baseApiUrl + 'find_customer/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	getCustomerAddressInfo(data) {
		return this._http.post(this.baseApiUrl + 'get_customer_info/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	loadProduct(data) {
		return this._http.post(this.baseApiUrl + 'warehousewise_product/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	loadCartInfo(data: any) {
		return this._http.post(this.baseApiUrl + 'product_discount_calculation/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	generatePicklist(data: any) {
		return this._http.post(this.baseApiUrl + 'picklist/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	generateShipment(data: any) {
		return this._http.post(this.baseApiUrl + 'shipment/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	createOrders(data: any, id:number) {
		if(id>0) {
			return this._http.put(this.baseApiUrl + 'edit-order/', data, this.globalService.getHttpOption()).pipe(
				map(res => res.json()),
				catchError(this.handleError));
		} else {
			return this._http.post(this.baseApiUrl + 'save-order/', data, this.globalService.getHttpOption()).pipe(
				map(res => res.json()),
				catchError(this.handleError));
		}
	}

	getAvailableSlot(zoneId) {
		return this._http.get(this.baseApiUrl + 'delivery-slot/?zone_id=' + zoneId, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	productLoad(data: any, page: number) {
		if (!page) {
			var url = this.baseApiUrl + 'warehousewise_product/';
		} else {
			var url = this.baseApiUrl + 'warehousewise_product/?page=' + page;
		}
		return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	loadGridES(moduleName: any, page: number, keywords: any, pageSize: number, sortFields: any, sortOrder, advancedSearch, websiteId) {
		// let userData = this._cookieService.getObject('userData');
		// if (userData["elastic_store_name"] != "") {
		// 	userData["elastic_url"] = userData["elastic_url"] + userData["elastic_store_name"]+"_";
		// }
		
		// let url = userData["elastic_url"] + 'order_' + websiteId + '/data/_search';
		// //let url = this.elasticUrl + 'order_'+websiteId+'/data/_search'
		// return this._http.post(url, advancedSearch, this.globalService.getHttpOptionNotLogin()).pipe(
		// 	map(res => res.json()),
		// 	catchError(this.handleError));

		 let payload :any = {}
         payload.table_name = "EngageboostOrdermaster";
         payload.website_id = this.globalService.getWebsiteId();
         payload.data = advancedSearch;

        return this._http.post(this.baseApiUrl + 'search_elastic/', payload, this.globalService.getHttpOptionNotLogin()).pipe(
        map(res => res.json()),
        catchError(this.handleError), );


	}
	
	orderLoad(id:number) {
    	let website_id:number = this.globalService.getWebsiteId();
    	if(id>0) {
    		// edit order get data...existing order get data for get method OrderList
        	return this._http.get(this.baseApiUrl+'orderinfoviewset/'+id+'/'+website_id+'/',this.globalService.getHttpOption()).pipe(
				map(res => res.json()),
				catchError(this.handleError));
		} else {
			// create/add order get data... new order get for get method
          	return this._http.get(this.baseApiUrl+'ordersloadview/'+ website_id+'/',this.globalService.getHttpOption()).pipe(
				map(res => res.json()),
				catchError(this.handleError));
	    }
    }
    //  Open popup product data for addand edit products...
    // getProducts(data:any, page: number){
    // 	if (!page) {
	// 		var url = this.baseApiUrl + 'orders_load_view_product/';
	// 	} else {
	// 		var url = this.baseApiUrl + 'orders_load_view_product/?page=' + page;
	// 	}
    //   	return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
	//       	map(res => res.json()),
	// 		catchError(this.handleError));
	// }
	getProducts(data:any, page: number){
    	if (!page) {
			var url = this.baseApiUrl + 'warehousewise_product/';
		} else {
			var url = this.baseApiUrl + 'warehousewise_product/?page=' + page;
		}
      	return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
	      	map(res => res.json()),
			catchError(this.handleError));
	}

	getProductsES1(advancedSearch, websiteId) {
		let userData = this._cookieService.getObject('userData');
		if (userData["elastic_store_name"]!= "") {
			userData["elastic_url"] = userData["elastic_url"] + userData["elastic_store_name"]+"_";
		}
		let url = userData["elastic_url"] + 'product_' + websiteId + '/data/_search';
		//let url = this.elasticUrl + 'product_' + websiteId + '/data/_search'
		return this._http.post(url, advancedSearch, this.globalService.getHttpOptionNotLogin()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
	}

	getProductsES(advancedSearch, websiteId) {
		
        let payload :any = {}
         payload.table_name = "EngageboostProducts";
         payload.website_id = this.globalService.getWebsiteId();
         payload.data = advancedSearch;

        return this._http.post(this.baseApiUrl + 'search_elastic/', payload, this.globalService.getHttpOptionNotLogin()).pipe(
        map(res => res.json()),
        catchError(this.handleError), );
	}


    orderAddEdit(data:any, id:number){
        let website_id:number = this.globalService.getWebsiteId();
        if(id>0){
        	// edit order save data...existing order save data for put method 
            return this._http.put(this.baseApiUrl+'orderinfoviewset/'+id+'/'+website_id+'/', data, this.globalService.getHttpOption()).pipe(
				map(res => res.json()),
				catchError(this.handleError));
	    } else {
	    	// create/add order save data... new order save for post method
            return this._http.post(this.baseApiUrl+'orderinfoviewset/', data, this.globalService.getHttpOption()).pipe(
				map(res => res.json()),
				catchError(this.handleError));
        }
    }

    getOrderActivity(id:number) {
    	let website_id:number = this.globalService.getWebsiteId();
    	return this._http.get(this.baseApiUrl+'get-order-activity/'+id+'/'+website_id+'/',this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError));
		
    }
}