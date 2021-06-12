import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { BmscommonModule } from '../../bmscommon.module';
import { OrderRoutingModule } from './order-routing.module';

import { NgxBarcodeModule } from 'ngx-barcode';
import { NgxDaterangepickerMd } from 'ngx-daterangepicker-material';
import { ColorPickerModule } from 'ngx-color-picker';

import { OrderComponent }  from '../../order/order/order.order.component';
import { OrderAddEditComponent,ManageTagsComponent,ManageTagsAddEditComponent,SelectProductComponent,ViewOrderComponent, OrderActivityComponent, ReturnOrderComponent }  from '../../order/order/order.order.addedit.component';
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';
import { MatFormFieldModule, MatSelectModule } from '@angular/material';
import { NgxMatSelectSearchModule } from 'ngx-mat-select-search';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';

@NgModule({
  imports: [
    CommonModule,
    OrderRoutingModule,
    BmscommonModule,
    NgxBarcodeModule,
    NgxDaterangepickerMd,
    ColorPickerModule,
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
    MatFormFieldModule,
    MatSelectModule,
    NgxMatSelectSearchModule,
    FormsModule,
    ReactiveFormsModule,
    NgSelectModule
  ],
  declarations: [
    OrderComponent,
    OrderAddEditComponent,
    ManageTagsComponent,
    ManageTagsAddEditComponent,
    SelectProductComponent,
    ViewOrderComponent,
    OrderActivityComponent,
    ReturnOrderComponent,
    // ColumnLayoutComponent
  ],
  entryComponents: [ 
  	OrderComponent,
    OrderAddEditComponent,
    ManageTagsComponent,
    ManageTagsAddEditComponent,
    SelectProductComponent,
    ViewOrderComponent,
    ReturnOrderComponent
  ]
})
export class OrderModule { }