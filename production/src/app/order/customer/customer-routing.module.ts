import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { CustomerComponent }  from '../..//order/customer/order.customer.component';
import { CustomerAddEditComponent,CustomerAddEditAddressComponent,CustomerOrderListComponent} from '../../order/customer/order.customer.addedit.component';
const routes: Routes = [	
    { path: '', component: CustomerComponent },
    { path: 'add', component: CustomerAddEditComponent },
    { path: 'add/step2', component: CustomerAddEditAddressComponent },
    { path: 'add/:id/step2', component: CustomerAddEditAddressComponent },
    { path: 'add/:id/step3', component: CustomerOrderListComponent,data: {type:1}},
    { path: 'add/:id/step4', component: CustomerOrderListComponent,data: {type:2}},
    { path: 'edit/:id', component: CustomerAddEditComponent },
    { path: 'edit/:id/step2', component: CustomerAddEditAddressComponent },
    { path: 'edit/:id/step3', component: CustomerOrderListComponent,data: {type:1}},
    { path: 'edit/:id/step4', component: CustomerOrderListComponent,data: {type:2}},
 ];
@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class CustomerRoutingModule { }