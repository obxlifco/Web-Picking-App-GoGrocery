import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { OrderComponent }  from '../../order/order/order.order.component';
import { OrderAddEditComponent,ManageTagsComponent,ManageTagsAddEditComponent ,SelectProductComponent,ViewOrderComponent }  from '../../order/order/order.order.addedit.component';
const routes: Routes = [	
    { path: '', component:OrderComponent },
    { path: 'add', component:OrderAddEditComponent },
    { path: 'edit/:id', component:OrderAddEditComponent },
    { path: 'details/:id', component:ViewOrderComponent }
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class OrderRoutingModule { }