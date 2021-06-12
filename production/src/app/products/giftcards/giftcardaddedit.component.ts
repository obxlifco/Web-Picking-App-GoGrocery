import {Component, ElementRef, OnInit, Input, Inject, AfterViewInit, Optional } from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { Global } from '../../global/service/global';
import { Router, ActivatedRoute } from '@angular/router';
import { AddEditTransition } from '../.././addedit.animation';
import * as _moment from 'moment';
import { DateTimeAdapter, OWL_DATE_TIME_FORMATS, OWL_DATE_TIME_LOCALE } from 'ng-pick-datetime';
import { MomentDateTimeAdapter } from 'ng-pick-datetime-moment';
const moment = (_moment as any).default ? (_moment as any).default : _moment;

export const MY_CUSTOM_FORMATS = {
    parseInput: 'LL LT',
    fullPickerInput: 'LL LT',
    datePickerInput: 'LL',
    timePickerInput: 'LT',
    monthYearLabel: 'MMM YYYY',
    dateA11yLabel: 'LL',
    monthYearA11yLabel: 'MMMM YYYY',
};
@Component({
  selector: 'app-giftcardaddedit',
  templateUrl: './templates/giftcardaddedit.component.html',
  styleUrls: ['./templates/giftcardaddedit.component.css'],
  animations: [AddEditTransition],
    host: {
        '[@AddEditTransition]': ''
    },
    providers: [
        // {provide: DateTimeAdapter, useClass: MomentDateTimeAdapter, deps: [OWL_DATE_TIME_LOCALE]},

        // {provide: OWL_DATE_TIME_FORMATS, useValue: MY_CUSTOM_FORMATS},
        // {provide: DateTimeAdapter, useClass: MomentDateTimeAdapter, deps: [OWL_DATE_TIME_LOCALE]},

        // {provide: OWL_DATE_TIME_FORMATS, useValue: MY_CUSTOM_FORMATS},
    ]
})
export class GiftcardaddeditComponent implements OnInit {
    
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
    public method:string;
    public post_url;
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
            this.global.getWebServiceData('giftcards','GET','',this.formModel.formId).subscribe(Response => {
                let data=Response.api_status;
                this.formModel.card_name = data.card_name;
                this.formModel.card_number = data.card_number;
                this.formModel.start_date = data.start_date;
                this.formModel.end_date = data.end_date;
                this.formModel.amount = data.amount;
            }, err => {
                console.log(err)
            })
        }else{
            this.formModel.formId      = '0';
            this.formModel.coupon_type = '1';
        }
    }

    generateCode(type: string) {	
        if (type == 'single') { //single code
			this.formModel.coupon_code = this.randomCode();
		} else { // multiple code
			if (this.formModel.number_of_coupon > 0) {
				if (this.formModel.coupon_codes == '') {
					if (!this.formModel.coupon_codes) {
						this.formModel.coupon_codes = [];
					}
					for (var i = 0; i < this.formModel.number_of_coupon; i++) {
						this.formModel.coupon_codes.push({ coupon_code: this.randomCode(), is_used: 'n' });
					}
				} else {
					this.formModel.coupon_codes = [];
					for (var i = 0; i < this.formModel.number_of_coupon; i++) {
						this.formModel.coupon_codes.push({ coupon_code: this.randomCode(), is_used: 'n' });
					}
				}
			} else {
				this._globalService.showToast('Number of coupon must be greater than 0');
			}
		}	
    }
    randomCode() {
        var text = "";
        var ts=Date.now();
		var charset = "0123456789"+ts;
		for (var i = 0; i < 12; i++)
			text += charset.charAt(Math.floor(Math.random() * charset.length));
        // console.log(text);
		return text;
	}

    addEdit() {

        setTimeout(() => {
            this._globalService.showLoaderSpinner(false);
        });
        let data: any = {};
        data.website_id     = this._globalService.getWebsiteId();
        data.card_name      = this.formModel.card_name;
        data.card_number    = this.formModel.card_number;
        data.start_date     = this.formModel.start_date;
        data.end_date       = this.formModel.end_date;
        data.amount         = this.formModel.amount;
        data.coupon_code    = this.formModel.coupon_codes;
        if (this.formModel.formId > 0) {
            data.id = this.formModel.formId;
            this.method='PUT';
            this.post_url='giftcards/'+this.formModel.formId;
        }else{
            this.method='POST';
            this.post_url='giftcards';
        }
        console.log(data)
        this.global.getWebServiceData(this.post_url,this.method,data,'').subscribe(res => { 
            if (res['status'] == '1') { // success response 
                this._globalService.showToast(res['message']);
                this._router.navigate(['/gift_cards/']);
            } else {
                this._globalService.showToast(res['message']);
            }
            setTimeout(() => {
                this._globalService.showLoaderSpinner(false);
            });
        }, err => {

        })
    }

}