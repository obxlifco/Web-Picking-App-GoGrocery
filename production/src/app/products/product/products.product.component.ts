import { Component, ElementRef, OnInit, Input, Inject, AfterViewInit, Optional } from '@angular/core';
import { Global } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';
import { Router, ActivatedRoute } from '@angular/router';
import { CookieService} from 'ngx-cookie';
import { DomSanitizer } from '@angular/platform-browser';
import { PaginationInstance } from 'ngx-pagination';
import { DialogsService } from '../../global/dialog/confirm-dialog.service'; 
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { DOCUMENT } from '@angular/platform-browser';
import { ProductService } from './products.product.service';
import { GlobalVariable } from '../../global/service/global';
import { AddEditTransition, AddEditStepFlipTransition } from '../.././addedit.animation';
import { ImportProductPriceImportComponent } from './products.product.addedit.component';
import { ColumnLayoutComponent } from '../../global/grid/app.grid-global.component';
import { ViewChild } from '@angular/core';
import { VERSION } from '@angular/material';
import { FormControl } from '@angular/forms';
import { MatSelect } from '@angular/material';
import * as pluginAnnotations from 'chartjs-plugin-annotation';
import { ChartOptions } from 'chart.js';
import { Color} from 'ng2-charts';
import * as moment from 'moment';
import { Subject } from 'rxjs';
import { take, takeUntil } from 'rxjs/operators';
import { ReplaySubject } from 'rxjs';
import { DashboardService } from '../../dashboard/dashboard.service';
import { OrderService } from '../../order/order/order.order.service';
interface Bank {
	id: string;
	name: string;
   }
@Component({
	selector: 'my-app',
	templateUrl: `./templates/product.html`,
	providers: [Global, ProductService],
})
export class ProductComponent implements OnInit, AfterViewInit {
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
	constructor(
		private globalService: GlobalService,
		private global: Global,
		private _router: Router,
		private sanitizer: DomSanitizer,
		private dialogsService: DialogsService,
		private elRef: ElementRef,
		private _cookieService: CookieService,
		public dialog: MatDialog,
		private _productService: ProductService,
		@Inject(DOCUMENT) private document: any
	) {}
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public bulk_ids: any = [];
	public pagination: any = {};
	public pageIndex: number = 0;
	public pageList: number = 0;
	public sortBy: any = '';
	public sortOrder: any = '';
	public sortClass: any = '';
	public sortRev: boolean = false;
	public selectedAll: any = false;
	public stat: any = {};
	public result_list: any = [];
	public total_list: any = [];
	public cols: any = [];
	public layout: any = [];
	public add_btn: string;
	public post_data = {};
	public searchData:any = {};
	page: number = 1;
	public filter: string = '';
	
	public maxSize: number = 10;
	public directionLinks: boolean = true;
	public autoHide: boolean = false;
	public config: any = {};
	public permission: any = [];
	public show_btn: any = {
		'add': true,
		'edit': true,
		'delete': true,
		'block': true
	};
	public userId: any;
	public individualRow: any = {};
	public search_text: any;
	public childData: any = {};
	public show_variant_product: boolean = true;
	public colSpanCount: number = 8;
	public tabIndex: number;
	public parentId: number = 0;
	showSkeletonLoaded: boolean = false;
	public temp_result=[];
	public temp_col=[];
	public selectedTabIndex: number = 0;
	public formModel: any = {};

	public field_arr : any=[];
	ConditionArr=[];
	filterArr=[];
	public search_type_option=false;
	advanced_search=[];
	input_type:any;
	selectArr:any=[];
	temp_key:any=[];
	advanced_search_temp=[];
	// filter={};
	Advancefilter={};
	order_information:any=[];
	item_information:any=[];
	customer_information:any=[];
	delivery_information:any=[];
	other_information:any=[];
	order_summary_information:any=[];
	show_data:any=[];
	remove_field_index:number;
	exclude_arr:any=[];
	public warehouse_id: any;
	public isSuperAdmin:any;
	//////////////////////////Initilise////////////////////////////
	ngOnInit() {
		this.tabIndex = +this.globalService.getCookie('active_tabs');
		this.parentId = this.globalService.getParentId(this.tabIndex);
		let userData = this._cookieService.getObject('userData');
		
		this.userId = userData['uid'];
		this.warehouse_id = userData['warehouse_id'];
		
		this.childData = {
			table: 'EngageboostProducts',
			heading: 'Product',
			ispopup: 'N',
			tablink: 'products',
			screen: 'list',
			is_import: 'Y',
			is_export: 'Y',
			tabparrentid: this.parentId,
		}
		this.generateGrid(0, '', '', '', '', 1);
  //       this.globalService.loadSkeletonChange$.subscribe(
		// 	(value) => {
		// 		this.showSkeletonLoaded = value;
		// 	}
		// );
		for (let i = 0; i < 15; i++) {
			this.temp_result.push(i);
		}
		for (let i = 0; i < 5; i++) {
			this.temp_col.push(i);
		}
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

	ngAfterViewInit(){
		this.globalService.skeletonLoader(true);
	}

	onChange(event) {
		if (event != undefined) {
			let index = 0;
			this.field_arr.forEach((element: any, key: any) => {
				if (element.field == event.field) {
					this.get_data(event, key);
				}
			})
		}
	}
	
	/////////////////////////Grid//////////////////////////////////////////////
	generateGrid(reload: any, page: any, sortBy: any, filter: any, search: any, show_variant_product: any) {

		let userData = this._cookieService.getObject('userData');
		let websiteId  = this.globalService.getWebsiteId();
		var page_size = 0;
		this.globalService.skeletonLoader(true);
		let filterQuery = [];
		let filterQuery2 = [];
		if(search == '' || search == null) {
			this.search_text = '';
			search = '';
		} else {
			this.search_text = search;
			if(search) {
				search = search.trim();
			}
		}
		let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
		elements[0].classList.remove('show');
		this.bulk_ids = [];
		this.individualRow = {};
		this.total_list = [];
		this.selectedAll = false;
		this.filter = filter;
		this.show_variant_product = show_variant_product;
		var visibility_id: any;
		if(this.show_variant_product) {
			//visibility_id = 4; // 
		} else {
			visibility_id = 1; // for parent product only
		}
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
			this.sortBy = sortBy;
		}
		
		this.post_data = {
			"model": this.childData.table,
			"screen_name": this.childData.screen,
			"userid": this.userId,
			"warehouse_id": this.formModel.default_warehouse,
			"visibility_id": visibility_id
		}
		// ELSATIC QUERY GENERATION START
		this.advanced_search.forEach(element => {
			//console.log(element);
			let search_field=element.field;
			let input_type=element.input_type;
			let search_value=element.key;
			var match='match';
			if(search_field=='delivery_email_address'){
				match='match_phrase_prefix';
			}
			if(element.comparer==1){
				if(input_type=='multi_select' ){
					match='terms';
					filterQuery.push({[match]: {[search_field] : search_value}});
				} else {
					filterQuery.push({[match]: {[search_field] : search_value}});
				}
			}
			if(element.comparer==2){
				if(input_type=='multi_select' ){
					match='terms';
					filterQuery2.push({[match]: {[search_field] : search_value}});
				} else {
					filterQuery2.push({[match]: {[search_field] : search_value}});
				}
			}
			if(element.comparer==3){
				filterQuery.push({ match_phrase_prefix: {[search_field] : search_value}});
			}
			if(element.comparer==4){
				filterQuery.push({ wildcard: {[search_field+'.keyword'] : '*'+search_value}});
			}
			if(element.comparer==5){
				filterQuery.push({ wildcard: {[search_field+'.keyword'] : '*'+search_value+'*'}});
			}   
			if(element.comparer==6){
				filterQuery2.push({ wildcard: {[search_field+'.keyword'] : '*'+search_value+'*'}});
			}
			if(element.comparer==7){ 
				if(search_field=='time_slot_date' || search_field=='created'){
					let d=this.globalService.convertDate(search_value, 'yyyy-MM-dd'); 
					let elasticData = {"range":{[search_field]:{"gte": d}}}
					filterQuery.push(elasticData);
				} else {
					filterQuery.push({"range":{[search_field]:{"gte": search_value}}});
				}
			}
			if(element.comparer==8) {
				if(search_field=='time_slot_date' || search_field=='created') {
					let d=this.globalService.convertDate(search_value, 'yyyy-MM-dd'); 
					let elasticData = {"range":{[search_field]:{"lte": d}}}
					filterQuery.push(elasticData);
				} else {
					filterQuery.push({"range":{[search_field]:{"lte": search_value}}});
				}
			}
		});

		// ELSATIC QUERY GENERATION END
		let matchArr = [];
		let termQuery = {};
		/////////////// loading default conditions for grid /////////////////
		let conditions:any = {}
		conditions.isdeleted = 'n';
		let innerMatch:any = {};
		innerMatch.match = conditions;
		matchArr.push(innerMatch);
		if(filter != '') {
			conditions = {}
			conditions.isblocked = this.filter;
			innerMatch = {};
			innerMatch.match = conditions;
			matchArr.push(innerMatch);
		}

		if(filterQuery && filterQuery.length > 0) {
			//console.log(filterQuery);
			matchArr = matchArr.concat(filterQuery);
		}

		if(!this.show_variant_product) {
			conditions = {}
			conditions.visibility_id =  'Catalog Search';
			innerMatch = {};
			innerMatch.match = conditions;
			matchArr.push(innerMatch);
		}
		
		if( websiteId != 1) {
			conditions = {}
			conditions.website_id =  websiteId;
			innerMatch = {};
			innerMatch.match = conditions;
			matchArr.push(innerMatch);
		}
		
		if(search != '') { // pushing search conditions
			//console.log("************ Search data ****************",search);
			search = search.replace("/", "\\", search);
			
			/*termQuery = {'name':search};*/
			//shouldArr.push(termQuery);
			conditions = {}
			conditions.query = search;
			innerMatch = {};
			innerMatch.query_string = conditions;
			matchArr.push(innerMatch);
		}
		// Warewouse conidition by cds......
		if(this.warehouse_id && this.warehouse_id > 0) {
			conditions = {'category_warehouse.id':this.warehouse_id}
			innerMatch = {};
			innerMatch.match = conditions;
			matchArr.push(innerMatch);
		}
		// Warewouse conidition by cds......
		this.globalService.skeletonLoader(true);
		let that = this;
		this.global.loadColumnVisibility(this.post_data).subscribe( data => {
			this.response = data;
			// this.cols = this.response.results[0].layout;
			this.cols = this.response.results[0].applied_layout;
			this.colSpanCount = this.cols.length;
			this.pageList = this.response.per_page_count;
			this.stat.active = this.response.results[0].active;
			this.stat.inactive = this.response.results[0].inactive;
			this.stat.all = this.response.results[0].all;
			this.add_btn = this.response.results[0].add_btn;
			this.permission = this.response.results[0].role_permission;
			page_size = this.response.page_size;
			///// startig query string filer ////////////////
			if(this.sortBy != 'id') {
				sortBy = this.sortBy + '.keyword';
			}
			if (this.sortBy == '') {
				sortBy = 'id';
			}
			let orderType = 'asc';
			if (this.sortOrder == '+') {
				orderType = 'asc'
			} else {
				orderType = 'desc'
			}
			let from = 0;
			if (page <= 0 || page == '') {
				page = 1;
				from = 0;
			} else {
				let start = page - 1;
				from = start * this.response.page_size;
				//from = from - 1;
			}
			if (from  < 0) {
				from = 0;
			}
			let extraFilter = JSON.stringify(matchArr);
			let extraFilter2 = JSON.stringify(filterQuery2);
			termQuery = JSON.stringify(termQuery);
			let booleanFilter = {};
			/*booleanFilter['must'] = extraFilter;
			booleanFilter['must_not'] = extraFilter;*/


			//let shouldFilter = JSON.stringify(shouldArr);
			let elasticData = '{"query":{"bool":{"must":' + extraFilter + ', "must_not":' + extraFilter2 +'}},"from": ' + from + ',"size": ' + page_size+',"sort": [{"' + sortBy + '": "' + orderType + '"}]}';
			elasticData = JSON.parse(elasticData);
			this._productService.loadGrid('products', page, search, page_size, sortBy, show_variant_product, this.sortOrder, elasticData, websiteId).subscribe(listData => {
				let tmpResult = [];
				this.result_list = [];
				listData.hits.hits.forEach(function(rows: any) {
					tmpResult.push(rows._source);
				});
				this.response.results[0].result = tmpResult;
				if (tmpResult.length > 0) {
					this.result_list = this.response.results[0].result;
					this.result_list.forEach(function(item: any) {
						if (item.isblocked == 'n') {
							item.isblocked = 'Active';
						} else {
							item.isblocked = 'Inactive';
						}
					})
					//console.log(this.result_list);
					if (userData['elastic_host'] == '50.16.162.98') {  // this is for new elsatic server
						listData.hits.total = listData.hits.total.value;
					}
					for (var i = 0; i < listData.hits.total; i++) {
						this.total_list.push(i);
					}
				} else {
					this.result_list = [];
				}
				this.pagination.total_page = Math.ceil(listData.hits.total/page_size);
				if(this.pagination.total_page >= 0){
					this.pagination.total_page= this.pagination.total_page;
				} else {
					this.pagination.total_page=0;
				}
				//console.log(listData.hits.total + " ===  " + this.response.page_size+ "===" +this.pagination.total_page);
				this.config.currentPageCount = this.result_list.length
				this.config.currentPage = page
				this.config.itemsPerPage = page_size;
				//console.log(this.config);
				this.globalService.skeletonLoader(false);
				let myelement: HTMLElement = this.document.getElementsByClassName('autoclick');
				myelement[0].click();
			}, err => {
				this.globalService.skeletonLoader(false);

			});
		}, err => {
			that.globalService.skeletonLoader(false);
		   },
		   function(){
			   that.globalService.skeletonLoader(false);
		   }
		);
		/*
		this.post_data = {
			"model": this.childData.table,
			"screen_name": this.childData.screen,
			"userid": this.userId,
			"search": search,
			"order_by": sortBy,
			"order_type": this.sortOrder,
			"status": filter,this.formModel.search_type=1;
		this.formModel.search_data='';
		this.formModel.temp_name='';
			"visibility_id": visibility_id
		}
		this._productService.doGrid(this.post_data, page).subscribe(
			data => {
				this.response = data;
				if (this.response.count > 0) {
					this.result_list = this.response.results[0].result;
					this.result_list.forEach(function(item: any) {
						if (item.isblocked == 'n') {
							item.isblocked = 'Active';
						} else {
							item.isblocked = 'Inactive';
						}

					})
					for (var i = 0; i < this.response.count; i++) {
						this.total_list.push(i);
					}

				} else {
					this.result_list = [];
				}

				this.cols = this.response.results[0].layout;
				this.colSpanCount = this.cols.length;
				this.pagination.total_page = this.response.per_page_count;
				this.pageList = this.response.per_page_count;
				this.stat.active = this.response.results[0].active;
				this.stat.inactive = this.response.results[0].inactive;
				this.stat.all = this.response.results[0].all;
				this.add_btn = this.response.results[0].add_btn;
				this.config.currentPageCount = this.result_list.length
				this.config.currentPage = page
				this.config.itemsPerPage = this.response.page_size;
				this.permission = this.response.results[0].role_permission;
				this.globalService.showLoaderSpinner(false);
			},
			err => console.log(err),
			function() {}
		); */
	}

