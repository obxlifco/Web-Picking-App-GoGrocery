import { Component, ElementRef, OnInit, Input, Inject, AfterViewInit, Optional } from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { Global } from '../../global/service/global';
import { Router, ActivatedRoute } from '@angular/router';
import { MatTooltipModule } from '@angular/material/tooltip';
import { DomSanitizer } from '@angular/platform-browser';
import { PaginationInstance } from 'ngx-pagination';
import { DialogsService } from '../../global/dialog/confirm-dialog.service';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { DOCUMENT } from '@angular/platform-browser';
import { GlobalVariable } from '../../global/service/global';
import { AddEditTransition, AddEditStepFlipTransition } from '../.././addedit.animation';
import { OrderAddEditComponent, ManageTagsComponent } from '../../order/order/order.order.addedit.component';
import { OrderService } from './order.order.service';
import * as moment from 'moment';
import { ColumnLayoutComponent } from '../../global/grid/app.grid-global.component';
import { ViewChild } from '@angular/core';
import { VERSION } from '@angular/material';
import { FormControl } from '@angular/forms';
import { MatSelect } from '@angular/material';
import { Subject } from 'rxjs';
import { take, takeUntil } from 'rxjs/operators';
import { ReplaySubject } from 'rxjs';
interface Bank {
	id: string;
	name: string;
}

