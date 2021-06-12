
import { mergeMap, map, filter } from 'rxjs/operators';
import { Component, OnInit, OnDestroy, Optional, Inject, ElementRef } from '@angular/core';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { PromotionService } from './products.promotion.service';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { Global } from '../../global/service/global';
import { DialogsService } from '../../global/dialog/confirm-dialog.service';
import { DOCUMENT } from '@angular/platform-browser';

@Component({
	templateUrl: './templates/add_coupon.html',
	providers: [PromotionService]
})
export class PromotionAddEditComponent implements OnInit, OnDestroy {

	public response: any;
	public errorMsg: string;

	public customergrp_list: any;
	public formModel: any = {};
	public minDate: any;
	public discount_master_type: number;
	public all_warehouse: any=[];
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public ipaddress: any;
	public add_edit: any;
	public selected_ids: any;
	public product_id_qty:any;
	public generated:boolean=false;
	public export_coupons:any;
	public export_coupons_file_path:string;
	public show_coupon:boolean=false;
	public isDisable:boolean=false;
	public childData = {};
	public coupon_prefix;
	public coupon_suffix;
	constructor(
		private _promotionService: PromotionService,
		public _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _cookieService: CookieService,
		public dialog: MatDialog,
		private global: Global,

	) {

		this.ipaddress = _globalService.getCookie('ipaddress');
		this._router.events.pipe(
			filter((event) => event instanceof NavigationEnd),
			map(() => this._route),
			map((route) => {
				while (route.firstChild) route = route.firstChild;
				return route;
			}),
			filter((route) => route.outlet === 'primary'),
			mergeMap((route) => route.data))
			.subscribe((event) => {
				this.discount_master_type = event['discountType'];

			});
	}

	ngOnInit() {

		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);

		this.sub = this._route.params.subscribe(params => {
			this.formModel.discountId = +params['id']; // (+) converts string 'id' to a number
		});
		
		if(this._router.url.includes('discount_coupon')){
			console.log('coupon')
			this.childData = {
				table : 'EngageboostDiscountMasters',
				heading : 'Coupon Specific Discount',
				ispopup:'N',
				tablink:'discount_coupon',
				tabparrentid:'0',
				screen:'list1',
				is_import: 'Y',
				is_export: 'Y'
			  }
		}

		if(this.formModel.discountId>0){
			this.export_all_coupons(this.formModel.discountId);
		}
		if (this.formModel.discountId) {
			this._cookieService.putObject('coupon_edit', this.formModel.discountId);
			this._cookieService.putObject('action', 'edit');
			this.add_edit = 'edit';
		} else {
			this._cookieService.putObject('action', 'add');
			this.formModel.discountId = this._cookieService.getObject('coupon_add');
			this.add_edit = 'add';
		}


