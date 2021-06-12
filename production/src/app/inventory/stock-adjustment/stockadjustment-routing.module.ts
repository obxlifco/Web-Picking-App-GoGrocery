import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { StockAdjustmentComponent }  from '../../inventory/stock-adjustment/inventory.stock.adjustment.component';
import { PoProductViewComponent } from '../../inventory/stock-adjustment/inventory.stock.adjustment.component';
const routes: Routes = [	
    { path: '', component: StockAdjustmentComponent }
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class StockAdjustmentRoutingModule { }