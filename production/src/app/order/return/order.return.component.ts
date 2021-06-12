import { Component,ElementRef, OnInit, Inject, Optional, AfterViewInit, Input, OnChanges, SimpleChange, DoCheck } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog, MatAutocompleteModule } from '@angular/material';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { Global } from '../../global/service/global';
import { MatTooltipModule } from '@angular/material/tooltip';
import { DomSanitizer } from '@angular/platform-browser';
import { PaginationInstance } from 'ngx-pagination';
import { DialogsService } from '../../global/dialog/confirm-dialog.service';
import { DOCUMENT } from '@angular/platform-browser';
import { GlobalVariable } from '../../global/service/global';
import { AddEditTransition, AddEditStepFlipTransition } from '../.././addedit.animation';
import { ReturnService } from './order.return.service';
import { OrderService } from '../order/order.order.service';
import * as moment from 'moment';
import { ColumnLayoutComponent } from '../../global/grid/app.grid-global.component';
import { ViewChild} from '@angular/core';
import {VERSION} from '@angular/material';
import { FormControl } from '@angular/forms';
import {MatSelect} from '@angular/material';

import { Subject } from 'rxjs';
import { take, takeUntil } from 'rxjs/operators';
import { ReplaySubject } from 'rxjs';
import { DeliverymanagerService } from '../../operations/delivery-manager/deliverymanager.service';

interface Bank {
    id: string;
    name: string;
   }
@Component({
	selector: 'my-app',
	templateUrl: `./templates/return_list.html`,
	providers: [Global, ReturnService,DeliverymanagerService],
})
export class ReturnComponent implements OnInit, AfterViewInit {
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
	public filter_date:any;
	//////////// start date picker  ///////////////////////////
	public selected: any;
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
	isInvalidDate = (m: moment.Moment) => {
		return this.invalidDates.some(d => d.isSame(m, 'day'))
	}
	
	rangeClicked(range) {
		//this.AppplyDate(range);
	}
	
	datesUpdated1(range) {
		this.AppplyDate(range);
	}

	AppplyDate(range) {
		const myObjStr = JSON.stringify(range);
		const selected_dates = JSON.parse(myObjStr);
		let selectedStartDate = this.globalService.convertDate(selected_dates.startDate, 'yyyy-MM-dd')+ ' 00:00:00';
		let selectedEndDate = this.globalService.convertDate(selected_dates.endDate, 'yyyy-MM-dd')+ ' 23:59:59';
		this.filter_date = selectedStartDate + '##' + selectedEndDate;
		if (selected_dates.startDate != null && selected_dates.endDate != null) {
			this.generateGrid(0, '', '', '', '');
		}
	}
		//////////// start date picker  ///////////////////////////
	constructor(
	   private globalService: GlobalService,
	   private global: Global,
	   private _router: Router,
	   private sanitizer: DomSanitizer,
	   private dialogsService: DialogsService,
	   private elRef:ElementRef,
	   private _cookieService:CookieService,
	   public dialog: MatDialog,
	   private _ordersService:ReturnService,
	   public _DeliverymanagerService:DeliverymanagerService,
	   @Inject(DOCUMENT) private document: any
	) { 
		this.tabIndex = +globalService.getCookie('active_tabs');
		this.parentId = globalService.getParentId(this.tabIndex);
		this.maxDate = moment().add(2, 'weeks');
		this.minDate = moment().subtract(3, 'days');
		this.alwaysShowCalendars = true;
		this.keepCalendarOpeningWithRange = true;
		this.showRangeLabelOnInput = true;
		this.selected = {
			startDate: moment().subtract(30, 'days'),
			endDate: moment().subtract(0, 'days')
		};
	}
	public response : any;
	public errorMsg: string;
	public successMsg: string;
	public bulk_ids:any = [];
	public pagination:any = {};
	public pageIndex : number = 0;
	public pageList : number = 0;
	public sortBy:any = '';
	public sortOrder:any = '';
	public sortClass:any = '';
	public sortRev:boolean = false;
	public selectedAll:any=false;
	public stat:any = {};
	public result_list:any=[];
	public total_list:any=[];
	public cols:any=[];
	public layout: any = [];
	public add_btn : string;
	public post_data = {};
	public page: number = 1;
	public filter: string = '';
	public maxSize: number = 10;
	public directionLinks: boolean = true;
	public autoHide: boolean = false;
	public config: any = {};
	public permission:any=[];
	public show_btn:any={'add':true,'edit':true,'delete':true,'block':true};
	public userId:any;
	public individualRow:any={};
	public search_text:any;
	public childData:any={};
	///////// DATE RANGE //////////////
	public date_range:any={};
	public mainInput = {
		start: moment().subtract(3, 'month'),
		end: moment()
	}
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
  //////////////////////////Initilise////////////////////////////
   ngOnInit(){
		let userData=this._cookieService.getObject('userData');
		this.userId = userData['uid'];
		this.warehouse_id = userData['warehouse_id'];
		this.childData = {
		  table: 'EngageboostOrdermaster',
		  heading : 'Order Returns',
		  ispopup:'N',
		  tablink:'return',
		  screen:'return_list',
		  tabparrentid:this.parentId,
		}
		let selectedStartDate = this.globalService.convertDate(this.selected.startDate, 'yyyy-MM-dd')+' 00:00:00';
		let selectedEndDate = this.globalService.convertDate(this.selected.endDate, 'yyyy-MM-dd')+' 23:59:59';
		this.filter_date = selectedStartDate + '##' + selectedEndDate;
		this.generateGrid(0,'','','','');
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
		let selectedStartDate = this.globalService.convertDate(this.selected.startDate, 'yyyy-MM-dd')+' 00:00:00';
		let selectedEndDate = this.globalService.convertDate(this.selected.endDate, 'yyyy-MM-dd')+' 23:59:59';
		this.filter_date = selectedStartDate + '##' + selectedEndDate;
	 setTimeout(() => {
	   this.globalService.showLoaderSpinner(true);
	 });
   }
	// Approve and Reject for return approval...
	processRequest(status:boolean, id:number, custom_order_id:string) {
		let warning_msg:string = (status)?'approve':'decline';
		this.dialogsService.confirm('Warning', `Do you really want to ${warning_msg} return `+custom_order_id ).subscribe(res => {
			if(res) {
				let req_data:any = {};
				req_data.website_id = this.globalService.getWebsiteId();
				req_data.type_of_return_status = (status)?'Processing':'Declined';
				req_data.order_id = id;
				this.globalService.showLoaderSpinner(true);
				this._ordersService.returnRequestProcess(req_data).subscribe(
					data => {
						if(data.status){
							this.globalService.showToast(data.message);
							this.generateGrid(0,'','','','');
						} else {
							this.dialogsService.alert('Error', data.message).subscribe(res => {});
						}
					},
					err => console.log(err),
					 ()=>{
					   this.globalService.showLoaderSpinner(false);
					}
				);
			}
		});
	}

