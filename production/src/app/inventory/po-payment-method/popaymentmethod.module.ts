import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { BmscommonModule } from '../../bmscommon.module';
import { PaymentMethodRoutingModule } from './popaymentmethod-routing.module';

import { PaymentMethodComponent }  from '../../inventory/po-payment-method/inventory.payment-method.component';
import { PaymentMethodAddEditComponent } from '../../inventory/po-payment-method/inventory.payment-method.addedit.component';

@NgModule({
  imports: [
    CommonModule,
    PaymentMethodRoutingModule,
    BmscommonModule,
  ],
  declarations: [
    PaymentMethodComponent,
    PaymentMethodAddEditComponent
  ],
  entryComponents: [ 
    PaymentMethodComponent,
  	PaymentMethodAddEditComponent
  ]
})
export class PaymentMethodModule { }