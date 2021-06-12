import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { BmscommonModule } from '../../bmscommon.module';
import { StockPriceRoutingModule } from './stock_price-routing.module';

import { StockPriceComponent, PriceComponent } from './inventory.stock_price.component';
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';
import { NgxMatSelectSearchModule } from 'ngx-mat-select-search';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';
import { InfiniteScrollModule } from 'ngx-infinite-scroll';
@NgModule({
  imports: [
    CommonModule,
    StockPriceRoutingModule,
    BmscommonModule,
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
    NgxMatSelectSearchModule,
    FormsModule,
    ReactiveFormsModule,
    NgSelectModule,
    InfiniteScrollModule
  ],
  declarations: [
    StockPriceComponent,
    PriceComponent
  ],
  entryComponents: [ 
    StockPriceComponent,
    PriceComponent
  ]
})
export class StockPriceModule { }