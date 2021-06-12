import { Component, AfterViewInit, ViewChild, Inject,OnInit} from '@angular/core';
import { Http } from '@angular/http';
import { MatAutocompleteTrigger,MatDialog,MatDialogRef,MAT_DIALOG_DATA } from '@angular/material';
import { LoginService } from '../../global/service/app.login.service';
import { Router,ActivatedRoute,Params } from '@angular/router';
import { CookieService} from 'ngx-cookie';
import { GlobalVariable, Global } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';
import { FacebookService, LoginResponse, LoginOptions, InitParams } from 'ngx-facebook';
import { DialogsService} from '../../global/dialog/confirm-dialog.service';
declare const gapi: any;
import {trigger, stagger, animate, style, group, query, transition, keyframes} from '@angular/animations';
import { FormBuilder, FormGroup } from '@angular/forms';
import { WINDOW } from '@ng-toolkit/universal';
import { TranslateService } from '@ngx-translate/core';
// export const query = (s:any,a:any,o={optional:true})=>q(s,a,o);
export const loginTransition = trigger('loginTransition', [
  transition(':enter', [
    query('.login-box', style({ opacity: 0 })),
    query('.login-box', stagger(300, [
      style({ transform: 'translate(0%,10%)' }),
      animate('1s cubic-bezier(.75,-0.48,.26,1.52)', style({transform: 'translate(0%,0%)', opacity: 1})),
    ])),
  ]),
  transition(':leave', [
    query('.login-box', stagger(300, [
      style({ transform: 'translate(0%,0%)', opacity: 1,display:'block'}),
      animate('.1s cubic-bezier(.75,-0.48,.26,1.52)', style({transform: 'translate(0%,0%)', opacity: 0, display:'none'})),
    ])),        
  ])
]);

@Component({
  selector: 'app-login',

  templateUrl: './templates/login.html',
  styleUrls: ['./login.component.css'],
  providers: [LoginService,Global],
  animations: [ loginTransition ],
  host: {
    '[@loginTransition]': ''
  }
})

export class LoginComponent { 
	public hide:boolean = false;
	public ipaddress: any;
	public response : any;
	public errorMsg: string;
	public successMsg: string;
	public company_name:string = '';	
	public facebookStore:boolean = false;
	public globalData: any = {};
	public follow_unfollow:string = 'Follow';
	public signupWindow = true;
	public otpWindow = false;
	public clickCounter: number = 0;
	public isDisabled: boolean = true;
	public otpValue: string;
	public userDataCookie: any = {};
	private formBuilder: FormBuilder;
	private dialogRef: MatDialogRef<LoginComponent>;
	@Inject(MAT_DIALOG_DATA) public data: any;
	constructor(@Inject(WINDOW) private window: Window, 	
		private _loginService: LoginService, 
		private _router: Router, 
		private _cookieService:CookieService,
		public globalService: GlobalService, 
		private _global: Global,
		public dialog: MatDialog,
		private dialogsService: DialogsService,
		private translate : TranslateService,

		) { 

		this.translate.setDefaultLang('en');
		this.ipaddress = globalService.getCookie('ipaddress');
		this.company_name = globalService.getFrontedCompanyName();
		let facebook_store = +this._cookieService.get('facebookStore');
  		if(facebook_store && facebook_store == 1){
  			this.facebookStore = true;
  		} else{
  			this.facebookStore = false;
  			this._cookieService.remove('facebookStore');
  		}
  		//console.log(this.facebookStore);
  		this.globalData = this._cookieService.getObject('globalData');
	}

