import {Component, ElementRef, OnInit, Input, Inject, AfterViewInit, Optional } from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { Global } from '../../global/service/global';
import { Router, ActivatedRoute } from '@angular/router';
import { DeliverymanagerService } from './deliverymanager.service';
@Component({
    selector: 'app-manager.addedit',
    templateUrl: 'templates/manager.addedit.component.html',
    providers: [DeliverymanagerService],
    animations: [],
    host: {},
})
export class ManagerAddeditComponent implements OnInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public ipaddress: any;
    public managerList: any = [];
    // public zoneList: any = [];
    public warehouseList:any=[];
    public userId: any;
    public warehouse_id: any;
    constructor(
        private _deliverymanagerService: DeliverymanagerService,
        public _globalService: GlobalService,
        private global: Global,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService
    ) {
        this.ipaddress = _globalService.getCookie('ipaddress');
    }

    ngOnInit() {
        let userData = this._cookieService.getObject('userData');
        this.userId = userData['uid'];
        this.warehouse_id = userData['warehouse_id'];

        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.sub = this._route.params.subscribe(params => {
            this.formModel.executiveId = +params['id']; // (+) converts string 'id' to a number
        });
        
        if (this.formModel.executiveId > 0) {
            this._deliverymanagerService.getManagereDetails(this.formModel.executiveId).subscribe(Response => {
                let data= Response.data[0];
                this.formModel.executive_name = data.name;
                this.formModel.executive_email = data.email;
                this.formModel.executive_address1 = data.address1;
                this.formModel.executive_address2 = data.address2;
                if (data.warehouse_ids != '') {
                    // let warehouse_ids = data.warehouse_ids.join(',');
                    // this.formModel.warehouse_ids = warehouse_ids.split(',').map(function(item) {
                    //     return parseInt(item, 10);
                    // });
                    let warehouse_ids = data.warehouse_ids.join(',');
                    var array = warehouse_ids.split(",").map(Number);
                    console.log(array)
                    this.formModel.warehouse_ids = array;
                } else {
                    this.formModel.warehouse_ids = [];
                }
                this.formModel.executive_mobile_number = data.phone;
                this.formModel.delivery_manager = data.user_id;
            }, err => {

            })
        }

        this.loadManagerList();
        // this.loadZoneMaster();
        // this.loadWarehouseList();

        let websiteId = this._globalService.getWebsiteId();
        this.global.warehouseLoad(websiteId, this._globalService.getUserId()).subscribe(
            data => {
                this.warehouseList = data.warehouse;
            },
            err => console.log(err),
            function() {
                //completed callback
            }
        );
        
    }

    addEditManeger(form: any) {
        this._globalService.showLoaderSpinner(false);
        if(this.formModel.executive_mobile_number<1111111111){
            this._globalService.showToast('Please enter a valid mobile number');
        } else {
            let data: any = {};
            data.website_id = this._globalService.getWebsiteId();
            data.user_id = this.formModel.delivery_manager;
            data.name = this.formModel.executive_name;
            data.email = this.formModel.executive_email;
            data.phone = this.formModel.executive_mobile_number;
            data.warehouse_ids = this.formModel.warehouse_ids.join(",");
            data.address1 = this.formModel.executive_address1;
            data.address2 = this.formModel.executive_address2;
            data.executive_linked = this.formModel.delivery_manager;
            if (this.formModel.executiveId > 0) {
                data.id = this.formModel.executiveId;
            }
            this._deliverymanagerService.saveMasterData(data).subscribe(res => {
                if (res['status'] == '1') { // success response 
                    this._globalService.showToast(res['Message']);
                } else {
                    this._globalService.showToast(res['Message']);
                }
                this._globalService.showLoaderSpinner(false);
                this._router.navigate(['/delivery_manager/']);
            }, err => {

            })
        }
    }

    loadManagerList() {
        this.global.getWebServiceData('manager_list','GET','','').subscribe(data => {
            if (data.status == 1) {
                this.managerList = data.users;
            }
        }, err => console.log(err), function() {});
    }

    // loadZoneMaster() {
    //     this.global.getWebServiceData('zone_list','GET','','').subscribe(res => {
    //         if(res.status == 1) {
    //             this.zoneList = res.data;
    //         }
    //     }, err => console.log(err), function() {});
    // }

    loadWarehouseList() {
        this.global.getWebServiceData('warehouse-list','GET','','').subscribe(res => {
            if(res.status == 1) {
                this.warehouseList = res.api_status;
            }
        }, err => console.log(err), function() {});
    }
}