import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { PaymentMethodComponent }  from '../../inventory/po-payment-method/inventory.payment-method.component';
const routes: Routes = [	
    { path: '', component: PaymentMethodComponent }
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class PaymentMethodRoutingModule { }