	/////////////////////////Grid//////////////////////////////////////////////
	generateGrid(reload:any,page:any,sortBy:any,filter:any,search:any,is_export:number=0){
		// search = search.trimLeft();
		if(search == '') {
			this.search_text = '';
		} else {
			this.search_text = search;
		}
	  let elements: NodeListOf<Element> = this.document.getElementsByClassName('action-box');
	  elements[0].classList.remove('show');
	  this.bulk_ids=[];
	  this.individualRow={};
	  this.total_list=[];
	  this.selectedAll=false;
	  this.filter=filter;
	  this.pagination.total_page=0;
	  this.config={};
	  this.page = page;
	  let that = this;
	  if(reload){
		this.date_range = {
			start_date: moment().subtract(3, 'month'),
			end_date: moment()
		}
		this.mainInput = {
		  start: moment().subtract(3, 'month'),
		  end: moment()
		}
	  }
		if(sortBy!='' && sortBy!=undefined){ 
		  if(this.sortRev){
			this.sortOrder = '-'
			this.sortRev = !this.sortRev;
			this.sortClass = 'icon-down';
		  }else{
			this.sortOrder = '+'
			this.sortRev = !this.sortRev;
			this.sortClass = 'icon-up';
		  }
		}

		this.post_data={
			"model": this.childData.table,
			"screen_name": this.childData.screen,
			"userid":this.userId,
			"search":search,
			"order_by":sortBy,
			"order_type":this.sortOrder,
			"return_status":this.filter,
			'export':is_export,
			'website_id': this.globalService.getWebsiteId(),
			'date': this.filter_date,
			"advanced_search": this.advanced_search,
			"warehouse_id": this.warehouse_id
		}

	  this.globalService.showLoaderSpinner(true);
			this._ordersService.doGridOrderReturnRequest(this.post_data,page).subscribe(data => {
				this.response = data;
				let that = this;
				this.total_list=[];
				if(this.response.count>0){
					this.result_list = this.response.results[0].result;
				  	this.result_list.forEach(function(item:any) {
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
						
						if(item.return_status == 'Partial Returned'){
							item.return_status_name = 'status-box partial_return';
						}else if(item.return_status == 'Full Returned'){
							item.return_status_name = 'status-box full_return';
						}

						///////////  amount formating with currency //////////////
						let currencyCode = item.currency_code;
						if(currencyCode == '') {
							currencyCode = 'AED';
						}
	
						if(item.net_amount || item.gross_amount || item.gross_discount_amount || item.tax_amount || item.shipping_cost){
							item.net_amount = currencyCode + " " + item.net_amount.toFixed(2);
							item.gross_amount = currencyCode + " " + item.gross_amount.toFixed(2);
							item.gross_discount_amount = currencyCode + " " + item.gross_discount_amount.toFixed(2);
							item.tax_amount = currencyCode + " " + item.tax_amount.toFixed(2);
							item.shipping_cost = currencyCode + " " + item.shipping_cost.toFixed(2);
						}
				  	});
				  	for (var i = 0; i < this.response.count; i++) {
						this.total_list.push(i);
				  	}
				} else {
				  	this.result_list =[];
				}

			    this.cols = this.response.results[0].applied_layout;
				this.layout = this.response.results[0].layout;

			    this.pagination.total_page = this.response.per_page_count;
			    this.pageList = this.response.per_page_count;
			    this.stat.pending = this.response.results[0].pending;
			    this.stat.declined = this.response.results[0].declined;
			    this.stat.processing = this.response.results[0].processing;
			    this.stat.completed = this.response.results[0].completed;
			    this.stat.all = this.response.results[0].all;
			    this.add_btn = this.response.results[0].add_btn;
			    this.config.currentPageCount = this.result_list.length
			    this.config.currentPage = page
			    this.config.itemsPerPage = this.response.page_size;
			    this.permission=this.response.results[0].role_permission;
			 },
			   err => console.log(err),
			  ()=>{
				 this.globalService.showLoaderSpinner(false);
			   }
			);

	}