		this._promotionService.promotionLoad(this.formModel.discountId).subscribe(
			data => {
				this.response = data;
				if (this.formModel.discountId > 0) {
					this.formModel = this.response.api_status;
					this.product_id_qty= this.response.api_status.product_id_qty;
					this.selected_ids=this.response.api_status.product_id;
					this.formModel.free_items=this.response.api_status.freebies_product_sku;

					this.customergrp_list = this.response.customer_group;
					this.formModel.discountId = this.response.api_status.id;
					this.formModel.disc_type = this.formModel.disc_type.toString();
					this.formModel.coupon_type = this.formModel.coupon_type.toString();
					if (this.response.api_status.has_multiplecoupons == 'n') {
						this.formModel.generate_couponcode = 'single';
					} else {
						this.formModel.generate_couponcode = 'multiple';
						this.formModel.coupon_codes = this.response.multiple_coupons;
						this.formModel.coupon_codes_temp = this.response.multiple_coupons;
						this.formModel.number_of_coupon = this.response.multiple_coupons.length;
					}
					if (this.response.api_status.customer_group) {
						this.formModel.customer_group = this.response.api_status.customer_group.split(",").map(Number);
					}
					if (this.response.api_status.warehouse_id) {
						this.formModel.warehouse = this.response.api_status.warehouse_id.split(",").map(Number);
					}
					this.minDate = new Date();
					this.minDate.setMinutes(this.minDate.getMinutes() - 1);
					this.formModel.disc_start_date = new Date(this.formModel.disc_start_date);
					this.formModel.disc_end_date = new Date(this.formModel.disc_end_date);
					if(this.formModel.disc_type == 7){
						this.isDisable = true;
					}
				} else {
					this.customergrp_list = this.response.customer;
					this.formModel.discountId = 0;
					this.formModel.generate_couponcode = 'single';
					this.formModel.isblocked = 'n';
					this.formModel.disc_type = '1';
					this.formModel.coupon_type = '1';
					this.minDate = new Date();
					this.minDate.setMinutes(this.minDate.getMinutes() - 1);
				}

			},
			err => {
				this._globalService.showToast('Something went wrong. Please try again.');
			},
			function () {
				//completed callback
			}
		);
		this.warehouseList();
	}

	ngOnDestroy() {
		this.sub.unsubscribe();
	}

	getDiscountType(discount_type_id){
		if(discount_type_id == 7){
			this.formModel.amount = 0;
			this.isDisable = true;
		}
	}

	generateCode(type: string) {
		if (type == 'single') { //single code
			this.formModel.coupon_code = this.randomCode();
		} else { // multiple code
			if (this.formModel.number_of_coupon > 0) {
				if (this.formModel.coupon_codes == '') {
					if (!this.formModel.coupon_codes) {
						this.formModel.coupon_codes = [];
					}
					for (var i = 0; i < this.formModel.number_of_coupon; i++) {
						this.formModel.coupon_codes.push({ coupon_code: this.randomCode(), is_used: 'n' });
					}
				this.generated=true;
				} else {
					this.formModel.coupon_codes = [];
					for (var i = 0; i < this.formModel.number_of_coupon; i++) {
						this.formModel.coupon_codes.push({ coupon_code: this.randomCode(), is_used: 'n' });
					}
				this.generated=true;
				}
			} else {
				this._globalService.showToast('Number of coupon must be greater than 0');
			}
		}
	}

	randomCode() {
		var text = "";
		var charset = "abcdefghijklmnopqrstuvwxyz0123456789";

		for (var i = 0; i < 6; i++)
			text += charset.charAt(Math.floor(Math.random() * charset.length));

		return text;
	}
	
	export_all_coupons(id:any){
		let data={discount_master_id:id}
		this.global.getWebServiceData('couponexport','POST',data,'').subscribe(data => {
			if(data.status==1){
				this.export_coupons_file_path = data.file_path;
				this.export_coupons = window.location.protocol + '//' + window.location.hostname + ':8062' + '/'+ this.export_coupons_file_path;
				this.show_coupon=true;
			}
		})
	}
	addEditCoupon(form: any) {
		if (this.formModel.disc_start_date > this.formModel.disc_end_date) {
			this.errorMsg = 'End Date should be greater than Start Date';
			this._globalService.showToast(this.errorMsg);
		} else {
			this.errorMsg = ''; 
			// if(this.formModel.warehouse){
			// 	if(this.formModel.warehouse.includes(0)){
			// 		this.formModel.warehouse = [];
			// 		this.all_warehouse.forEach(e => {
			// 			if(e['id'] != 0){
			// 				this.formModel.warehouse.push(e['id']);
			// 			}
			// 		});
			// 	}
			// }
			var data: any = {};
			data.value = {};
			if(this.childData['tablink'] == 'discount_coupon'){
				this.formModel.coupon_prefix = this.formModel.coupon_prefix ? this.formModel.coupon_prefix : '';
				this.formModel.coupon_suffix = this.formModel.coupon_suffix ? this.formModel.coupon_suffix : '';
				data.value = Object.assign({}, this.formModel);
			}else{
				data.value = Object.assign({}, this.formModel);
			}
			data.value.website_id = this._globalService.getWebsiteId();
			if (!this.formModel.used_coupon) {
				data.value.used_coupon = 0;
			}
			if (this.formModel.discountId < 1) {
				data.value.createdby = this._globalService.getUserId();
			}
			data.value.updatedby = this._globalService.getUserId();

			if (this.formModel.generate_couponcode == 'single' || this.discount_master_type == 0) {
				data.value.has_multiplecoupons = 'n';
			} else {
				data.value.has_multiplecoupons = 'y';
				data.multiple_coupons = [];
				data.multiple_coupons = this.formModel.coupon_codes;
			}

			if (this.formModel.customer_group) {
				data.value.customer_group = this.formModel.customer_group.join();
			}
			if(this.formModel.warehouse){
				data.value.warehouse_id = this.formModel.warehouse.join();
			}

			if (this.ipaddress) {
				data.value.ip_address = this.ipaddress;
			} else {
				data.value.ip_address = "";
			}
			if (this.discount_master_type == 0) {

				data.value.coupon_type = 1;
				data.value.discount_master_type = 0;
				data.value.product_id_qty=this.product_id_qty;
				data.value.product_id=this.selected_ids;
				data.value.freebies_product_sku=this.formModel.free_items;
			} else {
				data.value.discount_master_type = 1;
			}
			if(this.formModel.offer_type){
				data.value.offer_type = this.formModel.offer_type;
			}
			this._promotionService.promotionAddEdit(data, this.formModel.discountId).subscribe(
				data => {
					this.response = data;
					if (this.response.status == 1) {
						if (this.add_edit == 'add') {
							this._cookieService.putObject('coupon_add', this.response.api_status.id);
							if (this.discount_master_type) {
								this._router.navigate(['/discount_coupon/conditions']);
							} else {
								this._router.navigate(['/discount_product/conditions']);
							}
						} else {
							if (this.discount_master_type) {
								this._router.navigate(['/discount_coupon/edit/' + this.formModel.discountId + '/conditions']);
							} else {
								this._router.navigate(['/discount_product/edit/' + this.formModel.discountId + '/conditions']);
							}
						}
					} else {
						this.errorMsg = this.response.message;
						if(this.response.message=='Data Not Found'){
							this._globalService.showToast('Please enter valid data');
						}else{
							this._globalService.showToast(this.response.message);
						}
					}
				},
				err => {
					this._globalService.showToast('Something went wrong. Please try again.');
				},
				function () {
					//completed callback
				}
			);
		}

	}
	dialogProductRef: MatDialogRef<FreeProductListComponent> | null;

	openPop() {
		let data: any = {};
		let temp_pro_id=this.selected_ids;
		data['all_product_id']=temp_pro_id;
		data['all_product_id_qty']=this.product_id_qty;
		this.dialogProductRef = this.dialog.open(FreeProductListComponent, { data: data });
		this.dialogProductRef.afterClosed().subscribe(result => {
			if (result) {
				this.selected_ids = result['product_ids'];
				this.product_id_qty = result['product_id_quantity'];
				this.formModel.free_items = result['product_names'];
			}
		});
	}

	warehouseList() {
		let userData = this._cookieService.getObject('userData');
		let userId = userData['uid'];
		let data = {
			"model": 'EngageboostWarehouseMasters',
			"screen_name": 'list',
			"userid": userId,
			"search": '',
			"order_by": 'name',
			"order_type": '+',
			"status": 'n',
			"show_all":1,
			"website_id": this._globalService.getWebsiteId()
		}
		this._promotionService.warehouseLoad(data).subscribe(
			data => {
			  let that = this;
			  this.response = data;
			  this.all_warehouse = [];
				
			  if(this.response.count > 0) {
				this.all_warehouse = this.response.results[0].result;
				// if(this.childData['tablink'] == 'discount_coupon'){
				// 	let obj = {};
				// 	obj["id"]= 0 ;
				// 	obj["name"]='All';
				// 	this.all_warehouse.splice(0, 0, obj);
				// }
			} else if(this.response[0].active>0) {
				this.all_warehouse = this.response[0].result;
			}else{
				  this.all_warehouse = [];

			  }
			//   } else {
			// 	this.all_warehouse = [];
			//   }
			},
			err => {
			  this._globalService.showToast('Something went wrong. Please try again.');
			},
			function(){
			  //completed callback
			}
		);
		// this._promotionService.warehouseLoad(data).subscribe(
		// 	data => {
		// 	  let that = this;
		// 	  this.response = data;
		// 	  this.all_warehouse = [];
				
		// 	  if(this.response.count > 0) {
		// 		this.all_warehouse = this.response.results[0].result;
		// 		// if(this.childData['tablink'] == 'discount_coupon'){
		// 		// 	let obj = {};
		// 		// 	obj["id"]= 0 ;
		// 		// 	obj["name"]='All';
		// 		// 	this.all_warehouse.splice(0, 0, obj);
		// 		// }
		// 	  } else {
		// 		this.all_warehouse = [];
		// 	  }
		// 	},
		// 	err => {
		// 	  this._globalService.showToast('Something went wrong. Please try again.');
		// 	},
		// 	function(){
		// 	  //completed callback
		// 	}
		// );
	  }
}

