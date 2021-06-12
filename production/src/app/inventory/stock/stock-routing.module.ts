import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { StockComponent }  from '../../inventory/stock/inventory.stock.component';
import { StockAddEditComponent, StockMoveComponent, SafetyStockComponent, ImportStockComponent} from '../../inventory/stock/inventory.stock.component';
const routes: Routes = [	
    { path: '', component: StockComponent }
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class StockRoutingModule { }