import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { CustomerGroupComponent }  from '../../order/customer-group/order.customer-group.component';
import { CustomergroupAddeditComponent, OrderCustomerListComponent } from '../../order/customer-group/customergroup.addedit.component';

const routes: Routes = [	
    { path: '', component: CustomerGroupComponent },
    { path: 'add', component: CustomergroupAddeditComponent },
    { path: 'edit/:id', component: CustomergroupAddeditComponent },
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class CustomerGroupRoutingModule { }