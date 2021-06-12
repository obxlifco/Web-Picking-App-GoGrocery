import { Component, OnInit, Inject } from '@angular/core';
import { Router,ActivatedRoute } from '@angular/router';
import {CookieService} from 'ngx-cookie';
import { SupplierService } from './inventory.supplier.service';
import { GlobalService } from '../../global/service/app.global.service';
import {Global} from '../../global/service/global';
@Component({
  templateUrl: './templates/add_supplier.html',
  providers: [SupplierService]
})
export class SupplierAddEditComponent implements OnInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    public List: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public add_edit: any;
    public ipaddress: any;
    constructor(
        private _supplierService: SupplierService,
        private _cookieService: CookieService,
        public _globalService: GlobalService,
        private _router: Router,
        private _route: ActivatedRoute,
        private _global:Global,
    ) {
        this.ipaddress = _globalService.getCookie('ipaddress');
    }

    ngOnInit() {
        this.sub = this._route.params.subscribe(params => {
            this.formModel.supplierId = +params['id']; // (+) converts string 'id' to a number
        });
        this.tabIndex = +this._globalService.getCookie('active_tabs'); // current active tab index
        this.parentId = this._globalService.getParentTab(this.tabIndex); // parent id of the current active tab

        if (this.formModel.supplierId) {
            this._cookieService.putObject('supplier_edit', this.formModel.supplierId);
            this._cookieService.putObject('action', 'edit');
            this.add_edit = 'edit';
        } else {
            this._cookieService.putObject('action', 'add');
            this.formModel.supplierId = this._cookieService.getObject('supplier_add');
            this.add_edit = 'add';
        }
        this.loadsupplieruser(); // loading the master data 
        this._supplierService.supplierLoad(this.formModel.supplierId).subscribe(
            data => {
				this.response = data;
                if (this.formModel.supplierId > 0) {
                    this.formModel = this.response.api_status;
                    this.formModel.supplierId = this.response.api_status.id;
                    this.formModel.state = +this.response.api_status.state;
                    if(this.formModel.state == 0){
                        this.formModel.state = null;
                    }
                    this.List.country_list = this.response.countries;
                    this.List.currency_list = this.response.currency;
                    this.List.vendor_list = this.response.vendor;
                    this.List.warehouse_list = this.response.warehouse;
                    this.List.state_list = this.response.State;
				} else {
                    this.formModel.supplierId = 0;
                    this.List.country_list = this.response.countries;
                    this.List.currency_list = this.response.currency;
                    this.List.vendor_list = this.response.vendor;
                    this.List.warehouse_list = this.response.warehouse;
                    this.formModel.isblocked = 'n';
                    this.formModel.country_id = 99;
                    this.get_states(this.formModel.country_id);
                }
            },
            err => console.log(err),
            function() {
                //completed callback
            }
        );
	}

    loadsupplieruser() {
        this._global.getWebServiceData('manager_list','GET','','').subscribe(
            data => {
                if(data.status == 1) {
                    this.List.userList  =  data.users;
                } else {
                    this.List.userList  =  [];
                }
            } , err => {

            }
        );
    }

    get_states(id: any) {
        var country_id = id;
        if (country_id > 0) {
            this._supplierService.supplierState(country_id).subscribe(
                data => {
                    this.response = data;

                    if (this.response) {

                        this.List.state_list = this.response.state_arr;

                    } else {

                        this.errorMsg = this.response.message;
                    }
                },
                err => console.log(err),
                function() {
                    //completed callback
                }
            );
        }
    }

    getStates(id: any) {
        this.formModel.state = null;
        var country_id = id;
        if (country_id > 0) {
            this._supplierService.supplierState(country_id).subscribe(
                data => {
                    this.response = data;

                    if (this.response) {

                        this.List.state_list = this.response.state_arr;

                    } else {

                        this.errorMsg = this.response.message;
                    }
                },
                err => console.log(err),
                function() {
                    //completed callback
                }
            );
        }
    }

    addEditSupplier(form: any) {
	    this.errorMsg = '';
        var data: any = {};
        data = Object.assign({}, this.formModel);
        data.website_id = 1;
        if (this.formModel.supplierId < 1) {
            data.created_by = this._globalService.getUserId();
        }
        data.user_id = this._globalService.getUserId();
        data.modified_by = this._globalService.getUserId();
        data.ip_address = this.ipaddress;
        this._supplierService.supplierAddEdit(data, this.formModel.supplierId).subscribe(
            data => {
                this.response = data;

                if (this.response.status == 1) {

                    if (this.add_edit == 'add') {
                        this._cookieService.putObject('supplier_add', this.response.api_status);
                        this._router.navigate(['/suppliers/add/purchase_order']);
                    } else {
                        this._router.navigate(['/suppliers/edit/' + this.formModel.supplierId + '/purchase_order']);
                    }

                } else {

                    this.errorMsg = this.response.message;
                }
            },
            err => console.log(err),
            function() {
                //completed callback
            }
        );
	}
}
