import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { BmscommonModule } from '../../bmscommon.module';
import { CourierRoutingModule } from './courier-routing.module';

import { CourierComponent }  from '../../order/courier/order.courier.component';
import { CourierAddEditComponent,AwbMasterComponent,ViewAwbComponent }  from '../../order/courier/order.courier.addedit.component';
@NgModule({
  imports: [
    CommonModule,
    CourierRoutingModule,
    BmscommonModule,
  ],
  declarations: [
    CourierComponent,
    CourierAddEditComponent,
    AwbMasterComponent,
    ViewAwbComponent
  ],
  entryComponents: [ 
  	CourierComponent,
    CourierAddEditComponent,
    AwbMasterComponent,
    ViewAwbComponent
  ]
})
export class CourierModule { }