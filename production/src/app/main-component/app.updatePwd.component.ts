import { Component } from '@angular/core';
import {Http} from '@angular/http';

import { LoginService } from './app.login.service';
import { Router } from '@angular/router';
import {CookieService} from 'ngx-cookie';

@Component({
  templateUrl: './templates/update_password.html',
  providers: [LoginService]
})
export class UpdatePasswordComponent  { 
	
	constructor(private _loginService: LoginService, private _router: Router, private _cookieService:CookieService) { }
	public response : any;
	public errorMsg: string;
	public successMsg: string;

	submitUpdatePwd(formModel:any, form:any){

		var forgot_data = this._cookieService.getObject('forgotPasswordData');
		if(forgot_data && forgot_data['code']){
			formModel.code = forgot_data['code'];
		}
		this._loginService.changePwd(formModel).subscribe(
	       data => {
	       		this.response = data;
	       		if(this.response.status){
	       			this._cookieService.remove('forgotPasswordData');
		            this.successMsg = this.response.message;
		            form.resetForm();
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
