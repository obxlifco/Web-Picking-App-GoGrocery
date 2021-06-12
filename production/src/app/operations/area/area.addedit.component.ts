import {Component, ElementRef, OnInit, Input, Inject, AfterViewInit, Optional } from '@angular/core';
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
import { AreaService } from '../../operations/area/operation.area.service';

@Component({
    selector: 'app-area-addedit',
    templateUrl: 'templates/area.addedit.component.html',
    providers: [AreaService],
    animations: [ AddEditTransition ],
    host: {
    '[@AddEditTransition]': ''
    },
})

export class AreaAddEditComponent implements OnInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public rolelist: any;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public country_list: any = [];
    public state_list:any = [];
    public managerList:any=[];
    public zoneList:any=[];
    public warehouse_list:any=[];
    public zipCodeList:any=[];
    public zipAreaList:any=[];
    public locationType:any = 'Z';
    constructor(
        private _areaService: AreaService, 
        public _globalService: GlobalService,
        private global: Global,
        private _router: Router,
        private _route: ActivatedRoute
    ) {
    }
    ngOnInit() {
        this.global.globalDataSet.subscribe(dataSet => {
            if(dataSet != 0) {
                this.locationType = dataSet;
            }
        }, err => {
          console.log(err);
        });
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.sub = this._route.params.subscribe(params => {
            this.formModel.zoneId = +params['id']; // (+) converts string 'id' to a number
        });
        if(this.formModel.zoneId  > 0) {
            this._areaService.getZoneDetails(this.formModel.zoneId).subscribe(Response => {
                this.formModel.name = Response.data.name;
                this.formModel.city = Response.data.city;
                this.formModel.zonal_office_address1 = Response.data.office_address1;
                this.formModel.zonal_office_address2 = Response.data.office_address2;
                this.formModel.zone_zipcode = Response.data.zipcode;
                this.formModel.manager_id = Response.data.manager_id;
                this.formModel.warehouse_id = Response.data.warehouse_id;
                this.formModel.zone_country = Response.data.country_id;
                this.formModel.state_id = Response.data.state_id;
                this.formModel.zone_id = Response.data.zone_id;
                this.formModel.zipcode = Response.data.zipcode;
                this.formModel.area_id = Response.data.area_id;
                this.formModel.min_order_amount = Response.data.min_order_amount;
                this.getState(this.formModel.zone_country);
                if(this.locationType == 'S') {
                    this.getZipCodeArea(this.formModel.zone_id);
                }
            } , err => {

            })
        }

        if(this.locationType == 'Z') {
            this.getCountryList();
            this.formModel.zone_country = 99;
            this.getState(this.formModel.zone_country);
            this.loadManagerList();
            this.loadWarehouse();
        } 

        if(this.locationType == 'A') {
            this.loadZoneMaster();
        }

        if(this.locationType == 'S') {
            this.loadZoneMaster();
        }
        
    }
    ngOnDestroy() {
        this.sub.unsubscribe();
    }
    
    addEditZone(form: any) {
        setTimeout(() => {
            this._globalService.showLoaderSpinner(false);
        });
        let data:any = {};
        data.website_id = this._globalService.getWebsiteId();
        data.name = this.formModel.name;
        data.city = this.formModel.city;
        data.country_id = this.formModel.zone_country;
        data.state_id = this.formModel.state_id;
        data.address1 = this.formModel.zonal_office_address1;
        data.address2 = this.formModel.zonal_office_address2;
        data.zipcode = this.formModel.zone_zipcode;
        data.manager_id = this.formModel.manager_id;
        data.warehouse_id = this.formModel.warehouse_id;
        data.location_type = this.locationType;
        if(this.formModel.zoneId > 0) {
            data.id = this.formModel.zoneId;
        }
        console.log(data);
        this._areaService.saveMasterData(data).subscribe(res => {
            if(res['status'] == '') {
                this._globalService.showToast(res['Message']);
            } else {
                this._globalService.showToast(res['Message']);
            }
            setTimeout(() => {
                this._globalService.showLoaderSpinner(false);
            });
            this.global.setData('Z');
            this._router.navigate(['/area_management/']);
        }, err => {

        })
        if(this.formModel.zoneId > 0) {
        } else { 

        }
    }

    addEditArea(form:any) {
        setTimeout(() => {
            this._globalService.showLoaderSpinner(true);
        });
        let data:any = {};
        data.website_id = this._globalService.getWebsiteId();
        data.name = this.formModel.name;
        data.zone_id = this.formModel.zone_id;
        data.location_type = this.locationType;
        if(this.formModel.zoneId > 0) { // this for updated area 
            data.id = this.formModel.zoneId; // this is area id 
        } 
        this._areaService.saveMasterData(data).subscribe(res => {
            if(res['status'] == '') {
                this._globalService.showToast(res['Message']);
            } else {
                this._globalService.showToast(res['Message']);
            }
            setTimeout(() => {
                this._globalService.showLoaderSpinner(false);
            });
            this.global.setData('A');
            this._router.navigate(['/area_management/']);
        }, err => {

        })
    }

    addEditSubArea(form:any) {
         setTimeout(() => {
            this._globalService.showLoaderSpinner(true);
        });
        let data:any = {};
        data.website_id = this._globalService.getWebsiteId();
        data.name = this.formModel.name;
        data.zone_id = this.formModel.zone_id;
        data.area_id = this.formModel.area_id;
        data.zipcode = this.formModel.zipcode;
        data.min_order_amount = this.formModel.min_order_amount;
        data.location_type = this.locationType;
        if(this.formModel.zoneId > 0) { // this for updated subarea 
            data.id = this.formModel.zoneId; // this is sub area id
        } 
        this._areaService.saveMasterData(data).subscribe(res => {
            if(res['status'] == '') {
                this._globalService.showToast(res['Message']);
            } else {
                this._globalService.showToast(res['Message']);
            }
            setTimeout(() => {
                this._globalService.showLoaderSpinner(false);
            });
            this.global.setData('S');
            this._router.navigate(['/area_management/']);
        }, err => {

        })
    }

    getCountryList() {
        this._areaService.loadCountry().subscribe(data => {
            this.country_list = data.countrylist; // list of country list
        }, err => {}, function() { // call back function when exection is done
        })
    }

    getState(country_id: number) {
        console.log(country_id)
        this._areaService.loadStates(country_id).subscribe(data => {
            this.state_list = data.states;
        }, err => console.log(err), function() {});
    }
    
    loadManagerList() {
        this._areaService.loadManagerList().subscribe(data => {
            if(data.status == 1) {
                this.managerList = data.users;
            }
        }, err => console.log(err), function() {});
    }

    loadZoneMaster() {
        this._areaService.loadZoneMaster().subscribe(res => {
            if(res.status == 1) {
                this.zoneList = res.data;
            }
        }, err => console.log(err), function() {});
    }

    loadWarehouse() {
        this._areaService.loadWarehouse().subscribe(res => {
            if(res.status == 1) {
                this.warehouse_list = res.api_status;
            }
        }, err => console.log(err), function() {});
    }

    getZipCodeArea(zoneId:number) {
        let data:any = {};
        data.zone_id = zoneId
        this._areaService.loadZoneZipCode(data).subscribe(res => {
            if(res.status == 1) {
                this.zipCodeList = res.data;
            }
        }, err => console.log(err), function() {});

        this._areaService.loadZoneArea(data).subscribe(res => {
            if(res.status == 1) {
                this.zipAreaList = res.data;
            }
        }, err => console.log(err), function() {});
    }

}