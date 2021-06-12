import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { ShippingMethodComponent }  from '../../inventory/po-shipping-method/inventory.shipping-method.component';
const routes: Routes = [	
    { path: '', component: ShippingMethodComponent }
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class ShippingMethodRoutingModule { }