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
  selector: 'google-login',	
  template: `<button mat-raised-button class="btn-block btn-google" id="googleBtn" type="button"><mat-icon class="icon-Google_plus"></mat-icon>Google</button>`,
  providers: [LoginService, Global],
})
export class GoogleLoginComponent implements AfterViewInit { 
	public ipaddress: any;
	public formModel: any = {};
	public GOOGLE_CLIENT_ID: string;
	public response : any;
	public errorMsg: string;
	public successMsg: string;
	constructor(@Inject(WINDOW) private window: Window, 
			private _loginService: LoginService, 
			private _router: Router, 
			private _cookieService:CookieService,
			private globalService: GlobalService,
			private _global: Global,
			private dialogsService: DialogsService
		) { 
		this.ipaddress = globalService.getCookie('ipaddress');
	}

	ngAfterViewInit(){
		this.googleInit();
	    setTimeout(() =>{ this.globalService.showLoaderSpinner(false); }, 3000);
	}
	/////////Google Plus login///////////
	  
	  public auth2: any;
	  public googleInit() {
	  	this.GOOGLE_CLIENT_ID = this.globalService.getGoogleClientId();
	  	let that = this;
	    gapi.load('auth2', ()=> {
	      that.auth2 = gapi.auth2.init({
	        client_id: this.GOOGLE_CLIENT_ID,
	        cookiepolicy: 'single_host_origin',
	        scope: 'profile email'
	      });
	      that.attachSignin(document.getElementById('googleBtn'));
	    });
	  }
	  public attachSignin(element:any) {
	  	let that = this;
	    this.auth2.attachClickHandler(element, {},
	      function (googleUser:any) {
	        let profile = googleUser.getBasicProfile();
	        var name = profile.getName();
	        var res = name.split(" ");
	        var firstname=res[0];
	        var lastname=res[1];
	        var email = profile.getEmail();
	        var guser={};
	        if(that.ipaddress){
				guser['ip_address']=that.ipaddress;
	        } else {
	        	guser['ip_address']='';
	        }
	        guser['first_name'] = firstname;
	        guser['last_name'] = lastname;
	        if(email){
	            guser['email'] = email;  
	        }else{
	            guser['email'] = '';  
	        }
	        guser['google_login_id'] = profile.getId();
	        guser['facebook_login_id'] = '';
	        guser['is_frontend'] = 1;  
	        guser['website_id'] = that.globalService.getFrontedWebsiteId();
			guser['company_id'] = that.globalService.getFrontedCompanyId();
	        that.globalService.showLoaderSpinner(true);
	        that._loginService.GoogleLogin(guser).subscribe(
	           	data => {
       				that.response = data;
       				//console.log(that.response);
       				if(that.response.status){
                   		let userData = {};
		       			userData['uid'] = that.response.user_id;
			            userData['first_name'] = that.response.first_name;
			            userData['last_name'] = that.response.last_name;
			            userData['email'] = that.response.email;
			            userData['isLoggedIn'] = true;
			            userData['auth_token'] = that.response.token;
			            userData['user_type'] = that.response.user_type;
			            userData['customer_id'] = that.response.customer_id;
			            userData['products'] = that.response.products;
			            userData['login_first'] = that.response.login_first;
			            userData['usd_exchange_rate'] = that.response.usd_exchange_rate;
		            	userData['role_id'] = that.response.role_id;
			            if(that.response.user_type==='merchant') {
			            	userData['distributor_type'] = that.response.distributor_data.distributor_type;
			            	userData['distributor_user_type'] = that.response.distributor_data.distributor_user_type;
			            	userData['default_warehouse_type'] = that.response.distributor_data.default_warehouse_type;	
			            	userData['website_id'] = that.response.distributor_data.website_id;
			            	userData['company_id'] = that.response.user_id;
			            	userData['currency_id'] = that.response.currency_id;
            				userData['currency'] = that.response.currency;
            				userData['business_name'] = that.response.distributor_data.business_name;
            				userData['moodle_password'] = that.response.learning_center_password;
			            } else if(that.response.user_type==='agent') { 
		            		userData['business_name'] = that.response.distributor_data.business_name;
						}

			            that._cookieService.putObject('clientData', userData, that.globalService.getCookieOption());
			            let after_login_redirect:string = that._cookieService.get('after_login_redirect');
			            
			            if(userData['role_id'] == 320 && guser['website_id'] != that.response.distributor_data.website_id) {
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
			            } else if(after_login_redirect){
							let is_facebook:any[] = after_login_redirect.split('?');
			            	if(is_facebook.length>1) {
			            		that._router.navigate([is_facebook[0]],{ queryParams: { isfacebook: 1} });	
			            	}else{
			            		that._router.navigate([after_login_redirect]);		
			            	}
							that._cookieService.remove('after_login_redirect');	            	
			            } else if(that.globalService.getFrontedWebsiteId() > 1){
							that._router.navigate(['/page/home']);
					    } else {
			            	//that._router.navigate(['/']);
			            	that._router.navigate(['/latest_products/']);
			            }
		       			that.globalService.isLoginSource.next(true);
		       	  	} else {
                       that.errorMsg = that.response.message;
                       that.globalService.showToast(that.errorMsg);
                   	}  
	           },
	           err => {
	           	that.globalService.showLoaderSpinner(false);
	           },
	           function(){
	                   //completed callback
	                   that.globalService.showLoaderSpinner(false);
	           }
	        );
	      }, function (error:any) {
	        //alert(JSON.stringify(error, undefined, 2));
	    });
	}
}	
