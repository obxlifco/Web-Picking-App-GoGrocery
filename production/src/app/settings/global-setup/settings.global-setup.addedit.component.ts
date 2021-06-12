import {
    Component, OnInit, OnDestroy
}
from '@angular/core';
import {
    Router, ActivatedRoute
}
from '@angular/router';
import {
    GlobalSetupService
}
from './settings.global-setup.service';
import {
    GlobalService
}
from '../../global/service/app.global.service';
import {
    Global
}
from '../../global/service/global';
import {
    AddEditTransition
}
from '../.././addedit.animation';
@
Component({
    templateUrl: './templates/add_global_settings.html',
    providers: [GlobalSetupService, Global],
    animations: [AddEditTransition],
    host: {
        '[@AddEditTransition]': ''
    },
})
export class GlobalSetupAddEditComponent implements OnInit, OnDestroy {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public settingList: any = {};
    public showSmsGateway: boolean = false;
    public showShipCharge: boolean = false;
    public showAlgolia: boolean = false;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public ipaddress: any;
    public maximum_substitute_limit : number;
    public minimum_substitute_limit : number;
    public substitute_approval_time : number;
    // public refund_auto_approve:string = 'Yes';
    
    constructor(
        private _globalSetupService: GlobalSetupService,
        public _globalService: GlobalService,
        private _router: Router,
        private _route: ActivatedRoute
    ) {
        this.ipaddress = _globalService.getCookie('ipaddress');
    }
    ngOnInit() {
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.sub = this._route.params.subscribe(params => {
            this.formModel.settingsId = +params['id']; // (+) converts string 'id' to a number
        });
        this._globalSetupService.settingsLoad(this.formModel.settingsId).subscribe(
            data => {
                
                this.response = data;
                if (this.formModel.settingsId > 0) {
                    this.maximum_substitute_limit = this.response.additional_settings.maximum_substitute_limit;
                    this.minimum_substitute_limit = this.response.additional_settings.minimum_substitute_limit;
                    this.substitute_approval_time = this.response.additional_settings.substitute_approval_time;
                    this.formModel = this.response.globallist;
                    this.formModel.settingsId = this.response.globallist.id;
                    this.settingList.language_list = this.response.language;
                    this.formModel.language_id = this.response.language_list;
                    this.settingList.currency_list = this.response.currency;
                    this.formModel.currency_id = this.response.currency_list;
                    this.settingList.country_list = this.response.country;
                    this.formModel.country_id = this.response.country_list;
                    this.settingList.timezone = this.response.timezone;
                    this.formModel.timezone_id = this.response.globallist.timezone_id;
                    if (this.formModel.sms_check == 'Y') {
                        this.showSmsGateway = true;
                        this.formModel.sms_check = true;
                    } else {
                        this.showSmsGateway = false;
                        this.formModel.sms_check = false;
                    }
                    if (this.formModel.is_global_shipping_app == 1) {
                        this.showShipCharge = true;
                        this.formModel.is_global_shipping_app = true;
                    } else {
                        this.showShipCharge = false;
                        this.formModel.is_global_shipping_app = false;
                    }
                    if (this.formModel.algolia_search_status == 'y') {
                        this.showAlgolia = true;
                        this.formModel.algolia_search_status = true;
                    } else {
                        this.showAlgolia = false;
                        this.formModel.algolia_search_status = false;
                    }
                    
                    this.formModel.search_index = this.response.additional_settings.search_index;
                    this.formModel.search_url = this.response.additional_settings.search_url;
                    this.formModel.refund_auto_approve = this.response.additional_settings.refund_auto_approve;
                    this.formModel.default_refund_mode = this.response.additional_settings.default_refund_mode;

                    
                } else {
                    this.formModel.settingsId = 0;
                    this.settingList = this.response;
                    this.settingList.language_list = this.settingList.language;
                    this.settingList.currency_list = this.settingList.currency;
                    this.settingList.country_list = this.settingList.country;
                    this.formModel.refund_auto_approve = 'No';
                    this.formModel.default_refund_mode = 'Cash';
                    
                }
            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            },
            function() {
                //completed callback
            }
        );
    }
    toggleShipCharge() {
        this.showShipCharge = !this.showShipCharge;
    };
    toggleSmsGateway() {
        this.showSmsGateway = !this.showSmsGateway;
    };
    toggleAlgoliaSetting() {
        this.showAlgolia = !this.showAlgolia;
    };
    ngOnDestroy() {
        this.sub.unsubscribe();
    }
    addEditGlobalSettings(form: any) {
        this.errorMsg = '';
        let data: any = {};
        data = Object.assign({}, this.formModel)
        data.website_id = 1;
        data.country_id = this.formModel.country_id.join();
        data.language_id = this.formModel.language_id.join();
        data.currency_id = this.formModel.currency_id.join();
        data.timezone_id = this.formModel.timezone_id;
        if (this.ipaddress) {
            data.ip_address = this.ipaddress;
        } else {
            data.ip_address = "";
        }
        if (this.formModel.groupId < 1) {
            data.createdby = this._globalService.getUserId();
        }
        data.updatedby = this._globalService.getUserId();
        if (this.formModel.sms_check) {
            data.sms_check = 'Y';
        } else {
            data.sms_check = 'N';
        }
        if (this.formModel.is_global_shipping_app) {
            data.is_global_shipping_app = 1;
        } else {
            data.is_global_shipping_app = 0;
        }
        if (this.formModel.algolia_search_status) {
            data.algolia_search_status = 'y';
        } else {
            data.algolia_search_status = 'n';
        }
        data.additional_settings={
            'search_index':this.formModel.search_index,
            'search_url':this.formModel.search_url,
            'refund_auto_approve': this.formModel.refund_auto_approve,
            'default_refund_mode': this.formModel.default_refund_mode,
            'maximum_substitute_limit' : this.maximum_substitute_limit,
            'minimum_substitute_limit' : this.minimum_substitute_limit,
            'substitute_approval_time' : this.substitute_approval_time
        }

        console.log(data.additional_settings);
        
    
        this._globalSetupService.settingsAddEdit(data, this.formModel.settingsId).subscribe(
            data => {
                this.response = data;
                if (this.response.status == 1) {
                    this._router.navigate(['/globalsettings']);
                    this._globalService.deleteTab(this.tabIndex, this.parentId);
                } else {
                    this.errorMsg = this.response.message;
                }
            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            },
            function() {
                //completed callback
            }
        );
    }
}