@Component({
	templateUrl: './templates/free_products.html',
	providers: [PromotionService,Global]
})
export class FreeProductListComponent implements OnInit {
	public product_list: any = [];
	public response: any;
	public selectedAll: boolean;
	public bulk_ids: any = [];
	public search_text: string;
	public sortBy: any = '';
	public sortOrder: any = '';
	public sortClass: any = '';
	public sortRev: boolean = false;
	public customer_list: any = [];
	public errorMsg: string;
	public bulk_ids_exist: any = [];
	public pagination: any = {};
	public pageIndex: number = 0;
	public pageList: number = 0;
	public website_id: number = 1;
	public stat: any = {};
	public result_list: any = [];
	public total_list: any = [];
	public cols: any = []
	public post_data = {};
	public page: number = 1;
	public filter: string = '';
	public maxSize: number = 10;
	public directionLinks: boolean = true;
	public autoHide: boolean = false;
	public config: any = {};
	public customers: any = [];
	public formModel: any = {};
	public userId: number;
	constructor(
		public _globalService: GlobalService,
		private _promotionService: PromotionService,
		public dialog: MatDialog,
		private dialogRef: MatDialogRef<FreeProductListComponent>,
		private _cookieService: CookieService,
		private global: Global,

		@Inject(MAT_DIALOG_DATA) public data: any
	) {
			global.reset_dialog();
	}


