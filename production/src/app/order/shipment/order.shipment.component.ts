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
import { ShipmentService } from './order.shipment.service';
import * as moment from 'moment';
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
    selector: 'my-app',
    templateUrl: `./templates/picklist_list.html`,
    providers: [Global, ShipmentService],
})
export class PicklistComponent implements OnInit, AfterViewInit {
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
            this.generateGrid(0, '', '', '', '', this.show_item_wise_order_shipment);
        }
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
        private _shipmentService: ShipmentService, 
        @Inject(DOCUMENT) private document: any
    ) {
        this.tabIndex = +globalService.getCookie('active_tabs');
        this.parentId = globalService.getParentId(this.tabIndex);
        //console.log(this.parentId);
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
    public selectedAllStatus: any = false;
    public selectedAllAssignedWarehouse: any = false;
    public selectAll
    public stat: any = {};
    public result_list: any = [];
    public total_list: any = [];
    public cols: any = []
    public layout: any = [];
    public add_btn: string;
    public post_data = {};
    public page: number = 1;
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
    public show_item_wise_order_shipment: boolean = false;
    public warehouse_list: any = [];
    public status_list: any = [];
    public status_list_name: any = [];
    public action_status_list: any = [];
    public order_status_ids: any = [];
    public warehouse_ids: any = [];
    public warehouse_name:any = [];
    public action_order_status_ids: any = [];
    public daterange: any = {};
    public options: any = {
        locale: {
            format: 'YYYY-mm-dd'
        },
        alwaysShowCalendars: false,
    };
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
    order_summary_information:any=[];
    show_data:any=[];
    remove_field_index:number;
    exclude_arr:any=[];
    public warehouse_id: any;
    
    ngOnInit() {
        let userData = this._cookieService.getObject('userData');
        this.userId = userData['uid'];
        this.warehouse_id = userData['warehouse_id'];
        this.childData = {
            table: 'EngageboostTrentPicklists',
            heading: 'Picklist',
            ispopup: 'Picklist',
            tablink: 'picklist',
            tabparrentid: this.parentId,
            screen: 'list',
            disableSortBy: ['created_day'],
        }
        //this.AppplyDate(this.selected);
        let selectedStartDate = this.globalService.convertDate(this.selected.startDate, 'yyyy-MM-dd')+' 00:00:00';
        let selectedEndDate = this.globalService.convertDate(this.selected.endDate, 'yyyy-MM-dd')+' 23:59:59';
        this.filter_date = selectedStartDate + '##' + selectedEndDate;
        this.generateGrid(0, '', '', '', '', this.show_item_wise_order_shipment);
        this.formModel.search_type=1;
        this.formModel.search_data='';
        this.formModel.temp_name='';

        this.globalService.orderFilter$.subscribe(
            (value) => {
                this.generateGrid(0, '', '', '', '', this.show_item_wise_order_shipment);
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
    ngAfterViewInit() {
        setTimeout(() => {
            this.globalService.showLoaderSpinner(true);
        });
    }
        /////////////////////////Grid//////////////////////////////////////////////
    generateGrid(reload: any, page: any, sortBy: any, filter: any, search: any, show_item_wise_order_shipment: any) {
        // search = search.trimLeft();
        let warehouse_status  = this._cookieService.getObject('warehouse_status');

		this.globalService.skeletonLoader(true);
        if(search) {
            search = search.trim();
        }
        if(search == '') {
            this.search_text = '';
        } else {
            this.search_text = search;
        }
        let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
        elements[0].classList.remove('show');
        this.bulk_ids = [];
        this.individualRow = {};
        this.total_list = [];
        this.selectedAll = false;
        this.filter = filter;
        this.sortBy = sortBy;
        this.show_item_wise_order_shipment = show_item_wise_order_shipment;
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
        
        let filter_order_status = '';
        if (this.order_status_ids.length > 0) {
            let order_status_str = this.order_status_ids.join();
            filter_order_status = order_status_str.toString();
        }

        let filter_warehouse_id = '';
        if (this.warehouse_ids.length > 0) {
            let assinged_str = this.warehouse_ids.join();
            filter_warehouse_id = assinged_str.toString();
        }

        this.post_data = {
            "model": this.childData.table,
            "screen_name": this.childData.screen,
            "userid": this.userId,
            "search": this.search_text.trim(),
            "order_by": sortBy,
            "order_type": this.sortOrder,
            "status": filter,
            "show_item_wise_order_shipment": show_item_wise_order_shipment,
            'warehouse_id': filter_warehouse_id,
            'manager_warehouse_id': this.warehouse_id,
            'picklist_status': filter_order_status,
            'zones' : '',
            'date': this.filter_date,
			"advanced_search": this.advanced_search,
            "warehouse_status": warehouse_status

        }
        this._shipmentService.doGrid(this.post_data, page).subscribe(data => {
            this.response = data;
            let that = this;
            if (this.response.count > 0) {
                this.result_list = this.response.results[0].result;
                this.result_list.forEach(function(item: any) {
                    //////////////  end status settings ///////////////////
                    //console.log(item.picklist_status)
                    if(item.picklist_status == 'Picking') {
                        item.class_name = 'status-box packed';
                    } else if(item.picklist_status == 'Invoicing') {
                       item.class_name = 'status-box invoiced';
                    } else if(item.picklist_status == 'Create Shipment') {
                       item.class_name = 'status-box created';
                    } else {
                       item.class_name = 'status-box packed';
                    }
                })
                for (var i = 0; i < this.response.count; i++) {
                    this.total_list.push(i);
                }
            } else {
                this.result_list = [];
            }
            //console.log(this.result_list);
            this.cols = this.response.results[0].applied_layout;
            this.layout = this.response.results[0].layout;
                
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
            if( this.filter_date == "null 00:00:00##null 23:59:59") {
                let selectedStartDate = this.globalService.convertDate(this.selected.startDate, 'yyyy-MM-dd') + ' 00:00:00';
                let selectedEndDate = this.globalService.convertDate(this.selected.endDate, 'yyyy-MM-dd') + ' 23:59:59';
                this.filter_date = selectedStartDate + '##' + selectedEndDate;
            }
			let myelement: HTMLElement = this.document.getElementsByClassName('autoclick');
            if(myelement[0]) {
                myelement[0].click();
            }
        },err=>{
            console.log(err)
            this.globalService.skeletonLoader(false);
        });
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
        this.generateGrid(0, '', '', '', '',this.show_item_wise_order_shipment);
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
                this.formModel.search_data=this.globalService.convertDate(this.formModel.search_data, 'yyyy-MM-dd'); 
            }
            this.Advancefilter={'field':this.formModel.field_name,'comparer':this.formModel.search_type,'key':this.formModel.search_data,'name':this.formModel.field_name, 'show_name':this.formModel.field_name_show,'key2':this.formModel.update_key,'input_type':this.formModel.input_type,'field_id':this.formModel.field_id}
            this.advanced_search.push(this.Advancefilter);
            this.generateGrid(0, '', '', '', '',this.show_item_wise_order_shipment);
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
		this.generateGrid(0, '', '', '', '',this.show_item_wise_order_shipment);
	}
    
    show_options(){
        this.search_type_option=true;
    }

    cancel_filter() {
        let elements: NodeListOf < Element > = this.document.getElementsByClassName('meta_keywordbox');
        elements[0].classList.remove('show');  
		this.generateGrid(0, '', '', '', '',this.show_item_wise_order_shipment);
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
    
    ////////////////////////Delete/Block/Unblock///////////////////////////////
    updateStatusAll(type: number, id: number) {
        let msg='';
        let perm='';
        let msgp = '';
        if(id) {
            let that = this;
            that.bulk_ids = [];
            that.bulk_ids.push(id);
        }
        if(type == 2) {
            msg = 'Do you really want to delete selected records?';
            perm = this.permission.delete;
            msgp = 'You have no permission to delete!';
            if(this.individualRow.picklist_status != 'Picking') {
                this.dialogsService.alert('Error', "GRN is already completed, you can't delete this picklist.").subscribe(res => {});
                return false;
            }
        }
        if(perm == 'Y') {
            if (this.bulk_ids.length > 0) {
                this.dialogsService.confirm('Warning', msg).subscribe(res => {
                    if (res) {
                        if (type == 2) {
                            let website_id = this.globalService.getWebsiteId();
                            let delete_data = {
                                "shipment_id": id,
                                "website_id": website_id,
                                "userid": this.userId
                            }
                            this._shipmentService.deleteShipment(delete_data).subscribe(data => {
                                this.response = data;
                                this.globalService.showToast(this.response.message);
                                this.generateGrid(0, '', '', '', '', this.show_item_wise_order_shipment);
                            }, err => console.log(err), function() {});
                        } else {
                            this.global.doStatusUpdate(this.childData.table, this.bulk_ids, type).subscribe(data => {
                                this.response = data;
                                this.globalService.showToast(this.response.Message);
                                this.generateGrid(0, '', '', '', '', this.show_item_wise_order_shipment);
                            }, err => console.log(err), function() {});
                        }
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
            }
            else {
                elements[0].classList.remove('show');
            }
        });
        let myelement: NodeListOf < Element > = this.document.getElementsByClassName('action-box orderfilter');
		myelement[0].classList.remove('show');
    }
    toggleCheck(id: any, event: any) {
        let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
        let that = this;
        this.result_list.forEach(function(item: any) {
            if (item.id == id) {
                item.selected = event.checked;
                if (item.selected) {
                    that.bulk_ids.push(item.id);
                    that.action_order_status_ids.push(item.order_status);
                    elements[0].classList.add('show');
                }
                else {
                    let index = that.bulk_ids.indexOf(item.id);
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
       // console.log(this.bulk_ids);
       let myelement: NodeListOf < Element > = this.document.getElementsByClassName('action-box orderfilter');
		myelement[0].classList.remove('show');
    }

    /////////////////////////Filter Grid//////////////////////
    updateGrid(isdefault: any) {
        this._shipmentService.doGridFilter(this.childData.table, isdefault, this.cols, "list").subscribe(data => { 
            this.response = data;
            this.generateGrid(0, '', '', '', '', this.show_item_wise_order_shipment);
        }, err => console.log(err), function() {});
    }
    
    
    applyFilter(event: any, filter_type: any, id: number) {
        let that = this;
        if (filter_type == 'status') {
            this.status_list.forEach(function(item: any) {
                if (item.id == id) {
                    item.selected = event.checked;
                    if (item.selected) {
                        that.order_status_ids.push(item.id);
                        //elements[0].classList.add('show');
                    }
                    else {
                        let index = that.order_status_ids.indexOf(item.id);
                        that.order_status_ids.splice(index, 1);
                        if (that.order_status_ids.length == 0) {
                            //elements[0].classList.remove('show');
                        }
                    }
                }
                if (that.order_status_ids.length == 1) {
                    that.order_status_ids.forEach(function(item_id: any) {
                        if (item_id == item.id) {
                            //that.individualRow=item;
                        }
                    });
                }
                that.selectedAllStatus = false;
            });
        } else if (filter_type == 'AssignedWarehouse') {
            this.warehouse_list.forEach(function(item: any) {
                if (item.id == id) {
                    item.selected = event.checked;
                    if (item.selected) {
                        that.warehouse_ids.push(item.id);
                        that.warehouse_name.push(item.name);
                    }
                    else {
                        var nameIndex = that.warehouse_name.indexOf(item.name);
                        that.warehouse_name.splice(nameIndex, 1);

                        var index = that.warehouse_ids.indexOf(item.id);
                        that.warehouse_ids.splice(index, 1);
                        if (that.warehouse_ids.length == 0) {
                            //elements[0].classList.remove('show');
                        }
                    }
                }
                if (that.warehouse_ids.length == 1) {
                    that.warehouse_ids.forEach(function(item_id: any) {
                        if (item_id == item.id) {
                            //that.individualRow=item;
                        }
                    });
                }
                that.selectedAllAssignedWarehouse = false;
            });
        }
    }
    applyFilterAll(event: any, filter_type: any) {
        let that = this;
        if (filter_type == 'status') {
            let that = this;
            that.order_status_ids = [];
            this.selectedAllStatus = event.checked;
            this.status_list.forEach(function(item: any) {
                item.selected = event.checked;
                if (item.selected) {
                    that.order_status_ids.push(item.id);
                }
                else {}
            });
            //console.log(this.order_status_ids);
        } else if (filter_type == 'AssignedWarehouse') {
            let that = this;
            that.warehouse_ids = [];
            this.selectedAllAssignedWarehouse = event.checked;
            this.warehouse_list.forEach(function(item: any) {
                item.selected = event.checked;
                if (item.selected) {
                    that.warehouse_ids.push(item.id);
                    that.warehouse_name.push(item.name);
                }
                else {}
            });
        }
    }
    refreshPickList() {
        this.order_status_ids = [];
        this.warehouse_ids = [];
        this.status_list_name = [];
        this.warehouse_name = [];
        this.selected = {
            startDate: moment().subtract(30, 'days'),
            endDate: moment().subtract(0, 'days')
        }; // reset calender
        let selectedStartDate = this.globalService.convertDate(this.selected.startDate, 'yyyy-MM-dd')+ ' 00:00:00';
        let selectedEndDate = this.globalService.convertDate(this.selected.endDate, 'yyyy-MM-dd')+ ' 23:59:59';
        this.filter_date = selectedStartDate + '##' + selectedEndDate;
        // this.AppplyDate(this.selected);
        this.generateGrid(1, '', '', '', '', this.show_item_wise_order_shipment);
    }

    createPicklist(picklist_id,shipmentDetails) {
        //console.log(picklist_id);console.log(shipmentDetails);
        let that = this;
        if(that.bulk_ids.length > 0) {
            let shipment_status = shipmentDetails.picklist_status;
            if(shipment_status === 'Picking') {
                this.globalService.addTab('picklist','picklist/grn/'+picklist_id,'Picking',this.childData.tabparrentid)
                this._router.navigate(['/picklist/grn/'+picklist_id]);
            } else if(shipment_status === 'Invoicing') {
                this.globalService.addTab('picklist','picklist/invoice/'+picklist_id,'Invoice',this.childData.tabparrentid)
                this._router.navigate(['/picklist/invoice/'+picklist_id]);
            } else {
                this.globalService.addTab('picklist','picklist/grn/'+picklist_id,'Picking',this.childData.tabparrentid)
                this._router.navigate(['/picklist/grn/'+picklist_id]);
            }
        } else {
            this.globalService.showToast("Please select atleast one order");
        }
    }
    // perform_picklist_status_action // $data['Picklist']['isdeleted'] = 'y';
    remove_from_picklist() { 

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
    templateUrl: `./templates/shipment.html`,
    providers: [Global, ShipmentService],
})
export class ShipmentComponent implements OnInit, AfterViewInit {
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
	public showSkeletonLoaded: boolean = false;

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
        let selectedStartDate = this.globalService.convertDate(selected_dates.startDate, 'yyyy-MM-dd') + ' 00:00:00';
        let selectedEndDate = this.globalService.convertDate(selected_dates.endDate, 'yyyy-MM-dd') + ' 23:59:59';
        this.filter_date = selectedStartDate + '##' + selectedEndDate;
        if (selected_dates.startDate != null && selected_dates.endDate != null) {
            this.generateGrid(0, '', '', '', '', this.show_item_wise_order_shipment);
        }
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
        private _shipmentService: ShipmentService,
        @Inject(DOCUMENT) 
        private document: any
    ) {
        this.tabIndex = +globalService.getCookie('active_tabs');
        this.parentId = globalService.getParentId(this.tabIndex);
        //console.log(this.parentId);
        this.maxDate = moment().add(2, 'weeks');
        this.minDate = moment().subtract(3, 'days');
        this.alwaysShowCalendars = true;
        this.keepCalendarOpeningWithRange = true;
        this.showRangeLabelOnInput = true;
        this.selected = {
            startDate: moment().subtract(30, 'days'),
            endDate: moment().subtract(0, 'days')
        };
        let selectedStartDate = this.globalService.convertDate(this.selected.startDate, 'yyyy-MM-dd') + ' 00:00:00';
        let selectedEndDate = this.globalService.convertDate(this.selected.endDate, 'yyyy-MM-dd') + ' 23:59:59';
        this.filter_date = selectedStartDate + '##' + selectedEndDate;
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
    public selectedAllStatus: any = false;
    public selectedAllAssignedWarehouse: any = false;
    public selectAll
    public stat: any = {};
    public result_list: any = [];
    public total_list: any = [];
    public cols: any = []
    public add_btn: string;
    public post_data = {};
    public page: number = 1;
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
    public show_item_wise_order_shipment: boolean = false;
    public warehouse_list: any = [];
    public status_list_name: any = [];
    public status_list: any = [];
    public action_status_list: any = [];
    public order_status_ids: any = [];
    public warehouse_ids: any = [];
    public warehouse_name:any = [];
    public action_order_status_ids: any = [];
    
    public order_delivery_slot:any= [];
    public timeSlotIds:any = [];

    public daterange: any = {};
    public options: any = {
        locale: {
            format: 'YYYY-mm-dd'
        },
        alwaysShowCalendars: false,
    };
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
    public warehouse_id: any;
    public temp_result=[];
    public temp_col=[];
    ngOnInit() {
        let userData = this._cookieService.getObject('userData');
        this.userId = userData['uid'];
        this.warehouse_id = userData['warehouse_id'];
        this.childData = {
            table: 'EngageboostShipments',
            heading: 'Shipment',
            ispopup: 'Shipment',
            tablink: 'shipment',
            tabparrentid: this.parentId,
            screen: 'list',
            disableSortBy: ['created_day'],
        }
        this.generateGrid(0, '', '', '', '', this.show_item_wise_order_shipment);
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
        this.formModel.search_type=1;
        this.formModel.search_data='';
        this.formModel.temp_name='';

        this.globalService.orderFilter$.subscribe(
            (value) => {
                this.generateGrid(0, '', '', '', '', this.show_item_wise_order_shipment);
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
    ngAfterViewInit() {
        setTimeout(() => {
            this.globalService.skeletonLoader(true);
        });
    }
        /////////////////////////Grid//////////////////////////////////////////////
    generateGrid(reload: any, page: any, sortBy: any, filter: any, search: any, show_item_wise_order_shipment: any) {
         let warehouse_status  = this._cookieService.getObject('warehouse_status');
        this.globalService.skeletonLoader(true);
        // search = search.trimLeft();
        if(search) {
            search = search.trim();
        }
        if(search == '') {
            this.search_text = '';
        } else {
            this.search_text = search;
        }
        let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
        elements[0].classList.remove('show');
        this.bulk_ids = [];
        this.individualRow = {};
        this.total_list = [];
        this.selectedAll = false;
        this.filter = filter;
        this.sortBy = sortBy;
        this.show_item_wise_order_shipment = show_item_wise_order_shipment;
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
        
        let filter_order_status = '';
        if (this.order_status_ids.length > 0) {
            let order_status_str = this.order_status_ids.join();
            filter_order_status = order_status_str.toString();
        }
        
        let filter_delivery_slot_ids = '';
        if (this.timeSlotIds.length > 0) {
            let timeSlotIds_str = this.timeSlotIds.join();
            filter_delivery_slot_ids = timeSlotIds_str.toString();
        }
        let website_id = this.globalService.getWebsiteId();
        this.post_data = {
            "model": this.childData.table,
            "screen_name": this.childData.screen,
            "website_id" : website_id,
            "userid": this.userId,
            "search": this.search_text.trim(),
            "order_by": sortBy,
            "order_type": this.sortOrder,
            "status": filter,
            "show_item_wise_order_shipment": show_item_wise_order_shipment,
            'shipment_status': filter_order_status,
            'delivery_slot' : filter_delivery_slot_ids,
            'zones' : '',
            'date': this.filter_date,
            "advanced_search": this.advanced_search,
            'manager_warehouse_id': this.warehouse_id,
            "warehouse_status": warehouse_status,
        }
        //console.log(this.post_data);
        this._shipmentService.doGrid(this.post_data, page).subscribe(data => {
            this.response = data;
            if (this.response.count > 0) {
                this.result_list = this.response.results[0].result;
                this.globalService.skeletonLoader(false);
                //let that = this;
                this.result_list.forEach(function(item: any) {
                    //////////////  end status settings ///////////////////
                    // Picking, Invoicing(Pay now button), Packed, Shipment Processing, Ready to Ship, Shipped
                    if(item.shipment_status == 'Picking') {
                        item.class_name = 'status-box packed';
                    } else if(item.shipment_status == 'Invoicing') {
                        item.class_name = 'status-box invoiced';
                    } else if(item.shipment_status == 'Packed') {
                        item.class_name = 'status-box ready_to_dispatch';
                    } else if(item.shipment_status == 'Shipment Processing') {
                        item.class_name = 'status-box shipment_processing';
                    } else if(item.shipment_status == 'Ready to Ship') {
                        item.class_name = 'status-box ready_to_ship';
                    } else if(item.shipment_status == 'Shipped')  {
                        item.class_name = 'status-box shipped';
                    } else {
                        item.class_name = 'status-box shipped';
                    }

                    ///////////  amount formating with currency //////////////
                    let currencyCode = item.currency_code;
                    if(currencyCode == '') {
                        currencyCode = 'AED';
                    }

                    if(item.net_amount || item.gross_amount || item.discount_amount || item.tax_amount || item.shipping_amount){
                        item.net_amount = currencyCode + " " + item.net_amount.toFixed(2);
                        item.gross_amount = currencyCode + " " + item.gross_amount.toFixed(2);
                        item.discount_amount = currencyCode + " " + item.discount_amount.toFixed(2);
                        item.tax_amount = currencyCode + " " + item.tax_amount.toFixed(2);
                        item.shipping_amount = currencyCode + " " + item.shipping_amount.toFixed(2);
                    }
                })
                for (var i = 0; i < this.response.count; i++) {
                    this.total_list.push(i);
                }
            } else {
                this.globalService.skeletonLoader(false);
                this.result_list = [];
            }
            // this.cols = this.response.results[0].layout;
            this.cols = this.response.results[0].applied_layout;
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

            if( this.filter_date == "null 00:00:00##null 23:59:59") {
                let selectedStartDate = this.globalService.convertDate(this.selected.startDate, 'yyyy-MM-dd') + ' 00:00:00';
                let selectedEndDate = this.globalService.convertDate(this.selected.endDate, 'yyyy-MM-dd') + ' 23:59:59';
                this.filter_date = selectedStartDate + '##' + selectedEndDate;
            }
            let myelement: HTMLElement = this.document.getElementsByClassName('autoclick');
            if(myelement[0]) {
                myelement[0].click();
            }
        },err=>{
            //this.globalService.skeletonLoader(false);
        })
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
        this.generateGrid(0, '', '', '', '',this.show_item_wise_order_shipment);
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
                this.formModel.search_data=this.globalService.convertDate(this.formModel.search_data, 'yyyy-MM-dd'); 
            }
            this.Advancefilter={'field':this.formModel.field_name,'comparer':this.formModel.search_type,'key':this.formModel.search_data,'name':this.formModel.field_name, 'show_name':this.formModel.field_name_show,'key2':this.formModel.update_key,'input_type':this.formModel.input_type,'field_id':this.formModel.field_id}
            this.advanced_search.push(this.Advancefilter);
            this.generateGrid(0, '', '', '', '',this.show_item_wise_order_shipment);
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
            this.globalService.showToast('Please enter value');
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
        } else {
            this.formModel.update_key=item;
        }
        this.formModel.temp_name=item;
	}
	remove_filter(index:number){
        let remove_val=this.advanced_search.splice(index,1);
        const items = this.exclude_arr;
        const valueToRemove = remove_val[0].field_id;
        this.exclude_arr = items.filter(item => item !== valueToRemove)  
        this.generateGrid(0, '', '', '', '',this.show_item_wise_order_shipment);
	}
    
    show_options(){
        this.search_type_option=true;
    }

    cancel_filter() {
        let elements: NodeListOf < Element > = this.document.getElementsByClassName('meta_keywordbox');
        elements[0].classList.remove('show');  
		this.generateGrid(0, '', '', '', '',this.show_item_wise_order_shipment);
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
    
    ////////////////////////Delete/Block/Unblock///////////////////////////////
    updateStatusAll(type: number, id: number) {
        let msg = '';
        let perm = '';
        let msgp = '';
        if (id) {
            let that = this;
            that.bulk_ids = [];
            that.bulk_ids.push(id);
        }
        if (type == 2) {
            msg = 'Do you really want to delete selected records?';
            perm = this.permission.delete;
            msgp = 'You have no permission to delete!';
        } else if (type == 1) {
            msg = 'Do you really want to block selected records?';
            perm = this.permission.block;
            msgp = 'You have no permission to block!';
        } else {
            msg = 'Do you really want to unblock selected records?';
            perm = this.permission.block;
            msgp = 'You have no permission to unblock!';
        }
        if (perm == 'Y') {
            if (this.bulk_ids.length > 0) {
                this.dialogsService.confirm('Warning', msg).subscribe(res => {
                    if (res) {
                        if (type == 2) {
                            let website_id = this.globalService.getWebsiteId();
                            let delete_data = {
                                "shipment_id": id,
                                "website_id": website_id,
                                "userid": this.userId
                            }
                            this._shipmentService.deleteShipment(delete_data).subscribe(data => {
                                this.response = data;
                                this.globalService.showToast(this.response.message);
                                this.generateGrid(0, '', '', '', '', this.show_item_wise_order_shipment);
                            }, err => console.log(err), function() {});
                        } else {
                            this.global.doStatusUpdate(this.childData.table, this.bulk_ids, type).subscribe(data => {
                                this.response = data;
                                this.globalService.showToast(this.response.Message);
                                this.generateGrid(0, '', '', '', '', this.show_item_wise_order_shipment);
                            }, err => console.log(err), function() {});
                        }
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
            }
            else {
                elements[0].classList.remove('show');
            }
        });
        let myelement: NodeListOf < Element > = this.document.getElementsByClassName('action-box orderfilter');
		myelement[0].classList.remove('show');
    }
    toggleCheck(id: any, event: any) {
        let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
        let that = this;
        this.result_list.forEach(function(item: any) {
            if (item.id == id) {
                item.selected = event.checked;
                if (item.selected) {
                    that.bulk_ids.push(item.id);
                    that.action_order_status_ids.push(item.order_status);
                    elements[0].classList.add('show');
                }
                else {
                    let index = that.bulk_ids.indexOf(item.id);
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
    /////////////////////////Filter Grid//////////////////////
    updateGrid(isdefault: any) {
        this._shipmentService.doGridFilter(this.childData.table, isdefault, this.cols, "list").subscribe(data => {
            this.response = data;
            this.generateGrid(0, '', '', '', '', this.show_item_wise_order_shipment);
        }, err => console.log(err), function() {});
    }
    
    refreshShipment() {
        this.status_list_name = [];
        this.order_status_ids = [];
        this.warehouse_ids = [];
        this.selected = {
            startDate: moment().subtract(30, 'days'),
            endDate: moment().subtract(0, 'days')
        }; // reset calender
        // this.AppplyDate(this.selected);
        let selectedStartDate = this.globalService.convertDate(this.selected.startDate, 'yyyy-MM-dd') + ' 00:00:00';
        let selectedEndDate = this.globalService.convertDate(this.selected.endDate, 'yyyy-MM-dd') + ' 23:59:59';
        this.filter_date = selectedStartDate + '##' + selectedEndDate;
        this.generateGrid(1, '', '', '', '', this.show_item_wise_order_shipment);
    }

    createShipment(shipment_id, shipment_status) {
        if(shipment_status === 'Picking') {
            this.globalService.addTab('shipment','shipment/grn/'+shipment_id,'Picking',this.childData.tabparrentid)
            this._router.navigate(['/shipment/grn/'+shipment_id]);
        } else if(shipment_status === 'Invoicing' || shipment_status === 'Packed') {
            this.globalService.addTab('shipment','shipment/invoice/'+shipment_id,'Invoice',this.childData.tabparrentid)
            this._router.navigate(['/shipment/manifest/'+shipment_id]);
        } else if(shipment_status === 'Shipment Processing') {
           this.globalService.addTab('shipment','shipment/delivery_planner/'+shipment_id,'Delivery Planner',this.childData.tabparrentid)
            this._router.navigate(['/shipment/delivery_planner/'+shipment_id]);
        } else {
            this.globalService.addTab('shipment','shipment/manifest/'+shipment_id,'Delivery Note',this.childData.tabparrentid)
            this._router.navigate(['/shipment/manifest/'+shipment_id]);
        }
    }

    dialogRefColumnLayout: MatDialogRef<ColumnLayoutComponent> | null;
	loadColumnLayout() {
		let data: any = {}
		data["column"] = this.cols;
		this.dialogRefColumnLayout = this.dialog.open(ColumnLayoutComponent, { data: data });
		this.dialogRefColumnLayout.afterClosed().subscribe(result => {
			if(result != undefined) {
				this.cols = result;
				this.updateGrid(0);
			}
		});
    }
    refreshReturn(){
    }
}