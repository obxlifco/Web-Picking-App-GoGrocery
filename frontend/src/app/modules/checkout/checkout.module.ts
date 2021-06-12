import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CheckoutRoutingModule } from './checkout-routing.module';
import {MaterialModule} from '../../global/modules/material.module';
import {PipeModule} from '../../global/pipes/pipe.module';
import { CheckoutComponent } from './checkout.component';
import { DeliveryaddressComponent } from './pages/deliveryaddress/deliveryaddress.component';
import { DeliveryoptionsComponent } from './pages/deliveryoptions/deliveryoptions.component';
import { PromocodeComponent } from './pages/promocode/promocode.component';
import { AddnewdeliveryaddressComponent } from './pages/addnewdeliveryaddress/addnewdeliveryaddress.component';
import {FormsModule,ReactiveFormsModule} from '@angular/forms';
import { SuccessComponent } from './pages/success/success.component';
import {OwlModule} from 'ngx-owl-carousel';
import { NgSelectModule } from '@ng-select/ng-select';

@NgModule({
  declarations: [
                 CheckoutComponent,
                 DeliveryaddressComponent,
                 DeliveryoptionsComponent,
                 PromocodeComponent,
                 AddnewdeliveryaddressComponent,
                 SuccessComponent
               ],
  imports: [
    CommonModule,
    MaterialModule,
    CheckoutRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    PipeModule,
    CheckoutRoutingModule,
    OwlModule,
    NgSelectModule

  ],
  exports:[SuccessComponent,AddnewdeliveryaddressComponent]
})
export class CheckoutModule { }
