import {Component, ElementRef, OnInit, Input, Inject, AfterViewInit, Optional } from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { Global } from '../../global/service/global';
import { Router, ActivatedRoute } from '@angular/router';
import { AddEditTransition, AddEditStepFlipTransition } from '../.././addedit.animation';

@Component({
    selector: 'app-price.addedit',
    templateUrl: 'templates/price.addedit.component.html',
    animations: [AddEditTransition],
    host: {
        '[@AddEditTransition]': ''
    },
})

export class PriceAddeditComponent implements OnInit {
    public ipaddress: any;
    public errorMsg: string;
    public response: any;
    public successMsg: string;
    public rolelist: any;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public userId: any;

    constructor(
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

        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.sub = this._route.params.subscribe(params => {
            this.formModel.formId = +params['id']; // (+) converts string 'id' to a number
        });
        if (this.formModel.formId > 0) {
            this.global.getWebServiceData('price_formula-details','GET','',this.formModel.formId).subscribe(Response => {
                console.log(Response)
                let data=Response.data[0];
                this.formModel.formula_name = data.formulla_name;
                this.formModel.based_on = data.price_name;
                this.formModel.condition_type = data.condition;
                this.formModel.margin = data.margin;
                this.formModel.formula_for = data.formulla_type;
            }, err => {
                console.log(err)
            })
        } else {
            this.formModel.formula_for='customer';
        }
    }

    addEditPriceFormula(form: any) {
        setTimeout(() => {
            this._globalService.showLoaderSpinner(false);
        });
        let data: any = {};
        data.website_id = this._globalService.getWebsiteId();
        data.formula_name = this.formModel.formula_name;
        data.price_name = this.formModel.based_on;
        data.condition_type = this.formModel.condition_type;
        data.margin = this.formModel.margin;
        data.formula_type = this.formModel.formula_for;
       
        if (this.formModel.formId > 0) {
            data.id = this.formModel.formId;
        }
        this.global.getWebServiceData('price_formula','POST',data,'').subscribe(res => {  
            console.log(res);   
            if (res['status'] == '1') { // success response 
                this._globalService.showToast(res['Message']);
                this._router.navigate(['/price_formula/']);
            } else {
                this._globalService.showToast(res['Message']);
            }
            setTimeout(() => {
                this._globalService.showLoaderSpinner(false);
            });
        }, err => {

        })
    }

}