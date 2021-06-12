import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { PurchaseOrderComponent }  from '../../inventory/purchase-order/inventory.purchase-order.component';
import { PurchaseOrderAddEditComponent,PurchaseOrderViewComponent,PurchaseOrderGrnComponent }  from '../../inventory/purchase-order/inventory.purchase-order.addedit.component';

const routes: Routes = [	
    { path: '', component: PurchaseOrderComponent },
    { path: 'add', component: PurchaseOrderAddEditComponent },
    { path: 'edit/:id', component: PurchaseOrderAddEditComponent },
    { path: 'view', component: PurchaseOrderViewComponent },
    { path: 'view/:id', component: PurchaseOrderViewComponent },
    { path: 'grn/:id', component: PurchaseOrderGrnComponent },
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class PurchaseOrderRoutingModule { }