	// NEW fILTER STRAT
	load_fiter_column(){
		let data:any={};
		data.model=this.childData.table;
		data.website_id=this.globalService.getWebsiteId();
		data.search= this.formModel.field_name;
		data.screen_name=this.childData.screen;
		data.exclude=this.exclude_arr;
		console.log('data');
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
		this.generateGrid(0, '', '', '', '');
		this.load_fiter_column();
	this.exclude_arr=[];
	}
	get_data(data :any,index:number){
		this.selectArr=[];
		var element = this.document.getElementById('meta_keywordbox');
		element.classList.add("show");
		console.log(data);
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
						this.formModel.search_data=this.globalService.convertDate(this.formModel.search_data, 'yyyy-MM-dd'); 
				}
				this.Advancefilter={'field':this.formModel.field_name,'comparer':this.formModel.search_type,'key':this.formModel.search_data,'name':this.formModel.field_name, 'show_name':this.formModel.field_name_show,'key2':this.formModel.update_key,'input_type':this.formModel.input_type,'field_id':this.formModel.field_id}
				this.advanced_search.push(this.Advancefilter);
				this.generateGrid(0, '', '', '', '');
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
				console.log(this.field_arr);
				
		}else{
				this.globalService.showToast('Please enter value');
		}
		
	}
	change_search_val(item:any){
		if(this.formModel.input_type=='multi_select'){
				this.show_data.push(item);
				let data=this.show_data.join();
				this.formModel.update_key=data;
		}else{

				this.formModel.update_key=item;
		}
		this.formModel.temp_name=item;
	}
	remove_filter(index:number){
		let remove_val=this.advanced_search.splice(index,1);
		console.log('remove_val');
		console.log(remove_val);
		console.log(this.exclude_arr);

		const items = this.exclude_arr;
		const valueToRemove = remove_val[0].field_id;
		this.exclude_arr = items.filter(item => item !== valueToRemove)  
		console.log(this.exclude_arr);

	this.generateGrid(0, '', '', '', '');
	}

	show_options() {
		this.search_type_option=true;
	}

	cancel_filter() {
		let elements: NodeListOf < Element > = this.document.getElementsByClassName('meta_keywordbox');
		elements[0].classList.remove('show');  
		this.generateGrid(0, '', '', '', '');
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
	refreshReturn() {
        this.selected = {
            startDate: moment().subtract(30, 'days'),
            endDate: moment().subtract(0, 'days')
        }; // reset calender
        // this.AppplyDate(this.selected);
        let selectedStartDate = this.globalService.convertDate(this.selected.startDate, 'yyyy-MM-dd') + ' 00:00:00';
        let selectedEndDate = this.globalService.convertDate(this.selected.endDate, 'yyyy-MM-dd') + ' 23:59:59';
        this.filter_date = selectedStartDate + '##' + selectedEndDate;
        this.generateGrid(0, '', '', '', '');
    }

	////////////////////////Delete/Block/Unblock///////////////////////////////
	updateStatusAll(type:number,id:number) {
		  if(id) {
			let that=this;
			that.bulk_ids=[];
			that.bulk_ids.push(id);
		  }
		  if(type==2){var msg='Do you really want to delete selected records?'; var perm=this.permission.delete;var msgp='You have no permission to delete!';}  
		  else if(type==1){var msg='Do you really want to block selected records?';var perm=this.permission.block;var msgp='You have no permission to block!';}
		  else{var msg='Do you really want to unblock selected records?';var perm=this.permission.block;var msgp='You have no permission to unblock!';}
		  if(perm=='Y'){
			  if(this.bulk_ids.length>0){
				  this.dialogsService.confirm('Warning', msg).subscribe(res => {
						if(res){
						  this.global.doStatusUpdate(this.childData.table,this.bulk_ids,type).subscribe(
							   data => {
								   this.response = data;
								   this.globalService.showToast(this.response.Message);
								   this.generateGrid(0,'','','','');
								 },
							   err => console.log(err),
							   function(){
							   }
							);
						}
					  });
			}
			else
			{
				  this.dialogsService.alert('Error', 'Select Atleast One Record!').subscribe(res => {});
			}
		}
		  else{
			this.dialogsService.alert('Permission Error', msgp).subscribe(res => {});
		   }      

	}
	////////////////////////////Check/Uncheck//////////////
	toggleCheckAll(event:any){
		let elements: NodeListOf<Element> = this.document.getElementsByClassName('action-box');
			  let that=this;
			  that.bulk_ids=[];
			this.selectedAll = event.checked;
			this.result_list.forEach(function(item:any){
			  item.selected = event.checked;  
			  if(item.selected){
			  that.bulk_ids.push(item.id);
			  elements[0].classList.add('show');
			  }
			  else{
			  elements[0].classList.remove('show');
			  }  
			});
			let myelement: NodeListOf < Element > = this.document.getElementsByClassName('action-box orderfilter');
			myelement[0].classList.remove('show');
	} 
	toggleCheck(id:any,event:any){
	let elements: NodeListOf<Element> = this.document.getElementsByClassName('action-box');
		let that=this;
		//that.bulk_ids=[];
		this.result_list.forEach(function(item:any){
			if(item.id==id){
			item.selected = event.checked;  
			if(item.selected)
		{
			that.bulk_ids.push(item.id);
			elements[0].classList.add('show');
		}
		else{
			var index = that.bulk_ids.indexOf(item.id);
					that.bulk_ids.splice(index, 1);
					if(that.bulk_ids.length==0){
					elements[0].classList.remove('show');
					} 
		}  
			}
			if(that.bulk_ids.length==1){
			that.bulk_ids.forEach(function(item_id:any){
					if(item_id==item.id){
						that.individualRow=item;
						}
						});
				} 
				that.selectedAll=false;     

		});
		let myelement: NodeListOf < Element > = this.document.getElementsByClassName('action-box orderfilter');
		myelement[0].classList.remove('show');
	}
  	/////////////////////////Filter Grid//////////////////////
  
  	updateGrid(isdefault:any){
	this.global.doGridFilter('EngageboostOrdermaster',isdefault,this.cols,"list").subscribe(
	   data => {
		   this.response = data;
		   this.generateGrid(0,'','','','');
		 },
	   err => console.log(err),
	   function(){
	   }
	);
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
	
	dialogRefAssignDriver: MatDialogRef<AssignDriverComponent> | null;
		
	assign_driver(id:number,shipment_id:number,e){
		let data: any = {}
		data.return_id= id;
		data.shipment_id= shipment_id;
		data.warehouse_id= e.order_products[0].assign_wh;
		// alert(data.warehouse_id)
		this.dialogRefAssignDriver = this.dialog.open(AssignDriverComponent, { data: data ,height: 'auto',width: '500px'});
		this.dialogRefAssignDriver.afterClosed().subscribe(result => {
			console.log(result);
			if(result != undefined) {
				this.updateGrid(0);
			}
			this.updateGrid(0);
		});
	}
	
}


@Component({
	templateUrl: './templates/assign_driver.html',
	providers: [Global],
})
export class AssignDriverComponent implements OnInit {
	public formModel: any = {};
	public tabIndex: number;
	public parentId: number = 0;
	public ipaddress: any;
	public orderInfo:any = {};
	constructor(
		public _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _cookieService: CookieService,
		public dialog: MatDialog,
		private global:Global,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any={},
		private dialogRef: MatDialogRef<AssignDriverComponent>,
	) {
		this.ipaddress = _globalService.getCookie('ipaddress')
		let website_id = this._globalService.getWebsiteId();
		this.getAllDrivers(data.return_id,data.shipment_id);
		this.formModel.order_id = data.return_id
		this.formModel.shipment_id = data.shipment_id
	}

	ngOnInit() {
	
	}
	// return_driver_id, return_delivery_date, order_id, shipment_id
	addEdit(formData) {
		let postdata = formData.value;
		postdata.order_id = this.formModel.order_id;
		postdata.shipment_id = this.formModel.shipment_id;

		var dateString = postdata.return_delivery_date;
		var myDate = new Date(dateString);
		//add a day to the date
		myDate.setDate(myDate.getDate() + 1);
		
		postdata.return_delivery_date=myDate;
		
		if(postdata.return_driver_id != undefined) {
			this.global.getWebServiceData('create_assign_vehicle_return', 'POST', postdata, '').subscribe(res => {
				if (res.status == 1) {
					this._globalService.showToast(res.message);
					this.closeDialog();
				}
			}, err => {
	
			})
			this.closeDialog();
		} else {
			this._globalService.showToast('Please select any driver');
		}
	}

	getAllDrivers(order_id, shipment_id:number){
		let data={
			"website_id": this._globalService.getWebsiteId(),
			"shipment_id": shipment_id,
			"order_id":order_id,
			"warehouse_id": this.data.warehouse_id

		}
		this.global.getWebServiceData('assign_vehicle_return', 'POST', data, '').subscribe(res => {
			if (res.status == 1) {
				this.formModel.drivers = res.api_status.available_driver;
				this.formModel.return_delivery_date=res.api_status.return_delivery_date;
				this.formModel.return_driver_id=res.api_status.return_driver_id;
			}
		}, err => {
		})
	}

	closeDialog() {
		this.dialogRef.close();
	}
}

@Component({
	templateUrl: './templates/view_order_return.html',
	providers: [OrderService, DeliverymanagerService],
	animations: [AddEditTransition],
	host: {
		'[@AddEditTransition]': ''
	},
})
export class ViewOrderReturnComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public userId:any;
	public add_edit: any = '';
	public channel_list: any = [];
	public payment_method_list: any = [];
	public billing_country_list: any = [];
	public billing_state_list: any = [];
	public shipping_country_list: any = [];
	public shipping_state_list: any = [];
	public customer_list: any = [];
	public selected_products_ids: any = [];
	public cart_list: any = [];
	public orderDetails: any = {};
	public quantitiesArr: any = {};
	public orderData:any = {};
	public selected_coupon_code :string = '';
	public taxSettings:any;
	public ipaddress: any;
	public orderInfo:any = {};
	public is_disable_save:boolean = true;
	constructor(
		private _orderService: OrderService,
		public _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _cookieService: CookieService,
		public dialog: MatDialog,
		private global:Global
	) {
		this.ipaddress = _globalService.getCookie('ipaddress')
		let website_id = this._globalService.getWebsiteId();
		this.formModel.return_order_type = 1;
		this.loadTaxSettings(website_id);
	}

	ngOnInit() {
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		let website_id = this._globalService.getWebsiteId();
		let userData=this._cookieService.getObject('userData');
		this.userId = userData['uid'];
		this.formModel.created_date = new Date();
		this.formModel.payment_date = new Date();
		this.formModel.currencyCode = '$';
		this.sub = this._route.params.subscribe(params => {
			this.formModel.id = +params['id']; // (+) converts string 'id' to a number
			this.formModel.order_id = this.formModel.id;
		});
		this.orderInfo = { orderId: this.formModel.id, activityType : 1}
		this.global.getWebServiceData('view_order_return','GET','',this.formModel.id).subscribe(order => {
			if(order["status"] == '1') {
				this.orderData = order["data"];
				// cds working....
				if(this.orderData.return_status!='Authorized' && this.orderData.return_status != 'Processing' && this.orderData.return_status != 'Driver Assigned') {
					this.is_disable_save = false;
				}
				let that = this;
				this.orderData.order_products.forEach(function(inner_item:any, inner_index:number) {
					//console.log('Yes coming');
					inner_item.return_warehouse_id = inner_item.assign_wh;
					inner_item.damaged = 0;
				});
				
				let assign_wh = this.orderData.assign_wh;
				this.orderData.warehouse.forEach(function(warehouse_item:any) {
					if(warehouse_item.id == assign_wh) {
						that.orderData.warehouse_name = warehouse_item.name;
						// console.log(that.orderData.warehouse_name);
					}
				});
				this.getCurrencyDetails(this.orderData.currency_code);
			} else {
				this._globalService.showToast("Something went wrong. Please try later.");
			}
		}, err => {

		})
	}

	loadTaxSettings(website_id) {
		this.global.getTaxSettings(website_id).subscribe(result => {
			if(result["status"] == 1) {
					this.taxSettings = result["api_status"];
					// console.log(this.taxSettings);
				}
			},err => {
		});
	}

	getCurrencyDetails(currencyCode) {
		if(currencyCode == '' || currencyCode == null) {
			currencyCode = 'INR';
		}
		let data:any = {};
		data.currency_code = currencyCode;
		this.global.getWebServiceData('currency-by-code','POST',data,'').subscribe(result => {
			if(result["status"] == 1) {
				this.formModel.currency = result["data"]["id"]+'SSS'+result["data"]["currencysymbol"];
				this.currencySettings(this.formModel.currency);
			} else { // show error message
				this._globalService.showToast(result["message"]);
			}
		}, err => {
		});
	}

	currencySettings(currencyData:any) {
		const currencyArr = currencyData.split("SSS"); // string contains 'SSS'
		this.formModel.currency_id = currencyArr[0];
		this.formModel.currencyCode = currencyArr[1];
	}

	saveViewOrderReturn(from:any){
		console.log(this.formModel);
		let data:any = { };
		// this.ipaddress = _globalService.getCookie('ipaddress');
		data.website_id = this._globalService.getWebsiteId();
		data.return_order_type = this.formModel.return_order_type;
		data.order_id = this.formModel.id;
		data.userId = this.userId;
		data.return_note = this.formModel.return_note;
		data.return_others_reason = this.formModel.return_others_reason;
		data.trent_picklist_id = this.orderData.trent_picklist_id;
		data.customer_id = this.orderData.customer.id;
		data.custom_order_id = this.orderData.custom_order_id;
		let save_order_data_arr: any = [];
		let orderCount:number = 0;
		let returnCount:number = 0;
		let returnType:string = '';
		this.orderData.order_products.forEach(function(inner_item:any, inner_index:number) {
			//console.log('Yes coming');
			orderCount += inner_item.quantity;
			returnCount = returnCount+inner_item.returns+inner_item.shortage;
			let selected_order_list: any = {};
			selected_order_list['id'] = inner_item.id;
			selected_order_list['warehouse_id'] = inner_item.assign_wh;
			selected_order_list['shipment'] = inner_item.shipment;
			selected_order_list['quantity'] = inner_item.quantity;
			selected_order_list['shortage'] = inner_item.shortage;
			selected_order_list['returns'] = inner_item.returns;
			selected_order_list['grn_quantity'] = inner_item.grn_quantity;
			selected_order_list['product'] = inner_item.product;
			selected_order_list['product_id'] = inner_item.product.id;
			selected_order_list['damaged'] = inner_item.damaged;
			selected_order_list['return_warehouse_id'] = inner_item.return_warehouse_id;
			save_order_data_arr.push(selected_order_list);
		});
		if(orderCount == returnCount) {
			returnType = 'FR';
		} else {
			returnType = 'PR';
		}
		//console.log(this.formModel.orderData[0].selected_order);
		data.returnType = returnType;
		data.shipmentOrderProduct = save_order_data_arr;
		// console.log(data);
		this._globalService.showLoaderSpinner(true);
		this.global.getWebServiceData('view_order_return','PUT', data, data.order_id).subscribe(result => {
			if(result["status"] == 1) {
				this.successMsg = result["message"];
				this.is_disable_save = false;
				this._globalService.showLoaderSpinner(false);
			} else { // show error message
				this._globalService.showToast(result["message"]);
				this._globalService.showLoaderSpinner(false);
			}
		}, err => {
		});
	}
}