	////////////////////////Delete/Block/Unblock///////////////////////////////

	updateStatusAll(type: number, id: number) {
		let that = this;
		if (id) {
			that.bulk_ids = [];
			that.bulk_ids.push(id);
		}
		if (type == 2) {
			var msg = 'Do you really want to delete selected records?';
			var perm = this.permission.delete;
			var msgp = 'You have no permission to delete!';
		} else if (type == 1) {
			var msg = 'Do you really want to block selected records?';
			var perm = this.permission.block;
			var msgp = 'You have no permission to block!';
		} else {
			var msg = 'Do you really want to unblock selected records?';
			var perm = this.permission.block;
			var msgp = 'You have no permission to unblock!';
		}
		if (perm == 'Y') {
			if (this.bulk_ids.length > 0) {
				this.dialogsService.confirm('Warning', msg).subscribe(res => {
					if (res) {
						this.global.doStatusUpdate(this.childData.table, this.bulk_ids, type).subscribe(
							data => {
								this.response = data;
								setTimeout(() => {
									this.globalService.showToast(this.response.Message);
									that.generateGrid(0, '', '', '', '', 1);
								},300);
							},
							err => console.log(err),
						);
					}
				});
			} else {
				this.dialogsService.alert('Error', 'Select Atleast One Record!').subscribe(res => {});
			}
		} else {
			this.dialogsService.alert('Permission Error', msgp).subscribe(res => {});
		}
	}
	////////////////////////////Check/Uncheck//////////////
	toggleCheckAll(event: any) {
		let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
		let that = this;
		that.bulk_ids = [];
		this.selectedAll = event.checked;
		this.result_list.forEach(function(item: any) {
			item.selected = event.checked;
			if (item.selected) {
				that.bulk_ids.push(item.id);
				elements[0].classList.add('show');
			} else {
				elements[0].classList.remove('show');
			}
		});
		let myelement: NodeListOf < Element > = this.document.getElementsByClassName('action-box orderfilter');
		myelement[0].classList.remove('show');
	}
	toggleCheck(id: any, event: any) {
			let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
			let that = this;
			//that.bulk_ids=[];
			this.result_list.forEach(function(item: any) {
				if (item.id == id) {
					item.selected = event.checked;
					if (item.selected) {
						that.bulk_ids.push(item.id);
						elements[0].classList.add('show');
					} else {
						var index = that.bulk_ids.indexOf(item.id);
						that.bulk_ids.splice(index, 1);
						if (that.bulk_ids.length == 0) {
							elements[0].classList.remove('show');
						}
					}
				}
				if (that.bulk_ids.length == 1) {
					that.bulk_ids.forEach(function(item_id: any) {
						if (item_id == item.id) {
							that.individualRow = item;
						}
					});
				}
				that.selectedAll = false;
			});
		let myelement: NodeListOf < Element > = this.document.getElementsByClassName('action-box orderfilter');
		myelement[0].classList.remove('show');
	}

