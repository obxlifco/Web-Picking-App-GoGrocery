import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BmscommonModule } from '../../bmscommon.module';

import { GlobalSetupRoutingModule } from './global-setup-routing.module';

import { GlobalSetupComponent } from './settings.global-setup.component';
import { GlobalSetupAddEditComponent } from './settings.global-setup.addedit.component';
import { NgSelectModule } from '@ng-select/ng-select';
@NgModule({
  declarations: [
    GlobalSetupComponent,
    GlobalSetupAddEditComponent,
  ],
  imports: [
    CommonModule,
    GlobalSetupRoutingModule,
    BmscommonModule,
    NgSelectModule
  ]
})
export class GlobalSetupModule { }
