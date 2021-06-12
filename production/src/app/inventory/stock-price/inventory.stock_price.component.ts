import {Component,OnInit,Inject, HostListener, Optional} from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';
import {CookieService} from 'ngx-cookie';
import {PaginationInstance} from 'ngx-pagination';
import {DOCUMENT} from '@angular/platform-browser';
import { MatDialog,MatDialogRef,MAT_DIALOG_DATA } from '@angular/material';
import { StockPriceService } from './inventory.stock_price.service';
import {DialogsService} from '../../global/dialog/confirm-dialog.service';
import { Global, GlobalVariable } from '../../global/service/global';
import { ColumnLayoutComponent } from '../../global/grid/app.grid-global.component';
import { ViewChild} from '@angular/core';
import {VERSION} from '@angular/material';
import { FormControl } from '@angular/forms';
import {MatSelect} from '@angular/material';
import { Subject } from 'rxjs';
import { take, takeUntil } from 'rxjs/operators';
import { ReplaySubject } from 'rxjs';
interface Bank {
	id: string;
	name: string;
   }
@Component({
  templateUrl: 'templates/stock_price-listing.html',
  providers: [StockPriceService, Global]
})
export class StockPriceComponent implements OnInit {
	//MAT SELECT TO STRAT
	public bankCtrl: FormControl = new FormControl();
	public bankFilterCtrl: FormControl = new FormControl();
	public bankMultiCtrl: FormControl = new FormControl();
	public bankMultiFilterCtrl: FormControl = new FormControl();
	banks: Bank[] = [];
	public filteredBanks: ReplaySubject<Bank[]> = new ReplaySubject<Bank[]>(1);
	public filteredBanksMulti: ReplaySubject<Bank[]> = new ReplaySubject<Bank[]>(1);
	@ViewChild('singleSelect') singleSelect: MatSelect; 
	private _onDestroy = new Subject<void>();
	//MAT SELECT TO END
	public tabIndex: number;
	public parentId: number = 0;
	public warehouse_list: any = [];
	public stock_list: any = [];
	public total_stock_list: any = [];
	public default_warehouse: number;
	public hide_out_of_stock: boolean = false;
	public config: any = {};
	public total_list: any = [];
	public pagination: any = {};
	public pageIndex: number = 0;
	public pageList: number = 0;
	public page: number = 0;
	public filter: string;
	public search_text: any;
	public sortBy: any = '';
	public sortOrder: any = '';
	public sortClass: any = '';
	public sortRev: boolean = false;
	public selected_item: any = {};
	public maxSize: number = 10;
	public userId: number = 0;
	public permission: any = {};
	public cols: any = [];
	public category_list: any =[];
	public categoryList: any;
	public layout: any = [];
	response:any;
	public formModel: any = {};
	field_arr=[];
	ConditionArr=[];
	filterArr=[];
	public search_type_option=false;
	advanced_search=[];
	input_type:any;
	selectArr:any=[];
	temp_key:any=[];
	advanced_search_temp=[];
	advance_filter={};
	public total_product_image: any= [];
	Advancefilter={};
	show_data:any=[];
	remove_field_index:number;
	exclude_arr:any=[];
	public img_base: string;
	public message: any = {};	
	/*Infinite Scrolling*/

	from:any = 0;
	page_size: any;
	public throttle = 50;
  	public scrollDistance = 0;
	public scrollUpDistance = 0;
	public perPageCount: number;
	isSuperAdmin:any = 'Y';

	// public i=1;

	/*Infinite Scrolling*/
	
	constructor(
		public _globalService: GlobalService,
		private _global: Global,
		private _cookieService: CookieService,
		private _stockPriceService: StockPriceService,
		private dialogsService: DialogsService,
		private global: Global,
		public dialog: MatDialog, @Inject(DOCUMENT) private document: any) {
		this.tabIndex = +_globalService.getCookie('active_tabs');
		this.parentId = _globalService.getParentId(this.tabIndex);
		global.reset_dialog();
	}
	
	ngOnInit() {
		let userData = this._cookieService.getObject('userData');
		this.userId = userData['uid'];
		this.isSuperAdmin = userData['isSuperAdmin'];
		
		this.page_size=5;
		let websiteId = this._globalService.getWebsiteId();
		this._globalService.skeletonLoader(true);
		this._stockPriceService.warehouseLoad(websiteId, this.userId).subscribe(
			data => {
				this.warehouse_list = data.warehouse;
				this.default_warehouse = this.warehouse_list[0]['id'];
				this.callbackLoadStock(this.default_warehouse);
			},
			err => console.log(err),
			function() {
				//completed callback
			}
		);
		this.formModel.search_type=1;
		this.formModel.search_data='';
		this.formModel.temp_name='';
		this.load_category();
		this.img_base = GlobalVariable.S3_URL + 'product/200x200/';
	}