	ngOnInit() {

		if (this.data['all_product_id']) {
			this.bulk_ids = this.data['all_product_id'].split(",").map(Number);
		}
		this.generateGrid(0, '', '', '', '');
		
		
	}

	closeDialog() {
		this.dialogRef.close();
	}

	generateGrid(reload: any, page: any, sortBy: any, filter: any, search: any) {
		this.sortBy = sortBy;

		if (sortBy != "" && sortBy != undefined) {
			if (this.sortRev) {
				this.sortOrder = "-";
				this.sortRev = !this.sortRev;
				this.sortClass = "icon-down";
			} else {
				this.sortOrder = "+";
				this.sortRev = !this.sortRev;
				this.sortClass = "icon-up";
			}
		}

		let userData = this._cookieService.getObject('userData');
		this.userId = userData['uid'];

		let data = {
			"model": 'EngageboostProducts',
			"screen_name": 'list',
			"userid": this.userId,
			"search": this.search_text,
			"order_by": sortBy,
			"order_type": this.sortOrder,
			"status": 'n',
			"visibility_id": "Category,Search",
			"website_id": this._globalService.getWebsiteId()
		}

		this._promotionService.productLoad(data, page).subscribe(
			data => {
				let that = this;
				this.response = data;
				this.total_list = [];
				
				if (this.response.count > 0) {
					this.result_list = this.response.results[0].result;
					this.result_list.forEach(function (item: any) {
					item.quantity=1;
						if (that.bulk_ids.indexOf(item.id) > -1) {
							item.Selected = true;
							//Checking for item quantity
							item.quantity= 1;
							let str = that.data.all_product_id_qty;
							let str_array = str.split(',');
							str_array.forEach(element => {
								let temp_id=element.split('@')[0];
								let temp_qty=element.split('@')[1];
								if(item.id==temp_id){
									item.quantity=temp_qty;
								}
							});
						}
					});
					for (var i = 0; i < this.response.count; i++) {
						this.total_list.push(i);
					}
				} else {
					this.result_list = [];
				}
				this.pagination.total_page = this.response.per_page_count;
				this.pageList = this.response.per_page_count;
				this.config.currentPageCount = this.result_list.length
				this.config.currentPage = page
				this.config.itemsPerPage = this.response.page_size;

			},
			err => {
				this._globalService.showToast('Something went wrong. Please try again.');
			},
			function () {
				//completed callback
			}
		);
	}


	////////////////////////////Check/Uncheck//////////////

	toggleCheckAll(event: any) {

		let that = this;
		that.bulk_ids = [];
		this.selectedAll = event.checked;
		this.result_list.forEach(function (item: any) {
			
			item.Selected = event.checked;
			if (item.Selected) {
				that.bulk_ids.push(item.id);
			}
		});

	}