@Component({
  templateUrl: 'templates/order_return_view.html',
  providers: [ReturnService,Global]
})
export class OrderReturnViewComponent implements OnInit {
	public tabIndex: number;
	public parentId: number = 0;
	public formModel:any = {};
	public errorMsg:string = '';
	public errors_product:any = [];
	private sub: any;
	public activity_comments:string = null;
	public activities_list:any = [];
	public is_loaded: boolean = false;
	public returnId:number = 0;
	public is_disable_save:boolean = false;
	constructor(
		public _globalService:GlobalService, 
		private _cookieService: CookieService, 
		private _ordersService: ReturnService,
		private _router: Router,
		private _route: ActivatedRoute,
		public dialog: MatDialog,
		public dialogsService: DialogsService,
		private _global:Global, 
	    @Inject(DOCUMENT) private document: any
	) {
		this.tabIndex = +_globalService.getCookie('active_tabs');
		this.parentId = _globalService.getParentTab(this.tabIndex);
	}

	ngOnInit(){
	
	
	this.sub = this._route.params.subscribe(params => { // pick id from the route url
		 this.returnId = +params['return_id']; // (+) converts string 'id' to a number
	});
	this.orderLoad(this.returnId);
  }
  //order onload
  orderLoad(returnId:number){
	let that = this;
	this._globalService.showLoaderSpinner(true);
	let req_data:any = {};
	req_data.website_id = this._globalService.getWebsiteId();
	req_data.return_id = returnId;
	this._ordersService.viewOrderReturn(req_data).subscribe(
		data => {
			let that = this;
			this.formModel = data.api_status;
			this.formModel['return_details'] = data.return_details;
			this.formModel.return_details.created = data.return_created_date;
			if(this.formModel.return_details.return_status=='Processing'){
			  this.is_disable_save = true;
			}
			this.formModel['products'] = data.products;
			this.formModel['order_calc'] = {
			  gross_amount: 0,
			  shipping_cost: 0,
			  tax_amount: 0,
			  net_amount: 0,
			}; 
			this.formModel.products.forEach((item: any,index:number)=>{
			  
			  this.calcAmt(index);
			}); 
			this.formModel['order_status_text'] = this._globalService.get_order_status(data.merchant_order_status);
			this.formModel['activities'] = data.activity;
			this.formModel.activities.forEach(function(item:any){
			  let activity_date_time = item.activity_date;
			  item['activity_date'] = activity_date_time.substr(0,activity_date_time.indexOf(' '));
			  item['activity_time'] = activity_date_time.substr(activity_date_time.indexOf(' ')+1);
			});

			this.activities_list = [];
			this.formModel.activities.forEach(function(item:any){
			  const grouped = that.groupBy(that.formModel.activities, key => key.activity_date);
			  that.activities_list.push({'date': item.activity_date,'notes':grouped.get(item.activity_date)});
			});

			this.activities_list = this.removeDuplicates(that.activities_list, 'date');
			this.is_loaded = true;
		},
		err => {
			that._globalService.showToast('Something went wrong. Please try again.');
			this._globalService.showLoaderSpinner(false);
		},
		()=>{
		   //completed callback
		   this._globalService.showLoaderSpinner(false);
		}
	);
  }