	onScroll() {
		console.log(this.perPageCount)
		let page = ++this.page;
		console.log(page)
		let data: any = {};
		data['warehouse_id'] = this.default_warehouse;
		data['order_by'] = 'id';
		data['order_type'] = '+';
		data['search'] = this.search_text;
		data['hide_out_of_stock'] = 0;
		data['userid'] = this.userId;
		data["advanced_search"]= this.advanced_search;
		data['category_id'] = this.categoryList ? this.categoryList : '';
		this.total_list = [];
		if(this.perPageCount >= page){
			this._globalService.showLoaderSpinner(true);
			this._stockPriceService.stockLoad(data, page).subscribe(
				data => {
					let myelement: HTMLElement = this.document.getElementsByClassName('autoclick');
					myelement[0].click();
					if (data.status == 0) { // this is for success response
						this.stock_list = [];
					} else {
						if(data.results[0].result.product.length > 0) {
							data.results[0].result.product.forEach( elmt => {
								this.stock_list.push(elmt);
							})
						}
						//this.stock_list = data.results[0].result.product;

						this.permission = data.results[0].role_permission;
					}
					this._globalService.showLoaderSpinner(false);

				},
				err =>{
					console.log(err);
					// this._globalService.showLoaderSpinner(false);
					this._globalService.skeletonLoader(false);

				}
			);
		}
	}

	onScrollUp(){
		// alert();
	}

	// SELECT TO END
	callbackLoadStock(warehouse_id: number) {
		console.log(this.categoryList)
		this._globalService.showLoaderSpinner(true);
		if(this.search_text) {
			this.search_text = this.search_text.trim();
		} else {
			this.search_text = '';
		}
		this.hide_out_of_stock = false;
		let data: any = {};
		data['warehouse_id'] = warehouse_id;
		data['order_by'] = 'id';
		data['order_type'] = '+';
		data['search'] = this.search_text;
		data['hide_out_of_stock'] = 0;
		data['userid'] = this.userId;
		data['category_id'] = this.categoryList ? this.categoryList : '';
		this.total_list = [];
		this.stock_list = [];

		this._stockPriceService.stockLoad(data, 1).subscribe(
			data => {
				if(data.status != 0){
					data.results[0].result.product.forEach(element => {
						this.total_product_image.push(element.product_image);
					});					
					this.stock_list = data.results[0].result.product;
					this.perPageCount = data.per_page_count;
					this.page = 1;
					this.permission = data.results[0].role_permission;
				}else{
					this.stock_list = [];
				}
				this._globalService.showLoaderSpinner(false);
			},
			err => console.log(err),
			function() {
				//completed callback
			}
		);
	}

	load_category_filter(){
		console.log(this.categoryList)
		this._globalService.showLoaderSpinner(true);
		let data: any = {};
		data['warehouse_id'] = this.default_warehouse;
		data['order_by'] = 'id';
		data['order_type'] = '+';
		data['search'] = this.search_text;
		data['hide_out_of_stock'] = 0;
		data['userid'] = this.userId;
		data['category_id'] = this.categoryList ? this.categoryList : '';
		this.total_list = [];
		this.total_product_image = [];
		this.stock_list = [];
		this._stockPriceService.stockLoad(data, 1).subscribe(
			data => {
				if(data.status != 0){
					data.results[0].result.product.forEach(element => {
						this.total_product_image.push(element.product_image);
					});					
					this.stock_list = data.results[0].result.product;
					this.perPageCount = data.per_page_count;
					this.page = 1;					
					this.permission = data.results[0].role_permission;
				} else {
					this.stock_list = [];
					this.total_product_image = [];
				}
				this._globalService.showLoaderSpinner(false);
			},
			err => console.log(err),
			function() {
				//completed callback
			}
		);
	}
	

	inStock(id: any , quantity, i){
		this._globalService.showLoaderSpinner(true);
		let post_data = {
			"warehouse_id": this.default_warehouse,
			"product_id": id,
			"stock": quantity
		}
		this._stockPriceService.in_Stock(post_data).subscribe(
			data => {
				if(data.status == 1){
					this.stock_list[i].real_stock = quantity;
					this.message = data.api_status[0];
					if(quantity == 0){
						this._globalService.showToastMessage('Product has been marked as out of stock');
					}else{
						this._globalService.showToastMessage('Product has been marked as instock');
					}
				}else{
					this._globalService.showToastMessage(this.message['message']);
				}
				this._globalService.showLoaderSpinner(false);
			},
			err => console.log(err),
			function() {
				//completed callback
			}
		);
	}

	// Category list

