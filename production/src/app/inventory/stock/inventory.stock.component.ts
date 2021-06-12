import {Component,OnInit,Inject} from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';
import {CookieService} from 'ngx-cookie';
import {PaginationInstance} from 'ngx-pagination';
import {DOCUMENT} from '@angular/platform-browser';
import { MatDialog,MatDialogRef,MAT_DIALOG_DATA } from '@angular/material';
import { StockService } from './inventory.stock.service';
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
  templateUrl: 'templates/stock-listing.html',
  providers: [StockService]
})
export class StockComponent implements OnInit {
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
	public default_warehouse: number;
	public hide_out_of_stock: boolean = false;
	public config: any = {};
	public total_list: any = [];
	public pagination: any = {};
	public pageIndex: number = 0;
	public pageList: number = 0;
	public page: number = 1;
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
	
	Advancefilter={};
	show_data:any=[];
	remove_field_index:number;
	exclude_arr:any=[];
	constructor(
		private _globalService: GlobalService,
		private _cookieService: CookieService,
		private _stockService: StockService,
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
		let websiteId = this._globalService.getWebsiteId();
		this._stockService.warehouseLoad(websiteId, this.userId).subscribe(
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
	}

	//SELECT TO STRAT
	private filterBanks() {
		if (!this.banks) {
		return;
		}
		// get the search keyword
		let search = this.bankFilterCtrl.value;
		if (!search) {
		this.filteredBanks.next(this.banks.slice());
		return;
		} else {
		search = search.toLowerCase();
		}
		// filter the banks
		this.filteredBanks.next(
		this.banks.filter(bank => bank.name.toLowerCase().indexOf(search) > -1)
		);
	}

	private filterBanksMulti() {
		if (!this.banks) {
			return;
		}
		// get the search keyword
		let search = this.bankMultiFilterCtrl.value;
		if (!search) {
			this.filteredBanksMulti.next(this.banks.slice());
			return;
		} else {
			search = search.toLowerCase();
		}
		// filter the banks
		this.filteredBanksMulti.next(
			this.banks.filter(bank => bank.name.toLowerCase().indexOf(search) > -1)
		);
	}
	// SELECT TO END
	callbackLoadStock(warehouse_id: number) {
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
		this.total_list = [];
		this._stockService.stockLoad(data, 1).subscribe(
			data => {
				this.stock_list = data.results[0].result.product;
				this.pagination.total_page = data.per_page_count;
				this.pageList = data.per_page_count;
				for (var i = 0; i < data.count; i++) {
					this.total_list.push(i);
				}
				this.config.currentPageCount = this.stock_list.length;
				this.config.currentPage = 1;
				this.config.itemsPerPage = data.page_size;
				this.permission = data.results[0].role_permission;
			},
			err => console.log(err),
			function() {
				//completed callback
			}
		);
	}
	// NEW fILTER END
	clearSearchData() {
		if(this.search_text == '') {
			this.callbackLoadStock(this.default_warehouse);
		}
	}
	toggleCheck(id: any, event: any) {
		let that = this;
		let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
		this.stock_list.forEach(function(item: any) {
			if (item.id == id) {
				item.selected = event.checked;
				if (item.selected) {
					elements[0].classList.add('show');
					that.selected_item = item;
				} else {
					elements[0].classList.remove('show');
					that.selected_item = {};
				}
			} else {
				item.selected = false;
			}
		});
		let myelement: NodeListOf < Element > = this.document.getElementsByClassName('action-box orderfilter');
		myelement[0].classList.remove('show');
	}

	updateGrid(isdefault: any) {
		this.global.doGridFilter('EngageboostPurchaseOrders', isdefault, this.cols, "list").subscribe(
			data => {
				this.response = data;
				this.reload(0, '', '', '', '');
			},
			err => console.log(err),
			function() {}
		);
	}

	reload(reload: any, page: any, sortBy: any, filter: any, search: any) {
		// search = search.trimLeft();
		this._globalService.skeletonLoader(true);
		if(this.search_text == '' || this.search_text == null) {
			this.search_text = '';
		} else {
			this.search_text = this.search_text;
		}
		let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
		elements[0].classList.remove('show');
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
		this.total_list = [];
		this._stockService.stockLoad(data, page).subscribe(
			data => {
				let myelement: HTMLElement = this.document.getElementsByClassName('autoclick');
				myelement[0].click();
				if (data.status == 0) { // this is for success response
					this.stock_list = [];
				} else {
					this.stock_list = data.results[0].result.product;
					this.pagination.total_page = data.per_page_count;
					this.pageList = data.per_page_count;
					for (var i = 0; i < data.count; i++) {
						this.total_list.push(i);
					}
					this.config.currentPageCount = this.stock_list.length;
					this.config.currentPage = page;
					this.config.itemsPerPage = data.page_size;
					this.permission = data.results[0].role_permission;
				}
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

	// NEW fILTER STRAT
	load_fiter_column(){
		let data:any={};
		data.model='EngageboostProductStocks';
		data.website_id=this._globalService.getWebsiteId();
		data.search= this.formModel.field_name;
		data.screen_name='list';
		data.exclude=this.exclude_arr;
		this.global.getWebServiceData('advanced_filter', 'POST', data, '').subscribe(res => {
			if (res.status == 1) {
				this.field_arr=res.api_status[0];
			}
		}, err => {
			this._globalService.showToast('Something went wrong');
		})
		
	}
	FiltertoggleCheck( event: any) {
		this.load_fiter_column();
		let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box orderfilter');
		elements[0].classList.add('show');
		this.formModel.update_key='';
	}
	CloseFilter(event: any){
		let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box orderfilter');
		elements[0].classList.remove('show');
		var element = this.document.getElementById('meta_keywordbox');
		element.classList.remove("show");
		this.advanced_search=[];
		this.formModel.field_name='';
		this.formModel.search_module = null;
		this.formModel.search_type = 1;
		this.formModel.search_data = null;
		this.reload(0, '', '', '', '');
		this.load_fiter_column();
		this.exclude_arr=[];
	}
	get_data(data :any,index:number){
		this.selectArr=[];
		var element = this.document.getElementById('meta_keywordbox');
		element.classList.add("show");
		this.formModel.field_name_show=data.columns;
		this.formModel.field_id=data.id;
		this.formModel.input_type=data.input_type;
		this.formModel.search_module=data.search_module;
		if(data.field_type=='int'){
			this.ConditionArr=[
				{'type':1,'name':'Equals to'},
				{'type':2,'name':'Not Equals to'}
			]
		}
		if(data.field_type=='float'){
			this.ConditionArr=[
				{'type':1,'name':'Equals to'},
				{'type':2,'name':'Not Equals to'},
				{'type':7,'name':'Geater than'},
				{'type':8,'name':'Less than'},
			]
		}
		if(data.field_type=='date'){
			this.ConditionArr=[
				{'type':1,'name':'Equals to'},
				{'type':2,'name':'Not Equals to'},
				{'type':7,'name':'Geater than'},
				{'type':8,'name':'Less than'},
			]
		}
		if(data.field_type=='string'){
			this.ConditionArr=[
				{'type':1,'name':'Equals to'},
				{'type':2,'name':'Not Equals to'},
				{'type':3,'name':'Starts with'},
				{'type':4,'name':'Ends with'},
				{'type':5,'name':'Contains'},
				{'type':6,'name':'Does not contains'}
			]
		}
		//this.field_arr.splice(index,1);
		this.get_select_data();
		this.load_fiter_column();
		this.remove_field_index=index;
		
	}
	sendSearchData(){
		var search_data='';
		search_data=this.formModel.search_data;
		if(search_data){
			if(this.formModel.search_data=='n'){
				search_data='Active';
			}
			if(this.formModel.search_data=='y'){
				search_data='Inactive';
			}
			if(this.formModel.input_type=='date'){
				this.formModel.search_data=this._globalService.convertDate(this.formModel.search_data, 'yyyy-MM-dd'); 
			}
			this.Advancefilter={'field':this.formModel.field_name,'comparer':this.formModel.search_type,'key':this.formModel.search_data,'name':this.formModel.field_name, 'show_name':this.formModel.field_name_show,'key2':this.formModel.update_key,'input_type':this.formModel.input_type,'field_id':this.formModel.field_id}
			this.advanced_search.push(this.Advancefilter);
			this.reload(0, '', '', '', '');
			let elements: NodeListOf < Element > = this.document.getElementsByClassName('meta_keywordbox');
			elements[0].classList.remove('show');
			this.selectArr=[];
			this.formModel.search_data=null;
			this.formModel.search_module=null;
			this.formModel.update_key=this.formModel.search_data;
			this.formModel.field_name='';
			this.formModel.search_type=1;
			this.show_data=[];
			// form.reset();
			// this.load_fiter_column(); 
			this.formModel.temp_name='';
			this.get_select_data();
			// this.filteredBanksMulti=null;remove_field_index
			let exclude_id=this.field_arr[this.remove_field_index].id;
			this.exclude_arr.push(exclude_id);
			this.field_arr.splice(this.remove_field_index,1);
		} else {
			this._globalService.showToast('Please enter value');
		}
	}
	change_search_val(item:any){
		if(this.formModel.input_type=='multi_select'){
			if(this.show_data.includes(item)){
			} else {
				this.show_data.push(item);
			}
			let data=this.show_data.join();
			
			this.formModel.update_key=data;
		}else{

			this.formModel.update_key=item;
		}
		this.formModel.temp_name=item;
	}
	remove_filter(index:number){
		let remove_val=this.advanced_search.splice(index,1);
		const items = this.exclude_arr;
		const valueToRemove = remove_val[0].field_id;
		this.exclude_arr = items.filter(item => item !== valueToRemove)  
		this.reload(0, '', '', '', '');
	}
	show_options(){
		this.search_type_option=true;
	}
	cancel_filter() {
		let elements: NodeListOf < Element > = this.document.getElementsByClassName('meta_keywordbox');
		elements[0].classList.remove('show');  
		this.reload(0, '', '', '', '');
		this.formModel.field_name='';
		this.formModel.temp_name='';
		this.formModel.search_data = null;
		this.load_fiter_column();

	}
	get_select_data(){
		this.global.getWebServiceData('global_list/'+this.formModel.field_id, 'GET', '', '').subscribe(res => {
			if(res){
				if(res.status!=0){
					this.banks=res.results[0].result[0];
					//SELECT TO START
					this.bankCtrl.setValue(this.banks[10]);
					this.filteredBanks.next(this.banks.slice());
					this.filteredBanksMulti.next(this.banks.slice());
					this.bankFilterCtrl.valueChanges
					.pipe(takeUntil(this._onDestroy))
					.subscribe(() => {
						this.filterBanks();
					});
					this.bankMultiFilterCtrl.valueChanges
					.pipe(takeUntil(this._onDestroy))
					.subscribe(() => {
						this.filterBanksMulti();
					});
					//SELECt END
					this.selectArr=res.results[0].result[0];
				}else{
					this.banks=this.selectArr;
					//SELECT TO START
					this.bankCtrl.setValue(this.banks[10]);
					this.filteredBanks.next(this.banks.slice());
					this.filteredBanksMulti.next(this.banks.slice());
					this.bankFilterCtrl.valueChanges
					.pipe(takeUntil(this._onDestroy))
					.subscribe(() => {
						this.filterBanks();
					});
					this.bankMultiFilterCtrl.valueChanges
					.pipe(takeUntil(this._onDestroy))
					.subscribe(() => {
						this.filterBanksMulti();
					});
					//SELECt END
				}
			}
		}, err => {
			this.selectArr=[];
		})
	}
	// NEW fILTER END
	dialogManageStockRef: MatDialogRef < StockAddEditComponent > | null;
	manageStock(action) {
		let that = this;
		let data: any = {};
		data['product_id'] = this.selected_item.id;
		data['action'] = action;
		data['warehouse_id'] = this.default_warehouse;
		data['qty'] = this.selected_item.qty;
		data['safety_stock'] = this.selected_item.safety_stock;
		this.dialogManageStockRef = this.dialog.open(StockAddEditComponent, {
			data: data
		});
		this.dialogManageStockRef.afterClosed().subscribe(result => {
			if (result) {
				this.reload(1, 1, '', '', '');
			}
		});
	}

	dialogMoveStockRef: MatDialogRef < StockMoveComponent > | null;
	moveStock() {
		let that = this;
		let data: any = {};
		data['product_id'] = this.selected_item.id;
		data['from_location'] = this.default_warehouse;
		data['qty'] = this.selected_item.qty;
		data['safety_stock'] = this.selected_item.safety_stock;

		this.dialogMoveStockRef = this.dialog.open(StockMoveComponent, {
			data: data
		});
		this.dialogMoveStockRef.afterClosed().subscribe(result => {
			if (result) {
				this.reload(1, 1, '', '', '');
			}
		});
	}

	dialogSafetyStockRef: MatDialogRef < SafetyStockComponent > | null;
	safetyStock() {
		let that = this;
		let data: any = {};
		data['product_id'] = this.selected_item.id;
		data['warehouse_id'] = this.default_warehouse;
		data['safety_stock'] = this.selected_item.safety_stock;
		data['qty'] = this.selected_item.qty;
		this.dialogSafetyStockRef = this.dialog.open(SafetyStockComponent, {
			data: data
		});
		this.dialogSafetyStockRef.afterClosed().subscribe(result => {
			if (result) {
				this.reload(1, 1, '', '', '');
			}
		});
	}

	dialogImportStockRef: MatDialogRef < ImportStockComponent > | null;
	openImportBox() {
		let that = this;
		let data: any = {};
		this.dialogImportStockRef = this.dialog.open(ImportStockComponent, {
			data: 'import_file'
		});
		this.dialogImportStockRef.afterClosed().subscribe(result => {
			if (result) {
				this.reload(1, 1, '', '', '');
			}
		});
	}

	exportStockRequest() {
		this._globalService.showLoaderSpinner(true);
		let data:any = {}
		data.warehouse_id = this.default_warehouse;
		data.hide_out_of_stock = this.hide_out_of_stock ? 1 : 0;
		this.global.getWebServiceData("export-product-stock", "POST", data,'').subscribe(
			res=>{
				if(res.status == 1){
					let fileNBase = window.location.protocol + '//' + window.location.hostname + ':' + GlobalVariable.apiPort+'/';
					var url = fileNBase + res['export_file_path'];
					var a = document.createElement("a");
					a.href = url;
					a.download = res.file;
					document.body.appendChild(a);
					a.click();
					document.body.removeChild(a);
					// this._globalService.showToast(res.message);
				}
				this._globalService.showLoaderSpinner(false);
			} , err =>{

			}
		)
	}

	dialogRefColumnLayout: MatDialogRef<ColumnLayoutComponent> | null;
	loadColumnLayout() {
		let data: any = {}
		data["column"] = this.cols;
		data["layout"] = this.layout;
		this.dialogRefColumnLayout = this.dialog.open(ColumnLayoutComponent, { data: data });
		this.dialogRefColumnLayout.afterClosed().subscribe(result => {
			if(result != undefined) {
				this.cols = result;
				this.updateGrid(0);
			}
			
			
		});
	}
}

@Component({
	templateUrl: 'templates/manage-stock.html',
	providers: [StockService]
})
export class StockAddEditComponent implements OnInit {
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public previous_stock: number;
	public previous_safety: number;
	public minDate: any;
	public warehouse_list: any = [];
	public supplier_list: any = [];
	public popupLoder: boolean = false;	
	constructor(
		private _globalService: GlobalService,
		private _stockService: StockService,
		public dialog: MatDialog,
		private dialogRef: MatDialogRef < StockAddEditComponent > , @Inject(MAT_DIALOG_DATA) public data: any
	) {
		this.formModel = Object.assign({}, this.data);
		this.minDate = new Date();
		this.previous_stock = this.data.qty;
		this.previous_safety = this.data.safety_stock;
	}

	ngOnInit() {
		let websiteId = this._globalService.getWebsiteId();
		this._stockService.warehouseLoad(websiteId, this._globalService.getUserId()).subscribe(
			data => {
				this.warehouse_list = data.warehouse;
			},
			err => console.log(err),
			function() {
				//completed callback
			}
		);

		if (this.formModel.qty == 0) this.formModel.qty = '';
		this._stockService.manageStockLoad().subscribe(
			data => {
				//this.warehouse_list = data.warehouse;
				this.supplier_list = data.Suppliers;
				this.formModel.received_purchaseorder_id = data.received_code;
				this.formModel.received_date = new Date();
			},
			err => console.log(err),
			function() {
				//completed callback
			}
		);
	}

	closeDialog() {
		this.dialogRef.close();
	}

	calcTotAmt() {
		if (this.formModel.cost > 0 && this.formModel.qty > 0) {
			this.formModel.tot_amt = parseFloat(this.formModel.cost) * parseFloat(this.formModel.qty);
		} else {
			this.formModel.tot_amt = 0;
		}
	}

	manageStock(form) {
		if (this.formModel.action == 'Decrease' && this.formModel.qty > (this.previous_stock - this.formModel.safety_stock)) {
			this.errorMsg = 'Please put quantity less than real stock.';
		} else if (this.formModel.action == 'Increase' && ((this.formModel.qty + this.previous_stock) - this.formModel.safety_stock) < 0) {
			this.errorMsg = 'Real stock must be greater or equal to zero.';
		} else {
			this.popupLoder = true;
			this.errorMsg = '';
			var data: any = {};
			data = Object.assign({}, this.formModel);
			data.action = data.action.toLowerCase();
			data.website_id = this._globalService.getWebsiteId();
			data.createdby = this._globalService.getUserId();
			let that = this;
			this._stockService.stockAdjustment(data).subscribe(
				data => {
					let response = data;
					if (response) {
						that.dialogRef.close('success');
					} else {
						this.errorMsg = data.message;
					}
					this.popupLoder = false;
				},
				err => console.log(err),
				function() {
					//completed callback
				}
			);
		}
	}
}

@Component({
	templateUrl: 'templates/move-stock.html',
	providers: [StockService]
})
export class StockMoveComponent implements OnInit {
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public previous_stock: number;
	public previous_safety: number;
	public minDate: any;
	public warehouse_list: any = [];
	public popupLoder: boolean = false;
	constructor(private _globalService: GlobalService,
		private _stockService: StockService,
		public dialog: MatDialog,
		private dialogRef: MatDialogRef < StockMoveComponent > , @Inject(MAT_DIALOG_DATA) public data: any
	) {
		this.formModel = Object.assign({}, this.data);
		this.minDate = new Date();
		this.previous_stock = this.data.qty;
		this.previous_safety = this.data.safety_stock;
	}

	ngOnInit() {
		if (this.formModel.qty == 0) this.formModel.qty = '';
		this._stockService.manageStockLoad().subscribe(
			data => {
				this.warehouse_list = data.warehouse;
				this.formModel.received_date = new Date();
				this.formModel.received_code = data.received_code;
			},
			err => console.log(err),
			function() {
				//completed callback
			}
		);
	}

	closeDialog() {
		this.dialogRef.close();
	}

	moveStock(form) {
		if (this.formModel.qty > (this.previous_stock - this.previous_safety)) {
			this.errorMsg = 'Please put quantity less than real stock quantity.';
		} else {
			this.popupLoder = true;
			this.errorMsg = '';
			var data: any = {};
			data = Object.assign({}, this.formModel);
			data.createdby = this._globalService.getUserId();
			this._stockService.stockMove(data).subscribe(
				data => {
					if (data.status) {
						this.dialogRef.close('success');
					} else {
						this.errorMsg = data.message;
					}
					this.popupLoder = false;
				},
				err => console.log(err),
				function() {
					//completed callback
				}
			);
		}
	}
}

@Component({
	templateUrl: 'templates/manage-safety-stock.html',
	providers: [StockService]
})
export class SafetyStockComponent implements OnInit {
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public popupLoder: boolean = false;
	constructor(private _globalService: GlobalService,
		private _stockService: StockService,
		public dialog: MatDialog,
		private dialogRef: MatDialogRef < SafetyStockComponent > , @Inject(MAT_DIALOG_DATA) public data: any
	) {
		this.formModel = Object.assign({}, this.data);
	}

	ngOnInit() {
		this.formModel.safety_stock = (this.formModel.safety_stock) ? this.formModel.safety_stock : 0;
		// console.log(this.data);
	}

	closeDialog() {
		this.dialogRef.close();
	}

	updateSafetyStock(form) {
		if ((this.formModel.qty - this.formModel.safety_stock) < 0) {
			this.errorMsg = 'Real stock must be greater equal to zero.';
		} else {
			this.popupLoder = true;
			this.errorMsg = '';
			var data: any = {};
			data = Object.assign({}, this.formModel);
			data.updatedby = this._globalService.getUserId();

			this._stockService.safetyStockUpdate(data).subscribe(
				data => {
					if (data.status) {
						this.dialogRef.close('success');
					} else {
						this.errorMsg = data.message;
					}
					this.popupLoder = false;
				},
				err => console.log(err),
				function() {
					//completed callback
				}
			);
		}
	}
}

@Component({
	templateUrl: 'templates/import-stock-file.html',
	providers: [StockService]
})
export class ImportStockComponent implements OnInit {
	public errorMsg: string = '';
	public formModel: any = {};
	public sample_xls: any;
	public sample_csv: any;
	public file_data: any;
	public website_id_new: any;
	public company_id_new: any;
	public importOpt: any;
	public file_selection_tool: any;
	public popupLoder: boolean = false;
	constructor(private _globalService: GlobalService,
		private _stockService: StockService,
		public dialog: MatDialog,
		private dialogRef: MatDialogRef < ImportStockComponent > , @Inject(MAT_DIALOG_DATA) public data: any
	) {
		this.formModel = Object.assign({}, this.data);
	}

	ngOnInit() {
		this.sample_xls = window.location.protocol + '//' + window.location.hostname + ':8062' + '/media/importfile/sample/stock_import.xls';
		this.sample_csv = window.location.protocol + '//' + window.location.hostname + ':8062' + '/media/importfile/sample/stock_import.csv';
		this.importOpt = 'xls';
		this.file_selection_tool = 'No file choosen';
	}

	importStockFileXLS(e: Event) {
		let files: any = {};
		let target: HTMLInputElement = e.target as HTMLInputElement;
		for (let i = 0; i < target.files.length; i++) {
			let file_arr: any = [];

			let reader = new FileReader();
			reader.readAsDataURL(target.files[i]);
			reader.onload = (event) => {
				file_arr['url'] = event.srcElement['result']
			}
			file_arr['_file'] = target.files[i];
			files[this.data] = file_arr;
		}
		var filename = files.import_file._file.name;
		this.file_selection_tool = filename;
		this.file_data = files.import_file._file;
		console.log(this.file_data);
		let extn = filename.split(".").pop();
		if (extn == 'xls' || extn == 'xlsx') {
			//this.dialogRef.close(files);
		} else {
			this._globalService.showToast('Please choose XLS/XLSX file');
		}
	}

	closeDialog() {
		this.dialogRef.close();
	}

	saveFileDataImport(form: any) {
		this.popupLoder = true;
		this.website_id_new = this._globalService.getWebsiteId();
		this.company_id_new = this._globalService.getCompanyId();
		var form_data = new FormData();
		form_data.append("import_file", this.file_data);
		form_data.append('website_id', this.website_id_new);
		form_data.append('company_id', this.company_id_new);
		if (this.file_data != undefined) {
			this._stockService.SaveStockFileData(form_data).subscribe(
				data => {
					this.popupLoder = false;
					this._globalService.showToast('We have taken your file. we will update your stock and notify you via email.');
					this.dialogRef.close();
				},
				err => console.log(err),
				function () {
					//completed callback
				}
			);
		} else {
			this._globalService.showToast('Please choose XLS/XLSX file');
			this.popupLoder = false;
		}        
	}
}