	 // NEW fILTER STRAT
	load_fiter_column(){
		let data:any={};
		data.model=this.childData.table;
		data.website_id=this.globalService.getWebsiteId();
		data.search= this.formModel.field_name;
		data.screen_name=this.childData.screen;
		data.exclude=this.exclude_arr;
		this.global.getWebServiceData('advanced_filter', 'POST', data, '').subscribe(res => {
			if (res.status == 1) {
				this.field_arr=res.api_status[0];
			}
		}, err => {
			this.globalService.showToast('Something went wrong');
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
		this.generateGrid(0, '', '', '', '',this.show_variant_product);
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
		this.load_fiter_column();
		this.get_select_data();
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
				this.formModel.search_data=this.globalService.convertDate(this.formModel.search_data, 'yyyy-MM-dd'); 
			}
			this.Advancefilter={'field':this.formModel.field_name,'comparer':this.formModel.search_type,'key':this.formModel.search_data,'name':this.formModel.field_name, 'show_name':this.formModel.field_name_show,'key2':this.formModel.update_key,'input_type':this.formModel.input_type,'field_id':this.formModel.field_id}
			this.advanced_search.push(this.Advancefilter);
			this.generateGrid(0, '', '', '', '',this.show_variant_product);
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
			// console.log('Working3');
			// this.filteredBanksMulti=null;remove_field_index
			let exclude_id=this.field_arr[this.remove_field_index].id;
			this.exclude_arr.push(exclude_id);
			this.field_arr.splice(this.remove_field_index,1);
			// console.log(this.field_arr);
		} else {
			this.globalService.showToast('Please enter value');
		}
		
	}
	change_search_val(item:any){
		if(this.formModel.input_type=='multi_select'){
			if(this.show_data.includes(item)){
				console.log('Already in');
			}else{
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
		// console.log(this.exclude_arr);
		this.generateGrid(0, '', '', '', '',this.show_variant_product);
	}
	show_options(){
		this.search_type_option=true;
	}
	cancel_filter() {
		let elements: NodeListOf < Element > = this.document.getElementsByClassName('meta_keywordbox');
		elements[0].classList.remove('show');  
		this.generateGrid(0, '', '', '', '',this.show_variant_product);
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
					// let myelement: HTMLElement = this.document.getElementsByClassName('autoclick');
					// myelement[0].click();
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
	/////////////////////////Filter Grid//////////////////////
	updateGrid(isdefault: any) {
		this._productService.doGridFilter(this.childData.table, isdefault, this.cols, "list").subscribe(
			data => {
				this.response = data;
				this.generateGrid(0, '', '', '', '', 1);
			},
			err => console.log(err),
		);
	}

	dialogRefImportProducts: MatDialogRef < ImportProductComponent > | null;
	openProductImport(id: any, importType: any) {
		if (this.childData.table == 'EngageboostProducts') {
			let tmpData: any = {};
			tmpData["import_file"] = 'import_file';
			tmpData["importType"] = importType;
			this.dialogRefImportProducts = this.dialog.open(ImportProductComponent, {
				data: tmpData,
				disableClose: true
			});
			this.dialogRefImportProducts.afterClosed().subscribe(result => {});
		}
	}
	dialogRefImportProductPrice: MatDialogRef < ImportProductPriceImportComponent > | null;
	openProductPriceImport(){
		if (this.childData.table == 'EngageboostProducts') {
			let tmpData: any = {};
			this.dialogRefImportProductPrice = this.dialog.open(ImportProductPriceImportComponent, { data: 'import_file' });
			this.dialogRefImportProductPrice.afterClosed().subscribe(result => {
			});
		}
	}
	loadGridData(event: any) {
		let selectedTab = event.index;
		this.selectedTabIndex = selectedTab;
		if (selectedTab == 0) { // All
			this.generateGrid(0, '', '', '', this.search_text, this.show_variant_product);
		} else if (selectedTab == 1) { // Active
			this.generateGrid(1, '', '', 'n', this.search_text, this.show_variant_product);
		} else { // Inactive
			this.generateGrid(1, '', '', 'y', this.search_text, this.show_variant_product);
		}
	}

	dialogRefExportFiles: MatDialogRef <ExportProductComponent> | null;
	OpenExportPopUp() {
		if (this.childData.table == 'EngageboostProducts') {
			this.globalService.showLoaderSpinner(true);
			this._productService.generateProductSheet(this.childData.table).subscribe(
				data => {
					 let that = this;
					if (data.status == 1) {
						let export_file_data: any;
						export_file_data = data.file_path;
						this.globalService.showLoaderSpinner(false);
						that.dialogRefExportFiles = that.dialog.open(ExportProductComponent, {
							data: export_file_data
						});
						that.dialogRefExportFiles.afterClosed().subscribe(result => {});
					}
				},
				err => {
				});
		}
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
	selector: 'my-app',
	templateUrl: `./templates/product_details.html`,
	providers: [Global, ProductService, DashboardService, OrderService],
	animations: [AddEditTransition],
	host: {
		'[@AddEditTransition]': ''
	},
})

export class ProductDetailsComponent implements OnInit {
	// @Input() childData: {table: string, heading: string, tablink:string,tabparrentid:any,screen:any,ispopup:any};
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public menu_list: any;
	public formModel: any = {};
	public List: any = {}
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public add_edit: any = '';
	public imgsubscriber: any;
	public parent_category_list: any = [];
	public child_category_list: any = [];
	public sub_child_category_list: any = [];
	public sub_sub_child_category_list: any = [];
	public parent_child: any;
	public product_base: any;
	public product_details: any = {};
	public childData: any = {};
	public search_text: any;
	public bulk_ids: any = [];
	public individualRow: any = {};
	public pagination: any = {};
	public pageIndex: number = 0;
	public pageList: number = 0;
	public sortBy: any = '';
	public sortOrder: any = '';
	public sortClass: any = '';
	public sortRev: boolean = false;
	public selectedAll: any = false;
	public stat: any = {};
	public result_list: any = [];
	public flat_shipping_method_result: any = [];
	public inventory_list: any=[];
	public order_list: any=[];
	public table_rate_result: any = [];
	public free_shipping_result: any = [];
	public total_list: any = [];
	public cols: any = []
	public layout: any = []
	public add_btn: string;
	public post_data = {};
	public page: number = 1;
	public filter: string = '';
	public maxSize: number = 10;
	public directionLinks: boolean = true;
	public autoHide: boolean = false;
	public config: any = {};
	public permission: any = [];
	promition_list=[];
	top_customes=[];
	suppliers=[];
	feeds=[];
	all_counters={};
	public show_btn: any = {
		'add': true,
		'edit': true,
		'delete': true,
		'block': true
	};
	public userId: any;
	public companyId: any;
	public websiteId: any;
	public settingsId: number;
	public ship_type: number;
	public country_list: any = [];

	//Doughnut Chart config
	public doughnutChartLabels: string[] = ['Webstore', 'Amazon', 'Ebay', 'Flipkart'];
	public doughnutChartData:
	number[] = [];
	public doughnutChartType: string = 'doughnut';

	//Doughnut Chart config
	public doughnutChartLabelsVisitor: string[] = ['Webstore', 'Mobile Store'];
	public doughnutChartDataVisitor: number[] = [];
	public doughnutChartTypeVisitor: string = 'doughnut';

	public colors = [{
		backgroundColor: [
			'rgb(100,57,136)',
			'rgb(184, 4, 89)',
			'rgb(122, 196, 89)',
			'rgb(247, 3, 116)',
			'rgb(26, 47, 116)',
			'rgb(125, 4, 89)'
		]
	}];

	
	// public barChartLegend:boolean = true;
	// public barChartType:string = 'bar';
	// public bar_points_arr: Array<any> = [];
	// public barChartColors:Array<any> = [
	//   { 
	//     backgroundColor: 'rgba(2, 148, 215, 0.2)',
	//     borderColor: 'rgba(2, 148, 215, 1)',
	//     pointBackgroundColor: 'rgba(2, 148, 215, 1)',
	//     pointBorderColor: '#fff',
	//     pointHoverBackgroundColor: '#fff',
	//     pointHoverBorderColor: 'rgba(2, 148, 215, 0.8)'
	//   }
	// ];

	//sales graph//
	public selected: any;
	public customerBarChartData:any;
	alwaysShowCalendars: boolean;
	showRangeLabelOnInput: boolean;
	keepCalendarOpeningWithRange: boolean;
	maxDate: moment.Moment;
	minDate: moment.Moment;
	invalidDates: moment.Moment[] = [moment().add(2, 'days'), moment().add(3, 'days'), moment().add(5, 'days')];
	ranges: any = {
		'Today': [moment(), moment()],
		'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
		'Last 7 Days': [moment().subtract(6, 'days'), moment()],
		'Last 30 Days': [moment().subtract(29, 'days'), moment()],
		'This Month': [moment().startOf('month'), moment().endOf('month')],
		'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
	}
	public selectedItem :string = 'day';
	public selectedStartDate:any;
	public selectedEndDate:any;
	public graphdata:any;
	public graphlable:any;

	public ChartDataSets: any = [];

	public lineChartData_sales: any = [];
	public lineChartData_stock: any = [];
	public lineChartData_visitor: any = [];

	public chart_data: any = [];
	public chart_label: string = ''; 
	public graph_lables:any =[];
	public report_type: string = '';
	public chart_yAxisID: string = '';
	public lineChartLabels_sales:any = [''];
	public lineChartLabels_stock:any = [''];
	public lineChartLabels_visitor:any = [''];
	public lineChartOptions: (ChartOptions & { annotation: any }) = {
		responsive: true,   
		annotation: {
		annotations: [
			{
			type: 'line',
			mode: 'vertical',
			scaleID: 'x-axis-0',
			value: 'March',
			borderColor: 'orange',
			borderWidth: 2,
			label: {
				enabled: true,
				fontColor: 'orange',
				content: 'LineAnno'
			}
			},
		],
		},
	};
	public lineChartColors: Color[] = [
		{ 
			backgroundColor: 'rgba(260,150,200,0.2)',
			borderColor: 'rgba(200,140,200,1)',
			pointBackgroundColor: 'rgba(148,100,300,1)',
			pointBorderColor: '#fff',
			pointHoverBackgroundColor: '#fff',
			pointHoverBorderColor: 'rgba(148,159,177,0.8)'
		}
	];
	public lineChartLegend = false;
	public lineChartType = 'line';
	public lineChartPlugins = [pluginAnnotations];
	
  
	//end sales graph//

	//ORDER GRID VARIABLES
	public selectedAllTags: any = false;
	public selectedAllStatus: any = false;
	public selectedAllDestinations: any = false;
	public selectedAllAssignedWarehouse: any = false;
	public timeSlotAll: any = false;
	public selectAll;
	public show_item_wise_order: any = 0;
	public tag_list: any = [];
	public warehouse_list: any = [];
	public status_list: any = [];
	public action_status_list: any = [];
	public channel_list: any = [];
	public channel_ids: any = [];
	public tag_ids: any = [];
	public destination_list: any = [];
	public order_status_ids: any = [];
	public destinations_ids: any = [];
	public assigned_manager: any = [];
	public action_order_status_ids: any = [];
	
	public status_list_name: any = [];
	public channel_list_name: any = [];
	public destination_list_name: any = [];
	public tag_list_name: any = [];
	public assigned_manager_name: any = [];
	
	public order_delivery_slot: any = [];
	public timeSlotIds: any = [];

	public daterange: any = {};
	public options: any = {
		locale: {
			format: 'YYYY-mm-dd'
		},
		alwaysShowCalendars: false,
	};
	public filter_date = '';
	public colSpanCount: number = 4;
	public currency_list: any = {};
	showSkeletonLoaded: boolean = false;
	public temp_result = [];
	public temp_col = [];
	tab_number:number;
	//ORDER GRID VARIEBLES
	//SIDE PANEL VARIABLE
	public activitySettings: boolean = false;
	public user_type:any;
	public warehouse_id: any;
	constructor(
		public _globalService: GlobalService,
		private global: Global,
		private _router: Router,
		private _route: ActivatedRoute,
		private sanitizer: DomSanitizer,
		private dialogsService: DialogsService,
		private elRef: ElementRef,
		private _cookieService: CookieService,
		public dialog: MatDialog,
		private _productService: ProductService, @Inject(DOCUMENT) private document: any,
		private _orderService: OrderService,


	) {
		this.maxDate = moment().add(2, 'weeks');
		this.minDate = moment().subtract(3, 'days');
		this.alwaysShowCalendars = true;
		this.keepCalendarOpeningWithRange = true;
		this.showRangeLabelOnInput = true;
		this.selected = {
			startDate: moment().subtract(30, 'days'),
			endDate: moment().subtract(0, 'days')
		};
		this.getWarehouselist();
	}

	ngOnInit() {
		this.product_base = window.location.protocol + '//' + window.location.hostname + ':' + GlobalVariable.apiPort + '/product/';
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		this.sub = this._route.params.subscribe(params => {
			this.formModel.productId = +params['id']; // (+) converts string 'id' to a number
		});
		let userData = this._cookieService.getObject('userData');
		this.userId = userData['uid'];
		this.warehouse_id = userData['warehouse_id'];
		if(this.warehouse_id != '' && this.warehouse_id > 0) {
			this.formModel.default_warehouse = this.warehouse_id;
			this.callbackLoadStock(this.formModel.default_warehouse);
		} else {
			this.formModel.default_warehouse = null;
		}

		if (this.formModel.productId > 0) {
			this._productService.loadProductDetails(this.formModel.productId).subscribe(
				data => {
					this.formModel.sku = data.product_details.sku;
					this.formModel.name = data.product_details.name;
					this.formModel.barcode = data.product_details.ean;
					if(data.product_details.image!=''){
						this.formModel.cover_img = GlobalVariable.S3_URL + 'product/200x200/' + data.product_details.image;
					} else {
						this.formModel.cover_img = 'assets/images/dummy.png';
					}
					if(data.currency_code == ''){
						this.formModel.currency_code = data.currency_code;
					} else {
						this.formModel.currency_code = userData['currencysymbol'];
					}
					this.childData = {
						table: 'EngageboostProducts',
						heading: 'Product',
						ispopup: 'N',
						tablink: 'products',
						user_id: 277,
					}
				},
				err => {
					this._globalService.showToast('Something went wrong. Please try again.');
				})
		}
		this.load_product_summary();
		this.load_piechart_data();
		this.loadProductDetailsTab({'index':0});
		this.getgraphdata('month');
		this._globalService.loadSkeletonChange$.subscribe(
			(value) => {
				this.showSkeletonLoaded = value;
			}
		);
		for (let i = 0; i < 15; i++) {
			this.temp_result.push(i);
		}
		for (let i = 0; i < 5; i++) {
			this.temp_col.push(i);
		}
		this.loadCurrencyMasters();
		// reset calender
		this.AppplyDate(this.selected, 'y');
		this.user_type = userData['user_type'];
		// alert(this.user_type);
	}
	//SALES REPORT GRAPH AND ALL LINEAR GRPAH START
	getgraphdata(type:any) {
		var data: any     = {};
		this.report_type  = type;
		this.selectedItem = type;
		data.website_id   = this._globalService.getWebsiteId();
		data.company_id   = 1;
		data.warehouse_id = this.formModel.default_warehouse;
		data.report_type  =  this.report_type;
		if(this.selectedStartDate != null){
			data.start_date = this.selectedStartDate;
			data.end_date   = this.selectedEndDate;
		} else {
			// data.start_date = this._globalService.convertDate(moment().subtract(30, 'days'), 'yyyy-MM-dd');
			data.start_date = this._globalService.convertDate(moment().subtract(30, 'days'), 'yyyy-MM-dd');
			data.end_date   = this._globalService.convertDate(moment().subtract(0, 'days'), 'yyyy-MM-dd');
		}
		this.resetgraphdata();
		this.getGraphdetails(this.formModel.productId,'sales');
		this.getGraphdetails(this.formModel.productId,'stock');
		this.getGraphdetails(this.formModel.productId,'visitor');
	}

	getGraphdetails(data,graph_for=''){
		data = {
			"product_id":this.formModel.productId,
			"start_date":  this.selected.startDate,
			"end_date":  this.selected.endDate,
			"warehouse_id": this.formModel.default_warehouse
		}
		this._productService.graphLoad(data,graph_for,data).subscribe(data => {
			if(data.api_status==1) {
				this.chart_yAxisID  = 'y-axis-0';
				this.customerBarChartData =true;
				if(graph_for=='sales'){
					this.response   = data;
					let graph_lable = this.response.data;  //date
					let graph_data  = this.response.data; //Value 
					let graph_lables:any=[]
					graph_lable.forEach(items => { 
						if( this.report_type == 'day' ||  this.report_type == 'month'){
							graph_lables.push(this._globalService.convertDate(items.weekly_day, 'd MMM'));
						}else{
							graph_lables.push(items.weekly_day);
						}
					});
					this.lineChartLabels_sales = graph_lables;
					let chart_data:any=[];
					graph_data.forEach(item => {
						var val = item.total_sale;
						// let n = parseFloat(val).toFixed(2)
						// var withCommas = Number(n).toLocaleString('en');
						// var data_val = JSON.stringify(withCommas);
						// data_val.replace (/"/g,'');
						// console.log(data_val);
						chart_data.push(val);
					});
					let chart_label    = 'Sales';
					this.lineChartData_sales.push({
						data: chart_data, 
						label: chart_label,
						yAxisID: this.chart_yAxisID
					})
				}
				if(graph_for=='stock'){
					this.response   = data;
					let graph_lable = this.response.data;  //date
					let graph_data  = this.response.data; //Value 
					let graph_lables:any=[]
					graph_lable.forEach(items => { 
						if( this.report_type == 'day' ||  this.report_type == 'month'){
							graph_lables.push(this._globalService.convertDate(items.created, 'd MMM'));
						} else {
							graph_lables.push(items.created);
						}
					});
					this.lineChartLabels_stock = graph_lables;
					let chart_data:any=[]
					graph_data.forEach(item => {     
						chart_data.push(item.total);
					});
					let chart_label    = 'stock';
	
					this.lineChartData_stock.push({
						data: chart_data, 
						label: chart_label,
						yAxisID: this.chart_yAxisID
					})   
				}
				if(graph_for=='visitor'){
					this.response   = data;
					let graph_lable = this.response.data;  //date
					let graph_data  = this.response.data; //Value 

					let graph_lables:any=[]
	
					graph_lable.forEach(items => { 
						if( this.report_type == 'day' ||  this.report_type == 'month'){
							graph_lables.push(this._globalService.convertDate(items.date, 'd MMM'));
						}else{
							graph_lables.push(items.date);
						}
					});
					this.lineChartLabels_visitor = graph_lables;
					let chart_data:any=[]
					graph_data.forEach(item => {
						chart_data.push(item.total);
					});
					let chart_label = 'visitor';
					this.lineChartData_visitor.push({
						data: chart_data, 
						label: chart_label,
						yAxisID: this.chart_yAxisID
					})
				}
			}else{
				this.lineChartData_sales.push({
					data: [0], 
					label: ['Sales'],
					yAxisID: this.chart_yAxisID
				})
				this.lineChartData_stock.push({
					data: [0], 
					label: ['stock'],
					yAxisID: this.chart_yAxisID
				})
				this.lineChartData_visitor.push({
					data: [0], 
					label: ['visitors'],
					yAxisID: this.chart_yAxisID
				})
			}
		}, err => {
			this._globalService.showToast('Something went wrong. Please try again.');
		});
	  }
	resetgraphdata(){
		this.chart_data = [];
		this.chart_label    = '';
		this.chart_yAxisID  = 'y-axis-0';
		this.lineChartLabels_sales = '';
		this.lineChartLabels_stock = '';
		this.lineChartLabels_visitor = '';
		this.lineChartData_sales = [];
		this.lineChartData_stock = [];
		this.lineChartData_visitor = [];
		this.graph_lables = []; 
	}
	public chartClicked(e:any):void {
		console.log(e);
	}
	public chartHovered(e:any):void {
		console.log(e);
	}
	//SALES REPORT AND ALL LINEAR GRPAHGRAPH END

	//PIECHART DATA CREATION START
	load_piechart_data(){
		this.doughnutChartData = [400, 200, 100, 50];
		let data={
			"product_id":this.formModel.productId,
			"start_date":  this.selected.startDate,
			"end_date":  this.selected.endDate,

		}
		this.global.getWebServiceData('product-view-marketplace','POST',data,this.formModel.productId).subscribe(data => {
			if(data.api_status==1) {
				let pichart_date=data.dated;
				this.doughnutChartLabelsVisitor=[];
				this.doughnutChartDataVisitor=[];
				let pichart_data=data.data;
				pichart_data.forEach(element => {
					this.doughnutChartLabelsVisitor.push(element.order__webshop_id__name);
					this.doughnutChartDataVisitor.push(element.total_sale);
				});
				
			} else {
				this.doughnutChartDataVisitor=[0,0];
				//this._globalService.showToast("Something went wrong. Please try later.");
			}
		}, err => {
			this._globalService.showToast("Something went wrong. Please try later.");
		})
	}
	//PIECHART DATA CREATION END
	
	//GET PRODUCT SUMMARY
	load_product_summary(){
		let post_data = {
			"product_id":this.formModel.productId,
			"start_date":  this.selected.startDate,
			"end_date":  this.selected.endDate,
			"warehouse_id": this.formModel.default_warehouse
		}
		//console.log(post_data);
		this.global.getWebServiceData('product-view-summary','POST',post_data,this.formModel.productId).subscribe(data => {
			if(data) {
				this.formModel.total_sale = data.total_sale;//data.total_sale.toFixed(2);
				this.formModel.total_customer = data.total_customer;
				this.formModel.tot_stock = data.tot_stock;
				this.formModel.tot_real_stock = data.tot_real_stock;
				this.formModel.tot_virtual_stock = data.tot_virtual_stock;
				this.formModel.tot_safety_stock = data.tot_safety_stock;
				this.formModel.tot_visitors = data.tot_visitors;
			} else {
			   // this._globalService.showToast("Something went wrong. Please try later.");
			}
		}, err => {
			this._globalService.showToast("Something went wrong. Please try later.");
		})
	}
	toggleCheckAll(event: any) {
		let that = this;
		that.bulk_ids = [];
		this.selectedAll = event.checked;
		this.result_list.forEach(function(item: any) {
			item.selected = event.checked;
			if (item.selected) {
				that.bulk_ids.push(item.id);
			}
		});
	}
	get_promotion_list(id:number){
		this._productService.getPromotionList(id).subscribe(data=>{
			this.promition_list=data.api_status;
		})
	}
	get_suppliers(id:number){
		this._productService.getSuppliers(id).subscribe(data=>{
			this.suppliers=data.api_status;
		})
	}
	get_top_customers(id){
		this._productService.getTopCustomers(id).subscribe(data=>{
			this.top_customes=data.api_status;
		})
	}
	get_feeds(id:number){
		this.feeds=[];
		this._productService.getFeeds(id).subscribe(data=>{
			this.feeds=data.api_status;
		})
	}
	get_all_counters(id:number){
		this.all_counters={};
		// this._productService.getAllCounters(id).subscribe(data=>{
		//     console.log(data);
		// })
	}
	product_print() {
		let printContents, popupWin;
		printContents = document.getElementById('product-details').innerHTML;
		popupWin.document.open();
		popupWin.document.close();
	}

	loadProductDetailsTab(event:any) {
		let tab_number = event.index;
		this.tab_number=event.index;
		if (tab_number == 0) { // Summary Details
			this.get_promotion_list(this.formModel.productId);
			this.get_top_customers(this.formModel.productId);
			this.get_suppliers(this.formModel.productId);
			this.get_feeds(this.formModel.productId);
			this.get_all_counters(this.formModel.productId);
			//document.querySelector('.topheading').classList.add('ord');
		}
		if (tab_number == 1) { // Inventory
			this.generateGridInventory(0, '', '', '', '');
			//document.querySelector('.topheading').classList.remove('ord');
		}
		if (tab_number == 2) { // Order Details
			this.generateGridOrder(0, '', '', '', '', this.show_item_wise_order);
			//document.querySelector('.topheading').classList.remove('ord');
			
		}
		if (tab_number == 3) { // Invoice
			this.generateGridInvoice(0, '', '', '', '');
			//document.querySelector('.topheading').classList.remove('ord');
		}
		if (tab_number == 4) { // Purchase Order
			this.generateGridPurchase(0, '', '', '', '');
			//document.querySelector('.topheading').classList.remove('ord');
		}
	}
	datesUpdatedApply(range) {
		//console.log(range);
		this.AppplyDate(range, 'n');
	}
	AppplyDate(range, load_first: any = 'n') {
		const myObjStr = JSON.stringify(range);
		const selected_dates = JSON.parse(myObjStr);
		// console.log(selected_dates);
		// let selectedStartDate = this._globalService.convertDate(selected_dates.startDate, 'yyyy-MM-dd');
		let selectedStartDate = selected_dates.startDate;
		// let selectedStartDate = '2019-08-07';
		// let selectedEndDate = this._globalService.convertDate(selected_dates.endDate, 'yyyy-MM-dd');                                     
		let selectedEndDate = selected_dates.endDate
		// let selectedEndDate = '2019-09-06';
		this.filter_date = selectedStartDate + '##' + selectedEndDate;
		if (selectedStartDate != null && selectedEndDate != null && load_first != 'y') {
			let tab_number=this.tab_number;
			if(tab_number == 0){
				this.getgraphdata('month');
				this.load_piechart_data();
				this.load_product_summary();
			}
			if (tab_number == 1) { 
				// Inventory
				this.generateGridInventory(0, '', '', '', '');
			}
			if (tab_number == 2) { 
				// Order Details
				this.generateGridOrder(0, '', '', '', '', this.show_item_wise_order);
			}
			if (tab_number == 3) { 
				// Invoice
				this.generateGridInvoice(0, '', '', '', '');
			}
			if (tab_number == 4) { 
				// Purchase Order
				this.generateGridPurchase(0, '', '', '', '');
			}
		}
	}
	loadCurrencyMasters() {
		this.global.getWebServiceData('currencylist', 'GET', '', '').subscribe(res => {
			if (res["status"] == 1) {
				res["data"].forEach(element => {
					this.currency_list[element.currency] = element.currencysymbol;
				});
			}
		}, err => {

		})
	}
	generateGridInventory(reload: any, page: any, sortBy: any, filter: any, search: any) {
		setTimeout(() => {
			this._globalService.skeletonLoader(true);
		});
		if (search == '') {
			this.search_text = '';
		}
		this.bulk_ids = [];
		this.individualRow = {};
		this.total_list = [];
		this.selectedAll = false;
		this.filter = filter;
		this.filter = filter;
		this.pagination.total_page = 0;
		this.config = {};
		var visibility_id: any;
		let that = this;
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
		}
		
			let dateArr = this.filter_date.split("##");
			let fromDate = dateArr[0]
			let toDate = dateArr[1]
			if(fromDate=='null'){
				fromDate=this.selected.startDate;
			}
			if(toDate==='null'){
				toDate=this.selected.endDate;
			}
			this.post_data ={
				"warehouse_id": this.formModel.default_warehouse,
				"order_by": "id",
				"order_type": "+",
				"search": "",
				"hide_out_of_stock": 0,
				"userid":  this.userId,
				"advanced_search": [
					{
						"field": "product__id",
						"comparer": 1,
						"key": this.formModel.productId,
						"name": "Stock"
					}
				],
				"start_date":  fromDate,
				"end_date":  toDate,

			}
			this._productService.loadOrderProductGrid(this.post_data, page, this.formModel.productId).subscribe(
				data => {
					let that = this;
					this.response = data;
					this.total_list = [];
					if (this.response.count > 0) {
						this.result_list = this.response.results[0].result.product;
						// console.log( this.response.results[0].result);
						this.result_list.forEach(function(item: any) {
							if (item.isblocked == 'n') {
								item.isblocked = 'Active';
							} else {
								item.isblocked = 'Inactive';
							}
						});
						for (var i = 0; i < this.response.count; i++) {
							this.total_list.push(i);
						}
					} else {
						this.result_list = [];
					}
					this.inventory_list = this.result_list;
					
					// this.cols = this.response.results[0].layout;
					//this.cols = this.response.results[0].applied_layout;
					this.cols = this.response.results[0].applied_layout;
					this.layout = this.response.results[0].layout;

					this.pagination.total_page = this.response.per_page_count;
					this.pageList = this.response.per_page_count;
					this.stat.cancelled = this.response.results[0].Cancelled;
					this.stat.failed = this.response.results[0].Failed;
					this.stat.pending = this.response.results[0].Pending;
					this.stat.shipped = this.response.results[0].Shipped;
					this.stat.all = this.response.results[0].all;
					this.add_btn = this.response.results[0].add_btn;
					this.config.currentPageCount = this.result_list.length
					this.config.currentPage = page
					this.config.itemsPerPage = this.response.page_size;
					this.permission = this.response.results[0].role_permission;
					this._globalService.skeletonLoader(false);
				},
				err => console.log(err)
			);
		
	}
	generateGridOrder(reload: any, page: any, sortBy: any, filter: any, search: any, show_item_wise_order: any) {
		let userData = this._cookieService.getObject('userData');
		let websiteId = this._globalService.getWebsiteId();
		var page_size = 0;
		setTimeout(() => {
			this._globalService.skeletonLoader(true);
		});
		let filterQuery = [];
		let filterQuery2 = [];
		let filterQuery3 = [];
		// search = search.trimLeft();
		filterQuery.push({ match: { products_id: this.formModel.productId } });
		if(this.formModel.default_warehouse != '' && this.formModel.default_warehouse > 0){
			filterQuery.push({ match: { assign_wh: this.formModel.default_warehouse } });
		}

		if (search == '') {
			this.search_text = '';
		} else {
			this.search_text = search;
		}
		this.bulk_ids = [];
		this.individualRow = {};
		this.total_list = [];
		this.selectedAll = false;
		this.filter = filter;
		this.filter = filter;
		this.show_item_wise_order = show_item_wise_order;
		if (this.show_item_wise_order) {
			this.childData.table = 'EngageboostOrderProducts';
		} else {
			this.childData.table = 'EngageboostOrdermaster';
		}
		if (sortBy != '' && sortBy != undefined) {
			if (this.sortRev) {
				this.sortOrder = '-'
				this.sortRev = !this.sortRev;
				this.sortClass = 'icon-down';
			}
			else {
				this.sortOrder = '+'
				this.sortRev = !this.sortRev;
				this.sortClass = 'icon-up';
			}
		}
		let filter_tag_ids = '';
		if (this.tag_ids.length > 0) {
			let tags_str = this.tag_ids.join();
			filter_tag_ids = tags_str.toString();
			filterQuery.push({ 'terms': { 'tags': this.tag_ids } });
		}
		let filter_channel_list = '';
		if (this.channel_ids.length > 0) {
			let chanel_str = this.channel_ids.join();
			filter_channel_list = chanel_str.toString();
		}
		let filter_order_status = '';
		if (this.order_status_ids.length > 0) {
			let order_status_str = this.order_status_ids.join();
			filter_order_status = order_status_str.toString();
			filterQuery.push({ 'terms': { 'order_status': this.order_status_ids } });
		}
		let filter_destinations = '';
		if (this.destinations_ids.length > 0) {
			let destinations_str = this.destinations_ids.join();
			filter_destinations = destinations_str.toString();
		}
		let filter_warehouse_id = '';
		if (this.assigned_manager.length > 0) {
			let assinged_str = this.assigned_manager.join();
			filter_warehouse_id = assinged_str.toString();
			//filterQuery.push({'terms' : {'warehouse_id' : this.assigned_manager}});
			filterQuery.push({ 'terms': { 'assign_to': this.assigned_manager } });
		}

		
		let filter_delivery_slot_ids = '';
		if (this.timeSlotIds.length > 0) {
			//filterQuery['terms']['time_slot_id'] = this.timeSlotIds;
			let convertedTimeSlotIds = [];
			this.timeSlotIds.forEach(timeSlot => {
				timeSlot = timeSlot.replace(/-/g, "").replace(/ /g, '').replace(/:/g, '').toLowerCase();
				convertedTimeSlotIds.push(timeSlot);
				//filterQuery.push({'match' : {'time_slot' : '0500pm0700pm'}}); 
			})
			filterQuery.push({ 'terms': { 'time_slot': convertedTimeSlotIds } });
			let timeSlotIds_str = this.timeSlotIds.join();
			filter_delivery_slot_ids = timeSlotIds_str.toString();
		}
		if (this.filter_date === 'null##null') {
			this.selected = {
				startDate: moment().subtract(30, 'days'),
				endDate: moment().subtract(0, 'days')
			}; // reset calender
			this.AppplyDate(this.selected, 'y');
		}

		let matchArr = [];
		/////////////// loading default conditions for grid /////////////////
		let conditions: any = {}
		conditions.buy_status = 1;
		let innerMatch: any = {};
		innerMatch.match = conditions;
		// let new_field_query={"match": {"custom_order_id": 'SAMPLE-ORD#125'} }
		// let new_field_query2={"match": {"buy_status": 1} }
		matchArr.push(innerMatch);
		// matchArr.push(new_field_query);
		// matchArr.push(new_field_query2);
		if (filterQuery && filterQuery.length > 0) {
			//console.log(filterQuery);
			matchArr = matchArr.concat(filterQuery);
		}

		if (search != '') { // pushing search conditions
			conditions = {}
			conditions.query = "*" + search + "*";
			innerMatch = {};
			innerMatch.query_string = conditions;
			matchArr.push(innerMatch);
		}

		this.post_data = {
			"model": this.childData.table,
			"screen_name": 'list',
			"userid": this.userId,
		}
		let dateArr = this.filter_date.split("##");
		let fromDate = dateArr[0]
		let toDate = dateArr[1]
		this.global.loadColumnVisibility(this.post_data).subscribe(data => {
			this.response = data;
			// this.cols = this.response.results[0].layout;
			this.cols = this.response.results[0].applied_layout;
			this.colSpanCount = this.cols.length;
			this.pageList = this.response.per_page_count;
			this.stat.active = this.response.results[0].active;
			this.stat.inactive = this.response.results[0].inactive;
			this.stat.all = this.response.results[0].all;
			this.add_btn = this.response.results[0].add_btn;
			this.permission = this.response.results[0].role_permission;
			page_size = this.response.page_size;

			///// startig query string filer ////////////////
			if (sortBy == '') {
				sortBy = 'id';
			}
			let orderType = 'asc';
			if (this.sortOrder == '+') {
				orderType = 'asc'
			} else {
				orderType = 'desc'
			}
			let from = 0;
			if (page <= 0 || page == '') {
				page = 1;
				from = 0;
			} else {
				let start = page - 1;
				from = start * this.response.page_size;
				//from = from - 1;
			}
			if (from < 0) {
				from = 0;
			}
			this.sortBy = sortBy;
			//FOR TYPE 1
			let extraFilter = JSON.stringify(matchArr);
			//FOR TYPE 2
			let extraFilter2 = JSON.stringify(filterQuery2);
			let extraFilter3 = JSON.stringify(filterQuery3);

			let searchConditions:any={};
			searchConditions.extraFilter = extraFilter; 
			searchConditions.extraFilter2 = extraFilter2; 
			searchConditions.fromDate = fromDate; 
			searchConditions.toDate = toDate; 
			// this.elasticSearch.exportConditions = searchConditions;

			let elasticData = '{"query":{"bool":{"must":' + extraFilter + ', "must_not":' + extraFilter2 + ',"filter":{"range":{"created":{"gte":"' + fromDate + '","lte":"' + toDate + '"}}}}},"from": ' + from + ',"size": ' + page_size + ',"sort": [{"' + sortBy + '": "' + orderType + '"}]}';
			this._orderService.loadGridES('orders', page, search, page_size, sortBy, this.sortOrder, elasticData, websiteId).subscribe(listData => {
				let tmpResult = [];
				listData.hits.hits.forEach(function (rows: any) {
					tmpResult.push(rows._source);
				});
				this.response.results[0].result = tmpResult;
				if (tmpResult.length > 0) {
					this.result_list = this.response.results[0].result;
					let that = this;
					this.result_list.forEach(function (item: any) {
						//////////// start the status settings //////////////////////
						if (item.order_status == '99' && item.buy_status == '1') {
							item.order_status = 'Waiting Approval';
							item.class_name = 'status-box approval';
						} else if (item.order_status == '0' && item.buy_status == '1') {
							item.order_status = 'Pending';
							item.class_name = 'status-box pendings';
						} else if (item.order_status == '100' && item.buy_status == '1') {
							item.order_status = 'Processing';
							item.class_name = 'status-box processing';
						} else if (item.order_status == '1' && item.buy_status == '1') {
							item.order_status = 'Shipped';
							item.class_name = 'status-box shipped_new';
						} else if (item.order_status == '2' && item.buy_status == '1') {
							item.order_status = 'Cancelled';
							item.class_name = 'status-box cancelled';
						} else if (item.order_status == '4' && item.buy_status == '1') {
							item.order_status = 'Completed';
							item.class_name = 'status-box completed';
						} else if (item.order_status == '5' && item.buy_status == '1') {
							item.order_status = 'Full Refund';
							item.class_name = 'status-box full-refund';
						} else if (item.order_status == '6' && item.buy_status == '1') {
							item.order_status = 'Partial Refund';
							item.class_name = 'status-box partial-refund';
						} else if (item.order_status == '7' && item.buy_status == '1') {
							item.order_status = 'Return Initiate';
							item.class_name = 'status-box full-refund';
						} else if (item.order_status == '11' && item.buy_status == '1') {
							item.order_status = 'Partial Refund';
							item.class_name = 'status-box paid';
						} else if (item.order_status == '12' && item.buy_status == '1') {
							item.order_status = 'Assigned to Showroom';
							item.class_name = 'status-box assign-to-showroom';
						} else if (item.order_status == '13' && item.buy_status == '1') {
							item.order_status = 'Delivered';
							item.class_name = 'status-box delivered';
						} else if (item.order_status == '16' && item.buy_status == '1') {
							item.order_status = 'Closed';
							item.class_name = 'status-box closed';
						} else if (item.order_status == '18' && item.buy_status == '1') {
							item.order_status = 'Pending Service';
							item.class_name = 'status-box pending-service';
						} else if (item.order_status == '3' && item.buy_status == '0') {
							item.order_status = 'Abandoned';
							item.class_name = 'status-box abondoned';
						} else if (item.order_status == '999' && item.buy_status == '0') {
							item.order_status = 'Failed';
							item.class_name = 'status-box failed';
						}
						else if (item.order_status == '9999' && item.buy_status == '1') {
							item.order_status = 'Hold';
							item.class_name = 'status-box hold';
						} else {
							item.order_status = 'Invoiced';
							item.class_name = 'status-box invoiced';
						}

						//console.log(item.shipping_status);
						if (item.shipping_status == 'Pending') {
							item.shipping_class_name = 'status-box pendings';
						} else if (item.shipping_status == 'Created') {
							item.shipping_class_name = 'status-box created';
						} else if (item.shipping_status == 'Picking') {
							item.shipping_class_name = 'status-box packed';
						} else if (item.shipping_status == 'Ready to Ship') {
							item.shipping_class_name = 'status-box ready_to_ship';
						} else if (item.shipping_status == 'Create Shipment') {
							item.shipping_class_name = 'status-box processing';
						} else if (item.shipping_status == 'Shipped') {
							item.shipping_class_name = 'status-box shipped_new';
						} else if (item.shipping_status == 'Invoicing') {
							item.shipping_class_name = 'status-box invoiced';
						} else if (item.shipping_status == 'Shipment Processing') {
							item.shipping_class_name = 'status-box shipment_processing';
						} else {
							item.shipping_class_name = 'status-box completed';
						}

						//console.log(item.shipping_class_name);
						//////////////  end status settings /////////////////// 
						if (item.created != '') {
							item.created_day = that._globalService.convertDate(item.created, 'EEEE');
						}
						if (item.created != '') {
							item.created = that._globalService.convertDate(item.created, 'dd-MM-yyyy h:mm a');
						}

						if (item.time_slot_date != '') {
							item.time_slot_date = that._globalService.convertDate(item.time_slot_date, 'dd-MM-yyyy') + " " + item.time_slot_id;
						}

						let currencyCode = item.currency_code;
						item.gross_amount = that.currency_list[currencyCode] + " " + item.gross_amount.toFixed(2);
						item.shipping_cost = that.currency_list[currencyCode] + " " + item.shipping_cost.toFixed(2);
						item.gross_discount_amount = that.currency_list[currencyCode] + " " + item.gross_discount_amount.toFixed(2);
						item.tax_amount = that.currency_list[currencyCode] + " " + item.tax_amount.toFixed(2);
						item.net_amount = that.currency_list[currencyCode] + " " + item.net_amount.toFixed(2);
					})
					if (userData['elastic_host'] == '50.16.162.98') {  // this is for new elsatic server
						listData.hits.total = listData.hits.total.value;
					}
					for (var i = 0; i < listData.hits.total; i++) {
						this.total_list.push(i);
					}
					// console.log(this.result_list);
				} else {
					this.result_list = [];
				}
				this.pagination.total_page = Math.ceil(listData.hits.total / page_size);
				if (this.pagination.total_page >= 0) {
					this.pagination.total_page = this.pagination.total_page;
				} else {
					this.pagination.total_page = 0;
				}
				//console.log(listData.hits.total + " ===  " + this.response.page_size + "===" + this.pagination.total_page);
				this.config.currentPageCount = this.result_list.length
				this.config.currentPage = page
				this.config.itemsPerPage = this.response.page_size;
				this._globalService.skeletonLoader(false);
			});

		},err=>{
			this._globalService.skeletonLoader(false);
		});
	}
	generateGridInvoice(reload: any, page: any, sortBy: any, filter: any, search: any) {
		setTimeout(() => {
			this._globalService.skeletonLoader(true);
		});
		
		if(search == '') {
			this.search_text = '';
		} else {
			this.search_text = search;
		}
		this.bulk_ids = [];
		this.individualRow = {};
		this.total_list = [];
		this.selectedAll = false;
		this.filter = filter;
		this.sortOrder = '+';
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
		}
		let dateArr = this.filter_date.split("##");
		let fromDate = dateArr[0]
		let toDate = dateArr[1];
		if(fromDate=='null'){
			fromDate=this.selected.startDate;
		}
		if(toDate==='null'){
			toDate=this.selected.endDate;
		}
		this.post_data = {
			"warehouse_id": this.formModel.default_warehouse,
			"order_by": "id",
			"order_type": this.sortOrder,
			"search": this.search_text,
			"hide_out_of_stock": 0,
			"userid": this.userId,
			"product_id":this.formModel.productId,
			"start_date":  fromDate,
			"end_date":  toDate
		}
		this.global.doGridInvoice(this.post_data, page).subscribe(
			data => {
				this.response = data;
				// console.log(this.response)
				if (this.response.count > 0) {
					this.result_list = this.response.results[0].result.product;
					let that = this;
					this.result_list.forEach(function (item: any) {
						if (item.isblocked == 'n') {
							item.isblocked = 'Active';
						} else {
							item.isblocked = 'Inactive';
						}
						if (item.created_date != '') {
							item.created_date = that._globalService.convertDate(item.created_date, 'dd-MM-yyyy h:mm a');
						} else {
							item.created_date = item.created_date;
						}
					})
					for (let i = 0; i < this.response.count; i++) {
						this.total_list.push(i);
					}
				} else {
					this.result_list = [];
				}

				// this.cols = this.response.results[0].layout;
				// this.cols = this.response.results[0].applied_layout;
				// this.colSpanCount = this.response.results[0].layout.length;
				this.pagination.total_page = this.response.per_page_count;
				this.pageList = this.response.per_page_count;
				// this.stat.active = this.response.results[0].active;
				// this.stat.inactive = this.response.results[0].inactive;
				// this.stat.all = this.response.results[0].all;
				// this.add_btn = this.response.results[0].add_btn;
				this.config.currentPageCount = this.result_list.length
				this.config.currentPage = page
				this.config.itemsPerPage = this.response.page_size;
				// this.permission = this.response.results[0].role_permission;
				this._globalService.skeletonLoader(false);
			},err=>{
				console.log(err)
				this._globalService.skeletonLoader(false);

			}
		);
	}
	generateGridPurchase(reload: any, page: any, sortBy: any, filter: any, search: any) {
		setTimeout(() => {
			this._globalService.skeletonLoader(true);
		});
		
		if(search == '') {
			this.search_text = '';
		} else {
			this.search_text = search;
		}
		this.bulk_ids = [];
		this.individualRow = {};
		this.total_list = [];
		this.selectedAll = false;
		this.filter = filter;
		this.sortOrder = '+'
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
		}
		let dateArr = this.filter_date.split("##");
		let fromDate = dateArr[0];
		let toDate = dateArr[1];
		if(fromDate=='null'){
			fromDate=this.selected.startDate;
		}
		if(toDate==='null'){
			toDate=this.selected.endDate;
		}
		this.post_data = 
		{
			"userid": this.userId,
			"order_by": "id",
			"order_type": this.sortOrder,
			"search": this.search_text,
			"filter": "",
			"is_supplier": 0,
			"supplier_id": 0,
			"advanced_search": [],
			"product_id":this.formModel.productId,
			"start_date":  fromDate,
			"end_date":  toDate,
			"warehouse_id": this.formModel.default_warehouse

		}
		this.global.doGridPurchase(this.post_data, page).subscribe(
			data => {
				this.response = data;
				// console.log(this.response)
				if (this.response.count > 0) {
					this.result_list = this.response.results[0].result.product;
					let that = this;
					this.result_list.forEach(function (item: any) {
						// console.log(item.shipping_cost);
						if (item.isblocked == 'n') {
							item.isblocked = 'Active';
						} else {
							item.isblocked = 'Inactive';
						}
						if(item.shipping_cost==0){
							item.shipping_cost='0.0';
						}
						if(item.cart_discount==0){
							item.cart_discount='0.0';
						}
					})
					for (let i = 0; i < this.response.count; i++) {
						this.total_list.push(i);
					}
				} else {
					this.result_list = [];
				}

				this.cols = this.response.results[0].layout;
				this.cols = this.response.results[0].applied_layout;
				this.colSpanCount = this.response.results[0].layout.length;
				this.pagination.total_page = this.response.per_page_count;
				this.pageList = this.response.per_page_count;
				this.stat.active = this.response.results[0].active;
				this.stat.inactive = this.response.results[0].inactive;
				this.stat.all = this.response.results[0].all;
				this.add_btn = this.response.results[0].add_btn;
				this.config.currentPageCount = this.result_list.length
				this.config.currentPage = page
				this.config.itemsPerPage = this.response.page_size;
				this.permission = this.response.results[0].role_permission;
				this._globalService.skeletonLoader(false);
			},err=>{
				console.log(err)
				this._globalService.skeletonLoader(false);

			}
		);
	}
	showActivityPanel(show:boolean) {
		this.activitySettings = !show;
	}

