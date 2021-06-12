import { Component,OnInit } from '@angular/core';
import {Http} from '@angular/http';

import { LoginService } from './app.login.service';
import { Router } from '@angular/router';
import {CookieService} from 'ngx-cookie';
import { HeaderService } from '../partial-component/app.header.service';
import { GlobalService } from '../global/service/app.global.service';

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
  templateUrl: './templates/reset_password.html',
  providers: [LoginService,HeaderService,GlobalService],
  animations: [ loginTransition ],
  host: {
    '[@loginTransition]': ''
  }
})
export class ResetPasswordComponent  { 
	
	constructor(
	private _loginService: LoginService, 
	private _router: Router, 
	private _cookieService:CookieService,
	private _headerService:HeaderService,
	private _globalService:GlobalService
	) {
	}
	public response : any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};

	ngOnInit(){

		this.formModel.userId = this._globalService.getUserId();
		
	}

	submitResetPwd(formModel:any){

		this.errorMsg = '';

    	var data: any = {};
	    
        data.old_password = this.formModel.old_password;
     	data.new_password = this.formModel.password;
     	data.reset_password = 'n';
      	
        this._headerService.updatePassword(data,this.formModel.userId).subscribe(
           	resData => {
               	this.response = resData;
              
               	if(this.response.status==1){
               		this._router.navigate(['/']);
               		this.errorMsg = this.response.message;
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
