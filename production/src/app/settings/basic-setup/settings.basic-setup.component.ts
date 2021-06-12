import {
    Component, OnInit, Input, AfterViewInit, ElementRef, Inject
}
from '@angular/core';
import {
    GlobalService
}
from '../../global/service/app.global.service';
import {
    Global
}
from '../../global/service/global';
import {
    DOCUMENT
}
from '@angular/platform-browser';
import {
    CookieService
}
from 'ngx-cookie';
import {
    Router, ActivatedRoute
}
from '@angular/router';
import {
    DomSanitizer
}
from '@angular/platform-browser';
import {
    MatAutocompleteSelectedEvent, MatAutocompleteTrigger, MatDialog, MatDialogRef, MAT_DIALOG_DATA, MatTabsModule
}
from '@angular/material';
import {
    DialogsService
}
from '../../global/dialog/confirm-dialog.service';
import {
    BasicSetupService
}
from './settings.basic-setup.service';
import {
    FlatShipAddEditComponent, TableRateAddEditComponent, FreeShippingComponent, CODZipcodeComponent
}
from './settings.basic-setup.addedit.component';
import {
    AddEditTransition
}
from '../.././addedit.animation';
@
Component({
    selector: 'my-app',
    template: `<global-grid [childData]='childData'></global-grid>`,
})
export class BasicSetupComponent {
    public tabIndex: number;
    public parentId: number = 0;
    childData = {};
    constructor(
            public _globalService: GlobalService,
        ) {
        this.tabIndex = +_globalService.getCookie('active_tabs');
        this.parentId = _globalService.getParentId(this.tabIndex);
        this.childData = {
            table: 'EngageboostCompanyWebsites',
            heading: 'Basic Setup',
            ispopup: 'N',
            is_import: 'N',
            is_export: 'N',
            tablink: 'basicsetup',
            tabparrentid: this.parentId,
            screen: 'list'
        }
    }
}

