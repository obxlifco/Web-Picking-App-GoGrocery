import {Component, ElementRef, OnInit, Input, Inject, AfterViewInit, Optional } from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { Global } from '../../global/service/global';
import { Router, ActivatedRoute } from '@angular/router';
import { AddEditTransition, AddEditStepFlipTransition } from '../.././addedit.animation';
@Component({
    selector: 'app-customertax.addedit',
    templateUrl: 'templates/customertax.addedit.html',
    animations: [AddEditTransition],
    host: {
        '[@AddEditTransition]': ''
    },
    providers: []
})

export class CustomertaxAddeditComponent implements OnInit {
    public ipaddress: any;
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public userId: any;
    public customer_group_list: any;
    constructor(
        public _globalService: GlobalService,
        private global: Global,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService,
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
            this.global.getWebServiceData('view_customertaxclass','GET','',this.formModel.formId).subscribe(Response => {
                let data=Response.api_status;
                this.formModel.name = data.tax_class_name;
                this.formModel.customer_type = data.customer_type;
            }, err => {
                console.log(err)
            })
        }
        this.getCustomerGroupList();
    }

    addEditPriceFormula(form: any) {
        setTimeout(() => {
            this._globalService.showLoaderSpinner(false);
        });
        let data: any = {};
        data.website_id = this._globalService.getWebsiteId();
        data.tax_class_name = this.formModel.name;
        data.customer_type = this.formModel.customer_type;
        if (this.formModel.formId > 0) {
            data.id = this.formModel.formId;
        }
        data={"value":data};
        console.log(data)
        this.global.getWebServiceData('customertaxclass','POST',data,'').subscribe(res => { 
            if (res['status'] == '1') { // success response 
                this._globalService.showToast(res['message']);
                this._router.navigate(['/customer_tax_class/']);
            } else {
                this._globalService.showToast(res['message']);
            }
            setTimeout(() => {
                this._globalService.showLoaderSpinner(false);
            });
        }, err => {

        })
    }

    getCustomerGroupList() {
        let data = {
            "model": "EngageboostCustomerGroup",
            "screen_name": "list",
            "userid": this.userId,
            "search": "",
            "order_by": "name",
            "order_type": "+",
            "status": "",
            "website_id": this._globalService.getWebsiteId(),
          };
        this.global.getWebServiceData('global_list','POST',data,'').subscribe(data => {
            this.customer_group_list = data.results[0].result; // list of customer list
        }, err => {}, function() { // call back function when exection is done
        })
    }
}