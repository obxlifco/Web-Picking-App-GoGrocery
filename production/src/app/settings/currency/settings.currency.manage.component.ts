import {
    Component, OnInit, Inject, Optional
}
from '@angular/core';
import {
    MatDialogRef, MatDialog, MAT_DIALOG_DATA
}
from '@angular/material';
import {
    Router
}
from '@angular/router';
import {
    CurrencyService
}
from './settings.currency.service';
import {
    GlobalService
}
from '../../global/service/app.global.service';
@
Component({
    templateUrl: './templates/manage_currency.html',
    providers: [CurrencyService]
})
export class CurrencyManageComponent implements OnInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public currency_list: any;
    public formModel: any = {};
    public base_currency: any = [];
    public rate: any = [];
    public post_data: any = [];
    private sub: any;
    constructor(
        private _currencyService: CurrencyService,
        private _globalService: GlobalService,
        private _router: Router,
        private dialogRef: MatDialogRef < CurrencyManageComponent > ,
        public dialog: MatDialog, @Optional()@ Inject(MAT_DIALOG_DATA) public data: any
    ) {
        dialog.afterOpen.subscribe(() => {
            let containerElem: HTMLElement = < HTMLElement > document.getElementsByClassName('mat-dialog-container')[0];
            containerElem.classList.remove('pop-box-up');
        });
    }
    ngOnInit() {
        let that = this;
        this._currencyService.currencyLoad(0).subscribe(
            data => {
                this.response = data;
                this.currency_list = this.response.api_status;
                this.currency_list.forEach(function(item: any) {
                    if (item.isbasecurrency == 'y') {
                        that.base_currency = item;
                    }
                    that.rate[item.id] = item.exchange_rate;
                });
            },
            err => console.log(err),
            function() {
                //completed callback
            }
        );
    }
    sync() {
        let base_curr = this.base_currency.currency_code;
        let that = this;
        this._currencyService.syncCurr(this._globalService.getUserId()).subscribe(
            data => {
                this.response = data;
                this.currency_list = this.response.AllCurrencyRates;
                this.currency_list.forEach(function(item: any) {
                    if (item.isbasecurrency == 'y') {
                        that.base_currency = item;
                    }
                    that.rate[item.id] = item.exchange_rate;
                });
            },
            err => console.log(err),
            function() {
                //completed callback
            }
        );
    }
    manageCurrency(form: any) {
        this.errorMsg = '';
        let that = this;
        let data: any = {};
        this.currency_list.forEach(function(item: any) {
            let currency: any = {};
            currency.id = item.id;
            currency.engageboost_company_website_id = 1;
            currency.engageboost_currency_master_id = item.engageboost_currency_master_id;
            currency.currency_code = item.currency_code;
            currency.exchange_rate = that.rate[item.id];
            currency.isbasecurrency = item.isbasecurrency;
            currency.country_id = item.country_id;
            currency.createdby = that._globalService.getUserId();
            currency.updatedby = that._globalService.getUserId();
            that.post_data.push(currency);
        });
        data = {
            data: that.post_data
        };
        this._currencyService.currencyManage(data).subscribe(
            data => {
                this.response = data;
                if (this.response.status == 1) {
                    this.closeDialog();
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
    closeDialog() {
        this.dialogRef.close();
    }
}