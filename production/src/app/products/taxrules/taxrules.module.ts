import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BmscommonModule } from '../../bmscommon.module';

import { TaxrulesComponent } from '../../products/taxrules/taxrules.component';
import { TaxruleaddeditComponent } from '../../products/taxrules/taxruleaddedit.component';

import { TaxrulesRoutingModule } from './taxrules-routing.module';
import { NgSelectModule } from '@ng-select/ng-select';

@NgModule({
  declarations: [
  	TaxrulesComponent,
  	TaxruleaddeditComponent
  ],
  imports: [
    CommonModule,
    TaxrulesRoutingModule,
    BmscommonModule,
    NgSelectModule
  ]
})
export class TaxrulesModule { }
