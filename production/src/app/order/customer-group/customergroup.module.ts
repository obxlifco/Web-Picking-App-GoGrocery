import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { BmscommonModule } from '../../bmscommon.module';
import { CustomerGroupRoutingModule } from './customergroup-routing.module';

import { CustomerGroupComponent }  from '../../order/customer-group/order.customer-group.component';
import { CustomergroupAddeditComponent, OrderCustomerListComponent } from '../../order/customer-group/customergroup.addedit.component';
@NgModule({
  imports: [
    CommonModule,
    CustomerGroupRoutingModule,
    BmscommonModule,
  ],
  declarations: [
    CustomerGroupComponent,
    CustomergroupAddeditComponent,
    OrderCustomerListComponent
  ],
  entryComponents: [ 
  	CustomerGroupComponent,
    CustomergroupAddeditComponent,
    OrderCustomerListComponent
  ]
})
export class CustomerGroupModule { }