	getWarehouselist(){
		let userData = this._cookieService.getObject('userData');
		let obj = {};
		obj["id"]='';
		obj["name"]='All';
		this.userId = userData['uid'];
		let websiteId = this._globalService.getWebsiteId();
		this._productService.warehouseLoad(websiteId, this.userId).subscribe(
			data => {
				this.warehouse_list = data.warehouse;
				if(userData['user_type']=='SuperAdmin'){
					this.warehouse_list.splice(0, 0, obj);
				}
				console.log(this.warehouse_list)
				// this.formModel.default_warehouse = this.warehouse_list[0]['id'];
				// alert(this.warehouse_list[0]['id'])
					//this.callbackLoadStock(this.default_warehouse);
			},
			err => console.log(err),
			function() {
				//completed callback
			}
		);
	}
	callbackLoadStock(warehouse_id:number) {
		this.formModel.default_warehouse = warehouse_id;
		if(this.tab_number == 0){
			this.getgraphdata('month');
			this.load_piechart_data();
			this.load_product_summary();
		}
		if (this.tab_number == 1) { 
			// Inventory
			this.generateGridInventory(0, '', '', '', '');
		}
		if (this.tab_number == 2) { 
			// Order Details
			this.generateGridOrder(0, '', '', '', '', this.show_item_wise_order);
		}
		if (this.tab_number == 3) { 
			// Invoice
			this.generateGridInvoice(0, '', '', '', '');
		}
		if (this.tab_number == 4) { 
			// Purchase Order
			this.generateGridPurchase(0, '', '', '', '');
		}
	}
}

