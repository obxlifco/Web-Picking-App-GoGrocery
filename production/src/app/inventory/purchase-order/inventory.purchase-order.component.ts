import { Component,ElementRef,OnInit,Input,Inject} from '@angular/core';
import {Global} from '../../global/service/global';
import {GlobalService} from '../../global/service/app.global.service';
import {Router} from '@angular/router';
import { DomSanitizer } from '@angular/platform-browser';
import {PaginationInstance} from 'ngx-pagination';
import {DialogsService} from '../../global/dialog/confirm-dialog.service';
import {CookieService} from 'ngx-cookie';
import { MatDialog,MatDialogRef,MAT_DIALOG_DATA } from '@angular/material';
import {PurchaseOrderService} from './inventory.purchase-order.service';
import {DOCUMENT} from '@angular/platform-browser';
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
  templateUrl: './templates/purchase_orders.html',
  providers: [Global,PurchaseOrderService],
})
export class PurchaseOrderComponent implements OnInit {
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
    public isManager: any;
    public individualRow: any = {};
    public search_text: any;
    public colSpanCount = 4;
    public isSuperAdmin = 'Y';
    showSkeletonLoaded: boolean = false;
	public temp_result=[];
    public temp_col=[];
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
    edit_index:number;
    constructor(
        private globalService: GlobalService,
        private global: Global,
        private _router: Router,
        private sanitizer: DomSanitizer,
        private dialogsService: DialogsService,
        private elRef: ElementRef,
        private _cookieService: CookieService,
        public dialog: MatDialog,
        private _purchaseOrderService: PurchaseOrderService, @Inject(DOCUMENT) private document: any) {
        this.tabIndex = +globalService.getCookie('active_tabs');
        this.parentId = globalService.getParentId(this.tabIndex);
    }
    //////////////////////////Initilise////////////////////////////
    ngOnInit() {
        let userData = this._cookieService.getObject('userData');
        this.userId = userData['uid'];
        this.isManager = userData['isManager'];
        this.isSuperAdmin = userData['isSuperAdmin'];
        this.generateGrid(0, '', '', '', '');
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
    /////////////////////////Grid//////////////////////////////////////////////
    generateGrid(generateGrid: any, page: any, sortBy: any, filter: any, search: any) {
        setTimeout(() => {
            // this.globalService.showLoaderSpinner(true);
            this.globalService.skeletonLoader(true);
        });
        if (search == '') {
            this.search_text = '';
        }else{
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
        if (sortBy != '' && sortBy != undefined) {
            if (this.sortRev) {
                this.sortOrder = '-';
                this.sortRev = !this.sortRev;
                this.sortClass = 'icon-down';
            } else {
                this.sortOrder = '+';
                this.sortRev = !this.sortRev;
                this.sortClass = 'icon-up';
            }
        } else {
            this.sortBy = 'id';
            this.sortOrder = '-';
            this.sortRev = !this.sortRev;
            this.sortClass = 'icon-up';
        }
        this.post_data = {
            "userid": this.userId,
            "search": search.trim(),
            "order_by": this.sortBy,
            "order_type": this.sortOrder,
            "filter": filter,
            "is_supplier": (this.isManager == 'Suppliers') ? 1 : 0,
            "supplier_id": 0,
			"advanced_search": this.advanced_search

        }
        this._purchaseOrderService.doGrid(this.post_data, page).subscribe(
            data => {
                this.response = data;
                if (this.response.count > 0) {
                    this.result_list = this.response.results[0].result.product;
                    for (var i = 0; i < this.response.count; i++) {
                        this.total_list.push(i);
                    }
                } else {
                    this.result_list = [];
                }
                
                this.cols = this.response.results[0].applied_layout;
				this.layout = this.response.results[0].layout;

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
                
            },
            err => console.log(err),
            function() {}
        );
    }
   
    // NEW fILTER STRAT
	load_fiter_column(){
        let data:any={};
        data.model='EngageboostPurchaseOrders';
        data.website_id=this.globalService.getWebsiteId();
        data.search= this.formModel.field_name;
        data.screen_name='list';
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
        this.generateGrid(0, '', '', '', '');
        this.load_fiter_column();
		this.exclude_arr=[];
    }
    get_data(data :any,index:number){
        this.selectArr=[];
        // this.formModel.search_data=null;
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
        // alert(this.remove_field_index)
    }
    sendSearchData(){
        var search_data:any=[];
        var search_data_show:any=[];
        if(this.formModel.input_type=='multi_select'){

            this.formModel.search_data.forEach(element => {
                search_data.push(element.id);
                search_data_show.push(element.name);
            });
        }
        if( this.formModel.input_type=='select'){
			search_data=this.formModel.search_data.id;
            search_data_show=this.formModel.search_data.name;
        }
        if(this.formModel.input_type=='date'){
            search_data=this.globalService.convertDate(this.formModel.search_data, 'yyyy-MM-dd');
            search_data_show=this.globalService.convertDate(this.formModel.search_data, 'yyyy-MM-dd');
        }
        if(this.formModel.input_type=='float' || this.formModel.input_type=='text' || this.formModel.input_type=='fix_select' ){
            search_data=this.formModel.search_data;
            search_data_show=this.formModel.search_data;
        }

        if(search_data!=''){
            this.Advancefilter={'field':this.formModel.field_name,'comparer':this.formModel.search_type,'key':search_data,'name':this.formModel.field_name, 'show_name':this.formModel.field_name_show,'key2':search_data_show,'input_type':this.formModel.input_type,'field_id':this.formModel.field_id}
            if(this.edit_index!=undefined){
                this.advanced_search.splice(this.edit_index,1);
            }
            this.advanced_search.push(this.Advancefilter);
            this.generateGrid(0, '', '', '', '');
            let elements: NodeListOf < Element > = this.document.getElementsByClassName('meta_keywordbox');
            elements[0].classList.remove('show');
            this.selectArr=[];
            this.formModel.search_data=null;
            this.formModel.search_module=null;
            this.formModel.update_key=search_data_show;
            this.formModel.field_name='';
            this.formModel.search_type=1;
            this.formModel.search_data=null;
            this.get_select_data();
            this.field_arr.splice(this.remove_field_index,1);
            
        }else{
            this.globalService.showToast('Please enter value');
        }
        this.edit_index=null;
    }
	
	remove_filter(index:number){
        let remove_val=this.advanced_search.splice(index,1);
        const items = this.exclude_arr;
        const valueToRemove = remove_val[0].field_id;
        this.exclude_arr = items.filter(item => item !== valueToRemove)
		this.generateGrid(0, '', '', '', '');
	}
    show_options(){
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
	get_select_data(field_id=this.formModel.field_id){
        this.global.getWebServiceData('global_list/'+field_id, 'GET', '', '').subscribe(res => {
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

    edit_filter(i:number, item:any){
        this.get_select_data(item.field_id);
        this.formModel.field_name_show=item.show_name;
		this.formModel.field_id=item.field_id;
        this.formModel.input_type=item.input_type;
        if(this.formModel.input_type=="multi_select"){
            this.formModel.search_data=item.key;
        }else{
            this.formModel.search_data=item.key;
        }
        this.formModel.field_name=item.name;
        this.formModel.search_type=item.comparer;
        this.edit_index=i;
        var element = this.document.getElementById('meta_keywordbox');
        element.classList.add("show");
    }
    // NEW fILTER END
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
        /////////////////////////Filter Grid//////////////////////
    updateGrid(isdefault: any) {
        this.global.doGridFilter('EngageboostPurchaseOrders', isdefault, this.cols, "list").subscribe(
            data => {
                this.response = data;
                this.generateGrid(0, '', '', '', '');
            },
            err => console.log(err),
            function() {}
        );
    }

    dialogPoSentRef: MatDialogRef < PoSentComponent > | null;
    dialogShipTrackRef: MatDialogRef < ShipTrackComponent > | null;
    dialogPoReceivedRef: MatDialogRef < PoReceivedComponent > | null;
    changePoStatus(id: number, status: string) {
        let request_data: any = {};
        request_data['id'] = id;
        if (status == 'Cancel') {
            this.dialogsService.confirm('Warning', 'Do you really want to cancel this purchase order ?').subscribe(res => {
                if (res) {
                    request_data['status'] = status;
                    this.poStatusCallback(request_data);
                }
            });

        } else if (status == 'PO Sent') {
            let data: any = {};
            data['po_id'] = id;
            this.dialogPoSentRef = this.dialog.open(PoSentComponent, {
                data: data
            });
            this.dialogPoSentRef.afterClosed().subscribe(result => {
                if (result) {
                    this.poStatusCallback(result);
                }
            });
        } else if (status == 'Shipped') {
            let data: any = {};
            data['po_id'] = id;
            this.dialogShipTrackRef = this.dialog.open(ShipTrackComponent, {
                data: data
            });
            this.dialogShipTrackRef.afterClosed().subscribe(result => {
                if (result) {
                    this.poStatusCallback(result);
                }
            });
        } else if (status == 'GRN Pending') {
            let data: any = {};
            data['po_id'] = id;
            data['po_datails'] = this.individualRow;
            this.dialogPoReceivedRef = this.dialog.open(PoReceivedComponent, {
                data: data
            });
            this.dialogPoReceivedRef.afterClosed().subscribe(result => {
                if (result) {
                    let post_data: any = {};
                    post_data['id'] = result['id'];
                    post_data['status'] = result['status'];
                    post_data['received_id'] = result['receipt_no'];
                    post_data['received_date'] = result['received_date'];
                    post_data['warehouse_id'] = result['warehouse_id'];
                    let userData = this._cookieService.getObject('userData');
                    let userId = userData['uid'];
                    post_data['user_id'] = userId;
                    this.poStatusCallback(post_data);
                }
            });
        } else if (status == 'Received Full') {

            this._router.navigate(['/purchase_order/grn/' + id]);
            this.globalService.addTab('purchaseordergrn', '/purchase_order/grn/' + id, 'Purchase Order GRN', this.parentId);
        }
    }

    poStatusCallback(request_data: any) {
        this._purchaseOrderService.changePoStatus(request_data).subscribe(
            data => {
                if(data.status == '1') {
                    this.globalService.showToast(data.message);
                } 
                this.generateGrid(0, '', '', '', '');
            },
            err => console.log(err),
            function() {}
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
}

@Component({
    templateUrl: './templates/po_sent.html',
    providers: [PurchaseOrderService]
})
export class PoSentComponent implements OnInit {
    public formModel: any = {};
    public errorMsg: string;
    public successMsg: string;
    constructor(
        public _globalService: GlobalService,
        private _purchaseOrderService: PurchaseOrderService,
        public dialog: MatDialog,
        private _cookieService: CookieService,
        private dialogRef: MatDialogRef < PoSentComponent > , @Inject(MAT_DIALOG_DATA) public data: any
    ) {

    }

    ngOnInit() {
        this._purchaseOrderService.getSupplierEmail(this.data.po_id).subscribe(
            data => {
                this.formModel.supplier_email = data.email;
            },
            err => console.log(err),
            function() {}
        );
    }

    poSent(form: any) {
        let returnData: any = {};
        returnData['id'] = this.data.po_id;
        returnData['status'] = 'PO Sent';
        returnData['supplier_email'] = this.formModel.supplier_email;
        if (this.formModel.send_email) {
            returnData['send_email'] = 1;
        } else {
            returnData['send_email'] = 0;
        }
        let userData = this._cookieService.getObject('userData');
        let user_id = userData['uid'];
        returnData['user_id'] = user_id;
        this.dialogRef.close(returnData);
    }

    closeDialog() {
        this.dialogRef.close();
    }
}

@Component({
    templateUrl: './templates/shipping_track.html',
    providers: [PurchaseOrderService]
})
export class ShipTrackComponent {
    public formModel: any = {};
    public errorMsg: string;
    public successMsg: string;
    public userId: any;
    constructor(
        public _globalService: GlobalService,
        private _purchaseOrderService: PurchaseOrderService,
        public dialog: MatDialog,
        private dialogRef: MatDialogRef < ShipTrackComponent > ,
        private _cookieService: CookieService, @Inject(MAT_DIALOG_DATA) public data: any
    ) {
    }

    closeDialog() {
        this.dialogRef.close();
    }

    shipTrack(form: any) {
        let returnData: any = {};
        let userData = this._cookieService.getObject('userData');
        this.userId = userData['uid'];
        returnData = Object.assign({}, this.formModel);
        returnData['id'] = this.data.po_id;
        returnData['status'] = 'Shipped';
        returnData['user_id'] = this.userId;

        if (!this.formModel['tracking_company']) {
            returnData['tracking_company'] = '';
        }
        if (!this.formModel['tracking_id']) {
            returnData['tracking_id'] = '';
        }
        if (!this.formModel['tracking_url']) {
            returnData['tracking_url'] = '';
        }
        if (!this.formModel['isEmail']) {
            returnData['isEmail'] = false;
        }
        this.dialogRef.close(returnData);
    }
}

@Component({
    templateUrl: './templates/po_received.html',
    providers: [PurchaseOrderService]
})
export class PoReceivedComponent implements OnInit {
    public formModel: any = {};
    public minDate: any;
    public errorMsg: string;
    public successMsg: string;
    constructor(
        public _globalService: GlobalService,
        private _purchaseOrderService: PurchaseOrderService,
        public dialog: MatDialog,
        private dialogRef: MatDialogRef < ShipTrackComponent > , @Inject(MAT_DIALOG_DATA) public data: any
    ) {
    }
    
    ngOnInit() {
        this.formModel = Object.assign({}, this.data.po_datails);
        var match = /(\d+)-(\d+)-(\d+)/.exec(this.formModel.created_date);
        this.formModel.order_date = new Date(+match[3], (+match[2]) - 1, +match[1]);
        this.minDate = new Date();
        this.formModel.received_date = new Date();
        this._purchaseOrderService.getPoReceived(this.formModel.id).subscribe(
            data => {
                this.formModel.receipt_no = data.received_code;
                this.formModel.total_qty = data.total_qty;
                this.formModel.warehouse_id = data.warehouse_id;
            },
            err => console.log(err),
            function() {}
        );
    }

    poReceived(form: any) {
        let returnData: any = {};
        returnData = Object.assign({}, this.formModel);
        returnData['status'] = 'GRN Pending';
        this.dialogRef.close(returnData);
    }

    closeDialog() {
        this.dialogRef.close();
    }
}