	toggleCheck(id: any, event: any) {

		let that = this;
		this.result_list.forEach(function (item: any) {
			if (item.id == id) {
				item.Selected = event.checked;
				if (item.Selected) {
					that.bulk_ids.push(item.id);
				}
				else {
					var index = that.bulk_ids.indexOf(item.id);
					that.bulk_ids.splice(index, 1);
				}
			}
		});
	}

	saveSku() {

		let returnData: any = [];
		// returnData['index'] = this.data.index;

		let product_ids: string = '';
		let product_names: string = '';
		let products: any = [];
		let item_quantity: any = [];

		product_ids = this.bulk_ids.join(',');

		let that = this;
		this.bulk_ids.forEach(function (item: any) {

			that.result_list.forEach(function (inner_item: any) {

				if (item == inner_item.id) {
					products.push(inner_item.sku);
					item_quantity.push(inner_item.id+'@'+inner_item.quantity);
				}
			});
		});

		product_names = products.join(',');
		item_quantity = item_quantity.join(',');

		returnData['product_ids'] = product_ids;
		returnData['product_names'] = product_names;
		returnData['product_id_quantity'] = item_quantity;

		this.dialogRef.close(returnData);
	}
}

@Component({
	templateUrl: 'templates/import-promotion-file.html',
	providers: [Global,PromotionService]
})
export class ImportFileComponent implements OnInit {

	public response: any;
	public errorMsg: string;
	public formModel: any = {};
	public ipaddress: any;
	public sample_xls: any;
	public sample_csv: any;
	public xls_file: any;
	public website_id: any;
	public importOpt: any;
	public file_selection_tool: any;
	private userId: number;
	public parentId: number = 0;
	public tabIndex: number;
	public imported_file_name: string;

	constructor(
		private _globalService: GlobalService,
		private _router: Router,
		private dialogRef: MatDialogRef<ImportFileComponent>,
		public dialog: MatDialog,
		private _cookieService: CookieService,
		private _promotionService: PromotionService,
		private global: Global,

		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) { 
			global.reset_dialog();

		}

	ngOnInit() {
		this.sample_xls = window.location.protocol + '//' + window.location.hostname + ':8062' + '/media/importfile/sample/Discount_promotion_file.xls';
		this.sample_csv = window.location.protocol + '//' + window.location.hostname + ':8062' + '/media/importfile/sample/Discount_promotion_file.csv';
		this.importOpt = 'xls';
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		this.file_selection_tool = 'No file choosen';
		let userData = this._cookieService.getObject('userData');
		this.userId = userData['uid'];
		this.website_id = this._globalService.getWebsiteId();
	}

	import_file_promotion(e: Event) {
		var files: any = {};
		var target: HTMLInputElement = e.target as HTMLInputElement;
		for (var i = 0; i < target.files.length; i++) {
			var file_arr: any = [];

			var reader = new FileReader();
			reader.readAsDataURL(target.files[i]);
			reader.onload = (event) => {
				file_arr['url'] = event.srcElement['result']
			}

			file_arr['_file'] = target.files[i];
			files[this.data] = file_arr;
		}
		var filename = files.import_file._file.name;
		this.file_selection_tool = filename;
		this.xls_file = files.import_file._file;
		var extn = filename.split(".").pop();
		if (extn == 'xls' || extn == 'xlsx') {
		} else {
			this._globalService.showToast('Please choose XLS/XLSX file');
		}
	}

	send_file_data(form: any) {
		var form_data = new FormData();
		form_data.append("import_file", this.xls_file);
		form_data.append('website_id', this.website_id);
		form_data.append("import_file_type", 'promotion');
		if (this.xls_file != undefined) {
			this._promotionService.import_promotion_file_data(form_data).subscribe(
				data => {
					this.response = data;
					this.imported_file_name = data.filename;
					this._cookieService.putObject('promotion_imported_data', '');
					this.save_promotion_file_data();


					this.dialogRef.close();
				},
				err => console.log(err)
			);
		} else {
			this._globalService.showToast('Please choose XLS/XLSX file');
		}
	}

