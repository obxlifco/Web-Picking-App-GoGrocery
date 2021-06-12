import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BmscommonModule } from '../../bmscommon.module';

import { TaxsettingsRoutingModule } from './taxsettings-routing.module';

import { TaxsettingsComponent } from './taxsettings.component';
import { NgSelectModule } from '@ng-select/ng-select';
@NgModule({
  declarations: [TaxsettingsComponent],
  imports: [
  	RouterModule,
    BmscommonModule,
    CommonModule,
    TaxsettingsRoutingModule,
    NgSelectModule
  ]
})
export class TaxsettingsModule { }