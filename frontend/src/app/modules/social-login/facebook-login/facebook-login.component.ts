import { Component, AfterViewInit, ViewChild, Inject } from '@angular/core';
import { Http } from '@angular/http';
import { MatAutocompleteTrigger, MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { LoginService } from '../../../global/service/app.login.service';
import { Router,ActivatedRoute,Params } from '@angular/router';
import { CookieService} from 'ngx-cookie';
import { GlobalVariable, Global } from '../../../global/service/global';
import { GlobalService } from '../../../global/service/app.global.service';
import { FacebookService, LoginResponse, LoginOptions, InitParams } from 'ngx-facebook';
import { DialogsService} from '../../../global/dialog/confirm-dialog.service';
import { WINDOW } from '@ng-toolkit/universal';
declare const gapi: any;
@Component({
  selector: 'facebook-login',	
  template: `<button mat-raised-button class="btn-block btn-fb" type="button" (click)="loginWithFb()"><mat-icon class="icon-facebook-logo"></mat-icon>Facebook</button>`,
  providers: [LoginService, Global],
})

export class FacebookLoginComponent {
	public ipaddress: any;
	public formModel: any = {};
	public FACEBOOK_APP_ID:string;
	public response : any;
	public errorMsg: string;
	public successMsg: string;
	constructor(@Inject(WINDOW) private window: Window, 
		private _loginService: LoginService, 
		private _router: Router, 
		private _cookieService:CookieService,
		private globalService: GlobalService,
		private _global: Global,
		private fb: FacebookService,
		private dialogsService: DialogsService
	) {
		this.FACEBOOK_APP_ID = this.globalService.getFBAppId();
		this.ipaddress = globalService.getCookie('ipaddress');	
		let initParams: InitParams = {
	      appId: this.FACEBOOK_APP_ID,
	      xfbml: true,
	      version: 'v2.11'
	    };
	    fb.init(initParams);
	}

	loginWithFb(){
		const loginOptions: LoginOptions = {
	      enable_profile_selector: true,
	      return_scopes: true,
	      scope: 'public_profile,email'
	    };

	    this.fb.login(loginOptions)
	      .then((res: LoginResponse) => {
	        this.getProfile();
	      })
	      .catch(this.handleError);
	}	

	/**
	* Get the user's profile
	*/
	getProfile() {
	    this.fb.api('/me?fields=id,name,first_name,last_name,gender,email')
	      .then((res: any) => {
	        let fuser:any={};
	        if(this.ipaddress){
				fuser['ip_address']=this.ipaddress;
	        } else {
	        	fuser['ip_address']='';
	        }
	        
	        fuser['first_name'] = res.first_name;
	        fuser['last_name'] = res.last_name;
	        if(res.email){
	            fuser['email'] = res.email;  
	        }else{
	            fuser['email'] = '';  
	        }
	        fuser['google_login_id'] = '';
	        fuser['facebook_login_id'] = res.id;
	        fuser['is_frontend'] = 1;  
	        fuser['website_id'] = this.globalService.getFrontedWebsiteId();
			fuser['company_id'] = this.globalService.getFrontedCompanyId();
	        this.globalService.showLoaderSpinner(true);
	        this._loginService.GoogleLogin(fuser).subscribe(
	           	data => {
           				this.response = data;
           				//console.log(this.response);
	                   	if(this.response.status) {
	                   		let userData = {};
	                		userData['uid'] = this.response.user_id;
				            userData['first_name'] = this.response.first_name;
				            userData['last_name'] = this.response.last_name;
				            userData['email'] = this.response.email;
				            userData['isLoggedIn'] = true;
				            userData['auth_token'] = this.response.token;
				            userData['user_type'] = this.response.user_type;
				            userData['customer_id'] = this.response.customer_id;
				            userData['products'] = this.response.products;
				            userData['login_first'] = this.response.login_first;
				            userData['usd_exchange_rate'] = this.response.usd_exchange_rate;
		            		userData['role_id'] = this.response.role_id;
				            if(this.response.user_type==='merchant'){
				            	userData['distributor_type'] = this.response.distributor_data.distributor_type;
				            	userData['distributor_user_type'] = this.response.distributor_data.distributor_user_type;	
				            	userData['default_warehouse_type'] = this.response.distributor_data.default_warehouse_type;
				            	userData['website_id'] = this.response.distributor_data.website_id;
				            	userData['company_id'] = this.response.user_id;
				            	userData['currency_id'] = this.response.currency_id;
	            				userData['currency'] = this.response.currency;
	            				userData['business_name'] = this.response.distributor_data.business_name;
	            				userData['moodle_password'] = this.response.learning_center_password;
				            } else if(this.response.user_type==='agent') { 
			            		userData['business_name'] = this.response.distributor_data.business_name;
							}
				            this._cookieService.putObject('clientData', userData, this.globalService.getCookieOption());
				            let after_login_redirect:string = this._cookieService.get('after_login_redirect');

				            if(userData['role_id'] == 320 && fuser['website_id'] != this.response.distributor_data.website_id) {
				            	let dstore: any = '';
					            dstore = userData['business_name'].toLowerCase();
				            	let parser = document.createElement('a');
								parser.href = GlobalVariable.COMPANY_URL;
								let store_url = '';
								if(this.window.location.hostname == 'localhost' || this.window.location.hostname == 'staging.barawkat.com') {
						          	store_url = GlobalVariable.BASE_URL;
							        store_url = store_url + 'page/home?dstore='+ dstore;
								    this.window.location.href = store_url
						        } else {
						            store_url = parser.protocol +'//'+ dstore +'.'+this.window.location.hostname+'/';
							        store_url = store_url + 'page/home'
								}
						        this.window.location.href = store_url
			            	} else if(after_login_redirect) {
								let is_facebook:any[] = after_login_redirect.split('?');
				            	if(is_facebook.length>1){
				            		this._router.navigate([is_facebook[0]],{ queryParams: { isfacebook: 1} });	
				            	} else {
				            		this._router.navigate([after_login_redirect]);		
				            	}
								this._cookieService.remove('after_login_redirect');	            	
				            } else if(this.globalService.getFrontedWebsiteId() > 1) { 
				            	this._router.navigate(['/page/home']);	
				            } else {
				            	//this._router.navigate(['/']);
				            	this._router.navigate(['/latest_products/']);
				            }				       			
			       			this.globalService.isLoginSource.next(true);
			       	  	} else {	                       
	                       this.errorMsg = this.response.message;
	                       this.globalService.showToast(this.errorMsg);
	                   	}

	                   	this.globalService.showLoaderSpinner(false);
	           },
	           err => {
	           	this.globalService.showLoaderSpinner(false);
	           },
	           function() {
	                   //completed callback         
	           }
	        );
	      })
	      .catch(this.handleError);
	}
  	/**
   	* This is a convenience method for the sake of this example project.
   	* Do not use this in production, it's better to handle errors separately.
   	* @param error
   	*/
	private handleError(error) {
		console.error('Error processing action', error);
	}
}
