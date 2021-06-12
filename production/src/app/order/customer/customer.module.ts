import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { BmscommonModule } from '../../bmscommon.module';
import { CustomerRoutingModule } from './customer-routing.module';

import { NgxBarcodeModule } from 'ngx-barcode';
import { NgxDaterangepickerMd } from 'ngx-daterangepicker-material';
import { ColorPickerModule } from 'ngx-color-picker';
// import { SafeHtmlPipe } from '../../global/pipes/safe-html.pipe';
import { CustomerComponent }  from '../..//order/customer/order.customer.component';
import { CustomerAddEditComponent,CustomerAddEditAddressComponent,CustomerOrderListComponent} from '../../order/customer/order.customer.addedit.component';
@NgModule({
  imports: [
    CommonModule,
    CustomerRoutingModule,
    BmscommonModule,
    NgxBarcodeModule,
    NgxDaterangepickerMd,
    ColorPickerModule,
  ],
  declarations: [
    CustomerComponent,
    CustomerAddEditComponent,
    CustomerAddEditAddressComponent,
    CustomerOrderListComponent
  ],
  entryComponents: [ 
  	CustomerComponent,
    CustomerAddEditComponent,
    CustomerAddEditAddressComponent,
    CustomerOrderListComponent
  ]
})

export class CustomerModule { }
