import { Component, OnInit, OnDestroy, ViewChild } from '@angular/core';
import {
    Router, ActivatedRoute, NavigationEnd
}
from '@angular/router';
import {
    AutoResponderService
}
from './order.auto-responder.service';
import {
    GlobalService
}
from '../../global/service/app.global.service';
import {
    CookieService
}
from 'ngx-cookie';

import {
    AddEditTransition
}
from '../.././addedit.animation';@
Component({
    templateUrl: './templates/add_autoresponder.html',
    providers: [AutoResponderService],
    animations: [AddEditTransition],
    host: {
        '[@AddEditTransition]': ''
    },
})
export class AutoResponderAddEditComponent implements OnInit, OnDestroy {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    public shipping_list: any = {};
    public channel_list: any = {};
    public warehouse_list: any = {};
    public product_fields: any = [];
    public order_fields: any = [];
    public customer_fields: any = [];
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public ipaddress: any;
    public config: any;@
    ViewChild('editor') editor: any;
    constructor(private _autoResponderService: AutoResponderService, public _globalService: GlobalService, private _router: Router, private _route: ActivatedRoute, private _cookieService: CookieService, ) {
        this.ipaddress = _globalService.getCookie('ipaddress');
        this.config = {
            uiColor: '#ffffff',
            enterMode:1,
            allowedContent:true,
            toolbar: [{
                name: 'tools',
                items: ['Maximize']
            }, {
                name: 'clipboard',
                groups: ['clipboard', 'undo']
            }, {
                name: 'editing',
                groups: ['find', 'selection', 'spellchecker', 'editing']
            }, {
                name: 'links',
                groups: ['Link', 'Unlink', 'Anchor']
            }, {
                name: 'document',
                items: ['Source']
            }, {
                name: 'basicstyles',
                groups: ['basicstyles', 'cleanup'],
                items: ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'CopyFormatting', 'RemoveFormat']
            }, {
                name: 'paragraph',
                groups: ['list', 'indent', 'blocks', 'align', 'bidi'],
                items: ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl']
            }, {
                name: 'styles',
                items: ['Styles', 'Format', 'Font', 'FontSize']
            }, {
                name: 'colors',
                items: ['TextColor', 'BGColor']
            }, ]
        };
    }
    ngOnInit() {
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.sub = this._route.params.subscribe(params => {
            this.formModel.emailId = +params['id']; // (+) converts string 'id' to a number
        });
        this._autoResponderService.autoResponderLoad(this.formModel.emailId).subscribe(data => {
            this.response = data;
            if (this.formModel.emailId > 0) {
                this.formModel = this.response.data.api_status;
                this.formModel.emailId = this.response.data.api_status.id;
                this.shipping_list = this.response.data.shipping;
                this.channel_list = this.response.data.channels;
                this.warehouse_list = this.response.data.WarehouseMasters;
                this.product_fields = this.response.product_label;
                this.order_fields = this.response.order_label;
                this.customer_fields = this.response.customer_label;
                this.formModel.applicable_email_warehouse = this.response.data.selected_warehouse;
                this.formModel.applicable_email_channel = this.response.data.selected_channel;
                this.formModel.applicable_email_shipping_providers = this.response.data.selected_shippingprovider;
            } else {
            	this.formModel.emailId = 0;
                this.formModel.auto_responder_applied_for = 'Other';
                this.formModel.email_type = 'T';
                this.shipping_list = this.response.data.Shipping;
                this.channel_list = this.response.data.channels;
                this.warehouse_list = this.response.data.warehouse;
                this.product_fields = this.response.product_label;
                this.order_fields = this.response.order_label;
                this.customer_fields = this.response.customer_label;
            }
        }, err => {
            this._globalService.showToast('Something went wrong. Please try again.');
        }, function() {
            //completed callback
        });
    }
    ngOnDestroy() {
        this.sub.unsubscribe();
    }
    set_subject(field: string) {
        this.formModel.subject = (this.formModel.subject) ? (this.formModel.subject + field) : field;
    }
    set_template(type: string, field: string, val: number) {
        if (type == 'T') {
            this.formModel.email_content = (this.formModel.email_content) ? (this.formModel.email_content + field) : field;
        } else if (type == 'H') {
            this.editor.instance.insertHtml(field);
        } else {
            if (val == 1) { //text
                this.formModel.email_content_text = (this.formModel.email_content) ? (this.formModel.email_content + field) : field;
            } else { //editor
                this.editor.instance.insertHtml(field);
            }
        }
    }
    addEditEmailNotification(form: any) {
        this.errorMsg = '';
        var data: any = {};
        data = Object.assign({}, this.formModel);
        if (this.formModel.emailId < 1) {
            data.createdby = this._globalService.getUserId();
        }
        data.updatedby = this._globalService.getUserId();
        if (this.ipaddress) {
            data.ip_address = this.ipaddress;
        } else {
            data.ip_address = "";
        }
        data.website_id = 1;
        data.default_email_type_id = 1;
        data.emarketing_website_template_id = 1;
        data.emarketing_website_template_id = 1;
        data.description = this.formModel.name;
        if (!data.email_content) data.email_content = '';
        if (!data.email_content_text) data.email_content_text = '';
        if (this.formModel.auto_responder_applied_for == 'Order') {
            if (this.formModel.applicable_email_channel) data.channels = this.formModel.applicable_email_channel.join(',');
            else data.channels = '';
            if (this.formModel.applicable_email_warehouse) data.warehouse = this.formModel.applicable_email_warehouse.join(',');
            else data.warehouse = '';
            if (this.formModel.applicable_email_shipping_providers) data.shipping = this.formModel.applicable_email_shipping_providers.join(',');
            else data.shipping = '';
        } else {
            data.channels = '';
            data.warehouse = '';
            data.shipping = '';
        }
        this._autoResponderService.autoResponderAddEdit(data, this.formModel.emailId).subscribe(data => {
            this.response = data;
            if (this.response.status == 1) {
                this._router.navigate(['/emailnotification']);
                this._globalService.deleteTab(this.tabIndex, this.parentId);
            } else {
                this.errorMsg = this.response.message;
            }
        }, err => {
            this._globalService.showToast('Something went wrong. Please try again.');
        }, function() {
            //completed callback
        });
    }
}