import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { WarehouseComponent }  from '../../inventory/warehouse/inventory.warehouse.component';
import { WarehouseAddEditComponent }  from '../../inventory/warehouse/inventory.warehouse.addedit.component';
const routes: Routes = [	
    { path: '', component: WarehouseComponent },
    { path: 'add', component: WarehouseAddEditComponent },
    { path: 'edit/:id', component: WarehouseAddEditComponent },
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class WarehouseRoutingModule { }