	check_login(formModel:any) {
		var userloginData ={};
		userloginData=formModel;
		if(this.ipaddress){
			userloginData['ip_address']=this.ipaddress;
		}else{
			userloginData['ip_address']='';
		}
		userloginData['website_id'] = this.globalService.getFrontedWebsiteId();
		userloginData['company_id'] = this.globalService.getFrontedCompanyId();
		userloginData['is_frontend'] = 1;
		this.dialogRef.close();
		console.log(`${userloginData}`);
		this.globalService.showLoaderSpinner(true);
	    let that=this;
		this._loginService.doLogin(userloginData).subscribe(
	       	data => {
	       		this.response = data;
	       		//console.log(this.response);
	       		if(this.response.status) {
	       			var userData = {};
	       			userData['uid'] = this.response.user_id;
		            userData['first_name'] = this.response.first_name;
		            userData['last_name'] = this.response.last_name;
		            userData['email'] = this.response.email;
		            userData['isLoggedIn'] = true;
		            userData['keepLoggedIn'] = formModel.keep_login;
		            userData['auth_token'] = this.response.token;
		            userData['user_type'] = this.response.user_type;
		            userData['customer_id'] = this.response.customer_id;
		            userData['products'] = this.response.products;
		            userData['login_first'] = this.response.login_first;
		            userData['usd_exchange_rate'] = this.response.usd_exchange_rate;
		            userData['role_id'] = this.response.role_id;
		            if(this.response.user_type==='merchant') {
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
						userData['comp_website_id'] = this.response.website_id;
				    	userData['dist_website_id'] = this.response.distributor_data.website_id;
		            }
		            
		            if(this.response.email_verification == 'n') { // If email is not verified
		            	this.userDataCookie = userData;
		            	this.signupWindow = false;
                    	this.otpWindow = true;
                    	this.errorMsg = '';
		            } else {
		            	this._cookieService.putObject('clientData', userData, this.globalService.getCookieOption());
		            	// for distributor store...
		            	if(userloginData['website_id'] > 1) {
		            		//this.countFollowers(); // follow and unfollow	
		            	}
			            let after_login_redirect:string = this._cookieService.get('after_login_redirect');
			            if(userData['role_id'] == 320 && this.response.website_id != this.response.distributor_data.website_id) {
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
			            	if(this.facebookStore && is_facebook.length > 1){
			            		this._router.navigate([is_facebook[0]],{ queryParams: { isfacebook: 1} });	
			            	}else{
			            		this._router.navigate([after_login_redirect]);
			            	}
							
							this._cookieService.remove('after_login_redirect');	            	
			            } else if(this.globalService.getFrontedWebsiteId() > 1){
							this._router.navigate(['/page/home']);
					    } else {
			            	//this._router.navigate(['/']);
			            	this._router.navigate(['/latest_products/']);
			            }
						this.globalService.isLoginSource.next(true);
		            }
	       		} else {
	       			this.errorMsg = this.response.message;
	       		}
	       	},
	       	err => {
	       		this.globalService.showLoaderSpinner(false);
	       		this.errorMsg = "Something went wrong. Please try again."
	       	},
	       	function(){
	       		that.globalService.showLoaderSpinner(false);
	       		//completed callback
	       	}
	    );
	}