@Component({
	selector: 'my-app',
	templateUrl: `./templates/import_product_first_step.html`,
	providers: [Global, ProductService],
})

export class ImportProductComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public websiteId: any;
	public tabIndex: number;
	public parentId: number = 0;
	private sub: any;
	public product_base: any;
	private userId: number;
	public sample_xls: any;
	public xls_file: any;
	public file_selection_tool: any;
	public importType: any='Product';
	public popupLoder: boolean = false;
	constructor(
		private _globalService: GlobalService,
		private global: Global,
		private _router: Router,
		private dialogRef: MatDialogRef < ImportProductComponent > ,
		private _route: ActivatedRoute,
		private sanitizer: DomSanitizer,
		private dialogsService: DialogsService,
		private elRef: ElementRef,
		private _cookieService: CookieService,
		public dialog: MatDialog,
		private _productService: ProductService, @Optional()@ Inject(MAT_DIALOG_DATA) public data: any
	) {}

	ngOnInit() {
		this.product_base = window.location.protocol + '//' + window.location.hostname + ':' + GlobalVariable.apiPort + '/product/';
		this.importType = this.data.importType;
		if (this.data.importType == 'Related') { // this is for without category maping fields 
			this.sample_xls = window.location.protocol + '//' + window.location.hostname + ':' + GlobalVariable.apiPort + '/media/importfile/sample/related_product_import_sheet.xls';
		} else { // this is for with category mapping
			this.sample_xls = window.location.protocol + '//' + window.location.hostname + ':' + GlobalVariable.apiPort + '/media/importfile/sample/product_import_sheet.xls';
		}
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		this.sub = this._route.params.subscribe(params => {
			this.formModel.productId = +params['id']; // (+) converts string 'id' to a number
		});
		let userData = this._cookieService.getObject('userData');
		this.userId = userData['uid'];
		this.file_selection_tool = 'No file choosen';
	}

	import_file_product(e: Event) {
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
			files[this.data.import_file] = file_arr;
		}
		var filename = files.import_file._file.name;
		this.file_selection_tool = filename;
		this.xls_file = files.import_file._file;
		var extn = filename.split(".").pop();
		if (extn == 'xls' || extn == 'xlsx') {
			//this.dialogRef.close(files);
		} else {
			
			this._globalService.showToast('Please choose XLS/XLSX file');
		}
	}

	dialogRefShowMapfields: MatDialogRef < ShowMapFieldsComponent > | null;

	show_map_fields(form: any) {
		this.popupLoder = true;
		//this._globalService.showLoaderSpinner(true);
		var form_data = new FormData();
		form_data.append("import_file", this.xls_file);
		form_data.append("website_id", '1');
		let with_category: any = 0;
		if (this.formModel.checked == true) {
			with_category = 1;
		}
		form_data.append("with_category", with_category);
		if(this.data.importType == 'Main') {
			form_data.append("import_file_type", 'product');
		} else {
			form_data.append("import_file_type", 'related_product');
		}
		
		//form_data.append('website_id', this.website_id_new);
		if (this.xls_file != undefined) {
			this._productService.import_file_data(form_data, this.data.importType).subscribe(
				response => {
					this.popupLoder = false;
					response.importType = this.data.importType;
					response.with_category = with_category;
					this.dialogRef.close();
					this.dialogRefShowMapfields = this.dialog.open(ShowMapFieldsComponent, {
						data: response,
						width: '50%',
						disableClose: true
					});
					this.dialogRefShowMapfields.afterClosed().subscribe(result => {});
					//////this.dialogRef.close();
				},
				err => {
					this._globalService.showToast('Something went wrong with your file. Please download sample file.');
					this.popupLoder = false;
				},
			);
		} else {
			this._globalService.showToast('Please choose XLS/XLSX file');
			this.popupLoder = false;
		}
	}
	closeDialog() {
		this.dialogRef.close();
	}
}