	save_promotion_file_data() {

		var data: any = {};
		var form_data: any = {};
		data.website_id = this._globalService.getWebsiteId();
		data.filename = this.imported_file_name;
		data.category_id = 3;
		this._promotionService.save_promotion_file_data(data).subscribe(
			res => {
				this.response = data;
				let imported_result: any = {};
				this._cookieService.putObject('promotion_imported_data', '');
				imported_result.imported_filename = this.imported_file_name;
				imported_result.website_id = this._globalService.getWebsiteId();
				this._cookieService.putObject('promotion_imported_data', imported_result);
				this._globalService.addTab('priviewproducts', 'discount_product/preview_promotion', 'Preview Promotion', this.parentId)
				this._router.navigate(['/discount_product/preview_promotion']);
			},
			err => {
				this._globalService.showToast('Something went wrong. Please try again.');
			},
			function () {
				//completed callback
			}
		)
	}

	closeDialog() {
		this.dialogRef.close();
	}
}

@Component({
	selector: 'my-app',
	templateUrl: `./templates/promotion_preview.html`,
	providers: [Global, PromotionService],
})

export class PromotionPreviewComponent implements OnInit {

	constructor(
		public globalService: GlobalService,
		private _globalService: GlobalService,
		private _cookieService: CookieService,
		public dialog: MatDialog,
		private _promotionService: PromotionService,
		private dialogsService: DialogsService,
		private _router: Router,
		@Inject(DOCUMENT) private document: any
	) { }

	public response: any;
	public errorMsg: string;
	public bulk_ids: any = [];
	public columns: any = [];
	public temp_result_list: any = [];
	public result_list: any = [];
	public selectedAll: any = false;
	public tabIndex: number;
	public parentId: number = 0;
	public userId: any;
	public individualRow: any = {};
	//////////////////////////Initilise////////////////////////////

	ngOnInit() {

		this.tabIndex = +this.globalService.getCookie('active_tabs');
		this.parentId = this.globalService.getParentTab(this.tabIndex);
		let userData = this._cookieService.getObject('userData');
		let promotion_imported_data = this._cookieService.getObject('promotion_imported_data');
		this.userId = userData['uid'];
		let post_data: any = {};
		post_data.filename = promotion_imported_data['imported_filename'];
		post_data.website_id = this._globalService.getWebsiteId();//promotion_imported_data.website_id;
		post_data.model = 'discount';
		this.columns = [
			{ 'field_name': 'name', 'label': 'name' },
			{ 'field_name': 'description', 'label': 'Description' },
			{ 'field_name': 'customer_group', 'label': 'Customar Group' },
			{ 'field_name': 'disc_start_date', 'label': 'Discount Start Date' },
			{ 'field_name': 'disc_end_date', 'label': 'Discount End Date' },
			{ 'field_name': 'discount_type', 'label': 'Discount Type' },
			{ 'field_name': 'amount', 'label': 'Amount' },
			{ 'field_name': 'category_equals', 'label': 'Category Equal' },
			{ 'field_name': 'no_of_quantity_per', 'label': 'No. of quantity' },
			{ 'field_name': 'offer_type', 'label': 'Offer type' },
			{ 'field_name': 'up_to_discount', 'label': 'Discount Up to' },
			{ 'field_name': 'discount_master_type', 'label': 'Discount Type' },
			{ 'field_name': 'discount_priority', 'label': 'Priority' },
			{ 'field_name': 'amount_equals', 'label': 'Amount Equal' },
			{ 'field_name': 'amount_equals_greater', 'label': 'Amount Greater Type' },
			{ 'field_name': 'amount_equals_less', 'label': 'Amount Equal Less' },
			{ 'field_name': 'category_not_equals', 'label': 'Category not equal' },
			{ 'field_name': 'condition_for_freebie_items', 'label': 'Condition' },
			{ 'field_name': 'coupon_code', 'label': 'Coupon' },
			{ 'field_name': 'coupon_prefix', 'label': 'Prefix' },
			{ 'field_name': 'coupon_suffix', 'label': 'Suffix' },
			{ 'field_name': 'coupon_type', 'label': 'Coupon type' },
			{ 'field_name': 'free_item_quantity', 'label': 'Free item quantity' },
			{ 'field_name': 'free_item_sku', 'label': 'Free item sku' },
			{ 'field_name': 'free_shipping', 'label': 'Free shipping' },
			{ 'field_name': 'freebies_product_ids', 'label': 'Free products' },
			{ 'field_name': 'freebies_product_sku', 'label': 'Free product sku' },
			{ 'field_name': 'number_of_coupon', 'label': 'No. of coupon' },
			{ 'field_name': 'product_name', 'label': 'Product name' },
			{ 'field_name': 'weekly_equals', 'label': 'Weekly Equal' },
			{ 'field_name': 'weekly_not_equals', 'label': 'Weekly not equal' },
		]
		this._promotionService.load_promotion_preview_grid(post_data, 1).subscribe(
			data => {
				this.temp_result_list = data.preview_data;
				let that = this;
				this.temp_result_list.forEach(function (item: any) {
					if (item.error == 0) {
						item.selected = true;
					}
					if (item.selected && item.error == 0) {
						that.bulk_ids.push(item.id);
						//elements[0].classList.add('show');
					} else {
						//elements[0].classList.remove('show');
					}
				});
			},
			err => {
				this.globalService.showToast('Something went wrong. Please try again.');
			},
			function () {
				//completed callback
			}
		);
	}