	/*#################  OTP resend ##################*/
	otpResend(userType:number) {
		this.clickCounter += 1;
		if(this.clickCounter == 5){
          this.isDisabled = false;
          this.errorMsg = "You have reached the maximum limit (5)";
       } else if(this.clickCounter > 5){
          this.errorMsg = "Sorry! You have crossed the limit (5 times)";
          return;
		}
	    this.globalService.showLoaderSpinner(true);
		let that=this;
		var otpData ={};
		//var userData = that._cookieService.getObject('clientData');
		//otpData['email'] = userData['email'];
		otpData['email'] = this.userDataCookie['email'];
		otpData['is_frontend'] = userType;
		this._global.signupOtpResend(otpData).subscribe(
	       	data => {
	       		this.response = data;
	       		let cookie_options:any = {};
		        cookie_options.path = '/';
	       		if(this.response.status){
	       			this.successMsg = "OTP has been resent to your email.";
	       			this.window.scrollTo(0, 0);					
	       		} else {
	       			this.errorMsg = this.response.message;
	       			this.window.scrollTo(0, 0);
	       		}
	       	},
	       	err => {
	       		this.globalService.showLoaderSpinner(false);
	       		this.errorMsg = "Something went wrong. Please try again."
	       		this.window.scrollTo(0, 0);
	       	},
	       	function(){
	       		that.globalService.showLoaderSpinner(false);
	       		//completed callback
	       	}
	    );
	}
   /*################# User Signup Otp Verification ##################*/
	otpVerification(userType: number){  
	    this.globalService.showLoaderSpinner(true);
	    let that=this;
		var otpData ={};
		//var userData = that._cookieService.getObject('clientData'); 
		//otpData['website_id'] = userData['website_id'];
		otpData['email'] = this.userDataCookie['email'];
		otpData['is_frontend'] = userType;
		otpData['verification_code'] = this.otpValue;
		this.successMsg = '';
		this._global.signupOtpCheck(otpData).subscribe(
	       	data => {
	       		this.response = data;
	       		let cookie_options:any = {};
		        cookie_options.path = '/';
	       		if(this.response.status) {
	       			this._cookieService.putObject('clientData', this.userDataCookie, this.globalService.getCookieOption());
	       			if(this.globalService.getFrontedWebsiteId() > 1) {
	       				//this.countFollowers(); // follow and unfollow	
	       			}
		            let after_login_redirect:string = this._cookieService.get('after_login_redirect');
		            if(this.userDataCookie['role_id'] == 320 && this.userDataCookie['comp_website_id'] != this.userDataCookie['dist_website_id']) {
		            	let dstore: any = '';
			            dstore = this.userDataCookie['business_name'].toLowerCase();
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
		            	if(this.facebookStore && is_facebook.length > 1){
		            		this._router.navigate([is_facebook[0]],{ queryParams: { isfacebook: 1} });	
		            	} else {
		            		this._router.navigate([after_login_redirect]);
		            	}
						this._cookieService.remove('after_login_redirect');	            	
		            } else if(this.globalService.getFrontedWebsiteId() > 1){
						this._router.navigate(['/page/home']);
				    } else {
		            	//this._router.navigate(['/']);
		            	this._router.navigate(['/latest_products/']);
		            }
					this.globalService.isLoginSource.next(true);
				}else{
	       			this.errorMsg = this.response.message;
	       			this.window.scrollTo(0, 0);
	       		}
	       	},
	       	err => {
	       		this.globalService.showLoaderSpinner(false);
	       		this.errorMsg = "Something went wrong. Please try again."
	       		this.window.scrollTo(0, 0);
	       	},
	       	function(){
	       		that.globalService.showLoaderSpinner(false);
	       		//completed callback
	       	}
	    );
	}
	countFollowers() {
		let data:any = { user_id:this.globalService.getClientId(), company_website_id:this.globalService.getFrontedWebsiteId() };
		this._global.countFollowers(data).subscribe(
	        data => {
	    		if(data.status) {
	    			if(data.activity_status == 'subscribed') {
	    				this.follow_unfollow = 'Unfollow';
					} else {
	    				this.follow_unfollow = 'Follow';
					}
	    			this.setFollowers(this.follow_unfollow)
				}
	        },
	        err => {},
	        function(){
	            //completed callback
	        }
	    );
	}
	
	setFollowers(follow_unfollow:any) {
		this.globalData['follow_unfollow'] = follow_unfollow;
		this._cookieService.putObject('globalData',this.globalData, this.globalService.getCookieOption());
		this.globalService.isFollowSource.next(follow_unfollow);
	}
	// form: FormGroup;
	// ngOnInit() {
	// 	this.form = this.formBuilder.group({
	// 	  filename: ''
	// 	})
	//   }
	
	  submit(form) {
		// this.dialogRef.close(`${form.value.filename}`);
	  }
}
