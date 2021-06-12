import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { BmscommonModule } from '../../bmscommon.module';
import { ReturnRoutingModule } from './return-routing.module';

import { NgxBarcodeModule } from 'ngx-barcode';
import { NgxDaterangepickerMd } from 'ngx-daterangepicker-material';
import { ColorPickerModule } from 'ngx-color-picker';

import { ReturnComponent, ViewOrderReturnComponent,RefundOrderComponent,OrderActivityComponent, OrderReturnViewComponent, AssignDriverComponent }  from '../../order/return/order.return.component';
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';
import { NgxMatSelectSearchModule } from 'ngx-mat-select-search';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';

@NgModule({
  imports: [
    CommonModule,
    ReturnRoutingModule,
    BmscommonModule,
    NgxBarcodeModule,
    NgxDaterangepickerMd,
    ColorPickerModule,
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
    NgxMatSelectSearchModule,
    FormsModule,
    ReactiveFormsModule,
    NgSelectModule
  ],
  declarations: [
    ReturnComponent,
    ViewOrderReturnComponent,
    RefundOrderComponent,
    OrderActivityComponent,
    OrderReturnViewComponent,
    AssignDriverComponent
  ],
  entryComponents: [ 
  	ViewOrderReturnComponent,
    RefundOrderComponent,
    AssignDriverComponent
  ]
})
export class ReturnModule { }