@Component({
    templateUrl: `./templates/shipping_list.html`,
    providers: [Global, BasicSetupService],
    animations: [AddEditTransition],
    host: {
        '[@AddEditTransition]': ''
    },
})
export class BasicSetupShippingComponent implements OnInit, AfterViewInit {
    constructor(
        public globalService: GlobalService,
        private global: Global,
        private _router: Router,
        private _route: ActivatedRoute,
        private sanitizer: DomSanitizer,
        private dialogsService: DialogsService,
        private elRef: ElementRef,
        private _cookieService: CookieService,
        public dialog: MatDialog,
        private _basicSetupService: BasicSetupService, @Inject(DOCUMENT) private document: any,
        public _globalService: GlobalService

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
    public flat_shipping_method_result: any = [];
    public table_rate_result: any = [];
    public free_shipping_result: any = [];
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
    public formModel: any = {};
    public tabIndex: number;
    public parentId: number = 0;
    public companyId: any;
    public websiteId: any;
    public sub: any;
    public settingsId: number;
    public ship_type: number;
    public country_list: any = [];
    public selected_tab: any;
    public selected_shipping_master_id: any;
    public flatSippingMethodFlag:boolean = false;
    public tableRateSettings: boolean = false;
    //////////////////////////Initilise////////////////////////////
    ngOnInit() {
        // this.formModel.UPS_title ='Test';
        let userData = this._cookieService.getObject('userData');
        this.userId = userData['uid'];
        this.websiteId = userData['website_id'];
        this.companyId = userData['company_id'];
        this.tabIndex = +this.globalService.getCookie('active_tabs');
        this.parentId = this.globalService.getParentId(this.tabIndex);
        this.sub = this._route.params.subscribe(params => {
            this.settingsId = +params['id']; // (+) converts string 'id' to a number
        });
        this._route.url.subscribe(() => {
            this.ship_type = this._route.snapshot.data['ship_type'];
        });

        this._basicSetupService.checksettings(this.websiteId, 4).subscribe(
            result => {
                if (result.status == 1) {
                    this.flatSippingMethodFlag = true;
                } else {
                    this.flatSippingMethodFlag = false;
                }
            }, err => {

            }
        )


        this.childData = {
            table: 'EngageboostShippingMastersSettings',
            heading: (this.ship_type == 1) ? 'Flat Shipping Methods' : 'Free Shipping Methods',
            ispopup: 'Y',
            tablink: 'basicsetup',
            screen: 'list-flat-shipping',
            tabparrentid: this.parentId,
            shipping_method_id: 4,
        }
                
        this.loadShippingMethod(0, '', '', '', '', 4, 0);


    }
    ngAfterViewInit() {
        //  setTimeout(() => {
        //    this.globalService.showLoaderSpinner(true);
        //  });
    }
    generateGrid(reload: any, page: any, sortBy: any, filter: any, search: any) {
        let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
        elements[0].classList.remove('show-tab');
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
        let visibility_id: any;
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
        //this.post_data={"model":this.childData.table,"screen_name":this.childData.screen,"userid":this.userId,"search":"","order_by":sortBy,"order_type":this.sortOrder,"status":filter,"website_id": this.websiteId,"company_id": this.companyId}
        this.post_data = {
            "model": this.childData.table,
            "screen_name": this.childData.screen,
            "userid": this.userId,
            "search": "",
            "order_by": sortBy,
            "order_type": this.sortOrder,
            "status": filter,
            "website_id": this.websiteId,
        }
        this.global.doGrid(this.post_data, page).subscribe(
            data => {
                let that = this;
                this.response = data;
                this.total_list = [];
                if (this.response.count > 0) {
                    this.result_list = this.response.results[0].result;
                    this.result_list.forEach(function(item: any) {
                        if (item.isblocked == 'n') {
                            item.isblocked = 'Active';
                        } else {
                            item.isblocked = 'Inactive';
                        }
                    });
                    for (let i = 0; i < this.response.count; i++) {
                        this.total_list.push(i);
                    }
                } else {
                    this.result_list = [];
                }
                // this.cols = this.response.results[0].layout;
                this.cols = this.response.results[0].applied_layout;
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
            },
            err => console.log(err),
            function() {
                that.globalService.showLoaderSpinner(false);
            }
        );
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
                            this.global.doStatusUpdate(this.childData.table, this.bulk_ids, type).subscribe(
                                data => {
                                    this.response = data;
                                    this.loadShippingMethod(0, '', '', '', '', 4, 0); 
                                    this.loadShippingMethod(0, '', '', '', '', 5, 1);
                                    this.loadShippingMethod(0, '', '', '', '', 6, 2);
                                    this.globalService.showToast(this.response.Message);
                                    //this.loadShippingMethod(0, '', '', '', '',this.selected_shipping_master_id,this.selected_tab); // Flat Shipping Method
                                },
                                err => console.log(err),
                                function() {}
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

    updateStatusAllCOD(type: number, id: number) {
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
            }
            if (perm == 'Y') {
                if (this.bulk_ids.length > 0) {
                    this.dialogsService.confirm('Warning', msg).subscribe(res => {
                        if (res) {
                            let data: any = {};
                            data.website_id=this._globalService.getWebsiteId();
                            data.id=this.bulk_ids;
                            this.global.getWebServiceData('del-cod','POST',data,'').subscribe(res => { 
                                if (res['status'] == '1') { // success response 
                                    this.loadShippingMethod(0, '', '', '', '', 6, 2);
                                    this._globalService.showToast(res['message']);
                                } else {
                                    this._globalService.showToast(res['message']);
                                }
                                setTimeout(() => {
                                    this._globalService.showLoaderSpinner(false);
                                });
                            })
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
    toggleCheckAll(event: any,type) {
        let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
        let that = this;
        that.bulk_ids = [];
        this.selectedAll = event.checked;
        this.result_list.forEach(function(item: any) {
            item.selected = event.checked;
            if (item.selected) {
                that.bulk_ids.push(item.id);
                elements[0].classList.add('show-tab');
            } else {
                elements[0].classList.remove('show-tab');
            }
        });
    }
    toggleCheck(id: any, event: any) {
        let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
        let that = this;
        console.log(elements);
        
        //that.bulk_ids=[];
        this.result_list.forEach(function(item: any) {
            if (item.id == id) {
                item.selected = event.checked;
                if (item.selected) {
                    that.bulk_ids.push(item.id);
                    elements[0].classList.add('show-tab');
                } else {
                    let index = that.bulk_ids.indexOf(item.id);
                    that.bulk_ids.splice(index, 1);
                    if (that.bulk_ids.length == 0) {
                        elements[0].classList.remove('show-tab');
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
    toggleCheckShipping(id: any, event: any, shipping_method: any) {
            let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
            if (shipping_method == 'Free-Shipping') {
                let that = this;
                this.flat_shipping_method_result.forEach(function(item: any) {
                    if (item.id == id) {
                        item.selected = event.checked;
                        if (item.selected) {
                            that.bulk_ids.push(item.id);
                            elements[0].classList.add('show-tab');
                        } else {
                            let index = that.bulk_ids.indexOf(item.id);
                            that.bulk_ids.splice(index, 1);
                            if (that.bulk_ids.length == 0) {
                                elements[0].classList.remove('show-tab');
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
    }
    /////////////////////////Filter Grid//////////////////////
    updateGrid(isdefault: any) {
        let list: string = 'list';
        if (this.ship_type) {
            list = 'list1';
        }
        this.global.doGridFilter('EngageboostShippingMastersSettings', isdefault, this.cols, list).subscribe(
            data => {
                this.response = data;
                //this.generateGrid(0, '', '', '', '');
                this.loadShippingMethod(0, '', '', '', '', this.selected_shipping_master_id, this.selected_tab); // Flat Shipping Method
            },
            err => console.log(err),
            function() {}
        );
    }
    dialogRefFlatShip: MatDialogRef < FlatShipAddEditComponent > | null;
    dialogRefTableRate: MatDialogRef < TableRateAddEditComponent > | null;
    dialogRefFreeShipping: MatDialogRef < FreeShippingComponent > | null;
    dialogRefCODZipcode: MatDialogRef < CODZipcodeComponent > | null;
    openPop(shipping_master_type: any, id: any) {
        let data: any = {};
        data['id'] = id;
        data['shipping_master_type'] = shipping_master_type;
        if (shipping_master_type == 'Flat-Shipping') {
            data['import_file'] = '';
            data['shipping_master_type_id'] = 4;
            this.dialogRefFlatShip = this.dialog.open(FlatShipAddEditComponent, {
                data: data
            });
            this.dialogRefFlatShip.afterClosed().subscribe(result => {
                //this.generateGrid(0, '', '', '', '');
                this.childData = {
                    table: 'EngageboostShippingMastersSettings',
                    heading: 'Flat Shipping',
                    ispopup: 'Y',
                    tablink: 'basicsetup',
                    screen: 'list-flat-shipping',
                    tabparrentid: this.parentId,
                    shipping_method_id: 4,
                }
                this.loadShippingMethod(0, '', '', '', '', 4, 0); // Flat Shipping Method
                let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
                elements[0].classList.remove('show-tab');
            });
        } else if (shipping_master_type == 'Table-Rate') {
            data['import_file'] = '';
            data['shipping_master_type_id'] = 6;
            this.dialogRefTableRate = this.dialog.open(TableRateAddEditComponent, {
                data: data
            });
            this.dialogRefTableRate.afterClosed().subscribe(result => {
                //this.generateGrid(0, '', '', '', '');
                this.childData = {
                    table: 'EngageboostShippingMastersSettings',
                    heading: 'Table Rate Shipping',
                    ispopup: 'Y',
                    tablink: 'basicsetup',
                    screen: 'list-flat-shipping',
                    tabparrentid: this.parentId,
                    shipping_method_id: 5,
                }
                this.loadShippingMethod(0, '', '', '', '', 5, 1);
                let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
                elements[0].classList.remove('show-tab');
            });
        } else if (shipping_master_type == 'Free-Shipping') {
            data['import_file'] = '';
            data['shipping_master_type_id'] = 6;
            this.dialogRefFreeShipping = this.dialog.open(FreeShippingComponent, {
                data: data
            });
            this.dialogRefFreeShipping.afterClosed().subscribe(result => {
                this.childData = {
                    table: 'EngageboostShippingMastersSettings',
                    heading: 'Free Shipping',
                    ispopup: 'Y',
                    tablink: 'basicsetup',
                    screen: 'list-free-shipping',
                    tabparrentid: this.parentId,
                    shipping_method_id: 6,
                }
                this.loadShippingMethod(0, '', '', '', '', 6, 2);
                let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
                //console.log(elements);
                elements[0].classList.remove('show-tab');
            });
        } else if (shipping_master_type == 'COD-Zipcode') {
            data['import_file'] = '';
            data['shipping_master_type_id'] = 23;
            this.dialogRefCODZipcode = this.dialog.open(CODZipcodeComponent, {
                data: data
            });
            this.dialogRefCODZipcode.afterClosed().subscribe(result => {
                this.childData = {
                    table: 'EngageboostFedexZipcodes',
                    heading: 'COD ',
                    ispopup: 'Y',
                    tablink: 'basicsetup',
                    screen: 'list',
                    tabparrentid: this.parentId,
                    shipping_method_id: 23,
                }
                this.loadShippingMethod(0, '', '', '', '', 23, 6);
                let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
                //console.log(elements);
                elements[0].classList.remove('show-tab');
            });
        }
    }
    /////////////////////////Grid for shipping method //////////////////////////////////////////////
    loadShippingMethod(reload: any, page: any, sortBy: any, filter: any, search: any, shipping_method_id: any, tab_number: number) {
        let userData = this._cookieService.getObject('userData');
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
        let visibility_id: any;
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
        //console.log(this.country_list);
        this.post_data = {
            "model": this.childData.table,
            "screen_name": this.childData.screen,
            "userid": this.userId,
            "search": "",
            "order_by": sortBy,
            "order_type": this.sortOrder,
            "status": filter,
            "website_id": this.websiteId,
            "shipping_method_id": shipping_method_id
        }
        this.global.doGrid(this.post_data, page).subscribe(
            data => {
                let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
                //console.log(elements);
                elements[0].classList.remove('show-tab');
                let that = this;
                //console.log(data);
                this.response = data;
                this.total_list = [];
                if (this.response.count > 0) {
                    this.result_list = this.response.results[0].result;
                    this.result_list.forEach(function(item: any) {

                        if (item.handling_price>0) {
                            item.handling_price = userData["currencysymbol"] + item.handling_price.toFixed(2) +' ' +(item.mthod_type == 1 ? '(Per Item)' : '(Per Order)');
                        }

                        if (item.flat_price > 0) {
                            item.flat_price = userData["currencysymbol"] + item.flat_price.toFixed(2) +' ' + ' ' + (item.handling_fees_type == 0 ? '' : '%');
                        }

                        if (item.dispatch_time_max > 0) {
                            item.dispatch_time_max = item.dispatch_time_max+ " days";
                        }

                        if (item.isblocked == 'n') {
                            item.isblocked = 'Active';
                        } else {
                            item.isblocked = 'Inactive';
                        }
                    });
                    for (let i = 0; i < this.response.count; i++) {
                        this.total_list.push(i);
                    }
                } else {
                    this.result_list = [];
                }
                if (tab_number == 0) { //  Flat Shipping Method
                    this.flat_shipping_method_result = this.result_list;
                } else if (tab_number == 1) { // table Rate shipping
                    this.table_rate_result = this.result_list;
                } else if (tab_number == 2) { // Free shipping
                    this.free_shipping_result = this.result_list;
                }
                // this.cols = this.response.results[0].layout;
                this.cols = this.response.results[0].applied_layout;
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
                this.globalService.showLoaderSpinner(false);
            },
            err => console.log(err),
            function() {
                // that.globalService.showLoaderSpinner(false);
            }
        );
    }
    shipping_setup(event) {
        let tab_number = event.index;
        let shipping_master_id = 4;
        let websiteId = this.globalService.getWebsiteId();
        if (tab_number == 0) { //  Flat Shipping Method
            let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
            elements[0].classList.remove('show-tab');
            shipping_master_id = 4;

            this.checksettingStatus(shipping_master_id,websiteId)
            
            this.childData = {
                table: 'EngageboostShippingMastersSettings',
                heading: 'Flat Shipping Methods',
                ispopup: 'Y',
                tablink: 'basicsetup',
                screen: 'list-flat-shipping',
                tabparrentid: this.parentId,
                shipping_method_id: shipping_master_id,
            }
            this.loadShippingMethod(0, '', '', '', '', shipping_master_id, tab_number);
            //this.globalService.showLoaderSpinner(false);
        }
       
        if (tab_number == 1) { //  Free Shipping Method
            let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
            elements[0].classList.remove('show-tab');
            let shipping_master_id = 6;
            this.checksettingStatus(shipping_master_id, websiteId)
            this.childData = {
                table: 'EngageboostShippingMastersSettings',
                heading: 'Free Shipping Methods',
                ispopup: 'Y',
                tablink: 'basicsetup',
                screen: 'list-free-shipping',
                tabparrentid: this.parentId,
                shipping_method_id: 6,
            }
            this.loadShippingMethod(0, '', '', '', '', 6, 2);
        }
        if (tab_number == 2) { // COD
            let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
            //console.log(elements);
            elements[0].classList.remove('show-tab');
            let shipping_master_id = 23;
            this.checksettingStatus(shipping_master_id, websiteId)
            this.ngAfterViewInit();
            this.childData = {
                table: 'EngageboostFedexZipcodes',
                heading: 'COD ',
                ispopup: 'Y',
                tablink: 'basicsetup',
                screen: 'list',
                tabparrentid: this.parentId,
                shipping_method_id: 23,
            }
            this.loadShippingMethod(0, '', '', '', '', 23, tab_number);
        }
        this.selected_tab = tab_number;
        this.selected_shipping_master_id = shipping_master_id;
    }

    checksettingStatus(websiteId, shipping_master_id) {
        this._basicSetupService.checksettings(websiteId, shipping_master_id).subscribe(
            result => {
                if (result.status == 1) {
                    this.flatSippingMethodFlag = true;
                } else {
                    this.flatSippingMethodFlag = false;
                }
            }, err => {

            }
        )
    }

    ShippingSetup(form_name: any) {
        if (form_name == 'UPSSettingss') {
            let data: any = {};
            let country_id_str: any;
            data.website_id = 1;
            data.shipping_id = 183;
            data.shipping_method_id = 1;
            data.title = this.formModel.UPS_title;
            data.ups_user_id = this.formModel.UPS_ups_user_name;
            data.ups_account_number = this.formModel.ups_account_number;
            data.ups_password = this.formModel.UPS_ups_password;
            data.fedex_key = '';
            data.usps_devolopment_mode = this.formModel.UPS_devolopment_mode1;
            data.ups_min_weight = this.formModel.UPS_ups_min_weight;
            data.ups_max_weight = this.formModel.UPS_ups_max_weight;
            data.handling_price = this.formModel.UPS_handling_price;
            data.handling_fees_type = this.formModel.UPS_handling_fees;
            data.minimum_order_amount = this.formModel.UPS_minimum_order_amount;
            data.package_code = this.formModel.UPS_package;
            data.status = 'yes';
            country_id_str = this.formModel.country_id.join(',');
            data.country_ids = country_id_str;
            data.service_methods_free = this.formModel.UPS_shipping_methods_free;
            this._basicSetupService.saveShippingSettingsData(data).subscribe(
                data => {
                    this.globalService.showToast("Data saved successfully");
                },
                err => {
                    this.globalService.showToast('Something went wrong. Please try again.');
                },
                function() {
                    //completed callback
                }
            );
        }
        if (form_name == 'FedexSettings') {
            let data: any = {};
            let country_id_str: any;
            let service_code_str: any;
            data.website_id = 1;
            data.shipping_id = 185;
            data.shipping_method_id = 3;
            data.title = this.formModel.fedex_title;
            data.fedex_user_id = this.formModel.fedex_user_id;
            data.fedex_meter_no = this.formModel.fedex_fedex_meter_no;
            data.fedex_key = this.formModel.fedex_key;
            data.fedex_password = this.formModel.fedex_password;
            data.ups_min_weight = this.formModel.FEDEX_ups_min_weight;
            data.ups_max_weight = this.formModel.FEDEX_ups_max_weight;
            data.handling_price = this.formModel.FEDEX_handling_price;
            data.handling_fees_type = this.formModel.FEDEX_handling_fees;
            data.minimum_order_amount = this.formModel.FEDEX_minimum_order_amount;
            data.status = 'yes';
            country_id_str = this.formModel.fedex_country.join(',');
            data.country_ids = country_id_str;
            data.package_code = '0';
            //service_code_str = this.formModel.service_methods.join(',');
            data.service_methods = '';
            data.service_methods_free = this.formModel.service_methods.FEDEX_shipping_methods_free;
            this._basicSetupService.saveShippingSettingsData(data).subscribe(
                data => {
                    this.globalService.showToast("Data saved successfully");
                },
                err => {
                    this.globalService.showToast('Something went wrong. Please try again.');
                },
                function() {
                    //completed callback
                }
            );
        }
    }
    applicable_shippings(event, shipping_master_type, shipping_master_id ) {
        console.log(event.checked);
        let flag = event.checked == true ? 1 : 0;
        let website_id = this.globalService.getWebsiteId();
        let data:any = {}
        data.status = flag;
        data.website_id = website_id;
        data.shipping_method_id = shipping_master_id;
        this.global.getWebServiceData("shippingmethodstatus","POST",data,"").subscribe(
            result => {
                console.log(result);
            },err => {

            }
        )

    }
}