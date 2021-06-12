import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PriceCalculationRoutingModule } from './price-calculation-routing.module';
import { BmscommonModule } from '../../bmscommon.module';
import { PriceAddeditComponent } from './price.addedit.component';
import { PriceCalculationComponent } from './price-calculation.component';

@NgModule({
  declarations: [
    PriceAddeditComponent,
    PriceCalculationComponent,
  ],
  imports: [
    CommonModule,
    BmscommonModule,
    PriceCalculationRoutingModule
  ]
})
export class PriceCalculationModule { }
