import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GoogleLoginComponent } from './google-login/google-login.component';
import { FacebookLoginComponent } from './facebook-login/facebook-login.component';
import { MaterialModule } from '../../global/modules/material.module';
import {PipeModule} from '../../global/pipes/pipe.module';
import {FormsModule} from '@angular/forms';
import { SharedModule } from '../../global/modules/shared.module';

@NgModule({
  declarations: [GoogleLoginComponent, FacebookLoginComponent],
  imports: [
    CommonModule,
    MaterialModule,
    PipeModule,
    FormsModule,
    SharedModule
  ],
  exports : [
  	GoogleLoginComponent,
  	FacebookLoginComponent

  ]
})
export class SocialLoginModule { }
