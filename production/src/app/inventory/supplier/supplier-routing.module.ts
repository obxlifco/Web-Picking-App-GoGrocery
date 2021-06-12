import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { SupplierComponent }  from '../../inventory/supplier/inventory.supplier.component';
import { SupplierPOComponent } from '../../inventory/supplier/inventory.supplier.po.component';
import { SupplierAddEditComponent }  from '../../inventory/supplier/inventory.supplier.addedit.component';
const routes: Routes = [	
    { path: '', component: SupplierComponent },
    { path: 'add', component: SupplierAddEditComponent },
    { path: 'add/purchase_order', component: SupplierPOComponent },
    { path: 'edit/:id', component: SupplierAddEditComponent },
    { path: 'edit/:id/purchase_order', component: SupplierPOComponent },
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class SupplierRoutingModule { }