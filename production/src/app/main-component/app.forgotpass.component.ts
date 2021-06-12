import { Component } from '@angular/core';
import {Http} from '@angular/http';

import { LoginService } from './app.login.service';
import { Router } from '@angular/router';
import {CookieService} from 'ngx-cookie';

import {trigger, stagger, animate, style, group, query, transition, keyframes} from '@angular/animations';
// const query = (s:any,a:any,o={optional:true})=>q(s,a,o);

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
  templateUrl: './templates/forgot_password.html',
  providers: [LoginService],
  animations: [ loginTransition ],
  host: {
    '[@loginTransition]': ''
  }
})
export class ForgotPasswordComponent  { 
	
	constructor(private _loginService: LoginService, private _router: Router, private _cookieService:CookieService) { }
	public response : any;
	public errorMsg: string;
	public successMsg: string;

	submitForgotPwd(formModel:any){

		this._loginService.checkEmail(formModel).subscribe(
	       data => {
	       		this.response = data;
	       		if(this.response.status){
	       			
		            this._cookieService.putObject('forgotPasswordData', formModel);
	       			this._router.navigate(['/verify_code']);

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
