import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginRoutingModule } from './login-routing.module';
import { LoginComponent } from './login.component';
import {SocialLoginModule} from '../social-login/social-login.module';
import {MaterialModule} from '../../global/modules/material.module';
import {PipeModule} from '../../global/pipes/pipe.module';
import {FormsModule} from '@angular/forms';
import { SharedModule } from '../../global/modules/shared.module';


@NgModule({
  declarations: [LoginComponent],
  imports: [
    CommonModule,
    LoginRoutingModule,
    SocialLoginModule,
    MaterialModule,
    PipeModule,
    FormsModule,
    SharedModule
  ]
})
export class LoginModule { }
