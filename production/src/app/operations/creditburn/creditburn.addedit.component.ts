import {Component, ElementRef, OnInit, Input, Inject, AfterViewInit, Optional } from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { Global } from '../../global/service/global';
import { Router, ActivatedRoute,NavigationEnd } from '@angular/router';
import { AddEditTransition, AddEditStepFlipTransition } from '../.././addedit.animation';

@Component({
    selector: 'app-creditburn.addedit',
    templateUrl: 'templates/creditburn.addedit.component.html',
    animations: [AddEditTransition],
    styleUrls: [],
    host: {
        '[@AddEditTransition]': ''
    },
})
export class CreditburnAddeditComponent implements OnInit {
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
	public add_edit:any;

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
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        
        this.sub = this._route.params.subscribe(params => {
            this.formModel.formId = +params['id']; // (+) converts string 'id' to a number
        });

        if(this.formModel.formId){
	        this._cookieService.putObject('credit_point_edit', this.formModel.formId);
	        this._cookieService.putObject('action','edit');
	        this.add_edit='edit';
	    }else{  
	        this._cookieService.putObject('action','add');
            this.add_edit='add';
            this.formModel.redeem_amount_type='percentage';
            this.formModel.redeem_type='loyalty';
        }
        if (this.formModel.formId > 0) {
            this.global.getWebServiceData('loyalty','GET','',this.formModel.formId).subscribe(res => {
                if(res.status==1){
                    let data=res.api_status;
                    this.formModel.name = data.name;
                    this.formModel.loyalty_desc = data.loyalty_desc;
                    if(data.is_redeem_limited=='n'){
                        this.formModel.is_redeem_limited = false;
                    }else{
                        this.formModel.is_redeem_limited = true;
                    }
                    this.formModel.redeem_limit = data.redeem_limit;
                    this.formModel.redeem_amount_type = data.redeem_amount_type;
                    this.formModel.redeem_type = data.redeem_type;
                    this.formModel.points = data.points;

                } else {
                    this._globalService.showToast('Something went wrong. Please try again.'); 
                }
                
            }, err => {
                console.log(err)
            })
        }
    }
    addEdit(form: any) {
        setTimeout(() => {
            this._globalService.showLoaderSpinner(true);
        });
        let data: any = {};
        let is_redeem_limited='n';
        data.website_id = this._globalService.getWebsiteId();
        data.name=this.formModel.name;
        data.loyalty_desc=this.formModel.loyalty_desc;
        if(this.formModel.is_redeem_limited){
            is_redeem_limited='y';
            data.redeem_limit=this.formModel.redeem_limit;
        }
        data.is_redeem_limited=is_redeem_limited;
        data.redeem_amount_type=this.formModel.redeem_amount_type;
        data.redeem_type=this.formModel.redeem_type;
        data.points = this.formModel.points;
        data.loyal_type="burn";
        if (this.formModel.formId > 0) {
            data.id = this.formModel.formId;
        }
        data={"value":data};
        
        this.global.getWebServiceData('loyalty','POST',data,'').subscribe(
            data => {
                this.response = data;
                this._globalService.showLoaderSpinner(false);
                
                if(data.status==1){
                    
                    if(this.add_edit=='add'){
                        this._cookieService.putObject('credit_point_add', data.api_status.id);
                        this.add_edit='add';
                        this._router.navigate(['/credit_points_burn/conditions/'+data.api_status.id]);  	
                    }else{
                        
                        this._router.navigate(['/credit_points_burn/conditions/edit/'+this.formModel.formId]);
                    }
                
                }else{
                
                    this.errorMsg = this.response.message;
                }
            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            },
            function(){
                //completed callback
            }
        );
    }

}