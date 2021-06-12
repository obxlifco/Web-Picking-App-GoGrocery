import { Component, ElementRef, OnInit, Input, Inject, AfterViewInit, Optional } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { Router, ActivatedRoute } from '@angular/router';
import { CustomergroupService } from './customergroup.service';
import { GlobalService } from '../../global/service/app.global.service';
import { Global } from '../../global/service/global';
import { CookieService } from 'ngx-cookie';
import { AddEditTransition, AddEditStepFlipTransition } from '../.././addedit.animation';
import { DOCUMENT } from '@angular/platform-browser';

@Component({
    selector: 'app-customergroup.addedit',
    templateUrl: 'templates/customergroup.addedit.component.html',
    providers: [CustomergroupService],
    animations: [AddEditTransition],
    host: {
        '[@AddEditTransition]': ''
    },
})

export class CustomergroupAddeditComponent implements OnInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public rolelist: any;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public ipaddress: any;
    public zipCodeList: any = [];
    public zipAreaList: any = [];
    public locationType: any = 'Z';
    public userId: any;
    public mobErro: any;
    public customer_ids: any;
    public all_customer_ids: any;
    constructor(
        private _customergroupService: CustomergroupService,
        public _globalService: GlobalService,
        private global: Global,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService,
        public dialog: MatDialog,
    ) {
        this.ipaddress = _globalService.getCookie('ipaddress');
    }

    ngOnInit() {
        let userData = this._cookieService.getObject('userData');
        this.userId = userData['uid'];
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.sub = this._route.params.subscribe(params => {
            this.formModel.formId = +params['id']; // (+) converts string 'id' to a number
        });
        if (this.formModel.formId > 0) {
            this.global.getWebServiceData('customergrouplist', 'GET', '', this.formModel.formId).subscribe(Response => {
                let data = Response.api_status;
                this.formModel.group_name = data.name;
                this.formModel.view_type = data.view_type == 1 ? 'withlogin' : 'withoutlogin';
                this.formModel.customer_ids = data.customers;
                this.all_customer_ids = data.customer_ids;
                console.log(data);

            }, err => {

            })
        } else {
            this.formModel.view_type = 'withlogin';
        }
    }

    addEditManeger(form: any) {
        let data: any = {};
        data.website_id = this._globalService.getWebsiteId();
        data.name = this.formModel.group_name;
        data.view_type = this.formModel.view_type == 'withlogin' ? 1 : 0;
        data.customer_ids = this.customer_ids;
        //data.isblocked = 'n';
        if (this.formModel.formId > 0) {
            this.global.getWebServiceData('customergrouplist', 'PUT', data, this.formModel.formId + '/').subscribe(res => { // UPDATE
                if (res['status'] == '1') { // success response 
                    this._globalService.showToast(res['message']);
                } else {
                    this._globalService.showToast(res['message']);
                }
                this._router.navigate(['/customer_group/']);
            }, err => {

            })
        } else {
            this.global.getWebServiceData('customergroup', 'POST', data, '').subscribe(res => {
                if (res['status'] == '1') { // success response 
                    this._globalService.showToast(res['message']);
                } else {
                    this._globalService.showToast(res['message']);
                }
                this._router.navigate(['/customer_group/']);
            }, err => {

            })
        }

    }

    openPopup() {
        console.log(this.all_customer_ids);

        let data: any = {};
        data['all_customer_ids'] = this.all_customer_ids;
        this.dialogCustomerRef = this.dialog.open(OrderCustomerListComponent, { data: data });
        this.dialogCustomerRef.afterClosed().subscribe(result => {
            if (result) {
                console.log(result)
                this.formModel.customer_ids = result.customer_names;
                this.customer_ids = result.customer_ids;
            }
        });
    }

    dialogCustomerRef: MatDialogRef<OrderCustomerListComponent> | null;
}

@Component({
    templateUrl: './templates/customer-list.html',
    providers: [CustomergroupService]
})
export class OrderCustomerListComponent implements OnInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public bulk_ids: any = [];
    public bulk_ids_exist: any = [];
    public search_text: string;
    public pagination: any = {};
    public pageIndex: number = 0;
    public pageList: number = 0;
    public sortBy: any = '';
    public sortOrder: any = '';
    public sortClass: any = '';
    public sortRev: boolean = false;
    public selectedAll: any = false;
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

    public individualRow: any = {};
    public tabIndex: number;
    public parentId: number = 0;
    public userId: number;

    constructor(
        public _globalService: GlobalService,
        private _customergroupService: CustomergroupService,
        public dialog: MatDialog,
        @Inject(DOCUMENT) private document: any,
        private _cookieService: CookieService,
        private dialogRef: MatDialogRef<OrderCustomerListComponent>,
        @Optional() @Inject(MAT_DIALOG_DATA) public data: any
    ) {

    }

    ngOnInit() {
        this.website_id = this._globalService.getWebsiteId();
        console.log(this.data.all_customer_ids);

        if (this.data.all_customer_ids) {
            this.bulk_ids = this.data.all_customer_ids.split(",").map(Number);
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
            "model": 'EngageboostCustomers',
            "screen_name": 'list',
            "userid": this.userId,
            "search": this.search_text,
            "order_by": sortBy,
            "order_type": this.sortOrder,
            "status": 'n',
            "website_id": this._globalService.getWebsiteId()
        }

        this._customergroupService.customerLoad(data, page).subscribe(
            data => {
                let that = this;
                this.response = data;
                this.total_list = [];

                if (this.response.count > 0) {
                    this.result_list = this.response.results[0].result;
                    this.result_list.forEach(function (item: any) {
                        if (that.bulk_ids.indexOf(item.id) > -1) {
                            item.Selected = true;
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

    saveCustomers() {

        let returnData: any = [];
        returnData['index'] = this.data.index;

        let customer_ids: string = '';
        let customer_names: string = '';
        let customers: any = [];

        customer_ids = this.bulk_ids.join(',');

        let that = this;
        this.bulk_ids.forEach(function (item: any) {

            that.result_list.forEach(function (inner_item: any) {

                if (item == inner_item.id) {
                    customers.push(inner_item.first_name + " " + inner_item.last_name);
                }
            });
        });

        customer_names = customers.join(',');

        returnData['customer_ids'] = customer_ids;
        returnData['customer_names'] = customer_names;

        this.dialogRef.close(returnData);
    }
}	