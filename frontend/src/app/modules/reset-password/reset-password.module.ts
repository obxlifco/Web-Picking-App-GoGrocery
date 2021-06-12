import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ResetPasswordRoutingModule } from './reset-password-routing.module';
import { ResetPasswordComponent } from './reset-password.component';
import { FormsModule } from '@angular/forms';
import {PipeModule} from '../../global/pipes/pipe.module';

import {  MatCheckboxModule,MatOptionModule,MatSelectModule,MatRadioModule,
  MatIconModule,MatButtonModule,MatFormFieldModule,MatMenuModule,MatDatepickerModule, MatSlideToggleModule,
  MatRippleModule,
  MatSliderModule,
  MatTabsModule,
  MatNativeDateModule,
  MatChipsModule,
  MatAutocompleteModule,
  MatExpansionModule
} from '@angular/material';
import { MustMatchDirective } from '../../global/helper/must-match.directive';


@NgModule({
  declarations: [ResetPasswordComponent,MustMatchDirective],
  imports: [
    CommonModule,
    FormsModule,
    PipeModule,
    ResetPasswordRoutingModule,
    MatCheckboxModule,MatOptionModule,MatSelectModule,MatRadioModule,
    MatIconModule,MatButtonModule,MatFormFieldModule,MatMenuModule,MatDatepickerModule, MatSlideToggleModule,
    MatRippleModule,
    MatSliderModule,
    MatTabsModule,
    MatNativeDateModule,
    MatChipsModule,
    MatAutocompleteModule,
    MatExpansionModule
  ]
})
export class ResetPasswordModule { }