  removeDuplicates(originalArray, objKey) {
	var trimmedArray = [];
	var values = [];
	var value;
	for(var i = 0; i < originalArray.length; i++) {
	  value = originalArray[i][objKey];

	  if(values.indexOf(value) === -1) {
		trimmedArray.push(originalArray[i]);
		values.push(value);
	  }
	}
	return trimmedArray;
  }
  groupBy(list, keyGetter) {
	const map = new Map();
	list.forEach((item) => {
		const key = keyGetter(item);
		const collection = map.get(key);
		if (!collection) {
			map.set(key, [item]);
		} else {
			collection.push(item);
		}
	});
	return map;
  }

  // calculate amount on quantity, cpu and discount change
  calcAmt(index: number){
	//*************  Calculate product amounts based on index  **************//
	//calculate gross amount
	this.formModel.products[index]['returns'] = (isNaN(this.formModel.products[index]['returns'])?0:this.formModel.products[index]['returns']);
	this.formModel.products[index]['product_price'] = (isNaN(this.formModel.products[index]['product_price'])?0:this.formModel.products[index]['product_price']);
	this.formModel.products[index]['gross_amt'] = (this.formModel.products[index]['returns'] * this.formModel.products[index]['product_price']);

	//calculate net amount
	this.formModel.products[index]['net_amt'] = (this.formModel.products[index]['gross_amt'] - this.formModel.products[index]['product_discount_price']);

	this.formModel.order_calc.gross_amount += this.formModel.products[index]['net_amt'];
	this.formModel.order_calc.shipping_cost += parseFloat(this.formModel.products[index]['shipping_price']);
	this.formModel.order_calc.tax_amount += parseFloat(this.formModel.products[index]['product_tax_price']) * this.formModel.products[index]['returns'];

	this.formModel.order_calc.net_amount = this.formModel.order_calc.gross_amount+this.formModel.order_calc.shipping_cost+this.formModel.order_calc.tax_amount;

  }

