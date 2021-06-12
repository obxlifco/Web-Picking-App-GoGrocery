import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { BmscommonModule } from '../../bmscommon.module';
import { StockRoutingModule } from './stock-routing.module';

import { StockComponent }  from '../../inventory/stock/inventory.stock.component';
import { StockAddEditComponent, StockMoveComponent, SafetyStockComponent, ImportStockComponent} from '../../inventory/stock/inventory.stock.component';
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';
import { NgxMatSelectSearchModule } from 'ngx-mat-select-search';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
@NgModule({
  imports: [
    CommonModule,
    StockRoutingModule,
    BmscommonModule,
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
    NgxMatSelectSearchModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  declarations: [
    StockComponent,
    StockAddEditComponent,
    StockMoveComponent,
    SafetyStockComponent,
    ImportStockComponent
  ],
  entryComponents: [ 
  	StockComponent,
    StockAddEditComponent,
    StockMoveComponent,
    SafetyStockComponent,
    ImportStockComponent
  ]
})
export class StockModule { }