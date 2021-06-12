import { throwError as observableThrowError, Observable } from 'rxjs';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { Injectable } from '@angular/core';
import { GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';
@Injectable()
export class ShipmentService {
	private baseApiUrl = GlobalVariable.BASE_API_URL;
	public post_data = {};
	constructor(
		private _http: Http, 
		private globalService: GlobalService
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
			catchError(this.handleError),);
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
		return this._http.post(this.baseApiUrl + 'global_list_filter/', this.post_data, this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError),);
	}

	private handleError(error: Response) {
		return observableThrowError(error || "Server err");
	}

	loadTagMasters() {
		return this._http.get(this.baseApiUrl + 'tag_list', this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	loadWebsiteChannels() {
		return this._http.get(this.baseApiUrl + 'marketplace_list', this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	updateOrderStatus(data) {
		return this._http.post(this.baseApiUrl + 'update_order_status/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	setOrderTags(data) {
		return this._http.post(this.baseApiUrl + 'assign_tag/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	assignWarehouse(data: any) {
		return this._http.post(this.baseApiUrl + 'assign_to_warehouse/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	doGridManageTags(data: any, page: number) {

		if (!page) {
			var url = this.baseApiUrl + 'global_list/';
		} else {
			var url = this.baseApiUrl + 'global_list/?page=' + page;
		}
		return this._http.post(url, data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	loadTagsDetails(id: number) {
		if (id > 0) {
			return this._http.get(this.baseApiUrl + 'tag/' + id + '/', this.globalService.getHttpOption()).pipe(
				map(res => res.json()),
				catchError(this.handleError),);
		} else {}
	}

	tagAddEdit(data: any, id: any) {
		if (id > 0) {
			return this._http.post(this.baseApiUrl + 'manage_tags/', data, this.globalService.getHttpOption()).pipe(
				map(res => res.json()),
				catchError(this.handleError),);
		} else {
			return this._http.post(this.baseApiUrl + 'manage_tags/', data, this.globalService.getHttpOption()).pipe(
				map(res => res.json()),
				catchError(this.handleError),);
		}
	}

	loadWarehouseList() {
		return this._http.get(this.baseApiUrl + 'warehouse_list/', this.globalService.getHttpOption()).pipe(map(res => res.json()),
			catchError(this.handleError),);
	}

	loadChanneslMasters(website_id: number) {
		return this._http.get(this.baseApiUrl + 'marketplace_list/', this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	getCustomOrderId(webshop_id: number) {
		return this._http.get(this.baseApiUrl + 'generate_order_id/' + webshop_id, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	getWebsitePaymentMethods(data: number) {
		return this._http.post(this.baseApiUrl + 'payment_method_list/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	loadCountry() {
		return this._http.get(this.baseApiUrl + 'countrylist/', this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	loadStates(country_id) {
		return this._http.get(this.baseApiUrl + 'countrystatelist/' + country_id, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	loadPickList(data: any) {
		return this._http.post(this.baseApiUrl + 'picklist/', data, this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError));
	}
	
	generatePicklist(data: any) { // genrating the pickslist of the shipment
		return this._http.post(this.baseApiUrl + 'create_picklist/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),)
	}

	loadInvoices(data: any) { // loading the invoice details 
		return this._http.post(this.baseApiUrl + 'invoice/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	printInvoice(data: any) {
		return this._http.post(this.baseApiUrl + 'printinvoice/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	loadGrn(picklist_id:any,website_id: number) {
		return this._http.get(this.baseApiUrl + 'picklist-order-details/'+ picklist_id + '/'+ website_id+ '/', this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	loadDeliveryPlanner(data: any) { // loading the invoice details 
		return this._http.post(this.baseApiUrl + 'delivery-planner/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	
	getGrnOrderDetails(data: any) {
		return this._http.post(this.baseApiUrl + 'grn_order_details_by_order_id/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);   
	}

	getGrnSubstituteProducts(data: any) {
		return this._http.post(this.baseApiUrl + 'get_grn_substitute_products/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),catchError(this.handleError),);   
	}

	getOrderProductsInfo(data: any) {
		return this._http.post(this.baseApiUrl + 'get_order_products_info/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),catchError(this.handleError),);   
	}

	searchPickedProducts(data: any) {
		return this._http.post(this.baseApiUrl + 'search-picked-products/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),catchError(this.handleError),);
	}

	addCrates(data: any) {
		return this._http.post(this.baseApiUrl + 'add-crates/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),catchError(this.handleError),);
	}

	deleteCrates(data: any) {
		return this._http.post(this.baseApiUrl + 'delete-crates/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),catchError(this.handleError),);
	}

	getAllCrates(data: any) {
		return this._http.post(this.baseApiUrl + 'crate-list/', data, this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError),);   
	}


	grnSaveAsDraft(data: any) {
		return this._http.post(this.baseApiUrl + 'grn_draft/', data, this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError),);   
	}

	grnComplete(data: any) {
		return this._http.post(this.baseApiUrl + 'grn_complete/', data, this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError),);   
	}

	getAssignVehicle(data: any) {
		return this._http.post(this.baseApiUrl + 'assign_vehicle/', data, this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError),);   
	}

	createAssignVehicle(data: any) {
		return this._http.post(this.baseApiUrl + 'create_assign_vehicle/', data, this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError),);   
	}

	loadManifest(data: any) {
		return this._http.post(this.baseApiUrl + 'shipping_manifest/', data, this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError),);   
	}
	
	createManifest(data: any) {
		return this._http.post(this.baseApiUrl + 'create_shipping_manifest/', data, this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError),);   
	}

	printManifest(data: any) {
		return this._http.post(this.baseApiUrl + 'print_manifest/', data, this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError),);   
	}

	removeFromShipment(data: any) {
		return this._http.post(this.baseApiUrl + 'remove-from-shipment/', data, this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError),);   
	}

	deleteShipment(data: any) {
		return this._http.post(this.baseApiUrl + 'delete-shipment/',data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	deletePicklist(data: any) {
		return this._http.post(this.baseApiUrl + 'delete-picklist/',data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	saveSortBydistance(data: any) { // loading the invoice details 
		return this._http.post(this.baseApiUrl + 'save-sortby-distance/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	printPicklist(data: any) {
		return this._http.post(this.baseApiUrl + 'printpicklist/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);
	}

	getGrnProductInfo(data: any) {
		return this._http.post(this.baseApiUrl + 'get_grn_products_info/', data, this.globalService.getHttpOption()).pipe(
			map(res => res.json()),
			catchError(this.handleError),);   
	}

	saveEditGRN(data: any) {
		return this._http.post(this.baseApiUrl + 'save_edit_grn/', data, this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError),);   
	}

	saveEditPrice(data: any) {
		return this._http.post(this.baseApiUrl + 'save_edit_price/', data, this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError),);   
	}

	saveSubstituteProduct(data: any) {
		return this._http.post(this.baseApiUrl + 'save_substitute_product/', data, this.globalService.getHttpOption()).pipe(map(res => res.json()),catchError(this.handleError),);   
	}
}