  postComments(comment:string = ''){

	let that = this;
	if(comment.trim()!='' || comment.trim()!=null){
	  
	  let user_ip: string = (this._globalService.getCookie('ipaddress'))?this._globalService.getCookie('ipaddress'):'';
	  let data:any = { "order_id":this.formModel.id,"activity_comments":comment, "ip_address":user_ip, "user_id": this._globalService.getUserId() }
	  
	  this._ordersService.postComments(data).subscribe(
		data => {
			this.orderLoad(this.returnId);
		},
		err => {
			that._globalService.showToast('Something went wrong. Please try again.');
		},
		function(){
		   //completed callback
		}
	  );

	  this.activity_comments = null;
	}
  }

  checkReturnQty(qty:number,stock:number,damaged:number){

	let tot_qty = stock + damaged;
	if(tot_qty>qty){
	  this.is_disable_save = false;
	  this._globalService.showToast('Stock & Damaged quantity must be equal to return quantity');
	}else{
	  this.is_disable_save = true;
	}
  }

  saveReturn(from:any){
	let data:any = { };
	data.website_id = this._globalService.getWebsiteId();
	data.stock = this.formModel.products[0].stock;
	data.damaged = this.formModel.products[0].damaged;
	data.return_id = this.returnId;
	this._globalService.showLoaderSpinner(true);  
	this._ordersService.saveReturn(data).subscribe(
	  data => {
		  this.orderLoad(this.returnId);
	  },
	  err => {
		  this._globalService.showToast('Something went wrong. Please try again.');
		  this._globalService.showLoaderSpinner(false);
	  },
	  ()=>{
		 //completed callback
		 this._globalService.showLoaderSpinner(false);
	  }
	);
  }
}

