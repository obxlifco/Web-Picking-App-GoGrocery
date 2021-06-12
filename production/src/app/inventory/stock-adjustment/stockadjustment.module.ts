import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { BmscommonModule } from '../../bmscommon.module';
import { StockAdjustmentRoutingModule } from './stockadjustment-routing.module';

import { StockAdjustmentComponent }  from '../../inventory/stock-adjustment/inventory.stock.adjustment.component';
import { PoProductViewComponent } from '../../inventory/stock-adjustment/inventory.stock.adjustment.component';
@NgModule({
  imports: [
    CommonModule,
    StockAdjustmentRoutingModule,
    BmscommonModule,
  ],
  declarations: [
    StockAdjustmentComponent,
    PoProductViewComponent
  ],
  entryComponents: [ 
  	StockAdjustmentComponent,
    PoProductViewComponent
  ]
})
export class StockAdjustmentModule { }