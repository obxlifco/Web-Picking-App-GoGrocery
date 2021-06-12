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
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css'],
  animations: [ loginTransition ],
  host: {
    '[@loginTransition]': ''
  }
})
export class RegistrationComponent implements OnInit {
  public otpWindow:any;
  constructor() { }

  ngOnInit() {
  }

  userRegister(data:any){
    console.log(data);
    
  }
}