@Component({
	templateUrl: './templates/refund_order.html',
	providers: [OrderService],
	animations: [AddEditTransition],
	host: {
		'[@AddEditTransition]': ''
	},
})
export class RefundOrderComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public userId:any;
	public add_edit: any = '';
	public channel_list: any = [];
	public payment_method_list: any = [];
	public billing_country_list: any = [];
	public billing_state_list: any = [];
	public shipping_country_list: any = [];
	public shipping_state_list: any = [];
	public customer_list: any = [];
	public selected_products_ids: any = [];
	public cart_list: any = [];
	public orderDetails: any = {};
	public quantitiesArr: any = {};
	public orderData:any = {};
	public selected_coupon_code :string = '';
	public taxSettings:any;
	public ipaddress: any;
	public orderInfo:any = {};
	public is_disable_save: boolean = true;
	public return_note_arr_full = [
				{id: 1, text: 'Wrong Product Selected'},
				{id: 2, text: 'Wrong Price'},
				{id: 3, text: 'Ordered By Mistake'},
				{id: 4, text: 'Others'}
		   ];
	public return_note_arr_partial = [
		{id: 6, text: 'Damaged product'},
		{id: 7, text: 'Expiry product'},
		{id: 8, text: 'Poor Quality'},
		{id: 9, text: 'Wrong Product'},
		{id: 10, text: 'Duplicate/Extra  Product'},
		{id: 11, text: 'Wrong Price'},
		{id: 11, text: 'Requirement Changes'}
	]
	constructor(
		private _orderService: OrderService,
		public _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _cookieService: CookieService,
		public dialog: MatDialog,
		private global:Global
	) {
		this.ipaddress = _globalService.getCookie('ipaddress')
		let website_id = this._globalService.getWebsiteId();
		this.formModel.return_order_type = 1;
		this.loadTaxSettings(website_id);
	}

	ngOnInit() {
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		let website_id = this._globalService.getWebsiteId();
		let userData=this._cookieService.getObject('userData');
		this.userId = userData['uid'];
		this.formModel.created_date = new Date();
		this.formModel.payment_date = new Date();
		this.formModel.currencyCode = '$';
		this.sub = this._route.params.subscribe(params => {
			this.formModel.id = +params['id']; // (+) converts string 'id' to a number
			this.formModel.order_id = this.formModel.id;
			this.formModel.return_order_type = +params['canType']; // (+) converts string 'id' to a number
		});
		this.orderInfo = { orderId: this.formModel.id, activityType : 1}
		this.global.getWebServiceData('refund_orders','GET','',this.formModel.id).subscribe(order => {
			if(order["status"] == '1') {
				this.orderData = order["data"];
				let that = this;
				// console.log(this.orderData.order_products);
				if(this.orderData.order_status != 1 && this.orderData.order_status != 4) {
					this.is_disable_save = false;
				}
				this.orderData.order_products.forEach(function(inner_item:any, inner_index:number) {
					//console.log('Yes coming');
					if(that.formModel.return_order_type == 1) {
						inner_item.quantityrefund = inner_item.grn_quantity;
					} else {
						inner_item.quantityrefund = 0;
					}
				});
				this.getCurrencyDetails(this.orderData.currency_code);
			} else {
				this._globalService.showToast("Something went wrong. Please try later.");
			}
		}, err => {

		})
	}

	loadTaxSettings(website_id) {
	 this.global.getTaxSettings(website_id).subscribe(result => {
		  if(result["status"] == 1) {
			  this.taxSettings = result["api_status"];
			  // console.log(this.taxSettings);
			}
		} , err => {

		});
	 }

	getCurrencyDetails(currencyCode) {
		if(currencyCode == '' || currencyCode == null) {
			currencyCode = 'INR';
		}
		let data:any = {};
		data.currency_code = currencyCode;
		this.global.getWebServiceData('currency-by-code','POST',data,'').subscribe(result => {
			if(result["status"] == 1) {
				this.formModel.currency = result["data"]["id"]+'SSS'+result["data"]["currencysymbol"];
				this.currencySettings(this.formModel.currency);
			} else { // show error message
				this._globalService.showToast(result["message"]);
			}
		}, err => {
		});
	}

	currencySettings(currencyData:any) {
		const currencyArr = currencyData.split("SSS"); // string contains 'SSS'
		this.formModel.currency_id = currencyArr[0];
		this.formModel.currencyCode = currencyArr[1];
	}

	saveRefundOrder(from:any){
		let data:any = { };
		data.website_id = this._globalService.getWebsiteId();
		data.return_order_type = this.formModel.return_order_type;
		data.order_id = this.formModel.id;
		data.userId = this.userId;
		data.return_note = this.formModel.return_note;
		data.return_others_reason = this.formModel.return_others_reason;
		data.trent_picklist_id = this.orderData.trent_picklist_id;
		data.customer_id = this.orderData.customer.id;
		data.custom_order_id = this.orderData.custom_order_id;
		let save_order_data_arr: any = [];
		console.log(this.orderData);		
		this.orderData.order_products.forEach(function(inner_item:any, inner_index:number) {
			//console.log('Yes coming');
			let selected_order_list: any = {};
			selected_order_list['id'] = inner_item.id;
			selected_order_list['warehouse_id'] = inner_item.assign_wh;
			selected_order_list['shipment'] = inner_item.shipment;
			selected_order_list['quantity'] = inner_item.quantity;
			selected_order_list['shortage'] = inner_item.shortage;
			selected_order_list['returns'] = inner_item.returns;
			selected_order_list['deleted_quantity'] = inner_item.deleted_quantity;
			selected_order_list['grn_quantity'] = inner_item.grn_quantity;
			selected_order_list['product'] = inner_item.product;
			selected_order_list['product_id'] = inner_item.product.id;
			selected_order_list['quantityrefund'] = inner_item.quantityrefund;
			selected_order_list['return_request_message'] = inner_item.return_request_message;
			save_order_data_arr.push(selected_order_list);
		});
		//console.log(this.formModel.orderData[0].selected_order);
		data.shipmentOrderProduct = save_order_data_arr;
		// console.log(data);
		this._globalService.showLoaderSpinner(true);
		this.global.getWebServiceData('refund_orders','PUT', data, data.order_id).subscribe(result => {
			if(result["status"] == 1) {
				this.successMsg = result["message"];
				this._globalService.showLoaderSpinner(false);
				this.is_disable_save = false;
			} else { // show error message
				this._globalService.showToast(result["message"]);
				this._globalService.showLoaderSpinner(false);
			}
		}, err => {
		});
	}
}