@Component({
	selector: 'my-app',
	templateUrl: `./templates/show_map_fields.html`,
	providers: [Global, ProductService],
})

export class ShowMapFieldsComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public websiteId: any;
	public tabIndex: number;
	public parentId: number = 0;
	private sub: any;
	public product_base: any;
	private userId: number;
	public xls_header: any = [];
	public xls_header_master: any = [];
	public db_fields: any = [];
	public db_fields_label: any = [];
	public imported_file_name: string;
	public field_ids: any = {};
	public parent_category: any = [];
	public second_label_category: any = [];
	public third_label_category: any = [];
	public forth_label_category: any = [];
	public selected_category_id: number;
	public importType: any;
	public popupLoder: boolean = false;
	public with_category: any = 0;
	constructor(
		private _globalService: GlobalService,
		private global: Global,
		private _router: Router,
		private dialogRef: MatDialogRef < ShowMapFieldsComponent > ,
		private _route: ActivatedRoute,
		private sanitizer: DomSanitizer,
		private dialogsService: DialogsService,
		private elRef: ElementRef,
		private _cookieService: CookieService,
		public dialog: MatDialog,
		private _productService: ProductService, @Optional()@ Inject(MAT_DIALOG_DATA) public data: any
	) {}

	ngOnInit() {
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		this.xls_header_master = this.data.xls_header;
		this.importType = this.data.importType;
		this.with_category = this.data.with_category;
		console.log(this.with_category);
		this.imported_file_name = this.data.filename;
		this.parent_category = this.data.category_list;
		let response_header: any = [];
		let response_db_fields: any = [];
		let checking_db_field_label = [];
		let extra_fields: any = {};
		for (let key in this.data.xls_header) {
			response_header.push(key);
		}
		//console.log(response_header);
		///////// extra field in the drop down ///////////////////////
		extra_fields.field_label = 'Select Product Columns';
		extra_fields.model_field_value = '';
		extra_fields.id = '';
		response_db_fields.push(extra_fields);
		checking_db_field_label.push(extra_fields.field_label);

		let extra_fields_new: any = {};
		extra_fields_new.field_label = 'I do not need it';
		extra_fields_new.model_field_value = 'no';
		extra_fields_new.id = '';
		response_db_fields.push(extra_fields_new);
		checking_db_field_label.push(extra_fields_new.field_label);

		///////////// end extra field in the db field drop down //////
		for (var i = 0; i < this.data.db_fields.length; i++) {
			if (this.data.db_fields[i].field_label != '' && this.data.db_fields[i].field_label != 'undefined') { // removed blanlk column and white from the excel sheet
				response_db_fields.push(this.data.db_fields[i]);
				checking_db_field_label.push(this.data.db_fields[i].field_label)
				this.field_ids[this.data.db_fields[i].model_field_value] = (this.data.db_fields[i].id);
			}
		}
		this.db_fields = response_db_fields;
		this.xls_header = response_header;
		for (var i = 0; i < response_header.length; i++) {
			let field_name = response_header[i];
			field_name = field_name.toString(); // need to convert this as string
			let is_field_exist = checking_db_field_label.indexOf(field_name);
			//console.log(is_field_exist);
			if (is_field_exist === -1) {
				this.formModel[field_name] = '';
			} else {
				//console.log(response_db_fields[is_field_exist].model_field_value)
				let field_name1 = response_db_fields[is_field_exist].model_field_value;
				this.formModel[field_name] = field_name1;
			}
		}
		// console.log(this.db_fields)
		// console.log(this.formModel);
		let userData = this._cookieService.getObject('userData');
		this.userId = userData['uid'];
	}

	save_file_data(form: any) {
		this.popupLoder = true;
		var data: any = {};
		var form_data: any = {};
		data.website_id = this._globalService.getWebsiteId();
		data.filename = this.imported_file_name;
		let x = '';
		let mapped_fields: any = {};
		for (x in this.formModel) {
			let field_id = this.field_ids[this.formModel[x]] > 0 ? this.field_ids[this.formModel[x]] : '0';
			let field_obj: any = {};
			field_obj.field_name = this.formModel[x];
			field_obj.id = parseInt(field_id); // if basic field. it will null and for custom field it will be field id 
			mapped_fields[x] = field_obj;
		}
		data.map_fields = mapped_fields;
		data.category_id = this.selected_category_id;
		data.with_category = this.with_category;
		console.log(data)
		console.log(this.importType)
		//form_data = JSON.stringify(data);
		// post_data =  JSON.stringify(data)
		this._productService.save_file_data(data, this.importType).subscribe(
			data => {
				this.response = data;
				let imported_result: any = {};
				this._cookieService.putObject('product_imported_data', '');
				imported_result.excel_headers = this.xls_header;
				imported_result.selected_category_id = this.selected_category_id;
				imported_result.mapped_fields = mapped_fields;
				imported_result.imported_filename = this.imported_file_name;
				imported_result.importType = this.importType;
				imported_result.with_category = this.with_category;
				imported_result.website_id = this._globalService.getWebsiteId();
				this.parent_category = this.response.category_list;
				//console.log(imported_result);
				this._cookieService.putObject('product_imported_data', imported_result);
				this.dialogRef.close();
				this._globalService.addTab('priviewproducts', 'products/preview_product', 'Preview Product', this.parentId)
				this._router.navigate(['/products/preview_product']);
				this.popupLoder = false;
			},
			err => {
				this.popupLoder = false;
				this._globalService.showToast('Something went wrong. Please try again.');
			},
		);
	}

	closeDialog() {
		this.dialogRef.close();
	}

	get_child_category(id: any, category_label: any) {
		this.popupLoder = true;
		let data: any = {};
		let db_fields: any = [];
		data.category_id = id;
		this.selected_category_id = id;
		data.website_id = this._globalService.getWebsiteId();
		data.filename = this.imported_file_name;
		if (id > 0 && category_label != 'no') {
			this._productService.get_child_category(data).subscribe(
				data => {
					if (category_label == 'second') {
						this.second_label_category = data.category_list;
					}
					if (category_label == 'third') {
						this.third_label_category = data.category_list;
					}
					if (category_label == 'forth') {
						this.forth_label_category = data.category_list;
					}

					let response_header: any = [];
					let response_db_fields: any = [];
					let checking_db_field_label = [];
					let extra_fields: any = {};
					for (let key in this.xls_header_master) {
						response_header.push(key);
					}
					db_fields = data.db_fields;
					///////// extra field in the drop down ///////////////////////
					extra_fields.field_label = 'Select Product Columns';
					extra_fields.model_field_value = '';
					extra_fields.id = '';
					response_db_fields.push(extra_fields);
					checking_db_field_label.push(extra_fields.field_label);
					let extra_fields_new: any = {};
					extra_fields_new.field_label = 'I do not need it';
					extra_fields_new.model_field_value = 'no';
					extra_fields_new.id = '';
					response_db_fields.push(extra_fields_new);
					checking_db_field_label.push(extra_fields_new.field_label);
					///////////// end extra field in the db field drop down //////
					for (var i = 0; i < db_fields.length; i++) {
						if (db_fields[i].field_label != '' && db_fields[i].field_label != 'undefined') { // removed blanlk column and white from the excel sheet
							response_db_fields.push(db_fields[i]);
							checking_db_field_label.push(db_fields[i].field_label)
							this.field_ids[db_fields[i].model_field_value] = (db_fields[i].id);
						}
					}
					this.db_fields = response_db_fields;
					this.xls_header = response_header;
					for (var i = 0; i < response_header.length; i++) {
						let field_name = response_header[i];
						field_name = field_name.toString(); // need to convert this as string
						let is_field_exist = checking_db_field_label.indexOf(field_name);
						//console.log(is_field_exist);
						if (is_field_exist === -1) {
							this.formModel[field_name] = '';
						} else {
							//console.log(response_db_fields[is_field_exist].model_field_value)
							let field_name1 = response_db_fields[is_field_exist].model_field_value;
							this.formModel[field_name] = field_name1;
						}
					}
					//console.log(this.formModel);
				},
				err => {
				},
			)
			this.popupLoder = false;
		} else {
			this.popupLoder = false;
			this._globalService.showToast('We have only 4th label category');
		}
	}
}

