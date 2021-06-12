import { Component, AfterViewInit } from '@angular/core';
import { Http } from '@angular/http';
import { LoginService } from './app.login.service';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie';
import { GlobalVariable } from '../global/service/global';
import { GlobalService } from '../global/service/app.global.service';
declare const gapi: any;
import * as Crypto from 'crypto-js';
import {trigger, stagger, animate, style, group, query, transition, keyframes} from '@angular/animations';
// export const query = (s:any,a:any,o={optional:true})=>q(s,a,o);
export const loginTransition = trigger('loginTransition', [
	transition(':enter', [
		query('.login-box', style({ opacity: 0 })),
		query('.login-box', stagger(300, [
		  style({ transform: 'translate(-50%,-40%)' }),
		  animate('1s cubic-bezier(.75,-0.48,.26,1.52)', style({transform: 'translate(-50%,-50%)', opacity: 1})),
		])),
	]),
	transition(':leave', [
		query('.login-box', stagger(300, [
		  style({ transform: 'translate(-50%,-50%)', opacity: 1 }),
		  animate('.8s cubic-bezier(.75,-0.48,.26,1.52)', style({transform: 'translate(-50%,-70%)', opacity: 0})),
		])),        
	])
]);

@Component({
	templateUrl: './templates/login.html',
	providers: [LoginService],
	animations: [ loginTransition ],
	host: {
		'[@loginTransition]': ''
	}
})

export class LoginComponent implements AfterViewInit {
	constructor(
		private _loginService: LoginService, 
		private _router: Router,
		private _cookieService:CookieService,
		private globalService: GlobalService
	) { 
		this.ipaddress = globalService.getCookie('ipaddress');
	}
	public response : any;
	public errorMsg: string;
	public successMsg: string;
	public ipaddress: any;
	public otpField: boolean =false;
	public otpBtn: boolean =false;
	public passwordType: string = 'password';
	public showLoader: boolean = false;
	detectMobile(val:string) {
		var regex = /^[0-9]{10}$/;
		if(regex.test(val)){
	        this.otpBtn = true;
	    } else {
	        this.otpBtn = false;
	    }
	}

	showPassword() {
		if(this.passwordType=='password'){
			this.passwordType = 'text';
		} else {
			this.passwordType = 'password';
		}
	}
	
	check_login(formModel:any) {
		var userloginData ={};
		userloginData=formModel;
		if(this.ipaddress) {
			userloginData['ip_address']=this.ipaddress;
		}  else {
			userloginData['ip_address']='';
		}
		this.showLoader = true;
	    let that=this;
		this._loginService.doLogin(userloginData).subscribe(
	       	data => {
				   this.response = data;
	       		if(this.response.status) {
	       			var userData = {};
	       			userData['uid'] = this.response.user_id;
		            userData['first_name'] = this.response.first_name;
		            userData['last_name'] = this.response.last_name;
		            userData['email'] = formModel.username;
		            // userData['password'] = formModel.password;
		            // userData['is_otp'] = false;
		            userData['isLoggedIn'] = true;
		            // userData['keepLoggedIn'] = formModel.keep_login;
		            userData['auth_token'] = this.response.token;
					userData['user_type'] = this.response.designation;
					userData['company_id'] = this.response.company_id;
					userData['isManager'] = this.response.managerType;
					userData['isSuperAdmin'] = this.response.isSuperAdmin;
					//New Added
					userData['isSubAdmin'] = this.response.isSubAdmin;
                    userData['website_id'] = this.response.website_id;
                    if(this.response.warehouse_id && this.response.warehouse_id > 0){
                        userData['warehouse_id'] = this.response.warehouse_id;
                    }else{
                        userData['warehouse_id'] = "";
                    }
					/////////  currency setting data .............
					userData['currencyId'] = this.response.currencyId;
					userData['currencyCode'] = this.response.currencyCode;
					userData['currencysymbol'] = this.response.currencysymbol;

					/////////  ELASTIC SETTING DATA//////////////////////
					userData['elastic_host'] = this.response.elastic_host;
					userData['elastic_store_name'] = this.response.elastic_store_name;
					userData['elastic_port'] = this.response.elastic_port;
					userData['elastic_url'] = this.response.elastic_url;
					
					// global setting data...
					userData['gl_date_format'] = this.response.gl_date_format;
					userData['gl_timezone_id'] = this.response.gl_timezone_id;
					userData['applicable_tax'] = this.response.applicable_tax;
							
		            this._cookieService.putObject('userData', userData);
		            //this._loginService.cookieChangeSource.next(this._cookieService.getObject('userData'));
		            if(this.response.reset_password=='n') {
	       				this._router.navigate(['/dashboard']);
	       			} else {
	       				this._router.navigate(['/reset_password']);
	       			}
	       		} else {
	       			this.errorMsg = this.response.message;
	       		}
	       	},
	       	err => {
	       		this.showLoader = false;
	       		this.errorMsg = "Something went wrong. Please try again."
	       	},
	       	function(){
	       		that.showLoader = false;
	       		//completed callback
	       	}
	    );
	}
	