	////////////////////////////Check/Uncheck//////////////
	toggleCheckAllPreview(event: any) {
		let that = this;
		that.bulk_ids = [];
		this.selectedAll = event.checked;
		this.temp_result_list.forEach(function (item: any) {
			item.selected = event.checked;
			if (item.selected && item.error == 0) {
				that.bulk_ids.push(item.id);
				//elements[0].classList.add('show');
			} else {
				//elements[0].classList.remove('show');
			}
		});
	}

	toggleCheckPreview(id: any, event: any) {
		let that = this;
		this.temp_result_list.forEach(function (item: any) {
			if (item.id == id) {
				item.selected = event.checked;
				if (item.selected && item.error == 0) {
					that.bulk_ids.push(item.id);
				} else {
					var index = that.bulk_ids.indexOf(item.id);
					that.bulk_ids.splice(index, 1);
					if (that.bulk_ids.length == 0) {
					}
				}
			}
			if (that.bulk_ids.length == 1) {
				that.bulk_ids.forEach(function (item_id: any) {
					if (item_id == item.id) {
						that.individualRow = item;
					}
				});
			}
			that.selectedAll = false;
		});
	}

	ImportPromotionData(form: any) {
		if (this.bulk_ids.length > 0) {
			var msg = 'Are you sure to import selected products?';
			this.dialogsService.confirm('Warning', msg).subscribe(res => {
				if (res) {
					let post_data: any = {};
					let promotion_imported_data = this._cookieService.getObject('promotion_imported_data');
					post_data.filename = promotion_imported_data['imported_filename'];
					post_data.website_id = this.globalService.getWebsiteId();
					post_data.selected_ids = this.bulk_ids.join(); // convert array to string for selected ids
					this._promotionService.show_all_promotion_imported(post_data).subscribe(
						data => {
							this.globalService.deleteTab(this.tabIndex, this.parentId);
						},
						err => {
							this.globalService.showToast('Something went wrong. Please try again.');
						},
						function () {
						}
					);
				}
			});
		} else {
			this.dialogsService.alert('Error', ' Please select atleast one record!').subscribe(res => { });
		}
	}
}

@Component({
	templateUrl: 'templates/export-file.html',
	providers: [PromotionService]
})
export class ExportFileComponent implements OnInit {
	public errorMsg: string = '';
	public formModel: any = {};
	public download_url: any;
	public sample_csv: any;
	public file_data: any;
	public website_id_new: any;
	public company_id_new: any;
	public importOpt: any;
	constructor(private _globalService: GlobalService,
		private _stockService: PromotionService,
		public dialog: MatDialog,
		private dialogRef: MatDialogRef<ImportFileComponent>,
		private global: Global,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		this.formModel = Object.assign({}, this.data);
		global.reset_dialog();

	}

	ngOnInit() {
		this.download_url = window.location.protocol + '//' + window.location.hostname + ':8062' + '/media/exportfile/product_export.xls';
		this.sample_csv = window.location.protocol + '//' + window.location.hostname + ':8062' + '/media/importfile/sample/stock_import.csv';
		this.importOpt = 'xls';
	}

	closeDialog() {
		this.dialogRef.close();
	}
}