@Component({
	selector: 'my-app',
	templateUrl: `./templates/product_preview.html`,
	providers: [Global, ProductService],
})

export class ProductPreviewComponent implements OnInit {
	constructor(
		public globalService: GlobalService,
		private global: Global,
		private _router: Router,
		private sanitizer: DomSanitizer,
		private elRef: ElementRef,
		private _cookieService: CookieService,
		public dialog: MatDialog,
		private _productService: ProductService,
		private dialogsService: DialogsService, @Inject(DOCUMENT) private document: any
	) {}
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public bulk_ids: any = [];
	public columns: any = [];
	public temp_result_list: any = [];
	public result_list: any = [];
	public selectedAll: any = false;
	public tabIndex: number;
	public parentId: number = 0;
	public userId: any;
	public individualRow: any = {};
	public popupLoder: boolean = false;
	//////////////////////////Initilise////////////////////////////
	ngOnInit() {
		this.popupLoder = true;
		this.tabIndex = +this.globalService.getCookie('active_tabs');
		this.parentId = this.globalService.getParentTab(this.tabIndex);
		//console.log(this.parentId+'###3'+this.tabIndex);
		let userData = this._cookieService.getObject('userData');
		let product_imported_data = this._cookieService.getObject('product_imported_data');
		console.log(product_imported_data)
		this.userId = userData['uid'];
		let post_data: any = {};
		post_data.filename = product_imported_data['imported_filename'];
		post_data.website_id = 1; //product_imported_data.website_id;
		post_data.with_category = product_imported_data['with_category'];
		if (product_imported_data['importType'] == 'Related') {
			post_data.model = 'related_product';
		} else {
			post_data.model = 'product'; //product_imported_data.website_id;
		}
		post_data.category_id = product_imported_data['selected_category_id'];
		//console.log(post_data);
		this._productService.load_preview_grid(post_data, 1, product_imported_data['importType']).subscribe(
			data => {
				//console.log(data);
				this.temp_result_list = data.preview_data;
				let that = this;
				this.selectedAll = true;
				this.temp_result_list.forEach(function (item: any, key: any) {
					item.selected = true
					if (item.selected && item.error == 0) {
						that.bulk_ids.push(item.id);
					}
				});
				//console.log(this.temp_result_list);
				let x = '';
				//console.log(product_imported_data['mapped_fields']);
				for (x in product_imported_data['mapped_fields']) {
					if (x != 'parent_category_selected' && x != 'second_label_categorys' && x != 'third_label_categorys' && x != 'forth_label_categorys') {
						let field_obj: any = {};
						field_obj.field_name = product_imported_data['mapped_fields'][x].field_name;
						field_obj.label = x;
						this.columns.push(field_obj);
					}
				}
				this.popupLoder = false;
				// console.log('=================');
				// console.log(this.columns);
			},
			err => {
				this.globalService.showToast('Something went wrong. Please try again.');
			},
		);
	}

