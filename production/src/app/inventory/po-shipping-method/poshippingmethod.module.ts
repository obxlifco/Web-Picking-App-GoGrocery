import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { BmscommonModule } from '../../bmscommon.module';
import { ShippingMethodRoutingModule } from './poshippingmethod-routing.module';

import { ShippingMethodComponent }  from '../../inventory/po-shipping-method/inventory.shipping-method.component';
import { ShippingMethodAddEditComponent } from '../../inventory/po-shipping-method/inventory.shipping-method.addedit.component';
@NgModule({
  imports: [
    CommonModule,
    ShippingMethodRoutingModule,
    BmscommonModule,
  ],
  declarations: [
    ShippingMethodComponent,
    ShippingMethodAddEditComponent
  ],
  entryComponents: [ 
  	ShippingMethodComponent,
    ShippingMethodAddEditComponent
  ]
})
export class ShippingMethodModule { }