	/////////Google Plus login///////////
	// public auth2: any;
	// public googleInit() {
	//     let that = this;
	//     gapi.load('auth2', function () {
	//       that.auth2 = gapi.auth2.init({
	//         client_id: GlobalVariable.GOOGLE_CLIENT_ID,
	//         cookiepolicy: 'single_host_origin',
	//         scope: 'profile email'
	//       });
	//       that.attachSignin(document.getElementById('googleBtn'));
	//     });
	// }

	// public attachSignin(element:any) {
	//   	let that = this;
	//     this.auth2.attachClickHandler(element, {},
	//       function (googleUser:any) {
	//         let profile = googleUser.getBasicProfile();
	//         var name = profile.getName();
	//         var res = name.split(" ");
	//         var firstname=res[0];
	//         var lastname=res[1];
	//         var email = profile.getEmail();
	//         var guser={};
	//         if(that.ipaddress){
	//         	guser['ip_address']=that.ipaddress;
	//         } else {
	//         	guser['ip_address']='';
	//         }
	//         guser['first_name'] = firstname;
	//         guser['last_name'] = lastname;
	//         if(email){
	//             guser['email'] = email;  
	//         }else{
	//             guser['email'] = '';  
	//         }
	//         guser['google_login_id'] = profile.getId();
	//         that._loginService.GoogleLogin(guser).subscribe(
	//            	data => {
 //       				that.response = data;
 //                   	if(that.response.status){
 //                    	let userData = {};
	// 	       			userData['uid'] = that.response.user_id;
	// 		            userData['first_name'] = that.response.first_name;
	// 		            userData['last_name'] = that.response.last_name;
	// 		            userData['email'] = email;
	// 		            userData['isLoggedIn'] = true;
	// 		            userData['auth_token'] = that.response.token;
	// 		            userData['user_type'] = this.response.designation;
	// 		            that._cookieService.putObject('userData', userData);
	// 		            that._router.navigate(["/dashboard"]);
 //                  	} else {
 //                       that.errorMsg = that.response.message;
 //                   	}
	//            },
	//            err => console.log(err),
	//            function(){
	//            }
	//         );
	//       }, function (error:any) {
	//     });
	// }

	ngAfterViewInit() {
	    // this.googleInit();
	    this.globalService.showLoaderSpinner(false);
	    // setTimeout(() =>{ this.globalService.showLoaderSpinner(false); }, 3000);
	}
	//////////////////OTP /////////////////////
    sendOtp(value:any) {
        var otpData={};
        otpData['username'] = value;
        this._loginService.optvaluesend(otpData).subscribe(
           	data => {
               	this.response = data;
               	if(this.response.status==1) {
                   this.otpField = true;
                   this.otpBtn = false;
               	} else {
                   this.errorMsg = this.response.message;
               	}
            },
           	err => console.log(err),
           	function(){
                   //completed callback
           	}
        );
    }

    checkLogin(formModel:any) {
        var otpCheck={};
        otpCheck['username'] = formModel.username;
        otpCheck['pin'] = formModel.otp;
        if(this.ipaddress){
        	otpCheck['ip_address'] = this.ipaddress;
        } else {
        	otpCheck['ip_address'] = "";
        }
        this._loginService.checkotp(otpCheck).subscribe(
           data => {
               	this.response = data;
               	if(this.response.user>0){
                    var userData = {};
	       			userData['uid'] = this.response.user_id;
		            userData['first_name'] = this.response.first_name;
		            userData['last_name'] = this.response.last_name;
		            userData['username'] = formModel.username;
		            // userData['is_otp'] = true;
		            userData['isLoggedIn'] = true;
		            // userData['keepLoggedIn'] = formModel.keep_login;
		            userData['auth_token'] = this.response.token;
		            userData['user_type'] = this.response.designation;
		            this._cookieService.putObject('userData', userData);
                    this._router.navigate(['/dashboard']);
               	} else {
                   this.errorMsg = this.response.status;
               	}  
           },
           err => console.log(err),
           function(){
                   //completed callback
           }
        );
    }
}