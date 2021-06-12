import { Component } from '@angular/core';
import {Http} from '@angular/http';

import { LoginService } from './app.login.service';
import { Router } from '@angular/router';
import {CookieService} from 'ngx-cookie';

@Component({
  templateUrl: './templates/verification.html',
  providers: [LoginService]
})
export class VerifyCodeComponent  { 
	
	constructor(private _loginService: LoginService, private _router: Router, private _cookieService:CookieService) { }
	public response : any;
	public errorMsg: string;
	public successMsg: string;

	submitVerify(formModel:any){

		var forgot_data = this._cookieService.getObject('forgotPasswordData');
		if(forgot_data && forgot_data['email']){
			formModel.email = forgot_data['email'];
		}
		
		this._loginService.verifyCode(formModel).subscribe(
	       data => {
	       		this.response = data;
	       		if(this.response.status){
	       			
		            this._cookieService.putObject('forgotPasswordData', formModel);
	       			this._router.navigate(['/update_password']);

	       		}else{
	       			
	       			this.errorMsg = this.response.message;
	       		}
	       		
	       },
	       err => console.log(err),
	       function(){
	       		//completed callback
	       }
	    );
	}
}