@Component({
	selector: 'my-app',
	templateUrl: `./templates/order.html`,
	providers: [Global, OrderService],
})
export class OrderComponent implements OnInit {
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
	public colSpanCount: number = 4;
	public tabIndex: number;
	public parentId: number = 0;
	public filter_date = '';
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
		'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
		'This Year': [moment().startOf('year'), moment().endOf('year')],
		'Last Year' : [moment().subtract(1, 'year').startOf('year'), moment().subtract(1, 'year').endOf('year')]
	}
	//////////// start date picker  ///////////////////////////
	constructor(
		private globalService: GlobalService,
		private global: Global,
		private _router: Router,
		private sanitizer: DomSanitizer,
		private dialogsService: DialogsService,
		private elRef: ElementRef,
		private _cookieService: CookieService,
		public dialog: MatDialog,
		private _orderService: OrderService,
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
	public selectedAllTags: any = false;
	public selectedAllStatus: any = false;
	public selectedAllAssignedWarehouse: any = false;
	public timeSlotAll: any = false;
	public selectAll
	public stat: any = {};
	public result_list: any = [];
	public total_list: any = [];
	public cols: any = [];
	public layout: any = [];
	public add_btn: string;
	public post_data = {};
	public page: number = 1;
	public maxSize: number = 10;
	public directionLinks: boolean = true;
	public autoHide: boolean = false;
	public config: any = {};
	public permission: any = [];
	public userId: any;
	public individualRow: any = {};
	public search_text: any;
	public childData: any = {};
	public show_item_wise_order: any = 0;
	public tag_list: any = [];
	public warehouse_list: any = [];
	public status_list: any = [];
	public action_status_list: any = [];
	public tag_ids: any = [];
	public order_status_ids: any = [];
	public assigned_manager: any = [];
	public action_order_status_ids: any = [];
	public zoneList: any = [];
	
	public tagsIdsArr:any=[];

	public order_delivery_slot: any = [];
	public timeSlotIds: any = [];

	public daterange: any = {};
	public options: any = {
		locale: {
			format: 'YYYY-mm-dd'
		},
		alwaysShowCalendars: false,
	};

	//Shipment and pilist validation...by cds...
	// public create_shipment_error: number = 0;
	public create_picklist_error: number = 0;
	public assign_warehouse_error: number = 0;

	showSkeletonLoaded: boolean = false;
	public temp_result = [];
	public temp_col = [];
	public formModel: any = {};
	public elasticSearch:any = {};

	field_arr = [];
	ConditionArr = [];
	filterArr = [];
	public search_type_option = false;
	advanced_search = [];
	input_type: any;
	selectArr: any = [];
	temp_key: any = [];
	advanced_search_temp = [];
	filter = {};
	Advancefilter = {};
	order_information: any = [];
	item_information: any = [];
	customer_information: any = [];
	delivery_information: any = [];
	other_information: any = [];
	order_summary_information: any = [];
	show_data: any = [];
	remove_field_index: number;
	exclude_arr: any = [];
	public isDateFilter=0;
	public warehouse_id: any;

	public fromStartDate: any;
	public toEndDate: any;

	ngOnInit() {

		let userData = this._cookieService.getObject('userData');
		this.userId = userData['uid'];
		this.warehouse_id = userData['warehouse_id'];
		this.childData = {
			table: 'EngageboostOrdermaster',
			heading: 'Order',
			ispopup: 'N',
			tablink: 'orders',
			tabparrentid: this.parentId,
			screen: 'list',
			disableSortBy: ['created_day']
		}
		this.selected = {
			startDate: moment().subtract(30, 'days'),
			endDate: moment().subtract(0, 'days')
		};
		this.AppplyDate(this.selected, 'y');

		this.globalService.loadSkeletonChange$.subscribe(
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
		
		this.generateGrid(0, '', '', '', '', this.show_item_wise_order);
		
		this.formModel.search_type = 1;
		this.formModel.search_data = '';

		this.globalService.orderFilter$.subscribe(
			(value) => {
				this.generateGrid(0, '', '', '', '', this.show_item_wise_order);
			}
		);

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
	
	isInvalidDate = (m: moment.Moment) => {
		return this.invalidDates.some(d => d.isSame(m, 'day'))
	}

	rangeClicked(range) {
		//this.AppplyDate(range, 'n');
	}
	
	datesUpdatedApply(range) {
		//console.log(range);
		this.AppplyDate(range, 'n');
	}

	AppplyDate(range, load_first: any = 'n') {
		const myObjStr = JSON.stringify(range);
		const selected_dates = JSON.parse(myObjStr);
		//console.log(selected_dates);
		//console.log('=============Start Date ===============');
		let selectedStartDate = this.globalService.convertDate(selected_dates.startDate, 'yyyy-MM-dd');
		//console.log('=============End Date ===============');
		let selectedEndDate = this.globalService.convertDate(selected_dates.endDate, 'yyyy-MM-dd');
		//this.filter_date = selectedStartDate + '##' + selectedEndDate+" 23:59:59";
		this.filter_date = selectedStartDate + '##' + selectedEndDate;
		if (selectedStartDate != null && selectedEndDate != null && load_first != 'y') {
			this.isDateFilter=1;
			this.generateGrid(0, '', '', '', '', this.show_item_wise_order);
		}
	}



	/////////////////////////Grid//////////////////////////////////////////////

	generateGrid(reload: any, page: any, sortBy: any, filter: any, search: any, show_item_wise_order: any) {

		let warehouse_status  = this._cookieService.getObject('warehouse_status');

		var side_panel = this.document.getElementById('side_panel');
		side_panel.classList.remove("show");
		let userData = this._cookieService.getObject('userData');
		let websiteId = this.globalService.getWebsiteId();
		var page_size = 0;
		this.globalService.skeletonLoader(true);
		let filterQuery = [];
		let filterQuery2 = [];
		let filterQuery3 = [];
		if(search == '' || search == null) {
			this.search_text = '';
		} else {
			this.search_text = search;
			if(search) {
				search = search.trim();
			}
		}
		let elements: NodeListOf<Element> = this.document.getElementsByClassName('action-box');
		elements[0].classList.remove('show');
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
			this.sortBy = sortBy;
		}
		
		if (this.filter_date === 'null##null') {
			this.selected = {
				startDate: moment().subtract(30, 'days'),
				endDate: moment().subtract(0, 'days')
			}; // reset calender
			this.AppplyDate(this.selected, 'y');
		}

		
		this.post_data = { 
			"model": this.childData.table, 
			"screen_name": this.childData.screen, 
			"userid": this.userId, 
			"search": this.search_text.trim(),
			"order_by": this.sortBy, 
			"order_type": this.sortOrder, 
			"status": filter, 
			"date": this.filter_date,
			"warehouse_id": this.warehouse_id,
			"website_id": this.globalService.getWebsiteId(),
			"advanced_search": this.advanced_search,
			"warehouse_status": warehouse_status
		}

		let dateArr = this.filter_date.split("##");
		let fromDate = dateArr[0];
		let toDate = dateArr[1];

		this.fromStartDate = dateArr[0];
		this.toEndDate = dateArr[1];

		// ELSATIC QUERY GENERATION END
		let matchArr = [];
		/////////////// loading default conditions for grid /////////////////
		let conditions: any;
		// conditions.buy_status = 1;
		let innerMatch: any = {};
		// console.log(this.warehouse_id);
		if (this.warehouse_id && this.warehouse_id != '') {
			innerMatch.match = {'assign_to':this.userId};
			matchArr.push(innerMatch);
		}

		if (filterQuery && filterQuery.length > 0) {
			matchArr = matchArr.concat(filterQuery);
		}
		
		if (search != '') { // pushing search conditions
			search = search.replace("/", "\\", search);
			conditions = {}
			conditions.query = search;
			innerMatch = {};
			innerMatch.query_string = conditions;
			matchArr.push(innerMatch);
		}
		
	
		let extraFilter = JSON.stringify(matchArr);
		//FOR TYPE 2
		let extraFilter2 = JSON.stringify(filterQuery2);
		let extraFilter3 = JSON.stringify(filterQuery3);

		let searchConditions:any={};
		searchConditions.extraFilter = extraFilter; 
		searchConditions.extraFilter2 = extraFilter2; 
		searchConditions.fromDate = fromDate; 
		searchConditions.toDate = toDate;
		this.elasticSearch.exportConditions = searchConditions;
		

		this.global.doGrid(this.post_data, page).subscribe(
			data => {
				this.response = data;
				this.total_list=[];
				if (this.response.count > 0) {
					this.result_list = this.response.results[0].result;
					let that = this;
					this.result_list.forEach(function (item: any) {
						//////////// start the status settings //////////////////////
						if (item.order_status == '99' && item.buy_status == '1') {
							item.order_status = 'Waiting Approval';
							item.class_name = 'status-box approval';
						} else if (item.order_status == '20' && item.buy_status == '1') {
							item.order_status = 'Approved';
							item.class_name = 'status-box pendings';
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
							// alert(item.buy_status)
							// alert(item.shipping_status);

							item.order_status = 'Failed';
							item.class_name = 'status-box failed denger';
						}
						else if (item.order_status == '9999' && item.buy_status == '1') {
							item.order_status = 'Hold';
							item.class_name = 'status-box hold';
						}else if (item.order_status == '21' && item.buy_status == '1') {
							item.order_status = 'Payment Initiated';
							item.class_name = 'status-box hold';
						} else {
							item.order_status = 'Invoiced';
							item.class_name = 'status-box invoiced';
						}

						//console.log(item.shipping_status);
						if (item.shipping_status == 'Pending') {
							item.shipping_class_name = 'status-box pendings';
						} else if (item.shipping_status == 'Picking') {
							item.shipping_class_name = 'status-box packed';
						} else if (item.shipping_status == 'Invoicing') {
							item.shipping_class_name = 'status-box invoiced';
						} else if(item.shipping_status == 'Packed' && item.order_status != 'Failed') {
	                       item.shipping_class_name = 'status-box ready_to_dispatch';
	                    } else if (item.shipping_status == 'Create Shipment') {
							item.shipping_class_name = 'status-box processing';
						} else if (item.shipping_status == 'Shipment Processing') {
							item.shipping_class_name = 'status-box shipment_processing';
						} else if (item.shipping_status == 'Ready to Ship') {
							item.shipping_class_name = 'status-box ready_to_ship';
						} else if (item.shipping_status == 'Shipped') {
							item.shipping_class_name = 'status-box shipped_new';
						} else if (item.order_status == 'Failed' && item.shipping_status == 'Packed') {
							item.shipping_class_name = 'status-box denger';
						} else {
							item.shipping_class_name = 'status-box completed';
						}

						if(item.return_status == 'Partial Returned'){
							item.return_status_name = 'status-box partial_return';
						}else if(item.return_status == 'Full Returned'){
							item.return_status_name = 'status-box full_return';
						}
						//console.log(item.shipping_class_name);
						//////////////  end status settings /////////////////// 
						if (item.created != '') {
							item.created_day = that.globalService.convertDate(item.created, 'EEEE');
						}
						if (item.created != '') {
							item.created = that.globalService.convertDate(item.created, 'dd-MM-yyyy h:mm a');
						}

						if (item.time_slot_date != '') {
							let timeSlotArr = item.time_slot_date.split("-");
							let slot_date = timeSlotArr[2]+"-"+timeSlotArr[1]+"-"+timeSlotArr[0];
							item.time_slot_date = slot_date;
							//item.time_slot_date = item.time_slot_date; //that.globalService.convertDate(item.time_slot_date, 'dd-MM-yyyy');
						}
						///////////  amount formating with currency //////////////
						let currencyCode = item.currency_code;
						if(currencyCode == '') {
							currencyCode = 'AED';
						}
						item.gross_amount = currencyCode + " " + item.gross_amount.toFixed(2);
						item.shipping_cost = currencyCode + " " + item.shipping_cost.toFixed(2);
						item.cart_discount = currencyCode + " " + item.cart_discount.toFixed(2);
						item.gross_discount_amount = currencyCode + " " + item.gross_discount_amount.toFixed(2);
						item.tax_amount = currencyCode + " " + item.tax_amount.toFixed(2);
						item.net_amount = currencyCode + " " + item.net_amount.toFixed(2);
					})
					for (let i = 0; i < this.response.count; i++) {
						this.total_list.push(i);
					}
				} else {
					this.result_list = [];
				}

				this.cols = this.response.results[0].applied_layout;
				this.layout = this.response.results[0].layout;

				console.log(this.cols);
				console.log(this.layout);

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
				
				this.globalService.skeletonLoader(false);
				// Fired click event as data not loading....
				let myelement: HTMLElement = this.document.getElementsByClassName('autoclick');
				myelement[0].click();
			},err=>{
				console.log(err)
				this.globalService.skeletonLoader(false);
			}
		);

		
	}


	generateGridOLd(reload: any, page: any, sortBy: any, filter: any, search: any, show_item_wise_order: any) {
		var side_panel = this.document.getElementById('side_panel');
		side_panel.classList.remove("show");
		let userData = this._cookieService.getObject('userData');
		let websiteId = this.globalService.getWebsiteId();
		var page_size = 0;
		this.globalService.skeletonLoader(true);
		let filterQuery = [];
		let filterQuery2 = [];
		let filterQuery3 = [];
		if(search == '' || search == null) {
			this.search_text = '';
		} else {
			this.search_text = search;
			if(search) {
				search = search.trim();
			}
		}
		let elements: NodeListOf<Element> = this.document.getElementsByClassName('action-box');
		elements[0].classList.remove('show');
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
			this.sortBy = sortBy;
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

		// ELSATIC QUERY GENERATION START
		this.advanced_search.forEach(element => {
			let search_field = element.field;
			let input_type = element.input_type;
			let search_value = element.key;
			var match = 'match';
			if (search_field == 'delivery_email_address') {
				match = 'match_phrase_prefix';
			}
			if (search_field == 'custom_order_id') {
				match = 'match_phrase';
			}

			if (element.comparer == 1) {
				if (input_type == 'multi_select') {
					match = 'terms';
					filterQuery.push({ [match]: { [search_field]: search_value } });

				} else {

					filterQuery.push({ [match]: { [search_field]: search_value } });
				}
			}
			if (element.comparer == 2) {
				if (input_type == 'multi_select') {
					match = 'terms';
					filterQuery2.push({ [match]: { [search_field]: search_value } });

				} else {

					filterQuery2.push({ [match]: { [search_field]: search_value } });
				}
			}
			if (element.comparer == 3) {
				filterQuery.push({ match_phrase_prefix: { [search_field]: search_value } });
			}
			if (element.comparer == 4) {
				filterQuery.push({ wildcard: { [search_field + '.keyword']: '*' + search_value } });
			}
			if (element.comparer == 5) {
				filterQuery.push({ wildcard: { [search_field + '.keyword']: '*' + search_value + '*' } });
			}
			if (element.comparer == 6) {
				filterQuery2.push({ wildcard: { [search_field + '.keyword']: '*' + search_value + '*' } });
			}
			if (element.comparer == 7) {
				if (search_field == 'time_slot_date' || search_field == 'created') {
					let d = this.globalService.convertDate(search_value, 'yyyy-MM-dd');
					let elasticData = { "range": { [search_field]: { "gte": d } } }
					filterQuery.push(elasticData);
				} else {

					filterQuery.push({ "range": { [search_field]: { "gte": search_value } } });
				}
			}
			if (element.comparer == 8) {
				if (search_field == 'time_slot_date' || search_field == 'created') {
					let d = this.globalService.convertDate(search_value, 'yyyy-MM-dd');
					let elasticData = { "range": { [search_field]: { "lte": d } } }
					filterQuery.push(elasticData);
				} else {
					filterQuery.push({ "range": { [search_field]: { "lte": search_value } } });
				}
			}
		});
		// ELSATIC QUERY GENERATION END
		let matchArr = [];
		/////////////// loading default conditions for grid /////////////////
		let conditions: any;
		// conditions.buy_status = 1;
		let innerMatch: any = {};
		// console.log(this.warehouse_id);
		if (this.warehouse_id && this.warehouse_id != '') {
			innerMatch.match = {'assign_to':this.userId};
			matchArr.push(innerMatch);
		}

		if (filterQuery && filterQuery.length > 0) {
			matchArr = matchArr.concat(filterQuery);
		}
		
		if (search != '') { // pushing search conditions
			search = search.replace("/", "\\", search);
			conditions = {}
			conditions.query = search;
			innerMatch = {};
			innerMatch.query_string = conditions;
			matchArr.push(innerMatch);
		}

		this.post_data = {
			"model": this.childData.table,
			"screen_name": this.childData.screen,
			"userid": this.userId,
		}

		let dateArr = this.filter_date.split("##");
		let fromDate = dateArr[0]
		let toDate = dateArr[1]
		this.global.loadColumnVisibility(this.post_data).subscribe(data => {
			this.response = data;

			this.cols = this.response.results[0].applied_layout;
			this.layout = this.response.results[0].layout;

			this.colSpanCount = this.cols.length;
			this.pageList = this.response.per_page_count;
			this.stat.active = this.response.results[0].active;
			this.stat.inactive = this.response.results[0].inactive;
			this.stat.all = this.response.results[0].all;
			this.add_btn = this.response.results[0].add_btn;
			this.permission = this.response.results[0].role_permission;
			page_size = this.response.page_size;
			///// startig query string filer ////////////////
			if(this.sortBy != 'id' && this.sortBy != 'quantity' && this.sortBy != 'gross_amount' && this.sortBy != 'net_amount' && this.sortBy != 'shipping_cost' && this.sortBy != 'cart_discount' && this.sortBy != 'tax_amount') {
				sortBy = this.sortBy + '.keyword';
			} else {
				sortBy = this.sortBy;
			}
			
			if (this.sortBy == '') {
				sortBy = 'id';
			}
			let orderType = 'desc';
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
			this.elasticSearch.exportConditions = searchConditions;
			var start_end:any={};
			if(this.isDateFilter==1) {
				start_end='"gte":"' + fromDate + '","lte":"' + toDate + '"';
				// console.log(start_end);
			} else {
				start_end='"gte":"' + fromDate + '"';
				// console.log(start_end);
			}
			let elasticData = '{"query":{"bool":{"must":' + extraFilter + ', "must_not":' + extraFilter2 + ',"filter":{"range":{"created":{'+start_end+'}}}}},"from": ' + from + ',"size": ' + page_size + ',"sort": [{"' + sortBy + '": "' + orderType + '"}]}';
			// let elasticData = '{"query":{"bool":{"must":' + extraFilter + ', "must_not":' + extraFilter2 + ',"filter":{"range":{"created":{"gte":"' + fromDate + '","lte":"' + toDate + '"}}}}},"from": ' + from + ',"size": ' + page_size + ',"sort": [{"' + sortBy + '": "' + orderType + '"}]}';
			this._orderService.loadGridES('orders', page, search, page_size, sortBy, this.sortOrder, elasticData, websiteId).subscribe(listData => {
				let tmpResult = [];
				listData.hits.hits.forEach(function (rows: any) {
					// console.log(rows._source.order_products.length);
					if(rows._source.order_products && rows._source.order_products.length > 0) {
						tmpResult.push(rows._source);
					}
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
						} else if (item.order_status == '20' && item.buy_status == '1') {
							item.order_status = 'Approved';
							item.class_name = 'status-box pendings';
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
							// alert(item.buy_status)
							// alert(item.shipping_status);

							item.order_status = 'Failed';
							item.class_name = 'status-box failed denger';
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
						} else if (item.shipping_status == 'Picking') {
							item.shipping_class_name = 'status-box packed';
						} else if (item.shipping_status == 'Invoicing') {
							item.shipping_class_name = 'status-box invoiced';
						} else if(item.shipping_status == 'Packed' && item.order_status != 'Failed') {
	                       item.class_name = 'status-box ready_to_dispatch';
	                    } else if (item.shipping_status == 'Create Shipment') {
							item.shipping_class_name = 'status-box processing';
						} else if (item.shipping_status == 'Shipment Processing') {
							item.shipping_class_name = 'status-box shipment_processing';
						} else if (item.shipping_status == 'Ready to Ship') {
							item.shipping_class_name = 'status-box ready_to_ship';
						} else if (item.shipping_status == 'Shipped') {
							item.shipping_class_name = 'status-box shipped_new';
						} else if (item.order_status == 'Failed' && item.shipping_status == 'Packed') {
							item.shipping_class_name = 'status-box denger';
						} else {
							item.shipping_class_name = 'status-box completed';
						}
						//console.log(item.shipping_class_name);
						//////////////  end status settings /////////////////// 
						if (item.created != '') {
							item.created_day = that.globalService.convertDate(item.created, 'EEEE');
						}
						if (item.created != '') {
							item.created = that.globalService.convertDate(item.created, 'dd-MM-yyyy h:mm a');
						}

						if (item.time_slot_date != '') {
							item.time_slot_date = that.globalService.convertDate(item.time_slot_date, 'dd-MM-yyyy');
						}
						///////////  amount formating with currency //////////////
						let currencyCode = item.currency_code;
						if(currencyCode == '') {
							currencyCode = 'AED';
						}
						item.gross_amount = currencyCode + " " + item.gross_amount.toFixed(2);
						item.shipping_cost = currencyCode + " " + item.shipping_cost.toFixed(2);
						item.cart_discount = currencyCode + " " + item.cart_discount.toFixed(2);
						item.gross_discount_amount = currencyCode + " " + item.gross_discount_amount.toFixed(2);
						item.tax_amount = currencyCode + " " + item.tax_amount.toFixed(2);
						item.net_amount = currencyCode + " " + item.net_amount.toFixed(2);
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
				this.globalService.skeletonLoader(false);
				let myelement: HTMLElement = this.document.getElementsByClassName('autoclick');
				myelement[0].click();
				this.isDateFilter=0;
			});
		},err=>{
			this.globalService.skeletonLoader(false);
		});
	}

	getWarehouseList() {
		this.warehouse_list = this.warehouse_list;
		//console.log(this.warehouse_list);
	}
	////////////////////////Delete/Block/Unblock///////////////////////////////
	updateStatusAll(type: number, id: number) {
		if (id) {
			let that = this;
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
						this.global.doStatusUpdate(this.childData.table, this.bulk_ids, type).subscribe(data => {
							this.response = data;
							this.globalService.showToast(this.response.Message);
							this.generateGrid(0, '', '', '', '', this.show_item_wise_order);
						}, err => console.log(err), function () { });
					}
				});
			} else {
				this.dialogsService.alert('Error', 'Select Atleast One Record!').subscribe(res => { });
			}
		} else {
			this.dialogsService.alert('Permission Error', msgp).subscribe(res => { });
		}
	}
	////////////////////////////Check/Uncheck//////////////
	toggleCheckAll(event: any) {
		let elements: NodeListOf<Element> = this.document.getElementsByClassName('action-box');
		let that = this;
		that.bulk_ids = [];
		this.selectedAll = event.checked;
		this.result_list.forEach(function (item: any) {
			item.selected = event.checked;
			if (item.selected) {
				that.bulk_ids.push(item.id);
				elements[0].classList.add('show');
			} else {
				elements[0].classList.remove('show');
			}
		});
		that.assign_warehouse_error = this.checkOrdersStatus('Assign');
		that.create_picklist_error = this.checkOrdersStatus('Pending');
		// that.create_shipment_error = this.checkOrdersStatus('Processing');
		let myelement: NodeListOf<Element> = this.document.getElementsByClassName('action-box orderfilter');
		myelement[0].classList.remove('show');
	}
	toggleCheck(id: any, event: any) {
		let elements: NodeListOf<Element> = this.document.getElementsByClassName('action-box edit');
		let that = this;
		this.result_list.forEach(function (item: any) {
			if (item.id == id) {
				item.selected = event.checked;
				if (item.selected) {
					that.bulk_ids.push(item.id);
					that.action_order_status_ids.push(item.order_status);
					elements[0].classList.add('show');
				}
				else {
					var index = that.bulk_ids.indexOf(item.id);
					that.bulk_ids.splice(index, 1);
					if (that.bulk_ids.length == 0) {
						elements[0].classList.remove('show');
					}
				}
			}
			if (that.bulk_ids.length == 1) {
				that.bulk_ids.forEach(function (item_id: any) {
					if (item_id == item.id) {
						that.individualRow = item;
					}
				});
				//console.log(that.individualRow);
			}
			that.selectedAll = false;
		});
		that.assign_warehouse_error = this.checkOrdersStatus('Assign');
		// that.create_shipment_error = this.checkOrdersStatus('Processing');
		that.create_picklist_error = this.checkOrdersStatus('Pending');
		let myelement: NodeListOf<Element> = this.document.getElementsByClassName('action-box orderfilter');
		myelement[0].classList.remove('show');

	}
	close_sidepanel() {
		var side_panel = this.document.getElementById('side_panel');
		side_panel.classList.remove("show");
	}
	// view_panel(id) {
	// 	this.global.getWebServiceData('manage-order-details/' + id, 'GET', '', '').subscribe(result => {
	// 		let res = result.data;
	// 		if (result.status == 1) {
	// 			this.order_information = {
	// 				'created': res.created,
	// 				'order_id': res.custom_order_id,
	// 				'store': res.webshop.name
	// 				// 'quantity':this.item_information.length+1
	// 			};
	// 			this.order_summary_information = {
	// 				'gross_amount': res.shipping_cost,
	// 				'net_amount': res.net_amount,
	// 				'paid_amount': res.paid_amount,
	// 				'shipping_cost': res.shipping_cost,
	// 				'cod_cost': res.cod_charge,
	// 				'tax_amount': res.tax_amount
	// 			};
	// 			this.item_information = res.order_products;
	// 			this.customer_information = res.customer;
	// 			this.delivery_information = {
	// 				'name': res.delivery_name,
	// 				'phone': res.delivery_phone,
	// 				'email': res.delivery_email_address,
	// 				'delivery_street_address': res.delivery_street_address,
	// 				'delivery_street_address1': res.delivery_street_address1,
	// 				'area': res.area_id,
	// 				'country': res.delivery_country_name,
	// 				'state': res.delivery_state_name,
	// 				'city': res.delivery_city,
	// 				'zipcode': res.delivery_postcode,
	// 				'zone': res.zone_name,
	// 				'slot': res.time_slot_id,
	// 				'slot_date': res.time_slot_date
	// 			};
	// 			this.other_information = {
	// 				'payment_method': res.payment_method_name,
	// 				'status': res.received_status,
	// 				'custom_msg': res.custom_msg,
	// 				'pay_txntranid': res.pay_txntranid,
	// 				'currency_code': res.currency_code,
	// 			};
	// 		} else {

	// 		}
	// 	}, err => {

	// 	})
	// 	var side_panel = this.document.getElementById('side_panel');
	// 	side_panel.classList.add("show");
	// }
	// NEW fILTER STRAT
	load_fiter_column() {
		let data: any = {};
		data.model = this.childData.table;
		data.website_id = this.globalService.getWebsiteId();
		data.search = this.formModel.field_name;
		data.screen_name = this.childData.screen;
		data.exclude = this.exclude_arr;
		this.global.getWebServiceData('advanced_filter', 'POST', data, '').subscribe(res => {
			if (res.status == 1) {
				this.field_arr = res.api_status[0];
			}
		}, err => {
			this.globalService.showToast('Something went wrong');
		})

	}
	FiltertoggleCheck(event: any) {
		this.load_fiter_column();
		let elements: NodeListOf<Element> = this.document.getElementsByClassName('action-box orderfilter');
		elements[0].classList.add('show');
		this.formModel.update_key = '';
	}
	CloseFilter(event: any) {
		let elements: NodeListOf<Element> = this.document.getElementsByClassName('action-box orderfilter');
		elements[0].classList.remove('show');
		var element = this.document.getElementById('meta_keywordbox');
		element.classList.remove("show");
		this.advanced_search = [];
		this.formModel.field_name = '';
		this.formModel.search_module = null;
		this.formModel.search_type = 1;
		this.formModel.search_data = null;
		this.generateGrid(0, '', '', '', '', this.show_item_wise_order);
		this.load_fiter_column();
		this.exclude_arr = [];
	}
	get_data(data: any, index: number) {
		this.selectArr = [];
		var element = this.document.getElementById('meta_keywordbox');
		element.classList.add("show");
		this.formModel.field_name_show = data.columns;
		this.formModel.field_id = data.id;
		this.formModel.input_type = data.input_type;
		this.formModel.search_module = data.search_module;
		if (data.field_type == 'int') {
			this.ConditionArr = [
				{ 'type': 1, 'name': 'Equals to' },
				{ 'type': 2, 'name': 'Not Equals to' }
			]
		}
		if (data.field_type == 'float') {
			this.ConditionArr = [
				{ 'type': 1, 'name': 'Equals to' },
				{ 'type': 2, 'name': 'Not Equals to' },
				{ 'type': 7, 'name': 'Geater than' },
				{ 'type': 8, 'name': 'Less than' },
			]
		}
		if (data.field_type == 'date') {
			this.ConditionArr = [
				{ 'type': 1, 'name': 'Equals to' },
				{ 'type': 2, 'name': 'Not Equals to' },
				{ 'type': 7, 'name': 'Geater than' },
				{ 'type': 8, 'name': 'Less than' },
			]
		}
		if (data.field_type == 'string') {
			this.ConditionArr = [
				{ 'type': 1, 'name': 'Equals to' },
				{ 'type': 2, 'name': 'Not Equals to' },
				{ 'type': 3, 'name': 'Starts with' },
				{ 'type': 4, 'name': 'Ends with' },
				{ 'type': 5, 'name': 'Contains' },
				{ 'type': 6, 'name': 'Does not contains' }
			]
		}
		//this.field_arr.splice(index,1);
		this.get_select_data();
		this.load_fiter_column();
		this.remove_field_index = index;

	}
	sendSearchData() {
		var search_data = '';
		search_data = this.formModel.search_data;
		if (search_data) {
			if (this.formModel.search_data == 'n') {
				search_data = 'Active';
			}
			if (this.formModel.search_data == 'y') {
				search_data = 'Inactive';
			}
			if (this.formModel.input_type == 'date') {
				this.formModel.search_data = this.globalService.convertDate(this.formModel.search_data, 'yyyy-MM-dd');
			}
			this.Advancefilter = { 'field': this.formModel.field_name, 'comparer': this.formModel.search_type, 'key': this.formModel.search_data, 'name': this.formModel.field_name, 'show_name': this.formModel.field_name_show, 'key2': this.formModel.update_key, 'input_type': this.formModel.input_type, 'field_id': this.formModel.field_id }
			this.advanced_search.push(this.Advancefilter);
			this.generateGrid(0, '', '', '', '', this.show_item_wise_order);
			let elements: NodeListOf<Element> = this.document.getElementsByClassName('meta_keywordbox');
			elements[0].classList.remove('show');
			this.selectArr = [];
			this.formModel.search_data = null;
			this.formModel.search_module = null;
			this.formModel.update_key = this.formModel.search_data;
			this.formModel.field_name = '';
			this.formModel.search_type = 1;
			this.show_data = [];
			// form.reset();
			// this.load_fiter_column(); 
			this.get_select_data();
			// this.filteredBanksMulti=null;remove_field_index
			let exclude_id = this.field_arr[this.remove_field_index].id;
			this.exclude_arr.push(exclude_id);
			this.field_arr.splice(this.remove_field_index, 1);
		} else {
			this.globalService.showToast('Please enter value');
		}

	}
	change_search_val(item: any) {
		if (this.formModel.input_type == 'multi_select') {
			if (this.show_data.includes(item)) {
				// console.log('Already in');
			} else {
				this.show_data.push(item);
			}
			let data = this.show_data.join();

			this.formModel.update_key = data;
		} else {

			this.formModel.update_key = item;
		}
		this.formModel.temp_name = item;
	}
	remove_filter(index: number) {
		//this._cookieService.putObject('warehouse_status', status);
		let remove_val = this.advanced_search.splice(index, 1);
		const items = this.exclude_arr;
		const valueToRemove = remove_val[0].field_id;
		this.exclude_arr = items.filter(item => item !== valueToRemove)
		this.generateGrid(0, '', '', '', '', this.show_item_wise_order);
	}
	show_options() {
		this.search_type_option = true;
	}
	cancel_filter() {
		let elements: NodeListOf<Element> = this.document.getElementsByClassName('meta_keywordbox');
		elements[0].classList.remove('show');
		this.generateGrid(0, '', '', '', '', this.show_item_wise_order);
		this.formModel.field_name = '';
		this.formModel.search_data = null;
		this.load_fiter_column();

	}
	get_select_data() {
		this.global.getWebServiceData('global_list/' + this.formModel.field_id, 'GET', '', '').subscribe(res => {
			if (res) {
				if (res.status != 0) {
					this.banks = res.results[0].result[0];
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
					let myelement: HTMLElement = this.document.getElementsByClassName('autoclick');
					myelement[0].click();
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
			this.selectArr = [];
		})
	}
	// NEW fILTER END
	/////////////////////////Filter Grid//////////////////////
	updateGrid(isdefault: any) {
		this._orderService.doGridFilter(this.childData.table, isdefault, this.cols, "list").subscribe(data => {
			this.response = data;
			this.generateGrid(0, '', '', '', '', this.show_item_wise_order);
		}, err => console.log(err), function () { });
	}
	
	loadTagMasters() {
		this._orderService.loadTagMasters().subscribe(data => {
			if (data.status == 1) {
				this.tag_list = data.api_status;
			}
			//console.log(this.tag_list);
		}, err => console.log(err), function () { });
	}

	loadWarehouseList() {
		this._orderService.loadWarehouseList().subscribe(data => {
			if (data.status == 1) {
				this.warehouse_list = data.api_status;
			}
			//console.log(this.tag_list);
		}, err => console.log(err), function () { });
	}

	loadStatusMasters() {
		this.status_list = [{
			id: 99,
			name: "Waiting Approval"
		}, {
			id: 0,
			name: "Pending"
		}, {
			id: 100,
			name: "Processing"
		}, {
			id: 1,
			name: "Shipped"
		}, {
			id: 2,
			name: "Cancelled"
		}, {
			id: 4,
			name: "Completed"
		}, {
			id: 5,
			name: "Full Refund"
		}, {
			id: 6,
			name: "Partial Refund"
		}, {
			id: 12,
			name: "Assigned to Showroom"
		}, {
			id: 13,
			name: "Delivered"
		}, {
			id: 16,
			name: "Closed"
		}, {
			id: 18,
			name: "Pending Service"
		}, {
			id: 3,
			name: "Abandoned"
		}, {
			id: 999,
			name: "Failed"
		},];
	}

	loadActionOrderStatus() {
		this.action_status_list = [{
			id: 2,
			name: "Delete"
		},
		{
			id: 4,
			name: "Completed"
		},
		{
			id: 16,
			name: "Closed"
		}
		];
	}
	setOrderStatusAction(event: any, order_status_label: any, order_status: number) {
		let err = 0;
		let err_msg = "";
		if (this.bulk_ids.length > 0) {
			if (order_status_label == 'Completed' && order_status == 4) { // this is for waiting approve orders()         
				this.result_list.forEach(function (item: any) {
					if (item.selected) {
						let selected_order_status = item.order_status;
						if(item.return_status!="") {

						}
						if (selected_order_status != 'Shipped' && (item.return_status == null || item.return_status == "")) {
							err_msg = "Only Shipped/Returned orders can be updated to completed status";
							err++;
						}
					}
				});
				if (err > 0) {
					this.globalService.showToast(err_msg);
				}
				else {
					this.dialogsService.confirm('Warning', "Are you sure to complete selected orders").subscribe(res => {
						if (res) {
							let data: any = {};
							data.order_ids = this.bulk_ids.join();
							data.order_status = 'completed';
							this.updateOrderStatus(data);
							// console.log("Approve Success");
						}
					});
				}
			} else if (order_status_label == 'Pending' && order_status == 0) { // move order to success          
				this.result_list.forEach(function (item: any) {
					if (item.selected) {
						let selected_order_status = item.order_status
						if (selected_order_status != 'Failed' && selected_order_status != 'Abandoned') {
							err_msg = "Only Falied or Abandoned are allowed to move success order";
							err++;
						}
					}
				});
				if (err > 0) {
					this.globalService.showToast(err_msg);
				}
				else {
					this.dialogsService.confirm('Warning', "Are you sure to  move selected orders to success orders").subscribe(res => {
						if (res) {
							let data: any = {};
							data.order_ids = this.bulk_ids.join();
							data.order_status = 'pending';
							this.updateOrderStatus(data);
							// console.log("Failed/Abandoned Success");
						}
					});
				}
			} else if (order_status_label == 'Closed' && order_status == 16) { // Close/Complete the order
				this.result_list.forEach(function (item: any) {
					if (item.selected) {
						let selected_order_status = item.order_status
						if (selected_order_status == 'Pending' || selected_order_status == 'Failed' || selected_order_status == 'Abandoned' || selected_order_status == 'Cancelled' || selected_order_status == 'Closed' || selected_order_status == 'Waiting Approval' || selected_order_status == 'Processing') {
							err_msg = "Only shipped/completed orders can be changed to closed.";
							err++;
						}
					}
				});
				if (err > 0) {
					this.globalService.showToast(err_msg);
				}
				else {
					this.dialogsService.confirm('Warning', "Are you sure to closed the selected orders").subscribe(res => {
						if (res) {
							let data: any = {};
							data.order_ids = this.bulk_ids.join();
							data.order_status = 'closed';
							this.updateOrderStatus(data);
							// console.log("Closed Success");
						}
					});
				}
			} else if (order_status_label == 'Delete' && order_status == 2) { // Cancel the orders
				this.result_list.forEach(function (item: any) {
					if (item.selected) {
						let selected_order_status = item.order_status
						if (selected_order_status == "Shipped" || selected_order_status == "Cancelled" || selected_order_status == "Closed") {
							err_msg = "You can not cancel " + selected_order_status + " order";
							err++;
						}
					}
				});
				if (err > 0) {
					this.globalService.showToast(err_msg);
				} else {
					this.dialogsService.confirm('Warning', "Are you sure to Cancel the selected orders").subscribe(res => {
						if (res) {
							let data: any = {};
							data.order_ids = this.bulk_ids.join();
							data.order_status = 'delete';
							this.updateOrderStatus(data);
							// console.log("Cancel success");
						}
					});
				}
			} else {
				console.log(" Custom order status will goes here.");
			}
		} else {
			this.globalService.showToast("Please select atleast one order");
		}
	}

	menuClosed() {
		var tags = this.tagsIdsArr.filter((v, i, a) => a.indexOf(v) === i);
		if (this.bulk_ids.length > 0) {
			let data: any = {};
			data.order_ids = this.bulk_ids.join();
			data.tag_id = tags.join();
			this._orderService.setOrderTags(data).subscribe(data => {
				this.tagsIdsArr = [];
				if (data.status == 1) {
					this.globalService.showToast(data.message);
				}
				else {
					this.globalService.showToast(data.message);
				}
				setTimeout(() => {
					this.generateGrid(1, '', '', '', '', this.show_item_wise_order);
					this.loadTagMasters();
				}, 500);
			}, err => {
				console.log(err),
					function () { }
			});
		}
		else {
			this.globalService.showToast("Please select atleast one order");
		}
	}

	setTagAction(event: any, tag_name: any, tag_id: number) {
		if (event.checked) {
			this.tagsIdsArr.push(tag_id);
		} else {
			let index = this.tagsIdsArr.indexOf(tag_id)
			this.tagsIdsArr = this.tagsIdsArr.splice(index);
		}
	}

	AssignOrderWarehouse(event: any, manager_name: any, warehouse_id: number, manager_id: number) {
		if (this.bulk_ids.length > 0) {
			let data: any = {};
			let marketPlaceArr: any = [];
			if (this.show_item_wise_order) {
				data.item_ids = this.bulk_ids.join(); // this is for item wise order assing 
			} else {
				data.order_ids = this.bulk_ids.join(); // this is for order assign
			}
			if (warehouse_id > 0) {
				data.assign_wh = warehouse_id;
			} else {
				data.assign_wh = 'none';
			}
			if (manager_id > 0) {
				data.assign_to = manager_id;
			} else {
				data.assign_to = 'none';
			}

			data.manager_name = manager_name;
			this._orderService.assignWarehouse(data).subscribe(data => {
				if (data.status == 1) {
					this.globalService.showToast(data.message);
				} else {
					this.globalService.showToast(data.message);
				}
				// Update data in Elastic....
				this.loadWarehouseList();
				this.bulk_ids.forEach(orderID => {
					var index = this.result_list.map(function (order) { return order.id; }).indexOf(orderID);
					this.result_list[index]['assign_to_name'] = manager_name;
					this.result_list[index]['assign_to'] = manager_id;
					this.result_list[index]['assign_wh'] = warehouse_id;
				});
				this.assign_warehouse_error = this.checkOrdersStatus('Assign');
				this.create_picklist_error = this.checkOrdersStatus('Pending');
				//this.generateGrid(1, '', '', '', '', this.show_item_wise_order);    
			}, err => {
				console.log(err),
					function () { }
			});
		}
		else {
			this.globalService.showToast("Please select atleast one order");
		}
	}

	RemoveWarehouse() {
		if (this.bulk_ids.length > 0) {
			let data: any = {};
			if (this.show_item_wise_order) {
				data.item_ids = this.bulk_ids.join(); // this is for item wise order assing 
			} else {
				data.order_ids = this.bulk_ids.join(); // this is for order assign
			}
			data.assign_wh = "";
			data.assign_to = "";
			data.manager_name = "";
			this._orderService.assignWarehouse(data).subscribe(data => {
				if (data.status == 1) {
					this.globalService.showToast(data.message);
				}
				else {
					this.globalService.showToast(data.message);
				}
				// Update data in Elastic....
				this.loadWarehouseList();
				// this.generateGrid(1, '', '', '', '', this.show_item_wise_order);
				this.bulk_ids.forEach(orderID => {
					var index = this.result_list.map(function (order) { return order.id; }).indexOf(orderID);
					this.result_list[index]['assign_to_name'] = data.manager_name;
					this.result_list[index]['assign_to'] = data.assign_to;
					this.result_list[index]['assign_wh'] = data.assign_wh;
				});
				this.assign_warehouse_error = this.checkOrdersStatus('Assign');
				this.create_picklist_error = this.checkOrdersStatus('Pending');
			}, err => {
				console.log(err),
			   function () { }
			});
		} else {
			this.globalService.showToast("Please select atleast one order");
		}
	}
	updateOrderStatus(data: any) {
		this._orderService.updateOrderStatus(data).subscribe(data => {
			if (data.status == 1) {
				this.globalService.showToast(data.message);
			} else {
				this.globalService.showToast(data.message);
			}
			this.generateGrid(1, '', '', '', '', this.show_item_wise_order);
		}, err => {
			console.log(err),
		    function () { 
		   }
		});
	}
	
	refreshOrderList() {
		this._cookieService.putObject('warehouse_status', "");
		setTimeout(() => {
			this.globalService.skeletonLoader(true);
		});
		this.tag_ids = [];
		this.order_status_ids = [];
		this.assigned_manager = [];
		this.timeSlotIds = [];
		this.selected = {
			startDate: moment().subtract(30, 'days'),
			endDate: moment().subtract(0, 'days')
		}; // reset calender
		this.AppplyDate(this.selected);
		this.ngOnInit(); // due to two timesloading...
		//this.generateGrid(1, '', '', '', '', this.show_item_wise_order);
	}

	loadOrderDeliverySlot() {
		const data: any = {};
		data.delivery_date = this.filter_date;
		this.global.getWebServiceData('order-delivery-slot', 'POST', data, '').subscribe(result => {
			if (result["status"] == 1) {
				this.order_delivery_slot = result.time_slot;
				//console.log(result.time_slot);
			}
		}, err => {

		});
	}

	dialogRefTags: MatDialogRef<ManageTagsComponent> | null;
	openPopTags(id: any) {
		this.dialogRefTags = this.dialog.open(ManageTagsComponent, {
			data: id
		});
		this.dialogRefTags.afterClosed().subscribe(result => { });
	}

	checkOrdersStatus(order_status_check: string = 'Pending') {
		let selected_orders: any = this.result_list.filter((order) => this.bulk_ids.indexOf(order.id) > -1 && order.order_status != order_status_check);
		if (order_status_check == 'Processing') {
			selected_orders = this.result_list.filter((order) => this.bulk_ids.indexOf(order.id) > -1 && order.shipping_status != 'Create Shipment');
		} else if (order_status_check == 'Assign') {
			selected_orders = this.result_list.filter((order) => this.bulk_ids.indexOf(order.id) > -1 && (order.assign_wh == null || order.assign_wh == 0));
		} 
		// console.log(selected_orders)
		return selected_orders.length;
	}

	createPicklist() {
		if (this.checkOrdersStatus('Pending') > 0) {
			this.dialogsService.alert('Error', 'You can\'t create shipment for the Processing Order.').subscribe(res => { });
		} else {
			let that = this;
			let err = 0;
			let err_msg = "";
			if (that.bulk_ids.length > 0) {
				let WarehouseManager: any = [];
				let marketPlaceArr: any = [];
				// console.log('***********************');
				// console.log(this.result_list);
				// console.log('***********************');
				this.result_list.forEach(function (item: any) {
					if (item.selected) {
						let selected_order_status = item.order_status
						WarehouseManager.push(item.assign_to); // pushing warehouse manager to arr
						marketPlaceArr.push(item.webshop_id); // pushing warehouse manager to arr
						//console.log(selected_order_status);
						if (selected_order_status != 'Pending') {
							err_msg = "Shipment can be created for Pending orders only.";
							err++;
						}
						let assignTo = item.assign_to;
						if (assignTo == '' || assignTo == null) {
							err_msg = "Please assign warehouse manager for shipment.";
							err++;
						}
					}
				});

				let uniqueManager = Array.from(new Set(WarehouseManager)); // Assign unique warehouse manager
				//console.log(uniqueManager)
				if (uniqueManager.length > 1 && err == 0) {
					err_msg = "You can't create shipment from different warehouse.";
					err++;
				}
				let uniqueMarketplace = Array.from(new Set(marketPlaceArr));
				//console.log(uniqueMarketplace)
				if (uniqueMarketplace.length > 1 && err == 0) {
					err_msg = "You can't create shipment from different marketplace.";
					err++;
				}
				if (err > 0) {
					this.globalService.showToast(err_msg);
				} else {
					let selectedIds = that.bulk_ids;
					let data: any = {};
					if (that.show_item_wise_order) {
						data.shipmentType = 'ItemWise';
					} else {
						data.shipmentType = 'OrderWise';
					}
					data.website_id = this.globalService.getWebsiteId();
					data.company_id = this.globalService.getCompanyId();
					data.shipment_id = 0;
					data.userId = this.globalService.getUserId();
					data.selectedIds = selectedIds.join(",");
					this.dialogsService.confirm('Create Picklist', 'Do you want to create shipment for selected order(s).').subscribe(res => {
						if (res) {
							this._orderService.generatePicklist(data).subscribe(
								data => {
									if (data.status == 1) {
										let shipment_id = data.picklist_details.shipment_id;
										this.globalService.addTab('shipment', 'shipment/grn/' + shipment_id, 'Picking', 193)
										this._router.navigate(['/shipment/grn/' + shipment_id]);
									} else {
										this.globalService.showToast(data.message);
									}
								},
								err => {

								}, // callback function
								function () {
								});
						}
					});
				}
			} else {
				that.globalService.showToast("Please select atleast one order");
			}
		}
	}
	// Old not using now
	createShipment() {
		let that = this;
		let err = 0;
		let err_msg = "";
		let error_message = "";
		if (that.bulk_ids.length > 0) {
			let WarehouseManager: any = [];
			let marketPlaceArr: any = [];
			this.result_list.forEach(function (item: any) {
				if (item.selected) {
					let order_status = item.order_status;
					let shipping_status = item.shipping_status;
					WarehouseManager.push(item.assign_to); // pushing warehouse manager to arr
					marketPlaceArr.push(item.webshop_id); // pushing warehouse manager to arr
					//console.log(order_status);
					if (shipping_status != "Create Shipment") {
						err_msg = "You can't create shipment for the picklist status " + shipping_status + " Order.";
						err++;
					}
					if (order_status != "Processing" && order_status != "Reschedule") {
						err_msg = "You can't create shipment for the " + order_status + " Order.";
						err++;
					}
				}
			});

			let uniqueManager = Array.from(new Set(WarehouseManager)); // Assign unique warehouse manager
			//console.log(uniqueManager)
			if (uniqueManager.length > 1 && err == 0) {
				err_msg = "You can't create shipment from different warehouse.";
				err++;
			}
			let uniqueMarketplace = Array.from(new Set(marketPlaceArr));
			//console.log(uniqueMarketplace)
			if (uniqueMarketplace.length > 1 && err == 0) {
				err_msg = "You can't create shipment from different marketplace.";
				err++;
			}

			if (err > 0) {
				this.globalService.showToast(err_msg);
			} else {
				let selectedIds = that.bulk_ids;
				let data: any = {};
				if (that.show_item_wise_order) {
					data.shipmentType = 'ItemWise';
				} else {
					data.shipmentType = 'OrderWise';
				}
				data.website_id = this.globalService.getWebsiteId();
				data.company_id = this.globalService.getCompanyId();
				data.userId = this.globalService.getUserId();
				data.selectedIds = selectedIds.join(",");
				//console.log(data)
				this.dialogsService.confirm('Create Shipment', 'Do you want to create shipment for selected order(s).').subscribe(res => {
					if (res) {
						this._orderService.generateShipment(data).subscribe(
							data => {
								if (data.status == 1) {
									let shipment_id = data.shipment_id;
									//console.log(shipment_id)
									this.globalService.addTab('shipment', 'shipment/delivery_planner/' + shipment_id, 'Shipment', 194)
									this._router.navigate(['/shipment/delivery_planner/' + shipment_id]);
								} else {
									this.globalService.showToast(data.message);
								}
							},
							err => {
							}, // callback function
							function () {
							});
					}
				});
			}
		} else {
			that.globalService.showToast("Please select atleast one order");
		}
	}


	dialogRefColumnLayout: MatDialogRef<ColumnLayoutComponent> | null;
	loadColumnLayout() {
		let data: any = {}
		data["column"] = this.cols;
		data["layout"] = this.layout;
		this.dialogRefColumnLayout = this.dialog.open(ColumnLayoutComponent, { data: data });
		this.dialogRefColumnLayout.afterClosed().subscribe(result => {
			if (result != undefined) {
				this.cols = result;
				this.updateGrid(0);
			}
		});
	}

	downloadData() {
		this.globalService.showLoaderSpinner(true);
		let exportPayload:any = {}
		let fromDate = this.fromStartDate;
		let toDate = this.toEndDate;
		console.log(fromDate , 'fromDate')
		console.log(toDate , 'toDate')
		exportPayload.webshop_id = "6";
		exportPayload.moduleName = "Order";
		exportPayload.fileName = "order.xls";
		exportPayload.show_item_wise_order = 0;
		exportPayload.fromDate = fromDate;
		exportPayload.toDate = toDate;

		this.global.getWebServiceData("order-export", "POST", exportPayload, '').subscribe(results => {
			if (results.status == 1) {
				let fileNBase = window.location.protocol + '//' + window.location.hostname + ':' + GlobalVariable.apiPort+'/';
				var url = fileNBase + results['file_path'];
				console.log(url)
				var a = document.createElement("a");
				a.href = url;
				a.download = exportPayload.fileName;
				document.body.appendChild(a);
				a.click();
				document.body.removeChild(a);
			}
			this.globalService.showLoaderSpinner(false);
		}, err => {

		})
		// this.globalService.showLoaderSpinner(true);
		// let data:any = {};
		// let websiteId = this.globalService.getWebsiteId();;
		// data.website_id = websiteId;
		// data.moduleName = "Order";
		// data.fileName = "order.xlsx";
		// let extraFilter = this.elasticSearch.exportConditions.extraFilter;
		// let extraFilter2 = this.elasticSearch.exportConditions.extraFilter2;
		// let fromDate = this.elasticSearch.exportConditions.fromDate;
		// let toDate = this.elasticSearch.exportConditions.toDate;
		// let elasticData = '{"query":{"bool":{"must":' + extraFilter + ', "must_not":' + extraFilter2 + ',"filter":{"range":{"created":{"gte":"' + fromDate + '","lte":"' + toDate + '"}}}}},"size":10000 }';
		// this._orderService.loadGridES('orders', 1, this.search_text, 25, 'id', this.sortOrder, elasticData, websiteId).subscribe(listData => {
		// 	let tmpResult = [];
		// 	let orderIds:any = [];
		// 	listData.hits.hits.forEach(function (rows: any) {
		// 		tmpResult.push(rows._source);
		// 	});

		// 	this.response.results[0].result = tmpResult;
		// 	if (tmpResult.length > 0) {
		// 		let resultsList = this.response.results[0].result;
		// 		let that = this;
		// 		resultsList.forEach(function (item: any) {
		// 			orderIds.push(item.id);
		// 		})
				
		// 		if (orderIds.length > 0) {
		// 			let exportPayload:any = {}
		// 			exportPayload.webshop_id = "6";
		// 			exportPayload.moduleName = "Order";
		// 			exportPayload.fileName = "order.xls";
		// 			exportPayload.show_item_wise_order = 0;
		// 			exportPayload.order_ids = orderIds.join(',');

		// 			this.global.getWebServiceData("order-export", "POST", exportPayload, '').subscribe(results => {
		// 				if (results.status == 1) {
		// 					let fileNBase = window.location.protocol + '//' + window.location.hostname + ':' + GlobalVariable.apiPort+'/';
		// 					var url = fileNBase + results['file_path'];
		// 					var a = document.createElement("a");
		// 					a.href = url;
		// 					a.download = exportPayload.fileName;
		// 					document.body.appendChild(a);
		// 					a.click();
		// 					document.body.removeChild(a);
		// 				}
		// 				this.globalService.showLoaderSpinner(false);
		// 			}, err => {

		// 			})
		// 		}
		// 	}            
		// },err => {

		// })
		/*this.global.getWebServiceData("order-export","POST",data,'').subscribe(results=> {
			console.log(results);
		}, err => {

		}) */
	}
}