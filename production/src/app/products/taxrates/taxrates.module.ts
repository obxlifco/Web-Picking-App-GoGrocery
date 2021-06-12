import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BmscommonModule } from '../../bmscommon.module';

import { TaxratesRoutingModule } from './taxrates-routing.module';
import { TaxratesComponent, } from '../../products/taxrates/taxrates.component';
import { TaxrateaddeditComponent } from '../../products/taxrates/taxrateaddedit.component';
import { NgSelectModule } from '@ng-select/ng-select';

@NgModule({
  declarations: [
  TaxratesComponent,
  TaxrateaddeditComponent],
  imports: [
    CommonModule,
    TaxratesRoutingModule,
    BmscommonModule,
    NgSelectModule
  ]
})
export class TaxratesModule { }
