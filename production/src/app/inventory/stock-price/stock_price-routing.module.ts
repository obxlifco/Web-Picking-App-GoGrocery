import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { StockPriceComponent }  from '../../inventory/stock-price/inventory.stock_price.component';
const routes: Routes = [	
    { path: '', component: StockPriceComponent }
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class StockPriceRoutingModule { }