	////////////////////////////Check/Uncheck//////////////

	toggleCheckAllPreview(event: any) {
		this.popupLoder = true;
		//let elements: NodeListOf<Element> = this.document.getElementsByClassName('action-box');
		let that = this;
		that.bulk_ids = [];
		this.selectedAll = event.checked;
		this.temp_result_list.forEach(function(item: any,key:any) {
			item.selected = event.checked;
			if (item.selected && item.error == 0) {
				that.bulk_ids.push(item.id);
			}
			if (key == (that.temp_result_list.length-1)) {
				console.log(key);
				that.popupLoder = false;
			}
		});
	}

	toggleCheckPreview(id: any, event: any) {
		let that = this;
		//that.bulk_ids=[];
		this.temp_result_list.forEach(function(item: any) {
			if (item.id == id) {
				item.selected = event.checked;
				if (item.selected && item.error == 0) {
					that.bulk_ids.push(item.id);
					//elements[0].classList.add('show');
				} else {
					var index = that.bulk_ids.indexOf(item.id);
					that.bulk_ids.splice(index, 1);
					if (that.bulk_ids.length == 0) {
						//elements[0].classList.remove('show');
					}
				}
			}
			if (that.bulk_ids.length == 1) {
				that.bulk_ids.forEach(function(item_id: any) {
					if (item_id == item.id) {
						that.individualRow = item;
					}
				});
			}
			that.selectedAll = false;
		});
	}

	ImportProductData(form: any) {
		if (this.bulk_ids.length > 0) {
			var msg = 'Are you sure to import selected products?';
			this.dialogsService.confirm('Warning', msg).subscribe(res => {
				if (res) {
					this.popupLoder = true;
					let post_data: any = {};
					let product_imported_data = this._cookieService.getObject('product_imported_data');
					const importType = product_imported_data['importType'];
					post_data.filename = product_imported_data['imported_filename'];
					post_data.website_id = this.globalService.getWebsiteId();
					post_data.category_id = product_imported_data['selected_category_id'];
					post_data.with_category = product_imported_data['with_category'];
					post_data.selected_ids = this.bulk_ids.join(); // convert array to string for selected ids
					this._productService.show_all_imported_data(post_data, importType).subscribe(
						data => {
							this.popupLoder = false;
							this.globalService.deleteTab(this.tabIndex, this.parentId);
						},
						err => {
							this.popupLoder = false;
							this.globalService.showToast('Something went wrong. Please try again.');
						},
					);
				}
			});
		} else {
			this.dialogsService.alert('Error', ' Please select atleast one record!').subscribe(res => {});
		}
	}
	view_panel(id) {
	}
}

@Component({
	templateUrl: './templates/export-file.html',
	providers: [Global, ProductService],
})
export class ExportProductComponent implements OnInit {
	public errorMsg: string = '';
	public formModel: any = {};
	public download_url: any;
	public sample_csv: any;
	public file_data: any;
	public website_id_new: any;
	public company_id_new: any;
	public formLink: any;
	public importOpt: any;
	constructor(private _globalService: GlobalService,
		public dialog: MatDialog,
		private dialogRef: MatDialogRef<ExportProductComponent>,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		this.formLink = this.data;
		//this.formModel = Object.assign({}, this.data);
	}

	ngOnInit() {
		this.download_url = window.location.protocol + '//' + window.location.hostname + ':8062' + this.formLink;
		this.sample_csv = window.location.protocol + '//' + window.location.hostname + ':8062' + this.formLink;
		this.importOpt = 'xls';
	}

	closeDialog() {
		this.dialogRef.close();
	}
} 