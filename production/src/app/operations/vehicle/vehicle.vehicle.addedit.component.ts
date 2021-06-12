import { Component, OnInit, Inject, Optional } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material';
import { Router,ActivatedRoute } from '@angular/router';
import { PopupImgDirective, ImageUploadUrlDialog } from '../.././global/directive/popup-image.directive';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { vehicleService } from '../../operations/vehicle/vechile.vechile.service';
@Component({
	templateUrl: './templates/add_vehicle.html',
  	providers: [vehicleService]
})
export class vehicleAddEditComponent implements OnInit { 
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    public ipaddress: any;
    public country_list: any = [];
    public state_list:any = [];
    public managerList:any=[];
    public zoneList:any=[];
    public warehouseList:any=[];
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public userId: any;
    public warehouse_id: any;
	constructor(
		private _vehicleService:vehicleService,
		public _globalService:GlobalService,
		private _router: Router,
		public dialog: MatDialog,
		private _route: ActivatedRoute,
        private _cookieService: CookieService,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		dialog.afterOpen.subscribe(() => {
           let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
           containerElem.classList.remove('pop-box-up');
        });
        this.ipaddress = _globalService.getCookie('ipaddress'); 
	}
	
	ngOnInit() {
        let userData = this._cookieService.getObject('userData');
        this.userId = userData['uid'];
        this.warehouse_id = userData['warehouse_id'];

        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.sub = this._route.params.subscribe(params => {
            this.formModel.vehicleId = +params['id']; // (+) converts string 'id' to a number
        });

        if(this.formModel.vehicleId > 0) {
        	this._vehicleService.loadVehicleDetails(this.formModel.vehicleId).subscribe(Response => {
        		if(Response["status"] == 1) {
        			this.formModel.id = Response.data.id;
        			this.formModel.vehicle_description = Response.data.vehicle_description;
        			this.formModel.vehicle_number = Response.data.vehicle_number;
        			this.formModel.model_no = Response.data.model_no;
        			this.formModel.vehicle_address1 = Response.data.address1;
        			this.formModel.vehicle_address2 = Response.data.address2;
        			this.formModel.vehicle_city = Response.data.city;
        			this.formModel.vehicle_country_id = Response.data.country_id;
        			this.formModel.state_id = Response.data.state_id;
        			this.formModel.vehicle_mobile_number = Response.data.phone_number;
        			this.formModel.vehicle_zipcode = Response.data.zip_code;
        			this.formModel.delivery_manager = +Response.data.manager_id;
        			if(Response.data.warehouse_ids!='') {
						// console.log(Response.data.warehouse_ids);
						//this.formModel.vehicle_warehouse = Response.data.warehouse_ids.split(',');
        				// this.formModel.vehicle_warehouse = Response.data.warehouse_ids.split(',').map(function(item) {
						//     return parseInt(item, 10);
						// });
						var ware_house = Response.data.warehouse_ids;
                        var array = ware_house.split(",").map(Number);
                        console.log(array)
                        this.formModel.vehicle_warehouse = array;
        			} else {
        				this.formModel.vehicle_warehouse = [];
        			}
        			// console.log(this.formModel);
        		} else {
        			this._globalService.showToast(Response.Message);
        		}
        	}, err => {
        		
        	})
        }

        this.getCountryList();
        this.formModel.vehicle_country_id = 99;
        this.getState(this.formModel.vehicle_country_id);
        this.loadManagerList();
        // this.loadZoneMaster();
        this.loadWarehouseList();
	}


	addEditVehicle(form: any){ 
		let data:any={};
		if(this.formModel.vehicleId > 0) {
			data.id = this.formModel.vehicleId;
		}
		data.vehicle_description = this.formModel.vehicle_description;
		data.vehicle_number = this.formModel.vehicle_number;
		data.address1 = this.formModel.vehicle_address1;
		data.address2 = this.formModel.vehicle_address2;
		data.model_no = this.formModel.model_no;
		data.country_id = this.formModel.vehicle_country_id;
		data.state_id = this.formModel.state_id;
		data.city = this.formModel.vehicle_city;
		data.phone_number = this.formModel.vehicle_mobile_number;
		data.zip_code = this.formModel.vehicle_zipcode;
		data.manager_id = this.formModel.delivery_manager;
		data.warehouse_ids = this.formModel.vehicle_warehouse.join(",");
		data.website_id = this._globalService.getWebsiteId();
		this._vehicleService.saveVehicleData(data).subscribe( res => {
			if(res['status'] == 1) {
				this._globalService.showToast(res['Message']);
				this._router.navigate(['/vehicle']);
			} else {
				this._globalService.showToast(res['Message']);
			}
		} , err => {

		})
	}

	getCountryList() {
        this._vehicleService.loadCountry().subscribe(data => {
            this.country_list = data.countrylist; // list of country list
        }, err => {}, function() { // call back function when exection is done
        })
    }

    getState(country_id: number) {
        this._vehicleService.loadStates(country_id).subscribe(data => {
            this.state_list = data.states;
        }, err => console.log(err), function() {});
    }
    
    loadManagerList() {
    	let data:any={};
    	data["website_id"] = this._globalService.getWebsiteId();
        this._vehicleService.loadManagerList(data).subscribe(data => {
            if(data.status == 1) {
                this.managerList = data["data"];
            }
        }, err => console.log(err), function() {});
    }

    loadWarehouseList() {
        this._vehicleService.loadWarehouseList().subscribe(res => {
            if(res.status == 1) {
                this.warehouseList = res.api_status;
            }
        }, err => console.log(err), function() {});
    }

    loadZoneMaster() {
        this._vehicleService.loadZoneMaster().subscribe(res => {
            if(res.status == 1) {
                this.zoneList = res.data;
            }
        }, err => console.log(err), function() {});
    }
}


