import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';
import { ReturnComponent, ViewOrderReturnComponent,RefundOrderComponent }  from '../../order/return/order.return.component';
const routes: Routes = [
    { path: 'list', component:ReturnComponent },
    { path: 'view/:id', component:ViewOrderReturnComponent },
    { path: 'refund_orders/:id/:canType', component:RefundOrderComponent }
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class ReturnRoutingModule { }