	load_category() {
        let data = {
            "model": "EngageboostCategoryMasters",
            "screen_name": "list",
            "userid": 1,
            "search": "",
            "order_by": "",
            "order_type": "",
            "status": "",
            "website_id": this._globalService.getWebsiteId(),
			"show_all": 1,
			"category_id": this.categoryList ? this.categoryList : ''
        }
        this._global.getWebServiceData('global_list', 'POST', data, '').subscribe(res => {
            if (res) {
                let resultSet = res[0].result;
                this.category_list = resultSet;
            } else {
                this._globalService.showToast('Something went wrong. Please try again.');
            }

        }, err => {
            console.log(err)
        })
    }

	// NEW fILTER END
	clearSearchData() {
		if(this.search_text == '') {
			this.reload(0, '', '', '', '');
		}
	}

	clearMe() {
		this.reload(0, '', '', '', '');
	}

	reload(reload: any, page: any, sortBy: any, filter: any, search: any) {
		// search = search.trimLeft();
		this._globalService.skeletonLoader(true);
		if(search == '' || search == null) {
			this.search_text = '';
		} else {
			this.search_text = search;
		}
		this.total_list = [];
		this.sortBy = sortBy;
		if (sortBy != '' && sortBy != undefined) {
			if (this.sortRev) {
				this.sortOrder = '-'
				this.sortRev = !this.sortRev;
				this.sortClass = 'icon-down';
			} else {
				this.sortOrder = '+'
				this.sortRev = !this.sortRev;
				this.sortClass = 'icon-up';
			}
		} else {
			this.sortBy = 'id'
			this.sortOrder = '+'
		}

		if (reload == 2) {
			this.search_text = '';
			this.hide_out_of_stock = false;
		} else {
			this.hide_out_of_stock = filter;
		}
		let data: any = {};
		data['warehouse_id'] = this.default_warehouse;
		data['order_by'] = this.sortBy;
		data['order_type'] = this.sortOrder;
		data['search'] = (this.search_text)?this.search_text.trim():'';
		data['hide_out_of_stock'] = (filter) ? 1 : 0;
		data['userid'] = this.userId;
		data["advanced_search"]= this.advanced_search;
		data['category_id'] = this.categoryList ? this.categoryList : '';
		this.total_list = [];
		this._stockPriceService.stockLoad(data, page).subscribe(
			data => {
				let myelement: HTMLElement = this.document.getElementsByClassName('autoclick');
				myelement[0].click();
				if (data.status == 0) { // this is for success response
					this.stock_list = [];
				} else {
					this.stock_list = data.results[0].result.product;
					this.permission = data.results[0].role_permission;
				}
				this.perPageCount = data.per_page_count;
				this.page = 1;
				// this._globalService.showLoaderSpinner(false);
				this._globalService.skeletonLoader(false);

			},
			err =>{
				console.log(err);
				// this._globalService.showLoaderSpinner(false);
				this._globalService.skeletonLoader(false);

			}
		);
	}

	dialogRefEditPrice: MatDialogRef <PriceComponent > | null;
	edit_price_pop(price: number, i: any, product_id: any) {
		this.dialogRefEditPrice = this.dialog.open(PriceComponent, {
			data : {"product_price" : price, "warehouseID" : this.default_warehouse, "product_id":product_id, "price_tye_id": 1},
			disableClose: false
		});
		this.dialogRefEditPrice.afterClosed().subscribe(result => {
			if(result != undefined){
				let price = result;
				this.stock_list[i].product_price = price;
			}	
		});
	}
}


@Component({
	templateUrl: './templates/price.html',
	providers: [StockPriceService, Global],
})
export class PriceComponent implements OnInit {
	public resdata: number;
	public stock_price: any;
	constructor(
		private _globalService: GlobalService,
		private _stockPriceService: StockPriceService,
		public dialogRef: MatDialogRef<PriceComponent>,
		public dialog: MatDialog, @Optional() @Inject(MAT_DIALOG_DATA) public data: any
	){

	}

	ngOnInit() {
		if(this.data.product_price>0){
			this.stock_price = this.data.product_price;
		}
	}

	saveEditPrice(stock: number){
		this._globalService.showLoaderSpinner(true);
		// call webserivcce for saving data into database 
		this.resdata = stock;
		let post_data = {
			"warehouse_id": this.data.warehouseID,
			"price_tye_id": 1,
			"price": this.stock_price,
			"product_id": this.data.product_id
		}
		this._stockPriceService.editPrice(post_data).subscribe(
			data => {
				if(data.status == 1){
					this._globalService.showToastMessage(data['message']);
				}else{
					this._globalService.showToastMessage(data['message']);
				}
				this._globalService.showLoaderSpinner(false);
			},
			err => console.log(err),
			function() {
				//completed callback
			}
		);
		this.dialogRef.close(this.resdata);
	} 

	closeDialog() {
		this.dialogRef.close();	
	}
}