@Component({
	templateUrl: './templates/activity.html',
	selector : 'order-activity',
	providers: [OrderService],    
})
export class OrderActivityComponent implements OnInit {
	@Input() orderInfo: { orderId:number, activityType:any };
	public formModel: any = {};
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public order_activity:any = [];
	public orderId:any ;   
	constructor(
		private _orderService: OrderService,
		public _globalService: GlobalService,
		private _cookieService: CookieService,
		private global: Global,
		@Inject(DOCUMENT) private document: any
	) {
	}
	ngOnInit() {
		let orderId = +this.orderInfo.orderId;
		if(orderId) {
			this._orderService.getOrderActivity(orderId).subscribe(
				response => {
					if (response["status"] == '1') {
						this.order_activity = response["api_status"];
					}
				}, err => {

				}
			);
		}
	}

	postActivity() {
		let userData = this._cookieService.getObject('userData');
		let orderId = +this.orderInfo.orderId;
		let activity_msg = '';
		if(this.formModel.activity_msg) {
			activity_msg = this.formModel.activity_msg.trim();
		}
		if (orderId > 0 && activity_msg != '') {
			let data: any = {};
			data.user_id = userData['uid'];
			data.activity_comments = activity_msg;
			data.activity_type = this.orderInfo.activityType;
			data.username = userData['first_name'] + ' ' + userData['last_name'];
			data.order_id = orderId;
			data.status = 0;
			this.global.getWebServiceData('post_activity', 'POST', data, '').subscribe(res => {
				if (res["status"] == '1') {
					this.ngOnInit();
					this.formModel.activity_msg = ''; // reset the activity fields
				}
			}, err => {

			})
		}
	}

	postOrderActivities(event) {
		if (event.keyCode == 13) {
			this.postActivity();
		}
	}
}