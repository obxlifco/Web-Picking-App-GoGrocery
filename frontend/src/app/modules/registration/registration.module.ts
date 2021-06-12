import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RegistrationRoutingModule } from './registration-routing.module';
import { RegistrationComponent } from './registration.component';
import {SocialLoginModule} from '../social-login/social-login.module';
import {MaterialModule} from '../../global/modules/material.module';
import {PipeModule} from '../../global/pipes/pipe.module';
import {FormsModule} from '@angular/forms';
import { SharedModule } from '../../global/modules/shared.module';

@NgModule({
  declarations: [RegistrationComponent],
  imports: [
    CommonModule,
    RegistrationRoutingModule,
    SocialLoginModule,
    MaterialModule,
    PipeModule,
    FormsModule,
    SharedModule

  ]
})
export class RegistrationModule { }
